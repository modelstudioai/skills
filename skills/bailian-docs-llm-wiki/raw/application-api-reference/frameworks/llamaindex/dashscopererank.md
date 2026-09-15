# DashScopeRerank

DashScopeRerank提供阿里巴巴通义实验室开发的GTE-Rerank文本排序系列模型，开发者可以通过LlamaIndex框架进行集成高质量文本检索、排序。

## 开始

### 前提条件

-   已开通阿里云百炼服务：[产品开通](https://help.aliyun.com/zh/model-studio/activate-alibaba-cloud-model-studio)。
-   创建API\_KEY: [获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)。
-   安装DashScopeRerank的安装包 (python>=3.9,<=3.12）

```
pip install llama-index-core
pip install llama-index-postprocessor-dashscope-rerank
```

### 示例代码

设置API-KEY

```
export DASHSCOPE_API_KEY=YOUR_DASHSCOPE_API_KEY
```
```
from llama_index.core.data_structs import Node
from llama_index.core.schema import NodeWithScore
from llama_index.postprocessor.dashscope_rerank import DashScopeRerank

nodes = [
    NodeWithScore(node=Node(text="text1"), score=0.7),
    NodeWithScore(node=Node(text="text2"), score=0.8),
]

dashscope_rerank = DashScopeRerank(top_n=5)
results = dashscope_rerank.postprocess_nodes(nodes, query_str="<user query>")
for res in results:
    print("Text: ", res.node.get_content(), "Score: ", res.score)
```
**示例代码输出**
```
Text:  text1 Score:  0.25589250620997755
Text:  text2 Score:  0.18071043165292258
```

## 参数说明

### 输入参数

-   DashScopeRerank参数说明如下

参数

类型

默认值

说明

model

string

gte-rerank

支持的模型列表：

-   gte-rerank
    

top\_n

int

3

排序返回的top文档数量, 如果没有指定则返回全部候选doc，如果指定的top\_n值大于输入的候选doc数量，返回全部doc

return\_documents

bool

False

返回的排序结果列表里面是否返回每一条document原文，默认值False

api\_key

str

None

DashScope api key，可以通过环境变量等方法设置
