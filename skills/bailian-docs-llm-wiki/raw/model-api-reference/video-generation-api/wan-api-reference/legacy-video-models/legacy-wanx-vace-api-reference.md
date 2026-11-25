# 万相-视频编辑API参考（2.1）

万相2.1-视频编辑统一模型支持文本、图像、视频等多种模态输入，可执行多种视频生成与编辑任务。

**相关文档**：[使用指南](../../../../model-user-guide/use-cases/legacy-resources/legacy-video-generation/wan-vace-guide.md)

<a id="适用范围"></a>

<a id="1fd78afa5brlj"></a>

## 适用范围

为确保调用成功，请务必保证模型、Endpoint URL 和 API Key 均属于**同一地域**。跨地域调用将会失败。

-   [**选择模型**](../../../../model-user-guide/use-cases/legacy-resources/legacy-video-generation/wan-vace-guide.md#scope-title)：确认模型所属的地域。
-   **选择 URL**：选择对应的地域 Endpoint URL，支持HTTP URL。
-   **配置 API Key**：选择地域并[获取与配置 API Key](../../../preparations/get-api-key.md)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

> **说明**
>
> 本文的示例代码适用于**北京地域**。

> **重要**
>
> 阿里云百炼为华北2（北京）、新加坡地域推出了业务空间专属域名，**能够为推理请求提供卓越的性能和更高的稳定性**，建议迁移至新域名：
>
> -   华北2（北京）地域：从 `https://dashscope.aliyuncs.com` 迁移至 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
> -   新加坡地域：从 `https://dashscope-intl.aliyuncs.com` 迁移至 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`
>
> 其中 `{WorkspaceId}` 为您的业务空间 ID，可在阿里云百炼控制台的**业务空间详情**页面查看。现有域名仍可正常使用。

<a id="http调用"></a>

<a id="42703589880ts"></a>

## HTTP调用

视频编辑统一模型的处理耗时较长（约5-10分钟），API采用异步调用的方式。整个流程包含 **“创建任务 -> 轮询获取”** 两个核心步骤，具体如下：

<a id="步骤1-创建任务获取任务id"></a>

<a id="db8cf70432oe3"></a>

### 步骤1：创建任务获取任务ID

<a id="sec-tabs"></a>

<a id="北京"></a>

<a id="北京-h4"></a>

#### 北京

`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="新加坡"></a>

<a id="新加坡-h4"></a>

#### 新加坡

`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<table><tbody><tr><td><a id="afcd41d2b57zf"></a><h4>请求参数</h4><a id="79473e45c592d"></a><h5>请求头（Headers）</h5><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><p><strong>X-DashScope-Async</strong><code>string</code><strong>（必选）</strong></p><p>异步处理配置参数。HTTP请求只支持异步，<strong>必须设置为</strong><code>enable</code>。</p><div><div><p><strong>重要</strong>缺少此请求头将报错：“current user api does not support synchronous calls”。</p></div></div><a id="66a778d4fbfub"></a><h5>请求体（Request Body）</h5><a id="sec-tabs-2"></a><section><a id="多图参考"></a><section><a id="多图参考-h4"></a><h4>多图参考</h4><p><strong>model</strong> <code>string</code> <strong>（必选）</strong></p><p>模型名称。示例值：wanx2.1-vace-plus。</p><table><tbody><tr><td><p><strong>input</strong> <code>object</code> <strong>（必选）</strong></p><p>输入的基本信息，如提示词等。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>prompt</strong><code>string</code><strong>（必选）</strong></p><p>提示词，用来描述生成视频中期望包含的元素和视觉特点。</p><p>支持中英文，长度不超过800个字符，每个汉字/字母占一个字符，超过部分会自动截断。</p><p>提示词技巧请参见<a href="../../../../model-user-guide/use-cases/text-to-video-prompt.md">文生视频/图生视频Prompt指南</a>。</p><p><strong>function</strong><code>string</code><strong>（必选）</strong></p><p>功能名称。多图参考设置为<code>image_reference</code>。</p><p>多图参考支持最多3张参考图。图像内容可以包括主体与背景，例如人物、动物、服饰、场景等。使用 <code>prompt</code> 描述期望生成的视频画面内容，模型可将多张图片融合生成连贯的视频内容。</p><p><strong>ref_images_url</strong><code>array[string]</code> <strong>（必选）</strong></p><p>输入参考图像的URL 数组。</p><ol><li><p>公网URL：</p><ul><li>支持 HTTP 和 HTTPS 协议。</li><li>示例值：<a href="https://xxx/xxx.mp3"></a><a href="https://xxx/xxx.mp3">https://xxx/xxx.mp3</a>。</li></ul></li><li><p>临时URL：</p><ul><li>支持OSS协议，必须通过<a href="../../../more-about-models/get-temporary-file-url.md">上传文件获取临时 URL</a>。</li><li>示例值：oss://dashscope-instant/xxx/xxx.mp3。</li></ul></li></ol><p>参考图像支持<strong>1-3 张</strong>图像，若超过 3 张，则仅保留前 3 张作为输入。</p><p>图像限制：</p><ul><li>图像格式：JPG、JPEG、PNG、BMP、TIFF、WEBP。</li><li>图像分辨率：图像的宽和高范围在[360, 2000]，单位像素。</li><li>图像大小：不超过10MB。</li><li>URL地址中不能包含中文字符。</li></ul><p>使用建议：</p><ul><li>若使用参考图像中的主体时，建议每张图像中仅包含一个主体。背景建议为纯色（如白色或单一颜色），以便更好地突出主体。</li><li>若使用参考图像的背景时，背景图像最多只有一张，且背景图像中不包含任何主体对象。</li></ul></div></section></td></tr><tr><td><p><strong>parameters</strong> <code>object</code> （可选）</p><p>视频处理参数，如设置水印等。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>obj_or_bg</strong> <code>array[string]</code> （可选）</p><p>该参数用于标识每张参考图像的用途，与 <code>ref_images_url</code> 参数一一对应。数组中每个元素表示对应位置的图像为“主体”还是“背景”：</p><ul><li><code>obj</code>：表示该图像作为主体参考。</li><li><code>bg</code>：表示该图像作为背景参考 （最多仅允许一个）。</li></ul><p>使用说明：</p><ul><li>建议传入该参数，且长度必须与 <code>ref_images_url</code>保持一致，否则将报错。</li><li>仅当 <code>ref_images_url</code>为单元素数组时，可不传，此时默认值为 <code>[&quot;obj&quot;]</code>。</li></ul><p>示例值： [&quot;obj&quot;, &quot;obj&quot;, &quot;bg&quot;]。</p><p><strong>size</strong> <code>string</code> （可选）</p><p>生成视频的分辨率（宽*高）。目前支持生成720P 视频，分辨率的取值为：</p><ul><li><code>1280*720</code>（默认值）：视频宽高比为16:9。其中，1280代表宽度，720代表高度。</li><li><code>720*1280</code>：视频宽高比为9:16。</li><li><code>960*960</code>：视频宽高比为1:1。</li><li><code>832*1088</code>：视频宽高比为3:4。</li><li><code>1088*832</code>：视频宽高比为4:3。</li></ul><p><strong>duration</strong> <code>integer</code> （可选）</p><p>视频生成时长，单位为秒。当前参数值固定为5，且不支持修改。模型将始终生成5秒时长的视频。</p><p><strong>prompt_extend</strong><code>bool</code> （可选）</p><p>是否开启prompt智能改写。开启后使用大模型对输入prompt进行智能改写。对于较短的prompt生成效果提升明显，但会增加耗时。</p><ul><li><code>true</code>（默认值）：开启智能改写。</li><li><code>false</code>：关闭智能改写。</li></ul><p><strong>seed</strong><code>integer</code>（可选）</p><p>随机数种子，用于控制模型生成内容的随机性。seed参数取值范围是<code>[0, 2147483647]</code>。</p><p>如果不提供，则算法自动生成一个随机数作为种子。如果您希望生成内容保持相对稳定，请使用相同的seed参数值。</p><p><strong>watermark</strong> <code>bool</code>（可选）</p><p>是否添加水印标识，水印位于图片右下角，文案为“AI生成”。</p><ul><li><code>false</code>（默认值）：不添加水印。</li><li><code>true</code>：添加水印。</li></ul></div></section></td></tr></tbody></table></section><a id="视频重绘"></a><section><a id="视频重绘-h4"></a><h4>视频重绘</h4><p><strong>model</strong> <code>string</code> <strong>（必选）</strong></p><p>模型名称。示例值：wanx2.1-vace-plus。</p><table><tbody><tr><td><p><strong>input</strong> <code>object</code> <strong>（必选）</strong></p><p>输入的基本信息，如提示词等。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>prompt</strong><code>string</code><strong>（必选）</strong></p><p>提示词，用来描述生成视频中期望包含的元素和视觉特点。</p><p>支持中英文，长度不超过800个字符，每个汉字/字母占一个字符，超过部分会自动截断。</p><p>提示词技巧请参见<a href="../../../../model-user-guide/use-cases/text-to-video-prompt.md">文生视频/图生视频Prompt指南</a>。</p><p><strong>function</strong><code>string</code><strong>（必选）</strong></p><p>功能名称。视频重绘设置为 <code>video_repainting</code>。</p><p>视频重绘支持从输入视频中提取主体姿态与动作、构图与运动轮廓以及线稿结构，结合文本提示词（prompt），生成具有相同动态特征的新视频。同时，还支持通过参考图像替换原视频中的主体，例如更换角色形象但仍保留原有动作。</p><p><strong>video_url</strong><code>string</code> <strong>（必选）</strong></p><p>输入视频的URL地址。</p><ol><li><p>公网URL：</p><ul><li>支持 HTTP 和 HTTPS 协议。</li><li>示例值：<a href="https://xxx/xxx.mp3"></a><a href="https://xxx/xxx.mp3">https://xxx/xxx.mp3</a>。</li></ul></li><li><p>临时URL：</p><ul><li>支持OSS协议，必须通过<a href="../../../more-about-models/get-temporary-file-url.md">上传文件获取临时 URL</a>。</li><li>示例值：oss://dashscope-instant/xxx/xxx.mp3。</li></ul></li></ol><p>视频限制：</p><ul><li>视频格式：MP4。</li><li>视频帧率：大于等于16FPS。</li><li>视频大小：不超过50MB。</li><li>视频长度：不超过5秒，否则取视频的前5秒。</li><li>URL地址中不能包含中文字符。</li></ul><p>关于输出视频的分辨率：</p><ul><li>若输入视频分辨率 ≤ 720P，输出将保留原始分辨率；</li><li>若输入视频分辨率 &gt; 720P，则在保持原视频宽高比的前提下，按比例缩放至不超过 720P。</li></ul><p>关于输出视频的时长：</p><ul><li>输出视频时长与输入视频一致，最长不超过 5 秒。</li><li>示例：若输入视频为 3 秒，则输出也为 3 秒；若输入为 6 秒，则输出为前 5 秒。</li></ul><p><strong>ref_images_url</strong><code>array[string]</code> （可选）</p><p>输入参考图像的 URL数组。</p><ol><li><p>公网URL：</p><ul><li>支持 HTTP 和 HTTPS 协议。</li><li>示例值：<a href="https://xxx/xxx.mp3"></a><a href="https://xxx/xxx.mp3">https://xxx/xxx.mp3</a>。</li></ul></li><li><p>临时URL：</p><ul><li>支持OSS协议，必须通过<a href="../../../more-about-models/get-temporary-file-url.md">上传文件获取临时 URL</a>。</li><li>示例值：oss://dashscope-instant/xxx/xxx.mp3。</li></ul></li></ol><p>仅支持传入<strong>1张</strong>参考图像，且该图像建议为主体图像，用于替换输入视频中的主体内容。</p><p>图像限制：</p><ul><li>图像格式：JPG、JPEG、PNG、BMP、TIFF、WEBP。</li><li>图像分辨率：图像的宽度和高度范围为[360, 2000]，单位为像素。</li><li>图像大小：不超过10MB。</li><li>URL地址中不能包含中文字符。</li></ul><p>使用建议：</p><ul><li>若使用参考图像中的主体时，建议每张图像仅包含一个主体。背景建议为纯色（如白色或单一颜色），以便更好地突出主体。</li></ul></div></section></td></tr><tr><td><p><strong>parameters</strong> <code>object</code> <strong>（必选）</strong></p><p>视频处理参数，如设置水印等。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>control_condition</strong> <code>string</code> <strong>（必选）</strong></p><p>设置视频特征提取的方式。</p><ul><li><code>posebodyface</code>：提取输入视频中主体的脸部表情和肢体动作，适用于需保留主体表情细节的场景。</li><li><code>posebody</code>：提取输入视频中主体的肢体动作（不含脸部表情），适用于只需要控制主体身体动作的场景。</li><li><code>depth</code>：提取输入视频的构图和运动轮廓。</li><li><code>scribble</code>：提取输入视频的线稿结构。</li></ul><p><strong>strength</strong> <code>float</code> （可选）</p><p>调节 <code>control_condition</code> 所指定的视频特征提取方式对生成视频的控制强度。</p><p>默认值为1.0，取值范围[0.0, 1.0]。</p><p>数值越大，生成视频越贴近原视频动作和构图；数值越小，生成内容越自由。</p><p><strong>prompt_extend</strong><code>bool</code> （可选）</p><p>是否开启prompt智能改写。开启后使用大模型对输入prompt进行智能改写。对于较短的prompt生成效果提升明显，但会增加耗时。</p><ul><li><code>true</code>（默认值）：开启智能改写。</li><li><code>false</code>：关闭智能改写。<strong>（推荐）</strong></li></ul><blockquote><p>当文本描述与输入的视频内容不一致时，模型可能产生误解。建议手动关闭智能扩写，并在 <code>prompt</code> 中提供清晰、具体的画面描述，以提升生成一致性与准确性。</p></blockquote><p><strong>seed</strong><code>integer</code>（可选）</p><p>随机数种子，用于控制模型生成内容的随机性。seed参数取值范围是<code>[0, 2147483647]</code>。</p><p>如果不提供，则算法自动生成一个随机数作为种子。如果您希望生成内容保持相对稳定，请使用相同的seed参数值。</p><p><strong>watermark</strong> <code>bool</code>（可选）</p><p>是否添加水印标识，水印位于图片右下角，文案为“AI生成”。</p><ul><li><code>false</code>（默认值）：不添加水印。</li><li><code>true</code>：添加水印。</li></ul></div></section></td></tr></tbody></table></section><a id="局部编辑"></a><section><a id="局部编辑-h4"></a><h4>局部编辑</h4><p><strong>model</strong> <code>string</code> <strong>（必选）</strong></p><p>模型名称。示例值：wanx2.1-vace-plus。</p><table><tbody><tr><td><p><strong>input</strong> <code>object</code> <strong>（必选）</strong></p><p>输入的基本信息，如提示词等。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>prompt</strong><code>string</code><strong>（必选）</strong></p><p>提示词，用来描述生成视频中期望包含的元素和视觉特点。</p><p>支持中英文，长度不超过800个字符，每个汉字/字母占一个字符，超过部分会自动截断。</p><p>提示词技巧请参见<a href="../../../../model-user-guide/use-cases/text-to-video-prompt.md">文生视频/图生视频Prompt指南</a>。</p><p><strong>function</strong><code>string</code><strong>（必选）</strong></p><p>功能名称。局部编辑设置为 <code>video_edit</code>。</p><p>局部编辑支持对输入视频的指定区域进行增加、修改或删除元素，还可以对编辑区域的主体或背景进行替换，实现精细化的视频编辑。</p><p><strong>video_url</strong><code>string</code> <strong>（必选）</strong></p><p>输入视频的URL地址。</p><ol><li><p>公网URL：</p><ul><li>支持 HTTP 和 HTTPS 协议。</li><li>示例值：<a href="https://xxx/xxx.mp3"></a><a href="https://xxx/xxx.mp3">https://xxx/xxx.mp3</a>。</li></ul></li><li><p>临时URL：</p><ul><li>支持OSS协议，必须通过<a href="../../../more-about-models/get-temporary-file-url.md">上传文件获取临时 URL</a>。</li><li>示例值：oss://dashscope-instant/xxx/xxx.mp3。</li></ul></li></ol><p>视频限制：</p><ul><li>视频格式：MP4。</li><li>视频帧率：大于等于16FPS。</li><li>视频大小：不超过50MB。</li><li>视频长度：不超过5秒，否则取视频的前5秒。</li><li>URL地址中不能包含中文字符。</li></ul><p>关于输出视频的分辨率：</p><ul><li>若输入视频分辨率 ≤ 720P，输出将保留原始分辨率；</li><li>若输入视频分辨率 &gt; 720P，则在保持原视频宽高比的前提下，按比例缩放至不超过 720P。</li></ul><p>关于输出视频的时长：</p><ul><li>输出视频时长与输入视频一致，最长不超过 5 秒。</li><li>示例：若输入视频为 3 秒，则输出也为 3 秒；若输入为 6 秒，则输出为前 5 秒。</li></ul><p><strong>ref_images_url</strong><code>array[string]</code> （可选）</p><p>输入参考图像的URL数组。</p><ol><li><p>公网URL：</p><ul><li>支持 HTTP 和 HTTPS 协议。</li><li>示例值：<a href="https://xxx/xxx.mp3"></a><a href="https://xxx/xxx.mp3">https://xxx/xxx.mp3</a>。</li></ul></li><li><p>临时URL：</p><ul><li>支持OSS协议，必须通过<a href="../../../more-about-models/get-temporary-file-url.md">上传文件获取临时 URL</a>。</li><li>示例值：oss://dashscope-instant/xxx/xxx.mp3。</li></ul></li></ol><p>当前仅支持传入 <strong>1 张</strong>参考图像 ，该图像可作为主体或背景使用，用于替换输入视频中的对应内容。</p><p>图像限制：</p><ul><li>图像格式：JPG、JPEG、PNG、BMP、TIFF、WEBP。</li><li>图像分辨率：图像的宽度和高度范围为[360, 2000]，单位为像素。</li><li>图像大小：不超过10MB。</li><li>URL地址中不能包含中文字符。</li></ul><p>使用建议：</p><ul><li>若使用参考图像中的主体时，建议每张图像中仅包含一个主体。背景建议为纯色（如白色或单一颜色），以便更好地突出主体。</li><li>若使用参考图像的背景时，背景图像中不包含任何主体对象。</li></ul><p><strong>mask_image_url</strong><code>string</code> （可选）</p><p>掩码图像的URL地址。</p><ol><li><p>公网URL：</p><ul><li>支持 HTTP 和 HTTPS 协议。</li><li>示例值：<a href="https://xxx/xxx.mp3"></a><a href="https://xxx/xxx.mp3">https://xxx/xxx.mp3</a>。</li></ul></li><li><p>临时URL：</p><ul><li>支持OSS协议，必须通过<a href="../../../more-about-models/get-temporary-file-url.md">上传文件获取临时 URL</a>。</li><li>示例值：oss://dashscope-instant/xxx/xxx.mp3。</li></ul></li></ol><p>该参数用于指定视频的编辑区域。与 <code>mask_video_url</code> 参数二选一填写，<strong>推荐优先使用此参数</strong> 。</p><p>掩码图像的白色区域（像素值严格为 [255, 255, 255]）表示需要编辑的部分；黑色区域（像素值严格为 [0, 0, 0]）表示保留不变的区域。</p><p>图像限制：</p><ul><li>图像格式：JPG、JPEG、PNG、BMP、TIFF、WEBP。</li><li>图像分辨率：和输入视频（<code>video_url</code>）分辨率严格相同。</li><li>图像大小：不超过10MB。</li><li>URL地址中不能包含中文字符。</li></ul><p><strong>mask_frame_id</strong><code>integer</code> （可选）</p><p>当 <code>mask_image_url</code> 不为空时，该参数生效，用于标识掩码目标出现在视频中的哪一帧，以“帧 ID”表示。</p><p>默认值为 1，单位为帧，表示视频的第一帧（首帧）。</p><p>取值范围为<code>[1, max_frame_id]</code>，其中<code>max_frame_id=输入视频帧率*输入视频时长+1</code>。</p><blockquote><p>例如，输入视频（<code>video_url</code>）帧率为16FPS，表示每秒 16 帧，视频时长为5秒，因此输入视频的总帧数为16*5+1=81，即max_frame_id=81。</p></blockquote><p><strong>mask_video_url</strong><code>string</code> （可选）</p><p>掩码视频的URL地址。</p><ol><li><p>公网URL：</p><ul><li>支持 HTTP 和 HTTPS 协议。</li><li>示例值：<a href="https://xxx/xxx.mp3"></a><a href="https://xxx/xxx.mp3">https://xxx/xxx.mp3</a>。</li></ul></li><li><p>临时URL：</p><ul><li>支持OSS协议，必须通过<a href="../../../more-about-models/get-temporary-file-url.md">上传文件获取临时 URL</a>。</li><li>示例值：oss://dashscope-instant/xxx/xxx.mp3。</li></ul></li></ol><p>该参数用于指定视频的编辑区域。与<code>mask_image_url</code>参数，二选一填写。</p><p>掩码视频的视频格式、帧率、分辨率、长度需与输入视频（<code>video_url</code>）完全一致。</p><p>掩码视频的白色区域（像素值严格为 [255, 255, 255]）表示需要编辑的部分；黑色区域（像素值严格为 [0, 0, 0]）表示保留不变的区域。</p></div></section></td></tr><tr><td><p><strong>parameters</strong> <code>object</code> （可选）</p><p>视频处理参数，如设置水印等。</p><a id="accordion-属性-6"></a><section><p>属性</p><div><p><strong>control_condition</strong> <code>string</code> （可选）</p><p>设置视频特征提取的方式。默认为&quot;&quot;，表示不做任何提取。</p><ul><li><code>posebodyface</code>：提取输入视频的主体的脸部表情和肢体动作，适用于主体脸部在画面中占比较大、特征清晰可见的场景。</li><li><code>depth</code>：提取输入视频的构图和运动轮廓。</li></ul><p><strong>mask_type</strong> <code>string</code> （可选）</p><p>当 <code>mask_image_url</code> 不为空时，该参数生效，用于指定编辑区域的行为方式。</p><ul><li><code>tracking</code>（默认值）：编辑区域将根据目标物体的运动轨迹动态跟随，适用于主体运动场景。</li><li><code>fixed</code> ：编辑区域保持固定不变，不会随画面内容变化。</li></ul><p><strong>expand_ratio</strong> <code>float</code> （可选）</p><p>当 <code>mask_type</code> 为 <code>tracking</code> 时，该参数生效，表示对掩码区域进行向外扩展的比例。</p><p>取值范围为 [0.0, 1.0]，默认值为 0.05。推荐使用默认值。</p><p>取值越小，掩码区域越贴合目标物体；取值越大，掩码区域的扩展范围越广。</p><p><strong>expand_mode</strong> <code>string</code> （可选）</p><p>当 <code>mask_type</code> 为 <code>tracking</code> 时，该参数生效，表示掩码区域的形状。</p><p>算法会根据选择的<code>expand_mode</code>，基于输入的掩码图像生成对应形状的掩码视频。支持的取值如下：</p><ul><li><code>hull</code>（默认值）：多边形模式，表示使用一个多边形包裹掩码目标。</li><li><code>bbox</code>：边界框模式，表示使用一个矩形包裹掩码目标。</li><li><code>original</code>：原始模式，表示尽量保持与原始掩码目标的形状一致。</li></ul><p><strong>size</strong> <code>string</code> （可选）</p><p>生成视频的分辨率（宽*高）。目前支持生成720P 视频，分辨率的取值为：</p><ul><li><code>1280*720</code>（默认值）：视频宽高比为16:9。其中，1280代表宽度，720代表高度。</li><li><code>720*1280</code>：视频宽高比为9:16。</li><li><code>960*960</code>：视频宽高比为1:1。</li><li><code>832*1088</code>：视频宽高比为3:4。</li><li><code>1088*832</code>：视频宽高比为4:3。</li></ul><p><strong>duration</strong> <code>integer</code> （可选）</p><p>视频生成时长，单位为秒。当前参数值固定为5，且不支持修改。模型将始终生成5秒时长的视频。</p><p><strong>prompt_extend</strong><code>bool</code> （可选）</p><p>是否开启prompt智能改写。开启后使用大模型对输入prompt进行智能改写。对于较短的prompt生成效果提升明显，但会增加耗时。</p><ul><li><code>true</code>（默认值）：开启智能改写。</li><li><code>false</code>：关闭智能改写。<strong>（推荐）</strong></li></ul><blockquote><p>当文本描述与输入的视频内容不一致时，模型可能产生误解。建议手动关闭智能扩写，并在 <code>prompt</code> 中提供清晰、具体的画面描述，以提升生成一致性与准确性。</p></blockquote><p><strong>seed</strong><code>integer</code>（可选）</p><p>随机数种子，用于控制模型生成内容的随机性。seed参数取值范围是<code>[0, 2147483647]</code>。</p><p>如果不提供，则算法自动生成一个随机数作为种子。如果您希望生成内容保持相对稳定，请使用相同的seed参数值。</p><p><strong>watermark</strong> <code>bool</code>（可选）</p><p>是否添加水印标识，水印位于图片右下角，文案为“AI生成”。</p><ul><li><code>false</code>（默认值）：不添加水印。</li><li><code>true</code>：添加水印。</li></ul></div></section></td></tr></tbody></table></section><a id="视频延展"></a><section><a id="视频延展-h4"></a><h4>视频延展</h4><p><strong>model</strong> <code>string</code> <strong>（必选）</strong></p><p>模型名称。示例值：wanx2.1-vace-plus。</p><table><tbody><tr><td><p><strong>input</strong> <code>object</code> <strong>（必选）</strong></p><p>输入的基本信息，如提示词等。</p><a id="accordion-属性-7"></a><section><p>属性</p><div><p><strong>prompt</strong><code>string</code><strong>（必选）</strong></p><p>提示词，用来描述生成视频中期望包含的元素和视觉特点。</p><p>支持中英文，长度不超过800个字符，每个汉字/字母占一个字符，超过部分会自动截断。</p><p>提示词技巧请参见<a href="../../../../model-user-guide/use-cases/text-to-video-prompt.md">文生视频/图生视频Prompt指南</a>。</p><p><strong>function</strong><code>string</code><strong>（必选）</strong></p><p>功能名称。视频延展设置为 <code>video_extension</code>。</p><p>视频延展支持基于图像或视频生成延续性内容，还支持通过参考视频提取动态特征（如动作、构图等），用于指导生成具有相似运动表现的视频。</p><blockquote><p>延长后的视频总时长为 5 秒 ，请注意：这是指最终输出视频的完整时长为 5 秒，而非在原视频基础上延长 5 秒。</p></blockquote><p><strong>first_frame_url</strong><code>string</code> （可选）</p><p>首帧图像的URL地址。</p><ol><li><p>公网URL：</p><ul><li>支持 HTTP 和 HTTPS 协议。</li><li>示例值：<a href="https://xxx/xxx.mp3"></a><a href="https://xxx/xxx.mp3">https://xxx/xxx.mp3</a>。</li></ul></li><li><p>临时URL：</p><ul><li>支持OSS协议，必须通过<a href="../../../more-about-models/get-temporary-file-url.md">上传文件获取临时 URL</a>。</li><li>示例值：oss://dashscope-instant/xxx/xxx.mp3。</li></ul></li></ol><p>图像限制：</p><ul><li>图像格式：JPG、JPEG、PNG、BMP、TIFF、WEBP。</li><li>图像分辨率：图像的宽和高范围在[360, 2000]，单位像素。</li><li>图像大小：不超过10MB。</li><li>URL地址中不能包含中文字符。</li></ul><p><strong>last_frame_url</strong><code>string</code>（可选）</p><p>尾帧图像的URL地址。</p><ol><li><p>公网URL：</p><ul><li>支持 HTTP 和 HTTPS 协议。</li><li>示例值：<a href="https://xxx/xxx.mp3"></a><a href="https://xxx/xxx.mp3">https://xxx/xxx.mp3</a>。</li></ul></li><li><p>临时URL：</p><ul><li>支持OSS协议，必须通过<a href="../../../more-about-models/get-temporary-file-url.md">上传文件获取临时 URL</a>。</li><li>示例值：oss://dashscope-instant/xxx/xxx.mp3。</li></ul></li></ol><p>图像限制：</p><ul><li>图像格式：JPG、JPEG、PNG、BMP、TIFF、WEBP。</li><li>图像分辨率：图像的宽和高范围在[360, 2000]，单位像素。</li><li>图像大小：不超过10MB。</li><li>URL地址中不能包含中文字符。</li></ul><p><strong>first_clip_url</strong><code>string</code> （可选）</p><p>首段视频的URL地址。</p><ol><li><p>公网URL：</p><ul><li>支持 HTTP 和 HTTPS 协议。</li><li>示例值：<a href="https://xxx/xxx.mp3"></a><a href="https://xxx/xxx.mp3">https://xxx/xxx.mp3</a>。</li></ul></li><li><p>临时URL：</p><ul><li>支持OSS协议，必须通过<a href="../../../more-about-models/get-temporary-file-url.md">上传文件获取临时 URL</a>。</li><li>示例值：oss://dashscope-instant/xxx/xxx.mp3。</li></ul></li></ol><p>视频限制：</p><ul><li>视频格式：MP4。</li><li>视频帧率：大于等于16FPS。当<code>first_clip_url</code>和<code>last_clip_url</code>同时使用时，建议两个片段的帧率保持一致。</li><li>视频大小：不超过50MB。</li><li>视频长度：不超过3秒，否则取视频的前3秒。若同时填写<code>first_clip_url</code>和<code>last_clip_url</code>时，两段视频的总时长不超过3秒。</li><li>URL地址中不能包含中文字符。</li></ul><p>关于输出视频的分辨率：</p><ul><li>若输入视频分辨率 ≤ 720P，输出将保留原始分辨率；</li><li>若输入视频分辨率 &gt; 720P，则在保持原视频宽高比的前提下，按比例缩放至不超过 720P。</li></ul><p><strong>last_clip_url</strong><code>string</code>（可选）</p><p>尾段视频的URL地址。</p><ol><li><p>公网URL：</p><ul><li>支持 HTTP 和 HTTPS 协议。</li><li>示例值：<a href="https://help-static-aliyun-doc.aliyuncs.com/xxx.mp3"></a><a href="https://help-static-aliyun-doc.aliyuncs.com/xxx.mp3">https://help-static-aliyun-doc.aliyuncs.com/xxx.mp3</a>。</li></ul></li><li><p>临时URL：</p><ul><li>支持OSS协议，必须通过<a href="../../../more-about-models/get-temporary-file-url.md">上传文件获取临时 URL</a>。</li><li>示例值：oss://dashscope-instant/xxx/xxx.mp3。</li></ul></li></ol><p>视频限制：</p><ul><li>视频格式：MP4。</li><li>视频帧率：大于等于16FPS。当<code>first_clip_url</code>和<code>last_clip_url</code>同时使用时，建议两个片段的帧率保持一致。</li><li>视频大小：不超过50MB。</li><li>视频长度：不超过3秒，否则取视频的前3秒。若同时填写<code>first_clip_url</code>和<code>last_clip_url</code>时，两段视频的总时长不超过3秒。</li><li>URL地址中不能包含中文字符。</li></ul><p>关于输出视频的分辨率：</p><ul><li>若输入视频分辨率 ≤ 720P，输出将保留原始分辨率；</li><li>若输入视频分辨率 &gt; 720P，则在保持原视频宽高比的前提下，按比例缩放至不超过 720P。</li></ul><p><strong>video_url</strong><code>string</code> （可选）</p><p>输入视频的URL地址。</p><ol><li><p>公网URL：</p><ul><li>支持 HTTP 和 HTTPS 协议。</li><li>示例值：<a href="https://help-static-aliyun-doc.aliyuncs.com/xxx.mp3"></a><a href="https://help-static-aliyun-doc.aliyuncs.com/xxx.mp3">https://help-static-aliyun-doc.aliyuncs.com/xxx.mp3</a>。</li></ul></li><li><p>临时URL：</p><ul><li>支持OSS协议，必须通过<a href="../../../more-about-models/get-temporary-file-url.md">上传文件获取临时 URL</a>。</li><li>示例值：oss://dashscope-instant/xxx/xxx.mp3。</li></ul></li></ol><p>该视频主要用于提取其中的运动特征，与 <code>first_frame_url</code> 、 <code>last_frame_url</code> 、<code>first_clip_url</code> 、 <code>last_clip_url</code>参数配合使用，以指导生成具有相似运动表现的延展视频。</p><p>视频限制：</p><ul><li>视频格式：MP4。</li><li>视频帧率：大于等于16FPS，与前后片段保持一致。</li><li>视频分辨率：与前后帧、前后片段保持一致。</li><li>视频大小：不超过50MB。</li><li>视频长度：不超过5秒，否则取视频的前5秒。</li><li>URL地址中不能包含中文字符。</li></ul></div></section></td></tr><tr><td><p><strong>parameters</strong> <code>object</code> （可选）</p><p>视频处理参数，如设置输出视频的分辨率等。</p><a id="accordion-属性-8"></a><section><p>属性</p><div><p><strong>control_condition</strong> <code>string</code> （可选）</p><p>设置视频特征提取的方式，输入video_url时必选。默认为&quot;&quot;，表示不做任何提取。</p><ul><li><code>posebodyface</code>：提取输入视频的主体的脸部表情和肢体动作。</li><li><code>depth</code>：提取输入视频的构图和运动轮廓。</li></ul><p><strong>duration</strong> <code>integer</code> （可选）</p><p>视频生成时长，单位为秒。当前参数值固定为5，且不支持修改。模型将始终生成5秒时长的视频。</p><p><strong>prompt_extend</strong><code>bool</code> （可选）</p><p>是否开启prompt智能改写。开启后使用大模型对输入prompt进行智能改写。对于较短的prompt生成效果提升明显，但会增加耗时。</p><ul><li><code>true</code>（默认值）：开启智能改写。</li><li><code>false</code>：关闭智能改写。<strong>（推荐）</strong></li></ul><blockquote><p>当文本描述与输入的视频内容不一致时，模型可能产生误解。建议手动关闭智能扩写，并在 <code>prompt</code> 中提供清晰、具体的画面描述，以提升生成一致性与准确性。</p></blockquote><p><strong>seed</strong><code>integer</code>（可选）</p><p>随机数种子，用于控制模型生成内容的随机性。seed参数取值范围是<code>[0, 2147483647]</code>。</p><p>如果不提供，则算法自动生成一个随机数作为种子。如果您希望生成内容保持相对稳定，请使用相同的seed参数值。</p><p><strong>watermark</strong> <code>bool</code>（可选）</p><p>是否添加水印标识，水印位于图片右下角，文案为“AI生成”。</p><ul><li><code>false</code>（默认值）：不添加水印。</li><li><code>true</code>：添加水印。</li></ul></div></section></td></tr></tbody></table></section><a id="视频画面扩展"></a><section><a id="视频画面扩展-h4"></a><h4>视频画面扩展</h4><p><strong>model</strong> <code>string</code> <strong>（必选）</strong></p><p>模型名称。示例值：wanx2.1-vace-plus。</p><table><tbody><tr><td><p><strong>input</strong> <code>object</code> <strong>（必选）</strong></p><p>输入的基本信息，如提示词等。</p><a id="accordion-属性-9"></a><section><p>属性</p><div><p><strong>prompt</strong><code>string</code><strong>（必选）</strong></p><p>提示词，用来描述生成视频中期望包含的元素和视觉特点。</p><p>支持中英文，长度不超过800个字符，每个汉字/字母占一个字符，超过部分会自动截断。</p><p>提示词技巧请参见<a href="../../../../model-user-guide/use-cases/text-to-video-prompt.md">文生视频/图生视频Prompt指南</a>。</p><p><strong>function</strong><code>string</code><strong>（必选）</strong></p><p>功能名称。视频画面扩展设置为 <code>video_outpainting</code>。</p><p>视频画面扩展支持对视频在上、下、左、右四个方向按比例扩展。</p><p><strong>video_url</strong><code>string</code> <strong>（必选）</strong></p><p>输入视频的URL地址。</p><ol><li><p>公网URL：</p><ul><li>支持 HTTP 和 HTTPS 协议。</li><li>示例值：<a href="https://xxx/xxx.mp3"></a><a href="https://xxx/xxx.mp3">https://xxx/xxx.mp3</a>。</li></ul></li><li><p>临时URL：</p><ul><li>支持OSS协议，必须通过<a href="../../../more-about-models/get-temporary-file-url.md">上传文件获取临时 URL</a>。</li><li>示例值：oss://dashscope-instant/xxx/xxx.mp3。</li></ul></li></ol><p>视频限制：</p><ul><li>视频格式：MP4。</li><li>视频帧率：大于等于16FPS。</li><li>视频大小：不超过50MB。</li><li>视频长度：不超过5秒，否则取视频的前5秒。</li><li>URL地址中不能包含中文字符。</li></ul><p>关于输出视频的分辨率：</p><ul><li>若输入视频分辨率 ≤ 720P，输出将保留原始分辨率；</li><li>若输入视频分辨率 &gt; 720P，则在保持原视频宽高比的前提下，按比例缩放至不超过 720P。</li></ul><p>关于输出视频的时长：</p><ul><li>输出视频时长与输入视频一致，最长不超过 5 秒。</li><li>示例：若输入视频为 3 秒，则输出也为 3 秒；若输入为 6 秒，则输出为前 5 秒。</li></ul></div></section></td></tr><tr><td><p><strong>parameters</strong> <code>object</code> （可选）</p><p>视频处理参数，如设置扩展比例等。</p><a id="accordion-属性-10"></a><section><p>属性</p><div><p><strong>top_scale</strong> <code>float</code> （可选）</p><p>视频画面居中，向上按比例扩展视频。</p><p>取值范围为[1.0, 2.0]，默认值为1.0，表示不扩展。</p><p><strong>bottom_scale</strong> <code>float</code> （可选）</p><p>视频画面居中，向下按比例扩展视频。</p><p>取值范围为[1.0, 2.0]，默认值为1.0，表示不扩展。</p><p><strong>left_scale</strong> <code>float</code> （可选）</p><p>视频画面居中，向左按比例扩展视频。</p><p>取值范围为[1.0, 2.0]，默认值为1.0，表示不扩展。</p><p><strong>right_scale</strong> <code>float</code> （可选）</p><p>视频画面居中，向右按比例扩展视频。</p><p>取值范围为[1.0, 2.0]，默认值为1.0，表示不扩展。</p><p><strong>duration</strong> <code>integer</code> （可选）</p><p>视频生成时长，单位为秒。当前参数值固定为5，且不支持修改。模型将始终生成5秒时长的视频。</p><p><strong>prompt_extend</strong><code>bool</code> （可选）</p><p>是否开启prompt智能改写。开启后使用大模型对输入prompt进行智能改写。对于较短的prompt生成效果提升明显，但会增加耗时。</p><ul><li><code>true</code>（默认值）：开启智能改写。</li><li><code>false</code>：关闭智能改写。<strong>（推荐）</strong></li></ul><blockquote><p>当文本描述与输入的视频内容不一致时，模型可能产生误解。建议手动关闭智能扩写，并在 <code>prompt</code> 中提供清晰、具体的画面描述，以提升生成一致性与准确性。</p></blockquote><p><strong>seed</strong><code>integer</code>（可选）</p><p>随机数种子，用于控制模型生成内容的随机性。seed参数取值范围是<code>[0, 2147483647]</code>。</p><p>如果不提供，则算法自动生成一个随机数作为种子。如果您希望生成内容保持相对稳定，请使用相同的seed参数值。</p><p><strong>watermark</strong> <code>bool</code>（可选）</p><p>是否添加水印标识，水印位于图片右下角，文案为“AI生成”。</p><ul><li><code>false</code>（默认值）：不添加水印。</li><li><code>true</code>：添加水印。</li></ul></div></section></td></tr></tbody></table></section></section></td><td><a id="fig-code-group"></a><div><a id="fig-code-group-多图参考-tab"></a>多图参考<div><a id="code-code-group-多图参考"></a><pre class="language-bash"><code># 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
--header 'X-DashScope-Async: enable' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
    &quot;model&quot;: &quot;wanx2.1-vace-plus&quot;,
    &quot;input&quot;: {
        &quot;function&quot;: &quot;image_reference&quot;,
        &quot;prompt&quot;: &quot;视频中，一位女孩自晨雾缭绕的古老森林深处款款走出，她步伐轻盈，镜头捕捉她每一个灵动瞬间。当女孩站定，环顾四周葱郁林木时，她脸上绽放出惊喜与喜悦交织的笑容。这一幕，定格在了光影交错的瞬间，记录下女孩与大自然的美妙邂逅。&quot;,
        &quot;ref_images_url&quot;: [
            &quot;http://wanx.alicdn.com/material/20250318/image_reference_2_5_16.png&quot;,
            &quot;http://wanx.alicdn.com/material/20250318/image_reference_1_5_16.png&quot;
        ]
    },
    &quot;parameters&quot;: {
        &quot;prompt_extend&quot;: true,
        &quot;obj_or_bg&quot;: [&quot;obj&quot;,&quot;bg&quot;],
        &quot;size&quot;: &quot;1280*720&quot;
    }
}'
</code></pre></div><a id="fig-code-group-视频重绘-tab"></a>视频重绘<div><a id="code-code-group-视频重绘"></a><pre class="language-bash"><code># 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
--header 'X-DashScope-Async: enable' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
    &quot;model&quot;: &quot;wanx2.1-vace-plus&quot;,
    &quot;input&quot;: {
        &quot;function&quot;: &quot;video_repainting&quot;,
        &quot;prompt&quot;: &quot;视频展示了一辆黑色的蒸汽朋克风格汽车，绅士驾驶着，车辆装饰着齿轮和铜管。背景是蒸汽驱动的糖果工厂和复古元素，画面复古与趣味。&quot;,
        &quot;video_url&quot;: &quot;http://wanx.alicdn.com/material/20250318/video_repainting_1.mp4&quot;
    },
    &quot;parameters&quot;: {
        &quot;prompt_extend&quot;: false,
        &quot;control_condition&quot;: &quot;depth&quot;
    }
}'
</code></pre></div><a id="fig-code-group-局部编辑-tab"></a>局部编辑<div><a id="code-code-group-局部编辑"></a><pre class="language-bash"><code># 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
--header 'X-DashScope-Async: enable' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
    &quot;model&quot;: &quot;wanx2.1-vace-plus&quot;,
    &quot;input&quot;: {
        &quot;function&quot;: &quot;video_edit&quot;,
        &quot;prompt&quot;: &quot;视频展示了一家巴黎风情的法式咖啡馆，一只穿着西装的狮子优雅地品着咖啡。它一手端着咖啡杯，轻轻啜饮，神情惬意。咖啡馆装饰雅致，柔和的色调与温暖灯光映照着狮子所在的区域。&quot;,
        &quot;mask_image_url&quot;: &quot;http://wanx.alicdn.com/material/20250318/video_edit_1_mask.png&quot;,
        &quot;video_url&quot;: &quot;http://wanx.alicdn.com/material/20250318/video_edit_2.mp4&quot;,
        &quot;mask_frame_id&quot;: 1
    },
    &quot;parameters&quot;: {
        &quot;prompt_extend&quot;: false,
        &quot;mask_type&quot;: &quot;tracking&quot;,
        &quot;expand_ratio&quot;: 0.05
    }
}'
</code></pre></div><a id="fig-code-group-视频延展-tab"></a>视频延展<div><a id="code-code-group-视频延展"></a><pre class="language-bash"><code># 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
--header 'X-DashScope-Async: enable' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
    &quot;model&quot;: &quot;wanx2.1-vace-plus&quot;,
    &quot;input&quot;: {
        &quot;function&quot;: &quot;video_extension&quot;,
        &quot;prompt&quot;: &quot;一只戴着墨镜的狗在街道上滑滑板，3D卡通。&quot;,
        &quot;first_clip_url&quot;: &quot;http://wanx.alicdn.com/material/20250318/video_extension_1.mp4&quot;
    },
    &quot;parameters&quot;: {
        &quot;prompt_extend&quot;: false
    }
}'
</code></pre></div><a id="fig-code-group-视频画面扩展-tab"></a>视频画面扩展<div><a id="code-code-group-视频画面扩展"></a><pre class="language-bash"><code># 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
--header 'X-DashScope-Async: enable' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
    &quot;model&quot;: &quot;wanx2.1-vace-plus&quot;,
    &quot;input&quot;: {
        &quot;function&quot;: &quot;video_outpainting&quot;,
        &quot;prompt&quot;: &quot;一位优雅的女士正在激情演奏小提琴，她身后是一支完整的交响乐团。&quot;,
        &quot;video_url&quot;: &quot;http://wanx.alicdn.com/material/20250318/video_outpainting_1.mp4&quot;
    },
    &quot;parameters&quot;: {
        &quot;prompt_extend&quot;: false,
        &quot;top_scale&quot;: 1.5,
        &quot;bottom_scale&quot;: 1.5,
        &quot;left_scale&quot;: 1.5,
        &quot;right_scale&quot;: 1.5
    }
}'
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="cd3063363egdc"></a><h4>响应参数</h4><p><strong>output</strong> <code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-11"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../../preparations/error-code.md">错误码</a>。</p></td><td><a id="sec-tabs-3"></a><section><a id="成功响应"></a><section><a id="成功响应-h4"></a><h4>成功响应</h4><p>请保存 task_id，用于查询任务状态与结果。</p><a id="code-block"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
        &quot;task_status&quot;: &quot;PENDING&quot;,
        &quot;task_id&quot;: &quot;0385dc79-5ff8-4d82-bcb6-xxxxxx&quot;
    },
    &quot;request_id&quot;: &quot;4909100c-7b5a-9f92-bfe5-xxxxxx&quot;
}
</code></pre></section><a id="异常响应"></a><section><a id="异常响应-h4"></a><h4>异常响应</h4><p>创建任务失败，请参见<a href="../../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-2"></a><pre class="language-json"><code>{
    &quot;code&quot;: &quot;InvalidApiKey&quot;,
    &quot;message&quot;: &quot;No API-key provided.&quot;,
    &quot;request_id&quot;: &quot;7438d53d-6eb8-4596-8835-xxxxxx&quot;
}
</code></pre></section></section></td></tr></tbody></table>

<a id="步骤2-根据任务id查询结果"></a>

<a id="420e6e77a17om"></a>

### 步骤2：根据任务ID查询结果

<a id="sec-tabs-4"></a>

<a id="北京-2"></a>

<a id="北京-2-h4"></a>

#### 北京

`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="新加坡-2"></a>

<a id="新加坡-2-h4"></a>

#### 新加坡

`GET https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/tasks/{task_id}`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<table><tbody><tr><td><a id="eb9c8d77b6xg8"></a><h4>请求参数</h4><a id="36a28b657f196"></a><h5>请求头（Headers）</h5><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><a id="0e29e015d8opn"></a><h5>URL路径参数（Path parameters）</h5><p><strong>task_id</strong> <code>string</code><strong>（必选）</strong></p><p>任务ID。</p></td><td><a id="sec-tabs-5"></a><section><a id="查询任务结果"></a><section><a id="查询任务结果-h4"></a><h4>查询任务结果</h4><p>将<code>{task_id}</code>完整替换为上一步接口返回的<code>task_id</code>的值。<code>task_id</code>查询有效期为24小时，并请将<code>{WorkspaceId}</code>替换为真实的<a href="../../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain">业务空间ID</a>。</p><a id="code-block-3"></a><pre class="language-bash"><code>curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id} \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="810682d979i8q"></a><h4>响应参数</h4><p><strong>output</strong><code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-12"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值-2"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section><p><strong>submit_time</strong> <code>string</code></p><p>任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>scheduled_time</strong> <code>string</code></p><p>任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>end_time</strong> <code>string</code></p><p>任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>video_url</strong><code>string</code></p><p>视频URL。链接有效期24小时，可通过此URL下载视频。输出视频格式为mp4（H.264 编码）。</p><p><strong>orig_prompt</strong> <code>string</code></p><p>原始的输入prompt。</p><p><strong>actual_prompt</strong> <code>string</code></p><p>开启prompt智能改写后实际使用的prompt。若不开启prompt智能改写，不会返回该字段。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../../preparations/error-code.md">错误码</a>。</p></div></section><p><strong>usage</strong> <code>object</code></p><p>输出信息统计。只对成功的结果计数。</p><a id="accordion-属性-13"></a><section><p>属性</p><div><p><strong>video_duration</strong> <code>integer</code></p><p>生成视频的时长，单位为秒。</p><p><strong>video_ratio</strong> <code>string</code></p><p>生成视频的比例。固定为<code>standard</code>。</p><p><strong>video_count</strong> <code>integer</code></p><p>生成视频的数量。</p></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p></td><td><a id="sec-tabs-6"></a><section><a id="任务执行成功"></a><section><a id="任务执行成功-h4"></a><h4>任务执行成功</h4><p>任务数据（如任务状态、视频URL等）仅保留24小时，超时后会被自动清除。请您务必及时保存生成的视频。</p><a id="code-block-4"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;851985d0-fbba-9d8d-a17a-xxxxxx&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;208e2fd1-fcb4-4adf-9fcc-xxxxxx&quot;,
        &quot;task_status&quot;: &quot;SUCCEEDED&quot;,
        &quot;submit_time&quot;: &quot;2025-05-15 16:14:44.723&quot;,
        &quot;scheduled_time&quot;: &quot;2025-05-15 16:14:44.750&quot;,
        &quot;end_time&quot;: &quot;2025-05-15 16:20:09.389&quot;,
        &quot;video_url&quot;: &quot;https://dashscope-result-wlcb.oss-cn-wulanchabu.aliyuncs.com/xxx.mp4?xxxxxx&quot;,
        &quot;orig_prompt&quot;: &quot;视频中，一位女孩自晨雾缭绕的古老森林深处款款走出，她步伐轻盈，镜头捕捉她每一个灵动瞬间。当女孩站定，环顾四周葱郁林木时，她脸上绽放出惊喜与喜悦交织的笑容。这一幕，定格在了光影交错的瞬间，记录下女孩与大自然的美妙邂逅。&quot;,
        &quot;actual_prompt&quot;: &quot;一位身着浅色长裙的女孩从晨雾缭绕的古老森林深处缓缓走出，步伐轻盈如舞。她长发微卷，面容清秀，眼神明亮。镜头跟随她的动作，捕捉每一个灵动瞬间。当她站定，转身环顾四周葱郁林木时，脸上绽放出惊喜与喜悦交织的笑容。阳光透过树叶洒下斑驳光影，定格这一人与自然和谐共处的美好时刻。画面风格为清新自然系写真，中景全景结合，平视视角带有轻微移动运镜。&quot;
    },
    &quot;usage&quot;: {
        &quot;video_duration&quot;: 5,
        &quot;video_ratio&quot;: &quot;standard&quot;,
        &quot;video_count&quot;: 1
    }
}
</code></pre></section><a id="任务执行失败"></a><section><a id="任务执行失败-h4"></a><h4>任务执行失败</h4><p>若任务执行失败，task_status将置为 FAILED，并提供错误码和信息。请参见<a href="../../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-5"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;e5d70b02-ebd3-98ce-9fe8-759d7d7b107d&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;86ecf553-d340-4e21-af6e-a0c6a421c010&quot;,
        &quot;task_status&quot;: &quot;FAILED&quot;,
        &quot;code&quot;: &quot;InvalidParameter&quot;,
        &quot;message&quot;: &quot;The size is not match xxxxxx&quot;
    }
}
</code></pre></section></section></td></tr></tbody></table>

<a id="使用限制"></a>

<a id="48194b2ea8c7l"></a>

## 使用限制

-   **数据时效**：任务`task_id`和 视频`video_url`均只保留 24 小时，过期后将无法查询或下载。
-   **音频支持**：当前仅支持生成无声视频，不支持音频输出。如有需要，可通过[语音合成](../../../audio-api-directory/speech-recognition-api-reference.md)生成音频。

<a id="错误码"></a>

<a id="b61f9fd1c3caw"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](../../../preparations/error-code.md)进行解决。

<a id="常见问题"></a>

<a id="042dd764b01yt"></a>

## 常见问题

<a id="q-如何获取视频存储的访问域名白名单"></a>

<a id="c7421e6e32dj8"></a>

#### Q：如何获取视频存储的访问域名白名单？

A： 模型生成的视频存储于阿里云OSS，API将返回一个临时的公网URL。**若需要对该下载地址进行防火墙白名单配置**，请注意：由于底层存储会根据业务情况进行动态变更，为避免过期信息影响访问，文档不提供固定的OSS域名白名单。如有安全管控需求，请联系客户经理获取最新OSS域名列表。
