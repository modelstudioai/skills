# 快速开始

3 步体验记忆的写入、查看和检索

用默认记忆库，3 步跑通记忆的写入、查看和检索。如需自定义记忆规则，参见[创建记忆库](raw/application-user-guide/agent-context/memory-library-overview/create-memory.md)。

## 记忆体验路径

[

**1\. 写入记忆**

将示例对话交给 AddMemory，提取事实。

](#h-memory-qs-add)[

**2\. 查看记忆**

在控制台或 ListMemory 中核对 user\_001 的记忆。

](#h-memory-qs-list)[

**3\. 检索记忆**

为同一用户检索相关事实。

](#h-memory-qs-search)

## 前提条件

-   首次使用需开通记忆库服务：进入[百炼控制台记忆库页面](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list)，点击**立即开通**
-   已获取 `DASHSCOPE_API_KEY`，获取方式见[获取 API Key](raw/model-api-reference/preparations/get-api-key.md)
-   已获取[业务空间 ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)，并将下文请求地址中的 `{WorkspaceId}` 替换为该 ID。API Key 须属于同一业务空间
-   如使用 Python SDK，先安装：`pip install agentscope-runtime`，并设置服务地址：`export MEMORY_SERVICE_ENDPOINT="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/memory"` 注意：agentscope-runtime 依赖 `mcp.server.fastmcp`，该模块在 mcp 2.x 中已移除；若环境中 mcp 为 2.x 版本，需一并约束：`pip install agentscope-runtime "mcp<2"`，否则 import 时会报 `No module named 'mcp.server.fastmcp'`。

在运行示例的终端中显式设置 API Key；先替换占位值，不要将真实密钥提交到仓库：

```
export DASHSCOPE_API_KEY="sk-xxxxxxxxxxxxxxxx"
```

Python 示例使用同一终端中设置的 `DASHSCOPE_API_KEY` 和 `MEMORY_SERVICE_ENDPOINT`。启动 Python 前将服务地址中的 `{WorkspaceId}` 替换为实际业务空间 ID；未设置地址时，SDK 不会自动选择该业务空间的记忆服务地址。下方三步始终使用同一 `user_id="user_001"`。

本页使用独立 Memory 服务，与 Managed Agents 的 Memory Store 分开管理。

## 步骤一：写入记忆

调用 `AddMemory` 接口，将对话传入记忆库。系统自动从对话中提取事实记忆。

cURL

```
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/memory/add \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "messages": [
      {"role": "user", "content": "每天上午9点提醒我喝水"},
      {"role": "assistant", "content": "好的，已记录"},
      {"role": "user", "content": "明天10点提醒我整理会议纪要。"}
    ],
    "user_id": "user_001"
  }'
```

Python

```
from agentscope_runtime.tools.modelstudio_memory import (
    AddMemory, AddMemoryInput, Message,
)
import asyncio

async def add_memory_example():
    add_memory = AddMemory()
    try:
        await add_memory.arun(AddMemoryInput(
            user_id="user_001",
            messages=[
                Message(role="user", content="每天上午9点提醒我喝水"),
                Message(role="assistant", content="好的，已记录"),
                Message(role="user", content="明天10点提醒我整理会议纪要。"),
            ]
        ))
        print("记忆写入成功")
    finally:
        await add_memory.close()

asyncio.run(add_memory_example())
```

## 步骤二：查看记忆

在[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list)进入默认记忆库的**记忆详情**标签页，输入记忆实体 ID `user_001`，点击**查看**，即可看到系统自动提取的事实记忆。

也可通过 API 列出记忆：

cURL

```
curl -X GET "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/memory/memory_nodes?user_id=user_001&page_size=10&page_num=1" \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json"
```

Python

```
from agentscope_runtime.tools.modelstudio_memory import (
    ListMemory, ListMemoryInput,
)
import asyncio

async def list_memory_example():
    list_memory = ListMemory()
    try:
        result = await list_memory.arun(ListMemoryInput(
            user_id="user_001",
            page_size=10,
            page_num=1
        ))
        for node in result.memory_nodes:
            print(f"记忆: {node.content}")
    finally:
        await list_memory.close()

asyncio.run(list_memory_example())
```

## 步骤三：检索记忆

在控制台切换到**记忆检索**标签页，输入记忆实体 ID `user_001`，在输入框输入"我需要做什么？"，点击**运行**查看相关记忆。

通过 API 检索：

cURL

```
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/memory/memory_nodes/search \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "user_id": "user_001",
    "messages": [{"role": "user", "content": "我需要做什么？"}],
    "top_k": 10,
    "min_score": 0.3,
    "plan_version": "Lite"
  }'
```

Python

```
from agentscope_runtime.tools.modelstudio_memory import (
    SearchMemory, SearchMemoryInput, Message,
)
import asyncio

async def search_memory_example():
    search_memory = SearchMemory()
    try:
        result = await search_memory.arun(SearchMemoryInput(
            user_id="user_001",
            messages=[Message(role="user", content="我需要做什么？")]
        ))
        for node in result.memory_nodes:
            print(f"记忆: {node.content}")
    finally:
        await search_memory.close()

asyncio.run(search_memory_example())
```

**说明**到这里你已经完成了记忆的写入、查看和检索。核对 `user_001` 的列表与检索结果中的事实是否对应写入的对话。示例记录和检索提醒相关的事实，并不会自动创建定时提醒任务。将检索结果注入 Prompt 即可实现个性化回答。

**重要**体验完核心流程后，继续[创建记忆库](raw/application-user-guide/agent-context/memory-library-overview/create-memory.md)配置自定义记忆规则。

## 下一步

[

**自定义记忆规则**

创建适合业务的记忆库。

](raw/application-user-guide/agent-context/memory-library-overview/create-memory.md)[

**理解记忆模型**

了解记忆实体与事实记忆。

](raw/application-user-guide/agent-context/memory-library-overview/overview/concepts.md)[

**调整检索**

查看检索参数并将结果用于 Prompt。

](raw/application-api-reference/long-term-memory-new/fragments-overview/search-memory.md)
