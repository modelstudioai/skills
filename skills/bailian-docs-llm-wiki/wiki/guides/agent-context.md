# agent context

agent context 是百炼平台中用于定义 Agent 运行时环境与外部信息源的关键机制，它决定了 Agent 能够感知和利用哪些知识、历史交互及外部系统能力。通过 context，开发者可显式注入知识库、记忆片段、连接器配置等结构化上下文数据，从而影响 Agent 的推理与决策行为。其设计目标是解耦业务逻辑与上下文供给，支持灵活、可复用的上下文组合。

## 支持的模型/功能

当前 agent context 机制在所有支持 `agent` 类型调用的模型上可用，包括 Qwen-Max、Qwen-Plus 和 Qwen-Turbo（详见 [Agent 上下文](../../raw/application-user-guide/agent-context.md)）。核心支持的功能包括：
- RAG：接入知识库实现检索增强（参见 [RAG](../../raw/application-user-guide/agent-context/knowledge-base.md)）；
- Memory：加载对话历史或[长期记忆](../concepts/long-term-memory.md)片段；
- Connector：绑定第三方服务（如飞书、钉钉、数据库）的预注册连接器实例；
- ParseX：启用结构化文档解析与上下文注入（见 [ParseX](../../raw/application-user-guide/agent-context/getting-started-overview.md)）。

> **注意**：Qwen-VL 系列多模态模型暂不支持 memory 和 connector 类型 context，仅支持 RAG 和 ParseX；该限制未在 [Agent 上下文](../../raw/application-user-guide/agent-context.md) 中明确说明，以本 Wiki 实际行为为准。

## 关键参数

在 API 请求体中，context 通过 `context` 字段传入，类型为对象，支持以下子字段：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `knowledge_base_ids` | string[] | 否 | 知识库 ID 列表，用于 RAG 检索 |
| `memory_ids` | string[] | 否 | 记忆库 ID 列表，按时间倒序加载最近 N 条交互 |
| `connector_ids` | string[] | 否 | 已配置的 connector 实例 ID 列表 |
| `parsex_config` | object | 否 | ParseX 解析参数，含 `file_id`、`chunk_size` 等（详见 [ParseX](../../raw/application-user-guide/agent-context/getting-started-overview.md)）|

所有 ID 均需为用户空间内已创建并授权的有效资源 ID；空数组或缺失字段将被忽略。

## 使用方式

1. 在控制台或 SDK 中预先创建知识库、记忆库、connector 或上传文件启用 ParseX；
2. 构造请求时，在 `messages` 外层添加 `context` 对象，例如：

```json
{
  "model": "qwen-max",
  "messages": [{"role": "user", "content": "上次我问过什么？"}],
  "context": {
    "memory_ids": ["mem_abc123"],
    "knowledge_base_ids": ["kb_xyz789"]
  }
}
```

3. 注意：context 不参与 token 计费，但其关联内容（如检索结果、解析后文本）会作为 prompt 一部分计入总 token（参考 [Memory](../../raw/application-user-guide/agent-context/memory-library-overview.md) 中的计费说明）。

## 限制和注意事项

- 单次请求最多支持 5 个 `knowledge_base_ids`、3 个 `memory_ids`、3 个 `connector_ids`；
- `parsex_config` 仅支持单个 `file_id`，不支持批量解析；
- context 中引用的资源必须与请求所用 API Key 所属工作空间一致，跨空间 ID 无效；
- 若同时指定 `memory_ids` 和 `knowledge_base_ids`，Agent 默认优先融合记忆上下文，再执行 RAG 检索（此行为与 [Agent 上下文](../../raw/application-user-guide/agent-context.md) 描述一致，但 [Memory](../../raw/application-user-guide/agent-context/memory-library-overview.md) 中未明确融合顺序，建议以实际调用为准）。

## 来源文档

- [Agent 上下文](../../raw/application-user-guide/agent-context.md)


