# managed agents api

Managed Agents API 是百炼提供的智能体托管运行时，由平台托管会话、沙箱、工具执行与事件流。开发者通过 REST 或 DashScope SDK 管理智能体（Agent）、运行环境（Environment）、技能（Skill）、文件（File）和会话（Session）等资源，无需自建调度与执行基础设施。详见 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。

## 前提条件与 Endpoint

1. 开通百炼并创建 API Key（`sk-xxx`），将其配置到环境变量 `DASHSCOPE_API_KEY`。
2. 在控制台右上角获取工作空间 ID，形如 `ws_xxxxxxxxxxxx`。
3. Endpoint 按工作空间与地域拼装，当前仅支持 `cn-beijing`：

```
https://{workspace_id}.{region}.maas.aliyuncs.com/api/v1/agentstudio
```

全部请求通过 HTTP Header 鉴权，一个 Key 可访问其归属工作空间下的全部资源：

```
Authorization: Bearer <your-api-key>
```

请求体为 JSON（`Content-Type: application/json`），每个响应携带 `x-request-id` 头，提工单时附上可加速定位。列表端点支持分页：`limit`（默认 20，最大 100）、`page`（首次不传，后续传上一次响应的 `next_page`，响应不含该字段表示末页）。

## SDK

除直接调用 REST 外，可使用 Python 或 Java SDK 接入：

- Python：`pip install dashscope`，要求 v1.26.2 及以上
- Java：引入 `com.alibaba:dashscope-sdk-java`，要求 v2.22.24 及以上

旧版本需重新执行安装命令升级。端到端示例见 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)。

## 资源模型

| 资源 | 端点前缀 | 说明 |
| --- | --- | --- |
| Agent | `/agents` | 可复用的智能体配置：模型、系统提示词、工具包、技能 |
| Environment | `/environments` | 工具调用的执行沙箱与预装依赖，可被多会话复用 |
| Session and Event | `/sessions` | 智能体的一次运行实例，绑定 Agent 与 Environment 快照 |
| Skill | `/skills` | 以 zip 包封装的工具组合与文档，挂载时锁定具体版本号 |
| File | `/files` | 独立文件资源，可挂载到沙箱供工具读写或作为消息内容 |

## 调用流程

一次完整对话分四步（详见 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)）：

1. **创建 Agent**：定义模型与系统提示词，得到 `agent_xxx`。Agent 通常创建一次并长期复用。
2. **创建 Session**：绑定 Agent，得到 `sesn_xxx`。每轮对话新建一个 Session。
3. **发送 Event**：向 Session 写入用户消息，触发 Agent 进入 `running`。
4. **订阅 SSE**：通过 `GET /sessions/{session_id}/events/stream` 流式接收回复，直至 Session 回到 `idle`。

Bash 示例：

```bash
export DASHSCOPE_API_KEY="sk-xxx"
export AGENTSTUDIO_URL="https://ws_xxxxxxxxxxxx.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio"

# 1. 创建 Agent
AGENT_ID=$(curl -s -X POST "$AGENTSTUDIO_URL/agents" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name":"quickstart-assistant","model":{"id":"qwen-plus"},"system":"你是一个有帮助的助手。"}' | jq -r '.id')

# 2. 创建 Session
SESSION_ID=$(curl -s -X POST "$AGENTSTUDIO_URL/sessions" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"agent\":\"$AGENT_ID\"}" | jq -r '.id')

# 3. 发送用户消息
curl -X POST "$AGENTSTUDIO_URL/sessions/$SESSION_ID/events" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"input":[{"role":"user","type":"message","content":[{"type":"text","text":"你好，请介绍一下自己"}]}]}'

# 4. 订阅 SSE
curl -N "$AGENTSTUDIO_URL/sessions/$SESSION_ID/events/stream" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Accept: text/event-stream"
```

Python SDK 示例：

```python
import os
from dashscope.agentstudio import Client, user_message

client = Client(
    api_key=os.environ["DASHSCOPE_API_KEY"],
    workspace="ws_xxxxxxxxxxxx",
    region="cn-beijing",
)
agent = client.agents.create(name="quickstart-assistant", model="qwen-plus", system_prompt="你是一个有帮助的助手。")
session = client.sessions.create(agent=agent.id)
client.sessions.events.send(session.id, [user_message("你好，请介绍一下自己")])
with client.sessions.events.stream(session.id) as stream:
    for event in stream:
        print(event, flush=True)
        if event.session_status in ("idle", "terminated"):
            break
```

## Agent

Agent 是一份可复用配置，每次更新自动递增 `version` 版本号，会话创建时锁定当时版本。Agent 操作详见 [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)。

| 操作 | 端点 | 说明 |
| --- | --- | --- |
| 创建 Agent | `POST /agents` | 创建智能体，初始 `version` 为 1 |
| 获取 Agent | `GET /agents/{agent_id}` | 默认返回最新版本；`?version=N` 查询历史版本 |
| 列出 Agent | `GET /agents` | 分页列出，默认不含已归档 |
| 更新 Agent | `POST /agents/{agent_id}` | 全量替换；请求体需带 `version` 作乐观锁，不一致返回 409，成功后递增 |
| 归档 Agent | `POST /agents/{agent_id}/archive` | 软归档；不可用于新建会话，已有会话不受影响 |
| 列出 Agent 版本 | `GET /agents/{agent_id}/versions` | 分页返回全部历史版本 |

> **注意**：API 总览文档将更新 Agent 列为 `PATCH /agents/{agent_id}`，而 Agent 专篇文档说明为 `POST /agents/{agent_id}` 并采用全量替换语义。以 Agent 专篇为准，请求体需带 `version` 作乐观锁。

## Environment

运行环境定义工具调用的执行沙箱与预装依赖，独立于智能体管理，可被多个会话复用。详见 [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)。

| 操作 | 端点 | 说明 |
| --- | --- | --- |
| 创建 Environment | `POST /environments` | 指定沙箱类型与预装依赖 |
| 获取 Environment | `GET /environments/{environment_id}` | 获取环境详情 |
| 列出 Environment | `GET /environments` | 分页列出，默认不含已归档 |
| 更新 Environment | `POST /environments/{environment_id}` | 全量替换；缺省字段视为清空，运行中会话使用绑定快照不受影响 |
| 归档 Environment | `POST /environments/{environment_id}/archive` | 软归档；默认不再出现在列表中，已绑定会话仍可用 |
| 删除 Environment | `DELETE /environments/{environment_id}` | 硬删除；配置一并清除，不可恢复 |

> **注意**：API 总览文档将更新 Environment 列为 `PATCH`，Environment 专篇文档说明为 `POST`，以专篇为准。

## Session and Event

Session 是智能体的一次运行实例，绑定 Agent 与 Environment 快照，由平台驱动状态机。Event 是会话内的原子记录，由客户端写入或经订阅服务端推送。详见 [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)。

### 状态机

`status` 字段变化通过 SSE 的 `session_status` 事件推送。

| 状态 | 触发条件 | 下一状态 | 可执行操作 |
| --- | --- | --- | --- |
| `idle` | 会话创建完成或上一轮处理结束 | 收到消息 → `running` | 发送消息、归档、删除 |
| `running` | 收到用户消息，智能体开始处理 | 完成 → `idle`；不可恢复 → `terminated` | 中断、审批工具调用、回填函数结果 |
| `terminated` | 归档调用或不可恢复错误 | 终态 | 查询事件历史、删除会话 |

### 会话与事件操作

| 操作 | 端点 | 说明 |
| --- | --- | --- |
| 创建 Session | `POST /sessions` | 绑定 Agent 快照与运行环境，初始状态 `idle` |
| 获取 Session | `GET /sessions/{session_id}` | 含智能体快照与当前状态 |
| 列出 Session | `GET /sessions` | 分页列出工作空间下的会话 |
| 更新 Session | `POST /sessions/{session_id}` | 更新元数据（标题、metadata 等） |
| 归档 Session | `POST /sessions/{session_id}/archive` | 软归档；会话进入 `terminated` 终态 |
| 删除 Session | `DELETE /sessions/{session_id}` | 硬删除；事件历史一并清除，不可恢复 |
| 发送 Event | `POST /sessions/{session_id}/events` | 注入用户消息、中断、工具审批、回填函数结果等 |
| 列出 Event | `GET /sessions/{session_id}/events` | 分页列出事件历史 |
| 订阅 Event SSE | `GET /sessions/{session_id}/events/stream` | 长连接订阅实时事件，含 `session_status` 状态变更 |

> **注意**：API 总览文档将更新 Session 列为 `PATCH`，Session 专篇文档说明为 `POST`，以专篇为准。

## Skill

技能以 zip 包封装工具组合与文档，上传后经安全扫描方可挂载到智能体，挂载时锁定具体版本号（不支持 `latest`）。详见 [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)。

### 扫描状态

| 状态 | 含义 |
| --- | --- |
| `checking` | 扫描中，暂不可挂载 |
| `active` | 扫描通过，可挂载到智能体 |
| `rejected` | 命中安全风险，不可挂载；版本详情 `additional_properties.error_info` 按文件路径列出问题 |
| `deleted` | 技能已删除 |

### 技能与版本操作

| 操作 | 端点 | 说明 |
| --- | --- | --- |
| 创建 Skill | `POST /skills` | 用已上传的 zip 包 `file_id` 创建技能 |
| 查询 Skill | `GET /skills/{skill_id}` | 获取元数据与最新版本号 |
| 列出 Skill | `GET /skills` | 支持按 `source` 过滤自建/官方 |
| 删除 Skill | `DELETE /skills/{skill_id}` | 删除技能及全部版本；已挂载旧版本的智能体不受影响 |
| 上传 Skill 新版本 | `POST /skills/{skill_id}/versions` | 用新的 zip 包 `file_id` 上传；已挂载旧版本不受影响 |
| 列出 Skill 版本 | `GET /skills/{skill_id}/versions` | 按版本号倒序 |
| 查询 Skill 版本 | `GET /skills/{skill_id}/versions/{version}` | 查询指定版本的元数据与扫描状态 |
| 下载 Skill 包 | `GET /skills/{skill_id}/versions/{version}/content` | 返回 OSS 预签名 URL（2 小时有效） |

## File

文件是独立资源，上传一次后可被多个会话挂载至沙箱供工具读写，也可作为消息内容（图像、音频、附件）传给智能体。详见 [File](../../raw/application-api-reference/managed-agents-api/files-api.md)。

### 配额与状态

- 单文件直传上限 **20 MB**；单个工作空间总容量上限 **100 GB**；保留期 **30 天**，超期可能被自动清理。
- 上传后进入安全审核，`status` 取值 `checking` / `available` / `rejected` / `type_rejected`，仅 `available` 可挂载或作为消息内容引用。
- 挂载到会话沙箱时服务端做内部拷贝并生成新的 `file_id`，副本元数据带 `scope: {"type":"session","id":"sesn_..."}`，仅对应会话可见。

### 文件操作

| 操作 | 端点 | 说明 |
| --- | --- | --- |
| 上传 File | `POST /files` | `multipart/form-data` 直传，初始状态 `checking` |
| 查询 File | `GET /files/{file_id}` | 查询元数据与审核状态（不含内容） |
| 列出 File | `GET /files` | 支持按会话 ID 过滤 |
| 删除 File | `DELETE /files/{file_id}` | 硬删除；已挂载到会话的内部拷贝不受影响 |

## 限制与注意事项

- **版本与快照**：Agent、Environment、Skill 更新均不影响已绑定它们的运行中会话；会话使用创建时的快照。
- **乐观锁**：Agent 更新需在请求体携带当前 `version`，不一致返回 409。
- **软删除 vs 硬删除**：归档为软操作（`archived_at` 被填入，已绑定会话继续可用）；`DELETE` 为硬操作，配置与事件历史一并清除，不可恢复。
- **Skill 挂载**：必须指定具体 `version`，不支持 `latest`；上传新版本不影响已挂载的智能体。
- **File 配额**：单文件 20 MB、工作空间总量 100 GB、保留期 30 天，超期可能被自动清理。
- **地域**：当前仅支持 `cn-beijing`。
- **SDK 版本**：Python 需 v1.26.2+，Java 需 v2.22.24+。

## 来源文档

- [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)
- [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)
- [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)
- [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)
- [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)
- [File](../../raw/application-api-reference/managed-agents-api/files-api.md)
- [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)



