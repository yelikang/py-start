
# 1.数值类型
# 数值类型
age = 20
# 浮点数
price = 10.5


# 2.字符串类型
name = 'Coder'
multi_line = '''
    我是一个多行字符串
    我是一个多行字符串
    我是一个多行字符串
'''



# 3. 布尔类型
isStudent = False
isWorker = True

if isStudent:
    print('我是学生')
else:
    print('我不是一个学生')


# 4. 空值类型
empty_value = None
print(empty_value)

# 5. 列表类型 - 可变序列
numbers = [1, 2, 3, 4, 5]


# 6. 元组类型（内容不可修改） - 不可变序列
rgb = (255, 0, 0)

# 7. 集合类型
unique_numbers = {11, 2, 3, 4, 5, 2}
# 添加元素
unique_numbers.add(6)
# 删除元素（是删除元素，不是删除索引位置的元素）
unique_numbers.remove(11)
# 清空集合
# unique_numbers.clear()
print(unique_numbers)


# 8. 字典类型 - 键值对
user = {
    name:'coder',
    age: 12
}
print(user)