# flow agent api

Flow Agent API 是百炼平台提供的两类核心接口集合：一类是面向应用调用的智能体/工作流执行接口，另一类是面向 Flow Agent 组件管理的 OpenAPI（如 Prompt 模板、[长期记忆](../concepts/long-term-memory.md)等）。两类接口在鉴权方式、Base URL、错误响应格式上均不同，开发者需严格区分使用场景与调用规范。

## 支持的模型/功能

- **应用调用接口**：用于调用已发布的智能体应用或工作流应用，支持流式/非流式响应，底层可对接多种大模型（具体模型由应用配置决定，API 层不暴露模型选择参数）。
- **组件类接口**：提供 Prompt 模板管理、[长期记忆](../concepts/long-term-memory.md)（旧）等能力。其中[长期记忆](../concepts/long-term-memory.md)功能包含完整的 CRUD 操作，覆盖长期记忆体（`Memory`）和记忆片段（`MemoryNode`）两级资源，详见[长期记忆（旧）](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-long-term-memory.md)。> **注意**：文档明确标注该功能为“旧”，且说明“长期记忆体尚不支持存储与管理用户画像，请您通过控制台进行相关操作”，表明其能力已被新机制替代，不建议在新项目中依赖。

## 关键参数

- `workspaceId`：所有组件类接口（如长期记忆）的必需路径参数，标识业务空间，获取方式见[如何使用业务空间](https://help.aliyun.com/zh/model-studio/use-workspace)。
- `memoryId`：长期记忆体唯一标识，由 `CreateMemory` 返回，后续所有 `Memory` 及 `MemoryNode` 操作均需传入。
- `memoryNodeId`：记忆片段唯一标识，由 `CreateMemoryNode` 返回，用于单条记忆的读写删。
- 分页参数（`maxResults`, `nextToken`）：适用于 `ListMemories` 和 `ListMemoryNodes`，`maxResults` 有效范围为 1–50，默认 10；`nextToken` 为空时表示数据已全部返回。
- `description`（`Memory` 级）：长度 1–50 字符，仅支持 Unicode letter 类字符及 `:`, `_`, `.`, `-`。
- `content`（`MemoryNode` 级）：长度 1–200 字符，支持中文、英文、数字及 `:`, `_`, `-`, `.`, `:`。

## 使用方式

1. **鉴权分离**：
   - 应用调用接口：使用阿里云百炼 API Key，Header 中传 `Authorization: Bearer <your-api-key>`，Base URL 为 `https://{workspaceId}.cn-beijing.maas.aliyuncs.com`。
   - 组件类接口（含全部长期记忆 API）：属于阿里云 OpenAPI，**必须使用 AccessKey 签名（ACS3-HMAC-SHA256）**，不支持 `Bearer` 方式；推荐直接使用阿里云 SDK 或 [OpenAPI Explorer](https://api.aliyun.com/) 调试与生成代码，详见[认证](../../raw/application-api-reference/flow-agent-api/flow-agent-api-authentication.md)。

2. **典型流程（长期记忆）**：
   - 调用 `CreateMemory` 获取 `memoryId`；
   - （可选）调用 `CreateMemoryNode` 向该 `memoryId` 下添加记忆片段；
   - 调用智能体应用时，在请求体中传入 `memoryId`，使其在对话中被引用；
   - 日常管理使用 `GetMemory`/`UpdateMemory`/`DeleteMemory` 及对应 `MemoryNode` 接口。

3. **错误处理**：两类接口错误结构不同：
   - 应用调用接口：响应含 `request_id` 与自定义错误码/信息；
   - 组件类接口：遵循阿里云 OpenAPI 标准，出错时返回 `Code` 与 `Message` 字段。常见 HTTP 状态码含义见[错误码](../../raw/application-api-reference/flow-agent-api/flow-agent-api-errors.md)。

## 限制和注意事项

- **限流策略**：所有长期记忆组件接口（`CreateMemory`, `GetMemory`, `UpdateMemory`, `DeleteMemory`, `ListMemories`, `CreateMemoryNode` 等）均要求两次请求间隔 ≥ 1 秒，否则可能触发限流并返回 429。
- **幂等性**：`GetMemory`, `UpdateMemory`, `DeleteMemory`, `ListMemories` 具有幂等性；`CreateMemory` **不具备幂等性**，重复调用将创建多个独立记忆体。
- **功能弃用提示**：长期记忆相关接口明确标记为“（旧）”，且文档指出其不支持用户画像管理，应视为过渡方案。新项目请优先查阅控制台或最新版文档确认替代方案。
- **权限控制**：各组件接口需单独授权 RAM 权限，例如 `sfm:CreateMemory`（Write）、`sfm:ListMemories`（List），详见各接口的[授权信息](../../raw/_short/api-bailian-2023-12-29-creatememory-71d9eb60188e5ed4.md)章节。

## 来源文档

- [认证](../../raw/application-api-reference/flow-agent-api/flow-agent-api-authentication.md)
- [概览](../../raw/application-api-reference/flow-agent-api/flow-agent-api-overview.md)
- [错误码](../../raw/application-api-reference/flow-agent-api/flow-agent-api-errors.md)
- [长期记忆（旧）](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-long-term-memory.md)
- [CreateMemory - 创建长期记忆体](../../raw/_short/api-bailian-2023-12-29-creatememory-71d9eb60188e5ed4.md)
- [GetMemory - 获取长期记忆体](../../raw/_short/api-bailian-2023-12-29-getmemory-93a2074c0e9ce4e8.md)
- [UpdateMemory - 更新长期记忆体](../../raw/_short/api-bailian-2023-12-29-updatememory-b92bc2a2bf604c38.md)
- [CreateMemoryNode - 创建记忆片段](../../raw/_short/api-bailian-2023-12-29-creatememorynode-7e5dec47c8bf17cc.md)
- [DeleteMemory - 删除长期记忆体](../../raw/_short/api-bailian-2023-12-29-deletememory-2e39ced8c987fad3.md)
- [GetMemoryNode - 获取记忆片段](../../raw/_short/api-bailian-2023-12-29-getmemorynode-c43110862c1879b6.md)
- [UpdateMemoryNode - 更新记忆片段](../../raw/_short/api-bailian-2023-12-29-updatememorynode-c71c6bef92b1ecc3.md)
- [DeleteMemoryNode - 删除记忆片段](../../raw/_short/api-bailian-2023-12-29-deletememorynode-21f72ddcbaecd822.md)
- [ListMemoryNodes - 获取记忆片段列表](../../raw/_short/api-bailian-2023-12-29-listmemorynodes-ec6bee0a62fb4cb8.md)
- [ListMemories - 获取长期记忆体列表](../../raw/_short/api-bailian-2023-12-29-listmemories-ca86cf5601eec468.md)


