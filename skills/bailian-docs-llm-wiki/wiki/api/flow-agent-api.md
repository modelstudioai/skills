# flow agent api

Flow Agent API 是百炼平台提供的两类核心接口集合：一类用于调用已发布的智能体/工作流应用（通过 DashScope 应用网关），另一类用于管理 Flow Agent 组件（如 Prompt 模板、长期记忆等，通过百炼 OpenAPI）。两类接口在鉴权方式、Base URL、错误响应格式上均不同，开发者需严格区分使用场景与调用规范。

## 支持的模型/功能

- **应用调用功能**：支持通过 `https://{workspaceId}.cn-beijing.maas.aliyuncs.com` 调用已发布的智能体应用与工作流应用，适用于终端用户交互或业务系统集成。  
- **组件管理功能**：提供完整的长期记忆（Long-term Memory）生命周期管理能力，包括创建/获取/更新/删除长期记忆体（Memory）及其下属的记忆片段（MemoryNode），详见 [长期记忆（旧）](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-long-term-memory.md)。  
  > **注意**：文档明确标注该能力为“（旧）”，且说明“长期记忆体尚不支持存储与管理用户画像，请您通过控制台进行相关操作”[CreateMemory - 创建长期记忆体](../../raw/_short/api-bailian-2023-12-29-creatememory-71d9eb60188e5ed4.md)，表明该组件已进入维护期，新项目应优先评估控制台或其他替代方案。

## 关键参数

- **`workspaceId`**：所有组件类接口（如长期记忆）必需，标识业务空间，获取方式见[如何使用业务空间](https://help.aliyun.com/zh/model-studio/use-workspace)。  
- **`memoryId`**：长期记忆体唯一标识，由 `CreateMemory` 返回，后续所有 Memory 相关操作（如 `GetMemory`, `ListMemoryNodes`）均需传入。  
- **`memoryNodeId`**：记忆片段唯一标识，由 `CreateMemoryNode` 返回，用于精确操作单个记忆片段。  
- **分页参数（`maxResults`, `nextToken`）**：适用于 `ListMemories` 和 `ListMemoryNodes`，`maxResults` 取值范围为 `[1, 50]`，默认 `10`；`nextToken` 为空时表示结果已全部返回。

## 使用方式

- **应用调用接口**：使用阿里云百炼 API Key 鉴权，Header 中携带 `Authorization: Bearer <your-api-key>`，Base URL 为 `https://{workspaceId}.cn-beijing.maas.aliyuncs.com`。  
- **组件类接口（如长期记忆）**：属于阿里云 OpenAPI，**必须使用 AccessKey 签名（ACS3-HMAC-SHA256）**，不支持 `Bearer` 方式；推荐直接使用阿里云 SDK 或 [OpenAPI Explorer](https://api.aliyun.com/) 调试与生成代码，避免手动签名。  
  > **注意**：文档 2 明确指出两类接口鉴权方式不同，且组件类接口“不支持 `Authorization: Bearer` 方式”[认证](../../raw/application-api-reference/flow-agent-api/flow-agent-api-authentication.md)，若混用将导致 `401 Unauthorized` 错误。

## 限制和注意事项

- **限流策略**：所有长期记忆相关接口（`CreateMemory`, `GetMemory`, `UpdateMemory`, `DeleteMemory`, `ListMemories`, 以及所有 `*MemoryNode` 接口）均要求两次请求间隔 **至少 1 秒**，否则可能触发限流并返回 `429 Too Many Requests`。  
- **幂等性**：`GetMemory`, `UpdateMemory`, `DeleteMemory`, `ListMemories` 具有幂等性；但 `CreateMemory` **不具备幂等性**，重复调用将创建多个独立的长期记忆体。  
- **错误处理**：应用调用接口返回 `request_id` 便于问题定位；组件类接口遵循阿里云 OpenAPI 统一结构，错误信息在 `Code` 与 `Message` 字段中。常见状态码含义见 [错误码](../../raw/application-api-reference/flow-agent-api/flow-agent-api-errors.md)。  
- **资源清理**：`DeleteMemory` 为**永久性删除**，连同其下所有 `MemoryNode` 一并清除，不可恢复，调用前须谨慎确认。

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
- [GetMemoryNode - 获取记忆片段](../../raw/_short/api-bailian-2023-12-29-getmemorynode-c43110862c1879b6.md)
- [UpdateMemoryNode - 更新记忆片段](../../raw/_short/api-bailian-2023-12-29-updatememorynode-c71c6bef92b1ecc3.md)
- [DeleteMemoryNode - 删除记忆片段](../../raw/_short/api-bailian-2023-12-29-deletememorynode-21f72ddcbaecd822.md)
- [ListMemoryNodes - 获取记忆片段列表](../../raw/_short/api-bailian-2023-12-29-listmemorynodes-ec6bee0a62fb4cb8.md)


