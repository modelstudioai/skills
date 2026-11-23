# sandbox api

Sandbox API 是阿里云百炼提供的沙箱环境生命周期管理接口，兼容 E2B 协议，支持模版构建、实例创建与管控、文件挂载及网络策略配置。所有请求需通过阿里云百炼 AI 网关转发，鉴权依赖 API Key，Endpoint 按工作空间与地域动态拼装。该 API 面向需要隔离执行环境的 Agent 开发者，适用于代码解释、浏览器自动化等场景。

## 支持的模型/功能

- **模版管理**：支持创建、列举、获取、更新和删除沙箱模版（`/v3/templates`, `/v2/templates`, `/templates/{templateCode}` 等），模版基于 `fromImage`（如 `code-interpreter-v1`、`browser`）构建，可挂载预上传文件、配置环境变量与网络规则。
- **实例管理**：支持全生命周期操作，包括创建（`POST /sandboxes`）、列举（`GET /v2/sandboxes`）、获取详情（`GET /sandboxes/{sandboxID}`）、连接（`POST /sandboxes/{sandboxID}/connect`）、暂停（`POST /sandboxes/{sandboxID}/pause`）、恢复（`POST /sandboxes/{sandboxID}/resume`）和释放（`DELETE /sandboxes/{sandboxID}`）。
- **文件系统集成**：通过独立的文件上传接口（`POST /api/v1/agentstudio/files`）上传资源，仅当 `source=sandbox_template` 且 `status=available` 的文件才可用于模版 `mntConfig` 挂载 [文件上传](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)。
- **E2B 兼容性**：除模版更新（`PUT /templates/{templateCode}`）为阿里云百炼自定义协议外，其余接口方法、路径与响应结构均贴近 [E2B 官方 API Reference](https://docs.e2b.dev/api-reference)，开发者可直接复用 E2B SDK [实例管理与使用](../../raw/application-user-guide/agent-development/sandbox/sandbox-sdk.md)。

> **注意**：文档中多次出现 `POST /templates` 与 `POST /v3/templates` 并存，但根据 [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md) 明确说明“兼容路由 `POST /templates`”，而主推路径为 `/v3/templates`；实际调用应优先使用 `/v3/templates`，避免因路由兼容性导致行为不一致。

## 关键参数

- **通用路径参数**：`{sandboxID}`（实例 ID，格式如 `sbx-xxx`）、`{templateCode}`（模版 ID，即 `templateID`）。
- **创建实例（`POST /sandboxes`）**：
  - `templateID`（必填，string）：已构建完成（`buildStatus=ready`）的模版 ID；
  - `timeout`（可选，integer）：实例生命周期，300–604800 秒；
  - `allow_internet_access`（可选，boolean）：控制公网访问；
  - `lifecycle.on_timeout`（可选，string）：到期行为，支持 `pause`；`auto_resume` 控制连接时是否自动恢复。
- **创建/更新模版**：
  - `cpuCount` 与 `memoryMB`（必填且必须同时传）：须匹配平台预设规格组合；
  - `mntConfig`（可选，array）：每个项含 `originFileId`（来自 `source=sandbox_template` 的可用文件 ID）、`mountPath`（必须以 `/home/user/workspace/uploads/` 开头）；
  - `networkConfig.allowOut`/`denyOut`（可选）：支持域名、CIDR、IP；但 `denyOut` 不支持域名（见 [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)）。
- **文件上传**：`source` 必须为 `sandbox_template`，否则返回错误码 `100005`；上传后需轮询至 `status=available` 才可挂载。

## 使用方式

1. **前置准备**：
   - 开通百炼服务，[创建 API Key](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)；
   - 在百炼控制台完成 SLR 授权（首次使用必需）；
   - 获取工作空间 ID（`workspace_id`）与地域（当前仅 `cn-beijing`）。

2. **Endpoint 构造**：
   ```
   https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox
   ```

3. **典型流程**：
   - 上传文件 → 调用 `POST /api/v1/agentstudio/files` 并设置 `source=sandbox_template`，轮询至 `status=available`；
   - 创建模版 → `POST /v3/templates`，传入 `mntConfig` 引用上述文件 ID，记录返回的 `templateID` 和 `buildID`；
   - 等待构建就绪 → `GET /templates/{templateID}/builds/{buildID}/status`，直到 `status=ready`；
   - 创建实例 → `POST /sandboxes`，指定 `templateID`；
   - 连接实例 → `POST /sandboxes/{sandboxID}/connect`，获取 `domain` 与 `envdAccessToken` 用于数据面交互。

4. **SDK 接入**：推荐使用 E2B 官方 SDK（如 Python `e2b` 包），只需将 `api_key` 设为占位符（如 `e2b_${ALIYUN_UID}`），并配置自定义 `base_url` 指向百炼 Endpoint。

## 限制和注意事项

- **地域限制**：当前仅支持 `cn-beijing` 地域，Endpoint 中 region 固定为 `cn-beijing`。
- **文件限制**：
  - 单文件 ≤ 50 MB，工作空间总容量 ≤ 100 GB，保存时效 30 天；
  - 仅 `.yaml` 明确支持；`.csv`、`.yml`、`.sh`、`.whl`、`.tar.gz`、`.ts` 等被明确拒绝（见 [文件上传](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)）。
- **模版与实例约束**：
  - 创建实例前，模版 `buildStatus` 必须为 `ready`，否则返回 409；
  - 删除模版前，必须确保无运行中或暂停中的实例，否则返回 409（见 [删除模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-delete.md)）。
- **鉴权特殊性**：E2B SDK 的 `api_key` 参数仅用于协议占位，**不参与百炼业务鉴权**；真实鉴权依赖 HTTP Header `Authorization: Bearer <your-api-key>` [认证](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)。
- **错误处理**：兼容 E2B 协议的接口不封装为百炼统一 `Result<T>` 结构，错误响应直接返回 `{code, message, requestID}` 格式，HTTP 状态码语义需对照 [Sandbox API 错误码](../../raw/application-api-reference/sandbox-api/sandbox-api-errors.md) 解析。

## 来源文档

- [概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)
- [认证](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)
- [Sandbox API 错误码](../../raw/application-api-reference/sandbox-api/sandbox-api-errors.md)
- [创建实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md)
- [实例管理](../../raw/application-api-reference/sandbox-api/sandbox-api-instances.md)
- [列举实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-list.md)
- [获取实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-get.md)
- [暂停实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-pause.md)
- [连接实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-connect.md)
- [恢复实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-resume.md)
- [释放实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-delete.md)
- [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)
- [模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md)
- [列举模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-list.md)
- [获取模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-get.md)
- [更新模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-update.md)
- [获取构建状态](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-build-status.md)
- [删除模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-delete.md)


