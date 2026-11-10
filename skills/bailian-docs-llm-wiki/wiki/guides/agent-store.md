# agent store

agent store 是百炼平台提供的 Agent 能力分发与复用中心，支持开发者发布、发现和集成标准化的模型能力（如 MCP）与功能模块（如 Skill）。它通过统一接口降低 Agent 开发门槛，提升能力复用效率。所有上架内容均需符合平台定义的协议规范与安全要求。

## 支持的模型/功能

- **MCP（Model Context Protocol）**：用于封装模型上下文交互逻辑的标准协议，支持动态上下文注入与多轮状态管理。详细协议定义见 [MCP](../../raw/application-user-guide/agent-store/model-context-protocol.md)。
- **Skill（技能模块）**：可独立调用的功能单元，如天气查询、数据库查询、PDF 解析等，具备明确输入/输出 Schema 和权限声明。具体实现约束参见 [Skill](../../raw/application-user-guide/agent-store/skill.md)。

## 关键参数

- `store_id`：全局唯一标识符，由平台分配，不可自定义；
- `version`：语义化版本号（如 `1.2.0`），每次更新必须递增，不支持 `latest` 等模糊版本；
- `visibility`：取值为 `public` 或 `private`，`public` 表示对同租户内所有项目可见，**不支持跨租户共享**；
- `schema`：JSON Schema 格式描述输入/输出结构，必须与实际调用行为严格一致。

## 使用方式

1. 通过 `POST /v1/agent-store/publish` 提交符合协议的包（含 `manifest.yaml` + 代码/配置）；
2. 审核通过后获得 `store_id`，可在 Agent 编排中通过 `use: <store_id>@<version>` 引用；
3. 运行时自动拉取并沙箱化执行，无需手动部署依赖。  
完整发布流程与 manifest 示例详见 [Store](../../raw/application-user-guide/agent-store.md)。

## 限制和注意事项

- 单个 Skill 最大运行时长为 30 秒，超时将被强制终止；
- MCP 实例默认共享同一会话上下文，若需隔离，须显式设置 `session_isolation: true`；
- > **注意**：原始文档中提及“支持 HTTP 回调作为 Skill 入口”，但当前平台仅支持 gRPC 或内置 runtime 执行方式，HTTP 回调已下线，该描述已在 [Skill](../../raw/application-user-guide/agent-store/skill.md) 中过时，请以控制台提示为准；
- 所有 store 内容默认启用静态代码扫描，禁止包含 `eval()`、`exec()` 及未签名的二进制加载逻辑。

## 来源文档

- [Store](../../raw/application-user-guide/agent-store.md)


