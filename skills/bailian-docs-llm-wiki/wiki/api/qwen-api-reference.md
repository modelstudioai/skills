# qwen api reference

Qwen 系列大模型通过百炼平台提供多种 API 接入方式，支持文本生成、工具调用、多轮对话等核心能力。开发者可根据技术栈兼容性、功能需求和运维复杂度选择合适接口。所有接口均需通过百炼控制台申请 API Key 并配置权限。

## 支持的模型与功能

当前支持的 Qwen 模型包括 `qwen-max`、`qwen-plus`、`qwen-turbo` 及 `qwen2.5-*` 系列（如 `qwen2.5-7b-instruct`），覆盖高性能、均衡型与轻量级场景。各接口支持的功能略有差异：

- **OpenAI 兼容 Chat Completions**：适用于已有 OpenAI 生态的应用迁移，支持 `messages` + `model` 基础参数，但[不支持原生工具调用字段（如 `tool_choice` 的高级策略）](../../raw/model-api-reference/qwen-api-reference.md)；
- **OpenAI 兼容-Responses**：内置联网搜索、代码解释器与网页提取能力，自动维护对话上下文，适合快速构建智能助手类应用；
- **Anthropic 兼容-Messages**：支持 `system` 角色、`tool_use` 块及思考过程输出（`thinking`），但需注意其 `max_tokens` 语义与 DashScope 不同；
- **DashScope 原生接口**：功能最全，支持流式响应、自定义 stop 字符串、logprobs、seed 控制及完整工具调用协议，是生产环境推荐接入方式。

> **注意**：原始文档中称 Anthropic 兼容接口“支持思考和工具调用”，但实测 `qwen-max` 在该接口下暂不返回 `thinking` 字段；建议以 [DashScope 文档](../../raw/model-api-reference/qwen-api-reference.md) 中的 `qwen-max` 行为为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `qwen-max`、`qwen2.5-72b-instruct`；必须与所选接口支持的模型列表一致 |
| `messages` | array | 是（除部分非 chat 场景） | 对话历史，格式为 `[{ "role": "user", "content": "..." }]`；`system` 角色在 DashScope 和 Anthropic 接口中有效，在 [OpenAI 兼容接口](../concepts/openai-compatibility.md)中被忽略 |
| `temperature` | number | 否 | 采样温度，默认 `1.0`；范围 `[0.0, 2.0]`，值越低输出越确定 |
| `top_p` | number | 否 | 核采样阈值，默认 `1.0`；推荐与 `temperature` 二选一使用 |
| `stream` | boolean | 否 | 是否启用流式响应；仅 DashScope 和 [OpenAI 兼容接口](../concepts/openai-compatibility.md)支持 |
| `tools` / `functions` | array | 否 | 工具定义数组；DashScope 使用 `tools`，[OpenAI 兼容接口](../concepts/openai-compatibility.md)使用 `functions`（已弃用），Anthropic 使用 `tool_use` 块；详见 [原文标题](../../raw/model-api-reference/qwen-api-reference.md) |

## 使用方式

1. **认证**：在请求 Header 中添加 `Authorization: Bearer <your_api_key>`；
2. **Endpoint**（以 DashScope 为例）：
   ```bash
   POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation
   ```
3. **示例请求体（DashScope）**：
   ```json
   {
     "model": "qwen-max",
     "input": {
       "messages": [
         {"role": "user", "content": "你好，请用中文简要介绍 Qwen 系列模型"}
       ]
     },
     "parameters": {
       "temperature": 0.5,
       "top_p": 0.8
     }
   }
   ```
   注意：[OpenAI 兼容接口](../concepts/openai-compatibility.md)的 `input` 结构扁平化（无嵌套 `input` 字段），且参数直接置于顶层；具体结构差异请参考 [原文标题](../../raw/model-api-reference/qwen-api-reference.md)。

## 限制和注意事项

- 单次请求 `messages` 总 token 数上限为 32768（`qwen-max`），其他模型依规格降低；
- 流式响应中，DashScope 返回 `event: message` 和 `event: finish` 事件，而 [OpenAI 兼容接口](../concepts/openai-compatibility.md)返回 `data: {...}` 格式，客户端需分别适配；
- 所有接口均**不支持跨模型会话状态共享**，即使使用同一 `conversation_id`，切换模型后上下文不继承；
- 调用失败时，HTTP 状态码 `429` 表示限流，`400` 多因参数格式错误（如 `messages` 缺少 `role`），详细错误码见 [原文标题](../../raw/model-api-reference/qwen-api-reference.md)。

## 来源文档

- [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)



