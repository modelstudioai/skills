# sandbox api

Sandbox API 是阿里云百炼提供的沙箱环境生命周期管理接口，兼容 E2B 协议，支持沙箱实例与模版的创建、查询、控制及文件挂载。所有请求需通过百炼 API Key 鉴权，并经由工作空间专属 Endpoint 发起。该 API 适用于需要动态执行代码、隔离运行环境或构建 Agent 工具链的开发者场景。

## 支持的模型/功能

Sandbox API 不直接提供大模型推理能力，而是为模型应用提供**可编程、可隔离的执行环境**。核心功能包括：

- **沙箱实例管理**：创建、列举、获取、连接、暂停、恢复与释放实例（见 [实例管理](raw/application-api-reference/sandbox-api/sandbox-api-instances.md)）；
- **沙箱模版管理**：定义并构建可复用的运行时环境（CPU / 内存规格、基础镜像、挂载文件、网络策略、环境变量等），支持版本化更新（见 [模版管理](raw/application-api-reference/sandbox-api/sandbox-api-templates.md)）；
- **文件上传与挂载**：通过 `source=sandbox_template` 上传文件，供模版构建或实例运行时挂载（见 [概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md) 中“文件上传”章节）；
- **E2B 协议兼容**：除模版更新（`PUT /templates/{templateCode}`）为百炼扩展外，其余接口（如 `/sandboxes`, `/sandboxes/{id}/connect`）在路径、方法、响应结构上贴近 [E2B 官方 API](https://docs.e2b.dev/api-reference)，便于迁移和 SDK 复用。

> **注意**：文档中多次提及 `POST /templates` 作为创建模版的兼容路由（如 [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)），但主推荐路径为 `POST /v3/templates`；实际调用应以 [概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md) 中“模版管理”表格为准，避免使用已标记为兼容的旧路径。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `Authorization: Bearer <API_KEY>` | Header | string | 是 | 百炼 API Key，非 E2B SDK 所需的 `X-API-Key`（见 [认证](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)） |
| `workspace_id` | Endpoint 路径 | string | 是 | 控制台右上角获取的工作空间 ID，用于拼装 Base URL |
| `templateID` | 请求体（创建实例） / 路径（获取模版） | string | 是（创建实例、获取模版等） | 模版唯一标识，来自 `POST /v3/templates` 响应；模版构建状态必须为 `ready` 才能创建实例 |
| `sandboxID` | 路径参数 | string | 是（除列举外） | 实例唯一 ID，来自 `POST /sandboxes` 响应 |
| `originFileId` | `mntConfig` 数组元素 | string | 是（若配置挂载） | 文件 ID，须通过 `source=sandbox_template` 上传且 `status=available`（见 [概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)） |
| `mountPath` | `mntConfig` 数组元素 | string | 是（若配置挂载） | 必须以 `/home/user/workspace/uploads/` 开头；否则挂载将无效 |
| `timeout` | 请求体（创建/连接/恢复实例） | integer | 否 | 实例生命周期或连接会话超时时间，单位秒，范围 `[300, 604800]` |

## 使用方式

1. **前置准备**  
   - 开通百炼服务，[创建 API Key](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)；  
   - 在百炼控制台完成 [SLR 授权](../../raw/application-user-guide/agent-development/sandbox/sandbox-start-using/sandbox-quick-start.md)；  
   - 获取 `workspace_id` 和地域（当前仅支持 `cn-beijing`），拼装 Base URL：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox`。

2. **构建模版（一次，可复用）**  
   - 上传所需文件（如 `config.json`, `requirements.txt`），指定 `source=sandbox_template`；  
   - 轮询文件 `status` 至 `available`；  
   - 调用 `POST /v3/templates` 提交模版，传入 `cpuCount`/`memoryMB`、`mntConfig` 等；  
   - 调用 `GET /templates/{templateID}/builds/{buildID}/status` 确认 `status=ready`。

3. **管理实例（按需）**  
   - 创建：`POST /sandboxes` + `templateID`；  
   - 连接：`POST /sandboxes/{sandboxID}/connect` 获取 `domain` 与 `envdAccessToken`，用于数据面通信；  
   - 控制：`POST /sandboxes/{sandboxID}/pause` / `resume` / `DELETE /sandboxes/{sandboxID}`；  
   - 查询：`GET /sandboxes/{sandboxID}` 或 `GET /v2/sandboxes`（支持过滤）。

4. **SDK 接入（可选）**  
   - 可直接使用 E2B 官方 SDK（如 `e2b` Python 包），但需将 `api_key` 设为占位符（如 `e2b_${ALIYUN_UID}`），实际鉴权依赖 HTTP Header 中的百炼 API Key（见 [概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)）。

## 限制和注意事项

- **地域限制**：当前仅支持 `cn-beijing` 地域，Endpoint 中 `region` 字段不可替换为其他值。
- **文件限制**：单文件 ≤ 50 MB，工作空间总容量 ≤ 100 GB，保存时效 30 天；仅 `.yaml` 明确支持，`.csv`/`.yml`/`.sh`/`.whl`/`.tar.gz`/`.ts` 等均不支持（见 [概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)）。
- **模版删除约束**：若模版关联任何 `running` 或 `paused` 实例，`DELETE /templates/{templateCode}` 将返回 409 错误，必须先释放所有实例（见 [删除模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-delete.md)）。
- **错误处理**：兼容 E2B 协议的接口不返回统一 `Result<T>` 结构，错误响应为直出 JSON（含 `code`/`message`），HTTP 状态码语义需结合 [错误码](../../raw/application-api-reference/sandbox-api/sandbox-api-errors.md) 文档理解。
- **网络配置差异**：`networkConfig.denyOut` 仅支持 IPv4/IPv6/CIDR，**不支持域名**（见 [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)），而 `allowOut` 支持域名，此限制易被忽略导致配置失效。

## 来源文档

- [概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)
- [认证](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)
- [错误码](../../raw/application-api-reference/sandbox-api/sandbox-api-errors.md)
- [实例管理](../../raw/application-api-reference/sandbox-api/sandbox-api-instances.md)
- [创建实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md)
- [连接实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-connect.md)
- [列举实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-list.md)
- [获取实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-get.md)
- [暂停实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-pause.md)
- [恢复实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-resume.md)
- [释放实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-delete.md)
- [模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md)
- [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)
- [列举模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-list.md)
- [更新模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-update.md)
- [获取模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-get.md)
- [获取构建状态](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-build-status.md)
- [删除模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-delete.md)


