# 万相-图生视频-基于首帧API参考（2.1-2.6）

万相-图生视频模型根据 首帧图像 和 文本提示词 ，生成一段流畅的视频。

**相关文档**：[使用指南](../model-user-guide/use-cases/legacy-resources/legacy-video-generation/image-to-video-guide.md)

> **说明**
>
> 全新推出的[万相2.7-图生视频](../model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)支持首帧生视频、首尾帧生视频、视频续写三大任务，**推荐优先选用**。
>
> 本文档的[图生视频-基于首帧](legacy-image-to-video-api-reference-8b02dd673da405f1.md)（wan2.6及早期模型）仅支持首帧生视频。

<a id="适用范围"></a>

<a id="1fd78afa5brlj"></a>

<a id="09a068c6b1q5b"></a>

## 适用范围

为确保调用成功，请务必保证模型、endpoint URL 和 API Key 均属于**同一地域**。跨地域调用将会失败。

-   [**选择模型**](../model-user-guide/use-cases/legacy-resources/legacy-video-generation/image-to-video-guide.md#06f39eafa2dwt)：确认模型所属的地域。
-   **选择 URL**：选择对应的地域 Endpoint URL，支持HTTP URL或 DashScope SDK URL。
-   **配置 API Key**：获取该地域的[API Key](../model-api-reference/preparations/get-api-key.md)，再[配置API Key到环境变量](../model-api-reference/preparations/get-api-key.md)。
-   **安装 SDK**：如需通过SDK进行调用，请[安装DashScope SDK](../model-api-reference/preparations/install-sdk.md)。

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

<a id="7c782df20fkq8"></a>

## HTTP调用

图生视频任务耗时较长（通常为1-5分钟），API采用异步调用的方式。整个流程包含 **“创建任务 -> 轮询获取”** 两个核心步骤，具体如下：

<a id="步骤1-创建任务获取任务id"></a>

<a id="81185ac18blmj"></a>

<a id="fa69e36cd79fr"></a>

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

<a id="弗吉尼亚"></a>

<a id="弗吉尼亚-h4"></a>

#### 弗吉尼亚

`POST https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`

<a id="法兰克福"></a>

<a id="法兰克福-h4"></a>

#### 法兰克福

`POST https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

> **说明**
>
> -   创建成功后，使用接口返回的 `task_id` 查询结果，task\_id 有效期为 24 小时。**请勿重复创建任务**，轮询获取即可。
> -   新手指引请参见[Postman](https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api)。

<table><tbody><tr><td><a id="afcd41d2b57zf"></a><h4>请求参数</h4><a id="79473e45c592d"></a><h5>请求头（Headers）</h5><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><p><strong>X-DashScope-Async</strong><code>string</code><strong>（必选）</strong></p><p>异步处理配置参数。HTTP请求只支持异步，<strong>必须设置为</strong><code>enable</code>。</p><div><div><p><strong>重要</strong>缺少此请求头将报错：“current user api does not support synchronous calls”。</p></div></div><a id="66a778d4fbfub"></a><h5>请求体（Request Body）</h5><p><strong>model</strong> <code>string</code> <strong>（必选）</strong></p><p>模型名称。模型列表与价格详见<a href="../model-user-guide/test-1/model-pricing.md#517789fb633zr">模型价格</a>。</p><p>示例值：wan2.6-i2v-flash。</p><p><strong>input</strong> <code>object</code> <strong>（必选）</strong></p><p>输入的基本信息，如提示词等。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>prompt</strong> <code>string</code> （可选）</p><p>文本提示词。用来描述生成图像中期望包含的元素和视觉特点。</p><p>支持中英文，每个汉字/字母占一个字符，超过部分会自动截断。长度限制因模型版本而异：</p><ul><li>wan2.6和wan2.5系列模型：长度不超过1500个字符。</li><li>wan2.2 和wanx2.1系列模型：长度不超过800个字符。</li></ul><p>当使用视频特效参数（即<code>template</code>不为空）时，prompt参数无效，无需填写。</p><p>示例值：一只小猫在草地上奔跑。</p><p>提示词使用技巧详见<a href="../model-user-guide/use-cases/text-to-video-prompt.md">文生视频/图生视频Prompt指南</a>。</p><p><strong>negative_prompt</strong> <code>string</code> （可选）</p><p>反向提示词，用来描述不希望在视频画面中看到的内容，可以对视频画面进行限制。</p><p>支持中英文，长度不超过500个字符，超过部分会自动截断。</p><p>示例值：低分辨率、错误、最差质量、低质量、残缺、多余的手指、比例不良等。</p><p><strong>img_url</strong> <code>string</code> <strong>（必选）</strong></p><p>首帧图像的URL或 Base64 编码数据。</p><p>图像限制：</p><ul><li><p>图像格式：JPEG、JPG、PNG（不支持透明通道）、BMP、WEBP。</p></li><li><p>图像分辨率：图像的宽度和高度范围为[240,8000]，单位为像素。</p></li><li><p>文件大小：</p><ul><li>wan2.6和wan2.5系列模型：不超过20MB。</li><li>wan2.2 和wanx2.1系列模型：不超过10MB。</li></ul></li></ul><p>支持输入的格式：</p><ol><li><p>公网URL：</p><ul><li>支持 HTTP 或 HTTPS 协议。</li><li>示例值：<a href="https://cdn.translate.alibaba.com/r/wanx-demo-1.png"></a><a href="https://cdn.translate.alibaba.com/r/wanx-demo-1.png">https://cdn.translate.alibaba.com/r/wanx-demo-1.png</a>。</li></ul></li><li><p>临时URL：</p><ul><li>支持OSS协议，必须通过<a href="../model-api-reference/more-about-models/get-temporary-file-url.md">上传文件获取临时 URL</a>。</li><li>示例值：oss://dashscope-instant/xxx/xxx.png。</li></ul></li><li><p>Base64 编码图像后的字符串：</p><ul><li>数据格式：<code>data:{MIME_type};base64,{base64_data}</code>。</li><li>示例值：data:image/png;base64,GDU7MtCZzEbTbmRZ......。（编码字符串过长，仅展示片段）</li><li>详情请参见<a href="../model-user-guide/use-cases/legacy-resources/legacy-video-generation/image-to-video-guide.md#32d9db99f1fk0">传入图像</a>。</li></ul></li></ol><p><strong>audio_url</strong> <code>string</code> （可选）</p><strong>支持模型：wan2.6和wan2.5系列模型。</strong><p>音频文件的 URL，模型将使用该音频生成视频。</p><p>支持输入的格式：</p><ol><li><p>公网URL：</p><ul><li>支持 HTTP 和 HTTPS 协议。</li><li>示例值：<a href="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/xxx.mp3"></a><a href="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/xxx.mp3">https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/xxx.mp3</a>。</li></ul></li><li><p>临时URL：</p><ul><li>支持OSS协议，必须通过<a href="../model-api-reference/more-about-models/get-temporary-file-url.md">上传文件获取临时 URL</a>。</li><li>示例值：oss://dashscope-instant/xxx/2024-07-18/xxx/xxx.mp3。</li></ul></li></ol><p>音频限制：</p><ul><li>格式：wav、mp3。</li><li>时长：3～30s。</li><li>文件大小：不超过15MB。</li><li>超限处理：若音频长度超过 <code>duration</code> 值（5秒或10秒），自动截取前5秒或10秒，其余部分丢弃。若音频长度不足视频时长，超出音频长度部分为无声视频。例如，音频为3秒，视频时长为5秒，输出视频前3秒有声，后2秒无声。</li></ul><p>示例值：<a href="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/ozwpvi/rap.mp3"></a><a href="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/ozwpvi/rap.mp3">https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/ozwpvi/rap.mp3</a>。</p><p><strong>template</strong> <code>string</code> （可选）</p><p>视频特效模板的名称。若未填写，表示不使用任何视频特效。</p><p>不同模型支持不同的特效模板。调用前请查阅<a href="wanx-video-effects-5b23bdd72b8e7944.md">万相-图生视频-视频特效列表</a>，以免调用失败。</p><p>示例值：flying，表示使用“魔法悬浮”特效。</p></div></section><p><strong>parameters</strong> <code>object</code> （可选）</p><p>视频处理参数，如设置视频分辨率、设置视频时长、开启prompt智能改写、添加水印等。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>resolution</strong> <code>string</code> （可选）</p><div><div><p><strong>重要</strong>resolution直接影响费用，请在调用前确认<a href="../model-user-guide/test-1/model-pricing.md#517789fb633zr">模型价格</a>。</p></div></div><p>指定生成的视频分辨率档位，用于调整视频的清晰度（总像素）。模型根据选择的分辨率档位，自动缩放至相近总像素，<strong>视频宽高比将尽量与输入图像 img_url 的宽高比保持一致</strong>，详见<a href="legacy-image-to-video-api-reference-8b02dd673da405f1.md#2b6ac4aea9h5n">常见问题</a>。</p><p>此参数的默认值和可用枚举值依赖于 model 参数，规则如下：</p><ul><li>wan2.6-i2v-flash：可选值：720P、1080P。默认值为<code>1080P</code>。</li><li>wan2.6-i2v ：可选值：720P、1080P。默认值为<code>1080P</code>。</li><li>wan2.5-i2v-preview ：可选值：480P、720P、1080P。默认值为<code>1080P</code>。</li><li>wan2.2-i2v-flash：可选值：480P、720P、1080P。默认值为<code>720P</code>。</li><li>wan2.2-i2v-plus：可选值：480P、1080P。默认值为<code>1080P</code>。</li><li>wanx2.1-i2v-turbo：可选值：480P、720P。默认值为<code>720P</code>。</li><li>wanx2.1-i2v-plus：可选值：720P。默认值为<code>720P</code>。</li></ul><p>示例值：1080P。</p><p><strong>duration</strong> <code>integer</code> （可选）</p><div><div><p><strong>重要</strong>duration直接影响费用，请在调用前确认<a href="../model-user-guide/test-1/model-pricing.md#517789fb633zr">模型价格</a>。</p></div></div><p>生成视频的时长，单位为秒。该参数的取值依赖于 model参数：</p><ul><li>wan2.6-i2v-flash：取值为[2, 15]之间的整数。默认值为5。</li><li>wan2.6-i2v：取值为[2, 15]之间的整数。默认值为5。</li><li>wan2.5-i2v-preview：可选值为5、10。默认值为5。</li><li>wan2.2-i2v-plus：固定为5秒，且不支持修改。</li><li>wan2.2-i2v-flash：固定为5秒，且不支持修改。</li><li>wanx2.1-i2v-plus：固定为5秒，且不支持修改。</li><li>wanx2.1-i2v-turbo：可选值为3、4或5。默认值为5。</li></ul><p>示例值：5。</p><p><strong>prompt_extend</strong><code>boolean</code> （可选）</p><p>是否开启prompt智能改写。开启后使用大模型对输入prompt进行智能改写。对于较短的prompt生成效果提升明显，但会增加耗时。</p><ul><li>true：默认值，开启智能改写。</li><li>false：不开启智能改写。</li></ul><p>示例值：true。</p><p><strong>shot_type</strong> <code>string</code> （可选）</p><strong>支持模型：wan2.6系列模型。</strong><p>指定生成视频的镜头类型，即视频是由一个连续镜头还是多个切换镜头组成。</p><p>生效条件：仅当<code>&quot;prompt_extend&quot;: true</code> 时生效。</p><p>参数优先级：<code>shot_type &gt; prompt</code>。例如，若 shot_type设置为&quot;single&quot;，即使 prompt 中包含“生成多镜头视频”，模型仍会输出单镜头视频。</p><p>可选值：</p><ul><li>single：默认值，输出单镜头视频</li><li>multi：输出多镜头视频。</li></ul><p>示例值：single。</p><div><div><p><strong>说明</strong>当希望严格控制视频的叙事结构（如产品展示用单镜头、故事短片用多镜头），可通过此参数指定。</p></div></div><p><strong>audio</strong> <code>boolean</code> （可选）</p><div><div><p><strong>重要</strong>audio直接影响费用，有声视频与无声视频价格不同，请前往百炼控制台查看价格。</p></div></div><strong>支持模型：wan2.6-i2v-flash。</strong><p>是否生成有声视频。</p><p>参数优先级：<code>audio &gt; audio_url</code>。当 <code>audio=false</code>时，即使传入 <code>audio_url</code>，输出仍为无声视频，且计费按无声视频计算。</p><p>可选值：</p><ul><li>true：默认值，输出有声视频。</li><li>false：输出无声视频。</li></ul><p>示例值：true。</p><p><strong>watermark</strong> <code>boolean</code> （可选）</p><p>是否添加水印标识，水印位于视频右下角，文案固定为“AI生成”。</p><ul><li>false：默认值，不添加水印。</li><li>true：添加水印。</li></ul><p>示例值：false。</p><p><strong>seed</strong><code>integer</code>（可选）</p><p>随机数种子，取值范围为<code>[0, 2147483647]</code>。</p><p>未指定时，系统自动生成随机种子。若需提升生成结果的可复现性，建议固定seed值。</p><p>请注意，由于模型生成具有概率性，即使使用相同 seed，也不能保证每次生成结果完全一致。</p><p>示例值：12345。</p></div></section></td><td><a id="sec-tabs-2"></a><section><a id="多镜头叙事"></a><section><a id="多镜头叙事-h4"></a><h4>多镜头叙事</h4><p>仅wan2.6系列模型支持此功能。</p><p>可通过设置<code>&quot;prompt_extend&quot;: true</code>和<code>&quot;shot_type&quot;:&quot;multi&quot;</code>启用。</p><a id="code-block"></a><pre class="language-bash"><code># 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。

curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;wan2.6-i2v-flash&quot;,
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色。一个由喷漆所画成的少年，正从一面混凝土墙上活过来。他一边用极快的语速演唱一首英文rap，一边摆着一个经典的、充满活力的说唱歌手姿势。场景设定在夜晚一个充满都市感的铁路桥下。灯光来自一盏孤零零的街灯，营造出电影般的氛围，充满高能量和惊人的细节。视频的音频部分完全由他的rap构成，没有其他对话或杂音。&quot;,
        &quot;img_url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/wpimhv/rap.png&quot;,
        &quot;audio_url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/ozwpvi/rap.mp3&quot;
    },
    &quot;parameters&quot;: {
        &quot;resolution&quot;: &quot;720P&quot;,
        &quot;prompt_extend&quot;: true,
        &quot;duration&quot;: 10,
        &quot;shot_type&quot;:&quot;multi&quot;
    }
}'
</code></pre></section><a id="自动配音"></a><section><a id="自动配音-h4"></a><h4>自动配音</h4><p>仅wan2.6和wan2.5系列模型支持此功能。</p><p>若不提供 <code>input.audio_url</code> ，模型将根据视频内容自动生成匹配的背景音乐或音效。</p><a id="code-block-2"></a><pre class="language-bash"><code># 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。

curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;wan2.5-i2v-preview&quot;,
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色。一个由喷漆所画成的少年，正从一面混凝土墙上活过来。他一边用极快的语速演唱一首英文rap，一边摆着一个经典的、充满活力的说唱歌手姿势。场景设定在夜晚一个充满都市感的铁路桥下。灯光来自一盏孤零零的街灯，营造出电影般的氛围，充满高能量和惊人的细节。视频的音频部分完全由他的rap构成，没有其他对话或杂音。&quot;,
        &quot;img_url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/wpimhv/rap.png&quot;
    },
    &quot;parameters&quot;: {
        &quot;resolution&quot;: &quot;480P&quot;,
        &quot;prompt_extend&quot;: true,
        &quot;duration&quot;: 10
    }
}'
</code></pre></section><a id="传入音频文件"></a><section><a id="传入音频文件-h4"></a><h4>传入音频文件</h4><p>仅wan2.6和wan2.5系列模型支持此功能。</p><p>如需为视频指定背景音乐或配音，可通过 <code>input.audio_url</code> 参数传入自定义音频的 URL。</p><a id="code-block-3"></a><pre class="language-bash"><code># 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。

curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;wan2.5-i2v-preview&quot;,
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色。一个由喷漆所画成的少年，正从一面混凝土墙上活过来。他一边用极快的语速演唱一首英文rap，一边摆着一个经典的、充满活力的说唱歌手姿势。场景设定在夜晚一个充满都市感的铁路桥下。灯光来自一盏孤零零的街灯，营造出电影般的氛围，充满高能量和惊人的细节。视频的音频部分完全由他的rap构成，没有其他对话或杂音。&quot;,
        &quot;img_url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/wpimhv/rap.png&quot;,
        &quot;audio_url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/ozwpvi/rap.mp3&quot;
    },
    &quot;parameters&quot;: {
        &quot;resolution&quot;: &quot;480P&quot;,
        &quot;prompt_extend&quot;: true,
        &quot;duration&quot;: 10
    }
}'
</code></pre></section><a id="生成无声视频"></a><section><a id="生成无声视频-h4"></a><h4>生成无声视频</h4><p>仅以下模型支持生成无声视频：</p><ul><li>wan2.6-i2v-flash：若需生成无声视频，<strong>必须显式设置</strong> <code>parameters.audio = false</code>。</li><li>wan2.2 和wanx2.1系列模型：默认生成无声视频，无需额外参数配置。</li></ul><a id="code-block-4"></a><pre class="language-bash"><code># 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。

curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;wan2.2-i2v-plus&quot;,
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;一只猫在草地上奔跑&quot;,
        &quot;img_url&quot;: &quot;https://cdn.translate.alibaba.com/r/wanx-demo-1.png&quot;
    },
    &quot;parameters&quot;: {
        &quot;resolution&quot;: &quot;480P&quot;,
        &quot;prompt_extend&quot;: true
    }
}'
</code></pre></section><a id="使用base64"></a><section><a id="使用base64-h4"></a><h4>使用Base64</h4><p>通过 <code>img_url</code> 参数传入图像的 Base64 编码字符串。</p><p>关于 Base64 字符串的格式要求，请参见<a href="../model-user-guide/use-cases/legacy-resources/legacy-video-generation/image-to-video-guide.md#32d9db99f1fk0">传入图像</a>。</p><p>示例：下载<a href="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250722/pmcjis/img_base64.txt">img_base64</a>文件，并将完整内容粘贴至<code>img_url</code>参数中。</p><a id="code-block-5"></a><pre class="language-bash"><code># 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。

curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;wan2.2-i2v-plus&quot;,
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;一只猫在草地上奔跑&quot;,
        &quot;img_url&quot;: &quot;data:image/png;base64,GDU7MtCZzEbTbmRZ......&quot;
    },
    &quot;parameters&quot;: {
        &quot;resolution&quot;: &quot;480P&quot;,
        &quot;prompt_extend&quot;: true
    }
}'
</code></pre></section><a id="使用视频特效"></a><section><a id="使用视频特效-h4"></a><h4>使用视频特效</h4><ul><li>prompt 字段将被忽略，建议留空。</li><li>特效的可用性与模型相关。调用前请查阅<a href="wanx-video-effects-5b23bdd72b8e7944.md">万相-图生视频-视频特效列表</a>，以免调用失败。</li></ul><a id="code-block-6"></a><pre class="language-bash"><code># 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。

curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;wanx2.1-i2v-turbo&quot;,
    &quot;input&quot;: {
        &quot;img_url&quot;: &quot;https://cdn.translate.alibaba.com/r/wanx-demo-1.png&quot;,
        &quot;template&quot;: &quot;flying&quot;
    },
    &quot;parameters&quot;: {
        &quot;resolution&quot;: &quot;720P&quot;
    }
}'
</code></pre></section><a id="使用反向提示词"></a><section><a id="使用反向提示词-h4"></a><h4>使用反向提示词</h4><p>通过 negative_prompt 指定生成的视频避免出现“花朵”元素。</p><a id="code-block-7"></a><pre class="language-bash"><code># 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。

curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;wan2.2-i2v-plus&quot;,
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;一只猫在草地上奔跑&quot;,
        &quot;negative_prompt&quot;: &quot;花朵&quot;,
        &quot;img_url&quot;: &quot;https://cdn.translate.alibaba.com/r/wanx-demo-1.png&quot;
    },
    &quot;parameters&quot;: {
        &quot;resolution&quot;: &quot;480P&quot;,
        &quot;prompt_extend&quot;: true
    }
}'
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="cd3063363egdc"></a><a id="f5d1a44542v6q"></a><h4>响应参数</h4><p><strong>output</strong> <code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../model-api-reference/preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../model-api-reference/preparations/error-code.md">错误码</a>。</p></td><td><a id="sec-tabs-3"></a><section><a id="成功响应"></a><section><a id="成功响应-h4"></a><h4>成功响应</h4><p>请保存 task_id，用于查询任务状态与结果。</p><a id="code-block-8"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
        &quot;task_status&quot;: &quot;PENDING&quot;,
        &quot;task_id&quot;: &quot;0385dc79-5ff8-4d82-bcb6-xxxxxx&quot;
    },
    &quot;request_id&quot;: &quot;4909100c-7b5a-9f92-bfe5-xxxxxx&quot;
}
</code></pre></section><a id="异常响应"></a><section><a id="异常响应-h4"></a><h4>异常响应</h4><p>创建任务失败，请参见<a href="../model-api-reference/preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-9"></a><pre class="language-json"><code>{
    &quot;code&quot;: &quot;InvalidApiKey&quot;,
    &quot;message&quot;: &quot;No API-key provided.&quot;,
    &quot;request_id&quot;: &quot;7438d53d-6eb8-4596-8835-xxxxxx&quot;
}
</code></pre></section></section></td></tr></tbody></table>

<a id="步骤2-根据任务id查询结果"></a>

<a id="420e6e77a17om"></a>

<a id="80128613c02kf"></a>

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

<a id="弗吉尼亚-2"></a>

<a id="弗吉尼亚-2-h4"></a>

#### 弗吉尼亚

`GET https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v1/tasks/{task_id}`

<a id="法兰克福-2"></a>

<a id="法兰克福-2-h4"></a>

#### 法兰克福

`GET https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/api/v1/tasks/{task_id}`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

> **说明**
>
> -   **轮询建议**：视频生成过程约需数分钟，建议采用**轮询**机制，并设置合理的查询间隔（如 15 秒）来获取结果。
> -   **任务状态流转**：PENDING（排队中）→ RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。
> -   **结果链接**：任务成功后返回视频链接，有效期为 **24 小时**。建议在获取链接后立即下载并转存至永久存储（如[阿里云 OSS](https://help.aliyun.com/zh/oss/user-guide/what-is-oss)）。
> -   **task\_id 有效期**：**24小时**，超时后将无法查询结果，接口将返回任务状态为`UNKNOWN`。
> -   **RPS 限制**：查询接口默认RPS为20。如需更高频查询或事件通知，建议[配置异步任务回调](../model-api-reference/more-about-models/async-task-api.md)。
> -   **更多操作**：如需批量查询、取消任务等操作，请参见[管理异步任务](../model-api-reference/more-about-models/manage-asynchronous-tasks.md)。

<table><tbody><tr><td><a id="a9e0408c70ylw"></a><a id="b43fdb7196o58"></a><h4>请求参数</h4><a id="2d2fb41da6idy"></a><h5>请求头（Headers）</h5><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><a id="031d8a0fafqhp"></a><h5>URL路径参数（Path parameters）</h5><p><strong>task_id</strong> <code>string</code><strong>（必选）</strong></p><p>任务ID。</p></td><td><a id="sec-tabs-5"></a><section><a id="查询任务结果"></a><section><a id="查询任务结果-h4"></a><h4>查询任务结果</h4><p>将<code>{task_id}</code>完整替换为上一步接口返回的<code>task_id</code>的值。<code>task_id</code>查询有效期为24小时，并请将<code>{WorkspaceId}</code>替换为真实的<a href="../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain">业务空间ID</a>。</p><a id="code-block-10"></a><pre class="language-bash"><code>curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id} \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="810682d979i8q"></a><a id="209bb8b8c8976"></a><h4>响应参数</h4><p><strong>output</strong><code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值-2"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section><strong>轮询过程中的状态流转：</strong><ul><li>PENDING（排队中） → RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。</li><li>初次查询状态通常为 PENDING（排队中）或 RUNNING（处理中）。</li><li>当状态变为 SUCCEEDED 时，响应中将包含生成的视频URL。</li><li>若状态为 FAILED，请检查错误信息并重试。</li><li>若状态为 CANCELED，表示任务已取消，如需继续请重新提交任务。</li><li>若状态为 UNKNOWN，表示任务不存在或状态未知，可能在 task_id 不存在或超过 24 小时有效期后出现。</li></ul><p><strong>submit_time</strong> <code>string</code></p><p>任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>scheduled_time</strong> <code>string</code></p><p>任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>end_time</strong> <code>string</code></p><p>任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>video_url</strong><code>string</code></p><p>视频URL。仅在 task_status 为 SUCCEEDED 时返回。</p><p>链接有效期24小时，可通过此URL下载视频。视频格式为MP4（H.264 编码）。</p><p><strong>orig_prompt</strong> <code>string</code></p><p>原始输入的prompt，对应请求参数<code>prompt</code>。</p><p><strong>actual_prompt</strong> <code>string</code></p><p>当 <code>prompt_extend=true</code> 时，系统会对输入 prompt 进行智能改写，此字段返回实际用于生成的优化后 prompt。</p><ul><li>若 <code>prompt_extend=false</code>，该字段不会返回。</li><li>注意：wan2.6 模型无论 <code>prompt_extend</code> 取值如何，均不返回此字段。</li></ul><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../model-api-reference/preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../model-api-reference/preparations/error-code.md">错误码</a>。</p></div></section><p><strong>usage</strong> <code>object</code></p><p>输出信息统计，只对成功的结果计数。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><a id="accordion-wan2-6系列模型返回参数"></a><section><p>wan2.6系列模型返回参数</p><div><p><strong>input_video_duration</strong> <code>integer</code></p><p>输入的视频的时长，单位秒。当前不支持传入视频，因此固定为0。</p><p><strong>output_video_duration</strong> <code>integer</code></p><p>仅在使用 wan2.6 模型时返回。</p><p>输出视频的时长，单位秒。其值等同于<code>input.duration</code>的值。</p><p><strong>duration</strong> <code>integer</code></p><p>总的视频时长，用于计费。</p><p>计费公式：<code>duration=input_video_duration+output_video_duration</code>。</p><p><strong>SR</strong> <code>integer</code></p><p>仅在使用 wan2.6 模型时返回。生成视频的分辨率档位。示例值：720。</p><p><strong>video_count</strong> <code>integer</code></p><p>生成视频的数量。固定为1。</p><p><strong>audio</strong><code>boolean</code></p><p>仅在使用wan2.6-i2v-flash模型时返回。表示输出视频是否为有声视频。</p></div></section><a id="accordion-wan2-2和wan2-5系列模型返回参数"></a><section><p>wan2.2和wan2.5系列模型返回参数</p><div><p><strong>duration</strong> <code>integer</code></p><p>生成视频的时长，单位为秒。枚举值为5、10。</p><p>计费公式：费用 = 视频秒数 × 单价。</p><p><strong>SR</strong> <code>integer</code></p><p>生成视频的分辨率。枚举值为480、720、1080。</p><p><strong>video_count</strong> <code>integer</code></p><p>生成视频的数量。固定为1。</p></div></section><a id="accordion-wan2-1系列模型返回参数"></a><section><p>wan2.1系列模型返回参数</p><div><p><strong>video_duration</strong> <code>integer</code></p><p>生成视频的时长，单位为秒。枚举值为3、4、5。</p><p>计费公式：费用 = 视频秒数 × 单价。</p><p><strong>video_ratio</strong> <code>string</code></p><p>生成视频的比例。固定为standard。</p><p><strong>video_count</strong> <code>integer</code></p><p>生成视频的数量。固定为1。</p></div></section></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p></td><td><a id="sec-tabs-6"></a><section><a id="任务执行成功"></a><section><a id="任务执行成功-h4"></a><h4>任务执行成功</h4><p>视频URL仅保留24小时，超时后会被自动清除，请及时保存生成的视频。</p><a id="code-block-11"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;2ca1c497-f9e0-449d-9a3f-xxxxxx&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;af6efbc0-4bef-4194-8246-xxxxxx&quot;,
        &quot;task_status&quot;: &quot;SUCCEEDED&quot;,
        &quot;submit_time&quot;: &quot;2025-09-25 11:07:28.590&quot;,
        &quot;scheduled_time&quot;: &quot;2025-09-25 11:07:35.349&quot;,
        &quot;end_time&quot;: &quot;2025-09-25 11:17:11.650&quot;,
        &quot;orig_prompt&quot;: &quot;一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色。一个由喷漆所画成的少年，正从一面混凝土墙上活过来。他一边用极快的语速演唱一首英文rap，一边摆着一个经典的、充满活力的说唱歌手姿势。场景设定在夜晚一个充满都市感的铁路桥下。灯光来自一盏孤零零的街灯，营造出电影般的氛围，充满高能量和惊人的细节。视频的音频部分完全由他的rap构成，没有其他对话或杂音。&quot;,
        &quot;video_url&quot;: &quot;https://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/xxx.mp4?Expires=xxx&quot;
    },
    &quot;usage&quot;: {
        &quot;duration&quot;: 10,
        &quot;input_video_duration&quot;: 0,
        &quot;output_video_duration&quot;: 10,
        &quot;video_count&quot;: 1,
        &quot;SR&quot;: 720
    }
}
</code></pre></section><a id="任务执行失败"></a><section><a id="任务执行失败-h4"></a><h4>任务执行失败</h4><p>若任务执行失败，task_status将置为 FAILED，并提供错误码和信息。请参见<a href="../model-api-reference/preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-12"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;e5d70b02-ebd3-98ce-9fe8-759d7d7b107d&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;86ecf553-d340-4e21-af6e-a0c6a421c010&quot;,
        &quot;task_status&quot;: &quot;FAILED&quot;,
        &quot;code&quot;: &quot;InvalidParameter&quot;,
        &quot;message&quot;: &quot;The size is not match xxxxxx&quot;
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

<a id="dashscope-sdk调用"></a>

<a id="db17b3098c2iv"></a>

<a id="41ca556e17lbx"></a>

## DashScope SDK调用

SDK 的参数命名与[HTTP接口](legacy-image-to-video-api-reference-8b02dd673da405f1.md#42703589880ts)基本一致，参数结构根据语言特性进行封装。

由于图生视频任务耗时较长（通常为1-5分钟），SDK 在底层封装了 HTTP 异步调用流程，支持同步、异步两种调用方式。

> 具体耗时受限于排队任务数和服务执行情况，请在获取结果时耐心等待。

<a id="python-sdk调用"></a>

<a id="a3ad9a3b6d9if"></a>

<a id="cf97f2c7e50cg"></a>

### Python SDK调用

> **重要**
>
> 请确保 DashScope Python SDK 版本**不低于**2.0.1，再运行以下代码。
>
> 若版本过低，可能会触发 “url error, please check url!” 等错误。请参考[安装SDK](../model-api-reference/preparations/install-sdk.md)进行更新。

根据模型所在地域设置 `region`（构造 Client 时传入，各地域的region取值不同）：

<a id="sec-tabs-7"></a>

<a id="北京-3"></a>

<a id="北京-3-h4"></a>

#### 北京

`region="cn-beijing"`

<a id="新加坡-3"></a>

<a id="新加坡-3-h4"></a>

#### 新加坡

`region="ap-southeast-1"`

<a id="弗吉尼亚-3"></a>

<a id="弗吉尼亚-3-h4"></a>

#### 弗吉尼亚

`region="us-east-1"`

<a id="法兰克福-3"></a>

<a id="法兰克福-3-h4"></a>

#### 法兰克福

`region="eu-central-1"`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="示例代码"></a>

<a id="f2b1639e488og"></a>

<a id="b04667a06ed3d"></a>

#### 示例代码

<a id="sec-tabs-8"></a>

<a id="同步调用"></a>

<a id="同步调用-h4"></a>

#### 同步调用

同步调用会阻塞等待，直到视频生成完成并返回结果。本示例展示三种图像输入方式：公网URL、Base64编码、本地文件路径。

<a id="98834049b6p8l"></a>

<a id="33f9a763cd80s"></a>

##### 请求示例

<a id="code-block-14"></a>

```python
import base64
import os
import mimetypes
import dashscope
from dashscope import DashScopeError

# 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    # 获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

# --- 辅助函数：用于 Base64 编码 ---
# 格式为 data:{MIME_type};base64,{base64_data}
def encode_file(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type or not mime_type.startswith("image/"):
        raise ValueError("不支持或无法识别的图像格式")
    with open(file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return f"data:{mime_type};base64,{encoded_string}"

"""
图像输入方式说明：
以下提供了三种图片输入方式，三选一即可

1. 使用公网URL - 适合已有公开可访问的图片
2. 使用本地文件 - 适合本地开发测试
3. 使用Base64编码 - 适合私有图片或需要加密传输的场景
"""

# 【方式一】使用公网可访问的图片URL
# 示例：使用一个公开的图片URL
img_url = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/wpimhv/rap.png"

# 【方式二】使用本地文件（支持绝对路径和相对路径）
# 格式要求：file:// + 文件路径
# 示例（绝对路径）：
# img_url = "file://" + "/path/to/your/img.png"    # Linux/macOS
# img_url = "file://" + "/C:/path/to/your/img.png"  # Windows
# 示例（相对路径）：
# img_url = "file://" + "./img.png"                # 相对当前执行文件的路径

# 【方式三】使用Base64编码的图片
# img_url = encode_file("./img.png")

# 设置音频audio url
audio_url = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/ozwpvi/rap.mp3"

def sample_call_i2v():
    # generate 为一步式调用（提交任务并等待完成），返回已完成的 Job
    print('please wait...')
    # audio_url / negative_prompt 为 input 段字段，不在具名签名内，经 extra_input 透传
    try:
        job = client.videos.generate(model='wan2.6-i2v-flash',
                                     prompt='一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色。一个由喷漆所画成的少年，正从一面混凝土墙上活过来。他一边用极快的语速演唱一首英文rap，一边摆着一个经典的、充满活力的说唱歌手姿势。场景设定在夜晚一个充满都市感的铁路桥下。灯光来自一盏孤零零的街灯，营造出电影般的氛围，充满高能量和惊人的细节。视频的音频部分完全由他的rap构成，没有其他对话或杂音。',
                                     image_url=img_url,
                                     extra_input={'audio_url': audio_url,
                                                  'negative_prompt': ""},
                                     resolution="720P",
                                     duration=10,
                                     prompt_extend=True,
                                     watermark=False,
                                     seed=12345)
        print(job)
        print("video_url:", job.video_url)
    except DashScopeError as e:
        print(f"HTTP返回码：{e.status_code}")
        print(f"错误码：{e.code}")
        print(f"错误信息：{e.message}")
        print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")

if __name__ == '__main__':
    sample_call_i2v()
```

<a id="818467b02dzvx"></a>

##### 响应示例

> video\_url 有效期24小时，请及时下载视频。

<a id="code-block-15"></a>

```json
{
    "request_id": "2794c7a3-fe8c-4dd4-a1b7-xxxxxx",
    "task_id": "c15d5b14-07c4-4af5-b862-xxxxxx",
    "status": "SUCCEEDED",
    "video_url": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx.mp4?Expires=xxx",
    "task_metrics": {
        "TOTAL": 1,
        "SUCCEEDED": 1,
        "FAILED": 0
    },
    "usage": {
        "video_count": 1,
        "duration": 10,
        "input_video_duration": 0,
        "output_video_duration": 10,
        "audio": true,
        "SR": 720
    }
}
```

<a id="异步调用"></a>

<a id="异步调用-h4"></a>

#### 异步调用

本示例展示异步调用方式。该方式立即返回任务 ID，可通过 fetch 查询状态，或调用 wait 等待完成（内部自动轮询）。

<a id="b047752bac2fz"></a>

<a id="6903511374pcv"></a>

##### 请求示例

<a id="code-block-16"></a>

```python
import os
import dashscope
from dashscope import DashScopeError

# 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    # 获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

# 使用公网可访问的图片URL
img_url = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/wpimhv/rap.png"

# 设置音频audio url
audio_url = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/ozwpvi/rap.mp3"

def sample_async_call_i2v():
    # 异步调用，返回一个task_id
    # audio_url / negative_prompt 为 input 段字段，不在具名签名内，经 extra_input 透传
    try:
        job = client.videos.jobs.create(model='wan2.6-i2v-flash',
                                        prompt='一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色。一个由喷漆所画成的少年，正从一面混凝土墙上活过来。他一边用极快的语速演唱一首英文rap，一边摆着一个经典的、充满活力的说唱歌手姿势。场景设定在夜晚一个充满都市感的铁路桥下。灯光来自一盏孤零零的街灯，营造出电影般的氛围，充满高能量和惊人的细节。视频的音频部分完全由他的rap构成，没有其他对话或杂音。',
                                        image_url=img_url,
                                        extra_input={'audio_url': audio_url,
                                                     'negative_prompt': ""},
                                        resolution="720P",
                                        duration=10,
                                        prompt_extend=True,
                                        watermark=False,
                                        seed=12345)
        print(job)
        print("task_id: %s" % job.task_id)
    except DashScopeError as e:
        print(f"HTTP返回码：{e.status_code}")
        print(f"错误码：{e.code}")
        print(f"错误信息：{e.message}")
        print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
        return

    # 获取异步任务信息
    try:
        snapshot = client.videos.jobs.fetch(job.task_id)
        print(snapshot.status)
    except DashScopeError as e:
        print(f"HTTP返回码：{e.status_code}")
        print(f"错误码：{e.code}")
        print(f"错误信息：{e.message}")
        print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")

    # 等待异步任务结束（指数退避轮询，默认总预算24小时）
    try:
        done = client.videos.jobs.wait(job)
        print(done)
        print(done.video_url)
    except DashScopeError as e:
        print(f"HTTP返回码：{e.status_code}")
        print(f"错误码：{e.code}")
        print(f"错误信息：{e.message}")
        print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")

if __name__ == '__main__':
    sample_async_call_i2v()
```

<a id="15a0d419b9q5r"></a>

##### 响应示例

1、创建任务的响应示例

<a id="code-block-17"></a>

```json
{
    "request_id": "6dc3bf6c-be18-9268-9c27-xxxxxx",
    "task_id": "686391d9-7ecf-4290-a8e9-xxxxxx",
    "status": "PENDING"
}
```

2、查询任务结果的响应示例

> video\_url 有效期24小时，请及时下载视频。

<a id="code-block-18"></a>

```json
{
    "request_id": "2794c7a3-fe8c-4dd4-a1b7-xxxxxx",
    "task_id": "c15d5b14-07c4-4af5-b862-xxxxxx",
    "status": "SUCCEEDED",
    "video_url": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx.mp4?Expires=xxx",
    "task_metrics": {
        "TOTAL": 1,
        "SUCCEEDED": 1,
        "FAILED": 0
    },
    "usage": {
        "video_count": 1,
        "duration": 10,
        "input_video_duration": 0,
        "output_video_duration": 10,
        "audio": true,
        "SR": 720
    }
}
```

<a id="java-sdk调用"></a>

<a id="589b80853e6rn"></a>

<a id="0910550f7e6es"></a>

### Java SDK调用

> **重要**
>
> 请确保 DashScope Java SDK 版本**不低于**`2.22.6`，再运行以下代码。
>
> 若版本过低，可能会触发 “url error, please check url!” 等错误。请参考[安装SDK](../model-api-reference/preparations/install-sdk.md)进行更新。

根据模型所在地域设置 `baseHttpApiUrl`：

<a id="sec-tabs-9"></a>

<a id="北京-4"></a>

<a id="北京-4-h4"></a>

#### 北京

`Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";`

<a id="新加坡-4"></a>

<a id="新加坡-4-h4"></a>

#### 新加坡

`Constants.baseHttpApiUrl = "https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1";`

<a id="弗吉尼亚-4"></a>

<a id="弗吉尼亚-4-h4"></a>

#### 弗吉尼亚

`Constants.baseHttpApiUrl = "https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v1";`

<a id="法兰克福-4"></a>

<a id="法兰克福-4-h4"></a>

#### 法兰克福

`Constants.baseHttpApiUrl = "https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/api/v1";`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="示例代码-2"></a>

<a id="ae42e9ea5chzu"></a>

<a id="fabb5a6cf8y2e"></a>

#### 示例代码

<a id="sec-tabs-10"></a>

<a id="同步调用-2"></a>

<a id="同步调用-2-h4"></a>

#### 同步调用

同步调用会阻塞等待，直到视频生成完成并返回结果。本示例展示三种图像输入方式：公网URL、Base64编码、本地文件路径。

<a id="3e3609efb9rhl"></a>

<a id="e32ffd6888esr"></a>

##### 请求示例

<a id="code-block-19"></a>

```java
// Copyright (c) Alibaba, Inc. and its affiliates.

import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesis;
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisParam;
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.JsonUtils;
import com.alibaba.dashscope.utils.Constants;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Base64;
import java.util.HashMap;
import java.util.Map;

public class Image2Video {

    static {
        // 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
        // 获取URL：https://help.aliyun.com/zh/model-studio/image-to-video-api-reference
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
    }

    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey="sk-xxx"
    // 获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    /**
     * 图像输入方式说明：三选一即可
     *
     * 1. 使用公网URL - 适合已有公开可访问的图片
     * 2. 使用本地文件 - 适合本地开发测试
     * 3. 使用Base64编码 - 适合私有图片或需要加密传输的场景
     */

    //【方式一】公网URL
    static String imgUrl = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/wpimhv/rap.png";

    //【方式二】本地文件路径（file://+绝对路径）
    // static String imgUrl = "file://" + "/your/path/to/img.png";    // Linux/macOS
    // static String imgUrl = "file://" + "/C:/your/path/to/img.png";  // Windows

    //【方式三】Base64编码
    // static String imgUrl = Image2Video.encodeFile("/your/path/to/img.png");

    // 设置音频audio url
    static String audioUrl = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/ozwpvi/rap.mp3";

    public static void image2video() throws ApiException, NoApiKeyException, InputRequiredException {
        // 设置parameters参数
        Map<String, Object> parameters = new HashMap<>();
        parameters.put("prompt_extend", true);
        parameters.put("watermark", false);
        parameters.put("seed", 12345);

        VideoSynthesis vs = new VideoSynthesis();
        VideoSynthesisParam param =
                VideoSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("wan2.6-i2v-flash")
                        .prompt("一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色。一个由喷漆所画成的少年，正从一面混凝土墙上活过来。他一边用极快的语速演唱一首英文rap，一边摆着一个经典的、充满活力的说唱歌手姿势。场景设定在夜晚一个充满都市感的铁路桥下。灯光来自一盏孤零零的街灯，营造出电影般的氛围，充满高能量和惊人的细节。视频的音频部分完全由他的rap构成，没有其他对话或杂音。")
                        .imgUrl(imgUrl)
                        .audioUrl(audioUrl)
                        .duration(10)
                        .parameters(parameters)
                        .resolution("720P")
                        .negativePrompt("")
                        .build();
        System.out.println("please wait...");
        VideoSynthesisResult result = vs.call(param);
        System.out.println(JsonUtils.toJson(result));
    }

     /**
     * 将文件编码为Base64字符串
     * @param filePath 文件路径
     * @return Base64字符串，格式为 data:{MIME_type};base64,{base64_data}
     */
    public static String encodeFile(String filePath) {
        Path path = Paths.get(filePath);
        if (!Files.exists(path)) {
            throw new IllegalArgumentException("文件不存在: " + filePath);
        }
        // 检测MIME类型
        String mimeType = null;
        try {
            mimeType = Files.probeContentType(path);
        } catch (IOException e) {
            throw new IllegalArgumentException("无法检测文件类型: " + filePath);
        }
        if (mimeType == null || !mimeType.startsWith("image/")) {
            throw new IllegalArgumentException("不支持或无法识别的图像格式");
        }
        // 读取文件内容并编码
        byte[] fileBytes = null;
        try{
            fileBytes = Files.readAllBytes(path);
        } catch (IOException e) {
            throw new IllegalArgumentException("无法读取文件内容: " + filePath);
        }

        String encodedString = Base64.getEncoder().encodeToString(fileBytes);
        return "data:" + mimeType + ";base64," + encodedString;
    }

    public static void main(String[] args) {
        try {
            image2video();
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

<a id="dfe6c9cc786iy"></a>

##### 响应示例

> video\_url 有效期24小时，请及时下载视频。

<a id="code-block-20"></a>

```json
{
    "request_id": "87c091bb-7a3c-4904-8501-xxxxxx",
    "output": {
        "task_id": "413ed6e4-5f3a-4f57-8d58-xxxxxx",
        "task_status": "SUCCEEDED",
        "video_url": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx.mp4?Expires=xxx",
        "orig_prompt": "一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色。一个由喷漆所画成的少年，正从一面混凝土墙上活过来。他一边用极快的语速演唱一首英文rap，一边摆着一个经典的、充满活力的说唱歌手姿势。场景设定在夜晚一个充满都市感的铁路桥下。灯光来自一盏孤零零的街灯，营造出电影般的氛围，充满高能量和惊人的细节。视频的音频部分完全由他的rap构成，没有其他对话或杂音。",
        "submit_time": "2026-01-22 23:25:45.729",
        "scheduled_time": "2026-01-22 23:25:45.771",
        "end_time": "2026-01-22 23:26:44.942"
    },
    "usage": {
        "video_count": 1,
        "duration": 10.0,
        "input_video_duration": 0.0,
        "output_video_duration": 10.0,
        "SR": "720"
    },
    "status_code": 200,
    "code": "",
    "message": ""
}
```

<a id="异步调用-2"></a>

<a id="异步调用-2-h4"></a>

#### 异步调用

本示例展示异步调用方式。该方式会立即返回任务ID，需要自行轮询或等待任务完成。

<a id="2fc30f223b9py"></a>

<a id="5b5e9e31ecl3l"></a>

##### 请求示例

<a id="code-block-21"></a>

```java
// Copyright (c) Alibaba, Inc. and its affiliates.

import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesis;
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisListResult;
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisParam;
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.task.AsyncTaskListParam;
import com.alibaba.dashscope.utils.JsonUtils;
import com.alibaba.dashscope.utils.Constants;

import java.util.HashMap;
import java.util.Map;

public class Image2Video {

    static {
        // 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
        // 获取URL：https://help.aliyun.com/zh/model-studio/image-to-video-api-reference
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
    }

    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey="sk-xxx"
    // 获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    //设置输入图像url
    static String imgUrl = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/wpimhv/rap.png";

    // 设置音频audio url
    static String audioUrl = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/ozwpvi/rap.mp3";

    public static void image2video() throws ApiException, NoApiKeyException, InputRequiredException {
        // 设置parameters参数
        Map<String, Object> parameters = new HashMap<>();
        parameters.put("prompt_extend", true);
        parameters.put("watermark", false);
        parameters.put("seed", 12345);

        VideoSynthesis vs = new VideoSynthesis();
        VideoSynthesisParam param =
                VideoSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("wan2.6-i2v-flash")
                        .prompt("一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色。一个由喷漆所画成的少年，正从一面混凝土墙上活过来。他一边用极快的语速演唱一首英文rap，一边摆着一个经典的、充满活力的说唱歌手姿势。场景设定在夜晚一个充满都市感的铁路桥下。灯光来自一盏孤零零的街灯，营造出电影般的氛围，充满高能量和惊人的细节。视频的音频部分完全由他的rap构成，没有其他对话或杂音。")
                        .imgUrl(imgUrl)
                        .audioUrl(audioUrl)
                        .duration(10)
                        .parameters(parameters)
                        .resolution("720P")
                        .negativePrompt("")
                        .build();
        // 异步调用
        VideoSynthesisResult task = vs.asyncCall(param);
        System.out.println(JsonUtils.toJson(task));
        System.out.println("please wait...");

        //获取结果
        VideoSynthesisResult result = vs.wait(task, apiKey);
        System.out.println(JsonUtils.toJson(result));
    }

    // 获取任务列表
    public static void listTask() throws ApiException, NoApiKeyException {
        VideoSynthesis is = new VideoSynthesis();
        AsyncTaskListParam param = AsyncTaskListParam.builder().build();
        param.setApiKey(apiKey);
        VideoSynthesisListResult result = is.list(param);
        System.out.println(result);
    }

    // 获取单个任务结果
    public static void fetchTask(String taskId) throws ApiException, NoApiKeyException {
        VideoSynthesis is = new VideoSynthesis();
        // 如果已设置 DASHSCOPE_API_KEY 为环境变量，apiKey 可为空
        VideoSynthesisResult result = is.fetch(taskId, apiKey);
        System.out.println(result.getOutput());
        System.out.println(result.getUsage());
    }

    public static void main(String[] args) {
        try {
            image2video();
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

<a id="38e1e3c7303rm"></a>

##### 响应示例

1、创建任务的响应示例

<a id="code-block-22"></a>

```json
{
    "request_id": "5dbf9dc5-4f4c-9605-85ea-xxxxxxxx",
    "output": {
        "task_id": "7277e20e-aa01-4709-xxxxxxxx",
        "task_status": "PENDING"
    }
}
```

2、查询任务结果的响应示例

> video\_url 有效期24小时，请及时下载视频。

<a id="code-block-23"></a>

```json
{
    "request_id": "87c091bb-7a3c-4904-8501-xxxxxx",
    "output": {
        "task_id": "413ed6e4-5f3a-4f57-8d58-xxxxxx",
        "task_status": "SUCCEEDED",
        "video_url": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx.mp4?Expires=xxx",
        "orig_prompt": "一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色。一个由喷漆所画成的少年，正从一面混凝土墙上活过来。他一边用极快的语速演唱一首英文rap，一边摆着一个经典的、充满活力的说唱歌手姿势。场景设定在夜晚一个充满都市感的铁路桥下。灯光来自一盏孤零零的街灯，营造出电影般的氛围，充满高能量和惊人的细节。视频的音频部分完全由他的rap构成，没有其他对话或杂音。",
        "submit_time": "2026-01-22 23:25:45.729",
        "scheduled_time": "2026-01-22 23:25:45.771",
        "end_time": "2026-01-22 23:26:44.942"
    },
    "usage": {
        "video_count": 1,
        "duration": 10.0,
        "input_video_duration": 0.0,
        "output_video_duration": 10.0,
        "SR": "720"
    },
    "status_code": 200,
    "code": "",
    "message": ""
}
```

<a id="使用限制"></a>

<a id="445b4bb8acqle"></a>

<a id="3e28930521g0y"></a>

## 使用限制

-   **数据时效**：任务task\_id和 视频url均只保留 24 小时，过期后将无法查询或下载。
-   **内容审核**：输入的内容（如prompt、图像）、输出视频均会经过内容安全审核，含违规内容将返回 “IPInfringementSuspect”或“DataInspectionFailed”错误，详见参见[错误码](../model-api-reference/preparations/error-code.md)。

<a id="已知限制"></a>

<a id="known-limitations-title"></a>

<a id="known-limitations"></a>

## 已知限制

使用 **wan2.6-i2v-flash** 生成圆形物体连续旋转（如圆环、齿轮、表盘）的动画时，画面在约 3 秒后可能出现短暂卡顿（画面静止约 1 秒）。如需生成此类连续旋转效果，建议改用[万相2.7-图生视频](../model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)模型以规避此问题。

<a id="错误码"></a>

<a id="0d0a562d05nkh"></a>

<a id="2e1d8db361w9w"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](../model-api-reference/preparations/error-code.md)进行解决。

<a id="常见问题"></a>

<a id="2b6ac4aea9h5n"></a>

<a id="a3cf03d10dq3j"></a>

## 常见问题

<a id="q-如何生成特定宽高比-如3-4-的视频"></a>

<a id="646b718e448ww"></a>

<a id="aff1652b5a62n"></a>

#### Q：如何生成特定宽高比（如3:4）的视频？

**A：** 输出视频的宽高比由**输入首帧图像（img\_url）**决定，但**无法保证精确比例**（如严格3:4），会存在一定偏差。

-   **为什么会有偏差？**
    
    模型会以输入图像的比例为基准，结合设置的分辨率档位（resolution）总像素，自动计算出最接近的合法分辨率。由于要求视频的长和宽必须是 16 的倍数，模型会对最终分辨率做微调，因此无法保证输出比例严格等于 3:4，但会非常接近。
    
    -   例如：输入图像750×1000（宽高比 3:4 = 0.75），并设置 resolution = "720P"（目标总像素约 92 万），实际输出816×1104（宽高比 ≈ 0.739，总像素约90万）。
-   **实践建议**：
    
    -   **输入控制**：尽量使用与目标比例一致的图片作为首帧输入。
    -   **后期处理**：如果您对比例有严格要求，建议在视频生成后，使用编辑工具进行简单的裁剪或黑边填充。

<a id="q-如何获取视频存储的访问域名白名单"></a>

<a id="c7421e6e32dj8"></a>

<a id="03e78329f3mo2"></a>

#### Q：如何获取视频存储的访问域名白名单？

A： 模型生成的视频存储于阿里云OSS，API将返回一个临时的公网URL。**若需要对该下载地址进行防火墙白名单配置**，请注意：由于底层存储会根据业务情况进行动态变更，为避免过期信息影响访问，文档不提供固定的OSS域名白名单。如有安全管控需求，请联系客户经理获取最新OSS域名列表。
