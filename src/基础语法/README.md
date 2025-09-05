Python 的基础数据类型主要包括以下几类：

1. **数值类型**：

   - int（整数）：如 1, 100, -10
   - float（浮点数）：如 3.14, -0.001
   - complex（复数）：如 3+4j

2. **字符串类型(str)**：

   - 用单引号或双引号包围的文本
   - 支持多行字符串（三引号）

3. **布尔类型(bool)**：

   - True（真）
   - False（假）

4. **空值类型(None)**：

   - 表示空值或无意义的值

5. **列表类型(list)**：

   - 可变序列
   - 用方括号 [] 表示
   - 可以存储不同类型的元素

6. **元组类型(tuple)**：

   - 不可变序列
   - 用圆括号 () 表示 (‘Chrome’, ‘Firefox’, ‘Safari’)
   - 创建后不能修改
   - 读取: 元组名[索引]

7. **集合类型(set)**：

   - 无序不重复集合
   - 用花括号 {} 表示 {'Chrome', 'Firefox', 'Safari'}
   - 主要用于去重和集合运算
   - 读取：遍历 or 转换为元组 or 转换为列表

8. **字典类型(dict)**：
   - 键值对映射
   - 用花括号 {} 表示
   - 通过键来访问值
   - 读取：字典名[键] or 字典名.get('键名')

# 属性读取

## 字典(dict)属性读取

```python
user = {"name": "张三", "age": 18}
# 通过键来访问
user['name']
# 通过get方法访问
user.get('name', 'default_name')

```

## 对象(object)属性读取
```python
class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

u = User("张三", 18)
# 通过 obj.attribute直接访问
u.name
# 通过getattr访问
getattr(u, 'name', 'default_name')

```
