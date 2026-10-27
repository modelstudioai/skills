# DashScope Python SDK 1.x 历史用法参考

DashScope Python SDK 1.x 接口的历史用法速查与 1.x 到 2.0 的迁移对照，供存量项目参考。

本文面向**仍在使用 DashScope Python SDK 1.x 的存量项目**，集中收录 1.x 接口的典型用法，并给出对应的 2.0 写法。

**警告**新项目请直接使用 [SDK 2.0](raw/model-api-reference/preparations/install-sdk.md)：1.x 已进入冻结维护（只修缺陷、不增功能），1.x 与 2.0 在同一个 `dashscope` 包内并存（2.0.1 起提供），存量代码无需删除 1.x 依赖即可逐步迁移。Assistants / Threads / Runs 系列 API 已随 1.x 下线，服务端不再支持，请勿在新代码中使用。

## 接口迁移总对照

能力

1.x 接口

2.0 接口

文本生成

`Generation.call` / `AioGeneration.call`

`client.chat.completions.create`

多模态对话

`MultiModalConversation.call`

`client.multimodal.chat.create`

图像生成

`ImageSynthesis.call/async_call/fetch/wait`

`client.images.generate` / `client.images.jobs.*`

视频生成

`VideoSynthesis.call/async_call/fetch/wait`

`client.videos.generate` / `client.videos.jobs.*`

录音文件转写

`Transcription.async_call/fetch/wait`

`client.audio.asr.transcribe` / `client.audio.asr.jobs.*`

实时语音识别

`Recognition.start/send_audio_frame/stop`

`client.audio.asr.recognize(...)` 上下文管理器

语音合成

`SpeechSynthesizer`（tts\_v2 回调式）

`client.audio.tts.synthesize/stream/connect`

文本向量

`TextEmbedding.call` / `BatchTextEmbedding`

`client.embeddings.create` / `client.embeddings.jobs.*`

重排序

`TextReRank.call`

`client.rerank.create`

智能体应用

`Application.call`

`client.apps.completions.create`

文件管理

`Files.upload/list/get/delete`

`client.files.upload/list/get/delete`

模型列表

`Models.list/get`

`client.models.list/get`

## 客户端构造与鉴权

1.x 通过模块级全局变量配置；2.0 通过 `Client` 构造参数配置（优先级：构造参数 > `dashscope.settings` > 环境变量 > `~/.dashscope/config.toml`）。

```
# 1.x：全局变量
import dashscope
dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"
```
```
# 2.0：客户端构造
import dashscope
client = dashscope.Client(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)
```

## 文本生成

```
# 1.x
from dashscope import Generation
response = Generation.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="qwen-plus",
    messages=messages,
    result_format="message",
)
if response.status_code == 200:
    print(response.output.choices[0].message.content)
else:
    print(f"HTTP返回码：{response.status_code}")
    print(f"错误码：{response.code}")
    print(f"错误信息：{response.message}")
```
```
# 2.0
from dashscope.v2 import DashScopeError
try:
    response = client.chat.completions.create(
        model="qwen-plus",
        messages=messages,
    )
    print(response.choices[0].message.content)
except DashScopeError as e:
    print(f"HTTP返回码：{e.status_code}")
    print(f"错误码：{e.code}")
    print(f"错误信息：{e.message}")
```

## 多模态对话

```
# 1.x
from dashscope import MultiModalConversation
response = MultiModalConversation.call(
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model='qwen3-vl-plus',
    messages=[{
        "role": "user",
        "content": [
            {"image": "https://example.com/image.png"},
            {"text": "请问图片里有什么？"},
        ],
    }])
print(response.output.choices[0].message.content[0]['text'])
```
```
# 2.0：content parts 形状保留，取值扁平化
response = client.multimodal.chat.create(
    model='qwen3-vl-plus',
    messages=[{
        "role": "user",
        "content": [
            {"image": "https://example.com/image.png"},
            {"text": "请问图片里有什么？"},
        ],
    }])
print(response.output_text)
```

## 图像生成

```
# 1.x：同步 call（阻塞到出图）
from dashscope import ImageSynthesis
rsp = ImageSynthesis.call(api_key=os.getenv("DASHSCOPE_API_KEY"),
                          model=ImageSynthesis.Models.wanx_v1,
                          prompt=prompt,
                          n=1,
                          style='<watercolor>',
                          size='1024*1024')
if rsp.status_code == HTTPStatus.OK:
    for result in rsp.output.results:
        print(result.url)
else:
    print('Failed, status_code: %s, code: %s, message: %s' %
          (rsp.status_code, rsp.code, rsp.message))
```
```
# 2.0：generate 一步式（提交并等待）；枚举类改字符串
job = client.images.generate(
    model="wanx2.1-t2i-turbo",
    prompt=prompt,
    n=1,
    size='1024*1024',
)
for url in job.image_urls:
    print(url)
```

分步任务（1.x `async_call/fetch/wait`）对应 `client.images.jobs.create/fetch/wait`；任务状态判定由 `rsp.output.task_status == 'SUCCEEDED'` 改为 `job.succeeded`。

## 视频生成

```
# 1.x
from dashscope import VideoSynthesis
rsp = VideoSynthesis.call(api_key=api_key,
                          model='wan3.0-video',
                          prompt=prompt,
                          resolution="720P",
                          ratio="16:9",
                          duration=15,
                          watermark=True)
if rsp.status_code == HTTPStatus.OK:
    print("video_url:", rsp.output.video_url)
```
```
# 2.0
job = client.videos.generate(
    model='wan3.0-video',
    prompt=prompt,
    resolution="720P",
    ratio="16:9",
    duration=15,
    watermark=True,
)
print("video_url:", job.video_url)
```

**说明**1.x `VideoSynthesis` 的 `extend_prompt` 默认为 `True`；2.0 为 `prompt_extend` 且缺省由服务端决定，依赖旧默认的调用需显式传 `prompt_extend=True`。

## 录音文件转写

```
# 1.x：async_call 提交 + wait 等待
from dashscope.audio.asr import Transcription
task_response = Transcription.async_call(
    model='paraformer-v2',
    file_urls=['{YOUR_AUDIO_URL}'],
    language_hints=['zh', 'en'],
)
transcribe_response = Transcription.wait(task=task_response.output.task_id)
if transcribe_response.status_code == HTTPStatus.OK:
    print(json.dumps(transcribe_response.output, indent=4, ensure_ascii=False))
```
```
# 2.0：transcribe 一步式；签名外参数走 parameters
job = client.audio.asr.transcribe(
    ['{YOUR_AUDIO_URL}'],
    model='paraformer-v2',
    parameters={'language_hints': ['zh', 'en']},
)
print(json.dumps(job.model_dump(), indent=4, ensure_ascii=False))
```

分步控制（原 `async_call` + 循环 `fetch`）对应 `client.audio.asr.jobs.create` + 循环 `jobs.fetch`。

## 实时语音识别

1.x 使用回调类（`Recognition` + `RecognitionCallback`）；2.0 改为上下文管理器 + 事件迭代。

```
# 1.x（回调式，节选）
from dashscope.audio.asr import Recognition
class Callback(RecognitionCallback):
    def on_result(self, result): ...
recognition = Recognition(model='paraformer-realtime-v2', callback=Callback())
recognition.start()
recognition.send_audio_frame(chunk)
recognition.stop()
```
```
# 2.0（事件迭代式，发送与接收并发）
from concurrent.futures import ThreadPoolExecutor

def receive_events(rec):
    for event in rec.events():
        print(event)

with client.audio.asr.recognize(
        model='paraformer-realtime-v2',
        format='pcm',
        sample_rate=16000,
) as recognition:
    with ThreadPoolExecutor(max_workers=1) as pool:
        receiver = pool.submit(receive_events, recognition)
        for chunk in iter_pcm_chunks():  # 由应用提供实时 PCM 帧
            recognition.send_audio_frame(chunk)
        recognition.stop()
        receiver.result()
```

本地文件一次识别（1.x `Recognition.call(file)`）对应 `for event in client.audio.asr.recognize_file(path, model=...):`。

## 语音合成

1.x `tts_v2` 使用回调收音频；2.0 改为迭代/会话式。

```
# 1.x（回调式，节选）
from dashscope.audio.tts_v2 import SpeechSynthesizer, ResultCallback
class Callback(ResultCallback):
    def on_data(self, data: bytes): audio.write(data)
synthesizer = SpeechSynthesizer(
    model="cosyvoice-v3-flash",
    voice="longanyang",
    callback=Callback(),
)
synthesizer.streaming_call(text)
synthesizer.streaming_complete()
```
```
# 2.0：connect 会话（分段发送 + 逐段收音频）
with client.audio.tts.connect(
        model="cosyvoice-v3-flash",
        voice="longanyang",
        format="mp3",
) as session:
    session.send_text(text)
    session.flush()
    session.stop()  # 结束任务，等待剩余音频返回
    for chunk in session.audio_chunks():
        audio.write(chunk)
```

一次性合成（短文本整段返回）用 `client.audio.tts.synthesize(text, model=..., voice=...)`；纯流式用 `client.audio.tts.stream(text, ...)` 迭代 bytes。

## 文本向量与重排序

```
# 1.x
resp = dashscope.TextEmbedding.call(
    model="qwen3.7-text-embedding",
    input="衣服的质量杠杠的",
)
if resp.status_code == HTTPStatus.OK:
    print(resp)
```
```
# 2.0
resp = client.embeddings.create(
    model="qwen3.7-text-embedding",
    input="衣服的质量杠杠的",
)
for item in resp.embeddings:
    print(item.index, len(item.embedding))
```

批量向量（1.x `BatchTextEmbedding`）对应 `client.embeddings.jobs.create/fetch/wait`。重排序 `TextReRank.call` 对应 `client.rerank.create`，取值由 `resp.output.results[i]` 改为 `resp.results[i]`。

## 智能体应用调用

```
# 1.x
from dashscope import Application
response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id='APP_ID',
    prompt='你是谁？')
if response.status_code != HTTPStatus.OK:
    print(f'code={response.status_code}, message={response.message}')
else:
    print(response.output.text)
```
```
# 2.0
from dashscope.v2 import DashScopeError
try:
    response = client.apps.completions.create(
        app_id='APP_ID',
        prompt='你是谁？')
    print(response.text)
except DashScopeError as e:
    print(f'code={e.code}, message={e.message}')
```

应用流式调用保留 `incremental_output` 参数（帧形态由它决定），逐帧取值由 `response.output.text` 改为 `partial.text`。

## 行为差异要点

迁移时除接口名外，还需要注意以下行为差异：

-   **错误处理**：1.x 在响应对象上自查 `status_code`/`code`；2.0 默认失败直接抛 `DashScopeError` 异常族（含 `e.code`/`e.status_code`/`e.request_id`/`e.message`），需要信封风格可构造 `Client(raise_on_error=False)`。
-   **流式输出**：1.x `Generation.call(stream=True)` 默认每帧重放全量文本（需 `incremental_output=True` 才增量）；2.0 流式一律增量。百炼应用（`apps.completions`）保留 `incremental_output` 开关。
-   **异步任务等待**：1.x `wait` 默认无限等待、超时返回错误响应；2.0 `jobs.wait` 默认 24 小时总预算、指数退避轮询、任务 FAILED 抛异常。
-   **响应结构**：1.x 业务内容包裹在 `output` 字段下（`response.output.choices[...]`）；2.0 已扁平化（`response.choices[...]`），并新增 `resp.output_text`、`job.succeeded` 等便捷取值。
-   **签名外参数**：2.0 各资源方法为封闭具名签名，1.x 透传的模型专属参数需改走 `parameters={...}`（图像素材类走 `extra_input=`）。

## 相关文档

-   安装与升级：[安装 SDK](raw/model-api-reference/preparations/install-sdk.md)
-   文本生成：[文本生成](raw/model-user-guide/model-experience/text-generation-model/text-generation.md)、[流式输出](raw/model-user-guide/model-experience/text-generation-model/stream.md)、[多轮对话](raw/model-user-guide/model-experience/text-generation-model/multi-round-conversation.md)
-   图像与视频：[图像生成](raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)、[视频生成](raw/model-user-guide/model-experience/video-generate-edit-model/text-to-video-guide.md)
-   语音：[录音文件识别](raw/_short/paraformer-recorded-speech-recognition-python-sd-79138235fccede85.md)、[实时语音识别](raw/_short/paraformer-real-time-speech-recognition-python-s-145dc2b30661b050.md)、[实时语音合成](raw/model-user-guide/model-experience/speech-synthesis/realtime-tts-user-guide.md)
-   向量与排序：[向量](raw/model-user-guide/model-experience/embedding-rerank-model/embedding.md)、[重排序](raw/model-user-guide/model-experience/embedding-rerank-model/rerank.md)
-   应用调用：[智能体应用调用](raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
