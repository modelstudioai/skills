# Qwen-Audio-Realtime Node.js SDK

通过语音 Node.js SDK 调用 Qwen-Audio-Realtime，配置会话、收发音频、处理转写和工具调用。

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
import { readFileSync, writeFileSync } from 'node:fs'
import { setTimeout as sleep } from 'node:timers/promises'
import { RealtimeClient } from 'dashscope-sdk-nodejs/realtime'

const pcm = readFileSync('input.pcm')
const client = new RealtimeClient({
  apiKey: process.env.DASHSCOPE_API_KEY,
  workspaceId: process.env.DASHSCOPE_WORKSPACE_ID,
  baseUrl: 'dashscope.aliyuncs.com',
  model: 'qwen-audio-3.1-realtime-plus',
  voice: 'longanqian_v3.1',
  turnDetection: null,
  inputTranscription: { language: 'zh' },
})
const audio = []
function fail(err) {
  console.error(err.code, err.message)
  process.exitCode = 1
  client.close()
}
const timer = setTimeout(() => fail(new Error('Response timed out')), 60000)
client.on('close', () => clearTimeout(timer))
client.on('error', fail)
client.on('audio', chunk => audio.push(chunk))
client.on('inputTranscript', ({ transcript }) => console.log('User:', transcript))
client.on('outputTranscript', ({ transcript }) => console.log('Assistant:', transcript))
client.once('sessionUpdated', () => {
  ;(async () => {
    for (let offset = 0; offset < pcm.length; offset += 3200) {
      client.appendAudio(pcm.subarray(offset, offset + 3200))
      await sleep(100)
    }
    client.commit()
    client.createResponse()
  })().catch(fail)
})
client.once('responseDone', event => {
  if (event.response?.status !== 'completed') {
    fail(new Error('Response status: ' + event.response?.status))
    return
  }
  writeFileSync('output.pcm', Buffer.concat(audio))
  client.close()
})
try {
  await client.connect()
} catch (err) {
  fail(err)
}
```

## 接口参考

### 构造参数

`RealtimeClient` 的构造参数如下。

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

是

模型 ID。

`voice`

`string`

否

音色 ID。省略时使用服务端默认音色。

`instructions`

`string`

否

系统指令，设置角色、风格等。

`turnDetection`

`TurnDetection | null`

否

默认 `{ type: "server_vad" }`；`null` 表示手动提交；可使用 `smart_turn` 或 `smart_turn_v2`。

`modalities`

`Array<'text' | 'audio'>`

否

输出模态，默认 `["text", "audio"]`。

`maxHistoryTurns`

`number`

否

历史轮数，范围 `[1,50]`，服务端默认 `20`。

`tools`

`ToolDefinition[]`

否

工具定义；应用执行工具并校验参数。

`inputTranscription`

`{ model?: string; language?: string } | null`

否

输入音频转写配置，如 `{ model: "fun-asr", language: "zh" }`；`null` 关闭转写。

`sessionExtras`

`SessionConfig`

否

扩展会话参数，如 `speech_rate`、`enable_search`；覆盖对应的顶层配置，字段见[客户端事件](raw/model-api-reference/realtime-api-directory/audio-realtime-api-directory/fun-audiochat-client-events.md)。

`connectTimeoutMs`

`number`

否

建连超时（ms），默认 `10000`。

### 主要方法

方法

返回值

说明

`connect()`

`Promise<void>`

建立连接并发送会话配置，通过 `sessionUpdated` 确认配置生效。

`updateSession(session: SessionConfig)`

`void`

更新会话参数，通过 `sessionUpdated` 确认生效。

`appendAudio(pcm: Buffer | Uint8Array)`

`void`

发送 16 kHz、16-bit、单声道 PCM 音频。

`commit()`

`void`

手动模式下提交音频缓冲区。

`clearAudioBuffer()`

`void`

清空尚未提交的音频缓冲区。

`createResponse(response?: Record<string, unknown>)`

`void`

请求模型生成响应。

`cancelResponse()`

`void`

取消当前响应，保留会话。

`createConversationItem(item: ConversationItem, previousItemId?: string)`

`void`

添加对话历史或工具结果；`previousItemId` 指定插入位置。

`submitFunctionCallOutput(callId: string, output: string, autoCreateResponse?: boolean)`

`void`

提交工具结果字符串；`autoCreateResponse` 默认 `true`，自动请求后续响应。

`deleteConversationItem(itemId: string)`

`void`

删除指定对话项。

`retrieveConversationItem(itemId: string)`

`void`

查询对话项，结果通过 `event` 回调返回。

`sendEvent(event: ClientEvent)`

`void`

发送原始客户端事件。

`close(code?: number, reason?: string)`

`void`

关闭会话和 WebSocket 连接。

### 回调事件

通过 `on(event, listener)` 注册回调；完整事件字段见[服务端事件](raw/model-api-reference/realtime-api-directory/audio-realtime-api-directory/qwen-audio-realtime-server-events.md)。

事件

负载

说明

`open`

`void`

连接已建立、初始配置已发送。

`sessionCreated / sessionUpdated`

`ServerEvent`

会话创建或配置确认。

`audio`

`Buffer`

音频二进制块，可多次触发。

`audioTranscriptDelta`

`{ delta: string }`

输出音频转写的增量文本。

`outputTranscript`

`{ transcript: string }`

输出音频的完整转写。

`textDelta / textDone`

`{ delta: string } / { text: string }`

纯文本模态的增量或完整文本。

`inputTranscriptDelta`

`{ text: string; stash: string }`

`text` 是确定文本，`stash` 是暂存文本；以二者替换当前显示，而非累计拼接。

`inputTranscript`

`{ transcript: string }`

输入音频的最终转写。

`speechStarted / speechStopped`

`ServerEvent`

检测到用户语音开始或停止。

`responseCreated / responseDone`

`ServerEvent`

响应开始或结束。检查 `responseDone.response.status` 是否为 `completed`，或为取消、失败状态。

`functionCall`

`{ callId: string; name: string; arguments: string }`

完整工具调用参数；由应用解析并校验 `arguments` JSON 字符串。

`ambientTranscript / ambientTranscriptCompleted`

`{ text: string; stash: string } / { transcript: string }`

环境音当前或最终转写，不写入会话上下文。

`event`

`ServerEvent`

原始服务端 JSON 消息。

`error`

`DashScopeError`

连接或服务端错误。

`close`

`{ code: number; reason: string }`

底层连接关闭通知。
