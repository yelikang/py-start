# 主体模块介绍
## langchain
> 简化LLM程序生命周期的各个阶段，简单理解就是能更快速的对接LLM

## langsmith
> 用于监控和调试Langchain应用的平台

## langserve
> 用于将Langchain应用部署为API服务的工具


# langchain
## 核心组件
### 模型(Models)
> 主要包含各大语言模型的Langchain接口和调用细节，以及输入解析机制

### 提示模板(Prompts)
> 使提示工程流线化，进一步激发大语言模型的潜力
```
提示词模板类型
- LLM提示模板 PromptTemplate：常用的String提示模板

- 聊天提示模板 ChatPromptTemplate: 常用的Chat提示模板，用于组合各种角色的消息模板，传入聊天模型。消息模板包括：ChatMessagePromptTemplate、HumanMessagePromptTemplate、AIMessagePromptTemplate、SystemMessagePromptTemplate等

- 样本提示模板 FewShotPromptTemplate： 通过实例来教模型如何回答

- 部分格式化提示模板：提示模板传入所需值的子集，以创建仅期望剩余值子集的新提示模板

- 管道提示模板 PipelinePrompt：用于把几个提示组合在一起使用

- 自定义模板：允许基于其它模板类来定制自己的提示模板
```


### 数据检索(Indexes) - RAG
> 构建并操作文档的方法，接受用户的查询并返回相关的文档，轻松搭建本地知识库（文档向量化+内容检索）

### 记忆(Memory)
> 通过短时记忆和长时记忆，在对话过程中存储和检索数据，让ChatBox记住你

### 代理(Agents)
> 通过”代理“，让大模型自主调用外部工具和内部工具，使智能Agent成为可能

## 开源库组成
### langchain-core
> 基础抽象和langchain表达式语言

### langchain-community
> 第三方集成、合作伙伴包

### langchain
> 构建应用程序认知架构的链、代理和检索策略

### langgraph ?
> 通过将步骤建模为图中的边和节点，使用LLM构建健壮且有状态的多参与者应用程序

### langserve ?
> 将langchain链部署为rest api

### lansmith
> 开着盘平台，可调试、测试、评估和监控LLM应用程序，并与langchain无缝集成

