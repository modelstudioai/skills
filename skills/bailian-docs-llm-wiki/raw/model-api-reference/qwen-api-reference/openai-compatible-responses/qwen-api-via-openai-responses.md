# 创建响应

通过兼容 OpenAI 格式的 Responses API 调用千问模型，查看输入输出参数说明及调用示例。

**相较于OpenAI Chat Completions API 的优势：**

-   **内置工具**：内置联网搜索、网页抓取、代码解释器、文搜图、图搜图、知识库搜索等工具，可在处理复杂任务时获得更优效果，详情参考[工具调用](../../../model-user-guide/model-experience/text-generation-model/tool-calls.md)。
-   **更灵活的输入**：支持直接传入字符串作为模型输入，也兼容 Chat 格式的消息数组。
-   **简化上下文管理**：通过传递上一轮响应的 `previous_response_id`，无需手动构建完整的消息历史数组。
-   **便捷的上下文缓存**：只需在请求头中添加 `x-dashscope-session-cache: enable`（默认值为 disable），服务端即可自动缓存对话上下文，无需改动业务代码即可降低多轮对话的推理延迟与成本，详情参考[Session 缓存](../../toolkits-and-frameworks/compatibility-with-openai-responses-api.md#example-session-cache-title)。

<a id="兼容性说明与限制"></a>

<a id="0a0bff578cg0f"></a>

## 兼容性说明与限制

本 API 在接口设计上兼容 OpenAI，以降低开发者迁移成本，但在参数、功能和具体行为上存在差异。

**核心原则：**请求将仅处理本文档明确列出的参数，任何未提及的 OpenAI 参数都会被忽略。

以下是几个关键的差异点，以帮助您快速适配：

-   **部分参数不支持**：不支持部分 OpenAI Responses API 参数，例如异步执行参数`background`（当前仅支持同步调用）等。
-   **思考强度控制**：通过 `reasoning.effort` 参数控制模型的思考强度，具体用法请参考相应参数的说明。
-   **上下文限制**：为预留内置工具调用与推理生成空间，Responses API 的最大输入上下文约为模型窗口大小的 80%（预留约 20% 缓冲区），超出部分将自动触发截断，不会报错中断。

<a id="sec-tabs"></a>

<a id="华北2-北京"></a>

<a id="华北2-北京-h4"></a>

#### 华北2（北京）

SDK 调用配置的`base_url`：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`

HTTP 请求地址：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/responses`

<a id="新加坡"></a>

<a id="新加坡-h4"></a>

#### 新加坡

SDK 调用配置的`base_url`：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`

HTTP 请求地址：`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1/responses`

<a id="美国-弗吉尼亚"></a>

<a id="美国-弗吉尼亚-h4"></a>

#### 美国（弗吉尼亚）

SDK 调用配置的`base_url`：`https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/compatible-mode/v1`

HTTP 请求地址：`POST https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/compatible-mode/v1/responses`

<a id="德国-法兰克福"></a>

<a id="德国-法兰克福-h4"></a>

#### 德国（法兰克福）

SDK 调用配置的`base_url`：`https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1`

HTTP 请求地址：`POST https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1/responses`

<a id="日本-东京"></a>

<a id="日本-东京-h4"></a>

#### 日本（东京）

SDK 调用配置的`base_url`：`https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/compatible-mode/v1`

HTTP 请求地址：`POST https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/compatible-mode/v1/responses`

<a id="中国香港"></a>

<a id="中国香港-h4"></a>

#### 中国香港

SDK 调用配置的`base_url`：`https://{WorkspaceId}.cn-hongkong.maas.aliyuncs.com/compatible-mode/v1`

HTTP 请求地址：`POST https://{WorkspaceId}.cn-hongkong.maas.aliyuncs.com/compatible-mode/v1/responses`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

> **重要**
>
> 阿里云百炼为华北2（北京）、新加坡、中国香港地域推出了业务空间专属域名，**能够为推理请求提供卓越的性能和更高的稳定性**，建议迁移至新域名：
>
> -   华北2（北京）地域：从 `https://dashscope.aliyuncs.com` 迁移至 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
> -   新加坡地域：从 `https://dashscope-intl.aliyuncs.com` 迁移至 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`
>
> 其中 `{WorkspaceId}` 为您的业务空间 ID，可在阿里云百炼控制台的**业务空间详情**页面查看。现有域名仍可正常使用。

> **重要**
>
> OpenAI兼容-Responses API 的旧版URL路径 `/api/v2/apps/protocols/compatible-mode/v1/responses` 已经停止维护，将不再保证功能可用性，请尽快迁移至新版路径 `/compatible-mode/v1/responses`。

<table><tbody><tr><td><a id="f8eeeafac1c22"></a><h2>请求体</h2><p><strong>model</strong> <code>string</code> <strong>（必选）</strong></p><p>模型名称。</p><a id="accordion-支持的模型"></a><section><p>支持的模型</p><div><p><code>qwen4-max</code>、<code>qwen3.8-max</code>、<code>qwen3.8-max-0902</code>、<code>qwen3.8-flash</code>、<code>qwen3.8-2.4t-a95b</code>、<code>qwen3.8-27b</code>、<code>qwen3.8-omni-flash</code>、<code>qwen3.7-max</code>、<code>qwen3.7-max-2026-05-20</code>、<code>qwen3.7-max-2026-06-08</code>、<code>qwen3.7-max-2026-05-17</code>、<code>qwen3.7-max-preview</code>、<code>qwen3.7-plus</code>、<code>qwen3.7-plus-2026-05-26</code>、<code>qwen3.6-plus</code>、<code>qwen3.6-plus-2026-04-02</code>、<code>qwen3.5-plus</code>、<code>qwen3.5-plus-2026-04-20</code>、<code>qwen3.5-plus-2026-02-15</code>、<code>qwen3.7-flash</code>、<code>qwen3.7-flash-2026-07-15</code>、<code>qwen3.6-flash</code>、<code>qwen3.6-flash-2026-04-16</code>、<code>qwen3.5-flash</code>、<code>qwen3.5-flash-2026-02-23</code>、<code>qwen3.6-35b-a3b</code>、<code>qwen3.5-397b-a17b</code>、<code>qwen3.5-122b-a10b</code>、<code>qwen3.5-27b</code>、<code>qwen3.5-35b-a3b</code>、<code>deepseek-v4.1-flash</code>、<code>deepseek-v4.1-flash-1017</code>、<code>deepseek-v4-pro</code>、<code>deepseek-v4-pro-0813</code>、<code>deepseek-v4-flash-0731</code>、<code>glm-5.3</code>、<code>glm-5.2</code>、<code>kimi-k3.1-pro</code>、<code>kimi-k3</code></p><div><div><p><strong>重要</strong>非列表中阿里云百炼直供文本生成模型仅支持基础兼容能力，Agent 能力（内置工具等）受限。</p></div></div></div></section><p><strong>input</strong> <code>string 或 array</code> <strong>（必选）</strong></p><p>模型输入，支持以下格式：</p><ul><li><code>string</code>：纯文本，如 <code>&quot;你好&quot;</code>。</li><li><code>array</code>：消息数组，按对话顺序排列。</li></ul><a id="accordion-array-输入项类型"></a><section><p>array 输入项类型</p><div><p><strong>EasyInputMessage</strong> <code>object</code></p><p>通过 role 区分消息类型，通过content传递消息内容。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>role</strong> <code>string</code> <strong>（必选）</strong></p><p>消息角色，可选值：<code>user</code>、<code>assistant</code>、<code>system</code>、<code>developer</code>。</p><p><strong>content</strong> <code>string 或 array</code> <strong>（必选）</strong></p><p>消息内容，支持以下格式：</p><ul><li><code>string</code>：纯文本输入。</li><li><code>array</code>：内容数组，包含一个或多个内容项，可混合不同类型。<code>system</code>/<code>developer</code> 角色的元素类型为 <code>input_text</code>，<code>assistant</code> 角色的元素类型为 <code>output_text</code>。</li></ul><a id="accordion-array-元素类型"></a><section><p>array 元素类型</p><div><p>以下类型之一：</p><p><strong>input_text</strong> <code>{ type, text }</code></p><p>文本输入。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>固定为 <code>input_text</code>。</p><p><strong>text</strong> <code>string</code> <strong>（必选）</strong></p><p>输入模型的文本内容。</p><p><strong>prompt_cache_breakpoint</strong> <code>object</code> (可选)</p><p>仅支持 <code>qwen4-max</code>。 用于手动标记缓存断点，优先级高于顶层缓存模式。 详见<a href="../../../model-user-guide/model-experience/text-generation-model/explicit-cache-qwen4.md">显式缓存（Qwen4）</a>。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>mode</strong> <code>string</code> (必选)</p><p>仅支持 <code>explicit</code>；设置断点时需显式传入。</p></div></section></div></section><p><strong>input_image</strong> <code>{ type, image_url }</code></p><p>图片输入，仅 <code>user</code> 角色。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>固定为 <code>input_image</code>。</p><p><strong>image_url</strong> <code>string</code> <strong>（必选）</strong></p><p>图片的公网 URL 或 Base64 编码。Base64 请传入完整的 Data URI，例如：<code>data:image/png;base64,iVBORw0K...</code>。</p><p><strong>prompt_cache_breakpoint</strong> <code>object</code> (可选)</p><p>仅支持 <code>qwen4-max</code>。 用于手动标记缓存断点，优先级高于顶层缓存模式。 详见<a href="../../../model-user-guide/model-experience/text-generation-model/explicit-cache-qwen4.md">显式缓存（Qwen4）</a>。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>mode</strong> <code>string</code> (必选)</p><p>仅支持 <code>explicit</code>；设置断点时需显式传入。</p></div></section></div></section><p><strong>input_file</strong> <code>{ type, file_url }</code></p><p>文件输入，仅 <code>user</code> 角色。目前 <code>qwen4-max</code>、<code>qwen3.8-flash</code>、<code>qwen3.8-max</code>、<code>qwen3.5-ocr</code> 支持此类型。</p><a id="accordion-属性-6"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>固定为 <code>input_file</code>。</p><p><strong>file_url</strong> <code>string</code> <strong>（必选）</strong></p><p>PDF 文件的公网 URL，文件最大 100 MB。</p><p>PDF 的页数上限取决于 <code>ocr_options</code> 中的 <code>task</code>：设置为 <code>document_parsing</code> 时最大 50 页；未设置 <code>task</code> 或设置为其他任务时，最大 10 页。</p><p><strong>prompt_cache_breakpoint</strong> <code>object</code> (可选)</p><p>仅支持 <code>qwen4-max</code>。 用于手动标记缓存断点，优先级高于顶层缓存模式。 详见<a href="../../../model-user-guide/model-experience/text-generation-model/explicit-cache-qwen4.md">显式缓存（Qwen4）</a>。</p><a id="accordion-属性-7"></a><section><p>属性</p><div><p><strong>mode</strong> <code>string</code> (必选)</p><p>仅支持 <code>explicit</code>；设置断点时需显式传入。</p></div></section></div></section><p><strong>input_audio</strong> <code>{ type, format, audio_url, 2 more }</code></p><p>音频输入，仅适用于 <code>qwen3.8-omni-flash</code> 的 <code>user</code> 消息。</p><a id="accordion-属性-8"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>固定为 <code>input_audio</code>。</p><p><strong>format</strong> <code>string</code> <strong>（必选）</strong></p><p>音频格式，例如 <code>wav</code>、<code>mp3</code>。</p><p><strong>audio_url</strong> <code>string</code></p><p>音频的公网 URL。与 <code>data</code> 二选一，不能同时传入。</p><p><strong>data</strong> <code>string</code></p><p>包含 MIME 类型前缀和 Base64 编码音频的完整 Data URI，例如：<code>data:audio/wav;base64,UklGR...</code>。与 <code>audio_url</code> 二选一，不能同时传入。</p><p><strong>use_multichannel</strong> <code>boolean</code> （可选）</p><p>是否对音频进行空间音频解析，默认 <code>false</code>。设为 <code>true</code> 时，对双通道或四通道音频进行空间音频解析；设为 <code>false</code> 时，按单通道音频解析。</p></div></section><p><strong>input_video</strong> <code>{ type, video_url, fps }</code></p><p>视频输入，仅适用于 <code>qwen3.8-omni-flash</code> 的 <code>user</code> 消息。</p><a id="accordion-属性-9"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>固定为 <code>input_video</code>。</p><p><strong>video_url</strong> <code>string</code> <strong>（必选）</strong></p><p>视频的公网 URL。</p><p><strong>fps</strong> <code>number</code> （可选）</p><p>抽帧频率，表示每秒抽取的帧数，例如 <code>2</code> 表示每秒抽取 2 帧，不要传字符串。</p></div></section><p><strong>output_text</strong> <code>{ type, text }</code></p><p>助手回复，仅 <code>assistant</code> 角色。</p><a id="accordion-属性-10"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>固定为 <code>output_text</code>。</p><p><strong>text</strong> <code>string</code> <strong>（必选）</strong></p><p>助手回复的文本内容。</p></div></section><p>音视频输入沿用普通文本响应格式和流式事件，流式文本使用 <code>response.output_text.delta</code>、<code>response.output_text.done</code>。音视频输入、文本输出示例见<a href="../../../model-user-guide/model-experience/omni-modal/qwen-omni.md#qwen38-offline">Qwen3.8-Omni-Flash</a>。</p></div></section><p><strong>type</strong> <code>string</code> （可选）</p><p>固定为 <code>message</code>。</p></div></section><p><strong>ResponseOutputMessage</strong> <code>object</code> （可选）</p><p>模型的输出消息对象。可直接将上一轮响应的 output 中的 message 项传回 input，用于多轮对话场景。与 EasyInputMessage 的区别在于它携带了完整的输出结构（含 id、status 和结构化 content）。</p><a id="accordion-属性-11"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>固定为 <code>message</code>。</p><p><strong>id</strong> <code>string</code> <strong>（必选）</strong></p><p>输出消息的唯一标识，来自上一轮响应。</p><p><strong>role</strong> <code>string</code> <strong>（必选）</strong></p><p>固定为 <code>assistant</code>。</p><p><strong>status</strong> <code>string</code> <strong>（必选）</strong></p><p>消息状态，可选值：<code>in_progress</code>、<code>completed</code>、<code>incomplete</code>。</p><p><strong>content</strong> <code>array</code> <strong>（必选）</strong></p><p>内容数组，元素为 output_text 类型对象。</p><a id="accordion-属性-12"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>固定为 <code>output_text</code>。</p><p><strong>text</strong> <code>string</code> <strong>（必选）</strong></p><p>回复文本。</p><p><strong>annotations</strong> <code>array</code> （可选）</p><p>标注信息。</p></div></section></div></section><p><strong>Custom Tool Call</strong> <code>object</code> （可选）</p><p>模型返回的自定义工具调用。执行工具后，将调用项和对应的 <code>custom_tool_call_output</code> 追加到下一轮请求的 <code>input</code> 中。</p><a id="accordion-属性-13"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>固定为 <code>custom_tool_call</code>。</p><p><strong>id</strong> <code>string</code> （可选）</p><p>上一轮响应中的调用项 ID，原样回传。</p><p><strong>name</strong> <code>string</code> <strong>（必选）</strong></p><p>工具名称，例如 <code>emit_code</code>。</p><p><strong>input</strong> <code>string</code> <strong>（必选）</strong></p><p>自定义工具的自由文本输入，仅当 <code>type</code> 为 <code>custom_tool_call</code> 时存在。</p><p><strong>call_id</strong> <code>string</code> <strong>（必选）</strong></p><p>工具调用标识符，使用模型返回的 <code>call_id</code>。</p><p><strong>namespace</strong> <code>string</code> （可选）</p><p>工具所属的命名空间。调用命名空间内的 <code>function</code> 或 <code>custom</code> 工具时返回，回传调用项时保留该字段。</p></div></section><p><strong>Custom Tool Call Output</strong> <code>object</code> （可选）</p><p>自定义工具的执行结果，通过 <code>call_id</code> 关联对应的调用。</p><a id="accordion-属性-14"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>固定为 <code>custom_tool_call_output</code>。</p><p><strong>call_id</strong> <code>string</code> <strong>（必选）</strong></p><p>工具调用标识符，使用模型返回的 <code>call_id</code>。</p><p><strong>output</strong> <code>string</code> <strong>（必选）</strong></p><p>自定义工具的执行结果，通过 <code>call_id</code> 关联对应的调用。</p></div></section><p><strong>Function Call</strong> <code>object</code> （可选）</p><p>模型决定调用外部工具时生成的结构化指令。</p><a id="accordion-属性-15"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>固定为 <code>function_call</code>。</p><p><strong>id</strong> <code>string</code> （可选）</p><p>Function Call 的唯一标识，来自上一轮响应。</p><p><strong>name</strong> <code>string</code> <strong>（必选）</strong></p><p>工具函数名称。</p><p><strong>namespace</strong> <code>string</code> （可选）</p><p>工具所属的命名空间。调用命名空间内的 <code>function</code> 或 <code>custom</code> 工具时返回，回传调用项时保留该字段。</p><p><strong>arguments</strong> <code>string</code> <strong>（必选）</strong></p><p>工具调用参数，JSON 字符串格式。</p><p><strong>call_id</strong> <code>string</code> <strong>（必选）</strong></p><p>工具调用的标识符，需与模型返回的 <code>call_id</code> 一致。</p><p><strong>status</strong> <code>string</code> （可选）</p><p>状态，可选值：<code>in_progress</code>、<code>completed</code>、<code>incomplete</code>。</p></div></section><p><strong>Function Call Output</strong> <code>object</code> （可选）</p><p>工具调用的输出结果。在消息列表中<strong>必须</strong>紧跟对应的 <code>function_call</code> 消息，否则会报错。</p><a id="accordion-属性-16"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>固定为 <code>function_call_output</code>。</p><p><strong>id</strong> <code>string</code> （可选）</p><p>Function Call Output 的唯一标识。</p><p><strong>call_id</strong> <code>string</code> <strong>（必选）</strong></p><p>工具调用的标识符，需与模型返回的 <code>call_id</code> 一致。</p><p><strong>output</strong> <code>string 或 array</code> <strong>（必选）</strong></p><p>工具函数的执行结果。纯文本结果传入 string；需要模型理解工具产出的图片时传入 array，一个 output 中可包含多张图片。图片 URL 作为 string 传入时按普通文本处理，不会被解析为图片。</p><a id="accordion-array-元素类型-2"></a><section><p>array 元素类型</p><div><p>以下类型之一，不支持 <code>input_file</code>、<code>output_text</code> 以及音频、视频类型：</p><p><strong>input_text</strong> <code>{ type, text }</code></p><p>文本结果。</p><a id="accordion-属性-17"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>固定为 <code>input_text</code>。</p><p><strong>text</strong> <code>string</code> <strong>（必选）</strong></p><p>文本内容。</p></div></section><p><strong>input_image</strong> <code>{ type, image_url }</code></p><p>图片结果。</p><a id="accordion-属性-18"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>固定为 <code>input_image</code>。</p><p><strong>image_url</strong> <code>string</code> <strong>（必选）</strong></p><p>图片的公网 URL 或 Base64 编码。Base64 请传入完整的 Data URI，例如：<code>data:image/png;base64,iVBORw0K...</code>。此处为 string 类型，不支持 <code>{&quot;url&quot;: &quot;...&quot;}</code> 嵌套对象形式。</p></div></section></div></section><p><strong>status</strong> <code>string</code> （可选）</p><p>状态，可选值：<code>in_progress</code>、<code>completed</code>、<code>incomplete</code>。</p></div></section><p><strong>Reasoning</strong> <code>object</code> （可选）</p><p>模型的思考内容。可直接将上一轮响应的 output 中的 reasoning 项传回 input，用于在多轮对话中传递思考内容。</p><a id="accordion-属性-19"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>固定为 <code>reasoning</code>。</p><p><strong>id</strong> <code>string</code> <strong>（必选）</strong></p><p>思考内容的唯一标识，来自上一轮响应。</p><p><strong>encrypted_content</strong> <code>string</code></p><p><code>qwen4-max</code>, <code>reasoning.summary=&quot;auto&quot;</code>: Responses 的 reasoning item 包含 <code>summary</code>（<code>summary_text</code> 元素）和 <code>encrypted_content</code>。摘要按文本增量返回，密文在 reasoning item 完成事件及最终 response 中返回；可从完成快照补齐密文，不要重复追加摘要。 <a href="../../../model-user-guide/model-experience/text-generation-model/cot-summary.md#multi-turn">思维链摘要与加密</a>.</p><p><strong>summary</strong> <code>array</code> <strong>（必选）</strong></p><p>思考摘要内容。</p><a id="accordion-属性-20"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>固定为 <code>summary_text</code>。</p><p><strong>text</strong> <code>string</code> <strong>（必选）</strong></p><p>摘要文本。</p></div></section><p><strong>status</strong> <code>string</code> （可选）</p><p>状态，可选值：<code>in_progress</code>、<code>completed</code>、<code>incomplete</code>。</p></div></section><p><strong>Web Search Call</strong> <code>object</code> （可选）</p><p>搜索调用对象。可直接将上一轮响应的 output 中的 web_search_call 项传回 input，用于在多轮对话中传递搜索结果上下文。</p><a id="accordion-属性-21"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>固定为 <code>web_search_call</code>。</p><p><strong>id</strong> <code>string</code> <strong>（必选）</strong></p><p>搜索调用的唯一标识，来自上一轮响应。</p><p><strong>status</strong> <code>string</code> <strong>（必选）</strong></p><p>搜索状态，可选值：<code>in_progress</code>、<code>searching</code>、<code>completed</code>、<code>failed</code>。</p><p><strong>action</strong> <code>object</code> <strong>（必选）</strong></p><p>搜索信息。仅支持 <code>search</code> 类型。</p><a id="accordion-属性-22"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>搜索类型，固定为 <code>search</code>。</p><p><strong>queries</strong> <code>array</code> （可选）</p><p>搜索查询词列表，元素类型为 string。</p><p><strong>sources</strong> <code>array</code> （可选）</p><p>搜索结果来源列表。</p><a id="accordion-属性-23"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>来源类型，固定为 <code>url</code>。</p><p><strong>url</strong> <code>string</code> <strong>（必选）</strong></p><p>来源 URL。</p></div></section></div></section></div></section></div></section><p><strong>instructions</strong><code>string</code> （可选）</p><p>作为系统指令插入到上下文的起始位置。使用 <code>previous_response_id</code> 时，上一轮指定的 <code>instructions</code> 不会传入本轮上下文。</p><p><strong>previous_response_id</strong> <code>string</code> （可选）</p><p>上一个响应的唯一 ID，当前响应<code>id</code>有效期为7天。使用此参数可创建多轮对话，服务端会自动检索并组合该轮次的输入与输出作为上下文。当同时提供 <code>input</code> 消息数组和 <code>previous_response_id</code> 时，<code>input</code> 中的新消息会追加到历史上下文之后。不能与 <code>conversation</code> 同时使用。</p><p><strong>conversation</strong> <code>string</code> （可选）</p><p>当前响应所属的会话（参考<a href="../../toolkits-and-frameworks/openai-compatible-conversations.md">Conversations API</a>）。会话中的历史项会自动作为上下文传入本次请求，本次请求的输入和输出也会在响应完成后自动添加到会话中。不能与 <code>previous_response_id</code> 同时使用。</p><p><strong>prompt_cache_options</strong> <code>object</code> (可选)</p><p>仅支持 <code>qwen4-max</code>。 请求顶层的缓存配置。 Python SDK 通过 <code>extra_body</code> 传入顶层非标准参数；Node.js SDK 和 curl 直接传入。 详见<a href="../../../model-user-guide/model-experience/text-generation-model/explicit-cache-qwen4.md">显式缓存（Qwen4）</a>。</p><a id="accordion-属性-24"></a><section><p>属性</p><div><p><strong>mode</strong> <code>string</code></p><p><code>implicit</code>（默认）：开启显式缓存，在最后一条输入消息末尾自动设置断点，与手动断点同时生效。</p><p><code>explicit</code>：开启显式缓存，必须设置手动断点才会创建缓存，没有断点时不生效。</p><p><strong>ttl</strong> <code>string</code> (可选)</p><p>缓存有效期，支持 <code>5m</code> 和 <code>1h</code>，默认为 <code>5m</code>。</p></div></section><p><strong>stream</strong> <code>boolean</code> （可选）默认值为 <code>false</code></p><p>是否开启流式输出。设置为 <code>true</code> 时，模型响应数据将实时流式返回给客户端。</p><p><strong>store</strong> <code>boolean</code> （可选）默认值为 <code>true</code></p><p>是否储存本次会话生成的模型响应。</p><ul><li><code>false</code>：不储存，对话内容不能被 <code>previous_response_id</code> 和后续 API 使用。</li><li><code>true</code>：储存，当前模型响应可被 <code>previous_response_id</code> 和后续 API 使用。</li></ul><p><strong>tools</strong> <code>array</code> （可选）</p><p>模型在生成响应时可调用的工具数组。支持内置工具、自定义 <code>function</code> 和 <code>custom</code> 工具；可通过 <code>namespace</code> 将相关工具分组。</p><p><code>kimi-k3.1-pro</code>（阿里云百炼部署）支持 <code>web_search</code>、<code>web_extractor</code> 和 <code>code_interpreter</code> 三项内置工具，适用于北京、新加坡、美国（弗吉尼亚）、德国（法兰克福）、日本（东京）和中国香港。</p><p><code>deepseek-v4.1-flash-1017</code> 支持 <code>web_search</code>、<code>web_extractor</code> 和 <code>code_interpreter</code> 三项内置工具。</p><p><code>qwen3.8-omni-flash</code> 的内置工具仅支持 <code>web_search</code>，同时支持自定义 <code>function</code> 工具。</p><a id="accordion-属性-25"></a><section><p>属性</p><div><strong>web_search</strong><p>联网搜索工具，允许模型搜索互联网上的最新信息。相关文档：<a href="../../../model-user-guide/model-experience/text-generation-model/tool-calls/web-search.md">联网搜索</a></p><p>注：codex 模式下，在 <code>tools</code> 中开启 <code>web_search</code> 会自动启用 <code>web_extractor</code>。</p><a id="accordion-属性-26"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>固定为<code>web_search</code>。</p><p>使用示例：<code>[{&quot;type&quot;: &quot;web_search&quot;}]</code></p></div></section><strong>web_extractor</strong><p>网页抽取工具，允许模型访问并提取网页内容。当前必须配合<code>web_search</code>工具一起使用。相关文档：<a href="../../../model-user-guide/model-experience/text-generation-model/tool-calls/web-extractor.md">网页抓取</a></p><a id="accordion-属性-27"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>固定为<code>web_extractor</code>。</p><p>使用示例：<code>[{&quot;type&quot;: &quot;web_search&quot;}, {&quot;type&quot;: &quot;web_extractor&quot;}]</code></p></div></section><strong>code_interpreter</strong><p>代码解释器工具，允许模型执行代码并返回结果，支持数据分析。相关文档：<a href="../../../model-user-guide/model-experience/text-generation-model/tool-calls/qwen-code-interpreter.md">代码解释器</a></p><a id="accordion-属性-28"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>固定为<code>code_interpreter</code>。</p><p>使用示例：<code>[{&quot;type&quot;: &quot;code_interpreter&quot;}]</code></p></div></section><strong>web_search_image</strong><p>根据文本描述搜索图片。相关文档：<a href="../../../model-user-guide/model-experience/text-generation-model/tool-calls/web-search-image.md">文搜图</a></p><a id="accordion-属性-29"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>固定为<code>web_search_image</code>。</p><p>使用示例：<code>[{&quot;type&quot;: &quot;web_search_image&quot;}]</code></p></div></section><strong>image_search</strong><p>根据图片搜索相似或相关图片，输入中需要包含图片的URL。相关文档：<a href="../../../model-user-guide/model-experience/text-generation-model/tool-calls/image-search.md">图搜图</a></p><a id="accordion-属性-30"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>固定为<code>image_search</code>。</p><p>使用示例：<code>[{&quot;type&quot;: &quot;image_search&quot;}]</code></p></div></section><strong>file_search</strong><p>在已上传或关联的知识库中搜索。相关文档：<a href="../../../model-user-guide/model-experience/text-generation-model/tool-calls/file-search.md">知识检索</a></p><a id="accordion-属性-31"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>固定为<code>file_search</code>。</p><p><strong>vector_store_ids</strong> <code>array</code><strong>（必选）</strong></p><p>要检索的知识库 ID。<strong>当前仅支持传入一个知识库 ID</strong>。</p><p>使用示例：<code>[{&quot;type&quot;: &quot;file_search&quot;, &quot;vector_store_ids&quot;: [&quot;your_knowledge_base_id&quot;]}]</code></p></div></section><strong>MCP调用</strong><p>通过 MCP（Model Context Protocol）调用外部服务，相关文档：<a href="../../../model-user-guide/model-experience/text-generation-model/tool-calls/mcp.md">MCP</a></p><a id="accordion-属性-32"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>固定为<code>mcp</code>。</p><p><strong>server_protocol</strong> <code>string</code> <strong>（必选）</strong></p><p>与 MCP 服务的通信协议，如 <code>&quot;sse&quot;</code></p><p><strong>server_label</strong> <code>string</code> <strong>（必选）</strong></p><p>服务标签，用于标识该 MCP 服务。</p><p><strong>server_description</strong> <code>string</code> （可选）</p><p>服务描述，帮助模型理解其功能与适用场景。</p><p><strong>server_url</strong> <code>string</code> <strong>（必选）</strong></p><p>MCP 服务端点的 URL。</p><p><strong>headers</strong> <code>object</code> （可选）</p><p>请求头，用于携带身份验证等信息，如 <code>Authorization</code>。</p><p>使用示例：</p><a id="code-block"></a><pre class="language-json"><code>mcp_tool = {
    &quot;type&quot;: &quot;mcp&quot;,
    &quot;server_protocol&quot;: &quot;sse&quot;,
    &quot;server_label&quot;: &quot;amap-maps&quot;,
    &quot;server_description&quot;: &quot;高德地图MCP Server现已覆盖15大核心接口，提供全场景覆盖的地理信息服务，包括生成专属地图、导航到目的地、打车、地理编码、逆地理编码、IP定位、天气查询、骑行路径规划、步行路径规划、驾车路径规划、公交路径规划、距离测量、关键词搜索、周边搜索、详情搜索等。&quot;,
    &quot;server_url&quot;: &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/mcps/amap-maps/sse&quot;,
    &quot;headers&quot;: {
        &quot;Authorization&quot;: &quot;Bearer &lt;your-mcp-server-token&gt;&quot;
    }
}
</code></pre></div></section><strong>自定义工具</strong><strong>function</strong><p>自定义函数工具，允许模型调用您定义的函数。当模型判断需要调用工具时，响应会返回 <code>function_call</code> 类型的输出。相关文档：<a href="../../../model-user-guide/model-experience/text-generation-model/tool-calls/qwen-function-calling.md">Function Calling</a></p><a id="accordion-属性-33"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>必须设置为<code>function</code>。</p><p><strong>name</strong><code>string</code><strong>（必选）</strong></p><p>工具名称。仅允许字母、数字、下划线（<code>_</code>）和短划线（<code>-</code>），最长 64 个 Token。</p><p><strong>description</strong><code>string</code><strong>（必选）</strong></p><p>工具描述信息，帮助模型判断何时以及如何调用该工具。</p><p><strong>parameters</strong> <code>object</code> （可选）</p><p>工具的参数描述，需要是一个合法的 <a href="https://json-schema.org/understanding-json-schema">JSON Schema</a>。若<code>parameters</code>参数为空，表示该工具没有入参（如时间查询工具）。</p><blockquote><p>为提高工具调用的准确性，建议传入 <code>parameters</code>。</p></blockquote><p>使用示例：</p><a id="code-block-2"></a><pre class="language-json"><code>[{
  &quot;type&quot;: &quot;function&quot;,
  &quot;name&quot;: &quot;get_weather&quot;,
  &quot;description&quot;: &quot;获取指定城市的天气信息&quot;,
  &quot;parameters&quot;: {
    &quot;type&quot;: &quot;object&quot;,
    &quot;properties&quot;: {
      &quot;city&quot;: {
        &quot;type&quot;: &quot;string&quot;,
        &quot;description&quot;: &quot;城市名称&quot;
      }
    },
    &quot;required&quot;: [&quot;city&quot;]
  }
}]
</code></pre></div></section><strong>自定义工具</strong><strong>custom</strong><p>自定义格式工具，调用输入为自由文本，可通过 Lark 或 Regex 文法描述输入格式。模型返回 <code>custom_tool_call</code>，工具输入位于 <code>input</code> 字段。</p><a id="accordion-属性-34"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>固定为 <code>custom</code>。</p><p><strong>name</strong> <code>string</code> <strong>（必选）</strong></p><p>工具名称，例如 <code>emit_code</code>。</p><p><strong>description</strong> <code>string</code> （可选）</p><p>工具描述，说明用途及调用时机。</p><p><strong>format</strong> <code>object</code> （可选）</p><p>工具输入的格式配置。</p><p>若工具依赖特定的文法结构（如 <code>apply_patch</code> 补丁文件格式），建议将 <code>format.type</code> 设置为 <code>grammar</code> 并提供文法规则，帮助模型按指定格式生成调用输入。</p><p>当 <code>format.type</code> 为 <code>grammar</code> 时，需配对提供 <code>syntax</code> 和 <code>definition</code>；为 <code>text</code> 时，表示无约束的自由文本，<code>syntax</code> 和 <code>definition</code> 均可选。</p><a id="accordion-属性-35"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> （可选）</p><p>取值为 <code>text</code>（无特定文法约束的自由文本）或 <code>grammar</code>（文法格式）。</p><p><strong>syntax</strong> <code>string</code> （可选）</p><p>文法语法类型：<code>lark</code> 或 <code>regex</code>。</p><p><strong>definition</strong> <code>string</code> （可选）</p><p>文法规则定义。Lark 使用产生式，Regex 使用正则表达式。</p></div></section></div></section><p>以下对象作为 <code>tools</code> 数组的一个元素传入。</p><a id="code-block-3"></a><pre class="language-json"><code>{
  &quot;type&quot;: &quot;custom&quot;,
  &quot;name&quot;: &quot;apply_patch&quot;,
  &quot;description&quot;: &quot;Use the `apply_patch` tool to edit files. This is a FREEFORM tool, so do not wrap the patch in JSON.&quot;,
  &quot;format&quot;: {
    &quot;type&quot;: &quot;grammar&quot;,
    &quot;syntax&quot;: &quot;lark&quot;,
    &quot;definition&quot;: &quot;start: begin_patch hunk+ end_patch\nbegin_patch: \&quot;*** Begin Patch\&quot; LF\nend_patch: \&quot;*** End Patch\&quot; LF?\n\nhunk: add_hunk | delete_hunk | update_hunk\nadd_hunk: \&quot;*** Add File: \&quot; filename LF add_line+\ndelete_hunk: \&quot;*** Delete File: \&quot; filename LF\nupdate_hunk: \&quot;*** Update File: \&quot; filename LF change_move? change?\n\nfilename: /[^\\n]+/\nadd_line: ADD_LINE\nADD_LINE: /\\+[^\\n]*\\n/\n\nchange_move: \&quot;*** Move to: \&quot; filename LF\nchange: (change_context | change_line)+ eof_line?\nchange_context: CONTEXT_LINE\nCONTEXT_LINE: /@@[^\\n]*\\n/\nchange_line: CHANGE_LINE\nCHANGE_LINE: /[+\\- ][^\\n]*\\n/\neof_line: \&quot;*** End of File\&quot; LF\n\n%import common.LF\n&quot;
  }
}
</code></pre><strong>命名空间</strong><strong>namespace</strong><p>将相关的 <code>function</code> 或 <code>custom</code> 工具归拢在同一命名空间中。</p><a id="accordion-属性-36"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>固定为 <code>namespace</code>。</p><p><strong>name</strong> <code>string</code> <strong>（必选）</strong></p><p>命名空间名称，例如 <code>crm</code>。</p><p><strong>description</strong> <code>string</code> （可选）</p><p>命名空间的整体描述。</p><p><strong>tools</strong> <code>array[object]</code> <strong>（必选）</strong></p><p>命名空间内的工具列表。每个元素为 <code>function</code> 或 <code>custom</code> 工具对象，字段与对应工具定义相同。</p></div></section><p>以下对象作为 <code>tools</code> 数组的一个元素传入。</p><a id="code-block-4"></a><pre class="language-json"><code>{
  &quot;type&quot;: &quot;namespace&quot;,
  &quot;name&quot;: &quot;crm&quot;,
  &quot;description&quot;: &quot;Customer Relationship Management tools&quot;,
  &quot;tools&quot;: [
    {
      &quot;type&quot;: &quot;function&quot;,
      &quot;name&quot;: &quot;get_customer&quot;,
      &quot;description&quot;: &quot;Get customer details by ID&quot;,
      &quot;parameters&quot;: {
        &quot;type&quot;: &quot;object&quot;,
        &quot;properties&quot;: {
          &quot;customer_id&quot;: {
            &quot;type&quot;: &quot;string&quot;
          }
        },
        &quot;required&quot;: [
          &quot;customer_id&quot;
        ]
      }
    },
    {
      &quot;type&quot;: &quot;custom&quot;,
      &quot;name&quot;: &quot;import_patch&quot;,
      &quot;description&quot;: &quot;Import customer batch patch&quot;,
      &quot;format&quot;: {
        &quot;type&quot;: &quot;text&quot;
      }
    }
  ]
}
</code></pre></div></section><p><strong>tool_choice</strong> <code>string or object</code> （可选）默认值为 <code>auto</code></p><p>控制模型如何选择和调用工具。此参数支持两种赋值格式：<strong>字符串模式</strong>和<strong>对象模式</strong>。</p><strong>字符串模式</strong><ul><li><code>auto</code>：模型自动决定是否调用工具。</li><li><code>none</code>：禁止模型调用任何工具。</li><li><code>required</code>：强制模型调用工具（仅当 <code>tools</code> 列表中只有一个工具时可用）。</li></ul><strong>对象模式</strong><p>为模型设定可用的工具范围，仅限在预定义的工具列表中进行选择和调用。</p><a id="accordion-属性-37"></a><section><p>属性</p><div><p><strong>mode</strong> <code>string</code> <strong>（必选）</strong></p><ul><li><code>auto</code>：模型自动决定是否调用工具。</li><li><code>required</code>：强制模型调用工具（仅当 <code>tools</code> 列表中只有一个工具时可用）。</li></ul><p><strong>tools</strong> <code>array</code><strong>（必选）</strong></p><p>一个包含工具定义的列表，模型将被允许调用这些工具。</p><a id="code-block-5"></a><pre class="language-json"><code>[
  { &quot;type&quot;: &quot;function&quot;, &quot;name&quot;: &quot;get_weather&quot; }
]
</code></pre><p><strong>type</strong><code>string</code> <strong>（必选）</strong></p><p>允许的工具配置类型，固定为 <code>allowed_tools</code>。</p></div></section><p><strong>parallel_tool_calls</strong> <code>boolean</code> （可选）默认值为 <code>true</code></p><p>是否开启并行工具调用。相关文档：<a href="../../../model-user-guide/model-experience/text-generation-model/tool-calls/qwen-function-calling.md#cb6b5c484bt4x">并行工具调用</a></p><blockquote><p>kimi-k3 不支持通过此参数控制工具调用的并行性。设置为 <code>false</code> 也不能保证串行调用，模型仍可能在一次响应中返回多个 <code>function_call</code>。请按实际返回结果处理。</p></blockquote><p>可选值：</p><ul><li><code>true</code>：开启</li><li><code>false</code>：不开启</li></ul><p><strong>temperature</strong><code>float</code>（可选）</p><p><code>qwen4-max</code>：思考模式为 <code>1.0</code>，非思考模式为 <code>0.7</code>。</p><p>采样温度，控制模型生成文本的多样性。</p><p>temperature越高，生成的文本更多样，反之，生成的文本更确定。</p><p>取值范围： [0, 2)</p><p>temperature与top_p均可以控制生成文本的多样性，建议只设置其中一个值。更多说明，请参见<a href="../../../model-user-guide/model-experience/text-generation-model/text-generation.md">概述</a>。</p><p><strong>top_p</strong><code>float</code>（可选）</p><p><code>qwen4-max</code>：思考模式为 <code>0.95</code>，非思考模式为 <code>0.8</code>。</p><p>核采样的概率阈值，控制模型生成文本的多样性。</p><p>top_p越高，生成的文本更多样。反之，生成的文本更确定。</p><p>取值范围：（0,1.0]</p><p>temperature与top_p均可以控制生成文本的多样性，建议只设置其中一个值。更多说明，请参见<a href="../../../model-user-guide/model-experience/text-generation-model/text-generation.md">概述</a>。</p><p><strong>enable_thinking</strong> <code>boolean</code> （可选）</p><p>是否开启思考模式。开启后，模型会在回复前进行思考，思考内容将通过 <code>reasoning</code> 类型的输出项返回。开启思考模式时，<strong>建议开启</strong>内置工具，以在处理复杂任务时获得最佳的模型效果。</p><p>可选值：</p><ul><li><code>true</code>：开启</li><li><code>false</code>：不开启</li></ul><p>不同模型的默认值：<a href="../../../model-user-guide/model-experience/text-generation-model/deep-thinking.md#78286fdc35hlw">支持的模型</a></p><blockquote><p>该参数非OpenAI标准参数。Python SDK 通过 <code>extra_body={&quot;enable_thinking&quot;: True}</code> 传递；Node.js SDK 和 curl 直接使用 <code>enable_thinking: true</code> 作为顶层参数。建议使用 <code>reasoning.effort</code> 替代，<code>enable_thinking</code> 后续将不再支持。</p></blockquote><p><strong>reasoning</strong> <code>object</code> （可选）</p><p>控制模型的思考强度。模型会在回复前进行思考，思考内容将通过 <code>reasoning</code> 类型的输出项返回。</p><p>kimi-k3.1-pro（阿里云百炼部署）的 <code>reasoning.effort</code> 默认值为 <code>max</code>，支持 <code>max</code>（深度推理）、<code>high</code>（增强推理）、<code>medium</code>（中度推理）和 <code>low</code>（轻度推理）。建议保持默认思考配置，关闭思考会显著影响输出效果。</p><a id="accordion-属性-38"></a><section><p>属性</p><div><p>kimi-k3.1-pro 的档位与默认值以上述说明为准，以下说明适用于其他模型。</p><p><strong>effort</strong> <code>string</code> （可选）：思考强度档位。</p><p><strong><code>qwen4-max</code></strong></p><p>默认值: <code>reasoning.effort=high</code>.</p><table><thead><tr><th><code>reasoning.effort</code></th><th>实际档位</th></tr></thead><tbody><tr><td><code>minimal</code>, <code>low</code></td><td><code>low</code></td></tr><tr><td><code>medium</code>, <code>high</code></td><td><code>high</code></td></tr><tr><td><code>xhigh</code>, <code>max</code></td><td><code>xhigh</code></td></tr><tr><td><code>none</code></td><td>关闭思考</td></tr></tbody></table><p>仅设置 <code>reasoning.effort</code> 时，思考长度上限默认为 <code>131072</code> Token。</p><p>支持 <code>none</code>、<code>minimal</code>、<code>low</code>、<code>medium</code>、<code>high</code>、<code>xhigh</code>、<code>max</code> 共 7 个递增档位。降低该值可加快响应速度并减少推理 Token 的消耗。</p><table><thead><tr><th>模型</th><th>支持的档位</th><th>其余档位的映射</th></tr></thead><tbody><tr><td><code>qwen3.8-max</code>、<code>qwen3.8-max-0902</code>、<code>qwen3.8-flash</code>、<code>qwen3.8-2.4t-a95b</code>、<code>qwen3.8-27b</code></td><td><code>none</code>、<code>low</code>、<code>medium</code>、<code>xhigh</code>（默认）</td><td><code>minimal</code> 映射为 <code>low</code>，<code>high</code> 和 <code>max</code> 映射为 <code>xhigh</code></td></tr><tr><td><code>deepseek-v4-flash-0731</code>、<code>deepseek-v4-pro-0813</code></td><td><code>none</code>、<code>low</code>、<code>high</code>（默认）、<code>max</code></td><td><code>minimal</code> 映射为 <code>low</code>，<code>medium</code> 映射为 <code>high</code>，<code>xhigh</code> 映射为 <code>max</code></td></tr><tr><td><code>deepseek-v4.1-flash</code></td><td><code>none</code>、<code>low</code>、<code>high</code>（默认）、<code>max</code></td><td><code>minimal</code> 映射为 <code>low</code>，<code>medium</code> 和 <code>xhigh</code> 映射为 <code>high</code>，传入 <code>ultra</code> 会返回错误</td></tr><tr><td><code>glm-5.3</code></td><td><code>low</code>、<code>high</code>、<code>max</code>（默认）</td><td><code>minimal</code> 映射为 <code>low</code>，<code>medium</code> 映射为 <code>high</code>，<code>xhigh</code> 映射为 <code>max</code></td></tr><tr><td><code>glm-5.2</code>、<code>deepseek-v4-pro</code></td><td><code>none</code>、<code>high</code>（默认）、<code>max</code></td><td><code>minimal</code>、<code>low</code> 和 <code>medium</code> 映射为 <code>high</code>，<code>xhigh</code> 映射为 <code>max</code></td></tr></tbody></table><p><code>glm-5.3</code> 推荐使用 <code>max</code> 档位。</p><p><strong>summary</strong> <code>string</code> （可选）</p><p><code>qwen4-max</code>: <code>&quot;auto&quot;</code>. <a href="../../../model-user-guide/model-experience/text-generation-model/cot-summary.md#responses">思维链摘要与加密</a>.</p><p>默认返回完整思维链。开启本功能后，原始思维链不再以明文返回，改为返回摘要与完整密文。摘要用于展示，密文用于恢复历史思考。</p></div></section><blockquote><p><code>reasoning.effort</code> 的优先级高于 <code>enable_thinking</code>，建议优先使用 <code>reasoning.effort</code>，<code>enable_thinking</code> 后续将不再支持。</p></blockquote><p><strong>ocr_options</strong> <code>object</code> （可选）</p><p>OCR 定制任务参数。仅适用于 <code>qwen3.5-ocr</code> 模型。通过此参数可调用内置的 OCR 任务（如信息抽取、文字定位等），定制任务结果通过响应中的 <code>ocr_result</code> 字段返回。</p><p>解析 PDF 文件时，<code>task</code> 的取值决定支持的页数：设置为 <code>document_parsing</code> 时最大 50 页；未设置 <code>task</code> 或设置为其他任务时，最大 10 页。</p><blockquote><p>该参数非 OpenAI 标准参数。Python SDK 通过 <code>extra_body={&quot;ocr_options&quot;: {...}}</code> 传递；Node.js SDK 和 curl 直接使用 <code>ocr_options</code> 作为顶层参数。</p></blockquote><p><strong>max_output_tokens</strong> <code>integer</code>（可选）</p><p><code>qwen4-max</code>：思考模式限制思考与回复的 Token 总数，最大值和未传入时的默认值均为 <code>262144</code>；非思考模式最大值和默认值均为 <code>131072</code>。</p><p>限制生成输出的 Token 数量。</p><ul><li>Qwen3.8 系列：模型回复内容和思维链之和的最大Token数。</li><li>Qwen3.7、Qwen3.6、Qwen3.5、Qwen3-Max、DeepSeek、GLM 和 Kimi：模型回复内容的最大Token数。</li></ul><p>上述型号的最小值为16。生成的 Token 数达到所设置的上限时，生成将提前停止，状态为<code>incomplete</code>。</p><p><strong>text</strong> <code>object</code> （可选）</p><p>文本输出配置，用于控制模型输出纯文本或结构化 JSON 数据。</p><a id="accordion-属性-39"></a><section><p>属性</p><div><p><strong>format</strong> <code>object</code> （可选）</p><p>指定模型必须输出的格式。默认值为 <code>{&quot;type&quot;: &quot;text&quot;}</code>。</p><p>以下类型之一：</p><p><strong>ResponseFormatText</strong> <code>{ type }</code></p><p>默认值，输出文字。</p><a id="accordion-属性-40"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>固定为 <code>text</code>。</p></div></section><p><strong>ResponseFormatTextJSONSchemaConfig</strong> <code>{ type, json_schema }</code></p><p>输出严格符合指定 JSON Schema 的 JSON 字符串，可精确控制输出结构与字段类型。适用于 qwen3.8 系列、deepseek-v4 系列、glm-5 系列等模型；deepseek-v4.1 系列即将支持。使用该类型时，提示词无需包含 JSON 关键词。</p><a id="accordion-属性-41"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>固定为 <code>json_schema</code>。</p><p><strong>json_schema</strong> <code>object</code> <strong>（必选）</strong></p><p>JSON Schema 配置。</p><a id="accordion-属性-42"></a><section><p>属性</p><div><p><strong>name</strong> <code>string</code> <strong>（必选）</strong></p><p>Schema 的名称。</p><p><strong>schema</strong> <code>object</code> <strong>（必选）</strong></p><p>描述输出结构的 JSON Schema 对象。通过 <code>properties</code> 定义字段结构，通过 <code>required</code> 声明必填字段列表，通过 <code>additionalProperties</code> 控制是否允许输出未在 Schema 中定义的字段（推荐设置为 <code>false</code>，即只输出已定义的字段）。支持的数据类型：string、number、integer、boolean、object、array、enum。相关文档：<a href="../../../model-user-guide/model-experience/text-generation-model/qwen-structured-output.md#001cb6ae072tc">配置指南</a>。</p><p><strong>strict</strong> <code>boolean</code> （可选）</p><p>是否严格遵循 <code>schema</code> 定义的结构。推荐设置为 <code>true</code>。</p></div></section></div></section><p><strong>ResponseFormatJSONObject</strong> <code>{ type }</code></p><p>输出标准格式的 JSON 字符串。适用于 qwen3.8 系列、deepseek-v4 系列、deepseek-v4.1 系列、glm-5 系列模型及 kimi-k3.1-pro（阿里云百炼部署）。使用该类型时，需在提示词中明确指示模型输出 JSON，如：“请按照json格式输出”，否则会报错。</p><a id="accordion-属性-43"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>固定为 <code>json_object</code>。</p></div></section></div></section></td><td><div><a id="sec-tabs-2"></a><section><a id="基础调用"></a><section><a id="基础调用-h4"></a><h4>基础调用</h4><a id="fig-code-group"></a><div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    base_url=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;,
)

response = client.responses.create(
    model=&quot;qwen4-max&quot;,
    input=&quot;你能做些什么？&quot;
)

# 获取模型回复
print(response.output_text)
</code></pre></div><a id="fig-code-group-node-js-tab"></a>Node.js<div><a id="code-code-group-node-js"></a><pre class="language-javascript"><code>import OpenAI from &quot;openai&quot;;

const openai = new OpenAI({
    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: &quot;sk-xxx&quot;
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;
});

async function main() {
    const response = await openai.responses.create({
        model: &quot;qwen4-max&quot;,
        input: &quot;你能做些什么？&quot;
    });

    // 获取模型回复
    console.log(response.output_text);
}

main();
</code></pre></div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/responses \
-H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
-H &quot;Content-Type: application/json&quot; \
-d '{
    &quot;model&quot;: &quot;qwen4-max&quot;,
    &quot;input&quot;: &quot;你能做些什么？&quot;
}'
</code></pre></div></div></section><a id="流式输出"></a><section><a id="流式输出-h4"></a><h4>流式输出</h4><a id="fig-code-group-2"></a><div><a id="fig-code-group-2-python-tab"></a>Python<div><a id="code-code-group-2-python"></a><pre class="language-python"><code>import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    base_url=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;,
)

stream = client.responses.create(
    model=&quot;qwen4-max&quot;,
    input=&quot;请简单介绍一下人工智能。&quot;,
    stream=True
)

print(&quot;开始接收流式输出:&quot;)
for event in stream:
    if event.type == 'response.output_text.delta':
        print(event.delta, end='', flush=True)
    elif event.type == 'response.completed':
        print(&quot;\n流式输出完成&quot;)
        print(f&quot;总Token数: {event.response.usage.total_tokens}&quot;)
</code></pre></div><a id="fig-code-group-2-node-js-tab"></a>Node.js<div><a id="code-code-group-2-node-js"></a><pre class="language-javascript"><code>import OpenAI from &quot;openai&quot;;

const openai = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;
});

async function main() {
    const stream = await openai.responses.create({
        model: &quot;qwen4-max&quot;,
        input: &quot;请简单介绍一下人工智能。&quot;,
        stream: true
    });

    console.log(&quot;开始接收流式输出:&quot;);
    for await (const event of stream) {
        if (event.type === 'response.output_text.delta') {
            process.stdout.write(event.delta);
        } else if (event.type === 'response.completed') {
            console.log(&quot;\n流式输出完成&quot;);
            console.log(`总Token数: ${event.response.usage.total_tokens}`);
        }
    }
}

main();
</code></pre></div><a id="fig-code-group-2-curl-tab"></a>curl<div><a id="code-code-group-2-curl"></a><pre class="language-bash"><code>curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/responses \
-H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
-H &quot;Content-Type: application/json&quot; \
--no-buffer \
-d '{
    &quot;model&quot;: &quot;qwen4-max&quot;,
    &quot;input&quot;: &quot;请简单介绍一下人工智能。&quot;,
    &quot;stream&quot;: true
}'
</code></pre></div></div></section><a id="多轮对话"></a><section><a id="多轮对话-h4"></a><h4>多轮对话</h4><a id="fig-code-group-3"></a><div><a id="fig-code-group-3-python-tab"></a>Python<div><a id="code-code-group-3-python"></a><pre class="language-python"><code>import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    base_url=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;,
)

# 第一轮对话
response1 = client.responses.create(
    model=&quot;qwen4-max&quot;,
    input=&quot;我的名字是张三，请记住。&quot;
)
print(f&quot;第一轮回复: {response1.output_text}&quot;)

# 第二轮对话 - 使用 previous_response_id 关联上下文，响应id有效期为7天
response2 = client.responses.create(
    model=&quot;qwen4-max&quot;,
    input=&quot;你还记得我的名字吗？&quot;,
    previous_response_id=response1.id
)
print(f&quot;第二轮回复: {response2.output_text}&quot;)
</code></pre></div><a id="fig-code-group-3-node-js-tab"></a>Node.js<div><a id="code-code-group-3-node-js"></a><pre class="language-javascript"><code>import OpenAI from &quot;openai&quot;;

const openai = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;
});

async function main() {
    // 第一轮对话
    const response1 = await openai.responses.create({
        model: &quot;qwen4-max&quot;,
        input: &quot;我的名字是张三，请记住。&quot;
    });
    console.log(`第一轮回复: ${response1.output_text}`);

    // 第二轮对话 - 使用 previous_response_id 关联上下文，响应id有效期为7天
    const response2 = await openai.responses.create({
        model: &quot;qwen4-max&quot;,
        input: &quot;你还记得我的名字吗？&quot;,
        previous_response_id: response1.id
    });
    console.log(`第二轮回复: ${response2.output_text}`);
}

main();
</code></pre></div></div></section><a id="调用内置工具"></a><section><a id="调用内置工具-h4"></a><h4>调用内置工具</h4><a id="fig-code-group-4"></a><div><a id="fig-code-group-4-python-tab"></a>Python<div><a id="code-code-group-4-python"></a><pre class="language-python"><code>import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    base_url=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;,
)

response = client.responses.create(
    model=&quot;qwen4-max&quot;,
    input=&quot;帮我找一下阿里云官网，并提取首页的关键信息&quot;,
    # 建议同时开启内置工具以取得最佳效果
    tools=[
        {&quot;type&quot;: &quot;web_search&quot;},
        {&quot;type&quot;: &quot;code_interpreter&quot;},
        {&quot;type&quot;: &quot;web_extractor&quot;}
    ],
)

# 取消以下注释查看中间过程输出
# print(response.output)
print(response.output_text)
</code></pre></div><a id="fig-code-group-4-node-js-tab"></a>Node.js<div><a id="code-code-group-4-node-js"></a><pre class="language-javascript"><code>import OpenAI from &quot;openai&quot;;

const openai = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;
});

async function main() {
    const response = await openai.responses.create({
        model: &quot;qwen4-max&quot;,
        input: &quot;帮我找一下阿里云官网，并提取首页的关键信息&quot;,
        tools: [
            { type: &quot;web_search&quot; },
            { type: &quot;code_interpreter&quot; },
            { type: &quot;web_extractor&quot; }
        ]
    });

    for (const item of response.output) {
        if (item.type === &quot;reasoning&quot;) {
            console.log(&quot;模型正在思考...&quot;);
        } else if (item.type === &quot;web_search_call&quot;) {
            console.log(`搜索查询: ${item.action.query}`);
        } else if (item.type === &quot;web_extractor_call&quot;) {
            console.log(&quot;正在抽取网页内容...&quot;);
        } else if (item.type === &quot;message&quot;) {
            console.log(`回复内容: ${item.content[0].text}`);
        }
    }
}

main();
</code></pre></div><a id="fig-code-group-4-curl-tab"></a>curl<div><a id="code-code-group-4-curl"></a><pre class="language-bash"><code>curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/responses \
-H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
-H &quot;Content-Type: application/json&quot; \
-d '{
    &quot;model&quot;: &quot;qwen4-max&quot;,
    &quot;input&quot;: &quot;帮我找一下阿里云官网，并提取首页的关键信息&quot;,
    &quot;tools&quot;: [
        {
            &quot;type&quot;: &quot;web_search&quot;
        },
        {
            &quot;type&quot;: &quot;code_interpreter&quot;
        },
        {
            &quot;type&quot;: &quot;web_extractor&quot;
        }
    ]
}'
</code></pre></div></div></section><a id="自定义-function-call"></a><section><a id="自定义-function-call-h4"></a><h4>自定义 Function Call</h4><a id="fig-code-group-5"></a><div><a id="fig-code-group-5-python-tab"></a>Python<div><a id="code-code-group-5-python"></a><pre class="language-python"><code>from openai import OpenAI
import json
import os
import random

# 初始化客户端
client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;,
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    base_url=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;,
)
# 模拟用户问题
USER_QUESTION = &quot;北京天气咋样&quot;
# 定义工具列表
tools = [
    {
        &quot;type&quot;: &quot;function&quot;,
        &quot;name&quot;: &quot;get_current_weather&quot;,
        &quot;description&quot;: &quot;当你想查询指定城市的天气时非常有用。&quot;,
        &quot;parameters&quot;: {
            &quot;type&quot;: &quot;object&quot;,
            &quot;properties&quot;: {
                &quot;location&quot;: {
                    &quot;type&quot;: &quot;string&quot;,
                    &quot;description&quot;: &quot;城市或县区，比如北京市、杭州市、余杭区等。&quot;,
                }
            },
            &quot;required&quot;: [&quot;location&quot;],
        },
    }
]

# 模拟天气查询工具
def get_current_weather(arguments):
    weather_conditions = [&quot;晴天&quot;, &quot;多云&quot;, &quot;雨天&quot;]
    random_weather = random.choice(weather_conditions)
    location = arguments[&quot;location&quot;]
    return f&quot;{location}今天是{random_weather}。&quot;

# 封装模型响应函数
def get_response(input_data):
    response = client.responses.create(
        model=&quot;qwen4-max&quot;,
        input=input_data,
        tools=tools,
    )
    return response

# 维护对话上下文
conversation = [{&quot;role&quot;: &quot;user&quot;, &quot;content&quot;: USER_QUESTION}]

response = get_response(conversation)
function_calls = [item for item in response.output if item.type == &quot;function_call&quot;]
# 如果不需要调用工具，直接输出内容
if not function_calls:
    print(f&quot;助手最终回复：{response.output_text}&quot;)
else:
    # 进入工具调用循环
    while function_calls:
        for fc in function_calls:
            func_name = fc.name
            arguments = json.loads(fc.arguments)
            print(f&quot;正在调用工具 [{func_name}]，参数：{arguments}&quot;)
            # 执行工具
            tool_result = get_current_weather(arguments)
            print(f&quot;工具返回：{tool_result}&quot;)
            # 将工具调用和结果成对追加到上下文中
            conversation.append(
                {
                    &quot;type&quot;: &quot;function_call&quot;,
                    &quot;name&quot;: fc.name,
                    &quot;arguments&quot;: fc.arguments,
                    &quot;call_id&quot;: fc.call_id,
                }
            )
            conversation.append(
                {
                    &quot;type&quot;: &quot;function_call_output&quot;,
                    &quot;call_id&quot;: fc.call_id,
                    &quot;output&quot;: tool_result,
                }
            )
        # 携带完整上下文再次调用模型
        response = get_response(conversation)
        function_calls = [
            item for item in response.output if item.type == &quot;function_call&quot;
        ]
    print(f&quot;助手最终回复：{response.output_text}&quot;)
</code></pre></div><a id="fig-code-group-5-node-js-tab"></a>Node.js<div><a id="code-code-group-5-node-js"></a><pre class="language-javascript"><code>import OpenAI from &quot;openai&quot;;

// 初始化客户端
const openai = new OpenAI({
  // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：apiKey: &quot;sk-xxx&quot;,
  apiKey: process.env.DASHSCOPE_API_KEY,
  baseURL:
    &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;,
});

// 定义工具列表
const tools = [
  {
    type: &quot;function&quot;,
    name: &quot;get_current_weather&quot;,
    description: &quot;当你想查询指定城市的天气时非常有用。&quot;,
    parameters: {
      type: &quot;object&quot;,
      properties: {
        location: {
          type: &quot;string&quot;,
          description: &quot;城市或县区，比如北京市、杭州市、余杭区等。&quot;,
        },
      },
      required: [&quot;location&quot;],
    },
  },
];

// 模拟天气查询工具
const getCurrentWeather = (args) =&gt; {
  const weatherConditions = [&quot;晴天&quot;, &quot;多云&quot;, &quot;雨天&quot;];
  const randomWeather =
    weatherConditions[Math.floor(Math.random() * weatherConditions.length)];
  const location = args.location;
  return `${location}今天是${randomWeather}。`;
};

// 封装模型响应函数
const getResponse = async (inputData) =&gt; {
  const response = await openai.responses.create({
    model: &quot;qwen4-max&quot;,
    input: inputData,
    tools: tools,
  });
  return response;
};

const main = async () =&gt; {
  const userQuestion = &quot;北京天气&quot;;

  // 维护对话上下文
  const conversation = [{ role: &quot;user&quot;, content: userQuestion }];

  let response = await getResponse(conversation);
  let functionCalls = response.output.filter(
    (item) =&gt; item.type === &quot;function_call&quot;
  );
  // 如果不需要调用工具，直接输出内容
  if (functionCalls.length === 0) {
    console.log(`助手最终回复：${response.output_text}`);
  } else {
    // 进入工具调用循环
    while (functionCalls.length &gt; 0) {
      for (const fc of functionCalls) {
        const funcName = fc.name;
        const args = JSON.parse(fc.arguments);
        console.log(`正在调用工具 [${funcName}]，参数：`, args);
        // 执行工具
        const toolResult = getCurrentWeather(args);
        console.log(`工具返回：${toolResult}`);
        // 将工具调用和结果成对追加到上下文中
        conversation.push({
          type: &quot;function_call&quot;,
          name: fc.name,
          arguments: fc.arguments,
          call_id: fc.call_id,
        });
        conversation.push({
          type: &quot;function_call_output&quot;,
          call_id: fc.call_id,
          output: toolResult,
        });
      }
      // 携带完整上下文再次调用模型
      response = await getResponse(conversation);
      functionCalls = response.output.filter(
        (item) =&gt; item.type === &quot;function_call&quot;
      );
    }
    console.log(`助手最终回复：${response.output_text}`);
  }
};

// 启动程序
main().catch(console.error);
</code></pre></div><a id="fig-code-group-5-curl-tab"></a>curl<div><a id="code-code-group-5-curl"></a><pre class="language-bash"><code># 第一步：提交用户问题与工具定义，模型返回 function_call
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/responses \
-H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
-H &quot;Content-Type: application/json&quot; \
-d '{
    &quot;model&quot;: &quot;qwen4-max&quot;,
    &quot;input&quot;: [
        {
            &quot;role&quot;: &quot;user&quot;,
            &quot;content&quot;: &quot;北京天气咋样&quot;
        }
    ],
    &quot;tools&quot;: [
        {
            &quot;type&quot;: &quot;function&quot;,
            &quot;name&quot;: &quot;get_current_weather&quot;,
            &quot;description&quot;: &quot;当你想查询指定城市的天气时非常有用。&quot;,
            &quot;parameters&quot;: {
                &quot;type&quot;: &quot;object&quot;,
                &quot;properties&quot;: {
                    &quot;location&quot;: {
                        &quot;type&quot;: &quot;string&quot;,
                        &quot;description&quot;: &quot;城市或县区，比如北京市、杭州市、余杭区等。&quot;
                    }
                },
                &quot;required&quot;: [&quot;location&quot;]
            }
        }
    ]
}'

# 第二步：在本地执行函数后，将 function_call 与 function_call_output 成对追加到 input 中，获取最终回复
# 请将 call_id 与 arguments 替换为第一步响应中实际返回的值
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/responses \
-H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
-H &quot;Content-Type: application/json&quot; \
-d '{
    &quot;model&quot;: &quot;qwen4-max&quot;,
    &quot;input&quot;: [
        {
            &quot;role&quot;: &quot;user&quot;,
            &quot;content&quot;: &quot;北京天气咋样&quot;
        },
        {
            &quot;type&quot;: &quot;function_call&quot;,
            &quot;name&quot;: &quot;get_current_weather&quot;,
            &quot;arguments&quot;: &quot;{\&quot;location\&quot;: \&quot;北京市\&quot;}&quot;,
            &quot;call_id&quot;: &quot;call_xxx&quot;
        },
        {
            &quot;type&quot;: &quot;function_call_output&quot;,
            &quot;call_id&quot;: &quot;call_xxx&quot;,
            &quot;output&quot;: &quot;北京市今天是晴天。&quot;
        }
    ],
    &quot;tools&quot;: [
        {
            &quot;type&quot;: &quot;function&quot;,
            &quot;name&quot;: &quot;get_current_weather&quot;,
            &quot;description&quot;: &quot;当你想查询指定城市的天气时非常有用。&quot;,
            &quot;parameters&quot;: {
                &quot;type&quot;: &quot;object&quot;,
                &quot;properties&quot;: {
                    &quot;location&quot;: {
                        &quot;type&quot;: &quot;string&quot;,
                        &quot;description&quot;: &quot;城市或县区，比如北京市、杭州市、余杭区等。&quot;
                    }
                },
                &quot;required&quot;: [&quot;location&quot;]
            }
        }
    ]
}'
</code></pre></div></div></section><a id="工具返回多模态结果"></a><section><a id="工具返回多模态结果-h4"></a><h4>工具返回多模态结果</h4><a id="fig-code-group-6"></a><div><a id="fig-code-group-6-python-tab"></a>Python<div><a id="code-code-group-6-python"></a><pre class="language-python"><code>from openai import OpenAI
import json
import os

# 初始化客户端
client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;,
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    base_url=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;,
)
# 模拟用户问题
USER_QUESTION = &quot;画一张小狗的照片，然后告诉我图里的小狗是什么品种、在什么场景里&quot;
# 定义工具列表
tools = [
    {
        &quot;type&quot;: &quot;function&quot;,
        &quot;name&quot;: &quot;generate_image&quot;,
        &quot;description&quot;: &quot;当你需要根据文字描述生成图片时非常有用。&quot;,
        &quot;parameters&quot;: {
            &quot;type&quot;: &quot;object&quot;,
            &quot;properties&quot;: {
                &quot;prompt&quot;: {
                    &quot;type&quot;: &quot;string&quot;,
                    &quot;description&quot;: &quot;图片内容的文字描述。&quot;,
                }
            },
            &quot;required&quot;: [&quot;prompt&quot;],
        },
    }
]

# 模拟文生图工具，实际使用时请替换为真实的图片生成调用
def generate_image(arguments):
    print(f&quot;正在生成图片，提示词：{arguments['prompt']}&quot;)
    return &quot;https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg&quot;

# 封装模型响应函数
def get_response(input_data):
    response = client.responses.create(
        model=&quot;qwen4-max&quot;,
        input=input_data,
        tools=tools,
    )
    return response

# 维护对话上下文
conversation = [{&quot;role&quot;: &quot;user&quot;, &quot;content&quot;: USER_QUESTION}]

response = get_response(conversation)
function_calls = [item for item in response.output if item.type == &quot;function_call&quot;]
# 进入工具调用循环
while function_calls:
    for fc in function_calls:
        arguments = json.loads(fc.arguments)
        # 执行工具，得到图片地址
        image_url = generate_image(arguments)
        # 将工具调用和结果成对追加到上下文中
        conversation.append(
            {
                &quot;type&quot;: &quot;function_call&quot;,
                &quot;name&quot;: fc.name,
                &quot;arguments&quot;: fc.arguments,
                &quot;call_id&quot;: fc.call_id,
            }
        )
        # output 传入内容数组，模型才能理解图片内容
        conversation.append(
            {
                &quot;type&quot;: &quot;function_call_output&quot;,
                &quot;call_id&quot;: fc.call_id,
                &quot;output&quot;: [
                    {&quot;type&quot;: &quot;input_text&quot;, &quot;text&quot;: &quot;图片生成成功。&quot;},
                    {&quot;type&quot;: &quot;input_image&quot;, &quot;image_url&quot;: image_url},
                ],
            }
        )
    # 携带完整上下文再次调用模型
    response = get_response(conversation)
    function_calls = [item for item in response.output if item.type == &quot;function_call&quot;]
print(f&quot;助手最终回复：{response.output_text}&quot;)
</code></pre></div><a id="fig-code-group-6-node-js-tab"></a>Node.js<div><a id="code-code-group-6-node-js"></a><pre class="language-javascript"><code>import OpenAI from &quot;openai&quot;;

// 初始化客户端
const openai = new OpenAI({
  // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：apiKey: &quot;sk-xxx&quot;,
  apiKey: process.env.DASHSCOPE_API_KEY,
  baseURL:
    &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;,
});

// 定义工具列表
const tools = [
  {
    type: &quot;function&quot;,
    name: &quot;generate_image&quot;,
    description: &quot;当你需要根据文字描述生成图片时非常有用。&quot;,
    parameters: {
      type: &quot;object&quot;,
      properties: {
        prompt: {
          type: &quot;string&quot;,
          description: &quot;图片内容的文字描述。&quot;,
        },
      },
      required: [&quot;prompt&quot;],
    },
  },
];

// 模拟文生图工具，实际使用时请替换为真实的图片生成调用
const generateImage = (args) =&gt; {
  console.log(`正在生成图片，提示词：${args.prompt}`);
  return &quot;https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg&quot;;
};

// 封装模型响应函数
const getResponse = async (inputData) =&gt; {
  const response = await openai.responses.create({
    model: &quot;qwen4-max&quot;,
    input: inputData,
    tools: tools,
  });
  return response;
};

const main = async () =&gt; {
  const userQuestion = &quot;画一张小狗的照片，然后告诉我图里的小狗是什么品种、在什么场景里&quot;;

  // 维护对话上下文
  const conversation = [{ role: &quot;user&quot;, content: userQuestion }];

  let response = await getResponse(conversation);
  let functionCalls = response.output.filter(
    (item) =&gt; item.type === &quot;function_call&quot;
  );
  // 进入工具调用循环
  while (functionCalls.length &gt; 0) {
    for (const fc of functionCalls) {
      const args = JSON.parse(fc.arguments);
      // 执行工具，得到图片地址
      const imageUrl = generateImage(args);
      // 将工具调用和结果成对追加到上下文中
      conversation.push({
        type: &quot;function_call&quot;,
        name: fc.name,
        arguments: fc.arguments,
        call_id: fc.call_id,
      });
      // output 传入内容数组，模型才能理解图片内容
      conversation.push({
        type: &quot;function_call_output&quot;,
        call_id: fc.call_id,
        output: [
          { type: &quot;input_text&quot;, text: &quot;图片生成成功。&quot; },
          { type: &quot;input_image&quot;, image_url: imageUrl },
        ],
      });
    }
    // 携带完整上下文再次调用模型
    response = await getResponse(conversation);
    functionCalls = response.output.filter(
      (item) =&gt; item.type === &quot;function_call&quot;
    );
  }
  console.log(`助手最终回复：${response.output_text}`);
};

// 启动程序
main().catch(console.error);
</code></pre></div></div></section><a id="文档理解"></a><section><a id="文档理解-h4"></a><h4>文档理解</h4><a id="fig-code-group-7"></a><div><a id="fig-code-group-7-python-tab"></a>Python<div><a id="code-code-group-7-python"></a><pre class="language-python"><code>import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    base_url=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;,
)

response = client.responses.create(
    model=&quot;qwen3.5-ocr&quot;,
    input=[
        {
            &quot;role&quot;: &quot;user&quot;,
            &quot;content&quot;: [
                {
                    &quot;type&quot;: &quot;input_file&quot;,
                    &quot;file_url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260616/qmycjl/1506.02640v5.pdf&quot;,
                },
                {
                    &quot;type&quot;: &quot;input_text&quot;,
                    &quot;text&quot;: &quot;Read all the text in the file.&quot;,
                },
            ],
        }
    ],
    extra_body={
        &quot;ocr_options&quot;: {&quot;task&quot;: &quot;document_parsing&quot;}
    },
)

print(response.output_text)
</code></pre></div><a id="fig-code-group-7-node-js-tab"></a>Node.js<div><a id="code-code-group-7-node-js"></a><pre class="language-javascript"><code>import OpenAI from 'openai';

const client = new OpenAI({
    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: &quot;sk-xxx&quot;
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;,
});

async function main() {
    const response = await client.responses.create({
        model: &quot;qwen3.5-ocr&quot;,
        input: [{
            role: &quot;user&quot;,
            content: [{
                type: &quot;input_file&quot;,
                file_url: &quot;https://example.com/your-document.pdf&quot;
            }]
        }],
        ocr_options: { task: &quot;document_parsing&quot; }
    });

    // 获取定制任务结果
    console.log(response.output[0].content[0].ocr_result);
}

main();
</code></pre></div><a id="fig-code-group-7-curl-tab"></a>curl<div><a id="code-code-group-7-curl"></a><pre class="language-bash"><code>curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/responses \
-H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
-H &quot;Content-Type: application/json&quot; \
-d '{
    &quot;model&quot;: &quot;qwen3.5-ocr&quot;,
    &quot;input&quot;: [
        {
            &quot;role&quot;: &quot;user&quot;,
            &quot;content&quot;: [
                {
                    &quot;type&quot;: &quot;input_file&quot;,
                    &quot;file_url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260616/qmycjl/1506.02640v5.pdf&quot;
                },
                {
                    &quot;type&quot;: &quot;input_text&quot;,
                    &quot;text&quot;: &quot;Read all the text in the file.&quot;
                }
            ]
        }
    ],
    &quot;ocr_options&quot;: {&quot;task&quot;: &quot;document_parsing&quot;}
}'
</code></pre></div></div></section><a id="session-缓存"></a><section><a id="session-缓存-h4"></a><h4>Session 缓存</h4><p>在请求 Header 中设置 <code>x-dashscope-session-cache: enable</code> 开启 Session 缓存，多轮对话通过 <code>previous_response_id</code> 关联上下文。详细说明见<a href="../../toolkits-and-frameworks/compatibility-with-openai-responses-api.md#example-session-cache-title">Session 缓存</a>。</p><p>自动生效的隐式缓存另见<a href="../../../model-user-guide/model-experience/text-generation-model/context-cache.md">上下文缓存</a>。</p><a id="fig-code-group-8"></a><div><a id="fig-code-group-8-python-tab"></a>Python<div><a id="code-code-group-8-python"></a><pre class="language-python"><code>import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    base_url=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;,
    # 通过 default_headers 开启 Session 缓存
    default_headers={&quot;x-dashscope-session-cache&quot;: &quot;enable&quot;}
)

# 构造超过 1024 Token 的长文本，确保能触发缓存创建（若未达到1024 Token，后续累积对话上下文超过1024 Token时将触发缓存创建）
long_context = &quot;人工智能是计算机科学的一个重要分支，致力于研究和开发能够模拟、延伸和扩展人类智能的理论、方法、技术及应用系统。&quot; * 50

# 第一轮对话
response1 = client.responses.create(
    model=&quot;qwen4-max&quot;,
    input=long_context + &quot;\n\n基于以上背景知识，请简短介绍机器学习中的随机森林算法。&quot;,
)
print(f&quot;第一轮回复: {response1.output_text}&quot;)

# 第二轮对话：通过 previous_response_id 关联上下文，缓存由服务端自动处理
response2 = client.responses.create(
    model=&quot;qwen4-max&quot;,
    input=&quot;它和 GBDT 有什么主要区别？&quot;,
    extra_body={&quot;previous_response_id&quot;: response1.id},
)
print(f&quot;第二轮回复: {response2.output_text}&quot;)

# 查看缓存命中情况
usage = response2.usage
print(f&quot;输入 Token: {usage.input_tokens}&quot;)
print(f&quot;缓存命中 Token: {usage.input_tokens_details.cached_tokens}&quot;)
</code></pre></div><a id="fig-code-group-8-node-js-tab"></a>Node.js<div><a id="code-code-group-8-node-js"></a><pre class="language-javascript"><code>import OpenAI from &quot;openai&quot;;

const openai = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;,
    // 通过 defaultHeaders 开启 Session 缓存
    defaultHeaders: {&quot;x-dashscope-session-cache&quot;: &quot;enable&quot;}
});

// 构造超过 1024 Token 的长文本，确保能触发缓存创建（若未达到1024 Token，后续累积对话上下文超过1024 Token时将触发缓存创建）
const longContext = &quot;人工智能是计算机科学的一个重要分支，致力于研究和开发能够模拟、延伸和扩展人类智能的理论、方法、技术及应用系统。&quot;.repeat(50);

async function main() {
    // 第一轮对话
    const response1 = await openai.responses.create({
        model: &quot;qwen4-max&quot;,
        input: longContext + &quot;\n\n基于以上背景知识，请简短介绍机器学习中的随机森林算法，包括基本原理和应用场景。&quot;
    });
    console.log(`第一轮回复: ${response1.output_text}`);

    // 第二轮对话：通过 previous_response_id 关联上下文，缓存由服务端自动处理
    const response2 = await openai.responses.create(
        {
            model: &quot;qwen4-max&quot;,
            input: &quot;它和 GBDT 有什么主要区别？&quot;,
        },
        {
            body: { previous_response_id: response1.id }
        }
    );
    console.log(`第二轮回复: ${response2.output_text}`);

    // 查看缓存命中情况
    console.log(`输入 Token: ${response2.usage.input_tokens}`);
    console.log(`缓存命中 Token: ${response2.usage.input_tokens_details.cached_tokens}`);
}

main();
</code></pre></div><a id="fig-code-group-8-curl-tab"></a>curl<div><a id="code-code-group-8-curl"></a><pre class="language-bash"><code># 第一轮对话
# 长文本重复 50 次以确保超过 1024 Token，触发缓存创建
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/responses \
-H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
-H &quot;Content-Type: application/json&quot; \
-H &quot;x-dashscope-session-cache: enable&quot; \
-d '{
    &quot;model&quot;: &quot;qwen4-max&quot;,
    &quot;input&quot;: &quot;人工智能是计算机科学的一个重要分支...&quot;
}'

# 第二轮对话 - 使用上一轮返回的 id 作为 previous_response_id
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/responses \
-H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
-H &quot;Content-Type: application/json&quot; \
-H &quot;x-dashscope-session-cache: enable&quot; \
-d '{
    &quot;model&quot;: &quot;qwen4-max&quot;,
    &quot;input&quot;: &quot;它和 GBDT 有什么主要区别？&quot;,
    &quot;previous_response_id&quot;: &quot;第一轮返回的响应id&quot;
}'
</code></pre></div></div><strong>缓存命中规则</strong><p>Session 缓存按精确匹配命中，规则如下：</p><ul><li><strong>不支持前缀匹配</strong>：在原有 user prompt 之后追加内容不会命中缓存。</li><li><strong>不支持语义匹配</strong>：只有内容完全相同才会命中缓存，语义相同但文字不同不会命中。</li><li><strong>最小可缓存 Token 数</strong>：1024 Token。低于该阈值的输入不会触发缓存创建；多轮对话中累积上下文超过 1024 Token 后才会开始创建缓存。</li></ul><p>您可以通过 <code>usage.input_tokens_details.cached_tokens</code> 查看命中缓存的 Token 数，通过 <code>cache_creation_input_tokens</code> 查看本次请求新创建缓存的 Token 数。</p></section></section></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="8b91df45f4k58"></a><h2>Response 响应对象（非流式输出）</h2><p><strong>id</strong> <code>string</code></p><p>本次响应的唯一标识符，为 UUID 格式的字符串，有效期为7天。可用于 <code>previous_response_id</code> 参数以创建多轮对话。</p><p><strong>created_at</strong> <code>integer</code></p><p>本次请求的 Unix 时间戳（秒）。</p><p><strong>object</strong> <code>string</code></p><p>对象类型，固定为 <code>response</code>。</p><p><strong>status</strong> <code>string</code></p><p>响应生成的状态。枚举值：</p><ul><li><code>completed</code>：生成完成</li><li><code>failed</code>：生成失败</li><li><code>in_progress</code>：生成中</li><li><code>cancelled</code>：已取消</li><li><code>queued</code>：请求排队中</li><li><code>incomplete</code>：生成不完整</li></ul><p><strong>model</strong> <code>string</code></p><p>用于生成响应的模型 ID。</p><p><strong>output</strong> <code>array</code></p><p>模型生成的输出项数组。数组中的元素类型和顺序取决于模型的响应。</p><a id="accordion-数组元素属性"></a><section><p>数组元素属性</p><div><p><strong>type</strong> <code>string</code></p><p>输出项类型。枚举值：</p><ul><li><code>message</code>：消息类型，包含模型最终生成的回复内容。</li><li><code>reasoning</code>：推理类型，设置 <code>reasoning.effort</code>（非 <code>none</code>）或开启思考模式时返回。推理 Token 会被计入 <code>output_tokens_details.reasoning_tokens</code> 中，按推理 Token 计费。</li><li><code>function_call</code>：函数调用类型，使用自定义 <code>function</code> 工具时返回。需要处理函数调用并返回结果。</li><li><code>custom_tool_call</code>: 自定义工具调用类型，使用 <code>custom</code> 工具时返回。</li><li><code>web_search_call</code>：搜索调用类型，使用 <code>web_search</code> 工具时返回。</li><li><code>code_interpreter_call</code>：代码执行类型，使用 <code>code_interpreter</code> 工具时返回。</li><li><code>web_extractor_call</code>：网页抽取类型，使用 <code>web_extractor</code> 工具时返回。需要配合 <code>web_search</code> 工具一起使用。</li><li><code>web_search_image_call</code>：文搜图调用类型，使用 <code>web_search_image</code> 工具时返回。包含搜索到的图片列表。</li><li><code>image_search_call</code>：图搜图调用类型，使用 <code>image_search</code> 工具时返回。包含搜索到的相似图片列表。</li><li><code>mcp_call</code>：MCP 调用类型，使用 <code>mcp</code> 工具时返回。包含 MCP 服务的调用结果。</li><li><code>file_search_call</code>：知识库搜索调用类型，使用 <code>file_search</code> 工具时返回。包含知识库的检索查询和结果。</li></ul><p><strong>id</strong> <code>string</code></p><p>输出项的唯一标识符。所有类型的输出项都包含此字段。</p><p><strong>role</strong> <code>string</code></p><p>消息角色，固定为 <code>assistant</code>。仅当 <code>type</code> 为 <code>message</code> 时存在。</p><p><strong>status</strong> <code>string</code></p><p>输出项状态。可选值：<code>completed</code>（完成）、<code>in_progress</code>（生成中）。当 <code>type</code> 为 <code>reasoning</code> 或 <code>custom_tool_call</code> 时不返回此字段。</p><p><strong>name</strong> <code>string</code></p><p>工具或函数名称。当 <code>type</code> 为 <code>function_call</code> 或 <code>custom_tool_call</code>、<code>web_search_image_call</code>、<code>image_search_call</code>、<code>mcp_call</code> 时存在。</p><p>对于 <code>web_search_image_call</code> 和 <code>image_search_call</code>，值分别固定为 <code>&quot;web_search_image&quot;</code> 和 <code>&quot;image_search&quot;</code>。</p><p>对于 <code>mcp_call</code>，值为 MCP 服务中被调用的具体函数名（如 <code>amap-maps-maps_geo</code>）。</p><p><strong>namespace</strong> <code>string</code> （可选）</p><p>工具所属的命名空间。调用命名空间内的 <code>function</code> 或 <code>custom</code> 工具时返回，回传调用项时保留该字段。</p><p><strong>input</strong> <code>string</code> （可选）</p><p>自定义工具的自由文本输入，仅当 <code>type</code> 为 <code>custom_tool_call</code> 时存在。</p><p><strong>arguments</strong> <code>string</code></p><p>工具调用的参数，JSON 字符串格式。当 <code>type</code> 为 <code>function_call</code>、<code>web_search_image_call</code>、<code>image_search_call</code>、<code>mcp_call</code> 时存在。使用前需要通过 <code>JSON.parse()</code> 解析。不同工具类型的 arguments 内容：</p><ul><li><code>web_search_image_call</code>：<code>{&quot;queries&quot;: [&quot;搜索关键词1&quot;, &quot;搜索关键词2&quot;]}</code>，其中 <code>queries</code> 为模型根据用户输入自动生成的搜索关键词列表。</li><li><code>image_search_call</code>：<code>{&quot;img_idx&quot;: 0, &quot;bbox&quot;: [0, 0, 1000, 1000]}</code>，其中 <code>img_idx</code> 为输入图片的索引（从 0 开始），<code>bbox</code> 为搜索区域的边界框坐标 [x1, y1, x2, y2]，坐标范围 0-1000。</li><li><code>function_call</code>：按用户定义的函数参数 schema 生成的参数对象。</li><li><code>mcp_call</code>：MCP 服务中被调用函数的参数对象。</li></ul><p><strong>call_id</strong> <code>string</code></p><p>函数调用的唯一标识符。仅当 <code>type</code> 为 <code>function_call</code> 或 <code>custom_tool_call</code> 时存在。在返回函数调用结果时，需要通过此 ID 关联请求与响应。</p><p><strong>content</strong> <code>array</code></p><p>消息内容数组。仅当 <code>type</code> 为 <code>message</code> 时存在。</p><a id="accordion-数组元素属性-2"></a><section><p>数组元素属性</p><div><p><strong>type</strong> <code>string</code></p><p>内容类型，固定为 <code>output_text</code>。</p><p><strong>text</strong> <code>string</code></p><p>模型生成的文本内容。</p><p><strong>annotations</strong> <code>array</code></p><p>文本注释数组。通常为空数组。</p></div></section><p><strong>encrypted_content</strong> <code>string</code></p><p><code>qwen4-max</code>, <code>reasoning.summary=&quot;auto&quot;</code>: Responses 的 reasoning item 包含 <code>summary</code>（<code>summary_text</code> 元素）和 <code>encrypted_content</code>。摘要按文本增量返回，密文在 reasoning item 完成事件及最终 response 中返回；可从完成快照补齐密文，不要重复追加摘要。 <a href="../../../model-user-guide/model-experience/text-generation-model/cot-summary.md#multi-turn">思维链摘要与加密</a>. 密文必须原样回传。</p><p><strong>summary</strong> <code>array</code></p><p>推理摘要数组。仅当 <code>type</code> 为 <code>reasoning</code> 时存在。每个元素包含 <code>type</code>（值为 <code>summary_text</code>）和 <code>text</code>（摘要文本）字段。</p><p><strong>action</strong> <code>object</code></p><p>搜索动作信息。仅当 <code>type</code> 为 <code>web_search_call</code> 时存在。</p><a id="accordion-属性-44"></a><section><p>属性</p><div><p><strong>query</strong> <code>string</code></p><p>搜索查询关键词。</p><p><strong>type</strong> <code>string</code></p><p>搜索类型，固定为 <code>search</code>。</p><p><strong>sources</strong> <code>array</code></p><p>搜索来源列表。每个元素包含 <code>type</code>和 <code>url</code>字段。</p></div></section><p><strong>code</strong> <code>string</code></p><p>模型生成并执行的代码。仅当 <code>type</code> 为 <code>code_interpreter_call</code> 时存在。</p><p><strong>outputs</strong> <code>array</code></p><p>代码执行输出数组。仅当 <code>type</code> 为 <code>code_interpreter_call</code> 时存在。每个元素包含 <code>type</code>（值为 <code>logs</code>）和 <code>logs</code>（代码执行日志）字段。</p><p><strong>container_id</strong> <code>string</code></p><p>代码解释器容器标识符。仅当 <code>type</code> 为 <code>code_interpreter_call</code> 时存在。用于关联同一会话中的多次代码执行。</p><p><strong>goal</strong> <code>string</code></p><p>抽取目标描述，说明需要从网页中提取哪些信息。仅当 <code>type</code> 为 <code>web_extractor_call</code> 时存在。</p><p><strong>output</strong> <code>string</code></p><p>工具调用的输出结果，字符串格式。</p><ul><li>当 <code>type</code> 为 <code>web_extractor_call</code> 时为网页抽取的内容摘要</li><li>当 <code>type</code> 为 <code>web_search_image_call</code> 或 <code>image_search_call</code> 时为 JSON 字符串，包含图片搜索结果数组，每个元素包含 <code>title</code>（图片标题）、<code>url</code>（图片 URL）和 <code>index</code>（序号）字段</li><li>当 <code>type</code> 为 <code>mcp_call</code> 时为 MCP 服务返回的 JSON 字符串结果。</li></ul><p><strong>urls</strong> <code>array</code></p><p>被抽取的网页 URL 列表。仅当 <code>type</code> 为 <code>web_extractor_call</code> 时存在。</p><p><strong>server_label</strong> <code>string</code></p><p>MCP 服务标签。仅当 <code>type</code> 为 <code>mcp_call</code> 时存在。标识本次调用所使用的 MCP 服务。</p><p><strong>queries</strong> <code>array</code></p><p>知识库检索使用的查询列表。仅当 <code>type</code> 为 <code>file_search_call</code> 时存在。数组元素为字符串，表示模型生成的搜索查询词。</p><p><strong>results</strong> <code>array</code></p><p>知识库检索结果数组。仅当 <code>type</code> 为 <code>file_search_call</code> 时存在。</p><a id="accordion-数组元素属性-3"></a><section><p>数组元素属性</p><div><p><strong>file_id</strong> <code>string</code></p><p>匹配文档的文件 ID。</p><p><strong>filename</strong> <code>string</code></p><p>匹配文档的文件名。</p><p><strong>score</strong> <code>float</code></p><p>匹配相关度评分，取值范围 0-1，值越大表示相关度越高。</p><p><strong>text</strong> <code>string</code></p><p>匹配到的文档内容片段。</p></div></section></div></section><p><strong>tool_usage</strong> <code>object</code></p><p>统计本次请求的工具使用情况，与 <code>usage</code> 中的模型 Token 使用情况分开记录。没有工具调用时，默认返回空对象 <code>{}</code>。</p><a id="accordion-属性-45"></a><section><p>属性</p><div><p><strong>web_search</strong> <code>object</code></p><a id="accordion-属性-46"></a><section><p>属性</p><div><p><strong>num_requests</strong> <code>integer</code></p><p>计费搜索次数。</p></div></section><p><strong>code_interpreter</strong> <code>object</code></p><a id="accordion-属性-47"></a><section><p>属性</p><div><p><strong>num_requests</strong> <code>integer</code></p><p>代码解释器的执行次数。</p></div></section><p><strong>web_extractor</strong> <code>object</code></p><a id="accordion-属性-48"></a><section><p>属性</p><div><p><strong>num_requests</strong> <code>integer</code></p><p>网页内容抓取次数。</p></div></section><p><strong>image_search</strong> <code>object</code></p><a id="accordion-属性-49"></a><section><p>属性</p><div><p><strong>num_requests</strong> <code>integer</code></p><p>图搜图片的次数。</p></div></section><p><strong>web_search_image</strong> <code>object</code></p><a id="accordion-属性-50"></a><section><p>属性</p><div><p><strong>num_requests</strong> <code>integer</code></p><p>文搜图片的次数。</p></div></section><p><strong>pdf_page_parser</strong> <code>object</code></p><a id="accordion-属性-51"></a><section><p>属性</p><div><p><strong>num_requests</strong> <code>integer</code></p><p>PDF 解析的页面数。</p></div></section></div></section><p><strong>prompt_cache_options</strong> <code>object</code> (可选)</p><p>仅支持 <code>qwen4-max</code>。 本次请求的缓存模式和有效期。</p><a id="accordion-属性-52"></a><section><p>属性</p><div><p><strong>mode</strong> <code>string</code></p><p><code>implicit</code> / <code>explicit</code></p><p><strong>ttl</strong> <code>string</code></p><p><code>5m</code> / <code>1h</code></p></div></section><p><strong>usage</strong> <code>object</code></p><p>本次请求的 Token 消耗信息。</p><p>Qwen4 系列、Kimi-K3.1 系列及后续新模型使用下方的新响应结构。</p><a id="accordion-属性-53"></a><section><p>属性</p><div><p><strong>input_tokens</strong> <code>integer</code></p><p>输入的 Token 数。<a href="../../../model-user-guide/model-experience/text-generation-model/text-generation.md#e710782c79xqy">补充说明</a></p><p><strong>output_tokens</strong> <code>integer</code></p><p>模型输出的 Token 数。</p><p><strong>total_tokens</strong> <code>integer</code></p><p>消耗的总 Token 数，为 input_tokens 与 output_tokens 的总和。</p><p><strong>input_tokens_details</strong> <code>object</code></p><p>输入 Token 的细粒度分类。</p><a id="accordion-属性-54"></a><section><p>属性</p><div><p><strong>cached_tokens</strong> <code>integer</code></p><p>命中缓存的 Token 数。详情请参见<a href="../../../model-user-guide/model-experience/text-generation-model/context-cache.md">上下文缓存</a>。</p></div></section><p><strong>output_tokens_details</strong> <code>object</code></p><p>输出 Token 的细粒度分类。</p><a id="accordion-属性-55"></a><section><p>属性</p><div><p><strong>reasoning_tokens</strong> <code>integer</code></p><p>思考过程 Token 数。</p></div></section><p><strong>x_details</strong> <code>array</code></p><p>本次请求的计费明细数组。比顶级 <code>usage</code> 字段提供更细粒度的多模态 Token 拆分。</p><a id="accordion-属性-56"></a><section><p>属性</p><div><p><strong>input_tokens</strong> <code>integer</code></p><p>输入的 Token 数。<a href="../../../model-user-guide/model-experience/text-generation-model/text-generation.md#e710782c79xqy">补充说明</a></p><p><strong>output_tokens</strong> <code>integer</code></p><p>模型输出的 Token 数。</p><p><strong>total_tokens</strong> <code>integer</code></p><p>消耗的总 Token 数，为 input_tokens 与 output_tokens 的总和。</p><p><strong>x_billing_type</strong> <code>string</code></p><p>固定为<code>response_api</code>。</p><p><strong>image_tokens</strong> <code>integer</code></p><p>图像输入的 Token 数。包含图像输入时返回，等同于 <code>input_tokens_details.image_tokens</code>。</p><p><strong>input_tokens_details</strong> <code>object</code></p><p>输入 Token 的细粒度分类，返回字段取决于模型和输入模态。<code>qwen3.8-omni-flash</code> 的音频输入可返回 <code>audio_tokens</code>。</p><a id="accordion-属性-57"></a><section><p>属性</p><div><p><strong>text_tokens</strong> <code>integer</code></p><p>文本输入的 Token 数。</p><p><strong>image_tokens</strong> <code>integer</code></p><p>图像输入的 Token 数。</p><p><strong>audio_tokens</strong> <code>integer</code></p><p>音频输入的 Token 数，完整路径为 <code>usage.x_details[].input_tokens_details.audio_tokens</code>。可选字段，是否返回取决于模型及输入。</p></div></section><p><strong>output_tokens_details</strong> <code>object</code></p><p>输出 Token 的细粒度分类。比顶级 <code>output_tokens_details</code> 多 <code>text_tokens</code> 字段（多模态输入时返回）。</p><a id="accordion-属性-58"></a><section><p>属性</p><div><p><strong>reasoning_tokens</strong> <code>integer</code></p><p>思考过程 Token 数。</p><p><strong>text_tokens</strong> <code>integer</code></p><p>文本输出的 Token 数。多模态输入时返回。</p></div></section><p><strong>plugins</strong> <code>object</code></p><p>内置工具调用统计。使用内置工具（如 <code>web_search</code>）时返回，与顶级 <code>x_tools</code> 字段内容相同。</p><a id="accordion-属性-59"></a><section><p>属性</p><div><p><strong>web_search</strong> <code>object</code></p><p>联网搜索调用统计。</p><a id="accordion-属性-60"></a><section><p>属性</p><div><p><strong>count</strong> <code>integer</code></p><p>本次响应中联网搜索的调用次数。</p></div></section></div></section><p><strong>input_tokens_details</strong> <code>object</code></p><p>输入 Token 的缓存详情。启用 Session 缓存后返回；含图像输入但未命中缓存时可能返回空对象。</p><a id="accordion-属性-61"></a><section><p>属性</p><div><p><strong>cached_tokens</strong> <code>integer</code></p><p>命中缓存的 Token 数。</p><p><strong>cache_creation_input_tokens</strong> <code>integer</code></p><p>本次请求新创建缓存的 Token 数。</p><p><strong>cache_creation</strong> <code>object</code></p><p>缓存创建详情。</p><a id="accordion-属性-62"></a><section><p>属性</p><div><p><strong>ephemeral_5m_input_tokens</strong> <code>integer</code></p><p>5 分钟临时缓存新创建的 Token 数。</p></div></section><p><strong>cache_type</strong> <code>string</code></p><p>缓存类型，固定为<code>ephemeral</code>。</p></div></section></div></section><p><strong>x_tools</strong> <code>object</code></p><p>工具使用统计信息。当使用内置工具时，包含各工具的调用次数。</p><p>示例：<code>{&quot;web_search&quot;: {&quot;count&quot;: 1}}</code></p></div></section><a id="accordion-属性-qwen4-kimi-k3-1"></a><section><p>属性（Qwen4、Kimi-K3.1）</p><div><p><strong>input_tokens</strong> <code>integer</code></p><p>输入 Token 总数，包含读取缓存、创建缓存和未使用缓存的部分。</p><p><strong>input_tokens_details</strong> <code>object</code></p><p>输入 Token 明细。</p><a id="accordion-属性-63"></a><section><p>属性</p><div><p><strong>cache_write_tokens</strong> <code>integer</code></p><p>缓存创建的 Token 数。</p><p><strong>cache_write_tokens_details</strong> <code>object</code></p><p>按 TTL 统计的缓存创建明细。</p><a id="accordion-属性-64"></a><section><p>属性</p><div><p><strong>ttl_1h_tokens</strong> <code>integer</code></p><p>1 小时缓存创建的 Token 数。</p><p><strong>ttl_5m_tokens</strong> <code>integer</code></p><p>5 分钟缓存创建的 Token 数。</p></div></section><p><strong>cached_tokens</strong> <code>integer</code></p><p>缓存读取的 Token 数。</p></div></section><p><strong>output_tokens</strong> <code>integer</code></p><p>输出 Token 总数。</p><p><strong>output_tokens_details</strong> <code>object</code></p><p>输出 Token 明细。</p><a id="accordion-属性-65"></a><section><p>属性</p><div><p><strong>reasoning_tokens</strong> <code>integer</code></p><p>思考过程的 Token 数。</p></div></section><p><strong>total_tokens</strong> <code>integer</code></p><p>输入与输出 Token 数之和。</p><p>新响应结构不返回 <code>x_details</code> 和 <code>x_tools</code>。</p><a id="code-block-6"></a><pre class="language-json"><code>{
  &quot;usage&quot;: {
    &quot;input_tokens&quot;: 1053,
    &quot;input_tokens_details&quot;: {
      &quot;cache_write_tokens&quot;: 0,
      &quot;cache_write_tokens_details&quot;: {
        &quot;ttl_1h_tokens&quot;: 0,
        &quot;ttl_5m_tokens&quot;: 0
      },
      &quot;cached_tokens&quot;: 0
    },
    &quot;output_tokens&quot;: 23,
    &quot;output_tokens_details&quot;: {
      &quot;reasoning_tokens&quot;: 0
    },
    &quot;total_tokens&quot;: 1076
  }
}
</code></pre></div></section><p><strong>error</strong> <code>object</code></p><p>当模型生成响应失败时返回的错误对象。成功时为 <code>null</code>。</p><p><strong>tools</strong> <code>array</code></p><p>回显请求中 <code>tools</code> 参数的完整内容，结构与请求体中的 <code>tools</code> 参数相同。</p><p><strong>tool_choice</strong> <code>string</code></p><p>回显请求中 <code>tool_choice</code> 参数的值，枚举值为 <code>auto</code>、<code>none</code>、<code>required</code>。</p></td><td><div><p>以下为 <code>qwen3.8-max</code> 的返回示例，用于说明响应字段。</p><a id="code-block-7"></a><pre class="language-json"><code>{
    &quot;created_at&quot;: 1771165743,
    &quot;id&quot;: &quot;c9f9c06b-032d-4525-a422-ac8ab5eccxxx&quot;,
    &quot;model&quot;: &quot;qwen3.8-max&quot;,
    &quot;object&quot;: &quot;response&quot;,
    &quot;output&quot;: [
        {
            &quot;content&quot;: [
                {
                    &quot;annotations&quot;: [],
                    &quot;text&quot;: &quot;你好！我是 Qwen3.5，阿里巴巴最新推出的通义千问大语言模型，具备强大的语言理解、逻辑推理、代码生成及多模态处理能力，旨在为用户提供精准高效的智能服务。&quot;,
                    &quot;type&quot;: &quot;output_text&quot;
                }
            ],
            &quot;id&quot;: &quot;msg_544b2907-e88e-40d2-9a83-c30d6d1f9xxx&quot;,
            &quot;role&quot;: &quot;assistant&quot;,
            &quot;status&quot;: &quot;completed&quot;,
            &quot;type&quot;: &quot;message&quot;
        }
    ],
    &quot;parallel_tool_calls&quot;: false,
    &quot;status&quot;: &quot;completed&quot;,
    &quot;tool_choice&quot;: &quot;auto&quot;,
    &quot;tools&quot;: [],
    &quot;tool_usage&quot;: {},
    &quot;usage&quot;: {
        &quot;input_tokens&quot;: 55,
        &quot;input_tokens_details&quot;: {
            &quot;cached_tokens&quot;: 0
        },
        &quot;output_tokens&quot;: 43,
        &quot;output_tokens_details&quot;: {
            &quot;reasoning_tokens&quot;: 0
        },
        &quot;total_tokens&quot;: 98,
        &quot;x_details&quot;: [
            {
                &quot;input_tokens&quot;: 55,
                &quot;output_tokens&quot;: 43,
                &quot;total_tokens&quot;: 98,
                &quot;x_billing_type&quot;: &quot;response_api&quot;
            }
        ]
    }
}
</code></pre></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="94ea60632am5g"></a><h2>Response 响应 chunk 对象（流式输出）</h2><p>流式输出返回一系列 JSON 对象。每个对象包含 <code>type</code> 字段标识事件类型，<code>sequence_number</code> 字段标识事件顺序。<code>response.completed</code> 事件标志着流式传输的结束。</p><p><strong>type</strong> <code>string</code></p><p>事件类型标识符。枚举值：</p><ul><li><code>response.created</code>：响应创建时触发，状态为 <code>queued</code>。</li><li><code>response.in_progress</code>：响应开始处理时触发，状态变为 <code>in_progress</code>。</li><li><code>response.output_item.added</code>：新的输出项（如 message、<code>web_extractor_call</code>）被添加到 output 数组时触发。当 <code>item.type</code> 为 <code>web_extractor_call</code> 时，表示网页抽取工具调用开始。</li><li><code>response.content_part.added</code>：输出项的 content 数组中新增内容块时触发。</li><li><code>response.output_text.delta</code>：增量文本生成时触发，多次触发，<code>delta</code> 字段包含新增文本片段。</li><li><code>response.output_text.done</code>：文本生成完成时触发，<code>text</code> 字段包含完整文本。</li><li><code>response.content_part.done</code>：内容块完成时触发，<code>part</code> 对象包含完整内容块。</li><li><code>response.output_item.done</code>：输出项生成完成时触发，<code>item</code> 对象包含完整输出项。当 <code>item.type</code> 为 <code>web_extractor_call</code> 时，表示网页抽取工具调用完成。</li><li><code>response.reasoning_text.delta</code>：（开启思考模式时）推理摘要增量文本，<code>delta</code> 字段包含新增摘要片段。</li><li><code>response.reasoning_text.done</code>：（开启思考模式时）推理摘要完成，<code>text</code> 字段包含完整摘要。</li><li><code>response.custom_tool_call_input.delta</code>：自定义工具增量文本</li><li><code>response.custom_tool_call_input.done</code>：自定义工具完成</li><li><code>response.web_search_call.in_progress</code> / <code>searching</code> / <code>completed</code>：（使用 web_search 工具时）搜索状态变化事件。</li><li><code>response.code_interpreter_call.in_progress</code> / <code>interpreting</code> / <code>completed</code>：（使用 code_interpreter 工具时）代码执行状态变化事件。</li><li><strong>注意：</strong>使用 <code>web_extractor</code> 工具时，没有专门的事件类型标识符。网页抽取工具调用通过通用的 <code>response.output_item.added</code> 和 <code>response.output_item.done</code> 事件传递，通过 <code>item.type</code> 字段（值为 <code>web_extractor_call</code>）来识别。</li><li><code>response.incomplete</code>：响应因 max_output_tokens等限制而提前结束</li><li><code>response.mcp_call_arguments.delta</code> / <code>response.mcp_call_arguments.done</code>：（使用 mcp 工具时）MCP 调用参数的增量和完成事件。</li><li><code>response.mcp_call.in_progress</code>：MCP 服务调用中。</li><li><code>response.mcp_call.completed</code>：（使用 mcp 工具时）MCP 服务调用完成。</li><li><code>response.file_search_call.in_progress</code> / <code>searching</code> / <code>completed</code>：（使用 file_search 工具时）知识库搜索状态变化事件。</li><li><strong>注意：</strong>使用 <code>web_search_image</code> 和 <code>image_search</code> 工具时，没有专门的中间状态事件。工具调用通过 <code>response.output_item.added</code>（调用开始）和 <code>response.output_item.done</code>（调用完成）事件传递。</li><li><code>response.completed</code>：响应生成完成时触发，<code>response</code> 对象包含完整响应（含 usage）。此事件标志流式传输结束。</li></ul><p><strong>sequence_number</strong> <code>integer</code></p><p>事件序列号，从 0 开始递增。用于确保客户端按正确顺序处理事件。</p><p><strong>response</strong> <code>object</code></p><p>响应对象。出现在 <code>response.created</code>、<code>response.in_progress</code> 和 <code>response.completed</code> 事件中。在 <code>response.completed</code> 事件中包含完整的响应数据（包括 <code>output</code> 和 <code>usage</code>），其结构与非流式响应的 Response 对象一致。</p><p><strong>item</strong> <code>object</code></p><p>输出项对象。出现在 <code>response.output_item.added</code> 和 <code>response.output_item.done</code> 事件中。在 <code>added</code> 事件中为初始骨架（content 为空数组），在 <code>done</code> 事件中为完整对象。</p><a id="accordion-属性-66"></a><section><p>属性</p><div><p><strong>id</strong> <code>string</code></p><p>输出项的唯一标识符（如 <code>msg_xxx</code>）。</p><p><strong>type</strong> <code>string</code></p><p>输出项类型。枚举值：<code>message</code>（消息）、<code>reasoning</code>（推理）、<code>web_search_call</code>（搜索）、<code>web_search_image_call</code>（文搜图）、<code>image_search_call</code>（图搜图）、<code>mcp_call</code>（MCP 调用）、<code>file_search_call</code>（知识库搜索）。</p><p><strong>role</strong> <code>string</code></p><p>消息角色，固定为 <code>assistant</code>。仅当 type 为 <code>message</code> 时存在。</p><p><strong>status</strong> <code>string</code></p><p>生成状态。在 <code>added</code> 事件中为 <code>in_progress</code>，在 <code>done</code> 事件中为 <code>completed</code>。</p><p><strong>content</strong> <code>array</code></p><p>消息内容数组。在 <code>added</code> 事件中为空数组 <code>[]</code>，在 <code>done</code> 事件中包含完整的内容块对象（结构与 <code>part</code> 对象相同）。</p></div></section><p><strong>part</strong> <code>object</code></p><p>内容块对象。出现在 <code>response.content_part.added</code> 和 <code>response.content_part.done</code> 事件中。</p><a id="accordion-属性-67"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code></p><p>内容块类型，固定为 <code>output_text</code>。</p><p><strong>text</strong> <code>string</code></p><p>文本内容。在 <code>added</code> 事件中为空字符串，在 <code>done</code> 事件中为完整文本。</p><p><strong>annotations</strong> <code>array</code></p><p>文本注释数组。通常为空数组。</p><p><strong>logprobs</strong> <code>object | null</code></p><p>Token 的对数概率信息。当前固定返回 <code>null</code>。</p></div></section><p><strong>delta</strong> <code>string</code></p><p>增量文本内容。出现在 <code>response.output_text.delta</code> 事件中，包含本次新增的文本片段。客户端应将所有 <code>delta</code> 拼接以获得完整文本。</p><p><strong>text</strong> <code>string</code></p><p>完整文本内容。出现在 <code>response.output_text.done</code> 事件中，包含该内容块的完整文本，可用于校验 <code>delta</code> 拼接结果。</p><p><strong>item_id</strong> <code>string</code></p><p>输出项的唯一标识符。用于关联同一输出项的相关事件。</p><p><strong>output_index</strong> <code>integer</code></p><p>输出项在 <code>output</code> 数组中的索引位置。</p><p><strong>content_index</strong> <code>integer</code></p><p>内容块在 <code>content</code> 数组中的索引位置。</p></td><td><div><p>以下为原有响应结构的流式示例。</p><a id="fig-code-group-9"></a><div><a id="fig-code-group-9-基础调用-tab"></a>基础调用<div><a id="code-code-group-9-基础调用"></a><pre class="language-json"><code>// response.created - 响应创建
{&quot;response&quot;:{&quot;id&quot;:&quot;428c90e9-9cd6-90a6-9726-c02b08ebexxx&quot;,&quot;created_at&quot;:1769082930,&quot;object&quot;:&quot;response&quot;,&quot;status&quot;:&quot;queued&quot;,...},&quot;sequence_number&quot;:0,&quot;type&quot;:&quot;response.created&quot;}

// response.in_progress - 响应进行中
{&quot;response&quot;:{&quot;id&quot;:&quot;428c90e9-9cd6-90a6-9726-c02b08ebexxx&quot;,&quot;status&quot;:&quot;in_progress&quot;,...},&quot;sequence_number&quot;:1,&quot;type&quot;:&quot;response.in_progress&quot;}

// response.output_item.added - 新增输出项
{&quot;item&quot;:{&quot;id&quot;:&quot;msg_bcb45d66-fc34-46a2-bb56-714a51e8exxx&quot;,&quot;content&quot;:[],&quot;role&quot;:&quot;assistant&quot;,&quot;status&quot;:&quot;in_progress&quot;,&quot;type&quot;:&quot;message&quot;},&quot;output_index&quot;:0,&quot;sequence_number&quot;:2,&quot;type&quot;:&quot;response.output_item.added&quot;}

// response.content_part.added - 新增内容块
{&quot;content_index&quot;:0,&quot;item_id&quot;:&quot;msg_bcb45d66-fc34-46a2-bb56-714a51e8exxx&quot;,&quot;output_index&quot;:0,&quot;part&quot;:{&quot;annotations&quot;:[],&quot;text&quot;:&quot;&quot;,&quot;type&quot;:&quot;output_text&quot;,&quot;logprobs&quot;:null},&quot;sequence_number&quot;:3,&quot;type&quot;:&quot;response.content_part.added&quot;}

// response.output_text.delta - 增量文本（多次触发）
{&quot;content_index&quot;:0,&quot;delta&quot;:&quot;人工智能&quot;,&quot;item_id&quot;:&quot;msg_bcb45d66-fc34-46a2-bb56-714a51e8exxx&quot;,&quot;logprobs&quot;:[],&quot;output_index&quot;:0,&quot;sequence_number&quot;:4,&quot;type&quot;:&quot;response.output_text.delta&quot;}
{&quot;content_index&quot;:0,&quot;delta&quot;:&quot;（Artificial Intelligence，&quot;,&quot;item_id&quot;:&quot;msg_bcb45d66-fc34-46a2-bb56-714a51e8exxx&quot;,&quot;logprobs&quot;:[],&quot;output_index&quot;:0,&quot;sequence_number&quot;:6,&quot;type&quot;:&quot;response.output_text.delta&quot;}

// response.output_text.done - 文本完成
{&quot;content_index&quot;:0,&quot;item_id&quot;:&quot;msg_bcb45d66-fc34-46a2-bb56-714a51e8exxx&quot;,&quot;logprobs&quot;:[],&quot;output_index&quot;:0,&quot;sequence_number&quot;:53,&quot;text&quot;:&quot;人工智能（Artificial Intelligence，简称 AI）是指由计算机系统模拟人类智能行为的技术和科学...&quot;,&quot;type&quot;:&quot;response.output_text.done&quot;}

// response.content_part.done - 内容块完成
{&quot;content_index&quot;:0,&quot;item_id&quot;:&quot;msg_bcb45d66-fc34-46a2-bb56-714a51e8exxx&quot;,&quot;output_index&quot;:0,&quot;part&quot;:{&quot;annotations&quot;:[],&quot;text&quot;:&quot;...完整文本...&quot;,&quot;type&quot;:&quot;output_text&quot;,&quot;logprobs&quot;:null},&quot;sequence_number&quot;:54,&quot;type&quot;:&quot;response.content_part.done&quot;}

// response.output_item.done - 输出项完成
{&quot;item&quot;:{&quot;id&quot;:&quot;msg_bcb45d66-fc34-46a2-bb56-714a51e8exxx&quot;,&quot;content&quot;:[{&quot;annotations&quot;:[],&quot;text&quot;:&quot;...完整文本...&quot;,&quot;type&quot;:&quot;output_text&quot;,&quot;logprobs&quot;:null}],&quot;role&quot;:&quot;assistant&quot;,&quot;status&quot;:&quot;completed&quot;,&quot;type&quot;:&quot;message&quot;},&quot;output_index&quot;:0,&quot;sequence_number&quot;:55,&quot;type&quot;:&quot;response.output_item.done&quot;}

// response.completed - 响应完成（包含完整响应和 usage）
{&quot;response&quot;:{&quot;id&quot;:&quot;428c90e9-9cd6-90a6-9726-c02b08ebexxx&quot;,&quot;created_at&quot;:1769082930,&quot;model&quot;:&quot;qwen3.7-max&quot;,&quot;object&quot;:&quot;response&quot;,&quot;output&quot;:[...],&quot;status&quot;:&quot;completed&quot;,&quot;usage&quot;:{&quot;input_tokens&quot;:37,&quot;output_tokens&quot;:243,&quot;total_tokens&quot;:280,...}},&quot;sequence_number&quot;:56,&quot;type&quot;:&quot;response.completed&quot;}
</code></pre></div><a id="fig-code-group-9-网页抓取-tab"></a>网页抓取<div><a id="code-code-group-9-网页抓取"></a><pre class="language-json"><code>id:1
event:response.created
:HTTP_STATUS/200
data:{&quot;sequence_number&quot;:0,&quot;type&quot;:&quot;response.created&quot;,&quot;response&quot;:{&quot;output&quot;:[],&quot;parallel_tool_calls&quot;:false,&quot;created_at&quot;:1769435906,&quot;tool_choice&quot;:&quot;auto&quot;,&quot;model&quot;:&quot;&quot;,&quot;id&quot;:&quot;863df8d9-cb29-4239-a54f-3e15a2427xxx&quot;,&quot;tools&quot;:[],&quot;object&quot;:&quot;response&quot;,&quot;status&quot;:&quot;queued&quot;}}

id:2
event:response.in_progress
:HTTP_STATUS/200
data:{&quot;sequence_number&quot;:1,&quot;type&quot;:&quot;response.in_progress&quot;,&quot;response&quot;:{&quot;output&quot;:[],&quot;parallel_tool_calls&quot;:false,&quot;created_at&quot;:1769435906,&quot;tool_choice&quot;:&quot;auto&quot;,&quot;model&quot;:&quot;&quot;,&quot;id&quot;:&quot;863df8d9-cb29-4239-a54f-3e15a2427xxx&quot;,&quot;tools&quot;:[],&quot;object&quot;:&quot;response&quot;,&quot;status&quot;:&quot;in_progress&quot;}}

id:3
event:response.output_item.added
:HTTP_STATUS/200
data:{&quot;sequence_number&quot;:2,&quot;item&quot;:{&quot;summary&quot;:[],&quot;type&quot;:&quot;reasoning&quot;,&quot;id&quot;:&quot;msg_5bd0c6df-19b8-4a04-bc00-8042a224exxx&quot;},&quot;output_index&quot;:0,&quot;type&quot;:&quot;response.output_item.added&quot;}

id:4
event:response.reasoning_text.delta
:HTTP_STATUS/200
data:{&quot;delta&quot;:&quot;用户想要我：\n1. 搜索阿里云官网\n2. 提取官网首页的关键信息\n\n我需要先搜索阿里云官网的URL，然后使用web_extractor工具访问官网并提取关键信息。&quot;,&quot;sequence_number&quot;:3,&quot;output_index&quot;:0,&quot;type&quot;:&quot;response.reasoning_text.delta&quot;,&quot;item_id&quot;:&quot;msg_5bd0c6df-19b8-4a04-bc00-8042a224exxx&quot;}

id:14
event:response.reasoning_text.done
:HTTP_STATUS/200
data:{&quot;sequence_number&quot;:13,&quot;text&quot;:&quot;用户想要我：\n1. 搜索阿里云官网\n2. 提取官网首页的关键信息\n\n我需要先搜索阿里云官网的URL，然后使用web_extractor工具访问官网并提取关键信息。&quot;,&quot;output_index&quot;:0,&quot;type&quot;:&quot;response.reasoning_text.done&quot;,&quot;item_id&quot;:&quot;msg_5bd0c6df-19b8-4a04-bc00-8042a224exxx&quot;}

id:15
event:response.output_item.done
:HTTP_STATUS/200
data:{&quot;sequence_number&quot;:14,&quot;item&quot;:{&quot;summary&quot;:[{&quot;type&quot;:&quot;summary_text&quot;,&quot;text&quot;:&quot;用户想要我：\n1. 搜索阿里云官网\n2. 提取官网首页的关键信息\n\n我需要先搜索阿里云官网的URL，然后使用web_extractor工具访问官网并提取关键信息。&quot;}],&quot;type&quot;:&quot;reasoning&quot;,&quot;id&quot;:&quot;msg_5bd0c6df-19b8-4a04-bc00-8042a224exxx&quot;},&quot;output_index&quot;:1,&quot;type&quot;:&quot;response.output_item.done&quot;}

id:16
event:response.output_item.added
:HTTP_STATUS/200
data:{&quot;sequence_number&quot;:15,&quot;item&quot;:{&quot;action&quot;:{&quot;type&quot;:&quot;search&quot;,&quot;query&quot;:&quot;Web search&quot;},&quot;id&quot;:&quot;msg_a8a686b1-0a57-40e1-bb55-049a89cd4xxx&quot;,&quot;type&quot;:&quot;web_search_call&quot;,&quot;status&quot;:&quot;in_progress&quot;},&quot;output_index&quot;:1,&quot;type&quot;:&quot;response.output_item.added&quot;}

id:17
event:response.web_search_call.in_progress
:HTTP_STATUS/200
data:{&quot;sequence_number&quot;:16,&quot;output_index&quot;:1,&quot;type&quot;:&quot;response.web_search_call.in_progress&quot;,&quot;item_id&quot;:&quot;msg_a8a686b1-0a57-40e1-bb55-049a89cd4xxx&quot;}

id:19
event:response.web_search_call.completed
:HTTP_STATUS/200
data:{&quot;sequence_number&quot;:18,&quot;output_index&quot;:1,&quot;type&quot;:&quot;response.web_search_call.completed&quot;,&quot;item_id&quot;:&quot;msg_a8a686b1-0a57-40e1-bb55-049a89cd4xxx&quot;}

id:20
event:response.output_item.done
:HTTP_STATUS/200
data:{&quot;sequence_number&quot;:19,&quot;item&quot;:{&quot;action&quot;:{&quot;sources&quot;:[{&quot;type&quot;:&quot;url&quot;,&quot;url&quot;:&quot;https://cn.aliyun.com/&quot;},{&quot;type&quot;:&quot;url&quot;,&quot;url&quot;:&quot;https://www.aliyun.com/&quot;}],&quot;type&quot;:&quot;search&quot;,&quot;query&quot;:&quot;Web search&quot;},&quot;id&quot;:&quot;msg_a8a686b1-0a57-40e1-bb55-049a89cd4xxx&quot;,&quot;type&quot;:&quot;web_search_call&quot;,&quot;status&quot;:&quot;completed&quot;},&quot;output_index&quot;:1,&quot;type&quot;:&quot;response.output_item.done&quot;}

id:33
event:response.output_item.added
:HTTP_STATUS/200
data:{&quot;sequence_number&quot;:32,&quot;item&quot;:{&quot;urls&quot;:[&quot;https://cn.aliyun.com/&quot;],&quot;goal&quot;:&quot;提取阿里云官网首页的关键信息，包括：公司定位/简介、核心产品与服务、主要业务板块、特色功能/解决方案、最新动态/活动、免费试用/优惠信息、导航菜单结构等&quot;,&quot;id&quot;:&quot;msg_8c2cf651-48a5-460c-aa7a-bea5b09b4xxx&quot;,&quot;type&quot;:&quot;web_extractor_call&quot;,&quot;status&quot;:&quot;in_progress&quot;},&quot;output_index&quot;:3,&quot;type&quot;:&quot;response.output_item.added&quot;}

id:34
event:response.output_item.done
:HTTP_STATUS/200
data:{&quot;sequence_number&quot;:33,&quot;item&quot;:{&quot;output&quot;:&quot;The useful information in https://cn.aliyun.com/ for user goal 提取阿里云官网首页的关键信息，包括：公司定位/简介、核心产品与服务、主要业务板块、特色功能/解决方案、最新动态/活动、免费试用/优惠信息、导航菜单结构等 as follows: \n\nEvidence in page: \n## 通义大模型，企业拥抱 AI 时代首选\n\n## 完整的产品体系，为企业打造技术创新的云\n\n全部云产品## 依托大模型与云计算协同发展，让 AI 触手可及\n\n全部 AI 解决方案\n\nSummary: \nAlibaba Cloud positions itself as a leading enterprise AI solution provider centered around the Tongyi large model...&quot;,&quot;urls&quot;:[&quot;https://cn.aliyun.com/&quot;],&quot;goal&quot;:&quot;提取阿里云官网首页的关键信息，包括：公司定位/简介、核心产品与服务、主要业务板块、特色功能/解决方案、最新动态/活动、免费试用/优惠信息、导航菜单结构等&quot;,&quot;id&quot;:&quot;msg_8c2cf651-48a5-460c-aa7a-bea5b09b4xxx&quot;,&quot;type&quot;:&quot;web_extractor_call&quot;,&quot;status&quot;:&quot;completed&quot;},&quot;output_index&quot;:3,&quot;type&quot;:&quot;response.output_item.done&quot;}

id:50
event:response.output_item.added
:HTTP_STATUS/200
data:{&quot;sequence_number&quot;:50,&quot;item&quot;:{&quot;content&quot;:[{&quot;type&quot;:&quot;text&quot;,&quot;text&quot;:&quot;&quot;}],&quot;type&quot;:&quot;message&quot;,&quot;id&quot;:&quot;msg_final&quot;,&quot;role&quot;:&quot;assistant&quot;},&quot;output_index&quot;:5,&quot;type&quot;:&quot;response.output_item.added&quot;}

id:51
event:response.output_text.delta
:HTTP_STATUS/200
data:{&quot;delta&quot;:&quot;我已经找到阿里云官网并提取了首页的关键信息：\n\n&quot;,&quot;sequence_number&quot;:51,&quot;output_index&quot;:5,&quot;type&quot;:&quot;response.output_text.delta&quot;}

id:60
event:response.completed
:HTTP_STATUS/200
data:{&quot;type&quot;:&quot;response.completed&quot;,&quot;response&quot;:{&quot;id&quot;:&quot;863df8d9-cb29-4239-a54f-3e15a2427xxx&quot;,&quot;status&quot;:&quot;completed&quot;,&quot;usage&quot;:{&quot;input_tokens&quot;:45,&quot;output_tokens&quot;:320,&quot;total_tokens&quot;:365}}}
</code></pre></div><a id="fig-code-group-9-文搜图-tab"></a>文搜图<div><a id="code-code-group-9-文搜图"></a><pre class="language-json"><code>// 1. response.created - 响应创建
id:1
event:response.created
data:{&quot;sequence_number&quot;:0,&quot;type&quot;:&quot;response.created&quot;,&quot;response&quot;:{&quot;output&quot;:[],&quot;status&quot;:&quot;queued&quot;,...}}

// 2. response.in_progress - 响应进行中
id:2
event:response.in_progress
data:{&quot;sequence_number&quot;:1,&quot;type&quot;:&quot;response.in_progress&quot;,&quot;response&quot;:{&quot;status&quot;:&quot;in_progress&quot;,...}}

// 3. response.output_item.added - 推理开始（reasoning）
id:3
event:response.output_item.added
data:{&quot;sequence_number&quot;:2,&quot;item&quot;:{&quot;summary&quot;:[],&quot;type&quot;:&quot;reasoning&quot;,&quot;id&quot;:&quot;msg_xxx&quot;},&quot;output_index&quot;:0,&quot;type&quot;:&quot;response.output_item.added&quot;}

// 4. response.reasoning_text.delta - 推理摘要增量
id:4
event:response.reasoning_text.delta
data:{&quot;delta&quot;:&quot;用户想要找一张猫咪图片。我需要使用web_search_image工具来搜索...&quot;,&quot;sequence_number&quot;:3,&quot;output_index&quot;:0,&quot;type&quot;:&quot;response.reasoning_text.delta&quot;,&quot;item_id&quot;:&quot;msg_xxx&quot;}

// 5. response.reasoning_text.done - 推理摘要完成
id:10
event:response.reasoning_text.done
data:{&quot;sequence_number&quot;:9,&quot;text&quot;:&quot;用户想要找一张猫咪图片。我需要使用web_search_image工具来搜索猫咪图片。&quot;,&quot;output_index&quot;:0,&quot;type&quot;:&quot;response.reasoning_text.done&quot;,&quot;item_id&quot;:&quot;msg_xxx&quot;}

// 6. response.output_item.done - 推理项完成
id:11
event:response.output_item.done
data:{&quot;sequence_number&quot;:10,&quot;item&quot;:{&quot;summary&quot;:[{&quot;type&quot;:&quot;summary_text&quot;,&quot;text&quot;:&quot;...&quot;}],&quot;type&quot;:&quot;reasoning&quot;,&quot;id&quot;:&quot;msg_xxx&quot;},&quot;output_index&quot;:0,&quot;type&quot;:&quot;response.output_item.done&quot;}

// 7. response.output_item.added - 文搜图工具调用开始（status: in_progress，此时已包含 name 和 arguments）
id:12
event:response.output_item.added
data:{&quot;sequence_number&quot;:11,&quot;item&quot;:{&quot;name&quot;:&quot;web_search_image&quot;,&quot;arguments&quot;:&quot;{\&quot;queries\&quot;: [\&quot;猫咪图片\&quot;, \&quot;cute cat\&quot;]}&quot;,&quot;id&quot;:&quot;msg_xxx&quot;,&quot;type&quot;:&quot;web_search_image_call&quot;,&quot;status&quot;:&quot;in_progress&quot;},&quot;output_index&quot;:1,&quot;type&quot;:&quot;response.output_item.added&quot;}

// 8. response.output_item.done - 文搜图工具调用完成（包含完整的 output 搜索结果）
id:13
event:response.output_item.done
data:{&quot;sequence_number&quot;:12,&quot;item&quot;:{&quot;name&quot;:&quot;web_search_image&quot;,&quot;output&quot;:&quot;[{\&quot;title\&quot;: \&quot;可爱的小猫咪...\&quot;, \&quot;url\&quot;: \&quot;https://example.com/cat.jpg\&quot;, \&quot;index\&quot;: 1}, ...]&quot;,&quot;arguments&quot;:&quot;{\&quot;queries\&quot;: [\&quot;猫咪图片\&quot;, \&quot;cute cat\&quot;]}&quot;,&quot;id&quot;:&quot;msg_xxx&quot;,&quot;type&quot;:&quot;web_search_image_call&quot;,&quot;status&quot;:&quot;completed&quot;},&quot;output_index&quot;:1,&quot;type&quot;:&quot;response.output_item.done&quot;}

// 9-12. 第二轮推理 + 最终消息输出（与基础调用相同）
// response.output_item.added (reasoning) → reasoning_text.delta/done → response.output_item.done (reasoning)
// response.output_item.added (message) → response.content_part.added → response.output_text.delta → response.output_text.done → response.content_part.done → response.output_item.done (message)

// 13. response.completed - 响应完成
id:118
event:response.completed
data:{&quot;sequence_number&quot;:117,&quot;type&quot;:&quot;response.completed&quot;,&quot;response&quot;:{&quot;output&quot;:[...],&quot;status&quot;:&quot;completed&quot;,&quot;usage&quot;:{&quot;input_tokens&quot;:7895,&quot;output_tokens&quot;:318,&quot;total_tokens&quot;:8213,&quot;x_tools&quot;:{&quot;web_search_image&quot;:{&quot;count&quot;:1}}}}}
</code></pre></div><a id="fig-code-group-9-图搜图-tab"></a>图搜图<div><a id="code-code-group-9-图搜图"></a><pre class="language-json"><code>// 1-6. 推理阶段（与文搜图相同）

// 7. response.output_item.added - 图搜图工具调用开始
// 注意 arguments 中包含 img_idx（图片索引）和 bbox（搜索区域边界框）
id:29
event:response.output_item.added
data:{&quot;sequence_number&quot;:29,&quot;item&quot;:{&quot;name&quot;:&quot;image_search&quot;,&quot;arguments&quot;:&quot;{\&quot;img_idx\&quot;: 0, \&quot;bbox\&quot;: [0, 0, 1000, 1000]}&quot;,&quot;id&quot;:&quot;msg_xxx&quot;,&quot;type&quot;:&quot;image_search_call&quot;,&quot;status&quot;:&quot;in_progress&quot;},&quot;output_index&quot;:1,&quot;type&quot;:&quot;response.output_item.added&quot;}

// 8. response.output_item.done - 图搜图工具调用完成
id:30
event:response.output_item.done
data:{&quot;sequence_number&quot;:30,&quot;item&quot;:{&quot;name&quot;:&quot;image_search&quot;,&quot;output&quot;:&quot;[{\&quot;title\&quot;: \&quot;水墨山背景...\&quot;, \&quot;url\&quot;: \&quot;https://example.com/landscape.jpg\&quot;, \&quot;index\&quot;: 1}, ...]&quot;,&quot;arguments&quot;:&quot;{\&quot;img_idx\&quot;: 0, \&quot;bbox\&quot;: [0, 0, 1000, 1000]}&quot;,&quot;id&quot;:&quot;msg_xxx&quot;,&quot;type&quot;:&quot;image_search_call&quot;,&quot;status&quot;:&quot;completed&quot;},&quot;output_index&quot;:1,&quot;type&quot;:&quot;response.output_item.done&quot;}

// 9-12. 第二轮推理 + 最终消息输出（与基础调用相同）

// 13. response.completed
id:408
event:response.completed
data:{&quot;sequence_number&quot;:407,&quot;type&quot;:&quot;response.completed&quot;,&quot;response&quot;:{&quot;output&quot;:[...],&quot;status&quot;:&quot;completed&quot;,&quot;usage&quot;:{&quot;input_tokens&quot;:8371,&quot;output_tokens&quot;:417,&quot;total_tokens&quot;:8788,&quot;x_tools&quot;:{&quot;image_search&quot;:{&quot;count&quot;:1}}}}}
</code></pre></div><a id="fig-code-group-9-mcp-tab"></a>MCP<div><a id="code-code-group-9-mcp"></a><pre class="language-json"><code>// 1-6. 推理阶段（与其他工具相同）

// 7. response.mcp_call_arguments.delta - MCP 参数增量（MCP 独有事件）
id:27
event:response.mcp_call_arguments.delta
data:{&quot;delta&quot;:&quot;{\&quot;city\&quot;: \&quot;北京\&quot;}&quot;,&quot;sequence_number&quot;:26,&quot;output_index&quot;:1,&quot;type&quot;:&quot;response.mcp_call_arguments.delta&quot;,&quot;item_id&quot;:&quot;msg_xxx&quot;}

// 8. response.mcp_call_arguments.done - MCP 参数完成（MCP 独有事件）
id:28
event:response.mcp_call_arguments.done
data:{&quot;sequence_number&quot;:27,&quot;arguments&quot;:&quot;{\&quot;city\&quot;: \&quot;北京\&quot;}&quot;,&quot;output_index&quot;:1,&quot;type&quot;:&quot;response.mcp_call_arguments.done&quot;,&quot;item_id&quot;:&quot;msg_xxx&quot;}

// 9. response.output_item.added - MCP 工具调用开始（包含 name、server_label、arguments）
id:29
event:response.output_item.added
data:{&quot;sequence_number&quot;:28,&quot;item&quot;:{&quot;name&quot;:&quot;amap-maps-maps_weather&quot;,&quot;server_label&quot;:&quot;MCP Server&quot;,&quot;arguments&quot;:&quot;{\&quot;city\&quot;: \&quot;北京\&quot;}&quot;,&quot;id&quot;:&quot;msg_xxx&quot;,&quot;type&quot;:&quot;mcp_call&quot;,&quot;status&quot;:&quot;in_progress&quot;},&quot;output_index&quot;:1,&quot;type&quot;:&quot;response.output_item.added&quot;}

// 10. response.mcp_call.completed - MCP 调用完成（MCP 独有事件）
id:30
event:response.mcp_call.completed
data:{&quot;sequence_number&quot;:29,&quot;output_index&quot;:1,&quot;type&quot;:&quot;response.mcp_call.completed&quot;,&quot;item_id&quot;:&quot;msg_xxx&quot;}

// 11. response.output_item.done - MCP 输出项完成（包含完整 output）
id:31
event:response.output_item.done
data:{&quot;sequence_number&quot;:30,&quot;item&quot;:{&quot;output&quot;:&quot;{\&quot;city\&quot;:\&quot;北京市\&quot;,\&quot;forecasts\&quot;:[...]}&quot;,&quot;name&quot;:&quot;amap-maps-maps_weather&quot;,&quot;server_label&quot;:&quot;MCP Server&quot;,&quot;arguments&quot;:&quot;{\&quot;city\&quot;: \&quot;北京\&quot;}&quot;,&quot;id&quot;:&quot;msg_xxx&quot;,&quot;type&quot;:&quot;mcp_call&quot;,&quot;status&quot;:&quot;completed&quot;},&quot;output_index&quot;:1,&quot;type&quot;:&quot;response.output_item.done&quot;}

// 12-15. 第二轮推理 + 最终消息输出

// 16. response.completed
id:172
event:response.completed
data:{&quot;sequence_number&quot;:171,&quot;type&quot;:&quot;response.completed&quot;,&quot;response&quot;:{&quot;output&quot;:[...],&quot;status&quot;:&quot;completed&quot;,&quot;usage&quot;:{&quot;input_tokens&quot;:5019,&quot;output_tokens&quot;:539,&quot;total_tokens&quot;:5558}}}
</code></pre></div><a id="fig-code-group-9-知识库搜索-tab"></a>知识库搜索<div><a id="code-code-group-9-知识库搜索"></a><pre class="language-json"><code>// 1-6. 推理阶段（与其他工具相同）

// 7. response.output_item.added - 知识库搜索开始（包含 queries，无 results）
id:19
event:response.output_item.added
data:{&quot;sequence_number&quot;:18,&quot;item&quot;:{&quot;id&quot;:&quot;msg_xxx&quot;,&quot;type&quot;:&quot;file_search_call&quot;,&quot;queries&quot;:[&quot;阿里云百炼X1手机&quot;,&quot;Alibaba Cloud Bailian X1 phone&quot;,&quot;百炼X1&quot;],&quot;status&quot;:&quot;in_progress&quot;},&quot;output_index&quot;:1,&quot;type&quot;:&quot;response.output_item.added&quot;}

// 8. response.file_search_call.in_progress - 搜索进行中（file_search 独有事件）
id:20
event:response.file_search_call.in_progress
data:{&quot;sequence_number&quot;:19,&quot;output_index&quot;:1,&quot;type&quot;:&quot;response.file_search_call.in_progress&quot;,&quot;item_id&quot;:&quot;msg_xxx&quot;}

// 9. response.file_search_call.searching - 正在搜索（file_search 独有事件）
id:21
event:response.file_search_call.searching
data:{&quot;sequence_number&quot;:20,&quot;output_index&quot;:1,&quot;type&quot;:&quot;response.file_search_call.searching&quot;,&quot;item_id&quot;:&quot;msg_xxx&quot;}

// 10. response.file_search_call.completed - 搜索完成（file_search 独有事件）
id:22
event:response.file_search_call.completed
data:{&quot;sequence_number&quot;:21,&quot;output_index&quot;:1,&quot;type&quot;:&quot;response.file_search_call.completed&quot;,&quot;item_id&quot;:&quot;msg_xxx&quot;}

// 11. response.output_item.done - 输出项完成（包含 queries + results）
id:23
event:response.output_item.done
data:{&quot;sequence_number&quot;:22,&quot;item&quot;:{&quot;id&quot;:&quot;msg_xxx&quot;,&quot;type&quot;:&quot;file_search_call&quot;,&quot;queries&quot;:[&quot;阿里云百炼X1手机&quot;,&quot;Alibaba Cloud Bailian X1 phone&quot;,&quot;百炼X1&quot;],&quot;results&quot;:[{&quot;score&quot;:0.7519,&quot;filename&quot;:&quot;阿里云百炼系列手机产品介绍&quot;,&quot;text&quot;:&quot;阿里云百炼 X1 ——畅享极致视界...&quot;,&quot;file_id&quot;:&quot;file_xxx&quot;}],&quot;status&quot;:&quot;completed&quot;},&quot;output_index&quot;:1,&quot;type&quot;:&quot;response.output_item.done&quot;}

// 12-15. 第二轮推理 + 最终消息输出

// 16. response.completed
id:146
event:response.completed
data:{&quot;sequence_number&quot;:145,&quot;type&quot;:&quot;response.completed&quot;,&quot;response&quot;:{&quot;output&quot;:[...],&quot;status&quot;:&quot;completed&quot;,&quot;usage&quot;:{&quot;input_tokens&quot;:1576,&quot;output_tokens&quot;:722,&quot;total_tokens&quot;:2298,&quot;x_tools&quot;:{&quot;file_search&quot;:{&quot;count&quot;:1}}}}}
</code></pre></div></div></div></td></tr></tbody></table>

<a id="常见问题"></a>

<a id="614711697dm4t"></a>

## 常见问题

**Q：如何传递多轮对话的上下文？**

A：在发起新一轮对话请求时，请将上一轮模型响应成功返回的`id`作为 `previous_response_id` 参数传入。

**Q：为什么响应示例中的某些字段未在本文说明？**

A：如果使用OpenAI的官方SDK，它可能会根据其自身的模型结构输出一些额外的字段（通常为`null`）。这些字段是OpenAI协议本身定义的，我们的服务当前不支持，所以它们为空值。只需关注本文档中描述的字段即可。
