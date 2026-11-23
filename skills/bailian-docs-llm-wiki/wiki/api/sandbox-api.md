# sandbox api

Sandbox API 是阿里云百炼提供的[沙箱环境](../concepts/sandbox.md)管理接口，基于 E2B 协议兼容实现，用于创建、管理与销毁隔离的计算实例及模版。它通过阿里云百炼 AI 网关统一接入，支持实例生命周期控制、模版构建与文件挂载等核心能力。开发者需完成工作空间授权与 API Key 配置后方可调用。

## 支持的模型/功能

- **实例管理**：支持创建（`POST /sandboxes`）、列举（`GET /v2/sandboxes`）、获取详情（`GET /sandboxes/{sandboxID}`）、连接（`POST /sandboxes/{sandboxID}/connect`）、暂停（`POST /sandboxes/{sandboxID}/pause`）、恢复（`POST /sandboxes/{sandboxID}/resume`）和释放（`DELETE /sandboxes/{sandboxID}`）实例。所有操作均兼容 E2B 协议语义，详见[实例管理](raw/application-api-reference/sandbox-api/sandbox-api-instances.md)。
- **模版管理**：支持创建（`POST /v3/templates`）、列举（`GET /v2/templates`）、获取（`GET /templates/{templateCode}`）、更新（`PUT /templates/{templateCode}`）、查询构建状态（`GET /templates/{templateCode}/builds/{buildID}/status`）和删除（`DELETE /templates/{templateCode}`）模版。更新模版为阿里云百炼扩展协议，不完全兼容 E2B v2，具体差异见[更新模版](raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-update.md)。
- **文件上传与挂载**：仅支持 `source=sandbox_template` 的文件上传，且必须等待状态变为 `available` 后才能在 `mntConfig` 中引用。单文件上限 50 MB，工作空间总容量 100 GB，保存时效 30 天。文件类型校验严格，`.csv`、`.yml`、`.sh`、`.whl`、`.tar.gz` 等明确不支持，详见[文件上传](raw/application-api-reference/sandbox-api/sandbox-api-overview.md)。

> **注意**：文档中关于模版创建路径存在不一致描述——[概览](raw/application-api-reference/sandbox-api/sandbox-api-overview.md) 列出 `/v3/templates`，而[创建模版](raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md) 明确说明兼容 `POST /templates` 路由；实际应以 `/v3/templates` 为准（新版本路径），`/templates` 为向后兼容路由，但官方推荐使用 `/v3/templates`。

## 关键参数

- **通用参数**：
  - `workspace_id` 和 `region`（当前仅支持 `cn-beijing`）用于拼装 Endpoint：`https://{workspace_id}.{region}.maas.aliyuncs.com/api/v1/agentstudio/sandbox`。
  - 鉴权统一使用 `Authorization: Bearer <your-api-key>`，API Key 在[百炼控制台](https://bailian.console.aliyun.com/?tab=model#/api-key)获取。
- **实例创建参数**：
  - `templateID`（必填）：已构建完成（`buildStatus=ready`）的模版 ID；
  - `timeout`（可选）：实例生命周期，300–604800 秒；
  - `allow_internet_access`（可选）：是否允许公网访问；
  - `lifecycle.on_timeout`（可选）：到期行为，如 `"pause"`；`auto_resume` 控制暂停后连接是否自动恢复。
- **模版创建/更新参数**：
  - `cpuCount` 与 `memoryMB` 必须同时指定，且需匹配平台预设规格组合；
  - `mntConfig` 中 `originFileId` 必须指向 `source=sandbox_template` 且 `status=available` 的文件；
  - `networkConfig.allowOut` 支持域名，但 `denyOut` **仅支持 IPv4/IPv6/CIDR，不支持域名**（见[创建模版](raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)）。

## 使用方式

1. **前置准备**：开通百炼服务，[创建 API Key](raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)，完成 SLR 授权，并获取工作空间 ID。
2. **文件上传（如需挂载）**：先调用 `POST /api/v1/agentstudio/files` 上传文件，指定 `source=sandbox_template`，轮询至 `status=available`。
3. **创建模版**：调用 `POST /v3/templates`，传入资源配置、`mntConfig`（含已上传的 `originFileId`）等，获取 `templateID` 和 `buildID`。
4. **等待构建就绪**：调用 `GET /templates/{templateID}/builds/{buildID}/status`，直至 `status=ready`。
5. **创建实例**：调用 `POST /sandboxes`，传入 `templateID` 及其他配置。
6. **连接与交互**：调用 `POST /sandboxes/{sandboxID}/connect` 获取 `domain` 与各类 token，用于后续数据面通信。

> **注意**：E2B SDK 可直接接入，但需注意其 `X-API-Key` 字段仅为协议占位符，实际鉴权仍依赖 HTTP Header 中的 `Authorization`；推荐按[认证](raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)文档配置 `e2b_${ALIYUN_UID}` 占位。

## 限制和注意事项

- **地域限制**：当前仅支持 `cn-beijing` 地域，Endpoint 中 `region` 固定为此值。
- **文件限制**：单文件 ≤50 MB；工作空间总容量 ≤100 GB；文件保存期为 30 天；`.csv`、`.yml`、`.sh`、`.whl`、`.tar.gz` 等格式明确不支持，`.ts` 文件会返回视频格式错误。
- **模版删除约束**：若模版关联有运行中或暂停中的实例，`DELETE /templates/{templateCode}` 将返回 409 错误，必须先释放所有实例。
- **错误处理**：兼容 E2B 协议的接口错误结构贴近 E2B 原生定义，不封装为百炼统一 `Result<T>`；HTTP 状态码含义需结合 [Sandbox API 错误码](raw/application-api-reference/sandbox-api/sandbox-api-errors.md) 理解，例如 409 表示状态冲突（如模版未就绪时创建实例、模版有活跃实例时删除等）。
- **SDK 兼容性**：E2B SDK 可用于实例管理（如 `create()`, `list()`, `get_info()`, `pause()` 等），但模版管理（创建、更新、构建查询）为百炼扩展能力，需直接调用 REST 接口。

## 来源文档

- [概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)
- [认证](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)
- [Sandbox API 错误码](../../raw/application-api-reference/sandbox-api/sandbox-api-errors.md)
- [创建实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md)
- [实例管理](../../raw/application-api-reference/sandbox-api/sandbox-api-instances.md)
- [列举实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-list.md)
- [获取实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-get.md)
- [暂停实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-pause.md)
- [恢复实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-resume.md)
- [释放实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-delete.md)
- [模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md)
- [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)
- [列举模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-list.md)
- [更新模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-update.md)
- [获取构建状态](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-build-status.md)
- [删除模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-delete.md)
- [获取模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-get.md)
- [连接实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-connect.md)


