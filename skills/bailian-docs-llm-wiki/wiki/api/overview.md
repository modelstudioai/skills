# overview

百炼平台的 MCP（Model Calling Protocol）与 Skill（技能）能力提供了一套标准化的工具集成与版本管理机制，支持开发者将外部服务封装为可被智能体调用的工具，并对自定义 Skill 进行全生命周期管理。核心能力围绕 MCP 服务开通/启停、工具推荐与调用，以及 Skill 版本上传、查询、下载与删除展开。

## 支持的模型/功能

- **MCP 工具服务**：支持官方 MCP（如高德地图、天气等）的开通与关闭，以及自定义 MCP 的创建、更新、启用、停用；支持通过 `/tools/recommend` [推荐工具](../../raw/application-api-reference/overview/overview/recommend.md) 和 `/tools/call` 调用具体工具。
- **Skill（技能）管理**：面向自定义 Skill 提供完整的版本管理能力，包括上传新版本（`POST /versions`）、分页查询版本列表（`GET /versions`）、获取指定版本详情（`GET /versions/{version}`）及下载 ZIP 包（`GET /versions/{version}/content`）。官方 Skill 仅允许查询和下载 `active` 状态的版本。
- **统一错误处理**：所有接口遵循统一响应结构（含 `success`、`error_code`、`error_msg`、`data`、`request_id`），错误码语义明确，便于自动化排查。详见 [Skill API 错误码](../../raw/application-api-reference/overview/errors.md)。

## 关键参数

- **认证参数**：所有请求需携带 `Authorization: Bearer $DASHSCOPE_API_KEY` Header，并使用工作空间专属 Endpoint（格式为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com`）。API Key 获取方式见 [认证](../../raw/application-api-reference/overview/authentication.md)。
- **Skill 版本号**：格式为 `major.minor`（如 `1.0`），由服务端自动递增，**不可由客户端指定**；旧版本永久保留，挂载到智能体时必须显式指定版本。
- **分页参数**：`pageNo`（默认 1，最小 1）和 `pageSize`（默认 20，范围 1–100），且 `pageNo × pageSize ≤ 10000`。
- **ZIP 包限制**：上传 ZIP 需包含 `SKILL.md`（含 `name` 和 `description`），文件大小 ≤ 50MB，解压后总大小 ≤ 100MB，仅支持 UTF-8 或 GBK 文件名编码。

## 使用方式

1. **认证配置**：设置环境变量 `DASHSCOPE_API_KEY`，并确认 `workspace_id` 正确；
2. **MCP 操作**：
   - 官方 MCP：先调用 `/activate` 开通（需传入必要 `env`），再通过 `/tools/call` 调用；
   - 自定义 MCP：先 `POST /servers` 创建，再通过 `/enable` 启用，后续可 `POST /disable` 停用或 `POST /servers/{mcpCode}` 更新配置；
3. **Skill 版本操作**：
   - 上传：`POST /skills/{skill_id}/versions`，`multipart/form-data` 提交 ZIP；
   - 查询：`GET /skills/{skill_id}/versions`（列表）或 `GET /skills/{skill_id}/versions/{version}`（详情）；
   - 下载：`GET /skills/{skill_id}/versions/{version}/content` 获取临时 `file_url`；
4. **错误处理**：优先检查 HTTP 状态码（400/401/500），再解析 `error_code`；使用 `request_id` 追踪问题。

> **注意**：文档中存在多处重复内容（如 `list.md`、`get.md`、`create.md` 等被多次提交），但关键规则一致；唯一需警惕的矛盾点是：文档 7（更新自定义 MCP）要求修改 `mcp_config` 时必须同时提交 `mcp_type`，而文档 13（开通官方 MCP）示例中仅提交 `env` 即可成功——这反映两类 MCP 的配置模型本质不同，**切勿将官方 MCP 的 `env` 提交方式套用于自定义 MCP 的 `mcp_config` 更新**。

## 限制和注意事项

- **权限隔离**：官方 MCP 不可删除、不可更新配置；自定义 Skill 不可删除官方 Skill；RAM 子账号需显式授权。
- **状态约束**：
  - Skill 在 `checking`（安全扫描中）状态时，禁止创建新版本；
  - 自定义 MCP 在运行中或部署中时，禁止更新配置或启停；
  - One Key MCP（如部分云市场服务）不支持关闭（`/deactivate` 返回 `DeActivateFailed`）。
- **安全与合规**：上传 ZIP 必须通过安全扫描（`checking` → `active` 或 `rejected`），失败时 `additional_properties.error_info` 提供具体违规位置；`SKILL.md` 的 `name` 不得与官方或同空间其他自定义 Skill 重名。
- **资源限制**：单次 ZIP 上传上限 50MB；分页总数上限 10000 条；下载 URL 有效期仅 2 小时。

## 来源文档

- [MCP API 错误码](../../raw/application-api-reference/overview/errors.md)
- [认证](../../raw/application-api-reference/overview/authentication.md)
- [创建自定义 MCP](../../raw/application-api-reference/overview/overview/create.md)
- [查询 MCP 列表](../../raw/application-api-reference/overview/overview/list.md)
- [服务管理](../../raw/application-api-reference/overview/overview.md)
- [查询 MCP 详情](../../raw/application-api-reference/overview/overview/get.md)
- [更新自定义 MCP](../../raw/application-api-reference/overview/overview/update.md)
- [查询工具列表](../../raw/application-api-reference/overview/overview/list.md)
- [工具](../../raw/application-api-reference/overview/overview.md)
- [删除自定义 MCP](../../raw/application-api-reference/overview/overview/delete.md)
- [生命周期](../../raw/application-api-reference/overview/overview.md)
- [推荐工具](../../raw/application-api-reference/overview/overview/recommend.md)
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
- [版本管理](../../raw/application-api-reference/overview/overview.md)
- [创建版本](../../raw/application-api-reference/overview/overview/create.md)
- [列出版本](../../raw/application-api-reference/overview/overview/list.md)
- [获取版本详情](../../raw/application-api-reference/overview/overview/get.md)
- [下载版本 ZIP](../../raw/application-api-reference/overview/overview/download.md)
- [调用工具](../../raw/application-api-reference/overview/overview/call.md)


