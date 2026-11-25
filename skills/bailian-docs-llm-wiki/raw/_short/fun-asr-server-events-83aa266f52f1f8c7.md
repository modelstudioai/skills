# 实时语音识别（Fun-ASR-Realtime）服务端事件

本文介绍 Fun-ASR-Realtime 实时语音识别服务通过 WebSocket 推送给客户端的服务端事件，包括 task-started、result-generated、task-finished、task-failed 四类事件的数据结构与字段含义。

<a id="task-started"></a>

<a id="eac316aeacafj"></a>

## task-started

任务启动成功，客户端可开始发送音频数据。

<table><tbody><tr><td><p><strong>header</strong><code>object</code></p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>task_id</strong><code>string</code></p><p>客户端生成的任务 ID（UUID 格式）。</p><p><strong>event</strong><code>string</code></p><p>事件类型，固定为 <code>task-started</code>。</p><p><strong>attributes</strong><code>object</code></p><p>附加属性（通常为空）。</p></div></section><p><strong>payload</strong><code>object</code></p><p>固定为<code>{}</code>。</p></td><td><a id="code-block"></a><pre class="language-json"><code>{
    &quot;header&quot;: {
        &quot;task_id&quot;: &quot;2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx&quot;,
        &quot;event&quot;: &quot;task-started&quot;,
        &quot;attributes&quot;: {}
    },
    &quot;payload&quot;: {}
}
</code></pre></td></tr></tbody></table>

<a id="result-generated"></a>

<a id="9cb9c5831c7cs"></a>

## result-generated

识别结果，包含中间结果（sentence\_end=false）和最终结果（sentence\_end=true）。其中，新句子的首个中间结果包含 sentence\_begin=true。

<table><tbody><tr><td><p><strong>header</strong><code>object</code></p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>task_id</strong><code>string</code></p><p>客户端生成的任务 ID（UUID 格式）。</p><p><strong>event</strong><code>string</code></p><p>事件类型，固定为 <code>result-generated</code>。</p></div></section><p><strong>payload</strong><code>object</code></p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>output</strong><code>object</code></p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>sentence</strong><code>object</code></p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>begin_time</strong><code>integer</code></p><p>句子开始时间（ms）。</p><p><strong>end_time</strong><code>integer</code></p><p>句子结束时间（ms）。</p><p><strong>text</strong><code>string</code></p><p>识别文本。</p><p><strong>heartbeat</strong><code>boolean</code></p><p>若为 true，可跳过该结果（心跳包）。</p><p><strong>sentence_begin</strong><code>boolean</code></p><p>用于标识句子开始。</p><p><strong>sentence_end</strong><code>boolean</code></p><p>是否句子结束（true=最终结果，false=中间结果）。</p><p><strong>sentence_id</strong><code>integer</code></p><p>句子的序号标识。正常识别结果中，sentence_id 从 1 开始递增。当 heartbeat 为 true 时（即心跳包），sentence_id 固定为 0。</p><p><strong>words</strong><code>array[object]</code></p><p>字时间戳信息。</p><a id="accordion-属性-6"></a><section><p>属性</p><div><p><strong>begin_time</strong><code>integer</code></p><p>字开始时间（ms）。</p><p><strong>end_time</strong><code>integer</code></p><p>字结束时间（ms）。</p><p><strong>text</strong><code>string</code></p><p>识别文本。</p><p><strong>punctuation</strong><code>string</code></p><p>标点符号。</p></div></section></div></section></div></section><p><strong>usage</strong><code>object</code></p><p>当<code>payload.output.sentence.sentence_end</code>为<code>false</code>（当前句子未结束）时，<code>usage</code>为<code>null</code>。</p><p>当<code>payload.output.sentence.sentence_end</code>为<code>true</code>（当前句子已结束）时，<code>usage.duration</code>为当前任务计费时长。</p><a id="accordion-属性-7"></a><section><p>属性</p><div><p><strong>duration</strong><code>integer</code></p><p>任务计费时长（s）。</p></div></section></div></section></td><td><strong>句子开始结果：</strong><a id="code-block-2"></a><pre class="language-json"><code>{
  &quot;header&quot;: {
    &quot;task_id&quot;: &quot;2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx&quot;,
    &quot;event&quot;: &quot;result-generated&quot;,
    &quot;attributes&quot;: {}
  },
  &quot;payload&quot;: {
    &quot;output&quot;: {
      &quot;sentence&quot;: {
        &quot;begin_time&quot;: 0,
        &quot;end_time&quot;: null,
        &quot;text&quot;: &quot;&quot;,
        &quot;sentence_begin&quot;: true,
        &quot;sentence_end&quot;: false,
        &quot;sentence_id&quot;: 1,
        &quot;words&quot;: []
      }
    },
    &quot;usage&quot;: null
  }
}
</code></pre><strong>最终结果：</strong><a id="code-block-3"></a><pre class="language-json"><code>{
  &quot;header&quot;: {
    &quot;task_id&quot;: &quot;2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx&quot;,
    &quot;event&quot;: &quot;result-generated&quot;,
    &quot;attributes&quot;: {}
  },
  &quot;payload&quot;: {
    &quot;output&quot;: {
      &quot;sentence&quot;: {
        &quot;begin_time&quot;: 170,
        &quot;end_time&quot;: 920,
        &quot;text&quot;: &quot;好，我知道了&quot;,
        &quot;heartbeat&quot;: false,
        &quot;sentence_end&quot;: true,
        &quot;sentence_id&quot;: 1,
        &quot;words&quot;: [
          {
            &quot;begin_time&quot;: 170,
            &quot;end_time&quot;: 295,
            &quot;text&quot;: &quot;好&quot;,
            &quot;punctuation&quot;: &quot;，&quot;
          },
          {
            &quot;begin_time&quot;: 295,
            &quot;end_time&quot;: 503,
            &quot;text&quot;: &quot;我&quot;,
            &quot;punctuation&quot;: &quot;&quot;
          },
          {
            &quot;begin_time&quot;: 503,
            &quot;end_time&quot;: 711,
            &quot;text&quot;: &quot;知道&quot;,
            &quot;punctuation&quot;: &quot;&quot;
          },
          {
            &quot;begin_time&quot;: 711,
            &quot;end_time&quot;: 920,
            &quot;text&quot;: &quot;了&quot;,
            &quot;punctuation&quot;: &quot;&quot;
          }
        ]
      }
    },
    &quot;usage&quot;: {
      &quot;duration&quot;: 3
    }
  }
}
</code></pre></td></tr></tbody></table>

<a id="task-finished"></a>

<a id="b8aefe8e0c5fr"></a>

## task-finished

任务正常结束，可关闭连接或复用连接。

<table><tbody><tr><td><p><strong>header</strong><code>object</code></p><a id="accordion-属性-8"></a><section><p>属性</p><div><p><strong>task_id</strong><code>string</code></p><p>客户端生成的任务 ID（UUID 格式）。</p><p><strong>event</strong><code>string</code></p><p>事件类型，固定为 <code>task-finished</code>。</p><p><strong>attributes</strong><code>object</code></p><p>附加属性（通常为空）。</p></div></section><p><strong>payload</strong><code>object</code></p><p>无需关注其中内容，通常为<code>{}</code>。</p></td><td><a id="code-block-4"></a><pre class="language-json"><code>{
    &quot;header&quot;: {
        &quot;task_id&quot;: &quot;2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx&quot;,
        &quot;event&quot;: &quot;task-finished&quot;,
        &quot;attributes&quot;: {}
    },
    &quot;payload&quot;: {
        &quot;output&quot;: {},
        &quot;usage&quot;: null
    }
}
</code></pre></td></tr></tbody></table>

<a id="task-failed"></a>

<a id="3fb17b3b199fy"></a>

## task-failed

任务失败，连接会被关闭，无法复用。

<table><tbody><tr><td><p><strong>header</strong><code>object</code></p><a id="accordion-属性-9"></a><section><p>属性</p><div><p><strong>task_id</strong><code>string</code></p><p>客户端生成的任务 ID（UUID 格式）。</p><p><strong>event</strong><code>string</code></p><p>事件类型，固定为 <code>task-failed</code>。</p><p><strong>error_code</strong><code>string</code></p><p>错误类型描述。</p><p><strong>error_message</strong><code>string</code></p><p>具体错误原因。</p><p><strong>attributes</strong><code>object</code></p><p>附加属性（通常为空）。</p></div></section><p><strong>payload</strong><code>object</code></p><p>固定为<code>{}</code>。</p></td><td><a id="code-block-5"></a><pre class="language-json"><code>{
    &quot;header&quot;: {
        &quot;task_id&quot;: &quot;2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx&quot;,
        &quot;event&quot;: &quot;task-failed&quot;,
        &quot;error_code&quot;: &quot;CLIENT_ERROR&quot;,
        &quot;error_message&quot;: &quot;request timeout after 23 seconds.&quot;,
        &quot;attributes&quot;: {}
    },
    &quot;payload&quot;: {}
}
</code></pre></td></tr></tbody></table>
