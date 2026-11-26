# sandbox api

Sandbox API 是阿里云百炼提供的沙箱环境生命周期管理接口，兼容 E2B 协议，支持模版构建、实例创建与管控、文件挂载等核心能力。所有请求需通过阿里云百炼 AI 网关转发，使用统一的 API Key 鉴权，并按工作空间与地域拼装 Endpoint。开发者可通过 REST 直调或 E2B 官方 SDK 接入。

## 支持的模型/功能

- **模版管理**：支持创建（`POST /v3/templates`）、列举（`GET /v2/templates`）、获取（`GET /templates/{templateCode}`）、更新（`PUT /templates/{templateCode}`）、查询构建状态（`GET /templates/{templateCode}/builds/{buildID}/status`）和删除模版（`DELETE /templates/{templateCode}`）。模版构建成功且状态为 `ready` 后方可创建实例，详见 [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md) 和 [获取构建状态](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-build-status.md)。
- **实例管理**：支持全生命周期操作，包括创建（`POST /sandboxes`）、列举（`GET /v2/sandboxes`）、获取详情（`GET /sandboxes/{sandboxID}`）、连接（`POST /sandboxes/{sandboxID}/connect`）、暂停（`POST /sandboxes/{sandboxID}/pause`）、恢复（`POST /sandboxes/{sandboxID}/resume`）和释放（`DELETE /sandboxes/{sandboxID}`）。
- **文件挂载**：仅支持通过 `source=sandbox_template` 上传的文件参与模版构建；挂载路径必须以 `/home/user/workspace/uploads/` 开头，否则文件在实例中不可见（[文件上传](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md) 中明确约束）。

> **注意**：文档 1 中称“更新模版为阿里云百炼自定义协议”，而文档 15 明确说明该接口“不声明完全兼容 E2B Update Template v2”，二者表述一致，但需注意其非标准 E2B 行为，不可直接复用 E2B SDK 的 update 方法。

## 关键参数

- **通用参数**：
  - `workspace_id`：必填，从百炼控制台右上角下拉菜单获取；
  - `region`：当前仅支持 `cn-beijing`；
  - `Authorization: Bearer <your-api-key>`：API Key 鉴权，非 E2B SDK 所用 `X-API-Key`（见 [认证](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)）。

- **模版创建/更新关键字段**：
  - `cpuCount` 与 `memoryMB` 必须同时传且匹配平台预设规格组合；
  - `mntConfig[].originFileId`：必须指向 `source=sandbox_template` 且 `status=available` 的文件（文档 14、15 均强调）；
  - `mountPath`：必须以 `/home/user/workspace/uploads/` 开头，否则挂载无效；
  - `maxRunningTimeout` 与 `autoPauseTime`：若同时设置，前者优先生效；均未设置时默认最大运行时间为 604800 秒（7 天）。

- **实例创建关键字段**：
  - `templateID`：必须为已构建完成（`status=ready`）的模版 ID，否则返回 409；
  - `timeout`：取值范围 `[300, 604800]` 秒；
  - `lifecycle.on_timeout`：支持字符串 `"pause"` 或对象 `{ "action": "pause" }`，兼容性设计；
  - `network` 配置中 `denyOut` 不支持域名（仅 IPv4/IPv6/CIDR），而 `allowOut` 支持域名（见文档 14）。

## 使用方式

1. **前置准备**：
   - 开通百炼服务并[创建 API Key](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)；
   - 完成 SLR 服务授权（首次使用必需）；
   - 获取 `workspace_id` 并确认地域为 `cn-beijing`。

2. **Endpoint 拼装**：
   ```text
   https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox
   ```

3. **典型流程**：
   - 上传配置文件 → 创建模版 → 轮询构建状态至 `ready` → 创建实例 → 连接实例获取 `domain` 与 `envdAccessToken` → 数据面交互；
   - 文件上传支持表单（`multipart/form-data`）和预签名地址直传两种方式，大文件推荐后者（见 [文件上传](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)）。

4. **SDK 接入**：
   - 可直接使用 E2B 官方 SDK（如 `e2b-python`），但需注意：
     - 鉴权 Header 应设为 `Authorization: Bearer <your-bailian-api-key>`，而非 SDK 默认的 `X-API-Key`；
     - 模版更新等扩展接口需自行封装 REST 调用。

## 限制和注意事项

- **文件限制**：单文件 ≤ 50 MB，工作空间总容量 ≤ 100 GB，保存时效 30 天；支持 `.yaml`，不支持 `.csv`、`.yml`、`.sh`、`.whl`、`.tar.gz`、`.ts`（见 [文件上传](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)）。
- **模版与实例约束**：
  - 删除模版前必须确保无运行中或暂停中的实例，否则返回 409（文档 18）；
  - 实例 `timeout` 到期后行为由 `lifecycle.on_timeout` 决定，若为 `pause` 则进入暂停态，后续 `connect` 可自动恢复（文档 5、9）。
- **错误处理**：
  - 兼容 E2B 协议的接口错误结构贴近 E2B 原生定义，但 HTTP 状态码与错误码以百炼侧为准（如 `415` 表示文件类型不被允许，对应 code `11900014`）；
  - 文件相关错误需重点检查 `source`、`status`、`mime_type` 及路径合法性（见 [Sandbox API 错误码](../../raw/application-api-reference/sandbox-api/sandbox-api-errors.md)）。
- **网络配置差异**：`network.denyOut` 不支持域名（文档 14），而部分 E2B 文档可能允许，此为阿里云百炼侧明确限制。

## 来源文档

- [概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)
- [认证](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)
- [Sandbox API 错误码](../../raw/application-api-reference/sandbox-api/sandbox-api-errors.md)
- [实例管理](../../raw/application-api-reference/sandbox-api/sandbox-api-instances.md)
- [创建实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md)
- [列举实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-list.md)
- [暂停实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-pause.md)
- [连接实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-connect.md)
- [获取实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-get.md)
- [恢复实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-resume.md)
- [释放实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-delete.md)
- [模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md)
- [列举模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-list.md)
- [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)
- [更新模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-update.md)
- [获取构建状态](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-build-status.md)
- [获取模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-get.md)
- [删除模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-delete.md)


