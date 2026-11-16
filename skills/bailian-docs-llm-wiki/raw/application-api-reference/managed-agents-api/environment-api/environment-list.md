# 列出 Environment

分页列出当前工作空间下的运行环境，按 created\_at 倒序返回。默认不包含已归档项。

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。

## 接口

**GET** `/environments`

## Query 参数

**limit** `int` 默认 20

每页数量，最大 100

**page** `string` 默认 —

首次不传，后续传上一次响应的 `next_page`

**include\_archived** `bool` 默认 false

是否包含已归档环境

## 请求示例

curl

```
curl "$AGENTSTUDIO_URL/environments?limit=20" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

Python

```
for env in client.environments.list(include_archived=False, limit=20):
    print(env.id, env.name)
```

Java

```
CursorPage<Environment> page = client.environments().list(EnvironmentListParam.builder()
    .includeArchived(false)
    .limit(20)
    .build());
for (Environment e : page.getData()) System.out.println(e.getId() + " " + e.getName());
```

### Environment 对象字段

响应顶层包含 `data`（Environment 对象数组）、`next_page`（下一页游标）与 `request_id`（本次请求的唯一标识）。Environment 对象字段如下：

**id** `string`

环境 ID，格式 `env_&lt;ULID&gt;`

**type** `string`

固定为 `environment`

**name / description / scope / config / metadata** `string / object`

环境基础属性与完整运行时配置（沙箱类型、预装依赖、网络策略）

**archived\_at** `string / null`

归档时间，未归档时为 `null`

**created\_at / updated\_at** `string`

创建 / 最近更新时间，ISO 8601

## 响应示例

```
{
  "data": [
    {
      "id": "env_xxx",
      "type": "environment",
      "name": "data-sandbox",
      "description": "数据分析沙箱",
      "config": {
        "type": "cloud",
        "packages": {"apt": ["ffmpeg"], "pip": ["pandas", "numpy", "matplotlib"]},
        "networking": {"type": "unrestricted"}
      },
      "metadata": {"team": "infra"},
      "scope": "organization",
      "archived_at": null,
      "created_at": "2026-06-16T12:45:34+08:00",
      "updated_at": "2026-06-16T12:45:34+08:00"
    }
  ],
  "next_page": "xxx",
  "request_id": "xxx"
}
```
