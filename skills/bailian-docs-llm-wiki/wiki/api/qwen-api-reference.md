# qwen api reference

Qwen 系列大语言模型通过百炼平台提供多种 API 接口，支持文本生成、多轮对话、工具调用等核心能力。开发者可根据技术栈偏好和功能需求选择 OpenAI 兼容、Anthropic 兼容或百炼原生 DashScope 接口。所有接口均需通过 API Key 认证，并遵循统一的配额与计费规则。

## 支持的模型/功能

当前支持的 Qwen 模型包括 `qwen-max`（旗舰版）、`qwen-plus`（均衡版）和 `qwen-turbo`（轻量版），覆盖高精度推理、长上下文处理与低延迟响应场景。各接口支持的功能略有差异：
- OpenAI 兼容 Chat Completions 接口支持标准 `messages` 输入，但**不原生支持工具调用**，需自行封装；详见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。
- Anthropic 兼容 Messages 接口完整支持 `tool_use` 和 `thinking` 模式，适用于需要结构化工具调用的场景；该能力在 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md) 中有明确说明。
- DashScope 接口提供最全参数控制（如 `enable_search`、`enable_code_interpreter`），且是唯一支持 `system_prompt` 动态覆盖的通道；其详细能力清单见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。

## 关键参数

通用必填参数：`model`（如 `"qwen-max"`）、`input.messages`（非空数组）。  
常用可选参数：
- `temperature`: 控制输出随机性（0.0–1.0，默认 0.8）
- `top_p`: 核采样阈值（0.0–1.0，默认 0.95）
- `max_tokens`: 输出最大 token 数（默认 2048，上限 8192）
- `stream`: 布尔值，启用流式响应（仅 DashScope 和 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)支持）

> **注意**：[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)中 `n` 参数被忽略（始终为 1），而 DashScope 接口支持 `n > 1` 并行生成；该差异在 [OpenAI 兼容 Chat Completions](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md) 文档中未明确说明，但实测行为与 DashScope 文档一致。

## 使用方式

1. 获取 API Key：登录百炼控制台 →「API 密钥管理」→ 创建密钥  
2. 发送请求（以 DashScope 为例）：
```bash
curl -X POST "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "model": "qwen-max",
        "input": {"messages": [{"role": "user", "content": "你好"}]},
        "parameters": {"temperature": 0.5}
      }'
```
3. 解析响应：`output.text` 为生成文本，`usage.input_tokens` / `output_tokens` 用于监控消耗。

## 限制和注意事项

- 单次请求 `input.messages` 总长度（含 system prompt）不得超过 32768 tokens（`qwen-max`）或 8192 tokens（`qwen-turbo`）  
- 流式响应中，[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)返回 `delta.content` 字段，DashScope 返回 `output.choices[0].message.content`，二者字段路径不同  
- 所有接口均**不支持跨会话状态保持**；若需长程对话管理，必须自行维护 `messages` 历史并传入每次请求  
- 工具调用结果（如搜索、代码执行）仅在 Anthropic 兼容和 DashScope 接口中以结构化形式返回；OpenAI 兼容接口仅返回自然语言摘要，详见 [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)

## 来源文档

- [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)


