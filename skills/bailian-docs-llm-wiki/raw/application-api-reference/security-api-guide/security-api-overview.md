# 概览

Security API 的前提条件、Endpoint 拼装与鉴权方式，以及防护概况、策略与告警的可用接口和错误码。

**说明**调用前请先配置[认证](raw/application-api-reference/security-api-guide/security-api-authentication.md)；错误处理见[错误码](raw/application-api-reference/security-api-guide/security-api-errors.md)。

Security API 提供 Agent 安全防护数据的查询与告警导出能力。文档路径前缀为 `/api/v1/agentstudio/security`。

## 前提条件

1.  已开通阿里云百炼，并[创建 API Key](raw/application-api-reference/security-api-guide/security-api-authentication.md)。
2.  **获取工作空间 ID**：阿里云百炼控制台右上角下拉菜单查看，形如 `{workspace_id}`。

## Endpoint

API 基地址按工作空间与地域拼装：

```
https://{workspace_id}.{region}.maas.aliyuncs.com/api/v1/agentstudio/security
```

-   `workspace_id`：工作空间 ID
-   `region`：地域 ID，当前仅支持 `cn-beijing`

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
