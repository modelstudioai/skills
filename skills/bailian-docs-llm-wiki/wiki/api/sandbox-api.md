# sandbox api

Sandbox API 是阿里云百炼平台提供的沙箱环境生命周期管理接口，兼容 E2B 协议，支持模版构建与实例的创建、连接、暂停、恢复和释放等操作。所有请求需通过阿里云百炼 API Key 鉴权，并按工作空间与地域拼装 Endpoint。该 API 专为需要动态、隔离、可编程执行环境的 AI 应用（如代码解释器、浏览器自动化、安全分析）提供底层支撑。

## 支持的模型/功能

Sandbox API 不直接提供“模型”服务，而是提供**可运行任意代码的沙箱环境**，其能力由模版（Template）定义。模版基于预置或自定义镜像构建，当前官方支持以下基础镜像（位于 `fc-e2b-registry.cn-beijing.cr.aliyuncs.com/runtime/`）：
- `code-interpreter-v1`：Python 环境，预装 pandas、numpy、matplotlib 等科学计算库；
- `browser`：Chromium 浏览器 + Playwright，支持网页渲染与交互；
- `all-in-one`：整合上述两类能力的全功能镜像。

模版可配置 CPU（vCPU）、内存（MB）、网络规则（白/黑名单）、环境变量、文件挂载及生命周期策略。实例则继承模版配置，并支持运行时动态调整超时、网络访问与自动恢复行为。详细模版能力请参见 [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)。

> **注意**：文档中多次提及 `fromImage` 可填写完整镜像地址，但未明确列出所有可用镜像标签；实际使用时应以控制台或 [获取模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-get.md) 接口返回的 `imageName` 和 `envdVersion` 为准，避免因镜像不可用导致构建失败。

## 关键参数

### 全局必要参数
- `Authorization: Bearer <your-api-key>`：HTTP Header 中必填，使用阿里云百炼控制台生成的 API Key。
- `workspace_id` 与 `region`：用于拼装 Endpoint，当前仅支持 `cn-beijing`，格式为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox`。

### 实例创建关键参数（`POST /sandboxes`）
| 字段 | 类型 | 说明 |
|------|------|------|
| `templateID` | string | 必填；模版 ID，必须已构建完成（状态为 `ready`），否则返回 409 |
| `timeout` | integer | 可选；实例生命周期秒数，范围 `[300, 604800]`（5 分钟 ~ 7 天） |
| `allow_internet_access` | boolean | 可选；是否允许公网访问，默认 `false`；与 `network.allowPublicTraffic` 语义一致 |
| `lifecycle.on_timeout` | string | 可选；到期行为，值为 `"pause"`（暂停）或 `"kill"`（释放），默认 `"kill"` |
| `autoResume` / `lifecycle.auto_resume` | boolean | 可选；连接时是否自动恢复暂停实例 |

### 模版创建关键参数（`POST /v3/templates`）
| 字段 | 类型 | 说明 |
|------|------|------|
| `cpuCount` & `memoryMB` | integer | 必填且必须**同时指定**，且需匹配平台预设规格组合（如 `1/2048`, `4/8192`），不支持任意值 |
| `maxRunningTimeout` | integer | 可选；实例最大运行总时长（秒），优先级高于 `autoPauseTime`；两者均未传时默认 `604800` |
| `networkConfig.allowOut` / `denyOut` | array<string> | `allowOut` 支持域名（如 `"example.com"`），`denyOut` **仅支持 CIDR/IPv4/IPv6，不支持域名**（见 [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)） |

## 使用方式

1. **前置准备**：开通百炼服务、创建 API Key、完成 SLR 授权、获取 `workspace_id`（见 [API 总览与认证](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)）。
2. **创建模版**：调用 `POST /v3/templates` 提交资源配置与镜像信息，获取 `templateID` 和 `buildID`。
3. **等待构建就绪**：轮询 `GET /templates/{templateID}/builds/{buildID}/status`，直到 `status === "ready"`。
4. **创建实例**：调用 `POST /sandboxes`，传入 `templateID` 及运行时参数，获得 `sandboxID`。
5. **连接与交互**：调用 `POST /sandboxes/{sandboxID}/connect` 获取 `domain` 和 `envdAccessToken`，用于后续数据面通信（如 exec、file upload）。
6. **生命周期管理**：根据需要调用 `/pause`、`/resume` 或 `/sandboxes/{sandboxID}`（DELETE）控制实例状态。

推荐使用 E2B 官方 SDK（如 Python、TypeScript）接入，SDK 自动处理协议细节与重试逻辑，详见 [实例管理与使用](../../raw/application-user-guide/sandbox/sandbox-sdk.md)。

## 限制和注意事项

- **地域限制**：当前 Sandbox API 仅支持 `cn-beijing` 地域，Endpoint 中 `region` 固定为此值。
- **资源规格约束**：模版的 `cpuCount` 和 `memoryMB` 必须成对出现且属于平台预设组合，单独修改任一字段将导致 400 错误。
- **网络规则差异**：`denyOut` 字段**不支持域名**（仅 CIDR/IPv4/IPv6），而 `allowOut` 支持；此限制在 [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md) 中有明确说明，但 [获取实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-get.md) 的响应示例中错误地将 `denyOut` 列为域名（如 `"10.0.0.0/8"` 是合法 CIDR，但 `"example.com"` 在 `denyOut` 中非法）。
- **模版删除保护**：删除模版前必须确保无任何 `running` 或 `paused` 实例，否则返回 409 并附带关联 `sandboxID`，需先调用 `DELETE /sandboxes/{sandboxID}` 清理。
- **响应结构**：所有接口**不封装为百炼统一 `Result<T>` 结构**，直接返回 E2B 兼容格式（如数组、对象），错误响应体为 `{ "code": xxx, "message": "xxx", "requestID": "xxx" }`。
- **鉴权兼容性**：E2B SDK 中的 `X-API-Key` 或 `api_key` 参数仅用于满足协议格式，百炼侧**完全忽略其值**，业务鉴权仅依赖 `Authorization: Bearer <your-api-key>`。

## 来源文档

- [API 总览与认证](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)
- [实例管理](../../raw/application-api-reference/sandbox-api/sandbox-api-instances.md)
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


