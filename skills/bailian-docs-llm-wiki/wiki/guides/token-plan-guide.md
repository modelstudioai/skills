# token plan guide

阿里云百炼提供两类面向 AI 编程与智能体工具的订阅式套餐：**[Token](../concepts/token.md) Plan（团队版）** 与 **Coding Plan（个人版）**。两者均整合千问、GLM、Kimi、MiniMax 等模型，兼容 Claude Code、OpenCode、Cursor、Qwen Code 等主流编程工具，但计量方式、使用范围和管理粒度不同。本文汇总订阅、接入、团队管理、工具调用、[多模态](../concepts/multimodal.md)与常见报错的核心信息。

## 两类套餐对比

[Token](../concepts/token.md) Plan（团队版）与 Coding Plan 的关键差异如下，详见 [Token Plan（团队版）概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md) 与 [Coding Plan概述](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)。

| 维度 | [Token](../concepts/token.md) Plan（团队版） | Coding Plan |
| --- | --- | --- |
| 适用场景 | 团队/企业日常办公 | 个人开发场景 |
| 支持模型 | 文本生成 + 图像生成模型 | 仅文本生成模型 |
| [计费](../concepts/billing.md)方式 | 按 Token 消耗抵扣 Credits | 按模型调用次数 |
| 使用频次 | 无每 5 小时/每周限额 | 每 5 小时/每周/每月限额 |
| 高峰期性能 | 多租户隔离，不排队 | 高峰期间可能排队 |
| 数据安全 | 承诺不使用对话数据训练模型 | 使用期间数据用于服务改进与模型优化 |
| [API Key](../concepts/api-key.md) 格式 | `sk-sp-xxx`（专属） | `sk-sp-xxx`（专属） |
| 服务地域 | 仅华北2（北京） | 不限制地域，海外可用国际站 |

> **注意**：Token Plan 团队版、Coding Plan 与百炼按量[计费](../concepts/billing.md)三者的 [API Key](../concepts/api-key.md) 和 Base URL 互不相通，混用会导致额度不抵扣或额外扣费。

## 支持的模型

### Token Plan 团队版

模型 ID 为精确字符串白名单，必须逐字符完全匹配，禁止做版本兼容推理。仅支持以下精确版本：

- **千问**：qwen3.7-max（限时 Credits 减半）、qwen3.7-plus、qwen3.6-plus、qwen3.6-flash、qwen-image-2.0、qwen-image-2.0-pro
- **万相**：wan2.7-image、wan2.7-image-pro
- **DeepSeek**：deepseek-v4-pro、deepseek-v4-flash、deepseek-v3.2
- **月之暗面**：kimi-k2.7-code、kimi-k2.6、kimi-k2.5
- **智谱 AI**：glm-5.2、glm-5.1、glm-5
- **MiniMax**：MiniMax-M2.5

### Coding Plan

推荐模型：qwen3.7-plus、qwen3.6-plus、kimi-k2.5、glm-5、MiniMax-M2.5；更多模型含 qwen3.5-plus、qwen3-max-2026-01-23、qwen3-coder-next、qwen3-coder-plus、glm-4.7。Lite 套餐自 2026 年 3 月 20 日起停止新购，4 月 13 日起停止续费与升级，已购用户可用至到期。

> **注意**：Coding Plan 与 Token Plan 团队版的模型清单不完全一致（如 Coding Plan 不包含图像生成模型和 deepseek 系列），接入前请以各自套餐的支持列表为准。

## 套餐与定价

### Token Plan 团队版

提供三档坐席（席位是订阅最小单位，每席位绑定一个成员、对应一个 [API Key](../concepts/api-key.md)，不可共享）：

| 坐席类型 | 价格 | 月度额度 | 适用场景 |
| --- | --- | --- | --- |
| 标准坐席 | ¥198/月 | 25,000 Credits | 轻度使用 |
| 高级坐席 | ¥698/月 | 100,000 Credits | 日常高频使用 |
| 尊享坐席 | ¥1,398/月 | 250,000 Credits | 重度依赖 AI |

共享用量包为跨坐席弹性用量包：¥5,000/个，625,000 Credits/个，有效期 1 个月，到期清零，持有多个时优先抵扣最近到期的。每个阿里云账号限购一个订阅，共享用量包单次最多 1000 个，且需先订阅坐席后才能购买。

### Coding Plan

Pro 高级套餐 ¥200/月，用量限制为每 5 小时 6,000 次请求、每周 45,000 次、每月 90,000 次。单次提问按实际模型调用次数扣除额度，简单任务约 5–10 次，复杂任务约 10–30+ 次。

> **注意**：Coding Plan 服务**不支持退款**，订阅前务必知悉使用范围与数据授权条款。

## Credits [计费](../concepts/billing.md)与额度（Token Plan 团队版）

单次消耗的 Credits 由模型类型、Token 用量、思考模式及工具调用动态决定，实际以账单为准。抵扣顺序为：坐席月度额度 → 共享用量包 → 全部用尽则暂停至下一计费周期。

坐席额度在每个订阅月到期时重置，未用完不累积；共享用量包额度按月重置。续费仅延长有效期，不会立即增加当月额度——若当月已用尽，需购买共享用量包、升级坐席或等待重置。

## 接入流程

### 步骤一：订阅套餐

- Token Plan 团队版：访问购买页选择坐席类型/数量/订阅周期，主账号和 RAM 账号均可订阅。
- Coding Plan：RAM 子账号需先由主账号在百炼权限管理页添加用户并授予管理员权限后再订阅。

### 步骤二：获取 API Key 与 Base URL

两套套餐均使用 `sk-sp-` 开头的专属 API Key，Base URL 按协议选择：

**Token Plan 团队版 Base URL**：

- OpenAI 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
- Anthropic 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`

**Coding Plan Base URL**：

- OpenAI 兼容：`https://coding.dashscope.aliyuncs.com/v1`
- Anthropic 兼容：`https://coding.dashscope.aliyuncs.com/apps/anthropic`
- 海外：`https://coding-intl.dashscope.aliyuncs.com/...`

> **注意**：Base URL 路径必须与工具协议匹配。Anthropic 兼容协议（Claude Code 等）以 `/apps/anthropic` 结尾；OpenAI 兼容协议（Cursor、Qwen Code 等）以 `/compatible-mode/v1` 或 `/v1` 结尾。混用会触发 `400 InvalidParameter: url error` 或 `404 status code (no body)`。

### 步骤三：接入 AI 工具

兼容工具包括 OpenClaw、Hermes Agent、Claude Code、OpenCode、Cursor、Codex、Qwen Code、QwenPaw、Cherry Studio、Chatbox、Cline、Qoder、Lingma、Kilo CLI 等。具体接入文档参见 [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-quickstart.md)。

## 团队管理（仅 Token Plan 团队版）

详见 [团队管理](../../raw/model-user-guide/token-plan-guide/token-plan-team.md)。角色分为拥有者、管理员、成员三种：拥有者和管理员可管理成员与席位、查看全部用量；成员仅能使用分配的 API Key 调用模型。

成员添加方式：

- **手动添加**：填用户名（仅字母/数字/下划线）和角色，分配席位后系统自动生成 API Key。该类成员不能登录管理平台，仅供 API 调用。
- **SSO 或钉钉登录**：成员可登录管理平台自管席位和 API Key。SSO 通过标准 SAML 2.0 对接企业 IdP（如阿里云 IDaaS），钉钉需创建企业内部应用并配置回调域名 `https://account-enterprise.bailian.aliyunportal.com/api/v1/auth/dingtalk/callback` 与通讯录读权限。

席位操作支持分配、回收、加购（与现有订阅统一到期，按剩余时长折算）、升级（按剩余时长补缴差价，支持批量）。每个成员同一时间只能持有一个席位。用量分析（近 1/7/30 天 Credits 趋势、模型用量、成员用量）仅在管理平台提供。

## 工具调用

Token Plan 团队版提供两种工具接入方式，详见 [工具调用](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-tool.md)：

- **模型内置工具**：qwen3.7-max、qwen3.7-plus、qwen3.6-plus、qwen3.6-flash 的 Responses API 内置联网搜索、代码解释器、网页抓取、以图搜图、文搜图 5 个工具，启用后自动调用，不额外收费，token 消耗从 Credits 抵扣。
- **MCP 服务**：其他模型（deepseek-v3.2、glm-5 等）通过百炼 MCP 广场接入。联网搜索 MCP 全部用户前 2000 次免费，用尽后 29 元/千次。

> **注意**：调用 MCP 服务使用的是**百炼通用 API Key**（`sk-xxx`），与套餐专属 API Key（`sk-sp-xxx`）不同，需单独获取。

### 联网搜索 MCP 接入

联网搜索 MCP 已升级为 Streamable HTTP 协议，连接地址 `https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp`。已开通旧版 SSE 协议的用户需在 MCP 广场取消开通后重新开通升级。各工具接入命令示例（`YOUR_API_KEY` 替换为百炼通用 API Key）：

- Claude Code：`claude mcp add WebSearch https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp -t http -H "Authorization: Bearer YOUR_API_KEY"`
- Qwen Code：`qwen mcp add WebSearch -t http "https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp" -H "Authorization: Bearer YOUR_API_KEY"`
- OpenCode / Kilo CLI：在 `opencode.json` 的 `mcp` 字段写入 `WebSearch` 远程配置
- OpenClaw：安装 MCPorter 后用 `mcporter config add` 添加并 `openclaw gateway restart`

接入后在对话框执行 `/mcp` 或 `/mcps` 确认状态为 connected/Enabled，再提问 `用 websearch MCP 搜索阿里云的新闻` 验证。Cursor 等已内置联网搜索的工具无需额外添加。

## [多模态](../concepts/multimodal.md)能力

### 图像生成（Token Plan 团队版）

图像生成模型（qwen-image-2.0、wan2.7-image 等）使用独立接口，无法通过文本模型 Base URL 直接调用，需通过工具扩展机制（Skill、Slash Command 或 Agent）接入。以 Claude Code 为例，在 `.claude/commands/text-to-image.md` 创建 Slash Command，调用 `https://token-plan.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation` 文生图接口。其他工具的扩展机制与配置路径见 [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)。

### 视觉理解（Coding Plan）

详见 [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/add-vision-skill.md)。qwen3.6-plus、qwen3.5-plus、kimi-k2.5 原生支持视觉，直接传入图片即可；glm-5、MiniMax-M2.5 等纯文本模型需通过 Skill/Agent 辅助（如 Claude Code 的 `.claude/skills/image-analyzer/SKILL.md`，OpenCode 的 `.opencode/agents/image-analyzer.md`），在 Skill/Agent 中指定具备视觉的模型处理图片。

> **注意**：OpenCode 默认不启用模型视觉能力，需在模型定义中显式添加 `modalities.input: ["text","image"]`；OpenClaw 需在模型定义中包含 `"input": ["text","image"]` 并清除模型缓存重启。运行图片理解 Skill 会消耗 Coding Plan 额度。

## 思考模式

Coding Plan 中支持深度思考的模型多为默认支持。各工具开启方式：

- Claude Code：`/config` → Thinking mode → Enter 切换为 true，`Ctrl+O` 查看思考过程
- OpenCode：配置 `options.thinking: { type: "enabled", budgetTokens: 1024 }`
- Qwen Code：在 `~/.qwen/settings.json` 的 `modelProviders` 中设置 `extra_body.enable_thinking: true`

`budgetTokens` 上限因模型而异（qwen3.7-plus 262,144；qwen3.6-plus/qwen3.5-plus/qwen3-max-2026-01-23/kimi-k2.5 81,920；glm-5/glm-4.7 32,768），超出会触发 `thinking_budget parameter must be a positive integer and not greater than xxxxx`。qwen3-coder-next、qwen3-coder-plus 不支持思考模式，需移除该配置项。

## 限制与注意事项

- **使用范围**：两类套餐均仅限在兼容的 AI 编程/智能体工具中**交互式**使用，禁止用于自动化脚本或应用后端。违规可能导致订阅暂停或 API Key 封禁。
- **账号规范**：API Key 限已分配席位的成员本人使用，不可共享。Coding Plan 禁止账号共享。
- **退订**：Token Plan 团队版支持按席位退订（已有用量消耗的席位不可退订，退款 1-3 个工作日到账）；Coding Plan 不支持退款。
- **欠费**：Token Plan 团队版为预付费，阿里云账号欠费不影响套餐使用（只要额度未用尽且在有效期内）。
- **海外**：Coding Plan 不限制地域；Token Plan 团队版仅华北2（北京），海外调用需符合当地法规。

## 常见报错速查

| 报错 | 可能原因 | 解决方案 |
| --- | --- | --- |
| `401 InvalidApiKey` | 未传 API Key / 误用通用 Key / 订阅过期 / Key 不完整 | 使用专属 API Key，确认完整无空格，必要时重置 |
| `model 'xxx' is not supported` / `400 Model not exist` | 模型名拼写错误或不在套餐支持列表 | 严格按支持列表的精确 ID，区分大小写 |
| `401 invalid access token` / `403 invalid api-key` / `401 Incorrect API key` | 误用其他套餐的 Base URL 或通用 Base URL | 按工具协议选择对应套餐专属端点 |
| `400 InvalidParameter: url error` / `404 status code (no body)` | Base URL 路径与协议不匹配 | Anthropic 用 `/apps/anthropic`，OpenAI 用 `/compatible-mode/v1` 或 `/v1` |
| `400 Range of input length should be [1, xxx]` | 输入超出最大上下文 | 新建会话、`/compact`、`/clear` 或切换更长上下文模型 |
| `400 Range of max_tokens should be [1, xxxx]` | max_tokens 超出模型上限 | 调整为报错提示的上限值 |
| `thinking_budget parameter must be...` | budgetTokens 超过模型上限 | 按模型上限调整或移除配置 |
| `429 API-Key Requests rate limit` | 请求过于密集 | 等待重试，降低频率 |
| `429 Throttling.AllocationQuota` / `insufficient_quota` | 套餐额度用尽 | 加购坐席/共享用量包或等待重置 |
| `hour/week/month allocated quota exceeded`（Coding Plan） | 5 小时/周/月额度用完 | 等待对应周期自动恢复 |
| `concurrency allocated quota exceeded`（Coding Plan） | 并发超限 | 等待片刻重试 |
| `data_inspection_failed` | 命中内容安全策略 | 修改输入内容 |
| `Connection error` | Base URL 拼写错误或网络异常 | 检查域名与网络 |

更多问题可使用 [阿里云 AI 助理](https://www.aliyun.com/ai-assistant/) 查询，其[知识库](../concepts/knowledge-base.md)整合了官方帮助文档。

## 来源文档

- [Token Plan（团队版）概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)
- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-quickstart.md)
- [团队管理](../../raw/model-user-guide/token-plan-guide/token-plan-team.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-faq.md)
- [工具调用](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-tool.md)
- [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)
- [Coding Plan概述](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)
- [联网搜索](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/web-search-for-coding-plan.md)
- [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/add-vision-skill.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan-faq.md)



