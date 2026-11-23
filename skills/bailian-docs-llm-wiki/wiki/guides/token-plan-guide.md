# token plan guide

Token Plan 是阿里云百炼面向开发者提供的模型订阅服务，以 Credits 为统一计量单位，支持在兼容的 AI 编程与智能体工具中交互式调用模型。它不适用于自动化脚本或后端批量调用场景，且个人版与团队版额度、API Key 和使用范围完全隔离。所有模型调用必须使用 `sk-sp-` 开头的专属 API Key，并配合 Token Plan 专用 Base URL 才能正确抵扣套餐额度。

## 支持的模型/功能

Token Plan 支持千问（Qwen）、DeepSeek、万相、月之暗面、智谱 AI、MiniMax、HappyHorse 等主流模型，但**个人版与团队版支持的模型列表不同**，需按实际套餐档位确认可用模型 ID（如 `qwen3.8-flash`、`qwen3.6-plus`）。完整支持清单见 [个人版支持的模型](https://help.aliyun.com/zh/model-studio/token-plan-personal-overview#tppo-h-models) 和 [团队版支持的模型](https://help.aliyun.com/zh/model-studio/token-plan-team-overview#tpto-h-models)。

除基础文本模型外，还支持以下扩展能力：
- **模型内置工具**：联网搜索、网页抓取、代码解释器、文搜图等，通过 Responses API 自动触发，按 Credits 抵扣；
- **多模态模型**：图像生成、视频生成、语音合成/识别、实时语音对话等，需通过工具的 Skill/Slash Command 或 Agent 扩展机制接入，**不可直接通过文本模型 Base URL 调用**；
- **Harness 权益**：仅限个人版 Standard/Pro 套餐附赠，提供 RAG、Memory、Managed Agent 等基础设施服务及 MCP 工具（如图像生成 MCP、代码解释器 MCP），使用 `sk-` 开头的百炼通用 API Key，**不消耗 Credits**，详见 [Harness 服务本地配置指南](../../raw/token-plan-user-guide/token-plan-guide/token-plan-overview.md)。

> **注意**：文档 4 中称“支持 Cursor、Claude Code、Cline 等第三方工具”，但文档 3 明确限定“仅限在编程工具和智能体工具（如 Claude Code、Cursor、Qwen Code、Qoder、OpenClaw 等）中交互式使用”，且禁止用于“自动化脚本、自定义应用程序后端”。二者无矛盾，但需强调：**兼容 ≠ 允许任意方式调用**；工具兼容性仅覆盖其原生交互流程，绕过工具封装直接调用 API 属于违规。

## 关键参数

- **API Key**：必须为 `sk-sp-` 开头的 Token Plan 专属密钥，仅用于模型调用；`sk-` 开头的百炼通用 Key 仅用于 Harness 权益，混用将导致鉴权失败或按量扣费；
- **Base URL**：必须使用 Token Plan 专用地址（非 `dashscope.aliyuncs.com`），具体配置见各工具接入指南；
- **Credits 消耗**：非等价于 Token，由输入 Token、缓存 Token、输出 Token 及模型单价共同决定。例如 `qwen3.6-plus` 单次请求中，8,349 输入 Token + 40,794 缓存 Token + 573 输出 Token ≈ 消耗 3.18 Credits；
- **并发限制**：个人版按档位建议并发数（Lite: 1–2，Pro: 6–8），超限将触发 `429 Requests rate limit exceeded`；团队版存在动态并发上限，不支持手动提升；
- **夜间折扣**：个人版与团队版在每日 22:00–08:00 对部分模型提供 Credits 折扣，具体模型与折扣率以控制台为准。

## 使用方式

1. **获取凭证**：在 [百炼控制台 Token Plan 页面](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan) 购买套餐并生成 `sk-sp-` API Key；
2. **配置工具**：按所用工具选择对应接入方式。例如：
   - Claude Code / Codex / Qwen Code / OpenClaw / Hermes Agent：执行 CLI 配置命令（见 [Token Plan 概览](../../raw/token-plan-user-guide/token-plan-guide/token-plan-overview.md)）；
   - Qoder / Trae / DeepSeek Harness / WorkBuddy：参考各工具专属接入文档；
   - 其他支持自定义 Base URL 的工具：手动填入 `sk-sp-xxx` 和 Token Plan Base URL；
3. **调用模型**：在工具内通过自然语言指令、Slash Command 或 Agent 启动交互式任务；
4. **调用 Harness 服务**（仅 Standard/Pro）：使用 `sk-` Key 配置 MCP 服务（如 `https://dashscope.aliyuncs.com/api/v1/mcps/TextGenerateImage/mcp`），或通过 `bl knowledge` / `bl memory` 等 CLI 命令调用基础设施服务，详见 [Harness 服务本地配置指南](../../raw/token-plan-user-guide/token-plan-guide/token-plan-overview.md)。

## 限制和注意事项

- **使用范围限制**：仅限交互式开发场景（如编码辅助、内容创作、数据处理），**严禁用于生产环境自动化服务、后台定时任务、批量脚本或自定义应用后端**。违规可能导致订阅暂停或 API Key 封禁；
- **账号与权限**：RAM 子账号需主账号授予 `AliyunTokenPlanFullAccess` + `AliyunBSSReadOnlyAccess`（个人版）或 `AliyunBSSFullAccess`（团队版），否则“我的订阅”页面可能为空；
- **额度独立性**：Token Plan 套餐额度、免费额度、资源包、账户余额相互独立；`sk-sp-` Key 无法抵扣按量费用，`sk-` Key 无法抵扣模型调用额度；
- **升级与降配**：支持按剩余天数折算补差升级（公式见 [用量与额度](../../raw/token-plan-user-guide/token-plan-guide/token-plan-usage-quota.md)），但**不支持降配**；
- **退订规则**：个人版暂不支持退订；团队版可按坐席维度退订，已消耗坐席不可退款；
- **数据政策**：个人版输入与输出内容将用于服务优化；团队版**不用于模型训练**；
- **设备与共享**：同一 `sk-sp-` Key 可配置于本人多台设备，但**不可共享给他人**，亦不可多人共用同一账号；
- **用量监控**：务必通过 [控制台用量分析](https://bailian.console.aliyun.com/cn-beijing/subscription/overview) 查看实际 Credits 消耗，第三方工具显示的 Token 数≠实际 Credits，因系统提示词、工具 Schema、多轮历史等均计入 Credits。

## 来源文档

- [Token Plan 概览](../../raw/token-plan-user-guide/token-plan-guide/token-plan-overview.md)
- [用量与额度](../../raw/token-plan-user-guide/token-plan-guide/token-plan-usage-quota.md)
- [权限与使用规范](../../raw/token-plan-user-guide/token-plan-guide/token-plan-permissions-and-usage.md)
- [Token Plan 常见问题](../../raw/token-plan-user-guide/token-plan-guide/token-plan-faq.md)


