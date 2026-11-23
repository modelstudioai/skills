# Kilo CLI

在 Kilo CLI 中使用阿里云百炼模型。

## 快速开始

1.  1
    
    启动 Kilo CLI
    
    ```
    kilo
    ```
    
2.  2
    
    连接服务商
    
    输入 `/connect`，按计费方案选择服务商并输入 API Key：
    
    #### Token Plan
    
    选择 **Alibaba Token Plan (China)**，输入对应版本的 Token Plan API Key：
    
    -   Token Plan 个人版：[创建或查看 API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan/personal)
    -   Token Plan 团队版：[分配坐席并获取 API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/uac-admin/organization/members/list)
    
    #### 按量计费
    
    选择 **Alibaba (China)**，输入[百炼 API Key](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key?spm=5176.28197581.0.0.307f29a4lC7Vbh)。
    
    #### Coding Plan
    
    选择 **Alibaba Coding Plan (China)**，输入 [Coding Plan API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/coding-plan)。
    
3.  3
    
    选择模型
    
    输入 `/models`，选择需要的模型。
    
4.  4
    
    验证
    
    ```
    kilo run "你好"
    ```
    

## 通过配置文件接入

除了上述方式，也可以通过配置文件接入。

1.  1
    
    打开或新建配置文件
    
    -   macOS / Linux：`~/.config/kilo/config.json`
    -   Windows：`C:\Users\<用户名>\.config\kilo\config.json`
    
2.  2
    
    写入配置
    
    将 `YOUR_API_KEY` 替换为对应方案的 API Key，并把配置写入 `config.json`。
    
    #### Token Plan 个人版
    
    ```
    {
      "$schema": "https://kilo.ai/config.json",
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
      "$schema": "https://kilo.ai/config.json",
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
      "$schema": "https://kilo.ai/config.json",
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
      "$schema": "https://kilo.ai/config.json",
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
              }
            }
          }
        }
      }
    }
    ```
    
    **说明**使用 qwen4-max-preview 时，单次输出上限默认 32000，需要更长输出可设置 `KILO_EXPERIMENTAL_OUTPUT_TOKEN_MAX`；只改 `limit.output` 不会提高上限。
    
    **说明**使用 qwen4-max 时，单次输出上限默认 32000，需要更长输出可设置 `KILO_EXPERIMENTAL_OUTPUT_TOKEN_MAX`；只改 `limit.output` 不会提高上限。qwen4-max 的上下文长度为 1M Token；非思考模式最大输出 131,072 Token，思考与最终回答合计最大 262,144 Token；默认 reasoning\_effort=high，thinking\_budget=131072。
    
3.  3
    
    验证
    
    保存后运行以下命令：
    
    ```
    kilo run "你好" -m <provider>/<model>
    ```
    
    将 `<provider>/<model>` 替换为对应方案的 provider 和模型，例如 `bailian-token-plan/auto`。
    

## 错误码

配置过程中遇到报错，参考对应计费方案的常见问题文档：

-   Token Plan：[Token Plan 常见问题](https://help.aliyun.com/zh/model-studio/token-plan-faq#tpt-h-errors)
-   按量计费：[错误码](raw/model-api-reference/preparations/error-code.md)
-   Coding Plan：[Coding Plan 常见问题](https://help.aliyun.com/zh/model-studio/coding-plan-faq#e07ad90b4f3l0)

## 常见问题

如何按量计费接入节省计划与资源包？

按量计费接入方式不变，使用百炼通用 API Key 和 Base URL。购买节省计划或资源包后自动生效，调用费用按抵扣顺序自动抵扣。详情参见[节省计划与资源包](https://help.aliyun.com/zh/model-studio/savings-plan-and-resource-package#h2-usage)。

模型列表中没有需要的模型

在 `config.json` 的 `models` 中按现有格式追加模型 ID，保存后重新打开 Kilo CLI。支持的模型见对应计费方案的支持列表。

调用时返回 401 Unauthorized

API Key 与 Base URL 不匹配，或使用了其他计费方案的 Key。确认 Key 类型与配置中的 `baseURL` 对应，并重新保存配置。
