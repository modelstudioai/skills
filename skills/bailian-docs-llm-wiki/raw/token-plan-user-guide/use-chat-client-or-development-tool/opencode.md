# OpenCode

在 OpenCode 中使用阿里云百炼模型。

## 快速开始

1.  1
    
    连接服务商
    
    运行 `opencode`，输入 `/connect`，按计费方案选择服务商并输入 API Key：
    
    #### Token Plan
    
    选择 **Alibaba Token Plan (China)**，输入对应版本的 Token Plan API Key：
    
    -   Token Plan 个人版：[创建或查看 API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan/personal)
    -   Token Plan 团队版：[分配坐席并获取 API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/uac-admin/organization/members/list)
    
    #### 按量计费
    
    选择 **Alibaba (China)**，输入 [百炼 API Key](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key?spm=5176.28197581.0.0.307f29a4lC7Vbh)。
    
    #### Coding Plan
    
    选择 **Alibaba Coding Plan (China)**，输入 [Coding Plan API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/coding-plan)。
    
2.  2
    
    选择模型
    
    输入 `/models`，选择需要的模型。
    
3.  3
    
    验证
    
    运行以下命令验证：
    
    ```
    opencode run "你好"
    ```
    

## 通过配置文件接入

除了上述方式，也可以通过配置文件接入。

1.  1
    
    打开或新建配置文件
    
    -   macOS / Linux：`~/.config/opencode/opencode.json`
    -   Windows：`C:\Users\<用户名>\.config\opencode\opencode.json`
    
2.  2
    
    写入配置
    
    将 `YOUR_API_KEY` 替换为对应方案的 API Key。
    
    #### Token Plan 个人版
    
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
            "auto": {
              "name": "Auto",
              "modalities": {
                "input": [
                  "text"
                ],
                "output": [
                  "text"
                ]
              },
              "limit": {
                "context": 1000000,
                "output": 393216
              }
            },
            "qwen4-max-preview": {
              "name": "Qwen4.0 Max Preview",
              "modalities": {
                "input": [
                  "text",
                  "image"
                ],
                "output": [
                  "text"
                ]
              },
              "limit": {
                "context": 1000000,
                "output": 131072
              }
            },
            "qwen4-max": {
              "name": "Qwen4 Max",
              "modalities": {
                "input": [
                  "text",
                  "image"
                ],
                "output": [
                  "text"
                ]
              },
              "limit": {
                "context": 1000000,
                "output": 262144
              }
            },
            "qwen3.8-max": {
              "name": "Qwen3.8 Max",
              "modalities": {
                "input": [
                  "text",
                  "image"
                ],
                "output": [
                  "text"
                ]
              },
              "limit": {
                "context": 1000000,
                "output": 131072
              }
            },
            "qwen3.8-flash": {
              "name": "Qwen3.8 Flash",
              "modalities": {
                "input": [
                  "text",
                  "image"
                ],
                "output": [
                  "text"
                ]
              },
              "limit": {
                "context": 1000000,
                "output": 131072
              }
            },
            "qwen3.7-max": {
              "name": "Qwen3.7 Max",
              "modalities": {
                "input": [
                  "text"
                ],
                "output": [
                  "text"
                ]
              },
              "limit": {
                "context": 1000000,
                "output": 65536
              }
            },
            "qwen3.7-plus": {
              "name": "Qwen3.7 Plus",
              "modalities": {
                "input": [
                  "text",
                  "image"
                ],
                "output": [
                  "text"
                ]
              },
              "limit": {
                "context": 1000000,
                "output": 65536
              }
            },
            "qwen3.6-flash": {
              "name": "Qwen3.6 Flash",
              "modalities": {
                "input": [
                  "text",
                  "image"
                ],
                "output": [
                  "text"
                ]
              },
              "limit": {
                "context": 1000000,
                "output": 65536
              }
            },
            "deepseek-v4.1-flash": {
              "name": "DeepSeek V4.1 Flash",
              "modalities": {
                "input": [
                  "text",
                  "image"
                ],
                "output": [
                  "text"
                ]
              },
              "limit": {
                "context": 1000000,
                "output": 65536
              }
            },
            "deepseek-v4.1-flash-1017": {
              "name": "DeepSeek V4.1 Flash 1017",
              "modalities": {
                "input": [
                  "text",
                  "image"
                ],
                "output": [
                  "text"
                ]
              },
              "limit": {
                "context": 1000000,
                "output": 65536
              }
            },
            "deepseek-v4-pro": {
              "name": "DeepSeek V4 Pro",
              "modalities": {
                "input": [
                  "text"
                ],
                "output": [
                  "text"
                ]
              },
              "limit": {
                "context": 1000000,
                "output": 65536
              }
            },
            "deepseek-v4-pro-0813": {
              "name": "DeepSeek V4 Pro 0813",
              "modalities": {
                "input": [
                  "text"
                ],
                "output": [
                  "text"
                ]
              },
              "limit": {
                "context": 1000000,
                "output": 65536
              }
            },
            "deepseek-v4-flash-0731": {
              "name": "DeepSeek V4 Flash 0731",
              "modalities": {
                "input": [
                  "text"
                ],
                "output": [
                  "text"
                ]
              },
              "limit": {
                "context": 1000000,
                "output": 65536
              }
            },
            "glm-5.3": {
              "name": "GLM-5.3",
              "modalities": {
                "input": [
                  "text"
                ],
                "output": [
                  "text"
                ]
              },
              "limit": {
                "context": 202752,
                "output": 16384
              }
            },
            "glm-5.2": {
              "name": "GLM-5.2",
              "modalities": {
                "input": [
                  "text"
                ],
                "output": [
                  "text"
                ]
              },
              "limit": {
                "context": 202752,
                "output": 16384
              }
            }
          }
        }
      }
    }
    ```
    
    #### Token Plan 团队版
    
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
            "auto": {
              "name": "Auto",
              "modalities": {
                "input": [
                  "text"
                ],
                "output": [
                  "text"
                ]
              },
              "limit": {
                "context": 1000000,
                "output": 393216
              }
            },
            "qwen4-max-preview": {
              "name": "Qwen4.0 Max Preview",
              "modalities": {
                "input": [
                  "text",
                  "image"
                ],
                "output": [
                  "text"
                ]
              },
              "limit": {
                "context": 1000000,
                "output": 131072
              }
            },
            "qwen4-max": {
              "name": "Qwen4 Max",
              "modalities": {
                "input": [
                  "text",
                  "image"
                ],
                "output": [
                  "text"
                ]
              },
              "limit": {
                "context": 1000000,
                "output": 262144
              }
            },
            "qwen3.8-max": {
              "name": "Qwen3.8 Max",
              "modalities": {
                "input": [
                  "text",
                  "image"
                ],
                "output": [
                  "text"
                ]
              },
              "limit": {
                "context": 1000000,
                "output": 131072
              }
            },
            "qwen3.8-flash": {
              "name": "Qwen3.8 Flash",
              "modalities": {
                "input": [
                  "text",
                  "image"
                ],
                "output": [
                  "text"
                ]
              },
              "limit": {
                "context": 1000000,
                "output": 131072
              }
            },
            "qwen3.7-max": {
              "name": "Qwen3.7 Max",
              "modalities": {
                "input": [
                  "text"
                ],
                "output": [
                  "text"
                ]
              },
              "limit": {
                "context": 1000000,
                "output": 65536
              }
            },
            "qwen3.7-plus": {
              "name": "Qwen3.7 Plus",
              "modalities": {
                "input": [
                  "text",
                  "image"
                ],
                "output": [
                  "text"
                ]
              },
              "limit": {
                "context": 1000000,
                "output": 65536
              }
            },
            "qwen3.6-plus": {
              "name": "Qwen3.6 Plus",
              "modalities": {
                "input": [
                  "text",
                  "image"
                ],
                "output": [
                  "text"
                ]
              },
              "limit": {
                "context": 1000000,
                "output": 65536
              }
            },
            "qwen3.6-flash": {
              "name": "Qwen3.6 Flash",
              "modalities": {
                "input": [
                  "text",
                  "image"
                ],
                "output": [
                  "text"
                ]
              },
              "limit": {
                "context": 1000000,
                "output": 65536
              }
            },
            "deepseek-v4.1-flash": {
              "name": "DeepSeek V4.1 Flash",
              "modalities": {
                "input": [
                  "text",
                  "image"
                ],
                "output": [
                  "text"
                ]
              },
              "limit": {
                "context": 1000000,
                "output": 65536
              }
            },
            "deepseek-v4.1-flash-1017": {
              "name": "DeepSeek V4.1 Flash 1017",
              "modalities": {
                "input": [
                  "text",
                  "image"
                ],
                "output": [
                  "text"
                ]
              },
              "limit": {
                "context": 1000000,
                "output": 65536
              }
            },
            "deepseek-v4-pro": {
              "name": "DeepSeek V4 Pro",
              "modalities": {
                "input": [
                  "text"
                ],
                "output": [
                  "text"
                ]
              },
              "limit": {
                "context": 1000000,
                "output": 65536
              }
            },
            "deepseek-v4-pro-0813": {
              "name": "DeepSeek V4 Pro 0813",
              "modalities": {
                "input": [
                  "text"
                ],
                "output": [
                  "text"
                ]
              },
              "limit": {
                "context": 1000000,
                "output": 65536
              }
            },
            "deepseek-v4-flash-0731": {
              "name": "DeepSeek V4 Flash 0731",
              "modalities": {
                "input": [
                  "text"
                ],
                "output": [
                  "text"
                ]
              },
              "limit": {
                "context": 1000000,
                "output": 65536
              }
            },
            "kimi-k2.7-code": {
              "name": "Kimi K2.7 Code",
              "modalities": {
                "input": [
                  "text",
                  "image"
                ],
                "output": [
                  "text"
                ]
              },
              "limit": {
                "context": 262144,
                "output": 98304
              }
            },
            "kimi-k2.6": {
              "name": "Kimi K2.6",
              "modalities": {
                "input": [
                  "text",
                  "image"
                ],
                "output": [
                  "text"
                ]
              },
              "limit": {
                "context": 262144,
                "output": 98304
              }
            },
            "kimi-k2.5": {
              "name": "Kimi K2.5",
              "modalities": {
                "input": [
                  "text",
                  "image"
                ],
                "output": [
                  "text"
                ]
              },
              "limit": {
                "context": 262144,
                "output": 98304
              }
            },
            "glm-5.3": {
              "name": "GLM-5.3",
              "modalities": {
                "input": [
                  "text"
                ],
                "output": [
                  "text"
                ]
              },
              "limit": {
                "context": 202752,
                "output": 16384
              }
            },
            "glm-5.2": {
              "name": "GLM-5.2",
              "modalities": {
                "input": [
                  "text"
                ],
                "output": [
                  "text"
                ]
              },
              "limit": {
                "context": 202752,
                "output": 16384
              }
            },
            "glm-5.1": {
              "name": "GLM-5.1",
              "modalities": {
                "input": [
                  "text"
                ],
                "output": [
                  "text"
                ]
              },
              "limit": {
                "context": 202752,
                "output": 16384
              }
            },
            "glm-5": {
              "name": "GLM-5",
              "modalities": {
                "input": [
                  "text"
                ],
                "output": [
                  "text"
                ]
              },
              "limit": {
                "context": 202752,
                "output": 16384
              }
            },
            "MiniMax-M2.5": {
              "name": "MiniMax M2.5",
              "modalities": {
                "input": [
                  "text"
                ],
                "output": [
                  "text"
                ]
              },
              "limit": {
                "context": 196608,
                "output": 32768
              }
            }
          }
        }
      }
    }
    ```
    
    #### 按量计费
    
    将 `{WorkspaceId}` 替换为真实的 [Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。
    
    ```
    {
      "$schema": "https://opencode.ai/config.json",
      "provider": {
        "bailian-payg": {
          "npm": "@ai-sdk/anthropic",
          "name": "Alibaba Cloud Model Studio",
          "options": {
            "baseURL": "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic/v1",
            "apiKey": "YOUR_API_KEY"
          },
          "models": {
            "qwen3.8-max": {
              "name": "Qwen3.8 Max",
              "modalities": {
                "input": [
                  "text",
                  "image"
                ],
                "output": [
                  "text"
                ]
              },
              "limit": {
                "context": 1000000,
                "output": 131072
              }
            },
            "qwen3.7-plus": {
              "name": "Qwen3.7 Plus",
              "modalities": {
                "input": [
                  "text",
                  "image"
                ],
                "output": [
                  "text"
                ]
              },
              "limit": {
                "context": 1000000,
                "output": 65536
              }
            },
            "qwen3.8-flash": {
              "name": "Qwen3.8 Flash",
              "modalities": {
                "input": [
                  "text",
                  "image"
                ],
                "output": [
                  "text"
                ]
              },
              "limit": {
                "context": 1000000,
                "output": 131072
              }
            },
            "deepseek-v4-pro-0813": {
              "name": "DeepSeek V4 Pro 0813",
              "modalities": {
                "input": [
                  "text"
                ],
                "output": [
                  "text"
                ]
              },
              "limit": {
                "context": 1000000,
                "output": 65536
              }
            },
            "deepseek-v4.1-flash": {
              "name": "DeepSeek V4.1 Flash",
              "modalities": {
                "input": [
                  "text",
                  "image"
                ],
                "output": [
                  "text"
                ]
              },
              "limit": {
                "context": 1000000,
                "output": 65536
              }
            }
          }
        }
      }
    }
    ```
    
    #### Coding Plan
    
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
            "qwen3.7-plus": {
              "name": "Qwen3.7 Plus",
              "modalities": {
                "input": [
                  "text",
                  "image"
                ],
                "output": [
                  "text"
                ]
              },
              "limit": {
                "context": 1000000,
                "output": 65536
              }
            },
            "qwen3.6-plus": {
              "name": "Qwen3.6 Plus",
              "modalities": {
                "input": [
                  "text",
                  "image"
                ],
                "output": [
                  "text"
                ]
              },
              "limit": {
                "context": 1000000,
                "output": 65536
              }
            },
            "kimi-k2.5": {
              "name": "Kimi K2.5",
              "modalities": {
                "input": [
                  "text",
                  "image"
                ],
                "output": [
                  "text"
                ]
              },
              "limit": {
                "context": 262144,
                "output": 98304
              }
            },
            "glm-5": {
              "name": "GLM-5",
              "modalities": {
                "input": [
                  "text"
                ],
                "output": [
                  "text"
                ]
              },
              "limit": {
                "context": 202752,
                "output": 16384
              }
            },
            "MiniMax-M2.5": {
              "name": "MiniMax M2.5",
              "modalities": {
                "input": [
                  "text"
                ],
                "output": [
                  "text"
                ]
              },
              "limit": {
                "context": 196608,
                "output": 32768
              }
            },
            "qwen3.5-plus": {
              "name": "Qwen3.5 Plus",
              "modalities": {
                "input": [
                  "text",
                  "image"
                ],
                "output": [
                  "text"
                ]
              },
              "limit": {
                "context": 1000000,
                "output": 65536
              }
            }
          }
        }
      }
    }
    ```
    
    **说明**使用 qwen4-max-preview 时，单次输出上限默认 32000，需要更长输出可设置 `OPENCODE_EXPERIMENTAL_OUTPUT_TOKEN_MAX`。
    
    **说明**使用 qwen4-max 时，单次输出上限默认 32000，需要更长输出可设置 `OPENCODE_EXPERIMENTAL_OUTPUT_TOKEN_MAX`。qwen4-max 的上下文长度为 1M Token；非思考模式最大输出 131,072 Token，思考与最终回答合计最大 262,144 Token；默认 reasoning\_effort=high，thinking\_budget=131072。
    

## 错误码

配置过程中遇到报错，参考对应计费方案的常见问题文档：

-   Token Plan：[Token Plan 常见问题](https://help.aliyun.com/zh/model-studio/token-plan-faq#tpt-h-errors)
-   按量计费：[错误码](raw/model-api-reference/preparations/error-code.md)
-   Coding Plan：[Coding Plan 常见问题](https://help.aliyun.com/zh/model-studio/coding-plan-faq#e07ad90b4f3l0)

## 常见问题

如何按量计费接入节省计划与资源包？

按量计费接入方式不变，使用百炼通用 API Key 和 Base URL。购买节省计划或资源包后自动生效，调用费用按抵扣顺序自动抵扣。详情参见[节省计划与资源包](https://help.aliyun.com/zh/model-studio/savings-plan-and-resource-package#h2-usage)。

模型列表中没有需要的模型

先升级 OpenCode 到最新版本，再运行 `/models` 查看。仍没有时，可在 `opencode.json` 中自定义 provider 并添加模型。

调用时返回 401 Unauthorized

API Key 与所选服务商不匹配，或使用了其他计费方案的 Key。重新运行 `/connect`，选择对应计费方案的服务商并输入正确的 Key。
