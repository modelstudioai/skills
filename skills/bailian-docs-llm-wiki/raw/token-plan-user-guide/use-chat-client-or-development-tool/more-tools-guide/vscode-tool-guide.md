# VS Code

在 VS Code 中使用阿里云百炼模型。

<a id="快速开始"></a>

<a id="quick-connect"></a>

## 快速开始

1.  1
    
    获取 API Key
    
    根据计费方案获取 API Key：
    
    -   Token Plan 个人版：[创建或查看 API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan/personal)
    -   Token Plan 团队版：[分配坐席并获取 API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/uac-admin/organization/members/list)
    -   按量计费：[百炼 API Key](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key?spm=5176.28197581.0.0.307f29a4lC7Vbh)
    -   Coding Plan：[Coding Plan API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/coding-plan)
    
2.  2
    
    打开模型管理
    
    在 VS Code 中执行 `Chat: Manage Language Models`，选择 **Add Models** > **Custom Endpoint**，协议选择 **Chat Completions**。
    
3.  3
    
    填写连接信息
    
    按向导填写组名、显示名称和所选方案的 API Key。向导会为 `apiKey` 生成安全输入引用，不要写入明文 API Key。
    
4.  4
    
    选择模型
    
    <a id="connection-reference"></a>
    
    按计费方案填写连接地址和模型：
    
    <a id="sec-tabs"></a>
    
    <a id="token-plan"></a>
    
    <a id="token-plan-h4"></a>
    
    #### Token Plan
    
    -   Base URL：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
    -   完整 `url`：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions`
    -   模型：填写[个人版](../../token-plan-personal/token-plan-personal-overview.md#tppo-h-models)或[团队版](../../token-plan-team-edition/token-plan-team-overview.md#tpto-h-models)支持的文本生成模型
    
    <a id="按量计费"></a>
    
    <a id="按量计费-h4"></a>
    
    #### 按量计费
    
    将 `{WorkspaceId}` 替换为真实的 [Workspace ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。
    
    -   Base URL：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
    -   完整 `url`：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions`
    -   模型：例如 `qwen3.8-max` 或 `qwen3.8-flash`
    
    <a id="coding-plan"></a>
    
    <a id="coding-plan-h4"></a>
    
    #### Coding Plan
    
    -   Base URL：`https://coding.dashscope.aliyuncs.com/v1`
    -   完整 `url`：`https://coding.dashscope.aliyuncs.com/v1/chat/completions`
    -   模型：例如 `qwen3.7-plus`
    
5.  5
    
    配置模型参数
    
    在 `chatLanguageModels.json` 中配置以下字段：
    
    -   `vendor`：`customendpoint`
    -   `apiType`：`chat-completions`
    -   `models[].id`：上一步的模型 ID
    -   `models[].name`：自定义显示名称
    -   `models[].url`：上一步的完整 `url`
    -   `models[].toolCalling`、`vision`、`maxInputTokens`、`maxOutputTokens`：按模型规格填写
    
    先确认方案支持该模型，再查阅[模型列表](../../../model-user-guide/get-started-with-models/models.md)；输入与输出 Token 数之和不超过模型上下文长度。字段说明见 [VS Code 官方文档](https://code.visualstudio.com/docs/agent-customization/language-models)。
    
6.  6
    
    验证
    
    在 Chat 的模型选择器中选择已配置的模型，发送“你好”。收到回复即表示接入成功。
    

<a id="常见问题"></a>

<a id="faq"></a>

## 常见问题

<a id="accordion-如何按量计费接入节省计划与资源包"></a>

如何按量计费接入节省计划与资源包？

按量计费接入方式不变，使用百炼通用 API Key 和 Base URL。购买节省计划或资源包后自动生效，调用费用按抵扣顺序自动抵扣。详情参见[节省计划与资源包](../../../model-user-guide/test-1/savings-plan-and-resource-package.md#h2-usage)。

<a id="accordion-模型未出现在-vs-code-chat-的模型选择器中"></a>

模型未出现在 VS Code Chat 的模型选择器中

保存 `chatLanguageModels.json` 后重启 VS Code，再检查模型选择器。

<a id="accordion-无法调用模型或返回-401"></a>

无法调用模型或返回 401

确认 API Key、Base URL 和模型属于同一方案。Token Plan、Coding Plan 与按量计费的 API Key 互不通用。按量计费还需确认 `{WorkspaceId}` 已替换为正确地域的 Workspace ID。

<a id="accordion-组织策略限制-byok"></a>

组织策略限制 BYOK

联系 Copilot Business / Enterprise 管理员确认 **Bring Your Own Language Model Key in VS Code** 策略。
