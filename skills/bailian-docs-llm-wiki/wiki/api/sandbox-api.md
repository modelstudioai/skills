# [sandbox](../guides/sandbox.md) api

Sandbox API 是阿里云百炼提供的沙箱实例与模版全生命周期管理接口，兼容 E2B 协议，用于在隔离环境中运行代码、调试模型或执行可信计算任务。所有请求需通过阿里云百炼 API Key 鉴权，并按工作空间与地域拼装 Endpoint。该 API 分为实例管理与模版管理两大能力域，覆盖创建、查询、连接、暂停、释放等核心操作。

## 支持的模型/功能

- **实例管理**：支持沙箱实例的完整生命周期操作，包括创建（`POST /sandboxes`）、列举（`GET /v2/sandboxes`）、获取详情（`GET /sandboxes/{sandboxID}`）、连接（`POST /sandboxes/{sandboxID}/connect`）、暂停（`POST /sandboxes/{sandboxID}/pause`）、恢复（`POST /sandboxes/{sandboxID}/resume`）和释放（`DELETE /sandboxes/{sandboxID}`）。详见 [实例管理](../../raw/application-api-reference/sandbox-api/sandbox-api-instances.md)。
- **模版管理**：支持沙箱运行环境的预定义与复用，包括创建（`POST /v3/templates`）、列举（`GET /v2/templates`）、获取（`GET /templates/{templateCode}`）、更新（`PUT /templates/{templateCode}`）、查询构建状态（`GET /templates/{templateCode}/builds/{buildID}/status`）和删除（`DELETE /templates/{templateCode}`）。模版构建成功（`status: "ready"`）后方可创建实例。详见 [模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md)。
- **协议兼容性**：除模版更新（`PUT /templates/{templateCode}`）为阿里云百炼扩展协议外，其余接口严格兼容 [E2B API Reference](https://docs.e2b.dev/api-reference)，响应结构与字段语义一致，可直接使用 E2B 官方 SDK（如 `e2b-python`）接入，详见 [API 总览与认证](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)。

## 关键参数

- **通用参数**：
  - `Authorization: Bearer <your-api-key>`：必填 Header，使用阿里云百炼控制台生成的 API Key。
  - `workspace_id` 与 `region`：用于拼装 Endpoint，当前仅支持 `cn-beijing`，格式为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox`。
- **实例创建（`POST /sandboxes`）**：
  - `templateID`（必填，string）：已构建完成（`status: "ready"`）的模版 ID。
  - `timeout`（可选，integer）：实例生命周期上限，单位秒，范围 `[300, 604800]`。
  - `allow_internet_access`（可选，boolean）：是否允许公网访问；也可通过 `network.allowPublicTraffic` 控制。
  - `lifecycle.on_timeout`（可选，string）：超时行为，取值 `"pause"`（暂停）或 `"terminate"`（释放）；若同时传 `maxRunningTimeout`（模版级），后者优先生效。
- **模版创建（`POST /v3/templates`）**：
  - `cpuCount` 与 `memoryMB`（必填，integer）：必须成对出现，且仅支持平台预设的规格组合（如 `1 CPU / 2048 MB`）。
  - `autoPauseTime` 与 `maxRunningTimeout`（可选，integer）：均单位秒，范围 `[300, 604800]`；`maxRunningTimeout` 优先级高于 `autoPauseTime`，未传时默认最大运行时间为 604800 秒。
  - `networkConfig.allowOut` / `denyOut`（可选）：出口白名单支持域名、IPv4/IPv6/CIDR；黑名单**仅支持 IPv4/IPv6/CIDR，不支持域名**（见 [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)）。

> **注意**：文档 3 与文档 4 中对 `lifecycle` 字段的描述存在不一致——文档 3 允许传入对象形式 `{"on_timeout": "pause", "auto_resume": true}`，而文档 4 的响应示例中字段名为 `onTimeout`（驼峰）且为字符串。实际请求应以文档 3 的 `on_timeout`（下划线）为准，响应解析需兼容 `onTimeout`（驼峰）字段名，二者为同一字段的请求/响应形态差异。

## 使用方式

1. **准备环境**：开通百炼服务，[创建 API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)，完成 SLR 授权（见 [快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md)），并获取 `workspace_id`。
2. **创建模版**：调用 `POST /v3/templates` 提交资源配置与环境定义，记录返回的 `templateID` 和 `buildID`。
3. **等待构建就绪**：轮询 `GET /templates/{templateID}/builds/{buildID}/status`，直至 `status` 变为 `"ready"`。
4. **创建实例**：调用 `POST /sandboxes`，传入 `templateID` 等参数，获取 `sandboxID`。
5. **连接与交互**：调用 `POST /sandboxes/{sandboxID}/connect` 获取 `domain` 与 `envdAccessToken`，用于后续数据面通信（如 exec、file upload/download）。
6. **生命周期管理**：根据需要调用 `/pause`、`/resume` 或 `/delete` 操作实例。

> **注意**：`/v2/sandboxes`（列举实例）与 `/v2/templates`（列举模版）为推荐分页接口，`limit` 最大值分别为 50 和 100；旧路由 `/sandboxes` 和 `/templates` 虽兼容，但功能受限，建议优先使用新版路径。

## 限制和注意事项

- **地域限制**：当前 Sandbox API 仅支持 `cn-beijing` 地域，Endpoint 中 `region` 固定为 `cn-beijing`。
- **资源规格约束**：`cpuCount` 与 `memoryMB` 必须匹配平台预设组合，单独修改任一参数将导致 400 错误；具体可用规格请参考控制台或平台文档。
- **模版删除保护**：调用 `DELETE /templates/{templateCode}` 时，若该模版关联任何 `running` 或 `paused` 实例，将返回 HTTP 409 错误，并在响应体中明确列出 `sandboxId` 和 `sandboxInstanceId`，必须先释放所有关联实例才能删除模版。
- **鉴权说明**：E2B SDK 中的 `X-API-Key` 或 `api_key` 参数仅用于满足协议格式，**阿里云百炼侧实际鉴权仅依赖 `Authorization: Bearer <your-api-key>` Header**；建议 SDK 中填写占位值（如 `e2b_${ALIYUN_UID}`），避免混淆。
- **错误处理**：常见错误码包括 400（参数错误）、401（API Key 无效）、404（资源不存在）、409（状态冲突，如模版有活跃实例或模版未就绪）、500（服务异常）。所有错误响应均为 JSON 格式，含 `code`、`message` 和 `requestID` 字段，便于排查。

## 来源文档

- [实例管理](../../raw/application-api-reference/sandbox-api/sandbox-api-instances.md)
- [API 总览与认证](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)
- [创建实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md)
- [获取实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-get.md)
- [列举实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-list.md)
- [连接实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-connect.md)
- [暂停实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-pause.md)
- [恢复实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-resume.md)
- [释放实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-delete.md)
- [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)
- [模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md)
- [获取模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-get.md)
- [列举模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-list.md)
- [更新模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-update.md)
- [获取构建状态](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-build-status.md)
- [删除模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-delete.md)


