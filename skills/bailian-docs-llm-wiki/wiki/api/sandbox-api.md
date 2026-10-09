# sandbox api

Sandbox API 是阿里云百炼提供的沙箱实例与模版全生命周期管理接口，兼容 E2B 协议，支持开发者通过 RESTful 方式创建、查询、控制沙箱环境。所有请求需经阿里云百炼 AI 网关转发，并使用百炼 API Key 鉴权。该 API 分为实例管理与模版管理两大能力域，覆盖从镜像构建、实例启停到网络/生命周期配置的完整链路。

## 支持的模型/功能

Sandbox API 不直接提供大模型推理能力，而是为代码执行、浏览器自动化等场景提供**隔离、可控的运行时环境**。其核心能力分为两类：

- **模版（Template）管理**：定义沙箱的底层镜像、资源规格（CPU/内存）、网络策略、环境变量及文件挂载。支持基于官方镜像（如 `code-interpreter-v1`、`browser`、`all-in-one`）或自定义基础镜像构建；模版构建状态需显式轮询确认就绪后方可创建实例。详见 [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)。
- **实例（Sandbox）管理**：基于已就绪模版动态创建、连接、暂停、恢复和释放沙箱实例。实例支持自动超时暂停（`autoPause`）、连接时自动恢复（`autoResume`）、公网访问控制（`allow_internet_access`）、细粒度网络规则（`network.allowOut`/`denyOut`）及元数据标注（`metadata`）。所有实例操作均兼容 E2B SDK 的对应方法（如 `connect()`、`pause()`），详见 [实例管理](../../raw/application-api-reference/sandbox-api/sandbox-api-instances.md)。

> **注意**：文档 1 中列出的 `/v2/sandboxes`（列举实例）与 `/v3/templates`（创建模版）为当前主用路径；而文档 2 的目录结构中仍引用旧路径如 `/sandboxes`（创建实例），实际应以文档 1 和各子文档的接口定义为准，避免混淆。

## 关键参数

| 参数类别 | 参数名 | 类型 | 必填 | 说明 | 来源示例 |
|----------|--------|------|------|------|----------|
| **通用鉴权** | `Authorization: Bearer <api-key>` | Header | 是 | 百炼 API Key，**非 E2B 的 `X-API-Key`**；后者仅用于协议兼容占位 | [API 总览与认证](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md) |
| **实例创建** | `templateID` | string | 是 | 已构建完成（`buildStatus=ready`）的模版 ID，否则返回 409 | [创建实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md) |
| | `timeout` | integer | 否 | 实例生命周期秒数（300–604800），到期行为由 `lifecycle.on_timeout` 控制 | |
| | `lifecycle.on_timeout` | string | 否 | 到期动作，`"pause"`（暂停）或 `"terminate"`（释放）；若未指定，默认为 `pause` | |
| | `network.allowOut` / `denyOut` | array<string> | 否 | 出口白名单/黑名单，支持域名、CIDR、IPv4/IPv6；`denyOut` 不支持域名 | [创建实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md) |
| **模版创建** | `cpuCount` / `memoryMB` | integer | 是 | 必须同时指定，且必须匹配平台预设规格组合（如 1C2G、4C8G） | [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md) |
| | `maxRunningTimeout` | integer | 否 | 模版级最大运行时间（秒），优先级高于 `autoPauseTime`；两者均未传时默认 604800 秒 | |

## 使用方式

1. **准备环境**：开通百炼服务，[在控制台创建 API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)，并完成 SLR 授权（见[快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md)）；获取工作空间 ID（`workspace_id`）。
2. **拼接 Endpoint**：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox`（当前仅支持 `cn-beijing` 地域）。
3. **创建模版**：
   - 调用 `POST /v3/templates` 提交模版配置；
   - 用响应中的 `buildID` 轮询 `GET /templates/{templateID}/builds/{buildID}/status`，直至 `status="ready"`。
4. **创建并管理实例**：
   - `POST /sandboxes` 创建实例（传 `templateID`）；
   - `GET /sandboxes/{sandboxID}` 获取实例详情（含 `domain` 和 `envdAccessToken`）；
   - `POST /sandboxes/{sandboxID}/connect` 获取实时连接凭证（推荐用于长连接场景）；
   - `POST /sandboxes/{sandboxID}/pause` / `POST /sandboxes/{sandboxID}/resume` 控制状态；
   - `DELETE /sandboxes/{sandboxID}` 彻底释放资源。
5. **SDK 集成**：可直接使用 E2B 官方 SDK（如 Python 的 `e2b` 包），但需将 `api_key` 设为 `e2b_${ALIYUN_UID}`，并将 `base_url` 指向百炼 Endpoint —— 具体配置见 [实例管理与使用](../../raw/application-user-guide/sandbox/sandbox-sdk.md)。

## 限制和注意事项

- **地域限制**：Endpoint 中 `region` 固定为 `cn-beijing`，不支持其他地域。
- **资源规格约束**：`cpuCount` 与 `memoryMB` 必须成对出现，且仅允许平台预设的组合（如 1C2048MB、4C8192MB），非法组合返回 400。
- **模版删除保护**：若模版存在 `running` 或 `paused` 状态的实例，`DELETE /templates/{templateCode}` 将返回 409 错误，并在响应体中明确列出冲突的 `sandboxId` —— 必须先调用 `DELETE /sandboxes/{sandboxID}` 释放所有实例。
- **网络规则差异**：`network.denyOut` 仅支持 IPv4/IPv6/CIDR，**不支持域名**（文档 10、12 明确说明），而 `allowOut` 支持域名；此限制在创建/更新模版时生效。
- **E2B 兼容性边界**：除 `PUT /templates/{templateCode}`（模版更新）为百炼扩展协议外，其余接口严格兼容 E2B v1；但百炼侧不使用 E2B 的 `X-API-Key` 做业务鉴权，仅认 `Authorization: Bearer` 头 —— 此关键差异已在 [API 总览与认证](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md) 中强调。

## 来源文档

- [API 总览与认证](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)
- [实例管理](../../raw/application-api-reference/sandbox-api/sandbox-api-instances.md)
- [创建实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md)
- [获取实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-get.md)
- [连接实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-connect.md)
- [列举实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-list.md)
- [释放实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-delete.md)
- [暂停实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-pause.md)
- [模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md)
- [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)
- [获取模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-get.md)
- [更新模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-update.md)
- [获取构建状态](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-build-status.md)
- [删除模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-delete.md)
- [列举模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-list.md)
- [恢复实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-resume.md)


