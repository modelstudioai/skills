# Cursor

在 Cursor 中使用阿里云百炼模型。

<a id="快速开始"></a>

<a id="cursor-quickstart-h"></a>

<a id="install_cursor_title"></a>

<a id="connect_bailian_h"></a>

## 快速开始

1.  1
    
    获取 API Key
    
    根据所选计费方案获取 API Key：
    
    -   Token Plan 个人版：[创建或查看 API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan/personal)
    -   Token Plan 团队版：[分配坐席并获取 API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/uac-admin/organization/members/list)
    -   按量计费：[百炼 API Key](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key?spm=5176.28197581.0.0.307f29a4lC7Vbh)
    -   Coding Plan：[Coding Plan API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/coding-plan)
    
2.  2
    
    配置模型
    
    在 Cursor 中打开 **Cursor Settings** > **Models**，开启 **OpenAI API Key** 和 **Override OpenAI Base URL**，按所选方案填写。
    
    <a id="sec-tabs"></a>
    
    <a id="token-plan"></a>
    
    <a id="token-plan-h4"></a>
    
    #### Token Plan
    
    <a id="tpp_config_h"></a>
    
    <a id="tp_config_h"></a>
    
    | 配置项 | 值 |
    | --- | --- |
    | Base URL | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
    | API Key | Token Plan API Key |
    | 模型 | 填写[个人版](../../token-plan-personal/token-plan-personal-overview.md#tppo-h-models)或[团队版](../../token-plan-team-edition/token-plan-team-overview.md#tpto-h-models)支持的文本生成模型；部分模型需要设置别名，见[常见问题](#faq_title) |
    
    <a id="按量计费"></a>
    
    <a id="按量计费-h4"></a>
    
    #### 按量计费
    
    <a id="payg_config_h"></a>
    
    将 `{WorkspaceId}` 替换为真实的 [Workspace ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。
    
    | 配置项 | 值 |
    | --- | --- |
    | Base URL | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
    | API Key | 阿里云百炼 API Key |
    | 模型 | 例如 `qwen3.8-max` 或 `qwen3.8-flash` |
    
    <a id="coding-plan"></a>
    
    <a id="coding-plan-h4"></a>
    
    #### Coding Plan
    
    <a id="cp_config_h"></a>
    
    | 配置项 | 值 |
    | --- | --- |
    | Base URL | `https://coding.dashscope.aliyuncs.com/v1` |
    | API Key | Coding Plan API Key |
    | 模型 | 填写[支持的文本生成模型](../../coding-plan-guide/coding-plan.md) |
    
3.  3
    
    验证
    
    <a id="cursor-verify-h"></a>
    
    在 Cursor 聊天面板发送一条消息，模型正常返回响应即表示配置成功。
    

<a id="接入百炼-cli"></a>

<a id="cs-cli-h"></a>

## 接入百炼 CLI

[百炼 CLI](https://bailian.console.aliyun.com/cli) 安装时会向 `~/.cursor/skills/bailian-cli/` 注册 Skill，Cursor 可以通过对话调用百炼能力。能力清单见[百炼 CLI 控制台](https://bailian.console.aliyun.com/cli)。前置要求 [Node.js](https://nodejs.org/zh-cn/download) 18+。

1.  1
    
    安装百炼 CLI
    
    在 Cursor 对话中执行：
    
    <a id="code-block"></a>
    
    ```text
    请帮我全局安装阿里云百炼 CLI 命令行工具：npm install -g bailian-cli
    ```
    
2.  2
    
    配置 API Key
    
    获取 [API Key](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key?spm=5176.28197581.0.0.307f29a4lC7Vbh)，然后在对话中让 Cursor 配置该 API Key。
    

<a id="错误码"></a>

<a id="faq_error_h3"></a>

## 错误码

配置过程中遇到报错，参考对应计费方案的常见问题文档：

-   Token Plan：[Token Plan 常见问题](../../token-plan-guide/token-plan-faq.md#tpt-h-errors)
-   按量计费：[错误码](../../../model-api-reference/preparations/error-code.md)
-   Coding Plan：[Coding Plan 常见问题](../../coding-plan-guide/coding-plan-faq.md#e07ad90b4f3l0)

<a id="常见问题"></a>

<a id="faq_title"></a>

## 常见问题

<a id="accordion-如何按量计费接入节省计划与资源包"></a>

如何按量计费接入节省计划与资源包？

按量计费接入方式不变，使用百炼通用 API Key 和 Base URL。购买节省计划或资源包后自动生效，调用费用按抵扣顺序自动抵扣。详情参见[节省计划与资源包](../../../model-user-guide/test-1/savings-plan-and-resource-package.md#h2-usage)。

<a id="accordion-在-cursor-中无法调用已添加的模型"></a>

在 Cursor 中无法调用已添加的模型

<a id="faq_1_title"></a>

报错信息如下：

-   The model xxx does not work with your current plan or api key.
-   Named models unavailable Free plans can only use Auto. Switch to Auto or upgrade plans to continue.

**原因**：Cursor 免费版仅支持 Auto 模式，不支持调用自定义模型。

**解决方案**：升级至 **Cursor Pro 及以上套餐**。

<a id="accordion-配置完成后找不到添加的模型"></a>

配置完成后找不到添加的模型

<a id="faq_2_title"></a>

在聊天面板关闭 **Auto** 模式，在模型下拉栏选择所需模型。

<a id="accordion-部分模型名称无法调用"></a>

部分模型名称无法调用

<a id="faq_4_title"></a>

部分模型 ID 与 Cursor 内置模型名冲突，需要改写为连字符形式：

-   glm-5.3 写为 `glm-5-3`，glm-5.2 写为 `glm-5-2`，glm-5.1 写为 `glm-5-1`，glm-5 写为 `glm-5-0`
-   kimi-k2.6 写为 `kimi-k2-6`，kimi-k2.5 写为 `kimi-k2-5`

各方案支持的模型不同，以对应支持列表为准。

<a id="accordion-调用模型报错-we-re-having-trouble-connecting-to-the-model-provider-或-unauthorized-user-api-key"></a>

调用模型报错 "We're having trouble connecting to the model provider." 或 "Unauthorized User API key"

<a id="faq_3_title"></a>

请逐项排查：

-   API Key、Base URL 和模型名称是否与所选计费方案一致。不同方案的凭证不通用。
-   按量计费的 API Key 是否与 Base URL 属于同一地域。
-   模型名称是否需要改写，参见上一条。
