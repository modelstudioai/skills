# Trae

在 Trae 中使用阿里云百炼模型。

## 快速开始

登录后按以下步骤配置。

1.  1
    
    获取 API Key
    
    根据计费方案获取对应的 API Key：
    
    -   Token Plan 个人版：[创建或查看 API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan/personal)
    -   Token Plan 团队版：[分配坐席并获取 API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/uac-admin/organization/members/list)
    -   按量计费：[百炼 API Key](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key?spm=5176.28197581.0.0.307f29a4lC7Vbh)
    -   Coding Plan：[Coding Plan API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/coding-plan)
    
2.  2
    
    配置模型
    
    在 Trae 中前往**设置** > **模型**，点击**添加模型**。
    
    #### Token Plan
    
    选择**自定义模型**，按下表填写：
    
    配置项
    
    值
    
    API 格式
    
    兼容 OpenAI
    
    请求地址
    
    `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
    
    模型 ID
    
    填写[个人版](https://help.aliyun.com/zh/model-studio/token-plan-personal-overview#tppo-h-models)或[团队版](https://help.aliyun.com/zh/model-studio/token-plan-team-overview#tpto-h-models)支持的文本生成模型
    
    API 密钥
    
    上一步获取的 Token Plan API Key
    
    #### 按量计费
    
    选择**阿里云**，填写上一步获取的百炼 API Key，选择套餐支持的文本生成模型。
    
    #### Coding Plan
    
    选择**阿里云**，填写上一步获取的 Coding Plan API Key，选择套餐支持的文本生成模型。
    
3.  3
    
    验证
    
    在对话框右下角的模型列表中选择已配置的模型，发送一条消息。收到回复即表示配置成功。
    

## 错误码

配置过程中遇到报错，参考对应计费方案的常见问题文档：

-   Token Plan：[Token Plan 常见问题](https://help.aliyun.com/zh/model-studio/token-plan-faq#tpt-h-errors)
-   按量计费：[错误码](raw/model-api-reference/preparations/error-code.md)
-   Coding Plan：[Coding Plan 常见问题](https://help.aliyun.com/zh/model-studio/coding-plan-faq#e07ad90b4f3l0)

## 常见问题

如何按量计费接入节省计划与资源包？

按量计费接入方式不变，使用百炼通用 API Key 和 Base URL。购买节省计划或资源包后自动生效，调用费用按抵扣顺序自动抵扣。详情参见[节省计划与资源包](https://help.aliyun.com/zh/model-studio/savings-plan-and-resource-package#h2-usage)。

调用时报错 401 Unauthorized

API Key 与所选方案不匹配，或订阅已过期。确认 API Key 类型与所选方案一致，并重新获取、填写。

调用时报错模型不存在

模型 ID 与所选方案不匹配。选择对应方案支持的文本生成模型。
