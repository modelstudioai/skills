# DashScopeCloudRetriever

DashScopeCloudRetriever是百炼提供的检索增强服务管理SDK。使用该工具可以便捷地通过LlamaIndex框架初始化LlamaIndex检索器。

## 开始

### 前提条件

首先，登录[https://bailian.console.aliyun.com/](https://bailian.console.aliyun.com/)，获取你的API-KEY，当需要指定业务空间时也要获取指定“业务空间id”。

-   已创建API-KEY: [获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)。
-   已创建业务空间：[业务空间管理](https://help.aliyun.com/zh/model-studio/use-workspace)。

然后，安装DashScopeCloudIndex的安装包（python>=3.9,<=3.12）

```
pip install llama-index-core
pip install llama-index-indices-managed-dashscope
```
```
import os
from llama_index.indices.managed.dashscope.retriever import DashScopeCloudRetriever

os.environ["DASHSCOPE_API_KEY"] = "your_api_key_here"
os.environ["DASHSCOPE_WORKSPACE_ID"] = "your_workspace_here"

retriever = DashScopeCloudRetriever("your index name")
nodes = retriever.retrieve("test query")
print(nodes)
```

## 参数说明

### 输入参数

参数

类型

默认值

说明

index\_name

str

None

index\_name名

dense\_similarity\_top\_k

int

100

向量检索召回数量

sparse\_similarity\_top\_k

int

100

文本检索召回数量

enable\_reranking

bool

True

是否使用排序模型重排序

rerank\_model\_name

str

gte-rerank-hybrid

排序模型名称，支持的模型列表：

-   gte-rerank-hybrid
    
-   gte-rerank
    

rerank\_min\_score

float

0.0

retriever node分数过滤阈值。retriever仅返回高于rerank\_min\_score的node（该参数仅在enable\_reranking=True时生效）

rerank\_top\_n

int

5

retriever返回的节点数量,如果指定的top\_n值大于输入的候选节点数量，返回全部节点

workspace\_id

str

None

DashScope worksparce id，可以通过环境变量等方法设置

api\_key

str

None

DashScope api key，可以通过环境变量等方法设置
