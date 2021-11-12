import corrected_01

repetitions = 1_000
max_blocks = 50

results = corrected_01.monte_carlo_walk_analysis(max_blocks, repetitions)

round_trips_len4 = [walk for walk in results[4] if walk[1] == 0]

# roundtrips = {k: {tuple(i) for i in [v[0] for v in results[k] if v[1] == 0]} for k in results}
# overview = {(k, len(roundtrips[k])): list(roundtrips[k][:10]) for k in results}

roundtrips = {b: {tuple(walk[0]) for walk in results[b] if walk[1] == 0} for b in results.keys()}

import statistics

avg_dist = {n: (statistics.mean([walkinfo[1] for walkinfo in results[n]]), statistics.median([walkinfo[1] for walkinfo in results[n]])) for n in range(5, 26, 5)}

