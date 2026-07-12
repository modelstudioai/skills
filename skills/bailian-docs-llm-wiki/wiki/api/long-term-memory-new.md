# long term memory new

百炼平台的「长期记忆（新）」提供一组 RESTful API，用于存储、检索、更新和删除用户记忆片段，并支持通过画像模板（profile schema）维护用户画像。记忆片段会从对话中自动提取关键信息，可在后续对话中通过语义检索召回，从而实现跨会话的个性化上下文。完整接口参考见 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。

## 公共请求信息

所有接口共用以下请求约定（详见 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)）：

- **Base URL**：`https://dashscope.aliyuncs.com/api/v2/apps/memory/`
- **认证方式**：在请求 Header 中添加 `Authorization: Bearer $DASHSCOPE_API_KEY`。[API Key](../concepts/api-key.md) 的获取方式参见[获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。
- **Content-Type**：`application/json`

## 接口概览

长期记忆（新）提供以下 API 接口：

| 接口名称 | HTTP 方法 | 路径 | 说明 |
| --- | --- | --- | --- |
| AddMemory | POST | `/add` | 添加记忆片段 |
| SearchMemory | POST | `/memory_nodes/search` | 搜索记忆片段 |
| ListMemory | GET | `/memory_nodes` | 列出记忆片段 |
| DeleteMemory | DELETE | `/memory_nodes/{memory_node_id}` | 删除记忆片段 |
| UpdateMemory | PATCH | `/memory_nodes/{memory_node_id}` | 更新记忆片段 |
| CreateProfileSchema | POST | `/profile_schemas` | 创建画像模板 |
| ListProfileSchemas | GET | `/profile_schemas` | 获取画像模板列表 |
| DeleteProfileSchema | DELETE | `/profile_schemas/{profile_schema_id}` | 删除画像模板 |
| UpdateProfileSchema | PATCH | `/profile_schemas/{profile_schema_id}` | 更新画像模板 |
| GetProfileSchema | GET | `/profile_schemas/{profile_schema_id}` | 获取画像模板详情 |
| GetUserProfile | GET | `/profile_schemas/{profile_schema_id}/user_profile` | 获取用户画像 |

## 使用限制

| API 接口 | 限流（阿里云账号级别） |
| --- | --- |
| 全部接口 | 总计不超过 3000 QPM |
| 记忆片段 add 接口 | 120 QPM |
| 记忆片段 search 接口 | 300 QPM |

生成的记忆片段与用户画像暂无失效日期。

## 核心接口

### AddMemory - 添加记忆片段

将用户对话存储为记忆片段，自动提取关键信息和用户画像。

**请求体参数：**

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `user_id` | string | 是 | 记忆实体 ID，用于标识归属对象，最大 64 个字符 |
| `messages` | array | 是（与 `custom_content` 互斥） | 对话消息列表，每个消息包含 `role`（user/assistant）和 `content`。最多 50 条对话记录，一问一答算 2 条 |
| `custom_content` | string | 是（与 `messages` 互斥） | 自定义内容，最大 512 个字符。传入后会忽略 `messages` |
| `profile_schema` | string | 否 | 画像模板 ID，在记忆库详情页获取 |
| `memory_library_id` | string | 否 | 记忆库 ID，最大 32 个字符。不传则使用默认记忆库 |
| `project_id` | string | 否 | 记忆片段规则 ID。不传则使用指定记忆库的默认规则 |
| `meta_data` | object | 否 | 用户自定义信息 |

**返回结果：**

- `request_id` (string) - 请求 ID
- `memory_nodes` (array) - 变更的记忆片段列表，每项包含：
  - `memory_node_id` (string) - 记忆片段 ID
  - `content` (string) - 提取出的记忆片段内容
  - `event` (string) - 操作事件类型：`ADD`（创建）、`UPDATE`（更新）、`DELETE`（删除）
  - `old_content` (string) - 更新前的内容，仅当 `event` 为 `UPDATE` 时有效

**示例（cURL）：**

```bash
curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/add \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "messages": [
      {"role": "user", "content": "每天上午11点提醒我点外卖。"},
      {"role": "assistant", "content": "没问题"}
    ],
    "user_id": "user_001",
    "memory_library_id": "xxx",
    "meta_data": {"location_name": "北京"}
  }'
```

传入 `custom_content` 时可直接写入自定义文本，例如 `"custom_content": "用户周末去上海参加WAIC"`。

> **注意**：`messages` 与 `custom_content` 互斥，传入 `custom_content` 后 `messages` 会被忽略。

### SearchMemory - 搜索记忆片段

基于语义相似度搜索相关记忆片段，更多检索参数详见 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。

**请求体参数：**

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `user_id` | string | 是 | 记忆实体 ID，最大 64 个字符 |
| `messages` | array | 是 | 对话记录，每条含 `role` 与 `content` |
| `memory_library_id` | string | 否 | 记忆库 ID，不传使用默认 |
| `project_ids` | list | 否 | 记忆片段规则 ID 数组，可传入多个进行混合检索 |
| `top_k` | integer | 否 | 最大召回个数，取值 1~100（默认 10） |
| `min_score` | double | 否 | 最小相似度分数阈值，值域 [0,1]（默认 0.3） |
| `enable_rerank` | boolean | 否 | 是否开启搜索结果[重排序](../concepts/rerank.md)（默认 false） |
| `enable_judge` | boolean | 否 | 是否开启意图判别回调（默认 false） |
| `enable_rewrite` | boolean | 否 | 是否开启 query 重写（默认 false） |

**返回结果：**

- `request_id` (string) - 请求 ID
- `memory_nodes` (array) - 记忆片段列表，每项包含 `memory_node_id`、`content`、`created_at`、`updated_at`

**示例（cURL）：**

```bash
curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/memory_nodes/search \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "user_id": "user_001",
    "messages": [{"role": "user", "content": "明天上午十一点我有什么日程安排吗？"}],
    "top_k": 100,
    "min_score": 0
  }'
```

### ListMemory - 列出记忆片段

分页查看用户的所有记忆片段。

**查询参数：**

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `user_id` | string | 是 | 记忆实体 ID，最大 64 个字符 |
| `memory_library_id` | string | 否 | 记忆库 ID，不传使用默认 |
| `project_id` | string | 否 | 记忆片段规则 ID，不传使用默认 |
| `page_num` | integer | 否 | 页码，从 1 开始（默认 1） |
| `page_size` | integer | 否 | 每页条目数（默认 10） |

**返回结果：** `memory_nodes`（含 `memory_node_id`、`content`、`created_at`、`updated_at`、`meta_data`），以及分页字段 `total`、`page_size`、`page_num`。

### DeleteMemory - 删除记忆片段

**路径参数：** `memory_node_id` - 记忆片段 ID

**查询参数：** `memory_library_id`（可选，不传使用默认记忆库）

返回 `request_id`。

### UpdateMemory - 更新记忆片段

**路径参数：** `memory_node_id` - 记忆片段 ID

**请求体参数：**

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `custom_content` | string | 是 | 要更新的内容，最大 512 个字符 |
| `user_id` | string | 是 | 记忆实体 ID，最大 64 个字符 |
| `memory_library_id` | string | 否 | 记忆库 ID，不传使用默认 |
| `timestamp` | long | 否 | 事件发生时间戳（秒级 Unix，默认当前时间） |
| `meta_data` | object | 否 | 用户自定义信息（增量更新） |

返回 `request_id`。

### 画像模板接口

通过 `/profile_schemas` 系列接口可创建、查询、更新、删除画像模板，并通过 `GET /profile_schemas/{profile_schema_id}/user_profile` 获取对应用户画像。画像模板 ID 在 AddMemory 的 `profile_schema` 参数中传入，用于在写入记忆时同步抽取/更新用户画像。

## Python SDK

记忆相关接口通过 `agentscope-runtime` 提供封装，安装命令：`pip install agentscope-runtime>=1.1.5`。常用类包括 `AddMemory`、`SearchMemory`、`ListMemory`、`DeleteMemory` 及对应的 `*Input` 与 `Message`。

```python
from agentscope_runtime.tools.modelstudio_memory import (
    AddMemory, Message, AddMemoryInput,
)
import asyncio

async def add_memory_example():
    add_memory = AddMemory()
    try:
        result = await add_memory.arun(AddMemoryInput(
            user_id="user_001",
            messages=[
                Message(role="user", content="每天上午9点提醒我喝水"),
                Message(role="assistant", content="好的，已记录"),
            ],
            meta_data={"category": "提醒"}
        ))
        print(f"创建了 {len(result.memory_nodes)} 个记忆片段")
    finally:
        await add_memory.close()

asyncio.run(add_memory_example())
```

> **注意**：UpdateMemory 接口在 Python SDK 中暂未提供封装，需通过 `requests` 等库直接调用 REST API。

## 限制和注意事项

- **限流**：全部接口合计 3000 QPM；`add` 单独 120 QPM，`search` 单独 300 QPM。
- **消息上限**：AddMemory 的 `messages` 最多 50 条对话记录（一问一答算 2 条）。
- **内容长度**：`custom_content` 与 UpdateMemory 的 `custom_content` 均限制 512 个字符。
- **互斥参数**：AddMemory 中 `messages` 与 `custom_content` 互斥，传 `custom_content` 会忽略 `messages`。
- **默认记忆库**：`memory_library_id`、`project_id` 不传时自动使用默认值。
- **持久性**：生成的记忆片段与用户画像暂无失效日期，需通过 DeleteMemory 主动清理。

## 来源文档

- [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)

















