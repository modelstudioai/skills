# Trae

在 Trae 中使用阿里云百炼模型。

<a id="快速开始"></a>

<a id="quick-connect"></a>

## 快速开始

登录后按以下步骤配置。

<a id="trae-prerequisites"></a>

1.  1
    
    获取 API Key
    
    根据计费方案获取对应的 API Key：
    
    -   Token Plan 个人版：[创建或查看 API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan/personal)
    -   Token Plan 团队版：[分配坐席并获取 API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/uac-admin/organization/members/list)
    -   按量计费：[百炼 API Key](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key?spm=5176.28197581.0.0.307f29a4lC7Vbh)
    -   Coding Plan：[Coding Plan API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/coding-plan)
    
2.  2
    
    配置模型
    
    <a id="mt-config-h"></a>
    
    <a id="mt-trae-h"></a>
    
    在 Trae 中前往**设置** > **模型**，点击**添加模型**。
    
    <a id="sec-tabs"></a>
    
    <a id="token-plan"></a>
    
    <a id="token-plan-h4"></a>
    
    #### Token Plan
    
    <a id="tpp-mt-h"></a>
    
    <a id="mt-tp-h"></a>
    
    选择**自定义模型**，按下表填写：
    
    | 配置项 | 值 |
    | --- | --- |
    | API 格式 | 兼容 OpenAI |
    | 请求地址 | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
    | 模型 ID | 填写[个人版](../token-plan-personal/token-plan-personal-overview.md#tppo-h-models)或[团队版](../token-plan-team-edition/token-plan-team-overview.md#tpto-h-models)支持的文本生成模型 |
    | API 密钥 | 上一步获取的 Token Plan API Key |
    
    <a id="按量计费"></a>
    
    <a id="按量计费-h4"></a>
    
    #### 按量计费
    
    <a id="mt-payg-h"></a>
    
    选择**阿里云**，填写上一步获取的百炼 API Key，选择套餐支持的文本生成模型。
    
    <a id="coding-plan"></a>
    
    <a id="coding-plan-h4"></a>
    
    #### Coding Plan
    
    <a id="mt-cp-h"></a>
    
    选择**阿里云**，填写上一步获取的 Coding Plan API Key，选择套餐支持的文本生成模型。
    
3.  3
    
    验证
    
    <a id="trae-verify"></a>
    
    在对话框右下角的模型列表中选择已配置的模型，发送一条消息。收到回复即表示配置成功。
    

<a id="错误码"></a>

<a id="faq_error_h3"></a>

## 错误码

配置过程中遇到报错，参考对应计费方案的常见问题文档：

-   Token Plan：[Token Plan 常见问题](../token-plan-guide/token-plan-faq.md#tpt-h-errors)
-   按量计费：[错误码](../../model-api-reference/preparations/error-code.md)
-   Coding Plan：[Coding Plan 常见问题](../coding-plan-guide/coding-plan-faq.md#e07ad90b4f3l0)

<a id="常见问题"></a>

<a id="trae-faq"></a>

## 常见问题

<a id="accordion-如何按量计费接入节省计划与资源包"></a>

如何按量计费接入节省计划与资源包？

按量计费接入方式不变，使用百炼通用 API Key 和 Base URL。购买节省计划或资源包后自动生效，调用费用按抵扣顺序自动抵扣。详情参见[节省计划与资源包](../../model-user-guide/test-1/savings-plan-and-resource-package.md#h2-usage)。

<a id="accordion-调用时报错-401-unauthorized"></a>

调用时报错 401 Unauthorized

API Key 与所选方案不匹配，或订阅已过期。确认 API Key 类型与所选方案一致，并重新获取、填写。

<a id="accordion-调用时报错模型不存在"></a>

调用时报错模型不存在

模型 ID 与所选方案不匹配。选择对应方案支持的文本生成模型。
