# sandbox api

Sandbox API 是阿里云百炼提供的沙箱环境生命周期管理接口，兼容 E2B 协议，支持沙箱实例与模版的创建、查询、暂停/恢复、释放等操作，并提供文件挂载与网络策略配置能力。所有请求需通过阿里云百炼 API Key 鉴权，并按工作空间与地域拼装 Endpoint。该 API 由百炼 AI 网关统一转发，管控面与数据面分离。

## 支持的模型/功能

- **沙箱实例管理**：支持创建、列举、获取、连接、暂停、恢复和释放实例，全部兼容 E2B 协议语义（如 `pause()`、`resume()`、`connect()`），响应结构贴近 [E2B 官方 API Reference](https://docs.e2b.dev/api-reference)；但鉴权、Endpoint 和扩展字段（如 `bailianSandboxId`、`trafficAccessToken`）以百炼文档为准 [概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)。
- **沙箱模版管理**：支持创建、列举、获取、更新、删除模版及查询构建状态。模版构建成功（`status=ready`）后方可用于创建实例；更新模版会触发新版本构建并递增 `version` 字段，该行为为阿里云百炼自定义协议，不完全兼容 E2B Update Template v2 [更新模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-update.md)。
- **文件挂载**：仅支持通过 `/api/v1/agentstudio/files` 接口上传 `source=sandbox_template` 且状态为 `available` 的文件，挂载路径必须以 `/home/user/workspace/uploads/` 开头；`.csv`、`.yml`、`.sh`、`.whl`、`.tar.gz`、`.ts` 等格式明确不支持 [概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)。
- **网络与生命周期控制**：支持实例级 `allow_internet_access`、出口白/黑名单（`allowOut`/`denyOut`）、超时自动暂停（`autoPause`）或自动释放（`maxRunningTimeout`）等配置。

> **注意**：文档中关于模版创建路径存在不一致——[概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md) 表格列出创建模版路径为 `/v3/templates`，而其正文中又注明“兼容路由 `POST /templates`”；实际应以 `/v3/templates` 为准（见 [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)），`/templates` 为历史兼容路径，新集成建议使用 `/v3/templates`。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `Authorization` | Header | string | 是 | `Bearer <your-api-key>`，API Key 从百炼控制台获取 [认证](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md) |
| `workspace_id` | Endpoint | string | 是 | 工作空间 ID，控制台右上角下拉菜单查看 |
| `region` | Endpoint | string | 是 | 当前仅支持 `cn-beijing` |
| `templateID` | Body/Path | string | 是（创建/操作实例时） | 模版唯一 ID，需已构建完成（`status=ready`） |
| `sandboxID` | Path | string | 是（实例操作时） | 实例唯一 ID，由创建接口返回 |
| `originFileId` | `mntConfig` 元素 | string | 是（挂载文件时） | 文件上传后返回的 `id`，且 `source=sandbox_template`、`status=available` |
| `mountPath` | `mntConfig` 元素 | string | 是（挂载文件时） | 必须以 `/home/user/workspace/uploads/` 开头，否则文件不会出现在实例中 |

## 使用方式

1. **前置准备**：
   - 开通百炼服务，[创建 API Key](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)；
   - 在百炼控制台完成 SLR 服务授权（首次使用必需）；
   - 确认工作空间 ID 与地域（仅 `cn-beijing`）。

2. **文件上传（如需挂载）**：
   ```bash
   curl -X POST "https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/files" \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -F "file=@./config.json" \
     -F "source=sandbox_template"
   ```
   轮询 `/api/v1/agentstudio/files/{file_id}` 直至 `status=available`。

3. **创建模版**：
   ```bash
   curl -X POST "$BASE_URL/v3/templates" \
     -H "Authorization: Bearer $BAILIAN_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "my-template",
       "cpuCount": 1,
       "memoryMB": 2048,
       "mntConfig": [{"originFileId": "file_xxx", "mountPath": "/home/user/workspace/uploads/config.json"}]
     }'
   ```
   获取 `buildID` 后调用 `/templates/{templateID}/builds/{buildID}/status` 等待 `status=ready`。

4. **创建并操作实例**：
   - 创建：`POST /sandboxes`，传入 `templateID`；
   - 连接：`POST /sandboxes/{sandboxID}/connect`，获取 `domain` 与 `envdAccessToken` 用于数据面访问；
   - 暂停/恢复：`POST /sandboxes/{sandboxID}/pause` 或 `/resume`；
   - 释放：`DELETE /sandboxes/{sandboxID}`。

5. **SDK 集成**：可直接使用 E2B 官方 SDK（如 Python `e2b` 包），但需将 `api_key` 设为 `e2b_${ALIYUN_UID}` 占位符，真实鉴权仍依赖 HTTP Header 中的百炼 API Key [概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)。

## 限制和注意事项

- **地域限制**：当前仅支持 `cn-beijing` 地域，Endpoint 中 `region` 固定为此值。
- **文件限制**：单文件 ≤ 50 MB，工作空间总容量 ≤ 100 GB，保存时效 30 天；不支持 `.csv`、`.yml`、`.sh`、`.whl`、`.tar.gz`、`.ts` 等扩展名 [概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)。
- **模版构建依赖**：创建实例前，模版 `buildStatus` 必须为 `ready`；若为 `building` 或 `error`，接口返回 409 [创建实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md)。
- **模版删除约束**：删除模版前，必须确保无运行中或暂停中的实例，否则返回 409 并附带关联 `sandboxID` [删除模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-delete.md)。
- **错误处理**：兼容 E2B 协议的接口不封装为百炼标准 `Result<T>` 结构，错误响应为直出 JSON（含 `code`、`message`、`requestID`），HTTP 状态码含义详见 [错误码](../../raw/application-api-reference/sandbox-api/sandbox-api-errors.md)。
- **资源规格匹配**：`cpuCount` 与 `memoryMB` 必须同时指定，且需匹配平台预设的规格组合（如 1 vCPU + 2048 MB），单独传入任一字段将导致 400 错误。

## 来源文档

- [概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)
- [实例管理](../../raw/application-api-reference/sandbox-api/sandbox-api-instances.md)
- [认证](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)
- [错误码](../../raw/application-api-reference/sandbox-api/sandbox-api-errors.md)
- [列举实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-list.md)
- [创建实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md)
- [获取实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-get.md)
- [暂停实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-pause.md)
- [连接实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-connect.md)
- [恢复实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-resume.md)
- [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)
- [释放实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-delete.md)
- [模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md)
- [列举模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-list.md)
- [更新模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-update.md)
- [删除模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-delete.md)
- [获取构建状态](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-build-status.md)
- [获取模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-get.md)


