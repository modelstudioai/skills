# Cherry Studio

在 Cherry Studio 中使用阿里云百炼模型。

<a id="快速开始"></a>

<a id="cs-quickstart-h"></a>

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
    
    <a id="connect_bailian_h"></a>
    
    打开 Cherry Studio，点击右上角的设置按钮，在 **模型** 栏点击 **添加**，填写供应商名称（例如 `百炼`），提供商类型选择 **OpenAI**。按计费方案填写配置：
    
    <a id="sec-tabs"></a>
    
    <a id="token-plan"></a>
    
    <a id="token-plan-h4"></a>
    
    #### Token Plan
    
    <a id="tpp_config_h"></a>
    
    <a id="tp_config_h"></a>
    
    | 配置项 | 值 |
    | --- | --- |
    | API 地址 | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
    | API 密钥 | Token Plan 个人版或团队版专属 API Key |
    | 模型 | 填写[个人版](../../token-plan-personal/token-plan-personal-overview.md#tppo-h-models)或[团队版](../../token-plan-team-edition/token-plan-team-overview.md#tpto-h-models)支持的文本生成模型 |
    
    <a id="按量计费"></a>
    
    <a id="按量计费-h4"></a>
    
    #### 按量计费
    
    <a id="payg_config_h"></a>
    
    按实际调用量后付费。将 `{WorkspaceId}` 替换为 [Workspace ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)，以下以华北2（北京）为例。
    
    | 配置项 | 值 |
    | --- | --- |
    | API 地址 | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
    | API 密钥 | 百炼 API Key |
    | 模型 | `qwen3.8-max` 或 `qwen3.8-flash`；可用模型见 [OpenAI 兼容接口支持的模型](../../../model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md#7f9c78ae99pwz) |
    
    <a id="coding-plan"></a>
    
    <a id="coding-plan-h4"></a>
    
    #### Coding Plan
    
    <a id="cp_config_h"></a>
    
    | 配置项 | 值 |
    | --- | --- |
    | API 地址 | `https://coding.dashscope.aliyuncs.com/v1` |
    | API 密钥 | Coding Plan 专属 API Key |
    | 模型 | `qwen3.7-plus`；可用模型见 [Coding Plan 支持的模型](../../coding-plan-guide/coding-plan.md) |
    
3.  3
    
    验证
    
    <a id="verify_h"></a>
    
    在 **模型 ID** 填入模型，点击 **添加**。返回对话界面，选择刚添加的模型并发送任意消息，模型正常返回响应即配置成功。
    

<a id="错误码"></a>

<a id="faq_error_h3"></a>

## 错误码

配置过程中遇到报错，参考对应计费方案的常见问题文档：

-   Token Plan：[Token Plan 常见问题](../../token-plan-guide/token-plan-faq.md#tpt-h-errors)
-   按量计费：[错误码](../../../model-api-reference/preparations/error-code.md)
-   Coding Plan：[Coding Plan 常见问题](../../coding-plan-guide/coding-plan-faq.md#e07ad90b4f3l0)

<a id="常见问题"></a>

<a id="18040c60b4sve"></a>

## 常见问题

<a id="accordion-如何按量计费接入节省计划与资源包"></a>

如何按量计费接入节省计划与资源包？

按量计费接入方式不变，使用百炼通用 API Key 和 Base URL。购买节省计划或资源包后自动生效，调用费用按抵扣顺序自动抵扣。详情参见[节省计划与资源包](../../../model-user-guide/test-1/savings-plan-and-resource-package.md#h2-usage)。

<a id="accordion-调用时报错-401-unauthorized"></a>

调用时报错 401 Unauthorized

<a id="cs-faq-401-h"></a>

可能原因：

-   API Key 与所选计费方案不匹配。Token Plan、按量计费和 Coding Plan 的 API Key 互不通用。
-   按量计费的 API Key 与 API 地址不在同一地域。

使用对应方案的专属 API Key，并确认按量计费的 API Key 与地域匹配。

<a id="accordion-ram-子账号调用模型时报错无权限"></a>

RAM 子账号调用模型时报错无权限

<a id="cs-faq-ram-h"></a>

RAM 子账号需要拥有模型的调用权限。参见[业务空间管理](https://help.aliyun.com/zh/model-studio/use-workspace)。

<a id="accordion-报错-the-value-of-the-enable-thinking-parameter-is-restricted-to-true"></a>

报错 The value of the enable\_thinking parameter is restricted to True

<a id="b17bed2ce46hy"></a>

**原因**：该模型仅支持在思考模式下运行，但调用时未开启思考模式。

**解决方案**：在客户端中开启思考模式。

<a id="accordion-接入按量计费时-有免费额度但产生了费用"></a>

接入按量计费时，有免费额度但产生了费用

<a id="4ed36453edmeh"></a>

可能的原因：

-   **地域不匹配**：免费额度仅适用于华北2（北京）地域的模型。使用其他地域的模型会产生费用。请检查**API 地址**是否与目标地域匹配，详情请参见[新人免费额度](../../../model-user-guide/test-1/new-free-quota.md)。
-   **额度按模型独立计算**：各模型的免费额度相互独立，不可跨模型共享。
-   **数据更新延迟**：控制台显示的免费额度数据每小时更新。即使控制台显示仍有余量，实际额度也可能已耗尽。

可通过[如何查看产生费用的模型？](../../../model-user-guide/test-1/new-free-quota.md#3bfa8283d0tc2)及[如何查看模型调用记录？](../../../model-user-guide/test-1/new-free-quota.md#ab6ba5c538rn3)确认费用详情。
