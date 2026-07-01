# managed agents api

Managed Agents API 是百炼提供的智能体托管运行时，由平台托管会话、沙箱、工具执行与事件流。开发者通过 REST API 管理智能体、运行环境、会话、技能与文件五类资源，无需自建推理调度与工具执行基础设施。

## 接入前提

1. 开通百炼并创建 [API Key](../concepts/api-key.md)，[配置 API Key 到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
2. 在百炼控制台右上角下拉菜单获取工作空间 ID，形如 `ws_xxxxxxxxxxxx`。

基地址按工作空间与地域拼装：

```
https://{workspace_id}.{region}.maas.aliyuncs.com/api/v1/agentstudio
```

- `workspace_id`：工作空间 ID。
- `region`：地域 ID，当前仅支持 `cn-beijing`。

全部请求通过 HTTP Header 携带 [API Key](../concepts/api-key.md)，一个 Key 可访问其归属工作空间下的全部资源：

```
Authorization: Bearer <your-api-key>
```

请求体为 JSON（`Content-Type: application/json`，文件上传除外）；每次响应携带 `x-request-id` 头，提工单时附上可加速定位。列表端点支持分页：`limit`（默认 20，最大 100）、`page`（首次不传，后续传上一次响应的 `next_page`），响应不含 `next_page` 即末页。

## 资源模型与端点

API 围绕五类资源组织，详见 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)：

| 资源 | 端点前缀 | 用途 |
| --- | --- | --- |
| Agent | `/agents` | 可复用的智能体配置（模型、系统提示词、工具包、技能） |
| Environment | `/environments` | 工具调用的执行沙箱与预装依赖 |
| Session / Event | `/sessions` | 智能体运行实例与事件流 |
| File | `/files` | 独立文件资源，可挂载到沙箱或作为消息内容 |
| Skill | `/skills` | zip 包封装的工具组合与文档 |

## Agent

智能体是一份可复用的配置：模型、系统提示词、工具包、技能。每次更新自动递增版本号，会话创建时锁定当时版本，详见 [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)。

**版本机制**：更新接口采用全量替换语义，请求体需带当前 `version` 作乐观锁，不一致返回 409，成功后 `version` 自动 +1。会话创建时锁定当时 `version`，已有会话不受后续更新影响；查询历史版本用 `GET /agents/{agent_id}?version=N`。归档为软操作，归档后不可用于新建会话，已有会话不受影响。

| 操作 | 端点 |
| --- | --- |
| 创建 Agent | `POST /agents` |
| 获取 Agent | `GET /agents/{agent_id}`（带 `?version=N` 查历史） |
| 列出 Agent | `GET /agents`（默认不含已归档） |
| 更新 Agent | `POST /agents/{agent_id}` |
| 归档 Agent | `POST /agents/{agent_id}/archive` |
| 列出版本 | `GET /agents/{agent_id}/versions` |

## Environment

运行环境定义工具调用的执行沙箱与预装依赖，独立于智能体管理，可被多个会话复用。更新采用全量替换语义，缺省字段视为清空；已绑定该环境的运行中会话使用绑定时的快照，不受更新影响。

- 归档为软操作，默认不再出现在列表中，仍可被查询，已绑定会话继续可用。
- 删除为硬操作，环境配置一并清除，不可恢复。

| 操作 | 端点 |
| --- | --- |
| 创建 Environment | `POST /environments` |
| 获取 Environment | `GET /environments/{environment_id}` |
| 列出 Environment | `GET /environments` |
| 更新 Environment | `POST /environments/{environment_id}` |
| 归档 Environment | `POST /environments/{environment_id}/archive` |
| 删除 Environment | `DELETE /environments/{environment_id}` |

## Session and Event

Session 是智能体的一次运行实例，绑定智能体与环境快照，由平台驱动状态机。Event 是会话内的原子记录，由客户端写入或经订阅服务端推送，详见 [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)。

**状态机**（`status` 字段，变更通过 SSE `session_status` 事件推送）：

| 状态 | 触发条件 | 下一状态 | 可执行操作 |
| --- | --- | --- | --- |
| `idle` | 会话创建完成，或上一轮处理结束 | 收到消息 → `running` | 发送消息、归档、删除 |
| `running` | 收到用户消息，智能体开始处理 | 完成 → `idle`；不可恢复 → `terminated` | 中断、审批工具调用、回填函数结果 |
| `terminated` | 归档调用，或不可恢复错误 | 终态 | 查询事件历史、删除会话 |

| 操作 | 端点 |
| --- | --- |
| 创建 Session | `POST /sessions`（初始 `idle`） |
| 获取 Session | `GET /sessions/{session_id}` |
| 列出 Session | `GET /sessions` |
| 更新 Session | `POST /sessions/{session_id}`（标题、metadata） |
| 归档 Session | `POST /sessions/{session_id}/archive`（进入 `terminated`） |
| 删除 Session | `DELETE /sessions/{session_id}`（事件历史一并清除） |
| 发送 Event | `POST /sessions/{session_id}/events` |
| 列出 Event | `GET /sessions/{session_id}/events` |
| 订阅 SSE 事件流 | `GET /sessions/{session_id}/events/stream` |

## File

文件是独立资源，上传一次后可被多个会话挂载至沙箱供工具读写，也可作为消息内容（图像、音频、附件）传给智能体。

**配额与状态**：单文件直传上限 20 MB；单工作空间总容量上限 100 GB；保留期 30 天，超期可能被自动清理。上传后进入安全审核，`status` 取值 `checking` / `available` / `rejected` / `type_rejected`，仅 `available` 可挂载或作为消息内容引用。挂载到会话沙箱时服务端做内部拷贝并生成新的 `file_id`，副本仅对应会话可见。

| 操作 | 端点 |
| --- | --- |
| 上传 File | `POST /files`（`multipart/form-data`） |
| 查询 File | `GET /files/{file_id}` |
| 列出 File | `GET /files`（支持按会话 ID 过滤） |
| 删除 File | `DELETE /files/{file_id}` |

## Skill

技能以 zip 包封装工具组合与文档。上传后经安全扫描方可挂载到智能体，挂载时锁定具体版本号，详见 [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)。

**扫描状态**：新建或上传新版本后进入安全扫描，`status` 状态流转为 `checking`（扫描中）→ `active`（可挂载）或 `rejected`（命中风险，不可挂载，版本详情 `additional_properties.error_info` 按文件路径列出问题）；`deleted` 表示技能已删除。挂载时必须指定具体 `version`（不支持 `latest`），后续上传新版本不影响已挂载的智能体。

| 操作 | 端点 |
| --- | --- |
| 创建 Skill | `POST /skills`（用已上传 zip 包 `file_id`） |
| 查询 Skill | `GET /skills/{skill_id}` |
| 列出 Skill | `GET /skills`（支持按 `source` 过滤自建/官方） |
| 删除 Skill | `DELETE /skills/{skill_id}`（已挂载旧版本不受影响） |
| 上传新版本 | `POST /skills/{skill_id}/versions` |
| 列出版本 | `GET /skills/{skill_id}/versions` |
| 查询版本 | `GET /skills/{skill_id}/versions/{version}` |
| 下载 Skill 包 | `GET /skills/{skill_id}/versions/{version}/content`（返回 2 小时有效预签名 URL） |

## 通用约定

- **全量替换语义**：Agent、Environment 的更新均为全量替换，缺省字段视为清空，请求体需带当前版本号作乐观锁。
- **软归档 vs 硬删除**：归档为软操作（填入 `archived_at`，不影响已有会话/已挂载实例），删除为硬操作（配置/事件历史一并清除，不可恢复）。
- **快照绑定**：会话创建时锁定 Agent 与 Environment 的当时版本，后续对资源的更新不影响已运行的会话。
- **安全审核**：File 与 Skill 上传后均需通过安全扫描才可使用，`status` 为 `checking` 时不可挂载。

> **注意**：API 总览文档中将 Agent / Environment / Session 的更新端点列为 `PATCH` 方法，而各资源的专属文档（Agent、Environment、Session）中更新操作均使用 `POST` 方法并以全量替换语义描述。两处存在不一致，调用时以各资源专属文档的 `POST` + 请求体带 `version` 的写法为准，若遇 405 再尝试 `PATCH`。

## 来源文档

- [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)
- [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)
- [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)
- [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)
- [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)
- [File](../../raw/application-api-reference/managed-agents-api/files-api.md)



