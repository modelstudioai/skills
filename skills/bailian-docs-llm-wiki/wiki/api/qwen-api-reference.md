# qwen api reference

Qwen 系列大模型通过百炼平台提供多种 API 接入方式，支持文本生成、工具调用、多轮对话等核心能力。开发者可根据技术栈兼容性、功能需求和运维复杂度选择合适接口。所有接口均需通过阿里云 AccessKey 进行身份认证，并遵循统一的配额与计费规则。

## 支持的模型/功能

当前 Qwen 系列支持以下主流接入协议：

- **OpenAI 兼容 Chat Completions**：适用于已有 OpenAI 客户端（如 `openai>=1.0`）的快速迁移，支持 `qwen-max`、`qwen-plus`、`qwen-turbo` 等模型，但不支持原生工具调用（需依赖 [OpenAI兼容-Responses](https://help.aliyun.com/zh/model-studio/openai-compatible-responses) 的增强能力）。  
- **OpenAI兼容-Responses**：在标准 Chat Completions 基础上扩展了联网搜索、代码解释器、网页内容提取等内置工具，自动维护对话历史，适合需要开箱即用智能体能力的场景。该能力详见 [原文标题](../../raw/model-api-reference/qwen-api-reference.md)。  
- **Anthropic兼容-Messages**：完全兼容 Anthropic Messages API 规范，支持 `system` 消息、`tool_use`/`tool_result` 交互、以及结构化思考链输出，适用于构建可控性强的推理工作流。  
- **DashScope 原生接口**：百炼最底层、功能最全的接口，支持全部模型参数（如 `top_k`、`repetition_penalty`）、流式响应控制、自定义 stop 字符串及完整日志调试字段，是高级定制场景的首选。其详细参数说明见 [原文标题](../../raw/model-api-reference/qwen-api-reference.md)。

> **注意**：`qwen-vl` 和 `qwen-audio` 等多模态模型**不支持** [OpenAI 兼容接口](../concepts/openai-compatible-api.md)，仅可通过 DashScope 原生接口调用；相关限制已在 [原文标题](../../raw/model-api-reference/qwen-api-reference.md) 中明确，但部分旧版文档未同步更新该约束，请以 DashScope 文档为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `"qwen-max"`、`"qwen-plus"`；不同接口对取值范围有差异（例如 Anthropic 接口要求映射为 `"claude-3-haiku-20240307"` 风格别名） |
| `messages` | array | 是（除部分 DashScope 单轮模式外） | 对话消息列表，格式为 `{"role": "user/system/assistant", "content": "..."}`；`system` 角色仅 Anthropic 和 DashScope 原生接口支持 |
| `tools` / `tool_choice` | object/array | 否 | 工具定义与调用策略；仅 OpenAI兼容-Responses 和 Anthropic兼容-Messages 支持完整工具协议 |
| `stream` | boolean | 否 | 是否启用流式响应；所有接口均支持，但 DashScope 返回字段结构更细粒度（含 `usage` 实时统计） |

## 使用方式

1. **认证**：使用阿里云主账号或 RAM 子账号的 `AccessKeyId` 和 `AccessKeySecret`，通过 HTTP Header `Authorization: Bearer <api_key>` 传递（其中 `<api_key>` 为 DashScope API Key，非阿里云 AK）；  
2. **Endpoint**：各接口对应独立域名（如 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)为 `https://dashscope.aliyuncs.com/compatible-mode/v1`），具体地址请参考各协议文档；  
3. **示例请求（cURL）**：  
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation" \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "qwen-max",
           "input": {"messages": [{"role": "user", "content": "你好"}]},
           "parameters": {"temperature": 0.8}
         }'
   ```

## 限制和注意事项

- 单次请求 `messages` 总长度（token 数）上限因模型而异：`qwen-turbo` 为 8K，`qwen-plus` 为 32K，`qwen-max` 为 64K（上下文窗口）；  
- [OpenAI 兼容接口](../concepts/openai-compatible-api.md)默认禁用 `system` 消息和 `logprobs`，若需启用，须切换至 DashScope 原生接口；  
- 所有接口均**不支持跨区域调用**：API Key 必须与所选 Endpoint 所属地域一致（如华东1区 Key 仅可调用 `dashscope.aliyuncs.com`，不可用于 `dashscope-intl.aliyuncs.com`）；  
- 流式响应中，OpenAI 兼容接口返回 `delta` 字段，DashScope 返回 `output.text` 增量，二者语义一致但字段名不同——此差异已在 [原文标题](../../raw/model-api-reference/qwen-api-reference.md) 中列出，但部分 SDK 尚未适配，建议自行解析。

## 来源文档

- [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)


