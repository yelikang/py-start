# 全量导入add模块
import add
print(add.addFn(1, 2))

# 部分导入
from add import addFn
print(addFn(1, 2))

# 别名导入
from add import addFn as addMethod
print(addMethod(1, 2))
