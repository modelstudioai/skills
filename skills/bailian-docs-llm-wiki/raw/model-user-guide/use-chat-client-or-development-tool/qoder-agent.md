# Qoder

Qoder 是面向软件开发的 Agentic 编码平台，支持桌面 IDE、CLI 和 JetBrains 插件，可以通过按量付费、Coding Plan 或 Token Plan 团队版接入阿里云百炼。

## Qoder IDE

### 安装

1.  前往 [Qoder 官网](https://qoder.com/)下载并安装 Qoder。
    
2.  初次启动后完成初始配置并登录 Qoder 账号。
    

### 配置接入凭证

1.  在界面右上角打开 Qoder 设置，选择**模型**，点击**添加**。
    
2.  模型配置信息如下：
    
    **配置项**
    
    **说明**
    
    提供商
    
    在下拉菜单中选择 阿里云百炼 - 国内
    
    类型
    
    根据计费方案选择 **Token Plan**、**Coding Plan** 或 **按量付费**
    
    模型
    
    在下拉菜单中选择模型，仅支持文本生成模型。
    
    API Key
    
    填写对应方案的专属 API Key：
    
    -   Token Plan 团队版：[获取 API Key](https://bailian.console.aliyun.com/?tab=plan#/efm/subscription/overview)
        
    -   Coding Plan：[获取 API Key](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/coding_plan)
        
    -   按量计费：[获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)
        
    
3.  点击**添加**，通过校验后即可完成模型配置。
    
4.  在模型列表中选择对应模型即可开始使用。
    

## Qoder CLI

### 安装

1.  在终端执行以下命令安装。
    
    ```
    curl -fsSL https://qoder.com/install | bash
    ```
    
2.  验证安装是否成功。
    
    ```
    qodercli --version
    ```
    
    若输出版本号，则安装成功。
    

### 登录 Qoder

使用前需完成身份验证，有两种方式：

1.  **通过 TUI 登录（推荐）**
    
    1.  执行 `qodercli` 进入交互界面，在对话框中输入 `/login`。
        
    2.  选择 `login with browser` 或 `login with qoder personal access token` 完成登录。
        
2.  **通过环境变量登录**
    
    适用于非交互式环境（如 CI/CD 流水线）。将 `your_personal_access_token_here` 替换为实际的 Token，可在 [服务集成页面](https://qoder.com/account/integrations)获取。
    
    ## **macOS/Linux**
    
    ```
    export QODER_PERSONAL_ACCESS_TOKEN="your_personal_access_token_here"
    ```
    
    ## Windows
    
    ```
    set QODER_PERSONAL_ACCESS_TOKEN=your_personal_access_token_here
    ```
    

### 配置接入凭证

1.  在对话框中输入 `/model`，通过 Tab 键切换至 `Custom`。
    
2.  回车选择 Add custom model，提供商选择 Alibaba Cloud Model Studio - China，类型根据计费方案选择 **Token Plan**、**Coding Plan** 或 **按量付费**。
    
3.  选择模型后输入对应方案的专属 API Key，确认后等待配置生效。
    

### 使用 Qoder CLI

1.  重启 Qoder CLI。
    
    ```
    qodercli
    ```
    
2.  在对话框中输入 `/model`，通过 Tab 键切换至 `Custom`，选择已配置的模型即可开始使用。
    

## JetBrains 插件

1.  打开 JetBrains IDE（如 IntelliJ IDEA、PyCharm 等），在扩展市场中搜索 `Qoder` 并安装。
    
2.  点击右侧导航栏中的 Qoder，在 Qoder 对话面板中完成登录。
    
3.  点击右上角设置，选择**插件设置**，在弹出界面选择**添加模型**。
    
4.  配置信息如下：
    
    **配置项**
    
    **说明**
    
    提供商
    
    在下拉菜单中选择 阿里云百炼 - 国内
    
    类型
    
    根据计费方案选择 **Token Plan**、**Coding Plan** 或 **按量付费**
    
    模型
    
    在下拉菜单中选择模型，仅支持文本生成模型。
    
    API Key
    
    填写对应方案的专属 API Key：
    
    -   Token Plan 团队版：[获取 API Key](https://bailian.console.aliyun.com/?tab=plan#/efm/subscription/overview)
        
    -   Coding Plan：[获取 API Key](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/coding_plan)
        
    -   按量计费：[获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)
        
    
    配置完成后，点击**确定**，等待配置生效。
    
5.  在自定义模型中选择已配置的模型进行对话。
    

## 了解更多

如需进一步了解 Qoder 的智能体、MCP、Skills 等扩展能力，请参考 [Qoder 官方文档](https://docs.qoder.com/)。

## **使用案例：接入百炼 CLI**

[百炼 CLI](https://bailian.console.aliyun.com/cli) 安装时会向 `~/.qoder/skills/bailian-cli/` 注册 Skill，Qoder 即可通过对话调用百炼能力，能力清单详见[百炼 CLI 控制台](https://bailian.console.aliyun.com/cli)。前置要求 [Node.js](https://nodejs.org/zh-cn/download) 18+。

1.  告诉 Qoder 安装百炼 CLI：
    
    ```
    请帮我全局安装阿里云百炼 CLI 命令行工具：npm install -g bailian-cli
    ```
    
2.  前往百炼控制台[获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，告诉 Qoder 配置：
    
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
    

## 常见问题

### 错误码

配置过程中遇到报错，请参考对应计费方案的常见问题文档：

-   Coding Plan：[Coding Plan 常见问题](https://help.aliyun.com/zh/model-studio/coding-plan-faq)
    
-   Token Plan 团队版：[Token Plan 团队版常见问题](https://help.aliyun.com/zh/model-studio/token-plan-faq)
    

### 为什么在 Qoder 设置中找不到模型选项？

可能有以下原因：

-   **未完成登录**：需要先完成登录，才能进行对话和配置模型。
    
-   **当前版本不支持**：建议更新至最新版本（0.16.0 及以上）。
