# Qwen-Audio-TTS Node.js SDK

通过语音 Node.js SDK 调用 Qwen-Audio-TTS，使用一次性或流式文本输入生成音频，并处理字级时间戳和用量事件。

## 安装 SDK

需要 Node.js 18 或以上版本。下载 [SDK 0.1.0 安装包](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f90c7.tgz)后，在项目目录运行：

```
npm install ./dashscope-sdk-nodejs-0.1.0.tgz
```

## 快速开始

在[控制台](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key)获取 API Key，并配置为环境变量 `DASHSCOPE_API_KEY`。

将以下示例保存为 `example.mjs`，运行 `node example.mjs`。

```
import { writeFile } from 'node:fs/promises'
import { SpeechSynthesizer } from 'dashscope-sdk-nodejs/tts'

const synth = new SpeechSynthesizer({
  apiKey: process.env.DASHSCOPE_API_KEY,
  workspaceId: process.env.DASHSCOPE_WORKSPACE_ID,
  baseUrl: 'dashscope.aliyuncs.com',
  model: 'qwen-audio-3.1-tts-flash',
  voice: 'longanhuan_v3.1',
  format: 'mp3',
  sampleRate: 24000,
})
synth.on('error', err => console.error(err.code, err.message))

try {
  const audio = await synth.synthesize('Hello, welcome to Qwen Audio.')
  await writeFile('output.mp3', audio)
} finally {
  synth.close()
}
```

## 接口参考

### 构造参数

`SpeechSynthesizer` 的构造参数如下。

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

模型 ID。默认 `qwen-audio-3.1-tts-flash`。

`voice`

`string`

是

音色 ID，使用与模型匹配的[音色](raw/model-user-guide/model-experience/speech-and-audio/speech-synthesis/tts-voice-list/qwen-audio-tts-voice-list.md)。

`format`

`'pcm' | 'wav' | 'mp3' | 'opus'`

否

音频编码格式。省略时使用服务端默认值。

`sampleRate`

`8000 | 16000 | 22050 | 24000 | 44100 | 48000`

否

音频采样率（Hz），与编码格式匹配；省略时由服务端决定。

`volume`

`number`

否

音量，范围 `[0,100]`，服务端默认 `50`。

`rate`

`number`

否

语速，范围 `[0.5,2.0]`，服务端默认 `1.0`。

`pitch`

`number`

否

音调，范围 `[0.5,2.0]`，服务端默认 `1.0`。

`wordTimestampEnabled`

`boolean`

否

是否返回字级时间戳，默认 `false`。

`languageHints`

`string[]`

否

目标语言提示，当前仅第一个元素生效。

`instruction`

`string`

否

方言、情感或角色等合成指令。

`parameters`

`TtsSynthesisParameters`

否

其他合成参数，如 `enable_ssml`、`seed` 和 `hot_fix`。

`connectTimeoutMs`

`number`

否

建连超时（ms），默认 `10000`。

`taskTimeoutMs`

`number`

否

任务启动或结束的等待超时（ms），默认 `60000`；`0` 表示不限制。

`parameters.enable_ssml`

`boolean`

否

开启 SSML。一次任务只发送一次完整的非空 SSML 文本；[使用限制](raw/model-user-guide/model-experience/speech-and-audio/speech-synthesis/ssml-latex-user-guide.md)。

`parameters.bit_rate`

`number`

否

MP3/Opus 码率（kbps），参数范围 `[6,510]`，默认 `32`。

`parameters.seed`

`number`

否

随机种子，范围 `[0,65535]`。

`parameters.hot_fix`

`Record<string, unknown>`

否

热修复配置，通过 `parameters.hot_fix` 传入；结构见[客户端事件](raw/_short/qwen-audio-tts-client-events-26c1ffacfaed1e62.md)。

### 主要方法

方法

返回值

说明

`synthesize(text: string)`

`Promise<Buffer>`

合成完整文本并返回音频，文本最多 20000 字符。

`begin()`

`Promise<void>`

启动流式合成任务，完成后可发送文本。

`sendText(text: string)`

`void`

发送文本片段；每次最多 20000 字符，单任务累计最多 200000 字符。

`end()`

`Promise<Buffer>`

结束文本输入，等待合成完成并返回完整音频。

`cancel()`

`void`

发送取消合成的请求。

`close(code?: number, reason?: string)`

`void`

关闭连接并释放任务资源。

### 回调事件

通过 `on(event, listener)` 注册回调；完整事件字段见[服务端事件](raw/_short/qwen-audio-tts-server-events-e9137ffe8f4e3d2c.md)。

事件

负载

说明

`started`

`{ taskId: string }`

任务已启动，可发送输入。

`audio`

`Buffer`

音频二进制块，可多次触发。

`sentenceBegin`

`{ index: number; text: string }`

开始合成一个句子。

`sentenceEnd`

`{ index: number; text: string; characters?: number; words?: TtsWord[]; usage?: TtsUsage }`

句子合成完成；可获取字级时间戳及原始用量。

`finished`

`{ taskId: string; characters?: number; usage?: TtsUsage }`

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
