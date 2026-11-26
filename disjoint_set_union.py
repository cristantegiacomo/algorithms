n = 5
parent = list(range(n + 1))
rank = [1] * (n + 1)


def find(x: int) -> int:     # O(α(N)) ammortizzato; --> (~O(1))
    if parent[x] != x:
        parent[x] = find(parent[x])
    return parent[x]


def union(x: int, y: int) -> bool:  # O(α(N)) se ammortizzato (perché worst case sarebbe O(logN)). Si puo anche considerare come (~O(1))
    p1, p2 = find(x), find(y)
    if p1 == p2:
        return False
    if rank[p1] >= rank[p2]:
        parent[p2] = p1
        rank[p1] += rank[p2]
    else:
        parent[p1] = p2
        rank[p2] += rank[p1]
    return True



# Esempio 
# creazione grafo non orientato
components = n
for u, v in [(1, 2), (2, 3)]:
    if union(u, v):
        components -= 1             # components -> 3 ({1,2,3}, {4}, {5})

# queries
is_cycle = not union(1, 3)          # True (1 e 3 già connessi)
connected = find(1) == find(3)      # True
disconnected = find(1) == find(4)   # False
size = rank[find(2)]                # 3 (leggere sempre tramite find(x))
roots = {find(i) for i in range(1, n + 1)}  # {1, 4, 5} — O(N · α(N)). nota itera su n non su components e trasforma in set {}