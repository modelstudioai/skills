# sandbox api

Sandbox API 是阿里云百炼提供的沙箱环境生命周期管理接口，兼容 E2B 协议，支持模版构建与实例的创建、连接、暂停、恢复和释放。所有请求通过阿里云百炼 API Key 鉴权，Endpoint 按工作空间与地域拼装，当前仅支持 `cn-beijing` 地域。该 API 专为需要动态执行代码、隔离运行环境的 AI 应用场景设计，不封装为百炼统一 `Result<T>` 结构，响应体贴近 E2B 原生格式。

## 支持的模型/功能

Sandbox API 不直接提供“模型”推理能力，而是提供**可编程沙箱环境**作为执行底座，其功能围绕两类核心资源展开：

- **模版（Template）**：定义沙箱的基础镜像、资源配置（CPU/内存）、网络策略、环境变量及挂载文件等静态配置。支持使用官方镜像（如 `code-interpreter-v1`、`browser`、`all-in-one`）或自定义镜像。模版需经构建（build）流程，状态变为 `ready` 后方可用于创建实例。详见 [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)。
- **实例（Sandbox）**：基于模版启动的运行时环境，具备独立 CPU、内存、磁盘、网络与生命周期。支持按需创建、连接、暂停/恢复、自动超时控制，并可通过 `envdUrl` 和访问 token 接入数据面执行命令或文件操作。实例状态包括 `running`、`paused`，释放后不可恢复。

> **注意**：文档中 `fromImage` 字段在 [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md) 中明确说明官方镜像位于 `fc-e2b-registry.cn-beijing.cr.aliyuncs.com/runtime/` 下，但 [获取模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-get.md) 的响应示例未体现该 registry 前缀，实际使用应以创建时传入的完整镜像地址为准。

## 关键参数

| 参数类别 | 参数名 | 类型 | 必填 | 说明 |
|----------|--------|------|------|------|
| **通用** | `Authorization: Bearer <api-key>` | Header | 是 | 阿里云百炼 API Key，用于业务鉴权；E2B SDK 中的 `X-API-Key` 仅作协议占位，不参与鉴权。 |
| **实例创建** | `templateID` | string | 是 | 已构建完成（`buildStatus=ready`）的模版 ID，见 [获取构建状态](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-build-status.md)。 |
| | `timeout` | integer | 否 | 实例生命周期时间（秒），范围 `[300, 604800]`；到期行为由 `lifecycle.on_timeout` 控制。 |
| | `allow_internet_access` / `allowInternetAccess` | boolean | 否 | 是否允许公网访问；注意字段命名在请求体（snake_case）与响应体（camelCase）中不一致。 |
| | `lifecycle.on_timeout` | string | 否 | 到期行为，值为 `"pause"`（暂停）或 `"kill"`（释放），优先级高于 `autoPause`。 |
| **模版创建** | `cpuCount` & `memoryMB` | integer | 是 | 必须**同时指定**，且必须匹配平台预设的规格组合（如 1C2G、4C8G），单独传任一值将报错。 |
| | `maxRunningTimeout` | integer | 否 | 最大运行时间（秒），范围 `[300, 604800]`；若与 `autoPauseTime` 同时存在，则 `maxRunningTimeout` 优先生效，到期自动释放。 |

## 使用方式

1. **准备前提**：开通百炼服务、创建 API Key、完成 SLR 授权、获取 `workspace_id`（见 [API 总览与认证](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)）。
2. **构建模版**：
   - 调用 `POST /v3/templates` 创建模版，获取 `templateID` 和 `buildID`。
   - 轮询 `GET /templates/{templateID}/builds/{buildID}/status` 直至 `status="ready"`。
3. **管理实例**：
   - 创建：`POST /sandboxes`，传入 `templateID` 等参数。
   - 连接：`POST /sandboxes/{sandboxID}/connect` 获取 `domain`、`envdAccessToken` 等数据面凭证。
   - 控制：`POST /sandboxes/{sandboxID}/pause` 或 `/resume`；`DELETE /sandboxes/{sandboxID}` 释放。
4. **查询与调试**：
   - 列举：`GET /v2/sandboxes`（实例）、`GET /v2/templates`（模版）。
   - 查看详情：`GET /sandboxes/{sandboxID}`、`GET /templates/{templateID}`。

## 限制和注意事项

- **地域限制**：Endpoint 仅支持 `cn-beijing`，其他地域请求将失败。
- **资源规格约束**：模版的 `cpuCount` 与 `memoryMB` 必须成对出现且匹配平台规格表，否则创建模版返回 400。
- **实例生命周期**：`timeout` 最小值为 300 秒（5 分钟），最大值为 604800 秒（7 天）；`autoResume` 仅在实例处于 `paused` 状态且连接请求中启用时生效。
- **模版删除保护**：调用 `DELETE /templates/{templateCode}` 前，必须确保该模版下无 `running` 或 `paused` 实例，否则返回 409 错误并附带关联实例 ID。
- **网络配置差异**：`networkConfig.denyOut` 在模版创建时**不支持域名**（仅 IPv4/IPv6/CIDR），但 `network.allowOut` 支持；而实例创建时的 `network.allowOut`/`denyOut` 字段均支持域名（见 [创建实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md)）。

## 来源文档

- [API 总览与认证](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)
- [实例管理](../../raw/application-api-reference/sandbox-api/sandbox-api-instances.md)
- [创建实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md)
- [获取实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-get.md)
- [列举实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-list.md)
- [连接实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-connect.md)
- [暂停实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-pause.md)
- [恢复实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-resume.md)
- [释放实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-delete.md)
- [模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md)
- [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)
- [获取模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-get.md)
- [列举模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-list.md)
- [更新模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-update.md)
- [获取构建状态](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-build-status.md)
- [删除模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-delete.md)


