# Vidu-参考生视频 API 参考

Vidu-参考生视频模型支持传入 参考图片 和 文本提示词 ，将图片中的主体角色融合到提示词描述的场景中，生成流畅的视频内容。

> **重要**
>
> 本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。

<a id="服务开通"></a>

<a id="8bb48973d87d6"></a>

## 服务开通

请前往[阿里云百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)，搜索 **Vidu**，找到 **Vidu** 模型卡片，单击**立即开通**；在弹窗内确认开通及授权。

<a id="适用范围"></a>

<a id="1fd78afa5brlj"></a>

## 适用范围

为确保调用成功，请务必保证**模型、Endpoint URL 和 API Key 均属于同一地域**。跨地域调用将会失败。

-   [**选择模型**](https://bailian.console.aliyun.com/cn-beijing/model/market)：确认模型所属的地域。
-   **选择 URL**：选择对应的地域 Endpoint URL，支持HTTP URL。
-   **配置 API Key**：选择地域并[获取与配置 API Key](../../preparations/get-api-key.md)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

<a id="http-调用"></a>

<a id="pvr101a0h2http"></a>

## HTTP 调用

由于参考生视频任务耗时较长（通常为 1-5 分钟），API 采用异步调用。整个流程包含 **"创建任务 -> 轮询获取"** 两个核心步骤，具体如下：

<a id="步骤-1-创建任务获取任务-id"></a>

<a id="pvr111a0h4stp1"></a>

### 步骤 1：创建任务获取任务 ID

**北京地域**：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`

> **说明**
>
> -   创建成功后，使用接口返回的 `task_id` 查询结果，task\_id 有效期为 24 小时。**请勿重复创建任务**，轮询获取即可。
> -   新手指引请参见[Postman](https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api)。

<table><tbody><tr><td><a id="pvr123a0h4reqp"></a><h4>请求参数</h4><a id="pvr144a0h5hdr1"></a><h5>请求头（Headers）</h5><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><p><strong>X-DashScope-Async</strong><code>string</code><strong>（必选）</strong></p><p>异步处理配置参数。HTTP请求只支持异步，<strong>必须设置为</strong><code>enable</code>。</p><div><div><p><strong>重要</strong>缺少此请求头将报错：“current user api does not support synchronous calls”。</p></div></div><a id="pvr156a0h5body"></a><h5>请求体（Request Body）</h5><p><strong>model</strong> <code>string</code> <strong>（必选）</strong></p><p>模型名称。可选值为：</p><ul><li><code>vidu/viduq3-ad_reference2video</code></li><li><code>vidu/viduq3-drama_reference2video</code></li><li><code>vidu/viduq3-mix_reference2video</code></li><li><code>vidu/viduq3_reference2video</code></li><li><code>vidu/viduq3-turbo_reference2video</code></li><li><code>vidu/viduq2-pro_reference2video</code></li><li><code>vidu/viduq2_reference2video</code></li></ul><a id="accordion-模型选型"></a><section><p>模型选型</p><div><ul><li><strong>广告视频</strong>：推荐 <strong>viduq3-ad</strong>，面向广告行业，支持营销级智能切镜、运镜和音效直出，上传商品图即可生成广告视频。</li><li><strong>精品剧 / AI 漫剧</strong>：推荐 <strong>viduq3-drama</strong>，角色一致性强、动效细腻、情绪表达真实，适合剧情向内容生产。</li><li><strong>通用场景</strong>：推荐 <strong>viduq3-mix</strong>，画面质感与动态效果均衡，适合大多数参考生视频需求。</li><li><strong>追求速度与性价比</strong>：推荐 <strong>viduq3-turbo</strong>，生成速度最快。</li></ul></div></section><p><strong>input</strong> <code>object</code> <strong>（必选）</strong></p><p>输入的基本信息，包括参考图片和提示词。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>prompt</strong> <code>string</code> <strong>（必选）</strong></p><p>文本提示词。用来描述生成视频中期望包含的元素和视觉特点。</p><p>支持中英文，不超过 5000 个字符，超过部分会自动截断。</p><p>示例值：男人坐在靠窗的椅子上，手持吉他，在咖啡厅旁演奏一首舒缓的美国乡村民谣。</p><p>提示词编写请参见<a href="../../../model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md">Vidu视频生成Prompt指南</a>。</p><p><strong>media</strong> <code>array</code> <strong>（必选）</strong></p><p>媒体素材列表，用于指定视频生成所需的参考图像。</p><p>数组的每个元素为一个媒体对象，包含 <code>type</code>和 <code>url</code> 字段。</p><a id="accordion-元素属性"></a><section><p>元素属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>媒体素材类型。可选值与模型有关：</p><a id="accordion-仅传入参考图像"></a><section><p>仅传入参考图像</p><div><p>支持模型：vidu/viduq3-ad_reference2video、vidu/viduq3-drama_reference2video、vidu/viduq3-mix_reference2video、vidu/viduq3_reference2video、vidu/viduq3-turbo_reference2video、vidu/viduq2_reference2video</p><p>固定为：</p><ul><li><code>image</code>：参考图像。</li></ul><p>素材限制：图像数量为1～7张。</p></div></section><a id="accordion-传入参考图像和视频"></a><section><p>传入参考图像和视频</p><div><p>支持模型：vidu/viduq2-pro_reference2video</p><p>可选值为：</p><ul><li><code>image</code>：参考图像。必选。</li><li><code>video</code>：参考视频。可选。</li></ul><p>素材限制：</p><ul><li><p>仅参考图像：图像数量为1～7张。</p></li><li><p>参考图像和视频：</p><ul><li>图像数量为1～4张。</li><li>视频数量为1～2个。</li></ul></li></ul></div></section><p><strong>url</strong> <code>string</code> <strong>（必选）</strong></p><p>媒体素材URL。素材包括图像、视频。</p><a id="accordion-传入图像-type-image"></a><section><p>传入图像（type=image）</p><div><p>参考图像URL，必须为公网可访问的 URL。</p><ul><li>支持 HTTP 或 HTTPS 协议。</li><li>示例值：<a href="https://xxx/xxx.png"></a><a href="https://xxx/xxx.png">https://xxx/xxx.png</a>。</li></ul><p>图像限制：</p><ul><li>格式：JPEG、JPG、PNG、WEBP。</li><li>宽高比：1:4～4:1。</li><li>文件大小：不超过 50MB。</li></ul></div></section><a id="accordion-传入视频-type-video"></a><section><p>传入视频（type=video）</p><div><p>参考视频URL，必须为公网可访问的 URL。</p><ul><li>支持 HTTP 或 HTTPS 协议。</li><li>示例值：<a href="https://xxx/xxx.mp4"></a><a href="https://xxx/xxx.mp4">https://xxx/xxx.mp4</a>。</li></ul><p>视频限制：</p><ul><li>格式：mp4、avi、mov。</li><li>分辨率：总像素值不小于128*128。</li><li>宽高比：1:4～4:1。</li><li>时长：传入1个参考视频时为1～8秒；传入2个参考视频时各为1～5秒。</li><li>文件大小：不超过 50MB。</li></ul></div></section></div></section></div></section><p><strong>parameters</strong> <code>object</code> <strong>（必选）</strong></p><p>视频生成参数。如设置视频分辨率、时长等。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>resolution</strong> <code>string</code> （可选）</p><div><div><p><strong>重要</strong>resolution直接影响费用，请在调用前确认<a href="../../../model-user-guide/test-1/model-pricing.md#69993500dc6mi">模型价格</a>。</p></div></div><p>生成视频的分辨率。可选值与模型有关：</p><ul><li>vidu/viduq3-ad_reference2video：可选720P、1080P。默认值为720P。</li><li>vidu/viduq3-drama_reference2video：可选720P、1080P。默认值为1080P。</li><li>vidu/viduq3-mix_reference2video：可选540P、720P、1080P。默认值为720P。</li><li>vidu/viduq3_reference2video：可选540P、720P、1080P。默认值为720P。</li><li>vidu/viduq3-turbo_reference2video：可选540P、720P、1080P。默认值为720P。</li><li>vidu/viduq2-pro_reference2video：可选540P、720P、1080P。默认值为720P。</li><li>vidu/viduq2_reference2video：可选540P、720P、1080P。默认值为720P。</li></ul><p><strong>size</strong> <code>string</code> （可选）</p><p>生成视频的分辨率，格式为<code>宽*高</code>的像素值。</p><p>默认值根据<code>resolution</code>而定：</p><ul><li>当 resolution=540P 时，size 默认为 <code>1024*576</code>。</li><li>当 resolution=720P 时，size 默认为 <code>1280*720</code>。</li><li>当 resolution=1080P 时，size 默认为 <code>1920*1080</code>。</li></ul><p>各模型支持的宽高比有所不同：</p><ul><li>vidu/viduq3-drama_reference2video：仅支持 16:9 和 9:16。</li><li>其他模型：支持 16:9、4:3、1:1、3:4、9:16。</li></ul><table><tbody><tr><td><p>分辨率档位</p></td><td><p>宽高比</p></td><td><p><strong>size 取值（宽*高）</strong></p></td></tr><tr><td rowspan="5"><p>540P</p></td><td><p>16:9</p></td><td><p>1024*576</p></td></tr><tr><td><p>4:3</p></td><td><p>1024*768</p></td></tr><tr><td><p>1:1</p></td><td><p>1024*1024</p></td></tr><tr><td><p>3:4</p></td><td><p>768*1024</p></td></tr><tr><td><p>9:16</p></td><td><p>576*1024</p></td></tr><tr><td rowspan="5"><p>720P</p></td><td><p>16:9</p></td><td><p>1280*720</p></td></tr><tr><td><p>4:3</p></td><td><p>1280*960</p></td></tr><tr><td><p>1:1</p></td><td><p>1280*1280</p></td></tr><tr><td><p>3:4</p></td><td><p>960*1280</p></td></tr><tr><td><p>9:16</p></td><td><p>720*1280</p></td></tr><tr><td rowspan="5"><p>1080P</p></td><td><p>16:9</p></td><td><p>1920*1080</p></td></tr><tr><td><p>4:3</p></td><td><p>1920*1440</p></td></tr><tr><td><p>1:1</p></td><td><p>1808*1808</p></td></tr><tr><td><p>3:4</p></td><td><p>1440*1920</p></td></tr><tr><td><p>9:16</p></td><td><p>1080*1920</p></td></tr></tbody></table><p><strong>duration</strong> <code>integer</code> <strong>（必选）</strong></p><div><div><p><strong>重要</strong>duration直接影响费用，按秒计费，请在调用前确认<a href="../../../model-user-guide/test-1/model-pricing.md#69993500dc6mi">模型价格</a>。</p></div></div><p>生成视频的时长，单位为秒。</p><ul><li><p>vidu/viduq3-ad_reference2video：取值为[3, 15]之间的整数。默认值为<code>5</code>。</p></li><li><p>vidu/viduq3-drama_reference2video：取值为[2, 15]之间的整数。默认值为<code>5</code>。</p><ul><li>当分镜数量过多或明显少于duration时，模型可能自动调整时长以保障故事完整性，实际视频时长可能多于或少于duration设定值。</li><li>计费按实际输出时长计算。</li></ul></li><li><p>vidu/viduq3-mix_reference2video：取值为[1, 16]之间的整数。默认值为<code>5</code>。</p></li><li><p>vidu/viduq3_reference2video：取值为[1, 16]之间的整数。默认值为<code>5</code>。</p></li><li><p>vidu/viduq3-turbo_reference2video：取值为[1, 16]之间的整数。默认值为<code>5</code>。</p></li><li><p>vidu/viduq2-pro_reference2video：取值为[1, 10]之间的整数。默认值为<code>5</code>。</p><ul><li><p>特殊设置：支持设置为0，表示自动规划时长，上限不超过 10 秒。</p><ul><li>若上传 1 个参考视频：生成视频时长通常等于该参考视频时长。</li><li>若上传 2 个参考视频：模型结合提示词，生成视频时长通常等于”主要参考视频”的时长。</li></ul></li></ul></li><li><p>vidu/viduq2_reference2video：取值为[1, 10]之间的整数。默认值为<code>5</code>。</p></li></ul><p><strong>audio</strong> <code>boolean</code> （可选）</p><p><strong>支持模型</strong>：vidu/viduq3-ad_reference2video、vidu/viduq3-mix_reference2video、vidu/viduq3_reference2video、vidu/viduq3-turbo_reference2video。</p><p>是否生成有声视频。开启后模型将根据视频内容自动生成匹配的背景音乐或音效。</p><ul><li><code>false</code>：默认值，输出无声视频。</li><li><code>true</code>：输出有声视频。</li></ul><div><div><p><strong>说明</strong>vidu/viduq3-drama_reference2video 不支持该参数，默认输出有声视频。</p></div></div><p><strong>watermark</strong> <code>boolean</code> （可选）</p><p>是否添加水印标识，水印位于视频右下角，文案固定为“内容由AI生成”。</p><ul><li><code>false</code>：默认值，不添加水印。</li><li><code>true</code>：添加水印。</li></ul><p><strong>seed</strong><code>integer</code>（可选）</p><p>随机数种子，取值范围为<code>[0, 2147483647]</code>。</p><p>未指定时，系统自动生成随机种子。若需提升生成结果的可复现性，建议固定seed值。</p><p>请注意，由于模型生成具有概率性，即使使用相同 seed，也不能保证每次生成结果完全一致。</p><p>示例值：12345。</p></div></section></td><td><a id="sec-tabs"></a><section><a id="参考生视频-广告-仅参考图像"></a><section><a id="参考生视频-广告-仅参考图像-h4"></a><h4>参考生视频-广告（仅参考图像）</h4><p>支持模型：vidu/viduq3-ad_reference2video。</p><a id="code-block"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;vidu/viduq3-ad_reference2video&quot;,
    &quot;input&quot;: {
        &quot;media&quot;: [
            {
                &quot;type&quot;: &quot;image&quot;,
                &quot;url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260713/dtnctw/ad-1.png&quot;
            },
            {
                &quot;type&quot;: &quot;image&quot;,
                &quot;url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260713/bspdpd/ad-2.png&quot;
            },
            {
                &quot;type&quot;: &quot;image&quot;,
                &quot;url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260713/mhsjyy/ad-3.png&quot;
            }
        ],
        &quot;prompt&quot;: &quot;一个瑜伽裤的广告。商品是一条左右各有一个口袋的黑色高腰瑜伽裤。亚洲模特开心地说&quot;我现在再也不穿没有口袋的瑜伽裤了&quot;。画面保持清晰、稳定、容易理解。&quot;
    },
    &quot;parameters&quot;: {
        &quot;duration&quot;: 8,
        &quot;size&quot;: &quot;1080*1920&quot;,
        &quot;resolution&quot;: &quot;1080P&quot;,
        &quot;watermark&quot;: true
    }
}'
</code></pre></section><a id="python-sdk"></a><section><a id="python-sdk-h4"></a><h4>Python SDK</h4><a id="code-block-2"></a><pre class="language-python"><code>import dashscope
import os
from dashscope import DashScopeError

# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;
# 获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
client = dashscope.Client(api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;))

media = [{'type': 'image', 'url': 'https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260713/dtnctw/ad-1.png'}, {'type': 'image', 'url': 'https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260713/bspdpd/ad-2.png'}, {'type': 'image', 'url': 'https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260713/mhsjyy/ad-3.png'}]

def sample_async_call():
    # 异步提交视频生成任务
    try:
        job = client.videos.jobs.create(model='vidu/viduq3-ad_reference2video',
                                        prompt='一个瑜伽裤的广告。商品是一条左右各有一个口袋的黑色高腰瑜伽裤。亚洲模特开心地说&quot;我现在再也不穿没有口袋的瑜伽裤了&quot;。画面保持清晰、稳定、容易理解。',
                                        media=media,
                                        size='1080*1920',
                                        resolution='1080P',
                                        duration=8,
                                        watermark=True)
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
</code></pre></section><a id="参考生视频-短剧-仅参考图像"></a><section><a id="参考生视频-短剧-仅参考图像-h4"></a><h4>参考生视频-短剧（仅参考图像）</h4><p>支持模型：vidu/viduq3-drama_reference2video。</p><a id="code-block-3"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;vidu/viduq3-drama_reference2video&quot;,
       &quot;input&quot;: {
        &quot;media&quot;: [
            {
                &quot;type&quot;: &quot;image&quot;,
                &quot;url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260713/eelcsu/daram-1.png&quot;
            },
            {
                &quot;type&quot;: &quot;image&quot;,
                &quot;url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260713/adglrn/drama-2.png&quot;
            },
            {
                &quot;type&quot;: &quot;image&quot;,
                &quot;url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260713/fmofkp/drama-3.png&quot;
            },
            {
                &quot;type&quot;: &quot;image&quot;,
                &quot;url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260713/mktdht/drama-4.png&quot;
            }
        ],
        &quot;prompt&quot;: &quot;酒店宴会厅，王桂兰（图3）（在画面右侧，坐在席位上）苏文博（图1）、许向暖（图2）（在画面左侧远处，敬酒中）。婚礼现场座无虚席，坐满宾客。苏文博的母亲王桂兰坐在席位上，眉头紧紧皱起，面露不满。镜头固定，捕捉她皱眉的表情。镜头推进王桂兰面部，她眼神阴沉，嘴角下撇，带着嫌弃和不满。强调她的不悦。&quot;
    },
    &quot;parameters&quot;: {
        &quot;duration&quot;: 9,
        &quot;size&quot;: &quot;1080*1920&quot;,
        &quot;resolution&quot;: &quot;1080P&quot;,
        &quot;watermark&quot;: true
    }
}'
</code></pre></section><a id="参考生视频-仅参考图像"></a><section><a id="参考生视频-仅参考图像-h4"></a><h4>参考生视频（仅参考图像）</h4><a id="code-block-4"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
   -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;vidu/viduq3-mix_reference2video&quot;,
       &quot;input&quot;: {
        &quot;media&quot;: [
            {
                &quot;type&quot;: &quot;image&quot;,
                &quot;url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260320/knsple/wan-r2v-role-frame.jpg&quot;
            },
            {
                &quot;type&quot;: &quot;image&quot;,
                &quot;url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qpzxps/wan-r2v-object4.png&quot;
            },
            {
                &quot;type&quot;: &quot;image&quot;,
                &quot;url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/wfjikw/wan-r2v-backgroud5.png&quot;
            }
        ],
        &quot;prompt&quot;: &quot;男人坐在靠窗的椅子上，手持吉他，在咖啡厅旁演奏一首舒缓的美国乡村民谣&quot;
    },
    &quot;parameters&quot;: {
        &quot;duration&quot;: 5,
        &quot;size&quot;: &quot;1280*720&quot;,
        &quot;resolution&quot;: &quot;720P&quot;,
        &quot;watermark&quot;: true
    }
}'
</code></pre></section><a id="参考生视频-参考图像-视频"></a><section><a id="参考生视频-参考图像-视频-h4"></a><h4>参考生视频（参考图像+视频）</h4><p>支持模型：vidu/viduq2-pro_reference2video。</p><a id="code-block-5"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
   -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;vidu/viduq2-pro_reference2video&quot;,
       &quot;input&quot;: {
        &quot;media&quot;: [
            {
                &quot;type&quot;: &quot;video&quot;,
                &quot;url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qigswt/wan-r2v-role2.mp4&quot;
            },
            {
                &quot;type&quot;: &quot;image&quot;,
                &quot;url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qpzxps/wan-r2v-object4.png&quot;
            },
            {
                &quot;type&quot;: &quot;image&quot;,
                &quot;url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/wfjikw/wan-r2v-backgroud5.png&quot;
            }
        ],
        &quot;prompt&quot;: &quot;男人坐在靠窗的椅子上，手持吉他，在咖啡厅旁演奏一首舒缓的美国乡村民谣&quot;
    },
    &quot;parameters&quot;: {
        &quot;duration&quot;: 5,
        &quot;size&quot;: &quot;1280*720&quot;,
        &quot;resolution&quot;: &quot;720P&quot;,
        &quot;watermark&quot;: true
    }
}'
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="pvr379a0h4rsp1"></a><h4>响应参数</h4><p><strong>output</strong> <code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></td><td><a id="sec-tabs-2"></a><section><a id="成功响应"></a><section><a id="成功响应-h4"></a><h4>成功响应</h4><p>请保存 task_id，用于查询任务状态与结果。</p><a id="code-block-6"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
        &quot;task_status&quot;: &quot;PENDING&quot;,
        &quot;task_id&quot;: &quot;0385dc79-5ff8-4d82-bcb6-xxxxxx&quot;
    },
    &quot;request_id&quot;: &quot;4909100c-7b5a-9f92-bfe5-xxxxxx&quot;
}
</code></pre></section><a id="异常响应"></a><section><a id="异常响应-h4"></a><h4>异常响应</h4><p>创建任务失败，请参见<a href="../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-7"></a><pre class="language-json"><code>{
    &quot;code&quot;: &quot;InvalidApiKey&quot;,
    &quot;message&quot;: &quot;No API-key provided.&quot;,
    &quot;request_id&quot;: &quot;7438d53d-6eb8-4596-8835-xxxxxx&quot;
}
</code></pre></section></section></td></tr></tbody></table>

<a id="步骤-2-根据任务-id-查询结果"></a>

<a id="pvr411a0h4stp2"></a>

### 步骤 2：根据任务 ID 查询结果

**北京地域**：`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`

> **说明**
>
> -   **轮询建议**：视频生成过程约需数分钟，建议采用**轮询**机制，并设置合理的查询间隔（如 15 秒）来获取结果。
> -   **任务状态流转**：PENDING（排队中）→ RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。
> -   **task\_id 有效期**：**24 小时**，超时后将无法查询结果，接口将返回任务状态为`UNKNOWN`。
> -   **RPS 限制**：查询接口默认 RPS 为 20。如需更高频查询或事件通知，建议[配置异步任务回调](../../more-about-models/async-task-api.md)。
> -   **更多操作**：如需批量查询、取消任务等操作，请参见[管理异步任务](../../more-about-models/manage-asynchronous-tasks.md)。

<table><tbody><tr><td><a id="pvr424a0h4qr01"></a><h4>请求参数</h4><a id="pvr434a0h5qr01"></a><h5>请求头（Headers）</h5><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><a id="pvr440a0h5qr02"></a><h5>URL 路径参数（Path parameters）</h5><p><strong>task_id</strong> <code>string</code><strong>（必选）</strong></p><p>任务ID。</p></td><td><a id="sec-tabs-3"></a><section><a id="查询任务结果"></a><section><a id="查询任务结果-h4"></a><h4>查询任务结果</h4><p>将<code>{task_id}</code>完整替换为上一步接口返回的<code>task_id</code>的值。<code>task_id</code>查询有效期为24小时</p><a id="code-block-8"></a><pre class="language-bash"><code>curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id} \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="pvr448a0h4qrs1"></a><h4>响应参数</h4><p><strong>output</strong><code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值-2"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section><strong>轮询过程中的状态流转：</strong><ul><li>PENDING（排队中） → RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。</li><li>初次查询状态通常为 PENDING（排队中）或 RUNNING（处理中）。</li><li>当状态变为 SUCCEEDED 时，响应中将包含生成的视频URL。</li><li>若状态为 FAILED，请检查错误信息并重试。</li><li>若状态为 CANCELED，表示任务已取消，如需继续请重新提交任务。</li><li>若状态为 UNKNOWN，表示任务不存在或状态未知，可能在 task_id 不存在或超过 24 小时有效期后出现。</li></ul><p><strong>submit_time</strong> <code>string</code></p><p>任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>scheduled_time</strong> <code>string</code></p><p>任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>end_time</strong> <code>string</code></p><p>任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>video_url</strong><code>string</code></p><p>视频 URL。仅在 task_status 为 SUCCEEDED 时返回。</p><p>视频格式为 MP4（H.264 编码）。视频链接有效期24 小时，请及时下载。</p><p><strong>orig_prompt</strong> <code>string</code></p><p>原始输入的prompt，对应请求参数<code>prompt</code>。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></div></section><p><strong>usage</strong> <code>object</code></p><p>输出信息统计。只对成功的结果计数。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>duration</strong> <code>integer</code></p><p>生成视频的总视频时长，用于计费。</p><p><strong>size</strong> <code>string</code></p><p>生成视频的分辨率。</p><p><strong>fps</strong> <code>integer</code></p><p>生成视频的帧率。固定为 24。</p><p><strong>SR</strong> <code>string</code></p><p>生成视频的分辨率档位。</p><p><strong>audio</strong> <code>boolean</code></p><p>生成视频是否为有声视频。</p><p><strong>video_count</strong> <code>integer</code></p><p>生成视频的数量。固定为 1。</p><p><strong>reference_type</strong> <code>string</code></p><p>参考素材类型。</p></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p></td><td><a id="sec-tabs-4"></a><section><a id="任务执行成功"></a><section><a id="任务执行成功-h4"></a><h4>任务执行成功</h4><p>视频URL仅保留24小时，超时后会被自动清除，请及时保存生成的视频。</p><a id="code-block-9"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;8f240644-efe8-43bf-86ff-xxxxxx&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;b7e05baa-c318-440d-b293-xxxxxx&quot;,
        &quot;task_status&quot;: &quot;SUCCEEDED&quot;,
        &quot;submit_time&quot;: &quot;2026-03-27 15:10:42.723&quot;,
        &quot;scheduled_time&quot;: &quot;2026-03-27 15:10:42.754&quot;,
        &quot;end_time&quot;: &quot;2026-03-27 15:11:17.388&quot;,
        &quot;orig_prompt&quot;: &quot;男人坐在靠窗的椅子上，手持吉他，在咖啡厅旁演奏一首舒缓的美国乡村民谣&quot;,
        &quot;video_url&quot;: &quot;https://prod-ss-vidu.s3.cn-northwest-1.amazonaws.com.cn/xxx.mp4?xxx&quot;
    },
    &quot;usage&quot;: {
        &quot;duration&quot;: 5,
        &quot;size&quot;: &quot;960*528&quot;,
        &quot;output_video_duration&quot;: 5,
        &quot;fps&quot;: 24,
        &quot;video_count&quot;: 1,
        &quot;audio&quot;: false,
        &quot;reference_type&quot;: &quot;image,video&quot;,
        &quot;SR&quot;: &quot;540&quot;
    }
}
</code></pre></section><a id="任务执行失败"></a><section><a id="任务执行失败-h4"></a><h4>任务执行失败</h4><p>若任务执行失败，task_status将置为 FAILED，并提供错误码和信息。请参见<a href="../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-10"></a><pre class="language-json"><code>{
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

<a id="错误码"></a>

<a id="OajFO"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](../../preparations/error-code.md)进行解决。

<a id="常见问题"></a>

<a id="a0379eaad3lho"></a>

## 常见问题

<a id="q-size-与-resolution-必须同时传入吗"></a>

<a id="d64acbbcf61fn"></a>

#### Q：size 与 resolution 必须同时传入吗？

**A：** 不必。二者均为可选参数，但**推荐同时传入**。同时传入可精准控制生成视频的宽高比，具体参见[size取值](vidu-reference-to-video-api-reference.md)。

若不同时传入，系统将按以下两种场景处理：

-   **仅传 size**：size参数会被忽略，系统强制按默认的 `resolution=720P` 及其对应的`size`默认值（`1280*720`）处理。
    
    > 例如：接口返回为size="1280\*720", SR=720。
    
-   **仅传 resolution**：按指定分辨率档位及该档位对应的 16:9 比例输出。
    
    > 例如：当resolution=540P时，接口返回 size="960_528", SR=540；当resolution=1080P时，接口返回 size="1920_1080", SR=1080。
