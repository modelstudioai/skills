# long term memory new

百炼平台的长期记忆（新）功能提供了一套完整的 RESTful API，用于将用户对话自动提取为结构化记忆片段，并支持语义搜索召回。该功能适用于需要跨会话记住用户偏好、待办事项、个人信息等场景的 AI 应用。所有接口通过 DashScope API 网关访问，详细参数说明见[长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。

## 公共请求信息

- **Base URL**：`https://dashscope.aliyuncs.com/api/v2/apps/memory/`
- **认证方式**：在请求 Header 中添加 `Authorization: Bearer $DASHSCOPE_API_KEY`
- **Content-Type**：`application/json`

## 接口概览

长期记忆（新）共提供 11 个 API 接口，分为两大类：

### 记忆片段管理

| 接口 | 方法 | 路径 | 说明 |
|------|------|------|------|
| AddMemory | POST | `/add` | 添加记忆片段 |
| SearchMemory | POST | `/memory_nodes/search` | 语义搜索记忆片段 |
| ListMemory | GET | `/memory_nodes` | 分页列出记忆片段 |
| DeleteMemory | DELETE | `/memory_nodes/{memory_node_id}` | 删除记忆片段 |
| UpdateMemory | PATCH | `/memory_nodes/{memory_node_id}` | 更新记忆片段 |

### 画像模板管理

| 接口 | 方法 | 路径 | 说明 |
|------|------|------|------|
| CreateProfileSchema | POST | `/profile_schemas` | 创建画像模板 |
| ListProfileSchemas | GET | `/profile_schemas` | 获取画像模板列表 |
| GetProfileSchema | GET | `/profile_schemas/{profile_schema_id}` | 获取画像模板详情 |
| UpdateProfileSchema | PATCH | `/profile_schemas/{profile_schema_id}` | 更新画像模板 |
| DeleteProfileSchema | DELETE | `/profile_schemas/{profile_schema_id}` | 删除画像模板 |
| GetUserProfile | GET | `/profile_schemas/{profile_schema_id}/user_profile` | 获取用户画像 |

## 核心接口详解

### AddMemory - 添加记忆片段

将用户对话或自定义内容存储为记忆片段，系统自动提取关键信息并生成用户画像。支持两种输入方式（互斥）：

- **messages**：传入对话消息列表（最多 50 条记录），每条包含 `role`（user/assistant）和 `content`
- **custom_content**：直接传入自定义文本（最大 512 字符）

关键参数：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `user_id` | string | 是 | 记忆实体 ID，最大 64 字符 |
| `messages` | array | 与 custom_content 互斥 | 对话消息列表 |
| `custom_content` | string | 与 messages 互斥 | 自定义内容，最大 512 字符 |
| `memory_library_id` | string | 否 | 记忆库 ID，不传则使用默认记忆库 |
| `profile_schema` | string | 否 | 画像模板 ID |
| `meta_data` | object | 否 | 用户自定义元数据 |

返回结果中的 `memory_nodes` 数组包含变更的记忆片段，每个节点有 `event` 字段标识操作类型（ADD/UPDATE/DELETE）。

### SearchMemory - 搜索记忆片段

基于语义相似度搜索相关记忆片段，支持多种检索增强选项。根据[长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)，搜索接口支持以下高级参数：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `top_k` | integer | 10 | 最大召回个数，范围 1~100 |
| `min_score` | double | 0.3 | 最小相似度分数阈值，范围 [0,1] |
| `enable_rerank` | boolean | false | 是否开启搜索结果重排序 |
| `enable_judge` | boolean | false | 是否开启意图判别回调 |
| `enable_rewrite` | boolean | false | 是否开启 query 重写 |
| `project_ids` | list | - | 记忆片段规则 ID 数组，支持多规则混合检索 |

### UpdateMemory - 更新记忆片段

通过 PATCH 方法更新指定记忆片段的内容。需要在路径中传入 `memory_node_id`，请求体中必须包含 `custom_content`（最大 512 字符）和 `user_id`。可选传入 `timestamp`（秒级 Unix 时间戳）标记事件发生时间，`meta_data` 为增量更新。

### ListMemory / DeleteMemory

- **ListMemory**：GET 请求，通过 `page_num` 和 `page_size` 参数分页查询指定用户的所有记忆片段，返回结果包含分页信息（`total`、`page_size`、`page_num`）
- **DeleteMemory**：DELETE 请求，通过路径参数 `memory_node_id` 删除指定记忆片段

## SDK 支持

Python 开发者可使用 `agentscope-runtime` 包（需 v1.1.5+）调用记忆片段管理接口：

```bash
pip install agentscope-runtime>=1.1.5
```

该 SDK 封装了 `AddMemory`、`SearchMemory`、`ListMemory`、`DeleteMemory` 等异步接口，均通过 `arun()` 方法调用。

> **注意**：UpdateMemory 接口的 Python SDK 封装暂未提供，需通过 `requests` 库直接调用 REST API。

## 使用限制

根据[长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)，限流规则如下（阿里云账号级别）：

| 接口 | 限流 |
|------|------|
| 全部接口合计 | 3000 QPM |
| 记忆片段 add 接口 | 120 QPM |
| 记忆片段 search 接口 | 300 QPM |

其他注意事项：

- 生成的记忆片段与用户画像暂无失效日期
- `messages` 最多支持 50 条对话记录（一问一答算 2 条）
- `custom_content` 最大 512 个字符
- `user_id` 最大 64 个字符，`memory_library_id` 最大 32 个字符

## 来源文档

- [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)


