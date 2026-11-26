# Qwen-Audio-ASR HTTP API

提交音频文件的公网 URL 或 Base64 Data URI，获取转写文本和词级时间戳。支持一次返回结果或通过 SSE 流式返回。

<a id="h-fl-url"></a>

> **说明**
>
> 示例使用华北2（北京）地域。将 `{WorkspaceId}` 替换为[业务空间 ID](https://bailian.console.aliyun.com/cn-beijing/settings/workspace)，并将环境变量 `DASHSCOPE_API_KEY` 设为该地域的 [API Key](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key)。

POST`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

<a id="请求头"></a>

<a id="h-fl-hd"></a>

## 请求头

`Authorization`string必填

使用与请求地址对应的 API Key，格式为 `Bearer <API Key>`。

`Content-Type`string必填

请求参数的媒体类型，固定为`application/json`。

<a id="h-fl-stream-logic"></a>

`X-DashScope-SSE`string可选

控制结果的返回方式。

-   `enable`：请求流式返回，按响应的 `Content-Type` 选择解析方式。
    -   `text/event-stream`：逐个读取 SSE 事件，将 `data:` 后的内容解析为 JSON。
    -   `application/json`：按单个 JSON 对象解析整个响应。
-   `disable` 或不传：一次返回最终结果。

> **说明**
>
> qwen-audio-3.0-asr-flash 在音频时长不少于 1 分钟时才以 SSE 流式方式返回结果。

<a id="请求参数"></a>

<a id="h-fl-rq"></a>

## 请求参数

`model`string必填

模型名称。

`input`object必填

输入信息。

`messages`array\[object\]必填

消息列表。可在待识别音频前添加对话上下文。包含音频的 `user` 消息必须放在最后。

`role`string必填

消息角色。

-   `user`（必选）：至少一条用户消息须包含待识别的音频。其他用户消息可提供上下文。
-   `assistant`（可选）：提供之前的模型回复。

`content`array\[object\]必填

消息内容列表。

`type`string必填

按消息角色选择内容类型。每个请求至少包含一项 `input_audio`。

-   `input_audio`：`user` 的音频，必填 `input_audio` 对象。
-   `input_text`：`user` 的上下文，必填 `text` 字段。
-   `text`：`assistant` 的上下文，必填 `text` 字段。

`input_audio`object条件必填

当`type`为`input_audio`时必填。

`data`string必填

待识别的音频数据，支持两种输入方式。

-   **公网 URL**：传入可公开访问的音频文件地址，例如 `https://example.com/audio/sample.wav`。
-   **[Base64 Data URI](https://www.rfc-editor.org/rfc/rfc2397)**：传入与音频格式匹配的 MIME 类型和 Base64 编码的文件内容，例如 `data:audio/wav;base64,{BASE64_ENCODED_DATA}`。MP3 文件可使用 `audio/mpeg`。Base64 编码会增大数据体积，文件大小和时长限制见[音频规格](../model-user-guide/model-experience/speech-and-audio/speech-recognition/asr-model.md#asr_audio_spec02)。

<a id="accordion-如何生成-base64-data-uri"></a>

如何生成 Base64 Data URI

以下示例将本地 WAV 文件 `sample.wav` 编码为 Base64 Data URI，输出可直接传给 `input_audio.data`。可使用[示例 WAV 音频](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/zh/audios/6a4b3c2d1e0f9093.wav)运行示例。

<a id="fig-code-group"></a>

<a id="fig-code-group-python-tab"></a>

python

<a id="code-code-group-python"></a>

```python
import base64
from pathlib import Path

audio = Path("sample.wav").read_bytes()
print("data:audio/wav;base64," + base64.b64encode(audio).decode("ascii"))
```

<a id="fig-code-group-java-tab"></a>

java

<a id="code-code-group-java"></a>

```java
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Base64;

public class Main {
    public static void main(String[] args) throws Exception {
        byte[] audio = Files.readAllBytes(Paths.get("sample.wav"));
        System.out.println("data:audio/wav;base64," + Base64.getEncoder().encodeToString(audio));
    }
}
```

`text`string条件必填

上下文文本可提高专有词汇的识别准确率，使用方法见[上下文增强](../model-user-guide/model-experience/speech-and-audio/speech-recognition/improve-asr-accuracy.md#ctx_enhance_h2)。根据 `type` 填写以下内容。

-   `input_text`：前几轮用户语音的识别结果，或与当前音频相关的领域词表。
-   `text`：前几轮对话中的模型回复。

> **说明**
>
> -   消息数量：`input_text` 和 `text` 类型的上下文消息各最多 5 条，超出时保留最近的 5 条。
> -   文本长度：每轮 `user` 和 `assistant` 的 `text` 字段总长度不超过 400 个字符，每个字符计为 1；超出部分从末尾截断。
> -   消息顺序：按对话轮次排列，每轮中 `user`（`input_text` 类型）必须在对应的 `assistant`（`text` 类型）之前。

`parameters`object必填

模型参数。

`format`string必填

填写音频文件的实际格式，例如 `wav`、`mp3` 或 `opus`。支持的格式见[音频规格](../model-user-guide/model-experience/speech-and-audio/speech-recognition/asr-model.md#asr_audio_spec02)。

`sample_rate`string可选

音频采样率（Hz）。例如，16 kHz 音频填写 `16000`。支持的采样率见[音频规格](../model-user-guide/model-experience/speech-and-audio/speech-recognition/asr-model.md#asr_audio_spec02)。

`speaker_diarization_enabled`boolean可选

> **说明**
>
> 仅适用于 qwen-audio-3.1-asr-flash。

是否启用说话人分离，默认值为 `false`。设为 `true` 时，通过响应中的 `speaker_id` 区分说话人，并返回 `output.sentences`。开启后，`keep_dialect` 和 `language_hints` 不生效。

`keep_dialect`boolean可选

> **说明**
>
> 仅适用于 qwen-audio-3.1-asr-flash。

是否保留方言表达。

-   `false`：将方言转写为普通话文本（默认）。
-   `true`：保留方言表达。

`language_hints`array\[string\]可选

指定语种可提高识别准确率。最多传入 4 个语言代码，超出时仅前 4 个生效。无法确定语种时可省略，模型会自动识别。

<a id="accordion-支持的语言代码"></a>

支持的语言代码

-   `zh`: 中文
-   `en`: 英文
-   `ja`: 日语
-   `ko`: 韩语
-   `vi`: 越南语
-   `th`: 泰语
-   `id`: 印尼语
-   `ms`: 马来语
-   `tl`: 菲律宾语
-   `hi`: 印地语
-   `ar`: 阿拉伯语
-   `fr`: 法语
-   `de`: 德语
-   `es`: 西班牙语
-   `pt`: 葡萄牙语
-   `ru`: 俄语
-   `it`: 意大利语
-   `nl`: 荷兰语
-   `sv`: 瑞典语
-   `da`: 丹麦语
-   `fi`: 芬兰语
-   `no`: 挪威语
-   `el`: 希腊语
-   `pl`: 波兰语
-   `cs`: 捷克语
-   `hu`: 匈牙利语
-   `ro`: 罗马尼亚语
-   `bg`: 保加利亚语
-   `hr`: 克罗地亚语
-   `sk`: 斯洛伐克语

qwen-audio-3.1-asr-flash 还支持以下语言代码：

-   `tr`: 土耳其语
-   `fa`: 波斯语
-   `mr`: 马拉地语
-   `ml`: 马拉雅拉姆语
-   `ne`: 尼泊尔语
-   `ky`: 吉尔吉斯语
-   `az`: 阿塞拜疆语
-   `ka`: 格鲁吉亚语
-   `hy`: 亚美尼亚语
-   `sl`: 斯洛文尼亚语
-   `sq`: 阿尔巴尼亚语
-   `et`: 爱沙尼亚语
-   `lv`: 拉脱维亚语
-   `lt`: 立陶宛语
-   `ca`: 加泰罗尼亚语
-   `eu`: 巴斯克语
-   `gl`: 加利西亚语
-   `or`: 奥里亚语
-   `dv`: 迪维希语
-   `as`: 阿萨姆语
-   `kmr`: 北库尔德语
-   `tig`: 提格雷语
-   `fy`: 西弗里西亚语
-   `ba`: 巴什基尔语
-   `be`: 白俄罗斯语
-   `tt`: 鞑靼语
-   `ia`: 国际语
-   `mhr`: 草原马里语
-   `tok`: 道本语

`vocabulary_id`string可选

预编译热词列表 ID。

需预先调用创建热词列表接口生成，识别时传入该 ID 即可使用列表中的热词。

适用于词汇已知且相对稳定、需要跨请求复用同一词表的场景。

使用方法请参见[预编译热词](../model-user-guide/model-experience/speech-and-audio/speech-recognition/improve-asr-accuracy.md#hw_precompiled_h3)。

`vocabulary`object可选

用[即时热词](../model-user-guide/model-experience/speech-and-audio/speech-recognition/improve-asr-accuracy.md#hw_instant_h3)为当前请求指定词汇，无需预先创建词表。键为热词文本（`string`），值为权重（`integer`），例如 `{"祺元": 5, "洛柯": 5, "璇枢": 5}`。

热词权重可取以下值：

-   `1～5`：数值越大，模型越倾向于输出该词。
-   `50`：超级热词，可显著提高召回率，最多 50 个。

> **说明**
>
> 同时传入 `vocabulary_id` 和 `vocabulary` 时，系统会合并两类热词。合并后超过 2000 个时，随机选用 2000 个。

<a id="响应参数"></a>

<a id="h-fl-rs"></a>

## 响应参数

`request_id`string

本次请求的唯一标识。

`output`object

输出结果。

`sentence`object

当前句子的详细信息。

`sentence_id`integer

句子编号，从1开始。

`begin_time`integer

句子开始时间，单位毫秒。

`end_time`integer | null

句子结束时间，单位为毫秒。`sentence_end` 为 `true` 时读取有效值。

`text`string

当前句子的识别文本。

`channel_id`integer

声道编号，从0开始。

`speaker_id`integer | null

> **说明**
>
> 仅 qwen-audio-3.1-asr-flash 支持说话人分离。

开启说话人分离时返回说话人编号；关闭时该字段可能缺省或为 `null`。

`sentence_end`boolean

当前句子是否识别完成。

-   `true`：句子已结束。对 qwen-audio-3.0-asr-flash，此时词级时间戳已固定。
-   `false`：句子尚未结束，后续事件可能更新文本和时间戳。

`words`array\[object\]

词级别时间戳列表。

`begin_time`integer

词开始时间，单位毫秒。

`end_time`integer

词结束时间，单位毫秒。

`text`string

词文本。

`punctuation`string

词后的标点符号。无标点时为空字符串。

`fixed`boolean

词级时间戳是否已固定。使用 qwen-audio-3.1-asr-flash 且未开启说话人分离时，以此字段判断。

-   `true`：该词的时间戳已固定。
-   `false`：后续事件可能更新时间戳。

`speaker_id`integer | null

> **说明**
>
> 仅 qwen-audio-3.1-asr-flash 支持说话人分离。

词对应的说话人编号。开启说话人分离时返回编号，未开启时为 `null`。

`text`string

当前累积的完整识别文本。

`sentences`array\[object\]

> **说明**
>
> 仅适用于 qwen-audio-3.1-asr-flash。

开启说话人分离时返回。包含当前及历史句子的识别结果，每个元素的结构与 `sentence` 相同。

`usage`object

当前句子结束时返回用量，中间结果可省略此字段。

> **说明**
>
> -   qwen-audio-3.0-asr-flash 按音频时长（`duration`）计费。
> -   qwen-audio-3.1-asr-flash 按输入和输出 Token（`input_tokens`、`output_tokens`）计费，同时返回 `duration` 和 `total_tokens`。

`duration`integer

已处理的音频时长，单位秒。

`input_tokens`integer

本次调用消耗的输入 Token 数。

`output_tokens`integer

本次调用消耗的输出 Token 数。

`total_tokens`integer

本次调用消耗的总 Token 数，等于 `input_tokens` 与 `output_tokens` 之和。

<a id="sec-tabs"></a>

<a id="非流式"></a>

<a id="非流式-h4"></a>

#### 非流式

<a id="code-block"></a>

```bash
curl "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -H "X-DashScope-SSE: disable" \
  --data '{
  "model": "qwen-audio-3.1-asr-flash",
  "input": {
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "input_audio",
            "input_audio": {"data": "https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/zh/audios/6a4b3c2d1e0f9093.wav"}
          }
        ]
      }
    ]
  },
  "parameters": {
    "format": "wav",
    "sample_rate": "16000"
  }
}'
```

<a id="code-block-2"></a>

```json
{
  "output": {
    "sentence": {
      "sentence_id": 1,
      "begin_time": 120,
      "end_time": 6228,
      "text": "请把漆园项目的报告发给罗科，下周我们要上线悬枢系统。",
      "channel_id": 0,
      "sentence_end": true,
      "words": [
        {"begin_time": 120, "end_time": 600, "text": "请把", "punctuation": "", "fixed": true, "speaker_id": null},
        {"begin_time": 600, "end_time": 840, "text": "漆", "punctuation": "", "fixed": true, "speaker_id": null},
        {"begin_time": 840, "end_time": 1160, "text": "园", "punctuation": "", "fixed": true, "speaker_id": null},
        {"begin_time": 1160, "end_time": 1680, "text": "项目的", "punctuation": "", "fixed": true, "speaker_id": null},
        {"begin_time": 1680, "end_time": 2160, "text": "报告", "punctuation": "", "fixed": true, "speaker_id": null},
        {"begin_time": 2160, "end_time": 2600, "text": "发给", "punctuation": "", "fixed": true, "speaker_id": null},
        {"begin_time": 2600, "end_time": 2840, "text": "罗", "punctuation": "", "fixed": true, "speaker_id": null},
        {"begin_time": 2840, "end_time": 3480, "text": "科", "punctuation": "，", "fixed": true, "speaker_id": null},
        {"begin_time": 3480, "end_time": 4000, "text": "下周", "punctuation": "", "fixed": true, "speaker_id": null},
        {"begin_time": 4000, "end_time": 4520, "text": "我们要", "punctuation": "", "fixed": true, "speaker_id": null},
        {"begin_time": 4520, "end_time": 5160, "text": "上线", "punctuation": "", "fixed": true, "speaker_id": null},
        {"begin_time": 5160, "end_time": 5360, "text": "悬", "punctuation": "", "fixed": true, "speaker_id": null},
        {"begin_time": 5360, "end_time": 5680, "text": "枢", "punctuation": "", "fixed": true, "speaker_id": null},
        {"begin_time": 5680, "end_time": 5880, "text": "系", "punctuation": "", "fixed": true, "speaker_id": null},
        {"begin_time": 5880, "end_time": 6228, "text": "统", "punctuation": "。", "fixed": true, "speaker_id": null}
      ]
    },
    "text": "请把漆园项目的报告发给罗科，下周我们要上线悬枢系统。"
  },
  "usage": {
    "duration": 6,
    "input_tokens": 78,
    "output_tokens": 16,
    "total_tokens": 94
  },
  "request_id": "2e7a1ccb-766b-9d21-b2e4-762b52bdabab"
}
```

<a id="流式-sse"></a>

<a id="流式-sse-h4"></a>

#### 流式（SSE）

<a id="code-block-3"></a>

```bash
curl --no-buffer "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -H "X-DashScope-SSE: enable" \
  --data '{
  "model": "qwen-audio-3.1-asr-flash",
  "input": {
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "input_audio",
            "input_audio": {"data": "https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/zh/audios/6a4b3c2d1e0f9093.wav"}
          }
        ]
      }
    ]
  },
  "parameters": {
    "format": "wav",
    "sample_rate": "16000"
  }
}'
```

<a id="code-block-4"></a>

```text
data:{"output":{"sentence":{"sentence_id":1,"begin_time":120,"end_time":null,"text":"请把漆园项目的报告发给罗科，下周我们要上线玄枢","channel_id":0,"sentence_end":false,"words":[{"begin_time":120,"end_time":600,"text":"请把","punctuation":"","fixed":false,"speaker_id":null},{"begin_time":600,"end_time":840,"text":"漆","punctuation":"","fixed":false,"speaker_id":null},{"begin_time":840,"end_time":1160,"text":"园","punctuation":"","fixed":false,"speaker_id":null},{"begin_time":1160,"end_time":1680,"text":"项目的","punctuation":"","fixed":false,"speaker_id":null},{"begin_time":1680,"end_time":2160,"text":"报告","punctuation":"","fixed":false,"speaker_id":null},{"begin_time":2160,"end_time":2600,"text":"发给","punctuation":"","fixed":false,"speaker_id":null},{"begin_time":2600,"end_time":2840,"text":"罗","punctuation":"","fixed":false,"speaker_id":null},{"begin_time":2840,"end_time":3480,"text":"科","punctuation":"，","fixed":false,"speaker_id":null},{"begin_time":3480,"end_time":4000,"text":"下周","punctuation":"","fixed":false,"speaker_id":null},{"begin_time":4000,"end_time":4520,"text":"我们要","punctuation":"","fixed":false,"speaker_id":null},{"begin_time":4520,"end_time":5160,"text":"上线","punctuation":"","fixed":false,"speaker_id":null},{"begin_time":5160,"end_time":5360,"text":"玄","punctuation":"","fixed":false,"speaker_id":null},{"begin_time":5360,"end_time":5680,"text":"枢","punctuation":"","fixed":false,"speaker_id":null}]},"text":"请把漆园项目的报告发给罗科，下周我们要上线玄枢"},"request_id":"72ab1a19-770d-90bb-87d5-013aa67cdf5d"}

data:{"output":{"sentence":{"sentence_id":1,"begin_time":120,"end_time":6228,"text":"请把漆园项目的报告发给罗科，下周我们要上线玄枢系统。","channel_id":0,"sentence_end":true,"words":[{"begin_time":120,"end_time":600,"text":"请把","punctuation":"","fixed":true,"speaker_id":null},{"begin_time":600,"end_time":840,"text":"漆","punctuation":"","fixed":true,"speaker_id":null},{"begin_time":840,"end_time":1160,"text":"园","punctuation":"","fixed":true,"speaker_id":null},{"begin_time":1160,"end_time":1680,"text":"项目的","punctuation":"","fixed":true,"speaker_id":null},{"begin_time":1680,"end_time":2160,"text":"报告","punctuation":"","fixed":true,"speaker_id":null},{"begin_time":2160,"end_time":2600,"text":"发给","punctuation":"","fixed":true,"speaker_id":null},{"begin_time":2600,"end_time":2840,"text":"罗","punctuation":"","fixed":true,"speaker_id":null},{"begin_time":2840,"end_time":3480,"text":"科","punctuation":"，","fixed":true,"speaker_id":null},{"begin_time":3480,"end_time":4000,"text":"下周","punctuation":"","fixed":true,"speaker_id":null},{"begin_time":4000,"end_time":4520,"text":"我们要","punctuation":"","fixed":true,"speaker_id":null},{"begin_time":4520,"end_time":5160,"text":"上线","punctuation":"","fixed":true,"speaker_id":null},{"begin_time":5160,"end_time":5360,"text":"玄","punctuation":"","fixed":true,"speaker_id":null},{"begin_time":5360,"end_time":5680,"text":"枢","punctuation":"","fixed":true,"speaker_id":null},{"begin_time":5680,"end_time":5880,"text":"系","punctuation":"","fixed":true,"speaker_id":null},{"begin_time":5880,"end_time":6228,"text":"统","punctuation":"。","fixed":true,"speaker_id":null}]},"text":"请把漆园项目的报告发给罗科，下周我们要上线玄枢系统。"},"usage":{"duration":6,"input_tokens":78,"output_tokens":16,"total_tokens":94},"request_id":"72ab1a19-770d-90bb-87d5-013aa67cdf5d"}
```

<a id="携带上下文"></a>

<a id="携带上下文-h4"></a>

#### 携带上下文

<a id="code-block-5"></a>

```bash
curl "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -H "X-DashScope-SSE: disable" \
  --data '{
  "model": "qwen-audio-3.1-asr-flash",
  "input": {
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "input_text",
            "text": "祺元项目、洛柯、璇枢系统。"
          }
        ]
      },
      {
        "role": "assistant",
        "content": [
          {
            "type": "text",
            "text": "已记录这些项目和人名。"
          }
        ]
      },
      {
        "role": "user",
        "content": [
          {
            "type": "input_audio",
            "input_audio": {"data": "https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/zh/audios/6a4b3c2d1e0f9093.wav"}
          }
        ]
      }
    ]
  },
  "parameters": {
    "format": "wav",
    "sample_rate": "16000"
  }
}'
```

<a id="code-block-6"></a>

```json
{
  "output": {
    "sentence": {
      "sentence_id": 1,
      "begin_time": 120,
      "end_time": 6228,
      "text": "请把祺元项目的报告发给洛柯，下周我们要上线璇枢系统。",
      "channel_id": 0,
      "sentence_end": true,
      "words": [
        {"begin_time": 120, "end_time": 600, "text": "请把", "punctuation": "", "fixed": true, "speaker_id": null},
        {"begin_time": 600, "end_time": 840, "text": "祺", "punctuation": "", "fixed": true, "speaker_id": null},
        {"begin_time": 840, "end_time": 1160, "text": "元", "punctuation": "", "fixed": true, "speaker_id": null},
        {"begin_time": 1160, "end_time": 1680, "text": "项目的", "punctuation": "", "fixed": true, "speaker_id": null},
        {"begin_time": 1680, "end_time": 2160, "text": "报告", "punctuation": "", "fixed": true, "speaker_id": null},
        {"begin_time": 2160, "end_time": 2600, "text": "发给", "punctuation": "", "fixed": true, "speaker_id": null},
        {"begin_time": 2600, "end_time": 2840, "text": "洛", "punctuation": "", "fixed": true, "speaker_id": null},
        {"begin_time": 2840, "end_time": 3480, "text": "柯", "punctuation": "，", "fixed": true, "speaker_id": null},
        {"begin_time": 3480, "end_time": 4000, "text": "下周", "punctuation": "", "fixed": true, "speaker_id": null},
        {"begin_time": 4000, "end_time": 4520, "text": "我们要", "punctuation": "", "fixed": true, "speaker_id": null},
        {"begin_time": 4520, "end_time": 5160, "text": "上线", "punctuation": "", "fixed": true, "speaker_id": null},
        {"begin_time": 5160, "end_time": 5360, "text": "璇", "punctuation": "", "fixed": true, "speaker_id": null},
        {"begin_time": 5360, "end_time": 5680, "text": "枢", "punctuation": "", "fixed": true, "speaker_id": null},
        {"begin_time": 5680, "end_time": 5880, "text": "系", "punctuation": "", "fixed": true, "speaker_id": null},
        {"begin_time": 5880, "end_time": 6228, "text": "统", "punctuation": "。", "fixed": true, "speaker_id": null}
      ]
    },
    "text": "请把祺元项目的报告发给洛柯，下周我们要上线璇枢系统。"
  },
  "usage": {
    "duration": 6,
    "input_tokens": 100,
    "output_tokens": 16,
    "total_tokens": 116
  },
  "request_id": "062cc295-fa5d-92dd-a3ec-5d56d34a4e1e"
}
```

<a id="说话人分离"></a>

<a id="说话人分离-h4"></a>

#### 说话人分离

<a id="code-block-7"></a>

```bash
curl "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -H "X-DashScope-SSE: disable" \
  --data '{
  "model": "qwen-audio-3.1-asr-flash",
  "input": {
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "input_audio",
            "input_audio": {"data": "https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/zh/audios/6a4b3c2d1e0f9093.wav"}
          }
        ]
      }
    ]
  },
  "parameters": {
    "format": "wav",
    "sample_rate": "16000",
    "speaker_diarization_enabled": true
  }
}'
```

<a id="code-block-8"></a>

```json
{
  "output": {
    "sentence": {
      "sentence_id": 1,
      "begin_time": 0,
      "end_time": 6160,
      "text": "请把漆园项目的报告发给罗科，下周我们要上线玄枢系统。",
      "channel_id": 0,
      "speaker_id": 0,
      "sentence_end": true,
      "words": [
        {"begin_time": 0, "end_time": 473, "text": "请把", "punctuation": "", "fixed": true, "speaker_id": 0},
        {"begin_time": 473, "end_time": 710, "text": "漆", "punctuation": "", "fixed": true, "speaker_id": 0},
        {"begin_time": 710, "end_time": 947, "text": "园", "punctuation": "", "fixed": true, "speaker_id": 0},
        {"begin_time": 947, "end_time": 1658, "text": "项目的", "punctuation": "", "fixed": true, "speaker_id": 0},
        {"begin_time": 1658, "end_time": 2132, "text": "报告", "punctuation": "", "fixed": true, "speaker_id": 0},
        {"begin_time": 2132, "end_time": 2606, "text": "发给", "punctuation": "", "fixed": true, "speaker_id": 0},
        {"begin_time": 2606, "end_time": 2843, "text": "罗", "punctuation": "", "fixed": true, "speaker_id": 0},
        {"begin_time": 2843, "end_time": 3316, "text": "科", "punctuation": "，", "fixed": true, "speaker_id": 0},
        {"begin_time": 3316, "end_time": 3790, "text": "下周", "punctuation": "", "fixed": true, "speaker_id": 0},
        {"begin_time": 3790, "end_time": 4501, "text": "我们要", "punctuation": "", "fixed": true, "speaker_id": 0},
        {"begin_time": 4501, "end_time": 4975, "text": "上线", "punctuation": "", "fixed": true, "speaker_id": 0},
        {"begin_time": 4975, "end_time": 5212, "text": "玄", "punctuation": "", "fixed": true, "speaker_id": 0},
        {"begin_time": 5212, "end_time": 5449, "text": "枢", "punctuation": "", "fixed": true, "speaker_id": 0},
        {"begin_time": 5449, "end_time": 5686, "text": "系", "punctuation": "", "fixed": true, "speaker_id": 0},
        {"begin_time": 5686, "end_time": 6160, "text": "统", "punctuation": "。", "fixed": true, "speaker_id": 0}
      ]
    },
    "text": "请把漆园项目的报告发给罗科，下周我们要上线玄枢系统。",
    "sentences": [
      {
        "sentence_id": 1,
        "begin_time": 0,
        "end_time": 6160,
        "text": "请把漆园项目的报告发给罗科，下周我们要上线玄枢系统。",
        "channel_id": 0,
        "speaker_id": 0,
        "sentence_end": true,
        "words": [
          {"begin_time": 0, "end_time": 473, "text": "请把", "punctuation": "", "fixed": true, "speaker_id": 0},
          {"begin_time": 473, "end_time": 710, "text": "漆", "punctuation": "", "fixed": true, "speaker_id": 0},
          {"begin_time": 710, "end_time": 947, "text": "园", "punctuation": "", "fixed": true, "speaker_id": 0},
          {"begin_time": 947, "end_time": 1658, "text": "项目的", "punctuation": "", "fixed": true, "speaker_id": 0},
          {"begin_time": 1658, "end_time": 2132, "text": "报告", "punctuation": "", "fixed": true, "speaker_id": 0},
          {"begin_time": 2132, "end_time": 2606, "text": "发给", "punctuation": "", "fixed": true, "speaker_id": 0},
          {"begin_time": 2606, "end_time": 2843, "text": "罗", "punctuation": "", "fixed": true, "speaker_id": 0},
          {"begin_time": 2843, "end_time": 3316, "text": "科", "punctuation": "，", "fixed": true, "speaker_id": 0},
          {"begin_time": 3316, "end_time": 3790, "text": "下周", "punctuation": "", "fixed": true, "speaker_id": 0},
          {"begin_time": 3790, "end_time": 4501, "text": "我们要", "punctuation": "", "fixed": true, "speaker_id": 0},
          {"begin_time": 4501, "end_time": 4975, "text": "上线", "punctuation": "", "fixed": true, "speaker_id": 0},
          {"begin_time": 4975, "end_time": 5212, "text": "玄", "punctuation": "", "fixed": true, "speaker_id": 0},
          {"begin_time": 5212, "end_time": 5449, "text": "枢", "punctuation": "", "fixed": true, "speaker_id": 0},
          {"begin_time": 5449, "end_time": 5686, "text": "系", "punctuation": "", "fixed": true, "speaker_id": 0},
          {"begin_time": 5686, "end_time": 6160, "text": "统", "punctuation": "。", "fixed": true, "speaker_id": 0}
        ]
      }
    ]
  },
  "usage": {
    "duration": 6,
    "input_tokens": 78,
    "output_tokens": 31,
    "total_tokens": 109
  },
  "request_id": "f224bd86-52f0-95b3-96ca-a58889f08d1f"
}
```
