# sandbox api

Sandbox API 是阿里云百炼提供的沙箱环境生命周期管理接口，兼容 E2B 协议，支持沙箱实例与模版的创建、查询、启停、释放及构建管理。所有请求需通过阿里云百炼 AI 网关转发，并使用百炼 API Key 鉴权。开发者可直接调用 REST 接口，或通过 E2B 官方 SDK（需适配鉴权方式）接入。

## 支持的模型/功能

- **实例管理**：支持创建（`POST /sandboxes`）、列举（`GET /v2/sandboxes`）、获取详情（`GET /sandboxes/{sandboxID}`）、连接（`POST /sandboxes/{sandboxID}/connect`）、暂停（`POST /sandboxes/{sandboxID}/pause`）、恢复（`POST /sandboxes/{sandboxID}/resume`）和释放（`DELETE /sandboxes/{sandboxID}`）沙箱实例。  
- **模版管理**：支持创建（`POST /v3/templates`）、列举（`GET /v2/templates`）、获取（`GET /templates/{templateCode}`）、更新（`PUT /templates/{templateCode}`）、查询构建状态（`GET /templates/{templateCode}/builds/{buildID}/status`）和删除（`DELETE /templates/{templateCode}`）模版。  
- **文件上传**：仅支持 `source=sandbox_template` 的文件上传，用于模版挂载；上传后需轮询至 `status=available` 才可在 `mntConfig` 中引用。详细限制见 [Sandbox API 错误码](../../raw/application-api-reference/sandbox-api/sandbox-api-errors.md)。  
- **网络与生命周期配置**：支持在创建/更新模版或实例时指定 `networkConfig`（出口白/黑名单）和 `lifecycle`（如 `on_timeout: "pause"`），详见 [创建实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md) 和 [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)。

> **注意**：文档中 `/v2/sandboxes` 与 `/sandboxes` 均为列举实例的有效路径，但 `/v2/sandboxes` 是当前推荐路由；而 `/sandboxes` 为兼容旧版 E2B 协议的别名，未来可能逐步收敛。同理，模版创建接口 `/v3/templates` 是主路径，`/templates` 为兼容路由，详见 [概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)。

## 关键参数

- **认证**：必须在 `Authorization` Header 中携带百炼 API Key：`Bearer <your-api-key>`；E2B SDK 中的 `api_key` 字段仅作协议占位，不参与业务鉴权，建议填 `e2b_${ALIYUN_UID}`。  
- **Endpoint**：按工作空间与地域拼装，固定为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox`（当前仅支持 `cn-beijing`）。  
- **模版与实例标识**：`templateID`（模版唯一 code）和 `sandboxID`（实例唯一 ID）均为必填路径参数，不可省略。  
- **资源规格**：创建模版或实例时，`cpuCount` 与 `memoryMB` 必须同时提供，且必须匹配平台预设的规格组合（如 `1 vCPU + 2048 MB`）；单独传任一字段将导致 400 错误。  
- **文件挂载**：`mntConfig` 中的 `originFileId` 必须指向已上传且 `status=available` 的文件（`source=sandbox_template`），`mountPath` 必须以 `/home/user/workspace/uploads/` 开头，否则文件不会出现在实例中。

## 使用方式

1. **前置准备**：开通百炼服务，[创建 API Key](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)，完成 SLR 授权，并获取工作空间 ID。  
2. **上传模版依赖文件**（如 `config.json`）：  
   ```bash
   curl -X POST "$BASE_URL/api/v1/agentstudio/files" \
     -H "Authorization: Bearer $BAILIAN_API_KEY" \
     -F "file=@./config.json" \
     -F "source=sandbox_template"
   ```  
   轮询 `GET /api/v1/agentstudio/files/{file_id}` 直至 `status=available`。  
3. **创建模版**：调用 `POST /v3/templates`，在 `mntConfig` 中引用上一步的 `originFileId`；等待 `GET /templates/{templateID}/builds/{buildID}/status` 返回 `status=ready`。  
4. **创建实例**：调用 `POST /sandboxes`，传入 `templateID` 及可选 `timeout`、`allow_internet_access`、`lifecycle` 等参数。  
5. **连接与操作**：调用 `POST /sandboxes/{sandboxID}/connect` 获取 `domain` 与 `envdAccessToken`，再通过 E2B 数据面协议执行命令；或调用 `/pause`/`/resume` 控制状态。  

## 限制和注意事项

- **地域限制**：当前仅支持 `cn-beijing` 地域，Endpoint 中 `region` 不可替换为其他值。  
- **文件限制**：单文件 ≤ 50 MB，工作空间总容量 ≤ 100 GB，保存时效 30 天；仅 `.yaml` 等明确支持的扩展名可上传，`.csv`、`.sh`、`.ts` 等被拒绝（错误码 `11900014`/`11900019`），详见 [概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)。  
- **模版删除约束**：若模版关联任何运行中或暂停中的实例，`DELETE /templates/{templateCode}` 将返回 409 错误，必须先释放所有实例。  
- **错误处理**：兼容 E2B 协议的接口不封装为百炼统一 `Result<T>` 结构，错误响应体为原生 JSON（含 `code`、`message`），HTTP 状态码语义与标准一致（如 401 表示 API Key 无效，409 表示状态冲突）。完整错误码列表见 [Sandbox API 错误码](../../raw/application-api-reference/sandbox-api/sandbox-api-errors.md)。  
- **SDK 兼容性**：E2B 官方 SDK 可用于实例管理，但需注意其 `api_key` 参数不参与百炼鉴权，实际鉴权仍依赖 HTTP Header 中的 `Authorization`；模版管理等百炼扩展能力需直接调用 REST 接口。

## 来源文档

- [概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)
- [认证](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)
- [Sandbox API 错误码](../../raw/application-api-reference/sandbox-api/sandbox-api-errors.md)
- [实例管理](../../raw/application-api-reference/sandbox-api/sandbox-api-instances.md)
- [列举实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-list.md)
- [获取实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-get.md)
- [连接实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-connect.md)
- [创建实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md)
- [恢复实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-resume.md)
- [释放实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-delete.md)
- [模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md)
- [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)
- [暂停实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-pause.md)
- [获取模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-get.md)
- [更新模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-update.md)
- [获取构建状态](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-build-status.md)
- [删除模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-delete.md)
- [列举模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-list.md)


