# agent context

agent context 是百炼平台中用于定义 Agent 运行时环境与外部信息输入的关键机制，它决定了 Agent 能够感知和利用哪些上下文数据（如知识库、历史对话、外部系统连接等）。该机制通过结构化参数注入实现，直接影响 Agent 的推理准确性与任务执行能力。其设计兼顾灵活性与可控性，支持开发者按需组合多种上下文源。

## 支持的模型/功能

当前 agent context 机制在以下模型与功能中可用：
- 所有支持 `agent` 模式调用的百炼大模型（包括 Qwen-Max、Qwen-Plus、Qwen-Turbo）；
- RAG 增强型 Agent（依赖 [RAG](../../raw/application-user-guide/knowledge-base.md) 模块）；
- 具备[长期记忆](../concepts/long-term-memory.md)能力的 Agent（依赖 [Memory](../../raw/application-user-guide/agent-context/memory-library-overview.md) 库）；
- 集成第三方系统的 Connector Agent（依赖 [Connector](../../raw/application-user-guide/agent-context/overview.md) 框架）；
- 使用 ParseX 进行非结构化内容解析的上下文预处理场景（见 [ParseX](../../raw/application-user-guide/agent-context/getting-started-overview.md)）。

> **注意**：Qwen-Turbo 的 agent context 最大 token 限制为 8192，而 Qwen-Max 和 Qwen-Plus 在 v3.2+ 版本中已支持 up to 32768；旧版文档未明确区分，需以控制台模型详情页实际配置为准。

## 关键参数

调用时需在 `messages` 或 `tools` 请求体中显式传入 `context` 字段（类型为 `object`），主要子字段包括：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `knowledge_base_ids` | `string[]` | 否 | 关联的知识库 ID 列表，触发 RAG 检索 |
| `memory_id` | `string` | 否 | 指定 memory 实例 ID，启用对话历史回溯 |
| `connector_config` | `object` | 否 | Connector 认证与调用配置，格式由 connector 类型决定 |
| `parsex_config` | `object` | 否 | ParseX 解析规则（如 `file_type`, `chunk_size`），仅当启用 ParseX 预处理时有效 |

所有参数均不自动继承，必须显式声明；空对象 `{}` 不等价于省略该字段。

## 使用方式

1. **API 调用示例（JSON）**：
   ```json
   {
     "model": "qwen-max",
     "messages": [{"role": "user", "content": "帮我查一下上季度销售报告"}],
     "context": {
       "knowledge_base_ids": ["kb-abc123"],
       "memory_id": "mem-def456",
       "connector_config": {"type": "notion", "page_id": "xxx"}
     }
   }
   ```

2. **SDK 调用（Python）**：
   ```python
   client.chat.completions.create(
       model="qwen-plus",
       messages=[{"role": "user", "content": "总结会议纪要"}],
       context={
           "knowledge_base_ids": ["kb-789"],
           "parsex_config": {"file_type": "pdf", "chunk_size": 512}
       }
   )
   ```

3. 多上下文源可同时启用，但需确保各模块已正确授权并处于启用状态（参见 [Connector](../../raw/application-user-guide/agent-context/overview.md) 和 [Memory](../../raw/application-user-guide/agent-context/memory-library-overview.md) 文档）。

## 限制和注意事项

- 单次请求中 `context` 总大小（含嵌套 JSON 序列化后）不得超过 2MB；
- `knowledge_base_ids` 中每个知识库须已发布且对当前 API Key 可见；
- `memory_id` 对应的 memory 实例必须由同一用户创建，跨账号不可共享；
- 若同时启用 RAG 与 ParseX，系统默认先执行 ParseX 解析，再将结果注入 RAG 检索流程（详见 [ParseX](../../raw/application-user-guide/agent-context/getting-started-overview.md)）；
- 当前不支持在流式响应（`stream: true`）中动态更新 `context` 字段，变更需发起新请求。

## 来源文档

- [Agent 上下文](../../raw/application-user-guide/agent-context.md)


