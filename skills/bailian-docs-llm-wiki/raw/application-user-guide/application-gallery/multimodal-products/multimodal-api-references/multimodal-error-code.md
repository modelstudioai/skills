# 多模态交互套件-错误码

本文介绍使用阿里云百炼多模态交互套件可能出现的错误信息及解决方案。

## **AccessDenied.Unpurchased**

```
{"header":{"task_id":"xxxxx","event":"task-failed","error_code":"AccessDenied.Unpurchased","error_message":"Access to model denied. Please make sure you are eligible for using the model.","attributes":{}},"payload":{}}
```

### **Access to model denied. Please make sure you are eligible for using the model.**

**原因：**错误码error\_code出现在header里，用户未开通阿里云百炼服务，无法建连。

**解决方案：**注册或登录阿里云账号，然后前往模型广场开通百炼服务。

## **Model.AccessDenied**

```
{"header":{"task_id":"xxxxx","event":"task-failed","error_code":"Model.AccessDenied","error_message":"Model access denied.","attributes":{}},"payload":{}}
```

### **Model access denied.**

**原因：** 错误码error\_code出现在header里，使用的业务空间不是默认业务空间，无法建连。目前多模态交互只支持从默认业务空间调用。

**解决方案：**使用默认业务空间的API Key调用多模态交互。

## **RequestTimeOut**

```
{"header":{"task_id":"xxxxx","event":"task-failed","error_code":"ResponseTimeout","error_message":"Response timeout!","attributes":{}},"payload":{}}
```

### **Response timeout!**

**原因：** 错误码error\_code出现在header里，百炼网关报错，无法建连。百炼网关要求服务端和客户端必须持续通信，如果超过1分钟没有交互则会超时报错。

**解决方案：** 持续交互，避免长时间无消息传递。若客户端需在无交互时保持连接，应定期发送心跳消息（HeartBeat）。服务端会回应心跳，确保连接活跃，避免超时关闭。具体的心跳消息格式参见[心跳事件](https://help.aliyun.com/zh/model-studio/multimodal-interaction-protocol#df274da95fsoq)。

## **421-**InvalidParameter

```
{"header":{"event":"result-generated","task_id":"xxxxx","status_code":421,"status_name":"InvalidParameter","status_message":"xxxxx"},"payload":{"output":{"event":"Error","dialog_id":"xxxxx"}}}
```

### **type of directive payload is error, please choose transcript or prompt**

**原因：**错误码status\_code出现在header里，收到该错误后连接会断开，是RequestToRespond的参数type取值错误。

**解决方案：**修正RequestToRespond的参数type，重新发请求。type只能支持以下两种：

（1）transcript 表示直接把文本转语音。

（2）prompt 表示把文本送大模型回答。

### **status\_message是其他报错信息**

**原因：**status\_code出现在header里，收到该错误后连接会断开，是其他的参数取值错误 ，status\_message 信息都有具体的提示说明。

**解决方案：**根据 status\_message 信息提示修正参数取值。

## **422-**DirectiveNotSupported

```
{"header":{"event":"result-generated","task_id":"xxxxx","status_code":422,"status_name":"DirectiveNotSupported","status_message":"Directive not supported: xxx"},"payload":{"output":{"event":"Error","dialog_id":"xxxxx"}}}
```

### Directive not supported: xxx

**原因：**错误码status\_code出现在header里，收到该错误后连接会断开。传入的指令 directive 的取值是不支持的指令。

**解决方案：**请检查指令名称，使用多模态交互可用的指令。参考[文本消息类型](https://help.aliyun.com/zh/model-studio/multimodal-interaction-protocol#15c38d92bc50s)的说明。

## **432-**AppConfigError

```
{"header":{"event":"result-generated","task_id":"xxxxx","status_code":432,"status_name":"AppConfigError","status_message":"xxxxxxx"},"payload":{"output":{"event":"Error","dialog_id":"xxxxx"}}}
```

**原因：**错误码status\_code出现在header里，收到该错误后连接会断开。获取到百炼应用的配置时出现问题。

**解决方案：**参考status\_message 里的具体信息，修改传入的参数配置。

## **433-**BillingAuthError

```
{"header":{"event":"result-generated","task_id":"xxxxx","status_code":433,"status_name":"BillingAuthError","status_message":"xxxxxxx"},"payload":{"output":{"event":"Error","dialog_id":"xxxxx"}}}
```

### Billing auth info not found!

**原因：**错误码status\_code出现在header里，收到该错误后连接会断开。当前使用的账号未开通百炼多模态交互服务。

**解决方案：**为当前账号开通百炼多模态交互服务，或使用已开通的账号。

## **444-**ClientAudioTimeout

```
{"header":{"event":"result-generated","task_id":"xxxxx","status_code":444,"status_name":"ClientAudioTimeout","status_message":"Waiting for client audio timed out."},"payload":{"output":{"event":"Error","dialog_id":"xxxxx"}}}
```

### Waiting for client audio timed out.

**原因：**错误码status\_code出现在header里，收到该错误后连接会断开。服务端长时间收不到客户端的音频输入。

**解决方案：**在duplex模式应持续向服务端上传音频；在tap2talk模式应保证在状态切换到Listening之后立刻持续上传音频，也可以在所有状态下都上传音频；在push2talk模式发送SendSpeech消息后应立刻上传音频直到发送StopSpeech消息。

## **449-**TooManyInterrupt

```
{"header":{"event":"result-generated","task_id":"xxxxx","status_code":449,"status_name":"TooManyInterrupt","status_message":"Send too many RequestToRespond or RequestToSpeak directives in a short time!"},"payload":{"output":{"event":"Error","dialog_id":"xxxxx"}}}
```

### Send too many RequestToRespond or RequestToSpeak directives in a short time!

**原因：**错误码status\_code出现在header里，收到该错误后连接会断开。用户短时间内发送过多RequestToRespond或RequestToSpeek 打断正常交互，通常是调用程序bug导致。

**解决方案：**排查程序调用逻辑，避免多次发送RequestToRespond或RequestToSpeek 。

## **424-**AudioFormatError

```
{"header":{"event":"result-generated","task_id":"xxxxx","status_code":424,"status_name":"AudioFormatError","status_message":"xxxxx"},"payload":{"output":{"event":"Error","dialog_id":"xxxxx"}}}
```

### Failed to decode audio! Please check audio format! / ASR decode error, please check audio format!

**原因：**错误码status\_code出现在header里，收到该错误后连接会断开。输入音频的格式不合规，ASR无法正常解析音频。

**解决方案：**检查输入的音频格式，输入正确的音频数据。

## **425-**NoInputAudioError

```
{"header":{"event":"result-generated","task_id":"xxxxx","status_code":200,"status_name":"Success","status_message":"Success"},"payload":{"output":{"event":"Error","dialog_id":"xxxxx","round_id":"xxxxx","llm_request_id":"xxxxx","error_code":425,"error_name":"NoInputAudioError","error_message":"ASR input audio error, no input audio , please check audio data!"}}}
```

### ASR input audio error, no input audio , please check audio data!

**原因：**错误码error\_code出现在payload里，收到该错误后连接不会断开。没有获取到有效的输入音频数据，ASR无法识别。

**解决方案：**检查是否有音频数据发送，重新输入正确的音频数据。

## **426-**InvalidTtsVoice

```
{"header":{"event":"result-generated","task_id":"xxxxx","status_code":200,"status_name":"Success","status_message":"Success"},"payload":{"output":{"event":"Error","dialog_id":"xxxxx","round_id":"xxxxx","llm_request_id":"xxxxx","error_code":426,"error_name":"InvalidTtsVoice","error_message":"tts voice error , need xxx voice."}}}
```

### tts voice error , need xxx voice.

**原因：**错误码error\_code出现在payload里，收到该错误后连接不会断开。音色参数 voice 取值错误，选择的音色不是当前的语音合成模型支持的音色。

**解决方案：**将voice修正为正确的音色。

（1）官方音色：

-   参考官方文档：cosyvoice-v2 / cosyvoice-v3 / cosyvoice-v3-plus / cosyvoice-v3-flash 支持的官方音色参考[音色列表](https://help.aliyun.com/zh/model-studio/cosyvoice-voice-list)，qwen-tts-realtime / qwen3-tts 支持的官方音色参考[支持的音色](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#422789c49bqqx)，sambert支持的音色参考[模型列表](https://help.aliyun.com/zh/model-studio/sambert-java-sdk#74cedcb97el0b)（去掉开头的"sambert-"和末尾的"-v1"后就是voice的取值）。
    
-   其他语音合成模型的音色都可以在多模态交互控制台上查看：在左侧**语音交互**配置区域选择对应的语音合成模型，点击右侧**语音交互体验**区域的右上角即可查看可用的音色列表。
    

（2）复刻音色，确认音色状态为“OK”后才能使用。查询方法参考[查询指定音色](https://help.aliyun.com/zh/model-studio/cosyvoice-clone-design-api#34490e5a2by7z)。

## **451-**NoSpeechRecognized

```
{"header":{"event":"result-generated","task_id":"xxxxx","status_code":200,"status_name":"Success","status_message":"Success"},"payload":{"output":{"event":"Error","dialog_id":"xxxxx","round_id":"xxxxx","llm_request_id":"xxxxx","error_code":451,"error_name":"NoSpeechRecognized","error_message":"No speech recognized from audio!"}}}
```

### No speech recognized from audio!

**原因：**错误码error\_code出现在payload里，收到该错误后连接不会断开。服务没有识别到用户讲话，通常是push2talk模式下，用户发送了SendSpeech后，没有说话就又发送了StopSpeech指令。其他模式下也有极少数情况是由背景噪音引起。

**解决方案：**检查消息发送的逻辑，确认是否有用户说话的音频数据发送到服务端。

## **500-InternalSynthesizerError/InternalAsrError /InternalLLMError/LLMTimeoutError**

```
{"header":{"event":"result-generated","task_id":"xxxxx","status_code":200,"status_name":"Success","status_message":"Success"},"payload":{"output":{"event":"Error","dialog_id":"xxxxx","round_id":"xxxxx","llm_request_id":"xxxxx","error_code":500,"error_name":"InternalAsrError","error_message":"Internal asr error"}}}
```

### Internal synthesizer error/Internal asr error/Internal LLM error/LLM response timeout

**原因：**错误码error\_code出现在payload里，收到此类错误后连接不会断开。服务内部错误，tts/asr/llm出错。

**解决方案：**出现此类错误时，可以重新发起请求来恢复使用。如果需要确认具体原因，请记录出错时完整的request\_id和dialog\_id，联系技术支持。
