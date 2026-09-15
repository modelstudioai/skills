# DashScopeJsonNodeParser

DashScopeJsonNodeParser提供阿里巴巴通义实验室开发的文本切分模型，开发者可以通过LlamaIndex框架对DashScopeParse的解析结果进行文档切分。

## 开始

### 前提条件

首先，登录[https://bailian.console.aliyun.com/](https://bailian.console.aliyun.com/)，获取你的API-KEY，当需要指定业务空间时也要获取指定“业务空间id”。

-   已创建API-KEY: [获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)。
-   已创建业务空间：[业务空间管理](https://help.aliyun.com/zh/model-studio/use-workspace)。

然后，安装DashScopeJsonNodeParser的安装包（python>=3.9,<=3.12）

```
pip install llama-index-core
pip install llama-index-node-parser-dashscope
```

### 示例代码

```
import json
import os
from llama_index.node_parser.dashscope import (
    DashScopeJsonNodeParser,
)
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.schema import Document

# Set your Dashscope API key in the environment
os.environ["DASHSCOPE_API_KEY"] = "your_api_key_here"

documents = [
    # Prepare your documents obtained from the Dashscope reader
]

# Initialize the DashScope JsonNodeParser
node_parser = DashScopeJsonNodeParser(
    chunk_size=100, overlap_size=0, separator=" |,|，|。|？|！|\n|\?|\!"
)

# Set up the ingestion pipeline with the node parser
pipeline = IngestionPipeline(transformations=[node_parser])

# Process the documents and print the resulting nodes
nodes = pipeline.run(documents=documents, show_progress=True)
for node in nodes:
    print(node)
```
**Note：**

-   DashScopeJsonNodeParser主要用于配合DashScopeParse使用

### 参数说明

参数值

默认值

说明

try\_count\_limit

10

最大重试尝试次数

chunk\_size

500

每次处理的块大小

overlap\_size

100

连续块之间的重叠大小

separator

" |,|，|。|？|！|\\n|\\?|\\!"

用于分割文本的分隔符字符

language

cn

词法分析器的语言，接受"cn"（中文），"en"（英文），"any"（任意）。注意，任意模式将会比较慢
