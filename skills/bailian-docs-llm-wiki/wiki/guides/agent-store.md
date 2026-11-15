# agent store

agent store 是百炼平台提供的模型能力与技能的集中注册、发现与调用服务，用于在 Agent 应用中动态加载和组合外部模型能力（如 MCP）或预置技能（Skill）。它通过标准化接口实现能力解耦，支持运行时按需拉取与执行。开发者无需硬编码集成逻辑，即可复用平台托管的能力模块。

## 支持的模型/功能

agent store 当前主要支持两类可注册能力：
- **MCP（Model Context Protocol）**：提供结构化上下文交互协议，支持模型间上下文传递与协同推理，详见 [MCP](../../raw/application-user-guide/agent-store/model-context-protocol.md)；
- **Skill（技能）**：封装了特定业务逻辑（如查天气、发邮件）的可复用函数单元，具备明确输入/输出 Schema 和权限声明，详见 [Skill](../../raw/application-user-guide/agent-store/skill.md)。

> **注意**：文档 [Store](../../raw/application-user-guide/agent-store.md) 中未明确说明是否支持自定义 LLM 模型直接注册为 store 条目；根据当前实现，仅 MCP 和 Skill 为官方支持类型，其他模型需通过 MCP 封装后接入。

## 关键参数

调用 store 中的能力时，需在 `agent_config.yaml` 或 API 请求体中指定以下关键字段：
- `store_id`: 必填，全局唯一标识符（如 `mcp://github.com/xxx/weather-v1`），遵循 `type://namespace/name@version` 格式；
- `input_schema`: 可选，用于校验传入参数结构，必须与注册时声明的 Schema 兼容；
- `timeout_ms`: 可选，默认 30000（30 秒），超时将中断调用并返回错误。

## 使用方式

1. **注册能力**：通过控制台或 `POST /v1/store/register` 接口提交 MCP 或 Skill 的元数据与执行端点；
2. **引用能力**：在 Agent 的 `tools` 列表中添加 `{"type": "store", "store_id": "..."}` 条目；
3. **运行时调用**：Agent 执行过程中自动解析 `store_id`，从 store 拉取最新元数据并发起安全代理调用。完整流程参见 [Store](../../raw/application-user-guide/agent-store.md)。

## 限制和注意事项

- 单次 Agent 调用最多可声明 10 个不同的 `store_id`；
- Store 不支持跨租户共享能力，所有注册项默认作用域为当前 workspace；
- MCP 实现必须符合 v1.2+ 协议规范，旧版协议（如 v1.0）可能因字段缺失导致调用失败；
- Skill 的执行环境隔离依赖平台沙箱机制，不支持访问本地文件系统或发起未声明的网络请求。

## 来源文档

- [Store](../../raw/application-user-guide/agent-store.md)


