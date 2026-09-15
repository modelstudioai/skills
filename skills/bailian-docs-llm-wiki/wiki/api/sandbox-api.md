# [sandbox](../guides/sandbox.md) api

Sandbox API 是阿里云百炼平台提供的沙箱实例与模版全生命周期管理接口，兼容 E2B 协议（部分扩展字段与行为为百炼自定义），通过百炼 AI 网关转发。开发者可基于该 API 创建、查询、连接、暂停/恢复及释放沙箱实例，并管理模版的构建与配置。所有调用需使用百炼 API Key 鉴权，Endpoint 按工作空间与地域动态生成。

## 支持的模型/功能

Sandbox API 不直接提供大模型推理能力，而是为运行代码/Agent 的沙箱环境提供基础设施支持，核心能力包括：

- **实例管理**：创建（`POST /sandboxes`）、列举（`GET /v2/sandboxes`）、获取详情（`GET /sandboxes/{sandboxID}`）、连接（`POST /sandboxes/{sandboxID}/connect`）、暂停（`POST /sandboxes/{sandboxID}/pause`）、恢复（`POST /sandboxes/{sandboxID}/resume`）和释放（`DELETE /sandboxes/{sandboxID}`）沙箱实例。
- **模版管理**：创建（`POST /v3/templates`）、列举（`GET /v2/templates`）、获取（`GET /templates/{templateCode}`）、更新（`PUT /templates/{templateCode}`）、查询构建状态（`GET /templates/{templateCode}/builds/{buildID}/status`）和删除（`DELETE /templates/{templateCode}`）沙箱模版。
- **网络与生命周期扩展**：支持细粒度网络规则（如 `allowOut`/`denyOut` 域名与 CIDR 白黑名单）、自动暂停/恢复策略（`autoPause`、`lifecycle.on_timeout`）、超时控制（`timeout`、`maxRunningTimeout`）等百炼增强能力。

> **注意**：文档中列举的 `/sandboxes`（v1）与 `/v2/sandboxes` 路径均被支持，但推荐使用 `/v2/sandboxes` 进行实例列举，因其明确支持分页与过滤；而 `/sandboxes` 列举能力未在任一文档中明确定义，仅在[API 总览与认证](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)的表格中作为兼容路由提及，实际行为以 `/v2/sandboxes` 为准。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `Authorization` | Header | string | 是 | `Bearer <your-api-key>`，百炼 API Key，**非 E2B 的 `X-API-Key`**。详见[API 总览与认证](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)。 |
| `templateID` | Request Body (创建实例) / Path (模版操作) | string | 是 | 模版唯一标识，创建实例或操作模版时必需。创建实例前需确保模版构建状态为 `ready`，否则返回 409。参考[创建实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md)与[获取构建状态](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-build-status.md)。 |
| `timeout` | Request Body (创建/连接/恢复实例) | integer | 否 | 实例生命周期或连接会话超时时间（秒），范围 `[300, 604800]`。影响 `autoPause` 行为与资源回收时机。 |
| `allow_internet_access` / `allowInternetAccess` | Request Body (创建) / Response (获取) | boolean | 否 | 控制实例是否可访问公网。注意字段命名在请求体（snake_case）与响应体（camelCase）中不一致，需按上下文区分。 |
| `network` | Request Body (创建/模版) / Response (获取实例) | object | 否 | 网络配置对象，支持 `allowOut`（域名/CIDR 白名单）、`denyOut`（CIDR 黑名单，**不支持域名**）、`allowPublicTraffic` 等子字段。模版级与实例级配置均可生效。 |

## 使用方式

1. **准备环境**：开通百炼服务，创建 API Key，完成 SLR 授权，并获取工作空间 ID 和地域（当前仅支持 `cn-beijing`）。Endpoint 格式为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox`。
2. **创建模版**：调用 `POST /v3/templates` 提交资源配置（`cpuCount`/`memoryMB` 必须匹配平台规格组合）与环境配置（`envConfig`, `networkConfig`）。获取 `templateID` 和 `buildID` 后，轮询 `GET /templates/{templateID}/builds/{buildID}/status` 直至 `status: "ready"`。
3. **创建实例**：调用 `POST /sandboxes`，传入 `templateID` 及可选参数（如 `timeout`, `autoPause`, `lifecycle`）。成功返回 `sandboxID`。
4. **访问实例**：调用 `POST /sandboxes/{sandboxID}/connect` 获取 `domain` 与 `envdAccessToken`，用于后续数据面通信（如 exec、file upload/download）。
5. **管理生命周期**：根据需要调用 `/pause`、`/resume` 或 `/delete`。暂停后实例状态保留，恢复时从断点继续；释放后不可恢复。

## 限制和注意事项

- **地域限制**：当前 Sandbox API 仅支持 `cn-beijing` 地域，`region` 必须为 `cn-beijing`，否则 Endpoint 无效。
- **资源规格约束**：`cpuCount` 与 `memoryMB` 在创建/更新模版时必须同时指定，且必须属于平台预设的合法组合（如 1 vCPU + 2048 MB），单独修改任一值将导致 400 错误。
- **模版删除保护**：若模版关联有 `running` 或 `paused` 状态的实例，`DELETE /templates/{templateCode}` 将返回 409，并在错误响应中明确列出阻塞的 `sandboxId`，需先释放实例再删除模版。
- **E2B 兼容性边界**：虽声明兼容 E2B 协议，但模版更新（`PUT /templates`）为百炼自定义协议，不完全等价于 E2B v2；此外，`X-API-Key` 头部仅用于满足 E2B SDK 格式要求，**百炼业务鉴权完全依赖 `Authorization: Bearer`**，此关键差异已在[API 总览与认证](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)中强调。
- **响应结构差异**：Sandbox API 返回原生 E2B 风格 JSON，**不封装为百炼统一的 `Result<T>` 结构**，开发者需直接解析 HTTP 状态码与响应体。

## 来源文档

- [API 总览与认证](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)
- [创建实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md)
- [列举实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-list.md)
- [获取实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-get.md)
- [连接实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-connect.md)
- [暂停实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-pause.md)
- [释放实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-delete.md)
- [恢复实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-resume.md)
- [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)
- [模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md)
- [列举模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-list.md)
- [获取模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-get.md)
- [更新模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-update.md)
- [获取构建状态](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-build-status.md)
- [删除模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-delete.md)
- [实例管理](../../raw/application-api-reference/sandbox-api/sandbox-api-instances.md)


