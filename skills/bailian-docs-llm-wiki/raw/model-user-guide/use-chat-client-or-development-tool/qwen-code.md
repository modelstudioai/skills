# Qwen Code

Qwen Code 是一款终端 AI 编程工具，可以通过按量计费、Coding Plan 或 Token Plan 团队版接入阿里云百炼。

## **安装 Qwen Code**

-   **运行安装命令**
    
    -   **macOS/Linux：**
        
        打开终端，运行以下命令安装 Qwen Code。
        
        ```
        bash -c "$(curl -fsSL https://qwen-code-assets.oss-cn-hangzhou.aliyuncs.com/installation/install-qwen.sh)" -s --source bailian
        ```
        
    -   **Windows：**
        
        在任务栏搜索框里输入`cmd`，选择**以管理员身份运行**，打开`cmd`窗口后运行以下命令安装 Qwen Code。
        
        ```
        curl -fsSL -o %TEMP%\install-qwen.bat https://qwen-code-assets.oss-cn-hangzhou.aliyuncs.com/installation/install-qwen.bat && %TEMP%\install-qwen.bat --source bailian
        ```
        
-   **关闭并重新打开**`**cmd**`**窗口**
    
    Windows 系统在安装完成后，需关闭当前`cmd`窗口，以使环境变量生效。重新打开`cmd`后，运行以下命令查看当前安装版本。
    
    ```
    qwen --version
    ```
    

## **配置接入凭证**

启动 Qwen Code 后输入 `/auth` 命令进行可视化配置。阿里云百炼提供三种计费方案，根据需要选择：

-   **Token Plan 团队版**：按坐席订阅，按 token 消耗抵扣 Credits。
    
-   **Coding Plan**：固定月费订阅，按模型调用次数计量。
    
-   **按量计费**：按实际调用量后付费。
    

### Token Plan 团队版

启动 Qwen Code 后输入 `/auth`，依次选择 **订阅计划** > **阿里云百炼 Token Plan**，输入 Token Plan 团队版专属 [API Key](https://bailian.console.aliyun.com/?tab=plan#/efm/subscription/overview) 即可完成配置。可用模型请参考 Token Plan 团队版[支持的模型](https://help.aliyun.com/zh/model-studio/token-plan-overview)。

高级配置：通过 settings.json 配置文件

编辑或新建 `settings.json` 文件，将 `YOUR_API_KEY` 替换为 Token Plan 团队版专属 API Key。文件路径如下：

-   macOS/Linux：`~/.qwen/settings.json`
    
-   Windows：`C:\Users\<Windows用户名>\.qwen\settings.json`
    

```
{
  "env": {
    "BAILIAN_TOKEN_PLAN_API_KEY": "YOUR_API_KEY"
  },
  "modelProviders": {
    "openai": [
      {
        "id": "qwen3.7-max",
        "name": "[Token Plan 团队版] qwen3.7-max",
        "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
        "envKey": "BAILIAN_TOKEN_PLAN_API_KEY",
        "generationConfig": {
          "extra_body": {
            "enable_thinking": true
          }
        }
      },
      {
        "id": "qwen3.6-plus",
        "name": "[Token Plan 团队版] qwen3.6-plus",
        "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
        "envKey": "BAILIAN_TOKEN_PLAN_API_KEY",
        "generationConfig": {
          "extra_body": {
            "enable_thinking": true
          }
        }
      },
      {
        "id": "qwen3.6-flash",
        "name": "[Token Plan 团队版] qwen3.6-flash",
        "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
        "envKey": "BAILIAN_TOKEN_PLAN_API_KEY",
        "generationConfig": {
          "extra_body": {
            "enable_thinking": true
          }
        }
      },
      {
        "id": "deepseek-v4-pro",
        "name": "[Token Plan 团队版] deepseek-v4-pro",
        "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
        "envKey": "BAILIAN_TOKEN_PLAN_API_KEY"
      },
      {
        "id": "deepseek-v4-flash",
        "name": "[Token Plan 团队版] deepseek-v4-flash",
        "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
        "envKey": "BAILIAN_TOKEN_PLAN_API_KEY"
      },
      {
        "id": "deepseek-v3.2",
        "name": "[Token Plan 团队版] deepseek-v3.2",
        "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
        "envKey": "BAILIAN_TOKEN_PLAN_API_KEY"
      },
      {
        "id": "kimi-k2.6",
        "name": "[Token Plan 团队版] kimi-k2.6",
        "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
        "envKey": "BAILIAN_TOKEN_PLAN_API_KEY",
        "generationConfig": {
          "extra_body": {
            "enable_thinking": true
          }
        }
      },
      {
        "id": "kimi-k2.5",
        "name": "[Token Plan 团队版] kimi-k2.5",
        "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
        "envKey": "BAILIAN_TOKEN_PLAN_API_KEY",
        "generationConfig": {
          "extra_body": {
            "enable_thinking": true
          }
        }
      },
      {
        "id": "glm-5.1",
        "name": "[Token Plan 团队版] glm-5.1",
        "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
        "envKey": "BAILIAN_TOKEN_PLAN_API_KEY",
        "generationConfig": {
          "extra_body": {
            "enable_thinking": true
          }
        }
      },
      {
        "id": "glm-5",
        "name": "[Token Plan 团队版] glm-5",
        "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
        "envKey": "BAILIAN_TOKEN_PLAN_API_KEY",
        "generationConfig": {
          "extra_body": {
            "enable_thinking": true
          }
        }
      },
      {
        "id": "MiniMax-M2.5",
        "name": "[Token Plan 团队版] MiniMax-M2.5",
        "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
        "envKey": "BAILIAN_TOKEN_PLAN_API_KEY"
      }
    ]
  },
  "security": {
    "auth": {
      "selectedType": "openai"
    }
  },
  "tokenPlan": {
    "region": "china"
  },
  "model": {
    "name": "qwen3.6-plus"
  },
  "$version": 3
}
```

### Coding Plan

启动 Qwen Code 后输入 `/auth`，依次选择 **订阅计划** > **阿里云百炼 Coding Plan**，选择 Coding Plan 区域（china），输入 Coding Plan 专属 [API Key](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/coding_plan) 即可完成配置。可用模型请参考 Coding Plan [支持的模型](https://help.aliyun.com/zh/model-studio/coding-plan)。

高级配置：通过 settings.json 配置文件

编辑或新建 `settings.json` 文件，将 `YOUR_API_KEY` 替换为 Coding Plan 专属 API Key。文件路径如下：

-   macOS/Linux：`~/.qwen/settings.json`
    
-   Windows：`C:\Users\<Windows用户名>\.qwen\settings.json`
    

```
{
  "env": {
    "BAILIAN_CODING_PLAN_API_KEY": "YOUR_API_KEY"
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
      {
        "id": "qwen3.5-plus",
        "name": "[Bailian Coding Plan] qwen3.5-plus",
        "baseUrl": "https://coding.dashscope.aliyuncs.com/v1",
        "envKey": "BAILIAN_CODING_PLAN_API_KEY",
        "generationConfig": {
          "extra_body": {
            "enable_thinking": true
          }
        }
      },
      {
        "id": "qwen3-max-2026-01-23",
        "name": "[Bailian Coding Plan] qwen3-max-2026-01-23",
        "baseUrl": "https://coding.dashscope.aliyuncs.com/v1",
        "envKey": "BAILIAN_CODING_PLAN_API_KEY"
      },
      {
        "id": "qwen3-coder-next",
        "name": "[Bailian Coding Plan] qwen3-coder-next",
        "baseUrl": "https://coding.dashscope.aliyuncs.com/v1",
        "envKey": "BAILIAN_CODING_PLAN_API_KEY"
      },
      {
        "id": "qwen3-coder-plus",
        "name": "[Bailian Coding Plan] qwen3-coder-plus",
        "baseUrl": "https://coding.dashscope.aliyuncs.com/v1",
        "envKey": "BAILIAN_CODING_PLAN_API_KEY"
      },
      {
        "id": "MiniMax-M2.5",
        "name": "[Bailian Coding Plan] MiniMax-M2.5",
        "baseUrl": "https://coding.dashscope.aliyuncs.com/v1",
        "envKey": "BAILIAN_CODING_PLAN_API_KEY"
      },
      {
        "id": "glm-5",
        "name": "[Bailian Coding Plan] glm-5",
        "baseUrl": "https://coding.dashscope.aliyuncs.com/v1",
        "envKey": "BAILIAN_CODING_PLAN_API_KEY",
        "generationConfig": {
          "extra_body": {
            "enable_thinking": true
          }
        }
      },
      {
        "id": "glm-4.7",
        "name": "[Bailian Coding Plan] glm-4.7",
        "baseUrl": "https://coding.dashscope.aliyuncs.com/v1",
        "envKey": "BAILIAN_CODING_PLAN_API_KEY"
      },
      {
        "id": "kimi-k2.5",
        "name": "[Bailian Coding Plan] kimi-k2.5",
        "baseUrl": "https://coding.dashscope.aliyuncs.com/v1",
        "envKey": "BAILIAN_CODING_PLAN_API_KEY",
        "generationConfig": {
          "extra_body": {
            "enable_thinking": true
          }
        }
      }
    ]
  },
  "security": {
    "auth": {
      "selectedType": "openai"
    }
  },
  "codingPlan": {
    "region": "china"
  },
  "model": {
    "name": "qwen3.6-plus"
  },
  "$version": 3
}
```

### 按量计费

启动 Qwen Code 后输入 `/auth`，选择 **使用自己的 API Key** > **Standard API Key**，选择对应地域并输入[阿里云百炼 API Key](https://help.aliyun.com/zh/model-studio/get-api-key) 即可完成配置。可用模型请参考[OpenAI 兼容 - 支持的模型](https://help.aliyun.com/zh/model-studio/anthropic-api-messages#07833dedefft7)。

高级配置：通过 settings.json 配置文件

编辑或新建 `settings.json` 文件，将 `YOUR_API_KEY` 替换为阿里云百炼 API Key。文件路径如下：

-   macOS/Linux：`~/.qwen/settings.json`
    
-   Windows：`C:\Users\<Windows用户名>\.qwen\settings.json`
    

`baseUrl` 按地域设置，API Key 需与所选地域对应：

-   华北2（北京）：`https://dashscope.aliyuncs.com/compatible-mode/v1`
    
-   新加坡：`https://dashscope-intl.aliyuncs.com/compatible-mode/v1`
    
-   美国（弗吉尼亚）：`https://dashscope-us.aliyuncs.com/compatible-mode/v1`
    

```
{
  "env": {
    "BAILIAN_API_KEY": "YOUR_API_KEY"
  },
  "modelProviders": {
    "openai": [
      {
        "id": "qwen3.6-plus",
        "name": "[Bailian] qwen3.6-plus",
        "baseUrl": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "envKey": "BAILIAN_API_KEY",
        "generationConfig": {
          "extra_body": {
            "enable_thinking": true
          }
        }
      }
    ]
  },
  "security": {
    "auth": {
      "selectedType": "openai"
    }
  },
  "model": {
    "name": "qwen3.6-plus"
  },
  "$version": 3
}
```

如需添加[其他模型](https://help.aliyun.com/zh/model-studio/anthropic-api-messages#07833dedefft7)，在 `modelProviders.openai` 中以相同格式追加即可。

## **验证配置**

配置完成后，在项目目录下运行以下命令启动 Qwen Code，即可开始对话。

```
qwen
```

## Qwen Code IDE 插件

Qwen Code 支持在 VS Code 中以插件方式使用，在 IDE 中提供 AI 编程能力。

### VS Code

使用前请确保 VS Code 版本为 1.85.0 或更高版本。

1.  打开 VS Code，在扩展市场中搜索 `Qwen Code Companion` 并安装。
    
2.  CLI 和 IDE 插件共用同一个 `settings.json`。如果已按上方步骤完成配置，请跳过此步。否则请按照上方[配置接入凭证](#qc-config-h)章节进行配置。
    
3.  点击右上角图标启动 Qwen Code，通过输入或点击`/`，选择`Switch model`切换模型。
    

## **常见命令**

**说明**

以下命令适用于 Qwen Code CLI，IDE 插件仅支持部分命令，请以实际使用为准。

**命令**

**说明**

**示例**

`/model`

切换当前会话中使用的模型。

`/model`

`/auth`

更改认证方式。

`/auth`

`/init`

分析当前目录并创建初始上下文文件（QWEN.md），用于定义项目级指令和上下文。

`/init`

`/clear`

清除终端屏幕内容，开始全新对话。

`/clear`

`/compress`

用摘要替换聊天历史以节省 Token。

`/compress`

`/settings`

打开设置编辑器，可配置语言、主题等。

`/settings`

`/summary`

根据对话历史生成项目摘要。

`/summary`

`/resume`

恢复之前的对话会话。

`/resume`

`/stats`

显示当前会话的详细统计信息。

`/stats`

`/help`

显示可用命令的帮助信息。

`/help`或`/?`

`/quit`

退出 Qwen Code。

`/quit`

更多 Qwen Code 的进阶功能，可以参考 [Qwen Code 官方文档](https://qwenlm.github.io/qwen-code-docs/zh/users/features/commands/)。

## **使用案例**

### **接入百炼 CLI**

[百炼 CLI](https://bailian.console.aliyun.com/cli) 安装时会向 `~/.qwen/skills/bailian-cli/` 注册 Skill，Qwen Code 即可通过对话调用百炼能力，能力清单详见[百炼 CLI 控制台](https://bailian.console.aliyun.com/cli)。前置要求 [Node.js](https://nodejs.org/zh-cn/download) 18+。

1.  告诉 Qwen Code 安装百炼 CLI：
    
    ```
    请帮我全局安装阿里云百炼 CLI 命令行工具：npm install -g bailian-cli
    ```
    
2.  前往百炼控制台[获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，告诉 Qwen Code 配置：
    
    ```
    配置我的 API Key 是：sk-xxxxxxxxxxxxx
    ```
    
3.  直接用自然语言描述需求即可开始使用，例如：
    
    ```
    帮我生成 6 张亚马逊电商主图，产品是白色无线蓝牙耳机。
    ```
    ```
    帮我生成一段 30 秒的白色无线蓝牙耳机产品演示视频。
    ```
    

### **一句话复刻网站样式**

指定目标网站截图，Qwen Code 自动解析页面结构，生成高还原度的前端代码。

复刻以下网站的样式

![website](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6504883771/p1060998.png)

操作演示

**配置步骤**

1.  [安装并配置 Qwen Code](#ff6720b61fzuq)。
    
2.  在终端输入`qwen`进入 Qwen Code。
    
3.  输入以下内容安装插件，选择 `ui-design` 完成安装。
    
    ```
    /extensions install wshobson/agents
    ```
    
4.  输入以下内容安装 skill。
    
    ```
    查看我是否有find skills，没有就直接帮我安装：npx skills add https://github.com/vercel-labs/skills --skill find-skills -y -a qwen-code，然后帮我安装 web-component-design 到当前目录qwen code skills中。
    ```
    
5.  下载[website.png](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260318/ymehla/website.png)到项目目录，输入以下内容，将自动识别截图的布局、样式，生成网页代码。
    
    ```
    /skills web-component-design 根据这个技能，基于 @website.png 帮我复刻一个网页html，注意图片引用需有效。
    ```
    

### **为开源项目制作宣传视频**

给定开源项目仓库地址，即可一键生成专属宣传视频。

> 仓库地址为：[https://github.com/QwenLM/qwen-code](https://github.com/QwenLM/qwen-code)。

**配置步骤**

1.  [安装并配置 Qwen Code](#ff6720b61fzuq)。
    
2.  在终端输入`qwen`进入 Qwen Code。
    
3.  输入以下内容制作视频。
    
    ```
    基于这个技能 https://github.com/QwenLM/qwen-code-examples/blob/main/skills/oss-styles/SKILL.md，帮我为开源仓库：https://github.com/QwenLM/qwen-code 生成一个演示视频
    ```
    

## **了解更多**

-   Qwen Code 的子智能体、MCP、Skills 等高级功能，请参见[Qwen Code 官方文档](https://qwenlm.github.io/qwen-code-docs/zh/users/overview/)。
    
-   Qwen Code 的使用案例，请参见[使用案例](https://qwenlm.github.io/qwen-code-docs/zh/showcase/)。
    

## **常见问题**

### 错误码

配置过程中遇到报错，请参考对应计费方案的常见问题文档：

-   按量付费：[错误信息](https://help.aliyun.com/zh/model-studio/error-code)
    
-   Coding Plan：[Coding Plan 常见问题](https://help.aliyun.com/zh/model-studio/coding-plan-faq)
    
-   Token Plan 团队版：[Token Plan 团队版常见问题](https://help.aliyun.com/zh/model-studio/token-plan-faq)
    

### **如何切换模型？**

在 Qwen Code 中直接输入 `/model` 命令，即可从 `settings.json` 中已配置的模型列表中选择切换。如需添加新模型，请在 `settings.json` 的 `modelProviders` 中添加对应配置，然后重启 Qwen Code。
