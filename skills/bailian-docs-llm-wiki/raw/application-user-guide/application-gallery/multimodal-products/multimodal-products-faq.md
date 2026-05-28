# 多模态交互开发套件常见问题

## **功能介绍**

#### **语音合成支持哪些音色？**

CosyVoice-V2 支持的音色请参见：[语音合成-CosyVoice/Sambert](https://help.aliyun.com/zh/model-studio/text-to-speech#b757915932oz2)中 CosyVoice音色列表（CosyVoice-V2）。

Sambert 支持的音色请参见：[语音合成-CosyVoice/Sambert](https://help.aliyun.com/zh/model-studio/text-to-speech#b757915932oz2)中 Sambert音色列表。

通义千问-TTS 支持的音色请参见：[实时语音合成-通义千问](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide)。

#### **端侧支持哪些算法？仅是唤醒、指令这种，还是其他什么能力？**

端侧SDK里集成了语音唤醒、端侧 VAD（Voice Activity Detection，语音活动检测）、AEC 回声消除（Acoustic Echo Cancellation）、定向识音算法，详情参见[端侧算法](https://help.aliyun.com/zh/model-studio/multimodal-app-configuration#86521c2463nfi)。

#### **实时语音交互场景 push2talk/tap2talk/duplex 这三种 upstream 模式有什么区别？**

Push2Talk（按键通话）模式：按住按钮开始录音，松开按钮停止录音；

Tap2Talk（点击通话）模式：点击一次开始录音，再次点击结束录音；

Duplex（全双工）模式：支持同时双向通信，可实现边听边说的实时交流。

#### **语音翻译支持哪些语种？**

详见 [语音翻译](https://help.aliyun.com/zh/model-studio/official-agent#231a402a82pkh)。

## **配置与开发**

#### **音频数据采集和播放的格式要求是什么？**

详情参见：[音频采集和播放说明](https://help.aliyun.com/zh/model-studio/audio-capture-and-playback-instructions)。

#### **调用接口时 task\_id 需要每次生成新的吗？**

每次开启新会话时，要用新的 task\_id。task\_id 作为会话标识，可能会影响配置或状态判断。以SDK方式调用时，则无需关注，SDK会自动为新会话生成 task\_id。

#### **如何拼接特殊业务逻辑进提示词，一起传给大模型？**

在配置提示词时，您可以通过「自定义变量」实现这一功能，配置方法请参考[提示词](https://help.aliyun.com/zh/model-studio/multimodal-app-configuration#74a8b82973u0r)。

#### **能支持哪些类型的百炼工作空间？**

目前只支持主工作空间，请使用主空间的 workspaceId 接入。

## **部署**

#### **能否支持海外部署？**

百炼多模交互开发套件可以在海外接入使用，但尚不支持海外服务节点部署。海外接入时，降低网络延迟的方案请咨询商务。

## **问题排查**

#### **为什么TTS播报时，出现了文本中没有的内容？**

检查文本中是否有特殊格式或字符，如Markdown。TTS模型目前会将Markdown内容念出来，您可以约束模型不输出Markdown格式的内容，或对输出文本做特殊字符过滤。

#### **官网示例语音正常，换成自己待测试的语音就获取不到识别结果？**

检查音频文件格式：

-   建议您检查待测试的语音格式是否符合语音识别输入格式要求，格式要求请参见[音频采集和播放说明](https://help.aliyun.com/zh/model-studio/audio-capture-and-playback-instructions)。
    
-   将待测试语音转换成16kHz、16 bit采样位数、单声道（mono）无压缩的WAV文件。
    

#### **Tap2Talk/Duplex 模式下，发送音频没有最终结果返回？**

Tap2Talk/Duplex 模式使用云端 VAD（Voice Activity Detection，语音活动检测） 检测音频尾点。 使用音频文件调用时，需确保音频文件末尾至少包含 800-1000ms 静音，否则无法结束识别。

#### **为什么视频通话和视觉类 Agent 没有遵循指令？**

目前「理解与生成」模块的提示词不直接对 Agent 生效，您可以在「视频通话」和「拍照问答」Agent 中，设置对应的提示词。支持一键导入「理解与生成」模块的提示词及对应变量配置。

## **计费**

#### **有哪些计费模式？**

支持后付费与License模式。每个账号可获取一次10元免费试用额度用于后付费模式。购买节省计划可抵扣多模态交互所有按量付费项目。详细计费说明、购买链接参见：[产品计费](https://help.aliyun.com/zh/model-studio/product-billing)。

#### **特殊 Agent 交互次数如何统计？**

语音翻译：启动一次语音翻译到退出，算一次调用。

实时视频通话：启动后，一问一答算作一次调用。
