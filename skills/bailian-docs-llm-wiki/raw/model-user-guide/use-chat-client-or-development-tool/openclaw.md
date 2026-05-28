# OpenClaw

OpenClaw 是一个开源的个人 AI 助手平台，支持通过多种消息渠道与 AI 交互。通过配置可接入阿里云百炼平台上的 AI 模型，支持按量付费、Coding Plan、Token Plan 团队版三种接入方式。

## **安装 OpenClaw**

OpenClaw 需要 Node.js 22 或更高版本。可通过以下命令检查 Node.js 版本：

```
node --version
```

如果未安装或版本过低，请访问 [Node.js 官网](https://nodejs.org/)下载安装。

## macOS / Linux

推荐使用官方安装脚本：

```
curl -fsSL https://openclaw.ai/install.sh | bash
```

或通过 npm 全局安装：

```
npm install -g openclaw@latest
```

## Windows

在 PowerShell 中执行：

```
iwr -useb https://openclaw.ai/install.ps1 | iex
```

或通过 npm 全局安装：

```
npm install -g openclaw@latest
```

首次安装后，OpenClaw 会自动启动配置向导，完成初始设置。也可以手动执行`openclaw onboard`命令进行配置。

**配置项**

**建议配置**

I understand this is powerful and inherently risky. Continue?

选择 **Yes**

Onboarding mode

选择 **QuickStart**

Model/auth provider

选择 **Skip for now**（稍后配置百炼模型）

Filter models by provider

选择 **All providers**

Default model

选择 **Keep current**

Select channel (QuickStart)

选择 **Skip for now**（稍后配置渠道）

Configure skills now? (recommended)

选择 **No**

Enable hooks?

按空格键选中选项，按回车键进入下一步

How do you want to hatch your bot?

选择 **Do this later**

## **配置接入凭证**

### **Token Plan 团队版**

将 `YOUR_API_KEY` 替换为 Token Plan 团队版专属 [API Key](https://bailian.console.aliyun.com/?tab=plan#/efm/subscription/overview)。可用模型请参考 Token Plan 团队版[支持的模型](https://help.aliyun.com/zh/model-studio/token-plan-overview)。

**API Key**

Token Plan 团队版专属 [API Key](https://bailian.console.aliyun.com/?tab=plan#/efm/subscription/overview)

**Base URL**

`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`

**可用模型**

Token Plan 团队版[支持的模型](https://help.aliyun.com/zh/model-studio/token-plan-overview)

配置文件位于 `~/.openclaw/openclaw.json`，OpenClaw 启动时会自动读取。

**说明**

示例禁用了网关鉴权（`auth.mode: none`），仅适合单机本地使用。如需共享或远程访问，请运行 `openclaw doctor --fix` 启用 token 鉴权。

## 方式一：终端方式

1.  **打开配置文件**
    
    ```
    nano ~/.openclaw/openclaw.json
    ```
    
2.  **写入配置**
    
    **首次配置**：复制以下内容到配置文件，将 `YOUR_API_KEY` 替换为 Token Plan 团队版 API Key。
    
    **已有配置**：若需保留已有配置，请勿直接全量替换，详见[已有配置如何安全修改](#cp-openclaw-faq-safe-modify-title)。
    
    ```
    {
      "meta": {
        "lastTouchedVersion": "2026.2.1",
        "lastTouchedAt": "2026-02-03T08:20:00.000Z"
      },
      "models": {
        "mode": "merge",
        "providers": {
          "bailian-token-plan": {
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic",
            "apiKey": "YOUR_API_KEY",
            "api": "anthropic-messages",
            "models": [
              {
                "id": "qwen3.7-max",
                "name": "qwen3.7-max",
                "reasoning": false,
                "input": ["text"],
                "contextWindow": 1000000,
                "maxTokens": 65536,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "compat": { "thinkingFormat": "openai" }
              },
              {
                "id": "qwen3.6-plus",
                "name": "qwen3.6-plus",
                "reasoning": false,
                "input": ["text", "image"],
                "contextWindow": 1000000,
                "maxTokens": 65536,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "compat": { "thinkingFormat": "openai" }
              },
              {
                "id": "qwen3.6-flash",
                "name": "qwen3.6-flash",
                "reasoning": false,
                "input": ["text", "image"],
                "contextWindow": 1000000,
                "maxTokens": 32768,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "compat": { "thinkingFormat": "openai" }
              },
              {
                "id": "deepseek-v4-pro",
                "name": "deepseek-v4-pro",
                "reasoning": false,
                "input": ["text"],
                "contextWindow": 163840,
                "maxTokens": 32768,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 }
              },
              {
                "id": "deepseek-v4-flash",
                "name": "deepseek-v4-flash",
                "reasoning": false,
                "input": ["text"],
                "contextWindow": 163840,
                "maxTokens": 16384,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 }
              },
              {
                "id": "deepseek-v3.2",
                "name": "deepseek-v3.2",
                "reasoning": false,
                "input": ["text"],
                "contextWindow": 163840,
                "maxTokens": 16384,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "compat": { "thinkingFormat": "openai" }
              },
              {
                "id": "kimi-k2.6",
                "name": "kimi-k2.6",
                "reasoning": false,
                "input": ["text", "image"],
                "contextWindow": 262144,
                "maxTokens": 32768,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "compat": { "thinkingFormat": "openai" }
              },
              {
                "id": "kimi-k2.5",
                "name": "kimi-k2.5",
                "reasoning": false,
                "input": ["text", "image"],
                "contextWindow": 262144,
                "maxTokens": 16384,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "compat": { "thinkingFormat": "openai" }
              },
              {
                "id": "glm-5.1",
                "name": "glm-5.1",
                "reasoning": false,
                "input": ["text"],
                "contextWindow": 202752,
                "maxTokens": 16384,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "compat": { "thinkingFormat": "openai" }
              },
              {
                "id": "glm-5",
                "name": "glm-5",
                "reasoning": false,
                "input": ["text"],
                "contextWindow": 202752,
                "maxTokens": 16384,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "compat": { "thinkingFormat": "openai" }
              },
              {
                "id": "MiniMax-M2.5",
                "name": "MiniMax-M2.5",
                "reasoning": false,
                "input": ["text"],
                "contextWindow": 204800,
                "maxTokens": 131072,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 }
              }
            ]
          }
        }
      },
      "agents": {
        "defaults": {
          "model": {
            "primary": "bailian-token-plan/qwen3.6-plus"
          },
          "models": {
            "bailian-token-plan/qwen3.7-max": {},
            "bailian-token-plan/qwen3.6-plus": {},
            "bailian-token-plan/qwen3.6-flash": {},
            "bailian-token-plan/deepseek-v4-pro": {},
            "bailian-token-plan/deepseek-v4-flash": {},
            "bailian-token-plan/deepseek-v3.2": {},
            "bailian-token-plan/kimi-k2.6": {},
            "bailian-token-plan/kimi-k2.5": {},
            "bailian-token-plan/glm-5.1": {},
            "bailian-token-plan/glm-5": {},
            "bailian-token-plan/MiniMax-M2.5": {}
          }
        }
      },
      "gateway": {
        "mode": "local",
        "auth": { "mode": "none" }
      }
    }
    ```
    
3.  **保存并退出**
    
    按 `Ctrl+X`，按 `Y` 确认保存，按 `Enter` 确认文件名。
    
4.  **使配置生效**
    
    运行以下命令重启网关，使配置生效。
    
    ```
    openclaw gateway restart
    ```
    

## 方式二：Web UI 方式

**说明**

Web UI 方式仅在 OpenClaw **≤ 2026.3.28** 可用，更高版本请使用方式一：终端方式。

1.  **启动 Web UI**
    
    在终端运行以下命令启动 Web UI：
    
    ```
    openclaw dashboard
    ```
    
    在浏览器打开的页面中，单击左侧菜单 **设置**，将编辑器模式从 **Form** 切换为 **Raw**。
    
2.  **写入配置**
    
    **首次配置**：复制以下内容到配置文件，将 `YOUR_API_KEY` 替换为 Token Plan 团队版 API Key。
    
    **已有配置**：若需保留已有配置，请勿直接全量替换，详见[已有配置如何安全修改](#cp-openclaw-faq-safe-modify-title)。
    
    ```
    {
      "meta": {
        "lastTouchedVersion": "2026.2.1",
        "lastTouchedAt": "2026-02-03T08:20:00.000Z"
      },
      "models": {
        "mode": "merge",
        "providers": {
          "bailian-token-plan": {
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic",
            "apiKey": "YOUR_API_KEY",
            "api": "anthropic-messages",
            "models": [
              {
                "id": "qwen3.7-max",
                "name": "qwen3.7-max",
                "reasoning": false,
                "input": ["text"],
                "contextWindow": 1000000,
                "maxTokens": 65536,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "compat": { "thinkingFormat": "openai" }
              },
              {
                "id": "qwen3.6-plus",
                "name": "qwen3.6-plus",
                "reasoning": false,
                "input": ["text", "image"],
                "contextWindow": 1000000,
                "maxTokens": 65536,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "compat": { "thinkingFormat": "openai" }
              },
              {
                "id": "qwen3.6-flash",
                "name": "qwen3.6-flash",
                "reasoning": false,
                "input": ["text", "image"],
                "contextWindow": 1000000,
                "maxTokens": 32768,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "compat": { "thinkingFormat": "openai" }
              },
              {
                "id": "deepseek-v4-pro",
                "name": "deepseek-v4-pro",
                "reasoning": false,
                "input": ["text"],
                "contextWindow": 163840,
                "maxTokens": 32768,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 }
              },
              {
                "id": "deepseek-v4-flash",
                "name": "deepseek-v4-flash",
                "reasoning": false,
                "input": ["text"],
                "contextWindow": 163840,
                "maxTokens": 16384,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 }
              },
              {
                "id": "deepseek-v3.2",
                "name": "deepseek-v3.2",
                "reasoning": false,
                "input": ["text"],
                "contextWindow": 163840,
                "maxTokens": 16384,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "compat": { "thinkingFormat": "openai" }
              },
              {
                "id": "kimi-k2.6",
                "name": "kimi-k2.6",
                "reasoning": false,
                "input": ["text", "image"],
                "contextWindow": 262144,
                "maxTokens": 32768,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "compat": { "thinkingFormat": "openai" }
              },
              {
                "id": "kimi-k2.5",
                "name": "kimi-k2.5",
                "reasoning": false,
                "input": ["text", "image"],
                "contextWindow": 262144,
                "maxTokens": 16384,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "compat": { "thinkingFormat": "openai" }
              },
              {
                "id": "glm-5.1",
                "name": "glm-5.1",
                "reasoning": false,
                "input": ["text"],
                "contextWindow": 202752,
                "maxTokens": 16384,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "compat": { "thinkingFormat": "openai" }
              },
              {
                "id": "glm-5",
                "name": "glm-5",
                "reasoning": false,
                "input": ["text"],
                "contextWindow": 202752,
                "maxTokens": 16384,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "compat": { "thinkingFormat": "openai" }
              },
              {
                "id": "MiniMax-M2.5",
                "name": "MiniMax-M2.5",
                "reasoning": false,
                "input": ["text"],
                "contextWindow": 204800,
                "maxTokens": 131072,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 }
              }
            ]
          }
        }
      },
      "agents": {
        "defaults": {
          "model": {
            "primary": "bailian-token-plan/qwen3.6-plus"
          },
          "models": {
            "bailian-token-plan/qwen3.7-max": {},
            "bailian-token-plan/qwen3.6-plus": {},
            "bailian-token-plan/qwen3.6-flash": {},
            "bailian-token-plan/deepseek-v4-pro": {},
            "bailian-token-plan/deepseek-v4-flash": {},
            "bailian-token-plan/deepseek-v3.2": {},
            "bailian-token-plan/kimi-k2.6": {},
            "bailian-token-plan/kimi-k2.5": {},
            "bailian-token-plan/glm-5.1": {},
            "bailian-token-plan/glm-5": {},
            "bailian-token-plan/MiniMax-M2.5": {}
          }
        }
      },
      "gateway": {
        "mode": "local",
        "auth": { "mode": "none" }
      }
    }
    ```
    
3.  **保存并应用**
    
    先单击 **Save** 按钮将配置写入磁盘，再单击 **Apply** 按钮重启网关使配置生效。
    

### **Coding Plan**

将 `YOUR_API_KEY` 替换为 Coding Plan 专属 [API Key](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/coding_plan)（格式为 `sk-sp-xxxxx`）。可用模型请参考 Coding Plan [支持的模型](https://help.aliyun.com/zh/model-studio/coding-plan)。

**API Key**

Coding Plan 专属 [API Key](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/coding_plan)，格式为 `sk-sp-xxxxx`

**Base URL**

`https://coding.dashscope.aliyuncs.com/apps/anthropic`

**可用模型**

Coding Plan [支持的模型](https://help.aliyun.com/zh/model-studio/coding-plan)

配置文件位于 `~/.openclaw/openclaw.json`，OpenClaw 启动时会自动读取。

**说明**

示例禁用了网关鉴权（`auth.mode: none`），仅适合单机本地使用。如需共享或远程访问，请运行 `openclaw doctor --fix` 启用 token 鉴权。

## 方式一：终端方式

1.  **打开配置文件**
    
    ```
    nano ~/.openclaw/openclaw.json
    ```
    
2.  **写入配置**
    
    **首次配置**：复制以下内容到配置文件，将 `YOUR_API_KEY` 替换为 Coding Plan API Key。
    
    **已有配置**：若需保留已有配置，请勿直接全量替换，详见[已有配置如何安全修改](#cp-openclaw-faq-safe-modify-title)。
    
    ```
    {
      "meta": {
        "lastTouchedVersion": "2026.2.1",
        "lastTouchedAt": "2026-02-03T08:20:00.000Z"
      },
      "models": {
        "mode": "merge",
        "providers": {
          "bailian-coding-plan": {
            "baseUrl": "https://coding.dashscope.aliyuncs.com/apps/anthropic",
            "apiKey": "YOUR_API_KEY",
            "api": "anthropic-messages",
            "models": [
              {
                "id": "qwen3.6-plus",
                "name": "qwen3.6-plus",
                "reasoning": false,
                "input": ["text", "image"],
                "contextWindow": 1000000,
                "maxTokens": 65536,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "compat": { "thinkingFormat": "openai" }
              },
              {
                "id": "qwen3.5-plus",
                "name": "qwen3.5-plus",
                "reasoning": false,
                "input": ["text", "image"],
                "contextWindow": 1000000,
                "maxTokens": 65536,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "compat": { "thinkingFormat": "openai" }
              },
              {
                "id": "qwen3-max-2026-01-23",
                "name": "qwen3-max-2026-01-23",
                "reasoning": false,
                "input": ["text"],
                "contextWindow": 262144,
                "maxTokens": 65536,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "compat": { "thinkingFormat": "openai" }
              },
              {
                "id": "qwen3-coder-next",
                "name": "qwen3-coder-next",
                "reasoning": false,
                "input": ["text"],
                "contextWindow": 262144,
                "maxTokens": 65536,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 }
              },
              {
                "id": "qwen3-coder-plus",
                "name": "qwen3-coder-plus",
                "reasoning": false,
                "input": ["text"],
                "contextWindow": 1000000,
                "maxTokens": 65536,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 }
              },
              {
                "id": "MiniMax-M2.5",
                "name": "MiniMax-M2.5",
                "reasoning": false,
                "input": ["text"],
                "contextWindow": 204800,
                "maxTokens": 131072,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 }
              },
              {
                "id": "glm-5",
                "name": "glm-5",
                "reasoning": false,
                "input": ["text"],
                "contextWindow": 202752,
                "maxTokens": 16384,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "compat": { "thinkingFormat": "openai" }
              },
              {
                "id": "glm-4.7",
                "name": "glm-4.7",
                "reasoning": false,
                "input": ["text"],
                "contextWindow": 202752,
                "maxTokens": 16384,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 }
              },
              {
                "id": "kimi-k2.5",
                "name": "kimi-k2.5",
                "reasoning": false,
                "input": ["text", "image"],
                "contextWindow": 262144,
                "maxTokens": 16384,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "compat": { "thinkingFormat": "openai" }
              }
            ]
          }
        }
      },
      "agents": {
        "defaults": {
          "model": {
            "primary": "bailian-coding-plan/qwen3.6-plus"
          },
          "models": {
            "bailian-coding-plan/qwen3.6-plus": {},
            "bailian-coding-plan/qwen3.5-plus": {},
            "bailian-coding-plan/qwen3-max-2026-01-23": {},
            "bailian-coding-plan/qwen3-coder-next": {},
            "bailian-coding-plan/qwen3-coder-plus": {},
            "bailian-coding-plan/MiniMax-M2.5": {},
            "bailian-coding-plan/glm-5": {},
            "bailian-coding-plan/glm-4.7": {},
            "bailian-coding-plan/kimi-k2.5": {}
          }
        }
      },
      "gateway": {
        "mode": "local",
        "auth": { "mode": "none" }
      }
    }
    ```
    
3.  **保存并退出**
    
    按 `Ctrl+X`，按 `Y` 确认保存，按 `Enter` 确认文件名。
    
4.  **使配置生效**
    
    运行以下命令重启网关，使配置生效。
    
    ```
    openclaw gateway restart
    ```
    

## 方式二：Web UI 方式

**说明**

Web UI 方式仅在 OpenClaw **≤ 2026.3.28** 可用，更高版本请使用[方式一：终端方式](#cp-terminal-h2)。

1.  **启动 Web UI**
    
    在终端运行以下命令启动 Web UI：
    
    ```
    openclaw dashboard
    ```
    
    在浏览器打开的页面中，单击左侧菜单 **设置**，将编辑器模式从 **Form** 切换为 **Raw**。
    
2.  **写入配置**
    
    **首次配置**：复制以下内容到配置文件，将 `YOUR_API_KEY` 替换为 Coding Plan API Key。
    
    **已有配置**：若需保留已有配置，请勿直接全量替换，详见[已有配置如何安全修改](#cp-openclaw-faq-safe-modify-title)。
    
    ```
    {
      "meta": {
        "lastTouchedVersion": "2026.2.1",
        "lastTouchedAt": "2026-02-03T08:20:00.000Z"
      },
      "models": {
        "mode": "merge",
        "providers": {
          "bailian-coding-plan": {
            "baseUrl": "https://coding.dashscope.aliyuncs.com/apps/anthropic",
            "apiKey": "YOUR_API_KEY",
            "api": "anthropic-messages",
            "models": [
              {
                "id": "qwen3.6-plus",
                "name": "qwen3.6-plus",
                "reasoning": false,
                "input": ["text", "image"],
                "contextWindow": 1000000,
                "maxTokens": 65536,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "compat": { "thinkingFormat": "openai" }
              },
              {
                "id": "qwen3.5-plus",
                "name": "qwen3.5-plus",
                "reasoning": false,
                "input": ["text", "image"],
                "contextWindow": 1000000,
                "maxTokens": 65536,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "compat": { "thinkingFormat": "openai" }
              },
              {
                "id": "qwen3-max-2026-01-23",
                "name": "qwen3-max-2026-01-23",
                "reasoning": false,
                "input": ["text"],
                "contextWindow": 262144,
                "maxTokens": 65536,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "compat": { "thinkingFormat": "openai" }
              },
              {
                "id": "qwen3-coder-next",
                "name": "qwen3-coder-next",
                "reasoning": false,
                "input": ["text"],
                "contextWindow": 262144,
                "maxTokens": 65536,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 }
              },
              {
                "id": "qwen3-coder-plus",
                "name": "qwen3-coder-plus",
                "reasoning": false,
                "input": ["text"],
                "contextWindow": 1000000,
                "maxTokens": 65536,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 }
              },
              {
                "id": "MiniMax-M2.5",
                "name": "MiniMax-M2.5",
                "reasoning": false,
                "input": ["text"],
                "contextWindow": 204800,
                "maxTokens": 131072,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 }
              },
              {
                "id": "glm-5",
                "name": "glm-5",
                "reasoning": false,
                "input": ["text"],
                "contextWindow": 202752,
                "maxTokens": 16384,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "compat": { "thinkingFormat": "openai" }
              },
              {
                "id": "glm-4.7",
                "name": "glm-4.7",
                "reasoning": false,
                "input": ["text"],
                "contextWindow": 202752,
                "maxTokens": 16384,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 }
              },
              {
                "id": "kimi-k2.5",
                "name": "kimi-k2.5",
                "reasoning": false,
                "input": ["text", "image"],
                "contextWindow": 262144,
                "maxTokens": 16384,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "compat": { "thinkingFormat": "openai" }
              }
            ]
          }
        }
      },
      "agents": {
        "defaults": {
          "model": {
            "primary": "bailian-coding-plan/qwen3.6-plus"
          },
          "models": {
            "bailian-coding-plan/qwen3.6-plus": {},
            "bailian-coding-plan/qwen3.5-plus": {},
            "bailian-coding-plan/qwen3-max-2026-01-23": {},
            "bailian-coding-plan/qwen3-coder-next": {},
            "bailian-coding-plan/qwen3-coder-plus": {},
            "bailian-coding-plan/MiniMax-M2.5": {},
            "bailian-coding-plan/glm-5": {},
            "bailian-coding-plan/glm-4.7": {},
            "bailian-coding-plan/kimi-k2.5": {}
          }
        }
      },
      "gateway": {
        "mode": "local",
        "auth": { "mode": "none" }
      }
    }
    ```
    
3.  **保存并应用**
    
    先单击 **Save** 按钮将配置写入磁盘，再单击 **Apply** 按钮重启网关使配置生效。
    

### **按量付费**

将 `YOUR_API_KEY` 替换为[阿里云百炼 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)（格式为 `sk-xxxxx`）。可用模型请参考[模型广场](https://bailian.console.aliyun.com/?tab=model#/model-market)。

**API Key**

[阿里云百炼 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，格式为 `sk-xxxxx`

**Base URL**

请确保 Base URL、API Key 和模型归属同一地域：

-   华北2（北京）：`https://dashscope.aliyuncs.com/apps/anthropic`
    
-   新加坡：`https://dashscope-intl.aliyuncs.com/apps/anthropic`
    

**可用模型**

填入[模型广场](https://bailian.console.aliyun.com/?tab=model#/model-market)中支持的模型

以下配置以华北2（北京）地域为例，如使用其他地域请替换 `baseUrl` 为上表中对应地域的 URL。

配置文件位于 `~/.openclaw/openclaw.json`，OpenClaw 启动时会自动读取。

**说明**

示例禁用了网关鉴权（`auth.mode: none`），仅适合单机本地使用。如需共享或远程访问，请运行 `openclaw doctor --fix` 启用 token 鉴权。

## 方式一：终端方式

1.  **打开配置文件**
    
    ```
    nano ~/.openclaw/openclaw.json
    ```
    
2.  **写入配置**
    
    **首次配置**：复制以下内容到配置文件，将 `YOUR_API_KEY` 替换为百炼 API Key。
    
    **已有配置**：若需保留已有配置，请勿直接全量替换，详见[已有配置如何安全修改](#cp-openclaw-faq-safe-modify-title)。
    
    ```
    {
      "meta": {
        "lastTouchedVersion": "2026.2.1",
        "lastTouchedAt": "2026-02-03T08:20:00.000Z"
      },
      "models": {
        "mode": "merge",
        "providers": {
          "bailian": {
            "baseUrl": "https://dashscope.aliyuncs.com/apps/anthropic",
            "apiKey": "YOUR_API_KEY",
            "api": "anthropic-messages",
            "models": [
              {
                "id": "qwen3.6-plus",
                "name": "qwen3.6-plus",
                "reasoning": false,
                "input": ["text", "image"],
                "contextWindow": 1000000,
                "maxTokens": 65536,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "compat": { "thinkingFormat": "openai" }
              },
              {
                "id": "MiniMax-M2.5",
                "name": "MiniMax-M2.5",
                "reasoning": false,
                "input": ["text"],
                "contextWindow": 204800,
                "maxTokens": 131072,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 }
              },
              {
                "id": "glm-5",
                "name": "glm-5",
                "reasoning": false,
                "input": ["text"],
                "contextWindow": 202752,
                "maxTokens": 16384,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "compat": { "thinkingFormat": "openai" }
              },
              {
                "id": "deepseek-v3.2",
                "name": "deepseek-v3.2",
                "reasoning": false,
                "input": ["text"],
                "contextWindow": 163840,
                "maxTokens": 16384,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "compat": { "thinkingFormat": "openai" }
              }
            ]
          }
        }
      },
      "agents": {
        "defaults": {
          "model": {
            "primary": "bailian/qwen3.6-plus"
          },
          "models": {
            "bailian/qwen3.6-plus": {},
            "bailian/MiniMax-M2.5": {},
            "bailian/glm-5": {},
            "bailian/deepseek-v3.2": {}
          }
        }
      },
      "gateway": {
        "mode": "local",
        "auth": { "mode": "none" }
      }
    }
    ```
    
3.  **保存并退出**
    
    按 `Ctrl+X`，按 `Y` 确认保存，按 `Enter` 确认文件名。
    
4.  **使配置生效**
    
    运行以下命令重启网关，使配置生效。
    
    ```
    openclaw gateway restart
    ```
    

## 方式二：Web UI 方式

**说明**

Web UI 方式仅在 OpenClaw **≤ 2026.3.28** 可用，更高版本请使用[方式一：终端方式](#payg-terminal-h2)。

1.  **启动 Web UI**
    
    在终端运行以下命令启动 Web UI：
    
    ```
    openclaw dashboard
    ```
    
    在浏览器打开的页面中，单击左侧菜单 **设置**，将编辑器模式从 **Form** 切换为 **Raw**。
    
2.  **写入配置**
    
    **首次配置**：复制以下内容到配置文件，将 `YOUR_API_KEY` 替换为百炼 API Key。
    
    **已有配置**：若需保留已有配置，请勿直接全量替换，详见[已有配置如何安全修改](#cp-openclaw-faq-safe-modify-title)。
    
    ```
    {
      "meta": {
        "lastTouchedVersion": "2026.2.1",
        "lastTouchedAt": "2026-02-03T08:20:00.000Z"
      },
      "models": {
        "mode": "merge",
        "providers": {
          "bailian": {
            "baseUrl": "https://dashscope.aliyuncs.com/apps/anthropic",
            "apiKey": "YOUR_API_KEY",
            "api": "anthropic-messages",
            "models": [
              {
                "id": "qwen3.6-plus",
                "name": "qwen3.6-plus",
                "reasoning": false,
                "input": ["text", "image"],
                "contextWindow": 1000000,
                "maxTokens": 65536,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "compat": { "thinkingFormat": "openai" }
              },
              {
                "id": "MiniMax-M2.5",
                "name": "MiniMax-M2.5",
                "reasoning": false,
                "input": ["text"],
                "contextWindow": 204800,
                "maxTokens": 131072,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 }
              },
              {
                "id": "glm-5",
                "name": "glm-5",
                "reasoning": false,
                "input": ["text"],
                "contextWindow": 202752,
                "maxTokens": 16384,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "compat": { "thinkingFormat": "openai" }
              },
              {
                "id": "deepseek-v3.2",
                "name": "deepseek-v3.2",
                "reasoning": false,
                "input": ["text"],
                "contextWindow": 163840,
                "maxTokens": 16384,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "compat": { "thinkingFormat": "openai" }
              }
            ]
          }
        }
      },
      "agents": {
        "defaults": {
          "model": {
            "primary": "bailian/qwen3.6-plus"
          },
          "models": {
            "bailian/qwen3.6-plus": {},
            "bailian/MiniMax-M2.5": {},
            "bailian/glm-5": {},
            "bailian/deepseek-v3.2": {}
          }
        }
      },
      "gateway": {
        "mode": "local",
        "auth": { "mode": "none" }
      }
    }
    ```
    
3.  **保存并应用**
    
    先单击 **Save** 按钮将配置写入磁盘，再单击 **Apply** 按钮重启网关使配置生效。
    

## 接入消息渠道

### 钉钉

#### 步骤一：创建钉钉应用并获取凭证

1.  **选择或创建组织**
    
    1.  登录[钉钉开放平台](https://open-dev.dingtalk.com/)，选择您有开发者权限的组织，或者选择某个组织后，[获取开发者权限](https://open.dingtalk.com/document/orgapp/obtain-developer-permissions)。
        
    2.  如果没有开发者权限，请直接创建一个组织。使用移动端钉钉扫描下方二维码，可快速完成创建。
        
2.  **创建钉钉机器人应用**
    
    1.  登录[钉钉开放平台](https://open-dev.dingtalk.com/)，在顶部菜单栏，选择**应用开发**。
        
    2.  在页面右侧，单击**创建应用**，填写应用名称（例如"AI 助手"）和描述，然后单击**保存**，系统自动进入应用详情页。
        
    3.  在应用详情的**添加应用能力**页面，选择添加**机器人**。
        
    4.  配置机器人：
        
        -   开启**机器人配置**开关。
            
        -   填写机器人名称等必填项。
            
        -   **消息接收模式** 采用默认的 **Stream 模式**。
            
        -   单击**发布**。
            
3.  **获取应用凭证**
    
    在左侧导航栏，单击**凭证与基础信息**，获取Client ID和Client Secret。后续部署时使用。
    
4.  **发布应用**
    
    1.  在应用详情的左侧导航栏，单击**版本管理与发布**。
        
    2.  在页面右侧，单击**创建新版本**，填写版本号（例如 1.0.0）。
        
    3.  设置可见范围，例如**仅我可见**。
        
    4.  单击**保存**，然后确认发布。
        

#### 步骤二：安装钉钉渠道插件

**说明**

如果使用[轻量应用服务器部署方案](https://help.aliyun.com/zh/simple-application-server/use-cases/quickly-deploy-and-use-openclaw)或[无影云电脑部署方案](https://help.aliyun.com/zh/edsp/getting-started/quickly-create-openclaw-through-wuying-cloud-computer-personal-edition/)部署 OpenClaw，通常已经内置插件，无需手动安装。

1.  在终端执行以下命令安装钉钉渠道插件
    
    ```
    openclaw plugins install @soimy/dingtalk
    ```
    
2.  安装完成后，执行以下命令确认插件已加载：
    
    ```
    openclaw plugins list
    ```
    
    输出中应该包含`dingtalk`插件且状态为 `loaded`。
    

#### 步骤三：配置钉钉渠道

**说明**

如果使用[轻量应用服务器部署方案](https://help.aliyun.com/zh/simple-application-server/use-cases/quickly-deploy-and-use-openclaw)或[无影云电脑部署方案](https://help.aliyun.com/zh/edsp/getting-started/quickly-create-openclaw-through-wuying-cloud-computer-personal-edition/)部署 OpenClaw，通常可以通过图形化界面进行配置，无需手动修改配置文件。

在 `~/.openclaw/openclaw.json` 中添加 `channels` 和 `plugins.allow` 配置。将 `YOUR_DINGTALK_APPKEY` 和 `YOUR_DINGTALK_APPSECRET` 替换为[步骤一](#oc-channel-dingtalk-step1)中获取的凭证。请将 `channels` 和 `plugins` 添加到已有配置文件的对应位置，不要覆盖已有的 `models`、`agents` 等配置。

**说明**

如果使用轻量应用服务器或无影云电脑部署 OpenClaw，通常可以通过图形化界面进行配置，无需手动修改配置文件，具体请参见对应产品的文档。

```
{
  "channels": {
    "dingtalk": {
      "enabled": true,
      "clientId": "YOUR_DINGTALK_APPKEY",
      "clientSecret": "YOUR_DINGTALK_APPSECRET",
      "robotCode": "YOUR_DINGTALK_APPKEY",
      "dmPolicy": "open",
      "groupPolicy": "open",
      "messageType": "markdown"
    }
  },
  "plugins": {
    "allow": ["dingtalk"],
    "entries": {
      "dingtalk": {
        "enabled": true
      }
    }
  }
}
```

以上配置中 `dmPolicy` 和 `groupPolicy` 均设为 `open`，适用于测试或个人使用场景。生产环境中建议设为 `allowlist`，通过白名单限制可访问的用户和群组，降低安全风险。

#### 步骤四：测试

1.  执行以下命令重启网关。
    
    ```
    openclaw gateway restart
    ```
    
2.  执行以下命令检查钉钉渠道状态
    
    ```
    openclaw status
    ```
    
    在 Channels 部分，DingTalk 应显示为 `ON` 且状态为 `OK - configured`。
    
3.  在钉钉群聊中找到机器人，发送消息进行测试。
    

### 飞书

#### 步骤一：创建飞书应用

1.  访问[飞书开放平台](https://open.feishu.cn/app)，单击**创建企业自建应用**，填写应用名称和描述，选择应用图标，单击**创建**。
    
2.  左侧导航栏单击**凭证与基础信息** 页面，复制**App ID**（格式如 `cli_xxx`）和**App Secret**。
    
3.  左侧导航栏单击 **权限管理** 页面，单击**批量导入/导出权限** 按钮，粘贴以下 JSON 配置，单击**下一步，确认新增权限**，单击**申请开通**。
    
    **JSON配置文件内容**
    
    ```
    {
      "scopes": {
        "tenant": [
          "aily:file:read",
          "aily:file:write",
          "application:application.app_message_stats.overview:readonly",
          "application:application:self_manage",
          "application:bot.menu:write",
          "cardkit:card:write",
          "contact:user.employee_id:readonly",
          "corehr:file:download",
          "docs:document.content:read",
          "event:ip_list",
          "im:chat",
          "im:chat.access_event.bot_p2p_chat:read",
          "im:chat.members:bot_access",
          "im:message",
          "im:message.group_at_msg:readonly",
          "im:message.group_msg",
          "im:message.p2p_msg:readonly",
          "im:message:readonly",
          "im:message:send_as_bot",
          "im:resource",
          "sheets:spreadsheet",
          "wiki:wiki:readonly"
        ],
        "user": ["aily:file:read", "aily:file:write", "im:chat.access_event.bot_p2p_chat:read"]
      }
    }
    ```
    
4.  左侧导航栏中单击， 选择**按能力添加**页签，找到**机器人**卡片，单击**配置**。
    
5.  配置事件订阅。
    
    1.  在飞书开放平台左侧导航栏单击**事件与回调**，在**事件配置**页签中单击**订阅方式**，选择**使用 长连接 接收事件**，单击**保存**。
        
    2.  在事件配置页面，单击**添加事件**，搜索事件`im.message.receive_v1`（接收消息），单击**确认添加**。
        
6.  在 **版本管理与发布** 页面创建版本，填写**应用版本号**和**更新说明**，单击**保存**，提交审核并发布。
    

#### 步骤二：配置飞书机器人

1.  在终端中输入以下命令配置飞书渠道
    
    ```
    openclaw channels add
    ```
    
    根据界面交互提示，完成以下配置。
    
    -   选择 **Feishu**
        
    -   输入 **App ID**
        
    -   输入 **App Secret**
        
    
    配置完成后，重启网关。
    
2.  创建群聊或在已有群聊中添加机器人，在飞书群中**@机器人**进行对话，或通过搜索的方式与机器人私聊进行测试。
    
3.  在群聊中添加机器人：**设置**。
    
4.  单击机器人头像，单击发送消息，可向机器人私发一条消息，机器人会回复一条包含**配对码**的消息。
    
5.  复制消息的最后一行，在 OpenClaw 对话中发送，OpenClaw 会自动完成飞书机器人配对。
    

#### 步骤三：测试

1.  执行以下命令重启网关。
    
    ```
    openclaw gateway restart
    ```
    
2.  执行以下命令检查飞书渠道状态
    
    ```
    openclaw status
    ```
    
    在 Channels 部分，Feishu 应显示为 `ON` 且状态为 `OK`。
    
3.  在飞书中发送消息进行测试。
    

### 微信

**说明**

请确保微信版本不低于 8.0.70。

#### 步骤一：安装微信渠道插件

1.  在终端中执行以下命令安装微信渠道插件。
    
    ```
    npx -y @tencent-weixin/openclaw-weixin-cli@latest install
    ```
    
2.  安装完成后，终端会显示一个二维码，使用微信扫描该二维码完成身份绑定。绑定成功后，微信会自动弹出 ClawBot 的聊天页面。
    
3.  安装完成后，执行以下命令确认插件已加载：
    
    ```
    openclaw plugins list
    ```
    
    输出中应包含 `openclaw-weixin` 插件且状态为 `loaded`。
    

#### 步骤二：测试

1.  执行以下命令重启网关。
    
    ```
    openclaw gateway restart
    ```
    
2.  在微信中找到 ClawBot，发送消息进行测试。
    

### QQ

#### 步骤一：安装 QQ 渠道插件

1.  在终端中执行以下命令安装 QQ 渠道插件：
    
    ```
    openclaw plugins install @sliverp/qqbot
    ```
    
2.  安装完成后，执行以下命令确认插件已加载：
    
    ```
    openclaw plugins list
    ```
    
    输出中应该包含`qqbot`插件且状态为`loaded` 。
    

#### 步骤二：创建 QQ 机器人

1.  访问[QQ 开放平台](https://q.qq.com/#/)，注册并登录开发者账号。
    
2.  在[OpenClaw 专属页面](https://q.qq.com/qqbot/openclaw/index.html)创建机器人，并获取 AppID 和 AppSecret。
    
    **说明**
    
    AppSecret 不支持明文保存，二次查看将会强制重置，请自行妥善保存。
    
3.  创建完毕后，QQ 会自动弹出机器人聊天页面。
    

#### 步骤三：接入 QQ 消息渠道

1.  在 `~/.openclaw/openclaw.json` 中添加 `channels` 和 `plugins.allow` 配置。将 `YOUR_APP_ID` 和 `YOUR_APP_SECRET` 替换为[步骤二](#oc-channel-qq-step2)中获取的凭证。请将 `channels` 和 `plugins` 添加到已有配置文件的对应位置，不要覆盖已有的 `models`、`agents` 等配置。
    
    ```
    {
      "channels": {
        "qqbot": {
          "enabled": true,
          "appId": "YOUR_APP_ID",
          "clientSecret": "YOUR_APP_SECRET",
          "dmPolicy": "open",
          "allowFrom": ["*"]
        }
      },
      "plugins": {
        "allow": ["qqbot"],
        "entries": {
          "qqbot": {
            "enabled": true,
            "config": {}
          }
        }
      }
    }
    ```
    
    以上配置中`dmPolicy`设为`open`表示允许私聊，`allowFrom`设为`["*"]`表示允许所有用户消息，适用于测试或个人使用场景，生产环境中建议根据实际需求限制访问范围。
    
2.  配置完成后重启网关。
    
    ```
    openclaw gateway restart
    ```
    
3.  在 QQ 中向机器人发送消息进行测试。
    

## 常见命令

**命令**

**说明**

**示例**

/help

显示可用命令的快速摘要。

/help

/status

查看当前模型、会话、网关等状态信息。

/status

/model <模型名称>

切换当前会话使用的模型。

/model qwen3.7-max

/new

开始一个新会话。

/new

/compact

压缩对话历史，释放上下文窗口空间。

/compact

/think <级别>

设置思考（推理）深度级别，可选 off、low、medium、high 等。

/think high

/skills

展示全部可用的 Skill。

/skills

## 使用案例

### 案例一：定时推送 AI 新闻

通过 OpenClaw 的 Cron 定时任务功能，可以让 AI 每天定时抓取指定网站的新闻并通过钉钉推送给您，无需额外安装任何 Skill 或插件。

**配置步骤**

1.  完成[钉钉接入](#oc-channel-dingtalk)。
    
2.  在终端执行以下命令：
    
    ```
    openclaw cron add \
      --name "ai-daily-news" \
      --cron "0 9 * * *" \
      --tz "Asia/Shanghai" \
      --message "请访问 https://www.aibase.com/zh/daily 获取今天的AI日报，总结前10条最重要的AI新闻，用简洁的中文列表形式输出，每条包含标题和一句话摘要" \
      --channel dingtalk \
      --announce \
      --timeout-seconds 120
    ```
    
    参数说明如下：
    
    **参数**
    
    **说明**
    
    `--name`
    
    任务名称
    
    `--cron`
    
    Cron 表达式，`"0 9 * * *"` 表示每天 9:00 执行
    
    `--tz`
    
    时区，设为 `"Asia/Shanghai"` 即北京时间
    
    `--message`
    
    发送给 Agent 的提示词，告诉 AI 要抓取什么内容、如何总结
    
    `--channel`
    
    推送通道，设为 `dingtalk`
    
    `--announce`
    
    将结果推送到钉钉对话中
    
    `--timeout-seconds`
    
    任务超时时间（秒），网页抓取建议设为 120
    
    创建成功后将返回 JSON 格式的任务信息，包含任务 ID 和下次执行时间。
    
3.  创建任务后，可以立即手动触发一次以验证效果。
    
    1.  查看任务列表，获取任务 ID。
        
        ```
        openclaw cron list
        ```
        
    2.  手动触发执行。
        
        ```
        openclaw cron run <任务ID> --timeout 120000
        ```
        
    3.  查看执行结果。
        
        ```
        openclaw cron runs --id <任务ID>
        ```
        
        当输出中 `"status": "ok"` 且 `"delivered": true` 时，表示新闻已成功推送到钉钉。
        

### 案例二：更多定时推送模板

**arXiv 最新论文推送**

示例：每周一早上九点推送`agent+evaluation`相关的最新论文。

```
openclaw cron add \
  --name "paper-digest" \
  --cron "0 9 * * 1" \
  --tz "Asia/Shanghai" \
  --message '请使用 curl 命令执行以下请求获取论文数据：
curl -s "http://export.arxiv.org/api/query?search_query=all:%22agent+evaluation%22&start=0&max_results=5&sortBy=submittedDate&sortOrder=descending"
解析返回的 XML 数据，列出前5篇论文，每篇包含：
1. 标题
2. 发布日期
3. 摘要总结（用中文，2-3句话概括核心贡献）
4. arXiv链接
5. 如果XML中包含GitHub代码链接也列出
按发布时间从新到旧排列。' \
  --channel dingtalk \
  --announce \
  --timeout-seconds 120
```

**HuggingFace 热门模型推送**

示例：每周一早上九点推送 HuggingFace 上最近热门的大语言模型。

```
openclaw cron add \
  --name "hf-trending-models" \
  --cron "0 9 * * 1" \
  --tz "Asia/Shanghai" \
  --message '请使用 curl 命令执行以下请求获取 HuggingFace 上最近热门的大语言模型：
curl -s "https://hf-mirror.com/api/models?sort=trendingScore&direction=-1&limit=10&pipeline_tag=text-generation"
解析返回的 JSON 数据，列出前10个模型，每个包含：
1. 模型名称
2. 发布日期
3. 下载量和点赞数
4. 模型页面链接（格式为 https://huggingface.co/<模型id>）
重点标注最近一个月内新发布的模型，并用中文简要说明每个模型的特点（如参数量、所属机构等）。' \
  --channel dingtalk \
  --announce \
  --timeout-seconds 120
```

**Github 热门项目推送**

示例：每周一早上九点推送 Github 上新创建的热门项目。

```
openclaw cron add \
    --name "github-trending" \
    --cron "0 9 * * 1" \
    --tz "Asia/Shanghai" \
    --message '请获取过去一周内 GitHub 上新创建的热门项目（按 Star
  数排序前10），每个项目列出名称、Star
  数、简介（中文翻译）、编程语言和链接，重点标注 Star 数超过 1000
  的项目。请先用 date 命令计算7天前的日期，然后通过 GitHub Search API 的
  created 参数筛选。' \
    --channel dingtalk \
    --announce \
    --timeout-seconds 120
```

### 案例三：小红书自动运营

通过 OpenClaw 可自动化运营小红书账号，提供内容创作、自动发布、评论回复等全链路运营能力。

**配置步骤**

1.  **安装**[**小红书 Skill**](https://github.com/Xiangyu-CAS/xiaohongshu-ops-skill)
    
    在 OpenClaw 对话中输入以下指令，自动完成安装。
    
    ```
    帮我安装这个skill，`https://github.com/Xiangyu-CAS/xiaohongshu-ops-skill`
    ```
    
2.  安装完成后，返回终端并重启网关使 Skill 生效。
    
    ```
    openclaw gateway restart
    ```
    
3.  验证 Skill 是否安装成功。
    
    ```
    openclaw skills list
    ```
    
4.  首次使用需登录小红书，后续无需重复验证。在 OpenClaw 对话中输入`登录小红书`，按照提示完成扫码登录即可。
    

**示例 1：首页分析**

输入`帮我分析一下小红书首页推荐流`，OpenClaw 会分析首页推荐内容，提炼可复用的选题方向和标题模式。

**示例 2：自动发布笔记**

输入`帮我发布一篇关于AI工具使用技巧的小红书笔记`，OpenClaw 会自动生成封面、填写标题和正文，并完成发布。

**示例 3：自动回复评论**

输入`帮我检查小红书最新评论并回复`，OpenClaw 会自动检查通知中的新评论，根据账号人设逐条回复。

### 案例四：股市监控与分析

让 OpenClaw 分析股票走势，并提供技术面分析和投资建议。

**说明**

**AI 生成内容仅供参考，不构成实际的投资建议或决策依据。**

**配置步骤**

1.  **安装 ClawHub CLI**
    
    ```
    npm install -g clawhub
    ```
    
2.  **安装 Skill**
    
    在 OpenClaw 对话中输入以下指令，OpenClaw 会自动完成安装：
    
    ```
    帮我安装 china-stock-analysis 这个 skill
    ```
    
3.  安装完成后，返回终端并重启网关使 Skill 生效。
    
    ```
    openclaw gateway restart
    ```
    
    验证 Skill 是否安装成功。
    
    ```
    openclaw skills list
    ```
    
4.  在 OpenClaw 对话中输入股市相关问题，例如`分析贵州茅台的股价`。
    

## 了解更多

### Skill

Skill 是可扩展的能力模块，Agent 会根据请求自动匹配并加载对应的 Skill。OpenClaw 支持查看和启用内置 Skill，从 [ClawHub](https://clawhub.com/)安装社区 Skill，或创建自定义 Skill。

#### **查看已有 Skill**

1.  执行以下命令查看已安装的 Skill 及其状态。
    
    ```
    # 列出已安装的 Skill
    openclaw skills list
    
    # 查看 Skill 状态（已启用、已禁用、缺少依赖等）
    openclaw skills check
    
    # 查看特定 Skill 的详细信息
    openclaw skills info <skill-name>
    ```
    
2.  内置 Skill 默认未启用，需在 `~/.openclaw/openclaw.json` 中通过 `skills.allowBundled` 白名单启用，只有列在其中的内置 Skill 才会被加载。
    
    ```
    {
      "skills": {
        "allowBundled": [
          "github",
          "weather",
          "summarize",
          "coding-agent",
          "clawhub",
          "nano-pdf",
          "google-web-search",
          "image-lab"
        ]
      }
    }
    ```
    
    部分内置 Skill需要配置对应的第三方 API Key 才能使用，请在 `~/.openclaw/openclaw.json` 的 `skills.entries` 中配置，具体请参考 [Skills 配置文档](https://docs.openclaw.ai/zh-CN/tools/skills-config)。
    

#### **查找更多 Skill**

可以通过以下两种方式查找并安装更多 Skill。

1.  **通过 ClawHub 搜索安装**
    
    [ClawHub](https://clawhub.com/) 提供 3,000+ 个社区 Skill，可以在网站上浏览，也可以通过命令行搜索。
    
    ```
    # 按关键词搜索
    npx clawhub search [关键词]
    
    # 浏览最近更新的 Skill
    npx clawhub explore
    ```
    
    找到合适的 Skill 后，执行以下命令安装，安装完成后重启网关即可使用。
    
    ```
    npx clawhub install <skill-name>
    ```
    
2.  **直接在 OpenClaw 中提问**
    
    在对话中直接描述需求，例如`帮我找一个可以查天气的 Skill`，OpenClaw 会自动搜索并安装。
    

#### 创建自定义 Skill

1.  创建 Skill 目录。
    
    ```
    mkdir -p ~/.openclaw/workspace/skills/my-custom-skill
    ```
    
2.  在该目录下创建 `SKILL.md` 文件。文件由 YAML 前置元数据和 Markdown 指令两部分组成，其中 `name` 和 `description` 为必填字段。Agent 根据 `description` 判断是否加载该 Skill，请确保描述准确。
    
    ```
    ---
    name: my-custom-skill
    description: 简短描述
    ---
    
    # My Custom Skill
    
    当用户请求 XXX 时，执行以下操作：
    
    1. 使用 bash 工具运行 xxx 命令
    2. 解析输出结果
    3. 以表格形式返回给用户
    ```
    
3.  重启网关使 Skill 生效。
    
    ```
    # 重启网关
    openclaw gateway restart
    
    # 查看 Skill 是否生效
    openclaw skills list
    ```
    

更多 Skill 配置说明请参考[OpenClaw 官方文档](https://docs.openclaw.ai/tools/creating-skills)。

### 接入 MCP 服务

OpenClaw 支持通过 MCP（Model Context Protocol）插件扩展 Agent 的工具调用能力，例如联网搜索、网页抓取等。具体案例可以参考[添加联网搜索MCP](https://help.aliyun.com/zh/model-studio/web-search-for-coding-plan)。

## 常见问题

如何查看已配置的模型？

在终端输入`openclaw tui`，进入 OpenClaw 终端命令行，接着输入`/model`查看模型列表。按回车键选中模型，按Esc键退出模型列表。

为什么报错"HTTP 401: Incorrect API key provided."或"No API key found for provider xxx"？

可能原因：

1.  API Key 无效、过期、为空、格式错误，或与端点环境不匹配。请检查 API Key 是否与所使用的付费方式匹配，并确保复制完整且无空格；确认订阅状态有效。
    
2.  OpenClaw 的历史配置缓存导致配置错误，请删除`~/.openclaw/agents/main/agent/models.json`文件中的`providers`配置项，并重启 OpenClaw。
    

我已经配置过钉钉等其他渠道，如何安全地添加新套餐模型（防止原有配置丢失）？

-   **请勿直接全量覆盖**。直接"全部替换"会覆盖掉自定义配置，请进行**局部修改**。
    
-   可以选择以下方式完成配置：
    
    -   **若 OpenClaw 可正常对话**：直接在 OpenClaw 对话中输入指令完成配置合并。
        
    -   **若 OpenClaw 未配置模型或无法对话**：请手动编辑 `~/.openclaw/openclaw.json`，只修改需要变更的字段，保留原有配置不变。
        

重启网关后，已有会话可能无法正常对话，请重启会话。

报错 device identity required 怎么办？

详细报错信息：

```
http://127.0.0.1:18791/15:05:56 [ws] closed before connect conn=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx remote=127.0.0.1 fwd=n/a origin=n/a host=127.0.0.1:18789 ua=n/a code=1008 reason=device identity required
```

**原因：**

客户端连接网关时未提供设备身份信息，通常由以下原因导致：

-   首次打开浏览器访问地址，尚未完成设备配对。
    
-   浏览器缓存被清除，设备密钥丢失。
    
-   重装或升级 OpenClaw 后，`~/.openclaw/identity/` 目录下的密钥文件缺失。
    

**解决方法：**

在终端执行以下命令，允许当前设备连接并重新生成浏览器访问地址：

```
openclaw devices approve --latest
openclaw dashboard --no-open
```

如果仍未解决，先清除异常的设备记录再重试：

```
openclaw devices clear --pending --yes
openclaw dashboard --no-open
```

执行 `openclaw devices list`，确认设备显示在 Paired 列表中即为正常。
