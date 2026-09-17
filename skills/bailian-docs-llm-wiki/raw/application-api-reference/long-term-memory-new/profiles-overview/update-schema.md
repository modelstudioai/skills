# 更新画像模板

更新画像模板的名称、描述或策略版本

更新画像模板。修改 `plan_version` 后，新写入的记忆遵循新策略版本规则，已写入的记忆不受影响。

## 请求参数

参数

类型

必填

说明

`profile_schema_id`

string

是

画像模板 ID（路径参数）

`name`

string

否

更新后的模板名称

`description`

string

否

更新后的模板描述

`plan_version`

string

否

更新策略版本，`Pro` 或 `Lite`

## 代码示例

```
curl -X PATCH "https://dashscope.aliyuncs.com/api/v2/apps/memory/profile_schemas/{profile_schema_id}" \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "更新后的画像名称",
    "plan_version": "Lite"
  }'
```

## 响应示例

```
{
  "request_id": "813e8d62-062c-97d5-877b-e10f356ca7d4"
}
```

**重要**删除模板使用 [DeleteProfileSchema](raw/application-api-reference/long-term-memory-new/profiles-overview/delete-schema.md)。
