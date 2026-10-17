# 管理记忆

查看、检索调试、更新和删除记忆

建议使用元数据（`meta_data`）对记忆分类管理，便于后续精确检索。查看会话关联的记忆变更参见[记忆观测](raw/application-user-guide/agent-context/memory-library-overview/observability/observation.md)，追溯自动抽取及手动操作的变更记录参见[记忆审计](raw/application-user-guide/agent-context/memory-library-overview/observability/audit.md)。

## 查看记忆详情

在[记忆库](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list)卡片上点击**查看详情**，进入**记忆详情**标签页。顶部展示事实记忆数、用户画像数、技能记忆数和记忆实体数；下方为实体列表，支持通过实体 ID（`user_id`）模糊搜索。点击操作列的**查看**，按记忆规则查看该实体的事实记忆、用户画像和技能记忆。

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
    "plan_version": "pro"
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

### 编辑事实记忆

1.  在记忆库的**记忆详情**标签页找到实体并点击**查看**。
2.  在**事实记忆规则**下选择对应规则，找到目标记忆卡片，点击详情图标进入**事实记忆详情**。
3.  点击**编辑**修改记忆内容，再点击**保存**或**保存并关闭弹窗**。

保存后，在记忆详情中确认新内容；需要比较修改前后的内容时，进入[记忆审计](raw/application-user-guide/agent-context/memory-library-overview/observability/audit.md)查看更新快照。

### 停用和重新启用事实记忆

在**事实记忆详情**中关闭启用开关，记忆显示为**未启用**；重新开启后显示为**已启用**。审计中分别记录为**软删除**与**恢复**。

### 删除事实记忆

**警告**确认删除后记忆无法恢复。若只需暂时停用，使用启用开关，不要执行删除。

在目标记忆卡片上点击删除图标，再在确认框中点击**删除**。删除成功后，检查记忆列表；在[记忆审计](raw/application-user-guide/agent-context/memory-library-overview/observability/audit.md)中可查询删除记录及变更前的内容。

### 通过 API 更新和删除

cURL

```
# 更新记忆
curl -X PATCH "https://dashscope.aliyuncs.com/api/v2/apps/memory/memory_nodes/{memory_node_id}" \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
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

**重要**接口参数详情参见 [API 参考](raw/application-api-reference/long-term-memory-new/api-overview.md)，计费和限流参见[计费与限流](raw/application-user-guide/agent-context/memory-library-overview/integration-overview/billing.md)。
