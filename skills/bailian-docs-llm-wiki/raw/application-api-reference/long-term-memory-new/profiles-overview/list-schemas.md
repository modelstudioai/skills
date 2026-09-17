# 列出画像模板

分页查询所有画像模板

分页查询当前用户的所有画像模板。

## 请求参数

参数

类型

必填

说明

`page_size`

number

否

每页数量

`page_num`

number

否

页码，从 1 开始

## 代码示例

```
curl -X GET "https://dashscope.aliyuncs.com/api/v2/apps/memory/profile_schemas?page_size=10&page_num=1" \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json"
```

## 响应示例

```
{
  "profile_schemas": [
    {
      "description": "包含年龄和兴趣的用户信息",
      "extract_scene": "efficient",
      "name": "用户基础画像",
      "plan_version": "pro",
      "profile_schema_id": "50edf54eaa5842e891d959ae115205be"
    },
    {
      "description": "系统自动创建的默认画像模板",
      "extract_scene": "efficient",
      "name": "默认画像",
      "plan_version": "pro",
      "profile_schema_id": "976e2e6e59f64ed0b25e6ca0268624bb"
    }
  ],
  "request_id": "3c46983f-85fd-92a5-8440-2e459cc91b2f",
  "total": 2
}
```

**重要**查看单个模板详情使用 [GetProfileSchema](raw/application-api-reference/long-term-memory-new/profiles-overview/get-schema.md)。
