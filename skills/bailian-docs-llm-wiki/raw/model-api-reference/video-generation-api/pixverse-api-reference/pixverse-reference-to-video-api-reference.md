# 爱诗-参考生视频API参考

爱诗-参考生视频模型支持传入多张参考图片或视频，通过 文本提示词 描述场景，将素材中的主体角色融合生成一段流畅的视频。

> **重要**
>
> 本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。

<a id="服务开通"></a>

<a id="8bb48973d87d6"></a>

## 服务开通

1.  前往[阿里云百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)，搜索 **PixVerse**，找到 PixVerse 模型卡片，单击**立即开通**；
2.  在弹窗内确认开通及授权。

<a id="适用范围"></a>

<a id="pvr003a0h2scp"></a>

## 适用范围

为确保调用成功，请务必保证**模型、Endpoint URL 和 API Key 均属于同一地域**。跨地域调用将会失败。

-   [**选择模型**](../../../model-user-guide/model-experience/image-and-video-generation/video-generate-edit-model.md)：确认模型所属的地域。
-   **选择 URL**：选择对应的地域 Endpoint URL，支持HTTP URL或 DashScope SDK URL。
-   **配置 API Key**：选择地域并[获取与配置 API Key](../../preparations/get-api-key.md)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

<a id="http调用"></a>

<a id="pvr101a0h2http"></a>

## HTTP调用

由于参考生视频任务耗时较长（通常为1-5分钟），API采用异步调用。整个流程包含 **"创建任务 -> 轮询获取"** 两个核心步骤，具体如下：

<a id="步骤1-创建任务获取任务id"></a>

<a id="pvr111a0h4stp1"></a>

### 步骤1：创建任务获取任务ID

**北京地域**：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

> **说明**
>
> -   创建成功后，使用接口返回的 `task_id` 查询结果，task\_id 有效期为 24 小时。**请勿重复创建任务**，轮询获取即可。
> -   新手指引请参见[Postman](https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api)。

<table><tbody><tr><td><a id="pvr123a0h4reqp"></a><h4>请求参数</h4><a id="pvr144a0h5hdr1"></a><h5>请求头（Headers）</h5><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><p><strong>X-DashScope-Async</strong><code>string</code><strong>（必选）</strong></p><p>异步处理配置参数。HTTP请求只支持异步，<strong>必须设置为</strong><code>enable</code>。</p><div><div><p><strong>重要</strong>缺少此请求头将报错：“current user api does not support synchronous calls”。</p></div></div><a id="pvr156a0h5body"></a><h5>请求体（Request Body）</h5><p><strong>model</strong> <code>string</code> <strong>（必选）</strong></p><p>模型名称。模型输出规格请参见<a href="../../../model-user-guide/model-experience/image-and-video-generation/video-generate-edit-model.md">模型列表</a>。</p><p>可选值：</p><ul><li>pixverse/pixverse-v6-r2v-omni</li><li>pixverse/pixverse-c1-r2v</li><li>pixverse/pixverse-v6-r2v</li><li>pixverse/pixverse-v5.6-r2v</li></ul><a id="accordion-模型选型"></a><section><p>模型选型</p><div><ul><li>需要图片+视频融合参考生成时，推荐选用 <strong>v6-r2v-omni</strong>，支持同时传入参考图片和参考视频。</li><li>针对打斗、法术特效及高速运动等动态场景以及多宫格场景，推荐选用 <strong>c1</strong>。</li><li>通用场景推荐使用<strong>v6</strong>，<strong>v5.6</strong>建议直接升级至v6。</li></ul></div></section><p><strong>input</strong> <code>object</code> <strong>（必选）</strong></p><p>输入的基本信息，包括参考图片和提示词。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>prompt</strong> <code>string</code> <strong>（必选）</strong></p><p>文本提示词。用来描述生成视频中期望包含的元素和视觉特点。</p><p>支持中英文，每个汉字/字母占一个字符，字符编码为UTF-8，超过部分会自动截断。</p><ul><li>pixverse/pixverse-v6-r2v-omni：不超过5000个字符。</li><li>pixverse/pixverse-c1-r2v：不超过5000个字符。</li><li>pixverse/pixverse-v6-r2v：不超过2048个字符。</li><li>pixverse/pixverse-v5.6-r2v：不超过2048个字符。</li></ul><p>图片引用说明：当在 media 参数中传入参考图时，可以通过 <code>@ref_name</code>在prompt中直接引用该图片。</p><ul><li>media 中设置的 ref_name 在同一请求内必须全局唯一，且须与 prompt 中的引用一一对应。</li><li>书写规范：必须在 <code>@ref_name</code> 后保留一个空格作为分隔。</li></ul><p>示例值：</p><ul><li>普通提示词：男人坐在靠窗的椅子上，手持吉他，在咖啡厅旁演奏一首舒缓的美国乡村民谣。</li><li>含引用的提示词：@男人 坐在靠窗的椅子上，手持@吉他 ，在@咖啡厅 旁演奏一首舒缓的美国乡村民谣。</li></ul><p><strong>media</strong> <code>array</code> <strong>（必选）</strong></p><p>媒体素材列表，用于指定视频生成所需的参考图像和视频。</p><p>数组的每个元素为一个媒体对象，包含 <code>type</code>和 <code>url</code>字段。</p><a id="accordion-元素属性"></a><section><p>元素属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>媒体素材类型。可选值：</p><ul><li><code>image_url</code>：图像URL。</li><li><code>video_url</code>：视频URL（仅 pixverse/pixverse-v6-r2v-omni 支持）。</li></ul><p>素材数量限制：</p><ul><li>图像数量：pixverse/pixverse-v6-r2v-omni 最多10张，其他模型最多7张。</li><li>视频数量（仅 omni）：1～2个。</li></ul><p><strong>url</strong> <code>string</code> <strong>（必选）</strong></p><p>媒体素材URL。素材包括图像、视频（视频仅 omni 模型支持）。</p><a id="accordion-传入图像-type-image-url"></a><section><p>传入图像（type=image_url）</p><div><p>参考图像URL，必须为公网可访问的 URL。</p><ul><li>支持 HTTP 或 HTTPS 协议。</li><li>示例值：<a href="https://xxx/xxx.jpg"></a><a href="https://xxx/xxx.jpg">https://xxx/xxx.jpg</a>。</li></ul><p>图像限制：</p><ul><li>格式：JPG、PNG、WEBP。</li><li>分辨率：图像的宽度和高度均不超过10000像素。</li><li>文件大小：不超过20MB。</li></ul></div></section><a id="accordion-传入视频-type-video-url-仅-omni-模型"></a><section><p>传入视频（type=video_url，仅 omni 模型）</p><div><p>参考视频URL，必须为公网可访问的 URL。</p><ul><li>支持 HTTP 或 HTTPS 协议。</li><li>示例值：<a href="https://xxx/xxx.mp4"></a><a href="https://xxx/xxx.mp4">https://xxx/xxx.mp4</a>。</li></ul><p>视频限制：</p><ul><li>格式：MP4、MOV。</li><li>分辨率：长边不超过1920像素。</li><li>文件大小：单个视频不超过50MB。</li><li>时长：两个视频总时长不超过15秒。</li></ul></div></section><p><strong>ref_name</strong> <code>string</code> （可选）</p><p>参考图片或视频中主体的名称标识，用于在prompt中通过<code>@ref_name</code>引用。长度不超过30个字符。</p></div></section></div></section><p><strong>parameters</strong> <code>object</code> <strong>（必选）</strong></p><p>视频生成参数。如设置视频分辨率、时长、是否生成音频等。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>resolution</strong> <code>string</code> <strong>（omni 模型必选）</strong></p><p>生成视频的分辨率档位。仅 pixverse/pixverse-v6-r2v-omni 使用此参数。</p><p>可选值：</p><ul><li><code>360P</code></li><li><code>540P</code></li><li><code>720P</code></li><li><code>1080P</code></li></ul><p><strong>aspect_ratio</strong> <code>string</code> <strong>（omni 模型必选）</strong></p><p>生成视频的宽高比。仅 pixverse/pixverse-v6-r2v-omni 使用此参数。</p><p>可选值：</p><ul><li><code>auto</code>：自动采用第一个图片或视频的宽高比。</li><li><code>16:9</code></li><li><code>4:3</code></li><li><code>1:1</code></li><li><code>3:4</code></li><li><code>9:16</code></li><li><code>3:2</code></li><li><code>2:3</code></li><li><code>21:9</code></li></ul><p><strong>size</strong> <code>string</code> <strong>（c1/v6/v5.6 模型必选）</strong></p><p>生成视频的分辨率，格式为<code>宽*高</code>的像素值。不支持 pixverse/pixverse-v6-r2v-omni 模型。</p><p>不同分辨率档位对应的可选值见下方表格。</p><a id="accordion-pixverse-pixverse-c1-r2v模型"></a><section><p>pixverse/pixverse-c1-r2v模型</p><div><table><tbody><tr><td><p>分辨率档位</p></td><td><p>宽高比</p></td><td><p>size取值（宽*高）</p></td></tr><tr><td rowspan="8"><p>360P</p></td><td><p>16:9</p></td><td><p>640*360</p></td></tr><tr><td><p>4:3</p></td><td><p>640*480</p></td></tr><tr><td><p>1:1</p></td><td><p>640*640</p></td></tr><tr><td><p>3:4</p></td><td><p>480*640</p></td></tr><tr><td><p>9:16</p></td><td><p>360*640</p></td></tr><tr><td><p>3:2</p></td><td><p>640*432</p></td></tr><tr><td><p>2:3</p></td><td><p>432*640</p></td></tr><tr><td><p>21:9</p></td><td><p>640*288</p></td></tr><tr><td rowspan="8"><p>540P</p></td><td><p>16:9</p></td><td><p>1024*576</p></td></tr><tr><td><p>4:3</p></td><td><p>1024*768</p></td></tr><tr><td><p>1:1</p></td><td><p>1024*1024</p></td></tr><tr><td><p>3:4</p></td><td><p>768*1024</p></td></tr><tr><td><p>9:16</p></td><td><p>576*1024</p></td></tr><tr><td><p>3:2</p></td><td><p>1024*688</p></td></tr><tr><td><p>2:3</p></td><td><p>688*1024</p></td></tr><tr><td><p>21:9</p></td><td><p>1024*448</p></td></tr><tr><td rowspan="8"><p>720P</p></td><td><p>16:9</p></td><td><p>1280*720</p></td></tr><tr><td><p>4:3</p></td><td><p>1108*832</p></td></tr><tr><td><p>1:1</p></td><td><p>960*960</p></td></tr><tr><td><p>3:4</p></td><td><p>832*1108</p></td></tr><tr><td><p>9:16</p></td><td><p>720*1280</p></td></tr><tr><td><p>3:2</p></td><td><p>1200*800</p></td></tr><tr><td><p>2:3</p></td><td><p>800*1200</p></td></tr><tr><td><p>21:9</p></td><td><p>1280*560</p></td></tr><tr><td rowspan="8"><p>1080P</p></td><td><p>16:9</p></td><td><p>1920*1080</p></td></tr><tr><td><p>4:3</p></td><td><p>1664*1248</p></td></tr><tr><td><p>1:1</p></td><td><p>1440*1440</p></td></tr><tr><td><p>3:4</p></td><td><p>1248*1664</p></td></tr><tr><td><p>9:16</p></td><td><p>1080*1920</p></td></tr><tr><td><p>3:2</p></td><td><p>1776*1184</p></td></tr><tr><td><p>2:3</p></td><td><p>1184*1776</p></td></tr><tr><td><p>21:9</p></td><td><p>1920*832</p></td></tr></tbody></table></div></section><a id="accordion-pixverse-pixverse-v6-r2v模型"></a><section><p>pixverse/pixverse-v6-r2v模型</p><div><table><tbody><tr><td><p>分辨率档位</p></td><td><p>宽高比</p></td><td><p>size取值（宽*高）</p></td></tr><tr><td rowspan="8"><p>360P</p></td><td><p>16:9</p></td><td><p>640*360</p></td></tr><tr><td><p>4:3</p></td><td><p>640*480</p></td></tr><tr><td><p>1:1</p></td><td><p>640*640</p></td></tr><tr><td><p>3:4</p></td><td><p>480*640</p></td></tr><tr><td><p>9:16</p></td><td><p>360*640</p></td></tr><tr><td><p>3:2</p></td><td><p>640*432</p></td></tr><tr><td><p>2:3</p></td><td><p>432*640</p></td></tr><tr><td><p>21:9</p></td><td><p>640*288</p></td></tr><tr><td rowspan="8"><p>540P</p></td><td><p>16:9</p></td><td><p>1024*576</p></td></tr><tr><td><p>4:3</p></td><td><p>1024*768</p></td></tr><tr><td><p>1:1</p></td><td><p>1024*1024</p></td></tr><tr><td><p>3:4</p></td><td><p>768*1024</p></td></tr><tr><td><p>9:16</p></td><td><p>576*1024</p></td></tr><tr><td><p>3:2</p></td><td><p>1024*688</p></td></tr><tr><td><p>2:3</p></td><td><p>688*1024</p></td></tr><tr><td><p>21:9</p></td><td><p>1024*448</p></td></tr><tr><td rowspan="8"><p>720P</p></td><td><p>16:9</p></td><td><p>1280*720</p></td></tr><tr><td><p>4:3</p></td><td><p>1108*832</p></td></tr><tr><td><p>1:1</p></td><td><p>960*960</p></td></tr><tr><td><p>3:4</p></td><td><p>832*1108</p></td></tr><tr><td><p>9:16</p></td><td><p>720*1280</p></td></tr><tr><td><p>3:2</p></td><td><p>1200*800</p></td></tr><tr><td><p>2:3</p></td><td><p>800*1200</p></td></tr><tr><td><p>21:9</p></td><td><p>1280*560</p></td></tr><tr><td rowspan="8"><p>1080P</p></td><td><p>16:9</p></td><td><p>1920*1080</p></td></tr><tr><td><p>4:3</p></td><td><p>1664*1248</p></td></tr><tr><td><p>1:1</p></td><td><p>1440*1440</p></td></tr><tr><td><p>3:4</p></td><td><p>1248*1664</p></td></tr><tr><td><p>9:16</p></td><td><p>1080*1920</p></td></tr><tr><td><p>3:2</p></td><td><p>1776*1184</p></td></tr><tr><td><p>2:3</p></td><td><p>1184*1776</p></td></tr><tr><td><p>21:9</p></td><td><p>1920*832</p></td></tr></tbody></table></div></section><a id="accordion-pixverse-pixverse-v5-6-r2v模型-建议升级至v6"></a><section><p>pixverse/pixverse-v5.6-r2v模型（建议升级至v6）</p><div><table><tbody><tr><td><p>分辨率档位</p></td><td><p>宽高比</p></td><td><p>size取值（宽*高）</p></td></tr><tr><td rowspan="5"><p>360P</p></td><td><p>16:9</p></td><td><p>640*360</p></td></tr><tr><td><p>4:3</p></td><td><p>640*480</p></td></tr><tr><td><p>1:1</p></td><td><p>640*640</p></td></tr><tr><td><p>3:4</p></td><td><p>480*640</p></td></tr><tr><td><p>9:16</p></td><td><p>360*640</p></td></tr><tr><td rowspan="5"><p>540P</p></td><td><p>16:9</p></td><td><p>1024*576</p></td></tr><tr><td><p>4:3</p></td><td><p>1024*768</p></td></tr><tr><td><p>1:1</p></td><td><p>1024*1024</p></td></tr><tr><td><p>3:4</p></td><td><p>768*1024</p></td></tr><tr><td><p>9:16</p></td><td><p>576*1024</p></td></tr><tr><td rowspan="5"><p>720P</p></td><td><p>16:9</p></td><td><p>1280*720</p></td></tr><tr><td><p>4:3</p></td><td><p>1108*830</p></td></tr><tr><td><p>1:1</p></td><td><p>960*960</p></td></tr><tr><td><p>3:4</p></td><td><p>830*1108</p></td></tr><tr><td><p>9:16</p></td><td><p>720*1280</p></td></tr><tr><td rowspan="5"><p>1080P</p></td><td><p>16:9</p></td><td><p>1920*1080</p></td></tr><tr><td><p>4:3</p></td><td><p>1662*1246</p></td></tr><tr><td><p>1:1</p></td><td><p>1440*1440</p></td></tr><tr><td><p>3:4</p></td><td><p>1246*1662</p></td></tr><tr><td><p>9:16</p></td><td><p>1080*1920</p></td></tr></tbody></table></div></section><p>示例值：1280*720。</p><p><strong>duration</strong> <code>integer</code> <strong>（必选）</strong></p><div><div><p><strong>重要</strong>duration直接影响费用，请在调用前确认<a href="../../../model-user-guide/test-1/model-pricing.md#pxr002a0h3001">爱诗-参考生视频</a>。</p></div></div><p>生成视频的时长，单位为秒。</p><p>可选值：</p><ul><li><p>pixverse/pixverse-v6-r2v-omni：</p><ul><li>有视频参考时：必须填 <code>0</code>，系统将自动取输入视频中的最长时长。</li><li>仅图片参考时：取值范围为[1, 15]之间的整数。</li></ul></li><li><p>pixverse/pixverse-c1-r2v：取值范围为[1, 15]之间的整数。</p></li><li><p>pixverse/pixverse-v6-r2v：取值范围为[1, 15]之间的整数。</p></li><li><p>pixverse/pixverse-v5.6-r2v：</p><ul><li>当 size 为 360P / 540P / 720P 对应的所有分辨率时：取值为5、8、10。</li><li>当size为1080P对应的所有分辨率时：取值为5、8。</li></ul></li></ul><p>示例值：5。</p><p><strong>audio</strong> <code>boolean</code> （可选）</p><div><div><p><strong>重要</strong>audio直接影响费用，请在调用前确认<a href="../../../model-user-guide/test-1/model-pricing.md#pxr002a0h3001">爱诗-参考生视频</a>。</p></div></div><p>是否生成有声视频。开启后模型将根据视频内容自动生成匹配的背景音乐或音效。</p><ul><li><code>false</code>：默认值，输出无声视频。</li><li><code>true</code>：输出有声视频。</li></ul><p>示例值：false。</p><p><strong>watermark</strong> <code>boolean</code> （可选）</p><p>是否添加水印标识，水印位于视频右下角，文案固定为“AI生成”。</p><ul><li><code>false</code>：默认值，不添加水印。</li><li><code>true</code>：添加水印。</li></ul><p>示例值：false。</p><p><strong>seed</strong><code>integer</code>（可选）</p><p>随机数种子，取值范围为<code>[0, 2147483647]</code>。</p><p>未指定时，系统自动生成随机种子。若需提升生成结果的可复现性，建议固定seed值。</p><p>请注意，由于模型生成具有概率性，即使使用相同 seed，也不能保证每次生成结果完全一致。</p></div></section></td><td><a id="sec-tabs"></a><section><a id="参考生视频-图片-视频-omni"></a><section><a id="参考生视频-图片-视频-omni-h4"></a><h4>参考生视频（图片+视频，omni）</h4><p>通过 <code>media</code> 传入参考视频和参考图片，使用 <code>resolution</code> 和 <code>aspect_ratio</code> 控制输出分辨率和画面比例。</p><a id="code-block"></a><pre class="language-bash"><code># 调用时请将 {WorkspaceId} 替换为真实的业务空间ID。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;pixverse/pixverse-v6-r2v-omni&quot;,
    &quot;input&quot;: {
        &quot;media&quot;: [
            {
                &quot;type&quot;: &quot;video_url&quot;,
                &quot;url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qigswt/wan-r2v-role2.mp4&quot;,
                &quot;ref_name&quot;: &quot;参考视频&quot;
            },
            {
                &quot;type&quot;: &quot;image_url&quot;,
                &quot;url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260320/knsple/wan-r2v-role-frame.jpg&quot;,
                &quot;ref_name&quot;: &quot;男人&quot;
            },
            {
                &quot;type&quot;: &quot;image_url&quot;,
                &quot;url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/wfjikw/wan-r2v-backgroud5.png&quot;,
                &quot;ref_name&quot;: &quot;咖啡厅&quot;
            }
        ],
        &quot;prompt&quot;: &quot;@男人 在@咖啡厅 中弹吉他 参考@参考视频&quot;
    },
    &quot;parameters&quot;: {
        &quot;resolution&quot;: &quot;720P&quot;,
        &quot;aspect_ratio&quot;: &quot;16:9&quot;,
        &quot;duration&quot;: 0,
        &quot;audio&quot;: true,
        &quot;watermark&quot;: false
    }
}'
</code></pre></section><a id="python-sdk"></a><section><a id="python-sdk-h4"></a><h4>Python SDK</h4><a id="code-block-2"></a><pre class="language-python"><code>import dashscope
import os
from dashscope import DashScopeError

# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;
# 获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
client = dashscope.Client(api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;))

media = [{'type': 'video_url', 'url': 'https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qigswt/wan-r2v-role2.mp4', 'ref_name': '参考视频'}, {'type': 'image_url', 'url': 'https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260320/knsple/wan-r2v-role-frame.jpg', 'ref_name': '男人'}, {'type': 'image_url', 'url': 'https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/wfjikw/wan-r2v-backgroud5.png', 'ref_name': '咖啡厅'}]

def sample_async_call():
    # 异步提交视频生成任务
    # aspect_ratio/audio 为 parameters 段字段，不在具名签名内，经 parameters 透传
    try:
        job = client.videos.jobs.create(model='pixverse/pixverse-v6-r2v-omni',
                                        media=media,
                                        prompt='@男人 在@咖啡厅 中弹吉他 参考@参考视频',
                                        resolution='720P',
                                        duration=0,
                                        watermark=False,
                                        parameters={'aspect_ratio': '16:9',
                                                    'audio': True})
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
</code></pre></section><a id="参考生视频"></a><section><a id="参考生视频-h4"></a><h4>参考生视频</h4><p>通过 <code>media</code> 传入参考图像，设置 <code>size</code> 和 <code>duration</code> 控制视频分辨率和时长。</p><a id="code-block-3"></a><pre class="language-bash"><code># 调用时请将 {WorkspaceId} 替换为真实的业务空间ID。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;pixverse/pixverse-c1-r2v&quot;,
    &quot;input&quot;: {
        &quot;media&quot;: [
            {
                &quot;type&quot;: &quot;image_url&quot;,
                &quot;url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260320/knsple/wan-r2v-role-frame.jpg&quot;
            },
            {
                &quot;type&quot;: &quot;image_url&quot;,
                &quot;url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qpzxps/wan-r2v-object4.png&quot;
            },
            {
                &quot;type&quot;: &quot;image_url&quot;,
                &quot;url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/wfjikw/wan-r2v-backgroud5.png&quot;
            }
        ],
        &quot;prompt&quot;: &quot;男人坐在靠窗的椅子上，手持吉他，在咖啡厅旁演奏一首舒缓的美国乡村民谣&quot;
    },
    &quot;parameters&quot;: {
        &quot;size&quot;: &quot;1280*720&quot;,
        &quot;duration&quot;: 5,
        &quot;audio&quot;: false,
        &quot;watermark&quot;: true
    }
}'
</code></pre></section><a id="参考生视频-使用ref-name"></a><section><a id="参考生视频-使用ref-name-h4"></a><h4>参考生视频（使用ref_name）</h4><p>在 <code>media</code> 传入参考图像，并传入<code>ref_name</code>用于设置参考图像的主体名称。</p><a id="code-block-4"></a><pre class="language-bash"><code># 调用时请将 {WorkspaceId} 替换为真实的业务空间ID。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;pixverse/pixverse-c1-r2v&quot;,
    &quot;input&quot;: {
        &quot;media&quot;: [
            {
                &quot;type&quot;: &quot;image_url&quot;,
                &quot;url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260320/knsple/wan-r2v-role-frame.jpg&quot;,
                &quot;ref_name&quot;: &quot;男人&quot;
            },
            {
                &quot;type&quot;: &quot;image_url&quot;,
                &quot;url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qpzxps/wan-r2v-object4.png&quot;,
                &quot;ref_name&quot;: &quot;吉他&quot;
            },
            {
                &quot;type&quot;: &quot;image_url&quot;,
                &quot;url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/wfjikw/wan-r2v-backgroud5.png&quot;,
                &quot;ref_name&quot;: &quot;咖啡厅&quot;
            }
        ],
        &quot;prompt&quot;: &quot;@男人 坐在靠窗的椅子上，手持@吉他 ，在@咖啡厅 旁演奏一首舒缓的美国乡村民谣&quot;
    },
    &quot;parameters&quot;: {
        &quot;size&quot;: &quot;1280*720&quot;,
        &quot;duration&quot;: 5,
        &quot;audio&quot;: false,
        &quot;watermark&quot;: true
    }
}'
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="pvr379a0h4rsp1"></a><h4>响应参数</h4><p><strong>output</strong> <code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></td><td><a id="sec-tabs-2"></a><section><a id="成功响应"></a><section><a id="成功响应-h4"></a><h4>成功响应</h4><p>请保存 task_id，用于查询任务状态与结果。</p><a id="code-block-5"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
        &quot;task_status&quot;: &quot;PENDING&quot;,
        &quot;task_id&quot;: &quot;0385dc79-5ff8-4d82-bcb6-xxxxxx&quot;
    },
    &quot;request_id&quot;: &quot;4909100c-7b5a-9f92-bfe5-xxxxxx&quot;
}
</code></pre></section><a id="异常响应"></a><section><a id="异常响应-h4"></a><h4>异常响应</h4><p>创建任务失败，请参见<a href="../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-6"></a><pre class="language-json"><code>{
    &quot;code&quot;: &quot;InvalidApiKey&quot;,
    &quot;message&quot;: &quot;No API-key provided.&quot;,
    &quot;request_id&quot;: &quot;7438d53d-6eb8-4596-8835-xxxxxx&quot;
}
</code></pre></section></section></td></tr></tbody></table>

<a id="步骤2-根据任务id查询结果"></a>

<a id="pvr411a0h4stp2"></a>

### 步骤2：根据任务ID查询结果

**北京地域**：`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`

> **说明**
>
> -   **轮询建议**：视频生成过程约需数分钟，建议采用**轮询**机制，并设置合理的查询间隔（如 15 秒）来获取结果。
> -   **任务状态流转**：PENDING（排队中）→ RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。
> -   **task\_id 有效期**：**24小时**，超时后将无法查询结果，接口将返回任务状态为`UNKNOWN`。
> -   **RPS 限制**：查询接口默认RPS为20。如需更高频查询或事件通知，建议[配置异步任务回调](../../more-about-models/async-task-api.md)。
> -   **更多操作**：如需批量查询、取消任务等操作，请参见[管理异步任务](../../more-about-models/manage-asynchronous-tasks.md)。

<table><tbody><tr><td><a id="pvr424a0h4qr01"></a><h4>请求参数</h4><a id="pvr434a0h5qr01"></a><h5>请求头（Headers）</h5><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><a id="pvr440a0h5qr02"></a><h5>URL路径参数（Path parameters）</h5><p><strong>task_id</strong> <code>string</code><strong>（必选）</strong></p><p>任务ID。</p></td><td><a id="sec-tabs-3"></a><section><a id="查询任务结果"></a><section><a id="查询任务结果-h4"></a><h4>查询任务结果</h4><p>将<code>{task_id}</code>完整替换为上一步接口返回的<code>task_id</code>的值。<code>task_id</code>查询有效期为24小时，并请将<code>{WorkspaceId}</code>替换为真实的<a href="../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain">业务空间ID</a>。</p><a id="code-block-7"></a><pre class="language-bash"><code>curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id} \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="pvr448a0h4qrs1"></a><h4>响应参数</h4><p><strong>output</strong><code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值-2"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section><strong>轮询过程中的状态流转：</strong><ul><li>PENDING（排队中） → RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。</li><li>初次查询状态通常为 PENDING（排队中）或 RUNNING（处理中）。</li><li>当状态变为 SUCCEEDED 时，响应中将包含生成的视频URL。</li><li>若状态为 FAILED，请检查错误信息并重试。</li><li>若状态为 CANCELED，表示任务已取消，如需继续请重新提交任务。</li><li>若状态为 UNKNOWN，表示任务不存在或状态未知，可能在 task_id 不存在或超过 24 小时有效期后出现。</li></ul><p><strong>submit_time</strong> <code>string</code></p><p>任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>scheduled_time</strong> <code>string</code></p><p>任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>end_time</strong> <code>string</code></p><p>任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>video_url</strong><code>string</code></p><p>视频URL。仅在 task_status 为 SUCCEEDED 时返回。</p><p>视频格式为MP4（H.264 编码）。视频链接暂无过期时间，但不建议将其作为长期存储依赖，请及时下载。</p><p><strong>orig_prompt</strong> <code>string</code></p><p>原始输入的prompt，对应请求参数<code>prompt</code>。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></div></section><p><strong>usage</strong> <code>object</code></p><p>输出信息统计。只对成功的结果计数。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>duration</strong> <code>integer</code></p><p>生成视频的总视频时长，用于计费。</p><p><strong>size</strong> <code>string</code></p><p>生成视频的分辨率。</p><p><strong>fps</strong> <code>integer</code></p><p>生成视频的帧率。</p><p><strong>SR</strong> <code>string</code></p><p>生成视频的分辨率档位。</p><p><strong>audio</strong> <code>boolean</code></p><p>生成视频是否为有声视频。</p><p><strong>video_count</strong> <code>integer</code></p><p>生成视频的数量。固定为1。</p></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p></td><td><a id="sec-tabs-4"></a><section><a id="任务执行成功"></a><section><a id="任务执行成功-h4"></a><h4>任务执行成功</h4><a id="code-block-8"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;35137489-2862-96cb-b6f2-xxxxxx&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;1469cfc3-3004-4d9e-ab10-xxxxxx&quot;,
        &quot;task_status&quot;: &quot;SUCCEEDED&quot;,
        &quot;submit_time&quot;: &quot;2026-03-10 15:03:25.848&quot;,
        &quot;scheduled_time&quot;: &quot;2026-03-10 15:03:25.884&quot;,
        &quot;end_time&quot;: &quot;2026-03-10 15:04:05.882&quot;,
        &quot;orig_prompt&quot;: &quot;男人坐在靠窗的椅子上，手持吉他，在咖啡厅旁演奏一首舒缓的美国乡村民谣&quot;,
        &quot;video_url&quot;: &quot;https://media.pixverseai.cn/xxxx.mp4&quot;
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
</code></pre></section><a id="任务执行失败"></a><section><a id="任务执行失败-h4"></a><h4>任务执行失败</h4><p>若任务执行失败，task_status将置为 FAILED，并提供错误码和信息。请参见<a href="../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-9"></a><pre class="language-json"><code>{
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

<a id="错误码"></a>

<a id="OajFO"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](../../preparations/error-code.md)进行解决。

<a id="常见问题"></a>

<a id="pvr801a0h2faq1"></a>

## 常见问题

<a id="q-prompt-效果不理想时-如何优化"></a>

<a id="pvr806a0h4fq02"></a>

#### Q: prompt 效果不理想时，如何优化？

A： 可尝试使用 `@ref_name` 作为替代方案。

-   默认做法：直接使用 prompt，模型会自动全局解析参考图内容，适用于大多数常规场景。
-   替代方案：若发现生成效果偏离预期，可通过 `@ref_name`将参考图指定在提示词中，增强生成效果。

<a id="q-如何使用ref-name"></a>

<a id="1736f3617ahla"></a>

#### Q：如何使用ref\_name？

A：`ref_name` 用于建立参考图与提示词的绑定关系。在 `media`数组中为图片设置 `ref_name` 后，prompt 中可通过 `@ref_name`语法引用对应的参考图主体。

-   例如：media 中设置 `"ref_name": "小猫"`，则 prompt 中使用`@小猫`来引用该主体。注意：@小猫后必须保留空格。
-   示例：@小猫 和@小狗 在草地上玩耍。
