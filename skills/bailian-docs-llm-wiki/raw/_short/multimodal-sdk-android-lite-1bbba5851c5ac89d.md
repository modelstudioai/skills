# Android Lite SDK

本文介绍了如何使用阿里云百炼大模型服务提供的实时多模交互移动端 Android Lite SDK，包括SDK下载安装、关键接口及代码示例。

MultiModalDialog SDK是阿里云通义团队提供的支持音视频端到端多模实时交互的SDK。通过SDK对接千问大模型以及后端多种Agent，能够支持用户接入语音对话、天气、音乐、新闻等多种能力，并支持视频和图像的大模型对话能力。

<a id="多模态实时交互服务架构"></a>

<a id="f9224da564gai"></a>

## 多模态实时交互服务架构

![多模态实时交互服务接入架构-通用-流程图](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7227370571/p976841.jpg)

<a id="前提条件"></a>

<a id="3b0a8f6803lko"></a>

## 前提条件

-   开通阿里云百炼实时多模交互应用，获取[Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)、[APP ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#2612f896detsz)和[API Key](../model-api-reference/preparations/get-api-key.md)。

<a id="sdk接入"></a>

<a id="08beccbec49rz"></a>

## SDK接入

<a id="交互数据链路说明"></a>

<a id="d2dba24286nyf"></a>

### 交互数据链路说明

多模对话Android Lite SDK仅支持Websocket链路与服务端交互，并支持AudioOnly 音频模式进行对话：

-   音频交互：推荐使用Websocket 连接，连接速度较快，性能要求较低。
    
    -   WS 链路音频格式说明：
        
        -   上行：支持 pcm 和 opus 格式音频进行语音识别。
        -   下行：支持 pcm 和 mp3 音频流。

<a id="交互模式说明"></a>

<a id="35fbcbeefdnz1"></a>

### 交互模式说明

SDK支持 **Push2Talk**、 **Tap2Talk**和**Duplex**（全双工）三种交互模式。

-   Push2Talk: 长按说话，抬起结束的收音方式。
    
-   Tap2Talk: 点击开始说话，自动判断用户说话结束的收音方式。
    
-   Duplex: 全双工交互，连接开始后支持任意时刻开始说话，支持语音打断。
    
    注意：全双工交互需要客户端集成回声消除算法（AEC），Lite SDK不提供此算法模块。您可以自行集成回声消除算法模块，或者使用百炼多模对话全功能[移动端Android SDK](multimodal-sdk-android-5c6fac2dfb609de2.md)。
    

<a id="调用说明"></a>

<a id="76dd0830c98c7"></a>

### 调用说明

SDK及其调用Demo。

-   下载SDK和Demo [dashscope-lite-android-1.0.2.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250723/mesbwx/dashscope-lite-android-1.0.2.zip)并配置必要的环境、依赖。
-   导入压缩包中的示例代码，按照调用流程接入SDK。

<a id="sdk引用"></a>

<a id="8ae2c34e8fwd3"></a>

#### SDK引用

导入依赖库。

-   app/src/main/libs
    
    -   dashscope-multimodal-dialog-lite-1.\*.aar //阿里云多模交互Lite SDK
-   其他Demo APP引入的依赖：
    
    参考`app/build.gradle`
    

<a id="code-block"></a>

```groovy
implementation 'com.alibaba:fastjson:1.1.76.android'
implementation 'org.java-websocket:Java-WebSocket:1.5.7'
```

<a id="关键参数"></a>

<a id="ce029139edy2m"></a>

#### 关键参数

| 参数名称 | 是否必须 | 值 | 说明 |
| --- | --- | --- | --- |
| url | 是 | String | 请求的服务端地址。 |
| api\_key | 是 | String | 百炼服务接入[API Key](../model-api-reference/preparations/get-api-key.md) 请您在百炼平台创建API\_KEY，移动端为了安全考虑，您也可以在服务端接入[短时Token](../model-api-reference/more-about-models/generate-temporary-api-key.md)，并下发给客户端使用。 |
| workspace\_id | 是 | String | 百炼管控台，工作空间id。 |
| app\_id | 是 | String | 您在管控台创建的应用id。 |

<a id="demo简介"></a>

<a id="df4a2743e8bxz"></a>

#### Demo简介

-   **EntranceActivity** 入口页面，需要修改url/api\_key/app\_id等信息。
    
    -   可以通过页面选择对话使用Tap2Talk或者Push2Talk等模式。
-   **MultimodalDialogActivity**，对话交互实现类。
    
    -   Demo页面中引用TYAudioRecorder 作为录音输入，您可以替换为自己的实现。
        
    -   Demo页面使用AudioPlayer作为音频播放输出，您可以选择使用自己的实现类。
        
    -   Demo在音频交互模式下，支持VQA（图生文）功能，即通过语音说“拍照识别xxx”，触发服务下发拍照意图。之后：
        
        -   您可以将本地拍照并上传OSS（或其他内容服务生成公共链接），触发单张图片的识别和对话。
        -   您也可以直接上传图片的base64请求服务或者图片的对话结果。

<a id="接口设计"></a>

<a id="948a6af067omr"></a>

#### 接口设计

<a id="ad6675a229cee"></a>

##### MultimodalDialog 对话入口类

1.  MultiModalDialog
    
    初始化对话类，传入必要的全局参数。
    

<a id="code-block-2"></a>

```text
/**
 * 初始化
 * @param context: 上下文
 * @param url: 服务器地址
 * @param workspaceId: 工作空间id
 * @param appId: 应用id
 * @param dialogMode: 对话模式
 * */
    fun MultiModalDialog(
        context: Context,
        url: String?,
        workspaceId: String?,
        appId: String?,
        dialogMode: DialogMode?
    )
```

2.  createConversation
    
    创建会话。
    

<a id="code-block-3"></a>

```text
/**
 * 初始化成功后，启动对话流程
 * @param params 初始化参数
 * @param chatCallback 主回调，除了初始化过程的所有消息，都会从这里透出给上层
 */
 fun createConversation(@NonNull MultiModalRequestParam params,chatCallback: IConversationCallback)
```

3.  start
    
    开始对话。
    

<a id="code-block-4"></a>

```text
/**
 * 连接,启动对话
 * @param apiKey: 百炼服务apikey ，推荐使用短时apiKey
 * @param dialogId: 对话id，可选，传值继承之前的对话历史
 */
 fun start(String apiKey, String dialogId)
```

4.  stop
    
    结束对话。
    

<a id="code-block-5"></a>

```text
/**
 * 断开,结束对话
 */
fun stop()
```

5.  destroy

<a id="code-block-6"></a>

```text
/**
 * 销毁实例
 */
fun destroy()
```

6.  interrupt
    
    打断交互。
    

<a id="code-block-7"></a>

```text
/**
 * 打断AI说话
 */
fun interrupt()
```

7.  startSpeech
    
    通知服务端开始上传音频，注意需要在Listening状态才可以调用。只需要在Push2Talk模式下调用。
    

<a id="code-block-8"></a>

```text
/**
 * 通知服务端开始上传音频，注意需要在Listening状态才可以调用。
 * 只需要在Push2Talk模式下调用。
 */
fun startSpeech()
```

8.  sendAudioData
    
    通知服务端上传音频。
    

<a id="code-block-9"></a>

```text
/**
 * 通知服务端上传音频。
 * @param audioData 音频帧数据
 */
fun sendAudioData(byte[] data)
```

9.  stopSpeech
    
    通知服务端结束上传音频。只需要在Push2Talk模式下调用。
    

<a id="code-block-10"></a>

```text
/**
 * 通知服务端结束上传音频。只需要在Push2Talk模式下调用。
 * Push2Talk 用户结束说话
 */
fun stopSpeech()
```

10.  requestToRespond
     
     请求服务端回答指定问题or做TTS播放出来。
     

<a id="code-block-11"></a>

```text
/**
 * 请求服务端回答指定问题or做TTS播放出来
 * @param type: transcript 表示直接把文本转语音，prompt 表示把文本送大模型回答
 * @param text：对应的文本
 * @param params: 额外参数
 */
fun requestToRespond(type: String, text: String, params: MultiModalRequestParam)
```

11.  其他接口。

<a id="code-block-12"></a>

```text
/**
 * 发送语音回复结束
 */
fun sendResponseEnded()

/**
 * 发送语音回复开始
 */
fun sendResponseStarted()

```

<a id="c81c93c0e11xc"></a>

###### 关键参数枚举

<table><thead><tr><th><h5><strong>参数</strong></h5></th><th><p><strong>值</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td rowspan="3"><h5>DialogMode</h5></td><td><p>TAP2TALK</p></td><td><p>手动开始，自动结束</p></td></tr><tr><td><p>PUSH2TALK</p></td><td><p>手动开始，手动结束</p></td></tr><tr><td><p>DUPLEX</p></td><td><p>全双工交互</p></td></tr></tbody></table>

<a id="33f91b5e5d9fb"></a>

###### MultiModalRequestParam 端云交互参数详情

<table><thead><tr><th><p><strong>一级参数</strong></p></th><th><p><strong>二级参数</strong></p></th><th><p><strong>三级参数</strong></p></th><th><p><strong>四级参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>是否必选</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td rowspan="3"><p>input</p></td><td><p>workspace_id</p></td><td></td><td></td><td><p>string</p></td><td><p>是</p></td><td><p>用户业务空间id</p></td></tr><tr><td><p>app_id</p></td><td></td><td></td><td><p>string</p></td><td><p>是</p></td><td><p>客户在管控台创建的应用id，可以根据值规律确定使用哪个对话系统</p></td></tr><tr><td><p>dialog_id</p></td><td></td><td></td><td><p>string</p></td><td><p>否</p></td><td><p>对话id，如果传入表示接着聊</p></td></tr><tr><td rowspan="18"><p>parameters</p></td><td rowspan="3"><p>upstream</p></td><td><p>type</p></td><td></td><td><p>string</p></td><td><p>是</p></td><td><p>上行类型：</p><p>AudioOnly 仅语音通话</p><p>AudioAndVideo 上传视频</p></td></tr><tr><td><p>mode</p></td><td></td><td><p>string</p></td><td><p>否</p></td><td><p>客户端使用的模式，可选项：</p><ul><li><p>push2talk</p></li><li><p>tap2talk</p></li><li><p>duplex</p></li></ul><p>默认tap2talk</p></td></tr><tr><td><p>audio_format</p></td><td></td><td><p>string</p></td><td><p>否</p></td><td><p>音频格式，支持pcm，opus，默认为pcm</p></td></tr><tr><td rowspan="4"><p>downstream</p></td><td><p>voice</p></td><td></td><td><p>string</p></td><td><p>否</p></td><td><p>合成语音的音色</p></td></tr><tr><td><p>sample_rate</p></td><td></td><td><p>int</p></td><td><p>否</p></td><td><p>合成语音的采样率（单位：Hz），默认采样率24000Hz</p></td></tr><tr><td><p>intermediate_text</p></td><td></td><td><p>string</p></td><td><p>否</p></td><td><p>控制返回给用户那些中间文本：</p><p>transcript 返回用户语音识别结果</p><p>dialog 返回对话系统回答中间结果</p><p>可以设置多种，以逗号分割，默认为transcript</p></td></tr><tr><td><p>audio_format</p></td><td></td><td><p>string</p></td><td><p>否</p></td><td><p>音频格式，支持pcm，mp3，默认为pcm</p></td></tr><tr><td rowspan="6"><p>client_info</p></td><td><p>user_id</p></td><td></td><td><p>string</p></td><td><p>是</p></td><td><p>终端用户id，用来做用户相关的处理</p></td></tr><tr><td><p>device</p></td><td><p>uuid</p></td><td><p>string</p></td><td><p>否</p></td><td><p>客户端全局唯一的id，需要用户自己生成，传入SDK</p></td></tr><tr><td><p>network</p></td><td><p>ip</p></td><td><p>string</p></td><td><p>否</p></td><td><p>调用方公网ip</p></td></tr><tr><td rowspan="3"><p>location</p></td><td><p>latitude</p></td><td><p>string</p></td><td><p>否</p></td><td><p>调用方维度信息</p></td></tr><tr><td><p>longitude</p></td><td><p>string</p></td><td><p>否</p></td><td><p>调用方经度信息</p></td></tr><tr><td><p>city_name</p></td><td><p>string</p></td><td><p>否</p></td><td><p>调用方所在城市</p></td></tr><tr><td rowspan="5"><p>biz_params</p></td><td><p>user_defined_params</p></td><td></td><td><p>object</p></td><td><p>否</p></td><td><p>其他需要透传给agent的参数</p></td></tr><tr><td><p>user_defined_tokens</p></td><td></td><td><p>object</p></td><td><p>否</p></td><td><p>透传agent所需鉴权信息</p></td></tr><tr><td><p>tool_prompts</p></td><td></td><td><p>object</p></td><td><p>否</p></td><td><p>透传agent所需prompt</p></td></tr><tr><td><p>user_query_params</p></td><td></td><td><p>object</p></td><td><p>否</p></td><td><p>透传用户请求自定义参数</p></td></tr><tr><td><p>user_prompt_params</p></td><td></td><td><p>object</p></td><td><p>否</p></td><td><p>透传用户prompt自定义参数</p></td></tr></tbody></table>

<a id="290dc8b301e60"></a>

##### IConversationCallback （回调接口）

<a id="code-block-13"></a>

```text
/**
  * 鉴权通过，Websocket连接建立
  */
fun onConnected()

/**
  * 对话建立，开始对话流程
  */
fun onStarted(dialogId: String)

/**
   * 状态切换
   * 包含DIALOG_IDLE，DIALOG_LISTENING，DIALOG_RESPONDING，DIALOG_THINKING
   */
fun onConvStateChangedCallback(state: State.DialogState)

/**
   * 超出用户有效输入超时时间的超时时间，收到此事件，用户需要重新启动或者结束对话
   * @param timeout 超时时间
   */
fun onSpeechTimeout(timeout: Long)

/**
   * 对话过程中的异常信息
   * @param errorInfo 异常信息
   */
fun onErrorReceived(errorCode: Int, errorMessage: String)

/**
   * 合成tts音频回调
   * @param bytes 音频数据
   */
fun onSynthesizedSpeech(bytes: ByteArray)

/**
   * 对话结束
   */
fun onStopped()

/**
   * 检测到用户开始说话
   */
fun onSpeechStarted()

/**
   * 检测到用户说话结束
   */
fun onSpeechEnded()

/**
   * 打断请求被接受
   */
fun onRequestAccepted()

/**
   * 云端开始下发tts回复
   */
fun onRespondingStarted()

/**
   * 云端下发tts回复结束
   */
fun onRespondingEnded(output: Map<String, Any>)

/**
   * 语音识别内容
   */
fun onSpeechContent(output: Map<String, Any>)

/**
   * 对话响应内容
   */
fun onRespondingContent(output: Map<String, Any>)

/**
   * websocket连接关闭
   */
fun onClosed(closeCode: Int, reason: String)
```

<a id="ee9c017bdds3h"></a>

###### 重要回调方法说明

-   onSpeechContent(output: Map<String, Any>)
    
    语音识别内容
    
    <a id="03cb5f06fcxu5"></a>
    
    ##### SpeechContent - response
    
    | 一级参数 | 二级参数 | 三级参数 | 类型 | 是否必选 | 说明 |
    | --- | --- | --- | --- | --- | --- |
    | output | event |  | string | 是 | 事件名称：SpeechContent |
    |  | dialog\_id |  | string | 是 | 对话id |
    |  | text |  | string | 是 | 用户语音识别出的文本，流式全量输出 |
    |  | finished |  | bool | 是 | 输出是否结束 |
    
    <a id="code-block-14"></a>
    
    ```json
    {
        "header": {
            "request_id": "9B32878******************3D053",
            "service_id": "368208df",
            "status_code": 200,
            "status_name": "Success",
            "status_message": "Success.",
            "attributes":{
              "user_id":"1234557879x"
            }
        },
        "payload": {
            "output":{
              "event": "SpeechContent",
              "dialog_id": "b39398c9dd8147********35cdea81f7",
              "text": "一二三",
              "finished": false
            },
            "usage":{
              "invoke":10,
              "model_x":10
            }
        }
    }
    ```
    
-   onRespondingContent(output: Map<String, Any>)
    
    大模型的返回文本
    
    <table><thead><tr><th><p><strong>一级参数</strong></p></th><th><p><strong>二级参数</strong></p></th><th><p><strong>三级参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>是否必选</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td rowspan="6"><p>output</p></td><td><p>finished</p></td><td></td><td><p>bool</p></td><td><p>是</p></td><td><p>输出是否结束</p></td></tr><tr><td><p>dialog_id</p></td><td></td><td><p>string</p></td><td><p>是</p></td><td><p>对话id</p></td></tr><tr><td><p>event</p></td><td></td><td><p>string</p></td><td><p>是</p></td><td><p>消息类型</p></td></tr><tr><td><p>text</p></td><td></td><td><p>string</p></td><td><p>否</p></td><td><p>LLM大模型返回的文本结果</p></td></tr><tr><td><p>spoken</p></td><td></td><td><p>string</p></td><td><p>否</p></td><td><p>LLM大模型返回的播放内容的文本，可能跟 text 字段有所不同。</p></td></tr><tr><td><p>extra_info</p></td><td></td><td><p>object</p></td><td><p>否</p></td><td><p>其他扩展信息，目前支持：</p><p>commands: 命令字符串</p><p>agent_info: 智能体信息</p><p>tool_calls: 插件返回的信息</p><p>dialog_debug: 对话debug信息</p><p>timestamps: 链路中各节点时间戳</p></td></tr></tbody></table>
    
    示例：
    
    <a id="code-block-15"></a>
    
    ```json
    {
        "header": {
            "event": "result-generated",
            "task_id": "9B32878******************3D053"
        },
        "payload": {
            "output": {
                "event": "RequestAccepted",
                "dialog_id": "b39398c9dd8147********35cdea81f7",
                "text": "您输入了数字序列\"12345\"。如果您有关于这些数字的问题或者需要我用它们来完成某项任务，请告诉我更多的细节，我会尽力帮助您。",
                "spoken": "您输入了数字序列\"12345\"。如果您有关于这些数字的问题或者需要我用它们来完成某项任务，请告诉我更多的细节，我会尽力帮助您。",
                "finished": true,
                "extra_info": {
                    "commands": "[{\"name\":\"VOLUME_SET\",\"params\":[{\"name\":\"series\",\"normValue\":\"70\",\"value\":\"70\"}]}]",
                    "tool_result": [
                        {
                            "id": "",
                            "type": "function",
                            "function": {
                                "name": "function_name",
                                "arguments": "{\"id\": \"123\", \"name\": \"test\"}",
                                "outputs": "函数调用结果",
                                "status": {
                                    "code": 200,
                                    "message": "Success."
                                }
                            }
                        }
                    ]
                }
            },
            "usage": {
                "invoke": 10,
                "model_x": 10
            }
        }
    }
    ```
    

<a id="异常处理"></a>

<a id="b83dda5833kyf"></a>

#### 异常处理

<a id="e011088f10l8t"></a>

##### onErrorReceived - response

错误码以及对应的错误信息。

| 错误码 | 错误名称 | 说明 |
| --- | --- | --- |
| 40000000 | ClientError | 客户端错误 |
| 40000001 | InvalidParameter | 参数不合规，如参数缺失 |
| 40000002 | DirectiveNotSupported | 指令不支持，如指令名称错误 |
| 40000003 | MessageInvalid | 指令不合规，如指令格式错误 |
| 40000004 | ConnectError | 连接错误，如客户端或数字人RTC退出 |
| 40010000 | AccessDenied | 拒绝访问 |
| 40010001 | UNAUTHORIZED | 未授权 |
| 40020000 | DataInspectionFailed | 输入或输出触发绿网 |
| 50000000 | InternalError | 服务端内部错误，联系服务端排查 |
| 50000001 | UnknownError | 服务端内部未知错误，联系服务端排查 |
| 50010000 | InternalAsrError | asr内部错误 |
| 50020000 | InternalLLMError | 大模型内部错误 |
| 50030000 | InternalSynthesizerError | tts内部错误 |

<a id="调用时序"></a>

<a id="b6af8d622cqep"></a>

#### 调用时序

<a id="af5a6cc73bv6i"></a>

##### 半双工交互

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0921377471/p957927.png)

<a id="更多sdk接口使用说明"></a>

<a id="8e1dad4f24sb3"></a>

## 更多SDK接口使用说明

<a id="vqa交互"></a>

<a id="179a4ac1c22zs"></a>

### VQA交互

VQA 是在对话过程中通过发送图片实现图片+语音的多模交互的功能。

核心过程是语音或者文本请求拍照意图触发**"visual\_qa"**拍照指令。

当客户端通过回调函数`onRespondingContent`收到拍照指令后， 发送图片链接或者base64数据（支持小于180KB的图片）。

-   处理"visual\_qa" command和上传拍照。

<a id="code-block-16"></a>

```java
@Override
public void onRespondingContent(@NotNull final Map<String, ?> output) {
  Log.i(TAG,"onRespondingContent output:{"+output+"}");
  if (output.containsKey("extra_info")) {
    JSONObject extraInfo = (JSONObject) output.get("extra_info");
    try {
        if (extraInfo.containsKey("commands") && extraInfo.getString("commands") != null && extraInfo.getString("commands").contains("visual_qa")) {
        //包含vqa指令，这里简单实现
            uploadVQAImg();
            }
        } catch (JSONException e) {
            throw new RuntimeException(e);
        }
    }
}

//上传拍照
private void uploadVQAImg(){
    MultiModalRequestParam updateParams = null;
    JSONObject imageObject = new JSONObject();
    try{
        imageObject.put("type", "url");
        imageObject.put("value", vqaImgLink);
        List<JSONObject> images = new ArrayList<>();
        images.add(imageObject);
            updateParams= MultiModalRequestParam
                .builder()
                .images(images)
                    .build();
    }catch (JSONException e){
        e.printStackTrace();
    }
    Log.i(TAG, "uploadVQAImg: " + JSON.toJSONString(updateParams));
    multimodalDialog.requestToRespond("prompt", "",updateParams);
}
```

<a id="通过-websocket-链路请求liveai"></a>

<a id="6ff2cdacc27um"></a>

### 通过 Websocket 链路请求LiveAI

LiveAI （视频通话）是百炼多模交互提供的官方Agent。通过Android Lite SDK， 您也可以在Websocket链路中通过自行录制视频帧的方式来调用视频通话功能。

注意：通过 Websocket 调用 LiveAI发送图片只支持base64编码，每张图片的大小在180K以下。

-   LiveAI调用时序

<a id="e0a817e803bvl"></a>

#### ![截屏2025-06-20 11](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1903140571/p975541.png)

-   关键代码示例

请注意参照如下的调用流程实现 通过Websocket 协议调用 LiveAI。

<a id="code-block-17"></a>

```java
//1. 设置交互类型为AudioAndVideo
MultiModalRequestParam.UpStream.builder().mode(this.dialogMode.getValue()).type("AudioAndVideo").build();

//2. 在建联后发送voicechat_video_channel 请求
private void sendVideoChatCommand(){
    try {
        MultiModalRequestParam updateParams = MultiModalRequestParam.builder().build();
        org.json.JSONObject videoObj = new org.json.JSONObject();
        videoObj.put("action", "connect");
        videoObj.put("type", "voicechat_video_channel");

        List<org.json.JSONObject> videos = new ArrayList<>();
        videos.add(videoObj);

        updateParams.setBizParams(MultiModalRequestParam.BizParams.builder()
                .videos(videos).build());

        multimodalDialog.requestToRespond("prompt", "", updateParams);

    } catch (org.json.JSONException e) {
        Log.e(TAG, "启动视频模式失败", e);
    }
}

//3. 每 500ms 提交一张视频帧照片数据，注意图片尺寸小于 180KB。
/**
 * 演示在 websocket 链路中实现 liveAI
 * 启动视频帧流，每 500ms 发送一次图片帧
 */
private void startVideoFrameStreaming() {
    Thread videoStreamingThread = new Thread(new Runnable() {
        @Override
        public void run() {
            try {
                while (isVideoChatting && !Thread.currentThread().isInterrupted()) {
                    Thread.sleep(500);

                    MultiModalRequestParam updateParams = null;
                    try {

                        updateParams = MultiModalRequestParam
                                .builder()
                                .images(MultimodalDialogActivity.this.getImageList())
                                .build();
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }

                    multimodalDialog.updateInfo(updateParams);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            } catch (JSONException e) {
                throw new RuntimeException(e);
            }
        }
    });

    videoStreamingThread.setDaemon(true);
    videoStreamingThread.setName("LiveAI-VideoStreaming");
    videoStreamingThread.start();

}

/**
 * build images list request
 * */
private List getImageList() {
    AssetManager assetManager = getAssets();
    org.json.JSONObject imageObject = new org.json.JSONObject();
    List<org.json.JSONObject> images = new ArrayList<>();
    try{

        imageObject.put("type", "base64");
        imageObject.put("value", getImageBase64(assetManager.open("jpeg-bridge.jpg")));

        images.add(imageObject);

    }catch (Exception e){
        e.printStackTrace();
    }
    return images;
}

private String getImageBase64(InputStream file) { //200k以内大小图片
    try {

        byte[] bytes = new byte[file.available()];
        file.read(bytes);
        return Base64.encodeToString(bytes, Base64.NO_WRAP); //使用NO_WRAP 参数，避免换行
    } catch (Exception e) {
        e.printStackTrace();
    }
    return null;
}
```

<a id="文本合成tts"></a>

<a id="b8ccc5da4bb3b"></a>

### 文本合成TTS

SDK支持通过文本直接请求服务端合成音频。

您需要在客户端处于Listening状态下发送`requestToRespond`请求。

若当前状态非Listening，需要先调用`interrupt` 接口打断当前播报。

<a id="code-block-18"></a>

```java
multimodalDialog.requestToRespond("transcript","幸福是一种技能，是你摒弃了外在多余欲望后的内心平和。",null);
```

<a id="自定义提示词变量和传值"></a>

<a id="442af8d6f6i38"></a>

### 自定义提示词变量和传值

-   在管控台项目【提示词】配置自定义变量。

如下图示例，定义了一个`user_name`字段代表用户昵称。并将变量`user_name`以占位符形式${user\_name} 插入到Prompt 中。

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1903140571/p975545.png)

-   在代码中设置变量。

如下示例，设置`"user_name" = "大米"`。

<a id="code-block-19"></a>

```java
//在请求参数构建中传入biz_params.user_prompt_params
HashMap<String, String> userPromptParams = new HashMap<>();
userPromptParams.put("user_name", "大米");
        MultiModalRequestParam.BizParams bizParams = MultiModalRequestParam.BizParams
                .builder()
                .userPromptParams(userPromptParams)
                .build();
```

-   请求回复

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1903140571/p975544.png)
