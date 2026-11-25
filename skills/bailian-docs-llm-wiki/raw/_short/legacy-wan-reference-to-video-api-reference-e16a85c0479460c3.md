# 万相-参考生视频API参考（2.6）

万相2.6-参考生视频模型支持 多模态输入 ，可将人或物体作为主角，生成单角色表演或多角色互动视频。

**相关文档**：[使用指南](video-to-video-guide-f63917cdae4414ac.md)

<a id="适用范围"></a>

<a id="1fd78afa5brlj"></a>

## 适用范围

为确保调用成功，请务必保证模型、Endpoint URL 和 API Key 均属于**同一地域**。跨地域调用将会失败。

-   [**选择模型**](video-to-video-guide-f63917cdae4414ac.md#06f39eafa2dwt)：确认模型所属的地域。
-   **选择 URL**：选择对应的地域 Endpoint URL，支持HTTP URL。
-   **配置 API Key**：选择地域并[获取与配置 API Key](../model-api-reference/preparations/get-api-key.md)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

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
> 此接口为**旧版协议**，只支持**wan2.6模型**。

由于视频生成任务耗时较长（通常为1-5分钟），API采用异步调用。整个流程包含 **“创建任务 -> 轮询获取”** 两个核心步骤，具体如下：

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

<table><tbody><tr><td><a id="afcd41d2b57zf"></a><h4>请求参数</h4><a id="79473e45c592d"></a><h5>请求头（Headers）</h5><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><p><strong>X-DashScope-Async</strong><code>string</code><strong>（必选）</strong></p><p>异步处理配置参数。HTTP请求只支持异步，<strong>必须设置为</strong><code>enable</code>。</p><div><div><p><strong>重要</strong>缺少此请求头将报错：“current user api does not support synchronous calls”。</p></div></div><a id="66a778d4fbfub"></a><h5>请求体（Request Body）</h5><p><strong>model</strong> <code>string</code> <strong>（必选）</strong></p><p>模型名称。模型列表与价格详见<a href="../model-user-guide/test-1/model-pricing.md#5c3d28ad8a4x8">模型价格</a>。</p><p>示例值：wan2.6-r2v-flash。</p><p><strong>input</strong> <code>object</code> <strong>（必选）</strong></p><p>输入的基本信息，如提示词等。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>prompt</strong> <code>string</code> <strong>（必选）</strong></p><p>文本提示词。用来描述生成视频中期望包含的元素和视觉特点。</p><p>支持中英文，每个汉字、字母、标点占一个字符，超过部分会自动截断。</p><ul><li>wan2.6-r2v-flash：长度不超过1500个字符。</li><li>wan2.6-r2v：长度不超过1500个字符。</li></ul><p>角色引用说明：通过“<strong>character1、character2</strong>”这类标识引用参考角色，每个参考（视频或图像）仅包含单一角色。模型仅通过此方式识别参考中的角色。</p><p>示例值：character1在沙发上开心地看电影。</p><p>提示词的使用技巧请参见<a href="../model-user-guide/use-cases/text-to-video-prompt.md">文生视频/图生视频Prompt指南</a>。</p><p><strong>negative_prompt</strong> <code>string</code> （可选）</p><p>反向提示词，用来描述不希望在视频画面中出现的内容，可以对视频画面进行限制。</p><p>支持中英文，长度不超过500个字符，超过部分会自动截断。</p><p>示例值：低分辨率、错误、最差质量、低质量、残缺、多余的手指、比例不良等。</p><p><strong>reference_urls</strong> <code>array[string]</code> <strong>（必选）</strong></p><div><div><p><strong>重要</strong>reference_urls直接影响费用，计费规则请参见<a href="video-to-video-guide-f63917cdae4414ac.md#6f5774ce5fqie">计费与限流</a>。</p></div></div><p>上传的参考文件 URL 数组，支持传入视频和图像。用于提取角色形象与音色（如有），以生成符合参考特征的视频。</p><ul><li><p>每个 URL 可指向 <strong>一张图像</strong> 或 <strong>一段视频</strong>：</p><ul><li>图像数量：0～5。</li><li>视频数量：0～3。</li><li>总数限制：图像 + 视频 ≤ 5。</li></ul></li><li><p>传入多个参考文件时，按照数组顺序定义角色的顺序。即第 1 个 URL 对应 character1，第 2 个对应 character2，以此类推。</p></li><li><p>每个参考文件仅包含一个主体角色。例如 character1 为小女孩，character2 为闹钟。</p></li></ul><p>支持输入的格式：</p><ol><li><p>公网URL:</p><ul><li>支持 HTTP 或 HTTPS 协议。</li><li>示例值：<a href="https://cdn.translate.alibaba.com/xxx.png"></a><a href="https://cdn.translate.alibaba.com/xxx.png">https://cdn.translate.alibaba.com/xxx.png</a>。</li></ul></li><li><p>临时URL：</p><ul><li>支持OSS协议，必须通过<a href="../model-api-reference/more-about-models/get-temporary-file-url.md">上传文件获取临时 URL</a>。</li><li>示例值：oss://dashscope-instant/xxx/xxx.png。</li></ul></li></ol><p>参考视频要求：</p><ul><li>格式：MP4、MOV。</li><li>时长：1s～30s。</li><li>视频大小：不超过100MB。</li></ul><p>参考图像要求：</p><ul><li>格式：JPEG、JPG、PNG（不支持透明通道）、BMP、WEBP。</li><li>分辨率：宽高均需在[240,8000]像素之间。</li><li>图像大小：不超过20MB。</li></ul><p>示例值：[&quot;<a href="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/xxx.mp4"></a><a href="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/xxx.mp4">https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/xxx.mp4</a>&quot;, &quot;<a href="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/xxx.jpg"></a><a href="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/xxx.jpg">https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/xxx.jpg</a>&quot;]。</p><a id="accordion-已废弃字段"></a><section><p>已废弃字段</p><div><p><strong>reference_video_urls</strong> <code>array[string]</code></p><div><div><p><strong>重要</strong>推荐使用<code>reference_urls</code>替代<code>reference_video_urls</code>。</p></div></div><p>上传的参考视频文件 URL 数组。用于提取角色形象与音色（如有），以生成符合参考特征的视频。</p><ul><li>最多支持 <strong>3 个视频</strong>。</li><li>传入多个视频时，按照数组顺序定义视频角色的顺序。即第 1 个 URL 对应 character1，第 2 个对应 character2，以此类推。</li><li>每个参考视频仅包含一个角色（如 character1 为小女孩，character2 为闹钟）。</li><li>URL支持 HTTP 或 HTTPS 协议。本地文件可通过<a href="../model-api-reference/more-about-models/get-temporary-file-url.md">上传文件获取临时URL</a>。</li></ul><p>单个视频要求：</p><ul><li>格式：MP4、MOV。</li><li>时长：2～30s。</li><li>文件大小：视频不超过100MB。</li></ul><p>示例值：[&quot;<a href="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/xxx.mp4"></a><a href="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/xxx.mp4">https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/xxx.mp4</a>&quot;]。</p></div></section></div></section><p><strong>parameters</strong> <code>object</code> （可选）</p><p>图像处理参数。如设置视频分辨率、开启prompt智能改写、添加水印等。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>size</strong> <code>string</code> （可选）</p><div><div><p><strong>重要</strong></p><ul><li>size直接影响费用，费用 = 单价（基于分辨率）× 时长（秒）。同一模型：1080P &gt; 720P ，请在调用前确认<a href="../model-user-guide/test-1/model-pricing.md#5c3d28ad8a4x8">模型价格</a>。</li><li>size必须设置为具体数值（如 <code>1280*720</code>），而不是 1:1或720P。</li></ul></div></div><p>指定生成的视频分辨率，格式为<code>宽*高</code>。该参数的默认值和可用枚举值依赖于 model 参数，规则如下：</p><ul><li>wan2.6-r2v-flash：默认值为 <code>1920*1080</code>（1080P）。可选分辨率：720P、1080P对应的所有分辨率。</li><li>wan2.6-r2v：默认值为 <code>1920*1080</code>（1080P）。可选分辨率：720P、1080P对应的所有分辨率。</li></ul><p>720P档位：可选的视频分辨率及其对应的视频宽高比为：</p><ul><li><code>1280*720</code>：16:9。</li><li><code>720*1280</code>：9:16。</li><li><code>960*960</code>：1:1。</li><li><code>1088*832</code>：4:3。</li><li><code>832*1088</code>：3:4。</li></ul><p>1080P档位：可选的视频分辨率及其对应的视频宽高比为：</p><ul><li><code>1920*1080</code>： 16:9。</li><li><code>1080*1920</code>： 9:16。</li><li><code>1440*1440</code>： 1:1。</li><li><code>1632*1248</code>： 4:3。</li><li><code>1248*1632</code>： 3:4。</li></ul><p><strong>duration</strong> <code>integer</code> （可选）</p><div><div><p><strong>重要</strong>duration直接影响费用。费用 = 单价（基于分辨率）× 时长（秒），请在调用前确认<a href="../model-user-guide/test-1/model-pricing.md#5c3d28ad8a4x8">模型价格</a>。</p></div></div><p>生成视频的时长，单位为秒。</p><ul><li>wan2.6-r2v-flash：取值为[2, 10]之间的整数。默认值为5。</li><li>wan2.6-r2v：取值为[2, 10]之间的整数。默认值为5。</li></ul><p>示例值：5。</p><p><strong>shot_type</strong> <code>string</code> （可选）</p><p>指定生成视频的镜头类型，即视频是由一个连续镜头还是多个切换镜头组成。</p><p>参数优先级：<code>shot_type &gt; prompt</code>。例如，若 shot_type设置为&quot;single&quot;，即使 prompt 中包含“生成多镜头视频”，模型仍会输出单镜头视频。</p><p>可选值：</p><ul><li>single：默认值，输出单镜头视频</li><li>multi：输出多镜头视频。</li></ul><p>示例值：single。</p><div><div><p><strong>说明</strong>当希望严格控制视频的叙事结构（如产品展示用单镜头、故事短片用多镜头），可通过此参数指定。</p></div></div><p><strong>audio</strong> <code>boolean</code> （可选）</p><div><div><p><strong>重要</strong>audio直接影响费用，有声视频与无声视频价格不同，请在调用前确认<a href="../model-user-guide/test-1/model-pricing.md#5c3d28ad8a4x8">模型价格</a>。</p></div></div><strong>支持模型：wan2.6-r2v-flash。</strong><p>是否生成有声视频。</p><p>可选值：</p><ul><li>true：默认值，输出有声视频。</li><li>false：输出无声视频。</li></ul><p>示例值：true。</p><p><strong>watermark</strong> <code>boolean</code> （可选）</p><p>是否添加水印标识，水印位于视频右下角，文案固定为“AI生成”。</p><ul><li>false：默认值，不添加水印。</li><li>true：添加水印。</li></ul><p>示例值：false。</p><p><strong>seed</strong><code>integer</code>（可选）</p><p>随机数种子，取值范围为<code>[0, 2147483647]</code>。</p><p>未指定时，系统自动生成随机种子。若需提升生成结果的可复现性，建议固定seed值。</p><p>请注意，由于模型生成具有概率性，即使使用相同 seed，也不能保证每次生成结果完全一致。</p></div></section></td><td><a id="sec-tabs-2"></a><section><a id="多角色互动-参考图像和视频"></a><section><a id="多角色互动-参考图像和视频-h4"></a><h4>多角色互动（参考图像和视频）</h4><p>通过<code>reference_urls</code>传入图像和视频URL。同时设置<code>shot_type</code>为<code>multi</code>，生成多镜头视频。</p><a id="code-block"></a><pre class="language-bash"><code># 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;wan2.6-r2v-flash&quot;,
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;Character2 坐在靠窗的椅子上，手持 character3，在 character4 旁演奏一首舒缓的美国乡村民谣。Character1 对Character2开口说道：“听起来不错”&quot;,
        &quot;reference_urls&quot;: [
            &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/hfugmr/wan-r2v-role1.mp4&quot;,
            &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qigswt/wan-r2v-role2.mp4&quot;,
            &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qpzxps/wan-r2v-object4.png&quot;,
            &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/wfjikw/wan-r2v-backgroud5.png&quot;
        ]
    },
    &quot;parameters&quot;: {
        &quot;size&quot;: &quot;1280*720&quot;,
        &quot;duration&quot;: 10,
        &quot;audio&quot;: true,
        &quot;shot_type&quot;: &quot;multi&quot;,
        &quot;watermark&quot;: true
    }
}'
</code></pre></section><a id="多角色互动-参考视频"></a><section><a id="多角色互动-参考视频-h4"></a><h4>多角色互动（参考视频）</h4><p>通过<code>reference_urls</code>传入多个视频URL。同时设置<code>shot_type</code>为<code>multi</code>，生成多镜头视频。</p><a id="code-block-2"></a><pre class="language-bash"><code># 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;wan2.6-r2v&quot;,
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;character1对character2说: “I’ll rely on you tomorrow morning!” character2 回答: “You can count on me!”&quot;,
        &quot;reference_urls&quot;: [
            &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251217/dlrrly/%E5%B0%8F%E5%A5%B3%E5%AD%A91%E8%8B%B1%E6%96%872.mp4&quot;,
            &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251217/fkxknn/%E9%93%83%E9%93%83.mp4&quot;
        ]
    },
    &quot;parameters&quot;: {
        &quot;size&quot;: &quot;1280*720&quot;,
        &quot;duration&quot;: 10,
        &quot;shot_type&quot;: &quot;multi&quot;
    }
}'
</code></pre></section><a id="单角色扮演"></a><section><a id="单角色扮演-h4"></a><h4>单角色扮演</h4><p>通过<code>reference_urls</code>传入单个视频URL。同时设置<code>shot_type</code>为<code>multi</code>，生成多镜头视频。</p><a id="code-block-3"></a><pre class="language-bash"><code># 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;wan2.6-r2v&quot;,
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;character1一边喝奶茶，一边随着音乐即兴跳舞。&quot;,
        &quot;reference_urls&quot;:[&quot;https://cdn.wanx.aliyuncs.com/static/demo-wan26/vace.mp4&quot;]
    },
    &quot;parameters&quot;: {
        &quot;size&quot;: &quot;1280*720&quot;,
        &quot;duration&quot;: 5,
        &quot;shot_type&quot;:&quot;multi&quot;
    }
}'
</code></pre></section><a id="生成无声视频"></a><section><a id="生成无声视频-h4"></a><h4>生成无声视频</h4><p>仅支持<code>wan2.6-r2v-flash</code>生成无声视频。</p><p>当生成无声视频时，<strong>必须显式设置</strong> <code>parameters.audio = false</code>。</p><a id="code-block-4"></a><pre class="language-bash"><code># 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;wan2.6-r2v-flash&quot;,
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;character1一边喝奶茶，一边随着音乐即兴跳舞。&quot;,
        &quot;reference_urls&quot;:[&quot;https://cdn.wanx.aliyuncs.com/static/demo-wan26/vace.mp4&quot;]
    },
    &quot;parameters&quot;: {
        &quot;size&quot;: &quot;1280*720&quot;,
        &quot;duration&quot;: 5,
        &quot;audio&quot;: false,
        &quot;shot_type&quot;:&quot;multi&quot;
    }
}'
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="cd3063363egdc"></a><h4>响应参数</h4><p><strong>output</strong> <code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../model-api-reference/preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../model-api-reference/preparations/error-code.md">错误码</a>。</p></td><td><a id="sec-tabs-3"></a><section><a id="成功响应"></a><section><a id="成功响应-h4"></a><h4>成功响应</h4><p>请保存 task_id，用于查询任务状态与结果。</p><a id="code-block-5"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
        &quot;task_status&quot;: &quot;PENDING&quot;,
        &quot;task_id&quot;: &quot;0385dc79-5ff8-4d82-bcb6-xxxxxx&quot;
    },
    &quot;request_id&quot;: &quot;4909100c-7b5a-9f92-bfe5-xxxxxx&quot;
}
</code></pre></section><a id="异常响应"></a><section><a id="异常响应-h4"></a><h4>异常响应</h4><p>创建任务失败，请参见<a href="../model-api-reference/preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-6"></a><pre class="language-json"><code>{
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

<table><tbody><tr><td><a id="a9e0408c70ylw"></a><h4>请求参数</h4><a id="2d2fb41da6idy"></a><h5>请求头（Headers）</h5><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><a id="031d8a0fafqhp"></a><h5>URL路径参数（Path parameters）</h5><p><strong>task_id</strong> <code>string</code><strong>（必选）</strong></p><p>任务ID。</p></td><td><a id="sec-tabs-5"></a><section><a id="查询任务结果"></a><section><a id="查询任务结果-h4"></a><h4>查询任务结果</h4><p>将<code>{task_id}</code>完整替换为上一步接口返回的<code>task_id</code>的值。<code>task_id</code>查询有效期为24小时，并请将<code>{WorkspaceId}</code>替换为真实的<a href="../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain">业务空间ID</a>。</p><a id="code-block-7"></a><pre class="language-bash"><code>curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id} \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="810682d979i8q"></a><h4>响应参数</h4><p><strong>output</strong><code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code><strong>（必选）</strong></p><p>任务ID。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值-2"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section><p><strong>submit_time</strong> <code>string</code></p><p>任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>scheduled_time</strong> <code>string</code></p><p>任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>end_time</strong> <code>string</code></p><p>任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>video_url</strong><code>string</code></p><p>视频URL。仅在 task_status 为 SUCCEEDED 时返回。</p><p>链接有效期24小时，可通过此URL下载视频。视频格式为MP4（H.264 编码）。</p><p><strong>orig_prompt</strong> <code>string</code></p><p>原始输入的prompt，对应请求参数<code>prompt</code>。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../model-api-reference/preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../model-api-reference/preparations/error-code.md">错误码</a>。</p></div></section><p><strong>usage</strong> <code>object</code></p><p>输出信息统计。只对成功的结果计数。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>input_video_duration</strong> <code>integer</code></p><p>输入的参考视频的时长，单位秒。</p><p><strong>output_video_duration</strong> <code>integer</code></p><p>输出视频的时长，单位秒。</p><p><strong>duration</strong> <code>float</code></p><p>总视频时长。计费按duration时长计算。</p><p>计算公式：<code>duration = input_video_duration + output_video_duration</code>。</p><p><strong>SR</strong> <code>integer</code></p><p>生成视频的分辨率档位。示例值：720。</p><p><strong>size</strong><code>string</code></p><p>生成视频的分辨率。格式为“宽<em>高</em>”<em>，示例值：1280</em>720。</p><p><strong>video_count</strong> <code>integer</code></p><p>生成视频的数量。固定为1。</p></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p></td><td><a id="sec-tabs-6"></a><section><a id="任务执行成功"></a><section><a id="任务执行成功-h4"></a><h4>任务执行成功</h4><p>视频URL仅保留24小时，超时后会被自动清除，请及时保存生成的视频。</p><a id="code-block-8"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;caa62a12-8841-41a6-8af2-xxxxxx&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;eff1443c-ccab-4676-aad3-xxxxxx&quot;,
        &quot;task_status&quot;: &quot;SUCCEEDED&quot;,
        &quot;submit_time&quot;: &quot;2025-12-16 00:25:59.869&quot;,
        &quot;scheduled_time&quot;: &quot;2025-12-16 00:25:59.900&quot;,
        &quot;end_time&quot;: &quot;2025-12-16 00:30:35.396&quot;,
        &quot;orig_prompt&quot;: &quot;character1在沙发上开心的看电影&quot;,
        &quot;video_url&quot;: &quot;https://dashscope-result-sh.oss-accelerate.aliyuncs.com/xxx.mp4?Expires=xxx&quot;
    },
     &quot;usage&quot;: {
        &quot;duration&quot;: 10.0,
        &quot;size&quot;: &quot;1280*720&quot;,
        &quot;input_video_duration&quot;: 5,
        &quot;output_video_duration&quot;: 5,
        &quot;video_count&quot;: 1,
        &quot;SR&quot;: 720
    }
}
</code></pre></section><a id="任务执行失败"></a><section><a id="任务执行失败-h4"></a><h4>任务执行失败</h4><p>若任务执行失败，task_status将置为 FAILED，并提供错误码和信息。请参见<a href="../model-api-reference/preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-9"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;e5d70b02-ebd3-98ce-9fe8-759d7d7b107d&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;86ecf553-d340-4e21-af6e-a0c6a421c010&quot;,
        &quot;task_status&quot;: &quot;FAILED&quot;,
        &quot;code&quot;: &quot;InvalidParameter&quot;,
        &quot;message&quot;: &quot;The size is not match xxxxxx&quot;
    }
}
</code></pre></section><a id="任务查询过期"></a><section><a id="任务查询过期-h4"></a><h4>任务查询过期</h4><p>task_id查询有效期为 24 小时，超时后将无法查询，返回以下报错信息。</p><a id="code-block-10"></a><pre class="language-json"><code>{
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

SDK 的参数命名与[HTTP接口](legacy-wan-reference-to-video-api-reference-e16a85c0479460c3.md#42703589880ts)基本一致，参数结构根据语言特性进行封装。

由于参考生视频任务耗时较长（通常为1-5分钟），SDK 在底层封装了 HTTP 异步调用流程，支持同步、异步两种调用方式。

> 具体耗时受限于排队任务数和服务执行情况，请在获取结果时耐心等待。

<a id="python-sdk调用"></a>

<a id="29484e9a6a0qr"></a>

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

<a id="美国"></a>

<a id="美国-h4"></a>

#### 美国

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

同步调用会阻塞等待，直到视频生成完成并返回结果。

<a id="r2v741a6h5rq01"></a>

##### 请求示例

<a id="code-block-11"></a>

```python
import dashscope
from dashscope import DashScopeError
import os

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
            model='wan2.6-r2v-flash',
            prompt='Character2 坐在靠窗的椅子上，手持 character3，在 character4 旁演奏一首舒缓的美国乡村民谣。Character1 对Character2开口说道：“听起来不错”',
            # reference_urls 为 input 段字段，不在具名签名内，经 extra_input 透传
            # shot_type / audio 为 parameters 段字段，经 parameters 透传
            extra_input={'reference_urls': [
                "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/hfugmr/wan-r2v-role1.mp4",
                "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qigswt/wan-r2v-role2.mp4",
                "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qpzxps/wan-r2v-object4.png",
                "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/wfjikw/wan-r2v-backgroud5.png"
            ]},
            size='1280*720',
            duration=10,
            watermark=True,
            parameters={'shot_type': 'multi', 'audio': True})
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

<a id="异步调用"></a>

<a id="异步调用-h4"></a>

#### 异步调用

异步调用立即返回任务 ID，可通过 fetch 查询状态，或调用 wait 等待完成（内部自动轮询）。

<a id="r2v747a7h5rq02"></a>

##### 请求示例

<a id="code-block-12"></a>

```python
import os
import dashscope
from dashscope import DashScopeError

# 以下为华北2（北京）地域的配置。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

def sample_async_call_r2v_26():
    # 异步调用，返回一个task_id
    try:
        job = client.videos.jobs.create(
            model='wan2.6-r2v-flash',
            prompt='Character2 坐在靠窗的椅子上，手持 character3，在 character4 旁演奏一首舒缓的美国乡村民谣。Character1 对Character2开口说道：“听起来不错”',
            # reference_urls 为 input 段字段，不在具名签名内，经 extra_input 透传
            # shot_type / audio 为 parameters 段字段，经 parameters 透传
            extra_input={'reference_urls': [
                "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/hfugmr/wan-r2v-role1.mp4",
                "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qigswt/wan-r2v-role2.mp4",
                "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qpzxps/wan-r2v-object4.png",
                "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/wfjikw/wan-r2v-backgroud5.png"
            ]},
            size='1280*720',
            duration=10,
            watermark=True,
            parameters={'shot_type': 'multi', 'audio': True})
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
    sample_async_call_r2v_26()
```

<a id="java-sdk调用"></a>

<a id="3f41c60916y03"></a>

### Java SDK调用

> **重要**
>
> 请确保 DashScope Java SDK 版本**不低于**`2.22.14`，再运行以下代码。
>
> 若版本过低，可能会触发 "url error, please check url!" 等错误。请参考[安装SDK](../model-api-reference/preparations/install-sdk.md)进行更新。

根据模型所在地域设置 `baseHttpApiUrl`:

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

<a id="法兰克福-4"></a>

<a id="法兰克福-4-h4"></a>

#### 法兰克福

`Constants.baseHttpApiUrl = "https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/api/v1";`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="sec-tabs-10"></a>

<a id="同步调用-2"></a>

<a id="同步调用-2-h4"></a>

#### 同步调用

同步调用会阻塞等待，直到视频生成完成并返回结果。

<a id="r2v832a7h5jr01"></a>

##### 请求示例

<a id="code-block-13"></a>

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
import java.util.List;

public class Ref2Video26 {

    static {
        // 以下为北京地域url，各地域的url不同
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
    }

    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey="sk-xxx"
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    public static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    public static void ref2video26() throws ApiException, NoApiKeyException, InputRequiredException {
        VideoSynthesis vs = new VideoSynthesis();
        List<String> referenceUrls = new ArrayList<>();
        referenceUrls.add("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/hfugmr/wan-r2v-role1.mp4");
        referenceUrls.add("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qigswt/wan-r2v-role2.mp4");
        referenceUrls.add("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qpzxps/wan-r2v-object4.png");
        referenceUrls.add("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/wfjikw/wan-r2v-backgroud5.png");

        VideoSynthesisParam param =
                VideoSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("wan2.6-r2v-flash")
                        .prompt("Character2 坐在靠窗的椅子上，手持 character3，在 character4 旁演奏一首舒缓的美国乡村民谣。Character1 对Character2开口说道：“听起来不错”")
                        .referenceUrls(referenceUrls)
                        .shotType(VideoSynthesis.ShotType.MULTI)
                        .audio(Boolean.TRUE)
                        .size("1280*720")
                        .duration(10)
                        .watermark(Boolean.TRUE)
                        .build();
        System.out.println("please wait...");
        VideoSynthesisResult result = vs.call(param);
        System.out.println(JsonUtils.toJson(result));
    }

    public static void main(String[] args) {
        try {
            ref2video26();
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

<a id="异步调用-2"></a>

<a id="异步调用-2-h4"></a>

#### 异步调用

异步调用会立即返回任务ID，需要自行轮询或等待任务完成。

<a id="r2v839a7h5jr02"></a>

##### 请求示例

<a id="code-block-14"></a>

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
import java.util.List;

public class Ref2Video26Async {

    static {
        // 以下为北京地域url，各地域的url不同
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
    }

    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey="sk-xxx"
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    public static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    public static void asyncRef2video26() throws ApiException, NoApiKeyException, InputRequiredException, InterruptedException {
        VideoSynthesis vs = new VideoSynthesis();
        List<String> referenceUrls = new ArrayList<>();
        referenceUrls.add("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/hfugmr/wan-r2v-role1.mp4");
        referenceUrls.add("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qigswt/wan-r2v-role2.mp4");
        referenceUrls.add("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qpzxps/wan-r2v-object4.png");
        referenceUrls.add("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/wfjikw/wan-r2v-backgroud5.png");

        VideoSynthesisParam param =
                VideoSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("wan2.6-r2v-flash")
                        .prompt("Character2 坐在靠窗的椅子上，手持 character3，在 character4 旁演奏一首舒缓的美国乡村民谣。Character1 对Character2开口说道：“听起来不错”")
                        .referenceUrls(referenceUrls)
                        .shotType(VideoSynthesis.ShotType.MULTI)
                        .audio(Boolean.TRUE)
                        .size("1280*720")
                        .duration(10)
                        .watermark(Boolean.TRUE)
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
            asyncRef2video26();
        } catch (ApiException | NoApiKeyException | InputRequiredException | InterruptedException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

<a id="错误码"></a>

<a id="OajFO"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](../model-api-reference/preparations/error-code.md)进行解决。
