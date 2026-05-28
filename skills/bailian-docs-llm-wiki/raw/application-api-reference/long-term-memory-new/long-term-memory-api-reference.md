# 长期记忆（新）API 参考

长期记忆（新）的完整 API 接口参考文档，包含所有 API 的请求参数、返回结果和示例代码。

本文档提供长期记忆（新）功能的完整 API 接口参考。关于功能介绍和使用指南，请参见[长期记忆（新）](#)。

## 公共请求信息

**参数**

**说明**

Base URL

`https://dashscope.aliyuncs.com/api/v2/apps/memory/`

认证方式

在请求 Header 中添加 `Authorization: Bearer $DASHSCOPE_API_KEY`。API Key 的获取方式请参见[获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。

Content-Type

`application/json`

## 接口概览

长期记忆（新）提供以下 API 接口：

**接口名称**

**HTTP 方法**

**路径**

**说明**

AddMemory

POST

`/add`

添加记忆片段

SearchMemory

POST

`/memory_nodes/search`

搜索记忆片段

ListMemory

GET

`/memory_nodes`

列出记忆片段

DeleteMemory

DELETE

`/memory_nodes/{memory_node_id}`

删除记忆片段

UpdateMemory

PATCH

`/memory_nodes/{memory_node_id}`

更新记忆片段

CreateProfileSchema

POST

`/profile_schemas`

创建画像模板

ListProfileSchemas

GET

`/profile_schemas`

获取画像模板列表

DeleteProfileSchema

DELETE

`/profile_schemas/{profile_schema_id}`

删除画像模板

UpdateProfileSchema

PATCH

`/profile_schemas/{profile_schema_id}`

更新画像模板

GetProfileSchema

GET

`/profile_schemas/{profile_schema_id}`

获取画像模板详情

GetUserProfile

GET

`/profile_schemas/{profile_schema_id}/user_profile`

获取用户画像

## 使用限制

**限流（阿里云账号级别）：**

**API 接口**

**限流**

全部接口

总计不超过 3000 QPM

记忆片段 add 接口

120 QPM

记忆片段 search 接口

300 QPM

生成的记忆片段与用户画像暂无失效日期。

## 核心组件

### 1\. AddMemory - 添加记忆片段

将用户对话存储为记忆片段，自动提取关键信息和用户画像。

**请求体参数：**

**参数名**

**类型**

**必填**

**说明**

user\_id

string

是

记忆实体 ID，用于标识归属对象，最大 64 个字符

messages

array

是（与custom\_content互斥，填custom\_content后会忽略messages）

对话消息列表，每个消息包含 `role`（user/assistant）和 `content` 文本内容。

**说明**

最多支持50条对话记录。

一问一答算 2 条。

messages\[0\].role

string

\-

消息角色，可选值：`user`（用户消息）或 `assistant`（助手回复）

messages\[0\].content

string | array

\-

消息内容

custom\_content

string

是（与messages互斥，填custom\_content后会忽略messages）

自定义内容，最大 512 个字符（与messages互斥，填custom\_content后会忽略messages）

profile\_schema

string

否

[画像模板 ID](#4najl0a4ju096)，在记忆库详情页获取。

memory\_library\_id

string

否

记忆库 ID，最大 32 个字符，在[记忆库](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list)卡片上获取。

**说明**

如不传此参数，会自动选择默认记忆库ID。

project\_id

string

否

记忆片段规则 ID。

**说明**

如不传此参数，会自动选择指定记忆库的默认的记忆片段规则 ID。

meta\_data

object

否

用户自定义信息

**返回结果：**

返回字段包括：

-   `request_id` (string) - 请求ID
    
-   `memory_nodes` (array) - 变更的记忆片段列表，结构如下：
    

**字段**

**类型**

**说明**

memory\_node\_id

string

记忆片段 ID

content

string

记忆片段内容（从对话中提取）

event

string

操作事件类型：ADD（创建）、UPDATE（更新）、DELETE（删除）

old\_content

string

更新前的记忆片段内容，仅当 event 为"UPDATE"时有效

**示例代码：**

## cURL

```
# 添加记忆片段
curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/add \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "messages": [{
      "role": "user",
      "content": "你好"
    }, {
      "role": "assistant",
      "content": "你好，有什么可以帮您"
    }, {
      "role": "user",
      "content": "每天上午11点提醒我点外卖。"
    }, {
      "role": "assistant",
      "content": "没问题"
    }, {
      "role": "user",
      "content": "明天10点提醒我整理会议纪要。"
     }
    ],
    "user_id": "user_001",
    "memory_library_id": "xxx",
    "meta_data": {
      "location_name": "北京",
      "geo_coordinate": "116.481499,39.990475"
    }
  }'

# response
{
  "memory_nodes": [{
    "content": "用户要求每天上午11点提醒他点外卖",
    "event": "ADD",
    "memory_node_id": "50b46e9751504556a1a49a11b7639b3d"
  }, {
    "content": "用户要求明天10点提醒他整理会议纪要",
    "event": "ADD",
    "memory_node_id": "381cc694e4144dffbd546059189ce498"
  }],
  "request_id": "bec69131-627c-4636-a2ff-e71c0c8a5c53"
}

# 添加记忆片段（自定义内容）
curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/add \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "custom_content": "用户周末去上海参加WAIC",
    "user_id": "user_001",
    "meta_data": {
      "custom_key": "custom_value"
    }
  }'
```

## Python

**说明**

需要安装 agentscope-runtime，安装命令：`pip install agentscope-runtime>=1.1.5`

```
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
            meta_data={"category": "提醒", "priority": "中"}
        ))
        print(f"创建了 {len(result.memory_nodes)} 个记忆片段")
    finally:
        await add_memory.close()

asyncio.run(add_memory_example())
```

### 2\. SearchMemory - 搜索记忆片段

基于语义相似度搜索相关记忆片段。

**请求体参数：**

**参数名**

**类型**

**必填**

**说明**

user\_id

string

是

记忆实体 ID，用于标识归属对象，最大 64 个字符

messages

array

是

对话记录

messages\[0\].role

string

\-

消息角色，可选值：`user`（用户消息）或 `assistant`（助手回复）

messages\[0\].content

string | array

\-

消息内容

memory\_library\_id

string

否

记忆库 ID，最大 32 个字符，在记忆库卡片上获取。

**说明**

如不传此参数，会自动选择默认记忆库 ID。

project\_ids

list

否

记忆片段规则 ID 数组。可传入多记忆片段规则 ID 进行混合检索。

**说明**

如不传此参数，会自动选择指定记忆库的默认的记忆片段规则 ID。

top\_k

integer

否

最大召回个数，取值范围1~100（默认 10）

min\_score

double

否

最小相似度分数阈值，值域 \[0,1\]（默认 0.3）

enable\_rerank

boolean

否

是否开启搜索结果的重排序（默认 false）

enable\_judge

boolean

否

是否开启意图判别回调（默认 false）

enable\_rewrite

boolean

否

是否开启 query 重写（默认 false）

**返回结果：**

返回字段包括：

-   `request_id` (string) - 请求 ID
    
-   `memory_nodes` (array) - 记忆片段列表，包含以下字段：
    

**字段**

**类型**

**说明**

memory\_node\_id

string

记忆片段 ID

content

string

记忆片段内容（从对话中提取）

created\_at

long

创建时间

updated\_at

long

更新时间

**示例代码：**

## cURL

```
# 搜索记忆片段
curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/memory_nodes/search \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "user_id": "user_001",
    "memory_library_id": "xxx",
    "messages": [{
      "role": "user",
      "content": "你好"
    }, {
      "role": "assistant",
      "content": "你好"
    }, {
      "role": "user",
      "content": "明天上午十一点我有什么日程安排吗？"
    }],
    "top_k": 100,
    "min_score": 0
  }'

# response
{
  "memory_nodes": [{
    "updated_at": 1752941349,
    "created_at": 1752941349,
    "memory_node_id": "cce2393d894b477f8b207ba4d3aa70da",
    "content": "- 用户希望每天下午3点提醒他喝水\n- 用户最近在备考，且表示学习效率不高"
  }, {
    "updated_at": 1752941151,
    "created_at": 1752941151,
    "memory_node_id": "e9af5fbb696748d6b0133429e8c68b47",
    "content": "- 用户要求每天下午3点提醒他喝水\n- 用户最近在备考，学习效率不高，需要建议"
  }],
  "request_id": "cd6b32ef-a1ba-9ce1-af64-37f61e30e814"
}
```

## Python

**说明**

需要安装 agentscope-runtime，安装命令：`pip install agentscope-runtime>=1.1.5`

```
from agentscope_runtime.tools.modelstudio_memory import (
    SearchMemory, Message, SearchMemoryInput,
)
import asyncio

async def search_memory_example():
    search_memory = SearchMemory()
    try:
        result = await search_memory.arun(SearchMemoryInput(
            user_id="user_001",
            memory_library_id="xxx",
            messages=[Message(role="user", content="我需要做什么？")],
            top_k=5,
            min_score=0.5
        ))
        for node in result.memory_nodes:
            print(f"记忆片段: {node.content}")
    finally:
        await search_memory.close()

asyncio.run(search_memory_example())
```

### 3\. ListMemory - 列出记忆片段

分页查看用户的所有记忆片段。

**查询参数：**

**参数名**

**类型**

**必填**

**说明**

user\_id

string

是

记忆实体 ID，用于标识归属对象，最大 64 个字符

memory\_library\_id

string

否

记忆库 ID，最大 32 个字符，在[记忆库](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list)卡片上获取。

**说明**

如不传此参数，会自动选择默认记忆库 ID。

project\_id

string

否

记忆片段规则 ID。

**说明**

如不传此参数，会自动选择指定记忆库的默认的记忆片段规则 ID。

page\_num

integer

否

页码（从 1 开始，默认 1）

page\_size

integer

否

每页条目数（默认 10）

**返回结果：**

返回字段包括：

-   `request_id` (string) - 请求 ID
    
-   `memory_nodes` (array) - 记忆片段列表，包含以下字段：
    

**字段**

**类型**

**说明**

memory\_node\_id

string

记忆片段 ID

content

string

记忆片段内容（从对话中提取）

created\_at

long

创建时间

updated\_at

long

更新时间

meta\_data

object

用户自定义信息

分页字段：

-   `total` (integer) - 总数
    
-   `page_size` (integer) - 每页大小
    
-   `page_num` (integer) - 页号
    

**示例代码：**

## cURL

```
# 列出记忆片段
curl --location --request GET 'https://dashscope.aliyuncs.com/api/v2/apps/memory/memory_nodes?user_id=user_001&page_size=10&page_num=1' \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{}'

# response
{
  "memory_nodes": [{
    "updated_at": 1752941349,
    "created_at": 1752941349,
    "memory_node_id": "cce2393d894b477f8b207ba4d3aa70da",
    "content": "- 用户希望每天下午3点提醒他喝水\n- 用户最近在备考，且表示学习效率不高"
  }, {
    "updated_at": 1752941151,
    "created_at": 1752941151,
    "memory_node_id": "e9af5fbb696748d6b0133429e8c68b47",
    "content": "- 用户要求每天下午3点提醒他喝水\n- 用户最近在备考，学习效率不高，需要建议"
  }],
  "page_size": 10,
  "page_num": 1,
  "total": 100,
  "request_id": "cc2690f9f2b3485a93013e5705c91241"
}
```

## Python

**说明**

需要安装 agentscope-runtime，安装命令：`pip install agentscope-runtime>=1.1.5`

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
            page_num=1,
            page_size=10
        ))
        for node in result.memory_nodes:
            print(f"记忆片段 ID: {node.memory_node_id}, 内容: {node.content}")
    finally:
        await list_memory.close()

asyncio.run(list_memory_example())
```

### 4\. DeleteMemory - 删除记忆片段

删除指定的记忆片段。

**路径参数：**`memory_node_id` - 记忆片段 ID

**查询参数：**

**参数名**

**类型**

**必填**

**说明**

memory\_library\_id

string

否

记忆库 ID，最大 32 个字符，在记忆库卡片上获取。

**说明**

如不传此参数，会自动选择默认记忆库。

**示例代码：**

## cURL

```
# 删除记忆片段
curl --location --request DELETE 'https://dashscope.aliyuncs.com/api/v2/apps/memory/memory_nodes/{memory_node_id}' \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{}'

# response
{
  "request_id": "cc2690f9f2b3485a93013e5705c91241"
}
```

## Python

**说明**

需要安装 agentscope-runtime，安装命令：`pip install agentscope-runtime>=1.1.5`

```
from agentscope_runtime.tools.modelstudio_memory import (
    DeleteMemory, DeleteMemoryInput,
)
import asyncio

async def delete_memory_example():
    delete_memory = DeleteMemory()
    try:
        result = await delete_memory.arun(DeleteMemoryInput(
            user_id="user_001",
            memory_node_id="node_abc123"
        ))
        print(f"删除成功，request_id: {result.request_id}")
    finally:
        await delete_memory.close()

asyncio.run(delete_memory_example())
```

### 5\. UpdateMemory - 更新记忆片段

更新记忆片段内容。

**路径参数：**`memory_node_id` - 记忆片段 ID

**请求体参数：**

**参数名**

**类型**

**必填**

**说明**

custom\_content

string

是

要更新的记忆片段内容，最大 512 个字符

user\_id

string

是

记忆实体 ID，用于标识归属对象，最大 64 个字符

memory\_library\_id

string

否

记忆库 ID，最大 32 个字符，在[记忆库](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list)卡片上获取。

**说明**

如不传此参数，会自动选择默认记忆库。

timestamp

long

否

记忆片段对应事件发生时的时间戳（秒级 Unix 时间戳，默认当前时间）

meta\_data

object

否

用户自定义信息（增量更新）

**返回结果：**`request_id` (string) - 请求 ID

**示例代码：**

## cURL

```
# 更新记忆片段
curl --location --request PATCH 'https://dashscope.aliyuncs.com/api/v2/apps/memory/memory_nodes/{memory_node_id}' \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "user_id": "user_001",
    "memory_library_id": "xxx",
    "custom_content": "{new_memory_custom_content}",
    "timestamp": 1747278460,
    "meta_data": {
      "custom_key": "custom_value"
    }
  }'

# response
{
  "request_id": "23d4f8bf-5e39-43ef-925a-82cf7757ec70"
}
```

## Python

**说明**

Python SDK 暂未提供此接口的封装，以下示例通过 requests 库直接调用 API。安装命令：`pip install requests`

```
import os
import requests

api_key = os.getenv("DASHSCOPE_API_KEY")
memory_node_id = "MEMORY_NODE_ID"

response = requests.patch(
    f"https://dashscope.aliyuncs.com/api/v2/apps/memory/memory_nodes/{memory_node_id}",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    },
    json={
        "user_id": "user_001",
        "memory_library_id": "xxx",
        "custom_content": "{new_memory_custom_content}",
        "timestamp": 1747278460,
        "meta_data": {"custom_key": "custom_value"},
    },
)
print(response.json())
```

### 6\. CreateProfileSchema - 创建画像模板

**请求体参数：**

**参数名**

**类型**

**必填**

**说明**

memory\_library\_id

string

否

记忆库 ID，最大 32 个字符，在记忆库卡片上获取。

**说明**

如不传此参数，会自动选择默认记忆库ID。

name

string

是

模板名称，最大 32 个字符

description

string

否

模板描述，最大 128 个字符

attributes

array

是

模板的属性维度数组

attributes\[0\].name

string

是

属性名称，最大 32 个字符。应该尽可能保证在语义中唯一，不然会对抽取效果有一定影响，如\["姓名"、"名称"、"名字"\]，\["年龄"，"年纪"，"岁数"\]不应该同时出现

attributes\[0\].description

string

否

描述，最大 128 个字符

attributes\[0\].default\_value

string

否

初始值，最大 128 个字符，选填

**返回结果：**

-   `request_id` (string) - 请求 ID
    
-   `profile_schema_id` (string) - 画像模板 ID
    

**示例代码：**

## cURL

```
# 创建画像模板
curl --location "https://dashscope.aliyuncs.com/api/v2/apps/memory/profile_schemas" \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "{your_profile_schema_name}",
    "description": "{schema_description}",
    "attributes": [
      {"name": "年龄", "description": "用户的年龄", "default_value": "18"},
      {"name": "年龄段", "description": "用户当前所处的年龄阶段（如小学生、初中生、高中生、大学生、青年、中年、老年等）。"},
      {"name": "民族", "description": "用户的民族或种族背景。"},
      {"name": "性别", "description": "用户的性别认同或自我表达。"},
      {"name": "家庭成员", "description": "提及的家庭成员及其关系（如父母、兄弟姐妹、子女等）。"},
      {"name": "居住地", "description": "用户目前居住的城市、地区或国家。"},
      {"name": "饮食习惯", "description": "用户是否有特定饮食偏好或限制（如素食、忌口、节食、酸甜苦辣咸等）。"},
      {"name": "爱好", "description": "用户提到的兴趣爱好、休闲活动等。"},
      {"name": "使用平台", "description": "用户常使用的社交平台、内容平台或设备系统。"},
      {"name": "内容偏好", "description": "用户喜欢阅读或观看的内容类型（如新闻、娱乐、科技、动漫等）。"},
      {"name": "宠物", "description": "用户是否养宠物及其种类、数量。"},
      {"name": "宗教限制", "description": "用户的宗教信仰及相关的禁忌或行为规范。"},
      {"name": "童年经历", "description": "用户提及的童年记忆、成长环境等。"},
      {"name": "人生事件", "description": "用户经历的重要人生节点（如升学、毕业、就业、搬家等）。"},
      {"name": "收藏品/所有物", "description": "用户拥有的贵重物品、收藏品或特别提及的物品。"},
      {"name": "游戏", "description": "用户玩的游戏类型、偏好或成就。"},
      {"name": "负面情绪", "description": "用户表达的焦虑、压力、不满或困扰。"},
      {"name": "幸福来源", "description": "用户提到的让自己感到幸福、满足的事物或经历。"},
      {"name": "家庭关系", "description": "用户与家人之间的关系质量（如亲密、疏远、冲突等）。"},
      {"name": "人生理想/目标", "description": "用户的长远目标、梦想或人生规划。"},
      {"name": "社会关系（朋友圈）", "description": "用户的朋友圈构成、社交习惯或重要社交关系。"},
      {"name": "近期活动", "description": "用户近期所进行的活动或行为。"}
    ]
  }'

# response
{
  "profile_schema_id": "d148aac7f4ff42f598e3fcbc6eae4de3",
  "request_id": "23d4f8bf-5e39-43ef-925a-82cf7757ec70"
}
```

## Python

**说明**

需要安装 agentscope-runtime，安装命令：`pip install agentscope-runtime>=1.1.5`

```
from agentscope_runtime.tools.modelstudio_memory import (
    CreateProfileSchema, ProfileAttribute, CreateProfileSchemaInput,
)
import asyncio

async def create_schema_example():
    create_schema = CreateProfileSchema()
    try:
        result = await create_schema.arun(CreateProfileSchemaInput(
            name="用户基础画像",
            description="包含年龄、兴趣和职业的用户信息",
            attributes=[
                ProfileAttribute(name="年龄", description="用户年龄"),
                ProfileAttribute(name="爱好", description="用户的兴趣爱好"),
                ProfileAttribute(name="职业", description="用户职业"),
            ]
        ))
        print(f"创建的画像模板 ID: {result.profile_schema_id}")
    finally:
        await create_schema.close()

asyncio.run(create_schema_example())
```

### 7\. ListProfileSchemas - 获取画像模板列表

分页获取所有画像模板列表。

**查询参数：**

**参数名**

**类型**

**必填**

**说明**

memory\_library\_id

string

否

记忆库 ID，最大 32 个字符，在[记忆库](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list)卡片上获取。

**说明**

如不传此参数，会自动选择默认记忆库ID。

page\_size

integer

否

每页条目数（默认 10）

page\_num

integer

否

页码（从 1 开始，默认 1）

**返回结果：**

-   `request_id` (string) - 请求 ID
    
-   `profile_schemas` (array) - 画像模板列表，每个模板包含：
    
-   `name` (string) - 画像模板名称
    
-   `description` (string) - 画像模板描述
    
-   `profile_schema_id` (string) - 画像模板 ID
    
-   `total` (integer) - 总数
    

**示例代码：**

## cURL

```
# 获取画像模板列表
curl --location --request GET 'https://dashscope.aliyuncs.com/api/v2/apps/memory/profile_schemas?page_size=10&page_num=1' \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{}'

# response
{
  "profile_schemas": [
    {
      "name": "{your_profile_schema_name}",
      "description": "{schema_description}",
      "profile_schema_id": "2dd5b7961ac44630949db7533f796b18"
    },
    {
      "description": "测试description",
      "name": "测试profile_schema",
      "profile_schema_id": "fa06b80b08e1445bb128d2ea8373aef3"
    }
  ],
  "request_id": "25b10053-194d-48e2-9189-3e3d868afcf2",
  "total": 2
}
```

## Python

**说明**

Python SDK 暂未提供此接口的封装，以下示例通过 requests 库直接调用 API。安装命令：`pip install requests`

```
import os
import requests

api_key = os.getenv("DASHSCOPE_API_KEY")

response = requests.get(
    "https://dashscope.aliyuncs.com/api/v2/apps/memory/profile_schemas",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    },
    params={"page_size": 10, "page_num": 1},
)
result = response.json()
for schema in result.get("profile_schemas", []):
    print(f"模板: {schema['name']} (ID: {schema['profile_schema_id']})")
print(f"总数: {result.get('total')}")
```

### 8\. DeleteProfileSchema - 删除画像模板

删除指定的画像模板。

**路径参数：**`profile_schema_id` - 画像模板 ID

**查询参数：**`memory_library_id`：记忆库 ID，最大 32 个字符，在[记忆库](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list)卡片上获取。

**说明**

如不传此参数，会自动选择默认记忆库ID。

**返回结果：**`request_id` (string) - 请求ID

**示例代码：**

## cURL

```
# 删除画像模板
curl --location --request DELETE 'https://dashscope.aliyuncs.com/api/v2/apps/memory/profile_schemas/{profile_schema_id}' \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{}'

# response
{
  "request_id": "23d4f8bf-5e39-43ef-925a-82cf7757ec70"
}
```

## Python

**说明**

Python SDK 暂未提供此接口的封装，以下示例通过 requests 库直接调用 API。安装命令：`pip install requests`

```
import os
import requests

api_key = os.getenv("DASHSCOPE_API_KEY")
profile_schema_id = "PROFILE_SCHEMA_ID"

response = requests.delete(
    f"https://dashscope.aliyuncs.com/api/v2/apps/memory/profile_schemas/{profile_schema_id}",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    },
    json={},
)
print(response.json())
```

### 9\. UpdateProfileSchema - 更新画像模板

更新画像模板的名称、描述和属性。

**路径参数：**`profile_schema_id` - 画像模板 ID

**请求体参数：**

**参数名**

**类型**

**必填**

**说明**

memory\_library\_id

string

否

记忆库 ID，最大 32 个字符，在[记忆库](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list)卡片上获取。

**说明**

如不传此参数，会自动选择默认记忆库ID。

name

string

否

模板名称，最大 32 个字符

description

string

否

模板描述，最大 128 个字符

attributes\_operations

array

否

属性操作列表

attributes\_operations\[0\].op

string

是

操作类型：`add`（新增属性）、`update`（更新属性）、`delete`（删除属性）

attributes\_operations\[0\].attribute\_id

string

否

要操作的属性标识（操作类型为更新或删除时必填）

attributes\_operations\[0\].name

string

否

属性名称，最大 32 个字符（操作类型为新增时必填）

attributes\_operations\[0\].description

string

否

描述，最大 128 个字符

attributes\_operations\[0\].default\_value

string

否

默认值，最大 128 个字符

**返回结果：**`request_id` (string) - 请求ID

**示例代码：**

## cURL

```
# 更新画像模板
curl --location --request PATCH 'https://dashscope.aliyuncs.com/api/v2/apps/memory/profile_schemas/{profile_schema_id}' \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "New Schema Name",
    "description": "New schema description",
    "attributes_operations": [
      {
        "op": "add",
        "name": "plan",
        "description": "User subscription plan",
        "default_value": "free"
      },
      {
        "op": "update",
        "attribute_id": "attr_1",
        "name": "plan_v2",
        "description": "Updated description",
        "default_value": null
      },
      {
        "op": "delete",
        "attribute_id": "attr_2"
      }
    ]
  }'

# response
{
  "request_id": "733715b5-23b1-4bf5-87b7-076f72e7181f"
}
```

## Python

**说明**

Python SDK 暂未提供此接口的封装，以下示例通过 requests 库直接调用 API。安装命令：`pip install requests`

```
import os
import requests

api_key = os.getenv("DASHSCOPE_API_KEY")
profile_schema_id = "PROFILE_SCHEMA_ID"

response = requests.patch(
    f"https://dashscope.aliyuncs.com/api/v2/apps/memory/profile_schemas/{profile_schema_id}",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    },
    json={
        "name": "New Schema Name",
        "description": "New schema description",
        "attributes_operations": [
            {
                "op": "add",
                "name": "plan",
                "description": "User subscription plan",
                "default_value": "free",
            },
            {
                "op": "update",
                "attribute_id": "attr_1",
                "name": "plan_v2",
                "description": "Updated description",
                "default_value": None,
            },
            {
                "op": "delete",
                "attribute_id": "attr_2",
            },
        ],
    },
)
print(response.json())
```

### 10\. GetProfileSchema - 获取画像模板详情

获取指定画像模板的详细信息。

**路径参数：**`profile_schema_id` - 画像模板 ID

**查询参数：**`memory_library_id`：记忆库 ID，最大 32 个字符，在[记忆库](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list)卡片上获取。

**说明**

如不传此参数，会自动选择默认记忆库ID。

**返回结果：**

-   `request_id` (string) - 请求ID
    
-   `name` (string) - 画像模板名称
    
-   `description` (string) - 画像模板描述
    
-   `attributes` (array) - 属性列表，每个属性包含：
    
-   `attribute_id` (string) - 属性ID
    
-   `name` (string) - 名称
    
-   `description` (string) - 描述
    
-   `default_value` (string) - 属性初始值
    

**示例代码：**

## cURL

```
# 获取画像模板详情
curl --location --request GET 'https://dashscope.aliyuncs.com/api/v2/apps/memory/profile_schemas/{profile_schema_id}' \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{}'

# response
{
  "attributes": [
    {
      "attribute_id": "0050023926374ef397b9cf06542a287c",
      "default_value": "更新default_value",
      "description": "更新attribute",
      "name": "更新attribute"
    },
    {
      "attribute_id": "0270aff7e631425c91595455ff8a65cf",
      "description": "用户的长远目标、梦想或人生规划。",
      "name": "人生理想/目标"
    },
    {
      "attribute_id": "092fc04dd42241f5842dedb1ec6d9575",
      "description": "提及的家庭成员及其关系（如父母、兄弟姐妹、子女等）。",
      "name": "家庭成员"
    }
  ],
  "name": "{your_profile_schema_name}",
  "description": "{schema_description}",
  "request_id": "22e73019-c24d-4885-9cbd-89e6cb7ca801"
}
```

## Python

**说明**

Python SDK 暂未提供此接口的封装，以下示例通过 requests 库直接调用 API。安装命令：`pip install requests`

```
import os
import requests

api_key = os.getenv("DASHSCOPE_API_KEY")
profile_schema_id = "PROFILE_SCHEMA_ID"

response = requests.get(
    f"https://dashscope.aliyuncs.com/api/v2/apps/memory/profile_schemas/{profile_schema_id}",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    },
)
result = response.json()
print(f"模板名称: {result.get('name')}")
print(f"模板描述: {result.get('description')}")
for attr in result.get("attributes", []):
    print(f"  属性: {attr['name']} - {attr.get('description', '')}")
```

### 11\. GetUserProfile - 获取用户画像

获取系统自动提取的用户画像信息。

**路径参数：**`profile_schema_id` - 画像模板 ID

**查询参数：**

-   `user_id` - 记忆实体 ID，用于标识归属对象，最大 64 个字符
    
-   `memory_library_id`：记忆库 ID，最大 32 个字符，在[记忆库](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list)卡片上获取。
    
    **说明**
    
    如不传此参数，会自动选择默认记忆库ID。
    

**返回结果：**

返回字段包括：

-   `request_id` (string) - 请求ID
    
-   `profile` (object) - 用户画像对象，包含以下字段：
    

**字段**

**类型**

**说明**

schema\_name

string

画像模板名称

schema\_description

string

画像模板描述

attributes

array

属性列表，每个属性包含以下字段：

**attributes 字段：**

**字段**

**类型**

**说明**

id

string

属性 ID

name

string

名称

value

string

value（提取的属性值，未提取时不存在此字段）

**示例代码：**

## cURL

```
# 获取用户画像
curl --location --request GET 'https://dashscope.aliyuncs.com/api/v2/apps/memory/profile_schemas/{profile_schema_id}/user_profile?user_id={user_id}' \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{}'

# response
{
  "profile": {
    "attributes": [
      {
        "id": "00484806d4a343198d61abe8a0d8ae84",
        "name": "家庭关系"
      },
      {
        "id": "05fa398b8386454999a685d246bb2f91",
        "name": "使用平台"
      },
      {
        "id": "09100265f3d341a79e2916fa623b9ffc",
        "name": "宗教限制"
      },
      {
        "id": "14bb432a07c64dad82033e2613db7a9c",
        "name": "人生事件",
        "value": "27岁生日"
      },
      {
        "id": "15c3d7da69584e7c8b9b51c62afc121b",
        "name": "游戏"
      },
      {
        "id": "2f4d4a48125a45beb22f45f7578b167e",
        "name": "内容偏好"
      },
      {
        "id": "4d4a765760c749d082d82eb81029bd44",
        "name": "爱好"
      },
      {
        "id": "614991ce106b4e27a369c04204cd4412",
        "name": "民族"
      },
      {
        "id": "6cc071fb3e764128a2313443bff7eb70",
        "name": "负面情绪"
      },
      {
        "id": "8afa889cbe504ff69551d729a1a0df53",
        "name": "收藏品/所有物"
      },
      {
        "id": "8f73380e494b4b0fab6da1ed64b27eee",
        "name": "性别",
        "value": "男"
      },
      {
        "id": "8fb150e4acf8421cb2825c382e695ea2",
        "name": "家庭成员"
      },
      {
        "id": "93d5d2cb8b8b4b3bbfdea44a69b63642",
        "name": "近期活动",
        "value": "整理会议纪要"
      },
      {
        "id": "a118ec78a5874251b1892e148eef76d7",
        "name": "宠物",
        "value": "一只叫伊恩的小狗"
      },
      {
        "id": "a7a1023d69b74e23852165ffe1a7d249",
        "name": "年龄段",
        "value": "青年"
      },
      {
        "id": "aeb1c823222f4cdd849859403b2a9ff5",
        "name": "年龄",
        "value": "27岁"
      },
      {
        "id": "dca26843674945c59d7b822ae51c8f33",
        "name": "幸福来源"
      },
      {
        "id": "e11e8a29dd3b4c71b26bbd9b4283f65e",
        "name": "饮食习惯"
      },
      {
        "id": "f040cf561d8d461693d9d768ddcaa86c",
        "name": "人生理想/目标"
      },
      {
        "id": "f0c6744a65e44c2991e6b04864f05d6c",
        "name": "居住地"
      },
      {
        "id": "fe1be71415c6436f849064aeb781d7c3",
        "name": "社会关系（朋友圈）"
      },
      {
        "id": "ff87d78ca1e24018985d80157d1dc266",
        "name": "童年经历"
      }
    ],
    "schema_description": "用户画像001的描述",
    "schema_name": "用户画像001"
  },
  "request_id": "e5986fe3-6f2b-4381-892b-01528443790e"
}
```

## Python

**说明**

需要安装 agentscope-runtime，安装命令：`pip install agentscope-runtime>=1.1.5`

```
from agentscope_runtime.tools.modelstudio_memory import (
    GetUserProfile, GetUserProfileInput,
)
import asyncio

async def get_profile_example():
    get_profile = GetUserProfile()
    try:
        result = await get_profile.arun(GetUserProfileInput(
            schema_id="schema_abc123",
            user_id="user_001"
        ))
        for attr in result.profile.attributes:
            print(f"{attr.name}: {attr.value or '未提取'}")
    finally:
        await get_profile.close()

asyncio.run(get_profile_example())
```

## 错误处理

调用记忆库相关 API 时可能遇到以下常见错误：

**错误码**

**HTTP 状态码**

**说明**

**处理建议**

InvalidApiKey

401

API Key 无效或未配置

检查环境变量 DASHSCOPE\_API\_KEY 是否正确配置

UserNotFound

404

指定的 user\_id 不存在

确认 user\_id（记忆实体 ID）正确，或先调用 AddMemory 添加记忆片段

TooManyRequests

429

请求频率超过限制

降低请求频率，建议两次请求间隔至少 1 秒

InternalError

500

服务内部错误

稍后重试，如持续出现请联系技术支持

更多错误码信息，请参考[错误码](https://help.aliyun.com/zh/model-studio/error-code)。
