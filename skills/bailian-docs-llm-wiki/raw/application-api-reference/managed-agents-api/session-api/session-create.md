# 创建 Session

创建一个会话实例：绑定智能体与运行环境。会话创建时拍摄智能体当时最新版本的完整快照，支持会话级智能体配置覆盖与 MCP 请求头。

<a id="前提"></a>

<a id="h-sc-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。创建会话前需先有智能体和运行环境，分别详见[Agent](../agent-api.md)与[Environment](../environment-api.md)。挂载百炼记忆库时，需已开通百炼记忆服务。

<a id="接口"></a>

<a id="h-sc-endpoint"></a>

## 接口

**POST** `/sessions`

<table><tbody><tr><td><a id="h-sc-req"></a><h2>请求体</h2><p><strong>agent</strong> <code>object</code> <strong>（必选）</strong></p><p>绑定的智能体引用对象，只传 <code>id</code> 即引用；可锁定版本，并按需建立会话级覆盖，见<a href="#h-sc-override">会话级配置覆盖</a></p><p><strong>environment_id</strong> <code>string</code> <strong>（必选）</strong></p><p>绑定的运行环境 ID。环境配置预装包时创建后可能需要预热，准备中的环境不可被会话绑定（返回 invalid_parameter），需等待预热完成</p><p><strong>sandbox</strong> <code>object</code> <strong>（可选）</strong></p><p>沙箱快照持久化配置。省略时保持原有会话创建行为</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>enable_snapshot</strong> <code>boolean</code> <strong>（必选）</strong></p><p>是否为当前 Session 开启沙箱快照持久化。传入 <code>sandbox</code> 时必填</p><p><strong>snapshot_persistent_seconds</strong> <code>integer</code> <strong>（条件必填）</strong></p><p>单份快照的保留时间，单位秒，取值 86400～2592000（1～30 天）。<code>enable_snapshot=true</code> 时必填</p></div></section><p><strong>title</strong> <code>string</code> <strong>（可选）</strong></p><p>会话标题，便于在列表中辨识</p><p><strong>resources</strong> <code>array</code> <strong>（可选）</strong></p><p>创建时挂载的资源列表。</p><a id="accordion-文件项"></a><section><p>文件项</p><div><ul><li><code>type</code>：固定为 <code>file</code></li><li><code>file_id</code>：已上传的文件 ID</li><li><code>mount_path</code>：挂载路径，必须以 <code>/uploads/</code> 开头，实际路径会加上 <code>/mnt/session</code> 前缀</li></ul></div></section><a id="accordion-记忆项"></a><section><p>记忆项</p><div><ul><li><code>type</code>：固定为 <code>memory_store</code></li><li><code>provider</code>：<code>default</code> / <code>agentstudio_memory</code>，省略时为 <code>default</code></li><li><code>memory_store_id</code>：必填</li><li><code>entity_id</code>：百炼记忆必填</li><li><code>access</code>：<code>read_only</code> / <code>read_write</code>，默认 <code>read_write</code></li><li><code>description</code>：百炼记忆的挂载用途描述</li><li><code>project_ids</code>：百炼事实和技能记忆规则 ID，每条挂载合计最多 5 个</li><li><code>profile_schema</code>：百炼画像模板 ID，最多一个</li><li><code>instructions</code>：内置记忆的挂载说明，最长 4096 字符</li></ul></div></section><p>内置记忆的挂载路径由服务端生成；百炼记忆无挂载路径。详见<a href="../../../application-user-guide/agent-development/managed-agents/managed-agents-context/managed-agents-memory-store.md">记忆库</a></p><p><strong>vault_ids</strong> <code>array of string</code> <strong>（可选）</strong></p><p>Vault ID 列表。将指定 Vault 中的 Credential 注入会话运行环境，使智能体可访问对应密钥</p><p><strong>metadata</strong> <code>object</code> <strong>（可选）</strong></p><p>业务自定义键值，不影响模型行为</p><p><strong>environment_variables</strong> <code>object</code> <strong>（可选）</strong></p><p>会话运行时注入的环境变量，字符串键值对，沙箱代码中可直接按名读取</p><p><strong>mcp_configs</strong> <code>array</code> <strong>（可选）</strong></p><p>会话级 MCP 请求头，独立于 <code>agent</code>，见<a href="#h-sc-mcp">会话级 MCP 请求头</a>。省略时为空数组</p><ul><li><code>provider</code>：只接受 <code>default</code> 或 <code>agentstudio_memory</code>，显式传 <code>null</code>、空串或其他值会返回参数错误。</li><li><code>entity_id</code>：仅用于百炼记忆，是挂载绑定的实体 ID，不是云账号 UID，也不是 Session 顶层字段。</li><li><code>project_ids</code>：省略或为空数组时使用百炼默认记忆规则。</li><li><code>profile_schema</code>：省略时不启用画像能力，且不计入 5 条规则。</li><li>内置记忆：沿用 <code>memory_store_id</code>、<code>access</code> 和 <code>instructions</code> 字段。</li></ul><div><div><p><strong>说明</strong>同一会话绑定多个 Vault 时，不同 Vault 之间的 <code>secret_name</code> 不能重复，也不要使用前缀相同的名称（例如 <code>API_KEY</code> 与 <code>API_KEY_V2</code>），否则创建会话返回 400 <code>invalid_parameter</code>（Invalid request）。</p></div></div></td><td><a id="h-sc-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl -X POST &quot;$AGENTSTUDIO_URL/sessions&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
  -H &quot;Content-Type: application/json&quot; \
  -d '{
    &quot;agent&quot;: {&quot;type&quot;: &quot;agent&quot;, &quot;id&quot;: &quot;agent_xxx&quot;},
    &quot;environment_id&quot;: &quot;env_xxx&quot;,
    &quot;title&quot;: &quot;Q3 销售数据分析&quot;,
    &quot;resources&quot;: [
      {&quot;type&quot;: &quot;file&quot;, &quot;file_id&quot;: &quot;file_xxx&quot;, &quot;mount_path&quot;: &quot;/uploads/workspace/data.csv&quot;}
    ],
    &quot;vault_ids&quot;: [&quot;vlt_xxx&quot;],
    &quot;metadata&quot;: {&quot;biz_ticket_id&quot;: &quot;1234&quot;},
    &quot;environment_variables&quot;: {&quot;API_BASE_URL&quot;: &quot;https://api.example.com&quot;, &quot;LOG_LEVEL&quot;: &quot;info&quot;}
  }'
</code></pre></div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>session = client.sessions.create(
    agent={&quot;type&quot;: &quot;agent&quot;, &quot;id&quot;: &quot;agent_xxx&quot;},
    environment_id=&quot;env_xxx&quot;,
    title=&quot;Q3 销售数据分析&quot;,
    resources=[
        {&quot;type&quot;: &quot;file&quot;, &quot;file_id&quot;: &quot;file_xxx&quot;, &quot;mount_path&quot;: &quot;/uploads/workspace/data.csv&quot;},
    ],
    vault_ids=[&quot;vlt_xxx&quot;],
    metadata={&quot;biz_ticket_id&quot;: &quot;1234&quot;},
    environment_variables={&quot;API_BASE_URL&quot;: &quot;https://api.example.com&quot;, &quot;LOG_LEVEL&quot;: &quot;info&quot;},
)
print(session.id, session.status)
</code></pre></div><a id="fig-code-group-java-tab"></a>Java<div><a id="code-code-group-java"></a><pre class="language-java"><code>Map&lt;String, String&gt; metadata = new HashMap&lt;&gt;();
metadata.put(&quot;biz_ticket_id&quot;, &quot;1234&quot;);

Map&lt;String, String&gt; environmentVariables = new HashMap&lt;&gt;();
environmentVariables.put(&quot;API_BASE_URL&quot;, &quot;https://api.example.com&quot;);
environmentVariables.put(&quot;LOG_LEVEL&quot;, &quot;info&quot;);

Session session = client.sessions().create(SessionCreateParam.builder()
    .agent(SessionAgent.ofOverride(Map.of(&quot;type&quot;, &quot;agent&quot;, &quot;id&quot;, &quot;agent_xxx&quot;)))
    .environmentId(&quot;env_xxx&quot;)
    .title(&quot;Q3 销售数据分析&quot;)
    .resources(List.of(SessionResource.builder()
        .type(&quot;file&quot;)
        .fileId(&quot;file_xxx&quot;)
        .mountPath(&quot;/uploads/workspace/data.csv&quot;)
        .build()))
    .vaultIds(List.of(&quot;vlt_xxx&quot;))
    .metadata(metadata)
    .environmentVariables(environmentVariables)
    .build());
System.out.println(session.getId() + &quot; &quot; + session.getStatus());
</code></pre></div></div><a id="h-sc-memory-bailian"></a><h3>百炼记忆挂载示例</h3><p>挂载百炼记忆库时，将 <code>provider</code> 设为 <code>agentstudio_memory</code>，并填写 <code>entity_id</code>：</p><a id="code-block"></a><pre class="language-json"><code>{
  &quot;agent&quot;: {
    &quot;type&quot;: &quot;agent&quot;,
    &quot;id&quot;: &quot;agent_xxx&quot;
  },
  &quot;environment_id&quot;: &quot;env_xxx&quot;,
  &quot;resources&quot;: [
    {
      &quot;type&quot;: &quot;memory_store&quot;,
      &quot;provider&quot;: &quot;agentstudio_memory&quot;,
      &quot;memory_store_id&quot;: &quot;0123456789abcdef0123456789abcdef&quot;,
      &quot;entity_id&quot;: &quot;customer_001&quot;,
      &quot;access&quot;: &quot;read_write&quot;,
      &quot;description&quot;: &quot;保存客户确认的业务约定、可复用经验和沟通偏好&quot;,
      &quot;project_ids&quot;: [&quot;fact_rule_demo&quot;, &quot;skill_rule_demo&quot;],
      &quot;profile_schema&quot;: &quot;profile_schema_demo&quot;
    }
  ]
}
</code></pre><p><code>memory_store_id</code> 是百炼记忆库 ID，不要求 <code>memstore_</code> 前缀。规则与画像模板的默认行为详见<a href="../../../application-user-guide/agent-development/managed-agents/managed-agents-context/managed-agents-memory-store.md#h-ms-bailian">记忆库</a>。</p><p>需要开启沙箱持久化时，在请求体中增加 <code>sandbox</code> 字段，例如：</p><a id="code-block-2"></a><pre class="language-json"><code>{
  &quot;sandbox&quot;: {
    &quot;enable_snapshot&quot;: true,
    &quot;snapshot_persistent_seconds&quot;: 172800
  }
}
</code></pre><p>省略该字段时默认不开启。保留期内的恢复规则与到期行为见<a href="../../../application-user-guide/agent-development/managed-agents/managed-agents-session/managed-agents-session-operations.md#h-sandbox-persistence">沙箱持久化</a>。</p></td></tr></tbody></table>

<a id="会话级配置覆盖"></a>

<a id="h-sc-override"></a>

## 会话级配置覆盖

`agent` 对象可仅引用智能体，也可附带覆盖字段建立会话级覆盖：覆盖只修改本会话的配置快照，不改动智能体本身，多个会话可基于同一智能体各自定制。对象字段如下：

| 字段 | 必填 | 类型 | 说明 |
| --- | --- | --- | --- |
| `type` | 否 | string | `agent`（仅引用）或 `agent_with_overrides`（引用并覆盖）。携带覆盖字段时必须显式传 `agent_with_overrides`，否则返回 invalid\_parameter |
| `id` | 是 | string | 智能体 ID |
| `version` | 否 | integer | 锁定的智能体版本号，省略时使用当前最新版本；版本不存在时返回 not\_found |
| `system` | 否 | string / null | 覆盖系统提示词。省略时继承智能体源配置；空字符串明确使用空提示词 |
| `tools` | 否 | array / null | 覆盖工具包配置，结构与[创建 Agent](../agent-api/agent-create.md)的 `tools` 一致 |
| `mcp_servers` | 否 | array / null | 覆盖挂载的 MCP Server 列表，结构与创建 Agent 的 `mcp_servers` 一致 |
| `skills` | 否 | array / null | 覆盖挂载的技能列表，结构与创建 Agent 的 `skills` 一致 |

覆盖字段的取值语义（createSession 与[更新 Session](session-update.md)一致）：

| 取值 | 效果 |
| --- | --- |
| 省略 | 继承智能体源配置 |
| `null` | 不建立覆盖，继承源配置 |
| `[]`（数组字段） | 明确覆盖为空 |
| `""`（仅 `system`） | 明确使用空提示词 |

<a id="会话级-mcp-请求头"></a>

<a id="h-sc-mcp"></a>

## 会话级 MCP 请求头

`mcp_configs` 为指定 MCP Server 的全部请求注入自定义 Header，常用于透传租户 ID、鉴权 token。每项含 `mcp_server_name`（MCP Server 名称）与 `headers`（键值对，key 与 value 均为字符串）。传入不存在的 MCP Server 名称不报错，该配置不生效。按会话动态传值的接入方法与示例见[自定义 MCP 与 Skills](../../../_short/managed-agents-custom-mcp-skills-bb2b03130058d257.md#h-cm-dynamic-header)。

创建会话的完整请求示例：

<a id="fig-code-group-2"></a>

<a id="fig-code-group-2-curl-tab"></a>

curl

<a id="code-code-group-2-curl"></a>

```bash
curl -X POST "$AGENTSTUDIO_URL/sessions" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "agent": {
      "type": "agent_with_overrides",
      "id": "agent_xxx",
      "system": "你是本会话专用的数据核对助手，只输出核对结论。"
    },
    "environment_id": "env_xxx",
    "mcp_configs": [
      {"mcp_server_name": "crm", "headers": {"X-Tenant-Id": "tenant-demo"}}
    ]
  }'
```

<a id="fig-code-group-2-python-tab"></a>

Python

<a id="code-code-group-2-python"></a>

```python
session = client.sessions.create(
    agent={"type": "agent_with_overrides", "id": "agent_xxx",
           "system": "你是本会话专用的数据核对助手，只输出核对结论。"},
    environment_id="env_xxx",
    mcp_configs=[{"mcp_server_name": "crm", "headers": {"X-Tenant-Id": "tenant-demo"}}],
)
```

<a id="fig-code-group-2-java-tab"></a>

Java

<a id="code-code-group-2-java"></a>

```java
Map<String, Object> agentOverride = Map.of(
    "type", "agent_with_overrides",
    "id", "agent_xxx",
    "system", "你是本会话专用的数据核对助手，只输出核对结论。");
Map<String, String> headers = Map.of("X-Tenant-Id", "tenant-demo");

Session session = client.sessions().create(SessionCreateParam.builder()
    .agent(agentOverride)
    .environmentId("env_xxx")
    .mcpConfigs(List.of(Map.of(
        "mcp_server_name", "crm",
        "headers", headers)))
    .build());
```

<table><tbody><tr><td><a id="h-sc-dto"></a><h3>响应字段</h3><p>响应为 Session 对象。字段如下：</p><p><strong>id</strong> <code>string</code></p><p>会话 ID，格式 <code>sesn_&amp;lt;ULID&amp;gt;</code></p><p><strong>type</strong> <code>string</code></p><p>固定为 <code>session</code></p><p><strong>status</strong> <code>string</code></p><p>会话状态：<code>idle</code> / <code>running</code> / <code>terminated</code>。新建会话为 <code>idle</code></p><p><strong>agent</strong> <code>object</code></p><p>智能体配置完整快照，含 <code>id</code> / <code>version</code> / <code>name</code> / <code>model</code> / <code>system</code> / <code>tools</code> 等；会话级覆盖已并入快照</p><p><strong>environment_id</strong> <code>string</code></p><p>绑定的运行环境 ID</p><p><strong>resources</strong> <code>array</code></p><p>挂载的资源列表。</p><a id="accordion-文件项-2"></a><section><p>文件项</p><div><ul><li><code>id</code>：资源 ID</li><li><code>type</code>：资源类型</li><li><code>file_id</code>：内部副本 ID</li><li><code>mount_path</code>：含前缀的完整路径</li></ul></div></section><a id="accordion-记忆项-2"></a><section><p>记忆项</p><div><ul><li><code>id</code>：服务端生成的挂载 ID，与 <code>memory_store_id</code> 不同，创建时不传</li><li><code>type</code>：资源类型</li><li><code>provider</code>：记忆提供方</li><li><code>memory_store_id</code>：记忆库 ID</li><li><code>name</code>：可选，可能为空</li><li><code>access</code>：访问权限</li></ul></div></section><a id="accordion-百炼记忆项"></a><section><p>百炼记忆项</p><div><ul><li><code>entity_id</code>：百炼记忆实体 ID</li><li><code>project_ids</code>：百炼事实和技能记忆规则 ID</li><li><code>profile_schema</code>：百炼画像模板 ID</li><li><code>description</code>：创建时保存的挂载描述，未填时可为空</li><li>不返回 <code>mount_path</code></li></ul></div></section><a id="accordion-内置记忆项"></a><section><p>内置记忆项</p><div><ul><li><code>file_id</code>：固定为 <code>null</code></li><li><code>description</code>：记忆库元数据</li><li><code>instructions</code>：挂载说明</li><li><code>mount_path</code>：服务端生成，如 <code>/mnt/memory/&lt;名称&gt;</code></li></ul></div></section><p><strong>title / metadata</strong> <code>string / object</code></p><p>同请求体</p><p><strong>sandbox</strong> <code>object</code></p><p>沙箱快照持久化配置；未配置时省略</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>enable_snapshot</strong> <code>boolean</code></p><p>当前 Session 是否开启快照持久化</p><p><strong>snapshot_persistent_seconds</strong> <code>integer</code></p><p>单份快照配置的保留时间，单位秒；未配置时不返回</p></div></section><p><strong>archived_at</strong> <code>string / null</code></p><p>归档时间，未归档时为 <code>null</code></p><p><strong>created_at / updated_at</strong> <code>string</code></p><p>创建 / 最近更新时间，ISO 8601</p><p><strong>request_id</strong> <code>string</code></p><p>本次请求的唯一标识</p><p><strong>environment_variables</strong> <code>object</code></p><p>会话运行时注入的环境变量，字符串键值对，沙箱代码中可直接按名读取</p><p>百炼记忆挂载只返回创建时选择的规则和画像模板 ID，不补入默认规则或模板；不返回记忆正文、画像值或完整规则定义。</p><p>本响应不含 <code>mcp_configs</code>；通过<a href="session-get.md">获取 Session</a>查询。</p></td><td><a id="h-sc-resp"></a><h2>响应示例</h2><p>会话详情嵌入完整的智能体快照。</p><a id="code-block-3"></a><pre class="language-json"><code>{
  &quot;id&quot;: &quot;sesn_xxx&quot;,
  &quot;type&quot;: &quot;session&quot;,
  &quot;status&quot;: &quot;idle&quot;,
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
  &quot;resources&quot;: [
    {
      &quot;id&quot;: &quot;sesrsc_xxx&quot;,
      &quot;type&quot;: &quot;file&quot;,
      &quot;file_id&quot;: &quot;file_xxx&quot;,
      &quot;mount_path&quot;: &quot;/mnt/session/uploads/workspace/data.csv&quot;,
      &quot;created_at&quot;: &quot;2026-05-28T08:23:11Z&quot;,
      &quot;updated_at&quot;: &quot;2026-05-28T08:23:11Z&quot;
    }
  ],
  &quot;metadata&quot;: {&quot;biz_ticket_id&quot;: &quot;1234&quot;},
  &quot;archived_at&quot;: null,
  &quot;created_at&quot;: &quot;2026-05-28T08:23:11Z&quot;,
  &quot;updated_at&quot;: &quot;2026-05-28T08:23:11Z&quot;,
  &quot;request_id&quot;: &quot;xxx&quot;,
  &quot;environment_variables&quot;: {&quot;API_BASE_URL&quot;: &quot;https://api.example.com&quot;, &quot;LOG_LEVEL&quot;: &quot;info&quot;}
}
</code></pre></td></tr></tbody></table>

<a id="沙箱配置响应示例"></a>

### 沙箱配置响应示例

创建成功且开启沙箱持久化时，`sandbox` 只返回配置：

<a id="code-block-4"></a>

```json
{
  "sandbox": {
    "enable_snapshot": true,
    "snapshot_persistent_seconds": 172800
  }
}
```

当前快照状态和统计字段通过[获取 Session](session-get.md)查询。

<a id="配置锁定"></a>

<a id="h-sc-lock"></a>

## 配置锁定

会话创建时拍摄智能体当时最新版本的完整快照（嵌入到会话详情的 `agent` 字段）。后续编辑智能体只影响新建会话，已有会话继续使用快照中的配置。会话级配置目前仅支持通过 API 设置，控制台创建的会话为只读快照。会话创建后可继续修改会话级配置，见[更新 Session](session-update.md)。
