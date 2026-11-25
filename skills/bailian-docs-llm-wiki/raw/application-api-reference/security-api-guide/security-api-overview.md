# 概览

Security API 的前提条件、Endpoint 拼装与鉴权方式，以及防护概况、策略与告警的可用接口和错误码。

> **说明**
>
> 调用前请先配置[认证](security-api-authentication.md)；错误处理见[错误码](security-api-errors.md)。

Security API 提供 Agent 安全防护数据的查询与告警导出能力。文档路径前缀为 `/api/v1/agentstudio/security`。

<a id="前提条件"></a>

<a id="h-secapi-overview-prereq"></a>

## 前提条件

1.  已开通阿里云百炼，并[创建 API Key](security-api-authentication.md)。
2.  **获取工作空间 ID**：阿里云百炼控制台右上角下拉菜单查看，形如 `{workspace_id}`。

<a id="endpoint"></a>

<a id="h-secapi-overview-endpoint"></a>

## Endpoint

API 基地址按工作空间与地域拼装：

<a id="code-block"></a>

```text
https://{workspace_id}.{region}.maas.aliyuncs.com/api/v1/agentstudio/security
```

-   `workspace_id`：工作空间 ID
-   `region`：地域 ID，当前仅支持 `cn-beijing`

<a id="可用-api"></a>

<a id="h-secapi-overview-list"></a>

## 可用 API

<a id="防护概况"></a>

<a id="h-secapi-overview-list-protection"></a>

### 防护概况

| 能力 | 方法 | 路径 |
| --- | --- | --- |
| 查询防护总览 | `GET` | `/overview` |
| 查询 Agent 资产 | `GET` | `/asset_summary` |

<a id="策略与告警"></a>

<a id="h-secapi-overview-list-alert"></a>

### 策略与告警

| 能力 | 方法 | 路径 |
| --- | --- | --- |
| 查询安全策略 | `GET` | `/policies` |
| 查询告警列表 | `GET` | `/agent_logs` |
| 查询告警详情 | `GET` | `/agent_logs/{alert_id}` |
| 导出告警 | `POST` | `/export_agent_logs` |
| 查询导出状态 | `GET` | `/export_status` |
