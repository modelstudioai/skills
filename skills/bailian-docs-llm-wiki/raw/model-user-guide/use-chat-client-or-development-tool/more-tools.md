# 更多工具

除已列出的工具外，阿里云百炼还支持接入兼容 OpenAI / Anthropic API 协议且支持自定义服务端点的第三方编程工具。可通过按量计费、Coding Plan 或 Token Plan 团队版接入。

## **配置接入凭证**

### Token Plan 团队版

**API 协议**

**Base URL**

**API Key**

**支持模型**

OpenAI

`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`

Token Plan 团队版专属 [API Key](https://bailian.console.aliyun.com/?tab=plan#/efm/subscription/overview)

[支持的模型](https://help.aliyun.com/zh/model-studio/token-plan-overview)（仅文本生成类）

Anthropic

`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`

### Coding Plan

**API 协议**

**Base URL**

**API Key**

**支持模型**

OpenAI

`https://coding.dashscope.aliyuncs.com/v1`

Coding Plan 专属 [API Key](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/coding_plan)

[支持的模型](https://help.aliyun.com/zh/model-studio/coding-plan)

Anthropic

`https://coding.dashscope.aliyuncs.com/apps/anthropic`

### 按量计费

**API 协议**

**Base URL**

**API Key**

**支持模型**

OpenAI

华北2（北京）：`https://dashscope.aliyuncs.com/compatible-mode/v1`

新加坡：`https://dashscope-intl.aliyuncs.com/compatible-mode/v1`

美国（弗吉尼亚）：`https://dashscope-us.aliyuncs.com/compatible-mode/v1`

[阿里云百炼 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)

[支持的模型](https://help.aliyun.com/zh/model-studio/compatibility-of-openai-with-dashscope#7f9c78ae99pwz)

Anthropic

华北2（北京）：`https://dashscope.aliyuncs.com/apps/anthropic`

新加坡：`https://dashscope-intl.aliyuncs.com/apps/anthropic`

[支持的模型](https://help.aliyun.com/zh/model-studio/anthropic-api-messages#ae1b2c3d4e5f6)

## **不支持的工具类型**

Token Plan 团队版和 Coding Plan 仅限在 AI 编程工具和 OpenClaw 类型 Agent 中使用，以下类型的工具**不支持**接入：

-   **工作流/自动化平台**：如 Dify、n8n、Coze 等。
    
-   **API 测试工具**：如 Postman、Insomnia 等。
    
-   **自定义应用程序**：直接在自动化脚本、应用后端代码中调用 API 等。
    

> 将套餐 API Key 用于允许范围之外的调用将被视为违规或滥用，可能会导致订阅被暂停或 API Key 被封禁。

## **在 IDE 中使用**

**说明**

部分编程工具（如通义灵码个人版、Cursor 免费版、Trae）不支持接入自定义服务端点，无法直接使用 Token Plan 团队版或 Coding Plan。

如需在 VS Code 系列（Cursor、Trae 等）或 JetBrains IDE（IDEA、PyCharm 等）中使用，可通过安装以下插件接入：

**插件**

**支持 IDE**

**接入文档**

**Claude Code**

VS Code、JetBrains IDE

[Claude Code](https://help.aliyun.com/zh/model-studio/claude-code)

**Kilo Code**

VS Code、JetBrains IDE

[Kilo CLI](https://help.aliyun.com/zh/model-studio/kilo-cli)

**Qwen Code**

VS Code

[Qwen Code](https://help.aliyun.com/zh/model-studio/qwen-code)
