# [overview](overview.md) 1e06e5e20b81f10d

MCP API 是百炼平台用于统一管理 MCP（Model Calling Protocol）服务的核心接口，支持对官方及自定义 MCP 的全生命周期操作（查询、创建、启停、开通、删除）以及工具级能力（调用、推荐、列表获取）。该 API 面向开发者提供标准化的 RESTful 接口，所有响应遵循统一结构，并通过 `x-request-id` 支持链路追踪。详细行为与协议规范请参考 [原文标题](../../raw/application-api-reference/overview-1e06e5e20b81f10d.md)。

## 支持的模型/功能

- **服务类型覆盖**：支持四种 `server_type`：`STDIO`（函数计算部署）、`HTTP`（远程流式 HTTP）、`SSE`（远程 SSE）、`OPENAPI`（已有 HTTP API 封装）。
- **归属类型区分**：`OFFICIAL`（阿里云官方 MCP）与 `CUSTOMER`（用户自定义 MCP），二者在元信息字段（如 `icon`、`provider`、`is_onekey`）和状态文案上存在差异。
- **核心能力**：
  - 全生命周期管理：创建、更新、启用/停用（自定义）、开通/关闭（官方）、删除；
  - 工具交互：查询工具列表、调用指定工具、按自然语言推荐工具；
  - 状态与指标：实时返回 `server_status`、`call_success_rate`、`average_call_time` 等运行时指标。

> **注意**：官方 MCP 的 `DELETED` 状态未定义（文档中留空），而自定义 MCP 支持该状态；实际调用中应以 `server_status` 枚举值为准，避免依赖状态文案做逻辑判断。详见 [原文标题](../../raw/application-api-reference/overview-1e06e5e20b81f10d.md) 中的“枚举”章节。

## 关键参数

- **Endpoint 路径变量**：`{workspace_id}` 必须为真实工作空间 ID，构成完整地址 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/mcp/servers`。
- **分页与排序**：统一使用 `pageNo`（从 1 开始）和 `pageSize`；工具推荐接口使用 `topN` 指定返回数量。
- **请求/响应格式**：
  - 请求体与响应主体字段均为 `snake_case`（如 `mcp_code`, `server_name`）；
  - 工具调用结果例外：保留 MCP 协议字段名（如 `inputSchema`, `additionalProperties`），且必须检查 `data.isError` 判断执行是否成功（`success: true` 仅表示 API 调用成功）。
- **敏感字段警示**：`mcp_config.headers` 等配置字段会原样返回，可能含密钥或 Token，[原文标题](../../raw/application-api-reference/overview-1e06e5e20b81f10d.md) 明确要求仅在可信环境调用并保护响应内容。

## 使用方式

1. **前置准备**：
   - 开通百炼服务，创建 API Key（参见 [raw/model-api-reference/preparations/get-api-key.md](raw/model-api-reference/preparations/get-api-key.md)）；
   - 获取工作空间 ID（控制台右上角菜单复制）；
   - 配置认证头（Bearer Token），详见 [原文标题](../../raw/application-api-reference/overview-1e06e5e20b81f10d.md) 中“说明”部分引用的认证文档。
2. **典型流程**（自定义 MCP）：
   - `POST /` 创建 → 获取 `mcp_code`；
   - `POST /{mcpCode}/enable` 启用服务；
   - `GET /{mcpCode}/tools` 获取工具列表；
   - `POST /{mcpCode}/tools/call` 调用具体工具。
3. **错误处理**：所有接口统一返回 `error_code` 与 `error_msg`，业务错误码定义见 [MCP API 错误码](raw/application-api-reference/overview/errors-972b4127b84f4429.md)，需结合 `data.isError` 判断工具执行结果。

## 限制和注意事项

- **权限隔离**：API Key 作用域绑定工作空间，无法跨 workspace 操作。
- **状态最终一致性**：`ACTIVATING` / `ACTIVATED` 等状态变更存在延迟，轮询建议间隔 ≥1s；`ACTIVATE_FAILED` 时可通过 `activate_fail_reason` 字段定位失败原因。
- **自定义 MCP 配置安全**：`mcp_config` 中的 `headers`、`env` 等字段不脱敏，禁止在前端或日志中直接打印响应体。
- **官方 MCP 不可删除**：仅支持 `activate` / `deactivate`，无 DELETE 接口；删除操作仅适用于 `CUSTOMER` 类型。
- **响应头必含 `x-request-id`**：用于问题排查与服务端日志关联，务必在客户端记录。

## 来源文档

- [MCP API 概览](../../raw/application-api-reference/overview-1e06e5e20b81f10d.md)


