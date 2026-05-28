# 实时语音识别（Qwen-ASR-Realtime）Java SDK-API参考

本文档介绍如何使用 DashScope Java SDK 调用实时语音识别（Qwen-ASR-Realtime）模型。

**用户指南：**模型介绍、功能特性和完整示例代码请参见[实时语音识别-千问](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition-user-guide)

## **前提条件**

1.  [安装SDK](https://help.aliyun.com/zh/model-studio/install-sdk)，确保DashScope SDK版本不低于2.22.5。
    
2.  [获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。
    
3.  了解[交互流程](https://help.aliyun.com/zh/model-studio/qwen-asr-realtime-interaction-process)。
    

## **请求参数**

-   以下参数通过`OmniRealtimeParam`的链式方法设置。
    
    **点击查看示例代码**
    
    ```
    OmniRealtimeParam param = OmniRealtimeParam.builder()
                    .model("qwen3-asr-flash-realtime")
                    // 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：wss://dashscope-intl.aliyuncs.com/api-ws/v1/realtime
                    .url("wss://dashscope.aliyuncs.com/api-ws/v1/realtime")
                    // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                    // 若没有配置环境变量，请用百炼API Key将下行替换为：.apikey("sk-xxx")
                    .apikey(System.getenv("DASHSCOPE_API_KEY"))
                    .build();
    ```
    
    **参数**
    
    **类型**
    
    **是否必须**
    
    **说明**
    
    `model`
    
    `String`
    
    是
    
    指定要使用的[模型](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition-user-guide#ff8c59ef0busr)名称。
    
    `url`
    
    `String`
    
    是
    
    语音识别服务地址：
    
    -   中国内地：`wss://dashscope.aliyuncs.com/api-ws/v1/realtime`
        
    -   国际：`wss://dashscope-intl.aliyuncs.com/api-ws/v1/realtime`。
        
    
    `apikey`
    
    `String`
    
    否
    
    设置API Key。
    
-   以下参数通过`OmniRealtimeConfig`的链式方法设置。
    
    **点击查看示例代码**
    
    ```
    OmniRealtimeTranscriptionParam transcriptionParam = new OmniRealtimeTranscriptionParam();
            transcriptionParam.setLanguage("zh");
            transcriptionParam.setInputSampleRate(16000);
            transcriptionParam.setInputAudioFormat("pcm");
    
    OmniRealtimeConfig config = OmniRealtimeConfig.builder()
                    .modalities(Collections.singletonList(OmniRealtimeModality.TEXT))
                    .enableTurnDetection( true)
                    .turnDetectionType("server_vad")
                    .turnDetectionThreshold(0.0f)
                    .turnDetectionSilenceDurationMs(400)
                    .transcriptionConfig(transcriptionParam)
                    .build();
    ```
    
    **参数**
    
    **类型**
    
    **是否必须**
    
    **说明**
    
    `modalities`
    
    `List<OmniRealtimeModality>`
    
    是
    
    模型输出模态，固定为`[OmniRealtimeModality.TEXT]`。
    
    `enableTurnDetection`
    
    `boolean`
    
    否
    
    是否开启服务端语音活动检测（VAD）。关闭后，需手动调用`commit()`方法触发识别。
    
    默认值：`true`。
    
    取值范围：
    
    -   `true`：开启
        
    -   `false`：关闭
        
    
    `turnDetectionType`
    
    `String`
    
    否
    
    服务端VAD类型，固定为 `server_vad`。
    
    `turnDetectionThreshold`
    
    `float`
    
    否
    
    VAD检测阈值。推荐将该值设为`0.0`。
    
    默认值：`0.2`。
    
    取值范围：`[-1, 1]`。
    
    较低的阈值会提高 VAD 的灵敏度，可能将背景噪音误判为语音。较高的阈值则降低灵敏度，有助于在嘈杂环境中减少误触发。
    
    `turnDetectionSilenceDurationMs`
    
    `int`
    
    否
    
    VAD断句检测阈值（ms）。静音持续时长超过该阈值将被认为是语句结束。推荐将该值设为`400`。
    
    默认值：`800`。
    
    取值范围：`[200, 6000]`。
    
    较低的值（如 300ms）可使模型更快响应，但可能导致在自然停顿处发生不合理的断句。较高的值（如 1200ms）可更好地处理长句内的停顿，但会增加整体响应延迟。
    
    `transcriptionConfig`
    
    `OmniRealtimeTranscriptionParam`
    
    否
    
    语音识别相关配置。
    
-   以下参数通过`OmniRealtimeTranscriptionParam`的`setter`方法设置。
    
    **点击查看示例代码**
    
    ```
    OmniRealtimeTranscriptionParam transcriptionParam = new OmniRealtimeTranscriptionParam();
            transcriptionParam.setLanguage("zh");
            transcriptionParam.setInputSampleRate(16000);
            transcriptionParam.setInputAudioFormat("pcm");
    ```
    
    **参数**
    
    **类型**
    
    **是否必须**
    
    **说明**
    
    `language`
    
    `String`
    
    否
    
    音频源语言。
    
    -   zh：中文（普通话、四川话、闽南语、吴语）
        
    -   yue：粤语
        
    -   en：英文
        
    -   ja：日语
        
    -   de：德语
        
    -   ko：韩语
        
    -   ru：俄语
        
    -   fr：法语
        
    -   pt：葡萄牙语
        
    -   ar：阿拉伯语
        
    -   it：意大利语
        
    -   es：西班牙语
        
    -   hi：印地语
        
    -   id：印尼语
        
    -   th：泰语
        
    -   tr：土耳其语
        
    -   uk：乌克兰语
        
    -   vi：越南语
        
    -   cs：捷克语
        
    -   da：丹麦语
        
    -   fil：菲律宾语
        
    -   fi：芬兰语
        
    -   is：冰岛语
        
    -   ms：马来语
        
    -   no：挪威语
        
    -   pl：波兰语
        
    -   sv：瑞典语
        
    
    `inputSampleRate`
    
    `int`
    
    否
    
    音频采样率（Hz）。支持`16000`和`8000`。
    
    默认值：`16000`。
    
    设置为 `8000` 时，服务端会先升采样到16000Hz再进行识别，可能引入微小延迟。建议仅在源音频为8000Hz（如电话线路）时使用。
    
    `inputAudioFormat`
    
    `String`
    
    否
    
    音频格式。支持`pcm`和`opus`。
    
    默认值：`pcm`。
    

## **关键接口**

### **OmniRealtimeConversation类**

OmniRealtimeConversation通过`import com.alibaba.dashscope.audio.omni.OmniRealtimeConversation;`方法引入。

**方法签名**

**服务端响应事件（通过回调下发）**

**说明**

```
public OmniRealtimeConversation(OmniRealtimeParam param, OmniRealtimeCallback callback)
```

无

构造方法。

```
public void connect() throws NoApiKeyException, InterruptedException
```

[session.created](https://help.aliyun.com/zh/model-studio/qwen-asr-realtime-server-events#2c04b24bc3wlo)

> 会话已创建

[session.updated](https://help.aliyun.com/zh/model-studio/qwen-asr-realtime-server-events#4d6ed9dd62vmj)

> 会话配置已更新

和服务端创建连接。

```
public void updateSession(OmniRealtimeConfig config)
```

[session.updated](https://help.aliyun.com/zh/model-studio/qwen-asr-realtime-server-events#4d6ed9dd62vmj)

> 会话配置已更新

用于更新会话配置，建议在连接建立后首先调用该方法进行设置。若未调用该方法，系统将使用默认配置。只需关注[请求参数](#21cc616e29q8y)中的涉及到的参数。

```
public void appendAudio(String audioBase64)
```

无

将Base64编码后的音频数据片段追加到云端输入音频缓冲区。

-   [请求参数](#21cc616e29q8y)`enableTurnDetection`设为`true`，音频缓冲区用于检测语音，服务端决定何时提交。
    
-   [请求参数](#21cc616e29q8y)`enableTurnDetection`设为`false`，客户端可以选择每个事件中放置多少音频量，最多放置 15 MiB。 例如，从客户端流式处理较小的数据块可以让 VAD 响应更迅速。
    

```
public void commit()
```

[input\_audio\_buffer.committed](https://help.aliyun.com/zh/model-studio/qwen-asr-realtime-server-events#1108a3764an0e)

> 服务端收到提交的音频

提交之前通过append添加到云端缓冲区的音视频，如果输入的音频缓冲区为空将产生错误。

**禁用场景：**[请求参数](#21cc616e29q8y)`enableTurnDetection`设为`true`时。

```
public void endSession() throws InterruptedException
```

[session.finished](https://help.aliyun.com/zh/model-studio/qwen-asr-realtime-server-events#6eaa77339djdv)

> 服务端完成语音识别，结束会话

通知服务端结束会话，服务端收到会话结束通知后将完成最后的语音识别。

**调用时机**：

-   [VAD 模式（默认）](https://help.aliyun.com/zh/model-studio/qwen-asr-realtime-interaction-process#9b49887720jcw)下，发送完音频后调用该方法
    
-   [Manual 模式](https://help.aliyun.com/zh/model-studio/qwen-asr-realtime-interaction-process#ee09a3493fsuc)下，调用commit方法之后调用该方法
    

`endSessionAsync` 是 `endSession` 的异步版本，两者功能完全相同。

```
public void close()
```

无

终止任务，并关闭连接。

```
public String getSessionId()
```

无

获取当前任务的session\_id。

```
public String getResponseId()
```

无

获取最近一次response的response\_id。

### **回调接口（OmniRealtimeCallback）**

服务端会通过回调的方式，将服务端响应事件和数据返回给客户端。

继承此类并实现相应方法以处理服务端事件。

通过`import com.alibaba.dashscope.audio.omni.OmniRealtimeCallback;`引入。

**方法签名**

**参数**

**说明**

```
public void onOpen()
```

无

WebSocket连接成功建立时触发。

```
public abstract void onEvent(JsonObject message)
```

message：[服务端事件](https://help.aliyun.com/zh/model-studio/qwen-asr-realtime-server-events)

收到服务端事件时触发。

```
public abstract void onClose(int code, String reason)
```

code：状态码

reason：WebSocket连接关闭时的日志信息

WebSocket连接关闭时触发。
