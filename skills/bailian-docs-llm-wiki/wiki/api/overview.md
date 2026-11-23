# overview

百炼平台的 MCP（Model Calling Protocol）与 Skill 两大能力体系，为开发者提供标准化的模型服务集成与可复用技能管理能力。MCP 用于接入和编排外部工具服务，Skill 用于封装和分发可复用的业务逻辑模块。二者均通过统一的 API Key 鉴权、工作空间 Endpoint 访问，并具备完整的生命周期管理与错误处理机制。

## 支持的模型/功能

- **MCP 服务**：支持四种接入类型：`STDIO`（本地进程）、`HTTP`（RESTful 接口）、`SSE`（服务端事件流）和 `OPENAPI`（OpenAPI 规范描述的工具集）。官方 MCP（如高德地图、天气等）需开通后使用；自定义 MCP 可由用户自主创建、配置并部署 [创建自定义 MCP](../../raw/application-api-reference/overview/overview/create-a29c49f8a08e5095.md)。
- **Skill 技能**：支持 ZIP 包形式上传的自定义 Skill，包内必须包含 `SKILL.md`（含 `name` 和 `description`），最大体积 50MB（解压后 ≤100MB）[创建 Skill](../../raw/application-api-reference/overview/overview/create-44cf2cde0a7d9a72.md)。Skill 支持多版本管理，每个版本独立安全扫描与状态（`checking`/`active`/`rejected`），挂载到智能体时需指定具体版本。

## 关键参数

- **认证参数**：全局使用 `DASHSCOPE_API_KEY` 环境变量或 `Authorization: Bearer <key>` Header；Endpoint 中的 `{workspace_id}` 须从控制台右上角复制，不可省略。
- **分页参数**：`pageNo`（≥1）与 `pageSize`（1–100），二者乘积不得超过 10000，适用于 MCP 列表、Skill 列表及版本列表等接口。
- **MCP 配置参数**：`mcp_type` 与 `mcp_config` 必须同时提交才能触发重新部署；`mcp_config` 中 `url`/`api_host` 不得含凭据、`#` 片段或反斜杠；`headers` 值禁止含 CR/LF 字符。
- **Skill 版本参数**：版本号（如 `1.0`）由服务端自动递增，不可手动指定；`display_name` 和 `display_description` 可在创建 Skill 或新版本时覆盖 `SKILL.md` 中的值。

## 使用方式

- **MCP 流程**：先通过 [查询 MCP 列表](../../raw/application-api-reference/overview/overview/list-c680a6eef36ba755.md) 发现可用服务；对官方 MCP 调用 `/activate` 开通，对自定义 MCP 调用 `/create` 部署；再通过 `/tools` 查询工具列表，最后用 `/tools/call` 执行调用；也可用 `/tools/recommend` 根据自然语言需求推荐工具。
- **Skill 流程**：通过 `POST /skills` 创建 Skill，再用 `POST /skills/{id}/versions` 上传新版本；通过 `GET /skills/{id}/versions` 查看版本状态，用 `GET /skills/{id}/versions/{v}/content` 获取 ZIP 下载地址；最终在智能体配置中通过 `skills` 字段挂载指定 Skill ID 与版本。
- **通用调试**：所有请求响应头均含 `X-Request-Id`，用于问题定位；务必同时检查 HTTP 状态码与响应体中的 `success` 字段及 `data.isError`（尤其在工具调用中）。

> **注意**：MCP 的 `/list` 接口默认返回官方 + 当前工作空间自定义 MCP，而 Skill 的 `/skills` 列表接口不传 `type` 参数时也返回两类混合结果，但其 `total` 字段为合计值，与 MCP 的分页限制逻辑一致；然而，[查询 MCP 详情](../../raw/application-api-reference/overview/overview/get-b57e1839b6840677.md) 明确指出 `mcp_config.headers` 可能返回敏感信息（如 API Key），而 Skill 相关接口无此风险提示——开发者需在日志或存储中主动过滤 `mcp_config` 敏感字段。

## 限制和注意事项

- **权限与范围**：API Key 具有工作空间级权限，RAM 子账号需显式授权；官方 MCP 不支持删除或修改配置；One Key 类型 MCP 不支持关闭，且首次调用可能自动开通并产生费用。
- **状态依赖**：修改自定义 MCP 配置前必须先停用（`/disable`），否则返回 `400 OperationNotSupported`；Skill 在 `checking` 状态时无法创建新版本，需等待扫描完成。
- **错误处理差异**：MCP API 错误码中 `403 AccessDenied` 表示鉴权失败，而 Skill API 对应错误为 `401 WORKSPACE_ID_ILLEGAL`；两者虽都源于认证环节，但状态码与错误码命名不一致，需分别查阅 [MCP API 错误码](../../raw/application-api-reference/overview/errors-972b4127b84f4429.md) 和 [Skill API 错误码](../../raw/application-api-reference/overview/errors-9f5f81ed72f2a1c6.md) 进行适配。
- **数据一致性**：Skill 列表接口返回的数据为异步更新，新建/删除/状态变更后可能存在短暂延迟；权威状态应以 `GET /skills/{id}` 单点查询结果为准。

## 来源文档

- [认证](../../raw/application-api-reference/overview/authentication-58370587ddc046ee.md)
- [MCP API 错误码](../../raw/application-api-reference/overview/errors-972b4127b84f4429.md)
- [服务管理](../../raw/application-api-reference/overview/overview-448e7f104037b903.md)
- [查询 MCP 列表](../../raw/application-api-reference/overview/overview/list-c680a6eef36ba755.md)
- [创建自定义 MCP](../../raw/application-api-reference/overview/overview/create-a29c49f8a08e5095.md)
- [更新自定义 MCP](../../raw/application-api-reference/overview/overview/update.md)
- [删除自定义 MCP](../../raw/application-api-reference/overview/overview/delete-23f946e3aa963ba8.md)
- [工具](../../raw/application-api-reference/overview/overview-743a72f61b3a54f8.md)
- [查询工具列表](../../raw/application-api-reference/overview/overview/list-64eddd50625ee03f.md)
- [调用工具](../../raw/application-api-reference/overview/overview/call.md)
- [推荐工具](../../raw/application-api-reference/overview/overview/recommend.md)
- [开通官方 MCP](../../raw/application-api-reference/overview/overview/activate.md)
- [关闭官方 MCP](../../raw/application-api-reference/overview/overview/deactivate.md)
- [停用自定义 MCP](../../raw/application-api-reference/overview/overview/disable.md)
- [启用自定义 MCP](../../raw/application-api-reference/overview/overview/enable.md)
- [Skill API 认证](../../raw/application-api-reference/overview/authentication-26822a11844efd00.md)
- [Skill API 错误码](../../raw/application-api-reference/overview/errors-9f5f81ed72f2a1c6.md)
- [Skill 管理](../../raw/application-api-reference/overview/overview-9d8edaa0d219d019.md)
- [创建 Skill](../../raw/application-api-reference/overview/overview/create-44cf2cde0a7d9a72.md)
- [查询 MCP 详情](../../raw/application-api-reference/overview/overview/get-b57e1839b6840677.md)
- [列出 Skill](../../raw/application-api-reference/overview/overview/list-b23c792b7a3bf72b.md)
- [获取 Skill](../../raw/application-api-reference/overview/overview/get-9c06b4218676761a.md)
- [删除 Skill](../../raw/application-api-reference/overview/overview/delete-75ffff308650522a.md)
- [版本管理](../../raw/application-api-reference/overview/overview-1dac56b965dd0271.md)
- [列出版本](../../raw/application-api-reference/overview/overview/list-ee346a0747aae1d4.md)
- [创建版本](../../raw/application-api-reference/overview/overview/create-66b335d7c24c1f0f.md)
- [获取版本详情](../../raw/application-api-reference/overview/overview/get-2856ed31dd1c9b3d.md)
- [下载版本 ZIP](../../raw/application-api-reference/overview/overview/download.md)
- [生命周期](../../raw/application-api-reference/overview/overview-fc1e2b9f062d93f5.md)


