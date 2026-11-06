# managed agents api

Managed Agents API 是百炼平台提供的用于构建、部署和管理可编程智能体（Agent）的 RESTful 接口集合，支持环境隔离、会话状态管理、技能编排、文件与记忆存储等核心能力。该 API 采用标准 HTTP 协议，需通过 Bearer [Token](../concepts/token.md) 认证，适用于需要细粒度控制 Agent 生命周期与运行时行为的开发者场景。完整功能覆盖从开发调试到生产部署的全链路需求。

## 支持的模型与功能

Managed Agents API **不直接调用大模型**，而是提供对 Agent 运行时基础设施的编排能力；底层模型由用户在 `Agent` 配置中指定（如 `qwen-max`、`qwen-plus` 等），并受 [Managed Agent API 概览](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md) 中定义的模型兼容性约束。支持的核心功能包括：  
- Agent 实例的创建、更新与生命周期管理（含 `status` 查询与强制终止）  
- 独立 `Environment` 隔离（支持多租户、多版本配置）  
- 基于 `Session` 的有状态交互与事件流订阅（`event_type=agent_step`, `agent_finished`）  
- 文件上传/引用（`files-api`）、[长期记忆](../concepts/long-term-memory.md)存储（`memory-store-api`）及密钥安全托管（`vault-api`, `credential-api`）  
- 技能（Skill）注册与组合调用，支持自定义工具函数注入  

> **注意**：原始文档中 `skills-api.md` 描述的“动态技能热加载”能力在 v2.3+ 版本中已被弃用，实际应通过 `Agent` 配置中的 `tools` 字段静态声明，详见 [Agent API](../../raw/application-api-reference/managed-agents-api/agent-api.md)。

## 关键参数

所有写操作（如 `POST /v1/agents`, `PUT /v1/sessions/{id}`）均需以下通用参数：  
- `Authorization: Bearer <token>`（认证方式见 [Managed Agents API 认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-authentication.md)）  
- `x-bailian-region`: 指定资源所在地域（如 `cn-beijing`），必需且影响 `Environment` 和 `Vault` 的可见范围  
- `Content-Type: application/json`  
- 请求体中关键字段示例：  
  - `agent_id`（创建时可选，系统生成；后续操作必需）  
  - `session_id`（`Session` 相关接口必需，长度 ≤ 64 字符，仅支持字母、数字、下划线）  
  - `memory_store_id`（若启用记忆，需提前通过 `memory-store-api` 创建）  

## 使用方式

1. **快速验证**：参考 [Managed Agents 快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)，使用 `curl` 调用 `/v1/agents` 创建最小 Agent 并发起首次会话。  
2. **生产集成**：建议基于 `Deployment` API 发布稳定版本，并通过 `Webhook` API 接收异步事件（如 `agent_finished`），避免轮询。  
3. **调试辅助**：利用 `Session` API 的 `?include_events=true` 参数获取完整执行轨迹，结合 `Environment` 的 `debug_mode: true` 启用详细日志输出。

## 限制和注意事项

- 单个 `Environment` 下最多创建 100 个 `Agent`；单个 `Session` 最长存活 24 小时（超时自动清理）。  
- `File` API 上传单文件上限为 100 MB，且仅支持 `text/plain`, `application/pdf`, `image/*` 等白名单 MIME 类型。  
- `Memory Store` 的 `key` 长度限制为 256 字符，`value` 不超过 1 MB；高频读写需自行实现客户端缓存。  
- 所有 API 均遵循 429 限流策略（默认 100 QPS / 租户），突发流量需配合 `retry-after` 响应头重试。  
- `Credential` API 存储的敏感信息**不可被 Agent 运行时直接读取**，必须通过 `Vault` 绑定后以 `{{vault://...}}` 模板语法注入，此行为与 [Vault API 文档](../../raw/application-api-reference/managed-agents-api/vault-api.md) 一致。

## 来源文档

- [Managed Agent API](../../raw/application-api-reference/managed-agents-api.md)


