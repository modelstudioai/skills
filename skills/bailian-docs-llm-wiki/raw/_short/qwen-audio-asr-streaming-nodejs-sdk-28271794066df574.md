# Qwen-Audio-ASR-Streaming Node.js SDK

通过语音 Node.js SDK 调用 Qwen-Audio-ASR-Streaming，流式发送音频并接收识别结果、上下文和用量信息。

## 安装 SDK

需要 Node.js 18 或以上版本。下载 [SDK 0.1.0 安装包](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f90c7.tgz)后，在项目目录运行：

```
npm install ./dashscope-sdk-nodejs-0.1.0.tgz
```

## 快速开始

在[控制台](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key)获取 API Key，并配置为环境变量 `DASHSCOPE_API_KEY`。

下载[示例音频](https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3)，保存为 `input.mp3`，并转换为 16 kHz、16-bit、单声道 PCM：

```
ffmpeg -i input.mp3 -f s16le -ac 1 -ar 16000 input.pcm
```

将以下示例保存为 `example.mjs`，运行 `node example.mjs`。

```
import { readFile } from 'node:fs/promises'
import { setTimeout as sleep } from 'node:timers/promises'
import { RecognitionClient } from 'dashscope-sdk-nodejs/asr'

const pcm = await readFile('input.pcm')
const asr = new RecognitionClient({
  apiKey: process.env.DASHSCOPE_API_KEY,
  workspaceId: process.env.DASHSCOPE_WORKSPACE_ID,
  baseUrl: 'dashscope.aliyuncs.com',
  model: 'qwen-audio-3.1-asr-flash-streaming',
  format: 'pcm',
  sampleRate: 16000,
})
asr.on('sentenceEnd', sentence => console.log('Final sentence:', sentence.text))
asr.on('error', err => console.error(err.code, err.message))

try {
  await asr.start()
  for (let offset = 0; offset < pcm.length; offset += 3200) {
    asr.sendAudio(pcm.subarray(offset, offset + 3200))
    await sleep(100)
  }
  await asr.finish()
} finally {
  asr.close()
}
```

## 接口参考

### 构造参数

`RecognitionClient` 的构造参数如下。

参数

类型

必填

说明

`apiKey`

`string`

否

API Key。默认读取 `DASHSCOPE_API_KEY`。

`workspaceId`

`string`

否

业务空间 ID。默认读取 `DASHSCOPE_WORKSPACE_ID`。

`baseUrl`

`string`

否

服务域名，默认 `dashscope.aliyuncs.com`（北京）。

`model`

`string`

否

模型 ID，默认 `qwen-audio-3.1-asr-flash-streaming`。

`format`

`'pcm' | 'wav' | 'mp3' | 'opus' | 'speex' | 'aac' | 'amr'`

否

音频格式，默认 `pcm`；WAV 使用 PCM 编码，Opus/Speex 使用 Ogg 封装，AMR 使用 AMR-NB。

`sampleRate`

`number`

否

实际音频采样率（Hz），默认 `16000`。

`vocabularyId`

`string`

否

预编译热词列表 ID。

`languageHints`

`string[]`

否

识别语言提示，最多使用前 4 个值；未设置时自动识别。

`multiThresholdModeEnabled`

`boolean`

否

多阈值模式，避免 VAD 断句过长，默认 `false`。

`maxSentenceSilence`

`number`

否

VAD 断句静音阈值（ms），范围 `[200,6000]`，默认 `800`。

`heartbeat`

`boolean`

否

静音保活开关，默认 `false`；开启后需持续发送静音音频。

`context`

`AsrContextMessage[]`

否

识别上下文。消息格式为 `{ role, content: [{ type: "input_text", text }] }`，`role` 为 `user` 或 `assistant`；每种角色最多 5 条，文本共少于 400 字符，按对话轮次排列。

`parameters`

`Partial<RecognitionParameters>`

否

其他识别参数，如 `vad_model`、`keep_dialect` 和 `vocabulary`。

`connectTimeoutMs`

`number`

否

建连超时（ms），默认 `10000`。

`taskTimeoutMs`

`number`

否

任务启动或结束的等待超时（ms），默认 `60000`；`0` 表示不限制。

`parameters.vad_model`

`'near_meeting_16k' | 'far_field_meeting_16k'`

否

近场或远场 VAD，默认 `far_field_meeting_16k`。

`parameters.keep_dialect`

`boolean`

否

保留方言表达，默认 `false`。

`parameters.vocabulary`

`Record<string, number>`

否

即时热词：键为词，值为权重 `[1,5]` 或 `50`。

`parameters.speech_noise_threshold`

`number`

否

VAD 灵敏度阈值，范围 `[-1,1]`。

### 主要方法

方法

返回值

说明

`start()`

`Promise<void>`

启动识别任务，完成后可发送音频。

`sendAudio(audio: Buffer | Uint8Array)`

`void`

按配置的格式和采样率发送音频帧。

`finish()`

`Promise<void>`

结束音频输入并等待任务完成，文本通过回调返回。

`close(code?: number, reason?: string)`

`void`

关闭连接并释放任务资源。

### 回调事件

通过 `on(event, listener)` 注册回调；完整事件字段见[服务端事件](raw/_short/qwen-audio-asr-streaming-server-events-4757090610f208c7.md)。

事件

负载

说明

`started`

`{ taskId: string }`

任务已启动，可发送输入。

`result`

`{ text: string; sentence_end: boolean; sentence_begin?: boolean; words?: RecognitionWord[] }`

中间或最终句子，已过滤心跳结果。

`sentenceEnd`

`{ text: string; sentence_end: boolean; sentence_begin?: boolean; words?: RecognitionWord[] }`

最终句子，`sentence_end === true`。

`finished`

`{ taskId: string; duration?: number; usage?: RecognitionUsage }`

任务已结束，本地任务状态已清理。

`failed / error`

`DashScopeError`

调用错误，包含 `code`、`message` 和请求标识。

`close`

`{ code: number; reason: string }`

底层连接关闭通知。

`event`

`ServerEvent`

原始服务端 JSON 消息。
