# 列出 Skill

分页查询自定义和官方 Skill，支持按来源和关键词筛选。

## 接口

**GET** `/api/v1/skills`

分页查询自定义和官方 Skill。

## Query 参数

参数

类型

默认

说明

type

`string`

—

`OFFICIAL` 或 `CUSTOMER`，区分大小写；不传时同时查询两类

keywords

`string`

—

关键词，去除首尾空白后为空则忽略

pageNo

`integer`

1

页码，最小 1

pageSize

`integer`

20

单页条数，取值范围 1 到 100

-   `type=OFFICIAL`：仅返回未删除且 `active` 的官方 Skill。
-   `type=CUSTOMER`：返回主账号和工作空间下未删除的自定义 Skill，包含 `checking` 和 `rejected` 状态。
-   不传 `type`：一次返回官方和自定义两类 Skill，`total` 为两类合计。

## 响应

`data` 为分页对象，`items` 每项为 `SkillDTO`。

字段

类型

说明

items

`array<SkillDTO>`

当前页 Skill 列表

total

`long`

命中总数

page\_no

`integer`

当前页码

page\_size

`integer`

单页条数

无数据时 `items` 为空数组，`total` 为 0。

## 示例

```
# 官方和自定义混合
curl "https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/skills?pageNo=1&pageSize=20" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"

# 仅自定义，按关键词搜索
curl "https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/skills?type=CUSTOMER&keywords=pdf&pageNo=1&pageSize=20" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```
```
{
  "success": true,
  "error_code": null,
  "error_msg": null,
  "data": {
    "items": [
      {
        "id": "skill_abc123",
        "display_name": "My Custom Skill",
        "display_description": "描述",
        "source": "customer",
        "status": "active",
        "latest_version": "1.2",
        "classification": null,
        "meta_info": null,
        "created_at": "2026-06-15T08:23:11Z",
        "updated_at": "2026-06-15T08:23:11Z"
      }
    ],
    "total": 35,
    "page_no": 1,
    "page_size": 20
  },
  "request_id": "15a89d4c-f142-4e00-a9f7-b088442417c9"
}
```

**说明**列表数据异步更新。新建、删除或状态变化后，列表可能短暂未反映最新状态；以[获取 Skill](raw/application-api-reference/overview/overview/get-9c06b4218676761a.md)的结果为准。

## 错误

HTTP 状态码

error\_code

说明

401

WORKSPACE\_ID\_ILLEGAL

身份信息缺失或无效

400

INVALID\_PARAMETER

`type` 不是 `OFFICIAL` 或 `CUSTOMER`；`pageNo` 或 `pageSize` 非整数、越界或超出分页范围

500

SYSTEM\_ERROR

查询失败或服务内部错误
