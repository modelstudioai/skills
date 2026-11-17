# 接入 AgentScope

在 AgentScope 框架中通过自定义中间件把阿里云百炼 Knowledge Studio 作为智能体的知识记忆体，实现 static 静态注入与 agentic 自主检索两种模式

**说明**本实践面向使用 AgentScope 作为 runtime 托管智能体的开发者，展示如何通过自定义中间件把阿里云百炼 Knowledge Studio 接入 AgentScope Agent，作为智能体的知识记忆体。全流程高代码实现，不依赖控制台手动操作。文中示例代码实现基于 AgentScope 2.0.4 版本。

## 原理：知识库作为智能体的记忆体

大模型本身无状态，每次推理独立。AgentScope 通过**中间件**机制为智能体注入外部能力，RAG 检索、长期记忆、链路追踪等均以中间件形式挂载，无需修改智能体核心逻辑。

AgentScope 内置了 `RAGMiddleware`，它接收一组 `KnowledgeBase` 对象（封装了本地嵌入模型和向量库），在推理前注入检索结果。但阿里云百炼 Knowledge Studio 是**托管服务**，嵌入、向量存储、检索全部在服务端完成，不需要本地向量库。

本实践的做法是：编写一个自定义中间件 `KnowledgeStudioRAGMiddleware`，直接调用 Knowledge Studio 的[知识检索 API](raw/application-api-reference/rag-api/knowledge/knowledgesearch.md)，通过两种模式把检索结果接入 AgentScope Agent：

```
用户提问
  ──→ AgentScope Agent（ReAct 循环）
  ──→ KnowledgeStudioRAGMiddleware
        ├─ static 模式（on_system_prompt）：每次推理前检索，注入 system prompt
        └─ agentic 模式（list_tools）：暴露 search_knowledge 工具，模型自主调用
  ──→ Knowledge Studio（knowledge search API）
  ──→ 检索结果返回 Agent
```

模式

触发时机

实现方式

对应 AgentScope 中间件 hook

**static**

每次 reply 的首次推理前

把用户消息作为检索 query，结果注入 system prompt

`on_system_prompt`

**agentic**

模型自主判断

暴露 `search_knowledge` 工具，Agent 自主调用

`list_tools`

**说明**AgentScope 中间件有 6 个 hook 位置。本实践用到两个：`on_system_prompt`（Transformer 型，串行接力修改系统提示）和 `list_tools`（Tool source 型，声明中间件提供的工具）。详见 [AgentScope 中间件文档](https://docs.agentscope.io/versions/2.0.5dev/zh/building-blocks/middleware)。

## 环境准备

### 安装依赖

```
uv pip install "agentscope[full]" aiohttp
```

**重要**AgentScope 2.0 需要 Python 3.11 及以上。推荐使用 [uv](https://github.com/astral-sh/uv) 安装。详见 [AgentScope 快速开始](https://docs.agentscope.io/versions/2.0.5dev/zh/getting-started/quick-start)。

### 准备参数

参数

获取方式

示例

DashScope API Key

[设置 → API Key](https://bailian.console.aliyun.com/?tab=model#/api-key) 页创建

`sk-xxxxxxxx`

Workspace ID

控制台 URL 中的业务空间 ID

`llm-xxxxxxxx`

知识检索服务 ID

在[知识服务 → 知识检索](https://bailian.console.aliyun.com/cn-beijing/rag/retrieval/list)创建并发布后获取

`aid-xxxxxxxx`

## 第一步：通过 API 搭建知识库

知识库的搭建（文件上传 → 创建索引 → 导入）全部通过 API 完成。以下封装为可复用函数，完整 API 细节见 [创建知识库并导入](raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md) 和 [文件注册](raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-file.md)。

```
import os
import time
import hashlib
import requests

BASE_URL = "https://{workspace_id}.cn-beijing.maas.aliyuncs.com"
API_KEY = os.environ["DASHSCOPE_API_KEY"]
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

def upload_file(file_path: str, category: str = "default") -> str:
    """上传文件到数据中心，返回 fileId。"""
    file_size = str(os.path.getsize(file_path))
    file_name = os.path.basename(file_path)
    with open(file_path, "rb") as f:
        content_md5 = hashlib.md5(f.read()).hexdigest()

    # 1. 申请上传租约
    resp = requests.post(
        f"{BASE_URL}/api/v1/connector/dash/applyFileUploadLease",
        headers=HEADERS,
        json={"category": category, "fileName": file_name,
              "sizeBytes": file_size, "contentMd5": content_md5})
    lease = resp.json()["data"]

    # 2. 上传到 OSS
    with open(file_path, "rb") as f:
        requests.put(lease["param"]["url"],
                      headers=lease["param"]["headers"], data=f)

    # 3. 注册文件
    resp = requests.post(
        f"{BASE_URL}/api/v1/connector/dash/addFile",
        headers=HEADERS,
        json={"leaseId": lease["leaseId"], "category": category,
              "categoryType": "UNSTRUCTURED", "parser": "AUTO_SELECT"})
    return resp.json()["data"]["fileId"]

def create_kb_and_wait(file_ids: list[str], kb_name: str = "my-kb") -> str:
    """创建知识库并导入文件，轮询直到导入完成，返回知识库 ID。"""
    resp = requests.post(
        f"{BASE_URL}/api/v1/indices/rag/index/create_v2",
        headers=HEADERS,
        json={"name": kb_name, "structureType": "unstructured",
              "sinkType": "DEFAULT", "sourceType": "DATA_CENTER_FILE",
              "embeddingModelName": "text-embedding-v4", "chunkSize": 600,
              "docIds": file_ids,
              "dataSources": [{"sourceType": "DATA_CENTER_FILE"}]})
    data = resp.json()["data"]
    kb_id, job_id = data["pipelineId"], data["ingestionId"]

    while True:
        resp = requests.get(
            f"{BASE_URL}/api/v1/indices/rag/index_job/status",
            headers=HEADERS,
            params={"index_id": kb_id, "job_id": job_id})
        status = resp.json()["data"]["ingestion_status"]
        if status == "COMPLETED":
            break
        elif status in ("FAILED", "CANCELLED"):
            raise RuntimeError(f"导入失败: {status}")
        time.sleep(3)
    return kb_id

# 一行搭建知识库
file_id = upload_file("product-guide.md")
kb_id = create_kb_and_wait([file_id])
print(f"知识库就绪: {kb_id}")
```

**警告**文件 ID 参数名为 `docIds`，不是 `file_ids` 或 `fileIds`。`dataSources` 为必填字段。

## 第二步：封装检索客户端

把 Knowledge Studio 的[知识检索 API](raw/application-api-reference/rag-api/knowledge/knowledgesearch.md) 封装成轻量类，供中间件调用。知识检索 API 基于已发布的检索服务（agent），检索策略（rerank、top\_k 等）在控制台配置，调用时只需传入 `agent_id` 和查询意图。

```
import aiohttp

class KnowledgeStudioRetriever:
    """Knowledge Studio 检索客户端。"""

    def __init__(self, api_key: str, base_url: str, agent_id: str):
        self.api_key = api_key
        self.base_url = base_url
        self.agent_id = agent_id  # 知识检索服务 ID
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    async def search(self, query: str, top_n: int = 5) -> list[dict]:
        """检索知识库，返回切片列表。每条含 score 和 text。

        top_n 用于在本地截断结果数量，检索策略本身在 agent 中配置。
        """
        url = f"{self.base_url}/api/v1/indices/knowledge/search"
        payload = {"agent_id": self.agent_id, "query": query}

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=self.headers,
                                    json=payload) as resp:
                data = await resp.json()
                nodes = data["data"]["nodes"]
                return nodes[:top_n]

    def format_context(self, nodes: list[dict]) -> str:
        """把检索结果格式化为 prompt 上下文文本。"""
        parts = []
        for n in nodes:
            doc_name = n.get("metadata", {}).get("doc_name", "未知来源")
            parts.append(f"[{doc_name}]\n{n['text']}")
        return "\n---\n".join(parts)
```

## 第三步：实现 KnowledgeStudioRAGMiddleware

这是本实践的核心，一个自定义 `MiddlewareBase` 子类，同时实现 static 和 agentic 两种模式。参考 AgentScope 内置 [RAGMiddleware](https://docs.agentscope.io/versions/2.0.5dev/zh/building-blocks/rag#%E9%9B%86%E6%88%90%E5%88%B0%E6%99%BA%E8%83%BD%E4%BD%93) 的设计，但检索后端改为 Knowledge Studio API。

```
from typing import Any
from agentscope.middleware import MiddlewareBase
from agentscope.agent import Agent
from agentscope.tool import ToolBase
from agentscope.tool import ToolChunk
from agentscope.message import TextBlock, ToolResultState
from agentscope.permission import (
    PermissionDecision, PermissionBehavior, PermissionContext,
)

class KnowledgeStudioRAGMiddleware(MiddlewareBase):
    """把 Knowledge Studio 接入 AgentScope Agent 的 RAG 中间件。

    mode="static":  每次推理前检索，结果注入 system prompt
    mode="agentic": 暴露 search_knowledge 工具，模型自主调用
    """

    def __init__(self, retriever: KnowledgeStudioRetriever,
                 mode: str = "agentic", top_k: int = 5):
        self.retriever = retriever
        self.mode = mode
        self.top_k = top_k

    # ── static 模式：on_system_prompt hook ──────────────────────

    async def on_system_prompt(self, agent: Agent,
                               current_prompt: str) -> str:
        """static 模式：在 system prompt 中注入检索结果。

        AgentScope 在每轮 ReAct 的 reasoning 步骤组装 system prompt 时
        调用此 hook（Transformer 型，串行接力）。
        """
        if self.mode != "static":
            return current_prompt

        # 从上下文最后一条 user 消息提取检索 query
        recent_msgs = agent.state.context[-4:]
        user_query = ""
        for msg in reversed(recent_msgs):
            if msg.role == "user":
                user_query = msg.get_text_content()
                break
        if not user_query:
            return current_prompt

        # 检索并拼接
        nodes = await self.retriever.search(user_query, self.top_k)
        if not nodes:
            return current_prompt

        context = self.retriever.format_context(nodes)
        return (f"{current_prompt}\n\n## 知识库参考\n"
                f"以下是检索到的相关内容，回答时优先参考：\n\n{context}\n")

    # ── agentic 模式：list_tools hook ───────────────────────────

    async def list_tools(self) -> list[ToolBase]:
        """agentic 模式：暴露 search_knowledge 工具供模型自主调用。

        AgentScope 不会自动调用此 hook 返回的工具，
        需在组装 Agent 时手动收集并传入 Toolkit。
        """
        if self.mode != "agentic":
            return []

        retriever = self.retriever  # 闭包捕获

        class SearchKnowledgeTool(ToolBase):
            """在知识库中检索相关切片。"""
            name: str = "search_knowledge"
            description: str = (
                "Search the knowledge base for relevant information. "
                "Use this when you need to look up facts, docs, or "
                "specific knowledge to answer the question.")
            input_schema: dict = {
                "type": "object",
                "properties": {
                    "query": {"type": "string",
                              "description": "The search query."},
                    "top_k": {"type": "integer", "default": 5,
                               "description": "Number of results to return."},
                },
                "required": ["query"],
            }
            is_concurrency_safe: bool = True
            is_read_only: bool = True

            async def check_permissions(
                self, tool_input: dict[str, Any],
                context: PermissionContext,
            ) -> PermissionDecision:
                return PermissionDecision(
                    behavior=PermissionBehavior.ALLOW,
                    message="auto-allow search")

            async def call(self, query: str, top_k: int = 5):
                """检索知识库，返回相关切片文本。"""
                nodes = await retriever.search(query, top_k)
                if not nodes:
                    yield ToolChunk(
                        content=[TextBlock(text="No relevant results found.")],
                        state=ToolResultState.SUCCESS,
                        is_last=True,
                    )
                    return
                context = retriever.format_context(nodes)
                yield ToolChunk(
                    content=[TextBlock(text=context)],
                    state=ToolResultState.SUCCESS,
                    is_last=True,
                )

        return [SearchKnowledgeTool()]
```

**说明**AgentScope 的 `ToolBase` 是抽象基类，自定义工具需要实现：

-   类属性 `name`、`description`、`input_schema`（JSON Schema 格式）
-   类属性 `is_concurrency_safe`、`is_read_only`（权限与并发控制）
-   `check_permissions` 方法（返回 `PermissionDecision`，搜索工具直接 ALLOW）
-   `call` 方法（async generator，`yield ToolChunk` 返回结果）

## 第四步：组装并运行 Agent

用 DashScopeChatModel + KnowledgeStudioRAGMiddleware 组装 AgentScope Agent，展示两种模式的端到端运行。

### 创建模型和 Agent

```
import asyncio
import os
from agentscope.agent import Agent
from agentscope.model import DashScopeChatModel
from agentscope.credential import DashScopeCredential
from agentscope.tool import Toolkit
from agentscope.message import UserMsg

# 1. 创建 DashScope Chat Model
chat_model = DashScopeChatModel(
    credential=DashScopeCredential(api_key=os.environ["DASHSCOPE_API_KEY"]),
    model="qwen-plus",
    stream=True,
)

# 2. 创建检索客户端
retriever = KnowledgeStudioRetriever(
    api_key=os.environ["DASHSCOPE_API_KEY"],
    base_url=BASE_URL,
    agent_id="aid-xxxxxxxx",  # 从控制台知识检索服务获取
)
```

### 模式一：static 静态注入

```
async def run_static():
    """static 模式：每次推理前自动检索并注入 system prompt。"""
    mw = KnowledgeStudioRAGMiddleware(retriever, mode="static", top_k=3)
    agent = Agent(
        name="kb-assistant",
        system_prompt=(
            "你是知识库问答助手。根据检索到的知识库内容回答问题。"
            "如果知识库中没有相关信息，说明无法回答。"
        ),
        model=chat_model,
        middlewares=[mw],
    )

    result = await agent.reply(
        UserMsg(name="user", content="如何调用通义千问API？")
    )
    print(result.get_text_content())

asyncio.run(run_static())
```

实测输出（基于阿里云百炼技术文档知识库）：

```
调用通义千问API的步骤如下（依据知识库内容整理）：

1. 获取 API Key
   前往大模型服务平台阿里云百炼，开通模型调用服务，
   并创建 API Key……

2. 安装 SDK
   pip install dashscope

3. 调用 API
   使用 dashscope.Generation API 发起调用……
```

运行流程：

```
UserMsg ──→ on_system_prompt hook（检索 + 注入）──→ DashScopeChatModel（带上下文推理）──→ 回答
```

AgentScope 在每轮 ReAct 的 reasoning 步骤前调用 `on_system_prompt`，中间件自动执行检索并把结果拼进 system prompt，模型无需感知检索过程。

### 模式二：agentic 自主检索

```
async def run_agentic():
    """agentic 模式：模型自主决定何时检索、检索什么。"""
    mw = KnowledgeStudioRAGMiddleware(retriever, mode="agentic", top_k=3)
    tools = await mw.list_tools()  # 手动收集中间件提供的工具

    agent = Agent(
        name="kb-assistant",
        system_prompt=(
            "你是知识库问答助手。可以调用 search_knowledge 工具"
            "检索知识库。根据检索结果回答问题。"
        ),
        model=chat_model,
        toolkit=Toolkit(tools=tools),
        middlewares=[mw],
    )

    result = await agent.reply(
        UserMsg(name="user", content="如何调用通义千问API？")
    )
    print(result.get_text_content())

asyncio.run(run_agentic())
```

实测输出：

```
调用通义千问API主要有以下几种方式：

### 1. OpenAI 兼容接口（推荐，简单通用）
适用于熟悉 OpenAI SDK 的开发者……

### 2. DashScope SDK
使用阿里云原生 SDK……

### 3. HTTP 直接调用
使用 curl 或任意 HTTP 客户端……
```

运行流程：

```
UserMsg ──→ ReAct 第 1 轮推理 ──→ 模型决定调用 search_knowledge 工具 ──→ 工具执行（调 knowledge search API）──→ ReAct 第 2 轮推理（基于检索结果生成回答）──→ 回答
```

模型在 ReAct 循环中自主判断是否需要检索，如果问题简单或已有足够信息，可能直接回答不调用工具；如果需要查文档，则自主构造 query 调用 `search_knowledge` 工具。

### 两种模式叠加

AgentScope 允许同时挂两个不同 mode 的实例，既自动注入，又提供按需工具：

```
static_mw = KnowledgeStudioRAGMiddleware(retriever, mode="static", top_k=3)
agentic_mw = KnowledgeStudioRAGMiddleware(retriever, mode="agentic", top_k=5)
tools = await agentic_mw.list_tools()

agent = Agent(
    name="kb-assistant",
    system_prompt="你是知识库问答助手。",
    model=chat_model,
    toolkit=Toolkit(tools=tools),
    middlewares=[static_mw, agentic_mw],
)
```

## 模式对比与选型

维度

static 静态注入

agentic 自主检索

叠加模式

检索决策

固定（每次推理前都检索）

模型自主（按需）

两者兼有

AgentScope hook

`on_system_prompt`

`list_tools`

两个都用

上下文长度

每次注入 top\_k 条切片

工具结果按需进入

两者叠加

多轮检索

不支持（一次检索定结果）

支持（模型可多轮调用工具）

支持

适用场景

FAQ 问答、意图明确

复杂问答、需要判断是否查

高可靠性场景

与内置 RAGMiddleware

设计一致（static 模式）

设计一致（agentic 模式）

设计一致

**说明**本实践的自定义中间件在设计上与 AgentScope 内置的 `RAGMiddleware` 保持一致，两种模式、相同的参数命名（`mode`、`top_k`）。区别在于检索后端：内置 `RAGMiddleware` 依赖本地 `KnowledgeBase`（嵌入模型和向量库），本实践的中间件直接调用 Knowledge Studio 知识检索 API。

## 扩展：与 AgentScope 持久化状态结合

AgentScope 的 `AgentState` 可序列化为 JSON 并存储在 Redis 中，实现跨会话的状态恢复。知识库 ID 作为中间件配置项随 Agent 一起持久化：

```
from agentscope.state import AgentState
from agentscope.app.storage import RedisStorage

USER_ID = "user_123"
AGENT_ID = "agent_456"
SESSION_ID = "session_789"

async def run_with_persistence():
    async with RedisStorage(host="localhost", port=6379) as storage:
        record = await storage.get_session(
            user_id=USER_ID, agent_id=AGENT_ID, session_id=SESSION_ID)
        state = record.state if record else AgentState()

        agent = Agent(
            name="kb-assistant",
            system_prompt="你是知识库问答助手。",
            model=chat_model,
            toolkit=Toolkit(tools=await mw.list_tools()),
            middlewares=[mw],
            state=state,
        )

        result = await agent.reply(
            UserMsg(name="user", content="上次提到的功能还支持吗？")
        )

        if record:
            # 已有会话：直接更新状态
            await storage.update_session_state(
                user_id=USER_ID, agent_id=AGENT_ID,
                session_id=SESSION_ID, state=agent.state)
        else:
            # 首次会话：需先创建 session 记录
            from agentscope.app.storage import SessionConfig
            await storage.upsert_session(
                user_id=USER_ID, agent_id=AGENT_ID,
                config=SessionConfig(workspace_id="", name="kb-session"),
                state=agent.state, session_id=SESSION_ID)
```

**说明**Knowledge Studio 的检索是无状态的，每次检索调用独立，服务端不保存对话上下文。对话历史由 AgentScope 的 `AgentState` 管理，与知识库检索解耦。多轮对话传递工具历史的实践见[多轮对话 cookbook](raw/application-user-guide/knowledge-base/best-practices/multi-turn-chat.md)。

`update_session_state` 仅能更新已有会话的状态，首次调用需先通过 `upsert_session` 创建会话记录，否则会抛出 `KeyError`。

## 常见问题

### 为什么不用 AgentScope 内置的 RAGMiddleware？

内置 `RAGMiddleware` 依赖本地 `KnowledgeBase` 对象，需要本地嵌入模型和向量库。Knowledge Studio 是托管服务，嵌入、向量存储、检索全部在服务端。本实践的中间件直接调知识检索 API，省去本地向量库的部署和维护。

### static 模式每次推理都检索，会不会太慢？

Knowledge Studio 知识检索 API 的典型延迟在 200-500ms。如果对延迟敏感，可切换到 agentic 模式让模型按需检索，或调小 `top_k`。实测用 `top_k=3` 时，static 模式的 Agent 回答延迟在 3-5 秒（含模型生成时间）。

### agentic 模式下模型不调工具怎么办？

确保 system prompt 中明确提示"可以调用 search\_knowledge 工具检索知识库"。实测 `qwen-plus` 模型在问题涉及知识库内容时会自主调用工具。如果模型仍不调用，可换用更强的模型（如 `qwen-max`）。

### 能不能同时用 Knowledge Studio 的 knowledge/chat API 和 AgentScope？

可以，但两者是替代关系，不能叠加使用。Knowledge Studio [knowledge/chat](raw/application-api-reference/rag-api/knowledge/knowledgechat.md) 是内置 Agent 的托管问答服务，AgentScope 是自建 Agent 的框架。knowledge/chat 适合不想自建 Agent 的场景，AgentScope 适合需要自定义工具链、中间件、人机交互的场景。
