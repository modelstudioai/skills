# sandbox api

Sandbox API 是阿里云百炼提供的沙箱环境生命周期管理接口，兼容 E2B 协议，支持沙箱实例与模版的创建、查询、启停和释放，并提供文件挂载能力。所有请求需通过阿里云百炼 API Key 鉴权，经百炼 AI 网关转发至管控面。开发者可直接调用 REST 接口，或使用 E2B 官方 SDK（需注意鉴权适配）[概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)。

## 支持的模型/功能

- **沙箱实例管理**：支持创建、列举、获取、连接、暂停、恢复和释放实例，状态包括 `running`、`paused` 等；连接后返回 `envdAccessToken` 和 `domain` 用于数据面通信。
- **沙箱模版管理**：支持创建、列举、获取、更新、查询构建状态及删除模版；模版构建状态需为 `ready` 后方可创建实例；更新模版会触发新版本构建并递增 `version` 字段 [更新模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-update.md)。
- **文件挂载**：仅支持通过 `source=sandbox_template` 上传且 `status=available` 的文件，挂载路径必须以 `/home/user/workspace/uploads/` 开头；`.yaml` 允许上传，而 `.csv`、`.yml`、`.sh`、`.whl`、`.tar.gz`、`.ts` 等明确不支持 [概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)。
- **网络与环境配置**：模版和实例均支持 `allowOut`/`denyOut` 出口规则（域名仅在 `allowOut` 中有效）、环境变量 `envVars`/`envConfig`，以及生命周期策略（如 `on_timeout: pause` 或 `maxRunningTimeout` 自动释放）。

> **注意**：文档中关于模版创建路径存在不一致——[创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md) 明确声明主路径为 `POST /v3/templates`（兼容 `POST /templates`），但[概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md) 的表格中模版创建路径误写为 `POST /v3/templates`（正确），而实例创建路径 `POST /sandboxes` 与文档 5 一致，无矛盾。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `Authorization` | Header | string | 是 | `Bearer <your-api-key>`，API Key 从[百炼控制台](https://bailian.console.aliyun.com/?tab=model#/api-key)获取 [认证](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md) |
| `templateID` | 请求体（创建实例）/路径（模版操作） | string | 是 | 模版唯一标识，需已构建完成（`buildStatus=ready`） |
| `sandboxID` | 路径 | string | 是 | 实例唯一 ID，格式如 `sbx-xxx`，由创建接口返回 |
| `mntConfig` | 请求体（创建/更新模版） | array<object> | 否 | 挂载配置，`originFileId` 必须指向 `source=sandbox_template` 且 `status=available` 的文件 |
| `timeout` / `maxRunningTimeout` | 请求体 | integer | 否 | 单位秒，取值范围 `[300, 604800]`（5 分钟至 7 天）；`maxRunningTimeout` 优先级高于 `autoPauseTime` |

## 使用方式

1. **前置准备**  
   - 开通百炼服务，创建 API Key；  
   - 在百炼控制台完成 SLR 服务授权（首次使用必需）；  
   - 获取工作空间 ID（右上角下拉菜单）和地域 ID（当前仅支持 `cn-beijing`）。

2. **Endpoint 拼装**  
   基地址为：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox`

3. **典型流程**  
   - **上传文件** → `POST /api/v1/agentstudio/files`（带 `source=sandbox_template`）→ 轮询至 `status=available`；  
   - **创建模版** → `POST /v3/templates`（含 `mntConfig` 引用已上传文件）→ 记录 `buildID`；  
   - **等待构建就绪** → `GET /templates/{templateID}/builds/{buildID}/status` → 确认 `status=ready`；  
   - **创建实例** → `POST /sandboxes`（传 `templateID` 及 `timeout` 等）→ 获取 `sandboxID`；  
   - **连接实例** → `POST /sandboxes/{sandboxID}/connect` → 获取 `envdAccessToken` 和 `domain` 用于后续数据面调用。

4. **SDK 使用**  
   可使用 E2B 官方 SDK，但需注意：SDK 所需的 `api_key` 仅用于协议占位，实际鉴权仍依赖 HTTP Header 中的 `Authorization: Bearer <your-api-key>`，推荐填入 `e2b_${ALIYUN_UID}`。

## 限制和注意事项

- **地域限制**：当前仅支持 `cn-beijing` 地域，Endpoint 中 `region` 固定为此值。
- **文件限制**：单文件 ≤ 50 MB，工作空间总容量 ≤ 100 GB，保存时效 30 天；不支持扩展名 `.csv`、`.yml`、`.sh`、`.whl`、`.tar.gz`、`.ts`。
- **模版删除约束**：若模版关联任何 `running` 或 `paused` 实例，`DELETE /templates/{templateCode}` 将返回 409 错误，需先调用 `DELETE /sandboxes/{sandboxID}` 释放所有实例。
- **错误处理**：兼容 E2B 协议的接口不封装为百炼统一 `Result<T>` 结构，错误响应直接返回 `{code, message, requestID}`；常见状态码：400（参数错误）、401（API Key 无效）、404（资源不存在）、409（状态冲突）、415（文件类型不支持）[错误码](../../raw/application-api-reference/sandbox-api/sandbox-api-errors.md)。
- **鉴权特殊性**：E2B SDK 的 `X-API-Key` 头不参与百炼业务鉴权，仅为协议兼容占位；真实鉴权仅依赖 `Authorization` Header。

## 来源文档

- [概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)
- [认证](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)
- [错误码](../../raw/application-api-reference/sandbox-api/sandbox-api-errors.md)
- [实例管理](../../raw/application-api-reference/sandbox-api/sandbox-api-instances.md)
- [创建实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md)
- [列举实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-list.md)
- [连接实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-connect.md)
- [暂停实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-pause.md)
- [恢复实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-resume.md)
- [释放实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-delete.md)
- [模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md)
- [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)
- [列举模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-list.md)
- [获取模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-get.md)
- [更新模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-update.md)
- [获取构建状态](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-build-status.md)
- [删除模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-delete.md)
- [获取实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-get.md)


