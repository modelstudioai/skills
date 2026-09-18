# 创建 Session

创建一个会话实例：绑定智能体与运行环境。会话创建时拍摄智能体当时最新版本的完整快照。

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。创建会话前需先有智能体和运行环境，分别详见[Agent](raw/application-api-reference/managed-agents-api/agent-api.md)与[Environment](raw/application-api-reference/managed-agents-api/environment-api.md)。

## 接口

**POST** `/sessions`

## 请求体

字段

必填

类型

说明

`agent`

是

string

绑定的智能体 ID。会话锁定智能体当前最新版本的快照

`environment_id`

是

string

绑定的运行环境 ID

`title`

否

string

会话标题，便于在列表中辨识

`resources`

否

array

创建时挂载的资源列表。文件项含 `type`（固定为 `file`）、`file_id`（已上传的文件 ID）、`mount_path`（挂载路径，必须以 `/uploads/` 开头，实际路径会加上 `/mnt/session` 前缀）；记忆库项含 `type`（固定为 `memory_store`）、`memory_store_id`、`access`（`read_only` / `read_write`，默认 `read_write`）、`instructions`（挂载说明，最长 4096 字符），挂载路径由服务端按记忆库名称生成。详见[记忆库](raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-memory-store.md)

`vault_ids`

否

array of string

Vault ID 列表。将指定 Vault 中的 Credential 注入会话运行环境，使智能体可访问对应密钥

`metadata`

否

object

业务自定义键值，不影响模型行为

`environment_variables`

否

object

会话运行时注入的环境变量，字符串键值对，沙箱代码中可直接按名读取

## 请求示例

bash

```
curl -X POST "$AGENTSTUDIO_URL/sessions" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "agent": "agent_xxx",
    "environment_id": "env_xxx",
    "title": "Q3 销售数据分析",
    "resources": [
      {"type": "file", "file_id": "file_xxx", "mount_path": "/uploads/workspace/data.csv"}
    ],
    "vault_ids": ["vlt_xxx"],
    "metadata": {"biz_ticket_id": "1234"},
    "environment_variables": {"API_BASE_URL": "https://api.example.com", "LOG_LEVEL": "info"}
  }'
```

python

```
session = client.sessions.create(
    agent="agent_xxx",
    environment_id="env_xxx",
    title="Q3 销售数据分析",
    resources=[
        {"type": "file", "file_id": "file_xxx", "mount_path": "/uploads/workspace/data.csv"},
    ],
    vault_ids=["vlt_xxx"],
    metadata={"biz_ticket_id": "1234"},
    environment_variables={"API_BASE_URL": "https://api.example.com", "LOG_LEVEL": "info"},
)
print(session.id, session.status)
```

java

```
Map<String, String> metadata = new HashMap<>();
metadata.put("biz_ticket_id", "1234");

Map<String, String> environmentVariables = new HashMap<>();
environmentVariables.put("API_BASE_URL", "https://api.example.com");
environmentVariables.put("LOG_LEVEL", "info");

Session session = client.sessions().create(SessionCreateParam.builder()
    .agentId("agent_xxx")
    .environmentId("env_xxx")
    .title("Q3 销售数据分析")
    .resources(List.of(SessionResource.builder()
        .type("file")
        .fileId("file_xxx")
        .mountPath("/uploads/workspace/data.csv")
        .build()))
    .vaultIds(List.of("vlt_xxx"))
    .metadata(metadata)
    .environmentVariables(environmentVariables)
    .build());
System.out.println(session.getId() + " " + session.getStatus());
```

## 响应示例

会话详情嵌入完整的智能体快照。

```
{
  "id": "sesn_xxx",
  "type": "session",
  "status": "idle",
  "agent": {
    "id": "agent_xxx",
    "type": "agent",
    "version": 1,
    "name": "data-analyst",
    "description": null,
    "model": {"id": "qwen3-max"},
    "system": "你是数据分析专家，使用 pandas 处理 CSV 文件。",
    "tools": []
  },
  "environment_id": "env_xxx",
  "title": "Q3 销售数据分析",
  "resources": [
    {
      "id": "sesrsc_xxx",
      "type": "file",
      "file_id": "file_xxx",
      "mount_path": "/mnt/session/uploads/workspace/data.csv",
      "created_at": "2026-05-28T08:23:11Z",
      "updated_at": "2026-05-28T08:23:11Z"
    }
  ],
  "metadata": {"biz_ticket_id": "1234"},
  "archived_at": null,
  "created_at": "2026-05-28T08:23:11Z",
  "updated_at": "2026-05-28T08:23:11Z",
  "request_id": "xxx",
  "environment_variables": {"API_BASE_URL": "https://api.example.com", "LOG_LEVEL": "info"}
}
```

响应为 Session 对象。字段如下：

### 响应字段

字段

类型

说明

`id`

string

会话 ID，格式 `sesn_&lt;ULID&gt;`

`type`

string

固定为 `session`

`status`

string

会话状态：`idle` / `running` / `terminated`。新建会话为 `idle`

`agent`

object

智能体配置完整快照（创建时锁定），含 `id` / `version` / `name` / `model` / `system` / `tools` 等

`environment_id`

string

绑定的运行环境 ID

`resources`

array

挂载的资源列表。文件项含 `id`（资源 ID）、`type`、`file_id`（内部副本 ID）、`mount_path`（含前缀的完整路径）；记忆库项含 `id`、`type`、`file_id`（固定为 `null`）、`memory_store_id`、`name` / `description`（记忆库元数据）、`access`、`instructions`、`mount_path`（服务端生成，如 `/mnt/memory/<名称>`）

`title` / `metadata`

string / object

同请求体

`archived_at`

string / null

归档时间，未归档时为 `null`

`created_at` / `updated_at`

string

创建 / 最近更新时间，ISO 8601

`request_id`

string

本次请求的唯一标识

`environment_variables`

object

会话运行时注入的环境变量，字符串键值对，沙箱代码中可直接按名读取

## 配置锁定

会话创建时拍摄智能体当时最新版本的完整快照（嵌入到会话详情的 `agent` 字段）。后续编辑智能体只影响新建会话，已有会话继续使用快照中的配置。
