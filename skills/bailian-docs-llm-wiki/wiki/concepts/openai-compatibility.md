# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一组标准化 REST API，严格遵循 OpenAI 官方 API 的路径、请求体结构、响应格式与错误码规范，使开发者能复用现有 OpenAI SDK、工具链和业务代码，零改造接入 Qwen 系列大模型能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **快速集成开发**：开发者可直接使用 `openai` Python SDK、LangChain 的 `ChatOpenAI` 类或各类支持 OpenAI 标准的客户端（如 Cursor、Postman、Dify、Cherry Studio），仅需替换 `base_url` 和 `model` 参数即可调用百炼托管的 `qwen-max`、`qwen-plus` 等模型，无需重写逻辑。  
- **多模态与扩展能力**：除标准 `chat/completions` 外，兼容接口还覆盖 `completions`（文本补全）、`embeddings`（向量生成）、`vision`（图像理解）、`files`（文件上传/管理）、`batches`（异步批量处理）和 `conversations`（会话历史）等端点，满足多样化生产需求。  
- **[模型部署](model-deployment.md)服务化**：通过专属部署、PTU 或 [Token](token.md) 按量部署的模型，同样可通过 `/v1/chat/completions?deployment_id=xxx` 路径以 OpenAI 兼容方式调用，实现资源隔离与弹性伸缩下的统一接入体验。  
- **文件与批量任务协同**：`/compatible-mode/v1/files` 和 `/compatible-mode/v1/batches` 接口与 OpenAI Batch 流程完全对齐（如先上传文件再提交任务），便于迁移已有数据处理流水线。  
- **轻量验证与调试**：配合百炼控制台生成的临时 API Key 与标准 `Authorization: Bearer <api_key>` 认证，可快速在本地 CLI 或 IDE 中完成原型验证，跳过阿里云 AccessKey 签名复杂流程。

## 关键参数和配置

- **认证方式**：统一使用 `Authorization: Bearer <api_key>`（`api_key` 需在百炼控制台「API 密钥管理」中创建，非阿里云 AccessKey）。  
- **基础 URL**：`https://dashscope.aliyuncs.com/compatible-mode/v1`（注意路径含 `compatible-mode`，非 `/v1` 或 `/api/v1`）。  
- **必填字段**：  
  - `model`: 字符串，必须为百炼已开通的模型 ID（如 `"qwen-turbo"`），**不可使用 `gpt-4` 等 OpenAI 模型名**；  
  - `messages`: 数组，格式为 `[{ "role": "user", "content": "..." }]`，支持 `system`、`user`、`assistant` 角色；  
  - `stream`: 布尔值，设为 `true` 启用流式响应（SSE），适用于实时对话场景。  
- **常用采样参数（顶层字段）**：  
  - `temperature`: 浮点数（0.0–2.0），控制输出随机性；  
  - `max_completion_tokens`: 整数，替代 OpenAI 的 `max_tokens`，指定最大输出 token 数；  
  - `top_p`: 浮点数（0.0–1.0），核采样阈值；  
  - `stop`: 字符串或字符串数组，自定义终止序列。  
- **不支持的 OpenAI 参数**：`functions` / `tools`（[函数调用](function-calling.md)）、`response_format`（结构化输出）、`presence_penalty`、`frequency_penalty`、`logit_bias` 等非标准字段将被忽略，需改用百炼原生 `tool_call` 或 DashScope 接口。

## 面向开发者，简洁实用

- ✅ **即开即用**：安装 `openai==1.45.0+` 或更高版本，初始化时设置 `base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"` 和 `api_key="sk-xxx"`，其余代码无需修改。  
- ✅ **错误处理一致**：返回标准 OpenAI 错误格式（如 `{ "error": { "message": "...", "type": "invalid_request_error", "code": "model_not_found" } }`），可复用原有错误捕获逻辑。  
- ⚠️ **注意差异**：  
  - `messages` 数组超过 100 条时，服务端自动截断最早 20 条；  
  - `files` 接口仅支持 Base64 编码图像（不支持远程 URL）；  
  - `embeddings` 输入长度上限为 8192 tokens；  
  - 所有配额、计费、限流均按百炼平台规则执行，与 OpenAI 独立结算。  
- 🚀 **推荐实践**：新项目优先选用 OpenAI 兼容接口；若需 `tools`、`response_format` 或精细参数（如 `top_k`、`repetition_penalty`），请切换至 [DashScope 原生接口](https://help.aliyun.com/zh/model-studio/qwen-api-via-dashscope)。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [model deployment 1](../guides/model-deployment-1.md)
- [file management api](../api/file-management-api.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [more about models](../api/more-about-models.md)


