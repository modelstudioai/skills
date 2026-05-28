# Assistant API 流式输出参数说明（下线中）

通过 Assistant API 流式输出，您可以实时获取 Assistant 的运行结果。这些结果称为 Assistant 事件流，包含了 Assistant 运行时产生的状态信息和对话消息。为了正确处理这些对话消息，您需要了解消息增量对象和运行步骤增量对象。

**重要**

Assistant API**下线中**，建议迁移至[Responses API](https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-responses)：内置多种工具，并支持多轮上下文管理，可作为替代方案。

## **消息增量对象**

> 事件名：thread.message.delta

在流式运行中大模型生成的消息片段。

**字段名**

**类型**

**描述**

id

string

消息的标识符。

object

string

对象类型，与事件名保持一致。始终是 thread.message.delta。

delta

object

大模型生成的消息片段对象。

delta.role

string

生成消息的角色。可以是 user 或 assistant 中的一个。

delta.file\_ids

array

暂未使用的字段。

delta.content

object

消息内容对象。

delta.content.type

string

消息内容类型，始终是 text。

delta.content.text

object

消息中包含的文本内容对象。

delta.content.text.annotations

array

暂未使用的字段。

delta.content.text.value

string

消息中包含的文本内容。

**消息增量对象示例**

```
{
    "delta": {
        "content": {
            "text": {
                "annotations": [],
                "value": "[REDACTED]"
            },
            "type": "text"
        },
        "role": "[REDACTED]",
        "file_ids": []
    },
    "id": "[REDACTED]",
    "object": "thread.message.delta",
    "request_id": "[REDACTED]",
    "status_code": 200
}
```

## **运行步骤增量对象**

> 事件名：thread.run.step.delta

在流式运行中工具调用返回的消息片段。

**字段名**

**类型**

**描述**

id

string

运行步骤的标识符。

object

string

对象类型，与事件名保持一致。始终是 thread.run.step.delta。

delta

object

工具调用返回的消息片段对象。

delta.step\_details

object

片段的详细步骤信息对象。

delta.step\_details.type

string

步骤详情类型, 可能是 message\_creation 或 tool\_calls

delta.step\_details.message\_creation

object

步骤创建消息的详细信息。

delta.step\_details.message\_creation.type

string

始终为 message\_creation。

delta.step\_details.message\_creation.message\_id

string

此步骤创建的消息 ID。

delta.step\_details.tool\_calls

array

工具调用的详细信息列表。

delta.step\_details.tool\_calls.type

string

工具调用的类型，可能为 code\_interpreter, quark\_search, text\_to\_image, calculator

delta.step\_details.tool\_calls.code\_interpreter

object

代码解释器的消息对象。

delta.step\_details.tool\_calls.code\_interpreter.arguments

string

代码解释器的输入参数，包括代码类型，完整代码。由大模型生成。

delta.step\_details.tool\_calls.code\_interpreter.output

string

代码解释器的输出参数，包括执行结果。由代码解释器生成。

delta.step\_details.tool\_calls.quark\_search

object

夸克搜索的消息对象。

delta.step\_details.tool\_calls.quark\_search.arguments

string

夸克搜索的输入参数，包括改写后的查询语句。由大模型生成。

delta.step\_details.tool\_calls.quark\_search.output

string

夸克搜索的输出参数，包括成功标记，错误码，错误消息，搜索结果列表（标题、地址、描述、类型、消息源）。由夸克搜索生成。

delta.step\_details.tool\_calls.text\_to\_image

object

文生图的消息对象。

delta.step\_details.tool\_calls.text\_to\_image.arguments

string

文生图的输入参数，包括模型名，风格，图像大小，图像数量，正向提示词和负向提示词。由大模型生成。

delta.step\_details.tool\_calls.text\_to\_image.output

string

文生图的输出参数，包括请求id，任务id，任务状态，提交时间，预计完成时间，结束时间，生成结果，图像数量，成功标记和失败标记。由文生图生成。

delta.step\_details.tool\_calls.calculator

object

计算器的消息对象。

delta.step\_details.tool\_calls.calculator.arguments

string

计算器的输入参数，包括输入公式和请求头。由大模型生成。

delta.step\_details.tool\_calls.calculator.output

string

计算器的输出参数，包括公式和结果。由计算器生成。

**说明**

代码解释器，夸克搜索，文生图和计算器支持流式输出。

其他 Assistant API 工具不支持流式输出。如需在流式输出中获取这些工具调用的结果，请使用一般的工具调用处理方法。详情请参考[工具调用-概述](https://help.aliyun.com/zh/model-studio/tool-calling-overview/)目录的对应章节。

**运行步骤增量对象示例**

```
{
    "delta": {
        "step_details": {
            "tool_calls": [
                {
                    "code_interpreter": {
                        "output": [],
                        "arguments": "[REDACTED]"
                    },
                    "type": "code_interpreter"
                }
            ],
            "type": "tool_calls"
        }
    },
    "id": "[REDACTED]",
    "object": "thread.run.step.delta",
    "request_id": "[REDACTED]",
    "status_code": 200
}
```

## **Assistant 事件流**

在流式运行 Assistant 时发生的事件。

在 Assistant API 中，流式数据也称为“事件流”，由`event（事件）`和`data（事件数据）`组成：

-   `event`：每当创建新对象、转换到新状态或流式传输时，服务器都会发出事件。
    
    例如，创建新的运行`thread.run.created` 、运行完成 `thread.run.completed` 等。
    
-   `data`：包含了事件相关的详细数据。
    
    例如状态、文本或工具消息、错误等。
    

```
event: thread.created
data: {"id": "thread_123", "object": "thread", ...}
```

**事件名**

**数据类型**

**描述**

thread.created

thread

创建新线程时发生。

thread.run.created

run

创建新运行时发生。

thread.run.queued

run

当运行移动到 queued 状态时发生。

thread.run.in\_progress

run

当运行移动到 in\_progress 状态时发生。

thread.run.requires\_action

run

当运行移动到 requires\_action 状态时发生。

thread.run.completed

run

在运行完成时发生。

thread.run.failed

run

当运行失败时发生。

thread.run.cancelled

run

当运行被取消时发生。

thread.run.expired

run

发生在运行过期时。

thread.run.step.created

run step

在创建运行步骤时发生。

thread.run.step.in\_progress

run step

当运行步骤移动到 in\_progress 状态时发生。

thread.run.step.delta

run step delta

在运行步骤的部分内容被流式传输时发生。

thread.run.step.completed

run step

在运行步骤完成时发生。

thread.run.step.failed

run step

发生在运行步骤失败时。

thread.run.step.cancelled

run step

当运行步骤被取消时发生。

thread.run.step.expired

run step

发生在运行步骤过期时。

thread.message.created

message

在消息创建时发生。

thread.message.in\_progress

message

当消息变为 in\_progress 状态时发生。

thread.message.delta

message delta

当消息的部分内容被流式传输时发生。

thread.message.completed

message

当消息完成时发生。

thread.message.incomplete

message

当消息在完成之前结束时发生。

error

error

当发生错误时触发。这可能是由于内部服务器错误或超时引起的。

## **常见问题**

-   在配置流式输出时，如果您遇到代码执行错误，请参阅[错误信息](https://help.aliyun.com/zh/model-studio/error-code)排查错误类型。
    
-   如需了解 Assistant API 流式输出的配置方法，请参阅[Assistant API 流式输出快速入门](https://help.aliyun.com/zh/model-studio/streaming-output)以了解更多信息。
