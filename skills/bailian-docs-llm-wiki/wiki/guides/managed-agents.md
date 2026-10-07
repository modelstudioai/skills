# managed agents

managed agents 是百炼平台提供的托管式智能体服务，允许开发者无需自行部署和运维 Agent 运行时，即可快速创建、配置并调用具备多步推理与工具调用能力的智能体。它基于平台统一的执行引擎，支持声明式定义行为逻辑与上下文管理，并与百炼模型服务深度集成。详细背景可参见 [Managed Agents](../../raw/application-user-guide/managed-agents.md)。

## 支持的模型与功能

- **模型支持**：当前仅支持 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三款 Qwen 系列模型（[概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)）；其他模型（如 `qwen2.5-*` 或第三方模型）暂不可用于 managed agents。
- **核心功能**：
  - 多轮对话状态自动维护
  - 内置工具调用（HTTP 请求、知识库检索、函数执行等）
  - 可配置的会话生命周期与上下文窗口控制
  - 支持通过 YAML 或 API 定义 agent 行为逻辑（[构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)）

> **注意**：原始文档中 [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md) 提到支持 `qwen-vl` 视觉模型，但该能力已于 v2.3.0 版本下线，实际调用将返回 `model_not_supported` 错误 —— 请以 [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md) 中的模型白名单为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 必须为 `qwen-max` / `qwen-plus` / `qwen-turbo` 之一 |
| `tools` | array | 否 | 工具列表，每个工具需含 `type`（如 `"http"`、`"retrieval"`）和 `config` 字段 |
| `session_timeout_ms` | integer | 否 | 会话空闲超时时间，默认 `300000`（5 分钟），最大 `3600000`（1 小时） |
| `max_iterations` | integer | 否 | 单次请求最大推理步数，默认 `15`，范围 `1–50` |

## 使用方式

1. **定义 Agent**：通过 YAML 文件或 `/v1/agents` API 创建 agent 实例，指定模型、工具集与初始 [prompt](prompt.md)；
2. **启动会话**：调用 `/v1/agents/{agent_id}/sessions` 获取 session ID；
3. **交互调用**：向 `/v1/agents/{agent_id}/sessions/{session_id}/chat` 发送消息，支持流式响应（`stream=true`）；
4. **环境隔离**：每个 session 拥有独立上下文与工具访问权限，可通过 `context` 字段注入初始变量（[Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)）。

CLI 方式亦受支持，详见 [使用 CLI](../../raw/application-user-guide/managed-agents/managed-agents-cli.md)。

## 限制和注意事项

- 单个 agent 最多绑定 10 个工具；单次请求最多触发 5 次工具调用；
- session 生命周期内不支持动态切换模型或更新 tools 配置；
- 所有 HTTP 工具调用默认启用 TLS 验证，不支持自签名证书；
- 计费按实际 token 数 + 工具调用次数 + 会话时长（分钟）叠加计算（[计费](../../raw/application-user-guide/managed-agents/managed-agents-billing.md)）；
- 超时或中断的 session 不自动释放资源，需显式调用 `DELETE /v1/agents/{id}/sessions/{sid}` 清理。

## 来源文档

- [Managed Agents](../../raw/application-user-guide/managed-agents.md)


