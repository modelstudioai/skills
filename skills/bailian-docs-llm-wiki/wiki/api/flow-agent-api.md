# flow agent api

Flow Agent API 是百炼平台提供的两类核心接口集合：一类用于调用已发布的智能体/工作流应用（应用调用接口），另一类用于管理 Prompt 模板、[长期记忆](../concepts/long-term-memory.md)等底层组件（组件类接口）。两类接口在 Base URL、鉴权方式、错误响应格式上均存在显著差异，开发者需严格区分使用场景与调用规范。

## 支持的模型/功能

Flow Agent API 本身不直接提供模型推理能力，而是作为**智能体应用调度与组件管理的控制平面**：

- **应用调用功能**：支持通过 DashScope 应用网关调用已发布的智能体应用与工作流应用，适用于生产环境的端到端对话服务集成。
- **组件管理功能**：提供[长期记忆](../concepts/long-term-memory.md)（旧）全生命周期操作（含创建、读取、更新、删除记忆体及记忆片段），详见 [长期记忆（旧）](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-long-term-memory.md)。该能力基于百炼 OpenAPI（`bailian.{regionId}.aliyuncs.com`），当前**不支持用户画像存储与管理**，相关操作需通过控制台完成。

> **注意**：文档中多次提及“[长期记忆](../concepts/long-term-memory.md)（旧）”，表明该能力已被标记为遗留方案；新项目应优先评估平台推荐的长期记忆替代方案（如向量知识库或新版记忆服务），但本文档范围仅覆盖当前公开的旧版 API。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 来源示例 |
|--------|------|------|------|----------|
| `workspaceId` | string | 是 | 业务空间 ID，所有组件类接口（如长期记忆）均需显式传入，获取方式见[如何使用业务空间](https://help.aliyun.com/zh/model-studio/use-workspace)。应用调用接口的 Base URL 中已嵌入 workspaceId。 | [CreateMemory - 创建长期记忆体](../../raw/_short/api-bailian-2023-12-29-creatememory-71d9eb60188e5ed4.md) |
| `memoryId` | string | 是（部分接口） | 长期记忆体唯一标识，由 `CreateMemory` 接口返回，后续所有对该记忆体的操作（如 `GetMemory`, `UpdateMemoryNode`）均需传入。 | [GetMemory - 获取长期记忆体](../../raw/_short/api-bailian-2023-12-29-getmemory-93a2074c0e9ce4e8.md) |
| `content` | string | 是（`CreateMemoryNode` 等） | 记忆片段内容，长度限制为 1–200 字符，仅支持中文、英文、数字及 `:`, `_`, `.`, `-`。 | [CreateMemoryNode - 创建记忆片段](../../raw/_short/api-bailian-2023-12-29-creatememorynode-7e5dec47c8bf17cc.md) |
| `maxResults` / `nextToken` | integer / string | 否（分页） | 用于 `ListMemories` 和 `ListMemoryNodes` 的分页控制，`maxResults` 取值范围为 `[1, 50]`，默认 `10`。 | [ListMemories - 获取长期记忆体列表](../../raw/_short/api-bailian-2023-12-29-listmemories-ca86cf5601eec468.md) |

## 使用方式

### 1. 鉴权方式（关键区分点）
- **应用调用接口**（如调用智能体）：使用 **API Key** 鉴权，Header 中携带 `Authorization: Bearer <your-api-key>`。API Key 在[控制台](https://bailian.console.aliyun.com/?tab=model#/api-key)创建。
- **组件类接口**（如长期记忆、Prompt 模板）：使用 **AccessKey 签名（ACS3-HMAC-SHA256）**，不支持 `Bearer` 方式。强烈推荐使用阿里云 SDK 或 [OpenAPI Explorer](https://api.aliyun.com/) 自动签名，避免手动计算。

### 2. 典型调用流程（长期记忆）
1. 调用 `CreateMemory` 创建长期记忆体，获取 `memoryId`；
2. （可选）调用 `CreateMemoryNode` 向该记忆体写入具体信息；
3. 调用智能体应用时，在请求 Body 中传入 `memoryId`，使智能体在对话中引用该记忆；
4. 日常维护可通过 `ListMemories` / `ListMemoryNodes` 查询，`UpdateMemory` / `UpdateMemoryNode` 修改，`DeleteMemory` / `DeleteMemoryNode` 清理。

### 3. 错误处理
- **应用调用接口**：错误响应含 `request_id` 字段，便于问题定位；HTTP 状态码含义见 [错误码](../../raw/application-api-reference/flow-agent-api/flow-agent-api-errors.md)。
- **组件类接口**：遵循阿里云 OpenAPI 统一结构，出错时返回 `Code` 和 `Message` 字段。

## 限制和注意事项

- **限流策略**：所有长期记忆类接口（`CreateMemory`, `GetMemory`, `ListMemories`, `CreateMemoryNode` 等）均要求**两次请求间隔至少 1 秒**，否则可能触发限流（HTTP 429）。建议在客户端添加退避逻辑。
- **幂等性**：`GetMemory`, `ListMemories`, `UpdateMemory`, `DeleteMemory` 等读/删/改接口具有幂等性；但 `CreateMemory` **不具备幂等性**，重复调用将创建多个独立记忆体。
- **资源依赖**：`CreateMemoryNode`、`GetMemoryNode` 等接口必须依赖有效的 `memoryId`；若 `memoryId` 不存在或无权限，将返回 `404 Memory.MemoryIdNotFound` 错误。
- **路径与域名分离**：应用调用接口 Base URL 为 `https://{workspaceId}.cn-beijing.maas.aliyuncs.com`；组件类接口 Base URL 为 `https://bailian.{regionId}.aliyuncs.com`（如 `bailian.cn-beijing.aliyuncs.com`），二者不可混用。

## 来源文档

- [概览](../../raw/application-api-reference/flow-agent-api/flow-agent-api-overview.md)
- [错误码](../../raw/application-api-reference/flow-agent-api/flow-agent-api-errors.md)
- [长期记忆（旧）](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-long-term-memory.md)
- [CreateMemory - 创建长期记忆体](../../raw/_short/api-bailian-2023-12-29-creatememory-71d9eb60188e5ed4.md)
- [GetMemory - 获取长期记忆体](../../raw/_short/api-bailian-2023-12-29-getmemory-93a2074c0e9ce4e8.md)
- [认证](../../raw/application-api-reference/flow-agent-api/flow-agent-api-authentication.md)
- [ListMemories - 获取长期记忆体列表](../../raw/_short/api-bailian-2023-12-29-listmemories-ca86cf5601eec468.md)
- [CreateMemoryNode - 创建记忆片段](../../raw/_short/api-bailian-2023-12-29-creatememorynode-7e5dec47c8bf17cc.md)
- [GetMemoryNode - 获取记忆片段](../../raw/_short/api-bailian-2023-12-29-getmemorynode-c43110862c1879b6.md)
- [UpdateMemoryNode - 更新记忆片段](../../raw/_short/api-bailian-2023-12-29-updatememorynode-c71c6bef92b1ecc3.md)
- [DeleteMemoryNode - 删除记忆片段](../../raw/_short/api-bailian-2023-12-29-deletememorynode-21f72ddcbaecd822.md)
- [ListMemoryNodes - 获取记忆片段列表](../../raw/_short/api-bailian-2023-12-29-listmemorynodes-ec6bee0a62fb4cb8.md)
- [UpdateMemory - 更新长期记忆体](../../raw/_short/api-bailian-2023-12-29-updatememory-b92bc2a2bf604c38.md)
- [DeleteMemory - 删除长期记忆体](../../raw/_short/api-bailian-2023-12-29-deletememory-2e39ced8c987fad3.md)


