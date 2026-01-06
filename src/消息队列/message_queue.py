from loguru import logger
import asyncio

class Message_Queue:
    def __init__(self) -> None:
        self._queue = []

    def addMessage(self, msg):
        self._queue.append(msg)

    async def aiter(self):
        while len(self._queue) > 0:
            try:
                msg = self._queue.pop(0)
                yield msg
            except Exception as e:
                logger.error("消息队列获取消息失败：{}", e)

async def test():
    queue = Message_Queue()
    queue.addMessage("123")
    queue.addMessage("456")
    async for msg in queue.aiter():
        print(msg)
        await asyncio.sleep(1)
    queue.addMessage("789")
    print("done")

async def main():
    # 使用create_task创建任务
    task = asyncio.create_task(test())
    print("任务已创建，开始执行...")
    
    # 等待任务完成
    await task
    print("任务执行完毕")

if __name__ == '__main__':
    asyncio.run(main())