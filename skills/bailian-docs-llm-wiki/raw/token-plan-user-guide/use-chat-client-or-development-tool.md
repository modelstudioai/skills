# 接入AI工具

把 Token Plan 接入主流 AI 编程和智能体工具，包括通用 Base URL 和 API Key 配置。

<a id="选择工具"></a>

## 选择工具

-   [Qoder](use-chat-client-or-development-tool/qoder-agent.md)
-   [Claude Code](use-chat-client-or-development-tool/claude-code.md)
-   [Codex](use-chat-client-or-development-tool/codex.md)
-   [Qwen Code](use-chat-client-or-development-tool/qwen-code.md)
-   [OpenClaw](use-chat-client-or-development-tool/openclaw.md)
-   [Hermes Agent](use-chat-client-or-development-tool/hermes-agent.md)
-   [OpenCode](use-chat-client-or-development-tool/opencode.md)
-   [Trae](use-chat-client-or-development-tool/trae-tool-guide.md)
-   [DeepSeek Harness](use-chat-client-or-development-tool/deepseek-harness.md)
-   [WorkBuddy](use-chat-client-or-development-tool/workbuddy.md)
-   [更多工具](use-chat-client-or-development-tool/more-tools-guide.md)

<a id="通用配置"></a>

<a id="tpa-h-config"></a>

## 通用配置

工具支持手动填写 Base URL 时，按协议选择：

| 协议 | Base URL |
| --- | --- |
| OpenAI 兼容 | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| Anthropic 兼容 | `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` |

Token Plan 专属 API Key 以 `sk-sp-` 开头，仅在生成时完整显示一次。

> **重要**
>
> Token Plan、Coding Plan 和按量付费的 API Key 与 Base URL 相互隔离，必须配套使用。
>
> -   **Token Plan**：`sk-sp-` 开头的 API Key + 上方表格中的 Base URL。
> -   **Coding Plan**：Coding Plan API Key + `https://coding.dashscope.aliyuncs.com/v1`。
> -   **按量付费**：百炼 API Key（`sk-` 开头）+ `https://dashscope.aliyuncs.com/compatible-mode/v1`。
>
> 如果购买了 Token Plan 但使用了百炼 API Key 或其他计费模式的 Base URL，调用会走按量计费通道产生扣费，或返回 401/403 鉴权错误。
