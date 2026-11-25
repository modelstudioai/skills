# DashScopeCloudRetriever

DashScopeCloudRetriever是百炼提供的检索增强服务管理SDK。使用该工具可以便捷地通过LlamaIndex框架初始化LlamaIndex检索器。

<a id="开始"></a>

<a id="c5bad0170eh01"></a>

## 开始

<a id="前提条件"></a>

<a id="6dbd9a309bzyv"></a>

### 前提条件

首先，登录[https://bailian.console.aliyun.com/](https://bailian.console.aliyun.com/)，获取你的API-KEY，当需要指定业务空间时也要获取指定“业务空间id”。

-   已创建API-KEY: [获取与配置 API Key](../../../model-api-reference/preparations/get-api-key.md)。
-   已创建业务空间：[业务空间管理](https://help.aliyun.com/zh/model-studio/use-workspace)。

然后，安装DashScopeCloudIndex的安装包（python>=3.9,<=3.12）

<a id="code-block"></a>

```python
pip install llama-index-core
pip install llama-index-indices-managed-dashscope
```

<a id="code-block-2"></a>

```python
import os
from llama_index.indices.managed.dashscope.retriever import DashScopeCloudRetriever

os.environ["DASHSCOPE_API_KEY"] = "your_api_key_here"
os.environ["DASHSCOPE_WORKSPACE_ID"] = "your_workspace_here"

retriever = DashScopeCloudRetriever("your index name")
nodes = retriever.retrieve("test query")
print(nodes)
```

<a id="参数说明"></a>

<a id="726f54c1469yc"></a>

## 参数说明

<a id="输入参数"></a>

<a id="19986db12esqn"></a>

### 输入参数

<table><thead><tr><th><p>参数</p></th><th><p>类型</p></th><th><p>默认值</p></th><th><p>说明</p></th></tr></thead><tbody><tr><td><p>index_name</p></td><td><p>str</p></td><td><p>None</p></td><td><p>index_name名</p></td></tr><tr><td><p>dense_similarity_top_k</p></td><td><p>int</p></td><td><p>100</p></td><td><p>向量检索召回数量</p></td></tr><tr><td><p>sparse_similarity_top_k</p></td><td><p>int</p></td><td><p>100</p></td><td><p>文本检索召回数量</p></td></tr><tr><td><p>enable_reranking</p></td><td><p>bool</p></td><td><p>True</p></td><td><p>是否使用排序模型重排序</p></td></tr><tr><td><p>rerank_model_name</p></td><td><p>str</p></td><td><p>gte-rerank-hybrid</p></td><td><p>排序模型名称，支持的模型列表：</p><ul><li><p>gte-rerank-hybrid</p></li><li><p>gte-rerank</p></li></ul></td></tr><tr><td><p>rerank_min_score</p></td><td><p>float</p></td><td><p>0.0</p></td><td><p>retriever node分数过滤阈值。retriever仅返回高于rerank_min_score的node（该参数仅在enable_reranking=True时生效）</p></td></tr><tr><td><p>rerank_top_n</p></td><td><p>int</p></td><td><p>5</p></td><td><p>retriever返回的节点数量,如果指定的top_n值大于输入的候选节点数量，返回全部节点</p></td></tr><tr><td><p>workspace_id</p></td><td><p>str</p></td><td><p>None</p></td><td><p>DashScope worksparce id，可以通过环境变量等方法设置</p></td></tr><tr><td><p>api_key</p></td><td><p>str</p></td><td><p>None</p></td><td><p>DashScope api key，可以通过环境变量等方法设置</p></td></tr></tbody></table>
