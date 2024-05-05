import timeit
import random
import matplotlib.pyplot as plt

# Сортування злиттям
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

# Сортування вставками
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

# Генерування випадкового масиву даних
arr = [random.randint(0, 1000) for _ in range(1000)]

# Вимірювання часу сортування злиттям
merge_sort_time = timeit.timeit(lambda: merge_sort(arr.copy()), number=10)
print("Merge Sort time:", merge_sort_time)

# Вимірювання часу сортування вставками
insertion_sort_time = timeit.timeit(lambda: insertion_sort(arr.copy()), number=10)
print("Insertion Sort time:", insertion_sort_time)

# Вимірювання часу сортування Timsort (вбудований в Python)
timsort_time = timeit.timeit(lambda: sorted(arr.copy()), number=10)
print("Timsort time:", timsort_time)

# Побудова графіку
labels = ['Merge Sort', 'Insertion Sort', 'Timsort']
times = [merge_sort_time, insertion_sort_time, timsort_time]

plt.figure(figsize=(10, 6))
plt.bar(labels, times, color=['blue', 'green', 'red'])
plt.yscale('log')  # встановлення логарифмічної шкали на осі y
plt.ylabel('Час виконання (секунди)')
plt.title('Порівняння швидкодії методів сортування')
plt.show()
