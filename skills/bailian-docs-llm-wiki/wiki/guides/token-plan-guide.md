# token plan guide

[Token](../concepts/token.md) Plan 是阿里云百炼面向开发者提供的 AI 模型订阅服务，以 Credits 为统一计量单位，支持在兼容的编程与智能体工具中交互式调用模型。其核心设计是将模型使用成本与套餐额度绑定，而非按 [Token](../concepts/token.md) 精确计费；所有调用必须通过 `sk-sp-` 开头的专属 API Key 和配套 Base URL 发起，否则无法抵扣额度。开发者需重点关注模型支持范围、Credits 消耗逻辑及配置合规性，避免因误用导致按量扣费或调用失败。

## 支持的模型/功能

[Token](../concepts/token.md) Plan 支持千问（Qwen）、万相、DeepSeek、月之暗面、智谱 AI、MiniMax、HappyHorse 等多厂商模型，但**个人版与团队版支持的模型列表不同**，且部分模型（如视频生成、图像生成）需通过专用接口或工具扩展机制接入，不可直接通过文本模型 Base URL 调用。  
模型内置工具（如联网搜索、代码解释器、网页抓取）在通过 Responses API 调用时自动触发，**按 Credits 抵扣**；而 Harness 权益中同名工具（如图像生成 MCP、语音合成 MCP）需使用 `sk-` 开头的百炼通用 API Key 调用，**不占用 Credits**，详见 [Harness 权益](../token-plan-personal/token-plan-harness-benefits.md)。  
完整支持模型清单请查阅 [个人版支持的模型](../token-plan-personal/token-plan-personal-overview.md#tppo-h-models) 和 [团队版支持的模型](../token-plan-team-edition/token-plan-team-overview.md#tpto-h-models)，该信息亦在 [Token Plan 常见问题](raw/token-plan-user-guide/token-plan-guide/token-plan-faq.md) 中被引用和确认。

## 关键参数

- **API Key**：必须使用 `sk-sp-` 开头的 Token Plan 专属密钥，**不可混用** `sk-`（百炼通用）或 Coding Plan 的 Key；[Token Plan 常见问题](raw/token-plan-user-guide/token-plan-guide/token-plan-faq.md) 明确指出“团队版的 API Key 不能用在个人版上”，且“RAM 子账号需主账号授权后才能购买、管理订阅或使用模型”。
- **Base URL**：必须与 API Key 配套使用，Token Plan 的 Base URL 与百炼通用地址（`dashscope.aliyuncs.com`）和 Coding Plan 地址（`coding.dashscope.aliyuncs.com`）完全隔离。
- **Credits 消耗**：非线性计量单位，单次请求消耗由输入 Token、缓存 Token 和输出 Token 共同决定，并受模型单价、上下文长度、思考模式、工具调用次数及缓存命中率影响。例如 `qwen3.6-plus` 一次调用可能消耗约 3.18 Credits，而非等价于 Token 数量 [用量与额度](raw/token-plan-user-guide/token-plan-guide/token-plan-usage-quota.md)。

> **注意**：文档 3（FAQ）中“限流阈值（TPM/RPM）是多少？能否提升？”一节称“限流阈值会根据整体负载动态调整”，而文档 4（权限与使用规范）强调“**仅限在编程工具和智能体工具中交互式使用**，不可用于自动化脚本或批量调用”。二者逻辑一致，但需明确：动态限流是技术保障，而“禁止生产自动化调用”是使用策略红线——违反后者可能导致订阅暂停，而非仅触发限流。

## 使用方式

1. **开通与获取凭证**：在百炼控制台购买套餐后，获取 `sk-sp-` 开头的 API Key，并确认其与 Token Plan Base URL 配套。
2. **接入工具**：支持 Claude Code、Codex、Qwen Code、OpenClaw、Hermes Agent、Qoder、Trae、DeepSeek Harness、WorkBuddy 等主流工具。以 Claude Code 为例，需执行 CLI 安装并配置：
   ```bash
   curl -fsSL https://bailian.aliyun.com/cli/install.sh | bash
   export TOKEN_PLAN_API_KEY="sk-sp-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
   bl config agent --agent claude-code --region cn-beijing --api-key $TOKEN_PLAN_API_KEY --model auto
   ```
   完整接入指南见 [Token Plan 概览](raw/token-plan-user-guide/token-plan-guide/token-plan-overview.md)。
3. **Harness 权益接入（仅限个人版 Standard/Pro）**：使用 `sk-` 开头的百炼 API Key，按 [Harness 服务本地配置指南](raw/token-plan-user-guide/token-plan-guide/token-plan-overview.md#connect-harness) 配置 MCP 服务或 CLI 工具，**不消耗 Credits**。

## 限制和注意事项

- **额度独立性**：Token Plan 套餐额度、用量包、免费额度、资源包、节省计划及账户余额**相互独立**，不可交叉抵扣；`sk-` Key 仅能抵扣 Harness 权益，**不能用于抵扣模型调用额度** [用量与额度](raw/token-plan-user-guide/token-plan-guide/token-plan-usage-quota.md)。
- **额度用尽行为**：额度耗尽后调用返回 `429 insufficient_quota`，**不会自动转为按量计费**，必须等待重置、升级套餐、购买用量包或共享用量包 [Token Plan 常见问题](raw/token-plan-user-guide/token-plan-guide/token-plan-faq.md)。
- **并发与限流**：个人版档位对应建议并发数（Lite：1–2，Pro：6–8），超限将触发排队或 `429 Requests rate limit exceeded`；团队版虽无排队，但仍存在动态并发限制。
- **使用场景限制**：**严禁将 API Key 用于生产环境自动化服务、批量脚本或后台定时任务**；多人共用同一账号或 API Key 属违规行为，可能导致封禁 [权限与使用规范](raw/token-plan-user-guide/token-plan-guide/token-plan-permissions-and-usage.md)。
- **数据政策差异**：个人版对话数据用于服务改进与模型优化；团队版**不使用对话数据训练模型**。

## 来源文档

- [用量与额度](../../raw/token-plan-user-guide/token-plan-guide/token-plan-usage-quota.md)
- [Token Plan 概览](../../raw/token-plan-user-guide/token-plan-guide/token-plan-overview.md)
- [Token Plan 常见问题](../../raw/token-plan-user-guide/token-plan-guide/token-plan-faq.md)
- [权限与使用规范](../../raw/token-plan-user-guide/token-plan-guide/token-plan-permissions-and-usage.md)


