# 非实时语音合成Qwen-Audio-TTS Python SDK参考

本文介绍非实时语音合成Qwen-Audio-TTS的Python SDK调用方法，支持非流式和流式两种调用模式。

**重要**本文描述的功能仅在华北2（北京）地域可用。

**重要**阿里云百炼为华北2（北京）地域推出了业务空间专属域名，能够为推理请求提供卓越的性能和更高的稳定性，建议从 `dashscope.aliyuncs.com` 迁移至 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`。

## 前提条件

-   已[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)并将其配置到环境变量
-   已安装符合版本要求的DashScope Python SDK，建议[安装最新版](raw/model-api-reference/preparations/install-sdk.md)，SDK版本需≥2.0.1

## 核心资源（`client.audio.tts.http`）

**资源路径**：`client.audio.tts.http`

**功能**：基于HTTP的语音合成，`synthesize`方法为非流式调用（音频以URL返回），`stream`方法为流式调用（SSE逐片返回音频数据）。

### synthesize() / stream() - 语音合成调用

**方法签名**：

```
def synthesize(self,
               text: str,
               *,
               model: str,
               voice: str,
               format: str = None,
               sample_rate: int = None,
               language_type: str = None,
               parameters: Dict = None,
               extra_input: Dict = None,
               timeout: float = None,
               ...) -> HttpSynthesis

def stream(self,
           text: str,
           *,
           model: str,
           voice: str,
           format: str = None,
           sample_rate: int = None,
           language_type: str = None,
           parameters: Dict = None,
           extra_input: Dict = None,
           timeout: float = None,
           ...) -> HttpSynthesisStream
```

**参数说明**（`model`、`text`、`voice`、`format`、`sample_rate`、`language_type`为具名参数，其余输入参数通过`extra_input`字典传入）：

**参数**

**类型**

**必填**

**说明**

`model`

`str`

是

语音合成模型。

`text`

`str`

是

待合成文本。

支持 SSML 和 LaTeX 格式输入。将待合成文本替换为对应格式即可。

-   使用 SSML 时，需同时将 `enable_ssml` 设置为 `True`。支持的 SSML 标签及用法，请参见[SSML 与 LaTeX](raw/model-user-guide/model-experience/speech-synthesis/ssml-latex-user-guide.md)。
-   使用 LaTeX 时，将待合成文本替换为 LaTeX 格式即可，无需额外配置。支持的 LaTeX 语法及用法，请参见[LaTeX 公式转语音](https://help.aliyun.com/zh/model-studio/latex-capability-support-description)。

`voice`

`str`

是

音色。

取值范围：

-   系统音色：参见[Qwen-Audio-TTS音色列表](raw/model-user-guide/model-experience/speech-synthesis/tts-voice-list/qwen-audio-tts-voice-list.md)
-   声音复刻音色：如何创建音色请参见[声音复刻HTTP API参考](raw/_short/voice-clone-design-http-api-8f39943e5a676aae.md)
-   声音设计音色：如何创建音色请参见[声音设计API参考](raw/model-api-reference/audio-api-references/speech-synthesis-api-reference/voice-design-api-references.md)

`format`

`str`

否

音频编码格式。

默认值：mp3。

取值范围：

-   mp3
-   pcm
-   wav
-   opus

`sample_rate`

`int`

否

音频采样率（Hz）。

取值范围：8000, 16000, 22050（默认）, 24000, 44100, 48000。

`volume`

`int`

否

音量。

默认值：50。

取值范围：\[0, 100\]。

`rate`

`float`

否

语速。

默认值：1.0。

取值范围：\[0.5, 2.0\]。

`pitch`

`float`

否

音调。

默认值：1.0。

取值范围：\[0.5, 2.0\]。

`bit_rate`

`int`

否

音频码率（单位：kbps）。

默认值：32。

取值范围：\[6, 510\]。

**重要**仅在`format`为`opus`时支持使用该参数。

`enable_ssml`

`bool`

否

是否开启SSML功能。当`text`使用SSML格式时，需设为`True`。默认为`False`。支持的SSML标签及用法，请参考[SSML 与 LaTeX](raw/model-user-guide/model-experience/speech-synthesis/ssml-latex-user-guide.md)。SSML 的使用限制（支持的模型、音色和接口），请参见[使用限制](https://help.aliyun.com/zh/model-studio/ssml-latex-user-guide#sl01_constraint_h3)。

`word_timestamp_enabled`

`bool`

否

是否开启字级别时间戳。

默认值：False。

-   True：开启。
-   False：关闭。

仅在流式输出模式下可用。支持复刻音色；支持的系统音色请参见[Qwen-Audio-TTS音色列表](raw/model-user-guide/model-experience/speech-synthesis/tts-voice-list/qwen-audio-tts-voice-list.md)。

`seed`

`int`

否

生成时使用的随机数种子，使合成的效果产生变化。在模型版本、文本、音色及其他参数均相同的前提下，使用相同的seed可复现相同的合成结果。

默认值0。

取值范围：\[0, 65535\]。

`language_hints`

`list`

否

**重要**

-   此参数为数组，但当前版本仅处理第一个元素，因此建议只传入一个值。
-   此参数用于指定语音合成的目标语言，该设置与声音复刻时的样本音频的语种无关。如需设置复刻任务的源语言，请参见[声音复刻API参考](https://help.aliyun.com/zh/model-studio/voice-clone-design-http-api#h2-create)。

指定语音合成的目标语言，提升合成效果。

当数字、缩写、符号等朗读方式或者小语种合成效果不符合预期时使用，例如：

-   数字朗读方式不符合预期，“hello, this is 110”读成“hello, this is one one zero”而非“hello, this is 幺幺零”
-   符号朗读不准确，“@”读成“艾特”而非“at”
-   小语种合成效果差，合成不自然

取值范围

-   zh：中文
-   en：英语
-   fr：法语
-   de：德语
-   ja：日语
-   ko：韩语
-   ru：俄语
-   pt：葡萄牙语
-   th：泰语
-   id：印尼语
-   vi：越南语
-   es：西班牙语
-   it：意大利语
-   ms：马来西亚语
-   fil：菲律宾语
-   ar：阿拉伯语

`instruction`

`str`

否

设置指令，用于控制方言、情感或角色等合成效果。

具体用法请参见[非实时语音合成](raw/model-user-guide/model-experience/speech-synthesis/non-realtime-tts-user-guide.md)。

`enable_aigc_tag`

`bool`

否

是否在生成的音频中添加AIGC隐性标识。设置为True时，会将隐性标识嵌入到支持格式（wav/mp3/opus）的音频中。

默认值：false。

`aigc_propagator`

`str`

否

设置AIGC隐性标识中的 `ContentPropagator` 字段，用于标识内容的传播者。仅在 `enable_aigc_tag` 为 `True` 时生效。

默认值：阿里云UID。

`aigc_propagate_id`

`str`

否

设置AIGC隐性标识中的 `PropagateID` 字段，用于唯一标识一次具体的传播行为。仅在 `enable_aigc_tag` 为 `True` 时生效。

默认值：本次语音合成请求Request ID。

`hot_fix`

`dict`

否

文本热修复配置，用于自定义指定词语的发音或对待合成文本进行替换。

参数介绍：

-   pronunciation：自定义发音。指定词语的拼音标注，用于纠正默认发音不准确的情况。
-   replace：文本替换。在语音合成前将指定词语替换为目标文本，替换后的文本将作为实际合成内容。

示例：

```
"hot_fix": {
  "pronunciation": [
    {"天气": "tian1 qi4"}
  ],
  "replace": [
    {"今天": "金天"}
  ]
}
```

**返回值**：

-   **非流式模式**（`synthesize`）：返回结果对象（`HttpSynthesis`），包含以下属性：
    
    -   `audio_url`：音频下载URL（有效期有限）。
    -   `audio_id`：音频ID。
    -   `expires_at`：URL过期时间。
    -   `usage`：用量信息。
-   **流式模式**（`stream`）：返回迭代器（`HttpSynthesisStream`），每个元素（`HttpSynthesisChunk`）包含以下属性：
    
    -   `audio`：当前分片的音频二进制数据（bytes，已解码）。
    -   `sentence`：句子级别的合成信息（如有）。
    -   `is_final`：是否为收尾分片（`finish_reason == "stop"`）。
    -   `usage`：用量信息（收尾分片携带）。
    
    **重要**流式模式下，收尾分片（`is_final`为`True`）会额外携带`audio_url`（完整音频的下载地址）、`audio_id`与`expires_at`。遍历迭代器拼接音频时，以`chunk.audio`是否非空决定是否写入，避免同一段内容重复播放。
    

## 示例代码

以下示例展示Qwen-Audio-TTS语音合成的非流式和流式调用方式。运行前请确保已设置环境变量`DASHSCOPE_API_KEY`。

**重要**不同模型需使用匹配的音色。更换模型时，请同步更换音色，并确认音色支持目标语言。具体对应关系请参见[Qwen-Audio-TTS音色列表](raw/model-user-guide/model-experience/speech-synthesis/tts-voice-list/qwen-audio-tts-voice-list.md)。

#### 非流式调用

非流式调用使用`synthesize`方法，等待合成完成后返回音频URL，通过URL下载音频文件。

```
# -*- coding: utf-8 -*-
import os
import dashscope

# 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
client = dashscope.Client(
    # 若没有将API Key配置到环境变量中，请将下行替换为自己的API Key：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

# 非流式调用，返回音频URL
result = client.audio.tts.http.synthesize(
    "今天是个好日子，适合构建人们喜爱的产品！",
    model="qwen-audio-3.0-tts-flash",  # 更换模型时，需同步更换为对应版本的音色
    voice="longanhuan_v3.6",
    format="wav",
    sample_rate=24000,
)

# 获取音频URL
print(f"音频 URL: {result.audio_url}")
print(f"音频 ID: {result.audio_id}")
if result.audio_id:
    request_id = result.audio_id.removeprefix("audio_")
    print(f"请求 Id: {request_id}")
print(f"过期时间: {result.expires_at}")
```

#### 流式调用

流式调用使用`stream`方法，返回迭代器，逐段获取音频数据。适用于对首包延迟有要求的实时播放场景。流式模式下，收尾分片（`chunk.is_final`为`True`）会额外返回完整音频的`audio_url`，拼接时只写入`chunk.audio`非空的数据分片即可，避免音频内容重复。

```
# -*- coding: utf-8 -*-
import os
import dashscope

# 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
client = dashscope.Client(
    # 若没有将API Key配置到环境变量中，请将下行替换为自己的API Key：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

# 流式调用，逐段返回音频数据
stream_result = client.audio.tts.http.stream(
    "今天是个好日子，适合构建人们喜爱的产品！",
    model="qwen-audio-3.0-tts-flash",  # 更换模型时，需同步更换为对应版本的音色
    voice="longanhuan_v3.6",
    format="wav",
    sample_rate=24000,
)

# 遍历迭代器，逐段接收音频数据
audio_chunks = []
for chunk in stream_result:
    if chunk.audio:  # 只写入非空的音频分片，避免音频重复
        audio_chunks.append(chunk.audio)
        print(f"收到音频数据块，大小: {len(chunk.audio)} bytes")

    if chunk.sentence:
        print(f"句子信息: {chunk.sentence}")

    if chunk.is_final:  # 收尾分片：携带完整音频的下载地址与用量
        print(f"Audio ID: {chunk.audio_id}")
        request_id = chunk.audio_id.removeprefix("audio_")
        print(f"请求 Id: {request_id}")
        print(f"音频 URL: {chunk.audio_url}")
        print(f"用量: {chunk.usage}")

# 合并所有音频数据并保存
full_audio = b"".join(audio_chunks)
print(f"总音频大小: {len(full_audio)} bytes")

with open("output.wav", "wb") as f:
    f.write(full_audio)
print("音频已保存到 output.wav")
```
