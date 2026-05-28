# 长期记忆 API

AI 在长对话中会遗忘关键信息，且跨会话没有记忆，导致上下文丢失、体验不连贯。为解决此痛点，我们引入了长期记忆功能。该功能可自动从历史对话中提炼并结构化存储记忆片段与用户画像。在后续对话或新会话中，开发者可以检索这些记忆并将其注入 Prompt，赋能 AI 实现真正的持续性理解。

## 核心功能

**说明**

该功能与 API 调用限时免费。

-   **记忆片段**：从对话自动提取关键内容并结构化存储为记忆片段；也可以直接指定要存入的记忆内容；支持基于历史对话检索和动态更新。
    
-   **用户画像**：基于自定义画像模板，从对话中提取结构化用户属性（如年龄、职业、兴趣等）。
    

记忆片段适用于大多数长期记忆场景；当需要抽取固定属性时，建议搭配用户画像功能使用该功能。

生成的记忆片段与用户画像暂无失效日期。

## **适用范围**

长期记忆功能通过开放的 API 接口，可接入任意应用，也支持多应用共享同一记忆库。

## 相比[旧版长期记忆 API](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-dir-long-term-memory/)的改进

-   **速度与效率高：**拥有更低的延迟，更高的记忆检索召回效果。
    
-   **自动提取能力**：支持从对话中自动提取关键信息，自动去重，无需手动输入。
    
-   **检索算法优化**：新增语义检索能力，检索准确性显著提升，响应速度更快。
    
-   **用户画像能力**：新增完整的用户画像提取和管理能力。
    

## 使用方法

使用前需要配置环境变量`DASHSCOPE_API_KEY`，获取与配置方式请参考[获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。

## 添加记忆片段

-   **建立记忆**：通过 `AddMemory` 保存上一轮对话内容，转换为记忆片段并构建语义索引。
    
-   **检索记忆**：通过 `SearchMemory` 基于语义检索相关历史记忆。
    

**最佳实践：**在每轮对话结束后及时调用 AddMemory 保存记忆，检索时建议将 `top_k` 设置在 3 到 10 之间，平衡性能和效果。

## cURL

```
# 添加记忆
curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/add \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "messages": [
      {"role": "user", "content": "每天上午9点提醒我喝水"},
      {"role": "assistant", "content": "好的，已记录"},
      {"role": "user", "content": "明天10点提醒我整理会议纪要。"}
    ],
    "user_id": "user_001",
    "memory_library_id": "your_memory_library_id",
    "project_id": "your_project_id",
    "profile_schema": "your_profile_schema_id",
    "meta_data": {
      "location_name": "北京"
    }
  }'
# memory_library_id：非必填，记忆库 ID，在记忆库卡片上获取。不填则使用默认记忆库。
# project_id：非必填，记忆片段规则 ID，在记忆库详情页的记忆规则中获取。
# profile_schema：非必填，用户画像规则 ID，在记忆库详情页的记忆规则中获取。
# meta_data：非必填，自定义元数据，用于对记忆进行分类管理。

# 添加记忆（自定义内容）
curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/add \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "custom_content": "用户周末去上海参加WAIC",
    "user_id": "user_001",
    "memory_library_id": "your_memory_library_id",
    "meta_data": {
      "custom_key": "custom_value"
    }
  }'

# 搜索记忆
curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/memory_nodes/search \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "user_id": "user_001",
    "memory_library_id": "your_memory_library_id",
    "messages": [
      {"role": "user", "content": "我需要做什么？"}
    ],
    "top_k": 5
  }'
```

## 更新记忆片段

**管理记忆**：通过 `ListMemory`、`UpdateMemory`、`DeleteMemory` 管理记忆片段，支持元数据分类和智能去重。

**最佳实践：**使用元数据对记忆进行分类管理（如按类别、优先级等），便于后续的精确检索和管理。

## cURL

```
# 添加记忆
curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/add \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "user_id": "user_001",
    "messages": [
      {"role": "user", "content": "每天上午9点提醒我喝水"},
      {"role": "assistant", "content": "好的，已记录"}
    ]
  }'

# 列出记忆
curl --location --request GET 'https://dashscope.aliyuncs.com/api/v2/apps/memory/memory_nodes?user_id=user_001&page_size=10&page_num=1' \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{}'

# 更新记忆
curl --location --request PATCH 'https://dashscope.aliyuncs.com/api/v2/apps/memory/memory_nodes/{memory_node_id}' \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "user_id": "user_001",
    "custom_content": "还要提醒我上午10点吃药。"
  }'

# 查看更新的记忆
curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/memory_nodes/search \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "user_id": "user_001",
    "memory_library_id": "your_memory_library_id",
    "messages": [
      {"role": "user", "content": "我需要做什么？"}
    ],
    "top_k": 5
  }'

# 删除记忆
curl --location --request DELETE 'https://dashscope.aliyuncs.com/api/v2/apps/memory/memory_nodes/{memory_node_id}' \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{}'
```

## 提取用户画像

-   **创建画像模板**：通过 `CreateProfileSchema` 定义需要提取的用户属性。
    
-   **提取画像**：调用 `AddMemory` 时传入画像模板 ID，从对话中提取用户属性并更新画像。
    
-   **获取画像**：通过 `GetUserProfile` 获取完整的用户画像信息。
    

**最佳实践：**画像字段及描述应该清晰、具体，避免过于抽象。属性名称应尽可能保证在语义中唯一，如\["姓名"、"名称"、"名字"\]、\["年龄"、"年纪"、"岁数"\]不应同时出现，否则会对抽取效果有一定影响。不应期望一次对话就能提取所有信息，应通过多轮对话收集。

## cURL

```
# 创建画像 Schema
curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/profile_schemas \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "用户基础画像",
    "description": "包含年龄和兴趣的用户信息",
    "attributes": [
      {"name": "年龄", "description": "用户年龄"},
      {"name": "爱好", "description": "用户的兴趣爱好"},
      {"name": "职业", "description": "用户职业"}
    ]
  }'

# 添加包含画像信息的对话（使用上面返回的 profile_schema_id）
curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/add \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "user_id": "user_001",
    "messages": [
      {"role": "user", "content": "我今年28岁，是一名软件工程师。周末喜欢踢足球。"},
      {"role": "assistant", "content": "很高兴认识你！"}
    ],
    "profile_schema": "YOUR_SCHEMA_ID"
  }'

# 获取用户画像（等待3秒后执行）
curl -X GET "https://dashscope.aliyuncs.com/api/v2/apps/memory/profile_schemas/{YOUR_SCHEMA_ID}/user_profile?user_id=user_001" \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json"
```

## 环境变量配置

环境变量

必需

默认值

说明

`DASHSCOPE_API_KEY`

是

\-

百炼 API 密钥，获取方式请参见[获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)

## API 参考

完整的 API 接口参考（包括请求参数、返回结果和示例代码），请参见[长期记忆（新）API 参考](https://help.aliyun.com/zh/model-studio/long-term-memory-api-reference)。该文档也包含错误码说明及对应的处理建议。

## 相关文档

如需通过百炼控制台使用和管理本文介绍的长期记忆与用户画像功能，请参见[记忆库](https://help.aliyun.com/zh/model-studio/memory-library)。

## **常见问题**

### **API 是否存在限流？**

**API 接口**

**限流（阿里云账号级别）**

全部接口

总计不超过 3000 QPM

记忆片段 add 接口

120 QPM

记忆片段 search 接口

300 QPM
