# sandbox api

Sandbox API 是阿里云百炼提供的沙箱环境生命周期管理接口，兼容 E2B 协议，支持沙箱实例与模版的创建、查询、更新和销毁。所有请求需通过阿里云百炼 API Key 鉴权，并经由工作空间专属 Endpoint 转发。管控面能力（如模版构建、文件上传）与数据面访问（如连接、执行）分离，开发者需按阶段分步调用。

## 支持的模型/功能

- **沙箱实例管理**：支持创建、列举、获取详情、连接、暂停、恢复和释放实例，全部兼容 E2B 协议语义（如 `connect()` 对应 `/sandboxes/{sandboxID}/connect`）。详见 [创建实例](raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md) 和 [实例管理](raw/application-api-reference/sandbox-api/sandbox-api-instances.md)。
- **沙箱模版管理**：支持创建、列举、获取、更新、查询构建状态及删除模版；其中更新模版为阿里云百炼扩展协议，不完全兼容 E2B v2 Update Template。模版构建完成后状态需为 `ready` 才可创建实例，参见 [获取构建状态](raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-build-status.md)。
- **文件挂载能力**：仅支持通过 `source=sandbox_template` 上传的文件用于模版挂载（如 `mntConfig`），且文件状态必须为 `available`。不支持 `.csv`、`.yml`、`.sh`、`.whl`、`.tar.gz` 等扩展名，完整限制见 [概览](raw/application-api-reference/sandbox-api/sandbox-api-overview.md)。

> **注意**：文档中 `mntConfig.mountPath` 的路径要求存在不一致说明——[创建模版](raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md) 和 [更新模版](raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-update.md) 均明确要求 `mountPath` 必须以 `/home/user/workspace/uploads/` 开头；但 [概览](raw/application-api-reference/sandbox-api/sandbox-api-overview.md) 仅提示“推荐写完整文件路径”，未强调强制前缀。实际调用时请严格遵循前缀要求，否则文件不会出现在实例中。

## 关键参数

| 参数 | 位置 | 类型 | 说明 |
|------|------|------|------|
| `Authorization: Bearer <API_KEY>` | Header | string | 阿里云百炼 API Key，非 E2B SDK 所需的 `X-API-Key`；后者仅用于协议占位，[认证](raw/application-api-reference/sandbox-api/sandbox-api-authentication.md) 文档已明确说明。 |
| `templateID` | 请求体（创建实例） / 路径（模版操作） | string | 模版唯一标识，创建实例前必须确保其构建状态为 `ready`；模版更新后 `templateID` 不变，但 `version` 递增。 |
| `timeout` | 请求体（创建/连接/恢复实例） | integer | 实例生命周期或连接会话超时时间，单位秒，取值范围 `[300, 604800]`（5 分钟至 7 天）。 |
| `mntConfig` | 请求体（创建/更新模版） | array<object> | 文件挂载配置，`originFileId` 必须指向 `source=sandbox_template` 且 `status=available` 的文件；`mountPath` 必须以 `/home/user/workspace/uploads/` 开头。 |
| `autoPauseTime` / `maxRunningTimeout` | 请求体（创建/更新模版） | integer | 控制模版级自动行为：仅设 `autoPauseTime` 则到期暂停；两者均设则 `maxRunningTimeout` 优先生效（到期直接释放）。 |

## 使用方式

1. **前置准备**：开通百炼服务，[创建 API Key](raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)，完成 SLR 授权（见[快速开始](raw/application-user-guide/agent-development/sandbox/sandbox-start-using/sandbox-quick-start.md)），并获取 `workspace_id`。
2. **Endpoint 构造**：使用固定格式 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox`（当前仅支持 `cn-beijing` 地域）。
3. **文件上传（如需挂载）**：
   - 小文件：表单上传，`source=sandbox_template`；
   - 大文件：预签名地址上传，需调用 `/files` 获取 `upload_url`，PUT 后调用 `/files/{file_id}/complete` 并轮询至 `status=available`。
4. **模版构建**：调用 `/v3/templates` 创建模版 → 用返回的 `buildID` 轮询 `/templates/{templateCode}/builds/{buildID}/status` 直至 `status=ready`。
5. **实例操作**：基于就绪模版调用 `/sandboxes` 创建实例 → 使用 `/sandboxes/{sandboxID}/connect` 获取数据面凭证 → 按需调用 `/pause`、`/resume` 或 `/sandboxes/{sandboxID}`（DELETE）管理生命周期。

## 限制和注意事项

- **地域限制**：当前仅支持 `cn-beijing` 地域，Endpoint 中 `region` 字段不可替换为其他值。
- **文件限制**：单文件 ≤ 50 MB，工作空间总容量 ≤ 100 GB，保存时效 30 天；不支持 `.csv`、`.yml`、`.sh`、`.whl`、`.tar.gz` 等类型（[概览](raw/application-api-reference/sandbox-api/sandbox-api-overview.md) 明确列出）。
- **错误处理**：兼容 E2B 协议的接口不返回阿里云百炼标准 `Result<T>` 结构，错误响应贴近 E2B 原生格式；通用错误码见 [错误码](raw/application-api-reference/sandbox-api/sandbox-api-errors.md)，文件类错误码以 `119000xx` 开头。
- **模版删除约束**：若模版关联任何运行中或暂停中的实例，`DELETE /templates/{templateCode}` 将返回 409 错误，并在响应体中携带 `sandboxId` 和 `sandboxInstanceId`，需先释放实例再删除模版（[删除模版](raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-delete.md)）。
- **SDK 兼容性**：E2B 官方 SDK 可直接接入，但需注意：`api_key` 参数应填 `e2b_${ALIYUN_UID}` 占位，真实鉴权依赖 Header 中的 `Authorization`（[认证](raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)）。

## 来源文档

- [概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)
- [认证](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)
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
- [列举模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-list.md)
- [获取模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-get.md)
- [更新模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-update.md)
- [获取构建状态](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-build-status.md)
- [删除模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-delete.md)
- [实例管理](../../raw/application-api-reference/sandbox-api/sandbox-api-instances.md)


