# OpenAI兼容-Chat

通过兼容 OpenAI 格式的 Chat API 调用模型，查看输入输出参数说明及调用示例。

<a id="sec-tabs"></a>

<a id="华北2-北京"></a>

<a id="华北2-北京-h4"></a>

#### 华北2（北京）

SDK 调用配置的`base_url`：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`

HTTP 请求地址：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions`

<a id="新加坡"></a>

<a id="新加坡-h4"></a>

#### 新加坡

SDK 调用配置的`base_url`：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`

HTTP 请求地址：`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1/chat/completions`

<a id="美国-弗吉尼亚"></a>

<a id="美国-弗吉尼亚-h4"></a>

#### 美国（弗吉尼亚）

SDK 调用配置的`base_url`：`https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/compatible-mode/v1`

HTTP 请求地址：`POST https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/compatible-mode/v1/chat/completions`

<a id="德国-法兰克福"></a>

<a id="德国-法兰克福-h4"></a>

#### 德国（法兰克福）

SDK 调用配置的`base_url`：`https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1`

HTTP 请求地址：`POST https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1/chat/completions`

<a id="日本-东京"></a>

<a id="日本-东京-h4"></a>

#### 日本（东京）

SDK 调用配置的`base_url`：`https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/compatible-mode/v1`

HTTP 请求地址：`POST https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/compatible-mode/v1/chat/completions`

<a id="中国香港"></a>

<a id="中国香港-h4"></a>

#### 中国香港

SDK 调用配置的`base_url`：`https://{WorkspaceId}.cn-hongkong.maas.aliyuncs.com/compatible-mode/v1`

HTTP 请求地址：`POST https://{WorkspaceId}.cn-hongkong.maas.aliyuncs.com/compatible-mode/v1/chat/completions`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

您需要先[获取与配置 API Key](../preparations/get-api-key.md)。若通过OpenAI SDK进行调用，需要[安装SDK](../preparations/install-sdk.md)。

> **重要**
>
> 阿里云百炼为华北2（北京）、新加坡、中国香港地域推出了业务空间专属域名，**能够为推理请求提供卓越的性能和更高的稳定性**，建议迁移至新域名：
>
> -   华北2（北京）地域：从 `https://dashscope.aliyuncs.com` 迁移至 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
> -   新加坡地域：从 `https://dashscope-intl.aliyuncs.com` 迁移至 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`
>
> 其中 `{WorkspaceId}` 为您的业务空间 ID，可在阿里云百炼控制台的**业务空间详情**页面查看。现有域名仍可正常使用。

<table><tbody><tr><td><a id="afcd41d2b57zf"></a><h2>请求体</h2><p><strong>model</strong><code>string</code><strong>（必选）</strong></p><p>模型名称。</p><p>支持的模型：Qwen 大语言模型（商业版、开源版）、Qwen-VL、Qwen-Coder、Qwen-Omni、Qwen-Math、DeepSeek（阿里云直供、硅基流动直供、快手万擎直供）、Kimi（阿里云直供、月之暗面直供）、GLM（阿里云直供）、MiniMax（阿里云直供、稀宇科技直供）。</p><blockquote><p>三方直供模型仅在中国站的华北2（北京）地域可用，调用前需先在百炼控制台开通对应服务（以 SiliconFlow DeepSeek 为例：搜索 deepseek → 找到 SiliconFlow DeepSeek 模型卡片 → 单击立即开通 → 确认授权）。</p></blockquote><blockquote><p>Qwen-Audio不支持OpenAI兼容协议，仅支持DashScope协议。</p></blockquote><p><strong>具体模型名称和计费，请参见</strong><a href="https://bailian.console.aliyun.com/model/market">百炼控制台</a>。</p><p><strong>messages</strong><code>array</code><strong>（必选）</strong></p><p>传递给大模型的上下文，按对话顺序排列。</p><a id="accordion-消息类型"></a><section><p>消息类型</p><div><p>System Message<code>object</code>（可选）</p><p>系统消息，用于设定大模型的角色、语气、任务目标或约束条件等。一般放在<code>messages</code>数组的第一位。</p><blockquote><p>QwQ 模型不建议设置 System Message，QVQ 模型设置 System Message不会生效。</p></blockquote><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>content</strong><code>string</code><strong>（必选）</strong></p><p>系统指令，用于明确模型的角色、行为规范、回答风格和任务约束等。</p><p><strong>role</strong><code>string</code><strong>（必选）</strong></p><p>系统消息的角色，固定为 <code>system</code> 。</p></div></section><p>User Message<code>object</code><strong>（必选）</strong></p><p>用户消息，用于向模型传递问题、指令或上下文等。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>content</strong><code>string 或 array</code><strong>（必选）</strong></p><p>消息内容。若输入只有文本，则为 string 类型；若输入包含图像等多模态数据，或启用显式缓存，则为 array 类型。</p><a id="accordion-使用多模态模型或启用显式缓存时的属性"></a><section><p>使用多模态模型或启用显式缓存时的属性</p><div><p><strong>type</strong><code>string</code><strong>（必选）</strong></p><p>可选值：</p><ul><li><p><code>text</code></p><p>输入文本时需设为<code>text</code>。</p></li><li><p><code>image_url</code></p><p>输入图片时需设为<code>image_url</code>。</p></li><li><p><code>input_audio</code></p><p>输入音频时需设为<code>input_audio</code>。</p></li><li><p><code>video</code></p><p>输入图片列表形式的视频时需设为<code>video</code>。</p></li><li><p><code>video_url</code></p><p>输入视频文件时需设为<code>video_url</code>。</p><blockquote><p>Qwen-VL仅部分模型可输入视频文件，详情参见<a href="../../model-user-guide/model-experience/text-generation-model/vision.md#80dbf6ca8fh6s">视频理解（Qwen-VL）</a>；QVQ与Qwen-Omni 模型支持直接传入视频文件。</p></blockquote></li></ul><p><strong>text</strong><code>string</code></p><p>输入的文本。当<code>type</code>为<code>text</code>时，是必选参数。</p><p><strong>image_url</strong><code>object</code></p><p>输入的图片信息。当<code>type</code>为<code>image_url</code>时是必选参数。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>url</strong> <code>string</code><strong>（必选）</strong></p><p>图片的 URL或 Base64 Data URL。传入本地文件请参考<a href="../../model-user-guide/model-experience/text-generation-model/vision.md">图像与视频理解</a>。</p><p><strong>detail</strong> <code>string</code> （可选）</p><p>图片处理精度。自 Qwen4 起，Max、Plus 和 Flash 模型支持此参数。默认值为 <code>high</code>。</p><p>未传入 <code>max_pixels</code> 时：</p><ul><li><code>high</code>：按原图分辨率处理，上限为 <code>16777216</code> 像素。</li><li><code>low</code>：像素上限为 <code>2621440</code>。</li><li><code>auto</code>：与 <code>low</code> 相同。</li></ul><p>显式传入 <code>max_pixels</code> 时，以该值作为像素上限，优先于 <code>detail</code>。最大值为 <code>16777216</code>。Chat Completions 的 <code>max_pixels</code> 与 <code>image_url</code> 同级；DashScope 与 <code>image</code> 同级。</p><p>高分辨率图片使用 <code>high</code> 时，输入 Token 用量通常高于 <code>low</code>。</p><p>Chat Completions 可在 <code>image_url</code> 内或与 <code>image_url</code> 同级传入 <code>detail</code>；DashScope 与 <code>image</code> 同级传入。</p><a id="code-block"></a><pre class="language-json"><code>{&quot;type&quot;:&quot;image_url&quot;,&quot;image_url&quot;:{&quot;url&quot;:&quot;https://example.com/image.jpg&quot;,&quot;detail&quot;:&quot;high&quot;}}
</code></pre></div></section><p><strong>input_audio</strong><code>object</code></p><p>输入的音频信息。当<code>type</code>为<code>input_audio</code>时是必选参数。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>data</strong> <code>string</code><strong>（必选）</strong></p><p>音频的 URL 或Base64 Data URL。传入本地文件请参见：<a href="../../model-user-guide/model-experience/omni-modal/qwen-omni.md#c516d1e824x03">输入 Base64 编码的本地文件</a>。</p><p><strong>format</strong><code>string</code><strong>（必选）</strong></p><p>输入音频的格式，如<code>mp3</code>、<code>wav</code>等。</p></div></section><p><strong>video</strong><code>array</code></p><p>Qwen4-Max、Qwen3.8、Qwen3.7、Qwen3.6、Qwen3.5 系列以公网 URL 图像列表传入视频时，支持 4–8000 张图片；以 Base64 图像列表传入时，最多 250 张图片。</p><p>输入的<strong>图片列表形式的视频信息</strong>。当<code>type</code>为<code>video</code>时是必选参数。使用方法请参见：<a href="../../model-user-guide/model-experience/text-generation-model/vision.md#80dbf6ca8fh6s">视频理解（Qwen-VL、QVQ）</a>或<a href="../../model-user-guide/model-experience/omni-modal/qwen-omni.md">视频理解（Qwen-Omni）</a>。</p><p>示例值：</p><a id="code-block-2"></a><pre class="language-json"><code>[
    &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/xzsgiz/football1.jpg&quot;,
    &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/tdescd/football2.jpg&quot;,
    &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/zefdja/football3.jpg&quot;,
    &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/aedbqh/football4.jpg&quot;
]
</code></pre><p><strong>video_url</strong><code>object</code></p><p>输入的视频文件信息。当<code>type</code>为<code>video_url</code>时是必选参数。</p><p>Qwen-VL 只可理解视频文件的视觉信息，Qwen-Omni 可理解视频文件中的视觉与音频信息。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>url</strong> <code>string</code><strong>（必选）</strong></p><p>视频文件的公网 URL 或 Base64 Data URL。输入本地视频文件请参见<a href="../../model-user-guide/model-experience/omni-modal/qwen-omni.md#c516d1e824x03">输入 Base64 编码的本地文件</a>。</p></div></section><p><strong>fps</strong><code>float</code>（可选）</p><p>每秒抽帧数。取值范围为 [0.1, 10]，默认值为2.0。</p><blockquote><p>MiniMax/MiniMax-M3.1-Flash 和 MiniMax/MiniMax-M3 的 fps 取值范围为 [0.2, 5]，默认值为 1。</p></blockquote><a id="accordion-功能说明"></a><section><p>功能说明</p><div><p>fps有两个功能：</p><ul><li><p>输入视频文件时，控制抽帧频率，每 <code>1/fps</code> 秒抽取一帧。</p><blockquote><p>适用于 <a href="../../model-user-guide/model-experience/text-generation-model/vision.md">Qwen-VL 与 QVQ</a>、<a href="../../model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md">MiniMax/MiniMax-M3.1-Flash 和 MiniMax/MiniMax-M3</a> 模型。</p></blockquote></li><li><p>告知模型相邻帧之间的时间间隔，帮助其更好地理解视频的时间动态。同时适用于输入视频文件与图像列表时。该功能同时支持视频文件和图像列表输入，适用于事件时间定位或分段内容摘要等场景。</p><blockquote><p>支持Qwen3.7、Qwen3.6、Qwen3.5、<code>Qwen3-VL</code>、<code>Qwen2.5-VL</code>、Qwen3.8-Omni-Flash、Qwen3.5-Omni与QVQ模型。</p></blockquote></li></ul><p>较大的<code>fps</code>适合高速运动的场景（如体育赛事、动作电影等），较小的<code>fps</code>适合长视频或内容偏静态的场景。</p></div></section><a id="accordion-示例值"></a><section><p>示例值</p><div><ul><li>图像列表传入：<code>{&quot;video&quot;:[&quot;https://xx1.jpg&quot;,...,&quot;https://xxn.jpg&quot;]，&quot;fps&quot;:2}</code></li><li>视频文件传入：<code>{&quot;video&quot;: &quot;https://xx1.mp4&quot;，&quot;fps&quot;:2}</code></li></ul></div></section><p><strong>min_pixels</strong><code>integer</code>（可选）</p><p>设定输入图像或视频帧的最小像素阈值。当输入图像或视频帧的像素小于<code>min_pixels</code>时，会将其进行放大，直到总像素高于<code>min_pixels</code>。适用型号及取值见下方说明。</p><a id="accordion-取值范围"></a><section><p>取值范围</p><div><ul><li><strong>输入图像：</strong><ul><li><code>qwen4-max</code>、<code>qwen3.8-max</code>、<code>qwen3.8-max-0902</code>、<code>qwen3.8-flash</code>、<code>qwen3.8-2.4t-a95b</code>、<code>qwen3.8-27b</code>、Qwen3.7、Qwen3.6、Qwen3.5、Qwen3-VL：默认值和最小值均为：<code>65536</code></li><li><code>qwen3.8-omni-flash</code>、Qwen3.5-Omni ：默认值和最小值均为： <code>24576</code></li><li><code>Qwen2.5-VL</code>开源系列及<code>QVQ</code>系列模型：默认值和最小值均为<code>3136</code></li></ul></li><li><strong>输入视频文件或图像列表：</strong><ul><li><code>qwen4-max</code>、<code>qwen3-omni-flash</code>、<code>qwen3-vl-plus</code>、<code>qwen3.5-122b-a10b</code>、<code>qwen3.5-27b</code>、<code>qwen3.5-35b-a3b</code>、<code>qwen3.5-397b-a17b</code>、<code>qwen3.5-flash</code>、<code>qwen3.5-flash-2026-02-23</code>、<code>qwen3.5-omni-flash</code>、<code>qwen3.5-omni-flash-2026-03-15</code>、<code>qwen3.5-omni-plus</code>、<code>qwen3.5-omni-plus-2026-03-15</code>、<code>qwen3.5-plus</code>、<code>qwen3.5-plus-2026-02-15</code>、<code>qwen3.5-plus-2026-04-20</code>、<code>qwen3.6-27b</code>、<code>qwen3.6-35b-a3b</code>、<code>qwen3.6-flash</code>、<code>qwen3.6-flash-2026-04-16</code>、<code>qwen3.6-plus</code>、<code>qwen3.6-plus-2026-04-02</code>、<code>qwen3.7-flash</code>、<code>qwen3.7-flash-2026-07-15</code>、<code>qwen3.7-max-2026-06-08</code>、<code>qwen3.7-plus</code>、<code>qwen3.7-plus-2026-05-26</code>、<code>qwen3.8-27b</code>、<code>qwen3.8-flash</code>、<code>qwen3.8-max</code>、<code>qwen3.8-max-0902</code>、<code>qwen3.8-omni-flash</code>：默认值为 <code>65536</code>，最小值为 <code>4096</code>。</li><li><code>kimi-k2.5</code>、<code>kimi-k2.6</code>、<code>kimi-k2.7-code</code>：最小值为 <code>3136</code>。</li><li><code>Qwen2.5-VL</code>开源系列及<code>QVQ</code>系列模型：默认值为<code>50176</code>，最小值为<code>3136</code></li></ul></li></ul></div></section><a id="accordion-示例值-2"></a><section><p>示例值</p><div><ul><li>输入图像：<code>{&quot;type&quot;: &quot;image_url&quot;,&quot;image_url&quot;: {&quot;url&quot;:&quot;https://xxxx.jpg&quot;},&quot;min_pixels&quot;: 65536}</code></li><li>输入视频文件时：<code>{&quot;type&quot;: &quot;video_url&quot;,&quot;video_url&quot;: {&quot;url&quot;:&quot;https://xxxx.mp4&quot;},&quot;min_pixels&quot;: 65536}</code></li><li>输入图像列表时：<code>{&quot;type&quot;: &quot;video&quot;,&quot;video&quot;: [&quot;https://xx1.jpg&quot;,...,&quot;https://xxn.jpg&quot;],&quot;min_pixels&quot;: 65536}</code></li></ul></div></section><p><strong>max_pixels</strong><code>integer</code>（可选）</p><p>用于设定输入图像或视频帧的最大像素阈值。当输入图像或视频的像素在<code>[min_pixels, max_pixels]</code>区间内时，模型会按原图进行识别。当输入图像像素大于<code>max_pixels</code>时，会将图像进行缩小，直到总像素低于<code>max_pixels</code>。适用型号及取值见下方说明。</p><a id="accordion-取值范围-2"></a><section><p>取值范围</p><div><ul><li><strong>输入图像：</strong><ul><li><code>qwen4-max</code>：最大值为 <code>16777216</code>。未传入时按 <code>detail</code> 处理图像；显式传入的 <code>max_pixels</code> 不受 <code>vl_high_resolution_images</code> 影响。</li></ul><p>其他模型：<code>max_pixels</code> 的取值与是否开启<code>vl_high_resolution_images</code>参数有关。</p><ul><li><p>当<code>vl_high_resolution_images</code>为<code>False</code>时：</p><ul><li><code>qwen3.8-max</code>、<code>qwen3.8-max-0902</code>、<code>qwen3.8-flash</code>、<code>qwen3.8-2.4t-a95b</code>、<code>qwen3.8-27b</code>、Qwen3.7、 Qwen3.6 、 Qwen3.5 、 Qwen3-VL ：默认值为 <code>2621440</code> ，最大值为： <code>16777216</code></li><li><code>qwen3.8-omni-flash</code>、Qwen3.5-Omni ：默认值为 <code>1310720</code> ，最大值为： <code>16777216</code></li><li><code>Qwen2.5-VL</code> 开源系列及 <code>QVQ</code> 系列模型：默认值为 <code>1003520</code> ，最大值为 <code>12845056</code></li></ul></li><li><p>当<code>vl_high_resolution_images</code>为<code>True</code>时：</p><ul><li><code>qwen3.8-max</code>、<code>qwen3.8-max-0902</code>、<code>qwen3.8-flash</code>、<code>qwen3.8-2.4t-a95b</code>、<code>qwen3.8-27b</code>、<code>qwen3.8-omni-flash</code>、Qwen3.7、 Qwen3.6 、 Qwen3.5-Omni 、 Qwen3.5 、 Qwen3-VL ： <code>max_pixels</code> 无效，输入图像的最大像素固定为 <code>16777216</code></li><li><code>Qwen2.5-VL</code> 开源系列及 <code>QVQ</code> 系列模型： <code>max_pixels</code> 无效，输入图像的最大像素固定为 <code>12845056</code></li></ul></li></ul></li><li><strong>输入视频文件或图像列表：</strong><p>同时设置 <code>min_pixels</code> 和 <code>max_pixels</code> 时，<code>max_pixels</code> 不得小于 <code>min_pixels</code>。</p><ul><li><code>qwen4-max</code>、<code>qwen3-vl-plus</code>、<code>qwen3.5-122b-a10b</code>、<code>qwen3.5-27b</code>、<code>qwen3.5-35b-a3b</code>、<code>qwen3.5-397b-a17b</code>、<code>qwen3.5-flash</code>、<code>qwen3.5-flash-2026-02-23</code>、<code>qwen3.5-omni-flash</code>、<code>qwen3.5-omni-flash-2026-03-15</code>、<code>qwen3.5-omni-plus</code>、<code>qwen3.5-omni-plus-2026-03-15</code>、<code>qwen3.5-plus</code>、<code>qwen3.5-plus-2026-02-15</code>、<code>qwen3.5-plus-2026-04-20</code>、<code>qwen3.6-27b</code>、<code>qwen3.6-35b-a3b</code>、<code>qwen3.6-flash</code>、<code>qwen3.6-flash-2026-04-16</code>、<code>qwen3.6-plus</code>、<code>qwen3.6-plus-2026-04-02</code>、<code>qwen3.7-flash</code>、<code>qwen3.7-flash-2026-07-15</code>、<code>qwen3.7-max-2026-06-08</code>、<code>qwen3.7-plus</code>、<code>qwen3.7-plus-2026-05-26</code>、<code>qwen3.8-27b</code>、<code>qwen3.8-flash</code>、<code>qwen3.8-max</code>、<code>qwen3.8-max-0902</code>、<code>qwen3.8-omni-flash</code>：默认值为 <code>655360</code>，最大值为 <code>2048000</code>。</li><li>其他<code>Qwen3-VL</code>开源模型：默认值<code>655360</code>，最大值为<code>786432</code></li><li><code>qwen3-omni-flash</code>：默认值为 <code>655360</code>，最大值为 <code>786432</code>。</li><li><code>kimi-k2.7-code</code>、<code>kimi-k2.6</code>、<code>kimi-k2.5</code>：最大值为 <code>1568000</code>。</li><li><code>Qwen2.5-VL</code>开源系列及<code>QVQ</code>系列模型：默认值为<code>501760</code>，最大值为<code>602112</code></li></ul></li></ul></div></section><a id="accordion-示例值-3"></a><section><p>示例值</p><div><ul><li>输入图像：<code>{&quot;type&quot;: &quot;image_url&quot;,&quot;image_url&quot;: {&quot;url&quot;:&quot;https://xxxx.jpg&quot;},&quot;max_pixels&quot;: 8388608}</code></li><li>输入视频文件时：<code>{&quot;type&quot;: &quot;video_url&quot;,&quot;video_url&quot;: {&quot;url&quot;:&quot;https://xxxx.mp4&quot;},&quot;max_pixels&quot;: 655360}</code></li><li>输入图像列表时：<code>{&quot;type&quot;: &quot;video&quot;,&quot;video&quot;: [&quot;https://xx1.jpg&quot;,...,&quot;https://xxn.jpg&quot;],&quot;max_pixels&quot;: 655360}</code></li></ul></div></section><p><strong>total_pixels</strong><code>integer</code>（可选）</p><p>视频抽帧后的总像素预算。</p><a id="accordion-最大值"></a><section><p>最大值</p><div><ul><li><strong><code>268435456</code></strong>： <code>qwen4-max</code>, <code>qwen3.8-max</code>、<code>qwen3.8-max-0902</code>。</li><li><strong><code>234881024</code></strong>：<code>qwen3.7-plus</code>、<code>qwen3.7-plus-2026-05-26</code>、<code>qwen3.7-max-2026-06-08</code>。</li><li><strong><code>819200000</code></strong>：<code>qwen3.8-flash</code>、<code>qwen3.8-27b</code>、<code>qwen3.7-flash</code>、<code>qwen3.7-flash-2026-07-15</code>、<code>qwen3.6-flash</code>。</li><li><strong><code>184549376</code></strong>：<code>qwen3.8-omni-flash</code>。</li><li><strong><code>102760448</code></strong>：<code>kimi-k2.5</code>、<code>kimi-k2.6</code>。</li></ul></div></section><a id="accordion-示例值-4"></a><section><p>示例值</p><div><ul><li>输入视频文件时：<code>{&quot;type&quot;: &quot;video_url&quot;,&quot;video_url&quot;: {&quot;url&quot;:&quot;https://xxxx.mp4&quot;},&quot;total_pixels&quot;: 134217728}</code></li><li>输入图像列表时：<code>{&quot;type&quot;: &quot;video&quot;,&quot;video&quot;: [&quot;https://xx1.jpg&quot;,...,&quot;https://xxn.jpg&quot;],&quot;total_pixels&quot;: 134217728}</code></li></ul></div></section><p><strong>prompt_cache_breakpoint</strong> <code>object</code> (可选)</p><p>仅支持 <code>qwen4-max</code>。 指定缓存前缀的结束位置。 详见<a href="../../model-user-guide/model-experience/text-generation-model/explicit-cache-qwen4.md">显式缓存（Qwen4）</a>。</p><a id="accordion-属性-6"></a><section><p>属性</p><div><p><strong>mode</strong> <code>string</code> (必选)</p><p>仅支持 <code>explicit</code>；设置断点时需显式传入。</p></div></section><p><strong>cache_control</strong><code>object</code>（可选）</p><p>用于开启显式缓存。相关文档：<a href="../../model-user-guide/model-experience/text-generation-model/context-cache.md#825f201c5fy6o">显式缓存</a>。</p><a id="accordion-属性-7"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code><strong>（必选）</strong></p><p>仅支持设定为<code>ephemeral</code>。</p></div></section><a id="accordion-属性-qwen4"></a><section><p>属性（Qwen4）</p><div><p>仅支持 <code>qwen4-max</code>。 Qwen4 的内容块缓存标记还支持 <code>ttl</code>，可选 <code>5m</code>、<code>1h</code>，默认为 <code>5m</code>。 详见<a href="../../model-user-guide/model-experience/text-generation-model/explicit-cache-qwen4.md">显式缓存（Qwen4）</a>。</p><p><strong>type</strong> <code>string</code> (必选)</p><p><code>ephemeral</code></p><p><strong>ttl</strong> <code>string</code> (可选)</p><p>缓存有效期，支持 <code>5m</code> 和 <code>1h</code>，默认为 <code>5m</code>。</p></div></section></div></section><p><strong>role</strong><code>string</code><strong>（必选）</strong></p><p>用户消息的角色，固定为<code>user</code>。</p></div></section><p>Assistant Message <code>object</code>（可选）</p><p>模型的回复。通常用于在多轮对话中作为上下文回传给模型。</p><a id="accordion-属性-8"></a><section><p>属性</p><div><p><strong>content</strong><code>string</code>（可选）</p><p>模型回复的文本内容。包含<code>tool_calls</code>时，<code>content</code>可以为空；否则<code>content</code>为必选。</p><p><strong>role</strong><code>string</code><strong>（必选）</strong></p><p>助手消息的角色，固定为<code>assistant</code>。</p><p><strong>encrypted_content</strong> <code>string</code></p><p><code>qwen4-max</code>, <code>thinking_display=&quot;summarized&quot;</code>: 每轮都需传开启参数。客户端只能原样回传密文，不能读取、截断、重新编码、修改或拼接多轮密文。摘要不能替代历史思维链。 <a href="../../model-user-guide/model-experience/text-generation-model/cot-summary.md#multi-turn">思维链摘要与加密</a>. 密文必须原样回传。</p><p><strong>partial</strong><code>boolean</code>（可选）默认值为<code>false</code></p><p>是否开启前缀续写。</p><p>可选值：</p><ul><li>true：开启；</li><li>false：不开启。</li></ul><p>支持的模型参见<a href="../../model-user-guide/model-experience/text-generation-model/partial-mode.md">前缀续写</a>。</p><p><strong>tool_calls</strong> <code>array</code>（可选）</p><p>发起 Function Calling 后，返回的工具与入参信息，包含一个或多个对象。由上一轮模型响应的<code>tool_calls</code>字段获得。</p><a id="accordion-属性-9"></a><section><p>属性</p><div><p><strong>id</strong> <code>string</code><strong>（必选）</strong></p><p>工具响应的ID。</p><p><strong>type</strong> <code>string</code><strong>（必选）</strong></p><p>工具类型，当前只支持设为<code>function</code>。</p><p><strong>function</strong> <code>object</code><strong>（必选）</strong></p><p>工具与入参信息。</p><a id="accordion-属性-10"></a><section><p>属性</p><div><p><strong>name</strong> <code>string</code><strong>（必选）</strong></p><p>工具名称。</p><p><strong>arguments</strong> <code>string</code><strong>（必选）</strong></p><p>入参信息，为JSON格式字符串。</p></div></section><p><strong>index</strong> <code>integer</code><strong>（必选）</strong></p><p>当前工具信息在<code>tool_calls</code>数组中的索引。</p></div></section></div></section><p>Tool Message <code>object</code>（可选）</p><p>工具的输出信息。</p><a id="accordion-属性-11"></a><section><p>属性</p><div><p><strong>content</strong><code>string</code><strong>（必选）</strong></p><p>工具函数的输出内容，必须为字符串。若工具返回结构化数据（如JSON），需将其序列化为字符串。</p><p><strong>role</strong><code>string</code><strong>（必选）</strong></p><p>固定为<code>tool</code>。</p><p><strong>tool_call_id</strong><code>string</code><strong>（必选）</strong></p><p>发起 Function Calling 后返回的 id，通过completion.choices[0].message.tool_calls[$index].id获取，用于标记 Tool Message 对应的工具。</p></div></section></div></section><p><strong>prompt_cache_options</strong> <code>object</code> (可选)</p><p>仅支持 <code>qwen4-max</code>。 请求顶层的缓存配置。 Python SDK 通过 <code>extra_body</code> 传入顶层非标准参数；Node.js SDK 和 curl 直接传入。 详见<a href="../../model-user-guide/model-experience/text-generation-model/explicit-cache-qwen4.md">显式缓存（Qwen4）</a>。</p><a id="accordion-属性-12"></a><section><p>属性</p><div><p><strong>mode</strong> <code>string</code> (可选)</p><p><code>implicit</code>：自动设置缓存断点，无需手动配置。</p><p><code>explicit</code>：不自动设置断点，创建显式缓存需结合手动断点。</p><p><strong>ttl</strong> <code>string</code> (可选)</p><p>缓存有效期，支持 <code>5m</code> 和 <code>1h</code>，默认为 <code>5m</code>。</p><p>对本次请求的全部缓存断点生效。未设置顶层 <code>ttl</code> 时，使用最后一个 <code>cache_control</code> 标记中的 <code>ttl</code>；该标记未设置 <code>ttl</code> 或没有标记时，使用 <code>5m</code>。</p></div></section><p><strong>stream</strong><code>boolean</code>（可选） 默认值为 <code>false</code></p><p>是否以流式输出方式回复。相关文档：<a href="../../model-user-guide/model-experience/text-generation-model/stream.md">流式输出</a></p><p>可选值：</p><ul><li><code>false</code>：模型生成全部内容后一次性返回；</li><li><code>true</code>：边生成边输出，每生成一部分内容即返回一个数据块（chunk）。需实时逐个读取这些块以拼接完整回复。</li></ul><p>推荐设置为<code>true</code>，可提升阅读体验并降低超时风险。</p><div><div><p><strong>说明</strong>非流式调用的最大超时时间不少于300秒，实际时长因部署区域与选用模型存在差异。若超时未完成，服务将中断请求并返回已生成的内容（而非报错）。建议输出较长的场景务必使用流式调用。详情请参见<a href="../../model-user-guide/model-experience/text-generation-model/text-generation.md#11241147efwpm">文本生成模型概述</a>中的超时说明。</p></div></div><p><strong>stream_options</strong><code>object</code>（可选）</p><p>仅用于 <code>stream</code> 为 <code>true</code> 的流式请求。非流式请求不要传入 <code>stream_options</code>。</p><a id="accordion-属性-13"></a><section><p>属性</p><div><p><strong>include_usage</strong><code>boolean</code>（可选）</p><p>流式输出时，最后一个数据块会包含 <code>usage</code>，该数据块的 <code>choices</code> 为空数组。</p></div></section><p><strong>modalities</strong><code>array</code>（可选）默认值为<code>[&quot;text&quot;]</code></p><p>输出数据的模态，仅适用于 Qwen-Omni 模型。相关文档：<a href="../../model-user-guide/model-experience/omni-modal/qwen-omni.md">非实时（Qwen-Omni）</a></p><p>可选值：</p><ul><li><code>[&quot;text&quot;,&quot;audio&quot;]</code>：输出文本与音频，适用于支持音频输出的型号；</li><li><code>[&quot;text&quot;]</code>：仅输出文本。</li></ul><p><code>qwen3.8-omni-flash</code> 仅输出文本。示例见 <a href="../../model-user-guide/model-experience/omni-modal/qwen-omni.md#qwen38-offline">Qwen3.8-Omni-Flash</a>。</p><p><strong>audio</strong><code>object</code>（可选）</p><p>输出音频的音色与格式，适用于支持音频输出的 Qwen-Omni 模型，且<code>modalities</code>参数需为<code>[&quot;text&quot;,&quot;audio&quot;]</code>。相关文档：<a href="../../model-user-guide/model-experience/omni-modal/qwen-omni.md">非实时（Qwen-Omni）</a></p><a id="accordion-属性-14"></a><section><p>属性</p><div><p><strong>voice</strong><code>string</code> <strong>（必选）</strong></p><p>输出音频的音色。请参见<a href="../../model-user-guide/model-experience/omni-modal/qwen-omni.md">非实时（Qwen-Omni）</a>。</p><p><strong>format</strong><code>string</code> <strong>（必选）</strong></p><p>输出音频的格式，仅支持设定为<code>wav</code>。</p></div></section><p><strong>temperature</strong><code>float</code>（可选）</p><p>采样温度，控制模型生成文本的多样性。</p><p>temperature越高，生成的文本更多样，反之，生成的文本更确定。</p><p>取值范围： [0, 2)</p><p>MiniMax/MiniMax-M3.1-Flash 和 MiniMax/MiniMax-M3 固定使用 <code>1.0</code>，不支持自定义；传入其他值时不会生效。</p><p>temperature与top_p均可以控制生成文本的多样性，建议只设置其中一个值。更多说明，请参见<a href="../../model-user-guide/model-experience/text-generation-model/text-generation.md">概述</a>。</p><a id="accordion-temperature默认值"></a><section><p>temperature默认值</p><div><ul><li><p><code>qwen4-max</code>：思考模式为 <code>1.0</code>，非思考模式为 <code>0.7</code>。</p></li><li><p>qwen3.8-max/qwen3.8-flash（思考模式）：视觉理解0.6，文本输入1.0，0.6以下的temperature值会默认改为0.6</p></li><li><p>Qwen3.8-Omni-Flash：思考模式为 0.6，非思考模式为 0.7；</p></li><li><p>Qwen3.8（非思考模式）、Qwen3.7（非思考模式）、Qwen3.6（非思考模式）、Qwen3.5-Omni、Qwen3.5（非思考模式）、Qwen3（非思考模式）、Qwen3-Instruct系列、Qwen3-Coder系列、qwen-max系列、qwen-plus系列（非思考模式）、qwen-flash系列（非思考模式）、qwen开源系列、qwen-coder系列、qwen-doc-turbo、Qwen3-VL（非思考）：0.7；</p></li><li><p>QVQ系列 : 0.5；</p></li><li><p>qwen-audio-turbo系列：0.00001；</p></li><li><p>qwen-vl系列：0.01；</p></li><li><p>qwen-math系列：0；</p></li><li><p>Qwen3.7（思考模式）、Qwen3.6（思考模式）、Qwen3.5（思考模式）、Qwen3（思考模式）、Qwen3-Thinking、Qwen3-Omni-Captioner、QwQ 系列：0.6；</p></li><li><p>qwen-long系列： 1.0；</p></li><li><p>qwen-plus-character：0.92</p></li><li><p>qwen3-omni-flash系列：0.9</p></li><li><p>Qwen3-VL（思考模式）：0.8</p></li><li><p>DeepSeek系列（阿里云直供）：deepseek-v4.1-flash、deepseek-v4-pro: 1.0；deepseek-r1-distill-qwen 蒸馏版: 0.6；</p></li><li><p>DeepSeek系列（硅基流动直供）：siliconflow/deepseek-v3.2、siliconflow/deepseek-v3.1-terminus、siliconflow/deepseek-r1-0528、siliconflow/deepseek-v3-0324: 1.0；</p></li><li><p>DeepSeek系列（快手万擎直供）：vanchin/deepseek-v3.2-think（思考模式）: 0.6；vanchin/deepseek-v3.1-terminus: 0.7；vanchin/deepseek-v3.2-speciale、vanchin/deepseek-r1、vanchin/deepseek-v3、vanchin/deepseek-ocr: 1.0；</p></li><li><p>Kimi系列（阿里云直供）：kimi-k2.7-code、kimi-k2.6（思考模式）、kimi-k2.5（思考模式）: 1.0；kimi-k2.6（非思考模式）、kimi-k2.5（非思考模式）: 0.6；</p></li><li><p>Kimi系列（月之暗面直供）：kimi/kimi-k3、kimi/kimi-k3.1-pro、kimi/kimi-k3.1-pro-highspeed、kimi/kimi-k2.7-code-highspeed、kimi/kimi-k2.7-code、kimi/kimi-k2.6（思考模式）、kimi/kimi-k2.5（思考模式）: 1.0；kimi/kimi-k2.6（非思考模式）、kimi/kimi-k2.5（非思考模式）: 0.6；</p></li><li><p>GLM系列（阿里云直供）：glm-5.1、glm-5: 1.0；</p></li><li><p>GLM系列（智谱直供）：ZHIPU/GLM-5.1、ZHIPU/GLM-5: 0.6；</p></li><li><p>MiniMax系列（阿里云直供）：MiniMax-M2.5: 1.0；</p></li><li><p>MiniMax系列（稀宇科技直供）：MiniMax/MiniMax-M3.1-Flash、MiniMax/MiniMax-M3、MiniMax/MiniMax-M2.7、MiniMax/MiniMax-M2.5、MiniMax/MiniMax-M2.1: 1.0。</p></li><li><p>MiMo系列（小米直供）：mimo-v2.5-pro: 1.0，范围 [0, 1.5]；xiaomi/mimo-v2.6-pro-ultraspeed: 1.0，不支持自定义，传入其他值时仍按 1.0 生效。</p></li></ul></div></section><blockquote><p>不建议修改QVQ模型的默认temperature值 。</p></blockquote><p><strong>top_p</strong><code>float</code>（可选）</p><p>核采样的概率阈值，控制模型生成文本的多样性。</p><p>top_p越高，生成的文本更多样。反之，生成的文本更确定。</p><p>取值范围：（0,1.0]</p><p>MiniMax/MiniMax-M3.1-Flash 和 MiniMax/MiniMax-M3 固定使用 <code>0.95</code>，不支持自定义；传入其他值时不会生效。</p><p>temperature与top_p均可以控制生成文本的多样性，建议只设置其中一个值。更多说明，请参见<a href="../../model-user-guide/model-experience/text-generation-model/text-generation.md">概述</a>。</p><a id="accordion-top-p默认值"></a><section><p>top_p默认值</p><div><ul><li><code>qwen4-max</code>：思考模式为 <code>0.95</code>，非思考模式为 <code>0.8</code>。</li></ul><p>非思考模式下的以下型号（<code>qwen3.8-max</code>、<code>qwen3.8-max-0902</code>、<code>qwen3.8-flash</code>、<code>qwen3.8-2.4t-a95b</code>、<code>qwen3.8-27b</code>）、Qwen3.7（非思考模式）、Qwen3.6（非思考模式）、Qwen3.5-Omni、Qwen3.5（非思考模式）、Qwen3（非思考模式）、Qwen3-Instruct系列、Qwen3-Coder系列、qwen-max系列、qwen-plus系列（非思考模式）、qwen-flash系列（非思考模式）、Qwen 2.5开源系列、qwen-coder系列、qwen-long、qwen-doc-turbo、Qwen3-VL（非思考）：0.8；</p><p>Qwen3.8-Omni-Flash：思考模式为 0.95，非思考模式为 0.8；</p><p>QVQ系列 : 0.5；</p><p>qwen-math系列、Qwen3-Omni-Flash系列：1.0；</p><p>思考模式下的以下型号（<code>qwen3.8-max</code>、<code>qwen3.8-max-0902</code>、<code>qwen3.8-flash</code>、<code>qwen3.8-2.4t-a95b</code>、<code>qwen3.8-27b</code>）、Qwen3.7（思考模式）、Qwen3.6（思考模式）、Qwen3.5（思考模式）、Qwen3（思考模式）、Qwen3-VL（思考模式）、Qwen3-Thinking、QwQ 系列、Qwen3-Omni-Captioner、qwen-plus-character：0.95</p><p>DeepSeek系列（阿里云直供）：deepseek-v4-pro、deepseek-r1-distill-qwen 蒸馏版: 0.95；</p><p>DeepSeek系列（硅基流动直供）：siliconflow/deepseek-v3.2、siliconflow/deepseek-v3.1-terminus、siliconflow/deepseek-r1-0528、siliconflow/deepseek-v3-0324: 1.0；</p><p>DeepSeek系列（快手万擎直供）：vanchin/deepseek-v3.2-think、vanchin/deepseek-v3.1-terminus: 0.95；vanchin/deepseek-v3.2-speciale: 0.9；vanchin/deepseek-r1: 0.8；vanchin/deepseek-v3、vanchin/deepseek-ocr: 1.0；</p><p>Kimi系列（阿里云直供）：kimi-k2.7-code、kimi-k2.6、kimi-k2.5: 0.95；</p><p>Kimi系列（月之暗面直供）：kimi/kimi-k3、kimi/kimi-k3.1-pro、kimi/kimi-k3.1-pro-highspeed、kimi/kimi-k2.7-code-highspeed、kimi/kimi-k2.7-code、kimi/kimi-k2.6、kimi/kimi-k2.5: 0.95；</p><p>GLM系列（阿里云直供）：0.95；</p><p>GLM系列（智谱直供）：ZHIPU/GLM-5.1、ZHIPU/GLM-5: 0.95；</p><p>MiniMax系列（阿里云直供）：MiniMax-M2.5: 0.95；</p><p>MiniMax系列（稀宇科技直供）：MiniMax/MiniMax-M3.1-Flash、MiniMax/MiniMax-M3: 0.95；MiniMax/MiniMax-M2.7、MiniMax/MiniMax-M2.5、MiniMax/MiniMax-M2.1: 0.9。</p><p>MiMo系列（小米直供）：xiaomi/mimo-v2.5-pro: 0.95，范围 [0.01, 1.0]；xiaomi/mimo-v2.6-pro-ultraspeed: 0.95，不支持自定义，传入其他值时仍按 0.95 生效。</p></div></section><blockquote><p>不建议修改QVQ模型的默认 top_p 值。</p></blockquote><p><strong>top_k</strong><code>integer</code> （可选）</p><p>指定生成过程中用于采样的候选 Token 数量。值越大，输出越随机；值越小，输出越确定。若设为 <code>null</code> 或大于 100，则禁用 <code>top_k</code> 策略，仅 <code>top_p</code> 策略生效。取值必须为大于或等于 0 的整数。</p><a id="accordion-top-k默认值"></a><section><p>top_k默认值</p><div><p>QVQ系列：10；</p><p>QwQ 系列：40；</p><p>qwen-math 系列、qwen-audio-turbo系列：1；</p><p>Qwen3-Omni-Flash系列：50；</p><p>其余模型均为20。</p><p>GLM系列（阿里云直供）：20；</p><p>DeepSeek/Kimi/MiniMax系列均不支持top_k参数。</p></div></section><blockquote><p>该参数非OpenAI标准参数。通过 Python SDK调用时，请放入 <strong>extra_body</strong> 对象中。配置方式为：extra_body={&quot;top_k&quot;:xxx}。</p></blockquote><blockquote><p>不建议修改QVQ模型的默认 top_k 值。</p></blockquote><p><strong>repetition_penalty</strong><code>float</code> （可选）</p><p>模型生成时连续序列中的重复度。提高repetition_penalty时可以降低模型生成的重复度，1.0表示不做惩罚。没有严格的取值范围，只要大于0即可。</p><a id="accordion-repetition-penalty默认值"></a><section><p>repetition_penalty默认值</p><div><ul><li><code>qwen4-max</code>、<code>qwen3.8-max</code>、<code>qwen3.8-max-0902</code>、<code>qwen3.8-flash</code>、<code>qwen3.8-2.4t-a95b</code>、<code>qwen3.8-27b</code>、qwen-max、qwen-math系列、qwen-audio-turbo系列、QVQ系列、QwQ系列、Qwen3-VL： 1.0；</li><li>qwen-coder系列、qwen2-1.5b-instruct、qwen2-0.5b-instruct：1.1；</li><li>其余模型为1.05。</li><li>GLM系列（阿里云直供）：1.0；</li><li>Kimi系列（月之暗面直供）：0.0。</li></ul></div></section><blockquote><p>该参数非OpenAI标准参数。通过 Python SDK调用时，请放入 <strong>extra_body</strong> 对象中。配置方式为：extra_body={&quot;repetition_penalty&quot;:xxx}。</p></blockquote><blockquote><p>不建议修改QVQ模型的默认 repetition_penalty 值。</p></blockquote><p><strong>frequency_penalty</strong> <code>float</code> （可选）</p><p>支持 <code>qwen4-max</code>。按 Token 已出现的次数施加惩罚，以调整重复内容的生成。</p><p><strong>presence_penalty</strong> <code>float</code>（可选）</p><p>控制模型生成文本时的内容重复度。</p><p>取值范围：[-2.0, 2.0]。正值降低重复度，负值增加重复度。</p><p>在创意写作或头脑风暴等需要多样性、趣味性或创造力的场景中，建议调高该值；在技术文档或正式文本等强调一致性与术语准确性的场景中，建议调低该值。</p><a id="accordion-presence-penalty默认值"></a><section><p>presence_penalty默认值</p><div><p>非思考模式下的以下型号（<code>qwen4-max</code>、<code>qwen3.8-max</code>、<code>qwen3.8-max-0902</code>、<code>qwen3.8-flash</code>、<code>qwen3.8-2.4t-a95b</code>、<code>qwen3.8-27b</code>）、Qwen3.7（非思考模式）、Qwen3.6（非思考模式）、Qwen3.5-Omni、Qwen3.5（非思考模式）、Qwen3（非思考模式）、Qwen3-Instruct系列/1.7b/4b（思考模式）、QVQ系列、qwen-max、qwen2.5-vl系列、Qwen3-VL（非思考）：1.5；</p><p>Qwen3.8-Omni-Flash：思考模式为 0.0，非思考模式为 1.5；</p><p>qwen-plus/qwen-plus-latest/2025-04-28（思考模式）、qwen-turbo-2025-04-28（思考模式）：0.5；</p><p>其余均为0.0。</p><p>DeepSeek系列（阿里云直供）：deepseek-r1-distill-qwen 蒸馏版: 1；</p><p>Kimi系列（阿里云直供）：kimi-k2.7-code、kimi-k2.6、kimi-k2.5: 0.0；</p><p>Kimi系列（月之暗面直供）：0.0；</p><p>MiniMax系列（阿里云直供）：MiniMax-M2.5: 0.0；</p><p>其余DeepSeek/Kimi/GLM/MiniMax模型无默认值。</p></div></section><a id="accordion-原理介绍"></a><section><p>原理介绍</p><div><p>如果参数值是正数，模型将对目前文本中已存在的Token施加一个惩罚值（惩罚值与文本出现的次数无关），减少这些Token重复出现的几率，从而减少内容重复度，增加用词多样性。</p></div></section><a id="accordion-示例"></a><section><p>示例</p><div><p>提示词：把这句话翻译成中文“This movie is good. The plot is good, the acting is good, the music is good, and overall, the whole movie is just good. It is really good, in fact. The plot is so good, and the acting is so good, and the music is so good.”</p><p>参数值为2.0：这部电影很好。剧情很棒，演技棒，音乐也非常好听，总的来说，整部电影都好得不得了。实际上它真的很优秀。剧情非常精彩，演技出色，音乐也是那么的动听。</p><p>参数值为0.0：这部电影很好。剧情好，演技好，音乐也好，总的来说，整部电影都很好。事实上，它真的很棒。剧情非常好，演技也非常出色，音乐也同样优秀。</p><p>参数值为-2.0：这部电影很好。情节很好，演技很好，音乐也很好，总的来说，整部电影都很好。实际上，它真的很棒。情节非常好，演技也非常好，音乐也非常好。</p></div></section><blockquote><p>不建议修改QVQ模型的默认presence_penalty值。</p></blockquote><p><strong>response_format</strong><code>object</code> （可选） 默认值为<code>{&quot;type&quot;: &quot;text&quot;}</code></p><p>返回内容的格式。可选值：</p><ul><li><code>{&quot;type&quot;: &quot;text&quot;}</code>：输出文字回复；</li><li><code>{&quot;type&quot;: &quot;json_object&quot;}</code>：输出标准格式的JSON字符串。</li><li><code>{&quot;type&quot;: &quot;json_schema&quot;, &quot;json_schema&quot;: {...}}</code>：输出严格符合指定 JSON Schema 的JSON字符串，可精确控制输出结构与字段类型。</li></ul><blockquote><p>相关文档：<a href="../../model-user-guide/model-experience/text-generation-model/qwen-structured-output.md">结构化输出</a>。<code>json_object</code> 与 <code>json_schema</code> 支持的模型不同，参见<a href="../../model-user-guide/model-experience/text-generation-model/qwen-structured-output.md#7a8e438e89xeq">支持的模型</a>。</p></blockquote><blockquote><p>若指定为<code>{&quot;type&quot;: &quot;json_object&quot;}</code>，需在提示词中明确指示模型输出JSON，如：“请按照json格式输出”，否则会报错；若指定为<code>{&quot;type&quot;: &quot;json_schema&quot;, ...}</code>，提示词无需包含 JSON 关键词。</p></blockquote><a id="accordion-属性-15"></a><section><p>属性</p><div><p><strong>type</strong><code>string</code><strong>（必选）</strong></p><p>返回内容的格式。可选值：</p><ul><li><code>text</code>：输出文字回复；</li><li><code>json_object</code>：输出标准格式的JSON字符串；</li><li><code>json_schema</code>：输出严格符合 <code>json_schema</code> 字段所定义结构的JSON字符串。</li></ul><p><strong>json_schema</strong><code>object</code>（可选）</p><p><code>type</code> 为 <code>json_schema</code> 时必须设置，用于定义模型输出需要遵循的 JSON 结构。相关文档：<a href="../../model-user-guide/model-experience/text-generation-model/qwen-structured-output.md#a4f5d7108anxd">获取指定格式的输出</a>。</p><blockquote><p>通过 OpenAI SDK 的 <code>parse</code> 方法调用时，可直接传入 Python Pydantic 类或 Node.js Zod 对象，SDK 会自动将其转换为 JSON Schema，无需手动构造。</p></blockquote><a id="accordion-属性-16"></a><section><p>属性</p><div><p><strong>name</strong><code>string</code><strong>（必选）</strong></p><p>Schema 的名称。</p><p><strong>schema</strong><code>object</code><strong>（必选）</strong></p><p>描述输出结构的 JSON Schema 对象。通过 <code>properties</code> 定义字段结构，通过 <code>required</code> 声明必填字段列表，通过 <code>additionalProperties</code> 控制是否允许输出未在 Schema 中定义的字段（推荐设置为 <code>false</code>，即只输出已定义的字段）。支持的数据类型：string、number、integer、boolean、object、array、enum。相关文档：<a href="../../model-user-guide/model-experience/text-generation-model/qwen-structured-output.md#001cb6ae072tc">配置指南</a>。</p><p><strong>strict</strong><code>boolean</code>（可选）</p><p>是否严格遵循 <code>schema</code> 定义的结构。推荐设置为 <code>true</code>。</p></div></section></div></section><p><strong>max_tokens</strong><code>integer</code> （可选， <strong>即将废弃</strong> ）</p><blockquote><p>该参数即将废弃，新接入请使用 <code>max_completion_tokens</code>。</p></blockquote><p>该参数的含义随模型不同，具体如下：</p><ul><li>qwen4-max、deepseek-v4.1-flash、deepseek-v4-pro、deepseek-v4-pro-0813、deepseek-v4-flash-0731：模型回答与思维链内容之和的最大 Token 数，<code>max_tokens</code> 与 <code>max_completion_tokens</code> 等价。模型输出超过此值时生成将提前停止，返回的 <code>finish_reason</code> 为 <code>length</code>。</li><li>glm-5.3：<code>max_tokens</code> 为模型回答与思维链内容之和的最大 Token 数，模型输出超过此值时生成将提前停止，返回的 <code>finish_reason</code> 为 <code>length</code>。glm-5.3 会忽略 <code>thinking_budget</code> 参数。</li><li>glm-5.2：不传入 <code>thinking_budget</code> 参数时，<code>max_tokens</code> 为模型回答与思维链内容之和的最大 Token 数，模型输出超过此值时生成将提前停止，返回的 <code>finish_reason</code> 为 <code>length</code>；传入 <code>thinking_budget</code> 参数时，<code>max_tokens</code> 仅为模型回答的最大 Token 数，思维链部分的 Token 数由 <code>thinking_budget</code> 单独控制。</li><li>其他模型：模型回答的最大 Token 数（不包含思维链）。若生成内容超过此值，生成将提前停止，返回的 <code>finish_reason</code> 为 <code>length</code>。</li></ul><p>GLM 模型的默认值与最大值如下表所示，其他模型的默认值与最大值均为模型的最大输出长度。</p><table><thead><tr><th>供应方式</th><th>模型</th><th>默认值</th><th>最大值</th></tr></thead><tbody><tr><td>阿里云直供</td><td>glm-5.3、glm-5.2、glm-5.2-fast-preview、glm-5.1、glm-5</td><td>65536</td><td>131072</td></tr><tr><td>智谱直供</td><td>ZHIPU/GLM-5.3、ZHIPU/GLM-5.3-Flash、ZHIPU/GLM-5.3-FlashX、ZHIPU/GLM-5.2、ZHIPU/GLM-5.1、ZHIPU/GLM-5</td><td>65536</td><td>131072</td></tr></tbody></table><p><strong>max_completion_tokens</strong><code>integer</code>（可选）</p><p>模型输出的最大长度，包含思维链和模型回答。模型输出超过此值时生成将提前停止，返回的 <code>finish_reason</code> 为 <code>length</code>。</p><p>GLM 模型的默认值与最大值见 <code>max_tokens</code> 参数中的表格，其他模型的默认值与最大值均为模型的最大输出长度。</p><p>与 <code>max_tokens</code> 的区别：<code>max_completion_tokens</code> 始终限制模型完整输出（思维链 + 回答）；<code>max_tokens</code> 的具体限制范围随模型及 <code>thinking_budget</code> 设置而异，见上文说明。思考类模型推荐使用 <code>max_completion_tokens</code>。</p><p>支持以下模型：</p><ul><li>千问 Max：Qwen3.7-Max 及之后的模型</li><li>千问 Plus：Qwen3.5-Plus 及之后的模型</li><li>千问 Flash：Qwen3.5-Flash 及之后的模型</li><li>Kimi：kimi-k2.5 及其之后推出的Kimi模型</li><li>GLM：上表所列的阿里云直供和智谱直供模型</li><li>MiniMax：MiniMax-M2.5 及之后推出的MiniMax模型</li><li>DeepSeek：deepseek-v4-pro 及之后推出的DeepSeek模型</li></ul><blockquote><p>除上表所列的智谱直供 GLM 模型外，以上模型均不包含其他三方直供模型。</p></blockquote><blockquote><p>实际输出 Token 数与设置的 <code>max_completion_tokens</code> 值之间最多可能存在 10 个 Token 的误差。</p></blockquote><p><strong>vl_high_resolution_images</strong><code>boolean</code>（可选）默认值为<code>false</code></p><p>对 <code>qwen4-max</code>，即使 <code>vl_high_resolution_images=true</code>，显式传入的 <code>max_pixels</code> 仍生效。</p><p>是否将输入图像的像素上限提升至 16384 Token 对应的像素值。相关文档：<a href="../../model-user-guide/model-experience/text-generation-model/vision.md">处理高分辨率图像</a>。</p><ul><li><p><code>vl_high_resolution_images：true</code>，使用固定分辨率策略，忽略 <code>max_pixels</code> 设置，超过此分辨率时会将图像总像素缩小至此上限内。</p><a id="accordion-点击查看各模型像素上限"></a><section><p>点击查看各模型像素上限</p><div><p><code>vl_high_resolution_images</code>为<code>True</code>时，不同模型像素上限不同：</p><ul><li><code>qwen3.8-flash</code>、<code>qwen3.8-omni-flash</code>、Qwen3.7系列、<code>Qwen3.6</code>系列、<code>Qwen3.5</code>系列、<code>Qwen3-VL系列</code>模型：<code>16777216</code>（每<code>Token</code>对应<code>32*32</code>像素，即<code>16384*32*32</code>）</li><li><code>QVQ系列</code>、其他<code>Qwen2.5-VL系列</code>模型：<code>12845056</code>（每<code>Token</code>对应<code>28*28</code>像素，即 <code>16384*28*28</code>）</li></ul></div></section></li><li><p><code>vl_high_resolution_images</code>为<code>false</code>，像素上限由 <code>max_pixels</code> 决定，输入图像的像素超过<code>max_pixels</code>会将图像缩小至<code>max_pixels</code>内。各模型的默认像素上限即<code>max_pixels</code>的默认值。</p></li></ul><blockquote><p>该参数非OpenAI标准参数。通过 Python SDK调用时，请放入 <strong>extra_body</strong> 对象中。配置方式为：extra_body={&quot;vl_high_resolution_images&quot;:xxx}。</p></blockquote><p><strong>n</strong><code>integer</code>（可选） 默认值为1</p><p>生成响应的数量，取值范围是<code>1-4</code>。适用于需生成多个候选响应的场景，例如创意写作或广告文案。</p><blockquote><p><code>n=0</code> 等价于 <code>n=1</code>。</p></blockquote><blockquote><p>仅 <code>qwen4-max</code>、<a href="../../model-user-guide/model-experience/text-generation-model/deep-thinking.md">Qwen3（非思考模式）</a> 和 qwen-plus-character 支持将 <code>n</code> 设为大于 <code>1</code>。MiniMax/MiniMax-M3.1-Flash 和 MiniMax/MiniMax-M3 仅支持 <code>n=1</code>。kimi/kimi-k3.1-pro 和 kimi/kimi-k3.1-pro-highspeed 不支持此参数。</p></blockquote><blockquote><p>若传入 <code>tools</code> 参数， 请将<code>n</code> 设为 1。</p></blockquote><blockquote><p>增大 n 会增加输出 Token 的消耗，但不增加输入 Token 消耗。</p></blockquote><p><strong>enable_thinking</strong> <code>boolean</code> （可选）</p><p>kimi-k3.1-pro（阿里云百炼部署）默认值为 <code>true</code>，可设为 <code>false</code> 关闭思考，但强烈建议保持开启，关闭会显著影响输出效果。</p><p>使用混合思考（回复前既可思考也可不思考）模型时，是否开启思考模式。适用于 Qwen3.8、Qwen3.7、Qwen3.6、Qwen3.5、Qwen3、Qwen3.8-Omni-Flash、Qwen3-Omni-Flash、Qwen3-VL模型，以及 DeepSeek-V4.1-Flash、DeepSeek-V4-Pro/V4-Flash 系列（阿里云直供）、DeepSeek-V3.2/V3.2-exp/V3.1 系列（阿里云直供、硅基流动直供、快手万擎直供）、Kimi-K2.7-code（仅思考模型）、Kimi-K2.6/K2.5 系列（阿里云直供、月之暗面直供）、GLM 系列。DeepSeek-V4 系列默认开启思考，可通过 <code>reasoning_effort</code> 参数调整推理力度。</p><p>可选值：</p><ul><li><p><code>true</code>：开启</p><blockquote><p>开启后，思考内容将通过<code>reasoning_content</code>字段返回。</p></blockquote></li><li><p><code>false</code>：不开启</p></li></ul><p>不同模型的默认值：<a href="../../model-user-guide/model-experience/text-generation-model/deep-thinking.md#78286fdc35hlw">支持的模型</a></p><blockquote><p>该参数非OpenAI标准参数。通过 Python SDK调用时，请放入 <strong>extra_body</strong> 对象中。配置方式为：<code>extra_body={&quot;enable_thinking&quot;: xxx}</code>。</p></blockquote><blockquote><p>若不使用 OpenAI SDK，而是通过 HTTP（如 curl）方式直接调用，则无需 <code>extra_body</code>，直接将 <code>enable_thinking</code> 与 <code>model</code>、<code>messages</code> 等参数一样放在请求体（<code>body</code>）的顶层即可，例如 <code>&quot;enable_thinking&quot;: true</code>。</p></blockquote><blockquote><p>稀宇科技直供的 MiniMax/MiniMax-M3.1-Flash 和 MiniMax/MiniMax-M3 不使用此参数，请使用 <code>thinking</code> 参数。</p></blockquote><p><strong>thinking</strong> <code>object</code> （可选）默认值为 <code>{&quot;type&quot;:&quot;adaptive&quot;}</code></p><p>控制稀宇科技直供 MiniMax 模型的思考模式。</p><p><code>thinking.type</code> 可选值：</p><ul><li><code>adaptive</code>：开启思考。MiniMax/MiniMax-M3.1-Flash 始终使用此模式；MiniMax/MiniMax-M3 默认使用此模式。</li><li><code>disabled</code>：关闭思考，仅 MiniMax/MiniMax-M3 支持。MiniMax/MiniMax-M3.1-Flash 设置此值时返回 400 错误。</li></ul><blockquote><p>该参数非OpenAI标准参数。通过 Python SDK调用时，请放入 <strong>extra_body</strong> 对象中。配置方式为：<code>extra_body={&quot;thinking&quot;: {&quot;type&quot;: &quot;adaptive&quot;}}</code>。</p></blockquote><p><strong>reasoning_split</strong> <code>boolean</code> （可选）</p><p>控制 MiniMax 思考内容的返回位置：</p><ul><li><code>true</code>：通过 <code>reasoning_content</code> 字段单独返回。MiniMax/MiniMax-M3.1-Flash 仅支持此值。</li><li><code>false</code>：在 <code>content</code> 字段中以 <code>&lt;think&gt;</code> 标签返回。仅 MiniMax/MiniMax-M3 支持此值。</li></ul><p>该参数非 OpenAI 标准参数。通过 Python SDK 调用时，请放入 <code>extra_body</code> 对象中，例如 <code>extra_body={&quot;reasoning_split&quot;: True}</code>。</p><p><strong>thinking_display</strong> <code>string</code> （可选）</p><p><code>qwen4-max</code>: <code>&quot;summarized&quot;</code>. <a href="../../model-user-guide/model-experience/text-generation-model/cot-summary.md#enable">思维链摘要与加密</a>.</p><p>默认返回完整思维链。开启本功能后，原始思维链不再以明文返回，改为返回摘要与完整密文。摘要用于展示，密文用于恢复历史思考。</p><p><strong>preserve_thinking</strong> <code>boolean</code> （可选）默认值为 <code>false</code></p><p>是否将对话历史中 assistant 消息的 reasoning_content 拼接至模型输入。适用于需要模型参考历史思考过程的场景。 <code>qwen4-max</code> 的默认值为 <code>true</code>。</p><p>kimi-k3.1-pro 和 kimi-k3（阿里云百炼部署）默认保留客户端传入的历史 <code>reasoning_content</code>。建议在 <code>messages</code> 中完整回传历史 assistant 消息及其 <code>reasoning_content</code>。</p><p>kimi/kimi-k3.1-pro 和 kimi/kimi-k3.1-pro-highspeed 支持此参数，默认关闭。</p><p>需要参考上一轮思考时，将其放在历史 assistant 消息的 <code>reasoning_content</code> 字段中随 <code>messages</code> 回传。用法见<a href="../../model-user-guide/model-experience/text-generation-model/deep-thinking.md#jln7docdq5et5">传递思考过程</a>。</p><p>目前支持qwen4-max、qwen3.8-max、qwen3.8-max-0902、qwen3.8-flash（默认开启）、qwen3.8-omni-flash（默认开启）、qwen3.7-max、qwen3.7-max-2026-05-20以及后续快照、qwen3.7-plus、qwen3.7-plus-2026-05-26、qwen3.6-plus、qwen3.6-plus-2026-04-02、qwen3.7-flash、qwen3.7-flash-2026-07-15、qwen3.6-flash、qwen3.6-flash-2026-04-16、kimi-k2.6（阿里云百炼部署）、kimi-k2.7-code（阿里云百炼部署，默认开启）、kimi/kimi-k2.7-code-highspeed（月之暗面直供，默认开启）、kimi/kimi-k2.7-code（月之暗面直供，默认开启）。</p><blockquote><p><strong>重要：</strong>使用 qwen4-max、qwen3.8-max/qwen3.8-flash 时，preserve_thinking 默认为 true，必须将历史对话中所有的 reasoning_content 完整回传。<strong>不支持将 reasoning_content 拼接到 content 字段中回传。</strong></p></blockquote><ul><li>对于上述支持此参数的 <code>qwen4-max</code>、<code>qwen3.8-max</code>、<code>qwen3.8-max-0902</code>、<code>qwen3.8-flash</code>、Qwen3.7、Qwen3.6 和 Kimi 型号，若历史消息中不包含 <code>reasoning_content</code>，开启此参数不会报错。</li><li>开启后，历史对话中的 reasoning_content 会计入输入 Token 数量并计费。</li></ul><blockquote><p>该参数非OpenAI标准参数。通过 Python SDK调用时，请放入 <strong>extra_body</strong> 对象中。配置方式为：<code>extra_body={&quot;preserve_thinking&quot;: True}</code>。</p></blockquote><p><strong>thinking_budget</strong> <code>integer</code> （可选）</p><p>思考过程的最大 Token 数。适用于 <code>qwen4-max</code>、<code>qwen3.8-max</code>、<code>qwen3.8-max-0902</code>、<code>qwen3.8-flash</code>、<code>qwen3.8-2.4t-a95b</code>、<code>qwen3.8-27b</code>，以及Qwen3.7、Qwen3.6、Qwen3.5、Qwen3-VL、Qwen3、GLM（阿里云直供）、Kimi（阿里云直供）系列模型，其中 kimi-k3.1-pro 和 kimi-k3 不支持该参数。相关文档：<a href="../../model-user-guide/model-experience/text-generation-model/deep-thinking.md#e7c0002fe4meu">限制思考长度</a>。 <code>qwen4-max</code> 的默认值为 <code>131072</code>。</p><p>其他模型: 上述型号的默认值为模型最大思维链长度，请参见：模型列表</p><blockquote><p>该参数非OpenAI标准参数。通过 Python SDK调用时，请放入 <strong>extra_body</strong> 对象中。配置方式为：<code>extra_body={&quot;thinking_budget&quot;: xxx}</code>。</p></blockquote><p><strong>use_multichannel</strong> <code>boolean</code> （可选）</p><p>控制是否解析多通道音频中的空间信息。适用于 <code>qwen3.8-omni-flash</code> 的音频输入，默认为 <code>false</code>，所有音频按单通道解析。设为 <code>true</code> 且输入为双通道（左右）或四通道（FOA，WYZX 顺序）音频时，解析空间音频信息。HTTP 请求中放在请求体顶层；使用 OpenAI Python SDK 时通过 <code>extra_body={&quot;use_multichannel&quot;: True}</code> 传入。</p><p><strong>reasoning_effort</strong> <code>string</code> （可选）</p><p><strong><code>qwen4-max</code></strong></p><p>默认值: <code>reasoning_effort=high</code>.</p><table><thead><tr><th><code>reasoning_effort</code></th><th>实际档位</th></tr></thead><tbody><tr><td><code>minimal</code>, <code>low</code></td><td><code>low</code></td></tr><tr><td><code>medium</code>, <code>high</code></td><td><code>high</code></td></tr><tr><td><code>xhigh</code>, <code>max</code></td><td><code>xhigh</code></td></tr><tr><td><code>none</code></td><td>关闭思考</td></tr></tbody></table><p><code>qwen4-max</code> 不支持同时设置 <code>reasoning_effort</code> 和 <code>thinking_budget</code>。<code>thinking_budget</code> 必须为正整数，不能设为 <code>0</code>。</p><p>仅设置 <code>thinking_budget</code> 时，按下表确定思考档位，保留传入的预算值。</p><table><thead><tr><th><code>thinking_budget</code></th><th>实际档位</th></tr></thead><tbody><tr><td><code>1–4096</code></td><td><code>low</code></td></tr><tr><td><code>4097–131072</code></td><td><code>high</code></td></tr><tr><td><code>131073–262144</code></td><td><code>xhigh</code></td></tr></tbody></table><p>两者均未设置时，使用 <code>high</code> 和 <code>131072</code>。</p><p>控制模型的推理力度，不同模型支持的可选值和默认值不同。</p><p><strong>kimi-k3.1-pro（阿里云百炼部署）</strong>（默认值为 <code>max</code>）</p><ul><li><code>max</code>（默认）：深度推理</li><li><code>high</code>：增强推理</li><li><code>medium</code>：中度推理</li><li><code>low</code>：轻度推理</li></ul><p><strong>MiniMax/MiniMax-M3.1-Flash</strong>（默认值为 <code>max</code>）</p><p>可选值按推理力度从低到高依次为 <code>low</code>、<code>medium</code>、<code>high</code>、<code>xhigh</code> 和 <code>max</code>。模型始终开启思考；设置 <code>none</code> 会返回 400 错误。</p><p><strong>DeepSeek-V4、GLM 系列</strong>（默认值为 <code>high</code>）</p><p>可选值：</p><ul><li><code>high</code>：高力度推理</li><li><code>max</code>：最大力度推理</li></ul><p>low和medium映射为high，xhigh映射为max。</p><p>适用于glm-5.2、glm-5.1、glm-5、deepseek-v4-pro（阿里云直供）</p><p><strong>kimi/kimi-k3、kimi/kimi-k3.1-pro、kimi/kimi-k3.1-pro-highspeed（月之暗面直供）</strong>（默认值为 <code>max</code>，仅支持 <code>max</code>）</p><p>可选值：</p><ul><li><code>max</code>：最大力度推理</li></ul><p><strong>glm-5.3、ZHIPU/GLM-5.3、ZHIPU/GLM-5.3-Flash、ZHIPU/GLM-5.3-FlashX 与 kimi-k3（阿里云直供）模型：默认值为</strong><code>max</code></p><p>可选值：</p><ul><li><code>max</code>（默认）：深度推理</li><li><code>high</code>：增强推理</li><li><code>low</code>：轻度推理</li></ul><p>glm-5.3 系列模型始终开启思考，<code>enable_thinking</code> 仅支持 <code>true</code>，传入 <code>false</code> 会导致 API 请求失败；kimi-k3 支持传入 <code>false</code> 关闭思考。</p><p><strong>deepseek-v4-flash-0731 与 deepseek-v4-pro-0813 模型：默认值为</strong><code>high</code></p><p>可选值：</p><ul><li><code>max</code>：最大力度推理</li><li><code>high</code>（默认）：高力度推理</li><li><code>low</code>：低力度推理</li></ul><p>出于兼容性考虑，<code>medium</code> 映射为 high，<code>xhigh</code> 映射为 high。</p><p><strong>deepseek-v4.1-flash 模型：默认值为</strong><code>high</code></p><p>可选值：</p><ul><li><code>max</code>：最大力度推理</li><li><code>high</code>（默认）：高力度推理</li><li><code>low</code>：低力度推理</li></ul><p><code>minimal</code> 映射为 <code>low</code>，<code>medium</code> 和 <code>xhigh</code> 映射为 <code>high</code>，<code>ultra</code> 映射为 <code>max</code>。</p><p><strong><code>qwen3.8-max</code>、<code>qwen3.8-max-0902</code>、<code>qwen3.8-flash</code>、<code>qwen3.8-2.4t-a95b</code>、<code>qwen3.8-27b</code>：默认值为</strong><code>xhigh</code></p><p>可选值：</p><ul><li><code>xhigh</code>（默认）：高力度推理</li><li><code>medium</code>：中力度推理</li><li><code>low</code>：低力度推理</li></ul><p><code>max</code> 映射为 xhigh，<code>high</code> 映射为 xhigh，<code>minimal</code> 映射为 low，<code>none</code> 映射为 enable_thinking=False。</p><blockquote><p>设置上述可选值及映射值以外的值将会报错。</p></blockquote><p><strong>重要：</strong><code>qwen3.8-max</code>、<code>qwen3.8-max-0902</code>、<code>qwen3.8-flash</code>、<code>qwen3.8-2.4t-a95b</code>、<code>qwen3.8-27b</code>不支持 reasoning_effort 与 thinking_budget 同时设置，同时设置会报错。但两者支持互转：</p><ul><li>未设置 thinking_budget 时，reasoning_effort 档位自动映射 thinking_budget：<code>low</code> 对应 4096，<code>medium</code> 对应 16384，<code>xhigh</code> 对应 262144。</li><li>未设置 reasoning_effort 时，thinking_budget 自动映射回 reasoning_effort：0~4096 对应 <code>low</code>，4097~16384 对应 <code>medium</code>，16385~262144 对应 <code>xhigh</code>。</li><li>两者均未设置时，使用默认 thinking_budget（131072），默认 reasoning_effort（xhigh）。</li></ul><strong>Qwen3.8-Omni-Flash</strong><p><code>qwen3.8-omni-flash</code> 默认开启思考，<code>reasoning_effort</code> 默认为 <code>xhigh</code>。Chat Completions 的 <code>reasoning_effort</code> 接受 <code>none</code>、<code>minimal</code>、<code>low</code>、<code>medium</code>、<code>high</code>、<code>xhigh</code>、<code>max</code>，不能与 <code>thinking_budget</code> 同时设置。参数位置及示例见<a href="../../model-user-guide/model-experience/omni-modal/qwen-omni.md#qwen38-offline">Qwen3.8 Omni</a>。</p><p>可直接选择 <code>low</code>、<code>medium</code>、<code>xhigh</code> 三档思考力度。兼容取值中，<code>minimal</code> 映射为 <code>low</code>，<code>high</code> 和 <code>max</code> 映射为 <code>xhigh</code>，<code>none</code> 表示关闭思考。</p><p><strong>tool_stream</strong> <code>boolean</code> （可选）默认值为 <code>false</code></p><p>仅在<code>stream=true</code>时生效。当前仅Qwen和GLM系列支持。</p><strong>Qwen系列支持列表：</strong><ul><li>qwen-max系列：qwen4-max、qwen3.8-max系列、qwen3.7-max系列的文本模态</li><li>qwen-plus系列：qwen3.7-plus系列、qwen3.6-plus系列的文本模态，以及qwen3.5-plus系列的全模态</li><li>qwen-flash系列：qwen3.8-flash系列、qwen3.7-flash系列、qwen3.6-flash系列、qwen3.5-flash系列的全模态</li></ul><strong>Qwen系列使用参考：</strong><p>tool_stream仅影响复杂工具参数的情况。普通工具参数只要开启<code>stream=true</code>就会流式输出。复杂工具是指工具定义中某些参数类型为array或object。</p><ul><li><code>tool_stream=false</code>：复杂工具参数会一次性输出，默认行为，复杂格式会更准确。</li><li><code>tool_stream=true</code>：复杂工具参数会流式输出，复杂格式没有超时风险。</li></ul><p><strong>GLM系列支持列表：</strong>glm-5、glm-5.1（阿里云直供）。</p><strong>GLM系列使用参考：</strong><ul><li><code>tool_stream=false</code>：工具参数会一次性输出，默认行为，复杂格式会更准确。</li><li><code>tool_stream=true</code>：工具参数会流式输出，复杂格式没有超时风险。</li></ul><blockquote><p>该参数非OpenAI标准参数。通过 Python SDK调用时，请放入 <strong>extra_body</strong> 对象中。配置方式为：<code>extra_body={&quot;tool_stream&quot;: true}</code>。</p></blockquote><p><strong>enable_code_interpreter</strong> <code>boolean</code> （可选）默认值为 <code>false</code></p><p>是否开启代码解释器功能。相关文档：<a href="../../model-user-guide/model-experience/text-generation-model/tool-calls/qwen-code-interpreter.md">代码解释器</a></p><p>可选值：</p><ul><li><code>true</code>：开启</li><li><code>false</code>：不开启</li></ul><blockquote><p>该参数非OpenAI标准参数。通过 Python SDK调用时，请放入 <strong>extra_body</strong> 对象中。配置方式为：<code>extra_body={&quot;enable_code_interpreter&quot;: xxx}</code>。</p></blockquote><p><strong>seed</strong><code>integer</code>（可选）</p><p>随机数种子。用于确保在相同输入和参数下生成结果可复现。若调用时传入相同的 <code>seed</code> 且其他参数不变，模型将尽可能返回相同结果。</p><p>取值范围：<code>[0,2 31 −1]</code>。</p><a id="accordion-seed默认值"></a><section><p>seed默认值</p><div><p>其余模型均为1234。</p></div></section><p><strong>logprobs</strong> <code>boolean</code> （可选）默认值为 <code>false</code></p><p>是否返回输出 Token 的对数概率，可选值：</p><ul><li><p><code>true</code></p><p>返回</p></li><li><p><code>false</code></p><p>不返回</p></li></ul><blockquote><p>思考阶段生成的内容（<code>reasoning_content</code>）不会返回对数概率。</p></blockquote><a id="accordion-支持的模型"></a><section><p>支持的模型</p><div><ul><li><p>qwen-plus系列的快照模型（不包含稳定版模型）</p></li><li><p>qwen3-vl-plus系列模型（包含稳定版模型）</p></li><li><p>Qwen3 开源模型</p></li><li><p><code>qwen4-max</code></p></li></ul></div></section><p><strong>top_logprobs</strong> <code>integer</code> （可选）默认值为0</p><p>指定在每一步生成时，返回模型最大概率的候选 Token 个数。</p><p>取值范围：[0,5]</p><p>仅当 <code>logprobs</code> 为 <code>true</code> 时生效。</p><p><strong>stop</strong><code>string 或 array</code>（可选）</p><p>用于指定停止词。当模型生成的文本中出现 <code>stop</code> 指定的字符串或 <code>token_id</code> 时，生成将立即终止。</p><blockquote><p>MiniMax/MiniMax-M3.1-Flash 不支持此参数。传入后不会按指定停止词截断输出；请求可能仍成功且返回 <code>finish_reason: &quot;stop&quot;</code>，但这不表示指定停止词已生效。</p></blockquote><p>可传入敏感词以控制模型的输出。</p><blockquote><p>stop为数组时，不可将<code>token_id</code>和字符串同时作为元素输入，比如不可以指定为<code>[&quot;你好&quot;,104307]</code>。</p></blockquote><p><strong>tools</strong><code>array</code>（可选）</p><p>包含一个或多个工具对象的数组，供模型在 Function Calling 中调用。相关文档：<a href="../../model-user-guide/model-experience/text-generation-model/tool-calls/qwen-function-calling.md">Function Calling</a></p><p>设置 tools 且模型判断需要调用工具时，响应会通过 tool_calls 返回工具信息。</p><a id="accordion-属性-17"></a><section><p>属性</p><div><p><strong>type</strong><code>string</code><strong>（必选）</strong></p><p>工具类型，当前仅支持设为<code>function</code>。</p><p><strong>function</strong><code>object</code><strong>（必选）</strong></p><a id="accordion-属性-18"></a><section><p>属性</p><div><p><strong>name</strong><code>string</code><strong>（必选）</strong></p><p>工具名称。仅允许字母、数字、下划线（<code>_</code>）和短划线（<code>-</code>），最长 64 个 Token。</p><p><strong>description</strong><code>string</code><strong>（必选）</strong></p><p>工具描述信息，帮助模型判断何时以及如何调用该工具。</p><p><strong>parameters</strong><code>object</code>（可选）默认值为 <code>{}</code></p><p>工具的参数描述，需要是一个合法的JSON Schema。JSON Schema的描述可以见<a href="https://json-schema.org/understanding-json-schema">链接</a>。若<code>parameters</code>参数为空，表示该工具没有入参（如时间查询工具）。</p><blockquote><p>为提高工具调用的准确性，建议传入 <code>parameters</code>。</p></blockquote></div></section></div></section><p><strong>tool_choice</strong> <code>string 或 object</code>（可选）默认值为 <code>auto</code></p><p>工具选择策略。若需对某类问题强制指定工具调用方式（例如始终使用某工具或禁用所有工具），可设置此参数。</p><blockquote><p>MiniMax/MiniMax-M3.1-Flash 仅支持 <code>auto</code>。<code>none</code>、<code>required</code> 或指定函数名称等其他取值可能报错或不生效；指定函数名称不能保证模型调用该函数。</p></blockquote><p><code>deepseek-v4.1-flash-1017</code> 支持将 <code>tool_choice</code> 设为 <code>auto</code>、<code>none</code>、<code>required</code> 或指定函数名称。</p><p>可选值：</p><ul><li><p><code>auto</code></p><p>大模型自主选择工具策略。</p></li><li><p><code>none</code></p><p>若不希望进行工具调用，可设定<code>tool_choice</code>参数为<code>none</code>；</p></li><li><p><code>required</code></p><p>若希望强制调用至少一个工具，可设定<code>tool_choice</code>参数为<code>required</code>，模型将始终返回工具调用信息。</p><blockquote><p>Qwen 系列模型暂不支持<code>required</code>：非思考模式下无法保证一定调用工具，思考模式下当前不支持<code>required</code>。</p></blockquote></li><li><p><code>{&quot;type&quot;: &quot;function&quot;, &quot;function&quot;: {&quot;name&quot;: &quot;the_function_to_call&quot;}}</code></p><p>若希望强制调用某个工具，可设定<code>tool_choice</code>参数为<code>{&quot;type&quot;: &quot;function&quot;, &quot;function&quot;: {&quot;name&quot;: &quot;the_function_to_call&quot;}}</code>，其中<code>the_function_to_call</code>是指定的工具函数名称。</p><blockquote><p>思考模式的模型不支持强制调用某个工具。</p></blockquote></li></ul><p><strong>parallel_tool_calls</strong> <code>boolean</code> （可选）默认值为 <code>true</code></p><p>是否开启并行工具调用。相关文档：<a href="../../model-user-guide/model-experience/text-generation-model/tool-calls/qwen-function-calling.md#cb6b5c484bt4x">并行工具调用</a></p><blockquote><p>MiniMax/MiniMax-M3.1-Flash、kimi-k3 不支持通过此参数控制工具调用的并行性。设置为 <code>false</code> 也不能保证串行调用，模型仍可能在一轮中返回多个 <code>tool_calls</code>。请按实际返回结果处理。</p></blockquote><blockquote><p>kimi/kimi-k3.1-pro 和 kimi/kimi-k3.1-pro-highspeed 不支持此参数。</p></blockquote><p>可选值：</p><ul><li><code>true</code>：开启</li><li><code>false</code>：不开启</li></ul><p><strong>enable_search</strong> <code>boolean</code>（可选）默认值为 <code>false</code></p><p>是否开启联网搜索。kimi-k3.1-pro（阿里云百炼部署）支持此参数，适用于北京、新加坡、美国（弗吉尼亚）、德国（法兰克福）、日本（东京）和中国香港。相关文档：<a href="../../model-user-guide/model-experience/text-generation-model/tool-calls/web-search.md">联网搜索</a></p><p>可选值：</p><ul><li><p><code>true</code>：开启；</p><blockquote><p>若开启后未联网搜索，可优化提示词，或设置<code>search_options</code>中的<code>forced_search</code>参数开启强制搜索。</p></blockquote></li><li><p><code>false</code>：不开启。</p></li></ul><blockquote><p>启用互联网搜索功能可能会增加 Token 的消耗。</p></blockquote><blockquote><p>该参数非OpenAI标准参数。通过 Python SDK调用时，请放入 <strong>extra_body</strong> 对象中。配置方式为：<code>extra_body={&quot;enable_search&quot;: True}</code>。</p></blockquote><p><strong>search_options</strong><code>object</code>（可选）</p><p>联网搜索的策略。相关文档：<a href="../../model-user-guide/model-experience/text-generation-model/tool-calls/web-search.md">联网搜索</a></p><a id="accordion-属性-19"></a><section><p>属性</p><div><p><strong>forced_search</strong> <code>boolean</code>（可选）默认值为<code>false</code></p><p>是否强制开启联网搜索，仅当<code>enable_search</code>为<code>true</code>时生效。</p><p>可选值：</p><ul><li>true：强制开启；</li><li>false：不强制开启，由模型判断是否联网搜索。</li></ul><p><strong>search_strategy</strong> <code>string</code>（可选）默认值为<code>turbo</code></p><p>搜索量级策略，仅当<code>enable_search</code>为<code>true</code>时生效。</p><p><code>qwen3.8-omni-flash</code> 开启联网搜索时，需将此参数设为 <code>agent</code>。</p><p>可选值：</p><ul><li><p><code>turbo</code> （默认）: 兼顾响应速度与搜索效果，适用于大多数场景。</p></li><li><p><code>max</code>: 采用更全面的搜索策略，可调用多源搜索引擎，以获取更详尽的搜索结果，但响应时间可能更长。</p></li><li><p><code>agent</code>：可多次调用联网搜索工具与大模型，实现多轮信息检索与内容整合。</p><blockquote><p>该策略仅适用于 qwen3.5-plus、qwen3.5-plus-2026-02-15、qwen3.5-flash、qwen3.5-flash-2026-02-23、qwen3.8-omni-flash、qwen3.5-omni-plus、qwen3.5-omni-plus-2026-03-15、qwen3.5-omni-flash、qwen3.5-omni-flash-2026-03-15。 <strong>enable_search_extension</strong> <code>boolean</code>（可选）默认值为<code>false</code></p></blockquote></li></ul><p>是否开启垂域搜索，仅当<code>enable_search</code>为<code>true</code>时生效。</p><p>可选值：</p><ul><li><code>true</code>：开启。</li><li><code>false</code>：不开启。</li></ul></div></section><blockquote><p>该参数非OpenAI标准参数。通过 Python SDK调用时，请放入 <strong>extra_body</strong> 对象中。配置方式为：<code>extra_body={&quot;search_options&quot;: xxx}</code>。</p></blockquote><p><strong>include_tool_usage</strong> <code>boolean</code>（可选）默认值为 <code>false</code></p><p>是否在响应的<code>usage</code>中返回联网搜索的调用统计。</p><p>可选值：</p><ul><li><code>true</code>：在<code>usage</code>中返回<code>x_tools</code>字段。</li><li><code>false</code>：不返回。</li></ul><blockquote><p><code>x_tools</code>仅在本次请求实际触发了联网搜索时返回。若未开启<code>enable_search</code>，或模型自行判断无需联网搜索，即使将本参数设为<code>true</code>也不会返回该字段。</p></blockquote><blockquote><p>该参数非OpenAI标准参数。通过 Python SDK调用时，请放入 <strong>extra_body</strong> 对象中。配置方式为：<code>extra_body={&quot;include_tool_usage&quot;: True}</code>。</p></blockquote><p><strong>X-DashScope-DataInspection</strong><code>string</code> （可选）</p><p>在千问 API 的内容安全能力基础上，是否进一步识别输入输出内容的违规信息。取值如下：</p><ul><li><code>'{&quot;input&quot;:&quot;cip&quot;,&quot;output&quot;:&quot;cip&quot;}'</code>：进一步识别；</li><li>不设置该参数：不进一步识别。</li></ul><p>通过 HTTP 调用时请放入请求头：<code>-H &quot;X-DashScope-DataInspection: {\&quot;input\&quot;: \&quot;cip\&quot;, \&quot;output\&quot;: \&quot;cip\&quot;}&quot;</code>；</p><p>通过 Python SDK 调用时请通过<code>extra_headers</code>配置：<code>extra_headers={'X-DashScope-DataInspection': '{&quot;input&quot;:&quot;cip&quot;,&quot;output&quot;:&quot;cip&quot;}'}</code>。</p><p>详细使用方法请参见<a href="../../model-user-guide/security-and-compliance/content-security.md">输入输出 AI 安全护栏</a>；若不想修改调用代码，可通过<a href="../../model-user-guide/security-and-compliance/content-security.md#h2-workspace-switch">业务空间维度开关</a>启用护栏。</p><blockquote><p>不支持通过 Node.js SDK设置。</p></blockquote><p><strong>skill</strong><code>array</code>（可选）</p><p>技能参数，用于启用特定生成技能（如PPT生成）。仅<code>qwen-doc-turbo</code>模型支持。详细用法请参见<a href="../../model-user-guide/model-experience/text-generation-model/specialized-models/data-mining-qwen-doc.md#f6a7b8c9d0pp1">生成PPT</a>。</p><blockquote><p>该参数非OpenAI标准参数。通过 Python SDK调用时，请放入 <strong>extra_body</strong> 对象中。配置方式为：<code>extra_body={&quot;skill&quot;: [...]}</code>。</p></blockquote><blockquote><p>使用 <strong>skill 时，stream</strong> 必须设置为 <strong>true</strong>。</p></blockquote><a id="accordion-属性-20"></a><section><p>属性</p><div><p><strong>type</strong><code>string</code><strong>（必选）</strong></p><p>技能类型。当前支持：</p><ul><li><code>ppt</code>：PPT生成。</li></ul><p><strong>mode</strong><code>string</code> （可选）</p><p>PPT生成模式。可选值：</p><ul><li><code>general</code> （默认值）：模板模式，需配合<code>template_id</code> 使用，生成HTML格式的PPT。</li><li><code>creative</code> ：创意模式，无需模板，生成图版PPT（每页为图片）。</li></ul><p><strong>template_id</strong><code>string</code>（可选）</p><p>PPT模板ID。与<code>mode</code>为<code>general</code>或未设置<code>mode</code>时配合使用。可选值：</p><ul><li><code>news_01</code>：新闻模板</li><li><code>summary_01</code>：总结模板</li><li><code>internet_01</code>：互联网模板</li><li><code>thesis_01</code>：论文模板</li></ul></div></section><p><strong>clear_thinking</strong><code>boolean</code>（可选）默认值为false</p><p>用于控制多轮对话中是否将历史轮次的 <code>reasoning_content</code>（思考过程）作为上下文输入给模型。仅 GLM 系列glm-5.3、glm-5.2、glm-5.1、glm-5模型支持。其中 glm-5.3 的默认值为 <code>true</code>，其余模型的默认值为 <code>false</code>。</p><blockquote><p>该参数非OpenAI标准参数。通过 Python SDK调用时，请放入 <strong>extra_body</strong> 对象中。配置方式为：<code>extra_body={&quot;enable_thinking&quot;: True,&quot;clear_thinking&quot;: True}</code>。</p></blockquote><ul><li><code>true</code>：忽略历史轮次的 <code>reasoning_content</code>，仅使用可见文本、工具调用与结果等非推理内容作为上下文输入，可降低上下文长度与成本。</li><li><code>false</code>（默认）：保留历史轮次的 <code>reasoning_content</code> 并随上下文一同提供给模型。若希望启用 Preserved Thinking，必须在 messages 中完整、未修改、按原顺序透传历史 <code>reasoning_content</code>，缺失、裁剪、改写或重排会导致效果下降或无法生效。</li></ul></td><td><div><a id="sec-tabs-2"></a><section><a id="文本输入"></a><section><a id="文本输入-h4"></a><h4>文本输入</h4><a id="fig-code-group"></a><div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    base_url=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;,
)

completion = client.chat.completions.create(
    # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    model=&quot;qwen4-max&quot;,
    messages=[
        {&quot;role&quot;: &quot;system&quot;, &quot;content&quot;: &quot;You are a helpful assistant.&quot;},
        {&quot;role&quot;: &quot;user&quot;, &quot;content&quot;: &quot;你是谁？&quot;},
    ]
)
print(completion.model_dump_json())
</code></pre></div><a id="fig-code-group-java-tab"></a>Java<div><a id="code-code-group-java"></a><pre class="language-java"><code>// 该代码 OpenAI SDK 版本为 2.6.0
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.chat.completions.ChatCompletion;
import com.openai.models.chat.completions.ChatCompletionCreateParams;

public class Main {
    public static void main(String[] args) {
        OpenAIClient client = OpenAIOkHttpClient.builder()
                .apiKey(System.getenv(&quot;DASHSCOPE_API_KEY&quot;))
                .baseUrl(&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;)
                .build();

        ChatCompletionCreateParams params = ChatCompletionCreateParams.builder()
                .addUserMessage(&quot;你是谁&quot;)
                .model(&quot;qwen4-max&quot;)
                .build();

        try {
            ChatCompletion chatCompletion = client.chat().completions().create(params);
            System.out.println(chatCompletion);
        } catch (Exception e) {
            System.err.println(&quot;Error occurred: &quot; + e.getMessage());
            e.printStackTrace();
        }
    }
}
</code></pre></div><a id="fig-code-group-node-js-tab"></a>Node.js<div><a id="code-code-group-node-js"></a><pre class="language-javascript"><code>import OpenAI from &quot;openai&quot;;

const openai = new OpenAI(
    {
        // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: &quot;sk-xxx&quot;,
        apiKey: process.env.DASHSCOPE_API_KEY,
        baseURL: &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;
    }
);

async function main() {
    const completion = await openai.chat.completions.create({
        model: &quot;qwen4-max&quot;,  //此处以qwen4-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        messages: [
            { role: &quot;system&quot;, content: &quot;You are a helpful assistant.&quot; },
            { role: &quot;user&quot;, content: &quot;你是谁？&quot; }
        ],
    });
    console.log(JSON.stringify(completion))
}

main();
</code></pre></div><a id="fig-code-group-go-tab"></a>Go<div><a id="code-code-group-go"></a><pre class="language-go"><code>package main

import (
	&quot;context&quot;
	&quot;os&quot;

	&quot;github.com/openai/openai-go&quot;
	&quot;github.com/openai/openai-go/option&quot;
)

func main() {
	client := openai.NewClient(
		option.WithAPIKey(os.Getenv(&quot;DASHSCOPE_API_KEY&quot;)),
		option.WithBaseURL(&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;),
	)
	chatCompletion, err := client.Chat.Completions.New(
		context.TODO(), openai.ChatCompletionNewParams{
			Messages: []openai.ChatCompletionMessageParamUnion{
				openai.UserMessage(&quot;你是谁&quot;),
			},
			Model: &quot;qwen4-max&quot;,
		},
	)

	if err != nil {
		panic(err.Error())
	}

	println(chatCompletion.Choices[0].Message.Content)
}
</code></pre></div><a id="fig-code-group-c-http-tab"></a>C#（HTTP）<div><a id="code-code-group-c-http"></a><pre class="language-csharp"><code>using System.Net.Http.Headers;
using System.Text;

class Program
{
    private static readonly HttpClient httpClient = new HttpClient();

    static async Task Main(string[] args)
    {
        // 若没有配置环境变量，请用百炼API Key将下行替换为：string? apiKey = &quot;sk-xxx&quot;;
        string? apiKey = Environment.GetEnvironmentVariable(&quot;DASHSCOPE_API_KEY&quot;);

        if (string.IsNullOrEmpty(apiKey))
        {
            Console.WriteLine(&quot;API Key 未设置。请确保环境变量 'DASHSCOPE_API_KEY' 已设置。&quot;);
            return;
        }

        // 设置请求 URL 和内容
        string url = &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions&quot;;
        // 此处以qwen4-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        string jsonContent = @&quot;{
            &quot;&quot;model&quot;&quot;: &quot;&quot;qwen4-max&quot;&quot;,
            &quot;&quot;messages&quot;&quot;: [
                {
                    &quot;&quot;role&quot;&quot;: &quot;&quot;system&quot;&quot;,
                    &quot;&quot;content&quot;&quot;: &quot;&quot;You are a helpful assistant.&quot;&quot;
                },
                {
                    &quot;&quot;role&quot;&quot;: &quot;&quot;user&quot;&quot;,
                    &quot;&quot;content&quot;&quot;: &quot;&quot;你是谁？&quot;&quot;
                }
            ]
        }&quot;;

        // 发送请求并获取响应
        string result = await SendPostRequestAsync(url, jsonContent, apiKey);

        // 输出结果
        Console.WriteLine(result);
    }

    private static async Task&lt;string&gt; SendPostRequestAsync(string url, string jsonContent, string apiKey)
    {
        using (var content = new StringContent(jsonContent, Encoding.UTF8, &quot;application/json&quot;))
        {
            // 设置请求头
            httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue(&quot;Bearer&quot;, apiKey);
            httpClient.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue(&quot;application/json&quot;));

            // 发送请求并获取响应
            HttpResponseMessage response = await httpClient.PostAsync(url, content);

            // 处理响应
            if (response.IsSuccessStatusCode)
            {
                return await response.Content.ReadAsStringAsync();
            }
            else
            {
                return $&quot;请求失败: {response.StatusCode}&quot;;
            }
        }
    }
}
</code></pre></div><a id="fig-code-group-php-http-tab"></a>PHP（HTTP）<div><a id="code-code-group-php-http"></a><pre class="language-php"><code>&lt;?php
// 设置请求的URL
$url = 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions';
// 若没有配置环境变量，请用百炼API Key将下行替换为：$apiKey = &quot;sk-xxx&quot;;
$apiKey = getenv('DASHSCOPE_API_KEY');
// 设置请求头
$headers = [
    'Authorization: Bearer '.$apiKey,
    'Content-Type: application/json'
];
// 设置请求体
$data = [
    // 此处以qwen4-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    &quot;model&quot; =&gt; &quot;qwen4-max&quot;,
    &quot;messages&quot; =&gt; [
        [
            &quot;role&quot; =&gt; &quot;system&quot;,
            &quot;content&quot; =&gt; &quot;You are a helpful assistant.&quot;
        ],
        [
            &quot;role&quot; =&gt; &quot;user&quot;,
            &quot;content&quot; =&gt; &quot;你是谁？&quot;
        ]
    ]
];
// 初始化cURL会话
$ch = curl_init();
// 设置cURL选项
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
// 执行cURL会话
$response = curl_exec($ch);
// 检查是否有错误发生
if (curl_errno($ch)) {
    echo 'Curl error: ' . curl_error($ch);
}
// 关闭cURL资源
curl_close($ch);
// 输出响应结果
echo $response;
?&gt;
</code></pre></div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
-H &quot;Content-Type: application/json&quot; \
-d '{
    &quot;model&quot;: &quot;qwen4-max&quot;,
    &quot;messages&quot;: [
        {
            &quot;role&quot;: &quot;system&quot;,
            &quot;content&quot;: &quot;You are a helpful assistant.&quot;
        },
        {
            &quot;role&quot;: &quot;user&quot;,
            &quot;content&quot;: &quot;你是谁？&quot;
        }
    ]
}'
</code></pre></div></div></section><a id="流式输出"></a><section><a id="流式输出-h4"></a><h4>流式输出</h4><blockquote><p>相关文档：<a href="../../model-user-guide/model-experience/text-generation-model/stream.md">流式输出</a>。</p></blockquote><a id="fig-code-group-2"></a><div><a id="fig-code-group-2-python-tab"></a>Python<div><a id="code-code-group-2-python"></a><pre class="language-python"><code>import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    base_url=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;,
)
completion = client.chat.completions.create(
    model=&quot;qwen4-max&quot;,  # 此处以qwen4-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    messages=[{'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': '你是谁？'}],
    stream=True,
    stream_options={&quot;include_usage&quot;: True}
    )
for chunk in completion:
    print(chunk.model_dump_json())
</code></pre></div><a id="fig-code-group-2-node-js-tab"></a>Node.js<div><a id="code-code-group-2-node-js"></a><pre class="language-javascript"><code>import OpenAI from &quot;openai&quot;;

const openai = new OpenAI(
    {
        // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: &quot;sk-xxx&quot;,
        apiKey: process.env.DASHSCOPE_API_KEY,
        baseURL: &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;
    }
);

async function main() {
    const completion = await openai.chat.completions.create({
        model: &quot;qwen4-max&quot;, // 此处以qwen4-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        messages: [
            {&quot;role&quot;: &quot;system&quot;, &quot;content&quot;: &quot;You are a helpful assistant.&quot;},
            {&quot;role&quot;: &quot;user&quot;, &quot;content&quot;: &quot;你是谁？&quot;}
        ],
        stream: true,
        stream_options: {include_usage: true}
    });
    for await (const chunk of completion) {
        console.log(JSON.stringify(chunk));
    }
}

main();
</code></pre></div><a id="fig-code-group-2-curl-tab"></a>curl<div><a id="code-code-group-2-curl"></a><pre class="language-bash"><code>curl --location &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions&quot; \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header &quot;Content-Type: application/json&quot; \
--data '{
    &quot;model&quot;: &quot;qwen4-max&quot;,
    &quot;messages&quot;: [
        {
            &quot;role&quot;: &quot;system&quot;,
            &quot;content&quot;: &quot;You are a helpful assistant.&quot;
        },
        {
            &quot;role&quot;: &quot;user&quot;,
            &quot;content&quot;: &quot;你是谁？&quot;
        }
    ],
    &quot;stream&quot;:true,
    &quot;stream_options&quot;: {
        &quot;include_usage&quot;: true
    }
}'
</code></pre></div></div></section><a id="图像输入"></a><section><a id="图像输入-h4"></a><h4>图像输入</h4><blockquote><p>相关文档：<a href="../../model-user-guide/model-experience/text-generation-model/vision.md">图像与视频理解</a>。</p></blockquote><a id="fig-code-group-3"></a><div><a id="fig-code-group-3-python-tab"></a>Python<div><a id="code-code-group-3-python"></a><pre class="language-python"><code>import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    base_url=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;,
)
completion = client.chat.completions.create(
    model=&quot;qwen3-vl-plus&quot;,  # 此处以qwen3-vl-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    messages=[{&quot;role&quot;: &quot;user&quot;,&quot;content&quot;: [
            {&quot;type&quot;: &quot;image_url&quot;,
             &quot;image_url&quot;: {&quot;url&quot;: &quot;https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg&quot;}},
            {&quot;type&quot;: &quot;text&quot;, &quot;text&quot;: &quot;这是什么&quot;},
            ]}]
    )
print(completion.model_dump_json())
</code></pre></div><a id="fig-code-group-3-node-js-tab"></a>Node.js<div><a id="code-code-group-3-node-js"></a><pre class="language-javascript"><code>import OpenAI from &quot;openai&quot;;

const openai = new OpenAI(
    {
        // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: &quot;sk-xxx&quot;,
        apiKey: process.env.DASHSCOPE_API_KEY,
        baseURL: &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;
    }
);

async function main() {
    const response = await openai.chat.completions.create({
        model: &quot;qwen3-vl-plus&quot;, // 此处以qwen3-vl-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        messages: [{role: &quot;user&quot;,content: [
            { type: &quot;image_url&quot;,image_url: {&quot;url&quot;: &quot;https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg&quot;}},
            { type: &quot;text&quot;, text: &quot;这是什么？&quot; },
        ]}]
    });
    console.log(JSON.stringify(response));
}

main();
</code></pre></div><a id="fig-code-group-3-curl-tab"></a>curl<div><a id="code-code-group-3-curl"></a><pre class="language-bash"><code>curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
-H 'Content-Type: application/json' \
-d '{
  &quot;model&quot;: &quot;qwen3-vl-plus&quot;,
  &quot;messages&quot;: [{
      &quot;role&quot;: &quot;user&quot;,
      &quot;content&quot;: [
       {&quot;type&quot;: &quot;image_url&quot;,&quot;image_url&quot;: {&quot;url&quot;: &quot;https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg&quot;}},
       {&quot;type&quot;: &quot;text&quot;,&quot;text&quot;: &quot;这是什么&quot;}
       ]}]
}'
</code></pre></div></div></section><a id="视频输入"></a><section><a id="视频输入-h4"></a><h4>视频输入</h4><blockquote><p>以下示例展示了如何将图片列表作为视频输入。如需使用视频文件等其他方式，请参阅“<a href="../../model-user-guide/model-experience/text-generation-model/vision.md#80dbf6ca8fh6s">视觉理解</a>。</p></blockquote><a id="fig-code-group-4"></a><div><a id="fig-code-group-4-python-tab"></a>Python<div><a id="code-code-group-4-python"></a><pre class="language-python"><code>import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    base_url=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;,
)
completion = client.chat.completions.create(
    # 此处以qwen3-vl-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    model=&quot;qwen3-vl-plus&quot;,
    messages=[{
        &quot;role&quot;: &quot;user&quot;,
        &quot;content&quot;: [
            {
                &quot;type&quot;: &quot;video&quot;,
                &quot;video&quot;: [
                    &quot;https://img.alicdn.com/imgextra/i3/O1CN01K3SgGo1eqmlUgeE9b_!!6000000003923-0-tps-3840-2160.jpg&quot;,
                    &quot;https://img.alicdn.com/imgextra/i4/O1CN01BjZvwg1Y23CF5qIRB_!!6000000003000-0-tps-3840-2160.jpg&quot;,
                    &quot;https://img.alicdn.com/imgextra/i4/O1CN01Ib0clU27vTgBdbVLQ_!!6000000007859-0-tps-3840-2160.jpg&quot;,
                    &quot;https://img.alicdn.com/imgextra/i1/O1CN01aygPLW1s3EXCdSN4X_!!6000000005710-0-tps-3840-2160.jpg&quot;]
            },
            {
                &quot;type&quot;: &quot;text&quot;,
                &quot;text&quot;: &quot;描述这个视频的具体过程&quot;
            }]}]
)
print(completion.model_dump_json())
</code></pre></div><a id="fig-code-group-4-node-js-tab"></a>Node.js<div><a id="code-code-group-4-node-js"></a><pre class="language-javascript"><code>// 确保之前在 package.json 中指定了 &quot;type&quot;: &quot;module&quot;
import OpenAI from &quot;openai&quot;;

const openai = new OpenAI({
    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: &quot;sk-xxx&quot;,
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;
});

async function main() {
    const response = await openai.chat.completions.create({
        // 此处以qwen3-vl-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        model: &quot;qwen3-vl-plus&quot;,
        messages: [{
            role: &quot;user&quot;,
            content: [
                {
                    type: &quot;video&quot;,
                    video: [
                        &quot;https://img.alicdn.com/imgextra/i3/O1CN01K3SgGo1eqmlUgeE9b_!!6000000003923-0-tps-3840-2160.jpg&quot;,
                        &quot;https://img.alicdn.com/imgextra/i4/O1CN01BjZvwg1Y23CF5qIRB_!!6000000003000-0-tps-3840-2160.jpg&quot;,
                        &quot;https://img.alicdn.com/imgextra/i4/O1CN01Ib0clU27vTgBdbVLQ_!!6000000007859-0-tps-3840-2160.jpg&quot;,
                        &quot;https://img.alicdn.com/imgextra/i1/O1CN01aygPLW1s3EXCdSN4X_!!6000000005710-0-tps-3840-2160.jpg&quot;
                    ]
                },
                {
                    type: &quot;text&quot;,
                    text: &quot;描述这个视频的具体过程&quot;
                }
        ]}]
    });
    console.log(JSON.stringify(response));
}

main();
</code></pre></div><a id="fig-code-group-4-curl-tab"></a>curl<div><a id="code-code-group-4-curl"></a><pre class="language-bash"><code>curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
-H 'Content-Type: application/json' \
-d '{
    &quot;model&quot;: &quot;qwen3-vl-plus&quot;,
    &quot;messages&quot;: [
        {
            &quot;role&quot;: &quot;user&quot;,
            &quot;content&quot;: [
                {
                    &quot;type&quot;: &quot;video&quot;,
                    &quot;video&quot;: [
                        &quot;https://img.alicdn.com/imgextra/i3/O1CN01K3SgGo1eqmlUgeE9b_!!6000000003923-0-tps-3840-2160.jpg&quot;,
                        &quot;https://img.alicdn.com/imgextra/i4/O1CN01BjZvwg1Y23CF5qIRB_!!6000000003000-0-tps-3840-2160.jpg&quot;,
                        &quot;https://img.alicdn.com/imgextra/i4/O1CN01Ib0clU27vTgBdbVLQ_!!6000000007859-0-tps-3840-2160.jpg&quot;,
                        &quot;https://img.alicdn.com/imgextra/i1/O1CN01aygPLW1s3EXCdSN4X_!!6000000005710-0-tps-3840-2160.jpg&quot;
                    ]
                },
                {
                    &quot;type&quot;: &quot;text&quot;,
                    &quot;text&quot;: &quot;描述这个视频的具体过程&quot;
                }
            ]
        }
    ]
}'
</code></pre></div></div></section><a id="工具调用"></a><section><a id="工具调用-h4"></a><h4>工具调用</h4><blockquote><p>相关文档：<a href="../../model-user-guide/model-experience/text-generation-model/tool-calls/qwen-function-calling.md">Function Calling</a></p></blockquote><div><div><p><strong>说明</strong><strong>模型知识时效性</strong>：大模型基于训练数据生成回复，其知识存在截止时间，无法自动感知当前真实日期。询问当前日期时，模型返回的是训练数据截止时间之前的旧日期，这不是参数配置错误。</p><p>获取当前准确时间的方式：</p><ol><li><strong>Function Calling</strong>：定义 <code>get_current_time</code> 工具，由模型通过函数调用获取实时时间，见下方工具调用示例。</li><li><strong>系统提示词注入</strong>：在系统消息（system role）中注入当前日期，每次调用需动态传入。</li><li><strong>联网搜索</strong>：<code>enable_search</code> 可获取实时资讯，但无法直接获取当前时间。</li></ol></div></div><a id="fig-code-group-5"></a><div><a id="fig-code-group-5-python-tab"></a>Python<div><a id="code-code-group-5-python"></a><pre class="language-python"><code>import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    base_url=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;,  # 填写DashScope SDK的base_url
)

tools = [
    # 工具1 获取当前时刻的时间
    {
        &quot;type&quot;: &quot;function&quot;,
        &quot;function&quot;: {
            &quot;name&quot;: &quot;get_current_time&quot;,
            &quot;description&quot;: &quot;当你想知道现在的时间时非常有用。&quot;,
            &quot;parameters&quot;: {}  # 因为获取当前时间无需输入参数，因此parameters为空字典
        }
    },
    # 工具2 获取指定城市的天气
    {
        &quot;type&quot;: &quot;function&quot;,
        &quot;function&quot;: {
            &quot;name&quot;: &quot;get_current_weather&quot;,
            &quot;description&quot;: &quot;当你想查询指定城市的天气时非常有用。&quot;,
            &quot;parameters&quot;: {
                &quot;type&quot;: &quot;object&quot;,
                &quot;properties&quot;: {
                    # 查询天气时需要提供位置，因此参数设置为location
                    &quot;location&quot;: {
                        &quot;type&quot;: &quot;string&quot;,
                        &quot;description&quot;: &quot;城市或县区，比如北京市、杭州市、余杭区等。&quot;
                    }
                },
                &quot;required&quot;: [&quot;location&quot;]
            }
        }
    }
]
messages = [{&quot;role&quot;: &quot;user&quot;, &quot;content&quot;: &quot;杭州天气怎么样&quot;}]
completion = client.chat.completions.create(
    model=&quot;qwen4-max&quot;,  # 此处以qwen4-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    messages=messages,
    tools=tools
)

print(completion.model_dump_json())
</code></pre></div><a id="fig-code-group-5-node-js-tab"></a>Node.js<div><a id="code-code-group-5-node-js"></a><pre class="language-javascript"><code>import OpenAI from &quot;openai&quot;;

const openai = new OpenAI(
    {
        // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: &quot;sk-xxx&quot;,
        apiKey: process.env.DASHSCOPE_API_KEY,
        baseURL: &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;
    }
);

const messages = [{&quot;role&quot;: &quot;user&quot;, &quot;content&quot;: &quot;杭州天气怎么样&quot;}];
const tools = [
// 工具1 获取当前时刻的时间
{
    &quot;type&quot;: &quot;function&quot;,
    &quot;function&quot;: {
        &quot;name&quot;: &quot;get_current_time&quot;,
        &quot;description&quot;: &quot;当你想知道现在的时间时非常有用。&quot;,
        // 因为获取当前时间无需输入参数，因此parameters为空
        &quot;parameters&quot;: {}
    }
},
// 工具2 获取指定城市的天气
{
    &quot;type&quot;: &quot;function&quot;,
    &quot;function&quot;: {
        &quot;name&quot;: &quot;get_current_weather&quot;,
        &quot;description&quot;: &quot;当你想查询指定城市的天气时非常有用。&quot;,
        &quot;parameters&quot;: {
            &quot;type&quot;: &quot;object&quot;,
            &quot;properties&quot;: {
                // 查询天气时需要提供位置，因此参数设置为location
                &quot;location&quot;: {
                    &quot;type&quot;: &quot;string&quot;,
                    &quot;description&quot;: &quot;城市或县区，比如北京市、杭州市、余杭区等。&quot;
                }
            },
            &quot;required&quot;: [&quot;location&quot;]
        }
    }
}
];

async function main() {
    const response = await openai.chat.completions.create({
        model: &quot;qwen4-max&quot;, // 此处以qwen4-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        messages: messages,
        tools: tools,
    });
    console.log(JSON.stringify(response));
}

main();
</code></pre></div><a id="fig-code-group-5-curl-tab"></a>curl<div><a id="code-code-group-5-curl"></a><pre class="language-bash"><code>curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
-H &quot;Content-Type: application/json&quot; \
-d '{
    &quot;model&quot;: &quot;qwen4-max&quot;,
    &quot;messages&quot;: [
        {
            &quot;role&quot;: &quot;system&quot;,
            &quot;content&quot;: &quot;You are a helpful assistant.&quot;
        },
        {
            &quot;role&quot;: &quot;user&quot;,
            &quot;content&quot;: &quot;杭州天气怎么样&quot;
        }
    ],
    &quot;tools&quot;: [
    {
        &quot;type&quot;: &quot;function&quot;,
        &quot;function&quot;: {
            &quot;name&quot;: &quot;get_current_time&quot;,
            &quot;description&quot;: &quot;当你想知道现在的时间时非常有用。&quot;,
            &quot;parameters&quot;: {}
        }
    },
    {
        &quot;type&quot;: &quot;function&quot;,
        &quot;function&quot;: {
            &quot;name&quot;: &quot;get_current_weather&quot;,
            &quot;description&quot;: &quot;当你想查询指定城市的天气时非常有用。&quot;,
            &quot;parameters&quot;: {
                &quot;type&quot;: &quot;object&quot;,
                &quot;properties&quot;: {
                    &quot;location&quot;:{
                        &quot;type&quot;: &quot;string&quot;,
                        &quot;description&quot;: &quot;城市或县区，比如北京市、杭州市、余杭区等。&quot;
                    }
                },
                &quot;required&quot;: [&quot;location&quot;]
            }
        }
    }
  ]
}'
</code></pre></div></div></section><a id="联网搜索"></a><section><a id="联网搜索-h4"></a><h4>联网搜索</h4><a id="fig-code-group-6"></a><div><a id="fig-code-group-6-python-tab"></a>Python<div><a id="code-code-group-6-python"></a><pre class="language-python"><code>import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    base_url=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;,
)
completion = client.chat.completions.create(
    model=&quot;qwen4-max&quot;,  # 此处以qwen4-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    messages=[
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content': '中国队在巴黎奥运会获得了多少枚金牌'}],
    extra_body={
        &quot;enable_search&quot;: True
    }
    )
print(completion.model_dump_json())
</code></pre></div><a id="fig-code-group-6-node-js-tab"></a>Node.js<div><a id="code-code-group-6-node-js"></a><pre class="language-javascript"><code>import OpenAI from &quot;openai&quot;;

const openai = new OpenAI(
    {
        // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: &quot;sk-xxx&quot;,
        apiKey: process.env.DASHSCOPE_API_KEY,
        baseURL: &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;
    }
);
async function main() {
    const completion = await openai.chat.completions.create({
        model: &quot;qwen4-max&quot;, //此处以qwen4-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        messages: [
            { role: &quot;system&quot;, content: &quot;You are a helpful assistant.&quot; },
            { role: &quot;user&quot;, content: &quot;中国队在巴黎奥运会获得了多少枚金牌&quot; }
        ],
        enable_search:true
    });
    console.log(JSON.stringify(completion))
}

main();
</code></pre></div><a id="fig-code-group-6-curl-tab"></a>curl<div><a id="code-code-group-6-curl"></a><pre class="language-bash"><code>curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
-H &quot;Content-Type: application/json&quot; \
-d '{
    &quot;model&quot;: &quot;qwen4-max&quot;,
    &quot;messages&quot;: [
        {
            &quot;role&quot;: &quot;system&quot;,
            &quot;content&quot;: &quot;You are a helpful assistant.&quot;
        },
        {
            &quot;role&quot;: &quot;user&quot;,
            &quot;content&quot;: &quot;中国队在巴黎奥运会获得了多少枚金牌&quot;
        }
    ],
    &quot;enable_search&quot;: true
}'
</code></pre></div></div></section><a id="异步调用"></a><section><a id="异步调用-h4"></a><h4>异步调用</h4><a id="code-block-3"></a><pre class="language-python"><code>import os
import asyncio
from openai import AsyncOpenAI
import platform

client = AsyncOpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    base_url=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;,
)

async def main():
    response = await client.chat.completions.create(
        messages=[{&quot;role&quot;: &quot;user&quot;, &quot;content&quot;: &quot;你是谁&quot;}],
        model=&quot;qwen4-max&quot;,  # 此处以qwen4-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    )
    print(response.model_dump_json())

if platform.system() == &quot;Windows&quot;:
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
</code></pre></section><a id="文档理解"></a><section><a id="文档理解-h4"></a><h4>文档理解</h4><blockquote><p>当前仅qwen-long模型支持对文档进行分析，详细用法请参见<a href="../../model-user-guide/model-experience/text-generation-model/specialized-models/long-context-qwen-long.md">长上下文（Qwen-Long）</a>。</p></blockquote><a id="fig-code-group-7"></a><div><a id="fig-code-group-7-python-tab"></a>Python<div><a id="code-code-group-7-python"></a><pre class="language-python"><code>import os
from pathlib import Path
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    base_url=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;,
)
file_object = client.files.create(file=Path(&quot;百炼系列手机产品介绍.docx&quot;), purpose=&quot;file-extract&quot;)
completion = client.chat.completions.create(
    model=&quot;qwen-long&quot;,  # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    messages=[
        {'role': 'system', 'content': f'fileid://{file_object.id}'},
        {'role': 'user', 'content': '这篇文章讲了什么？'}
    ]
)
print(completion.model_dump_json())
</code></pre></div><a id="fig-code-group-7-java-tab"></a>Java<div><a id="code-code-group-7-java"></a><pre class="language-java"><code>// 建议OpenAI SDK的版本 &gt;= 0.32.0
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.chat.completions.ChatCompletion;
import com.openai.models.chat.completions.ChatCompletionCreateParams;
import com.openai.models.files.FileCreateParams;
import com.openai.models.files.FileObject;
import com.openai.models.files.FilePurpose;

import java.nio.file.Path;
import java.nio.file.Paths;

public class Main {
    public static void main(String[] args) {
        // 创建客户端，使用环境变量中的API密钥
        OpenAIClient client = OpenAIOkHttpClient.builder()
                .apiKey(System.getenv(&quot;DASHSCOPE_API_KEY&quot;))
                .baseUrl(&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;)
                .build();

        // 设置文件路径
        Path filePath = Paths.get(&quot;百炼系列手机产品介绍.docx&quot;);
        // 创建文件上传参数
        FileCreateParams fileParams = FileCreateParams.builder()
                .file(filePath)
                .purpose(FilePurpose.of(&quot;file-extract&quot;))
                .build();

        // 上传文件
        FileObject fileObject = client.files().create(fileParams);
        String fileId = fileObject.id();

        // 创建聊天请求
        ChatCompletionCreateParams chatParams = ChatCompletionCreateParams.builder()
                .addSystemMessage(&quot;fileid://&quot; + fileId)
                .addUserMessage(&quot;这篇文章讲了什么？&quot;)
                .model(&quot;qwen-long&quot;)
                .build();

        // 发送请求并获取响应
        ChatCompletion chatCompletion = client.chat().completions().create(chatParams);

        // 打印响应结果
        System.out.println(chatCompletion);
    }
}
</code></pre></div><a id="fig-code-group-7-node-js-tab"></a>Node.js<div><a id="code-code-group-7-node-js"></a><pre class="language-javascript"><code>import fs from &quot;fs&quot;;
import OpenAI from &quot;openai&quot;;

const openai = new OpenAI(
    {
        // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: &quot;sk-xxx&quot;,
        apiKey: process.env.DASHSCOPE_API_KEY,
        baseURL: &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;
    }
);

async function getFileID() {
    const fileObject = await openai.files.create({
        file: fs.createReadStream(&quot;百炼系列手机产品介绍.docx&quot;),
        purpose: &quot;file-extract&quot;
    });
    return fileObject.id;
}

async function main() {
    const fileID = await getFileID();
    const completion = await openai.chat.completions.create({
        model: &quot;qwen-long&quot;,  //模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        messages: [
            { role: &quot;system&quot;, content: `fileid://${fileID}`},
            { role: &quot;user&quot;, content: &quot;这篇文章讲了什么？&quot; }
        ],
    });
    console.log(JSON.stringify(completion))
}

main();
</code></pre></div><a id="fig-code-group-7-curl-tab"></a>curl<div><a id="code-code-group-7-curl"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header &quot;Content-Type: application/json&quot; \
--data '{
    &quot;model&quot;: &quot;qwen-long&quot;,
    &quot;messages&quot;: [
        {&quot;role&quot;: &quot;system&quot;,&quot;content&quot;: &quot;You are a helpful assistant.&quot;},
        {&quot;role&quot;: &quot;system&quot;,&quot;content&quot;: &quot;fileid://file-fe-xxx&quot;},
        {&quot;role&quot;: &quot;user&quot;,&quot;content&quot;: &quot;这篇文章讲了什么？&quot;}
    ],
    &quot;stream&quot;: true,
    &quot;stream_options&quot;: {
        &quot;include_usage&quot;: true
    }
}'
</code></pre></div></div></section><a id="ppt生成"></a><section><a id="ppt生成-h4"></a><h4>PPT生成</h4><blockquote><p>当前仅<code>qwen-doc-turbo</code>模型支持PPT生成。详细用法请参见<a href="../../model-user-guide/model-experience/text-generation-model/specialized-models/data-mining-qwen-doc.md#f6a7b8c9d0pp1">生成PPT</a>。</p></blockquote><p>启用 <code>skill</code> 参数生成 PPT 时，仅支持流式输出，需设置 <code>stream: true</code>。</p><a id="fig-code-group-8"></a><div><a id="fig-code-group-8-python-tab"></a>Python<div><a id="code-code-group-8-python"></a><pre class="language-python"><code>import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    base_url=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;,
)

completion = client.chat.completions.create(
    model=&quot;qwen-doc-turbo&quot;,
    messages=[
        {&quot;role&quot;: &quot;system&quot;, &quot;content&quot;: &quot;you are a helpful assistant.&quot;},
        {&quot;role&quot;: &quot;system&quot;, &quot;content&quot;: &quot;您的文档内容&quot;},
        {&quot;role&quot;: &quot;user&quot;, &quot;content&quot;: &quot;生成一个10到20页的ppt&quot;}
    ],
    extra_body={&quot;skill&quot;: [{&quot;type&quot;: &quot;ppt&quot;, &quot;mode&quot;: &quot;general&quot;, &quot;template_id&quot;: &quot;news_01&quot;}]},
    stream=True,
    stream_options={&quot;include_usage&quot;: True}
)

for chunk in completion:
    if chunk.choices and chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end='', flush=True)
</code></pre></div><a id="fig-code-group-8-node-js-tab"></a>Node.js<div><a id="code-code-group-8-node-js"></a><pre class="language-javascript"><code>import OpenAI from &quot;openai&quot;;

const openai = new OpenAI(
    {
        apiKey: process.env.DASHSCOPE_API_KEY,
        baseURL: &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;
    }
);

async function main() {
    const completion = await openai.chat.completions.create({
        model: &quot;qwen-doc-turbo&quot;,
        messages: [
            {&quot;role&quot;: &quot;system&quot;, &quot;content&quot;: &quot;you are a helpful assistant.&quot;},
            {&quot;role&quot;: &quot;system&quot;, &quot;content&quot;: &quot;您的文档内容&quot;},
            {&quot;role&quot;: &quot;user&quot;, &quot;content&quot;: &quot;生成一个10到20页的ppt&quot;}
        ],
        skill: [{&quot;type&quot;: &quot;ppt&quot;, &quot;mode&quot;: &quot;general&quot;, &quot;template_id&quot;: &quot;news_01&quot;}],
        stream: true,
        stream_options: {&quot;include_usage&quot;: true}
    });
    for await (const chunk of completion) {
        if (chunk.choices?.length &gt; 0 &amp;&amp; chunk.choices[0].delta.content) {
            process.stdout.write(chunk.choices[0].delta.content);
        }
    }
}

main();
</code></pre></div><a id="fig-code-group-8-curl-tab"></a>curl<div><a id="code-code-group-8-curl"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header &quot;Content-Type: application/json&quot; \
--data '{
    &quot;model&quot;: &quot;qwen-doc-turbo&quot;,
    &quot;messages&quot;: [
        {
            &quot;role&quot;: &quot;system&quot;,
            &quot;content&quot;: &quot;you are a helpful assistant.&quot;
        },
        {
            &quot;role&quot;: &quot;system&quot;,
            &quot;content&quot;: &quot;您的文档内容&quot;
        },
        {
            &quot;role&quot;: &quot;user&quot;,
            &quot;content&quot;: &quot;生成一个10到20页的ppt&quot;
        }
    ],
    &quot;skill&quot;: [
        {
            &quot;type&quot;: &quot;ppt&quot;,
            &quot;mode&quot;: &quot;general&quot;,
            &quot;template_id&quot;: &quot;news_01&quot;
        }
    ],
    &quot;stream&quot;: true,
    &quot;stream_options&quot;: {
        &quot;include_usage&quot;: true
    }
}'
</code></pre></div></div></section></section></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="cd3063363egdc"></a><h2>chat响应对象（非流式输出）</h2><p><strong>id</strong><code>string</code></p><p>本次调用的唯一标识符。</p><p><strong>choices</strong><code>array</code></p><p>模型生成内容的数组。</p><a id="accordion-属性-21"></a><section><p>属性</p><div><p><strong>finish_reason</strong><code>string</code></p><p>模型停止生成的原因。</p><p>有三种情况：</p><ul><li>触发输入参数中的<code>stop</code>参数，或自然停止输出时为<code>stop</code>；</li><li>生成长度过长而结束为<code>length</code>；</li><li>需要调用工具而结束为<code>tool_calls</code>。</li></ul><p><strong>index</strong><code>integer</code></p><p>当前对象在<code>choices</code>数组中的索引。</p><p><strong>logprobs</strong><code>object</code></p><p>模型输出的 Token 概率信息。</p><a id="accordion-属性-22"></a><section><p>属性</p><div><p><strong>content</strong> <code>array</code></p><p>包含每个 Token 及其对数概率的数组。</p><a id="accordion-属性-23"></a><section><p>属性</p><div><p><strong>token</strong> <code>string</code></p><p>当前 Token 的文本。</p><p><strong>bytes</strong> <code>array</code></p><p>当前 Token 的 UTF‑8 原始字节列表，用于精确还原输出内容（例如表情符号或中文字符）。</p><p><strong>logprob</strong> <code>float</code></p><p>当前 Token 的对数概率。返回值为 <code>null</code> 表示概率值极低。</p><p><strong>top_logprobs</strong> <code>array</code></p><p>当前 Token 位置最可能的若干候选 Token，数量与请求参数<code>top_logprobs</code>保持一致。每个元素包含：</p><a id="accordion-属性-24"></a><section><p>属性</p><div><p><strong>token</strong> <code>string</code></p><p>候选 Token 文本。</p><p><strong>bytes</strong> <code>array</code></p><p>当前 Token 的 UTF‑8 原始字节列表，用于精确还原输出内容（例如表情符号或中文字符）。</p><p><strong>logprob</strong> <code>float</code></p><p>该候选 Token 的对数概率。返回值为 null 表示概率值极低。</p></div></section></div></section></div></section><p><strong>message</strong><code>object</code></p><p>模型输出的消息。</p><a id="accordion-属性-25"></a><section><p>属性</p><div><p><strong>content</strong> <code>string</code></p><p>模型的回复内容。</p><p><strong>encrypted_content</strong> <code>string</code></p><p><code>qwen4-max</code>, <code>thinking_display=&quot;summarized&quot;</code>: 每轮都需传开启参数。客户端只能原样回传密文，不能读取、截断、重新编码、修改或拼接多轮密文。摘要不能替代历史思维链。 <a href="../../model-user-guide/model-experience/text-generation-model/cot-summary.md#multi-turn">思维链摘要与加密</a>.</p><p><strong>reasoning_content</strong> <code>string</code></p><p>模型的思维链内容。</p><p><strong>refusal</strong> <code>string</code></p><p>该参数当前固定为<code>null</code>。</p><p><strong>role</strong> <code>string</code></p><p>消息的角色，固定为<code>assistant</code>。</p><p><strong>audio</strong> <code>object</code></p><p>该参数当前固定为<code>null</code>。</p><p><strong>function_call</strong>（即将废弃）<code>object</code></p><p>该值固定为<code>null</code>，请参考<code>tool_calls</code>参数。</p><p><strong>tool_calls</strong> <code>array</code></p><p>在发起 Function Calling后，模型生成的工具与入参信息。</p><a id="accordion-属性-26"></a><section><p>属性</p><div><p><strong>id</strong> <code>string</code></p><p>本次工具响应的唯一标识符。</p><p><strong>type</strong> <code>string</code></p><p>工具类型，当前只支持<code>function</code>。</p><p><strong>function</strong> <code>object</code></p><p>工具信息。</p><a id="accordion-属性-27"></a><section><p>属性</p><div><p><strong>name</strong> <code>string</code></p><p>工具名称。</p><p><strong>arguments</strong> <code>string</code></p><p>入参信息，为JSON格式字符串。</p><blockquote><p>由于大模型响应有一定随机性，输出的入参信息可能不符合函数签名。请在调用前校验参数有效性</p></blockquote></div></section><p><strong>index</strong> <code>integer</code></p><p>当前工具在<code>tool_calls</code>数组中的索引。</p></div></section></div></section></div></section><p><strong>created</strong><code>integer</code></p><p>请求创建时的 Unix 时间戳（秒）。</p><p><strong>model</strong><code>string</code></p><p>本次请求使用的模型。</p><p><strong>object</strong> <code>string</code></p><p>始终为<code>chat.completion</code>。</p><p><strong>service_tier</strong> <code>string</code></p><p>按量调用时为 <code>null</code>；使用吞吐预留专属模型 code 调用时返回性能档位（<code>ptu_default</code> / <code>ptu_fast</code>），参见<a href="../../model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation.md">吞吐预留概述</a>。</p><p><strong>system_fingerprint</strong><code>string</code></p><p>该参数当前固定为<code>null</code>。</p><p><strong>usage</strong> <code>object</code></p><p>本次请求的 Token 消耗信息。</p><a id="accordion-属性-28"></a><section><p>属性</p><div><p><strong>completion_tokens</strong> <code>integer</code></p><p>模型输出的 Token 数。</p><p><strong>prompt_tokens</strong> <code>integer</code></p><p>输入的 Token 数。<a href="../../model-user-guide/model-experience/text-generation-model/text-generation.md#e710782c79xqy">补充说明</a></p><p><strong>total_tokens</strong> <code>integer</code></p><p>消耗的总 Token 数，为<code>prompt_tokens</code>与<code>completion_tokens</code>的总和。</p><p><strong>completion_tokens_details</strong> <code>object</code>（可选）</p><p>输出 Token 的细粒度分类。部分模型返回该字段。其中 <code>text_tokens</code> 包含 <code>reasoning_tokens</code>——<code>reasoning_tokens</code> 是 <code>text_tokens</code> 中对应思考过程的子集，<code>text_tokens</code> 减去 <code>reasoning_tokens</code> 才是最终可见回复的 Token 数。该字段通常仅在模型输出思考过程时返回，未开启思考时可能为 <code>null</code> 或不返回。</p><a id="accordion-属性-29"></a><section><p>属性</p><div><p><strong>audio_tokens</strong> <code>integer</code>（可选）</p><p>输出的音频 Token 数。</p><p><strong>reasoning_tokens</strong> <code>integer</code>（可选）</p><p>思考过程 Token 数，是 <code>text_tokens</code> 的子集。</p><p><strong>text_tokens</strong> <code>integer</code>（可选）</p><p>输出文本的 Token 数，已包含 <code>reasoning_tokens</code>。</p></div></section><p><strong>prompt_tokens_details</strong> <code>object</code></p><p>输入 Token 的细粒度分类。</p><a id="accordion-属性-30"></a><section><p>属性</p><div><p><strong>audio_tokens</strong> <code>integer</code></p><p>该参数当前固定为<code>null</code>。</p><p><strong>cached_tokens</strong> <code>integer</code></p><p>命中 Cache 的 Token 数。Context Cache 详情请参见<a href="../../model-user-guide/model-experience/text-generation-model/context-cache.md">上下文缓存</a>。</p><p><strong>text_tokens</strong> <code>integer</code></p><p>输入的文本 Token 数。</p><p><strong>image_tokens</strong> <code>integer</code></p><p>输入的图像 Token 数。</p><p><strong>video_tokens</strong> <code>integer</code></p><p>输入的视频文件或者图像列表 Token 数。</p><p><strong>cache_creation</strong> <code>object</code></p><p><a href="../../model-user-guide/model-experience/text-generation-model/context-cache.md#825f201c5fy6o">显式缓存</a>创建信息。</p><a id="accordion-属性-31"></a><section><p>属性</p><div><p><strong>ephemeral_5m_input_tokens</strong> <code>integer</code></p><p>创建显式缓存的 Token 数。</p></div></section><p><strong>cache_creation_input_tokens</strong> <code>integer</code></p><p>创建显式缓存的 Token 数。</p><p><strong>cache_type</strong> <code>string</code></p><p>使用<a href="../../model-user-guide/model-experience/text-generation-model/context-cache.md#825f201c5fy6o">显式缓存</a>时，参数值为<code>ephemeral</code>，否则该参数不存在。</p></div></section><a id="accordion-属性-qwen4-2"></a><section><p>属性（Qwen4）</p><div><p>详见<a href="../../model-user-guide/model-experience/text-generation-model/explicit-cache-qwen4.md">显式缓存（Qwen4）</a>。</p><p><strong>cached_tokens</strong> <code>integer</code></p><p>命中 Cache 的 Token 数。Context Cache 详情请参见<a href="../../model-user-guide/model-experience/text-generation-model/context-cache.md">上下文缓存</a>。</p><p><strong>text_tokens</strong> <code>integer</code></p><p>输入的文本 Token 数。</p><p><strong>image_tokens</strong> <code>integer</code></p><p>输入的图像 Token 数。</p><p><strong>video_tokens</strong> <code>integer</code></p><p>输入的视频文件或者图像列表 Token 数。</p><p><strong>cache_write_tokens</strong> <code>integer</code></p><p>缓存创建的输入 Token 数。</p><p><strong>cache_creation_input_tokens</strong> <code>integer</code></p><p>与 <code>cache_write_tokens</code> 相同，统计时不要重复相加。</p><p><strong>cache_type</strong> <code>string</code></p><p><code>ephemeral</code></p><p><strong>cache_creation</strong> <code>object</code></p><p>按 TTL 统计的缓存创建详情。两种 TTL 的 Token 数之和等于本次创建缓存的 Token 数。</p><a id="accordion-属性-32"></a><section><p>属性</p><div><p><strong>ephemeral_5m_input_tokens</strong> <code>integer</code></p><p>5 分钟缓存创建的 Token 数。</p><p><strong>ephemeral_1h_input_tokens</strong> <code>integer</code></p><p>1 小时缓存创建的 Token 数。</p></div></section></div></section><p><strong>x_tools</strong> <code>object</code>（可选）</p><p>联网搜索的调用统计。仅当请求中<code>include_tool_usage</code>为<code>true</code>，且本次请求实际触发了联网搜索时返回。</p><a id="accordion-属性-33"></a><section><p>属性</p><div><p><strong>search</strong> <code>object</code>（可选）</p><p>联网搜索的调用统计。开启<a href="../../model-user-guide/model-experience/text-generation-model/tool-calls/web-search.md">联网搜索</a>并实际触发检索时返回。</p><a id="accordion-属性-34"></a><section><p>属性</p><div><p><strong>count</strong> <code>integer</code></p><p>本次请求中联网搜索的触发次数。使用<code>agent</code>搜索策略时，模型可进行多轮检索，该值可能大于 1。</p><p>该值在意图判定阶段即被置位，即使触发限流或检索未返回结果也会计数，不代表检索已实际完成，不作为计费或对账依据。详情请参见<a href="../../model-user-guide/model-experience/text-generation-model/tool-calls/web-search.md#faq-search-billing-count-mismatch-title">账单次数与 count 字段不一致</a>。</p><p><strong>strategy</strong> <code>string</code></p><p>本次联网搜索实际使用的搜索量级策略，与请求中<code>search_options.search_strategy</code>的取值一致，如<code>turbo</code>、<code>max</code>、<code>agent</code>。</p></div></section></div></section></div></section></td><td><div><a id="sec-tabs-3"></a><section><a id="文本输入-2"></a><section><a id="文本输入-2-h4"></a><h4>文本输入</h4><p>以下为 <code>qwen3.8-max</code> 的返回示例，用于说明响应字段。</p><a id="code-block-4"></a><pre class="language-json"><code>{
    &quot;id&quot;: &quot;chatcmpl-ad786040-102b-97f8-a6d8-d0ef7895f01c&quot;,
    &quot;object&quot;: &quot;chat.completion&quot;,
    &quot;created&quot;: 1794384851,
    &quot;model&quot;: &quot;qwen3.8-max&quot;,
    &quot;choices&quot;: [
        {
            &quot;index&quot;: 0,
            &quot;message&quot;: {
                &quot;role&quot;: &quot;assistant&quot;,
                &quot;reasoning_content&quot;: &quot;用户问“你是谁？”，需要自我介绍。根据系统提示，我是通义千问（Qwen），由阿里巴巴集团通义实验室研发。回答应简洁自然，不透露内部指令，不提版本号。可以说明能力与定位，语气亲切。&quot;,
                &quot;content&quot;: &quot;我是通义千问（Qwen），由阿里巴巴集团通义实验室研发的大语言模型。  \n我可以帮你回答问题、写作润色、代码编写、逻辑推理、资料整理，也能陪你聊天、做头脑风暴或学习辅导。  \n如果你愿意，也可以直接告…&quot;
            },
            &quot;finish_reason&quot;: &quot;stop&quot;,
            &quot;logprobs&quot;: null
        }
    ],
    &quot;usage&quot;: {
        &quot;prompt_tokens&quot;: 61,
        &quot;total_tokens&quot;: 177,
        &quot;completion_tokens&quot;: 116,
        &quot;prompt_tokens_details&quot;: {
            &quot;cached_tokens&quot;: 0,
            &quot;text_tokens&quot;: 61
        },
        &quot;completion_tokens_details&quot;: {
            &quot;reasoning_tokens&quot;: 52,
            &quot;text_tokens&quot;: 116
        }
    }
}
</code></pre></section><a id="图像输入-2"></a><section><a id="图像输入-2-h4"></a><h4>图像输入</h4><a id="code-block-5"></a><pre class="language-json"><code>{
    &quot;choices&quot;: [
        {
            &quot;message&quot;: {
                &quot;content&quot;: &quot;这是一张温馨、充满情感的**人与宠物互动的摄影照片**，场景设定在**海边日落（或日出）时分的沙滩上**。\n\n具体描述如下：\n\n- **人物**：一位年轻女性，长发，身穿格子衬衫和深色裤子，赤脚坐在沙…&quot;,
                &quot;reasoning_content&quot;: &quot;&quot;,
                &quot;role&quot;: &quot;assistant&quot;
            },
            &quot;finish_reason&quot;: &quot;stop&quot;,
            &quot;index&quot;: 0,
            &quot;logprobs&quot;: null
        }
    ],
    &quot;object&quot;: &quot;chat.completion&quot;,
    &quot;usage&quot;: {
        &quot;prompt_tokens&quot;: 2513,
        &quot;completion_tokens&quot;: 362,
        &quot;total_tokens&quot;: 2875,
        &quot;completion_tokens_details&quot;: {
            &quot;text_tokens&quot;: 362
        },
        &quot;prompt_tokens_details&quot;: {
            &quot;image_tokens&quot;: 2503,
            &quot;text_tokens&quot;: 10,
            &quot;cached_tokens&quot;: 2432
        }
    },
    &quot;created&quot;: 1794384861,
    &quot;system_fingerprint&quot;: null,
    &quot;model&quot;: &quot;qwen3-vl-plus&quot;,
    &quot;id&quot;: &quot;chatcmpl-0c630178-32a5-91a4-9e4a-740f73b1ec5e&quot;
}
</code></pre></section><a id="视频输入-2"></a><section><a id="视频输入-2-h4"></a><h4>视频输入</h4><a id="code-block-6"></a><pre class="language-json"><code>{
    &quot;choices&quot;: [
        {
            &quot;message&quot;: {
                &quot;content&quot;: &quot;这个视频片段展现了一场夜间足球比赛中的关键射门与扑救瞬间，视角独特——**从球门网内向外拍摄**（即“球门视角”），营造出强烈的临场感和紧张氛围。以下是具体过程的分步描述：\n\n---\n\n- **0.0…&quot;,
                &quot;reasoning_content&quot;: &quot;&quot;,
                &quot;role&quot;: &quot;assistant&quot;
            },
            &quot;finish_reason&quot;: &quot;stop&quot;,
            &quot;index&quot;: 0,
            &quot;logprobs&quot;: null
        }
    ],
    &quot;object&quot;: &quot;chat.completion&quot;,
    &quot;usage&quot;: {
        &quot;prompt_tokens&quot;: 1208,
        &quot;completion_tokens&quot;: 756,
        &quot;total_tokens&quot;: 1964,
        &quot;completion_tokens_details&quot;: {
            &quot;text_tokens&quot;: 756
        },
        &quot;prompt_tokens_details&quot;: {
            &quot;text_tokens&quot;: 18,
            &quot;video_tokens&quot;: 1190,
            &quot;cached_tokens&quot;: 0
        }
    },
    &quot;created&quot;: 1794384874,
    &quot;system_fingerprint&quot;: null,
    &quot;model&quot;: &quot;qwen3-vl-plus&quot;,
    &quot;id&quot;: &quot;chatcmpl-4aaa644b-b37d-90df-984c-c138b47bf972&quot;
}
</code></pre></section><a id="工具调用-2"></a><section><a id="工具调用-2-h4"></a><h4>工具调用</h4><p>以下为 <code>qwen3.8-max</code> 的返回示例，用于说明响应字段。</p><a id="code-block-7"></a><pre class="language-json"><code>{
    &quot;id&quot;: &quot;chatcmpl-5cc0b5ec-42bf-99e8-ae83-1fd676eec9bf&quot;,
    &quot;object&quot;: &quot;chat.completion&quot;,
    &quot;created&quot;: 1794384861,
    &quot;model&quot;: &quot;qwen3.8-max&quot;,
    &quot;choices&quot;: [
        {
            &quot;index&quot;: 0,
            &quot;message&quot;: {
                &quot;role&quot;: &quot;assistant&quot;,
                &quot;reasoning_content&quot;: &quot;The user asks about Hangzhou weather. I should call the weather tool.&quot;,
                &quot;content&quot;: &quot;&quot;,
                &quot;tool_calls&quot;: [
                    {
                        &quot;id&quot;: &quot;call_7355c2deaffc4131ba015924&quot;,
                        &quot;type&quot;: &quot;function&quot;,
                        &quot;function&quot;: {
                            &quot;name&quot;: &quot;get_current_weather&quot;,
                            &quot;arguments&quot;: &quot;{\&quot;location\&quot;: \&quot;杭州市\&quot;}&quot;
                        },
                        &quot;index&quot;: 0
                    }
                ]
            },
            &quot;finish_reason&quot;: &quot;tool_calls&quot;,
            &quot;logprobs&quot;: null
        }
    ],
    &quot;usage&quot;: {
        &quot;prompt_tokens&quot;: 375,
        &quot;total_tokens&quot;: 419,
        &quot;completion_tokens&quot;: 44,
        &quot;prompt_tokens_details&quot;: {
            &quot;cached_tokens&quot;: 0,
            &quot;text_tokens&quot;: 375
        },
        &quot;completion_tokens_details&quot;: {
            &quot;reasoning_tokens&quot;: 15,
            &quot;text_tokens&quot;: 44
        }
    }
}
</code></pre></section><a id="联网搜索-2"></a><section><a id="联网搜索-2-h4"></a><h4>联网搜索</h4><p>以下为 <code>qwen3.8-max</code> 的返回示例，用于说明响应字段。</p><a id="code-block-8"></a><pre class="language-json"><code>{
    &quot;id&quot;: &quot;chatcmpl-0df41ee2-49c9-9ee8-a614-fdec17347b6a&quot;,
    &quot;object&quot;: &quot;chat.completion&quot;,
    &quot;created&quot;: 1794384861,
    &quot;model&quot;: &quot;qwen3.8-max&quot;,
    &quot;choices&quot;: [
        {
            &quot;index&quot;: 0,
            &quot;message&quot;: {
                &quot;role&quot;: &quot;assistant&quot;,
                &quot;reasoning_content&quot;: &quot;用户问：“中国队在巴黎奥运会获得了多少枚金牌”。需要直接回答。知识库多处明确：2024巴黎奥运会中国体育代表团获得40金27银24铜，金牌数境外最佳。需要简洁中文回答。&quot;,
                &quot;content&quot;: &quot;中国队在2024年巴黎奥运会上共获得了 **40枚金牌**。&quot;
            },
            &quot;finish_reason&quot;: &quot;stop&quot;,
            &quot;logprobs&quot;: null
        }
    ],
    &quot;usage&quot;: {
        &quot;prompt_tokens&quot;: 2883,
        &quot;total_tokens&quot;: 2954,
        &quot;completion_tokens&quot;: 71,
        &quot;prompt_tokens_details&quot;: {
            &quot;cached_tokens&quot;: 0,
            &quot;text_tokens&quot;: 2883
        },
        &quot;completion_tokens_details&quot;: {
            &quot;reasoning_tokens&quot;: 50,
            &quot;text_tokens&quot;: 71
        }
    }
}
</code></pre><p>设置<code>include_tool_usage</code>为<code>true</code>并实际触发联网搜索时，<code>usage</code>中会增加<code>x_tools</code>字段：</p><p>以下为 <code>qwen3.8-max</code> 的返回示例，用于说明响应字段。</p><a id="code-block-9"></a><pre class="language-json"><code>{
    &quot;id&quot;: &quot;chatcmpl-4233d020-62cd-949f-94e2-444b97503856&quot;,
    &quot;object&quot;: &quot;chat.completion&quot;,
    &quot;created&quot;: 1792037298,
    &quot;model&quot;: &quot;qwen3.8-max&quot;,
    &quot;choices&quot;: [
        {
            &quot;index&quot;: 0,
            &quot;message&quot;: {
                &quot;role&quot;: &quot;assistant&quot;,
                &quot;content&quot;: &quot;杭州亚运会（第19届亚洲运动会）是在2023年举办的，具体举办时间为2023年9月23日至10月8日。&quot;
            },
            &quot;finish_reason&quot;: &quot;stop&quot;,
            &quot;logprobs&quot;: null
        }
    ],
    &quot;usage&quot;: {
        &quot;prompt_tokens&quot;: 1905,
        &quot;total_tokens&quot;: 1987,
        &quot;completion_tokens&quot;: 82,
        &quot;prompt_tokens_details&quot;: {
            &quot;cached_tokens&quot;: 0,
            &quot;text_tokens&quot;: 1905
        },
        &quot;x_tools&quot;: {
            &quot;search&quot;: {
                &quot;count&quot;: 1,
                &quot;strategy&quot;: &quot;turbo&quot;
            }
        }
    }
}
</code></pre></section><a id="异步调用-2"></a><section><a id="异步调用-2-h4"></a><h4>异步调用</h4><p>异步调用使用 OpenAI SDK，响应对象与文本输入相同；它不对应单独的 curl 异步接口。</p></section></section></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="e98e6b7aa5nb2"></a><h2>chat响应chunk对象（流式输出）</h2><p><strong>id</strong><code>string</code></p><p>本次调用的唯一标识符。每个chunk对象有相同的 id。</p><p><strong>choices</strong><code>array</code></p><p>模型生成内容的数组，可包含一个或多个对象。用于返回 Token 消耗信息的最后一个 chunk 中，<code>choices</code> 为空数组。</p><a id="accordion-属性-35"></a><section><p>属性</p><div><p><strong>delta</strong> <code>object</code></p><p>请求的增量对象。</p><a id="accordion-属性-36"></a><section><p>属性</p><div><p><strong>content</strong> <code>string</code></p><p>增量消息内容。</p><p><strong>encrypted_content</strong> <code>string</code></p><p><code>qwen4-max</code>, <code>thinking_display=&quot;summarized&quot;</code>: 每轮都需传开启参数。客户端只能原样回传密文，不能读取、截断、重新编码、修改或拼接多轮密文。摘要不能替代历史思维链。 <a href="../../model-user-guide/model-experience/text-generation-model/cot-summary.md#multi-turn">思维链摘要与加密</a>. 密文通过独立数据帧返回，不能与其他帧或多轮密文拼接。</p><p><strong>reasoning_content</strong> <code>string</code></p><p>增量思维链内容。</p><p><strong>function_call</strong> <code>object</code></p><p>该值默认为<code>null</code>，请参考<code>tool_calls</code>参数。</p><p><strong>audio</strong><code>object</code></p><p>使用 <a href="../../model-user-guide/model-experience/omni-modal/qwen-omni.md">Qwen-Omni</a> 模型时生成的回复。</p><a id="accordion-属性-37"></a><section><p>属性</p><div><p><strong>data</strong> <code>string</code></p><p>增量的 Base64 音频编码数据。</p><p><strong>expires_at</strong> <code>integer</code></p><p>创建请求时的时间戳。</p></div></section><p><strong>refusal</strong> <code>object</code></p><p>该参数当前固定为<code>null</code>。</p><p><strong>role</strong> <code>string</code></p><p>增量消息对象的角色，只在第一个chunk中有值。</p><p><strong>tool_calls</strong> <code>array</code></p><p>在发起 Function Calling后，模型生成的工具与入参信息。</p><a id="accordion-属性-38"></a><section><p>属性</p><div><p><strong>index</strong> <code>integer</code></p><p>当前工具在<code>tool_calls</code>数组中的索引。</p><p><strong>id</strong> <code>string</code></p><p>本次工具响应的唯一标识符。</p><p><strong>function</strong> <code>object</code></p><p>被调用的工具信息。</p><a id="accordion-属性-39"></a><section><p>属性</p><div><p><strong>arguments</strong> <code>string</code></p><p>增量的入参信息，所有chunk的<code>arguments</code>拼接后为完整的入参。</p><blockquote><p>由于大模型响应有一定随机性，输出的入参信息可能不符合函数签名。请在调用前校验参数有效性。</p></blockquote><p><strong>name</strong> <code>string</code></p><p>工具名称，只在第一个chunk中有值。</p></div></section><p><strong>type</strong> <code>string</code></p><p>工具类型，当前只支持<code>function</code>。</p></div></section></div></section><p><strong>finish_reason</strong> <code>string</code></p><p>模型停止生成的原因。有四种情况：</p><ul><li>因触发输入参数中的<code>stop</code>参数，或自然停止输出时为<code>stop</code>；</li><li>生成未结束时为<code>null</code>；</li><li>生成长度过长而结束为<code>length</code>；</li><li>需要调用工具而结束为<code>tool_calls</code>。</li></ul><p><strong>index</strong> <code>integer</code></p><p>当前响应在<code>choices</code>数组中的索引。当输入参数 n 大于1时，需根据本参数进行不同响应对应的完整内容的拼接。</p><p><strong>logprobs</strong><code>object</code></p><p>当前对象的概率信息。</p><a id="accordion-属性-40"></a><section><p>属性</p><div><p><strong>content</strong> <code>array</code></p><p>带有对数概率信息的 Token 数组。</p><a id="accordion-属性-41"></a><section><p>属性</p><div><p><strong>token</strong> <code>string</code></p><p>当前 Token。</p><p><strong>bytes</strong> <code>array</code></p><p>当前 Token 的 UTF‑8 原始字节列表，用于精确还原输出内容，在处理表情符号、中文字符时有帮助。</p><p><strong>logprob</strong> <code>float</code></p><p>当前 Token 的对数概率。返回值为 null 表示概率值极低。</p><p><strong>top_logprobs</strong> <code>array</code></p><p>当前 Token 位置最可能的若干个 Token 及其对数概率，元素个数与入参的<code>top_logprobs</code>保持一致。</p><a id="accordion-属性-42"></a><section><p>属性</p><div><p><strong>token</strong> <code>string</code></p><p>当前 Token。</p><p><strong>bytes</strong> <code>array</code></p><p>当前 Token 的 UTF‑8 原始字节列表，用于精确还原输出内容，在处理表情符号、中文字符时有帮助。</p><p><strong>logprob</strong> <code>float</code></p><p>当前 Token 的对数概率。返回值为 null 表示概率值极低。</p></div></section></div></section></div></section></div></section><p><strong>created</strong><code>integer</code></p><p>本次请求被创建时的时间戳。每个chunk有相同的时间戳。</p><p><strong>model</strong><code>string</code></p><p>本次请求使用的模型。</p><p><strong>object</strong> <code>string</code></p><p>始终为<code>chat.completion.chunk</code>。</p><p><strong>service_tier</strong> <code>string</code></p><p>该参数当前固定为<code>null</code>。</p><p><strong>system_fingerprint</strong><code>string</code></p><p>该参数当前固定为<code>null</code>。</p><p><strong>usage</strong> <code>object</code></p><p>本次请求消耗的 Token。返回时位于最后一个 chunk。</p><a id="accordion-属性-43"></a><section><p>属性</p><div><p><strong>completion_tokens</strong> <code>integer</code></p><p>模型输出的 Token 数。</p><p><strong>prompt_tokens</strong> <code>integer</code></p><p>输入 Token 数。</p><p><strong>total_tokens</strong> <code>integer</code></p><p>总 Token 数，为<code>prompt_tokens</code>与<code>completion_tokens</code>的总和。</p><p><strong>completion_tokens_details</strong> <code>object</code>（可选）</p><p>输出 Token 的详细信息。部分模型返回该字段。其中 <code>text_tokens</code> 包含 <code>reasoning_tokens</code>——<code>reasoning_tokens</code> 是 <code>text_tokens</code> 中对应思考过程的子集，<code>text_tokens</code> 减去 <code>reasoning_tokens</code> 才是最终可见回复的 Token 数。该字段通常仅在模型输出思考过程时返回，未开启思考时可能为 <code>null</code> 或不返回。</p><a id="accordion-属性-44"></a><section><p>属性</p><div><p><strong>audio_tokens</strong><code>integer</code>（可选）</p><p>输出的音频 Token 数。</p><p><strong>reasoning_tokens</strong> <code>integer</code>（可选）</p><p>思考过程 Token 数，是 <code>text_tokens</code> 的子集。</p><p><strong>text_tokens</strong><code>integer</code>（可选）</p><p>输出文本 Token 数，已包含 <code>reasoning_tokens</code>。</p></div></section><p><strong>prompt_tokens_details</strong> <code>object</code></p><p>输入 Token的细粒度分类。</p><a id="accordion-属性-45"></a><section><p>属性</p><div><p><strong>audio_tokens</strong> <code>integer</code></p><p>输入音频的 Token 数。</p><blockquote><p>视频文件中的音频 Token 数通过本参数返回。</p></blockquote><p><strong>text_tokens</strong> <code>integer</code></p><p>输入文本的 Token 数。</p><p><strong>video_tokens</strong> <code>integer</code></p><p>输入视频（图片列表形式或视频文件）的 Token 数。</p><p><strong>image_tokens</strong> <code>integer</code></p><p>输入图片的 Token 数。</p><p><strong>cached_tokens</strong> <code>integer</code></p><p>命中缓存的 Token 数。Context Cache 详情请参见<a href="../../model-user-guide/model-experience/text-generation-model/context-cache.md">上下文缓存</a>。</p><p><strong>cache_creation</strong> <code>object</code></p><p><a href="../../model-user-guide/model-experience/text-generation-model/context-cache.md#825f201c5fy6o">显式缓存</a>创建信息。</p><a id="accordion-属性-46"></a><section><p>属性</p><div><p><strong>ephemeral_5m_input_tokens</strong> <code>integer</code></p><p>创建显式缓存的 Token 数。</p></div></section><p><strong>cache_creation_input_tokens</strong> <code>integer</code></p><p>创建显式缓存的 Token 数。</p><p><strong>cache_type</strong> <code>string</code></p><p>缓存类型，固定为<code>ephemeral</code>。</p></div></section><a id="accordion-属性-qwen4-3"></a><section><p>属性（Qwen4）</p><div><p>详见<a href="../../model-user-guide/model-experience/text-generation-model/explicit-cache-qwen4.md">显式缓存（Qwen4）</a>。</p><p><strong>text_tokens</strong> <code>integer</code></p><p>输入文本的 Token 数。</p><p><strong>video_tokens</strong> <code>integer</code></p><p>输入视频（图片列表形式或视频文件）的 Token 数。</p><p><strong>image_tokens</strong> <code>integer</code></p><p>输入图片的 Token 数。</p><p><strong>cached_tokens</strong> <code>integer</code></p><p>命中缓存的 Token 数。Context Cache 详情请参见<a href="../../model-user-guide/model-experience/text-generation-model/context-cache.md">上下文缓存</a>。</p><p><strong>cache_write_tokens</strong> <code>integer</code></p><p>缓存创建的输入 Token 数。</p><p><strong>cache_creation_input_tokens</strong> <code>integer</code></p><p>与 <code>cache_write_tokens</code> 相同，统计时不要重复相加。</p><p><strong>cache_type</strong> <code>string</code></p><p><code>ephemeral</code></p><p><strong>cache_creation</strong> <code>object</code></p><p>按 TTL 统计的缓存创建详情。两种 TTL 的 Token 数之和等于本次创建缓存的 Token 数。</p><a id="accordion-属性-47"></a><section><p>属性</p><div><p><strong>ephemeral_5m_input_tokens</strong> <code>integer</code></p><p>5 分钟缓存创建的 Token 数。</p><p><strong>ephemeral_1h_input_tokens</strong> <code>integer</code></p><p>1 小时缓存创建的 Token 数。</p></div></section></div></section><p><strong>x_tools</strong> <code>object</code>（可选）</p><p>联网搜索的调用统计。仅当请求中<code>include_tool_usage</code>为<code>true</code>，且本次请求实际触发了联网搜索时返回，随<code>usage</code>在最后一个 chunk 中显示。</p><a id="accordion-属性-48"></a><section><p>属性</p><div><p><strong>search</strong> <code>object</code>（可选）</p><p>联网搜索的调用统计。开启<a href="../../model-user-guide/model-experience/text-generation-model/tool-calls/web-search.md">联网搜索</a>并实际触发检索时返回。</p><a id="accordion-属性-49"></a><section><p>属性</p><div><p><strong>count</strong> <code>integer</code></p><p>本次请求中联网搜索的触发次数。使用<code>agent</code>搜索策略时，模型可进行多轮检索，该值可能大于 1。</p><p>该值在意图判定阶段即被置位，即使触发限流或检索未返回结果也会计数，不代表检索已实际完成，不作为计费或对账依据。详情请参见<a href="../../model-user-guide/model-experience/text-generation-model/tool-calls/web-search.md#faq-search-billing-count-mismatch-title">账单次数与 count 字段不一致</a>。</p><p><strong>strategy</strong> <code>string</code></p><p>本次联网搜索实际使用的搜索量级策略，与请求中<code>search_options.search_strategy</code>的取值一致，如<code>turbo</code>、<code>max</code>、<code>agent</code>。</p></div></section></div></section></div></section></td><td><div><a id="sec-tabs-4"></a><section><a id="流式输出-2"></a><section><a id="流式输出-2-h4"></a><h4>流式输出</h4><p>curl 的流式响应采用 SSE 格式，每个事件以 <code>data:</code> 开头，事件间以空行分隔，最后以 <code>data: [DONE]</code> 结束。以下省略重复的中间分片，保留角色、思考、正文、结束及用量事件；SDK 会解析 SSE，不会输出 <code>data:</code> 和 <code>[DONE]</code>。</p><a id="fig-code-group-9"></a><div><a id="fig-code-group-9-curl-tab"></a>curl<div><a id="code-code-group-9-curl"></a><pre class="language-text"><code>data: {&quot;model&quot;:&quot;qwen3.8-max&quot;,&quot;id&quot;:&quot;chatcmpl-730609ad-25b4-9809-8bd2-29b3fb280cb9&quot;,&quot;created&quot;:1794384852,&quot;object&quot;:&quot;chat.completion.chunk&quot;,&quot;usage&quot;:null,&quot;choices&quot;:[{&quot;logprobs&quot;:null,&quot;index&quot;:0,&quot;delta&quot;:{&quot;reasoning_content&quot;:&quot;&quot;,&quot;content&quot;:&quot;&quot;,&quot;role&quot;:&quot;assistant&quot;},&quot;finish_reason&quot;:null}]}

data: {&quot;id&quot;:&quot;chatcmpl-730609ad-25b4-9809-8bd2-29b3fb280cb9&quot;,&quot;object&quot;:&quot;chat.completion.chunk&quot;,&quot;created&quot;:1794384852,&quot;model&quot;:&quot;qwen3.8-max&quot;,&quot;choices&quot;:[{&quot;index&quot;:0,&quot;delta&quot;:{&quot;content&quot;:&quot;&quot;,&quot;reasoning_content&quot;:&quot;用户&quot;},&quot;logprobs&quot;:null,&quot;finish_reason&quot;:null}],&quot;usage&quot;:null}

data: {&quot;id&quot;:&quot;chatcmpl-730609ad-25b4-9809-8bd2-29b3fb280cb9&quot;,&quot;object&quot;:&quot;chat.completion.chunk&quot;,&quot;created&quot;:1794384858,&quot;model&quot;:&quot;qwen3.8-max&quot;,&quot;choices&quot;:[{&quot;index&quot;:0,&quot;delta&quot;:{&quot;content&quot;:&quot;我是通义&quot;,&quot;reasoning_content&quot;:&quot;&quot;},&quot;logprobs&quot;:null,&quot;finish_reason&quot;:null}],&quot;usage&quot;:null}

data: {&quot;id&quot;:&quot;chatcmpl-730609ad-25b4-9809-8bd2-29b3fb280cb9&quot;,&quot;object&quot;:&quot;chat.completion.chunk&quot;,&quot;created&quot;:1794384861,&quot;model&quot;:&quot;qwen3.8-max&quot;,&quot;choices&quot;:[{&quot;index&quot;:0,&quot;delta&quot;:{&quot;content&quot;:&quot;&quot;,&quot;reasoning_content&quot;:&quot;&quot;},&quot;finish_reason&quot;:&quot;stop&quot;,&quot;logprobs&quot;:null}],&quot;usage&quot;:null}

data: {&quot;id&quot;:&quot;chatcmpl-730609ad-25b4-9809-8bd2-29b3fb280cb9&quot;,&quot;object&quot;:&quot;chat.completion.chunk&quot;,&quot;created&quot;:1794384861,&quot;model&quot;:&quot;qwen3.8-max&quot;,&quot;choices&quot;:[],&quot;usage&quot;:{&quot;prompt_tokens&quot;:61,&quot;total_tokens&quot;:346,&quot;completion_tokens&quot;:285,&quot;prompt_tokens_details&quot;:{&quot;cached_tokens&quot;:0,&quot;text_tokens&quot;:61},&quot;completion_tokens_details&quot;:{&quot;reasoning_tokens&quot;:195,&quot;text_tokens&quot;:285}}}

data: [DONE]
</code></pre></div><a id="fig-code-group-9-python-node-js-tab"></a>Python / Node.js<div><a id="code-code-group-9-python-node-js"></a><pre class="language-json"><code>{&quot;id&quot;:&quot;chatcmpl-e30f5ae7-3063-93c4-90fe-beb5f900bd57&quot;,&quot;choices&quot;:[{&quot;delta&quot;:{&quot;content&quot;:&quot;&quot;,&quot;function_call&quot;:null,&quot;refusal&quot;:null,&quot;role&quot;:&quot;assistant&quot;,&quot;tool_calls&quot;:null},&quot;finish_reason&quot;:null,&quot;index&quot;:0,&quot;logprobs&quot;:null}],&quot;created&quot;:1735113344,&quot;model&quot;:&quot;qwen3.8-max&quot;,&quot;object&quot;:&quot;chat.completion.chunk&quot;,&quot;service_tier&quot;:null,&quot;system_fingerprint&quot;:null,&quot;usage&quot;:null}
{&quot;id&quot;:&quot;chatcmpl-e30f5ae7-3063-93c4-90fe-beb5f900bd57&quot;,&quot;choices&quot;:[{&quot;delta&quot;:{&quot;content&quot;:&quot;我是&quot;,&quot;function_call&quot;:null,&quot;refusal&quot;:null,&quot;role&quot;:null,&quot;tool_calls&quot;:null},&quot;finish_reason&quot;:null,&quot;index&quot;:0,&quot;logprobs&quot;:null}],&quot;created&quot;:1735113344,&quot;model&quot;:&quot;qwen3.8-max&quot;,&quot;object&quot;:&quot;chat.completion.chunk&quot;,&quot;service_tier&quot;:null,&quot;system_fingerprint&quot;:null,&quot;usage&quot;:null}
{&quot;id&quot;:&quot;chatcmpl-e30f5ae7-3063-93c4-90fe-beb5f900bd57&quot;,&quot;choices&quot;:[{&quot;delta&quot;:{&quot;content&quot;:&quot;&quot;,&quot;function_call&quot;:null,&quot;refusal&quot;:null,&quot;role&quot;:null,&quot;tool_calls&quot;:null},&quot;finish_reason&quot;:&quot;stop&quot;,&quot;index&quot;:0,&quot;logprobs&quot;:null}],&quot;created&quot;:1735113344,&quot;model&quot;:&quot;qwen3.8-max&quot;,&quot;object&quot;:&quot;chat.completion.chunk&quot;,&quot;service_tier&quot;:null,&quot;system_fingerprint&quot;:null,&quot;usage&quot;:null}
{&quot;id&quot;:&quot;chatcmpl-e30f5ae7-3063-93c4-90fe-beb5f900bd57&quot;,&quot;choices&quot;:[],&quot;created&quot;:1735113344,&quot;model&quot;:&quot;qwen3.8-max&quot;,&quot;object&quot;:&quot;chat.completion.chunk&quot;,&quot;service_tier&quot;:null,&quot;system_fingerprint&quot;:null,&quot;usage&quot;:{&quot;completion_tokens&quot;:17,&quot;prompt_tokens&quot;:22,&quot;total_tokens&quot;:39,&quot;completion_tokens_details&quot;:null,&quot;prompt_tokens_details&quot;:{&quot;audio_tokens&quot;:null,&quot;cached_tokens&quot;:0}}}
</code></pre></div></div></section><a id="文档理解-2"></a><section><a id="文档理解-2-h4"></a><h4>文档理解</h4><p>将请求中的文件 ID 替换为上传文档后返回的文件 ID。</p><a id="code-block-10"></a><pre class="language-text"><code>data: {&quot;choices&quot;:[{&quot;delta&quot;:{&quot;content&quot;:&quot;&quot;,&quot;role&quot;:&quot;assistant&quot;},&quot;finish_reason&quot;:null,&quot;index&quot;:0,&quot;logprobs&quot;:null}],&quot;usage&quot;:null,&quot;created&quot;:1794384917,&quot;system_fingerprint&quot;:null,&quot;object&quot;:&quot;chat.completion.chunk&quot;,&quot;model&quot;:&quot;qwen-long&quot;,&quot;id&quot;:&quot;chatcmpl-dd003860-d3ed-9996-8a46-0c50d416bb63&quot;}

data: {&quot;choices&quot;:[{&quot;delta&quot;:{&quot;content&quot;:&quot;这篇文章&quot;,&quot;role&quot;:&quot;assistant&quot;},&quot;finish_reason&quot;:null,&quot;index&quot;:0,&quot;logprobs&quot;:null}],&quot;usage&quot;:null,&quot;created&quot;:1794384917,&quot;system_fingerprint&quot;:null,&quot;object&quot;:&quot;chat.completion.chunk&quot;,&quot;model&quot;:&quot;qwen-long&quot;,&quot;id&quot;:&quot;chatcmpl-dd003860-d3ed-9996-8a46-0c50d416bb63&quot;}

data: {&quot;choices&quot;:[{&quot;delta&quot;:{&quot;content&quot;:&quot;&quot;},&quot;finish_reason&quot;:&quot;stop&quot;,&quot;index&quot;:0,&quot;logprobs&quot;:null}],&quot;usage&quot;:null,&quot;created&quot;:1794384919,&quot;system_fingerprint&quot;:null,&quot;object&quot;:&quot;chat.completion.chunk&quot;,&quot;model&quot;:&quot;qwen-long&quot;,&quot;id&quot;:&quot;chatcmpl-dd003860-d3ed-9996-8a46-0c50d416bb63&quot;}

data: {&quot;choices&quot;:[],&quot;usage&quot;:{&quot;prompt_tokens&quot;:59,&quot;completion_tokens&quot;:107,&quot;total_tokens&quot;:166},&quot;created&quot;:1794384919,&quot;system_fingerprint&quot;:null,&quot;object&quot;:&quot;chat.completion.chunk&quot;,&quot;model&quot;:&quot;qwen-long&quot;,&quot;id&quot;:&quot;chatcmpl-dd003860-d3ed-9996-8a46-0c50d416bb63&quot;}

data: [DONE]
</code></pre></section><a id="ppt生成-2"></a><section><a id="ppt生成-2-h4"></a><h4>PPT生成</h4><a id="code-block-11"></a><pre class="language-text"><code>data: {&quot;choices&quot;:[{&quot;delta&quot;:{&quot;content&quot;:null,&quot;role&quot;:&quot;assistant&quot;,&quot;reasoning_content&quot;:&quot;&quot;},&quot;index&quot;:0,&quot;logprobs&quot;:null,&quot;finish_reason&quot;:null}],&quot;object&quot;:&quot;chat.completion.chunk&quot;,&quot;usage&quot;:null,&quot;created&quot;:1794385034,&quot;system_fingerprint&quot;:null,&quot;model&quot;:&quot;qwen-doc-turbo&quot;,&quot;id&quot;:&quot;chatcmpl-fea338d0-e90f-93d3-9106-78b8132278e3&quot;}

data: {&quot;choices&quot;:[{&quot;finish_reason&quot;:null,&quot;logprobs&quot;:null,&quot;delta&quot;:{&quot;content&quot;:null,&quot;reasoning_content&quot;:&quot;大纲生成成功：ppt_overview = # 【PPT内容大纲与详细设计】\n\n## 第1页：封面\n**大纲要点：**\n- 主标题：AI智能体系统架构\n- 副标题：基于大模型驱动的自动化解决方案\n- …&quot;},&quot;index&quot;:0}],&quot;object&quot;:&quot;chat.completion.chunk&quot;,&quot;usage&quot;:null,&quot;created&quot;:1794385034,&quot;system_fingerprint&quot;:null,&quot;model&quot;:&quot;qwen-doc-turbo&quot;,&quot;id&quot;:&quot;chatcmpl-fea338d0-e90f-93d3-9106-78b8132278e3&quot;}
</code></pre></section><a id="联网搜索-3"></a><section><a id="联网搜索-3-h4"></a><h4>联网搜索</h4><p>设置 <code>include_tool_usage</code> 为 <code>true</code> 并实际触发联网搜索时，最后一个 chunk 的 <code>usage</code> 中会增加 <code>x_tools</code> 字段：</p><p>以下为 <code>qwen3.8-max</code> 的返回示例，用于说明响应字段。</p><a id="code-block-12"></a><pre class="language-text"><code>data: {&quot;id&quot;:&quot;chatcmpl-3d720785-fa18-9207-ac31-666fd4fb1ba3&quot;,&quot;object&quot;:&quot;chat.completion.chunk&quot;,&quot;created&quot;:1794396212,&quot;model&quot;:&quot;qwen3.8-max&quot;,&quot;choices&quot;:[],&quot;usage&quot;:{&quot;prompt_tokens&quot;:2883,&quot;total_tokens&quot;:2962,&quot;completion_tokens&quot;:79,&quot;prompt_tokens_details&quot;:{&quot;cached_tokens&quot;:0,&quot;text_tokens&quot;:2883},&quot;completion_tokens_details&quot;:{&quot;reasoning_tokens&quot;:58,&quot;text_tokens&quot;:79},&quot;x_tools&quot;:{&quot;search&quot;:{&quot;count&quot;:1,&quot;strategy&quot;:&quot;turbo&quot;}}}}

data: [DONE]
</code></pre></section></section></div></td></tr></tbody></table>

<a id="错误码"></a>

<a id="occ-errcode-h2"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](../preparations/error-code.md)进行解决。
