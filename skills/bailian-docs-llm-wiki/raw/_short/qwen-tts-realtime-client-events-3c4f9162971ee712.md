# 客户端事件

本文介绍 Qwen-TTS Realtime API 的客户端事件。

> 相关文档：[实时语音合成](../model-user-guide/model-experience/speech-and-audio/speech-synthesis/realtime-tts-user-guide.md)。

<a id="session-update"></a>

<a id="a5065ac8c1psu"></a>

## session.update

用于更新会话配置。在WebSocket连接建立成功后，可立即发送此事件作为交互的第一步。如果未发送，系统将使用默认配置。服务端成功处理此事件后，会返回`session.updated`事件作为确认。

<table><tbody><tr><td><p><strong>event_id</strong><code>string</code><strong>（必选）</strong></p><p>客户端生成的唯一事件ID。在单次WebSocket连接会话中必须保持唯一。强烈建议使用 UUID（通用唯一标识符）。</p><p><strong>type</strong><code>string</code><strong>（必选）</strong></p><p>事件类型，固定为<code>session.update</code>。</p><p><strong>session</strong><code>object</code>（可选）</p><p>会话配置。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>voice</strong><code>string</code><strong>（必选）</strong></p><p>语音合成所使用的系统音色，参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-synthesis/realtime-tts-user-guide.md#bac280ddf5a1u">支持的音色</a>。</p><p><strong>mode</strong><code>string</code>（可选）</p><p>交互模式，可选值：</p><ul><li><code>server_commit</code>（默认）：服务端自动判断合成时机，平衡延迟与质量，推荐大多数场景使用</li><li><code>commit</code>：客户端手动触发合成，延迟最低，但需自行管理句子完整性</li></ul><p><strong>language_type</strong><code>string</code>（可选）</p><p>指定合成音频的语种，默认为 <code>Auto</code>。</p><ul><li><p><code>Auto</code>：适用无法确定文本的语种或文本包含多种语言的场景，模型会自动为文本中的不同语言片段匹配各自的发音，但无法保证发音完全精准。</p></li><li><p>指定语种：适用于文本为单一语种的场景，此时指定为具体语种，能显著提升合成质量，效果通常优于 <code>Auto</code>。可选值包括：</p><ul><li><code>Chinese</code></li><li><code>English</code></li><li><code>German</code></li><li><code>Italian</code></li><li><code>Portuguese</code></li><li><code>Spanish</code></li><li><code>Japanese</code></li><li><code>Korean</code></li><li><code>French</code></li><li><code>Russian</code></li></ul></li></ul><p><strong>response_format</strong><code>string</code>（可选）</p><p>模型输出音频的格式。</p><p>支持的格式：</p><ul><li><code>pcm</code>（默认）</li><li><code>wav</code></li><li><code>mp3</code></li><li><code>opus</code></li></ul><p><strong>sample_rate</strong><code>integer</code>（可选）</p><p>模型输出音频的采样率（Hz）。</p><p>支持的采样率：</p><ul><li>8000</li><li>16000</li><li>24000（默认）</li><li>48000</li></ul><p><strong>speech_rate</strong><code>float</code>（可选）</p><p>音频的语速。1.0为正常语速，小于1.0为慢速，大于1.0为快速。</p><p>默认值：1.0。</p><p>取值范围：[0.5, 2.0]。</p><p><strong>volume</strong><code>integer</code>（可选）</p><p>音频的音量。</p><p>默认值：50。</p><p>取值范围：[0, 100]。</p><p><strong>pitch_rate</strong><code>float</code>（可选）</p><p>合成音频的语调。</p><p>默认值：1.0。</p><p>取值范围：[0.5, 2.0]。</p><p><strong>bit_rate</strong><code>integer</code>（可选）</p><p>指定音频的<a href="https://opus-codec.org/">码率</a>（kbps）。码率越大，音质越好，音频文件体积越大。仅在音频格式（<code>response_format</code>）为<code>opus</code>时可用。</p><p>默认值：128。</p><p>取值范围：[6, 510]。</p></div></section></td><td><a id="code-block"></a><pre class="language-json"><code>{
    &quot;event_id&quot;: &quot;event_123&quot;,
    &quot;type&quot;: &quot;session.update&quot;,
    &quot;session&quot;: {
        &quot;voice&quot;: &quot;Cherry&quot;,
        &quot;mode&quot;: &quot;server_commit&quot;,
        &quot;language_type&quot;: &quot;Chinese&quot;,
        &quot;response_format&quot;: &quot;pcm&quot;,
        &quot;sample_rate&quot;: 24000
    }
}
</code></pre></td></tr></tbody></table>

<a id="input-text-buffer-append"></a>

<a id="37be8f579bxvj"></a>

## input\_text\_buffer.append

用于将待合成文本追加到文本缓冲区。在server\_commit模式中，文本将追加到服务端的文本缓冲区；在commit模式中，文本将追加到客户端的文本缓冲区。

<table><tbody><tr><td><p><strong>event_id</strong><code>string</code><strong>（必选）</strong></p><p>客户端生成的唯一事件ID。在单次WebSocket连接会话中必须保持唯一。强烈建议使用 UUID（通用唯一标识符）。</p><p><strong>type</strong><code>string</code><strong>（必选）</strong></p><p>事件类型，固定为<code>input_text_buffer.append</code>。</p><p><strong>text</strong><code>string</code><strong>（必选）</strong></p><p>待合成文本。</p></td><td><a id="code-block-2"></a><pre class="language-json"><code>{
  &quot;event_id&quot;: &quot;event_B4o9RHSTWobB5OQdEHLTo&quot;,
  &quot;type&quot;: &quot;input_text_buffer.append&quot;,
  &quot;text&quot;: &quot;您好，我是千问。&quot;
}
</code></pre></td></tr></tbody></table>

<a id="input-text-buffer-commit"></a>

<a id="63086fc329sib"></a>

## input\_text\_buffer.commit

用于提交用户输入文本缓冲区，从而在对话中创建新的用户消息项。 如果输入的文本缓冲区为空，此事件将产生错误。处于“server\_commit”模式时，用户提交此事件，表示立即合成之前的所有文本，服务器不再缓存文本。处于“commit”模式时，客户端必须提交文本缓冲区才能创建用户消息项。提交输入文本缓冲区不会从模型创建响应，服务器将返回 `input_text_buffer.committed` 事件进行响应。

<table><tbody><tr><td><p><strong>event_id</strong><code>string</code><strong>（必选）</strong></p><p>客户端生成的唯一事件ID。在单次WebSocket连接会话中必须保持唯一。强烈建议使用 UUID（通用唯一标识符）。</p><p><strong>type</strong><code>string</code><strong>（必选）</strong></p><p>事件类型，固定为<code>input_text_buffer.commit</code>。</p></td><td><a id="code-block-3"></a><pre class="language-json"><code>{
  &quot;event_id&quot;: &quot;event_B4o9RHSTWobB5OQdEHLTo&quot;,
  &quot;type&quot;: &quot;input_text_buffer.commit&quot;
}
</code></pre></td></tr></tbody></table>

<a id="input-text-buffer-clear"></a>

<a id="794b88b49ennz"></a>

## input\_text\_buffer.clear

用于清除缓冲区中的文本。服务端返回`input_text_buffer.cleared` 事件进行响应。

<table><tbody><tr><td><p><strong>event_id</strong><code>string</code><strong>（必选）</strong></p><p>客户端生成的唯一事件ID。在单次WebSocket连接会话中必须保持唯一。强烈建议使用 UUID（通用唯一标识符）。</p><p><strong>type</strong><code>string</code><strong>（必选）</strong></p><p>事件类型，固定为<code>input_text_buffer.clear</code>。</p></td><td><a id="code-block-4"></a><pre class="language-json"><code>{
  &quot;event_id&quot;: &quot;event_2728&quot;,
  &quot;type&quot;: &quot;input_text_buffer.clear&quot;
}
</code></pre></td></tr></tbody></table>

<a id="session-finish"></a>

<a id="53715b556bstd"></a>

## session.finish

客户端发送 `session.finish` 事件通知服务端不再有文本输入，服务端将剩余音频返回，随后关闭连接。

<table><tbody><tr><td><p><strong>event_id</strong><code>string</code><strong>（必选）</strong></p><p>客户端生成的唯一事件ID。在单次WebSocket连接会话中必须保持唯一。强烈建议使用 UUID（通用唯一标识符）。</p><p><strong>type</strong><code>string</code><strong>（必选）</strong></p><p>事件类型，固定为<code>session.finish</code>。</p></td><td><a id="code-block-5"></a><pre class="language-json"><code>{
  &quot;event_id&quot;: &quot;event_2239&quot;,
  &quot;type&quot;: &quot;session.finish&quot;
}
</code></pre></td></tr></tbody></table>
