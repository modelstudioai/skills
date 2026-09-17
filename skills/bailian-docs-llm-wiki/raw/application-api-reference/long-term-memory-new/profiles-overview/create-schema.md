# 创建画像模板

创建用户画像模板，定义画像字段

创建用户画像模板，定义画像包含的字段及描述。

## 请求参数

参数

类型

必填

说明

`name`

string

是

画像模板名称

`description`

string

否

模板描述，用于指导智能体调用

`attributes`

array

是

画像字段列表，每项含 `name` 和 `description`

`plan_version`

string

否

`Pro` 或 `Lite`，不传默认 Pro

## 代码示例

cURL

```
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
```

Python

```
from agentscope_runtime.tools.modelstudio_memory import (
    CreateProfileSchema, CreateProfileSchemaInput, ProfileAttribute,
)
import asyncio

async def main():
    create_schema = CreateProfileSchema()
    try:
        result = await create_schema.arun(CreateProfileSchemaInput(
            name="用户基础画像",
            description="包含年龄和兴趣的用户信息",
            attributes=[
                ProfileAttribute(name="年龄", description="用户年龄"),
                ProfileAttribute(name="爱好", description="用户的兴趣爱好"),
                ProfileAttribute(name="职业", description="用户职业"),
            ]
        ))
        print(f"Schema ID: {result.profile_schema_id}")
    finally:
        await create_schema.close()

asyncio.run(main())
```

## 响应示例

```
{
  "profile_schema_id": "50edf54eaa5842e891d959ae115205be",
  "request_id": "f190a540-814e-9c1c-873e-0661851c8fca"
}
```

**重要**创建后，使用 [AddMemory](raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md) 传入 `profile_schema` 提取画像，再用 [GetUserProfile](raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md) 获取。
