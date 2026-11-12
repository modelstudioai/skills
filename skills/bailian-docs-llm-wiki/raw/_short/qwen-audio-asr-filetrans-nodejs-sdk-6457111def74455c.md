# Qwen-Audio-ASR-Filetrans Node.js SDK

通过语音 Node.js SDK 调用 Qwen-Audio-ASR-Filetrans，提交录音文件 URL、查询异步任务并下载转写结果。

## 安装 SDK

需要 Node.js 18 或以上版本。下载 [SDK 0.1.0 安装包](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f90c7.tgz)后，在项目目录运行：

```
npm install ./dashscope-sdk-nodejs-0.1.0.tgz
```

## 快速开始

在[控制台](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key)获取 API Key，并配置为环境变量 `DASHSCOPE_API_KEY`。

将以下示例保存为 `example.mjs`，运行 `node example.mjs`。

```
import { TranscriptionClient } from 'dashscope-sdk-nodejs/asr'

const client = new TranscriptionClient({
  apiKey: process.env.DASHSCOPE_API_KEY,
  workspaceId: process.env.DASHSCOPE_WORKSPACE_ID,
  baseUrl: 'dashscope.aliyuncs.com',
  model: 'qwen-audio-3.1-asr-flash-filetrans',
})
const job = await client.transcribe(
  'https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3',
)
for (const result of job.results) {
  if (result.subtaskStatus === 'SUCCEEDED') {
    console.log('Transcript:', result.text)
  } else {
    console.error(result.code, result.message)
    process.exitCode = 1
  }
}
```

## 接口参考

### 构造参数

`TranscriptionClient` 的构造参数如下。

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

模型 ID，默认 `qwen-audio-3.1-asr-flash-filetrans`。

`pollIntervalMs`

`number`

否

查询间隔，默认 `3000` ms。

`pollTimeoutMs`

`number`

否

轮询超时（ms），默认 `600000`。

`requestTimeoutMs`

`number`

否

单次 HTTP 请求超时（ms），默认 `30000`；`0` 表示不限制单次请求。

### 转写参数

`transcribe()` 和 `submitTask()` 的第二个参数为 `parameters`，第三个参数可传入 `context`。模型参数的完整说明见 [HTTP API](raw/_short/qwen-audio-asr-filetrans-http-api-e0184f38f9d98459.md)。

参数

类型

必填

说明

`fileUrls`

`string | string[]`

是

公网可访问的音频 URL；每次提交一个文件。

`parameters.keep_dialect`

`boolean`

否

保留方言表达，默认 `false`。

`parameters.vocabulary_id`

`string`

否

预编译热词列表 ID。

`parameters.vocabulary`

`Record<string, number>`

否

即时热词：键为词，值为权重 `[1,5]` 或 `50`。

`parameters.channel_id`

`number[]`

否

音轨索引，默认 `[0]`。

`parameters.special_word_filter`

`string | Record<string, unknown>`

否

敏感词过滤配置，可传 JSON 字符串或对象。

`parameters.diarization_enabled`

`boolean`

否

单声道音频的说话人分离，默认 `false`。

`parameters.speaker_count`

`number`

否

说话人数量参考值，范围 `[2,100]`，需启用说话人分离。

`parameters.language_hints`

`string[]`

否

识别语言提示，最多使用前 4 个值；未设置时自动识别。

`callOpts.context / submitOpts.context`

`AsrContextMessage[]`

否

识别上下文。消息格式为 `{ role, content: [{ type: "input_text", text }] }`，`role` 为 `user` 或 `assistant`；每种角色最多 5 条，文本共少于 400 字符，按对话轮次排列。

`callOpts.onProgress`

`(status: string, response: QueryTaskResponse) => void`

否

查询进度回调，接收 `status` 和原始响应 `response`。

### 主要方法

方法

返回值

说明

`transcribe(fileUrls: string | string[], parameters?: TranscriptionParameters, callOpts?: TranscribeCallOptions)`

`Promise<TranscriptionJobResult>`

提交音频、轮询并下载结果；`callOpts` 可设置上下文和进度回调。

`submitTask(fileUrls: string | string[], parameters?: TranscriptionParameters, submitOpts?: TranscriptionSubmitOptions)`

`Promise<{ taskId: string; taskStatus: string }>`

提交任务并返回任务 ID、初始状态；`submitOpts.context` 设置识别上下文。

`fetchTask(taskId: string, requestTimeoutMs?: number)`

`Promise<QueryTaskResponse>`

查询一次任务，返回状态和结果下载链接。

### 返回结果

字段

类型

说明

`taskId`

`string`

任务 ID。

`taskStatus`

`string`

任务状态。

`results`

`FileTranscriptionResult[]`

文件结果列表，包含 `subtaskStatus`、`text`、`transcription`；失败项含 `code`、`message`。

`usage`

`RecognitionUsage | undefined`

服务端返回的用量统计。

`raw`

`QueryTaskResponse`

原始任务查询响应。
