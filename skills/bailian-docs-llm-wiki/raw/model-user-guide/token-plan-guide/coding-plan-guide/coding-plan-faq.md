# 常见问题

## **使用阿里云 AI 助理**

推荐使用[阿里云 AI 助理](https://www.aliyun.com/ai-assistant/)，其知识库整合了阿里云官方帮助文档。

示例问题：

```
使用coding plan时，报错model 'xxx' is not supported是什么原因
```

阿里云 AI 助理会分析原因并给出解决方案：

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4077616771/p1067334.png)

## **接入与配置相关问题**

### **常见报错及解决方案**

**报错信息**

**可能原因**

**解决方案**

**400 InvalidParameter: Range of input length should be \[1, xxx\]**

输入长度超出了允许范围

1.  可通过新建会话解决报错。
    
2.  通过精简输入、切换更长上下文的模型等方式可以避免输入超限问题，详见[各模型的上下文长度是多少？超出上下文长度如何处理？](#fb46a77831l0o)
    
3.  若使用OpenCode，请配置`limit`来限制上下文长度，详见[OpenCode](https://help.aliyun.com/zh/model-studio/opencode)。
    

**401 invalid access token or token expired**

1.  误用了百炼通用 API Key（sk-xxx）
    
2.  Coding Plan 订阅过期
    
3.  API Key 复制不完整、有空格或拼写错误
    

1.  [使用套餐专属 API Key](https://help.aliyun.com/zh/model-studio/coding-plan-quickstart#2782cf93b1w8h)
    
2.  前往[Coding Plan 页面](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/coding_plan)确认订阅是否过期
    
3.  前往[Coding Plan 页面](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/coding_plan)重新复制 API Key，确保完整且无空格
    
4.  如以上均正常仍报错，可在 [Coding Plan 页面](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/coding_plan)重置 API Key，重置后请使用新 API Key 进行配置
    

**model 'xxx' is not supported**

1.  使用了 Coding Plan 不支持的模型
    
2.  模型名称拼写错误、大小写错误、包含空格
    

模型名称必须为[Coding Plan](https://help.aliyun.com/zh/model-studio/coding-plan#dc0d98da6ev4j)支持的模型 ID，区分大小写，前后无空格。

**403 invalid api-key**

误用了百炼通用 Base URL

Anthropic 兼容端点：`https://coding.dashscope.aliyuncs.com/apps/anthropic`

OpenAI 兼容端点：`https://coding.dashscope.aliyuncs.com/v1`

**404 status code (no body)**

Base URL 路径错误。例如：在 Claude Code 中错误地将 Base URL 配置为`https://coding.dashscope.aliyuncs.com/v1`，正确的配置应该是`https://coding.dashscope.aliyuncs.com/apps/anthropic`。

Anthropic 兼容端点：`https://coding.dashscope.aliyuncs.com/apps/anthropic`

OpenAI 兼容端点：`https://coding.dashscope.aliyuncs.com/v1`

**Connection error**

Base URL 拼写错误或网络问题

检查 Base URL 域名拼写及网络连接。

**hour allocated quota exceeded**

每 5 小时请求额度已用完

等待 5 小时后额度自动恢复。

**week allocated quota exceeded**

每周请求额度已用完

等待至每周一 00:00:00（UTC+8）额度重置。

**month allocated quota exceeded**

每月请求额度已用完

等待至订阅月对应日 00:00:00（UTC+8）额度重置。

**concurrency allocated quota exceeded**

当前并发请求数超出平台动态分配的上限

等待片刻后重试即可。平台会根据整体资源负载动态调整并发上限，高峰时段可能触发此限制。

### 海外用户如何使用 Coding Plan？

阿里云中国站的百炼 Coding Plan 不限制使用地域，海外用户可以正常使用。如果您在使用过程中遇到网络延迟或账号问题，可以选择使用[国际站 Coding Plan](https://www.alibabacloud.com/help/zh/model-studio/coding-plan-quickstart)。

### **Claude Code 提示 “Claude Code has switched from npm to native installer”怎么办？**

不影响 Claude Code 的正常使用。你可以选择在终端执行`claude install` 将 Claude Code 迁移到官方原生安装版本，并参照终端中返回的命令完成配置迁移。

### **Claude Code 报错 “Unable to connect to Anthropic services. Failed to connect to api.anthropic.com: ERR\_BAD\_REQUEST”怎么办**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7935123771/p1049322.png)

**原因**：Claude Code 首次启动时会尝试连接 api.anthropic.com 完成初始化认证，但 Claude Code 在部分国家和地区不可用，导致连接失败。

**解决方案**：

1.  在 `~/.claude.json`中添加 `"hasCompletedOnboarding": true`作为顶层字段。
    
    > 建议使用 [Qwen Code](https://help.aliyun.com/zh/model-studio/qwen-code) 自动添加。在终端运行`qwen`启动后，在对话框中发送以下内容：`请在 ~/.claude.json 文件中添加 "hasCompletedOnboarding": true 作为顶层字段，不要覆盖已有内容`。
    
    ```
    {
      "hasCompletedOnboarding": true
    }
    ```
    
2.  保存后重新启动 Claude Code。
    
    ```
    claude
    ```
    

### **OpenCode 报错 "Request Entity Too Large" 怎么办？**

该报错表示请求内容（如代码上下文、对话历史）过大，超出最大输入限制。请按以下方式处理：

1.  执行 `/new` 新建对话，或执行 `/compact` 压缩上下文。更多缓解上下文超限的方法，请参见[各模型的上下文长度是多少？超出上下文长度如何处理？](#fb46a77831l0o)。
    
2.  若以上方法无法解决，请将 OpenCode 更新至 1.2.16 或以上版本，该版本修复了相关问题。
    

### **OpenCode 报错 "The thinking\_budget parameter must be a positive integer and not greater than 38912" 怎么办？**

**原因**： 配置文件`opencode.json`中 `budgetTokens` 的值超过了当前模型支持的最大 `thinking_budget`。不同模型的上限不同，请参照下表调整配置。

**模型名称**

**最大思维链长度**

qwen3.6-plus

81,920

qwen3.5-plus

81,920

qwen3-max-2026-01-23

81,920

kimi-k2.5

81,920

glm-5

32,768

glm-4.7

32,768

MiniMax-M2.5

默认启用，无需配置 budgetTokens

qwen3-coder-next

不支持思考模式

qwen3-coder-plus

不支持思考模式

**解决方案**：打开 OpenCode 配置文件 `opencode.json`，将对应模型的 `options.thinking.budgetTokens` 值调整为不超过该模型的上限值。对于不支持思考模式的模型（qwen3-coder-next、qwen3-coder-plus），需要移除 `options.thinking` 配置项。详情请参见[OpenCode](https://help.aliyun.com/zh/model-studio/opencode)。

### **OpenCode报错“InternalError.Algo.InvalidParameter: Range of max\_tokens should be \[1, xxxx\]”怎么办？**

**原因**：配置文件`opencode.json`中 `limit.output` 的值超过了当前模型支持的最大输出Token数（`max_tokens`）。

**解决方案**：请根据[OpenCode](https://help.aliyun.com/zh/model-studio/opencode)修改配置文件 `opencode.json`，调整对应模型的`limit`值。

### **Coding Plan 模型支持开启思考模式吗？**

Coding Plan 支持深度思考的模型多为默认支持思考模式，常见工具开启方式为：

> 使用的模型需支持思考模式。

## Claude Code

**开启思考模式**：输入`/config`，移动到`Thinking mode`，通过`Enter`切换为`true`开启思考模式。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7325012771/p1055133.png)

**查看思考过程**：使用快捷键 `Ctrl + O` 可查看思考过程。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9530922771/p1055595.png)

## OpenCode

参见[OpenCode](https://help.aliyun.com/zh/model-studio/opencode)，配置options参数为：

```
{
  "thinking": {
    "type": "enabled",
    "budgetTokens": 1024
  }
}
```

> budgetTokens 为最大思考Token数，可根据需求调整。

## Qwen Code

打开`~/.qwen/settings.json`，在`modelProviders`属性中设置`enable_thinking`参数为`true`开启思考模式：

```
{
  "ide": {
    "hasSeenNudge": true
  },
  "env": {
    "BAILIAN_CODING_PLAN_API_KEY": "sk-sp-xxx"
  },
  "modelProviders": {
    "openai": [
      {
        "id": "qwen3.6-plus",
        "name": "[Bailian Coding Plan] qwen3.6-plus",
        "baseUrl": "https://coding.dashscope.aliyuncs.com/v1",
        "envKey": "BAILIAN_CODING_PLAN_API_KEY",
        "generationConfig": {
          "extra_body": {
            "enable_thinking": true
          }
        }
      },
      ...
    ]
  },
  "security": {
    "auth": {
      "selectedType": "openai"
    }
  },
  "codingPlan": {
    "region": "china",
    "version": "xxx"
  },
  "model": {
    "name": "qwen3.6-plus"
  },
  "$version": 3
}
```

## OpenClaw

OpenClaw 开启思考模式的步骤如下：

1.  **查看 OpenClaw 版本**
    
    在终端执行 `openclaw tui` 进入TUI 界面，在对话框输入`openclaw --version`查看版本，确认 OpenClaw 是否为`v2026.03.02`或更高版本，低版本的 OpenClaw 可能无法开启思考模式。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4890023771/p1058523.png)
    
2.  **选择思考级别**
    
    继续在 OpenClaw 的 TUI 界面，输入`/think high`命令选择[思考级别](https://docs.openclaw.ai/tools/thinking)（本示例选择`high`作为当前会话的思考级别）。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8479172771/p1057350.png)
    
3.  **修改配置文件**
    
    1.  **设置**`compat`**参数**
        
        参见[OpenClaw](https://help.aliyun.com/zh/model-studio/openclaw#0c6a73ae73mqr)打开配置文件，在支持思考模式的模型配置中添加`compat`参数：
        
        ```
        "compat": {
            "thinkingFormat": "qwen"
          }
        ```
        
    2.  **设置**`reasoning`**参数**
        
        在同一模型配置中，将`reasoning`参数设置为`true`：
        
        ```
        {
          "id": "qwen3-max-2026-01-23",
          "name": "qwen3-max-2026-01-23",
          "reasoning": true, 
          "compat": {
            "thinkingFormat": "qwen"
          },
          "input": [
            "text"
          ],
          "cost": {
            "input": 0,
            "output": 0,
            "cacheRead": 0,
            "cacheWrite": 0
          },
          "contextWindow": 262144,
          "maxTokens": 65536
        }
        ```
        
4.  **重启 OpenClaw Gateway**
    
    保存配置文件后，在终端执行以下命令重启 OpenClaw Gateway，来使配置生效。
    
    ```
    openclaw gateway restart
    ```
    

### 为什么 OpenClaw 中出现未配置模型的调用记录？

**原因**：`openclaw.json`中没有配置`agents.defaults.models`来限制可用模型范围。

**解决方案**：请在`~/.openclaw/openclaw.json`的`agents.defaults.models`中显式声明允许使用的模型列表，限制 OpenClaw 仅调用已配置的模型，详情请参考[OpenClaw](https://help.aliyun.com/zh/model-studio/openclaw#0c6a73ae73mqr)。

### OpenClaw 显示已连接但聊天无响应/一直转圈怎么办？

可能的原因如下：

1.  本地代理（VPN/HTTP Proxy）拦截或无法正确转发请求到 `coding.dashscope.aliyuncs.com`。
    
2.  OpenClaw 缓存文件`~/.openclaw/agents/main/agent/models.json`中的 Base URL 指向了错误地址，请求被发送到了无法响应的端点。
    

**解决方案**：

1.  尝试关闭本地代理，或确保代理能正常访问`coding.dashscope.aliyuncs.com`。
    
2.  删除`~/.openclaw/agents/main/agent/models.json`缓存文件并重启 OpenClaw，重启后缓存文件会根据`~/.openclaw/openclaw.json`中的配置自动重建。
    

### OpenClaw中报错 "Agent failed before reply: OAuth token refresh failed" 怎么办？

此报错表明当前接入的是第三方 OAuth 服务，而非 Coding Plan。

**解决方案**：

1.  在 OpenClaw 中配置 Coding Plan，详情请参考[OpenClaw](https://help.aliyun.com/zh/model-studio/openclaw#0c6a73ae73mqr)。
    
2.  清理旧的 OAuth 凭证和模型缓存并重启 OpenClaw。
    
    > 删除旧的 OAuth 凭证前，建议先备份相关文件，以便恢复时回退。
    
    ```
    rm ~/.openclaw/agents/main/agent/auth.json
      rm ~/.openclaw/agents/main/agent/models.json
      openclaw gateway restart
    ```
    

### OpenClaw报错“Agent failed before reply: Unknown model”怎么办？

该报错表示 OpenClaw 在配置文件中找不到指定的模型。请按以下顺序逐一排查：

1.  `models.providers` 键名或模型前缀配置错误
    
    当使用 Coding Plan套餐时，`models.providers` 下的键名必须包含 `bailian` 键（可与其他 provider 共存）。并且，`agents.defaults.model.primary` 必须加 `bailian/`前缀。正确的结构如下所示：
    
    ```
    //配置文件：~/.openclaw/openclaw.json
    {
      "models": { "providers": { "bailian": {...} } },
      "agents": { "defaults": { "model": { "primary": "bailian/qwen3.6-plus" } } }
    }
    ```
    
2.  旧 Provider 配置残留导致路由冲突
    
    若之前使用过 qwen-portal 等其他提供商，旧 provider 残留会导致模型路由混乱。请清理无关 provider，确保 `primary` 字段指向的模型已在 `models.providers.bailian.models` 列表中正确定义。配置信息请参见[OpenClaw](https://help.aliyun.com/zh/model-studio/openclaw)。
    

### qwen-portal/coder-model是什么模型？

`qwen-portal/coder-model` 是 Qwen Chat 网页版提供的免费模型，并不属于百炼平台。如果您在百炼平台或 Coding Plan 中尝试使用该模型，将会遇到模型不存在的报错。请使用百炼平台支持的模型。

### OpenClaw报错"No API key found for provider "xxxxx"."怎么办？

该报错表示 OpenClaw 无法找到报错信息中所指 provider（xxxx）对应的 API Key。请按以下步骤逐一排查：

1.  `models.providers` 中缺少对应 provider 配置
    
    打开配置文件 `~/.openclaw/openclaw.json`，确认`models.providers` 下存在与报错中 provider 名称一致的键。
    
    1.  若接入 Coding Plan，配置中必须包含 `bailian` 键（可与其他 provider 共存）。
        
    2.  若不存在，请补充对应的 provider 配置。
        
2.  provider对应的API Key 配置错误
    
    -   确保已填写有效的 API Key（非空、无多余空格）。
        
    -   若使用 Coding Plan，请确保使用的是专属 Key（`sk-sp-xxx`）。
        
    -   若 Web UI 中显示的是 “\_\_OPENCLAW\_REDACTED\_\_”，表示API Key 已保存，无需重填；若显示为空或YOUR\_API\_KEY，则需重新填写。
        
3.  本地凭证缓存未更新，导致配置未生效
    
    > 删除旧的凭证前，建议先备份相关文件，以便出错时回退。
    
    ```
    # 删除旧凭证和模型缓存
    rm ~/.openclaw/agents/main/agent/auth-profiles.json
    rm ~/.openclaw/agents/main/agent/models.json
    
    # 重启 Gateway 使配置重新生效
    openclaw gateway restart
    ```
    

### OpenClaw报错“API rate limit reached”怎么办？

请按以下顺序排查：

1.  OpenClaw 配置错误
    
    若 Base URL 或模型提供商配置有误，导致请求未进入 Coding Plan 专属通道，而是被路由到了 通用的API 调用，从而触发限流。
    
    -   若使用 Coding Plan 套餐，请核对[OpenClaw配置文件](https://help.aliyun.com/zh/model-studio/openclaw#0c6a73ae73mqr)中的 `models`、`agents`、`gateway`（含嵌套字段），确保与文档配置一致。例如：模型服务提供商的结构为`{ "models": { "providers": { "**bailian**": {...} } } }` 。
        
    -   若当前未使用 Coding Plan 套餐，建议切换至 Coding Plan 以获取专属额度。
        
2.  超出套餐限额：在[Coding Plan页面](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/coding_plan)查看套餐用量情况。
    
3.  尝试重置 API Key**：**若完成上述排查后问题仍未解决，请前往[Coding Plan页面](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/coding_plan)重置 API Key。
    

### **OpenClaw 启动时报错 "Failed to discover Alibaba Cloud models" 怎么办？**

OpenClaw 启动时出现以下报错信息：

-   `Failed to discover Alibaba Cloud models: TimeoutError: The operation was aborted due to timeout`
    
-   `Failed to discover Alibaba Cloud models: 404 Not Found`
    

**原因**：OpenClaw试图查询百炼Coding Plan的模型列表，但模型列表不支持通过接口查询。

**解决方案**：

1.  该信息不影响 OpenClaw 的正常使用，可忽略。
    
2.  若 OpenClaw 无法正常运行，请检查其他错误信息。
    
3.  如需屏蔽此提示，请将 `~/.openclaw/agents/main/agent/auth-profiles.json` 文件中的`alibaba-cloud:default profile`删除，例如，当前为
    
    ```
    "profiles": {                                                                                                                                                                                                   
         "alibaba-cloud:default": {                                                                                                                                                                                    
           "type": "api_key",                                                                                                                                                                                          
           "provider": "alibaba-cloud",                                                                                                                                                                                
           "key": "sk-sp-xxxxx"                                                                                                                                                                                        
         }                                                                                                                                                                                                             
       }
    ```
    
    修改为 `"profiles": {}` 后提示就不会再出现。
    

### OpenClaw 报错 "auth.profiles.xxx" 怎么办？

使用 OpenClaw 时出现类似以下报错：

-   `auth.profiles.qwen-portal:default.mode: Invalid input`
    
-   `auth.profiles.qwen-portal:default: Unrecognized key: "apiKey"`
    

**原因**：错误修改了`openclaw.json`文件中的`auth.profiles`字段（如将 `mode` 改为非法值、添加 `apiKey` 字段）。 `auth`仅存储认证元数据，不存储密钥。Coding Plan **无需**在 `auth.profiles` 中配置。

**解决方案**

1.  修复 `auth.profiles` 配置，删除错误添加、修改的字段和不必要的 profile。
    
2.  确认 Coding Plan 的 API Key 配置在 `models.providers.bailian.apiKey`，详情请参见[OpenClaw](https://help.aliyun.com/zh/model-studio/openclaw)。
    

### **为什么报错“HTTP 401: Incorrect API key provided.”？**

可能原因：

-   **API Key 格式错误：**API Key 填写为空、格式不正确、复制不完整，或在复制时误带了多余的空格。请确认API Key 为Coding Plan 专属 [API Key](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/coding_plan)（以 `sk-sp-` 开头），复制完整且无空格。
    
-   **Coding Plan 订阅状态已过期或失效：** Coding Plan 专属 API Key依赖于套餐的订阅状态。如果 Coding Plan 套餐已到期或失效，对应的专属 Key 将无法继续使用。请确保Coding Plan 订阅状态是否仍然有效。
    
-   **使用了错误的Base URL**：配置了 Coding Plan 专属 API Key（以 `sk-sp-` 开头），但 Base URL 仍保留为阿里云百炼通用地址（如 https://dashscope.aliyuncs.com/compatible-mode/v1）。请根据[接入的AI工具](https://help.aliyun.com/zh/model-studio/use-chat-client-or-development-tool/)，将 Base URL 替换为下表中Coding Plan 专属地址。
    
    **工具**
    
    **协议**
    
    **Base URL**
    
    OpenClaw
    
    OpenAI 兼容
    
    https://coding.dashscope.aliyuncs.com/v1
    
    OpenCode
    
    Anthropic 兼容
    
    https://coding.dashscope.aliyuncs.com/apps/anthropic/v1
    
    Claude Code
    
    Anthropic 兼容
    
    https://coding.dashscope.aliyuncs.com/apps/anthropic
    
    Cursor
    
    OpenAI 兼容
    
    https://coding.dashscope.aliyuncs.com/v1
    
    VSCode Cline
    
    OpenAI 兼容
    
    https://coding.dashscope.aliyuncs.com/v1
    
    Qwen Code
    
    OpenAI 兼容
    
    https://coding.dashscope.aliyuncs.com/v1
    
-   **使用了错误的API Key**：配置了 Coding Plan 的专属 Base URL，但 API Key 误填了阿里云百炼的通用 API Key（以 `sk-` 开头）。请将API Key更新为Coding Plan 专属 [API Key](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/coding_plan)。
    
-   **OpenClaw历史配置缓存导致配置错误：**请删除`~/.openclaw/agents/main/agent/models.json`文件中的`providers.bailian`配置项，并重启OpenClaw。
    

### **为什么报错“Authentication failed, please make sure that a valid ModelScope token is supplied.”？**

此报错表明当前接入的是第三方 ModelScope 服务，而非 Coding Plan。如需接入Coding Plan，请参考[接入客户端/开发工具](https://help.aliyun.com/zh/model-studio/use-chat-client-or-development-tool/)。

报错信息表示身份验证失败。通常是在调用 ModelScope（魔搭社区）API 服务时，填写的访问凭证有误。请按以下顺序排查：

1.  填错了平台的访问凭证：ModelScope 的 Token格式为`ms-xxx` ，阿里云百炼的通用 API Key格式为`sk-xxx`。两者为独立平台，访问凭证互不通用。请前往[ModelScope](https://www.modelscope.cn/my/access/token)获取。
    
2.  格式有误：确认复制ModelScope Token 时，无多余空格或换行符。
    

### **为什么报错“Coding Plan is currently only available for Coding Agents”？**

此报错表明使用了Coding Plan 不支持的工具或环境发起调用。

Coding Plan 仅限在编程工具（如 Claude Code、Qwen Code 等）中使用，不支持在 curl、Postman、Dify等工具上使用。

## **计费与额度相关问题**

### **为什么开通了Coding Plan还有模型 API 调用费用产生**（或导致欠费）**？**

如果开通 Coding Plan 后仍产生扣费或欠费，可能有以下原因：

1.  **未正确配置专属 API Key 和 Base URL（最常见原因）**
    
    -   原因：如果在 AI 工具中配置的是通用 API Key（格式为`sk-xxx`）和通用 Base URL（不含 coding 关键字），系统会将其识别为按量计费调用，产生按量计费的账单。
        
    -   解决方案：请务必使用Coding Plan专属配置。**API Key** 的格式必须为`sk-sp-xxx`，**Base URL** 必须包含 `coding` 关键字（如 `https://coding.dashscope.aliyuncs.com/xxx`）。详情请参见[获取套餐专属 API Key 和 Base URL](https://help.aliyun.com/zh/model-studio/coding-plan-quickstart#2782cf93b1w8h)。
        
2.  **账单结算延时导致欠费（费用产生于开通Coding Plan套餐前）**
    
    -   原因：账单按分钟汇总，出账存在分钟级延迟。 例如 16:00 产生的 API 调用，可能延至 16:05（开通Coding Plan套餐后） 才出账扣费。
        
    -   解决方案：以实际出账时间为准，详情请参见[账单查询与成本管理](https://help.aliyun.com/zh/model-studio/bill-query-and-cost-management)。
        
3.  **同时配置了 Coding Plan和通用API调用凭证，但误用了通用API调用**
    
    -   原因：若工具中同时保留了“通用”和“专属”两套配置，部分工具（如 OpenClaw）会自动路由到通用凭证进行请求，从而产生扣费。
        
    -   解决方案：建议在工具中移除通用 API 配置，并确保选用[Coding Plan支持的模型](https://help.aliyun.com/zh/model-studio/coding-plan#2bbc4faf2ej0e)。例如在 OpenCode 中，请选择供应商标为“Model Studio Coding Plan”的模型。
        
4.  **客户端缓存未清理**
    
    -   原因：配置新凭证后，部分工具可能仍在读取旧的通用API调用凭证缓存。
        
    -   解决方案：清理缓存并重启。以 OpenClaw 为例：删除 `~/.openclaw/agents/main/agent/models.json` 文件，执行 `openclaw gateway restart` 重启服务后，再根据[OpenClaw](https://help.aliyun.com/zh/model-studio/openclaw)重新配置。
        

### **额度用完了怎么办？**

-   **Lite 套餐**：5 小时或每周额度用完后可等待自动恢复；每月额度用完需等待至下个订阅月恢复。
    
-   **Pro 套餐**：5 小时或每周额度用完后等待自动恢复；每月额度用完需等待至下个订阅月恢复。
    

### **Coding Plan 额度用完后会转为按量计费吗？**

Coding Plan 额度消耗完毕后，继续调用会失败报错，并且不会自动转为按量付费模式计费。如需继续使用，请等待下一订阅周期额度刷新。

### **Coding Plan 可以使用百炼的模型免费试用吗？**

Coding Plan 是一个独立的订阅产品，其计费和配额系统**不参与**百炼的通用模型免费试用计划。

### **为什么 2 月购买的 Coding Plan 只有 28 天，而不是 31 天？**

套餐自开通时刻起生效，有效期至次月对应日 23:59:59（UTC+8）结束。若次月没有对应日期，则有效期至次月最后一日23:59:59（UTC+8）结束。

例如：2026 年 2 月 3 日开通 Coding Plan，有效期至 2026 年 3 月 3 日，因此剩余天数为 28 天。

### **如何查看 Token 消耗信息？**

暂无法查看。Coding Plan的额度消耗与 Token 消耗无关，只与模型调用次数有关。可在[Coding Plan页面](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/coding_plan)查看用量信息。

### 可以查询 Coding Plan 套餐内特定模型（如qwen3.6-plus）的使用量吗？

不支持。[Coding Plan页面](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/coding_plan)仅展示套餐总额度的整体消耗和剩余情况。

### **Coding Plan 有年付套餐吗？**

目前 Coding Plan 仅支持按月订阅，暂无年付套餐。

### 为什么自动续费失败？

通常有以下原因：

1.  **设置后未生效**：开启自动续订后次日生效，并非立即执行续订。
    
2.  **已超过自动扣款周期**：自动续订将于资源到期前 9 天的 08:00:00 （UTC+8） 开始扣款，如扣款失败，次日会继续扣款直到扣款成功或到期前 1 天。资源到期前 1 天不支持自动续订，请手动续订。
    
3.  **账户余额不足**：自动续订扣款仅可扣除账户可用额度（不支持银行卡、支付宝或信用卡），请保证额度充足。如扣款失败，次日会继续扣款，直到扣款成功或到期前 1 天。
    

### **到期后还能续费吗？**

到期后不支持续费操作。

### 续费报错“当前已经存在待生效续费，不允许重复续费”怎么办?

**原因**：当前账号已经续费到下个月，不支持手动续费到更多月份。

### **Coding Plan 提前续订后，新服务周期如何计算？**

新购 1 个月套餐，按照自然月计算订单时长。套餐自开通时刻起生效，有效期至次月对应日 23:59:59（UTC+8）结束。若次月没有对应日期，则有效期至次月最后一日23:59:59（UTC+8）结束。提前续订时，新周期在原到期日基础上自动顺延。

例如：

-   首次开通为 3 月 15 日 10:00，有效期至 4 月 15 日 23:59:59。
    
-   4 月 10 日提前续订 1 个月，新有效期至 5 月 15 日 23:59:59。
    

### **续订是否可以使用代金券抵扣？**

可以使用通用代金券。

### **续费入口在哪里？**

Pro 套餐可以在[Coding Plan页面](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/coding_plan)或[资源续订页面](https://billing-cost.console.aliyun.com/renew/manual)进行续费。Lite 基础套餐停止续费通知请参见[公告](https://www.aliyun.com/notice/118175)。

## **产品功能相关问题**

### **Coding Plan支持哪些模型？**

Lite 套餐和Pro 套餐**均**支持套餐内全部模型（含千问、GLM、Kimi、MiniMax）。完整模型列表请参见[Coding Plan概述](https://help.aliyun.com/zh/model-studio/coding-plan)。

### **Coding Plan 支持的模型列表会更新吗？**

Coding Plan 支持的模型会不定期更新，当前支持的模型以[Coding Plan概述](https://help.aliyun.com/zh/model-studio/coding-plan)页面展示为准，敬请关注。

### **每个百炼账号支持同时开通几个 Coding Plan？**

每个百炼账号同时只能订阅一个 Coding Plan（不区分 Lite 和 Pro 套餐版本）。

### **是否可以使用**[**支持的模型列表**](https://help.aliyun.com/zh/model-studio/coding-plan#dc0d98da6ev4j)**以外的模型？**

Coding Plan 当前仅可以使用[支持的模型列表](https://help.aliyun.com/zh/model-studio/coding-plan#dc0d98da6ev4j)中的模型，使用其他模型会报错。

### Lite 和 Pro 套餐的模型响应速度相同吗？

Lite 基础套餐和 Pro 高级套餐在模型响应速度上是相同的，两个套餐使用的是同样的模型资源和推理服务。

### Lite 套餐可以续费和升级吗？

自 2026 年 4 月 13 日起，Lite 基础套餐将停止续费，且不再支持升级至 Pro 套餐，详情请参见[公告](https://www.aliyun.com/notice/118175)。

-   如您已购买 Coding Plan Lite 基础套餐，您仍可继续使用至服务到期。
    
-   如您已开通 Coding Plan Lite 基础套餐自动续费，自动续费将于自公告起 30 日之后自动失效，您仍可继续使用至服务到期。
    

感谢您对于阿里云百炼的理解与支持。

### Pro套餐是否可以降级到Lite套餐？

不支持降配。

### Coding Plan 有并发限制吗？

Coding Plan 存在并发限制。平台会根据整体资源负载动态调整并发上限，在高峰时段避免资源过载，确保每个 Agent 都能获得稳定的响应速度和推理质量。触发并发限制时，等待片刻后重试即可。

### Coding Plan是否支持多人使用？

Coding Plan 的 API Key 仅供个人使用，暂不支持多人共享，请勿与他人共享。若系统检测到您的 API Key 存在公开泄露的情况，可能会自动将其禁用。

### Pro 套餐支持企业多名开发人员同时使用吗？

不支持。请妥善保存密钥信息，不要与他人共享，或者暴露在客户端代码中。若系统检测到您的 API Key 存在公开泄露的情况，可能会自动将其禁用。

### 各模型的上下文长度是多少？超出上下文长度如何处理？

**模型名称**

**上下文长度（Tokens）**

qwen3.6-plus

1,000,000

qwen3.5-plus

1,000,000

kimi-k2.5

262,144

glm-5

202,752

MiniMax-M2.5

196,608

qwen3-max-2026-01-23

262,144

qwen3-coder-next

262,144

qwen3-coder-plus

1,000,000

glm-4.7

202,752

当遇到与上下文超限相关的报错时，建议新建会话。此外，可以通过以下方式来避免超出上下文长度：

1.  **切换模型**：切换支持更长上下文的模型，如 qwen3.6-plus、qwen3.5-plus、qwen3-coder-plus。
    
2.  **减少无关文件**：建议在具体的项目目录中启动 AI 编程工具，同时仅保留必要的项目文件。
    
3.  **拆分任务**：将复杂任务拆成若干子任务，逐项提问，降低单次请求的上下文占用。
    
4.  **精确指令**：模糊的请求会触发非必要的文件扫描，请在使用 AI 编程工具时提出更明确、具体的问题或指令。
    

具体操作因工具而异，请参考[接入客户端/开发工具](https://help.aliyun.com/zh/model-studio/use-chat-client-or-development-tool/)。

### Coding Plan 如何重置 API Key？

在[Coding Plan页面](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/coding_plan)，点击Coding Plan 的 API Key 旁边的**重置**按钮即可。

**说明**

重置后，您需要将新的API Key更新到所有使用的工具中，否则将会导致工具不可用。

### Coding Plan 到期不续费，重新开通后**API Key**会重置吗？

会重置；在到期前续费则不会重置。

### **Coding Plan 到期前有无提醒？**

有提醒。系统会在到期前7、3、1天，通过站内信、邮件、短信以及智能外呼提醒您及时续订。

### **支持为 Coding Plan 配置到期消息订阅吗？**

不支持，也无需额外配置。系统会在到期前 7 天、3 天、1 天，通过站内信、邮件、短信以及智能外呼自动推送到期提醒，无需手动订阅。

### **Coding Plan 可以生成多个 API Key 吗？**

当前仅支持一个 API Key。

### **Coding Plan 支持设置使用的IP白名单吗？**

不支持。如果API Key泄露，请在[Coding Plan页面](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/coding_plan)重置API Key。

### **子账号如何查看获取 Coding Plan API Key？**

请联系主账号或具有管理员权限的子账号为账号添加**订阅套餐**权限。

### **VSCode 如何使用 Coding Plan？**

使用支持接入兼容OpenAI / Anthropic API 协议的插件，如 Qwen Code、Claude Code 等。

### **Coding Plan 中的模型是否经过量化处理？**

Coding Plan 套餐中包含的模型（如 glm-5、qwen3.5-plus 等）均为完整版模型，未经过量化或功能阉割，属于满血版本。

### **Coding Plan 和节省计划有什么区别？**

**对比项**

[**Coding Plan**](https://help.aliyun.com/zh/model-studio/coding-plan)

[**AI 通用节省计划**](https://help.aliyun.com/zh/model-studio/savings-plan-and-resource-package)

用途

在 AI 编程工具中使用（Claude Code、OpenClaw 等）

抵扣阿里云百炼通用 API 按量调用费用

API Key 格式

`sk-sp-xxx`（专属 Key）

`sk-xxx`（百炼通用 Key）

Base URL域名

`coding.dashscope.aliyuncs.com`

`dashscope.aliyuncs.com`

计费方式

按套餐按月计费

按 Token 用量计费

适用场景

交互式 AI 编程

API 调用、应用开发

### data\_inspection\_failed 报错如何处理？

请参见[错误码](https://help.aliyun.com/zh/model-studio/error-code#inappropriate-content)文档。

### **Coding Plan 配置 Dify 为什么报错？**

不建议在 Dify 中使用 Coding Plan。Coding Plan 套餐额度仅可在编程工具（如 Claude Code、Qwen Code 等）中使用，禁止以 API 调用的形式用于自动化脚本、自定义应用程序后端或任何非交互式批量调用场景。将套餐 API Key 用于允许范围之外的调用将被视为违规或滥用，可能会导致订阅被暂停或 API Key 被封禁。

### **Coding Plan** 能在 postman上调用吗？

不建议。Coding Plan 套餐额度仅可在编程工具（如 Claude Code、Qwen Code 等）中使用，禁止以 API 调用的形式用于自动化脚本、自定义应用程序后端或任何非交互式批量调用场景。将套餐 API Key 用于允许范围之外的调用将被视为违规或滥用，可能会导致订阅被暂停或 API Key 被封禁。
