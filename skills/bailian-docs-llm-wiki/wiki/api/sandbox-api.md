# [sandbox](../guides/sandbox.md) api

Sandbox API 是阿里云百炼提供的沙箱环境生命周期管理接口，兼容 E2B 协议，支持模版构建与实例的创建、连接、暂停、恢复和释放。所有请求需通过阿里云百炼 API Key 鉴权，并按工作空间与地域拼装 Endpoint。该 API 服务于代码执行、浏览器自动化等需要隔离运行时的场景，不封装为百炼统一 `Result<T>` 结构，响应体贴近 E2B 原生格式。

## 支持的模型/功能

Sandbox API 不直接提供“模型”推理能力，而是提供**可定制化沙箱环境的托管服务**，其核心能力分为两类：

- **模版（Template）管理**：定义沙箱基础镜像、资源规格（CPU / 内存）、网络策略、环境变量、文件挂载等静态配置。支持基于官方镜像（如 `code-interpreter-v1`、`browser`、`all-in-one`）或自定义镜像构建，详见 [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)。
- **实例（Sandbox）管理**：基于已构建完成（`buildStatus: "ready"`）的模版动态创建、连接、控制运行中沙箱。支持带状态暂停/恢复、自动超时策略、公网访问控制及细粒度网络规则（白名单/黑名单），详见 [创建实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md)。

> **注意**：文档 1 中称“Sandbox API 兼容 E2B 协议”，但文档 12 明确指出更新模版接口（`PUT /templates/{templateCode}`）是“阿里云百炼扩展协议，不声明完全兼容 E2B Update Template v2”。开发者不应假设所有模版操作均与 E2B 官方行为一致。

## 关键参数

| 参数 | 所属接口 | 必填 | 类型 | 说明 |
|------|----------|------|------|------|
| `templateID` | 创建/列举/获取实例 | 是 | string | 模版唯一标识，必须为已构建完成（`status: "ready"`）的模版，否则创建实例返回 409 |
| `timeout` | 创建/连接/恢复实例 | 否 | integer | 实例生命周期或连接会话超时时间（秒），范围 `[300, 604800]`；到期行为由 `lifecycle.on_timeout` 或 `autoPause` 控制 |
| `allow_internet_access` / `allowInternetAccess` | 创建/获取实例 | 否 | boolean | 是否允许实例访问公网；注意字段名在请求体（snake_case）与响应体（camelCase）中不一致 |
| `lifecycle` / `network` | 创建/获取实例 | 否 | object | 生命周期配置（`on_timeout`, `auto_resume`）与网络配置（`allowOut`, `denyOut`, `allowPublicTraffic`）；文档 3 和文档 5 字段结构存在嵌套差异，建议以文档 5 的响应结构为准 |
| `cpuCount` & `memoryMB` | 创建/更新模版 | 是（创建时）/ 同时传（更新时） | integer | 资源规格，必须匹配平台支持的组合；更新时二者须同时提供，否则保留原值 |

## 使用方式

1. **准备前提**：开通百炼服务、创建 API Key、完成 SLR 授权、获取 `workspace_id`（见 [API 总览与认证](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)）。
2. **拼装 Endpoint**：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox`（当前仅支持 `cn-beijing` 地域）。
3. **鉴权**：所有请求 Header 携带 `Authorization: Bearer <your-api-key>`；E2B SDK 中的 `X-API-Key` 仅用于协议占位，不参与百炼业务鉴权。
4. **典型流程**：
   - 创建模版 → 查询构建状态（`GET /templates/{templateCode}/builds/{buildID}/status`）→ 等待 `status: "ready"`；
   - 创建实例（`POST /sandboxes`）→ 连接实例（`POST /sandboxes/{sandboxID}/connect`）获取 `domain` 与 `envdAccessToken`；
   - （可选）暂停/恢复实例（`POST /sandboxes/{sandboxID}/pause` / `resume`）；
   - 实例使用完毕后释放（`DELETE /sandboxes/{sandboxID}`）或删除模版（`DELETE /templates/{templateCode}`，需确保无活跃实例）。

## 限制和注意事项

- **地域限制**：Endpoint 中 `region` 固定为 `cn-beijing`，不支持其他地域。
- **模版构建依赖**：创建实例前，模版构建状态必须为 `ready`；若构建失败（`status: "error"`），需检查 [获取构建状态](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-build-status.md) 返回的 `reason` 字段定位问题。
- **实例释放与模版删除强约束**：删除模版前，必须确保该模版下无 `running` 或 `paused` 状态的实例，否则返回 409 错误并附带关联实例 ID（见 [删除模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-delete.md)）。
- **分页与路由兼容性**：列举接口存在多版本路径（如 `/v2/sandboxes`、`/v2/templates`），同时兼容旧路由（`/sandboxes`、`/templates`），但推荐使用带版本号的路径以保证稳定性。
- **错误处理**：HTTP 状态码含义明确（400 参数错误、401 鉴权失败、404 资源不存在、409 状态冲突、500 内部异常），错误响应体结构统一（含 `code`, `message`, `requestID`），便于程序化处理。

## 来源文档

- [API 总览与认证](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)
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
- [更新模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-update.md)
- [获取构建状态](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-build-status.md)
- [删除模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-delete.md)
- [列举模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-list.md)
- [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)


