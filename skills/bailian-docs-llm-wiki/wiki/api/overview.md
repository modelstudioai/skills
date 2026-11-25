# overview

百炼平台的 MCP（Model Calling Protocol）和 Skill 两大能力体系，为开发者提供标准化的模型服务集成与可复用技能管理能力。MCP 用于对接外部工具服务（如天气、地图、数据库等），支持多种协议类型；Skill 则是封装了完整业务逻辑的可挂载、可版本化的功能单元。二者均通过统一的 API Key 鉴权和工作空间 Endpoint 访问，适用于构建智能体、自动化流程等场景。

## 支持的模型/功能

- **MCP 服务**：支持官方 MCP（如高德地图、通义万相）和自定义 MCP，后者可基于 `STDIO`（函数计算部署）、`HTTP`、`SSE` 或 `OPENAPI` 四种协议接入外部服务 [创建自定义 MCP](../../raw/application-api-reference/overview/overview/create-a29c49f8a08e5095.md)。
- **Skill 技能**：支持上传 ZIP 包形式的自定义 Skill（含 `SKILL.md` 和代码文件），经安全扫描后生成版本化技能；官方 Skill 可直接查询和挂载 [创建 Skill](../../raw/application-api-reference/overview/overview/create-44cf2cde0a7d9a72.md)。
- **核心功能**：
  - MCP：服务全生命周期管理（开通/关闭/启用/停用）、工具发现（列表/推荐）、工具调用；
  - Skill：版本化管理（创建/查询/下载/删除）、状态跟踪（`checking`/`active`/`rejected`）。

## 关键参数

- **认证参数**：`DASHSCOPE_API_KEY`（环境变量或 `Authorization: Bearer` Header），配合工作空间 ID 构成 Endpoint（如 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com`）[认证](../../raw/application-api-reference/overview/authentication-58370587ddc046ee.md)。
- **分页参数**：`pageNo`（≥1）、`pageSize`（1–100），`pageNo × pageSize ≤ 10000`，适用于 MCP 列表、Skill 列表及版本列表等接口。
- **MCP 配置字段**：`mcp_type`（必填）、`mcp_config`（按类型结构化，如 `HTTP` 的 `url` 和 `headers`，`OPENAPI` 的 `api_list` 及 `input_params` schema）。
- **Skill ZIP 要求**：根目录必须包含 `SKILL.md`（Front Matter 含 `name` 和 `description`），包大小 ≤ 50MB，解压后总大小 ≤ 100MB [Skill API 错误码](../../raw/application-api-reference/overview/errors-9f5f81ed72f2a1c6.md)。

## 使用方式

1. **初始化**：配置 `DASHSCOPE_API_KEY` 环境变量，并确认工作空间 ID 正确。
2. **MCP 流程**：
   - 查询可用 MCP：`GET /api/v1/mcp/servers/list?type=CUSTOMER`
   - 创建自定义 MCP：`POST /api/v1/mcp/servers`（传 `server_name`, `mcp_type`, `mcp_config`）
   - 查询工具列表：`GET /api/v1/mcp/servers/{mcpCode}/tools`
   - 调用工具：`POST /api/v1/mcp/servers/{mcpCode}/tools/call`（传 `tool_name` 和 `tool_params`）
3. **Skill 流程**：
   - 创建 Skill：`POST /api/v1/skills`（`multipart/form-data` 上传 ZIP）
   - 查询 Skill：`GET /api/v1/skills/{skill_id}`（确认 `status` 为 `active` 后挂载）
   - 创建新版本：`POST /api/v1/skills/{skill_id}/versions`（ZIP 包自动递增版本号）

> **注意**：One Key MCP 服务（如部分云市场商品）不支持手动开通/关闭，首次调用工具时可能自动开通并产生费用；而需要 KMS 凭据或 RAM 角色的 MCP 必须前往控制台手动开通 [开通官方 MCP](../../raw/application-api-reference/overview/overview/activate.md)。

## 限制和注意事项

- **权限与安全**：
  - API Key 具有工作空间级权限，严禁硬编码或泄露 [认证](../../raw/application-api-reference/overview/authentication-58370587ddc046ee.md)。
  - `mcp_config.headers` 响应中可能包含敏感凭据（如 `Authorization`），需妥善保护响应内容 [查询 MCP 详情](../../raw/application-api-reference/overview/overview/get-b57e1839b6840677.md)。
- **状态与并发**：
  - 自定义 MCP 修改配置前必须先停用（`/disable`），否则返回 `400 OperationNotSupported`。
  - Skill 在 `checking` 状态时禁止创建新版本，需等待安全扫描完成。
- **错误处理**：
  - 工具调用失败时，接口可能返回 `200 success=true data.isError=true`，务必同时检查 HTTP 状态码和 `data.isError` 字段 [调用工具](../../raw/application-api-reference/overview/overview/call.md)。
  - 列表类接口（如 `/skills`）数据异步更新，状态变更后可能短暂延迟，应以单资源接口（如 `/skills/{id}`）结果为准 [列出 Skill](../../raw/application-api-reference/overview/overview/list-b23c792b7a3bf72b.md)。
- **其他限制**：
  - 官方 MCP 不支持删除；自定义 MCP 删除后不可恢复。
  - Skill ZIP 文件名编码仅支持 UTF-8 或 GBK，否则解压失败。

## 来源文档

- [认证](../../raw/application-api-reference/overview/authentication-58370587ddc046ee.md)
- [MCP API 错误码](../../raw/application-api-reference/overview/errors-972b4127b84f4429.md)
- [查询 MCP 列表](../../raw/application-api-reference/overview/overview/list-c680a6eef36ba755.md)
- [服务管理](../../raw/application-api-reference/overview/overview-448e7f104037b903.md)
- [创建自定义 MCP](../../raw/application-api-reference/overview/overview/create-a29c49f8a08e5095.md)
- [查询 MCP 详情](../../raw/application-api-reference/overview/overview/get-b57e1839b6840677.md)
- [更新自定义 MCP](../../raw/application-api-reference/overview/overview/update.md)
- [删除自定义 MCP](../../raw/application-api-reference/overview/overview/delete-23f946e3aa963ba8.md)
- [工具](../../raw/application-api-reference/overview/overview-743a72f61b3a54f8.md)
- [调用工具](../../raw/application-api-reference/overview/overview/call.md)
- [推荐工具](../../raw/application-api-reference/overview/overview/recommend.md)
- [生命周期](../../raw/application-api-reference/overview/overview-fc1e2b9f062d93f5.md)
- [关闭官方 MCP](../../raw/application-api-reference/overview/overview/deactivate.md)
- [开通官方 MCP](../../raw/application-api-reference/overview/overview/activate.md)
- [启用自定义 MCP](../../raw/application-api-reference/overview/overview/enable.md)
- [停用自定义 MCP](../../raw/application-api-reference/overview/overview/disable.md)
- [Skill API 认证](../../raw/application-api-reference/overview/authentication-26822a11844efd00.md)
- [Skill API 错误码](../../raw/application-api-reference/overview/errors-9f5f81ed72f2a1c6.md)
- [Skill 管理](../../raw/application-api-reference/overview/overview-9d8edaa0d219d019.md)
- [创建 Skill](../../raw/application-api-reference/overview/overview/create-44cf2cde0a7d9a72.md)
- [列出 Skill](../../raw/application-api-reference/overview/overview/list-b23c792b7a3bf72b.md)
- [获取 Skill](../../raw/application-api-reference/overview/overview/get-9c06b4218676761a.md)
- [版本管理](../../raw/application-api-reference/overview/overview-1dac56b965dd0271.md)
- [查询工具列表](../../raw/application-api-reference/overview/overview/list-64eddd50625ee03f.md)
- [列出版本](../../raw/application-api-reference/overview/overview/list-ee346a0747aae1d4.md)
- [获取版本详情](../../raw/application-api-reference/overview/overview/get-2856ed31dd1c9b3d.md)
- [下载版本 ZIP](../../raw/application-api-reference/overview/overview/download.md)
- [删除 Skill](../../raw/application-api-reference/overview/overview/delete-75ffff308650522a.md)
- [创建版本](../../raw/application-api-reference/overview/overview/create-66b335d7c24c1f0f.md)


