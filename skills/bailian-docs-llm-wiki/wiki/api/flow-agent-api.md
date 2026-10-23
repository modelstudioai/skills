# flow agent api

Flow Agent API 是百炼平台提供的两类核心接口集合：一类用于调用已发布的智能体/工作流应用（通过 DashScope 应用网关），另一类用于管理 Flow Agent 组件（如 Prompt 模板、[长期记忆](../concepts/long-term-memory.md)等，通过百炼 OpenAPI）。两类接口在鉴权方式、Base URL、错误响应格式上均不相同，开发者需严格区分使用场景与调用规范。

## 支持的模型/功能

Flow Agent API **本身不直接提供模型推理能力**，而是面向智能体编排与状态管理。其核心功能分为两类：

- **应用调用功能**：支持调用已发布的工作流应用或智能体应用，实现端到端对话交互。该能力依赖于后台配置的模型（如 Qwen 系列、Qwen-VL 等），但模型选择由应用发布时确定，API 调用时不暴露模型参数。
- **组件管理功能**：当前主要覆盖**[长期记忆](../concepts/long-term-memory.md)（旧）**，包括记忆体（Memory）和记忆片段（MemoryNode）的全生命周期操作（创建、读取、更新、删除、列表查询）。[长期记忆（旧）](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-long-term-memory.md) 文档明确列出全部 10 个相关接口，是当前唯一完整支持的组件类能力。Prompt 模板等其他组件虽在[概览](../../raw/application-api-reference/flow-agent-api/flow-agent-api-overview.md)中提及，但未提供具体接口文档，暂不可用。

> **注意**：文档 4 中标题为“[长期记忆](../concepts/long-term-memory.md)（旧）”，且文档 5 明确说明“长期记忆体尚不支持存储与管理用户画像，请您通过控制台进行相关操作”。这表明该能力已被标记为遗留方案，新项目应关注后续替代方案（如新版长期记忆或知识库集成），但当前 API 仍为唯一可用的记忆管理接口。

## 关键参数

两类接口的关键参数差异显著：

- **应用调用接口**（DashScope 网关）：
  - `workspaceId`：路径参数，标识应用所属工作空间，构成 Base URL 的子域（如 `https://{workspaceId}.cn-beijing.maas.aliyuncs.com`）。
  - `appId`：请求体或路径参数（依具体接口而定），指定被调用的应用 ID。
  - `input`：JSON 对象，包含用户输入消息（`messages` 数组）及可选上下文（如 `memoryId`）。

- **组件类接口**（百炼 OpenAPI，如长期记忆）：
  - `workspaceId`：路径参数，必需，标识业务空间。
  - `memoryId` / `memoryNodeId`：路径参数，必需，用于定位具体资源（见 [CreateMemory - 创建长期记忆体](../../raw/_short/api-bailian-2023-12-29-creatememory-71d9eb60188e5ed4.md) 和 [CreateMemoryNode - 创建记忆片段](../../raw/_short/api-bailian-2023-12-29-creatememorynode-7e5dec47c8bf17cc.md)）。
  - `maxResults` / `nextToken`：分页参数，仅 `ListMemories` 和 `ListMemoryNodes` 接口支持（见 [ListMemories - 获取长期记忆体列表](../../raw/_short/api-bailian-2023-12-29-listmemories-ca86cf5601eec468.md)）。
  - `content`：`CreateMemoryNode` 和 `UpdateMemoryNode` 的必需请求体字段，长度限制为 1–200 字符。

## 使用方式

### 1. 鉴权方式（必须区分）
- **应用调用接口**：使用阿里云百炼 API Key，通过 `Authorization: Bearer <your-api-key>` 头传递。API Key 在[控制台](https://bailian.console.aliyun.com/?tab=model#/api-key)创建。
- **组件类接口**（如长期记忆）：使用阿里云 AccessKey 进行 `ACS3-HMAC-SHA256` 签名，**不支持** `Bearer` 方式。强烈推荐使用阿里云官方 SDK 或 [OpenAPI Explorer](https://api.aliyun.com/) 自动生成签名与调用代码。

### 2. 基础调用流程（以长期记忆为例）
1. 调用 `CreateMemory` 获取 `memoryId`；
2. （可选）调用 `CreateMemoryNode` 向该 `memoryId` 下添加记忆片段；
3. 调用智能体应用时，在请求体中传入 `"memoryId": "<memoryId>"`，使智能体在本次会话中引用该长期记忆；
4. 日常维护可通过 `GetMemory`、`UpdateMemory`、`ListMemories` 等接口操作。

### 3. 错误处理
- **应用调用接口**：错误响应含 `code`、`message` 和 `request_id` 字段，HTTP 状态码含义见[错误码](../../raw/application-api-reference/flow-agent-api/flow-agent-api-errors.md)。
- **组件类接口**：遵循阿里云 OpenAPI 标准，错误时返回 `Code` 和 `Message` 字段，HTTP 状态码规则一致（如 401=凭证无效，429=限流）。

## 限制和注意事项

- **限流策略**：所有长期记忆组件接口（`CreateMemory`、`GetMemory` 等）均要求两次请求间隔 **≥ 1 秒**，否则可能触发限流（HTTP 429），需主动退避重试（见文档 5–14 的“限流说明”）。
- **幂等性**：`GetMemory`、`UpdateMemory`、`DeleteMemory`、`ListMemories`、`ListMemoryNodes` 等读写操作均声明为幂等；但 `CreateMemory` **不具备幂等性**，重复调用将创建多个独立记忆体（见文档 5）。
- **资源依赖**：`CreateMemoryNode` 等操作必须传入有效的 `memoryId`，否则返回 `Memory.MemoryIdNotFound`（404）；同理，操作 `memoryNodeId` 前需确保其所属 `memoryId` 存在且未被删除。
- **功能边界**：长期记忆仅支持结构化文本片段存储，**不支持**用户画像、文件上传、向量检索等高级能力（见文档 5 说明）。所有记忆操作均为显式调用，智能体不会自动学习或更新记忆，需开发者主动管理。
- **路径与域名**：务必使用正确的 Base URL —— 应用调用走 `https://{workspaceId}.cn-beijing.maas.aliyuncs.com`，组件类接口走 `https://bailian.{regionId}.aliyuncs.com`（如 `bailian.cn-beijing.aliyuncs.com`），混用将导致 404 或鉴权失败。

## 来源文档

- [概览](../../raw/application-api-reference/flow-agent-api/flow-agent-api-overview.md)
- [认证](../../raw/application-api-reference/flow-agent-api/flow-agent-api-authentication.md)
- [错误码](../../raw/application-api-reference/flow-agent-api/flow-agent-api-errors.md)
- [长期记忆（旧）](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-long-term-memory.md)
- [CreateMemory - 创建长期记忆体](../../raw/_short/api-bailian-2023-12-29-creatememory-71d9eb60188e5ed4.md)
- [GetMemory - 获取长期记忆体](../../raw/_short/api-bailian-2023-12-29-getmemory-93a2074c0e9ce4e8.md)
- [UpdateMemory - 更新长期记忆体](../../raw/_short/api-bailian-2023-12-29-updatememory-b92bc2a2bf604c38.md)
- [DeleteMemory - 删除长期记忆体](../../raw/_short/api-bailian-2023-12-29-deletememory-2e39ced8c987fad3.md)
- [ListMemories - 获取长期记忆体列表](../../raw/_short/api-bailian-2023-12-29-listmemories-ca86cf5601eec468.md)
- [CreateMemoryNode - 创建记忆片段](../../raw/_short/api-bailian-2023-12-29-creatememorynode-7e5dec47c8bf17cc.md)
- [UpdateMemoryNode - 更新记忆片段](../../raw/_short/api-bailian-2023-12-29-updatememorynode-c71c6bef92b1ecc3.md)
- [ListMemoryNodes - 获取记忆片段列表](../../raw/_short/api-bailian-2023-12-29-listmemorynodes-ec6bee0a62fb4cb8.md)
- [GetMemoryNode - 获取记忆片段](../../raw/_short/api-bailian-2023-12-29-getmemorynode-c43110862c1879b6.md)
- [DeleteMemoryNode - 删除记忆片段](../../raw/_short/api-bailian-2023-12-29-deletememorynode-21f72ddcbaecd822.md)


