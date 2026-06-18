# Sambert WebSocket API 参考

本文介绍通过WebSocket连接访问Sambert实时语音合成服务的交互流程、服务端点和请求头。

DashScope SDK目前仅支持Java和Python。使用其他编程语言时，可通过WebSocket连接与服务进行通信。

**用户指南：**关于模型介绍和选型建议请参见[语音合成](https://help.aliyun.com/zh/model-studio/tts-model/)。

## **服务端点**

Sambert仅支持在北京地域使用。

WebSocket 服务端点固定为：`wss://dashscope.aliyuncs.com/api-ws/v1/inference`

**重要**

URL 必须使用 `wss://` 协议，且固定不变。Authorization 在请求头中设置（参见[请求头](#sb-ws-h2-headers)）。

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

X-DashScope-DataInspection

string

否

是否启用数据合规检测功能。默认不传或设为`enable`。如非必要，请勿启用该参数。

**重要**

Authorization 鉴权在 WebSocket 握手阶段验证。如果 API Key 无效或缺失，握手将失败并返回 HTTP 401/403 错误。

## 交互流程

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7806858771/CAEQURiBgICX8Y6AmBkiIGJmOTc2YjY2ZTYyNDQ0MmI4M2U4NTYxYmE5ZjYwMDY44709861_20241015153444.149.svg)

客户端事件和服务端事件的详细说明，请参见[客户端事件](https://help.aliyun.com/zh/model-studio/sambert-client-events)和[服务端事件](https://help.aliyun.com/zh/model-studio/sambert-server-events)。

按时间顺序，客户端与服务端的交互流程如下：

1.  建立连接：客户端与服务端建立WebSocket连接。
    
2.  开启任务：客户端发送run-task事件以开启任务。Sambert在run-task中一次性发送全部待合成文本。
    
3.  等待确认：客户端收到服务端返回的task-started事件，标志着任务已成功开启。
    
4.  接收音频：客户端通过 `binary` 通道接收服务端持续返回的音频流，同时收到result-generated事件（携带时间戳等附加信息）。
    
5.  任务结束：客户端收到服务端返回的task-finished事件，标志着任务结束。
    
6.  关闭连接：客户端关闭WebSocket连接。
    

为提高资源利用率，建议复用 WebSocket 连接处理多个任务，而非为每个任务建立新连接。详细操作请参见[实时语音合成-千问](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#ug-ws-reuse-sec)。

**重要**

Sambert 不支持流式输入（streaming 为 `out` 而非 duplex），所有待合成文本必须在 run-task 事件中一次性发送。不支持 continue-task 和 finish-task 指令。
