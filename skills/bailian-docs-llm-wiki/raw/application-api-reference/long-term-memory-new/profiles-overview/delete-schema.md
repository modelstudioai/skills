# 删除画像模板

删除一个画像模板，已提取的画像数据将同时清除

删除指定的画像模板。删除后不可恢复。

**警告**删除操作不可逆，已提取的画像数据将一并清除。

## 请求参数

参数

类型

必填

说明

`profile_schema_id`

string

是

画像模板 ID（路径参数）

## 代码示例

```
curl -X DELETE "https://dashscope.aliyuncs.com/api/v2/apps/memory/profile_schemas/{profile_schema_id}" \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json"
```

## 响应示例

```
{
  "request_id": "47d6db85-2887-9f87-b5ca-1ad66fc1fd63"
}
```

**重要**获取用户画像使用 [GetUserProfile](raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)。
