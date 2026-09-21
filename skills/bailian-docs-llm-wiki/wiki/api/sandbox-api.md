# [sandbox](../guides/sandbox.md) api

Sandbox API 是阿里云百炼提供的沙箱实例与模版全生命周期管理接口，兼容 E2B 协议，支持创建、连接、暂停、恢复、释放实例，以及模版的构建、更新与状态查询。所有请求通过阿里云百炼 API Key 鉴权，Endpoint 按工作空间 ID 和地域（当前仅 `cn-beijing`）拼装。开发者可直接调用 REST 接口，或使用 E2B 官方 SDK（需注意鉴权方式差异）[API 总览与认证](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)。

## 支持的模型/功能

Sandbox API 不提供“模型”推理能力，而是提供**沙箱运行时环境的编排与管控能力**，核心功能分为两类：

- **实例管理**：支持基于模版快速创建隔离的计算实例（`POST /sandboxes`），并提供完整的生命周期操作：列举（`GET /v2/sandboxes`）、获取详情（`GET /sandboxes/{sandboxID}`）、连接（`POST /sandboxes/{sandboxID}/connect`）、暂停（`POST /sandboxes/{sandboxID}/pause`）、恢复（`POST /sandboxes/{sandboxID}/resume`）和释放（`DELETE /sandboxes/{sandboxID}`）[实例管理](../../raw/application-api-reference/sandbox-api/sandbox-api-instances.md)。
- **模版管理**：支持定义可复用的沙箱环境配置，包括 CPU/内存规格、基础镜像、网络规则、环境变量等；提供模版的创建（`POST /v3/templates`）、列举（`GET /v2/templates`）、获取（`GET /templates/{templateCode}`）、更新（`PUT /templates/{templateCode}`）、构建状态查询（`GET /templates/{templateCode}/builds/{buildID}/status`）和删除（`DELETE /templates/{templateCode}`）[模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md)。

> **注意**：文档中多次出现 `POST /templates` 与 `POST /v3/templates` 并存的描述（如[创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)），但官方推荐路径为 `/v3/templates`；`/templates` 仅为兼容路由，新集成应优先使用 `/v3/templates`。

## 关键参数

- **`templateID` / `templateCode`**：模版唯一标识，创建模版后返回，后续所有模版操作（获取、更新、删除、构建查询）及实例创建均需传入。模版必须处于 `ready` 构建状态才可创建实例，否则返回 409 [创建实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md)。
- **`sandboxID`**：实例唯一标识，创建成功后返回，用于所有实例级操作（连接、暂停、恢复、释放、获取详情）。
- **`timeout`**：通用超时参数，单位秒，取值范围 `[300, 604800]`（5 分钟至 7 天）。在创建实例、连接实例、恢复实例时均可指定，控制实例自动终止或暂停的时间点。
- **`lifecycle` 对象**：精细化控制实例生命周期行为。`on_timeout`（或 `onTimeout`）指定到期动作（`"pause"` 或 `"kill"`），`auto_resume`（或 `autoResume`）控制连接时是否自动恢复暂停实例。该字段在创建和获取实例响应中均有体现，但语义需以[获取实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-get.md)文档为准。
- **`network` 配置**：支持细粒度网络管控。`allowOut`（出口白名单，支持域名/IP/CIDR）、`denyOut`（出口黑名单，**仅支持 IP/CIDR，不支持域名**）、`allowPublicTraffic`（布尔开关）等字段在模版创建（`networkConfig`）和实例创建（`network`）中均存在，但字段名和嵌套层级略有差异，需按对应接口文档使用。

## 使用方式

1. **准备环境**：开通百炼服务，创建 API Key，并完成 SLR 授权；从控制台获取 `workspace_id`。
2. **构建模版**：调用 `POST /v3/templates` 提交模版配置（含 `cpuCount`/`memoryMB` 等必填项），获取 `templateID` 和 `buildID`；轮询 `GET /templates/{templateID}/builds/{buildID}/status` 直至 `status: "ready"`。
3. **创建实例**：调用 `POST /sandboxes`，传入 `templateID` 及可选参数（如 `timeout`, `allow_internet_access`, `envVars`），获取 `sandboxID`。
4. **访问实例**：调用 `POST /sandboxes/{sandboxID}/connect` 获取 `domain` 和 `envdAccessToken`，用于后续数据面通信（如执行代码、上传文件）。
5. **管理实例**：根据需要调用 `GET /sandboxes/{sandboxID}` 查看状态，`POST /sandboxes/{sandboxID}/pause` 暂停，`POST /sandboxes/{sandboxID}/resume` 恢复，或 `DELETE /sandboxes/{sandboxID}` 彻底释放资源。

所有请求需携带 `Authorization: Bearer <your-api-key>` Header。Endpoint 格式为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox`。

## 限制和注意事项

- **地域限制**：当前 Sandbox API 仅支持 `cn-beijing` 地域，Endpoint 中 `region` 字段不可更改。
- **资源规格**：CPU 与内存必须同时指定，且必须匹配平台预设的规格组合（如 `1 vCPU + 2048 MB`），单独修改任一参数将导致创建失败。
- **网络黑名单限制**：`denyOut` 字段在模版创建（`networkConfig`）和实例创建（`network`）中均不支持域名，仅接受 IPv4、IPv6 或 CIDR 表达式；若文档中出现“支持域名”的描述，以[创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)中明确说明的限制为准。
- **模版删除约束**：删除模版前，必须确保其下无任何运行中（`running`）或已暂停（`paused`）的实例，否则返回 409 错误，并在响应体中列出阻塞的 `sandboxId`。
- **E2B 兼容性说明**：虽然接口路径与部分字段名兼容 E2B，但鉴权方式（仅认 `Authorization: Bearer`）、Endpoint 拼装、扩展字段（如 `bailianSandboxId`, `trafficAccessToken`）及部分行为（如模版更新为阿里云百炼自定义协议）均为百炼特有，不可直接套用 E2B 文档中的鉴权或错误处理逻辑。

## 来源文档

- [实例管理](../../raw/application-api-reference/sandbox-api/sandbox-api-instances.md)
- [创建实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md)
- [API 总览与认证](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)
- [连接实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-connect.md)
- [获取实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-get.md)
- [列举实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-list.md)
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


