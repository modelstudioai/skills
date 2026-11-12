# 查询用量汇总

查询工作空间、Agent 或 Session 的用量汇总，返回总量及按模型、工具分组的明细。

## 前提

已完成工作空间和 API Key 配置，接入方式见 [API 总览与认证](raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。时间格式、粒度选择和区间对齐规则见 [Usage](https://help.aliyun.com/zh/model-studio/usage-api#h-usage-time)。

## 接口

**POST** `/usage/summary`

获取指定时间范围内工作空间或 Agent 的用量，也可获取单个 Session 自创建以来累计的用量。响应同时包含总量、按模型分组的明细和按工具分组的明细。

## 请求体

参数

必填

类型

说明

`dimension`

是

string

查询维度，区分大小写。取值仅为 `workspace`、`agent`、`session`

`agent_id`

条件必填

string

`dimension=agent` 时必填，指定一个 Agent；其他维度不传

`agent_version`

否

string

仅 `dimension=agent` 可用。指定 Agent 版本；不传或为 `null` 时合并全部版本。不能是空字符串或纯空白；按原始字符串精确匹配，不自动去除首尾空格

`session_id`

条件必填

string

`dimension=session` 时必填。使用创建 Session 时返回的 ID；必须为非空、非纯空白的单个字符串，其他维度不传

`time_range`

条件必填

object

`workspace`、`agent` 维度必填；`session` 维度不接受

`time_range.start_time`

条件必填

string

使用 `time_range` 时必填。带时区的秒级 RFC 3339 字符串，例如 `2026-11-02T10:15:30+08:00`；秒可以非零，无需对齐整分钟

`time_range.end_time`

条件必填

string

使用 `time_range` 时必填。结束时间，格式同上，必须晚于开始时间

`granularity`

否

string

`workspace`、`agent` 维度可用，取值为 `hour`、`day`、`month`；不传时自动选择。影响实际统计区间的对齐方式。`session` 维度不传

三个维度的参数组合如下：

dimension

查询范围

参数要求

`workspace`

当前工作空间的用量

必传 `time_range`，不传 `agent_id`、`agent_version`、`session_id`

`agent`

当前工作空间内指定 Agent 的用量

必传 `agent_id`、`time_range`，可传 `agent_version`，不传 `session_id`

`session`

当前工作空间内指定 Session 的生命周期累计用量

只传 `dimension`、`session_id`；不传 Agent 筛选、`time_range` 或 `granularity`

`agent_id`、`session_id` 必须为非空单值。`time_range`、`granularity` 不接受显式 `null`。`workspace` 维度传入 Agent 筛选，或 `session` 维度传入 `time_range`、`granularity`，返回 HTTP 400 / `invalid_parameter`。时间范围会按 UTC+8 对齐，详见 [Usage](https://help.aliyun.com/zh/model-studio/usage-api#h-usage-time)。

此接口一次返回总量及全部模型、工具明细，不提供分页参数；单次模型与工具明细项合计上限为 100,000，超出返回 HTTP 400 / `query_limit_exceeded`，不返回截断结果。

## 请求示例

### 查询当前工作空间的用量

```
curl -X POST "$AGENTSTUDIO_URL/usage/summary" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "dimension": "workspace",
    "time_range": {
      "start_time": "2026-11-02T10:15:30+08:00",
      "end_time": "2026-11-02T14:00:01+08:00"
    },
    "granularity": "hour"
  }'
```

### 查询指定 Agent 的指定版本

```
curl -X POST "$AGENTSTUDIO_URL/usage/summary" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "dimension": "agent",
    "agent_id": "agent_xxx",
    "agent_version": "1",
    "time_range": {
      "start_time": "2026-11-02T10:15:30+08:00",
      "end_time": "2026-11-02T14:00:01+08:00"
    },
    "granularity": "hour"
  }'
```

### 查询指定 Session 的累计用量

```
curl -X POST "$AGENTSTUDIO_URL/usage/summary" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "dimension": "session",
    "session_id": "sesn_xxx"
  }'
```

## 响应示例

成功时返回 HTTP 200，顶层字段为 `request_id`、`data`。以下为上述 Agent 请求的汇总示例：秒级起止时间按 `hour` 对齐为 UTC+8 10:00—15:00，数值仅用于说明响应结构。

```
{
  "request_id": "req_summary_example",
  "data": {
    "query_range": {
      "start_time": "2026-11-02T10:00:00+08:00",
      "end_time": "2026-11-02T15:00:00+08:00"
    },
    "data_updated_at": "2026-11-02T14:10:00+08:00",
    "usage": {
      "total": {
        "input_tokens": {"value": 1000, "unit": "tokens"},
        "output_tokens": {"value": 200, "unit": "tokens"},
        "total_tokens": {"value": 1200, "unit": "tokens"},
        "cache_read_tokens": {"value": 400, "unit": "tokens"},
        "cache_creation_tokens": {"value": 100, "unit": "tokens"},
        "cache_hit_ratio": {"value": 0.4, "unit": "ratio"},
        "model_call_count": {"value": 5, "unit": "count"},
        "tool_call_count": {"value": 3, "unit": "count"},
        "builtin_tool_call_count": {"value": 0, "unit": "count"},
        "mcp_tool_call_count": {"value": 3, "unit": "count"},
        "custom_tool_call_count": {"value": 0, "unit": "count"},
        "turns": {"value": 2, "unit": "count"},
        "steps": {"value": 8, "unit": "count"},
        "interrupt_error_count": {"value": 0, "unit": "count"},
        "model_failed_count": {"value": 1, "unit": "count"},
        "tool_failed_count": {"value": 1, "unit": "count"},
        "runtime_ms": {"value": 60000, "unit": "ms"}
      },
      "models": [
        {
          "model_name": "qwen-plus",
          "usage": {
            "input_tokens": {"value": 1000, "unit": "tokens"},
            "output_tokens": {"value": 200, "unit": "tokens"},
            "total_tokens": {"value": 1200, "unit": "tokens"},
            "cache_read_tokens": {"value": 400, "unit": "tokens"},
            "cache_creation_tokens": {"value": 100, "unit": "tokens"},
            "cache_hit_ratio": {"value": 0.4, "unit": "ratio"},
            "call_count": {"value": 5, "unit": "count"},
            "failed_count": {"value": 1, "unit": "count"}
          }
        }
      ],
      "tools": [
        {
          "source": "mcp",
          "tool_name": "web_search",
          "usage": {
            "call_count": {"value": 3, "unit": "count"},
            "failed_count": {"value": 1, "unit": "count"}
          }
        }
      ]
    }
  }
}
```

## 响应字段

字段

类型

说明

`request_id`

string

请求标识，可用于问题排查

`data`

object

用量查询结果

`data.query_range`

object

实际统计区间。仅 `workspace`、`agent` 维度返回；`session` 维度不返回该字段

`data.query_range.start_time`

string

对齐后的开始时间，包含该时刻，固定使用 `+08:00` 时区

`data.query_range.end_time`

string

对齐后的结束时间，不包含该时刻，固定使用 `+08:00` 时区

`data.data_updated_at`

string / null

本次返回用量记录中最近的已知更新时间，固定使用 `+08:00` 时区；无记录或更新时间未知时为 `null`

`data.usage`

object

总量及分组明细

`data.usage.total`

object

查询范围内的汇总指标，详见 [汇总指标（total）](https://help.aliyun.com/zh/model-studio/usage-api#h-usage-total)

`data.usage.models`

array

按模型名称分组的用量明细，无明细时为 `[]`

`data.usage.tools`

array

按工具来源和名称分组的用量明细，无明细时为 `[]`

Session 查询返回相同的 `usage` 结构，不包含 `query_range` 或 Session 标题、状态等元数据。服务先校验 Session 归属，再查询生命周期累计用量。Session 存在但尚无统计记录时，指标 `value` 为 `null`，模型和工具明细为空数组；不会据此返回 Session 不存在。
