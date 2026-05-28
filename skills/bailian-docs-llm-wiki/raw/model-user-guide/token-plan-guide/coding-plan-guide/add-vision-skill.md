# 添加视觉理解能力

百炼 Coding Plan 中的部分模型（qwen3.6-plus、qwen3.5-plus、kimi-k2.5）原生支持视觉理解，可直接处理图片输入。对于 glm-5、MiniMax-M2.5 等纯文本模型，可通过添加本地 Skill 使其获得视觉能力。

**说明**

运行图片理解 Skill 会消耗 Coding Plan 额度，无其他收费项。

## 前提条件

1.  已订阅 [Coding Plan](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/coding_plan)，详情请参见[快速开始](https://help.aliyun.com/zh/model-studio/coding-plan-quickstart)。
    
2.  已在 Coding Plan 工具中完成接入配置，且能正常对话，详情请参见[接入客户端/开发工具](https://help.aliyun.com/zh/model-studio/use-chat-client-or-development-tool/)。
    

## 视觉支持情况

**模型**

**是否支持视觉**

**说明**

-   qwen3.6-plus
    
-   qwen3.5-plus
    
-   kimi-k2.5
    

是

无需额外配置，可直接传入图片

-   qwen3-max-2026-01-23
    
-   qwen3-coder-next
    
-   qwen3-coder-plus
    
-   glm-5
    
-   glm-4.7
    
-   MiniMax-M2.5
    

否

需通过 Skill 或 Agent 辅助模型获得视觉能力

## 方法 1：直接使用视觉模型（推荐）

qwen3.6-plus、qwen3.5-plus 和 kimi-k2.5 具备视觉理解能力。如果经常需要处理图片，直接切换到这些模型是最简单、推荐的做法。

**工具**

**模型切换方式**

Claude Code

`/model qwen3.6-plus`或`/model qwen3.5-plus`或 `/model kimi-k2.5`

OpenCode

`/models`→ 搜索并选择`qwen3.6-plus`或`qwen3.5-plus`或`kimi-k2.5`

Qwen Code

`/model`→ 选择`qwen3.6-plus`或`qwen3.5-plus`或`kimi-k2.5`

更多编程工具中的模型切换方式请参考[接入客户端/开发工具](https://help.aliyun.com/zh/model-studio/use-chat-client-or-development-tool/)。切换后可直接在对话中引用图片路径，或拖拽/粘贴图片。

## 方法 2：通过 Skill 或 Agent 添加视觉能力

如需使用 glm-5、MiniMax-M2.5 等不支持视觉的模型处理图片，可通过配置 Skill 或 Agent 实现。

## Claude Code

1.  **添加 Skill**
    
    在项目目录下的 `.claude` 文件夹中新建 `skills/image-analyzer` 目录：
    
    ```
    mkdir -p .claude/skills/image-analyzer
    ```
    
    在该目录下创建 `SKILL.md` 文件，并写入以下内容：
    
    ```
    ---
    name: image-analyzer
    description: 帮助没有视觉能力的模型进行图像理解。当需要分析图像内容、提取图片中的信息、文字、界面元素，或理解截图、图表、架构图等任何视觉内容时，使用此技能，传入图片路径即可获得描述信息。
    model: qwen3.6-plus
    ---
    qwen3.6-plus具有视觉理解能力，请直接使用qwen3.6-plus模型进行图片理解。
    ```
    
    创建完成后的目录结构如下：
    
    ```
    .claude/
    └── skills/
        └── image-analyzer/
            └── SKILL.md
    ```
    
2.  **开始使用**
    
    1.  在项目目录下运行`claude`启动 Claude Code，并运行`/model glm-5`切换到`glm-5`模型。
        
    2.  下载[aliyun.png](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260225/hxwnny/aliyun.png)到项目目录下，并提问：`请加载image-analyzer skill，描述一下 aliyun.png banner位置是什么信息。`可收到如下回复：
        
        ![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5928202771/p1054884.png)
        

### OpenCode

1.  **添加 Agent**
    
    在项目目录下的 `.opencode` 文件夹中新建 `agents` 目录：
    
    ```
    mkdir -p .opencode/agents
    ```
    
    在该目录下创建`image-analyzer.md`文件，并写入以下内容：
    
    **说明**
    
    model 字段必须使用 OpenCode 配置文件中定义的 provider 和模型名称。参考 [OpenCode](https://help.aliyun.com/zh/model-studio/opencode) 文档的配置示例，应为`bailian-coding-plan/qwen3.6-plus`。
    
    ```
    ---
    description: Analyzes images using a vision-capable model. Use this agent when the user needs to understand image content, extract information from screenshots, diagrams, UI mockups, or any visual content. Invoke with @image-analyzer followed by the image path and your question.
    mode: subagent
    model: bailian-coding-plan/qwen3.6-plus
    tools:
      write: false
      edit: false
    ---
    You have vision capabilities. Analyze the provided image and return a clear, structured description focused on what the user is asking about.
    ```
    
    创建完成后的目录结构如下：
    
    ```
    .opencode/
    └── agents/
        └── image-analyzer.md
    ```
    
2.  **开始使用**
    
    1.  在项目目录下运行`opencode`启动 OpenCode，并切换到`glm-5`模型。
        
    2.  下载[aliyun.png](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260225/hxwnny/aliyun.png)到项目目录下，通过`@`唤起`image-analyzer`并提问：`@image-analyzer，描述一下 aliyun.png banner位置是什么信息。`可收到如下回复：
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6472262771/p1055847.png)
        

## **常见问题**

### **OpenCode + 视觉理解模型为什么无法理解图片？**

**原因**：OpenCode 默认不启用模型的视觉能力，需要在配置文件中显式声明 `modalities` 参数。

**解决方案**：在 OpenCode 配置文件的模型定义中添加 `modalities` 字段，将 `input` 设为 `["text", "image"]`，如下所示：

> 将sk-sp-xxx替换为Coding Plan API Key。

```
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "bailian-coding-plan-test": {
      "npm": "@ai-sdk/anthropic",
      "name": "Model Studio Coding Plan",
      "options": {
        "baseURL": "https://coding.dashscope.aliyuncs.com/apps/anthropic/v1",
        "apiKey": "sk-sp-xxx"
      },
      "models": {
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
          "options": {
            "thinking": {
              "type": "enabled",
              "budgetTokens": 1024
            }
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
          "options": {
            "thinking": {
              "type": "enabled",
              "budgetTokens": 1024
            }
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

### **OpenClaw + 视觉理解模型为什么无法理解图片？**

**原因**：OpenClaw 需要通过配置文件中的 input 字段来判断模型是否支持视觉能力。

**解决方案**：

1.  在`~/.openclaw/openclaw.json`配置文件中，确保模型定义包含`"input": ["text", "image"]`字段。
    
    ```
    {
      "models": {
        "mode": "merge",
        "providers": {
          "bailian": {
            "baseUrl": "https://coding.dashscope.aliyuncs.com/v1",
            "apiKey": "YOUR_API_KEY",
            "api": "openai-completions",
            "models": [
              {
                "id": "qwen3.6-plus",
                "name": "qwen3.6-plus",
                "reasoning": false,
                "input": ["text", "image"],
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "contextWindow": 1000000,
                "maxTokens": 65536
              },
              {
                "id": "qwen3.5-plus",
                "name": "qwen3.5-plus",
                "reasoning": false,
                "input": ["text", "image"],
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "contextWindow": 1000000,
                "maxTokens": 65536
              },
              {
                "id": "kimi-k2.5",
                "name": "kimi-k2.5",
                "reasoning": false,
                "input": ["text", "image"],
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "contextWindow": 262144,
                "maxTokens": 32768
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
            "bailian/qwen3.5-plus": {},
            "bailian/kimi-k2.5": {}
          }
        }
      },
      "gateway": {
        "mode": "local"
      }
    }
    ```
    
2.  修改配置后，需要清除 OpenClaw 的模型缓存并重启，否则旧的配置仍会生效。
    
    ```
    rm ~/.openclaw/agents/main/agent/models.json
    openclaw gateway restart
    ```
