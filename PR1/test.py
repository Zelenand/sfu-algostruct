import dynamic_array
import array


arr1 = dynamic_array.Array('d', [1, 2, 3])
arr2 = dynamic_array.Array('i', [])
arr3 = array.array("i", [1,2,3])
print(arr1 == arr2)
arr1.insert(-1000, 8)
arr1.insert(1000, 4)
arr1.insert(1, 3)
arr1.insert(1, 4)
arr1.append(9.9)
res = arr1.remove(4)
print(res)
print(arr1)
# print(arr1.pop())
# print(arr1.pop())
# print(arr1.pop())
# print(arr1.pop())
# print(arr1.pop())
# print(arr1)