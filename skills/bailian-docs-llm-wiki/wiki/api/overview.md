# overview

百炼 MCP（Model Calling Protocol）与 Skill 服务提供了一套标准化的模型能力接入与扩展机制，支持开发者通过 API 管理自定义工具服务（MCP）和可复用技能包（Skill）。本文档概述其核心能力、使用方式及关键约束，适用于需要集成外部服务或封装业务逻辑的开发者。

## 支持的模型/功能

- **MCP（Model Calling Protocol）服务**：支持四种接入类型——`STDIO`（函数计算部署）、`HTTP`、`SSE` 和 `OPENAPI`，用于将任意后端服务封装为大模型可调用的工具。官方 MCP（如高德地图）需开通后使用；自定义 MCP 可由用户创建、更新、停用/启用及删除。
- **Skill 技能包**：以 ZIP 包形式上传的可复用能力单元，包含 `SKILL.md` 定义元信息及执行代码。支持多版本管理、安全扫描（状态为 `checking` 或 `rejected`）、下载与挂载到智能体。Skill 分为官方（`source: "official"`）和自定义（`source: "customer"`）两类，详见 [Skill 管理](raw/application-api-reference/overview/overview-9d8edaa0d219d019.md)。
- **工具发现与调用**：提供 `tools/recommend`（按自然语言需求推荐工具）、`/{mcpCode}/tools`（查询工具列表）和 `/{mcpCode}/tools/call`（调用指定工具）三类接口，实现动态工具发现与执行。

> **注意**：文档 17（Skill API 错误码）中列出的 `SKILL_NAME_OFFICIAL_DUPLICATE` 错误码在文档 19 和 24 中被重复引用，但文档 17 的错误码说明更完整，应以该文档为准；文档 1 和文档 28 均描述认证流程，但文档 28 针对 Skill API 明确返回 `401 WORKSPACE_ID_ILLEGAL`，而文档 1 对 MCP API 返回 `403 AccessDenied`，二者鉴权逻辑一致但错误码语义不同，属正常设计分层。

## 关键参数

- **通用参数**：
  - `workspace_id`：工作空间 ID，用于构造 Endpoint（如 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com`），从控制台右上角复制。
  - `DASHSCOPE_API_KEY`：百炼 API Key，通过 Header `Authorization: Bearer $DASHSCOPE_API_KEY` 传递，具有工作空间级权限，[获取方式见此文档](../../raw/application-api-reference/overview/authentication-58370587ddc046ee.md)。
- **MCP 相关**：
  - `mcp_code`：MCP 唯一编码，创建后生成，用于所有操作路径（如 `/api/v1/mcp/servers/{mcpCode}`）。
  - `mcp_type`：必填，取值为 `STDIO`/`HTTP`/`SSE`/`OPENAPI`，决定 `mcp_config` 结构。
  - 分页参数：`pageNo`（≥1）、`pageSize`（1–100），且 `pageNo × pageSize ≤ 10000`（见 [查询 MCP 列表](../../raw/application-api-reference/overview/overview/list-c680a6eef36ba755.md)）。
- **Skill 相关**：
  - `skill_id`：Skill 唯一标识，创建后返回，用于版本管理等操作。
  - `version`：版本号格式为 `major.minor`（如 `1.0`），由服务端递增，不可手动指定（见 [创建版本](../../raw/application-api-reference/overview/overview/create-66b335d7c24c1f0f.md)）。
  - ZIP 包限制：上传大小 ≤ 50MB，解压后总大小 ≤ 100MB，必须包含 `SKILL.md` 且含 `name` 和 `description` 字段。

## 使用方式

1. **认证配置**：设置环境变量 `DASHSCOPE_API_KEY`，并确认 `workspace_id` 正确；MCP 与 Skill API 共享同一认证机制，Endpoint 基础路径分别为 `/api/v1/mcp/servers` 和 `/api/v1/skills`。
2. **MCP 生命周期操作**：
   - 官方 MCP：调用 `POST /{mcpCode}/activate` 开通，`POST /{mcpCode}/deactivate` 关闭。
   - 自定义 MCP：`POST /` 创建 → `POST /{mcpCode}/disable` 停用 → `POST /{mcpCode}/enable` 启用 → `DELETE /{mcpCode}` 删除。
3. **Skill 全流程管理**：
   - 创建：`POST /api/v1/skills` 上传 ZIP 包。
   - 版本迭代：`POST /api/v1/skills/{skill_id}/versions` 上传新版本。
   - 查询：`GET /api/v1/skills`（列表）、`GET /api/v1/skills/{skill_id}`（详情）、`GET /api/v1/skills/{skill_id}/versions`（版本列表）。
   - 下载：`GET /api/v1/skills/{skill_id}/versions/{version}/content` 获取临时 ZIP 下载地址（有效期 2 小时）。
4. **工具调用**：
   - 先查可用工具：`GET /api/v1/mcp/servers/{mcpCode}/tools`。
   - 或按需推荐：`GET /api/v1/mcp/servers/tools/recommend?query=...`。
   - 再执行：`POST /api/v1/mcp/servers/{mcpCode}/tools/call`，请求体必须含 `tool_name`（即使无参）。

## 限制和注意事项

- **权限与安全**：API Key 具有工作空间级权限，严禁硬编码或提交至代码仓库；`mcp_config.headers` 可能包含敏感凭据（如 API Key），响应中需脱敏处理（见 [查询 MCP 详情](../../raw/application-api-reference/overview/overview/get-b57e1839b6840677.md) 警告）。
- **状态依赖**：操作前需校验服务状态。例如，更新自定义 MCP 配置前必须先停用（`disable`），否则返回 `400 OperationNotSupported`；Skill 在 `checking` 状态时无法创建新版本（见 [创建版本](../../raw/application-api-reference/overview/overview/create-66b335d7c24c1f0f.md) 规则）。
- **错误处理**：必须同时检查 HTTP 状态码和响应体中的 `success` 字段及 `data.isError`（尤其 `tools/call` 接口可能返回 `200 success=true data.isError=true`）；所有错误均带 `request_id`，用于问题定位（见 [MCP API 错误码](../../raw/application-api-reference/overview/errors-972b4127b84f4429.md)）。
- **数据一致性**：Skill 列表（`GET /api/v1/skills`）为异步更新，新建/删除后可能短暂不一致，应以 `GET /api/v1/skills/{skill_id}` 结果为准（见 [列出 Skill](../../raw/application-api-reference/overview/overview/list-b23c792b7a3bf72b.md) 说明）。

## 来源文档

- [认证](../../raw/application-api-reference/overview/authentication-58370587ddc046ee.md)
- [服务管理](../../raw/application-api-reference/overview/overview-448e7f104037b903.md)
- [查询 MCP 列表](../../raw/application-api-reference/overview/overview/list-c680a6eef36ba755.md)
- [创建自定义 MCP](../../raw/application-api-reference/overview/overview/create-a29c49f8a08e5095.md)
- [查询 MCP 详情](../../raw/application-api-reference/overview/overview/get-b57e1839b6840677.md)
- [更新自定义 MCP](../../raw/application-api-reference/overview/overview/update.md)
- [删除自定义 MCP](../../raw/application-api-reference/overview/overview/delete-23f946e3aa963ba8.md)
- [工具](../../raw/application-api-reference/overview/overview-743a72f61b3a54f8.md)
- [MCP API 错误码](../../raw/application-api-reference/overview/errors-972b4127b84f4429.md)
- [调用工具](../../raw/application-api-reference/overview/overview/call.md)
- [生命周期](../../raw/application-api-reference/overview/overview-fc1e2b9f062d93f5.md)
- [开通官方 MCP](../../raw/application-api-reference/overview/overview/activate.md)
- [关闭官方 MCP](../../raw/application-api-reference/overview/overview/deactivate.md)
- [停用自定义 MCP](../../raw/application-api-reference/overview/overview/disable.md)
- [启用自定义 MCP](../../raw/application-api-reference/overview/overview/enable.md)
- [查询工具列表](../../raw/application-api-reference/overview/overview/list-64eddd50625ee03f.md)
- [Skill API 错误码](../../raw/application-api-reference/overview/errors-9f5f81ed72f2a1c6.md)
- [Skill 管理](../../raw/application-api-reference/overview/overview-9d8edaa0d219d019.md)
- [创建 Skill](../../raw/application-api-reference/overview/overview/create-44cf2cde0a7d9a72.md)
- [推荐工具](../../raw/application-api-reference/overview/overview/recommend.md)
- [列出 Skill](../../raw/application-api-reference/overview/overview/list-b23c792b7a3bf72b.md)
- [删除 Skill](../../raw/application-api-reference/overview/overview/delete-75ffff308650522a.md)
- [版本管理](../../raw/application-api-reference/overview/overview-1dac56b965dd0271.md)
- [创建版本](../../raw/application-api-reference/overview/overview/create-66b335d7c24c1f0f.md)
- [列出版本](../../raw/application-api-reference/overview/overview/list-ee346a0747aae1d4.md)
- [获取版本详情](../../raw/application-api-reference/overview/overview/get-2856ed31dd1c9b3d.md)
- [下载版本 ZIP](../../raw/application-api-reference/overview/overview/download.md)
- [Skill API 认证](../../raw/application-api-reference/overview/authentication-26822a11844efd00.md)
- [获取 Skill](../../raw/application-api-reference/overview/overview/get-9c06b4218676761a.md)


