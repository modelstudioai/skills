# 获取 Session

返回会话元数据、嵌入的智能体快照与资源列表。事件历史与消息内容通过事件 API 获取。

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。

## 接口

**GET** `/sessions/{session_id}`

## 请求示例

curl

```
curl "$AGENTSTUDIO_URL/sessions/sesn_xxx" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

Python

```
session = client.sessions.retrieve("sesn_xxx")
print(session.id, session.status, session.title)
```

Java

```
Session session = client.sessions().retrieve("sesn_xxx");
System.out.println(session.getId() + " " + session.getStatus() + " " + session.getTitle());
```

### 响应字段

响应为 Session 对象。字段如下：

**id** `string`

会话 ID，格式 `sesn_&lt;ULID&gt;`

**type** `string`

固定为 `session`

**status** `string`

会话状态：`idle` / `running` / `terminated`

**stop\_reason** `object / null`

会话回到 `idle` 的原因，判别联合。`null`（`running`，或 `idle` 刚创建尚未产生结束原因）/ `{"type":"end_turn"}`（模型主动结束）/ `{"type":"retries_exhausted"}`（重试耗尽）/ `{"type":"requires_action","pending_batch_id":"...","pending_call_ids":[...]}`（等待工具审批，`pending_call_ids` 为待裁决调用列表）。仅在 `status=idle` 时用于判断交互状态；`running` 时为 `null`；`terminated` 是终态，客户端不应依赖其 `stop_reason`

**agent** `object`

智能体配置完整快照，含 `id` / `version` / `name` / `model` / `system` / `tools` 等；会话级覆盖（若已设置）已并入快照

**environment\_id** `string`

绑定的运行环境 ID

**sandbox** `object`

沙箱快照持久化配置与当前快照状态；未配置时省略

属性

**enable\_snapshot** `boolean`

当前 Session 是否开启快照持久化

**snapshot\_persistent\_seconds** `integer`

单份快照配置的保留时间，单位秒；未配置时不返回

**is\_persisting** `boolean`

当前 Session 是否正在保留可用快照；尚未取得统计时可能不返回

**predict\_release\_time** `string / null`

当前快照预计释放时间，ISO 8601 UTC；没有当前快照时为 `null`

**usage.sandbox** `object`

沙箱快照时长统计。创建响应中可能省略；已开启快照但尚未生成快照时，内部时长字段为 `null`。

属性

**session\_total\_persisted\_hours** `integer / null`

历史快照累计保留小时数；尚无统计时为 `null`

**latest\_snapshot\_persisted\_hours** `integer / null`

当前最新快照已保留小时数；没有当前快照时为 `null`

**title / metadata** `string / object`

会话标题与业务自定义元数据

**archived\_at** `string / null`

归档时间，未归档时为 `null`

**created\_at / updated\_at** `string`

创建 / 最近更新时间，ISO 8601

**request\_id** `string`

本次请求的唯一标识

**environment\_variables** `object`

会话运行时注入的环境变量，字符串键值对，沙箱代码中可直接按名读取

**vault\_ids** `array of string`

绑定的 Vault ID 列表

**mcp\_configs** `array of object`

会话级 MCP 请求头，每项含 `mcp_server_name` 与 `headers`；未配置时为空数组

## 响应示例

```
{
  "id": "sesn_xxx",
  "type": "session",
  "status": "idle",
  "stop_reason": {
    "type": "requires_action",
    "pending_batch_id": "response_xxx:9f2c...",
    "pending_call_ids": [
      "call_xxx"
    ]
  },
  "agent": {
    "id": "agent_xxx",
    "type": "agent",
    "version": 1,
    "name": "data-analyst",
    "description": null,
    "model": {"id": "qwen3.7-max"},
    "system": "你是数据分析专家，使用 pandas 处理 CSV 文件。",
    "tools": []
  },
  "environment_id": "env_xxx",
  "title": "Q3 销售数据分析",
  "metadata": {"biz_ticket_id": "1234"},
  "archived_at": null,
  "created_at": "2026-05-28T08:23:11Z",
  "updated_at": "2026-05-28T08:23:25Z",
  "request_id": "xxx",
  "environment_variables": {"API_BASE_URL": "https://api.example.com", "LOG_LEVEL": "info"},
  "vault_ids": ["vlt_xxx"],
  "mcp_configs": [{"mcp_server_name": "crm", "headers": {"X-Tenant-Id": "tenant-demo"}}]
}
```

### 沙箱快照响应示例

当前存在可用快照时：

```
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

```
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
