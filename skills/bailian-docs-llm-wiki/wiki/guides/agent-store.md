# agent store

agent store 是百炼平台提供的模型能力与工具注册中心，用于统一管理、发现和调用外部模型、协议（如 MCP）及技能（Skill）。它为 Agent 提供标准化的插件接入机制，支持运行时动态加载与组合。开发者可通过配置声明式地绑定能力，无需硬编码集成。

## 支持的模型/功能

agent store 当前支持两类核心能力注册：
- **MCP（Model Context Protocol）服务**：提供标准化上下文交互协议，支持跨模型上下文传递与结构化工具调用，详见 [Store](../../raw/application-user-guide/agent-store.md)；
- **Skill（技能）**：封装可复用的业务逻辑单元（如查天气、发邮件），支持参数校验、权限控制与版本管理，同样在 [Store](../../raw/application-user-guide/agent-store.md) 中定义其元数据规范。

> **注意**：原始文档未明确列出支持的模型类型（如 Qwen 系列或第三方 LLM），仅聚焦于能力抽象层；实际可用模型需参考 [Model Registry](../../raw/model-registry/index.md)，该文档与 [Store](../../raw/application-user-guide/agent-store.md) 的能力边界存在隐含耦合，建议以 Model Registry 为准。

## 关键参数

注册或调用 store 中能力时，需配置以下关键字段：
- `id`：全局唯一标识符，命名需符合 `[a-z0-9\-]{3,64}` 正则；
- `type`：取值为 `"mcp"` 或 `"skill"`，决定解析器与执行链路；
- `endpoint`：HTTP 地址（MCP）或函数路径（Skill），必须可被平台内网访问；
- `schema`：OpenAPI 3.0 或 JSON Schema 格式，用于参数校验与 UI 自动生成。

## 使用方式

1. **注册能力**：通过控制台「Agent Store」页或 OpenAPI `/v1/agent-store/register` 提交 YAML/JSON 描述文件；
2. **在 Agent 中引用**：在 `agent.yaml` 的 `tools` 字段中声明 `store://<id>` 协议 URI；
3. **调试调用**：使用 `bailian-cli tool invoke --store-id <id>` 进行本地验证。

完整流程与示例见 [Store](../../raw/application-user-guide/agent-store.md)。

## 限制和注意事项

- 单个 store 实例最多注册 200 个能力，超出需联系平台管理员扩容；
- MCP 服务响应超时默认为 5s，不可覆盖；Skill 执行超时为 30s，可在注册时通过 `timeout_ms` 覆盖（最小 1000ms）；
- 所有 store 能力均运行于沙箱环境，禁止访问外网（除非显式申请白名单）；
- 修改已注册能力的 `schema` 可能导致存量 Agent 调用失败，建议遵循语义化版本升级并同步更新引用方。

## 来源文档

- [Store](../../raw/application-user-guide/agent-store.md)


