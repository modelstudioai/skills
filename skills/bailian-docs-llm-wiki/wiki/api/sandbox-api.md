# sandbox api

Sandbox API 是阿里云百炼提供的沙箱环境生命周期管理接口，兼容 E2B 协议，支持通过 RESTful 接口创建、管理沙箱实例与模版，并挂载自定义文件。所有管控面请求经百炼 AI 网关转发，需使用阿里云百炼 API Key 鉴权。开发者可直接调用 HTTP 接口，也可借助 E2B 官方 SDK（如 Python SDK）接入，详见 [实例管理与使用](raw/application-user-guide/agent-development/sandbox/sandbox-sdk.md)。

## 支持的模型/功能

- **实例管理**：支持创建、列举、获取、连接、暂停、恢复和释放沙箱实例。实例基于预构建模版启动，状态包括 `running`、`paused`，暂停后可保留内存与文件系统状态。
- **模版管理**：支持创建、列举、获取、更新、查询构建状态及删除模版。模版定义 CPU、内存、基础镜像、网络规则、环境变量及挂载文件；每次更新触发新版本构建，`version` 递增，`buildStatus` 为 `building` → `ready` 后方可创建实例。
- **文件挂载**：仅支持通过 `/api/v1/agentstudio/files` 上传 `source=sandbox_template` 的文件，且必须等待其 `status` 变为 `available` 后，才能在 `mntConfig` 中引用。支持表单上传与预签名地址直传两种方式，详见 [文件上传](https://help.aliyun.com/zh/model-studio/sandbox-api-overview#h-sandbox-api-file-upload)。
- **网络与生命周期配置**：实例级支持 `allow_internet_access`、出口白/黑名单（`allowOut`/`denyOut`）、`maskRequestHost`；生命周期支持 `on_timeout`（`pause` 或自动释放）与 `auto_resume`。

> **注意**：文档中 `mntConfig.mountPath` 要求以 `/home/user/workspace/uploads/` 开头，但[创建模版](raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)与[更新模版](raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-update.md)均明确说明：“路径不在该目录下时接口接受配置但实例中不会出现文件”。因此，非该前缀路径虽能提交成功，但实际挂载无效，务必严格遵守。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `Authorization: Bearer <your-api-key>` | Header | string | 是 | 阿里云百炼 API Key，非 E2B SDK 所用 `X-API-Key`；详见 [认证](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md) |
| `workspace_id` | Endpoint 路径 | string | 是 | 百炼控制台右上角获取的工作空间 ID，用于拼装 Base URL：<br>`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox` |
| `templateID` | 请求体（创建实例）或路径参数（其他操作） | string | 是（创建/操作实例时） | 模版唯一标识，来自 `/v3/templates` 创建响应；模版必须处于 `ready` 构建状态才可创建实例 |
| `sandboxID` | 路径参数 | string | 是 | 实例唯一 ID，来自 `/sandboxes` 创建响应，用于后续所有实例操作 |
| `originFileId` | `mntConfig` 数组元素 | string | 是（挂载文件时） | 文件上传后返回的 `id`，且该文件 `source` 必须为 `sandbox_template`、`status` 必须为 `available` |
| `timeout` | 请求体（创建/连接/恢复实例） | integer | 否 | 实例生命周期或连接会话超时时间（秒），范围 `[300, 604800]`；`maxRunningTimeout` 优先级高于 `autoPauseTime` |

## 使用方式

1. **前置准备**：
   - 开通百炼服务，[创建 API Key](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)；
   - 在百炼控制台完成 [SLR 授权](../../raw/application-user-guide/agent-development/sandbox/sandbox-start-using/sandbox-quick-start.md)；
   - 获取 `workspace_id`。

2. **文件上传（如需挂载）**：
   ```bash
   curl -X POST "https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/files" \
     -H "Authorization: Bearer $BAILIAN_API_KEY" \
     -F "file=@./config.json" \
     -F "source=sandbox_template"
   ```
   轮询 `GET /api/v1/agentstudio/files/{file_id}` 直至 `status` 为 `available`。

3. **创建模版**：
   ```bash
   curl -X POST "$BASE_URL/v3/templates" \
     -H "Authorization: Bearer $BAILIAN_API_KEY" \
     -d '{"name":"my-template","cpuCount":1,"memoryMB":2048,"mntConfig":[{"originFileId":"file_xxx","mountPath":"/home/user/workspace/uploads/config.json"}]}'
   ```
   记录返回的 `templateID` 和 `buildID`，调用 `GET /templates/{templateID}/builds/{buildID}/status` 等待 `status=ready`。

4. **创建实例**：
   ```bash
   curl -X POST "$BASE_URL/sandboxes" \
     -H "Authorization: Bearer $BAILIAN_API_KEY" \
     -d '{"templateID":"your-template-id","timeout":3600}'
   ```
   成功后获得 `sandboxID`，用于后续操作。

5. **数据面访问**：
   - 调用 `POST /sandboxes/{sandboxID}/connect` 获取 `domain` 与 `envdAccessToken`；
   - 使用 E2B SDK 的 `connect()` 方法或直接构造 WebSocket 连接（需 `envdUrl` + `envdAccessToken`）。

## 限制和注意事项

- **地域限制**：当前仅支持 `cn-beijing` 地域，Endpoint 中 `region` 固定为 `cn-beijing`。
- **文件限制**：
  - 单文件 ≤ 50 MB；
  - 工作空间总容量 ≤ 100 GB；
  - 保存时效 30 天；
  - 仅 `.yaml` 明确支持；`.csv`、`.yml`、`.sh`、`.whl`、`.tar.gz`、`.ts` 等不支持（见 [概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)）。
- **资源规格**：`cpuCount` 与 `memoryMB` 必须同时传递，且必须匹配平台提供的组合（如 1 vCPU + 2048 MB），否则创建/更新模版失败。
- **错误处理**：
  - 通用错误码参考 [错误码](../../raw/application-api-reference/sandbox-api/sandbox-api-errors.md)，如 `401`（API Key 无效）、`409`（模版未就绪或存在活跃实例）；
  - 兼容 E2B 协议的接口错误结构贴近 E2B 原生定义，可对照 [E2B 官方文档](https://docs.e2b.dev/api-reference) 理解。
- **鉴权说明**：E2B SDK 的 `api_key` 参数（如 `e2b_${ALIYUN_UID}`）仅用于满足协议格式，**阿里云百炼侧不校验它**；业务鉴权完全依赖 HTTP Header 中的 `Authorization: Bearer <your-api-key>`（见 [认证](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)）。

## 来源文档

- [认证](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)
- [概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)
- [错误码](../../raw/application-api-reference/sandbox-api/sandbox-api-errors.md)
- [创建实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md)
- [实例管理](../../raw/application-api-reference/sandbox-api/sandbox-api-instances.md)
- [获取实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-get.md)
- [列举实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-list.md)
- [连接实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-connect.md)
- [暂停实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-pause.md)
- [释放实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-delete.md)
- [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)
- [列举模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-list.md)
- [获取模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-get.md)
- [更新模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-update.md)
- [获取构建状态](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-build-status.md)
- [删除模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-delete.md)
- [恢复实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-resume.md)
- [模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md)


