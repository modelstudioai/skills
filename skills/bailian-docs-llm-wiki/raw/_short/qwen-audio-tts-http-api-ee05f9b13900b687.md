# 非实时语音合成Qwen-Audio-TTS HTTP API参考

本文介绍非实时语音合成Qwen-Audio-TTS的HTTP调用方法，支持非流式和流式两种调用模式。

<a id="接口地址"></a>

<a id="fe508c8badxjg"></a>

## 接口地址

<a id="sec-tabs"></a>

<a id="华北2-北京"></a>

<a id="华北2-北京-h4"></a>

#### 华北2（北京）

`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/SpeechSynthesizer`

<a id="新加坡"></a>

<a id="新加坡-h4"></a>

#### 新加坡

`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/audio/tts/SpeechSynthesizer`

调用时请将 `{WorkspaceId}` 替换为对应地域的[业务空间 ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)，并使用同地域的 [API Key](../model-api-reference/preparations/get-api-key.md)。

<a id="请求头"></a>

<a id="f5b7af17168sz"></a>

## 请求头

| 参数 | 类型 | 是否必选 | 说明 |
| --- | --- | --- | --- |
| **Authorization** | `string` | 是 | 鉴权令牌，格式为`Bearer <your_api_key>`，使用时，将“`<your_api_key>`”替换为实际的API Key。 |
| **Content-Type** | `string` | 是 | 请求体的媒体类型，固定为`application/json`。 |
| **X-DashScope-SSE** | `string` | 否 | 用于控制是否以流式方式返回输出结果。仅在流式合成时使用该参数，参数值固定为`enable`。 |

<table><tbody><tr><td><a id="2a1c410015otp"></a><h2>请求体</h2><p><strong>model</strong> <code>string</code><strong>（必选）</strong></p><p>语音合成模型。</p><p><strong>input</strong> <code>object</code><strong>（必选）</strong></p><p>输入参数对象<strong>。</strong></p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>text</strong> <code>string</code><strong>（必选）</strong></p><p>待合成文本。</p><p>支持 SSML 和 LaTeX 格式输入。将待合成文本替换为对应格式即可。</p><ul><li>使用 SSML 时，需同时将 <code>enable_ssml</code> 设置为 <code>true</code>。支持的 SSML 标签及用法，请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-synthesis/ssml-latex-user-guide.md">SSML 与 LaTeX</a>。</li><li>使用 LaTeX 时，将待合成文本替换为 LaTeX 格式即可，无需额外配置。支持的 LaTeX 语法及用法，请参见<a href="https://help.aliyun.com/zh/model-studio/latex-capability-support-description">LaTeX 公式转语音</a>。</li></ul><p><strong>voice</strong> <code>string</code><strong>（必选）</strong></p><p>音色。</p><p>取值范围：</p><ul><li>系统音色：参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-synthesis/tts-voice-list/qwen-audio-tts-voice-list.md">Qwen-Audio-TTS音色列表</a></li><li>声音复刻音色：如何创建音色请参见<a href="voice-clone-design-http-api-b6a5abbe2d5d2730.md">声音复刻HTTP API参考</a></li><li>声音设计音色：如何创建音色请参见<a href="../model-api-reference/voice-customization-api-directory/voice-design-api-references.md">声音设计API参考</a></li></ul><p><strong>format</strong> <code>string</code>（可选）</p><p>音频编码格式。</p><p>默认值：mp3。</p><p>取值范围：</p><ul><li>mp3</li><li>pcm</li><li>wav</li><li>opus</li></ul><p><strong>sample_rate</strong> <code>integer</code>（可选）</p><p>音频采样率（Hz）。</p><p>取值范围：8000、12000、16000、22050（默认）、24000、44100、48000。</p><div><div><p><strong>说明</strong>当 <code>format</code> 为 <code>opus</code> 时，<code>sample_rate</code> 仅支持 8000、12000、16000、24000、48000。</p></div></div><p><strong>volume</strong> <code>integer</code>（可选）</p><p>音量。</p><p>默认值：50。</p><p>取值范围：[0, 100]。</p><p><strong>rate</strong> <code>float</code>（可选）</p><p>语速。</p><p>默认值：1.0。</p><p>取值范围：[0.5, 2.0]。</p><p><strong>bit_rate</strong> <code>integer</code>（可选）</p><p>音频码率（单位：kbps）。</p><p>默认值：32。</p><p>取值范围：[6, 510]。</p><div><div><p><strong>重要</strong>仅在<code>format</code>为<code>opus</code>时支持使用该参数。</p></div></div><p><strong>pitch</strong> <code>float</code>（可选）</p><p>音调。</p><p>默认值：1.0。</p><p>取值范围：[0.5, 2.0]。</p><p><strong>enable_ssml</strong> <code>boolean</code>（可选）</p><p>是否开启SSML功能。SSML 的使用限制（支持的模型、音色和接口），请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-synthesis/ssml-latex-user-guide.md#sl01_constraint_h3">使用限制</a>。</p><p><strong>word_timestamp_enabled</strong> <code>boolean</code>（可选）</p><p>是否开启字级别时间戳。</p><p>默认值：false。</p><p>仅在流式输出模式下可用。支持复刻音色；支持的系统音色请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-synthesis/tts-voice-list/qwen-audio-tts-voice-list.md">Qwen-Audio-TTS音色列表</a>。</p><p><strong>seed</strong> <code>integer</code>（可选）</p><p>生成时使用的随机数种子，使合成的效果产生变化。在模型版本、文本、音色及其他参数均相同的前提下，使用相同的seed可复现相同的合成结果。</p><p>默认值0。</p><p>取值范围：[0, 65535]。</p><p><strong>language_hints</strong> <code>array[string]</code>（可选）</p><div><div><p><strong>说明</strong>使用 qwen-audio-3.1-tts-flash 的多语种与方言音色时，可通过此参数指定语种或方言。具体用法请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-synthesis/tts-voice-list/qwen-audio-tts-voice-list.md#qwen-tts31-language-hints">多语种与方言音色的设置方法</a>。</p></div></div><p>指定语音合成的目标语言，提升合成效果。</p><p>当数字、缩写、符号等朗读方式或者小语种合成效果不符合预期时使用，例如：</p><ul><li>数字朗读方式不符合预期，“hello, this is 110”读成“hello, this is one one zero”而非“hello, this is 幺幺零”</li><li>符号朗读不准确，“@”读成“艾特”而非“at”</li><li>小语种合成效果差，合成不自然</li></ul><a id="accordion-取值范围"></a><section><p>取值范围</p><div><ul><li><p>zh：中文</p></li><li><p>en：英语</p></li><li><p>fr：法语</p></li><li><p>de：德语</p></li><li><p>ja：日语</p></li><li><p>ko：韩语</p></li><li><p>ru：俄语</p></li><li><p>pt：葡萄牙语</p></li><li><p>th：泰语</p></li><li><p>id：印尼语</p></li><li><p>vi：越南语</p></li><li><p>es：西班牙语</p></li><li><p>it：意大利语</p></li><li><p>ms：马来西亚语</p></li><li><p>fil：菲律宾语</p></li><li><p>ar：阿拉伯语</p></li><li><p>other：其他语种（适用于 <code>qwen-audio-3.1-tts-flash</code>）</p><p>保加利亚语、荷兰语、匈牙利语、罗马尼亚语、丹麦语、克罗地亚语、希腊语、捷克语、挪威语、瑞典语、印地语、斯洛伐克语、芬兰语、乌尔都语、塞尔维亚语、墨西哥西班牙语、立陶宛语、拉脱维亚语、土耳其语、波斯语、希伯来语、蒙古语、斯洛文尼亚语、阿塞拜疆语、波兰语、加泰罗尼亚语、高棉语、巴西葡萄牙语、老挝语、格鲁吉亚语、南非荷兰语、尼泊尔语、白俄罗斯语、马拉雅拉姆语、卢森堡语、阿尔巴尼亚语、泰米尔语、僧伽罗语、泰卢固语、爱沙尼亚语、宿务语、波斯尼亚语、缅甸语、亚美尼亚语、拉丁语、冰岛语、马耳他语、斯瓦希里语、哈萨克语、塞舌尔克里奥尔语、乌克兰语。</p></li></ul></div></section><div><div><p><strong>说明</strong></p><ul><li>此参数为数组，但当前版本仅处理第一个元素，因此建议只传入一个值。</li><li>此参数用于指定语音合成的目标语言，该设置与声音复刻时的样本音频的语种无关。如需设置复刻任务的源语言，请参见<a href="voice-clone-design-http-api-b6a5abbe2d5d2730.md#h2-create">声音复刻API参考</a>。</li></ul></div></div><p><strong>instruction</strong> <code>string</code>（可选）</p><p>设置指令，用于控制方言、情感或角色等合成效果。</p><p>具体用法请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-synthesis/non-realtime-tts-user-guide.md">非实时语音合成</a>。</p><p><strong>enable_aigc_tag</strong> <code>boolean</code>（可选）</p><p>是否在生成的音频中添加AIGC隐性标识。设置为true时，会将隐性标识嵌入到支持格式（wav/mp3/opus）的音频中。</p><p>默认值：false。</p><p><strong>aigc_propagator</strong> <code>string</code>（可选）</p><p>设置AIGC隐性标识中的 <code>ContentPropagator</code> 字段，用于标识内容的传播者。仅在 <code>enable_aigc_tag</code> 为 <code>true</code> 时生效。</p><p>默认值：阿里云UID。</p><p><strong>aigc_propagate_id</strong> <code>string</code>（可选）</p><p>设置AIGC隐性标识中的 <code>PropagateID</code> 字段，用于唯一标识一次具体的传播行为。仅在 <code>enable_aigc_tag</code> 为 <code>true</code> 时生效。</p><p>默认值：本次语音合成请求Request ID。</p><p><strong>hot_fix</strong> <code>object</code>（可选）</p><p>文本热修复配置，用于自定义指定词语的发音或对待合成文本进行替换。</p><p>参数介绍：</p><ul><li>pronunciation：自定义发音。指定词语的拼音标注，用于纠正默认发音不准确的情况。</li><li>replace：文本替换。在语音合成前将指定词语替换为目标文本，替换后的文本将作为实际合成内容。</li></ul><p>示例：</p><a id="code-block"></a><pre class="language-json"><code>&quot;hot_fix&quot;: {
  &quot;pronunciation&quot;: [
    {&quot;天气&quot;: &quot;tian1 qi4&quot;}
  ],
  &quot;replace&quot;: [
    {&quot;今天&quot;: &quot;金天&quot;}
  ]
}
</code></pre><p><strong>enable_markdown_filter</strong> <code>boolean</code>（可选）</p><p>是否启用 Markdown 过滤。启用后，服务会在合成前将 Markdown 转换成适合朗读的文本。</p><p>默认值：<code>false</code>。设为 <code>true</code> 启用。</p></div></section></td><td><a id="fig-code-group"></a><div><a id="fig-code-group-非流式-tab"></a>非流式<div><a id="code-code-group-非流式"></a><pre class="language-bash"><code>curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/SpeechSynthesizer \
-H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
-H &quot;Content-Type: application/json&quot; \
-d '{
    &quot;model&quot;: &quot;qwen-audio-3.0-tts-flash&quot;,
    &quot;input&quot;: {
      &quot;text&quot;: &quot;我家的后面有一个很大的花园。&quot;,
      &quot;voice&quot;: &quot;longanhuan_v3.6&quot;,
      &quot;format&quot;: &quot;wav&quot;,
      &quot;sample_rate&quot;: 24000
    }
}'
</code></pre></div><a id="fig-code-group-流式-tab"></a>流式<div><a id="code-code-group-流式"></a><pre class="language-bash"><code>curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/SpeechSynthesizer \
-H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
-H &quot;Content-Type: application/json&quot; \
-H &quot;X-DashScope-SSE: enable&quot; \
-d '{
    &quot;model&quot;: &quot;qwen-audio-3.0-tts-flash&quot;,
    &quot;input&quot;: {
      &quot;text&quot;: &quot;我家的后面有一个很大的花园。&quot;,
      &quot;voice&quot;: &quot;longanhuan_v3.6&quot;,
      &quot;format&quot;: &quot;wav&quot;,
      &quot;sample_rate&quot;: 24000
    }
}'
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="0e1c44902ea1e"></a><h2>返回体</h2><p><strong>request_id</strong> <code>string</code></p><p>本次调用的唯一标识符。</p><p><strong>output</strong> <code>object</code></p><p>模型返回的数据。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>finish_reason</strong> <code>string</code></p><p>任务停止原因，自然停止时为<code>stop</code>。</p><p>取值范围：</p><ul><li>null：语音合成中</li><li>stop：语音合成结束</li></ul><p><strong>type</strong> <code>string</code></p><p>子事件类型。仅流式合成时返回该值。</p><p>取值范围：</p><ul><li><p>sentence-begin：标识句子开始，返回待合成的句子文本内容</p></li><li><p>sentence-synthesis：标识音频数据块</p><ul><li>一个句子的合成过程中会产生多个<code>sentence-synthesis</code>事件，每个对应一个音频数据块</li><li>客户端需要按顺序接收这些音频数据块并以追加模式写入同一文件</li><li><code>sentence-synthesis</code>事件与其后的音频数据帧是一一对应的关系，不会出现错位</li></ul></li><li><p>sentence-end：标识句子结束，返回句子文本内容和用量信息（<code>usage</code>）</p></li></ul><p><strong>original_text</strong> <code>string</code></p><p>对用户输入文本进行分句后的句内容。最后一个句子可能没有此字段。</p><p><strong>sentence</strong> <code>object</code></p><p>句子信息。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>index</strong> <code>integer</code></p><p>句子的编号，从0开始。</p><p><strong>words</strong> <code>array</code></p><p>每句话对应的字的信息。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>text</strong> <code>string</code></p><p>字。</p><p><strong>begin_index</strong> <code>integer</code></p><p>字在句子中的开始位置索引，从 0 开始。</p><p><strong>end_index</strong> <code>integer</code></p><p>字在句子中的结束位置索引，从 1 开始。</p><p><strong>begin_time</strong> <code>integer</code></p><p>字对应音频的开始时间戳，单位为毫秒。</p><p><strong>end_time</strong> <code>integer</code></p><p>字对应音频的结束时间戳，单位为毫秒。</p></div></section></div></section><p><strong>audio</strong> <code>object</code></p><p>合成的音频数据。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>data</strong> <code>string</code></p><p>流式合成时输出Base64格式音频数据。非流式合成时为空。</p><p><strong>url</strong> <code>string</code></p><p>模型输出的完整音频文件的URL，有效期24小时。</p><p><strong>id</strong> <code>string</code></p><p>模型输出的音频信息对应的ID。</p><p><strong>expires_at</strong> <code>integer</code></p><p><code>url</code> 过期时间戳。</p></div></section></div></section><p><strong>usage</strong> <code>object</code></p><a id="usage-fields"></a><p>计费用量。</p><div><div><p><strong>说明</strong><code>qwen-audio-3.1-tts-flash</code> 按输入和输出 Token 计费；<code>qwen-audio-3.1-tts-plus</code>、<code>qwen-audio-3.0-tts-plus</code> 和 <code>qwen-audio-3.0-tts-flash</code> 按字符计费。</p></div></div><a id="accordion-属性-6"></a><section><p>属性</p><div><p><strong>input_tokens</strong> <code>integer</code></p><p>本次请求的输入 Token 数。</p><div><div><p><strong>说明</strong>适用于 <code>qwen-audio-3.1-tts-plus</code>、<code>qwen-audio-3.1-tts-flash</code>。</p></div></div><p><strong>output_tokens</strong> <code>integer</code></p><p>本次请求的输出 Token 数。</p><div><div><p><strong>说明</strong>适用于 <code>qwen-audio-3.1-tts-plus</code>、<code>qwen-audio-3.1-tts-flash</code>。</p></div></div><p><strong>total_tokens</strong> <code>integer</code></p><p>输入和输出 Token 数之和。</p><div><div><p><strong>说明</strong>适用于 <code>qwen-audio-3.1-tts-plus</code>、<code>qwen-audio-3.1-tts-flash</code>。</p></div></div><p><strong>characters</strong> <code>integer</code></p><p>累计计费字符数。</p></div></section></td><td><a id="sec-tabs-2"></a><section><a id="非流式"></a><section><a id="非流式-h4"></a><h4>非流式</h4><a id="code-block-2"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;ee88b03d-0457-9286-8c67-xxxxxxxxxxxx&quot;,
    &quot;output&quot;: {
        &quot;finish_reason&quot;: &quot;stop&quot;,
        &quot;audio&quot;: {
            &quot;data&quot;: &quot;&quot;,
            &quot;url&quot;: &quot;http://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/pre/qwen-audio-3.0-tts-flash/20260304/xxxxxxxx/ee88b03d-0457-9286-8c67-xxxxxxxxxxxx.wav?xxxxxxx&quot;,
            &quot;id&quot;: &quot;audio_ee88b03d-0457-9286-8c67-xxxxxxxxxxxx&quot;,
            &quot;expires_at&quot;: 1772697707
        }
    },
    &quot;usage&quot;: {
        &quot;characters&quot;: 15
    }
}
</code></pre></section><a id="流式"></a><section><a id="流式-h4"></a><h4>流式</h4><p>中间结果：</p><a id="code-block-3"></a><pre class="language-json"><code>{
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
</code></pre><p>最终结果：</p><a id="code-block-4"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;8ac1cd04-06af-9a63-b031-xxxxxxxxxxxx&quot;,
    &quot;output&quot;: {
        &quot;finish_reason&quot;: &quot;stop&quot;,
        &quot;audio&quot;: {
            &quot;data&quot;: &quot;&quot;,
            &quot;url&quot;: &quot;http://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/pre/qwen-audio-3.0-tts-flash/20260304/xxxxxxxx/8ac1cd04-06af-9a63-b031-xxxxxxxxxxxx.wav?xxxxxxx&quot;,
            &quot;id&quot;: &quot;audio_8ac1cd04-06af-9a63-b031-xxxxxxxxxxxx&quot;,
            &quot;expires_at&quot;: 1772698611
        }
    },
    &quot;usage&quot;: {
        &quot;characters&quot;: 15
    }
}
</code></pre></section></section></td></tr></tbody></table>
