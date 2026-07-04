# token plan guide

阿里云百炼提供两类面向 AI 编程与智能体场景的订阅型套餐——**Token Plan 团队版**与 **Coding Plan**。两者均以专属 API Key + 专属 Base URL 的方式接入主流 AI 编程工具（Claude Code、Qwen Code、OpenClaw、OpenCode、Cursor、Codex、Cline、Kilo CLI 等），通过预付费订阅锁定预算、避免按量计费欠费风险。本主题汇总两款套餐的产品定位、订阅流程、接入方式、团队与用量管理、工具扩展（联网搜索 / 多模态生成 / 视觉理解）以及高频报错排查。

## 套餐总览与对比

| 对比项 | Token Plan 团队版 | Coding Plan |
| --- | --- | --- |
| 适用场景 | 一人公司 / 团队 / 企业日常办公 | 个人开发场景 |
| 支持模型 | 文本生成 + 图像生成模型 | 文本生成模型 |
| 计费方式 | 按 Token 消耗抵扣 Credits | 按模型调用次数 |
| 使用频次限制 | 无每 5 小时 / 每周限额 | 每 5 小时 / 每周 / 每月限额 |
| 高峰期性能 | 多租户隔离，不排队 | 高峰期间可能排队 |
| 数据安全 | 承诺不使用对话数据训练模型 | 用户数据授权用于服务改进 |
| API Key 格式 | `sk-sp-xxx`（专属） | `sk-sp-xxx`（专属） |
| 服务地域 | 仅支持华北2（北京） | 不限制使用地域 |

> 三类 API Key 与 Base URL 互不相通：百炼按量计费（`sk-xxx` + `dashscope.aliyuncs.com`）、Token Plan 团队版（`sk-sp-xxx` + `token-plan.cn-beijing.maas.aliyuncs.com`）、Coding Plan（`sk-sp-xxx` + `coding.dashscope.aliyuncs.com`）。误用会导致按量计费扣费或 401/403 报错。

## Token Plan 团队版

### 产品简介

Token Plan 团队版整合千问、万相、DeepSeek、月之暗面、智谱 AI、MiniMax 等厂商模型，支持文本生成与图像生成，以 Credits 统一计量。提供标准坐席、高级坐席、尊享坐席三档套餐，配套团队管理后台（席位分配 / 用量分析 / SSO / 钉钉登录），并承诺不使用对话数据训练模型。目前仅支持**华北2（北京）**地域。

### 支持的模型

模型判定为**精确字符串白名单**，必须逐字符完全匹配，禁止版本兼容推理。支持品牌与模型 ID 包括：

- 千问：`qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-plus`、`qwen3.6-flash`、`qwen-image-2.0`、`qwen-image-2.0-pro`
- 万相：`wan2.7-image`、`wan2.7-image-pro`
- DeepSeek：`deepseek-v4-pro`、`deepseek-v4-flash`、`deepseek-v3.2`
- 月之暗面：`kimi-k2.7-code`、`kimi-k2.6`、`kimi-k2.5`
- 智谱 AI：`glm-5.2`、`glm-5.1`、`glm-5`
- MiniMax：`MiniMax-M2.5`

### 套餐与定价

| 坐席类型 | 价格 | 月度额度 | 适用场景 |
| --- | --- | --- | --- |
| 标准坐席 | ¥198/坐席/月 | 25,000 Credits | 轻度使用 AI 辅助 |
| 高级坐席 | ¥698/坐席/月 | 100,000 Credits | 日常高频 AI 编程/办公 |
| 尊享坐席 | ¥1,398/坐席/月 | 250,000 Credits | 重度依赖 AI 的核心开发者 |

席位是最小订阅单位，一个席位绑定一个成员、对应一个专属 API Key，不可共享。订阅周期支持按月、按年、连续包月包年。

**共享用量包**：跨坐席共享的弹性用量包，¥5,000/个，对应 625,000 Credits，有效期 1 个月，到期清零；持有多个时优先抵扣最近到期的用量包。需先订阅坐席套餐才能购买。

**限时活动**：即日起至 2026 年 7 月 22 日 23:59（UTC+8），`qwen3.7-max` 模型 Credits 消耗减半并支持隐式缓存。

### Credits 计费机制

单次消耗由模型类型、Token 用量、思考模式及工具调用动态决定，以控制台订阅页用量明细为准。以 `qwen3.6-plus` 为例：8,349 输入 tokens（1.67 Credits）+ 40,794 缓存 tokens（0.82 Credits）+ 573 输出 tokens（0.69 Credits）≈ **3.18 Credits**。

**抵扣顺序**：
1. 优先从坐席月度额度抵扣；
2. 坐席额度用尽后从共享用量包抵扣（多个时优先最近到期）；
3. 全部用尽后服务暂停至下一计费周期或购买共享用量包补充。

坐席额度在订阅月到期时重置，不累积；共享用量包额度有效期 1 个月，不随坐席按月重置。续费仅延长订阅有效期，不立即增加当月额度。

### 订阅管理

在 Token Plan 控制台「我的订阅」页面操作：

- **加购席位**：新加席位与现有订阅统一到期，费用与额度按剩余时长折算。
- **升级席位**：按差价补缴费用，支持批量升级。
- **退订席位**：按席位维度退订，已有用量消耗的席位不可退订；退款原路退回，1-3 个工作日到账。
- **续费 / 自动续费**：续费周期与订阅时一致；自动续费次日生效，到期前 9 天按周期自动扣款，关闭后到期自动停订。
- **加购共享用量包**：在「共享用量包」区域点击「前往购买」。

阿里云账号欠费不影响预付费订阅的正常使用，只要套餐额度未用尽且订阅有效即可。

### 快速开始三步

1. **订阅**：访问购买页面选择坐席类型与数量，主账号或 RAM 账号均可订阅。
2. **获取 API Key 与 Base URL**：管理员在成员管理页面创建成员并分配席位后，系统自动生成 API Key。Base URL 按协议选择：
   - OpenAI 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
   - Anthropic 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`
3. **接入 AI 工具**：在 Claude Code、Qwen Code、OpenClaw、OpenCode、Cursor、Codex、Cline、Cherry Studio、Chatbox、Qoder、Lingma、Kilo CLI 等工具中填入专属 API Key 与 Base URL 即可。

### 团队管理

**访问入口**：阿里云主账号或 RAM 用户登录 Token Plan 控制台，在「我的订阅」页面进行管理；通过 SSO 或钉钉加入的成员使用管理员分发的管理平台地址（形如 `tokenplan-enterprise.bailian.aliyunportal.com`）登录。RAM 用户使用前需主账号授予 `AliyunTokenPlanReadOnlyAccess` 或 `AliyunTokenPlanFullAccess` 系统策略，并在百炼账号管理页面分配管理员或订阅套餐权限。

**角色与权限**：

| 角色 | 权限 |
| --- | --- |
| 所有者 | 添加/移除成员、分配/回收席位、修改角色、查看全部用量 |
| 管理员 | 与所有者相同，由所有者授予，可被移除或降级 |
| 成员 | 使用管理员分配的 API Key 和 Base URL 调用模型 |

**成员管理**：
- 手动添加成员（仅供 API 调用，不能登录管理平台）：填用户名（英文字母/数字/下划线）和角色，分配席位后系统自动生成 API Key。
- SSO 或钉钉登录（可登录管理平台自管席位与 API Key）：完成 SAML 或钉钉接入配置后，成员从登录页对应入口登录即自动加入组织。
- 修改角色、重置 API Key（重置后原 Key 立即失效）、移出成员（席位自动回收、API Key 立即失效）均在成员管理页面操作。

**SAML 接入**：在控制台「团队版」卡片「设置」中的 SSO 配置区域编辑，填入自定义 SP Entity ID 及企业 IdP 的 IdP Entity ID、IdP SSO URL、IdP Certificate，保存后系统自动生成 ACS URL 与 SP Certificate，回填到企业 IdP 的 SSO 应用配置即可。支持阿里云 IDaaS 作为 IdP，需在 IDaaS 创建标准 SAML 2.0 应用并完成账户授权。

**钉钉接入**：在钉钉开发者后台创建企业内部应用，记录 Client ID/Client Secret，配置回调域名为 `https://account-enterprise.bailian.aliyunportal.com/api/v1/auth/dingtalk/callback`，开通通讯录个人信息读权限并发布应用，最后在 Token Plan 控制台 SSO 配置的钉钉选项卡填入 AppKey 与 AppSecret。

**席位操作**：查看席位状态、分配席位（生成 API Key）、回收席位（原成员失去额度，重新分配生成新 API Key）、加购席位（按剩余时长折算）、升级席位（按差价补缴，支持批量）。

**用量分析**：可查看近 1/7/30 天的 Credits 消耗趋势、各模型用量、各成员消耗明细。

## Coding Plan

### 产品简介

Coding Plan 整合千问、GLM、Kimi、MiniMax 模型，兼容主流 AI 编程工具，折算成本远低于常规 API 调用，固定月费防范欠费风险。仅支持按月订阅，无年付套餐；不支持退款；每个百炼账号同时只能订阅一个 Coding Plan。

### 套餐详情

Lite 基础套餐自 2026 年 3 月 20 日起停止新购，4 月 13 日起停止续费与升级，已购买用户可继续使用至服务到期。当前主推 **Pro 高级套餐**：

- **价格**：¥200/月
- **支持模型**：qwen3.7-plus（图片理解）、qwen3.6-plus（图片理解）、kimi-k2.5（图片理解）、glm-5、MiniMax-M2.5；以及 qwen3.5-plus（图片理解）、qwen3-max-2026-01-23、qwen3-coder-next、qwen3-coder-plus、glm-4.7
- **用量限制**：每 5 小时 6,000 次请求 / 每周 45,000 次 / 每月 90,000 次
- **额度消耗**：按模型调用次数扣除，简单任务约 5-10 次，复杂任务约 10-30+ 次
- **额度恢复**：每 5 小时额度滚动恢复（每分钟释放 5 小时前的额度）；每周一 00:00（UTC+8）重置；每月额度在下月订阅日 00:00 重置

Pro 与 Lite 套餐使用同样的模型资源与推理服务，响应速度相同；套餐内模型均为完整版，未量化、未阉割。Coding Plan 额度用尽后**不会**自动转为按量计费，继续调用会失败报错。

### 快速开始三步

1. **订阅**：访问 Coding Plan 购买页选择套餐。RAM 子账号需先在百炼权限管理页面由主账号添加用户并授予管理员权限后再订阅。
2. **获取专属 API Key 与 Base URL**：在 Coding Plan 页面获取 `sk-sp-xxx` 格式专属 API Key。Base URL 按协议选择：
   - OpenAI 兼容：`https://coding.dashscope.aliyuncs.com/v1`
   - Anthropic 兼容：`https://coding.dashscope.aliyuncs.com/apps/anthropic`
3. **接入 AI 工具**：在 Claude Code、Qwen Code、OpenClaw、OpenCode、Cursor、Codex 等工具中填入专属配置。

### 订阅前须知

1. **严禁 API 调用**：仅限在编程工具中交互式使用，禁止用于自动化脚本、应用后端、Dify、Postman、curl 等非交互式批量调用。违规可能导致订阅暂停或 API Key 封禁。
2. **数据使用授权**：使用期间模型输入与生成内容用于服务改进与模型优化；停止使用可终止后续授权，但不涵盖已授权数据。
3. **账号专享**：禁止共享，Pro 套餐不支持企业多名开发人员同时使用。系统检测到 API Key 公开泄露会自动禁用。

### 额度与续费

- 额度用完：5 小时/每周额度等待自动恢复，每月额度等待下个订阅月恢复；不支持降配到 Lite。
- 自动续费：开启后次日生效，到期前 9 天 08:00 开始扣款（仅扣账户可用额度，不支持银行卡/支付宝/信用卡），失败次日继续，到期前 1 天停止自动续费需手动续费。
- 提前续订：新周期在原到期日基础上自动顺延；到期后不支持续费。
- 到期提醒：到期前 7/3/1 天通过站内信、邮件、短信、智能外呼自动推送，无需手动订阅。
- 代金券：续订可使用通用代金券。

### 上下文长度与思考模式

各模型上下文长度：qwen3.7-plus / qwen3.6-plus / qwen3.5-plus / qwen3-coder-plus 为 1,000,000；kimi-k2.5 / qwen3-max-2026-01-23 / qwen3-coder-next 为 262,144；glm-5 / glm-4.7 为 202,752；MiniMax-M2.5 为 196,608。

避免上下文超限的方法：新建会话、切换更[长上下文](../concepts/long-context.md)模型、减少无关文件、拆分任务、精确指令；OpenCode 可配置 `limit` 限制上下文长度。

各模型最大思维链长度：qwen3.7-plus 262,144；qwen3.6-plus / qwen3.5-plus / qwen3-max-2026-01-23 / kimi-k2.5 为 81,920；glm-5 / glm-4.7 为 32,768；MiniMax-M2.5 默认启用无需配置；qwen3-coder-next / qwen3-coder-plus 不支持思考模式。

## 工具扩展能力

### 工具调用（Token Plan 团队版）

Token Plan 团队版提供两种工具接入方式：

1. **模型内置工具**：`qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-plus`、`qwen3.6-flash` 的 Responses API 内置联网搜索、代码解释器、网页抓取、以图搜图、文搜图 5 种工具，启用后模型自动调用。内置工具不额外收费，token 消耗从套餐 Credits 抵扣。
2. **MCP 服务**：其他模型（deepseek-v3.2、glm-5 等）通过百炼 MCP 广场的 MCP 服务获取工具能力。联网搜索 MCP 全部用户前 2000 次免费，用尽后 29 元/千次；其他 MCP 服务部分限时免费。

接入 MCP 需使用百炼通用 API Key（`sk-xxx`，用于调用 MCP 服务），与套餐专属 API Key（`sk-sp-xxx`）不同。联网搜索 MCP 的 Streamable HTTP Endpoint 为 `https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp`。各工具接入命令示例：

- Claude Code：`claude mcp add WebSearch https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp -t http -H "Authorization: Bearer YOUR_API_KEY"`
- Qwen Code：`qwen mcp add WebSearch -t http "https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp" -H "Authorization: Bearer YOUR_API_KEY"`
- OpenCode / Kilo CLI：在 `opencode.json` 的 `mcp` 字段写入远程 HTTP 配置。
- OpenClaw：通过 `mcporter` 安装并 `openclaw gateway restart` 生效。
- Kilo Code IDE 插件：在 `mcpServers` 中配置 `streamable-http` 类型。

> 提问时建议明确提及 `websearch MCP` 以避免与其他工具混淆。旧版 SSE 协议（`/sse` 结尾）需取消开通后重新开通以升级到 Streamable HTTP。

### 接入多模态生成模型（图像生成）

Token Plan 团队版支持 `qwen-image-2.0`、`qwen-image-2.0-pro`、`wan2.7-image`、`wan2.7-image-pro` 等图像生成模型，但需通过工具的扩展机制（Skill / Slash Command / Agent）接入，无法通过文本模型 Base URL 直接调用。

以 Claude Code 为例，在项目根目录创建 `.claude/commands/text-to-image.md` Slash Command，调用 `https://token-plan.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation` 文生图接口，从返回 JSON 的 `output.choices[*].message.content[*].image` 提取 URL 并下载。其他工具的扩展机制与配置路径：Codex / Qwen Code / OpenClaw / Hermes Agent 使用 Skill（`SKILL.md`，需 YAML front matter），OpenCode 使用 Agent（`.opencode/agents/*.md`）。

### 添加视觉理解能力（Coding Plan）

Coding Plan 中 `qwen3.6-plus`、`qwen3.5-plus`、`kimi-k2.5` 原生支持视觉理解，可直接传入图片。对于 `glm-5`、`MiniMax-M2.5`、`qwen3-max-2026-01-23`、`qwen3-coder-next/plus`、`glm-4.7` 等纯文本模型，可通过 Skill 或 Agent 调用视觉模型获得视觉能力。

- **Claude Code**：在 `.claude/skills/image-analyzer/SKILL.md` 中配置 `model: qwen3.6-plus`，启动后 `/model glm-5` 切换到纯文本模型，提问时加载该 [skill](skill.md)。
- **OpenCode**：在 `.opencode/agents/image-analyzer.md` 中配置 `model: bailian-coding-plan/qwen3.6-plus`，通过 `@image-analyzer` 唤起。

**常见问题**：
- OpenCode + 视觉模型无法理解图片：默认不启用视觉能力，需在模型定义中显式声明 `modalities.input: ["text", "image"]`。
- OpenClaw + 视觉模型无法理解图片：需在 `~/.openclaw/openclaw.json` 模型定义中包含 `"input": ["text", "image"]`，修改后需删除 `~/.openclaw/agents/main/agent/models.json` 缓存并 `openclaw gateway restart`。

## 查看额度与用量

- **Token Plan 团队版**：控制台「我的订阅」查看总额度使用百分比、重置时间、席位分配、共享用量包状态；管理平台「用量分析」查看近 1/7/30 天 Credits 趋势、各模型用量、各成员消耗明细。
- **Coding Plan**：在 Coding Plan 页面查看套餐总额度整体消耗与剩余；暂无法查看 Token 消耗或特定模型使用量，因额度仅与模型调用次数相关。

## 使用限制与数据安全

- **使用范围**：两类套餐均仅限在兼容的 AI 编程和智能体工具中交互式使用，不可用于自动化脚本、应用后端、Dify、Postman、curl 等非交互式批量调用。
- **账号规范**：API Key 仅限已分配席位的成员本人使用（Token Plan）或订阅人专享（Coding Plan），不可共享或公开泄露，系统检测到泄露会自动禁用。
- **数据安全**：Token Plan 团队版承诺不使用对话数据训练模型，传输采用 HTTPS 加密，多租户隔离；Coding Plan 期间模型输入与生成内容用于服务改进与模型优化。
- **服务地域**：Token Plan 团队版仅华北2（北京）；Coding Plan 不限制使用地域，海外用户可正常使用，也可选择国际站 Coding Plan。

## 常见报错与排查

### 认证类报错

| 报错 | 原因 | 解决方案 |
| --- | --- | --- |
| `401 InvalidApiKey: No API-key provided` | 请求头未携带 API Key | 在管理后台生成 API Key 并配置到工具 |
| `401 InvalidApiKey: Invalid API-key provided` | 误用通用 Key / 订阅过期 / 复制不完整 | 确认专属 API Key 完整无空格，确认订阅有效，必要时重置 |
| `401 invalid access token or token expired` | 误用其他套餐 Base URL | 改用对应套餐的专属 Base URL |
| `401 Incorrect API key provided` | 误用通用 Base URL | 改用套餐专属 Base URL |
| `403 invalid api-key`（Coding Plan） | 误用通用 Base URL | Anthropic: `https://coding.dashscope.aliyuncs.com/apps/anthropic`；OpenAI: `https://coding.dashscope.aliyuncs.com/v1` |
| `Authentication failed ... ModelScope token` | 接入了第三方 ModelScope 服务 | 改用百炼专属配置 |
| `Coding Plan is currently only available for Coding Agents` | 使用了不支持的工具（curl/Postman/Dify） | 仅在编程工具中使用 |

### 模型与参数类报错

| 报错 | 原因 | 解决方案 |
| --- | --- | --- |
| `404 model 'xxx' not found` / `400 Model not exist` | 模型名称拼写错误 / 不在套餐支持列表 | 模型 ID 区分大小写，与套餐支持列表完全一致 |
| `400 InvalidParameter: Range of input length` | 输入超出最大上下文 | 新建会话、`/compact`、切换更[长上下文](../concepts/long-context.md)模型、OpenCode 配置 `limit` |
| `400 InvalidParameter: Range of max_tokens` | `max_tokens` 超过模型上限 | 调整为报错提示的上限值 |
| `400 thinking_budget parameter must be a positive integer ...` | 思维链长度超过模型上限 | 调整 `budgetTokens` 不超过上限，不支持思考模式的模型移除该配置 |
| `400 data_inspection_failed` | 命中内容安全策略 | 修改输入内容，调整提示词避免敏感话题 |
| `400 url error` / `404 status code (no body)` | Base URL 路径与协议不匹配 | Anthropic 协议用 `/apps/anthropic`，OpenAI 协议用 `/compatible-mode/v1` 或 `/v1` |

### 限流与额度类报错

| 报错 | 原因 | 解决方案 |
| --- | --- | --- |
| `429 API-Key Requests rate limit exceeded` | 短时间请求过于密集 | 等待约 1 分钟重试，降低请求频率 |
| `429 Throttling.AllocationQuota` / `insufficient_quota` | 套餐额度用尽 或 触发 TPS/TPM 限流 | 额度用尽：加购坐席/共享用量包或等待重置；限流：平滑请求、指数退避，必要时申请临时 TPM 提额 |
| `hour/week/month allocated quota exceeded`（Coding Plan） | 5 小时/每周/每月额度用完 | 等待自动恢复；每月额度等待下个订阅月 |
| `concurrency allocated quota exceeded` | 并发超出动态上限 | 等待片刻重试 |
| `Connection error` | Base URL 拼写错误或网络异常 | 检查域名拼写与网络 |
| `Connection closed mid response` | 流式响应中断（网络波动/代理不稳定） | 客户端通常自动重试；频繁出现则关闭 VPN/代理 |

### OpenClaw 专属问题

- `Agent failed before reply: Unknown model`：`models.providers` 必须包含 `bailian` 键，`agents.defaults.model.primary` 必须加 `bailian/` 前缀；清理旧 provider 残留。
- `No API key found for provider "xxxxx"`：补充对应 provider 配置，确认 API Key 有效（`sk-sp-xxx`），清理 `auth-profiles.json` 与 `models.json` 缓存后 `openclaw gateway restart`。
- `Failed to discover Alibaba Cloud models`：模型列表不支持接口查询，可忽略；如需屏蔽，删除 `auth-profiles.json` 中的 `alibaba-cloud:default` profile。
- 显示已连接但无响应/一直转圈：关闭本地代理，删除 `~/.openclaw/agents/main/agent/models.json` 缓存并重启。
- 出现未配置模型的调用记录：在 `agents.defaults.models` 中显式声明允许模型列表。

### Claude Code 专属问题

- `Unable to connect to Anthropic services`：首次启动会连接 `api.anthropic.com` 初始化认证，在不可用地区会失败。在 `~/.claude.json` 添加顶层字段 `"hasCompletedOnboarding": true` 后重启（可用 `qwen` 命令让 Qwen Code 自动添加）。
- `Claude Code has switched from npm to native installer`：执行 `claude install` 迁移到原生安装版本。

### OpenCode 专属问题

- `Request Entity Too Large`：`/new` 新建对话或 `/compact` 压缩上下文；更新到 1.2.16 或以上版本。
- `thinking_budget ... not greater than 38912`：`budgetTokens` 超过模型上限，按各模型上限表调整。
- `InternalError.Algo InvalidParameter: Range of max_tokens`：`limit.output` 超过模型最大输出，调整 `opencode.json` 中对应模型 `limit`。

### 通用排查要点

1. **确认 API Key 与 Base URL 配对**：专属 Key（`sk-sp-`）必须配专属 Base URL（含 `coding` 或 `token-plan` 关键字），通用 Key（`sk-`）配通用 Base URL（`dashscope.aliyuncs.com`），三者不可混用。
2. **清理客户端缓存**：OpenClaw 删除 `~/.openclaw/agents/main/agent/models.json` 后 `openclaw gateway restart`；其他工具重启或重新加载配置。
3. **关闭本地代理**：VPN/HTTP Proxy 可能中断与 `coding.dashscope.aliyuncs.com` 或 `token-plan.cn-beijing.maas.aliyuncs.com` 的长连接。
4. **重置 API Key**：排查无效时在控制台重置，重置后更新到所有工具。
5. **使用阿里云 AI 助理**：其知识库整合官方帮助文档，可直接提问如「使用 coding plan 时，报错 model 'xxx' is not [support](support.md)ed 是什么原因」获取分析。

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



