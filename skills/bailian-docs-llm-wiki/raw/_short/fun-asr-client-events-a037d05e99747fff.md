# 实时语音识别（Fun-ASR-Realtime）客户端事件

本文介绍 Fun-ASR-Realtime 实时语音识别服务中客户端通过 WebSocket 发送给服务端的客户端事件，包括 run-task（启动任务）、finish-task（结束任务）等指令的数据结构与字段含义。

<a id="run-task"></a>

<a id="9cae7e7b85ebm"></a>

## run-task

启动语音识别任务，设置模型、音频格式、采样率等参数。

**发送时机**：建立 WebSocket 连接后立即发送。

**响应事件**：服务端返回 `task-started` 事件后才能发送音频。

<table><tbody><tr><td><p><strong>header</strong><code>object</code><strong>（必选）</strong></p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>action</strong><code>string</code><strong>（必选）</strong></p><p>指令类型，固定为 <code>run-task</code>。</p><p><strong>task_id</strong><code>string</code><strong>（必选）</strong></p><p>客户端生成的任务 ID（UUID 格式），用于关联后续事件。</p><p><strong>streaming</strong><code>string</code><strong>（必选）</strong></p><p>固定为 <code>duplex</code>。</p></div></section><p><strong>payload</strong><code>object</code><strong>（必选）</strong></p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>task_group</strong><code>string</code><strong>（必选）</strong></p><p>任务组，固定为 <code>audio</code>。</p><p><strong>task</strong><code>string</code><strong>（必选）</strong></p><p>任务类型，固定为 <code>asr</code>。</p><p><strong>function</strong><code>string</code><strong>（必选）</strong></p><p>功能类型。固定为<code>recognition</code>。</p><p><strong>model</strong><code>string</code><strong>（必选）</strong></p><p>模型名称。</p><p><strong>input</strong><code>object</code><strong>（必选）</strong></p><p>输入对象。不携带上下文时传入<code>{}</code>。</p><div><div><p><strong>重要</strong>仅 <code>fun-asr-realtime</code> 模型支持上下文。</p></div></div><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>context</strong><code>array(object)</code>（可选）</p><p>对话上下文，用于辅助识别、提升专有词汇的识别准确率。使用方法详见<a href="../model-user-guide/model-experience/speech-and-audio/speech-recognition/improve-asr-accuracy.md#ctx_enhance_h2">上下文增强</a>。</p><div><div><p><strong>重要</strong>上下文消息（<code>input_text</code> 和 <code>text</code> 类型）各最多 5 条，超出时保留最近的 5 条。每轮上下文文本总长度（<code>user</code> 和 <code>assistant</code> 的 <code>text</code> 字段长度之和）不超过 400 个字符（按字符数计算，每个字符计为 1），超出部分从末尾截断。</p></div></div><div><div><p><strong>重要</strong>携带上下文时，<code>context</code> 中的消息顺序有要求：上下文消息必须按对话轮次排列，每轮中 <code>user</code>（<code>input_text</code> 类型）必须在对应的 <code>assistant</code>（<code>text</code> 类型）之前。</p></div></div><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>role</strong><code>string</code><strong>（必选）</strong></p><p>消息角色。取值范围：</p><ul><li><code>user</code>：前几轮用户语音的识别结果或领域相关的词表。</li><li><code>assistant</code>：前几轮大语言模型的回复内容。</li></ul><p><strong>content</strong><code>array(object)</code><strong>（必选）</strong></p><p>消息内容列表。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>type</strong><code>string</code><strong>（必选）</strong></p><p>内容类型。取值范围：</p><ul><li><code>input_text</code>：前几轮用户语音的识别结果或领域相关的词表（role 为 user 时使用），需同时传入 <code>text</code> 字段。</li><li><code>text</code>：前几轮大语言模型的回复内容（role 为 assistant 时使用），需同时传入 <code>text</code> 字段。</li></ul><p><strong>text</strong><code>string</code><strong>（必选）</strong></p><p>文本内容。当 <code>type</code> 为 <code>input_text</code> 时，填入前几轮用户语音的识别结果或领域相关的词表；当 <code>type</code> 为 <code>text</code> 时，填入前几轮大语言模型的回复内容。</p></div></section></div></section></div></section><p><strong>parameters</strong><code>object</code><strong>（必选）</strong></p><p>语音识别参数。</p><a id="accordion-属性-6"></a><section><p>属性</p><div><p><strong>format</strong><code>string</code><strong>（必选）</strong></p><p>音频格式。</p><p>取值范围：</p><ul><li><code>pcm</code></li><li><code>wav</code></li><li><code>mp3</code></li><li><code>opus</code></li><li><code>speex</code></li><li><code>aac</code></li><li><code>amr</code></li></ul><div><div><p><strong>重要</strong>opus/speex：必须使用Ogg封装；</p><p>wav：必须为PCM编码；</p><p>amr：仅支持AMR-NB类型。</p></div></div><p><strong>sample_rate</strong><code>integer</code><strong>（必选）</strong></p><p>采样率（Hz）。</p><p>取值范围：8k模型仅支持 8000 Hz，其他模型支持任意采样率。</p><p><strong>vocabulary_id</strong><code>string</code>（可选）</p><p>预编译热词列表 ID。</p><p>需预先调用创建热词列表接口生成，识别时传入该 ID 即可使用列表中的热词。</p><p>适用于词汇已知且相对稳定、需要跨请求复用同一词表的场景。</p><p>使用方法请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-recognition/improve-asr-accuracy.md#hw_precompiled_h3">预编译热词</a>。</p><p><strong>language_hints</strong><code>array[string]</code>（可选）</p><p>待识别音频语种。无默认值，不设置时模型自动识别。</p><p>仅支持设置 1 个值，设置多个时仅第一个生效。</p><a id="accordion-点击查看支持的语言代码"></a><section><p>点击查看支持的语言代码</p><div><ul><li><p>fun-asr-realtime：</p><ul><li>zh: 中文</li><li>en: 英文</li><li>ja: 日语</li><li>ko：韩语</li><li>vi：越南语</li><li>th：泰语</li><li>id：印尼语</li><li>ms：马来语</li><li>tl：菲律宾语</li><li>hi：印地语</li><li>ar：阿拉伯语</li><li>fr：法语</li><li>de：德语</li><li>es：西班牙语</li><li>pt：葡萄牙语</li><li>ru：俄语</li><li>it：意大利语</li><li>nl：荷兰语</li><li>sv：瑞典语</li><li>da：丹麦语</li><li>fi：芬兰语</li><li>no：挪威语</li><li>el：希腊语</li><li>pl：波兰语</li><li>cs：捷克语</li><li>hu：匈牙利语</li><li>ro：罗马尼亚语</li><li>bg：保加利亚语</li><li>hr：克罗地亚语</li><li>sk：斯洛伐克语</li></ul></li><li><p>fun-asr-realtime-2026-02-28：</p><ul><li>zh: 中文</li><li>en: 英文</li><li>ja: 日语</li></ul></li><li><p>fun-asr-flash-8k-realtime、fun-asr-flash-8k-realtime-2026-01-28：</p><ul><li>zh: 中文</li></ul></li></ul></div></section><p><strong>max_sentence_silence</strong><code>integer</code>（可选）</p><p>VAD 断句静音阈值（ms）。当一段语音后的静音时长超过该阈值时，系统会判定该句子已结束。</p><p>默认值：1300。</p><p>取值范围：[200, 6000]。</p><p><strong>multi_threshold_mode_enabled</strong><code>boolean</code>（可选）</p><p>是否启用多阈值模式。启用后可防止 VAD 断句切割过长。</p><p>默认值：false。</p><p><strong>heartbeat</strong><code>boolean</code>（可选）</p><p>是否启用心跳包。</p><p>默认值：false。</p><ul><li>true：在持续发送静音音频的情况下，可保持与服务端的连接不中断。</li><li>false（默认）：即使持续发送静音音频，连接也将在一定时间后因超时而断开。</li></ul><p>静音音频指的是在音频文件或数据流中没有声音信号的内容。静音音频可以通过多种方法生成，例如使用音频编辑软件如Audacity或Adobe Audition，或者通过命令行工具如FFmpeg。</p><p><strong>speech_noise_threshold</strong><code>float</code>（可选）</p><p>语音与噪音的判定阈值，用于调整语音活动检测（VAD）的灵敏度。</p><p>取值范围：[-1.0, 1.0]。</p><p>取值说明：</p><ul><li>取值越接近 -1：降低噪音判定阈值，噪音被识别为语音的概率增大，可能导致更多噪音被转写</li><li>取值越接近 +1：提高噪音判定阈值，语音被误判为噪音的概率增大，可能导致部分语音被过滤</li></ul><p>此参数为高级配置参数，调整可能显著影响识别效果，建议：</p><ul><li>调整前充分测试验证效果</li><li>根据实际音频环境小幅度调整（建议步长 0.1）</li></ul><p><strong>special_word_filter</strong> <code>string</code>（可选）</p><a id="special-word-filter"></a><p>敏感词过滤规则，用于将识别结果中的指定词汇替换为等长的星号，或从结果中移除。值为规则对象序列化后的 JSON 字符串。最多可设置 32 个敏感词；未传入该参数时不进行过滤。</p><ul><li><code>filter_with_signed.word_list</code>：字符串数组。匹配的词替换为等长的星号。</li><li><code>filter_with_empty.word_list</code>：字符串数组。匹配的词从结果中移除。</li><li><code>system_reserved_filter</code>：布尔值，默认 <code>false</code>。控制是否使用系统预置词表；自定义的替换、移除规则分别由上述两个列表配置。</li></ul><a id="code-block"></a><pre class="language-json"><code>{
  &quot;special_word_filter&quot;: &quot;{\&quot;filter_with_signed\&quot;:{\&quot;word_list\&quot;:[\&quot;项目\&quot;]},\&quot;filter_with_empty\&quot;:{\&quot;word_list\&quot;:[\&quot;报告\&quot;]},\&quot;system_reserved_filter\&quot;:false}&quot;
}
</code></pre></div></section></div></section></td><td><a id="fig-code-group"></a><div><a id="fig-code-group-基本请求-tab"></a>基本请求<div><a id="code-code-group-基本请求"></a><pre class="language-json"><code>{
    &quot;header&quot;: {
        &quot;action&quot;: &quot;run-task&quot;,
        &quot;task_id&quot;: &quot;2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx&quot;,
        &quot;streaming&quot;: &quot;duplex&quot;
    },
    &quot;payload&quot;: {
        &quot;task_group&quot;: &quot;audio&quot;,
        &quot;task&quot;: &quot;asr&quot;,
        &quot;function&quot;: &quot;recognition&quot;,
        &quot;model&quot;: &quot;fun-asr-realtime&quot;,
        &quot;parameters&quot;: {
            &quot;format&quot;: &quot;pcm&quot;,
            &quot;sample_rate&quot;: 16000
        },
        &quot;input&quot;: {}
    }
}
</code></pre></div><a id="fig-code-group-携带上下文-tab"></a>携带上下文<div><a id="code-code-group-携带上下文"></a><pre class="language-json"><code>{
    &quot;header&quot;: {
        &quot;action&quot;: &quot;run-task&quot;,
        &quot;task_id&quot;: &quot;2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx&quot;,
        &quot;streaming&quot;: &quot;duplex&quot;
    },
    &quot;payload&quot;: {
        &quot;task_group&quot;: &quot;audio&quot;,
        &quot;task&quot;: &quot;asr&quot;,
        &quot;function&quot;: &quot;recognition&quot;,
        &quot;model&quot;: &quot;fun-asr-realtime&quot;,
        &quot;parameters&quot;: {
            &quot;format&quot;: &quot;pcm&quot;,
            &quot;sample_rate&quot;: 16000
        },
        &quot;input&quot;: {
            &quot;context&quot;: [
                {
                    &quot;role&quot;: &quot;user&quot;,
                    &quot;content&quot;: [
                        {
                            &quot;type&quot;: &quot;input_text&quot;,
                            &quot;text&quot;: &quot;你好啊&quot;
                        }
                    ]
                },
                {
                    &quot;role&quot;: &quot;assistant&quot;,
                    &quot;content&quot;: [
                        {
                            &quot;type&quot;: &quot;text&quot;,
                            &quot;text&quot;: &quot;你好啊，我是通义千问，有什么可以帮助你的？&quot;
                        }
                    ]
                }
            ]
        }
    }
}
</code></pre></div></div></td></tr></tbody></table>

<a id="finish-task"></a>

<a id="85880fa44008n"></a>

## finish-task

通知服务端音频发送完毕，请求结束任务。

**发送时机**：所有音频数据发送完毕后。

**响应事件**：服务端返回 `task-finished` 事件。

<table><tbody><tr><td><p><strong>header</strong><code>object</code><strong>（必选）</strong></p><a id="accordion-属性-7"></a><section><p>属性</p><div><p><strong>action</strong><code>string</code><strong>（必选）</strong></p><p>指令类型，固定为 <code>finish-task</code>。</p><p><strong>task_id</strong><code>string</code><strong>（必选）</strong></p><p>客户端生成的任务 ID（UUID 格式），需与<code>run-task</code>事件中的 task_id 保持一致。</p><p><strong>streaming</strong><code>string</code><strong>（必选）</strong></p><p>固定为 <code>duplex</code>。</p></div></section><p><strong>payload</strong><code>object</code><strong>（必选）</strong></p><a id="accordion-属性-8"></a><section><p>属性</p><div><p><strong>input</strong><code>object</code><strong>（必选）</strong></p><p>固定为<code>{}</code>。</p></div></section></td><td><a id="code-block-2"></a><pre class="language-json"><code>{
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
