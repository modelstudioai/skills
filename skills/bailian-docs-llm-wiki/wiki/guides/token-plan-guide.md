# token plan guide

阿里云百炼提供两套面向 AI 编程工具的订阅制套餐：**Token Plan 团队版**与 **Coding Plan**。两者均整合千问、DeepSeek、GLM、Kimi、MiniMax 等主流模型，通过专属 API Key/Base URL 在 Claude Code、Cursor、Qwen Code、OpenCode 等工具中调用，避免按量计费的欠费风险。Token Plan 团队版按 Credits 计量、面向团队；Coding Plan 按调用次数计量、面向个人开发场景。详细差异见下文。

## 套餐对比

| 维度 | Token Plan 团队版 | Coding Plan |
| --- | --- | --- |
| 适用场景 | 一人公司/团队/企业日常办公 | 个人开发场景 |
| 支持模型 | 文本生成、图像生成模型 | 文本生成模型（Pro 套餐全模型） |
| 计费方式 | 按 Token 消耗抵扣 Credits | 按模型调用次数 |
| 使用频次限制 | 无每 5 小时/每周限额 | 每 5 小时/每周/每月限额 |
| 高峰期性能 | 多租户隔离，不排队 | 高峰期可能排队 |
| 数据安全 | 承诺不使用数据训练模型 | 数据用于服务改进与模型优化 |
| API Key 格式 | `sk-sp-xxx`（专属） | `sk-sp-xxx`（专属） |

> **注意**：两者 API Key 与 Base URL 互不相通，误用会导致按量计费扣费。Coding Plan Lite 版已于 2026 年 3 月起停止新购，4 月 13 日起停止续费与升级，已购用户可继续使用至到期。

## 接入步骤

两套套餐接入流程相同：订阅套餐 → 获取专属 API Key 和 Base URL → 配置 AI 工具。详见 [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-quickstart.md)。

### Base URL

Token Plan 团队版（华北2-北京地域）：

- OpenAI 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
- Anthropic 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`

Coding Plan：

- OpenAI 兼容：`https://coding.dashscope.aliyuncs.com/v1`
- Anthropic 兼容：`https://coding.dashscope.aliyuncs.com/apps/anthropic`
- 海外：`https://coding-intl.dashscope.aliyuncs.com/v1` 与 `.../apps/anthropic`

**协议必须与 Base URL 路径匹配**：Anthropic 协议端点以 `/apps/anthropic` 结尾，OpenAI 协议端点以 `/compatible-mode/v1` 或 `/v1` 结尾。混淆会触发 `400 InvalidParameter: url error` 或 `404`。

### 兼容的 AI 工具

两套套餐均适配：Claude Code、Cursor、Codex、Qwen Code、OpenCode、OpenClaw、Hermes Agent、Cline、Cherry Studio、Chatbox、Qoder、Lingma、Kilo CLI 等。

## Token Plan 团队版

### 支持的模型

模型清单为**精确字符串白名单**，必须逐字符完全匹配，禁止版本兼容推理。仅支持以下精确版本（部分示例）：

- 千问：`qwen3.7-max`（限时活动至 2026-07-22，Credits 减半并支持隐式缓存）、`qwen3.7-plus`、`qwen3.6-plus`、`qwen3.6-flash`、`qwen-image-2.0`、`qwen-image-2.0-pro`
- 万相：`wan2.7-image`、`wan2.7-image-pro`（图像生成）
- DeepSeek：`deepseek-v4-pro`、`deepseek-v4-flash`、`deepseek-v3.2`
- 月之暗面：`kimi-k2.7-code`、`kimi-k2.6`、`kimi-k2.5`
- 智谱 AI：`glm-5.2`、`glm-5.1`、`glm-5`
- MiniMax：`MiniMax-M2.5`

完整清单与判定规则见 [Token Plan（团队版）概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)。

### 套餐与定价

| 坐席类型 | 价格 | 月度额度 | 适用场景 |
| --- | --- | --- | --- |
| 标准坐席 | ¥198/坐席/月 | 25,000 Credits | 轻度使用 |
| 高级坐席 | ¥698/坐席/月 | 100,000 Credits | 日常高频 |
| 尊享坐席 | ¥1,398/坐席/月 | 250,000 Credits | 重度依赖 |

席位是最小订阅单位，每个席位绑定一个成员、对应一个 API Key，不可共享。另有**共享用量包**（¥5,000/个，625,000 Credits/个，有效期 1 个月），跨坐席共享，用于个别坐席超额抵扣。

### Credits 计费与抵扣顺序

单次消耗由模型类型、Token 用量、思考模式及工具调用动态决定，以账单为准。抵扣顺序：

1. 优先从坐席套餐月度额度抵扣；
2. 坐席额度用尽后从共享用量包抵扣（多个用量包优先抵扣最近到期的）；
3. 全部用尽后服务暂停，至下一计费周期或购买共享用量包补充额度。

坐席额度在订阅月到期时重置，未用完额度不累积。

### 团队管理

角色分拥有者、管理员、成员三级。管理员在管理后台创建成员、分配席位后系统自动生成专属 API Key。支持 SAML SSO 与钉钉接入，成员通过管理平台地址登录。席位可分配、回收、加购（按剩余时长折算费用）、升级（补缴差价）。用量分析仅在管理平台提供，可查看近 1/7/30 天 Credits 消耗趋势、各模型与各成员用量。详见 [团队管理](../../raw/model-user-guide/token-plan-guide/token-plan-team.md)。

### 使用限制与数据安全

- **使用范围**：仅限兼容的 AI 编程与智能体工具交互式使用，不可用于自动化脚本或应用后端，违规可能暂停订阅或封禁 API Key。
- **数据安全**：承诺不使用对话数据训练模型，传输采用 HTTPS 加密，多租户隔离。
- **退订**：支持按席位退订，已有用量消耗的席位不可退订；退款原路退回，预计 1-3 个工作日到账。
- **账号欠费**：预付费订阅，账号欠费不影响套餐正常使用（只要额度未用尽且订阅有效）。

## Coding Plan

### 套餐详情

Pro 高级套餐 ¥200/月，用量限制：每 5 小时 6,000 次请求、每周 45,000 次、每月 90,000 次。单次提问按"模型调用次数"扣除额度，简单任务约 5-10 次，复杂任务约 10-30+ 次。

**额度恢复**：每 5 小时额度滚动恢复（每分钟释放 5 小时前的额度）；每周额度每周一 00:00（UTC+8）重置；每月额度在下一个月订阅日 00:00（UTC+8）重置。

### 支持的模型（Pro 套餐）

推荐模型：`qwen3.7-plus`、`qwen3.6-plus`（图片理解）、`kimi-k2.5`（图片理解）、`glm-5`、`MiniMax-M2.5`。更多模型：`qwen3.5-plus`（图片理解）、`qwen3-max-2026-01-23`、`qwen3-coder-next`、`qwen3-coder-plus`、`glm-4.7`。模型 ID 区分大小写，需与套餐支持列表精确匹配，详见 [Coding Plan概述](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)。

### 订阅前须知

- **不支持退款**。
- **严禁 API 调用**：仅限编程工具交互式使用，违规格可能导致订阅暂停或 API Key 封禁。
- **数据授权**：使用期间模型输入及生成内容用于服务改进与模型优化；停止使用可终止后续授权，已授权数据不在范围内。
- **账号专享**：禁止共享，共享可能导致权益受限。

## 工具调用能力

### 模型内置工具

Token Plan 团队版的 `qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-plus`、`qwen3.6-flash` 通过 Responses API 内置联网搜索、代码解释器、网页抓取、以图搜图、文搜图五种工具，启用后模型自动调用。内置工具不额外收费，token 消耗从 Credits 抵扣。

### MCP 服务接入

其他模型可通过百炼 MCP 广场接入工具能力。**联网搜索 MCP** 已从旧版 SSE 协议升级为 Streamable HTTP 协议，连接地址 `https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp`。全部用户前 2000 次调用免费，之后按 29 元/千次计费。

> **注意**：MCP 服务鉴权使用**百炼通用 API Key（`sk-xxx`）**，与 Token Plan/Coding Plan 专属 API Key（`sk-sp-xxx`）不同，两者不可混用。

各工具接入命令示例（`YOUR_API_KEY` 替换为百炼通用 API Key）：

- Claude Code：`claude mcp add WebSearch https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp -t http -H "Authorization: Bearer YOUR_API_KEY"`，随后在对话框执行 `/mcp` 确认状态为 connected。
- Qwen Code：`qwen mcp add WebSearch -t http "https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp" -H "Authorization: Bearer YOUR_API_KEY"`。
- OpenCode / Kilo CLI：在 `opencode.json` 配置文件 `mcp` 字段写入 remote 类型配置。
- OpenClaw：通过 `mcporter` 安装并 `openclaw gateway restart` 生效。

详见 [工具调用](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-tool.md)。

## 多模态与视觉能力

### 图像生成

Token Plan 团队版支持 `qwen-image-2.0`、`qwen-image-2.0-pro`、`wan2.7-image`、`wan2.7-image-pro` 等图像生成模型，使用独立接口，需通过工具的扩展机制（Skill、Slash Command 或 Agent）接入。例如 Claude Code 在 `.claude/commands/text-to-image.md` 创建 Slash Command，通过 Bash 调用 `https://token-plan.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation` 生成图片。详见 [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)。

### 视觉理解

Coding Plan 中 `qwen3.6-plus`、`qwen3.5-plus`、`kimi-k2.5` 原生支持视觉理解，可直接处理图片输入。`glm-5`、`MiniMax-M2.5` 等纯文本模型可通过添加本地 Skill（如 Claude Code 的 `.claude/skills/image-analyzer/SKILL.md`）或 Agent（OpenCode 的 `.opencode/agents/image-analyzer.md`）调用视觉模型间接获得能力。

> **注意**：OpenCode 与 OpenClaw 默认不启用模型视觉能力，需在配置文件中显式声明 `modalities.input: ["text", "image"]`（OpenCode）或 `input: ["text", "image"]`（OpenClaw）。OpenClaw 修改后需清除模型缓存 `rm ~/.openclaw/agents/main/agent/models.json` 并 `openclaw gateway restart`。

## 思考模式

Coding Plan 支持深度思考的模型多为默认支持思考模式。各模型最大思维链长度（`budgetTokens` 上限）不同，超限会触发 `invalid_parameter_error: The thinking_budget parameter must be a positive integer and not greater than xxxxx`。示例上限：

| 模型 | 最大思维链长度 |
| --- | --- |
| qwen3.7-plus | 262,144 |
| qwen3.6-plus / qwen3.5-plus / qwen3-max-2026-01-23 / kimi-k2.5 | 81,920 |
| glm-5 / glm-4.7 | 32,768 |
| MiniMax-M2.5 | 默认启用，无需配置 |
| qwen3-coder-next / qwen3-coder-plus | 不支持思考模式 |

开启方式：Claude Code 输入 `/config` 切换 `Thinking mode`；Qwen Code 在 `~/.qwen/settings.json` 设置 `enable_thinking: true`；OpenCode 配置 `options.thinking.budgetTokens`。

## 常见报错排查

| 报错 | 原因 | 解决方案 |
| --- | --- | --- |
| `401 InvalidApiKey: No API-key provided` | 请求头未携带 API Key | 在管理后台生成并在工具中配置 |
| `401 InvalidApiKey: Invalid API-key provided` | 误用通用/Coding Plan Key、订阅过期、Key 复制不完整 | 确认专属 API Key 完整无空格，必要时重置 |
| `404 model 'xxx' not found` / `400 Model not exist` | 模型名拼写错误或不在套餐支持列表 | 核对精确模型 ID，区分大小写 |
| `401 invalid access token` / `Incorrect API key` | 误用其他套餐 Base URL 或通用 Base URL | 使用对应套餐的专属端点 |
| `400 InvalidParameter: Range of input length` | 输入超出上下文长度 | 新建会话、`/compact`、切换长上下文模型 |
| `400 InvalidParameter: Range of max_tokens` | `max_tokens` 超出模型上限 | 调整为报错提示的上限值 |
| `400 InvalidParameter: url error` | Base URL 与协议不匹配 | 按协议选择对应端点 |
| `429 API-Key Requests rate limit` | 请求过密触发限流 | 等待重试，降低频率 |
| `429 Throttling.AllocationQuota` / `insufficient_quota` | 套餐额度用尽 | 加购共享用量包/坐席，或等待重置 |
| `hour/week/month allocated quota exceeded`（Coding Plan） | 对应周期额度用完 | 等待额度恢复 |
| `concurrency allocated quota exceeded`（Coding Plan） | 并发超限 | 等待片刻重试 |
| `400 data_inspection_failed` | 命中内容安全策略 | 修改输入内容 |

详见 [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-faq.md) 与 [Coding Plan 常见问题](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan-faq.md)。

### Claude Code 初始化报错

首次启动时若报 `Unable to connect to Anthropic services. Failed to connect to api.anthropic.com`，原因是 Claude Code 在部分国家/地区不可用。在 `~/.claude.json` 添加顶层字段 `"hasCompletedOnboarding": true` 后重启即可（可用 Qwen Code 自动添加）。

### OpenCode Request Entity Too Large

请求内容过大。执行 `/new` 或 `/compact`；若无效，升级 OpenCode 至 1.2.16 或以上版本。

## 来源文档

- [Token Plan（团队版）概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)
- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-quickstart.md)
- [团队管理](../../raw/model-user-guide/token-plan-guide/token-plan-team.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-faq.md)
- [工具调用](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-tool.md)
- [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)
- [Coding Plan概述](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)
- [联网搜索](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/web-search-for-coding-plan.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan-faq.md)
- [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/add-vision-skill.md)


