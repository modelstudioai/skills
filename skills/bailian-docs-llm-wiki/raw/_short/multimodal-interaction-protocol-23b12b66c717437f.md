# WebSocket 协议

本文介绍基于 WebSocket 协议的实时多模态交互 API。WebSocket协议延迟低、资源占用少，是首选接入方案。

WebSocket是一种支持全双工通信的网络协议。客户端和服务器通过一次握手建立持久连接，双方可以互相主动推送数据，因此在实时性和效率方面具有显著优势。

对于常用编程语言，有许多现成的WebSocket库和示例可供参考，例如：

-   Go：`gorilla/websocket`
-   PHP：`Ratchet`
-   Node.js：`ws`

建议您先了解WebSocket的基本原理和技术细节，再参照本文进行开发。

> **说明**
>
> 对于RTOS或某些旧版Linux系统，建立安全Websocket 通信所依赖的 TLS 隧道，需要做如下配置：
>
> -   TLS 版本要求 TLS1.2 或以上
> -   开启 SNI（SERVER NAME INDICATION）
> -   配置 CA 证书（[GlobalSign Root CA - R46](https://secure.globalsign.com/cacert/rootr46.crt)）（也可至GlobalSign官网下载）

<a id="前提条件"></a>

<a id="39976381bblbp"></a>

## 前提条件

已开通服务并[获取与配置 API Key](../model-api-reference/preparations/get-api-key.md)。请[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)，而非硬编码在代码中，防范因代码泄露导致的安全风险。

> **说明**
>
> 对于客户端调用的场景，在客户端处理API Key有安全风险，建议从服务端用API Key获取临时鉴权Token，再把Token下发给客户端使用。具体方法请参考：[生成临时API Key](../model-api-reference/more-about-models/generate-temporary-api-key.md)。

<a id="调用时序图"></a>

<a id="6d25d6f8ddbtd"></a>

## 调用时序图

**\[关键流程\]** 服务端返回`Started`消息表示会话创建成功，但客户端**禁止**立即发送音频。客户端必须等待并接收到`DialogStateChanged`事件且`state`为`Listening`后，方可开始发送音频流。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8963248471/p958632.png)

<a id="服务地址"></a>

<a id="aded0e18ae7we"></a>

## 服务地址

<a id="code-block"></a>

```text
wss://dashscope.aliyuncs.com/api-ws/v1/inference
```

<a id="鉴权"></a>

<a id="f33e29403a9i8"></a>

## 鉴权

需要在发起初始的WebSocket握手（HTTP Upgrade）请求时，把API Key放在HTTP Header里（需要将your\_api\_key替换为真实的API Key）：

<a id="code-block-2"></a>

```text
"Authorization": "Bearer your_api_key"
```

<a id="语音交互"></a>

<a id="34b63cd8b0qvr"></a>

## 语音交互

多模态交互应用开启了**语音交互**后，支持语音识别和语音合成。

语音识别支持的模型包括：[Paraformer实时语音识别](paraformer-real-time-speech-recognition-api-refe-fcf57d84158b854c.md)（Paraformer），[FUN-ASR实时语音识别](fun-asr-real-time-speech-recognition-api-referen-c1b5c2ef9baf2fd3.md)（FunASR），[Qwen-Audio-3.0-ASR-Flash-Streaming](qwen-audio-asr-streaming-websocket-sdk-java-923284a83b541f4a.md)，[千问3-ASR-Flash-Realtime](../model-user-guide/model-experience/speech-and-audio/speech-recognition/real-time-speech-recognition-user-guide.md)（qwen3-asr-flash-realtime），多模态交互轻量版语音识别（AppSpecificASR-Realtime）。

语音合成支持的模型包括：[语音合成CosyVoice-v2大模型](../model-api-reference/realtime-api-directory/realtime-tts-model-apis/cosyvoice-large-model-for-speech-synthesis.md)（cosyvoice-v2），[语音合成CosyVoice-v3-Flash大模型](https://help.aliyun.com/zh/model-studio/text-to-speech)（cosyvoice-v3-flash），[语音合成CosyVoice-v3-plus大模型](https://help.aliyun.com/zh/model-studio/text-to-speech)（cosyvoice-v3-plus），[语音合成CosyVoice-v3.5-Flash大模型](https://help.aliyun.com/zh/model-studio/text-to-speech)（cosyvoice-v3.5-flash），[语音合成CosyVoice-v3.5-Plus大模型](https://help.aliyun.com/zh/model-studio/text-to-speech)（cosyvoice-v3.5-plus），[Qwen-Audio-3.0-TTS-Plus](../model-user-guide/model-experience/speech-and-audio/speech-synthesis/realtime-tts-user-guide.md)（qwen-audio-3.0-tts-plus）、[Qwen-Audio-3.0-TTS-Flash](../model-user-guide/model-experience/speech-and-audio/speech-synthesis/realtime-tts-user-guide.md)（qwen-audio-3.0-tts-flash），[千问3-TTS-Flash-Realtime](../model-user-guide/model-experience/speech-and-audio/speech-synthesis/realtime-tts-user-guide.md)（qwen3-tts），[千问3-TTS-Instruct-Flash-Realtime](../model-user-guide/model-experience/speech-and-audio/speech-synthesis/realtime-tts-user-guide.md)（qwen3-tts-instruct），[千问3-声音设计](https://help.aliyun.com/zh/model-studio/qwen-tts-voice-design)（qwen3-tts-vd），[千问3-声音复刻](https://help.aliyun.com/zh/model-studio/qwen-tts-voice-cloning)（qwen3-tts-vc），[Sambert语音合成](sambert-speech-synthesis-32c5c56b36543707.md)（sambert），多模态交互轻量版语音合成（AppSpecificTTS）。

语音合成支持的音色，可以在控制台上选择了模型后，点击右侧语音交互体验区域的右上角查看音色列表。

官方音色也可以参考官方文档：[支持的音色](../model-user-guide/model-experience/speech-and-audio/speech-synthesis/realtime-tts-user-guide.md#bac280ddf5a1u)，sambert支持的音色参考[Sambert音色列表](sambert-java-sdk-79ed7a3fed2f3f90.md)（去掉开头的"sambert-"和末尾的"-v1"后就是voice的取值）。

使用复刻音色时，确认复刻音色状态为"OK"后才能使用。查询方法参考[查询特定音色](https://help.aliyun.com/zh/model-studio/cosyvoice-clone-design-api)。

<a id="消息类型"></a>

<a id="e3a7c0fbdfzuh"></a>

## 消息类型

<a id="二进制消息-binary-message"></a>

<a id="ef6ec1325br4c"></a>

### 二进制消息（Binary Message）

当前二进制消息仅包含音频数据。

<a id="上传音频"></a>

<a id="78981c8e11kef"></a>

#### 上传音频

上传音频时，将原始音频直接转为二进制流即可，无需额外处理。

上传的语音识别音频需满足：16bit（采样位深）、单声道、有符号、little-endian PCM编码，采样率参考[Start](multimodal-interaction-protocol-23b12b66c717437f.md#5b2363d40585y)消息的参数parameters.upstream.sample\_rate的取值说明。

如果希望减少网络流量和带宽占用，用户可以把PCM音频编码为Opus格式，同时设置上传音频格式为raw-opus。

上传音频时，根据[Start](multimodal-interaction-protocol-23b12b66c717437f.md#5b2363d40585y)消息中`upstream.mode`设置不同，采取的措施也不同：

-   mode为 `tap2talk` 或 `duplex`：客户端需持续上传音频，服务端自动检测语音活动。建议每100ms上传一次数据，间隔太长或太短会对延时和处理效率造成负面影响。
    
    -   音频上传速率计算公式：`数据每次上传的字节数 = 采样率 * 采样位深/8 * 时间间隔（ms）/ 1000`
    -   以16kHz采样率、16bit位深、100ms间隔为例，每次应上传 `16000 * (16/8) * 100 / 1000 = 3200` 字节的PCM数据。
-   mode为 `push2talk`：客户端无需持续上传音频，但需通过[SendSpeech](multimodal-interaction-protocol-23b12b66c717437f.md#cec23c1556u8x)和[StopSpeech](multimodal-interaction-protocol-23b12b66c717437f.md#d11933e7b5jz0)通知服务端音频识别的开始和结束。发送[SendSpeech](multimodal-interaction-protocol-23b12b66c717437f.md#cec23c1556u8x)后需立即上传音频，否则会增加处理时间。
    

<a id="下发音频"></a>

<a id="f7aa2ba72cj1n"></a>

#### 下发音频

服务端将大模型回复发送至TTS生成语音然后下发给客户端：

-   下发音频为16bit单声道，采样率和编码由[Start](multimodal-interaction-protocol-23b12b66c717437f.md#5b2363d40585y)消息参数定义。
-   下发速度取决于TTS服务性能，通常快于播放速度。
-   音频下发前发送[RespondingStarted](multimodal-interaction-protocol-23b12b66c717437f.md#0693e9d4a5f91)事件；结束后发送[RespondingEnded](multimodal-interaction-protocol-23b12b66c717437f.md#402cbee340r1m)事件。
-   客户端需在播放完成后上报[LocalRespondingEnded](multimodal-interaction-protocol-23b12b66c717437f.md#f4b1a6bf22ymq)，通知服务端播放结束。

<a id="文本消息-text-message"></a>

<a id="48b2452228o2z"></a>

### 文本消息（Text Message）

文本消息是JSON格式字符串，按传递方向分为两类：

-   **输入消息（Input Message）**：客户端发送给服务端的指令（directive），表示客户端希望服务端执行特定动作。
-   **输出消息（Output Message）**：服务端发送给客户端的事件（event），表示服务端动作执行结果或进展。

文本消息标记交互流程的关键节点，控制流程并传输关键信息。通过[时序图](multimodal-interaction-protocol-23b12b66c717437f.md#6d25d6f8ddbtd)可了解不同消息的交互时序。

文本消息包含两部分：`header`和`payload`。

-   `payload`：内容随[消息类型](multimodal-interaction-protocol-23b12b66c717437f.md#408ddb268eyt7)变化。
    
-   `header`：内容固定，包含以下参数：
    
    <table><thead><tr><th><p><strong>参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>是否必选</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td><p>task_id</p></td><td><p>string</p></td><td><p>是</p></td><td><p>本次连接唯一标识，用于在工程链路上跟踪任务执行。由客户端生成，格式建议为36位uuid字符串，格式示例：&quot;f894c16f-f20e-4c1d-837e-89e0fbc63a43&quot;</p></td></tr><tr><td><p>streaming</p></td><td><p>string</p></td><td><p>是</p></td><td><p>输入输出类型，对于多模态交互必须为 &quot;duplex&quot; ，表示流式输入，流式输出</p></td></tr><tr><td><p>action</p></td><td><p>string</p></td><td><p>是</p></td><td><p>模型输入消息类型：</p><ul><li><p>run-task: 任务的第一个输入消息</p></li><li><p>finish-task: 任务的最后一个输入消息</p></li><li><p>continue-task: 任务中其他输入消息</p></li></ul></td></tr></tbody></table>
    

<a id="连接保活策略"></a>

<a id="8e82725ed5vag"></a>

## 连接保活策略

百炼平台规定，如果在**任意连续的60秒内**服务端没有向客户端发送任何消息，则认为调用发生错误，WebSocket连接将被服务端主动断开并返回`ResponseTimeout`错误。

若客户端需在无交互时保持连接，应定期发送心跳消息（HeartBeat）。服务端会回应心跳，确保连接活跃，避免超时关闭。

移动端和C++ SDK已内置心跳保活逻辑，用户无需手动发送。

<a id="文本消息类型"></a>

<a id="408ddb268eyt7"></a>

## 文本消息类型

<a id="开始会话"></a>

<a id="92d1f462e5xrm"></a>

### 开始会话

<a id="start-input-message"></a>

<a id="5b2363d40585y"></a>

#### Start - Input Message

请求开始会话消息。服务收到Start消息后，向客户端发送**Started**消息。

<table><thead><tr><th><p><strong>一级参数</strong></p></th><th><p><strong>二级参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>是否必选</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td><p>task_group</p></td><td></td><td><p>string</p></td><td><p>是</p></td><td><p>任务组名称，固定为&quot;aigc&quot;，请直接复制使用</p></td></tr><tr><td><p>task</p></td><td></td><td><p>string</p></td><td><p>是</p></td><td><p>任务名称，固定为&quot;multimodal-generation&quot;，请直接复制使用</p></td></tr><tr><td><p>function</p></td><td></td><td><p>string</p></td><td><p>是</p></td><td><p>调用功能，固定为&quot;generation&quot;，请直接复制使用</p></td></tr><tr><td><p>model</p></td><td></td><td><p>string</p></td><td><p>是</p></td><td><p>阿里云百炼模型名称，固定为&quot;multimodal-dialog&quot;，请直接复制使用</p></td></tr><tr><td rowspan="4"><p>input</p></td><td><p>directive</p></td><td><p>string</p></td><td><p>是</p></td><td><p>指令名称：Start</p></td></tr><tr><td><p>workspace_id</p></td><td><p>string</p></td><td><p>是</p></td><td><p>客户在阿里云百炼业务空间ID（<a href="../application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md#732535cfc959h">Workspace ID</a>），可在<strong>多模态交互开发套件控制台</strong>，点击左下角业务空间名称，&quot;业务空间详情&quot;中查看，目前仅支持主账号默认业务空间。</p></td></tr><tr><td><p>app_id</p></td><td><p>string</p></td><td><p>是</p></td><td><p>客户创建的应用ID（<a href="../application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md#2612f896detsz">APP ID</a>），可在<strong>多模态交互开发套件</strong>控制台的&quot;我的应用&quot;页面查看。</p></td></tr><tr><td><p>dialog_id</p></td><td><p>string</p></td><td><p>否</p></td><td><p>对话ID，默认不填时是开启新会话，服务端会自动生成并在事件中下发，格式示例：&quot;12345678-1234-1234-1234-1234567890ab&quot;，共36个字符。当希望继续之前的对话时，把当时服务端下发的dialog_id在这里传入</p></td></tr><tr><td rowspan="4"><p>parameters</p></td><td><p>upstream</p></td><td><p>object</p></td><td><p>是</p></td><td><p>参数说明参考下方 <a href="multimodal-interaction-protocol-23b12b66c717437f.md">parameters.upstream的参数说明</a>表格</p></td></tr><tr><td><p>downstream</p></td><td><p>object</p></td><td><p>否</p></td><td><p>参数说明参考下方 <a href="multimodal-interaction-protocol-23b12b66c717437f.md">parameters.downstream的参数说明</a>表格</p></td></tr><tr><td><p>client_info</p></td><td><p>object</p></td><td><p>是</p></td><td><p>参数说明参考下方 <a href="multimodal-interaction-protocol-23b12b66c717437f.md">parameters.client_info的参数说明</a>表格</p></td></tr><tr><td><p>biz_params</p></td><td><p>object</p></td><td><p>否</p></td><td><p>参数说明参考下方 <a href="multimodal-interaction-protocol-23b12b66c717437f.md">parameters.biz_params的参数说明</a>表格</p></td></tr></tbody></table>

**parameters.upstream**的参数说明如下**：**

<table><thead><tr><th><p><strong>一级参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>是否必选</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td><p>type</p></td><td><p>string</p></td><td><p>是</p></td><td><p>上行类型：</p><p>AudioOnly 仅语音通话</p></td></tr><tr><td><p>mode</p></td><td><p>string</p></td><td><p>否</p></td><td><p>客户端使用的模式，默认<strong>tap2talk。</strong></p><p>可选项：</p><ul><li><p>push2talk: 客户端控制模式。</p></li><li><p>tap2talk: 点击模式。</p></li><li><p>duplex: 双工模式。</p></li></ul><p>三种模式的对比可以参考下方的<a href="multimodal-interaction-protocol-23b12b66c717437f.md#5e82453407pum">客户端使用的三种模式对比</a>表格。</p></td></tr><tr><td><p>audio_format</p></td><td><p>string</p></td><td><p>否</p></td><td><p>音频格式，支持pcm，raw-opus，默认为pcm</p></td></tr><tr><td><p>sample_rate</p></td><td><p>int</p></td><td><p>否</p></td><td><p>语音识别的采样率，支持范围：</p><ul><li><p>8000</p></li><li><p>16000</p></li><li><p>24000</p></li><li><p>48000</p></li></ul><p>默认为16000</p></td></tr><tr><td><p>vocabulary_id</p></td><td><p>string</p></td><td><p>否</p></td><td><p>热词id，设置该参数时会覆盖管控台热词配置。当管控台提供的热词不能满足客户需求时，可以考虑用Open API程序化管理热词，参见<a href="https://next.api.aliyun.com/document/MultimodalDialog/2025-09-03/Vocabulary">热词API文档</a>。</p></td></tr><tr><td><p>language</p></td><td><p>string</p></td><td><p>否</p></td><td><p>语音识别语种，默认和控制台选择的语言保持一致。设置多个语种时，使用英文逗号分隔，例如：<code>zh,en</code>。</p></td></tr></tbody></table>

**parameters.downstream**的参数说明如下：

<table><thead><tr><th><p><strong>一级参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>是否必选</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td><p>voice</p></td><td><p>string</p></td><td><p>否</p></td><td><p>合成语音的音色，支持范围取决于用户在管控台选择的语音合成模型</p></td></tr><tr><td><p>sample_rate</p></td><td><p>int</p></td><td><p>否</p></td><td><p>合成语音的采样率，支持范围：</p><ul><li><p>8000</p></li><li><p>16000</p></li><li><p>24000</p></li><li><p>48000</p></li></ul><p>默认为24000。</p><p>千问-TTS、千问3-TTS模型仅支持24000。</p></td></tr><tr><td><p>audio_format</p></td><td><p>string</p></td><td><p>否</p></td><td><p>音频格式，支持pcm，opus，mp3，raw-opus，默认为pcm。</p><p>千问-TTS模型仅支持pcm。</p><p>注意：opus 和 raw-opus的区别是opus格式的每一包数据都有额外ogg封装（<a href="https://www.rfc-editor.org/rfc/rfc7845.html">RFC 7845</a>）</p></td></tr><tr><td><p>frame_size</p></td><td><p>int</p></td><td><p>否</p></td><td><p>合成音频的帧大小，取值范围：</p><ul><li><p>10</p></li><li><p>20</p></li><li><p>40</p></li><li><p>60</p></li><li><p>100</p></li><li><p>120</p></li></ul><p>默认值为60，单位ms</p><p>只在合成音频格式为opus或raw-opus时生效</p></td></tr><tr><td><p>volume</p></td><td><p>int</p></td><td><p>否</p></td><td><p>合成音频的音量，取值范围0-100，默认50</p></td></tr><tr><td><p>speech_rate</p></td><td><p>int</p></td><td><p>否</p></td><td><p>合成音频的语速，取值范围50-200，表示默认语速的50%-200%，默认100</p></td></tr><tr><td><p>pitch_rate</p></td><td><p>int</p></td><td><p>否</p></td><td><p>合成音频的声调，取值范围50-200，默认100</p></td></tr><tr><td><p>bit_rate</p></td><td><p>int</p></td><td><p>否</p></td><td><p>合成音频的比特率，取值范围：6~510kbps，默认值为32，单位kbps，只在合成音频格式为mp3, opus或raw-opus时生效</p></td></tr><tr><td><p>intermediate_text</p></td><td><p>string</p></td><td><p>否</p></td><td><p>控制返回给用户哪些中间文本：</p><ul><li><p>transcript：返回用户语音识别结果</p></li><li><p>dialog：返回对话系统回答中间结果</p></li></ul><p>可以设置多种，以逗号分隔，默认为transcript</p></td></tr><tr><td><p>word_timestamp_enabled</p></td><td><p>boolean</p></td><td><p>否</p></td><td><p>是否下发tts合成音频对应的时间戳。如果设置为true，会在RespondingContent.extra_info下返回时间戳信息，用于客户端显示字幕等，默认为false。</p><p>必须在intermediate_text有指定dialog的情况下才会返回；</p><p>只有<a href="../model-user-guide/model-experience/speech-and-audio/speech-synthesis/tts-voice-list/cosyvoice-voice-list.md">CosyVoice音色列表</a>中表明支持时间戳的音色和复刻音色才会返回。</p></td></tr><tr><td><p>transmit_rate_limit</p></td><td><p>int</p></td><td><p>否</p></td><td><p>下发音频发送速率限制，单位：字节每秒</p></td></tr><tr><td><p>incremental_response</p></td><td><p>boolean</p></td><td><p>否</p></td><td><p>是否增量返回大模型结果，true为增量，false为全量。默认为false，全量下发</p></td></tr><tr><td><p>instruction</p></td><td><p>string</p></td><td><p>否</p></td><td><p>设置指令，用于控制方言、情感等合成效果。该功能适用的模型以及在不同模型的格式要求请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-synthesis/realtime-tts-user-guide.md#12884a10929p9">指令控制</a>。</p></td></tr><tr><td><p>language</p></td><td><p>string</p></td><td><p>否</p></td><td><p>语音合成语种，默认和控制台选择的语言保持一致。</p></td></tr></tbody></table>

**parameters.client\_info**的参数说明如下：

<table><thead><tr><th><p><strong>一级参数</strong></p></th><th><p><strong>二级参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>是否必选</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td><p>user_id</p></td><td></td><td><p>string</p></td><td><p>是</p></td><td><p>终端用户ID，客户根据自己业务规则生成，用来针对不同终端用户实现定制化功能。最大长度36个字符。</p></td></tr><tr><td><p>device</p></td><td><p>uuid</p></td><td><p>string</p></td><td><p>否</p></td><td><p>客户端全局唯一的ID，需要用户自己生成并传入SDK，最大长度40个字符。一个终端用户可以有多个设备，那么每一个设备的uuid都不同，但user_id相同。</p></td></tr><tr><td><p>network</p></td><td><p>ip</p></td><td><p>string</p></td><td><p>否</p></td><td><p>调用方公网IP</p></td></tr><tr><td rowspan="3"><p>location</p></td><td><p>latitude</p></td><td><p>string</p></td><td><p>否</p></td><td><p>调用方纬度信息，在需要客户端精确位置的业务场景提交</p></td></tr><tr><td><p>longitude</p></td><td><p>string</p></td><td><p>否</p></td><td><p>调用方经度信息，在需要客户端精确位置的业务场景提交</p></td></tr><tr><td><p>city_name</p></td><td><p>string</p></td><td><p>否</p></td><td><p>调用方所在城市，指明客户端粗略位置</p></td></tr></tbody></table>

**parameters.biz\_params**的参数说明如下：

| 一级参数 | 类型 | 是否必选 | 说明 |
| --- | --- | --- | --- |
| user\_defined\_params | json object | 否 | 设置需要透传给agent 和 mcp 服务的参数，各类agent传递的参数参考[调用官方Agent](official-agent-297b22931e69e622.md)文档说明， mcp 传递参数依照 mcp 服务本身所需的参数。可以在extra\_config子节点中设置对话扩展参数，目前支持：1. enable\_web\_search，表示是否开启联网搜索。这里的设置优先级更高，会覆盖管控台配置；2. agent\_timeout，表示agent连接超时的时间，传值范围是10秒到120秒。如果不传，则默认为10秒。 |
| user\_prompt\_params | json object | 否 | 用于设置用户自定义prompt变量，由用户自定义设置json中的key和value。管控台上配置自定义prompt变量的方法参考[应用配置-提示词](multimodal-app-configuration-8919f99b339e17da.md#cbbc5f73caixw) |
| user\_query\_params | json object | 否 | 用于设置用户自定义对话变量，由用户自定义设置json中的key和value。管控台上配置自定义对话变量的方法参考[应用配置-对话变量](multimodal-app-configuration-8919f99b339e17da.md#6abc9330e2yx9) |

<a id="5e82453407pum"></a>

##### 客户端使用的三种模式对比：

| 对比项 | push2talk | tap2talk | duplex |
| --- | --- | --- | --- |
| 类型 | 客户端控制模式 | 点击模式 | 双工模式 |
| 音频上传方式 | 按需 | 持续<br><br>Listening状态超过20秒不上传音频即报错 | 持续<br><br>任何状态超过20秒不上传音频都报错 |
| VAD检测方 | 客户端 | 服务端 | 服务端 |
| 打断方式 | [RequestToSpeak](multimodal-interaction-protocol-23b12b66c717437f.md#96541eff55v86)消息打断 | [RequestToSpeak](multimodal-interaction-protocol-23b12b66c717437f.md#96541eff55v86)消息打断 | 语音打断 |
| 使用场景 | 由用户控制开始/结束客户端语音发送和识别，适用于按键说话，松开停止说话的场景。 | 客户端需持续上传音频，服务端自动检测语音活动的场景。但不支持用户语音打断大模型输出，只能发送RequestToSpeak打断消息。 | 客户端需持续上传音频，服务端自动检测语音活动的场景。用户随时可以说话打断大模型输出。 |

示例如下：

<a id="code-block-3"></a>

```json
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
                "extra_config": {
                    "enable_web_search": false,
                    "agent_timeout": 10
                },
                "agent_id_xxxxx": {
                    "name": "value"
                },
                "mcp_server_id_xxxxx":{
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

<a id="started-output-message"></a>

<a id="06ba46fd89wqt"></a>

#### Started - Output Message

> **说明**
>
> SDK接收到**Started**之后，先不可以向服务发送音频，应等待**DialogStateChanged**消息，确认切换到Listening状态之后才发送音频。

| 一级参数 | 二级参数 | 类型 | 说明 |
| --- | --- | --- | --- |
| output | event | string | 事件名称：Started |
|  | dialog\_id | string | 对话ID |

示例如下：

Started返回消息样例

<a id="code-block-4"></a>

```json
{
    "header": {
        "event":"result-generated",
        "task_id": "f894c16f-f20e-4c1d-837e-89e0fbc63a43"
    },
    "payload": {
        "output":{
          "event": "Started",
          "dialog_id": "dd84xxxx-xxxx-xxxx-xxxx-xxxxb7bb"
        }
    }
}
```

<a id="结束会话"></a>

<a id="3a4e21be9563m"></a>

### 结束会话

<a id="stop-input-message"></a>

<a id="ed70d4193bihk"></a>

#### Stop - Input Message

| 一级参数 | 二级参数 | 类型 | 是否必选 | 说明 |
| --- | --- | --- | --- | --- |
| input | directive | string | 是 | 指令名称：Stop |
|  | dialog\_id | string | 否 | 对话ID |

示例如下：

Stop请求样例

<a id="code-block-5"></a>

```json
{
    "header": {
        "action":"finish-task",
        "task_id": "f894c16f-f20e-4c1d-837e-89e0fbc63a43",
        "streaming":"duplex"
    },
    "payload": {
        "input":{
          "directive": "Stop",
          "dialog_id": "dd84xxxx-xxxx-xxxx-xxxx-xxxxb7bb"
        }
    }
}
```

<a id="stopped-output-message"></a>

<a id="4dda641432be2"></a>

#### Stopped - Output Message

| 一级参数 | 二级参数 | 类型 | 是否必选 | 说明 |
| --- | --- | --- | --- | --- |
| output | event | string | 是 | 事件名称：Stopped |
|  | dialog\_id | string | 是 | 对话ID |

示例如下：

<a id="code-block-6"></a>

```json
{
    "header": {
        "event":"result-generated",
        "task_id": "f894c16f-f20e-4c1d-837e-89e0fbc63a43"
    },
    "payload": {
        "output":{
          "event": "Stopped",
          "dialog_id": "dd84xxxx-xxxx-xxxx-xxxx-xxxxb7bb"
        }
    }
}
```

<a id="服务端下发状态切换事件"></a>

<a id="8fc863293amcu"></a>

### 服务端下发状态切换事件

<a id="dialogstatechanged-output-message"></a>

<a id="7e67f7ec50f6z"></a>

#### DialogStateChanged - Output Message

| 一级参数 | 二级参数 | 类型 | 是否必选 | 说明 |
| --- | --- | --- | --- | --- |
| output | event | string | 是 | 事件名称：DialogStateChanged |
|  | state | string | 是 | AI交互状态，取值范围：Listening，Thinking， Responding<br><br>注意：其中状态Listening 只是表示SDK可以发语音给服务端，不代表客户端是否开麦 |
|  | dialog\_id | string | 是 | 对话ID |

示例如下：

<a id="code-block-7"></a>

```json
{
    "header": {
        "event":"result-generated",
        "task_id": "f894c16f-f20e-4c1d-837e-89e0fbc63a43"
    },
    "payload": {
        "output":{
          "event": "DialogStateChanged",
          "state": "Listening",
          "dialog_id": "dd84xxxx-xxxx-xxxx-xxxx-xxxxb7bb"
        }
    }
}
```

<a id="请求上传语音"></a>

<a id="96541eff55v86"></a>

### 请求上传语音

<a id="requesttospeak-input-message"></a>

<a id="edd2de91d9zcb"></a>

#### RequestToSpeak - Input Message

当前状态不是Listening，而用户又想说话时，先提交此事件打断大模型的回答，等待服务端应答。

具体触发此事件的用户行为根据交互类型有所不同，比如用户按下按钮、语音打断（依赖双工模块）等。

| 一级参数 | 二级参数 | 类型 | 是否必选 | 说明 |
| --- | --- | --- | --- | --- |
| input | directive | string | 是 | 指令名称：RequestToSpeak |
|  | dialog\_id | string | 否 | 对话ID |

示例如下：

<a id="code-block-8"></a>

```json
{
    "header": {
        "action":"continue-task",
        "task_id": "f894c16f-f20e-4c1d-837e-89e0fbc63a43",
        "streaming":"duplex"
    },
    "payload": {
        "input":{
          "directive": "RequestToSpeak",
          "dialog_id": "dd84xxxx-xxxx-xxxx-xxxx-xxxxb7bb"
        }
    }
}
```

<a id="requestaccepted-output-message-请求被准许"></a>

<a id="532ee1c9efeii"></a>

#### RequestAccepted - Output Message 请求被准许

| 一级参数 | 二级参数 | 类型 | 是否必选 | 说明 |
| --- | --- | --- | --- | --- |
| output | event | string | 是 | 事件名称：RequestAccepted |
|  | dialog\_id | string | 是 | 对话ID |

示例如下：

<a id="code-block-9"></a>

```json
{
    "header": {
        "event":"result-generated",
        "task_id": "f894c16f-f20e-4c1d-837e-89e0fbc63a43"
    },
    "payload": {
        "output":{
          "event": "RequestAccepted",
          "dialog_id": "dd84xxxx-xxxx-xxxx-xxxx-xxxxb7bb"
        }
    }
}
```

<a id="上传语音指令"></a>

<a id="52da7f14ec2ga"></a>

### 上传语音指令

<a id="sendspeech-input-message"></a>

<a id="cec23c1556u8x"></a>

#### SendSpeech - Input Message

当Start消息指定模式为push2talk，需要客户端告知服务端用户何时开始说话。在Listening状态下，当用户按下按键时应上报SendSpeech消息，通知服务端即将开始上传语音，语音数据应紧接着此事件之后发送。

| 一级参数 | 二级参数 | 类型 | 是否必选 | 说明 |
| --- | --- | --- | --- | --- |
| input | directive | string | 是 | 指令名称：SendSpeech |
|  | dialog\_id | string | 否 | 对话ID |

示例如下：

<a id="code-block-10"></a>

```json
{
    "header": {
        "action":"continue-task",
        "task_id": "f894c16f-f20e-4c1d-837e-89e0fbc63a43",
        "streaming":"duplex"
    },
    "payload": {
        "input":{
          "directive": "SendSpeech",
          "dialog_id": "dd84xxxx-xxxx-xxxx-xxxx-xxxxb7bb"
        }
    }
}
```

<a id="stopspeech-input-message"></a>

<a id="d11933e7b5jz0"></a>

#### StopSpeech - Input Message

当Start消息指定模式为push2talk的时候，用户说完话松开按键时，客户端必须使用StopSpeech消息通知服务端结束语音指令输入。

| 一级参数 | 二级参数 | 类型 | 是否必选 | 说明 |
| --- | --- | --- | --- | --- |
| input | directive | string | 是 | 指令名称：StopSpeech |
|  | dialog\_id | string | 否 | 对话ID |

示例如下：

<a id="code-block-11"></a>

```json
{
    "header": {
        "action":"continue-task",
        "task_id": "f894c16f-f20e-4c1d-837e-89e0fbc63a43",
        "streaming":"duplex"
    },
    "payload": {
        "input":{
          "directive": "StopSpeech",
          "dialog_id": "dd84xxxx-xxxx-xxxx-xxxx-xxxxb7bb"
        }
    }
}
```

<a id="cancelspeech-input-message"></a>

<a id="033cbf278074j"></a>

#### CancelSpeech - Input Message

当Start消息指定模式为push2talk或tap2talk的时候，在语音输入过程中，用户可以使用CancelSpeech消息结束语音输入。服务会结束识别，回到空闲状态。

| 一级参数 | 二级参数 | 类型 | 是否必选 | 说明 |
| --- | --- | --- | --- | --- |
| input | directive | string | 是 | 指令名称：CancelSpeech |
|  | dialog\_id | string | 否 | 对话ID |

示例如下：

<a id="code-block-12"></a>

```json
{
    "header": {
        "action":"continue-task",
        "task_id": "f894c16f-f20e-4c1d-837e-89e0fbc63a43",
        "streaming":"duplex"
    },
    "payload": {
        "input":{
          "directive": "CancelSpeech",
          "dialog_id": "dd84xxxx-xxxx-xxxx-xxxx-xxxxb7bb"
        }
    }
}
```

<a id="语音识别开始-结束"></a>

<a id="d594e7d5853wk"></a>

### 语音识别开始/结束

<a id="speechstarted-output-message"></a>

<a id="4dad1fc3265ro"></a>

#### SpeechStarted - Output Message

当服务端检测到asr语音起点时下发此事件。

| 一级参数 | 二级参数 | 类型 | 是否必选 | 说明 |
| --- | --- | --- | --- | --- |
| output | event | string | 是 | 事件名称：SpeechStarted |
|  | dialog\_id | string | 是 | 对话ID |

示例如下：

<a id="code-block-13"></a>

```json
{
    "header": {
        "event":"result-generated",
        "task_id": "f894c16f-f20e-4c1d-837e-89e0fbc63a43"
    },
    "payload": {
        "output":{
          "event": "SpeechStarted",
          "dialog_id": "dd84xxxx-xxxx-xxxx-xxxx-xxxxb7bb"
        }
    }
}
```

<a id="speechended-output-message"></a>

<a id="e5e95eb9a3uy2"></a>

#### SpeechEnded - Output Message

当服务端检测到asr语音尾点时下发此事件，如果客户端还在上传音频，则收到此事件后应停止上传音频。

| 一级参数 | 二级参数 | 类型 | 是否必选 | 说明 |
| --- | --- | --- | --- | --- |
| output | event | string | 是 | 事件名称：SpeechEnded |
|  | dialog\_id | string | 是 | 对话ID |

示例如下：

<a id="code-block-14"></a>

```json
{
    "header": {
        "event":"result-generated",
        "task_id": "f894c16f-f20e-4c1d-837e-89e0fbc63a43"
    },
    "payload": {
        "output":{
          "event": "SpeechEnded",
          "dialog_id": "dd84xxxx-xxxx-xxxx-xxxx-xxxxb7bb"
        }
    }
}
```

<a id="指定应答内容"></a>

<a id="d8cb5ffb9aemh"></a>

### 指定应答内容

<a id="requesttorespond-input-message"></a>

<a id="ea3b4279e717m"></a>

#### RequestToRespond - Input Message

在Listening状态时，通知服务端与用户主动交互，服务端会根据type字段把在text字段中上传的文本直接转换为语音下发，或调用大模型，返回的结果再转换为语音下发。

<table><thead><tr><th><p><strong>一级参数</strong></p></th><th><p><strong>二级参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>是否必选</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td rowspan="4"><p>input</p></td><td><p>directive</p></td><td><p>string</p></td><td><p>是</p></td><td><p>指令名称：RequestToRespond</p></td></tr><tr><td><p>dialog_id</p></td><td><p>string</p></td><td><p>是</p></td><td><p>对话ID</p></td></tr><tr><td><p>type</p></td><td><p>string</p></td><td><p>是</p></td><td><p>服务应该采取的交互类型，目前支持两种：</p><ul><li><p>transcript：表示直接把文本转语音</p></li><li><p>prompt：表示把文本发送给大模型让其进行回答</p></li></ul></td></tr><tr><td><p>text</p></td><td><p>string</p></td><td><p>是</p></td><td><p>要处理的文本，非null。</p><ul><li><p>调用部分agent时，text可以是&quot;&quot;空字符串，服务端只需要使用parameters中的images或者biz_params参数即可处理。具体参考<a href="official-agent-297b22931e69e622.md">调用官方Agent</a>。</p></li></ul></td></tr><tr><td rowspan="3"><p>parameters</p></td><td><p>history</p></td><td><p>list[]</p></td><td><p>否</p></td><td><p>客户自己组织的问答历史，会覆盖服务内默认维护的问答历史，影响后续所有问答。</p></td></tr><tr><td><p>images</p></td><td><p>list[]</p></td><td><p>否</p></td><td><p>需要分析的图片信息</p></td></tr><tr><td><p>biz_params</p></td><td><p>object</p></td><td><p>否</p></td><td><p>参数说明参考下方 <a href="multimodal-interaction-protocol-23b12b66c717437f.md">parameters.biz_params的参数说明</a>表格</p></td></tr></tbody></table>

**parameters.history**内每条记录的参数说明如下：

| 一级参数 | 类型 | 是否必选 | 说明 |
| --- | --- | --- | --- |
| role | string | 是 | 本记录是哪个角色说的，只支持user, assistant两种。<br><br>注意：不支持设为system |
| content | string | 是 | 具体文本内容 |

**parameters.images**内每个图片的参数说明如下：

<table><thead><tr><th><p><strong>一级参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>是否必选</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td><p>type</p></td><td><p>string</p></td><td><p>是</p></td><td><p>图片类型，支持两种：base64/url</p></td></tr><tr><td><p>value</p></td><td><p>string</p></td><td><p>是</p></td><td><p>图片内容。</p><ul><li><p>当type为base64时，这里是图片的base64字符串。</p></li><li><p>当type为url时，这里是图片的url地址。</p></li></ul></td></tr></tbody></table>

**parameters.biz\_params**的参数说明如下：

| 一级参数 | 类型 | 是否必选 | 说明 |
| --- | --- | --- | --- |
| videos | list\[\] | 否 | 用来控制进入和退出视频通话。<br><br>示例如下：<br><br>payload.biz\_params.videos.action为connect，表示进入视频模式。<br><br>payload.biz\_params.videos.action为exit，表示退出视频模式。 |
| 其他参数 |  | 否 | 与[Start](multimodal-interaction-protocol-23b12b66c717437f.md#5b2363d40585y)消息中`parameters.biz_params`相同，传递对话系统自定义参数。RequestToRespond的`biz_params`参数只在本次请求中生效。 |

> **说明**
>
> 除了videos参数外，`parameters.biz_params`与[Start](multimodal-interaction-protocol-23b12b66c717437f.md#5b2363d40585y)消息中的`parameters.biz_params`相同，传递对话系统自定义参数。RequestToRespond的`biz_params`参数只在本次请求中生效。

<a id="code-block-15"></a>

```json
{
    "header": {
        "action":"continue-task",
        "task_id": "f894c16f-f20e-4c1d-837e-89e0fbc63a43",
        "streaming":"duplex"
    },
    "payload": {
        "input":{
          "directive": "RequestToRespond",
          "dialog_id": "dd84xxxx-xxxx-xxxx-xxxx-xxxxb7bb",
          "type": "prompt",
          "text": "你好，你有什么想聊的呢"
        },
        "parameters":{
          "images":[{
              "type": "base64",
              "value": "aGVsbG8gd29ybGQ="
          }],
          "biz_params":{
            "user_defined_params":{},
            "videos": [
                  {
                    "action": "connect/exit",
                    "type": "voicechat_video_channel"
                  }
                ]
          }
        }
    }
}
```

<a id="ai语音应答状态"></a>

<a id="125b3f72ca808"></a>

### AI语音应答状态

<a id="respondingstarted-output-message"></a>

<a id="0693e9d4a5f91"></a>

#### RespondingStarted - Output Message

AI语音应答开始，sdk要准备接收服务端下发的语音数据

| 一级参数 | 二级参数 | 类型 | 是否必选 | 说明 |
| --- | --- | --- | --- | --- |
| output | event | string | 是 | 事件名称：RespondingStarted |
|  | dialog\_id | string | 是 | 对话ID |

示例如下：

<a id="code-block-16"></a>

```json
{
    "header": {
        "event":"result-generated",
        "task_id": "f894c16f-f20e-4c1d-837e-89e0fbc63a43"
    },
    "payload": {
        "output":{
          "event": "RespondingStarted",
          "dialog_id": "dd84xxxx-xxxx-xxxx-xxxx-xxxxb7bb"
        }
    }
}
```

<a id="respondingended-output-message"></a>

<a id="402cbee340r1m"></a>

#### RespondingEnded - Output Message

AI语音应答结束

| 一级参数 | 二级参数 | 类型 | 是否必选 | 说明 |
| --- | --- | --- | --- | --- |
| output | event | string | 是 | 事件名称：RespondingEnded |
|  | dialog\_id | string | 是 | 对话ID |

示例如下：

<a id="code-block-17"></a>

```json
{
    "header": {
        "event":"result-generated",
        "task_id": "f894c16f-f20e-4c1d-837e-89e0fbc63a43"
    },
    "payload": {
        "output":{
          "event": "RespondingEnded",
          "dialog_id": "dd84xxxx-xxxx-xxxx-xxxx-xxxxb7bb"
        }
    }
}
```

<a id="客户端播放事件"></a>

<a id="04875c3cf6yua"></a>

### 客户端播放事件

<a id="localrespondingstarted-input-message"></a>

<a id="0ebcb0b0714eh"></a>

#### LocalRespondingStarted - Input Message

客户端开始播放服务端下发的音频

| 一级参数 | 二级参数 | 类型 | 是否必选 | 说明 |
| --- | --- | --- | --- | --- |
| input | directive | string | 是 | 指令名称：LocalRespondingStarted |
|  | dialog\_id | string | 否 | 对话ID |

示例如下：

<a id="code-block-18"></a>

```json
{
    "header": {
        "action":"continue-task",
        "task_id": "f894c16f-f20e-4c1d-837e-89e0fbc63a43",
        "streaming":"duplex"
    },
    "payload": {
        "input":{
          "directive": "LocalRespondingStarted",
          "dialog_id": "dd84xxxx-xxxx-xxxx-xxxx-xxxxb7bb"
        }
    }
}
```

<a id="localrespondingended-input-message"></a>

<a id="f4b1a6bf22ymq"></a>

#### LocalRespondingEnded - Input Message

客户端播放服务端下发的音频完成，服务端根据此消息判断端侧语音播放结束，结束当前问答，重新切换到Listening状态。

| 一级参数 | 二级参数 | 类型 | 是否必选 | 说明 |
| --- | --- | --- | --- | --- |
| input | directive | string | 是 | 指令名称：LocalRespondingEnded |
|  | dialog\_id | string | 否 | 对话ID |

示例如下：

<a id="code-block-19"></a>

```json
{
    "header": {
        "action":"continue-task",
        "task_id": "f894c16f-f20e-4c1d-837e-89e0fbc63a43",
        "streaming":"duplex"
    },
    "payload": {
        "input":{
          "directive": "LocalRespondingEnded",
          "dialog_id": "dd84xxxx-xxxx-xxxx-xxxx-xxxxb7bb"
        }
    }
}
```

<a id="文本下发事件"></a>

<a id="588b9df38azvr"></a>

### 文本下发事件

<a id="speechcontent-output-message"></a>

<a id="07fb23a571ekv"></a>

#### SpeechContent - Output Message

| 一级参数 | 二级参数 | 类型 | 是否必选 | 说明 |
| --- | --- | --- | --- | --- |
| output | event | string | 是 | 事件名称：SpeechContent |
|  | dialog\_id | string | 是 | 对话ID |
|  | text | string | 是 | 用户语音识别出的文本，流式返回，每次返回从识别开始到当前的完整识别结果。例如，您会先收到`"text": "你好"`，接着收到`"text": "你好世界"`。 |
|  | finished | bool | 是 | 输出是否结束 |

示例如下：

<a id="code-block-20"></a>

```json
{
    "header": {
        "event":"result-generated",
        "task_id": "f894c16f-f20e-4c1d-837e-89e0fbc63a43"
    },
    "payload": {
        "output":{
          "event": "SpeechContent",
          "dialog_id": "dd84xxxx-xxxx-xxxx-xxxx-xxxxb7bb",
          "text": "一二三",
          "finished": false
        }
    }
}
```

<a id="respondingcontent-output-message"></a>

<a id="3b421d978fco5"></a>

#### RespondingContent - Output Message

<table><thead><tr><th><p><strong>一级参数</strong></p></th><th><p><strong>二级参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>是否必选</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td><p>output</p></td><td><p>event</p></td><td><p>string</p></td><td><p>是</p></td><td><p>事件名称：RespondingContent</p></td></tr><tr><td></td><td><p>dialog_id</p></td><td><p>string</p></td><td><p>是</p></td><td><p>对话ID</p></td></tr><tr><td></td><td><p>round_id</p></td><td><p>string</p></td><td><p>是</p></td><td><p>本轮交互的ID</p></td></tr><tr><td></td><td><p>llm_request_id</p></td><td><p>string</p></td><td><p>是</p></td><td><p>调用llm的request_id</p></td></tr><tr><td></td><td><p>text</p></td><td><p>string</p></td><td><p>是</p></td><td><p>系统对外输出的文本，流式全量输出</p></td></tr><tr><td></td><td><p>spoken</p></td><td><p>string</p></td><td><p>是</p></td><td><p>合成语音时使用的文本，流式全量输出</p></td></tr><tr><td></td><td><p>finished</p></td><td><p>bool</p></td><td><p>是</p></td><td><p>输出是否结束</p></td></tr><tr><td></td><td><p>extra_info</p></td><td><p>object</p></td><td><p>否</p></td><td><p>其他扩展信息，目前支持：</p><ul><li><p>commands: 命令字符串，<strong>此字段为JSON字符串，需要进行二次解析。</strong>各类agent使用的命令字符串可以参考<a href="official-agent-297b22931e69e622.md">调用官方Agent</a>的说明。</p></li><li><p>agent_info: 智能体信息</p></li><li><p>tool_calls: 插件返回的信息</p></li><li><p>word_timestamps: tts对应文本时间戳信息</p></li></ul><p>如果没有扩展信息要提交则省略此字段。</p></td></tr></tbody></table>

示例如下：

<a id="code-block-21"></a>

```json
{
    "header": {
        "event": "result-generated",
        "task_id": "f894c16f-f20e-4c1d-837e-89e0fbc63a43"
    },
    "payload": {
        "output": {
            "event": "RespondingContent",
            "dialog_id": "dd84xxxx-xxxx-xxxx-xxxx-xxxxb7bb",
            "text": "您输入了数字序列"12345"。如果您有关于这些数字的问题或者需要我用它们来完成某项任务，请告诉我更多的细节，我会尽力帮助您。",
            "spoken": "您输入了数字序列"12345"。如果您有关于这些数字的问题或者需要我用它们来完成某项任务，请告诉我更多的细节，我会尽力帮助您。",
            "finished": true,
            "extra_info": {
                "commands": "[{\"name\":\"VOLUME_SET\",\"params\":[{\"name\":\"series\",\"normValue\":\"70\",\"value\":\"70\"}]}]",
                "tool_calls": [
                    {
                        "id": "",
                        "type": "function",
                        "function": {
                            "name": "function_name",
                            "arguments": "{\"id\": \"123\", \"name\": \"test\"}",
                            "outputs": "{\"result\": \"success\"}",
                            "status": {
                                "code": 200,
                                "message": "Success."
                            }
                        }
                    }
                ]
            }
        }
    }
}
```

<a id="客户端更新事件"></a>

<a id="39b223a2f6y9y"></a>

### 客户端更新事件

<a id="updateinfo-input-message"></a>

<a id="649c4ce759ep7"></a>

#### UpdateInfo - Input Message

| 一级参数 | 二级参数 | 三级参数 | 类型 | 是否必选 | 说明 |
| --- | --- | --- | --- | --- | --- |
| input | directive |  | string | 是 | 指令名称：UpdateInfo |
|  | dialog\_id |  | string | 否 | 对话ID |
| parameters | images |  | list\[\] | 否 | 图片数据 |
|  | client\_info | status | object | 否 | 客户端当前状态 |
|  | biz\_params |  | object | 否 | 与Start消息中biz\_params相同，传递对话系统自定义参数。UpdateInfo指令中biz\_params下面每个子项会全量替换Start指令中biz\_params下面的同名项，并在本次连接后续所有对话中生效。 |
|  | upstream | language | String | 否 | 语音识别语种更新，不配置则语种不变。设置多个语种时，使用英文逗号分隔，例如：`zh,en`。 |
|  | downstream | language | String | 否 | 语音合成语种更新，不配置则语种不变。 |

示例如下：

<a id="code-block-22"></a>

```json
{
    "header": {
        "action":"continue-task",
        "task_id": "f894c16f-f20e-4c1d-837e-89e0fbc63a43",
        "streaming":"duplex"
    },
    "payload": {
        "input":{
          "directive": "UpdateInfo",
          "dialog_id": "dd84xxxx-xxxx-xxxx-xxxx-xxxxb7bb"
        },
        "parameters":{
          "images":[{
              "type": "base64",
              "value": "base64String"
          }],
          "client_info": {
              "status": {
                  "bluetooth_announcement": {
                      "status": "stopped"
                  },
                  "stream_media_playback": {
                      "status": "stopped"
                  },
                  "phone_ringing": {
                      "status": "stopped"
                  },
                  "stream_media_playback_qq": {
                      "status": "stopped"
                  }
              }
          },
          "biz_params":{
          }
        }
    }
}
```

<a id="心跳事件"></a>

<a id="adedb03b40fzw"></a>

### 心跳事件

可以通过定期向服务端发送此消息，避免连接超时断开。考虑到预留网络延迟和处理时间的buffer，建议发送频率50秒一次。服务端会回应相同消息，客户端收到不需要做任何处理，忽略即可。

<a id="heartbeat-input-message"></a>

<a id="ab649a20bagsl"></a>

#### HeartBeat - Input Message

| 一级参数 | 二级参数 | 类型 | 是否必选 | 说明 |
| --- | --- | --- | --- | --- |
| input | directive | string | 是 | 指令名称：**HeartBeat** |
|  | dialog\_id | string | 否 | 对话id |

示例：

<a id="code-block-23"></a>

```json
{
  "header": {
    "action": "continue-task",
    "task_id": "f894c16f-f20e-4c1d-837e-89e0fbc63a43",
    "streaming": "duplex"
  },
  "payload": {
    "input": {
      "directive": "HeartBeat",
      "dialog_id": "dd84xxxx-xxxx-xxxx-xxxx-xxxxb7bb"
    }
  }
}
```

<a id="heartbeat-output-message"></a>

<a id="696a99197ejce"></a>

#### HeartBeat - Output Message

| 一级参数 | 二级参数 | 类型 | 是否必选 | 说明 |
| --- | --- | --- | --- | --- |
| output | event | string | 是 | 事件名称：**HeartBeat** |
|  | dialog\_id | string | 是 | 对话id |

示例：

<a id="code-block-24"></a>

```json
{
    "header": {
        "event":"result-generated",
        "task_id": "f894c16f-f20e-4c1d-837e-89e0fbc63a43"
    },
    "payload": {
        "output":{
          "event": "HeartBeat",
          "dialog_id": "dd84xxxx-xxxx-xxxx-xxxx-xxxxb7bb"
        }
    }
}
```

<a id="错误事件"></a>

<a id="61f76efaaci3b"></a>

### 错误事件

<a id="error-output-message"></a>

<a id="480a36a0b3w8k"></a>

#### Error - Output Message

<table><thead><tr><th><p><strong>一级参数</strong></p></th><th><p><strong>二级参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>是否必选</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td rowspan="3"><p>output</p></td><td><p>error_code</p></td><td><p>int</p></td><td><p>是</p></td><td><p>错误码</p></td></tr><tr><td><p>error_name</p></td><td><p>string</p></td><td><p>是</p></td><td><p>错误名称</p></td></tr><tr><td><p>error_message</p></td><td><p>string</p></td><td><p>是</p></td><td><p>错误消息</p></td></tr></tbody></table>

<a id="code-block-25"></a>

```json
{
    "header": {
        "event":"result-generated",
        "task_id": "f894c16f-f20e-4c1d-837e-89e0fbc63a43"
    },
    "payload": {
        "output":{
          "event": "Error",
          "dialog_id": "dd84xxxx-xxxx-xxxx-xxxx-xxxxb7bb",
          "error_code": 500,
          "error_name": "InternalLLMError",
          "error_message": "Internal LLM error"
        }
    }
}
```

<a id="错误码"></a>

<a id="d4ae67ae2cgzn"></a>

### 错误码

如遇报错问题，请参见[多模态交互套件-错误码](multimodal-error-code-27e8073eb3267722.md)进行排查。

若问题仍未解决，请联系技术支持，反馈遇到的问题，并提供完整的request\_id和dialog\_id，以便进一步排查问题。

<a id="术语说明"></a>

<a id="266e769fd83o8"></a>

## 术语说明

**VAD**：Voice Activity Detection，语音活动检测。

**ASR**：Automatic Speech Recognition，自动语音识别。

**TTS**：Text-to-Speech，文本转语音，语音合成。

**LLM**：Large Language Model，大语言模型。
