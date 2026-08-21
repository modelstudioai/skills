# Codex

Codex 是 OpenAI 推出的终端 AI 编程助手。可通过 Token Plan 个人版、Token Plan 团队版、Coding Plan 或按量计费接入阿里云百炼。

## **安装 Codex**

1.  安装或更新 [Node.js](https://nodejs.org/en/download/)（v18.0 或更高版本）。
    
2.  在终端中执行以下命令安装 Codex。
    
    ```
    npm install -g @openai/codex
    ```
    
    执行以下命令验证安装。
    
    ```
    codex --version
    ```
    

## **配置接入凭证**

接入需要编辑配置文件`~/.codex/config.toml`并配置环境变量`OPENAI_API_KEY`。请根据您的接入方式选择对应配置。

### 配置模型元数据

使用自定义模型（如 qwen3.8-max）时，需要配置模型元数据文件，使 Codex 正确识别模型的上下文窗口、推理深度等参数。

1.  新建文件 `~/.codex/model-catalog.local.json`，写入以下内容：
    
    ```
    {
      "models": [
        {
          "slug": "qwen3.8-max",
          "display_name": "qwen3.8-max",
          "description": "DashScope model: qwen3.8-max",
          "default_reasoning_level": "xhigh",
          "supported_reasoning_levels": [
            {
              "effort": "low",
              "description": "Fast responses with lighter reasoning"
            },
            {
              "effort": "medium",
              "description": "Greater reasoning depth for complex problems"
            },
            {
              "effort": "xhigh",
              "description": "Extra high reasoning depth for complex problems"
            }
          ],
          "context_window": 983616,
          "effective_context_window_percent": 95,
          "supports_parallel_tool_calls": false,
          "supports_image_detail_original": true,
          "input_modalities": ["text", "image"],
          "shell_type": "default",
          "visibility": "list",
          "supported_in_api": true,
          "priority": 1,
          "base_instructions": "",
          "support_verbosity": false,
          "supports_reasoning_summaries": false,
          "experimental_supported_tools": [],
          "truncation_policy": {
            "mode": "bytes",
            "limit": 10000
          }
        }
      ]
    }
    ```
    
2.  在 `~/.codex/config.toml` 中添加以下配置，指向元数据文件：
    
    ```
    model_catalog_json = "~/.codex/model-catalog.local.json"
    ```
    

### Token Plan 个人版

`model`请选择[支持的模型](https://help.aliyun.com/zh/model-studio/token-plan-personal-overview)。将`OPENAI_API_KEY`环境变量设置为 Token Plan 个人版专属 [API Key](https://bailian.console.aliyun.com/cn-beijing?tab=plan#/efm/subscription/overview)。

#### Responses API

若所选模型支持 [OpenAI Responses API](https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-responses)，可使用最新版 Codex。

```
model_provider = "Model_Studio_Token_Plan_Personal"
model = "qwen3.8-max"
[model_providers.Model_Studio_Token_Plan_Personal]
name = "Model_Studio_Token_Plan_Personal"
base_url = "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
env_key = "OPENAI_API_KEY"
wire_api = "responses"
```

#### Chat/Completions API（其他模型）

其他模型需通过 Chat/Completions API 接入，需安装旧版本 Codex，如 0.80.0（新版本 Codex 已不再支持 wire\_api = "chat" 配置，升级后如遇报错请参见下文 FAQ）：

```
npm install -g @openai/codex@0.80.0
```
```
model_provider = "Model_Studio_Token_Plan_Personal"
model = "glm-5"
[model_providers.Model_Studio_Token_Plan_Personal]
name = "Model_Studio_Token_Plan_Personal"
base_url = "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
env_key = "OPENAI_API_KEY"
wire_api = "chat"
```

#### 配置环境变量

将`OPENAI_API_KEY`环境变量设置为 Token Plan 个人版专属 API Key。

## macOS

1.  在终端中执行以下命令，查看默认 Shell 类型。
    
    ```
    echo $SHELL
    ```
    
2.  根据 Shell 类型设置环境变量：
    
    ## Zsh
    
    ```
    # 将 YOUR_API_KEY 替换为 Token Plan 个人版 API Key
    echo 'export OPENAI_API_KEY="YOUR_API_KEY"' >> ~/.zshrc
    ```
    
    ## Bash
    
    ```
    # 将 YOUR_API_KEY 替换为 Token Plan 个人版 API Key
    echo 'export OPENAI_API_KEY="YOUR_API_KEY"' >> ~/.bash_profile
    ```
    
3.  执行以下命令使环境变量生效。
    
    ## Zsh
    
    ```
    source ~/.zshrc
    ```
    
    ## Bash
    
    ```
    source ~/.bash_profile
    ```
    

## Windows

## CMD

1.  在 CMD 中运行以下命令，设置环境变量。
    
    ```
    REM 将 YOUR_API_KEY 替换为 Token Plan 个人版 API Key
    setx OPENAI_API_KEY "YOUR_API_KEY"
    ```
    
2.  打开一个新的 CMD 窗口，运行以下命令检查环境变量是否生效。
    
    ```
    echo %OPENAI_API_KEY%
    ```
    

## PowerShell

1.  在 PowerShell 中运行以下命令，设置环境变量。
    
    ```
    # 将 YOUR_API_KEY 替换为 Token Plan 个人版 API Key
    [Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "YOUR_API_KEY", [EnvironmentVariableTarget]::User)
    ```
    
2.  打开一个新的 PowerShell 窗口，运行以下命令检查环境变量是否生效。
    
    ```
    echo $env:OPENAI_API_KEY
    ```
    

### Token Plan 团队版

`model`请选择[支持的模型](https://help.aliyun.com/zh/model-studio/token-plan-overview)。将`OPENAI_API_KEY`环境变量设置为 Token Plan 团队版专属 [API Key](https://bailian.console.aliyun.com/cn-beijing?tab=plan#/efm/subscription/uac-admin/organization/members/list)。

#### Responses API

若所选模型支持 [OpenAI Responses API](https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-responses)，可使用最新版 Codex。

```
model_provider = "Model_Studio_Token_Plan"
model = "qwen3.8-max"
[model_providers.Model_Studio_Token_Plan]
name = "Model_Studio_Token_Plan"
base_url = "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
env_key = "OPENAI_API_KEY"
wire_api = "responses"
```

#### Chat/Completions API（其他模型）

其他模型需通过 Chat/Completions API 接入，需安装旧版本 Codex，如 0.80.0（新版本 Codex 已不再支持 wire\_api = "chat" 配置，升级后如遇报错请参见下文 FAQ）：

```
npm install -g @openai/codex@0.80.0
```
```
model_provider = "Model_Studio_Token_Plan"
model = "glm-5"
[model_providers.Model_Studio_Token_Plan]
name = "Model_Studio_Token_Plan"
base_url = "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
env_key = "OPENAI_API_KEY"
wire_api = "chat"
```

#### 配置环境变量

将`OPENAI_API_KEY`环境变量设置为 Token Plan 团队版专属 API Key。

## macOS

1.  在终端中执行以下命令，查看默认 Shell 类型。
    
    ```
    echo $SHELL
    ```
    
2.  根据 Shell 类型设置环境变量：
    
    ## Zsh
    
    ```
    # 将 YOUR_API_KEY 替换为 Token Plan 团队版 API Key
    echo 'export OPENAI_API_KEY="YOUR_API_KEY"' >> ~/.zshrc
    ```
    
    ## Bash
    
    ```
    # 将 YOUR_API_KEY 替换为 Token Plan 团队版 API Key
    echo 'export OPENAI_API_KEY="YOUR_API_KEY"' >> ~/.bash_profile
    ```
    
3.  执行以下命令使环境变量生效。
    
    ## Zsh
    
    ```
    source ~/.zshrc
    ```
    
    ## Bash
    
    ```
    source ~/.bash_profile
    ```
    

## Windows

## CMD

1.  在 CMD 中运行以下命令，设置环境变量。
    
    ```
    REM 将 YOUR_API_KEY 替换为 Token Plan 团队版 API Key
    setx OPENAI_API_KEY "YOUR_API_KEY"
    ```
    
2.  打开一个新的 CMD 窗口，运行以下命令检查环境变量是否生效。
    
    ```
    echo %OPENAI_API_KEY%
    ```
    

## PowerShell

1.  在 PowerShell 中运行以下命令，设置环境变量。
    
    ```
    # 将 YOUR_API_KEY 替换为 Token Plan 团队版 API Key
    [Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "YOUR_API_KEY", [EnvironmentVariableTarget]::User)
    ```
    
2.  打开一个新的 PowerShell 窗口，运行以下命令检查环境变量是否生效。
    
    ```
    echo $env:OPENAI_API_KEY
    ```
    

### Coding Plan

`model`请选择[支持的模型](https://help.aliyun.com/zh/model-studio/coding-plan)。将`OPENAI_API_KEY`环境变量设置为 Coding Plan 专属 [API Key](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/coding_plan)。

#### Chat/Completions API

Coding Plan 仅支持 Chat/Completions API，需安装旧版本 Codex，如 0.80.0（新版本 Codex 已不再支持 wire\_api = "chat" 配置，升级后如遇报错请参见下文 FAQ）：

```
npm install -g @openai/codex@0.80.0
```
```
model_provider = "Model_Studio_Coding_Plan"
model = "qwen3.7-plus"
[model_providers.Model_Studio_Coding_Plan]
name = "Model_Studio_Coding_Plan"
base_url = "https://coding.dashscope.aliyuncs.com/v1"
env_key = "OPENAI_API_KEY"
wire_api = "chat"
```

#### 配置环境变量

将`OPENAI_API_KEY`环境变量设置为 Coding Plan 专属 API Key。

## macOS

1.  在终端中执行以下命令，查看默认 Shell 类型。
    
    ```
    echo $SHELL
    ```
    
2.  根据 Shell 类型设置环境变量：
    
    ## Zsh
    
    ```
    # 将 YOUR_API_KEY 替换为 Coding Plan API Key
    echo 'export OPENAI_API_KEY="YOUR_API_KEY"' >> ~/.zshrc
    ```
    
    ## Bash
    
    ```
    # 将 YOUR_API_KEY 替换为 Coding Plan API Key
    echo 'export OPENAI_API_KEY="YOUR_API_KEY"' >> ~/.bash_profile
    ```
    
3.  执行以下命令使环境变量生效。
    
    ## Zsh
    
    ```
    source ~/.zshrc
    ```
    
    ## Bash
    
    ```
    source ~/.bash_profile
    ```
    

## Windows

## CMD

1.  在 CMD 中运行以下命令，设置环境变量。
    
    ```
    REM 将 YOUR_API_KEY 替换为 Coding Plan API Key
    setx OPENAI_API_KEY "YOUR_API_KEY"
    ```
    
2.  打开一个新的 CMD 窗口，运行以下命令检查环境变量是否生效。
    
    ```
    echo %OPENAI_API_KEY%
    ```
    

## PowerShell

1.  在 PowerShell 中运行以下命令，设置环境变量。
    
    ```
    # 将 YOUR_API_KEY 替换为 Coding Plan API Key
    [Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "YOUR_API_KEY", [EnvironmentVariableTarget]::User)
    ```
    
2.  打开一个新的 PowerShell 窗口，运行以下命令检查环境变量是否生效。
    
    ```
    echo $env:OPENAI_API_KEY
    ```
    

### 按量计费

将`OPENAI_API_KEY`环境变量设置为[百炼 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。可用模型参见[支持的模型](https://help.aliyun.com/zh/model-studio/compatibility-of-openai-with-dashscope#7f9c78ae99pwz)。

根据地域设置`base_url`，API Key 须与所选地域对应，请将 URL 中的 `{WorkspaceId}` 替换为真实的[获取Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#d3eb3cd37b7fu)：

-   华北2（北京）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
    
-   新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`
    

按量计费支持 Responses API 和 Chat/Completions API 两种接入方式，请根据使用的模型选择：

#### Responses API

适用于支持 [OpenAI Responses API](https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-responses) 的模型（如 qwen3.7-max），可使用最新版 Codex。

```
model_provider = "Model_Studio"
model = "qwen3.7-max"
[model_providers.Model_Studio]
name = "Model_Studio"
base_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
env_key = "OPENAI_API_KEY"
wire_api = "responses"
```

#### Chat/Completions API

适用于仅支持 Chat/Completions API 的模型，需安装 Codex 0.80.0（新版本 Codex 已不再支持 wire\_api = "chat" 配置，升级后如遇报错请参见下文 FAQ）：

```
npm install -g @openai/codex@0.80.0
```
```
model_provider = "Model_Studio"
model = "qwen3.6-plus"
[model_providers.Model_Studio]
name = "Model_Studio"
base_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
env_key = "OPENAI_API_KEY"
wire_api = "chat"
```

#### 配置环境变量

将`OPENAI_API_KEY`环境变量设置为[百炼 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。

## macOS

1.  在终端中执行以下命令，查看默认 Shell 类型。
    
    ```
    echo $SHELL
    ```
    
2.  根据 Shell 类型设置环境变量：
    
    ## Zsh
    
    ```
    # 将 YOUR_API_KEY 替换为百炼 API Key
    echo 'export OPENAI_API_KEY="YOUR_API_KEY"' >> ~/.zshrc
    ```
    
    ## Bash
    
    ```
    # 将 YOUR_API_KEY 替换为百炼 API Key
    echo 'export OPENAI_API_KEY="YOUR_API_KEY"' >> ~/.bash_profile
    ```
    
3.  执行以下命令使环境变量生效。
    
    ## Zsh
    
    ```
    source ~/.zshrc
    ```
    
    ## Bash
    
    ```
    source ~/.bash_profile
    ```
    

## Windows

## CMD

1.  在 CMD 中运行以下命令，设置环境变量。
    
    ```
    REM 将 YOUR_API_KEY 替换为百炼 API Key
    setx OPENAI_API_KEY "YOUR_API_KEY"
    ```
    
2.  打开一个新的 CMD 窗口，运行以下命令检查环境变量是否生效。
    
    ```
    echo %OPENAI_API_KEY%
    ```
    

## PowerShell

1.  在 PowerShell 中运行以下命令，设置环境变量。
    
    ```
    # 将 YOUR_API_KEY 替换为百炼 API Key
    [Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "YOUR_API_KEY", [EnvironmentVariableTarget]::User)
    ```
    
2.  打开一个新的 PowerShell 窗口，运行以下命令检查环境变量是否生效。
    
    ```
    echo $env:OPENAI_API_KEY
    ```
    

## **验证配置**

配置完成后，新建终端窗口，执行以下命令启动 Codex：

```
codex
```

如果正常进入对话界面，说明配置成功。

## **使用 CC Switch**

[CC Switch](https://github.com/farion1231/cc-switch) 是社区开源的桌面 GUI，支持在多个 API Key 或计费套餐之间一键切换，无需手动修改 `~/.codex/config.toml`。

### 安装

-   macOS：执行 `brew tap farion1231/ccswitch && brew install --cask cc-switch`，或从 [Releases](https://github.com/farion1231/cc-switch/releases) 下载 `.dmg`。
    
-   Windows：从 [Releases](https://github.com/farion1231/cc-switch/releases) 下载 `.msi` 安装包或便携版 `.zip`。
    
-   Linux：Arch 发行版执行 `paru -S cc-switch-bin`；其他发行版从 [Releases](https://github.com/farion1231/cc-switch/releases) 下载 `.deb` / `.rpm` / `.AppImage`。
    

### 添加供应商

1.  在 CC Switch 主界面顶部图标栏选中 Codex 图标，点击右上角 **+** 进入**添加新供应商**，按下表填入配置后点击**添加**。
    
    **计费方案**
    
    **配置信息**
    
    Token Plan 个人版
    
    供应商名称：百炼-Token Plan 个人版
    
    API Key：[控制台获取](https://bailian.console.aliyun.com/cn-beijing?tab=plan#/efm/subscription/overview)
    
    请求地址：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
    
    Token Plan 团队版
    
    供应商名称：百炼-Token Plan 团队版
    
    API Key：[控制台获取](https://bailian.console.aliyun.com/cn-beijing?tab=plan#/efm/subscription/uac-admin/organization/members/list)
    
    请求地址：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
    
    Coding Plan
    
    供应商名称：百炼-Coding Plan
    
    API Key：[控制台获取](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/coding_plan)
    
    请求地址：`https://coding.dashscope.aliyuncs.com/v1`
    
    按量计费
    
    供应商名称：百炼-按量计费
    
    API Key：[百炼 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)
    
    请求地址：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
    
2.  展开**高级选项**填写模型名称，从对应套餐[支持的模型](https://help.aliyun.com/zh/model-studio/token-plan-overview)中选择，例如 `qwen3.7-max`（Coding Plan 不支持）。
    
3.  回到主界面，点击该供应商右侧**启用**按钮，然后重新打开终端窗口执行 `codex` 使配置生效。
    

## 常见问题

### **第三方工具提示“不支持国内模型”或“检查被拒 / Bad request (400)”怎么办？**

**原因**：部分第三方管理工具（如 CC-Switch）在切换供应商时会发起“健康检查/连接测试”探测请求，该探测请求的格式与 Codex 实际调用的请求格式不同，百炼网关可能因此返回 400 Bad request 并提示“检查被拒”，工具据此显示“不支持国内模型”。此提示仅代表健康检查探测未通过，**并不代表百炼不支持中国内地模型，也不影响 Codex 的实际使用。**

**说明**：百炼支持通过 Codex 使用中国内地模型，配置方式详见上文[配置接入凭证](#cdx-config)。

**解决方案**：建议参照上文配置接入凭证，直接在`~/.codex/config.toml`中完成配置，无需依赖第三方工具的健康检查结果；配置完成后参照[验证配置](#cdx-verify)启动 Codex，若能正常进入对话界面即表示可正常使用中国内地模型。

### **报错 wire\_api 配置问题怎么办？**

**原因**：Codex 新版本不再支持 `wire_api = "chat"` 配置。根据版本不同，可能出现以下报错：

-   `wire_api = "chat" is no longer supported`
    
-   `unknown configuration field wire_api`
    

**解决方案**：

-   报错 `wire_api = "chat" is no longer supported`：将配置文件中的 `wire_api` 改为 `responses`，并确认 `base_url` 配置正确。详见上文[配置接入凭证](#cdx-config)中对应方案的配置示例。
    
-   报错 `unknown configuration field wire_api`：从配置文件 `~/.codex/config.toml` 的对应 provider 节中删除 `wire_api` 字段。
    

### 报错 **unexpected status 401 Unauthorized 怎么办？**

**原因**：

-   误用了其他方案的 API Key（Token Plan 个人版、Token Plan 团队版、Coding Plan 和按量计费的 API Key 互不相通）
    
-   订阅过期
    
-   API Key 复制不完整、有空格或拼写错误
    

**解决方案**：

-   确认使用的是所选方案对应的专属 API Key。
    
-   前往对应方案的管理页面确认订阅是否过期。
    
-   重新复制 API Key，确保完整且无空格。
    
-   如以上均正常仍报错，可在对应管理页面重置 API Key，重置后请使用新 API Key 进行配置。
    

### 报错 unexpected status 404 Not Found 怎么办？

**原因**：配置文件中的`base_url`或`wire_api`填写错误。

**解决方案**：确认`base_url`和`wire_api`与所选方案的配置一致。参见上文[配置接入凭证](#cdx-config)中对应方案的配置示例。

### **报错 stream disconnected before completion: stream closed before response.completed 怎么办？**

**原因**：Codex 与服务端的流式连接在响应完成前断开。常见于以下场景：

-   对话线程过长，Codex 触发上下文压缩时请求失败
    
-   网络不稳定，SSE 或 WebSocket 连接中途断开
    
-   服务端过载或触发限流，提前终止连接
    

**解决方案**：

-   开启新的对话线程，避免单个线程积累过多上下文。
    
-   检查网络连接是否稳定，关闭 VPN 或代理后重试。
    
-   等待一段时间后重试，Codex 内置了自动重试机制，多数情况下重试可恢复。
    

### **报错 429 请求超频或额度用尽怎么办？**

**原因**：429 错误有以下两种情形：

-   **请求超频**（`429 Requests rate limit exceeded`）：短时间内请求过于密集。
    
-   **限额用尽**（`429 Allocated quota exceeded` 或 `Your token-plan 1-week quota has been exhausted`）：Token Plan 个人版的 7 天限额触顶。
    

**解决方案**：

-   请求超频：等待一分钟后重试，降低请求频率。
    
-   限额用尽：等待 7 天窗口周期结束后额度自动重置；或购买用量包（用量包额度不受窗口限额约束）；或升级套餐。注意：报错信息中的重置时间（如 `The quota will reset at HH:MM:SS UTC`）以协调世界时（UTC）为准，换算为北京时间（CST）需加 8 小时。
