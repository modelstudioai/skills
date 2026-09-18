# 管理记忆

查看、检索调试、更新和删除记忆

记忆写入后，可在控制台查看和检索，或通过 API 进行列表、更新和删除操作。建议使用元数据（`meta_data`）对记忆分类管理，便于后续精确检索。

## 查看记忆详情

在[记忆库详情](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list)页的**记忆详情**标签页，顶部展示记忆库基本信息和统计数据。下方展示记忆实体列表，支持通过记忆实体 ID（`user_id`）筛选。点击操作列的**查看**可查看记忆详情。

通过 API 列出记忆：

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
            user_id="user_001", page_size=10, page_num=1
        ))
        for node in result.memory_nodes:
            print(f"记忆 {node.memory_node_id}: {node.content}")
    finally:
        await list_memory.close()

asyncio.run(list_memory_example())
```

## 检索调试

在记忆库详情页的**记忆检索**标签页调试检索效果，优化召回准确性和相关性。

参数

说明

建议值

**记忆实体 ID**

写入记忆时设置的 `user_id`

—

**事实记忆规则**

选择指定规则进行检索

—

**最大召回数量**

每次检索返回的记忆条数（1~100）

按需设置

**意图判别召回**

系统判断当前对话是否需要召回记忆，避免无关检索

开启

**改写**

对用户查询优化改写，提升语义检索准确率

口语化提问时开启

**排序**

对检索结果重排，提升相关性

需要高相关性时开启

**相似度阈值**

`0.0~1.0`，过滤低相关性结果

`0.5~0.7`

**说明**排序目前仅支持 `gte-rerank-v2` 模型。相似度过高可能漏召相关记忆，过低可能引入噪声。

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
            messages=[Message(role="user", content="我需要做什么？")],
            top_k=10,
            min_score=0.6
        ))
        for node in result.memory_nodes:
            print(f"记忆: {node.content}")
    finally:
        await search_memory.close()

asyncio.run(search_memory_example())
```

## 更新和删除记忆

cURL

```
# 更新记忆
curl -X PATCH "https://dashscope.aliyuncs.com/api/v2/apps/memory/memory_nodes/{memory_node_id}" \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "user_id": "user_001",
    "custom_content": "还要提醒我上午10点吃药。"
  }'

# 删除记忆
curl -X DELETE "https://dashscope.aliyuncs.com/api/v2/apps/memory/memory_nodes/{memory_node_id}" \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json"
```

Python

```
from agentscope_runtime.tools.modelstudio_memory import (
    ListMemory, ListMemoryInput,
    DeleteMemory, DeleteMemoryInput,
)
import asyncio

async def manage_memory_example():
    list_memory = ListMemory()
    delete_memory = DeleteMemory()
    try:
        # 列出记忆
        result = await list_memory.arun(ListMemoryInput(
            user_id="user_001", page_size=10, page_num=1
        ))
        for node in result.memory_nodes:
            print(f"记忆 {node.memory_node_id}: {node.content}")

        # 删除记忆
        await delete_memory.arun(DeleteMemoryInput(
            user_id="user_001",
            memory_node_id="MEMORY_NODE_ID"
        ))
    finally:
        await list_memory.close()
        await delete_memory.close()

asyncio.run(manage_memory_example())
```

**重要**接口参数详情参见 [API 参考](raw/application-api-reference/long-term-memory-new/overview.md)，计费和限流参见[计费与限流](raw/application-user-guide/memory-library-overview/overview/billing.md)。
