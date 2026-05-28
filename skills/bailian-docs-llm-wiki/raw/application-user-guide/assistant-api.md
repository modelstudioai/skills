# Assistant API（下线中）

Assistant API 旨在帮助开发者快速开发[大模型应用](https://help.aliyun.com/zh/model-studio/application-introduction#c92394b9b4d8v)（Assistant），例如个人助理、智能导购、会议助手等。相比[文本生成 API](https://help.aliyun.com/zh/model-studio/text-generation)，Assistant API 还内置了多轮对话和工具调用组件，从而降低了大模型应用的开发成本。

**重要**

Assistant API**下线中**，建议迁移至[Responses API](https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-responses)：内置多种工具，并支持多轮上下文管理，可作为替代方案。

**说明**

[智能体应用](https://help.aliyun.com/zh/model-studio/single-agent-application)和 Assistant 虽然均为大模型应用，但二者的功能相互独立，使用方法也不相同。

-   智能体应用：仅可使用控制台进行创建、查看、更新和删除，以及通过[应用调用 API](https://help.aliyun.com/zh/model-studio/agent-and-workflow-application-api-reference)进行调用。
    
-   Assistant：仅可使用 Assistant API 创建、查看、更新、删除和调用。
    

## **为什么选择 Assistant API**

Assistant API 为您提供高效、灵活的大模型应用构建能力，具备以下核心优势：

**内置官方工具：**提供代码执行、文生图、在线搜索等实用工具。例如，Assistant 可以直接运行 Python 代码生成结果，调用搜索功能获取实时信息，或生成图片用于创意设计。![2025-01-16\_15-58-13 (1)](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8610967371/p906615.gif)

```
# 示例代码，仅供参考
def submit_message(thread, assistant, message):
    Messages.create(
        thread_id=thread.id,
        role="user",
        content=message
    )

    run = Runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
        stream=True
    )
    
    for event, data in run:
        if event == 'thread.message.delta':
            yield data.delta.content.text.value
        if event == 'thread.message.completed':
            yield '\n'
        if event == 'thread.run.step.delta':
            # 第一次检测到step.delta时输出工具名称
            if not hasattr(submit_message, 'tool_name_shown'):
                submit_message.tool_name_shown = True
                tool_name = data.delta.step_details.tool_calls[0]['type']
                yield f"\n正在使用工具: {tool_name}\n\n"
            
            formatted_output = format_tool_output(data.delta.step_details.tool_calls[0])
            if formatted_output is not None:
                yield formatted_output
```

**内置对话管理：**提供上下文管理工具，无需手动维护对话历史。![2025-01-20\_16-55-03 (1)](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8610967371/p907622.gif)

```
# 示例代码，仅供参考
while True:
    for event, data in run:
        elif event == 'thread.run.requires_action':
            # 工具调用 => 可能需要提交工具输出 => 导致新的 run 生成器
            tool_calls = data.required_action.submit_tool_outputs.tool_calls
            if not tool_calls:
                continue  
         
            tool_outputs = []
            for tool_call in tool_calls:
                name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)
                output = tools_map[name](**arguments)
                # 普通工具
                tool_outputs.append({"output": output})

            # 将工具输出提交给 run，会返回一个新的 run 生成器
            run = Runs.submit_tool_outputs(
                thread_id=thread.id,  # 原生的对话线程，无需手动管理
                run_id=data.id,
                tool_outputs=tool_outputs,
                stream=True
            )
            yield "转接中...\n"
            break  # 跳出当前事件循环，用返回的 new_run 接着处理

        elif event in ('thread.run.completed', 'thread.run.cancelled',
                    'thread.run.expired', 'thread.run.failed'):
            # 当前 run 结束
            break
    else:
        # for循环正常结束(没有 break)，说明 run 流耗尽
        break
```

**快速搭建多智能体系统：**提供 Assistant、上下文、消息封装、流程控制等简易模板，可以灵活、高效地实现多智能体系统。例如[具备自动规划能力的 Multi Agent 系统](https://help.aliyun.com/zh/model-studio/use-multi-agent-to-query-alibaba-cloud-resource-information)。![output](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9873322271/p826567.gif)

```
# 示例代码，仅供参考
# 获得Multi Agent的回复，输入与输出需要与Gradio前端展示界面中的参数对齐
def get_multi_agent_response(query,history):
    # 处理输入为空的情况
    if len(query) == 0:
        return "",history+[("","")],"",""
    # 获取Agent的运行顺序
    assistant_order = get_agent_response(PlannerAssistant,query)
    try:
        order_stk = ast.literal_eval(assistant_order)
        cur_query = query
        # 依次运行Agent
        for i in range(len(order_stk)):
            yield "----->".join(order_stk),history+[(query,"multi agent正在努力工作中...")],f"{order_stk[i]}正在处理信息...",""
            cur_assistant = assistant_mapper[order_stk[i]]
            response = get_agent_response(cur_assistant,cur_query)
            yield "----->".join(order_stk),history+[(query,"multi agent正在努力工作中...")],response,""
            # 如果当前Agent为最后一个Agent，则将其输出作为Multi Agent的输出
            if i == len(order_stk)-1:
                yield "----->".join(order_stk),history+[(query,response)],"assistant已处理完毕",""
            # 如果当前Agent不是最后一个Agent，则将上一个Agent的输出response添加到下一轮的query中，作为参考信息
            else:
                # 在参考信息前后加上特殊标识符，可以防止大模型混淆参考信息与提问
                cur_query = f"你可以参考已知的信息：\n{response}\n你要完整地回答用户的问题。问题是：{query}。"
    # 兜底策略，如果上述程序运行失败，则直接调用ChatAssistant
    except Exception as e:
        yield "ChatAssistant",[(query,get_agent_response(ChatAssistant,query))],"",""
```

## **快速构建 Assistant**

您可以与 Assistant 进行多轮对话，同时可以选择启用[流式输出](https://help.aliyun.com/zh/model-studio/streaming-output)。通常情况下，您需要依次完成四个主要步骤：

1.  **创建 Assistant：**Assistant 配置了大模型、指令和工具列表，用于执行特定任务。
    
2.  **创建 Thread：**Thread 将记录用户和 Assistant 的所有消息，用于实现多轮对话。
    
3.  **创建 Message：** Message 是承载用户和 Assistant 消息的容器。
    
4.  **创建 Run：**Run 代表 Assistant 响应多轮对话的一系列过程，包括模型推理和工具调用。在这个步骤中，可同时选择启用[流式输出](https://help.aliyun.com/zh/model-studio/streaming-output)，实现自然的交互效果。
    

在[Assistant API 快速入门](https://help.aliyun.com/zh/model-studio/quick-start-of-assistant-api)中，您可以快速上手 Assistant 的使用方法，包括模型推理、工具调用、多轮对话和流式输出。

## **兼容性**

### **模型支持**

Assistant API 支持千问的多款主流模型。您可以前往[模型广场](https://bailian.console.aliyun.com/#/model-market)查看和体验这些模型。

**说明**

千问-Turbo、千问-Plus、千问-Max 模型的快照版本（例如qwen-plus-1220）仅兼容“函数调用”及“知识检索增强”工具。模型的兼容性以实际运行结果为准。

**模型系列**

**模型标识符**

千问-Turbo

qwen-turbo

千问-Plus

qwen-plus

千问-Max

qwen-max

### **工具支持**

Assistant API 支持多款官方工具，以及自定义的函数调用或插件。

**说明**

插件的兼容性请以实际执行结果为准，更多详情可参考[插件列表](https://help.aliyun.com/zh/model-studio/plug-ins/)。

**工具（tools）**

**唯一标识符**

**用途**

代码解释器

code\_interpreter

帮助执行 Python 代码，适用于编程问题、数学计算、数据分析等场景

夸克搜索

quark\_search

用于实时检索网络信息，增强知识获取能力。

文生图

text\_to\_image

将文字描述转为图像，丰富回复形式。

计算器

calculator

拥有良好的计算能力，可用于执行精确运算任务。

生成二维码

generate\_qrcode

可将文本转换为二维码。

GitHub搜索

github\_search

可搜索GitHub项目的实时信息。

函数调用（Function calling）

function

在本地设备上执行特定功能，无需依赖外部网络服务。

知识检索增强（RAG）

rag

检索外部知识，增强大模型回答准确性。

自定义插件

${plugin\_id}

连接自定义业务接口，扩展 AI 业务能力。
