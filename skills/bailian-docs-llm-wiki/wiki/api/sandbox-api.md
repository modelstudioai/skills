# [sandbox](../guides/sandbox.md) api

Sandbox API 是阿里云百炼提供的沙箱实例与模版全生命周期管理接口，兼容 E2B 协议，支持开发者通过 RESTful 方式创建、查询、控制沙箱环境。所有请求需经阿里云百炼 AI 网关转发，并使用百炼 API Key 鉴权。该 API 适用于需要动态执行代码、隔离运行环境或构建 Agent 数据面的场景。

## 支持的模型/功能

Sandbox API 不直接提供“模型”推理能力，而是提供**可编程沙箱环境**作为模型能力的执行载体。其核心功能分为两类：

- **实例管理**：支持创建、列举、获取、连接、暂停、恢复和释放沙箱实例。实例基于预构建的模版启动，具备独立 CPU、内存、磁盘、网络与文件系统，状态包括 `running`、`paused` 和已释放。
- **模版管理**：支持创建、列举、获取、更新、查询构建状态和删除模版。模版定义了沙箱的基础镜像（如 `code-interpreter-v1`、`browser`）、资源规格（CPU/内存组合）、网络规则、环境变量及挂载配置；每次创建或更新均触发异步镜像构建，仅当构建状态为 `ready` 后方可创建实例。

> **注意**：文档中多次提及 `fromImage` 可选值（如 `code-interpreter-v1`、`browser`、`all-in-one`），但[创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)明确说明官方镜像位于 `fc-e2b-registry.cn-beijing.cr.aliyuncs.com/runtime/` 下，而[API 总览与认证](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)未列出具体镜像名。实际使用时应以[创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)为准，避免直接拼接不完整路径。

## 关键参数

| 参数 | 位置 | 必填 | 类型 | 说明 |
|------|------|------|------|------|
| `Authorization` | Header | 是 | string | `Bearer <your-api-key>`，百炼 API Key，**非 E2B 的 `X-API-Key`** |
| `templateID` | 请求体（创建实例） / 路径（模版操作） | 是 | string | 模版唯一标识，来自创建/更新模版响应 |
| `sandboxID` | 路径 | 是 | string | 实例唯一标识，来自创建实例响应 |
| `cpuCount` / `memoryMB` | 请求体（创建/更新模版） | 是（同时传） | integer | 必须匹配平台预设规格组合，不支持任意值 |
| `timeout` | 请求体（创建/恢复/连接实例） | 否 | integer | 取值范围 `[300, 604800]`（5 分钟至 7 天），单位秒 |
| `allow_internet_access` | 请求体（创建实例） | 否 | boolean | 控制公网访问，默认 `false`；与 `network.allowPublicTraffic` 语义一致，推荐统一使用后者 |

其他重要参数包括：`autoPause`（到期是否暂停）、`lifecycle.on_timeout`（到期行为）、`network.allowOut`/`denyOut`（网络白/黑名单）、`envVars`/`envConfig`（实例/模版级环境变量）、`mntConfig`（文件挂载）。

## 使用方式

1. **准备环境**：开通百炼服务，[获取 API Key](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)，完成 SLR 授权，并确认工作空间 ID 与地域（当前仅 `cn-beijing`）。
2. **构造 Endpoint**：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox`
3. **创建模版**：调用 `POST /v3/templates` 提交资源配置与镜像信息，记录返回的 `templateID` 和 `buildID`。
4. **等待构建就绪**：轮询 `GET /templates/{templateID}/builds/{buildID}/status`，直至 `status` 为 `ready`。
5. **创建实例**：调用 `POST /sandboxes`，传入 `templateID` 及可选生命周期/网络参数，获取 `sandboxID`。
6. **连接与操作**：调用 `POST /sandboxes/{sandboxID}/connect` 获取 `domain` 与 `envdAccessToken`，用于后续数据面通信；按需调用 `pause`/`resume`/`DELETE` 管理实例状态。

E2B 官方 SDK 可直接接入（需配置 `api_key` 为占位符如 `e2b_${ALIYUN_UID}`），详见[实例管理与使用](../../raw/application-user-guide/sandbox/sandbox-sdk.md)。

## 限制和注意事项

- **地域限制**：当前仅支持 `cn-beijing` 地域，Endpoint 中 region 固定为 `cn-beijing`。
- **资源规格约束**：`cpuCount` 与 `memoryMB` 必须成对提交且严格匹配平台支持的组合（如 1C2G、2C4G），单独修改任一字段将导致 400 错误。
- **模版删除保护**：若模版关联有 `running` 或 `paused` 实例，`DELETE /templates/{templateCode}` 将返回 409，必须先调用 `DELETE /sandboxes/{sandboxID}` 释放所有实例。
- **鉴权唯一性**：所有请求**仅校验 `Authorization: Bearer <key>`**；E2B SDK 所需的 `X-API-Key` 或 `api_key` 字段在百炼侧无业务意义，仅作协议兼容占位。
- **响应结构差异**：Sandbox API 响应**不封装为百炼统一 `Result<T>` 结构**，而是直接返回 E2B 兼容格式（如实例数组、对象），错误响应体为 `{code, message, requestID}` 形式。
- **构建状态时效性**：模版 `tags` 和 `aliases` 字段在[创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)响应中存在，但文档明确说明“在能够被后续列举/获取模版稳定返回前，不作为持久化字段”，生产环境不应依赖其一致性。

## 来源文档

- [API 总览与认证](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)
- [实例管理](../../raw/application-api-reference/sandbox-api/sandbox-api-instances.md)
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
- [更新模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-update.md)
- [获取构建状态](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-build-status.md)
- [删除模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-delete.md)
- [获取模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-get.md)


