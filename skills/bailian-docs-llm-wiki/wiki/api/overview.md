# overview

百炼平台的 Skill API 提供对自定义和官方 Skill（即 MCP 工具）的全生命周期管理能力，包括创建、查询、更新、调用和删除。核心能力围绕 Skill 版本管理与 MCP 服务启停展开，所有操作均通过统一的 RESTful 接口完成，需使用百炼 API Key 鉴权。

## 支持的模型/功能

- **Skill（自定义工具）**：支持上传 ZIP 包形式的自定义 Skill，包含 `SKILL.md` 和执行逻辑（如 `index.js`），经安全扫描后生成版本；版本号由服务端自动递增（`major.minor` 格式），旧版本永久保留 [创建版本](../../raw/application-api-reference/overview/overview/create.md)。
- **MCP 服务（官方 & 自定义）**：
  - *官方 MCP*：通过 `/activate` 和 `/deactivate` 开通或关闭（One Key 类型不支持关闭）[开通官方 MCP](../../raw/application-api-reference/overview/overview/activate.md)；
  - *自定义 MCP*：通过 `/enable` / `/disable` 启停服务，通过 `/update` 修改配置并重新部署 [更新自定义 MCP](../../raw/application-api-reference/overview/overview/update.md)。
- **工具调用与发现**：支持直接调用指定 MCP 工具（`/tools/call`），也支持根据自然语言需求推荐匹配工具（`/tools/recommend`）[推荐工具](../../raw/application-api-reference/overview/overview/recommend.md)。

## 关键参数

- **认证参数**：`DASHSCOPE_API_KEY`（HTTP Header `Authorization: Bearer <key>`）和 `workspace_id`（用于构造 Endpoint，如 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com`）是所有请求的必需前置条件，详见 [认证](../../raw/application-api-reference/overview/authentication.md)。
- **Skill 版本参数**：`skill_id`（路径）、`version`（路径，精确匹配）、`pageNo`/`pageSize`（分页查询）；ZIP 包大小限制为 ≤50MB，解压后总大小 ≤100MB。
- **MCP 操作参数**：`mcpCode`（路径）、`tool_name`（调用时必填）、`query`（推荐时必填）；官方 MCP 的 `activate` 接口可能需传入 `env` 环境变量。

## 使用方式

1. **认证准备**：在控制台获取 API Key 并设置环境变量，确认工作空间 ID。
2. **Skill 管理**：
   - 创建新版本：`POST /api/v1/skills/{skill_id}/versions`，以 `multipart/form-data` 上传 ZIP；
   - 查询版本：`GET /api/v1/skills/{skill_id}/versions`（列表）或 `GET /api/v1/skills/{skill_id}/versions/{version}`（详情）；
   - 下载 ZIP：`GET /api/v1/skills/{skill_id}/versions/{version}/content` 获取临时下载链接。
3. **MCP 管理**：
   - 官方 MCP：`POST /api/v1/mcp/servers/{mcpCode}/activate` 或 `/deactivate`；
   - 自定义 MCP：`POST /api/v1/mcp/servers/{mcpCode}/enable` / `/disable` 启停，`POST /api/v1/mcp/servers/{mcpCode}` 更新配置；
   - 调用工具：`POST /api/v1/mcp/servers/{mcpCode}/tools/call`，需提供 `tool_name` 和可选 `tool_params`。
4. **错误处理**：统一响应结构含 `success`、`error_code`、`error_msg` 和 `request_id`；需同时检查 HTTP 状态码与 `data.isError` 字段（尤其在工具调用中）。

> **注意**：文档中多次出现对同一接口（如 `/api/v1/skills/{skill_id}/versions`）的描述，但部分文档（如 文档 3、9、13、20、26）将“版本管理”作为主标题，而实际内容完全重复，属冗余信息；开发者应以具体接口文档（如 [创建版本](../../raw/application-api-reference/overview/overview/create.md)）为准，避免混淆。

## 限制和注意事项

- **权限限制**：API Key 权限由控制台配置决定；RAM 子账号需显式授权；官方 Skill 仅允许查询/下载 `active` 版本，自定义 Skill 可操作全部未删除版本。
- **并发与状态限制**：Skill 正在 `checking`（安全扫描）状态时，禁止创建新版本；修改自定义 MCP 配置前必须先停用（`/disable`），否则返回 `400`；同一 Skill 的版本创建存在并发锁（`SKILL_UPDATE_LOCK_ERROR`）。
- **文件与内容限制**：ZIP 包必须包含 `SKILL.md`，且其 Front Matter 至少含 `name` 和 `description`；文件名编码仅支持 UTF-8 或 GBK；`SKILL.md` 中的 `name` 不得与官方或同空间其他自定义 Skill 重名。
- **行为差异**：调用工具接口（`/tools/call`）在工具自身执行出错时，可能返回 HTTP 200 + `data.isError=true`，而非 HTTP 错误码，需业务层主动检查该字段。

## 来源文档

- [认证](../../raw/application-api-reference/overview/authentication.md)
- [MCP API 错误码](../../raw/application-api-reference/overview/errors.md)
- [服务管理](../../raw/application-api-reference/overview/overview.md)
- [查询 MCP 列表](../../raw/application-api-reference/overview/overview/list.md)
- [创建自定义 MCP](../../raw/application-api-reference/overview/overview/create.md)
- [查询 MCP 详情](../../raw/application-api-reference/overview/overview/get.md)
- [更新自定义 MCP](../../raw/application-api-reference/overview/overview/update.md)
- [删除自定义 MCP](../../raw/application-api-reference/overview/overview/delete.md)
- [工具](../../raw/application-api-reference/overview/overview.md)
- [查询工具列表](../../raw/application-api-reference/overview/overview/list.md)
- [调用工具](../../raw/application-api-reference/overview/overview/call.md)
- [推荐工具](../../raw/application-api-reference/overview/overview/recommend.md)
- [生命周期](../../raw/application-api-reference/overview/overview.md)
- [关闭官方 MCP](../../raw/application-api-reference/overview/overview/deactivate.md)
- [开通官方 MCP](../../raw/application-api-reference/overview/overview/activate.md)
- [启用自定义 MCP](../../raw/application-api-reference/overview/overview/enable.md)
- [停用自定义 MCP](../../raw/application-api-reference/overview/overview/disable.md)
- [Skill API 认证](../../raw/application-api-reference/overview/authentication.md)
- [Skill API 错误码](../../raw/application-api-reference/overview/errors.md)
- [Skill 管理](../../raw/application-api-reference/overview/overview.md)
- [创建 Skill](../../raw/application-api-reference/overview/overview/create.md)
- [获取 Skill](../../raw/application-api-reference/overview/overview/get.md)
- [列出 Skill](../../raw/application-api-reference/overview/overview/list.md)
- [删除 Skill](../../raw/application-api-reference/overview/overview/delete.md)
- [创建版本](../../raw/application-api-reference/overview/overview/create.md)
- [版本管理](../../raw/application-api-reference/overview/overview.md)
- [列出版本](../../raw/application-api-reference/overview/overview/list.md)
- [获取版本详情](../../raw/application-api-reference/overview/overview/get.md)
- [下载版本 ZIP](../../raw/application-api-reference/overview/overview/download.md)


