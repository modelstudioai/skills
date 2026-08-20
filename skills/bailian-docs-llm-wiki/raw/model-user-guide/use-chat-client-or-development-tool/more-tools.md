# 更多工具

除已列出的工具外，阿里云百炼还支持接入兼容 OpenAI / Anthropic API 协议且支持自定义服务端点的第三方编程工具。可通过按量计费、Coding Plan、Token Plan 个人版或 Token Plan 团队版接入。

## 配置接入凭证

### Token Plan 个人版

**API 协议**

**Base URL**

**API Key**

**支持模型**

OpenAI

`[https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1](https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1)`

Token Plan 个人版专属 [API Key](https://bailian.console.aliyun.com/cn-beijing?tab=plan#/efm/subscription/overview)

[支持的模型](raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)（仅文本生成类）

Anthropic

`[https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic](https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic)`

### Token Plan 团队版

**API 协议**

**Base URL**

**API Key**

**支持模型**

OpenAI

`[https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1](https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1)`

Token Plan 团队版专属 [API Key](https://bailian.console.aliyun.com/cn-beijing?tab=plan#/efm/subscription/uac-admin/organization/members/list)

[支持的模型](raw/model-user-guide/token-plan-guide/token-plan-overview.md)（仅文本生成类）

Anthropic

`[https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic](https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic)`

### Coding Plan

**API 协议**

**Base URL**

**API Key**

**支持模型**

OpenAI

`[https://coding.dashscope.aliyuncs.com/v1](https://coding.dashscope.aliyuncs.com/v1)`

Coding Plan 专属 [API Key](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/coding_plan)

[支持的模型](raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)

Anthropic

`[https://coding.dashscope.aliyuncs.com/apps/anthropic](https://coding.dashscope.aliyuncs.com/apps/anthropic)`

### 按量计费

**API 协议**

**Base URL**

**API Key**

**支持模型**

OpenAI

根据地域，填入对应 URL（请将 URL 中的 `{WorkspaceId}` 替换为真实的[获取Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#d3eb3cd37b7fu)）：

华北2（北京）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`

新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`

美国（弗吉尼亚）：`https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/compatible-mode/v1`

[阿里云百炼 API Key](raw/model-api-reference/preparations/get-api-key.md)

[支持的模型](https://help.aliyun.com/zh/model-studio/compatibility-of-openai-with-dashscope#7f9c78ae99pwz)

Anthropic

华北2（北京）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic`

新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/apps/anthropic`

[支持的模型](https://help.aliyun.com/zh/model-studio/anthropic-api-messages)

### 配置示例：Trae

Trae 支持接入自定义模型，无需安装插件即可直接配置上述任一方案的服务端点接入阿里云百炼。以下以 Trae 为例说明配置步骤：

1.  在 Trae 中前往**设置** > **模型**，单击**添加**，选择**自定义配置**。
2.  **API 格式**：根据所选服务端点的协议，选择**兼容 OpenAI**或**兼容 Anthropic**。
3.  **请求地址**：填写上表中对应方案的 Base URL。
4.  **模型 ID**：填写对应方案支持的模型名称。
5.  **API 密钥**：填写对应方案的专属 API Key。
6.  保存后，在对话框右下角的模型列表中即可选择并使用该模型。

## 不支持的工具类型

Token Plan 个人版、Token Plan 团队版和 Coding Plan 仅限在 AI 编程工具和 OpenClaw 类型 Agent 中使用，以下类型的工具**不支持**接入：

-   **工作流/自动化平台**：如 Dify、n8n、Coze 等。
-   **API 测试工具**：如 Postman、Insomnia 等。
-   **自定义应用程序**：直接在自动化脚本、应用后端代码中调用 API 等。

> 将套餐 API Key 用于允许范围之外的调用将被视为违规或滥用，可能会导致订阅被暂停或 API Key 被封禁。

## 在 IDE 中使用

如需在 VS Code 系列或 JetBrains IDE 中使用，可通过安装以下插件接入：

**插件**

**支持 IDE**

**接入文档**

**Claude Code**

VS Code、JetBrains IDE

[Claude Code](raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)

**Kilo Code**

VS Code、JetBrains IDE

[Kilo CLI](raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)

**Qwen Code**

VS Code

[Qwen Code](raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
