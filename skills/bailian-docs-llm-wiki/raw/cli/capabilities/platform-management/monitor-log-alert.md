# 监控、日志与告警

阿里云百炼 CLI 查询模型调用监控、调用日志并管理告警规则的命令速查。

`bl monitor`、`bl log` 和 `bl alert` 查询模型调用监控、调用日志、链路追踪和告警规则，并管理监控投递、日志投递和告警模板。

**说明**这些命令需要先完成控制台登录（`bl auth login --console`），并使用当前 Workspace 的可观测服务。首次使用监控或日志前，需要分别开通对应的投递服务。

**重要**任意命令追加 `--help` 可查看完整参数说明，例如 `bl monitor overview --help`。本文命令明细以 bl 2.8.0 为基准核实。

## 通用参数

以下参数适用于全部 `bl monitor`、`bl log` 和 `bl alert` 命令，各命令明细中不再重复列出。

参数

类型

说明

`--console-region <region>`

string

控制台网关地域，例如 cn-beijing、ap-southeast-1

`--console-site <site>`

string

控制台站点：domestic、international

`--console-switch-agent <uid>`

number

切换代理访问的 Agent UID

`--workspace-id <id>`

string

Workspace ID；也可设置 BAILIAN\_WORKSPACE\_ID

`--output <format>`

string

输出格式：text、json

-   业务结果默认使用 JSON，即使 Profile 配置为 text。需要文本输出时显式传入 `--output text` 或设置 `DASHSCOPE_OUTPUT=text`。
-   遥测命令根据选定的 Workspace 自动解析控制台身份，预检、业务请求、异步轮询和后续请求使用同一身份。
-   `bl monitor` 和 `bl alert history` 默认查询最近 7 天；`bl log` 默认查询最近 1 小时。
-   `--start-time` 和 `--end-time` 可覆盖默认时间范围，支持 ISO 日期或毫秒时间戳。
-   需要分页的命令使用 `--max-results` 和 `--skip`；返回分页 Token 时，将 `next-token` 原样传回。
-   `log audit count` 和 `log inference count` 使用对应列表接口的 `totalCount`，不遍历分页，也不获取完整日志内容。推理计数会保留多模型、多 API Key 过滤，去重后按单值组合查询并汇总；只有全部查询成功后才输出结果。

## 监控

### bl monitor overview

查看模型调用汇总，包括调用量、成功率、失败量、4xx/5xx、平均耗时、首 Token 耗时和流式调用量。

**语法**

```
bl monitor overview [--days <days>] [--start-time <time>] [--end-time <time>] [--model <model>] [--api-key-id <id>] [--channel <channel>] [--source <source>]
```

参数

类型

必填

说明

`--days <days>`

number

否

查询最近 N 天（默认：7）

`--start-time <time>`

string

否

开始时间；设置后覆盖 --days

`--end-time <time>`

string

否

结束时间；默认当前时间

`--model <model>`

string

否

模型名称，多个用逗号分隔

`--api-key-id <id>`

string

否

API Key ID，多个用逗号分隔

`--channel <channel>`

string

否

调用渠道，多个用逗号分隔

`--source <source>`

string

否

调用来源，多个用逗号分隔

**示例**：查看最近 7 天的调用汇总

```
bl monitor overview --days 7
```

### bl monitor models

按模型或 API Key 查看调用统计，支持服务端排序和分页。

**语法**

```
bl monitor models [--days <days>] [--start-time <time>] [--end-time <time>] [--model <model>] [--api-key-id <id>] [--channel <channel>] [--source <source>] [--sort-by <field>] [--order <ASC|DESC>] [--max-results <n>] [--skip <n>] [--next-token <token>]
```

参数

类型

必填

说明

`--days <days>`

number

否

查询最近 N 天（默认：7）

`--start-time <time>`

string

否

开始时间；设置后覆盖 --days

`--end-time <time>`

string

否

结束时间

`--model <model>`

string

否

模型名称，多个用逗号分隔

`--api-key-id <id>`

string

否

API Key ID，多个用逗号分隔

`--channel <channel>`

string

否

调用渠道，多个用逗号分隔

`--source <source>`

string

否

调用来源，多个用逗号分隔

`--sort-by <field>`

string

否

排序字段：modelAndWorkspaceId、callCount、callSuccessCount、callFailedCount、callFailedPercent、avgCallDuration、avgFirstTokenDuration（默认：callCount）

`--order <ASC|DESC>`

string

否

排序方向（默认：DESC）

`--max-results <n>`

number

否

每页行数，1–50（默认：10）

`--skip <n>`

number

否

跳过的行数（默认：0）

`--next-token <token>`

string

否

上一次响应返回的分页 Token

**示例**：按失败次数降序查看前 3 个模型

```
bl monitor models --days 7 --sort-by callFailedCount --order DESC --max-results 3
```

### bl monitor metrics

查询时间序列指标，例如调用量、失败量、耗时分位和 Token 用量。

**语法**

```
bl monitor metrics --metric <name>[,<name>...] [--agg <agg>] [--step <seconds>] [--days <days>] [--start-time <time>] [--end-time <time>] [--model <model>] [--api-key-id <id>] [--channel <channel>] [--source <source>]
```

参数

类型

必填

说明

`--metric <name>`

string

是

指标名称，多个用逗号分隔

`--agg <agg>`

string

否

聚合方式：sum、avg、max、min、p50、p95、p99、cumsum、cumavg、sum\_pm（默认：sum）

`--step <seconds>`

number

否

数据点间隔：60、3600 或 86400（默认按时间范围自动选择）

`--days <days>`

number

否

查询最近 N 天（默认：7）

`--start-time <time>`

string

否

开始时间；设置后覆盖 --days

`--end-time <time>`

string

否

结束时间

`--model <model>`

string

否

模型名称，多个用逗号分隔

`--api-key-id <id>`

string

否

API Key ID，多个用逗号分隔

`--channel <channel>`

string

否

调用渠道，多个用逗号分隔

`--source <source>`

string

否

调用来源，多个用逗号分隔

查看支持的指标

指标

说明

`model_call_count`

调用次数

`model_call_duration`

调用耗时

`model_first_token_duration`

首 Token 耗时

`model_generation_duration_per_token`

每 Token 生成耗时

`model_call_failed_count`

失败次数

`model_call_4xx_count`

4xx 次数

`model_call_5xx_count`

5xx 次数

`model_call_429_count`

429 次数

`model_call_data_inspection_failed_count`

内容安全检查失败次数

`model_total_amount`

总用量

`model_input_amount`

输入用量

`model_output_amount`

输出用量

`model_usage`

模型用量

`model_tps_per_request`

单请求 TPS

`model_cache_hit_percent`

缓存命中率

`model_ptu_token_quota`

PTU Token 配额

`model_ptu_usage_quota`

PTU 已用配额

`model_ptu_total_tokens`

PTU 总 Token 数

`model_ptu_quota`

PTU 配额

`model_ptu_utilization`

PTU 利用率

**示例**：查询最近 1 小时的调用量和失败量

```
bl monitor metrics --metric model_call_count,model_call_failed_count --days 1 --step 3600
```

-   监控统计只计入实时（在线）推理调用。
-   同时设置 `--days` 和 `--start-time` 时，以 `--start-time` 为准。

### bl monitor errors

按 HTTP 状态码和错误码查看失败分布。

**语法**

```
bl monitor errors [--days <days>] [--start-time <time>] [--end-time <time>] [--model <model>] [--api-key-id <id>] [--channel <channel>] [--source <source>]
```

参数

类型

必填

说明

`--days <days>`

number

否

查询最近 N 天（默认：7）

`--start-time <time>`

string

否

开始时间；设置后覆盖 --days

`--end-time <time>`

string

否

结束时间

`--model <model>`

string

否

模型名称，多个用逗号分隔

`--api-key-id <id>`

string

否

API Key ID，多个用逗号分隔

`--channel <channel>`

string

否

调用渠道，多个用逗号分隔

`--source <source>`

string

否

调用来源，多个用逗号分隔

**示例**：查看最近 7 天的失败分布

```
bl monitor errors --days 7
```

-   返回列表包含 `httpStatusCode`、`errorCode`、`callCount` 和 `callPercent`。
-   `errorCode` 为 `null` 时表示没有可用的服务端错误码。

### bl monitor delivery status

查看监控投递状态，包括 CMS 服务关联角色、CMS 服务、Prometheus 实例和投递开关。

**语法**

```
bl monitor delivery status
```

**示例**：查看监控投递状态

```
bl monitor delivery status
```

-   未开通时返回 `Telemetry.SlrNotExist` 或 `cmsSlrAuthorized: false`。
-   文本输出会给出下一步操作提示。

### bl monitor delivery enable

开通监控投递：检查 CMS 服务关联角色状态（缺失时中止并提示手动授权）、开通 CMS 服务、创建专用 Prometheus 实例，并打开全部模型的监控投递开关。

**语法**

```
bl monitor delivery enable [--no-wait]
```

参数

类型

必填

说明

`--no-wait`

switch

否

提交开通请求后立即返回，不等待实例就绪

**警告**该操作会开通 CMS 服务和 Prometheus 实例，可能产生费用。先使用 --dry-run 查看请求，确认后再执行。

**示例**：开通监控投递

```
bl monitor delivery enable
```

-   开通步骤：检查 CMS 服务关联角色状态（缺失时中止并提示手动授权）→ 开通 CMS 服务（异步轮询）→ 创建 Prometheus 实例（异步轮询）→ 打开投递开关。
-   服务端会对 30 秒内的重复提交做限流。

### bl monitor delivery disable

关闭全部模型的监控投递开关。

**语法**

```
bl monitor delivery disable
```

**示例**：预览关闭监控投递

```
bl monitor delivery disable --dry-run
```

-   仅关闭投递开关；CMS 服务和 Prometheus 实例（含已存数据）会保留。
-   重新执行 `bl monitor delivery enable` 可恢复投递。

## 日志

### bl log status

查看日志投递状态，包括 SLS 授权、审计日志和推理日志的服务与开关。

**语法**

```
bl log status
```

**示例**：查看日志投递状态

```
bl log status
```

-   审计日志和推理日志有独立开关；推理日志要求审计日志保持开启。
-   未开通时返回 `Telemetry.SlrNotExist`，可先执行 `bl log audit enable`。

### bl log audit list

查询模型审计日志。审计日志记录调用元数据，不记录请求和响应内容。

**语法**

```
bl log audit list [--hours <n>] [--start-time <time>] [--end-time <time>] [--model <model>] [--api-key-id <id>] [--channel <channel>] [--source <source>] [--call-source <Online|Offline>] [--request-id <id>] [--status-code <type>] [--max-results <n>] [--skip <n>] [--next-token <token>]
```

参数

类型

必填

说明

`--hours <hours>`

number

否

查询最近 N 小时（默认：1）

`--start-time <time>`

string

否

开始时间；设置后覆盖 --hours

`--end-time <time>`

string

否

结束时间

`--model <model>`

string

否

模型名称，多个用逗号分隔

`--api-key-id <id>`

string

否

API Key ID，多个用逗号分隔

`--channel <channel>`

string

否

调用渠道，多个用逗号分隔

`--source <source>`

string

否

调用来源，多个用逗号分隔

`--call-source <Online|Offline>`

string

否

推理类型：Online、Offline

`--request-id <id>`

string

否

精确匹配模型请求 ID

`--status-code <type>`

string

否

状态筛选：SUCCESS、CLIENT\_ERROR、SERVER\_ERROR、CANCEL，多个用逗号分隔

`--max-results <n>`

number

否

每页行数（默认：20）

`--skip <n>`

number

否

跳过的行数（默认：0）

`--next-token <token>`

string

否

上一次响应返回的分页 Token

**示例**：查询最近 1 小时的审计日志

```
bl log audit list --hours 1 --max-results 20
```

-   审计日志包含调用时间、模型、状态码、耗时、Token 用量和请求 ID。
-   请求和响应内容请使用推理日志查询。

### bl log audit get

查看单条审计日志及其原始记录。

**语法**

```
bl log audit get --request-id <id> [--hours <n>] [--start-time <time>] [--end-time <time>] [--model <model>]
```

参数

类型

必填

说明

`--request-id <id>`

string

是

模型请求 ID（可从 `log audit list` 获取）

`--hours <hours>`

number

否

查询最近 N 小时（默认：1）

`--start-time <time>`

string

否

开始时间；设置后覆盖 --hours

`--end-time <time>`

string

否

结束时间

`--model <model>`

string

否

模型名称，用于缩小搜索范围

**示例**：查看指定请求 ID 的审计日志

```
bl log audit get --request-id 12345678-abcd-1234-abcd-123456789012 --hours 2
```

### bl log audit count

统计时间范围内的审计日志数量，适合导出前估算。

**语法**

```
bl log audit count [--hours <n>] [--start-time <time>] [--end-time <time>] [--model <model>] [--api-key-id <id>]
```

参数

类型

必填

说明

`--hours <hours>`

number

否

查询最近 N 小时（默认：1）

`--start-time <time>`

string

否

开始时间；设置后覆盖 --hours

`--end-time <time>`

string

否

结束时间

`--model <model>`

string

否

模型名称，多个用逗号分隔

`--api-key-id <id>`

string

否

API Key ID，多个用逗号分隔

**示例**：统计最近 24 小时的审计日志数量

```
bl log audit count --hours 24
```

### bl log audit enable

开通审计日志投递：检查 SLS 服务关联角色状态（缺失时中止并提示手动授权）、初始化 SLS 实例，并打开全部模型的审计日志开关。

**语法**

```
bl log audit enable [--no-wait]
```

参数

类型

必填

说明

`--no-wait`

switch

否

提交请求后立即返回，不等待 SLS 实例就绪

**警告**该操作会初始化 SLS 实例并产生日志存储费用。先使用 --dry-run 查看请求，确认后再执行。

**示例**：开通审计日志投递

```
bl log audit enable
```

-   开通审计日志是开通推理日志的前提。
-   审计日志仅记录调用元数据。

### bl log audit disable

关闭全部模型的审计日志投递。

**语法**

```
bl log audit disable
```

**示例**：预览关闭审计日志投递

```
bl log audit disable --dry-run
```

-   推理日志仍开启时会被拒绝；先执行 `bl log inference disable`。

### bl log inference list

查询模型推理日志，包含请求和响应内容。

**语法**

```
bl log inference list [--hours <n>] [--start-time <time>] [--end-time <time>] [--model <model>] [--api-key-id <id>] [--request-id <id>] [--status-code <type>] [--call-source <Online|Offline>] [--max-results <n>] [--skip <n>]
```

参数

类型

必填

说明

`--hours <hours>`

number

否

查询最近 N 小时（默认：1）

`--start-time <time>`

string

否

开始时间；设置后覆盖 --hours

`--end-time <time>`

string

否

结束时间

`--model <model>`

string

否

模型名称；推理日志 API 只接受单个模型

`--api-key-id <id>`

string

否

API Key ID；推理日志 API 只接受单个 ID

`--request-id <id>`

string

否

精确匹配模型请求 ID

`--status-code <type>`

string

否

状态筛选：SUCCESS、CLIENT\_ERROR、SERVER\_ERROR、CANCEL，多个用逗号分隔

`--call-source <Online|Offline>`

string

否

推理类型：Online、Offline

`--max-results <n>`

number

否

每页行数（默认：20）

`--skip <n>`

number

否

跳过的行数（默认：0）

**示例**：查询最近 1 小时的推理日志

```
bl log inference list --hours 1 --max-results 20
```

-   需要先开通推理日志投递。
-   返回列表只包含摘要；完整请求和响应内容使用 `log inference get`。

### bl log inference get

查看单条推理日志的完整请求和响应内容。

**语法**

```
bl log inference get --request-id <id> [--hours <n>] [--start-time <time>] [--end-time <time>] [--model <model>]
```

参数

类型

必填

说明

`--request-id <id>`

string

是

模型请求 ID（可从 `log inference list` 获取）

`--hours <hours>`

number

否

查询最近 N 小时（默认：1）

`--start-time <time>`

string

否

开始时间；设置后覆盖 --hours

`--end-time <time>`

string

否

结束时间

`--model <model>`

string

否

模型名称，用于缩小搜索范围

**示例**：查看指定请求的完整推理日志

```
bl log inference get --request-id 12345678-abcd-1234-abcd-123456789012 --hours 2
```

### bl log inference count

统计时间范围内的推理日志数量。

**语法**

```
bl log inference count [--hours <n>] [--start-time <time>] [--end-time <time>] [--model <model>] [--api-key-id <id>]
```

参数

类型

必填

说明

`--hours <hours>`

number

否

查询最近 N 小时（默认：1）

`--start-time <time>`

string

否

开始时间；设置后覆盖 --hours

`--end-time <time>`

string

否

结束时间

`--model <model>`

string

否

模型名称，多个用逗号分隔

`--api-key-id <id>`

string

否

API Key ID，多个用逗号分隔

**示例**：统计最近 24 小时的推理日志数量

```
bl log inference count --hours 24
```

-   只统计推理日志投递开启期间的调用。

### bl log inference enable

开通推理日志投递：检查 SLS 服务关联角色状态（缺失时中止并提示手动授权）、初始化 SLS 实例，并打开全部模型的推理日志开关。

**语法**

```
bl log inference enable [--no-wait]
```

参数

类型

必填

说明

`--no-wait`

switch

否

提交请求后立即返回，不等待 SLS 实例就绪

**警告**该操作会初始化 SLS 实例并记录请求、响应内容，可能产生存储费用。先使用 --dry-run 查看请求，确认后再执行。

**示例**：开通推理日志投递

```
bl log inference enable
```

-   必须先开通审计日志（`bl log audit enable`）。

### bl log inference disable

关闭全部模型的推理日志投递。

**语法**

```
bl log inference disable
```

**示例**：预览关闭推理日志投递

```
bl log inference disable --dry-run
```

-   仅关闭推理日志；审计日志开关保持不变。

### bl log trace list

列出模型或应用的调用链路。

**语法**

```
bl log trace list --resource-id <id> [--resource-type <model|app>] [--hours <n>] [--start-time <time>] [--end-time <time>] [--max-results <n>] [--skip <n>]
```

参数

类型

必填

说明

`--resource-id <id>`

string

是

要查询的模型名称或应用 ID

`--resource-type <model|app>`

string

否

资源类型：model、app（默认：model）

`--hours <hours>`

number

否

查询最近 N 小时（默认：1）

`--start-time <time>`

string

否

开始时间；设置后覆盖 --hours

`--end-time <time>`

string

否

结束时间

`--max-results <n>`

number

否

每页行数（默认：20）

`--skip <n>`

number

否

跳过的行数（默认：0）

**示例**：列出指定模型的调用链路

```
bl log trace list --resource-id qwen3.6-plus --hours 1
```

### bl log trace get

查看单条调用链路的 Span 树。

**语法**

```
bl log trace get --trace-id <id> [--resource-id <id>] [--hours <n>] [--start-time <time>] [--end-time <time>]
```

参数

类型

必填

说明

`--trace-id <id>`

string

是

链路 ID（可从 `log trace list` 获取）

`--resource-id <id>`

string

否

模型名称或应用 ID，用于缩小搜索范围

`--hours <hours>`

number

否

查询最近 N 小时（默认：1）

`--start-time <time>`

string

否

开始时间；设置后覆盖 --hours

`--end-time <time>`

string

否

结束时间

**示例**：查看指定链路的 Span 树

```
bl log trace get --trace-id trace_xxx --resource-id qwen3.6-plus
```

### bl log trace stats

查看按资源聚合的链路统计，包括调用次数、Token 用量和延迟。

**语法**

```
bl log trace stats [--resource-id <id>] [--resource-type <model|app>] [--hours <n>] [--start-time <time>] [--end-time <time>]
```

参数

类型

必填

说明

`--resource-id <id>`

string

否

模型名称或应用 ID，多个用逗号分隔；省略时查询全部

`--resource-type <model|app>`

string

否

资源类型：model、app（默认：model）

`--hours <hours>`

number

否

查询最近 N 小时（默认：1）

`--start-time <time>`

string

否

开始时间；设置后覆盖 --hours

`--end-time <time>`

string

否

结束时间

**示例**：查看最近 1 小时的应用链路统计

```
bl log trace stats --resource-type app --hours 1
```

-   按实测，`--resource-type model` 可能返回 `Not support resourceType model`；应用链路请使用 `--resource-type app`。

## 告警

### bl alert metrics

列出可用于告警规则的指标及其支持的聚合方式。

**语法**

```
bl alert metrics
```

**示例**：查看可用告警指标

```
bl alert metrics
```

-   需要先开通监控投递（`bl monitor delivery enable`）。
-   未开通时返回 `The monitoring service is not activated yet`。

### bl alert template list

列出官方和自定义告警模板；传入 `--template-id` 查看单个模板详情。

**语法**

```
bl alert template list [--template-id <id>] [--name <name>] [--source <Official|Customize>] [--max-results <n>] [--skip <n>]
```

参数

类型

必填

说明

`--template-id <id>`

string

否

精确查询单个模板

`--name <name>`

string

否

按模板名称模糊筛选

`--source <Official|Customize>`

string

否

模板来源：Official、Customize；省略时查询全部

`--max-results <n>`

number

否

每页行数（默认：50）

`--skip <n>`

number

否

跳过的行数（默认：0）

**示例**：查看官方告警模板

```
bl alert template list --source Official
```

### bl alert template create

创建自定义告警模板，或通过 `--from` 复制已有模板。

**语法**

```
bl alert template create --name <name> [--condition <metric:agg:cmp:value:period>...] [--from <template-id>] [--logical-operator <or|and>]
```

参数

类型

必填

说明

`--name <name>`

string

是

模板名称，最多 64 个字符

`--condition <metric:agg:cmp:value:period>`

array

否

告警条件，可重复 1–10 次

`--from <template-id>`

string

否

复制已有模板的条件

`--logical-operator <or|and>`

string

否

多条件组合方式（默认：or）

**示例**：创建失败次数告警模板

```
bl alert template create --name 失败次数告警 --condition 'model_call_failed_count:sum:>:10:60'
```

-   条件格式为 `指标:聚合:比较:阈值:周期`，例如 `model_call_failed_count:sum:>:10:60`。
-   条件中包含 `>` 或 `<` 时，必须用引号包裹整条条件，避免被 Shell 当作重定向。
-   指标名称可通过 `bl alert metrics` 查看。

### bl alert template update

更新自定义告警模板，完整替换条件列表。

**语法**

```
bl alert template update --template-id <id> --name <name> --condition <metric:agg:cmp:value:period>... [--logical-operator <or|and>]
```

参数

类型

必填

说明

`--template-id <id>`

string

是

模板 ID

`--name <name>`

string

是

模板名称，最多 64 个字符

`--condition <metric:agg:cmp:value:period>`

array

是

告警条件，可重复 1–10 次

`--logical-operator <or|and>`

string

否

多条件组合方式（默认：or）

**示例**：更新失败次数阈值

```
bl alert template update --template-id 123 --name 失败次数告警 --condition 'model_call_failed_count:sum:>:20:60'
```

### bl alert template delete

删除自定义告警模板。官方模板不能删除。

**语法**

```
bl alert template delete --template-id <id>[,<id>...]
```

参数

类型

必填

说明

`--template-id <id>`

string

是

模板 ID，多个用逗号分隔

`--yes`

switch

否

确认执行此高风险操作

**警告**该操作会永久删除告警模板，且无法撤销。

**示例**：预览删除告警模板

```
bl alert template delete --template-id 123 --dry-run
```

### bl alert list

列出模型告警规则。

**语法**

```
bl alert list [--rule-id <id>] [--name <name>] [--enabled <true|false>] [--level <INFO|WARNING|ERROR>] [--max-results <n>] [--skip <n>] [--next-token <token>]
```

参数

类型

必填

说明

`--rule-id <id>`

string

否

精确查询规则 ID

`--name <name>`

string

否

按规则名称模糊筛选

`--enabled <true|false>`

string

否

按启用状态筛选

`--level <INFO|WARNING|ERROR>`

string

否

按告警等级筛选

`--max-results <n>`

number

否

每页行数（默认：20）

`--skip <n>`

number

否

跳过的行数（默认：0）

`--next-token <token>`

string

否

上一次响应返回的分页 Token

**示例**：查看已启用的告警规则

```
bl alert list --enabled true
```

### bl alert create

基于告警模板创建模型告警规则。

**语法**

```
bl alert create --name <name> --template-id <id> --model <model> [--message <text>] [--level <INFO|WARNING|ERROR>] [--interval <seconds>] [--duration <seconds>] [--contact <id>] [--contact-group <id>] [--notify-window <HH:mm-HH:mm>] [--notify-days <days>] [--silence <seconds>] [--gmt-offset <offset>]
```

参数

类型

必填

说明

`--name <name>`

string

是

告警规则名称，最多 64 个字符

`--template-id <id>`

string

是

告警模板 ID（通过 `alert template list` 获取）

`--model <model>`

string

是

要告警的模型名称，多个用逗号分隔

`--message <text>`

string

否

告警通知内容（Go Template）；默认使用控制台模板

`--level <INFO|WARNING|ERROR>`

string

否

告警等级（默认：INFO）

`--interval <seconds>`

number

否

检查间隔（默认：60）

`--duration <seconds>`

number

否

条件持续多久后触发；0 表示立即（默认：60）

`--contact <id>`

string

否

CloudMonitor 告警联系人 ID，多个用逗号分隔

`--contact-group <id>`

string

否

CloudMonitor 告警联系人组 ID，多个用逗号分隔

`--notify-window <HH:mm-HH:mm>`

string

否

每日通知时间段（默认：00:00-23:59）

`--notify-days <days>`

string

否

通知星期，1–7，多个用逗号分隔（默认：每天）

`--silence <seconds>`

number

否

重复通知的静默时间（默认：不重复）

`--gmt-offset <offset>`

string

否

通知时间段的时区偏移（默认：+0800）

**示例**：为指定模型创建失败次数告警

```
bl alert create --name high-failure-rate --template-id 123 --model qwen3.6-plus
```

-   告警条件来自模板；先通过 `alert template list` 选择模板。
-   联系人和联系人组需要在 CloudMonitor 控制台创建，再通过 ID 传入。
-   创建前可使用 `--dry-run` 查看请求体。

### bl alert update

更新模型告警规则，完整替换字段。

**语法**

```
bl alert update --rule-id <id> --name <name> --template-id <id> --model <model> [--message <text>] [--level <INFO|WARNING|ERROR>] [--interval <seconds>] [--duration <seconds>] [--contact <id>] [--contact-group <id>] [--notify-window <HH:mm-HH:mm>] [--notify-days <days>] [--silence <seconds>] [--gmt-offset <offset>]
```

参数

类型

必填

说明

`--rule-id <id>`

string

是

告警规则 ID（通过 `alert list` 获取）

`--name <name>`

string

是

告警规则名称

`--template-id <id>`

string

是

告警模板 ID

`--model <model>`

string

是

要告警的模型名称，多个用逗号分隔

`--message <text>`

string

否

告警通知内容（Go Template）

`--level <INFO|WARNING|ERROR>`

string

否

告警等级（默认：INFO）

`--interval <seconds>`

number

否

检查间隔（默认：60）

`--duration <seconds>`

number

否

条件持续多久后触发（默认：60）

`--contact <id>`

string

否

告警联系人 ID，多个用逗号分隔

`--contact-group <id>`

string

否

告警联系人组 ID，多个用逗号分隔

`--notify-window <HH:mm-HH:mm>`

string

否

每日通知时间段

`--notify-days <days>`

string

否

通知星期，1–7

`--silence <seconds>`

number

否

重复通知的静默时间

`--gmt-offset <offset>`

string

否

通知时间段的时区偏移

**示例**：更新告警等级

```
bl alert update --rule-id 789 --name high-failure-rate --template-id 123 --model qwen3.6-plus --level WARNING
```

### bl alert delete

删除模型告警规则。

**语法**

```
bl alert delete --rule-id <id>[,<id>...]
```

参数

类型

必填

说明

`--rule-id <id>`

string

是

告警规则 ID，多个用逗号分隔

`--yes`

switch

否

确认执行此高风险操作

**警告**该操作会永久删除告警规则，且无法撤销。

**示例**：预览删除告警规则

```
bl alert delete --rule-id 789 --dry-run
```

### bl alert enable

启用模型告警规则。

**语法**

```
bl alert enable --rule-id <id>
```

参数

类型

必填

说明

`--rule-id <id>`

string

是

告警规则 ID

**示例**：启用指定告警规则

```
bl alert enable --rule-id 789
```

### bl alert disable

停用模型告警规则。规则保留，但停止发送通知。

**语法**

```
bl alert disable --rule-id <id>
```

参数

类型

必填

说明

`--rule-id <id>`

string

是

告警规则 ID

**示例**：停用指定告警规则

```
bl alert disable --rule-id 789
```

### bl alert history

查看模型告警历史，包括触发和恢复事件。

**语法**

```
bl alert history [--days <days>] [--start-time <time>] [--end-time <time>] [--rule-id <id>] [--status <ALARM|OK>] [--level <INFO|WARNING|ERROR>] [--max-results <n>] [--skip <n>] [--next-token <token>]
```

参数

类型

必填

说明

`--days <days>`

number

否

查询最近 N 天（默认：7）

`--start-time <time>`

string

否

开始时间；设置后覆盖 --days

`--end-time <time>`

string

否

结束时间

`--rule-id <id>`

string

否

按告警规则 ID 筛选

`--status <ALARM|OK>`

string

否

告警状态：ALARM（触发）、OK（恢复）

`--level <INFO|WARNING|ERROR>`

string

否

按最高告警等级筛选

`--max-results <n>`

number

否

每页行数，1–50（默认：10）

`--skip <n>`

number

否

跳过的行数（默认：0）

`--next-token <token>`

string

否

上一次响应返回的分页 Token

**示例**：查看最近 7 天触发过的告警

```
bl alert history --days 7 --status ALARM
```
