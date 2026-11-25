# Sambert客户端事件

**用户指南：**关于模型介绍和选型建议请参见[语音合成](../model-user-guide/model-experience/speech-and-audio/speech-synthesis/tts-model.md)。

> **重要**
>
> Sambert仅支持在北京地域使用。

<a id="run-task"></a>

<a id="sb_h2_runtask"></a>

## run-task

**说明**：启动语音合成任务，设置模型、采样率等参数，并一次性发送待合成文本。

**发送时机**：建立 WebSocket 连接后立即发送。

**响应事件**：服务端返回 task-started 事件。

> **重要**
>
> Sambert 不支持流式输入，待合成文本需要在 run-task 的 `input.text` 中一次性发送。不支持 continue-task 和 finish-task 指令。

<table><tbody><tr><td><p><strong>header</strong><code>object</code><strong>（必选）</strong></p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>action</strong><code>string</code><strong>（必选）</strong></p><p>指令类型，固定为 <code>run-task</code>。</p><p><strong>task_id</strong><code>string</code><strong>（必选）</strong></p><p>客户端生成的任务 ID（UUID 格式），用于关联后续事件。</p><p><strong>streaming</strong><code>string</code><strong>（必选）</strong></p><p>固定为 <code>out</code></p></div></section><p><strong>payload</strong><code>object</code><strong>（必选）</strong></p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>task_group</strong><code>string</code><strong>（必选）</strong></p><p>任务组，固定为 <code>audio</code>。</p><p><strong>task</strong><code>string</code><strong>（必选）</strong></p><p>任务类型，固定为 <code>tts</code>。</p><p><strong>function</strong><code>string</code><strong>（必选）</strong></p><p>功能类型，固定为 <code>SpeechSynthesizer</code>。</p><p><strong>model</strong><code>string</code><strong>（必选）</strong></p><p>模型名称，如 <code>sambert-zhichu-v1</code>。</p><p><strong>input</strong><code>object</code><strong>（必选）</strong></p><p>输入数据，包含 <code>text</code> 字段，直接传入待合成文本。</p><p><strong>text</strong><code>string</code><strong>（必选）</strong></p><p>待合成文本。</p><p><strong>parameters</strong><code>object</code><strong>（必选）</strong></p><p>语音合成参数。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>text_type</strong><code>string</code><strong>（必选）</strong></p><p>固定为 <code>PlainText</code>。</p><p><strong>format</strong><code>string</code>（可选）</p><p>音频编码格式。</p><p>取值范围：</p><ul><li>pcm</li><li>wav（默认）</li><li>mp3</li></ul><p><strong>sample_rate</strong><code>integer</code>（可选）</p><p>音频采样率（Hz）。</p><p>取值范围：8000, 16000（默认）, 22050, 24000。</p><p><strong>volume</strong><code>integer</code>（可选）</p><p>音量。</p><p>默认值：50。</p><p>取值范围：[0, 100]。</p><p><strong>rate</strong><code>float</code>（可选）</p><p>语速。</p><p>默认值：1.0。</p><p>取值范围：[0.5, 2.0]。</p><p><strong>pitch</strong><code>float</code>（可选）</p><p>音调。</p><p>默认值：1.0。</p><p>取值范围：[0.5, 2.0]。</p><p><strong>word_timestamp_enabled</strong><code>boolean</code>（可选）</p><p>是否开启字级别时间戳。</p><p>默认值：false。</p><p>适用范围：所有 Sambert 模型。</p><p><strong>phoneme_timestamp_enabled</strong><code>boolean</code>（可选）</p><p>是否开启音素级别时间戳。</p><p>默认值：false。</p><p>需要先开启 word_timestamp_enabled。</p></div></section></div></section></td><td><a id="code-block"></a><pre class="language-json"><code>{
    &quot;header&quot;: {
        &quot;action&quot;: &quot;run-task&quot;,
        &quot;task_id&quot;: &quot;2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx&quot;,
        &quot;streaming&quot;: &quot;out&quot;
    },
    &quot;payload&quot;: {
        &quot;task_group&quot;: &quot;audio&quot;,
        &quot;task&quot;: &quot;tts&quot;,
        &quot;function&quot;: &quot;SpeechSynthesizer&quot;,
        &quot;model&quot;: &quot;sambert-zhichu-v1&quot;,
        &quot;parameters&quot;: {
            &quot;text_type&quot;: &quot;PlainText&quot;,
            &quot;format&quot;: &quot;wav&quot;,
            &quot;sample_rate&quot;: 16000,
            &quot;volume&quot;: 50,
            &quot;rate&quot;: 1.0,
            &quot;pitch&quot;: 1.0,
            &quot;word_timestamp_enabled&quot;: true,
            &quot;phoneme_timestamp_enabled&quot;: true
        },
        &quot;input&quot;: {
            &quot;text&quot;: &quot;待合成文本&quot;
        }
    }
}
</code></pre></td></tr></tbody></table>
