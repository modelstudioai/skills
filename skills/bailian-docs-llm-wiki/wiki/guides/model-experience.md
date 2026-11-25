# model experience

`model experience` 是百炼平台统一的模型调用抽象层，为开发者提供一致的 API 接口与参数语义，屏蔽底层模型类型（文本、视觉、语音等）和部署形态（SaaS/私有化）的差异。所有模型能力均通过该层接入，支持同步推理、流式响应、批量处理等通用交互模式。其设计目标是降低多模态模型集成复杂度，提升跨模型迁移效率。

## 支持的模型与功能

当前 `model experience` 覆盖以下五大能力域，各领域对应独立子文档说明具体模型列表、输入输出格式及典型用例：

- 文本生成：包括大语言模型（LLM）的对话、补全、指令遵循等任务，详见 [模型调用 (raw/model-user-guide/model-experience.md)](../../raw/model-user-guide/model-experience.md)  
- 视觉生成：支持文生图、图生图、视频生成及理解类模型，详见 [模型调用 (raw/model-user-guide/model-experience.md)](../../raw/model-user-guide/model-experience.md)  
- 语音与音频：涵盖 TTS、ASR、音色克隆及音频理解，详见 [模型调用 (raw/model-user-guide/model-experience.md)](../../raw/model-user-guide/model-experience.md)  
- 向量与重排：提供嵌入（embedding）和检索重排（rerank）模型，适用于 RAG 场景  
- 全模态：支持跨文本、图像、语音的联合建模与推理（如图文问答、语音指令驱动视觉操作）

> **注意**：`omni-modal.md` 中描述的“端到端多模态 tokenization”能力尚未在 v3.2 SDK 中开放，实际调用仍需按单模态路径拆分输入；请以 [模型调用 (raw/model-user-guide/model-experience.md)](../../raw/model-user-guide/model-experience.md) 中列出的可用模型为准。

## 关键参数

所有请求共用以下核心参数（部分参数在特定模型类型中为可选或忽略）：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型唯一标识符（如 `qwen-max`, `wanx-v1`），须从控制台或 `/v1/models` 接口获取有效值 |
| `input` | object | 是 | 模型输入数据，结构依模型类型而异（见各子文档） |
| `parameters` | object | 否 | 控制生成行为的键值对，如 `temperature`, `top_p`, `max_tokens`（文本）、`size`（图像）等 |
| `stream` | boolean | 否 | 是否启用流式响应，默认 `false`；仅部分文本/语音模型支持 |

`parameters` 中的字段语义与 OpenAI 兼容，但部分视觉模型不支持 `temperature`；具体支持情况请查阅对应子文档。

## 使用方式

1. **认证**：使用 `Authorization: Bearer <api_key>` 请求头  
2. **端点**：统一 POST 到 `/v1/chat/completions`（文本/全模态）或 `/v1/models/{model}/invoke`（其他类型，推荐）  
3. **示例（文本）**：
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/chat/completions \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "qwen-max",
           "input": {"messages": [{"role":"user","content":"你好"}]},
           "parameters": {"temperature": 0.7}
         }'
   ```
4. **SDK 调用**：推荐使用 `dashscope` Python SDK v1.20.0+，自动适配 `model experience` 协议。

## 限制和注意事项

- 单次请求最大 `input` 大小为 16 MB（视觉/语音模型以原始文件计，文本以 UTF-8 字节计）  
- 流式响应仅保证 chunk 顺序，不保证每个 chunk 的 token 边界与模型内部 tokenizer 严格对齐  
- 私有化部署场景下，`model` 参数必须与本地注册的模型别名完全一致，大小写敏感  
- 所有模型调用受账户配额与速率限制约束，超限返回 `429 Too Many Requests`；详细策略见 [模型调用 (raw/model-user-guide/model-experience.md)](../../raw/model-user-guide/model-experience.md)  
- 不支持跨模型状态保持（如 session-based 对话历史），需由应用层自行管理上下文

## 来源文档

- [模型调用](../../raw/model-user-guide/model-experience.md)


