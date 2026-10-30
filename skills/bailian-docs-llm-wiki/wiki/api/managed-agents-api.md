# managed agents api

Managed Agents API 是百炼平台提供的用于构建、部署和管理可编程智能体（Agent）的 RESTful 接口集合，支持环境隔离、会话状态管理、技能编排、文件与记忆存储等核心能力。该 API 采用标准 HTTP 协议，需通过 Bearer [Token](../concepts/token.md) 认证，适用于需要细粒度控制 Agent 生命周期与运行时行为的开发者场景。完整功能覆盖从开发调试到生产部署的全链路需求。

## 支持的模型与功能

Managed Agents API **不直接绑定特定大模型**，而是通过 `agent` 资源中的 `model_id` 字段指定所用模型（如 `qwen-max`、`qwen-plus` 等），模型能力由底层 Model API 提供。核心功能模块包括：  
- Agent 定义与版本管理（含 prompt、tools、memory 配置）  
- Environment 隔离运行时上下文（如 sandbox、prod）  
- Session 与 Event 驱动的交互流控制（支持 streaming 响应）  
- File 上传/引用、Memory Store 键值持久化、Skill 复用封装  
- Vault 与 Credential 安全凭证管理，以及 Deployment 灰度发布能力  

详细接口说明请参阅 [Managed Agent API](../../raw/application-api-reference/managed-agents-api.md) 的子章节结构。

## 关键参数

所有 POST/PUT 请求需在 `Content-Type: application/json` 下提交以下必需字段（部分接口有额外要求）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | string | 是 | Agent 或资源唯一标识符（仅限字母、数字、下划线、短横线，长度 1–64） |
| `model_id` | string | 是 | 所用模型 ID，必须已在当前项目中启用；不支持自定义模型别名 |
| `environment_id` | string | 否（默认 `default`） | 指定运行环境，需提前通过 [Environment API](../../raw/application-api-reference/managed-agents-api/environment-api.md) 创建 |
| `stream` | boolean | 否（默认 `false`） | 设为 `true` 时返回 SSE 流式响应，仅适用于 `/v1/agents/{id}/chat` 等会话接口 |

> **注意**：`model_id` 的合法取值范围以 [Model API 文档](../../raw/model-api-reference/model-list.md) 为准；若文档中未列出某模型但 API 返回 400 错误，应优先参考该文档而非本页示例。

## 使用方式

1. **认证**：在请求头中携带 `Authorization: Bearer <access_token>`，[Token](../concepts/token.md) 通过 [认证文档](../../raw/application-api-reference/managed-agents-api/managed-agents-api-authentication.md) 中描述的 OAuth2 流程获取；  
2. **创建 Agent**：`POST /v1/agents`，传入基础配置（含 `model_id`、`prompt`、`skills` 列表）；  
3. **启动会话**：`POST /v1/agents/{agent_id}/sessions` 获取 `session_id`，再调用 `/v1/agents/{agent_id}/chat` 发送消息；  
4. **调试建议**：首次集成推荐从 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md) 文档的 cURL 示例入手，验证基础链路。

## 限制和注意事项

- 单次 `chat` 请求最大输入 tokens 为 32768（受模型本身限制约束）；  
- Memory Store 单个 key 最大 1MB，总容量按项目配额计费；  
- Webhook 回调 URL 必须为 HTTPS，且需在 5 秒内返回 2xx 响应，否则视为失败并触发重试（最多 3 次）；  
- Agent 部署后不可修改 `model_id`，如需切换模型，须新建 Agent 并重新部署；  
- 文件上传接口（`/v1/files`）暂不支持分片上传，单文件上限 100MB。  

如遇非预期错误，请对照 [错误码文档](../../raw/application-api-reference/managed-agents-api/managed-agents-api-errors.md) 进行定位。

## 来源文档

- [Managed Agent API](../../raw/application-api-reference/managed-agents-api.md)


