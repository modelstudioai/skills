# token plan guide

百炼平台面向 AI 编程与智能体场景提供两类订阅制套餐：**Token Plan 团队版**（按 Token 消耗抵扣 Credits、面向团队/企业、支持文本与图像生成）和 **Coding Plan**（按模型调用次数计费、面向个人开发者、纯文本模型）。两者的 API Key（均以 `sk-sp-` 开头）与 Base URL 完全隔离、互不相通，配套使用才能正确抵扣额度。本文汇总两套套餐的支持模型、接入方式、计费机制及常见限制。

## 两种套餐对比

| 维度 | Token Plan 团队版 | Coding Plan |
| --- | --- | --- |
| 适用场景 | 一人公司 / 团队 / 企业日常办公 | 个人开发场景 |
| 支持模型 | 文本生成 + 图像生成 | 文本生成 |
| 计费方式 | 按 Token 消耗抵扣 Credits | 按模型调用次数 |
| 使用频次 | 无每 5 小时 / 每周限额 | 有每 5 小时 / 每周 / 每月限额 |
| 高峰性能 | 多租户隔离，不排队 | 高峰期间可能排队 |
| 数据安全 | 承诺不使用对话数据训练模型 | 用户数据授权用于服务改进 |

> **注意**：两个套餐互不转换，即使补差价也不支持将 Token Plan 团队版换成 Coding Plan（或反之），但可同时订阅、各自独立计费。详见 [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-faq.md)。

## 支持的模型

**模型清单为精确字符串白名单**，必须逐字符完全匹配，版本号/子型号任何差异均视为不支持，禁止做版本兼容推理。

- **Token Plan 团队版**：千问（qwen3.7-max、qwen3.7-plus、qwen3.6-plus、qwen3.6-flash、qwen-image-2.0、qwen-image-2.0-pro）、万相（wan2.7-image、wan2.7-image-pro）、DeepSeek（deepseek-v4-pro、deepseek-v4-flash、deepseek-v3.2）、月之暗面（kimi-k2.7-code、kimi-k2.6、kimi-k2.5）、智谱（glm-5.2、glm-5.1、glm-5）、MiniMax（MiniMax-M2.5）。完整能力标注见 [Token Plan（团队版）概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)。
- **Coding Plan（Pro 套餐）**：推荐 qwen3.7-plus、qwen3.6-plus、kimi-k2.5、glm-5、MiniMax-M2.5；更多包含 qwen3.5-plus、qwen3-max-2026-01-23、qwen3-coder-next、qwen3-coder-plus、glm-4.7。详见 [Coding Plan概述](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)。

> **注意**：Coding Plan Lite 基础套餐已于 2026-03-20 起停止新购、2026-04-13 起停止续费与升级，已购用户可继续使用至到期。

## 接入方式

两套套餐均兼容主流 AI 编程/智能体工具（Claude Code、Qwen Code、OpenClaw、OpenCode、Cursor、Codex、Cline、Qoder、Kilo CLI 等），核心是「专属 API Key + 匹配协议的 Base URL」。

**Token Plan 团队版 Base URL**（华北2 北京地域，见 [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-quickstart.md)）：

- OpenAI 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
- Anthropic 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`

**Coding Plan Base URL**：

- OpenAI 兼容：`https://coding.dashscope.aliyuncs.com/v1`
- Anthropic 兼容：`https://coding.dashscope.aliyuncs.com/apps/anthropic`

三步接入 Token Plan：订阅套餐 → 分配席位并获取专属 API Key（`sk-sp-` 开头，仅创建/重置时完整显示一次）→ 按工具协议配置 Base URL。RAM 子账号订阅前需主账号授予 `AliyunBailianFullAccess` 权限。

> **注意**：Token Plan 专属 API Key（`sk-sp-`）、Coding Plan 专属 API Key 与百炼通用 API Key（`sk-`）格式不同且完全隔离。误用通用 Key 或错误 Base URL 会走按量计费通道产生意外扣费，或返回 401/403 鉴权失败。

## 扩展能力

- **工具调用（Token Plan）**：qwen3.7-max、qwen3.7-plus、qwen3.6-plus、qwen3.6-flash 的 Responses API 内置联网搜索、代码解释器、网页抓取、以图搜图、文搜图 5 种工具，自动调用、不额外收费（token 从套餐 Credits 抵扣）。其他模型通过百炼 MCP 广场的 MCP 服务接入。
- **联网搜索 MCP**：Endpoint 为 `https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp`，鉴权用**百炼通用 API Key（`sk-xxx`，非套餐 Key）**。全部用户前 2000 次调用免费，超出按 29 元/千次计费。协议已从旧版 SSE 升级为 Streamable HTTP。
- **图像生成模型（Token Plan）**：qwen-image-2.0、wan2.7-image 等使用独立的 `multimodal-generation` API，不在文本模型 Base URL 上调用，需通过工具的 Skill / Slash Command / Agent 扩展机制接入，详见 [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)。
- **视觉理解（Coding Plan）**：qwen3.6-plus、qwen3.5-plus、kimi-k2.5 原生支持视觉，直接切换即可；glm-5、MiniMax-M2.5 等纯文本模型可通过 Skill/Agent 转发到视觉模型获得图像理解能力。

## 团队管理（Token Plan 团队版）

角色分为**所有者 / 管理员 / 成员**。所有者与管理员可添加/移除成员、分配或回收席位、修改角色、查看用量。席位是最小订阅单位，一席绑定一个成员与一个 API Key，不可共享。成员支持手动添加（仅供 API 调用）或通过 **SAML 2.0（SSO）/ 钉钉**登录管理平台自助加入。用量分析可查看近 1/7/30 天的 Credits 趋势、各模型与各成员消耗明细。

## 计费、额度与限制

- **Token Plan 计费**：单次消耗由模型类型、输入/缓存/输出 Token、思考模式、工具调用动态决定。抵扣顺序为「坐席月度额度 → 共享用量包（多个时优先最近到期）→ 用尽则暂停至下一周期」。坐席额度按订阅月到期重置、不累积；共享用量包有效期 1 个月。**续费不叠加到当前周期额度**，需立即恢复可加购共享用量包/坐席或升级坐席。
- **Coding Plan 限制**：Pro 套餐每 5 小时 6,000 次、每周 45,000 次、每月 90,000 次。每 5 小时额度滚动恢复，每周一 00:00（UTC+8）重置周额度，每月按订阅日重置。
- **使用范围**：两套套餐均**仅限在兼容 AI 编程/智能体工具中交互式使用**，禁止用于自动化脚本或应用后端，违规可能导致订阅暂停或 API Key 封禁。
- **退订**：Token Plan 团队版支持按席位退订（已消耗用量的席位不可退订，退款 1-3 个工作日原路退回）；**Coding Plan 不支持退款**。

调用失败时可对照文档排查常见报错（401/403 鉴权、404 模型不存在、400 参数超限、429 限流/额度用尽等），详见 [Coding Plan 常见问题](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan-faq.md)。

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


