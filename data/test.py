artists = [
    ['/johnny-hallyday', 4],
    ['/kendji-girac', 7]
]


for n in range(len(artists)):
    print(n)
    for p in range(1, artists[n][1]+1):
        if p == 1:
            print(f"n={n}")
            print(f"p={p}")
            link = artists[n][0]
            print(link)
        else:
            print(f"n={n}")
            print(f"p={p}")
            link = f"{artists[n][0]}-{p}"
            print(link)
