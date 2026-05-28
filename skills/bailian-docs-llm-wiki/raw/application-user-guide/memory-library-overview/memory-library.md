# 记忆库

大模型受上下文窗口限制，跨会话无法保留记忆，导致每次对话都从零开始。记忆库通过自动提取对话中的关键信息并持久化存储，使智能体能够跨会话持续引用用户偏好和历史信息，提供个性化、连贯的对话体验。

## **概述**

大模型受上下文窗口限制，无法跨会话保留信息。记忆库通过自动从对话中提取关键信息并持久化存储，在后续对话中基于语义检索相关记忆并注入上下文，使智能体能够持续理解用户偏好和历史信息。记忆库提供开放的 API 接口，可接入任意应用，也支持多应用共享同一记忆库。

记忆库支持两种记忆内容：

-   **记忆片段**：从对话中自动提取的关键事件和信息，如"用户每天上午9点需要喝水提醒"。适用于大多数长期记忆场景。
    
-   **用户画像**：基于自定义模板从对话中提取的结构化属性，如年龄、职业、偏好等。适用于需要固定属性的场景。
    

**使用流程：**

1.  获取 API Key，创建或使用默认记忆库。
    
2.  每轮对话结束后，调用 AddMemory 写入记忆。
    
3.  在控制台查看和检索记忆，或调用 SearchMemory 在应用中检索。
    
4.  将检索结果注入 Prompt，实现个性化回答。
    

## **快速开始**

以下示例使用默认记忆库，3 步快速体验记忆的写入、查看和检索。如需自定义记忆规则，请参见[创建记忆库](#heading-create)。

### **步骤一：写入记忆**

调用 [AddMemory](https://help.aliyun.com/zh/model-studio/long-term-memory-api-reference) 接口，将对话传入记忆库。调用前需配置 `DASHSCOPE_API_KEY`，获取方式请参考[获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。

#### **代码示例：写入记忆**

## cURL

```
curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/add \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "messages": [
      {"role": "user", "content": "每天上午9点提醒我喝水"},
      {"role": "assistant", "content": "好的，已记录"},
      {"role": "user", "content": "明天10点提醒我整理会议纪要。"}
    ],
    "user_id": "user_001"
  }'
```

## Python

**说明**

需要安装 agentscope-runtime，安装命令：`pip install agentscope-runtime`

```
from agentscope_runtime.tools.modelstudio_memory import (
    AddMemory, AddMemoryInput, Message,
)
import asyncio

async def add_memory_example():
    add_memory = AddMemory()
    try:
        await add_memory.arun(AddMemoryInput(
            user_id="user_001",
            messages=[
                Message(role="user", content="每天上午9点提醒我喝水"),
                Message(role="assistant", content="好的，已记录"),
                Message(role="user", content="明天10点提醒我整理会议纪要。"),
            ]
        ))
        print("记忆写入成功")
    finally:
        await add_memory.close()

asyncio.run(add_memory_example())
```

### **步骤二：在控制台查看记忆**

1.  登录[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list)，进入默认记忆库的**记忆详情**标签页。
    
2.  在**记忆实体 ID**中输入 `user_001`，单击**查看**，即可看到系统从对话中自动提取的记忆片段。
    

#### **代码示例：列出记忆**

## cURL

```
curl -X GET "https://dashscope.aliyuncs.com/api/v2/apps/memory/memory_nodes?user_id=user_001&page_size=10&page_num=1" \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json"
```

## Python

**说明**

需要安装 agentscope-runtime，安装命令：`pip install agentscope-runtime`

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
            page_size=10,
            page_num=1
        ))
        for node in result.memory_nodes:
            print(f"记忆: {node.content}")
    finally:
        await list_memory.close()

asyncio.run(list_memory_example())
```

### **步骤三：在控制台检索记忆**

1.  切换到**记忆检索**标签页，输入**记忆实体 ID**为 `user_001`。
    
2.  在**输入**框输入"我需要做什么？"，点击**运行**，查看系统返回的相关记忆。
    

#### **代码示例：检索记忆**

## cURL

```
curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/search \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "user_id": "user_001",
    "query": "我需要做什么？"
  }'
```

## Python

**说明**

需要安装 agentscope-runtime，安装命令：`pip install agentscope-runtime`

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
            messages=[Message(role="user", content="我需要做什么？")]
        ))
        for node in result.memory_nodes:
            print(f"记忆: {node.content}")
    finally:
        await search_memory.close()

asyncio.run(search_memory_example())
```

如需在应用中集成检索能力，请参见 [SearchMemory API](https://help.aliyun.com/zh/model-studio/long-term-memory-api-reference)。

## **创建记忆库**

创建[记忆库](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list)并配置记忆规则，以定义记忆的提取和召回行为。每个用户账号下都自带一个默认记忆库，无需额外创建即可直接使用。如需自定义记忆规则或为不同业务场景分别管理记忆，可创建新的记忆库。

### **默认记忆库**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3820503771/p1055468.png)

-   默认记忆库无法删除，但可以编辑名称和描述、添加自定义记忆规则。
    
-   默认记忆库已预置一条”默认项目”记忆片段规则，默认有效期 180 天。可点击编辑调整信息。
    
    ### **创建新的记忆库**
    
    1.  在[记忆库](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list)页面，单击右上角的**创建记忆库**。
        
    2.  在**创建记忆库**对话框中，填写以下基础信息：
        
        **记忆库名称**：描述记忆库内容的名称。
        
        **记忆库描述**：可能会用于指导智能体调用的描述语句。
        
    3.  单击**确定**完成创建。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3820503771/p1055567.png)
        
    4.  创建成功后，会提示**是否立即开始创建记忆规则**：![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3820503771/p1055568.png)
        
        -   单击**立即创建**（推荐）：跳转到记忆规则配置页面，继续配置记忆规则。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3820503771/p1055579.png)
            
        -   单击**暂不**：返回记忆库列表页面，可后续通过点击记忆库卡片上的**查看详情**进入配置。
            

### **配置记忆规则**

记忆规则定义了如何从对话中提取、存储和检索记忆，包括**记忆片段规则**和**用户画像规则**。每个记忆库最多可配置 50 条记忆片段规则和 50 条用户画像规则。

> 记忆库已预置一条“默认项目”记忆片段规则，默认有效期 180 天。不可删除，但可点击**编辑**调整信息。

#### **配置记忆片段规则**

记忆片段规则用于从给定的对话内容中提取关键事件和信息片段。

1.  点击记忆库卡片的**查看详情**，进入记忆库详情页，在**记忆规则**标签页下的**记忆片段规则**区域，单击**添加片段规则**按钮。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6377893771/p1055580.png)
    
2.  在对话框中配置以下参数：![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3820503771/p1055585.png)
    
    -   **规则名称**：当前记忆抽取规则的唯一标识。
        
    -   **规则指令**：定义记忆抽取的策略指令，即描述如何抽取和抽取哪些内容。可选择**默认规则指令**或**自定义规则指令**。
        
        -   **默认规则指令****（推荐）**
            
        -   **自定义规则指令**
            
    -   **自动更新**：开启后，模型会自动更新记忆内容。默认开启。
        
    -   **记忆过期时间**：记忆的有效期，可选：7 天、30 天、180 天、永不过期。
        
3.  单击**确认**完成配置。
    

#### **配置用户画像规则**

用户画像规则用于持久化存储用户的属性信息。

1.  进入记忆库详情页，在**记忆规则**标签页下的**用户画像规则**区域，单击**添加用户画像**。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3820503771/p1055586.png)
    
2.  在对话框中配置以下参数：
    
    -   **画像规则名称**：当前画像规则的唯一标识。
        
    -   **画像字段列表**：点击**添加用户画像字段**填写以下信息，然后点击**保存**。
        
        -   **用户画像字段名称：**定义抽取出的画像包含哪些字段。
            
        -   **描述**：描述该字段的含义，引导模型提取相关信息。
            
        -   **初始值**：为该画像属性设置初始默认值。当用户尚未通过对话提供相关信息时，系统将使用该初始值作为画像属性的值。
            
3.  单击**确认**完成配置。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4490727771/p1055587.png)
    

## **用户画像**

用户画像用于从对话中提取结构化的用户属性（如年龄、职业、偏好），适用于需要持久化存储固定属性的场景。

### **在控制台配置用户画像**

1.  进入记忆库详情页，在**记忆规则**标签页的**用户画像规则**区域，单击**添加用户画像**。
    
2.  填写画像规则名称，添加画像字段（如"年龄""职业""爱好"），为每个字段填写描述以引导模型提取。
    
3.  单击**确认**完成配置。详细参数说明请参见[配置用户画像规则](#heading-profile-rules)。
    

配置后，调用 [AddMemory](https://help.aliyun.com/zh/model-studio/long-term-memory-api-reference) 时传入画像模板 ID，系统会自动从对话中提取属性。提取结果可在**记忆详情**标签页中查看。

### **通过 API 使用用户画像**

通过 API 可以创建画像模板、添加对话并提取画像、获取完整的用户画像。

#### **代码示例：创建画像 → 提取 → 获取**

## cURL

```
# 1. 创建画像模板（CreateProfileSchema）
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

# 2. 添加对话并提取画像（AddMemory，传入上面返回的 profile_schema_id）
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

# 3. 获取用户画像（GetUserProfile，等待3秒后执行）
curl -X GET "https://dashscope.aliyuncs.com/api/v2/apps/memory/profile_schemas/{YOUR_SCHEMA_ID}/user_profile?user_id=user_001" \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json"
```

## Python

**说明**

需要安装 agentscope-runtime，安装命令：`pip install agentscope-runtime`

```
from agentscope_runtime.tools.modelstudio_memory import (
    CreateProfileSchema, GetUserProfile, AddMemory,
    ProfileAttribute, CreateProfileSchemaInput,
    GetUserProfileInput, AddMemoryInput, Message,
)
import asyncio

async def profile_example():
    create_schema = CreateProfileSchema()
    get_profile = GetUserProfile()
    add_memory = AddMemory()

    try:
        # 1. 创建画像模板
        schema_result = await create_schema.arun(CreateProfileSchemaInput(
            name="用户基础画像",
            description="包含年龄和兴趣的用户信息",
            attributes=[
                ProfileAttribute(name="年龄", description="用户年龄"),
                ProfileAttribute(name="爱好", description="用户的兴趣爱好"),
                ProfileAttribute(name="职业", description="用户职业"),
            ]
        ))
        schema_id = schema_result.profile_schema_id

        # 2. 添加对话并提取画像
        await add_memory.arun(AddMemoryInput(
            user_id="user_001",
            messages=[
                Message(role="user", content="我今年28岁，是一名软件工程师。周末喜欢踢足球。"),
                Message(role="assistant", content="很高兴认识你！"),
            ]
        ))

        await asyncio.sleep(3)  # 等待画像提取

        # 3. 获取用户画像
        profile = await get_profile.arun(GetUserProfileInput(
            schema_id=schema_id, user_id="user_001"
        ))
        for attr in profile.profile.attributes:
            print(f"{attr.name}: {attr.value or '未提取'}")

    finally:
        await create_schema.close()
        await get_profile.close()
        await add_memory.close()

asyncio.run(profile_example())
```

相关 API：[CreateProfileSchema](https://help.aliyun.com/zh/model-studio/long-term-memory-api-reference)、[AddMemory](https://help.aliyun.com/zh/model-studio/long-term-memory-api-reference)、[GetUserProfile](https://help.aliyun.com/zh/model-studio/long-term-memory-api-reference)。

## **管理记忆**

### **查看记忆详情**

可访问**记忆详情**页查看成功添加的记忆内容，顶部展示记忆库的基本信息和统计数据。

页面下方展示记忆实体列表，支持通过记忆实体 ID （`user_id`）筛选。

单击操作列的**查看**，可查看当前记忆实体的记忆详情。

#### **代码示例：列出记忆**

## cURL

```
curl -X GET "https://dashscope.aliyuncs.com/api/v2/apps/memory/memory_nodes?user_id=user_001&page_size=10&page_num=1" \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json"
```

## Python

**说明**

需要安装 agentscope-runtime，安装命令：`pip install agentscope-runtime`

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
            page_size=10,
            page_num=1
        ))
        for node in result.memory_nodes:
            print(f"记忆: {node.content}")
    finally:
        await list_memory.close()

asyncio.run(list_memory_example())
```

### **检索调试**

在控制台调试记忆检索效果，优化召回的准确性和相关性。

1.  在记忆库详情页的**记忆检索**标签页中，配置以下参数：![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4490727771/p1055592.png)
    
    -   **记忆实体 ID：**输入[写入记忆](#29baf0c8b5y5g)时设置的`user_id`字段值。
        
    -   **记忆片段规则：**选择指定规则进行检索。
        
    -   **最大召回数量**：每次检索返回的记忆条数（1~100）。
        
    -   **意图判别召回**：系统判断当前对话是否需要召回记忆，避免无关检索。建议开启。
        
    -   **改写**：对用户查询进行优化改写，提升语义检索的准确率。当提问较口语化时建议开启。
        
    -   **排序**：开启后将对检索结果进行重排，提升相关性。
        
        -   **选择排序模型：**目前仅支持gte-rerank-v2模型。
            
        -   **相似度阈值**（0.0~1.0）：建议设置在 0.5~0.7 之间。过高可能漏召相关记忆，过低可能引入噪声。
            
    -   **输入**：传入当前提问，系统将基于语义检索返回最相关的记忆片段和用户画像。
        
2.  点击**运行**，查看检索结果。
    

#### **代码示例：检索记忆**

## cURL

```
curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/search \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "user_id": "user_001",
    "query": "我需要做什么？",
    "max_results": 10,
    "rewrite": true,
    "rerank": true,
    "similarity_threshold": 0.6
  }'
```

## Python

**说明**

需要安装 agentscope-runtime，安装命令：`pip install agentscope-runtime`

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

### **更新和删除记忆**

通过 API 对记忆片段进行列出、更新和删除操作。建议使用元数据（`meta_data`）对记忆进行分类管理，便于后续的精确检索和管理。相关 API：[ListMemory](https://help.aliyun.com/zh/model-studio/long-term-memory-api-reference)、[UpdateMemory](https://help.aliyun.com/zh/model-studio/long-term-memory-api-reference)、[DeleteMemory](https://help.aliyun.com/zh/model-studio/long-term-memory-api-reference)。

#### **代码示例：列出、更新与删除记忆**

## cURL

```
# 列出记忆
curl -X GET "https://dashscope.aliyuncs.com/api/v2/apps/memory/memory_nodes?user_id=user_001&page_size=10&page_num=1" \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json"

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

## Python

**说明**

需要安装 agentscope-runtime，安装命令：`pip install agentscope-runtime`

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

## **删除记忆库**

删除记忆库有以下两种方式，删除后记忆库中的所有记忆内容将被清除且不可恢复。

-   在记忆库卡片上点击**...**，然后点击**删除**。
    
-   在记忆库详情页右上角点击**...**，然后点击**删除**。
    

## **相关 API**

**API**

**说明**

[AddMemory - 添加记忆](https://help.aliyun.com/zh/model-studio/long-term-memory-api-reference)

添加记忆。传入对话消息后，系统自动提取记忆片段和用户画像。也支持直接指定要存储的记忆内容。

[SearchMemory - 搜索记忆](https://help.aliyun.com/zh/model-studio/long-term-memory-api-reference)

检索记忆。基于语义检索返回与当前查询最相关的历史记忆。

[ListMemory - 列出记忆](https://help.aliyun.com/zh/model-studio/long-term-memory-api-reference)

列出记忆。分页查看用户的所有记忆。

[DeleteMemory - 删除记忆](https://help.aliyun.com/zh/model-studio/long-term-memory-api-reference)

删除记忆。支持删除指定的记忆条目。

[UpdateMemory - 更新记忆](https://help.aliyun.com/zh/model-studio/long-term-memory-api-reference)

更新记忆。修改已有记忆的内容。

更多调用详情请参阅[长期记忆 API](https://help.aliyun.com/zh/model-studio/long-term-memory-api-reference)。

## **计费说明**

-   记忆库功能与 API 调用：目前限时免费。
    
-   模型调用：在检索记忆并将其注入 Prompt 时，记忆内容会作为上下文传递给大模型，从而增加 Token 消耗。具体费用以实际调用大模型产生的 Token 用量为准。
    

## **常见问题**

1.  **记忆内容会存储多长时间？**
    
    生成的记忆片段与用户画像暂无失效日期（除非在创建记忆库时配置了记忆过期时间）。您可以随时通过控制台或 API 删除不再需要的记忆内容。
    
2.  **如何实现不同用户之间的记忆隔离？**
    
    记忆的存储和检索以记忆实体（如 user\_id）为维度进行隔离。不同用户的记忆内容互不干扰。您也可以创建多个记忆库，分别用于不同的业务场景。
    
3.  **与之前的长期记忆功能有什么区别？**
    
    记忆库是之前长期记忆功能的全面升级版。主要区别在于：引入了记忆库作为独立的记忆管理容器，支持更灵活的记忆规则配置，新增了用户画像能力，并在检索效果、成本和延时方面进行了优化。
    
4.  **记忆片段和用户画像有什么区别？何时使用哪个？**
    
    记忆片段适用于记录具体的事件和信息（如"用户上周去了北京"），用户画像适用于结构化的用户属性（如年龄、职业、偏好等）。如果需要记录固定的用户属性，建议使用用户画像；如果是动态的事件信息，使用记忆片段。两者可以同时使用。
    
5.  **记忆实体数量在哪里查看？**
    
    在记忆库列表页单击**查看详情**，在**记忆详情**标签页可查看记忆片段数、用户画像数和记忆实体数的统计信息。
    
6.  **如何优化记忆检索效果？**
    
    可通过以下方式优化：1）在记忆库详情的**记忆检索**标签页进行调试测试；2）调整相似度阈值（建议 0.5-0.7）；3）开启"意图判别召回"避免无关检索；4）开启"改写"和"排序"提升检索准确性；5）合理设置最大召回数量（根据实际需求设置）。
    
7.  **默认记忆库可以删除吗？**
    
    默认记忆库不可删除，但可以编辑其名称、描述和记忆规则。默认记忆库已预置一条"默认项目"记忆片段规则，默认有效期 180 天，您可以根据需要修改或添加新的规则。
    
8.  **API 是否存在限流？**
    
    **API 接口**
    
    **限流（阿里云账号级别）**
    
    全部接口
    
    总计不超过 3000 QPM
    
    记忆片段 add 接口
    
    120 QPM
    
    记忆片段 search 接口
    
    300 QPM
