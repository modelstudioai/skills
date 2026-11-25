# 更新记忆

更新指定记忆节点的内容

更新指定记忆节点的内容。接口会自动识别节点类型并格式化内容。

<a id="请求方法与路径"></a>

## 请求方法与路径

`PATCH https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/memory/memory_nodes/{memory_node_id}`

调用时请将 `{WorkspaceId}` 替换为真实的[业务空间 ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="请求参数"></a>

## 请求参数

| 参数 | 类型 | 必填 | 位置 | 说明 |
| --- | --- | --- | --- | --- |
| `memory_node_id` | string | 是 | Path | 记忆节点 ID |
| `custom_content` | string | 是 | Body | 更新后的记忆内容 |
| `memory_library_id` | string | 否 | Body | 记忆库 ID |
| `meta_data` | object | 否 | Body | 元信息。增量更新，未指定的键保持不变 |
| `skill_name` | string | 条件必填 | Body | 节点为 skill 类型时，必须同时传入 `skill_name`、`skill_description` 和 `skill_tags` |
| `skill_description` | string | 条件必填 | Body | skill 描述。必填条件同 `skill_name` |
| `skill_tags` | array\[string\] | 条件必填 | Body | skill 标签。必填条件同 `skill_name` |

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
curl --location --request PATCH 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/memory/memory_nodes/42dfc089dfa7409889966960a95c3b7e' \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "custom_content": "更新后的记忆内容",
    "memory_library_id": "memory_library_001",
    "meta_data": {"location_name": "杭州"}
  }'
```

<a id="fig-code-group-python-tab"></a>

Python

<a id="code-code-group-python"></a>

```python
from agentscope_runtime.tools.modelstudio_memory import UpdateMemory
import asyncio

async def main():
    update_memory = UpdateMemory()
    try:
        await update_memory.arun(
            memory_node_id="MEMORY_NODE_ID",
            user_id="user_001",
            custom_content="还要提醒我上午10点吃药。"
        )
        print("更新成功")
    finally:
        await update_memory.close()

asyncio.run(main())
```

<a id="响应示例"></a>

## 响应示例

<a id="code-block"></a>

```json
{
  "request_id": "cc2690f9f2b3485a93013e5705c91241"
}
```

> **重要**
>
> 删除记忆使用 [DeleteMemory](delete-memory.md)。
