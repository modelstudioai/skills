# get started with agents

百炼平台的 Agents 功能支持开发者快速构建具备规划、工具调用和多步推理能力的智能体应用。它基于大模型驱动，提供标准化的运行时接口与可扩展的插件机制，适用于客服助手、数据查询、自动化工作流等场景。本文档汇总关键配置项、调用方式及常见约束，帮助开发者在 5 分钟内完成首个 Agent 实例部署。

## 支持的模型与功能

当前仅支持 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三款 Qwen 系列模型作为 Agent 的底层推理引擎；其他模型（如 `qwen2-72b`）虽可在基础 chat 接口使用，但**不支持 Agent 模式下的 tool calling 与 step-by-step planning**。Agent 内置功能包括：自动工具选择（基于 OpenAPI Schema）、多轮状态保持、结构化输出强制校验，以及内置 `web_search`、`calculator` 和 `code_interpreter` 三个默认工具。详细能力说明见 [开始使用](../../raw/application-user-guide/get-started-with-agents.md)。

## 关键参数

调用 Agent 接口时，必需参数为 `model`（值必须为上述三款支持模型之一）和 `input`（字符串或对象格式的用户初始请求）。可选参数包括：
- `tools`: 工具列表，每个工具需含 `name`、`description` 和 `parameters`（遵循 JSON Schema v7）；
- `tool_choice`: 控制工具调用策略，可选 `"auto"`（默认）、`"none"` 或指定工具名；
- `max_iterations`: 最大执行步数，默认为 8，上限为 12；
- `stream`: 布尔值，启用流式响应时需设为 `true`，此时响应结构与非流式不同（见 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md)）。

> **注意**：原始文档中 `temperature` 和 `top_p` 被列为“Agent 特有参数”，但实际测试表明它们对 Agent 行为无影响，仅作用于底层模型生成阶段；该描述已在最新 SDK 中移除，以 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md) 为准。

## 使用方式

推荐通过百炼 SDK（v3.0.0+）调用：
```python
from aliyun_bailian import AgentClient

client = AgentClient(api_key="YOUR_API_KEY", endpoint="https://dashscope.aliyuncs.com/api/v1")
response = client.run(
    model="qwen-plus",
    input="查一下上海今天最高气温，并换算成华氏度",
    tools=[{"name": "web_search", "description": "...", "parameters": {...}}, ...]
)
print(response.output)
```
HTTP 直接调用需 POST 至 `/agents/run`，Content-Type 为 `application/json`，Body 结构与 SDK 参数一致。完整请求示例参见 [开始使用](../../raw/application-user-guide/get-started-with-agents.md)。

## 限制和注意事项

- 单次请求最大输入长度为 32,768 token，超出将被截断且不报错；
- `tools` 数量上限为 20 个，单个工具 `parameters` Schema 总字符数不得超过 4,096；
- Agent 不支持 `system` 消息字段，所有指令需通过 `input` 或工具描述注入；
- 流式响应中，`event: tool_calls` 类型事件可能重复触发同一工具（已知竞态问题），建议客户端按 `call_id` 去重处理；
- 所有日志与 trace 数据默认保留 7 天，如需长期审计，请自行集成 OpenTelemetry 上报——该要求在 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md) 中有明确说明。

## 来源文档

- [开始使用](../../raw/application-user-guide/get-started-with-agents.md)


