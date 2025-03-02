class User:

    def __init__(self, name, age):
        self.name = name
        self.age = age
    # 定义get方法
    def get_age(self):
        return self.age + 1
    # 定义set方法
    def set_age(self, age):
        self.age = age

user = User("Alice", 30)
print(user.get_age())
user.set_age(31)
print(user.get_age())
