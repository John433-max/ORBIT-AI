"""
A real, from-scratch byte-pair-encoding tokenizer — trained on this repo's
own corpus, not the byte-level fallback used until now. DESIGN.md Part 4
specified this as the production approach and Part 18 flagged the byte-level
tokenizer as a stand-in; this closes that gap.

Algorithm (standard BPE, GPT-2-style byte-level base alphabet so any UTF-8
text still round-trips losslessly even for merges the training corpus never
saw):
1. Pretokenize on whitespace/non-whitespace runs (a simplified version of
   GPT-2's regex split — good enough at this corpus size, doesn't need to
   handle contractions/punctuation edge cases specially).
2. Represent each pretoken as a sequence of byte ids (0-255).
3. Repeatedly find the most frequent adjacent pair across the whole corpus
   and merge it into a new token id, recording the merge rule.
4. Stop at a target vocab size or when no pair repeats.

Encoding a new string applies the learned merges in the order they were
learned (standard BPE encode). Because the base alphabet is raw bytes, any
input — including bytes/words never seen in training — still encodes and
decodes losslessly; unseen text just doesn't benefit from any merges.
"""
import re
import json
from collections import Counter

_PRETOKEN_RE = re.compile(r"\s+|\S+")


class BPETokenizer:
    def __init__(self):
        self.merges: dict[tuple[int, int], int] = {}   # (a,b) -> new_id, in learned order
        self.merge_order: list[tuple[int, int]] = []
        self.next_id = 256
        self.BOS = None
        self.EOS = None
        self.PAD = None

    @property
    def VOCAB_SIZE(self):
        return self.next_id + 3  # + BOS/EOS/PAD

    def _pretokenize(self, text: str):
        return [m.group(0) for m in _PRETOKEN_RE.finditer(text)]

    def train(self, text: str, vocab_size: int = 700, min_frequency: int = 2, verbose: bool = False):
        words = self._pretokenize(text)
        word_freq = Counter(words)
        unique_words = list(word_freq.keys())
        freqs = [word_freq[w] for w in unique_words]
        seqs = [list(w.encode("utf-8", errors="replace")) for w in unique_words]
        n_merges_target = max(0, vocab_size - 256 - 3)

        for step in range(n_merges_target):
            pair_counts = Counter()
            for seq, freq in zip(seqs, freqs):
                for i in range(len(seq) - 1):
                    pair_counts[(seq[i], seq[i + 1])] += freq
            if not pair_counts:
                break
            best_pair, best_count = pair_counts.most_common(1)[0]
            if best_count < min_frequency:
                break
            new_id = self.next_id
            self.next_id += 1
            self.merges[best_pair] = new_id
            self.merge_order.append(best_pair)
            new_seqs = []
            for seq in seqs:
                merged = []
                i = 0
                while i < len(seq):
                    if i < len(seq) - 1 and (seq[i], seq[i + 1]) == best_pair:
                        merged.append(new_id)
                        i += 2
                    else:
                        merged.append(seq[i])
                        i += 1
                new_seqs.append(merged)
            seqs = new_seqs
            if verbose and step % 50 == 0:
                print(f"  merge {step}: {best_pair} -> {new_id} (count={best_count})")

        self.BOS, self.EOS, self.PAD = self.next_id, self.next_id + 1, self.next_id + 2
        return self

    def _apply_merges(self, byte_ids: list) -> list:
        seq = list(byte_ids)
        for pair in self.merge_order:
            merged = []
            i = 0
            new_id = self.merges[pair]
            while i < len(seq):
                if i < len(seq) - 1 and (seq[i], seq[i + 1]) == pair:
                    merged.append(new_id)
                    i += 2
                else:
                    merged.append(seq[i])
                    i += 1
            seq = merged
        return seq

    def encode(self, text: str, add_bos=True, add_eos=True) -> list:
        ids = []
        cache = {}
        for word in self._pretokenize(text):
            cached = cache.get(word)
            if cached is None:
                cached = self._apply_merges(list(word.encode("utf-8", errors="replace")))
                cache[word] = cached
            ids.extend(cached)
        if add_bos:
            ids = [self.BOS] + ids
        if add_eos:
            ids = ids + [self.EOS]
        return ids

    def _id_to_bytes(self, token_id: int) -> bytes:
        if token_id < 256:
            return bytes([token_id])
        for (a, b), new_id in self.merges.items():
            if new_id == token_id:
                return self._id_to_bytes(a) + self._id_to_bytes(b)
        return b""

    def decode(self, ids: list) -> str:
        out = bytearray()
        for i in ids:
            if i in (self.BOS, self.EOS, self.PAD):
                continue
            out += self._id_to_bytes(i)
        return bytes(out).decode("utf-8", errors="replace")

    def save(self, path: str):
        data = {
            "merge_order": self.merge_order,
            "next_id": self.next_id,
            "BOS": self.BOS, "EOS": self.EOS, "PAD": self.PAD,
        }
        with open(path, "w") as f:
            json.dump(data, f)

    @classmethod
    def load(cls, path: str):
        with open(path) as f:
            data = json.load(f)
        tok = cls()
        tok.merge_order = [tuple(p) for p in data["merge_order"]]
        tok.next_id = 256
        for pair in tok.merge_order:
            tok.merges[pair] = tok.next_id
            tok.next_id += 1
        tok.BOS, tok.EOS, tok.PAD = data["BOS"], data["EOS"], data["PAD"]
        return tok


if __name__ == "__main__":
    from dataset import build_corpus
    train_text, val_text, _ = build_corpus()
    tok = BPETokenizer().train(train_text + "\n" + val_text, vocab_size=700, verbose=True)
    print(f"\nLearned {len(tok.merge_order)} merges, vocab size {tok.VOCAB_SIZE}")

    sample = "the orchestrator routes a request to the coding agent"
    ids = tok.encode(sample)
    back = tok.decode(ids)
    print(f"\nsample: {sample!r}")
    print(f"tokens: {len(ids)} (vs {len(sample.encode('utf-8'))} bytes -> "
          f"{len(ids) / len(sample.encode('utf-8')) * 100:.0f}% of byte-level length)")
    print(f"round-trip ok: {back == sample}")

    unseen = "zzqx unseen gibberish 你好"
    ids2 = tok.encode(unseen)
    print(f"\nunseen text round-trip ok: {tok.decode(ids2) == unseen}")

    tok.save("bpe_tokenizer.json")
    print("\nsaved to bpe_tokenizer.json")
