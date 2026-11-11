# sandbox api

Sandbox API 是阿里云百炼提供的沙箱环境生命周期管理接口，兼容 E2B 协议，支持通过 RESTful API 或 E2B SDK 创建、管理沙箱实例与模版。其核心能力包括实例的启停、连接、释放，模版的构建与配置，以及文件挂载等。所有请求需经阿里云百炼 AI 网关转发，并使用工作空间级 API Key 鉴权。

## 支持的模型/功能

- **实例管理**：支持创建（`POST /sandboxes`）、列举（`GET /v2/sandboxes`）、获取详情（`GET /sandboxes/{sandboxID}`）、连接（`POST /sandboxes/{sandboxID}/connect`）、暂停（`POST /sandboxes/{sandboxID}/pause`）、恢复（`POST /sandboxes/{sandboxID}/resume`）和释放（`DELETE /sandboxes/{sandboxID}`）沙箱实例。详见 [创建实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md) 和 [实例管理](../../raw/application-api-reference/sandbox-api/sandbox-api-instances.md)。
- **模版管理**：支持创建（`POST /v3/templates`）、列举（`GET /v2/templates`）、获取（`GET /templates/{templateCode}`）、更新（`PUT /templates/{templateCode}`）、查询构建状态（`GET /templates/{templateCode}/builds/{buildID}/status`）和删除（`DELETE /templates/{templateCode}`）模版。模版构建完成后（`status=ready`）方可用于创建实例。
- **文件挂载**：仅支持通过 `source=sandbox_template` 上传的文件（如 `.yaml`），且状态必须为 `available`，方可写入模版的 `mntConfig` 字段。`.csv`、`.yml`、`.sh`、`.whl`、`.tar.gz`、`.ts` 等类型明确不支持，具体以接口返回为准。文件上传能力见 [概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md) 中的“文件上传”章节。

> **注意**：文档中对 `mntConfig.mountPath` 的路径要求存在不一致表述。[创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md) 和 [更新模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-update.md) 均强调 `mountPath` “必须以 `/home/user/workspace/uploads/` 开头”，但同时注明“路径不在该目录下时接口接受配置但实例中不会出现文件”。实践中应严格遵守该前缀，否则挂载将静默失败。

## 关键参数

- **认证参数**：`Authorization: Bearer <your-api-key>`，API Key 须在百炼控制台 [API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key) 创建。E2B SDK 中的 `X-API-Key` / `api_key` 仅用于协议兼容，百炼侧不用于业务鉴权，推荐填写 `e2b_${ALIYUN_UID}`。
- **Endpoint 拼装**：`https://{workspace_id}.{region}.maas.aliyuncs.com/api/v1/agentstudio/sandbox`，其中 `workspace_id` 从控制台右上角获取，`region` 当前仅支持 `cn-beijing`。
- **实例创建关键字段**：
  - `templateID`（必填）：已构建完成（`status=ready`）的模版 ID；
  - `timeout`（可选）：实例生命周期，单位秒，范围 `[300, 604800]`；
  - `allow_internet_access`（可选）：是否允许公网访问；
  - `lifecycle.on_timeout`（可选）：到期行为，如 `"pause"`；`auto_resume` 控制连接时是否自动恢复。
- **模版创建关键字段**：
  - `cpuCount` 与 `memoryMB`（必填且需匹配平台规格组合）；
  - `mntConfig` 中的 `originFileId` 必须指向 `source=sandbox_template` 且 `status=available` 的文件；
  - `maxRunningTimeout` 与 `autoPauseTime` 共存时，前者优先生效，到期直接释放实例。

## 使用方式

1. **前置准备**：开通百炼服务，完成 SLR 授权（见 [快速开始](../../raw/application-user-guide/agent-development/sandbox/sandbox-start-using/sandbox-quick-start.md)），获取 `workspace_id` 和 API Key。
2. **上传文件（如需）**：调用 `POST /api/v1/agentstudio/files`，`form-data` 或 JSON 请求体中指定 `source=sandbox_template`，轮询至 `status=available`。
3. **创建模版**：调用 `POST /v3/templates`，传入资源配置与 `mntConfig` 等，记录返回的 `templateID` 和 `buildID`。
4. **等待构建就绪**：轮询 `GET /templates/{templateID}/builds/{buildID}/status`，直至 `status=ready`。
5. **创建实例**：调用 `POST /sandboxes`，传入 `templateID` 及其他配置。
6. **连接与操作**：调用 `POST /sandboxes/{sandboxID}/connect` 获取 `domain` 和 `envdAccessToken`，用于后续数据面交互；按需调用 `pause`/`resume`/`delete` 等管理接口。

## 限制和注意事项

- **地域限制**：当前仅支持 `cn-beijing` 地域。
- **文件限制**：单文件 ≤ 50 MB，工作空间总容量 ≤ 100 GB，保存时效 30 天；仅 `.yaml` 明确支持，其余扩展名（如 `.yml`、`.csv`）均不支持。
- **模版删除约束**：若模版关联任何运行中或暂停中的实例，`DELETE /templates/{templateCode}` 将返回 `409` 错误，必须先释放所有实例。
- **错误处理**：兼容 E2B 协议的接口（如实例管理）错误结构贴近 E2B 原生定义，通用字段可参考 [E2B 官方文档](https://docs.e2b.dev/api-reference)；百炼特有错误码详见 [错误码](../../raw/application-api-reference/sandbox-api/sandbox-api-errors.md)。
- **SDK 兼容性**：推荐使用 E2B 官方 SDK（如 `@e2b/sdk`），但需注意其 `api_key` 参数不参与百炼业务鉴权，仅作协议占位。完整接入指南见 [实例管理与使用](../../raw/application-user-guide/agent-development/sandbox/sandbox-sdk.md)。

## 来源文档

- [认证](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)
- [概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)
- [错误码](../../raw/application-api-reference/sandbox-api/sandbox-api-errors.md)
- [创建实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md)
- [实例管理](../../raw/application-api-reference/sandbox-api/sandbox-api-instances.md)
- [列举实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-list.md)
- [连接实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-connect.md)
- [获取实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-get.md)
- [释放实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-delete.md)
- [暂停实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-pause.md)
- [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)
- [恢复实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-resume.md)
- [模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md)
- [列举模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-list.md)
- [获取模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-get.md)
- [获取构建状态](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-build-status.md)
- [更新模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-update.md)
- [删除模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-delete.md)


