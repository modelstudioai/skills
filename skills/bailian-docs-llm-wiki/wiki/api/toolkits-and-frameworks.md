# toolkits and [frameworks](frameworks.md)

阿里云百炼平台提供多种 [OpenAI 兼容接口](../concepts/openai-compatibility.md)，覆盖文本生成、多模态理解、向量化、批量处理、对话管理及文件操作等核心场景。开发者可复用现有 OpenAI 生态代码（如 SDK、LangChain 集成），仅需调整 `base_url`、`api_key` 和模型名即可快速迁移。所有接口均支持标准 OpenAI 请求/响应格式，并针对百炼模型能力进行了增强（如内置工具、长上下文、自动上下文管理等）。

## 支持的模型/功能

- **文本生成**：`qwen3.8-max`、`qwen3.7-plus`、`qwen3.5-flash` 等全系 Qwen 文本模型；第三方模型如 `deepseek-v4-pro`、`glm-5.3`、`kimi-k3`（[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)）。
- **多模态理解**：`qwen3-vl-plus`、`qwen3-vl-flash`、`qwen3-omni-flash`、`QVQ`、`Qwen-OCR`，支持图像 URL / Base64 输入与结构化 content 数组（[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)）。
- **向量嵌入**：`text-embedding-v4`、`qwen3.7-text-embedding`、`text-embedding-v2`，支持多维度配置与 201 种语种（[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)）。
- **长文档与文件分析**：`Qwen-Long`、`Qwen-Doc-Turbo`，通过 `file-extract` 用途上传文件后调用（[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)）。
- **批量处理**：
  - 文件批量（Batch File）：支持 JSONL 格式，适用于评测、数据标注等异步场景；
  - 单请求批量（Batch Chat）：同步调用但后台异步执行，成本降低 50%；
  - Embedding 批量：在 `text-embedding-v4` 等模型上启用 Batch 调用可享半价（[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)）。
- **对话状态管理**：`Conversations API` 提供会话创建、消息追加、元数据更新与删除，配合 `Responses API` 实现跨设备上下文延续（[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)）。

> **注意**：`Qwen-Audio` 明确不支持 OpenAI 兼容协议，仅支持 DashScope 原生协议（见 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)）。另，`completions` 接口当前**仅限华北2（北京）地域**且**仅支持 `qwen-coder-turbo` 模型**（见 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)），与其他接口的多地域、多模型支持存在显著差异。

## 关键参数

| 参数 | 类型 | 说明 | 备注 |
|------|------|------|------|
| `base_url` | string | 接口服务地址，必须匹配地域与业务空间 | 必须使用 `{WorkspaceId}` 替换占位符；旧域名（如 `dashscope.aliyuncs.com`）仍可用但**不推荐**（见 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)） |
| `model` | string | 模型标识符 | 不同接口支持范围不同：`Responses API` 支持 `qwen3.8-omni-flash` 处理音视频；`completions` 仅支持 `qwen-coder-turbo`；`Embedding` 仅支持指定 embedding 模型（见各文档） |
| `stream` | boolean | 是否启用[流式输出](../concepts/streaming.md) | `true` 时返回 `chat.completion.chunk`；`Responses API` 还支持 `stream_options={"include_usage": true}` 在末尾返回 token 统计 |
| `previous_response_id` | string | 上一轮 `responses.create()` 返回的顶层 `id` | 用于 `Responses API` 多轮对话，**非 `output` 数组内 `msg_xxx` ID**（见 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)） |
| `enable_thinking` | boolean | 控制是否启用思考模式（产生 reasoning tokens） | 对 `qwen3.5+` 系列模型默认开启，**必须作为 `body` 顶层参数传入**，不可置于 `extra_body`（见 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)） |

## 使用方式

1. **环境准备**  
   - 获取对应地域的 API Key（[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)）；  
   - 安装 SDK：`pip install -U openai langchain_openai`（Python）、`npm install @langchain/openai @langchain/community`（JS）等；  
   - 推荐将 `DASHSCOPE_API_KEY` 配置为环境变量以降低泄露风险。

2. **SDK 初始化**  
   ```python
   from openai import OpenAI
   client = OpenAI(
       api_key=os.getenv("DASHSCOPE_API_KEY"),
       base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"  # 替换为实际 WorkspaceId
   )
   ```

3. **接口调用示例**  
   - **Chat Completions**（标准对话）：`client.chat.completions.create(model="qwen-plus", messages=[...])`  
   - **Responses API**（智能体原生）：`client.responses.create(model="qwen3.8-max", input="你好")`  
   - **Embedding**：`client.embeddings.create(model="text-embedding-v4", input="文本")`  
   - **文件上传**：`client.files.create(file=Path("doc.pdf"), purpose="file-extract")`  
   - **LangChain 集成**：使用 `ChatOpenAI`（兼容部分模型）或 `ChatTongyi`（支持全部模型）（见 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)）  

4. **地域与鉴权**  
   - API Key 严格按地域绑定：北京 Key 只能调用北京 endpoint，否则返回 `invalid_api_key`（HTTP 401）；  
   - `WorkspaceId` 从控制台「业务空间详情」获取，是专属域名必要组成部分。

## 限制和注意事项

- **地域限制**：`completions` 接口仅支持华北2（北京）；`Responses API` 新加坡、弗吉尼亚、法兰克福、东京、中国香港均支持；`Conversations API` 当前仅北京与新加坡支持（见 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md) 和 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)）。
- **模型能力差异**：  
  - `qwen3.8-omni-flash` 在 `Responses API` 中支持音视频输入，但在 `Chat Completions` 中不支持；  
  - `Qwen-VL` 等视觉模型在 `Chat Completions` 中需使用 `content` 数组格式（含 `image_url`），而 `completions` 接口完全不支持多模态；  
  - `file-extract` 用途上传的文件最大 150 MB，`batch` 用途最大 500 MB（见 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)）。
- **超时与重试**：  
  - `Batch Chat` 默认超时 3600 秒，需显式设置 `timeout`（如 Python 的 `with_options(timeout=1800)`）；  
  - `conversations.create` 等长耗时操作无内置重试，建议应用层实现幂等与重试逻辑。
- **错误排查重点**：  
  - HTTP 401：检查 API Key 地域是否匹配 `base_url` 所属地域；  
  - HTTP 404：确认 endpoint 路径是否为新版（如 `/compatible-mode/v1/responses` 而非 `/api/v2/.../v1/responses`）；  
  - `invalid_api_key` 错误码：99% 为地域不匹配，而非密钥失效（见 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)）。

## 来源文档

- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)


