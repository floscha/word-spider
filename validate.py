import json
import sys

if __name__ == '__main__':
    fpath = sys.argv[1]

    with open(fpath, 'r') as f:
        data = json.load(f)

    rank_set = set([d['rank'] for d in data])
    missing_set = rank_set ^ set(range(1, 1001))
    print("%d missing ranks:" % len(missing_set))
    print(missing_set)
