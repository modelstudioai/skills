# overview

百炼 MCP（Model Calling Protocol）API 提供统一接口管理、调用和集成外部能力服务（即 Skill / MCP 服务）。开发者可通过该 API 创建、配置、启停自定义 MCP，开通/关闭官方 MCP，并查询、推荐及调用其提供的工具。所有操作均基于工作空间隔离，通过标准 RESTful 接口与统一错误响应结构实现。

## 支持的模型/功能

- **MCP 服务类型**：支持 `STDIO`（函数计算部署）、`HTTP`、`SSE` 和 `OPENAPI` 四类自定义 MCP；官方 MCP 由平台预置，按需开通。
- **核心功能**：
  - 管理生命周期：开通/关闭官方 MCP（[开通 MCP](raw/application-api-reference/overview/overview/activate.md)、[关闭官方 MCP](raw/application-api-reference/overview/overview/deactivate.md)），停用/启用自定义 MCP（[停用自定义 MCP](raw/application-api-reference/overview/overview/disable.md)、[启用自定义 MCP](raw/application-api-reference/overview/overview/enable.md)）。
  - 查询与发现：获取 MCP 详情（[查询 MCP 详情](raw/application-api-reference/overview/overview/get.md)）、列出工具（[查询工具列表](raw/application-api-reference/overview/overview/list.md)）、自然语言推荐工具（[推荐工具](raw/application-api-reference/overview/overview/recommend.md)）。
  - 调用执行：同步调用指定工具（[调用工具](raw/application-api-reference/overview/overview/call.md)）。
- **One Key MCP 支持**：部分官方 MCP 支持“一键开通”，首次查询或调用时自动完成开通流程，无需预先调用 activate 接口。

## 关键参数

- `mcpCode`：全局唯一 MCP 编码，用于所有资源路径（如 `/servers/{mcpCode}`），区分官方与自定义服务。
- `server_name` / `description`：创建或更新自定义 MCP 时必填的元信息字段。
- `mcp_type` + `mcp_config`：决定 MCP 类型及运行时配置：
  - `HTTP`/`SSE`：需提供 `url`（公网 HTTPS 地址）和可选 `headers`；
  - `OPENAPI`：需提供 `api_host`、`api_list`（含 `name`、`path`、`method`、`input_params` 等完整 OpenAPI 描述）；
  - `STDIO`：需提供 `command`（`npx` 或 `uvx`）、`args` 及可选 `env` 和 `fc_deploy_region`。
- `tool_name` 与 `tool_params`：调用工具时必需，`tool_name` 必须严格匹配 [查询工具列表](raw/application-api-reference/overview/overview/list.md) 返回的名称。

> **注意**：文档中多处提及 `fc_deploy_region` 需“使用控制台支持的地域”，但未明确列出有效值；实际使用时请以[百炼控制台地域列表](https://help.aliyun.com/zh/model-studio/product-overview/regions)为准，避免因地域不匹配导致 `400 InvalidParameter` 错误。

## 使用方式

1. **认证**：使用百炼 API Key，通过 `Authorization: Bearer <API_KEY>` Header 传递；Endpoint 格式为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/mcp/...`，其中 `workspace_id` 从控制台右上角复制。
2. **创建自定义 MCP**：`POST /api/v1/mcp/servers`，传入完整配置；成功返回 `201`，状态为 `ACTIVATED` 或 `ACTIVATE_FAILED`（见 [创建自定义 MCP](raw/application-api-reference/overview/overview/create.md)）。
3. **调用工具**：`POST /api/v1/mcp/servers/{mcpCode}/tools/call`，请求体必须包含 `tool_name` 字段，即使无参数也需提交空对象 `{}`。
4. **错误处理**：统一响应结构含 `success`、`error_code`、`error_msg` 和 `request_id`；需同时检查 HTTP 状态码与 `data.isError` 字段（例如工具执行失败可能返回 `200` + `{"isError": true}`）。

## 限制和注意事项

- **权限与安全**：API Key 具有工作空间级权限，严禁硬编码或泄露；`mcp_config.headers` 可能包含敏感凭据（如 API Key），响应内容需妥善保护。
- **服务状态约束**：
  - 修改自定义 MCP 配置前必须先停用（`disable`），否则返回 `400 OperationNotSupported`；
  - 官方 MCP 不支持 `disable`/`enable`，仅支持 `activate`/`deactivate`；One Key MCP 不支持 `deactivate`。
- **删除与不可逆操作**：`DELETE /api/v1/mcp/servers/{mcpCode}` 仅适用于自定义 MCP，删除后不可恢复。
- **版本与 ZIP 下载**：`/api/v1/skills/{skill_id}/versions/{version}/content` 接口属于 Skill（非 MCP）体系，与本文档主题 MCP 无直接关联，开发者应确认使用场景是否匹配。

> **注意**：文档 12（下载版本 ZIP）所属路径 `raw/application-api-reference/overview/overview/download.md` 明确指向 `skills` 资源，而其余 28 篇文档均围绕 `mcp/servers` 展开。该接口与 MCP 功能无技术耦合，属不同能力域，使用时需注意上下文隔离。

## 来源文档

- [Skill API 认证](../../raw/application-api-reference/overview/authentication.md)
- [Skill API 错误码](../../raw/application-api-reference/overview/errors.md)
- [获取 Skill](../../raw/application-api-reference/overview/overview/get.md)
- [Skill 管理](../../raw/application-api-reference/overview/overview.md)
- [创建 Skill](../../raw/application-api-reference/overview/overview/create.md)
- [删除 Skill](../../raw/application-api-reference/overview/overview/delete.md)
- [列出 Skill](../../raw/application-api-reference/overview/overview/list.md)
- [版本管理](../../raw/application-api-reference/overview/overview.md)
- [列出版本](../../raw/application-api-reference/overview/overview/list.md)
- [创建版本](../../raw/application-api-reference/overview/overview/create.md)
- [获取版本详情](../../raw/application-api-reference/overview/overview/get.md)
- [下载版本 ZIP](../../raw/application-api-reference/overview/overview/download.md)
- [MCP API 错误码](../../raw/application-api-reference/overview/errors.md)
- [认证](../../raw/application-api-reference/overview/authentication.md)
- [服务管理](../../raw/application-api-reference/overview/overview.md)
- [查询 MCP 列表](../../raw/application-api-reference/overview/overview/list.md)
- [创建自定义 MCP](../../raw/application-api-reference/overview/overview/create.md)
- [更新自定义 MCP](../../raw/application-api-reference/overview/overview/update.md)
- [查询 MCP 详情](../../raw/application-api-reference/overview/overview/get.md)
- [工具](../../raw/application-api-reference/overview/overview.md)
- [删除自定义 MCP](../../raw/application-api-reference/overview/overview/delete.md)
- [查询工具列表](../../raw/application-api-reference/overview/overview/list.md)
- [推荐工具](../../raw/application-api-reference/overview/overview/recommend.md)
- [调用工具](../../raw/application-api-reference/overview/overview/call.md)
- [生命周期](../../raw/application-api-reference/overview/overview.md)
- [开通官方 MCP](../../raw/application-api-reference/overview/overview/activate.md)
- [停用自定义 MCP](../../raw/application-api-reference/overview/overview/disable.md)
- [关闭官方 MCP](../../raw/application-api-reference/overview/overview/deactivate.md)
- [启用自定义 MCP](../../raw/application-api-reference/overview/overview/enable.md)


