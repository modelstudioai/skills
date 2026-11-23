# OpenClaw

在 OpenClaw 中使用阿里云百炼模型。

## 快速开始

1.  1
    
    安装 Qwen 插件
    
    ```
    openclaw plugins install @openclaw/qwen-provider
    ```
    
    **说明**无法安装插件时，参考[通过配置文件接入](#5843746f3452j)。
    
2.  2
    
    获取 API Key
    
    #### Token Plan
    
    按 Token Plan 版本获取 API Key：
    
    -   Token Plan 个人版：[创建或查看 API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan/personal)
    -   Token Plan 团队版：[分配坐席并获取 API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/uac-admin/organization/members/list)
    
    #### 按量计费
    
    从 [百炼 API Key 页面](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key?spm=5176.28197581.0.0.307f29a4lC7Vbh) 获取百炼 API Key。
    
    #### Coding Plan
    
    从 [Coding Plan 页面](https://bailian.console.aliyun.com/cn-beijing/subscription/coding-plan) 获取 Coding Plan API Key。
    
3.  3
    
    配置模型
    
    按计费方案运行对应命令，并按提示输入 API Key。
    
    #### Token Plan
    
    ```
    openclaw onboard --auth-choice qwen-token-plan-cn
    ```
    
    #### 按量计费
    
    ```
    openclaw onboard --auth-choice qwen-standard-api-key-cn
    ```
    
    #### Coding Plan
    
    ```
    openclaw onboard --auth-choice qwen-api-key-cn
    ```
    
4.  4
    
    验证
    
    运行以下命令确认模型列表和调用结果：
    
    ```
    openclaw models list --provider qwen-token-plan
    openclaw agent --model qwen-token-plan/qwen3.8-max --message "只回复 ok"
    ```
    

## 通过配置文件接入

适用于无法安装 Qwen 插件或需要手动管理配置的场景。

1.  1
    
    打开或新建配置文件
    
    `~/.openclaw/openclaw.json`
    
    只更新 `models`、`agents` 和 `gateway` 中对应字段，不要全量替换已有配置。
    
2.  2
    
    写入配置
    
    #### Token Plan 个人版
    
    将 `YOUR_API_KEY` 替换为 Token Plan 个人版 API Key。
    
    ```
    {
      "models": {
        "mode": "merge",
        "providers": {
          "bailian-token-plan": {
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic",
            "apiKey": "YOUR_API_KEY",
            "api": "anthropic-messages",
            "models": [
              {
                "id": "auto",
                "name": "auto",
                "reasoning": false,
                "input": [
                  "text"
                ],
                "contextWindow": 1000000,
                "maxTokens": 393216,
                "cost": {
                  "input": 0,
                  "output": 0,
                  "cacheRead": 0,
                  "cacheWrite": 0
                }
              },
              {
                "id": "qwen4-max-preview",
                "name": "qwen4-max-preview",
                "reasoning": true,
                "input": [
                  "text",
                  "image"
                ],
                "contextWindow": 1000000,
                "maxTokens": 131072,
                "cost": {
                  "input": 0,
                  "output": 0,
                  "cacheRead": 0,
                  "cacheWrite": 0
                }
              },
              {
                "id": "qwen4-max",
                "name": "qwen4-max",
                "reasoning": true,
                "input": [
                  "text",
                  "image"
                ],
                "contextWindow": 1000000,
                "maxTokens": 262144,
                "cost": {
                  "input": 0,
                  "output": 0,
                  "cacheRead": 0,
                  "cacheWrite": 0
                }
              },
              {
                "id": "qwen3.8-max",
                "name": "qwen3.8-max",
                "reasoning": true,
                "input": [
                  "text",
                  "image"
                ],
                "contextWindow": 1000000,
                "maxTokens": 131072,
                "cost": {
                  "input": 0,
                  "output": 0,
                  "cacheRead": 0,
                  "cacheWrite": 0
                }
              },
              {
                "id": "qwen3.8-flash",
                "name": "qwen3.8-flash",
                "reasoning": true,
                "input": [
                  "text",
                  "image"
                ],
                "contextWindow": 1000000,
                "maxTokens": 131072,
                "cost": {
                  "input": 0,
                  "output": 0,
                  "cacheRead": 0,
                  "cacheWrite": 0
                }
              },
              {
                "id": "qwen3.7-max",
                "name": "qwen3.7-max",
                "reasoning": true,
                "input": [
                  "text"
                ],
                "contextWindow": 1000000,
                "maxTokens": 65536,
                "cost": {
                  "input": 0,
                  "output": 0,
                  "cacheRead": 0,
                  "cacheWrite": 0
                }
              },
              {
                "id": "qwen3.7-plus",
                "name": "qwen3.7-plus",
                "reasoning": true,
                "input": [
                  "text",
                  "image"
                ],
                "contextWindow": 1000000,
                "maxTokens": 65536,
                "cost": {
                  "input": 0,
                  "output": 0,
                  "cacheRead": 0,
                  "cacheWrite": 0
                }
              },
              {
                "id": "qwen3.6-flash",
                "name": "qwen3.6-flash",
                "reasoning": true,
                "input": [
                  "text",
                  "image"
                ],
                "contextWindow": 1000000,
                "maxTokens": 65536,
                "cost": {
                  "input": 0,
                  "output": 0,
                  "cacheRead": 0,
                  "cacheWrite": 0
                }
              },
              {
                "id": "deepseek-v4.1-flash",
                "name": "deepseek-v4.1-flash",
                "reasoning": true,
                "input": [
                  "text",
                  "image"
                ],
                "contextWindow": 1000000,
                "maxTokens": 65536,
                "cost": {
                  "input": 0,
                  "output": 0,
                  "cacheRead": 0,
                  "cacheWrite": 0
                }
              },
              {
                "id": "deepseek-v4.1-flash-1017",
                "name": "deepseek-v4.1-flash-1017",
                "reasoning": true,
                "input": [
                  "text",
                  "image"
                ],
                "contextWindow": 1000000,
                "maxTokens": 65536,
                "cost": {
                  "input": 0,
                  "output": 0,
                  "cacheRead": 0,
                  "cacheWrite": 0
                }
              },
              {
                "id": "deepseek-v4-pro",
                "name": "deepseek-v4-pro",
                "reasoning": true,
                "input": [
                  "text"
                ],
                "contextWindow": 1000000,
                "maxTokens": 65536,
                "cost": {
                  "input": 0,
                  "output": 0,
                  "cacheRead": 0,
                  "cacheWrite": 0
                }
              },
              {
                "id": "deepseek-v4-pro-0813",
                "name": "deepseek-v4-pro-0813",
                "reasoning": true,
                "input": [
                  "text"
                ],
                "contextWindow": 1000000,
                "maxTokens": 65536,
                "cost": {
                  "input": 0,
                  "output": 0,
                  "cacheRead": 0,
                  "cacheWrite": 0
                }
              },
              {
                "id": "deepseek-v4-flash-0731",
                "name": "deepseek-v4-flash-0731",
                "reasoning": true,
                "input": [
                  "text"
                ],
                "contextWindow": 1000000,
                "maxTokens": 65536,
                "cost": {
                  "input": 0,
                  "output": 0,
                  "cacheRead": 0,
                  "cacheWrite": 0
                }
              },
              {
                "id": "glm-5.3",
                "name": "glm-5.3",
                "reasoning": true,
                "input": [
                  "text"
                ],
                "contextWindow": 202752,
                "maxTokens": 16384,
                "cost": {
                  "input": 0,
                  "output": 0,
                  "cacheRead": 0,
                  "cacheWrite": 0
                }
              },
              {
                "id": "glm-5.2",
                "name": "glm-5.2",
                "reasoning": true,
                "input": [
                  "text"
                ],
                "contextWindow": 202752,
                "maxTokens": 16384,
                "cost": {
                  "input": 0,
                  "output": 0,
                  "cacheRead": 0,
                  "cacheWrite": 0
                }
              }
            ]
          }
        }
      },
      "agents": {
        "defaults": {
          "model": {
            "primary": "bailian-token-plan/auto"
          }
        }
      },
      "gateway": {
        "mode": "local",
        "auth": {
          "mode": "none"
        }
      }
    }
    ```
    
    #### Token Plan 团队版
    
    将 `YOUR_API_KEY` 替换为 Token Plan 团队版 API Key。
    
    ```
    {
      "models": {
        "mode": "merge",
        "providers": {
          "bailian-token-plan": {
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic",
            "apiKey": "YOUR_API_KEY",
            "api": "anthropic-messages",
            "models": [
              {
                "id": "auto",
                "name": "auto",
                "reasoning": false,
                "input": [
                  "text"
                ],
                "contextWindow": 1000000,
                "maxTokens": 393216,
                "cost": {
                  "input": 0,
                  "output": 0,
                  "cacheRead": 0,
                  "cacheWrite": 0
                }
              },
              {
                "id": "qwen4-max-preview",
                "name": "qwen4-max-preview",
                "reasoning": true,
                "input": [
                  "text",
                  "image"
                ],
                "contextWindow": 1000000,
                "maxTokens": 131072,
                "cost": {
                  "input": 0,
                  "output": 0,
                  "cacheRead": 0,
                  "cacheWrite": 0
                }
              },
              {
                "id": "qwen4-max",
                "name": "qwen4-max",
                "reasoning": true,
                "input": [
                  "text",
                  "image"
                ],
                "contextWindow": 1000000,
                "maxTokens": 262144,
                "cost": {
                  "input": 0,
                  "output": 0,
                  "cacheRead": 0,
                  "cacheWrite": 0
                }
              },
              {
                "id": "qwen3.8-max",
                "name": "qwen3.8-max",
                "reasoning": true,
                "input": [
                  "text",
                  "image"
                ],
                "contextWindow": 1000000,
                "maxTokens": 131072,
                "cost": {
                  "input": 0,
                  "output": 0,
                  "cacheRead": 0,
                  "cacheWrite": 0
                }
              },
              {
                "id": "qwen3.8-flash",
                "name": "qwen3.8-flash",
                "reasoning": true,
                "input": [
                  "text",
                  "image"
                ],
                "contextWindow": 1000000,
                "maxTokens": 131072,
                "cost": {
                  "input": 0,
                  "output": 0,
                  "cacheRead": 0,
                  "cacheWrite": 0
                }
              },
              {
                "id": "qwen3.7-max",
                "name": "qwen3.7-max",
                "reasoning": true,
                "input": [
                  "text"
                ],
                "contextWindow": 1000000,
                "maxTokens": 65536,
                "cost": {
                  "input": 0,
                  "output": 0,
                  "cacheRead": 0,
                  "cacheWrite": 0
                }
              },
              {
                "id": "qwen3.7-plus",
                "name": "qwen3.7-plus",
                "reasoning": true,
                "input": [
                  "text",
                  "image"
                ],
                "contextWindow": 1000000,
                "maxTokens": 65536,
                "cost": {
                  "input": 0,
                  "output": 0,
                  "cacheRead": 0,
                  "cacheWrite": 0
                }
              },
              {
                "id": "qwen3.6-plus",
                "name": "qwen3.6-plus",
                "reasoning": true,
                "input": [
                  "text",
                  "image"
                ],
                "contextWindow": 1000000,
                "maxTokens": 65536,
                "cost": {
                  "input": 0,
                  "output": 0,
                  "cacheRead": 0,
                  "cacheWrite": 0
                }
              },
              {
                "id": "qwen3.6-flash",
                "name": "qwen3.6-flash",
                "reasoning": true,
                "input": [
                  "text",
                  "image"
                ],
                "contextWindow": 1000000,
                "maxTokens": 65536,
                "cost": {
                  "input": 0,
                  "output": 0,
                  "cacheRead": 0,
                  "cacheWrite": 0
                }
              },
              {
                "id": "deepseek-v4.1-flash",
                "name": "deepseek-v4.1-flash",
                "reasoning": true,
                "input": [
                  "text",
                  "image"
                ],
                "contextWindow": 1000000,
                "maxTokens": 65536,
                "cost": {
                  "input": 0,
                  "output": 0,
                  "cacheRead": 0,
                  "cacheWrite": 0
                }
              },
              {
                "id": "deepseek-v4.1-flash-1017",
                "name": "deepseek-v4.1-flash-1017",
                "reasoning": true,
                "input": [
                  "text",
                  "image"
                ],
                "contextWindow": 1000000,
                "maxTokens": 65536,
                "cost": {
                  "input": 0,
                  "output": 0,
                  "cacheRead": 0,
                  "cacheWrite": 0
                }
              },
              {
                "id": "deepseek-v4-pro",
                "name": "deepseek-v4-pro",
                "reasoning": true,
                "input": [
                  "text"
                ],
                "contextWindow": 1000000,
                "maxTokens": 65536,
                "cost": {
                  "input": 0,
                  "output": 0,
                  "cacheRead": 0,
                  "cacheWrite": 0
                }
              },
              {
                "id": "deepseek-v4-pro-0813",
                "name": "deepseek-v4-pro-0813",
                "reasoning": true,
                "input": [
                  "text"
                ],
                "contextWindow": 1000000,
                "maxTokens": 65536,
                "cost": {
                  "input": 0,
                  "output": 0,
                  "cacheRead": 0,
                  "cacheWrite": 0
                }
              },
              {
                "id": "deepseek-v4-flash-0731",
                "name": "deepseek-v4-flash-0731",
                "reasoning": true,
                "input": [
                  "text"
                ],
                "contextWindow": 1000000,
                "maxTokens": 65536,
                "cost": {
                  "input": 0,
                  "output": 0,
                  "cacheRead": 0,
                  "cacheWrite": 0
                }
              },
              {
                "id": "kimi-k2.7-code",
                "name": "kimi-k2.7-code",
                "reasoning": true,
                "input": [
                  "text",
                  "image"
                ],
                "contextWindow": 262144,
                "maxTokens": 98304,
                "cost": {
                  "input": 0,
                  "output": 0,
                  "cacheRead": 0,
                  "cacheWrite": 0
                }
              },
              {
                "id": "kimi-k2.6",
                "name": "kimi-k2.6",
                "reasoning": true,
                "input": [
                  "text",
                  "image"
                ],
                "contextWindow": 262144,
                "maxTokens": 98304,
                "cost": {
                  "input": 0,
                  "output": 0,
                  "cacheRead": 0,
                  "cacheWrite": 0
                }
              },
              {
                "id": "kimi-k2.5",
                "name": "kimi-k2.5",
                "reasoning": true,
                "input": [
                  "text",
                  "image"
                ],
                "contextWindow": 262144,
                "maxTokens": 98304,
                "cost": {
                  "input": 0,
                  "output": 0,
                  "cacheRead": 0,
                  "cacheWrite": 0
                }
              },
              {
                "id": "glm-5.3",
                "name": "glm-5.3",
                "reasoning": true,
                "input": [
                  "text"
                ],
                "contextWindow": 202752,
                "maxTokens": 16384,
                "cost": {
                  "input": 0,
                  "output": 0,
                  "cacheRead": 0,
                  "cacheWrite": 0
                }
              },
              {
                "id": "glm-5.2",
                "name": "glm-5.2",
                "reasoning": true,
                "input": [
                  "text"
                ],
                "contextWindow": 202752,
                "maxTokens": 16384,
                "cost": {
                  "input": 0,
                  "output": 0,
                  "cacheRead": 0,
                  "cacheWrite": 0
                }
              },
              {
                "id": "glm-5.1",
                "name": "glm-5.1",
                "reasoning": true,
                "input": [
                  "text"
                ],
                "contextWindow": 202752,
                "maxTokens": 16384,
                "cost": {
                  "input": 0,
                  "output": 0,
                  "cacheRead": 0,
                  "cacheWrite": 0
                }
              },
              {
                "id": "glm-5",
                "name": "glm-5",
                "reasoning": true,
                "input": [
                  "text"
                ],
                "contextWindow": 202752,
                "maxTokens": 16384,
                "cost": {
                  "input": 0,
                  "output": 0,
                  "cacheRead": 0,
                  "cacheWrite": 0
                }
              },
              {
                "id": "MiniMax-M2.5",
                "name": "MiniMax-M2.5",
                "reasoning": true,
                "input": [
                  "text"
                ],
                "contextWindow": 196608,
                "maxTokens": 32768,
                "cost": {
                  "input": 0,
                  "output": 0,
                  "cacheRead": 0,
                  "cacheWrite": 0
                }
              }
            ]
          }
        }
      },
      "agents": {
        "defaults": {
          "model": {
            "primary": "bailian-token-plan/auto"
          }
        }
      },
      "gateway": {
        "mode": "local",
        "auth": {
          "mode": "none"
        }
      }
    }
    ```
    
    #### 按量计费
    
    将 `YOUR_API_KEY` 替换为百炼 API Key，并将 `{WorkspaceId}` 替换为 [Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。
    
    ```
    {
      "models": {
        "mode": "merge",
        "providers": {
          "bailian": {
            "baseUrl": "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic",
            "apiKey": "YOUR_API_KEY",
            "api": "anthropic-messages",
            "models": [
              {
                "id": "qwen3.8-max",
                "name": "qwen3.8-max",
                "reasoning": true,
                "input": [
                  "text",
                  "image"
                ],
                "contextWindow": 1000000,
                "maxTokens": 131072,
                "cost": {
                  "input": 0,
                  "output": 0,
                  "cacheRead": 0,
                  "cacheWrite": 0
                }
              },
              {
                "id": "qwen3.7-plus",
                "name": "qwen3.7-plus",
                "reasoning": true,
                "input": [
                  "text",
                  "image"
                ],
                "contextWindow": 1000000,
                "maxTokens": 65536,
                "cost": {
                  "input": 0,
                  "output": 0,
                  "cacheRead": 0,
                  "cacheWrite": 0
                }
              },
              {
                "id": "qwen3.8-flash",
                "name": "qwen3.8-flash",
                "reasoning": true,
                "input": [
                  "text",
                  "image"
                ],
                "contextWindow": 1000000,
                "maxTokens": 131072,
                "cost": {
                  "input": 0,
                  "output": 0,
                  "cacheRead": 0,
                  "cacheWrite": 0
                }
              },
              {
                "id": "deepseek-v4-pro-0813",
                "name": "deepseek-v4-pro-0813",
                "reasoning": true,
                "input": [
                  "text"
                ],
                "contextWindow": 1000000,
                "maxTokens": 65536,
                "cost": {
                  "input": 0,
                  "output": 0,
                  "cacheRead": 0,
                  "cacheWrite": 0
                }
              },
              {
                "id": "deepseek-v4.1-flash",
                "name": "deepseek-v4.1-flash",
                "reasoning": true,
                "input": [
                  "text",
                  "image"
                ],
                "contextWindow": 1000000,
                "maxTokens": 65536,
                "cost": {
                  "input": 0,
                  "output": 0,
                  "cacheRead": 0,
                  "cacheWrite": 0
                }
              }
            ]
          }
        }
      },
      "agents": {
        "defaults": {
          "model": {
            "primary": "bailian/qwen3.8-max"
          }
        }
      },
      "gateway": {
        "mode": "local",
        "auth": {
          "mode": "none"
        }
      }
    }
    ```
    
    #### Coding Plan
    
    将 `YOUR_API_KEY` 替换为 Coding Plan API Key。
    
    ```
    {
      "models": {
        "mode": "merge",
        "providers": {
          "bailian-coding": {
            "baseUrl": "https://coding.dashscope.aliyuncs.com/apps/anthropic",
            "apiKey": "YOUR_API_KEY",
            "api": "anthropic-messages",
            "models": [
              {
                "id": "qwen3.7-plus",
                "name": "qwen3.7-plus",
                "reasoning": true,
                "input": [
                  "text",
                  "image"
                ],
                "contextWindow": 1000000,
                "maxTokens": 65536,
                "cost": {
                  "input": 0,
                  "output": 0,
                  "cacheRead": 0,
                  "cacheWrite": 0
                }
              },
              {
                "id": "qwen3.6-plus",
                "name": "qwen3.6-plus",
                "reasoning": true,
                "input": [
                  "text",
                  "image"
                ],
                "contextWindow": 1000000,
                "maxTokens": 65536,
                "cost": {
                  "input": 0,
                  "output": 0,
                  "cacheRead": 0,
                  "cacheWrite": 0
                }
              },
              {
                "id": "kimi-k2.5",
                "name": "kimi-k2.5",
                "reasoning": true,
                "input": [
                  "text",
                  "image"
                ],
                "contextWindow": 262144,
                "maxTokens": 98304,
                "cost": {
                  "input": 0,
                  "output": 0,
                  "cacheRead": 0,
                  "cacheWrite": 0
                }
              },
              {
                "id": "glm-5",
                "name": "glm-5",
                "reasoning": true,
                "input": [
                  "text"
                ],
                "contextWindow": 202752,
                "maxTokens": 16384,
                "cost": {
                  "input": 0,
                  "output": 0,
                  "cacheRead": 0,
                  "cacheWrite": 0
                }
              },
              {
                "id": "MiniMax-M2.5",
                "name": "MiniMax-M2.5",
                "reasoning": true,
                "input": [
                  "text"
                ],
                "contextWindow": 196608,
                "maxTokens": 32768,
                "cost": {
                  "input": 0,
                  "output": 0,
                  "cacheRead": 0,
                  "cacheWrite": 0
                }
              },
              {
                "id": "qwen3.5-plus",
                "name": "qwen3.5-plus",
                "reasoning": false,
                "input": [
                  "text",
                  "image"
                ],
                "contextWindow": 1000000,
                "maxTokens": 65536,
                "cost": {
                  "input": 0,
                  "output": 0,
                  "cacheRead": 0,
                  "cacheWrite": 0
                }
              }
            ]
          }
        }
      },
      "agents": {
        "defaults": {
          "model": {
            "primary": "bailian-coding/qwen3.7-plus"
          }
        }
      },
      "gateway": {
        "mode": "local",
        "auth": {
          "mode": "none"
        }
      }
    }
    ```
    
    **说明**使用 qwen4-max-preview 时，可用 `params.cacheRetention` 设置 `short`、`long` 或 `none`，`long` 对应 1 小时 TTL。
    
    **说明**使用 qwen4-max 时，可用 `params.cacheRetention` 设置 `short`、`long` 或 `none`，`long` 对应 1 小时 TTL。qwen4-max 的上下文长度为 1M Token；非思考模式最大输出 131,072 Token，思考与最终回答合计最大 262,144 Token；默认 reasoning\_effort=high，thinking\_budget=131072。
    

**说明**`gateway.auth.mode: none` 仅适合单机本地使用。需要共享或远程访问时，运行 `openclaw doctor --generate-gateway-token` 生成 token，再重启 Gateway。

## 接入消息渠道

#### 钉钉

**说明**使用[轻量应用服务器](https://help.aliyun.com/zh/simple-application-server/use-cases/quickly-deploy-and-use-openclaw)或[无影云电脑](https://help.aliyun.com/zh/edsp/getting-started/quickly-create-openclaw-through-wuying-cloud-computer-personal-edition/)部署 OpenClaw 时，通常已内置钉钉插件，并可通过图形化界面完成配置。

1.  1
    
    创建钉钉应用并获取凭证
    
    1.  登录[钉钉开放平台](https://open-dev.dingtalk.com/)，选择有开发者权限的组织，或创建组织后[获取开发者权限](https://open.dingtalk.com/document/orgapp/obtain-developer-permissions)。
    2.  在顶部菜单栏选择**应用**，点击**创建应用**，填写应用名称和描述后点击**保存**。
    3.  在**添加应用能力**页面添加**机器人**，开启**机器人配置**，填写必填项，**消息接收模式**保持默认的 **Stream 模式**，点击**发布**。
    4.  在**凭证与基础信息**页面获取 Client ID 和 Client Secret。
    5.  在**版本管理与发布**页面创建版本，设置可见范围，保存并发布。
    
2.  2
    
    安装钉钉渠道插件
    
    ```
    openclaw plugins install @soimy/dingtalk
    openclaw plugins list
    ```
    
    输出中应包含 `dingtalk` 插件且状态为 `loaded`。
    
3.  3
    
    配置钉钉渠道
    
    在 `~/.openclaw/openclaw.json` 中添加以下配置。将 `YOUR_DINGTALK_APPKEY` 和 `YOUR_DINGTALK_APPSECRET` 替换为步骤一获取的凭证，不要覆盖已有的 `models`、`agents` 等配置。
    
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
    
    `dmPolicy` 和 `groupPolicy` 设为 `open` 适用于测试或个人使用。生产环境建议改为 `allowlist`，并添加 `allowFrom` 字段：
    
    ```
    "dmPolicy": "allowlist",
    "groupPolicy": "allowlist",
    "allowFrom": ["你的工号", "群ID"]
    ```
    
4.  4
    
    验证
    
    ```
    openclaw gateway restart
    openclaw status
    ```
    
    在 Channels 部分，DingTalk 应显示为 `ON`，状态为 `OK - configured`。在钉钉群聊中向机器人发送消息测试。
    

#### 飞书

1.  1
    
    创建飞书应用
    
    1.  访问[飞书开放平台](https://open.feishu.cn/app)，点击**创建企业自建应用**，填写应用名称和描述，选择应用图标后点击**创建**。
    2.  在**凭证与基础信息**页面复制 **App ID**（格式如 `cli_xxx`）和 **App Secret**。
    3.  在**权限管理**页面点击**批量导入/导出权限**，粘贴以下 JSON，点击**下一步，确认新增权限**，再点击**申请开通**。
    
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
    
    4.  在**添加应用能力**页面选择**按能力添加**，找到**机器人**卡片并点击**配置**。
    5.  在**事件与回调**的**事件配置**页签中，将**订阅方式**设为**使用长连接接收事件**并保存；再添加事件 `im.message.receive_v1`。
    6.  在**版本管理与发布**页面创建版本，填写版本号和更新说明，保存并提交审核发布。
    
2.  2
    
    配置飞书机器人
    
    运行 `openclaw channels add`，按提示选择 **Feishu**，输入 App ID 和 App Secret，再重启网关：
    
    ```
    openclaw gateway restart
    ```
    
    在飞书群聊中添加机器人，或向机器人发送消息。机器人会回复一条包含**配对码**的消息，复制最后一行并在 OpenClaw 对话中发送，完成配对。
    
3.  3
    
    验证
    
    ```
    openclaw status
    ```
    
    在 Channels 部分，Feishu 应显示为 `ON`，状态为 `OK`。在飞书中发送消息测试。
    

#### 微信

**说明**微信版本需要 8.0.70 或更高。

1.  1
    
    安装微信渠道插件
    
    ```
    npx -y @tencent-weixin/openclaw-weixin-cli@latest install
    ```
    
    安装完成后终端会显示二维码，使用微信扫码完成身份绑定。绑定成功后微信会自动打开 ClawBot 聊天页面。
    
    运行 `openclaw plugins list`，输出中应包含 `openclaw-weixin` 插件且状态为 `loaded`。
    
2.  2
    
    验证
    
    ```
    openclaw gateway restart
    ```
    
    在微信中找到 ClawBot，发送消息测试。
    

#### QQ

1.  1
    
    安装 QQ 渠道插件
    
    ```
    openclaw plugins install @sliverp/qqbot
    openclaw plugins list
    ```
    
    输出中应包含 `qqbot` 插件且状态为 `loaded`。
    
2.  2
    
    创建 QQ 机器人
    
    1.  访问 [QQ 开放平台](https://q.qq.com/#/)，注册并登录开发者账号。
    2.  在 [OpenClaw 页面](https://q.qq.com/qqbot/openclaw/index.html) 创建机器人，获取 AppID 和 AppSecret。
    
    **说明**AppSecret 不支持明文保存，二次查看会强制重置，请妥善保存。
    
3.  3
    
    配置 QQ 渠道
    
    在 `~/.openclaw/openclaw.json` 中添加以下配置。将 `YOUR_APP_ID` 和 `YOUR_APP_SECRET` 替换为步骤二获取的凭证，不要覆盖已有的 `models`、`agents` 等配置。
    
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
    
    `dmPolicy` 设为 `open` 表示允许私聊，`allowFrom` 设为 `["*"]` 表示允许全部来源的消息，适用于测试或个人使用。生产环境建议限制访问范围。
    
4.  4
    
    验证
    
    ```
    openclaw gateway restart
    ```
    
    在 QQ 中向机器人发送消息测试。
    

#### 邮箱

通过邮箱渠道，可以使用 163 邮箱等支持 IMAP/SMTP 协议的邮箱与 OpenClaw 进行交互。

#### 步骤一：安装邮箱渠道插件

1.  1
    
    在终端中执行以下命令安装邮箱渠道插件：
    
    ```
    openclaw plugins install @openclaw/email
    ```
    
2.  2
    
    安装完成后，执行以下命令确认插件已加载：
    
    ```
    openclaw plugins list
    ```
    
    输出中应包含 `email` 插件且状态为 `loaded`。
    

#### 步骤二：配置邮箱渠道

在 `~/.openclaw/openclaw.json` 中添加 `channels` 和 `plugins.allow` 配置。请将 `channels` 和 `plugins` 添加到已有配置文件的对应位置，不要覆盖已有的 `models`、`agents` 等配置。

以 163 邮箱为例，将 `YOUR_EMAIL` 替换为 163 邮箱地址，将 `YOUR_AUTH_CODE` 替换为 163 邮箱的授权码（非登录密码，需在 163 邮箱设置中开启 IMAP 服务后获取）。

```
{
  "channels": {
    "email": {
      "enabled": true,
      "imap": {
        "host": "imap.163.com",
        "port": 993,
        "secure": true,
        "user": "YOUR_EMAIL",
        "password": "YOUR_AUTH_CODE"
      },
      "smtp": {
        "host": "smtp.163.com",
        "port": 465,
        "secure": true,
        "user": "YOUR_EMAIL",
        "password": "YOUR_AUTH_CODE"
      }
    }
  },
  "plugins": {
    "allow": ["email"],
    "entries": {
      "email": {
        "enabled": true
      }
    }
  }
}
```

#### 步骤三：测试

1.  1
    
    执行以下命令重启网关。
    
    ```
    openclaw gateway restart
    ```
    
2.  2
    
    执行以下命令检查邮箱渠道状态。
    
    ```
    openclaw status
    ```
    
    在 Channels 部分，Email 应显示为 `ON` 且状态为 `OK`。
    
3.  3
    
    向配置的邮箱地址发送一封邮件，验证机器人是否自动回复。
    

## 错误码

配置过程中遇到报错，参考对应计费方案的常见问题文档：

-   Token Plan：[Token Plan 常见问题](https://help.aliyun.com/zh/model-studio/token-plan-faq#tpt-h-errors)
-   按量计费：[错误码](raw/model-api-reference/preparations/error-code.md)
-   Coding Plan：[Coding Plan 常见问题](https://help.aliyun.com/zh/model-studio/coding-plan-faq#e07ad90b4f3l0)

## 常见问题

如何按量计费接入节省计划与资源包？

按量计费接入方式不变，使用百炼通用 API Key 和 Base URL。购买节省计划或资源包后自动生效，调用费用按抵扣顺序自动抵扣。详情参见[节省计划与资源包](https://help.aliyun.com/zh/model-studio/savings-plan-and-resource-package#h2-usage)。

如何查看已配置的模型？

在终端输入 `openclaw tui`，进入 OpenClaw 终端命令行，接着输入 `/model` 查看模型列表。按回车键选中模型，按 Esc 键退出模型列表。

为什么报错“HTTP 401: Incorrect API key provided.”、“No API key found for provider xxx”或“HTTP 401: invalid\_iam\_token”？

可能原因：

1.  API Key 无效、过期、为空、格式错误，或与端点环境不匹配。请检查 API Key 是否与所使用的付费方式匹配，并确保复制完整且无空格；确认订阅状态有效。
2.  OpenClaw 的历史配置缓存导致配置错误，请删除 `~/.openclaw/agents/main/agent/models.json` 文件中的 `providers` 配置项，并重启 OpenClaw。
3.  `invalid_iam_token` 表示 API Key 经 IAM 鉴权校验失败。常见场景：API Key 已被吊销或禁用、API Key 归属的地域与 Base URL 所指地域不一致（例如 API Key 在华北2（北京），但 Base URL 指向其他地域）、使用 STS 临时凭证且已过期。请核对 API Key 与 Base URL 归属同一地域，并确认 API Key 状态正常。

我已经配置过钉钉等其他渠道，如何安全地添加新套餐模型？

-   不要直接全量覆盖。全量替换会覆盖自定义配置，请进行局部修改。
-   若 OpenClaw 可正常对话，直接在 OpenClaw 对话中输入指令完成配置合并。
-   若 OpenClaw 未配置模型或无法对话，手动编辑 `~/.openclaw/openclaw.json`，只修改需要变更的字段，保留原有配置不变。

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
-   重装或升级 OpenClaw 后，`~/.openclaw/identity/` 目录下的密钥文件缺失。

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

执行 `openclaw devices list`，确认设备显示在 Paired 列表中即为正常。

没有主动使用 OpenClaw，但仍产生了 Token 消耗

**原因：** OpenClaw 内置心跳机制（Heartbeat），网关运行期间会按固定间隔（默认 30 分钟）自动调用已配置的模型，检查是否有待处理任务。每次心跳都会消耗少量 Token。

**如何确认：** 查看 `~/.openclaw/agents/main/sessions/` 目录下的会话记录文件（.jsonl），其中包含 `[OpenClaw heartbeat poll]` 标记的心跳调用记录。

**解决方法：**

-   停止网关：不使用时执行 `openclaw gateway stop`，心跳随即停止。
-   增大心跳间隔：在 `~/.openclaw/openclaw.json` 中设置 `agents.defaults.heartbeat.every`，例如 `"2h"` 表示每 2 小时一次。
