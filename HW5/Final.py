import BaseLibraryNew as lib

all_walks = lib.monte_carlo_walk(50, 100)

for length, walks in all_walks.items():
    walks_len_6_or_less = 0
    for x, dist in walks:
        if dist <= 6:
            walks_len_6_or_less += 1
    print(f"Walks of length {length:3} are with a probability of {(walks_len_6_or_less / len(walks)) * 100:.2f} % short.")