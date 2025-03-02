# -*- coding: utf-8 -*-

# 1. 默认包
import sys
# 输出当前py的版本
print('当前python版本',sys.version)

# 2. 第三方包
# 使用 pip 安装依赖： pip install numpy
import numpy as np

# 创建一个包含100个随机数的数组，范围在0到100之间
data = np.random.randint(0,100, 100)
print('随机数',data)

# 3. 导包方式
# 导入部分内容
# from flask import Flask  从flask中导入Flask类
# import flask  导入全部flask包

