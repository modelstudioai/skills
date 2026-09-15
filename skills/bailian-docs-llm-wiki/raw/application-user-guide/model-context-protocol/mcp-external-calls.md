# 外部调用

阿里云百炼提供了全周期 MCP 服务，既支持在平台内部（如智能体、工作流）进行配置，也支持通过外部调用集成至第三方应用或个人项目。针对外部调用场景，可以选择以下两种方式：

-   集成至第三方应用：支持一键自动配置到第三方应用，快速实现外部调用。
-   集成至个人项目：通过 MCP SDK 调用，实现灵活编码和深度定制。

## 开通 MCP 服务

**说明**百炼 MCP 服务已从旧版 SSE 协议升级为新版 Streamable HTTP 协议。请根据您的情况选择对应的操作步骤。

#### 首次开通（新用户）

1.  前往[阿里云百炼 MCP 广场](https://bailian.console.aliyun.com/cn-beijing/?spm=5176.21213303.aillm.1.1a232f3dAFihmQ&tab=app&scm=20140722.S_%E7%99%BE%E7%82%BCprompt._.RL_%E7%99%BE%E7%82%BCprompt-LOC_aillm-OR_chat-V_3-RC_llm#/mcp-market)选择 MCP 服务。以 Amap Maps 服务为例，点击卡片。
    
2.  点击**立即开通**，点击**确认开通**后即可开通 Amap Maps MCP 服务。
    
    **说明**阿里云百炼已部署云端的 Amap Maps MCP 服务，开通试用服务无需填写**AMAP\_MAPS\_API\_KEY**。如需商业化服务定制，也支持使用个人**AMAP\_MAPS\_API\_KEY**。
    
    如果涉及输入敏感信息，需通过创建 KMS 凭据进行加密。
    

#### 升级协议（已开通用户）

1.  前往[阿里云百炼 MCP 广场](https://bailian.console.aliyun.com/cn-beijing/?spm=5176.21213303.aillm.1.1a232f3dAFihmQ&tab=app&scm=20140722.S_%E7%99%BE%E7%82%BCprompt._.RL_%E7%99%BE%E7%82%BCprompt-LOC_aillm-OR_chat-V_3-RC_llm#/mcp-market)选择 MCP 服务。以 Amap Maps 服务为例，点击卡片。
2.  单击右侧**取消开通**，再单击**立即开通**，**确认开通**后即可更新 Amap Maps MCP 服务。

## 外部调用 MCP 服务

### 集成至第三方应用

阿里云百炼支持配置 MCP 服务至 Cherry Studio 和 Cursor，支持自动配置和手动配置。以 Amap Maps 服务为例。

#### Cherry Studio

1.  安装 [Cherry Studio](https://www.cherry-ai.com/)。
    
2.  进入 [Amap Maps MCP](https://bailian.console.aliyun.com/?tab=mcp&scm=20140722.S_%E7%99%BE%E7%82%BCprompt._.RL_%E7%99%BE%E7%82%BCprompt-LOC_aillm-OR_chat-V_3-RC_llm#/mcp-market/detail/amap-maps) 服务界面，在**外部调用**界面中选择 **Cherry Studio**。
    
    页面显示两种配置方式：**方法1 自动配置**，点击**一键配置至 Cherry Studio** 按钮；**方法2 手动配置**，获取 DASHSCOPE\_API\_KEY 并替换配置文件中的对应变量。
    
3.  点击**一键配置至 Cherry Studio**，选择 API Key，点击**确定**。
    
    弹出**选择 API Key 并配置至 Cherry Studio** 对话框，在列表中选择要使用的 API Key，点击**确定**。可以在弹出的 Cherry Studio 界面中看到所配置的 MCP 服务的详细信息。其中显示服务名称为 **AliyunBailianMCP\_amap-maps**，类型为**服务器发送事件 (sse)**，URL 为 MCP 服务地址，开关已开启。
    
4.  也可以手动配置 MCP 服务。在**外部调用**界面获取 DASHSCOPE\_API\_KEY 并复制配置文件。在 Cherry Studio 的 **MCP 设置**页面点击**添加服务器**\>**从JSON导入**，粘贴配置信息，点击**确定**。可以看到已配置的 MCP 服务列表，其中 **AliyunBailianMCP\_amap-maps** 已成功添加并启用。
    
5.  在 Cherry Studio 中使用 MCP 服务。新建话题，在下方选择**AliyunBailianMCP\_amap-maps** 服务。
    
    在弹出的 MCP 服务列表中，勾选 **AliyunBailianMCP\_amap-maps** 服务并确认。
    
6.  在对话框中输入`现在出发，从杭州萧山国际机场到杭州西湖景区。请你提供三种公共交通出行方案`，可以看到大模型成功调用了 MCP 工具来规划路线。
    
    > 若模型无法调用 MCP，请参考[常见问题](https://help.aliyun.com/zh/model-studio/mcp-external-calls#71be503ed7ucy)。
    

#### Cursor

1.  安装 [Cursor](https://cursor.com/)。
    
2.  进入 [Amap Maps MCP](https://bailian.console.aliyun.com/?tab=mcp&scm=20140722.S_%E7%99%BE%E7%82%BCprompt._.RL_%E7%99%BE%E7%82%BCprompt-LOC_aillm-OR_chat-V_3-RC_llm#/mcp-market/detail/amap-maps) 服务界面，在**外部调用**界面中选择 **Cursor**。
    
    页面显示两种配置方式：**方法1 自动配置**，点击**一键配置至 Cursor** 按钮；**方法2 手动配置**，获取 DASHSCOPE\_API\_KEY 并替换配置文件中的对应变量。
    
3.  点击**一键配置至Cursor**，选择 API Key，点击**确定**。在弹出的 Cursor 界面中点击 **Install**。
    
    界面显示 MCP Server 配置信息，包括名称 **AliyunBailianMCP\_amap-maps**、类型 **stdio**、命令 **npx** 等，确认无误后点击 **Install**。
    
    头像右下角状态显示为绿色即为安装成功。
    

### 通过 SDK 进行开发集成

通过 MCP SDK 调用阿里云百炼 MCP 服务，编码更加灵活。

以下示例使用 OpenAI SDK 与 MCP SDK 调用百炼联网搜索（WebSearch）MCP 服务，实现联网搜索。

1.  安装依赖。

```
pip install openai mcp
```

2.  [配置百炼 API Key 到环境变量](https://help.aliyun.com/zh/model-studio/first-api-call-to-qwen#fcceb7b5d2pqx)。
    
3.  代码示例如下：
    
    #### Python
    
    ```
    # -*- coding: utf-8 -*-
    # 使用 OpenAI SDK + MCP SDK 调用百炼联网搜索（WebSearch）MCP 服务
    import os
    import asyncio
    import json
    from openai import OpenAI
    from mcp.client.streamable_http import streamablehttp_client
    from mcp import ClientSession
    
    async def main():
        api_key = os.getenv("DASHSCOPE_API_KEY")
        if not api_key:
            print("错误：请设置环境变量 DASHSCOPE_API_KEY")
            return
        mcp_url = "https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp"
        headers = {"Authorization": f"Bearer {api_key}"}
        # 1. 连接 MCP Server，获取可用工具列表
        async with streamablehttp_client(mcp_url, headers=headers) as (read, write, _):
            async with ClientSession(read, write) as session:
                await session.initialize()
                tools_result = await session.list_tools()
                # 转换为 OpenAI function calling 格式
                openai_tools = []
                for tool in tools_result.tools:
                    openai_tools.append({
                        "type": "function",
                        "function": {
                            "name": tool.name,
                            "description": tool.description or "",
                            "parameters": tool.inputSchema or {"type": "object", "properties": {}},
                        },
                    })
                # 2. 调用 DashScope（OpenAI 兼容接口）
                client = OpenAI(
                    api_key=api_key,
                    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
                )
                messages = [{"role": "user", "content": "搜索一下阿里云百炼MCP的最新进展"}]
                print("正在联网搜索...")
                print("=" * 50)
                # 3. 多轮工具调用循环
                while True:
                    response = client.chat.completions.create(
                        model="qwen-max",
                        messages=messages,
                        tools=openai_tools or None,
                    )
                    choice = response.choices[0]
                    msg = choice.message
                    if not msg.tool_calls:
                        print(msg.content)
                        break
                    messages.append(msg)
                    for tc in msg.tool_calls:
                        args = json.loads(tc.function.arguments)
                        result = await session.call_tool(tc.function.name, args)
                        tool_content = ""
                        for block in result.content:
                            if hasattr(block, "text"):
                                tool_content += block.text
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tc.id,
                            "content": tool_content,
                        })
    
    if __name__ == "__main__":
        asyncio.run(main())
    ```
    
4.  运行代码，结果如下：
    

```
正在联网搜索...
==================================================
阿里云百炼 MCP（Model Context Protocol）是一项新推出的服务，允许用户在百炼平台上统一接入和管理 MCP 服务。最新进展包括：
1. 支持通过 MCP 广场一键开通多种 MCP 服务（如 Amap Maps、联网搜索等）。
2. 提供 Streamable HTTP 协议，支持外部应用通过标准 HTTP 调用。
3. 已与 Cherry Studio、Cursor 等主流工具集成，支持自动配置。
4. 开发者可通过 MCP SDK 灵活编码集成至自有项目。
```

## 常见问题

### 无法连接 MCP 服务怎么办？

1.  **未开通或者未升级 MCP 服务**：请确认已在百炼 MCP 广场开通或升级 MCP 服务，详情参见[开通 MCP 服务](https://help.aliyun.com/zh/model-studio/mcp-external-calls#17e41c39a9fnf)。
2.  **API Key 错误**：请确认使用了有效的百炼通用 API Key。
3.  **额度用尽**：部分 MCP （如联网搜索）存在每月额度限制，额度用尽后自动停止。

其他报错及常见问题请参考[常见问题](raw/application-user-guide/model-context-protocol/mcp-faq.md)。

### 模型正常对话且 MCP 无报错，但无法成功地调用 MCP 怎么办？

大模型需要明确的指令才能准确地调用 MCP 服务。请在提示词中明确工具名称和工具能力。示例：调用阿里云百炼 Amap Maps MCP 服务，规划从杭州到上海的自驾路线。
