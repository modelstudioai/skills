# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一套标准化 REST API 协议，完全遵循 OpenAI 的请求格式、响应结构与语义规范（如 `/v1/chat/completions`），使开发者能直接复用现有 OpenAI SDK（如 `openai==1.0+`）、工具链和代码逻辑，零改造调用百炼托管的 Qwen 全系列模型及主流第三方模型。

## 在百炼平台的不同场景中，这个概念如何使用

- **快速接入与迁移**：无需重写业务逻辑，只需替换 `base_url` 和 `api_key`，即可将原有 OpenAI 应用无缝迁移到百炼，适用于原型验证、A/B 测试或混合模型路由场景。  
- **多模型统一调度**：同一套 OpenAI SDK 代码可切换调用 `qwen3.7-plus`、`qwen3.8-omni-flash`、`deepseek-v4-pro` 等不同能力模型，仅需修改 `model` 字段，降低多模型集成复杂度。  
- **Agent 与工具链开发**：支持 OpenAI-style `tools` 参数声明（如 `{"type": "web_search"}`），配合 `tool_choice` 自动触发联网搜索、代码解释器等内置能力，适用于构建智能体（Agent）应用。  
- **流式响应与结构化输出**：完整支持 `stream: true`（SSE 流式传输）和 `response_format: {"type": "json_object"}`，满足实时对话、前端增量渲染及强 Schema 约束等生产需求。  
- **不适用场景**：Qwen-Audio、部分语音/视频专用模型（如 `wanx-video`、`speech-to-speech`）及需显式缓存控制（`cache_control`）的高级用例，需改用 DashScope 原生协议。

## 关键参数和配置

| 参数 | 必填 | 说明 | 示例 |
|------|------|------|------|
| `base_url` | ✅ | OpenAI 兼容接口根地址，**必须与 API Key 所属地域和计费方案匹配**。推荐使用业务空间专属域名（高吞吐、低延迟、流量隔离）。 | `https://ws-abc123.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| `api_key` | ✅ | 通过百炼控制台创建的 API Key，需设置为环境变量 `DASHSCOPE_API_KEY` 或 SDK 初始化参数。注意：主账号维度生效，跨地域不通用。 | `sk-xxx` |
| `model` | ✅ | 请求的目标模型 ID，区分大小写，必须在当前地域可用且权限已授权。 | `"qwen3.7-plus"`、`"deepseek-v4-pro"` |
| `messages` | ✅ | 标准 OpenAI 消息数组，含 `role`（`system`/`user`/`assistant`）和 `content`（字符串或含 `image_url` 的[多模态](multimodal.md)内容）。 | `[{"role":"user","content":"你好"}]` |
| `tools` | ❌（可选） | 声明可用工具列表，启用自动工具调用。仅部分模型（如 `qwen3.8-omni-flash`）支持有限工具集。 | `[{"type":"web_search"}]` |
| `response_format` | ❌（可选） | 强制结构化输出，支持 `{"type": "json_object"}`（需模型支持 JSON 模式）。 | `{"type": "json_object"}` |
| `stream` | ❌（可选） | 启用流式响应，返回 `text/event-stream`；前端需按 SSE 协议解析。 | `true` |
| `temperature` / `top_p` / `max_tokens` | ❌（可选） | 标准采样参数，行为与 OpenAI 一致（`temperature` 范围 `0.0–2.0`，默认 `1.0`）。 | `{"temperature": 0.7, "max_tokens": 1024}` |

> ⚠️ 注意：  
> - 不支持 OpenAI 的 `functions`（旧版[函数调用](function-calling.md)），请统一使用 `tools`；  
> - `system` 消息在 `messages` 数组首位即生效，无需额外字段；  
> - [多模态](multimodal.md)输入（图像）需使用 `content` 数组格式，含 `{"type": "image_url", "image_url": {"url": "data:image/png;base64,..."} }`；  
> - 所有请求均受账号级 RPM（每分钟调用次数）与 TPM（每分钟 [Token](token.md) 总消耗）双重限流，超限返回 `429`。

## 面向开发者，简洁实用

- ✅ **立刻上手**：复制示例代码，填入你的 `WorkspaceId` 和 `DASHSCOPE_API_KEY`，5 分钟完成首次调用。  
- ✅ **零适配成本**：`openai>=1.0.0` SDK、LangChain、LlamaIndex 等生态工具开箱即用。  
- ✅ **生产就绪**：业务空间专属域名提供 SLA 保障，支持监控、审计日志与用量分析。  
- ❌ **避免踩坑**：  
  - 不要用 DashScope 域名（`dashscope.aliyuncs.com`）用于新项目——2026 年 9 月起停更；  
  - 不要硬编码 API Key，务必通过环境变量注入；  
  - 不要跨地域混用 Key 与 Base URL，否则返回 `401 Unauthorized`；  
  - 测试勿用试用域名（`trial.*`），其限流极严，仅限功能验证。  

> 提示：调试时优先使用 [百炼控制台 → 模型体验页](https://bailian.console.aliyun.com/model/experience)，可视化查看请求/响应、自动补全参数、一键生成 SDK 代码。

## 关联主题页

- [get started with models](../guides/get-started-with-models.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [model experience](../guides/model-experience.md)


