# [sandbox](../guides/sandbox.md) api

Sandbox API 是阿里云百炼提供的沙箱实例与模版全生命周期管理接口，兼容 E2B 协议，支持开发者按需创建、连接、暂停、恢复和释放隔离的计算环境。所有请求通过阿里云百炼 API Key 鉴权，Endpoint 按工作空间与地域拼装。该 API 专为 AI 应用编排、代码执行沙箱、浏览器自动化等场景设计，不封装为百炼统一 `Result<T>` 结构，响应体贴近 E2B 原生格式。

## 支持的模型/功能

Sandbox API 不直接提供“模型”推理能力，而是提供**可编程沙箱环境**，其底层运行时基于 envd 构建，支持以下预置镜像（通过 `fromImage` 指定）：
- `code-interpreter-v1`：轻量级 Python 执行环境（默认）
- `browser`：含 Chromium 的无头浏览器环境
- `all-in-one`：集成代码解释器、浏览器与常见工具链的全能环境

所有沙箱均支持：
- 实例级网络策略（出口白名单/黑名单、公网访问开关）
- 文件挂载（通过 `mntConfig` 挂载工作空间内文件）
- 环境变量注入（`envVars` 实例级 / `envConfig` 模版级）
- 生命周期自动管理（超时暂停、自动恢复、最大运行时间强制释放）

> **注意**：文档中多次出现 `allow_public_traffic`、`allowOut`、`denyOut` 等字段名变体（如 `allow_internet_access` vs `allowPublicTraffic`），实际使用以 [API 总览与认证](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md) 中定义的字段为准；部分旧文档示例仍沿用 E2B 命名习惯，但服务端已统一映射，开发者应优先参考最新接口定义。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `Authorization` | Header | string | 是 | `Bearer <your-api-key>`，百炼 API Key |
| `templateID` | 请求体（创建实例）或路径（获取/更新模版） | string | 是（创建实例/获取模版） | 模版唯一标识，由 `/v3/templates` 创建返回 |
| `sandboxID` | 路径参数（除 `/sandboxes` 外所有实例操作） | string | 是 | 实例唯一 ID，格式为 `sbx-xxx`，由 `/sandboxes` 创建返回 |
| `timeout` | 请求体（创建/连接/恢复实例） | integer | 否 | 实例生命周期或连接会话超时时间（秒），范围 `[300, 604800]` |
| `autoPause` / `lifecycle.on_timeout` | 请求体（创建实例） | boolean / string | 否 | 控制超时后行为：`true` 或 `"pause"` 表示暂停；`"kill"` 表示释放（需配合 `maxRunningTimeout`） |
| `maxRunningTimeout` | 请求体（创建/更新模版） | integer | 否 | 模版级最大运行时间（秒），优先生效；若仅设 `autoPauseTime` 则到期暂停 |

> **注意**：`networkConfig.denyOut` 在 [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md) 中明确注明“**不支持域名**”，但 [获取实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-get.md) 的响应示例中 `network.denyOut` 出现了 CIDR 格式（如 `"10.0.0.0/8"`），符合规范；若传入域名将被忽略或报错，务必遵循文档约束。

## 使用方式

### 1. 初始化配置
- 获取工作空间 ID（控制台右上角下拉菜单）
- 开通服务并创建 API Key：[控制台链接](https://bailian.console.aliyun.com/?tab=model#/api-key)
- 完成 SLR 授权（首次使用必需）：详见 [快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md)

### 2. Endpoint 拼装
```
https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox
```
当前仅支持 `cn-beijing` 地域。

### 3. 典型流程
1. **创建模版**：调用 `POST /v3/templates`，指定 `cpuCount`/`memoryMB`/`fromImage` 等，获取 `templateID` 和 `buildID`
2. **等待构建就绪**：轮询 `GET /templates/{templateID}/builds/{buildID}/status`，直到 `status: "ready"`
3. **创建实例**：调用 `POST /sandboxes`，传入 `templateID` 及 `timeout`、`allow_internet_access` 等配置
4. **连接使用**：调用 `POST /sandboxes/{sandboxID}/connect` 获取 `domain` 与 `envdAccessToken`，用于数据面通信
5. **管理状态**：按需调用 `/pause`、`/resume`、`/delete`

E2B 官方 SDK（如 Python `e2b` 包）可直接接入，只需将 `api_key` 设为 `e2b_${ALIYUN_UID}` 即可，详见 [实例管理与使用](../../raw/application-user-guide/sandbox/sandbox-sdk.md)。

## 限制和注意事项

- **地域限制**：当前仅支持 `cn-beijing`，Endpoint 中 region 固定不可更改。
- **资源规格**：`cpuCount` 与 `memoryMB` 必须匹配平台预设组合（如 `1CPU+2048MB`、`4CPU+8192MB`），单独修改任一参数将导致 400 错误。
- **模版删除保护**：若模版关联任何 `running` 或 `paused` 实例，`DELETE /templates/{templateCode}` 将返回 409，必须先调用 `DELETE /sandboxes/{sandboxID}` 释放所有实例。
- **构建状态依赖**：`templateID` 创建后需等待 `buildStatus: "ready"` 才能创建实例；模版更新（`PUT /templates/{templateCode}`）同样触发新构建，旧版本实例不受影响，但新实例必须基于新 `buildID`。
- **鉴权特殊性**：E2B SDK 中的 `X-API-Key` 头仅用于协议兼容，**业务鉴权完全依赖 `Authorization: Bearer <your-api-key>`**，此点在 [API 总览与认证](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md) 中有明确强调。

## 来源文档

- [API 总览与认证](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)
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
- [实例管理](../../raw/application-api-reference/sandbox-api/sandbox-api-instances.md)


