# qwen4-max-preview（最新模型）

了解 Qwen4-Max-Preview 的多模态理解、深度思考、工具调用能力与 Token Plan 接入方式

Qwen4-Max-Preview 是通义千问新一代旗舰多模态模型，融合文本生成、图片与视频理解及深度思考能力，适用于编程开发、办公、前端设计与复杂智能体任务。模型支持联网搜索、工具调用和结构化输出，兼容 OpenAI 与 Anthropic API，帮助开发者构建具备多模态理解与任务执行能力的智能应用。

Model ID：`qwen4-max-preview`

**说明**Qwen4-Max-Preview 当前为预览版，仅支持 Token Plan，不支持按量计费。预览期为 2026 年 11 月 11 日 10:00 至 11 月 25 日 24:00（UTC+8），期间不做变更，预览结束后下线。

## 模型能力与规格

能力

说明

文本生成与深度思考

默认开启思考，可通过 `reasoning_effort` 调节推理力度

图片与视频理解

支持文本、图片和视频输入，适用于截图分析、文档理解与视频分析

工具调用

支持 Function Calling、联网搜索及内置工具

结构化输出

支持 JSON Object 与 JSON Schema

API 兼容性

兼容 OpenAI Chat Completions、Responses 和 Anthropic Messages API

参数

值

上下文长度

1M Token

最大输出长度

393,216 Token，思考与最终回答共享此预算

## 快速接入

通过 [Token Plan](https://help.aliyun.com/zh/model-studio/token-plan-overview) 接入 Qwen4-Max-Preview：

1.  选择 [Token Plan 个人版](https://help.aliyun.com/zh/model-studio/token-plan-personal-overview) 或 [Token Plan 团队版](https://help.aliyun.com/zh/model-studio/token-plan-team-overview)，按对应指南获取套餐专用 API Key。
2.  使用套餐专用 Base URL：`https://token-plan.cn-beijing.maas.aliyuncs.com`。各协议的完整接入地址见 Token Plan 指南。
3.  将模型 ID 设置为 `qwen4-max-preview`。

套餐支持的客户端、配置步骤与 Credits 权益均见 Token Plan 指南。

## 使用注意事项

**说明****输出预算变化（OpenAI Chat Completions）**：自 `qwen4-max-preview` 起，`max_tokens` 与 `max_completion_tokens` 等价，均限制思考内容与最终回答的 Token 总量。开启思考时，思考内容会占用同一预算；迁移时沿用仅为回答预留的上限，可能导致输出提前截断，请为思考与回答共同预留额度。此前已上线的 Qwen 模型行为不变。详见 [API 兼容性升级说明](https://help.aliyun.com/zh/model-studio/api-compatibility-upgrade-notice)。

-   **思考模式**：默认开启，可选择 `low`、`medium` 或 `xhigh`（默认）。`reasoning_effort` 和 `thinking_budget` 不能同时设置。详见 [深度思考](raw/model-user-guide/model-experience/text-generation-model/deep-thinking.md)。
-   **多轮对话**：Chat Completions 的 `preserve_thinking` 默认开启，需在历史 assistant 消息的 `reasoning_content` 字段中完整回传思考内容，不支持拼接到 `content` 字段。
-   **多模态与工具调用**：图片和视频输入见 [图像与视频理解](raw/model-user-guide/model-experience/text-generation-model/vision.md)；工具定义与调用流程见 [函数调用](raw/model-user-guide/model-experience/text-generation-model/tool-calls/qwen-function-calling.md)；输出格式见 [结构化输出](raw/model-user-guide/model-experience/text-generation-model/qwen-structured-output.md)。
