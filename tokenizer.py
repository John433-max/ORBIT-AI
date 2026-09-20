"""
Byte-level tokenizer.

Honest toy-scale stand-in for trained BPE: zero training data, lossless
round-trip, same fallback layer GPT-style byte BPE bottoms out on.
"""

class ByteTokenizer:
    BOS, EOS, PAD = 256, 257, 258
    VOCAB_SIZE = 259

    def encode(self, text: str, add_bos=True, add_eos=True):
        ids = list(text.encode("utf-8", errors="replace"))
        if add_bos:
            ids = [self.BOS] + ids
        if add_eos:
            ids = ids + [self.EOS]
        return ids

    def decode(self, ids):
        byte_ids = [i for i in ids if i < 256]
        return bytes(byte_ids).decode("utf-8", errors="replace")
