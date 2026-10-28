# flow agent api

Flow Agent API 是百炼平台提供的面向智能体（Agent）开发的接口集合，分为应用调用类与组件管理类两大类别。前者用于运行已发布的 Flow Agent 应用，后者用于管理 Prompt 模板、[长期记忆](../concepts/long-term-memory.md)等底层组件。两类接口在鉴权方式、Endpoint 和响应结构上存在显著差异，开发者需严格区分使用场景。

## 支持的模型/功能

- **应用调用功能**：支持通过 DashScope 应用网关调用已发布的智能体应用与工作流应用，适用于对话推理、任务编排等运行时场景。
- **组件管理功能**：提供完整的[长期记忆](../concepts/long-term-memory.md)（Long-term Memory）生命周期管理能力，包括创建、查询、更新、删除[长期记忆](../concepts/long-term-memory.md)体（`Memory`）及其下属的记忆片段（`MemoryNode`）。该能力当前以 [长期记忆（旧）](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-long-term-memory.md) 文档体系为主，覆盖 `CreateMemory`、`ListMemories`、`GetMemoryNode` 等共 10 个核心接口。
- > **注意**：文档中多次提及“长期记忆体尚不支持存储与管理用户画像”，且明确要求“通过控制台进行相关操作”[CreateMemory - 创建长期记忆体](../../raw/_short/api-bailian-2023-12-29-creatememory-71d9eb60188e5ed4.md)，表明该 API 不具备用户画像建模能力，不可用于替代用户中心服务。

## 关键参数

- `workspaceId`：所有组件类接口（如长期记忆）的必填路径参数，标识业务空间，获取方式见[如何使用业务空间](https://help.aliyun.com/zh/model-studio/use-workspace)。
- `memoryId`：长期记忆体唯一标识，由 `CreateMemory` 接口返回，后续所有 `Memory` 及 `MemoryNode` 操作均需传入。
- `memoryNodeId`：记忆片段唯一标识，由 `CreateMemoryNode` 返回，用于精确操作单个片段。
- `maxResults` / `nextToken`：分页参数，适用于 `ListMemories` 和 `ListMemoryNodes`，`maxResults` 取值范围为 `[1, 50]`，默认 `10`；`nextToken` 为空时表示结果已全部返回。
- `content`：`MemoryNode` 的核心字段，长度限制为 `1–200` 字符，仅支持中文、英文、数字及 `_`, `-`, `.`, `:` 等有限符号。

## 使用方式

- **认证方式分离**：
  - 应用调用接口（如运行智能体）使用 **DashScope API Key**，Header 为 `Authorization: Bearer <your-api-key>`；
  - 组件类接口（含全部长期记忆接口）属于阿里云 OpenAPI，**必须使用 AccessKey 签名（ACS3-HMAC-SHA256）**，不支持 `Bearer` 方式。推荐使用阿里云 SDK 或 [OpenAPI Explorer](https://api.aliyun.com/) 调用，避免手动签名错误 [认证](../../raw/application-api-reference/flow-agent-api/flow-agent-api-authentication.md)。
- **Endpoint 区分**：
  - 应用调用：`https://{workspaceId}.cn-beijing.maas.aliyuncs.com`
  - 组件类（长期记忆等）：`https://bailian.{regionId}.aliyuncs.com`（如 `bailian.cn-beijing.aliyuncs.com`），路径前缀含 `{workspaceId}`，例如 `PUT /{workspaceId}/memories/{memoryId}`。
- **典型流程**：
  1. 调用 `CreateMemory` 获取 `memoryId`；
  2. （可选）调用 `CreateMemoryNode` 向该 `memoryId` 下写入初始记忆；
  3. 在调用智能体应用时，将 `memoryId` 作为参数传入，使 Agent 在推理中引用该长期记忆；
  4. 日常维护使用 `GetMemory`/`ListMemoryNodes` 查询，`UpdateMemoryNode` 修改内容，`DeleteMemory` 彻底清理。

## 限制和注意事项

- **限流策略**：所有长期记忆组件接口（`CreateMemory`、`GetMemory`、`ListMemories` 等）均要求两次请求间隔 **≥ 1 秒**，否则可能触发限流并返回 `429 Too Many Requests` [错误码](../../raw/application-api-reference/flow-agent-api/flow-agent-api-errors.md)。
- **幂等性**：`GetMemory`、`UpdateMemory`、`DeleteMemory`、`ListMemories` 等读写操作均为幂等；但 `CreateMemory` **不具备幂等性**，重复调用将创建多个独立记忆体。
- **错误处理**：
  - 应用调用接口返回标准 `request_id` + 自定义错误码/信息；
  - 组件类接口遵循阿里云 OpenAPI 规范，错误时返回 `Code` 与 `Message` 字段；
  - 常见 HTTP 状态码含义统一：`400`（参数错误）、`401`（凭证无效）、`403`（权限不足）、`404`（资源不存在）、`429`（限流）、`500`（服务异常）。
- > **注意**：文档 2（[长期记忆（旧）](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-long-term-memory.md)）标题含“（旧）”，而其余 10 篇子文档（如 `CreateMemory`）发布日期均为 `2023-12-29`，未见更新标记；结合文档 14 中“长期记忆（旧）”的显式命名，应视为当前稳定但非最新演进版本，新项目需关注平台是否已发布替代方案。

## 来源文档

- [错误码](../../raw/application-api-reference/flow-agent-api/flow-agent-api-errors.md)
- [长期记忆（旧）](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-long-term-memory.md)
- [CreateMemory - 创建长期记忆体](../../raw/_short/api-bailian-2023-12-29-creatememory-71d9eb60188e5ed4.md)
- [GetMemory - 获取长期记忆体](../../raw/_short/api-bailian-2023-12-29-getmemory-93a2074c0e9ce4e8.md)
- [UpdateMemory - 更新长期记忆体](../../raw/_short/api-bailian-2023-12-29-updatememory-b92bc2a2bf604c38.md)
- [DeleteMemory - 删除长期记忆体](../../raw/_short/api-bailian-2023-12-29-deletememory-2e39ced8c987fad3.md)
- [认证](../../raw/application-api-reference/flow-agent-api/flow-agent-api-authentication.md)
- [ListMemories - 获取长期记忆体列表](../../raw/_short/api-bailian-2023-12-29-listmemories-ca86cf5601eec468.md)
- [CreateMemoryNode - 创建记忆片段](../../raw/_short/api-bailian-2023-12-29-creatememorynode-7e5dec47c8bf17cc.md)
- [GetMemoryNode - 获取记忆片段](../../raw/_short/api-bailian-2023-12-29-getmemorynode-c43110862c1879b6.md)
- [DeleteMemoryNode - 删除记忆片段](../../raw/_short/api-bailian-2023-12-29-deletememorynode-21f72ddcbaecd822.md)
- [UpdateMemoryNode - 更新记忆片段](../../raw/_short/api-bailian-2023-12-29-updatememorynode-c71c6bef92b1ecc3.md)
- [ListMemoryNodes - 获取记忆片段列表](../../raw/_short/api-bailian-2023-12-29-listmemorynodes-ec6bee0a62fb4cb8.md)
- [概览](../../raw/application-api-reference/flow-agent-api/flow-agent-api-overview.md)


