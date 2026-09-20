# API 参考

Security 模块的接口概览，覆盖防护总览、Agent 资产、安全策略与风险告警。

Security 模块提供 7 个接口，用于查询防护总览与 Agent 资产、查看安全策略与风险告警，以及导出告警记录。接口路径前缀为 `/api/v1/agentstudio/security`。

## 接口总览

接口

路径

方法

入参

分页

防护总览

/overview

GET

无

否

Agent 资产

/asset\_summary

GET

无

否

安全策略

/policies

GET

无

否

告警列表

/agent\_logs

GET

有

游标

告警详情

/agent\_logs/{alert\_id}

GET

有

否

导出告警

/export\_agent\_logs

POST

有

否

导出状态

/export\_status

GET

有

否

## 通用约定

全部接口的响应结构一致：

```
// 成功
{"success": true, "data": { }}

// 失败
{"success": false, "errorCode": "12000092", "errorMsg": "无权限创建服务关联角色"}
```

单项数据不可用时，接口不报错：对应字段返回 `null`，部分场景返回该项的 `available: false`，不影响整体响应。

各接口的请求参数、响应参数与错误码见 [Security API 总览与认证](raw/application-api-reference/security-api-guide/security-api-overview.md)。
