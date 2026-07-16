# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的智能体托管运行时，由平台负责会话管理、沙箱执行、工具调用与事件流推送。开发者通过 REST API 或 SDK 完成 Agent 定义、Environment 配置、Session 创建与事件交互，五分钟即可跑通端到端流程。详细的认证方式与 SDK 版本要求见 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。

## 核心概念与资源模型

Managed Agents 围绕五类资源构建：

- **Agent** — 智能体配置，包含模型、系统提示词、技能挂载。每次更新自动递增版本号，会话创建时锁定当时版本，后续更新不影响已有会话。详见 [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)。
- **Environment** — 运行环境，定义工具调用的沙箱类型与预装依赖，可被多个会话复用。
- **Session** — 智能体的一次运行实例，绑定 Agent 与 Environment 快照，由平台驱动状态机（`idle` → `running` → `idle` / `terminated`）。
- **Event** — 会话内的原子消息记录，包括用户消息、工具调用回执、状态变更等，支持 SSE 流式推送。
- **Skill** — 以 zip 包封装的工具组合，上传后经安全扫描（`checking` → `active` / `rejected`）方可挂载到 Agent，挂载时锁定具体版本号。
- **File** — 独立文件资源，上传后可挂载到会话沙箱供工具读写，或作为消息附件传给智能体。

## 认证与 Endpoint

API 基地址按工作空间与地域拼装：

```
https://{workspace_id}.{region}.maas.aliyuncs.com/api/v1/agentstudio
```

当前仅支持 `cn-beijing` 地域。所有请求通过 HTTP Header 携带 [API Key 鉴权](../concepts/api-key.md)：

```
Authorization: Bearer <your-api-key>
```

[API Key](../concepts/api-key.md) 通过百炼控制台获取，一个 Key 可访问其归属工作空间下的全部资源。每次响应携带 `x-request-id` 头，提工单时附上此 ID 可加速定位。

## 主要 API 端点

### Agent

| 操作 | 端点 | 说明 |
|------|------|------|
| 创建 | `POST /agents` | 创建智能体，初始 `version` 为 1 |
| 获取 | `GET /agents/{agent_id}` | 支持 `?version=N` 查询历史版本 |
| 列出 | `GET /agents` | 分页列出，默认不含已归档 |
| 更新 | `POST /agents/{agent_id}` | 全量替换，需带 `version` 作乐观锁 |
| 归档 | `POST /agents/{agent_id}/archive` | 软归档，已有会话不受影响 |
| 列出版本 | `GET /agents/{agent_id}/versions` | 分页返回全部历史版本 |

> **注意**：[API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md) 中 Agent 更新端点标注为 `PATCH`，而 [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md) 详情页标注为 `POST`，以各资源详情页为准。Environment 和 Session 的更新端点也存在类似差异。

### Session 与 Event

| 操作 | 端点 | 说明 |
|------|------|------|
| 创建 Session | `POST /sessions` | 绑定 Agent 与 Environment，初始状态 `idle` |
| 获取 Session | `GET /sessions/{session_id}` | 含智能体快照与当前状态 |
| 发送 Event | `POST /sessions/{session_id}/events` | 注入用户消息、工具审批、函数结果等 |
| 列出 Event | `GET /sessions/{session_id}/events` | 分页列出事件历史 |
| 订阅 SSE | `GET /sessions/{session_id}/events/stream` | 长连接流式接收实时事件 |
| 归档 Session | `POST /sessions/{session_id}/archive` | 进入 `terminated` 终态 |
| 删除 Session | `DELETE /sessions/{session_id}` | 硬删除，事件历史一并清除 |

会话状态机详见 [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)。

### Skill

技能上传后需通过安全扫描才能挂载。挂载时必须指定具体 `version`（不支持 `latest`），上传新版本不影响已挂载的智能体。详见 [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)。

| 操作 | 端点 | 说明 |
|------|------|------|
| 创建 | `POST /skills` | 用已上传的 zip 包 `file_id` 创建 |
| 上传新版本 | `POST /skills/{skill_id}/versions` | 新 zip 包，已挂载旧版本不受影响 |
| 下载 | `GET /skills/{skill_id}/versions/{version}/content` | 返回 OSS 预签名 URL（2 小时有效） |
| 删除 | `DELETE /skills/{skill_id}` | 删除技能及全部版本 |

### File

文件上传后经安全审核（`checking` → `available` / `rejected` / `type_rejected`），仅 `available` 状态可挂载到会话或作为消息引用。详见 [File](../../raw/application-api-reference/managed-agents-api/files-api.md)。

| 操作 | 端点 | 说明 |
|------|------|------|
| 上传 | `POST /files` | `multipart/form-data` 直传 |
| 查询 | `GET /files/{file_id}` | 元数据与审核状态 |
| 列出 | `GET /files` | 支持按会话 ID 过滤 |
| 删除 | `DELETE /files/{file_id}` | 已挂载的内部拷贝不受影响 |

**文件配额**：单文件上限 20 MB，工作空间总容量上限 100 GB，保留期 30 天。

### Environment

| 操作 | 端点 | 说明 |
|------|------|------|
| 创建 | `POST /environments` | 指定沙箱类型与预装依赖 |
| 获取 | `GET /environments/{environment_id}` | 环境详情 |
| 更新 | `POST /environments/{environment_id}` | 全量替换，运行中会话不受影响 |
| 归档 | `POST /environments/{environment_id}/archive` | 软归档，已绑定会话仍可用 |
| 删除 | `DELETE /environments/{environment_id}` | 硬删除，不可恢复 |

## 典型调用流程

一次完整的任务执行分五步，详见 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)：

1. **创建 Agent** — 定义模型与系统提示词，得到 `agent_xxx`（通常只创建一次，长期复用）
2. **创建 Environment** — 定义运行沙箱，得到 `env_xxx`（通常只创建一次，长期复用）
3. **创建 Session** — 绑定 Agent 与 Environment，得到 `sesn_xxx`
4. **发送 Event** — 向 Session 提交用户消息，触发 Agent 进入 `running`
5. **订阅 SSE** — 流式接收执行结果，直至 Session 回到 `idle`

## SDK 支持

Managed Agents 模块通过 [DashScope SDK](../concepts/dashscope-sdk.md) 接入，版本要求：

| 语言 | 包名 | 最低版本 |
|------|------|----------|
| Python | `dashscope` | v1.26.2 |
| Java | `dashscope-sdk-java` | v2.22.24 |

## 分页约定

列表端点统一支持分页参数：`limit`（默认 20，最大 100）和 `page`（首次不传，后续传上一次响应的 `next_page`）。响应不含 `next_page` 表示已是末页。

## 关键设计要点

- **版本锁定**：Agent 更新采用乐观锁（请求体带 `version`，不一致返回 409）；会话创建时锁定 Agent 版本，Skill 挂载锁定具体版本号，确保运行中会话不受配置变更影响。
- **软归档 vs 硬删除**：Agent、Session、Environment 均支持软归档（`archived_at` 标记），归档后不影响已有会话；File 和 Environment 支持硬删除（不可恢复）。
- **安全扫描**：Skill 和 File 上传后均需经过安全扫描/审核，仅通过后方可使用。
- **沙箱隔离**：文件挂载到会话时服务端做内部拷贝，生成独立 `file_id`，仅对应会话可见。

## 来源文档

- [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)
- [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)
- [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)
- [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)
- [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)
- [File](../../raw/application-api-reference/managed-agents-api/files-api.md)
- [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)











