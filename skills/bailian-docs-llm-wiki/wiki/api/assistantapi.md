# assistantapi

Assistant API 提供了一套标准化的编程接口，用于快速构建、编排和运行基于大语言模型的智能体应用。开发者可通过该 API 定义智能体行为、挂载外部工具，并在独立的会话上下文中管理多轮对话与异步任务执行。由于该接口已处于**下线中**状态，新建业务建议优先迁移至 [[responses-api]]。

## 支持的模型与核心功能
- **基础模型**：支持调用通义系列大模型（如 `qwen-max`，完整列表参考 [[models]]）。
- **工具生态**：内置代码解释器 (`code_interpreter`)、搜索 (`search`)、文生图 (`text_to_image`)、计算器 (`calculator`)，并支持通过 OpenAI 兼容格式接入自定义 `function` 插件。
- **[[streaming-output|流式输出]]**：基于 SSE 协议提供事件流，支持实时监听运行状态 (`thread.run.*`)、生成文本片段 (`thread.message.delta`) 及工具调用步骤 (`thread.run.step.delta`)。
- **架构设计**：采用 `Assistant`（智能体配置）+ `Thread`（会话容器）+ `Message`（单条消息）+ `Run`（执行任务）四层对象模型，实现配置、上下文与执行状态解耦。

## 关键参数
| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `model` | string | 是 | 底层推理模型名称 |
| `instructions` | string | 否 | 系统提示词（System Prompt），定义智能体角色与行为规范 |
| `tools` | list[dict] | 否 | 可用工具集合。接入自定义插件时需配置 `auth.user_token` 实现用户级 HTTP 鉴权 |
| `temperature`/`top_p`/`top_k` | float/int | 否 | 控制文本生成随机性与多样性的采样参数 |
| `stream` | boolean | 否 | 是否启用 SSE 流式响应，默认 `false` |
| `metadata` | dict | 否 | 附加业务数据（最多16个键值对，键≤64字符，值≤512字符） |
| `assistant_id` / `thread_id` | string | 是 | 运行时绑定的智能体 ID 与会话线程 ID |

## 使用方式与工作流
API 提供 HTTP RESTful 端点与 Python/Java SDK 两种集成路径。标准交互流程如下：
1. **创建智能体**：定义模型、系统提示词与可用工具集。
2. **初始化线程**：创建 `Thread` 对象隔离会话，可预置初始 `Messages`。
3. **提交运行**：将 Assistant 绑定至 Thread 触发推理。支持同步等待 (`wait`) 或异步流式迭代。
4. **状态检查与结果提取**：轮询或监听 `Run` 状态（`completed`/`failed`/`requires_action` 等），完成后检索 `Messages` 获取最终回复，或通过 `RunSteps` 查看工具调用明细。

详细对象定义与生命周期管理可查阅：[Assistants（下线中）](../../raw/application-api-reference/assistantapi/assistant.md)、[Threads（下线中）](../../raw/application-api-reference/assistantapi/thread.md) 与 [Runs（下线中）](../../raw/application-api-reference/assistantapi/runs.md)。

**Python SDK 核心调用示例（同步模式）**
```python
from dashscope import Assistants, Threads, Runs, Messages
import os

# 1. 创建智能体
assistant = Assistants.create(
    model="qwen-max",
    instructions="你是一个专业的数据分析助手。",
    tools=[{"type": "code_interpreter"}]
)

# 2. 创建线程与初始消息
thread = Threads.create(
    messages=[{"role": "user", "content": "计算 25 的平方根并输出结果。"}]
)

# 3. 触发运行并阻塞等待完成
run = Runs.create(thread.id, assistant_id=assistant.id)
run_status = Runs.wait(run.id, thread_id=thread.id)

# 4. 获取回复内容
if run_status.status == "completed":
    history = Messages.list(thread.id)
    for msg in history.data:
        if msg.role == "assistant":
            print(msg.content[0].text.value)
```

## 限制与注意事项
- **生命周期管理**：所有 `Assistant` 与 `Thread` 实例持久化存储于阿里云百炼服务端，无自动失效日期，支持通过 ID 长期检索。
- **概念隔离**：[[agent-application]] 与本 API 相互独立。前者仅支持控制台管理并通过专用应用 API 调用，二者底层架构与调用方式不互通。
- **[[streaming-output|流式输出]]局限**：仅代码解释器、搜索、文生图和计算器支持 `delta` 增量流式推送。其他自定义 `function` 调用需在 `Run` 结束后通过常规步骤接口获取完整结果。
- **SDK 版本依赖**：运行示例需确保 Python SDK `dashscope>=1.18.0`，Java SDK `>=2.14.2`。
- **工作空间鉴权**：若使用子业务空间 API Key，请求必须显式传入 `workspace` 参数。生产环境建议通过环境变量注入 `DASHSCOPE_API_KEY`。

> **注意**：
> 1. **状态与迁移**：该 API 已进入**下线中**阶段，官方不再推荐用于新建生产链路。请评估迁移至 [[responses-api]]，新接口原生内置多轮上下文管理与工具路由，大幅降低 `Run` 生命周期维护成本。
> 2. **参数类型矛盾修正**：原始文档中 `metadata` 字段在部分表格被标注为 `str`，但实际 HTTP 请求体、返回示例及 SDK 构造均严格使用 `dict`（JSON Object）。开发时请以对象格式传入，避免序列化报错。
> 3. **工具鉴权透传差异**：`tools` 配置中的 `auth.user_http` 传递规则在 HTTP 直调与 SDK 封装中存在实现差异，建议优先使用 SDK 提供的 Builder/Dict 构造方法，以确保 Header 鉴权字段正确挂载。

## 来源文档

- [Assistants（下线中）](../../raw/application-api-reference/assistantapi/assistant.md)
- [Threads（下线中）](../../raw/application-api-reference/assistantapi/thread.md)
- [Messages（下线中）](../../raw/application-api-reference/assistantapi/message.md)
- [Runs（下线中）](../../raw/application-api-reference/assistantapi/runs.md)
- [Run Steps（下线中）](../../raw/application-api-reference/assistantapi/run-steps.md)
- [Assistant API [[streaming-output|流式输出]]参数说明（下线中）](../../raw/application-api-reference/assistantapi/event-streaming.md)
- [Assistant API 调用示例（下线中）](../../raw/application-api-reference/assistantapi/call-example.md)

