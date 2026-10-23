# agent store

agent store 是百炼平台提供的模型能力与技能的集中注册、发现与调用服务，用于在 Agent 应用中动态加载和组合外部模型能力（如 MCP）或预置技能（Skill）。它通过标准化接口实现能力解耦，支持运行时按需拉取与执行。开发者无需硬编码集成逻辑，即可复用平台托管的能力模块。

## 支持的模型/功能

agent store 当前主要支持两类可注册能力：
- **MCP（Model Context Protocol）**：提供结构化上下文交互协议，支持模型间上下文传递与协同推理，详见 [MCP](../../raw/application-user-guide/agent-store/model-context-protocol.md)；
- **Skill（技能）**：封装了特定业务逻辑（如查天气、发邮件）的可复用函数单元，具备明确输入/输出 Schema 和权限声明，详见 [Skill](../../raw/application-user-guide/agent-store/skill.md)。

> **注意**：文档 [Store](../../raw/application-user-guide/agent-store.md) 中未明确说明是否支持自定义 LLM 模型直接注册为 store 条目；根据当前实现，仅 MCP 和 Skill 为官方支持类型，LLM 模型需通过 `model_id` 显式指定，不纳入 store 管理范畴。

## 关键参数

调用 store 中的能力时，需在 `agent_config` 或 `tool_calls` 中指定以下关键字段：
- `store_id`: 唯一标识符，由平台分配，格式为 `mcp/<id>` 或 `skill/<id>`；
- `version`: 语义化版本号（如 `v1.2.0`），用于灰度发布与兼容性控制；
- `parameters`: 运行时传入的 JSON 对象，须严格匹配该能力在 [Skill](../../raw/application-user-guide/agent-store/skill.md) 或 [MCP](../../raw/application-user-guide/agent-store/model-context-protocol.md) 中定义的 Schema。

## 使用方式

1. 在应用配置中启用 `enable_store: true`；
2. 通过 `tools` 字段声明所需能力，例如：
   ```yaml
   tools:
     - type: "store"
       store_id: "skill/weather_v2"
       version: "v1.0.0"
   ```
3. 在 LLM 的 function calling 输出中返回对应 `store_id` 及参数，平台自动解析并执行。

## 限制和注意事项

- 单次请求最多可声明 10 个 store 能力，超出将被截断并报错 `TOO_MANY_STORE_TOOLS`；
- store 能力不可嵌套调用（即一个 Skill 内部不能触发另一个 store_id）；
- 所有 store 调用均受租户配额与速率限制约束，具体阈值请参考 [Store](../../raw/application-user-guide/agent-store.md) 中的“配额说明”章节；
- `version` 字段为必填项，空值或 `latest` 将导致调用失败——平台不支持自动解析 latest 别名。

## 来源文档

- [Store](../../raw/application-user-guide/agent-store.md)


