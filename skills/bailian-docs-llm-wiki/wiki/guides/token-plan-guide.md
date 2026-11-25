# token plan guide

[Token](../concepts/token.md) Plan 是阿里云百炼面向开发者提供的 AI 模型订阅服务，以 Credits 为统一计量单位，支持在兼容的编程与智能体工具中交互式调用模型。其核心设计是将模型使用成本与套餐额度绑定，而非按 [Token](../concepts/token.md) 精确计费；所有调用必须通过 `sk-sp-` 开头的专属 API Key 和配套 Base URL 发起，否则无法抵扣套餐额度。本文档聚焦关键实践要点，帮助开发者快速接入、合理规划用量并规避常见陷阱。

## 支持的模型与功能

[Token](../concepts/token.md) Plan 支持千问（Qwen）、万相、DeepSeek、月之暗面、智谱 AI、MiniMax 等主流模型，但**个人版与团队版支持的模型范围不同**，且部分模型（如视频生成、语音识别）需通过专用接口或工具扩展机制接入，不可直接通过文本模型 Base URL 调用 [Token Plan 常见问题](../../raw/token-plan-user-guide/token-plan-guide/token-plan-faq.md)。  
支持的 AI 工具包括：Claude Code、Codex、Qwen Code、OpenClaw、Hermes Agent、Qoder、WorkBuddy、Trae、DeepSeek Harness 等。所有工具均需配置 `sk-sp-` API Key 及 Token Plan Base URL 才能正确抵扣 Credits [Token Plan 概览](../../raw/token-plan-user-guide/token-plan-guide/token-plan-overview.md)。  
模型内置工具（如联网搜索、代码解释器）通过 Responses API 自动触发，**按 Credits 抵扣**；而 Harness 权益中的同名工具（如图像生成 MCP）需使用 `sk-` 开头的百炼通用 API Key 调用，不占用 Credits，属于独立权益 [Token Plan 常见问题](../../raw/token-plan-user-guide/token-plan-guide/token-plan-faq.md)。

> **注意**：文档 3 中明确说明“Harness 权益中的同名工具通过 `sk-` 开头的百炼 API Key 调用”，但文档 2 的 Harness 配置指南中给出的 MCP URL 示例均使用 `dashscope.aliyuncs.com` 域名（即百炼通用域名），这与 `sk-` Key 的使用逻辑一致；而文档 1 强调 `sk-sp-` Key **仅用于模型调用**，不能用于 Harness 工具。二者无矛盾，但需严格区分 Key 类型与服务域。

## 关键参数

- **Credits**：Token Plan 的唯一计量单位，**不等于 Token**。单次请求消耗由输入 Token、缓存 Token 和输出 Token 共同决定，且受模型单价、上下文长度、思考模式、[工具调用](../concepts/tool-calling.md)次数和缓存命中率影响。例如 `qwen3.6-plus` 一次调用可能消耗约 3.18 Credits，而非对应 Token 数 [用量与额度](../../raw/token-plan-user-guide/token-plan-guide/token-plan-usage-quota.md)。  
- **API Key**：必须为 `sk-sp-` 开头的 Token Plan 专属 Key；`sk-`（百炼通用）和 `sk-cp-`（Coding Plan）Key 均无法抵扣套餐额度。  
- **Base URL**：必须与 `sk-sp-` Key 配套使用，不可混用 `dashscope.aliyuncs.com` 或 `coding.dashscope.aliyuncs.com` 等其他计费体系的地址 [Token Plan 常见问题](../../raw/token-plan-user-guide/token-plan-guide/token-plan-faq.md)。  
- **额度重置**：按订阅月自动重置，重置时间取决于首次订阅日期（非每月 1 日），当月未用完额度不结转。

## 使用方式

1. **获取凭证**：在[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan)购买套餐后，获取 `sk-sp-` API Key。  
2. **配置工具**：按所用工具（如 Claude Code、Qwen Code）的指引，设置环境变量 `TOKEN_PLAN_API_KEY` 并执行 `bl config agent` 命令完成 CLI 配置 [Token Plan 概览](../../raw/token-plan-user-guide/token-plan-guide/token-plan-overview.md)。  
3. **调用模型**：在工具内发起交互式请求（如自然语言编程、代码生成）。  
4. **调用 Harness 工具（可选）**：若套餐附赠 Harness 权益（Standard/Pro），需单独使用 `sk-` Key 配置 MCP 服务（如图像生成 MCP URL），该调用不消耗 Credits [Token Plan 概览](../../raw/token-plan-user-guide/token-plan-guide/token-plan-overview.md)。  
5. **监控用量**：定期访问[用量分析页面](https://bailian.console.aliyun.com/cn-beijing/subscription/overview)查看各模型、成员的 Credits 消耗明细。

## 限制和注意事项

- **禁止生产自动化调用**：Token Plan 仅限交互式开发（如终端编码、AI 助手对话），**严禁用于后台定时任务、批量脚本或自定义应用后端** [权限与使用规范](../../raw/token-plan-user-guide/token-plan-guide/token-plan-permissions-and-usage.md)。  
- **额度用尽即阻断**：套餐额度与用量包（含团队版共享包）全部耗尽后，调用将返回 `429 insufficient_quota` 并被立即阻断，**不会自动降级为按量计费** [用量与额度](../../raw/token-plan-user-guide/token-plan-guide/token-plan-usage-quota.md)。  
- **并发与限流**：个人版有建议并发数（Lite：1–2 个 Agent；Pro：6–8 个），超限可能触发 `429 Requests rate limit exceeded`；团队版虽无排队，但仍存在动态调整的并发上限 [Token Plan 常见问题](../../raw/token-plan-user-guide/token-plan-guide/token-plan-faq.md)。  
- **账号与 Key 管理**：同一阿里云账号可同时持有个人版与团队版，额度完全独立；但 `sk-sp-` Key 仅限本人使用，多人共用或泄露可能导致封禁 [权限与使用规范](../../raw/token-plan-user-guide/token-plan-guide/token-plan-permissions-and-usage.md)。  
- **RAM 子账号**：需主账号授予 `AliyunTokenPlan*Access` + `AliyunBSS*Access` 权限，否则“我的订阅”页面可能为空 [权限与使用规范](../../raw/token-plan-user-guide/token-plan-guide/token-plan-permissions-and-usage.md)。

## 来源文档

- [用量与额度](../../raw/token-plan-user-guide/token-plan-guide/token-plan-usage-quota.md)
- [Token Plan 概览](../../raw/token-plan-user-guide/token-plan-guide/token-plan-overview.md)
- [Token Plan 常见问题](../../raw/token-plan-user-guide/token-plan-guide/token-plan-faq.md)
- [权限与使用规范](../../raw/token-plan-user-guide/token-plan-guide/token-plan-permissions-and-usage.md)


