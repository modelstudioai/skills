# [sandbox](../guides/sandbox.md) api

Sandbox API 是阿里云百炼提供的沙箱环境生命周期管理接口，兼容 E2B 协议，支持模版构建与实例的创建、连接、暂停、恢复和释放。所有请求通过阿里云百炼 API Key 鉴权，Endpoint 按工作空间与地域拼装，当前仅支持 `cn-beijing` 地域。该 API 专为需要动态执行代码、隔离运行环境或构建 AI Agent 数据面的开发者设计。

## 支持的模型/功能

Sandbox API 不直接提供大模型推理能力，而是提供**可编程的沙箱运行时环境**，其功能围绕两类核心资源展开：

- **模版（Template）**：定义沙箱的底层镜像、资源配置（CPU / 内存）、网络策略、环境变量及挂载文件。支持基于官方镜像（如 `code-interpreter-v1`、`browser`、`all-in-one`）或自定义基础镜像构建；[创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md) 接口返回 `buildID`，需轮询 [获取构建状态](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-build-status.md) 确保状态为 `ready` 后方可创建实例。
- **实例（Sandbox Instance）**：基于就绪模版启动的临时计算单元，具备完整 Linux 环境、联网能力（可配置白/黑名单）与持久化文件系统。支持按需启停、自动超时管理（`timeout` + `on_timeout`），并可通过 `connect` 接口获取数据面访问凭证（`envdAccessToken`、`domain` 等）。

> **注意**：文档中多次出现 `fromImage` 的镜像地址前缀为 `fc-e2b-registry.cn-beijing.cr.aliyuncs.com/runtime/`，但 [API 总览与认证](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md) 明确说明当前仅支持 `cn-beijing` 地域，因此该 registry 地址是唯一有效路径，不存在跨地域镜像拉取场景。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `Authorization: Bearer <api-key>` | Header | string | 是 | 阿里云百炼 API Key，**非 E2B 的 `X-API-Key`**；SDK 中 `X-API-Key` 仅为协议占位，应填 `e2b_${ALIYUN_UID}` |
| `templateID` | 请求体（创建实例） / 路径（获取/删除模版） | string | 是 | 模版唯一标识，来自 `/v3/templates` 创建响应；模版未就绪（`buildStatus != "ready"`）时创建实例将返回 409 |
| `sandboxID` | 路径参数（除 `/sandboxes` 外所有实例接口） | string | 是 | 实例唯一 ID，来自 `/sandboxes` 创建响应 |
| `timeout` | 请求体（创建/连接/恢复实例） | integer | 否 | 生命周期超时时间（秒），范围 `[300, 604800]`；到期行为由 `lifecycle.on_timeout` 控制（如 `"pause"`） |
| `lifecycle.on_timeout` | 请求体（创建实例） | string | 否 | 到期动作，支持 `"pause"`（暂停）或 `"terminate"`（释放）；若同时传 `maxRunningTimeout`（模版级），后者优先生效 |
| `network.allowOut` / `denyOut` | 请求体（创建模版/实例） | array<string> | 否 | 出口流量控制：`allowOut` 支持域名/IP/CIDR；`denyOut` **仅支持 IP/CIDR，不支持域名**（见 [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md) 文档） |

## 使用方式

1. **前置准备**：开通百炼服务、创建 API Key、完成 SLR 授权、获取 `workspace_id`；
2. **构建模版**：
   - 调用 `POST /v3/templates` 提交模版配置；
   - 用返回的 `buildID` 轮询 `GET /templates/{templateCode}/builds/{buildID}/status`，直至 `status == "ready"`；
3. **创建与管理实例**：
   - `POST /sandboxes` 基于就绪模版创建实例；
   - `GET /sandboxes/{sandboxID}` 获取实例详情（含 `domain` 和 `envdAccessToken`）；
   - `POST /sandboxes/{sandboxID}/connect` 刷新访问凭证（可选 `timeout`）；
   - `POST /sandboxes/{sandboxID}/pause` / `POST /sandboxes/{sandboxID}/resume` 控制运行状态；
   - `DELETE /sandboxes/{sandboxID}` 彻底释放资源；
4. **模版维护**：
   - `PUT /templates/{templateCode}` 更新配置并触发新构建；
   - `DELETE /templates/{templateCode}` 删除模版（要求无活跃实例，否则 409）。

## 限制和注意事项

- **地域限制**：Endpoint 中 `region` 固定为 `cn-beijing`，不支持其他地域；
- **资源规格**：`cpuCount` 与 `memoryMB` 必须同时传递，且必须匹配平台预设的组合（如 `1C2G`、`4C8G`），单独传一个将报错；
- **网络配置差异**：`denyOut` 在模版级（`networkConfig`）和实例级（`network`）均不支持域名，仅支持 IPv4/IPv6/CIDR；而 `allowOut` 在两者中均支持域名；
- **E2B 兼容性边界**：除 `PUT /templates/{templateCode}` 为百炼扩展外，其余接口严格兼容 E2B v1 协议；但响应体**不封装为百炼统一 `Result<T>` 结构**，而是直接返回 E2B 原生格式；
- **错误处理**：HTTP 409 表示状态冲突（如模版未就绪、模版有活跃实例、实例非暂停态时调用 `resume`），需根据 `message` 字段判断具体原因；
- **分页机制**：`/v2/sandboxes` 与 `/v2/templates` 均返回扁平数组，无分页元信息，需自行处理 `limit` 与游标逻辑。

## 来源文档

- [API 总览与认证](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)
- [实例管理](../../raw/application-api-reference/sandbox-api/sandbox-api-instances.md)
- [创建实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md)
- [获取实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-get.md)
- [列举实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-list.md)
- [连接实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-connect.md)
- [恢复实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-resume.md)
- [释放实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-delete.md)
- [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)
- [列举模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-list.md)
- [获取模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-get.md)
- [更新模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-update.md)
- [获取构建状态](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-build-status.md)
- [删除模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-delete.md)
- [暂停实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-pause.md)
- [模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md)


