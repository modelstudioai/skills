# 万相2.7-参考生视频API参考

万相-参考生视频模型支持 多模态输入 （图片、视频、音频），生成保持角色形象和音色一致性的视频，适用于单角色表演或多角色互动场景。

**相关文档**：[使用指南](../../../_short/video-to-video-guide-f63917cdae4414ac.md)

<a id="适用范围"></a>

<a id="1fd78afa5brlj"></a>

## 适用范围

为确保调用成功，请务必保证模型、Endpoint URL和API Key 均属于**同一地域**。跨地域调用将会失败。

-   [选择模型](../../../_short/video-to-video-guide-f63917cdae4414ac.md#06f39eafa2dwt)：确认模型所属的地域。
-   **选择 URL**：选择对应的地域 Endpoint URL，支持HTTP URL。
-   **配置API Key**：选择地域并[获取与配置 API Key](../../preparations/get-api-key.md)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

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

<a id="7f493e3256ajz"></a>

## HTTP调用

> **重要**
>
> 此接口为**新版协议**，支持**wan2.7模型**。

由于视频生成任务耗时较长（通常为1-5分钟），API采用异步调用。整个流程包含 **“创建任务 -> 轮询获取”** 两个核心步骤，具体如下：

<a id="步骤1-创建任务获取任务id"></a>

<a id="19494db8e8gey"></a>

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

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

> **说明**
>
> -   创建成功后，使用接口返回的 `task_id` 查询结果，task\_id 有效期为 24 小时。**请勿重复创建任务**，轮询获取即可。
> -   新手指引请参见[Postman](https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api)。

<table><tbody><tr><td><a id="34ce9ac268wb7"></a><h4>请求参数</h4><a id="69e447998dxho"></a><h5>请求头（Headers）</h5><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><p><strong>X-DashScope-Async</strong><code>string</code><strong>（必选）</strong></p><p>异步处理配置参数。HTTP请求只支持异步，<strong>必须设置为</strong><code>enable</code>。</p><div><div><p><strong>重要</strong>缺少此请求头将报错：“current user api does not support synchronous calls”。</p></div></div><a id="ad5d07b350xer"></a><h5>请求体（Request Body）</h5><p><strong>model</strong> <code>string</code> <strong>（必选）</strong></p><p>模型名称。模型列表与价格详见<a href="../../../model-user-guide/test-1/model-pricing.md#5c3d28ad8a4x8">模型价格</a>。</p><p>示例值：wan2.7-r2v、wan2.7-r2v-2026-06-12。</p><p><strong>input</strong> <code>object</code> <strong>（必选）</strong></p><p>输入的基本信息，如提示词等。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>prompt</strong> <code>string</code> <strong>（必选）</strong></p><p>文本提示词。用来描述生成视频中期望包含的元素和视觉特点。</p><p>支持中英文，每个汉字、字母、标点占一个字符，超过部分会自动截断。</p><ul><li>wan2.7-r2v、wan2.7-r2v-2026-06-12：不超过5000个字符。</li></ul><p><strong>参考指代</strong>：当为中文提示词时，参考图片时通过“<strong>图1、图2</strong>”这类标识指代，参考视频时通过“<strong>视频1、视频2</strong>”这类标识指代。英文提示词则写为“Image 1”、&quot;Video 1”这类标识。英文字母和数字之间有空格，首字母大写。顺序与<code>media</code>数组顺序一致。图和视频分别计数，即同时存在图1、视频1等标识。若参考素材有且仅有一张图片或一个视频，则可简化表述为”<strong>参考图片</strong>”或“<strong>参考视频</strong>”。</p><p><strong>画面描述</strong>：假设参考图1是一只猫，图2是一个房间，要描述猫在房间里玩耍，支持两种写法：一种是直接使用标识指代（如“图1在图2里玩耍”）；另一种是结合主体与场景补充说明（如“图1的猫在图2的房间里玩耍”）。</p><p>当参考图片为多宫格（故事板图像）时，提示词建议按照多分镜的形式描述画面内容。无需描述每个宫格，提供关键分镜内容即可，模型将自动识别宫格逻辑并智能补全镜头内容。为达到更好的效果，建议单次仅输入一张多宫格图。</p><p>提示词的使用技巧请参见<a href="../../../model-user-guide/use-cases/text-to-video-prompt.md">文生视频/图生视频Prompt指南</a>。</p><p><strong>negative_prompt</strong> <code>string</code> （可选）</p><p>反向提示词，用来描述不希望在视频画面中出现的内容，可以对视频画面进行限制。</p><p>支持中英文，长度不超过500个字符，超过部分会自动截断。</p><p>示例值：低分辨率、错误、最差质量、低质量、残缺、多余的手指、比例不良等。</p><p><strong>media</strong> <code>array</code> <strong>（必选）</strong></p><p>媒体素材数组，素材包括图像、视频和音频。支持图像/视频输入作为视觉参考，图像支持多视图，常见参考角色、道具、场景等。</p><ul><li><p>数组中每个元素为一个媒体对象，包含 <code>type</code> 与 <code>url</code> 字段。</p></li><li><p>按照数组顺序定义<code>prompt</code>中角色引用的顺序。图和视频分别计数，即可同时存在图1、视频1。</p><ul><li>数组中的第 1 个<code>reference_video</code> 对应 <strong>视频1</strong>，第 2 个对应 <strong>视频2</strong>，以此类推。</li><li>数组中的第 1 个<code>reference_image</code>对应 <strong>图1</strong>，第 2 个对应 <strong>图2</strong>，以此类推。</li></ul></li></ul><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>媒体素材类型。可选值为：</p><ul><li><p><code>reference_image</code>：参考图像。提供主体角色（人物/动物/物体）和场景参考。</p></li><li><p><code>reference_video</code>：参考视频。提供主体角色（人物/动物/物体）和音色参考，不推荐传入空镜视频。</p></li><li><p><code>first_frame</code>：首帧图像。基于首帧生成视频，通常包含主体角色（人物/动物/物体）。支持同时传入首帧图联合控制，常见用法如下：</p><ul><li>首帧中已经出现待参考主体：此时可以搭配主体参考强化一致性，或进行音色参考。</li><li>首帧中未出现待参考主体：此时可以用主体参考来定义视频动态过程中新出现的主体特征。</li></ul></li></ul><p>素材限制：</p><ul><li>首帧图像，最多传入1张。</li><li>参考图像和参考视频至少传入1个，<strong>参考图像 + 参考视频 ≤ 5</strong>。</li><li>参考素材为主体角色时，仅包含单一角色。</li></ul><p><strong>url</strong> <code>string</code> <strong>（必选）</strong></p><p>媒体素材URL。每个值可指向<strong>一张图像或一段视频</strong>。</p><a id="accordion-传入参考图像-type-reference-image"></a><section><p>传入参考图像（type=reference_image）</p><div><p>参考图像URL或 Base64 编码数据。参考图可以是主体（人物/动物/物体）或者背景。当包含主体时，仅包含一个角色。</p><p>图像限制：</p><ul><li>格式：JPEG、JPG、PNG（不支持透明通道）、BMP、WEBP。</li><li>分辨率：宽度和高度范围为[240, 8000]像素。</li><li>宽高比：1:8～8:1。</li><li>文件大小：不超过20MB。</li></ul><p>支持输入的格式：</p><ol><li><p>公网URL:</p><ul><li>支持HTTP或HTTPS协议。</li><li>示例值：<a href="https://xxx/xxx.png"></a><a href="https://xxx/xxx.png">https://xxx/xxx.png</a>。</li></ul></li><li><p>临时URL：</p><ul><li>支持OSS协议，必须通过<a href="../../more-about-models/get-temporary-file-url.md">上传文件获取临时 URL</a>。</li><li>示例值：oss://dashscope-instant/xxx/xxx.png。</li></ul></li><li><p>Base64 编码图像后的字符串：</p><ul><li>数据格式：<code>data:{MIME_type};base64,{base64_data}</code>。</li><li>示例值：data:image/png;base64,GDU7MtCZzEbTbmRZ......。（编码字符串过长，仅展示片段）</li><li>详情请参见<a href="../../../model-user-guide/use-cases/legacy-resources/legacy-video-generation/image-to-video-guide.md#32d9db99f1fk0">传入图像</a>。</li></ul></li></ol></div></section><a id="accordion-传入参考视频-type-reference-video"></a><section><p>传入参考视频（type=reference_video）</p><div><p>参考视频URL。视频内容建议包含主体（人物/动物/物体），不建议使用背景或空镜视频。当包含主体时，仅包含一个角色。若视频有声音，也可以参考音色。</p><p>视频限制：</p><ul><li>格式：mp4、mov。</li><li>时长：1～30s。</li><li>分辨率：宽度和高度范围为[240,4096]像素。</li><li>宽高比：1:8～8:1。</li><li>文件大小：不超过100MB。</li></ul><p>支持输入的格式：</p><ol><li><p>公网URL：</p><ul><li>支持HTTP和HTTPS协议。</li><li>示例值：<a href="https://xxx/xxx.mp4"></a><a href="https://xxx/xxx.mp4">https://xxx/xxx.mp4</a>。</li></ul></li><li><p>临时URL：</p><ul><li>支持OSS协议，必须通过<a href="../../more-about-models/get-temporary-file-url.md">上传文件获取临时 URL</a>。</li><li>示例值：oss://dashscope-instant/xxx/xxx.mp4。</li></ul></li></ol></div></section><p><strong>reference_voice</strong> <code>string</code> <strong>（可选）</strong></p><p>音频 URL。用于指定参考素材（图像/视频）中主体角色的音色。与<code>reference_image</code>或<code>reference_video</code>搭配使用。该音频仅参考音色，与说话内容无关。建议参考音频语种与提示词语种保持一致，匹配效果更佳。</p><p>音频生效逻辑：</p><ul><li>默认行为：若 <code>reference_video</code> 本身包含音频，但未指定 <code>reference_voice</code>，默认使用视频原声。</li><li>优先级：若同时传入 <code>reference_video</code>（含音频）和 <code>reference_voice</code>，则优先使用 <code>reference_voice</code> 的音色，覆盖视频原声。</li></ul><p>音频限制：</p><ul><li>格式：wav、mp3。</li><li>时长：1～10s。</li><li>文件大小：不超过15MB。</li></ul><p>支持输入的格式：</p><ol><li><p>公网URL：</p><ul><li>支持HTTP和HTTPS协议。</li><li>示例值：<a href="https://xxx/xxx.mp3"></a><a href="https://xxx/xxx.mp3">https://xxx/xxx.mp3</a>。</li></ul></li><li><p>临时URL：</p><ul><li>支持OSS协议，必须通过<a href="../../more-about-models/get-temporary-file-url.md">上传文件获取临时 URL</a>。</li><li>示例值：oss://dashscope-instant/xxx/xxx.mp3。</li></ul></li></ol></div></section></div></section><p><strong>parameters</strong> <code>object</code> （可选）</p><p>视频处理参数，如设置视频分辨率。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>resolution</strong> <code>string</code> （可选）</p><div><div><p><strong>重要</strong><code>resolution</code>直接影响费用，请在调用前确认<a href="https://bailian.console.aliyun.com/cn-beijing/model/market">百炼控制台</a>。</p></div></div><p>生成视频的分辨率档位，用于控制视频的清晰度（总像素）。</p><ul><li>wan2.7-r2v、wan2.7-r2v-2026-06-12：可选值：720P、1080P。默认值为<code>1080P</code>。</li></ul><p><strong>ratio</strong> <code>string</code> （可选）</p><p>生成视频的宽高比。</p><p>生效逻辑：</p><ul><li>未传入首帧图像：按指定的 <code>ratio</code> 参数生成视频。</li><li>已传入首帧图像：自动忽略 <code>ratio</code> 参数，以首帧图像的宽高比生成近似比例的视频。</li></ul><p>可选值为：</p><ul><li><code>16:9</code>（默认值）</li><li><code>9:16</code></li><li><code>1:1</code></li><li><code>4:3</code></li><li><code>3:4</code></li></ul><p>不同宽高比对应的输出视频分辨率（宽高像素值）见下方表格。</p><p><strong>duration</strong> <code>integer</code> （可选）</p><div><div><p><strong>重要</strong>duration直接影响费用，请在调用前确认<a href="../../../model-user-guide/test-1/model-pricing.md#5c3d28ad8a4x8">模型价格</a>。</p></div></div><p>生成视频的时长，单位为秒。</p><ul><li><p>wan2.7-r2v、wan2.7-r2v-2026-06-12：默认值为5。</p><ul><li>当参考素材中包含视频时：取值为[2, 10]之间的整数。</li><li>当参考素材中不包含视频时：取值为[2, 15]之间的整数。</li></ul></li></ul><p><strong>prompt_extend</strong><code>boolean</code> （可选）</p><p>是否开启prompt智能改写。开启后使用大模型对输入prompt进行智能改写。对于较短的prompt生成效果提升明显，但会增加耗时。</p><ul><li>true：默认值，开启智能改写。</li><li>false：不开启智能改写。</li></ul><p><strong>watermark</strong> <code>boolean</code> （可选）</p><p>是否添加水印标识，水印位于视频右下角，文案固定为“AI生成”。</p><ul><li><code>false</code>：默认值，不添加水印。</li><li><code>true</code>：添加水印。</li></ul><p><strong>seed</strong><code>integer</code>（可选）</p><p>随机数种子，取值范围为<code>[0, 2147483647]</code>。</p><p>未指定时，系统自动生成随机种子。若需提升生成结果的可复现性，建议固定seed值。</p><p>请注意，由于模型生成具有概率性，即使使用相同 seed，也不能保证每次生成结果完全一致。</p></div></section></td><td><a id="sec-tabs-2"></a><section><a id="多主体参考-图像-视频-音色"></a><section><a id="多主体参考-图像-视频-音色-h4"></a><h4>多主体参考（图像+视频+音色）</h4><p>传入多张参考素材（图像+视频），并指定音色生成视频。</p><a id="code-block"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;wan2.7-r2v-2026-06-12&quot;,
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;视频1抱着图3，在图4的椅子上弹奏一支舒缓的乡村民谣，并说道：“今天的阳光真好。”图1手中拿着图2，路过视频1，把手中的图2放到视频1旁边的桌子上，并说道：“真好听，能不能再唱一遍”。 &quot;,
        &quot;media&quot;: [
            {
                &quot;type&quot;: &quot;reference_image&quot;,
                &quot;url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260408/sjuytr/wan-r2v-object-girl.jpg&quot;,
                &quot;reference_voice&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260408/gbqewz/wan-r2v-girl-voice.mp3&quot;
            },
            {
                &quot;type&quot;: &quot;reference_video&quot;,
                &quot;url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qigswt/wan-r2v-role2.mp4&quot;,
                &quot;reference_voice&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260408/isllrq/wan-r2v-boy-voice.mp3&quot;
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
        &quot;resolution&quot;: &quot;720P&quot;,
        &quot;ratio&quot;: &quot;16:9&quot;,
        &quot;duration&quot;: 10,
        &quot;prompt_extend&quot;: false,
        &quot;watermark&quot;: true
    }
}'
</code></pre></section><a id="单图参考-多宫格图像"></a><section><a id="单图参考-多宫格图像-h4"></a><h4>单图参考（多宫格图像）</h4><p>传入一张九宫格参考图，可以控制故事走向、机位构图与角色设定，生成视频。</p><a id="code-block-2"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;wan2.7-r2v-2026-06-12&quot;,
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;参考图片，3D卡通冒险电影风，角色Q版但材质细腻，动作流畅，色彩鲜明，保持角色与森林场景一致，不要加入文字。氛围： 冒险、轻快、神秘、童趣。角色： 小男孩探险家：圆帽、背包、短斗篷。小伙伴：会飞的小机器人，圆形身体，蓝色发光眼。场景： 奇幻森林，巨大树根、蘑菇、藤蔓、藏宝洞口、阳光光束。分镜脚本： 1. 全景：奇幻森林里高大树木与光束交错，环境神秘明亮。 2. 中景：小男孩拨开藤蔓向前探路。 3. 中景：小机器人飞在他身边，用蓝光扫描前方。 4. 特写：一张旧藏宝图在男孩手里展开。 5. 近景：他露出兴奋表情，眼睛亮起来。 6. 动作镜头：两人跳过树根和小溪，继续深入森林。 7. 中景：藤蔓后方露出一个被苔藓覆盖的宝箱。 8. 特写：宝箱边缘闪出金色光芒。 9. 收束镜头：男孩和小机器人站在宝箱前惊喜对望，冒险感拉满。&quot;,
        &quot;media&quot;: [
            {
                &quot;type&quot;: &quot;reference_image&quot;,
                &quot;url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260403/wgjaxy/banana_storyboard_00000020.png&quot;
            }
        ]
    },
    &quot;parameters&quot;: {
        &quot;resolution&quot;: &quot;720P&quot;,
        &quot;duration&quot;: 10,
        &quot;prompt_extend&quot;: false,
        &quot;watermark&quot;: true
    }
}'
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="17bfdb2bdclsh"></a><h4>响应参数</h4><p><strong>output</strong> <code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></td><td><a id="sec-tabs-3"></a><section><a id="成功响应"></a><section><a id="成功响应-h4"></a><h4>成功响应</h4><p>请保存 task_id，用于查询任务状态与结果。</p><a id="code-block-3"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
        &quot;task_status&quot;: &quot;PENDING&quot;,
        &quot;task_id&quot;: &quot;0385dc79-5ff8-4d82-bcb6-xxxxxx&quot;
    },
    &quot;request_id&quot;: &quot;4909100c-7b5a-9f92-bfe5-xxxxxx&quot;
}
</code></pre></section><a id="异常响应"></a><section><a id="异常响应-h4"></a><h4>异常响应</h4><p>创建任务失败，请参见<a href="../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-4"></a><pre class="language-json"><code>{
    &quot;code&quot;: &quot;InvalidApiKey&quot;,
    &quot;message&quot;: &quot;No API-key provided.&quot;,
    &quot;request_id&quot;: &quot;7438d53d-6eb8-4596-8835-xxxxxx&quot;
}
</code></pre></section></section></td></tr></tbody></table>

<a id="步骤2-根据任务id查询结果"></a>

<a id="f0dccc56b7vho"></a>

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

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

> **说明**
>
> -   **轮询建议**：视频生成过程约需数分钟，建议采用**轮询**机制，并设置合理的查询间隔（如 15 秒）来获取结果。
> -   **任务状态流转**：PENDING（排队中）→ RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。
> -   **结果链接**：任务成功后返回视频链接，有效期为 **24 小时**。建议在获取链接后立即下载并转存至永久存储（如[阿里云 OSS](https://help.aliyun.com/zh/oss/user-guide/what-is-oss)）。
> -   **task\_id 有效期**：**24小时**，超时后将无法查询结果，接口将返回任务状态为`UNKNOWN`。
> -   **RPS 限制**：查询接口默认RPS为20。如需更高频查询或事件通知，建议[配置异步任务回调](../../more-about-models/async-task-api.md)。
> -   **更多操作**：如需批量查询、取消任务等操作，请参见[管理异步任务](../../more-about-models/manage-asynchronous-tasks.md)。

<table><tbody><tr><td><a id="adeb821afa3qe"></a><h4>请求参数</h4><a id="10fdb2d3060rn"></a><h5>请求头（Headers）</h5><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><a id="13b97de165qnk"></a><h5>URL路径参数（Path parameters）</h5><p><strong>task_id</strong> <code>string</code><strong>（必选）</strong></p><p>任务ID。</p></td><td><a id="sec-tabs-5"></a><section><a id="查询任务结果"></a><section><a id="查询任务结果-h4"></a><h4>查询任务结果</h4><p>将<code>{task_id}</code>完整替换为上一步接口返回的<code>task_id</code>的值。<code>task_id</code>查询有效期为24小时，并请将<code>{WorkspaceId}</code>替换为真实的<a href="../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain">业务空间ID</a>。</p><a id="code-block-5"></a><pre class="language-bash"><code>curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id} \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="e1ca3ef445nzd"></a><h4>响应参数</h4><p><strong>output</strong><code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code><strong>（必选）</strong></p><p>任务ID。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值-2"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section><p><strong>submit_time</strong> <code>string</code></p><p>任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>scheduled_time</strong> <code>string</code></p><p>任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>end_time</strong> <code>string</code></p><p>任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>video_url</strong><code>string</code></p><p>视频URL。仅在 task_status 为 SUCCEEDED 时返回。</p><p>链接有效期24小时，可通过此URL下载视频。视频格式为MP4（H.264 编码）。</p><p><strong>orig_prompt</strong> <code>string</code></p><p>原始输入的prompt，对应请求参数<code>prompt</code>。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></div></section><p><strong>usage</strong> <code>object</code></p><p>输出信息统计。只对成功的结果计数。</p><a id="accordion-属性-6"></a><section><p>属性</p><div><p><strong>input_video_duration</strong> <code>integer</code></p><p>输入视频的时长，单位秒。</p><p><strong>output_video_duration</strong> <code>integer</code></p><p>输出视频的时长，单位秒。</p><p><strong>duration</strong> <code>integer</code></p><p>总视频时长。计费按duration时长计算。</p><p>计算公式：<code>duration = input_video_duration + output_video_duration</code>。</p><p><strong>SR</strong> <code>integer</code></p><p>生成视频的分辨率档位。示例值：720。</p><p><strong>ratio</strong> <code>string</code></p><p>生成视频的宽高比。示例值：16:9。</p><p><strong>video_count</strong> <code>integer</code></p><p>生成视频的数量。固定为1。</p></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p></td><td><a id="sec-tabs-6"></a><section><a id="任务执行成功"></a><section><a id="任务执行成功-h4"></a><h4>任务执行成功</h4><p>视频URL仅保留24小时，超时后会被自动清除，请及时保存生成的视频。</p><a id="code-block-6"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;52cade0d-905e-9b7d-a01e-xxxxxx&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;18814247-f944-4102-aa4a-xxxxxx&quot;,
        &quot;task_status&quot;: &quot;SUCCEEDED&quot;,
        &quot;submit_time&quot;: &quot;2026-04-02 22:53:19.537&quot;,
        &quot;scheduled_time&quot;: &quot;2026-04-02 22:53:30.427&quot;,
        &quot;end_time&quot;: &quot;2026-04-02 23:00:39.287&quot;,
        &quot;orig_prompt&quot;: &quot;视频2抱着图片3在咖啡厅里弹奏一支舒缓的美式乡村民谣，视频1笑着看着视频2，并缓缓向他走去&quot;,
        &quot;video_url&quot;: &quot;https://dashscope-a717.oss-accelerate.aliyuncs.com/xxx.mp4?xxxx&quot;
    },
    &quot;usage&quot;: {
        &quot;duration&quot;: 15,
        &quot;input_video_duration&quot;: 5,
        &quot;output_video_duration&quot;: 10,
        &quot;video_count&quot;: 1,
        &quot;SR&quot;: 720,
        &quot;ratio&quot;: &quot;16:9&quot;
    }
}
</code></pre></section><a id="任务执行失败"></a><section><a id="任务执行失败-h4"></a><h4>任务执行失败</h4><p>若任务执行失败，task_status将置为 FAILED，并提供错误码和信息。请参见<a href="../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-7"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;e5d70b02-ebd3-98ce-9fe8-759d7d7b107d&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;86ecf553-d340-4e21-af6e-a0c6a421c010&quot;,
        &quot;task_status&quot;: &quot;FAILED&quot;,
        &quot;code&quot;: &quot;InvalidParameter&quot;,
        &quot;message&quot;: &quot;The size is not match xxxxxx&quot;
    }
}
</code></pre></section><a id="任务查询过期"></a><section><a id="任务查询过期-h4"></a><h4>任务查询过期</h4><p>task_id查询有效期为 24 小时，超时后将无法查询，返回以下报错信息。</p><a id="code-block-8"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;a4de7c32-7057-9f82-8581-xxxxxx&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;502a00b1-19d9-4839-a82f-xxxxxx&quot;,
        &quot;task_status&quot;: &quot;UNKNOWN&quot;
    }
}
</code></pre></section></section></td></tr></tbody></table>

<a id="dashscope-sdk调用"></a>

<a id="r2v702a0h2sdk"></a>

## DashScope SDK调用

SDK 的参数命名与[HTTP接口](wan-video-to-video-api-reference.md#7f493e3256ajz)基本一致，参数结构根据语言特性进行封装。

参考生视频任务通常需要1–5分钟。SDK 封装了HTTP异步调用流程，支持同步和异步两种调用方式。

> 实际耗时取决于排队任务数和服务运行状态。

<a id="python-sdk调用"></a>

<a id="549026665ct3b"></a>

### Python SDK调用

> **重要**
>
> 运行以下代码前，请确保 DashScope Python SDK版本 **≥2.0.1**。
>
> 版本过低可能会触发 "url error, please check url!" 等错误。请参考[安装SDK](../../preparations/install-sdk.md)进行更新。

根据模型所在地域设置 **region**（构造 Client 时传入，各地域的region取值不同）:

<a id="sec-tabs-7"></a>

<a id="北京-3"></a>

<a id="北京-3-h4"></a>

#### 北京

`region="cn-beijing"`

<a id="新加坡-3"></a>

<a id="新加坡-3-h4"></a>

#### 新加坡

`region="ap-southeast-1"`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="sec-tabs-8"></a>

<a id="同步调用"></a>

<a id="同步调用-h4"></a>

#### 同步调用

同步调用会阻塞直到视频生成完成，直接返回结果。

<a id="r2v742a0h5rq01"></a>

##### 请求示例

<a id="code-block-9"></a>

```python
import dashscope
import os
from dashscope import DashScopeError

# 以下为华北2（北京）地域的配置。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

def sample_sync_call_r2v():
    # 同步调用，直接返回结果；generate 为一步式调用（提交任务并等待完成），返回已完成的 Job
    print('please wait...')
    try:
        job = client.videos.generate(
            model='wan2.7-r2v-2026-06-12',
            prompt='视频1抱着图3，在图4的椅子上弹奏一支舒缓的乡村民谣，并说道：“今天的阳光真好。”图1手中拿着图2，路过视频1，把手中的图2放到视频1旁边的桌子上，并说道：“真好听，能不能再唱一遍”。 ',
            media=[
                {
                    "type": "reference_image",
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260408/sjuytr/wan-r2v-object-girl.jpg",
                    "reference_voice": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260408/gbqewz/wan-r2v-girl-voice.mp3"
                },
                {
                    "type": "reference_video",
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qigswt/wan-r2v-role2.mp4",
                    "reference_voice": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260408/isllrq/wan-r2v-boy-voice.mp3"
                },
                {
                    "type": "reference_image",
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/rtjeqf/wan-r2v-object3.png"
                },
                {
                    "type": "reference_image",
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qpzxps/wan-r2v-object4.png"
                },
                {
                    "type": "reference_image",
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/wfjikw/wan-r2v-backgroud5.png"
                }
            ],
            resolution='720P',
            ratio='16:9',
            duration=10,
            prompt_extend=False,
            watermark=True)
        print(job)
        print(job.video_url)
    except DashScopeError as e:
        print(f"HTTP返回码：{e.status_code}")
        print(f"错误码：{e.code}")
        print(f"错误信息：{e.message}")
        print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")

if __name__ == '__main__':
    sample_sync_call_r2v()
```

<a id="i2v27pysyncrsph"></a>

##### 响应示例

> video\_url 有效期24小时，请及时下载视频。

<a id="code-block-10"></a>

```json
{
    "request_id": "b040d446-f9b6-977f-b9ad-xxxxxx",
    "task_id": "5dab3291-393e-424d-929b-xxxxxx",
    "status": "SUCCEEDED",
    "video_url": "https://dashscope-a717.oss-accelerate.aliyuncs.com/xxx.mp4?Expires=xxx",
    "task_metrics": {
        "TOTAL": 1,
        "SUCCEEDED": 1,
        "FAILED": 0
    },
    "usage": {
        "video_count": 1,
        "duration": 15,
        "input_video_duration": 5,
        "output_video_duration": 10,
        "SR": 720,
        "ratio": "16:9"
    }
}
```

<a id="异步调用"></a>

<a id="异步调用-h4"></a>

#### 异步调用

异步调用立即返回任务ID，可通过fetch查询状态，或调用wait等待完成（内部自动轮询）。

<a id="r2v751a0h5rq02"></a>

##### 请求示例

<a id="code-block-11"></a>

```python
import dashscope
import os
from dashscope import DashScopeError

# 以下为华北2（北京）地域的配置。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

def sample_async_call_r2v():
    # 异步调用，返回一个task_id
    try:
        job = client.videos.jobs.create(
            model='wan2.7-r2v-2026-06-12',
            prompt='视频1抱着图3，在图4的椅子上弹奏一支舒缓的乡村民谣，并说道：“今天的阳光真好。”图1手中拿着图2，路过视频1，把手中的图2放到视频1旁边的桌子上，并说道：“真好听，能不能再唱一遍”。 ',
            media=[
                {
                    "type": "reference_image",
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260408/sjuytr/wan-r2v-object-girl.jpg",
                    "reference_voice": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260408/gbqewz/wan-r2v-girl-voice.mp3"
                },
                {
                    "type": "reference_video",
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qigswt/wan-r2v-role2.mp4",
                    "reference_voice": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260408/isllrq/wan-r2v-boy-voice.mp3"
                },
                {
                    "type": "reference_image",
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/rtjeqf/wan-r2v-object3.png"
                },
                {
                    "type": "reference_image",
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qpzxps/wan-r2v-object4.png"
                },
                {
                    "type": "reference_image",
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/wfjikw/wan-r2v-backgroud5.png"
                }
            ],
            resolution='720P',
            ratio='16:9',
            duration=10,
            prompt_extend=False,
            watermark=True)
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
    sample_async_call_r2v()
```

<a id="15a0d419b9q5r"></a>

##### 响应示例

1、创建任务的响应示例

<a id="code-block-12"></a>

```json
{
    "request_id": "6dc3bf6c-be18-9268-9c27-xxxxxx",
    "task_id": "686391d9-7ecf-4290-a8e9-xxxxxx",
    "status": "PENDING"
}
```

2、查询任务结果的响应示例

> video\_url 有效期24小时，请及时下载视频。

<a id="code-block-13"></a>

```json
{
    "request_id": "b040d446-f9b6-977f-b9ad-xxxxxx",
    "task_id": "5dab3291-393e-424d-929b-xxxxxx",
    "status": "SUCCEEDED",
    "video_url": "https://dashscope-a717.oss-accelerate.aliyuncs.com/xxx.mp4?Expires=xxx",
    "task_metrics": {
        "TOTAL": 1,
        "SUCCEEDED": 1,
        "FAILED": 0
    },
    "usage": {
        "video_count": 1,
        "duration": 15,
        "input_video_duration": 5,
        "output_video_duration": 10,
        "SR": 720,
        "ratio": "16:9"
    }
}
```

<a id="java-sdk调用"></a>

<a id="3f41c60916y03"></a>

### Java SDK调用

> **重要**
>
> 运行以下代码前，请确保 DashScope Java SDK版本 **≥2.22.14**。
>
> 版本过低可能会触发 "url error, please check url!" 等错误。请参考[安装SDK](../../preparations/install-sdk.md)进行更新。

根据模型所在地域设置 **baseHttpApiUrl**:

<a id="sec-tabs-9"></a>

<a id="北京-4"></a>

<a id="北京-4-h4"></a>

#### 北京

`Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";`

<a id="新加坡-4"></a>

<a id="新加坡-4-h4"></a>

#### 新加坡

`Constants.baseHttpApiUrl = "https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1";`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="sec-tabs-10"></a>

<a id="同步调用-2"></a>

<a id="同步调用-2-h4"></a>

#### 同步调用

同步调用会阻塞直到视频生成完成，直接返回结果。

<a id="r2v836a0h5jr01"></a>

##### 请求示例

<a id="code-block-14"></a>

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

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Ref2Video {

    static {
        // 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
    }

    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey="sk-xxx"
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    public static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    public static void ref2video() throws ApiException, NoApiKeyException, InputRequiredException {
        VideoSynthesis vs = new VideoSynthesis();
        List<VideoSynthesisParam.Media> media = new ArrayList<VideoSynthesisParam.Media>(){{
            add(VideoSynthesisParam.Media.builder()
                    .url("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260408/sjuytr/wan-r2v-object-girl.jpg")
                    .type("reference_image")
                    .referenceVoice("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260408/gbqewz/wan-r2v-girl-voice.mp3")
                    .build());
            add(VideoSynthesisParam.Media.builder()
                    .url("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qigswt/wan-r2v-role2.mp4")
                    .type("reference_video")
                    .referenceVoice("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260408/isllrq/wan-r2v-boy-voice.mp3")
                    .build());
            add(VideoSynthesisParam.Media.builder()
                    .url("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/rtjeqf/wan-r2v-object3.png")
                    .type("reference_image")
                    .build());
            add(VideoSynthesisParam.Media.builder()
                    .url("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qpzxps/wan-r2v-object4.png")
                    .type("reference_image")
                    .build());
            add(VideoSynthesisParam.Media.builder()
                    .url("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/wfjikw/wan-r2v-backgroud5.png")
                    .type("reference_image")
                    .build());
        }};
        Map<String, Object> parameters = new HashMap<>();
        parameters.put("resolution", "720P");
        parameters.put("ratio", "16:9");
        parameters.put("prompt_extend", false);
        parameters.put("watermark", true);

        VideoSynthesisParam param =
                VideoSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("wan2.7-r2v-2026-06-12")
                        .prompt("视频1抱着图3，在图4的椅子上弹奏一支舒缓的乡村民谣，并说道：“今天的阳光真好。”图1手中拿着图2，路过视频1，把手中的图2放到视频1旁边的桌子上，并说道：“真好听，能不能再唱一遍”。 ")
                        .media(media)
                        .duration(10)
                        .parameters(parameters)
                        .build();
        System.out.println("please wait...");
        VideoSynthesisResult result = vs.call(param);
        System.out.println(JsonUtils.toJson(result));
    }

    public static void main(String[] args) {
        try {
            ref2video();
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

<a id="i2v27javasyncrsph"></a>

##### 响应示例

> video\_url 有效期24小时，请及时下载视频。

<a id="code-block-15"></a>

```json
{
    "request_id": "f6365287-336f-9f2b-ab59-xxxxxx",
    "output": {
        "task_id": "cb7f1da5-a987-41de-b0a4-xxxxxx",
        "task_status": "SUCCEEDED",
        "video_url": "https://dashscope-a717.oss-accelerate.aliyuncs.com/xxx.mp4?Expires=xxxx",
        "orig_prompt": "视频1抱着图3，在图4的椅子上弹奏一支舒缓的乡村民谣，并说道：“今天的阳光真好。”图1手中拿着图2，路过视频1，把手中的图2放到视频1旁边的桌子上，并说道：“真好听，能不能再唱一遍”。 ",
        "submit_time": "2026-04-17 17:15:11.536",
        "scheduled_time": "2026-04-17 17:15:20.316",
        "end_time": "2026-04-17 17:29:44.277"
    },
    "usage": {
        "video_count": 1,
        "duration": 15,
        "input_video_duration": 5,
        "output_video_duration": 10,
        "SR": 720
    },
    "status_code": 200,
    "code": "",
    "message": ""
}
```

<a id="异步调用-2"></a>

<a id="异步调用-2-h4"></a>

#### 异步调用

异步调用立即返回任务ID，可通过fetch查询状态，或调用wait等待完成（内部自动轮询）。

<a id="r2v843a0h5jr02"></a>

##### 请求示例

<a id="code-block-16"></a>

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

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Ref2VideoAsync {

    static {
        // 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
    }

    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey="sk-xxx"
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    public static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    public static void asyncRef2video() throws ApiException, NoApiKeyException, InputRequiredException, InterruptedException {
        VideoSynthesis vs = new VideoSynthesis();
        List<VideoSynthesisParam.Media> media = new ArrayList<VideoSynthesisParam.Media>(){{
            add(VideoSynthesisParam.Media.builder()
                    .url("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260408/sjuytr/wan-r2v-object-girl.jpg")
                    .type("reference_image")
                    .referenceVoice("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260408/gbqewz/wan-r2v-girl-voice.mp3")
                    .build());
            add(VideoSynthesisParam.Media.builder()
                    .url("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qigswt/wan-r2v-role2.mp4")
                    .type("reference_video")
                    .referenceVoice("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260408/isllrq/wan-r2v-boy-voice.mp3")
                    .build());
            add(VideoSynthesisParam.Media.builder()
                    .url("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/rtjeqf/wan-r2v-object3.png")
                    .type("reference_image")
                    .build());
            add(VideoSynthesisParam.Media.builder()
                    .url("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qpzxps/wan-r2v-object4.png")
                    .type("reference_image")
                    .build());
            add(VideoSynthesisParam.Media.builder()
                    .url("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/wfjikw/wan-r2v-backgroud5.png")
                    .type("reference_image")
                    .build());
        }};
        Map<String, Object> parameters = new HashMap<>();
        parameters.put("resolution", "720P");
        parameters.put("ratio", "16:9");
        parameters.put("prompt_extend", false);
        parameters.put("watermark", true);

        VideoSynthesisParam param =
                VideoSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("wan2.7-r2v-2026-06-12")
                        .prompt("视频1抱着图3，在图4的椅子上弹奏一支舒缓的乡村民谣，并说道：“今天的阳光真好。”图1手中拿着图2，路过视频1，把手中的图2放到视频1旁边的桌子上，并说道：“真好听，能不能再唱一遍”。 ")
                        .media(media)
                        .duration(10)
                        .parameters(parameters)
                        .build();
        // 提交异步任务
        VideoSynthesisResult result = vs.asyncCall(param);
        System.out.println("task_id: " + result.getOutput().getTaskId());
        System.out.println(JsonUtils.toJson(result));

        // 等待任务完成
        result = vs.wait(result, null);
        System.out.println(JsonUtils.toJson(result));
    }

    public static void main(String[] args) {
        try {
            asyncRef2video();
        } catch (ApiException | NoApiKeyException | InputRequiredException | InterruptedException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

<a id="i2v27javaasyncrsph"></a>

##### 响应示例

1、创建任务的响应示例

<a id="code-block-17"></a>

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

<a id="code-block-18"></a>

```json
{
    "request_id": "f6365287-336f-9f2b-ab59-xxxxxx",
    "output": {
        "task_id": "cb7f1da5-a987-41de-b0a4-xxxxxx",
        "task_status": "SUCCEEDED",
        "video_url": "https://dashscope-a717.oss-accelerate.aliyuncs.com/xxx.mp4?Expires=xxxx",
        "orig_prompt": "视频1抱着图3，在图4的椅子上弹奏一支舒缓的乡村民谣，并说道：“今天的阳光真好。”图1手中拿着图2，路过视频1，把手中的图2放到视频1旁边的桌子上，并说道：“真好听，能不能再唱一遍”。 ",
        "submit_time": "2026-04-17 17:15:11.536",
        "scheduled_time": "2026-04-17 17:15:20.316",
        "end_time": "2026-04-17 17:29:44.277"
    },
    "usage": {
        "video_count": 1,
        "duration": 15,
        "input_video_duration": 5,
        "output_video_duration": 10,
        "SR": 720
    },
    "status_code": 200,
    "code": "",
    "message": ""
}
```

<a id="错误码"></a>

<a id="OajFO"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](../../preparations/error-code.md)进行解决。

<a id="常见问题"></a>

## 常见问题

<a id="从-wan2-6-升级到-wan2-7-代码需要改哪些地方"></a>

#### 从 wan2.6 升级到 wan2.7，代码需要改哪些地方？

主要区别如下：

1.  **提示词的参考引用写法不同**
    
    wan2.7 不再使用 character1、character2 这类标识，需要改为按类型分别指代：图像用“图n”（如图1、图2），视频用“视频n”（如视频1、视频2）。英文提示词则写为“Image 1”、"Video 1”这类标识。提示词说明详见[prompt参数](wan-video-to-video-api-reference.md)。
    
2.  **多镜头控制方式不同**
    -   wan2.7：不支持 shot\_type 参数，通过在 prompt 中描述分镜脚本来实现多镜头效果。
    -   wan2.6：通过设置 shot\_type 为 multi 来生成多镜头视频。
3.  **请求参数结构不同**
    -   参考素材传入方式：wan2.7 使用 `media`（对象数组，每个元素含 `type` 和 `url`），替代 wan2.6 的 `reference_urls`（字符串数组）。
    -   分辨率参数：wan2.7 使用 `resolution`（如 `720P`），替代 wan2.6 的 `size`（如 `1280*720`）。
    -   audio 参数：wan2.7 默认生成有声视频，无需设置。wan2.6 需要显式设置 `audio` 为 `true` 或 `false`。

<a id="如何为主体配音-音色参考"></a>

<a id="a3b4c5d6e7f8g"></a>

#### 如何为主体配音（音色参考）？

仅 **wan2.7** 支持。在 `media` 中通过 `reference_voice` 传入音频 URL，可为参考图像或参考视频指定参考音色。

<a id="code-block-19"></a>

```json
{
    "media": [
        {
            "type": "reference_image",
            "url": "<参考图像URL>",
            "reference_voice": "<音频URL>"
        },
        {
            "type": "reference_video",
            "url": "<参考视频URL>",
            "reference_voice": "<音频URL>"
        }
    ]
}
```
