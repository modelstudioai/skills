# 实时语音识别（Paraformer）客户端事件

本文介绍 Paraformer 实时语音识别服务中客户端通过 WebSocket 发送给服务端的客户端事件，包括 run-task（启动任务）和 finish-task（结束任务）两类指令的数据结构与字段含义。

**用户指南：**关于模型介绍和选型建议请参见[语音识别](../model-user-guide/model-experience/speech-and-audio/speech-recognition/asr-model.md)。

**事件交互流程**：如需了解事件交互时序，请参见[WebSocket API](websocket-for-paraformer-real-time-service-71905b8ff2bb55c1.md)。

<a id="run-task"></a>

<a id="b618a7624b06f"></a>

## run-task

**说明**：启动语音识别任务，设置模型、音频格式、采样率等参数。

**发送时机**：建立 WebSocket 连接后立即发送。

**响应事件**：服务端返回 `task-started` 事件后才能发送音频。

<table><tbody><tr><td><p><strong>header</strong><code>object</code><strong>（必选）</strong></p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>action</strong><code>string</code><strong>（必选）</strong></p><p>指令类型，固定为 <code>run-task</code>。</p><p><strong>task_id</strong><code>string</code><strong>（必选）</strong></p><p>客户端生成的任务 ID（UUID 格式），用于关联后续事件。</p><p><strong>streaming</strong><code>string</code><strong>（必选）</strong></p><p>固定为 <code>duplex</code>。</p></div></section><p><strong>payload</strong><code>object</code><strong>（必选）</strong></p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>task_group</strong><code>string</code><strong>（必选）</strong></p><p>任务组，固定为 <code>audio</code>。</p><p><strong>task</strong><code>string</code><strong>（必选）</strong></p><p>任务类型，固定为 <code>asr</code>。</p><p><strong>function</strong><code>string</code><strong>（必选）</strong></p><p>功能类型。固定为<code>recognition</code>。</p><p><strong>model</strong><code>string</code><strong>（必选）</strong></p><p>模型名称。</p><p><strong>input</strong><code>object</code><strong>（必选）</strong></p><p>固定为<code>{}</code>。</p><p><strong>parameters</strong><code>object</code><strong>（必选）</strong></p><p>语音识别参数。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>format</strong><code>string</code><strong>（必选）</strong></p><p>音频格式。</p><p>取值范围：</p><ul><li><code>pcm</code></li><li><code>wav</code></li><li><code>mp3</code></li><li><code>opus</code></li><li><code>speex</code></li><li><code>aac</code></li><li><code>amr</code></li></ul><div><div><p><strong>重要</strong>Paraformer须遵循如下约束：</p><ul><li>opus/speex：必须使用Ogg封装</li><li>wav：必须为PCM编码</li><li>amr：仅支持AMR-NB类型</li></ul></div></div><p><strong>sample_rate</strong><code>integer</code><strong>（必选）</strong></p><p>采样率（Hz）。</p><p>取值范围：</p><ul><li><p>Paraformer（因模型而异）：</p><ul><li><p>paraformer-realtime-v2：支持任意采样率</p></li><li><p>paraformer-realtime-8k-v2：仅支持 8000 Hz</p></li></ul></li></ul><p><strong>vocabulary_id</strong><code>string</code>（可选）</p><p>热词列表 ID。</p><p><strong>disfluency_removal_enabled</strong><code>boolean</code>（可选）</p><div><div><p><strong>重要</strong>仅Paraformer支持该参数。</p></div></div><p>是否过滤语气词。</p><p>默认值：false。</p><p><strong>language_hints</strong><code>array[string]</code>（可选）</p><p>待识别音频语种。无默认值，不设置时模型自动识别。</p><p>取值范围：</p><ul><li><p>Paraformer：</p><ul><li>zh: 中文</li><li>en: 英文</li><li>ja: 日语</li><li>yue: 粤语</li><li>ko: 韩语</li><li>de：德语</li><li>fr：法语</li><li>ru：俄语</li></ul></li></ul><p><strong>semantic_punctuation_enabled</strong><code>boolean</code>（可选）</p><div><div><p><strong>重要</strong>仅Paraformer（v2）支持该参数。</p></div></div><p>是否启用语义断句。</p><p>默认值：false。</p><ul><li>true：开启语义断句，关闭 VAD 断句。</li><li>false（默认）：开启 VAD 断句，关闭语义断句。</li></ul><p>语义断句准确性更高，适合会议转写场景；VAD（Voice Activity Detection，语音活动检测）断句延迟较低，适合交互场景。</p><p><strong>max_sentence_silence</strong><code>integer</code>（可选）</p><div><div><p><strong>重要</strong></p><ul><li>仅Paraformer（v2）支持该参数。</li><li>仅在<code>semantic_punctuation_enabled</code>参数为false时生效。</li></ul></div></div><p>VAD 断句静音阈值（ms）。当一段语音后的静音时长超过该阈值时，系统会判定该句子已结束。</p><p>默认值：1300。</p><p>取值范围：[200, 6000]。</p><p><strong>multi_threshold_mode_enabled</strong><code>boolean</code>（可选）</p><div><div><p><strong>重要</strong></p><ul><li>仅Paraformer（v2）支持该参数。</li><li>仅在<code>semantic_punctuation_enabled</code>参数为false时生效。</li></ul></div></div><p>是否启用多阈值模式。启用后可防止 VAD 断句切割过长。</p><p>默认值：false。</p><p><strong>punctuation_prediction_enabled</strong><code>boolean</code>（可选）</p><div><div><p><strong>重要</strong>仅Paraformer（v2）支持该参数。</p></div></div><p>是否在识别结果中添加标点符号。</p><p>默认值：true。</p><p><strong>heartbeat</strong><code>boolean</code>（可选）</p><div><div><p><strong>重要</strong>仅Paraformer（v2）支持该参数。</p></div></div><p>是否启用心跳包。</p><p>默认值：false。</p><ul><li>true：在持续发送静音音频的情况下，可保持与服务端的连接不中断。</li><li>false（默认）：即使持续发送静音音频，连接也将在一定时间后因超时而断开。</li></ul><p><strong>inverse_text_normalization_enabled</strong><code>boolean</code>（可选）</p><div><div><p><strong>重要</strong>仅Paraformer（v2）支持该参数。</p></div></div><p>是否启用逆文本正则化（ITN）。启用后，中文数字将转换为阿拉伯数字。</p><p>默认值：true。</p></div></section></div></section></td><td><a id="code-block"></a><pre class="language-json"><code>{
    &quot;header&quot;: {
        &quot;action&quot;: &quot;run-task&quot;,
        &quot;task_id&quot;: &quot;2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx&quot;,
        &quot;streaming&quot;: &quot;duplex&quot;
    },
    &quot;payload&quot;: {
        &quot;task_group&quot;: &quot;audio&quot;,
        &quot;task&quot;: &quot;asr&quot;,
        &quot;function&quot;: &quot;recognition&quot;,
        &quot;model&quot;: &quot;paraformer-realtime-v2&quot;,
        &quot;parameters&quot;: {
            &quot;format&quot;: &quot;pcm&quot;,
            &quot;sample_rate&quot;: 16000,
            &quot;disfluency_removal_enabled&quot;: false,
            &quot;language_hints&quot;: [
                &quot;en&quot;
            ]
        },
        &quot;input&quot;: {}
    }
}
</code></pre></td></tr></tbody></table>

<a id="finish-task"></a>

<a id="c28f5d7ddb6dc"></a>

## finish-task

**说明**：通知服务端音频发送完毕，请求结束任务。

**发送时机**：所有音频数据发送完毕后。

**响应事件**：服务端返回 `task-finished` 事件。

<table><tbody><tr><td><p><strong>header</strong><code>object</code><strong>（必选）</strong></p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>action</strong><code>string</code><strong>（必选）</strong></p><p>指令类型，固定为 <code>finish-task</code>。</p><p><strong>task_id</strong><code>string</code><strong>（必选）</strong></p><p>客户端生成的任务 ID（UUID 格式），需与<a href="paraformer-client-events-2ebe52755a401965.md#b618a7624b06f">run-task</a>事件中的 task_id 保持一致。</p><p><strong>streaming</strong><code>string</code><strong>（必选）</strong></p><p>固定为 <code>duplex</code>。</p></div></section><p><strong>payload</strong><code>object</code><strong>（必选）</strong></p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>input</strong><code>object</code><strong>（必选）</strong></p><p>固定为<code>{}</code>。</p></div></section></td><td><a id="code-block-2"></a><pre class="language-json"><code>{
    &quot;header&quot;: {
        &quot;action&quot;: &quot;finish-task&quot;,
        &quot;task_id&quot;: &quot;2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx&quot;,
        &quot;streaming&quot;: &quot;duplex&quot;
    },
    &quot;payload&quot;: {
        &quot;input&quot;: {}
    }
}
</code></pre></td></tr></tbody></table>
