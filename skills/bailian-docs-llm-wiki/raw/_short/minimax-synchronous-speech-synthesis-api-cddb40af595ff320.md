# MiniMax同步语音合成API参考

<a id="支持的模型"></a>

<a id="b00a633ba3xh5"></a>

## 支持的模型

<table><thead><tr><th><p><strong>模型名称</strong></p></th><th><p><strong>语音合成单价（每万字符）</strong></p></th><th><p><a href="https://help.aliyun.com/zh/model-studio/mini-clone-api">复刻一个音色</a></p></th><th><p><strong>免费额度</strong><a href="../model-user-guide/test-1/new-free-quota.md#977b13081ab56">（注）</a></p></th></tr></thead><tbody><tr><td><p>MiniMax/speech-2.8-hd</p></td><td><p>3.5元</p></td><td rowspan="4"><p>9.9元</p><p>（在首次使用复刻出来的音色进行语音合成的时候收取）</p></td><td rowspan="4"><p>无</p></td></tr><tr><td><p>MiniMax/speech-02-hd</p></td><td><p>3.5元</p></td></tr><tr><td><p>MiniMax/speech-2.8-turbo</p></td><td><p>2元</p></td></tr><tr><td><p>MiniMax/speech-02-turbo</p></td><td><p>2元</p></td></tr></tbody></table>

<a id="url"></a>

<a id="fe508c8badxjg"></a>

## URL

<a id="sec-tabs"></a>

<a id="华北2-北京"></a>

<a id="华北2-北京-h4"></a>

#### 华北2（北京）

HTTP请求地址：`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

SDK调用配置的base\_url：`https://dashscope.aliyuncs.com/api/v1`

<a id="headers"></a>

<a id="f5b7af17168sz"></a>

## Headers

| 参数 | 类型 | 是否必选 | 说明 |
| --- | --- | --- | --- |
| Authorization | string | 是 | 鉴权令牌，格式为`Bearer <your_api_key>`，使用时，将“`<your_api_key>`”替换为实际的API Key。 |
| Content-Type | string | 是 | 请求体的媒体类型，固定为`application/json`。 |
| X-DashScope-SSE | string | 否 | 是否启用 SSE（Server-Sent Events）流式输出。设为 `enable` 时，服务端将以流式事件逐步返回结果，适用于实时性要求较高的场景。不设置时，使用默认的同步响应模式。 |

<table><tbody><tr><td><a id="2a1c410015otp"></a><h2>请求体</h2><p><strong>model</strong><code>string</code><strong>（必选）</strong></p><p>模型名称。支持：</p><table><tbody><tr><td><p>MiniMax/speech-2.8-hd</p></td></tr><tr><td><p>MiniMax/speech-02-hd</p></td></tr><tr><td><p>MiniMax/speech-2.8-turbo</p></td></tr><tr><td><p>MiniMax/speech-02-turbo</p></td></tr></tbody></table><p><strong>input</strong><code>object</code><strong>（必选）</strong></p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>text</strong> <code>string</code><strong>（必选）</strong></p><p>待合成语音的文本。</p><p>长度限制小于 10000 字符，若文本长度大于 3000 字符，推荐使用流式输出。</p><p><strong>stream_options</strong> <code>object</code>（可选）</p><p>流式输出的配置项，仅在请求头 <code>X-DashScope-SSE: enable</code> 时生效。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>exclude_aggregated_audio</strong> <code>boolean</code>（可选） 默认值为<code>false</code></p><p>控制流式输出的合成结束帧中，<code>audio</code> 字段是否返回本次合成的完整音频（即此前所有合成中分块拼接后的整段 hex 数据）。</p><p>取值范围：</p><ul><li><code>false</code>：合成结束帧的 <code>audio</code> 字段返回所有分块拼接后的完整音频，客户端可在流结束时直接取用整段音频，无需自行拼接前面的分块。</li><li><code>true</code>：合成结束帧的 <code>audio</code> 字段为空字符串，整段音频需由客户端将此前所有合成中分块的 <code>audio</code> 按顺序自行拼接得到。可显著减少尾包体积与传输耗时，适用于客户端已经按 chunk 边接收边播放、或自行累积保存音频的场景。</li></ul><div><div><p><strong>说明</strong>该参数仅在流式输出场景下生效；非流式输出场景下设置无效。</p></div></div></div></section><p><strong>voice_setting</strong> <code>object</code><strong>（必选）</strong></p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>voice_id</strong> <code>string</code><strong>（必选）</strong></p><p>设置音色ID。</p><p>若需要设置混合音色，请设置 <code>timbre_weights</code> 参数，本参数设置为空值。</p><p><strong>speed</strong> <code>float</code>（可选） 默认值为<code>1.0</code></p><p>设置语速。</p><p>取值范围：<code>[0.5, 2.0]</code>。</p><p><strong>vol</strong> <code>float</code>（可选） 默认值为<code>1.0</code></p><p>设置音量。</p><p>取值范围：<code>(0.0, 10.0]</code>。</p><p><strong>pitch</strong> <code>integer</code>（可选） 默认值为<code>0</code></p><p>设置音高。</p><p>取值范围：<code>[-12, 12]</code>。</p><p><strong>emotion</strong> <code>string</code>（可选） 无默认值</p><p>设置情感。模型会根据输入文本自动匹配合适的情感，一般无需手动指定。</p><p>取值范围：</p><ul><li><code>happy</code>：高兴</li><li><code>sad</code>：悲伤</li><li><code>angry</code>：愤怒</li><li><code>fearful</code>：害怕</li><li><code>disgusted</code>：厌恶</li><li><code>surprised</code>：惊讶</li><li><code>calm</code>：中性</li><li><code>whisper</code>：低语</li></ul><div><div><p><strong>说明</strong><code>speech-2.8-hd</code>, <code>speech-2.8-turbo</code> 模型不支持 <code>whisper</code></p></div></div><p><strong>text_normalization</strong> <code>boolean</code>（可选） 默认值为<code>false</code></p><p>是否启用中文、英语文本规范化，开启后可提升数字阅读场景的性能，但会略微增加延迟。</p><p>取值范围：</p><ul><li><code>true</code>：开启</li><li><code>false</code>：关闭</li></ul><p><strong>latex_read</strong> <code>boolean</code>（可选） 默认值为<code>false</code></p><p>是否启用朗读 LaTeX 公式的功能。</p><p>取值范围：</p><ul><li><code>true</code>：开启</li><li><code>false</code>：关闭</li></ul><p>示例：</p><p>x = 2 a − b ± b 2 − 4 a c ​ ​</p><p>如上公式应表示为：<code>$$x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}$$</code>。</p><div><div><p><strong>说明</strong></p><ul><li>仅支持中文，开启该功能后，<code>language_boost</code>参数会被设置为<code>Chinese</code>。</li><li>请求中的公式需要在公式的首尾加上 <code>$$</code>。</li><li>请求中公式若有 <code>&quot;\&quot;</code>，需转义成 <code>&quot;\\&quot;</code>。</li></ul></div></div></div></section><p><strong>audio_setting</strong> <code>object</code>（可选）</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>sample_rate</strong> <code>integer</code>（可选） 默认值为<code>32000</code></p><p>设置生成的音频的采样率（单位为Hz）。</p><p>取值范围：</p><ul><li><code>8000</code></li><li><code>16000</code></li><li><code>22050</code></li><li><code>24000</code></li><li><code>32000</code></li><li><code>44100</code></li></ul><p><strong>bitrate</strong> <code>integer</code>（可选） 默认值为<code>128000</code></p><p>设置生成的音频的码率（单位kbps）。</p><p>取值范围：</p><ul><li><code>32000</code></li><li><code>64000</code></li><li><code>128000</code></li><li><code>256000</code></li></ul><div><div><p><strong>说明</strong>该参数仅在<code>format</code>参数为<code>mp3</code>时生效。对于其他格式，该参数将被忽略。</p></div></div><p><strong>format</strong> <code>string</code>（可选） 默认值为<code>mp3</code></p><p>设置生成的音频的格式。</p><p>取值范围：</p><ul><li><code>mp3</code></li><li><code>pcm</code></li><li><code>flac</code></li><li><code>wav</code></li></ul><p><strong>channel</strong> <code>integer</code>（可选） 默认值为<code>1</code></p><p>设置生成的音频的声道数。</p><p>取值范围：</p><ul><li><code>1</code>：单声道</li><li><code>2</code>：双声道</li></ul><p><strong>force_cbr</strong> <code>boolean</code>（可选） 默认值为<code>false</code></p><p>是否以恒定码率进行音频编码。</p><p>取值范围：</p><ul><li><code>true</code>：是</li><li><code>false</code>：否</li></ul><div><div><p><strong>说明</strong>仅流式输出且音频格式为<code>mp3</code>时该参数生效。</p></div></div></div></section><p><strong>pronunciation_dict</strong> <code>object</code>（可选）</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>tone</strong> <code>string[]</code>（可选）</p><p>定义需要特殊标注的文字或符号对应的注音或发音替换规则。</p><blockquote><p>使用 / 作为分隔符。</p></blockquote><p>在中文文本中，声调用数字表示：一声为 1，二声为 2，三声为 3，四声为 4，轻声为 5。</p><p>示例：</p><p><code>[&quot;燕少飞/(yan4)(shao3)(fei1)&quot;, &quot;omg/oh my god&quot;]</code></p></div></section><p><strong>timbre_weights</strong> <code>object[]</code>（可选）</p><p>若需要设置混合音色，请对该参数进行设置。最多支持 4 种音色混合。</p><a id="accordion-属性-6"></a><section><p>属性</p><div><p><strong>voice_id</strong> <code>string</code><strong>（必选）</strong></p><p>设置音色ID。</p><p><strong>weight</strong> <code>integer</code><strong>（必选）</strong></p><p>设置音色所占权重，必须与 <code>voice_id</code> 同步填写。单一音色取值占比越高，合成音色与该音色相似度越高。</p><p>取值范围：<code>[1, 100]</code>。</p></div></section><p><strong>language_boost</strong> <code>string</code>（可选） 默认值为<code>null</code></p><p>是否增强对指定的小语种和方言的识别能力。可设置为 <code>auto</code> 让模型自主判断。</p><a id="accordion-取值范围-点击查看"></a><section><p>取值范围（点击查看）：</p><div><ul><li><code>Chinese</code></li><li><code>Chinese,Yue</code></li><li><code>English</code></li><li><code>Arabic</code></li><li><code>Russian</code></li><li><code>Spanish</code></li><li><code>French</code></li><li><code>Portuguese</code></li><li><code>German</code></li><li><code>Turkish</code></li><li><code>Dutch</code></li><li><code>Ukrainian</code></li><li><code>Vietnamese</code></li><li><code>Indonesian</code></li><li><code>Japanese</code></li><li><code>Italian</code></li><li><code>Korean</code></li><li><code>Thai</code></li><li><code>Polish</code></li><li><code>Romanian</code></li><li><code>Greek</code></li><li><code>Czech</code></li><li><code>Finnish</code></li><li><code>Hindi</code></li><li><code>Bulgarian</code></li><li><code>Danish</code></li><li><code>Hebrew</code></li><li><code>Malay</code></li><li><code>Persian</code></li><li><code>Slovak</code></li><li><code>Swedish</code></li><li><code>Croatian</code></li><li><code>Filipino</code></li><li><code>Hungarian</code></li><li><code>Norwegian</code></li><li><code>Slovenian</code></li><li><code>Catalan</code></li><li><code>Nynorsk</code></li><li><code>Tamil</code></li><li><code>Afrikaans</code></li><li><code>auto</code></li></ul></div></section><p><strong>voice_modify</strong> <code>object</code>（可选）</p><p>设置声音效果，该参数支持的音频格式：</p><ul><li>非流式：<code>mp3</code>、<code>wav</code>、<code>flac</code></li><li>流式：<code>mp3</code></li></ul><a id="accordion-属性-7"></a><section><p>属性</p><div><p><strong>pitch</strong> <code>integer</code>（可选） 无默认值</p><p>设置音高（低沉/明亮）。</p><p>数值越低声音越低沉，数值越高声音越明亮。</p><p>取值范围：<code>[-100, 100]</code>。</p><p><strong>intensity</strong> <code>integer</code>（可选） 无默认值</p><p>设置强度（力量感/柔和）。</p><p>数值越低声音越刚劲，数值越高声音越轻柔。</p><p>取值范围：<code>[-100, 100]</code>。</p><p><strong>timbre</strong> <code>integer</code>（可选） 无默认值</p><p>设置音色明暗程度（磁性/清脆）。</p><p>数值越低声音越浑厚，数值越高声音越清脆。</p><p>取值范围：<code>[-100, 100]</code>。</p><p><strong>sound_effects</strong> <code>string</code>（可选） 无默认值</p><p>设置音效。</p><p>取值范围：</p><ul><li><code>spacious_echo</code>：空旷回音</li><li><code>auditorium_echo</code>：礼堂广播</li><li><code>lofi_telephone</code>：电话失真</li><li><code>robotic</code>：电音</li></ul></div></section><p><strong>subtitle_enable</strong> <code>boolean</code>（可选） 默认值为<code>false</code></p><p>是否开启字幕。</p><p>取值范围：</p><ul><li><code>true</code>：是</li><li><code>false</code>：否</li></ul><div><div><p><strong>说明</strong>该参数仅在非流式输出场景下有效，且仅对 <code>speech-2.8-hd</code>, <code>speech-2.8-turbo</code>, <code>speech-2.6-hd</code>, <code>speech-2.6-turbo</code>, <code>speech-02-hd</code>, <code>speech-02-turbo</code>, <code>speech-01-hd</code>, <code>speech-01-turbo</code> 模型有效。</p></div></div><p><strong>output_format</strong> <code>string</code>（可选） 默认值为<code>hex</code></p><p>设置输出结果形式。</p><p>取值范围：</p><ul><li><code>url</code>：语音合成结果以URL形式返回，有效期为24小时</li><li><code>hex</code>：语音合成结果以二进制形式返回</li></ul><div><div><p><strong>说明</strong>该参数仅在非流式场景中生效（流式场景只返回<code>hex</code>形式）。</p></div></div><p><strong>aigc_watermark</strong> <code>boolean</code>（可选） 默认值为<code>false</code></p><p>是否在合成音频末尾添加 AIGC 隐性标识。</p><p>取值范围：</p><ul><li><code>true</code>：是</li><li><code>false</code>：否</li></ul><div><div><p><strong>说明</strong>该参数仅在非流式输出场景下有效。</p></div></div></div></section></td><td><a id="fig-code-group"></a><div><a id="fig-code-group-非流式-tab"></a>非流式<div><a id="code-code-group-非流式"></a><pre class="language-bash"><code>curl -X POST &quot;https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation&quot; \
-H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
-H &quot;Content-Type: application/json&quot; \
-d '{
  &quot;model&quot;: &quot;MiniMax/speech-2.8-hd&quot;,
  &quot;input&quot;: {
    &quot;text&quot;: &quot;今天是不是很开心呀(laughs)，当然了！&quot;,
    &quot;voice_setting&quot;: {
      &quot;voice_id&quot;: &quot;male-qn-qingse&quot;,
      &quot;speed&quot;: 1,
      &quot;vol&quot;: 1,
      &quot;pitch&quot;: 0,
      &quot;emotion&quot;: &quot;happy&quot;
    },
    &quot;audio_setting&quot;: {
      &quot;sample_rate&quot;: 32000,
      &quot;bitrate&quot;: 128000,
      &quot;format&quot;: &quot;mp3&quot;,
      &quot;channel&quot;: 1
    },
    &quot;pronunciation_dict&quot;: {
      &quot;tone&quot;: [
        &quot;处理/(chu3)(li3)&quot;,
        &quot;危险/dangerous&quot;
      ]
    },
    &quot;subtitle_enable&quot;: false
  }
}'
</code></pre></div><a id="fig-code-group-流式-tab"></a>流式<div><a id="code-code-group-流式"></a><pre class="language-bash"><code>curl -X POST &quot;https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation&quot; \
-H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
-H &quot;Content-Type: application/json&quot; \
-H &quot;X-DashScope-SSE: enable&quot; \
-d '{
  &quot;model&quot;: &quot;MiniMax/speech-2.8-hd&quot;,
  &quot;input&quot;: {
    &quot;text&quot;: &quot;今天是不是很开心呀(laughs)，当然了！&quot;,
    &quot;voice_setting&quot;: {
      &quot;voice_id&quot;: &quot;male-qn-qingse&quot;,
      &quot;speed&quot;: 1,
      &quot;vol&quot;: 1,
      &quot;pitch&quot;: 0,
      &quot;emotion&quot;: &quot;happy&quot;
    },
    &quot;audio_setting&quot;: {
      &quot;sample_rate&quot;: 32000,
      &quot;bitrate&quot;: 128000,
      &quot;format&quot;: &quot;mp3&quot;,
      &quot;channel&quot;: 1
    },
    &quot;pronunciation_dict&quot;: {
      &quot;tone&quot;: [
        &quot;处理/(chu3)(li3)&quot;,
        &quot;危险/dangerous&quot;
      ]
    },
    &quot;subtitle_enable&quot;: false
  }
}'
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="0e1c44902ea1e"></a><h2>返回体</h2><p><strong>request_id</strong><code>string</code></p><p>本次调用的唯一标识符。</p><p><strong>output</strong><code>object</code></p><p>模型返回的数据。</p><a id="accordion-属性-8"></a><section><p>属性</p><div><p><strong>base_resp</strong><code>object</code></p><p>本次请求的状态码和详情。</p><a id="accordion-属性-9"></a><section><p>属性</p><div><p><strong>status_code</strong> <code>integer</code></p><p>状态码。</p><p>您可在header中获取本次会话的trace_id，用于在咨询/反馈时帮助定位问题</p><ul><li><code>0</code>: 请求结果正常</li><li><code>1000</code>: 未知错误</li><li><code>1001</code>: 超时</li><li><code>1002</code>: 触发限流</li><li><code>1004</code>: 鉴权失败</li><li><code>1039</code>: 触发 TPM 限流</li><li><code>1042</code>: 非法字符超过 10%</li><li><code>2013</code>: 输入参数信息不正常</li></ul><p>更多内容可查看 <a href="https://platform.minimaxi.com/docs/api-reference/errorcode"><strong>错误码查询列表</strong></a> 了解详情</p><p><strong>status_msg</strong> <code>string</code></p><p>状态详情。</p></div></section><p><strong>data</strong><code>object</code></p><p>返回的合成数据对象，可能为 null，需进行非空判断。</p><a id="accordion-属性-10"></a><section><p>属性</p><div><p><strong>audio</strong><code>string</code></p><p>合成后的音频数据，采用 hex 编码，格式与请求中（<code>output_format</code>参数）指定的输出格式一致。</p><p><strong>status</strong> <code>integer</code></p><p>当前音频流状态：1 表示合成中，2 表示合成结束</p></div></section><p><strong>extra_info</strong><code>object</code></p><a id="accordion-属性-11"></a><section><p>属性</p><div><p><strong>audio_length</strong><code>integer</code></p><p>音频时长（毫秒）</p><p><strong>audio_sample_rate</strong><code>integer</code></p><p>音频采样率</p><p><strong>audio_size</strong><code>integer</code></p><p>音频文件大小（字节）</p><p><strong>bitrate</strong><code>integer</code></p><p>音频比特率</p><p><strong>audio_format</strong><code>string</code></p><p>生成音频文件的格式。取值范围 <code>[mp3, pcm, flac]</code></p><p>可用选项： <code>mp3</code>, <code>pcm</code>, <code>flac</code>。</p><p><a href="https://platform.minimaxi.com/docs/api-reference/speech-t2a-http#response-extra-info-audio-channel"><strong>​</strong></a><strong>audio_channel</strong> <code>integer</code></p><p>生成音频声道数,1：单声道，2：双声道</p><p><a href="https://platform.minimaxi.com/docs/api-reference/speech-t2a-http#response-extra-info-invisible-character-ratio"><strong>​</strong></a><strong>invisible_character_ratio</strong> <code>float</code></p><p>非法字符占比.非法字符不超过 10%（包含 10%），音频会正常生成,并返回非法字符占比数据；如超过 10% 将进行报错</p><p><a href="https://platform.minimaxi.com/docs/api-reference/speech-t2a-http#response-extra-info-usage-characters"><strong>​</strong></a><strong>usage_characters</strong><code>integer</code></p><p>计费字符数</p><p><strong>word_count</strong><code>integer</code></p><p>已发音的字数统计，包含汉字、数字、字母，不包含标点符号</p></div></section><p><strong>trace_id</strong><code>string</code></p><p>本次会话的 id，用于在咨询/反馈时帮助定位问题</p></div></section><p><strong>base_resp</strong><code>object</code></p><p>本次请求的状态码和详情。</p><a id="accordion-属性-12"></a><section><p>属性</p><div><p><strong>audio</strong><code>string</code></p><p>合成后的音频数据，采用 hex 编码，格式与请求中（<code>output_format</code>参数）指定的输出格式一致。</p></div></section><p><strong>usage</strong><code>object</code></p><p>本次请求的计费用量。</p><a id="accordion-属性-13"></a><section><p>属性</p><div><p><strong>characters</strong> <code>integer</code></p><p>输入文本的字符数。</p><p><strong>count</strong> <code>integer</code>（可选）</p><p>本次请求产生的复刻音色解锁计费次数。首次使用复刻音色合成语音会返回此字段，值为 <code>1</code>；后续使用同一音色时不返回此字段。</p><p>音色解锁费仅收取一次。</p><a id="fig-code-group-2"></a><div><a id="fig-code-group-2-首次使用复刻音色-tab"></a>首次使用复刻音色<div><a id="code-code-group-2-首次使用复刻音色"></a><pre class="language-json"><code>{
    &quot;characters&quot;: 17,
    &quot;count&quot;: 1
}
</code></pre></div><a id="fig-code-group-2-再次使用同一音色-tab"></a>再次使用同一音色<div><a id="code-code-group-2-再次使用同一音色"></a><pre class="language-json"><code>{
    &quot;characters&quot;: 17
}
</code></pre></div></div></div></section></td><td><a id="fig-code-group-3"></a><div><a id="fig-code-group-3-非流式-tab"></a>非流式<div><a id="code-code-group-3-非流式"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
        &quot;base_resp&quot;: {
            &quot;status_code&quot;: 0,
            &quot;status_msg&quot;: &quot;success&quot;
        },
        &quot;data&quot;: {
            &quot;audio&quot;: &quot;&lt;hex编码的audio&gt;&quot;,
            &quot;ced&quot;: &quot;&quot;,
            &quot;status&quot;: 2
        },
        &quot;extra_info&quot;: {
            &quot;audio_channel&quot;: 1,
            &quot;audio_format&quot;: &quot;mp3&quot;,
            &quot;audio_length&quot;: 4536,
            &quot;audio_sample_rate&quot;: 32000,
            &quot;audio_size&quot;: 74292,
            &quot;bitrate&quot;: 128000,
            &quot;invisible_character_ratio&quot;: 0,
            &quot;usage_characters&quot;: 34,
            &quot;word_count&quot;: 22
        },
        &quot;trace_id&quot;: &quot;07251d0708c723e3a8f8dd979928e429&quot;
    },
    &quot;usage&quot;: {
        &quot;characters&quot;: 34
    },
    &quot;request_id&quot;: &quot;35c7bb92-2898-9c4a-9be4-200bc7c5d61f&quot;
}
</code></pre></div><a id="fig-code-group-3-流式-tab"></a>流式<div><a id="code-code-group-3-流式"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
        &quot;base_resp&quot;: {
            &quot;status_code&quot;: 0,
            &quot;status_msg&quot;: &quot;success&quot;
        },
        &quot;data&quot;: {
            &quot;audio&quot;: &quot;&lt;hex编码的audio&gt;&quot;,
            &quot;ced&quot;: &quot;&quot;,
            &quot;status&quot;: 2
        },
        &quot;extra_info&quot;: {
            &quot;audio_channel&quot;: 1,
            &quot;audio_format&quot;: &quot;mp3&quot;,
            &quot;audio_length&quot;: 4003,
            &quot;audio_sample_rate&quot;: 32000,
            &quot;audio_size&quot;: 66804,
            &quot;bitrate&quot;: 128000,
            &quot;invisible_character_ratio&quot;: 0,
            &quot;usage_characters&quot;: 34,
            &quot;word_count&quot;: 22
        },
        &quot;trace_id&quot;: &quot;07251d0bd210b373b1c718f87b8452f4&quot;
    },
    &quot;usage&quot;: {
        &quot;characters&quot;: 34
    },
    &quot;request_id&quot;: &quot;eae023d1-5bbd-919f-8586-90e0ee99cd7e&quot;
}
</code></pre></div></div></td></tr></tbody></table>
