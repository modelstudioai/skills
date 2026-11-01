# sandbox api

Sandbox API 是阿里云百炼提供的沙箱环境生命周期管理接口，兼容 E2B 协议，支持沙箱实例与模版的创建、查询、启停及销毁。所有请求需通过阿里云百炼 API Key 鉴权，并经百炼 AI 网关转发。管控面与数据面分离，实例连接后需使用返回的 `envdAccessToken` 和 `domain` 访问数据面服务。

## 支持的模型/功能

- **沙箱实例管理**：支持创建、列举、获取详情、连接、暂停、恢复和释放实例，覆盖完整生命周期。实例基于预构建模版启动，支持配置 CPU（1–4 核）、内存（2048–8192 MB）、磁盘（10240 MB 起）、网络策略（`allowOut`/`denyOut`）、环境变量及生命周期行为（如 `on_timeout: pause`）。
- **沙箱模版管理**：支持创建、列举、获取、更新和删除模版。模版可指定基础镜像（如 `code-interpreter-v1`、`browser`）、挂载文件（需先上传至 `source=sandbox_template`）、网络规则与默认环境变量。每次创建或更新均触发新版本构建，状态需轮询 [获取构建状态](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-build-status.md) 确认为 `ready` 后方可创建实例。
- **文件上传能力**：仅支持 `source=sandbox_template` 的文件上传，用于模版挂载。上传后需等待 `status=available` 才能写入 `mntConfig`。该机制在 [概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md) 中有详细说明。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `templateID` | 请求体（创建实例）、路径（获取/删除模版） | string | 是 | 模版唯一标识，必须已构建完成（`buildStatus=ready`）；模版未就绪时创建实例返回 409 |
| `sandboxID` | 路径参数（除 `/sandboxes` 外所有实例接口） | string | 是 | 实例唯一 ID，由创建接口返回，用于后续操作 |
| `timeout` | 请求体（创建/连接/恢复实例）、`lifecycle.on_timeout`（创建实例） | integer | 否 | 实例或连接超时时间（秒），范围 `[300, 604800]`；`maxRunningTimeout` 优先级高于 `autoPauseTime` |
| `mntConfig` | 请求体（创建/更新模版） | array<object> | 否 | 文件挂载配置，`originFileId` 必须为已上传且 `status=available` 的文件 ID；`mountPath` 必须以 `/home/user/workspace/uploads/` 开头 |
| `networkConfig.allowOut` / `denyOut` | 请求体（创建/更新模版） | array<string> | 否 | 出口白名单/黑名单，`denyOut` 不支持域名（见 [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)） |

> **注意**：文档中关于 `mntConfig.mountPath` 的约束存在不一致——[创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md) 明确要求“必须以 `/home/user/workspace/uploads/` 开头”，而 [更新模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-update.md) 仅复述该要求但未强调强制性；实际调用应严格遵循前者，否则文件不会出现在实例中。

## 使用方式

1. **前置准备**  
   - 开通百炼服务并[创建 API Key](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)；  
   - 完成 SLR 服务授权（见[快速开始](../../raw/application-user-guide/agent-development/sandbox/sandbox-start-using/sandbox-quick-start.md)）；  
   - 获取工作空间 ID（控制台右上角下拉菜单）；  
   - 构建 Endpoint：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox`。

2. **模版流程**  
   - 上传文件（`source=sandbox_template`）→ 轮询至 `status=available`；  
   - `POST /v3/templates` 创建模版 → 获取 `templateID` 和 `buildID`；  
   - `GET /templates/{templateID}/builds/{buildID}/status` 等待 `status=ready`；  
   - `POST /sandboxes` 基于该模版创建实例。

3. **实例流程**  
   - 创建后可直接 `GET /sandboxes/{sandboxID}` 查看详情；  
   - `POST /sandboxes/{sandboxID}/connect` 获取实时访问凭证（`envdAccessToken` + `domain`）；  
   - `POST /sandboxes/{sandboxID}/pause` 暂停（保留状态）→ `POST /sandboxes/{sandboxID}/resume` 恢复；  
   - `DELETE /sandboxes/{sandboxID}` 彻底释放资源。

4. **SDK 接入**  
   可直接使用 E2B 官方 SDK（如 Python `e2b` 包），只需将 `api_key` 设为占位符（如 `e2b_${ALIYUN_UID}`），真实鉴权由 `Authorization: Bearer <your-api-key>` 完成，详见 [实例管理与使用](../../raw/application-user-guide/agent-development/sandbox/sandbox-sdk.md)。

## 限制和注意事项

- **地域限制**：当前仅支持 `cn-beijing` 地域，Endpoint 中 `region` 固定为此值。
- **文件限制**：单文件 ≤ 50 MB，工作空间总容量 ≤ 100 GB，保存时效 30 天；支持 `.yaml`，不支持 `.csv`、`.yml`、`.sh`、`.whl`、`.tar.gz`、`.ts` 等（见 [概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)）。
- **模版删除约束**：若模版关联任何运行中或暂停中的实例，`DELETE /templates/{templateCode}` 将返回 409 错误，需先释放所有实例。
- **错误处理**：兼容 E2B 协议的接口不封装为百炼统一 `Result<T>` 结构，错误响应直接返回 `{code, message, requestID}`；HTTP 状态码语义与标准一致（如 401=API Key 无效，409=状态冲突），完整错误码见 [错误码](../../raw/application-api-reference/sandbox-api/sandbox-api-errors.md)。
- **鉴权特殊性**：E2B SDK 的 `api_key` 字段仅用于协议占位，**不参与业务鉴权**；真实鉴权依赖 HTTP Header 中的 `Authorization: Bearer <your-api-key>`。

## 来源文档

- [概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)
- [认证](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)
- [实例管理](../../raw/application-api-reference/sandbox-api/sandbox-api-instances.md)
- [错误码](../../raw/application-api-reference/sandbox-api/sandbox-api-errors.md)
- [列举实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-list.md)
- [创建实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md)
- [获取实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-get.md)
- [连接实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-connect.md)
- [暂停实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-pause.md)
- [释放实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-delete.md)
- [恢复实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-resume.md)
- [模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md)
- [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)
- [获取模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-get.md)
- [列举模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-list.md)
- [获取构建状态](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-build-status.md)
- [更新模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-update.md)
- [删除模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-delete.md)


