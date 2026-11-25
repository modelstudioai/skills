# Chatbox

在 Chatbox 中使用阿里云百炼模型。

<a id="快速开始"></a>

<a id="cb-config-h"></a>

<a id="cb-config"></a>

## 快速开始

1.  1
    
    获取 API Key
    
    根据计费方案获取对应的 API Key：
    
    -   Token Plan 个人版：[创建或查看 API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan/personal)
    -   Token Plan 团队版：[分配坐席并获取 API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/uac-admin/organization/members/list)
    -   按量计费：[百炼 API Key](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key?spm=5176.28197581.0.0.307f29a4lC7Vbh)
    -   Coding Plan：[Coding Plan API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/coding-plan)
    
2.  2
    
    配置模型
    
    在 Chatbox 中点击左下角的 **设置**，点击 **模型提供方**，点击底部的 **添加**。填写 **名称**，**API 模式** 选择 **OpenAI API 兼容**，点击 **添加**。按计费方案填写配置：
    
    <a id="sec-tabs"></a>
    
    <a id="token-plan"></a>
    
    <a id="token-plan-h4"></a>
    
    #### Token Plan
    
    <a id="cb-tpp-config-h"></a>
    
    <a id="cb-tpp-config"></a>
    
    <a id="cb-tp-config-h"></a>
    
    <a id="cb-tp-config"></a>
    
    | 配置项 | 值 |
    | --- | --- |
    | API 主机 | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
    | API 密钥 | Token Plan 个人版或团队版专属 API Key |
    | 模型 | 填写[个人版](../../token-plan-personal/token-plan-personal-overview.md#tppo-h-models)或[团队版](../../token-plan-team-edition/token-plan-team-overview.md#tpto-h-models)支持的文本生成模型 |
    
    <a id="按量计费"></a>
    
    <a id="按量计费-h4"></a>
    
    #### 按量计费
    
    <a id="cb-payg-config-h"></a>
    
    <a id="cb-payg-config"></a>
    
    按实际调用量后付费。将 `{WorkspaceId}` 替换为 [Workspace ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)，以下以华北2（北京）为例。
    
    | 配置项 | 值 |
    | --- | --- |
    | API 主机 | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
    | API 密钥 | 百炼 API Key |
    | 模型 | `qwen3.8-max` 或 `qwen3.8-flash`；可用模型见 [OpenAI 兼容接口支持的模型](../../../model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md#7f9c78ae99pwz) |
    
    <a id="coding-plan"></a>
    
    <a id="coding-plan-h4"></a>
    
    #### Coding Plan
    
    <a id="cb-cp-config-h"></a>
    
    <a id="cb-cp-config"></a>
    
    | 配置项 | 值 |
    | --- | --- |
    | API 主机 | `https://coding.dashscope.aliyuncs.com/v1` |
    | API 密钥 | Coding Plan 专属 API Key |
    | 模型 | `qwen3.7-plus`；可用模型见 [Coding Plan 支持的模型](../../coding-plan-guide/coding-plan.md) |
    
    API 路径无需填写。
    
3.  3
    
    验证
    
    <a id="cb-verify-h"></a>
    
    <a id="cb-verify"></a>
    
    点击 **新建**，在 **模型 ID** 填入上表中的模型并保存。在对话框中选择该模型，发送“你好”，模型正常返回响应即配置成功。
    

<a id="错误码"></a>

<a id="cb-faq-errorcode-h"></a>

<a id="cb-faq-errorcode"></a>

## 错误码

配置过程中遇到报错，参考对应计费方案的常见问题文档：

-   Token Plan：[Token Plan 常见问题](../../token-plan-guide/token-plan-faq.md#tpt-h-errors)
-   按量计费：[错误码](../../../model-api-reference/preparations/error-code.md)
-   Coding Plan：[Coding Plan 常见问题](../../coding-plan-guide/coding-plan-faq.md#e07ad90b4f3l0)

<a id="常见问题"></a>

<a id="cb-faq-h"></a>

<a id="cb-faq"></a>

## 常见问题

<a id="accordion-如何按量计费接入节省计划与资源包"></a>

如何按量计费接入节省计划与资源包？

按量计费接入方式不变，使用百炼通用 API Key 和 Base URL。购买节省计划或资源包后自动生效，调用费用按抵扣顺序自动抵扣。详情参见[节省计划与资源包](../../../model-user-guide/test-1/savings-plan-and-resource-package.md#h2-usage)。

<a id="accordion-调用时报错-401-unauthorized"></a>

调用时报错 401 Unauthorized

<a id="cb-faq-401-h"></a>

可能原因：

-   API Key 与所选计费方案不匹配。Token Plan、按量计费和 Coding Plan 的 API Key 互不通用。
-   API Key 复制不完整，或包含多余的空格。

使用对应方案的专属 API Key，并重新复制完整 Key。
