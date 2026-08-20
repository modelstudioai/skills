# Cherry Studio

Cherry Studio 是一款开源 AI 桌面客户端，可以通过 Token Plan 个人版、Token Plan 团队版、Coding Plan 或按量计费接入阿里云百炼。

## 安装 Cherry Studio

前往 [Cherry Studio 下载页面](https://www.cherry-ai.com/download)，根据操作系统下载安装包并完成安装。

## 配置接入凭证

打开 Cherry Studio，点击右上角的设置按钮，在**模型**栏点击**添加**，填写供应商名称（如 Token Plan 团队版），提供商类型选择 OpenAI。

百炼提供四种计费方案，根据需要选择：

-   **Token Plan 个人版**：按 token 消耗抵扣个人 Credits。
-   **Token Plan 团队版**：按坐席订阅，按 token 消耗抵扣 Credits。
-   **Coding Plan**：固定月费订阅，按模型调用次数计量。
-   **按量计费**：按实际调用量后付费。

### Token Plan 个人版

**配置项**

**说明**

**API 密钥**

填入 Token Plan 个人版专属 [API Key](https://bailian.console.aliyun.com/cn-beijing?tab=plan#/efm/subscription/token-plan/personal)。

**API 地址**

`[https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1](https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1)`

**模型**

可用模型请参考 Token Plan 个人版[支持的模型](raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)。

### Token Plan 团队版

**配置项**

**说明**

**API 密钥**

填入 Token Plan 团队版专属 [API Key](https://bailian.console.aliyun.com/cn-beijing?tab=plan#/efm/subscription/token-plan/enterprise)。

**API 地址**

`[https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1](https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1)`

**模型**

可用模型请参考 Token Plan 团队版[支持的模型](raw/model-user-guide/token-plan-guide/token-plan-overview.md)。

### Coding Plan

**配置项**

**说明**

**API 密钥**

填入 Coding Plan 专属 [API Key](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/coding_plan)。

**API 地址**

`[https://coding.dashscope.aliyuncs.com/v1](https://coding.dashscope.aliyuncs.com/v1)`

**模型**

可用模型请参考 Coding Plan [支持的模型](raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)。

### 按量计费

**配置项**

**说明**

**API 密钥**

填入[阿里云百炼 API Key](raw/model-api-reference/preparations/get-api-key.md)。

**API 地址**

根据地域，填入对应 URL（请将 URL 中的 `{WorkspaceId}` 替换为真实的[获取Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#d3eb3cd37b7fu)）：

-   华北2（北京）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
    
-   新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`
    
-   美国（弗吉尼亚）：`https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/compatible-mode/v1`
    

**模型**

填入[支持的模型](https://help.aliyun.com/zh/model-studio/compatibility-of-openai-with-dashscope#7f9c78ae99pwz)。

## 验证配置

在**模型 ID**填入需要使用的模型，点击**添加**。返回对话界面，输入任意问题，模型正常返回响应即配置成功。

> 如果是 RAM 子账号，请参见[业务空间管理](raw/model-user-guide/security-and-compliance/permission-management-overview.md)，确保拥有模型的调用权限。

## 常见问题

### 错误码

配置过程中遇到报错，请参考对应计费方案的常见问题文档：

-   按量计费：[错误码排查](raw/model-api-reference/preparations/error-code.md)
-   Coding Plan：[Coding Plan 常见问题](raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan-faq.md)
-   Token Plan 个人版：[Token Plan 常见问题](raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-faq.md)
-   Token Plan 团队版：[Token Plan 团队版常见问题](raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-faq.md)

### 报错 The value of the enable\_thinking parameter is restricted to True

**原因**：该模型仅支持在思考模式下运行，但调用时未开启思考模式。

**解决方案**：在客户端中开启思考模式。

### 接入按量计费时，有免费额度但产生了费用

可能的原因：

-   **地域不匹配**：免费额度仅适用于华北2（北京）地域的模型。使用其他地域的模型会产生费用。请检查**API 地址**是否与目标地域匹配，详情请参见[新人免费额度](raw/model-user-guide/test-1/new-free-quota.md)。
-   **额度按模型独立计算**：各模型的免费额度相互独立，不可跨模型共享。
-   **数据更新延迟**：控制台显示的免费额度数据每小时更新。即使控制台显示仍有余量，实际额度也可能已耗尽。

可通过[如何查看产生费用的模型？](https://help.aliyun.com/zh/model-studio/new-free-quota#3bfa8283d0tc2)及[如何查看模型调用记录？](https://help.aliyun.com/zh/model-studio/new-free-quota#ab6ba5c538rn3)确认费用详情。
