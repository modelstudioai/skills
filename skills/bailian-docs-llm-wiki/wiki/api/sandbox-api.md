# [sandbox](../guides/sandbox.md) api

Sandbox API 是阿里云百炼平台提供的沙箱实例与模版全生命周期管理接口，兼容 E2B 协议，面向需要动态创建、运行和销毁隔离计算环境的 AI 应用场景。所有请求通过阿里云百炼 API Key 鉴权，经百炼 AI 网关转发至管控面。开发者可直接调用 REST 接口或使用 E2B 官方 SDK（需注意鉴权差异）[API 总览与认证](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)。

## 支持的模型/功能

Sandbox API 不提供“模型”推理能力，而是提供**沙箱环境编排能力**，核心功能分为两类：

- **模版管理（Template）**：定义沙箱的基础设施规格（CPU、内存）、基础镜像、网络策略、环境变量、挂载配置等不可变模板。模版需经构建（build）流程生成可运行镜像，状态变为 `ready` 后方可创建实例。支持创建、列举、获取、更新、查询构建状态和删除 [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)。
- **实例管理（Instance）**：基于已就绪模版启动具体沙箱实例，支持按需启停、连接、释放。实例具备独立域名、访问 Token 和完整资源隔离，支持自动暂停/恢复、超时控制与网络精细化管控 [创建实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md)。

> **注意**：文档中多次出现 `POST /templates` 与 `POST /v3/templates` 并存的描述（如文档 11），但实际生产环境仅 `POST /v3/templates` 为当前有效路径；`/templates` 路由已废弃，调用将返回 404。请以 [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md) 中明确声明的 `/v3/templates` 为准。

## 关键参数

### 实例创建（`POST /sandboxes`）
- `templateID`（必填，string）：已构建完成的模版 ID，未就绪时返回 409。
- `timeout`（可选，integer）：实例生命周期上限，单位秒，范围 `[300, 604800]`（5 分钟 ~ 7 天）。
- `allow_internet_access`（可选，boolean）：是否允许公网出向流量（等价于 `network.allowPublicTraffic`）。
- `lifecycle.on_timeout`（可选，string）：超时后行为，`"pause"`（暂停）或 `"terminate"`（释放），默认 `"terminate"`。
- `network.allowOut` / `denyOut`（可选，array<string>）：出口白名单/黑名单，支持域名、IP、CIDR；注意 `denyOut` **不支持域名**（见 [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)）。

### 模版创建（`POST /v3/templates`）
- `cpuCount` 与 `memoryMB`（必填，integer）：必须**同时指定**，且必须匹配平台预设的规格组合（如 `1C2G`, `4C8G`），单独传任一值将报错。
- `autoPauseTime` 与 `maxRunningTimeout`（可选，integer）：两者逻辑互斥——仅传 `autoPauseTime` 则到期暂停；两者都传则 `maxRunningTimeout` 优先生效（到期强制释放）；均不传则默认最大运行时间为 7 天。

## 使用方式

1. **准备环境**：开通百炼服务、创建 API Key、完成 SLR 授权、获取 `workspace_id`（见 [API 总览与认证](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)）。
2. **拼装 Endpoint**：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox`（当前仅支持 `cn-beijing` 地域）。
3. **模版工作流**：
   - `POST /v3/templates` 提交模版定义 → 获取 `templateID` 和 `buildID`；
   - `GET /templates/{templateID}/builds/{buildID}/status` 轮询构建状态，直至 `status: "ready"`；
4. **实例工作流**：
   - `POST /sandboxes` 基于就绪模版创建实例 → 获取 `sandboxID`；
   - `POST /sandboxes/{sandboxID}/connect` 获取 `domain` 和 `envdAccessToken` 用于数据面交互；
   - `POST /sandboxes/{sandboxID}/pause` / `POST /sandboxes/{sandboxID}/resume` 控制运行状态；
   - `DELETE /sandboxes/{sandboxID}` 彻底释放资源。

所有请求必须携带 `Authorization: Bearer <your-api-key>` Header。E2B SDK 可用，但须忽略其 `X-API-Key` 字段，仅用百炼 API Key 鉴权。

## 限制和注意事项

- **地域限制**：Endpoint 中 `region` 固定为 `cn-beijing`，不支持其他地域。
- **资源规格强约束**：模版的 `cpuCount`/`memoryMB` 必须成对出现且匹配平台规格表，否则创建失败（400）。
- **实例状态依赖**：暂停中的实例无法再次暂停；已释放的实例无法恢复；模版存在活跃实例（`running` 或 `paused`）时禁止删除（409）。
- **网络配置差异**：`allowOut` 支持域名（如 `"example.com"`），但 `denyOut` **仅支持 IP/CIDR**（如 `"10.0.0.0/8"`），传入域名将被静默忽略或导致构建失败。
- **响应结构**：所有接口返回原生 E2B 兼容格式，**不封装为百炼统一 `Result<T>` 结构**，错误响应体为 `{ "code": xxx, "message": "xxx", "requestID": "xxx" }`（见 [API 总览与认证](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)）。
- **SDK 兼容性**：E2B SDK 的 `connect()`、`pause()`、`resume()` 等方法可直接调用，但 `get_info()` 返回字段可能比百炼原生接口少（如缺失 `network`、`lifecycle` 等扩展字段），建议优先使用百炼 REST 接口获取完整信息。

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
- [获取模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-get.md)
- [列举模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-list.md)
- [更新模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-update.md)
- [获取构建状态](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-build-status.md)
- [删除模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-delete.md)


