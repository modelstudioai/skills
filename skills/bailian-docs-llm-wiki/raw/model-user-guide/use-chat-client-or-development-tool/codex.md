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

`model`请选择[支持的模型](https://help.aliyun.com/zh/model-studio/token-plan-overview)。将`OPENAI_API_KEY`环境变量设置为 Token Plan 团队版专属 [API Key](https://bailian.console.aliyun.com/cn-beijing?tab=plan#/efm/subscription/uac-admin/organization/members/list)。

#### Responses API（qwen3.7-max、qwen3.7-plus、qwen3.6-plus、qwen3.6-flash）

qwen3.7-max、qwen3.7-plus、qwen3.6-plus 和 qwen3.6-flash 支持 Responses API，可使用最新版 Codex。

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

根据地域设置`base_url`，API Key 须与所选地域对应：

-   华北2（北京）：`https://dashscope.aliyuncs.com/compatible-mode/v1`
    
-   新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`，请将`WorkspaceId`替换为真实的[获取Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#d3eb3cd37b7fu)
    

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

### **第三方工具提示“不支持国内模型”或“检查被拒 / Bad request (400)”怎么办？**

**原因**：部分第三方管理工具（如 CC-Switch）在切换供应商时会发起“健康检查/连接测试”探测请求，该探测请求的格式与 Codex 实际调用的请求格式不同，百炼网关可能因此返回 400 Bad request 并提示“检查被拒”，工具据此显示“不支持国内模型”。此提示仅代表健康检查探测未通过，**并不代表百炼不支持国内模型，也不影响 Codex 的实际使用。**

**说明**：百炼支持通过 Codex 使用 qwen3.7-max、qwen3.7-plus、qwen3.6-plus、qwen3.6-flash、glm-5 等国内模型，配置方式详见上文[配置接入凭证](#cdx-config)。

**解决方案**：建议参照上文配置接入凭证，直接在`~/.codex/config.toml`中完成配置，无需依赖第三方工具的健康检查结果；配置完成后参照[验证配置](#cdx-verify)启动 Codex，若能正常进入对话界面即表示可正常使用国内模型。

### **报错 wire\_api 配置问题怎么办？**

**原因**：Codex 新版本不再支持 `wire_api = "chat"` 配置。根据版本不同，可能出现以下报错：

-   `wire_api = "chat" is no longer supported`
    
-   `unknown configuration field wire_api`
    

**解决方案**：

-   报错 `wire_api = "chat" is no longer supported`：将配置文件中的 `wire_api` 改为 `responses`，并确认 `base_url` 配置正确。详见上文[配置接入凭证](#cdx-config)中对应方案的配置示例。
    
-   报错 `unknown configuration field wire_api`：从配置文件 `~/.codex/config.toml` 的对应 provider 节中删除 `wire_api` 字段。
    

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

### **报错 stream disconnected before completion: stream closed before response.completed 怎么办？**

**原因**：Codex 与服务端的流式连接在响应完成前断开。常见于以下场景：

-   对话线程过长，Codex 触发上下文压缩时请求失败
    
-   网络不稳定，SSE 或 WebSocket 连接中途断开
    
-   服务端过载或触发限流，提前终止连接
    

**解决方案**：

-   开启新的对话线程，避免单个线程积累过多上下文。
    
-   检查网络连接是否稳定，关闭 VPN 或代理后重试。
    
-   等待一段时间后重试，Codex 内置了自动重试机制，多数情况下重试可恢复。
