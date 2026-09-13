# bailian application calling

百炼平台支持通过 API 方式调用已发布的智能体（Agent）应用和工作流（Workflow）应用，实现与业务系统的集成。调用过程需指定应用 ID、传入输入参数，并处理返回结果。所有调用均基于 HTTPS POST 请求，遵循统一的鉴权与错误响应规范。

## 支持的模型/功能

- **智能体应用**：支持单步或多轮对话式调用，适用于客服助手、知识问答等场景；详见 [应用调用](../../raw/application-user-guide/bailian-application-calling.md)。
- **工作流应用**：支持多节点编排任务（如数据清洗→模型推理→结果格式化），可透传参数至各子节点；调用方式与智能体类似，但需注意输入结构兼容性，参考 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling.md)。
- **参数透传能力**：支持将用户请求中的 `input` 字段以 JSON 对象形式完整传递至应用内部，也可通过 `parameters` 字段显式覆盖应用默认配置；具体规则见 [应用的参数传递](../../raw/application-user-guide/bailian-application-calling.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `application_id` | string | 是 | 百炼控制台发布后的应用唯一 ID（非模型 ID） |
| `input` | object | 是 | 用户输入内容，结构由应用定义（如 `{ "query": "你好" }`） |
| `parameters` | object | 否 | 运行时覆盖参数，例如 `{"temperature": 0.3, "max_output_tokens": 512}` |
| `stream` | boolean | 否 | 是否启用流式响应，默认 `false`；仅部分工作流应用支持 |

> **注意**：`parameters` 中的字段必须与应用所绑定模型的实际可配置参数一致；若应用绑定的是 Qwen2-72B-Instruct，则 `temperature`、`top_p` 等有效，但 `presence_penalty` 不被识别（该参数仅适用于部分旧版模型）。请以 [应用调用](../../raw/application-user-guide/bailian-application-calling.md) 中最新支持列表为准。

## 使用方式

1. 获取 `application_id`：在百炼控制台「应用管理」中复制已发布应用的 ID；
2. 构造请求：
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/application \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "application_id": "app-xxx",
           "input": {"query": "解释量子纠缠"},
           "parameters": {"temperature": 0.5}
         }'
   ```
3. 解析响应：成功时返回 `output` 字段（含 `text` 或结构化 `data`），错误时返回标准 `code` 和 `message`。

## 限制和注意事项

- 单次调用 `input` 总长度（UTF-8 编码）不得超过 100 KB；
- 智能体应用默认最大对话轮数为 10 轮（含系统初始化消息），超出后需重置会话；
- 工作流应用不支持跨应用状态共享，每次调用均为无状态执行；
- 流式响应（`stream=true`）仅对输出含 `text` 字段的场景生效，结构化输出（如 JSON 表格）不支持流式；
- 应用调用频控策略独立于模型 API，具体配额请查阅 [应用调用](../../raw/application-user-guide/bailian-application-calling.md) 的限流说明。

## 来源文档

- [应用调用](../../raw/application-user-guide/bailian-application-calling.md)


