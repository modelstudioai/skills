# 错误码

OpenAI 兼容 API 的错误响应结构和常见错误类型。

## 错误响应

业务错误返回以下结构：

```
{
  "error": {
    "type": "invalid_request_error",
    "code": "invalid_request_error",
    "message": "$: required property 'model' not found",
    "param": "model"
  }
}
```

字段

类型

说明

`error.type`

string

错误类别

`error.code`

string

机器可读错误代码

`error.message`

string

错误说明，不作为稳定枚举判断

`error.param`

string / null

对应参数路径；资源或系统错误可能为 `null`

响应头携带 `x-request-id`，排查问题时保留该值。成功资源正文没有统一的 `request_id` 字段。

error 对象的字段顺序不固定；读取时按字段名取值，不要依赖 JSON 顺序。

## 常见状态码

HTTP 状态码

错误类型 / 错误码

解决方案

`400`

`invalid_request_error` / `invalid_request_error`

按参数说明修正请求参数

`401`

`authentication_error` / `invalid_api_key`

在请求头携带有效的 `Authorization: Bearer $DASHSCOPE_API_KEY`

`403`

网关错误码

确认工作空间存在且当前账号有权限

`404`

`not_found_error` / `not_found_error`

使用当前工作空间内存在且未删除的资源

`409`

`conflict_error` / `conflict_error`

确认资源状态；同一幂等键使用相同请求正文后重试

`429`

网关错误码

降低请求频率后重试

`500`

`server_error` / `server_error`

稍后重试；持续失败时提交工单并提供 `x-request-id`

`502`

`server_error` / `agents_api_upstream_unavailable`

稍后重试；持续失败时提交工单并提供 `x-request-id`

`503`

`server_error` / 具体服务错误码

稍后重试；持续失败时提交工单并提供 `x-request-id`

## 常见 `param`

`param` 使用字段路径，例如：

-   `model`
-   `environment.type`
-   `agent.tools[0].transport.type`
-   `events[0].output`

跨字段约束、资源不存在或系统错误可能返回 `null`。

## 网关错误

鉴权、工作空间路由、限流和部分路由错误可能由网关直接返回，结构可能与业务错误不同。排查时同时检查 HTTP 状态、响应头 `x-request-id` 和响应正文，不要只复制 `message` 文本。

## 重试建议

场景

建议

`429`、`500`、`502`、`503`

使用指数退避重试；写请求先确认幂等键或资源状态

`409`

重新获取资源状态后再决定是否重试

`400`、`401`、`403`、`404`

修正请求或权限，不直接重试

SSE 中断

重新获取 Session、Turns 和 Items，不依赖断线重放
