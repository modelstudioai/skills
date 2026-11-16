# agent store

agent store 是百炼平台提供的模型能力与技能的集中注册、发现与调用服务，用于在 Agent 应用中动态加载和组合外部模型能力（如 MCP）或预置技能（Skill）。它通过标准化接口实现能力解耦，支持运行时按需拉取与执行。开发者无需硬编码集成逻辑，即可复用平台托管的能力模块。

## 支持的模型/功能

agent store 当前主要支持两类可注册能力：
- **MCP（Model Context Protocol）**：提供结构化上下文交互协议，支持模型间上下文传递与协同推理，详见 [MCP](../../raw/application-user-guide/agent-store/model-context-protocol.md)；
- **Skill（技能）**：封装了特定业务逻辑（如查天气、发邮件）的可复用函数单元，具备明确输入/输出 Schema 和权限声明，详见 [Skill](../../raw/application-user-guide/agent-store/skill.md)。

> **注意**：文档 [Store](../../raw/application-user-guide/agent-store.md) 中未明确说明是否支持自定义 LLM 模型直接注册为 store 条目；根据当前实现，仅 MCP 和 Skill 为官方支持类型，LLM 模型需通过 `model_id` 显式指定，不纳入 store 管理范畴。

## 关键参数

调用 store 中的能力时，需在 `agent_config` 或 `tool_calls` 中指定以下关键字段：
- `store_id`: 唯一标识符，由平台分配，格式为 `mcp/{uuid}` 或 `skill/{uuid}`；
- `version`: 语义化版本号（如 `v1.2.0`），用于灰度发布与兼容性控制；
- `input_schema`: JSON Schema 定义的输入约束，必须与注册时一致，否则调用失败；
- `auth_required`: 布尔值，指示是否需用户授权（仅 Skill 类型强制校验）。

## 使用方式

1. **注册能力**：通过控制台或 OpenAPI（`POST /v1/store/items`）提交 MCP 或 Skill 的元数据与执行逻辑；
2. **发现能力**：调用 `GET /v1/store/search` 并传入关键词、标签或 `type=mcp|skill` 过滤；
3. **调用能力**：在 Agent 的 `tool_choice` 或 `function_call` 中引用 `store_id`，平台自动解析并路由至对应实现。完整流程参见 [Store](../../raw/application-user-guide/agent-store.md)。

## 限制和注意事项

- 单次请求最多并发调用 5 个 store 能力，超出将触发限流（HTTP 429）；
- MCP 能力不支持嵌套调用自身 store ID，否则引发循环依赖错误；
- Skill 的 `input_schema` 变更需同步更新所有下游 Agent 配置，否则运行时报 `validation_error`；
- 所有 store 能力默认启用沙箱执行环境，但 Skill 若声明 `privileged: true`，需经平台安全审核后方可上线——该要求在 [Skill](../../raw/application-user-guide/agent-store/skill.md) 中明确，在 [MCP](../../raw/application-user-guide/agent-store/model-context-protocol.md) 中未提及，建议 Skill 场景严格遵循。

## 来源文档

- [Store](../../raw/application-user-guide/agent-store.md)


