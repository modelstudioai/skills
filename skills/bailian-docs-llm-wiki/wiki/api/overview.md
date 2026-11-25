# overview

百炼平台的 MCP（Model Calling Protocol）与 Skill 两大能力提供标准化接口，用于集成外部服务与自定义工具。MCP 支持将 HTTP、SSE、OPENAPI 或 STDIO 类型的服务快速注册为可调用的模型工具；Skill 则面向代码化技能，通过 ZIP 包定义功能逻辑与元数据。二者均基于统一认证体系，支持全生命周期管理。

## 支持的模型/功能

- **MCP 服务**：支持四种接入类型：`STDIO`（本地进程）、`HTTP`（同步请求）、`SSE`（服务端事件流）、`OPENAPI`（OpenAPI 3.0 规范描述的 RESTful 接口）。每种类型需按对应 schema 提交 `mcp_config` [创建自定义 MCP](../../raw/application-api-reference/overview/overview/create-a29c49f8a08e5095.md)。
- **官方与自定义 MCP**：可通过 `/list` 接口分页查询全部官方 MCP 和当前工作空间下的自定义 MCP；官方 MCP 需显式开通后方可使用，而 One Key 类型 MCP 在首次调用时自动开通 [查询 MCP 列表](../../raw/application-api-reference/overview/overview/list-c680a6eef36ba755.md)。
- **Skill 技能**：支持上传 ZIP 包定义技能逻辑（含 `SKILL.md` 和可执行文件），版本号由服务端自动递增（如 `1.0` → `1.1`），旧版本永久保留且不影响已挂载智能体 [版本管理](../../raw/application-api-reference/overview/overview-1dac56b965dd0271.md)。
- **工具发现与调用**：提供三类工具操作接口：`/tools`（查询工具列表）、`/tools/call`（调用指定工具）、`/tools/recommend`（根据自然语言需求推荐工具）[工具](../../raw/application-api-reference/overview/overview-743a72f61b3a54f8.md)。

## 关键参数

- **认证参数**：所有请求必须携带 `Authorization: Bearer $DASHSCOPE_API_KEY` Header，并使用工作空间专属 Endpoint（格式为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/{resource}`）[认证](../../raw/application-api-reference/overview/authentication-58370587ddc046ee.md)。
- **分页参数**：`pageNo`（从 1 开始）和 `pageSize`（1–100），`pageNo × pageSize ≤ 10000`，适用于 `/list` 及 `/versions` 等接口。
- **MCP 配置字段**：
  - `mcp_type`：必填，值为 `STDIO`/`HTTP`/`SSE`/`OPENAPI`；
  - `mcp_config`：结构强依赖 `mcp_type`，例如 `HTTP` 类型需提供 `url` 和可选 `headers`，`OPENAPI` 类型需完整定义 `api_list` 及各 API 的 `input_params` [创建自定义 MCP](../../raw/application-api-reference/overview/overview/create-a29c49f8a08e5095.md)。
- **Skill ZIP 要求**：根目录必须包含 `SKILL.md`（Front Matter 中 `name` 和 `description` 为必填字段），包大小 ≤ 50MB，解压后内容 ≤ 100MB [创建 Skill](../../raw/application-api-reference/overview/overview/create-44cf2cde0a7d9a72.md)。

## 使用方式

1. **认证配置**：设置环境变量 `DASHSCOPE_API_KEY`，并从控制台获取 `workspace_id` 构造 Endpoint。
2. **MCP 流程**：
   - 查询可用 MCP：`GET /api/v1/mcp/servers/list`
   - 创建自定义 MCP：`POST /api/v1/mcp/servers`（传入 `server_name`, `description`, `mcp_type`, `mcp_config`）
   - 开通官方 MCP：`POST /api/v1/mcp/servers/{mcpCode}/activate`
   - 调用工具：`POST /api/v1/mcp/servers/{mcpCode}/tools/call`（需先查工具列表确认 `tool_name` 和参数 schema）
3. **Skill 流程**：
   - 创建 Skill：`POST /api/v1/skills`（`multipart/form-data` 上传 ZIP）
   - 上传新版本：`POST /api/v1/skills/{skill_id}/versions`
   - 查询版本详情：`GET /api/v1/skills/{skill_id}/versions/{version}`
   - 下载 ZIP：`GET /api/v1/skills/{skill_id}/versions/{version}/content`（返回 2 小时有效预签名 URL）

> **注意**：文档中 `MCP API 错误码`（文档 7）与 `Skill API 错误码`（文档 18）的 HTTP 状态码语义存在差异：MCP 的 `403 AccessDenied` 表示鉴权失败，而 Skill 的 `401 WORKSPACE_ID_ILLEGAL` 才表示身份无效；开发者应分别参照各自错误码文档处理响应。

## 限制和注意事项

- **权限隔离**：API Key 权限作用于工作空间级别，RAM 子账号需显式授权；官方 MCP 不支持删除或修改，仅可开通/关闭；自定义 MCP 删除后不可恢复 [删除自定义 MCP](../../raw/application-api-reference/overview/overview/delete-23f946e3aa963ba8.md)。
- **状态约束**：
  - 修改自定义 MCP 配置前必须先停用（`/disable`），否则返回 `400 OperationNotSupported`；
  - Skill 处于 `checking`（安全扫描中）状态时，禁止创建新版本 [创建版本](../../raw/application-api-reference/overview/overview/create-66b335d7c24c1f0f.md)；
  - 官方 MCP 的 `deactivate` 接口不支持 One Key 类型 [关闭官方 MCP](../../raw/application-api-reference/overview/overview/deactivate.md)。
- **敏感信息保护**：`/get` 接口响应中的 `mcp_config.headers` 可能包含 API Key 等凭据，务必避免日志记录或前端暴露 [查询 MCP 详情](../../raw/application-api-reference/overview/overview/get-b57e1839b6840677.md)。
- **错误处理惯例**：[工具调用](../concepts/tool-calling.md)成功但业务失败时，HTTP 状态码仍为 `200`，需检查响应体中 `data.isError === true`；所有接口均返回 `request_id`，用于问题排查 [MCP API 错误码](../../raw/application-api-reference/overview/errors-972b4127b84f4429.md)。

## 来源文档

- [认证](../../raw/application-api-reference/overview/authentication-58370587ddc046ee.md)
- [服务管理](../../raw/application-api-reference/overview/overview-448e7f104037b903.md)
- [查询 MCP 列表](../../raw/application-api-reference/overview/overview/list-c680a6eef36ba755.md)
- [创建自定义 MCP](../../raw/application-api-reference/overview/overview/create-a29c49f8a08e5095.md)
- [查询 MCP 详情](../../raw/application-api-reference/overview/overview/get-b57e1839b6840677.md)
- [更新自定义 MCP](../../raw/application-api-reference/overview/overview/update.md)
- [MCP API 错误码](../../raw/application-api-reference/overview/errors-972b4127b84f4429.md)
- [删除自定义 MCP](../../raw/application-api-reference/overview/overview/delete-23f946e3aa963ba8.md)
- [工具](../../raw/application-api-reference/overview/overview-743a72f61b3a54f8.md)
- [查询工具列表](../../raw/application-api-reference/overview/overview/list-64eddd50625ee03f.md)
- [调用工具](../../raw/application-api-reference/overview/overview/call.md)
- [推荐工具](../../raw/application-api-reference/overview/overview/recommend.md)
- [生命周期](../../raw/application-api-reference/overview/overview-fc1e2b9f062d93f5.md)
- [开通官方 MCP](../../raw/application-api-reference/overview/overview/activate.md)
- [关闭官方 MCP](../../raw/application-api-reference/overview/overview/deactivate.md)
- [停用自定义 MCP](../../raw/application-api-reference/overview/overview/disable.md)
- [启用自定义 MCP](../../raw/application-api-reference/overview/overview/enable.md)
- [Skill API 错误码](../../raw/application-api-reference/overview/errors-9f5f81ed72f2a1c6.md)
- [Skill API 认证](../../raw/application-api-reference/overview/authentication-26822a11844efd00.md)
- [Skill 管理](../../raw/application-api-reference/overview/overview-9d8edaa0d219d019.md)
- [创建 Skill](../../raw/application-api-reference/overview/overview/create-44cf2cde0a7d9a72.md)
- [列出 Skill](../../raw/application-api-reference/overview/overview/list-b23c792b7a3bf72b.md)
- [获取 Skill](../../raw/application-api-reference/overview/overview/get-9c06b4218676761a.md)
- [删除 Skill](../../raw/application-api-reference/overview/overview/delete-75ffff308650522a.md)
- [版本管理](../../raw/application-api-reference/overview/overview-1dac56b965dd0271.md)
- [创建版本](../../raw/application-api-reference/overview/overview/create-66b335d7c24c1f0f.md)
- [列出版本](../../raw/application-api-reference/overview/overview/list-ee346a0747aae1d4.md)
- [下载版本 ZIP](../../raw/application-api-reference/overview/overview/download.md)
- [获取版本详情](../../raw/application-api-reference/overview/overview/get-2856ed31dd1c9b3d.md)


