# [sandbox](../guides/sandbox.md) api

Sandbox API 是阿里云百炼平台提供的沙箱环境管理接口，兼容 E2B 协议，支持沙箱实例的全生命周期管理（创建、连接、暂停、恢复、释放）及沙箱模版的构建与配置管理。所有请求通过百炼 AI 网关转发，使用标准阿里云百炼 API Key 鉴权，Endpoint 按工作空间与地域动态生成。该 API 面向需要动态执行代码、隔离运行环境或构建 AI Agent 工作流的开发者。

## 支持的模型/功能

Sandbox API 不直接提供语言模型推理能力，而是提供**可编程的计算沙箱环境**，其核心能力分为两类：

- **实例管理**：基于已构建完成的模版启动独立、隔离的 Linux 运行时（基于 envd），支持按需连接、暂停、恢复与释放。实例内可自由安装依赖、运行任意代码（Python、Node.js、Shell 等），并可通过 `domain` + `trafficAccessToken` 访问数据面服务。
- **模版管理**：定义沙箱的底层镜像与运行时配置（CPU、内存、网络规则、环境变量、文件挂载等）。模版创建后需等待构建状态变为 `ready` 才能用于创建实例；更新模版会触发新版本构建，`templateID` 保持不变但 `version` 递增。

> **注意**：文档中多次提及“兼容 E2B 协议”，但实际实现存在关键差异：阿里云百炼侧**不使用 E2B SDK 的 `X-API-Key` 或 `api_key` 字段进行业务鉴权**，仅要求其满足协议格式（推荐填 `e2b_${ALIYUN_UID}`），真实鉴权完全依赖 HTTP Header 中的 `Authorization: Bearer <your-api-key>`。详见 [API 总览与认证](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)。

## 关键参数

### 实例创建（`POST /sandboxes`）
- `templateID`（必填，string）：已构建完成的模版 ID，未就绪时返回 409。
- `timeout`（可选，integer）：实例生命周期上限，单位秒，范围 `[300, 604800]`（5 分钟至 7 天）。
- `allow_internet_access`（可选，boolean）：是否允许公网访问，默认 `false`。
- `lifecycle.on_timeout`（可选，string）：超时后行为，`"pause"`（暂停）或 `"terminate"`（释放），默认 `"pause"`。
- `autoResume`（可选，boolean）：连接时是否自动恢复暂停的实例。

### 模版创建（`POST /v3/templates`）
- `cpuCount` & `memoryMB`（必填，integer）：必须**同时指定**，且必须匹配平台预设的规格组合（如 `1 CPU + 2048 MB`），不支持任意值。
- `networkConfig.allowOut`（可选，array<string>）：出口白名单，**支持域名**（如 `"example.com"`）。
- `networkConfig.denyOut`（可选，array<string>）：出口黑名单，**仅支持 IPv4/IPv6/CIDR，不支持域名**（见 [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)）。
- `maxRunningTimeout`（可选，integer）：实例最大运行时间，单位秒，范围 `[300, 604800]`。若与 `autoPauseTime` 同时设置，则 `maxRunningTimeout` 优先生效（到期强制释放）。

> **注意**：`autoPauseTime` 和 `maxRunningTimeout` 的语义在不同文档中存在不一致表述。[创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md) 明确说明“两者都传时 `maxRunningTimeout` 优先生效”，而 [获取实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-get.md) 的响应字段描述中仅列出 `onTimeout`（对应 `lifecycle.on_timeout`），未体现 `maxRunningTimeout` 的运行时覆盖逻辑。开发者应以创建/更新模版时传入的 `maxRunningTimeout` 为准。

## 使用方式

1. **准备环境**：
   - 在百炼控制台开通服务、创建 API Key，并完成 SLR 授权（参考 [快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md)）。
   - 获取工作空间 ID（控制台右上角下拉菜单）和地域（当前仅支持 `cn-beijing`），拼装 Endpoint：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox`。

2. **创建模版**：
   ```bash
   curl -X POST "$BASE_URL/v3/templates" \
     -H "Authorization: Bearer $BAILIAN_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"name":"my-py311","cpuCount":1,"memoryMB":2048}'
   ```
   - 记录响应中的 `templateID` 和 `buildID`。
   - 轮询 `GET /templates/{templateID}/builds/{buildID}/status` 直至 `status` 为 `"ready"`。

3. **创建并操作实例**：
   - 创建：`POST /sandboxes` 传入 `templateID`。
   - 连接：`POST /sandboxes/{sandboxID}/connect` 获取 `domain` 和 `trafficAccessToken` 用于后续数据面调用。
   - 管理：`POST /sandboxes/{sandboxID}/pause`、`POST /sandboxes/{sandboxID}/resume`、`DELETE /sandboxes/{sandboxID}`。
   - 查询：`GET /sandboxes/{sandboxID}` 或 `GET /v2/sandboxes`（支持过滤）。

4. **SDK 集成**：
   - 可直接使用 E2B 官方 SDK（如 `e2b-python`），但需手动覆盖鉴权逻辑，将 `api_key` 设为占位符（如 `e2b_${ALIYUN_UID}`），并在 HTTP Client 层添加 `Authorization: Bearer <your-api-key>` Header。详情见 [实例管理与使用](../../raw/application-user-guide/sandbox/sandbox-sdk.md)。

## 限制和注意事项

- **地域限制**：当前 Sandbox API 仅支持 `cn-beijing` 地域，Endpoint 中 `region` 固定为 `cn-beijing`。
- **资源规格约束**：模版的 `cpuCount` 和 `memoryMB` 必须选择平台预设的组合，不可自定义（如 `2 CPU + 3000 MB` 无效）。
- **网络规则差异**：`denyOut` 黑名单**不支持域名**，仅接受 IP/CIDR；而 `allowOut` 白名单支持域名。此限制在 [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md) 中明确，但易被忽略。
- **实例状态依赖**：暂停（`pause`）操作要求实例处于 `running` 状态；恢复（`resume`）要求实例处于 `paused` 状态；释放（`DELETE`）前需确保无 `running` 或 `paused` 实例关联该模版（否则返回 409）。
- **错误处理**：HTTP 400 表示参数问题（如缺失 `templateID`、`timeout` 超限）；401 表示 API Key 无效；404 表示资源不存在；409 表示状态冲突（如模版有活跃实例时尝试删除，或模版未就绪时创建实例）；500/501 为服务端异常。
- **响应结构**：所有接口均**不封装为百炼统一的 `Result<T>` 结构**，而是直接返回 E2B 兼容的原始 JSON，开发者需按文档字段定义解析。

## 来源文档

- [API 总览与认证](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)
- [实例管理](../../raw/application-api-reference/sandbox-api/sandbox-api-instances.md)
- [创建实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md)
- [列举实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-list.md)
- [获取实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-get.md)
- [连接实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-connect.md)
- [暂停实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-pause.md)
- [恢复实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-resume.md)
- [模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md)
- [释放实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-delete.md)
- [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)
- [列举模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-list.md)
- [获取模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-get.md)
- [获取构建状态](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-build-status.md)
- [更新模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-update.md)
- [删除模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-delete.md)


