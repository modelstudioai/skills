# 非实时语音识别（Qwen-Audio-ASR）HTTP API

本文介绍Qwen-Audio-ASR非实时语音识别HTTP API的参数和接口细节。

关于支持的音频格式、文件大小限制、时长限制等输入要求，请参见[音频规格](../model-user-guide/model-experience/speech-and-audio/speech-recognition/asr-model.md#asr_audio_spec02)。

<a id="接口地址"></a>

<a id="h-fl-url"></a>

## 接口地址

<a id="sec-tabs"></a>

<a id="华北2-北京"></a>

<a id="华北2-北京-h4"></a>

#### 华北2（北京）

`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="新加坡"></a>

<a id="新加坡-h4"></a>

#### 新加坡

`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

> **重要**
>
> 阿里云百炼为华北2（北京）、新加坡地域推出了业务空间专属域名，能够为推理请求提供卓越的性能和更高的稳定性，建议迁移至新域名：
>
> -   华北2（北京）地域：从 `dashscope.aliyuncs.com` 迁移至 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
> -   新加坡地域：从 `dashscope-intl.aliyuncs.com` 迁移至 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`

<a id="请求头"></a>

<a id="h-fl-hd"></a>

## 请求头

| 参数 | 类型 | 是否必选 | 说明 |
| --- | --- | --- | --- |
| `Authorization` | `string` | 是 | 鉴权令牌，格式为`Bearer <your_api_key>`，使用时将"`<your_api_key>`"替换为实际的API Key。 |
| `Content-Type` | `string` | 是 | 请求参数的媒体类型，固定为`application/json`。 |
| `X-DashScope-SSE` | `string` | 否 | 用于控制是否请求流式返回。设置为 `enable` 时请求 SSE 流式返回；设置为 `disable` 或不传该参数则仅返回最终结果。<br><br>> **说明**<br>><br>> 仅适用于 `qwen-audio-3.0-asr-flash`：音频时长不少于 1 分钟时才以 SSE 流式方式返回结果。 |

<table><tbody><tr><td><a id="h-fl-rq"></a><h2>请求参数</h2><p><strong>model</strong><code>string</code><strong>（必选）</strong></p><p>模型名称。</p><p><strong>input</strong><code>object</code><strong>（必选）</strong></p><p>输入信息。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>messages</strong><code>array(object)</code><strong>（必选）</strong></p><p>消息列表。包含当前待识别的音频，以及可选的对话上下文（用于提升识别效果）。</p><div><div><p><strong>重要</strong>上下文功能用于提升专有词汇的识别准确率，使用方法详见<a href="../model-user-guide/model-experience/speech-and-audio/speech-recognition/improve-asr-accuracy.md#ctx_enhance_h2">上下文增强</a>。</p><p>上下文消息（<code>input_text</code> 和 <code>text</code> 类型）各最多 5 条，超出时保留最近的 5 条。每轮上下文文本总长度（<code>user</code> 和 <code>assistant</code> 的 <code>text</code> 字段长度之和）不超过 400 个字符（按字符数计算，每个字符计为 1），超出部分从末尾截断。</p></div></div><div><div><p><strong>重要</strong>携带上下文时，<code>messages</code> 中的消息顺序有要求：上下文消息必须按对话轮次排列，每轮中 <code>user</code>（<code>input_text</code> 类型）必须在对应的 <code>assistant</code>（<code>text</code> 类型）之前；包含 <code>input_audio</code> 的 <code>user</code> 消息必须放在 <code>messages</code> 数组的最后。</p></div></div><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>role</strong><code>string</code><strong>（必选）</strong></p><p>消息角色。取值范围：</p><ul><li><code>user</code>（必选）：用户消息。type为<code>input_audio</code>时表示当前待识别的音频；type为<code>input_text</code>时表示前几轮的识别结果或领域相关的词表（可选，上下文）。</li><li><code>assistant</code>（可选，上下文）：前几轮大语言模型的回复内容。</li></ul><p><strong>content</strong><code>array(object)</code><strong>（必选）</strong></p><p>消息内容列表。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>type</strong><code>string</code><strong>（必选）</strong></p><p>内容类型。每个请求至少需要一条<code>input_audio</code>类型的消息。取值范围：</p><ul><li><code>input_audio</code>（必选）：当前待识别的音频输入（role为user），需同时传入<code>input_audio</code>对象。</li><li><code>input_text</code>（可选，上下文）：前几轮用户语音的识别结果或领域相关的词表（role为user），需同时传入<code>text</code>字段。</li><li><code>text</code>（可选，上下文）：前几轮大语言模型的回复内容（role为assistant），需同时传入<code>text</code>字段。</li></ul><p><strong>input_audio</strong><code>object</code><strong>（条件必选）</strong></p><p>当<code>type</code>为<code>input_audio</code>时必填。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>data</strong><code>string</code><strong>（必选）</strong></p><p>待识别音频数据。关于支持的音频格式、文件大小限制、时长限制等输入要求，请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-recognition/asr-model.md#asr_audio_spec02">音频规格</a>。支持以下两种方式：</p><ul><li><strong>音频文件URL</strong>：直接传入可公开访问的音频文件地址。</li><li><strong>Base64 Data URI</strong>：采用Data URI格式传入Base64编码的音频数据，值由<code>data:{MIME_TYPE};base64,</code>前缀与Base64编码的音频数据拼接而成。支持的MIME类型包括<code>audio/wav</code>、<code>audio/mp3</code>等。</li></ul><p>示例（URL方式）：<code>https://example.com/audio/sample.wav</code></p><p>示例（Base64方式）：<code>data:audio/wav;base64,{BASE64_ENCODED_DATA}</code></p></div></section><p><strong>text</strong><code>string</code><strong>（条件必选）</strong></p><p>当<code>type</code>为<code>input_text</code>时，填入前几轮用户语音的识别结果或领域相关的词表；当<code>type</code>为<code>text</code>时，填入前几轮大语言模型的回复内容。文本按字符数计算，每个字符计为 1。每轮上下文中所有消息的 <code>text</code> 字段长度之和不超过 400 个字符，超出部分从末尾截断。</p></div></section></div></section></div></section><p><strong>parameters</strong><code>object</code><strong>（必选）</strong></p><p>模型参数。</p><div><div><p><strong>说明</strong><code>qwen-audio-3.0-asr-flash</code> 的润色顺滑功能默认关闭，暂未开放。<code>qwen-audio-3.1-asr-flash</code> 支持原生文本润色。</p><p>润色顺滑：模型在识别语音的同时，自动清理无意义语气词和口吃重复，处理说话过程中的自我纠正，理顺口语表达，并规范标点与文本格式。输出结果更加简洁、流畅、易读，同时尽可能保留用户的最终意图和关键信息。</p></div></div><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>speaker_diarization_enabled</strong> <code>boolean</code> （可选）</p><div><div><p><strong>说明</strong>仅适用于 <code>qwen-audio-3.1-asr-flash</code>。</p></div></div><p>是否启用说话人分离，默认值为 <code>false</code>。设为 <code>true</code> 时，通过响应中的 <code>speaker_id</code> 区分说话人，并返回 <code>output.sentences</code>。开启后，<code>keep_dialect</code> 和 <code>language_hints</code> 不生效。</p><p><strong>keep_dialect</strong> <code>boolean</code> （可选）</p><div><div><p><strong>说明</strong>仅适用于 <code>qwen-audio-3.1-asr-flash</code>。</p></div></div><p>是否保留方言表达，默认值为 <code>false</code>。<code>false</code>：将方言转写为普通话文本；<code>true</code>：保留方言表达。</p><p><strong>format</strong><code>string</code><strong>（必选）</strong></p><p>音频格式。根据实际音频格式填写，支持<code>wav</code>、<code>mp3</code>、<code>opus</code>等。详情请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-recognition/asr-model.md#asr_audio_spec02">音频规格</a>。</p><p><strong>sample_rate</strong><code>string</code>（可选）</p><p>音频采样率，单位Hz。例如<code>16000</code>表示16kHz采样率。详情请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-recognition/asr-model.md#asr_audio_spec02">音频规格</a>。</p><p><strong>vocabulary_id</strong><code>string</code>（可选）</p><p>预编译热词列表 ID。</p><p>需预先调用创建热词列表接口生成，识别时传入该 ID 即可使用列表中的热词。</p><p>适用于词汇已知且相对稳定、需要跨请求复用同一词表的场景。</p><p>使用方法请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-recognition/improve-asr-accuracy.md#hw_precompiled_h3">预编译热词</a>。</p><p><strong>vocabulary</strong><code>object</code>（可选）</p><p>即时热词。</p><p>以键值对形式传入，键为热词文本（<code>string</code>），值为热词权重（<code>integer</code>），无需预先创建热词列表。权重取值范围为 [1, 5] 或 50：取 [1, 5] 时值越大模型越倾向输出该词；取 50 时为超级热词，召回率大幅提升，但超级热词数量最多不超过 50 个。</p><p>适用于临时性、会话级别的热词优化。</p><p>与预编译热词同时配置时，系统会合并两类热词；合并后超过 2000 个时，随机选择 2000 个使用。使用方法请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-recognition/improve-asr-accuracy.md#hw_instant_h3">即时热词</a>。</p><p><strong>language_hints</strong> <code>array[string]</code>（可选）</p><p>设置待识别语言代码。如果无法提前确定语种，可不设置，模型会自动识别语种。最多支持设置 4 个值，超出时仅前 4 个生效。</p><p>指定语种代码可提升识别准确率。</p><a id="accordion-支持的语言代码"></a><section><p>支持的语言代码</p><div><ul><li>zh: 中文</li><li>en: 英文</li><li>ja: 日语</li><li>ko: 韩语</li><li>vi: 越南语</li><li>th: 泰语</li><li>id: 印尼语</li><li>ms: 马来语</li><li>tl: 菲律宾语</li><li>hi: 印地语</li><li>ar: 阿拉伯语</li><li>fr: 法语</li><li>de: 德语</li><li>es: 西班牙语</li><li>pt: 葡萄牙语</li><li>ru: 俄语</li><li>it: 意大利语</li><li>nl: 荷兰语</li><li>sv: 瑞典语</li><li>da: 丹麦语</li><li>fi: 芬兰语</li><li>no: 挪威语</li><li>el: 希腊语</li><li>pl: 波兰语</li><li>cs: 捷克语</li><li>hu: 匈牙利语</li><li>ro: 罗马尼亚语</li><li>bg: 保加利亚语</li><li>hr: 克罗地亚语</li><li>sk: 斯洛伐克语</li></ul><p><code>qwen-audio-3.1-asr-flash</code> 还支持以下语言代码：</p><ul><li>tr: 土耳其语</li><li>fa: 波斯语</li><li>mr: 马拉地语</li><li>ml: 马拉雅拉姆语</li><li>ne: 尼泊尔语</li><li>ky: 吉尔吉斯语</li><li>az: 阿塞拜疆语</li><li>ka: 格鲁吉亚语</li><li>hy: 亚美尼亚语</li><li>sl: 斯洛文尼亚语</li><li>sq: 阿尔巴尼亚语</li><li>et: 爱沙尼亚语</li><li>lv: 拉脱维亚语</li><li>lt: 立陶宛语</li><li>ca: 加泰罗尼亚语</li><li>eu: 巴斯克语</li><li>gl: 加利西亚语</li><li>or: 奥里亚语</li><li>dv: 迪维希语</li><li>as: 阿萨姆语</li><li>kmr: 北库尔德语</li><li>tig: 提格雷语</li><li>fy: 西弗里西亚语</li><li>ba: 巴什基尔语</li><li>be: 白俄罗斯语</li><li>tt: 鞑靼语</li><li>ia: 国际语</li><li>mhr: 草原马里语</li><li>tok: 道本语</li></ul></div></section></div></section></td><td><p>以下为华北2（北京）地域的配置，调用时请将&quot;{WorkspaceId}&quot;替换为真实的业务空间ID，各地域的配置不同。</p><a id="sec-tabs-2"></a><section><a id="非流式"></a><section><a id="非流式-h4"></a><h4>非流式</h4><a id="code-block"></a><pre class="language-bash"><code>curl --location --request POST 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
     --header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
     --header &quot;Content-Type: application/json&quot; \
     --header &quot;X-DashScope-SSE: disable&quot; \
     --data '{
    &quot;model&quot;: &quot;qwen-audio-3.1-asr-flash&quot;,
    &quot;input&quot;: {
        &quot;messages&quot;: [
            {
                &quot;role&quot;: &quot;user&quot;,
                &quot;content&quot;: [
                    {
                        &quot;type&quot;: &quot;input_audio&quot;,
                        &quot;input_audio&quot;: {
                            &quot;data&quot;: &quot;{YOUR_AUDIO_URL}&quot;
                        }
                    }
                ]
            }
        ]
    },
    &quot;parameters&quot;: {
        &quot;format&quot;: &quot;wav&quot;,
        &quot;sample_rate&quot;: &quot;16000&quot;
    }
}'
</code></pre></section><a id="流式"></a><section><a id="流式-h4"></a><h4>流式</h4><a id="code-block-2"></a><pre class="language-bash"><code>curl --location --request POST 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
     --header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
     --header &quot;Content-Type: application/json&quot; \
     --header &quot;X-DashScope-SSE: enable&quot; \
     --data '{
    &quot;model&quot;: &quot;qwen-audio-3.1-asr-flash&quot;,
    &quot;input&quot;: {
        &quot;messages&quot;: [
            {
                &quot;role&quot;: &quot;user&quot;,
                &quot;content&quot;: [
                    {
                        &quot;type&quot;: &quot;input_audio&quot;,
                        &quot;input_audio&quot;: {
                            &quot;data&quot;: &quot;{YOUR_AUDIO_URL}&quot;
                        }
                    }
                ]
            }
        ]
    },
    &quot;parameters&quot;: {
        &quot;format&quot;: &quot;wav&quot;,
        &quot;sample_rate&quot;: &quot;16000&quot;
    }
}'
</code></pre></section><a id="携带上下文-非流式"></a><section><a id="携带上下文-非流式-h4"></a><h4>携带上下文-非流式</h4><a id="code-block-3"></a><pre class="language-bash"><code>curl --location --request POST 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
     --header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
     --header &quot;Content-Type: application/json&quot; \
     --header &quot;X-DashScope-SSE: disable&quot; \
     --data '{
    &quot;model&quot;: &quot;qwen-audio-3.1-asr-flash&quot;,
    &quot;input&quot;: {
        &quot;messages&quot;: [
            {
                &quot;role&quot;: &quot;user&quot;,
                &quot;content&quot;: [
                    {
                        &quot;type&quot;: &quot;input_text&quot;,
                        &quot;text&quot;: &quot;你好啊&quot;
                    }
                ]
            },
            {
                &quot;role&quot;: &quot;assistant&quot;,
                &quot;content&quot;: [
                    {
                        &quot;type&quot;: &quot;text&quot;,
                        &quot;text&quot;: &quot;你好啊，我是通义千问，有什么可以帮助你的？&quot;
                    }
                ]
            },
            {
                &quot;role&quot;: &quot;user&quot;,
                &quot;content&quot;: [
                    {
                        &quot;type&quot;: &quot;input_audio&quot;,
                        &quot;input_audio&quot;: {
                            &quot;data&quot;: &quot;{YOUR_AUDIO_URL}&quot;
                        }
                    }
                ]
            }
        ]
    },
    &quot;parameters&quot;: {
        &quot;format&quot;: &quot;wav&quot;,
        &quot;sample_rate&quot;: &quot;16000&quot;
    }
}'
</code></pre></section><a id="携带上下文-流式"></a><section><a id="携带上下文-流式-h4"></a><h4>携带上下文-流式</h4><a id="code-block-4"></a><pre class="language-bash"><code>curl --location --request POST 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
     --header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
     --header &quot;Content-Type: application/json&quot; \
     --header &quot;X-DashScope-SSE: enable&quot; \
     --data '{
    &quot;model&quot;: &quot;qwen-audio-3.1-asr-flash&quot;,
    &quot;input&quot;: {
        &quot;messages&quot;: [
            {
                &quot;role&quot;: &quot;user&quot;,
                &quot;content&quot;: [
                    {
                        &quot;type&quot;: &quot;input_text&quot;,
                        &quot;text&quot;: &quot;你好啊&quot;
                    }
                ]
            },
            {
                &quot;role&quot;: &quot;assistant&quot;,
                &quot;content&quot;: [
                    {
                        &quot;type&quot;: &quot;text&quot;,
                        &quot;text&quot;: &quot;你好啊，我是通义千问，有什么可以帮助你的？&quot;
                    }
                ]
            },
            {
                &quot;role&quot;: &quot;user&quot;,
                &quot;content&quot;: [
                    {
                        &quot;type&quot;: &quot;input_audio&quot;,
                        &quot;input_audio&quot;: {
                            &quot;data&quot;: &quot;{YOUR_AUDIO_URL}&quot;
                        }
                    }
                ]
            }
        ]
    },
    &quot;parameters&quot;: {
        &quot;format&quot;: &quot;wav&quot;,
        &quot;sample_rate&quot;: &quot;16000&quot;
    }
}'
</code></pre></section><a id="base64"></a><section><a id="base64-h4"></a><h4>Base64</h4><p>可输入Base64编码数据（<a href="https://www.rfc-editor.org/rfc/rfc2397">Data URL</a>），格式为：<code>data:&lt;mediatype&gt;;base64,&lt;data&gt;</code>。</p><ul><li><p><code>&lt;mediatype&gt;</code>：MIME类型</p><p>因音频格式而异，例如：</p><ul><li>WAV：<code>audio/wav</code></li><li>MP3：<code>audio/mpeg</code></li></ul></li><li><p><code>&lt;data&gt;</code>：音频转成的Base64编码的字符串</p><p>Base64 编码会增大数据体积，音频文件的大小和时长限制请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-recognition/asr-model.md#asr_audio_spec02">音频规格</a>。</p></li><li><p>示例：<code>data:audio/wav;base64,SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU4LjI5LjEwMAAAAAAAAAAAAAAA//PAxABQ/BXRbMPe4IQAhl9</code></p><a id="fig-code-group"></a><div><a id="fig-code-group-python-tab"></a>python<div><a id="code-code-group-python"></a><pre class="language-python"><code>import base64, pathlib

# 请替换为自己的音频文件路径，确保其符合音频要求
file_path = pathlib.Path(&quot;{YOUR_AUDIO_FILE}&quot;)
base64_str = base64.b64encode(file_path.read_bytes()).decode()
data_uri = f&quot;data:audio/mpeg;base64,{base64_str}&quot;
</code></pre></div><a id="fig-code-group-java-tab"></a>java<div><a id="code-code-group-java"></a><pre class="language-java"><code>import java.nio.file.*;
import java.util.Base64;

public class Main {
    /**
     * 请替换为自己的音频文件路径，确保其符合音频要求
     */
    public static String toDataUrl(String filePath) throws Exception {
        byte[] bytes = Files.readAllBytes(Paths.get(filePath));
        String encoded = Base64.getEncoder().encodeToString(bytes);
        return &quot;data:audio/mpeg;base64,&quot; + encoded;
    }

    public static void main(String[] args) throws Exception {
        System.out.println(toDataUrl(&quot;{YOUR_AUDIO_FILE}&quot;));
    }
}
</code></pre></div></div></li></ul><a id="code-block-5"></a><pre class="language-python"><code>import base64, pathlib
import os
import requests

# 请替换为自己的音频文件路径，确保其符合音频要求
file_path = pathlib.Path(&quot;{YOUR_AUDIO_FILE}&quot;)
base64_str = base64.b64encode(file_path.read_bytes()).decode()
data_uri = f&quot;data:audio/wav;base64,{base64_str}&quot;

url = &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation&quot;

headers = {
    &quot;Authorization&quot;: f&quot;Bearer {os.environ['DASHSCOPE_API_KEY']}&quot;,
    &quot;Content-Type&quot;: &quot;application/json&quot;,
    &quot;X-DashScope-SSE&quot;: &quot;disable&quot;,
}

payload = {
    &quot;model&quot;: &quot;qwen-audio-3.1-asr-flash&quot;,
    &quot;input&quot;: {
        &quot;messages&quot;: [
            {
                &quot;role&quot;: &quot;user&quot;,
                &quot;content&quot;: [
                    {
                        &quot;type&quot;: &quot;input_audio&quot;,
                        &quot;input_audio&quot;: {
                            &quot;data&quot;: data_uri,
                        },
                    }
                ],
            }
        ]
    },
    &quot;parameters&quot;: {
        &quot;format&quot;: &quot;wav&quot;,
        &quot;sample_rate&quot;: &quot;16000&quot;,
    },
}

response = requests.post(url, headers=headers, json=payload)
print(response.status_code)
print(response.json())
</code></pre></section><a id="即时热词"></a><section><a id="即时热词-h4"></a><h4>即时热词</h4><a id="code-block-6"></a><pre class="language-bash"><code>curl --location --request POST 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
     --header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
     --header &quot;Content-Type: application/json&quot; \
     --header &quot;X-DashScope-SSE: disable&quot; \
     --data '{
    &quot;model&quot;: &quot;qwen-audio-3.1-asr-flash&quot;,
    &quot;input&quot;: {
        &quot;messages&quot;: [
            {
                &quot;role&quot;: &quot;user&quot;,
                &quot;content&quot;: [
                    {
                        &quot;type&quot;: &quot;input_audio&quot;,
                        &quot;input_audio&quot;: {
                            &quot;data&quot;: &quot;{YOUR_AUDIO_URL}&quot;
                        }
                    }
                ]
            }
        ]
    },
    &quot;parameters&quot;: {
        &quot;format&quot;: &quot;wav&quot;,
        &quot;sample_rate&quot;: &quot;16000&quot;,
        &quot;vocabulary&quot;: {&quot;张三&quot;: 5, &quot;李四&quot;: 5}
    }
}'
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-fl-rs"></a><h2>响应参数</h2><p><strong>request_id</strong><code>string</code></p><p>本次请求的唯一标识。</p><p><strong>output</strong><code>object</code></p><p>输出结果。</p><a id="accordion-属性-6"></a><section><p>属性</p><div><p><strong>text</strong><code>string</code></p><p>当前累积的完整识别文本。</p><p><strong>sentences</strong> <code>array[object]</code></p><div><div><p><strong>说明</strong>仅适用于 <code>qwen-audio-3.1-asr-flash</code>。</p></div></div><p>开启说话人分离时返回。包含当前及历史句子的识别结果，每个元素的结构与 <code>sentence</code> 相同。</p><p><strong>sentence</strong><code>object</code></p><p>当前句子的详细信息。</p><a id="accordion-属性-7"></a><section><p>属性</p><div><p><strong>speaker_id</strong> <code>integer | null</code></p><div><div><p><strong>说明</strong>仅适用于 <code>qwen-audio-3.1-asr-flash</code>。</p></div></div><p>说话人编号，用于区分不同说话人。开启说话人分离时返回编号，未开启时为 <code>null</code>。</p><p><strong>sentence_id</strong><code>integer</code></p><p>句子编号，从1开始。</p><p><strong>sentence_end</strong><code>boolean</code></p><p>是否为该句的最终结果。为<code>true</code>时表示该句识别完成。</p><p><strong>begin_time</strong><code>integer</code></p><p>句子开始时间，单位毫秒。</p><p><strong>end_time</strong><code>integer</code></p><p>句子结束时间，单位毫秒。仅在<code>sentence_end</code>为<code>true</code>时返回。</p><p><strong>text</strong><code>string</code></p><p>当前句子的识别文本。</p><p><strong>channel_id</strong><code>integer</code></p><p>声道编号，从0开始。</p><p><strong>words</strong><code>array</code></p><p>词级别时间戳列表。</p><a id="accordion-属性-8"></a><section><p>属性</p><div><p><strong>speaker_id</strong> <code>integer | null</code></p><div><div><p><strong>说明</strong>仅适用于 <code>qwen-audio-3.1-asr-flash</code>。</p></div></div><p>词对应的说话人编号。开启说话人分离时返回编号，未开启时为 <code>null</code>。</p><p><strong>text</strong><code>string</code></p><p>词文本。</p><p><strong>begin_time</strong><code>integer</code></p><p>词开始时间，单位毫秒。</p><p><strong>end_time</strong><code>integer</code></p><p>词结束时间，单位毫秒。</p><p><strong>punctuation</strong><code>string</code></p><p>词后的标点符号。无标点时为空字符串。</p><p><strong>fixed</strong><code>boolean</code></p><p>词是否已稳定。<code>false</code>表示后续事件中该词的时间戳可能调整。</p></div></section></div></section></div></section><p><strong>usage</strong><code>object</code></p><p>用量信息。仅在<code>sentence_end</code>为<code>true</code>时返回。</p><a id="accordion-属性-9"></a><section><p>属性</p><div><p><strong>duration</strong><code>integer</code></p><p>已处理的音频时长，单位秒。</p><p><strong>input_tokens</strong> <code>integer</code></p><div><div><p><strong>说明</strong>仅适用于 <code>qwen-audio-3.1-asr-flash</code>。</p></div></div><p>本次调用消耗的输入 Token 数。</p><p><strong>output_tokens</strong> <code>integer</code></p><div><div><p><strong>说明</strong>仅适用于 <code>qwen-audio-3.1-asr-flash</code>。</p></div></div><p>本次调用消耗的输出 Token 数。</p><p><strong>total_tokens</strong> <code>integer</code></p><div><div><p><strong>说明</strong>仅适用于 <code>qwen-audio-3.1-asr-flash</code>。</p></div></div><p>本次调用消耗的总 Token 数，等于 <code>input_tokens</code> 与 <code>output_tokens</code> 之和。</p></div></section></td><td><a id="sec-tabs-3"></a><section><a id="非流式-2"></a><section><a id="非流式-2-h4"></a><h4>非流式</h4><a id="code-block-7"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
        &quot;sentence&quot;: {
            &quot;begin_time&quot;: 760,
            &quot;channel_id&quot;: 0,
            &quot;end_time&quot;: 3800,
            &quot;sentence_end&quot;: true,
            &quot;sentence_id&quot;: 1,
            &quot;text&quot;: &quot;Hello World，这里是阿里巴巴语音实验室。&quot;,
            &quot;words&quot;: [
                {&quot;begin_time&quot;: 760, &quot;end_time&quot;: 1040, &quot;fixed&quot;: true, &quot;punctuation&quot;: &quot;&quot;, &quot;text&quot;: &quot;Hello&quot;},
                {&quot;begin_time&quot;: 1040, &quot;end_time&quot;: 1240, &quot;fixed&quot;: true, &quot;punctuation&quot;: &quot;，&quot;, &quot;text&quot;: &quot; World&quot;},
                {&quot;begin_time&quot;: 1360, &quot;end_time&quot;: 1880, &quot;fixed&quot;: true, &quot;punctuation&quot;: &quot;&quot;, &quot;text&quot;: &quot;这里是&quot;},
                {&quot;begin_time&quot;: 1880, &quot;end_time&quot;: 2520, &quot;fixed&quot;: true, &quot;punctuation&quot;: &quot;&quot;, &quot;text&quot;: &quot;阿里巴巴&quot;},
                {&quot;begin_time&quot;: 2520, &quot;end_time&quot;: 2840, &quot;fixed&quot;: true, &quot;punctuation&quot;: &quot;&quot;, &quot;text&quot;: &quot;语音&quot;},
                {&quot;begin_time&quot;: 2840, &quot;end_time&quot;: 3800, &quot;fixed&quot;: true, &quot;punctuation&quot;: &quot;。&quot;, &quot;text&quot;: &quot;实验室&quot;}
            ]
        },
        &quot;text&quot;: &quot;Hello World，这里是阿里巴巴语音实验室。&quot;
    },
    &quot;usage&quot;: {
        &quot;duration&quot;: 4
    },
    &quot;request_id&quot;: &quot;40e0734d-096f-9ae3-86c1-a8c013287561&quot;
}
</code></pre></section><a id="流式-2"></a><section><a id="流式-2-h4"></a><h4>流式</h4><p>SSE 流式响应的事件格式如下：</p><a id="code-block-8"></a><pre class="language-text"><code>id:{序列号}
event:result
:HTTP_STATUS/200
data:{JSON数据}
</code></pre><p>返回示例：</p><a id="code-block-9"></a><pre class="language-text"><code>id:1
event:result
:HTTP_STATUS/200
data:{&quot;output&quot;:{&quot;sentence&quot;:{&quot;sentence_id&quot;:1,&quot;sentence_end&quot;:true,&quot;end_time&quot;:3800,&quot;words&quot;:[{&quot;end_time&quot;:1040,&quot;punctuation&quot;:&quot;&quot;,&quot;begin_time&quot;:760,&quot;fixed&quot;:true,&quot;text&quot;:&quot;Hello&quot;},{&quot;end_time&quot;:1240,&quot;punctuation&quot;:&quot;，&quot;,&quot;begin_time&quot;:1040,&quot;fixed&quot;:true,&quot;text&quot;:&quot; World&quot;},{&quot;end_time&quot;:1880,&quot;punctuation&quot;:&quot;&quot;,&quot;begin_time&quot;:1360,&quot;fixed&quot;:true,&quot;text&quot;:&quot;这里是&quot;},{&quot;end_time&quot;:2520,&quot;punctuation&quot;:&quot;&quot;,&quot;begin_time&quot;:1880,&quot;fixed&quot;:true,&quot;text&quot;:&quot;阿里巴巴&quot;},{&quot;end_time&quot;:2840,&quot;punctuation&quot;:&quot;&quot;,&quot;begin_time&quot;:2520,&quot;fixed&quot;:true,&quot;text&quot;:&quot;语音&quot;},{&quot;end_time&quot;:3800,&quot;punctuation&quot;:&quot;。&quot;,&quot;begin_time&quot;:2840,&quot;fixed&quot;:true,&quot;text&quot;:&quot;实验室&quot;}],&quot;begin_time&quot;:760,&quot;text&quot;:&quot;Hello World，这里是阿里巴巴语音实验室。&quot;,&quot;channel_id&quot;:0},&quot;text&quot;:&quot;Hello World，这里是阿里巴巴语音实验室。&quot;},&quot;usage&quot;:{&quot;duration&quot;:4},&quot;request_id&quot;:&quot;fc1582e4-935c-9fc2-a482-a98bf43daa69&quot;}
</code></pre></section></section></td></tr></tbody></table>

<a id="sse-流式结果处理逻辑"></a>

<a id="h-fl-stream-logic"></a>

## SSE 流式结果处理逻辑

在流式模式下，客户端需关注以下处理要点：

1.  每收到一个SSE事件，解析`data`字段中的JSON。
2.  对于 `qwen-audio-3.0-asr-flash`，通过 `output.sentence.sentence_end` 判断当前句子是否结束：当该值为 `true` 时，该句识别完成，词级时间戳已稳定，可作为最终结果使用；当该值为 `false` 时，识别仍在进行中，文本和时间戳可能在后续事件中更新。
3.  `usage` 信息仅在句子结束事件中返回，包含音频处理时长。对于 `qwen-audio-3.1-asr-flash`，还包含本次调用的输入、输出和总 Token 数，该模型按 Token 计费。

对于 `qwen-audio-3.1-asr-flash`，未开启说话人分离时，词级时间戳在 `output.sentence.words[i].fixed` 为 `true` 后才固定；在此之前，时间戳仍可能调整。开启说话人分离时，应读取 `output.sentences` 中当前及历史句子的结果。
