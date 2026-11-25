# 更新 Session

修改会话的 title、metadata、environment\_variables、vault\_ids、会话级智能体配置与会话级 MCP 请求头。会话更新是唯一会触发 session.updated 事件的操作。

<a id="前提"></a>

<a id="h-su-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。

<a id="接口"></a>

<a id="h-su-endpoint"></a>

## 接口

**POST** `/sessions/{session_id}`

支持修改 `title`、`metadata`、`environment_variables`、`vault_ids`、会话级智能体配置（`agent`）与会话级 MCP 请求头（`mcp_configs`）。数组与对象字段整体替换，空值清空。**会话更新是唯一会触发**`session.updated`**事件的操作**。

<a id="请求体"></a>

<a id="h-su-req"></a>

## 请求体

**title** `string` **（可选）**

会话标题。省略保持原值，`null` 不执行更新

**metadata** `object` **（可选）**

业务自定义键值。整体替换；省略保持原值，`null` 不执行更新

**environment\_variables** `object` **（可选）**

会话运行时注入的环境变量，字符串键值对，沙箱代码中可直接按名读取。整体替换；空对象清空，省略保持原值

**vault\_ids** `array of string` **（可选）**

整体替换 Vault 绑定；空数组清空，省略保持原值

**agent** `object` **（可选）**

会话级智能体配置 patch，只能携带 `system` / `tools` / `mcp_servers` / `skills` 覆盖字段，携带其他字段（如 `type` / `id` / `version` / `model`）返回 invalid\_parameter。见[会话级配置 patch](#h-su-agent)

**mcp\_configs** `array` **（可选）**

整体替换会话级 MCP 请求头，结构与[创建 Session](session-create.md)一致；空数组清空，省略保持原值，`null` 非法

<a id="会话级配置-patch"></a>

<a id="h-su-agent"></a>

## 会话级配置 patch

`agent` patch 只修改本会话的配置快照，不生成智能体新版本。子字段取值语义（与创建 Session 的覆盖语义一致）：

| 取值 | 效果 |
| --- | --- |
| 省略 | 保留已有覆盖 |
| `null` | 删除该字段覆盖，重新继承智能体源配置 |
| `[]`（数组字段） | 明确覆盖为空 |
| `""`（仅 `system`） | 明确使用空提示词 |

<a id="请求示例"></a>

<a id="h-su-eg"></a>

## 请求示例

<a id="fig-code-group"></a>

<a id="fig-code-group-curl-tab"></a>

curl

<a id="code-code-group-curl"></a>

```bash
curl -X POST "$AGENTSTUDIO_URL/sessions/sesn_xxx" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Q3 销售复盘",
    "metadata": {"biz_ticket_id": "1234", "status": "done"},
    "environment_variables": {"API_BASE_URL": "https://api.example.com", "LOG_LEVEL": "info"},
    "agent": {
      "system": "你是本会话专用的项目分析助手。",
      "skills": []
    },
    "mcp_configs": [
      {"mcp_server_name": "crm", "headers": {"X-Tenant-Id": "tenant-demo"}}
    ]
  }'
```

<a id="fig-code-group-python-tab"></a>

Python

<a id="code-code-group-python"></a>

```python
session = client.sessions.update(
    "sesn_xxx",
    title="Q3 销售复盘",
    metadata={"biz_ticket_id": "1234", "status": "done"},
    environment_variables={"API_BASE_URL": "https://api.example.com", "LOG_LEVEL": "info"},
    agent={"system": "你是本会话专用的项目分析助手。", "skills": []},
    mcp_configs=[{"mcp_server_name": "crm", "headers": {"X-Tenant-Id": "tenant-demo"}}],
)
```

<a id="fig-code-group-java-tab"></a>

Java

<a id="code-code-group-java"></a>

```java
Map<String, String> metadata = new HashMap<>();
metadata.put("biz_ticket_id", "1234");
metadata.put("status", "done");

Map<String, String> environmentVariables = new HashMap<>();
environmentVariables.put("API_BASE_URL", "https://api.example.com");
environmentVariables.put("LOG_LEVEL", "info");

Map<String, Object> agentPatch = Map.of(
    "system", "你是本会话专用的项目分析助手。",
    "skills", List.of());
Map<String, String> headers = Map.of("X-Tenant-Id", "tenant-demo");

Session updated = client.sessions().update("sesn_xxx",
    SessionUpdateParam.builder()
        .title("Q3 销售复盘")
        .metadata(metadata)
        .environmentVariables(environmentVariables)
        .agent(agentPatch)
        .mcpConfigs(List.of(Map.of(
            "mcp_server_name", "crm",
            "headers", headers)))
        .build());
```

<table><tbody><tr><td><a id="h-su-dto"></a><h3>响应字段</h3><strong>id</strong><code>string</code><p>会话 ID</p><strong>type</strong><code>string</code><p>固定为 <code>session</code></p><strong>status</strong><code>string</code><p>当前会话状态（更新不改变状态）</p><strong>title / metadata</strong><code>string / object</code><p>请求体覆盖后的新值</p><strong>updated_at</strong><code>string</code><p>最近更新时间，ISO 8601</p><strong>request_id</strong><code>string</code><p>本次请求的唯一标识</p><strong>environment_variables</strong><code>object</code><p>会话运行时注入的环境变量，字符串键值对，沙箱代码中可直接按名读取</p><strong>agent</strong><code>object</code><p>更新后的智能体配置快照，会话级覆盖已并入。字段同<a href="session-get.md">获取 Session</a></p><strong>vault_ids</strong><code>array of string</code><p>更新后的 Vault 绑定</p><strong>mcp_configs</strong><code>array of object</code><p>更新后的会话级 MCP 请求头，每项含 <code>mcp_server_name</code> 与 <code>headers</code></p></td><td><a id="h-su-resp"></a><h2>响应示例</h2><p>返回更新后的会话详情：<code>title</code> / <code>metadata</code> 等覆盖后的新值、<code>agent</code>（覆盖已并入的完整快照）、<code>mcp_configs</code>、<code>vault_ids</code>、<code>updated_at</code> 与 <code>request_id</code>。</p><a id="code-block"></a><pre class="language-json"><code>{
  &quot;id&quot;: &quot;sesn_xxx&quot;,
  &quot;type&quot;: &quot;session&quot;,
  &quot;status&quot;: &quot;idle&quot;,
  &quot;title&quot;: &quot;Q3 销售复盘&quot;,
  &quot;metadata&quot;: {&quot;biz_ticket_id&quot;: &quot;1234&quot;, &quot;status&quot;: &quot;done&quot;},
  &quot;updated_at&quot;: &quot;2026-05-28T09:30:00Z&quot;,
  &quot;request_id&quot;: &quot;xxx&quot;,
  &quot;environment_variables&quot;: {&quot;API_BASE_URL&quot;: &quot;https://api.example.com&quot;, &quot;LOG_LEVEL&quot;: &quot;info&quot;},
  &quot;agent&quot;: {
    &quot;id&quot;: &quot;agent_xxx&quot;,
    &quot;type&quot;: &quot;agent&quot;,
    &quot;version&quot;: 1,
    &quot;name&quot;: &quot;data-analyst&quot;,
    &quot;system&quot;: &quot;你是本会话专用的项目分析助手。&quot;,
    &quot;tools&quot;: [],
    &quot;mcp_servers&quot;: [],
    &quot;skills&quot;: []
  },
  &quot;vault_ids&quot;: [&quot;vlt_xxx&quot;],
  &quot;mcp_configs&quot;: [{&quot;mcp_server_name&quot;: &quot;crm&quot;, &quot;headers&quot;: {&quot;X-Tenant-Id&quot;: &quot;tenant-demo&quot;}}]
}
</code></pre></td></tr></tbody></table>
