import BaseLibraryNew as lib
import tracemalloc as tracer

tracer.start()

walk_dict = lib.monte_carlo_walk_analysis(20, 10_000)
walk_snapshot = tracer.take_snapshot()
_, walk_peak = tracer.get_traced_memory()
tracer.reset_peak()
tracer.stop()

tracer.start()
dist_dict = lib.monte_carlo_walk(20, 10_000)
dist_snapshot = tracer.take_snapshot()
_, dist_peak = tracer.get_traced_memory()

diff = dist_snapshot.compare_to(walk_snapshot, 'lineno')

print(f"Peak memory used with walk saving: {walk_peak}")
print(f"Peak memory used with no walk saving: {dist_peak}")

print("[ Difference in the 10 most allocation heavy lines ]")
for entry in diff[:10]:
    print(entry)
