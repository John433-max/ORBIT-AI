"""Cycle 578: Number-theoretic and transform templates.

Closes educational gaps for:
- Number-theoretic transform (NTT) polynomial multiplication
- Cooley–Tukey FFT polynomial multiplication (complex, rounded)
- Miller–Rabin probabilistic primality
- Pollard's Rho factorization (one non-trivial factor)
- Baby-step giant-step discrete logarithm
- Matrix exponentiation (binary, optional modulus)

Matchers are phrase-specific so existing Rabin–Karp / prime / power
templates are not stolen. Self-checking examples keep verification deterministic.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "ntt_poly_mul",
            "def ntt_poly_mul(a, b):\n"
            '    """Multiply polynomials via NTT mod 998244353.\n\n'
            "    a, b are coefficient lists (low degree first).\n"
            "    Returns coefficients of the product, trailing zeros trimmed.\n"
            '    """\n'
            "    MOD = 998244353\n"
            "    ROOT = 3\n"
            "    def _pow(x, n):\n"
            "        r = 1\n"
            "        x %= MOD\n"
            "        while n:\n"
            "            if n & 1:\n"
            "                r = r * x % MOD\n"
            "            x = x * x % MOD\n"
            "            n >>= 1\n"
            "        return r\n"
            "    def _ntt(p, invert):\n"
            "        n = len(p)\n"
            "        j = 0\n"
            "        for i in range(1, n):\n"
            "            bit = n >> 1\n"
            "            while j & bit:\n"
            "                j ^= bit\n"
            "                bit >>= 1\n"
            "            j ^= bit\n"
            "            if i < j:\n"
            "                p[i], p[j] = p[j], p[i]\n"
            "        length = 2\n"
            "        while length <= n:\n"
            "            wlen = _pow(ROOT, (MOD - 1) // length)\n"
            "            if invert:\n"
            "                wlen = _pow(wlen, MOD - 2)\n"
            "            for i in range(0, n, length):\n"
            "                w = 1\n"
            "                half = length // 2\n"
            "                for k in range(half):\n"
            "                    u = p[i + k]\n"
            "                    v = p[i + k + half] * w % MOD\n"
            "                    p[i + k] = (u + v) % MOD\n"
            "                    p[i + k + half] = (u - v) % MOD\n"
            "                    w = w * wlen % MOD\n"
            "            length <<= 1\n"
            "        if invert:\n"
            "            inv_n = _pow(n, MOD - 2)\n"
            "            for i in range(n):\n"
            "                p[i] = p[i] * inv_n % MOD\n"
            "        return p\n"
            "    if not a or not b:\n"
            "        return []\n"
            "    n = 1\n"
            "    need = len(a) + len(b) - 1\n"
            "    while n < need:\n"
            "        n <<= 1\n"
            "    fa = [(x % MOD) for x in a] + [0] * (n - len(a))\n"
            "    fb = [(x % MOD) for x in b] + [0] * (n - len(b))\n"
            "    _ntt(fa, False)\n"
            "    _ntt(fb, False)\n"
            "    for i in range(n):\n"
            "        fa[i] = fa[i] * fb[i] % MOD\n"
            "    _ntt(fa, True)\n"
            "    out = fa[:need]\n"
            "    while out and out[-1] == 0:\n"
            "        out.pop()\n"
            "    return out\n",
            lambda low: bool(
                re.search(r"\bntt\b", low)
                or re.search(r"\bnumber[- ]theoretic[- ]transform\b", low)
                or re.search(r"\bmodular[- ]fft\b", low)
            ),
            examples=(
                (([1, 1], [1, 2]), [1, 3, 2]),
                (([1, 2, 3], [4, 5]), [4, 13, 22, 15]),
                (([1], [1, 0, 1]), [1, 0, 1]),
            ),
        ),
        T(
            "fft_poly_mul",
            "def fft_poly_mul(a, b):\n"
            '    """Multiply polynomials via Cooley–Tukey FFT (complex, rounded).\n\n'
            "    a, b are coefficient lists (low degree first).\n"
            "    Returns integer coefficients of the product.\n"
            '    """\n'
            "    import cmath\n"
            "    def _fft(p, invert):\n"
            "        n = len(p)\n"
            "        if n <= 1:\n"
            "            return p\n"
            "        even = _fft(p[0::2], invert)\n"
            "        odd = _fft(p[1::2], invert)\n"
            "        ang = (2 * cmath.pi / n) * (-1 if invert else 1)\n"
            "        w = 1\n"
            "        wn = cmath.exp(1j * ang)\n"
            "        out = [0] * n\n"
            "        half = n // 2\n"
            "        for k in range(half):\n"
            "            t = w * odd[k]\n"
            "            out[k] = even[k] + t\n"
            "            out[k + half] = even[k] - t\n"
            "            w *= wn\n"
            "        return out\n"
            "    if not a or not b:\n"
            "        return []\n"
            "    n = 1\n"
            "    need = len(a) + len(b) - 1\n"
            "    while n < need:\n"
            "        n <<= 1\n"
            "    fa = [complex(x) for x in a] + [0j] * (n - len(a))\n"
            "    fb = [complex(x) for x in b] + [0j] * (n - len(b))\n"
            "    fa = _fft(fa, False)\n"
            "    fb = _fft(fb, False)\n"
            "    fa = [fa[i] * fb[i] for i in range(n)]\n"
            "    fa = _fft(fa, True)\n"
            "    out = [int(round(fa[i].real / n)) for i in range(need)]\n"
            "    while out and out[-1] == 0:\n"
            "        out.pop()\n"
            "    return out\n",
            lambda low: bool(
                re.search(r"\bfft\b", low)
                or re.search(r"\bfast fourier\b", low)
            )
            and "ntt" not in low
            and "number theoretic" not in low
            and "modular" not in low,
            examples=(
                (([1, 1], [1, 2]), [1, 3, 2]),
                (([1, 2, 3], [4, 5]), [4, 13, 22, 15]),
                (([3, 0, 1], [2, 1]), [6, 3, 2, 1]),
            ),
        ),
        T(
            "miller_rabin_primality",
            "def miller_rabin(n, k=8):\n"
            '    """Miller–Rabin probabilistic primality test.\n\n'
            "    Returns True if n is probably prime, False if composite.\n"
            "    Deterministic for n < 2**32 with fixed bases when k is large enough;\n"
            "    educational implementation uses small fixed bases.\n"
            '    """\n'
            "    if n < 2:\n"
            "        return False\n"
            "    small = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29)\n"
            "    for p in small:\n"
            "        if n == p:\n"
            "            return True\n"
            "        if n % p == 0:\n"
            "            return False\n"
            "    # Write n-1 = 2^s * d\n"
            "    d = n - 1\n"
            "    s = 0\n"
            "    while d % 2 == 0:\n"
            "        d //= 2\n"
            "        s += 1\n"
            "    bases = (2, 3, 5, 7, 11, 13, 23, 29)[: max(1, min(k, 8))]\n"
            "    for a in bases:\n"
            "        if a >= n:\n"
            "            continue\n"
            "        x = pow(a, d, n)\n"
            "        if x == 1 or x == n - 1:\n"
            "            continue\n"
            "        for _ in range(s - 1):\n"
            "            x = pow(x, 2, n)\n"
            "            if x == n - 1:\n"
            "                break\n"
            "        else:\n"
            "            return False\n"
            "    return True\n",
            lambda low: bool(
                re.search(r"\bmiller[- ]?rabin\b", low)
                or re.search(r"\bprobabilistic primality\b", low)
                or (
                    "primality" in low
                    and ("miller" in low or "rabin" in low)
                )
            )
            and "karp" not in low,
            examples=(
                ((17,), True),
                ((15,), False),
                ((2,), True),
                ((1,), False),
                ((7919,), True),
                ((561,), False),  # Carmichael number, caught by MR
            ),
        ),
        T(
            "pollard_rho_factor",
            "def pollard_rho(n):\n"
            '    """Find one non-trivial factor of n via Pollard\'s Rho.\n\n'
            "    Returns a proper divisor, or n if n is prime / failure on this seed.\n"
            "    Educational Brent-style cycle; not guaranteed for all composites.\n"
            '    """\n'
            "    import math\n"
            "    if n % 2 == 0:\n"
            "        return 2\n"
            "    if n % 3 == 0:\n"
            "        return 3\n"
            "    def _f(x, c):\n"
            "        return (x * x + c) % n\n"
            "    for c in (1, 2, 3):\n"
            "        x = y = 2\n"
            "        d = 1\n"
            "        while d == 1:\n"
            "            x = _f(x, c)\n"
            "            y = _f(_f(y, c), c)\n"
            "            d = math.gcd(abs(x - y), n)\n"
            "            if d == n:\n"
            "                break\n"
            "        if 1 < d < n:\n"
            "            return d\n"
            "    return n\n",
            lambda low: bool(
                re.search(r"\bpollard(?:['’]s)?[- ]?rho\b", low)
                or re.search(r"\bpollard[- ]rho\b", low)
            ),
            examples=(
                ((91,), 7),   # 7*13; rho typically finds 7
                ((15,), 3),
                ((77,), 7),
                ((4,), 2),
            ),
        ),
        T(
            "baby_step_giant_step",
            "def discrete_log(a, b, p):\n"
            '    """Baby-step giant-step discrete log: find x with a^x ≡ b (mod p).\n\n'
            "    p should be prime. Returns the smallest non-negative x, or None.\n"
            '    """\n'
            "    import math\n"
            "    if p <= 1:\n"
            "        return None\n"
            "    a %= p\n"
            "    b %= p\n"
            "    if b == 1:\n"
            "        return 0\n"
            "    m = int(math.isqrt(p - 1)) + 1\n"
            "    baby = {}\n"
            "    cur = 1\n"
            "    for j in range(m):\n"
            "        if cur not in baby:\n"
            "            baby[cur] = j\n"
            "        cur = cur * a % p\n"
            "    factor = pow(a, m * (p - 2), p)  # a^{-m} via Fermat\n"
            "    cur = b\n"
            "    for i in range(m):\n"
            "        if cur in baby:\n"
            "            return i * m + baby[cur]\n"
            "        cur = cur * factor % p\n"
            "    return None\n",
            lambda low: bool(
                re.search(r"\bbaby[- ]step[- ]giant[- ]step\b", low)
                or re.search(r"\bbsgs\b", low)
                or re.search(r"\bdiscrete[- ]log(?:arithm)?\b", low)
            ),
            examples=(
                ((2, 8, 13), 3),
                ((2, 1, 5), 0),
                ((3, 6, 7), 3),  # 3^3 = 27 ≡ 6 (mod 7)
                ((2, 3, 5), 3),  # 2^3 = 8 ≡ 3 (mod 5)
            ),
        ),
        T(
            "matrix_exponentiation",
            "def matrix_pow(M, n, mod=None):\n"
            '    """Binary matrix exponentiation.\n\n'
            "    M is a square list-of-lists. Returns M^n.\n"
            "    If mod is set, all entries are reduced modulo mod.\n"
            '    """\n'
            "    if n < 0:\n"
            "        raise ValueError('n must be non-negative')\n"
            "    size = len(M)\n"
            "    def mul(A, B):\n"
            "        C = [[0] * size for _ in range(size)]\n"
            "        for i in range(size):\n"
            "            for k in range(size):\n"
            "                aik = A[i][k]\n"
            "                if not aik:\n"
            "                    continue\n"
            "                for j in range(size):\n"
            "                    C[i][j] += aik * B[k][j]\n"
            "                    if mod is not None:\n"
            "                        C[i][j] %= mod\n"
            "        return C\n"
            "    # Identity\n"
            "    result = [[1 if i == j else 0 for j in range(size)] for i in range(size)]\n"
            "    base = [row[:] for row in M]\n"
            "    while n:\n"
            "        if n & 1:\n"
            "            result = mul(result, base)\n"
            "        base = mul(base, base)\n"
            "        n >>= 1\n"
            "    return result\n",
            lambda low: bool(
                re.search(r"\bmatrix[- ]exponentiation\b", low)
                or re.search(r"\bmatrix[- ]pow(?:er)?\b", low)
                or re.search(r"\bpow(?:er)? a matrix\b", low)
            )
            and "polynomial" not in low,
            examples=(
                (([[1, 1], [1, 0]], 5), [[8, 5], [5, 3]]),  # Fib matrix^5
                (([[2, 0], [0, 2]], 3), [[8, 0], [0, 8]]),
                (([[1, 1], [1, 0]], 5, 10), [[8, 5], [5, 3]]),
            ),
        ),
    ]
