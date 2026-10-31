# sandbox api

Sandbox API 是阿里云百炼提供的沙箱环境生命周期管理服务，兼容 E2B 协议，支持通过 REST 接口或 E2B SDK 创建、管理沙箱实例与模版。其核心能力包括实例的启停、连接、资源隔离，以及模版的构建、更新与文件挂载。所有请求需经阿里云百炼 AI 网关转发，并依赖工作空间 ID 与地域拼装 Endpoint。

## 支持的模型/功能

- **实例管理**：支持创建（`POST /sandboxes`）、列举（`GET /v2/sandboxes`）、获取详情（`GET /sandboxes/{sandboxID}`）、连接（`POST /sandboxes/{sandboxID}/connect`）、暂停（`POST /sandboxes/{sandboxID}/pause`）、恢复（`POST /sandboxes/{sandboxID}/resume`）和释放（`DELETE /sandboxes/{sandboxID}`）等全生命周期操作。  
- **模版管理**：支持创建（`POST /v3/templates`）、列举（`GET /v2/templates`）、获取（`GET /templates/{templateCode}`）、更新（`PUT /templates/{templateCode}`）、查询构建状态（`GET /templates/{templateCode}/builds/{buildID}/status`）和删除（`DELETE /templates/{templateCode}`）。模版构建成功（`status=ready`）后方可用于创建实例。  
- **文件上传**：仅支持 `source=sandbox_template` 的文件上传，用于模版挂载；上传后需轮询至 `status=available` 才可写入 `mntConfig`。详细限制见[文件上传](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)。  
- **网络与生命周期配置**：实例级支持 `allow_internet_access`、`network`（含 `allowOut`/`denyOut`）、`lifecycle`（含 `on_timeout` 和 `auto_resume`）；模版级支持 `networkConfig` 与 `autoPauseTime`/`maxRunningTimeout`。

> **注意**：文档中 `GET /sandboxes` 路由在[列举实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-list.md)中被标注为“兼容路由”，但主推荐路径为 `/v2/sandboxes`；而[概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)表格中未列出该兼容路径，存在表述不一致。建议以 `/v2/sandboxes` 为准。

## 关键参数

| 参数 | 位置 | 类型 | 说明 | 来源 |
|------|------|------|------|------|
| `templateID` | 请求体（创建实例）/路径（获取模版） | string | 模版唯一标识，创建实例前必须已构建完成（`status=ready`） | [创建实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md) |
| `sandboxID` | 路径参数（多数实例接口） | string | 实例唯一 ID，由创建接口返回，用于后续所有实例操作 | [获取实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-get.md) |
| `timeout` | 请求体（创建/连接/恢复） | integer | 实例或连接超时时间（秒），范围 `[300, 604800]`；`maxRunningTimeout` 优先生效于 `autoPauseTime` | [创建实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md) 和 [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md) |
| `mntConfig` | 请求体（创建/更新模版） | array<object> | 文件挂载配置，`originFileId` 必须指向 `source=sandbox_template` 且 `status=available` 的文件；`mountPath` 必须以 `/home/user/workspace/uploads/` 开头 | [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md) |

## 使用方式

1. **前置准备**：  
   - 开通百炼服务并[创建 API Key](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)；  
   - 完成 SLR 服务授权（见[快速开始](../../raw/application-user-guide/agent-development/sandbox/sandbox-start-using/sandbox-quick-start.md)）；  
   - 获取工作空间 ID（控制台右上角下拉菜单）；  
   - 构建模版并确认其 `buildStatus=ready`（通过[获取构建状态](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-build-status.md)验证）。

2. **Endpoint 拼装**：  
   ```
   https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox
   ```

3. **鉴权**：  
   所有请求需携带 `Authorization: Bearer <your-api-key>` Header。E2B SDK 中 `api_key` 字段仅用于协议兼容，实际鉴权使用阿里云百炼 API Key。

4. **典型流程**：  
   - 上传文件 → 创建模版 → 轮询构建状态 → 创建实例 → 连接实例 → （可选）暂停/恢复 → 释放实例。

## 限制和注意事项

- **地域限制**：当前仅支持 `cn-beijing` 地域。  
- **文件限制**：单文件 ≤ 50 MB，工作空间总容量 ≤ 100 GB，保存时效 30 天；仅 `.yaml` 等明确支持的扩展名可上传，`.csv`、`.yml`、`.sh`、`.whl`、`.tar.gz`、`.ts` 等不支持（见[文件上传](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)）。  
- **模版约束**：`cpuCount` 与 `memoryMB` 必须同时传递且匹配平台规格组合；更新模版时若修改 `mntConfig`，需确保新引用的文件已上传并可用。  
- **错误处理**：  
  - 模版未就绪时创建实例返回 `409`；  
  - 删除模版前必须释放所有关联实例，否则返回 `409` 并附带 `sandboxId`；  
  - 错误响应结构贴近 E2B 原生定义，非阿里云百炼统一 `Result<T>` 格式（见[错误码](../../raw/application-api-reference/sandbox-api/sandbox-api-errors.md)）。  
- **SDK 兼容性**：推荐使用 E2B 官方 SDK，但需注意其 `X-API-Key` 字段不参与百炼业务鉴权，应填占位符如 `e2b_${ALIYUN_UID}`（见[认证](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)）。

## 来源文档

- [概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)
- [认证](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)
- [错误码](../../raw/application-api-reference/sandbox-api/sandbox-api-errors.md)
- [实例管理](../../raw/application-api-reference/sandbox-api/sandbox-api-instances.md)
- [创建实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md)
- [列举实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-list.md)
- [获取实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-get.md)
- [连接实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-connect.md)
- [暂停实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-pause.md)
- [恢复实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-resume.md)
- [模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md)
- [释放实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-delete.md)
- [获取模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-get.md)
- [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)
- [列举模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-list.md)
- [删除模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-delete.md)
- [更新模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-update.md)
- [获取构建状态](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-build-status.md)


