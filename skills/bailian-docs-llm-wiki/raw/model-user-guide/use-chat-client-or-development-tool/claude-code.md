# Claude Code

Claude Code 是 Anthropic 推出的命令行 AI 编程助手。通过阿里云百炼，可以使用按量计费、Coding Plan 或 Token Plan 团队版接入 Claude Code。

## **安装 Claude Code**

### 安装

## **macOS**

1.  安装或更新 [Node.js](https://nodejs.org/en/download/)（v18.0 或更高版本）。
    
2.  在终端中执行以下命令安装 Claude Code。
    
    ```
    npm install -g @anthropic-ai/claude-code
    ```
    
3.  验证安装结果。输出版本号即表示安装成功。
    
    ```
    claude --version
    ```
    

## **Windows**

在 Windows 上使用 Claude Code，需先安装 WSL 或 [Git for Windows](https://git-scm.com/install/windows)，然后在 WSL 或 Git Bash 中执行以下命令。

```
npm install -g @anthropic-ai/claude-code
```

> 详情参见 Claude Code 官方文档的 [Windows 安装教程](https://docs.anthropic.com/en/docs/claude-code/setup#windows-setup) 。

### 跳过登录验证

编辑或新建 `~/.claude.json`（Windows 路径：`C:\Users\<用户名>\.claude.json`），将 `hasCompletedOnboarding` 设为 `true`，跳过 Anthropic 官方登录验证。

```
{
  "hasCompletedOnboarding": true
}
```

## **配置接入凭证**

新建 `~/.claude/settings.json`（Windows 路径：`C:\Users\<用户名>\.claude\settings.json`），写入对应套餐的配置。

### Token Plan 团队版

将 YOUR\_API\_KEY 替换为 Token Plan 团队版专属 [API Key](https://bailian.console.aliyun.com/?tab=plan#/efm/subscription/overview)。可用模型参见 Token Plan 团队版[支持的模型](https://help.aliyun.com/zh/model-studio/token-plan-overview)。

```
{
    "env": {
        "ANTHROPIC_AUTH_TOKEN": "YOUR_API_KEY",
        "ANTHROPIC_BASE_URL": "https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic",
        "ANTHROPIC_MODEL": "qwen3.7-max",
        "ANTHROPIC_DEFAULT_HAIKU_MODEL": "qwen3.6-flash",
        "ANTHROPIC_DEFAULT_SONNET_MODEL": "qwen3.7-max",
        "ANTHROPIC_DEFAULT_OPUS_MODEL": "qwen3.7-max",
        "CLAUDE_CODE_SUBAGENT_MODEL": "qwen3.7-max"
    }
}
```

### Coding Plan

将 YOUR\_API\_KEY 替换为 Coding Plan 专属 [API Key](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/coding_plan)。可用模型参见 Coding Plan [支持的模型](https://help.aliyun.com/zh/model-studio/coding-plan)。

```
{
    "env": {
        "ANTHROPIC_AUTH_TOKEN": "YOUR_API_KEY",
        "ANTHROPIC_BASE_URL": "https://coding.dashscope.aliyuncs.com/apps/anthropic",
        "ANTHROPIC_MODEL": "qwen3.6-plus",
        "ANTHROPIC_DEFAULT_HAIKU_MODEL": "qwen3.6-plus",
        "ANTHROPIC_DEFAULT_SONNET_MODEL": "qwen3.6-plus",
        "ANTHROPIC_DEFAULT_OPUS_MODEL": "qwen3.6-plus",
        "CLAUDE_CODE_SUBAGENT_MODEL": "qwen3.6-plus"
    }
}
```

### 按量计费

将 YOUR\_API\_KEY 替换为[阿里云百炼API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。可用模型参见[Anthropic 兼容 API](https://help.aliyun.com/zh/model-studio/anthropic-api-messages#07833dedefft7)。

`ANTHROPIC_BASE_URL` 按地域设置，API Key 需与所选地域对应：

-   华北2（北京）：`https://dashscope.aliyuncs.com/apps/anthropic`
    
-   新加坡：`https://dashscope-intl.aliyuncs.com/apps/anthropic`
    

```
{
    "env": {
        "ANTHROPIC_AUTH_TOKEN": "YOUR_API_KEY",
        "ANTHROPIC_BASE_URL": "https://dashscope.aliyuncs.com/apps/anthropic",
        "ANTHROPIC_MODEL": "qwen3.7-max",
        "ANTHROPIC_DEFAULT_HAIKU_MODEL": "qwen3.6-flash",
        "ANTHROPIC_DEFAULT_SONNET_MODEL": "qwen3.7-max",
        "ANTHROPIC_DEFAULT_OPUS_MODEL": "qwen3.7-max",
        "CLAUDE_CODE_SUBAGENT_MODEL": "qwen3.7-max"
    }
}
```

配置保存后，新开一个终端窗口执行 `claude "你好"`。若模型正常返回响应，配置成功。如需进一步确认，在 Claude Code 中执行 `/status`，检查 `ANTHROPIC_BASE_URL` 和 `ANTHROPIC_AUTH_TOKEN` 是否正确指向百炼地址。

## **使用 CC Switch**

[CC Switch](https://github.com/farion1231/cc-switch) 是社区开源的桌面 GUI，支持在多个API Key 或计费套餐之间一键切换，无需手动修改 `settings.json`。

### 安装

-   macOS：执行 `brew tap farion1231/ccswitch && brew install --cask cc-switch`，或从 [Releases](https://github.com/farion1231/cc-switch/releases) 下载 `.dmg`。
    
-   Windows：从 [Releases](https://github.com/farion1231/cc-switch/releases) 下载 `.msi` 安装包或便携版 `.zip`。
    
-   Linux：Arch 发行版执行 `paru -S cc-switch-bin`；其他发行版从 [Releases](https://github.com/farion1231/cc-switch/releases) 下载 `.deb` / `.rpm` / `.AppImage`。
    

### 添加供应商

1.  在 CC Switch 主界面顶部图标栏选中 Claude Code 橙色星形图标，点击右上角 **+** 进入**添加新供应商**，按下表填入配置后点击**添加**。
    
    **计费方案**
    
    **配置信息**
    
    Token Plan 团队版
    
    供应商名称：百炼-Token Plan
    
    API Key：[控制台获取](https://bailian.console.aliyun.com/?tab=plan#/efm/subscription/overview)
    
    请求地址：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`
    
    Coding Plan
    
    供应商名称：百炼-Coding Plan
    
    API Key：[控制台获取](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/coding_plan)
    
    请求地址：`https://coding.dashscope.aliyuncs.com/apps/anthropic`
    
    按量计费
    
    供应商名称：百炼-按量计费
    
    API Key：[百炼API Key](https://help.aliyun.com/zh/model-studio/get-api-key)
    
    请求地址：`https://dashscope.aliyuncs.com/apps/anthropic`
    
2.  展开**高级选项**配置模型映射，将主模型与 Haiku、Sonnet、Opus 默认模型设置为对应套餐[支持的模型](https://help.aliyun.com/zh/model-studio/token-plan-overview)。映射关系按需选择，示例如下：
    
    -   主模型：`qwen3.7-max`（Coding Plan 不支持）
        
    -   Haiku 默认模型：`qwen3.6-flash`（Coding Plan 不支持）
        
    -   Sonnet 默认模型：`qwen3.7-max`（Coding Plan 不支持）
        
    -   Opus 默认模型：`qwen3.7-max`（Coding Plan 不支持）
        
3.  回到主界面，点击该供应商右侧**启用**按钮，然后新开一个 Claude Code 会话使配置生效。
    

### 接入 Claude Code 桌面版

1.  从 [Claude 下载页](https://claude.ai/download)安装 Claude Code 桌面版。
    
2.  顶部菜单 **Help** → **Troubleshooting** → **Enable Developer Mode**，重启后顶部出现 **Developer** 菜单。
    
3.  **Developer** → **Configure Third-Party Inference**，**Connection** 选 **Gateway**，按下表填写后点击 **Apply locally**：
    
    **字段**
    
    **填写**
    
    Gateway base URL
    
    CC Switch 路由监听地址，默认 `http://127.0.0.1:15721`，如已修改则与下一步保持一致。
    
    Gateway API key
    
    百炼API Key
    
    Gateway auth scheme
    
    bearer
    
    Model list
    
    Model ID须为 Anthropic 风格，如 `claude-opus-4.7`。实际调用模型由 CC Switch 路由决定，对应关系即供应商[高级选项中的模型映射](#ccswitch-add-li2)。Display name 仅影响下拉显示。
    
4.  CC Switch 左上角设置 → **路由**，开启**路由总开关**，监听地址默认 `127.0.0.1:15721`，如需修改请同步上一步。
    
5.  在桌面版模型下拉中选择已配置的模型ID即可使用。
    

## **Claude Code IDE 插件**

完成上述 CLI 配置后，在 IDE 中安装 Claude Code 插件，可直接复用 `settings.json` 中的配置。

### VS Code

1.  在扩展市场搜索 `Claude Code for VS Code` 并安装。
    
2.  重启 VS Code，点击右上角图标进入 Claude Code。
    
3.  在对话框中输入 `/`，选择 General config，在 Selected Model 中设置模型。
    

### JetBrains

1.  在扩展市场搜索 `Claude Code` 并安装。
    
2.  重启 IDE，点击右上角图标即可使用。
    

## **使用案例：接入百炼 CLI**

[百炼 CLI](https://bailian.console.aliyun.com/cli) 安装时会向 `~/.claude/skills/bailian-cli/` 注册 Skill，Claude Code 即可通过对话调用百炼能力，能力清单详见[百炼 CLI 控制台](https://bailian.console.aliyun.com/cli)。前置要求 [Node.js](https://nodejs.org/zh-cn/download) 18+。

1.  告诉 Claude Code 安装百炼 CLI：
    
    ```
    请帮我全局安装阿里云百炼 CLI 命令行工具：npm install -g bailian-cli
    ```
    
2.  前往百炼控制台[获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，告诉 Claude Code 配置：
    
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

配置过程中遇到报错，参考对应套餐的常见问题文档：

-   按量计费：[Anthropic API兼容 - 错误码](https://help.aliyun.com/zh/model-studio/anthropic-api-messages#7d8d58d0736zv)
    
-   Coding Plan：[Coding Plan 常见问题](https://help.aliyun.com/zh/model-studio/coding-plan-faq)
    
-   Token Plan 团队版：[Token Plan 团队版常见问题](https://help.aliyun.com/zh/model-studio/token-plan-faq)
    

### 启动 Claude Code 后，界面显示"Unable to connect to Anthropic services. Failed to connect to api.anthropic.com: ERR\_BAD\_REQUEST"

此错误表示 Claude Code 正在尝试连接 Anthropic 官方服务而非阿里云百炼。通常是环境变量未正确配置或未生效。按以下步骤排查：

1.  **检查配置。**启动 Claude Code 后执行 `/status` 命令，确认 `ANTHROPIC_BASE_URL` 和 `ANTHROPIC_AUTH_TOKEN` 是否正确指向百炼地址。输出为空或指向非百炼地址时，检查 `settings.json` 配置是否正确。
    
2.  **确认 hasCompletedOnboarding。**检查 `~/.claude.json` 文件中 `hasCompletedOnboarding` 是否设置为 `true`。未设置时，Claude Code 启动后会尝试连接 Anthropic 官方服务进行登录验证。
    
3.  **重新打开终端。**修改配置文件后，需要新开一个终端窗口再执行 `claude`，配置才会生效。
    

### 使用旧版接口，切换模型不生效

旧版兼容接口 `https://dashscope.aliyuncs.com/api/v2/apps/claude-code-proxy` 仅支持 `qwen3-coder-plus` 模型，指定其他模型不会生效。如需调用其他模型，按本文配置迁移至新版接口。
