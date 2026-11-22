# overview

百炼平台的 `overview` 文档汇总了 Skill（工具）和 MCP（模型能力平台）服务的核心管理能力，涵盖认证、版本控制、生命周期操作及调用方式。本文档面向开发者，聚焦可编程接口的使用规范与约束，不涉及控制台交互或产品营销描述。

## 支持的模型/功能

- **Skill（自定义工具）**：支持上传 ZIP 包形式的自定义 Skill，包含 `SKILL.md`（必需）和执行逻辑（如 `index.js`），经安全扫描后生成版本；官方 Skill 仅提供只读访问（`active` 状态）。
- **MCP（模型能力平台）**：分为两类：
  - *官方 MCP*：通过 `/activate` 和 `/deactivate` 开通/关闭（如 `amap-maps`），部分需配置环境变量（见[开通官方 MCP](raw/application-api-reference/overview/overview/activate.md)）；
  - *自定义 MCP*：通过 `/enable`/`/disable` 启停，支持 `/update` 修改配置并重新部署（见[更新自定义 MCP](raw/application-api-reference/overview/overview/update.md)）。
- **工具推荐与调用**：提供 `/tools/recommend` 接口根据自然语言需求推荐可用工具，并通过 `/tools/call` 执行具体工具（见[调用工具](raw/application-api-reference/overview/overview/call.md)）。

## 关键参数

- **认证参数**：所有请求必须携带 `Authorization: Bearer $DASHSCOPE_API_KEY` Header，并使用工作空间专属 Endpoint（格式为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/...`），详见[认证](raw/application-api-reference/overview/authentication.md)。
- **Skill 版本参数**：`skill_id`（路径参数）、`version`（精确匹配，不回退）、`pageNo`/`pageSize`（分页，`pageNo × pageSize ≤ 10000`）。
- **MCP 操作参数**：`mcpCode`（路径参数）为必填；开通官方 MCP 时，`env` 字段为必填（若服务声明了环境变量），且 `fc_deploy_region` 必须与控制台地域一致。
- **ZIP 包限制**：上传 ZIP 包大小 ≤ 50MB；解压后总大小 ≤ 100MB；文件名编码仅支持 UTF-8 或 GBK；必须包含 `SKILL.md` 且其 Front Matter 至少含 `name` 和 `description`。

## 使用方式

1. **认证准备**：获取 API Key 并设置环境变量 `DASHSCOPE_API_KEY`，确认 `workspace_id` 正确。
2. **Skill 版本管理**：
   - 创建：`POST /api/v1/skills/{skill_id}/versions`，以 `multipart/form-data` 上传 ZIP；
   - 查询：`GET /api/v1/skills/{skill_id}/versions`（列表）或 `GET /api/v1/skills/{skill_id}/versions/{version}`（详情）；
   - 下载：`GET /api/v1/skills/{skill_id}/versions/{version}/content` 获取临时下载地址（2 小时有效）。
3. **MCP 生命周期管理**：
   - 官方 MCP：`POST /api/v1/mcp/servers/{mcpCode}/activate`（开通）或 `POST /api/v1/mcp/servers/{mcpCode}/deactivate`（关闭）；
   - 自定义 MCP：`POST /api/v1/mcp/servers/{mcpCode}/enable`（启用）、`/disable`（停用）、`/update`（更新配置）；
   - 删除：仅支持自定义 MCP，`DELETE /api/v1/mcp/servers/{mcpCode}`。
4. **工具调用**：先调用 `/tools/recommend?query=...` 获取工具信息，再用 `POST /tools/call` 提交 `tool_name` 和 `tool_params`。

> **注意**：文档 7（更新自定义 MCP）与文档 15（启用自定义 MCP）存在关键矛盾——前者称“修改 `mcp_type` 和 `mcp_config` 会重新部署”，后者明确“启用时不能提交新配置”。实际行为以文档 15 为准：`/enable` 仅使用已保存配置，新配置必须通过 `/update` 提交。

## 限制和注意事项

- **权限隔离**：RAM 子账号需显式授权；API Key 权限由控制台配置决定；官方 Skill 不可删除（见[Skill API 错误码](raw/application-api-reference/overview/errors.md)中 `SKILL_DELETE_OFFICIAL_NOT_ALLOWED`）。
- **版本不可变性**：Skill 版本号由服务端递增（`major.minor`），不可指定；旧版本保留，但挂载到智能体时必须显式指定版本，后续上传不影响已挂载实例。
- **状态约束**：
  - Skill 处于 `checking` 状态时禁止创建新版本；
  - MCP 服务运行中或部署中时，禁止 `update`/`enable`/`disable`（返回 `409 McpServerBusy`）；
  - One Key MCP 不支持关闭（`/deactivate` 返回 `400 DeActivateFailed`）。
- **错误处理**：统一响应结构含 `success`、`error_code`、`error_msg` 和 `request_id`；务必同时检查 HTTP 状态码和 `data.isError`（如工具执行失败时可能返回 `200` + `data.isError=true`）。

## 来源文档

- [认证](../../raw/application-api-reference/overview/authentication.md)
- [MCP API 错误码](../../raw/application-api-reference/overview/errors.md)
- [服务管理](../../raw/application-api-reference/overview/overview.md)
- [查询 MCP 列表](../../raw/application-api-reference/overview/overview/list.md)
- [创建自定义 MCP](../../raw/application-api-reference/overview/overview/create.md)
- [查询 MCP 详情](../../raw/application-api-reference/overview/overview/get.md)
- [更新自定义 MCP](../../raw/application-api-reference/overview/overview/update.md)
- [工具](../../raw/application-api-reference/overview/overview.md)
- [查询工具列表](../../raw/application-api-reference/overview/overview/list.md)
- [调用工具](../../raw/application-api-reference/overview/overview/call.md)
- [生命周期](../../raw/application-api-reference/overview/overview.md)
- [开通官方 MCP](../../raw/application-api-reference/overview/overview/activate.md)
- [关闭官方 MCP](../../raw/application-api-reference/overview/overview/deactivate.md)
- [停用自定义 MCP](../../raw/application-api-reference/overview/overview/disable.md)
- [启用自定义 MCP](../../raw/application-api-reference/overview/overview/enable.md)
- [Skill API 认证](../../raw/application-api-reference/overview/authentication.md)
- [Skill API 错误码](../../raw/application-api-reference/overview/errors.md)
- [Skill 管理](../../raw/application-api-reference/overview/overview.md)
- [创建 Skill](../../raw/application-api-reference/overview/overview/create.md)
- [获取 Skill](../../raw/application-api-reference/overview/overview/get.md)
- [列出 Skill](../../raw/application-api-reference/overview/overview/list.md)
- [删除 Skill](../../raw/application-api-reference/overview/overview/delete.md)
- [推荐工具](../../raw/application-api-reference/overview/overview/recommend.md)
- [版本管理](../../raw/application-api-reference/overview/overview.md)
- [获取版本详情](../../raw/application-api-reference/overview/overview/get.md)
- [创建版本](../../raw/application-api-reference/overview/overview/create.md)
- [下载版本 ZIP](../../raw/application-api-reference/overview/overview/download.md)
- [列出版本](../../raw/application-api-reference/overview/overview/list.md)
- [删除自定义 MCP](../../raw/application-api-reference/overview/overview/delete.md)


