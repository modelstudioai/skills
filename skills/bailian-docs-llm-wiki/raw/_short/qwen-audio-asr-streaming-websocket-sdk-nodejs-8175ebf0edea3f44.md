# Qwen-Audio-ASR-Streaming Node.js SDK

## 前提条件

在[控制台](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key)获取 API Key，并配置为环境变量 `DASHSCOPE_API_KEY`。

### 安装 SDK

需要 Node.js 18 或以上版本。下载 [SDK 0.1.0 安装包](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f90c7.tgz)后，在项目目录运行：

```
npm install ./dashscope-sdk-nodejs-0.1.0.tgz
```

## 快速开始

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

## 详细参考

-   [请求参数](https://help.aliyun.com/zh/model-studio/realtime-websocket-nodejs-sdk-qwen-audio-asr-fun-asr#model-qwen-audio-asr-streaming)
-   [接口参考](raw/_short/realtime-websocket-nodejs-sdk-qwen-audio-asr-fun-6a032c20c8fc224f.md)
