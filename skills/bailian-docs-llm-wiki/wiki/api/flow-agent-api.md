# flow agent api

Flow Agent API 是百炼平台提供的两类核心接口集合：一类用于调用已发布的智能体/工作流应用（通过 DashScope 应用网关），另一类用于管理 Flow Agent 组件（如[长期记忆](../concepts/long-term-memory.md)、Prompt 模板等，通过百炼 OpenAPI）。两类接口在认证方式、Base URL、错误响应格式上均不同，开发者需严格区分使用场景与调用规范。[概览](../../raw/application-api-reference/flow-agent-api/flow-agent-api-overview.md) 文档明确划分了这两类接口的边界与职责。

## 支持的模型/功能

- **应用调用功能**：支持调用已发布的工作流应用（Workflow App）和智能体应用（Agent App），底层可集成多种大模型（如 Qwen 系列、GLM 等），具体可用模型取决于应用配置，API 层不直接暴露模型选择参数。
- **组件管理功能**：当前主要提供**[长期记忆](../concepts/long-term-memory.md)（旧）** 的全生命周期管理能力，包括创建/查询/更新/删除[长期记忆](../concepts/long-term-memory.md)体（Memory）及其下属的记忆片段（MemoryNode）。该能力属于百炼 OpenAPI 体系，**不支持用户画像存储与管理**（需通过控制台操作）[CreateMemory - 创建长期记忆体](../../raw/_short/api-bailian-2023-12-29-creatememory-71d9eb60188e5ed4.md)。其他组件（如 Prompt 模板）虽在[概览](../../raw/application-api-reference/flow-agent-api/flow-agent-api-overview.md)中提及，但本次文档集未提供其具体接口说明。

> **注意**：文档 4 中标题为“长期记忆（旧）”，且文档 5 明确说明“长期记忆体尚不支持存储与管理用户画像”，表明该能力已被标记为遗留方案，新项目应关注平台后续推出的“长期记忆（新）”或替代机制，当前文档不覆盖新方案。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 来源接口 |
|--------|------|------|------|----------|
| `workspaceId` | string | 是 | 业务空间 ID，所有组件类接口（长期记忆）必需，获取方式见[如何使用业务空间](https://help.aliyun.com/zh/model-studio/use-workspace) | 所有长期记忆接口（如 [CreateMemory](../../raw/_short/api-bailian-2023-12-29-creatememory-71d9eb60188e5ed4.md)） |
| `memoryId` | string | 是（除 ListMemories） | 长期记忆体唯一标识，由 `CreateMemory` 返回，后续所有 Memory 相关操作必需 | `GetMemory`, `UpdateMemory`, `DeleteMemory`, `ListMemoryNodes` 等 |
| `memoryNodeId` | string | 是（除 CreateMemoryNode） | 记忆片段唯一标识，由 `CreateMemoryNode` 返回 | `GetMemoryNode`, `UpdateMemoryNode`, `DeleteMemoryNode` |
| `description` | string | 否 | 长期记忆体描述，1–50 字符，支持中英文、数字及 `:`, `_`, `.`, `-` | `CreateMemory`, `UpdateMemory` |
| `content` | string | 是 | 记忆片段内容，1–200 字符，支持中英文、数字及 `:`, `_`, `.`, `-` | `CreateMemoryNode`, `UpdateMemoryNode` |
| `maxResults` / `nextToken` | integer / string | 否 | 分页参数，`maxResults` 范围 1–50，默认 10；`nextToken` 用于分页续查 | `ListMemories`, `ListMemoryNodes` |

## 使用方式

### 1. 认证方式（关键区分点）
- **应用调用接口**（如调用已发布工作流）：使用 **阿里云百炼 API Key**，Header 中传入 `Authorization: Bearer <your-api-key>`。API Key 在[控制台](https://bailian.console.aliyun.com/?tab=model#/api-key)创建。[认证](../../raw/application-api-reference/flow-agent-api/flow-agent-api-authentication.md) 文档对此有明确说明。
- **组件类接口**（如所有长期记忆 API）：使用 **阿里云 AccessKey 签名（ACS3-HMAC-SHA256）**，**不支持** `Authorization: Bearer`。强烈推荐使用阿里云官方 SDK 或 [OpenAPI Explorer](https://api.aliyun.com/) 自动生成签名与调用代码。

### 2. 基础调用流程（以长期记忆为例）
1. 调用 `POST /{workspaceId}/memories` 创建长期记忆体，获取 `memoryId`；
2. （可选）调用 `POST /{workspaceId}/memories/{memoryId}/memoryNodes` 创建记忆片段，获取 `memoryNodeId`；
3. 在调用智能体应用时，将 `memoryId` 作为参数传入，使智能体在推理中引用该记忆；
4. 日常维护可通过 `GET`/`PUT`/`DELETE` 对 Memory 和 MemoryNode 进行读取、更新、删除。

### 3. 错误处理
- **应用调用接口**：错误响应含 `request_id`，错误码与信息按各接口文档定义；
- **组件类接口**：遵循阿里云 OpenAPI 统一格式，错误时返回 `Code` 与 `Message` 字段。通用 HTTP 状态码含义见[错误码](../../raw/application-api-reference/flow-agent-api/flow-agent-api-errors.md)。

## 限制和注意事项

- **限流策略**：所有长期记忆接口（`CreateMemory`, `UpdateMemory`, `DeleteMemory`, `ListMemories`, `CreateMemoryNode` 等）均要求**两次请求间隔 ≥ 1 秒**，否则可能触发限流（HTTP 429），需重试。
- **幂等性**：`UpdateMemory`、`DeleteMemory`、`ListMemories`、`GetMemory` 等接口声明为幂等；但 `CreateMemory` **不具备幂等性**，重复调用将创建多个独立记忆体。
- **数据一致性**：`DeleteMemory` 为**永久性删除**，连同其下所有 `MemoryNode` 一并清除，不可恢复，请谨慎操作。
- **功能边界**：长期记忆仅用于存储结构化事实信息（如用户偏好、历史决策），**不支持**自动提取、向量化或语义检索；用户画像类数据必须通过控制台管理。
- **路径与域名**：应用调用 Base URL 为 `https://{workspaceId}.cn-beijing.maas.aliyuncs.com`；组件类接口（长期记忆）Base URL 为 `https://bailian.{regionId}.aliyuncs.com`，实际调用需拼接完整路径（如 `/v1/{workspaceId}/memories`）。

## 来源文档

- [概览](../../raw/application-api-reference/flow-agent-api/flow-agent-api-overview.md)
- [认证](../../raw/application-api-reference/flow-agent-api/flow-agent-api-authentication.md)
- [错误码](../../raw/application-api-reference/flow-agent-api/flow-agent-api-errors.md)
- [长期记忆（旧）](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-long-term-memory.md)
- [CreateMemory - 创建长期记忆体](../../raw/_short/api-bailian-2023-12-29-creatememory-71d9eb60188e5ed4.md)
- [UpdateMemory - 更新长期记忆体](../../raw/_short/api-bailian-2023-12-29-updatememory-b92bc2a2bf604c38.md)
- [DeleteMemory - 删除长期记忆体](../../raw/_short/api-bailian-2023-12-29-deletememory-2e39ced8c987fad3.md)
- [CreateMemoryNode - 创建记忆片段](../../raw/_short/api-bailian-2023-12-29-creatememorynode-7e5dec47c8bf17cc.md)
- [ListMemories - 获取长期记忆体列表](../../raw/_short/api-bailian-2023-12-29-listmemories-ca86cf5601eec468.md)
- [UpdateMemoryNode - 更新记忆片段](../../raw/_short/api-bailian-2023-12-29-updatememorynode-c71c6bef92b1ecc3.md)
- [DeleteMemoryNode - 删除记忆片段](../../raw/_short/api-bailian-2023-12-29-deletememorynode-21f72ddcbaecd822.md)
- [ListMemoryNodes - 获取记忆片段列表](../../raw/_short/api-bailian-2023-12-29-listmemorynodes-ec6bee0a62fb4cb8.md)
- [GetMemory - 获取长期记忆体](../../raw/_short/api-bailian-2023-12-29-getmemory-93a2074c0e9ce4e8.md)
- [GetMemoryNode - 获取记忆片段](../../raw/_short/api-bailian-2023-12-29-getmemorynode-c43110862c1879b6.md)


