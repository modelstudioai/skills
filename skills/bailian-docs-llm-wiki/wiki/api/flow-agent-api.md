# flow agent api

Flow Agent API 是百炼平台面向智能体（Agent）应用开发提供的核心接口集合，分为两类：一类是通过 DashScope 应用网关调用已发布的智能体/工作流应用的**应用调用接口**；另一类是管理 Prompt 模板、[长期记忆](../concepts/long-term-memory.md)等组件的**OpenAPI 组件类接口**。两类接口在鉴权方式、Base URL、错误响应格式上均不同，开发者需严格区分使用场景。

## 支持的模型/功能

- **应用调用能力**：支持调用已发布的智能体应用（Agent App）与工作流应用（Workflow App），底层可对接百炼托管的多种大模型（如 Qwen 系列），具体模型能力由应用配置决定，不直接暴露模型选择参数。
- **[长期记忆](../concepts/long-term-memory.md)（Long-term Memory）管理**：提供完整的 CRUD 接口，包括 `CreateMemory`、`GetMemory`、`UpdateMemory`、`DeleteMemory` 和 `ListMemories`，以及记忆片段（MemoryNode）的 `CreateMemoryNode` 等 10 个操作 [长期记忆（旧）](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-long-term-memory.md)。> **注意**：文档 1 明确指出“[长期记忆](../concepts/long-term-memory.md)（旧）”为历史命名，当前功能已稳定，但控制台侧用户画像类记忆仍需人工配置，API 不支持 [概览](../../raw/application-api-reference/flow-agent-api/flow-agent-api-overview.md)。
- **其他组件**：Prompt 模板等能力通过百炼 OpenAPI 提供，但本文档聚焦 Flow Agent 相关接口，模板类接口不在本范围。

## 关键参数

- **通用路径参数**：
  - `workspaceId`：业务空间 ID，所有组件类接口（长期记忆等）必需，获取方式见[如何使用业务空间](https://help.aliyun.com/zh/model-studio/use-workspace)。
- **长期记忆相关参数**：
  - `memoryId`：由 `CreateMemory` 返回，用于所有后续 Memory 操作（如 `GetMemory`、`CreateMemoryNode`），必须妥善持久化。
  - `memoryNodeId`：由 `CreateMemoryNode` 返回，用于 MemoryNode 的读写删操作。
  - `description`（Memory 级）：长度 1–50 字符，支持中英文、数字及 `:`, `_`, `.`, `-`。
  - `content`（MemoryNode 级）：长度 1–200 字符，同上字符集限制。
- **分页参数（List 接口）**：
  - `maxResults`：每页最大条数，取值范围 `[1, 50]`，默认 `10`。
  - `nextToken`：分页凭证，首次请求不传；后续请求需传入上一次响应中的 `nextToken` 值。

## 使用方式

- **应用调用接口**：
  - Base URL：`https://{workspaceId}.cn-beijing.maas.aliyuncs.com`
  - 鉴权：使用百炼 API Key，Header 中携带 `Authorization: Bearer <your-api-key>` [认证](../../raw/application-api-reference/flow-agent-api/flow-agent-api-authentication.md)。
- **组件类接口（长期记忆等）**：
  - Base URL：`https://bailian.{regionId}.aliyuncs.com`（如 `bailian.cn-beijing.aliyuncs.com`）
  - 鉴权：**必须**使用阿里云 AccessKey 签名（ACS3-HMAC-SHA256），不支持 `Bearer` [Token](../concepts/token.md)；强烈推荐使用阿里云官方 SDK 或 [OpenAPI Explorer](https://api.aliyun.com/) 自动生成签名与代码 [认证](../../raw/application-api-reference/flow-agent-api/flow-agent-api-authentication.md)。
- **典型流程**：
  1. 调用 `CreateMemory` 创建长期记忆体，获取 `memoryId`；
  2. （可选）调用 `CreateMemoryNode` 向该记忆体注入初始知识；
  3. 调用智能体应用时，在请求 payload 中传入 `memoryId`，使 Agent 在对话中引用该记忆；
  4. 按需调用 `ListMemoryNodes`、`UpdateMemoryNode` 等维护记忆内容。

## 限制和注意事项

- **限流策略**：所有长期记忆类接口（`CreateMemory`、`ListMemories` 等）均要求两次请求间隔 ≥ 1 秒，否则可能触发限流并返回 `429` 错误 [CreateMemory - 创建长期记忆体](../../raw/_short/api-bailian-2023-12-29-creatememory-71d9eb60188e5ed4.md)。
- **幂等性**：`CreateMemory` **不具备幂等性**；而 `UpdateMemory`、`GetMemory`、`DeleteMemory`、`ListMemories` 及所有 MemoryNode 接口均具备幂等性 [UpdateMemory - 更新长期记忆体](../../raw/_short/api-bailian-2023-12-29-updatememory-b92bc2a2bf604c38.md)。
- **错误处理**：
  - 应用调用接口错误响应含 `request_id`，便于排查；
  - 组件类接口遵循阿里云 OpenAPI 标准，错误时返回 `Code` 和 `Message` 字段 [错误码](../../raw/application-api-reference/flow-agent-api/flow-agent-api-errors.md)。
- **关键约束**：
  - `DeleteMemory` 为**永久删除**，不可恢复，且会级联删除其下所有 `MemoryNode`；
  - `description` 和 `content` 参数对 Unicode 字符有明确限制，超长或含非法字符将返回 `400 Memory.DescriptionInvalid` 或 `400 Memory.MemoryNodeContentInvalid`；
  - 所有 `memoryId` / `memoryNodeId` 必须真实存在且授权，否则返回 `404 Memory.MemoryIdNotFound`。

## 来源文档

- [概览](../../raw/application-api-reference/flow-agent-api/flow-agent-api-overview.md)
- [认证](../../raw/application-api-reference/flow-agent-api/flow-agent-api-authentication.md)
- [错误码](../../raw/application-api-reference/flow-agent-api/flow-agent-api-errors.md)
- [CreateMemory - 创建长期记忆体](../../raw/_short/api-bailian-2023-12-29-creatememory-71d9eb60188e5ed4.md)
- [UpdateMemory - 更新长期记忆体](../../raw/_short/api-bailian-2023-12-29-updatememory-b92bc2a2bf604c38.md)
- [GetMemory - 获取长期记忆体](../../raw/_short/api-bailian-2023-12-29-getmemory-93a2074c0e9ce4e8.md)
- [DeleteMemory - 删除长期记忆体](../../raw/_short/api-bailian-2023-12-29-deletememory-2e39ced8c987fad3.md)
- [ListMemories - 获取长期记忆体列表](../../raw/_short/api-bailian-2023-12-29-listmemories-ca86cf5601eec468.md)
- [CreateMemoryNode - 创建记忆片段](../../raw/_short/api-bailian-2023-12-29-creatememorynode-7e5dec47c8bf17cc.md)
- [GetMemoryNode - 获取记忆片段](../../raw/_short/api-bailian-2023-12-29-getmemorynode-c43110862c1879b6.md)
- [UpdateMemoryNode - 更新记忆片段](../../raw/_short/api-bailian-2023-12-29-updatememorynode-c71c6bef92b1ecc3.md)
- [DeleteMemoryNode - 删除记忆片段](../../raw/_short/api-bailian-2023-12-29-deletememorynode-21f72ddcbaecd822.md)
- [ListMemoryNodes - 获取记忆片段列表](../../raw/_short/api-bailian-2023-12-29-listmemorynodes-ec6bee0a62fb4cb8.md)
- [长期记忆（旧）](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-long-term-memory.md)


