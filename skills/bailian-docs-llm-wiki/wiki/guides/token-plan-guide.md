# token plan guide

Token Plan 是阿里云百炼面向开发者提供的 AI 模型订阅服务，以 Credits 为统一计量单位，支持在兼容的交互式 AI 工具中调用模型。它不适用于自动化脚本或后端服务等非交互场景，且与百炼按量计费体系（`sk-` Key）完全隔离。正确配置 `sk-sp-` 开头的专属 API Key 和配套 Base URL 是保障额度抵扣和调用成功的关键前提。

## 支持的模型/功能

Token Plan 支持千问（Qwen）、万相、DeepSeek、月之暗面（Kimi）、智谱 AI（GLM）、MiniMax、HappyHorse 等主流模型，但**个人版与团队版支持的模型范围不同**，具体清单需查阅对应版本文档：[个人版支持的模型](../token-plan-personal/token-plan-personal-overview.md#tppo-h-models) 和 [团队版支持的模型](../token-plan-team-edition/token-plan-team-overview.md#tpto-h-models)。

支持的功能包括：
- **模型内置工具**：联网搜索、文搜图、网页抓取、代码解释器等，通过 Responses API 自动触发，按 Credits 抵扣；
- **多模态能力**：图像生成、视频生成、语音合成/识别、实时语音对话等，需通过工具的 Skill/Slash Command/Agent 扩展机制接入，**不可直接使用文本模型 Base URL 调用**；
- **Harness 权益**（仅限个人版 Standard/Pro 套餐）：提供 AgentStudio 工具免费额度，使用 `sk-` 开头的百炼通用 API Key 调用，**不占用 Token Plan Credits**，详见 [Harness 权益](../token-plan-personal/token-plan-harness-benefits.md)。

> **注意**：文档 4 中称“模型内置工具”通过 Responses API 调用并按 Credits 抵扣，而文档 2 的 Harness 配置指南中列出的 MCP 服务（如图像生成 MCP）明确要求使用 `sk-` Key 和 `dashscope.aliyuncs.com` 地址——这表明同一工具名（如“图像生成”）存在两种接入路径：一种是模型内置、走 `sk-sp-` + Token Plan Base URL、消耗 Credits；另一种是 Harness 权益、走 `sk-` + 百炼通用地址、不消耗 Credits。开发者必须根据实际调用方式区分。

## 关键参数

- **API Key**：必须使用 `sk-sp-` 开头的 Token Plan 专属密钥，**不可混用** `sk-`（百炼通用）或 Coding Plan Key。Key 仅在生成时完整显示一次，泄露后需重置。
- **Base URL**：必须与 `sk-sp-` Key 配套使用，不可使用 `dashscope.aliyuncs.com` 或 `coding.dashscope.aliyuncs.com`。正确地址见 [接入AI工具·通用配置](../use-chat-client-or-development-tool.md#tpa-h-config)。
- **Credits 消耗**：1 Credits ≠ 1 Token。单次请求消耗由输入 Token、缓存 Token 和输出 Token 共同决定，并受模型单价、上下文长度、思考模式、工具调用次数及缓存命中率影响。例如团队版 `qwen3.6-plus` 一次调用可能消耗约 3.18 Credits（含缓存折算）[原文标题](../../raw/token-plan-user-guide/token-plan-guide/token-plan-usage-quota.md)。
- **并发与限流**：个人版档位决定建议并发数（Lite: 1–2，Pro: 6–8），超限将触发 `429 Requests rate limit exceeded`；团队版虽无固定上限，但会动态调整并发阈值。限流不支持人工提升，需等待或优化请求。

## 使用方式

1. **开通与获取 Key**：在 [百炼控制台 Token Plan 页面](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan) 购买套餐，生成 `sk-sp-` Key。
2. **配置工具**：为所用 AI 工具（如 Claude Code、Qwen Code、OpenClaw、Hermes Agent 等）配置 Key 和 Base URL。CLI 快速接入示例见 [Token Plan 概览](../../raw/token-plan-user-guide/token-plan-guide/token-plan-overview.md)。
3. **调用模型**：在工具内交互式发起请求（如自然语言编程、对话问答）。**禁止用于生产环境自动化脚本、批量任务或后台定时任务** [原文标题](../../raw/token-plan-user-guide/token-plan-guide/token-plan-permissions-and-usage.md)。
4. **调用 Harness 工具（可选）**：Standard/Pro 用户可额外配置 `sk-` Key 调用 Harness 服务（如 RAG、Memory、MCP 工具），不消耗 Credits，配置指南见 [Token Plan 概览](../../raw/token-plan-user-guide/token-plan-guide/token-plan-overview.md)。

## 限制和注意事项

- **使用范围限制**：Token Plan **仅限交互式开发场景**，严禁用于非交互式批量调用。违规可能导致订阅暂停或 Key 封禁 [原文标题](../../raw/token-plan-user-guide/token-plan-guide/token-plan-permissions-and-usage.md)。
- **额度独立性**：Token Plan 套餐额度、用量包、共享用量包、免费额度、资源包、节省计划及账户余额**全部相互独立**，不可交叉抵扣。
- **额度重置与结转**：额度按订阅月自动重置（非每月 1 日），**当月未用完额度不结转**；升级套餐/坐席不重置周期，新增额度按剩余天数折算发放。
- **RAM 子账号授权**：子账号需主账号授予 `AliyunTokenPlanFullAccess`、`AliyunBSSReadOnlyAccess`（个人版）或 `AliyunBSSFullAccess`（团队版）及百炼控制台权限，否则“我的订阅”页面可能为空。
- **额度用尽行为**：额度耗尽后调用被阻断（返回 `429 insufficient_quota`），**不会自动转为按量计费**。恢复方式仅限：等待重置、升级套餐/坐席、购买用量包或共享用量包 [原文标题](../../raw/token-plan-user-guide/token-plan-guide/token-plan-usage-quota.md)。
- **数据政策差异**：个人版使用数据可能用于服务改进；团队版**明确承诺不用于模型训练**。

## 来源文档

- [用量与额度](../../raw/token-plan-user-guide/token-plan-guide/token-plan-usage-quota.md)
- [Token Plan 概览](../../raw/token-plan-user-guide/token-plan-guide/token-plan-overview.md)
- [权限与使用规范](../../raw/token-plan-user-guide/token-plan-guide/token-plan-permissions-and-usage.md)
- [Token Plan 常见问题](../../raw/token-plan-user-guide/token-plan-guide/token-plan-faq.md)


