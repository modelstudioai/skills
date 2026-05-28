# Codex

Codex 是 OpenAI 推出的终端 AI 编程助手。可通过 Token Plan 团队版、Coding Plan 或按量计费接入阿里云百炼。

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

接入需要编辑配置文件`~/.codex/config.toml`并配置环境变量`OPENAI_API_KEY`。根据所选计费方案替换对应值，阿里云百炼提供三种计费方案：

### Token Plan 团队版

`model`请选择[支持的模型](https://help.aliyun.com/zh/model-studio/token-plan-overview)。将`OPENAI_API_KEY`环境变量设置为 Token Plan 团队版专属 [API Key](https://bailian.console.aliyun.com/?tab=plan#/efm/subscription/overview)。

#### Responses API（qwen3.7-max、qwen3.6-plus）

qwen3.7-max 和 qwen3.6-plus 支持 Responses API，可使用最新版 Codex。

```
model_provider = "Model_Studio_Token_Plan"
model = "qwen3.7-max"
[model_providers.Model_Studio_Token_Plan]
name = "Model_Studio_Token_Plan"
base_url = "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
env_key = "OPENAI_API_KEY"
wire_api = "responses"
```

#### Chat/Completions API（其他模型）

其他模型需通过 Chat/Completions API 接入，需安装旧版本 Codex，如 0.80.0：

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

`model`请选择[支持的模型](https://help.aliyun.com/zh/model-studio/coding-plan-overview)。将`OPENAI_API_KEY`环境变量设置为 Coding Plan 专属 [API Key](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/coding_plan)。

#### Chat/Completions API

Coding Plan 仅支持 Chat/Completions API，需安装旧版本 Codex，如 0.80.0：

```
npm install -g @openai/codex@0.80.0
```
```
model_provider = "Model_Studio_Coding_Plan"
model = "qwen3.6-plus"
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

根据地域设置`base_url`，API Key 须与所选地域对应：

-   华北2（北京）：`https://dashscope.aliyuncs.com/compatible-mode/v1`
    
-   新加坡：`https://dashscope-intl.aliyuncs.com/compatible-mode/v1`
    

按量计费支持 Responses API 和 Chat/Completions API 两种接入方式，请根据使用的模型选择：

#### Responses API

适用于支持 [OpenAI Responses API](https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-responses) 的模型（如 qwen3.7-max），可使用最新版 Codex。

```
model_provider = "Model_Studio"
model = "qwen3.7-max"
[model_providers.Model_Studio]
name = "Model_Studio"
base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
env_key = "OPENAI_API_KEY"
wire_api = "responses"
```

#### Chat/Completions API

适用于仅支持 Chat/Completions API 的模型，需安装 Codex 0.80.0：

```
npm install -g @openai/codex@0.80.0
```
```
model_provider = "Model_Studio"
model = "qwen3.6-plus"
[model_providers.Model_Studio]
name = "Model_Studio"
base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
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

## 常见问题

### **报错 wire\_api = chat is no longer supported 怎么办？**

**原因**：Codex 新版本使用 Responses API，不支持`wire_api = "chat"`配置。

**解决方案**：

-   Token Plan 团队版或按量计费：将`wire_api`改为`responses`，并确认`base_url`配置正确。
    
-   Coding Plan：执行以下命令降级到旧版本：
    
    ```
    npm install -g @openai/codex@0.80.0
    ```
    

### 报错 **unexpected status 401 Unauthorized 怎么办？**

**原因**：

-   误用了其他方案的 API Key（Token Plan 团队版、Coding Plan 和按量计费的 API Key 互不相通）
    
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
