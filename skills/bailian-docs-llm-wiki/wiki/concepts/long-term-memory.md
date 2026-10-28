# 长期记忆

长期记忆（Long Term Memory, LTM）是百炼平台提供的结构化、持久化记忆管理能力，用于在多轮对话与智能体运行过程中跨请求存储和检索用户事实性信息、行为偏好与上下文锚点。它独立于单次会话生命周期，由平台统一索引与向量检索，为模型提供低延迟、高相关性的上下文增强。

## 在百炼平台的不同场景中，这个概念如何使用

长期记忆在百炼平台中存在**两类并行但隔离的实现路径**，开发者需根据技术栈严格区分：

- **API 调用层（推荐新项目使用）**：通过 `application call` 或 `flow agent api` 的 **应用调用类接口**（如 `/apps/{app_id}/completion`）启用。只需在 `messages` 中嵌入 `memory` 字段（JSON 对象），即可在单次请求中完成写入、更新或删除；模型在生成响应前自动检索匹配记忆并注入上下文。适用于智能体应用、工作流及 OpenAI 兼容模式，无需额外 SDK 或签名。

- **组件管理层（旧版/高级运维场景）**：通过 `flow agent api` 的 **组件类接口**（如 `POST /{workspaceId}/memories`）进行显式生命周期管理。需使用阿里云 AccessKey 签名（ACS3-HMAC-SHA256），调用 `CreateMemory` 获取 `memoryId`，再通过 `CreateMemoryNode` 写入片段。该方式适用于需要精细控制记忆体粒度、批量操作或与 Flow Agent 工作流深度集成的场景，但不支持用户画像建模，且所有接口有 ≥1 秒限流要求。

> ⚠️ 注意：两类路径**完全隔离**——API 调用层写入的记忆无法通过组件层 API 查询，反之亦然；同一 `app_id` 下的长期记忆也**不跨 workspace 共享**。

## 关键参数和配置

### 1. API 调用层（`messages` 内嵌 `memory`）
```json
{
  "role": "user",
  "content": "请记住我的偏好。",
  "memory": {
    "type": "fact",
    "id": "user_birthday_123",
    "content": "用户生日是1992年5月3日",
    "metadata": {
      "source": "user_input",
      "ttl_seconds": 31536000
    }
  }
}
```
- `type`：必填，取值 `"fact"`（可验证事实）、`"profile"`（用户画像标签）、`"generic"`（临时上下文块），影响检索权重与存储策略；
- `id`：必填，全局唯一字符串，重复提交将覆盖旧记录（无版本回溯）；
- `content`：必填，纯文本内容，≤ 2048 字符；
- `metadata.ttl_seconds`：可选整数，指定自动过期时间（最小 3600 秒），超时后不可检索；
- 单次请求最多携带 **5 条 memory 记录**（含 `type: "delete"`），超出部分静默截断；
- `memory` 字段**仅允许出现在 `system` 或 `user` 消息中**，不可置于 `assistant` 消息。

### 2. 组件管理层（OpenAPI 接口）
- `workspaceId`：所有接口必填路径参数，标识业务空间；
- `memoryId`：由 `CreateMemory` 返回，作为后续所有操作的根标识；
- `memoryNodeId`：由 `CreateMemoryNode` 返回，用于精确操作单个记忆片段；
- `content`：`MemoryNode` 核心字段，长度限制为 **1–200 字符**，仅支持 ASCII 字母、数字及 `_`, `-`, `.`, `:`；
- 分页参数：`maxResults`（1–50，默认 10）、`nextToken`（空表示结束）。

## 面向开发者，简洁实用

- ✅ **优先选用 API 调用层**：新项目直接在 `messages` 中传 `memory`，零配置、免签名、自动注入，兼容 DashScope 和 OpenAI Responses API；
- ✅ **敏感信息必须脱敏**：长期记忆基于语义向量检索，**不保证精确关键词匹配**（如身份证号、手机号），写入前务必自行哈希或掩码；
- ✅ **用户画像需显式构造**：当前无自动聚类能力，`type: "profile"` 必须配合 `metadata` 中的明确标签（如 `"interests": ["AI", "travel"]`）；
- ❌ **避免混用两套体系**：不要在同一个应用中既用 `memory` 字段又调用 `CreateMemoryNode`，会导致记忆碎片化且无法协同；
- ⚠️ **容量与性能红线**：
  - 单应用上限：100 万条记录；
  - 单条 `content`：≤ 2048 字符（API 层） / ≤ 200 字符（组件层）；
  - 向量检索对长文本、代码、公式等非自然语言内容效果下降，建议拆分为语义清晰的短句；
- 🔁 **删除操作**：API 层用 `{"type": "delete", "id": "xxx"}`；组件层用 `DeleteMemoryNode` 或 `DeleteMemory`。

> 提示：调试时可通过 `ListMemoryNodes`（组件层）或观察模型生成内容是否包含预期记忆（API 层）快速验证写入是否生效。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [flow agent api](../api/flow-agent-api.md)
- [application call](../api/application-call.md)
- [agent context](../guides/agent-context.md)
- [agent development](../guides/agent-development.md)


