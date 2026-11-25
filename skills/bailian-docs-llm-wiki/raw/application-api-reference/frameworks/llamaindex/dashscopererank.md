# DashScopeRerank

DashScopeRerank提供阿里巴巴通义实验室开发的GTE-Rerank文本排序系列模型，开发者可以通过LlamaIndex框架进行集成高质量文本检索、排序。

<a id="开始"></a>

<a id="c5bad0170eh01"></a>

## 开始

<a id="前提条件"></a>

<a id="6dbd9a309bzyv"></a>

### 前提条件

-   已开通阿里云百炼服务：[产品开通](https://help.aliyun.com/zh/model-studio/activate-alibaba-cloud-model-studio)。
-   创建API\_KEY: [获取与配置 API Key](../../../model-api-reference/preparations/get-api-key.md)。
-   安装DashScopeRerank的安装包 (python>=3.9,<=3.12）

<a id="code-block"></a>

```python
pip install llama-index-core
pip install llama-index-postprocessor-dashscope-rerank
```

<a id="示例代码"></a>

<a id="ec23f0f77d2cx"></a>

### 示例代码

设置API-KEY

<a id="code-block-2"></a>

```bash
export DASHSCOPE_API_KEY=YOUR_DASHSCOPE_API_KEY
```

<a id="code-block-3"></a>

```python
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

<a id="code-block-4"></a>

```text
Text:  text1 Score:  0.25589250620997755
Text:  text2 Score:  0.18071043165292258
```

<a id="参数说明"></a>

<a id="726f54c1469yc"></a>

## 参数说明

<a id="输入参数"></a>

<a id="19986db12esqn"></a>

### 输入参数

-   DashScopeRerank参数说明如下

<table><thead><tr><th><p>参数</p></th><th><p>类型</p></th><th><p>默认值</p></th><th><p>说明</p></th></tr></thead><tbody><tr><td><p>model</p></td><td><p>string</p></td><td><p>gte-rerank</p></td><td><p>支持的模型列表：</p><ul><li><p>gte-rerank</p></li></ul></td></tr><tr><td><p>top_n</p></td><td><p>int</p></td><td><p>3</p></td><td><p>排序返回的top文档数量, 如果没有指定则返回全部候选doc，如果指定的top_n值大于输入的候选doc数量，返回全部doc</p></td></tr><tr><td><p>return_documents</p></td><td><p>bool</p></td><td><p>False</p></td><td><p>返回的排序结果列表里面是否返回每一条document原文，默认值False</p></td></tr><tr><td><p>api_key</p></td><td><p>str</p></td><td><p>None</p></td><td><p>DashScope api key，可以通过环境变量等方法设置</p></td></tr></tbody></table>
