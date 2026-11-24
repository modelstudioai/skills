# coding plan guide

Coding Plan 是面向开发者的一站式 AI 编程订阅服务，通过固定月费模式提供稳定、可控的模型调用额度，专为交互式编程工具设计。它不支持 API 直接调用，仅限在认证的开源/商业编程客户端中使用，以保障服务稳定性与资源公平性。所有套餐均使用独立的 `sk-sp-` 开头 API Key 和专属 Base URL，与百炼按量计费体系完全隔离。

## 支持的模型与功能

Coding Plan Pro 套餐当前**仅支持以下精确模型版本**（区分大小写，严格匹配）：

- **推荐模型**：`qwen3.7-plus`（支持图片理解）、`qwen3.6-plus`（支持图片理解）、`kimi-k2.5`（支持图片理解）、`glm-5`、`MiniMax-M2.5`  
- **更多模型**：`qwen3.5-plus`（支持图片理解）

> **注意**：文档 1 中称 Lite 套餐“支持所有套餐模型”，但文档 1 同时明确说明 Lite 套餐已于 **2026 年 4 月 13 日起停止续费与升级**，且当前已不可新购；因此实际可用模型仅限 Pro 套餐所列。Lite 的兼容性描述已失效，开发者应以 [Coding Plan概述](../../raw/token-plan-user-guide/coding-plan-guide/coding-plan.md) 中 Pro 套餐模型列表为准。

所有支持模型默认启用深度思考（reasoning）能力。不同工具开启方式各异：
- **Claude Code**：执行 `/config` → 切换 `Thinking mode` 为 `true`，快捷键 `Ctrl + O` 查看过程  
- **OpenCode**：在 `opencode.json` 中配置 `thinking.type: "enabled"` 及合理 `budgetTokens` 值（参考各模型上限）  
- **Qwen Code**：在 `~/.qwen/settings.json` 的 `generationConfig.extra_body` 中设置 `"enable_thinking": true`  
- **OpenClaw**：需在模型配置中同时启用 `"reasoning": true` 和 `"compat": {"thinkingFormat": "qwen"}`，并确保模型 ID 带 `bailian/` 前缀（详见 [OpenClaw](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/openclaw.md)）

## 关键参数

| 参数类型 | 值 | 说明 |
|----------|----|------|
| **API Key 格式** | `sk-sp-xxxxx` | 必须使用 Coding Plan 专属 Key，**不可混用**百炼通用 Key（`sk-xxxxx`）；复制时需确保无空格或换行 |
| **Base URL（OpenAI 兼容）** | `https://coding.dashscope.aliyuncs.com/v1` | 用于 Qwen Code、OpenCode、Cursor 等 OpenAI 协议工具 |
| **Base URL（Anthropic 兼容）** | `https://coding.dashscope.aliyuncs.com/apps/anthropic` | 用于 Claude Code、Hermes Agent 等 Anthropic 协议工具 |
| **5 小时额度** | 6,000 次请求 | 滚动恢复：每分钟释放 5 小时前消耗的额度（例：10:00 消耗 100 次，15:00 自动恢复） |
| **每周额度** | 45,000 次请求 | 每周一 00:00:00（UTC+08:00）重置 |
| **每月额度** | 90,000 次请求 | 在订阅日次月同一时刻重置 |

额度消耗按“模型调用次数”计费，非按 token。简单任务约 5–10 次，复杂任务约 10–30+ 次，受上下文长度、工具调用频次影响。实时用量可在 [Coding Plan 页面](https://bailian.console.aliyun.com/cn-beijing/subscription/coding-plan) 查看。

## 使用方式

1. **订阅服务**  
   主账号直接访问 [Coding Plan 购买页](https://common-buy.aliyun.com/coding-plan) 订购；RAM 子账号需由主账号在 [权限管理](https://bailian.console.aliyun.com/cn-beijing/model/settings/permission) 中授予**管理员权限**后方可订阅。

2. **获取凭证**  
   订阅成功后，在 [Coding Plan 页面](https://bailian.console.aliyun.com/cn-beijing/subscription/coding-plan) 获取 `sk-sp-xxxxx` Key 和对应 Base URL。

3. **接入工具**  
   将 Key 与 Base URL 配置至支持的编程工具。完整兼容工具列表见 [Coding Plan概述](../../raw/token-plan-user-guide/coding-plan-guide/coding-plan.md)，包括 OpenClaw、Hermes Agent、Claude Code、OpenCode、Cursor、Qwen Code 等。配置错误是常见报错主因（如 401/403/404），请严格对照工具文档操作。

4. **验证与调试**  
   推荐使用 [阿里云 AI 助理](https://www.aliyun.com/ai-assistant/) 提问排查问题，例如：“使用coding plan时，报错model 'xxx' is not [support](support.md)ed是什么原因”。该助手可结合官方文档精准定位模型名错误、URL 配置错位等典型问题（参见 [Coding Plan 常见问题](../../raw/token-plan-user-guide/coding-plan-guide/coding-plan-faq.md)）。

## 限制和注意事项

- **严禁 API 直接调用**：仅限在交互式编程客户端中使用。禁止用于自动化脚本、自定义后端服务或任何非交互式批量场景。违规将导致订阅暂停或 Key 封禁。  
- **额度超限响应**：  
  - `hour allocated quota exceeded` → 等待 5 小时滚动恢复  
  - `week/month allocated quota exceeded` → 分别等待周一 00:00 或订阅日 00:00 重置  
  - `concurrency allocated quota exceeded` / `429 usage allocated quota exceeded` → 降低请求频率，避免短时高负载；确认 Key 未被共享  
- **模型调用约束**：  
  - 必须使用文档明确列出的模型 ID，拼写、大小写、空格均敏感；`qwen-portal/coder-model` 等非百炼模型**不支持**（见 [Coding Plan 常见问题](../../raw/token-plan-user-guide/coding-plan-guide/coding-plan-faq.md)）  
  - OpenClaw 等多 provider 工具需显式配置 `bailian/` 前缀及 `models.providers.bailian` 结构，否则触发 `Unknown model` 或 `No API key found for provider` 错误  
- **地域与网络**：全球可用，但需确保客户端能直连 `coding.dashscope.aliyuncs.com`。海外用户若遇连接中断（`Connection closed mid-response`），应检查本地代理是否拦截或转发失败。  
- **数据授权**：输入与输出内容将用于服务优化；停用服务后终止后续授权，但已授权数据不追溯撤销（详见 [Coding Plan概述](../../raw/token-plan-user-guide/coding-plan-guide/coding-plan.md) 订阅前须知第 2 条）。  
- **不支持退款**：订阅前请充分评估需求。

## 来源文档

- [Coding Plan概述](../../raw/token-plan-user-guide/coding-plan-guide/coding-plan.md)
- [Coding Plan 常见问题](../../raw/token-plan-user-guide/coding-plan-guide/coding-plan-faq.md)


