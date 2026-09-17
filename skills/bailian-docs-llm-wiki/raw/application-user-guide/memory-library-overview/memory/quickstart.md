# 快速开始

3 步体验记忆的写入、查看和检索

用默认记忆库，3 步跑通记忆的写入、查看和检索。如需自定义记忆规则，参见[创建记忆库](raw/application-user-guide/memory-library-overview/create-memory.md)。

## 前提条件

-   已获取 `DASHSCOPE_API_KEY`，获取方式见[获取 API Key](raw/model-api-reference/preparations/get-api-key.md)
-   如使用 Python SDK，先安装：`pip install agentscope-runtime`

## 步骤一：写入记忆

调用 `AddMemory` 接口，将对话传入记忆库。系统自动从对话中提取事实记忆。

cURL

```
curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/add \
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
curl -X GET "https://dashscope.aliyuncs.com/api/v2/apps/memory/memory_nodes?user_id=user_001&page_size=10&page_num=1" \
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
curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/memory_nodes/search \
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

**说明**到这里你已经完成了记忆的写入、查看和检索。将检索结果注入 Prompt 即可实现个性化回答。

**重要**体验完核心流程后，继续[创建记忆库](raw/application-user-guide/memory-library-overview/create-memory.md)配置自定义记忆规则。
