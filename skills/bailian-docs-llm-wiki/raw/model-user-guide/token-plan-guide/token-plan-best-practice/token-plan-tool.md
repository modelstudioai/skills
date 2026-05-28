# 工具调用

Token Plan 团队版支持通过模型内置工具和 MCP 服务两种方式为 AI 编程工具扩展能力，如联网搜索、代码解释器、网页抓取等。

## **工具概览**

Token Plan 团队版提供两种方式接入工具：

-   **模型内置工具**：qwen3.7-max、qwen3.6-plus、qwen3.6-flash 模型的 Responses API 内置了联网搜索、代码解释器、网页抓取、以图搜图、文搜图五种工具。启用后，模型会在需要时自动调用相应工具。
    
-   **MCP 服务**：其他模型（如 deepseek-v3.2、glm-5 等）可通过百炼 MCP 广场的 MCP 服务获取工具能力。本文以联网搜索 MCP 为例说明接入方式，其他 MCP 服务的接入方式类似。
    

## **费用说明**

### **模型内置工具**

qwen3.7-max、qwen3.6-plus、qwen3.6-flash 模型内置工具的费用可通过 Token Plan 团队版抵扣，内置工具不额外收费，产生的 token 消耗统一从套餐 Credits 中抵扣。具体价格以[控制台模型详情页](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market/detail/qwen3.6-plus)为准。

### **MCP 服务**

百炼 MCP 广场提供联网搜索、代码解释器、网页抓取等 MCP 服务，部分服务**限时免费**，每月提供一定免费额度。具体价格以[MCP 广场](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/mcp-market)各服务详情页为准。

## **使用方式**

### **使用 qwen3.7-max / qwen3.6-plus / qwen3.6-flash 模型内置工具**

将 AI 工具的模型设置为 `qwen3.7-max`、`qwen3.6-plus` 或 `qwen3.6-flash`，在对话中直接提问即可。模型会根据问题自动调用相应的内置工具：

**工具**

**说明**

联网搜索

检索互联网信息，结合搜索结果生成回答

代码解释器

调用模型时启用内置的 Python 代码解释器，可使模型在沙箱环境里编写与运行 Python 代码，以解决数学计算、数据分析等复杂问题。

网页抓取

网页抓取工具可以访问指定 URL 并提取内容，为大模型提供所需信息。

以图搜图

图搜图工具使模型能够根据输入图片从互联网搜索视觉相似的图片，并基于搜索结果进行分析和推理，适用于以图找同款、视觉内容溯源等场景。

文搜图

文搜图工具使模型能够根据文本描述从互联网搜索相关图片，并基于图片内容进行描述和推理，适用于可视化问答、配图推荐等场景。

### **通过 MCP 服务接入工具**

其他模型可通过百炼 MCP 广场的 MCP 服务获取工具能力。以下以联网搜索 MCP 为例说明接入方式。

#### **前提条件**

已获取[百炼 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。此处的 API Key 为百炼通用 API Key（格式为 sk-xxx），用于调用 MCP 服务，与 Token Plan 团队版专属 API Key（格式为 sk-sp-xxx）不同。

#### **开通 MCP 服务**

1.  进入百炼的[MCP 广场](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/mcp-market)，找到需要的 MCP 服务（如联网搜索）。
    
2.  点击**立即开通**，确认开通。
    
3.  开通成功后，获取以下配置信息：
    
    -   **Streamable HTTP Endpoint**：MCP 服务的连接地址。
        
    -   **API Key**：即百炼 API Key，是 MCP 服务的鉴权密钥。
        

#### **接入工具**

将 MCP 服务添加到 AI 编程工具中。以下以联网搜索 MCP 为例，示例中的 `YOUR_API_KEY` 需替换为百炼 API Key。接入其他 MCP 服务时，将 Endpoint 地址替换为对应服务的地址即可。

## OpenClaw

1.  在终端执行如下命令安装 MCPorter。
    
    ```
    npm install -g mcporter
    ```
    
2.  在终端执行如下命令启用 MCPorter。
    
    ```
    openclaw config set skills.entries.mcporter.enabled true
    ```
    
3.  在 `~/.openclaw/workspace` 目录下，执行如下命令添加联网搜索 MCP。
    
    ```
    mcporter config add WebSearch https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp --transport http --header "Authorization=Bearer YOUR_API_KEY"
    ```
    
4.  执行如下命令确认 MCP 已安装。
    
    ```
    mcporter list
    ```
    
5.  执行如下命令使配置生效。
    
    ```
    openclaw gateway restart
    ```
    
6.  发送提问 `用 mcporter 搜索阿里云的新闻` 即可看到搜索结果。
    

## OpenCode

1.  在配置文件 `~/.config/opencode/opencode.json` 中写入 MCP 配置信息。
    
    ```
    {
      "mcp": {
        "WebSearch": {
          "type": "remote",
          "httpUrl": "https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp",
          "headers": {
            "Authorization": "Bearer YOUR_API_KEY"
          }
        }
      }
    }
    ```
    
    若 `opencode.json` 中已有其他配置（如 provider），将 mcp 字段合并到现有配置中即可。
    
2.  在终端执行以下命令进入 OpenCode。
    
    ```
    opencode
    ```
    
3.  在对话框执行 `/mcps` 确认 `websearch` 状态为 Enabled。确认后按 Esc 退出。
    
4.  发送提问 `用 websearch MCP 搜索阿里云的新闻` 即可看到搜索结果。
    
    > 为了避免和其他工具混淆，建议提问时明确提及 websearch MCP。
    

## Claude Code

1.  在终端执行以下命令添加联网搜索 MCP 服务。
    
    ```
    claude mcp add WebSearch https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp -t http -H "Authorization: Bearer YOUR_API_KEY"
    ```
    
    终端返回 `Added SSE MCP server xx` 即表示添加成功。
    
2.  执行以下命令进入 Claude Code。
    
    ```
    claude
    ```
    
3.  在对话框执行 `/mcp` 命令，确认 `websearch` 的状态为 connected。
    
4.  按 Esc 退出 MCP 列表后，发送提问 `用 websearch MCP 搜索阿里云的新闻` 即可看到搜索结果。
    
    > 为了避免和其他工具混淆，建议提问时明确提及 websearch MCP。
    

## Qwen Code

1.  在终端执行以下命令添加联网搜索 MCP。
    
    ```
    qwen mcp add WebSearch \
      -t http \
      "https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp" \
      -H "Authorization: Bearer YOUR_API_KEY"
    ```
    
2.  在终端执行以下命令进入 Qwen Code。
    
    ```
    qwen
    ```
    
3.  在对话框执行 `/mcp` 命令确认 MCP 连接状态。
    
4.  发送提问 `用 websearch MCP 搜索阿里云的新闻` 即可看到搜索结果。
    
    > 为了避免和其他工具混淆，建议提问时明确提及 websearch MCP。
    

## Kilo CLI

1.  在配置文件 `~/.config/kilo/opencode.json` 中写入 MCP 配置信息。
    
    ```
    {
      "mcp": {
        "websearch": {
          "type": "remote",
          "url": "https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp",
          "headers": {
            "Authorization": "Bearer YOUR_API_KEY"
          }
        }
      }
    }
    ```
    
    若 `opencode.json` 中已有其他配置（如 provider），将 mcp 字段合并到现有配置中即可。
    
2.  在终端执行以下命令查看 MCP 状态。Connected 即表示连接成功。
    
    ```
    kilocode mcp list
    ```
    
3.  在终端执行以下命令进入 Kilo CLI。
    
    ```
    kilo
    ```
    
4.  发送提问 `用 websearch MCP 搜索阿里云的新闻` 即可看到搜索结果。
    
    > 为了避免和其他工具混淆，建议提问时明确提及 websearch MCP。
    

## Kilo Code IDE 插件

1.  打开 Kilo Code IDE 插件，配置联网搜索 MCP 信息。
    
    ```
    {
      "mcpServers": {
        "websearch": {
          "type": "streamable-http",
          "url": "https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp",
          "headers": {
            "Authorization": "Bearer YOUR_API_KEY"
          }
        }
      }
    }
    ```
    
    当联网搜索的 MCP 状态显示为绿色时，表示添加成功。
    
2.  返回对话界面，发送提问 `用 websearch MCP 搜索阿里云的新闻` 即可看到搜索结果。
    
    > 为了避免和其他工具混淆，建议提问时明确提及 websearch MCP。
