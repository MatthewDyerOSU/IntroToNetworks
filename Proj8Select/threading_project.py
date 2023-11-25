import sys
import threading

def add_range(name, some_range, result, i):
    iterable_range = range(some_range[0], some_range[1]+1)
    print(f'Running: {name}')
    result[i] = sum(iterable_range)

def main():
    # ranges = sys.argv[1]
    ranges = [
    [10, 20],
    [1, 5],
    [70, 80],
    [27, 92],
    [0, 16]
]
    n = len(ranges)
    result = [0] * n
    threads = []

    for i in range(n):
        name = f"Thread{i}"

        t = threading.Thread(target=add_range, args=(name, ranges[i], result, i))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
    print(result)
    total = sum(result)
    print(total)

if __name__ == "__main__":
    main()