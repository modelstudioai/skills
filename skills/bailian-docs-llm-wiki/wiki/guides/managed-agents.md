# managed agents

Managed Agents 是百炼平台提供的智能体托管运行时，专为多步工具调用、代码执行、文件处理等长时运行任务设计。平台统一托管会话状态、沙箱环境与工具执行生命周期，事件历史在服务端持久化，支持中断续接与跨会话状态共享。开发者可聚焦于 Agent 逻辑本身，无需自行构建代理循环、沙箱编排或工具执行基础设施。

## 支持的模型与功能

Managed Agents 支持百炼全系列大模型（如 `qwen3-max`、`qwen3.7-plus`、`qwen3.8-max` 等），模型选择在创建智能体时指定，变更将生成新版本并影响后续新建会话 [定义 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-agent-definition.md)。

核心功能覆盖：
- **多步自主执行**：智能体基于系统提示词与上下文，自主决策调用内置工具、MCP 服务或 Skill；
- **云端沙箱环境**：独立容器化执行环境，支持预装 `apt`/`pip`/`npm` 包及自定义网络策略；
- **文件与记忆管理**：支持挂载本地文件（单文件 ≤50 MB）、跨会话持久化的记忆库（Memory Store）[记忆库](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-memory-store.md)；
- **多智能体协作**：通过 `coordinator` 编队协调多个成员智能体协同完成复杂任务 [多智能体协作](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-multiagent.md)；
- **安全密钥注入**：通过密钥库（Vault）集中管理 API Key，网关按域名规则在 Authorization 头中动态替换占位符，避免密钥泄露 [密钥库认证](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-credential.md)。

> **注意**：文档 1 中示例代码使用 `qwen3.8-max`，而文档 6 的 API 示例使用 `qwen3-max`；实际可用模型以控制台下拉列表或 [模型服务文档](https://help.aliyun.com/zh/model-studio/model-service) 为准，API 请求中传入不存在的模型 ID 将返回 400 错误。

## 关键参数

| 参数 | 说明 | 是否必填 | 可变更性 | 来源 |
|------|------|----------|-----------|------|
| `name` | 智能体/环境/会话唯一标识符（工作空间内） | 是 | 是 | [定义 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-agent-definition.md) |
| `model.id` | 模型 ID（如 `qwen3-max`） | 是 | 是（触发新版本） | [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md) |
| `system_prompt` | 定义角色、行为与约束的系统提示词 | 否 | 是（触发新版本） | [定义 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-agent-definition.md) |
| `tools` | 内置工具包配置，含 `bash`/`read`/`write`/`edit`/`glob`/`grep`/`web_search`/`web_fetch`/`mark_artifacts`；支持 `permission_policy: always_allow` 或 `always_ask` | 否 | 是 | [Agent 工具配置](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md) |
| `mcp_servers` | MCP 服务列表（如 `{"type": "official", "name": "web_search"}`） | 否 | 是 | [Agent MCP](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-mcp.md) |
| `multiagent` | 协作拓扑配置，当前仅支持 `coordinator` 类型 | 否 | 是 | [多智能体协作](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-multiagent.md) |
| `config.type` | 运行环境类型，固定为 `"cloud"` | 是（API） | 否 | [云端托管环境](../../raw/application-user-guide/managed-agents/managed-agents-environment/managed-agents-cloud-hosting.md) |
| `resources` | 会话挂载资源，支持 `file`（含 `mount_path`）和 `memory_store`（含 `access` 和 `instructions`） | 否 | 创建时指定，运行时仅可追加文件 | [文件上传与挂载](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-file.md) |

## 使用方式

### 1. 创建智能体（Agent）
通过控制台向导或 API 创建，需指定名称、模型与可选工具/MCP/Skill。每次保存生成新版本，会话创建时锁定该版本：
```python
agent = client.agents.create(
    name="data-analyst",
    model="qwen3-max",
    system_prompt="你是数据分析专家，使用 pandas 处理 CSV 文件。",
    tools=[{
        "type": "builtin_toolkit",
        "default_config": {"enabled": True, "permission_policy": {"type": "always_allow"}},
        "configs": [{"name": "bash", "enabled": True}, {"name": "read", "enabled": True}]
    }]
)
```

### 2. 创建运行环境（Environment）
独立于智能体管理，支持复用。配置云端沙箱及预装包：
```python
env = client.environments.create(
    name="data-sandbox",
    config={
        "type": "cloud",
        "packages": {"pip": ["pandas", "numpy"]},
        "networking": {"type": "unrestricted"}
    }
)
```

### 3. 发起会话（Session）
绑定智能体与环境，可挂载文件或记忆库：
```python
session = client.sessions.create(
    agent=agent.id,
    environment_id=env.id,
    resources=[
        {"type": "file", "file_id": "file_xxx", "mount_path": "/workspace/data.csv"},
        {"type": "memory_store", "memory_store_id": "memstore_xxx", "access": "read_write"}
    ]
)
```

### 4. 交互与事件流
- 发送用户消息：`POST /sessions/{id}/events`，`type=message`
- 订阅实时事件：`GET /sessions/{id}/events/stream`（SSE）
- 处理审批：收到 `tool_approval_request` 后，发送 `tool_approval_response`（`allow`/`deny`）[会话事件流（SSE）](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-event-stream.md)

### 5. CLI 管理（基础设施即代码）
使用 `bl managed-agent` 命令集进行声明式管理：
```bash
bl managed-agent init          # 初始化 YAML 配置模板
bl managed-agent apply         # 创建/更新资源（Agent/Env/Skill/Deployment）
bl managed-agent session run   # 创建会话并发送初始消息
```

## 限制和注意事项

- **会话状态机约束**：会话处于 `idle` 且 `stop_reason=requires_action` 时，**禁止发送普通 `message`**，必须先提交 `tool_approval_response` 或发送 `interrupt`；否则返回 `pending_tool_approval_unresolved` 错误 [管理会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-operations.md)。
- **资源配额**：
  - 单文件 ≤ 50 MB，工作空间总容量 ≤ 100 GB，文件保存时效 30 天；
  - 单个记忆文件 ≤ 102,400 UTF-8 字节，单会话最多挂载 8 个记忆库；
  - `web_search` 工具按 0.03 元/次计费，`web_fetch` 当前限时免费 [计费说明](../../raw/application-user-guide/managed-agents/managed-agents-billing.md)。
- **挂载路径约定**：所有挂载资源均位于 `/mnt/` 下——文件挂载至 `/mnt/session/uploads/{mount_path}`，记忆库挂载至 `/mnt/memory/{名称}`；智能体必须使用**实际路径**（非用户填写的相对路径）访问。
- **审批机制范围**：工具审批（`always_ask`）**仅对主智能体生效，不支持子智能体**；客户端自定义工具（`function`/`custom`）不参与此审批流程 [Agent 工具配置](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)。
- **密钥安全边界**：密钥库仅支持在 Authorization 头中替换 `${VAR}` 占位符，**不支持请求体或查询参数中的密钥注入**；若第三方 SDK 无法保证密钥仅出现在 Authorization 头，应改用会话环境变量 [密钥库认证](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-credential.md)。

## 来源文档

- [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)
- [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)
- [使用 CLI](../../raw/application-user-guide/managed-agents/managed-agents-cli.md)
- [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)
- [Agent 工具配置](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)
- [定义 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-agent-definition.md)
- [Agent MCP](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-mcp.md)
- [多智能体协作](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-multiagent.md)
- [Agent Skills](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-skill.md)
- [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)
- [云端托管环境](../../raw/application-user-guide/managed-agents/managed-agents-environment/managed-agents-cloud-hosting.md)
- [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)
- [发起会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-event.md)
- [管理会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-operations.md)
- [会话事件流（SSE）](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-event-stream.md)
- [密钥库认证](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-credential.md)
- [定时任务](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-deployment.md)
- [Webhook 通知](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-webhook.md)
- [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)
- [文件上传与挂载](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-file.md)
- [记忆库](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-memory-store.md)
- [计费说明](../../raw/application-user-guide/managed-agents/managed-agents-billing.md)
- [更新日志](../../raw/application-user-guide/managed-agents/managed-agents-changelog.md)


