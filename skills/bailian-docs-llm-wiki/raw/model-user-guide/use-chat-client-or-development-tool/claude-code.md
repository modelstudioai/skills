# Claude Code

Claude Code 是 Anthropic 推出的命令行 AI 编程助手。通过阿里云百炼，可以使用按量计费、Coding Plan、Token Plan 个人版或 Token Plan 团队版接入 Claude Code。

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

若您此前使用旧版兼容接口 `https://dashscope.aliyuncs.com/api/v2/apps/claude-code-proxy`（仅支持 `qwen3-coder-plus` 模型），请按本文配置迁移至新版接口，详见下文 FAQ“使用旧版接口，切换模型不生效”。

### Token Plan 个人版

将 YOUR\_API\_KEY 替换为 Token Plan 个人版专属 [API Key](https://bailian.console.aliyun.com/cn-beijing?tab=plan#/efm/subscription/overview)。可用模型参见 Token Plan 个人版[支持的模型](https://help.aliyun.com/zh/model-studio/token-plan-personal-overview)。

```
{
    "env": {
        "ANTHROPIC_AUTH_TOKEN": "YOUR_API_KEY",
        "ANTHROPIC_BASE_URL": "https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic",
        "ANTHROPIC_MODEL": "qwen3.8-max",
        "ANTHROPIC_DEFAULT_HAIKU_MODEL": "qwen3.6-flash",
        "ANTHROPIC_DEFAULT_SONNET_MODEL": "qwen3.8-max",
        "ANTHROPIC_DEFAULT_OPUS_MODEL": "qwen3.8-max",
        "CLAUDE_CODE_SUBAGENT_MODEL": "qwen3.7-max",
        "CLAUDE_CODE_MAX_CONTEXT_TOKENS": "983616"
    }
}
```

**提示**：上述配置将 `CLAUDE_CODE_SUBAGENT_MODEL` 设为 `qwen3.7-max`，子任务（如文件搜索、Plan 模式）将使用该模型。如需子任务也使用 `qwen3.8-max`，可将 `CLAUDE_CODE_SUBAGENT_MODEL` 改为 `qwen3.8-max`。

### Token Plan 团队版

将 YOUR\_API\_KEY 替换为 Token Plan 团队版专属 [API Key](https://bailian.console.aliyun.com/cn-beijing?tab=plan#/efm/subscription/uac-admin/organization/members/list)。可用模型参见 Token Plan 团队版[支持的模型](https://help.aliyun.com/zh/model-studio/token-plan-overview)。

```
{
    "env": {
        "ANTHROPIC_AUTH_TOKEN": "YOUR_API_KEY",
        "ANTHROPIC_BASE_URL": "https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic",
        "ANTHROPIC_MODEL": "qwen3.8-max",
        "ANTHROPIC_DEFAULT_HAIKU_MODEL": "qwen3.6-flash",
        "ANTHROPIC_DEFAULT_SONNET_MODEL": "qwen3.8-max",
        "ANTHROPIC_DEFAULT_OPUS_MODEL": "qwen3.8-max",
        "CLAUDE_CODE_SUBAGENT_MODEL": "qwen3.7-max",
        "CLAUDE_CODE_MAX_CONTEXT_TOKENS": "983616"
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
        "ANTHROPIC_MODEL": "qwen3.7-plus",
        "ANTHROPIC_DEFAULT_HAIKU_MODEL": "qwen3.7-plus",
        "ANTHROPIC_DEFAULT_SONNET_MODEL": "qwen3.7-plus",
        "ANTHROPIC_DEFAULT_OPUS_MODEL": "qwen3.7-plus",
        "CLAUDE_CODE_SUBAGENT_MODEL": "qwen3.7-plus"
    }
}
```

### 按量计费

将 YOUR\_API\_KEY 替换为[阿里云百炼API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。可用模型参见[Anthropic 兼容 API](https://help.aliyun.com/zh/model-studio/anthropic-api-messages#07833dedefft7)。

`ANTHROPIC_BASE_URL` 按地域设置，API Key 需与所选地域对应，并将`WorkspaceId`替换为真实的 [Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#d3eb3cd37b7fu)：

-   华北2（北京）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic`
    
-   新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/apps/anthropic`
    

```
{
    "env": {
        "ANTHROPIC_AUTH_TOKEN": "YOUR_API_KEY",
        "ANTHROPIC_BASE_URL": "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic",
        "ANTHROPIC_MODEL": "qwen3.7-max",
        "ANTHROPIC_DEFAULT_HAIKU_MODEL": "qwen3.6-flash",
        "ANTHROPIC_DEFAULT_SONNET_MODEL": "qwen3.7-max",
        "ANTHROPIC_DEFAULT_OPUS_MODEL": "qwen3.7-max",
        "CLAUDE_CODE_SUBAGENT_MODEL": "qwen3.7-max"
    }
}
```

配置保存后，新开一个终端窗口执行 `claude "你好"`。若模型正常返回响应，配置成功。如需进一步确认，在 Claude Code 中执行 `/status`，检查 `ANTHROPIC_BASE_URL` 和 `ANTHROPIC_AUTH_TOKEN` 是否正确指向百炼地址。

### 配置上下文窗口大小

Claude Code 默认使用 200K 上下文窗口。如果需要处理大型代码仓库或长对话，可以将上下文窗口扩展到 1M（1,000,000 tokens），前提是所用模型支持该上下文长度。有两种配置方式：

**方式一：通过环境变量设置**

在 `~/.claude/settings.json` 的 `env` 字段中添加 `CLAUDE_CODE_MAX_CONTEXT_TOKENS`：

```
{
    "env": {
        "ANTHROPIC_AUTH_TOKEN": "YOUR_API_KEY",
        "ANTHROPIC_BASE_URL": "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic",
        "ANTHROPIC_MODEL": "qwen3.7-plus",
        "CLAUDE_CODE_MAX_CONTEXT_TOKENS": "1000000"
    }
}
```

**方式二：通过模型名称后缀**

在模型名称后添加 `[1m]` 后缀，适用于百炼支持 1M 上下文的模型：

```
{
    "env": {
        "ANTHROPIC_AUTH_TOKEN": "YOUR_API_KEY",
        "ANTHROPIC_BASE_URL": "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic",
        "ANTHROPIC_MODEL": "qwen3.7-plus[1m]",
        "ANTHROPIC_DEFAULT_SONNET_MODEL": "qwen3.7-plus[1m]",
        "ANTHROPIC_DEFAULT_OPUS_MODEL": "qwen3.7-plus[1m]",
        "CLAUDE_CODE_SUBAGENT_MODEL": "qwen3.7-plus[1m]"
    }
}
```

修改配置后，需新开终端窗口重新启动 Claude Code 使配置生效。更多环境变量说明参见 [Claude Code 官方环境变量文档](https://code.claude.com/docs/zh-CN/env-vars)。

## **权限模式配置**

Claude Code 提供 6 种权限模式，控制工具执行操作时的确认行为：

**模式**

**行为**

`default`

每次操作询问用户确认。

`acceptEdits`

自动批准文件编辑，其他操作仍询问。

`plan`

只读规划模式，不执行修改。

`dontAsk`

不询问，需要询问的操作直接拒绝。

`bypassPermissions`

绕过所有权限检查。

`delegate`

委托模式。

### 命令行参数

使用 `--permission-mode` 指定本次会话的默认权限模式：

```
claude --permission-mode plan
claude --permission-mode acceptEdits
```

### 交互命令

在会话中输入 `/permissions`，可动态管理工具的预批准（pre-approve）和预拒绝（pre-deny）规则，支持配置 bash、edit 和 MCP 工具的规则。

### settings.json 配置

在 `~/.claude/settings.json`（Windows 路径：`C:\Users\<用户名>\.claude\settings.json`）中配置 `permissions` 字段：

```
{
    "permissions": {
        "allow": ["Bash(git:*)", "Read", "Edit"],
        "deny": ["Bash(rm:*)"],
        "defaultMode": "default"
    }
}
```

`allow` 自动批准匹配的工具调用，`deny` 自动拒绝匹配的工具调用。规则支持通配符，例如 `Bash(npm:*)` 匹配所有以 npm 开头的命令。`defaultMode` 设置会话的默认权限模式，取值为上表 6 种模式之一。

## **使用 CC Switch**

[CC Switch](https://github.com/farion1231/cc-switch) 是社区开源的桌面 GUI，支持在多个API Key 或计费套餐之间一键切换，无需手动修改 `settings.json`。该工具为第三方软件，其脚本与代码不受阿里云审核和维护，安装使用前请自行评估其来源可信度与代码安全性。

### 安装

-   macOS：执行 `brew tap farion1231/ccswitch && brew install --cask cc-switch`，或从 [Releases](https://github.com/farion1231/cc-switch/releases) 下载 `.dmg`。
    
-   Windows：从 [Releases](https://github.com/farion1231/cc-switch/releases) 下载 `.msi` 安装包或便携版 `.zip`。
    
-   Linux：Arch 发行版执行 `paru -S cc-switch-bin`；其他发行版从 [Releases](https://github.com/farion1231/cc-switch/releases) 下载 `.deb` / `.rpm` / `.AppImage`。
    

### 添加供应商

1.  在 CC Switch 主界面顶部图标栏选中 Claude Code 橙色星形图标，点击右上角 **+** 进入**添加新供应商**，按下表填入配置后点击**添加**。
    
    **计费方案**
    
    **配置信息**
    
    Token Plan 个人版
    
    供应商名称：百炼-Token Plan 个人版
    
    API Key：[控制台获取](https://bailian.console.aliyun.com/cn-beijing?tab=plan#/efm/subscription/overview)
    
    请求地址：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`
    
    Token Plan 团队版
    
    供应商名称：百炼-Token Plan 团队版
    
    API Key：[控制台获取](https://bailian.console.aliyun.com/cn-beijing?tab=plan#/efm/subscription/uac-admin/organization/members/list)
    
    请求地址：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`
    
    Coding Plan
    
    供应商名称：百炼-Coding Plan
    
    API Key：[控制台获取](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/coding_plan)
    
    请求地址：`https://coding.dashscope.aliyuncs.com/apps/anthropic`
    
    按量计费
    
    供应商名称：百炼-按量计费
    
    API Key：[百炼API Key](https://help.aliyun.com/zh/model-studio/get-api-key)
    
    请求地址：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic`
    
2.  展开**高级选项**配置模型映射，将主模型与 Haiku、Sonnet、Opus 默认模型设置为对应套餐[支持的模型](https://help.aliyun.com/zh/model-studio/token-plan-overview)。映射关系按需选择，示例如下：
    
    -   主模型：`qwen3.7-max`（Coding Plan 不支持，可填 qwen3.7-plus）
        
    -   Haiku 默认模型：`qwen3.6-flash`（Coding Plan 不支持，可填 qwen3.7-plus）
        
    -   Sonnet 默认模型：`qwen3.7-max`（Coding Plan 不支持，可填 qwen3.7-plus）
        
    -   Opus 默认模型：`qwen3.7-max`（Coding Plan 不支持，可填 qwen3.7-plus）
        
3.  回到主界面，点击该供应商右侧**启用**按钮，然后新开一个 Claude Code 会话使配置生效。
    

### 接入 Claude Code 桌面版

Claude Code 桌面版（Claude Desktop）与 Claude Code CLI 是两个独立入口，在 CC Switch 中分别对应 **Claude Code** 与 **Claude Desktop** 面板。桌面版通过 CC Switch 本地网关访问百炼：网关地址与鉴权令牌均由 CC Switch 自动写入桌面版配置，**无需在桌面版中手动填写百炼 API Key**——百炼 API Key 只在 CC Switch 供应商配置中填写，由本地路由转发时自动注入。

**重要**

请勿在桌面版的第三方推理配置中手动填写百炼 API Key。桌面版对 CC Switch 本地网关（地址 `http://127.0.0.1:15721/claude-desktop`）的鉴权令牌由 CC Switch 自动生成并写入，手动填入百炼 API Key 会因令牌不匹配导致鉴权失败。桌面版第三方配置写入目前仅支持 macOS、Windows。

1.  从 [Claude 下载页](https://claude.ai/download)安装 Claude Code 桌面版。
    
2.  在 CC Switch 左侧应用切换器切换到 **Claude Desktop** 面板。若未显示该入口，前往**设置 → 通用 → 应用可见性**确认 Claude Desktop 未被隐藏。
    
3.  添加百炼供应商：若已在 **Claude Code** 面板配置过百炼供应商，可点击**将 Claude Code 中已有的供应商导入**一键复用；也可点击右上角 **+** 新增。由于百炼模型 ID（如 `qwen3.7-max`）不是 Claude Desktop 识别的 `claude-sonnet-* / claude-opus-* / claude-haiku-*` 三档角色 ID，需开启**需要模型映射**，为 Sonnet、Opus、Haiku 三档分别填写实际请求的百炼模型（如 Sonnet → qwen3.7-max）。
    
4.  开启本地路由：前往**设置 → 路由 → 本地路由**，打开**在主页面显示本地路由开关**；回到 Claude Desktop 面板，打开 **Claude Desktop 本地路由**开关，监听地址默认 `127.0.0.1:15721`。
    
5.  在供应商卡片点击**启用**，CC Switch 会自动将第三方推理配置写入 Claude Code 桌面版。
    
6.  保持 CC Switch 运行，**完全退出并重启** Claude Code 桌面版后生效，在模型菜单中选择已配置的模型即可使用。
    

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
    
-   Token Plan 个人版：[Token Plan 常见问题](https://help.aliyun.com/zh/model-studio/token-plan-team-faq)
    
-   Token Plan 团队版：[Token Plan 团队版常见问题](https://help.aliyun.com/zh/model-studio/token-plan-team-faq)
    

### 调用时返回 401 invalid\_api\_key

此错误表示 API Key 类型与 `ANTHROPIC_BASE_URL` 不匹配。百炼提供三种接入方式，每种方式使用不同的 `base_url` 和专属 API Key，两者必须配套使用：

**接入方式**

**base\_url**

**API Key**

按量计费

`https://dashscope.aliyuncs.com/apps/anthropic`

百炼 API Key（`sk-` 开头）

Coding Plan

`https://coding.dashscope.aliyuncs.com/apps/anthropic`

Coding Plan 专属 API Key

Token Plan 团队版

`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`

Token Plan 团队版专属 API Key

排查步骤如下：

1.  **检查请求地址。**查看 `~/.claude/settings.json` 中 `ANTHROPIC_BASE_URL` 的取值。
    
2.  **确认 API Key 类型。**对照上表，确认所用 API Key 的类型与 `base_url` 匹配。
    
3.  **修正配置。**使用百炼按量计费 API Key 时，将 `ANTHROPIC_BASE_URL` 设为 `https://dashscope.aliyuncs.com/apps/anthropic`。
    

### 启动 Claude Code 后，界面显示"Unable to connect to Anthropic services. Failed to connect to api.anthropic.com: ERR\_BAD\_REQUEST"

此错误表示 Claude Code 正在尝试连接 Anthropic 官方服务而非阿里云百炼。通常是环境变量未正确配置或未生效。按以下步骤排查：

1.  **检查配置。**启动 Claude Code 后执行 `/status` 命令，确认 `ANTHROPIC_BASE_URL` 和 `ANTHROPIC_AUTH_TOKEN` 是否正确指向百炼地址。输出为空或指向非百炼地址时，检查 `settings.json` 配置是否正确。
    
2.  **确认 hasCompletedOnboarding。**检查 `~/.claude.json` 文件中 `hasCompletedOnboarding` 是否设置为 `true`。未设置时，Claude Code 启动后会尝试连接 Anthropic 官方服务进行登录验证。
    
3.  **重新打开终端。**修改配置文件后，需要新开一个终端窗口再执行 `claude`，配置才会生效。
    
4.  **更新 Claude Code。**若以上步骤均无效，可能是 Claude Code 版本过旧导致。执行 `npm install -g @anthropic-ai/claude-code@latest` 更新到最新版本后重试。
    

### 使用旧版接口，切换模型不生效

旧版兼容接口 `https://dashscope.aliyuncs.com/api/v2/apps/claude-code-proxy` 仅支持 `qwen3-coder-plus` 模型，指定其他模型不会生效。如需调用其他模型，按本文配置迁移至新版接口。

### 使用 CC Switch 添加供应商时提示"未找到可用的模型列表端点，请检查 Base URL 或确认供应商是否开放端口"

该提示来自 CC Switch 保存供应商时的连通性检查——它会向配置的请求地址探测模型列表端点（如 `/v1/models`）。百炼的 Anthropic 兼容接入端点（以 `/apps/anthropic` 结尾）仅提供对话端点 `/v1/messages`，不提供模型列表端点，该探测因此返回 404，CC Switch 据此提示"未找到可用的模型列表端点"。

**该提示不影响 Claude Code 正常使用，可忽略。**Claude Code 通过 `/v1/messages` 发起对话，所用模型由 CC Switch **高级选项**中的模型映射直接指定，不依赖模型列表端点的自动发现。请求地址与 API Key 配置正确时，直接点击**启用**并新开一个 Claude Code 会话即可正常对话。

若确实无法对话，请确认：请求地址以 `/apps/anthropic` 结尾、勿额外添加 `/v1`，并已在[高级选项的模型映射](#ccswitch-add-li2)中填入对应套餐支持的模型。

### CC Switch 中模型映射后无法调用

模型映射配置后在 Claude Code 中无法调用、返回 `AccessDenied`（HTTP 403，错误码 `access_denied`）错误时，检查该模型是否在百炼控制台的**模型广场**中被标记为“即将下线”。标记为“即将下线”的模型仍会显示在列表中，但 API 调用会返回 403 `AccessDenied`。排查步骤如下：

1.  **检查模型是否标记“即将下线”。**在百炼控制台的**模型广场**搜索所用模型，查看其状态标签。
    
2.  **更换为最新可用模型。**将模型映射中的旧版模型（如 `qwen-coder-turbo-0919`）替换为最新版本的可用模型（如 `qwen3-coder-plus`）。
    
3.  **重新配置模型映射并测试。**在 CC Switch 的**高级选项**中更新模型映射，点击**启用**并新开一个 Claude Code 会话验证。
    

百炼控制台的**模型广场**中标记“即将下线”的模型可能随时不可用，请关注模型生命周期，并在模型广场查看模型的可用状态。
