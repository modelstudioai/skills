# token plan guide

阿里云百炼提供两类面向 AI 编程与办公场景的订阅套餐：**Token Plan 团队版**与 **Coding Plan**。两者均以固定月费替代按量计费，兼容主流 AI 编程工具与智能体工具，但定位、计量方式与适用对象不同。本主题页系统梳理两类套餐的产品形态、模型与定价、接入流程、团队管理、扩展能力（工具调用、多模态生成、视觉理解、联网搜索）以及常见报错排查。

## 套餐总览与差异

| 对比项 | Token Plan 团队版 | Coding Plan |
| --- | --- | --- |
| 适用场景 | 一人公司/团队/企业日常办公 | 个人开发场景 |
| 支持模型 | 文本生成、图像生成模型 | 文本生成模型 |
| 计费方式 | 按 Token 消耗抵扣 Credits | 按模型调用次数 |
| 使用限额 | 无每 5 小时/每周限额 | 每 5 小时/每周/每月限额 |
| 高峰期性能 | 多租户隔离，不排队 | 高峰期可能排队 |
| 数据安全 | 承诺不使用数据训练模型 | 用户数据授权用于服务改进 |
| API Key 格式 | Token Plan 专属（`sk-sp-xxx`） | Coding Plan 专属（`sk-sp-xxx`） |
| 多人使用 | 支持团队席位分配 | 仅限个人，禁止共享 |

**关键约束**：两类套餐的 API Key 与 Base URL 互不相通，也不可与百炼按量计费通用凭证（`sk-xxx` / `dashscope.aliyuncs.com`）混用。误用其他凭证不会抵扣套餐额度，并可能产生额外扣费。两类套餐均**仅限在兼容的 AI 编程和智能体工具中交互式使用**，禁止用于自动化脚本、应用后端或非交互式批量调用（curl、Postman、Dify 等），违规可能导致订阅暂停或 API Key 封禁。

## Token Plan 团队版

### 产品定位

Token Plan 团队版以 **Credits** 统一计量，支持千问、万相、DeepSeek、月之暗面、智谱 AI、MiniMax 等多品牌模型，覆盖文本生成与图像生成。提供团队管理后台、席位分配与回收、成员用量分析等能力，承诺不使用对话数据训练模型，基于多租户隔离架构保障调用高峰期间不排队。目前仅支持**华北2（北京）**地域。

### 套餐与定价

席位（坐席）是最小订阅单位，每个席位绑定一个成员、对应一个 API Key，不可共享。三档坐席匹配不同使用强度：

| 坐席类型 | 价格 | 月度额度 | 适用场景 |
| --- | --- | --- | --- |
| 标准坐席 | ¥198/坐席/月 | 25,000 Credits | 轻度使用 AI 辅助的成员 |
| 高级坐席 | ¥698/坐席/月 | 100,000 Credits | 日常高频 AI 编程或办公 |
| 尊享坐席 | ¥1,398/坐席/月 | 250,000 Credits | 重度依赖 AI 的核心开发者 |

**共享用量包**：跨坐席共享的弹性用量包，单档 ¥5,000/个，含 625,000 Credits，有效期 1 个月，到期清零。持有多个时优先抵扣最近到期的用量包。共享用量包不可单独购买，需先订阅坐席套餐。每个阿里云账号限购一个订阅，同一订阅下每种坐席可购买多个，共享用量包单次最多 1000 个。

**限时活动**：即日起至 2026 年 7 月 22 日 23:59（UTC+8），qwen3.7-max 模型 Credits 消耗减半，并支持隐式缓存。

### Credits 计费机制

单次消耗的 Credits 由模型类型、Token 用量（输入/缓存/输出）、思考模式及工具调用动态决定，实际以账单为准。以 qwen3.6-plus 为例，单次请求约消耗 3.18 Credits（输入 8349 tokens 1.67 + 缓存 40794 tokens 0.82 + 输出 573 tokens 0.69）。

**抵扣顺序**：
1. 优先从坐席月度额度抵扣；
2. 坐席额度用尽后从共享用量包抵扣（多个用量包优先抵扣最近到期的）；
3. 全部额度用尽后服务暂停，至下一计费周期或购买共享用量包补充额度。

坐席额度在每个订阅月到期时重置，未用完不累积；共享用量包同样按月重置。续费仅延长订阅有效期，不立即增加当月额度。

### 支持的模型

模型 ID 为精确字符串白名单，必须逐字符完全匹配，禁止版本兼容推理。支持千问（qwen3.7-max、qwen3.7-plus、qwen3.6-plus、qwen3.6-flash、qwen-image-2.0、qwen-image-2.0-pro）、万相（wan2.7-image、wan2.7-image-pro）、DeepSeek（deepseek-v4-pro、deepseek-v4-flash、deepseek-v3.2）、月之暗面（kimi-k2.7-code、kimi-k2.6、kimi-k2.5）、智谱 AI（glm-5.2、glm-5.1、glm-5）、MiniMax（MiniMax-M2.5）。其中 qwen3.7-plus、qwen3.6-plus、qwen3.6-flash 等具备推理与视觉理解能力，qwen-image 与 wan2.7 系列为图像生成模型。

### 订阅管理

在 Token Plan 控制台「我的订阅」页面管理：
- **加购席位**：新加席位与现有订阅统一到期，费用按剩余时长折算；
- **升级席位**：按差价补缴费用，支持批量升级；
- **退订席位**：按席位维度退订，已有用量消耗的席位不可退订，退款原路退回，1-3 个工作日到账；
- **续费/自动续费**：续费周期与订阅时一致；自动续费次日生效，到期前 9 天按订阅周期自动扣款；
- **加购共享用量包**：在「共享用量包」区域加购。

阿里云账号欠费不影响 Token Plan 使用（预付费订阅产品，只要额度未用尽且订阅有效）。

### 团队管理

**访问入口**：阿里云主账号或 RAM 用户登录 Token Plan 控制台；RAM 用户需由主账号在百炼「账号管理」页面分配**管理员**或**订阅套餐**权限。通过 SSO 或钉钉加入的成员使用管理员分发的**管理平台地址**登录独立管理平台。

**角色与权限**：
- **拥有者**：添加/移除成员、分配/回收席位、修改角色、查看全部用量；
- **管理员**：权限范围与拥有者相同，由拥有者授予，可被移除或降级；
- **成员**：使用分配的 API Key 和 Base URL 调用模型。

**成员管理**：
- **手动添加**：填用户名（英文字母、数字、下划线）和角色，分配席位后系统自动生成 API Key；此类成员不能登录管理平台，仅供 API 调用。
- **SSO/钉钉登录**：成员可登录管理平台自管席位和 API Key，登录即自动加入组织。

**席位操作**：分配席位后自动生成 API Key；回收席位后原成员 API Key 立即失效，席位转为未分配可重新分配（生成新 API Key）；每个成员同一时间只能持有一个席位，更换需先回收再分配。席位到期后 API Key 无法调用，续订并重新分配后恢复。

**身份接入**：
- **SAML 接入**：通过标准 SAML 2.0 对接企业 IdP。在控制台「设置 > SSO 配置」填入自定义 SP Entity ID 及 IdP 信息（IdP Entity ID、IdP SSO URL、IdP Certificate），保存后系统生成 ACS URL，再将 SP Entity ID 和 ACS URL 填入企业 IdP。组织内有成员时无法编辑 SSO 配置，需先全部移出。阿里云 IDaaS 可作为示例 IdP。
- **钉钉接入**：创建钉钉企业内部应用，获取 Client ID/Client Secret，配置回调域名为 `https://account-enterprise.bailian.aliyunportal.com/api/v1/auth/dingtalk/callback`，开通通讯录读权限并发布应用；在管理平台「SSO 配置 > 钉钉」填入 AppKey/AppSecret。

**用量分析**：仅在管理平台提供，可查看近 1/7/30 天 Credits 消耗趋势、各模型用量、各成员消耗明细。

## Coding Plan

### 产品定位

Coding Plan 整合千问、GLM、Kimi、MiniMax 等模型，兼容主流 AI 编程工具，按模型调用次数计费，折算成本远低于常规 API 调用。仅支持文本生成模型，仅限个人使用，禁止共享。

### 套餐详情

**Pro 高级套餐**：¥200/月。
- 用量限制：每 5 小时 6,000 次请求、每周 45,000 次、每月 90,000 次。
- 额度恢复：每 5 小时额度滚动恢复（每分钟释放 5 小时前的额度）；每周一 00:00（UTC+8）重置；每月在下个订阅日 00:00 重置。
- 推荐模型：qwen3.7-plus、qwen3.6-plus、kimi-k2.5（均支持图片理解）、glm-5、MiniMax-M2.5；更多模型含 qwen3.5-plus、qwen3-max-2026-01-23、qwen3-coder-next、qwen3-coder-plus、glm-4.7。

**Lite 套餐**：自 2026 年 3 月 20 日起停止新购，4 月 13 日起停止续费与升级。已购买用户可继续使用至到期，支持套餐内全部模型。

Coding Plan 不支持退款，仅支持按月订阅，无年付套餐。每个百炼账号同时只能订阅一个 Coding Plan。Pro 不可降级到 Lite。额度用完后继续调用会失败，不会自动转按量计费，也不参与百炼通用模型免费试用。

### 上下文长度与思考模式

各模型上下文长度：qwen3.7-plus / qwen3.6-plus / qwen3.5-plus / qwen3-coder-plus 为 1,000,000；kimi-k2.5、qwen3-max-2026-01-23、qwen3-coder-next 为 262,144；glm-5 / glm-4.7 为 202,752；MiniMax-M2.5 为 196,608。超出上下文建议新建会话、切换更长上下文模型、减少无关文件、拆分任务或使用精确指令。

思考模式最大思维链长度：qwen3.7-plus 262,144；qwen3.6-plus / qwen3.5-plus / qwen3-max-2026-01-23 / kimi-k2.5 81,920；glm-5 / glm-4.7 32,768；MiniMax-M2.5 默认启用；qwen3-coder-next / qwen3-coder-plus 不支持思考模式。

## 快速开始（接入流程）

两类套餐接入三步走：订阅 → 获取 API Key 和 Base URL → 配置 AI 工具。

### 步骤一：订阅

访问对应购买页（Token Plan 团队版购买页 / Coding Plan 购买页）选择套餐并完成订阅。主账号可直接订阅；RAM 子账号需先由主账号在工作空间「权限管理」页面添加用户并授予**管理员**权限后方可订阅。

### 步骤二：获取 API Key 和 Base URL

**Token Plan 团队版**：在控制台「成员管理」页面创建成员并分配席位后，系统为成员生成专属 API Key。Base URL 按协议选择：
- OpenAI 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
- Anthropic 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`

**Coding Plan**：在 Coding Plan 页面获取专属 API Key（`sk-sp-xxx`）。Base URL：
- OpenAI 兼容：`https://coding.dashscope.aliyuncs.com/v1`
- Anthropic 兼容：`https://coding.dashscope.aliyuncs.com/apps/anthropic`
- 海外用户国际站：`https://coding-intl.dashscope.aliyuncs.com/...`

### 步骤三：接入 AI 工具

兼容工具包括 OpenClaw、Hermes Agent、Claude Code、OpenCode、Cursor、Codex、Qwen Code、QwenPaw、Cherry Studio、Chatbox、Cline、Qoder、Lingma、Kilo CLI 等。Base URL 路径必须与工具使用的协议匹配：Anthropic 兼容协议（Claude Code 等）以 `/apps/anthropic` 结尾；OpenAI 兼容协议（Cursor、Qwen Code 等）以 `/compatible-mode/v1` 或 `/v1` 结尾。

## 扩展能力

### 工具调用

Token Plan 团队版提供两种工具接入方式：
- **模型内置工具**：qwen3.7-max、qwen3.7-plus、qwen3.6-plus、qwen3.6-flash 的 Responses API 内置联网搜索、代码解释器、网页抓取、以图搜图、文搜图五种工具，启用后自动调用，不额外收费，token 消耗从 Credits 抵扣。
- **MCP 服务**：其他模型（deepseek-v3.2、glm-5 等）通过百炼 MCP 广场接入。MCP 服务调用使用百炼通用 API Key（`sk-xxx`），与套餐专属 Key 不同。联网搜索 MCP 前 2000 次免费，之后 29 元/千次。

### 联网搜索 MCP

联网搜索 MCP 已升级为 Streamable HTTP 协议，连接地址 `https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp`。在百炼 MCP 广场开通后，将 Endpoint 与百炼 API Key 配置到编程工具：
- **Claude Code**：`claude mcp add WebSearch <endpoint> -t http -H "Authorization: Bearer YOUR_API_KEY"`，进入后用 `/mcp` 确认状态为 connected。
- **Qwen Code**：`qwen mcp add WebSearch -t http <endpoint> -H "Authorization: Bearer YOUR_API_KEY"`。
- **OpenCode / Kilo CLI**：在配置文件 `opencode.json` 的 `mcp` 字段写入 remote 配置。
- **Kilo Code IDE 插件**：在 `mcpServers` 中配置 `streamable-http` 类型。
- **OpenClaw**：通过 MCPorter 安装并启用，重启 gateway 生效。

旧版 SSE 协议（`/sse` 结尾）需在 MCP 广场取消开通后重新开通以升级。提问时建议明确提及 `websearch MCP` 以避免工具混淆。

### 接入多模态生成模型

图像生成模型（qwen-image-2.0、wan2.7-image 等）使用独立接口，无法通过文本模型 Base URL 直接调用，需通过工具的扩展机制（Skill、Slash Command 或 Agent）接入。以 Claude Code 为例，在项目根目录创建 `.claude/commands/text-to-image.md`，调用文生图 API `https://token-plan.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`，从返回 JSON 的 `output.choices[*].message.content[*].image` 提取图片 URL 下载。其他工具按各自扩展机制和配置路径配置（Codex/Qwen Code/OpenClaw/Hermes Agent 用 Skill，OpenCode 用 Agent），Skill 类工具需在文件开头添加 YAML front matter。

### 添加视觉理解能力

Coding Plan 中 qwen3.6-plus、qwen3.5-plus、kimi-k2.5 原生支持视觉，可直接传入图片，推荐直接切换到这些模型。对 glm-5、MiniMax-M2.5 等纯文本模型，可通过本地 Skill/Agent 辅助获得视觉能力：
- **Claude Code**：在 `.claude/skills/image-analyzer/SKILL.md` 中配置 `model: qwen3.6-plus`，主对话用 `/model glm-5`，提问时加载 [skill](skill.md)。
- **OpenCode**：在 `.opencode/agents/image-analyzer.md` 中配置 `model: bailian-coding-plan/qwen3.6-plus`、`mode: subagent`。

OpenCode 默认不启用模型视觉能力，需在配置文件模型定义中显式声明 `modalities.input` 为 `["text", "image"]`；OpenClaw 需在模型配置中添加 `"input": ["text", "image"]` 并清除模型缓存重启。

## 常见报错与排查

### 鉴权类

| 报错 | 原因 | 解决方案 |
| --- | --- | --- |
| `401 InvalidApiKey: No API-key provided` | 请求头未携带 API Key | 在管理后台生成并在工具中配置 |
| `401 InvalidApiKey: Invalid API-key provided` | 误用通用/Coding Plan Key、订阅过期、复制不完整 | 确认专属 Key 完整无空格、订阅有效，必要时重置 |
| `401 invalid access token or token expired` / `401 Incorrect API key` | 误用其他套餐或通用 Base URL | 改用对应套餐专属端点 |
| `403 invalid api-key` / `404 status code (no body)` | Base URL 路径与协议不匹配 | Anthropic 协议用 `/apps/anthropic`，OpenAI 协议用 `/v1` 或 `/compatible-mode/v1` |

### 模型与参数类

| 报错 | 原因 | 解决方案 |
| --- | --- | --- |
| `404 model 'xxx' not found` / `400 Model not exist` / `model 'xxx' is not supported` | 模型名拼写错误、大小写错误、不在套餐支持列表 | 模型 ID 区分大小写，与套餐支持列表逐字符匹配 |
| `400 Range of input length should be [1, xxx]` | 输入超出最大上下文 | 新建会话、`/compact`、切换更长上下文模型 |
| `400 Range of max_tokens should be [1, xxxx]` | max_tokens 超过模型上限 | 调整为不超过报错上限 |
| `400 thinking_budget parameter must be a positive integer and not greater than xxxxx` | 思维链长度超模型上限 | 调整 budgetTokens，不支持思考模式的模型移除配置 |
| `400 data_inspection_failed` | 命中内容安全策略 | 修改输入内容，调整提示词 |
| `Request Entity Too Large`（OpenCode） | 请求内容过大 | `/new` 或 `/compact`，升级到 1.2.16+ |

### 限流与额度类

| 报错 | 原因 | 解决方案 |
| --- | --- | --- |
| `429 API-Key Requests rate limit exceeded` | 请求过于密集 | 等待一分钟后重试，降低频率 |
| `429 Throttling.AllocationQuota` / `insufficient_quota`（Token Plan） | 坐席额度与共享用量包均耗尽 | 加购坐席/共享用量包，或等待重置 |
| `hour/week/month allocated quota exceeded`（Coding Plan） | 对应周期额度用完 | 等待自动恢复/重置 |
| `concurrency allocated quota exceeded`（Coding Plan） | 并发超上限 | 等待片刻重试 |

### 连接与工具类

- `Connection error`：Base URL 域名拼写错误或网络异常，检查拼写与网络。
- Claude Code `Unable to connect to Anthropic services`：首次启动连接 api.anthropic.com 失败，在 `~/.claude.json` 添加顶层 `"hasCompletedOnboarding": true` 后重启。
- OpenClaw `Unknown model` / `No API key found for provider` / `API rate limit reached`：核对 `models.providers.bailian` 配置、`agents.defaults.model.primary` 加 `bailian/` 前缀、清理 `models.json` 与 `auth-profiles.json` 缓存后 `openclaw gateway restart`。
- OpenClaw `Failed to discover Alibaba Cloud models`：模型列表不支持接口查询，可忽略；如需屏蔽，删除 `auth-profiles.json` 中 `alibaba-cloud:default` profile。
- `Coding Plan is currently only available for Coding Agents`：在不支持的工具（curl/Postman/Dify）上调用，需切换到编程工具。

### 计费异常

开通 Coding Plan 后仍产生扣费/欠费，常见原因：未正确配置专属 API Key 和 Base URL（最常见，误用通用凭证被识别为按量计费）、账单结算延迟、同时配置通用与专属凭证被路由到通用、客户端缓存未清理。需确保 API Key 为 `sk-sp-xxx`、Base URL 含 `coding` 关键字，并清理工具缓存重启。

## 使用限制与数据安全

- **使用范围**：两类套餐仅限兼容 AI 编程和智能体工具的交互式使用，禁止自动化脚本、应用后端、非交互式批量调用。
- **账号规范**：API Key 仅限已分配席位的成员/订阅人本人使用，不可共享或公开泄露；系统检测到泄露可能自动禁用。
- **数据安全**：Token Plan 团队版承诺不使用对话数据训练模型，传输 HTTPS 加密，多租户隔离；Coding Plan 期间模型输入与生成内容用于服务改进与模型优化，停止使用可终止后续授权。
- **服务地域**：Token Plan 团队版目前仅华北2（北京）；Coding Plan 不限制使用地域，海外用户可正常使用或选择国际站。

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


