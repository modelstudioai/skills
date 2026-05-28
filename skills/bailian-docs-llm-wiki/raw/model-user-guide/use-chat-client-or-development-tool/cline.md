# Cline

Cline 是一款 VSCode 智能编程插件，可以通过 Token Plan 团队版、Coding Plan或按量计费接入阿里云百炼。

## **安装 Cline**

1.  下载并安装 [VSCode](https://code.visualstudio.com/)。
    
2.  打开 VSCode，在扩展商店搜索 `Cline` 并安装。
    

## **配置接入凭证**

安装完成后，点击左侧边栏的 Cline 图标进入配置界面。点击 **Bring my own API key**，选择 **OpenAI Compatible** 作为 API Provider，根据所选方案填入对应参数。如果之前使用过 Cline，请点击右上角的设置按钮进入配置界面。

阿里云百炼提供三种计费方案，根据需要选择：

-   **Token Plan 团队版**：按坐席订阅，按 token 消耗抵扣 Credits。
    
-   **Coding Plan**：固定月费订阅，按模型调用次数计量。
    
-   **按量计费**：按实际调用量后付费。
    

### Token Plan 团队版

**配置项**

**说明**

API Provider

选择 **OpenAI Compatible**。

Base URL

`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`

API Key

填入 Token Plan 团队版专属 [API Key](https://bailian.console.aliyun.com/?tab=plan#/efm/subscription/overview)。

Model ID

填入 Token Plan 团队版[支持的模型](https://help.aliyun.com/zh/model-studio/token-plan-overview)，如 `qwen3.7-max`。

### Coding Plan

**配置项**

**说明**

API Provider

选择 **OpenAI Compatible**。

Base URL

`https://coding.dashscope.aliyuncs.com/v1`

API Key

填入 Coding Plan 专属 [API Key](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/coding_plan)。

Model ID

填入 Coding Plan [支持的模型](https://help.aliyun.com/zh/model-studio/coding-plan)，如 `qwen3.6-plus`。

### 按量计费

**配置项**

**说明**

API Provider

选择 **OpenAI Compatible**。

Base URL

根据地域，填入对应 URL：

-   华北2（北京）：`https://dashscope.aliyuncs.com/compatible-mode/v1`
    
-   新加坡：`https://dashscope-intl.aliyuncs.com/compatible-mode/v1`
    
-   美国（弗吉尼亚）：`https://dashscope-us.aliyuncs.com/compatible-mode/v1`
    

API Key

填入[阿里云百炼 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，需与所选地域对应。

Model ID

填入[支持的模型](https://help.aliyun.com/zh/model-studio/compatibility-of-openai-with-dashscope#7f9c78ae99pwz)。

如果使用 Qwen3（思考模式）或 QwQ 模型，需在设置界面点击 `MODEL CONFIGURATION`，勾选 **Enable R1 messages format**。

## **使用案例：接入百炼 CLI**

[百炼 CLI](https://bailian.console.aliyun.com/cli) 安装时会向 `~/.cline/skills/bailian-cli/` 注册 Skill，Cline 即可通过对话调用百炼能力，能力清单详见[百炼 CLI 控制台](https://bailian.console.aliyun.com/cli)。前置要求 [Node.js](https://nodejs.org/zh-cn/download) 18+。

1.  告诉 Cline 安装百炼 CLI：
    
    ```
    请帮我全局安装阿里云百炼 CLI 命令行工具：npm install -g bailian-cli
    ```
    
2.  前往百炼控制台[获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，告诉 Cline 配置：
    
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
    

### 报错 401 Incorrect API key provided

可能原因：

-   API Key 与 Base URL 不匹配。三种计费方案的 API Key 不通用，请确认 API Key 和 Base URL 来自同一方案。
    
-   按量计费的 API Key 与 Base URL 的地域不一致，请检查二者是否对应同一地域。
    

### 报错 400 InternalError.Algo.InvalidParameter

请在设置界面点击 `MODEL CONFIGURATION`，勾选 **Enable R1 messages format**。
