# Qwen-Omni-Realtime Python SDK

通过 WebSocket 使用 DashScope Python SDK 调用 Qwen-Omni-Realtime。

<a id="model-qwen-omni-realtime"></a>

连接与鉴权参见 [WebSocket 接入](../model-api-reference/realtime-api-directory/omni-realtime-api-directory/omni-realtime-websocket-access.md)；事件字段与 JSON 示例参见[客户端事件](../model-api-reference/realtime-api-directory/omni-realtime-api-directory/client-events.md)和[服务端事件](../model-api-reference/realtime-api-directory/omni-realtime-api-directory/server-events.md)。

<a id="前提条件"></a>

<a id="model-qwen-omni-realtime-8779ce97deiou"></a>

<a id="前期准备"></a>

## 前提条件

SDK 版本需要不低于 2.0.1。请先阅读[实时多模态交互流程](../model-api-reference/realtime-api-directory/omni-realtime-api-directory/omni-realtime-websocket-access.md#websocket-workflow)。

<a id="快速开始"></a>

<a id="model-qwen-omni-realtime-3dc1a29b077gt"></a>

## 快速开始

使用 `qwen3.8-omni-flash-realtime` 时，将会话构造参数 `model` 设为该模型名，默认音色为 `Tina`。Python SDK 会话配置和视频聚合参数示例见[实时调用指南](../model-user-guide/model-experience/omni-modal/realtime.md#6905316411elw)。

请访问[GitHub](https://github.com/aliyun/alibabacloud-bailian-speech-demo/tree/master/samples/conversation/omni)下载示例代码。我们提供了三种调用方式的示例代码：

1.  [音频对话示例](https://github.com/aliyun/alibabacloud-bailian-speech-demo/tree/master/samples/conversation/omni/python)：麦克风采集实时音频输入，开启[VAD 模式](../model-user-guide/model-experience/omni-modal/realtime.md)（自动检测语音起止），支持语音打断。
    
    > `enable_turn_detection`参数需设为 True。
    
    > 推荐使用耳机播放音频，避免回声触发语音打断。
    
2.  [音视频对话示例](https://github.com/aliyun/alibabacloud-bailian-speech-demo/tree/master/samples/conversation/omni/python)：麦克风和摄像头采集实时音视频输入，开启[VAD 模式](../model-user-guide/model-experience/omni-modal/realtime.md)（自动检测语音起止），支持语音打断。
    
    > `enable_turn_detection`参数需设为 True。
    
    > 推荐使用耳机播放音频，避免回声触发语音打断。
    
3.  [本地调用](https://github.com/aliyun/alibabacloud-bailian-speech-demo/tree/master/samples/conversation/omni/python)：本地音频和图片作为输入，开启[Manual 模式](../model-user-guide/model-experience/omni-modal/realtime.md)（手动控制发送节奏）。
    
    > `enable_turn_detection`参数需设为 False。
    

<a id="请求参数"></a>

<a id="model-qwen-omni-realtime-0ce39f0139nb1"></a>

## 请求参数

下述请求参数可以通过`client.audio.realtime.connect`方法进行设置。服务端事件不再通过回调下发，改为在接收线程中迭代会话的`events()`并按`event["type"]`分发处理（参见[事件迭代](realtime-websocket-python-sdk-qwen-omni-realtime-e50924065f85dda8.md#model-qwen-omni-realtime-9d08669109iwx)）。

<table><thead><tr><th><p><strong>参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td><p>model</p></td><td><p>str</p></td><td><p>Qwen-Omni系列模型名称。参见模型列表。</p></td></tr><tr><td><p>ws_url</p></td><td><p>str</p></td><td><p>完整WebSocket端点，未指定时按<code>Client</code>的<code>workspace</code>与<code>region</code>自动选择端点：</p><ul><li><p>新加坡地域：wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/realtime</p></li><li><p>北京地域：wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime</p></li></ul><p>指定完整地址时，将域名替换为业务空间对应的 <a href="https://bailian.console.aliyun.com/cn-beijing/settings/workspace">API Host</a>，保留协议和路径。</p></td></tr></tbody></table>

> **重要**
>
> 阿里云百炼为华北2（北京）、新加坡地域推出了业务空间专属域名，**能够为推理请求提供卓越的性能和更高的稳定性**，建议迁移至新域名：
>
> -   华北2（北京）地域：从 `wss://dashscope.aliyuncs.com` 迁移至 `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
> -   新加坡地域：从 `wss://dashscope-intl.aliyuncs.com` 迁移至 `wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`
>
> 其中 `{WorkspaceId}` 为您的业务空间 ID，可在阿里云百炼控制台的**业务空间详情**页面查看。Qwen3.8-Omni-Flash-Realtime 必须使用上述业务空间专属域名；旧型号可继续使用原域名。

下述请求参数可以通过update\_session接口配置。

<table><thead><tr><th><strong>参数</strong></th><th><strong>类型</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><p>output_modalities</p></td><td><p>list[str]</p></td><td><p>模型输出模态设置，支持设置['text']（仅输出文本）或['text', 'audio']（输出音频和文本）。</p></td></tr><tr><td><p>voice</p></td><td><p>str</p></td><td><p>模型生成音频的音色，支持的音色参见<a href="../model-user-guide/model-experience/omni-modal/realtime.md#f4c9fd97f221z">音色列表</a>。</p><p>默认音色：</p><ul><li>Qwen3.5-Omni-Realtime系列模型: <code>&quot;Tina&quot;</code></li><li>qwen3-omni-flash-realtime-2025-09-15: <code>&quot;Cherry&quot;</code></li></ul></td></tr><tr><td><p>input_audio_config</p></td><td><p>dict</p></td><td><p>用户输入音频格式配置。通过 dict（含 <code>type</code>/<code>sample_rate</code> 键）同时设置格式（<code>type</code>：<code>pcm</code>/<code>wav</code>）和采样率（<code>sample_rate</code>：<code>8000</code>/<code>16000</code>/<code>24000</code>/<code>48000</code>，默认 16000 Hz），写法参见<a href="realtime-websocket-python-sdk-qwen-omni-realtime-e50924065f85dda8.md#model-qwen-omni-realtime-py_audioformatconfig_h3">音频格式与采样率配置</a>。</p><strong>适用模型：<code>qwen3.5-omni-plus-realtime</code>、<code>qwen3.5-omni-flash-realtime</code>。</strong></td></tr><tr><td><p>output_audio_config</p></td><td><p>dict</p></td><td><p>模型输出音频格式配置。通过 dict（含 <code>type</code>/<code>sample_rate</code> 键）同时设置格式（<code>type</code>：<code>pcm</code>/<code>wav</code>）和采样率（<code>sample_rate</code>：<code>8000</code>/<code>16000</code>/<code>24000</code>/<code>48000</code>）。未指定采样率时默认 16000 Hz；配置输出音频时请显式设置所需采样率，如 24000 Hz。</p><strong>适用模型：<code>qwen3.5-omni-plus-realtime</code>、<code>qwen3.5-omni-flash-realtime</code>。</strong></td></tr><tr><td><p>input_audio_format</p></td><td><p>str</p></td><td><p>历史兼容字段，新增接入建议使用 <code>input_audio_config</code> 同时配置输入格式和采样率。</p></td></tr><tr><td><p>output_audio_format</p></td><td><p>str</p></td><td><p>历史兼容字段，新增接入建议使用 <code>output_audio_config</code> 同时配置输出格式和采样率。</p></td></tr><tr><td><p>smooth_output</p></td><td><p>bool</p></td><td><p>仅 <code>qwen3-omni-flash-realtime-2025-09-15</code> 支持设置。</p><ul><li><p>True：获得口语化的回复</p></li><li><p>False：获得更书面化、正式的回复</p><blockquote><p>但可能会因为存在难以朗读的内容而导致效果不好。</p></blockquote></li><li><p>None：模型自动选择口语化或书面化的回复风格</p></li></ul></td></tr><tr><td><p>instructions</p></td><td><p>str</p></td><td><p>系统消息，用于设定模型的目标或角色。</p><p>例如：你是某五星级酒店的AI客服专员，请准确且友好地解答客户关于房型、设施、价格、预订政策的咨询。请始终以专业和乐于助人的态度回应，杜绝提供未经证实或超出酒店服务范围的信息。</p></td></tr><tr><td><p>enable_input_audio_transcription</p></td><td><p>bool</p></td><td><p>是否开启输入音频的语音识别。</p></td></tr><tr><td><p>input_audio_transcription_model</p></td><td><p>str</p></td><td><p>用于输入音频转录的语音识别模型，固定为qwen3-asr-flash-realtime，不支持修改。</p></td></tr><tr><td><p>turn_detection_type</p></td><td><p>str</p></td><td><p>VAD类型，取值如下：</p><ul><li><code>server_vad</code>（默认值）：基于声学特征检测用户语音结束。</li><li><code>semantic_vad</code>：基于语义有效性检测用户语音结束，可过滤无意义语音（如回应语、背景音）。Qwen3.8-Omni-Flash-Realtime 和 Qwen3.5-Omni-Realtime 系列模型支持。</li></ul></td></tr><tr><td><p>turn_detection_threshold</p></td><td><p>float</p></td><td><p>VAD检测阈值。建议在嘈杂的环境中增加， 在安静的环境中降低。</p><ul><li>取值越接近-1，噪音被判定为语音的概率越大。</li><li>取值越接近1，噪音被判定为语音的概率越小。</li></ul><p>默认为 0.5，参数范围：[-1.0, 1.0]。</p></td></tr><tr><td><p>turn_detection_silence_duration_ms</p></td><td><p>int</p></td><td><p>检测语音停止的静音持续时间，超过此值后会触发模型响应。默认值为800，参数范围[200, 6000]。</p></td></tr><tr><td><p>turn_detection_param</p></td><td><p>dict</p></td><td><p>VAD 扩展参数字典，用于传入 <code>turn_detection</code> 的额外配置项。当前支持传入 <code>idle_timeout_ms</code>（int）：静默超时时间（毫秒）。<strong>仅在使用</strong><code>qwen3.5-omni-plus-realtime</code><strong>或</strong><code>qwen3.5-omni-flash-realtime</code><strong>模型且 VAD 类型为</strong><code>server_vad</code><strong>时生效。</strong>服务端完成音频播报且用户持续静默超过该时间（未触发 <code>speech.started</code>）后，模型将主动触发一轮响应，基于当前上下文引导用户继续对话。取值范围：[5000, 30000]。</p><p>示例：<code>turn_detection_param={'idle_timeout_ms': 5000}</code></p></td></tr><tr><td><p>enable_search</p></td><td><p>bool</p></td><td><p>适用于 Qwen3.8-Omni-Flash-Realtime 和 Qwen3.5-Omni-Realtime 系列模型。</p><p>是否启用联网搜索功能。设置为 <code>true</code> 启用，默认为 <code>false</code>。启用后，模型可自主判断是否需要搜索来回应用户的即时问题。</p><blockquote><p>工具调用（tools）和联网搜索（enable_search）不兼容，不可同时开启。</p></blockquote></td></tr><tr><td><p>search_options</p></td><td><p>object</p></td><td><p>联网搜索选项配置。需启用 <code>enable_search</code> 后才生效。</p><p>目前仅支持设置 <code>enable_source</code>（Boolean），表示是否返回搜索结果来源列表，设置为 <code>true</code> 启用。示例：<code>search_options={'enable_source': True}</code>。</p></td></tr><tr><td><p>tools</p></td><td><p>list[dict]</p></td><td><p>适用于 Qwen3.8-Omni-Flash-Realtime 和 Qwen3.5-Omni-Realtime 系列模型。</p><p>工具定义列表。启用后，模型可自主判断是否需要调用外部工具来回应用户的问题。命中 Function Calling 时，模型不生成音频，仅返回工具调用参数。</p><p>Qwen3.8-Omni-Flash-Realtime 可在同一会话中配置 Function Calling 和 MCP 工具。MCP 配置字段见<a href="../model-api-reference/realtime-api-directory/omni-realtime-api-directory/client-events.md#session-tools-mcp">客户端事件</a>，调用限制见<a href="../model-api-reference/realtime-api-directory/omni-realtime-api-directory/omni-realtime-websocket-access.md#qwen38-mcp-limits">MCP 调用限制</a>。<code>tools</code> 与 <code>enable_search</code> 不可同时开启，该限制也适用于 MCP。</p><p>以下字段描述 Function Calling 工具。每个工具为一个字典，包含以下字段：</p><ul><li><p><code>type</code>（<code>string</code>，必选）：固定为 <code>&quot;function&quot;</code>。</p></li><li><p><code>function</code>（<code>dict</code>，必选）：工具函数的定义，包含以下字段：</p><ul><li><p><code>name</code>（<code>string</code>，必选）：自定义的工具函数名称，建议使用与函数相同的名称，如 <code>get_current_weather</code> 或 <code>get_current_time</code>。</p></li><li><p><code>description</code>（<code>string</code>，可选）：对工具函数功能的描述，大模型会参考该字段来选择是否使用该工具函数。</p></li><li><p><code>parameters</code>（<code>dict</code>，可选）：对工具函数入参的描述，大模型会参考该字段来进行入参的提取。如果工具函数不需要输入参数，则无需指定。包含以下字段：</p><ul><li><code>type</code>（<code>string</code>，必选）：固定为 <code>&quot;object&quot;</code>。</li><li><code>properties</code>（<code>dict</code>，可选）：描述各入参的名称、数据类型与描述。Key 值为入参的名称，Value 值为包含数据类型（<code>type</code>）与描述（<code>description</code>）的字典。</li><li><code>required</code>（<code>list</code>，可选）：指定哪些入参为必填项。</li></ul></li></ul></li></ul></td></tr><tr><td><p>temperature</p></td><td><p>float</p></td><td><p>采样温度，控制模型生成内容的多样性。</p><p>temperature越高，生成的内容更多样，反之，生成的内容更确定。</p><p>取值范围： [0, 2)</p><p>由于temperature与top_p均可以控制生成内容的多样性，因此建议只设置其中一个值。</p><ul><li><code>qwen3.8-omni-flash-realtime</code>：0.6</li><li>Qwen3.5-Omni-Realtime系列模型：0.7</li><li>qwen3-omni-flash-realtime-2025-09-15：0.9</li></ul></td></tr><tr><td><p>top_p</p></td><td><p>float</p></td><td><p>核采样的概率阈值，控制模型生成内容的多样性。</p><p>top_p越高，生成的内容更多样。反之，生成的内容更确定。</p><p>取值范围：（0,1.0]</p><p>由于temperature与top_p均可以控制生成内容的多样性，因此建议只设置其中一个值。</p><p>top_p默认值：</p><ul><li><code>qwen3.8-omni-flash-realtime</code>：0.95</li><li>Qwen3.5-Omni-Realtime系列模型：0.8</li><li>qwen3-omni-flash-realtime-2025-09-15：1.0</li></ul></td></tr><tr><td><p>top_k</p></td><td><p>integer</p></td><td><p>生成过程中采样候选集的大小。例如，取值为50时，仅将单次生成中得分最高的50个Token组成随机采样的候选集。取值越大，生成的随机性越高；取值越小，生成的确定性越高。取值为None或当top_k大于100时，表示不启用top_k策略，此时仅有top_p策略生效。</p><p>取值需要大于或等于0。</p><p>top_k默认值：</p><ul><li><code>qwen3.8-omni-flash-realtime</code>：20</li><li>Qwen3.5-Omni-Realtime系列模型：20</li><li>qwen3-omni-flash-realtime-2025-09-15：50</li></ul></td></tr><tr><td><p>max_tokens</p></td><td><p>integer</p></td><td><p>本次请求返回的最大 Token 数。</p><blockquote><p><code>max_tokens</code> 的设置不会影响大模型的生成过程，如果模型生成的 Token 数超过<code>max_tokens</code>，本次请求会返回截断后的内容。</p></blockquote><p><code>qwen3.8-omni-flash-realtime</code> 的取值范围为 [1, 65536]。其他模型的默认值和最大值都是模型的最大输出长度。关于各模型的最大输出长度，请参见百炼控制台。</p><p>max_tokens参数适用于需要限制字数（如生成摘要、关键词）、控制成本或减少响应时间的场景。</p></td></tr><tr><td><p>repetition_penalty</p></td><td><p>float</p></td><td><p>模型生成时连续序列中的重复度。提高repetition_penalty时可以降低模型生成的重复度，1.0表示不做惩罚。<code>qwen3.8-omni-flash-realtime</code> 支持取值 0；其他模型没有严格的取值范围，只要大于0即可。</p><p>repetition_penalty默认值：</p><ul><li><code>qwen3.8-omni-flash-realtime</code>：0</li><li>Qwen3.5-Omni-Realtime系列模型：1.0</li><li>其他模型：1.05</li></ul></td></tr><tr><td><p>presence_penalty</p></td><td><p>float</p></td><td><p>控制模型生成内容的重复度。</p><p>取值范围：[-2.0, 2.0]。正数会减少重复度，负数会增加重复度。</p><p>presence_penalty默认值：</p><ul><li><code>qwen3.8-omni-flash-realtime</code>：1</li><li>Qwen3.5-Omni-Realtime系列模型：1.5</li><li>其他模型：0.0</li></ul><p>适用场景：</p><p>较高的presence_penalty适用于要求多样性、趣味性或创造性的场景，如创意写作或头脑风暴。</p><p>较低的presence_penalty适用于要求一致性或专业术语的场景，如技术文档或其他正式文档。</p></td></tr><tr><td><p>seed</p></td><td><p>integer</p></td><td><p>设置seed参数会使模型生成过程更具有确定性，通常用于使模型每次运行的结果一致。</p><p>在每次模型调用时传入相同的seed值（自行指定），并保持其他参数不变，模型将尽可能返回相同的结果。</p><p>取值范围：0到231−1，默认值-1。</p></td></tr></tbody></table>

<a id="接口参考"></a>

<a id="model-qwen-omni-realtime-08096516dauq0"></a>

<a id="关键接口"></a>

## 接口参考

<a id="realtimesession-client-audio-realtime-connect"></a>

<a id="model-qwen-omni-realtime-4c4810ff87ofz"></a>

### RealtimeSession（`client.audio.realtime.connect`）

实时会话通过`client.audio.realtime.connect(model=...)`创建：进入`with`上下文（或调用会话的`connect()`方法）后建立连接。

<table><thead><tr><th><p>方法签名</p></th><th><p>服务端响应事件（通过<code>events()</code>下发）</p></th><th><p>说明</p></th></tr></thead><tbody><tr><td><a id="code-block"></a><pre class="language-python"><code>def connect(self) -&gt; RealtimeSession
</code></pre></td><td><p><a href="../model-api-reference/realtime-api-directory/omni-realtime-api-directory/server-events.md">服务端事件</a></p><blockquote><p>会话已创建</p></blockquote><p><a href="../model-api-reference/realtime-api-directory/omni-realtime-api-directory/server-events.md#424ef2e774q9p">session.updated</a></p><blockquote><p>会话配置已更新</p></blockquote></td><td><p>和服务端创建连接。进入<code>with</code>上下文时自动调用，勿先<code>connect()</code>再进入同一会话的<code>with</code>。</p></td></tr><tr><td><a id="code-block-2"></a><pre class="language-python"><code>def update_session(self,
                   output_modalities: List[str] = ...,
                   *,
                   voice: str = ...,
                   input_audio_format: str = ...,
                   output_audio_format: str = ...,
                   enable_input_audio_transcription: bool = ...,
                   input_audio_transcription_model: str = ...,
                   enable_turn_detection: bool = ...,
                   turn_detection_type: str = ...,
                   prefix_padding_ms: int = ...,
                   turn_detection_threshold: float = ...,
                   turn_detection_silence_duration_ms: int = ...,
                   turn_detection_param: dict = ...,
                   input_audio_config: dict = ...,
                   output_audio_config: dict = ...,
                   **kwargs) -&gt; None
</code></pre></td><td><p><a href="../model-api-reference/realtime-api-directory/omni-realtime-api-directory/server-events.md#424ef2e774q9p">session.updated</a></p><blockquote><p>会话配置已更新</p></blockquote></td><td><p>更新本次会话交互的默认配置。参数配置请参考《请求参数》章节。</p><p>在建立链接后，服务端会及时返回用于此会话的默认输出输入配置。如果需要更新默认会话配置，推荐总是在建立链接后即刻调用此接口。</p><p>服务端在收到session.update事件后，会进行参数校验，如果参数不合法则返回错误，否则更新服务端侧的会话配置。</p></td></tr><tr><td><a id="code-block-3"></a><pre class="language-python"><code>def append_audio(self, audio_b64: Union[str, bytes]) -&gt; None
</code></pre></td><td><p>无</p></td><td><p>将音频数据片段追加到云端输入音频缓冲区。<code>str</code>视为已编码的Base64，<code>bytes</code>会自动Base64编码。 音频缓冲区是可以写入并稍后提交的临时存储。</p><ul><li>打开&quot;turn_detection&quot;，音频缓冲区用于检测语音，服务端决定何时提交。</li><li>关闭&quot;turn_detection&quot;，客户端可以选择每个事件中放置多少音频量，最多放置 15 MiB。 例如，从客户端流式处理较小的数据块可以让 VAD 响应更迅速。</li></ul></td></tr><tr><td><a id="code-block-4"></a><pre class="language-python"><code>def append_video(self, video_b64: Union[str, bytes]) -&gt; None
</code></pre></td><td><p>无</p></td><td><p>将图片数据添加到云端视频缓冲区，<code>str</code>视为已编码的Base64，<code>bytes</code>会自动Base64编码。图片数据可以是本地的图片，或从视频流实时采集的图片数据。</p><p>目前对图片输入有以下限制：</p><ul><li>图片格式需要为JPG或JPEG，建议传入的图片分辨率为480P或720P， 最大1080P；</li><li>单张图片经Base64编码后不得超过256KB，建议编码前原始图片大小不超过190KB；</li><li>图片数据需要经过Base64编码；</li><li>建议以 1张/秒 的频率向服务端发送图片；</li></ul></td></tr><tr><td><a id="code-block-5"></a><pre class="language-python"><code>def clear_appended_audio(self, ) -&gt; None
</code></pre></td><td><p><a href="../model-api-reference/realtime-api-directory/omni-realtime-api-directory/server-events.md#1103f53e9b13o">input_audio_buffer.cleared</a></p><blockquote><p>清空服务端收到的音频</p></blockquote></td><td><p>删除当前云端缓冲区的音频。</p></td></tr><tr><td><a id="code-block-6"></a><pre class="language-python"><code>def commit(self, ) -&gt; None
</code></pre></td><td><p><a href="../model-api-reference/realtime-api-directory/omni-realtime-api-directory/server-events.md#bd9bfdc258afy">input_audio_buffer.committed</a></p><blockquote><p>服务端收到提交的音频</p></blockquote></td><td><p>提交之前通过append添加到云端缓冲区的音视频，如果输入的音频缓冲区为空将产生错误。</p><ul><li>打开&quot;turn_detection&quot;，客户端不需要发送此事件，服务端会自动提交音频缓冲区。</li><li>关闭&quot;turn_detection&quot;，客户端必须提交音频缓冲区才能创建用户消息项。</li></ul><p><strong>注意</strong>：</p><ol><li>如果 input_audio_transcription为会话配置了音频转录，系统会转录音频。</li><li>提交输入音频缓冲区不会从模型创建响应。</li></ol></td></tr><tr><td><a id="code-block-7"></a><pre class="language-python"><code>def create_response(self,
        modalities: list[str] = ...,
        instructions: str = ...,
        **kwargs) -&gt; None
</code></pre></td><td><p><a href="../model-api-reference/realtime-api-directory/omni-realtime-api-directory/server-events.md">服务端事件</a></p><blockquote><p>服务端开始生成响应</p></blockquote><p><a href="../model-api-reference/realtime-api-directory/omni-realtime-api-directory/server-events.md#dae2260d40qtu">response.output_item.added</a></p><blockquote><p>响应时有新的输出内容</p></blockquote><p><a href="../model-api-reference/realtime-api-directory/omni-realtime-api-directory/server-events.md">服务端事件</a></p><blockquote><p>对话项被创建</p></blockquote><p><a href="../model-api-reference/realtime-api-directory/omni-realtime-api-directory/server-events.md#de7fa0b877j25">response.content_part.added</a></p><blockquote><p>新的输出内容添加到assistant message 项</p></blockquote><p><a href="../model-api-reference/realtime-api-directory/omni-realtime-api-directory/server-events.md#35396453cfood">response.audio_transcript.delta</a></p><blockquote><p>增量生成的转录文字</p></blockquote><p><a href="../model-api-reference/realtime-api-directory/omni-realtime-api-directory/server-events.md#a25cc50a15car">response.audio.delta</a></p><blockquote><p>模型增量生成的音频</p></blockquote><p><a href="../model-api-reference/realtime-api-directory/omni-realtime-api-directory/server-events.md#f4d1698567bsm">response.audio_transcript.done</a></p><blockquote><p>完成文本转录</p></blockquote><p><a href="../model-api-reference/realtime-api-directory/omni-realtime-api-directory/server-events.md#9e8eb59c67qnt">response.audio.done</a></p><blockquote><p>完成音频生成</p></blockquote><p><a href="../model-api-reference/realtime-api-directory/omni-realtime-api-directory/server-events.md#011ad54242wft">response.content_part.done</a></p><blockquote><p>Assistant message 的文本或音频内容流式输出完成</p></blockquote><p><a href="../model-api-reference/realtime-api-directory/omni-realtime-api-directory/server-events.md#f580421f45w3h">response.output_item.done</a></p><blockquote><p>Assistant message 的整个输出项流式传输完成</p></blockquote><p><a href="../model-api-reference/realtime-api-directory/omni-realtime-api-directory/server-events.md#f2333c777d9s4">response.done</a></p><blockquote><p>响应完成</p></blockquote></td><td><p>指示服务端创建模型响应。</p><p>打开&quot;turn_detection&quot;模式下配置会话时，服务端会自动创建模型响应。</p></td></tr><tr><td><a id="code-block-8"></a><pre class="language-python"><code>def cancel_response(self, ) -&gt; None
</code></pre></td><td><p>无</p></td><td><p>取消正在进行的响应。如果没有任何响应可供取消，服务端将以一个错误进行响应。</p></td></tr><tr><td><a id="code-block-9"></a><pre class="language-python"><code>def create_item(self, item: dict) -&gt; None
</code></pre></td><td><p>无</p></td><td><p>向服务端发送 <code>conversation.item.create</code> 事件。</p><p>回传 Function Calling 工具结果时，<code>item</code> 为 dict，包含以下字段：</p><ul><li><code>type</code>：固定为 <code>function_call_output</code>。</li><li><code>call_id</code>：对应 <code>response.function_call_arguments.done</code> 事件中的 call_id。</li><li><code>output</code>：工具执行结果的字符串。</li></ul><p>MCP 审批也使用此事件，但 <code>item.type</code> 为 <code>mcp_approval_response</code>；字段见<a href="../model-api-reference/realtime-api-directory/omni-realtime-api-directory/client-events.md#qwen38-mcp-approval-response">客户端事件中的 MCP 审批回复</a>。</p></td></tr><tr><td><a id="code-block-10"></a><pre class="language-python"><code>def close(self, ) -&gt; None
</code></pre></td><td><p>无</p></td><td><p>终止任务，并关闭连接（幂等，不发送<code>session.finish</code>）。</p></td></tr><tr><td><a id="code-block-11"></a><pre class="language-python"><code>session.session_id
session.last_response_id
</code></pre></td><td><p>无</p></td><td><p>获取当前任务的session_id、最近一次response的response_id（会话属性，另有<code>last_first_text_delay</code>/<code>last_first_audio_delay</code>等首包延迟指标）。</p></td></tr></tbody></table>

<a id="音频格式与采样率配置"></a>

<a id="model-qwen-omni-realtime-py_audioformatconfig_h3"></a>

### 音频格式与采样率配置

通过 `update_session` 的 `input_audio_config` / `output_audio_config` 参数（`dict`，含 `type` 与 `sample_rate` 键）同时配置音频格式和采样率。

**适用模型：`qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime`。**

<a id="code-block-12"></a>

```python
# dict 中同时指定格式（type）与采样率（sample_rate）
session.update_session(
    output_modalities=['audio', 'text'],
    voice=voice,
    input_audio_config={"type": "pcm", "sample_rate": 16000},
    output_audio_config={"type": "wav", "sample_rate": 24000},
)
```

<a id="事件迭代-events"></a>

<a id="model-qwen-omni-realtime-9d08669109iwx"></a>

### 事件迭代（`events()`）

服务端会通过事件的方式，将服务端响应事件和数据返回给客户端。您需要在接收线程中迭代会话的`events()`，按`event["type"]`分发处理（完整事件列表参见[服务端事件](../model-api-reference/realtime-api-directory/omni-realtime-api-directory/server-events.md)）。

<a id="code-block-13"></a>

```python
def receive_events(session):
    for event in session.events():
        kind = event.get('type')
        if kind == 'session.created':
            print('start session: {}'.format(event['session']['id']))
        elif kind == 'conversation.item.input_audio_transcription.completed':
            print(f"[User] {event['transcript']}")
        elif kind == 'response.audio.delta':
            # 模型增量生成的音频（Base64），可解码后送入播放设备
            audio = base64.b64decode(event['delta'])
        elif kind == 'response.audio_transcript.done':
            print(f"[LLM] {event['transcript']}")
```

<table><thead><tr><th><p>方法签名</p></th><th><p>参数</p></th><th><p>说明</p></th></tr></thead><tbody><tr><td><a id="code-block-14"></a><pre class="language-python"><code>def events(self) -&gt; Iterator[Dict]
</code></pre></td><td><p>event：<a href="../model-api-reference/realtime-api-directory/omni-realtime-api-directory/server-events.md">服务端事件</a></p></td><td><p>连续读取并逐个产出服务端事件（<code>dict</code>）。连接关闭或收到<code>session.finished</code>后迭代结束。请由一个接收线程持续消费，不要并发创建多个读取者。</p></td></tr><tr><td><a id="code-block-15"></a><pre class="language-python"><code>def recv_event(self) -&gt; Optional[Dict]
</code></pre></td><td><p>无</p></td><td><p>阻塞读取单条服务端事件，不自动循环；无事件（连接关闭）时返回<code>None</code>。错误事件会以<code>DashScopeError</code>异常抛出。</p></td></tr></tbody></table>
