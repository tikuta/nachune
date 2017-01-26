def smith_waterman(s1: str, s2: str) -> int:
    match = 2
    mismatch = -2
    gap = -1

    mat = [[0 for i in range(len(s1) + 1)] for j in range(len(s2) + 1)]

    for j in range(len(mat)):
        for i in range(len(mat[j])):
            if i == 0 or j == 0:
                continue

            upper_left = mat[j - 1][i - 1] + match if s1[i - 1] == s2[j - 1] else mat[j - 1][i - 1] + mismatch
            left = mat[j - 1][i - 1] + gap
            upper = mat[j - 1][i - 1] + gap

            mat[j][i] = max(upper_left, left, upper, 0)
    return max(max(l) for l in mat)
