# 实时语音识别（Qwen-ASR-Realtime）服务端事件

本文档介绍在与 Qwen-ASR Realtime API 的 WebSocket 会话中，服务端向客户端发送的事件。

**用户指南：**模型介绍、功能特性和完整示例代码请参见[实时语音识别](../model-user-guide/model-experience/speech-and-audio/speech-recognition/real-time-speech-recognition-user-guide.md)

<a id="error"></a>

<a id="af43722339yva"></a>

## error

当服务端检测到错误（包括客户端错误和服务端错误）时，向客户端发送的事件。

<table><tbody><tr><td><table><thead><tr><th><p><strong>参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td><p>type</p></td><td><p>string</p></td><td><p>事件类型。固定为<code>error</code>。</p></td></tr><tr><td><p>event_id</p></td><td><p>string</p></td><td><p>事件ID。</p></td></tr><tr><td><p>error.type</p></td><td><p>string</p></td><td><p>错误类型。</p></td></tr><tr><td><p>error.code</p></td><td><p>string</p></td><td><p>错误代码。</p></td></tr><tr><td><p>error.message</p></td><td><p>string</p></td><td><p>具体的报错信息。请按<a href="../model-api-reference/preparations/error-code.md">错误码</a>所示的解决方案进行处理。</p></td></tr><tr><td><p>error.param</p></td><td><p>string</p></td><td><p>与错误相关的参数。</p></td></tr><tr><td><p>error.event_id</p></td><td><p>string</p></td><td><p>与错误相关的事件ID。</p></td></tr></tbody></table></td><td><a id="code-block"></a><pre class="language-json"><code>{
  &quot;event_id&quot;: &quot;event_B2uoU7VOt1AAITsPRPH9n&quot;,
  &quot;type&quot;: &quot;error&quot;,
  &quot;error&quot;: {
    &quot;type&quot;: &quot;invalid_request_error&quot;,
    &quot;code&quot;: &quot;invalid_value&quot;,
    &quot;message&quot;: &quot;Invalid value: 'whisper-1xx'. Supported values are: 'whisper-1'.&quot;,
    &quot;param&quot;: &quot;session.input_audio_transcription.model&quot;,
    &quot;event_id&quot;: &quot;event_123&quot;
  }
}
</code></pre></td></tr></tbody></table>

<a id="session-created"></a>

<a id="2c04b24bc3wlo"></a>

## session.created

当客户端成功连接到服务端后，服务端响应的第一个事件。该事件包含服务端为此次连接设置的默认配置信息。

<table><tbody><tr><td><table><thead><tr><th><p><strong>参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td><p>type</p></td><td><p>string</p></td><td><p>事件类型。固定为<code>session.created</code>。</p></td></tr><tr><td><p>event_id</p></td><td><p>string</p></td><td><p>事件ID。</p></td></tr><tr><td><p>session.id</p></td><td><p>string</p></td><td><p>本次 WebSocket 会话的ID。</p></td></tr><tr><td><p>session.object</p></td><td><p>string</p></td><td><p>固定为<code>realtime.session</code>。</p></td></tr><tr><td><p>session.model</p></td><td><p>string</p></td><td><p>当前调用的<a href="../model-user-guide/model-experience/speech-and-audio/speech-recognition/real-time-speech-recognition-user-guide.md">模型</a>名称。</p></td></tr><tr><td><p>session.modalities</p></td><td><p>array[string]</p></td><td><p>模型输出模态，固定为<code>[&quot;text&quot;]</code>。</p></td></tr><tr><td><p>session.input_audio_format</p></td><td><p>string</p></td><td><p>输入音频格式。</p></td></tr><tr><td><p>session.input_audio_transcription</p></td><td><p>object</p></td><td><p>语音识别相关配置参数。详情参见客户端<a href="qwen-asr-realtime-client-events-1496b1c0718012d4.md#af43722339yva">session.update</a>事件<code>input_audio_transcription</code>参数。</p></td></tr><tr><td><p>session.turn_detection</p></td><td><p>object</p></td><td><p>VAD（Voice Activity Detection，语音活动检测）配置。</p></td></tr><tr><td><p>session.turn_detection.type</p></td><td><p>string</p></td><td><p>固定为<code>server_vad</code>。</p></td></tr><tr><td><p>session.turn_detection.threshold</p></td><td><p>float</p></td><td><p>VAD检测阈值。</p></td></tr><tr><td><p>session.turn_detection.silence_duration_ms</p></td><td><p>integer</p></td><td><p>VAD断句检测阈值（ms）。</p></td></tr></tbody></table></td><td><a id="code-block-2"></a><pre class="language-json"><code>{
    &quot;event_id&quot;: &quot;event_1234&quot;,
    &quot;type&quot;: &quot;session.created&quot;,
    &quot;session&quot;: {
        &quot;id&quot;: &quot;sess_001&quot;,
        &quot;object&quot;: &quot;realtime.session&quot;,
        &quot;model&quot;: &quot;qwen3-asr-flash-realtime&quot;,
        &quot;modalities&quot;: [&quot;text&quot;],
        &quot;input_audio_format&quot;: &quot;pcm16&quot;,
        &quot;input_audio_transcription&quot;: null,
        &quot;turn_detection&quot;: {
            &quot;type&quot;: &quot;server_vad&quot;,
            &quot;threshold&quot;: 0.5,
            &quot;silence_duration_ms&quot;: 200
        }
    }
}
</code></pre></td></tr></tbody></table>

<a id="session-updated"></a>

<a id="4d6ed9dd62vmj"></a>

## session.updated

当客户端发送[session.update](qwen-asr-realtime-client-events-1496b1c0718012d4.md#af43722339yva)事件并成功被服务端处理后，服务端将发送该事件。如果处理过程中出现错误，则直接发送 error 事件。

<table><tbody><tr><td><table><thead><tr><th><p><strong>参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td><p>type</p></td><td><p>string</p></td><td><p>事件类型。固定为<code>session.updated</code>。</p></td></tr></tbody></table><p>其他参数含义同<a href="qwen-asr-realtime-server-events-5dc40b9e8a313c98.md#2c04b24bc3wlo">session.created</a>。</p></td><td><a id="code-block-3"></a><pre class="language-json"><code>{
    &quot;event_id&quot;: &quot;event_1234&quot;,
    &quot;type&quot;: &quot;session.updated&quot;,
    &quot;session&quot;: {
        &quot;id&quot;: &quot;sess_001&quot;,
        &quot;object&quot;: &quot;realtime.session&quot;,
        &quot;model&quot;: &quot;gpt-4o-realtime-preview-2024-12-17&quot;,
        &quot;modalities&quot;: [&quot;text&quot;],
        &quot;input_audio_format&quot;: &quot;pcm16&quot;,
        &quot;input_audio_transcription&quot;: null,
        &quot;turn_detection&quot;: {
            &quot;type&quot;: &quot;server_vad&quot;,
            &quot;threshold&quot;: 0.5,
            &quot;silence_duration_ms&quot;: 200
        }
    }
}
</code></pre></td></tr></tbody></table>

<a id="input-audio-buffer-speech-started"></a>

<a id="038d846199nbm"></a>

## input\_audio\_buffer.speech\_started

此事件仅在 VAD 模式下发送。当服务端在音频缓冲区中检测到语音开始时发送。

该事件可能在每次音频添加到缓冲区时发生（除非已检测到语音开始）。

<table><tbody><tr><td><table><thead><tr><th><p><strong>参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td><p>type</p></td><td><p>string</p></td><td><p>事件类型。固定为<code>input_audio_buffer.speech_started</code>。</p></td></tr><tr><td><p>event_id</p></td><td><p>string</p></td><td><p>事件ID。</p></td></tr><tr><td><p>audio_start_ms</p></td><td><p>integer</p></td><td><p>在会话期间，从音频开始写入缓冲区到首次检测到语音时的毫秒数。</p></td></tr><tr><td><p>item_id</p></td><td><p>string</p></td><td><p>将创建的用户消息项的 ID。</p></td></tr></tbody></table></td><td><a id="code-block-4"></a><pre class="language-json"><code>{
  &quot;event_id&quot;: &quot;event_B1lV7FPbgTv9qGxPI1tH4&quot;,
  &quot;type&quot;: &quot;input_audio_buffer.speech_started&quot;,
  &quot;audio_start_ms&quot;: 64,
  &quot;item_id&quot;: &quot;item_B1lV7jWLscp4mMV8hSs8c&quot;
}
</code></pre></td></tr></tbody></table>

<a id="input-audio-buffer-speech-stopped"></a>

<a id="3d73b074cak7k"></a>

## input\_audio\_buffer.speech\_stopped

此事件仅在 VAD 模式下发送。当服务端在音频缓冲区中检测到语音结束时发送。

该事件触发后，服务端将紧接着发送一个[conversation.item.created](qwen-asr-realtime-server-events-5dc40b9e8a313c98.md#04dabbb9b6eto)事件，包含从音频缓冲区创建的用户消息项。

<table><tbody><tr><td><table><thead><tr><th><p><strong>参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td><p>type</p></td><td><p>string</p></td><td><p>事件类型。固定为<code>input_audio_buffer.speech_stopped</code>。</p></td></tr><tr><td><p>event_id</p></td><td><p>string</p></td><td><p>事件ID。</p></td></tr><tr><td><p>audio_end_ms</p></td><td><p>integer</p></td><td><p>从会话开始到语音停止的毫秒数。</p></td></tr><tr><td><p>item_id</p></td><td><p>string</p></td><td><p>当语音停止时将创建的用户消息项的 ID。</p></td></tr></tbody></table></td><td><a id="code-block-5"></a><pre class="language-json"><code>{
  &quot;event_id&quot;: &quot;event_B3GGEYh2orwNIdhUagZPz&quot;,
  &quot;type&quot;: &quot;input_audio_buffer.speech_stopped&quot;,
  &quot;audio_end_ms&quot;: 28128,
  &quot;item_id&quot;: &quot;item_B3GGE8ry4yqbqJGzrVhEM&quot;
}
</code></pre></td></tr></tbody></table>

<a id="input-audio-buffer-committed"></a>

<a id="1108a3764an0e"></a>

## input\_audio\_buffer.committed

-   **VAD模式：**当客户端完成音频数据发送（通过[input\_audio\_buffer.append](qwen-asr-realtime-client-events-1496b1c0718012d4.md#a42f8e9111n72)事件）后，服务端发送该事件。
-   **非VAD模式：**客户端完成音频数据发送（通过[input\_audio\_buffer.append](qwen-asr-realtime-client-events-1496b1c0718012d4.md#a42f8e9111n72)事件）并发送[input\_audio\_buffer.commit](qwen-asr-realtime-client-events-1496b1c0718012d4.md#d6d5cd90f3q4c)事件后，服务端发送该事件。

<table><tbody><tr><td><table><thead><tr><th><p><strong>参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td><p>type</p></td><td><p>string</p></td><td><p>事件类型。固定为<code>input_audio_buffer.committed</code>。</p></td></tr><tr><td><p>event_id</p></td><td><p>string</p></td><td><p>事件ID。</p></td></tr><tr><td><p>previous_item_id</p></td><td><p>string</p></td><td><p>前一个对话项的ID</p></td></tr><tr><td><p>item_id</p></td><td><p>string</p></td><td><p>将创建的用户对话项的 ID。</p></td></tr></tbody></table></td><td><a id="code-block-6"></a><pre class="language-json"><code>{
    &quot;event_id&quot;: &quot;event_1121&quot;,
    &quot;type&quot;: &quot;input_audio_buffer.committed&quot;,
    &quot;previous_item_id&quot;: &quot;msg_001&quot;,
    &quot;item_id&quot;: &quot;msg_002&quot;
}
</code></pre></td></tr></tbody></table>

<a id="conversation-item-created"></a>

<a id="04dabbb9b6eto"></a>

## conversation.item.created

当对话项（item）创建时发送该事件。

<table><tbody><tr><td><table><thead><tr><th><p><strong>参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td><p>type</p></td><td><p>string</p></td><td><p>事件类型。固定为<code>conversation.item.created</code>。</p></td></tr><tr><td><p>event_id</p></td><td><p>string</p></td><td><p>事件ID。</p></td></tr><tr><td><p>previous_item_id</p></td><td><p>string</p></td><td><p>前一个对话项的ID</p></td></tr><tr><td><p>item</p></td><td><p>object</p></td><td><p>要添加到对话中的条目。</p></td></tr><tr><td><p>item.id</p></td><td><p>string</p></td><td><p>对话项的唯一ID。</p></td></tr><tr><td><p>item.object</p></td><td><p>string</p></td><td><p>固定为 <code>realtime.item</code> 。</p></td></tr><tr><td><p>item.type</p></td><td><p>string</p></td><td><p>固定为<code>message</code>。</p></td></tr><tr><td><p>item.status</p></td><td><p>string</p></td><td><p>对话项的状态。</p></td></tr><tr><td><p>item.role</p></td><td><p>string</p></td><td><p>消息发送的角色。</p></td></tr><tr><td><p>item.content</p></td><td><p>array[object]</p></td><td><p>消息的内容。</p></td></tr><tr><td><p>item.content.type</p></td><td><p>string</p></td><td><p>固定为<code>input_audio</code>。</p></td></tr><tr><td><p>item.content.transcript</p></td><td><p>string</p></td><td><p>固定为<code>null</code>。完整的识别结果通过<a href="qwen-asr-realtime-server-events-5dc40b9e8a313c98.md#403ecacd74qqg">conversation.item.input_audio_transcription.completed</a>事件提供。</p></td></tr></tbody></table></td><td><a id="code-block-7"></a><pre class="language-json"><code>{
  &quot;type&quot;: &quot;conversation.item.created&quot;,
  &quot;event_id&quot;: &quot;event_B3GGKbCfBZTpqFHZ0P8vg&quot;,
  &quot;previous_item_id&quot;: &quot;item_B3GGE8ry4yqbqJGzrVhEM&quot;,
  &quot;item&quot;: {
    &quot;id&quot;: &quot;item_B3GGEPlolCqdMiVbYIf5L&quot;,
    &quot;object&quot;: &quot;realtime.item&quot;,
    &quot;type&quot;: &quot;message&quot;,
    &quot;status&quot;: &quot;completed&quot;,
    &quot;role&quot;: &quot;user&quot;,
    &quot;content&quot;: [
      {
        &quot;type&quot;: &quot;input_audio&quot;,
        &quot;transcript&quot;: null
      }
    ]
  }
}
</code></pre></td></tr></tbody></table>

<a id="conversation-item-input-audio-transcription-text"></a>

<a id="ba1b5cdd79fxu"></a>

## conversation.item.input\_audio\_transcription.text

此事件会高频发送，用于展示实时识别结果。

<table><tbody><tr><td><table><thead><tr><th><p><strong>参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td><p>type</p></td><td><p>string</p></td><td><p>事件类型。固定为<code>conversation.item.input_audio_transcription.text</code>。</p></td></tr><tr><td><p>event_id</p></td><td><p>string</p></td><td><p>事件ID。</p></td></tr><tr><td><p>item_id</p></td><td><p>string</p></td><td><p>关联的对话项ID。</p></td></tr><tr><td><p>content_index</p></td><td><p>integer</p></td><td><p>包含音频的内容部分的索引。</p></td></tr><tr><td><p>language</p></td><td><p>string</p></td><td><div><p>被识别音频的语种。当请求参数<code>language</code>已指定语种时，该值与所指定的参数一致。</p><p>可能的值如下：</p><div><ul><li><p>zh：中文（普通话、四川话、闽南语、吴语）</p></li><li><p>yue：粤语</p></li><li><p>en：英文</p></li><li><p>ja：日语</p></li><li><p>de：德语</p></li><li><p>ko：韩语</p></li><li><p>ru：俄语</p></li><li><p>fr：法语</p></li><li><p>pt：葡萄牙语</p></li><li><p>ar：阿拉伯语</p></li><li><p>it：意大利语</p></li><li><p>es：西班牙语</p></li><li><p>hi：印地语</p></li><li><p>id：印尼语</p></li><li><p>th：泰语</p></li><li><p>tr：土耳其语</p></li><li><p>uk：乌克兰语</p></li><li><p>vi：越南语</p></li></ul></div></div></td></tr><tr><td><p>emotion</p></td><td><p>string</p></td><td><p>情感识别固定开启，无需额外配置。</p><div><p>被识别音频的情感。支持的情感如下：</p><ul><li><p><code>surprised</code>：惊讶</p></li><li><p><code>neutral</code>：平静</p></li><li><p><code>happy</code>：愉快</p></li><li><p><code>sad</code>：悲伤</p></li><li><p><code>disgusted</code>：厌恶</p></li><li><p><code>angry</code>：愤怒</p></li><li><p><code>fearful</code>：恐惧</p></li></ul></div></td></tr><tr><td><p>text</p></td><td><p>string</p></td><td><p>已确认的文本前缀。这是当前句子中，模型已确认不会再变更的部分。</p></td></tr><tr><td><p>stash</p></td><td><p>string</p></td><td><p>预识别的文本后缀。这是紧跟在已确认部分之后，模型仍在处理、可能会被修正的临时草稿。</p></td></tr></tbody></table></td><td><a id="code-block-8"></a><pre class="language-json"><code>{
  &quot;event_id&quot;: &quot;event_R7Pfu8QVBfP5HmpcbEFSd&quot;,
  &quot;type&quot;: &quot;conversation.item.input_audio_transcription.text&quot;,
  &quot;item_id&quot;: &quot;item_MpJQPNQzqVRc9aC9zMwSj&quot;,
  &quot;content_index&quot;: 0,
  &quot;language&quot;: &quot;zh&quot;,
  &quot;emotion&quot;: &quot;neutral&quot;,
  &quot;text&quot;: &quot;&quot;,
  &quot;stash&quot;: &quot;北京的&quot;
}
</code></pre><p>在任何时刻，要获取当前最完整的句子预览，都需要将这两个字段拼接起来：实时预览句子 = <code>text</code> + <code>stash</code>。</p><a id="accordion-点击查看示例"></a><section><p>点击查看示例</p><div><p>假设用户正在说：“今天天气不错，阳光明媚。”</p><p>以下是您可能会收到的事件流以及如何解读它们：</p><table><thead><tr><th><p><strong>时间点</strong></p></th><th><p><strong>用户说话进度</strong></p></th><th><p><strong>API 响应 (text 和 stash)</strong></p></th><th><p><strong>客户端 UI 应显示 (text + stash)</strong></p></th></tr></thead><tbody><tr><td><p>T1</p></td><td><p>“今天……”</p></td><td><p>text: &quot;&quot;</p><p>stash: &quot;今天&quot;</p></td><td><p>今天</p></td></tr><tr><td><p>T2</p></td><td><p>“……天气……”</p></td><td><p>text: &quot;&quot;</p><p>stash: &quot;今天天气&quot;</p></td><td><p>今天天气</p></td></tr><tr><td><p>T3</p></td><td><p>“……不错”</p></td><td><p>text: &quot;今天&quot;</p><p>stash: &quot;天气不错&quot;</p></td><td><p>今天天气不错</p><p>（注意，“今天”已被确认并移入text）</p></td></tr><tr><td><p>T4</p></td><td><p>（短暂停顿）</p></td><td><p>text: &quot;今天天气不错，&quot;</p><p>stash: &quot;&quot;</p></td><td><p>今天天气不错，</p><p>（前半句完全确认）</p></td></tr><tr><td><p>T5</p></td><td><p>“……阳光……”</p></td><td><p>text: &quot;今天天气不错，&quot;</p><p>stash: &quot;阳光&quot;</p></td><td><p>今天天气不错，阳光</p></td></tr><tr><td><p>T6</p></td><td><p>“……明媚。”</p></td><td><p>text: &quot;今天天气不错，&quot;</p><p>stash: &quot;阳光明媚。&quot;</p></td><td><p>今天天气不错，阳光明媚。</p></td></tr><tr><td><p>T7</p></td><td><p>（结束说话）</p></td><td><p>-</p></td><td><p>使用<a href="qwen-asr-realtime-server-events-5dc40b9e8a313c98.md#403ecacd74qqg">conversation.item.input_audio_transcription.completed</a>的transcript的内容作为最终结果。</p></td></tr></tbody></table></div></section></td></tr></tbody></table>

<a id="conversation-item-input-audio-transcription-completed"></a>

<a id="403ecacd74qqg"></a>

## conversation.item.input\_audio\_transcription.completed

向客户端发送最终识别结果。此事件标志着一个对话项（item）的结束。

<table><tbody><tr><td><table><thead><tr><th><p><strong>参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td><p>type</p></td><td><p>string</p></td><td><p>事件类型。固定为<code>conversation.item.input_audio_transcription.completed</code>。</p></td></tr><tr><td><p>event_id</p></td><td><p>string</p></td><td><p>事件ID。</p></td></tr><tr><td><p>item_id</p></td><td><p>string</p></td><td><p>关联的对话项ID。</p></td></tr><tr><td><p>content_index</p></td><td><p>integer</p></td><td><p>包含音频的内容部分的索引。</p></td></tr><tr><td><p>language</p></td><td><p>string</p></td><td><div><p>被识别音频的语种。当请求参数<code>language</code>已指定语种时，该值与所指定的参数一致。</p><p>可能的值如下：</p><div><ul><li><p>zh：中文（普通话、四川话、闽南语、吴语）</p></li><li><p>yue：粤语</p></li><li><p>en：英文</p></li><li><p>ja：日语</p></li><li><p>de：德语</p></li><li><p>ko：韩语</p></li><li><p>ru：俄语</p></li><li><p>fr：法语</p></li><li><p>pt：葡萄牙语</p></li><li><p>ar：阿拉伯语</p></li><li><p>it：意大利语</p></li><li><p>es：西班牙语</p></li><li><p>hi：印地语</p></li><li><p>id：印尼语</p></li><li><p>th：泰语</p></li><li><p>tr：土耳其语</p></li><li><p>uk：乌克兰语</p></li><li><p>vi：越南语</p></li></ul></div></div></td></tr><tr><td><p>emotion</p></td><td><p>string</p></td><td><p>情感识别固定开启，无需额外配置。</p><div><p>被识别音频的情感。支持的情感如下：</p><ul><li><p><code>surprised</code>：惊讶</p></li><li><p><code>neutral</code>：平静</p></li><li><p><code>happy</code>：愉快</p></li><li><p><code>sad</code>：悲伤</p></li><li><p><code>disgusted</code>：厌恶</p></li><li><p><code>angry</code>：愤怒</p></li><li><p><code>fearful</code>：恐惧</p></li></ul></div></td></tr><tr><td><p>transcript</p></td><td><p>string</p></td><td><p>识别结果。</p></td></tr></tbody></table></td><td><a id="code-block-9"></a><pre class="language-json"><code>{
  &quot;event_id&quot;: &quot;event_B3GGEjPT2sLzjBM74W6kB&quot;,
  &quot;type&quot;: &quot;conversation.item.input_audio_transcription.completed&quot;,
  &quot;item_id&quot;: &quot;item_B3GGC53jGOuIFcjZkmEQ9&quot;,
  &quot;content_index&quot;: 0,
  &quot;language&quot;: &quot;zh&quot;,
  &quot;emotion&quot;: &quot;neutral&quot;,
  &quot;transcript&quot;: &quot;今天天气怎么样&quot;
}
</code></pre></td></tr></tbody></table>

<a id="conversation-item-input-audio-transcription-failed"></a>

<a id="09bf7fb06aear"></a>

## conversation.item.input\_audio\_transcription.failed

当输入了音频但是识别失败时，服务端发送该事件。与其他 `error` 事件分开处理，便于客户端识别相关的具体项目。

<table><tbody><tr><td><table><thead><tr><th><p><strong>参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td><p>type</p></td><td><p>string</p></td><td><p>事件类型。固定为<code>conversation.item.input_audio_transcription.failed</code>。</p></td></tr><tr><td><p>item_id</p></td><td><p>string</p></td><td><p>关联的对话项ID。</p></td></tr><tr><td><p>content_index</p></td><td><p>integer</p></td><td><p>包含音频的内容部分的索引。</p></td></tr><tr><td><p>error.code</p></td><td><p>string</p></td><td><p>错误代码。</p></td></tr><tr><td><p>error.message</p></td><td><p>string</p></td><td><p>错误消息。</p></td></tr><tr><td><p>error.param</p></td><td><p>string</p></td><td><p>错误相关的参数。</p></td></tr></tbody></table></td><td><a id="code-block-10"></a><pre class="language-json"><code>{
  &quot;type&quot;: &quot;conversation.item.input_audio_transcription.failed&quot;,
  &quot;item_id&quot;: &quot;&lt;item_id&gt;&quot;,
  &quot;content_index&quot;: 0,
  &quot;error&quot;: {
    &quot;code&quot;: &quot;&lt;code&gt;&quot;,
    &quot;message&quot;: &quot;&lt;message&gt;&quot;,
    &quot;param&quot;: &quot;&lt;param&gt;&quot;
  }
}
</code></pre></td></tr></tbody></table>

<a id="session-finished"></a>

<a id="6eaa77339djdv"></a>

## session.finished

会话结束事件，表示当前会话中，所有音频识别已完成。

该事件只有在客户端发送`session.finish`后才会发送，客户端接收到该事件后可主动断开连接。

<table><tbody><tr><td><table><thead><tr><th><p><strong>参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td><p>type</p></td><td><p>string</p></td><td><p>事件类型。固定为<code>session.finished</code>。</p></td></tr><tr><td><p>event_id</p></td><td><p>string</p></td><td><p>事件ID。</p></td></tr></tbody></table></td><td><a id="code-block-11"></a><pre class="language-json"><code>{
  &quot;event_id&quot;: &quot;event_2239&quot;,
  &quot;type&quot;: &quot;session.finished&quot;
}
</code></pre></td></tr></tbody></table>
