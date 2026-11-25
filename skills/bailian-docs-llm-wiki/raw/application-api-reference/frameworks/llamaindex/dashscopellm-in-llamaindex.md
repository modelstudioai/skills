# 使用百炼大模型

本文介绍如何基于LlamaIndex框架，调用百炼平台提供的大模型。

<a id="前提条件"></a>

<a id="a78a19d952plg"></a>

## 前提条件

-   您已开通百炼服务并获得API-KEY， 请参考[获取与配置 API Key](../../../model-api-reference/preparations/get-api-key.md)。
-   已导入 API-KEY，请参考[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

<a id="openailike-方式调用"></a>

<a id="f7f8039703ke7"></a>

## OPENAILIKE 方式调用

LlamIndex 的 OpenAI-like 封装可以用于调用百炼支持 [文本生成](../../../model-api-reference/qwen-api-reference.md)的大模型。完整列表请参考：[OpenAI 兼容模式支持的模型列表](../../../model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md#eadfc13038jd5)。调用费用、输入输出上限等请参考：[选择模型](../../../model-user-guide/get-started-with-models/models.md)。

使用前需要安装 LlamaIndex 核心组件和 OpenAI Like：

<a id="code-block"></a>

```bash
pip install llama-index-core
pip install llama-index-llms-openai-like
```

<a id="修改全局设置-可选"></a>

<a id="b5631e462csyy"></a>

### 修改全局设置（可选）

<a id="code-block-2"></a>

```python
import os
from llama_index.core import Settings
from llama_index.llms.openai_like import OpenAILike

# LlamaIndex默认使用的大模型被替换为百炼
Settings.llm = OpenAILike(
    model="qwen-plus",
    api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    is_chat_model=True
)
```

<a id="大模型调用示例"></a>

<a id="323e80e83f4x3"></a>

### 大模型调用示例

<a id="code-block-3"></a>

```python
import os
from llama_index.llms.openai_like import OpenAILike

# 所调用的模型
llm = OpenAILike(
    model="qwen-plus",
    api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    is_chat_model=True
)

response = llm.complete("帮我推荐一下江浙沪5天的旅游攻略。")
print(response)
```

详细介绍以及完整的 API Reference 请前往 LlamaIndex 官方的 [OpenAILike API Reference](https://docs.llamaindex.ai/en/stable/api_reference/llms/openai_like/)。

<a id="dashscope-方式调用"></a>

<a id="1cb6f7fcb2ahm"></a>

## DashScope 方式调用

支持百炼所有的文本生成模型，完整列表与调用费用请参考：[选择模型](../../../model-user-guide/get-started-with-models/models.md)。（也支持[部署](../../../model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-introduction.md)后的模型）

使用前需要安装 LlamaIndex 核心组件和 DashScopeLLM：

<a id="code-block-4"></a>

```bash
pip install llama-index-core
pip install llama-index-llms-dashscope
```

<a id="修改全局设置-可选-2"></a>

<a id="80f68552e3f46"></a>

### 修改全局设置（可选）

<a id="code-block-5"></a>

```python
import os
from llama_index.core import Settings
from llama_index.llms.dashscope import DashScope

# LlamaIndex默认使用的大模型被替换为百炼
Settings.llm = DashScope(model_name="qwen-plus", api_key=os.getenv("DASHSCOPE_API_KEY"))
```

<a id="大模型调用示例-2"></a>

<a id="cbb52ff8f5iat"></a>

### 大模型调用示例

<a id="code-block-6"></a>

```python
import os
from llama_index.llms.dashscope import DashScope

llm = DashScope(model_name="qwen-plus", api_key=os.getenv("DASHSCOPE_API_KEY"))
response = llm.complete("帮我推荐一下江浙沪5天的旅游攻略。")
print(response)
```

详细介绍与更多示例请前往 LlamaIndex 官方的 [DashScope LLM Examples](https://docs.llamaindex.ai/en/stable/examples/llm/dashscope/)，完整的 API Reference 请前往 LlamaIndex 官方的 [DashScope API Reference](https://docs.llamaindex.ai/en/stable/api_reference/llms/dashscope/)。
