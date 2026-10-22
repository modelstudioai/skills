# sandbox api

Sandbox API 是阿里云百炼提供的沙箱环境生命周期管理接口，兼容 E2B 协议，支持模版构建、实例创建与管控、文件挂载及网络策略配置。所有请求需通过阿里云百炼 AI 网关转发，鉴权依赖 API Key，并需提前完成工作空间 SLR 授权。该 API 面向 Agent 开发者，用于构建可编程、隔离、带状态的执行环境。

## 支持的模型/功能

- **模版（Template）管理**：支持创建、列举、获取、更新、删除模版，以及查询构建状态。模版定义运行时资源规格（CPU/memory）、基础镜像（如 `code-interpreter-v1`、`browser`）、挂载文件（需先上传至 `source=sandbox_template`）、网络规则（`allowOut`/`denyOut`）和环境变量。
- **实例（Sandbox）管理**：支持创建、列举、获取详情、连接、暂停、恢复、释放实例。实例基于已构建完成（`status=ready`）的模版启动，支持自动暂停/恢复、超时控制与公网访问开关。
- **文件上传**：提供表单上传与预签名地址直传两种方式，仅 `source=sandbox_template` 且 `status=available` 的文件可用于模版挂载。详见 [文件上传](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)。
- **E2B 兼容性**：除模版更新（`PUT /templates/{templateCode}`）为阿里云百炼扩展协议外，其余接口（如 `/sandboxes`、`/v2/sandboxes`）在路径、方法、响应结构上贴近 [E2B 官方 API](https://docs.e2b.dev/api-reference)，通用字段语义可参考其文档。

> **注意**：文档中多次出现 `GET /sandboxes` 与 `GET /v2/sandboxes` 并列作为列举实例接口（见 [概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md) 和 [列举实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-list.md)），但后者是当前推荐路由；前者虽兼容，但分页参数（如 `cursor`）仅在 `/v2/sandboxes` 中生效，`/sandboxes` 实际不支持游标分页。建议统一使用 `/v2/sandboxes`。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `Authorization` | Header | string | 是 | `Bearer <your-api-key>`，API Key 从[百炼控制台](https://bailian.console.aliyun.com/?tab=model#/api-key)获取，见 [认证](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md) |
| `workspace_id` | Endpoint | string | 是 | 工作空间 ID，控制台右上角下拉菜单查看；Endpoint 格式为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox` |
| `templateID` | Body/Path | string | 是（创建/更新/删除时） | 模版唯一标识，来自 `POST /v3/templates` 响应；模版必须处于 `ready` 状态才可创建实例 |
| `sandboxID` | Path | string | 是（实例操作时） | 实例唯一 ID，来自 `POST /sandboxes` 响应，格式如 `sbx-xxx` |
| `originFileId` | Body (`mntConfig`) | string | 是（挂载文件时） | 文件 ID，须通过 `source=sandbox_template` 上传并轮询至 `status=available`，见 [文件上传](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md) |
| `timeout` | Body | integer | 否 | 实例或连接超时时间（秒），范围 `[300, 604800]`；影响 `autoPause` 行为与 `on_timeout` 策略 |

## 使用方式

1. **前置准备**  
   - 开通百炼服务，[创建 API Key](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)；  
   - 在百炼控制台完成 [SLR 授权](../../raw/application-user-guide/agent-development/sandbox/sandbox-start-using/sandbox-quick-start.md)；  
   - 获取 `workspace_id`，确认地域为 `cn-beijing`。

2. **构建模版流程**  
   - 上传所需文件（如 `config.json`）至 `source=sandbox_template`；  
   - 调用 `POST /v3/templates` 创建模版，传入 `mntConfig` 引用已上传文件；  
   - 轮询 `GET /templates/{templateID}/builds/{buildID}/status` 直至 `status=ready`。

3. **管理实例流程**  
   - 调用 `POST /sandboxes` 创建实例（需 `templateID`）；  
   - 调用 `POST /sandboxes/{sandboxID}/connect` 获取 `domain` 与 `envdAccessToken` 以访问数据面；  
   - 按需调用 `pause`/`resume`/`DELETE` 控制生命周期。

4. **SDK 支持**  
   可直接使用 E2B 官方 SDK（如 Python `e2b` 包），只需将 `api_key` 设为占位符（如 `e2b_${ALIYUN_UID}`），实际鉴权由 `Authorization` Header 完成，详见 [实例管理与使用](../../raw/application-user-guide/agent-development/sandbox/sandbox-sdk.md)。

## 限制和注意事项

- **地域限制**：当前仅支持 `cn-beijing` 地域，Endpoint 中 `region` 字段不可更改。
- **文件限制**：单文件 ≤ 50 MB，工作空间总容量 ≤ 100 GB，保存时效 30 天；仅 `.yaml` 等白名单扩展名允许上传，`.csv`、`.sh`、`.ts` 等明确不支持（见 [文件上传](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)）。
- **模版约束**：`cpuCount` 与 `memoryMB` 必须匹配平台预设规格组合；`mntConfig.mountPath` 必须以 `/home/user/workspace/uploads/` 开头，否则挂载无效。
- **错误处理**：HTTP 409 表示状态冲突（如模版未就绪时创建实例、存在活跃实例时删除模版）；文件类错误码（如 `11900014`）需结合 [错误码](../../raw/application-api-reference/sandbox-api/sandbox-api-errors.md) 文档排查。
- **权限安全**：API Key 具有账号级权限，严禁硬编码或提交至公开仓库；`Authorization` Header 是唯一有效鉴权方式，SDK 中的 `X-API-Key` 仅为协议占位符。

## 来源文档

- [概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)
- [认证](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)
- [创建实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md)
- [列举实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-list.md)
- [获取实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-get.md)
- [连接实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-connect.md)
- [暂停实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-pause.md)
- [恢复实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-resume.md)
- [释放实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-delete.md)
- [错误码](../../raw/application-api-reference/sandbox-api/sandbox-api-errors.md)
- [模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md)
- [列举模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-list.md)
- [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)
- [更新模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-update.md)
- [获取构建状态](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-build-status.md)
- [删除模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-delete.md)
- [获取模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-get.md)
- [实例管理](../../raw/application-api-reference/sandbox-api/sandbox-api-instances.md)


