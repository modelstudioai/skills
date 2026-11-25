# 删除记忆

删除指定记忆节点，删除后不可恢复

删除指定的记忆节点。

> **警告**
>
> 删除操作不可逆，请谨慎操作。

<a id="请求方法与路径"></a>

## 请求方法与路径

`DELETE https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/memory/memory_nodes/{memory_node_id}`

调用时请将 `{WorkspaceId}` 替换为真实的[业务空间 ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="请求参数"></a>

## 请求参数

| 参数 | 类型 | 必填 | 位置 | 说明 |
| --- | --- | --- | --- | --- |
| `memory_node_id` | string | 是 | Path | 记忆节点 ID |
| `memory_library_id` | string | 否 | Query | 记忆库 ID。不传时按默认记忆库解析 |

<a id="返回结果"></a>

## 返回结果

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `request_id` | string | 请求 ID |

<a id="请求示例"></a>

## 请求示例

<a id="fig-code-group"></a>

<a id="fig-code-group-curl-tab"></a>

cURL

<a id="code-code-group-curl"></a>

```bash
curl --location --request DELETE 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/memory/memory_nodes/42dfc089dfa7409889966960a95c3b7e?memory_library_id=memory_library_001' \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

<a id="fig-code-group-python-tab"></a>

Python

<a id="code-code-group-python"></a>

```python
from agentscope_runtime.tools.modelstudio_memory import (
    DeleteMemory, DeleteMemoryInput,
)
import asyncio

async def main():
    delete_memory = DeleteMemory()
    try:
        await delete_memory.arun(DeleteMemoryInput(
            user_id="user_001",
            memory_node_id="MEMORY_NODE_ID"
        ))
        print("删除成功")
    finally:
        await delete_memory.close()

asyncio.run(main())
```

<a id="响应示例"></a>

## 响应示例

<a id="code-block"></a>

```json
{
  "request_id": "a1b2c3d4-5678-90ab-cdef-1234567890ab"
}
```

> **重要**
>
> 用户画像 API 参见 [CreateProfileSchema](../profiles-overview/create-schema.md)。
