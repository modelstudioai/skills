# 万相3.0-视频生成API参考

万相3.0是全能参考视频生成模型（All-in-One），统一支持 文生视频 、 图生视频 （首帧/首尾帧）和 参考生视频 等多种用法。最长可生成30秒视频，输出帧率为30fps。

使用指南请参见[万相3.0-视频生成](../../../_short/wan3-video-generation-guide-0e56f533d7040652.md)。

<a id="适用范围"></a>

<a id="w30scope01t"></a>

## 适用范围

为确保调用成功，请务必保证**模型、Endpoint URL 和 API Key 均属于同一地域**。跨地域调用将会失败。

-   [**选择模型**](https://bailian.console.aliyun.com/cn-beijing/model/market)：前往模型广场选择模型，并确认其所属地域。
-   **选择 URL**：选择对应的地域 Endpoint URL。
-   **配置 API Key**：选择地域并[获取与配置 API Key](../../preparations/get-api-key.md)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

> **说明**
>
> 本文的示例代码适用于**北京地域**。

<a id="http调用"></a>

<a id="w30http01t"></a>

## HTTP调用

由于视频生成任务耗时较长（通常为1-5分钟），API采用异步调用。整个流程包含 **"创建任务 -> 轮询获取"** 两个核心步骤，具体如下：

<a id="步骤1-创建任务获取任务id"></a>

<a id="w30step1t"></a>

### 步骤1：创建任务获取任务ID

<a id="sec-tabs"></a>

<a id="北京"></a>

<a id="北京-h4"></a>

#### 北京

`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`

<a id="新加坡"></a>

<a id="新加坡-h4"></a>

#### 新加坡

`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`

<a id="日本-东京"></a>

<a id="日本-东京-h4"></a>

#### 日本（东京）

`POST https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`

<a id="德国-法兰克福"></a>

<a id="德国-法兰克福-h4"></a>

#### 德国（法兰克福）

`POST https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`

<a id="美国-弗吉尼亚"></a>

<a id="美国-弗吉尼亚-h4"></a>

#### 美国（弗吉尼亚）

`POST https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`

<a id="中国香港"></a>

<a id="中国香港-h4"></a>

#### 中国香港

`POST https://{WorkspaceId}.cn-hongkong.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

> **说明**
>
> -   创建成功后，使用接口返回的 `task_id` 查询结果，task\_id 有效期为 24 小时。**请勿重复创建任务**，轮询获取即可。
> -   新手指引请参见[Postman](https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api)。

<table><tbody><tr><td><a id="w30req01h"></a><h4>请求参数</h4><a id="w30req02h"></a><h5>请求头（Headers）</h5><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><p><strong>X-DashScope-Async</strong><code>string</code><strong>（必选）</strong></p><p>异步处理配置参数。HTTP请求只支持异步，<strong>必须设置为</strong><code>enable</code>。</p><div><div><p><strong>重要</strong>缺少此请求头将报错：“current user api does not support synchronous calls”。</p></div></div><a id="w30req06h"></a><h5>请求体（Request Body）</h5><p><strong>model</strong> <code>string</code> <strong>（必选）</strong></p><p>模型名称。可选值：</p><ul><li><code>wan3.0-video-prime</code>：能力对齐标准版。资源紧张时，个别任务可能以标准速率完成推理；系统将自动识别此类任务，并按标准速率的模型计费。</li><li><code>wan3.0-video</code>：标准版。</li></ul><p><strong>input</strong> <code>object</code> <strong>（必选）</strong></p><p>输入的基本信息。<code>prompt</code> 和 <code>media</code> 必填其一。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>prompt</strong> <code>string</code> （条件必选）</p><p>文本提示词，用来描述期望生成的视频内容。和 <code>media</code> 必填其一。</p><p>支持中英文，每个汉字/字母占一个字符，不超过20000个字符，超过部分会自动截断。</p><p>在全能参考模式下，prompt中可以用&quot;图1&quot;&quot;视频1&quot;&quot;音频1&quot;等指代 media 数组中对应顺序的媒体素材。</p><p><strong>media</strong> <code>array</code> （条件必选）</p><p>媒体素材数组，支持图像、视频、音频、文件和网页作为输入。和 <code>prompt</code> 必填其一。</p><ul><li><p>数组中每个元素为一个媒体对象，包含 <code>type</code> 与 <code>url</code> 字段。</p></li><li><p>在参考生视频模式下，按照数组顺序定义 <code>prompt</code> 中素材引用的顺序。图和视频分别计数，即可同时存在图1、视频1。</p><ul><li>数组中的第 1 个 <code>reference_video</code> 对应 <strong>视频1</strong>，第 2 个对应 <strong>视频2</strong>，以此类推。</li><li>数组中的第 1 个 <code>reference_image</code> 对应 <strong>图1</strong>，第 2 个对应 <strong>图2</strong>，以此类推。</li><li>数组中的第 1 个 <code>reference_audio</code> 对应 <strong>音频1</strong>，第 2 个对应 <strong>音频2</strong>，以此类推。</li></ul></li></ul><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>媒体素材类型。可选值为：</p><ul><li><code>first_frame</code>：首帧图像。最多1张，严格作为视频第一帧。</li><li><code>last_frame</code>：尾帧图像。最多1张，严格作为视频最后一帧。</li><li><code>reference_image</code>：参考图像。最多10张。</li><li><code>reference_video</code>：参考视频。最多5段，总时长不大于15秒。</li><li><code>reference_audio</code>：参考音频。最多5段，总时长不大于15秒。</li><li><code>file</code>：文件。最多1个，不可与 link 同时输入。</li><li><code>link</code>：网页链接。最多1个，不可与 file 同时输入。</li></ul><div><div><p><strong>重要</strong>不同 <code>type</code> 的组合规则和限制请参见<a href="#w30media_combo_t">素材组合</a>。</p></div></div><p><strong>url</strong> <code>string</code> <strong>（必选）</strong></p><p>媒体素材URL或Base64 编码数据。</p><a id="accordion-传入图像-type-first-frame-last-frame-reference-image"></a><section><p>传入图像（type=first_frame / last_frame / reference_image）</p><div><p>图像URL或Base64 编码数据。</p><p>图像限制：</p><ul><li>格式：JPEG、JPG、PNG（不支持透明通道）、BMP、WEBP。</li><li>分辨率：单边[240, 8000]像素。</li><li>长宽比：不超过8:1。</li><li>文件大小：不超过20MB。</li></ul><p>支持输入的格式：</p><ol><li><p>公网URL：</p><ul><li>支持HTTP或HTTPS协议。</li><li>示例值：<a href="https://xxx/xxx.png"></a><a href="https://xxx/xxx.png">https://xxx/xxx.png</a>。</li></ul></li><li><p>临时URL：</p><ul><li>支持OSS协议，必须通过<a href="../../more-about-models/get-temporary-file-url.md">上传文件获取临时 URL</a>。</li><li>示例值：oss://dashscope-instant/xxx/xxx.png。</li></ul></li><li><p>Base64 编码图像后的字符串：</p><ul><li>数据格式：<code>data:{MIME_type};base64,{base64_data}</code>。</li><li>示例值：data:image/png;base64,GDU7MtCZzEbTbmRZ......。（编码字符串过长，仅展示片段）</li><li>详情请参见<a href="../../../model-user-guide/use-cases/legacy-resources/legacy-video-generation/image-to-video-guide.md#32d9db99f1fk0">传入图像</a>。</li></ul></li></ol></div></section><a id="accordion-传入视频-type-reference-video"></a><section><p>传入视频（type=reference_video）</p><div><p>参考视频URL。</p><p>视频限制：</p><ul><li>格式：mp4、mov。</li><li>时长：单个[1, 15]秒，总时长不大于15秒。</li><li>帧率：≥16 fps。</li><li>分辨率：单边[240, 4096]像素。</li><li>长宽比：不超过8:1。</li><li>单文件大小：不超过100MB。</li></ul><p>支持输入的格式：</p><ol><li><p>公网URL：</p><ul><li>支持HTTP或HTTPS协议。</li><li>示例值：<a href="https://xxx/xxx.mp4"></a><a href="https://xxx/xxx.mp4">https://xxx/xxx.mp4</a>。</li></ul></li><li><p>临时URL：</p><ul><li>支持OSS协议，必须通过<a href="../../more-about-models/get-temporary-file-url.md">上传文件获取临时 URL</a>。</li><li>示例值：oss://dashscope-instant/xxx/xxx.mp4。</li></ul></li></ol></div></section><a id="accordion-传入音频-type-reference-audio"></a><section><p>传入音频（type=reference_audio）</p><div><p>参考音频URL。</p><p>音频限制：</p><ul><li>格式：wav、mp3。</li><li>时长：单个[1, 15]秒，总时长不大于15秒。</li><li>文件大小：不超过15MB。</li></ul><p>支持输入的格式：</p><ol><li><p>公网URL：</p><ul><li>支持HTTP或HTTPS协议。</li><li>示例值：<a href="https://xxx/xxx.mp3"></a><a href="https://xxx/xxx.mp3">https://xxx/xxx.mp3</a>。</li></ul></li><li><p>临时URL：</p><ul><li>支持OSS协议，必须通过<a href="../../more-about-models/get-temporary-file-url.md">上传文件获取临时 URL</a>。</li><li>示例值：oss://dashscope-instant/xxx/xxx.mp3。</li></ul></li></ol></div></section><a id="accordion-传入文件-type-file"></a><section><p>传入文件（type=file）</p><div><p>文件URL。</p><p>文件限制：</p><ul><li>格式：docx、doc、xlsx、xls、pptx、ppt、pdf、txt、key、pages、numbers、md。</li><li>文件大小：不超过100MB。</li><li>页数限制：不超过50页（对pdf、docx、doc、pptx、ppt、key、pages格式校验）。</li></ul><p>支持输入的格式：</p><ol><li><p>公网URL：</p><ul><li>支持HTTP或HTTPS协议。</li><li>示例值：<a href="https://xxx/xxx.pdf"></a><a href="https://xxx/xxx.pdf">https://xxx/xxx.pdf</a>。</li></ul></li><li><p>临时URL：</p><ul><li>支持OSS协议，必须通过<a href="../../more-about-models/get-temporary-file-url.md">上传文件获取临时 URL</a>。</li><li>示例值：oss://dashscope-instant/xxx/xxx.pdf。</li></ul></li></ol></div></section><a id="accordion-传入网页链接-type-link"></a><section><p>传入网页链接（type=link）</p><div><p>公开网页的URL地址。仅支持解析无需登录的公开网页（如新闻、博客、公众号等）。</p><p>支持输入的格式：</p><ol><li><p>公网URL：</p><ul><li>支持HTTP或HTTPS协议。</li><li>示例值：<a href="https://xxx/article/xxx"></a><a href="https://xxx/article/xxx">https://xxx/article/xxx</a>。</li></ul></li></ol></div></section></div></section></div></section><p><strong>parameters</strong> <code>object</code> （可选）</p><p>视频处理参数。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>resolution</strong> <code>string</code> （可选）</p><p>生成视频的分辨率档位。默认值为 <code>1080P</code>。可选值：</p><ul><li><code>1080P</code></li><li><code>720P</code></li><li><code>480P</code></li></ul><p><strong>ratio</strong> <code>string</code> （可选）</p><p>生成视频的宽高比。可选值：</p><ul><li><code>adaptive</code>（默认值）：自适应长宽比，根据输入媒体比例和意图自动推荐合适的长宽比。</li><li><code>21:9</code></li><li><code>16:9</code></li><li><code>4:3</code></li><li><code>1:1</code></li><li><code>3:4</code></li><li><code>9:16</code></li></ul><p><strong>duration</strong> <code>integer</code> （可选）</p><p>生成视频的时长，单位为秒。默认值为5。</p><ul><li>无视频输入时：取值范围为[2, 30]的整数。</li><li>有视频输入时：输入视频总时长 + 输出视频时长不超过30秒。</li><li>传 <code>-1</code> 时：智能时长模式，模型根据输入的 prompt、内容和富媒体自动推荐合适时长生成。</li></ul><p><strong>audio</strong> <code>boolean</code> （可选）</p><p>输出视频是否包含音频。</p><ul><li><code>true</code>：默认值，输出视频包含声音。</li><li><code>false</code>：输出视频不包含音轨。</li></ul><p>开关声音价格相同。</p><p><strong>seed</strong> <code>integer</code> （可选）</p><p>随机种子，用于复现生成结果。取值范围：-1或[0, 2147483647]。传入-1或未指定时，系统自动生成随机种子。即使使用相同seed，也不能保证每次生成结果完全一致。</p><p><strong>prompt_extend</strong> <code>boolean</code> （可选）</p><p>是否开启prompt智能改写。开启后使用大模型对输入prompt进行智能改写。对于较短的prompt生成效果提升明显，但会增加耗时。</p><ul><li><code>true</code>：默认值，开启智能改写。</li><li><code>false</code>：不开启智能改写。</li></ul><div><div><p><strong>重要</strong>当传入文档（<code>file</code>）或网页（<code>link</code>）素材时，<code>prompt_extend</code> 取值必须为 <code>true</code>。</p></div></div><p><strong>watermark</strong> <code>boolean</code> （可选）</p><p>是否添加水印标识。</p><ul><li><code>false</code>：默认值，不添加水印。</li><li><code>true</code>：添加水印。</li></ul></div></section></td><td><a id="sec-tabs-2"></a><section><a id="参考文件生视频"></a><section><a id="参考文件生视频-h4"></a><h4>参考文件生视频</h4><p>通过 <code>file</code> 类型传入文件，模型自动理解文件内容生成视频。</p><a id="code-block"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;wan3.0-video&quot;,
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;一支高端智能眼镜产品广告，整体风格极简、未来感、时尚高级，光影克制，画面以黑色、银灰色、冰蓝色为主色调，局部点缀柔和白光与参数UI图形。开场在纯黑背景中，一副智能眼镜从黑暗中缓缓浮现，镜腿边缘掠过精致高光，镜框轮廓在冷冽边缘光下被勾勒出来，镜头超近距离掠过镜片、鼻托、转轴、镜腿与材质细节，展现金属与高性能复合材料的细腻质感，表面处理高级克制，线条轻薄流畅。随后产品在空中缓慢旋转，画面以极简动态图形同步展示核心参数信息。随后镜头快速收拢，所有零件精准回归组装成完整产品，切换到年轻模特佩戴展示，模特五官立体、气质自信，穿着简洁高级的都市时尚服装，在极简空间和城市光影环境中自然转头、抬手、行走、微笑，镜头从正面、侧面、斜后方展示眼镜佩戴状态，突出轻薄贴合、时尚轮廓与日常百搭属性。结尾在纯色背景中，产品悬浮定格，镜头缓慢推进到品牌logo和核心slogan，整体音乐极简电子氛围配合精准鼓点，节奏干净有力，画面质感高级、克制、纯粹，具有强烈品牌记忆点和国际化科技审美。&quot;,
        &quot;media&quot;: [
            {
                &quot;type&quot;: &quot;file&quot;,
                &quot;url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260806/ebapmr/glass.pptx&quot;
            }
        ]
    },
    &quot;parameters&quot;: {
        &quot;resolution&quot;: &quot;480P&quot;,
        &quot;ratio&quot;: &quot;adaptive&quot;,
        &quot;duration&quot;: 10,
        &quot;prompt_extend&quot;: true
    }
}'
</code></pre></section><a id="参考生视频"></a><section><a id="参考生视频-h4"></a><h4>参考生视频</h4><p>通过 <code>input.media</code> 传入参考图片、视频、音频、文件或网页链接，模型自动理解意图生成视频。</p><a id="code-block-2"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;wan3.0-video&quot;,
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;视频1抱着图3，在图4的椅子上弹奏一支舒缓的乡村民谣，并说道：&quot;今天的阳光真好。&quot;图1手中拿着图2，路过视频1，把手中的图2放到视频1旁边的桌子上，并说道：&quot;真好听，能不能再唱一遍&quot;。&quot;,
        &quot;media&quot;: [
            {
                &quot;type&quot;: &quot;reference_image&quot;,
                &quot;url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260408/sjuytr/wan-r2v-object-girl.jpg&quot;
            },
            {
                &quot;type&quot;: &quot;reference_video&quot;,
                &quot;url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qigswt/wan-r2v-role2.mp4&quot;
            },
            {
                &quot;type&quot;: &quot;reference_image&quot;,
                &quot;url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/rtjeqf/wan-r2v-object3.png&quot;
            },
            {
                &quot;type&quot;: &quot;reference_image&quot;,
                &quot;url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qpzxps/wan-r2v-object4.png&quot;
            },
            {
                &quot;type&quot;: &quot;reference_image&quot;,
                &quot;url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/wfjikw/wan-r2v-backgroud5.png&quot;
            }
        ]
    },
    &quot;parameters&quot;: {
        &quot;resolution&quot;: &quot;480P&quot;,
        &quot;ratio&quot;: &quot;adaptive&quot;,
        &quot;duration&quot;: 5,
        &quot;prompt_extend&quot;: true
    }
}'
</code></pre></section><a id="文生视频"></a><section><a id="文生视频-h4"></a><h4>文生视频</h4><p>仅通过 <code>prompt</code> 生成视频，不传入任何媒体文件。</p><a id="code-block-3"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;wan3.0-video&quot;,
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;一只小猫在月光下的屋顶上奔跑，城市的霓虹灯在远处闪烁，电影级画质，流畅运镜。&quot;
    },
    &quot;parameters&quot;: {
        &quot;resolution&quot;: &quot;480P&quot;,
        &quot;ratio&quot;: &quot;adaptive&quot;,
        &quot;duration&quot;: 5,
        &quot;prompt_extend&quot;: true
    }
}'
</code></pre></section><a id="首帧生视频"></a><section><a id="首帧生视频-h4"></a><h4>首帧生视频</h4><p>仅传入 <code>first_frame</code>，严格指定视频首帧图像。</p><a id="code-block-4"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;wan3.0-video&quot;,
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;一只猫在草地上奔跑&quot;,
        &quot;media&quot;: [
            {
                &quot;type&quot;: &quot;first_frame&quot;,
                &quot;url&quot;: &quot;https://cdn.translate.alibaba.com/r/wanx-demo-1.png&quot;
            }
        ]
    },
    &quot;parameters&quot;: {
        &quot;resolution&quot;: &quot;480P&quot;,
        &quot;ratio&quot;: &quot;adaptive&quot;,
        &quot;duration&quot;: 5,
        &quot;prompt_extend&quot;: true
    }
}'
</code></pre></section><a id="首尾帧生视频"></a><section><a id="首尾帧生视频-h4"></a><h4>首尾帧生视频</h4><p>仅支持传入 <code>first_frame</code> 和 <code>last_frame</code>，严格指定视频的首帧和尾帧图像。</p><a id="code-block-5"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;wan3.0-video&quot;,
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;清晨太阳刚刚升起，在南瓜地里面，有一颗小南瓜上面挂着露珠，突然小南瓜咔擦一声，出现了裂缝，从裂缝中透出金光，小南瓜伴随着金光裂开，出现一团白雾，一只小兔子在南瓜裂开的南瓜中央出现。&quot;,
        &quot;media&quot;: [
            {
                &quot;type&quot;: &quot;first_frame&quot;,
                &quot;url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260414/welyei/wan2.7-i2v-first-frame.webp&quot;
            },
            {
                &quot;type&quot;: &quot;last_frame&quot;,
                &quot;url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260414/zongha/wan2.7-i2v-last-frame.webp&quot;
            }
        ]
    },
    &quot;parameters&quot;: {
        &quot;resolution&quot;: &quot;480P&quot;,
        &quot;ratio&quot;: &quot;adaptive&quot;,
        &quot;duration&quot;: 5,
        &quot;prompt_extend&quot;: true
    }
}'
</code></pre></section><a id="视频编辑"></a><section><a id="视频编辑-h4"></a><h4>视频编辑</h4><p>通过 <code>reference_video</code> 类型传入待编辑视频，结合 <code>prompt</code> 指令编辑视频内容。</p><a id="code-block-6"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;wan3.0-video&quot;,
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;将整个画面转换为黏土风格&quot;,
        &quot;media&quot;: [
            {
                &quot;type&quot;: &quot;reference_video&quot;,
                &quot;url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260402/ldnfdf/wan2.7-videoedit-style-change.mp4&quot;
            }
        ]
    },
    &quot;parameters&quot;: {
        &quot;resolution&quot;: &quot;720P&quot;,
        &quot;prompt_extend&quot;: true
    }
}'
</code></pre></section><a id="视频延长"></a><section><a id="视频延长-h4"></a><h4>视频延长</h4><p>通过 <code>reference_video</code> 类型传入原始视频，结合含延长意图关键词的 <code>prompt</code> 延长视频内容。需将 <code>ratio</code> 设为 <code>adaptive</code>。</p><a id="code-block-7"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;wan3.0-video&quot;,
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;将视频1向后延长，面包师端上刷好的面包，将刷子放到一旁，镜头跟随面包师，去斜后方的烤炉进行烤制&quot;,
        &quot;media&quot;: [
            {
                &quot;type&quot;: &quot;reference_video&quot;,
                &quot;url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260402/ldnfdf/wan2.7-videoedit-style-change.mp4&quot;
            }
        ]
    },
    &quot;parameters&quot;: {
        &quot;resolution&quot;: &quot;720P&quot;,
        &quot;ratio&quot;: &quot;adaptive&quot;,
        &quot;prompt_extend&quot;: true
    }
}'
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="w30resp01h"></a><h4>响应参数</h4><p><strong>output</strong> <code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></td><td><a id="sec-tabs-3"></a><section><a id="成功响应"></a><section><a id="成功响应-h4"></a><h4>成功响应</h4><p>请保存 task_id，用于查询任务状态与结果。</p><a id="code-block-8"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
        &quot;task_status&quot;: &quot;PENDING&quot;,
        &quot;task_id&quot;: &quot;0385dc79-5ff8-4d82-bcb6-xxxxxx&quot;
    },
    &quot;request_id&quot;: &quot;4909100c-7b5a-9f92-bfe5-xxxxxx&quot;
}
</code></pre></section><a id="异常响应"></a><section><a id="异常响应-h4"></a><h4>异常响应</h4><p>创建任务失败，请参见<a href="../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-9"></a><pre class="language-json"><code>{
    &quot;code&quot;: &quot;InvalidApiKey&quot;,
    &quot;message&quot;: &quot;No API-key provided.&quot;,
    &quot;request_id&quot;: &quot;7438d53d-6eb8-4596-8835-xxxxxx&quot;
}
</code></pre></section></section></td></tr></tbody></table>

<a id="步骤2-根据任务id查询结果"></a>

<a id="w30step2t"></a>

### 步骤2：根据任务ID查询结果

<a id="sec-tabs-4"></a>

<a id="北京-2"></a>

<a id="北京-2-h4"></a>

#### 北京

`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`

<a id="新加坡-2"></a>

<a id="新加坡-2-h4"></a>

#### 新加坡

`GET https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/tasks/{task_id}`

<a id="日本-东京-2"></a>

<a id="日本-东京-2-h4"></a>

#### 日本（东京）

`GET https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/api/v1/tasks/{task_id}`

<a id="德国-法兰克福-2"></a>

<a id="德国-法兰克福-2-h4"></a>

#### 德国（法兰克福）

`GET https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/api/v1/tasks/{task_id}`

<a id="美国-弗吉尼亚-2"></a>

<a id="美国-弗吉尼亚-2-h4"></a>

#### 美国（弗吉尼亚）

`GET https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v1/tasks/{task_id}`

<a id="中国香港-2"></a>

<a id="中国香港-2-h4"></a>

#### 中国香港

`GET https://{WorkspaceId}.cn-hongkong.maas.aliyuncs.com/api/v1/tasks/{task_id}`

> **说明**
>
> -   **轮询建议**：视频生成过程约需数分钟，建议采用**轮询**机制，并设置合理的查询间隔（如 15 秒）来获取结果。
> -   **任务状态流转**：PENDING（排队中）→ RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。
> -   **结果链接**：任务成功后返回视频链接，有效期为 **24 小时**。建议在获取链接后立即下载并转存至永久存储（如[阿里云 OSS](https://help.aliyun.com/zh/oss/user-guide/what-is-oss)）。
> -   **task\_id 有效期**：**24小时**，超时后将无法查询结果，接口将返回任务状态为`UNKNOWN`。
> -   **RPS 限制**：查询接口默认RPS为20。如需更高频查询或事件通知，建议[配置异步任务回调](../../more-about-models/async-task-api.md)。
> -   **更多操作**：如需批量查询、取消任务等操作，请参见[管理异步任务](../../more-about-models/manage-asynchronous-tasks.md)。

<table><tbody><tr><td><a id="w30s2req01h"></a><h4>请求参数</h4><a id="w30s2req02h"></a><h5>请求头（Headers）</h5><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><a id="w30s2req04h"></a><h5>URL路径参数（Path parameters）</h5><p><strong>task_id</strong> <code>string</code><strong>（必选）</strong></p><p>任务ID。</p></td><td><a id="sec-tabs-5"></a><section><a id="查询任务结果"></a><section><a id="查询任务结果-h4"></a><h4>查询任务结果</h4><p>将<code>{task_id}</code>完整替换为上一步接口返回的<code>task_id</code>的值。<code>task_id</code>查询有效期为24小时，并请将<code>{WorkspaceId}</code>替换为真实的<a href="../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain">业务空间ID</a>。</p><a id="code-block-10"></a><pre class="language-bash"><code>curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id} \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="w30s2resp01h"></a><h4>响应参数</h4><p><strong>output</strong> <code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code><strong>（必选）</strong></p><p>任务ID。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值-2"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section><p><strong>submit_time</strong> <code>string</code></p><p>任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>scheduled_time</strong> <code>string</code></p><p>任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>end_time</strong> <code>string</code></p><p>任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>orig_prompt</strong> <code>string</code></p><p>原始输入的提示词。</p><p><strong>video_url</strong> <code>string</code></p><p>生成视频的URL地址。任务成功时返回。视频格式为 MP4（H.264 编码）。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></div></section><p><strong>usage</strong> <code>object</code></p><p>输出信息统计。只对成功的结果计数。</p><a id="accordion-属性-6"></a><section><p>属性</p><div><p><strong>served_model</strong> <code>string</code></p><p>实际提供服务的模型，用于计量计费，计费按该字段返回的模型计算。请求的模型为 Prime 模型时返回此字段且必有值：未降级时为 wan3.0-video-prime，降级时为 wan3.0-video。</p><p><strong>video_count</strong> <code>integer</code></p><p>生成视频的数量。固定为1。</p><p><strong>duration</strong> <code>float</code></p><p>总视频时长，单位为秒。无输入参考视频时，等于输出视频的时长；有输入参考视频时，等于输入视频时长与输出视频时长之和。</p><p><strong>SR</strong> <code>integer</code></p><p>生成视频的分辨率。示例值：720。</p><p><strong>output_video_duration</strong> <code>float</code></p><p>输出视频的时长，单位为秒。</p><p><strong>input_video_duration</strong> <code>float</code></p><p>输入视频的时长，单位为秒。无视频输入时为0.0。</p><p><strong>fps</strong> <code>integer</code></p><p>生成视频的帧率。默认值为30。</p><p><strong>ratio</strong> <code>string</code></p><p>生成视频的宽高比。示例值：16:9。</p></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p></td><td><a id="sec-tabs-6"></a><section><a id="任务执行成功"></a><section><a id="任务执行成功-h4"></a><h4>任务执行成功</h4><p>视频URL仅保留24小时，超时后会被自动清除，请及时保存生成的视频。</p><a id="code-block-11"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;78c9b768-0285-996c-b682-xxxxxx&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;17ed7e50-00cf-4509-aea1-xxxxxx&quot;,
        &quot;task_status&quot;: &quot;SUCCEEDED&quot;,
        &quot;submit_time&quot;: &quot;2026-08-06 10:01:35.452&quot;,
        &quot;scheduled_time&quot;: &quot;2026-08-06 10:01:35.507&quot;,
        &quot;end_time&quot;: &quot;2026-08-06 10:13:33.838&quot;,
        &quot;orig_prompt&quot;: &quot;A golden retriever running on a sunny beach, waves crashing in the background, cinematic lighting&quot;,
        &quot;video_url&quot;: &quot;https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx/video.mp4&quot;
    },
    &quot;usage&quot;: {
        &quot;served_model&quot;: &quot;wan3.0-video&quot;,
        &quot;video_count&quot;: 1,
        &quot;duration&quot;: 5.0,
        &quot;SR&quot;: 480,
        &quot;output_video_duration&quot;: 5.0,
        &quot;input_video_duration&quot;: 0.0,
        &quot;fps&quot;: 30,
        &quot;ratio&quot;: &quot;16:9&quot;
    }
}
</code></pre></section><a id="任务执行失败"></a><section><a id="任务执行失败-h4"></a><h4>任务执行失败</h4><p>若任务执行失败，task_status将置为 FAILED，并提供错误码和信息。请参见<a href="../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-12"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;e5e57877-c0fc-47ed-8fad-xxxxxx&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;eff1443c-ccab-4676-aad3-xxxxxx&quot;,
        &quot;task_status&quot;: &quot;FAILED&quot;,
        &quot;code&quot;: &quot;InvalidParameter&quot;,
        &quot;message&quot;: &quot;The two modes are mutually exclusive. Do not pass reference_xx and first_frame/last_frame at the same time.&quot;
    }
}
</code></pre></section><a id="任务查询过期"></a><section><a id="任务查询过期-h4"></a><h4>任务查询过期</h4><p>task_id查询有效期为 24 小时，超时后将无法查询，返回以下报错信息。</p><a id="code-block-13"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;a4de7c32-7057-9f82-8581-xxxxxx&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;502a00b1-19d9-4839-a82f-xxxxxx&quot;,
        &quot;task_status&quot;: &quot;UNKNOWN&quot;
    }
}
</code></pre></section></section></td></tr></tbody></table>

<a id="素材组合"></a>

<a id="w30media_combo_t"></a>

## 素材组合

> **说明**
>
> 仅支持以下特定的素材组合，传入其他组合将报错。

**文生视频**：仅传入 `prompt`，不支持传入 `media`。

<a id="code-block-14"></a>

```json
// 文生视频
{
  "input": {
    "prompt": "..."
  }
}
```

**图生视频、参考生视频、视频编辑、视频延长等模式**需通过 `media` 数组传入素材，每个元素需指定 `type` 和 `url`。`type` 组合规则：

-   `first_frame`/`last_frame` 与 `reference_image`/`reference_video`/`reference_audio`/`file`/`link` 类型互斥，不能在同一请求中混用。
-   `file` 和 `link` 二选一，但均可与 `reference_image`/`reference_video`/`reference_audio` 组合使用。
-   `reference_image`/`reference_video`/`reference_audio` 之间可自由组合。

<a id="fig-code-group"></a>

<a id="fig-code-group-首帧生视频-tab"></a>

首帧生视频

<a id="code-code-group-首帧生视频"></a>

```json
// 仅首帧
{
  "media": [
    { "type": "first_frame", "url": "..." }
  ]
}
```

<a id="fig-code-group-首尾帧生视频-tab"></a>

首尾帧生视频

<a id="code-code-group-首尾帧生视频"></a>

```json
// 仅首帧+尾帧
{
  "media": [
    { "type": "first_frame", "url": "..." },
    { "type": "last_frame", "url": "..." }
  ]
}
```

<a id="fig-code-group-参考生视频-tab"></a>

参考生视频

<a id="code-code-group-参考生视频"></a>

```json
// reference_image、reference_video、reference_audio 可自由组合

// 仅参考图片
{
  "media": [
    { "type": "reference_image", "url": "..." }
  ]
}

// 仅参考视频
{
  "media": [
    { "type": "reference_video", "url": "..." }
  ]
}

// 仅参考音频
{
  "media": [
    { "type": "reference_audio", "url": "..." }
  ]
}

// 图片+视频
{
  "media": [
    { "type": "reference_image", "url": "..." },
    { "type": "reference_video", "url": "..." }
  ]
}

// 图片+音频
{
  "media": [
    { "type": "reference_image", "url": "..." },
    { "type": "reference_audio", "url": "..." }
  ]
}

// 视频+音频
{
  "media": [
    { "type": "reference_video", "url": "..." },
    { "type": "reference_audio", "url": "..." }
  ]
}

// 图片+视频+音频
{
  "media": [
    { "type": "reference_image", "url": "..." },
    { "type": "reference_video", "url": "..." },
    { "type": "reference_audio", "url": "..." }
  ]
}
```

<a id="fig-code-group-文件-网页生视频-tab"></a>

文件/网页生视频

<a id="code-code-group-文件-网页生视频"></a>

```json
// 必须包含 file 或 link（二选一），可与 reference_image/reference_video/reference_audio 自由组合

// 仅文件
{
  "media": [
    { "type": "file", "url": "..." }
  ]
}

// 文件+图片
{
  "media": [
    { "type": "file", "url": "..." },
    { "type": "reference_image", "url": "..." }
  ]
}

// 文件+视频
{
  "media": [
    { "type": "file", "url": "..." },
    { "type": "reference_video", "url": "..." }
  ]
}

// 文件+音频
{
  "media": [
    { "type": "file", "url": "..." },
    { "type": "reference_audio", "url": "..." }
  ]
}

// 文件+图片+视频
{
  "media": [
    { "type": "file", "url": "..." },
    { "type": "reference_image", "url": "..." },
    { "type": "reference_video", "url": "..." }
  ]
}

// 文件+图片+音频
{
  "media": [
    { "type": "file", "url": "..." },
    { "type": "reference_image", "url": "..." },
    { "type": "reference_audio", "url": "..." }
  ]
}

// 文件+视频+音频
{
  "media": [
    { "type": "file", "url": "..." },
    { "type": "reference_video", "url": "..." },
    { "type": "reference_audio", "url": "..." }
  ]
}

// 文件+图片+视频+音频
{
  "media": [
    { "type": "file", "url": "..." },
    { "type": "reference_image", "url": "..." },
    { "type": "reference_video", "url": "..." },
    { "type": "reference_audio", "url": "..." }
  ]
}
```

<a id="fig-code-group-视频编辑-tab"></a>

视频编辑

<a id="code-code-group-视频编辑"></a>

```json
// 必须包含 reference_video，可与 reference_image/reference_audio 组合
// 提示词含编辑意图

// 仅参考视频
{
  "media": [
    { "type": "reference_video", "url": "..." }
  ]
}

// 视频+图片
{
  "media": [
    { "type": "reference_video", "url": "..." },
    { "type": "reference_image", "url": "..." }
  ]
}

// 视频+音频
{
  "media": [
    { "type": "reference_video", "url": "..." },
    { "type": "reference_audio", "url": "..." }
  ]
}

// 视频+图片+音频
{
  "media": [
    { "type": "reference_video", "url": "..." },
    { "type": "reference_image", "url": "..." },
    { "type": "reference_audio", "url": "..." }
  ]
}
```

<a id="fig-code-group-视频延长-tab"></a>

视频延长

<a id="code-code-group-视频延长"></a>

```json
// 必须包含 reference_video，可与 reference_image/reference_audio 组合
// 提示词含延长意图

// 仅参考视频
{
  "media": [
    { "type": "reference_video", "url": "..." }
  ]
}

// 视频+图片
{
  "media": [
    { "type": "reference_video", "url": "..." },
    { "type": "reference_image", "url": "..." }
  ]
}

// 视频+音频
{
  "media": [
    { "type": "reference_video", "url": "..." },
    { "type": "reference_audio", "url": "..." }
  ]
}

// 视频+图片+音频
{
  "media": [
    { "type": "reference_video", "url": "..." },
    { "type": "reference_image", "url": "..." },
    { "type": "reference_audio", "url": "..." }
  ]
}
```

<a id="常见问题"></a>

<a id="w30faq01t"></a>

## 常见问题

<a id="首尾帧模式下为什么不能同时传入音频等其他媒体素材"></a>

<a id="w30faq02t"></a>

### 首尾帧模式下为什么不能同时传入音频等其他媒体素材？

万相3.0 的首帧/首尾帧模式仅支持传入 `first_frame` 和 `last_frame`，不可同时传入音频等其他类型（详见[素材组合](#w30media_combo_t)）。

与[万相2.7图生视频系列](../../../_short/wan-image-to-video-guide-5ad4d6cc1d9411ab.md)的区别：wan2.7 首帧/首尾帧模式支持同时传入 `driving_audio` 驱动音频；万相3.0 首帧/首尾帧模式不支持，如需音频驱动，请使用全模态参考模式（`reference_image` + `reference_audio` 组合）替代首尾帧模式。具体用法请参见[万相3.0-视频生成使用指南](../../../_short/wan3-video-generation-guide-0e56f533d7040652.md)。
