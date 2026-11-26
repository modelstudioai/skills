# [overview](overview.md) 1e06e5e20b81f10d

MCP API 是百炼平台提供的服务管理接口，用于统一管控官方 MCP 和自定义 MCP 的全生命周期（查询、创建、启停、开通、删除）及工具能力（列表、调用、推荐）。该 API 面向开发者设计，需配合工作空间 ID 和 API Key 使用，所有请求均通过工作空间专属 endpoint 发起。详细错误处理机制和认证要求请参见 [MCP API 概览](../../raw/application-api-reference/overview-1e06e5e20b81f10d.md)。

## 支持的模型/功能

- **MCP 类型支持**：官方 MCP（`type=OFFICIAL`）与自定义 MCP（`type=CUSTOMER`），二者在元信息字段（如 `icon`、`provider`）、状态文案及管理方式上存在差异。
- **服务类型支持**：`STDIO`（FC 函数部署）、`HTTP`（远程流式服务）、`SSE`（远程事件流）、`OPENAPI`（HTTP API 封装为 MCP）。
- **核心功能**：
  - 全生命周期管理：创建、更新、启用/停用（自定义）、开通/关闭（官方）、删除；
  - 工具能力：获取工具列表、调用指定工具（含 `isError` 判断执行结果）、按自然语言推荐工具；
  - 元数据聚合：提供调用量、成功率、平均耗时等可观测指标（仅 `meta_info` 中返回）。

> **注意**：[MCP API 概览](../../raw/application-api-reference/overview-1e06e5e20b81f10d.md) 明确指出 `meta_info` 中 `icon`、`provider`、`is_onekey` 仅适用于官方 MCP；而部分旧版文档未强调此限制，实际调用自定义 MCP 的 `DetailResponse` 时这些字段恒为 `null`，请勿依赖。

## 关键参数

- **路径参数**：`mcpCode`（MCP 唯一编码），用于详情、更新、删除、工具操作等接口。
- **分页参数**：`pageNo`（页码，从 1 开始）、`pageSize`（每页条数），用于 `/list` 等列表接口。
- **推荐参数**：`topN`（推荐工具数量），用于 `/tools/recommend`。
- **请求体字段**：全部使用 `snake_case`（如 `server_name`, `mcp_config`），但工具调用结果中保留 MCP 协议字段名 `inputSchema`、`additionalProperties` 及 `isError`。
- **响应头**：必含 `x-request-id`，用于问题排查。

## 使用方式

1. **前置准备**：
   - 开通百炼服务并[创建 API Key](../model-api-reference/preparations/get-api-key.md)；
   - 登录[百炼控制台](https://bailian.console.aliyun.com/)获取工作空间 ID；
   - 配置认证（详见 [MCP API 概览](../../raw/application-api-reference/overview-1e06e5e20b81f10d.md) 中的“认证”说明）。

2. **Endpoint 构造**：
   ```text
   https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/mcp/servers
   ```
   所有接口均基于此 base URL，后接具体路径（如 `/list`, `/{mcpCode}/enable`）。

3. **典型流程示例（自定义 MCP）**：
   - `POST /` 创建 → 获取 `mcp_code`；
   - `POST /{mcpCode}/enable` 启用 → 等待 `server_status=ACTIVATED`；
   - `GET /{mcpCode}/tools` 获取工具列表；
   - `POST /{mcpCode}/tools/call` 调用工具。

## 限制和注意事项

- **敏感信息风险**：`mcp_config`（尤其 `headers` 字段）可能包含密钥等敏感配置，响应体中会原样返回。请确保调用环境可信，并禁止日志记录或前端透出该字段 —— 此约束在 [MCP API 概览](../../raw/application-api-reference/overview-1e06e5e20b81f10d.md) 的“警告”区块中已明确强调。
- **状态一致性**：`success: true` 仅表示 HTTP 请求成功，**不保证业务操作完成**；需结合 `data.isError`（工具调用）或 `server_status`（服务状态）判断最终结果。
- **枚举值兼容性**：`server_status_text` 为中文文案，其值随 `type`（`OFFICIAL`/`CUSTOMER`）变化（如 `INACTIVE` 对应“未开通”或“未启用”），客户端应依据 `type` + `server_status` 组合解析，而非硬编码文案。
- **错误处理**：统一响应结构含 `error_code`/`error_msg`，具体含义需查阅 [MCP API 错误码](overview/errors-972b4127b84f4429.md)，该文档与 [MCP API 概览](../../raw/application-api-reference/overview-1e06e5e20b81f10d.md) 保持同步。

## 来源文档

- [MCP API 概览](../../raw/application-api-reference/overview-1e06e5e20b81f10d.md)


