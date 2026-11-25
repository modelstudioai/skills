# 基于LlamaIndex构建RAG应用

在LlamaIndex中使用阿里云百炼提供的检索增强服务。

<a id="开始"></a>

<a id="c5bad0170eh01"></a>

## 开始

<a id="前提条件"></a>

<a id="6dbd9a309bzyv"></a>

### 前提条件

-   您需要已[获取与配置 API Key](../../model-api-reference/preparations/get-api-key.md)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
-   已在[百炼控制台](https://bailian.console.aliyun.com/rag/knowledge)开通知识库服务。首次进入知识库页面时，按照页面提示开通即可。
-   如果需要指定业务空间，还要获取指定业务空间的“业务空间ID”。
-   在Python编程工具的终端中执行以下命令安装DashScopeCloudIndex的安装包（您的Python版本要求：>=3.9 且 <=3.12）。

<a id="code-block"></a>

```python
pip install llama-index-core
pip install llama-index-llms-dashscope
pip install llama-index-indices-managed-dashscope
```

<a id="文件解析"></a>

<a id="ec23f0f77d2cx"></a>

### 文件解析

准备您的知识库文件：

-   可以是一个或多个独立的文件。
-   可以将所有文件放在一个文件夹中。

下面的例子将使用阿里云百炼的[智能化解析和切分文档](../../application-api-reference/frameworks/llamaindex/dashscopeparse.md)作为文档解析器。

> DashScopeParse 解析器支持在线解析 .doc、.docx、.pdf 文件，要求单个文件的大小在100M以内， 并且文件页数在1000以内。

<a id="code-block-2"></a>

```python
import os

from llama_index.readers.dashscope.base import DashScopeParse
from llama_index.readers.dashscope.utils import ResultType

# 设置业务空间 ID 将决定文档解析结果在“创建知识库”步骤中上传到哪个业务空间
os.environ['DASHSCOPE_WORKSPACE_ID'] = "<您的业务空间ID，使用默认业务空间时留空>"

# 第一种方式：使用文档解析器解析一个或多个文件
file = [
    # 需要解析的文件，支持pdf,doc,docx，请替换为您的文件路径
    "path/to/your_file.pdf",
]
# 解析文件
parse = DashScopeParse(result_type=ResultType.DASHSCOPE_DOCMIND)
documents = parse.load_data(file_path=file)

# 第二种方式：使用文档解析器解析一个文件夹内指定类型的文件
from llama_index.core import SimpleDirectoryReader
parse = DashScopeParse(result_type=ResultType.DASHSCOPE_DOCMIND)
# 定义不同文档类型的解析器
file_extractor = {".pdf": parse, '.doc': parse, '.docx': parse}
# 读取文件夹，提取和解析文件信息
documents = SimpleDirectoryReader(
    "your_folder", file_extractor=file_extractor
).load_data(num_workers=1)
```

上传成功后，您可以访问**[数据连接器](https://bailian.console.aliyun.com/cn-beijing/rag/connector/list)**页面，点击指定连接器卡片上的**查看详情**，查看上传的文档。

<a id="创建知识库"></a>

<a id="b710412982hu4"></a>

### 创建知识库

使用得到的documents创建知识库。

<a id="code-block-3"></a>

```python
from llama_index.indices.managed.dashscope import DashScopeCloudIndex

# create a new index
index = DashScopeCloudIndex.from_documents(
    documents,
    "my_first_index",
    verbose=True,
)
```

创建成功后，您可以在**[知识库](https://bailian.console.aliyun.com/rag/knowledge)**页面查看已创建的知识库。

<a id="读取知识库"></a>

<a id="231a9f60a7ovu"></a>

### 读取知识库

通过以下代码，您可以在LlamaIndex中初始化已创建的知识库。

<a id="code-block-4"></a>

```python
index = DashScopeCloudIndex("my_first_index")
```

<a id="获得retriever"></a>

<a id="66178c0084vvl"></a>

### 获得retriever

您可以从index对象中快速获得您的retriever，或者使用知识库名称初始化您的DashScopeCloudRetriever。

<a id="code-block-5"></a>

```python
# convert from index
retriever = index.as_retriever()

# initialize from DashScopeCloudRetriever
from llama_index.indices.managed.dashscope.retriever import DashScopeCloudRetriever
retriever = DashScopeCloudRetriever("my_first_index")

nodes = retriever.retrieve("my query")
```

<a id="获得query-engine"></a>

<a id="d3359300fa7dx"></a>

### 获得query engine

<a id="code-block-6"></a>

```python
import os

from llama_index.llms.dashscope import DashScope, DashScopeGenerationModels

dashscope_llm = DashScope(
  model_name=DashScopeGenerationModels.QWEN_MAX, api_key=os.environ["DASHSCOPE_API_KEY"]
)

query_engine = index.as_query_engine(llm=dashscope_llm)
```

<a id="向知识库新增-删除文档"></a>

<a id="8ed39ec846enl"></a>

### 向知识库新增/删除文档

<a id="code-block-7"></a>

```python
# add documents to index
index._insert(documents)
# delete documents from index
doc_id = "your_doc_id"  # 替换为待删除文档的ID
index.delete_ref_doc([doc_id])
```
