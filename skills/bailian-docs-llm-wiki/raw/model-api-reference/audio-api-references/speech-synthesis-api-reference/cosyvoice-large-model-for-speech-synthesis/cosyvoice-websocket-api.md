# CosyVoice WebSocket API参考

本文介绍通过WebSocket连接访问CosyVoice实时语音合成服务的交互流程、服务端点和请求头。

DashScope SDK目前仅支持Java和Python。使用其他编程语言时，可通过WebSocket连接与服务进行通信。

**用户指南：**关于模型介绍和选型建议请参见[语音合成](https://help.aliyun.com/zh/model-studio/tts-model/)。

## **服务端点**

WebSocket URL固定如下：

## 华北2（北京）

`wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference`

调用时请将`WorkspaceId`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#d3eb3cd37b7fu)。

## 新加坡

`wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/inference`

调用时请将`WorkspaceId`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#d3eb3cd37b7fu)。

**重要**

URL 必须使用 `wss://` 协议，且固定不变。Authorization 在请求头中设置（参见[请求头](#b02603aacf7e9)）。

**重要**

百炼为华北2（北京）、新加坡地域推出了业务空间专属域名，**能够为推理请求提供卓越的性能和更高的稳定性**，建议迁移至新域名：

-   华北2（北京）地域：从 `wss://dashscope.aliyuncs.com` 迁移至 `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
    
-   新加坡地域：从 `wss://dashscope-intl.aliyuncs.com` 迁移至 `wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`
    

其中 `{WorkspaceId}` 为您的业务空间 ID，可在百炼控制台的**业务空间详情**页面查看。现有域名仍可正常使用。

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

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9751312871/CAEQaxiBgID50pCW3hkiIDVlOWNkODdhOGYyYjQ2ZDFiMzgyYjNmMmUzOGZkNGVh4709861_20241015153444.149.svg)

客户端事件和服务端事件的详细说明，请参见[客户端事件](https://help.aliyun.com/zh/model-studio/cosyvoice-client-events)和[服务端事件](https://help.aliyun.com/zh/model-studio/cosyvoice-server-events)。

按时间顺序，客户端与服务端的交互流程如下：

1.  建立连接：客户端与服务端建立WebSocket连接。
    
2.  开启任务：客户端发送run-task事件以开启任务。
    
3.  等待确认：客户端收到服务端返回的task-started事件，标志着任务已成功开启，可以进行后续步骤。
    
4.  发送待合成文本：
    
    客户端按顺序向服务端发送一个或多个包含待合成文本的continue-task事件，服务端接收到完整语句后返回result-generated事件和音频流（文本长度有约束， 详情参见continue-task事件中`text`字段描述）。
    
    **说明**
    
    支持多次发送continue-task事件，按顺序提交文本片段。服务端接收文本片段后自动进行分句：
    
    -   完整语句立即合成，此时客户端能够接收到服务端返回的音频
        
    -   不完整语句缓存至完整后合成，语句不完整时服务端不返回音频
        
    
    当发送finish-task事件时，服务端会强制合成所有缓存内容。
    
5.  接收音频：通过 `binary` 通道接收音频流
    
6.  通知服务端结束任务：
    
    待文本发送完毕后，客户端发送finish-task事件通知服务端结束任务，并继续接收服务端返回的音频流。此步骤不可省略，否则可能导致语音数据不完整。
    
7.  任务结束：
    
    客户端收到服务端返回的task-finished事件，标志着任务结束。
    
8.  关闭连接：客户端关闭WebSocket连接。
    

为提高资源利用率，建议复用 WebSocket 连接处理多个任务，而非为每个任务建立新连接。

**重要**

同一次合成任务中，run-task、所有 continue-task、finish-task 必须使用相同的 `task_id`。每次发起新任务时生成新的 task\_id（如使用 UUID）。使用不同 task\_id 会导致音频错乱或任务失败。
