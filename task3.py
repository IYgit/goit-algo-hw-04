import timeit
import random
import matplotlib.pyplot as plt


# ── Merge Sort ─────────────────────────────────────────────────────────────────

def merge_sort(arr: list) -> list:
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)


def merge(left: list, right: list) -> list:
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


# ── Insertion Sort ─────────────────────────────────────────────────────────────

def insertion_sort(arr: list) -> list:
    arr = arr[:]
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


# ── Benchmark ──────────────────────────────────────────────────────────────────

SIZES = [100, 500, 1_000, 5_000, 10_000, 50_000]
REPEATS = 5  # timeit repetitions per measurement


def benchmark(data: list) -> tuple[float, float, float]:
    """Returns (merge_sort_time, insertion_sort_time, timsort_time) in seconds."""
    t_merge = timeit.timeit(lambda: merge_sort(data), number=REPEATS) / REPEATS
    t_insert = timeit.timeit(lambda: insertion_sort(data), number=REPEATS) / REPEATS
    t_tim = timeit.timeit(lambda: sorted(data), number=REPEATS) / REPEATS
    return t_merge, t_insert, t_tim


def run_benchmarks() -> dict:
    results = {"size": [], "merge": [], "insertion": [], "timsort": []}

    for size in SIZES:
        data = [random.randint(0, 10_000) for _ in range(size)]
        print(f"  Benchmarking n={size:>6} ...", end=" ", flush=True)
        t_merge, t_insert, t_tim = benchmark(data)
        print(f"merge={t_merge:.6f}s  insertion={t_insert:.6f}s  timsort={t_tim:.6f}s")

        results["size"].append(size)
        results["merge"].append(t_merge)
        results["insertion"].append(t_insert)
        results["timsort"].append(t_tim)

    return results


# ── Output ─────────────────────────────────────────────────────────────────────

def print_table(results: dict) -> None:
    col_w = [12, 18, 20, 14]
    headers = ["Array size", "Merge sort (s)", "Insertion sort (s)", "Timsort (s)"]
    sep = "+-" + "-+-".join("-" * w for w in col_w) + "-+"
    row_fmt = "| " + " | ".join(f"{{:<{w}}}" for w in col_w) + " |"

    print("\n" + sep)
    print(row_fmt.format(*headers))
    print(sep)
    for size, m, ins, tim in zip(
        results["size"], results["merge"], results["insertion"], results["timsort"]
    ):
        print(row_fmt.format(size, f"{m:.6f}", f"{ins:.6f}", f"{tim:.6f}"))
    print(sep)


def plot_results(results: dict) -> None:
    sizes = results["size"]

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # ── All sizes ──
    ax = axes[0]
    ax.plot(sizes, results["merge"], marker="o", label="Merge sort", color="steelblue")
    ax.plot(sizes, results["insertion"], marker="s", label="Insertion sort", color="tomato")
    ax.plot(sizes, results["timsort"], marker="^", label="Timsort (built-in)", color="seagreen")
    ax.set_title("Sorting algorithms: all sizes")
    ax.set_xlabel("Array size")
    ax.set_ylabel("Time (seconds)")
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.6)

    # ── Zoom: merge vs timsort (skip insertion for large n) ──
    ax2 = axes[1]
    ax2.plot(sizes, results["merge"], marker="o", label="Merge sort", color="steelblue")
    ax2.plot(sizes, results["timsort"], marker="^", label="Timsort (built-in)", color="seagreen")
    ax2.set_title("Merge sort vs Timsort")
    ax2.set_xlabel("Array size")
    ax2.set_ylabel("Time (seconds)")
    ax2.legend()
    ax2.grid(True, linestyle="--", alpha=0.6)

    plt.suptitle("Sorting Algorithm Benchmark", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.show()


def print_conclusions(results: dict) -> None:
    print("\n" + "=" * 60)
    print("ВИСНОВКИ")
    print("=" * 60)

    max_size = results["size"][-1]
    idx = -1
    m = results["merge"][idx]
    ins = results["insertion"][idx]
    tim = results["timsort"][idx]

    print(f"""
Тестування проводилось на масивах розміром від {results['size'][0]}
до {max_size} елементів (випадкові цілі числа).

Результати для n={max_size}:
  • Сортування злиттям:   {m:.6f} с
  • Сортування вставками: {ins:.6f} с
  • Timsort (sorted):     {tim:.6f} с

  Timsort швидший за злиття   у {m / tim:.1f}x разів
  Timsort швидший за вставки  у {ins / tim:.1f}x разів

Теоретична складність:
  • Сортування вставками: O(n²)  — погано масштабується
  • Сортування злиттям:   O(n log n) — добре, але є накладні витрати
    на рекурсію та виділення пам'яті
  • Timsort:              O(n log n) — реалізований на C, використовує
    сортування вставками для малих підмасивів (runs) і ефективно
    об'єднує вже впорядковані послідовності

Висновок:
  Timsort є значно ефективнішим на практиці завдяки:
  1. Реалізації на рівні інтерпретатора (C extension)  
  2. Адаптивності — використовує natural runs у даних
  3. Оптимізації для малих підмасивів через insertion sort
  Саме тому вбудовані sorted() / list.sort() є стандартом
  для сортування в Python.
""")


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    print("Sorting Algorithm Benchmark")
    print("-" * 60)
    results = run_benchmarks()
    print_table(results)
    print_conclusions(results)
    plot_results(results)


if __name__ == "__main__":
    main()

