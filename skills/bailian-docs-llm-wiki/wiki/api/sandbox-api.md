# sandbox api

Sandbox API 是阿里云百炼提供的沙箱环境生命周期管理服务，兼容 E2B 协议，支持通过 REST 接口或 E2B SDK 创建、管理沙箱实例与模版。其核心能力包括实例的启停、连接、释放，模版的构建与配置，以及文件挂载等。所有请求均需通过阿里云百炼 API Key 鉴权，并经由工作空间专属 Endpoint 转发。

## 支持的模型/功能

- **实例管理**：支持创建（`POST /sandboxes`）、列举（`GET /v2/sandboxes`）、获取详情（`GET /sandboxes/{sandboxID}`）、连接（`POST /sandboxes/{sandboxID}/connect`）、暂停（`POST /sandboxes/{sandboxID}/pause`）、恢复（`POST /sandboxes/{sandboxID}/resume`）和释放（`DELETE /sandboxes/{sandboxID}`）沙箱实例。详见 [实例管理](raw/application-api-reference/sandbox-api/sandbox-api-instances.md)。
- **模版管理**：支持创建（`POST /v3/templates`）、列举（`GET /v2/templates`）、获取（`GET /templates/{templateCode}`）、更新（`PUT /templates/{templateCode}`）、查询构建状态（`GET /templates/{templateCode}/builds/{buildID}/status`）和删除（`DELETE /templates/{templateCode}`）模版。模版构建完成后方可用于创建实例，具体流程见 [创建模版](raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)。
- **文件挂载**：支持将上传至 `source=sandbox_template` 的文件挂载到实例中，挂载路径必须以 `/home/user/workspace/uploads/` 开头；文件需处于 `available` 状态才可使用。文件上传方式详见 [概览](raw/application-api-reference/sandbox-api/sandbox-api-overview.md) 中的“文件上传”章节。

## 关键参数

- **通用参数**：
  - `workspace_id`：工作空间 ID，从百炼控制台右上角获取；
  - `region`：当前仅支持 `cn-beijing`；
  - `Authorization: Bearer <API_KEY>`：必填请求头，API Key 在 [百炼控制台 API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key) 创建。
- **实例创建参数**（`POST /sandboxes`）：
  - `templateID`（必填）：已构建完成（`status=ready`）的模版 ID；
  - `timeout`（可选）：实例生命周期秒数，范围 `[300, 604800]`；
  - `allow_internet_access`（可选）：是否允许公网访问；
  - `lifecycle.on_timeout`（可选）：到期行为，支持 `"pause"` 或 `"kill"`；
  - `autoResume` / `lifecycle.auto_resume`（可选）：连接时是否自动恢复暂停实例。
- **模版创建/更新参数**（`POST /v3/templates` / `PUT /templates/{templateCode}`）：
  - `cpuCount` 与 `memoryMB`（必填且需同时指定）：必须匹配平台预设规格组合；
  - `mntConfig`（可选）：挂载配置数组，每个元素含 `originFileId`（来自 `source=sandbox_template` 的可用文件 ID）和 `mountPath`（路径须以 `/home/user/workspace/uploads/` 开头）；
  - `networkConfig.allowOut` / `denyOut`（可选）：支持域名、IPv4/IPv6、CIDR 格式白/黑名单；
  - `maxRunningTimeout`（可选）：优先级高于 `autoPauseTime`，到期强制释放实例。

> **注意**：文档 13 与文档 16 均指出 `mntConfig.mountPath` 必须以 `/home/user/workspace/uploads/` 开头，但文档 13 补充说明“路径不在该目录下时接口接受配置但实例中不会出现文件”，而文档 16 未强调此限制。实际使用中应严格遵守路径前缀要求，否则挂载失败且无明确报错。

## 使用方式

1. **前置准备**：
   - 完成 [服务授权（SLR）](raw/application-user-guide/agent-development/sandbox/sandbox-start-using/sandbox-quick-start.md)；
   - 获取 `workspace_id` 和 `DASHSCOPE_API_KEY`；
   - 拼装 Base URL：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox`。

2. **文件上传（如需挂载）**：
   ```bash
   curl -X POST "$BASE_URL/api/v1/agentstudio/files" \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -F "file=@./config.json" \
     -F "source=sandbox_template"
   ```
   轮询 `GET /api/v1/agentstudio/files/{file_id}` 直至 `status="available"`。

3. **创建模版**：
   ```bash
   curl -X POST "$BASE_URL/v3/templates" \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"name":"my-tpl","cpuCount":1,"memoryMB":2048}'
   ```
   调用 `GET /templates/{templateID}/builds/{buildID}/status` 等待 `status="ready"`。

4. **创建并操作实例**：
   ```bash
   # 创建
   curl -X POST "$BASE_URL/sandboxes" \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"templateID":"tpl-xxx"}'
   # 连接（获取数据面 token）
   curl -X POST "$BASE_URL/sandboxes/sbx-xxx/connect" \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY"
   ```

## 限制和注意事项

- **地域限制**：当前仅支持 `cn-beijing` 地域，Endpoint 中 `region` 字段不可更改。
- **文件限制**：
  - 单文件 ≤ 50 MB；
  - 工作空间总容量 ≤ 100 GB；
  - 文件保存时效为 30 天；
  - 仅 `.yaml` 扩展名明确支持；`.csv`、`.yml`、`.sh`、`.whl`、`.tar.gz`、`.ts` 等不支持（见 [概览](raw/application-api-reference/sandbox-api/sandbox-api-overview.md)）。
- **模版与实例约束**：
  - 创建实例时，对应模版的构建状态必须为 `ready`，否则返回 `409`；
  - 删除模版前，必须确保无运行中或暂停中的实例，否则返回 `409`（见 [删除模版](raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-delete.md)）；
  - `cpuCount` 与 `memoryMB` 必须成对设置且符合平台规格组合，否则创建/更新模版失败。
- **错误处理**：
  - 兼容 E2B 错误结构，但 HTTP 状态码与错误码以阿里云百炼定义为准（如 `11900008` 表示文件超限，对应 `413`）；
  - 文件类错误（如 `11900023`）常因文件未就绪（`status != available`）导致，需轮询确认状态。

## 来源文档

- [概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)
- [错误码](../../raw/application-api-reference/sandbox-api/sandbox-api-errors.md)
- [认证](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)
- [实例管理](../../raw/application-api-reference/sandbox-api/sandbox-api-instances.md)
- [列举实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-list.md)
- [创建实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md)
- [获取实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-get.md)
- [连接实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-connect.md)
- [暂停实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-pause.md)
- [恢复实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-resume.md)
- [模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md)
- [释放实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-delete.md)
- [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)
- [获取模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-get.md)
- [列举模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-list.md)
- [更新模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-update.md)
- [获取构建状态](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-build-status.md)
- [删除模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-delete.md)


