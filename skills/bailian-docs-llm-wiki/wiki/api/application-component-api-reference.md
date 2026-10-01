# application component api reference

应用组件 API 是百炼平台提供的核心能力封装，用于在自定义应用中集成大模型推理、知识库检索、工作流编排等能力。该 API 以 RESTful 形式提供，支持细粒度权限控制与异步任务管理。开发者需通过 RAM 授权并使用指定 endpoint 调用，具体行为受所选模型和参数组合约束。

## 支持的模型/功能

当前支持以下能力类型：
- **基础推理**：`qwen-max`、`qwen-plus`、`qwen-turbo` 等 Qwen 系列模型（详见 [API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md)）；
- **增强能力**：RAG 检索增强（需绑定知识库 ID）、[函数调用](../concepts/function-calling.md)（function calling）、多轮对话状态保持（`conversation_id` 必填）；
- **异步任务**：长耗时任务（如批量文档解析）返回 `task_id`，需轮询 [GET /v1/tasks/{task_id}](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md) 获取结果。

> **注意**：[版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md) 中声明 `qwen-14b-chat` 已于 2024-03-01 下线，但部分旧版 SDK 示例仍引用该模型，实际调用将返回 `404 Model not found` 错误，请务必使用当前有效模型列表。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，必须为 [API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md) 中列出的有效值 |
| `input.messages` | array | 是 | 对话消息数组，格式为 `[{role: "user", content: "xxx"}]`；`role` 仅支持 `"user"`/`"assistant"`/`"system"` |
| `parameters.temperature` | number | 否 | 取值范围 [0.0, 2.0]，默认 1.0；低于 0.5 时输出稳定性显著提升 |
| `parameters.max_tokens` | integer | 否 | 响应最大 token 数，上限 8192（`qwen-max`）或 4096（其余模型） |

## 使用方式

1. **认证**：在请求 Header 中携带 `Authorization: Bearer <access_token>`，Token 需通过 RAM 角色扮演获取（参见 [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)）；  
2. **Endpoint**：生产环境统一使用 `https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`；  
3. **调用示例**（cURL）：
   ```bash
   curl -X POST \
     -H "Authorization: Bearer $ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "qwen-plus",
           "input": {"messages": [{"role":"user","content":"你好"}]},
           "parameters": {"temperature": 0.7}
         }' \
     https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation
   ```

## 限制和注意事项

- 单次请求 `input.messages` 最多 10 条，总输入 token 不得超过模型上下文长度（`qwen-plus` 为 32768）；  
- 免费试用额度按自然日重置，超出后触发计费（详见 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)）；  
- `system` 角色消息仅在首条生效，后续出现将被忽略；  
- 异步任务最长保留 7 天，超期后 `task_id` 不可查，建议业务侧及时持久化结果。

## 来源文档

- [应用组件](../../raw/application-api-reference/application-component-api-reference.md)


