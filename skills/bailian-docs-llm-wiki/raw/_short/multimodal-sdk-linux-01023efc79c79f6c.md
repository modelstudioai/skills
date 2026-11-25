# Linux C++ SDK

本文介绍了如何使用阿里云百炼大模型服务提供的实时多模交互 Linux C++ SDK，包括SDK下载安装、关键接口及代码示例。

<a id="前提条件"></a>

<a id="16080106289ux"></a>

## 前提条件

开通阿里云百炼实时多模交互应用，获取[Workspace ID](../application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md#732535cfc959h)、[APP ID](../application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md#2612f896detsz)和[API Key](../model-api-reference/preparations/get-api-key.md)。

<a id="多模态实时交互服务接入架构"></a>

<a id="f9224da564gai"></a>

## 多模态实时交互服务接入架构

![多模态实时交互服务接入架构-通用-流程图](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7227370571/p976841.jpg)

<a id="下载安装"></a>

<a id="985cb1a0a4zdz"></a>

## 下载安装

| 最新 SDK 包 | 平台 | MD5 |
| --- | --- | --- |
| [V1.4.10-02E-20260920\_Linux.tar.gz](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f9dfa.gz) | Linux x86\_64 | `eed1091b64c2ec60ab28bec873531e59` |
| [V1.4.10-02E-20260920\_Linux\_aarch64\_10.tar.gz](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f9df9.gz) | Linux aarch64 (gcc-arm-10.2) | `dfdb9bd7e8e6f7c48dfc04bc5b8bc452` |
| [V1.4.10-02E-20260920\_Linux\_aarch64\_11.tar.gz](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f9df8.gz) | Linux aarch64 (gcc-arm-11.2) | `d62c213f19f4a183c522eb32a80d7207` |

<a id="音频格式说明"></a>

<a id="cdddab24a0p96"></a>

## 音频格式说明

Websocket 链路音频格式说明：

-   上行：支持 pcm 和 opus 格式音频进行语音识别。仅支持用户送入pcm格式音频（16K采样率，16bit，单通道），opus格式音频由SDK内部自动完成编码。
-   下行：支持单通道 pcm、mp3和opus 音频流。其中opus音频流将会在SDK内部进行解码，用户收到的将是对应格式的pcm数据。

<a id="接口说明"></a>

<a id="a81d9436b0lvr"></a>

## 接口说明

<a id="createconversation"></a>

<a id="56c1ecb7f49ze"></a>

### CreateConversation

创建交互，设置回调。对应销毁接口为DestroyConversation。

<a id="code-block"></a>

```cpp
/**
 * @brief 创建交互，设置回调。对应销毁接口为DestroyConversation
 * @param onMessage : 各事件监听回调，参见下文具体回调
 * @param onEventTrackMessage : 用于SDK内部日志(info以上)通过回调送给上层
 * @param user_data : 回调返回
 * @return Conversation* : Conversation单例指针
 */
static Conversation* CreateConversation(
    const ConversationCallbackMethod onMessage,
    const EventTrackCallbackMethod onEventTrackMessage,
    void* user_data = NULL);
```

其中ConversationCallbackMethod类型如下：

<a id="conversationcallbackmethod"></a>

<a id="170b8b4761cjb"></a>

#### ConversationCallbackMethod

SDK事件回调

<a id="code-block-2"></a>

```cpp
/**
 * @brief SDK各事件回调
 * @param ConvEvent*
 * ：回调事件，可通过调用其中具体方法获得事件及相关信息。具体方法见下方ConvEvent
 * @param void* ：用户设置的user_data
 */
typedef void (*ConversationCallbackMethod)(ConvEvent*, void*);
```

<a id="414df0825e87w"></a>

##### ConvEvent

方法列表

<table><tbody><tr><td><p><strong>方法名</strong></p></td><td><p><strong>说明</strong></p></td></tr><tr><td><p>int GetStatusCode();</p></td><td><p>获取状态码，正常情况为0或者20000000，失败时对应的错误码。错误码参考SDK文档说明。</p></td></tr><tr><td><p>ConvEventType GetMsgType();</p></td><td><p>获取当前所发生Event的类型，详见<strong>ConvEventType</strong>。</p></td></tr><tr><td><p>ConvEventType GetSubMsgType();</p></td><td><p>获取当前所发生Event的子类型，当ConvEvent::kRTCMessage时使用。</p></td></tr><tr><td><p>const char* GetAllResponse();</p></td><td><p>获得此ConvEvent的完整JSON格式response。</p></td></tr><tr><td><p>const char* GetErrorMessage();</p></td><td><p>获得错误信息。</p></td></tr><tr><td><p>const char* GetTaskId();</p></td><td><p>获取本次连接唯一ID，定位问题建议用dialog_id和round_id。</p></td></tr><tr><td><p>const char* GetDialogId();</p></td><td><p>获取对话ID。</p></td></tr><tr><td><p>const char* GetRoundId();</p></td><td><p>获取本轮交互的ID。</p></td></tr><tr><td><p>std::vector&lt;unsigned char&gt; GetBinaryData();</p></td><td><p>获取云端返回的二进制数据。当ConvEvent::kBinary时使用。</p></td></tr><tr><td><p>unsigned char* GetBinaryDataInChar();</p></td><td><p>同GetBinaryData()。当ConvEvent::kBinary时使用。</p></td></tr><tr><td><p>int GetBinaryDataSize();</p></td><td><p>同GetBinaryData(), 获得这一次二进制数据的字节数，与GetBinaryDataInChar()搭配。当ConvEvent::kBinary时使用。</p></td></tr><tr><td><p>int GetDialogStateChanged();</p></td><td><p>获得对话当前状态，当ConvEvent::kDialogStateChanged时使用。</p><ul><li><p>0: DIALOG_IDLE</p></li><li><p>1: DIALOG_LISTENING</p></li><li><p>2: DIALOG_RESPONDING</p></li><li><p>3: DIALOG_THINKING</p></li></ul></td></tr><tr><td><p>float GetSoundDb();</p></td><td><p>返回最近一次输入音频的音量db值, 范围-160~0db，当ConvEvent::kSoundLevel时使用。</p></td></tr><tr><td><p>int GetSoundLevel();</p></td><td><p>返回最近一次输入音频的音量db值的分级, 范围0~100，当ConvEvent::kSoundLevel时使用。</p></td></tr><tr><td><p>int GetSampleRate();</p></td><td><p>返回此数据的采样率。当ConvEvent::kUserBinary时使用。</p></td></tr><tr><td><p>int GetChannelSelect();</p></td><td><p>返回音频数据的通道选择。</p><ul><li><p>0: 表示第一通道</p></li><li><p>1: 表示第二通道</p></li><li><p>2: 表示双通道</p></li></ul><p>当ConvEvent::kUserBinary时使用。</p></td></tr><tr><td><p>NetworkEventType GetNetworkEvent();</p></td><td><p>网络事件，详见<strong>NetworkEventType</strong>。当ConvEvent::kNetworkStatus时使用。</p></td></tr><tr><td><p>int GetNetworkLatency();</p></td><td><p>返回网络延迟信息, 单位为毫秒。当ConvEvent::kNetworkStatus时使用。</p></td></tr></tbody></table>

<a id="c62539183anmi"></a>

###### ConvEventType

|  |  |
| --- | --- |
| **事件名称** | **事件说明** |
| kConversationFailed | 会话任务发生错误，需要查看错误码及错误信息。收到此事件后需要根据错误信息判断如何处理，也可以使用此dialog\_id重新连接，继续会话。 |
| kConversationConnected | 与AI服务建连成功。 |
| kConversationInitialized | AI（服务端）初始化完成, 返回初始化信息。 |
| kConversationStarted | AI（服务端）登场, 会话任务成功启动, 建连成功。 |
| kConversationCompleted | AI（服务端）退场。任务成功完成，执行断连操作。 |
| kSentenceBegin | HUMAN开始说话。PushToTalk模式按键则触发此事件，TapToTalk和Duplex模式是用户开始说话触发此事件。 |
| kSentenceEnd | HUMAN说话结束。PushToTalk模式按键松开则触发此事件，TapToTalk和Duplex模式是用户说话结束触发此事件。 |
| kDataOutputStarted | AI（服务端）开始传送TTS数据。 |
| kDataOutputCompleted | AI（服务端）TTS数据合成完成且发送完成。 |
| kBinary | 表示此ConvEvent中包含AI(服务端)传回的TTS数据包。 |
| kSoundLevel | 最近一次传入的HUMAN说话声音数据的音量值。 |
| kDialogStateChanged | 对话状态发生变化。 |
| kInterruptAccepted | AI（服务端）接收指令打断（如按键打断）请求。 |
| kInterruptDenied | AI（服务端）拒绝指令打断（如按键打断）请求。 |
| kVoiceInterruptAccepted | AI（服务端）接收语音打断请求。 |
| kVoiceInterruptDenied | AI（服务端）拒绝语音打断请求。 |
| kConnectionDisconnected | SDK与服务端断开链接。 |
| kConnectionConnected | SDK与服务端链接。 |
| kHumanSpeakingDetail | 用户语音识别出的详细信息，比如文本。 |
| kRespondingDetail | 系统对外输出的详细信息，比如LLM大模型返回的结果。 |
| kNetworkStatus | 网络状态信息, 比如网络延迟。 |
| kKeywordSpotted | 触发唤醒。 |
| kKeywordTrusted | 触发唤醒并确认确实唤醒。 |
| kVoiceTimeout | 触发唤醒后长时间无人说话退出唤醒态。 |
| kOtherMessage | 未定义消息。 |
| kUserBinary | RTC模式使用，表示此ConvEvent中包含HUMAN（用户）传回的MIC数据包。 |
| kRTCMessage | 表示将事件整理成RTC消息，具体事件查看GetSubMsgType()。 |
| kConversationStart | RTC模式使用，"StartedReceived"事件。 |
| kConversationStop | RTC模式使用，"Stop"事件。 |
| kSendSpeech | RTC模式使用，"SendSpeech"事件。 |
| kStopSpeech | RTC模式使用，"StopSpeech"事件。 |
| kRequestToSpeak | RTC模式使用，"RequestToSpeak"事件。 |
| kRequestToRespond | RTC模式使用，"RequestToRespond"事件。 |
| kLocalRespondingStarted | RTC模式使用，"LocalRespondingStarted"事件。 |
| kLocalRespondingEnded | RTC模式使用，"LocalRespondingEnded"事件。 |
| kAvatarStateChanged | RTC模式使用，"AvatarStateChanged"事件。 |

<a id="5257d03510o8i"></a>

###### NetworkEventType

|  |  |
| --- | --- |
| **事件名称** | **事件说明** |
| kNetworkEventUnknown | 无。 |
| kNetworkEventLatency | 网络延迟事件。 |

其中EventTrackCallbackMethod类型如下：

<a id="eventtrackcallbackmethod"></a>

<a id="32acded1ec2tg"></a>

#### EventTrackCallbackMethod

获得关键埋点信息日志

<a id="code-block-3"></a>

```cpp
/**
 * @brief SDK内部日志通过回调送给用户处理
 * @param ConvLogLevel ：返回日志的日志级别
 * @param const char* ：具体日志字符串
 * @param void* ：用户设置的user_data
 */
typedef void (*EventTrackCallbackMethod)(ConvLogLevel, const char*, void*);

enum ConvLogLevel {
  kConvLogLevelVerbose,
  kConvLogLevelDebug,
  kConvLogLevelInfo,
  kConvLogLevelWarning,
  kConvLogLevelError,
  kConvLogLevelNone,
};
```

<a id="destroyconversation"></a>

<a id="96f4373d6ftl4"></a>

### DestroyConversation

销毁交互。对应创建接口为CreateConversation。

<a id="code-block-4"></a>

```cpp
/**
 * @brief 销毁交互，若交互进行中，则内部完成Disconnect()
 * @return ConvRetCode : 状态码
 */
ConvRetCode DestroyConversation();
```

<a id="connect"></a>

<a id="b74e4d0e80q92"></a>

### Connect

组装一个start请求，用于发起对服务端的链接。返回成功并不代表与VoiceChat Server链接成功，仅代表发起start请求构建成功，是否链接成功以返回的Response为准。

<a id="code-block-5"></a>

```cpp
/**
 * @brief 与服务端建立链接
 * @param params ：json string形式的初始化参数
 * @return ConvRetCode : 状态码
 */
ConvRetCode Connect(const char* params);
```

<a id="百炼参数设置说明"></a>

<a id="87b66e60c0yma"></a>

#### 百炼参数设置说明

<table><tbody><tr><td><strong>一级参数</strong></td><td><strong>二级参数</strong></td><td><strong>三级参数</strong></td><td><strong>类型</strong></td><td><strong>必须</strong></td><td><strong>说明</strong></td></tr><tr><td><p>apikey</p></td><td></td><td></td><td><p>String</p></td><td><p>是</p></td><td><p>临时凭证，具体请查看<a href="../model-api-reference/preparations/get-api-key.md">获取与配置 API Key</a>。</p></td></tr><tr><td><p>workspace</p></td><td></td><td></td><td><p>String</p></td><td><p>是</p></td><td><p>资源文件所在目录，即资源文件所在目录。</p><p>若为02C版本（纯云端RTC），可不设置。</p><p>若为02A/02E版本（带本地AEC&amp;VAD），必须设置。</p></td></tr><tr><td><p>url</p></td><td></td><td></td><td><p>String</p></td><td><p>是</p></td><td><p>请求的网关域名，百炼请求域名：&quot;wss://dashscope.aliyuncs.com/api-ws/v1/inference&quot;，设置百炼请求域名时则ws_version自动切换到百炼交互协议。</p></td></tr><tr><td><p>chain_mode</p></td><td></td><td></td><td><p>String</p><p>/</p><p>int</p></td><td><p>是</p></td><td><p>默认“ws”或0。可选“ws”或0、“rtc”或1，前者启用Websocket交互方式，后者启用RTC交互方式。</p></td></tr><tr><td><p>ws_version</p></td><td></td><td></td><td><p>int</p></td><td><p>否</p></td><td><p>交互协议版本，默认情况无需设置。</p><p>若url设置为百炼域名，此参数自动设置为3，即选择百炼协议。</p></td></tr><tr><td><p>rtc_version</p></td><td></td><td></td><td><p>int</p></td><td><p>否</p></td><td><p>交互协议版本，默认情况无需设置。</p><p>若使用百炼交互协议，此参数设置为3。</p></td></tr><tr><td><p>app_id</p></td><td></td><td></td><td><p>String</p></td><td><p>是</p></td><td><p>url选用百炼域名时即ws_version为3时，必填app_id，否则无需设置。</p></td></tr><tr><td><p>workspace_id</p></td><td></td><td></td><td><p>String</p></td><td><p>是</p></td><td><p>用户业务空间id。</p></td></tr><tr><td><p>dialog_id</p></td><td></td><td></td><td><p>String</p></td><td><p>否</p></td><td><p>对话id，空代表新的对话，传入则代表继续通话。格式为32位随机字符串。</p></td></tr><tr><td><p>mode</p></td><td></td><td></td><td><p>String</p></td><td><p>否</p></td><td><p>运行模式，默认&quot;duplex&quot;或&quot;mix_duplex&quot;。</p><ul><li>full_duplex：启用本地能力(VAD、AEC)，且云端提升打断效果的全双工模式。</li><li>duplex/mix_duplex：启用本地能力(VAD、AEC)的全双工模式。</li><li>tap2talk/tap_to_talk：可点击打断的交互模式。</li><li>push2talk/push_to_talk</li><li>kws_duplex/mix_kws_duplex：duplex/mix_duplex模式基础上，前置唤醒功能。</li><li>cloud_duplex：未启用本地能力(VAD、AEC)的双工模式。</li></ul><p>注意：SDK中的AEC为软件AEC， 需使用回声硬参考，保障mic和ref时延严格稳定对齐。推荐使用硬件AEC。</p></td></tr><tr><td><p>debug_path</p></td><td></td><td></td><td><p>String</p></td><td><p>否</p></td><td><p>日志和音频文件存储目录，不设置则会在workspace下创建debug目录。</p></td></tr><tr><td><p>save_log</p></td><td></td><td></td><td><p>boolean</p></td><td><p>否</p></td><td><p>是否存储日志，默认false。</p></td></tr><tr><td><p>save_wav</p></td><td></td><td></td><td><p>boolean</p></td><td><p>否</p></td><td><p>是否存储音频，默认false。</p></td></tr><tr><td><p>log_level</p></td><td></td><td></td><td><p>String</p></td><td><p>否</p></td><td><p>日志级别，默认&quot;info&quot;或2，可选择&quot;verbose/debug/info/warn(warning)/error&quot;或0/1/2/3/4。</p></td></tr><tr><td><p>ping_interval_ms</p></td><td></td><td></td><td><p>int</p></td><td><p>否</p></td><td><p>统计网络延迟的操作间隔，即每次上报网络延迟回调的间隔时间，单位毫秒。不小于1000ms。</p></td></tr><tr><td><p>channel_select</p></td><td></td><td></td><td><p>int</p></td><td><p>否</p></td><td><ul><li>0：送回第一通道数据，即对VAD友好的音频数据。</li><li>1：送回第二通道数据，即对ASR友好的音频数据。</li><li>2：默认设置，即VAD+ASR组成的双通道数据。</li></ul><p>若为02C版本（纯云端RTC），则默认1，即返回MIC的音频数据。</p></td></tr><tr><td rowspan="3"><p>voice_activity_detection_attributes</p></td><td></td><td></td><td><p>JSONObject</p></td><td><p>否</p></td><td><p>人声检测VAD相关参数。</p></td></tr><tr><td><p>enable_external_vad_module</p></td><td></td><td><p>boolean</p><p>/</p><p>String</p></td><td><p>否</p></td><td><p>启用外部VAD模块，启用后即设置true/&quot;true&quot;时，将关闭内部VAD模块，使用外部VAD。</p></td></tr><tr><td><p>enable_vad_module</p></td><td></td><td><p>boolean</p><p>/</p><p>String</p></td><td><p>否</p></td><td><p>启用VAD模块，默认为false/&quot;false&quot;。此参数与enable_external_vad_module联合设置，两者均为false/&quot;false&quot;时，表示关闭VAD模块，只使用云端VAD功能。</p></td></tr><tr><td rowspan="2"><p>acoustic_echo_cancelling_attributes</p></td><td></td><td></td><td><p>JSONObject</p></td><td><p>否</p></td><td><p>回声消除AEC相关参数。</p></td></tr><tr><td><p>enable_external_aec_module</p></td><td></td><td><p>boolean</p><p>/</p><p>String</p></td><td><p>否</p></td><td><p>启用外部AEC模块，启用后即设置true/&quot;true&quot;时，将关闭内部AEC模块，且会忽略送入的Ref音频（也可不送入），只使用送入的Mic音频。默认false/&quot;false&quot;，即使用内部AEC模块。</p></td></tr><tr><td rowspan="6"><p>key_words_spotting_attributes</p></td><td></td><td></td><td><p>JSONObject</p></td><td><p>否</p></td><td><p>唤醒相关参数。</p></td></tr><tr><td><p>enable_external_kws_module</p></td><td></td><td><p>boolean</p><p>/</p><p>String</p></td><td><p>否</p></td><td><p>启用外部KWS模块，启用后即设置true/&quot;true&quot;时，将关闭内部KWS模块，由外部SetAction(kKeywordTrusted)来通知触发唤醒，SDK可继续后续交互流程。</p><p>&quot;kws_duplex&quot;模式有效。</p></td></tr><tr><td><p>independent_kws_mode</p></td><td></td><td><p>bool</p></td><td><p>否</p></td><td><p>启用内部KWS模块的独立运行模式，默认为false。当启用时，KWS模块触发唤醒词时，SDK内部不会继续进行下一步流程，而是等待用户调用SetAction(kContinue)后SDK才继续进行下一步交互。即这段期间用户可以做其他业务相关的工作。</p><p>&quot;kws_duplex&quot;模式有效。</p></td></tr><tr><td><p>vad_asleep_tail_timeout</p></td><td></td><td><p>int</p></td><td><p>否</p></td><td><p>说话人说话后多久时间未触发唤醒，则返回最初状态，默认为2000ms，单位为ms。</p><p>&quot;kws_duplex&quot;模式有效。</p></td></tr><tr><td><p>vad_awake_front_timeout</p></td><td></td><td><p>int</p></td><td><p>否</p></td><td><p>唤醒后和唤醒识别后，说话人多久未说话，则退出唤醒态返回最初状态，默认为5000ms，单位ms。</p><p>&quot;kws_duplex&quot;模式有效。</p></td></tr><tr><td><p>word_list</p></td><td></td><td><p>JSONArray</p></td><td><p>否</p></td><td><p>自定义唤醒词设置。默认无需设置，未设置时使用唤醒资源文件中的默认配置。</p><ul><li><code>activation</code>：是否启用此唤醒词。</li><li><code>name</code>：唤醒词。</li><li><code>type</code>：唤醒词类型，取值为 <code>wakeup</code> 或 <code>main</code>。</li><li><code>threshold1</code>：唤醒阈值。</li></ul><a id="code-block-6"></a><pre class="language-json"><code>{
  &quot;word_list&quot;: [
    {
      &quot;activation&quot;: true,
      &quot;name&quot;: &quot;小白小白&quot;,
      &quot;type&quot;: &quot;wakeup&quot;,
      &quot;threshold1&quot;: 0.01
    },
    {
      &quot;activation&quot;: false,
      &quot;name&quot;: &quot;小云小云&quot;,
      &quot;type&quot;: &quot;wakeup&quot;
    }
  ]
}
</code></pre></td></tr><tr><td rowspan="5"><p>upstream</p></td><td></td><td></td><td><p>JSONObject</p></td><td><p>是</p></td><td></td></tr><tr><td><p>type</p></td><td></td><td><p>String</p></td><td><p>是</p></td><td><p>上行类型：</p><p>AudioOnly 仅语音通话。</p><p>AudioAndVideo 上传视频。</p></td></tr><tr><td><p>mode</p></td><td></td><td><p>String</p></td><td><p>否</p></td><td><p>运行模式，默认“duplex”，可选“tap2talk/push2talk”。</p><p>&quot;kws_duplex&quot;模式在这里设置为&quot;duplex&quot;。</p></td></tr><tr><td><p>sample_rate</p></td><td></td><td><p>int</p></td><td><p>否</p></td><td><p>上行语音的采样率，支持范围：</p><ul><li>8000</li><li>16000</li><li>24000</li><li>48000</li></ul><p>默认为16000。</p></td></tr><tr><td><p>audio_format</p></td><td></td><td><p>String</p></td><td><p>否</p></td><td><p>上行音频格式，默认为pcm，可选opus。</p><p>pcm：用户送入pcm音频数据。</p><p>opus：用户送入pcm音频数据，SDK内部编码成opus进行传送。注意，full_duplex和cloud_duplex模式不支持此格式。</p><p>raw-opus：用户送入pcm音频数据，SDK内部编码成raw-opus进行传送。</p></td></tr><tr><td rowspan="11"><p>downstream</p></td><td></td><td></td><td><p>JSONObject</p></td><td><p>否</p></td><td></td></tr><tr><td><p>type</p></td><td></td><td><p>String</p></td><td><p>否</p></td><td><p>下行媒体类型：</p><p>Text：不需要下发语音。</p><p>Audio：输出语音，默认值。</p></td></tr><tr><td><p>voice</p></td><td></td><td><p>String</p></td><td><p>否</p></td><td><p>合成语音的音色，支持范围取决于用户在<a href="https://bailian.console.aliyun.com/?tab=app#/app/app-market/multi-modal-app">管控台</a>的应用配置中选择的TTS模型和可选音色。具体选择范围可参考<a href="cosyvoice-websocket-sdk-python-47e109e34183e539.md#model-cosyvoice">Python SDK</a>。</p></td></tr><tr><td><p>sample_rate</p></td><td></td><td><p>int</p></td><td><p>否</p></td><td><p>合成语音的采样率，默认由服务端指定。支持范围：</p><ul><li>16000</li><li>24000</li><li>48000</li></ul><p>默认为24000。</p></td></tr><tr><td><p>audio_format</p></td><td></td><td><p>String</p></td><td><p>否</p></td><td><p>下行音频格式，默认为pcm，可设置pcm、mp3和opus。用户接收到的音频参数为单通道、16bit。</p><p>注意：若用户设置opus，则由SDK内部将opus解码成pcm数据送还给用户。若用户设置mp3和pcm，则直接透传给用户。</p></td></tr><tr><td><p>volume</p></td><td></td><td><p>int</p></td><td><p>否</p></td><td><p>合成音频的音量，取值范围0-100，默认50。</p></td></tr><tr><td><p>speech_rate</p></td><td></td><td><p>int</p></td><td><p>否</p></td><td><p>合成音频的语速，取值范围50-200，表示默认语速的50%-200%，默认100。</p></td></tr><tr><td><p>pitch_rate</p></td><td></td><td><p>int</p></td><td><p>否</p></td><td><p>合成音频的声调，取值范围50-200，默认100。</p></td></tr><tr><td><p>frame_size</p></td><td></td><td><p>int</p></td><td><p>否</p></td><td><p>合成音频的帧大小，单位为毫秒。仅在downstream.audio_format为opus时生效。</p><p>取值范围：10、20、40、60、100、120。默认为60。</p></td></tr><tr><td><p>transmit_rate_limit</p></td><td></td><td><p>int</p></td><td><p>否</p></td><td><p>合成音频发送速率限制，单位：字节每秒。默认无限制。</p></td></tr><tr><td><p>intermediate_text</p></td><td></td><td><p>String</p></td><td><p>否</p></td><td><p>控制返回给用户中间文本：</p><p>transcript 返回用户语音识别结果。</p><p>dialog 返回对话系统回答中间结果。</p><p>可以设置多种，以逗号分割，默认为transcript。</p></td></tr><tr><td rowspan="10"><p>client_info</p></td><td></td><td></td><td><p>JSONObject</p></td><td><p>是</p></td><td></td></tr><tr><td><p>user_id</p></td><td></td><td><p>String</p></td><td><p>是</p></td><td><p>终端用户 ID，由客户根据业务规则生成，用于针对不同终端用户实现定制化功能。最大长度为 36 个字符。</p></td></tr><tr><td rowspan="2"><p>device</p></td><td></td><td><p>JSONObject</p></td><td><p>否</p></td><td><p>终端用户id，用来做用户相关的处理。</p></td></tr><tr><td><p>uuid</p></td><td><p>String</p></td><td><p>否</p></td><td><p>客户端全局唯一的 ID，需要用户自行生成并传入 SDK，最大长度为 40 个字符。同一终端用户可以有多个设备，各设备的 uuid 不同，但 user_id 相同。</p></td></tr><tr><td rowspan="2"><p>network</p></td><td></td><td><p>JSONObject</p></td><td><p>否</p></td><td><p>终端用户id，用来做用户相关的处理。</p></td></tr><tr><td><p>ip</p></td><td><p>String</p></td><td><p>否</p></td><td><p>调用方公网ip。</p></td></tr><tr><td rowspan="4"><p>location</p></td><td></td><td><p>JSONObject</p></td><td><p>否</p></td><td><p>终端用户id，用来做用户相关的处理。</p></td></tr><tr><td><p>latitude</p></td><td><p>String</p></td><td><p>否</p></td><td><p>调用方维度信息。</p></td></tr><tr><td><p>longitude</p></td><td><p>String</p></td><td><p>否</p></td><td><p>调用方经度信息。</p></td></tr><tr><td><p>city_name</p></td><td><p>String</p></td><td><p>否</p></td><td><p>调用方所在城市。</p></td></tr><tr><td rowspan="5"><p>biz_params</p></td><td></td><td></td><td><p>JSONObject</p></td><td><p>否</p></td><td></td></tr><tr><td><p>user_defined_params</p></td><td></td><td><p>JSONObject</p></td><td><p>否</p></td><td><p>其他需要透传给agent的参数。</p></td></tr><tr><td><p>user_defined_tokens</p></td><td></td><td><p>JSONObject</p></td><td><p>否</p></td><td><p>透传agent所需鉴权信息。</p></td></tr><tr><td><p>user_prompt_params</p></td><td></td><td><p>JSONObject</p></td><td><p>否</p></td><td><p>用于设置并传入用户自定义的提示词中的变量。设置方法详见示例：<a href="multimodal-sdk-linux-01023efc79c79f6c.md#84db981acd6za">自定义提示词变量和传值</a>。</p></td></tr><tr><td><p>user_query_params</p></td><td></td><td><p>JSONObject</p></td><td><p>否</p></td><td><p>用于设置并传入用户自定义的结构化后的对话变量，是给到大模型的额外信息。搭配提示词设置，增加大模型的环境感知能力。设置方法详见示例：<a href="multimodal-sdk-linux-01023efc79c79f6c.md#18ce21efcck1m">自定义对话变量和传值</a>。</p></td></tr><tr><td><p>nls_rule</p></td><td></td><td></td><td><p>JSONObject</p></td><td><p>否</p></td><td><p>万能协议参数规则制定，可直接修改Websocket协议中发送的指令。</p><p>例如：</p><a id="code-block-7"></a><pre class="language-json"><code>{
  &quot;nls_rule&quot;: {
    &quot;header&quot;: [
      &quot;Start_custom1&quot;
    ],
    &quot;payload&quot;:[
      &quot;Start_task_group&quot;,
      &quot;Start_task&quot;
    ]
  }
}
</code></pre><p>将修改Start发送的指令中的header.custom1,和payload.task_group,payload.task。</p><p>具体修改为何值，见nls_params。</p></td></tr><tr><td><p>nls_params</p></td><td></td><td></td><td><p>JSONObject</p></td><td><p>否</p></td><td><p>万能协议参数设置，可直接修改Websocket协议中发送的指令。</p><p>例如：</p><a id="code-block-8"></a><pre class="language-json"><code>{
	&quot;nls_params&quot;: {
		&quot;Start_custom1&quot;: {
			&quot;test&quot;: 1
		},
		&quot;Start_task_group&quot;: &quot;aigc&quot;,
		&quot;Start_task&quot;: &quot;multimodal-generation&quot;,
		&quot;Start_function&quot;: &quot;generation&quot;,
		&quot;Start_model&quot;: &quot;multimodal-dialog&quot;
	}
}
</code></pre><p>将修改Start发送的指令中的：</p><p>header.custom1的值改为{&quot;test&quot;:1},</p><p>payload.task_group的值改为&quot;aigc&quot;,</p><p>payload.task的值改为&quot;aigc&quot;,</p><p>payload.function的值改为&quot;generation&quot;,</p><p>payload.model的值改为&quot;multimodal-dialog&quot;。</p></td></tr></tbody></table>

<a id="disconnect"></a>

<a id="66c4bbe617n1q"></a>

### Disconnect

组装一个stop请求，用于发送指令告诉服务端中止链接。返回成功并不代表与VoiceChat Server断链成功，仅代表发起stop请求构建成功，是否断链成功以返回的Response为准。

<a id="code-block-9"></a>

```cpp
/**
 * @brief 断开链接
 * @return ConvRetCode : 状态码
 */
ConvRetCode Disconnect();
```

<a id="interrupt"></a>

<a id="e39ad7ff645vc"></a>

### Interrupt

打断交互，使AI进入听状态。

<a id="code-block-10"></a>

```cpp
/**
 * @brief 按键(Tap)打断。正在播放时，调用此接口请求打断播放。
 * @return ConvRetCode : 状态码
 */
ConvRetCode Interrupt();
```

<a id="sendaudiodata"></a>

<a id="001de084be2m2"></a>

### SendAudioData

推送实时采集的音频数据。

<a id="code-block-11"></a>

```cpp
/**
 * @brief 推送音频数据
 * @param data : 音频数据，PCM格式
 * @param data_size : 音频数据字节数
 * @param type : 音频数据编码设置，暂未启用，设置无效。
 * @param timestamp : 此数据包的时间戳(ms)。
 * @return ConvRetCode : 状态码
 */
ConvRetCode SendAudioData(const uint8_t* data, size_t data_size,
                          EncoderType type = kEncoderNone,
                          uint64_t timestamp = 0);
```

<a id="sendrefdata"></a>

<a id="c68d4f91b8v4t"></a>

### SendRefData

推送参考音频数据，在音频数据送给播放器时推送。

<a id="code-block-12"></a>

```cpp
/**
 * @brief 推送参考音频数据，在音频数据送给播放器时推送
 * @param data : 音频数据，PCM格式
 * @param data_size : 音频数据字节数
 * @param timestamp : 此数据包的时间戳(ms)。
 * @return ConvRetCode : 状态码
 */
ConvRetCode SendRefData(const uint8_t* data, size_t data_size,
                          uint64_t timestamp = 0);
```

<a id="sendresponsedata"></a>

<a id="7b26edb48f6h4"></a>

### SendResponseData

Listening/Idle状态下，通知服务端与用户主动交互，可以直接把上传的文本转换为语音下发，也可以上传文本调用大模型，返回的结果再转换为语音下发。

<a id="code-block-13"></a>

```cpp
/**
 * @brief
 * 通知服务端与用户主动交互，可以直接把上传的文本转换为语音下发，也可以上传文本调用大模型，返回的结果再转换为语音下发
 * @param params ：json string形式的初始化参数
 * @return ConvRetCode : 状态码
 */
ConvRetCode SendResponseData(const char* params);
```

<a id="parameters参数设置"></a>

<a id="b91c492f07sgt"></a>

#### parameters参数设置

<table><tbody><tr><td><p><strong>参数</strong></p></td><td><p><strong>类型</strong></p></td><td><p><strong>必须</strong></p></td><td><p><strong>说明</strong></p></td></tr><tr><td><p>type</p></td><td><p>String</p></td><td><p>是</p></td><td><p>服务应该采取的交互类型：</p><p>transcript 表示直接把文本转语音。</p><p>prompt 表示把文本送大模型回答。</p></td></tr><tr><td><p>text</p></td><td><p>String</p></td><td><p>是</p></td><td><p>要处理的文本，可以是&quot;&quot;空字符串，非null即可。</p></td></tr><tr><td><p>parameters</p></td><td><p>JSONObject</p></td><td><p>否</p></td><td></td></tr><tr><td><ul><li><p>parameters.images</p></li></ul></td><td><p>JSONArray</p></td><td><p>否</p></td><td><p>需要分析的图片信息。</p></td></tr><tr><td><ul><li><p>parameters.biz_params</p></li></ul></td><td><p>JSONArray</p></td><td><p>否</p></td><td><p>与Start消息中biz_params相同，传递对话系统自定义参数。RequestToRespond的biz_params参数只在本次请求中生效。</p></td></tr><tr><td><p>任意</p></td><td><p>Any</p></td><td><p>否</p></td><td><p>将会透传给协议的payload中。</p></td></tr></tbody></table>

<a id="parameters示例"></a>

<a id="434107d3c8kzf"></a>

#### parameters示例

<a id="d19eae998be5j"></a>

##### 切换到视频模式

<a id="code-block-14"></a>

```json
{
	"type": "prompt",
	"parameters": {
		"biz_params": {
			"videos": [{
				"action": "connect",
				"type": "voicechat_video_channel"
			}]
		}
	}
}
```

<a id="20eebe75e9gj4"></a>

##### 退出视频模式

<a id="code-block-15"></a>

```json
{
	"type": "prompt",
	"parameters": {
		"biz_params": {
			"videos": [{
				"action": "exit",
				"type": "voicechat_video_channel"
			}]
		}
	}
}
```

<a id="2cfba7a5ca4yh"></a>

##### 发送图片进行问答

<a id="code-block-16"></a>

```json
# 发送图片base64数据(支持小于180KB图片)
{
	"type": "prompt",
	"parameters": {
		"images": [{
			"type": "base64",
			"value": "base64String"
		}]
	}
}

# 发送图片链接
{
	"type": "prompt",
	"parameters": {
		"images": [{
			"type": "url",
			"value": "https://xxxxxxx"
		}]
	}
}
```

<a id="updatemessage"></a>

<a id="d9c9926360vxo"></a>

### UpdateMessage

更新参数，如p2t参数，或者发送参数，如UpdateInfo。

<a id="code-block-17"></a>

```java
/**
 * @brief 发送如P2T相关的参数
 * @param params : 参数
 * @return ConvRetCode : 状态码
 */
ConvRetCode UpdateMessage(const char* params);
```

<a id="更新自定义唤醒词-仅kws-duplex有效"></a>

<a id="e71f6ccb07qty"></a>

#### 更新自定义唤醒词（仅kws\_duplex有效）

<a id="code-block-18"></a>

```json
{
	"type": "update_local_modules",
	"work": "update_keywords_list",
	"wuw": {
		"word_list": [{
			"name": "小云",
			"type": "main"
		}]
	}
}
```

<a id="更新其他参数"></a>

<a id="2a07a8d09f85n"></a>

#### 更新其他参数

<a id="code-block-19"></a>

```json
{"type":"update_nls_parameters", "avatar":{}}
{"type":"update_nls_parameters", "client_info":{}}
{"type":"update_nls_parameters", "agent_chat":{}}

//【SDK V1.2.4 新增】
{"type":"update_nls_parameters", "extra_info":{}, "context":{}}
```

<a id="更新参数万能方法"></a>

<a id="1e609001b7esw"></a>

#### 更新参数万能方法

用户自定义服务端交互参数，`"type": "update_custom_nls_parameters"`表示使用用户自定义参数功能。

`nls_rule`中规定参数在协议中添加的位置，如`"payload": ["Start_custom2", "SendSpeech_custom3"]`表示在向服务端发送`"Start"`协议时，`payload`中添加参数`"custom2":{"test":2}； "header": ["Start_custom1"]`表示在向服务端发送`"Start"`协议时，`header`中添加参数`"custom1":{"test":1}`。

<a id="code-block-20"></a>

```json
{
	"type": "update_custom_nls_parameters",
	"nls_rule": {
		"header": ["Start_custom1"],
		"payload": ["Start_custom2", "SendHumanSpeech_custom3"],
		"context": ["Stop_custom4"]
	},
	"nls_params": {
		"Start_custom1": {
			"test": 1
		},
		"Start_custom2": {
			"test": 2
		},
       "SendHumanSpeech_custom3": {
			"test": 3
		},
		"Stop_custom4": {
			"test": 4
		}
	}
}
```

<a id="发送参数-updateinfo"></a>

<a id="c85d82de4a2l7"></a>

#### 发送参数（UpdateInfo）

客户端更新事件，例如发送图片数据。

<a id="3b3385b52fnz2"></a>

##### 百炼协议参数

<table><tbody><tr><td><p><strong>参数</strong></p></td><td><p><strong>类型</strong></p></td><td><p><strong>必须</strong></p></td><td><p><strong>说明</strong></p></td></tr><tr><td><p>type</p></td><td><p>String</p></td><td><p>是</p></td><td><p>update_info。</p></td></tr><tr><td><p>parameters</p></td><td><p>JSONObject</p></td><td><p>是</p></td><td></td></tr><tr><td><ul><li><p>parameters.images</p></li></ul></td><td><p>JSONArray</p></td><td><p>否</p></td><td><p>图片数据。</p></td></tr><tr><td><ul><li><p>parameters.client_info</p></li></ul></td><td><p>JSONObject</p></td><td><p>否</p></td><td></td></tr><tr><td><ul><li><p>parameters.client_info.status</p></li></ul></td><td><p>JSONObject</p></td><td><p>否</p></td><td><p>客户端当前状态。</p></td></tr><tr><td><ul><li><p>parameters.biz_params</p></li></ul></td><td><p>JSONObject</p></td><td><p>否</p></td><td><p>与Start消息中biz_params相同，传递对话系统自定义参数。</p></td></tr></tbody></table>

<a id="b89464b81dr77"></a>

##### 百炼协议示例

<a id="code-block-21"></a>

```json
{
    "type": "update_info",
	"parameters": {
		"biz_params": {},
		"client_info": {
			"status": {
				"bluetooth_announcement": {
					"status": "stopped"
				}
			}
		},
		"images": [{
			"type": "base64",
			"value": "base64String"
		}]
	}
}
```

<a id="发送万能参数"></a>

<a id="54ac0e302ckza"></a>

#### 发送万能参数

<a id="code-block-22"></a>

```json
{
	"type": "update_custom_message",
	"header": {
		"TEST1": "XXX"
	},
	"payload": {
		"TEST2": "YYY"
	}
}
返回的对应消息
{
	"header": {
		"TEST1": "XXX",
		"dialog_id": "2b9bea3d2b2749a0808bae06a9da493c",
		"namespace": "VoiceChat",
		"request_id": "c48cfe7bbadd485db2e387136ce6608c",
		"task_id": "fffffff707fe4c288869931b0eeeeeee"
	},
	"payload": {
		"TEST2": "YYY"
	}
}
```

<a id="setaction"></a>

<a id="e0552b0c27lvw"></a>

### SetAction

需要有一个音频（播放）开始/结束事件告知到SDK。

<a id="code-block-23"></a>

```cpp
  /**
   * @brief 触发SDK动作，比如音频（播放）开始/结束事件告知到SDK
   * @param action : 触发的动作类型
   * @param data : 此次SDK动作附带的数据, 比如音频数据比如json字符串
   * @param data_size : 此次SDK动作附带的数据的字节数
   * @return ConvRetCode : 状态码
   */
  ConvRetCode SetAction(ConvAction action, const uint8_t* data = NULL,
                        size_t data_size = 0);
```

<a id="convaction"></a>

<a id="c77214898d0qx"></a>

#### ConvAction

<table><tbody><tr><td><strong>枚举名</strong></td><td><strong>说明</strong></td></tr><tr><td><p>kMicStarted</p></td><td><p>MIC开始工作。</p></td></tr><tr><td><p>kMicStopped</p></td><td><p>MIC停止录音。</p></td></tr><tr><td><p>kPlayerStarted</p></td><td><p>开始播放。</p></td></tr><tr><td><p>kPlayerStopped</p></td><td><p>播放完毕。注意：需确保播放器中缓存数据全部播放完毕后给出，否则会导致自打断或播放数据进入 ASR。</p></td></tr><tr><td><p>kEnableVoiceInterruption</p></td><td><p>开启语音打断功能。</p></td></tr><tr><td><p>kDisableVoiceInterruption</p></td><td><p>关闭语音打断功能。</p></td></tr><tr><td><p>kVoiceMute</p></td><td><p>语音静音。若正在AI听阶段，则主动告知AI，用户已经说完话。</p></td></tr><tr><td><p>kVoiceUnmute</p></td><td><p>语音静音关闭。</p></td></tr><tr><td><p>kStartHumanSpeech</p></td><td><p>仅在push2talk模式有效, 表示用户开始说话。</p><p>注意：Connect()成功后请在收到DialogStateChanged为kDialogIdle后再调用。</p></td></tr><tr><td><p>kStopHumanSpeech</p></td><td><p>仅在push2talk模式有效, 表示用户说话完毕。</p></td></tr><tr><td><p>kCancelHumanSpeech</p></td><td><p>仅在push2talk模式有效, 表示用户说话取消。</p></td></tr><tr><td><p>kPullOutHeadphones</p></td><td><p>拔耳机时调用，用于优化耳机切换的回声消除效果。</p></td></tr><tr><td><p>kContinue</p></td><td><p>交互流程暂停时，继续下一步，比如唤醒后调用此接口继续下一步流程。</p></td></tr><tr><td><p>kVoiceDetectedBegin</p></td><td><p>外置VAD时使用，表示检测到人开始说话。</p></td></tr><tr><td><p>kVoiceDetectedEnd</p></td><td><p>外置VAD时使用，表示检测到人说话完毕。</p></td></tr><tr><td><p>kVoiceTimeout</p></td><td><p>外置KWS时使用，表示人长时间未说话。</p></td></tr><tr><td><p>kKeywordTrusted</p></td><td><p>外置KWS时使用，触发唤醒并确认确实唤醒。</p><a id="code-block-24"></a><pre class="language-json"><code>{
	&quot;keyword_str&quot;: &quot;小云&quot;,
	&quot;keyword_tag&quot;: &quot;other_keyword&quot;
}
</code></pre></td></tr></tbody></table>

<a id="getstate"></a>

<a id="b8730bdf9cl5p"></a>

### GetState

获得当前各种状态。

<a id="code-block-25"></a>

```cpp
/**
 * @brief 获得当前状态
 * @param type : 状态类型
 * @return ConvRetCode : 状态码
 */
int GetState(StateType type);
```

<a id="statetype"></a>

<a id="3ba26e7552mbn"></a>

#### StateType

|  |  |
| --- | --- |
| **枚举名** | **说明** |
| kTypeDialogState | 对话（AI）当前状态，枚举值为ConvConstants.DialogState。 |
| kTypeConnectionState | 链接状态。 |
| kTypeMicState | MIC当前状态，枚举值为ConvConstants.ConvAppAction。 |
| kTypePlayerState | PLAYER当前状态，枚举值为ConvConstants.ConvAppAction。 |

<a id="4eebbcdbd1pxa"></a>

##### DialogState

|  |  |
| --- | --- |
| **枚举名** | **说明** |
| kDialogIdle | 当前处于空闲未工作状态。 |
| kDialogListening | AI（服务端）处于听状态，接收用户输入数据（如MIC音频数据）。 |
| kDialogResponding | AI（服务端）处于反馈状态，送出AI的数据（如TTS音频数据）。 |
| kDialogThinking | AI（服务端）处于思考阶段。 |

<a id="getresponse"></a>

<a id="aa4fee5a2cm4x"></a>

### GetResponse

向SDK送入通过RTC获得的VoiceChat相关response。response将在VideoChat Native SDK内部进行解析，转成交互状态和相关事件给APP。

<a id="code-block-26"></a>

```cpp
/**
 * @brief
 * 向SDK送入通过RTC获得的VoiceChat相关response。response将在VideoChat Native
 * SDK内部进行解析，转成交互状态和相关事件给APP。
 * @param params ：json string形式的初始化参数
 * @return ConvRetCode : 状态码
 */
ConvRetCode GetResponse(const char* params);
```

另外，如AvatarStateChanged请求的组装，处理通过updateMessage()，用此getResponse()也可，传入的格式如下：

<a id="code-block-27"></a>

```json
{"type":"rtc","from_state":"2","seq_id":"1","to_state":"0"}
或
{"from_state":"2","seq_id":"1","to_state":"0"}
或
{"from_state":2,"seq_id":1,"to_state":0}
或
{"header":{"name":"AvatarStateChanged","namespace":"Conversation"},"payload":{"from_state":2,"seq_id":2,"to_state":0}}
或
{"header":{"name":"AvatarStateChanged","namespace":"Conversation"},"payload":{"from_state":"2","seq_id":"2","to_state":"0"}}
```

<a id="代码示例"></a>

<a id="7c117c29067pp"></a>

## 代码示例

<a id="语音对话初始化"></a>

<a id="ee9558a86bw66"></a>

### 语音对话初始化

这一步通过设置回调函数来接收交互过程中的所有事件，包括对话状态、对话结果等。

<a id="code-block-28"></a>

```cpp
void onMessage(ConvEvent* event, void* param) {
  ConvEvent::ConvEventType event_type = event->GetMsgType();
  int dialog_state = event->GetDialogStateChanged();

  if (event_type != ConvEvent::kSoundLevel &&
      event_type != ConvEvent::kBinary) {
    std::cout << "trigger onMessage -->>\n"
              << "  session id: " << event->GetSessionId() << "\n"
              << "  messge type: " << event->GetMsgTypeString() << "\n"
              << "  dialog state: " << dialog_state << "\n"
              << "  response: " << event->GetAllResponse() << std::endl;
  }

  switch (event_type) {
    case ConvEvent::kConversationFailed:
      // 对话发生错误
      break;
    case ConvEvent::kConversationStarted:
      // 对话建连成功
      break;
    case ConvEvent::kConversationCompleted:
      break;
    case ConvEvent::kSentenceBegin:
      break;
    case ConvEvent::kSentenceEnd:
      break;
    case ConvEvent::kDataOutputStarted:
      // 后续将接收语音合成数据, 这里可启动播放器。
      // 播放器启动后需要通知SDK
      break;
    case ConvEvent::kDataOutputCompleted:
      // 接收语音合成数据完成, 这里需要通知播放器已经送完数据。
      // 注意, 这里只是接收完语音合成数据, 而非播放完成, 缓存或播放器中还有大量数据待播放。
      // 完全播放完后必须通知SDK
      break;
    case ConvEvent::kBinary:
      break;
    case ConvEvent::kSoundLevel:
      break;
    case ConvEvent::kDialogStateChanged:
      // 可通过对话状态进行相关业务逻辑操作
      break;
    case ConvEvent::kInterruptAccepted:
      // 允许打断, 这里可以关闭正在播放的音频
      break;
    case ConvEvent::kInterruptDenied:
      break;
    case ConvEvent::kVoiceInterruptAccepted:
      // 允许打断, 这里可以关闭正在播放的音频
      break;
    case ConvEvent::kVoiceInterruptDenied:
      break;
    case ConvEvent::kHumanSpeakingDetail:
      break;
    case ConvEvent::kRespondingDetail:
      break;
  }
}

void onEtMessage(ConvLogLevel level, const char* log, void* user_data) {
  std::cout << " ==>> [" << level << "] " << log << std::endl;
}

ConversationCallbackMethod on_message_callback = onMessage;
EventTrackCallbackMethod on_et_callback = onEtMessage;
Conversation* conversation = Conversation::CreateConversation(on_message_callback,
                                                              on_et_callback, NULL);
```

<a id="语音对话发起建连"></a>

<a id="fc89888332gmr"></a>

### 语音对话发起建连

建连参数把包括账号信息以json的形式构建，具体参考接口文档。PushToTalk模式下，建连成功后对话状态处于Idle状态。

<a id="code-block-29"></a>

```cpp
std::string gen_init_params() {
  Json::FastWriter writer;
  Json::Value root;
  Json::Value agent_chat;
  root["mode"] = g_mode;
  root["chain_mode"] = "ws";
  root["ws_version"] = 3;

  root["debug_mode"] = "xxxxxxx";
  root["workspace"] = "xxxxxxx";
  root["save_log"] = true;
  root["save_wav"] = true;
  root["log_level"] = g_log_level;

  root["url"] = "";
  root["apikey"] = "";
  root["app_id"] = "";
  root["workspace_id"] = "";

  Json::Value upstream;
  upstream["type"] = "AudioOnly";
  upstream["audio_format"] = "opus";  // asr格式，支持pcm,opus
  root["upstream"] = upstream;

  Json::Value downstream;
  downstream["type"] = "Audio";
  downstream["voice"] = "longxiaoxia_v2";
  downstream["sample_rate"] = 24000;  // default tts sample_rate is 24000
  downstream["audio_format"] = "pcm";  // 下发的音频编码格式，支持opu,pcm
  downstream["intermediate_text"] = "transcript,dialog";
  downstream["debug"] = true;
  root["downstream"] = downstream;

  Json::Value client_info; /* 额外扩充的用户信息 */
  client_info["user_id"] = "bin23439207";
  root["client_info"] = client_info;

  Json::Value dialog_attributes;
  dialog_attributes["prompt"] = "你是个有用的助手。";
  root["dialog_attributes"] = dialog_attributes;

  Json::Value acoustic_echo_cancelling_attributes;
  acoustic_echo_cancelling_attributes["enable_external_aec_module"] = false;
  root["acoustic_echo_cancelling_attributes"] =
      acoustic_echo_cancelling_attributes;

  Json::Value voice_activity_detection_attributes;
  voice_activity_detection_attributes["enable_external_vad_module"] = false;
  root["voice_activity_detection_attributes"] =
      voice_activity_detection_attributes;

  Json::Value key_words_spotting_attributes;
  key_words_spotting_attributes["enable_external_kws_module"] = false;
  key_words_spotting_attributes["independent_kws_mode"] = false;
  root["key_words_spotting_attributes"] = key_words_spotting_attributes;

  std::string result = writer.write(root);
  std::cout << "init params: " << result.c_str() << std::endl;
  return result;
}

// 发起建连, 可通过返回值判断是否建连成功。
// 若建连失败可通过返回值和回调信息进行判断。
ConvRetCode ret = conversation->Connect(gen_init_params().c_str());
```

<a id="语音对话结束"></a>

<a id="91b62f81d5d8j"></a>

### 语音对话结束

<a id="code-block-30"></a>

```cpp
ConvRetCode ret = conversation->Disconnect();
```

<a id="语音对话释放"></a>

<a id="2e0990f6e87c8"></a>

### 语音对话释放

<a id="code-block-31"></a>

```cpp
conversation->DestroyConversation();
conversation = NULL;
```

<a id="打断当前语音对话"></a>

<a id="4e39479c66kwp"></a>

### 打断当前语音对话

对话正处于Responding状态可调用此接口打断，并进入Listening状态。

<a id="code-block-32"></a>

```cpp
ConvRetCode ret = conversation->Interrupt();
```

<a id="pushtotalk模式用户开始说话"></a>

<a id="b514f609dceji"></a>

### PushToTalk模式用户开始说话

对话状态处于Idle状态时调用此接口，对话状态进入Listening。若对话状态处于Responding和Thinking，则打断当前状态重新进入Listening。调用接口成功后，用户所说的话持续送给服务端进行交互，直到停止。

<a id="code-block-33"></a>

```cpp
ConvRetCode ret = conversation->SetAction(kStartHumanSpeech);
```

<a id="pushtotalk模式用户结束说话"></a>

<a id="d7f18b7584r5o"></a>

### PushToTalk模式用户结束说话

用户所说的话持续送给服务端进行交互，直到调用此接口，AI将根据用户所说的话进行对应的反馈。

<a id="code-block-34"></a>

```cpp
ConvRetCode ret = conversation->SetAction(kStopHumanSpeech);
```

<a id="文本合成tts"></a>

<a id="1470b2a4897uw"></a>

### 文本合成TTS

SDK支持通过文本直接请求服务端合成音频。

您需要在客户端处于Listening状态下发送SendResponseData()请求。

若当前状态非Listening，需要先调用Interrupt()接口打断当前播报。

<a id="code-block-35"></a>

```cpp
Json::Value root;
root["text"] = "幸福是一种技能，是你摒弃了外在多余欲望后的内心平和。";
root["type"] = "transcript";

Json::StreamWriterBuilder writer;
writer["indentation"] = "";

ConvRetCode ret = conversation->SendResponseData(Json::writeString(writer, root).c_str());
```

<a id="vqa交互发送图片实现多模交互"></a>

<a id="67b1692be7tyt"></a>

### VQA交互发送图片实现多模交互

VQA 是在对话过程中通过发送图片实现图片+语音的多模交互的功能。

核心过程是语音或者文本通过SendResponseData()接口发送多模交互指令。

<a id="code-block-36"></a>

```cpp
Json::Value root;
root["text"] = "看看图片里是什么？";
root["type"] = "prompt";

Json::Value parameters;
Json::Value biz_params;

biz_params["user_defined_params"] = Json::Value(Json::objectValue);
Json::Value videos(Json::arrayValue);
{
    Json::Value video1;
    video1["action"] = "connect";//进入视频模式
    video1["type"] = "voicechat_video_channel";
    videos.append(video1);

    Json::Value video2;
    video2["action"] = "exit";//退出视频模式
    video2["type"] = "voicechat_video_channel";
    videos.append(video2);
}
biz_params["videos"] = videos;
parameters["biz_params"] = biz_params;

Json::Value images(Json::arrayValue);
{
    Json::Value image;
    // 发送图片base64数据的示例
    // 这里base64encode可借用SDK的辅助接口也可自行实现
    ConversationUtils utils;
    image["type"] = "base64";
    image["value"] = utils.Base64EncodeFromFilePath(path/*图片路径*/);

    // 发送图片链接的示例
    image["type"] = "url";
    image["value"] = "https://xxxx";

    images.append(image);
}
parameters["images"] = images;

root["parameters"] = parameters;

Json::StreamWriterBuilder writer;
writer["indentation"] = "";
ConvRetCode ret = conversation->SendResponseData(Json::writeString(writer, root).c_str());
```

<a id="liveai交互发送图片实现多模交互"></a>

<a id="b5128286be2ve"></a>

### LiveAI交互发送图片实现多模交互

若使用此功能，需要Connect()入参中upstream.type设置为AudioAndVideo，即通过UpdateInfo接口持续发送图片数据来实现图片+语音的多模交互。图片大小只支持720p、480p。视频模式每500ms传一次。

<a id="code-block-37"></a>

```cpp
// 发送图片base64数据的示例
// 这里base64encode可借用SDK的辅助接口也可自行实现
ConversationUtils utils;
std::string base64_content = utils.Base64EncodeFromFilePath(path/*图片路径*/);
if (!base64_content.empty()) {
  Json::Value root;
  root["type"] = "update_info";
  Json::Value parameters;
  parameters["biz_params"] = Json::objectValue;

  Json::Value client_info;
  Json::Value status;
  Json::Value bluetooth_announcement;
  bluetooth_announcement["status"] = "stopped";
  status["bluetooth_announcement"] = bluetooth_announcement;
  client_info["status"] = status;
  parameters["client_info"] = client_info;

  Json::Value image;
  image["type"] = "base64";
  image["value"] = base64_content;
  image["width"] = 480;
  image["height"] = 720;
  Json::Value images(Json::arrayValue);
  images.append(image);
  parameters["images"] = images;
  root["parameters"] = parameters;

  Json::StreamWriterBuilder writer;
  writer["indentation"] = "";
  conversation->UpdateMessage(Json::writeString(writer, root).c_str());
}
```

<a id="自定义提示词变量和传值"></a>

<a id="84db981acd6za"></a>

### 自定义提示词变量和传值

-   在管控台项目【提示词】配置自定义变量。

定义了一个`user_name`字段代表用户昵称。并将变量`user_name`以占位符形式${user\_name} 插入到Prompt 中。

在控制台**提示词**编辑区顶部可通过**自定义变量**入口添加变量字段，并在Prompt正文中以`${变量名}`占位符形式引用。

-   在代码中设置变量。

如下示例，设置`"user_name" = "大米"`。

<a id="code-block-38"></a>

```cpp
/* 以下示例在<语音对话发起建连>的示例上, 新增传入参数biz_params */
std::string gen_init_params() {
  /* 其他初始化参数不再赘述, 请看<语音对话发起建连> */

  Json::Value biz_params;
  Json::Value user_prompt_params;
  user_prompt_params["user_name"] = "大米";
  biz_params["user_prompt_params"] = user_prompt_params;
  root["biz_params"] = biz_params;

  std::string result = writer.write(root);
  std::cout << "init params: " << result.c_str() << std::endl;
  return result;
}

// 发起建连, 可通过返回值判断是否建连成功。
// 若建连失败可通过返回值和回调信息进行判断。
ConvRetCode ret = conversation->Connect(gen_init_params().c_str());
```

<a id="自定义对话变量和传值"></a>

<a id="18ce21efcck1m"></a>

### 自定义对话变量和传值

-   在管控台项目【对话变量】配置自定义变量。

添加一个`name`变量代表面前的人，添加一个`emotion`变量代表用户的心情。

在控制台**提示词**编辑区下方的**对话变量**面板中，单击右上角**\+ 添加**按钮，依次录入变量名（如`name`、`emotion`）和对应描述（如`面前的人`、`用户的心情`）。

-   在代码中设置变量。

如下示例，设置`"name" = "张三"`和`"emotion" = "难过"`。

<a id="code-block-39"></a>

```cpp
/* 以下示例在<语音对话发起建连>的示例上, 新增传入参数biz_params */
std::string gen_init_params() {
  /* 其他初始化参数不再赘述, 请看<语音对话发起建连> */

  Json::Value biz_params;
  Json::Value user_query_params;
  user_query_params["name"] = "张三";
  user_query_params["emotion"] = "难过";
  biz_params["user_query_params"] = user_query_params;
  root["biz_params"] = biz_params;

  std::string result = writer.write(root);
  std::cout << "init params: " << result.c_str() << std::endl;
  return result;
}

// 发起建连, 可通过返回值判断是否建连成功。
// 若建连失败可通过返回值和回调信息进行判断。
ConvRetCode ret = conversation->Connect(gen_init_params().c_str());
```

<a id="sdk错误码"></a>

<a id="fd86875c173zj"></a>

## SDK错误码

|  |  |  |
| --- | --- | --- |
| **枚举值** | **枚举** | **说明** |
| 0 | kSuccess |  |
| 10 | kDefaultError |  |
| 11 | kMemAllocError | 内存分配失败 |
| 50 | kInitFailed | 初始化为不支持的模式 |
| 51 | kNotConnected | 链接失败，如联网超时等 |
| 52 | kEngineNull | 交互引擎未创建，不可使用 |
| 53 | kIllegalParam | 设置参数非法 |
| 54 | kIllegalInitParam | 初始化参数非法 |
| 55 | kInvalidState | 当前交互状态无法调用此接口 |
| 56 | kHasInvoked | 已经调用了此接口 |
| 57 | kNotCreateConversation | 还未创建会话即未调用createConversation就开始操作 |
| 58 | kSkipSendData | 当前交互状态忽略此次音频 |
| 59 | kSendDataFailed | 发送音频失败 |
| 60 | kInvalidAudioData | 无效音频 |
| 61 | kStopFailed | stop()失败，如超时 |
| 62 | kCancelFailed | cancel()失败，如超时 |
| 63 | kInvokeTimeout | 接口调用超时 |
| 64 | kRequestDenied | 打断请求拒绝 |
| 65 | kRequestAccepted | 允许打断请求 |
| 66 | kSkipDestroyConversation | 当前SDK未创建，跳过释放操作 |
| 67 | kInvokeInvalidAction | SetAction()调用错误事件 |
| 100 | kCeiInitFailed | 内部引擎初始化失败，常发生于connect()时 |
| 101 | kCeiSetParamFailed | 内部引擎配置参数失败 |
| 111 | kVadSdkFileNotFound | 内部引擎因为找不到资源文件而初始化失败，请检查资源文件是否完备，且是最新版本 |
| 112 | kVadSdkInvalidParam | 内部vad引擎的初始化参数非法 |
| 113 | kVadSdkInvalidState | 内部vad引擎运行处于异常状态，比如vad已经释放 |
| 114 | kVadSdkProcessFailed | 内部vad引擎在异常状态送入数据 |
| 115 | kVadSdkCreateFailed | 内部vad引擎初始化失败，一般是由于资源文件缺失或者不兼容的旧版本 |
| 200 | kEmptyConvEvent | 非法ConvEvent |
| 201 | kInvalidConvEventMsgType | 非法的ConvEvent事件类型 |
| 301 | kServerNotAccess | 链接服务端失败，比如服务端不可链接，dns不可解析等 |
| 310 | kNoSupportMode | 不支持的服务端交互协议 |
| 311 | kJsonFormatError | 接收到服务端返回的消息不符合JSON格式 |
| 312 | kSslError | SSL失败，比如握手失败 |
| 313 | kSslConnectFailed | SSL链接失败 |
| 350 | kNlsIsNullptr |  |
| 351 | kNlsInvokeTimeout | 向服务端发送请求操作超时 |
| 352 | kNlsStartFailed | 向服务端发送建立会话请求失败，常为网络问题 |
| 353 | kNlsStopFailed | 向服务端发送停止会话请求失败，常为网络问题 |
| 354 | kNlsCancelFailed | 向服务端发送停止会话请求失败，常为网络问题 |
| 355 | kNlsStartInboundFailed | 向服务端发送启动对话任务请求失败，常为网络问题 |
| 358 | kNlsCancelBoundFailed | 向服务端发送停止对话任务请求失败，常为网络问题 |
| 359 | kNlsSetParamsFailed | 设置请求参数错误，比如设置token无效 |
| 360 | kNlsSendAudioFailed | 向服务端发送音频数据失败，常为网络问题 |
| 361 | kNlsControlFailed | UpdateInfo等向服务端发送指令失败 |
| 400 | kEncoderExistent |  |
| 401 | kDecoderExistent |  |
| 402 | kEncoderInexistent | 编码器不存在 |
| 403 | kDecoderInexistent |  |
| 404 | kOpusEncoderCreateFailed | Opus编码器创建失败 |
| 405 | kOpusDecoderCreateFailed |  |
| 406 | kOggOpusEncoderCreateFailed | OggOpus编码器创建失败 |
| 407 | kInvalidEncoderType | encoder类型无效 |
| 500 | kInvalidAkId | 阿里云账号ak id无效 |
| 501 | kInvalidAkSecret | 阿里云账号ak secret无效 |
| 502 | kInvalidAppKey | 项目appKey无效 |
| 503 | kInvalidDomain | domain无效 |
| 504 | kInvalidAction | action无效 |
| 505 | kInvalidServerVersion | ServerVersion无效 |
| 506 | kInvalidServerResource | ServerResource无效 |
| 507 | kInvalidRegionId | RegionId无效 |
| 508 | kClientRequestFaild | 账号客户端请求失败 |
| 509 | kInvalidUrlCmd | 无效的url |
| 510 | kInvalidTokenCmd | 无效的token指令 |
| 511 | kTokenConnectFailed | 链接token服务器失败 |
| 512 | kTokenResponseError | token返回失败 |

* * *

<a id="时序图说明"></a>

<a id="e70a2c95fdiq5"></a>

## 时序图说明

<a id="duplex"></a>

<a id="3752a25c3er62"></a>

### duplex

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6431377471/p957958.png)

<a id="push2talk"></a>

<a id="e12803355dt6i"></a>

### push2talk

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6431377471/p957956.png)

<a id="tap2talk"></a>

<a id="d97668f237jjg"></a>

### tap2talk

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6431377471/p957957.png)
