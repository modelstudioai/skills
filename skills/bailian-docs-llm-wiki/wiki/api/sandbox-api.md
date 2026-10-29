# sandbox api

Sandbox API 是阿里云百炼提供的沙箱环境生命周期管理接口，兼容 E2B 协议，支持沙箱实例与模版的创建、查询、更新和释放。所有请求需通过阿里云百炼工作空间专属 Endpoint 发起，并使用 API Key 鉴权。管控面请求经百炼 AI 网关转发，数据面访问需通过连接后返回的 domain 与 token 完成。

## 支持的模型/功能

- **沙箱实例管理**：支持创建、列举、获取详情、连接、暂停、恢复和释放实例，覆盖完整生命周期操作。实例基于预构建的模版启动，支持自定义 CPU、内存、网络策略、环境变量与生命周期行为（如自动暂停/恢复）。
- **沙箱模版管理**：支持创建、列举、获取、更新和删除模版；模版可挂载文件（需先上传至 `source=sandbox_template`）、配置基础镜像（如 `code-interpreter-v1`、`browser`）、网络规则（白名单/黑名单）及运行时环境变量。每次更新触发新版本构建，需等待构建状态变为 `ready` 后方可创建实例。
- **文件上传能力**：提供表单上传与预签名地址上传两种方式，仅 `source=sandbox_template` 且 `status=available` 的文件可用于模版挂载。详细限制见 [文件上传](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)。
- **SDK 兼容性**：官方推荐使用 E2B SDK（如 Python SDK）接入，其方法名（如 `connect()`、`pause()`）与语义与本 API 严格对齐，详见 [实例管理与使用](../../raw/application-user-guide/agent-development/sandbox/sandbox-sdk.md)。

> **注意**：文档中提及的 `/sandboxes`（v1）与 `/v2/sandboxes` 列举接口均有效，但 `/v2/sandboxes` 为当前推荐路径；而模版创建接口 `/v3/templates` 为最新版本，旧版 `/templates` 虽兼容但不推荐用于新集成。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `Authorization` | Header | string | 是 | `Bearer <your-api-key>`，API Key 需在[百炼控制台](https://bailian.console.aliyun.com/?tab=model#/api-key)创建，详见 [认证](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md) |
| `workspace_id` | Endpoint | string | 是 | 工作空间 ID，位于控制台右上角下拉菜单，拼入 Base URL：<br>`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox` |
| `templateID` | 请求体（创建实例）/路径（模版操作） | string | 是 | 模版唯一标识，必须已构建完成（`buildStatus=ready`），否则创建实例返回 409 |
| `sandboxID` | 路径参数 | string | 是 | 实例唯一 ID，由创建接口返回，用于后续所有实例操作 |
| `originFileId` | `mntConfig` 数组元素 | string | 是（挂载文件时） | 文件 ID，须来自 `source=sandbox_template` 且 `status=available` 的上传响应，详见 [概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md) |
| `timeout` | 请求体（创建/连接/恢复） | integer | 否 | 实例或连接超时时间（秒），范围 `[300, 604800]`；`maxRunningTimeout` 优先生效于 `autoPauseTime` |

## 使用方式

1. **前置准备**  
   - 开通百炼服务，[创建 API Key](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)；  
   - 在百炼控制台完成 [SLR 授权](../../raw/application-user-guide/agent-development/sandbox/sandbox-start-using/sandbox-quick-start.md)；  
   - 获取 `workspace_id` 并确认地域为 `cn-beijing`。

2. **文件上传（如需挂载）**  
   ```bash
   curl -X POST "https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/files" \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -F "file=@./config.json" \
     -F "source=sandbox_template"
   ```
   轮询 `GET /api/v1/agentstudio/files/{file_id}` 直至 `status=available`。

3. **创建模版 → 查询构建状态 → 创建实例**  
   - 调用 `POST /v3/templates` 提交模版配置（含 `mntConfig` 引用已上传文件）；  
   - 轮询 `GET /templates/{templateID}/builds/{buildID}/status` 直至 `status=ready`；  
   - 调用 `POST /sandboxes` 创建实例，传入 `templateID` 及其他参数（如 `timeout`, `envVars`）。

4. **实例交互**  
   - 连接：`POST /sandboxes/{sandboxID}/connect` 获取 `domain` 和 `envdAccessToken`；  
   - 暂停/恢复：`POST /sandboxes/{sandboxID}/pause` 或 `/resume`；  
   - 释放：`DELETE /sandboxes/{sandboxID}`（不可逆）。

## 限制和注意事项

- **地域与 Endpoint**：当前仅支持 `cn-beijing` 地域，Endpoint 中 `region` 字段不可替换为其他值。
- **文件限制**：单文件 ≤ 50 MB，工作空间总容量 ≤ 100 GB，保存时效 30 天；支持 `.yaml`，不支持 `.csv`、`.yml`、`.sh`、`.whl`、`.tar.gz`、`.ts` 等扩展名（以接口实际校验为准）。
- **模版约束**：`cpuCount` 与 `memoryMB` 必须匹配平台预设规格组合（如 1 vCPU + 2048 MB），不可任意指定；`mntConfig.mountPath` 必须以 `/home/user/workspace/uploads/` 开头，否则挂载无效。
- **错误处理**：  
  - 409 错误常见于模版未就绪（创建实例时）或模版存在活跃实例（删除模版时）；  
  - 文件相关错误码详见 [错误码](../../raw/application-api-reference/sandbox-api/sandbox-api-errors.md)，如 `11900024`（文件非沙箱模版来源）、`11900014`（文件类型不被允许）；  
  - 兼容 E2B 协议的接口**不封装为阿里云百炼统一 `Result<T>` 结构**，错误响应格式贴近 E2B 原生定义。
- **鉴权特殊性**：E2B SDK 的 `api_key` 参数仅用于协议占位，**阿里云百炼侧实际鉴权仅依赖 HTTP Header 中的 `Authorization`**，`X-API-Key` 不生效。

## 来源文档

- [概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)
- [认证](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)
- [实例管理](../../raw/application-api-reference/sandbox-api/sandbox-api-instances.md)
- [错误码](../../raw/application-api-reference/sandbox-api/sandbox-api-errors.md)
- [创建实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md)
- [列举实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-list.md)
- [获取实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-get.md)
- [连接实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-connect.md)
- [暂停实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-pause.md)
- [恢复实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-resume.md)
- [释放实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-delete.md)
- [模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md)
- [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)
- [获取模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-get.md)
- [列举模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-list.md)
- [更新模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-update.md)
- [获取构建状态](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-build-status.md)
- [删除模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-delete.md)


