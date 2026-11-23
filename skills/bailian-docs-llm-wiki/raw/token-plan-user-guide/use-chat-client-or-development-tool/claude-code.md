# Claude Code

在 Claude Code 中使用阿里云百炼模型。

## 快速接入

选择你使用的客户端，完成配置。

#### CLI

1.  1
    
    配置模型
    
    #### Token Plan
    
    将 `YOUR_API_KEY` 替换为 Token Plan API Key：
    
    -   Token Plan 个人版：[创建或查看 API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan/personal)
    -   Token Plan 团队版：[分配坐席并获取 API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/uac-admin/organization/members/list)
    
    ```
    export ANTHROPIC_AUTH_TOKEN="YOUR_API_KEY"
    export ANTHROPIC_BASE_URL="https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic"
    export ANTHROPIC_MODEL="auto"
    export ANTHROPIC_DEFAULT_HAIKU_MODEL="qwen3.6-flash"
    export ANTHROPIC_DEFAULT_SONNET_MODEL="qwen3.8-flash"
    export ANTHROPIC_DEFAULT_OPUS_MODEL="qwen4-max-preview"
    export CLAUDE_CODE_SUBAGENT_MODEL="auto"
    export CLAUDE_CODE_MAX_CONTEXT_TOKENS="983616"
    ```
    
    **说明**使用 qwen4-max-preview 时，长输出被截断可设置 `CLAUDE_CODE_MAX_OUTPUT_TOKENS=64000`。
    
    **说明**如需使用 qwen4-max，将 `ANTHROPIC_DEFAULT_OPUS_MODEL` 设为 `qwen4-max`，并将 `CLAUDE_CODE_MAX_CONTEXT_TOKENS` 保持为 `983616`。长输出被截断可设置 `CLAUDE_CODE_MAX_OUTPUT_TOKENS=131072`。qwen4-max 的上下文长度为 1M Token；非思考模式最大输出 131,072 Token，思考与最终回答合计最大 262,144 Token；默认 reasoning\_effort=high，thinking\_budget=131072。
    
    #### 按量计费
    
    将 `YOUR_API_KEY` 替换为[阿里云百炼 API Key](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key?spm=5176.28197581.0.0.307f29a4lC7Vbh)，并将 `{WorkspaceId}` 替换为真实的 [Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。以下示例使用华北2（北京）。
    
    ```
    export ANTHROPIC_AUTH_TOKEN="YOUR_API_KEY"
    export ANTHROPIC_BASE_URL="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic"
    export ANTHROPIC_MODEL="qwen3.7-max"
    export ANTHROPIC_DEFAULT_HAIKU_MODEL="qwen3.6-flash"
    export ANTHROPIC_DEFAULT_SONNET_MODEL="qwen3.7-max"
    export ANTHROPIC_DEFAULT_OPUS_MODEL="qwen3.7-max"
    export CLAUDE_CODE_SUBAGENT_MODEL="qwen3.7-max"
    ```
    
    #### Coding Plan
    
    将 `YOUR_API_KEY` 替换为 [Coding Plan API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/coding-plan)。
    
    ```
    export ANTHROPIC_AUTH_TOKEN="YOUR_API_KEY"
    export ANTHROPIC_BASE_URL="https://coding.dashscope.aliyuncs.com/apps/anthropic"
    export ANTHROPIC_MODEL="qwen3.7-plus"
    export ANTHROPIC_DEFAULT_HAIKU_MODEL="qwen3.7-plus"
    export ANTHROPIC_DEFAULT_SONNET_MODEL="qwen3.7-plus"
    export ANTHROPIC_DEFAULT_OPUS_MODEL="qwen3.7-plus"
    export CLAUDE_CODE_SUBAGENT_MODEL="qwen3.7-plus"
    ```
    
    **说明**以上环境变量只对当前终端生效。需要持久化配置时，使用[通过配置文件接入](#connect_bailian_h)。
    
2.  2
    
    验证
    
    运行以下命令验证：
    
    ```
    claude -p "你好"
    ```
    

#### CC Switch

1.  1
    
    安装 CC Switch
    
    从 [CC Switch](https://github.com/farion1231/cc-switch) 下载并安装。
    
2.  2
    
    添加百炼供应商
    
    在 CC Switch 选中 Claude Code 图标，点击 **+**，按对应 Tab 填入配置并添加。
    
    #### Token Plan
    
    -   供应商名称：百炼-Token Plan
    -   Token Plan 个人版 API Key：[创建或查看](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan/personal)
    -   Token Plan 团队版 API Key：[分配坐席并获取](https://bailian.console.aliyun.com/cn-beijing/subscription/uac-admin/organization/members/list)
    -   请求地址：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`
    
    #### 按量计费
    
    -   供应商名称：百炼-按量计费
    -   API Key：[百炼 API Key](raw/model-api-reference/preparations/get-api-key.md)
    -   请求地址：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic`
    
    #### Coding Plan
    
    -   供应商名称：百炼-Coding Plan
    -   API Key：[控制台获取](https://bailian.console.aliyun.com/cn-beijing/subscription/coding-plan)
    -   请求地址：`https://coding.dashscope.aliyuncs.com/apps/anthropic`
    
3.  3
    
    配置模型映射
    
    展开**高级选项**，设置主模型和 Haiku、Sonnet、Opus 模型。例如：
    
    -   主模型：`qwen3.8-max`
    -   Haiku 默认模型：`qwen3.8-flash`
    -   Sonnet 默认模型：`qwen3.8-flash`
    -   Opus 默认模型：`qwen3.8-max`
    
4.  4
    
    切换到 Claude Desktop 面板
    
    在 CC Switch 左侧切换到 **Claude Desktop** 面板；未显示时，在**设置 → 通用 → 应用可见性**中启用。
    
5.  5
    
    导入供应商
    
    可导入 Claude Code 中已配置的供应商，或点击 **+** 新增。百炼模型 ID 需开启**需要模型映射**，为 Sonnet、Opus、Haiku 填写实际模型。
    
6.  6
    
    开启本地路由
    
    前往**设置 → 路由 → 本地路由**，打开主页面开关；在 Claude Desktop 面板打开本地路由，默认 `127.0.0.1:15721`。
    
7.  7
    
    启用并重启桌面版
    
    在供应商卡片点击**启用**，不要在桌面版中手动填写 API Key。保持 CC Switch 运行，**完全退出并重启**桌面版。
    

#### IDE 插件

1.  1
    
    安装插件
    
    在所用 IDE 的扩展市场安装 Claude Code 插件。
    
2.  2
    
    配置模型
    
    按[通过配置文件接入](#connect_bailian_h)写入 `settings.json`，或先在 CLI 中完成配置。
    
3.  3
    
    打开 Claude Code
    
    重启 IDE，点击 Claude Code 图标，在对话框中输入 `/`，选择 General config，在 Selected Model 中设置模型。
    

#### 桌面版

Claude Code 桌面版通过 CC Switch 本地网关接入百炼。

1.  1
    
    安装 Claude Code 桌面版
    
    从 [Claude 下载页](https://claude.ai/download) 下载并安装。
    
2.  2
    
    配置 CC Switch
    
    按 **CC Switch** Tab 完成供应商和路由配置。
    
3.  3
    
    重启桌面版
    
    保持 CC Switch 运行，完全退出并重启 Claude Code 桌面版。
    

## 通过配置文件接入

除了上述方式，也可以通过配置文件接入。

1.  1
    
    打开或新建配置文件
    
    -   macOS / Linux：`~/.claude/settings.json`
    -   Windows：`C:\Users\<用户名>\.claude\settings.json`
    
2.  2
    
    写入配置
    
    #### Token Plan
    
    将 `YOUR_API_KEY` 替换为 Token Plan API Key：
    
    -   Token Plan 个人版：[创建或查看 API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan/personal)
    -   Token Plan 团队版：[分配坐席并获取 API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/uac-admin/organization/members/list)
    
    ```
    {
        "env": {
            "ANTHROPIC_AUTH_TOKEN": "YOUR_API_KEY",
            "ANTHROPIC_BASE_URL": "https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic",
            "ANTHROPIC_MODEL": "auto",
            "ANTHROPIC_DEFAULT_HAIKU_MODEL": "qwen3.6-flash",
            "ANTHROPIC_DEFAULT_SONNET_MODEL": "qwen3.8-flash",
            "ANTHROPIC_DEFAULT_OPUS_MODEL": "qwen4-max-preview",
            "CLAUDE_CODE_SUBAGENT_MODEL": "auto",
            "CLAUDE_CODE_MAX_CONTEXT_TOKENS": "983616"
        }
    }
    ```
    
    #### 按量计费
    
    将 `YOUR_API_KEY` 替换为[阿里云百炼 API Key](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key?spm=5176.28197581.0.0.307f29a4lC7Vbh)，并将 `{WorkspaceId}` 替换为真实的 [Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)，以华北2（北京）地域为例。
    
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
    
    #### Coding Plan
    
    将 `YOUR_API_KEY` 替换为 [Coding Plan API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/coding-plan)。
    
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
    
3.  3
    
    验证
    
    保存后运行以下命令验证：
    
    ```
    claude -p "你好"
    ```
    

## 配置上下文窗口大小

Claude Code 默认 200K 上下文窗口。模型支持 1M 时，可扩展至 1M（1,000,000 tokens）。

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

修改配置后，需新开终端窗口重新启动 Claude Code 使配置生效。

## 权限模式配置

Claude Code 提供以下权限模式：

-   `default`：每次操作询问用户确认。
-   `acceptEdits`：自动批准文件编辑，其他操作仍询问。
-   `plan`：只读规划模式，不执行修改。
-   `auto`：由分类器判断操作是否允许执行，减少确认提示。在交互式终端和 VS Code 会话中，Claude Code v2.1.283 及以上版本默认使用该模式。
-   `dontAsk`：不询问，需要询问的操作直接拒绝。
-   `bypassPermissions`：绕过所有权限检查。
-   `delegate`：委托模式。

**说明**在 Token Plan 端点使用 `auto` 模式时，分类器检查可能无法返回结果。部分模型下会出现 `Not run · auto mode's check had no usable answer`，导致操作未执行。

遇到该提示时，可将 `permissions.defaultMode` 设为 `default` 或 `acceptEdits`，或调整分类器使用的模型（`ANTHROPIC_DEFAULT_SONNET_MODEL`；Claude Code v2.1.302 及以上版本也可设置 `CLAUDE_CODE_AUTO_MODE_MODEL`）后重新启动会话。

**方式一：命令行参数**

使用 `--permission-mode` 指定本次会话的默认权限模式：

```
claude --permission-mode plan
claude --permission-mode acceptEdits
```
**方式二：交互命令**

在会话中输入 `/permissions` 管理工具的预批准和预拒绝规则，支持 bash、edit 和 MCP 工具。

**方式三：settings.json 配置**

在 `~/.claude/settings.json` 的 `permissions` 字段中配置：

```
{
    "permissions": {
        "allow": ["Bash(git:*)", "Read", "Edit"],
        "deny": ["Bash(rm:*)"],
        "defaultMode": "default"
    }
}
```

## 接入百炼 CLI

1.  1
    
    安装 [百炼 CLI](https://github.com/modelstudioai/cli)
    
    ```
    请帮我全局安装阿里云百炼 CLI 命令行工具：npm install -g bailian-cli
    ```
    
2.  2
    
    配置 API Key
    
    前往[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key?spm=5176.28197581.0.0.307f29a4lC7Vbh)获取 API Key，然后告诉 Claude Code：
    
    ```
    配置我的 API Key 是：sk-xxxxxxxxxxxxx
    ```
    
3.  3
    
    开始使用
    
    直接用自然语言描述需求，例如：
    
    ```
    帮我生成 6 张亚马逊电商主图，产品是白色无线蓝牙耳机。
    帮我生成一段 30 秒的白色无线蓝牙耳机产品演示视频。
    ```
    

## 错误码

配置过程中遇到报错，参考对应套餐的常见问题文档：

-   Token Plan：[Token Plan 常见问题](https://help.aliyun.com/zh/model-studio/token-plan-faq#tpt-h-errors)
-   按量计费：[错误码](raw/model-api-reference/preparations/error-code.md)
-   Coding Plan：[Coding Plan 常见问题](https://help.aliyun.com/zh/model-studio/coding-plan-faq#e07ad90b4f3l0)

## 常见问题

如何按量计费接入节省计划与资源包？

按量计费接入方式不变，使用百炼通用 API Key 和 Base URL。购买节省计划或资源包后自动生效，调用费用按抵扣顺序自动抵扣。详情参见[节省计划与资源包](https://help.aliyun.com/zh/model-studio/savings-plan-and-resource-package#h2-usage)。

如何跳过 Anthropic 官方登录验证？

编辑或新建 `~/.claude.json`（Windows 路径：`C:\Users\<用户名>\.claude.json`），将 `hasCompletedOnboarding` 设为 `true`，跳过 Anthropic 官方登录验证。

```
{
  "hasCompletedOnboarding": true
}
```

调用时返回 401 invalid\_api\_key

此错误表示 API Key 类型与 `ANTHROPIC_BASE_URL` 不匹配。百炼提供三种接入方式，每种方式使用不同的 `base_url` 和专属 API Key，两者必须配套使用：

**接入方式**

**base\_url**

**API Key**

Token Plan

`[https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic](https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic)`

Token Plan API Key

按量计费

`[https://dashscope.aliyuncs.com/apps/anthropic](https://dashscope.aliyuncs.com/apps/anthropic)`

百炼 API Key（`sk-` 开头）

Coding Plan

`[https://coding.dashscope.aliyuncs.com/apps/anthropic](https://coding.dashscope.aliyuncs.com/apps/anthropic)`

Coding Plan API Key

排查步骤如下：

1.  **检查请求地址。**查看 `~/.claude/settings.json` 中 `ANTHROPIC_BASE_URL` 的取值。
2.  **确认 API Key 类型。**对照上表，确认所用 API Key 的类型与 `base_url` 匹配。
3.  **修正配置。**使用百炼按量计费 API Key 时，将 `ANTHROPIC_BASE_URL` 设为 `https://dashscope.aliyuncs.com/apps/anthropic`。

启动 Claude Code 后，界面显示"Unable to connect to Anthropic services. Failed to connect to api.anthropic.com: ERR\_BAD\_REQUEST"

此错误表示 Claude Code 正在尝试连接 Anthropic 官方服务而非阿里云百炼。通常是环境变量未正确配置或未生效。按以下步骤排查：

1.  **检查配置。**启动 Claude Code 后执行 `/status` 命令，确认 `ANTHROPIC_BASE_URL` 和 `ANTHROPIC_AUTH_TOKEN` 是否正确指向百炼地址。输出为空或指向非百炼地址时，检查 `settings.json` 配置是否正确。
2.  **确认 hasCompletedOnboarding。**检查 `~/.claude.json` 文件中 `hasCompletedOnboarding` 是否设置为 `true`。未设置时，Claude Code 启动后会尝试连接 Anthropic 官方服务进行登录验证。
3.  **重新打开终端。**修改配置文件后，需要新开一个终端窗口再执行 `claude`，配置才会生效。
4.  **更新 Claude Code。**若以上步骤均无效，可能是 Claude Code 版本过旧导致。执行 `npm install -g @anthropic-ai/claude-code@latest` 更新到最新版本后重试。

使用旧版接口，切换模型不生效

旧版兼容接口 `https://dashscope.aliyuncs.com/api/v2/apps/claude-code-proxy` 仅支持已下架的模型，指定其他模型不会生效。如需调用可用模型，按本文配置迁移至新版接口。

使用 CC Switch 添加供应商时提示"未找到可用的模型列表端点，请检查 Base URL 或确认供应商是否开放端口"

该提示来自 CC Switch 保存供应商时的连通性检查——它会向配置的请求地址探测模型列表端点（如 `/v1/models`）。百炼的 Anthropic 兼容接入端点（以 `/apps/anthropic` 结尾）仅提供对话端点 `/v1/messages`，不提供模型列表端点，该探测因此返回 404，CC Switch 据此提示"未找到可用的模型列表端点"。

**该提示不影响 Claude Code 正常使用，可忽略。**Claude Code 通过 `/v1/messages` 发起对话，所用模型由 CC Switch **高级选项**中的模型映射直接指定，不依赖模型列表端点的自动发现。请求地址与 API Key 配置正确时，直接点击**启用**并新开一个 Claude Code 会话即可正常对话。

若确实无法对话，请确认：请求地址以 `/apps/anthropic` 结尾、勿额外添加 `/v1`，并已在[高级选项的模型映射](raw/token-plan-user-guide/use-chat-client-or-development-tool/claude-code.md)中填入对应套餐支持的模型。

CC Switch 中模型映射后无法调用

模型映射配置后在 Claude Code 中无法调用、返回 `AccessDenied`（HTTP 403，错误码 `access_denied`）错误时，检查该模型是否在百炼控制台的**模型广场**中被标记为“即将下线”。标记为“即将下线”的模型仍会显示在列表中，但 API 调用会返回 403 `AccessDenied`。排查步骤如下：

1.  **检查模型是否标记“即将下线”。**在百炼控制台的**模型广场**搜索所用模型，查看其状态标签。
2.  **更换为最新可用模型。**将模型映射中的旧版模型（如 `qwen-coder-turbo-0919`）替换为最新版本的可用模型（如 `qwen3.8-max`）。
3.  **重新配置模型映射并测试。**在 CC Switch 的**高级选项**中更新模型映射，点击**启用**并新开一个 Claude Code 会话验证。

百炼控制台的**模型广场**中标记“即将下线”的模型可能随时不可用，请关注模型生命周期，并在模型广场查看模型的可用状态。
