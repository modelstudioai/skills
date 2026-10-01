# OpenAI 兼容接口

OpenAI 兼容接口是阿里云百炼平台提供的一套标准化 API 协议，完全遵循 OpenAI REST API 的请求/响应格式、路径结构与核心字段语义（如 `messages`、`model`、`stream`），使开发者无需修改业务逻辑即可复用现有 OpenAI SDK、工具链或框架代码，快速接入百炼托管的 Qwen 系列大模型及增强能力。

## 在百炼平台的不同场景中如何使用

- **快速迁移已有项目**：只需将 OpenAI SDK 的 `base_url` 替换为百炼专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），并传入百炼颁发的 `api_key` 和支持的 `model` 名称，即可调用文本生成、视觉理解、向量嵌入等服务。
- **构建智能体（Agent）应用**：通过 `/compatible-mode/v1/responses` 端点调用，原生集成联网搜索、网页抓取、代码解释器、文搜图、知识库检索等工具链，支持 `previous_response_id` 多轮上下文管理与 `x-dashscope-session-cache` 自动会话缓存。
- **对接主流开发工具与框架**：兼容 VS Code 插件、Cursor、Dify、LlamaIndex、Spring AI Alibaba 等生态，例如在 LlamaIndex 中直接配置 `DashScopeLLM(model_name="qwen3.8-max")`，或在 Dify 中选择 “OpenAI-compatible” 供应商类型并填入百炼 Base URL 与 Key。
- **多模态任务处理**：在 `/chat/completions` 中通过 `messages.content` 支持 `image_url`、`video_url`；在 `/responses` 中进一步支持 `input_audio`、`input_video`（限 `qwen3.8-omni-flash`），实现音视频理解。
- **批量与文件处理**：结合 `purpose=file-extract` 文件上传接口，配合 `Qwen-Long` 或 `Qwen-Doc-Turbo` 模型完成长文档问答与结构化数据提取。

> ⚠️ 注意：`Qwen-Audio` 模型**不支持** OpenAI 兼容协议，必须使用 DashScope 原生协议；Token Plan 和 Coding Plan 用户需确认所选模型在对应套餐中可用（如 Token Plan 不支持多模态模型）。

## 关键参数和配置

| 参数 | 说明 | 示例值 | 注意事项 |
|------|------|--------|----------|
| `base_url` | 必填，服务入口地址，**必须匹配 Workspace ID 与地域** | `https://ws-abc123.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | 旧域名（如 `dashscope.aliyuncs.com`）仍可工作但不推荐，性能与稳定性较低；子业务空间必须使用专属域名。 |
| `api_key` | 必填，地域与计费方案绑定的凭证 | `sk-xxx`（按量）、`tp-xxx`（Token Plan） | **不可跨地域或跨方案混用**：北京 Key 不能调用弗吉尼亚 endpoint；Token Plan Key 无法用于 Dify 等开放平台。 |
| `model` | 必填，严格区分大小写与版本号 | `qwen3.8-max`, `qwen3-vl-plus`, `text-embedding-v4` | 第三方模型（如 `deepseek-v4-pro`）需在控制台手动开通；`Qwen-Audio` 不在此列表中。 |
| `stream` | 控制输出方式 | `true`（推荐流式） / `false` | 流式响应符合 OpenAI SSE 格式，便于前端实时渲染。 |
| `enable_thinking` | 启用深度思考模式（影响 token 成本与响应时长） | `true` / `false` | 仅对 `qwen3.5+` 系列生效；须置于 JSON 请求体顶层，不可放入 `extra_body`。 |
| `dimensions` | 向量嵌入维度（仅 `text-embedding-v3`/`v4` 支持） | `1024` | `v1`/`v2` 忽略该参数；错误传入不会报错但无效。 |

## 面向开发者：简洁实用提示

- ✅ **一行切换**：Python 中用 `openai.OpenAI(base_url=..., api_key=...)` 即可调用，无需重写逻辑。
- ✅ **调试友好**：所有错误返回标准 OpenAI 格式（如 `{"error": {"message": "...", "type": "invalid_request_error"}}`），便于日志解析与监控。
- ✅ **端点明确**：
  - 对话生成 → `POST /chat/completions`
  - 智能体增强 → `POST /responses`（推荐新项目使用）
- ✅ **安全实践**：始终从百炼控制台获取 Workspace ID 和对应地域的 API Key；避免硬编码或跨环境复用密钥。
- ❌ **避坑提醒**：
  - 不要尝试用 OpenAI 兼容接口调用 `Qwen-Audio`；
  - 不要将 Token Plan Key 用于 Dify、OpenClaw 等要求按量计费的平台；
  - `/responses` 的旧路径（`/api/v2/apps/protocols/compatible-mode/v1/responses`）已下线，请务必迁移到 `/compatible-mode/v1/responses`。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [application call](../api/application-call.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [frameworks](../api/frameworks.md)


