# 工具接入

高代码应用通过 MCP（Model Context Protocol） 协议接入各类工具，为 AI Agent 扩展知识检索、外部服务调用、应用编排和数据访问能力。

## 概述

在高代码应用详情页的**工具**页面中，您可以添加和管理 Agent 使用的工具。添加的工具用于展示调用方式，开发者需要在代码中以 MCP 协议实际接入。

> 控制台中添加工具主要用于展示和管理，实际的工具调用逻辑需要在代码中通过 MCP 协议实现。

高代码应用支持以下四种工具类型：

**工具类型**

**说明**

**适用场景**

**知识库**

配置好的知识库可发布为 MCP 服务接入，为智能体提供补充知识以增强回复准确性。

产品文档问答、企业知识检索、FAQ 自动回复等需要特定领域知识的场景。

**MCP 服务**

通过插件转换或开通广场中的 MCP 服务，为智能体提供可使用的技能。

联网搜索、天气查询、金融数据分析、企业工商查询等外部服务调用场景。

**应用组件**

将已创建的智能体或工作流作为组件接入，为当前智能体提供更强大的能力。

多 Agent 协作、复杂任务编排、将已有的工作流复用到高代码应用中。

**数据连接器**

百炼平台上访问外部数据的桥梁，提供企业级的稳定、安全的数据服务。

读取表格数据、文件处理、企业数据库对接等外部数据访问场景。

## 推荐项目结构

一个规范的高代码应用项目推荐使用该项目结构：[tool\_use\_demo.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260422/bfethg/tool_use_demo.zip)。

```
my-agent-app/
├── main.py              # 入口文件（必须，程序启动入口）
├── requirements.txt     # Python 依赖声明
├── tools/               # 工具函数模块（按功能分类）
│   ├── search.py        # 搜索工具
│   ├── knowledge.py     # 知识库工具
│   └── data.py          # 数据连接工具
├── prompts/             # 系统提示词模板
│   └── system.txt
└── utils/               # 通用工具类
    └── helpers.py
```

其中 `requirements.txt` 建议使用 `==` 固定所有依赖的版本号，避免使用 `>=` 等范围约束符。固定版本可确保每次构建的依赖环境一致，防止因上游依赖更新导致构建失败或运行异常。

## 接入流程

工具接入高代码应用分为以下三个步骤：

1.  **Step 1：添加工具**
    
    在高代码应用详情页的**工具**页面中，选择所需的工具类型（知识库、MCP 服务、应用组件或数据连接器），单击对应区域的 **+** 按钮，在弹出的面板中搜索并添加工具。
    
2.  **Step 2：代码接入**
    
    添加工具后，系统会自动配置相关环境变量。在代码中通过 `fastmcp.Client` 连接 MCP 服务并调用工具。示例：
    

```
import os
from agentscope.message import TextBlock
from agentscope.tool import ToolResponse
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport

async def web_search(query: str) -> ToolResponse:
    """通过 MCP 服务调用联网搜索工具。

    Args:
        query: 搜索关键词。

    Returns:
        ToolResponse with search results.
    """
    api_key = os.environ.get("DASHSCOPE_API_KEY")
    transport = StreamableHttpTransport(
        _MCP_URL="https://dashscope.aliyuncs.com/api/v1/mcps/{mcpCode}/mcp",
        headers={"Authorization": f"Bearer {api_key}"},
    )
    async with Client(transport=transport) as client:
        result = await client.call_tool("{toolName}", {"query": query})
    if result and result.content:
        text = "\n".join(
            block.text for block in result.content if hasattr(block, "text")
        )
    else:
        text = "No results found."
    return ToolResponse(content=[TextBlock(type="text", text=text)])
```

3.  **Step 3：部署验证**
    
    重新部署应用使工具生效，然后在右侧的**API 测试**或**文本对话体验**中验证工具调用是否正常。
    

## 知识库

知识库为 Agent 提供特定领域的补充知识，增强回复准确性。配置好的知识库需先发布为 MCP 服务，才能被高代码应用调用。

**添加知识库**

1.  在**工具**页面的**知识库**区域，单击 **+** 按钮，打开**选择知识库**面板。
2.  在面板中搜索或浏览已有知识库，单击**添加**将其关联到当前应用。如需新建知识库，单击**创建知识库**。
3.  添加完成后，知识库会显示在工具列表中，切换到**已添加** Tab 可查看当前已关联的知识库。

**代码接入示例**
```
import os
from agentscope.message import TextBlock
from agentscope.tool import ToolResponse
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport

async def search_knowledge(query: str, top_k: int = 5) -> ToolResponse:
    """在产品文档知识库中检索相关内容。

    Args:
        query: 用户的搜索问题。
        top_k: 返回的文档数量，默认 5。

    Returns:
        ToolResponse with retrieved documents.
    """
    api_key = os.environ.get("DASHSCOPE_API_KEY")
    # 知识库发布为 MCP 服务后，从工具页面获取对应的 mcpCode
    transport = StreamableHttpTransport(
        _MCP_URL="https://dashscope.aliyuncs.com/api/v1/mcps/{知识库mcpCode}/mcp",
        headers={"Authorization": f"Bearer {api_key}"},
    )
    async with Client(transport=transport) as client:
        result = await client.call_tool("retrieve", {
            "query": query,
            "top_k": top_k
        })
    if result and result.content:
        text = "\n".join(
            block.text for block in result.content if hasattr(block, "text")
        )
    else:
        text = "未找到相关文档。"
    return ToolResponse(content=[TextBlock(type="text", text=text)])
```

## MCP 服务

MCP 服务为 Agent 提供外部技能调用能力。您可以从 MCP 广场开通现成的服务，也可以创建自定义 MCP 服务或从已有插件转换。

**添加 MCP 服务**

1.  在**工具**页面的**MCP** 区域，单击 **+** 按钮，打开**选择 MCP 服务**面板。
    
2.  在面板中选择 MCP 服务来源：
    
    -   **MCP 广场**：浏览和开通平台提供的 MCP 服务（如联网搜索、金融数据分析、企业工商查询等），支持按"已开通"和"未开通"筛选。
    -   **自定义 MCP**：添加自行创建的 MCP 服务，或通过**从插件转 MCP**将已有插件转换为 MCP 服务。
3.  选择所需的 MCP 服务，单击**添加**或**立即开通**完成配置。
    

**代码接入示例**
```
import os
from agentscope.message import TextBlock
from agentscope.tool import ToolResponse
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport

async def web_search(query: str) -> ToolResponse:
    """通过 MCP 广场的联网搜索服务查询实时信息。

    Args:
        query: 搜索关键词。

    Returns:
        ToolResponse with search results.
    """
    api_key = os.environ.get("DASHSCOPE_API_KEY")
    # 从 MCP 广场开通服务后，获取对应的 mcpCode
    transport = StreamableHttpTransport(
        _MCP_URL="https://dashscope.aliyuncs.com/api/v1/mcps/{MCP服务mcpCode}/mcp",
        headers={"Authorization": f"Bearer {api_key}"},
    )
    async with Client(transport=transport) as client:
        result = await client.call_tool("web_search", {"query": query})
    if result and result.content:
        text = "\n".join(
            block.text for block in result.content if hasattr(block, "text")
        )
    else:
        text = "No results found."
    return ToolResponse(content=[TextBlock(type="text", text=text)])
```

## 应用组件

应用组件允许您将已创建的智能体或工作流作为子组件接入当前高代码应用，实现多 Agent 协作和复杂任务编排。

**添加应用组件**

1.  在**工具**页面的**应用组件**区域，单击 **+** 按钮，打开**选择应用组件**面板。
2.  在面板中搜索或浏览已有的智能体和工作流应用，单击**添加**将其作为组件接入。如需新建应用，单击**创建应用**。
3.  添加完成后，可在**已添加** Tab 中查看当前已关联的应用组件。

**代码接入示例**
```
import os
from agentscope.message import TextBlock
from agentscope.tool import ToolResponse
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport

async def call_translation_agent(text: str, target_lang: str = "en") -> ToolResponse:
    """调用翻译智能体将文本翻译为目标语言。

    Args:
        text: 待翻译的文本内容。
        target_lang: 目标语言代码，如 en、ja、ko。

    Returns:
        ToolResponse with translation result.
    """
    api_key = os.environ.get("DASHSCOPE_API_KEY")
    # 应用组件对应的 mcpCode
    transport = StreamableHttpTransport(
        _MCP_URL="https://dashscope.aliyuncs.com/api/v1/mcps/{应用组件mcpCode}/mcp",
        headers={"Authorization": f"Bearer {api_key}"},
    )
    async with Client(transport=transport) as client:
        result = await client.call_tool("translate", {
            "text": text,
            "target_lang": target_lang
        })
    if result and result.content:
        translated = "\n".join(
            block.text for block in result.content if hasattr(block, "text")
        )
    else:
        translated = "翻译失败。"
    return ToolResponse(content=[TextBlock(type="text", text=translated)])
```

## 数据连接器

数据连接器是百炼平台上 Agent、工作流、知识库等访问外部数据的桥梁，提供企业级的稳定、安全的数据服务。

> 数据文件会在公网传递，请不要通过数据连接器传输敏感数据。

**添加数据连接器**

1.  在**工具**页面的**数据连接器**区域，单击 **+** 按钮，打开**选择数据连接器**面板。
    
2.  在面板中选择数据连接器。平台默认提供两种连接器：
    
    -   **默认表格连接器**：用于读取和处理表格类数据（如 CSV、Excel）。
    -   **默认文件连接器**：用于读取和处理各类文件数据。
3.  单击**添加**完成配置。如需自定义连接器，单击**创建连接器**。
    

**代码接入示例**
```
import os
from agentscope.message import TextBlock
from agentscope.tool import ToolResponse
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport

async def query_sales_data(start_date: str, end_date: str) -> ToolResponse:
    """通过数据连接器查询指定时间范围的销售数据。

    Args:
        start_date: 起始日期，格式 YYYY-MM-DD。
        end_date: 结束日期，格式 YYYY-MM-DD。

    Returns:
        ToolResponse with query results.
    """
    api_key = os.environ.get("DASHSCOPE_API_KEY")
    # 数据连接器对应的 mcpCode
    transport = StreamableHttpTransport(
        _MCP_URL="https://dashscope.aliyuncs.com/api/v1/mcps/{数据连接器mcpCode}/mcp",
        headers={"Authorization": f"Bearer {api_key}"},
    )
    async with Client(transport=transport) as client:
        result = await client.call_tool("query_data", {
            "start_date": start_date,
            "end_date": end_date
        })
    if result and result.content:
        text = "\n".join(
            block.text for block in result.content if hasattr(block, "text")
        )
    else:
        text = "未找到相关数据。"
    return ToolResponse(content=[TextBlock(type="text", text=text)])
```

## MCP 协议开发要点

所有工具都通过 MCP（Model Context Protocol）协议接入。以下是开发 MCP 工具时的关键要点。

### 工具命名与描述

工具函数的名称和文档字符串直接影响大模型判断何时调用该工具，应准确描述工具的功能和适用场景。

```
# 好的命名 — 函数名和文档字符串清晰描述工具用途
async def search_product_docs(query: str, top_k: int = 5) -> ToolResponse:
    """在产品文档知识库中搜索与用户问题相关的技术文档和操作指南，
    适用于回答产品功能、配置方法、故障排查等问题。"""
    ...

# 不好的命名 — 过于笼统，大模型难以判断使用场景
async def search(q: str) -> ToolResponse:
    """搜索工具。"""
    ...
```

### 参数定义

为每个参数提供清晰的类型标注和文档说明，帮助大模型正确提取和传递参数值。

```
async def get_weather(city: str, unit: str = "celsius") -> ToolResponse:
    """查询指定城市的当前天气信息。

    Args:
        city: 城市名称，如'杭州'、'北京'。
        unit: 温度单位，celsius 或 fahrenheit，默认 celsius。
    """
    ...
```

### 错误处理

工具函数应当妥善处理异常情况，返回有意义的错误信息，而不是让异常直接抛出导致对话中断。

```
async def query_database(sql: str) -> ToolResponse:
    """查询业务数据库。"""
    try:
        api_key = os.environ.get("DASHSCOPE_API_KEY")
        transport = StreamableHttpTransport(
            _MCP_URL="https://dashscope.aliyuncs.com/api/v1/mcps/{mcpCode}/mcp",
            headers={"Authorization": f"Bearer {api_key}"},
        )
        async with Client(transport=transport) as client:
            result = await client.call_tool("query_db", {"sql": sql})
        text = "\n".join(
            block.text for block in result.content if hasattr(block, "text")
        )
        return ToolResponse(content=[TextBlock(type="text", text=text)])
    except ConnectionError:
        return ToolResponse(content=[
            TextBlock(type="text", text="数据服务暂时不可用，请稍后重试")
        ])
    except Exception as e:
        return ToolResponse(content=[
            TextBlock(type="text", text=f"查询失败：{e}")
        ])
```

## 环境变量

添加工具后，系统会自动将相关的连接信息通过环境变量注入到运行环境中。以下是常用的系统环境变量：

**环境变量**

**说明**

`DASHSCOPE_API_KEY`

百炼平台 API Key，用于调用模型服务和工具 API。

`DASHSCOPE_API_HEADERS`

API 请求附加的 Header 信息。

`PATH`

系统路径变量，包含 Python 运行环境路径。

`PYTHONPATH`

Python 模块搜索路径。

`TZ`

时区设置。

> 您可以在**部署**页面的**环境变量**区域查看和编辑所有环境变量。添加工具后自动注入的环境变量也可在此处确认。

## 常见问题

**Q：控制台中添加的工具和代码中的工具有什么关系？**

A：控制台中添加工具主要用于展示调用方式和管理工具的关联关系，同时系统会自动注入相关的环境变量。实际的工具调用逻辑需要在代码中通过 MCP 协议实现。

**Q：知识库如何接入高代码应用？**

A：知识库需要先在百炼平台创建并配置好，然后在**工具**页面添加到应用中。添加后，系统会自动注入知识库的连接信息（如 Endpoint、ID 等），您需要在代码中通过 `fastmcp.Client` 调用知识库的 MCP 服务实现检索逻辑。

**Q：MCP 广场的服务如何使用？**

A：在 MCP 广场中找到所需服务，单击**立即开通**激活服务，然后在**工具**页面将其添加到应用中。开通后的 MCP 服务会提供标准的调用接口，在代码中通过环境变量获取连接信息并调用。

**Q：添加工具后需要重新部署吗？**

A：是的。添加或移除工具后需要重新部署应用，新的环境变量和工具配置才会生效。

**Q：工具的 description 为什么很重要？**

A：大模型通过工具的 `description` 来判断何时调用该工具。描述应包含工具的功能、适用场景和输入输出说明，避免过于笼统（如"搜索工具"），否则大模型可能无法正确选择工具。
