import yaml
from loguru import logger
from kink import di

def init_config(file_path: str)-> None:
    with open(file_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
        print(config)
        # 注入config配置
        di['config'] = config
        logger.info('配置文件加载完成')

def get_config( key: str):
    config = di['config']
    return config[key]

if __name__ == '__main__':
    # open方法查找文件是相对python执行的目录开始的，根目录下执行会找不到
    # init_config('test.yaml')
    # 绝对路径
    # init_config('src/配置文件读取/test.yaml')
    # 计算绝对路径
    import os
    current_abs = os.path.dirname(os.path.abspath(__file__))
    file_path = current_abs + '/test.yaml'
    init_config(file_path)

    get_config('Databases')