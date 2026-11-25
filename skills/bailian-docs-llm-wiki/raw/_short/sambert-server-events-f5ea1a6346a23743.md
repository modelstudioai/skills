# Sambert服务端事件

**用户指南：**关于模型介绍和选型建议请参见[语音合成](../model-user-guide/model-experience/speech-and-audio/speech-synthesis/tts-model.md)。

<a id="task-started"></a>

<a id="sb_srv_h3_taskstarted"></a>

## task-started

当客户端发送 `run-task` 指令后，服务端返回 `task-started` 事件，标志任务已成功开启。

<table><tbody><tr><td><p><strong>header.task_id</strong><code>string</code></p><p>客户端生成的任务 ID。</p><p><strong>header.event</strong><code>string</code></p><p>事件类型，固定为 <code>task-started</code>。</p><p><strong>payload</strong><code>object</code></p><p>无内容，为空对象。</p></td><td><a id="code-block"></a><pre class="language-json"><code>{
  &quot;header&quot;: {
    &quot;task_id&quot;: &quot;2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx&quot;,
    &quot;event&quot;: &quot;task-started&quot;,
    &quot;attributes&quot;: {}
  },
  &quot;payload&quot;: {}
}
</code></pre></td></tr></tbody></table>

<a id="result-generated"></a>

<a id="sb_srv_h3_resultgen"></a>

## result-generated

客户端发送文本后，服务端持续返回 `result-generated` 事件。该事件在 `output.sentence` 中直接返回完整的时间戳信息，包括字级别和音素级别时间戳（需启用相应参数）。

<table><tbody><tr><td><p><strong>header.task_id</strong><code>string</code></p><p>客户端生成的任务 ID。</p><p><strong>header.event</strong><code>string</code></p><p>事件类型，固定为 <code>result-generated</code>。</p><p><strong>payload.output</strong><code>object</code></p><p>输出信息。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>sentence.begin_time</strong><code>integer</code></p><p>句子开始时间戳，单位：毫秒。</p><p><strong>sentence.end_time</strong><code>integer</code></p><p>句子结束时间戳，单位：毫秒。</p><p><strong>sentence.words</strong><code>array</code></p><p>字级别时间戳信息数组。</p><a id="accordion-words-元素属性"></a><section><p>words 元素属性</p><div><p><strong>text</strong><code>string</code></p><p>字的文本内容。</p><p><strong>begin_time</strong><code>integer</code></p><p>字对应音频的开始时间戳，单位：毫秒。</p><p><strong>end_time</strong><code>integer</code></p><p>字对应音频的结束时间戳，单位：毫秒。</p><p><strong>phonemes</strong><code>array</code><strong>（需启用 phoneme_timestamp_enabled）</strong></p><p>音素级别时间戳信息数组。</p><a id="accordion-phonemes-元素属性"></a><section><p>phonemes 元素属性</p><div><p><strong>text</strong><code>string</code></p><p>音素文本。</p><p><strong>tone</strong><code>integer</code></p><p>音调。</p><p><strong>begin_time</strong><code>integer</code></p><p>音素开始时间戳，单位：毫秒。</p><p><strong>end_time</strong><code>integer</code></p><p>音素结束时间戳，单位：毫秒。</p></div></section></div></section></div></section><p><strong>payload.usage</strong><code>object</code></p><p>计费信息。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>characters</strong><em>integer</em></p><p>截止当前累计的计费字符数。</p></div></section></td><td><a id="code-block-2"></a><pre class="language-json"><code>{
  &quot;header&quot;: {
    &quot;task_id&quot;: &quot;2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx&quot;,
    &quot;event&quot;: &quot;result-generated&quot;,
    &quot;attributes&quot;: {}
  },
  &quot;payload&quot;: {
    &quot;output&quot;: {
      &quot;sentence&quot;: {
        &quot;begin_time&quot;: 0,
        &quot;end_time&quot;: 1162,
        &quot;words&quot;: [
          {
            &quot;text&quot;: &quot;床&quot;,
            &quot;begin_time&quot;: 0,
            &quot;end_time&quot;: 263,
            &quot;phonemes&quot;: [
              {
                &quot;begin_time&quot;: 0,
                &quot;end_time&quot;: 119,
                &quot;text&quot;: &quot;ch_c&quot;,
                &quot;tone&quot;: 2
              }
            ]
          }
        ]
      }
    },
    &quot;usage&quot;: {
      &quot;characters&quot;: 6
    }
  }
}
</code></pre></td></tr></tbody></table>

<a id="task-finished"></a>

<a id="sb_srv_h3_taskfinished"></a>

## task-finished

服务端返回 `task-finished` 事件，标志任务已结束。客户端可以关闭 WebSocket 连接或复用连接开启新任务。

<table><tbody><tr><td><p><strong>header.task_id</strong><code>string</code></p><p>客户端生成的任务 ID。</p><p><strong>header.event</strong><code>string</code></p><p>事件类型，固定为 <code>task-finished</code>。</p><p><strong>payload.usage.characters</strong><code>integer</code></p><p>截止当前累计的计费字符数。</p></td><td><a id="code-block-3"></a><pre class="language-json"><code>{
  &quot;header&quot;: {
    &quot;task_id&quot;: &quot;2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx&quot;,
    &quot;event&quot;: &quot;task-finished&quot;,
    &quot;attributes&quot;: {
      &quot;request_uuid&quot;: &quot;0a9dba9e-d3a6-45a4-be6d-xxxxxxxxxxxx&quot;
    }
  },
  &quot;payload&quot;: {
    &quot;usage&quot;: {
      &quot;characters&quot;: 13
    }
  }
}
</code></pre></td></tr></tbody></table>

<a id="task-failed"></a>

<a id="sb_srv_h3_taskfailed"></a>

## task-failed

当任务失败时，服务端返回 `task-failed` 事件。客户端需要关闭 WebSocket 连接并处理错误。

<table><tbody><tr><td><p><strong>header.task_id</strong><code>string</code></p><p>客户端生成的任务 ID。</p><p><strong>header.event</strong><code>string</code></p><p>事件类型，固定为 <code>task-failed</code>。</p><p><strong>header.error_code</strong><code>string</code></p><p>错误码。</p><p><strong>header.error_message</strong><code>string</code></p><p>具体错误信息。</p></td><td><a id="code-block-4"></a><pre class="language-json"><code>{
  &quot;header&quot;: {
    &quot;task_id&quot;: &quot;2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx&quot;,
    &quot;event&quot;: &quot;task-failed&quot;,
    &quot;error_code&quot;: &quot;InvalidParameter&quot;,
    &quot;error_message&quot;: &quot;[tts:]Engine return error code: 418&quot;,
    &quot;attributes&quot;: {}
  },
  &quot;payload&quot;: {}
}
</code></pre></td></tr></tbody></table>
