# 爱诗-文生视频API参考

爱诗-文生视频模型基于 文本提示词 ，生成一段流畅的视频。

> **重要**
>
> 本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。

<a id="服务开通"></a>

<a id="8bb48973d87d6"></a>

## 服务开通

1.  前往[阿里云百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)，搜索 **PixVerse**，找到 PixVerse 模型卡片，单击**立即开通**；
2.  在弹窗内确认开通及授权。

<a id="适用范围"></a>

<a id="1fd78afa5brlj"></a>

## 适用范围

为确保调用成功，请务必保证**模型、Endpoint URL 和 API Key 均属于同一地域**。跨地域调用将会失败。

-   [**选择模型**](https://bailian.console.aliyun.com/cn-beijing/model/market)：确认模型所属的地域。
-   **选择 URL**：选择对应的地域 Endpoint URL，支持HTTP URL或 DashScope SDK URL。
-   **配置 API Key**：选择地域并[获取与配置 API Key](../../preparations/get-api-key.md)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
-   **安装 SDK**：如需通过SDK进行调用，请[安装DashScope SDK](../../preparations/install-sdk.md)。

> **说明**
>
> 本文的示例代码适用于**华北2（北京）地域**。

<a id="http调用"></a>

<a id="pv101a0h2http"></a>

## HTTP调用

由于文生视频任务耗时较长（通常为1-5分钟），API采用异步调用。整个流程包含 **"创建任务 -> 轮询获取"** 两个核心步骤，具体如下：

<a id="步骤1-创建任务获取任务id"></a>

<a id="pv111a0h4stp1"></a>

### 步骤1：创建任务获取任务ID

**北京地域**：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

> **说明**
>
> -   创建成功后，使用接口返回的 `task_id` 查询结果，task\_id 有效期为 24 小时。**请勿重复创建任务**，轮询获取即可。
> -   新手指引请参见[Postman](https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api)。

<table><tbody><tr><td><a id="pv123a0h4reqp"></a><h4>请求参数</h4><a id="pv142a0h5hdr1"></a><h5>请求头（Headers）</h5><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><p><strong>X-DashScope-Async</strong><code>string</code><strong>（必选）</strong></p><p>异步处理配置参数。HTTP请求只支持异步，<strong>必须设置为</strong><code>enable</code>。</p><div><div><p><strong>重要</strong>缺少此请求头将报错：“current user api does not support synchronous calls”。</p></div></div><a id="pv154a0h5body"></a><h5>请求体（Request Body）</h5><p><strong>model</strong> <code>string</code> <strong>（必选）</strong></p><p>模型名称。</p><p>可选值：</p><ul><li>pixverse/pixverse-v6-max-t2v</li><li>pixverse/pixverse-c1-t2v</li><li>pixverse/pixverse-v6-t2v</li><li>pixverse/pixverse-v5.6-t2v</li></ul><a id="accordion-模型选型"></a><section><p>模型选型</p><div><ul><li>推荐使用 <strong>v6-max</strong>。</li><li>针对打斗、法术特效及高速运动等动态场景，可选 <strong>c1</strong>。</li></ul></div></section><p><strong>input</strong> <code>object</code> <strong>（必选）</strong></p><p>输入的基本信息，如提示词等。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>prompt</strong> <code>string</code> <strong>（必选）</strong></p><p>文本提示词。用来描述生成视频中期望包含的元素和视觉特点。</p><p>支持中英文，每个汉字/字母占一个字符，字符编码为UTF-8，超过部分会自动截断。</p><ul><li>pixverse/pixverse-v6-max-t2v：不超过5000个字符。</li><li>pixverse/pixverse-c1-t2v：不超过5000个字符。</li><li>pixverse/pixverse-v6-t2v：不超过5000个字符。</li><li>pixverse/pixverse-v5.6-t2v：不超过2048个字符。</li></ul></div></section><p><strong>parameters</strong> <code>object</code> <strong>（必选）</strong></p><p>视频生成参数。如设置视频分辨率、时长、是否生成音频等。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>resolution</strong> <code>string</code> <strong>（条件必选）</strong></p><p>使用pixverse/pixverse-v6-max-t2v时必选。</p><div><div><p><strong>重要</strong>resolution直接影响费用，请在调用前确认<a href="../../../model-user-guide/test-1/model-pricing.md#pxt002a0h3001">模型价格</a>。</p></div></div><p>生成视频的分辨率档位。</p><p>可选值：</p><ul><li><code>360P</code></li><li><code>540P</code></li><li><code>720P</code></li><li><code>1080P</code></li></ul><p>视频分辨率由resolution和aspect_ratio确定，无需设置size。</p><p><strong>aspect_ratio</strong> <code>string</code> （可选）</p><p>生成视频的宽高比。</p><p>可选值：</p><ul><li><code>16:9</code>：默认值</li><li><code>4:3</code></li><li><code>1:1</code></li><li><code>3:4</code></li><li><code>9:16</code></li><li><code>3:2</code></li><li><code>2:3</code></li><li><code>21:9</code></li></ul><p><strong>size</strong> <code>string</code> <strong>（条件必选）</strong></p><p>使用pixverse/pixverse-c1-t2v、pixverse/pixverse-v6-t2v、pixverse/pixverse-v5.6-t2v时必选。</p><p>生成视频的分辨率，格式为<code>宽*高</code>的像素值。</p><div><div><p><strong>重要</strong></p><ul><li>size直接影响费用，请在调用前确认<a href="../../../model-user-guide/test-1/model-pricing.md#pxt002a0h3001">模型价格</a>。</li><li>使用pixverse/pixverse-v5.6-t2v模型，若设置<code>size=1808*1808</code>，且duration为8时，实际输出的视频分辨率为<code>1440*1440</code>。</li></ul></div></div><p>不同分辨率档位和宽高比对应的可选值见下方表格。</p><a id="accordion-pixverse-pixverse-c1-t2v-pixverse-pixverse-v6-t2v模型"></a><section><p>pixverse/pixverse-c1-t2v、pixverse/pixverse-v6-t2v模型</p><div><table><tbody><tr><td><p>分辨率档位</p></td><td><p>宽高比</p></td><td><p>size取值（宽*高）</p></td></tr><tr><td rowspan="8"><p>360P</p></td><td><p>16:9</p></td><td><p>640*360</p></td></tr><tr><td><p>4:3</p></td><td><p>640*480</p></td></tr><tr><td><p>1:1</p></td><td><p>640*640</p></td></tr><tr><td><p>3:4</p></td><td><p>480*640</p></td></tr><tr><td><p>9:16</p></td><td><p>360*640</p></td></tr><tr><td><p>3:2</p></td><td><p>640*432</p></td></tr><tr><td><p>2:3</p></td><td><p>432*640</p></td></tr><tr><td><p>21:9</p></td><td><p>640*288</p></td></tr><tr><td rowspan="8"><p>540P</p></td><td><p>16:9</p></td><td><p>1024*576</p></td></tr><tr><td><p>4:3</p></td><td><p>1024*768</p></td></tr><tr><td><p>1:1</p></td><td><p>1024*1024</p></td></tr><tr><td><p>3:4</p></td><td><p>768*1024</p></td></tr><tr><td><p>9:16</p></td><td><p>576*1024</p></td></tr><tr><td><p>3:2</p></td><td><p>1024*688</p></td></tr><tr><td><p>2:3</p></td><td><p>688*1024</p></td></tr><tr><td><p>21:9</p></td><td><p>1024*448</p></td></tr><tr><td rowspan="8"><p>720P</p></td><td><p>16:9</p></td><td><p>1280*720</p></td></tr><tr><td><p>4:3</p></td><td><p>1108*832</p></td></tr><tr><td><p>1:1</p></td><td><p>960*960</p></td></tr><tr><td><p>3:4</p></td><td><p>832*1108</p></td></tr><tr><td><p>9:16</p></td><td><p>720*1280</p></td></tr><tr><td><p>3:2</p></td><td><p>1200*800</p></td></tr><tr><td><p>2:3</p></td><td><p>800*1200</p></td></tr><tr><td><p>21:9</p></td><td><p>1280*560</p></td></tr><tr><td rowspan="8"><p>1080P</p></td><td><p>16:9</p></td><td><p>1920*1080</p></td></tr><tr><td><p>4:3</p></td><td><p>1664*1248</p></td></tr><tr><td><p>1:1</p></td><td><p>1440*1440</p></td></tr><tr><td><p>3:4</p></td><td><p>1248*1664</p></td></tr><tr><td><p>9:16</p></td><td><p>1080*1920</p></td></tr><tr><td><p>3:2</p></td><td><p>1776*1184</p></td></tr><tr><td><p>2:3</p></td><td><p>1184*1776</p></td></tr><tr><td><p>21:9</p></td><td><p>1920*832</p></td></tr></tbody></table></div></section><a id="accordion-pixverse-pixverse-v5-6-t2v模型"></a><section><p>pixverse/pixverse-v5.6-t2v模型</p><div><table><tbody><tr><td><p>分辨率档位</p></td><td><p>宽高比</p></td><td><p>size取值（宽*高）</p></td></tr><tr><td rowspan="5"><p>360P</p></td><td><p>16:9</p></td><td><p>640*360</p></td></tr><tr><td><p>4:3</p></td><td><p>640*480</p></td></tr><tr><td><p>1:1</p></td><td><p>640*640</p></td></tr><tr><td><p>3:4</p></td><td><p>480*640</p></td></tr><tr><td><p>9:16</p></td><td><p>360*640</p></td></tr><tr><td rowspan="5"><p>540P</p></td><td><p>16:9</p></td><td><p>1024*576</p></td></tr><tr><td><p>4:3</p></td><td><p>1024*768</p></td></tr><tr><td><p>1:1</p></td><td><p>1024*1024</p></td></tr><tr><td><p>3:4</p></td><td><p>768*1024</p></td></tr><tr><td><p>9:16</p></td><td><p>576*1024</p></td></tr><tr><td rowspan="5"><p>720P</p></td><td><p>16:9</p></td><td><p>1280*720</p></td></tr><tr><td><p>4:3</p></td><td><p>1280*960</p></td></tr><tr><td><p>1:1</p></td><td><p>1280*1280</p></td></tr><tr><td><p>3:4</p></td><td><p>960*1280</p></td></tr><tr><td><p>9:16</p></td><td><p>720*1280</p></td></tr><tr><td rowspan="5"><p>1080P</p></td><td><p>16:9</p></td><td><p>1920*1080</p></td></tr><tr><td><p>4:3</p></td><td><p>1920*1440</p></td></tr><tr><td><p>1:1</p></td><td><p>1808*1808</p></td></tr><tr><td><p>3:4</p></td><td><p>1440*1920</p></td></tr><tr><td><p>9:16</p></td><td><p>1080*1920</p></td></tr></tbody></table></div></section><p><strong>duration</strong> <code>integer</code> <strong>（必选）</strong></p><div><div><p><strong>重要</strong>duration直接影响费用，按秒计费，请在调用前确认<a href="../../../model-user-guide/test-1/model-pricing.md#pxt002a0h3001">模型价格</a>。</p></div></div><p>生成视频的时长，单位为秒。</p><ul><li><p>pixverse/pixverse-v6-max-t2v：取值范围为[1, 15]之间的整数。</p></li><li><p>pixverse/pixverse-c1-t2v：取值范围为[1, 15]之间的整数。</p></li><li><p>pixverse/pixverse-v6-t2v：取值范围为[1, 15]之间的整数。</p></li><li><p>pixverse/pixverse-v5.6-t2v：</p><ul><li>当 size 为 360P / 540P / 720P 对应的所有分辨率时：取值为5、8、10。</li><li>当size为1080P对应的所有分辨率时：取值为5、8。</li></ul></li></ul><p><strong>audio</strong> <code>boolean</code> （可选）</p><div><div><p><strong>重要</strong>audio直接影响费用，请在调用前确认<a href="../../../model-user-guide/test-1/model-pricing.md#pxt002a0h3001">模型价格</a>。</p></div></div><p>是否生成有声视频。开启后模型将根据视频内容自动生成匹配的背景音乐或音效。</p><ul><li><code>false</code>：默认值，输出无声视频。</li><li><code>true</code>：输出有声视频。</li></ul><p><strong>watermark</strong> <code>boolean</code> （可选）</p><p>是否添加水印标识，水印位于视频右下角，文案固定为“AI生成”。</p><ul><li><code>false</code>：默认值，不添加水印。</li><li><code>true</code>：添加水印。</li></ul><p><strong>shot_type</strong> <code>string</code> （可选）</p><p><strong>支持模型</strong>：pixverse/pixverse-v6-t2v。</p><p>指定生成视频的镜头类型，控制视频是由一个连续镜头还是多镜头组成。</p><ul><li><code>single</code>：默认值，生成单镜头视频。</li><li><code>multi</code>：多镜头，系统会进行智能分镜。</li></ul><p>使用建议：prompt 参数优先级高于 shot_type 。为获得最佳效果，建议此参数设置与 prompt 描述保持一致。</p><ul><li>若想稳定输出单镜头：设置 <code>shot_type=&quot;single&quot;</code> 并在 prompt 中描述单镜头场景。</li><li>若想稳定输出多镜头：设置 <code>shot_type=&quot;multi&quot;</code> 并在 prompt 中描述多镜头场景。</li></ul><p><strong>seed</strong><code>integer</code>（可选）</p><p>随机数种子，取值范围为<code>[0, 2147483647]</code>。</p><p>未指定时，系统自动生成随机种子。若需提升生成结果的可复现性，建议固定seed值。</p><p>请注意，由于模型生成具有概率性，即使使用相同 seed，也不能保证每次生成结果完全一致。</p></div></section></td><td><a id="sec-tabs"></a><section><a id="文生视频-v6-max"></a><section><a id="文生视频-v6-max-h4"></a><h4>文生视频（v6-max）</h4><p>支持模型：pixverse/pixverse-v6-max-t2v。</p><a id="code-block"></a><pre class="language-bash"><code># 调用时请将 {WorkspaceId} 替换为真实的业务空间ID。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;pixverse/pixverse-v6-max-t2v&quot;,
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;下着雨，赛博城市里，一只浣熊在栏杆上行走。突然他眼睛发出蓝光，变身成一架高科技无人机，快速飞离画面。&quot;
    },
    &quot;parameters&quot;: {
        &quot;resolution&quot;: &quot;720P&quot;,
        &quot;aspect_ratio&quot;: &quot;16:9&quot;,
        &quot;duration&quot;: 5,
        &quot;audio&quot;: true,
        &quot;watermark&quot;: true
    }
}'
</code></pre></section><a id="文生视频"></a><section><a id="文生视频-h4"></a><h4>文生视频</h4><p>支持模型：pixverse/pixverse-c1-t2v、pixverse/pixverse-v6-t2v、pixverse/pixverse-v5.6-t2v。</p><a id="code-block-2"></a><pre class="language-bash"><code># 调用时请将 {WorkspaceId} 替换为真实的业务空间ID。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;pixverse/pixverse-c1-t2v&quot;,
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;下着雨，赛博城市里，一只浣熊在栏杆上行走。突然他眼睛发出蓝光，变身成一架高科技无人机，快速飞离画面。&quot;
    },
    &quot;parameters&quot;: {
        &quot;size&quot;: &quot;1280*720&quot;,
        &quot;duration&quot;: 5,
        &quot;watermark&quot;: true
    }
}'
</code></pre></section><a id="文生视频-多镜头"></a><section><a id="文生视频-多镜头-h4"></a><h4>文生视频（多镜头）</h4><a id="sec-tabs-2"></a><section><a id="pixverse-c1"></a><section><a id="pixverse-c1-h4"></a><h4>pixverse-c1</h4><p>支持模型：pixverse/pixverse-c1-t2v。</p><p>在<code>prompt</code>中描述多镜头场景即可，不支持设置 <code>shot_type</code>参数。</p><a id="code-block-3"></a><pre class="language-bash"><code># 调用时请将 {WorkspaceId} 替换为真实的业务空间ID。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;pixverse/pixverse-c1-t2v&quot;,
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;镜头1：模特面向镜头平稳向前漫步；镜头2： 快速切换至中景，展示腰线裁剪与蓝白格纹棉质面料的清爽质感；镜头3： 远景捕捉微风吹拂裙摆的自然动态，画面干净明亮。&quot;
    },
    &quot;parameters&quot;: {
        &quot;size&quot;: &quot;1280*720&quot;,
        &quot;duration&quot;: 5,
        &quot;audio&quot;: true,
        &quot;watermark&quot;: true
    }
}'
</code></pre></section><a id="pixverse-v6"></a><section><a id="pixverse-v6-h4"></a><h4>pixverse-v6</h4><p>支持模型：pixverse/pixverse-v6-t2v。</p><p>在<code>prompt</code>中描述多镜头场景，并设置 <code>shot_type</code> 为<code>multi</code>， 即可生成有声多镜头视频。</p><a id="code-block-4"></a><pre class="language-bash"><code># 调用时请将 {WorkspaceId} 替换为真实的业务空间ID。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;pixverse/pixverse-v6-t2v&quot;,
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;镜头1：模特面向镜头平稳向前漫步；镜头2： 快速切换至中景，展示腰线裁剪与蓝白格纹棉质面料的清爽质感；镜头3： 远景捕捉微风吹拂裙摆的自然动态，画面干净明亮。&quot;
    },
    &quot;parameters&quot;: {
        &quot;size&quot;: &quot;1280*720&quot;,
        &quot;duration&quot;: 5,
        &quot;audio&quot;: true,
        &quot;shot_type&quot;: &quot;multi&quot;,
        &quot;watermark&quot;: true
    }
}'
</code></pre></section></section></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="pv355a0h4rsp1"></a><h4>响应参数</h4><p><strong>output</strong> <code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></td><td><a id="sec-tabs-3"></a><section><a id="成功响应"></a><section><a id="成功响应-h4"></a><h4>成功响应</h4><p>请保存 task_id，用于查询任务状态与结果。</p><a id="code-block-5"></a><pre class="language-json"><code>{
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

<a id="pv401a0h4stp2"></a>

### 步骤2：根据任务ID查询结果

**北京地域**：`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`

> **说明**
>
> -   **轮询建议**：视频生成过程约需数分钟，建议采用**轮询**机制，并设置合理的查询间隔（如 15 秒）来获取结果。
> -   **任务状态流转**：PENDING（排队中）→ RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。
> -   **task\_id 有效期**：**24小时**，超时后将无法查询结果，接口将返回任务状态为`UNKNOWN`。
> -   **RPS 限制**：查询接口默认RPS为20。如需更高频查询或事件通知，建议[配置异步任务回调](../../more-about-models/async-task-api.md)。
> -   **更多操作**：如需批量查询、取消任务等操作，请参见[管理异步任务](../../more-about-models/manage-asynchronous-tasks.md)。

<table><tbody><tr><td><a id="pv414a0h4qr01"></a><h4>请求参数</h4><a id="pv424a0h5qr01"></a><h5>请求头（Headers）</h5><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><a id="pv430a0h5qr02"></a><h5>URL路径参数（Path parameters）</h5><p><strong>task_id</strong> <code>string</code><strong>（必选）</strong></p><p>任务ID。</p></td><td><a id="sec-tabs-4"></a><section><a id="查询任务结果"></a><section><a id="查询任务结果-h4"></a><h4>查询任务结果</h4><p>将<code>{task_id}</code>完整替换为上一步接口返回的<code>task_id</code>的值。<code>task_id</code>查询有效期为24小时，并请将<code>{WorkspaceId}</code>替换为真实的<a href="../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain">业务空间ID</a>。</p><a id="code-block-7"></a><pre class="language-bash"><code>curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id} \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="pv438a0h4qrs1"></a><h4>响应参数</h4><p><strong>output</strong><code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值-2"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section><strong>轮询过程中的状态流转：</strong><ul><li>PENDING（排队中） → RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。</li><li>初次查询状态通常为 PENDING（排队中）或 RUNNING（处理中）。</li><li>当状态变为 SUCCEEDED 时，响应中将包含生成的视频URL。</li><li>若状态为 FAILED，请检查错误信息并重试。</li><li>若状态为 CANCELED，表示任务已取消，如需继续请重新提交任务。</li><li>若状态为 UNKNOWN，表示任务不存在或状态未知，可能在 task_id 不存在或超过 24 小时有效期后出现。</li></ul><p><strong>submit_time</strong> <code>string</code></p><p>任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>scheduled_time</strong> <code>string</code></p><p>任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>end_time</strong> <code>string</code></p><p>任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>video_url</strong><code>string</code></p><p>视频URL。仅在 task_status 为 SUCCEEDED 时返回。</p><p>视频格式为MP4（H.264 编码）。视频链接暂无过期时间，但不建议将其作为长期存储，请及时下载。</p><p><strong>orig_prompt</strong> <code>string</code></p><p>原始输入的prompt，对应请求参数<code>prompt</code>。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></div></section><p><strong>usage</strong> <code>object</code></p><p>输出信息统计。只对成功的结果计数。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>duration</strong> <code>integer</code></p><p>生成视频的总视频时长（秒），用于计费。</p><p><strong>size</strong> <code>string</code></p><p>生成视频的分辨率。</p><p><strong>fps</strong> <code>integer</code></p><p>生成视频的帧率。</p><p><strong>SR</strong> <code>string</code></p><p>生成视频的分辨率档位。</p><p><strong>audio</strong> <code>boolean</code></p><p>生成视频是否为有声视频。</p><p><strong>video_count</strong> <code>integer</code></p><p>生成视频的数量。固定为1。</p><p>使用pixverse/pixverse-v6-max-t2v时不返回该字段。</p><p><strong>shot_type</strong><code>string</code></p><p>生成视频的镜头类型。</p><p>使用pixverse/pixverse-v6-max-t2v时不返回该字段。</p></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p></td><td><a id="sec-tabs-5"></a><section><a id="任务执行成功"></a><section><a id="任务执行成功-h4"></a><h4>任务执行成功</h4><a id="code-block-8"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;19171ea5-9efb-4d35-93a1-xxxxxx&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;7ed706b7-a9a9-4319-820c-xxxxxx&quot;,
        &quot;task_status&quot;: &quot;SUCCEEDED&quot;,
        &quot;submit_time&quot;: &quot;2026-03-20 10:34:41.630&quot;,
        &quot;scheduled_time&quot;: &quot;2026-03-20 10:34:41.655&quot;,
        &quot;end_time&quot;: &quot;2026-03-20 10:35:12.725&quot;,
        &quot;orig_prompt&quot;: &quot;下着雨，赛博城市里，一只浣熊在栏杆上行走。突然他眼睛发出蓝光，变身成一架高科技无人机，快速飞离画面。&quot;,
        &quot;video_url&quot;: &quot;https://media.pixverseai.cn/xxxx.mp4&quot;
    },
    &quot;usage&quot;: {
        &quot;duration&quot;: 5,
        &quot;shot_type&quot;: &quot;single&quot;,
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

<a id="dashscope-sdk调用"></a>

<a id="pv601a0h2sdk1"></a>

## DashScope SDK调用

SDK 的参数命名与[HTTP接口](pixverse-text-to-video-api-reference.md#pv101a0h2http)基本一致，参数结构根据语言特性进行封装。

由于文生视频任务耗时较长（通常为1-5分钟），SDK 在底层封装了 HTTP 异步调用流程，支持同步、异步两种调用方式。

> 具体耗时受限于排队任务数和服务执行情况，请在获取结果时耐心等待。

<a id="python-sdk调用"></a>

<a id="pv607a0h3pyth"></a>

### Python SDK调用

> **重要**
>
> 请确保 DashScope Python SDK 版本**不低于**2.0.1，再运行以下代码。

**北京地域**：`region="cn-beijing"`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)，各地域的region取值不同。

<a id="sec-tabs-6"></a>

<a id="同步调用"></a>

<a id="同步调用-h4"></a>

#### 同步调用

<a id="pv626a0h5syn1"></a>

##### 请求示例

<a id="code-block-11"></a>

```python
import os
import dashscope
from dashscope import DashScopeError

# 以下为华北2（北京）地域的配置。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的region取值不同。
# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
# 获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
client = dashscope.Client(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

def sample_sync_call_t2v():
    # call sync api, will return the result
    print('please wait...')
    # generate 为一步式调用（提交任务并等待完成），返回已完成的 Job
    try:
        job = client.videos.generate(model='pixverse/pixverse-v6-max-t2v',
                                     prompt='下着雨，赛博城市里，一只浣熊在栏杆上行走。突然他眼睛发出蓝光，变身成一架高科技无人机，快速飞离画面。',
                                     resolution='720P',
                                     duration=5,
                                     watermark=False,
                                     parameters={'aspect_ratio': '16:9', 'audio': False})
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

<a id="pv628a0h5syn2"></a>

##### 响应示例

> `video_url`暂无过期时间，但不建议将其作为长期存储，请及时下载。

<a id="code-block-12"></a>

```json
{
    "request_id": "2b68d32e-86c8-4383-8a18-xxxxxx",
    "task_id": "ec40bb42-02d4-44d8-bf35-xxxxxx",
    "status": "SUCCEEDED",
    "results": [
        {
            "video_url": "https://media.pixverseai.cn/xxx.mp4"
        }
    ],
    "task_metrics": {
        "TOTAL": 1,
        "SUCCEEDED": 1,
        "FAILED": 0
    },
    "usage": {
        "video_count": 1,
        "video_duration": 0,
        "video_ratio": "",
        "duration": 10,
        "size": "1280*720",
        "fps": 24,
        "audio": false,
        "SR": "720"
    }
}
```

<a id="异步调用"></a>

<a id="异步调用-h4"></a>

#### 异步调用

<a id="pv636a0h5asy1"></a>

##### 请求示例

<a id="code-block-13"></a>

```python
import os
import dashscope
from dashscope import DashScopeError

# 以下为华北2（北京）地域的配置。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的region取值不同。
# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
# 获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
client = dashscope.Client(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

def sample_async_call_t2v():
    # call async api, will return the task information
    # you can get task status with the returned task id.
    try:
        job = client.videos.jobs.create(model='pixverse/pixverse-v6-max-t2v',
                                        prompt='下着雨，赛博城市里，一只浣熊在栏杆上行走。突然他眼睛发出蓝光，变身成一架高科技无人机，快速飞离画面。',
                                        resolution='720P',
                                        duration=5,
                                        watermark=True,
                                        parameters={'aspect_ratio': '16:9', 'audio': False})
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

<a id="code-block-14"></a>

```json
{
	"request_id": "c86ff7ba-8377-917a-90ed-xxxxxx",
	"task_id": "721164c6-8619-4a35-a6d9-xxxxxx",
	"status": "PENDING"
}
```

2、查询任务结果的响应示例

> `video_url` 暂无过期时间，但不建议将其作为长期存储，请及时下载。

<a id="code-block-15"></a>

```json
{
    "request_id": "2b68d32e-86c8-4383-8a18-xxxxxx",
    "task_id": "ec40bb42-02d4-44d8-bf35-xxxxxx",
    "status": "SUCCEEDED",
    "results": [
        {
            "video_url": "https://media.pixverseai.cn/xxx.mp4"
        }
    ],
    "task_metrics": {
        "TOTAL": 1,
        "SUCCEEDED": 1,
        "FAILED": 0
    },
    "usage": {
        "video_count": 1,
        "video_duration": 0,
        "video_ratio": "",
        "duration": 10,
        "size": "1280*720",
        "fps": 24,
        "audio": false,
        "SR": "720"
    }
}
```

<a id="java-sdk调用"></a>

<a id="589b80853e6rn"></a>

### Java SDK调用

> **重要**
>
> 请确保 DashScope Java SDK 版本**不低于**`2.22.6`，再运行以下代码。

**北京地域**：`Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="sec-tabs-7"></a>

<a id="同步调用-2"></a>

<a id="同步调用-2-h4"></a>

#### 同步调用

<a id="3e3609efb9rhl"></a>

##### 请求示例

<a id="code-block-16"></a>

```java
// 调用时请将 {WorkspaceId} 替换为真实的业务空间ID。
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
        // 以下为北京地域url
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
    }

    // 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    // 获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    public static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    /**
     * Create a video compositing task and wait for the task to complete.
     */
    public static void text2Video() throws ApiException, NoApiKeyException, InputRequiredException {
        VideoSynthesis vs = new VideoSynthesis();
        Map<String, Object> parameters = new HashMap<>();
        parameters.put("aspect_ratio", "16:9");

        VideoSynthesisParam param =
                VideoSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("pixverse/pixverse-v6-max-t2v")
                        .prompt("下着雨，赛博城市里，一只浣熊在栏杆上行走。突然他眼睛发出蓝光，变身成一架高科技无人机，快速飞离画面。")
                        .resolution("720P")
                        .duration(5)
                        .audio(true)
                        .watermark(true)
                        .seed(12345)
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

> `video_url` 暂无过期时间，但不建议将其作为长期存储，请及时下载。

<a id="code-block-17"></a>

```json
{
    "request_id": "bd1109bd-6c63-4e62-8bb8-xxxxxx",
    "output": {
        "task_id": "72af7c13-dad5-4aaa-b85d-xxxxxx",
        "task_status": "SUCCEEDED",
        "video_url": "https://media.pixverseai.cn/xxx.mp4",
        "orig_prompt": "下着雨，赛博城市里，一只浣熊在栏杆上行走。突然他眼睛发出蓝光，变身成一架高科技无人机，快速飞离画面。",
        "submit_time": "2026-03-20 11:21:13.227",
        "scheduled_time": "2026-03-20 11:21:13.252",
        "end_time": "2026-03-20 11:21:43.924"
    },
    "usage": {
        "video_count": 1,
        "duration": 5.0,
        "size": "1280*720",
        "input_video_duration": 0.0,
        "output_video_duration": 0.0,
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

<a id="code-block-18"></a>

```java
// 调用时请将 {WorkspaceId} 替换为真实的业务空间ID。
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
        // 以下为北京地域url
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
    }

    // 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    // 获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    public static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    /**
     * Create a video compositing task and wait for the task to complete.
     */
    public static void text2Video() throws ApiException, NoApiKeyException, InputRequiredException {
        VideoSynthesis vs = new VideoSynthesis();

        Map<String, Object> parameters = new HashMap<>();
        parameters.put("aspect_ratio", "16:9");

        VideoSynthesisParam param =
                VideoSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("pixverse/pixverse-v6-max-t2v")
                        .prompt("下着雨，赛博城市里，一只浣熊在栏杆上行走。突然他眼睛发出蓝光，变身成一架高科技无人机，快速飞离画面。")
                        .resolution("720P")
                        .duration(5)
                        .audio(true)
                        .watermark(true)
                        .seed(12345)
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

<a id="code-block-19"></a>

```json
{
    "request_id": "9b583f1b-2423-4fac-bb3f-xxxxxx",
    "output": {
        "task_id": "3944b819-1bbb-4da0-a230-xxxxxx",
        "task_status": "PENDING"
    },
    "status_code": 200,
    "code": "",
    "message": ""
}
```

2、查询任务结果的响应示例

> `video_url` 暂无过期时间，但不建议将其作为长期存储，请及时下载。

<a id="code-block-20"></a>

```json
{
    "request_id": "bd1109bd-6c63-4e62-8bb8-xxxxxx",
    "output": {
        "task_id": "72af7c13-dad5-4aaa-b85d-xxxxxx",
        "task_status": "SUCCEEDED",
        "video_url": "https://media.pixverseai.cn/xxx.mp4",
        "orig_prompt": "下着雨，赛博城市里，一只浣熊在栏杆上行走。突然他眼睛发出蓝光，变身成一架高科技无人机，快速飞离画面。",
        "submit_time": "2026-03-20 11:21:13.227",
        "scheduled_time": "2026-03-20 11:21:13.252",
        "end_time": "2026-03-20 11:21:43.924"
    },
    "usage": {
        "video_count": 1,
        "duration": 5.0,
        "size": "1280*720",
        "input_video_duration": 0.0,
        "output_video_duration": 0.0,
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

如果模型调用失败并返回报错信息，请参见[错误码](../../preparations/error-code.md)进行解决。

<a id="常见问题"></a>

<a id="pv801a0h2faq1"></a>

## 常见问题

<a id="q-为什么1080p分辨率下不能使用10秒时长"></a>

<a id="pv806a0h4fq02"></a>

#### Q：为什么1080P分辨率下不能使用10秒时长？

A： `pixverse-v5.6-t2v` 在 1080P 下不支持 10 秒。建议降低分辨率至 720P/540P/360P，或切换至 `pixverse-c1-t2v`或`pixverse-v6-t2v` 模型。
