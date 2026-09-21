# qwen-audio-3.1-tts-next

qwen-audio-3.1-tts-next 是一款面向统一音频生成的 Audiogen 模型，不再局限于传统 TTS 的单一语音合成，而是能够围绕文本、时间戳和参考音频等输入，一次生成完整的音频内容，包括人声、音效、环境音等。模型支持多语种 TTS、单人说话、多人对话、Podcast 播客、影视剧声景、环境音与音效等任务。其核心亮点在于更自然的人声表达、稳定的音色保持、灵活的时间控制，以及高质量综合声景生成能力，适用于内容创作、短视频、播客、影视和游戏音频制作等场景。

## 推理服务供应商

本模型的推理服务由阿里云百炼提供。

## 模型能力

能力项

支持情况

能力项

支持情况

输入模态

文本、参考音频

输出模态

音频

语种

中文、英文

输出方式

非流式

输出格式

WAV、MP3、PCM

参考音频

URL 或 Base64

## 上下文限制

参数

值

最大输入长度

3000 字符

单次生成音频时长上限

播客：240 秒（4 分钟）；其他场景：120 秒

参考音频数量

最多 3 条

单条参考音频时长

最长 30 秒

单条参考音频大小

不超过 10 MB

参考音频格式

WAV、MP3、OGG Opus；不支持裸 PCM

## 模型价格

本文仅展示模型调用原价，不包含限时优惠。活动信息请参见[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)。

#### 华北2（北京）

计费项

单价（元/百万 Token）

输入

6

输出

12

按输入和输出 Token 数分别计费。详情请参见[模型调用计费](https://help.aliyun.com/zh/model-studio/model-pricing#audio-generation-pricing)。

## 限流

#### 华北2（北京）

指标

数值

每秒钟调用次数（RPS）

3

## 调用方式

通过 HTTPS API 调用，返回完整音频文件。效果与提示词写法请参见[音频生成](raw/model-user-guide/model-experience/audio-generation.md)，请求参数及示例请参见[音频生成 API参考](raw/model-api-reference/audio-api-references/audio-generation-api.md)。
