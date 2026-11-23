# Cline

在 Cline 中使用阿里云百炼模型。

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
    
    打开 Cline 面板，点击 **Bring my own API key**，将 API Provider 设为 **OpenAI Compatible**，按所选方案填写。已配置过 Cline 时，点击右上角设置图标进入配置界面。
    
    #### Token Plan
    
    配置项
    
    值
    
    Base URL
    
    `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
    
    API Key
    
    Token Plan API Key
    
    Model ID
    
    填写[个人版](https://help.aliyun.com/zh/model-studio/token-plan-personal-overview#tppo-h-models)或[团队版](https://help.aliyun.com/zh/model-studio/token-plan-team-overview#tpto-h-models)支持的文本生成模型
    
    #### 按量计费
    
    将 `{WorkspaceId}` 替换为真实的 [Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。
    
    配置项
    
    值
    
    Base URL
    
    `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
    
    API Key
    
    阿里云百炼 API Key
    
    Model ID
    
    例如 `qwen3.8-max` 或 `qwen3.8-flash`
    
    #### Coding Plan
    
    配置项
    
    值
    
    Base URL
    
    `https://coding.dashscope.aliyuncs.com/v1`
    
    API Key
    
    Coding Plan API Key
    
    Model ID
    
    填写[支持的文本生成模型](raw/token-plan-user-guide/coding-plan-guide/coding-plan.md)
    
3.  3
    
    验证
    
    在 Cline 对话面板发送一条消息，模型正常返回响应即表示配置成功。
    

## 接入百炼 CLI

[百炼 CLI](https://bailian.console.aliyun.com/cli) 安装时会向 `~/.cline/skills/bailian-cli/` 注册 Skill，Cline 可以通过对话调用百炼能力。能力清单见[百炼 CLI 控制台](https://bailian.console.aliyun.com/cli)。前置要求 [Node.js](https://nodejs.org/zh-cn/download) 18+。

1.  1
    
    安装百炼 CLI
    
    在 Cline 对话中执行：
    
    ```
    请帮我全局安装阿里云百炼 CLI 命令行工具：npm install -g bailian-cli
    ```
    
2.  2
    
    配置 API Key
    
    获取 [API Key](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key?spm=5176.28197581.0.0.307f29a4lC7Vbh)，然后在对话中让 Cline 配置该 API Key。
    

## 错误码

配置过程中遇到报错，参考对应计费方案的常见问题文档：

-   Token Plan：[Token Plan 常见问题](https://help.aliyun.com/zh/model-studio/token-plan-faq#tpt-h-errors)
-   按量计费：[错误码](raw/model-api-reference/preparations/error-code.md)
-   Coding Plan：[Coding Plan 常见问题](https://help.aliyun.com/zh/model-studio/coding-plan-faq#e07ad90b4f3l0)

## 常见问题

如何按量计费接入节省计划与资源包？

按量计费接入方式不变，使用百炼通用 API Key 和 Base URL。购买节省计划或资源包后自动生效，调用费用按抵扣顺序自动抵扣。详情参见[节省计划与资源包](https://help.aliyun.com/zh/model-studio/savings-plan-and-resource-package#h2-usage)。

报错 401 Incorrect API key provided

可能原因：

-   API Key 与 Base URL 不匹配。不同计费方案的 API Key 不通用，请确认 API Key 和 Base URL 来自同一方案。
-   按量计费的 API Key 与 Base URL 的地域不一致，请检查二者是否对应同一地域。

报错 400 InternalError.Algo.InvalidParameter

使用 Qwen3 思考模式或 QwQ 模型时，在设置界面点击 `MODEL CONFIGURATION`，勾选 **Enable R1 messages format**。
