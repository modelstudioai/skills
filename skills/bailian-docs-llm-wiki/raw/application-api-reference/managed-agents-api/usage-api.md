# Usage

查询 Managed Agents 的 Token 消耗、模型调用、工具调用和运行时长，支持工作空间、Agent 与 Session 维度。

## 概览

查询 Managed Agents 的 Token 消耗、模型调用、工具调用和运行时长，支持按工作空间、Agent 或 Session 获取汇总，以及按小时、UTC+8 自然日或自然月查看用量变化。

## 前提

已完成工作空间和 API Key 配置，接入方式见 [API 总览与认证](raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。

下文使用环境变量 `AGENTSTUDIO_URL` 表示 API 基地址，`DASHSCOPE_API_KEY` 表示有权访问该工作空间的 API Key，配置方法见[认证](raw/application-api-reference/managed-agents-api/managed-agents-api-authentication.md)。例如：

```
export AGENTSTUDIO_URL="https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio"
```

将 `{workspace_id}` 替换为工作空间 ID。一次请求只查询 Endpoint 对应工作空间的用量，账号和空间由鉴权网关提供。请求体中的账号或空间字段不能覆盖网关身份。

## 接口

接口

用途

[`POST /usage/summary`](raw/application-api-reference/managed-agents-api/usage-api/usage-summary.md)

查询工作空间、Agent 或 Session 的用量汇总及模型、工具明细

[`POST /usage/trend`](raw/application-api-reference/managed-agents-api/usage-api/usage-trend.md)

分页查询工作空间或 Agent 的用量趋势，每个时间段包含汇总及模型、工具明细

## 时间范围与粒度

本节适用于工作空间和 Agent 的汇总与趋势查询。Session 汇总固定查询生命周期累计用量，不使用时间范围和粒度。

### 时间格式

起止时间使用带时区的秒级 RFC 3339 字符串，支持 `Z` 或数字时区偏移。秒可以非零，无需对齐整分钟，例如：

-   `2026-11-02T10:00:30+08:00`
-   `2026-11-02T02:00:30Z`，与上一项表示同一时刻。

不接受 Unix 时间戳、缺少时区的字符串或小数秒，例如 `2026-11-02T10:00:00.123+08:00`。响应时间统一使用 `+08:00`；运行时长使用毫秒数。

### 自动选择粒度

省略 `granularity` 时，按原始请求区间选择粒度：

原始区间

使用粒度

不超过 72 小时

`hour`

超过 72 小时，且终点不晚于起点在 UTC+8 下加 3 个日历月

`day`

其他情况

`month`

显式传入 `granularity` 时使用指定粒度，支持 `hour`、`day`、`month`。

### 实际统计区间

服务按 UTC+8（Asia/Shanghai）将开始时间向前、结束时间向后对齐到完整时间段，实际区间由响应的 `query_range` 给出。

粒度

对齐边界

`hour`

每小时整点

`day`

UTC+8 每日 00:00

`month`

UTC+8 每月 1 日 00:00，自然月长度随月份变化

例如，指定 `hour` 查询 UTC+8 10:15:30—14:00:01，实际统计 10:00:00—15:00:00。结束时间已在边界上时不再扩展，例如 10:00:00—14:00:00 保持不变。

区间均为左闭右开，即包含开始时刻、不包含结束时刻。比较汇总与趋势时，使用相同的查询条件，并核对 `query_range`。比例指标需合计分子、分母后重新计算，不能直接相加或平均。

## 用量对象

汇总响应的 `data.usage` 与趋势响应的 `data.points[].usage` 使用相同结构：

字段

类型

说明

`total`

object

当前范围的汇总指标

`models`

array

模型明细，按 `model_name` 分组

`tools`

array

工具明细，按 `source`、`tool_name` 分组；同名但来源不同的工具分别返回

### 指标值与单位

每个指标包含 `value`、`unit` 两个字段：

```
{
  "input_tokens": {"value": 1000, "unit": "tokens"},
  "tool_call_count": {"value": 3, "unit": "count"},
  "runtime_ms": {"value": 60000, "unit": "ms"},
  "cache_hit_ratio": {"value": 0.4, "unit": "ratio"}
}
```

unit

value 类型

含义

`tokens`

int64 / null

Token 数量

`count`

int64 / null

次数

`ms`

int64 / null

毫秒

`ratio`

number / null

小数比例，例如 `0.4` 表示 40%

指标未知时保留对象和单位，例如 `{"value":null,"unit":"tokens"}`；已知零用量返回 `0`。不要将 `null` 当作零。

### 汇总指标（total）

字段

单位

说明

`input_tokens`

`tokens`

模型输入 Token 数

`output_tokens`

`tokens`

模型输出 Token 数

`total_tokens`

`tokens`

输入与输出 Token 之和；任一项未知时为 `null`

`cache_read_tokens`

`tokens`

从缓存读取的输入 Token 数

`cache_creation_tokens`

`tokens`

创建缓存的输入 Token 数

`cache_hit_ratio`

`ratio`

`cache_read_tokens / input_tokens`。输入为 0、输入未知或缓存读取量未知时为 `null`；结果保留 8 位小数，四舍五入

`model_call_count`

`count`

模型调用次数，按已记录的模型请求结束事件统计，包含成功和失败调用

`tool_call_count`

`count`

工具调用次数，按调用开始统计，包含成功、失败和尚未结束的调用

`builtin_tool_call_count`

`count`

内置工具调用次数

`mcp_tool_call_count`

`count`

MCP 工具调用次数

`custom_tool_call_count`

`count`

自定义工具调用次数

`turns`

`count`

交互轮数，按 `role=user` 的事件计数

`steps`

`count`

执行步骤数，每次模型请求结束、每次工具调用开始各计一步

`interrupt_error_count`

`count`

非模型、工具调用类的错误事件数；模型和工具调用失败分别计入对应失败数

`model_failed_count`

`count`

模型调用失败次数

`tool_failed_count`

`count`

已确认的工具调用失败次数

`runtime_ms`

`ms`

已结算运行片段的累计时长，尚未结算的运行片段暂不计入

缓存读取和缓存创建 Token 已属于输入用量，计算 `total_tokens` 时不要再次叠加。`total`、`models`、`tools` 是同一范围的不同统计视图，不应将总量与明细重复相加。

### 模型明细（models）

字段

类型

说明

`models[].model_name`

string / null

模型名称

`models[].usage`

object

当前模型的用量指标

`models[].usage` 包含以下指标：

字段

单位

说明

`input_tokens`、`output_tokens`、`total_tokens`

`tokens`

当前模型的输入、输出、总 Token 数，计算规则与汇总相同

`cache_read_tokens`、`cache_creation_tokens`

`tokens`

当前模型的缓存读取、缓存创建 Token 数

`cache_hit_ratio`

`ratio`

当前模型的缓存命中率，计算规则与汇总相同

`call_count`

`count`

当前模型的调用次数

`failed_count`

`count`

当前模型的调用失败次数

### 工具明细（tools）

字段

类型

说明

`tools[].source`

string / null

工具来源：`builtin`（内置工具）、`mcp`（MCP 工具）、`custom`（自定义工具）；未知时为 `null`

`tools[].tool_name`

string / null

工具名称

`tools[].usage.call_count`

object

调用次数，`unit=count`

`tools[].usage.failed_count`

object

已确认的调用失败次数，`unit=count`

工具明细不包含 Token 或运行时长指标。汇总接口不保证模型、工具明细数组的返回顺序；趋势接口的 `points` 按时间段升序返回。模型名称、工具名称或来源未知时，保留对应明细，相关字段可为 `null`。

## 数据更新与空结果

-   统计结果会随用量处理持续更新，最近发生的调用可能尚未出现在结果中。结果可能短暂命中缓存，连续请求不保证立即反映最新统计。
-   `data_updated_at` 表示本次结果中最近的已知来源更新时间，不表示该时刻之前的数据已经全部统计完成，也不是本次请求时间。
-   汇总没有匹配统计记录时，保留 `usage.total` 及各指标单位，指标 `value` 为 `null`，`models`、`tools` 为 `[]`，`data_updated_at` 为 `null`。工作空间、Agent 维度仍返回 `query_range`。
-   趋势没有匹配统计记录时返回空 `points`。缺失时间段不会自动补零。
-   汇总和趋势均完整返回本次查询包含的模型、工具明细，不以 Top N 或静默截断方式返回部分结果。模型与工具明细项合计上限为 100,000，汇总按整个查询范围计算，趋势按当前页计算；`total` 不计入该上限。超出时返回 `query_limit_exceeded`。

## 错误响应

业务错误使用以下结构。例如，分页游标失效时返回 HTTP 410：

```
{
  "type": "error",
  "error": {
    "code": "page_token_expired",
    "message": "page_token has expired; restart pagination from the first page."
  },
  "request_id": "req_error_example"
}
```

认证或工作空间路由错误由网关返回，结构为顶层的 `request_id`、`code`、`message`。例如，API Key 无效时返回 HTTP 401：

```
{
  "request_id": "req_auth_error_example",
  "code": "InvalidApiKey",
  "message": "Invalid API-key provided."
}
```

通用错误响应和工作空间路由错误说明见[错误码](raw/application-api-reference/managed-agents-api/managed-agents-api-errors.md)。两个用量接口共用请求频率限制，收到 HTTP 429 时减少并发并稍后重试。

## 错误码

HTTP 状态码

错误码

说明及处理方式

400

`invalid_parameter`

参数不合法，包括不支持的维度、粒度、时间格式、分页大小或请求体格式错误；根据 `error.message` 修正请求

400

`invalid_page_token`

分页游标格式错误，或续页身份、原始查询条件、实际粒度、`page_size` 与游标不匹配；使用上页返回的游标并保持查询条件一致。仅趋势查询

400

`query_limit_exceeded`

模型与工具明细项合计超过 100,000：汇总按整个查询范围计算，趋势按当前页计算。汇总可缩小时间范围或查询更具体的维度，趋势可减小 `page_size` 或改用更细粒度

404

`not_found`

Session 不存在或不属于当前账号和工作空间，仅适用于 Session 汇总查询

410

`page_token_expired`

分页游标已失效，移除 `page_token` 后从第一页重查。仅趋势查询

429

`rate_limit`

两个用量接口共用主账号和工作空间维度的频率限制；降低并发并稍后重试

503

`service_unavailable`

用量查询或分页服务暂不可用，稍后重试

500

`internal_error`

服务内部异常，保留 `request_id` 以便排查
