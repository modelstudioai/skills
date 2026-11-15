# sandbox api

Sandbox API 是阿里云百炼提供的沙箱环境生命周期管理接口，兼容 E2B 协议，支持沙箱实例与模版的创建、查询、启停和释放。所有请求需通过阿里云百炼 API Key 鉴权，并经由工作空间专属 Endpoint 转发。该 API 适用于需要隔离、可复现、带网络/文件/环境配置能力的代码执行场景，如 Agent 工具调用、代码解释器后端等。

## 支持的模型/功能

Sandbox API 不直接提供“模型”服务，而是提供**沙箱运行时环境**（即容器化计算单元），其底层基于 envd 构建的定制镜像。当前支持以下官方基础镜像（通过 `fromImage` 指定）：
- `code-interpreter-v1`：默认镜像，预装 Python、Jupyter、常用数据科学库；
- `browser`：含无头浏览器（Chromium）的环境；
- `all-in-one`：集成上述能力的全功能镜像。

所有镜像托管于 `fc-e2b-registry.cn-beijing.cr.aliyuncs.com/runtime/`。用户可通过 [创建模版](raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md) 自定义资源规格（CPU/内存）、挂载文件、配置网络规则与环境变量，并构建专属模版。模版构建完成后，方可用于创建实例。

> **注意**：文档中多次提及 `fromImage` 缺省时使用“代码解释器镜像”，但未明确其完整镜像名；实际应填写 `fc-e2b-registry.cn-beijing.cr.aliyuncs.com/runtime/code-interpreter-v1`，否则可能构建失败。建议始终显式指定完整地址。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `Authorization` | Header | string | 是 | `Bearer <your-api-key>`，来自[认证](raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)文档 |
| `workspace_id` | Endpoint | string | 是 | 工作空间 ID，控制台右上角获取；Endpoint 格式为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox` |
| `templateID` | Request Body (创建实例) / Path (其他) | string | 是（创建实例） | 模版唯一标识，必须已构建完成（`status=ready`），详见[创建实例](raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md) |
| `sandboxID` | Path | string | 是 | 实例唯一 ID，由创建接口返回，用于后续所有实例操作 |
| `source=sandbox_template` | Form Data / JSON Body (文件上传) | string | 是 | 文件上传时**必须**指定此值，否则无法用于模版挂载，见[文件上传](raw/application-api-reference/sandbox-api/sandbox-api-overview.md) |

其他重要参数包括：
- `timeout`（实例/连接超时，单位秒，范围 `[300, 604800]`）
- `allow_internet_access` / `networkConfig`（网络访问控制）
- `mntConfig`（文件挂载，`originFileId` 必须是 `source=sandbox_template` 且 `status=available` 的文件）

## 使用方式

1. **前置准备**：开通百炼服务，[创建 API Key](raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)，完成 SLR 授权（见[快速开始](raw/application-user-guide/agent-development/sandbox/sandbox-start-using/sandbox-quick-start.md)），并确认工作空间 ID 与地域（仅 `cn-beijing`）。
2. **上传文件（可选）**：若需挂载代码或配置，先调用 `/api/v1/agentstudio/files` 上传，`source=sandbox_template`，轮询至 `status=available`。
3. **创建模版**：调用 `POST /v3/templates`，传入 `cpuCount`/`memoryMB`、`fromImage`、`mntConfig` 等，获取 `templateID` 和 `buildID`。
4. **等待构建就绪**：调用 `GET /templates/{templateID}/builds/{buildID}/status`，直至 `status=ready`。
5. **创建实例**：调用 `POST /sandboxes`，传入 `templateID` 及生命周期参数（如 `timeout`, `autoPause`）。
6. **连接与交互**：调用 `POST /sandboxes/{sandboxID}/connect` 获取 `domain` 和 `envdAccessToken`，用于数据面通信；也可用 `pause`/`resume`/`delete` 管理实例状态。

推荐使用 E2B 官方 SDK（如 Python SDK），其协议兼容性已验证，详见[实例管理与使用](raw/application-user-guide/agent-development/sandbox/sandbox-sdk.md)。

## 限制和注意事项

- **地域限制**：当前仅支持 `cn-beijing` 地域，Endpoint 中 `region` 固定为此值。
- **文件限制**：单文件 ≤ 50 MB，工作空间总容量 ≤ 100 GB，保存时效 30 天；仅 `.yaml` 等白名单扩展名支持上传，`.csv`、`.yml`、`.sh`、`.whl`、`.tar.gz`、`.ts` 明确不支持（见[文件上传](raw/application-api-reference/sandbox-api/sandbox-api-overview.md)）。
- **模版与实例约束**：
  - 创建实例前，模版 `buildStatus` 必须为 `ready`，否则返回 409；
  - 删除模版前，必须确保无 `running` 或 `paused` 实例，否则返回 409（见[删除模版](raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-delete.md)）；
  - `mntConfig.mountPath` 必须以 `/home/user/workspace/uploads/` 开头，否则文件在实例中不可见。
- **鉴权特殊性**：E2B SDK 的 `api_key` 参数仅用于协议占位，**不参与百炼业务鉴权**；真实鉴权仅依赖 HTTP Header 中的 `Authorization: Bearer <your-api-key>`（见[认证](raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)）。
- **错误处理**：兼容 E2B 协议的接口不返回阿里云百炼标准 `Result<T>` 结构，错误响应格式贴近 E2B 原生定义，具体码值参考[Sandbox API 错误码](raw/application-api-reference/sandbox-api/sandbox-api-errors.md)。

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
- [释放实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-delete.md)
- [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)
- [列举模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-list.md)
- [模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md)
- [更新模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-update.md)
- [获取构建状态](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-build-status.md)
- [获取模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-get.md)
- [删除模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-delete.md)


