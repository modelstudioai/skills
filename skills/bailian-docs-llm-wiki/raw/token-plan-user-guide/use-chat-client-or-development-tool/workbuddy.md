# 接入 WorkBuddy

在 WorkBuddy 中使用阿里云百炼模型。

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
    
    在对话界面底部点击模型选择器，在列表底部点击**配置自定义模型**；也可以从左下角头像进入**设置**，在左侧导航的功能分组中选择**模型**。点击**添加模型**，供应商选择**自定义**，按所选方案填写：
    
    #### Token Plan
    
    配置项
    
    值
    
    接口地址
    
    `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions`
    
    API Key
    
    上一步获取的 API Key
    
    模型名称
    
    填写[个人版](https://help.aliyun.com/zh/model-studio/token-plan-personal-overview#tppo-h-models)或[团队版](https://help.aliyun.com/zh/model-studio/token-plan-team-overview#tpto-h-models)支持的文本生成模型
    
    #### 按量计费
    
    按实际调用量后付费。
    
    配置项
    
    值
    
    接口地址
    
    `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions`，`{WorkspaceId}` 替换为 [Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)
    
    API Key
    
    上一步获取的 API Key，需与 Base URL 同地域（华北2 北京）
    
    模型名称
    
    `qwen3.8-max` 或 `qwen3.8-flash`（[支持的模型](https://help.aliyun.com/zh/model-studio/compatibility-of-openai-with-dashscope#7f9c78ae99pwz)）
    
    #### Coding Plan
    
    配置项
    
    值
    
    接口地址
    
    `https://coding.dashscope.aliyuncs.com/v1/chat/completions`
    
    API Key
    
    上一步获取的 Coding Plan API Key
    
    模型名称
    
    `qwen3.7-plus`（[支持的模型](raw/token-plan-user-guide/coding-plan-guide/coding-plan.md)）
    
    **说明**
    
    1.  接口地址不会自动补全，需填写完整的 Chat Completions 地址（结尾为 `/chat/completions`）。
    2.  自定义模型仅支持 OpenAI 兼容的 Chat Completions 协议，不支持 Responses API 与 Anthropic 协议。
    
    填写后点击**保存**；可点击**测试连接**确认接口连通。
    
3.  3
    
    验证
    
    在对话界面底部的模型选择器中选择已添加的模型，输入任意问题。模型正常返回响应即表示配置成功。
    

## 错误码

配置过程中遇到报错，参考对应计费方案的常见问题文档：

-   Token Plan：[Token Plan 常见问题](https://help.aliyun.com/zh/model-studio/token-plan-faq#tpt-h-errors)
-   按量计费：[错误码](raw/model-api-reference/preparations/error-code.md)
-   Coding Plan：[Coding Plan 常见问题](https://help.aliyun.com/zh/model-studio/coding-plan-faq#e07ad90b4f3l0)

## 常见问题

如何按量计费接入节省计划与资源包？

按量计费接入方式不变，使用百炼通用 API Key 和 Base URL。购买节省计划或资源包后自动生效，调用费用按抵扣顺序自动抵扣。详情参见[节省计划与资源包](https://help.aliyun.com/zh/model-studio/savings-plan-and-resource-package#h2-usage)。

调用时返回 401 或鉴权失败

检查 API Key 是否与 Base URL 同地域。按量计费使用华北2（北京）的 Base URL 时，API Key 也必须来自华北2（北京）。

调用时报错模型不存在

模型名称会作为请求中的 `model` 参数发送，须与百炼模型名完全一致（区分大小写，不带额外前后缀）。在自定义模型设置中核对模型名称后重试。
