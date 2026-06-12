# QwenPaw

QwenPaw（原 CoPaw）是 AgentScope 团队开源的个人 AI 助手，支持本地或云端部署，可通过 Token Plan 团队版、Coding Plan 或按量计费接入阿里云百炼。

## **安装 QwenPaw**

推荐 pip 包或一键安装脚本。Docker、桌面端、ModelScope 在线运行等方式参考 [QwenPaw 官方文档](https://qwenpaw.agentscope.io/)。

## 一键脚本

脚本自动安装 uv、创建虚拟环境并下载依赖，无需手动配置 Python。根据操作系统选择对应命令：

-   macOS / Linux：
    
    ```
    curl -fsSL https://qwenpaw.agentscope.io/install.sh | bash
    ```
    
-   Windows（CMD）：
    
    ```
    curl -fsSL https://qwenpaw.agentscope.io/install.bat -o install.bat && install.bat
    ```
    
-   Windows（PowerShell）：
    
    ```
    irm https://qwenpaw.agentscope.io/install.ps1 | iex
    ```
    

安装完成后，在新终端执行：

```
qwenpaw init --defaults
qwenpaw app
```

## pip 安装

需 Python 3.10 ~ 3.13：

```
pip install qwenpaw
qwenpaw init --defaults
qwenpaw app
```

启动后访问 `http://127.0.0.1:8088/` 打开 QwenPaw Console。

## **配置接入凭证**

在 Console 点击 **设置** > **模型**，根据计费方案配置对应的提供商。

### Token Plan 团队版

进入内置的 **Aliyun Token Plan** 提供商**设置**页面，填入 API Key。

**配置项**

**说明**

**API 密钥**

填入 Token Plan 团队版专属 [API Key](https://bailian.console.aliyun.com/?tab=plan#/efm/subscription/overview)。

**模型**

已预设常用模型。新增模型点击**添加模型**，**模型 ID**填入 Token Plan 团队版[支持的模型](https://help.aliyun.com/zh/model-studio/token-plan-overview)。

### Coding Plan

进入内置的 **Aliyun Coding Plan (China)** 提供商**设置**页面，填入 API Key。

**配置项**

**说明**

**API 密钥**

填入 Coding Plan 专属 [API Key](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/coding_plan)。

**模型**

已预设常用模型，可在**模型**页面**测试连接**验证。新增模型点击**添加模型**，**模型 ID**填入 Coding Plan [支持的模型](https://help.aliyun.com/zh/model-studio/coding-plan)。

### 按量计费

进入内置的 **DashScope** 提供商**设置**页面，填入 API Key。基础 URL 默认为 China (Beijing)，可在下拉菜单切换地域。

**配置项**

**说明**

**API 密钥**

填入[阿里云百炼 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，需与所选地域对应。

**基础 URL**

根据模型部署地域，在下拉菜单选择对应 URL：

-   China (Beijing)：`https://dashscope.aliyuncs.com/compatible-mode/v1`
    
-   International (Singapore)：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`，将 `WorkspaceId` 替换为真实的[获取Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#d3eb3cd37b7fu)。
    
-   US (Virginia)：`https://dashscope-us.aliyuncs.com/compatible-mode/v1`
    

**模型**

已预设常用模型。新增模型点击**添加模型**，**模型 ID**填入[支持的模型](https://help.aliyun.com/zh/model-studio/compatibility-of-openai-with-dashscope#7f9c78ae99pwz)。

## **设置默认模型**

进入 **设置** > **模型** > **默认LLM** 选择模型并**保存**。聊天页面右上角下拉菜单可临时切换当前会话的提供商和模型。

## **常见问题**

### 错误码

按计费方案排查：

-   按量计费：[错误码排查](https://help.aliyun.com/zh/model-studio/error-code)
    
-   Coding Plan：[Coding Plan 常见问题](https://help.aliyun.com/zh/model-studio/coding-plan-faq)
    
-   Token Plan 团队版：[Token Plan 团队版常见问题](https://help.aliyun.com/zh/model-studio/token-plan-faq)
    

### 报错 401 Incorrect API key provided

可能原因：

-   三种计费方案的 API Key 不通用，确认与基础 URL 来自同一方案。
    
-   按量计费的 API Key 与基础 URL 不在同一地域。
    

### 长对话或工具调用时报错上下文超限

在该模型的提供商**设置**页面展开**进阶配置**，按 JSON 格式调整 `max_tokens` 等生成参数后保存：

```
{
  "temperature": 0.7,
  "top_p": 0.9,
  "max_tokens": 4096
}
```
