# sandbox api

Sandbox API 是阿里云百炼提供的沙箱环境生命周期管理接口，兼容 E2B 协议，支持通过 REST API 或 E2B SDK 创建、管理沙箱实例与模版。它面向需要安全隔离执行环境的 AI 应用场景（如代码解释、浏览器自动化），提供资源规格控制、网络策略、文件挂载与生命周期管理能力。所有管控面请求均经百炼 AI 网关转发，并需使用阿里云百炼 API Key 鉴权。

## 支持的模型/功能

Sandbox API **不直接提供大模型推理服务**，而是提供可运行任意代码的沙箱环境。其核心能力围绕两类资源展开：

- **沙箱实例（Sandbox Instance）**：基于模版启动的临时计算环境，支持 `running`/`paused` 状态切换，具备 CPU、内存、磁盘、网络与超时控制。实例支持连接后自动恢复（`autoResume`）、公网访问开关（`allow_internet_access`）及细粒度网络规则（`network.allowOut`/`denyOut`）。详见 [创建实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md) 与 [获取实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-get.md)。
- **沙箱模版（Sandbox Template）**：定义沙箱基础镜像、资源配置、挂载文件、环境变量与网络策略的可复用模板。支持官方镜像（如 `code-interpreter-v1`、`browser`）和自定义镜像；文件挂载需先通过文件上传接口上传并指定 `source=sandbox_template`，且状态为 `available` 后方可写入 `mntConfig`。详见 [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md) 和 [更新模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-update.md)。

> **注意**：文档中多次提及 `fromImage` 可填写完整镜像地址（如 `fc-e2b-registry.cn-beijing.cr.aliyuncs.com/runtime/code-interpreter-v1`），但未明确列出所有可用官方镜像名称。实际使用时应以控制台或最新 [API 总览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md) 中的示例为准，避免硬编码不可靠的镜像路径。

## 关键参数

| 参数类别 | 参数名 | 类型 | 必填 | 说明 |
|----------|--------|------|------|------|
| **通用** | `Authorization: Bearer <api-key>` | Header | 是 | 使用阿里云百炼 API Key，非 E2B SDK 的 `X-API-Key`。详见 [认证](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)。 |
| **实例创建** | `templateID` | string | 是 | 已构建完成（`buildStatus=ready`）的模版 ID。模版未就绪时返回 409。 |
| | `timeout` | integer | 否 | 实例生命周期秒数，范围 `[300, 604800]`（5 分钟至 7 天）。到期行为由 `lifecycle.on_timeout` 控制。 |
| | `lifecycle.on_timeout` | string | 否 | 到期动作，`pause`（暂停）或 `terminate`（释放）；若未指定，默认为 `terminate`。 |
| | `mntConfig` | array<object> | 否 | 挂载配置，`originFileId` 必须为 `source=sandbox_template` 且 `status=available` 的文件 ID；`mountPath` 必须以 `/home/user/workspace/uploads/` 开头。 |
| **模版创建/更新** | `cpuCount` / `memoryMB` | integer | 是（创建时）<br/>否（更新时，但需同时传） | 必须匹配平台预设规格组合（如 `1CPU+2048MB`），不支持任意值。 |
| | `maxRunningTimeout` | integer | 否 | 模版级最大运行时间（秒），优先级高于实例级 `timeout`；两者均未传时默认 604800 秒。 |

## 使用方式

1. **前置准备**  
   - 开通百炼服务，[创建 API Key](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)；  
   - 在百炼控制台完成 **SLR 服务授权**（首次使用必需）；  
   - 获取工作空间 ID（控制台右上角）与地域（当前仅支持 `cn-beijing`）；  
   - 构建 Endpoint：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox`。

2. **文件上传（如需挂载）**  
   - 调用 `POST /api/v1/agentstudio/files`，`form-data` 中指定 `source=sandbox_template`；  
   - 轮询 `GET /api/v1/agentstudio/files/{file_id}`，待 `status=available` 后，将 `id` 用于 `mntConfig.originFileId`。

3. **模版生命周期**  
   - `POST /v3/templates` 创建模版 → 获取 `templateID` 与 `buildID`；  
   - `GET /templates/{templateID}/builds/{buildID}/status` 轮询构建状态，直至 `status=ready`；  
   - `POST /sandboxes` 基于该模版创建实例。

4. **实例生命周期**  
   - 创建后，用 `GET /sandboxes/{sandboxID}` 获取连接信息；  
   - `POST /sandboxes/{sandboxID}/connect` 获取实时 token（支持动态 `timeout`）；  
   - `POST /sandboxes/{sandboxID}/pause` 与 `POST /sandboxes/{sandboxID}/resume` 控制状态；  
   - `DELETE /sandboxes/{sandboxID}` 彻底释放资源。

## 限制和注意事项

- **地域限制**：当前 Sandbox API 仅支持 `cn-beijing` 地域，Endpoint 中 `region` 固定为此值。
- **文件限制**：单文件 ≤ 50 MB，工作空间总容量 ≤ 100 GB，文件保存时效为 30 天；扩展名校验严格，`.csv`、`.yml`、`.sh`、`.whl`、`.tar.gz`、`.ts` 等均不支持（见 [文件上传](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)）。
- **模版删除约束**：删除模版前必须确保无 `running` 或 `paused` 状态的关联实例，否则返回 409 错误（见 [删除模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-delete.md)）。
- **鉴权差异**：E2B SDK 的 `api_key` 参数仅用于满足协议格式，**阿里云百炼侧业务鉴权完全依赖 HTTP Header 中的 `Authorization: Bearer <your-api-key>`**。推荐 SDK 中 `api_key` 填写 `e2b_${ALIYUN_UID}` 以作标识。
- **错误处理**：HTTP 状态码语义遵循标准（如 401=Key 无效，409=状态冲突），错误响应体结构贴近 E2B 原生格式，但百炼特有错误码（如 `11900008` 文件超限）需查 [错误码](../../raw/application-api-reference/sandbox-api/sandbox-api-errors.md) 文档。

## 来源文档

- [认证](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)
- [概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)
- [错误码](../../raw/application-api-reference/sandbox-api/sandbox-api-errors.md)
- [实例管理](../../raw/application-api-reference/sandbox-api/sandbox-api-instances.md)
- [列举实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-list.md)
- [创建实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md)
- [获取实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-get.md)
- [连接实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-connect.md)
- [恢复实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-resume.md)
- [暂停实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-pause.md)
- [模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md)
- [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)
- [列举模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-list.md)
- [获取模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-get.md)
- [更新模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-update.md)
- [获取构建状态](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-build-status.md)
- [删除模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-delete.md)
- [释放实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-delete.md)


