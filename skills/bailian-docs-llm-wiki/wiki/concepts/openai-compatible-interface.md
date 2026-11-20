# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一套标准化 REST API 协议层，完全遵循 OpenAI 官方 API 的路径、请求/响应结构、参数命名与语义规范（如 `/chat/completions`、`/embeddings`、`/batches` 等），使开发者无需修改业务逻辑即可将现有 OpenAI 集成快速迁移到百炼托管的 Qwen 系列及专用模型上。

## 在百炼平台的不同场景中如何使用

- **通用大模型调用**：通过 `chat/completions` 端点调用 `qwen4-max`、`qwen3.7-plus`、`qwen3.8-flash` 等文本模型，支持多模态输入（图像/Base64、PDF、视频帧）、系统消息、工具调用（`tools` + `tool_choice`）和 Session 上下文缓存（需 `x-dashscope-session-cache: enable` 请求头）。
- **向量与嵌入服务**：通过 `/embeddings` 端点调用百炼专用嵌入模型（如 `text-embedding-v3`），兼容 OpenAI 的 `input` 字段格式（string 或 string[]），但不支持 `response_format=json_object`。
- **批量异步处理**：通过 `/batches` 端点提交 JSONL 格式任务文件（上限 100MB），适用于大规模文本生成或嵌入计算；注意该端点不支持流式响应与 `json_object` 输出格式。
- **智能体（Agent）开发**：通过专属路径 `/compatible-mode/v1/agents/chat/completions` 调用 `qwen-plus-agent-v1` 等 Agent 专用模型，支持工具自动选择、Session 持久化、Environment 隔离执行与 Vault 敏感凭证注入，语义与 OpenAI Agents API 高度对齐。
- **垂直场景模型接入**：`tongyi-intent-detect-v3`（意图识别）、`gui-plus`（GUI 自动化）、`qwen3.5-ocr`（OCR）等专用模型均支持 OpenAI 兼容接口；但 `qwen-deep-research` 等研究型模型**明确不支持**该协议，仅限 DashScope SDK 调用。

> ⚠️ 注意：Qwen-Audio 模型不支持 OpenAI 兼容协议；QwQ/QVQ 模型的 `system` 消息无效；所有模型必须使用百炼平台颁发的 `api_key`，且不可复用 OpenAI 密钥。

## 关键参数和配置

| 参数 | 是否必填 | 说明 | 兼容性备注 |
|------|----------|------|------------|
| `model` | ✓ | 百炼控制台已开通的模型 ID（如 `qwen4-max`、`qwen-plus-agent-v1`），**不可使用 `gpt-4` 等 OpenAI 模型名** | 所有端点均强制校验，非法值返回 404 |
| `api_key` | ✓（Header） | 百炼平台生成的密钥（`Bearer <sk-xxx>`），需在控制台「API Keys」中创建并授权对应权限（如 `agents:run`） | 不兼容 OpenAI 密钥；LangChain 需配合 `BailianLLM` 使用 |
| `base_url` | ✓（客户端配置） | 必须显式设置为：<br>• 通用接口：`https://dashscope.aliyuncs.com/api/v1`<br>• Agents 接口：`https://dashscope.aliyuncs.com/compatible-mode/v1/agents`<br>• **推荐生产环境使用业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`） | LangChain 示例易遗漏此配置，导致连接失败 |
| `messages` | ✓（`chat/completions`） | 标准 OpenAI 消息数组，支持 `role: "system"/"user"/"assistant"/"tool"`；`tool` 消息需含 `tool_call_id` 和 `content` | `gui-plus`、`qwen-vl-ocr` 支持 `image_url.data:image/*;base64,...` 内联图；**不支持 `image_url.url` 远程链接** |
| `tools` / `tool_choice` | ✗ | 工具定义与调用策略，格式与 OpenAI 完全一致；`tool_choice="auto"` 时自动触发[函数调用](function-calling.md) | `stream=True` 时该功能被静默忽略（不支持 streaming + function calling 组合） |
| `response_format` | ✗ | 仅 `chat/completions` 支持 `{"type": "json_object"}`；其他端点（如 `embeddings`、`batches`）传入将被忽略 | 启用后模型将严格输出合法 JSON，无需额外解析 |
| `session_id` | ✗（Agents） | 复用已有会话上下文；首次调用可省略，服务自动生成并返回 | Session 默认 TTL 24 小时，超时需主动调用 `/sessions/{id}/extend` 延长 |

## 面向开发者：快速上手建议

- ✅ **首选业务空间专属域名**：性能更优、延迟更低、稳定性更强（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）。
- ✅ **Python 开发者**：直接使用 `openai>=1.0.0` SDK，只需覆盖 `base_url` 和 `api_key`：
  ```python
  from openai import OpenAI
  client = OpenAI(
      api_key="sk-xxx",  # 百炼密钥
      base_url="https://dashscope.aliyuncs.com/api/v1"
  )
  response = client.chat.completions.create(
      model="qwen4-max",
      messages=[{"role": "user", "content": "你好"}]
  )
  ```
- ✅ **LangChain 用户**：导入 `BailianLLM` 替代 `ChatOpenAI`，链式逻辑零改造：
  ```python
  from langchain_community.llms import BailianLLM
  llm = BailianLLM(model="qwen4-max", api_key="sk-xxx")
  ```
- ❌ **避免踩坑**：
  - 不要传 `gpt-4` 等非百炼模型名；
  - 不要对 `batches` 或 `embeddings` 设置 `response_format`；
  - 不要在 `stream=True` 时依赖 `tool_calls`；
  - 图像输入务必用 Base64 内联（`data:image/png;base64,...`），勿用 URL。

如需调试，推荐使用 [百炼 API Playground](https://bailian.console.aliyun.com) 实时验证请求结构与响应。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [openai compatible agents api](../api/openai-compatible-agents-api.md)
- [more models](../api/more-models.md)


