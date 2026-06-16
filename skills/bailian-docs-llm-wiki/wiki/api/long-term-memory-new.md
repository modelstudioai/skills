# long term memory new

长期记忆（新）是百炼平台提供的用户记忆管理服务，通过 REST API 实现对话记忆的自动提取、存储、检索和管理。该功能可将用户对话自动转化为结构化的记忆片段，并支持基于语义相似度的搜索，适用于构建具有长期记忆能力的智能助手。API 基于阿里云 DashScope 服务，支持 cURL 和 Python SDK 两种调用方式。

## 接口概览

根据 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)，长期记忆（新）共提供 11 个 API 接口，分为三大类：

### 记忆片段管理

| 接口名称 | HTTP 方法 | 路径 | 说明 |
|---------|----------|------|------|
| AddMemory | POST | `/add` | 添加记忆片段 |
| SearchMemory | POST | `/memory_nodes/search` | 搜索记忆片段 |
| ListMemory | GET | `/memory_nodes` | 列出记忆片段 |
| DeleteMemory | DELETE | `/memory_nodes/{memory_node_id}` | 删除记忆片段 |
| UpdateMemory | PATCH | `/memory_nodes/{memory_node_id}` | 更新记忆片段 |

### 画像模板管理

| 接口名称 | HTTP 方法 | 路径 | 说明 |
|---------|----------|------|------|
| CreateProfileSchema | POST | `/profile_schemas` | 创建画像模板 |
| ListProfileSchemas | GET | `/profile_schemas` | 获取画像模板列表 |
| DeleteProfileSchema | DELETE | `/profile_schemas/{profile_schema_id}` | 删除画像模板 |
| UpdateProfileSchema | PATCH | `/profile_schemas/{profile_schema_id}` | 更新画像模板 |
| GetProfileSchema | GET | `/profile_schemas/{profile_schema_id}` | 获取画像模板详情 |

### 用户画像

| 接口名称 | HTTP 方法 | 路径 | 说明 |
|---------|----------|------|------|
| GetUserProfile | GET | `/profile_schemas/{profile_schema_id}/user_profile` | 获取用户画像 |

## 公共请求信息

- **Base URL**：`https://dashscope.aliyuncs.com/api/v2/apps/memory/`
- **认证方式**：Header 中添加 `Authorization: Bearer $DASHSCOPE_API_KEY`
- **Content-Type**：`application/json`

## 核心接口详解

### AddMemory - 添加记忆片段

将用户对话存储为记忆片段，自动提取关键信息和用户画像。

**关键参数：**

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `user_id` | string | 是 | 记忆实体 ID，最大 64 个字符 |
| `messages` | array | 是（与 `custom_content` 互斥） | 对话消息列表，最多 50 条记录 |
| `custom_content` | string | 是（与 `messages` 互斥） | 自定义内容，最大 512 个字符 |
| `profile_schema` | string | 否 | 画像模板 ID |
| `memory_library_id` | string | 否 | 记忆库 ID，不传则使用默认记忆库 |
| `project_id` | string | 否 | 记忆片段规则 ID |
| `meta_data` | object | 否 | 用户自定义信息 |

`messages` 中每条消息包含 `role`（`user` 或 `assistant`）和 `content` 字段。

**返回结果**包含 `request_id` 和 `memory_nodes` 数组，每个节点包含：
- `memory_node_id` - 记忆片段 ID
- `content` - 从对话中提取的记忆内容
- `event` - 操作类型：`ADD`（创建）、`UPDATE`（更新）、`DELETE`（删除）
- `old_content` - 更新前的内容（仅 `UPDATE` 事件）

### SearchMemory - 搜索记忆片段

基于语义相似度搜索相关记忆片段，支持多种检索增强选项。

**关键参数：**

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `user_id` | string | 是 | 记忆实体 ID |
| `messages` | array | 是 | 对话记录 |
| `memory_library_id` | string | 否 | 记忆库 ID |
| `project_ids` | list | 否 | 记忆片段规则 ID 数组，支持多规则混合检索 |
| `top_k` | integer | 否 | 最大召回个数，范围 1~100（默认 10） |
| `min_score` | double | 否 | 最小相似度分数阈值，范围 [0,1]（默认 0.3） |
| `enable_rerank` | boolean | 否 | 是否开启重排序（默认 false） |
| `enable_judge` | boolean | 否 | 是否开启意图判别回调（默认 false） |
| `enable_rewrite` | boolean | 否 | 是否开启 query 重写（默认 false） |

### ListMemory - 列出记忆片段

分页查看用户的所有记忆片段，通过查询参数传入 `user_id`、`page_num`（默认 1）、`page_size`（默认 10）等参数。返回结果包含分页信息（`total`、`page_size`、`page_num`）。

### DeleteMemory - 删除记忆片段

通过路径参数 `memory_node_id` 指定要删除的记忆片段，可选传入 `memory_library_id`。

### UpdateMemory - 更新记忆片段

通过路径参数 `memory_node_id` 指定目标片段，请求体中传入 `custom_content`（最大 512 字符）、`user_id`，可选传入 `timestamp`（秒级 Unix 时间戳）和 `meta_data`（增量更新）。

## 使用方式

### cURL 调用

如 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 中所示，直接通过 HTTP 请求调用：

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
    "memory_library_id": "xxx"
  }'
```

### Python SDK 调用

需要安装 `agentscope-runtime`（版本 ≥ 1.1.5）：

```bash
pip install agentscope-runtime>=1.1.5
```

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
        ))
        print(f"创建了 {len(result.memory_nodes)} 个记忆片段")
    finally:
        await add_memory.close()

asyncio.run(add_memory_example())
```

> **注意**：Python SDK 目前暂未提供 UpdateMemory 接口的封装，需通过 `requests` 库直接调用 REST API。

## 限制和注意事项

根据 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)，使用时需注意以下限制：

### 限流（阿里云账号级别）

| API 接口 | 限流 |
|---------|------|
| 全部接口合计 | 3000 QPM |
| 记忆片段 add 接口 | 120 QPM |
| 记忆片段 search 接口 | 300 QPM |

### 其他限制

- `messages` 最多支持 **50 条**对话记录（一问一答算 2 条）
- `custom_content` 最大 **512 个字符**
- `user_id` 最大 **64 个字符**
- `memory_library_id` 最大 **32 个字符**
- SearchMemory 的 `top_k` 取值范围为 **1~100**
- 生成的记忆片段与用户画像**暂无失效日期**
- `messages` 与 `custom_content` 互斥，同时传入时 `messages` 会被忽略
- 不传 `memory_library_id` 时，系统会自动选择默认记忆库

## 来源文档

- [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)











