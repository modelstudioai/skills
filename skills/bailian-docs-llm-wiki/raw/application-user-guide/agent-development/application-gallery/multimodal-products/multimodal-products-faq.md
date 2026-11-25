# 多模态交互开发套件常见问题

<a id="功能介绍"></a>

<a id="28fe576f6dznk"></a>

## 功能介绍

<a id="语音合成支持哪些音色"></a>

<a id="7cdfd42d02zi8"></a>

#### 语音合成支持哪些音色？

CosyVoice-V2 支持的音色请参见：[实时语音合成-CosyVoice /Sambert](https://help.aliyun.com/zh/model-studio/text-to-speech)中 CosyVoice音色列表（CosyVoice-V2）。

Sambert 支持的音色请参见：[实时语音合成-CosyVoice /Sambert](https://help.aliyun.com/zh/model-studio/text-to-speech)中 Sambert音色列表。

通义千问-TTS 支持的音色请参见：[实时语音合成](../../../../model-user-guide/model-experience/speech-and-audio/speech-synthesis/realtime-tts-user-guide.md)。

<a id="端侧支持哪些算法-仅是唤醒-指令这种-还是其他什么能力"></a>

<a id="d1dc49e20aele"></a>

#### 端侧支持哪些算法？仅是唤醒、指令这种，还是其他什么能力？

端侧SDK里集成了语音唤醒、端侧 VAD（Voice Activity Detection，语音活动检测）、AEC 回声消除（Acoustic Echo Cancellation）、定向识音算法，详情参见[端侧算法](../../../../_short/multimodal-app-configuration-8919f99b339e17da.md#fb2cbc9b879g8)。

<a id="实时语音交互场景-push2talk-tap2talk-duplex-这三种-upstream-模式有什么区别"></a>

<a id="50a0a3d137py7"></a>

#### 实时语音交互场景 push2talk/tap2talk/duplex 这三种 upstream 模式有什么区别？

Push2Talk（按键通话）模式：按住按钮开始录音，松开按钮停止录音；

Tap2Talk（点击通话）模式：点击一次开始录音，再次点击结束录音；

Duplex（全双工）模式：支持同时双向通信，可实现边听边说的实时交流。

<a id="语音翻译支持哪些语种"></a>

<a id="7b691fc8dcymn"></a>

#### 语音翻译支持哪些语种？

详见[语音翻译](../../../../_short/official-agent-297b22931e69e622.md#231a402a82pkh)。

<a id="配置与开发"></a>

<a id="378a0fc3f7i9e"></a>

## 配置与开发

<a id="音频数据采集和播放的格式要求是什么"></a>

<a id="3b87f1d6e3mtr"></a>

#### 音频数据采集和播放的格式要求是什么？

详情参见：[音频采集和播放说明](../../../../_short/audio-capture-and-playback-instructions-73592f9927f41ea9.md)。

<a id="调用接口时-task-id-需要每次生成新的吗"></a>

<a id="3670d5cecel60"></a>

#### 调用接口时 task\_id 需要每次生成新的吗？

每次开启新会话时，要用新的 task\_id。task\_id 作为会话标识，可能会影响配置或状态判断。以SDK方式调用时，则无需关注，SDK会自动为新会话生成 task\_id。

<a id="如何拼接特殊业务逻辑进提示词-一起传给大模型"></a>

<a id="17e61e8a86d8i"></a>

#### 如何拼接特殊业务逻辑进提示词，一起传给大模型？

在配置提示词时，您可以通过“自定义变量”实现这一功能，配置方法请参考[提示词](../../../../_short/multimodal-app-configuration-8919f99b339e17da.md#cbbc5f73caixw)。

<a id="能支持哪些类型的百炼工作空间"></a>

<a id="4f30ea75e1kn4"></a>

#### 能支持哪些类型的百炼工作空间？

目前只支持主工作空间，请使用主空间的 workspaceId 接入。

<a id="部署"></a>

<a id="436603ca533r4"></a>

## 部署

<a id="能否支持海外部署"></a>

<a id="3afb2849b6js7"></a>

#### 能否支持海外部署？

百炼多模交互开发套件可以在海外接入使用，但尚不支持海外服务节点部署。海外接入时，降低网络延迟的方案请咨询商务。

<a id="问题排查"></a>

<a id="835fa743345bf"></a>

## 问题排查

<a id="为什么tts播报时-出现了文本中没有的内容"></a>

<a id="d1deb9cbafp4l"></a>

#### 为什么TTS播报时，出现了文本中没有的内容？

检查文本中是否有特殊格式或字符，如Markdown。TTS模型目前会将Markdown内容念出来，您可以约束模型不输出Markdown格式的内容，或对输出文本做特殊字符过滤。

<a id="官网示例语音正常-换成自己待测试的语音就获取不到识别结果"></a>

<a id="15887eda19h3a"></a>

#### 官网示例语音正常，换成自己待测试的语音就获取不到识别结果？

检查音频文件格式：

-   建议您检查待测试的语音格式是否符合语音识别输入格式要求，格式要求请参见[音频采集和播放说明](../../../../_short/audio-capture-and-playback-instructions-73592f9927f41ea9.md)。
-   将待测试语音转换成16kHz、16 bit采样位数、单声道（mono）无压缩的WAV文件。

<a id="tap2talk-duplex-模式下-发送音频没有最终结果返回"></a>

<a id="a3a1f3b167j9o"></a>

#### Tap2Talk/Duplex 模式下，发送音频没有最终结果返回？

Tap2Talk/Duplex 模式使用云端 VAD（Voice Activity Detection，语音活动检测） 检测音频尾点。 使用音频文件调用时，需确保音频文件末尾至少包含 800-1000ms 静音，否则无法结束识别。

<a id="为什么视频通话和视觉类-agent-没有遵循指令"></a>

<a id="4f0b90a2e18yo"></a>

#### 为什么视频通话和视觉类 Agent 没有遵循指令？

目前“理解与生成”模块的提示词不直接对 Agent 生效，您可以在“视频通话”和“拍照问答”Agent 中，设置对应的提示词。支持一键导入“理解与生成”模块的提示词及对应变量配置。

<a id="计费"></a>

<a id="55fecb3468ub4"></a>

## 计费

<a id="有哪些计费模式"></a>

<a id="afa7d020d3dyz"></a>

#### 有哪些计费模式？

支持后付费与License模式。每个账号可获取一次10元免费试用额度用于后付费模式。购买节省计划可抵扣多模态交互所有按量付费项目。详细计费说明、购买链接参见：[产品计费](product-billing.md)。

<a id="特殊-agent-交互次数如何统计"></a>

<a id="d0b5063973wzv"></a>

#### 特殊 Agent 交互次数如何统计？

语音翻译：启动一次语音翻译到退出，算一次调用。

实时视频通话：启动后，一问一答算作一次调用。
