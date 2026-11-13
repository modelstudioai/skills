# sandbox api

Sandbox API 是阿里云百炼提供的沙箱环境生命周期管理服务，基于 E2B 协议兼容实现，支持沙箱实例与模版的创建、查询、启停、释放及构建管理。所有请求需通过百炼工作空间专属 Endpoint 发起，并使用百炼 API Key 鉴权。管控面请求经百炼 AI 网关转发，数据面访问需通过返回的 `domain` 与 `envdAccessToken` 连接。

## 支持的模型/功能

- **沙箱实例管理**：支持创建（`POST /sandboxes`）、列举（`GET /v2/sandboxes`）、获取详情（`GET /sandboxes/{sandboxID}`）、连接（`POST /sandboxes/{sandboxID}/connect`）、暂停（`POST /sandboxes/{sandboxID}/pause`）、恢复（`POST /sandboxes/{sandboxID}/resume`）和释放（`DELETE /sandboxes/{sandboxID}`）等全生命周期操作。详见 [实例管理](raw/application-api-reference/sandbox-api/sandbox-api-instances.md)。
- **沙箱模版管理**：支持创建（`POST /v3/templates`）、列举（`GET /v2/templates`）、获取（`GET /templates/{templateCode}`）、更新（`PUT /templates/{templateCode}`）、查询构建状态（`GET /templates/{templateCode}/builds/{buildID}/status`）和删除（`DELETE /templates/{templateCode}`）。模版构建完成后（`status=ready`）方可用于创建实例，参见 [创建模版](raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)。
- **文件挂载能力**：仅支持通过百炼文件上传接口上传 `source=sandbox_template` 且 `status=available` 的文件，并在模版 `mntConfig` 中引用；挂载路径必须以 `/home/user/workspace/uploads/` 开头，否则文件不会出现在实例中。具体限制见 [文件上传](raw/application-api-reference/sandbox-api/sandbox-api-overview.md)。

> **注意**：文档中存在两处不一致的路由兼容说明：  
> - 文档 1（[概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)）称模版创建接口为 `POST /v3/templates`，并注明兼容 `POST /templates`；  
> - 文档 13（[创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)）同样声明兼容 `POST /templates`；  
> - 但文档 12（[模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md)）的子项索引未体现该兼容性，且文档 16（[更新模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-update.md)）明确指出“该接口为阿里云百炼扩展协议，不声明完全兼容 E2B Update Template v2”。  
> 实际开发中请以 `POST /v3/templates` 和 `PUT /templates/{templateCode}` 为准，`/templates` 路由为兼容层，行为可能随版本演进调整。

## 关键参数

- **认证参数**：`Authorization: Bearer <your-api-key>`，API Key 需在百炼控制台创建，**不可**用 E2B SDK 的 `api_key` 字段替代业务鉴权（[认证](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)）。
- **实例创建参数**：
  - `templateID`（必填）：已构建完成（`status=ready`）的模版 ID；
  - `timeout`（可选）：实例生命周期上限，单位秒，范围 `[300, 604800]`；
  - `allow_internet_access`（可选）：是否允许公网访问；
  - `lifecycle.on_timeout`（可选）：到期行为，如 `"pause"`；`auto_resume` 控制连接时是否自动恢复；
  - `network.allowOut`/`denyOut`（可选）：出口流量白/黑名单，域名仅支持于 `allowOut`。
- **模版创建/更新参数**：
  - `cpuCount` 与 `memoryMB` 必须**同时指定**，且需匹配平台预设规格组合；
  - `mntConfig` 中 `originFileId` 必须指向 `source=sandbox_template` 且 `status=available` 的文件；
  - `maxRunningTimeout` 与 `autoPauseTime` 共存时，前者优先生效；均未传则默认最大运行时间为 604800 秒。

## 使用方式

1. **前置准备**：
   - 开通百炼服务，创建 API Key（[认证](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)）；
   - 完成 SLR 服务授权（[快速开始](raw/application-user-guide/agent-development/sandbox/sandbox-start-using/sandbox-quick-start.md)）；
   - 获取工作空间 ID（控制台右上角下拉菜单）。

2. **Endpoint 拼装**：  
   `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox`（当前仅支持 `cn-beijing` 地域）。

3. **典型流程**：
   - 上传配置文件 → 创建模版 → 轮询构建状态至 `ready` → 创建实例 → 连接实例 → 执行任务 → 暂停/释放实例。

4. **SDK 支持**：可直接使用 E2B 官方 SDK（如 `e2b` Python 包），但需将 `api_key` 设为占位符（如 `e2b_${ALIYUN_UID}`），实际鉴权仍依赖 HTTP Header 中的百炼 API Key（[实例管理与使用](raw/application-user-guide/agent-development/sandbox/sandbox-sdk.md)）。

## 限制和注意事项

- **文件限制**：单文件 ≤ 50 MB，工作空间总容量 ≤ 100 GB，保存时效 30 天；仅 `.yaml` 明确支持，`.csv`、`.yml`、`.sh`、`.whl`、`.tar.gz`、`.ts` 等**不支持**（[概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)）。
- **模版约束**：`mntConfig.mountPath` 必须以 `/home/user/workspace/uploads/` 开头；若路径不在此目录下，接口虽接受请求，但文件**不会挂载到实例中**（[创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)）。
- **错误处理**：
  - 模版构建未就绪时调用创建实例接口，返回 `409 Conflict`；
  - 删除模版前需确保无运行中或暂停中的实例，否则返回 `409` 并附带关联实例 ID（[删除模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-delete.md)）；
  - 文件类错误码集中定义于 [Sandbox API 错误码](../../raw/application-api-reference/sandbox-api/sandbox-api-errors.md)，如 `11900014`（文件类型不被允许）、`11900023`（文件暂不可用）等。
- **兼容性说明**：除模版更新接口为百炼自定义外，其余接口方法、路径与响应结构贴近 E2B 官方定义，通用字段语义可参考 [E2B API Reference](https://docs.e2b.dev/api-reference)，但鉴权、Endpoint 及扩展字段（如 `bailianSandboxId`）以本文档为准（[概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)）。

## 来源文档

- [概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)
- [认证](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)
- [实例管理](../../raw/application-api-reference/sandbox-api/sandbox-api-instances.md)
- [Sandbox API 错误码](../../raw/application-api-reference/sandbox-api/sandbox-api-errors.md)
- [创建实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md)
- [列举实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-list.md)
- [获取实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-get.md)
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


