# [overview](overview.md) 1e06e5e20b81f10d

MCP API 是百炼平台用于统一管理 MCP（Model Calling Protocol）服务的核心接口，支持对官方及自定义 MCP 的全生命周期操作（查询、创建、启停、开通、删除）以及工具级能力（列表、调用、推荐）。该 API 面向开发者提供标准化的 RESTful 接口，所有请求需通过 API Key 认证，并遵循统一响应结构。详细行为与错误处理请参考 [原文标题](../../raw/application-api-reference/overview-1e06e5e20b81f10d.md)。

## 支持的模型/功能

- **服务类型覆盖**：支持 `OFFICIAL`（官方 MCP）和 `CUSTOMER`（自定义 MCP）两类归属；服务部署形态包括 `STDIO`（函数计算 FC）、`HTTP`（远程流式 HTTP）、`SSE`（远程 SSE）和 `OPENAPI`（已有 HTTP API 封装）。
- **核心能力**：
  - 全生命周期管理：创建、更新、启用/停用（自定义）、开通/关闭（官方）、删除；
  - 工具能力：查询工具列表、调用指定工具、按自然语言推荐工具；
  - 元信息聚合：提供调用量、成功率、平均耗时等可观测指标（仅 `meta_info` 中返回）。
- 所有接口定义详见 [原文标题](../../raw/application-api-reference/overview-1e06e5e20b81f10d.md) 中的「接口列表」章节。

## 关键参数

- **Endpoint 模板**：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/mcp/servers`，其中 `workspace_id` 必须从[百炼控制台](https://bailian.console.aliyun.com/)右上角工作空间菜单中获取。
- **认证**：必须配置 API Key，具体方式见 [原文标题](../../raw/application-api-reference/overview-1e06e5e20b81f10d.md) 中「前提条件」部分。
- **分页与筛选**：统一使用 `pageNo` 和 `pageSize`；工具推荐使用 `topN`；路径参数为 `mcpCode`。
- **字段命名规范**：请求体与响应主体（除工具调用结果外）均采用 `snake_case`；工具 schema 保留 MCP 协议字段（如 `inputSchema`），调用结果含 `isError` 字段判断执行状态。

## 使用方式

1. 确保已开通百炼服务，并[创建 API Key](../../raw/model-api-reference/preparations/get-api-key.md)；
2. 获取工作空间 ID，构造完整 Endpoint；
3. 按需调用对应接口（如 `GET /list` 查询全部 MCP，`POST /{mcpCode}/activate` 开通官方服务）；
4. 解析标准响应结构：检查 `success` 字段判断请求是否送达，再结合 `data.isError`（工具调用场景）或 `server_status`（服务状态场景）确认业务结果；
5. 注意 `x-request-id` 响应头，用于问题排查与日志追踪。

## 限制和注意事项

- **敏感信息风险**：`CreateResponse` 或 `DetailResponse` 中的 `mcp_config` 可能包含明文 `headers` 等敏感配置，**严禁在不可信前端或日志中直接打印或透出**。详见 [原文标题](../../raw/application-api-reference/overview-1e06e5e20b81f10d.md) 中的「警告」说明。
- **状态文案差异**：`server_status_text` 对 `OFFICIAL` 和 `CUSTOMER` 类型 MCP 返回不同文案（如 `INACTIVE` 对应“未开通” vs “未启用”），开发者应优先依据 `server_status` 枚举值做逻辑判断，而非依赖文案字符串。
- > **注意**：文档中 `meta_info` 字段说明称 `icon`、`provider`、`is_onekey` 仅适用于官方 MCP，但部分旧版 SDK 示例代码中尝试读取自定义 MCP 的 `icon` 字段并静默忽略空值——该行为已过时，当前 API 明确不返回这些字段，不应做 fallback 处理。

## 来源文档

- [MCP API 概览](../../raw/application-api-reference/overview-1e06e5e20b81f10d.md)


