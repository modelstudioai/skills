# long term memory new

百炼平台的长期记忆（新）功能提供了一套完整的 RESTful API，用于管理用户对话中的记忆片段和用户画像。通过这些接口，开发者可以将对话内容自动提取为结构化记忆，并在后续交互中基于语义相似度检索相关记忆，从而实现个性化的对话体验。详细接口说明参见[长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。

## 公共请求信息

所有接口共享以下请求配置：

- **Base URL**：`https://dashscope.aliyuncs.com/api/v2/apps/memory/`
- **认证方式**：在请求 Header 中添加 `Authorization: Bearer $DASHSCOPE_API_KEY`
- **Content-Type**：`application/json`

## 接口概览

长期记忆（新）共提供 11 个 API 接口，分为两大类：

### 记忆片段管理

| 接口 | 方法 | 路径 | 说明 |
|------|------|------|------|
| AddMemory | POST | `/add` | 添加记忆片段 |
| SearchMemory | POST | `/memory_nodes/search` | 搜索记忆片段 |
| ListMemory | GET | `/memory_nodes` | 列出记忆片段 |
| DeleteMemory | DELETE | `/memory_nodes/{memory_node_id}` | 删除记忆片段 |
| UpdateMemory | PATCH | `/memory_nodes/{memory_node_id}` | 更新记忆片段 |

### 画像模板管理

| 接口 | 方法 | 路径 | 说明 |
|------|------|------|------|
| CreateProfileSchema | POST | `/profile_schemas` | 创建画像模板 |
| ListProfileSchemas | GET | `/profile_schemas` | 获取画像模板列表 |
| DeleteProfileSchema | DELETE | `/profile_schemas/{profile_schema_id}` | 删除画像模板 |
| UpdateProfileSchema | PATCH | `/profile_schemas/{profile_schema_id}` | 更新画像模板 |
| GetProfileSchema | GET | `/profile_schemas/{profile_schema_id}` | 获取画像模板详情 |
| GetUserProfile | GET | `/profile_schemas/{profile_schema_id}/user_profile` | 获取用户画像 |

## 核心接口详解

### AddMemory - 添加记忆片段

将用户对话存储为记忆片段，系统会自动提取关键信息和用户画像。支持两种输入方式：

- **messages**：传入对话消息列表（最多 50 条记录），每条包含 `role`（user/assistant）和 `content`
- **custom_content**：直接传入自定义文本（最大 512 字符）

两者互斥，传入 `custom_content` 后会忽略 `messages`。

关键参数：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `user_id` | string | 是 | 记忆实体 ID，最大 64 字符 |
| `messages` | array | 是（与 custom_content 互斥） | 对话消息列表 |
| `custom_content` | string | 是（与 messages 互斥） | 自定义内容，最大 512 字符 |
| `memory_library_id` | string | 否 | 记忆库 ID，不传则使用默认记忆库 |
| `profile_schema` | string | 否 | 画像模板 ID |
| `meta_data` | object | 否 | 用户自定义信息 |

返回结果中 `memory_nodes` 数组包含变更的记忆片段，每个片段有 `memory_node_id`、`content` 和 `event`（ADD/UPDATE/DELETE）字段。

### SearchMemory - 搜索记忆片段

基于语义相似度搜索相关记忆片段，据[长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)，支持多种检索增强选项：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `user_id` | string | - | 必填，记忆实体 ID |
| `messages` | array | - | 必填，对话记录 |
| `top_k` | integer | 10 | 最大召回个数，取值 1~100 |
| `min_score` | double | 0.3 | 最小相似度分数阈值，值域 [0,1] |
| `enable_rerank` | boolean | false | 是否开启重排序 |
| `enable_judge` | boolean | false | 是否开启意图判别 |
| `enable_rewrite` | boolean | false | 是否开启 query 重写 |
| `project_ids` | list | - | 记忆片段规则 ID 数组，支持混合检索 |

### ListMemory - 列出记忆片段

分页查看用户的所有记忆片段，支持 `page_num`（默认 1）和 `page_size`（默认 10）分页参数。返回结果包含 `total`、`page_size`、`page_num` 分页信息以及 `memory_nodes` 列表。

### UpdateMemory - 更新记忆片段

通过 PATCH 方法更新指定记忆片段的内容。需要提供 `custom_content`（最大 512 字符）和 `user_id`，可选传入 `timestamp`（秒级 Unix 时间戳）和 `meta_data`（增量更新）。

### DeleteMemory - 删除记忆片段

通过 DELETE 方法删除指定 `memory_node_id` 对应的记忆片段。

## SDK 支持

根据[长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)，Python 开发者可使用 `agentscope-runtime` 包（需 >= 1.1.5）：

```bash
pip install agentscope-runtime>=1.1.5
```

SDK 提供了 `AddMemory`、`SearchMemory`、`ListMemory`、`DeleteMemory` 等异步接口封装。UpdateMemory 目前尚未提供 SDK 封装，需通过 `requests` 库直接调用 REST API。

## 使用限制

- **全部接口**：总计不超过 3000 QPM（阿里云账号级别）
- **记忆片段 add 接口**：120 QPM
- **记忆片段 search 接口**：300 QPM
- **AddMemory messages**：最多支持 50 条对话记录
- **custom_content / UpdateMemory**：内容最大 512 字符
- **user_id**：最大 64 字符
- **memory_library_id**：最大 32 字符
- 生成的记忆片段与用户画像暂无失效日期

## 来源文档

- [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)




