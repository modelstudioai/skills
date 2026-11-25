# 查询告警列表

查询安全告警列表，游标分页。支持按风险等级、处置状态、资产类型等条件筛选。

<a id="前提"></a>

<a id="h-secapi-alerts-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../security-api-overview.md)。

<a id="接口"></a>

<a id="h-secapi-alerts-endpoint"></a>

## 接口

**GET** `/agent_logs`

查询安全告警列表，游标分页。支持按风险等级、处置状态、资产类型等条件筛选。

<a id="请求参数"></a>

<a id="h-secapi-alerts-params"></a>

## 请求参数

| 参数 | 必填 | 类型 | 说明 |
| --- | --- | --- | --- |
| `current_page` | 否 | integer | 当前页码，默认 1 |
| `page_size` | 否 | integer | 每页条数，默认 20 |
| `risk_level` | 否 | string | 风险等级筛选：`high` / `medium` / `low` |
| `status` | 否 | string | 处置状态筛选 |
| `status_list` | 否 | array | 处置状态批量筛选（多值） |
| `risk_name` | 否 | string | 风险名称筛选 |
| `app_name` | 否 | string | 应用名称筛选 |
| `asset_type` | 否 | string | 资产类型筛选：`agent` / `tool` / `skill` / `knowledge_base` / `memory` / `channel` |
| `vendor` | 否 | string | 厂商筛选 |
| `order_by` | 否 | string | 排序字段，默认 `check_time` |
| `order` | 否 | string | 排序方向：`asc` / `desc`，默认 `desc` |
| `lang` | 否 | string | 语言：`zh` / `en` |

<a id="请求示例"></a>

<a id="h-secapi-alerts-eg"></a>

## 请求示例

<a id="code-block"></a>

```bash
curl -X GET "$BASE_URL/agent_logs?current_page=1&page_size=20&risk_level=high&order_by=check_time&order=desc&lang=zh" \
  -H "Authorization: Bearer $BAILIAN_API_KEY"
```

其中 `BASE_URL` 为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security`，`BAILIAN_API_KEY` 为阿里云百炼 API Key。

<a id="响应体"></a>

<a id="h-secapi-alerts-resp"></a>

## 响应体

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `stats` | object | 统计数据：`total` 总数，`high` / `medium` / `low` 按等级分组数量 |
| `data` | array | 告警列表，列表项字段见下表 |
| `next_page` | integer | 游标页码，末页返回 `null` |

列表项字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `alert_id` | string | 告警 ID，纯数字，用于查询详情 |
| `risk_level` | string | 风险等级：`high` / `medium` / `low` |
| `risk_name` | string | 风险名称 |
| `risk_desc` | string | 风险描述 |
| `asset_type` | string | 资产类型 |
| `asset_name` | string | 资产名称 |
| `app_id` | string | 应用 ID |
| `app_name` | string | 应用名称 |
| `agent_name` | string | Agent 名称 |
| `status` | string | 处置状态：`unhandled` / `handling` / `intercepted` 等 |
| `source` | string | 来源：`aiguard` / `Agent-Runtime-Guard` / `cspm` 等 |
| `check_time` | string | 检查时间，毫秒时间戳字符串 |
| `handle_time` | string | 处置时间，毫秒时间戳字符串 |

<a id="响应示例"></a>

<a id="h-secapi-alerts-resp-eg"></a>

## 响应示例

<a id="code-block-2"></a>

```json
{
  "success": true,
  "data": {
    "stats": {"total": 15, "high": 3, "medium": 7, "low": 5},
    "data": [
      {
        "alert_id": "4289016",
        "risk_level": "high",
        "risk_name": "提示词注入攻击",
        "risk_desc": "提示词泄漏，请求已被拦截",
        "asset_type": "agent",
        "asset_name": "demo_agent",
        "app_id": "app-1001",
        "app_name": "demo_application",
        "agent_name": "demo_agent",
        "status": "intercepted",
        "source": "Agent-Runtime-Guard",
        "check_time": "1788365324000",
        "handle_time": null
      }
    ],
    "next_page": null
  }
}
```
