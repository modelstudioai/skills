# 查询用量汇总

查询工作空间、Agent 或 Session 的用量汇总，返回总量及按模型、工具分组的明细。

<a id="前提"></a>

<a id="h-usage-summary-prereq"></a>

## 前提

已完成工作空间和 API Key 配置，接入方式见 [API 总览与认证](../managed-agents-api-overview.md)。时间格式、粒度选择和区间对齐规则见 [Usage](../usage-api.md#h-usage-time)。

<a id="接口"></a>

<a id="h-usage-summary-endpoint"></a>

## 接口

**POST** `/usage/summary`

获取指定时间范围内工作空间或 Agent 的用量，也可获取单个 Session 自创建以来累计的用量。响应同时包含总量、按模型分组的明细和按工具分组的明细。

<table><tbody><tr><td><a id="h-usage-summary-req"></a><h2>请求体</h2><p><strong>dimension</strong> <code>string</code> <strong>（必选）</strong></p><p>查询维度，区分大小写。取值仅为 <code>workspace</code>、<code>agent</code>、<code>session</code></p><p><strong>agent_id</strong> <code>string</code> <strong>（条件必填）</strong></p><p><code>dimension=agent</code> 时必填，指定一个 Agent；其他维度不传</p><p><strong>agent_version</strong> <code>string</code> <strong>（可选）</strong></p><p>仅 <code>dimension=agent</code> 可用。指定 Agent 版本；不传或为 <code>null</code> 时合并全部版本。不能是空字符串或纯空白；按原始字符串精确匹配，不自动去除首尾空格</p><p><strong>session_id</strong> <code>string</code> <strong>（条件必填）</strong></p><p><code>dimension=session</code> 时必填。使用创建 Session 时返回的 ID；必须为非空、非纯空白的单个字符串，其他维度不传</p><p><strong>time_range</strong> <code>object</code> <strong>（条件必填）</strong></p><p><code>workspace</code>、<code>agent</code> 维度必填；<code>session</code> 维度不接受</p><p><strong>time_range.start_time</strong> <code>string</code> <strong>（条件必填）</strong></p><p>使用 <code>time_range</code> 时必填。带时区的秒级 RFC 3339 字符串，例如 <code>2026-11-02T10:15:30+08:00</code>；秒可以非零，无需对齐整分钟</p><p><strong>time_range.end_time</strong> <code>string</code> <strong>（条件必填）</strong></p><p>使用 <code>time_range</code> 时必填。结束时间，格式同上，必须晚于开始时间</p><p><strong>granularity</strong> <code>string</code> <strong>（可选）</strong></p><p><code>workspace</code>、<code>agent</code> 维度可用，取值为 <code>hour</code>、<code>day</code>、<code>month</code>；不传时自动选择。影响实际统计区间的对齐方式。<code>session</code> 维度不传</p><p>三个维度的参数组合如下：</p><table><thead><tr><th>dimension</th><th>查询范围</th><th>参数要求</th></tr></thead><tbody><tr><td><code>workspace</code></td><td>当前工作空间的用量</td><td>必传 <code>time_range</code>，不传 <code>agent_id</code>、<code>agent_version</code>、<code>session_id</code></td></tr><tr><td><code>agent</code></td><td>当前工作空间内指定 Agent 的用量</td><td>必传 <code>agent_id</code>、<code>time_range</code>，可传 <code>agent_version</code>，不传 <code>session_id</code></td></tr><tr><td><code>session</code></td><td>当前工作空间内指定 Session 的生命周期累计用量</td><td>只传 <code>dimension</code>、<code>session_id</code>；不传 Agent 筛选、<code>time_range</code> 或 <code>granularity</code></td></tr></tbody></table><p><code>agent_id</code>、<code>session_id</code> 必须为非空单值。<code>time_range</code>、<code>granularity</code> 不接受显式 <code>null</code>。<code>workspace</code> 维度传入 Agent 筛选，或 <code>session</code> 维度传入 <code>time_range</code>、<code>granularity</code>，返回 HTTP 400 / <code>invalid_parameter</code>。时间范围会按 UTC+8 对齐，详见 <a href="../usage-api.md#h-usage-time">Usage</a>。</p><p>此接口一次返回总量及全部模型、工具明细，不提供分页参数；单次模型与工具明细项合计上限为 100,000，超出返回 HTTP 400 / <code>query_limit_exceeded</code>，不返回截断结果。</p></td><td><a id="h-usage-summary-eg"></a><h2>请求示例</h2><a id="h-usage-summary-eg-workspace"></a><h3>查询当前工作空间的用量</h3><a id="code-block"></a><pre class="language-bash"><code>curl -X POST &quot;$AGENTSTUDIO_URL/usage/summary&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
  -H &quot;Content-Type: application/json&quot; \
  -d '{
    &quot;dimension&quot;: &quot;workspace&quot;,
    &quot;time_range&quot;: {
      &quot;start_time&quot;: &quot;2026-11-02T10:15:30+08:00&quot;,
      &quot;end_time&quot;: &quot;2026-11-02T14:00:01+08:00&quot;
    },
    &quot;granularity&quot;: &quot;hour&quot;
  }'
</code></pre><a id="h-usage-summary-eg-agent"></a><h3>查询指定 Agent 的指定版本</h3><a id="code-block-2"></a><pre class="language-bash"><code>curl -X POST &quot;$AGENTSTUDIO_URL/usage/summary&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
  -H &quot;Content-Type: application/json&quot; \
  -d '{
    &quot;dimension&quot;: &quot;agent&quot;,
    &quot;agent_id&quot;: &quot;agent_xxx&quot;,
    &quot;agent_version&quot;: &quot;1&quot;,
    &quot;time_range&quot;: {
      &quot;start_time&quot;: &quot;2026-11-02T10:15:30+08:00&quot;,
      &quot;end_time&quot;: &quot;2026-11-02T14:00:01+08:00&quot;
    },
    &quot;granularity&quot;: &quot;hour&quot;
  }'
</code></pre><a id="h-usage-summary-eg-session"></a><h3>查询指定 Session 的累计用量</h3><a id="code-block-3"></a><pre class="language-bash"><code>curl -X POST &quot;$AGENTSTUDIO_URL/usage/summary&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
  -H &quot;Content-Type: application/json&quot; \
  -d '{
    &quot;dimension&quot;: &quot;session&quot;,
    &quot;session_id&quot;: &quot;sesn_xxx&quot;
  }'
</code></pre></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-usage-summary-resp-fields"></a><h2>响应字段</h2><p><strong>request_id</strong> <code>string</code></p><p>请求标识，可用于问题排查</p><p><strong>data</strong> <code>object</code></p><p>用量查询结果</p><p><strong>data.query_range</strong> <code>object</code></p><p>实际统计区间。仅 <code>workspace</code>、<code>agent</code> 维度返回；<code>session</code> 维度不返回该字段</p><p><strong>data.query_range.start_time</strong> <code>string</code></p><p>对齐后的开始时间，包含该时刻，固定使用 <code>+08:00</code> 时区</p><p><strong>data.query_range.end_time</strong> <code>string</code></p><p>对齐后的结束时间，不包含该时刻，固定使用 <code>+08:00</code> 时区</p><p><strong>data.data_updated_at</strong> <code>string / null</code></p><p>本次返回用量记录中最近的已知更新时间，固定使用 <code>+08:00</code> 时区；无记录或更新时间未知时为 <code>null</code></p><p><strong>data.usage</strong> <code>object</code></p><p>总量及分组明细</p><p><strong>data.usage.total</strong> <code>object</code></p><p>查询范围内的汇总指标，详见 <a href="../usage-api.md#h-usage-total">汇总指标（total）</a></p><p><strong>data.usage.models</strong> <code>array</code></p><p>按模型名称分组的用量明细，无明细时为 <code>[]</code></p><p><strong>data.usage.tools</strong> <code>array</code></p><p>按工具来源和名称分组的用量明细，无明细时为 <code>[]</code></p><p>Session 查询返回相同的 <code>usage</code> 结构，不包含 <code>query_range</code> 或 Session 标题、状态等元数据。服务先校验 Session 归属，再查询生命周期累计用量。Session 存在但尚无统计记录时，指标 <code>value</code> 为 <code>null</code>，模型和工具明细为空数组；不会据此返回 Session 不存在。</p></td><td><a id="h-usage-summary-resp"></a><h2>响应示例</h2><p>成功时返回 HTTP 200，顶层字段为 <code>request_id</code>、<code>data</code>。以下为上述 Agent 请求的汇总示例：秒级起止时间按 <code>hour</code> 对齐为 UTC+8 10:00—15:00，数值仅用于说明响应结构。</p><a id="code-block-4"></a><pre class="language-json"><code>{
  &quot;request_id&quot;: &quot;req_summary_example&quot;,
  &quot;data&quot;: {
    &quot;query_range&quot;: {
      &quot;start_time&quot;: &quot;2026-11-02T10:00:00+08:00&quot;,
      &quot;end_time&quot;: &quot;2026-11-02T15:00:00+08:00&quot;
    },
    &quot;data_updated_at&quot;: &quot;2026-11-02T14:10:00+08:00&quot;,
    &quot;usage&quot;: {
      &quot;total&quot;: {
        &quot;input_tokens&quot;: {&quot;value&quot;: 1000, &quot;unit&quot;: &quot;tokens&quot;},
        &quot;output_tokens&quot;: {&quot;value&quot;: 200, &quot;unit&quot;: &quot;tokens&quot;},
        &quot;total_tokens&quot;: {&quot;value&quot;: 1200, &quot;unit&quot;: &quot;tokens&quot;},
        &quot;cache_read_tokens&quot;: {&quot;value&quot;: 400, &quot;unit&quot;: &quot;tokens&quot;},
        &quot;cache_creation_tokens&quot;: {&quot;value&quot;: 100, &quot;unit&quot;: &quot;tokens&quot;},
        &quot;cache_hit_ratio&quot;: {&quot;value&quot;: 0.4, &quot;unit&quot;: &quot;ratio&quot;},
        &quot;model_call_count&quot;: {&quot;value&quot;: 5, &quot;unit&quot;: &quot;count&quot;},
        &quot;tool_call_count&quot;: {&quot;value&quot;: 3, &quot;unit&quot;: &quot;count&quot;},
        &quot;builtin_tool_call_count&quot;: {&quot;value&quot;: 0, &quot;unit&quot;: &quot;count&quot;},
        &quot;mcp_tool_call_count&quot;: {&quot;value&quot;: 3, &quot;unit&quot;: &quot;count&quot;},
        &quot;custom_tool_call_count&quot;: {&quot;value&quot;: 0, &quot;unit&quot;: &quot;count&quot;},
        &quot;turns&quot;: {&quot;value&quot;: 2, &quot;unit&quot;: &quot;count&quot;},
        &quot;steps&quot;: {&quot;value&quot;: 8, &quot;unit&quot;: &quot;count&quot;},
        &quot;interrupt_error_count&quot;: {&quot;value&quot;: 0, &quot;unit&quot;: &quot;count&quot;},
        &quot;model_failed_count&quot;: {&quot;value&quot;: 1, &quot;unit&quot;: &quot;count&quot;},
        &quot;tool_failed_count&quot;: {&quot;value&quot;: 1, &quot;unit&quot;: &quot;count&quot;},
        &quot;runtime_ms&quot;: {&quot;value&quot;: 60000, &quot;unit&quot;: &quot;ms&quot;}
      },
      &quot;models&quot;: [
        {
          &quot;model_name&quot;: &quot;qwen-plus&quot;,
          &quot;usage&quot;: {
            &quot;input_tokens&quot;: {&quot;value&quot;: 1000, &quot;unit&quot;: &quot;tokens&quot;},
            &quot;output_tokens&quot;: {&quot;value&quot;: 200, &quot;unit&quot;: &quot;tokens&quot;},
            &quot;total_tokens&quot;: {&quot;value&quot;: 1200, &quot;unit&quot;: &quot;tokens&quot;},
            &quot;cache_read_tokens&quot;: {&quot;value&quot;: 400, &quot;unit&quot;: &quot;tokens&quot;},
            &quot;cache_creation_tokens&quot;: {&quot;value&quot;: 100, &quot;unit&quot;: &quot;tokens&quot;},
            &quot;cache_hit_ratio&quot;: {&quot;value&quot;: 0.4, &quot;unit&quot;: &quot;ratio&quot;},
            &quot;call_count&quot;: {&quot;value&quot;: 5, &quot;unit&quot;: &quot;count&quot;},
            &quot;failed_count&quot;: {&quot;value&quot;: 1, &quot;unit&quot;: &quot;count&quot;}
          }
        }
      ],
      &quot;tools&quot;: [
        {
          &quot;source&quot;: &quot;mcp&quot;,
          &quot;tool_name&quot;: &quot;web_search&quot;,
          &quot;usage&quot;: {
            &quot;call_count&quot;: {&quot;value&quot;: 3, &quot;unit&quot;: &quot;count&quot;},
            &quot;failed_count&quot;: {&quot;value&quot;: 1, &quot;unit&quot;: &quot;count&quot;}
          }
        }
      ]
    }
  }
}
</code></pre></td></tr></tbody></table>
