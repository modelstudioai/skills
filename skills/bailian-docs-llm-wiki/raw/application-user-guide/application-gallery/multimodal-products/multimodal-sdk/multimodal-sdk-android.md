# 移动端Android SDK

本文介绍了如何使用阿里云百炼大模型服务提供的实时多模交互移动端 Android SDK，包括SDK下载安装、关键接口及代码示例。

MultiModalDialog SDK是阿里云千问团队提供的支持音视频端到端多模实时交互的SDK。通过SDK对接千问大模型以及后端多种Agent，能够支持用户接入语音对话、天气、音乐、新闻等多种能力，并支持视频和图像的大模型对话能力。

## **多模态实时交互服务架构**

![多模态实时交互服务接入架构-通用-流程图](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7227370571/p976841.jpg)

## **前提条件**

-   开通阿里云百炼实时多模交互应用，获取[Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)、[APP ID](https://bailian.console.aliyun.com/?tab=app#/app/app-market/multi-modal-app/myApp)和[API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。
    
-   下载SDK和 Demo并配置必要的环境、依赖。
    
-   导入示例代码，按照调用流程接入SDK。
    
-   您可以直接运行压缩包中的 APK 测试程序，填入上方三个必要参数，即可进行测试。
    

Package

Version

[bailian-multi-modal-android-sdk-1.0.6.5.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260513/soazyy/bailian-multi-modal-android-sdk-1.0.6.5.zip)

1.0.6.5

## **SDK接入**

### **交互数据链路说明**

SDK使用WebSocket协议与服务端交互，支持AudioOnly和AudioAndVideo 两种模式：

-   音频交互：仅支持音频和文本对话功能。
    
-   音视频交互：在交互中通过指令方式进入视频通话模式，客户端持续向服务端发送图片序列，实现端到端的音视频多模交互能力。
    

### **交互模式说明**

SDK支持 **Push2Talk**、 **Tap2Talk**和**Duplex**（全双工）三种交互模式。

-   Push2Talk: 长按说话，抬起结束的收音方式。
    
-   Tap2Talk: 点击开始说话，自动判断用户说话结束的收音方式。
    
-   Duplex: 全双工交互，连接开始后支持任意时刻开始说话，支持语音打断。
    

### **调用说明**

SDK及其调用Demo。

#### **SDK引用**

导入依赖库。

-   app/src/main/libs
    
    -   convsdk-release\_\*.aar //阿里云VoiceChatSDK
        
    -   multimodal\_dialog\_sdk.aar // 阿里云多模对话SDK
        
    -   multimodal\_dialog\_tongyimetathings.aar //使用 License 模式接入服务使用的鉴权 SDK
        
-   其他Demo APP 引入的依赖：
    
    参考`app/build.gradle`
    
    ```
    implementation libs.androidbootstrap
    implementation libs.okhttp
    implementation libs.okio //Android OKHttp3应用要增加一个收发IO的okio包
    implementation libs.http.logging.interceptor
    implementation libs.core.ktx
    ```
    

#### **关键参数**

参数名称

是否必须

值

说明

url

是

String

请求的服务端地址。

WebSocket 链路地址：wss://dashscope.aliyuncs.com/api-ws/v1/inference

api\_key

是

String

百炼服务接入[API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。请您在百炼平台创建API\_KEY，移动端为了安全考虑，您也可以在服务端接入[短时Token](https://help.aliyun.com/zh/model-studio/generate-temporary-api-key)，并下发给客户端使用。

workspace\_id

是

String

百炼管控台，业务空间 ID。

app\_id

是

String

您在管控台创建的应用 ID。

chain\_mode

是

String

WebSocket。

#### **Demo简介**

-   **EntranceActivity** 入口页面，需要修改url/api\_key/app\_id等信息。
    
    -   可以通过页面选择对话使用Tap2Talk或者Duplex等模式。
        
    -   使用 License 模式，请参考子文档【[使用 License 模式接入Android SDK](https://help.aliyun.com/zh/model-studio/multimodal-license-android)】。
        
-   **MultimodalDialogActivity**，对话交互实现类。
    
    -   Demo页面中引用TYAudioRecorder 作为录音输入，您可以替换为自己的实现。
        
    -   Demo页面使用AudioPlayer作为音频播放输出，您可以选择使用自己的实现类。
        
    -   Demo在音频交互模式下，支持VQA（图生文）功能，即通过语音说"拍照识别xxx"，触发服务下发拍照意图。之后：
        
        -   您可以将本地拍照并上传OSS（或其他内容服务生成公共链接），触发单张图片的识别和对话。
            
        -   您也可以直接上传图片的 base64 数据，向服务请求图片识别对话结果。
            
    -   Demo在VideoAndAudio音视频交互模式下，目前通过外部采集的方式输入图像序列，方便眼镜等IoT设备的采集和视频对话接入。
        

#### **接口设计**

##### **MultimodalDialog 对话入口类**

1.  MultiModalDialog
    
    初始化对话类，传入必要的全局参数。
    
    ```
    /**
         * 初始化     
         * @param context: 上下文
         * @param url: 服务器地址
         * @param chainMode: 链路模式
         * @param workspaceId: 工作空间id
         * @param appId: 应用id
         * @param dialogMode: 对话模式
         * */
        fun MultiModalDialog(
            context: Context,
            url: String?,
            chainMode: ChainMode?,
            workspaceId: String?,
            appId: String?,
            dialogMode: DialogMode?
        )
    ```
    
2.  createConversation
    
    创建会话。
    
    ```
    /**
         * 初始化成功后，启动对话流程
         * @param params 初始化参数
         * @param chatCallback 主回调，除了初始化过程的所有消息，都会从这里透出给上层
         */
        fun createConversation(@NonNull MultiModalRequestParam params,chatCallback: IConversationCallback)
    ```
    
3.  start
    
    开始对话。
    
    ```
    /**
         * 连接,启动对话
         */
        fun start()
    ```
    
4.  stop
    
    结束对话。
    
    ```
    /**
         * 断开,结束对话
         */
        fun stop()
    ```
    
5.  destroy
    
    ```
    /**
         * 销毁实例
         */
        fun destroy()
    ```
    
6.  setConversationTimeout
    
    设置超时时间。
    
    ```
    /**
         * 设置对话超时时间,当服务未在指定时间内检出用户说话，上报timeout事件
         * @param timeout 超时时间,单位ms
         */
        fun setConversationTimeout(timeout: Long)
    ```
    
7.  interrupt
    
    打断交互。
    
    ```
    /**
         * 打断AI说话
         */
        fun interrupt()
    ```
    
8.  startSpeech
    
    通知服务端开始上传音频，注意需要在Listening状态才可以调用。只需要在Push2Talk模式下调用。
    
    ```
    /**
     * 通知服务端开始上传音频，注意需要在Listening状态才可以调用。
     * 只需要在Push2Talk模式下调用。
     */
    fun startSpeech()
    ```
    
9.  sendAudioData
    
    通知服务端上传音频。
    
    ```
    /**
     * 通知服务端上传音频。
     * @param audioData 音频帧数据
     */
    fun sendAudioData(audioData: ByteArray?)
    ```
    
10.  stopSpeech
     
     通知服务端结束上传音频。只需要在Push2Talk模式下调用。
     
     ```
     /**
      * 通知服务端结束上传音频。只需要在Push2Talk模式下调用。
      * Push2Talk 用户结束说话
      */
     fun stopSpeech()
     ```
     
11.  requestToRespond
     
     请求服务端回答指定问题或做TTS播放出来。
     
     ```
     /**
          * 请求服务端回答指定问题或做TTS播放出来
          * @param type: transcript 表示直接把文本转语音，prompt 表示把文本送大模型回答
          * @param text：对应的文本
          * @param params: 额外参数
          */
         fun requestToRespond(type: String, text: String, params: JSONObject)
     ```
     
12.  其他接口。
     
     ```
     /**
          * 当前配置是否是全双工模式
          */
         fun isDuplexMode(): Boolean
     
         /**
          * Push2Talk 用户取消说话
          */
         fun cancelSpeech()
     
         /**
          * 发送语音回复结束
          * */
         fun sendResponseEnded()
         
         /**
          * 发送语音回复开始
          * */
         fun sendResponseStarted()
     
         /**
          * 推送视频帧
          *
          * @param videoFrame 视频帧
          * @param callback: 送帧结果回调
          */
         fun sendVideoFrame(videoFrame: TYVideoFrame,callback: IVideoChatPushFrameCallback)
     ```
     

###### **关键参数枚举**

##### 参数

值

说明

##### ChainMode

WebSocket

支持AudioOnly和AudioAndVideo两种交互

##### DialogMode

TAP2TALK

手动开始，自动结束

PUSH2TALK

手动开始，手动结束

DUPLEX

全双工交互

###### **MultiModalRequestParam 端云交互参数详情**

**Start - Input Message**

请求开始会话消息。服务收到Start消息后，向客户端发送**Started**消息。

**一级参数**

**二级参数**

**类型**

**是否必选**

**说明**

task\_group

string

是

任务组名称，固定为"aigc"，请直接复制使用

task

string

是

任务名称，固定为"multimodal-generation"，请直接复制使用

function

string

是

调用功能，固定为"generation"，请直接复制使用

model

string

是

阿里云百炼模型名称，固定为"multimodal-dialog"，请直接复制使用

input

directive

string

是

指令名称：Start

workspace\_id

string

是

客户在阿里云百炼业务空间ID（[Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)），可在**多模态交互开发套件控制**台，点击左下角业务空间名称，“业务空间详情”中查看，目前仅支持主账号默认工作空间。

app\_id

string

是

客户创建的应用ID（[APP ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#2612f896detsz)），可在**多模态交互开发套件**控制台的“我的应用”页面查看

dialog\_id

string

否

对话ID，默认不填时是开启新会话，服务端会自动生成并在事件中下发，格式示例："12345678-1234-1234-1234-1234567890ab"，共36个字符。当希望继续之前的对话时，把当时服务端下发的dialog\_id在这里传入

parameters

upstream

object

是

参数说明参考下方 [parameters.upstream的参数说明](#c70ad23b46rng)表格

downstream

object

否

参数说明参考下方 [parameters.downstream的参数说明](#18bc9ff97bxur)表格

client\_info

object

是

参数说明参考下方 [parameters.client\_info的参数说明](#51228f3bc17yk)表格

biz\_params

object

否

参数说明参考下方 [parameters.biz\_params的参数说明](#eb89a03bfdk00)表格

**parameters.upstream**的参数说明如下**：**

**一级参数**

**类型**

**是否必选**

**说明**

type

string

是

上行类型：

AudioOnly 仅语音通话

mode

string

否

客户端使用的模式，默认**tap2talk。**

可选项：

-   push2talk: 客户端控制模式。
    
-   tap2talk: 点击模式。
    
-   duplex: 双工模式。
    

三种模式的对比可以参考下方的[客户端使用的三种模式对比](#5e82453407pum)表格。

audio\_format

string

否

音频格式，支持pcm，raw-opus，默认为pcm

sample\_rate

int

否

语音识别的采样率，支持范围：

-   8000
    
-   16000
    
-   24000
    
-   48000
    

默认为16000

vocabulary\_id

string

否

热词id，设置该参数时会覆盖管控台热词配置。当管控台提供的热词不能满足客户需求时，可以考虑用Open API程序化管理热词，参见[热词API文档](https://next.api.aliyun.com/document/MultimodalDialog/2025-09-03/Vocabulary)

**parameters.downstream**的参数说明如下：

**一级参数**

**类型**

**是否必选**

**说明**

voice

string

否

合成语音的音色，支持范围取决于用户在管控台选择的语音合成模型

sample\_rate

int

否

合成语音的采样率，支持范围：

-   8000
    
-   16000
    
-   24000
    
-   48000
    

默认为24000。

千问-TTS、千问3-TTS模型仅支持24000。

audio\_format

string

否

音频格式，支持pcm，opus，mp3，raw-opus，默认为pcm。

千问-TTS模型仅支持pcm。

注意：opus 和 raw-opus的区别是opus格式的每一包数据都有额外ogg封装（[RFC 7845](https://www.rfc-editor.org/rfc/rfc7845.html)）

frame\_size

int

否

合成音频的帧大小，取值范围：

-   10
    
-   20
    
-   40
    
-   60
    
-   100
    
-   120
    

默认值为60，单位ms

只在合成音频格式为opus或raw-opus时生效

volume

int

否

合成音频的音量，取值范围0-100，默认50

speech\_rate

int

否

合成音频的语速，取值范围50-200，表示默认语速的50%-200%，默认100

pitch\_rate

int

否

合成音频的声调，取值范围50-200，默认100

bit\_rate

int

否

合成音频的比特率，取值范围：6~510kbps，默认值为32，单位kbps，只在合成音频格式为opus或raw-opus时生效

intermediate\_text

string

否

控制返回给用户哪些中间文本：

-   transcript：返回用户语音识别结果
    
-   dialog：返回对话系统回答中间结果
    

可以设置多种，以逗号分隔，默认为transcript

transmit\_rate\_limit

int

否

下发音频发送速率限制，单位：字节每秒

incremental\_response

boolean

否

是否增量返回大模型结果，true为增量，false为全量。默认为false，全量下发

instruction

string

否

设置指令，用于控制方言、情感等合成效果。该功能仅适用于cosyvoice-v3-flash模型的复刻音色，以及[音色列表](https://help.aliyun.com/zh/model-studio/cosyvoice-voice-list)中标记为支持Instruct的系统音色。

instruction有固定格式要求，具体格式参考此文档里的“instruction”参数说明。[Java SDK](https://help.aliyun.com/zh/model-studio/cosyvoice-java-sdk)

**parameters.client\_info**的参数说明如下：

**一级参数**

**二级参数**

**类型**

**是否必选**

**说明**

user\_id

string

是

终端用户ID，客户根据自己业务规则生成，用来针对不同终端用户实现定制化功能。最大长度36个字符。

device

uuid

string

否

客户端全局唯一的ID，需要用户自己生成并传入SDK，最大长度40个字符。一个终端用户可以有多个设备，那么每一个设备的uuid都不同，但user\_id相同。

network

ip

string

否

调用方公网IP

location

latitude

string

否

调用方纬度信息，在需要客户端精确位置的业务场景提交

longitude

string

否

调用方经度信息，在需要客户端精确位置的业务场景提交

city\_name

string

否

调用方所在城市，指明客户端粗略位置

**parameters.biz\_params**的参数说明如下：

**一级参数**

**类型**

**是否必选**

**说明**

user\_defined\_params

json object

否

需要透传给agent的参数，各类agent传递的参数参考[调用官方Agent](https://help.aliyun.com/zh/model-studio/official-agent)文档说明

user\_prompt\_params

json object

否

用于设置用户自定义prompt变量，由用户自定义设置json中的key和value。管控台上配置自定义prompt变量的方法参考[应用配置-提示词](https://help.aliyun.com/zh/model-studio/multimodal-app-configuration#74a8b82973u0r)

user\_query\_params

json object

否

用于设置用户自定义对话变量，由用户自定义设置json中的key和value。管控台上配置自定义对话变量的方法参考[应用配置-对话变量](https://help.aliyun.com/zh/model-studio/multimodal-app-configuration#62d90ef075ve1)

**客户端使用的三种模式对比：**

**对比项**

**push2talk**

**tap2talk**

**duplex**

类型

客户端控制模式

点击模式

双工模式

音频上传方式

按需

持续

Listening状态超过20秒不上传音频即报错

持续

任何状态超过20秒不上传音频都报错

VAD检测方

客户端

服务端

服务端

打断方式

[RequestToSpeak](https://help.aliyun.com/zh/model-studio/multimodal-interaction-protocol#8f987c58ddg2i)消息打断

[RequestToSpeak](https://help.aliyun.com/zh/model-studio/multimodal-interaction-protocol#8f987c58ddg2i)消息打断

语音打断

使用场景

由用户控制开始/结束客户端语音发送和识别，适用于按键说话，松开停止说话的场景。

客户端需持续上传音频，服务端自动检测语音活动的场景。但不支持用户语音打断大模型输出，只能发送RequestToSpeak打断消息。

客户端需持续上传音频，服务端自动检测语音活动的场景。用户随时可以说话打断大模型输出。

示例如下：

```
{
    "header": {
        "action":"run-task",
        "task_id": "f894c16f-f20e-4c1d-837e-89e0fbc63a43",
        "streaming":"duplex"
    },
    "payload": {
        "task_group":"aigc",
        "task":"multimodal-generation", // 任务类型：多模态生成
        "function":"generation",
        "model":"multimodal-dialog", // 模型名称：多模态对话（注意与task不同）
        "input":{
          "directive": "Start",
          "workspace_id": "llm-***********",
          "app_id": "****************"
        },
        "parameters":{
          "upstream":{
            "type": "AudioOnly",
            "mode": "duplex"
          },
          "downstream":{
            "voice": "longxiaochun_v2",
            "sample_rate": 24000
          },
          "client_info":{
            "user_id": "bin********207",
            "device":{
              "uuid": "432k*********k449"
            },
            "network":{
              "ip": "203.0.113.10"
            },
            "location":{
              "city_name": "北京市"
            }
          },
          "biz_params":{
            "user_defined_params": {
                "agent_id_xxxxx": {
                    "name": "value"
                }
            },
            "user_prompt_params": {
                "name": "value"
            },
            "user_query_params": {
                "name": "value"
            }
          }
        }
    }
}
```

##### **IConversationCallback （回调接口）**

```
/**
     * 对话启动结果，鉴权、客户端加入通道成功后，会回调该消息
     */
    fun onStartResult(isSuccess: Boolean, errorInfo: TYError?)

    /**
     * 主动打断的回调，包括手动打断和语音打断
     */
    fun onInterruptResult(isSuccess: Boolean, errorInfo: TYError?)

    /**
     * 对话准备完成，多端（客户端/VoiceChat/视频理解）均加入通道后，会回调该消息，此时才能调用业务接口
     */
    fun onReadyToSpeech()

    /**
     * 状态切换回调
     * 包含DIALOG_IDLE，DIALOG_LISTENING，DIALOG_RESPONDING，DIALOG_THINKING
     */
    fun onConvStateChangedCallback(state: DialogState)

    /**
     * 音量强度回调
     * @param audioType 参考 {@link Constant.TYVolumeSourceType}
     * @param audioLevel 0-100
     */
    fun onConvSoundLevelCallback(audioLevel: Float, audioType: Constant.TYVolumeSourceType)

    /**
     * 超出用户有效输入超时时间，收到此事件，用户需要重新启动或者结束对话
     * @param timeout 超时时间
     */
    fun onSpeechTimeout(timeout: Long)

    /**
     * 回路音频，用于客户端AEC回声消除
     * @param bytes 音频数据
     */
    fun onPlaybackAudioData(bytes: ByteArray)

    /**
     * 对话过程中的异常信息
     * @param errorInfo 异常信息
     */
    fun onErrorReceived(errorInfo: TYError)

    /**
     * 对话过程中的事件信息
     * @param errorInfo 事件信息
     */
    fun onConvEventCallback(var1: ConvEvent?)

    /**
     * 运行过程中回调关键日志信息给上层
     * @param level 日志级别，参考Android.Log
     * @param type 日志类型
     * @param debugInfo 日志信息
     */
    fun onDebugInfoTrack(level: Int, type: Constant.TYDebugInfoType, debugInfo: String)
```

###### **onConvEventCallback AI对话 Response详情**

-   EVENT\_HUMAN\_SPEAKING\_DETAIL
    
    语音识别内容
    
    ##### **SpeechContent - response**
    
    一级参数
    
    二级参数
    
    三级参数
    
    类型
    
    是否必选
    
    说明
    
    output
    
    event
    
    string
    
    是
    
    事件名称：SpeechContent
    
    dialog\_id
    
    string
    
    是
    
    对话 ID。
    
    text
    
    string
    
    是
    
    用户语音识别出的文本，流式**全量**输出
    
    finished
    
    bool
    
    是
    
    输出是否结束
    
    ```
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
    
-   EVENT\_RESPONDING\_DETAIL
    
    大模型的返回文本
    
    output
    
    finished
    
    bool
    
    是
    
    输出是否结束
    
    dialog\_id
    
    string
    
    是
    
    对话 ID。
    
    event
    
    string
    
    是
    
    消息类型
    
    text
    
    string
    
    否
    
    大模型返回的文本结果。
    
    spoken
    
    string
    
    否
    
    大模型返回的播放内容的文本，可能跟 text 字段有所不同。
    
    extra\_info
    
    object
    
    否
    
    其他扩展信息，目前支持：
    
    commands: 命令字符串
    
    agent\_info: 智能体信息
    
    tool\_calls: 插件返回的信息
    
    dialog\_debug: 对话debug信息
    
    timestamps: 链路中各节点时间戳
    
    示例：
    
    ```
    {
        "header": {
            "event":"result-generated",
            "task_id": "9B32878******************3D053"
        },
        "payload": {
            "output":{
              "event": "RequestAccepted",
              "dialog_id": "b39398c9dd8147********35cdea81f7",
              "text": "您输入了数字序列「12345」。如果您有关于这些数字的问题或者需要我用它们来完成某项任务，请告诉我更多的细节，我会尽力帮助您。",
              "spoken": "您输入了数字序列「12345」。如果您有关于这些数字的问题或者需要我用它们来完成某项任务，请告诉我更多的细节，我会尽力帮助您。",
              "finished": true,
            "extra_info": {
              "commands": "[{\"name\":\"VOLUME_SET\",\"params\":[{\"name\":\"series\",\"normValue\":\"70\",\"value\":\"70\"}]}]",
              "tool_result": [{
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
              }]
            }
            },
            "usage":{
              "invoke":10,
              "model_x":10
            }
        }
    }
    ```
    

#### **异常处理**

##### **onErrorReceived - response**

#### **通用错误码**

如遇报错问题，请参见[多模态交互套件-错误码](https://help.aliyun.com/zh/model-studio/multimodal-error-code)进行排查。

若问题仍未解决，请联系技术支持，反馈遇到的问题，并提供完整的request\_id和dialog\_id，以便进一步排查问题。

#### **调用时序**

##### **全双工交互**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0921377471/p957926.png)

##### **半双工交互**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0921377471/p957927.png)

## **更多SDK接口使用说明**

### **双工交互**

移动端Android SDK支持Duplex 双工交互模式。 在双工交互模式下，SDK支持在播放语音合成回复的同时，输入录音数据。当用户在此时说话时，服务会自动打断当前播报数据返回 (客户端播放器缓存需要应用层处理)，并开始新的回复。

双工交互需要实现回声消除（AEC，Acoustic Echo Cancellation），Android SDK内置了回声消除算法。当您需要使用双工交互时，仍需要您进行必要的配置。

-   输入麦克风录音音频
    

请将实时录音获取的音频数据通过如下接口传入SDK。

```
multiModalDialog.sendAudioData(data);
```

-   输入参考通道音频
    

请将实时播放的音频数据通过如下接口传入SDK。注意传入数据需要保证与当前播放数据一致。

```
multiModalDialog.sendRefData(data);
```

### **VQA交互**

VQA 是在对话过程中通过发送图片实现图片+语音的多模交互的功能。

核心过程是语音或者文本请求拍照意图触发**"visual\_qa"**拍照指令。

当客户端通过回调函数`onConvEventCallback`收到拍照指令后， 发送图片链接或者base64数据（支持小于 180 KB 的图片）。

-   处理"visual\_qa" command和上传拍照。
    

```
private void executeCmd(String cmd,String dialogId,String taskId){
  String cmdName = null;
  String cmdParamValue = null;
  try {
    cmdName = new JSONArray(cmd).getJSONObject(0).getString("name");
  }catch (Exception ex) {
    ex.printStackTrace();
  }
  switch (cmdName){
     case "visual_qa":
       JSONObject extraObject = new JSONObject();
       extraObject.put("images", imagesArray);
       multimodalConversation.requestToRespond(type, text, extraObject.toString());
       break;
  ......
}

//上传拍照
public static JSONArray getMockOSSImage() {
    JSONObject imageObject = new JSONObject();
    JSONArray images = new JSONArray();
    try{
      if (vqaUseUrl){
        imageObject.put("type", "url");
        imageObject.put("value", "https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7043267371/p909896.png");
      }else {
        imageObject.put("type", "base64");
        imageObject.put("value", getLocalImageBase64());
      }
      images.put(imageObject);

    }catch (Exception e){
      e.printStackTrace();
    }
    return images;
  }
```

### **通过 WebSocket 链路请求LiveAI**

LiveAI （视频通话）是百炼多模交互提供的官方Agent。通过Android 全功能版本SDK， 您也可以在 WebSocket 链路中通过自行录制视频帧的方式来调用视频通话功能。

注意：通过 WebSocket 调用 LiveAI发送图片只支持base64编码，每张图片的大小在 180 KB 以下。

-   LiveAI调用时序
    

#### ![截屏2025-06-20 11](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1903140571/p975541.png)

-   关键代码示例
    

请注意参照如下的调用流程实现 通过 WebSocket 协议调用 LiveAI。

```
//1. 设置交互类型为AudioAndVideo
MultiModalRequestParam.UpStream.builder().mode("duplex").type("AudioAndVideo").build();

//2. 在建联后发送voicechat_video_channel 请求
private void startVideoMode() {
    if (isVideoMode) return;

    try {
        MultiModalRequestParam updateParams = MultiModalRequestParam.builder().build();
        JSONObject videoObj = new JSONObject();
        videoObj.put("action", "connect");
        videoObj.put("type", "voicechat_video_channel");

        List<JSONObject> videos = new ArrayList<>();
        videos.add(videoObj);

        updateParams.setBizParams(MultiModalRequestParam.BizParams.builder()
                .videos(videos).build());

        multiModalDialog.requestToRespond("prompt", "", updateParams.getParametersAsJson());
        multiModalDialog.setVideoContainer(videoContainer, uiHandler);

        isVideoMode = true;
        runOnUiThread(() -> videoContainer.setVisibility(View.VISIBLE));

    } catch (JSONException e) {
        Log.e(TAG, "启动视频模式失败", e);
    }
}

//3. 每 500ms 提交一张视频帧照片数据，注意图片尺寸小于 180 KB。
/**
 * DEMO 流程未调用。演示在 websocket 链路中实现 liveAI
 * 启动视频帧流，每 500ms 发送一次图片帧
 */
private void startVideoFrameStreaming() {
    Thread videoStreamingThread = new Thread(() -> {
        try {
            while ( !Thread.currentThread().isInterrupted()) {
                Thread.sleep(500);

                JSONObject extraObject = new JSONObject();
                extraObject.put("images", getMockOSSImage());

                multiModalDialog.updateInfo(extraObject);
                }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        } catch (JSONException e) {
            throw new RuntimeException(e);
        }
    });

    videoStreamingThread.setDaemon(true);
    videoStreamingThread.setName("LiveAI-VideoStreaming");
    videoStreamingThread.start();

}

/**
 * build images list request
 * */
private static JSONArray getMockOSSImage() {
    JSONObject imageObject = new JSONObject();
    JSONArray images = new JSONArray();
    try{

        imageObject.put("type", "base64");
        imageObject.put("value", getLocalImageBase64());

        images.put(imageObject);

    }catch (Exception e){
        e.printStackTrace();
    }
    return images;
}

//read local image to base64
private static String getLocalImageBase64(){
    return "";
}
```

### **文本合成TTS**

SDK支持通过文本直接请求服务端合成音频。

您需要在客户端处于Listening状态下发送`requestToRespond`请求。

若当前状态非Listening，需要先调用`Interrupt` 接口打断当前播报。

```
conversation.requestToRespond("transcript","幸福是一种技能，是你摒弃了外在多余欲望后的内心平和。",null);
```

### **自定义提示词变量和传值**

-   在管控台项目【提示词】配置自定义变量。
    

例如，定义了一个`user_name`字段代表用户昵称。并将变量`user_name`以占位符形式${user\_name} 插入到Prompt 中。

在**提示词**编辑页面顶部，单击**{x} 自定义变量**按钮添加所需的自定义变量。

-   在代码中设置变量。
    

如下示例，设置`"user_name" = "大米"`。

```
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

### **ASR结果即时纠错**

在对话过程中，ASR 识别结果有可能出现错误或者非预期的结果。 除了配置热词之外，您也可以通过即时纠错功能接口上传词表进行实时干预。

-   参数说明。
    

通过配置UpStream的AsrPostProcessing 参数来配置纠错词表。

参数

一级参数

二级参数

类型

说明

AsrPostProcessing

Object

ASR 纠错词表

ReplaceWord\[\]

List

词表列表，每个ReplaceWord 对应一组词的替换规则

source

String

需要被替换的文本

target

String

替换目标文本

match\_mode

String

匹配模式，默认为exact：

**exact**：整句精确匹配，只有文本与source完全相同才匹配成功

**partial**：部分匹配，文本中部分字符与source相同即匹配成功

```
//构建AsrPostProcessing对象
MultiModalRequestParam.UpStream.ReplaceWord replaceWord = new MultiModalRequestParam.UpStream.ReplaceWord();
    replaceWord.setTarget("一加一");
    replaceWord.setSource("1加1");
    replaceWord.setMatchMode("partial");
// 在创建对话请求时将asrPostProcessing 传入UpStream.AsrPostProcessing
.upStream(MultiModalRequestParam.UpStream.builder()
.asrPostProcessing(Collections.singletonList(replaceWord))
.build())
```
