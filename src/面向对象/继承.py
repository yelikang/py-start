

class Parent:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def say_hello(self):
        print(f"Hello, my name is {self.name} and I am {self.age} years old.")


# 子类继承父类
class Child(Parent):

    def __init__(self, name, age, gender):
        # 调用父类的构造函数
        super().__init__(name, age)
        # 私有属性（以双下划线开头）
        self.__gender = gender

    def say_hello(self):
        print(f"Hello, my name is {self.name} and I am {self.age} years old and I am a {self.__gender}.")
        self.__private_method('key')

    # 私有方法（以双下划线开头） (self理解为js的this对象，后面的属性才是实际的传参)
    def __private_method(self, key):
        print("This is a private method.", self.name, key)

    # 静态方法
    @staticmethod
    def staticShow():
        print('我是静态方法')

child = Child("Alice", 10, "girl")
child.say_hello()

Child.staticShow()

# 外部不能调用私有方法
# child.__private_method('key')