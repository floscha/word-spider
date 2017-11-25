import json
import sys

if __name__ == '__main__':
    fpath = sys.argv[1]
    sort_key = sys.argv[2]

    with open(fpath, 'r') as f:
        data = json.load(f)

    sorted_data = sorted(data, key=lambda x: x[sort_key])

    with open(fpath, 'w') as f:
        json.dump(sorted_data, f, indent=2)
