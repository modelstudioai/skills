# [overview](overview.md) 1e06e5e20b81f10d

MCP API 是百炼平台提供的服务管理接口，用于统一管控官方 MCP 和自定义 MCP 的全生命周期（查询、创建、启停、开通、删除）及工具能力（列表、调用、推荐）。该 API 面向开发者设计，需配合工作空间 ID 和 API Key 使用，所有请求均通过 RESTful 方式交互。详细行为规范与错误处理机制请参阅 [MCP API 概览](../../raw/application-api-reference/overview-1e06e5e20b81f10d.md)。

## 支持的模型/功能

- **服务类型支持**：`STDIO`（函数计算部署）、`HTTP`（远程 Streamable）、`SSE`（远程事件流）、`OPENAPI`（HTTP API 封装为 MCP）。
- **MCP 类型支持**：`OFFICIAL`（平台预置，如天气、翻译等 One Key MCP）和 `CUSTOMER`（用户自主开发并部署的 MCP）。
- **核心功能**：
  - 全生命周期管理（创建/更新/启用/停用/删除/开通/关闭）；
  - 工具发现与执行（`/tools` 列表、`/tools/call` 调用、`/tools/recommend` 推荐）；
  - 状态监控（含 `activate_user_count`、`call_success_rate` 等运行指标）。

> **注意**：`OPENAPI` 类型仅适用于将已有 HTTP 接口转换为 MCP 协议的服务，其工具 schema 必须严格遵循 [MCP 协议规范](../../raw/application-api-reference/overview-1e06e5e20b81f10d.md)，而非 OpenAPI Specification v3 格式；相关字段命名（如 `inputSchema`）在响应中保持原协议约定，不转为 snake_case。

## 关键参数

- **路径参数**：`mcpCode`（MCP 唯一编码），用于详情、启停、调用等单资源操作。
- **分页参数**：`pageNo`（从 1 开始）、`pageSize`（默认 20，最大 100）。
- **推荐参数**：`topN`（推荐工具数量，默认 5，最大 10）。
- **认证参数**：`Authorization: Bearer <api_key>`，需提前在[百炼控制台](https://bailian.console.aliyun.com/)创建 API Key —— 具体流程见 [MCP API 概览](../../raw/application-api-reference/overview-1e06e5e20b81f10d.md) 中的“前提条件”章节。
- **敏感字段**：`mcp_config.headers` 等配置项可能包含密钥或 [Token](../concepts/token.md)，响应中直接透出，**禁止日志记录或前端展示**。

## 使用方式

1. 构造 Endpoint：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/mcp/servers`，其中 `workspace_id` 从控制台右上角工作空间菜单复制获取；
2. 设置请求头：`Content-Type: application/json` 和 `Authorization: Bearer <your_api_key>`；
3. 根据目标操作选择对应接口（如 `GET /list` 查询全部 MCP，`POST /{mcpCode}/enable` 启用自定义服务）；
4. 解析标准响应结构：检查 `success` 字段判断请求是否被平台接收，再结合 `data.isError`（[工具调用](../concepts/tool-calling.md)场景）或 `server_status`（服务状态变更）确认业务结果。

所有接口的请求体与响应主体字段均采用 `snake_case` 命名（[工具调用](../concepts/tool-calling.md)结果除外），详见 [MCP API 概览](../../raw/application-api-reference/overview-1e06e5e20b81f10d.md) 中的“请求命名”小节。

## 限制和注意事项

- **配额限制**：单 workspace 默认限流 10 QPS，超出返回 `429 Too Many Requests`；高并发场景需提工单申请提升。
- **状态最终一致性**：`ACTIVATING`/`ACTIVATE_FAILED` 等中间态可能持续数秒，客户端应轮询 `GET /{mcpCode}` 直至 `server_status` 变为 `ACTIVATED` 或 `ACTIVATE_FAILED`。
- **自定义 MCP 配置安全**：`mcp_config` 在 `DetailResponse` 中完整返回（含 `headers`、`auth` 等），调用方必须确保传输与存储环境可信，避免泄露。
- **官方 MCP 不可修改配置**：`mcp_config` 对 `OFFICIAL` 类型恒为 `null`，且 `update`、`enable`、`disable` 等接口仅对 `CUSTOMER` 类型生效。
- **错误处理**：统一使用 `error_code`/`error_msg` 字段标识业务错误，`request_id` 用于问题定位，完整错误码列表见 [MCP API 错误码](../../raw/application-api-reference/overview-1e06e5e20b81f10d.md)。

## 来源文档

- [MCP API 概览](../../raw/application-api-reference/overview-1e06e5e20b81f10d.md)


