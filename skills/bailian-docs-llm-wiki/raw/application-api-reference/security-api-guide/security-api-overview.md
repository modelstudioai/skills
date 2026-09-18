# API 总览与认证

Security API 的前提条件、Endpoint 拼装与鉴权方式，以及防护概况、策略与告警的可用接口和错误码。

Security API 提供 Agent 安全防护数据的查询与告警导出能力。文档路径前缀为 `/api/v1/agentstudio/security`。

## 前提条件

1.  **开通阿里云百炼并创建 API Key**：通过[控制台](https://bailian.console.aliyun.com/?tab=model#/api-key)获取。
2.  **获取工作空间 ID**：阿里云百炼控制台右上角下拉菜单查看，形如 `{workspace_id}`。

## Endpoint

API 基地址按工作空间与地域拼装：

```
https://{workspace_id}.{region}.maas.aliyuncs.com/api/v1/agentstudio/security
```

-   `workspace_id`：工作空间 ID
-   `region`：地域 ID，当前仅支持 `cn-beijing`

## 鉴权

全部请求通过 HTTP Header 携带阿里云百炼 API Key：

```
Authorization: Bearer <your-api-key>
```

## 通用响应结构

全部接口的响应结构一致：

```
// 成功
{"success": true, "data": { }}

// 失败
{"success": false, "errorCode": "12000094", "errorMsg": "告警查询失败"}
```

单项数据不可用时，接口不报错：对应字段返回 `null`，部分场景返回该项的 `available: false`，不影响整体响应。

## 可用 API

### 防护概况

**能力**

**方法**

**路径**

查询防护总览

`GET`

`/overview`

查询 Agent 资产

`GET`

`/asset_summary`

### 策略与告警

**能力**

**方法**

**路径**

查询安全策略

`GET`

`/policies`

查询告警列表

`GET`

`/agent_logs`

查询告警详情

`GET`

`/agent_logs/{alert_id}`

导出告警

`POST`

`/export_agent_logs`

查询导出状态

`GET`

`/export_status`

## 错误码

错误码

HTTP 状态码

说明

处理建议

12000093

503

云安全服务异常

对应能力暂时不可用，稍后重试

12000094

503

告警查询失败

稍后重试
