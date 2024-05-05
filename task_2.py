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

def merge_k_lists(lists):
    if len(lists) == 1:
        return lists[0]
    
    new_lists = []
    for i in range(1, len(lists), 2):
        new_lists.append(merge(lists[i-1], lists[i]))

    if (len(lists) % 2 != 0):
        new_lists.append(lists[len(lists)-1])

    return merge_k_lists(new_lists)

# Приклад використання
lists = [[1, 4, 5], [1, 3, 4], [2, 6]]
merged_list = merge_k_lists(lists)
print("Відсортований список:", merged_list)
