# sandbox api

Sandbox API 是阿里云百炼提供的沙箱环境生命周期管理接口，兼容 E2B 协议，支持沙箱实例与模版的创建、查询、暂停/恢复、释放等操作。所有请求需通过阿里云百炼 [API Key 鉴权](../concepts/api-key-authentication.md)，并经由工作空间专属 Endpoint 转发。管控面能力（如模版构建、文件挂载）与数据面访问（如 envd 连接）职责分离，开发者需按阶段分步调用。

## 支持的模型/功能

- **沙箱实例管理**：支持基于模版创建、列举、获取、连接、暂停、恢复和释放实例；实例状态包括 `running`、`paused`，不支持 `stopped` 等中间态。
- **沙箱模版管理**：支持创建、列举、获取、更新、查询构建状态及删除模版；模版构建状态需轮询 `/templates/{templateCode}/builds/{buildID}/status` 确认是否为 `ready` 后方可创建实例 [获取构建状态](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-build-status.md)。
- **文件挂载能力**：仅支持通过 `source=sandbox_template` 上传且 `status=available` 的文件挂载至模版（`mntConfig`），路径必须以 `/home/user/workspace/uploads/` 开头；`.csv`、`.yml`、`.sh`、`.whl`、`.tar.gz`、`.ts` 等扩展名明确不被支持 [概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)。
- **网络与生命周期配置**：支持出口白名单/黑名单（`allowOut`/`denyOut`）、公网访问开关（`allow_internet_access`）、超时自动暂停（`autoPauseTime`）与最大运行时限（`maxRunningTimeout`）；注意 `denyOut` 不支持域名，仅支持 IPv4/IPv6/CIDR [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)。

> **注意**：文档中关于 `networkConfig.denyOut` 的说明存在矛盾——[创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md) 明确指出“仅支持 IPv4、IPv6 和 CIDR，不支持域名”，但 [获取实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-get.md) 的响应示例中 `denyOut` 字段值为 `["10.0.0.0/8"]`（符合限制），而部分 SDK 文档未同步该约束。请以创建/更新模版接口的实际校验逻辑为准。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `Authorization` | Header | string | 是 | `Bearer <your-api-key>`，API Key 从[百炼控制台](https://bailian.console.aliyun.com/?tab=model#/api-key)获取 [认证](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md) |
| `workspace_id` | Endpoint | string | 是 | 工作空间 ID，控制台右上角下拉菜单查看；Endpoint 格式为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox` |
| `templateID` | 请求体 / 路径 | string | 是（创建实例） | 模版唯一 ID，需确保其 `buildStatus` 为 `ready`，否则创建实例返回 409 |
| `timeout` | 请求体 | integer | 否 | 实例或连接超时时间（秒），范围 `[300, 604800]`；`maxRunningTimeout` 优先生效于 `autoPauseTime` |
| `mntConfig` | 请求体 | array<object> | 否 | 文件挂载配置，`originFileId` 必须为 `source=sandbox_template` 且 `status=available` 的文件 ID |

## 使用方式

1. **前置准备**：完成 SLR 服务授权（见[快速开始](../../raw/application-user-guide/agent-development/sandbox/sandbox-start-using/sandbox-quick-start.md)），获取 `workspace_id` 与 API Key；
2. **上传文件（可选）**：若需挂载文件，先调用 `POST /api/v1/agentstudio/files` 并指定 `source=sandbox_template`，轮询至 `status=available`；
3. **创建模版**：调用 `POST /v3/templates`，传入 `cpuCount`/`memoryMB`（需匹配平台规格组合）、`envConfig`、`networkConfig` 等，获取 `templateID` 与 `buildID`；
4. **等待构建就绪**：轮询 `GET /templates/{templateID}/builds/{buildID}/status`，直到 `status=ready`；
5. **创建实例**：调用 `POST /sandboxes`，传入 `templateID` 及 `timeout`、`allow_internet_access` 等配置；
6. **连接与管理**：使用 `GET /sandboxes/{sandboxID}` 查看详情，`POST /sandboxes/{sandboxID}/connect` 获取数据面 token，`POST /sandboxes/{sandboxID}/pause` 暂停等。

> **注意**：E2B SDK 可直接接入，但 SDK 中的 `X-API-Key` 或 `api_key` 仅用于协议占位，**实际鉴权仍依赖 HTTP Header 中的 `Authorization: Bearer <your-api-key>`**；推荐 SDK 填写 `e2b_${ALIYUN_UID}` [认证](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)。

## 限制和注意事项

- **地域限制**：当前仅支持 `cn-beijing` 地域，Endpoint 中 `region` 固定为此值；
- **文件限制**：单文件 ≤ 50 MB，工作空间总容量 ≤ 100 GB，保存时效 30 天；上传失败错误码详见 [错误码](../../raw/application-api-reference/sandbox-api/sandbox-api-errors.md)；
- **实例生命周期**：`timeout` 到期后行为由 `lifecycle.on_timeout` 控制（如 `pause`），`autoResume` 决定连接时是否自动恢复；`maxRunningTimeout` 到期将强制释放实例；
- **模版更新**：`PUT /templates/{templateCode}` 会触发新版本构建，`version` 递增，但旧版本实例不受影响；更新时若 `mntConfig` 中引用了已失效文件 ID，将校验失败；
- **错误处理**：兼容 E2B 协议的接口不返回统一 `Result<T>` 结构，错误响应格式贴近 E2B 原生定义（如 `code`/`message`），HTTP 状态码语义需对照 [错误码](../../raw/application-api-reference/sandbox-api/sandbox-api-errors.md) 解析；
- **资源规格**：`cpuCount` 与 `memoryMB` 必须同时传递且匹配平台预设组合（如 1C2G、4C8G），单独修改任一字段将被拒绝。

## 来源文档

- [概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)
- [认证](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)
- [错误码](../../raw/application-api-reference/sandbox-api/sandbox-api-errors.md)
- [创建实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md)
- [实例管理](../../raw/application-api-reference/sandbox-api/sandbox-api-instances.md)
- [获取实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-get.md)
- [连接实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-connect.md)
- [列举实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-list.md)
- [释放实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-delete.md)
- [暂停实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-pause.md)
- [恢复实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-resume.md)
- [模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md)
- [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)
- [列举模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-list.md)
- [更新模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-update.md)
- [获取模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-get.md)
- [获取构建状态](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-build-status.md)
- [删除模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-delete.md)


