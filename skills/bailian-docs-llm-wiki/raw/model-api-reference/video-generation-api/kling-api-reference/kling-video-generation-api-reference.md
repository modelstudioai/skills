# 可灵-视频生成API文档

可灵-视频生成模型支持 文生视频、图生视频-基于首帧、图生视频-基于首尾帧、参考生视频以及视频编辑 。

> **重要**
>
> 本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。

<a id="服务开通"></a>

<a id="kl004a0h2svco"></a>

<a id="kl003a0sesvco"></a>

## 服务开通

请前往[阿里云百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)，搜索“kling”，找到**可灵AI**模型卡片，单击**立即开通**，在弹窗内确认开通及授权。

<a id="适用范围"></a>

<a id="kl013a0h2scop"></a>

<a id="kl012a0scope"></a>

## 适用范围

为确保调用成功，请务必保证**模型、Endpoint URL 和 API Key 均属于同一地域**。跨地域调用将会失败。

-   [**选择模型**](../../../model-user-guide/model-experience/image-and-video-generation/video-generate-edit-model.md)：确认模型所属的地域。
-   **选择 URL**：选择对应的地域 Endpoint URL，支持HTTP URL。
-   **配置 API Key**：选择地域并[获取与配置 API Key](../../preparations/get-api-key.md)，再[配置API Key到环境变量](../../preparations/get-api-key.md)。

<a id="模型概览"></a>

## 模型概览

| 模型名称 | 能力支持 | 输入模态 | 输出视频规格 |
| --- | --- | --- | --- |
| kling/kling-v3-turbo-video-generation | 文生视频；图生视频-基于首帧 | 文本、图像 | 分辨率模式：std（720P）、pro（1080P）；宽高比：16:9、9:16、1:1；视频时长：3-15秒；视频格式：MP4 |
| kling/kling-v3-video-generation | 文生视频；图生视频-基于首帧；图生视频-基于首尾帧 | 文本、图像 | 分辨率模式：std（720P）、pro（1080P）、4k；宽高比：16:9、9:16、1:1；视频时长：3-15秒；视频格式：MP4 |
| kling/kling-v3-omni-video-generation | 文生视频；图生视频-基于首帧；图生视频-基于首尾帧；参考生视频；视频编辑 | 文本、图像、视频 | 分辨率模式：std（720P）、pro（1080P）、4k；宽高比：16:9、9:16、1:1；视频时长：3-15秒；视频格式：MP4 |

以下两个 Kling 4.0 模型均仅在华北2（北京）地域提供，采用相同的百炼异步调用流程，但支持的素材不同：

| 模型名称 | 能力支持 | 输入模态 | 输出视频规格 |
| --- | --- | --- | --- |
| kling/kling-v4-video-generation | 文生视频、关键帧生视频（首帧、中间帧、尾帧可任意组合） | 文本、帧图 | `std`（720P）、`pro`（1080P）；21:9、16:9、9:16、1:1；3～30秒；MP4（H.264） |
| kling/kling-v4-omni-reference-video-generation | 文生视频、关键帧生视频、参考生视频、视频编辑 | 文本、帧图、参考图、视频、主体 | `std`（720P）、`pro`（1080P）；21:9、16:9、9:16、1:1；3～30秒；MP4（H.264） |

4.0 固定生成有声视频，不支持 `4k` 模式。模型和素材的详细限制见下文请求参数。

<a id="http调用"></a>

<a id="kl101a0h2http"></a>

<a id="kl100a0httpsec"></a>

## HTTP调用

由于视频生成任务耗时较长（通常为1-5分钟），API采用异步调用。整个流程包含 **"创建任务 -> 轮询获取"** 两个核心步骤，具体如下：

<a id="步骤1-创建任务获取任务id"></a>

<a id="kl111a0h3stp1"></a>

<a id="kl110a0step1"></a>

### 步骤1：创建任务获取任务ID

**北京地域**：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

> **说明**
>
> -   创建成功后，使用接口返回的 `task_id` 查询结果，task\_id 有效期为 24 小时。**请勿重复创建任务**，轮询获取即可。
> -   新手指引请参见[Postman](https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api)。

<table><tbody><tr><td><a id="kl123a0h4reqp"></a><h4>请求参数</h4><a id="kl142a0h5hdr1"></a><h5>请求头（Headers）</h5><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><p><strong>X-DashScope-Async</strong><code>string</code><strong>（必选）</strong></p><p>异步处理配置参数。HTTP请求只支持异步，<strong>必须设置为</strong><code>enable</code>。</p><div><div><p><strong>重要</strong>缺少此请求头将报错：“current user api does not support synchronous calls”。</p></div></div><a id="kl154a0h5body"></a><h5>请求体（Request Body）</h5><p><strong>model</strong> <code>string</code> <strong>（必选）</strong></p><p>模型名称。</p><p>可选值：</p><ul><li><code>kling/kling-v3-turbo-video-generation</code></li><li><code>kling/kling-v3-video-generation</code></li><li><code>kling/kling-v3-omni-video-generation</code></li><li><code>kling/kling-v4-video-generation</code></li><li><code>kling/kling-v4-omni-reference-video-generation</code></li></ul><p><strong>input</strong> <code>object</code> <strong>（必选）</strong></p><p>输入的基本信息，如提示词、媒体素材等。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>prompt</strong> <code>string</code> （条件必填）</p><p>文本提示词。用来描述生成视频中期望包含的元素和视觉特点。</p><p>3.0 模型支持中英文，每个汉字/字母占一个字符，不超过2500个字符，超过将返回错误。填写逻辑：</p><ul><li>当 <code>shot_type=intelligence</code> 时，此参数<strong>必填</strong>。</li><li>当 <code>shot_type=customize</code> 时，此参数<strong>不生效</strong>，请以 <code>multi_prompt</code> 为准。</li></ul><p>4.0 模型可在 <code>prompt</code> 中同时描述期望和不期望出现的内容，并直接描述分镜需求：</p><ul><li><code>kling/kling-v4-video-generation</code>：文生视频时必填；传入帧图时可不填。</li><li><code>kling/kling-v4-omni-reference-video-generation</code>：必填。</li><li>纯英文最多26000个字符，纯非英文最多11000个字符；中英文混合时，英文字符数 ÷ 26000 + 非英文字符数 ÷ 11000 ≤ 1。</li></ul><p>Omni 模型可在 <code>prompt</code> 中引用主体、图片、视频等内容：</p><ul><li>支持模型：<code>kling/kling-v3-omni-video-generation</code>、<code>kling/kling-v4-omni-reference-video-generation</code>；3.0 的此用法适用于参考生视频。</li><li>引用格式：使用 <code>&lt;&lt;&lt;element_1&gt;&gt;&gt;</code>、<code>&lt;&lt;&lt;image_1&gt;&gt;&gt;</code>、<code>&lt;&lt;&lt;video_1&gt;&gt;&gt;</code> 等标记；4.0 还可使用 <code>&lt;&lt;&lt;voice_1&gt;&gt;&gt;</code> 引用 <code>voice_list</code> 中的音色。</li><li>引用顺序：4.0 的图片、视频分别按 <code>media</code> 中同类素材的出现顺序编号，主体和音色分别按 <code>element_list</code>、<code>voice_list</code> 的顺序编号；3.0 按 <code>media</code> 数组顺序定义图片和视频的引用顺序。</li><li>用法示例：<code>一只&lt;&lt;&lt;element_1&gt;&gt;&gt;在月光下奔跑</code>。</li></ul><p><strong>negative_prompt</strong> <code>string</code> （可选）</p><p>3.0 模型的负向提示词，用于描述不希望在结果中出现的内容，不超过2500个字符。</p><ul><li><code>kling/kling-v3-turbo-video-generation</code> 无独立负向提示词能力，该字段不生效（负向描述可写入<code>prompt</code>）。</li><li>支持模型：<code>kling/kling-v3-video-generation</code>、<code>kling/kling-v3-omni-video-generation</code>。</li><li>4.0 模型的此字段不生效，请将负向描述写入 <code>prompt</code>。</li></ul><p><strong>media</strong> <code>array</code> （可选）</p><p>文生视频任务无需填写此参数。</p><p>媒体素材列表，用于指定图像或视频素材。</p><p>不同模型支持的媒体素材搭配不一样：</p><a id="accordion-素材组合规则"></a><section><p>素材组合规则</p><div><a id="accordion-kling-kling-v3-turbo-video-generation"></a><section><p>kling/kling-v3-turbo-video-generation</p><div><p>仅支持以下媒体素材组合，非法组合将报错。</p><ul><li><p><strong>图生视频-基于首帧</strong>：<code>first_frame</code>。</p><ul><li>数量限制：首帧恰好1张。不支持<code>last_frame</code>。</li></ul></li></ul></div></section><a id="accordion-kling-kling-v3-video-generation"></a><section><p>kling/kling-v3-video-generation</p><div><p>仅支持以下媒体素材组合，非法组合将报错。</p><ul><li><p><strong>图生视频-基于首帧</strong>：<code>first_frame</code>。</p><ul><li>数量限制：首帧1张。</li></ul></li><li><p><strong>图生视频-基于首尾帧</strong>：<code>first_frame+last_frame</code>。</p><ul><li>数量限制：首帧1张，尾帧1张。</li></ul></li></ul></div></section><a id="accordion-kling-kling-v3-omni-video-generation"></a><section><p>kling/kling-v3-omni-video-generation</p><div><p>仅支持以下媒体素材组合，非法组合将报错。</p><ul><li><p><strong>图生视频-基于首帧</strong>：<code>first_frame</code>。</p><ul><li>图像数量：首帧1张。</li></ul></li><li><p><strong>图生视频-基于首尾帧</strong>：<code>first_frame+last_frame</code>。</p><ul><li>图像数量：首帧1张，尾帧1张。</li></ul></li><li><p><strong>参考生视频</strong>：支持以下 <code>media</code> 组合。</p><ul><li>仅传入 <code>feature</code> 时：必须传入1个视频。</li><li>仅传入 <code>refer</code> 时：参考图片与多图主体数量（<code>element_list</code> 的数组长度）之和不得超过7。</li><li>传入 <code>feature+refer</code> 时：必须传入1个视频，且参考图片与多图主体数量（<code>element_list</code> 的数组长度）之和不得超过4。</li><li>传入 <code>feature+first_frame</code> 时：必须传入1个视频和1张首帧。</li></ul></li><li><p><strong>视频编辑</strong>：支持以下 <code>media</code> 组合。</p><ul><li>仅传入 <code>base</code> 时：必须传入1个视频。</li><li>传入 <code>base+refer</code> 时：必须传入1个视频，且参考图片与多图主体数量（<code>element_list</code> 的数组长度）之和不得超过4。</li></ul></li></ul></div></section><a id="accordion-kling-kling-v4-video-generation"></a><section><p>kling/kling-v4-video-generation</p><div><p>支持 <code>first_frame</code>、<code>middle_frame</code>、<code>last_frame</code> 任意组合，也可不传 <code>media</code> 进行文生视频；可仅传尾帧或中间帧。首帧和尾帧各最多1张，帧图总数不超过10张。不支持 <code>refer</code>、<code>feature</code>、<code>base</code> 或 <code>element_list</code>。</p></div></section><a id="accordion-kling-kling-v4-omni-reference-video-generation"></a><section><p>kling/kling-v4-omni-reference-video-generation</p><div><p>支持帧图、参考图（<code>refer</code>）、特征参考视频（<code>feature</code>）、待编辑视频（<code>base</code>）及主体；3.0 的素材互斥限制不适用于此模型，尾帧无需与首帧同时传入，<code>base</code> 可与帧图和 <code>feature</code> 组合。</p><ul><li>图片（首帧、中间帧、尾帧和参考图）合计不超过10张，首帧和尾帧各最多1张。</li><li>视频（<code>feature</code> 和 <code>base</code>）合计不超过5个，<code>base</code> 最多1个；视频角色主体与参考视频合计不超过5个。</li><li>主体最多7个，其中视频角色主体最多3个；音色最多3个，已绑定音色的主体不占音色数量。</li><li>图片、视频、主体、音色合计不超过15个。素材规格见下文 <code>url</code> 参数。</li></ul></div></section></div></section><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>媒体素材类型。可选值与所选模型有关：</p><a id="accordion-kling-kling-v3-turbo-video-generation-2"></a><section><p>kling/kling-v3-turbo-video-generation</p><div><p>可选值：</p><ul><li><code>first_frame</code>：首帧图片。</li></ul><p>不支持<code>last_frame</code>。不同媒体素材之间的搭配限制，请参见 <code>media</code> 参数下的”素材组合规则”。</p></div></section><a id="accordion-kling-kling-v3-video-generation-2"></a><section><p>kling/kling-v3-video-generation</p><div><p>可选值：</p><ul><li><code>first_frame</code>：首帧图片。</li><li><code>last_frame</code>：尾帧图片。</li></ul><p>不同媒体素材之间的搭配限制，请参见 <code>media</code> 参数下的”素材组合规则”。</p></div></section><a id="accordion-kling-kling-v3-omni-video-generation-2"></a><section><p>kling/kling-v3-omni-video-generation</p><div><p>可选值：</p><ul><li><code>first_frame</code>：首帧图片。</li><li><code>last_frame</code>：尾帧图片。</li><li><code>refer</code>：参考图片。</li><li><code>base</code>：待编辑视频。</li><li><code>feature</code>：特征参考视频。</li></ul><p>不同媒体素材之间的搭配限制，请参见 <code>media</code> 参数下的“素材组合规则”。</p></div></section><a id="accordion-kling-kling-v4-video-generation-2"></a><section><p>kling/kling-v4-video-generation</p><div><ul><li><code>first_frame</code>：首帧图片。</li><li><code>middle_frame</code>：中间帧图片，可传多张。</li><li><code>last_frame</code>：尾帧图片。</li></ul></div></section><a id="accordion-kling-kling-v4-omni-reference-video-generation-2"></a><section><p>kling/kling-v4-omni-reference-video-generation</p><div><ul><li><code>first_frame</code>、<code>middle_frame</code>、<code>last_frame</code>：首帧、中间帧和尾帧图片。</li><li><code>refer</code>：参考图片。</li><li><code>feature</code>：特征参考视频。</li><li><code>base</code>：待编辑视频。</li></ul></div></section><p><strong>url</strong> <code>string</code> <strong>（必选）</strong></p><p>媒体素材URL。素材包括图像、视频。</p><a id="accordion-传入图像-type-first-frame-middle-frame-last-frame或refer"></a><section><p>传入图像（type=first_frame、middle_frame、last_frame或refer）</p><div><p>图像URL。</p><ul><li>支持 HTTP 或 HTTPS 协议。</li><li>示例值：<code>https://example.com/image.png</code>。</li></ul><p>3.0 模型的图像限制：</p><ul><li>格式：JPEG、JPG、PNG（不支持透明通道）。</li><li>分辨率：宽和高的范围为[300, 8000]像素。</li><li>宽高比：1:2.5 ~ 2.5:1。</li><li>文件大小：不超过10MB。</li></ul><p>4.0 模型的图像限制：</p><ul><li>格式：JPG、JPEG、PNG。</li><li>分辨率：宽和高均不小于300像素。</li><li>宽高比：2:5～5:2。</li><li>文件大小：不超过30MB。</li></ul></div></section><a id="accordion-传入视频-type-base或feature"></a><section><p>传入视频（type=base或feature）</p><div><p>视频文件的 URL。</p><ul><li>支持 HTTP 和 HTTPS 协议。</li><li>示例值：<code>https://example.com/video.mp4</code>。</li></ul><p>3.0 Omni 模型的视频限制：</p><ul><li>格式：mp4、mov。</li><li>文件大小：不超过200MB。</li><li>时长：3～15.5s。</li><li>分辨率：宽和高的范围为[700, 4553]像素，像素总面积不超过8294400。</li><li>宽高比：0.4～2。</li><li>帧率：24～60fps。</li></ul><p>4.0 Omni 模型的视频限制（<code>feature</code>、<code>base</code>）：</p><ul><li>格式：MP4、MOV；单个文件不超过300MB。</li><li>单个视频及输入视频总时长均为3～30秒；输入视频总时长还包含视频角色主体的时长。</li><li>宽和高均在700～4553像素之间，像素总面积不超过8294400；宽高比2:5～5:2，帧率24～60fps。</li></ul></div></section><p><strong>keep_original_sound</strong> <code>string</code> （可选）</p><p>支持模型：kling/kling-v3-omni-video-generation 。</p><p>生效条件：当且仅当传入视频（type=base或feature）时生效。</p><p>是否保留原视频声音。</p><ul><li><code>no</code>：默认值，不保留原声。</li><li><code>yes</code>：保留原声。</li></ul><p>4.0 Omni 模型不保留输入视频原声：传 <code>yes</code> 会导致参数错误，传 <code>no</code> 或不传不受影响。</p></div></section><p><strong>multi_shot</strong> <code>boolean</code> （可选）</p><p>3.0 模型是否开启多镜头生成。</p><ul><li><code>false</code>：默认值，不开启多镜头。</li><li><code>true</code>：开启多镜头生成。</li></ul><p>注意：</p><ul><li>3.0 的视频特征参考（feature）场景支持开启多镜头（<code>shot_type</code>仅支持<code>intelligence</code>）。</li><li>3.0 的视频编辑（base）场景不支持多镜头。</li><li>4.0 默认智能分镜，无需设置此字段；传入任何 <code>multi_shot</code> 值均不生效。分镜需求直接写在 <code>prompt</code> 中。</li></ul><p><strong>shot_type</strong> <code>string</code> （条件必填）</p><p>3.0 模型在 <code>multi_shot=true</code> 时必填。多镜头模式类型。</p><ul><li><code>intelligence</code>：智能分镜，由模型自动规划镜头。</li><li><code>customize</code>：自定义模式，支持自定义每个片段的提示词和时长。</li></ul><p>4.0 模型不使用此字段；传入 <code>shot_type=customize</code> 会导致参数错误，分镜需求请直接写在 <code>prompt</code> 中。</p><p><strong>multi_prompt</strong> <code>array</code> （条件必填）</p><p>3.0 模型在 <code>shot_type=customize</code> 时必填。多镜头自定义模式下的片段列表。4.0 模型传入此字段会导致参数错误。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>index</strong> <code>integer</code> <strong>（必选）</strong></p><p>分镜片段索引，分镜数量为1～6个，索引从1开始。</p><p><strong>prompt</strong> <code>string</code> <strong>（必选）</strong></p><p>对应片段的提示词，支持中英文，不超过512个字符，超过自动截断。</p><p><strong>duration</strong> <code>integer</code> <strong>（必选）</strong></p><p>对应片段的时长，单位为秒。</p><p>取值为[1, <code>parameters.duration</code>]之间的整数。</p></div></section><p><strong>element_list</strong> <code>array</code> （可选）</p><p>主体列表，用于指定视频中需要引入的主体元素。</p><p>注意：<code>kling/kling-v3-turbo-video-generation</code> 和 <code>kling/kling-v4-video-generation</code> 不支持主体，该字段不可传。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>element_id</strong> <code>integer</code> （条件必填）</p><p>传<code>element_list</code>时必填，表示主体ID。请在<a href="kling-object-ids.md#entity-library">可灵-官方主体库</a>获取主体ID。</p><p>3.0 模型的主体个数限制（<code>element_list</code> 数组长度限制）：</p><ul><li>图生视频-基于首帧：最多支持3个主体。</li><li>图生视频-基于首尾帧：最多支持3个主体。</li><li>参考生视频（<code>type=refer</code>）：参考图片与多图主体数量之和不得超过7。</li><li>参考生视频（<code>type=feature+refer</code>）：参考图片与多图主体数量之和不得超过4。</li><li>视频输入场景（omni模型）：支持视频类型主体，最多1个。引用视频类型主体后，不可再传参考图/图片类型主体。</li></ul><p>4.0 Omni 模型最多传7个主体，其中视频角色主体最多3个；视频角色主体与输入视频合计不超过5个，视频角色主体的时长计入视频总时长。图片、视频、主体、音色合计不超过15个。主体 ID 仅可来自官方主体库，不支持主体创建接口。</p></div></section><p><strong>voice_list</strong> <code>array</code> （可选，适用于4.0模型）</p><p>音色列表，最多3个；已绑定音色的主体不占此数量。每项的 <code>voice_id</code> 为必填音色 ID，仅可来自<a href="kling-object-ids.md#voice-library">官方音色库</a>，不支持音色定制接口。可在 <code>prompt</code> 中通过 <code>&lt;&lt;&lt;voice_1&gt;&gt;&gt;</code>、<code>&lt;&lt;&lt;voice_2&gt;&gt;&gt;</code> 等标记，按 <code>voice_list</code> 顺序引用音色。</p></div></section><p><strong>parameters</strong> <code>object</code> （可选）</p><p>视频生成参数。如设置生成模式、画面比例、视频时长、是否生成音频等。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>mode</strong> <code>string</code> （可选）</p><p>视频生成模式。</p><ul><li><code>pro</code>：默认值，专业模式，输出视频分辨率为1080P。</li><li><code>std</code>：标准模式，输出视频分辨率为720P。</li><li><code>4k</code>：4K模式，输出视频分辨率为4K（仅适用于支持该模式的3.0模型）。</li></ul><p><code>kling/kling-v3-turbo-video-generation</code> 和两个 4.0 模型仅支持 <code>std</code>（720P）和 <code>pro</code>（1080P），不支持 <code>4k</code>；4.0 默认 <code>pro</code>。</p><p><strong>aspect_ratio</strong> <code>string</code> （3.0条件必填；4.0可选）</p><p>生成视频的宽高比例。</p><p>3.0 模型的可选值：</p><ul><li><code>16:9</code>：默认值。</li><li><code>9:16</code></li><li><code>1:1</code></li></ul><p>3.0 模型的以下场景必须填写：</p><ul><li>文生视频：必须设置。</li><li>参考生视频（<code>type=feature</code>、<code>type=feature+refer</code>、<code>type=refer</code>）：必须设置。</li></ul><a id="accordion-3-0-模型其他场景无需设置"></a><section><p>3.0 模型其他场景无需设置</p><div><ul><li>图生视频-基于首帧：以首帧的宽高比为基准，无需填写。</li><li>图生视频-基于首尾帧：以首帧的宽高比为基准，无需填写。</li><li>参考生视频（<code>type=feature+first_frame</code>）：以首帧的宽高比为基准，无需填写。</li><li>视频编辑：以输入视频的宽高比为基准，无需填写。</li></ul></div></section><p>4.0 模型可选 <code>21:9</code>、<code>16:9</code>、<code>9:16</code>、<code>1:1</code>：</p><ul><li><code>kling/kling-v4-video-generation</code>：文生视频时生效；不传则先按提示词中的比例描述生成，未指明时使用 <code>16:9</code>。传入帧图时此参数不生效，比例依次跟随首帧、中间帧首张、尾帧。</li><li><code>kling/kling-v4-omni-reference-video-generation</code>：可显式指定；不传则先按提示词中的比例描述，未指明时依次跟随待编辑视频、首帧、中间帧首张、尾帧，均无时使用 <code>16:9</code>。</li></ul><p><strong>duration</strong> <code>integer</code> （可选）</p><div><div><p><strong>重要</strong>3.0 模型按生成视频时长计费。4.0 模型按计费时长（秒）计费：无视频输入时等于生成视频时长；有视频输入时等于 max（输入视频总时长，生成视频时长）+ 生成视频时长。具体单价见<a href="../../../model-user-guide/test-1/model-pricing.md#9cb8313752li4">模型价格</a>。</p></div></div><p>生成视频的时长，单位为秒。</p><ul><li><p>kling/kling-v3-turbo-video-generation：取值为[3, 15]之间的整数，默认值为5。</p></li><li><p>kling/kling-v3-video-generation：取值为[3, 15]之间的整数，默认值为5。</p></li><li><p>kling/kling-v3-omni-video-generation：取值为[3, 15]之间的整数，默认值为5。</p><ul><li><p>注意：当传入视频时，该参数的行为因<code>type</code>不同而异：</p><ul><li><code>type=feature</code>：取值为[3, 10]之间的整数，默认值为5。</li><li><code>type=base</code>：输出视频时长与传入视频时长相同，此时当前参数无效。按输入视频时长四舍五入取整计量计费。</li></ul></li></ul></li><li><p>两个 4.0 模型：取值为3～30之间的整数。不传时先按提示词中的时长描述生成；若未指明，Omni 模型有待编辑视频时跟随该视频时长，否则默认10秒。</p></li></ul><p>示例值：5。</p><p><strong>audio</strong> <code>boolean</code> （可选）</p><div><div><p><strong>重要</strong>3.0 模型的有声选项会影响费用，请前往<a href="https://bailian.console.aliyun.com/cn-beijing/model/market">百炼控制台</a>查看对应型号的价格；4.0 固定生成有声视频。</p></div></div><p>3.0 模型是否生成有声视频。开启后模型将根据视频内容自动生成匹配的背景音乐或音效。</p><ul><li><code>false</code>：默认值，输出无声视频。</li><li><code>true</code>：输出有声视频。</li></ul><p>注意：</p><ul><li>3.0 Omni 模型传入视频（<code>type=base或feature</code>）时，<code>audio</code>只能设置为<code>false</code>。</li><li><code>kling/kling-v3-turbo-video-generation</code> 固定生成音画同出视频，该字段不生效（恒为生成）。</li><li>两个 4.0 模型固定生成有声视频，传入任何 <code>audio</code> 值均不生效，不能关闭声音。</li></ul><p><strong>watermark</strong> <code>boolean</code> （可选）</p><p>是否同时生成含水印的视频。3.0 模型的水印位于视频右下角，文案固定为”可灵AI”。3.0 和 4.0 模型设置为 <code>true</code> 时，响应中均额外返回 <code>watermark_video_url</code> 字段。</p><ul><li><code>false</code>：默认值，不生成含水印的视频。</li><li><code>true</code>：同时生成含水印的视频。</li></ul></div></section></td><td><p>以下原有示例使用3.0模型及其专属参数，不可仅替换模型名称用于4.0。4.0 请参考末尾两个示例，并按上述参数规则选择素材与设置。</p><a id="sec-tabs"></a><section><a id="文生视频"></a><section><a id="文生视频-h4"></a><h4>文生视频</h4><p>支持模型：<code>kling/kling-v3-turbo-video-generation</code>、<code>kling/kling-v3-video-generation</code>、<code>kling/kling-v3-omni-video-generation</code>。</p><a id="code-block"></a><pre class="language-bash"><code># 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;kling/kling-v3-turbo-video-generation&quot;,
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;一只小猫在月光下奔跑&quot;
    },
    &quot;parameters&quot;: {
        &quot;mode&quot;: &quot;std&quot;,
        &quot;aspect_ratio&quot;: &quot;16:9&quot;,
        &quot;duration&quot;: 5,
        &quot;audio&quot;: false,
        &quot;watermark&quot;: true
    }
}'
</code></pre></section><a id="python-sdk"></a><section><a id="python-sdk-h4"></a><h4>Python SDK</h4><a id="code-block-2"></a><pre class="language-python"><code>import dashscope
import os
from dashscope import DashScopeError

# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;
# 获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
client = dashscope.Client(api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;))

def sample_async_call():
    # 异步提交视频生成任务
    # mode/aspect_ratio/audio 为 parameters 段字段，不在具名签名内，经 parameters 透传
    try:
        job = client.videos.jobs.create(model='kling/kling-v3-turbo-video-generation',
                                        prompt='一只小猫在月光下奔跑',
                                        duration=5,
                                        watermark=True,
                                        parameters={'mode': 'std',
                                                    'aspect_ratio': '16:9',
                                                    'audio': False})
        print(job)
        print(&quot;task_id: %s&quot; % job.task_id)
    except DashScopeError as e:
        print(f&quot;HTTP返回码：{e.status_code}&quot;)
        print(f&quot;错误码：{e.code}&quot;)
        print(f&quot;错误信息：{e.message}&quot;)
        print(&quot;请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code&quot;)
        return

    # 查询任务状态
    try:
        snapshot = client.videos.jobs.fetch(job.task_id)
        print(snapshot.status)
    except DashScopeError as e:
        print(f&quot;HTTP返回码：{e.status_code}&quot;)
        print(f&quot;错误码：{e.code}&quot;)
        print(f&quot;错误信息：{e.message}&quot;)
        print(&quot;请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code&quot;)

    # 等待任务完成
    try:
        done = client.videos.jobs.wait(job)
        print(done)
        print(done.video_url)
    except DashScopeError as e:
        print(f&quot;HTTP返回码：{e.status_code}&quot;)
        print(f&quot;错误码：{e.code}&quot;)
        print(f&quot;错误信息：{e.message}&quot;)
        print(&quot;请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code&quot;)

if __name__ == '__main__':
    sample_async_call()
</code></pre></section><a id="文生视频-智能分镜"></a><section><a id="文生视频-智能分镜-h4"></a><h4>文生视频（智能分镜）</h4><p>支持模型：<code>kling/kling-v3-turbo-video-generation</code>、<code>kling/kling-v3-video-generation</code>、<code>kling/kling-v3-omni-video-generation</code>。</p><a id="code-block-3"></a><pre class="language-bash"><code># 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;kling/kling-v3-video-generation&quot;,
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;&quot;,
        &quot;multi_shot&quot;: true,
        &quot;shot_type&quot;: &quot;customize&quot;,
        &quot;multi_prompt&quot;: [
            {
                &quot;index&quot;: 1,
                &quot;prompt&quot;: &quot;雾岭镇比地图上更小，山雾像棉絮一样堵在街口。邮局背后果然有三棵槐树，第三棵树根旁的泥土被人动过。&quot;,
                &quot;duration&quot;: 5
            },
            {
                &quot;index&quot;: 2,
                &quot;prompt&quot;: &quot;林澈蹲下挖出一个铁盒，里面除了一把生锈的钥匙，还有一盘老旧的录音带。录音机是邮局借的，按下播放键时，父亲的声音从沙沙杂音里爬出来：“如果你听到这段话，说明你已经走到我走过的路上了。&quot;,
                &quot;duration&quot;: 5
            }
        ],
        &quot;media&quot;: [],
        &quot;element_list&quot;: []
    },
    &quot;parameters&quot;: {
        &quot;mode&quot;: &quot;pro&quot;,
        &quot;duration&quot;: 10,
        &quot;audio&quot;: true,
        &quot;aspect_ratio&quot;: &quot;9:16&quot;,
        &quot;watermark&quot;: true
    }
}'
</code></pre></section><a id="图生视频-首帧生视频"></a><section><a id="图生视频-首帧生视频-h4"></a><h4>图生视频（首帧生视频）</h4><p>支持模型：<code>kling/kling-v3-turbo-video-generation</code>、<code>kling/kling-v3-video-generation</code>、<code>kling/kling-v3-omni-video-generation</code>。</p><a id="code-block-4"></a><pre class="language-bash"><code># 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;kling/kling-v3-omni-video-generation&quot;,
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;让图片中的人物动起来，头发被微风吹动&quot;,
        &quot;media&quot;: [
            {
                &quot;type&quot;: &quot;first_frame&quot;,
                &quot;url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260121/zlpocv/wan-i2v-haigui.webp&quot;
            }
        ]
    },
    &quot;parameters&quot;: {
        &quot;mode&quot;: &quot;std&quot;,
        &quot;duration&quot;: 5,
        &quot;audio&quot;: false,
        &quot;watermark&quot;: true
    }
}'
</code></pre></section><a id="图生视频-首尾帧生视频"></a><section><a id="图生视频-首尾帧生视频-h4"></a><h4>图生视频（首尾帧生视频）</h4><p>支持模型：<code>kling/kling-v3-video-generation</code>、<code>kling/kling-v3-omni-video-generation</code>。</p><a id="code-block-5"></a><pre class="language-bash"><code># 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;kling/kling-v3-omni-video-generation&quot;,
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;写实风格，一只黑色小猫好奇地看向天空，镜头从平视逐渐上升，最后俯拍它的好奇的眼神。&quot;,
        &quot;media&quot;: [
            {
                &quot;type&quot;: &quot;first_frame&quot;,
                &quot;url&quot;: &quot;https://wanx.alicdn.com/material/20250318/first_frame.png&quot;
            },
          {
                &quot;type&quot;: &quot;last_frame&quot;,
                &quot;url&quot;: &quot;https://wanx.alicdn.com/material/20250318/last_frame.png&quot;
            }
        ]
    },
    &quot;parameters&quot;: {
        &quot;mode&quot;: &quot;std&quot;,
        &quot;duration&quot;: 5,
        &quot;audio&quot;: false,
        &quot;watermark&quot;: true
    }
}'
</code></pre></section><a id="参考生视频-视频-图像"></a><section><a id="参考生视频-视频-图像-h4"></a><h4>参考生视频（视频+图像）</h4><p>支持模型：<code>kling/kling-v3-omni-video-generation</code>。</p><a id="code-block-6"></a><pre class="language-bash"><code># 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;kling/kling-v3-omni-video-generation&quot;,
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;&lt;&lt;&lt;element_1&gt;&gt;&gt;背景，&lt;&lt;&lt;image_2&gt;&gt;&gt;和&lt;&lt;&lt;image_1&gt;&gt;&gt;握手交谈，&lt;&lt;&lt;video_1&gt;&gt;&gt;人物穿着黑色风衣的侦探站在公寓楼顶，手持望远镜观察街道&quot;,
        &quot;multi_shot&quot;: false,
        &quot;shot_type&quot;: &quot;intelligence&quot;,
        &quot;multi_prompt&quot;: [],
        &quot;media&quot;: [
            {
                &quot;url&quot;: &quot;https://p2-kling.klingai.com/kcdn/cdn-kcdn112452/kling-qa-test/lip_sync_5s.mp4&quot;,
                &quot;type&quot;: &quot;base&quot;,
                &quot;keep_original_sound&quot;: &quot;yes&quot;
            },
            {
                &quot;type&quot;: &quot;refer&quot;,
                &quot;url&quot;: &quot;https://p2-kling.klingai.com/kcdn/cdn-kcdn112452/kling-qa-test/zem_test/yangmi01.jpg&quot;
            },
            {
                &quot;type&quot;: &quot;refer&quot;,
                &quot;url&quot;: &quot;https://p2-kling.klingai.com/kcdn/cdn-kcdn112452/kling-qa-test/human_2.JPG&quot;
            }
        ],
        &quot;element_list&quot;: [
            {
                &quot;element_id&quot;: 171
            }
        ]
    },
    &quot;parameters&quot;: {
        &quot;mode&quot;: &quot;pro&quot;,
        &quot;duration&quot;: 10,
        &quot;audio&quot;: false,
        &quot;aspect_ratio&quot;: &quot;1:1&quot;,
        &quot;watermark&quot;: true
    }
}'
</code></pre></section><a id="kling-4-0-关键帧生视频"></a><section><a id="kling-4-0-关键帧生视频-h4"></a><h4>Kling 4.0 关键帧生视频</h4><p>支持模型：<code>kling/kling-v4-video-generation</code>。以下示例使用首尾帧；也可以仅传中间帧或尾帧。将示例图片 URL 替换为可访问且符合规格的图片地址。</p><a id="code-block-7"></a><pre class="language-bash"><code># 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;kling/kling-v4-video-generation&quot;,
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;镜头从近景缓慢拉远，人物站在海边看向远处，头发被海风吹动，海浪声渐强&quot;,
        &quot;media&quot;: [
            {&quot;type&quot;: &quot;first_frame&quot;, &quot;url&quot;: &quot;https://example.com/first.jpeg&quot;},
            {&quot;type&quot;: &quot;last_frame&quot;, &quot;url&quot;: &quot;https://example.com/last.jpeg&quot;}
        ]
    },
    &quot;parameters&quot;: {
        &quot;mode&quot;: &quot;pro&quot;,
        &quot;duration&quot;: 10,
        &quot;watermark&quot;: false
    }
}'
</code></pre></section><a id="kling-4-0-全能参考生视频"></a><section><a id="kling-4-0-全能参考生视频-h4"></a><h4>Kling 4.0 全能参考生视频</h4><p>支持模型：<code>kling/kling-v4-omni-reference-video-generation</code>。将视频 URL 和 <code>element_id</code> 替换为符合规格、可使用的素材与<a href="kling-object-ids.md">主体 ID</a>。</p><a id="code-block-8"></a><pre class="language-bash"><code># 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;kling/kling-v4-omni-reference-video-generation&quot;,
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;让&lt;&lt;&lt;element_1&gt;&gt;&gt;模仿&lt;&lt;&lt;video_1&gt;&gt;&gt;中的动作，从画面左侧走向镜头，整体保持电影感夜景氛围&quot;,
        &quot;media&quot;: [
            {&quot;type&quot;: &quot;feature&quot;, &quot;url&quot;: &quot;https://example.com/reference.mp4&quot;}
        ],
        &quot;element_list&quot;: [
            {&quot;element_id&quot;: 148}
        ]
    },
    &quot;parameters&quot;: {
        &quot;mode&quot;: &quot;pro&quot;,
        &quot;duration&quot;: 10,
        &quot;aspect_ratio&quot;: &quot;16:9&quot;,
        &quot;watermark&quot;: false
    }
}'
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="kl365a0h4rsp1"></a><a id="kl361a0sersp1"></a><h4>响应参数</h4><p><strong>output</strong> <code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-6"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></td><td><a id="sec-tabs-2"></a><section><a id="成功响应"></a><section><a id="成功响应-h4"></a><h4>成功响应</h4><p>请保存 task_id，用于查询任务状态与结果。</p><a id="code-block-9"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
        &quot;task_status&quot;: &quot;PENDING&quot;,
        &quot;task_id&quot;: &quot;0385dc79-5ff8-4d82-bcb6-xxxxxx&quot;
    },
    &quot;request_id&quot;: &quot;4909100c-7b5a-9f92-bfe5-xxxxxx&quot;
}
</code></pre></section><a id="异常响应"></a><section><a id="异常响应-h4"></a><h4>异常响应</h4><p>创建任务失败，请参见<a href="../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-10"></a><pre class="language-json"><code>{
    &quot;code&quot;: &quot;InvalidApiKey&quot;,
    &quot;message&quot;: &quot;No API-key provided.&quot;,
    &quot;request_id&quot;: &quot;7438d53d-6eb8-4596-8835-xxxxxx&quot;
}
</code></pre></section></section></td></tr></tbody></table>

<a id="步骤2-根据任务id查询结果"></a>

<a id="kl401a0h3stp2"></a>

<a id="kl400a0step2"></a>

### 步骤2：根据任务ID查询结果

**北京地域**：`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`

> **说明**
>
> -   **轮询建议**：视频生成过程约需数分钟，建议采用**轮询**机制，并设置合理的查询间隔（如 15 秒）来获取结果。
> -   **任务状态流转**：PENDING（排队中）→ RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。
> -   **task\_id 有效期**：**24小时**，超时后将无法查询结果，接口将返回任务状态为`UNKNOWN`。
> -   **RPS 限制**：查询接口默认RPS为20。如需更高频查询或事件通知，建议[配置异步任务回调](../../more-about-models/async-task-api.md)。
> -   **更多操作**：如需批量查询、取消任务等操作，请参见[管理异步任务](../../more-about-models/manage-asynchronous-tasks.md)。

<table><tbody><tr><td><a id="kl424a0h4qr01"></a><a id="kl420a0secqry"></a><h4>请求参数</h4><a id="kl434a0h5qr01"></a><h5>请求头（Headers）</h5><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><a id="kl440a0h5qr02"></a><h5>URL路径参数（Path parameters）</h5><p><strong>task_id</strong> <code>string</code><strong>（必选）</strong></p><p>任务ID。</p></td><td><a id="sec-tabs-3"></a><section><a id="查询任务结果"></a><section><a id="查询任务结果-h4"></a><h4>查询任务结果</h4><p>将<code>{task_id}</code>完整替换为上一步接口返回的<code>task_id</code>的值。<code>task_id</code>查询有效期为24小时，并请将<code>{WorkspaceId}</code>替换为真实的<a href="../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain">业务空间ID</a>。</p><a id="code-block-11"></a><pre class="language-bash"><code>curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id} \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="kl448a0h4qrs1"></a><a id="kl444a0seqrsp"></a><h4>响应参数</h4><p><strong>output</strong><code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-7"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值-2"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section><strong>轮询过程中的状态流转：</strong><ul><li>PENDING（排队中） → RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。</li><li>初次查询状态通常为 PENDING（排队中）或 RUNNING（处理中）。</li><li>当状态变为 SUCCEEDED 时，响应中将包含生成的视频URL。</li><li>若状态为 FAILED，请检查错误信息并重试。</li><li>若状态为 CANCELED，表示任务已取消，如需继续请重新提交任务。</li><li>若状态为 UNKNOWN，表示任务不存在或状态未知，可能在 task_id 不存在或超过 24 小时有效期后出现。</li></ul><p><strong>submit_time</strong> <code>string</code></p><p>任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>scheduled_time</strong> <code>string</code></p><p>任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>end_time</strong> <code>string</code></p><p>任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>video_url</strong><code>string</code></p><p>视频URL。仅在 task_status 为 SUCCEEDED 时返回。</p><p>视频格式为MP4（H.264 编码）。视频链接有效期30天，但不建议将其作为长期存储依赖，请及时下载。</p><p><strong>watermark_video_url</strong><code>string</code></p><p>带水印的视频URL，仅在 task_status 为 SUCCEEDED 且启用水印时返回。</p><p>视频格式为MP4（H.264 编码）。视频链接有效期30天，但不建议将其作为长期存储依赖，请及时下载。</p><p><strong>orig_prompt</strong> <code>string</code></p><p>原始输入的prompt，对应请求参数<code>prompt</code>。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></div></section><p><strong>usage</strong> <code>object</code></p><p>输出信息统计，只对成功的结果计数。</p><a id="accordion-属性-8"></a><section><p>属性</p><div><p><strong>duration</strong> <code>number</code></p><p>计费时长（秒）。无视频输入时等于生成视频时长；3.0 Omni 的 <code>base</code> 视频编辑按输入视频时长四舍五入取整计量；4.0 模型有视频输入时等于 max（输入视频总时长，生成视频时长）+ 生成视频时长。</p><p><strong>input_video_duration</strong> <code>number</code></p><p>4.0 模型的输入视频总时长（秒），保留两位小数，包含特征参考视频、待编辑视频与视频角色主体；无视频输入时为0.00。</p><p><strong>output_video_duration</strong> <code>number</code></p><p>4.0 模型生成的视频时长（秒），保留两位小数。</p><p><strong>reference_type</strong> <code>string</code></p><p>4.0 模型存在视频输入（特征参考视频、待编辑视频、视频角色主体任一）时返回 <code>video</code>；无视频输入时不返回该字段。</p><p><strong>size</strong> <code>string</code></p><p>生成视频的分辨率。示例值：1280*720。</p><p><strong>fps</strong> <code>integer</code></p><p>生成视频的帧率。示例值：24。</p><p><strong>SR</strong> <code>string</code></p><p>生成视频的分辨率档位。示例值：720。<code>mode=4k</code>时返回<code>4k</code>；<code>kling/kling-v3-turbo-video-generation</code>仅返回<code>720</code>或<code>1080</code>。</p><p><strong>audio</strong> <code>boolean</code></p><p>生成视频是否为有声视频。示例值：false。<code>kling/kling-v3-turbo-video-generation</code>和两个 4.0 模型恒为<code>true</code>（固定音画同出）。</p><p><strong>video_count</strong> <code>integer</code></p><p>生成视频的数量。固定为1。</p></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p></td><td><a id="sec-tabs-4"></a><section><a id="3-0-任务执行成功"></a><section><a id="3-0-任务执行成功-h4"></a><h4>3.0 任务执行成功</h4><a id="code-block-12"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;340f0d7d-bf7e-4c8f-9c03-xxxxxx&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;24f5c51e-d67b-44dc-9acb-xxxxxx&quot;,
        &quot;task_status&quot;: &quot;SUCCEEDED&quot;,
        &quot;submit_time&quot;: &quot;2026-03-27 21:30:32.575&quot;,
        &quot;scheduled_time&quot;: &quot;2026-03-27 21:30:32.603&quot;,
        &quot;end_time&quot;: &quot;2026-03-27 21:31:09.177&quot;,
        &quot;video_url&quot;: &quot;https://v4-fdl.kechuangai.com/ksc2/xxx.mp4?xxxx&quot;,
        &quot;watermark_video_url&quot;: &quot;https://v2-fdl.kechuangai.com/ksc2/xxx.mp4?xxxx&quot;
    },
    &quot;usage&quot;: {
        &quot;duration&quot;: 5,
        &quot;size&quot;: &quot;1280*720&quot;,
        &quot;fps&quot;: 24,
        &quot;video_count&quot;: 1,
        &quot;audio&quot;: false,
        &quot;SR&quot;: &quot;720&quot;
    }
}
</code></pre></section><a id="4-0-任务执行成功"></a><section><a id="4-0-任务执行成功-h4"></a><h4>4.0 任务执行成功</h4><p>以下示例为传入参考视频的 4.0 Omni 任务。无视频输入时，<code>input_video_duration</code> 为0.00，且不返回 <code>reference_type</code>。</p><a id="code-block-13"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;bd547b6a-be36-9a46-857f-xxxxxxxxxxxx&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;6c44c3ee-9c48-462b-8186-xxxxxxxxxxxx&quot;,
        &quot;task_status&quot;: &quot;SUCCEEDED&quot;,
        &quot;submit_time&quot;: &quot;2026-11-16 15:53:34.236&quot;,
        &quot;scheduled_time&quot;: &quot;2026-11-16 15:53:34.309&quot;,
        &quot;end_time&quot;: &quot;2026-11-16 15:54:20.367&quot;,
        &quot;video_url&quot;: &quot;https://v4-fdl.kechuangai.com/ksc2/xxx.mp4?xxxx&quot;,
        &quot;watermark_video_url&quot;: &quot;https://v4-fdl.kechuangai.com/ksc2/xxx.mp4?xxxx&quot;
    },
    &quot;usage&quot;: {
        &quot;video_count&quot;: 1,
        &quot;SR&quot;: &quot;720&quot;,
        &quot;duration&quot;: 7.63,
        &quot;input_video_duration&quot;: 4.63,
        &quot;output_video_duration&quot;: 3.0,
        &quot;reference_type&quot;: &quot;video&quot;,
        &quot;size&quot;: &quot;940*940&quot;,
        &quot;audio&quot;: true,
        &quot;fps&quot;: 24
    }
}
</code></pre></section><a id="任务执行失败"></a><section><a id="任务执行失败-h4"></a><h4>任务执行失败</h4><p>若任务执行失败，task_status将置为 FAILED，并提供错误码和信息。请参见<a href="../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-14"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;e5d70b02-ebd3-98ce-9fe8-759d7d7b107d&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;86ecf553-d340-4e21-af6e-a0c6a421c010&quot;,
        &quot;task_status&quot;: &quot;FAILED&quot;,
        &quot;code&quot;: &quot;InvalidParameter&quot;,
        &quot;message&quot;: &quot;The parameter is invalid xxxxxx&quot;
    }
}
</code></pre></section><a id="任务查询过期"></a><section><a id="任务查询过期-h4"></a><h4>任务查询过期</h4><p>task_id查询有效期为 24 小时，超时后将无法查询，返回以下报错信息。</p><a id="code-block-15"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;a4de7c32-7057-9f82-8581-xxxxxx&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;502a00b1-19d9-4839-a82f-xxxxxx&quot;,
        &quot;task_status&quot;: &quot;UNKNOWN&quot;
    }
}
</code></pre></section></section></td></tr></tbody></table>

<a id="错误码"></a>

<a id="OajFO"></a>

<a id="b3533d7d91okm"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](../../preparations/error-code.md)进行解决。
