# coding plan guide

Coding Plan 是面向开发者的一站式 AI 编程订阅服务，通过固定月费模式提供确定性成本与额度保障，专为交互式编程工具（如 Claude Code、Qoder、OpenClaw 等）设计。它不支持 API 直接调用，所有请求必须经由兼容的客户端工具发起，并严格使用专属 API Key 与 Base URL 才能正确抵扣套餐额度。详细背景与定位请参见 [Coding Plan概述](../../raw/token-plan-user-guide/coding-plan-guide/coding-plan.md)。

## 支持的模型/功能

Coding Plan Pro 套餐当前**仅支持以下精确模型版本**（区分大小写，不可混用别名或旧版 ID）：

- **推荐模型（均支持图片理解）**：`qwen3.7-plus`、`qwen3.6-plus`、`kimi-k2.5`、`glm-5`、`MiniMax-M2.5`  
- **额外支持**：`qwen3.5-plus`（支持图片理解）

> **注意**：文档 1 中称 Lite 套餐“支持所有套餐模型”，但该套餐已于 2026 年 3 月 20 日起停止新购、4 月 13 日起停止续费与升级，**当前仅 Pro 套餐有效**，Lite 相关描述已过时，实际可用模型以 Pro 套餐列表为准（详见 [Coding Plan概述](../../raw/token-plan-user-guide/coding-plan-guide/coding-plan.md)）。

所有支持模型默认启用深度思考（Thinking Mode），具体开启方式因工具而异：
- **Claude Code**：执行 `/config` → 切换 `Thinking mode` 为 `true`，快捷键 `Ctrl + O` 查看过程  
- **OpenCode**：在 `opencode.json` 中配置 `"thinking": { "type": "enabled", "budgetTokens": N }`  
- **Qwen Code**：在 `~/.qwen/settings.json` 的 `generationConfig.extra_body` 中设 `"enable_thinking": true`  
- **OpenClaw**：需 v2026.03.02+ 版本，在模型配置中设 `"reasoning": true` 并指定 `"compat": {"thinkingFormat": "qwen"}`  

完整工具接入指南与配置示例见 [Coding Plan 常见问题](../../raw/token-plan-user-guide/coding-plan-guide/coding-plan-faq.md)。

## 关键参数

| 参数 | 说明 | 值/范围 |
|------|------|---------|
| **API Key** | Coding Plan 专用密钥，格式为 `sk-sp-xxxxx` | 必须从 [Coding Plan 页面](https://bailian.console.aliyun.com/cn-beijing/subscription/coding-plan) 获取，**不可与百炼通用 `sk-xxxxx` 混用** |
| **Base URL** | 必须匹配所选协议：<br>• OpenAI 兼容：`https://coding.dashscope.aliyuncs.com/v1`<br>• Anthropic 兼容：`https://coding.dashscope.aliyuncs.com/apps/anthropic` | 错误使用百炼通用 Base URL（如 `dashscope.aliyuncs.com`）将导致按量扣费（见 [Coding Plan概述](../../raw/token-plan-user-guide/coding-plan-guide/coding-plan.md)） |
| **额度限制** | 三级滚动配额，独立计算：<br>• **每 5 小时**：6,000 次请求（每分钟自动释放 5 小时前用量）<br>• **每周**：45,000 次请求（每周一 00:00:00 UTC+08 重置）<br>• **每月**：90,000 次请求（订阅日当日 00:00:00 UTC+08 重置） | 超额报错示例：<br>`hour allocated quota exceeded` / `week allocated quota exceeded` / `month allocated quota exceeded`（详见 [Coding Plan 常见问题](../../raw/token-plan-user-guide/coding-plan-guide/coding-plan-faq.md)） |
| **并发限制** | 平台动态分配，无固定数值 | 触发 `concurrency allocated quota exceeded` 时等待后重试即可 |

## 使用方式

1. **订阅套餐**：访问 [Coding Plan 购买页](https://common-buy.aliyun.com/coding-plan) 订购 Pro 套餐（Lite 已停售）；RAM 子账号需主账号授权管理员权限后方可订阅。  
2. **获取凭证**：在 [Coding Plan 页面](https://bailian.console.aliyun.com/cn-beijing/subscription/coding-plan) 获取 `sk-sp-xxxxx` API Key 及对应 Base URL。  
3. **配置工具**：根据所选工具文档（如 [Claude Code](../use-chat-client-or-development-tool/claude-code.md)、[OpenCode](../use-chat-client-or-development-tool/opencode.md) 等），填入上述 Key 与 URL。  
4. **启动使用**：在工具内新建会话并开始交互式编程。  

> **注意**：首次使用建议通过 [阿里云 AI 助理](https://www.aliyun.com/ai-assistant/) 查询报错（如 `model 'xxx' is not supported`），其知识库可精准定位模型名错误、URL 配置偏差等常见问题（参考 [Coding Plan 常见问题](../../raw/token-plan-user-guide/coding-plan-guide/coding-plan-faq.md)）。

## 限制和注意事项

- **严禁 API 直接调用**：仅限在官方支持的交互式编程工具中使用（如 Claude Code、Qoder、OpenClaw 等）。禁止用于自动化脚本、自定义后端或批量非交互场景。违规将导致订阅暂停或 API Key 封禁。  
- **额度消耗规则**：单次提问按“模型调用次数”扣减，简单任务约 5–10 次，复杂任务约 10–30+ 次，受任务难度、上下文长度及工具调用影响。  
- **地域与网络**：全球可用，但海外用户若遇延迟，可优先选用 Model Studio Coding Plan（见 [Coding Plan 常见问题](../../raw/token-plan-user-guide/coding-plan-guide/coding-plan-faq.md)）。  
- **数据授权**：输入与生成内容将用于服务优化；停止使用后，新数据授权终止，但历史数据授权不可撤回（详见阿里云百炼服务协议第 5.2 条）。  
- **不支持退款**：订阅前请确认需求，服务一经开通概不退费。  
- **模型上下文限制**：各模型有最大输入/输出 [Token](../concepts/token.md) 限制（如 `glm-5` 最大 `thinking_budget` 为 32,768），超限将报 `Request Entity Too Large` 或 `InternalError.Algo.InvalidParameter`，需精简输入或调整配置（详见 [Coding Plan 常见问题](../../raw/token-plan-user-guide/coding-plan-guide/coding-plan-faq.md)）。

## 来源文档

- [Coding Plan概述](../../raw/token-plan-user-guide/coding-plan-guide/coding-plan.md)
- [Coding Plan 常见问题](../../raw/token-plan-user-guide/coding-plan-guide/coding-plan-faq.md)


