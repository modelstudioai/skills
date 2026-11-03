# sandbox api

Sandbox API 是阿里云百炼提供的沙箱环境生命周期管理服务，兼容 E2B 协议，支持沙箱实例与模版的创建、查询、启停和释放。它通过统一的 HTTP 接口暴露管控面能力，并经由百炼 AI 网关转发。开发者需完成工作空间授权、API Key 配置及文件上传等前置步骤后方可使用。

## 支持的模型/功能

- **沙箱实例管理**：支持创建（`POST /sandboxes`）、列举（`GET /v2/sandboxes`）、获取详情（`GET /sandboxes/{sandboxID}`）、连接（`POST /sandboxes/{sandboxID}/connect`）、暂停（`POST /sandboxes/{sandboxID}/pause`）、恢复（`POST /sandboxes/{sandboxID}/resume`）和释放（`DELETE /sandboxes/{sandboxID}`）等全生命周期操作，详见[实例管理](raw/application-api-reference/sandbox-api/sandbox-api-instances.md)。
- **沙箱模版管理**：支持创建（`POST /v3/templates`）、列举（`GET /v2/templates`）、获取（`GET /templates/{templateCode}`）、更新（`PUT /templates/{templateCode}`）、查询构建状态（`GET /templates/{templateCode}/builds/{buildID}/status`）和删除（`DELETE /templates/{templateCode}`），其中更新接口为阿里云百炼扩展协议，不完全兼容 E2B v2 [更新模版](raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-update.md)。
- **文件挂载能力**：仅支持通过 `source=sandbox_template` 上传并处于 `available` 状态的文件，挂载路径必须以 `/home/user/workspace/uploads/` 开头；不支持 `.csv`、`.yml`、`.sh`、`.whl`、`.tar.gz` 等扩展名，具体限制见[文件上传](raw/application-api-reference/sandbox-api/sandbox-api-overview.md)章节。

> **注意**：文档中 `mntConfig.mountPath` 的路径约束存在不一致说明——[创建模版](raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md) 和 [更新模版](raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-update.md) 均强调“路径不在该目录下时接口接受配置但实例中不会出现文件”，而[概览](raw/application-api-reference/sandbox-api/sandbox-api-overview.md)仅要求“必须以 `/home/user/workspace/uploads/` 开头”。实践中应严格遵循前两者，使用完整文件路径（如 `/home/user/workspace/uploads/config.json`）以确保挂载生效。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `templateID` | 请求体（创建实例）/路径（获取/更新模版） | string | 是 | 已构建完成（`status=ready`）的模版 ID；模版未就绪时创建实例返回 409 |
| `sandboxID` | 路径 | string | 是 | 实例唯一标识，由创建接口返回，用于所有实例级操作 |
| `timeout` | 请求体（创建/连接/恢复实例） | integer | 否 | 生命周期超时时间，单位秒，范围 `[300, 604800]`；到期行为由 `lifecycle.on_timeout` 或 `autoPause` 控制 |
| `allow_internet_access` | 请求体（创建实例） | boolean | 否 | 是否允许公网访问，默认 `false`；与 `network.allowPublicTraffic` 语义一致 |
| `mntConfig` | 请求体（创建/更新模版） | array<object> | 否 | 文件挂载配置，每个元素含 `originFileId`（必填，需已上传且 `status=available`）、`mountPath`（必填，须以 `/home/user/workspace/uploads/` 开头） |
| `cpuCount` / `memoryMB` | 请求体（创建/更新模版） | integer | 是（创建时）/ 否（更新时，但需同时传） | 必须匹配平台预设规格组合，不支持任意值 |

## 使用方式

1. **前置准备**  
   - 开通百炼服务，[创建 API Key](raw/application-api-reference/sandbox-api/sandbox-api-authentication.md) 并完成 SLR 授权（参见[快速开始](raw/application-user-guide/agent-development/sandbox/sandbox-start-using/sandbox-quick-start.md)）；  
   - 获取工作空间 ID（控制台右上角下拉菜单）；  
   - 构造 Endpoint：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox`（当前仅支持 `cn-beijing` 地域）。

2. **文件上传（如需挂载）**  
   - 使用 `POST /api/v1/agentstudio/files` 上传文件，**必须指定 `source=sandbox_template`**；  
   - 轮询 `GET /api/v1/agentstudio/files/{file_id}`，待 `status` 变为 `available` 后，方可将其 `id` 填入 `mntConfig.originFileId`。

3. **模版构建**  
   - 调用 `POST /v3/templates` 创建模版，获取 `templateID` 和 `buildID`；  
   - 轮询 `GET /templates/{templateID}/builds/{buildID}/status`，确认 `status=ready` 后方可创建实例。

4. **实例操作**  
   - 创建实例后，使用 `POST /sandboxes/{sandboxID}/connect` 获取数据面访问凭证（`domain` + `envdAccessToken`）；  
   - 暂停/恢复实例无需额外参数，直接调用对应路径即可；  
   - 释放实例使用 `DELETE /sandboxes/{sandboxID}`，成功返回 204。

## 限制和注意事项

- **地域限制**：当前仅支持 `cn-beijing` 地域，Endpoint 中 `region` 固定为此值。
- **文件限制**：单文件 ≤ 50 MB，工作空间总容量 ≤ 100 GB，保存时效 30 天；扩展名校验严格，`.yaml` 可上传，`.yml`、`.csv`、`.sh` 等明确不支持。
- **模版删除约束**：若模版关联任何运行中或暂停中的实例，`DELETE /templates/{templateCode}` 将返回 409 错误，需先释放所有实例。
- **鉴权特殊性**：E2B SDK 中的 `X-API-Key` 仅用于协议兼容，**实际业务鉴权依赖阿里云百炼 API Key**（`Authorization: Bearer <your-api-key>`），详见[认证](raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)。
- **错误处理**：HTTP 状态码含义与通用 REST 规范一致（如 400 参数错误、401 认证失败、404 资源不存在、409 状态冲突）；文件类错误码（如 `11900014` 表示类型不被允许）详见[错误码](raw/application-api-reference/sandbox-api/sandbox-api-errors.md)。

## 来源文档

- [概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)
- [错误码](../../raw/application-api-reference/sandbox-api/sandbox-api-errors.md)
- [认证](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)
- [创建实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md)
- [实例管理](../../raw/application-api-reference/sandbox-api/sandbox-api-instances.md)
- [获取实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-get.md)
- [连接实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-connect.md)
- [暂停实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-pause.md)
- [恢复实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-resume.md)
- [模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md)
- [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)
- [列举模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-list.md)
- [获取模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-get.md)
- [更新模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-update.md)
- [获取构建状态](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-build-status.md)
- [删除模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-delete.md)
- [列举实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-list.md)
- [释放实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-delete.md)


