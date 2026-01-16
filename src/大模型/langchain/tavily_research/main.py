from graph import Graph
from entity.domain.state import CompanyState
from loguru import logger

# lanchain 结合 tavily 进行搜索
class SearchWorkflow:
    def __init__(self):
        pass
    async def async_run(self):
        state = CompanyState(
            company_name='零食很忙',
            company_url='https://www.hnlshm.com/',
            industry='零售行业'
        )

        graph = Graph()
        async for state in graph.astream(state):
            node_name = list(state.keys())[0] if state else 'unknown'
            node_state = state[node_name]
            # yield state
            logger.debug(f"Node completed: {node_name}")
            if node_state.get('briefings'):
                logger.info('简报生成完毕:\n')
                logger.info(node_state['briefings'])
                break


    async def run(self):
        state = CompanyState(
            company_name='百度',
        )

        graph = Graph()
        compiled_graph =  graph.invoke(state)
        async for state in compiled_graph.astream(state):
            yield state

if __name__ == '__main__':
    import asyncio
    asyncio.run(SearchWorkflow().async_run())
