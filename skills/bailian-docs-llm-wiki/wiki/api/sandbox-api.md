# sandbox api

Sandbox API 是阿里云百炼提供的沙箱环境生命周期管理接口，兼容 E2B 协议，支持沙箱实例与模版的创建、查询、暂停/恢复、释放等操作。所有请求需通过阿里云百炼 API Key 鉴权，并经由工作空间专属 Endpoint 转发。该 API 适用于需要隔离执行环境的代码解释、浏览器自动化、数据处理等场景。

## 支持的模型/功能

Sandbox API 不直接提供大模型推理能力，而是为 Agent 或应用提供**可编程的、隔离的运行时环境**（即“沙箱”），其核心能力包括：

- **实例管理**：基于模版快速创建、列举、获取、连接、暂停、恢复和释放沙箱实例；实例状态包含 `running`、`paused`，支持自动暂停与超时恢复；
- **模版管理**：定义沙箱基础镜像（如 `code-interpreter-v1`、`browser`、`all-in-one`）、CPU/内存规格、挂载文件、网络规则、环境变量及生命周期策略；
- **文件挂载**：支持将上传至百炼文件服务的配置或代码文件（`source=sandbox_template`）挂载到 `/home/user/workspace/uploads/` 下指定路径；
- **E2B 兼容性**：除模版更新（`PUT /templates/{templateCode}`）为阿里云百炼扩展协议外，其余接口（如 `/sandboxes`、`/sandboxes/{id}/connect`）严格遵循 [E2B 官方 API](https://docs.e2b.dev/api-reference) 的方法、路径与响应结构，可直接使用 E2B SDK 接入 —— 详见 [实例管理与使用](raw/application-user-guide/agent-development/sandbox/sandbox-sdk.md)。

> **注意**：文档中多次提及 `fromImage` 可填写完整镜像地址（如 `fc-e2b-registry.cn-beijing.cr.aliyuncs.com/runtime/code-interpreter-v1`），但 [创建模版](raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md) 明确说明“缺省时使用平台默认镜像（代码解释器镜像）”，且未列出其他可用镜像名称。实际可用镜像列表应以控制台或最新 API 响应为准，避免硬编码非官方维护的镜像地址。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `Authorization` | Header | string | 是 | `Bearer <your-api-key>`，使用阿里云百炼 API Key，**非 E2B SDK 所需的 `X-API-Key`** —— 详见 [认证](raw/application-api-reference/sandbox-api/sandbox-api-authentication.md) |
| `workspace_id` | Endpoint | string | 是 | 工作空间 ID，位于控制台右上角下拉菜单中，用于拼装 Base URL：<br>`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox` |
| `templateID` | Body (创建实例) / Path (获取/更新模版) | string | 是 | 模版唯一标识，必须为已构建完成（`status=ready`）的模版，否则创建实例返回 `409` —— 参考 [创建实例](raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md) |
| `originFileId` | `mntConfig[].originFileId` | string | 是（若挂载文件） | 文件 ID，须通过 `source=sandbox_template` 上传且 `status=available`，否则模版创建/更新失败 —— 见 [文件上传](raw/application-api-reference/sandbox-api/sandbox-api-overview.md) |
| `timeout` | Body (创建/连接/恢复实例) | integer | 否 | 实例生命周期或连接会话超时时间（秒），范围 `[300, 604800]`（5 分钟至 7 天） |

## 使用方式

1. **前置准备**  
   - 开通百炼服务，[创建 API Key](raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)；  
   - 在百炼控制台完成 **SLR 服务授权**（首次使用必需），并获取 `workspace_id`；  
   - 如需挂载文件，先调用文件上传接口（`POST /api/v1/agentstudio/files`）并指定 `source=sandbox_template`，轮询至 `status=available`。

2. **模版工作流**  
   - `POST /v3/templates` 创建模版 → 获取 `templateID` 和 `buildID`；  
   - `GET /templates/{templateID}/builds/{buildID}/status` 轮询构建状态，待 `status=ready`；  
   - `POST /sandboxes` 基于该模版创建实例。

3. **实例工作流**  
   - 创建后，用 `GET /sandboxes/{sandboxID}` 获取详情，或 `POST /sandboxes/{sandboxID}/connect` 获取数据面访问凭证（`domain` + `envdAccessToken`）；  
   - 实例可 `POST /sandboxes/{sandboxID}/pause` 暂停（保留状态），再 `POST /sandboxes/{sandboxID}/resume` 恢复；  
   - 不再需要时，`DELETE /sandboxes/{sandboxID}` 释放资源。

4. **SDK 接入**  
   推荐使用 E2B 官方 SDK（如 Python `e2b` 包），只需将 `api_key` 设为占位符（如 `e2b_${ALIYUN_UID}`），Endpoint 替换为百炼 Base URL 即可 —— 具体配置见 [实例管理与使用](raw/application-user-guide/agent-development/sandbox/sandbox-sdk.md)。

## 限制和注意事项

- **地域限制**：当前仅支持 `cn-beijing` 地域，Endpoint 中 `region` 固定为此值；
- **文件限制**：单文件 ≤ 50 MB，工作空间总容量 ≤ 100 GB，文件保存时效为 30 天；不支持 `.csv`、`.yml`、`.sh`、`.whl`、`.tar.gz`、`.ts` 等扩展名（具体以接口返回错误码 `11900014` / `11900019` 为准）；
- **模版删除约束**：`DELETE /templates/{templateCode}` 仅在无任何 `running` 或 `paused` 实例时成功，否则返回 `409` 并附带关联实例 ID —— 详见 [删除模版](raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-delete.md)；
- **鉴权差异**：E2B SDK 的 `api_key` 字段**不参与百炼业务鉴权**，仅满足协议格式；真实鉴权依赖 HTTP Header 中的 `Authorization: Bearer <your-api-key>`；
- **错误处理**：兼容 E2B 协议的接口返回原生错误结构（非百炼统一 `Result<T>`），HTTP 状态码语义与标准一致（如 `401` 表示 API Key 无效，`404` 表示资源不存在），详细错误码见 [Sandbox API 错误码](raw/application-api-reference/sandbox-api/sandbox-api-errors.md)。

## 来源文档

- [概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)
- [认证](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)
- [Sandbox API 错误码](../../raw/application-api-reference/sandbox-api/sandbox-api-errors.md)
- [实例管理](../../raw/application-api-reference/sandbox-api/sandbox-api-instances.md)
- [创建实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md)
- [列举实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-list.md)
- [获取实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-get.md)
- [连接实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-connect.md)
- [恢复实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-resume.md)
- [暂停实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-pause.md)
- [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)
- [释放实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-delete.md)
- [列举模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-list.md)
- [获取模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-get.md)
- [更新模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-update.md)
- [获取构建状态](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-build-status.md)
- [删除模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-delete.md)
- [模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md)


