# Cursor

Cursor 是一款 AI 编程 IDE，可以通过按量计费、Coding Plan 或 Token Plan 团队版接入阿里云百炼。

## **安装 Cursor**

通过 [Cursor 官网](https://cursor.com/features)下载并安装 Cursor。

## **配置接入凭证**

在 Cursor 中，点击设置图标，进入 **Cursor Settings** > **Models**。开启 **OpenAI API Key** 和 **Override OpenAI Base URL**，根据所选方案填入对应的 API Key、Base URL 和模型名称。

阿里云百炼提供三种计费方案，根据需要选择：

-   **Token Plan 团队版**：按坐席订阅，按 token 消耗抵扣 Credits。
    
-   **Coding Plan**：固定月费订阅，按模型调用次数计量。
    
-   **按量计费**：按实际调用量后付费。
    

### Token Plan 团队版

**API Key**

Token Plan 团队版专属 [API Key](https://bailian.console.aliyun.com/?tab=plan#/efm/subscription/overview)

**Base URL**

`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`

**可用模型**

Token Plan 团队版[支持的模型](https://help.aliyun.com/zh/model-studio/token-plan-overview)

部分模型名称需调整：kimi-k2.6 写为 **kimi-k2-6**，kimi-k2.5 写为 **kimi-k2-5**，glm-5.1 写为 **glm-5-1**，glm-5 写为 **glm-5-0**。

### Coding Plan

**API Key**

Coding Plan 专属 [API Key](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/coding_plan)

**Base URL**

`https://coding.dashscope.aliyuncs.com/v1`

**可用模型**

Coding Plan [支持的模型](https://help.aliyun.com/zh/model-studio/coding-plan)

部分模型名称需调整：kimi-k2.5 写为 **kimi-k2-5**，glm-4.7 写为 **glm-4-7**，glm-5 写为 **glm-5-0**。

### 按量计费

**API Key**

[阿里云百炼 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)

**Base URL**

根据地域，填入对应 URL：

-   华北2（北京）：`https://dashscope.aliyuncs.com/compatible-mode/v1`
    
-   新加坡：`https://dashscope-intl.aliyuncs.com/compatible-mode/v1`
    
-   美国（弗吉尼亚）：`https://dashscope-us.aliyuncs.com/compatible-mode/v1`
    

**可用模型**

填入[支持的模型](https://help.aliyun.com/zh/model-studio/compatibility-of-openai-with-dashscope#7f9c78ae99pwz)。

## **使用案例：接入百炼 CLI**

[百炼 CLI](https://bailian.console.aliyun.com/cli) 安装时会向 `~/.cursor/skills/bailian-cli/` 注册 Skill，Cursor 即可通过对话调用百炼能力，能力清单详见[百炼 CLI 控制台](https://bailian.console.aliyun.com/cli)。前置要求 [Node.js](https://nodejs.org/zh-cn/download) 18+。

1.  告诉 Cursor 安装百炼 CLI：
    
    ```
    请帮我全局安装阿里云百炼 CLI 命令行工具：npm install -g bailian-cli
    ```
    
2.  前往百炼控制台[获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，告诉 Cursor 配置：
    
    ```
    配置我的 API Key 是：sk-xxxxxxxxxxxxx
    ```
    
3.  直接用自然语言描述需求即可开始使用，例如：
    
    ```
    帮我生成 6 张亚马逊电商主图，产品是白色无线蓝牙耳机。
    ```
    ```
    帮我生成一段 30 秒的白色无线蓝牙耳机产品演示视频。
    ```
    

## **常见问题**

### 错误码

配置过程中遇到报错，请参考对应计费方案的常见问题文档：

-   按量付费：[错误信息](https://help.aliyun.com/zh/model-studio/error-code)
    
-   Coding Plan：[Coding Plan 常见问题](https://help.aliyun.com/zh/model-studio/coding-plan-faq)
    
-   Token Plan 团队版：[Token Plan 团队版常见问题](https://help.aliyun.com/zh/model-studio/token-plan-faq)
    

### 在 Cursor 中无法调用已添加的模型

报错信息如下：

-   The model xxx does not work with your current plan or api key.
    
-   Named models unavailable Free plans can only use Auto. Switch to Auto or upgrade plans to continue.
    

**原因**：Cursor 免费版仅支持 Auto 模式，不支持调用自定义模型。

**解决方案**：请升级至 **Cursor Pro 及以上套餐**。

### 配置完成后找不到添加的模型

请在聊天面板点击并关闭**Auto**模式，在模型下拉栏选择所需模型。

### 调用模型报错 "We're having trouble connecting to the model provider." 或 "Unauthorized User API key"

请逐项排查：

-   检查 API Key、Base URL 和模型名称是否与所选计费方案一致。不同方案的凭证不通用。
    
-   部分模型名称与 Cursor 内置模型名冲突，需使用别名。请参考上方可用模型中的说明。
