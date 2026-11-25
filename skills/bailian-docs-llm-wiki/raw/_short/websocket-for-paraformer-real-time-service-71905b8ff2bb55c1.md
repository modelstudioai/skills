# WebSocket 接入指南

本文介绍通过 WebSocket 连接访问 Paraformer 实时语音识别服务的接口地址、请求头和交互流程。

使用 Python 调用模型时，请参见 [Paraformer Python SDK](realtime-websocket-python-sdk-paraformer-48f2eb5035b28f23.md)。

> **重要**
>
> 阿里云百炼为华北2（北京）地域推出了业务空间专属域名，能够为推理请求提供卓越的性能和更高的稳定性，建议从 `dashscope.aliyuncs.com` 迁移至 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`。
>
> `{WorkspaceId}`需要替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。现有域名仍可正常使用。

**用户指南：**关于模型介绍和选型建议请参见[语音识别](../model-user-guide/model-experience/speech-and-audio/speech-recognition/asr-model.md)，示例代码请参见[实时语音识别](../model-user-guide/model-experience/speech-and-audio/speech-recognition/real-time-speech-recognition-user-guide.md)。

DashScope SDK 目前仅支持 Java 和 Python。使用其他编程语言时，可通过 WebSocket 连接与服务进行通信。

<a id="接口地址"></a>

<a id="f8ab6424cbcdk"></a>

## 接口地址

Paraformer仅支持在华北2（北京）地域使用。WebSocket URL 固定如下：

`wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

> **重要**
>
> URL 必须使用 `wss://` 协议，且固定不变。Authorization 在请求头中设置（参见[请求头](websocket-for-paraformer-real-time-service-71905b8ff2bb55c1.md#f5b7af17168sz)）。

<a id="请求头"></a>

<a id="f5b7af17168sz"></a>

## 请求头

请求头中需添加如下信息：

| 参数 | 类型 | 是否必选 | 说明 |
| --- | --- | --- | --- |
| Authorization | string | 是 | 鉴权令牌，格式为`Bearer <your_api_key>`，使用时，将“`<your_api_key>`”替换为实际的API Key。 |
| user-agent | string | 否 | 客户端标识，便于服务端追踪来源。 |
| X-DashScope-WorkSpace | string | 否 | 阿里云百炼[业务空间ID](https://help.aliyun.com/zh/model-studio/use-workspace)。 |
| X-DashScope-DataInspection | string | 否 | 是否启用数据合规检测功能。默认不传或设为`enable`。如非必要，请勿启用该参数。 |

> **重要**
>
> Authorization 鉴权在 WebSocket 握手阶段验证。如果 API Key 无效或缺失，握手将失败并返回 HTTP 401/403 错误。

<a id="交互流程"></a>

<a id="62149ca39bx2i"></a>

## 交互流程

客户端事件和服务端事件的详细说明，请参见[客户端事件](paraformer-client-events-2ebe52755a401965.md)和[服务端事件](paraformer-server-events-19da1acc086012f9.md)。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8352835871/CAEQURiBgMCczta5pxkiIGY0N2Q2YjIwZTM1MTQyNTY4ZmFkY2MwN2JmOTllODFl4709861_20241015153444.149.svg)

按时间顺序，客户端与服务端的交互流程如下：

1.  建立连接：客户端与服务端建立 WebSocket 连接。
2.  开启任务：客户端发送 run-task 指令以开启任务，并接收服务端返回的 task-started 事件，标志着任务已成功开启，可以进行后续步骤。
3.  发送音频流：客户端开始发送二进制音频（须为单声道音频），并同时接收服务端持续返回的 result-generated 事件，该事件包含语音识别结果。
4.  通知服务端结束任务：客户端发送 finish-task 指令通知服务端结束任务，并继续接收服务端返回的 result-generated 事件。
5.  任务结束：客户端收到服务端返回的 task-finished 事件，标志着任务结束。
6.  关闭连接：客户端关闭 WebSocket 连接。

<a id="可用的-sdk"></a>

## 可用的 SDK

-   [Python SDK](realtime-websocket-python-sdk-paraformer-48f2eb5035b28f23.md)
-   [Java SDK](paraformer-real-time-speech-recognition-java-sdk-7a1a7974a8aacc5d.md)
-   [Android SDK](android-sdk-for-paraformer-real-time-service-9e7815d0b3adcb41.md)
-   [iOS SDK](ios-sdk-for-paraformer-real-time-service-28718b821c8d6e25.md)
-   [HarmonyOS SDK](harmonyos-sdk-for-paraformer-real-time-service-642577184b92b90f.md)
