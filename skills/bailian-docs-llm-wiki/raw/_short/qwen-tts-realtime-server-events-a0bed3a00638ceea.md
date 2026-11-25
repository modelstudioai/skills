# 服务端事件

本文介绍 Qwen-TTS-Realtime API 的服务端事件。

> 相关文档：[实时语音合成](../model-user-guide/model-experience/speech-and-audio/speech-synthesis/realtime-tts-user-guide.md)。

<a id="error"></a>

<a id="a5065ac8c1psu"></a>

## error

不论是遇到客户端错误还是服务端错误，服务端都会响应该事件。

<table><tbody><tr><td><p><strong>event_id</strong><code>string</code></p><p>服务端事件ID。</p><p><strong>type</strong><code>string</code></p><p>事件类型，固定为<code>error</code>。</p><p><strong>error</strong><code>object</code></p><p>错误详情。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>code</strong><em>string</em></p><p>错误码。</p><p><strong>message</strong><em>string</em></p><p>错误信息。</p></div></section></td><td><a id="code-block"></a><pre class="language-json"><code>{
  &quot;event_id&quot;: &quot;event_QzAVZRVa9hKqM5VOaHunh&quot;,
  &quot;type&quot;: &quot;error&quot;,
  &quot;error&quot;: {
    &quot;code&quot;: &quot;invalid_value&quot;,
    &quot;message&quot;: &quot;Session update error: session already started or finished or failed.&quot;
  }
}
</code></pre></td></tr></tbody></table>

<a id="session-created"></a>

<a id="05bb97c283l2n"></a>

## session.created

客户端连接到服务端后，响应的第一个事件，该事件返回时会携带服务端对此次连接的默认配置信息。

<table><tbody><tr><td><p><strong>event_id</strong><code>string</code></p><p>服务端事件ID。</p><p><strong>type</strong><code>string</code></p><p>事件类型，固定为<code>session.created</code>。</p><p><strong>session</strong><code>object</code></p><p>会话配置。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>id</strong><code>string</code></p><p>会话ID。</p><p><strong>object</strong><code>string</code></p><p>会话服务名。</p><p><strong>mode</strong><code>string</code></p><p>交互模式，<code>server_commit</code>或<code>commit</code>。</p><p><strong>model</strong><code>string</code></p><p>使用的模型。</p><p><strong>voice</strong><code>string</code></p><p>使用的音色。</p><p><strong>response_format</strong><code>string</code></p><p>音频格式。</p><p><strong>sample_rate</strong><code>integer</code></p><p>音频采样率。</p></div></section></td><td><a id="code-block-2"></a><pre class="language-json"><code>{
  &quot;event_id&quot;: &quot;event_xxx&quot;,
  &quot;type&quot;: &quot;session.created&quot;,
  &quot;session&quot;: {
    &quot;object&quot;: &quot;realtime.session&quot;,
    &quot;mode&quot;: &quot;server_commit&quot;,
    &quot;model&quot;: &quot;qwen3-tts-flash-realtime&quot;,
    &quot;voice&quot;: &quot;Cherry&quot;,
    &quot;response_format&quot;: &quot;pcm&quot;,
    &quot;sample_rate&quot;: 24000,
    &quot;id&quot;: &quot;sess_xxx&quot;
  }
}
</code></pre></td></tr></tbody></table>

<a id="session-updated"></a>

<a id="58f078ab61di5"></a>

## session.updated

接收到客户端的`session.update`请求并正确处理后返回。如果出现错误，则直接返回error事件。

<table><tbody><tr><td><p><strong>event_id</strong><code>string</code></p><p>服务端事件ID。</p><p><strong>type</strong><code>string</code></p><p>事件类型，固定为<code>session.updated</code>。</p><p><strong>session</strong><code>object</code></p><p>会话配置。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>id</strong><code>string</code></p><p>会话ID。</p><p><strong>object</strong><code>string</code></p><p>会话服务名。</p><p><strong>mode</strong><code>string</code></p><p>交互模式，<code>server_commit</code>或<code>commit</code>。</p><p><strong>model</strong><code>string</code></p><p>使用的模型。</p><p><strong>voice</strong><code>string</code></p><p>使用的音色。</p><p><strong>response_format</strong><code>string</code></p><p>音频格式。</p><p><strong>sample_rate</strong><code>integer</code></p><p>音频采样率。</p><p><strong>language_type</strong><code>string</code></p><p>音频语种。</p></div></section></td><td><a id="code-block-3"></a><pre class="language-json"><code>{
  &quot;event_id&quot;: &quot;event_xxx&quot;,
  &quot;type&quot;: &quot;session.updated&quot;,
  &quot;session&quot;: {
    &quot;id&quot;: &quot;sess_xxx&quot;,
    &quot;object&quot;: &quot;realtime.session&quot;,
    &quot;model&quot;: &quot;qwen3-tts-flash-realtime&quot;,
    &quot;voice&quot;: &quot;Cherry&quot;,
    &quot;language_type&quot;: &quot;Chinese&quot;,
    &quot;mode&quot;: &quot;commit&quot;,
    &quot;response_format&quot;: &quot;pcm&quot;,
    &quot;sample_rate&quot;: 24000
  }
}
</code></pre></td></tr></tbody></table>

<a id="input-text-buffer-committed"></a>

<a id="76abc25665qt8"></a>

## input\_text\_buffer.committed

客户端发送`input_text_buffer.commit`事件后，服务端的响应事件。

<table><tbody><tr><td><p><strong>event_id</strong><code>string</code></p><p>服务端事件ID。</p><p><strong>type</strong><code>string</code></p><p>事件类型，固定为<code>input_text_buffer.committed</code>。</p><p><strong>item_id</strong><code>string</code></p><p>将创建的用户消息项的 ID。</p></td><td><a id="code-block-4"></a><pre class="language-json"><code>{
  &quot;event_id&quot;: &quot;event_FC6MA88wS2oEeXkPvWsxX&quot;,
  &quot;type&quot;: &quot;input_text_buffer.committed&quot;,
  &quot;item_id&quot;: &quot;&quot;
}
</code></pre></td></tr></tbody></table>

<a id="input-text-buffer-cleared"></a>

<a id="7a04edb8840o7"></a>

## input\_text\_buffer.cleared

客户端发送`input_audio_buffer.clear`事件后，服务端的响应事件。

<table><tbody><tr><td><p><strong>event_id</strong><code>string</code></p><p>服务端事件ID。</p><p><strong>type</strong><code>string</code></p><p>事件类型，固定为<code>input_text_buffer.cleared</code>。</p></td><td><a id="code-block-5"></a><pre class="language-json"><code>{
    &quot;event_id&quot;: &quot;event_1122&quot;,
    &quot;type&quot;: &quot;input_text_buffer.cleared&quot;
}
</code></pre></td></tr></tbody></table>

<a id="response-created"></a>

<a id="4e06909a7es5k"></a>

## response.created

客户端发送`input_text_buffer.commit`事件后，服务端的响应事件。

<table><tbody><tr><td><p><strong>event_id</strong><code>string</code></p><p>服务端事件ID。</p><p><strong>type</strong><code>string</code></p><p>事件类型，固定为<code>response.created</code>。</p><p><strong>response</strong><code>object</code></p><p>响应详情。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>id</strong><code>string</code></p><p>响应ID。</p><p><strong>object</strong><code>string</code></p><p>对象类型，在此事件下固定为<code>realtime.response</code>。</p><p><strong>status</strong><code>string</code></p><p>响应的最终状态，取值范围：</p><ul><li>completed</li><li>failed</li><li>in_progress</li><li>incomplete</li></ul><p><strong>voice</strong><code>string</code></p><p>使用的音色。</p><p><strong>output</strong><code>array</code></p><p>在此事件下为空。</p></div></section></td><td><a id="code-block-6"></a><pre class="language-json"><code>{
  &quot;event_id&quot;: &quot;event_IMnLqDvG6Ahhk7sWV2uOs&quot;,
  &quot;type&quot;: &quot;response.created&quot;,
  &quot;response&quot;: {
    &quot;id&quot;: &quot;resp_USvBwHktHcz76r6GaIJUV&quot;,
    &quot;object&quot;: &quot;realtime.response&quot;,
    &quot;conversation_id&quot;: &quot;&quot;,
    &quot;status&quot;: &quot;in_progress&quot;,
    &quot;voice&quot;: &quot;Cherry&quot;,
    &quot;output&quot;: []
  }
}
</code></pre></td></tr></tbody></table>

<a id="response-output-item-added"></a>

<a id="efd58c096b3bv"></a>

## response.output\_item.added

当新的item项需要输出时，服务端返回此事件。

<table><tbody><tr><td><p><strong>event_id</strong><code>string</code></p><p>服务端事件ID。</p><p><strong>type</strong><code>string</code></p><p>事件类型，固定为<code>response.output_item.added</code>。</p><p><strong>response_id</strong><code>string</code></p><p>响应的ID。</p><p><strong>output_index</strong><code>integer</code></p><p>响应输出项的索引，目前固定为0。</p><p><strong>item</strong><code>object</code></p><p>输出项信息。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>id</strong><code>string</code></p><p>输出项ID。</p><p><strong>object</strong><code>string</code></p><p>始终为 <code>realtime.item</code>。</p><p><strong>status</strong><code>string</code></p><p>输出项的状态。</p><p><strong>content</strong><code>array</code></p><p>消息的内容。</p></div></section></td><td><a id="code-block-7"></a><pre class="language-json"><code>{
  &quot;event_id&quot;: &quot;event_INDGnGNulaXCrStd9ZM5X&quot;,
  &quot;type&quot;: &quot;response.output_item.added&quot;,
  &quot;response_id&quot;: &quot;resp_USvBwHktHcz76r6GaIJUV&quot;,
  &quot;output_index&quot;: 0,
  &quot;item&quot;: {
    &quot;id&quot;: &quot;item_FIrYGaNVK3rbIZqeY4QjM&quot;,
    &quot;object&quot;: &quot;realtime.item&quot;,
    &quot;type&quot;: &quot;message&quot;,
    &quot;status&quot;: &quot;in_progress&quot;,
    &quot;role&quot;: &quot;assistant&quot;,
    &quot;content&quot;: []
  }
}
</code></pre></td></tr></tbody></table>

<a id="response-content-part-added"></a>

<a id="141bec9bb11yi"></a>

## response.content\_part.added

当新的内容项需要输出时，服务端返回此事件。

<table><tbody><tr><td><p><strong>event_id</strong><code>string</code></p><p>服务端事件ID。</p><p><strong>type</strong><code>string</code></p><p>事件类型，固定为<code>response.content_part.added</code>。</p><p><strong>response_id</strong><code>string</code></p><p>响应的ID。</p><p><strong>item_id</strong><code>string</code></p><p>消息项ID。</p><p><strong>output_index</strong><code>integer</code></p><p>响应输出项的索引，目前固定为0。</p><p><strong>content_index</strong><code>integer</code></p><p>响应输出项中内部部分的索引，目前固定为0。</p><p><strong>part</strong><code>object</code></p><p>已完成的内容部分。</p><a id="accordion-属性-6"></a><section><p>属性</p><div><p><strong>type</strong><code>string</code></p><p>内容部分的类型。</p><p><strong>text</strong><code>string</code></p><p>内容部分的文本。</p></div></section></td><td><a id="code-block-8"></a><pre class="language-json"><code>{
  &quot;event_id&quot;: &quot;event_DigZ95MWN36YYyyjcENoq&quot;,
  &quot;type&quot;: &quot;response.content_part.added&quot;,
  &quot;response_id&quot;: &quot;resp_USvBwHktHcz76r6GaIJUV&quot;,
  &quot;item_id&quot;: &quot;item_FIrYGaNVK3rbIZqeY4QjM&quot;,
  &quot;output_index&quot;: 0,
  &quot;content_index&quot;: 0,
  &quot;part&quot;: {
    &quot;type&quot;: &quot;audio&quot;,
    &quot;text&quot;: &quot;&quot;
  }
}
</code></pre></td></tr></tbody></table>

<a id="response-audio-delta"></a>

<a id="a2b95643bdvnl"></a>

## response.audio.delta

当模型增量生成新的audio数据时，系统会返回服务器 response.audio.delta 事件。

<table><tbody><tr><td><p><strong>event_id</strong><code>string</code></p><p>服务端事件ID。</p><p><strong>type</strong><code>string</code></p><p>事件类型，固定为<code>response.audio.delta</code>。</p><p><strong>response_id</strong><code>string</code></p><p>响应的ID。</p><p><strong>item_id</strong><code>string</code></p><p>消息项ID。</p><p><strong>output_index</strong><code>integer</code></p><p>响应输出项的索引，目前固定为0。</p><p><strong>content_index</strong><code>integer</code></p><p>响应输出项中内部部分的索引，目前固定为0。</p><p><strong>delta</strong><code>string</code></p><p>模型增量输出的audio数据，使用Base64编码。</p></td><td><a id="code-block-9"></a><pre class="language-json"><code>{
  &quot;event_id&quot;: &quot;event_B1osWMZBtrEQbiIwW0qHQ&quot;,
  &quot;type&quot;: &quot;response.audio.delta&quot;,
  &quot;response_id&quot;: &quot;resp_B1osWTzBb8hO0WsELHgVP&quot;,
  &quot;item_id&quot;: &quot;item_B1osWH81fXDoyim1T5fsF&quot;,
  &quot;output_index&quot;: 0,
  &quot;content_index&quot;: 0,
  &quot;delta&quot;: &quot;base64 audio&quot;
}
</code></pre></td></tr></tbody></table>

<a id="response-content-part-done"></a>

<a id="5244e1dbc9vw6"></a>

## response.content\_part.done

当新的内容项输出完成时，服务端返回此事件。

<table><tbody><tr><td><p><strong>event_id</strong><code>string</code></p><p>服务端事件ID。</p><p><strong>type</strong><code>string</code></p><p>事件类型，固定为<code>response.content_part.done</code>。</p><p><strong>response_id</strong><code>string</code></p><p>响应的ID。</p><p><strong>item_id</strong><code>string</code></p><p>消息项ID。</p><p><strong>output_index</strong><code>integer</code></p><p>响应输出项的索引，目前固定为0。</p><p><strong>content_index</strong><code>integer</code></p><p>响应输出项中内部部分的索引，目前固定为0。</p><p><strong>part</strong><code>object</code></p><p>已完成的内容部分。</p><a id="accordion-属性-7"></a><section><p>属性</p><div><p><strong>type</strong><code>string</code></p><p>内容部分的类型。</p><p><strong>text</strong><code>string</code></p><p>内容部分的文本。</p></div></section></td><td><a id="code-block-10"></a><pre class="language-json"><code>{
  &quot;event_id&quot;: &quot;event_Vo2YUjlYQJ4colH8nVzkU&quot;,
  &quot;type&quot;: &quot;response.content_part.done&quot;,
  &quot;response_id&quot;: &quot;resp_USvBwHktHcz76r6GaIJUV&quot;,
  &quot;item_id&quot;: &quot;item_FIrYGaNVK3rbIZqeY4QjM&quot;,
  &quot;output_index&quot;: 0,
  &quot;content_index&quot;: 0,
  &quot;part&quot;: {
    &quot;type&quot;: &quot;audio&quot;,
    &quot;text&quot;: &quot;&quot;
  }
}
</code></pre></td></tr></tbody></table>

<a id="response-output-item-done"></a>

<a id="a922404106vzd"></a>

## response.output\_item.done

当新的item输出完成时，服务端返回此事件。

<table><tbody><tr><td><p><strong>event_id</strong><code>string</code></p><p>服务端事件ID。</p><p><strong>type</strong><code>string</code></p><p>事件类型，固定为<code>response.output_item.done</code>。</p><p><strong>response_id</strong><code>string</code></p><p>响应的ID。</p><p><strong>output_index</strong><code>integer</code></p><p>响应输出项的索引，目前固定为0。</p><p><strong>item</strong><code>object</code></p><p>输出项信息。</p><a id="accordion-属性-8"></a><section><p>属性</p><div><p><strong>id</strong><code>string</code></p><p>输出项ID。</p><p><strong>object</strong><code>string</code></p><p>始终为 <code>realtime.item</code>。</p><p><strong>status</strong><code>string</code></p><p>输出项的状态。</p><p><strong>content</strong><code>array</code></p><p>消息的内容。</p></div></section></td><td><a id="code-block-11"></a><pre class="language-json"><code>{
  &quot;event_id&quot;: &quot;event_LO6SJRKIQ9NBayyYB8a1A&quot;,
  &quot;type&quot;: &quot;response.output_item.done&quot;,
  &quot;response_id&quot;: &quot;resp_USvBwHktHcz76r6GaIJUV&quot;,
  &quot;output_index&quot;: 0,
  &quot;item&quot;: {
    &quot;id&quot;: &quot;item_FIrYGaNVK3rbIZqeY4QjM&quot;,
    &quot;object&quot;: &quot;realtime.item&quot;,
    &quot;type&quot;: &quot;message&quot;,
    &quot;status&quot;: &quot;completed&quot;,
    &quot;role&quot;: &quot;assistant&quot;,
    &quot;content&quot;: [
      {
        &quot;type&quot;: &quot;audio&quot;,
        &quot;text&quot;: &quot;&quot;
      }
    ]
  }
}
</code></pre></td></tr></tbody></table>

<a id="response-audio-done"></a>

<a id="faa3f9bc106tj"></a>

## response.audio.done

当模型生成audio数据完成时，系统会返回服务器 response.audio.done 事件。

<table><tbody><tr><td><p><strong>event_id</strong><code>string</code></p><p>服务端事件ID。</p><p><strong>type</strong><code>string</code></p><p>事件类型，固定为<code>response.audio.done</code>。</p><p><strong>response_id</strong><code>string</code></p><p>响应的ID。</p><p><strong>item_id</strong><code>string</code></p><p>消息项ID。</p><p><strong>output_index</strong><code>integer</code></p><p>响应输出项的索引，目前固定为0。</p><p><strong>content_index</strong><code>integer</code></p><p>响应输出项中内部部分的索引，目前固定为0。</p></td><td><a id="code-block-12"></a><pre class="language-json"><code>{
  &quot;event_id&quot;: &quot;event_LZaOHPzXYMUXGBcVkBmKX&quot;,
  &quot;type&quot;: &quot;response.audio.done&quot;,
  &quot;response_id&quot;: &quot;resp_USvBwHktHcz76r6GaIJUV&quot;,
  &quot;item_id&quot;: &quot;item_FIrYGaNVK3rbIZqeY4QjM&quot;,
  &quot;output_index&quot;: 0,
  &quot;content_index&quot;: 0
}
</code></pre></td></tr></tbody></table>

<a id="response-done"></a>

<a id="91f767e7440pc"></a>

## response.done

当响应生成完成时，服务端会返回此事件。该事件中包含的 Response 对象将包含 Response 中的所有输出项，但不包括已返回的原始音频数据。

<table><tbody><tr><td><p><strong>event_id</strong><code>string</code></p><p>服务端事件ID。</p><p><strong>type</strong><code>string</code></p><p>事件类型，固定为<code>response.done</code>。</p><p><strong>response_id</strong><code>string</code></p><p>响应的ID。</p><p><strong>response</strong><code>object</code></p><p>响应详情。</p><a id="accordion-属性-9"></a><section><p>属性</p><div><p><strong>id</strong><code>string</code></p><p>响应ID。</p><p><strong>object</strong><code>string</code></p><p>对象类型，在此事件下固定为<code>realtime.response</code>。</p><p><strong>output</strong><code>array</code></p><p>响应的输出。</p><p><strong>usage</strong><code>object</code></p><p>本次语音合成计费信息。</p><a id="accordion-属性-10"></a><section><p>属性</p><div><p><strong>characters</strong><code>integer</code></p><p>Qwen3-TTS Realtime计费字符数。</p></div></section></div></section></td><td><a id="fig-code-group"></a><div><a id="fig-code-group-qwen3-tts-realtime-tab"></a>Qwen3-TTS Realtime<div><a id="code-code-group-qwen3-tts-realtime"></a><pre class="language-json"><code>{
    &quot;event_id&quot;: &quot;event_Aemy83XqHFFDDSeJIDn6N&quot;,
    &quot;type&quot;: &quot;response.done&quot;,
    &quot;response&quot;: {
        &quot;id&quot;: &quot;resp_LFeR42yXZ9SxUAeXjmyTz&quot;,
        &quot;object&quot;: &quot;realtime.response&quot;,
        &quot;conversation_id&quot;: &quot;&quot;,
        &quot;status&quot;: &quot;completed&quot;,
        &quot;modalities&quot;: [
            &quot;text&quot;,
            &quot;audio&quot;
        ],
        &quot;voice&quot;: &quot;Cherry&quot;,
        &quot;output&quot;: [
            {
                &quot;id&quot;: &quot;item_Ae1lv2XmRljRSG96L8Zm1&quot;,
                &quot;object&quot;: &quot;realtime.item&quot;,
                &quot;type&quot;: &quot;message&quot;,
                &quot;status&quot;: &quot;completed&quot;,
                &quot;role&quot;: &quot;assistant&quot;,
                &quot;content&quot;: [
                    {
                        &quot;type&quot;: &quot;audio&quot;,
                        &quot;transcript&quot;: &quot;&quot;
                    }
                ]
            }
        ],
        &quot;usage&quot;: {
            &quot;characters&quot;: 25
        }
    }
}
</code></pre></div></div></td></tr></tbody></table>

<a id="session-finished"></a>

<a id="ac332f7d78oxg"></a>

## session.finished

当所有响应生成完成时，服务端会返回此事件。

<table><tbody><tr><td><p><strong>event_id</strong><code>string</code></p><p>服务端事件ID。</p><p><strong>type</strong><code>string</code></p><p>事件类型，固定为<code>session.finished</code>。</p></td><td><a id="code-block-13"></a><pre class="language-json"><code>{
  &quot;event_id&quot;: &quot;event_2239&quot;,
  &quot;type&quot;: &quot;session.finished&quot;
}
</code></pre></td></tr></tbody></table>
