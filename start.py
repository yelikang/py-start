# 输出hello world
print("hello world")

# 写一个排序算法
def sort(arr):
    for i in range(len(arr)):
        for j in range(len(arr) - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


arr = [1, 3, 2, 5, 4]
result = sort(arr)
print(result)