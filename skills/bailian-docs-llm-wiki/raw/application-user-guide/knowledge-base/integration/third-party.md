# 第三方平台接入

将 RAG 知识库接入 Dify、Coze、n8n、LangChain 等平台

## Dify

Dify 支持通过外部知识库（External Knowledge）接入。

1.  **获取 API 信息**
    
    在阿里云百炼控制台 [**服务渠道**](https://bailian.console.aliyun.com/cn-beijing/rag/channel) 页面，复制 Dash API 的 Endpoint 和 API Key。
    
2.  **配置 Dify**
    
    进入 Dify 的 **知识库** 设置，选择 **外部知识库**，填写：
    
    -   API Endpoint：DashScope 检索接口地址
    -   API Key：你的 DashScope API Key
    -   知识库 ID：目标知识库 ID
3.  **在工作流中使用**
    
    在 Dify 工作流或对话应用中，选择该外部知识库作为检索源。
    

## Coze

Coze 支持通过 MCP 或自定义 API 插件接入。

**方式一：MCP 接入**

在 Coze 的 Bot 设置中添加 MCP 工具：

1.  选择 **添加 MCP 工具**
2.  填写 MCP Server URL 和认证信息（从控制台 [服务渠道](https://bailian.console.aliyun.com/cn-beijing/rag/channel) 页面获取）
3.  选择要暴露的检索 / 问答能力

**方式二：API 插件**

1.  在 Coze 中创建自定义插件
2.  配置 HTTP 请求指向 DashScope 检索接口
3.  映射输入参数（`query`、`top_k`）和输出参数（切片列表）

## n8n

n8n 可通过 HTTP Request 节点调用 RAG 检索接口：

1.  添加 **HTTP Request** 节点
2.  方法选 POST，URL 填检索接口地址（见下方说明）
3.  在 Headers 中添加 `Authorization: Bearer <API-Key>`
4.  Body 填写检索参数

**两种接口可选：**

-   **知识搜索**（应用级，推荐）：`https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/indices/knowledge/search`，参数为 `query` 和 `agent_id`，检索策略由知识检索服务配置驱动
-   **底层检索**：`https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/indices/rag/index/retrieve`，参数为 `index_id`、`query`、`top_k`，直接指定知识库 ID

## LangChain

在 LangChain 中作为自定义 Retriever 使用：

```
import requests

class DashScopeRetriever:
    def __init__(self, api_key, index_id):
        self.api_key = api_key
        self.index_id = index_id

    def get_relevant_documents(self, query):
        resp = requests.post(
            "https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/indices/rag/index/retrieve",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "index_id": self.index_id,
                "query": query,
                "top_k": 5,
            },
        )
        nodes = resp.json().get("data", {}).get("nodes", [])
        return [{"page_content": n["text"], "metadata": n.get("metadata", {})} for n in nodes]
```

**说明**以上代码为示例，实际使用时请添加错误处理和重试逻辑。

**重要**所有第三方接入的基础都是 DashScope API，完整接口文档见 [API 参考](raw/application-api-reference/rag-api/rag-api-overview.md)。
