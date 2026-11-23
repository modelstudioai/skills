# ZCode

在 ZCode 中使用阿里云百炼模型。

## 快速开始

1.  1
    
    获取 API Key
    
    根据计费方案获取 API Key：
    
    -   Token Plan 个人版：[创建或查看 API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan/personal)
    -   Token Plan 团队版：[分配坐席并获取 API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/uac-admin/organization/members/list)
    -   按量计费：[百炼 API Key](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key?spm=5176.28197581.0.0.307f29a4lC7Vbh)
    -   Coding Plan：[Coding Plan API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/coding-plan)
    
2.  2
    
    添加供应商
    
    在 ZCode 中进入模型设置，在左侧供应商列表底部添加供应商，填写自定义名称。
    
3.  3
    
    选择协议和 Base URL
    
    ZCode 支持 Anthropic 和 OpenAI 协议，Base URL 不追加 `/chat/completions`。
    
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
    
4.  4
    
    填写 API Key
    
    填入所选方案的 API Key。
    
5.  5
    
    填写模型并保存
    
    按计费方案填写模型 ID，开启启用开关后保存：
    
    -   Token Plan：填写[个人版](https://help.aliyun.com/zh/model-studio/token-plan-personal-overview#tppo-h-models)或[团队版](https://help.aliyun.com/zh/model-studio/token-plan-team-overview#tpto-h-models)支持的文本生成模型
    -   按量计费：例如 `qwen3.8-max` 或 `qwen3.8-flash`
    -   Coding Plan：填写[支持的文本生成模型](raw/token-plan-user-guide/coding-plan-guide/coding-plan.md)
    
6.  6
    
    验证
    
    在 ZCode 中选择已添加的模型，发送一条测试消息。收到模型回复即表示接入成功。
    

## 常见问题

如何按量计费接入节省计划与资源包？

按量计费接入方式不变，使用百炼通用 API Key 和 Base URL。购买节省计划或资源包后自动生效，调用费用按抵扣顺序自动抵扣。详情参见[节省计划与资源包](https://help.aliyun.com/zh/model-studio/savings-plan-and-resource-package#h2-usage)。

模型未出现在 ZCode 的模型列表中

确认已添加模型、开启启用开关并保存配置。返回模型设置检查供应商和模型条目是否完整。

无法调用模型或返回 401

确认 API Key、Base URL 和模型属于同一方案。Token Plan、Coding Plan 与按量计费的 API Key 互不通用。按量计费还需确认 `{WorkspaceId}` 已替换为正确地域的 Workspace ID。

请求返回 404 或提示端点不存在

检查 Base URL 是否误加了 `/chat/completions`。ZCode 使用 Base URL，不追加该路径。
