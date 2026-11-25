# Qwen-MT-Uni API参考

<a id="模型概览"></a>

<a id="uni-overview"></a>

## 模型概览

Qwen-MT-Uni 是一款面向图片、文本、音频及各类文档的全模态翻译模型，通过统一的格式识别、智能路由、内容抽取、跨模态翻译与原格式重构链路，实现多类型输入的一体化高保真翻译。同时提供**同步调用**（请求后等待并直接返回翻译结果，适合文本、图片、小文件等耗时较短的场景）和**异步调用**（请求头加 `X-DashScope-Async: enable`，先返回 `task_id`，再通过查询接口轮询结果，适合大文档、长音频等耗时较长的场景）两种模式。

接口采用 DashScope 标准协议，同步调用顶层出现字符串 `code` 表示失败（错误码 = `code`，原因 = `message`），否则顶层有 `output` 表示成功（结果在 `output.Data`，用量在 `usage`）；异步调用需轮询查询接口，直到 `output.task_status = SUCCEEDED`（任务执行完毕），再看 `output.Success`：`true` 表示业务成功、`false` 表示业务失败（原因在 `output.Code`、`output.Message`）。

<a id="前提条件"></a>

<a id="uni-prerequisites"></a>

## 前提条件

您需要已[获取与配置 API Key](../preparations/get-api-key.md)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

<a id="支持的输入格式"></a>

<a id="uni-input-formats"></a>

## 支持的输入格式

-   **字符串**：输入 `str` 或 `list[str]`，输出保持相同的标量/数组形状。
-   **PDF**：输入 `.pdf`，输出 `.pdf`。
-   **Word**：输入 `.docx`，输出 `.docx`。
-   **PowerPoint**：输入 `.pptx`，输出 `.pptx`。
-   **Excel**：输入 `.xlsx`，输出 `.xlsx`。
-   **TXT**：输入 `.txt`，输出 `.txt`。
-   **HTML**：输入 `.html`、`.htm`，输出 `.html`。
-   **Markdown**：输入 `.md`、`.markdown`、`.mdown`、`.mkd`，输出 `.md`。
-   **图像**：输入 `.png`、`.jpg`、`.jpeg`，输出 `.jpg`。
-   **音频**：输入 `.mp3`、`.wav`，输出 `.mp3`。

> **说明**
>
> -   单文件不超过 **100 MB**，文档不超过 **200 页**，音频时长需在 **3 秒～60 分钟** 之间。
> -   URL 地址中不能包含中文字符。
> -   旧版二进制 Word（`.doc`）和 PowerPoint（`.ppt`）需要先转换为 OOXML 格式（`.docx`/`.pptx`）再传入。

<a id="同步调用"></a>

<a id="uni-sync"></a>

## 同步调用

`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`，调用时请将 `{WorkspaceId}` 替换为真实的[Workspace ID](../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

同步模式下，请求会等待处理完成后直接返回翻译结果（文本或译后文件 URL），无需轮询任务状态。

<table><tbody><tr><td><h4>请求参数</h4><h5>请求头（Headers）</h5><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为 <code>application/json</code>。</p><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼 API Key 进行身份认证。示例值：<code>Bearer sk-xxxx</code>。</p><h5>请求体（Request Body）</h5><p><strong>model</strong> <code>string</code> <strong>（必选）</strong></p><p>模型名称，设置为 <code>qwen-mt-uni</code>。</p><p><strong>input</strong> <code>object</code> <strong>（必选）</strong></p><p>输入参数对象，包含以下字段：</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>fileUrl</strong> <code>string</code> <strong>（条件必选）</strong></p><p>可访问的 HTTP(S) URL，服务端自动判断模态类型（文档 / 图片 / 音频）。</p><ul><li><strong>支持格式</strong>：PDF、DOCX、PPTX、XLSX、TXT、HTML、Markdown、JPG、PNG、MP3、WAV。</li><li><strong>大小限制</strong>：单文件不超过 100 MB，文档不超过 200 页，音频时长需在 3 秒～60 分钟之间。</li><li>URL 地址中不能包含中文字符。</li><li>与 <code>source_texts</code> <strong>必须且只能提供一个</strong>。</li></ul><p><strong>source_texts</strong> <code>string | array&lt;string&gt;</code> <strong>（条件必选）</strong></p><p>一条非空字符串或非空字符串数组。批量翻译保持输入顺序，响应保持标量/数组形状。与 <code>fileUrl</code> <strong>必须且只能提供一个</strong>。</p><p><strong>source_lang</strong> <code>string</code> （可选）</p><p>源语言代码，例如 <code>zh</code>。不填则自动识别。</p><p><strong>target_lang</strong> <code>string</code> <strong>（必选）</strong></p><p>目标语言代码或项目支持的语言名称，例如 <code>ko</code>。详见<a href="qwen-mt-uni-api.md#uni-languages">支持的语种</a>。</p><p><strong>ext</strong> <code>object</code> （可选）</p><p>扩展字段对象。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>domainHint</strong> <code>string</code> （可选）</p><p>英文领域提示，最多 200 个英文单词。为使译文风格更贴合特定领域，可以使用英文描述使用场景、译文风格等需求。</p><div><div><p><strong>重要</strong>领域提示语句当前<strong>只支持英文</strong>。</p></div></div><p><strong>示例：</strong><code>These sentences are from seller-buyer conversations on a B2C ecommerce platform. Translate them into clear, engaging customer service language.</code></p><p><strong>format_hint</strong> <code>string</code> （可选）</p><p>格式提示。当 <code>fileUrl</code> 没有可识别后缀时，用它显式指定格式，如 <code>pdf</code>、<code>image</code>。</p><p><strong>sensitives</strong> <code>array</code> （可选）</p><p>敏感词列表，<strong>区分大小写</strong>，最多 50 个非空字符串。提取文本与某项完全相同时保留原文且不发送给模型。</p><p><strong>示例：</strong><code>[&quot;全场9折&quot;, &quot;七天无理由退换&quot;]</code></p><p><strong>glossary</strong> <code>array</code> （可选）</p><p>术语表，最多 100 组 <code>{&quot;src&quot;: &quot;源文本&quot;, &quot;tgt&quot;: &quot;目标文本&quot;}</code>。当前作为 Prompt 术语表接入，支持保持原文、指定翻译和空目标词。</p><p><strong>示例：</strong><code>[{&quot;src&quot;: &quot;应用程序接口&quot;, &quot;tgt&quot;: &quot;API&quot;}, {&quot;src&quot;: &quot;机器学习&quot;, &quot;tgt&quot;: &quot;ML&quot;}]</code></p><p><strong>config</strong> <code>object</code> （可选）</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>imageSegment</strong> <code>bool</code> （可选）</p><p><strong>仅图像格式生效</strong>。是否开启图像主体分割。开启后，将跳过对图像中主体（如人物、商品、Logo）上文字的翻译。</p><ul><li><code>false</code>：（默认值）翻译图像中的所有文字。</li><li><code>true</code>：不翻译图像主体的文字。</li></ul></div></section></div></section></div></section></td><td><a id="code-block"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
    &quot;model&quot;: &quot;qwen-mt-uni&quot;,
    &quot;input&quot;: {
        &quot;fileUrl&quot;: &quot;https://maas-infra-public.oss-cn-hangzhou.aliyuncs.com/lzhe/test/03bc3a6a-a02b-11f1-8874-00163e79676e.jpg&quot;,
        &quot;target_lang&quot;: &quot;zh&quot;
    }
}'
</code></pre></td></tr></tbody></table>

<table><tbody><tr><td><h4>响应参数（成功）</h4><p><strong>output</strong> <code>object</code></p><p>业务结果容器；成功时返回，失败时不返回。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>Success</strong> <code>boolean</code></p><p>是否成功，成功为 <code>true</code>。</p><p><strong>Code</strong> <code>integer</code></p><p>业务结果码，成功为 <code>200</code>。</p><p><strong>Message</strong> <code>string</code></p><p>结果说明，成功固定为 <code>Success</code>。</p><p><strong>RequestId</strong> <code>string</code></p><p>本次调用的唯一 ID，便于问题排查。</p><p><strong>Data</strong> <code>object</code></p><p>翻译结果。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>FileType</strong> <code>string</code></p><p>结果类型，可能值：<code>strings</code>（文本）/ <code>document</code>（文档）/ <code>image</code>（图片）/ <code>audio</code>（音频）。</p><p><strong>TranslatedTexts</strong> <code>string | array&lt;string&gt;</code></p><p>文本翻译结果。<strong>仅传 <code>source_texts</code> 时返回</strong>，形状与入参一致。</p><p><strong>TranslatedFileUrl</strong> <code>string</code></p><p>译后文件的下载地址（带签名，有有效期）。<strong>仅传 <code>fileUrl</code> 时返回</strong>。</p></div></section></div></section><p><strong>usage</strong> <code>object</code></p><p>Token 用量统计（在 output 之外的顶层），按 <code>input_tokens</code> 计费。</p><a id="accordion-属性-6"></a><section><p>属性</p><div><p><strong>input_tokens</strong> <code>integer</code></p><p>输入 Token 总量。</p><p><strong>output_tokens</strong> <code>integer</code></p><p>输出 Token 总量。</p><p><strong>total_tokens</strong> <code>integer</code></p><p>输入与输出 Token 总量。</p><p><strong>input_tokens_details</strong> <code>object</code></p><p>按内容类型划分的输入 Token 用量明细，包含 <code>document_tokens</code>、<code>audio_tokens</code>、<code>character_tokens</code>、<code>image_tokens</code>。</p><p><strong>output_tokens_details</strong> <code>object</code></p><p>按内容类型划分的输出 Token 用量明细，字段同 <code>input_tokens_details</code>。</p></div></section><p><strong>request_id</strong> <code>string</code></p><p>顶层请求 ID，成功和失败均返回。</p><h4>响应参数（失败）</h4><p><strong>code</strong> <code>string</code></p><p>错误码字符串，如 <code>InvalidParameter</code>。<strong>仅失败返回</strong>。</p><p><strong>message</strong> <code>string</code></p><p>错误详情，形如 <code>InvalidParameter: &lt;原因&gt;</code>。<strong>仅失败返回</strong>。</p><p><strong>request_id</strong> <code>string</code></p><p>请求 ID。</p></td><td><a id="sec-tabs"></a><section><a id="成功响应"></a><section><a id="成功响应-h4"></a><h4>成功响应</h4><a id="code-block-2"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
        &quot;Code&quot;: 200,
        &quot;Data&quot;: {
            &quot;FileType&quot;: &quot;image&quot;,
            &quot;TranslatedFileUrl&quot;: &quot;http://dashscope-a717.oss-cn-beijing.aliyuncs.com/xxx.jpg?Expires=xxx&quot;
        },
        &quot;Message&quot;: &quot;Success&quot;,
        &quot;RequestId&quot;: &quot;a20aa16a-2445-929f-9130-af70b4a0ade4&quot;,
        &quot;Success&quot;: true
    },
    &quot;usage&quot;: {
        &quot;input_tokens&quot;: 1887,
        &quot;input_tokens_details&quot;: {
            &quot;audio_tokens&quot;: 0,
            &quot;character_tokens&quot;: 0,
            &quot;document_tokens&quot;: 0,
            &quot;image_tokens&quot;: 1887
        },
        &quot;output_tokens&quot;: 1887,
        &quot;output_tokens_details&quot;: {
            &quot;audio_tokens&quot;: 0,
            &quot;character_tokens&quot;: 0,
            &quot;document_tokens&quot;: 0,
            &quot;image_tokens&quot;: 1887
        },
        &quot;total_tokens&quot;: 3774
    },
    &quot;request_id&quot;: &quot;a20aa16a-2445-929f-9130-af70b4a0ade4&quot;
}
</code></pre></section><a id="异常响应"></a><section><a id="异常响应-h4"></a><h4>异常响应</h4><p>请参见<a href="qwen-mt-uni-api.md#uni-errors">错误码</a>进行解决。</p><a id="code-block-3"></a><pre class="language-json"><code>{
    &quot;code&quot;: &quot;InvalidParameter&quot;,
    &quot;message&quot;: &quot;InvalidParameter: missing required field: input.target_lang&quot;,
    &quot;request_id&quot;: &quot;a20aa16a-2445-929f-9130-af70b4a0ade4&quot;
}
</code></pre></section></section></td></tr></tbody></table>

<a id="异步调用"></a>

<a id="uni-async"></a>

## 异步调用

`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`，调用时请将 `{WorkspaceId}` 替换为真实的[Workspace ID](../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

异步调用流程分两步：

1.  **创建任务获取任务 ID**：发送一个请求创建任务，该请求会返回**任务 ID（task\_id）**。
2.  **根据任务 ID 查询结果**：使用 `task_id` 轮询任务状态，直到任务完成并获得译后文件 URL 或译文文本。

<a id="步骤1-创建任务获取任务-id"></a>

<a id="uni-async-create"></a>

### 步骤1：创建任务获取任务 ID

> **说明**
>
> -   创建成功后，使用接口返回的 `task_id` 查询结果，`task_id` 有效期为 24 小时。**请勿重复创建任务**，轮询获取即可。
> -   请求参数与同步调用**完全一致**，只需在请求头额外加上 `X-DashScope-Async: enable`。

<table><tbody><tr><td><a id="uni-async-req"></a><h4>请求参数</h4><h5>请求头（Headers）</h5><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为 <code>application/json</code>。</p><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼 API Key 进行身份认证。示例值：<code>Bearer sk-xxxx</code>。</p><p><strong>X-DashScope-Async</strong><code>string</code><strong>（必选）</strong></p><p>异步处理配置参数。<strong>必须设置为</strong> <code>enable</code>。缺少此请求头将使用同步模式。</p><h5>请求体（Request Body）</h5><p>请求体字段与<a href="qwen-mt-uni-api.md#uni-sync">同步调用</a>完全一致，包括 <code>model</code>、<code>input</code>（<code>fileUrl</code>/<code>source_texts</code>、<code>source_lang</code>、<code>target_lang</code>、<code>ext</code>）等参数。</p></td><td><a id="code-block-4"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
--header 'X-DashScope-Async: enable' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
    &quot;model&quot;: &quot;qwen-mt-uni&quot;,
    &quot;input&quot;: {
        &quot;fileUrl&quot;: &quot;https://maas-infra-public.oss-cn-hangzhou.aliyuncs.com/lzhe/test/03bc3a6a-a02b-11f1-8874-00163e79676e.jpg&quot;,
        &quot;target_lang&quot;: &quot;zh&quot;
    }
}'
</code></pre></td></tr></tbody></table>

<table><tbody><tr><td><a id="uni-async-resp"></a><h4>响应参数</h4><p><strong>output</strong> <code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-7"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务 ID。查询有效期 24 小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值"></a><section><p>枚举值</p><div><ul><li><code>PENDING</code>：任务排队中</li><li><code>RUNNING</code>：任务处理中</li><li><code>SUCCEEDED</code>：任务执行完成，需结合 <code>output.Success</code> 判断业务是否成功</li><li><code>FAILED</code>：任务执行失败</li><li><code>UNKNOWN</code>：任务不存在或状态未知</li></ul></div></section></div></section><p><strong>request_id</strong> <code>string</code></p><p>请求唯一标识，可用于请求明细溯源和问题排查。</p></td><td><a id="sec-tabs-2"></a><section><a id="成功响应-2"></a><section><a id="成功响应-2-h4"></a><h4>成功响应</h4><p>请保存 <code>task_id</code>，用于查询任务状态与结果。</p><a id="code-block-5"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;5dfd1549-e956-4f26-8802-6c9e06f704c6&quot;,
        &quot;task_status&quot;: &quot;PENDING&quot;
    },
    &quot;request_id&quot;: &quot;fe9a9059-02dd-497c-a62c-8e27a0081c02&quot;
}
</code></pre></section><a id="异常响应-2"></a><section><a id="异常响应-2-h4"></a><h4>异常响应</h4><p>创建任务失败，请参见<a href="qwen-mt-uni-api.md#uni-errors">错误码</a>进行解决。</p><a id="code-block-6"></a><pre class="language-json"><code>{
    &quot;code&quot;: &quot;InvalidParameter&quot;,
    &quot;message&quot;: &quot;InvalidParameter: missing required field: input.target_lang&quot;,
    &quot;request_id&quot;: &quot;a20aa16a-2445-929f-9130-af70b4a0ade4&quot;
}
</code></pre></section></section></td></tr></tbody></table>

<a id="步骤2-根据任务-id-查询结果"></a>

<a id="uni-async-query"></a>

### 步骤2：根据任务 ID 查询结果

`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`

> **说明**
>
> -   `task_id` 有效期为 **24 小时**，若 ID 不存在或已过期，任务状态将返回 `UNKNOWN`。
> -   任务成功后返回的 `TranslatedFileUrl` 有效期为 **24 小时**，请及时下载并保存文件。
> -   此查询接口的默认 RPS 为 1。如需更高频次的查询或事件通知，请[配置异步任务回调](../more-about-models/async-task-api.md)。

<table><tbody><tr><td><h4>请求参数</h4><h5>请求头（Headers）</h5><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼 API Key 进行身份认证。示例值：<code>Bearer sk-xxxx</code>。</p><h5>URL 路径参数（Path parameters）</h5><p><strong>task_id</strong> <code>string</code> <strong>（必选）</strong></p><p>任务 ID，由创建任务接口返回。</p></td><td><a id="sec-tabs-3"></a><section><a id="查询任务结果"></a><section><a id="查询任务结果-h4"></a><h4>查询任务结果</h4><p>您需要将 <code>86ecf553-d340-4e21-xxxxxxxxx</code> 替换为真实的 <code>task_id</code>。</p><a id="code-block-7"></a><pre class="language-bash"><code>curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/86ecf553-d340-4e21-xxxxxxxxx \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><h4>响应参数</h4><div><div><p><strong>说明</strong><strong>字段返回时机</strong>：<code>task_status</code> 为 <code>PENDING</code> / <code>RUNNING</code> 时，<code>TranslatedFileUrl</code>、<code>TranslatedTexts</code>、<code>usage</code>、<code>end_time</code> 均为空，调用方需继续轮询。</p></div></div><p><strong>output</strong> <code>object</code></p><p>异步任务状态及执行结果。</p><a id="accordion-属性-8"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>异步任务的唯一标识；三种状态均返回。</p><p><strong>task_status</strong> <code>string</code></p><p>异步任务状态。<code>PENDING</code>：等待处理；<code>RUNNING</code>：处理中；<code>SUCCEEDED</code>：任务执行完成。<strong>业务失败示例中该字段仍为 <code>SUCCEEDED</code>，需结合 <code>output.Success</code> 判断业务是否成功。</strong></p><p><strong>submit_time</strong> <code>string</code></p><p>任务提交时间，格式为 <code>yyyy-MM-dd HH:mm:ss.SSS</code>。成功和失败示例均返回。</p><p><strong>scheduled_time</strong> <code>string</code></p><p>任务开始调度时间，格式为 <code>yyyy-MM-dd HH:mm:ss.SSS</code>。成功和失败示例均返回。</p><p><strong>end_time</strong> <code>string</code></p><p>任务结束时间，格式为 <code>yyyy-MM-dd HH:mm:ss.SSS</code>。成功和失败示例均返回。</p><p><strong>Success</strong> <code>boolean</code></p><p>业务执行是否成功。<code>true</code>：成功；<code>false</code>：失败。<strong>待处理示例不返回。</strong></p><p><strong>Code</strong> <code>integer</code></p><p>业务结果码。<code>200</code> 表示成功，<code>400</code> 表示请求参数错误。待处理示例不返回。</p><p><strong>Message</strong> <code>string</code></p><p>业务执行结果说明。成功示例为 <code>Success</code>；失败时返回错误详情，例如 <code>InvalidParameter: missing required field: input.target_lang</code>。</p><p><strong>RequestId</strong> <code>string</code></p><p>业务执行请求标识。成功和失败示例均返回。</p><p><strong>Data</strong> <code>object</code></p><p>翻译结果数据；<strong>仅业务成功时返回</strong>。</p><a id="accordion-属性-9"></a><section><p>属性</p><div><p><strong>FileType</strong> <code>string</code></p><p>结果类型：<code>strings</code> / <code>document</code> / <code>image</code> / <code>audio</code>。</p><p><strong>TranslatedFileUrl</strong> <code>string</code></p><p>译后文件的下载地址（带签名及有效期参数）。<strong>仅传 <code>fileUrl</code> 时返回</strong>。</p><p><strong>TranslatedTexts</strong> <code>string | array&lt;string&gt;</code></p><p>文本翻译结果。<strong>仅传 <code>source_texts</code> 时返回</strong>，形状与入参一致。</p></div></section></div></section><p><strong>usage</strong> <code>object</code></p><p>Token 用量统计。成功示例返回详细统计；失败示例返回空对象 <code>{}</code>；待处理示例不返回。字段与同步调用一致。</p><p><strong>request_id</strong> <code>string</code></p><p>本次查询请求的唯一标识；三种状态均返回。</p></td><td><a id="sec-tabs-4"></a><section><a id="处理中"></a><section><a id="处理中-h4"></a><h4>处理中</h4><a id="code-block-8"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;6e8d1dd6-9e02-9793-ad25-6e7fda5eeea0&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;df8fc25e-b9ee-4e96-9aa2-24d69681299e&quot;,
        &quot;task_status&quot;: &quot;PENDING&quot;
    }
}
</code></pre></section><a id="处理成功"></a><section><a id="处理成功-h4"></a><h4>处理成功</h4><a id="code-block-9"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;47bb236e-4ecc-90a7-ac39-9ab3435d2cc8&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;9a7ccda6-4604-4541-a2f3-f9d412c0779b&quot;,
        &quot;task_status&quot;: &quot;SUCCEEDED&quot;,
        &quot;submit_time&quot;: &quot;2026-09-15 13:35:06.883&quot;,
        &quot;scheduled_time&quot;: &quot;2026-09-15 13:35:06.931&quot;,
        &quot;end_time&quot;: &quot;2026-09-15 13:35:10.149&quot;,
        &quot;Message&quot;: &quot;Success&quot;,
        &quot;RequestId&quot;: &quot;9a7ccda6-4604-4541-a2f3-f9d412c0779b&quot;,
        &quot;Data&quot;: {
            &quot;FileType&quot;: &quot;image&quot;,
            &quot;TranslatedFileUrl&quot;: &quot;http://dashscope-a717.oss-cn-beijing.aliyuncs.com/xxx.jpg?Expires=xxx&quot;
        },
        &quot;Code&quot;: 200,
        &quot;Success&quot;: true
    },
    &quot;usage&quot;: {
        &quot;input_tokens_details&quot;: {
            &quot;document_tokens&quot;: 0,
            &quot;audio_tokens&quot;: 0,
            &quot;character_tokens&quot;: 0,
            &quot;image_tokens&quot;: 1887
        },
        &quot;total_tokens&quot;: 3774,
        &quot;output_tokens&quot;: 1887,
        &quot;input_tokens&quot;: 1887,
        &quot;output_tokens_details&quot;: {
            &quot;document_tokens&quot;: 0,
            &quot;audio_tokens&quot;: 0,
            &quot;character_tokens&quot;: 0,
            &quot;image_tokens&quot;: 1887
        }
    }
}
</code></pre></section><a id="处理失败"></a><section><a id="处理失败-h4"></a><h4>处理失败</h4><p>业务失败时 <code>task_status</code> 仍为 <code>SUCCEEDED</code>，需通过 <code>output.Success = false</code> 判断。</p><a id="code-block-10"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;&lt;查询请求id&gt;&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;&lt;task-id&gt;&quot;,
        &quot;task_status&quot;: &quot;SUCCEEDED&quot;,
        &quot;submit_time&quot;: &quot;2026-09-14 11:09:36.876&quot;,
        &quot;scheduled_time&quot;: &quot;2026-09-14 11:09:36.926&quot;,
        &quot;end_time&quot;: &quot;2026-09-14 11:09:37.050&quot;,
        &quot;Success&quot;: false,
        &quot;Code&quot;: 400,
        &quot;Message&quot;: &quot;InvalidParameter: missing required field: input.target_lang&quot;,
        &quot;RequestId&quot;: &quot;&lt;=task_id&gt;&quot;
    },
    &quot;usage&quot;: {}
}
</code></pre></section></section></td></tr></tbody></table>

<a id="支持的语种"></a>

<a id="uni-languages"></a>

## 支持的语种

若不确定源语种，可将 `source_lang` 留空以自动识别。下表列出全部受支持的翻译方向：

| 源语种（中文名） | 源语种（编码） | 可选目标语种 |
| --- | --- | --- |
| 中文（简体） | `zh` | 中文（繁体）（`zh-tw`）、英语（`en`）、日语（`ja`）、韩语（`ko`）、哈萨克语（`kk`）、马来语（`ms`）、泰语（`th`） |
| 中文（繁体） | `zh-tw` | 中文（简体）（`zh`）、英语（`en`）、日语（`ja`）、韩语（`ko`）、哈萨克语（`kk`）、马来语（`ms`）、泰语（`th`） |
| 英语 | `en` | 阿拉伯语（`ar`）、阿塞拜疆语（`az`）、孟加拉语（`bn`）、波斯尼亚语（`bs`）、捷克语（`cs`）、丹麦语（`da`）、德语（`de`）、希腊语（`el`）、西班牙语（`es`）、爱沙尼亚语（`et`）、芬兰语（`fi`）、法语（`fr`）、希伯来语（`he`）、印地语（`hi`）、匈牙利语（`hu`）、印度尼西亚语（`id`）、意大利语（`it`）、日语（`ja`）、韩语（`ko`）、立陶宛语（`lt`）、拉脱维亚语（`lv`）、马来语（`ms`）、缅甸语（`my`）、尼泊尔语（`ne`）、荷兰语（`nl`）、挪威语（`no`）、波兰语（`pl`）、葡萄牙语-巴西（`pt`）、葡萄牙语-葡萄牙（`pt-pt`）、罗马尼亚语（`ro`）、罗马尼亚语-乌尔都（`ro_ur`）、俄语（`ru`）、僧伽罗语（`si`）、斯洛伐克语（`sk`）、斯洛文尼亚语（`sl`）、塞尔维亚语（`sr`）、瑞典语（`sv`）、泰语（`th`）、菲律宾语（`tl`）、土耳其语（`tr`）、乌克兰语（`uk`）、乌尔都语（`ur`）、越南语（`vi`）、中文（简体）（`zh`）、中文（繁体）（`zh-tw`） |
| 西班牙语 | `es` | 保加利亚语（`bg`）、捷克语（`cs`）、丹麦语（`da`）、德语（`de`）、希腊语（`el`）、英语（`en`）、爱沙尼亚语（`et`）、芬兰语（`fi`）、法语（`fr`）、克罗地亚语（`hr`）、匈牙利语（`hu`）、意大利语（`it`）、立陶宛语（`lt`）、拉脱维亚语（`lv`）、荷兰语（`nl`）、挪威语（`no`）、波兰语（`pl`）、葡萄牙语-巴西（`pt`）、葡萄牙语-葡萄牙（`pt-pt`）、罗马尼亚语（`ro`）、俄语（`ru`）、斯洛伐克语（`sk`）、瑞典语（`sv`） |
| 阿拉伯语 | `ar` | 英语（`en`）、土耳其语（`tr`） |
| 土耳其语 | `tr` | 阿拉伯语（`ar`）、捷克语（`cs`）、德语（`de`）、希腊语（`el`）、英语（`en`）、匈牙利语（`hu`）、罗马尼亚语（`ro`）、斯洛伐克语（`sk`） |
| 罗马尼亚语 | `ro` | 英语（`en`）、土耳其语（`tr`） |
| 阿塞拜疆语 | `az` | 英语（`en`） |
| 孟加拉语 | `bn` | 英语（`en`） |
| 捷克语 | `cs` | 英语（`en`） |
| 德语 | `de` | 英语（`en`） |
| 希腊语 | `el` | 英语（`en`） |
| 芬兰语 | `fi` | 英语（`en`） |
| 法语 | `fr` | 英语（`en`） |
| 希伯来语 | `he` | 英语（`en`） |
| 印地语 | `hi` | 英语（`en`） |
| 匈牙利语 | `hu` | 英语（`en`） |
| 印度尼西亚语 | `id` | 英语（`en`） |
| 意大利语 | `it` | 英语（`en`） |
| 日语 | `ja` | 英语（`en`） |
| 韩语 | `ko` | 英语（`en`） |
| 马来语 | `ms` | 英语（`en`） |
| 缅甸语 | `my` | 英语（`en`） |
| 尼泊尔语 | `ne` | 英语（`en`） |
| 荷兰语 | `nl` | 英语（`en`） |
| 波兰语 | `pl` | 英语（`en`） |
| 葡萄牙语（巴西） | `pt` | 英语（`en`） |
| 俄语 | `ru` | 英语（`en`） |
| 僧伽罗语 | `si` | 英语（`en`） |
| 瑞典语 | `sv` | 英语（`en`） |
| 泰语 | `th` | 英语（`en`） |
| 菲律宾语 | `tl` | 英语（`en`） |
| 乌克兰语 | `uk` | 英语（`en`） |
| 乌尔都语 | `ur` | 英语（`en`） |
| 越南语 | `vi` | 英语（`en`） |
| 保加利亚语 | `bg` | 英语（`en`） |
| 波斯尼亚语 | `bs` | 英语（`en`） |
| 丹麦语 | `da` | 英语（`en`） |
| 爱沙尼亚语 | `et` | 英语（`en`） |
| 克罗地亚语 | `hr` | 英语（`en`） |
| 立陶宛语 | `lt` | 英语（`en`） |
| 拉脱维亚语 | `lv` | 英语（`en`） |
| 挪威语 | `no` | 英语（`en`） |
| 葡萄牙语（葡萄牙） | `pt-pt` | 英语（`en`） |
| 罗马尼亚语（乌尔都） | `ro_ur` | 英语（`en`） |
| 斯洛伐克语 | `sk` | 英语（`en`） |
| 斯洛文尼亚语 | `sl` | 英语（`en`） |
| 塞尔维亚语 | `sr` | 英语（`en`） |

<a id="计费与限流"></a>

<a id="uni-billing"></a>

## 计费与限流

-   模型免费额度和计费单价请参见[模型价格](../../model-user-guide/test-1/model-pricing.md#uni-pricing)。
-   模型限流请参见[限流](../../model-user-guide/get-started-with-models/rate-limit.md#uni-rate-limit)。
-   计费说明：按 `input_tokens` 计费。同步与异步价格一致。
-   **注意**：模型调用失败或处理错误不产生任何费用，也不消耗[新人免费额度](../../model-user-guide/test-1/new-free-quota.md)。

<a id="错误码"></a>

<a id="uni-errors"></a>

## 错误码

请参见[错误码](../preparations/error-code.md)。
