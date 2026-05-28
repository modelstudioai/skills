# 实时多模态交互流程

本文介绍实时多模态服务端和客户端的交互流程。

## VAD 模式

将[客户端事件](https://help.aliyun.com/zh/model-studio/client-events#af43722339yva)事件的`session.turn_detection` 设为`"server_vad"`以启用 VAD 模式。在 VAD 模式下，服务端对传入的音频进行语音活动检测，并在检测到作出响应。此模式适用于客户端到服务器始终发送音频的情况，也是当前的默认模式。

![server\_vad](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0520773571/p991064.svg)

-   服务端在检测到语音开始时发送`input_audio_buffer.speech_started` 事件。
    
-   客户端随时可以选择通过发送 `input_audio_buffer.append` 事件将音频追加到缓冲区。
    
-   服务端在检测到语音结束时发送`input_audio_buffer.speech_stopped`事件。
    
-   服务端通过发送 `input_audio_buffer.committed` 事件来提交输入音频缓冲区。
    
-   服务端发送 `conversation.item.created` 事件，其中包含从音频缓冲区创建的用户消息项。
    

### **工具调用流程**

在 VAD 模式下，当服务端生成的响应需要调用工具时，遵循以下交互流程：

![image.svg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3014236771/p1067613.svg)

-   服务端在检测到语音结束并生成响应时，识别到需要调用工具。
    
-   服务端发送 `response.function_call_arguments.delta` 事件，包含工具调用参数的增量数据。
    
-   服务端发送 `response.function_call_arguments.done` 事件，表示工具调用参数传递完成。
    
-   客户端执行工具调用并获取结果。
    
-   客户端通过 `conversation.item.create` 事件发送工具调用结果。
    
-   服务端自动基于工具调用结果生成响应。
    

## **Manual 模式**

将[客户端事件](https://help.aliyun.com/zh/model-studio/client-events#af43722339yva)事件的`session.turn_detection` 设为 null 以启用 Manual 模式。此模式下，客户端通过显式发送`input_audio_buffer.commit` 和`response.create`事件请求服务器响应。适用于按下即说场景，如聊天软件中的发送语音。

![manual](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0520773571/p991066.svg)

-   客户端可以通过发送 `input_audio_buffer.append` 事件将音频追加到缓冲区。
    
-   客户端通过发送 `input_audio_buffer.commit`事件来提交输入音频缓冲区。 该提交会在对话中创建一个新的用户消息项。
    
-   服务器通过发送 `input_audio_buffer.committed`事件进行响应。
    
-   客户端发送 `response.create` 事件，触发模型生成最终响应。
    
-   服务器通过发送 `conversation.item.created`事件进行响应。
    

### **工具调用流程**

![image.svg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3014236771/p1067740.svg)

在 Manual 模式下，当服务端生成的响应需要调用工具时，遵循以下交互流程：

-   客户端发送 `response.create` 事件后，服务端生成响应并识别到需要调用工具。
    
-   服务端发送 `response.function_call_arguments.delta` 事件，包含工具调用参数的增量数据。
    
-   服务端发送 `response.function_call_arguments.done` 事件，表示工具调用参数传递完成。
    
-   客户端执行工具调用并获取结果。
    
-   客户端通过 `conversation.item.create` 事件发送工具调用结果。
    
-   客户端发送 `response.create` 事件，触发模型生成最终响应。
    
-   服务端基于工具调用结果生成响应，并通过 `response.audio.delta` 或 `response.text.delta` 事件返回给客户端。
