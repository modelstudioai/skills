# agent store

agent store 是百炼平台提供的模型能力分发与复用中心，用于统一管理、发布和调用经过封装的 Agent 能力（如 Skill、MCP 等）。开发者可通过 Store 发现、订阅并集成第三方或平台预置的结构化智能体能力，降低重复开发成本。其设计遵循标准化协议，支持按需加载与权限管控。

## 支持的模型/功能

agent store 当前主要支持两类可复用能力单元：
- **Skill**：面向具体任务封装的原子能力（如“查天气”“解析 PDF”），具备明确定义的输入/输出 Schema 和执行逻辑，详见 [Skill](../../raw/application-user-guide/agent-store/skill.md)；
- **MCP（Model Context Protocol）**：一种轻量级上下文交互协议，用于在不同模型间传递结构化上下文与指令，适用于多步协同场景，详见 [MCP](../../raw/application-user-guide/agent-store/model-context-protocol.md)。

> **注意**：原始文档中未明确说明是否支持 LLM 模型本身（如 Qwen 系列）直接上架为 Store 资源；根据 [Store](../../raw/application-user-guide/agent-store.md) 的上下文，Store 仅承载能力封装体（Skill/MCP），不托管基础大模型权重或推理服务。

## 关键参数

调用 Store 中的能力时，需在请求中指定以下必需参数：
- `store_id`：全局唯一标识符，由平台分配，用于定位具体 Skill 或 MCP 实例；
- `version`：语义化版本号（如 `v1.2.0`），默认使用 `latest`，但生产环境强烈建议锁定具体版本；
- `input`：符合该能力 Schema 的 JSON 对象，字段名与类型须严格匹配，否则触发校验失败。

## 使用方式

1. 在控制台「Agent Store」页面浏览/搜索能力，点击进入详情页获取 `store_id` 和接口文档；
2. 调用 `/v1/agent/store/invoke` 接口，以 POST 方式提交含 `store_id`、`version` 和 `input` 的 JSON 请求体；
3. 解析返回的 `output` 字段（结构化 JSON）或 `error` 字段（标准错误码与消息）。

完整调用示例与 SDK 封装见 [Store](../../raw/application-user-guide/agent-store.md)。

## 限制和注意事项

- 单次调用最大 `input` 大小为 256 KB，超限将返回 `413 Payload Too Large`；
- 同一 `store_id` 下，免费版用户最多并发调用 5 路，企业版配额可配置；
- Skill 执行超时默认为 30 秒，MCP 协议链路超时为 60 秒，不可覆盖；
- 所有 Store 能力均运行于沙箱环境，禁止访问外网、读写本地文件系统或执行系统命令——此约束在 [Skill](../../raw/application-user-guide/agent-store/skill.md) 和 [MCP](../../raw/application-user-guide/agent-store/model-context-protocol.md) 文档中均有强调。

## 来源文档

- [Store](../../raw/application-user-guide/agent-store.md)


