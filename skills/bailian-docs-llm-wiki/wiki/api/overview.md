# overview

MCP API 是百炼平台用于统一管理 MCP（Model Calling Protocol）服务的核心接口，支持对官方及自定义 MCP 的全生命周期操作（查询、创建、启停、开通、删除）以及工具级能力（列表、调用、推荐）。该 API 面向开发者提供标准化的 RESTful 接口，所有请求均需通过工作空间 ID 和 API Key 认证。响应结构统一，便于错误诊断与自动化集成。

## 支持的模型/功能

- **服务类型**：支持 `STDIO`（函数计算部署）、`HTTP`（流式 HTTP 服务）、`SSE`（Server-Sent Events）、`OPENAPI`（已有 HTTP API 封装）四类 MCP 服务。
- **服务归属**：区分 `OFFICIAL`（阿里云官方提供）与 `CUSTOMER`（用户自定义）两类，元信息（如 `icon`、`provider`、`is_onekey`）仅对官方 MCP 返回，详见 [MCP API 概览](../../raw/application-api-reference/overview.md)。
- **核心能力**：包括 MCP 列表/详情/创建/更新/删除、工具列表查询、工具调用、工具推荐、官方 MCP 开通/关闭、自定义 MCP 启用/停用等。完整接口清单见 [MCP API 概览](../../raw/application-api-reference/overview.md) 中的「接口列表」章节。

## 关键参数

- **Endpoint**：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/mcp/servers`，其中 `workspace_id` 为必填路径前缀，需从[百炼控制台](https://bailian.console.aliyun.com/)右上角工作空间菜单中复制。
- **认证**：必须配置 API Key，参见 [认证](../../raw/application-api-reference/overview/authentication.md) 文档。
- **分页与筛选**：统一使用 `pageNo` / `pageSize` 分页，工具推荐使用 `topN` 参数。
- **命名规范**：请求体与响应字段采用 `snake_case`；工具调用结果例外，保留 MCP 协议字段 `inputSchema`、`additionalProperties` 及 `isError` 字段。
- **敏感字段注意**：`mcp_config` 中的 `headers` 等配置按原值返回，可能含密钥等敏感信息，仅限可信环境调用 —— 此限制在 [Skill API 概览](../../raw/application-api-reference/overview.md) 和 [MCP API 概览](../../raw/application-api-reference/overview.md) 中均明确强调。

> **注意**：两份原始文档内容完全一致（文件名与标题略有差异，但路径 `raw/application-api-reference/overview.md` 实际指向同一份内容），不存在实质矛盾。但需注意文档 1 标题为“Skill API 概览”，而正文及所有链接均使用“MCP API”，属命名不一致问题；实际 API 名称应以正文中反复出现的 **MCP API** 为准，开发者应忽略标题中的“Skill API”表述，避免混淆。

## 使用方式

1. 前置准备：开通百炼服务，[创建 API Key](../../raw/model-api-reference/preparations/get-api-key.md)，获取 `workspace_id`；
2. 构造请求：按接口文档指定方法（GET/POST/DELETE）、路径（如 `/list`、`/{mcpCode}/activate`）和请求体（如创建时的 `mcp_config`）发起调用；
3. 解析响应：所有接口统一返回包含 `success`、`error_code`、`data`、`request_id` 的 JSON 结构；工具调用结果需额外检查 `data.isError` 字段判断执行是否成功；
4. 错误处理：参考 [MCP API 错误码](../../raw/application-api-reference/overview/errors.md) 进行重试或告警。

## 限制和注意事项

- 官方 MCP 不可修改 `mcp_config`，仅支持开通/关闭；自定义 MCP 支持创建、更新、启用/停用、删除全流程管理。
- `server_status` 枚举值含义因 `type` 而异（如 `INACTIVE` 对官方 MCP 表示“未开通”，对自定义 MCP 表示“未启用”），调用方需结合 `type` 字段解析状态文案。
- `meta_info` 中的监控指标（如 `call_success_rate`、`average_call_time`）为近实时聚合数据，非强一致性，不适用于精确 SLA 计算。
- 所有接口均受百炼平台配额与速率限制约束，超限将返回 `429 Too Many Requests`，具体策略请查阅平台级限流文档。

## 来源文档

- [Skill API 概览](../../raw/application-api-reference/overview.md)
- [MCP API 概览](../../raw/application-api-reference/overview.md)


