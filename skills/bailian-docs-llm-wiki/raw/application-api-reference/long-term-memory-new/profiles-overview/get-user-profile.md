# 获取用户画像

查询指定用户已提取的画像属性

获取指定用户的画像属性。需在调用 AddMemory 添加对话后等待约 3 秒，待画像提取完成。

**说明**若返回的属性值均为空，请确认调用 [AddMemory](raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md) 时已传入相同的 `profile_schema`。未传该参数时不会触发画像提取。

## 请求参数

参数

类型

必填

说明

`profile_schema_id`

string

是

画像模板 ID（路径参数）

`user_id`

string

是

记忆实体 ID

## 返回结果

字段

类型

说明

`request_id`

string

请求 ID

`profile.schema_name`

string

画像模板名称

`profile.schema_description`

string

画像模板描述

`profile.attributes`

array

画像属性列表

`profile.attributes[].id`

string

属性 ID

`profile.attributes[].name`

string

属性名称

`profile.attributes[].value`

string

属性值

## 代码示例

cURL

```
curl -X GET "https://dashscope.aliyuncs.com/api/v2/apps/memory/profile_schemas/{profile_schema_id}/user_profile?user_id=user_001" \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json"
```

Python

```
from agentscope_runtime.tools.modelstudio_memory import (
    GetUserProfile, GetUserProfileInput,
)
import asyncio

async def main():
    get_profile = GetUserProfile()
    try:
        profile = await get_profile.arun(GetUserProfileInput(
            schema_id="YOUR_SCHEMA_ID",
            user_id="user_001"
        ))
        for attr in profile.profile.attributes:
            print(f"{attr.name}: {attr.value or '未提取'}")
    finally:
        await get_profile.close()

asyncio.run(main())
```

## 响应示例

```
{
  "profile": {
    "attributes": [
      {"id": "bb28e6cd522443fc9bf7e75b1377bf9d", "name": "年龄", "value": "28"},
      {"id": "04eb06f5f04a437b82d07ceb088103f9", "name": "爱好", "value": "踢足球"},
      {"id": "2eff4652a6bc47b0803635033b1e08dd", "name": "职业", "value": "软件工程师"}
    ],
    "schema_description": "包含年龄和兴趣的用户信息",
    "schema_name": "用户基础画像"
  },
  "request_id": "78cb6090-a7a5-9897-861c-082a64b43d97"
}
```

**重要**完整画像流程参见[使用用户画像](raw/application-user-guide/memory-library-overview/create-memory/user-profile.md)。
