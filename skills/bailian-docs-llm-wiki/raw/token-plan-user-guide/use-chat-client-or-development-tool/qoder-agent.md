# Qoder

在 Qoder 中使用阿里云百炼模型。

<a id="connection-reference"></a>

<a id="add-model"></a>

<a id="快速接入"></a>

## 快速接入

选择你使用的客户端，完成配置。

<a id="sec-tabs"></a>

<a id="桌面端"></a>

<a id="桌面端-h4"></a>

#### 桌面端

1.  1
    
    打开模型设置
    
    打开 **设置 → 模型**，点击 **添加模型**。
    
2.  2
    
    选择供应商
    
    供应商选择 **阿里云百炼 - 中国**。
    
3.  3
    
    填写模型信息
    
    选择类型和模型，按计费方案获取对应的 **API Key** 并填写：
    
    <a id="sec-tabs-2"></a>
    
    <a id="token-plan"></a>
    
    <a id="token-plan-h4"></a>
    
    #### Token Plan
    
    -   Token Plan 个人版：[创建或查看 API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan/personal)
    -   Token Plan 团队版：[分配坐席并获取 API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/uac-admin/organization/members/list)
    
    <a id="按量计费"></a>
    
    <a id="按量计费-h4"></a>
    
    #### 按量计费
    
    [阿里云百炼 API Key](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key?spm=5176.28197581.0.0.307f29a4lC7Vbh)
    
    <a id="coding-plan"></a>
    
    <a id="coding-plan-h4"></a>
    
    #### Coding Plan
    
    [Coding Plan API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/coding-plan)
    
4.  4
    
    校验并保存
    
    点击 **校验并添加模型**。显示“模型已保存”后，点击 **完成**。
    
5.  5
    
    选择模型
    
    返回对话，在模型选择器的 **自定义** 分组中选择已添加的模型。
    

<a id="ide"></a>

<a id="ide-h4"></a>

#### IDE

<a id="qd-ide-h"></a>

<a id="qd-ide-config-h"></a>

1.  1
    
    打开模型设置
    
    点击右上角的 **用户设置**，进入 **Qoder IDE 设置 → 模型**。
    
2.  2
    
    选择提供商
    
    点击 **添加**，提供商选择 **阿里云百炼 - 中国**。
    
3.  3
    
    填写并保存模型
    
    选择类型和模型，按计费方案获取对应的 **API 密钥** 并填写：
    
    <a id="sec-tabs-3"></a>
    
    <a id="token-plan-2"></a>
    
    <a id="token-plan-2-h4"></a>
    
    #### Token Plan
    
    -   Token Plan 个人版：[创建或查看 API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan/personal)
    -   Token Plan 团队版：[分配坐席并获取 API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/uac-admin/organization/members/list)
    
    <a id="按量计费-2"></a>
    
    <a id="按量计费-2-h4"></a>
    
    #### 按量计费
    
    [阿里云百炼 API Key](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key?spm=5176.28197581.0.0.307f29a4lC7Vbh)
    
    <a id="coding-plan-2"></a>
    
    <a id="coding-plan-2-h4"></a>
    
    #### Coding Plan
    
    [Coding Plan API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/coding-plan)
    
    点击 **添加**。
    
4.  4
    
    选择模型
    
    校验通过后，在对话模型选择器的 **自定义** 分组中选择该模型。
    

<a id="cli"></a>

<a id="cli-h4"></a>

#### CLI

<a id="qd-cli-h"></a>

<a id="qd-cli-config-h"></a>

<a id="qd-cli-use-h"></a>

1.  1
    
    打开自定义模型列表
    
    输入 `/model`，按 Tab 键切换到 **Custom**。
    
2.  2
    
    选择提供商
    
    选择 **Add custom model...**，在 **Platform presets** 下选择 **Alibaba Cloud Model Studio - China**。
    
3.  3
    
    选择模型
    
    在对应的 **Token plan**、**Coding plan** 或 **PayAsYouGo** 分组下选择模型。
    
4.  4
    
    填写模型参数和 API Key
    
    确认 **Context Window** 和 **Thinking Effort** 设置，按计费方案获取对应的 **API Key** 并填写：
    
    <a id="sec-tabs-4"></a>
    
    <a id="token-plan-3"></a>
    
    <a id="token-plan-3-h4"></a>
    
    #### Token Plan
    
    -   Token Plan 个人版：[创建或查看 API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan/personal)
    -   Token Plan 团队版：[分配坐席并获取 API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/uac-admin/organization/members/list)
    
    <a id="按量计费-3"></a>
    
    <a id="按量计费-3-h4"></a>
    
    #### 按量计费
    
    [阿里云百炼 API Key](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key?spm=5176.28197581.0.0.307f29a4lC7Vbh)
    
    <a id="coding-plan-3"></a>
    
    <a id="coding-plan-3-h4"></a>
    
    #### Coding Plan
    
    [Coding Plan API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/coding-plan)
    
5.  5
    
    使用模型
    
    校验成功后，在模型列表中选择该模型。无需重启 CLI。
    

<a id="jetbrains-插件"></a>

<a id="jetbrains-插件-h4"></a>

#### JetBrains 插件

<a id="qd-jb-h"></a>

1.  1
    
    打开模型设置
    
    点击插件面板右上角的账号头像，选择 **插件设置**，进入 **个人设置 → 模型设置**。
    
2.  2
    
    选择提供商
    
    点击 **添加模型**，提供商选择 **阿里云百炼 - 中国**。
    
3.  3
    
    填写并保存模型
    
    选择类型和模型，按计费方案获取对应的 **API 密钥** 并填写：
    
    <a id="sec-tabs-5"></a>
    
    <a id="token-plan-4"></a>
    
    <a id="token-plan-4-h4"></a>
    
    #### Token Plan
    
    -   Token Plan 个人版：[创建或查看 API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan/personal)
    -   Token Plan 团队版：[分配坐席并获取 API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/uac-admin/organization/members/list)
    
    <a id="按量计费-4"></a>
    
    <a id="按量计费-4-h4"></a>
    
    #### 按量计费
    
    [阿里云百炼 API Key](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key?spm=5176.28197581.0.0.307f29a4lC7Vbh)
    
    <a id="coding-plan-4"></a>
    
    <a id="coding-plan-4-h4"></a>
    
    #### Coding Plan
    
    [Coding Plan API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/coding-plan)
    
    点击 **确定**。
    
4.  4
    
    选择模型
    
    校验通过后，返回会话，在输入框下方的模型选择器中选择已添加的模型。
    

<a id="常见问题"></a>

## 常见问题

<a id="qd-faq-h"></a>

<a id="accordion-如何按量计费接入节省计划与资源包"></a>

如何按量计费接入节省计划与资源包？

按量计费接入方式不变，使用百炼通用 API Key 和 Base URL。购买节省计划或资源包后自动生效，调用费用按抵扣顺序自动抵扣。详情参见[节省计划与资源包](../../model-user-guide/test-1/savings-plan-and-resource-package.md#h2-usage)。

<a id="accordion-错误码"></a>

错误码

<a id="faq_error_h3"></a>

配置过程中遇到报错，请参考对应计费方案的常见问题文档：

-   Token Plan：[Token Plan 常见问题](../token-plan-guide/token-plan-faq.md#tpt-h-errors)
-   按量计费：[错误码](../../model-api-reference/preparations/error-code.md)
-   Coding Plan：[Coding Plan 常见问题](../coding-plan-guide/coding-plan-faq.md#e07ad90b4f3l0)

<a id="accordion-为什么在-qoder-设置中找不到模型选项"></a>

为什么在 Qoder 设置中找不到模型选项？

可能有以下原因：

-   **未完成登录**：需要先完成登录，才能进行对话和配置模型。
-   **当前版本不支持**：建议更新至最新版本。
