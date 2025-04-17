# 从flask包中导入Flask类
from flask import Flask
from app_factory import create_app

print(__name__)

# 创建Flask应用实例，__name__表示当前模块名
app = create_app()


# 定义路由，当访问根路径'/'时，执行index函数
@app.route("/")
def index():
    # 返回字符串作为响应内容
    return "Hello, World22!"


# 判断是否是直接运行该脚本; 只有当前程序自身运行，__name__的值是'__main__'
# 每个模块都有一个 __name__ 属性，当其值是 '__main__' 时，表明该模块自身在运行，否则是被引入。
if __name__ == "__main__":
    # 启动Flask开发服务器，开启调试模式
    app.run(debug=True)

#  需要再根目录通过命令行运行 (flask在根目录安装的)
#  py -m demo.本地服务.app


#  __name__是Python的内置变量
# 它表示当前模块的名称
# 如果直接运行该脚本，__name__的值是'__main__'
# 如果作为模块导入，__name__的值是模块名（即文件名）
