# coding plan guide

Coding Plan 是面向开发者的一站式 AI 编程订阅服务，通过固定月费提供确定性成本与额度保障，专为本地 AI 编程工具（如 Claude Code、OpenCode、Qwen Code 等）设计。它不支持直接 API 调用，仅限交互式编程场景使用，且需严格使用专属 API Key 与 Base URL 才能正确抵扣套餐额度。服务当前仅提供 Pro 套餐，Lite 套餐已全面停止新购与续费。

## 支持的模型/功能

- **支持模型（Pro 套餐）**：仅限以下精确版本（区分大小写，前后无空格）：
  - 推荐模型：`qwen3.7-plus`（支持图片理解）、`qwen3.6-plus`（支持图片理解）、`kimi-k2.5`（支持图片理解）、`glm-5`、`MiniMax-M2.5`
  - 其他可用模型：`qwen3.5-plus`（支持图片理解）
- **核心功能**：
  - 多模型统一接入：兼容 OpenAI / Anthropic 协议，适配主流开源编程工具。
  - 深度思考模式（Reasoning Mode）：`qwen3.7-plus`、`qwen3.6-plus`、`kimi-k2.5`、`glm-5` 等均原生支持；需在对应工具中显式启用（如 `/config` 切换或配置 `enable_thinking: true`），详见 [Coding Plan 常见问题](../../raw/token-plan-user-guide/coding-plan-guide/coding-plan-faq.md)。
  - 图片理解能力：仅限标注“支持图片理解”的模型（如 `qwen3.7-plus`），需工具端支持多模态输入。

> **注意**：文档 1 中称“Lite 套餐支持所有套餐模型”，但 Lite 套餐已于 2026 年 4 月 13 日起完全停止续费与升级，当前无有效 Lite 订阅；所有新用户及续订用户均须使用 Pro 套餐，其模型列表以本文档“支持模型”为准。该信息已在 [Coding Plan概述](../../raw/token-plan-user-guide/coding-plan-guide/coding-plan.md) 中明确说明。

## 关键参数

| 参数 | 说明 | 取值/范围 |
|------|------|-----------|
| **API Key** | Coding Plan 专用密钥，格式为 `sk-sp-xxxxx` | 必须从 [Coding Plan 页面](https://bailian.console.aliyun.com/cn-beijing/subscription/coding-plan) 获取，**不可复用百炼通用 `sk-xxxxx` Key** |
| **Base URL** | 协议兼容入口，决定请求路由与额度归属 | OpenAI 兼容：`https://coding.dashscope.aliyuncs.com/v1`<br>Anthropic 兼容：`https://coding.dashscope.aliyuncs.com/apps/anthropic` |
| **额度周期** | 三重滚动/重置机制，独立计费 | • 每 5 小时：滚动恢复（每分钟释放 5 小时前用量）<br>• 每周：周一 00:00:00（UTC+08:00）重置<br>• 每月：订阅日 00:00:00（UTC+08:00）重置 |
| **额度总量（Pro）** | 每周期上限，超限返回 `quota exceeded` 错误 | • 每 5 小时：6,000 次<br>• 每周：45,000 次<br>• 每月：90,000 次 |
| **并发限制** | 动态分配，非固定值 | 触发 `concurrency allocated quota exceeded` 时需等待后重试 |

## 使用方式

1. **订阅服务**  
   访问 [Coding Plan 购买页](https://common-buy.aliyun.com/coding-plan) 完成 Pro 套餐购买。RAM 子账号需由主账号在 [权限管理](https://bailian.console.aliyun.com/cn-beijing/model/settings/permission) 中授予**管理员**权限后方可订阅。

2. **获取凭证**  
   在 [Coding Plan 页面](https://bailian.console.aliyun.com/cn-beijing/subscription/coding-plan) 获取 `sk-sp-xxxxx` API Key 与对应 Base URL。务必确认 Key 以 `sk-sp-` 开头，Base URL 含 `coding.dashscope.aliyuncs.com` —— 混用百炼通用 Key/URL 将导致按量扣费，详见 [Coding Plan概述](../../raw/token-plan-user-guide/coding-plan-guide/coding-plan.md)。

3. **配置工具**  
   根据所用工具选择协议与 Base URL：
   - OpenAI 兼容工具（如 OpenCode、Qwen Code、Cursor）→ 配置 `https://coding.dashscope.aliyuncs.com/v1`
   - Anthropic 兼容工具（如 Claude Code）→ 配置 `https://coding.dashscope.aliyuncs.com/apps/anthropic`  
   具体配置步骤参见各工具文档，例如 [OpenCode](../use-chat-client-or-development-tool/opencode.md)、[Claude Code](../use-chat-client-or-development-tool/claude-code.md)。

4. **启用高级功能**  
   - **思考模式**：需在工具配置中显式开启（如 Qwen Code 修改 `~/.qwen/settings.json` 的 `enable_thinking`；OpenCode 设置 `thinking.budgetTokens`；Claude Code 执行 `/config`）。预算值须符合模型上限（如 `glm-5` 最大 `budgetTokens=32768`），详见 [Coding Plan 常见问题](../../raw/token-plan-user-guide/coding-plan-guide/coding-plan-faq.md)。
   - **上下文管理**：若遇 `Request Entity Too Large` 或 `max_tokens` 超限，可通过 `/new` 新建会话、`/compact` 压缩历史，或调整 `limit.output` 配置。

## 限制和注意事项

- **严禁 API 直接调用**：Coding Plan 仅限在官方支持的交互式编程工具中使用（如 [Claude Code](../use-chat-client-or-development-tool/claude-code.md)、[Qoder](../use-chat-client-or-development-tool/qoder-agent.md)、[OpenClaw](../use-chat-client-or-development-tool/openclaw.md) 等）。禁止用于自动化脚本、自定义后端服务或任何非交互式批量调用——违规将导致订阅暂停或 API Key 封禁。
- **数据授权**：输入与生成内容将用于服务优化，终止使用后不再新增授权，但已授权数据不溯及既往。条款详见 [阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html) 第 5.2 条。
- **账号与共享**：套餐为订阅人专享，禁止共享账号或 API Key。共享可能导致额度异常消耗、触发限流（如 `429 usage allocated quota exceeded`）或服务受限。
- **地域与网络**：全球可用，但需确保客户端可稳定访问 `coding.dashscope.aliyuncs.com`。海外用户若遇连接问题，可尝试切换 DNS 或关闭代理；`Connection closed mid-response` 类错误多因本地网络/代理不稳定导致，建议排查后重试。
- **额度消耗逻辑**：单次提问按“模型调用次数”扣减，非按 Token 计费。简单任务约 5–10 次，复杂任务约 10–30+ 次，实际受任务难度、上下文长度及工具调用链影响。实时用量可在 [Coding Plan 页面](https://bailian.console.aliyun.com/cn-beijing/subscription/coding-plan) 查看。

## 来源文档

- [Coding Plan概述](../../raw/token-plan-user-guide/coding-plan-guide/coding-plan.md)
- [Coding Plan 常见问题](../../raw/token-plan-user-guide/coding-plan-guide/coding-plan-faq.md)


