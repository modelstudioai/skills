# 联网搜索

在 Coding Plan 支持的编程工具中添加联网搜索工具，使模型能够检索实时信息。

## 适用范围

本文适用于需要通过 MCP 扩展联网搜索能力的工具，如 Qwen Code、Claude Code 等。部分工具（如 Cursor）已内置联网搜索功能，无需额外添加联网搜索服务。

## 前提条件

1.  已订阅 [Coding Plan](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/coding_plan)，详情请参见[快速开始](https://help.aliyun.com/zh/model-studio/coding-plan-quickstart)。
    
2.  已在 Coding Plan 工具（如 Claude Code、Qwen Code）中完成接入配置，且能正常对话，详情请参见[接入客户端/开发工具](https://help.aliyun.com/zh/model-studio/use-chat-client-or-development-tool/)。
    
3.  已获取[百炼 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。此处的 API Key 为百炼通用 API Key（格式为 sk-xxx），用于调用 MCP 服务，与 Coding Plan 专属 API Key（格式为 sk-sp-xxx）不同。
    

## 开通或升级联网搜索 MCP

联网搜索 MCP 已从旧版 SSE 协议升级为新版 Streamable HTTP 协议。请根据您的情况选择对应的操作步骤：

### **首次开通（新用户）**

1.  进入百炼的[MCP广场](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/mcp-market)，找到**联网搜索** MCP 服务。
    
2.  单击**立即开通** > **确认开通**。
    
    -   联网搜索、网页抓取、代码解释器等 MCP 服务**限时免费**，每月 2000 次免费额度。如果使用第三方MCP服务，该MCP服务可能收费，以MCP服务的介绍信息为准。
        
3.  开通成功后，可以获取以下配置信息：
    
    1.  **Streamable HTTP Endpoint**：MCP 服务的连接地址。联网搜索 MCP 的连接地址为`https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp`。
        
    2.  **API Key**：即百炼 API Key，是 MCP 服务的鉴权密钥。
        

## **升级协议（已开通用户）**

1.  进入百炼的[MCP广场](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/mcp-market)，找到**联网搜索** MCP 服务。
    
2.  单击右侧**取消开通**，再单击**立即开通**。
    
    -   联网搜索、网页抓取、代码解释器等 MCP 服务**限时免费**，每月 2000 次免费额度。如果使用第三方MCP服务，该MCP服务可能收费，以MCP服务的介绍信息为准。
        
3.  重新开通成功后，即完成协议升级，可以获取以下配置信息：
    
    1.  **Streamable HTTP Endpoint**：MCP 服务的连接地址。联网搜索 MCP 的连接地址为`https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp`。
        
    2.  **API Key**：即百炼 API Key，是 MCP 服务的鉴权密钥。
        

## **接入工具**

将 MCP 服务添加到 AI 编程工具中。

## OpenClaw

1.  在终端执行如下命令安装 MCPorter。
    
    ```
    npm install -g mcporter
    ```
    
2.  在终端执行如下命令，启用 MCPorter。
    
    ```
    openclaw config set skills.entries.mcporter.enabled true
    ```
    
3.  在`~/.openclaw/workspace`目录下，执行如下命令。执行命令前，将命令中的 YOUR\_API\_KEY 替换为[开通或升级联网搜索 MCP](#da7cd47fa8pcd)时获取的阿里云百炼 API Key。
    
    ```
    mcporter config add WebSearch https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp --transport http --header "Authorization=Bearer YOUR_API_KEY" --scope home
    ```
    
4.  在`~/.openclaw/workspace`目录下，执行如下命令确认MCP已安装。
    
    ```
    mcporter list
    ```
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9753812771/p1055340.png)
    
5.  在终端执行如下命令使配置生效。
    
    ```
    openclaw gateway restart
    ```
    
6.  发送提问`用 mcporter 搜索阿里云的新闻`即可看到搜索结果。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9753812771/p1055129.png)
    

## OpenCode

1.  在 OpenCode 配置文件`~/.config/opencode/opencode.json`中写入 MCP 配置信息，并将`YOUR_API_KEY`替换为上一步骤获取的 API Key。
    
    ```
    {
      "mcp": {
        "WebSearch": {
          "type": "remote",
          "url": "https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp",
          "headers": {
            "Authorization": "Bearer YOUR_API_KEY"
          }
        }
      }
    }
    ```
    
    若`opencode.json`中已有其他配置（如 provider），将 mcp 字段合并到现有配置中即可。配置完成后，保存文件。
    
2.  在终端中执行以下命令进入 OpenCode。
    
    ```
    opencode
    ```
    
3.  在对话框执行`/mcps`确认`websearch`状态是否为 Enabled。确认后按 Esc 退出。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4753812771/p1054875.png)
    
4.  发送提问`用websearch MCP搜索阿里云的新闻`即可看到搜索结果。
    
    > 为了避免和其他工具混淆，建议提问时明确提及 websearch MCP。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9228202771/p1054876.png)
    

## Claude Code

1.  添加联网搜索MCP服务。
    
    1.  将以下命令复制到终端。
        
        ```
        claude mcp add WebSearch https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp -t http -H "Authorization: Bearer YOUR_API_KEY"
        ```
        
    2.  将命令中的 YOUR\_API\_KEY 替换为[开通或升级联网搜索 MCP](#da7cd47fa8pcd)时获取的阿里云百炼 API Key。
        
    3.  在终端执行更新后的命令。
        
        **说明**
        
        终端返回`Added HTTP MCP server WebSearch with URL: ... to local config`并不代表 MCP 添加成功，其连接状态需通过以下步骤确认。
        
2.  在终端执行以下命令进入 Claude Code。
    
    ```
    claude
    ```
    
3.  在对话框执行`/mcp`命令，确认`websearch`的状态为 connected。首次添加可能需要等待状态从 connecting 变成 connected。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9276802771/p1054987.png)
    
    若连接状态显示 failed，请选中该 MCP 并选择 Reconnect 重连。若重试 1-2 次仍失败，请核实配置。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0613342771/p1055684.png)
    
4.  按 Esc 退出 MCP 列表后，发送提问`用websearch MCP搜索阿里云的新闻`即可看到搜索结果。
    
    > 为了避免和其他工具混淆，建议提问时明确提及 websearch MCP。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9276802771/p1054990.png)
    

## Qwen Code

1.  添加联网搜索 MCP。
    
    1.  将以下命令复制到终端。
        
        ```
        qwen mcp add WebSearch \
          -t http \
          "https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp" \
          -H "Authorization: Bearer YOUR_API_KEY"
        ```
        
    2.  将命令中的 YOUR\_API\_KEY 替换为[开通或升级联网搜索 MCP](#da7cd47fa8pcd)时获取的阿里云百炼 API Key。
        
    3.  在终端执行更新后的命令。
        
        **说明**
        
        终端返回`MCP server "WebSearch" added to user settings. (http)`并不代表 MCP 添加成功，其连接状态需通过以下步骤确认。
        
2.  在终端执行以下命令进入 Qwen Code。
    
    ```
    qwen
    ```
    
3.  在`Qwen Code`对话框执行`/mcp`命令以确认 MCP 连接状态。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4753812771/p1054878.png)
    
4.  发送提问`用 websearch MCP 搜索阿里云的新闻`即可看到搜索结果。
    
    > 为了避免和其他工具混淆，建议提问时明确提及`websearch MCP`。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9228202771/p1054879.png)
    

## Kilo CLI

1.  在配置文件`~/.config/kilo/opencode.json`中写入 MCP 配置信息，并将`YOUR_API_KEY`替换为上一步骤获取的 API Key。配置完成后，保存文件。
    
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
    
    若`opencode.json`中已有其他配置（如 provider），将 mcp 字段合并到现有配置中即可。配置完成后，保存文件。
    
2.  在终端中执行以下命令查看 MCP 状态。Connected 即表示连接成功。
    
    ```
    kilocode mcp list
    ```
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0248612771/p1055115.png)
    
3.  在终端中执行以下命令进入 Kilo CLI。
    
    ```
    kilo
    ```
    
4.  发送提问`用websearch MCP搜索阿里云的新闻`即可看到搜索结果。
    
    > 为了避免和其他工具混淆，建议提问时明确提及 websearch MCP。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9228202771/p1054891.png)
    

## Kilo Code IDE 插件

1.  打开Kilo Code IDE插件配置联网搜索 MCP 信息，并将`YOUR_API_KEY`替换为上一步骤获取的 API Key。配置完成后，保存文件。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3100902771/p1055026.png)
    
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
    
    当联网搜索的MCP状态显示为绿色时，表示添加成功。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3100902771/p1055021.png)
    
2.  返回对话界面，发送提问`用websearch MCP搜索阿里云的新闻`即可看到搜索结果。
    
    > 为了避免和其他工具混淆，建议提问时明确提及 websearch MCP。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3100902771/p1055023.png)
    

## 常见问题

### 无法连接联网搜索 MCP 服务怎么办？

常见原因及排查方式：

1.  **未开通或者未升级联网搜索 MCP 服务**：请确认已在百炼 MCP 广场开通或升级联网搜索 MCP 服务，详情请参见[开通或升级联网搜索 MCP](#da7cd47fa8pcd)。
    
2.  **Streamable HTTP Endpoint 地址错误**：
    
    -   请检查 URL 是否拼写正确，完整 URL 为 `https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp`。
        
    -   如果使用的 URL 为 `https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/sse`，说明开通的是旧版 SSE 协议，请将协议[升级至Streamable HTTP](#da7cd47fa8pcd)。
        
3.  **API Key 错误**：请确认使用了有效的百炼通用 API Key（格式为 sk-xxx，非 Coding Plan 专属 API Key），并已在命令中正确替换 YOUR\_API\_KEY。
    
4.  **免费额度用尽**：联网搜索 MCP 每月有 2000 次免费额度，额度用尽后自动停止。
    
5.  **网络不通**：确认当前网络可以访问。
    

### **对话中模型没有调用联网搜索**怎么办？

1.  请确保联网搜索 MCP 服务连接成功并可用。
    
2.  在对话中明确提及工具名称，例如：`用 websearch MCP 搜索阿里云的新闻`。
