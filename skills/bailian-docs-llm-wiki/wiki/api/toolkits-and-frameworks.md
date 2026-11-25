# toolkits and [frameworks](frameworks.md)

阿里云百炼提供多套 OpenAI 兼容的工具包与框架，覆盖文本生成、多模态理解、[向量嵌入](../concepts/vector-embedding.md)、批量推理、会话管理及文件处理等核心场景。开发者可复用现有 OpenAI SDK 和工程实践，仅需调整 `base_url`、`api_key` 和 `model` 参数即可快速迁移。所有接口均支持主流编程语言（Python/Node.js/Java/Go/C#）和 HTTP 直调。

## 支持的模型/功能

百炼兼容 OpenAI 的六大类接口分别支持不同模型与能力：

- **Chat 接口**：支持全系列 Qwen 文本模型（如 `qwen4-max`、`qwen3.8-plus`）、Qwen-VL、Qwen-Coder、DeepSeek、Kimi、GLM 等；但 [Qwen-Audio 不支持 OpenAI 兼容协议](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)，仅支持 DashScope 原生协议 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。
- **Responses 接口**：专为智能体（Agent）设计，内置联网搜索、网页抓取、代码解释器等工具，仅对阿里云直供模型（如 `qwen4-max`、`qwen3.8-omni-flash`）完整开放 Agent 能力；非直供模型仅支持基础兼容 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。
- **Vision 接口**：支持 `qwen3-vl-plus`、`QVQ`、`Qwen-OCR` 等视觉模型，用于图像/视频理解与文字提取 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)。
- **Embedding 接口**：支持 `text-embedding-v4`、`qwen3.7-text-embedding` 等向量模型，但**不支持稀疏向量输出**（传入 `output_type=sparse` 将返回空 embedding）[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)。
- **Conversations 接口**：用于跨设备/长时间对话的上下文持久化，配合 Responses API 实现自动历史注入，支持 `system`/`developer`/`user`/`assistant` 多角色消息 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)。
- **Files 与 Batch 接口**：`files` 接口支持 `file-extract`（文档问答）、`batch`（批量任务）、`fine-tune`（调优数据集）三类用途；`batch` 接口分文件输入（JSONL）与单请求同步两种模式，后者称为 Batch Chat [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。

> **注意**：文档 4（Batch 文件）与文档 5（Batch Chat）对同一模型的上下文长度限制表述存在差异——文档 4 称 `qwen3.8-max` 等支持 256K token，而文档 5 未明确该数值。以文档 4 为准，因其位于 Batch 核心流程说明章节，且与 Responses API 文档中 `qwen3.8-omni-flash` 的 Omni 模态能力描述一致。

## 关键参数

| 参数 | 说明 | 示例值 | 注意事项 |
|------|------|--------|----------|
| `base_url` | 必填，服务端点地址 | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | `{WorkspaceId}` 需替换为控制台获取的真实 ID；旧域名（如 `dashscope.aliyuncs.com`）已逐步停用，详见各文档“重要”提示 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md) |
| `model` | 必填，模型名称 | `qwen4-max`, `qwen3-vl-plus`, `text-embedding-v4` | 模型必须在对应接口的支持列表中，且地域需匹配 API Key（跨地域调用将返回 `invalid_api_key`） |
| `enable_thinking` | 可选，控制思考模式 | `true` / `false` | `qwen3.5+` 系列默认开启，开启后产生额外 `reasoning_tokens`；**必须作为 `body` 顶层参数传入，不可置于 `extra_body` 内** |
| `previous_response_id` | Responses 多轮对话专用 | `"0c842a11-c7d1-45da-b7ec-4e668c389xxx"` | 必须传入上一轮响应的顶层 `id`（UUID），而非 `output` 数组内消息的 `id` |
| `purpose` | Files 接口必填 | `"file-extract"`, `"batch"`, `"fine-tune"` | 决定文件用途及格式要求（如 `file-extract` 支持 PDF/DOCX，`batch` 仅接受 JSONL） |

## 使用方式

### 通用步骤
1. **获取并配置 API Key**：在百炼控制台对应地域创建 API Key，并设为环境变量 `DASHSCOPE_API_KEY`；
2. **设置 `base_url`**：按地域选择专属域名（推荐）或通用域名；
3. **安装 SDK**（可选）：`pip install -U openai langchain_openai` 或对应语言 SDK；
4. **发起调用**：使用标准 OpenAI SDK 方法（如 `client.chat.completions.create`）或 HTTP POST。

### 各接口典型调用路径
- **Chat/Responses/Vision/Embedding**：直接调用 `create()` 方法，传入 `model` + 输入内容（`messages`/`input`/`content`）；
- **Conversations**：先 `client.conversations.create()` 创建会话，再在后续 `responses.create()` 中通过 `conversation_id` 关联；
- **Files**：先 `client.files.create(file=..., purpose=...)` 上传，获得 `file_id` 后用于文档分析、Batch 或调优任务；
- **Batch（文件）**：上传 JSONL 文件 → `client.batches.create(input_file_id=..., endpoint="/v1/chat/completions")` → 轮询状态 → 下载 `output_file_id`；
- **Batch Chat（单请求）**：将 `base_url` 替换为 `https://batch.dashscope.aliyuncs.com/compatible-mode/v1`，其余参数同实时 Chat。

## 限制和注意事项

- **地域绑定严格**：API Key 与 `base_url` 所属地域必须一致（如北京 Key 只能调北京 endpoint），否则返回 `invalid_api_key`（HTTP 401）；
- **域名迁移强制性**：`/api/v2/apps/protocols/...` 等旧路径已废弃，新版统一为 `/compatible-mode/v1/...`，且推荐使用业务空间专属域名（如 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）；
- **文件配额硬限制**：`files` 接口总存储上限为 **10,000 个文件 + 100 GB**，超限后上传失败，需手动清理；
- **Batch 超时机制**：Batch Chat 默认等待 3600 秒（1 小时），超时断连；Batch 文件任务最长等待 24 小时；
- **模型能力差异**：三方直供模型（如 SiliconFlow DeepSeek）仅在中国站华北2（北京）可用，且需在控制台单独开通服务；
- **LangChain 集成建议**：若需使用全部百炼模型（含非 OpenAI 兼容模型如 Qwen-Audio），应优先选用 `langchain-community` 的 `ChatTongyi`（Python）或 `ChatAlibabaTongyi`（JS）集成，而非 `langchain_openai` [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。

## 来源文档

- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)
- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)


