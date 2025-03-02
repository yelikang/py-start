
class User:
    # 静态属性
    Worker = "工人"
    # 构造函数
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def say_hello(self):
        print(f"Hello, my name is {self.name} and I am {self.age} years old.")

user = User("Alice", 30)
user.say_hello()

print(User.Worker)
