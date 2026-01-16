from entity.domain.state import CompanyState
from langgraph.graph import StateGraph,END
from nodes.grounding import GroundingNode
from nodes.nodes_researcher.financical import FinancialNode
from nodes.nodes_researcher.Industry import IndustryNode
from nodes.collector import CollectorNode
from nodes.enricher import EnricherNode
from nodes.briefing import BriefingNode


class Graph:
    def __init__(self):
        self.nodes = {}
        self.workflow = None
        self._init_nodes()
        self._init_workflow()

    def _init_nodes(self):
        self.grounding = GroundingNode()
        self.financial = FinancialNode()
        self.industry = IndustryNode()
        self.industry = IndustryNode()
        self.collector = CollectorNode()
        self.enricher = EnricherNode()
        self.briefing = BriefingNode()

    def _init_workflow(self):
        self.workflow = StateGraph(CompanyState)

        self.workflow.add_node('grounding', self.grounding.run)
        self.workflow.add_node('financial', self.financial.run)
        self.workflow.add_node('industry', self.industry.run)
        self.workflow.add_node('collector', self.collector.run)
        self.workflow.add_node('enricher', self.enricher.run)
        self.workflow.add_node('briefing', self.briefing.run)

        self.workflow.set_entry_point('grounding')

        self.workflow.add_edge('grounding', 'financial')
        self.workflow.add_edge('grounding', 'industry')

        self.workflow.add_edge('financial', 'collector')
        self.workflow.add_edge('industry', 'collector')
        
        self.workflow.add_edge('collector', 'enricher')
        self.workflow.add_edge('enricher', 'briefing')
        self.workflow.add_edge('briefing', END)

    async def astream(self, input_state: CompanyState):
        '''
        异步执行工作流，返回状态流
        '''
        compiled_graph = self.workflow.compile()
        # 异步编译工作流
        async for state in compiled_graph.astream(input_state):
            # print(state)
            yield state

    def invoke(self, input_state: CompanyState):
        '''
        同步执行工作流，返回最终状态
        '''
        compiled_graph = self.workflow.compile()
        return compiled_graph

        
