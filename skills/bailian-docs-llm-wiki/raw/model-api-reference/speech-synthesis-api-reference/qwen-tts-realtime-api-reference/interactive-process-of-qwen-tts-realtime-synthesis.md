# Qwen-TTS-Realtime WebSocket API 参考

本文介绍通过 WebSocket 连接访问 Qwen-TTS 实时语音合成服务的服务端点、请求头和交互流程。

**用户指南**：关于模型介绍和选型建议请参见[实时语音合成-千问](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide)

Qwen-TTS Realtime API 基于 WebSocket 协议。Java 和 Python 推荐通过 DashScope SDK 调用，可免去处理 WebSocket 细节；其他语言可使用 WebSocket 库直接连接。

## **服务端点**

WebSocket URL 固定如下，通过查询参数 `model` 指定要调用的模型名称：

## 中国内地

WebSocket URL：`wss://dashscope.aliyuncs.com/api-ws/v1/realtime?model=qwen3-tts-flash-realtime`

## 国际

WebSocket URL：`wss://dashscope-intl.aliyuncs.com/api-ws/v1/realtime?model=qwen3-tts-flash-realtime`

**重要**

URL 必须使用 `wss://` 协议。Authorization 在请求头中设置（参见[请求头](#qwen-ws-header-h2)），模型通过 URL 查询参数 `model` 指定。

## **请求头**

请求头中需添加如下信息：

**参数**

**类型**

**是否必选**

**说明**

Authorization

string

是

鉴权令牌，格式为 `Bearer <your_api_key>`，将 `<your_api_key>` 替换为实际的 API Key。

user-agent

string

否

客户端标识，便于服务端追踪来源。

X-DashScope-WorkSpace

string

否

阿里云百炼[业务空间ID](https://help.aliyun.com/zh/model-studio/use-workspace#c5222ec081sbo)。

**重要**

Authorization 鉴权在 WebSocket 握手阶段验证。如果 API Key 无效或缺失，握手将失败并返回 HTTP 401/403 错误。

## **交互流程**

客户端事件和服务端事件的详细说明，请参见[客户端事件](https://help.aliyun.com/zh/model-studio/qwen-tts-realtime-client-events)和[服务端事件](https://help.aliyun.com/zh/model-studio/qwen-tts-realtime-server-events)。

支持两种使用模式：

-   **ServerCommit 模式**：服务端智能判断文本分段与合成时机，开发者无需关心内部状态切分。
    
-   **Commit 模式**：客户端控制每一段文本的提交时间，需显式调用 `input_text_buffer.commit` 触发合成。
    

##### 模式说明：

-   ServerCommit 模式下调用 `input_text_buffer.append` 多次，系统根据内部规则判断合成起点。
    
-   若在 ServerCommit 模式中主动调用 `input_text_buffer.commit`，表示立即合成当前缓冲内容，后续仍维持 ServerCommit 模式。
    
-   Commit 模式下仅调用 `input_text_buffer.append` 不会触发合成，需明确调用 `input_text_buffer.commit`。
    

![qwen-tts](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2220693571/p992312.svg)

**关键流程说明：**

1.  **连接阶段**：客户端发起 WebSocket 连接，服务端返回 `session.created`，表示会话已初始化。
    
2.  **配置会话**：客户端发送 `session.update` 事件设置音色、格式、模式等参数。
    
3.  **文本输入阶段**：客户端通过多次发送 `input_text_buffer.append` 添加文本到缓冲区。
    
4.  **触发合成阶段**：
    
    -   ServerCommit 模式中系统自动判断合成时机，或客户端手动调用 `input_text_buffer.commit` 强制触发。
        
    -   Commit 模式中仅 `input_text_buffer.commit` 操作才会真正触发语音合成流程。
        
5.  **音频生成阶段**：服务端发出 `response.created` 表示任务已启动，随后分片返回音频 `response.audio.delta`（base64 编码），直到 `response.audio.done`。
    
6.  **会话结束阶段**：客户端显式调用 `session.finish` 通知服务端清理状态，服务端返回 `session.finished` 后关闭连接。
    

连接建立后，服务端返回如下 `session.created` 事件：

```
{
    "event_id": "event_xxx",
    "type": "session.created",
    "session": {
        "object": "realtime.session",
        "mode": "server_commit",
        "model": "qwen3-tts-flash-realtime",
        "voice": "Cherry",
        "response_format": "pcm",
        "sample_rate": 24000,
        "id": "sess_xxx"
    }
}
```
