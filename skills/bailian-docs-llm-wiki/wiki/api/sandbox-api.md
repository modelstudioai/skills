# sandbox api

Sandbox API 是阿里云百炼平台提供的沙箱实例与模版全生命周期管理接口，兼容 E2B 协议，支持开发者通过 RESTful 方式创建、管理、连接和释放沙箱环境。其核心能力围绕模版构建、实例调度、文件挂载与网络策略展开，所有管控面请求均经百炼 AI 网关转发。开发者需先完成服务授权与 API Key 配置，方可调用。

## 支持的模型/功能

- **模版管理**：支持创建、列举、获取、更新、删除沙箱模版（`/v3/templates`, `/v2/templates`, `/templates/{templateCode}` 等），模版基于 `fromImage`（如 `code-interpreter-v1`）构建，可配置 CPU、内存、环境变量、网络规则及文件挂载（`mntConfig`）。  
- **实例管理**：支持创建、列举、获取、连接、暂停、恢复、释放沙箱实例（`/sandboxes`, `/v2/sandboxes`, `/sandboxes/{sandboxID}` 等），实例状态包括 `running`、`paused`，支持自动暂停（`autoPause`）与超时后自动恢复（`auto_resume`）。  
- **文件上传**：通过 `/api/v1/agentstudio/files` 上传文件，**必须指定 `source=sandbox_template`**，且仅当 `status=available` 后才可用于模版挂载；支持表单上传与预签名地址直传两种方式。  
- **数据面访问**：实例创建或连接后返回 `domain`、`envdAccessToken`、`trafficAccessToken` 等字段，用于后续通过 E2B SDK 或原生 envd 协议访问沙箱内部环境。

> **注意**：文档中多次提及“兼容 E2B 协议”，但模版更新（`PUT /templates/{templateCode}`）明确标注为[阿里云百炼扩展协议，不声明完全兼容 E2B Update Template v2](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-update.md)，开发者不应假设其行为与 E2B 官方定义完全一致。

## 关键参数

- **认证参数**：所有请求必须携带 `Authorization: Bearer <your-api-key>`，API Key 通过[百炼控制台](https://bailian.console.aliyun.com/?tab=model#/api-key)获取；E2B SDK 中的 `X-API-Key` 仅用于协议占位，百炼侧不校验 [认证](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)。  
- **模版参数**：`cpuCount` 与 `memoryMB` 必须同时传递且匹配平台规格组合；`mntConfig.originFileId` 必须指向已上传且 `status=available` 的文件；`mountPath` 必须以 `/home/user/workspace/uploads/` 开头，否则挂载无效 [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)。  
- **实例参数**：`timeout` 取值范围为 `[300, 604800]` 秒；`allow_internet_access` 控制公网访问；`lifecycle.on_timeout` 支持 `pause` 行为；`network` 支持 `allowOut`（域名/IP）、`denyOut`（仅 CIDR/IP）等细粒度规则 [创建实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md)。  
- **分页与过滤**：列举接口支持 `limit`（最大 50 实例 / 100 模版）与 `cursor`（模版）或 `state`/`templateID`（实例）等查询参数 [列举实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-list.md)。

## 使用方式

1. **前置准备**：开通百炼服务，完成 SLR 授权（见[快速开始](../../raw/application-user-guide/agent-development/sandbox/sandbox-start-using/sandbox-quick-start.md)），获取工作空间 ID 与地域（当前仅 `cn-beijing`），创建 API Key。  
2. **Endpoint 拼装**：基地址为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox`。  
3. **文件上传**：先调用 `/api/v1/agentstudio/files` 上传配置文件，`source=sandbox_template`，轮询至 `status=available`。  
4. **创建模版**：`POST /v3/templates`，传入 `name`、`cpuCount`、`memoryMB` 及 `mntConfig` 等，获取 `templateID` 与 `buildID`。  
5. **等待构建就绪**：`GET /templates/{templateID}/builds/{buildID}/status`，待 `status=ready` 后方可创建实例。  
6. **创建实例**：`POST /sandboxes`，指定 `templateID` 与可选 `timeout`、`lifecycle` 等，获得 `sandboxID`。  
7. **连接与操作**：使用 `sandboxID` 调用 `/connect` 获取访问凭证，或 `/pause`/`/resume`/`/delete` 管理生命周期。

## 限制和注意事项

- **文件限制**：单文件 ≤ 50 MB，工作空间总容量 ≤ 100 GB，保存时效 30 天；支持 `.yaml`，不支持 `.csv`、`.yml`、`.sh`、`.whl`、`.tar.gz`、`.ts` 等扩展名 [概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)。  
- **模版删除约束**：若模版存在 `running` 或 `paused` 实例，`DELETE /templates/{templateCode}` 返回 409 错误，需先释放所有关联实例 [删除模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-delete.md)。  
- **错误处理**：HTTP 状态码 400–501 对应参数、鉴权、资源、格式等错误；文件类错误（如 `11900008`）对应 413，视频格式错误（`11900019`）对应 415；通用错误结构贴近 E2B，可参考其[官方文档](https://docs.e2b.dev/api-reference)理解 [Sandbox API 错误码](../../raw/application-api-reference/sandbox-api/sandbox-api-errors.md)。  
- **SDK 兼容性**：推荐使用 E2B 官方 SDK（如 Python/JS），但需注意百炼扩展字段（如 `bailianSandboxId`）与非标准行为（如模版更新）可能未被 SDK 原生支持。

## 来源文档

- [认证](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)
- [Sandbox API 错误码](../../raw/application-api-reference/sandbox-api/sandbox-api-errors.md)
- [概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)
- [列举实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-list.md)
- [创建实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md)
- [实例管理](../../raw/application-api-reference/sandbox-api/sandbox-api-instances.md)
- [暂停实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-pause.md)
- [获取实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-get.md)
- [连接实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-connect.md)
- [恢复实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-resume.md)
- [释放实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-delete.md)
- [模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md)
- [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)
- [列举模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-list.md)
- [获取模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-get.md)
- [删除模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-delete.md)
- [更新模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-update.md)
- [获取构建状态](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-build-status.md)


