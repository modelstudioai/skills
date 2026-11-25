# Anthropic兼容-Messages

通过兼容 Anthropic 格式的 Messages API 调用模型，查看输入输出参数说明及调用示例。

通过修改以下配置，即可将原有的 Anthropic 应用迁移至阿里云百炼：

-   `api_key`：替换为[百炼 API Key](../preparations/get-api-key.md)。
-   `base_url`：替换为百炼的兼容端点地址（见下方接入信息）。
-   `model`：替换为百炼支持的模型名称（例如 `qwen3.7-plus`）。

> **重要**
>
> 阿里云百炼为华北2（北京）、新加坡、中国香港地域推出了业务空间专属域名，**能够为推理请求提供卓越的性能和更高的稳定性**，建议迁移至新域名：
>
> -   华北2（北京）地域：从 `https://dashscope.aliyuncs.com` 迁移至 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
> -   新加坡地域：从 `https://dashscope-intl.aliyuncs.com` 迁移至 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`
>
> 其中 `{WorkspaceId}` 为您的业务空间 ID，可在阿里云百炼控制台的**业务空间详情**页面查看。现有域名仍可正常使用。

<a id="sec-tabs"></a>

<a id="华北2-北京"></a>

<a id="华北2-北京-h4"></a>

#### 华北2（北京）

SDK 调用配置的 `base_url`：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic`

HTTP 请求地址：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic/v1/messages`

<a id="新加坡"></a>

<a id="新加坡-h4"></a>

#### 新加坡

SDK 调用配置的 `base_url`：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/apps/anthropic`

HTTP 请求地址：`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/apps/anthropic/v1/messages`

<a id="美国-弗吉尼亚"></a>

<a id="美国-弗吉尼亚-h4"></a>

#### 美国（弗吉尼亚）

SDK 调用配置的 `base_url`：`https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/apps/anthropic`

HTTP 请求地址：`POST https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/apps/anthropic/v1/messages`

<a id="德国-法兰克福"></a>

<a id="德国-法兰克福-h4"></a>

#### 德国（法兰克福）

SDK 调用配置的 `base_url`：`https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/apps/anthropic`

HTTP 请求地址：`POST https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/apps/anthropic/v1/messages`

<a id="日本-东京"></a>

<a id="日本-东京-h4"></a>

#### 日本（东京）

SDK 调用配置的 `base_url`：`https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/apps/anthropic`

HTTP 请求地址：`POST https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/apps/anthropic/v1/messages`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

认证方式：通过 `x-api-key` 请求头或 `Authorization: Bearer` 请求头传入[百炼 API Key](../preparations/get-api-key.md)，二者选其一即可。

<a id="与-anthropic-官方-api-的主要差异"></a>

<a id="bfr1diff0a1h2"></a>

## 与 Anthropic 官方 API 的主要差异

以下差异点汇总自本文正文，从 Anthropic 官方迁移时请重点确认：

|  |  |
| --- | --- |
| **差异项** | **说明** |
| 接入地址（Base URL） | `base_url` 需替换为百炼兼容端点（形如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic`，各地域地址见上方接入信息），其中 `{WorkspaceId}` 需替换为真实的业务空间 ID。 |
| 鉴权方式 | `api_key` 需替换为百炼 API Key；支持通过 `x-api-key` 或 `Authorization: Bearer` 请求头传入，二者选其一即可。 |
| 模型名称 | `model` 需替换为百炼支持的模型名称（例如 `qwen3.7-plus`），完整列表见下方 `model` 参数说明。 |
| temperature 取值范围 | 百炼取值范围为 \[0, 2)，与 Anthropic 官方的 \[0.0, 1.0\] 不同，迁移时请确认该参数取值。 |
| 接口范围 | 仅提供 Messages 接口（`/v1/messages`），不提供模型列表接口（`/v1/models`）；客户端的模型发现请求会返回 404，处理方式见下方常见问题。 |
| 扩展参数 | `output_config`（结构化输出与思考强度 `effort`）为百炼平台扩展参数，官方 SDK 类型定义中不包含，需在请求体中透传（见右侧“结构化输出”示例）；`thinking.budget_tokens` 即将废弃，新接入建议使用 `output_config.effort` 控制思考强度。 |

<table><tbody><tr><td><a id="ac3a4b5c6d7f2"></a><h2>请求体</h2><p><strong>model</strong> <code>string</code> <strong>（必选）</strong></p><p>模型名称，支持范围如下。</p><a id="accordion-支持的模型列表"></a><section><p>支持的模型列表</p><div><p><strong>千问Max</strong>：qwen4-max、qwen3.8-max、qwen3.8-max-0902、qwen3.7-max、qwen3.7-max-2026-05-20、qwen3.7-max-2026-06-08</p><p><strong>千问Plus</strong>：qwen3.7-plus、qwen3.7-plus-2026-05-26、qwen3.6-plus、qwen3.6-plus-2026-04-02、qwen3.5-plus、qwen3.5-plus-2026-04-20、qwen3.5-plus-2026-02-15、qwen-plus、qwen-plus-latest</p><p><strong>千问Flash</strong>：qwen3.8-flash、qwen3.7-flash、qwen3.7-flash-2026-07-15、qwen3.6-flash、qwen3.6-flash-2026-04-16、qwen3.5-flash、qwen3.5-flash-2026-02-23、qwen-flash、qwen-flash-2025-07-28</p><p><strong>千问Coder</strong>：qwen3-coder-flash</p><p><strong>千问VL</strong>：qwen3-vl-plus</p><p><strong>千问开源模型</strong>：qwen3.6-27b、qwen3.5-397b-a17b、qwen3.5-122b-a10b、qwen3.5-27b、qwen3.5-35b-a3b、qwen3.8-2.4t-a95b、qwen3.8-27b</p><strong>第三方模型</strong><p>deepseek-v4.1-flash、deepseek-v4-pro、deepseek-v4-pro-0813、deepseek-v4-flash-0731、kimi-k3.1-pro、kimi-k3、kimi-k2.7-code、kimi-k2.6、kimi-k2.5、glm-5.3、glm-5.2、glm-5.1、glm-5、MiniMax-M2.5、deepseek-v4.1-flash-1017</p></div></section><p><strong>max_tokens</strong> <code>integer</code> <strong>（必选）</strong></p><ul><li><p>qwen4-max、deepseek-v4.1-flash、deepseek-v4-pro、deepseek-v4-pro-0813、deepseek-v4-flash-0731、qwen3.8-max、qwen3.8-flash：模型回复内容和思维链内容之和的最大Token数，模型输出超过此值时生成将提前停止，<code>stop_reason</code> 为 <code>max_tokens</code>。</p><blockquote><p><code>max_tokens</code> 限制模型回复内容+思考过程的长度。开启深度思考时，<code>max_tokens</code> &gt; <code>thinking.budget_tokens</code></p></blockquote></li><li><p>glm-5.3：<code>max_tokens</code> 为模型回复内容和思维链内容之和的最大Token数，模型输出超过此值时生成将提前停止，<code>stop_reason</code> 为 <code>max_tokens</code>。glm-5.3 会忽略 <code>thinking.budget_tokens</code> 参数。</p></li><li><p>glm-5.2：不传入 <code>thinking.budget_tokens</code> 参数时，<code>max_tokens</code> 为模型回复内容和思维链内容之和的最大Token数，模型输出超过此值时生成将提前停止，<code>stop_reason</code> 为 <code>max_tokens</code>；传入 <code>thinking.budget_tokens</code> 参数时，<code>max_tokens</code> 仅为模型回复内容的最大Token数，思考部分的 Token 数由 <code>thinking.budget_tokens</code> 单独控制。</p></li><li><p>其他模型：模型回复内容的最大 Token 数。若生成内容超过此值，生成将提前停止，<code>stop_reason</code> 为 <code>max_tokens</code>。</p><blockquote><p><code>max_tokens</code> 不限制思考过程的长度。开启深度思考时，思考部分的 Token 数由 <code>thinking.budget_tokens</code> 单独控制。</p></blockquote></li></ul><p><strong>system</strong> <code>string 或 array</code> （可选）</p><p>系统提示词，用于设定模型的角色或行为。</p><p>传入字符串等价于单个 <code>type=&quot;text&quot;</code> 的内容块。当需要为系统提示词标记显式缓存断点（参见右侧&quot;显式缓存&quot;示例）时，必须传入数组形式。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>固定为 <code>text</code>。</p><p><strong>text</strong> <code>string</code> <strong>（必选）</strong></p><p>系统提示词文本。</p><p><strong>cache_control</strong> <code>object</code> （可选）</p><p>在该内容块上标记显式缓存断点（参见右侧&quot;显式缓存&quot;示例），命中后第二次及之后的请求按缓存读取计费。仅包含字段 <code>type</code>，取值固定为 <code>ephemeral</code>。</p><a id="accordion-属性-qwen4"></a><section><p>属性（Qwen4）</p><div><p>仅支持 <code>qwen4-max</code>。 Qwen4 的内容块缓存标记还支持 <code>ttl</code>，可选 <code>5m</code>、<code>1h</code>，默认为 <code>5m</code>。 详见<a href="../../model-user-guide/model-experience/text-generation-model/explicit-cache-qwen4.md">显式缓存（Qwen4）</a>。</p><p><strong>type</strong> <code>string</code> (必选)</p><p><code>ephemeral</code></p><p><strong>ttl</strong> <code>string</code> (可选)</p><p>缓存有效期，支持 <code>5m</code> 和 <code>1h</code>，默认为 <code>5m</code>。</p></div></section></div></section><p><strong>messages</strong> <code>array</code> <strong>（必选）</strong></p><a id="accordion-messages-数组元素"></a><section><p>messages 数组元素</p><div><p><strong>role</strong> <code>string</code> <strong>（必选）</strong></p><p>消息角色，可选值：<code>user</code>、<code>assistant</code>、<code>system</code>。</p><p><strong>content</strong> <code>string 或 array</code> <strong>（必选）</strong></p><p>消息内容。可以是纯文本字符串，也可以是结构化内容数组。<code>content</code> 为字符串时，等价于单个 <code>type=&quot;text&quot;</code> 的内容块。</p><a id="accordion-content-数组元素类型"></a><section><p>content 数组元素类型</p><div><a id="accordion-thinking-qwen4-max"></a><section><p>thinking (qwen4-max)</p><div><p><strong>type</strong> <code>string</code></p><p><code>thinking</code></p><p><strong>thinking</strong> <code>string</code></p><p><strong>signature</strong> <code>string</code></p><p>思考摘要与签名密文。将完整思考块原样回传到后续请求。</p></div></section><strong>文本信息</strong><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>固定为 <code>text</code>。</p><p><strong>text</strong> <code>string</code> <strong>（必选）</strong></p><p>文本内容。</p><p><strong>cache_control</strong> <code>object</code> （可选）</p><p>在该文本块上标记显式缓存断点（参见右侧&quot;显式缓存&quot;示例）。仅包含字段 <code>type</code>，取值固定为 <code>ephemeral</code>。</p><a id="accordion-属性-qwen4-2"></a><section><p>属性（Qwen4）</p><div><p>仅支持 <code>qwen4-max</code>。 Qwen4 的内容块缓存标记还支持 <code>ttl</code>，可选 <code>5m</code>、<code>1h</code>，默认为 <code>5m</code>。 详见<a href="../../model-user-guide/model-experience/text-generation-model/explicit-cache-qwen4.md">显式缓存（Qwen4）</a>。</p><p><strong>type</strong> <code>string</code> (必选)</p><p><code>ephemeral</code></p><p><strong>ttl</strong> <code>string</code> (可选)</p><p>缓存有效期，支持 <code>5m</code> 和 <code>1h</code>，默认为 <code>5m</code>。</p></div></section></div></section><p><strong>图片信息</strong>（需使用视觉模型）</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>固定为 <code>image</code>。</p><p><strong>source</strong> <code>object</code> <strong>（必选）</strong></p><p>图片数据来源。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>取值：<code>url</code>（公网图片地址）、<code>base64</code>（Base64 编码）。</p><p><strong>url</strong> <code>string</code></p><p>图片的公网地址。当 <code>type</code> 为 <code>url</code> 时必填。</p><p><strong>media_type</strong> <code>string</code></p><p>图片的 MIME 类型，如 <code>image/jpeg</code>。当 <code>type</code> 为 <code>base64</code> 时必填。</p><p><strong>data</strong> <code>string</code></p><p>Base64 编码的图片数据。当 <code>type</code> 为 <code>base64</code> 时必填。</p></div></section></div></section><p><strong>视频信息</strong>（需使用视觉模型）</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>固定为 <code>video</code>。</p><p><strong>source</strong> <code>object</code> <strong>（必选）</strong></p><p>视频数据来源。</p><a id="accordion-属性-6"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>取值：<code>url</code>（公网视频地址）、<code>base64</code>（Base64 编码）。</p><p><strong>url</strong> <code>string</code></p><p>视频的公网地址。当 <code>type</code> 为 <code>url</code> 时必填。</p><p><strong>media_type</strong> <code>string</code></p><p>视频的 MIME 类型，如 <code>video/mp4</code>。当 <code>type</code> 为 <code>base64</code> 时必填。</p><p><strong>data</strong> <code>string</code></p><p>Base64 编码的视频数据。当 <code>type</code> 为 <code>base64</code> 时必填。</p></div></section></div></section><strong>PDF 文档信息</strong><a id="accordion-属性-7"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>固定为 <code>document</code>。</p><p><strong>source</strong> <code>object</code> <strong>（必选）</strong></p><p>PDF 文档的数据来源，包含以下字段：</p><ul><li><code>type</code> (<code>string</code>): 必填，取值为 <code>url</code> 或 <code>base64</code>。</li><li><code>url</code> (<code>string</code>): 当 <code>source.type</code> 为 <code>url</code> 时必填，指定 PDF 文件 URL。</li><li><code>media_type</code> (<code>string</code>): 当 <code>source.type</code> 为 <code>base64</code> 时必填，设置为 <code>application/pdf</code>。</li><li><code>data</code> (<code>string</code>): 当 <code>source.type</code> 为 <code>base64</code> 时必填，传入不含 Data URI 前缀的 Base64 编码 PDF 数据。</li></ul></div></section><p>PDF 理解的使用说明见 <a href="../../model-user-guide/model-experience/text-generation-model/tool-calls/pdf-understanding.md">PDF理解</a>。</p><p><strong>工具调用信息</strong>（assistant 角色，模型返回的工具调用指令）</p><a id="accordion-属性-8"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>固定为 <code>tool_use</code>。</p><p><strong>id</strong> <code>string</code> <strong>（必选）</strong></p><p>工具调用的唯一标识，用于在后续 <code>tool_result</code> 中关联结果。</p><p><strong>name</strong> <code>string</code> <strong>（必选）</strong></p><p>被调用的工具名称。</p><p><strong>input</strong> <code>object</code> <strong>（必选）</strong></p><p>工具调用的入参，结构由 <code>tools</code> 中对应工具的 <code>input_schema</code> 决定。</p><p><strong>cache_control</strong> <code>object</code> （可选）</p><p>在该块上标记显式缓存断点（参见右侧&quot;显式缓存&quot;示例）。仅包含字段 <code>type</code>，取值固定为 <code>ephemeral</code>。工具调用内容本身会参与缓存前缀。</p><a id="accordion-属性-qwen4-3"></a><section><p>属性（Qwen4）</p><div><p>仅支持 <code>qwen4-max</code>。 Qwen4 的内容块缓存标记还支持 <code>ttl</code>，可选 <code>5m</code>、<code>1h</code>，默认为 <code>5m</code>。 详见<a href="../../model-user-guide/model-experience/text-generation-model/explicit-cache-qwen4.md">显式缓存（Qwen4）</a>。</p><p><strong>type</strong> <code>string</code> (必选)</p><p><code>ephemeral</code></p><p><strong>ttl</strong> <code>string</code> (可选)</p><p>缓存有效期，支持 <code>5m</code> 和 <code>1h</code>，默认为 <code>5m</code>。</p></div></section></div></section><p><strong>工具结果信息</strong>（user 角色，工具执行结果回传给模型）</p><a id="accordion-属性-9"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>固定为 <code>tool_result</code>。</p><p><strong>tool_use_id</strong> <code>string</code> <strong>（必选）</strong></p><p>对应 <code>tool_use</code> 信息中的 <code>id</code>。</p><p><strong>content</strong> <code>string</code> <strong>（必选）</strong></p><p>工具执行返回的内容。</p><p><strong>cache_control</strong> <code>object</code> （可选）</p><p>在该工具结果块上标记显式缓存断点（参见右侧&quot;显式缓存&quot;示例）。仅包含字段 <code>type</code>，取值固定为 <code>ephemeral</code>。</p><a id="accordion-属性-qwen4-4"></a><section><p>属性（Qwen4）</p><div><p>仅支持 <code>qwen4-max</code>。 Qwen4 的内容块缓存标记还支持 <code>ttl</code>，可选 <code>5m</code>、<code>1h</code>，默认为 <code>5m</code>。 详见<a href="../../model-user-guide/model-experience/text-generation-model/explicit-cache-qwen4.md">显式缓存（Qwen4）</a>。</p><p><strong>type</strong> <code>string</code> (必选)</p><p><code>ephemeral</code></p><p><strong>ttl</strong> <code>string</code> (可选)</p><p>缓存有效期，支持 <code>5m</code> 和 <code>1h</code>，默认为 <code>5m</code>。</p></div></section></div></section></div></section></div></section><p><strong>cache_control</strong> <code>object</code> (可选)</p><p>仅支持 <code>qwen4-max</code>。 在请求顶层开启自动缓存，也可在内容块上设置手动断点。<code>type</code> 固定为 <code>ephemeral</code>。 Python SDK 通过 <code>extra_body</code> 传入顶层非标准参数；Node.js SDK 和 curl 直接传入。 详见<a href="../../model-user-guide/model-experience/text-generation-model/explicit-cache-qwen4.md">显式缓存（Qwen4）</a>。</p><a id="accordion-属性-10"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> (必选)</p><p><code>ephemeral</code></p><p><strong>ttl</strong> <code>string</code> (可选)</p><p>缓存有效期，支持 <code>5m</code> 和 <code>1h</code>，默认为 <code>5m</code>。</p></div></section><p><strong>stream</strong> <code>boolean</code> （可选）</p><p>是否启用流式输出，默认为 <code>false</code>。</p><p><strong>temperature</strong> <code>number</code> （可选）</p><p>控制生成文本的多样性，取值范围 [0, 2)。值越大，生成结果越随机。</p><div><div><p><strong>说明</strong>该范围与 Anthropic 官方的 [0.0, 1.0] 不同，从 Anthropic 迁移时请确认该参数取值。</p></div></div><p><strong>top_p</strong> <code>number</code> （可选）</p><p>核采样的概率阈值，控制生成文本的多样性。</p><blockquote><p><code>temperature</code> 与 <code>top_p</code> 均可控制生成文本的多样性，建议只设置其中一个值。更多说明请参见<a href="../../model-user-guide/model-experience/text-generation-model/text-generation.md">概述</a>。</p></blockquote><p><strong>top_k</strong> <code>integer</code> （可选）</p><p>生成过程中采样候选集的大小。</p><p><strong>stop_sequences</strong> <code>array</code> （可选）</p><p>指定停止生成的文本序列。模型生成到该序列前会停止输出，且不包含该序列本身。</p><div><div><p><strong>说明</strong>命中后，响应的 <code>stop_reason</code> 为 <code>stop_sequence</code>，并在响应的 <code>stop_sequence</code> 字段中回填命中的序列。</p></div></div><p><strong>thinking</strong> <code>object</code> （可选）</p><p>深度思考配置。开启后，模型会在生成回复前先进行推理，以提升回答准确度。开启后，响应会包含 <code>thinking</code> 类型的内容块。</p><p>未传入该参数时，是否进行思考由模型默认行为决定：qwen4-max、qwen3.8-max、qwen3.8-flash、deepseek-v4 系列、glm 系列、kimi-k3.1-pro 默认开启思考；kimi-k2.6、kimi-k2.5 默认关闭思考；kimi-k2.7-code、MiniMax-M2.5 仅支持思考模式（无法关闭）。各模型对思考模式的支持情况与默认开关，请参见<a href="../../model-user-guide/model-experience/text-generation-model/deep-thinking.md">深度思考</a>。</p><a id="accordion-属性-11"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>可选值：<code>enabled</code>（开启思考模式）、<code>disabled</code>（关闭思考模式）。</p><p><strong>budget_tokens</strong> <code>integer</code> （可选，<strong>即将废弃</strong>）</p><blockquote><p>该参数即将废弃，并将在后续模型中逐步停止支持，新接入建议使用 <code>effort</code>控制模型的思考强度。</p></blockquote><p>思考过程可使用的最大 Token 数，与 <code>max_tokens</code> 的关系因模型而异，详见 <code>max_tokens</code> 参数说明。预算越大，在复杂问题上的分析越充分。当 <code>type</code> 为 <code>enabled</code> 时生效。</p><p><strong>display</strong> <code>string</code> （可选）</p><p><code>qwen4-max</code>: <code>&quot;summarized&quot;</code>. <a href="../../model-user-guide/model-experience/text-generation-model/cot-summary.md#anthropic">思维链摘要与加密</a>.</p><p>默认返回完整思维链。开启本功能后，原始思维链不再以明文返回，改为返回摘要与完整密文。摘要用于展示，密文用于恢复历史思考。</p></div></section><p><strong>tools</strong> <code>array</code> （可选）</p><p>工具定义数组，用于 Function Call 场景。</p><a id="accordion-tools-数组元素"></a><section><p>tools 数组元素</p><div><p><strong>name</strong> <code>string</code> <strong>（必选）</strong></p><p>工具名称。</p><p><strong>description</strong> <code>string</code> （可选）</p><p>工具的功能描述。</p><p><strong>input_schema</strong> <code>object</code> <strong>（必选）</strong></p><p>工具输入参数的 JSON Schema 定义。</p></div></section><p>除上述自定义工具外，<code>tools</code> 还支持百炼服务端联网搜索工具，在 <code>tools</code> 中声明即可启用，无需客户端执行检索。</p><a id="accordion-联网搜索工具"></a><section><p>联网搜索工具</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>工具类型，取值为 <code>web_search_20250305</code> 等带日期后缀的形式。日期后缀无需固定，与客户端发送的值保持一致即可。</p><p><strong>name</strong> <code>string</code> <strong>（必选）</strong></p><p>固定为 <code>web_search</code>。</p><p><strong>max_uses</strong> <code>integer</code> （可选）</p><p>单次请求最多检索次数。</p></div></section><blockquote><p>使用 Anthropic SDK 或 HTTP 直接调用时，<strong>必须</strong>在 <code>system</code> 中传入客户端标识 <code>x-anthropic-billing-header: cc_entrypoint=cli;</code>，否则联网搜索不生效。面向 Claude Code 等 Anthropic 官方客户端时无需额外配置。详见 <a href="../../model-user-guide/model-experience/text-generation-model/tool-calls/web-search.md">联网搜索</a>。</p></blockquote><blockquote><p>支持以下模型：<code>qwen4-max</code>; Qwen3.8 Max、Flash 与开源系列（不含 Omni）；Qwen3.7 Max、Plus、Flash 系列；Qwen3.6-Plus、Qwen3.6-Flash 系列；Qwen3.5-Plus、Qwen3.5-Flash 系列；deepseek-v4-pro、deepseek-v4-pro-0813、deepseek-v4-flash-0731、deepseek-v4.1-flash-1017；glm-5.2；kimi-k3；kimi-k3.1-pro。联网搜索的计费与 agent 策略相同，参见 <a href="../../model-user-guide/model-experience/text-generation-model/tool-calls/web-search.md#92ce83df3a599">计费说明</a>。</p></blockquote><p><code>kimi-k3.1-pro</code>（阿里云百炼部署）在北京、新加坡、美国（弗吉尼亚）、德国（法兰克福）、日本（东京）和中国香港均支持 <code>web_search</code> 和 <code>web_fetch</code>。</p><p><code>deepseek-v4.1-flash-1017</code> 还支持网页抓取工具 <code>web_fetch</code>。Anthropic 兼容的请求要求及示例请参见<a href="./web-extractor">网页抓取</a>。</p><p><code>qwen4-max</code>: <code>web_search</code>, <code>web_fetch</code>.</p><p>在 <code>tools</code> 参数中添加 Anthropic 服务端的网页抓取工具（<code>name</code> 为 <code>web_fetch</code>）即可启用网页抓取，并且必须同时添加联网搜索工具（<code>name</code> 为 <code>web_search</code>）。请求地址为 <code>https://{WorkspaceId}.{region}.maas.aliyuncs.com/apps/anthropic</code>。</p><a id="accordion-web-fetch-qwen4-max"></a><section><p>web_fetch (qwen4-max)</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>工具类型，取值为 <code>web_fetch_20250910</code> 等带日期后缀的形式。日期后缀无需固定，与客户端发送的值保持一致即可。</p><p><strong>name</strong> <code>string</code> <strong>（必选）</strong></p><p>固定为 <code>web_fetch</code>。</p><p><strong>max_uses</strong> <code>integer</code></p><p>单次请求最多抓取次数。</p></div></section><p><strong>tool_choice</strong> <code>object</code> （可选）</p><p>工具选择策略。支持以下值：</p><ul><li><code>{&quot;type&quot;: &quot;auto&quot;}</code>：模型自行决定是否调用工具（默认）。</li><li><code>{&quot;type&quot;: &quot;any&quot;}</code>：强制模型调用任意一个工具。</li><li><code>{&quot;type&quot;: &quot;none&quot;}</code>：禁止模型调用工具。</li><li><code>{&quot;type&quot;: &quot;tool&quot;, &quot;name&quot;: &quot;tool_name&quot;}</code>：强制模型调用指定工具。</li></ul><p><strong>output_config</strong> <code>object</code> （可选）</p><p>输出参数设置。</p><a id="accordion-属性-12"></a><section><p>属性</p><div><p><strong>effort</strong> <code>string</code> （可选）</p><p><strong><code>qwen4-max</code></strong></p><p>可选值：<code>low</code>、<code>high</code>（默认）、<code>xhigh</code>。</p><p><code>medium</code> 映射为 <code>high</code>，<code>max</code> 映射为 <code>xhigh</code>。</p><p>控制模型的推理力度。</p><p>kimi-k3.1-pro（阿里云百炼部署）默认值为 <code>max</code>，支持 <code>max</code>（深度推理）、<code>high</code>（增强推理）、<code>medium</code>（中度推理）和 <code>low</code>（轻度推理）。</p><ul><li><p>glm-5.3（默认值为 <code>max</code>）：</p><p>可选值：</p><ul><li><code>low</code>：低力度推理</li><li><code>high</code>：高力度推理</li><li><code>max</code>：最大力度推理</li></ul><p>传入其它取值会返回错误。</p></li><li><p>glm-5.2、deepseek-v4-pro（阿里云直供）（默认值为 <code>max</code>）：</p><p>可选值：</p><ul><li><code>high</code>：高力度推理</li><li><code>max</code>：最大力度推理</li></ul><p><code>low</code>和<code>medium</code>映射为<code>high</code>，<code>xhigh</code>映射为<code>max</code>。</p></li><li><p>qwen3.8-max/qwen3.8-flash（默认值为 <code>xhigh</code>）：</p><p>可选值：</p><ul><li><code>xhigh</code>：高力度推理</li><li><code>medium</code>：中力度推理</li><li><code>low</code>：低力度推理</li></ul><p><code>max</code> 、<code>high</code>映射为 <code>xhigh</code>。</p></li></ul><p><strong>format</strong> <code>object</code> （可选）</p><p>结构化输出配置。开启后，模型将输出 JSON 字符串。不同模型的支持力度不同：</p><ul><li><strong>严格结构化输出</strong>：适用于 qwen3.8 系列、qwen3.7 系列、deepseek 系列（不含 <code>deepseek-v4-flash-0731</code>、<code>deepseek-v4-pro-0813</code>）、glm 系列模型。模型严格按照传入的 JSON Schema 进行强约束输出，确保字段类型与层级完全一致。</li><li><strong>普通结构化输出</strong>：适用于上述以外的其他模型。Schema 的具体字段约束默认不生效，API 会自动将其转换为普通 JSON 模式（仅保证输出为合法的 JSON 字符串）。触发普通 JSON 模式时，请求必须同时满足以下两点约束：1、显式传入 <code>output_config</code> 参数；2、<code>system</code> 或 <code>messages</code> 的内容中必须包含不区分大小写的 &quot;JSON&quot; 关键词。若提示词中未包含 &quot;JSON&quot; 关键词，API将抛出异常：<code>'messages' must contain the word 'json' in some form</code>。</li></ul><a id="accordion-属性-13"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>取值固定为 <code>json_schema</code>。</p><p><strong>schema</strong> <code>object</code> <strong>（必选）</strong></p><p>JSON Schema 对象，遵循标准 JSON Schema 规范。需包含 <code>type</code>（数据类型）、<code>properties</code>（字段定义）、<code>required</code>（必填字段名数组）、<code>additionalProperties</code>（必须设为 <code>false</code>）等字段。</p></div></section></div></section><a id="accordion-属性-qwen4-5"></a><section><p>属性（Qwen4）</p><div><p>详见<a href="../../model-user-guide/model-experience/text-generation-model/explicit-cache-qwen4.md">显式缓存（Qwen4）</a>。</p><p><strong>input_tokens</strong> <code>integer</code></p><p>仅统计未读取也未创建缓存的输入 Token 数；全部输入为本字段与缓存读取、创建 Token 数之和。</p><p><strong>output_tokens</strong> <code>integer</code></p><p>输出 Token 数量。</p><p><strong>cache_creation_input_tokens</strong> <code>integer</code></p><p>缓存创建消耗的输入 Token 数量。</p><p><strong>cache_read_input_tokens</strong> <code>integer</code></p><p>缓存读取消耗的输入 Token 数量。</p><p><strong>server_tool_use</strong> <code>object</code> （可选）</p><p>服务端工具用量统计。仅在请求中使用了服务端工具（如联网搜索）时返回。</p><a id="accordion-属性-14"></a><section><p>属性</p><div><p><strong>web_search_requests</strong> <code>integer</code></p><p>联网搜索的检索次数。</p><p><strong>web_fetch_requests</strong> <code>integer</code></p><p>网页抓取次数。</p></div></section><p><strong>cache_creation</strong> <code>object</code></p><p>按 TTL 统计的缓存创建详情。两种 TTL 的 Token 数之和等于本次创建缓存的 Token 数。</p><a id="accordion-属性-15"></a><section><p>属性</p><div><p><strong>ephemeral_5m_input_tokens</strong> <code>integer</code></p><p>5 分钟缓存创建的 Token 数。</p><p><strong>ephemeral_1h_input_tokens</strong> <code>integer</code></p><p>1 小时缓存创建的 Token 数。</p></div></section><p><strong>prompt_tokens_details</strong> <code>object</code></p><p>缓存读取详情。<code>cached_tokens</code> 与 <code>cache_read_input_tokens</code> 相同，统计时不要重复相加。</p><a id="accordion-属性-16"></a><section><p>属性</p><div><p><strong>cached_tokens</strong> <code>integer</code></p><p>缓存读取的输入 Token 数。</p></div></section></div></section></td><td><a id="anthropic-messages-request-example"></a><div><a id="sec-tabs-2"></a><section><a id="基础调用"></a><section><a id="基础调用-h4"></a><h4>基础调用</h4><a id="fig-code-group"></a><div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>import anthropic
import os

client = anthropic.Anthropic(
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    base_url=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic&quot;,
)

message = client.messages.create(
    model=&quot;qwen4-max&quot;,
    max_tokens=1024,
    system=&quot;You are a helpful assistant&quot;,
    messages=[
        {
            &quot;role&quot;: &quot;user&quot;,
            &quot;content&quot;: &quot;你是谁？&quot;
        }
    ],
    thinking={&quot;type&quot;: &quot;disabled&quot;},
)

print(message.content[0].text)
</code></pre></div><a id="fig-code-group-typescript-tab"></a>TypeScript<div><a id="code-code-group-typescript"></a><pre class="language-typescript"><code>import Anthropic from &quot;@anthropic-ai/sdk&quot;;

const anthropic = new Anthropic({
  apiKey: process.env.DASHSCOPE_API_KEY,
  baseURL: &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic&quot;,
});

async function main() {
  const message = await anthropic.messages.create({
    model: &quot;qwen4-max&quot;,
    max_tokens: 1024,
    system: &quot;You are a helpful assistant&quot;,
    messages: [{
      role: &quot;user&quot;,
      content: &quot;你是谁？&quot;
    }],
    thinking: { type: &quot;disabled&quot; },
  });

  console.log(message.content[0].text);
}

main().catch(console.error);
</code></pre></div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl -X POST &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic/v1/messages&quot; \
  -H &quot;Content-Type: application/json&quot; \
  -H &quot;x-api-key: $DASHSCOPE_API_KEY&quot; \
  -d '{
    &quot;model&quot;: &quot;qwen4-max&quot;,
    &quot;max_tokens&quot;: 1024,
    &quot;system&quot;: &quot;You are a helpful assistant&quot;,
    &quot;messages&quot;: [
        {
            &quot;role&quot;: &quot;user&quot;,
            &quot;content&quot;: &quot;你是谁？&quot;
        }
    ],
    &quot;thinking&quot;: {&quot;type&quot;: &quot;disabled&quot;}
}'
</code></pre></div></div></section><a id="流式输出"></a><section><a id="流式输出-h4"></a><h4>流式输出</h4><a id="fig-code-group-2"></a><div><a id="fig-code-group-2-python-tab"></a>Python<div><a id="code-code-group-2-python"></a><pre class="language-python"><code>import anthropic
import os

client = anthropic.Anthropic(
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    base_url=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic&quot;,
)

stream = client.messages.create(
    model=&quot;qwen4-max&quot;,
    max_tokens=1024,
    stream=True,
    messages=[
        {
            &quot;role&quot;: &quot;user&quot;,
            &quot;content&quot;: &quot;请简单介绍一下人工智能。&quot;
        }
    ],
    thinking={&quot;type&quot;: &quot;disabled&quot;},
)

for chunk in stream:
    if chunk.type == &quot;content_block_delta&quot;:
        if hasattr(chunk.delta, 'text'):
            print(chunk.delta.text, end=&quot;&quot;, flush=True)
</code></pre></div><a id="fig-code-group-2-typescript-tab"></a>TypeScript<div><a id="code-code-group-2-typescript"></a><pre class="language-typescript"><code>import Anthropic from &quot;@anthropic-ai/sdk&quot;;

async function main() {
  const anthropic = new Anthropic({
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic&quot;,
  });

  const stream = await anthropic.messages.create({
    model: &quot;qwen4-max&quot;,
    max_tokens: 1024,
    stream: true,
    messages: [{
      role: &quot;user&quot;,
      content: &quot;请简单介绍一下人工智能。&quot;
    }],
    thinking: { type: &quot;disabled&quot; },
  });

  for await (const chunk of stream) {
    if (chunk.type === &quot;content_block_delta&quot; &amp;&amp; 'text' in chunk.delta) {
      process.stdout.write(chunk.delta.text);
    }
  }
}

main().catch(console.error);
</code></pre></div><a id="fig-code-group-2-curl-tab"></a>curl<div><a id="code-code-group-2-curl"></a><pre class="language-bash"><code>curl -X POST &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic/v1/messages&quot; \
  -H &quot;Content-Type: application/json&quot; \
  -H &quot;x-api-key: $DASHSCOPE_API_KEY&quot; \
  --no-buffer \
  -d '{
    &quot;model&quot;: &quot;qwen4-max&quot;,
    &quot;max_tokens&quot;: 1024,
    &quot;stream&quot;: true,
    &quot;messages&quot;: [
        {
            &quot;role&quot;: &quot;user&quot;,
            &quot;content&quot;: &quot;请简单介绍一下人工智能。&quot;
        }
    ],
    &quot;thinking&quot;: {&quot;type&quot;: &quot;disabled&quot;}
}'
</code></pre></div></div></section><a id="深度思考"></a><section><a id="深度思考-h4"></a><h4>深度思考</h4><a id="fig-code-group-3"></a><div><a id="fig-code-group-3-python-tab"></a>Python<div><a id="code-code-group-3-python"></a><pre class="language-python"><code>import anthropic
import os

client = anthropic.Anthropic(
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    base_url=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic&quot;,
)

stream = client.messages.create(
    model=&quot;qwen4-max&quot;,
    max_tokens=2048,
    stream=True,
    thinking={
        &quot;type&quot;: &quot;enabled&quot;,
        &quot;budget_tokens&quot;: 1024
    },
    messages=[
        {
            &quot;role&quot;: &quot;user&quot;,
            &quot;content&quot;: &quot;分析一下量子计算的发展前景。&quot;
        }
    ]
)

for chunk in stream:
    if chunk.type == &quot;content_block_delta&quot;:
        if hasattr(chunk.delta, 'thinking'):
            print(chunk.delta.thinking, end=&quot;&quot;, flush=True)
        elif hasattr(chunk.delta, 'text'):
            print(chunk.delta.text, end=&quot;&quot;, flush=True)
</code></pre></div><a id="fig-code-group-3-typescript-tab"></a>TypeScript<div><a id="code-code-group-3-typescript"></a><pre class="language-typescript"><code>import Anthropic from &quot;@anthropic-ai/sdk&quot;;

async function main() {
  const anthropic = new Anthropic({
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic&quot;,
  });

  const stream = await anthropic.messages.create({
    model: &quot;qwen4-max&quot;,
    max_tokens: 2048,
    stream: true,
    thinking: { type: &quot;enabled&quot;, budget_tokens: 1024 },
    messages: [{
      role: &quot;user&quot;,
      content: &quot;分析一下量子计算的发展前景。&quot;
    }]
  });

  for await (const chunk of stream) {
    if (chunk.type === &quot;content_block_delta&quot;) {
      if ('thinking' in chunk.delta) {
        process.stdout.write(chunk.delta.thinking);
      } else if ('text' in chunk.delta) {
        process.stdout.write(chunk.delta.text);
      }
    }
  }
}

main().catch(console.error);
</code></pre></div><a id="fig-code-group-3-curl-tab"></a>curl<div><a id="code-code-group-3-curl"></a><pre class="language-bash"><code>curl -X POST &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic/v1/messages&quot; \
  -H &quot;Content-Type: application/json&quot; \
  -H &quot;x-api-key: $DASHSCOPE_API_KEY&quot; \
  -d '{
    &quot;model&quot;: &quot;qwen4-max&quot;,
    &quot;max_tokens&quot;: 2048,
    &quot;stream&quot;: true,
    &quot;thinking&quot;: {
        &quot;type&quot;: &quot;enabled&quot;,
        &quot;budget_tokens&quot;: 1024
    },
    &quot;messages&quot;: [
        {
            &quot;role&quot;: &quot;user&quot;,
            &quot;content&quot;: &quot;分析一下量子计算的发展前景。&quot;
        }
    ]
}'
</code></pre></div></div></section><a id="图片理解"></a><section><a id="图片理解-h4"></a><h4>图片理解</h4><a id="fig-code-group-4"></a><div><a id="fig-code-group-4-python-tab"></a>Python<div><a id="code-code-group-4-python"></a><pre class="language-python"><code>import anthropic
import os

client = anthropic.Anthropic(
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    base_url=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic&quot;,
)

stream = client.messages.create(
    model=&quot;qwen4-max&quot;,
    max_tokens=1024,
    stream=True,
    messages=[
        {
            &quot;role&quot;: &quot;user&quot;,
            &quot;content&quot;: [
                {
                    &quot;type&quot;: &quot;image&quot;,
                    &quot;source&quot;: {
                        &quot;type&quot;: &quot;url&quot;,
                        &quot;url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250414/mqqmiy/animal_01.jpg&quot;,
                    },
                },
                {
                    &quot;type&quot;: &quot;text&quot;,
                    &quot;text&quot;: &quot;描述这张图片的内容。&quot;
                },
            ],
        }
    ],
    thinking={&quot;type&quot;: &quot;disabled&quot;},
)

for chunk in stream:
    if chunk.type == &quot;content_block_delta&quot;:
        if hasattr(chunk.delta, 'text'):
            print(chunk.delta.text, end=&quot;&quot;, flush=True)
</code></pre></div><a id="fig-code-group-4-typescript-tab"></a>TypeScript<div><a id="code-code-group-4-typescript"></a><pre class="language-typescript"><code>import Anthropic from &quot;@anthropic-ai/sdk&quot;;

async function main() {
  const anthropic = new Anthropic({
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic&quot;,
  });

  const stream = await anthropic.messages.create({
    model: &quot;qwen4-max&quot;,
    max_tokens: 1024,
    stream: true,
    messages: [{
      role: &quot;user&quot;,
      content: [
        {
          type: &quot;image&quot;,
          source: {
            type: &quot;url&quot;,
            url: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250414/mqqmiy/animal_01.jpg&quot;,
          },
        },
        { type: &quot;text&quot;, text: &quot;描述这张图片的内容。&quot; },
      ],
    }],
    thinking: { type: &quot;disabled&quot; },
  });

  for await (const chunk of stream) {
    if (chunk.type === &quot;content_block_delta&quot; &amp;&amp; 'text' in chunk.delta) {
      process.stdout.write(chunk.delta.text);
    }
  }
}

main().catch(console.error);
</code></pre></div><a id="fig-code-group-4-curl-tab"></a>curl<div><a id="code-code-group-4-curl"></a><pre class="language-bash"><code>curl -X POST &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic/v1/messages&quot; \
  -H &quot;Content-Type: application/json&quot; \
  -H &quot;x-api-key: $DASHSCOPE_API_KEY&quot; \
  -d '{
    &quot;model&quot;: &quot;qwen4-max&quot;,
    &quot;max_tokens&quot;: 1024,
    &quot;stream&quot;: true,
    &quot;messages&quot;: [
        {
            &quot;role&quot;: &quot;user&quot;,
            &quot;content&quot;: [
                {
                    &quot;type&quot;: &quot;image&quot;,
                    &quot;source&quot;: {
                        &quot;type&quot;: &quot;url&quot;,
                        &quot;url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250414/mqqmiy/animal_01.jpg&quot;
                    }
                },
                {
                    &quot;type&quot;: &quot;text&quot;,
                    &quot;text&quot;: &quot;描述这张图片的内容。&quot;
                }
            ]
        }
    ],
    &quot;thinking&quot;: {&quot;type&quot;: &quot;disabled&quot;}
}'
</code></pre></div></div></section><a id="视频理解"></a><section><a id="视频理解-h4"></a><h4>视频理解</h4><a id="fig-code-group-5"></a><div><a id="fig-code-group-5-python-tab"></a>Python<div><a id="code-code-group-5-python"></a><pre class="language-python"><code>import anthropic
import os

client = anthropic.Anthropic(
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    base_url=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic&quot;,
)

stream = client.messages.create(
    model=&quot;qwen4-max&quot;,
    max_tokens=1024,
    stream=True,
    messages=[
        {
            &quot;role&quot;: &quot;user&quot;,
            &quot;content&quot;: [
                {
                    &quot;type&quot;: &quot;video&quot;,
                    &quot;source&quot;: {
                        &quot;type&quot;: &quot;url&quot;,
                        &quot;url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251208/zpupby/3e81ef38-98f0-4d55-bbb6-259334ca18d0.mp4&quot;,
                    },
                },
                {
                    &quot;type&quot;: &quot;text&quot;,
                    &quot;text&quot;: &quot;描述这段视频的内容。&quot;
                },
            ],
        }
    ],
    thinking={&quot;type&quot;: &quot;disabled&quot;},
)

for chunk in stream:
    if chunk.type == &quot;content_block_delta&quot;:
        if hasattr(chunk.delta, 'text'):
            print(chunk.delta.text, end=&quot;&quot;, flush=True)
</code></pre></div><a id="fig-code-group-5-typescript-tab"></a>TypeScript<div><a id="code-code-group-5-typescript"></a><pre class="language-typescript"><code>import Anthropic from &quot;@anthropic-ai/sdk&quot;;

async function main() {
  const anthropic = new Anthropic({
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic&quot;,
  });

  const stream = await anthropic.messages.create({
    model: &quot;qwen4-max&quot;,
    max_tokens: 1024,
    stream: true,
    messages: [{
      role: &quot;user&quot;,
      content: [
        {
          type: &quot;video&quot;,
          source: {
            type: &quot;url&quot;,
            url: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251208/zpupby/3e81ef38-98f0-4d55-bbb6-259334ca18d0.mp4&quot;,
          },
        },
        { type: &quot;text&quot;, text: &quot;描述这段视频的内容。&quot; },
      ],
    }],
    thinking: { type: &quot;disabled&quot; },
  });

  for await (const chunk of stream) {
    if (chunk.type === &quot;content_block_delta&quot; &amp;&amp; 'text' in chunk.delta) {
      process.stdout.write(chunk.delta.text);
    }
  }
}

main().catch(console.error);
</code></pre></div><a id="fig-code-group-5-curl-tab"></a>curl<div><a id="code-code-group-5-curl"></a><pre class="language-bash"><code>curl -X POST &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic/v1/messages&quot; \
  -H &quot;Content-Type: application/json&quot; \
  -H &quot;x-api-key: $DASHSCOPE_API_KEY&quot; \
  -d '{
    &quot;model&quot;: &quot;qwen4-max&quot;,
    &quot;max_tokens&quot;: 1024,
    &quot;stream&quot;: true,
    &quot;messages&quot;: [
        {
            &quot;role&quot;: &quot;user&quot;,
            &quot;content&quot;: [
                {
                    &quot;type&quot;: &quot;video&quot;,
                    &quot;source&quot;: {
                        &quot;type&quot;: &quot;url&quot;,
                        &quot;url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251208/zpupby/3e81ef38-98f0-4d55-bbb6-259334ca18d0.mp4&quot;
                    }
                },
                {
                    &quot;type&quot;: &quot;text&quot;,
                    &quot;text&quot;: &quot;描述这段视频的内容。&quot;
                }
            ]
        }
    ],
    &quot;thinking&quot;: {&quot;type&quot;: &quot;disabled&quot;}
}'
</code></pre></div></div></section><a id="function-call"></a><section><a id="function-call-h4"></a><h4>Function Call</h4><a id="fig-code-group-6"></a><div><a id="fig-code-group-6-python-tab"></a>Python<div><a id="code-code-group-6-python"></a><pre class="language-python"><code>import anthropic
import os

client = anthropic.Anthropic(
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    base_url=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic&quot;,
)

tools = [
    {
        &quot;name&quot;: &quot;get_weather&quot;,
        &quot;description&quot;: &quot;获取指定城市的天气信息&quot;,
        &quot;input_schema&quot;: {
            &quot;type&quot;: &quot;object&quot;,
            &quot;properties&quot;: {
                &quot;city&quot;: {
                    &quot;type&quot;: &quot;string&quot;,
                    &quot;description&quot;: &quot;城市名称&quot;
                }
            },
            &quot;required&quot;: [&quot;city&quot;]
        }
    }
]

message = client.messages.create(
    model=&quot;qwen4-max&quot;,
    max_tokens=1024,
    tools=tools,
    messages=[
        {
            &quot;role&quot;: &quot;user&quot;,
            &quot;content&quot;: &quot;杭州今天天气怎么样？&quot;
        }
    ]
)

print(message.content)
</code></pre></div><a id="fig-code-group-6-typescript-tab"></a>TypeScript<div><a id="code-code-group-6-typescript"></a><pre class="language-typescript"><code>import Anthropic from &quot;@anthropic-ai/sdk&quot;;

async function main() {
  const anthropic = new Anthropic({
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic&quot;,
  });

  const message = await anthropic.messages.create({
    model: &quot;qwen4-max&quot;,
    max_tokens: 1024,
    tools: [
      {
        name: &quot;get_weather&quot;,
        description: &quot;获取指定城市的天气信息&quot;,
        input_schema: {
          type: &quot;object&quot;,
          properties: {
            city: { type: &quot;string&quot;, description: &quot;城市名称&quot; }
          },
          required: [&quot;city&quot;],
        },
      },
    ],
    messages: [{
      role: &quot;user&quot;,
      content: &quot;杭州今天天气怎么样？&quot;
    }],
  });

  console.log(JSON.stringify(message.content, null, 2));
}

main().catch(console.error);
</code></pre></div><a id="fig-code-group-6-curl-tab"></a>curl<div><a id="code-code-group-6-curl"></a><pre class="language-bash"><code>curl -X POST &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic/v1/messages&quot; \
  -H &quot;Content-Type: application/json&quot; \
  -H &quot;x-api-key: $DASHSCOPE_API_KEY&quot; \
  -d '{
    &quot;model&quot;: &quot;qwen4-max&quot;,
    &quot;max_tokens&quot;: 1024,
    &quot;tools&quot;: [
        {
            &quot;name&quot;: &quot;get_weather&quot;,
            &quot;description&quot;: &quot;获取指定城市的天气信息&quot;,
            &quot;input_schema&quot;: {
                &quot;type&quot;: &quot;object&quot;,
                &quot;properties&quot;: {
                    &quot;city&quot;: {
                        &quot;type&quot;: &quot;string&quot;,
                        &quot;description&quot;: &quot;城市名称&quot;
                    }
                },
                &quot;required&quot;: [&quot;city&quot;]
            }
        }
    ],
    &quot;messages&quot;: [
        {
            &quot;role&quot;: &quot;user&quot;,
            &quot;content&quot;: &quot;杭州今天天气怎么样？&quot;
        }
    ]
}'
</code></pre></div></div></section><a id="联网搜索"></a><section><a id="联网搜索-h4"></a><h4>联网搜索</h4><a id="fig-code-group-7"></a><div><a id="fig-code-group-7-python-tab"></a>Python<div><a id="code-code-group-7-python"></a><pre class="language-python"><code>import anthropic
import os

client = anthropic.Anthropic(
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    base_url=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic&quot;,
)

message = client.messages.create(
    model=&quot;qwen4-max&quot;,
    max_tokens=2048,
    # 传入客户端标识，否则联网搜索不生效
    system=[{&quot;type&quot;: &quot;text&quot;, &quot;text&quot;: &quot;x-anthropic-billing-header: cc_entrypoint=cli;&quot;}],
    messages=[{&quot;role&quot;: &quot;user&quot;, &quot;content&quot;: &quot;杭州明天天气如何&quot;}],
    tools=[
        {
            &quot;type&quot;: &quot;web_search_20250305&quot;,
            &quot;name&quot;: &quot;web_search&quot;,
            &quot;max_uses&quot;: 8
        }
    ],
    thinking={&quot;type&quot;: &quot;disabled&quot;},
)

for block in message.content:
    print(f&quot;[{block.type}]&quot;)
    if block.type == &quot;server_tool_use&quot;:
        print(f&quot;  name: {block.name}, queries: {block.input.get('queries')}&quot;)
    elif block.type == &quot;web_search_tool_result&quot;:
        for result in block.content:
            print(f&quot;  {result.title} - {result.url}&quot;)
    elif block.type == &quot;text&quot;:
        print(block.text)

print(f&quot;检索次数: {message.usage.server_tool_use.web_search_requests}&quot;)
</code></pre></div><a id="fig-code-group-7-typescript-tab"></a>TypeScript<div><a id="code-code-group-7-typescript"></a><pre class="language-typescript"><code>import Anthropic from &quot;@anthropic-ai/sdk&quot;;

async function main() {
  const anthropic = new Anthropic({
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic&quot;,
  });

  const message = await anthropic.messages.create({
    model: &quot;qwen4-max&quot;,
    max_tokens: 2048,
    // 传入客户端标识，否则联网搜索不生效
    system: [{ type: &quot;text&quot;, text: &quot;x-anthropic-billing-header: cc_entrypoint=cli;&quot; }],
    messages: [{ role: &quot;user&quot;, content: &quot;杭州明天天气如何&quot; }],
    tools: [
      {
        type: &quot;web_search_20250305&quot;,
        name: &quot;web_search&quot;,
        max_uses: 8,
      },
    ],
    thinking: { type: &quot;disabled&quot; },
  });

  for (const block of message.content) {
    console.log(`[${block.type}]`);
    if (block.type === &quot;server_tool_use&quot;) {
      console.log(`  name: ${block.name}, queries: ${block.input?.queries}`);
    } else if (block.type === &quot;web_search_tool_result&quot;) {
      for (const result of block.content) {
        console.log(`  ${result.title} - ${result.url}`);
      }
    } else if (block.type === &quot;text&quot;) {
      console.log(block.text);
    }
  }

  console.log(`检索次数: ${message.usage.server_tool_use?.web_search_requests}`);
}

main().catch(console.error);
</code></pre></div><a id="fig-code-group-7-curl-tab"></a>curl<div><a id="code-code-group-7-curl"></a><pre class="language-bash"><code>curl -X POST &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic/v1/messages&quot; \
  -H &quot;Content-Type: application/json&quot; \
  -H &quot;x-api-key: $DASHSCOPE_API_KEY&quot; \
  -d '{
    &quot;model&quot;: &quot;qwen4-max&quot;,
    &quot;max_tokens&quot;: 2048,
    &quot;system&quot;: [{&quot;type&quot;: &quot;text&quot;, &quot;text&quot;: &quot;x-anthropic-billing-header: cc_entrypoint=cli;&quot;}],
    &quot;messages&quot;: [{&quot;role&quot;: &quot;user&quot;, &quot;content&quot;: &quot;杭州明天天气如何&quot;}],
    &quot;tools&quot;: [{&quot;type&quot;: &quot;web_search_20250305&quot;, &quot;name&quot;: &quot;web_search&quot;, &quot;max_uses&quot;: 8}],
    &quot;thinking&quot;: {&quot;type&quot;: &quot;disabled&quot;}
}'
</code></pre></div></div></section><a id="显式缓存"></a><section><a id="显式缓存-h4"></a><h4>显式缓存</h4><a id="fig-code-group-8"></a><div><a id="fig-code-group-8-python-tab"></a>Python<div><a id="code-code-group-8-python"></a><pre class="language-python"><code>import anthropic
import os

client = anthropic.Anthropic(
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    base_url=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic&quot;,
)

# 模拟代码仓库内容，需达到最小可缓存长度（1024 Token）
long_text_content = &quot;&lt;Your Code Here&gt;&quot; * 400

def get_completion(user_input):
    response = client.messages.create(
        # 选择支持显式缓存的模型
        model=&quot;qwen4-max&quot;,
        max_tokens=1024,
        system=[
            {
                &quot;type&quot;: &quot;text&quot;,
                &quot;text&quot;: long_text_content,
                # 在 text 块上添加 cache_control 即标记缓存断点；也可放在 messages 数组的 content 块上
                &quot;cache_control&quot;: {&quot;type&quot;: &quot;ephemeral&quot;},
            }
        ],
        messages=[
            {&quot;role&quot;: &quot;user&quot;, &quot;content&quot;: user_input},
        ],
    )
    return response

# 第一次请求：创建缓存
first = get_completion(&quot;这段代码的内容是什么&quot;)
print(f&quot;创建缓存 Token：{first.usage.cache_creation_input_tokens}&quot;)
print(f&quot;命中缓存 Token：{first.usage.cache_read_input_tokens}&quot;)
print(&quot;=&quot; * 20)
# 第二次请求：长内容相同，仅修改提问 → 命中缓存
second = get_completion(&quot;这段代码可以怎么优化&quot;)
print(f&quot;创建缓存 Token：{second.usage.cache_creation_input_tokens}&quot;)
print(f&quot;命中缓存 Token：{second.usage.cache_read_input_tokens}&quot;)
</code></pre></div><a id="fig-code-group-8-typescript-tab"></a>TypeScript<div><a id="code-code-group-8-typescript"></a><pre class="language-typescript"><code>import Anthropic from &quot;@anthropic-ai/sdk&quot;;

const client = new Anthropic({
  apiKey: process.env.DASHSCOPE_API_KEY,
  baseURL: &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic&quot;,
});

// 模拟代码仓库内容，需达到最小可缓存长度（1024 Token）
const longTextContent = &quot;&lt;Your Code Here&gt;&quot;.repeat(400);

async function getCompletion(userInput) {
  return client.messages.create({
    // 选择支持显式缓存的模型
    model: &quot;qwen4-max&quot;,
    max_tokens: 1024,
    system: [
      {
        type: &quot;text&quot;,
        text: longTextContent,
        // 在 text 块上添加 cache_control 即标记缓存断点；也可放在 messages 数组的 content 块上
        cache_control: { type: &quot;ephemeral&quot; },
      },
    ],
    messages: [{ role: &quot;user&quot;, content: userInput }],
  });
}

// 第一次请求：创建缓存
const first = await getCompletion(&quot;这段代码的内容是什么&quot;);
console.log(`创建缓存 Token：${first.usage.cache_creation_input_tokens}`);
console.log(`命中缓存 Token：${first.usage.cache_read_input_tokens}`);
console.log(&quot;=&quot;.repeat(20));
// 第二次请求：长内容相同，仅修改提问 → 命中缓存
const second = await getCompletion(&quot;这段代码可以怎么优化&quot;);
console.log(`创建缓存 Token：${second.usage.cache_creation_input_tokens}`);
console.log(`命中缓存 Token：${second.usage.cache_read_input_tokens}`);
</code></pre></div><a id="fig-code-group-8-curl-tab"></a>curl<div><a id="code-code-group-8-curl"></a><pre class="language-bash"><code>curl -X POST &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic/v1/messages&quot; \
  -H &quot;Content-Type: application/json&quot; \
  -H &quot;x-api-key: $DASHSCOPE_API_KEY&quot; \
  -d '{
    &quot;model&quot;: &quot;qwen4-max&quot;,
    &quot;max_tokens&quot;: 1024,
    &quot;system&quot;: [
      {
        &quot;type&quot;: &quot;text&quot;,
        &quot;text&quot;: &quot;&lt;请在此处放置长度 ≥ 1024 Token 的可缓存内容&gt;&quot;,
        &quot;cache_control&quot;: {&quot;type&quot;: &quot;ephemeral&quot;}
      }
    ],
    &quot;messages&quot;: [
      {&quot;role&quot;: &quot;user&quot;, &quot;content&quot;: &quot;这段代码的内容是什么&quot;}
    ]
}'
</code></pre></div></div></section><a id="结构化输出"></a><section><a id="结构化输出-h4"></a><h4>结构化输出</h4><a id="fig-code-group-9"></a><div><a id="fig-code-group-9-python-tab"></a>Python<div><a id="code-code-group-9-python"></a><pre class="language-python"><code>import anthropic
import os

client = anthropic.Anthropic(
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    base_url=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic&quot;,
)

message = client.messages.create(
    model=&quot;deepseek-v4-pro&quot;,
    max_tokens=1024,
    messages=[
        {
            &quot;role&quot;: &quot;user&quot;,
            &quot;content&quot;: &quot;提取以下邮件的关键信息：张三 (zhangsan@example.com) 对企业版方案感兴趣，希望预约下周二下午 2 点的演示。&quot;
        }
    ],
    extra_body={
        &quot;output_config&quot;: {
            &quot;format&quot;: {
                &quot;type&quot;: &quot;json_schema&quot;,
                &quot;schema&quot;: {
                    &quot;type&quot;: &quot;object&quot;,
                    &quot;properties&quot;: {
                        &quot;name&quot;: {&quot;type&quot;: &quot;string&quot;},
                        &quot;email&quot;: {&quot;type&quot;: &quot;string&quot;},
                        &quot;plan_interest&quot;: {&quot;type&quot;: &quot;string&quot;},
                        &quot;demo_requested&quot;: {&quot;type&quot;: &quot;boolean&quot;}
                    },
                    &quot;required&quot;: [&quot;name&quot;, &quot;email&quot;, &quot;plan_interest&quot;, &quot;demo_requested&quot;],
                    &quot;additionalProperties&quot;: False
                }
            }
        }
    },
)

# deepseek-v4-pro 模型会返回 thinking 块，需要找到 type='text' 的内容块
text_block = next(block for block in message.content if block.type == &quot;text&quot;)
print(text_block.text)
</code></pre></div><a id="fig-code-group-9-typescript-tab"></a>TypeScript<div><a id="code-code-group-9-typescript"></a><pre class="language-typescript"><code>import Anthropic from &quot;@anthropic-ai/sdk&quot;;

const anthropic = new Anthropic({
  apiKey: process.env.DASHSCOPE_API_KEY,
  baseURL: &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic&quot;,
});

async function main() {
  // output_config 是百炼平台扩展参数，SDK 类型定义中不包含该字段，
  // 通过交叉类型扩展官方参数类型进行透传，避免不安全的类型断言
  type MessageCreateParamsWithOutputConfig =
    Anthropic.MessageCreateParamsNonStreaming &amp; {
      output_config: {
        format: {
          type: &quot;json_schema&quot;;
          schema: Record&lt;string, unknown&gt;;
        };
      };
    };

  const params: MessageCreateParamsWithOutputConfig = {
    model: &quot;deepseek-v4-pro&quot;,
    max_tokens: 1024,
    messages: [{
      role: &quot;user&quot;,
      content: &quot;提取以下邮件的关键信息：张三 (zhangsan@example.com) 对企业版方案感兴趣，希望预约下周二下午 2 点的演示。&quot;
    }],
    output_config: {
      format: {
        type: &quot;json_schema&quot;,
        schema: {
          type: &quot;object&quot;,
          properties: {
            name: { type: &quot;string&quot; },
            email: { type: &quot;string&quot; },
            plan_interest: { type: &quot;string&quot; },
            demo_requested: { type: &quot;boolean&quot; }
          },
          required: [&quot;name&quot;, &quot;email&quot;, &quot;plan_interest&quot;, &quot;demo_requested&quot;],
          additionalProperties: false
        }
      }
    }
  };
  const message = await anthropic.messages.create(params);

  // deepseek-v4-pro 模型会返回 thinking 块，需要找到 type='text' 的内容块
  const textBlock = message.content.find(
    (block): block is Anthropic.TextBlock =&gt; block.type === &quot;text&quot;
  );
  console.log(textBlock?.text);
}

main().catch(console.error);
</code></pre></div><a id="fig-code-group-9-curl-tab"></a>curl<div><a id="code-code-group-9-curl"></a><pre class="language-bash"><code>curl -X POST &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic/v1/messages&quot; \
  -H &quot;Content-Type: application/json&quot; \
  -H &quot;x-api-key: $DASHSCOPE_API_KEY&quot; \
  -d '{
    &quot;model&quot;: &quot;deepseek-v4-pro&quot;,
    &quot;max_tokens&quot;: 1024,
    &quot;messages&quot;: [
        {
            &quot;role&quot;: &quot;user&quot;,
            &quot;content&quot;: &quot;提取以下邮件的关键信息：张三 (zhangsan@example.com) 对企业版方案感兴趣，希望预约下周二下午 2 点的演示。&quot;
        }
    ],
    &quot;output_config&quot;: {
        &quot;format&quot;: {
            &quot;type&quot;: &quot;json_schema&quot;,
            &quot;schema&quot;: {
                &quot;type&quot;: &quot;object&quot;,
                &quot;properties&quot;: {
                    &quot;name&quot;: {&quot;type&quot;: &quot;string&quot;},
                    &quot;email&quot;: {&quot;type&quot;: &quot;string&quot;},
                    &quot;plan_interest&quot;: {&quot;type&quot;: &quot;string&quot;},
                    &quot;demo_requested&quot;: {&quot;type&quot;: &quot;boolean&quot;}
                },
                &quot;required&quot;: [&quot;name&quot;, &quot;email&quot;, &quot;plan_interest&quot;, &quot;demo_requested&quot;],
                &quot;additionalProperties&quot;: false
            }
        }
    }
}'
</code></pre></div></div></section></section></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="ag1a2b3c4d5f0"></a><h2>非流式响应</h2><p><strong>id</strong> <code>string</code></p><p>消息的唯一标识。</p><p><strong>type</strong> <code>string</code></p><p>固定为 <code>message</code>。</p><p><strong>role</strong> <code>string</code></p><p>固定为 <code>assistant</code>。</p><p><strong>model</strong> <code>string</code></p><p>使用的模型名称。</p><p><strong>content</strong> <code>array</code></p><p>内容数组。</p><a id="accordion-content-数组元素类型-2"></a><section><p>content 数组元素类型</p><div><strong>文本信息</strong><a id="accordion-属性-17"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code></p><p>固定为 <code>text</code>。</p><p><strong>text</strong> <code>string</code></p><p>模型生成的文本回复。</p></div></section><p><strong>思考信息</strong>（开启深度思考时返回）</p><a id="accordion-属性-18"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code></p><p>固定为 <code>thinking</code>。</p><p><strong>thinking</strong> <code>string</code></p><p>模型在生成最终回复前的思考过程。</p><p><strong>signature</strong> <code>string</code></p><p><code>qwen4-max</code>, <code>thinking.display=&quot;summarized&quot;</code>: Anthropic Messages 的 thinking block 包含 <code>thinking</code> 摘要和 <code>signature</code> 密文。流式先返回 <code>thinking_delta</code>，再返回完整 <code>signature_delta</code>，关闭 thinking block 后返回正文或工具调用；未产生思考或加密失败时 signature 可能为空字符串。</p><p><code>thinking.display != &quot;summarized&quot;</code>: 当前固定为空字符串。</p></div></section><p><strong>工具调用信息</strong>（Function Call 场景）</p><a id="accordion-属性-19"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code></p><p>固定为 <code>tool_use</code>。</p><p><strong>id</strong> <code>string</code></p><p>工具调用的唯一标识，用于在后续 <code>tool_result</code> 中关联结果。</p><p><strong>name</strong> <code>string</code></p><p>被调用的工具名称。</p><p><strong>input</strong> <code>object</code></p><p>工具调用的入参。</p></div></section><p><strong>服务端工具调用信息</strong>（联网搜索场景，模型返回的服务端检索请求）</p><a id="accordion-属性-20"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code></p><p>固定为 <code>server_tool_use</code>。</p><p><strong>id</strong> <code>string</code></p><p>服务端工具调用唯一标识。</p><p><strong>name</strong> <code>string</code></p><p>工具名称，如 <code>web_search</code>。</p><p><strong>input</strong> <code>object</code></p><p>入参，含 <code>queries</code> 数组（模型生成的检索查询）。</p><p><strong>caller</strong> <code>object</code> （可选）</p><p>调用方信息，<code>type</code> 为 <code>direct</code> 表示由模型直接发起调用。</p></div></section><p><strong>联网搜索结果信息</strong>（联网搜索场景，服务端返回的检索结果）</p><a id="accordion-属性-21"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code></p><p>固定为 <code>web_search_tool_result</code>。</p><p><strong>tool_use_id</strong> <code>string</code></p><p>对应 <code>server_tool_use</code> 中的 <code>id</code>。</p><p><strong>content</strong> <code>array</code></p><p>检索结果数组，元素为 <code>web_search_result</code> 对象。</p><a id="accordion-web-search-result-属性"></a><section><p>web_search_result 属性</p><div><p><strong>type</strong> <code>string</code></p><p>固定为 <code>web_search_result</code>。</p><p><strong>title</strong> <code>string</code></p><p>网页标题。</p><p><strong>url</strong> <code>string</code></p><p>网页地址。</p><p><strong>encrypted_content</strong> <code>string</code></p><p>加密的网页内容。</p><p><strong>page_age</strong> <code>string 或 null</code></p><p>网页时效，可为 <code>null</code>。</p></div></section><p><strong>caller</strong> <code>object</code> （可选）</p><p>调用方信息，<code>type</code> 为 <code>direct</code> 表示由模型直接发起调用。</p></div></section><p><strong>网页抓取结果</strong>（<code>web_fetch_tool_result</code>）</p><a id="accordion-网页抓取结果"></a><section><p>网页抓取结果</p><div><table><thead><tr><th>字段</th><th>类型</th><th>说明</th></tr></thead><tbody><tr><td><code>type</code></td><td><code>string</code></td><td><code>web_fetch_tool_result</code></td></tr><tr><td><code>tool_use_id</code></td><td><code>string</code></td><td>对应 <code>server_tool_use.id</code>。</td></tr><tr><td><code>content</code></td><td><code>object</code></td><td>抓取结果。</td></tr><tr><td><code>content.type</code></td><td><code>string</code></td><td><code>web_fetch_result</code></td></tr><tr><td><code>content.url</code></td><td><code>string</code></td><td>网页地址。</td></tr><tr><td><code>content.retrieved_at</code></td><td><code>string</code></td><td>抓取时间。</td></tr><tr><td><code>content.content</code></td><td><code>object</code></td><td>网页文档。</td></tr><tr><td><code>content.content.type</code></td><td><code>string</code></td><td><code>document</code></td></tr><tr><td><code>content.content.title</code></td><td><code>string</code></td><td>网页标题。</td></tr><tr><td><code>content.content.source</code></td><td><code>object</code></td><td>文档内容。</td></tr><tr><td><code>content.content.source.type</code></td><td><code>string</code></td><td><code>text</code></td></tr><tr><td><code>content.content.source.media_type</code></td><td><code>string</code></td><td><code>text/plain</code></td></tr><tr><td><code>content.content.source.data</code></td><td><code>string</code></td><td>文档内容。</td></tr><tr><td><code>caller</code></td><td><code>object</code></td><td>调用方信息。</td></tr><tr><td><code>caller.type</code></td><td><code>string</code></td><td><code>direct</code></td></tr></tbody></table></div></section></div></section><p><strong>stop_reason</strong> <code>string</code></p><p>停止原因。可选值：<code>end_turn</code>（正常结束）、<code>max_tokens</code>（达到 Token 上限）、<code>tool_use</code>（工具调用）。</p><p><strong>stop_sequence</strong> <code>string</code></p><p>固定为 <code>null</code>。</p><p><strong>usage</strong> <code>object</code></p><p>Token 用量统计。</p><div><div><p><strong>说明</strong>流式调用中，<code>message_start</code> 事件的 <code>usage</code> 仅包含 <code>input_tokens</code> 和 <code>output_tokens</code>；完整字段（含 <code>cache_creation_input_tokens</code>、<code>cache_read_input_tokens</code> 和 <code>server_tool_use</code>）在 <code>message_delta</code> 事件中返回。</p></div></div><a id="accordion-属性-22"></a><section><p>属性</p><div><p><strong>input_tokens</strong> <code>integer</code></p><p>输入 Token 数量。</p><p><strong>output_tokens</strong> <code>integer</code></p><p>输出 Token 数量。</p><p><strong>cache_creation_input_tokens</strong> <code>integer</code></p><p>缓存创建消耗的输入 Token 数量。</p><p><strong>cache_read_input_tokens</strong> <code>integer</code></p><p>缓存读取消耗的输入 Token 数量。</p><p><strong>server_tool_use</strong> <code>object</code> （可选）</p><p>服务端工具用量统计。仅在请求中使用了服务端工具（如联网搜索）时返回。</p><a id="accordion-属性-23"></a><section><p>属性</p><div><p><strong>web_search_requests</strong> <code>integer</code></p><p>联网搜索的检索次数。</p><p><strong>web_fetch_requests</strong> <code>integer</code></p><p>网页抓取次数。</p></div></section></div></section></td><td><a id="anthropic-messages-response-example"></a><div><a id="sec-tabs-3"></a><section><a id="基础响应"></a><section><a id="基础响应-h4"></a><h4>基础响应</h4><p>以下为 <code>qwen3.8-max</code> 的返回示例，用于说明响应字段。</p><a id="code-block"></a><pre class="language-json"><code>{
  &quot;id&quot;: &quot;msg_e2898f19-fc0e-4cb3-bd9b-5b7dc4ea3bc9&quot;,
  &quot;type&quot;: &quot;message&quot;,
  &quot;role&quot;: &quot;assistant&quot;,
  &quot;model&quot;: &quot;qwen3.8-max&quot;,
  &quot;content&quot;: [
    {
      &quot;type&quot;: &quot;thinking&quot;,
      &quot;thinking&quot;: &quot;让我分析一下这个问题...&quot;,
      &quot;signature&quot;: &quot;&quot;
    },
    {
      &quot;type&quot;: &quot;text&quot;,
      &quot;text&quot;: &quot;你好！我是通义千问...&quot;
    }
  ],
  &quot;stop_reason&quot;: &quot;end_turn&quot;,
  &quot;stop_sequence&quot;: null,
  &quot;usage&quot;: {
    &quot;input_tokens&quot;: 22,
    &quot;output_tokens&quot;: 223,
    &quot;cache_creation_input_tokens&quot;: 0,
    &quot;cache_read_input_tokens&quot;: 0
  }
}
</code></pre></section><a id="联网搜索响应"></a><section><a id="联网搜索响应-h4"></a><h4>联网搜索响应</h4><p>以下为 <code>qwen3.8-max</code> 的返回示例，用于说明响应字段。</p><a id="code-block-2"></a><pre class="language-json"><code>{
  &quot;id&quot;: &quot;msg_2db0950e-956e-9528-b75f-0b047ef86c03&quot;,
  &quot;type&quot;: &quot;message&quot;,
  &quot;role&quot;: &quot;assistant&quot;,
  &quot;model&quot;: &quot;qwen3.8-max&quot;,
  &quot;content&quot;: [
    {
      &quot;type&quot;: &quot;server_tool_use&quot;,
      &quot;id&quot;: &quot;srvtoolu_1bffa8e70882403cb14499af&quot;,
      &quot;name&quot;: &quot;web_search&quot;,
      &quot;input&quot;: {
        &quot;queries&quot;: [&quot;杭州明天天气&quot;]
      },
      &quot;caller&quot;: {&quot;type&quot;: &quot;direct&quot;}
    },
    {
      &quot;type&quot;: &quot;web_search_tool_result&quot;,
      &quot;tool_use_id&quot;: &quot;srvtoolu_1bffa8e70882403cb14499af&quot;,
      &quot;content&quot;: [
        {
          &quot;type&quot;: &quot;web_search_result&quot;,
          &quot;title&quot;: &quot;17日（明天）&quot;,
          &quot;url&quot;: &quot;https://www.weather.com.cn/weather/101210101.shtml&quot;,
          &quot;encrypted_content&quot;: &quot;eyJ0aXRsZSI6ICIxN+aXpe+8iOaYjuWkqe+8iSIs...&quot;,
          &quot;page_age&quot;: null
        },
        {
          &quot;type&quot;: &quot;web_search_result&quot;,
          &quot;title&quot;: &quot;杭州-天气预报&quot;,
          &quot;url&quot;: &quot;https://www.nmc.cn/publish/forecast/AZJ/hangzhou.html&quot;,
          &quot;encrypted_content&quot;: &quot;eyJ0aXRsZSI6ICLmna3lt54t5aSp5rCU6aKE5oqlIiw...&quot;,
          &quot;page_age&quot;: null
        }
      ],
      &quot;caller&quot;: {&quot;type&quot;: &quot;direct&quot;}
    },
    {
      &quot;type&quot;: &quot;text&quot;,
      &quot;text&quot;: &quot;杭州明天（10月17日）的天气预计为多云转晴，气温在 22℃ 到 30℃ 之间...&quot;
    }
  ],
  &quot;stop_reason&quot;: &quot;end_turn&quot;,
  &quot;stop_sequence&quot;: null,
  &quot;usage&quot;: {
    &quot;input_tokens&quot;: 1920,
    &quot;output_tokens&quot;: 122,
    &quot;cache_creation_input_tokens&quot;: 0,
    &quot;cache_read_input_tokens&quot;: 0,
    &quot;server_tool_use&quot;: {
      &quot;web_search_requests&quot;: 1
    }
  },
  &quot;x_tools&quot;: {
    &quot;web_search&quot;: {
      &quot;count&quot;: 1
    }
  }
}
</code></pre></section></section></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="ah1a2b3c4d5e8"></a><h2>流式响应</h2><strong>message_start</strong><p>流的第一个事件，标记消息开始。</p><a id="accordion-属性-24"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code></p><p>固定为 <code>message_start</code>。</p><p><strong>message</strong> <code>object</code></p><p>初始消息对象，<code>content</code> 为空数组，<code>usage</code> 仅含 <code>input_tokens</code> 和 <code>output_tokens</code>。</p></div></section><strong>content_block_start</strong><p>每个内容块开始时发送，标记新内容块的索引和类型。</p><a id="accordion-属性-25"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code></p><p>固定为 <code>content_block_start</code>。</p><p><strong>index</strong> <code>integer</code></p><p>内容块索引，从 0 开始，对应该消息 <code>content</code> 数组中的位置。</p><p><strong>content_block</strong> <code>object</code></p><p>内容块的初始对象。<code>type</code> 取值为 <code>text</code>、<code>thinking</code>、<code>tool_use</code>、<code>server_tool_use</code> 或 <code>web_search_tool_result</code> / <code>web_fetch_tool_result</code>。<code>tool_use</code> 类型在此事件中 <code>input</code> 为空对象，完整入参由后续 <code>content_block_delta</code> 增量拼接。<code>web_search_tool_result</code> 在此事件中携带完整 <code>content</code> 数组，非增量拼接。</p></div></section><strong>content_block_delta</strong><p>内容块的增量更新事件。同一内容块会发送多个该事件。</p><a id="accordion-属性-26"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code></p><p>固定为 <code>content_block_delta</code>。</p><p><strong>index</strong> <code>integer</code></p><p>所属内容块索引。</p><p><strong>delta</strong> <code>object</code></p><p>增量对象，<code>type</code> 取值：</p><ul><li><code>text_delta</code>：文本增量，含 <code>text</code> 字段。</li><li><code>thinking_delta</code>：思考增量，含 <code>thinking</code> 字段。</li><li><code>signature_delta</code> (<code>signature</code>): <code>qwen4-max</code>, <code>thinking.display=&quot;summarized&quot;</code>: Anthropic Messages 的 thinking block 包含 <code>thinking</code> 摘要和 <code>signature</code> 密文。流式先返回 <code>thinking_delta</code>，再返回完整 <code>signature_delta</code>，关闭 thinking block 后返回正文或工具调用；未产生思考或加密失败时 signature 可能为空字符串。 <code>thinking.display != &quot;summarized&quot;</code>: <code>signature=&quot;&quot;</code>.</li><li><code>input_json_delta</code>：工具调用入参增量，含 <code>partial_json</code> 字段。</li></ul></div></section><strong>content_block_stop</strong><p>内容块结束事件。</p><a id="accordion-属性-27"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code></p><p>固定为 <code>content_block_stop</code>。</p><p><strong>index</strong> <code>integer</code></p><p>结束的内容块索引。</p></div></section><strong>message_delta</strong><p>消息级更新事件，在所有内容块结束后发送，包含停止原因和完整的 Token 用量统计。</p><a id="accordion-属性-28"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code></p><p>固定为 <code>message_delta</code>。</p><p><strong>delta</strong> <code>object</code></p><p>包含 <code>stop_reason</code> 和 <code>stop_sequence</code>，取值参见上方非流式响应表格。</p><p><strong>usage</strong> <code>object</code></p><p>完整的 Token 用量统计，包含 <code>input_tokens</code>、<code>output_tokens</code>、<code>cache_creation_input_tokens</code>、<code>cache_read_input_tokens</code>。</p></div></section><strong>message_stop</strong><p>流的最后一个事件，标记消息结束。</p><a id="accordion-属性-29"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code></p><p>固定为 <code>message_stop</code>。</p><p>此外，流式响应还会定期发送 <strong>ping</strong> 事件（<code>{&quot;type&quot;:&quot;ping&quot;}</code>）用于保持连接活跃，客户端可忽略。</p></div></section></td><td><a id="anthropic-messages-stream-example"></a><div><strong>流式响应示例</strong><p>以下为 <code>qwen3.8-max</code> 的返回示例，用于说明响应字段。</p><a id="code-block-3"></a><pre class="language-json"><code>{&quot;type&quot;:&quot;message_start&quot;,&quot;message&quot;:{&quot;id&quot;:&quot;msg_xxx&quot;,&quot;type&quot;:&quot;message&quot;,&quot;role&quot;:&quot;assistant&quot;,&quot;model&quot;:&quot;qwen3.8-max&quot;,&quot;content&quot;:[],&quot;usage&quot;:{&quot;input_tokens&quot;:15,&quot;output_tokens&quot;:0}}}
{&quot;type&quot;:&quot;content_block_start&quot;,&quot;index&quot;:0,&quot;content_block&quot;:{&quot;type&quot;:&quot;thinking&quot;,&quot;thinking&quot;:&quot;&quot;,&quot;signature&quot;:&quot;&quot;}}
{&quot;type&quot;:&quot;content_block_delta&quot;,&quot;index&quot;:0,&quot;delta&quot;:{&quot;type&quot;:&quot;thinking_delta&quot;,&quot;thinking&quot;:&quot;Here's a thinking process:\n\n1. **Analyze User Input:**\n   - **Topic:** 人工智能 (Artificial Intelligence / AI)\n   - **Request:** 请简单介绍一下人工智能。&quot;}}
{&quot;type&quot;:&quot;content_block_delta&quot;,&quot;index&quot;:0,&quot;delta&quot;:{&quot;type&quot;:&quot;signature_delta&quot;,&quot;signature&quot;:&quot;&quot;}}
{&quot;type&quot;:&quot;content_block_stop&quot;,&quot;index&quot;:0}
{&quot;type&quot;:&quot;content_block_start&quot;,&quot;index&quot;:1,&quot;content_block&quot;:{&quot;type&quot;:&quot;text&quot;,&quot;text&quot;:&quot;&quot;}}
{&quot;type&quot;:&quot;content_block_delta&quot;,&quot;index&quot;:1,&quot;delta&quot;:{&quot;type&quot;:&quot;text_delta&quot;,&quot;text&quot;:&quot;人工智能（Artificial Intelligence，简称AI）是计算机科学的重要分支...&quot;}}
{&quot;type&quot;:&quot;content_block_stop&quot;,&quot;index&quot;:1}
{&quot;type&quot;:&quot;message_delta&quot;,&quot;delta&quot;:{&quot;stop_reason&quot;:&quot;end_turn&quot;,&quot;stop_sequence&quot;:null},&quot;usage&quot;:{&quot;input_tokens&quot;:15,&quot;output_tokens&quot;:1078,&quot;cache_creation_input_tokens&quot;:0,&quot;cache_read_input_tokens&quot;:0}}
{&quot;type&quot;:&quot;message_stop&quot;}
</code></pre></div></td></tr></tbody></table>

<a id="常见问题"></a>

<a id="faq-ccbaseurl-h2"></a>

## 常见问题

**在 Claude Desktop 或 Claude Code 中配置后，连接测试报错**`Model discovery — Gateway /v1/models returned HTTP 404`**，或请求地址出现**`/v1/v1/models`**，如何解决？**

Claude Desktop、Claude Code 等客户端的模型发现（model discovery）功能会在配置的 base URL 后自动追加 `/v1/models`。请按以下两点排查：

-   **base URL 不要以**`/v1/`**结尾**：应填写到 `/apps/anthropic` 为止（例如华北2（北京）填 `https://dashscope.aliyuncs.com/apps/anthropic`，其余地域的地址见上方“接入信息”）。若误填为 `.../apps/anthropic/v1/`，客户端追加 `/v1/models` 后会形成 `/v1/v1/models` 的重复路径，导致 HTTP 404。因此出现 404 时，请先检查实际请求地址是否出现 `/v1/v1/` 重复，若有则去掉 base URL 末尾的 `/v1/`。
-   **手动添加模型以跳过自动发现**：百炼 Anthropic 兼容端点仅提供 Messages 接口（`/v1/messages`），不提供模型列表接口（`/v1/models`），因此模型发现请求本身也会返回 404。请在客户端的 Models 中手动添加模型（例如 `qwen3.7-plus`）以跳过自动发现。
