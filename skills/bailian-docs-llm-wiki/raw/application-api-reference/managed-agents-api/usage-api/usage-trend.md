# 查询用量趋势

按小时、UTC+8 自然日或自然月分页查询工作空间或 Agent 的用量趋势。

## 前提

已完成工作空间和 API Key 配置，接入方式见 [API 总览与认证](raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。时间格式、粒度选择和区间对齐规则见 [Usage](https://help.aliyun.com/zh/model-studio/usage-api#h-usage-time)。

## 接口

**POST** `/usage/trend`

按小时、UTC+8 自然日或自然月查询用量变化。每个时间段返回总量、模型明细和工具明细，结果按时间升序分页。

## 请求体

参数

必填

类型

说明

`dimension`

是

string

取值仅为小写 `workspace`、`agent`，区分大小写。不支持 `session`

`agent_id`

条件必填

string

`dimension=agent` 时必填，指定一个 Agent；`workspace` 维度不传

`agent_version`

否

string

仅 `dimension=agent` 可用。不传或为 `null` 时合并全部版本；不能是空字符串或纯空白，按原始字符串精确匹配，不自动去除首尾空格

`time_range`

是

object

查询时间范围

`time_range.start_time`

是

string

带时区的秒级 RFC 3339 开始时间；秒可以非零，无需对齐整分钟，不接受小数秒

`time_range.end_time`

是

string

结束时间，格式同上，必须晚于开始时间

`granularity`

否

string

`hour`、`day` 或 `month`；不传时自动选择，不接受显式 `null`

`page_size`

否

integer

每页最多返回的时间段数量，取值 `1`～`100`，默认 `100`；不接受显式 `null`

`page_token`

否

string

首次查询不传。续页原样传入上一页的 `next_page_token`，不解析或自行拼接；不接受显式 null、空字符串、纯空白或无效游标

`workspace` 维度不传 Agent 筛选参数，传入时返回 HTTP 400 / `invalid_parameter`；`agent` 维度的 `agent_id` 必须为非空单值。Body 字段均直接放在 JSON 根对象中。

## 请求示例

查询当前工作空间的小时用量趋势，使用秒级起止时间。为演示分页，设置 `page_size=1`：

```
curl -X POST "$AGENTSTUDIO_URL/usage/trend" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "dimension": "workspace",
    "time_range": {
      "start_time": "2026-11-02T10:15:30+08:00",
      "end_time": "2026-11-02T14:00:01+08:00"
    },
    "granularity": "hour",
    "page_size": 1
  }'
```

查询 Agent 趋势时，将 `dimension` 改为 `agent`，并添加 `agent_id`；需要限定版本时，再添加 `agent_version`。

## 响应示例

成功时返回 HTTP 200。上述请求实际统计 UTC+8 10:00—15:00。以下示例假设该区间仅 10:00—11:00 和 13:00—14:00 存在汇总统计记录；第一页返回第一个时间段：

```
{
  "request_id": "req_trend_example",
  "data": {
    "query_range": {
      "start_time": "2026-11-02T10:00:00+08:00",
      "end_time": "2026-11-02T15:00:00+08:00"
    },
    "data_updated_at": "2026-11-02T11:05:00+08:00",
    "granularity": "hour",
    "points": [
      {
        "start_time": "2026-11-02T10:00:00+08:00",
        "end_time": "2026-11-02T11:00:00+08:00",
        "usage": {
          "total": {
            "input_tokens": {"value": 600, "unit": "tokens"},
            "output_tokens": {"value": 120, "unit": "tokens"},
            "total_tokens": {"value": 720, "unit": "tokens"},
            "cache_read_tokens": {"value": 240, "unit": "tokens"},
            "cache_creation_tokens": {"value": 60, "unit": "tokens"},
            "cache_hit_ratio": {"value": 0.4, "unit": "ratio"},
            "model_call_count": {"value": 3, "unit": "count"},
            "tool_call_count": {"value": 2, "unit": "count"},
            "builtin_tool_call_count": {"value": 0, "unit": "count"},
            "mcp_tool_call_count": {"value": 2, "unit": "count"},
            "custom_tool_call_count": {"value": 0, "unit": "count"},
            "turns": {"value": 1, "unit": "count"},
            "steps": {"value": 5, "unit": "count"},
            "interrupt_error_count": {"value": 0, "unit": "count"},
            "model_failed_count": {"value": 1, "unit": "count"},
            "tool_failed_count": {"value": 1, "unit": "count"},
            "runtime_ms": {"value": 36000, "unit": "ms"}
          },
          "models": [
            {
              "model_name": "qwen-plus",
              "usage": {
                "input_tokens": {"value": 600, "unit": "tokens"},
                "output_tokens": {"value": 120, "unit": "tokens"},
                "total_tokens": {"value": 720, "unit": "tokens"},
                "cache_read_tokens": {"value": 240, "unit": "tokens"},
                "cache_creation_tokens": {"value": 60, "unit": "tokens"},
                "cache_hit_ratio": {"value": 0.4, "unit": "ratio"},
                "call_count": {"value": 3, "unit": "count"},
                "failed_count": {"value": 1, "unit": "count"}
              }
            }
          ],
          "tools": [
            {
              "source": "mcp",
              "tool_name": "web_search",
              "usage": {
                "call_count": {"value": 2, "unit": "count"},
                "failed_count": {"value": 1, "unit": "count"}
              }
            }
          ]
        }
      }
    ],
    "has_more": true,
    "next_page_token": "v1_0123456789abcdef0123456789abcdef"
  }
}
```

## 响应字段

字段

类型

说明

`request_id`

string

请求标识

`data.query_range`

object

整次查询对齐后的实际区间，各页保持一致，不是当前页的起止范围

`data.query_range.start_time`

string

整次查询的开始时间，包含该时刻，使用 `+08:00` 时区

`data.query_range.end_time`

string

整次查询的结束时间，不包含该时刻，使用 `+08:00` 时区

`data.data_updated_at`

string / null

当前页返回用量记录中最近的已知更新时间，无记录或更新时间未知时为 `null`。不同页的值可能不同

`data.granularity`

string

实际使用的粒度：`hour`、`day` 或 `month`

`data.points`

array

当前页的时间段列表，按 `start_time` 升序；无记录时为 `[]`

`data.points[].start_time`

string

当前时间段的开始时间，包含该时刻，使用 `+08:00` 时区

`data.points[].end_time`

string

当前时间段的结束时间，不包含该时刻，使用 `+08:00` 时区

`data.points[].usage`

object

当前时间段的用量，包含 `total`、`models`、`tools`，结构见 [用量对象](https://help.aliyun.com/zh/model-studio/usage-api#h-usage-object)

`data.has_more`

boolean

是否还有下一页

`data.next_page_token`

string / null

下一页游标。`has_more=true` 时为非空字符串；末页为 `null`

## 分页

将上一页返回的 `next_page_token` 原样传入 `page_token`。保持同一主账号、工作空间、维度、Agent、版本、原始起止时间、实际粒度及 `page_size`。起止时间按同一绝对时刻比较，等价时区写法可以互换；即使对齐后的 `query_range` 相同，也不能修改原始时间边界。

以下游标仅为格式示例，实际调用时请替换为上一页返回的值：

```
curl -X POST "$AGENTSTUDIO_URL/usage/trend" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "dimension": "workspace",
    "time_range": {
      "start_time": "2026-11-02T10:15:30+08:00",
      "end_time": "2026-11-02T14:00:01+08:00"
    },
    "granularity": "hour",
    "page_size": 1,
    "page_token": "v1_0123456789abcdef0123456789abcdef"
  }'
```

本例下一页返回 13:00—14:00 的用量，`has_more=false`、`next_page_token=null`，分页结束。

-   每个游标自生成起有效期为 15 分钟，有效期内可重试；重试同一游标不会延长其有效期。游标失效返回 HTTP 410 / `page_token_expired`，此时去掉 `page_token`，重新查询第一页。
-   分页单位是完整时间段，`page_size` 只限制时间段数量。一个时间段内的模型和工具明细一起返回；本页全部时间段的模型与工具明细项合计最多 100,000，汇总 `total` 不计入该上限。
-   只返回有汇总统计记录的时间段，不自动填充缺失时间段。已有记录的指标即使为 `0` 或 `null`，该时间段仍会返回。
-   首次查询没有记录时，返回 `points=[]`、`has_more=false`、`next_page_token=null`，仍保留实际 `query_range` 和 `granularity`。
-   分页期间统计数据可能继续更新，游标不锁定数据快照。续页从上一页最后一个时间段之后开始；后补到已翻过时间段的数据不会在后续页重复返回。需要刷新时从第一页重查，结果仍可能短暂命中缓存。

错误码见 [Usage](https://help.aliyun.com/zh/model-studio/usage-api#h-usage-error-codes)。
