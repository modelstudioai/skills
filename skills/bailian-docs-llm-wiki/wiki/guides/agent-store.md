# agent store

agent store 是百炼平台提供的模型能力分发与复用中心，用于统一管理、发布和调用经过封装的 Agent 能力（如 Skill）及上下文协议（如 MCP）。它支持开发者将自定义能力注册为可发现、可组合的标准组件，并在应用中按需集成。该机制依赖于 [Store (raw/application-user-guide/agent-store.md)](../../raw/application-user-guide/agent-store.md) 定义的基础架构。

## 支持的模型/功能

- **Skill**：封装了特定业务逻辑（如查天气、订会议室）的可复用原子能力，支持参数校验、异步执行与错误重试；详情见 [Skill](../../raw/application-user-guide/agent-store/skill.md)。  
- **MCP（Model Context Protocol）**：定义模型与外部系统交互的标准化上下文协议，包括输入 schema、输出解析规则及上下文生命周期管理；详见 [MCP](../../raw/application-user-guide/agent-store/model-context-protocol.md)。  
- 不支持直接托管 LLM 基座模型或微调检查点——仅承载能力封装层（即 Skill/MCP 实例），底层模型需通过 `model_id` 显式引用。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `skill_id` 或 `mcp_id` | string | 是 | 在 store 中注册的唯一标识符，命名需符合 `[a-z0-9\-]{3,64}` 正则 |
| `version` | string | 否 | 语义化版本（如 `v1.2.0`），未指定时默认使用 `latest` 别名 |
| `input_schema` | object | 是（Skill）/ 否（MCP） | JSON Schema 格式，用于运行时参数校验与 IDE 提示 |
| `auth_config` | object | 否 | 指定调用所需的认证方式（如 `api_key_header`, `oauth2`），若为空则视为无认证 |

> **注意**：原始文档中 `Store (raw/application-user-guide/agent-store.md)` 提到 `auth_config` 支持 `basic_auth` 类型，但当前 API 实际仅接受 `api_key_header` 和 `oauth2`，`basic_auth` 已废弃，请以 [Store (raw/application-user-guide/agent-store.md)](../../raw/application-user-guide/agent-store.md) 的最新接口文档为准。

## 使用方式

1. **注册能力**：通过控制台或 OpenAPI v3 `/v1/store/skills` 或 `/v1/store/mcps` 接口上传 Skill/MCP 定义（含 `input_schema` 和执行逻辑元数据）；  
2. **调用能力**：在 Agent 编排 YAML 或 API 请求中，以 `store://<skill_id>@<version>` 形式引用（例如 `store://weather-query@v1.0.0`）；  
3. **调试验证**：使用 `bailian-cli store invoke --id <skill_id> --input '{...}'` 进行端到端测试，该命令会自动解析 [Store (raw/application-user-guide/agent-store.md)](../../raw/application-user-guide/agent-store.md) 中声明的认证与路由配置。

## 限制和注意事项

- 单个 Skill/MCP 最大 payload 为 2MB（含代码、schema 及静态资源）；  
- `version` 字段不支持通配符（如 `v1.*`），必须精确匹配已发布的版本；  
- 所有 store 能力默认启用沙箱执行环境，禁止访问本地文件系统、`process.env` 或任意网络地址（仅允许白名单域名）；  
- 若 Skill 内部调用另一个 store 能力，需显式声明 `dependencies` 字段，否则运行时抛出 `PermissionDeniedError`。

## 来源文档

- [Store](../../raw/application-user-guide/agent-store.md)


