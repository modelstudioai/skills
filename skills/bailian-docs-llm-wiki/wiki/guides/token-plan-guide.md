# token plan guide

阿里云百炼面向 AI 编程与智能体场景提供两种订阅制套餐：**Token Plan 团队版**（按 Credits 计量、面向团队、支持文本与图像模型）和 **Coding Plan**（按模型调用次数计量、面向个人开发者、仅文本模型）。两者共享"通过专属 API Key + 专属 Base URL 接入兼容 OpenAI / Anthropic 协议的 AI 编程工具"的接入范式，但 API Key、Base URL、计费机制、数据策略均互不相通，使用前必须明确选型。

## 两种套餐的核心差异

详细对比见[常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-faq.md)。要点：

| 维度 | Token Plan 团队版 | Coding Plan |
| --- | --- | --- |
| 定位 | 团队/企业日常办公与协作 | 个人开发者 |
| 计费 | 按输入/缓存/输出 Token 抵扣 Credits | 按模型调用次数 |
| 频次限制 | 无每 5 小时/每周限额 | 有每 5 小时、每周、每月限额 |
| 模型范围 | 文本生成 + 图像生成 | 仅文本生成 |
| 高峰期 | 多租户隔离，不排队 | 高峰可能排队 |
| 数据策略 | 承诺**不用于**模型训练 | 模型输入与生成内容用于服务改进与模型优化 |
| API Key | `sk-sp-xxx`（管理后台为成员分发） | `sk-sp-xxx`（个人控制台获取） |
| Base URL 域名 | `token-plan.cn-beijing.maas.aliyuncs.com` | `coding.dashscope.aliyuncs.com` |
| 服务地域 | 仅华北 2（北京） | 不限地域 |

> **注意**：两套餐的 API Key 都以 `sk-sp-` 开头但**互不相通**，配错会触发 `401 Invalid API-key` 或 `401 invalid access token`。同样，把 Token Plan 的 Base URL 用到 Coding Plan 工具上、或反之，会得到 `400 url error` / `404 status code`。

## 支持的模型

### Token Plan 团队版

来自[Token Plan（团队版）概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)的精确白名单（**逐字符匹配，禁止做版本兼容推理**）：

- **千问**：`qwen3.7-max`（推理+文本，限时活动 Credits 减半至 2026-06-22）、`qwen3.6-plus`（推理+视觉+文本）、`qwen3.6-flash`、`qwen-image-2.0`、`qwen-image-2.0-pro`（图像生成）
- **万相**：`wan2.7-image`、`wan2.7-image-pro`（图像生成）
- **DeepSeek**：`deepseek-v4-pro`、`deepseek-v4-flash`、`deepseek-v3.2`
- **月之暗面**：`kimi-k2.6`、`kimi-k2.5`（含视觉）
- **智谱 AI**：`glm-5.1`、`glm-5`
- **MiniMax**：`MiniMax-M2.5`

### Coding Plan（Pro 套餐）

来自[Coding Plan概述](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)：

- 推荐：`qwen3.6-plus`、`kimi-k2.5`（均含视觉）、`glm-5`、`MiniMax-M2.5`
- 更多：`qwen3.5-plus`、`qwen3-max-2026-01-23`、`qwen3-coder-next`、`qwen3-coder-plus`、`glm-4.7`

> **注意**：Coding Plan **不包含** `qwen3.7-max`、图像生成模型（`qwen-image-2.0` / `wan2.7-image`）以及 DeepSeek 系列，这些只在 Token Plan 团队版中可用。Coding Plan Lite 套餐已于 2026-03-20 停止新购、2026-04-13 停止续费与升级，仅 Pro 套餐可新购。

## Base URL 速查

按协议选择正确的端点，路径不匹配会直接报错：

| 套餐 | 协议 | Base URL |
| --- | --- | --- |
| Token Plan 团队版 | OpenAI 兼容 | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| Token Plan 团队版 | Anthropic 兼容 | `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` |
| Coding Plan | OpenAI 兼容 | `https://coding.dashscope.aliyuncs.com/v1` |
| Coding Plan | Anthropic 兼容 | `https://coding.dashscope.aliyuncs.com/apps/anthropic` |

判定路径与协议的对应关系：Anthropic 兼容协议（Claude Code 等）以 `/apps/anthropic` 结尾；OpenAI 兼容协议（Cursor、Qwen Code、Cline 等）以 `/compatible-mode/v1` 或 `/v1` 结尾。

## 快速接入流程

1. **订阅**：访问购买页（[Token Plan 团队版](https://common-buy.aliyun.com/token-plan/) 或 [Coding Plan](https://common-buy.aliyun.com/coding-plan)）下单。Token Plan 团队版提供标准/高级/尊享三档坐席（分别 25,000 / 100,000 / 250,000 Credits/月），可加购共享用量包（5,000 元/625,000 Credits，月度有效期，到期清零）。
2. **获取 API Key 与 Base URL**：
   - Token Plan：在[管理后台](https://tokenplan-enterprise.bailian.console.aliyun.com)由管理员创建成员账号、分配席位后生成 API Key。详见[快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-quickstart.md)。
   - Coding Plan：在 [Coding Plan 页面](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/coding_plan)直接获取专属 `sk-sp-xxx` Key。
3. **配置 AI 工具**：填入对应的 API Key 与 Base URL。官方覆盖 OpenClaw、Hermes Agent、Claude Code、OpenCode、Cursor、Codex、Qwen Code、Cherry Studio、Chatbox、Cline、Qoder、Lingma、Kilo CLI 等主流工具。
4. **（可选）扩展能力**：见下方"工具调用"与"图像生成"章节。

## Credits 计费机制（仅 Token Plan）

- **计量维度**：单次调用按输入 Tokens、缓存 Tokens、输出 Tokens 与模型单价综合计算。示例：qwen3.6-plus 单次请求消耗约 3.18 Credits（8,349 输入 + 40,794 缓存 + 573 输出）。
- **抵扣顺序**：坐席月度额度 → 共享用量包（多个时优先抵扣最近到期者）→ 全部用尽后服务暂停至下月或购买共享用量包补充。
- **重置规则**：坐席额度按订阅月重置，**未用完不累积**；共享用量包同样按月重置。
- **查看用量**：控制台**我的订阅**页面查看百分比、重置时间、席位状态；管理平台**用量分析**页面查看近 1/7/30 天趋势、模型用量、成员明细。

## Coding Plan 额度规则

Pro 套餐 ¥200/月，含三档限额：每 5 小时 6,000 次、每周 45,000 次、每月 90,000 次。每次提问简单任务约消耗 5-10 次，复杂任务 10-30+ 次。额度恢复方式：

- **5 小时额度**：滚动恢复，每分钟自动释放 5 小时前的额度。
- **每周额度**：每周一 00:00（UTC+8）重置。
- **每月额度**：在下一个月订阅日的 00:00（UTC+8）重置。

> **注意**：Coding Plan 额度用完后**不会**自动转按量计费，调用会直接报错（`hour/week/month allocated quota exceeded`），需等待重置周期或购买新订阅。

## 团队管理（Token Plan 专属）

[团队管理](../../raw/model-user-guide/token-plan-guide/token-plan-team.md)涵盖三类角色：

- **拥有者** / **管理员**：添加/移除成员、分配/回收席位、修改成员角色、查看全部用量。
- **成员**：仅使用管理员分发的 API Key 与 Base URL 调用模型。

接入方式：

- **手动添加**：管理员在管理后台创建账号（用户名仅支持英文字母/数字/下划线，不能数字开头）、分配席位、生成 API Key 后分发；成员不能登录管理平台，仅供 API 调用。
- **SSO（SAML 2.0）**：组织内有成员时不能编辑 SSO 配置，需先全部移出。配置流程：在 IdP 创建 SAML 应用 → 把 IdP Entity ID / SSO URL / Certificate 填入百炼 → 把百炼自动生成的 ACS URL 和自定义 SP Entity ID 回填 IdP → 分享管理平台地址给成员。文档以阿里云 IDaaS EIAM 为例给出完整配置示范。
- **钉钉接入**：钉钉开放平台创建企业内部应用 → 配置回调 URL `https://account-enterprise.bailian.aliyunportal.com/api/v1/auth/dingtalk/callback` → 开通**通讯录个人信息读权限** → 发布应用 → 把 AppKey/AppSecret 填入 Token Plan 管理平台。

席位操作支持分配、回收、批量升级/退订；席位回收后原 API Key 立即失效，重新分配时系统生成新 Key。**已有用量消耗的席位不可退订**。

## 工具调用（联网搜索 / 代码解释器等）

详见 Token Plan 的[工具调用](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-tool.md)与 Coding Plan 的[联网搜索](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/web-search-for-coding-plan.md)。两种接入方式：

1. **模型内置工具**（仅 `qwen3.7-max` / `qwen3.6-plus` / `qwen3.6-flash`）：Responses API 内置联网搜索、代码解释器、网页抓取、以图搜图、文搜图五类工具，模型按需自动调用，**不额外收费**，token 消耗从套餐 Credits 抵扣。
2. **百炼 MCP 服务**（其他模型）：联网搜索 MCP 全部用户前 2000 次免费，之后 29 元/千次。

> **注意**：调用 MCP 服务用的是**百炼通用 API Key**（`sk-xxx`），与 Token Plan / Coding Plan 的专属 Key（`sk-sp-xxx`）不同；并且联网搜索 MCP 已从 SSE 升级为 Streamable HTTP，老用户需在 MCP 广场"取消开通 + 重新开通"完成协议升级。新版端点为 `https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp`，老端点 `.../WebSearch/sse` 已不可用。

主流工具的添加命令：

- **Claude Code**：`claude mcp add WebSearch <endpoint> -t http -H "Authorization: Bearer YOUR_API_KEY"`
- **Qwen Code**：`qwen mcp add WebSearch -t http "<endpoint>" -H "Authorization: Bearer YOUR_API_KEY"`
- **OpenCode / Kilo CLI / Kilo Code IDE**：在 `~/.config/<tool>/<config>.json` 写入 `mcp` 段
- **OpenClaw**：先 `npm install -g mcporter` → `openclaw config set skills.entries.mcporter.enabled true` → `mcporter config add WebSearch ...` → `openclaw gateway restart`

调用时建议在提问中明确提及 `websearch MCP`，避免与工具内置搜索混淆。

## 图像生成与视觉理解

### 在编程工具里调用图像生成模型（Token Plan）

图像生成模型走独立接口，无法用文本模型的 Base URL 直接调用，需通过工具的扩展机制（Slash Command / Skill / Agent）接入。完整示例见[接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)：在 Claude Code 中创建 `.claude/commands/text-to-image.md`，内部用 `curl` 调用 `https://token-plan.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`，从 `output.choices[*].message.content[*].image` 提取 URL 后本地下载。Codex / Qwen Code / OpenCode / OpenClaw / Hermes Agent 复用同一模板，仅扩展机制和配置路径不同（Skill 类工具需添加 `name` + `description` 的 YAML front matter；OpenCode Agent 需 `description` + `mode: subagent` + `tools` 形式的 front matter）。

### 给纯文本模型添加视觉能力（Coding Plan）

`qwen3.6-plus` / `qwen3.5-plus` / `kimi-k2.5` 原生支持视觉，**优先直接切换到这些模型**（`/model qwen3.6-plus` 等）。如必须用 `glm-5` / `MiniMax-M2.5` 等纯文本模型处理图片，可通过[添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/add-vision-skill.md)在 Claude Code 配置 Skill 或在 OpenCode 配置 Agent 让视觉模型代理图片解析。OpenCode 还需在配置中显式声明 `modalities: { input: ["text", "image"] }`；OpenClaw 需在 `~/.openclaw/openclaw.json` 的模型定义中加 `"input": ["text", "image"]`，并清除模型缓存后重启 Gateway。

## 常见报错排查

来自[Token Plan FAQ](../../raw/model-user-guide/token-plan-guide/token-plan-faq.md)与[Coding Plan FAQ](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan-faq.md)：

| 报错 | 主要原因 | 处理 |
| --- | --- | --- |
| `401 InvalidApiKey: Invalid API-key provided` / `401 invalid access token or token expired` | API Key 套餐错配、过期、复制有空格 | 核对 `sk-sp-xxx` 与套餐一致；必要时在控制台重置 |
| `401 Incorrect API key provided` / `403 invalid api-key` | 误用了通用 Base URL（`dashscope.aliyuncs.com`） | 改用专属 Base URL（含 `token-plan` 或 `coding` 关键字） |
| `404 model not found` / `400 Model not exist` / `model 'xxx' is not supported` | 模型名拼写或大小写错误，或模型不在套餐白名单 | 用精确字符串匹配套餐支持的 Model ID |
| `400 url error, please check url` / `404 status code (no body)` | Base URL 路径与协议不匹配 | OpenAI 兼容 → `/compatible-mode/v1` 或 `/v1`；Anthropic 兼容 → `/apps/anthropic` |
| `400 Range of input length should be [1, xxx]` | 上下文超限 | 新建会话 / 用工具的 `/compact` / `/clear` / 切换更大上下文模型（如 qwen3.6-plus 支持 1,000,000 tokens） |
| `400 max_tokens should be [1, xxxx]` / `thinking_budget must be a positive integer and not greater than xxxxx` | `max_tokens` / `budgetTokens` 超过模型上限 | 按报错数值下调；不支持思考的模型（如 `qwen3-coder-next`/`qwen3-coder-plus`）需移除 `thinking` 配置 |
| `429 rate limit exceeded` / `Throttling.AllocationQuota` / `insufficient_quota` | 短时请求过密 / 套餐额度耗尽 | 等待限流恢复或下个计费周期；Token Plan 可加购共享用量包 |
| `hour/week/month allocated quota exceeded` | Coding Plan 滚动/周/月额度用完 | 按对应规则等待恢复，月度需等订阅日 |
| `data_inspection_failed` | 内容触发安全策略 | 修改提示词避免敏感内容 |
| `Coding Plan is currently only available for Coding Agents` | 在 curl / Postman / Dify 等非编程工具中调用 Coding Plan | 仅限编程工具交互式使用 |

## 使用细则与限制

- **使用范围**：两个套餐均**仅限交互式 AI 编程与智能体工具**，禁止用于自动化脚本、应用后端、批量调用。违规可能被暂停订阅或封禁 API Key。
- **账号规范**：API Key 仅限单人使用，禁止共享或公开泄露；系统检测到泄露会自动禁用。Coding Plan 不支持多人共享、不支持企业多名开发者同时使用。
- **退订**：Token Plan 按席位退订，已有用量消耗的席位不可退，退款 1-3 个工作日原路退回。Coding Plan **不支持退款**。
- **续费**：到期前 7 / 3 / 1 天系统通过站内信、邮件、短信、智能外呼自动提醒；到期后不支持续费。
- **欠费影响**：Token Plan 为预付费，套餐内额度未用尽且未到期时阿里云账号欠费不影响使用。

完整错误码参见 [error-code](https://help.aliyun.com/zh/model-studio/error-code) 文档。

## 来源文档

- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-quickstart.md)
- [Token Plan（团队版）概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)
- [团队管理](../../raw/model-user-guide/token-plan-guide/token-plan-team.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-faq.md)
- [工具调用](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-tool.md)
- [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)
- [Coding Plan概述](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)
- [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/add-vision-skill.md)
- [联网搜索](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/web-search-for-coding-plan.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan-faq.md)



