# 万相-文生视频API参考（2.1-2.6）

万相-文生视频模型基于 文本提示词 ，生成一段流畅的视频。

**相关文档**：[使用指南](text-to-video-guide-99fbc872809463c8.md)

<a id="适用范围"></a>

<a id="1fd78afa5brlj"></a>

## 适用范围

为确保调用成功，请务必保证**模型、Endpoint URL 和 API Key 均属于同一地域**。跨地域调用将会失败。

-   [**选择模型**](text-to-video-guide-99fbc872809463c8.md#06f39eafa2dwt)：确认模型所属的地域。
-   **选择 URL**：选择对应的地域 Endpoint URL，支持HTTP URL或 DashScope SDK URL。
-   **配置 API Key**：选择地域并[获取与配置 API Key](../model-api-reference/preparations/get-api-key.md)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
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

## HTTP调用

> **重要**
>
> 此接口为**旧版协议**，支持**wan2.6及早期系列模型（wan2.5/wan2.2/wanx2.1）**。

由于文生视频任务耗时较长（通常为1-5分钟），API采用异步调用。整个流程包含 **“创建任务 -> 轮询获取”** 两个核心步骤，具体如下：

<a id="步骤1-创建任务获取任务id"></a>

<a id="81185ac18blmj"></a>

### 步骤1：创建任务获取任务ID

<a id="sec-tabs"></a>

<a id="北京"></a>

<a id="北京-h4"></a>

#### 北京

`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="新加坡"></a>

<a id="新加坡-h4"></a>

#### 新加坡

`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

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

<table><tbody><tr><td><a id="afcd41d2b57zf"></a><h4>请求参数</h4><a id="79473e45c592d"></a><h5>请求头（Headers）</h5><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><p><strong>X-DashScope-Async</strong><code>string</code><strong>（必选）</strong></p><p>异步处理配置参数。HTTP请求只支持异步，<strong>必须设置为</strong><code>enable</code>。</p><div><div><p><strong>重要</strong>缺少此请求头将报错：“current user api does not support synchronous calls”。</p></div></div><a id="66a778d4fbfub"></a><h5>请求体（Request Body）</h5><p><strong>model</strong> <code>string</code> <strong>（必选）</strong></p><p>模型名称。可选模型请参见<a href="../model-user-guide/test-1/model-pricing.md#ba6f7744d5e0o">模型列表</a>。</p><p>示例值：wan2.6-t2v。</p><p><strong>input</strong> <code>object</code> <strong>（必选）</strong></p><p>输入的基本信息，如提示词等。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>prompt</strong> <code>string</code> <strong>（必选）</strong></p><p>文本提示词。用来描述生成视频中期望包含的元素和视觉特点。</p><p>支持中英文，每个汉字/字母占一个字符，超过部分会自动截断。长度限制因模型版本而异：</p><ul><li>wan2.6和wan2.5系列模型：不超过1500个字符。</li><li>wan2.2 和wanx2.1系列模型：不超过800个字符。</li></ul><p>示例值：一只小猫在月光下奔跑。</p><p>提示词的使用技巧请参见<a href="../model-user-guide/use-cases/text-to-video-prompt.md">文生视频/图生视频Prompt指南</a>。</p><p><strong>negative_prompt</strong> <code>string</code> （可选）</p><p>反向提示词，用来描述不希望在视频画面中看到的内容，可以对视频画面进行限制。</p><p>支持中英文，长度不超过500个字符，超过部分会自动截断。</p><p>示例值：低分辨率、错误、最差质量、低质量、残缺、多余的手指、比例不良等。</p><p><strong>audio_url</strong> <code>string</code> （可选）</p><strong>支持模型：wan2.6和wan2.5系列模型。</strong><p>音频文件URL，模型将使用该音频生成视频。</p><p>支持输入的格式：</p><ol><li><p>公网URL：</p><ul><li>支持 HTTP 和 HTTPS 协议。</li><li>示例值：<a href="https://help-static-aliyun-doc.aliyuncs.com/xxx.mp3"></a><a href="https://help-static-aliyun-doc.aliyuncs.com/xxx.mp3">https://help-static-aliyun-doc.aliyuncs.com/xxx.mp3</a>。</li></ul></li><li><p>临时URL：</p><ul><li>支持OSS协议，必须通过<a href="../model-api-reference/more-about-models/get-temporary-file-url.md">上传文件获取临时 URL</a>。</li><li>示例值：oss://dashscope-instant/xxx/xxx.mp3。</li></ul></li></ol><p>音频限制：</p><ul><li>格式：wav、mp3。</li><li>时长：3～30s。</li><li>文件大小：不超过15MB。</li><li>超限处理：若音频长度超过 <code>duration</code> 值（ 如5秒），自动截取前5秒，其余部分丢弃。若音频长度不足视频时长，超出音频长度部分为无声视频。例如，音频为3秒，视频时长为5秒，输出视频前3秒有声，后2秒无声。</li></ul></div></section><p><strong>parameters</strong> <code>object</code> （可选）</p><p>图像处理参数。如设置视频分辨率、开启prompt智能改写、添加水印等。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>size</strong> <code>string</code> （可选）</p><div><div><p><strong>重要</strong></p><ul><li>size直接影响费用，请在调用前确认<a href="../model-user-guide/test-1/model-pricing.md#ba6f7744d5e0o">模型价格</a>。</li><li>size必须设置为具体数值（如 <code>1280*720</code>），而不是 1:1或480P。</li></ul></div></div><p>指定生成的视频分辨率，格式为<code>宽*高</code>。该参数的默认值和可用枚举值依赖于 model 参数，规则如下：</p><ul><li><strong>wan2.6-t2v</strong>：默认值为 <code>1920*1080</code>（1080P）。可选分辨率：720P、1080P对应的所有分辨率。</li><li><strong>wan2.5-t2v-preview</strong>：默认值为 <code>1920*1080</code>（1080P）。可选分辨率：480P、720P、1080P对应的所有分辨率。</li><li><strong>wan2.2-t2v-plus</strong>：默认值为 <code>1920*1080</code>（1080P）。可选分辨率：480P、1080P对应的所有分辨率。</li><li><strong>wanx2.1-t2v-turbo</strong> ：默认值为 <code>1280*720</code>（720P）。可选分辨率：480P、720P 对应的所有分辨率。</li><li><strong>wanx2.1-t2v-plus</strong>：默认值为<code>1280*720</code>（720P）。可选分辨率：720P 对应的所有分辨率。</li></ul><p>480P档位：可选的视频分辨率及其对应的视频宽高比为：</p><ul><li><code>832*480</code>：16:9。</li><li><code>480*832</code>：9:16。</li><li><code>624*624</code>：1:1。</li></ul><p>720P档位：可选的视频分辨率及其对应的视频宽高比为：</p><ul><li><code>1280*720</code>：16:9。</li><li><code>720*1280</code>：9:16。</li><li><code>960*960</code>：1:1。</li><li><code>1088*832</code>：4:3。</li><li><code>832*1088</code>：3:4。</li></ul><p>1080P档位：可选的视频分辨率及其对应的视频宽高比为：</p><ul><li><code>1920*1080</code>： 16:9。</li><li><code>1080*1920</code>： 9:16。</li><li><code>1440*1440</code>： 1:1。</li><li><code>1632*1248</code>： 4:3。</li><li><code>1248*1632</code>： 3:4。</li></ul><p><strong>duration</strong> <code>integer</code> （可选）</p><div><div><p><strong>重要</strong>duration直接影响费用。费用 = 单价（基于分辨率）× 时长（秒），请在调用前确认<a href="../model-user-guide/test-1/model-pricing.md#ba6f7744d5e0o">模型价格</a>。</p></div></div><p>生成视频的时长，单位为秒。该参数的取值依赖于 model参数：</p><ul><li>wan2.6-t2v：取值为[2, 15]之间的整数。默认值为5。</li><li>wan2.5-t2v-preview：可选值为5、10。默认值为5。</li><li>wan2.2-t2v-plus：固定为5秒，且不支持修改。</li><li>wanx2.1-t2v-plus：固定为5秒，且不支持修改。</li><li>wanx2.1-t2v-turbo：固定为5秒，且不支持修改。</li></ul><p><strong>prompt_extend</strong><code>boolean</code> （可选）</p><p>是否开启prompt智能改写。开启后使用大模型对输入prompt进行智能改写。对于较短的prompt生成效果提升明显，但会增加耗时。</p><ul><li><code>true</code>：默认值，开启智能改写。</li><li><code>false</code>：不开启智能改写。</li></ul><p><strong>shot_type</strong> <code>string</code> （可选）</p><strong>支持模型：wan2.6模型。</strong><p>指定生成视频的镜头类型，即视频是由一个连续镜头还是多个切换镜头组成。</p><p>可选值：</p><ul><li><code>single</code>：默认值，输出单镜头视频。</li><li><code>multi</code>：输出多镜头视频。</li></ul><p>生效条件：仅当<code>&quot;prompt_extend&quot;: true</code> 时生效。</p><p>参数优先级：<code>shot_type &gt; prompt</code>。例如，若 shot_type设置为&quot;single&quot;，即使 prompt 中包含“生成多镜头视频”，模型仍会输出单镜头视频。</p><p><strong>watermark</strong> <code>boolean</code> （可选）</p><p>是否添加水印标识，水印位于视频右下角，文案固定为“AI生成”。</p><ul><li><code>false</code>：默认值，不添加水印。</li><li><code>true</code>：添加水印。</li></ul><p><strong>seed</strong><code>integer</code>（可选）</p><p>随机数种子，取值范围为<code>[0, 2147483647]</code>。</p><p>未指定时，系统自动生成随机种子。若需提升生成结果的可复现性，建议固定seed值。</p><p>请注意，由于模型生成具有概率性，即使使用相同 seed，也不能保证每次生成结果完全一致。</p></div></section></td><td><a id="sec-tabs-2"></a><section><a id="多镜头叙事"></a><section><a id="多镜头叙事-h4"></a><h4>多镜头叙事</h4><ul><li><code>shot_type</code>: 多镜头必须设为 <code>&quot;multi&quot;</code>。</li><li><code>prompt_extend</code>: 多镜头必须设为 <code>true</code>（开启智能改写以优化分镜描述）。</li></ul><a id="code-block"></a><pre class="language-bash"><code>
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;wan2.6-t2v&quot;,
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;一幅史诗级可爱的场景。一只小巧可爱的卡通小猫将军，身穿细节精致的金色盔甲，头戴一个稍大的头盔，勇敢地站在悬崖上。他骑着一匹虽小但英勇的战马，说：”青海长云暗雪山，孤城遥望玉门关。黄沙百战穿金甲，不破楼兰终不还。“。悬崖下方，一支由老鼠组成的、数量庞大、无穷无尽的军队正带着临时制作的武器向前冲锋。这是一个戏剧性的、大规模的战斗场景，灵感来自中国古代的战争史诗。远处的雪山上空，天空乌云密布。整体氛围是“可爱”与“霸气”的搞笑和史诗般的融合。&quot;,
        &quot;audio_url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250923/hbiayh/%E4%BB%8E%E5%86%9B%E8%A1%8C.mp3&quot;
    },
    &quot;parameters&quot;: {
        &quot;size&quot;: &quot;1280*720&quot;,
        &quot;prompt_extend&quot;: true,
        &quot;duration&quot;: 10,
        &quot;shot_type&quot;:&quot;multi&quot;
    }
}'
</code></pre></section><a id="传入音频文件"></a><section><a id="传入音频文件-h4"></a><h4>传入音频文件</h4><p>支持模型：wan2.6/wan2.5系列模型。</p><p>可通过 <code>input.audio_url</code> 参数传入自定义音频的 URL。</p><a id="code-block-2"></a><pre class="language-bash"><code>
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;wan2.5-t2v-preview&quot;,
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;一幅史诗级可爱的场景。一只小巧可爱的卡通小猫将军，身穿细节精致的金色盔甲，头戴一个稍大的头盔，勇敢地站在悬崖上。他骑着一匹虽小但英勇的战马，说：”青海长云暗雪山，孤城遥望玉门关。黄沙百战穿金甲，不破楼兰终不还。“。悬崖下方，一支由老鼠组成的、数量庞大、无穷无尽的军队正带着临时制作的武器向前冲锋。这是一个戏剧性的、大规模的战斗场景，灵感来自中国古代的战争史诗。远处的雪山上空，天空乌云密布。整体氛围是“可爱”与“霸气”的搞笑和史诗般的融合。&quot;,
        &quot;audio_url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250923/hbiayh/%E4%BB%8E%E5%86%9B%E8%A1%8C.mp3&quot;
    },
    &quot;parameters&quot;: {
        &quot;size&quot;: &quot;832*480&quot;,
        &quot;prompt_extend&quot;: true,
        &quot;duration&quot;: 10
    }
}'
</code></pre></section><a id="自动配音"></a><section><a id="自动配音-h4"></a><h4>自动配音</h4><p>支持模型wan2.6/wan2.5系列模型。</p><p>若不提供 <code>input.audio_url</code> ，模型将根据视频内容自动生成匹配的背景音乐或音效。</p><a id="code-block-3"></a><pre class="language-bash"><code>
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;wan2.5-t2v-preview&quot;,
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;一幅史诗级可爱的场景。一只小巧可爱的卡通小猫将军，身穿细节精致的金色盔甲，头戴一个稍大的头盔，勇敢地站在悬崖上。他骑着一匹虽小但英勇的战马，说：”青海长云暗雪山，孤城遥望玉门关。黄沙百战穿金甲，不破楼兰终不还。“。悬崖下方，一支由老鼠组成的、数量庞大、无穷无尽的军队正带着临时制作的武器向前冲锋。这是一个戏剧性的、大规模的战斗场景，灵感来自中国古代的战争史诗。远处的雪山上空，天空乌云密布。整体氛围是“可爱”与“霸气”的搞笑和史诗般的融合。&quot;
    },
    &quot;parameters&quot;: {
        &quot;size&quot;: &quot;832*480&quot;,
        &quot;prompt_extend&quot;: true,
        &quot;duration&quot;: 10
    }
}'
</code></pre></section><a id="生成无声视频"></a><section><a id="生成无声视频-h4"></a><h4>生成无声视频</h4><p>仅wan2.2 和wanx2.1系列模型支持生成无声视频。默认生成无声视频，无需设置。</p><blockquote><p>wan2.6 及wan2.5系列模型默认生成有声视频。</p></blockquote><a id="code-block-4"></a><pre class="language-bash"><code>
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;wan2.2-t2v-plus&quot;,
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;低对比度，在一个复古的70年代风格地铁站里，街头音乐家在昏暗的色彩和粗糙的质感中演奏。他穿着旧式夹克，手持吉他，专注地弹奏。通勤者匆匆走过，一小群人渐渐聚拢聆听。镜头慢慢向右移动，捕捉到乐器声与城市喧嚣交织的场景，背景中有老式的地铁标志和斑驳的墙面。&quot;
    },
    &quot;parameters&quot;: {
        &quot;size&quot;: &quot;832*480&quot;,
        &quot;prompt_extend&quot;: true
    }
}'
</code></pre></section><a id="使用反向提示词"></a><section><a id="使用反向提示词-h4"></a><h4>使用反向提示词</h4><p>支持模型：所有模型。</p><p>通过 negative_prompt 排除“花朵”元素，避免其出现在视频画面中。</p><a id="code-block-5"></a><pre class="language-bash"><code>
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;wan2.2-t2v-plus&quot;,
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;一只小猫在月光下奔跑&quot;,
        &quot;negative_prompt&quot;: &quot;花朵&quot;
    },
    &quot;parameters&quot;: {
        &quot;size&quot;: &quot;832*480&quot;
    }
}'
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="cd3063363egdc"></a><h4>响应参数</h4><p><strong>output</strong> <code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../model-api-reference/preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../model-api-reference/preparations/error-code.md">错误码</a>。</p></td><td><a id="sec-tabs-3"></a><section><a id="成功响应"></a><section><a id="成功响应-h4"></a><h4>成功响应</h4><p>请保存 task_id，用于查询任务状态与结果。</p><a id="code-block-6"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
        &quot;task_status&quot;: &quot;PENDING&quot;,
        &quot;task_id&quot;: &quot;0385dc79-5ff8-4d82-bcb6-xxxxxx&quot;
    },
    &quot;request_id&quot;: &quot;4909100c-7b5a-9f92-bfe5-xxxxxx&quot;
}
</code></pre></section><a id="异常响应"></a><section><a id="异常响应-h4"></a><h4>异常响应</h4><p>创建任务失败，请参见<a href="../model-api-reference/preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-7"></a><pre class="language-json"><code>{
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

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="新加坡-2"></a>

<a id="新加坡-2-h4"></a>

#### 新加坡

`GET https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/tasks/{task_id}`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

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

<table><tbody><tr><td><a id="a9e0408c70ylw"></a><h4>请求参数</h4><a id="2d2fb41da6idy"></a><h5>请求头（Headers）</h5><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><a id="031d8a0fafqhp"></a><h5>URL路径参数（Path parameters）</h5><p><strong>task_id</strong> <code>string</code><strong>（必选）</strong></p><p>任务ID。</p></td><td><a id="sec-tabs-5"></a><section><a id="查询任务结果"></a><section><a id="查询任务结果-h4"></a><h4>查询任务结果</h4><p>将<code>{task_id}</code>完整替换为上一步接口返回的<code>task_id</code>的值。<code>task_id</code>查询有效期为24小时，并请将<code>{WorkspaceId}</code>替换为真实的<a href="../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain">业务空间ID</a>。</p><a id="code-block-8"></a><pre class="language-bash"><code>curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id} \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="810682d979i8q"></a><h4>响应参数</h4><p><strong>output</strong><code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值-2"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section><strong>轮询过程中的状态流转：</strong><ul><li>PENDING（排队中） → RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。</li><li>初次查询状态通常为 PENDING（排队中）或 RUNNING（处理中）。</li><li>当状态变为 SUCCEEDED 时，响应中将包含生成的视频URL。</li><li>若状态为 FAILED，请检查错误信息并重试。</li><li>若状态为 CANCELED，表示任务已取消，如需继续请重新提交任务。</li><li>若状态为 UNKNOWN，表示任务不存在或状态未知，可能在 task_id 不存在或超过 24 小时有效期后出现。</li></ul><p><strong>submit_time</strong> <code>string</code></p><p>任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>scheduled_time</strong> <code>string</code></p><p>任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>end_time</strong> <code>string</code></p><p>任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>video_url</strong><code>string</code></p><p>视频URL。仅在 task_status 为 SUCCEEDED 时返回。</p><p>链接有效期24小时，可通过此URL下载视频。视频格式为MP4（H.264 编码）。</p><p><strong>orig_prompt</strong> <code>string</code></p><p>原始输入的prompt，对应请求参数<code>prompt</code>。</p><p><strong>actual_prompt</strong> <code>string</code></p><p>当 <code>prompt_extend=true</code> 时，系统会对输入 prompt 进行智能改写，此字段返回实际用于生成的优化后 prompt。</p><ul><li>若 <code>prompt_extend=false</code>，该字段不会返回。</li><li>注意：wan2.6 模型无论 <code>prompt_extend</code> 取值如何，均不返回此字段。</li></ul><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../model-api-reference/preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../model-api-reference/preparations/error-code.md">错误码</a>。</p></div></section><p><strong>usage</strong> <code>object</code></p><p>输出信息统计。只对成功的结果计数。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>video_duration</strong> <code>integer</code></p><p>仅在使用 wan2.5 及以下版本模型时返回，用于计费。</p><p>生成视频的时长，单位秒。枚举值为5、10。</p><p><strong>duration</strong> <code>float</code></p><p>仅在使用 wan2.6 模型时返回，用于计费。</p><p>表示总的视频时长，且<code>duration=input_video_duration+output_video_duration</code>。</p><p><strong>input_video_duration</strong> <code>integer</code></p><p>仅在使用 wan2.6 模型时返回。固定为0。</p><p><strong>output_video_duration</strong> <code>integer</code></p><p>仅在使用 wan2.6 模型时返回。</p><p>输出视频的时长，单位秒。其值等同于<code>input.duration</code>的值。</p><p><strong>SR</strong> <code>integer</code></p><p>仅在使用 wan2.6 模型时返回。生成视频的分辨率档位。示例值：720。</p><p><strong>size</strong> <code>string</code></p><p>仅在使用 wan2.6 模型时返回。生成视频的分辨率。格式为“宽<em>高</em>”<em>，示例值：1920</em>1080。</p><p><strong>video_ratio</strong> <code>string</code></p><p>仅 wan2.5 及以下版本模型时返回。生成视频的分辨率。格式为“宽<em>高</em>”<em>，示例值：832</em>480。</p><p><strong>video_count</strong> <code>integer</code></p><p>生成视频的数量。固定为1。</p></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p></td><td><a id="sec-tabs-6"></a><section><a id="任务执行成功"></a><section><a id="任务执行成功-h4"></a><h4>任务执行成功</h4><p>视频URL仅保留24小时，超时后会被自动清除，请及时保存生成的视频。</p><a id="code-block-9"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;caa62a12-8841-41a6-8af2-xxxxxx&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;eff1443c-ccab-4676-aad3-xxxxxx&quot;,
        &quot;task_status&quot;: &quot;SUCCEEDED&quot;,
        &quot;submit_time&quot;: &quot;2025-09-29 14:18:52.331&quot;,
        &quot;scheduled_time&quot;: &quot;2025-09-29 14:18:59.290&quot;,
        &quot;end_time&quot;: &quot;2025-09-29 14:23:39.407&quot;,
        &quot;orig_prompt&quot;: &quot;一幅史诗级可爱的场景。一只小巧可爱的卡通小猫将军，身穿细节精致的金色盔甲，头戴一个稍大的头盔，勇敢地站在悬崖上。他骑着一匹虽小但英勇的战马，说：”青海长云暗雪山，孤城遥望玉门关。黄沙百战穿金甲，不破楼兰终不还。“。悬崖下方，一支由老鼠组成的、数量庞大、无穷无尽的军队正带着临时制作的武器向前冲锋。这是一个戏剧性的、大规模的战斗场景，灵感来自中国古代的战争史诗。远处的雪山上空，天空乌云密布。整体氛围是“可爱”与“霸气”的搞笑和史诗般的融合。&quot;,
        &quot;video_url&quot;: &quot;https://dashscope-result-sh.oss-accelerate.aliyuncs.com/xxx.mp4?Expires=xxx&quot;
    },
    &quot;usage&quot;: {
        &quot;duration&quot;: 10,
        &quot;size&quot;: &quot;1280*720&quot;,
        &quot;input_video_duration&quot;: 0,
        &quot;output_video_duration&quot;: 10,
        &quot;video_count&quot;: 1,
        &quot;SR&quot;: 720
    }
}
</code></pre></section><a id="任务执行失败"></a><section><a id="任务执行失败-h4"></a><h4>任务执行失败</h4><p>若任务执行失败，task_status将置为 FAILED，并提供错误码和信息。请参见<a href="../model-api-reference/preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-10"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;e5d70b02-ebd3-98ce-9fe8-759d7d7b107d&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;86ecf553-d340-4e21-af6e-a0c6a421c010&quot;,
        &quot;task_status&quot;: &quot;FAILED&quot;,
        &quot;code&quot;: &quot;InvalidParameter&quot;,
        &quot;message&quot;: &quot;The size is not match xxxxxx&quot;
    }
}
</code></pre></section><a id="任务查询过期"></a><section><a id="任务查询过期-h4"></a><h4>任务查询过期</h4><p>task_id查询有效期为 24 小时，超时后将无法查询，返回以下报错信息。</p><a id="code-block-11"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;a4de7c32-7057-9f82-8581-xxxxxx&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;502a00b1-19d9-4839-a82f-xxxxxx&quot;,
        &quot;task_status&quot;: &quot;UNKNOWN&quot;
    }
}
</code></pre></section></section></td></tr></tbody></table>

<a id="dashscope-sdk调用"></a>

<a id="db17b3098c2iv"></a>

## DashScope SDK调用

SDK 的参数命名与HTTP接口基本一致，参数结构根据语言特性进行封装。

由于文生视频任务耗时较长（通常为1-5分钟），SDK 在底层封装了 HTTP 异步调用流程，支持同步、异步两种调用方式。

> 具体耗时受限于排队任务数和服务执行情况，请在获取结果时耐心等待。

<a id="python-sdk调用"></a>

<a id="t2v26pyh426"></a>

### Python SDK调用

> **重要**
>
> 请确保 DashScope Python SDK 版本**不低于**`2.0.1`，再运行以下代码。
>
> 若版本过低，可能会触发 "url error, please check url!" 等错误。请参考[安装SDK](../model-api-reference/preparations/install-sdk.md)进行更新。

根据模型所在地域设置 `region`（构造 Client 时传入，各地域的region取值不同）:

<a id="sec-tabs-7"></a>

<a id="北京-3"></a>

<a id="北京-3-h4"></a>

#### 北京

`region="cn-beijing"`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="新加坡-3"></a>

<a id="新加坡-3-h4"></a>

#### 新加坡

`region="ap-southeast-1"`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="弗吉尼亚-3"></a>

<a id="弗吉尼亚-3-h4"></a>

#### 弗吉尼亚

`region="us-east-1"`

<a id="法兰克福-3"></a>

<a id="法兰克福-3-h4"></a>

#### 法兰克福

`region="eu-central-1"`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="sec-tabs-8"></a>

<a id="同步调用"></a>

<a id="同步调用-h4"></a>

#### 同步调用

<a id="3cd4969b00193"></a>

##### 请求示例

<a id="code-block-12"></a>

```python
import dashscope
from dashscope import DashScopeError
import os

# 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

def sample_sync_call_t2v():
    # generate 为一步式调用（提交任务并等待完成），返回已完成的 Job
    print('please wait...')
    # audio_url / negative_prompt 为 input 段字段，不在具名签名内，经 extra_input 透传
    try:
        job = client.videos.generate(model='wan2.6-t2v',
                                     prompt='一幅史诗级可爱的场景。一只小巧可爱的卡通小猫将军，身穿细节精致的金色盔甲，头戴一个稍大的头盔，勇敢地站在悬崖上。他骑着一匹虽小但英勇的战马，说：”青海长云暗雪山，孤城遥望玉门关。黄沙百战穿金甲，不破楼兰终不还。“。悬崖下方，一支由老鼠组成的、数量庞大、无穷无尽的军队正带着临时制作的武器向前冲锋。这是一个戏剧性的、大规模的战斗场景，灵感来自中国古代的战争史诗。远处的雪山上空，天空乌云密布。整体氛围是“可爱”与“霸气”的搞笑和史诗般的融合。',
                                     extra_input={'audio_url': 'https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250923/hbiayh/%E4%BB%8E%E5%86%9B%E8%A1%8C.mp3',
                                                  'negative_prompt': ""},
                                     size='1280*720',
                                     duration=10,
                                     prompt_extend=True,
                                     watermark=False,
                                     seed=12345)
        print(job)
        print(job.video_url)
    except DashScopeError as e:
        print(f"HTTP返回码：{e.status_code}")
        print(f"错误码：{e.code}")
        print(f"错误信息：{e.message}")
        print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")

if __name__ == '__main__':
    sample_sync_call_t2v()
```

<a id="0c0533477emwb"></a>

##### 响应示例

> video\_url 有效期24小时，请及时下载视频。

<a id="code-block-13"></a>

```json
{
    "request_id": "167f3beb-3dd0-47fe-a83c-xxxxxx",
    "task_id": "5b65411f-d946-4e29-859e-xxxxxx",
    "status": "SUCCEEDED",
    "video_url": "https://dashscope-result-bj.oss-accelerate.aliyuncs.com/xxx.mp4?Expires=xxx",
    "task_metrics": {
        "TOTAL": 1,
        "SUCCEEDED": 1,
        "FAILED": 0
    },
    "usage": {
        "video_count": 1,
        "duration": 10,
        "size": "1280*720",
        "input_video_duration": 0,
        "output_video_duration": 10,
        "SR": 720
    }
}
```

<a id="异步调用"></a>

<a id="异步调用-h4"></a>

#### 异步调用

<a id="b994ca9918t7e"></a>

##### 请求示例

<a id="code-block-14"></a>

```python
import dashscope
from dashscope import DashScopeError
import os

# 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

def sample_async_call_t2v():
    # call async api, will return the task information
    # you can get task status with the returned task id.
    # audio_url / negative_prompt 为 input 段字段，不在具名签名内，经 extra_input 透传
    try:
        job = client.videos.jobs.create(model='wan2.6-t2v',
                                        prompt='一幅史诗级可爱的场景。一只小巧可爱的卡通小猫将军，身穿细节精致的金色盔甲，头戴一个稍大的头盔，勇敢地站在悬崖上。他骑着一匹虽小但英勇的战马，说：”青海长云暗雪山，孤城遥望玉门关。黄沙百战穿金甲，不破楼兰终不还。“。悬崖下方，一支由老鼠组成的、数量庞大、无穷无尽的军队正带着临时制作的武器向前冲锋。这是一个戏剧性的、大规模的战斗场景，灵感来自中国古代的战争史诗。远处的雪山上空，天空乌云密布。整体氛围是“可爱”与“霸气”的搞笑和史诗般的融合。',
                                        extra_input={'audio_url': 'https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250923/hbiayh/%E4%BB%8E%E5%86%9B%E8%A1%8C.mp3',
                                                     'negative_prompt': ""},
                                        size='1280*720',
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

    # get the task information include the task status.
    try:
        snapshot = client.videos.jobs.fetch(job.task_id)
        print(snapshot.status)  # check the task status
    except DashScopeError as e:
        print(f"HTTP返回码：{e.status_code}")
        print(f"错误码：{e.code}")
        print(f"错误信息：{e.message}")
        print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")

    # wait the task complete, will call fetch interval, and check it's in finished status.
    # （2.0 jobs.wait 指数退避轮询，默认总预算24小时，任务 FAILED 会抛出异常）
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
    sample_async_call_t2v()
```

<a id="ae28dc8f72g6i"></a>

##### 响应示例

1、创建任务的响应示例

<a id="code-block-15"></a>

```json
{
    "request_id": "c86ff7ba-8377-917a-90ed-xxxxxx",
    "task_id": "721164c6-8619-4a35-a6d9-xxxxxx",
    "status": "PENDING"
}
```

2、查询任务结果的响应示例

> video\_url 有效期24小时，请及时下载视频。

<a id="code-block-16"></a>

```text
{
    "request_id": "167f3beb-3dd0-47fe-a83c-xxxxxx",
    "task_id": "5b65411f-d946-4e29-859e-xxxxxx",
    "status": "SUCCEEDED",
    "video_url": "https://dashscope-result-bj.oss-accelerate.aliyuncs.com/xxx.mp4?Expires=xxx",
    "task_metrics": {
        "TOTAL": 1,
        "SUCCEEDED": 1,
        "FAILED": 0
    },
    "usage": {
        "video_count": 1,
        "duration": 10,
        "size": "1280*720",
        "input_video_duration": 0,
        "output_video_duration": 10,
        "SR": 720
    }
}
```

<a id="java-sdk调用"></a>

<a id="38800f946d43r"></a>

### Java SDK调用

> **重要**
>
> 请确保 DashScope Java SDK 版本**不低于**`2.22.14`，再运行以下代码。
>
> 若版本过低，可能会触发 "url error, please check url!" 等错误。请参考[安装SDK](../model-api-reference/preparations/install-sdk.md)进行更新。

根据模型所在地域设置 `Constants.baseHttpApiUrl`:

<a id="sec-tabs-9"></a>

<a id="北京-4"></a>

<a id="北京-4-h4"></a>

#### 北京

`Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="新加坡-4"></a>

<a id="新加坡-4-h4"></a>

#### 新加坡

`Constants.baseHttpApiUrl = "https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1";`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="弗吉尼亚-4"></a>

<a id="弗吉尼亚-4-h4"></a>

#### 弗吉尼亚

`Constants.baseHttpApiUrl = "https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v1";`

<a id="法兰克福-4"></a>

<a id="法兰克福-4-h4"></a>

#### 法兰克福

`Constants.baseHttpApiUrl = "https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/api/v1";`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="sec-tabs-10"></a>

<a id="同步调用-2"></a>

<a id="同步调用-2-h4"></a>

#### 同步调用

<a id="3e3609efb9rhl"></a>

##### 请求示例

<a id="code-block-17"></a>

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
import java.util.HashMap;
import java.util.Map;

public class Text2Video {

    static {
        // 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。获取URL：https://help.aliyun.com/zh/model-studio/text-to-video-api-reference
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
    }

    // 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    public static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    /**
     * Create a video compositing task and wait for the task to complete.
     */
    public static void text2Video() throws ApiException, NoApiKeyException, InputRequiredException {
        VideoSynthesis vs = new VideoSynthesis();
        Map<String, Object> parameters = new HashMap<>();
        parameters.put("prompt_extend", true);
        parameters.put("watermark", false);
        parameters.put("seed", 12345);

        VideoSynthesisParam param =
                VideoSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("wan2.6-t2v")
                        .prompt("一幅史诗级可爱的场景。一只小巧可爱的卡通小猫将军，身穿细节精致的金色盔甲，头戴一个稍大的头盔，勇敢地站在悬崖上。他骑着一匹虽小但英勇的战马，说：”青海长云暗雪山，孤城遥望玉门关。黄沙百战穿金甲，不破楼兰终不还。“。悬崖下方，一支由老鼠组成的、数量庞大、无穷无尽的军队正带着临时制作的武器向前冲锋。这是一个戏剧性的、大规模的战斗场景，灵感来自中国古代的战争史诗。远处的雪山上空，天空乌云密布。整体氛围是“可爱”与“霸气”的搞笑和史诗般的融合。")
                        .audioUrl("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250923/hbiayh/%E4%BB%8E%E5%86%9B%E8%A1%8C.mp3")
                        .negativePrompt("")
                        .size("1280*720")
                        .duration(10)
                        .parameters(parameters)
                        .build();
        System.out.println("please wait...");
        VideoSynthesisResult result = vs.call(param);
        System.out.println(JsonUtils.toJson(result));
    }

    public static void main(String[] args) {
        try {
            text2Video();
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

<a id="code-block-18"></a>

```json
{
    "request_id": "c1209113-8437-424f-a386-xxxxxx",
    "output": {
        "task_id": "966cebcd-dedc-4962-af88-xxxxxx",
        "task_status": "SUCCEEDED",
        "video_url": "https://dashscope-result-sh.oss-accelerate.aliyuncs.com/xxx.mp4?Expires=xxx",
        "orig_prompt": "一幅史诗级可爱的场景。一只小巧可爱的卡通小猫将军，身穿细节精致的金色盔甲，头戴一个稍大的头盔，勇敢地站在悬崖上。他骑着一匹虽小但英勇的战马，说：”青海长云暗雪山，孤城遥望玉门关。黄沙百战穿金甲，不破楼兰终不还。“。悬崖下方，一支由老鼠组成的、数量庞大、无穷无尽的军队正带着临时制作的武器向前冲锋。这是一个戏剧性的、大规模的战斗场景，灵感来自中国古代的战争史诗。远处的雪山上空，天空乌云密布。整体氛围是“可爱”与“霸气”的搞笑和史诗般的融合。",
        "submit_time": "2026-01-22 23:13:40.553",
        "scheduled_time": "2026-01-22 23:13:49.415",
        "end_time": "2026-01-22 23:17:56.380"
    },
    "usage": {
        "video_count": 1,
        "duration": 10.0,
        "size": "1280*720",
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

<a id="2fc30f223b9py"></a>

##### 请求示例

<a id="code-block-19"></a>

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

public class Text2Video {

    static {
        // 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。获取URL：https://help.aliyun.com/zh/model-studio/text-to-video-api-reference
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
    }

     // 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    public static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    /**
     * Create a video compositing task and wait for the task to complete.
     */
    public static void text2Video() throws ApiException, NoApiKeyException, InputRequiredException {
        VideoSynthesis vs = new VideoSynthesis();
        Map<String, Object> parameters = new HashMap<>();
        parameters.put("prompt_extend", true);
        parameters.put("watermark", false);
        parameters.put("seed", 12345);

        VideoSynthesisParam param =
                VideoSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("wan2.6-t2v")
                        .prompt("一幅史诗级可爱的场景。一只小巧可爱的卡通小猫将军，身穿细节精致的金色盔甲，头戴一个稍大的头盔，勇敢地站在悬崖上。他骑着一匹虽小但英勇的战马，说：”青海长云暗雪山，孤城遥望玉门关。黄沙百战穿金甲，不破楼兰终不还。“。悬崖下方，一支由老鼠组成的、数量庞大、无穷无尽的军队正带着临时制作的武器向前冲锋。这是一个戏剧性的、大规模的战斗场景，灵感来自中国古代的战争史诗。远处的雪山上空，天空乌云密布。整体氛围是“可爱”与“霸气”的搞笑和史诗般的融合。")
                        .audioUrl("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250923/hbiayh/%E4%BB%8E%E5%86%9B%E8%A1%8C.mp3")
                        .negativePrompt("")
                        .size("1280*720")
                        .duration(10)
                        .parameters(parameters)
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
            text2Video();
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

<a id="38e1e3c7303rm"></a>

##### 响应示例

1、创建任务的响应示例。

<a id="code-block-20"></a>

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

<a id="code-block-21"></a>

```json
{
    "request_id": "c1209113-8437-424f-a386-xxxxxx",
    "output": {
        "task_id": "966cebcd-dedc-4962-af88-xxxxxx",
        "task_status": "SUCCEEDED",
        "video_url": "https://dashscope-result-sh.oss-accelerate.aliyuncs.com/xxx.mp4?Expires=xxx",
        "orig_prompt": "一幅史诗级可爱的场景。一只小巧可爱的卡通小猫将军，身穿细节精致的金色盔甲，头戴一个稍大的头盔，勇敢地站在悬崖上。他骑着一匹虽小但英勇的战马，说：”青海长云暗雪山，孤城遥望玉门关。黄沙百战穿金甲，不破楼兰终不还。“。悬崖下方，一支由老鼠组成的、数量庞大、无穷无尽的军队正带着临时制作的武器向前冲锋。这是一个戏剧性的、大规模的战斗场景，灵感来自中国古代的战争史诗。远处的雪山上空，天空乌云密布。整体氛围是“可爱”与“霸气”的搞笑和史诗般的融合。",
        "submit_time": "2026-01-22 23:13:40.553",
        "scheduled_time": "2026-01-22 23:13:49.415",
        "end_time": "2026-01-22 23:17:56.380"
    },
    "usage": {
        "video_count": 1,
        "duration": 10.0,
        "size": "1280*720",
        "input_video_duration": 0.0,
        "output_video_duration": 10.0,
        "SR": "720"
    },
    "status_code": 200,
    "code": "",
    "message": ""
}
```

<a id="错误码"></a>

<a id="OajFO"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](../model-api-reference/preparations/error-code.md)进行解决。

<a id="常见问题"></a>

<a id="c928ee689aw6l"></a>

## 常见问题

<a id="q-如何将临时的视频链接转为永久链接"></a>

<a id="99f5bae3c2y7a"></a>

#### Q: 如何将临时的视频链接转为永久链接？

A: 不能直接转换该链接。正确的做法是：后端服务获取到url后，通过代码下载该视频文件，然后将其上传到永久对象存储服务（如阿里云 OSS），生成一个新的、永久访问链接。

<a id="accordion-示例代码-下载视频到本地"></a>

示例代码：下载视频到本地

<a id="code-block-22"></a>

```python
import requests

def download_and_save_video(video_url, save_path):
    try:
        response = requests.get(video_url, stream=True, timeout=300) # 设置超时
        response.raise_for_status() # 如果HTTP状态码不是200，则引发异常
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"视频已成功下载到: {save_path}")
        # 此处可以接上传到永久存储的逻辑
    except requests.exceptions.RequestException as e:
        print(f"下载视频失败: {e}")

if __name__ == '__main__':
    video_url = "http://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/xxxx"
    save_path = "video.mp4"
    download_and_save_video(video_url, save_path)
```

<a id="q-返回的视频链接可以在浏览器中直接播放吗"></a>

<a id="bc74fbbfach4a"></a>

#### Q: 返回的视频链接可以在浏览器中直接播放吗？

A: 不建议这样做，因为链接会在 24 小时后失效。最佳实践是后端下载转存后，使用永久链接进行视频播放。
