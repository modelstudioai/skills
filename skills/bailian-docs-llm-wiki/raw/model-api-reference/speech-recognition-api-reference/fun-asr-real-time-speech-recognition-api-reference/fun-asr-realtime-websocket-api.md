# Fun-ASR实时语音识别WebSocket API

本文介绍通过 WebSocket 连接访问 Fun-ASR 实时语音识别服务的服务端点、请求头和交互流程。

**用户指南：**关于模型介绍和选型建议请参见[语音识别](https://help.aliyun.com/zh/model-studio/asr-model/)，示例代码请参见[实时语音识别](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition-user-guide)。

DashScope SDK 目前仅支持 Java 和 Python。使用其他编程语言时，可通过 WebSocket 连接与服务进行通信。

## **服务端点**

WebSocket URL 固定如下：

## 中国内地

`wss://dashscope.aliyuncs.com/api-ws/v1/inference`

## 国际

`wss://dashscope-intl.aliyuncs.com/api-ws/v1/inference`

**重要**

URL 必须使用 `wss://` 协议，且固定不变。Authorization 在请求头中设置（参见[请求头](#请求头-headers)）。

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

## **交互流程**

客户端事件和服务端事件的详细说明，请参见[客户端事件](https://help.aliyun.com/zh/model-studio/fun-asr-client-events)和[服务端事件](https://help.aliyun.com/zh/model-studio/fun-asr-server-events)。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5808119771/CAEQURiBgMCczta5pxkiIGY0N2Q2YjIwZTM1MTQyNTY4ZmFkY2MwN2JmOTllODFl4709861_20241015153444.149.svg)

按时间顺序，客户端与服务端的交互流程如下：

1.  建立连接：客户端与服务端建立 WebSocket 连接。
    
2.  开启任务：客户端发送 run-task 指令以开启任务，并接收服务端返回的 task-started 事件，标志着任务已成功开启，可以进行后续步骤。
    
3.  发送音频流：客户端开始发送二进制音频（须为单声道音频），并同时接收服务端持续返回的 result-generated 事件，该事件包含语音识别结果。
    
4.  通知服务端结束任务：客户端发送 finish-task 指令通知服务端结束任务，并继续接收服务端返回的 result-generated 事件。
    
5.  任务结束：客户端收到服务端返回的 task-finished 事件，标志着任务结束。
    
6.  关闭连接：客户端关闭 WebSocket 连接。
