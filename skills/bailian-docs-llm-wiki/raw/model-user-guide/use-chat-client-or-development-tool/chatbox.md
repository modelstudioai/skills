# Chatbox

Chatbox 是一款跨平台 AI 客户端应用，可以通过Token Plan 团队版、Coding Plan或按量计费接入阿里云百炼。

## **下载安装 Chatbox**

前往[Chatbox 官网](https://chatboxai.app/zh)，根据操作系统下载并安装，或直接使用网页版。

## **配置接入凭证**

点击 Chatbox 页面左下方的**设置**，点击**模型提供方**，点击底部的**添加**。在弹窗中填写**名称**，**API 模式**选择**OpenAI API 兼容**，点击**添加**。然后根据所选方案，填入对应的 API 密钥和 API 主机。

百炼提供三种计费方案，根据需要选择：

-   **Token Plan 团队版**：按坐席订阅，按 token 消耗抵扣 Credits。
    
-   **Coding Plan**：固定月费订阅，按模型调用次数计量。
    
-   **按量计费**：按实际调用量后付费。
    

### Token Plan 团队版

**配置项**

**说明**

**API 密钥**

填入 Token Plan 团队版专属 [API Key](https://bailian.console.aliyun.com/?tab=plan#/efm/subscription/overview)。

**API 主机**

`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`

> API 路径无需填写。

**模型**

点击**新建**，在**模型 ID**中填入模型名称。可用模型请参考 Token Plan 团队版[支持的模型](https://help.aliyun.com/zh/model-studio/token-plan-overview)。

### Coding Plan

**配置项**

**说明**

**API 密钥**

填入 Coding Plan 专属 [API Key](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/coding_plan)。

**API 主机**

`https://coding.dashscope.aliyuncs.com/v1`

> API 路径无需填写。

**模型**

点击**新建**，在**模型 ID**中填入模型名称。可用模型请参考 Coding Plan [支持的模型](https://help.aliyun.com/zh/model-studio/coding-plan)。

### 按量计费

**配置项**

**说明**

**API 密钥**

填入[阿里云百炼 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。

**API 主机**

根据模型部署地域，填入对应 URL：

-   华北2（北京）：`https://dashscope.aliyuncs.com/compatible-mode/v1`
    
-   新加坡：`https://dashscope-intl.aliyuncs.com/compatible-mode/v1`
    
-   美国（弗吉尼亚）：`https://dashscope-us.aliyuncs.com/compatible-mode/v1`
    

> API 路径无需填写。

**模型**

点击**新建**，在**模型 ID**中填入[支持的模型](https://help.aliyun.com/zh/model-studio/compatibility-of-openai-with-dashscope#7f9c78ae99pwz)。

## **验证配置**

完成配置后，在对话框输入“你好”并发送，模型正常返回响应即配置成功。

## **常见问题**

### 错误码

配置过程中遇到报错，请参考对应计费方案的常见问题文档：

-   按量计费：[错误码排查](https://help.aliyun.com/zh/model-studio/error-code)
    
-   Coding Plan：[Coding Plan 常见问题](https://help.aliyun.com/zh/model-studio/coding-plan-faq)
    
-   Token Plan 团队版：[Token Plan 团队版常见问题](https://help.aliyun.com/zh/model-studio/token-plan-faq)
