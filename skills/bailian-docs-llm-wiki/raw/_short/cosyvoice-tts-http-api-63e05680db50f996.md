# 非实时语音合成CosyVoice HTTP API参考

本文介绍非实时语音合成CosyVoice的HTTP调用方法，支持非流式和流式两种调用模式。

<a id="接口地址"></a>

<a id="fe508c8badxjg"></a>

## 接口地址

<a id="sec-tabs"></a>

<a id="华北2-北京"></a>

<a id="华北2-北京-h4"></a>

#### 华北2（北京）

`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/SpeechSynthesizer`

调用时请将 `{WorkspaceId}` 替换为对应地域的[业务空间 ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)，并使用同地域的 [API Key](../model-api-reference/preparations/get-api-key.md)。

<a id="请求头"></a>

<a id="f5b7af17168sz"></a>

## 请求头

| 参数 | 类型 | 是否必选 | 说明 |
| --- | --- | --- | --- |
| **Authorization** | `string` | 是 | 鉴权令牌，格式为`Bearer <your_api_key>`，使用时，将“`<your_api_key>`”替换为实际的API Key。 |
| **Content-Type** | `string` | 是 | 请求体的媒体类型，固定为`application/json`。 |
| **X-DashScope-SSE** | `string` | 否 | 用于控制是否以流式方式返回输出结果。仅在流式合成时使用该参数，参数值固定为`enable`。 |

<table><tbody><tr><td><a id="2a1c410015otp"></a><h2>请求体</h2><p><strong>model</strong> <code>string</code><strong>（必选）</strong></p><p>语音合成模型。</p><p>取值范围：</p><ul><li>cosyvoice-v3.5-plus</li><li>cosyvoice-v3.5-flash</li><li>cosyvoice-v3-plus</li><li>cosyvoice-v3-flash</li><li>cosyvoice-v2</li></ul><p><strong>input</strong> <code>object</code><strong>（必选）</strong></p><p>输入参数对象<strong>。</strong></p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>text</strong> <code>string</code><strong>（必选）</strong></p><p>待合成文本。</p><p>支持 SSML 和 LaTeX 格式输入。将待合成文本替换为对应格式即可。</p><ul><li>使用 SSML 时，需同时将 <code>enable_ssml</code> 设置为 <code>true</code>。支持的 SSML 标签及用法，请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-synthesis/ssml-latex-user-guide.md">SSML 与 LaTeX</a>。</li><li>使用 LaTeX 时，将待合成文本替换为 LaTeX 格式即可，无需额外配置。支持的 LaTeX 语法及用法，请参见<a href="https://help.aliyun.com/zh/model-studio/latex-capability-support-description">LaTeX 公式转语音</a>。</li></ul><p><strong>voice</strong> <code>string</code><strong>（必选）</strong></p><p>音色。</p><p>取值范围：</p><ul><li>系统音色：参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-synthesis/tts-voice-list/cosyvoice-voice-list.md">CosyVoice音色列表</a></li><li>声音复刻音色：如何创建音色请参见<a href="voice-clone-design-http-api-b6a5abbe2d5d2730.md">声音复刻HTTP API参考</a></li><li>声音设计音色：如何创建音色请参见<a href="../model-api-reference/voice-customization-api-directory/voice-design-api-references.md">声音设计API参考</a></li></ul><p><strong>format</strong> <code>string</code>（可选）</p><p>音频编码格式。</p><p>默认值：mp3。</p><p>取值范围：</p><ul><li>mp3</li><li>pcm</li><li>wav</li><li>opus</li></ul><p><strong>sample_rate</strong> <code>integer</code>（可选）</p><p>音频采样率（Hz）。</p><p>取值范围：8000、12000、16000、22050（默认）、24000、44100、48000。</p><div><div><p><strong>说明</strong>当 <code>format</code> 为 <code>opus</code> 时，<code>sample_rate</code> 仅支持 8000、12000、16000、24000、48000。</p></div></div><p><strong>volume</strong> <code>integer</code>（可选）</p><p>音量。</p><p>默认值：50。</p><p>取值范围：[0, 100]。</p><p><strong>rate</strong> <code>float</code>（可选）</p><p>语速。</p><p>默认值：1.0。</p><p>取值范围：[0.5, 2.0]。</p><p><strong>bit_rate</strong> <code>integer</code>（可选）</p><p>音频码率（单位：kbps）。</p><p>默认值：32。</p><p>取值范围：[6, 510]。</p><div><div><p><strong>重要</strong>仅在<code>format</code>为<code>opus</code>时支持使用该参数。</p></div></div><p><strong>pitch</strong> <code>float</code>（可选）</p><p>音调。</p><p>默认值：1.0。</p><p>取值范围：[0.5, 2.0]。</p><p><strong>enable_ssml</strong> <code>boolean</code>（可选）</p><p>是否开启SSML功能。SSML 的使用限制（支持的模型、音色和接口），请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-synthesis/ssml-latex-user-guide.md#sl01_constraint_h3">使用限制</a>。</p><p><strong>word_timestamp_enabled</strong> <code>boolean</code>（可选）</p><p>是否开启字级别时间戳。</p><p>默认值：false。</p><p>仅在流式输出模式下可用。支持的音色范围：cosyvoice-v3.5-plus、cosyvoice-v3.5-flash、cosyvoice-v3-flash、cosyvoice-v3-plus、cosyvoice-v2模型的复刻音色，以及<a href="../model-user-guide/model-experience/speech-and-audio/speech-synthesis/tts-voice-list/cosyvoice-voice-list.md">CosyVoice音色列表</a>中标记为支持的系统音色。其他模型的复刻音色不支持此功能。</p><p><strong>seed</strong> <code>integer</code>（可选）</p><p>生成时使用的随机数种子，使合成的效果产生变化。在模型版本、文本、音色及其他参数均相同的前提下，使用相同的seed可复现相同的合成结果。</p><p>默认值0。</p><p>取值范围：[0, 65535]。</p><p><strong>language_hints</strong> <code>array[string]</code>（可选）</p><div><div><p><strong>重要</strong></p><ul><li>此参数为数组，但当前版本仅处理第一个元素，因此建议只传入一个值。</li><li>此参数用于指定语音合成的目标语言，该设置与声音复刻时的样本音频的语种无关。如需设置复刻任务的源语言，请参见<a href="voice-clone-design-http-api-b6a5abbe2d5d2730.md#h2-create">声音复刻API参考</a>。</li></ul></div></div><p>指定语音合成的目标语言，提升合成效果。</p><p>当数字、缩写、符号等朗读方式或者小语种合成效果不符合预期时使用，例如：</p><ul><li>数字朗读方式不符合预期，“hello, this is 110”读成“hello, this is one one zero”而非“hello, this is 幺幺零”</li><li>符号朗读不准确，“@”读成“艾特”而非“at”</li><li>小语种合成效果差，合成不自然</li></ul><a id="accordion-取值范围"></a><section><p>取值范围</p><div><ul><li>zh：中文</li><li>en：英语</li><li>fr：法语</li><li>de：德语</li><li>ja：日语</li><li>ko：韩语</li><li>ru：俄语</li><li>pt：葡萄牙语</li><li>th：泰语</li><li>id：印尼语</li><li>vi：越南语</li><li>es：西班牙语</li><li>it：意大利语</li><li>ms：马来西亚语</li><li>fil：菲律宾语</li><li>ar：阿拉伯语</li></ul></div></section><p><strong>instruction</strong> <code>string</code>（可选）</p><p>设置指令，用于控制方言、情感或角色等合成效果。</p><p>具体用法请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-synthesis/non-realtime-tts-user-guide.md">非实时语音合成</a>。</p><p><strong>enable_aigc_tag</strong> <code>boolean</code>（可选）</p><p>是否在生成的音频中添加AIGC隐性标识。设置为true时，会将隐性标识嵌入到支持格式（wav/mp3/opus）的音频中。</p><p>默认值：false。</p><div><div><p><strong>说明</strong>仅cosyvoice-v3-flash、cosyvoice-v3-plus、cosyvoice-v2支持该功能。</p></div></div><p><strong>aigc_propagator</strong> <code>string</code>（可选）</p><p>设置AIGC隐性标识中的 <code>ContentPropagator</code> 字段，用于标识内容的传播者。仅在 <code>enable_aigc_tag</code> 为 <code>true</code> 时生效。</p><p>默认值：阿里云UID。</p><div><div><p><strong>说明</strong>仅cosyvoice-v3-flash、cosyvoice-v3-plus、cosyvoice-v2支持该功能。</p></div></div><p><strong>aigc_propagate_id</strong> <code>string</code>（可选）</p><p>设置AIGC隐性标识中的 <code>PropagateID</code> 字段，用于唯一标识一次具体的传播行为。仅在 <code>enable_aigc_tag</code> 为 <code>true</code> 时生效。</p><p>默认值：本次语音合成请求Request ID。</p><div><div><p><strong>说明</strong>仅cosyvoice-v3-flash、cosyvoice-v3-plus、cosyvoice-v2支持该功能。</p></div></div><p><strong>enable_markdown_filter</strong> <code>boolean</code>（可选）</p><div><div><p><strong>说明</strong>cosyvoice-v2 不支持此功能。</p></div></div><p>是否启用 Markdown 过滤。启用后，服务会在合成前将 Markdown 转换成适合朗读的文本。</p><p>默认值：false。</p><p>取值范围：</p><ul><li>true：启用Markdown过滤</li><li>false：禁用Markdown过滤</li></ul></div></section></td><td><a id="fig-code-group"></a><div><a id="fig-code-group-非流式-tab"></a>非流式<div><a id="code-code-group-非流式"></a><pre class="language-bash"><code>curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/SpeechSynthesizer \
-H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
-H &quot;Content-Type: application/json&quot; \
-d '{
    &quot;model&quot;: &quot;cosyvoice-v3-plus&quot;,
    &quot;input&quot;: {
      &quot;text&quot;: &quot;我家的后面有一个很大的花园。&quot;,
      &quot;voice&quot;: &quot;longanyang&quot;,
      &quot;format&quot;: &quot;wav&quot;,
      &quot;sample_rate&quot;: 24000
    }
}'
</code></pre></div><a id="fig-code-group-流式-tab"></a>流式<div><a id="code-code-group-流式"></a><pre class="language-bash"><code>curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/SpeechSynthesizer \
-H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
-H &quot;Content-Type: application/json&quot; \
-H &quot;X-DashScope-SSE: enable&quot; \
-d '{
    &quot;model&quot;: &quot;cosyvoice-v3-plus&quot;,
    &quot;input&quot;: {
      &quot;text&quot;: &quot;我家的后面有一个很大的花园。&quot;,
      &quot;voice&quot;: &quot;longanyang&quot;,
      &quot;format&quot;: &quot;wav&quot;,
      &quot;sample_rate&quot;: 24000
    }
}'
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="0e1c44902ea1e"></a><h2>返回体</h2><p><strong>request_id</strong> <code>string</code></p><p>本次调用的唯一标识符。</p><p><strong>output</strong> <code>object</code></p><p>模型返回的数据。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>finish_reason</strong> <code>string</code></p><p>任务停止原因，自然停止时为<code>stop</code>。</p><p>取值范围：</p><ul><li>null：语音合成中</li><li>stop：语音合成结束</li></ul><p><strong>type</strong> <code>string</code></p><p>子事件类型。仅流式合成时返回该值。</p><p>取值范围：</p><ul><li><p>sentence-begin：标识句子开始，返回待合成的句子文本内容</p></li><li><p>sentence-synthesis：标识音频数据块</p><ul><li>一个句子的合成过程中会产生多个<code>sentence-synthesis</code>事件，每个对应一个音频数据块</li><li>客户端需要按顺序接收这些音频数据块并以追加模式写入同一文件</li><li><code>sentence-synthesis</code>事件与其后的音频数据帧是一一对应的关系，不会出现错位</li></ul></li><li><p>sentence-end：标识句子结束，返回句子文本内容和累计的计费字符数</p></li></ul><p><strong>original_text</strong> <code>string</code></p><p>对用户输入文本进行分句后的句内容。最后一个句子可能没有此字段。</p><p><strong>sentence</strong> <code>object</code></p><p>句子信息。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>index</strong> <code>integer</code></p><p>句子的编号，从0开始。</p><p><strong>words</strong> <code>array</code></p><p>每句话对应的字的信息。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>text</strong> <code>string</code></p><p>字。</p><p><strong>begin_index</strong> <code>integer</code></p><p>字在句子中的开始位置索引，从 0 开始。</p><p><strong>end_index</strong> <code>integer</code></p><p>字在句子中的结束位置索引，从 1 开始。</p><p><strong>begin_time</strong> <code>integer</code></p><p>字对应音频的开始时间戳，单位为毫秒。</p><p><strong>end_time</strong> <code>integer</code></p><p>字对应音频的结束时间戳，单位为毫秒。</p></div></section></div></section><p><strong>audio</strong> <code>object</code></p><p>合成的音频数据。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>data</strong> <code>string</code></p><p>流式合成时输出Base64格式音频数据。非流式合成时为空。</p><p><strong>url</strong> <code>string</code></p><p>模型输出的完整音频文件的URL，有效期24小时。</p><p><strong>id</strong> <code>string</code></p><p>模型输出的音频信息对应的ID。</p><p><strong>expires_at</strong> <code>integer</code></p><p><code>url</code> 过期时间戳。</p></div></section></div></section><p><strong>usage</strong> <code>object</code></p><p>本次请求的字符用量。</p><a id="accordion-属性-6"></a><section><p>属性</p><div><p><strong>characters</strong> <code>integer</code></p><p>本次请求中计费的有效字符数。</p></div></section></td><td><a id="sec-tabs-2"></a><section><a id="非流式"></a><section><a id="非流式-h4"></a><h4>非流式</h4><a id="code-block"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;ee88b03d-0457-9286-8c67-xxxxxxxxxxxx&quot;,
    &quot;output&quot;: {
        &quot;finish_reason&quot;: &quot;stop&quot;,
        &quot;audio&quot;: {
            &quot;data&quot;: &quot;&quot;,
            &quot;url&quot;: &quot;http://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/pre/cosyvoice-v3-flash/20260304/xxxxxxxx/ee88b03d-0457-9286-8c67-xxxxxxxxxxxx.wav?xxxxxxx&quot;,
            &quot;id&quot;: &quot;audio_ee88b03d-0457-9286-8c67-xxxxxxxxxxxx&quot;,
            &quot;expires_at&quot;: 1772697707
        }
    },
    &quot;usage&quot;: {
        &quot;characters&quot;: 15
    }
}
</code></pre></section><a id="流式"></a><section><a id="流式-h4"></a><h4>流式</h4><p>中间结果：</p><a id="code-block-2"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;8ac1cd04-06af-9a63-b031-xxxxxxxxxxxx&quot;,
    &quot;output&quot;: {
        &quot;finish_reason&quot;: &quot;null&quot;,
        &quot;type&quot;: &quot;sentence-begin&quot;,
        &quot;original_text&quot;: &quot;我家的后面有一个很大的花园。&quot;,
        &quot;sentence&quot;: {
            &quot;index&quot;: 0,
            &quot;words&quot;: []
        },
        &quot;audio&quot;: {
            &quot;data&quot;: &quot;&quot;,
            &quot;id&quot;: &quot;audio_ee88b03d-0457-9286-8c67-xxxxxxxxxxxx&quot;,
            &quot;expires_at&quot;: 1772697707
        }
    },
    &quot;usage&quot;: {
        &quot;characters&quot;: 15
    }
}
</code></pre><p>最终结果：</p><a id="code-block-3"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;8ac1cd04-06af-9a63-b031-xxxxxxxxxxxx&quot;,
    &quot;output&quot;: {
        &quot;finish_reason&quot;: &quot;stop&quot;,
        &quot;audio&quot;: {
            &quot;data&quot;: &quot;&quot;,
            &quot;url&quot;: &quot;http://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/pre/cosyvoice-v3-flash/20260304/xxxxxxxx/8ac1cd04-06af-9a63-b031-xxxxxxxxxxxx.wav?xxxxxxx&quot;,
            &quot;id&quot;: &quot;audio_8ac1cd04-06af-9a63-b031-xxxxxxxxxxxx&quot;,
            &quot;expires_at&quot;: 1772698611
        }
    },
    &quot;usage&quot;: {
        &quot;characters&quot;: 15
    }
}
</code></pre></section></section></td></tr></tbody></table>
