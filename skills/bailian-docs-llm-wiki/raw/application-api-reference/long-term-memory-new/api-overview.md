# API 概览

服务地址、协议约定、请求格式与通用响应

通过记忆库 API，你可以以编程方式写入记忆、检索记忆、管理画像模板。所有接口通过 DashScope 网关提供服务。

## 服务地址

```
https://dashscope.aliyuncs.com/api/v2/apps/memory/
```

所有接口使用统一的服务地址，路径前缀为 `/memory/`。

## 协议约定

-   所有接口均通过 **HTTPS** 访问，不支持 HTTP
-   请求体和响应体均为 **JSON** 格式，字符集 **UTF-8**
-   写入和检索接口使用 `POST` 方法；列表查询使用 `GET` 方法；更新使用 `PATCH`；删除使用 `DELETE`

## 通用请求头

Header

必填

说明

`Authorization`

是

`Bearer $DASHSCOPE_API_KEY`，获取方式见[鉴权](raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)

`Content-Type`

是

`application/json`

## 通用响应格式

所有接口返回统一的 JSON 结构。

**成功响应：**

```
{
  "request_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "memory_nodes": [
    {
      "memory_node_id": "node_xxx",
      "content": "用户每天上午9点需要喝水提醒"
    }
  ]
}
```

**失败响应：**

```
{
  "code": "InvalidParameter",
  "message": "user_id is required",
  "request_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
}
```

排查问题时，请提供 `request_id`，以便技术支持快速定位。完整错误码见[错误码参考](raw/application-api-reference/long-term-memory-new/api-overview/errors.md)。

## 分页

列表接口支持分页查询：

参数

说明

`page_size`

每页数量

`page_num`

页码，从 1 开始

**说明**记忆库将于 **2026 年 8 月 20 日** 正式商业化计费。Add 和 Search 调用区分 **Pro** 和 **Lite** 两个策略版本。详见[计费说明](raw/application-user-guide/memory-library-overview/integration-overview/billing.md)。

**重要**准备好凭证后，查看 [AddMemory 接口](raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)。
