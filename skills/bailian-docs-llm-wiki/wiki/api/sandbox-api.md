# sandbox api

Sandbox API 是阿里云百炼提供的沙箱环境生命周期管理接口，兼容 E2B 协议，支持沙箱实例与模版的创建、查询、启停及销毁。所有请求需通过阿里云百炼 API Key 鉴权，并经由工作空间专属 Endpoint 转发。管控面能力（如模版构建、文件挂载）与数据面访问（如 `envdAccessToken`）分离，开发者需按阶段分步调用。

## 支持的模型/功能

- **沙箱实例管理**：支持创建、列举、获取详情、连接、暂停、恢复和释放实例，全部兼容 E2B 协议语义（如 `connect()`、`pause()`、`kill()`），详见 [创建实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md) 和 [释放实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-delete.md)。
- **沙箱模版管理**：支持创建、列举、获取、更新、查询构建状态及删除模版；其中更新模版为阿里云百炼扩展协议（非完全兼容 E2B v2），每次更新触发新版本构建并递增 `version` 字段，详见 [更新模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-update.md)。
- **文件挂载能力**：仅支持通过 `source=sandbox_template` 上传的文件（且 `status=available`）挂载至模版，`mntConfig.mountPath` 必须以 `/home/user/workspace/uploads/` 开头；不支持 `.csv`、`.yml`、`.sh`、`.whl`、`.tar.gz`、`.ts` 等扩展名，详见 [概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md) 中的文件限制说明。
- **网络与生命周期配置**：实例级支持 `allow_internet_access`、`network.allowOut/denyOut`；模版级支持 `autoPauseTime` 与 `maxRunningTimeout`（后者优先生效），详见 [创建实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md) 和 [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)。

> **注意**：文档中 `GET /sandboxes`（实例列举）与 `GET /templates`（模版列举）被标记为“兼容路由”，但主推路径分别为 `/v2/sandboxes` 和 `/v2/templates`；实际使用应优先采用带版本号的路径，避免未来兼容性风险。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `Authorization` | Header | string | 是 | `Bearer <your-api-key>`，API Key 来自百炼控制台，详见 [认证](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md) |
| `workspace_id` | Endpoint | string | 是 | 工作空间 ID，控制台右上角下拉菜单获取；Endpoint 格式为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox` |
| `templateID` | Body (创建实例) / Path (获取模版) | string | 是 | 模版唯一标识，必须已构建完成（`buildStatus=ready`），否则创建实例返回 409 |
| `sandboxID` | Path | string | 是 | 实例唯一 ID，由创建接口返回，用于后续所有实例操作 |
| `originFileId` | `mntConfig` 数组元素 | string | 是（当传 `mntConfig`） | 文件 ID，需先通过文件上传接口上传且 `status=available`，详见 [概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md) |
| `timeout` | Body (创建/恢复/连接) | integer | 否 | 取值范围 `[300, 604800]`（5 分钟至 7 天），单位秒；超时后行为由 `lifecycle.on_timeout` 或 `autoPause` 控制 |

## 使用方式

1. **前置准备**：开通百炼服务 → 创建 API Key → 完成 SLR 授权（见[快速开始](../../raw/application-user-guide/agent-development/sandbox/sandbox-start-using/sandbox-quick-start.md)）→ 获取 `workspace_id`。
2. **上传文件（可选）**：若需挂载文件，先调用 `POST /api/v1/agentstudio/files` 并指定 `source=sandbox_template`，轮询至 `status=available`。
3. **创建模版**：调用 `POST /v3/templates`，传入 `cpuCount`/`memoryMB`（需匹配平台规格）、`mntConfig` 等；获取 `templateID` 与 `buildID`。
4. **等待构建就绪**：调用 `GET /templates/{templateID}/builds/{buildID}/status`，直至 `status=ready`。
5. **创建实例**：调用 `POST /sandboxes`，传入 `templateID` 及可选 `timeout`、`allow_internet_access` 等。
6. **连接与操作**：调用 `POST /sandboxes/{sandboxID}/connect` 获取 `domain` 与 `envdAccessToken`；调用 `POST /sandboxes/{sandboxID}/pause` 或 `POST /sandboxes/{sandboxID}/resume` 控制状态；最后调用 `DELETE /sandboxes/{sandboxID}` 释放资源。

> **注意**：E2B SDK 可直接接入（如 `e2b.connect()`），但 SDK 的 `api_key` 参数仅用于协议占位，**实际鉴权仍依赖 HTTP Header 中的 `Authorization: Bearer <your-api-key>`**，详见 [认证](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)。

## 限制和注意事项

- **地域限制**：当前仅支持 `cn-beijing` 地域，Endpoint 中 `region` 固定为此值。
- **文件限制**：单文件 ≤ 50 MB，工作空间总容量 ≤ 100 GB，保存时效 30 天；扩展名校验严格，`.yaml` 可传，`.yml` 不可传（见 [概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)）。
- **模版删除约束**：若模版关联任何运行中或暂停中的实例，`DELETE /templates/{templateCode}` 返回 409，必须先释放所有实例。
- **错误处理**：兼容 E2B 原生错误结构（非阿里云统一 `Result<T>`），HTTP 状态码含义需结合 [错误码](../../raw/application-api-reference/sandbox-api/sandbox-api-errors.md) 文档理解；例如 `415 Unsupported Media Type` 可能由文件类型不被允许（code `11900014`）或 multipart 请求体超限（`RequestEntityTooLarge`）导致。
- **SDK 兼容性提示**：使用 E2B SDK 时，`connect()` 返回的 `domain` 和 `envdAccessToken` 可直接用于数据面调用，但管控面操作（如创建模版、列举实例）仍需调用百炼原生 REST 接口。

## 来源文档

- [概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)
- [认证](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)
- [错误码](../../raw/application-api-reference/sandbox-api/sandbox-api-errors.md)
- [实例管理](../../raw/application-api-reference/sandbox-api/sandbox-api-instances.md)
- [创建实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md)
- [列举实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-list.md)
- [连接实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-connect.md)
- [获取实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-get.md)
- [暂停实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-pause.md)
- [恢复实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-resume.md)
- [模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md)
- [释放实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-delete.md)
- [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)
- [列举模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-list.md)
- [获取模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-get.md)
- [获取构建状态](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-build-status.md)
- [删除模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-delete.md)
- [更新模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-update.md)


