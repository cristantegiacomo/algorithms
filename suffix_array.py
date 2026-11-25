from collections.abc import Sequence

def build_suffix_array(seq: str | Sequence[int]) -> tuple[list[int], list[int], list[int]]:
    """
    Costruisce Suffix Array, Rank Array e LCP Array in O(N log^2 N).
    """

    n = len(seq)
    if n == 0:
        return [], [], [] # (sa, rk, lcp)

    # Normalizza tutti gli elementi a interi >= 1 (0 riservato alla sentinella $ o % o... che indica fine stringa)
    if isinstance(seq, str):
        rk = [ord(c) + 1 for c in seq]
    else:
        min_val = min(seq)
        offset = 1 - min_val if min_val <= 0 else 0
        rk = [x + offset for x in seq]

    base = max(max(rk), n) + 2
    sa = list(range(n))
    k = 1

    # 1. Prefix Doubling - O(N log^2 N)
    while k < n:
        key = [rk[i] * base + (rk[i + k] + 1 if i + k < n else 0) for i in range(n)]
        sa.sort(key=lambda x: key[x])

        new_rk = [0] * n
        for r in range(1, n):
            new_rk[sa[r]] = new_rk[sa[r - 1]] + (key[sa[r]] != key[sa[r - 1]])
        rk = new_rk

        if rk[sa[-1]] == n - 1:
            break
        k *= 2

    # 2. Kasai LCP - O(N)
    lcp = [0] * n
    h = 0
    for i in range(n):
        if rk[i] == 0:
            h = 0
            continue
        j = sa[rk[i] - 1]
        while i + h < n and j + h < n and seq[i + h] == seq[j + h]:
            h += 1
        lcp[rk[i]] = h
        if h > 0:
            h -= 1

    return sa, rk, lcp