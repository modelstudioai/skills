# 通用接入指南

在兼容 OpenAI 或 Anthropic API 的第三方工具中接入阿里云百炼。

## 快速开始

1.  1
    
    获取 API Key
    
    根据计费方案获取 API Key：
    
    -   Token Plan 个人版：[创建或查看 API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan/personal)
    -   Token Plan 团队版：[分配坐席并获取 API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/uac-admin/organization/members/list)
    -   按量计费：[百炼 API Key](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key?spm=5176.28197581.0.0.307f29a4lC7Vbh)
    -   Coding Plan：[Coding Plan API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/coding-plan)
    
2.  2
    
    选择协议和 Base URL
    
    在工具的自定义模型设置中选择协议，并填写对应 Base URL。OpenAI 协议使用 `compatible-mode/v1` 或 `/v1` 地址，Anthropic 协议使用 `/apps/anthropic` 地址。
    
    #### Token Plan
    
    -   OpenAI Base URL：`[https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1](https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1)`
    -   Anthropic Base URL：`[https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic](https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic)`
    
    #### 按量计费
    
    将 `{WorkspaceId}` 替换为真实的 [Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。
    
    -   OpenAI Base URL：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
    -   Anthropic Base URL：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic`
    
    #### Coding Plan
    
    -   OpenAI Base URL：`[https://coding.dashscope.aliyuncs.com/v1](https://coding.dashscope.aliyuncs.com/v1)`
    -   Anthropic Base URL：`[https://coding.dashscope.aliyuncs.com/apps/anthropic](https://coding.dashscope.aliyuncs.com/apps/anthropic)`
    
3.  3
    
    填写模型
    
    按计费方案填写模型 ID：
    
    -   Token Plan：填写[个人版](https://help.aliyun.com/zh/model-studio/token-plan-personal-overview#tppo-h-models)或[团队版](https://help.aliyun.com/zh/model-studio/token-plan-team-overview#tpto-h-models)支持的文本生成模型
    -   按量计费：例如 `qwen3.8-max` 或 `qwen3.8-flash`
    -   Coding Plan：填写[支持的文本生成模型](raw/token-plan-user-guide/coding-plan-guide/coding-plan.md)
    
4.  4
    
    验证
    
    发送一条测试消息。收到模型回复即表示接入成功。
    

## 不支持的工具类型

Token Plan 个人版、Token Plan 团队版和 Coding Plan 仅限在 AI 编程工具和 OpenClaw 类型 Agent 中使用，以下类型的工具**不支持**接入：

-   **工作流/自动化平台**：如 Dify、n8n、Coze 等。
-   **API 测试工具**：如 Postman、Insomnia 等。
-   **自定义应用程序**：直接在自动化脚本、应用后端代码中调用 API 等。

将套餐 API Key 用于允许范围之外的调用可能被视为违规或滥用，导致订阅暂停或 API Key 被封禁。
