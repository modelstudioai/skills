# sandbox api

Sandbox API 是阿里云百炼提供的[沙箱](../concepts/sandbox.md)实例与模版全生命周期管理接口，兼容 E2B 协议，支持创建、连接、暂停、恢复和释放[沙箱](../concepts/sandbox.md)实例，以及模版的构建、更新与查询。所有请求需通过阿里云百炼 API Key 鉴权，并按工作空间与地域拼装 Endpoint。该 API 专为需要动态执行代码、隔离运行环境的 AI 应用场景设计，不封装为百炼统一 `Result<T>` 结构，响应体贴近 E2B 原生格式。

## 支持的模型/功能

- **实例管理**：支持基于预构建模版创建[沙箱](../concepts/sandbox.md)实例（`POST /sandboxes`），并提供完整生命周期操作：列举（`GET /v2/sandboxes`）、获取详情（`GET /sandboxes/{sandboxID}`）、连接（`POST /sandboxes/{sandboxID}/connect`）、暂停（`POST /sandboxes/{sandboxID}/pause`）、恢复（`POST /sandboxes/{sandboxID}/resume`）和释放（`DELETE /sandboxes/{sandboxID}`）。详见 [实例管理](../../raw/application-api-reference/sandbox-api/sandbox-api-instances.md)。
- **模版管理**：支持自定义沙箱运行环境，包括创建模版（`POST /v3/templates`）、列举（`GET /v2/templates`）、获取详情（`GET /templates/{templateCode}`）、更新配置（`PUT /templates/{templateCode}`）、轮询构建状态（`GET /templates/{templateCode}/builds/{buildID}/status`）及删除（`DELETE /templates/{templateCode}`）。模版构建成功（`status: "ready"`）后方可用于创建实例。详见 [模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md)。
- **资源规格与镜像**：模版支持指定 `cpuCount` 和 `memoryMB`（必须成对设置且匹配平台规格组合），可选挂载文件、配置网络规则（`allowOut`/`denyOut`）、注入环境变量（`envConfig`），并支持从官方镜像（如 `code-interpreter-v1`、`browser`）或自定义镜像构建。基础镜像仓库地址为 `fc-e2b-registry.cn-beijing.cr.aliyuncs.com/runtime/`。

## 关键参数

- **认证与路由**：所有请求必须携带 `Authorization: Bearer <your-api-key>` Header；Endpoint 格式为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox`，其中 `workspace_id` 需从百炼控制台右上角获取。
- **实例创建参数**：
  - `templateID`（必填）：已构建完成的模版 ID；
  - `timeout`（可选）：实例生命周期时间（秒），范围 `[300, 604800]`；
  - `allow_internet_access`（可选）：是否允许公网访问；
  - `lifecycle.on_timeout`（可选）：到期行为，支持 `"pause"`；`auto_resume` 控制连接时是否自动恢复；
  - `network.allowOut`/`denyOut`（可选）：出口流量白/黑名单（支持域名、CIDR、IP）。
- **模版创建/更新参数**：
  - `cpuCount` 与 `memoryMB` 必须同时传且匹配平台规格；
  - `maxRunningTimeout`（可选）：实例最大运行时间（秒），优先级高于 `autoPauseTime`；
  - `mntConfig` 中 `originFileId` 必须为当前工作空间内真实存在的文件 ID；
  - `networkConfig.denyOut` 不支持域名（仅 IPv4/IPv6/CIDR），与 `allow_internet_access` 参数语义不同，需注意区分。

> **注意**：文档 3（创建实例）中 `lifecycle` 字段示例使用对象形式 `{"on_timeout": "pause", "auto_resume": true}`，而文档 5（获取实例）响应中字段名为 `onTimeout`（驼峰）且值为字符串；实际调用应以文档 3 的请求体格式为准，服务端兼容两种写法，但响应字段名统一为 `onTimeout`。此外，文档 12（创建模版）明确要求 `cpuCount` 与 `memoryMB` 必须同时传递，而文档 15（更新模版）说明二者“必须同时传”，否则保留原值——这与文档 12 的强约束一致，开发者应避免单独更新 CPU 或内存。

## 使用方式

1. **前置准备**：开通百炼服务，[创建 API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)，完成 SLR 授权（见 [快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md)），并确认工作空间 ID 与地域（当前仅 `cn-beijing`）。
2. **构建模版**：调用 `POST /v3/templates` 提交模版配置，获取 `templateID` 和 `buildID`；轮询 `GET /templates/{templateID}/builds/{buildID}/status` 直至 `status: "ready"`。
3. **创建与管理实例**：
   - 创建：`POST /sandboxes`，传入 `templateID` 等参数；
   - 连接：`POST /sandboxes/{sandboxID}/connect` 获取 `domain` 与 `envdAccessToken`，用于后续数据面通信；
   - 暂停/恢复：`POST /sandboxes/{sandboxID}/pause` 或 `/resume`，暂停后状态保留，恢复即续跑；
   - 释放：`DELETE /sandboxes/{sandboxID}` 彻底回收资源。
4. **SDK 接入（可选）**：可直接使用 E2B 官方 SDK（如 Python `e2b` 包），但需将 `api_key` 设为 `e2b_${ALIYUN_UID}`，实际鉴权仍依赖 `Authorization` Header。详见 [实例管理与使用](../../raw/application-user-guide/sandbox/sandbox-sdk.md)。

## 限制和注意事项

- **地域与版本限制**：API 当前仅支持 `cn-beijing` 地域；部分接口路径存在多版本（如 `/v2/sandboxes` 与 `/sandboxes`），推荐使用文档 2 明确列出的路径，避免依赖未声明的兼容路由。
- **资源与配额**：实例 `timeout` 和模版 `maxRunningTimeout` 最大值均为 604800 秒（7 天）；模版 `cpuCount`/`memoryMB` 必须匹配平台预设规格组合，非法组合将返回 400 错误。
- **状态依赖**：创建实例前模版必须处于 `ready` 状态，否则返回 409；删除模版前必须确保无 `running` 或 `paused` 实例，否则返回 409 并附带关联实例 ID。
- **错误处理**：HTTP 状态码含义需严格遵循文档 2 定义（如 401=API Key 无效，409=状态冲突）；错误响应体结构统一为 `{ "code": number, "message": string, "requestID": string }`，不嵌套在 `Result` 中。
- **网络配置差异**：`allow_internet_access`（实例级布尔开关）与 `networkConfig.allowOut`（模版级细粒度白名单）作用层级不同，不可混用；`denyOut` 在模版层不支持域名，但在实例层 `network.allowOut` 支持——此差异已在 [API 总览与认证](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md) 中明确说明。

## 来源文档

- [实例管理](../../raw/application-api-reference/sandbox-api/sandbox-api-instances.md)
- [API 总览与认证](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)
- [创建实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md)
- [列举实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-list.md)
- [获取实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-get.md)
- [连接实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-connect.md)
- [暂停实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-pause.md)
- [恢复实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-resume.md)
- [释放实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-delete.md)
- [模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md)
- [列举模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-list.md)
- [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)
- [获取模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-get.md)
- [获取构建状态](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-build-status.md)
- [更新模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-update.md)
- [删除模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-delete.md)


