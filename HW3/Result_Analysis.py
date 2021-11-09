import HW1.basic_library as walk_generator
import statistics

walks = walk_generator.monte_carlo_walk_analysis(50, 10_000)

len4Roundtrips = [w for w, dist in walks[4] if dist == 0]

print(len(len4Roundtrips))

allRoundTrips = {k: [w for w, dist in walks[k] if dist == 0] for k in walks}
uniqueRoundTrips = {k: {tuple(w) for w in allRoundTrips[k]} for k in allRoundTrips}
first10RoundTrips = {k: [w for w in list(uniqueRoundTrips[k])[:10]] for k in uniqueRoundTrips}

print(len(uniqueRoundTrips))
print(first10RoundTrips)


def calculate_mean(walk):
    dist = [dist for w, dist in walk]
    return statistics.mean(dist)


def calculate_median(walk):
    dist = [dist for w, dist in walk]
    dist.sort()
    return statistics.median(dist)


print("List of 5")
print("Mean: " + str(calculate_mean(walks[5])))
print("Median: " + str(calculate_median(walks[5])))

print("List of 10")
print("Mean: " + str(calculate_mean(walks[10])))
print("Median: " + str(calculate_median(walks[10])))

print("List of 15")
print("Mean: " + str(calculate_mean(walks[15])))
print("Median: " + str(calculate_median(walks[15])))

print("List of 20")
print("Mean: " + str(calculate_mean(walks[20])))
print("Median: " + str(calculate_median(walks[20])))

print("List of 25")
print("Mean: " + str(calculate_mean(walks[25])))
print("Median: " + str(calculate_median(walks[25])))

maxPossibleDist = {k: [(w, dist) for w, dist in walks[k] if dist == k] for k in walks}
maxPossibleDistPercentage = {k: (len(maxPossibleDist[k]) / len(walks[k]) * 100) for k in walks}

print(maxPossibleDistPercentage)

def checkEqual(iterator):
    if len(iterator) == 0:
        return True
    for x in iterator:
        if x != iterator[0]:
            return False
    return True


allStraightTrips = {k: [w for w, dist in walks[k] if checkEqual(w)] for k in walks}
uniqueStraightTrips = {k: {tuple(w) for w in allStraightTrips[k]} for k in allStraightTrips}
