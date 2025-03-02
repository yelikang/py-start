# 1. 遍历列表
list = [1, 2, 3, 4, 5]

for item in list:
    print(item)

# 带索引的遍历
for index, item in enumerate(list):
    print("带索引的遍历", index, item)


users = [
    {"name": "张三", "age": 18, "gender": "男"},
    {"name": "李四", "age": 20, "gender": "女"},
]

for user in users:
    print(user)

# 2. 遍历字典
user = {"name": "coder", "age": 18, "gender": "男"}
for key, value in user.items():
    # f类似于js的模板字符串
    # print(f"{key}: {value}")
    print(key, value)
