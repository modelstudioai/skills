# [sandbox](../guides/sandbox.md) api

Sandbox API 是阿里云百炼平台提供的沙箱实例与模版全生命周期管理接口，兼容 E2B 协议，支持通过 RESTful HTTP 接口或 E2B SDK 进行调用。所有请求需经阿里云百炼 AI 网关转发，并使用百炼 API Key 鉴权。该 API 适用于需要动态创建、连接、暂停和销毁隔离计算环境的 AI 应用场景，如代码执行、模型推理沙箱、自动化测试等。

## 支持的模型/功能

Sandbox API 不直接提供大语言模型（LLM）推理能力，而是提供**沙箱运行时基础设施**，即基于 envd 构建的可编程、可配置、带网络与资源隔离的 Linux 容器环境。其核心能力分为两类：

- **模版管理**：定义沙箱的底层镜像、CPU/内存规格、网络策略、挂载文件、环境变量等静态配置。模版构建完成后生成 `templateID`，供实例复用。详见 [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md) 和 [更新模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-update.md)。
- **实例管理**：基于模版动态创建、查询、连接、暂停、恢复和释放运行时实例。每个实例拥有独立域名、访问 token 和完整生命周期控制。详见 [创建实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md) 和 [连接实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-connect.md)。

> **注意**：文档中多次提及“兼容 E2B 协议”，但实际实现存在关键差异：阿里云百炼侧**不使用 E2B SDK 中的 `X-API-Key` 或 `api_key` 字段进行业务鉴权**，仅要求其满足协议格式（推荐填 `e2b_${ALIYUN_UID}`），真实鉴权依赖 `Authorization: Bearer <your-api-key>` 头。此行为与标准 E2B 自托管部署不同，开发者需特别注意。

## 关键参数

### 全局参数
- `workspace_id`：工作空间 ID，从百炼控制台右上角获取，用于拼装 Endpoint。
- `region`：当前仅支持 `cn-beijing`，构成完整 Endpoint：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox`。
- `Authorization`：HTTP Header，值为 `Bearer <your-api-key>`，API Key 须在[控制台](https://bailian.console.aliyun.com/?tab=model#/api-key)开通。

### 实例创建关键参数（`POST /sandboxes`）
| 参数 | 类型 | 说明 |
|------|------|------|
| `templateID` | string | 必填；已构建完成（`status=ready`）的模版 ID，否则返回 409 |
| `timeout` | integer | 可选；实例生命周期秒数，范围 `[300, 604800]`（5 分钟 ~ 7 天） |
| `allow_internet_access` | boolean | 可选；是否允许公网出向流量（等价于 `network.allowPublicTraffic`） |
| `lifecycle.on_timeout` | string | 可选；超时后行为，`"pause"`（暂停）或 `"terminate"`（释放），默认 `"pause"` |
| `autoResume` | boolean | 可选；连接时是否自动恢复暂停中的实例 |

### 模版创建关键参数（`POST /v3/templates`）
| 参数 | 类型 | 说明 |
|------|------|------|
| `cpuCount` & `memoryMB` | integer | **必须同时指定**，且必须匹配平台预设的规格组合（如 `1/2048`, `4/8192`） |
| `maxRunningTimeout` | integer | 可选；实例最大运行时间（秒），优先级高于 `autoPauseTime`；两者均未传时默认 7 天 |
| `networkConfig.allowOut` / `denyOut` | array<string> | `allowOut` 支持域名/IP/CIDR；`denyOut` **仅支持 IP/CIDR，不支持域名**（见 [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)） |

## 使用方式

1. **前置准备**：开通百炼服务、创建 API Key、完成 SLR 授权（见 [API 总览与认证](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)）。
2. **创建模版**：调用 `POST /v3/templates` 提交资源配置，获取 `templateID` 和 `buildID`。
3. **等待构建就绪**：轮询 `GET /templates/{templateID}/builds/{buildID}/status`，直至 `status="ready"`。
4. **创建实例**：调用 `POST /sandboxes`，传入 `templateID` 及所需运行时参数。
5. **连接与交互**：调用 `POST /sandboxes/{sandboxID}/connect` 获取 `domain` 和 `envdAccessToken`，用于后续数据面通信。
6. **生命周期管理**：按需调用 `/pause`、`/resume`、`/delete` 控制实例状态。

> **注意**：列举接口路径存在版本差异——实例列表为 `GET /v2/sandboxes`（文档明确标注），但部分旧文档或 SDK 示例可能仍引用 `GET /sandboxes`（兼容路由）；模版列表为 `GET /v2/templates`，而创建模版主路径为 `POST /v3/templates`。建议以 `/v2/` 和 `/v3/` 显式路径为准，避免隐式兼容带来的不确定性。

## 限制和注意事项

- **地域限制**：当前仅支持 `cn-beijing` 地域，Endpoint 中 region 固定不可更改。
- **资源规格约束**：`cpuCount` 与 `memoryMB` 必须成对出现且匹配平台白名单组合，单独修改任一字段将导致 `400` 错误。
- **实例状态依赖**：暂停/恢复操作仅对 `running` 状态实例有效；释放操作对 `running` 或 `paused` 状态均有效；但删除模版前**必须确保无任何活跃实例**（包括 `running` 和 `paused`），否则返回 `409`（见 [删除模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-delete.md)）。
- **网络配置限制**：`denyOut` 黑名单不支持域名（仅 IPv4/IPv6/CIDR），而 `allowOut` 支持，设计网络策略时需注意此不对称性。
- **错误处理**：所有接口遵循统一错误结构 `{ "code": number, "message": string, "requestID": string }`，常见状态码含义见 [API 总览与认证](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md) 的错误响应章节。

## 来源文档

- [API 总览与认证](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)
- [实例管理](../../raw/application-api-reference/sandbox-api/sandbox-api-instances.md)
- [创建实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md)
- [列举实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-list.md)
- [获取实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-get.md)
- [暂停实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-pause.md)
- [连接实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-connect.md)
- [恢复实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-resume.md)
- [释放实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-delete.md)
- [模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md)
- [列举模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-list.md)
- [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)
- [更新模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-update.md)
- [获取模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-get.md)
- [获取构建状态](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-build-status.md)
- [删除模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-delete.md)


