# 使用用户画像

通过 API 创建画像模板、提取画像并获取用户画像

用户画像用于从对话中提取结构化的用户属性（如年龄、职业、偏好），适用于需要持久化存储固定属性的场景。控制台配置方式参见[配置记忆规则](https://help.aliyun.com/zh/model-studio/memory/configure-rules#profile-rules)。

本页介绍通过 API 完成画像模板创建、对话提取和画像获取的完整流程。

## 前提条件

-   已创建记忆库或使用默认记忆库
-   配置 `DASHSCOPE_API_KEY` 环境变量

## 完整流程

创建画像模板 → 添加对话并提取 → 获取用户画像。

cURL

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

Python

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

        # 2. 添加对话并提取画像（必须传入 profile_schema，否则不会提取画像）
        await add_memory.arun(AddMemoryInput(
            user_id="user_001",
            profile_schema=schema_id,
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

**说明**画像提取是异步过程，添加对话后需等待约 3 秒再获取画像。

**重要**画像配置完成后，继续[管理记忆](raw/application-user-guide/memory-library-overview/create-memory/manage-memory.md)查看和检索已有记忆。
