import random

options = ('N', 'E', 'S', 'W')


def generate_walk(blocks=1):
    if blocks < 0:
        raise ValueError("Blocks must be larger than 0")

    for _ in range(blocks):
        yield random.choice(options)


def decode_walk(walk):
    dx, dy = 0, 0

    for w in walk:
        if w == 'N':
            dy += 1
        elif w == 'E':
            dx += 1
        elif w == 'S':
            dy -= 1
        elif w == 'W':
            dx -= 1
        else:
            raise ValueError("Walk contains an invalid direction")

    return dx, dy


def distance_manhattan(start, end):
    result = 0
    for s, e in zip(start, end):
        result += abs(s - e)
    return result


def do_walk(blocks, dist=distance_manhattan, gen_walk=True):
    walk = list(generate_walk(blocks))
    start = (0, 0)
    distance = decode_walk(walk)
    end = (start[0] + distance[0], start[1] + distance[1])
    if gen_walk:
        return walk, dist(start, end)
    else:
        return None, dist(start, end)


def monte_carlo_walk_analysis(max_blocks, repetitions=10000):
    result = dict()

    for blocks in range(1, max_blocks + 1):
        result[blocks] = []

        for _ in range(repetitions):
            walk = do_walk(blocks)
            result[blocks].append(walk)

    return result


def monte_carlo_walk(max_blocks, repetitions=100000):
    result = dict()

    for blocks in range(1, max_blocks + 1):
        result[blocks] = []

        for _ in range(repetitions):
            walk = do_walk(blocks, distance_manhattan, False)
            result[blocks].append(walk)

    return result
