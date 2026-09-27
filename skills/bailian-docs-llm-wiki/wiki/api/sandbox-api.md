# [sandbox](../guides/sandbox.md) api

Sandbox API 是阿里云百炼提供的沙箱实例与模版全生命周期管理接口，兼容 E2B 协议，支持开发者通过 RESTful 方式创建、查询、控制沙箱环境。所有请求需经阿里云百炼 AI 网关转发，并使用百炼 API Key 鉴权。该 API 不封装为百炼统一 `Result<T>` 结构，响应体贴近 E2B 原生格式，便于与 E2B SDK 无缝集成。

## 支持的模型/功能

Sandbox API 提供两类核心资源管理能力：**沙箱实例（[sandbox](../guides/sandbox.md)）** 和 **沙箱模版（template）**。

- **实例管理**：支持创建、列举、获取详情、连接、暂停、恢复和释放实例，覆盖完整运行时生命周期。实例基于已构建完成的模版启动，状态包括 `running`、`paused` 等，支持自动暂停与连接时自动恢复。
- **模版管理**：支持创建、列举、获取、更新、查询构建状态及删除模版。模版定义了沙箱的基础镜像、资源配置（CPU/内存）、网络规则、环境变量等；每次更新均触发新版本构建，构建状态需显式轮询确认是否就绪（`status: "ready"`）后方可创建实例。

> **注意**：文档中 `/v2/sandboxes` 与 `/sandboxes` 均被标注为“兼容路由”，但 [API 总览与认证](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md) 明确将 `/sandboxes` 列为创建实例的标准路径，而 `/v2/sandboxes` 仅用于列举；实际使用中应严格区分路径语义，避免误用 `/v2/sandboxes` 发起创建请求。

## 关键参数

### 实例创建（`POST /sandboxes`）
- `templateID`（必填，string）：已构建完成的模版 ID，未就绪时返回 409。
- `timeout`（可选，integer）：实例生命周期上限，单位秒，范围 `[300, 604800]`。
- `allow_internet_access`（可选，boolean）：是否允许公网访问（等价于 `network.allowPublicTraffic`）。
- `lifecycle.on_timeout`（可选，string）：超时行为，如 `"pause"`；也可传对象形式 `{"action": "pause"}`。
- `autoResume`（可选，boolean）：连接时是否自动恢复暂停实例（兼容 `{"enabled": true}` 对象形式）。

### 模版创建（`POST /v3/templates`）与更新（`PUT /templates/{templateCode}`）
- `cpuCount` 与 `memoryMB`（必填且必须同时指定）：需匹配平台预设规格组合，不支持任意值。
- `maxRunningTimeout` 与 `autoPauseTime`（可选）：若两者均传，`maxRunningTimeout` 优先生效（到期自动释放）；仅传 `autoPauseTime` 则到期暂停。
- `networkConfig.allowOut`（支持域名）、`denyOut`（**仅支持 CIDR/IP，不支持域名**）：网络出口控制需注意字段限制差异。

## 使用方式

1. **准备前提**：开通百炼服务、创建 API Key、完成 SLR 授权、获取工作空间 ID（`workspace_id`）。
2. **拼装 Endpoint**：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox`（当前仅支持 `cn-beijing` 地域）。
3. **鉴权**：所有请求 Header 中携带 `Authorization: Bearer <your-api-key>`；E2B SDK 的 `X-API-Key` 仅作协议占位，**不参与百炼业务鉴权**，建议填 `e2b_${ALIYUN_UID}`。
4. **典型流程**：
   - 创建模版 → 轮询 `/templates/{templateID}/builds/{buildID}/status` 直至 `status: "ready"`；
   - 调用 `POST /sandboxes` 创建实例；
   - 通过 `GET /sandboxes/{sandboxID}` 或 `POST /sandboxes/{sandboxID}/connect` 获取数据面访问凭证（`domain` + `envdAccessToken`）；
   - 按需调用 `/pause`、`/resume` 或 `/delete` 控制实例。

> **注意**：[创建实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md) 文档明确要求模版“已构建完成”，而 [获取构建状态](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-build-status.md) 文档强调“构建状态变为 `ready` 后才能创建实例”——二者逻辑一致，但开发者需主动轮询构建状态，API 不提供阻塞式等待。

## 限制和注意事项

- **地域限制**：Endpoint 中 `region` 固定为 `cn-beijing`，暂不支持其他地域。
- **资源规格**：`cpuCount`/`memoryMB` 必须匹配平台预设组合，非法值导致 400 错误；具体组合请参考控制台或 [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md) 文档说明。
- **网络配置差异**：`allowOut` 支持域名（如 `"example.com"`），但 `denyOut` **仅支持 CIDR 和 IP 地址**（如 `"10.0.0.0/8"`），传入域名将被忽略或报错。
- **模版删除约束**：删除模版前必须确保无任何 `running` 或 `paused` 实例，否则返回 409 并附带关联实例 ID（见 [删除模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-delete.md)）。
- **错误处理**：HTTP 409 表示状态冲突（如模版未就绪即创建实例、模版有活跃实例时尝试删除）；501 表示接口暂未实现（如部分 E2B 协议接口尚未支持）。

## 来源文档

- [API 总览与认证](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)
- [实例管理](../../raw/application-api-reference/sandbox-api/sandbox-api-instances.md)
- [创建实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md)
- [列举实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-list.md)
- [获取实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-get.md)
- [暂停实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-pause.md)
- [恢复实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-resume.md)
- [释放实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-delete.md)
- [连接实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-connect.md)
- [列举模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-list.md)
- [获取模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-get.md)
- [更新模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-update.md)
- [获取构建状态](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-build-status.md)
- [模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md)
- [删除模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-delete.md)
- [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)


