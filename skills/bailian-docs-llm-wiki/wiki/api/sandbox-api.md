# sandbox api

Sandbox API 是阿里云百炼提供的沙箱环境管控面接口，基于 E2B 协议兼容设计，支持沙箱实例与模版的全生命周期管理、文件挂载及网络/资源配置。所有请求需通过阿里云百炼 AI 网关转发，使用统一的 API Key 鉴权，并按工作空间与地域拼装 Endpoint。开发者可直接调用 REST 接口，也可复用 E2B 官方 SDK（需注意鉴权适配）[原文标题](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)。

## 支持的模型/功能

Sandbox API 不提供“模型”概念，而是提供**沙箱模版（Template）** 作为可复用的运行环境定义，其底层基于预置或自定义容器镜像构建。当前支持以下官方基础镜像（通过 `fromImage` 指定）：
- `code-interpreter-v1`（默认）
- `browser`
- `all-in-one`

模版支持配置 CPU（vCPU）、内存（MB）、环境变量、网络规则（白/黑名单）、文件挂载（`mntConfig`）及生命周期策略（`autoPauseTime` / `maxRunningTimeout`）。实例基于就绪（`status=ready`）的模版创建，支持 `running` / `paused` 状态切换，并保留内存与文件系统状态 [原文标题](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)。  
> **注意**：文档 13 明确要求 `cpuCount` 与 `memoryMB` 必须同时传递且匹配平台规格组合；而文档 15 的更新接口允许单独传入任一字段（未传则保留原值），二者逻辑不一致。实际调用时，**更新模版必须同时指定 `cpuCount` 和 `memoryMB`**，否则可能触发校验失败。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `Authorization` | Header | string | 是 | `Bearer <your-api-key>`，API Key 从[百炼控制台](https://bailian.console.aliyun.com/?tab=model#/api-key)获取 [原文标题](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md) |
| `workspace_id` | Endpoint | string | 是 | 工作空间 ID，控制台右上角下拉菜单查看 |
| `region` | Endpoint | string | 是 | 当前仅支持 `cn-beijing` |
| `templateID` | Body (创建实例) / Path (其他) | string | 是 | 模版唯一标识，创建实例前需确保其 `buildStatus=ready` |
| `sandboxID` | Path | string | 是 | 实例唯一 ID，由创建接口返回 |
| `originFileId` | `mntConfig` item | string | 是 | 文件上传后返回的 `id`，且 `source=sandbox_template`、`status=available` |
| `mountPath` | `mntConfig` item | string | 是 | 必须以 `/home/user/workspace/uploads/` 开头，否则文件不会出现在实例中 |

## 使用方式

1. **前置准备**：完成 SLR 服务授权（见[快速开始](../../application-user-guide/agent-development/sandbox/sandbox-start-using/sandbox-quick-start.md)），获取 `workspace_id` 和 API Key；
2. **上传文件（如需）**：调用 `POST /api/v1/agentstudio/files` 上传配置文件，`source=sandbox_template`，轮询至 `status=available`；
3. **创建模版**：`POST /v3/templates`，传入 `name`、`cpuCount`、`memoryMB` 及可选配置，记录返回的 `templateID` 和 `buildID`；
4. **等待构建就绪**：轮询 `GET /templates/{templateID}/builds/{buildID}/status`，直至 `status=ready`；
5. **创建实例**：`POST /sandboxes`，传入 `templateID` 及实例配置（如 `timeout`、`allow_internet_access`）；
6. **连接与操作**：使用 `sandboxID` 调用 `/connect`、`/pause`、`/resume` 或 `/sandboxes/{sandboxID}` 获取实时状态。

SDK 用户可复用 E2B 官方 SDK，但需注意：SDK 中的 `api_key` 仅用于协议占位，**实际鉴权仍依赖 HTTP Header 的 `Authorization: Bearer <your-api-key>`** [原文标题](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)。

## 限制和注意事项

- **文件限制**：单文件 ≤ 50 MB，工作空间总容量 ≤ 100 GB，保存时效 30 天；仅 `.yaml` 等明确支持的扩展名可上传，`.csv`、`.yml`、`.sh`、`.whl`、`.tar.gz`、`.ts` 均不支持；
- **实例生命周期**：`timeout` 取值范围 `[300, 604800]` 秒（5 分钟 ~ 7 天），`autoPause=true` 时到期暂停而非释放；
- **错误处理**：HTTP 409 表示状态冲突（如模版未就绪即创建实例、有活跃实例时删除模版）；415 表示文件类型或 `Content-Type` 不合法（预签名上传时勿设 `Content-Type`）；
- **地域锁定**：Endpoint 中 `region` 固定为 `cn-beijing`，不支持其他地域；
- **模版更新**：`PUT /templates/{templateCode}` 会递增 `version` 并触发新构建，旧版本实例不受影响，但新创建实例将使用最新就绪版本。

## 来源文档

- [概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)
- [Sandbox API 错误码](../../raw/application-api-reference/sandbox-api/sandbox-api-errors.md)
- [实例管理](../../raw/application-api-reference/sandbox-api/sandbox-api-instances.md)
- [创建实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md)
- [列举实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-list.md)
- [获取实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-get.md)
- [连接实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-connect.md)
- [暂停实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-pause.md)
- [恢复实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-resume.md)
- [认证](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)
- [模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md)
- [释放实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-delete.md)
- [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)
- [列举模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-list.md)
- [更新模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-update.md)
- [获取模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-get.md)
- [删除模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-delete.md)
- [获取构建状态](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-build-status.md)


