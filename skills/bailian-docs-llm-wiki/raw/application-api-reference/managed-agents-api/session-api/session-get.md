# 获取 Session

返回会话元数据、嵌入的智能体快照与资源列表。事件历史与消息内容通过事件 API 获取。

<a id="前提"></a>

<a id="h-sg-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。

<a id="接口"></a>

<a id="h-sg-endpoint"></a>

## 接口

**GET** `/sessions/{session_id}`

<a id="请求示例"></a>

<a id="h-sg-eg"></a>

## 请求示例

<a id="fig-code-group"></a>

<a id="fig-code-group-curl-tab"></a>

curl

<a id="code-code-group-curl"></a>

```bash
curl "$AGENTSTUDIO_URL/sessions/sesn_xxx" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

<a id="fig-code-group-python-tab"></a>

Python

<a id="code-code-group-python"></a>

```python
session = client.sessions.retrieve("sesn_xxx")
print(session.id, session.status, session.title)
```

<a id="fig-code-group-java-tab"></a>

Java

<a id="code-code-group-java"></a>

```java
Session session = client.sessions().retrieve("sesn_xxx");
System.out.println(session.getId() + " " + session.getStatus() + " " + session.getTitle());
```

<table><tbody><tr><td><a id="h-sg-dto"></a><h3>响应字段</h3><p>响应为 Session 对象。字段如下：</p><p><strong>id</strong> <code>string</code></p><p>会话 ID，格式 <code>sesn_&amp;lt;ULID&amp;gt;</code></p><p><strong>type</strong> <code>string</code></p><p>固定为 <code>session</code></p><p><strong>status</strong> <code>string</code></p><p>会话状态：<code>idle</code> / <code>running</code> / <code>terminated</code></p><p><strong>stop_reason</strong> <code>object / null</code></p><p>会话回到 <code>idle</code> 的原因，判别联合。<code>null</code>（<code>running</code>，或 <code>idle</code> 刚创建尚未产生结束原因）/ <code>{&quot;type&quot;:&quot;end_turn&quot;}</code>（模型主动结束）/ <code>{&quot;type&quot;:&quot;retries_exhausted&quot;}</code>（重试耗尽）/ <code>{&quot;type&quot;:&quot;requires_action&quot;,&quot;pending_batch_id&quot;:&quot;...&quot;,&quot;pending_call_ids&quot;:[...]}</code>（等待工具审批，<code>pending_call_ids</code> 为待裁决调用列表）。仅在 <code>status=idle</code> 时用于判断交互状态；<code>running</code> 时为 <code>null</code>；<code>terminated</code> 是终态，客户端不应依赖其 <code>stop_reason</code></p><p><strong>agent</strong> <code>object</code></p><p>智能体配置完整快照，含 <code>id</code> / <code>version</code> / <code>name</code> / <code>model</code> / <code>system</code> / <code>tools</code> 等；会话级覆盖（若已设置）已并入快照</p><p><strong>environment_id</strong> <code>string</code></p><p>绑定的运行环境 ID</p><p><strong>sandbox</strong> <code>object</code></p><p>沙箱快照持久化配置与当前快照状态；未配置时省略</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>enable_snapshot</strong> <code>boolean</code></p><p>当前 Session 是否开启快照持久化</p><p><strong>snapshot_persistent_seconds</strong> <code>integer</code></p><p>单份快照配置的保留时间，单位秒；未配置时不返回</p><p><strong>is_persisting</strong> <code>boolean</code></p><p>当前 Session 是否正在保留可用快照；尚未取得统计时可能不返回</p><p><strong>predict_release_time</strong> <code>string / null</code></p><p>当前快照预计释放时间，ISO 8601 UTC；没有当前快照时为 <code>null</code></p></div></section><p><strong>usage.sandbox</strong> <code>object</code></p><p>沙箱快照时长统计。创建响应中可能省略；已开启快照但尚未生成快照时，内部时长字段为 <code>null</code>。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>session_total_persisted_hours</strong> <code>integer / null</code></p><p>历史快照累计保留小时数；尚无统计时为 <code>null</code></p><p><strong>latest_snapshot_persisted_hours</strong> <code>integer / null</code></p><p>当前最新快照已保留小时数；没有当前快照时为 <code>null</code></p></div></section><p><strong>title / metadata</strong> <code>string / object</code></p><p>会话标题与业务自定义元数据</p><p><strong>archived_at</strong> <code>string / null</code></p><p>归档时间，未归档时为 <code>null</code></p><p><strong>created_at / updated_at</strong> <code>string</code></p><p>创建 / 最近更新时间，ISO 8601</p><p><strong>request_id</strong> <code>string</code></p><p>本次请求的唯一标识</p><p><strong>environment_variables</strong> <code>object</code></p><p>会话运行时注入的环境变量，字符串键值对，沙箱代码中可直接按名读取</p><p><strong>vault_ids</strong> <code>array of string</code></p><p>绑定的 Vault ID 列表</p><p><strong>mcp_configs</strong> <code>array of object</code></p><p>会话级 MCP 请求头，每项含 <code>mcp_server_name</code> 与 <code>headers</code>；未配置时为空数组</p></td><td><a id="h-sg-resp"></a><h2>响应示例</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;id&quot;: &quot;sesn_xxx&quot;,
  &quot;type&quot;: &quot;session&quot;,
  &quot;status&quot;: &quot;idle&quot;,
  &quot;stop_reason&quot;: {
    &quot;type&quot;: &quot;requires_action&quot;,
    &quot;pending_batch_id&quot;: &quot;response_xxx:9f2c...&quot;,
    &quot;pending_call_ids&quot;: [
      &quot;call_xxx&quot;
    ]
  },
  &quot;agent&quot;: {
    &quot;id&quot;: &quot;agent_xxx&quot;,
    &quot;type&quot;: &quot;agent&quot;,
    &quot;version&quot;: 1,
    &quot;name&quot;: &quot;data-analyst&quot;,
    &quot;description&quot;: null,
    &quot;model&quot;: {&quot;id&quot;: &quot;qwen3.7-max&quot;},
    &quot;system&quot;: &quot;你是数据分析专家，使用 pandas 处理 CSV 文件。&quot;,
    &quot;tools&quot;: []
  },
  &quot;environment_id&quot;: &quot;env_xxx&quot;,
  &quot;title&quot;: &quot;Q3 销售数据分析&quot;,
  &quot;metadata&quot;: {&quot;biz_ticket_id&quot;: &quot;1234&quot;},
  &quot;archived_at&quot;: null,
  &quot;created_at&quot;: &quot;2026-05-28T08:23:11Z&quot;,
  &quot;updated_at&quot;: &quot;2026-05-28T08:23:25Z&quot;,
  &quot;request_id&quot;: &quot;xxx&quot;,
  &quot;environment_variables&quot;: {&quot;API_BASE_URL&quot;: &quot;https://api.example.com&quot;, &quot;LOG_LEVEL&quot;: &quot;info&quot;},
  &quot;vault_ids&quot;: [&quot;vlt_xxx&quot;],
  &quot;mcp_configs&quot;: [{&quot;mcp_server_name&quot;: &quot;crm&quot;, &quot;headers&quot;: {&quot;X-Tenant-Id&quot;: &quot;tenant-demo&quot;}}]
}
</code></pre></td></tr></tbody></table>

<a id="沙箱快照响应示例"></a>

### 沙箱快照响应示例

当前存在可用快照时：

<a id="code-block-2"></a>

```json
{
  "sandbox": {
    "enable_snapshot": true,
    "snapshot_persistent_seconds": 172800,
    "is_persisting": true,
    "predict_release_time": "2026-11-17T06:09:50Z"
  },
  "usage": {
    "sandbox": {
      "session_total_persisted_hours": 3,
      "latest_snapshot_persisted_hours": 1
    }
  }
}
```

已开启快照但尚未生成快照时：

<a id="code-block-3"></a>

```json
{
  "sandbox": {
    "enable_snapshot": true,
    "snapshot_persistent_seconds": 172800,
    "is_persisting": false,
    "predict_release_time": null
  },
  "usage": {
    "sandbox": {
      "session_total_persisted_hours": null,
      "latest_snapshot_persisted_hours": null
    }
  }
}
```
