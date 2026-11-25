# 万相-首尾帧生视频API参考（2.2）

万相2.2-首尾帧生视频模型基于 首帧图像 、 尾帧图像和文本提示词 ，生成一段平滑过渡的视频。

**相关文档**：[使用指南](../model-user-guide/use-cases/legacy-resources/legacy-video-generation/image-to-video-first-and-last-frames-guide.md)

<a id="适用范围"></a>

<a id="1fd78afa5brlj"></a>

## 适用范围

为确保调用成功，请务必保证模型、Endpoint URL 和 API Key 均属于**同一地域**。跨地域调用将会失败。

-   [**选择模型**](../model-user-guide/use-cases/legacy-resources/legacy-video-generation/image-to-video-first-and-last-frames-guide.md#06f39eafa2dwt)：确认模型所属的地域。
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

由于图生视频任务耗时较长（通常为1-5分钟），API采用异步调用。整个流程包含 **“创建任务 -> 轮询获取”** 两个核心步骤，具体如下：

<a id="步骤1-创建任务获取任务id"></a>

<a id="81185ac18blmj"></a>

### 步骤1：创建任务获取任务ID

<a id="sec-tabs"></a>

<a id="北京"></a>

<a id="北京-h4"></a>

#### 北京

`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="新加坡"></a>

<a id="新加坡-h4"></a>

#### 新加坡

`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

> **说明**
>
> -   创建成功后，使用接口返回的 `task_id` 查询结果，task\_id 有效期为 24 小时。**请勿重复创建任务**，轮询获取即可。
> -   新手指引请参见[Postman](https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api)。

<table><tbody><tr><td><a id="afcd41d2b57zf"></a><h4>请求参数</h4><a id="79473e45c592d"></a><h5>请求头（Headers）</h5><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><p><strong>X-DashScope-Async</strong><code>string</code><strong>（必选）</strong></p><p>异步处理配置参数。HTTP请求只支持异步，<strong>必须设置为</strong><code>enable</code>。</p><div><div><p><strong>重要</strong>缺少此请求头将报错：“current user api does not support synchronous calls”。</p></div></div><a id="66a778d4fbfub"></a><h5>请求体（Request Body）</h5><p><strong>model</strong> <code>string</code> <strong>（必选）</strong></p><p>模型名称。示例值：wan2.2-kf2v-flash。</p><p>详情参见百炼控制台。</p><p><strong>input</strong> <code>object</code> <strong>（必选）</strong></p><p>输入的基本信息，如提示词等。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>prompt</strong> <code>string</code> （可选）</p><p>文本提示词。支持中英文，长度不超过800个字符，每个汉字/字母占一个字符，超过部分会自动截断。</p><p>如果首尾帧的主体和场景变化较大，建议描写变化过程，例如运镜过程（镜头向左移动）或者主体运动过程（人向前奔跑）。</p><p>示例值：一只黑色小猫好奇地看向天空，<strong>镜头从平视逐渐上升</strong>，最后<strong>俯拍</strong>它的好奇的眼神。</p><p>提示词的使用技巧请参见<a href="../model-user-guide/use-cases/text-to-video-prompt.md">文生视频/图生视频Prompt指南</a>。</p><p><strong>negative_prompt</strong> <code>string</code> （可选）</p><p>反向提示词，用来描述不希望在视频画面中看到的内容，可以对视频画面进行限制。</p><p>支持中英文，长度不超过500个字符，超过部分会自动截断。</p><p>示例值：低分辨率、错误、最差质量、低质量、残缺、多余的手指、比例不良等。</p><p><strong>first_frame_url</strong> <code>string</code> <strong>（必选）</strong></p><p>首帧图像的URL或 Base64 编码数据。<strong>输出视频的宽高比将以此图像为基准。</strong></p><p>图像限制：</p><ul><li>图像格式：JPEG、JPG、PNG（不支持透明通道）、BMP、WEBP。</li><li>图像分辨率：图像的宽度和高度范围为[240,8000]，单位为像素。</li><li>文件大小：不超过10MB。</li></ul><p>支持输入的格式：</p><ol><li><p>公网URL:</p><ul><li>支持 HTTP 或 HTTPS 协议。</li><li>示例值：<a href="https://wanx.alicdn.com/xxx/first_frame.png"></a><a href="https://wanx.alicdn.com/xxx/first_frame.png">https://wanx.alicdn.com/xxx/first_frame.png</a>。</li></ul></li><li><p>临时URL：</p><ul><li>支持OSS协议，必须通过<a href="../model-api-reference/more-about-models/get-temporary-file-url.md">上传文件获取临时 URL</a>。</li><li>示例值：oss://dashscope-instant/xxx/xxx.png。</li></ul></li><li><p>Base64 编码图像后的字符串：</p><ul><li>数据格式：<code>data:{MIME_type};base64,{base64_data}</code>。</li><li>示例值：data:image/png;base64,GDU7MtCZzEbTbmRZ......。（编码字符串过长，仅展示片段）</li><li>详情请参见<a href="../model-user-guide/use-cases/legacy-resources/legacy-video-generation/image-to-video-first-and-last-frames-guide.md#69308edfbebnx">如何输入图像</a>。</li></ul></li></ol><p><strong>last_frame_url</strong> <code>string</code> （可选）</p><p>尾帧图像的URL或 Base64 编码数据。</p><p>图像限制：</p><ul><li>图像格式：JPEG、JPG、PNG（不支持透明通道）、BMP、WEBP。</li><li>图像分辨率：图像的宽度和高度范围为[240,8000]，单位为像素。尾帧图像分辨率可与首帧不同，无需强制对齐。</li><li>文件大小：不超过10MB。</li></ul><p>支持输入的格式：</p><ol><li><p>公网URL:</p><ul><li>支持 HTTP 或 HTTPS 协议。</li><li>示例值：<a href="https://wanx.alicdn.com/xxxx/last_frame.png"></a><a href="https://wanx.alicdn.com/xxxx/last_frame.png">https://wanx.alicdn.com/xxxx/last_frame.png</a>。</li></ul></li><li><p>临时URL：</p><ul><li>支持OSS协议，必须通过<a href="../model-api-reference/more-about-models/get-temporary-file-url.md">上传文件获取临时 URL</a>。</li><li>示例值：oss://dashscope-instant/xxx/xxx.png。</li></ul></li><li><p>Base64 编码图像后的字符串：</p><ul><li>数据格式：<code>data:{MIME_type};base64,{base64_data}</code>。</li><li>示例值：data:image/png;base64,GDU7MtCZ......。（编码字符串过长，仅展示片段）</li><li>详情请参见<a href="../model-user-guide/use-cases/legacy-resources/legacy-video-generation/image-to-video-first-and-last-frames-guide.md#69308edfbebnx">如何输入图像</a>。</li></ul></li></ol><p><strong>template</strong> <code>string</code> （可选）</p><p>视频特效模板的名称。使用此参数时，仅需传入 <code>first_frame_url</code>。</p><p>不同模型支持不同的特效模板。调用前请查阅<a href="wanx-video-effects-5b23bdd72b8e7944.md">万相-图生视频-视频特效列表</a>，以免调用失败。</p><p>示例值：hufu-1，表示使用“唐韵翩然”特效。</p></div></section><p><strong>parameters</strong> <code>object</code> （可选）</p><p>视频处理参数。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>resolution</strong> <code>string</code> （可选）</p><div><div><p><strong>重要</strong><strong>resolution</strong>直接影响费用，同一模型：1080P &gt; 720P &gt; 480P，调用前请确认百炼控制台。</p></div></div><p>生成的视频分辨率档位。仅用于调整视频的清晰度（总像素），不改变视频的宽高比，<strong>视频宽高比将与首帧图像 first_frame_url 的宽高比保持一致</strong>。</p><p>此参数的默认值和可用枚举值依赖于 model 参数，规则如下：</p><ul><li>wan2.2-kf2v-flash：可选值：480P、720P、1080P。默认值为<code>720P</code>。</li><li>wanx2.1-kf2v-plus：可选值：720P。默认值为<code>720P</code>。</li></ul><p>示例值：720P。</p><p><strong>duration</strong> <code>integer</code> （可选）</p><div><div><p><strong>重要</strong>duration直接影响费用，按秒计费，调用前请确认百炼控制台。</p></div></div><p>视频生成时长，单位为秒。当前参数值固定为5，且不支持修改。模型将始终生成5秒时长的视频。</p><p><strong>prompt_extend</strong><code>bool</code> （可选）</p><p>是否开启prompt智能改写。开启后使用大模型对输入prompt进行智能改写。对于较短的prompt生成效果提升明显，但会增加耗时。</p><ul><li>true：默认值，开启智能改写。</li><li>false：不开启智能改写。</li></ul><p>示例值：true。</p><p><strong>watermark</strong> <code>bool</code> （可选）</p><p>是否添加水印标识，水印位于图片右下角，文案为“AI生成”。</p><ul><li>false：默认值，不添加水印。</li><li>true：添加水印。</li></ul><p>示例值：false。</p><p><strong>seed</strong><code>integer</code>（可选）</p><p>随机数种子，取值范围为<code>[0, 2147483647]</code>。</p><p>未指定时，系统自动生成随机种子。若需提升生成结果的可复现性，建议固定seed值。</p><p>请注意，由于模型生成具有概率性，即使使用相同 seed，也不能保证每次生成结果完全一致。</p></div></section></td><td><a id="sec-tabs-2"></a><section><a id="首尾帧生视频"></a><section><a id="首尾帧生视频-h4"></a><h4>首尾帧生视频</h4><p>根据首帧、尾帧和prompt生成视频。</p><a id="code-block"></a><pre class="language-bash"><code># 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;wan2.2-kf2v-flash&quot;,
    &quot;input&quot;: {
        &quot;first_frame_url&quot;: &quot;https://wanx.alicdn.com/material/20250318/first_frame.png&quot;,
        &quot;last_frame_url&quot;: &quot;https://wanx.alicdn.com/material/20250318/last_frame.png&quot;,
        &quot;prompt&quot;: &quot;写实风格，一只黑色小猫好奇地看向天空，镜头从平视逐渐上升，最后俯拍它的好奇的眼神。&quot;
    },
    &quot;parameters&quot;: {
        &quot;resolution&quot;: &quot;480P&quot;,
        &quot;prompt_extend&quot;: true
    }
}'
</code></pre></section><a id="使用base64"></a><section><a id="使用base64-h4"></a><h4>使用Base64</h4><p>首帧first_frame_url和尾帧last_frame_url参数支持传入图像的 Base64 编码字符串。先下载<a href="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250722/vzjwiv/first_frame_base64.txt">first_frame_base64</a>和<a href="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250722/qbtevh/last_frame_base64.txt">last_frame_base64</a>文件，并将完整内容粘贴至对应参数中。</p><p>格式参见<a href="../model-user-guide/use-cases/legacy-resources/legacy-video-generation/image-to-video-first-and-last-frames-guide.md#69308edfbebnx">如何输入图像</a>。</p><a id="code-block-2"></a><pre class="language-bash"><code># 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;wanx2.1-kf2v-plus&quot;,
    &quot;input&quot;: {
        &quot;first_frame_url&quot;: &quot;data:image/png;base64,GDU7MtCZzEbTbmRZ......&quot;,
        &quot;last_frame_url&quot;: &quot;data:image/png;base64,VBORw0KGgoAAAANSUh......&quot;,
        &quot;prompt&quot;: &quot;写实风格，一只黑色小猫好奇地看向天空，镜头从平视逐渐上升，最后俯拍它的好奇的眼神。&quot;
    },
    &quot;parameters&quot;: {
        &quot;resolution&quot;: &quot;720P&quot;,
        &quot;prompt_extend&quot;: true
    }
}'
</code></pre></section><a id="使用视频特效"></a><section><a id="使用视频特效-h4"></a><h4>使用视频特效</h4><p>必须传入<code>first_frame_url</code>和<code>template</code>，无需传入prompt和last_frame_url。</p><p>不同模型支持不同的特效模板。调用前请查阅<a href="wanx-video-effects-5b23bdd72b8e7944.md">万相-图生视频-视频特效列表</a>，以免调用失败。</p><a id="code-block-3"></a><pre class="language-bash"><code># 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;wanx2.1-kf2v-plus&quot;,
    &quot;input&quot;: {
        &quot;first_frame_url&quot;: &quot;https://ty-yuanfang.oss-cn-hangzhou.aliyuncs.com/lizhengjia.lzj/tmp/11.png&quot;,
        &quot;template&quot;: &quot;hanfu-1&quot;
    },
    &quot;parameters&quot;: {
        &quot;resolution&quot;: &quot;720P&quot;,
        &quot;prompt_extend&quot;: true
    }
}'
</code></pre></section><a id="使用反向提示词"></a><section><a id="使用反向提示词-h4"></a><h4>使用反向提示词</h4><p>通过 negative_prompt 指定生成的视频避免出现“人物”元素。</p><a id="code-block-4"></a><pre class="language-bash"><code># 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;wanx2.1-kf2v-plus&quot;,
    &quot;input&quot;: {
        &quot;first_frame_url&quot;: &quot;https://wanx.alicdn.com/material/20250318/first_frame.png&quot;,
        &quot;last_frame_url&quot;: &quot;https://wanx.alicdn.com/material/20250318/last_frame.png&quot;,
        &quot;prompt&quot;: &quot;写实风格，一只黑色小猫好奇地看向天空，镜头从平视逐渐上升，最后俯拍它的好奇的眼神。&quot;,
        &quot;negative_prompt&quot;: &quot;人物&quot;
    },
    &quot;parameters&quot;: {
        &quot;resolution&quot;: &quot;720P&quot;,
        &quot;prompt_extend&quot;: true
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

> **说明**
>
> -   **轮询建议**：视频生成过程约需数分钟，建议采用**轮询**机制，并设置合理的查询间隔（如 15 秒）来获取结果。
> -   **任务状态流转**：PENDING（排队中）→ RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。
> -   **结果链接**：任务成功后返回视频链接，有效期为 **24 小时**。建议在获取链接后立即下载并转存至永久存储（如[阿里云 OSS](https://help.aliyun.com/zh/oss/user-guide/what-is-oss)）。
> -   **task\_id 有效期**：**24小时**，超时后将无法查询结果，接口将返回任务状态为`UNKNOWN`。
> -   **RPS 限制**：查询接口默认RPS为20。如需更高频查询或事件通知，建议[配置异步任务回调](../model-api-reference/more-about-models/async-task-api.md)。
> -   **更多操作**：如需批量查询、取消任务等操作，请参见[管理异步任务](../model-api-reference/more-about-models/manage-asynchronous-tasks.md)。

<table><tbody><tr><td><a id="a9e0408c70ylw"></a><h4>请求参数</h4><a id="2d2fb41da6idy"></a><h5>请求头（Headers）</h5><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><a id="031d8a0fafqhp"></a><h5>URL路径参数（Path parameters）</h5><p><strong>task_id</strong> <code>string</code><strong>（必选）</strong></p><p>任务ID。</p></td><td><a id="sec-tabs-5"></a><section><a id="查询任务结果"></a><section><a id="查询任务结果-h4"></a><h4>查询任务结果</h4><p>请将<code>86ecf553-d340-4e21-xxxxxxxxx</code>替换为真实的task_id。</p><blockquote><p>若使用新加坡地域的模型，需将base_url替换为https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/tasks/86ecf553-d340-4e21-xxxxxxxxx，其中{WorkspaceId}需替换为真实的业务空间ID。</p></blockquote><a id="code-block-7"></a><pre class="language-bash"><code>curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/86ecf553-d340-4e21-xxxxxxxxx \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="810682d979i8q"></a><h4>响应参数</h4><p><strong>output</strong><code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值-2"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section><strong>轮询过程中的状态流转：</strong><ul><li>PENDING（排队中） → RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。</li><li>初次查询状态通常为 PENDING（排队中）或 RUNNING（处理中）。</li><li>当状态变为 SUCCEEDED 时，响应中将包含生成的视频URL。</li><li>若状态为 FAILED，请检查错误信息并重试。</li><li>若状态为 CANCELED，表示任务已取消，如需继续请重新提交任务。</li><li>若状态为 UNKNOWN，表示任务不存在或状态未知，可能在 task_id 不存在或超过 24 小时有效期后出现。</li></ul><p><strong>submit_time</strong> <code>string</code></p><p>任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>scheduled_time</strong> <code>string</code></p><p>任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>end_time</strong> <code>string</code></p><p>任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>video_url</strong><code>string</code></p><p>视频URL。仅在 task_status 为 SUCCEEDED 时返回。</p><p>链接有效期24小时，可通过此URL下载视频。视频格式为MP4（H.264 编码）。</p><p><strong>orig_prompt</strong> <code>string</code></p><p>原始输入的prompt，对应请求参数<code>prompt</code>。</p><p><strong>actual_prompt</strong> <code>string</code></p><p>开启 prompt 智能改写后，返回实际使用的优化后 prompt。若未开启该功能，则不返回此字段。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../model-api-reference/preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../model-api-reference/preparations/error-code.md">错误码</a>。</p></div></section><p><strong>usage</strong> <code>object</code></p><p>输出信息统计。只对成功的结果计数。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>video_duration</strong> <code>integer</code></p><p>生成视频的时长，单位秒。枚举值为5。计费公式：费用 = 视频秒数 × 单价。</p><p><strong>video_count</strong> <code>integer</code></p><p>生成视频的数量。固定为1。</p><p><strong>video_ratio</strong> <code>string</code></p><p>当前仅当2.1模型返回该值。生成视频的比例，固定为standard。</p><p><strong>SR</strong> <code>integer</code></p><p>当前仅当2.2模型返回该值。生成视频的分辨率档位，枚举值为480、720、1080。</p></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p></td><td><a id="sec-tabs-6"></a><section><a id="任务执行成功"></a><section><a id="任务执行成功-h4"></a><h4>任务执行成功</h4><p>视频URL仅保留24小时，超时后会被自动清除，请及时保存生成的视频。</p><a id="code-block-8"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;ec016349-6b14-9ad6-8009-xxxxxx&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;3f21a745-9f4b-4588-b643-xxxxxx&quot;,
        &quot;task_status&quot;: &quot;SUCCEEDED&quot;,
        &quot;submit_time&quot;: &quot;2025-04-18 10:36:58.394&quot;,
        &quot;scheduled_time&quot;: &quot;2025-04-18 10:37:13.802&quot;,
        &quot;end_time&quot;: &quot;2025-04-18 10:45:23.004&quot;,
        &quot;video_url&quot;: &quot;https://dashscope-result-wlcb.oss-cn-wulanchabu.aliyuncs.com/xxx.mp4?xxxxx&quot;,
        &quot;orig_prompt&quot;: &quot;写实风格，一只黑色小猫好奇地看向天空，镜头从平视逐渐上升，最后俯拍它的好奇的眼神。&quot;,
        &quot;actual_prompt&quot;: &quot;写实风格，一只黑色小猫好奇地看向天空，镜头从平视逐渐上升，最后俯拍它的好奇的眼神。小猫的黄色眼睛明亮有神，毛发光滑，胡须清晰可见。背景是简单的浅色墙面，突显小猫的黑色身影。近景特写，强调小猫的表情变化和眼神细节。&quot;
    },
    &quot;usage&quot;: {
        &quot;video_duration&quot;: 5,
        &quot;video_count&quot;: 1,
        &quot;SR&quot;: 480
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

<a id="db17b3098c2iv"></a>

## DashScope SDK调用

SDK 的参数命名与[HTTP接口](../model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)基本一致，参数结构根据语言特性进行封装。

由于图生视频任务耗时较长（通常为1-5分钟），SDK 在底层封装了 HTTP 异步调用流程，支持同步、异步两种调用方式。

> 具体耗时受限于排队任务数和服务执行情况，请在获取结果时耐心等待。

<a id="python-sdk调用"></a>

<a id="a3ad9a3b6d9if"></a>

### Python SDK调用

> **重要**
>
> 请确保 DashScope Python SDK 版本**不低于**2.0.1，再运行以下代码。
>
> 若版本过低，可能会触发 “url error, please check url!” 等错误。请参考[安装SDK](../model-api-reference/preparations/install-sdk.md)进行更新。

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

<a id="示例代码"></a>

<a id="f2b1639e488og"></a>

#### 示例代码

<a id="sec-tabs-8"></a>

<a id="同步调用"></a>

<a id="同步调用-h4"></a>

#### 同步调用

本示例展示三种图像输入方式：公网URL、Base64编码、本地文件路径。

<a id="3cd4969b00193"></a>

##### 请求示例

<a id="code-block-11"></a>

```python
import base64
import os
import mimetypes
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

# 【方式一】使用公网图片 URL
first_frame_url = "https://wanx.alicdn.com/material/20250318/first_frame.png"
last_frame_url = "https://wanx.alicdn.com/material/20250318/last_frame.png"

# 【方式二】使用本地文件（支持绝对路径和相对路径）
# 格式要求：file:// + 文件路径
# 示例（绝对路径）：
# first_frame_url = "file://" + "/path/to/your/first_frame.png"  # Linux/macOS
# last_frame_url = "file://" + "C:/path/to/your/last_frame.png"  # Windows
# 示例（相对路径）：
# first_frame_url = "file://" + "./first_frame.png"              # 以实际路径为准
# last_frame_url = "file://" + "./last_frame.png"                # 以实际路径为准

# 【方式三】使用Base64编码的图片
# first_frame_url = encode_file("./first_frame.png")            # 以实际路径为准
# last_frame_url = encode_file("./last_frame.png")              # 以实际路径为准

def sample_sync_call_kf2v():
    print('please wait...')
    # generate 为一步式调用（提交任务并等待完成），返回已完成的 Job
    # first_frame_url / last_frame_url 为 input 段字段，不在具名签名内，经 extra_input 透传
    try:
        job = client.videos.generate(model="wan2.2-kf2v-flash",
                                     prompt="写实风格，一只黑色小猫好奇地看向天空，镜头从平视逐渐上升，最后俯拍它的好奇的眼神。",
                                     extra_input={'first_frame_url': first_frame_url,
                                                  'last_frame_url': last_frame_url},
                                     resolution="720P",
                                     prompt_extend=True)
        print(job)
        print(job.video_url)
    except DashScopeError as e:
        print(f"HTTP返回码：{e.status_code}")
        print(f"错误码：{e.code}")
        print(f"错误信息：{e.message}")
        print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")

if __name__ == '__main__':
    sample_sync_call_kf2v()
```

<a id="0c0533477emwb"></a>

##### 响应示例

> video\_url 有效期24小时，请及时下载视频。

<a id="code-block-12"></a>

```json
{
    "request_id": "efa545b3-f95c-9e3a-a3b6-xxxxxx",
    "task_id": "721164c6-8619-4a35-a6d9-xxxxxx",
    "status": "SUCCEEDED",
    "video_url": "https://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/xxx.mp4?xxxxx",
    "task_metrics": {
        "TOTAL": 1,
        "SUCCEEDED": 1,
        "FAILED": 0
    },
    "usage": {
        "video_count": 1,
        "video_duration": 5,
        "video_ratio": "standard"
    }
}
```

<a id="异步调用"></a>

<a id="异步调用-h4"></a>

#### 异步调用

本示例展示异步调用方式。该方式立即返回任务 ID，可通过 fetch 查询状态，或调用 wait 等待完成（内部自动轮询）。

<a id="b994ca9918t7e"></a>

##### 请求示例

<a id="code-block-13"></a>

```python
import os
import dashscope
from dashscope import DashScopeError

# 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

```

<a id="java-sdk调用"></a>

<a id="589b80853e6rn"></a>

### Java SDK调用

> **重要**
>
> 请确保 DashScope Java SDK 版本**不低于**`2.20.9`，再运行以下代码。
>
> 若版本过低，可能会触发 “url error, please check url!” 等错误。请参考[安装SDK](../model-api-reference/preparations/install-sdk.md)进行更新。

<a id="示例代码-2"></a>

<a id="8287893d0cod7"></a>

#### 示例代码

<a id="sec-tabs-9"></a>

<a id="同步调用-2"></a>

<a id="同步调用-2-h4"></a>

#### 同步调用

本示例展示同步调用方式，并支持三种图像输入方式：公网URL、Base64编码、本地文件路径。

<a id="3e3609efb9rhl"></a>

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
import com.alibaba.dashscope.utils.Constants;
import com.alibaba.dashscope.utils.JsonUtils;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Base64;
import java.util.HashMap;
import java.util.Map;

/**
 * 环境要求
 *      dashscope java SDK >= 2.20.9
 * 更新maven依赖:
 *      https://mvnrepository.com/artifact/com.alibaba/dashscope-sdk-java
 */
public class Kf2vSync {

    static {
        // 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。

```

<a id="异步调用-2"></a>

<a id="异步调用-2-h4"></a>

#### 异步调用

本示例展示异步调用方式。该方式会立即返回任务ID，需要自行轮询或等待任务完成。

<a id="2fc30f223b9py"></a>

##### 请求示例

<a id="code-block-15"></a>

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

/**
 * 环境要求
 *      dashscope java SDK >= 2.20.9
 * 更新maven依赖:
 *      https://mvnrepository.com/artifact/com.alibaba/dashscope-sdk-java
 */

public class Kf2vAsync {

    static {
        // 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。

```

<a id="使用限制"></a>

<a id="445b4bb8acqle"></a>

## 使用限制

-   **数据时效**：任务`task_id`和 视频`video_url`均只保留 24 小时，过期后将无法查询或下载。
-   **音频支持**：当前仅支持生成无声视频，不支持音频输出。如有需要，可通过[语音合成](../model-api-reference/audio-api-directory/speech-recognition-api-reference.md)生成音频。
-   **内容审核**：输入prompt 和图像、输出视频均会经过内容安全审核，含违规内容将返回 “IPInfringementSuspect”或“DataInspectionFailed”错误，详情请参见[错误码](../model-api-reference/preparations/error-code.md)。

<a id="错误码"></a>

<a id="0d0a562d05nkh"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](../model-api-reference/preparations/error-code.md)进行解决。

<a id="常见问题"></a>

<a id="2b6ac4aea9h5n"></a>

## 常见问题

<a id="q-如何生成特定宽高比-如3-4-的视频"></a>

<a id="da90d99af1c8v"></a>

#### Q：如何生成特定宽高比（如3:4）的视频？

**A：** 输出视频的宽高比由**输入首帧图像（first\_frame\_url）**决定，但**无法保证精确比例**（如严格3:4），会存在一定偏差。

-   **为什么会有偏差？**
    
    模型会以输入图像的比例为基准，结合设置的分辨率档位（resolution）总像素，自动计算出最接近的合法分辨率。由于要求视频的长和宽必须是 16 的倍数，模型会对最终分辨率做微调，因此无法保证输出比例严格等于 3:4，但会非常接近。
    
    -   例如：输入图像750×1000（宽高比 3:4 = 0.75），并设置 resolution = "720P"（目标总像素约 92 万），实际输出816×1104（宽高比 ≈ 0.739，总像素约90万）。
-   **实践建议**：
    
    -   **输入控制**：尽量使用与目标比例一致的图片作为首帧输入。
    -   **后期处理**：如果您对比例有严格要求，建议在视频生成后，使用编辑工具进行简单的裁剪或黑边填充。

<a id="q-如何获取视频存储的访问域名白名单"></a>

<a id="a2d8df6eeabd3"></a>

### Q：如何获取视频存储的访问域名白名单？

A： 模型生成的视频存储于阿里云OSS，API将返回一个临时的公网URL。**若需要对该下载地址进行防火墙白名单配置**，请注意：由于底层存储会根据业务情况进行动态变更，为避免过期信息影响访问，文档不提供固定的OSS域名白名单。如有安全管控需求，请联系客户经理获取最新OSS域名列表。
