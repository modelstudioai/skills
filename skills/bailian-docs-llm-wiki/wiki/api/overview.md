# overview

百炼平台的 MCP（Model Calling Protocol）与 Skill 服务提供统一的 API 接口，支持开发者通过标准化方式管理外部能力服务。MCP 用于接入和编排 HTTP/STDIO/SSE/OPENAPI 类型的服务，Skill 则用于封装可复用、可挂载到智能体的 ZIP 包功能模块。两者均基于工作空间隔离、API Key 鉴权，并共享统一的错误响应结构。

## 支持的模型/功能

- **MCP 服务**：支持四种接入类型：`STDIO`（本地进程）、`HTTP`（同步请求）、`SSE`（服务端事件流）、`OPENAPI`（OpenAPI 规范描述的工具集合）。官方 MCP（如高德地图）需开通后使用；自定义 MCP 可由用户创建、更新、停用/启用及删除。详情见 [服务管理](../../raw/application-api-reference/overview/overview-448e7f104037b903.md)。
- **Skill 服务**：以 ZIP 包形式上传，包含 `SKILL.md`（定义元信息）及运行时代码。支持多版本管理（自动递增 `major.minor` 格式），每个版本独立安全扫描与状态（`checking`/`active`/`rejected`）。Skill 可挂载至智能体，但必须指定具体版本。详情见 [版本管理](../../raw/application-api-reference/overview/overview-1dac56b965dd0271.md)。
- **工具调用能力**：所有 MCP 均暴露工具列表（`GET /{mcpCode}/tools`）和调用接口（`POST /{mcpCode}/tools/call`），支持参数校验与结构化响应。同时提供自然语言驱动的 [推荐工具](../../raw/application-api-reference/overview/overview/recommend.md) 接口，按语义匹配最适配的 MCP 工具。

## 关键参数

- **认证参数**：全局依赖 `DASHSCOPE_API_KEY`（通过 `Authorization: Bearer <key>` 传递）和工作空间 ID（用于构造 Endpoint，如 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com`）。[认证](../../raw/application-api-reference/overview/authentication-58370587ddc046ee.md) 文档明确要求 API Key 不得硬编码或泄露。
- **分页参数**：`pageNo`（从 1 开始）与 `pageSize`（1–100），二者乘积上限为 10000，适用于 MCP 列表、Skill 列表及版本列表等接口。
- **MCP 配置字段**：
  - `STDIO`：`command`（如 `npx`）、`args`（启动参数数组）、`env`（环境变量映射）；
  - `HTTP/SSE`：`url`（公网 HTTPS 地址）、`headers`（下游请求头）；
  - `OPENAPI`：`api_list`（含 `name`、`path`、`method`、`input_params` 等完整 OpenAPI 描述）。
- **Skill 上传参数**：`multipart/form-data` 中必传 `file`（ZIP，≤50MB），可选 `display_name`/`display_description` 覆盖 `SKILL.md` 内容。

## 使用方式

1. **初始化认证**：获取 API Key 并配置环境变量 `DASHSCOPE_API_KEY`，确认工作空间 ID 正确；
2. **MCP 流程**：
   - 查询可用 MCP：`GET /api/v1/mcp/servers/list?type=CUSTOMER`；
   - 创建自定义 MCP：`POST /api/v1/mcp/servers`，传入 `mcp_type` 与 `mcp_config`；
   - （可选）开通官方 MCP：`POST /api/v1/mcp/servers/{mcpCode}/activate`；
   - 调用工具：先查工具列表 `GET /{mcpCode}/tools`，再 `POST /{mcpCode}/tools/call`；
3. **Skill 流程**：
   - 创建 Skill：`POST /api/v1/skills` 上传 ZIP；
   - 上传新版本：`POST /api/v1/skills/{skill_id}/versions`；
   - 查询版本：`GET /api/v1/skills/{skill_id}/versions`；
   - 下载 ZIP：`GET /api/v1/skills/{skill_id}/versions/{version}/content` 获取临时 URL。

> **注意**：MCP 的 `tools/call` 接口在工具执行失败时可能返回 `200 success=true data.isError=true`，而 Skill 的 `create` 和 `create-version` 接口在 ZIP 解压后总大小超 100MB 时返回 `500 SKILL_PACKAGE_TOO_LARGE` —— 这与文档 21 中“ZIP 包不超过 50MB”的限制不一致，实际限制应以解压后大小为准。

## 限制和注意事项

- **权限与安全**：
  - API Key 具有工作空间级权限，严禁写入代码仓库或前端代码（见 [认证](../../raw/application-api-reference/overview/authentication-58370587ddc046ee.md) 警告）；
  - `mcp_config.headers` 可能包含敏感凭据（如 `Authorization`），查询详情时需妥善保护响应（见 [查询 MCP 详情](../../raw/application-api-reference/overview/overview/get-b57e1839b6840677.md) 警告）；
  - Skill ZIP 必须包含 `SKILL.md` 且 Front Matter 含 `name`/`description`，否则创建失败（见 [创建 Skill](../../raw/application-api-reference/overview/overview/create-44cf2cde0a7d9a72.md)）。
- **状态与生命周期**：
  - 官方 MCP 不支持关闭 One Key 类型；自定义 MCP 删除后不可恢复；
  - Skill 版本状态为 `checking` 时无法创建新版本，需等待扫描完成；
  - 列表接口（如 `/skills`）数据异步更新，状态变更后可能短暂延迟，应以单资源 `GET` 接口（如 `/skills/{id}`）结果为准（见 [列出 Skill](../../raw/application-api-reference/overview/overview/list-b23c792b7a3bf72b.md) 说明）。
- **错误处理**：
  - 统一响应含 `success`、`error_code`、`error_msg` 和 `request_id`，务必结合 HTTP 状态码与 `data.isError` 判断真实执行结果；
  - 常见错误如 `403 AccessDenied`（认证失败）、`404 McpServerNotFound`（MCP 不存在）、`500 SKILL_NOT_EXIST`（Skill 未找到）需按 [MCP API 错误码](../../raw/application-api-reference/overview/errors-972b4127b84f4429.md) 和 [Skill API 错误码](../../raw/application-api-reference/overview/errors-9f5f81ed72f2a1c6.md) 排查。

## 来源文档

- [认证](../../raw/application-api-reference/overview/authentication-58370587ddc046ee.md)
- [MCP API 错误码](../../raw/application-api-reference/overview/errors-972b4127b84f4429.md)
- [服务管理](../../raw/application-api-reference/overview/overview-448e7f104037b903.md)
- [查询 MCP 列表](../../raw/application-api-reference/overview/overview/list-c680a6eef36ba755.md)
- [创建自定义 MCP](../../raw/application-api-reference/overview/overview/create-a29c49f8a08e5095.md)
- [查询 MCP 详情](../../raw/application-api-reference/overview/overview/get-b57e1839b6840677.md)
- [更新自定义 MCP](../../raw/application-api-reference/overview/overview/update.md)
- [删除自定义 MCP](../../raw/application-api-reference/overview/overview/delete-23f946e3aa963ba8.md)
- [工具](../../raw/application-api-reference/overview/overview-743a72f61b3a54f8.md)
- [查询工具列表](../../raw/application-api-reference/overview/overview/list-64eddd50625ee03f.md)
- [调用工具](../../raw/application-api-reference/overview/overview/call.md)
- [推荐工具](../../raw/application-api-reference/overview/overview/recommend.md)
- [生命周期](../../raw/application-api-reference/overview/overview-fc1e2b9f062d93f5.md)
- [关闭官方 MCP](../../raw/application-api-reference/overview/overview/deactivate.md)
- [停用自定义 MCP](../../raw/application-api-reference/overview/overview/disable.md)
- [启用自定义 MCP](../../raw/application-api-reference/overview/overview/enable.md)
- [Skill API 认证](../../raw/application-api-reference/overview/authentication-26822a11844efd00.md)
- [Skill API 错误码](../../raw/application-api-reference/overview/errors-9f5f81ed72f2a1c6.md)
- [Skill 管理](../../raw/application-api-reference/overview/overview-9d8edaa0d219d019.md)
- [获取 Skill](../../raw/application-api-reference/overview/overview/get-9c06b4218676761a.md)
- [创建 Skill](../../raw/application-api-reference/overview/overview/create-44cf2cde0a7d9a72.md)
- [列出 Skill](../../raw/application-api-reference/overview/overview/list-b23c792b7a3bf72b.md)
- [删除 Skill](../../raw/application-api-reference/overview/overview/delete-75ffff308650522a.md)
- [版本管理](../../raw/application-api-reference/overview/overview-1dac56b965dd0271.md)
- [创建版本](../../raw/application-api-reference/overview/overview/create-66b335d7c24c1f0f.md)
- [列出版本](../../raw/application-api-reference/overview/overview/list-ee346a0747aae1d4.md)
- [获取版本详情](../../raw/application-api-reference/overview/overview/get-2856ed31dd1c9b3d.md)
- [下载版本 ZIP](../../raw/application-api-reference/overview/overview/download.md)
- [开通官方 MCP](../../raw/application-api-reference/overview/overview/activate.md)


