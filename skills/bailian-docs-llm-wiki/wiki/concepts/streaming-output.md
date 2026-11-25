# 流式输出

流式输出（Streaming Output）是百炼平台提供的一种实时响应机制，允许模型在生成过程中持续分块返回结果（如逐字、逐词或逐 token），而非等待全部内容生成完毕后一次性返回。该机制显著降低用户感知延迟，提升交互自然度，是构建响应式 AI 应用（如聊天界面、实时翻译、代码补全）的关键能力。

## 在百炼平台的不同场景中如何使用

流式输出在以下核心场景中被统一支持，但启用条件与行为细节因服务抽象层而异：

- **基础模型调用（`/v1/chat/completions`）**：所有文本生成模型（`qwen-max`、`qwen-plus`、`qwen-turbo`）均支持 `stream=true`。响应格式为 Server-Sent Events（SSE），每帧包含一个 `delta` 字段（增量内容）和可选的 `finish_reason`。注意：`usage` 统计仅在最终 `data: [DONE]` 帧中返回。

- **Model Experience 统一接口（`/v1/model/experience`）**：作为平台级抽象层，`stream` 是顶层通用参数。但需注意：  
  - ✅ 文本类、语音类（TTS/ASR）模型支持流式；  
  - ❌ 视觉生成类（图像/视频）及全模态（Omni-modal）模型**不支持**流式，设置 `stream=true` 将返回错误。

- **Knowledge Base（RAG）问答（`/v1/rag/qa`）**：知识库问答服务原生支持流式，启用后可在检索完成即开始生成回答，实现“边查边答”。流式响应中自动嵌入引用溯源标记（如 `[1]`），便于前端高亮来源切片。

- **Prompt 调试与应用集成**：通过 `/v1/chat/completions` 接口提交 [prompt](../guides/prompt.md) 时，`stream=true` 同样生效；在 Agent 或 RAG 增强应用中，流式输出可与插件调用、多轮状态管理无缝衔接。

- **增量式优化（`incremental_output=true`）**：当 `stream=true` 时，额外启用该参数可确保每帧仅返回**本次新增内容**（非全量重发），避免前端重复渲染，推荐在 Web UI 场景中启用。

## 关键参数和配置

| 参数名 | 类型 | 说明 | 默认值 | 注意事项 |
|--------|------|------|--------|----------|
| `stream` | boolean | 启用流式响应（SSE 格式） | `false` | 必须显式设为 `true` 才生效；不支持的模型将报错（如 `qwen-vl-plus`） |
| `incremental_output` | boolean | 在流式下启用增量输出（仅返回新生成 token） | `false` | 非标准 OpenAI 字段，百炼特有；需与 `stream=true` 同时使用才有效 |
| `model` | string | 模型 ID 必须支持流式（见[模型能力矩阵](../../raw/models/capabilities.md)） | — | `qwen-turbo` 支持，`qwen-vl-plus` 不支持；[函数调用](function-calling.md)（Function Calling）场景下流式仍可用 |

> ⚠️ 重要限制：  
> - 流式响应下，`usage` 字段**仅在最终 `data: [DONE]` 帧中出现**，中间帧无 token 统计；  
> - 知识库问答（`/v1/rag/qa`）流式响应中，`retrieval_results`（召回切片）**仅在首帧返回**，后续帧仅含 `delta`；  
> - 所有流式请求必须正确处理 SSE 协议（包括 `event: message`、`data: {...}`、空行分隔），建议使用 SDK 内置流式解析器（如 `bailian-sdk` 的 `onChunk` 回调）。

## 面向开发者：简洁实用提示

- ✅ **快速验证**：CLI 中添加 `--stream` 参数即可开启流式，例如：  
  ```bash
  bailian chat --model qwen-plus --message "写一首五言绝句" --stream
  ```

- ✅ **HTTP 请求示例（curl）**：  
  ```bash
  curl -X POST https://dashscope.aliyuncs.com/api/v1/chat/completions \
    -H "Authorization: Bearer $BAI_LIAN_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
          "model": "qwen-plus",
          "input": {"messages": [{"role": "user", "content": "你好"}]},
          "parameters": {"stream": true, "incremental_output": true}
        }'
  ```

- ✅ **错误规避**：  
  - 不要对视觉/全模态模型设置 `stream=true`；  
  - 不要在流式请求中依赖中间帧的 `usage`；  
  - 前端务必监听 `event: message` 并拼接 `delta.content`，而非直接覆盖 `message.content`。

- ✅ **性能建议**：  
  - 高频低延迟场景（如实时对话）必开 `incremental_output=true`；  
  - 日志审计或调试时，可先关闭流式以获取完整 `usage` 和结构化响应。

## 关联主题页

- [getting started](../guides/getting-started.md)
- [model experience](../guides/model-experience.md)
- [knowledge base](../guides/knowledge-base.md)
- [prompt](../guides/prompt.md)
- [application support](../guides/application-support.md)


