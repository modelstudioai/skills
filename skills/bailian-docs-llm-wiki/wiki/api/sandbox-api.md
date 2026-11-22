# sandbox api

Sandbox API 是阿里云百炼提供的沙箱环境生命周期管理接口，兼容 E2B 协议，支持沙箱实例与模版的创建、查询、更新和释放。所有请求需经阿里云百炼 AI 网关转发，并通过 API Key 鉴权。管控面操作（如实例启停、模版构建）与数据面访问（如代码执行）分离，开发者需结合 `domain` 和 `envdAccessToken` 进行后续交互。

## 支持的模型/功能

- **沙箱实例管理**：支持创建、列举、获取、连接、暂停、恢复和释放实例，覆盖完整生命周期。实例基于预构建模版启动，状态包括 `running`、`paused` 等。
- **沙箱模版管理**：支持创建、列举、获取、更新、查询构建状态和删除模版。模版定义 CPU/内存规格、基础镜像（如 `code-interpreter-v1`、`browser`）、网络规则、环境变量及挂载文件；每次更新触发新版本构建，`buildStatus` 需变为 `ready` 后方可创建实例。
- **文件上传能力**：仅支持 `source=sandbox_template` 的文件上传，用于模版 `mntConfig` 挂载。上传后需轮询至 `status=available` 才可使用，详见 [文件上传](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)。
- **E2B 兼容性**：除模版更新（`PUT /templates/{templateCode}`）为阿里云百炼自定义协议外，其余接口（如 `/sandboxes`、`/sandboxes/{sandboxID}/connect`）在方法、路径、响应结构上贴近 [E2B 官方 API](https://docs.e2b.dev/api-reference)，通用字段语义可参照其文档理解。

## 关键参数

- **认证参数**：所有请求必须携带 `Authorization: Bearer <your-api-key>`，API Key 须在[百炼控制台](https://bailian.console.aliyun.com/?tab=model#/api-key)创建；E2B SDK 中 `api_key` 字段仅用于协议占位，实际鉴权以该 Header 为准。
- **实例创建参数**：
  - `templateID`（必填）：已构建完成（`buildStatus=ready`）的模版 ID；
  - `timeout`（可选）：实例生命周期上限，300–604800 秒；
  - `allow_internet_access`（可选）：是否允许公网访问；
  - `lifecycle.on_timeout`（可选）：到期行为，`pause` 或 `kill`；
  - `mntConfig` 不在此接口中传入，仅在模版层配置。
- **模版创建/更新参数**：
  - `cpuCount` 与 `memoryMB` 必须同时指定，且须匹配平台支持的规格组合；
  - `mntConfig` 中 `originFileId` 必须指向 `source=sandbox_template` 且 `status=available` 的文件，`mountPath` 必须以 `/home/user/workspace/uploads/` 开头；
  - `networkConfig.allowOut` 支持域名，`denyOut` 仅支持 CIDR/IPv4/IPv6，不支持域名（见 [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)）。
- **文件上传参数**：`source=sandbox_template` 为强制要求，否则返回错误码 `100005`；单文件上限 50 MB，总容量 100 GB，保存时效 30 天。

## 使用方式

1. **前置准备**：
   - 开通百炼服务，创建 API Key（见 [认证](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)）；
   - 完成 SLR 服务授权（见 [快速开始](../../raw/application-user-guide/agent-development/sandbox/sandbox-start-using/sandbox-quick-start.md)）；
   - 获取工作空间 ID（控制台右上角下拉菜单查看），拼装 Endpoint：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox`。

2. **模版流程**：
   - 上传所需文件（`source=sandbox_template`），轮询至 `status=available`；
   - 调用 `POST /v3/templates` 创建模版，记录返回的 `templateID` 和 `buildID`；
   - 轮询 `GET /templates/{templateID}/builds/{buildID}/status`，待 `status=ready`；
   - （可选）调用 `PUT /templates/{templateID}` 更新模版，新版本需重新构建。

3. **实例流程**：
   - 调用 `POST /sandboxes` 创建实例，传入 `templateID` 及配置；
   - 调用 `GET /sandboxes/{sandboxID}` 或 `POST /sandboxes/{sandboxID}/connect` 获取 `domain` 与 `envdAccessToken`，用于数据面访问；
   - 实例可按需 `POST /sandboxes/{sandboxID}/pause` 暂停或 `POST /sandboxes/{sandboxID}/resume` 恢复；
   - 不再需要时调用 `DELETE /sandboxes/{sandboxID}` 释放资源。

> **注意**：文档中列举实例接口存在路径不一致问题——[概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md) 表格写为 `GET /v2/sandboxes`，而 [列举实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-list.md) 明确说明兼容 `GET /sandboxes`。实际应以 `GET /v2/sandboxes` 为准，`/sandboxes` 为旧路由，可能在未来版本废弃。

## 限制和注意事项

- **地域限制**：当前仅支持 `cn-beijing` 地域，Endpoint 中 `region` 固定为此值。
- **文件限制**：`.csv`、`.yml`、`.sh`、`.whl`、`.tar.gz`、`.ts` 等扩展名明确不支持；`.yaml` 可上传。具体支持列表以接口返回错误码 `11900014`（文件类型不被允许）为准。
- **模版删除约束**：调用 `DELETE /templates/{templateCode}` 前，必须确保该模版无任何 `running` 或 `paused` 实例，否则返回 409 错误并附带关联实例 ID（见 [删除模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-delete.md)）。
- **错误处理**：兼容 E2B 协议的接口不封装为百炼统一 `Result<T>` 结构，错误响应直接返回 `{ "code": xxx, "message": "..." }`，HTTP 状态码含义见 [Sandbox API 错误码](../../raw/application-api-reference/sandbox-api/sandbox-api-errors.md)。
- **SDK 使用**：推荐使用 E2B 官方 SDK（如 Python SDK），但需注意其 `api_key` 参数仅满足协议格式，真实鉴权仍依赖 HTTP Header 中的百炼 API Key。

## 来源文档

- [概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)
- [认证](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)
- [Sandbox API 错误码](../../raw/application-api-reference/sandbox-api/sandbox-api-errors.md)
- [实例管理](../../raw/application-api-reference/sandbox-api/sandbox-api-instances.md)
- [创建实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md)
- [获取实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-get.md)
- [列举实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-list.md)
- [连接实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-connect.md)
- [恢复实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-resume.md)
- [释放实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-delete.md)
- [模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md)
- [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)
- [列举模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-list.md)
- [暂停实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-pause.md)
- [获取模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-get.md)
- [更新模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-update.md)
- [获取构建状态](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-build-status.md)
- [删除模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-delete.md)


