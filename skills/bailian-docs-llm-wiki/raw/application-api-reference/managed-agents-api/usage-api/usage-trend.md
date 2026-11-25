# 查询用量趋势

按小时、UTC+8 自然日或自然月分页查询工作空间或 Agent 的用量趋势。

<a id="前提"></a>

<a id="h-usage-trend-prereq"></a>

## 前提

已完成工作空间和 API Key 配置，接入方式见 [API 总览与认证](../managed-agents-api-overview.md)。时间格式、粒度选择和区间对齐规则见 [Usage](../usage-api.md#h-usage-time)。

<a id="接口"></a>

<a id="h-usage-trend-endpoint"></a>

## 接口

**POST** `/usage/trend`

按小时、UTC+8 自然日或自然月查询用量变化。每个时间段返回总量、模型明细和工具明细，结果按时间升序分页。

<table><tbody><tr><td><a id="h-usage-trend-req"></a><h2>请求体</h2><p><strong>dimension</strong> <code>string</code> <strong>（必选）</strong></p><p>取值仅为小写 <code>workspace</code>、<code>agent</code>，区分大小写。不支持 <code>session</code></p><p><strong>agent_id</strong> <code>string</code> <strong>（条件必填）</strong></p><p><code>dimension=agent</code> 时必填，指定一个 Agent；<code>workspace</code> 维度不传</p><p><strong>agent_version</strong> <code>string</code> <strong>（可选）</strong></p><p>仅 <code>dimension=agent</code> 可用。不传或为 <code>null</code> 时合并全部版本；不能是空字符串或纯空白，按原始字符串精确匹配，不自动去除首尾空格</p><p><strong>time_range</strong> <code>object</code> <strong>（必选）</strong></p><p>查询时间范围</p><p><strong>time_range.start_time</strong> <code>string</code> <strong>（必选）</strong></p><p>带时区的秒级 RFC 3339 开始时间；秒可以非零，无需对齐整分钟，不接受小数秒</p><p><strong>time_range.end_time</strong> <code>string</code> <strong>（必选）</strong></p><p>结束时间，格式同上，必须晚于开始时间</p><p><strong>granularity</strong> <code>string</code> <strong>（可选）</strong></p><p><code>hour</code>、<code>day</code> 或 <code>month</code>；不传时自动选择，不接受显式 <code>null</code></p><p><strong>page_size</strong> <code>integer</code> <strong>（可选）</strong></p><p>每页最多返回的时间段数量，取值 <code>1</code>～<code>100</code>，默认 <code>100</code>；不接受显式 <code>null</code></p><p><strong>page_token</strong> <code>string</code> <strong>（可选）</strong></p><p>首次查询不传。续页原样传入上一页的 <code>next_page_token</code>，不解析或自行拼接；不接受显式 null、空字符串、纯空白或无效游标</p><p><code>workspace</code> 维度不传 Agent 筛选参数，传入时返回 HTTP 400 / <code>invalid_parameter</code>；<code>agent</code> 维度的 <code>agent_id</code> 必须为非空单值。Body 字段均直接放在 JSON 根对象中。</p></td><td><a id="h-usage-trend-eg"></a><h2>请求示例</h2><p>查询当前工作空间的小时用量趋势，使用秒级起止时间。为演示分页，设置 <code>page_size=1</code>：</p><a id="code-block"></a><pre class="language-bash"><code>curl -X POST &quot;$AGENTSTUDIO_URL/usage/trend&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
  -H &quot;Content-Type: application/json&quot; \
  -d '{
    &quot;dimension&quot;: &quot;workspace&quot;,
    &quot;time_range&quot;: {
      &quot;start_time&quot;: &quot;2026-11-02T10:15:30+08:00&quot;,
      &quot;end_time&quot;: &quot;2026-11-02T14:00:01+08:00&quot;
    },
    &quot;granularity&quot;: &quot;hour&quot;,
    &quot;page_size&quot;: 1
  }'
</code></pre><p>查询 Agent 趋势时，将 <code>dimension</code> 改为 <code>agent</code>，并添加 <code>agent_id</code>；需要限定版本时，再添加 <code>agent_version</code>。</p></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-usage-trend-resp-fields"></a><h2>响应字段</h2><p><strong>request_id</strong> <code>string</code></p><p>请求标识</p><p><strong>data.query_range</strong> <code>object</code></p><p>整次查询对齐后的实际区间，各页保持一致，不是当前页的起止范围</p><p><strong>data.query_range.start_time</strong> <code>string</code></p><p>整次查询的开始时间，包含该时刻，使用 <code>+08:00</code> 时区</p><p><strong>data.query_range.end_time</strong> <code>string</code></p><p>整次查询的结束时间，不包含该时刻，使用 <code>+08:00</code> 时区</p><p><strong>data.data_updated_at</strong> <code>string / null</code></p><p>当前页返回用量记录中最近的已知更新时间，无记录或更新时间未知时为 <code>null</code>。不同页的值可能不同</p><p><strong>data.granularity</strong> <code>string</code></p><p>实际使用的粒度：<code>hour</code>、<code>day</code> 或 <code>month</code></p><p><strong>data.points</strong> <code>array</code></p><p>当前页的时间段列表，按 <code>start_time</code> 升序；无记录时为 <code>[]</code></p><p><strong>data.points[].start_time</strong> <code>string</code></p><p>当前时间段的开始时间，包含该时刻，使用 <code>+08:00</code> 时区</p><p><strong>data.points[].end_time</strong> <code>string</code></p><p>当前时间段的结束时间，不包含该时刻，使用 <code>+08:00</code> 时区</p><p><strong>data.points[].usage</strong> <code>object</code></p><p>当前时间段的用量，包含 <code>total</code>、<code>models</code>、<code>tools</code>，结构见 <a href="../usage-api.md#h-usage-object">用量对象</a></p><p><strong>data.has_more</strong> <code>boolean</code></p><p>是否还有下一页</p><p><strong>data.next_page_token</strong> <code>string / null</code></p><p>下一页游标。<code>has_more=true</code> 时为非空字符串；末页为 <code>null</code></p></td><td><a id="h-usage-trend-resp"></a><h2>响应示例</h2><p>成功时返回 HTTP 200。上述请求实际统计 UTC+8 10:00—15:00。以下示例假设该区间仅 10:00—11:00 和 13:00—14:00 存在汇总统计记录；第一页返回第一个时间段：</p><a id="code-block-2"></a><pre class="language-json"><code>{
  &quot;request_id&quot;: &quot;req_trend_example&quot;,
  &quot;data&quot;: {
    &quot;query_range&quot;: {
      &quot;start_time&quot;: &quot;2026-11-02T10:00:00+08:00&quot;,
      &quot;end_time&quot;: &quot;2026-11-02T15:00:00+08:00&quot;
    },
    &quot;data_updated_at&quot;: &quot;2026-11-02T11:05:00+08:00&quot;,
    &quot;granularity&quot;: &quot;hour&quot;,
    &quot;points&quot;: [
      {
        &quot;start_time&quot;: &quot;2026-11-02T10:00:00+08:00&quot;,
        &quot;end_time&quot;: &quot;2026-11-02T11:00:00+08:00&quot;,
        &quot;usage&quot;: {
          &quot;total&quot;: {
            &quot;input_tokens&quot;: {&quot;value&quot;: 600, &quot;unit&quot;: &quot;tokens&quot;},
            &quot;output_tokens&quot;: {&quot;value&quot;: 120, &quot;unit&quot;: &quot;tokens&quot;},
            &quot;total_tokens&quot;: {&quot;value&quot;: 720, &quot;unit&quot;: &quot;tokens&quot;},
            &quot;cache_read_tokens&quot;: {&quot;value&quot;: 240, &quot;unit&quot;: &quot;tokens&quot;},
            &quot;cache_creation_tokens&quot;: {&quot;value&quot;: 60, &quot;unit&quot;: &quot;tokens&quot;},
            &quot;cache_hit_ratio&quot;: {&quot;value&quot;: 0.4, &quot;unit&quot;: &quot;ratio&quot;},
            &quot;model_call_count&quot;: {&quot;value&quot;: 3, &quot;unit&quot;: &quot;count&quot;},
            &quot;tool_call_count&quot;: {&quot;value&quot;: 2, &quot;unit&quot;: &quot;count&quot;},
            &quot;builtin_tool_call_count&quot;: {&quot;value&quot;: 0, &quot;unit&quot;: &quot;count&quot;},
            &quot;mcp_tool_call_count&quot;: {&quot;value&quot;: 2, &quot;unit&quot;: &quot;count&quot;},
            &quot;custom_tool_call_count&quot;: {&quot;value&quot;: 0, &quot;unit&quot;: &quot;count&quot;},
            &quot;turns&quot;: {&quot;value&quot;: 1, &quot;unit&quot;: &quot;count&quot;},
            &quot;steps&quot;: {&quot;value&quot;: 5, &quot;unit&quot;: &quot;count&quot;},
            &quot;interrupt_error_count&quot;: {&quot;value&quot;: 0, &quot;unit&quot;: &quot;count&quot;},
            &quot;model_failed_count&quot;: {&quot;value&quot;: 1, &quot;unit&quot;: &quot;count&quot;},
            &quot;tool_failed_count&quot;: {&quot;value&quot;: 1, &quot;unit&quot;: &quot;count&quot;},
            &quot;runtime_ms&quot;: {&quot;value&quot;: 36000, &quot;unit&quot;: &quot;ms&quot;}
          },
          &quot;models&quot;: [
            {
              &quot;model_name&quot;: &quot;qwen-plus&quot;,
              &quot;usage&quot;: {
                &quot;input_tokens&quot;: {&quot;value&quot;: 600, &quot;unit&quot;: &quot;tokens&quot;},
                &quot;output_tokens&quot;: {&quot;value&quot;: 120, &quot;unit&quot;: &quot;tokens&quot;},
                &quot;total_tokens&quot;: {&quot;value&quot;: 720, &quot;unit&quot;: &quot;tokens&quot;},
                &quot;cache_read_tokens&quot;: {&quot;value&quot;: 240, &quot;unit&quot;: &quot;tokens&quot;},
                &quot;cache_creation_tokens&quot;: {&quot;value&quot;: 60, &quot;unit&quot;: &quot;tokens&quot;},
                &quot;cache_hit_ratio&quot;: {&quot;value&quot;: 0.4, &quot;unit&quot;: &quot;ratio&quot;},
                &quot;call_count&quot;: {&quot;value&quot;: 3, &quot;unit&quot;: &quot;count&quot;},
                &quot;failed_count&quot;: {&quot;value&quot;: 1, &quot;unit&quot;: &quot;count&quot;}
              }
            }
          ],
          &quot;tools&quot;: [
            {
              &quot;source&quot;: &quot;mcp&quot;,
              &quot;tool_name&quot;: &quot;web_search&quot;,
              &quot;usage&quot;: {
                &quot;call_count&quot;: {&quot;value&quot;: 2, &quot;unit&quot;: &quot;count&quot;},
                &quot;failed_count&quot;: {&quot;value&quot;: 1, &quot;unit&quot;: &quot;count&quot;}
              }
            }
          ]
        }
      }
    ],
    &quot;has_more&quot;: true,
    &quot;next_page_token&quot;: &quot;v1_0123456789abcdef0123456789abcdef&quot;
  }
}
</code></pre></td></tr></tbody></table>

<a id="分页"></a>

<a id="h-usage-trend-pagination"></a>

## 分页

将上一页返回的 `next_page_token` 原样传入 `page_token`。保持同一主账号、工作空间、维度、Agent、版本、原始起止时间、实际粒度及 `page_size`。起止时间按同一绝对时刻比较，等价时区写法可以互换；即使对齐后的 `query_range` 相同，也不能修改原始时间边界。

以下游标仅为格式示例，实际调用时请替换为上一页返回的值：

<a id="code-block-3"></a>

```bash
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

错误码见 [Usage](../usage-api.md#h-usage-error-codes)。
