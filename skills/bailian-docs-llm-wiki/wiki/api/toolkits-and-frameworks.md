# toolkits and [frameworks](frameworks.md)

阿里云百炼提供多套 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)工具包与框架，覆盖文本生成、多模态理解、向量嵌入、批量处理、会话管理等核心场景。开发者可复用现有 OpenAI SDK 代码，仅需调整 `base_url`、`api_key` 和模型名称即可快速迁移。所有接口均支持标准 OpenAI REST API 协议与 SDK 调用方式，同时扩展了百炼专属能力（如内置工具、长上下文、业务空间专属域名等）。

## 支持的模型/功能

百炼兼容接口支持以下模型类型及对应功能：

- **文本生成**：`qwen3.8-max`、`qwen3.7-plus`、`qwen-coder-turbo-latest` 等全系列 Qwen 模型，支持 `chat/completions`、`completions`、`responses` 等多种调用模式；[OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md) 文档列出了全部支持的商业版、开源版及三方直供模型（如 DeepSeek、Kimi、GLM 等）。
- **多模态理解**：`qwen3-vl-plus`、`qwen3-omni-flash`、`qwen-vl-ocr` 等视觉模型，支持图像/视频/文档输入，兼容 OpenAI 的 `message.content` 多类型数组格式；详见 [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)。
- **向量嵌入**：`text-embedding-v4`、`qwen3.7-text-embedding` 等 Embedding 模型，支持多维度输出与多语种；注意 [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md) 明确指出不支持稀疏向量（`output_type=sparse`），该参数将被忽略。
- **批量处理**：`qwen3.8-max`、`qwen3.5-omni-plus` 等模型支持 Batch Chat（单请求同步等待）与 Batch File（JSONL 文件异步提交）两种模式，最高支持 256K 上下文 [Token](../concepts/token.md)；[OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md) 提供了完整的 JSONL 格式规范与测试模型 `batch-test-model`。
- **会话与上下文管理**：`Conversations API` 支持跨设备会话持久化，`Responses API` 支持通过 `previous_response_id` 自动注入历史上下文，无需手动拼接消息数组；二者协同可构建高鲁棒性智能体应用。

> **注意**：`Qwen-Audio` 明确不支持 OpenAI 兼容协议，仅支持 DashScope 原生协议；该限制在 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md) 中已强调，开发者需避免在 Audio 场景下误用兼容接口。

## 关键参数

所有兼容接口共用以下关键参数，行为与 OpenAI 官方一致，但部分参数有百炼特有约束：

- `base_url`：必须使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），旧域名（`dashscope.aliyuncs.com`）虽仍可用，但性能与稳定性较低；该要求在 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)、[OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md) 等多篇文档中反复强调。
- `model`：模型名称需严格匹配文档所列支持列表，例如 `qwen3.8-max` 可用于 `chat/completions` 和 `responses`，但 `qwen-coder-turbo-latest` 仅支持 `completions` 接口。
- `stream` 与 `stream_options`：流式响应支持 `{"include_usage": true}` 以在末尾 chunk 返回 token 统计；`completions` 接口也支持此参数，见 [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)。
- `enable_thinking`：仅适用于 `qwen3.5+` 系列模型的 Batch 场景，控制是否启用思考模式（影响 token 成本），必须作为 `body` 顶层参数传入，不可置于 `extra_body` 内；该规则在 [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md) 和 [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md) 中均被明确要求。
- `dimensions`：仅 `text-embedding-v3` 和 `text-embedding-v4` 支持，用于指定向量维度；`text-embedding-v1/v2` 不支持该参数。

## 使用方式

### 初始化客户端
```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),  # 强烈建议配置为环境变量
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"  # 替换为实际 WorkspaceId
)
```

### 接口调用示例
- **Chat Completions**（标准对话）：
  ```python
  client.chat.completions.create(model="qwen3.8-max", messages=[{"role":"user","content":"你好"}])
  ```
- **Responses API**（带内置工具的智能体）：
  ```python
  client.responses.create(model="qwen3.8-max", input="查一下今天北京天气")
  ```
- **Completions**（代码补全/FIM）：
  ```python
  client.completions.create(model="qwen-coder-turbo-latest", prompt="<tool_call>def quick_sort(arr):<tool_call>")
  ```
- **Embeddings**（文本向量化）：
  ```python
  client.embeddings.create(model="text-embedding-v4", input="hello world", dimensions=1024)
  ```
- **Batch Chat**（同步批量）：
  ```python
  client.chat.completions.create(
      model="qwen-plus",
      messages=[{"role":"user","content":"你是谁？"}]
  ).with_options(timeout=1800.0)  # 设置最长等待时间
  ```

### LangChain 集成
LangChain 支持双路径集成：
- `langchain_openai.ChatOpenAI`：仅支持百炼 OpenAI 兼容模型子集，需配置 `base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"`；
- `langchain_community.chat_models.tongyi.ChatTongyi`：支持百炼全部文本模型（含部署模型），使用原生 DashScope 协议，需安装 `dashscope` 包；详情见 [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。

## 限制和注意事项

- **地域绑定**：API Key 与 `base_url` 所属地域必须严格一致（如北京 Key 只能调用北京 endpoint），跨地域调用将返回 `invalid_api_key` 错误；该规则适用于所有兼容接口，[OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md) 文档中已明确说明。
- **文件大小限制**：`file-extract` 用途单文件 ≤ 150 MB，`batch` 用途 ≤ 500 MB，`fine-tune` 用途 ≤ 300 MB；超出将直接拒绝上传。
- **Batch 场景特殊性**：`qwen3.5-omni-plus` 在 Batch 模式下不支持语音输出；`qwen3.8` 系列模型默认开启思考模式，若未显式设置 `enable_thinking=false`，将产生额外 reasoning tokens 成本。
- **三方模型可用性**：DeepSeek、Kimi 等三方直供模型仅在中国站华北2（北京）地域可用，且需在控制台单独开通服务；该限制在 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md) 中重点标注。
- **旧路径弃用**：`/api/v2/apps/protocols/compatible-mode/v1/responses` 和 `/api/v2/apps/protocols/compatible-mode/v1/conversations` 已停止维护，必须迁移至 `/compatible-mode/v1/responses` 和 `/compatible-mode/v1/conversations`；[OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md) 与 [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md) 均已发出强提示。

## 来源文档

- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)


