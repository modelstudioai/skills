# 知识库日志与监控

知识库的所有检索调用都会以日志形式投递到日志服务（SLS），您可以基于这些日志做调用审计、问题排查、用量统计与告警监控。本文介绍开通方式、日志字段含义、常见使用场景。

## 开通与查看

检索日志的存储与查询全部由日志服务（SLS）承载，开通后会自动在您账号下创建固定的 Project 与 LogStore，按 SLS 实际产生的存储与流量计费（参见[日志服务收费概述](https://help.aliyun.com/zh/sls/billing-overview)）。

### **首次使用**

在[知识库列表页](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/knowledge-base)右上方单击**监控配置**，弹出知识库监控配置面板，首次使用时面板会引导完成以下工作：

1.  **授权日志服务角色权限**
    
    角色名称：AliyunServiceRoleForSFMAccessSLS
    
    角色权限策略：AliyunServiceRolePolicyForSFMAccessSLS
    
2.  **开通日志服务**
    
    使用用户日志服务 LogStore 收集和存储百炼知识库日志，支持实时查看和自定义日志分析功能。
    
3.  **创建日志服务Logstore**
    
    刷新页面，点击创建Logstore，默认打开**检索日志**开关。可点击**查看详情**访问日志库。
    
    > **检索日志**开关显示**已开启**后，所有检索调用都会实时投递到上述 LogStore，投递延迟通常为秒级。
    

### **查看与分析日志**

在[知识库列表页](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/knowledge-base)右上方单击**监控配置**，然后在监控配置面板的**存储到日志服务**区域单击**查看详情**，即可跳转到 SLS 控制台对应的[LogStore](https://sls.console.aliyun.com/lognext/project/aliyun-product-data-1673024660412530-cn-hangzhou/logsearch/bailian-rag-retrieve-log)页面，使用 SLS 的查询分析、仪表盘、告警等能力。

**说明**

关闭**检索日志**开关只会停止新日志投递，已投递的历史日志仍按 SLS 默认配置保留与计费。如需彻底停止计费，请到 SLS 控制台删除对应 LogStore。

## 字段说明

每条检索日志的 topic 为 `log_dispatch`，包含以下索引字段：

**字段**

**类型**

**含义**

`request_id`

string

单次请求的唯一 ID，用于精确定位单次调用。

`pipeline_id`

string

知识库 ID，可用于按知识库聚合统计。

`workspace_id`

string

业务空间 ID（格式：llm-xxxx），多业务空间维度的用量分析与隔离。

`user_id`

string

调用方 UID。

`path`

string

调用的 API 路径（例：/api/v1/indices/rag/index/retrieve），用于区分调用来源。

`latency`

long

请求处理耗时(毫秒)，用于性能监控与慢查询分析。

`response_status_code`

long

HTTP 状态码（200 / 4xx / 5xx），错误监控。

`response_code`

string

业务响应码，成功为 `Success`，失败为点分错误码（例如 `Index.IndexNotExist` 表示知识库不存在），配合 `response_status_code` 和 `response_message` 定位具体原因。

`response_message`

string

业务响应文本，成功为 `success`，失败时含定位信息（例如 `index not exist, index_id: xxx, workspace: llm-xxx`）。

`request_body`

json

请求体（JSON），用于详细排查请求参数。

`response_body`

json

响应体（JSON）。顶层结构 `{code, status_code, data}`，召回切片在 `data.nodes[]`，每个节点含 `score`（综合得分）、`text`（切片文本）、`metadata`（含 `doc_name`、`doc_id` 等）。可用于召回结果审计。

## 常见使用场景

以下为常见使用场景，更多语法参考[SLS 查询语法](https://help.aliyun.com/zh/sls/query-syntax/)与[SLS分析语法](https://help.aliyun.com/zh/sls/query-and-analyze-logs-in-index-mode/)。

**说明**

遇到语法问题可在查询分析框中使用 **使用 Copilot** 入口，由 SLS 内置 AI 辅助纠错与生成。

**场景一：用量统计（按知识库 / 业务空间）**

```
* | select pipeline_id, count(*) as cnt
    group by pipeline_id
    order by cnt desc
```

将 `pipeline_id` 替换为 `workspace_id` 即可改为按业务空间聚合；将聚合字段去掉、改用 `select distinct pipeline_id` 可获取活跃的知识库 ID 列表。

**场景二：按 API 路径聚合调用量**

```
* | select path, count(*) as cnt
    group by path
    order by cnt desc
```

用于查看不同检索接口的调用占比。

**更复杂的分析**

如错误请求明细、按时间窗滚动统计、跨字段联合查询等场景，建议在 SLS 查询分析框使用内置 **使用 Copilot** 入口，结合本节字段表用自然语言生成 SQL，并在 SLS 中实际运行验证。

## 使用建议

建议在 SLS 中搭建以下仪表盘组件与告警类目，具体阈值请基于您业务的历史基线设定。

**仪表盘组件**

**用途**

调用量趋势（按小时 / 天）

整体用量监控。

TopN 知识库调用排名

识别核心 / 边缘知识库。

**建议监控指标**

**说明**

业务错误率（response\_code != Success）

业务层异常监控。

HTTP 5xx 错误率

服务侧异常监控。
