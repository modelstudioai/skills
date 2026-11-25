# 音色设计 API 参考

本文介绍声音设计的HTTP API接口详情，包括创建音色、查询音色列表、查询音色详情和删除音色四个操作。

**用户指南：**[声音设计](../../model-user-guide/model-experience/speech-and-audio/speech-synthesis/voice-customization/voice-design-user-guide.md)。

<a id="接口地址"></a>

<a id="vd-h2-url"></a>

## 接口地址

<a id="sec-tabs"></a>

<a id="华北2-北京"></a>

<a id="华北2-北京-h4"></a>

#### 华北2（北京）

`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/customization`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

> **重要**
>
> 阿里云百炼为华北2（北京）地域推出了业务空间专属域名，能够为推理请求提供卓越的性能和更高的稳定性，建议迁移至新域名：
>
> -   华北2（北京）地域：从 `dashscope.aliyuncs.com` 迁移至 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
>
> `{WorkspaceId}`需要替换为真实的[Workspace ID](../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。现有域名仍可正常使用。

<a id="请求头"></a>

<a id="vd-h2-headers"></a>

## 请求头

| 参数 | 类型 | 是否必选 | 说明 |
| --- | --- | --- | --- |
| Authorization | string | 是 | 鉴权令牌，格式为`Bearer <your_api_key>`，使用时，将"`<your_api_key>`"替换为实际的API Key。 |
| Content-Type | string | 是 | 请求体的媒体类型。固定为`application/json`。 |

<a id="创建音色"></a>

<a id="vd-h2-create"></a>

## 创建音色

<table><tbody><tr><td><a id="vd-h3-cr-rq"></a><h3>请求体</h3><p><strong>model</strong><code>string</code><strong>（必选）</strong></p><p>声音设计模型。取值：</p><ul><li><code>voice-enrollment</code>：Qwen-Audio-TTS/CosyVoice声音设计。</li></ul><p><strong>input</strong><code>object</code><strong>（必选）</strong></p><p>输入参数对象。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>action</strong> <code>string</code><strong>（必选）</strong></p><p>操作类型。</p><ul><li>Qwen-Audio-TTS/CosyVoice（<code>voice-enrollment</code>）：固定为<code>create_voice</code>。</li></ul><p><strong>target_model</strong> <code>string</code><strong>（必选）</strong></p><p>驱动音色的语音合成模型。必须与后续调用语音合成接口时使用的模型一致，否则合成会失败。</p><p><strong>voice_prompt</strong> <code>string</code><strong>（必选）</strong></p><p>声音描述文本，仅支持中文和英文。</p><ul><li>Qwen-Audio-TTS/CosyVoice（<code>voice-enrollment</code>）：最大长度500字符。</li></ul><p><strong>preview_text</strong> <code>string</code><strong>（必选）</strong></p><p>预览音频对应的文本。</p><ul><li>Qwen-Audio-TTS/CosyVoice（<code>voice-enrollment</code>）：最小长度15字符，最大长度200字符，支持中文和英文。</li></ul><p><strong>prefix</strong> <code>string</code><strong>（必选）</strong></p><div><div><p><strong>重要</strong>仅适用于Qwen-Audio-TTS/CosyVoice（model为<code>voice-enrollment</code>时）。</p></div></div><p>音色名称前缀，仅允许数字和英文字母，不超过10个字符。生成的音色名格式：<code>{target_model}-vd-{prefix}-{唯一标识}</code></p><p><strong>language_hints</strong> <code>array[string]</code>（可选）</p><div><div><p><strong>重要</strong>仅适用于Qwen-Audio-TTS/CosyVoice（model为<code>voice-enrollment</code>时）。</p></div></div><p>指定生成音色的语言倾向，影响音色的语言特征和发音倾向，建议根据实际使用场景选择对应语言代码。若使用该参数，设置的语种须与 <code>preview_text</code> 的语种一致。</p><p>此参数为数组，但当前版本仅处理第一个元素。</p><p>取值范围：</p><ul><li>zh：中文</li><li>en：英文</li></ul><p>默认值：[&quot;zh&quot;]。</p></div></section><p><strong>parameters</strong><code>object</code>（可选）</p><p>声音设计的参数配置。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>sample_rate</strong> <code>int</code>（可选）</p><p>预览音频采样率（Hz）。</p><ul><li>Qwen-Audio-TTS/CosyVoice支持：16000、24000、48000。</li></ul><p>默认值：24000。</p><p><strong>response_format</strong> <code>string</code>（可选）</p><p>预览音频格式。</p><ul><li>Qwen-Audio-TTS/CosyVoice支持：pcm、wav、mp3。</li></ul><p>默认值：wav。</p></div></section></td><td><p>以下为华北2（北京）地域的配置，调用时请将&quot;{WorkspaceId}&quot;替换为真实的业务空间ID，各地域的配置不同。</p><a id="fig-code-group"></a><div><a id="fig-code-group-qwen-audio-tts-cosyvoice声音设计-tab"></a>Qwen-Audio-TTS/CosyVoice声音设计<div><a id="code-code-group-qwen-audio-tts-cosyvoice声音设计"></a><pre class="language-bash"><code>curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/customization \
-H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
-H &quot;Content-Type: application/json&quot; \
-d '{
    &quot;model&quot;: &quot;voice-enrollment&quot;,
    &quot;input&quot;: {
        &quot;action&quot;: &quot;create_voice&quot;,
        &quot;target_model&quot;: &quot;cosyvoice-v3.5-plus&quot;,
        &quot;voice_prompt&quot;: &quot;沉稳的中年男性，音色低沉浑厚&quot;,
        &quot;preview_text&quot;: &quot;各位听众朋友们大家好，欢迎收听本期节目&quot;,
        &quot;prefix&quot;: &quot;announcer&quot;,
        &quot;language_hints&quot;: [&quot;zh&quot;]
    },
    &quot;parameters&quot;: {
        &quot;sample_rate&quot;: 24000,
        &quot;response_format&quot;: &quot;wav&quot;
    }
}'
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="vd-h3-cr-rs"></a><h3>返回体</h3><p><strong>request_id</strong><code>string</code></p><p>本次调用的唯一标识符。</p><p><strong>output</strong><code>object</code></p><p>模型返回的数据。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>voice_id</strong><code>string</code></p><p>音色 ID，可用于语音合成接口的 <code>voice</code> 参数。</p><p><strong>preview_audio</strong><code>object</code></p><p>预览音频数据。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>data</strong> <code>string</code></p><p>预览音频数据，Base64编码。</p><p><strong>sample_rate</strong> <code>int</code></p><p>预览音频采样率（Hz）。</p><p><strong>response_format</strong> <code>string</code></p><p>预览音频格式。</p></div></section><p><strong>target_model</strong><code>string</code></p><p>驱动音色的语音合成模型。</p></div></section><p><strong>usage</strong><code>object</code></p><p>本次请求用量信息。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>count</strong> <code>integer</code></p><p>创建的音色数量，固定为1。</p></div></section></td><td><a id="fig-code-group-2"></a><div><a id="fig-code-group-2-qwen-audio-tts-cosyvoice声音设计-tab"></a>Qwen-Audio-TTS/CosyVoice声音设计<div><a id="code-code-group-2-qwen-audio-tts-cosyvoice声音设计"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
        &quot;preview_audio&quot;: {
            &quot;data&quot;: &quot;{base64_encoded_audio}&quot;,
            &quot;sample_rate&quot;: 24000,
            &quot;response_format&quot;: &quot;wav&quot;
        },
        &quot;target_model&quot;: &quot;cosyvoice-v3.5-plus&quot;,
        &quot;voice_id&quot;: &quot;cosyvoice-v3.5-plus-vd-announcer-xxxxxx&quot;
    },
    &quot;usage&quot;: {
        &quot;count&quot;: 1
    },
    &quot;request_id&quot;: &quot;xxxx-xxxx-xxxx&quot;
}
</code></pre></div></div></td></tr></tbody></table>

<a id="查询音色列表"></a>

<a id="vd-h2-list"></a>

## 查询音色列表

<table><tbody><tr><td><a id="vd-h3-ls-rq"></a><h3>请求体</h3><p><strong>model</strong><code>string</code><strong>（必选）</strong></p><p>声音设计模型。取值：</p><ul><li><code>voice-enrollment</code>：Qwen-Audio-TTS/CosyVoice声音设计。</li></ul><p><strong>input</strong><code>object</code><strong>（必选）</strong></p><p>输入参数对象。</p><a id="accordion-属性-6"></a><section><p>属性</p><div><p><strong>action</strong> <code>string</code><strong>（必选）</strong></p><p>固定为 <code>list_voice</code>。</p><p><strong>prefix</strong> <code>string</code>（可选）</p><div><div><p><strong>重要</strong>仅适用于Qwen-Audio-TTS/CosyVoice。</p></div></div><p>按前缀筛选音色。</p><p><strong>page_index</strong> <code>integer</code>（可选）</p><p>页码索引。</p><p><strong>page_size</strong> <code>integer</code>（可选）</p><p>每页包含数据条数。</p></div></section></td><td><p>以下为华北2（北京）地域的配置，调用时请将&quot;{WorkspaceId}&quot;替换为真实的业务空间ID，各地域的配置不同。</p><a id="fig-code-group-3"></a><div><a id="fig-code-group-3-qwen-audio-tts-cosyvoice-tab"></a>Qwen-Audio-TTS/CosyVoice<div><a id="code-code-group-3-qwen-audio-tts-cosyvoice"></a><pre class="language-bash"><code>curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/customization \
-H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
-H &quot;Content-Type: application/json&quot; \
-d '{
    &quot;model&quot;: &quot;voice-enrollment&quot;,
    &quot;input&quot;: {
        &quot;action&quot;: &quot;list_voice&quot;,
        &quot;prefix&quot;: &quot;myvoice&quot;,
        &quot;page_size&quot;: 10,
        &quot;page_index&quot;: 0
    }
}'
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="vd-h3-ls-rs"></a><h3>返回体</h3><p><strong>request_id</strong><code>string</code></p><p>本次调用的唯一标识符。</p><p><strong>output</strong><code>object</code></p><p>模型返回的数据。</p><a id="accordion-属性-7"></a><section><p>属性</p><div><p><strong>voice_list</strong><code>array[object]</code></p><p>查询到的音色列表。</p><a id="accordion-属性-8"></a><section><p>属性</p><div><p><strong>voice_id</strong><code>string</code></p><p>音色 ID，可用于语音合成接口的 <code>voice</code> 参数。</p><p><strong>gmt_create</strong><code>string</code></p><p>创建时间。</p><p><strong>gmt_modified</strong><code>string</code></p><p>修改时间。</p><p><strong>status</strong><code>string</code></p><div><div><p><strong>重要</strong>仅Qwen-Audio-TTS/CosyVoice返回。</p></div></div><p>音色状态，取值参见&quot;音色状态说明&quot;。</p><p><strong>voice_prompt</strong><code>string</code></p><p>声音描述文本。</p><p><strong>preview_text</strong><code>string</code></p><p>预览音频文本。</p></div></section></div></section><p><strong>usage</strong><code>object</code></p><p>本次请求用量信息。</p><a id="accordion-属性-9"></a><section><p>属性</p><div><p><strong>count</strong> <code>integer</code></p><p>固定为 1。</p></div></section></td><td><a id="fig-code-group-4"></a><div><a id="fig-code-group-4-qwen-audio-tts-cosyvoice-tab"></a>Qwen-Audio-TTS/CosyVoice<div><a id="code-code-group-4-qwen-audio-tts-cosyvoice"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
        &quot;voice_list&quot;: [
            {
                &quot;voice_id&quot;: &quot;cosyvoice-v3.5-plus-vd-announcer-xxxxxx&quot;,
                &quot;gmt_create&quot;: &quot;2025-12-10 14:54:09&quot;,
                &quot;gmt_modified&quot;: &quot;2025-12-10 17:47:48&quot;,
                &quot;status&quot;: &quot;OK&quot;,
                &quot;voice_prompt&quot;: &quot;沉稳的中年男性播音员&quot;,
                &quot;preview_text&quot;: &quot;各位听众朋友们，大家好&quot;
            }
        ]
    },
    &quot;usage&quot;: {
        &quot;count&quot;: 1
    },
    &quot;request_id&quot;: &quot;xxxx-xxxx-xxxx&quot;
}
</code></pre></div></div></td></tr></tbody></table>

<a id="查询音色详情"></a>

<a id="vd-h2-query"></a>

## 查询音色详情

<table><tbody><tr><td><a id="vd-h3-qr-rq"></a><h3>请求体</h3><p><strong>model</strong><code>string</code><strong>（必选）</strong></p><p>声音设计模型。取值：</p><ul><li><code>voice-enrollment</code>：Qwen-Audio-TTS/CosyVoice声音设计。</li></ul><p><strong>input</strong><code>object</code><strong>（必选）</strong></p><p>输入参数对象。</p><a id="accordion-属性-10"></a><section><p>属性</p><div><p><strong>action</strong> <code>string</code><strong>（必选）</strong></p><p>固定为 <code>query_voice</code>。</p><p><strong>voice_id</strong> <code>string</code><strong>（必选）</strong></p><div><div><p><strong>重要</strong>仅适用于Qwen-Audio-TTS/CosyVoice。</p></div></div><p>要查询的音色ID。</p></div></section></td><td><p>以下为华北2（北京）地域的配置，调用时请将&quot;{WorkspaceId}&quot;替换为真实的业务空间ID，各地域的配置不同。</p><a id="fig-code-group-5"></a><div><a id="fig-code-group-5-qwen-audio-tts-cosyvoice-tab"></a>Qwen-Audio-TTS/CosyVoice<div><a id="code-code-group-5-qwen-audio-tts-cosyvoice"></a><pre class="language-bash"><code>curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/customization \
-H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
-H &quot;Content-Type: application/json&quot; \
-d '{
    &quot;model&quot;: &quot;voice-enrollment&quot;,
    &quot;input&quot;: {
        &quot;action&quot;: &quot;query_voice&quot;,
        &quot;voice_id&quot;: &quot;yourVoiceId&quot;
    }
}'
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="vd-h3-qr-rs"></a><h3>返回体</h3><p><strong>request_id</strong><code>string</code></p><p>本次调用的唯一标识符。</p><p><strong>output</strong><code>object</code></p><p>模型返回的数据。</p><a id="accordion-属性-11"></a><section><p>属性</p><div><p><strong>voice_id</strong><code>string</code></p><p>音色 ID，可用于语音合成接口的 <code>voice</code> 参数。</p><p><strong>gmt_create</strong><code>string</code></p><p>创建时间。</p><p><strong>gmt_modified</strong><code>string</code></p><p>修改时间。</p><p><strong>status</strong><code>string</code></p><div><div><p><strong>重要</strong>仅Qwen-Audio-TTS/CosyVoice返回。</p></div></div><p>音色状态，取值参见&quot;音色状态说明&quot;。</p><p><strong>target_model</strong><code>string</code></p><p>驱动音色的语音合成模型。</p><p><strong>voice_prompt</strong><code>string</code></p><div><div><p><strong>重要</strong>仅Qwen-Audio-TTS/CosyVoice声音设计返回。</p></div></div><p>声音描述文本。</p><p><strong>preview_text</strong><code>string</code></p><div><div><p><strong>重要</strong>仅Qwen-Audio-TTS/CosyVoice声音设计返回。</p></div></div><p>预览音频文本。</p></div></section><p><strong>usage</strong><code>object</code></p><p>本次请求用量信息。</p><a id="accordion-属性-12"></a><section><p>属性</p><div><p><strong>count</strong> <code>integer</code></p><p>固定为1。</p></div></section></td><td><a id="fig-code-group-6"></a><div><a id="fig-code-group-6-qwen-audio-tts-cosyvoice声音设计-tab"></a>Qwen-Audio-TTS/CosyVoice声音设计<div><a id="code-code-group-6-qwen-audio-tts-cosyvoice声音设计"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
        &quot;voice_id&quot;: &quot;cosyvoice-v3.5-plus-vd-announcer-xxxxxx&quot;,
        &quot;gmt_create&quot;: &quot;2025-12-10 14:54:09&quot;,
        &quot;gmt_modified&quot;: &quot;2025-12-10 17:47:48&quot;,
        &quot;preview_text&quot;: &quot;各位听众朋友们，大家好&quot;,
        &quot;target_model&quot;: &quot;cosyvoice-v3.5-plus&quot;,
        &quot;status&quot;: &quot;OK&quot;,
        &quot;voice_prompt&quot;: &quot;沉稳的中年男性播音员，音色低沉浑厚&quot;
    },
    &quot;usage&quot;: {
        &quot;count&quot;: 1
    },
    &quot;request_id&quot;: &quot;xxxx-xxxx-xxxx&quot;
}
</code></pre></div></div></td></tr></tbody></table>

<a id="删除音色"></a>

<a id="vd-h2-delete"></a>

## 删除音色

<table><tbody><tr><td><a id="vd-h3-dl-rq"></a><h3>请求体</h3><p><strong>model</strong><code>string</code><strong>（必选）</strong></p><p>声音设计模型。取值：</p><ul><li><code>voice-enrollment</code>：Qwen-Audio-TTS/CosyVoice声音设计。</li></ul><p><strong>input</strong><code>object</code><strong>（必选）</strong></p><p>输入参数对象。</p><a id="accordion-属性-13"></a><section><p>属性</p><div><p><strong>action</strong> <code>string</code><strong>（必选）</strong></p><p>固定为 <code>delete_voice</code>。</p><p><strong>voice_id</strong> <code>string</code><strong>（必选）</strong></p><div><div><p><strong>重要</strong>仅适用于Qwen-Audio-TTS/CosyVoice。</p></div></div><p>要删除的音色ID。</p></div></section></td><td><p>以下为华北2（北京）地域的配置，调用时请将&quot;{WorkspaceId}&quot;替换为真实的业务空间ID，各地域的配置不同。</p><a id="fig-code-group-7"></a><div><a id="fig-code-group-7-qwen-audio-tts-cosyvoice-tab"></a>Qwen-Audio-TTS/CosyVoice<div><a id="code-code-group-7-qwen-audio-tts-cosyvoice"></a><pre class="language-bash"><code>curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/customization \
-H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
-H &quot;Content-Type: application/json&quot; \
-d '{
    &quot;model&quot;: &quot;voice-enrollment&quot;,
    &quot;input&quot;: {
        &quot;action&quot;: &quot;delete_voice&quot;,
        &quot;voice_id&quot;: &quot;yourVoiceId&quot;
    }
}'
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="vd-h3-dl-rs"></a><h3>返回体</h3><p><strong>request_id</strong><code>string</code></p><p>本次调用的唯一标识符。</p><p><strong>output</strong><code>object</code></p><p>模型返回的数据，为空对象。</p><p><strong>usage</strong><code>object</code></p><p>本次请求用量信息。</p><a id="accordion-属性-14"></a><section><p>属性</p><div><p><strong>count</strong> <code>integer</code></p><p>固定为1。</p></div></section></td><td><a id="fig-code-group-8"></a><div><a id="fig-code-group-8-qwen-audio-tts-cosyvoice-tab"></a>Qwen-Audio-TTS/CosyVoice<div><a id="code-code-group-8-qwen-audio-tts-cosyvoice"></a><pre class="language-json"><code>{
    &quot;output&quot;: {},
    &quot;usage&quot;: {
        &quot;count&quot;: 1
    },
    &quot;request_id&quot;: &quot;xxxx-xxxx-xxxx&quot;
}
</code></pre></div></div></td></tr></tbody></table>

<a id="音色状态说明"></a>

<a id="vd-h2-status"></a>

## 音色状态说明

音色创建后会经过审核流程。以下状态适用于 Qwen-Audio-TTS/CosyVoice（`model` 为 `voice-enrollment`）。

| 状态 | 说明 |
| --- | --- |
| DEPLOYING | 审核中/处理中。 |
| OK | 审核通过，可正常使用。 |
| UNDEPLOYED | 审核未通过，不可使用。 |
