# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一套标准化 RESTful API 协议，其请求/响应格式、路径、参数命名与语义均严格对齐 OpenAI 官方 API（如 `/v1/chat/completions` 和 `/v1/responses`），使开发者无需修改核心调用逻辑，即可将基于 OpenAI SDK 或适配器的代码无缝迁移至百炼平台。

## 在百炼平台的不同场景中如何使用

- **通用大模型调用**：通过 `POST /v1/chat/completions` 调用 Qwen 系列（如 `qwen3.8-max`、`qwen3.7-plus`）、DeepSeek、GLM、Kimi 等支持模型，适用于对话、摘要、生成等标准 LLM 场景；支持[多模态](multi-modal.md)输入（图像、视频、PDF 文件）——其中 Qwen-Omni 支持视频文件上传，Qwen-VL/QVQ 支持图像理解。
- **高级智能体能力集成**：通过 `POST /v1/responses`（OpenAI 兼容 Responses 协议）启用完整工具调用链路（`web_search`、联网搜索、网页抓取、代码解释器）、显式缓存（`cache_control.type = "ephemeral"`）和 Session 级缓存（`x-dashscope-session-cache: enable`），适合构建需长期上下文、外部动作执行的 Agent 应用。
- **Flow Agent 工作流接入**：在 Flow Agent 的「OpenAI 兼容模式」下，可通过 `POST /api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses` 直接复用 OpenAI 风格的 `messages` 输入结构调用已发布的智能体应用，降低工作流集成门槛。
- **不适用场景**：Qwen-Audio 模型**明确不支持** OpenAI 兼容协议，必须使用 DashScope 原生协议；QwQ/QVQ 模型的 `system` 角色消息无效，调用时应避免设置。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 | 示例值 |
|------|------|------|------|--------|
| `model` | string | 是 | 模型 ID，需与 OpenAI 兼容协议支持列表一致（覆盖最广） | `"qwen3.8-max"`, `"deepseek-v4.1-flash-1017"` |
| `messages` | array | 是（Chat）<br>否（Responses） | Chat 接口必填，格式为 `[{role: "user"/"assistant"/"system", content: string}]`；Responses 接口可选，若提供则自动转为 `input` 字段 | `[{"role":"user","content":"解释量子纠缠"}]` |
| `stream` | boolean | 否 | 是否启用流式响应（SSE）。设为 `true` 时，客户端需正确解析 Server-Sent Events | `true` |
| `incremental_output` | boolean | 否（仅 Responses） | 仅当 `stream=true` 时生效，控制是否返回增量 token（推荐开启） | `true` |
| `tools` | array | 否 | 定义可调用工具。支持内置工具（如 `{"type": "web_search"}`）和自定义 function schema | `[{"type": "web_search"}, {"type": "function", "function": {...}}]` |
| `tool_choice` | string / object | 否 | 控制工具调用策略：`"auto"`（默认）、`"none"` 或指定 `{"type": "function", "function": {"name": "xxx"}}` | `"auto"` |
| `cache_control` | object | 否（仅 Chat） | 显式缓存控制：`{"type": "ephemeral"}` 表示本次请求结果可被后续相同请求命中 | `{"type": "ephemeral"}` |
| `max_tokens` | integer | 否 | 最大输出 token 数（非总长度）。注意：不同模型语义不同（如 `qwen3.8-max` 包含思考+回复，`qwen3.7-plus` 仅限回复） | `2048` |
| `temperature` | number | 否 | 温度值，范围 `[0, 2)`，高于 OpenAI 官方 `[0, 1]` 上限，迁移时建议校准 | `0.7` |

> **Endpoint 格式**：推荐使用业务空间专属域名 `https://{WorkspaceId}.{region}.maas.aliyuncs.com`（如 `https://ws-abc123.cn-beijing.maas.aliyuncs.com`），性能与稳定性优于公共域名。  
> **认证方式**：统一使用 `Authorization: Bearer <API_KEY>` Header，API Key 在百炼控制台「API 密钥管理」中创建。  
> **地域限制**：所有 OpenAI 兼容接口（包括 Chat 和 Responses）**仅支持华北2（北京）地域**，跨地域调用将失败。

## 开发者提示

- ✅ **快速验证**：用 `curl` 即可发起首调，无需 SDK：
  ```bash
  curl -X POST "https://ws-xxx.cn-beijing.maas.aliyuncs.com/v1/chat/completions" \
    -H "Authorization: Bearer YOUR_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
          "model": "qwen3.8-max",
          "messages": [{"role": "user", "content": "你好"}],
          "stream": false
        }'
  ```
- ✅ **流式处理**：启用 `stream=true` 时，务必按 SSE 格式逐行解析（每行以 `data:` 开头），避免直接 JSON.parse 整个响应体。
- ⚠️ **避坑提醒**：
  - 不要为 QwQ/QVQ 模型设置 `system` 消息；
  - `temperature` 超出 `[0, 2)` 将报错，`top_p` 等其他采样参数在 OpenAI 兼容接口中**暂不支持**；
  - [多模态](multi-modal.md)输入需确保文件已通过百炼文件服务上传并获得 `file_id`，再以 `{"type": "image_url", "image_url": {"url": "file-{id}"}}` 形式传入 `content`。

如需进一步了解具体模型能力边界或错误码含义，请查阅对应协议文档：[OpenAI 兼容 Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)、[OpenAI 兼容 Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [get started with models](../guides/get-started-with-models.md)
- [managed agents api](../api/managed-agents-api.md)
- [flow agent api](../api/flow-agent-api.md)


