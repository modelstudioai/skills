# overview

百炼平台的 MCP（Model Calling Protocol）与 Skill 两大能力体系，为开发者提供标准化的模型服务接入和可复用的功能模块管理。MCP 用于封装外部工具服务（如天气、地图、数据库等），通过统一协议暴露为可调用的工具；Skill 则是面向智能体的、可版本化管理的代码包，支持 ZIP 打包、安全扫描与多版本挂载。二者均基于工作空间隔离，通过 API Key 鉴权，适用于构建复杂 Agent 工作流。

## 支持的模型/功能

- **MCP 服务类型**：支持 `STDIO`（函数计算部署）、`HTTP`、`SSE` 和 `OPENAPI` 四种接入方式，覆盖本地 CLI 工具、Webhook 服务及符合 OpenAPI 规范的 RESTful 接口 [创建自定义 MCP](../../raw/application-api-reference/overview/overview/create-a29c49f8a08e5095.md)。
- **MCP 生命周期操作**：官方 MCP 可开通（`activate`）与关闭（`deactivate`）；自定义 MCP 支持创建、更新配置、停用（`disable`）与启用（`enable`），且停用后配置保留 [生命周期](../../raw/application-api-reference/overview/overview-fc1e2b9f062d93f5.md)。
- **Skill 功能**：支持 ZIP 包上传创建自定义 Skill、多版本管理（自动递增 `major.minor` 格式）、安全扫描（状态含 `checking`/`active`/`rejected`）、按版本下载与挂载到智能体 [版本管理](../../raw/application-api-reference/overview/overview-1dac56b965dd0271.md)。
- **工具交互能力**：所有 MCP 均可通过 `/tools` 查询工具列表、`/tools/call` 同步调用、`/tools/recommend` 按自然语言推荐工具，实现语义驱动的工具发现与执行 [工具](../../raw/application-api-reference/overview/overview-743a72f61b3a54f8.md)。

## 关键参数

- **认证参数**：必须使用百炼 API Key（通过 `Authorization: Bearer <key>` 传递），并指定工作空间 Endpoint（如 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com`）。MCP 与 Skill 使用不同 Endpoint 路径：MCP 为 `/api/v1/mcp/servers`，Skill 为 `/api/v1/skills`。
- **MCP 创建必填字段**：`server_name`、`description`、`mcp_type` 及对应 `mcp_config`（如 `HTTP` 类型需 `url`，`OPENAPI` 类型需 `api_list`）；`args` 中参数值须匹配正则 `[A-Za-z0-9_@./:=,+-]+`，环境变量名须匹配 `[A-Za-z_][A-Za-z0-9_]*`。
- **Skill 上传约束**：ZIP 包大小 ≤ 50MB，解压后总大小 ≤ 100MB；根目录必须包含 `SKILL.md`，其 Front Matter 必须含 `name` 和 `description` 字段。
- **分页参数**：MCP 列表与 Skill 列表均支持 `pageNo`（≥1）和 `pageSize`（1–100），且 `pageNo × pageSize ≤ 10000`。

## 使用方式

- **MCP 服务管理**：  
  - 查询：`GET /api/v1/mcp/servers/list?type=CUSTOMER` 分页获取自定义服务；`GET /api/v1/mcp/servers/{mcpCode}` 获取详情（含 `mcp_config`，但注意敏感信息风险 [查询 MCP 详情](../../raw/application-api-reference/overview/overview/get-b57e1839b6840677.md)）。  
  - 创建：`POST /api/v1/mcp/servers` 提交完整配置，成功返回 `201` 并触发部署（即使部署失败也返回 `201`，状态为 `ACTIVATE_FAILED`）。  
  - 更新：`POST /api/v1/mcp/servers/{mcpCode}` 仅修改名称/描述不重新部署；修改 `mcp_type` 或 `mcp_config` 需先停用服务，否则返回 `400 OperationNotSupported`。  
- **Skill 全流程**：  
  - 创建：`POST /api/v1/skills` 上传 ZIP，初始版本为 `1.0`；后续版本通过 `POST /api/v1/skills/{skill_id}/versions` 上传，版本号由服务端自动递增。  
  - 管理：`GET /api/v1/skills/{skill_id}/versions` 查看历史版本；`GET /api/v1/skills/{skill_id}/versions/{version}/content` 获取临时下载地址（2 小时有效）。  
- **工具调用**：先查工具列表（`GET /api/v1/mcp/servers/{mcpCode}/tools`），再调用（`POST /api/v1/mcp/servers/{mcpCode}/tools/call`），务必检查响应中 `data.isError` 字段，因工具内部错误可能返回 HTTP 200 + `isError=true` [调用工具](../../raw/application-api-reference/overview/overview/call.md)。

## 限制和注意事项

- **权限与范围**：API Key 具有工作空间级权限，RAM 子账号需显式授权；官方 MCP 不支持删除或修改配置，仅能开通/关闭；自定义 MCP 删除后不可恢复 [删除自定义 MCP](../../raw/application-api-reference/overview/overview/delete-23f946e3aa963ba8.md)。
- **状态一致性**：Skill 列表接口（`GET /api/v1/skills`）数据异步更新，新建/删除后可能短暂延迟；应以单个 Skill 查询（`GET /api/v1/skills/{skill_id}`）结果为准 [列出 Skill](../../raw/application-api-reference/overview/overview/list-b23c792b7a3bf72b.md)。
- **错误处理差异**：MCP API 错误码中 `403 AccessDenied` 表示鉴权失败，而 Skill API 对应错误码为 `401 WORKSPACE_ID_ILLEGAL`；二者错误结构相似但字段名与枚举值不完全兼容，需分别处理 [MCP API 错误码](../../raw/application-api-reference/overview/errors-972b4127b84f4429.md) 与 [Skill API 错误码](../../raw/application-api-reference/overview/errors-9f5f81ed72f2a1c6.md)。
- > **注意**：文档 17（Skill API 认证）与文档 1（MCP 认证）均声明使用 `DASHSCOPE_API_KEY`，但文档 1 的错误说明指出认证失败返回 `403 AccessDenied`，而文档 17 明确 `401 WORKSPACE_ID_ILLEGAL` 是身份缺失/无效的错误码。实际开发中应以具体接口返回的 HTTP 状态码和 `error_code` 为准，而非统一假设 `403` 为鉴权失败。
- > **注意**：文档 4（创建自定义 MCP）示例响应被截断（末尾为 `"data": { "mcp_co`），且未给出完整 `CreateResponse` 结构；应以文档 5（更新）和文档 6（详情）中定义的 `mcp_code`/`server_status` 等字段为准，避免依赖不完整示例。
- **敏感信息防护**：`GET /api/v1/mcp/servers/{mcpCode}` 响应中的 `mcp_config.headers` 可能包含 API Key 等凭据，调用方需严格保护响应内容，禁止日志打印或前端透出。

## 来源文档

- [认证](../../raw/application-api-reference/overview/authentication-58370587ddc046ee.md)
- [MCP API 错误码](../../raw/application-api-reference/overview/errors-972b4127b84f4429.md)
- [服务管理](../../raw/application-api-reference/overview/overview-448e7f104037b903.md)
- [创建自定义 MCP](../../raw/application-api-reference/overview/overview/create-a29c49f8a08e5095.md)
- [更新自定义 MCP](../../raw/application-api-reference/overview/overview/update.md)
- [查询 MCP 详情](../../raw/application-api-reference/overview/overview/get-b57e1839b6840677.md)
- [工具](../../raw/application-api-reference/overview/overview-743a72f61b3a54f8.md)
- [查询工具列表](../../raw/application-api-reference/overview/overview/list-64eddd50625ee03f.md)
- [删除自定义 MCP](../../raw/application-api-reference/overview/overview/delete-23f946e3aa963ba8.md)
- [调用工具](../../raw/application-api-reference/overview/overview/call.md)
- [推荐工具](../../raw/application-api-reference/overview/overview/recommend.md)
- [生命周期](../../raw/application-api-reference/overview/overview-fc1e2b9f062d93f5.md)
- [开通官方 MCP](../../raw/application-api-reference/overview/overview/activate.md)
- [关闭官方 MCP](../../raw/application-api-reference/overview/overview/deactivate.md)
- [停用自定义 MCP](../../raw/application-api-reference/overview/overview/disable.md)
- [启用自定义 MCP](../../raw/application-api-reference/overview/overview/enable.md)
- [Skill API 认证](../../raw/application-api-reference/overview/authentication-26822a11844efd00.md)
- [Skill API 错误码](../../raw/application-api-reference/overview/errors-9f5f81ed72f2a1c6.md)
- [Skill 管理](../../raw/application-api-reference/overview/overview-9d8edaa0d219d019.md)
- [创建 Skill](../../raw/application-api-reference/overview/overview/create-44cf2cde0a7d9a72.md)
- [获取 Skill](../../raw/application-api-reference/overview/overview/get-9c06b4218676761a.md)
- [列出 Skill](../../raw/application-api-reference/overview/overview/list-b23c792b7a3bf72b.md)
- [删除 Skill](../../raw/application-api-reference/overview/overview/delete-75ffff308650522a.md)
- [版本管理](../../raw/application-api-reference/overview/overview-1dac56b965dd0271.md)
- [创建版本](../../raw/application-api-reference/overview/overview/create-66b335d7c24c1f0f.md)
- [列出版本](../../raw/application-api-reference/overview/overview/list-ee346a0747aae1d4.md)
- [下载版本 ZIP](../../raw/application-api-reference/overview/overview/download.md)
- [获取版本详情](../../raw/application-api-reference/overview/overview/get-2856ed31dd1c9b3d.md)
- [查询 MCP 列表](../../raw/application-api-reference/overview/overview/list-c680a6eef36ba755.md)


