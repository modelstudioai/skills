# OpenCode

OpenCode 是一款终端 AI 编程工具，可以通过按量计费、Coding Plan 或 Token Plan 团队版接入阿里云百炼。

## **安装 OpenCode**

1.  安装 [Node.js](https://nodejs.org/en/download/)（v18.0 或更高版本）。
    
2.  在终端中执行以下命令安装 OpenCode：
    
    ```
    npm install -g opencode-ai
    ```
    
    运行以下命令验证安装。若有版本号输出，则表示安装成功。
    
    ```
    opencode -v
    ```
    

## **配置接入凭证**

使用文本编辑器打开：

-   macOS / Linux：`~/.config/opencode/opencode.json`
    
-   Windows：`C:\Users\<用户名>\.config\opencode\opencode.json`
    

根据所选方案写入对应配置：

-   **Token Plan 团队版**：按坐席订阅，按 token 消耗抵扣 Credits。
    
-   **Coding Plan**：固定月费订阅，按模型调用次数计量。
    
-   **按量计费**：按实际调用量后付费。
    

### Token Plan 团队版

需先购买 Token Plan 团队版套餐且套餐处于有效期内。可在[Token Plan 团队版页面](https://bailian.console.aliyun.com/?tab=plan#/efm/subscription/overview)购买套餐。

将 `YOUR_API_KEY` 替换为 Token Plan 团队版专属 [API Key](https://bailian.console.aliyun.com/?tab=plan#/efm/subscription/overview)。可用模型请参考 Token Plan 团队版[支持的模型](https://help.aliyun.com/zh/model-studio/token-plan-overview)。

```
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "bailian-token-plan": {
      "npm": "@ai-sdk/anthropic",
      "name": "Alibaba Cloud Model Studio",
      "options": {
        "baseURL": "https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic/v1",
        "apiKey": "YOUR_API_KEY"
      },
      "models": {
        "qwen3.7-max": {
          "name": "Qwen3.7 Max",
          "options": {
            "thinking": {
              "type": "enabled",
              "budgetTokens": 8192
            }
          }
        },
        "qwen3.6-plus": {
          "name": "Qwen3.6 Plus",
          "options": {
            "thinking": {
              "type": "enabled",
              "budgetTokens": 8192
            }
          }
        },
        "qwen3.6-flash": {
          "name": "Qwen3.6 Flash",
          "options": {
            "thinking": {
              "type": "enabled",
              "budgetTokens": 8192
            }
          }
        },
        "deepseek-v4-pro": {
          "name": "DeepSeek V4 Pro"
        },
        "deepseek-v4-flash": {
          "name": "DeepSeek V4 Flash"
        },
        "deepseek-v3.2": {
          "name": "DeepSeek V3.2"
        },
        "kimi-k2.6": {
          "name": "Kimi K2.6",
          "options": {
            "thinking": {
              "type": "enabled",
              "budgetTokens": 8192
            }
          }
        },
        "kimi-k2.5": {
          "name": "Kimi K2.5",
          "options": {
            "thinking": {
              "type": "enabled",
              "budgetTokens": 8192
            }
          }
        },
        "glm-5.1": {
          "name": "GLM-5.1",
          "options": {
            "thinking": {
              "type": "enabled",
              "budgetTokens": 8192
            }
          }
        },
        "glm-5": {
          "name": "GLM-5",
          "options": {
            "thinking": {
              "type": "enabled",
              "budgetTokens": 8192
            }
          }
        },
        "MiniMax-M2.5": {
          "name": "MiniMax M2.5"
        }
      }
    }
  }
}
```

### Coding Plan

将 `YOUR_API_KEY` 替换为 Coding Plan 专属 [API Key](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/coding_plan)。可用模型请参考 Coding Plan [支持的模型](https://help.aliyun.com/zh/model-studio/coding-plan)。

```
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "bailian-coding-plan": {
      "npm": "@ai-sdk/anthropic",
      "name": "Alibaba Cloud Model Studio",
      "options": {
        "baseURL": "https://coding.dashscope.aliyuncs.com/apps/anthropic/v1",
        "apiKey": "YOUR_API_KEY"
      },
      "models": {
        "qwen3.6-plus": {
          "name": "Qwen3.6 Plus",
          "options": {
            "thinking": {
              "type": "enabled",
              "budgetTokens": 1024
            }
          }
        },
        "qwen3.5-plus": {
          "name": "Qwen3.5 Plus",
          "options": {
            "thinking": {
              "type": "enabled",
              "budgetTokens": 1024
            }
          }
        },
        "qwen3-max-2026-01-23": {
          "name": "Qwen3 Max 0123"
        },
        "qwen3-coder-next": {
          "name": "Qwen3 Coder Next"
        },
        "qwen3-coder-plus": {
          "name": "Qwen3 Coder Plus"
        },
        "MiniMax-M2.5": {
          "name": "MiniMax M2.5"
        },
        "glm-5": {
          "name": "GLM-5",
          "options": {
            "thinking": {
              "type": "enabled",
              "budgetTokens": 1024
            }
          }
        },
        "glm-4.7": {
          "name": "GLM-4.7"
        },
        "kimi-k2.5": {
          "name": "Kimi K2.5",
          "options": {
            "thinking": {
              "type": "enabled",
              "budgetTokens": 1024
            }
          }
        }
      }
    }
  }
}
```

### 按量计费

将 `YOUR_API_KEY` 替换为[阿里云百炼 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。可用模型请参考[Anthropic 兼容 API](https://help.aliyun.com/zh/model-studio/anthropic-api-messages#07833dedefft7)。

```
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "bailian-payg": {
      "npm": "@ai-sdk/anthropic",
      "name": "Alibaba Cloud Model Studio",
      "options": {
        "baseURL": "https://dashscope.aliyuncs.com/apps/anthropic/v1",
        "apiKey": "YOUR_API_KEY"
      },
      "models": {
        "qwen3.7-max": {
          "name": "Qwen3.7 Max",
          "options": {
            "thinking": {
              "type": "enabled",
              "budgetTokens": 8192
            }
          }
        },
        "qwen3.6-plus": {
          "name": "Qwen3.6 Plus",
          "options": {
            "thinking": {
              "type": "enabled",
              "budgetTokens": 8192
            }
          }
        },
        "deepseek-v3.2": {
          "name": "DeepSeek V3.2"
        }
      }
    }
  }
}
```

## **验证配置**

保存配置后，重启 OpenCode，输入 `/models`，搜索 `Alibaba Cloud Model Studio`，选择需要使用的模型即可开始对话。

## **常见问题**

### 错误码

配置过程中遇到报错，请参考对应计费方案的常见问题文档：

-   按量付费：[Anthropic API 兼容 - 错误码](https://help.aliyun.com/zh/model-studio/anthropic-api-messages#7d8d58d0736zv)
    
-   Coding Plan：[Coding Plan 常见问题](https://help.aliyun.com/zh/model-studio/coding-plan-faq)
    
-   Token Plan 团队版：[Token Plan 团队版常见问题](https://help.aliyun.com/zh/model-studio/token-plan-faq)
