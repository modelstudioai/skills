# MiniMax-视频生成API文档

MiniMax-视频生成模型支持 文生视频、图生视频-基于首帧、图生视频-基于尾帧、图生视频-基于首尾帧以及多模态参考生视频 。

> **重要**
>
> 本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。

<a id="服务开通"></a>

<a id="mm04h2svc"></a>

## 服务开通

请前往[阿里云百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)，搜索"MiniMax"，找到**MiniMax**模型卡片，单击**立即开通**，在弹窗内确认开通及授权。

<a id="适用范围"></a>

<a id="mm09h2scope"></a>

## 适用范围

为确保调用成功，请务必保证**模型、Endpoint URL 和 API Key 均属于同一地域**。跨地域调用将会失败。

-   [**选择模型**](../../../model-user-guide/model-experience/image-and-video-generation/video-generate-edit-model.md)：确认模型所属的地域。
-   **选择 URL**：选择对应的地域 Endpoint URL，支持HTTP URL。
-   **配置 API Key**：选择地域并[获取与配置 API Key](../../preparations/get-api-key.md)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

<a id="http调用"></a>

<a id="mm101h2http"></a>

## HTTP调用

由于视频生成任务耗时较长（通常为1-5分钟），API采用异步调用。整个流程包含 **"创建任务 -> 轮询获取"** 两个核心步骤，具体如下：

<a id="步骤1-创建任务获取任务id"></a>

<a id="mm111h3step1"></a>

### 步骤1：创建任务获取任务ID

**北京地域**：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

> **说明**
>
> -   创建成功后，使用接口返回的 `task_id` 查询结果，task\_id 有效期为 24 小时。**请勿重复创建任务**，轮询获取即可。
> -   新手指引请参见[Postman](https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api)。

<table><tbody><tr><td><a id="mm123h4reqp"></a><h4>请求参数</h4><a id="mm172h5hdr1"></a><h5>请求头（Headers）</h5><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><p><strong>X-DashScope-Async</strong><code>string</code><strong>（必选）</strong></p><p>异步处理配置参数。HTTP请求只支持异步，<strong>必须设置为</strong><code>enable</code>。</p><div><div><p><strong>重要</strong>缺少此请求头将报错：“current user api does not support synchronous calls”。</p></div></div><a id="mm184h5body"></a><h5>请求体（Request Body）</h5><p><strong>model</strong> <code>string</code> <strong>（必选）</strong></p><p>模型名称。</p><p>可选值：</p><ul><li><code>MiniMax/MiniMax-H3</code></li></ul><p><strong>input</strong> <code>object</code> <strong>（必选）</strong></p><p>输入的基本信息，如提示词、媒体素材等。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>prompt</strong> <code>string</code> <strong>（必选）</strong></p><p>文本提示词。用来描述生成视频中期望包含的元素和视觉特点。</p><p>支持中英文，按字符数计算长度，不超过7000个字符，超过将返回错误。</p><p><strong>media</strong> <code>array</code> （可选）</p><p>文生视频任务无需填写此参数。</p><p>媒体素材列表，用于指定图像、视频或音频素材。</p><p>支持的输入组合（对应不同生成场景）：</p><ul><li><strong>图生视频-首帧</strong>：1张<code>first_frame</code>图片。</li><li><strong>图生视频-尾帧</strong>：1张<code>last_frame</code>图片。</li><li><strong>图生视频-首尾帧</strong>：1张<code>first_frame</code> + 1张<code>last_frame</code>图片。</li><li><strong>多模态参考生视频</strong>：参考图片（<code>image_url</code>）+ 参考视频（<code>feature</code>）+ 参考音频（<code>driving_audio</code>）的组合。</li></ul><div><div><p><strong>说明</strong>图生视频与多模态参考生视频互斥：media中出现<code>image_url</code> / <code>feature</code> / <code>driving_audio</code>任一类型时，不能再出现<code>first_frame</code> / <code>last_frame</code>（反之亦然），二者不可混用。</p></div></div><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>媒体素材类型。可选值：</p><ul><li><code>first_frame</code>：首帧图片。</li><li><code>last_frame</code>：尾帧图片。</li><li><code>image_url</code>：参考图片（多模态参考生视频）。</li><li><code>feature</code>：参考视频（多模态参考生视频）。</li><li><code>driving_audio</code>：参考音频（多模态参考生视频）。</li></ul><p><strong>url</strong> <code>string</code> <strong>（必选）</strong></p><p>媒体素材URL。素材包括图像、视频、音频。</p><a id="accordion-传入图像-type-first-frame或last-frame或image-url"></a><section><p>传入图像（type=first_frame或last_frame或image_url）</p><div><p>图像URL。</p><ul><li>支持 HTTP 或 HTTPS 协议。</li><li>示例值：<a href="https://xxx/xxx.png"></a><a href="https://xxx/xxx.png">https://xxx/xxx.png</a>。</li></ul><p>图像限制：</p><ul><li>格式：JPG、JPEG、PNG、WEBP、HEIC、HEIF。</li><li>分辨率：宽和高的范围为[256, 5760]像素。</li><li>宽高比（宽/高）：[0.4, 2.5]。</li><li>文件大小：不超过30MB。</li><li>数量限制：首帧最多1张、尾帧最多1张、参考图最多9张。</li></ul></div></section><a id="accordion-传入视频-type-feature"></a><section><p>传入视频（type=feature）</p><div><p>视频文件的 URL。仅多模态参考生视频场景使用。</p><ul><li>支持 HTTP 和 HTTPS 协议。</li><li>示例值：<a href="https://xxx/xxx.mp4"></a><a href="https://xxx/xxx.mp4">https://xxx/xxx.mp4</a>。</li></ul><p>视频限制：</p><ul><li>格式：MP4、MOV。</li><li>编码：视频 H.264/AVC、H.265/HEVC；音频 AAC、MP3。</li><li>单段时长：[2, 15]秒，总时长不超过15秒。</li><li>分辨率：宽和高的范围为[256, 5760]像素。</li><li>宽高比（宽/高）：[0.4, 2.5]。</li><li>帧率：[23.976, 60]fps。</li><li>文件大小：不超过50MB。</li><li>数量限制：最多3个视频。</li></ul></div></section><a id="accordion-传入音频-type-driving-audio"></a><section><p>传入音频（type=driving_audio）</p><div><p>音频文件的 URL。仅多模态参考生视频场景使用。</p><ul><li>支持 HTTP 和 HTTPS 协议。</li><li>示例值：<a href="https://xxx/xxx.mp3"></a><a href="https://xxx/xxx.mp3">https://xxx/xxx.mp3</a>。</li></ul><p>音频限制：</p><ul><li>格式：WAV、MP3。</li><li>单段时长：[2, 15]秒，总时长不超过15秒。</li><li>文件大小：不超过15MB。</li><li>数量限制：最多3个音频。</li></ul></div></section></div></section></div></section><p><strong>parameters</strong> <code>object</code> （可选）</p><p>视频生成参数。如设置分辨率、画面比例、视频时长等。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>resolution</strong> <code>string</code> <strong>（必选）</strong></p><p>视频分辨率档位。</p><ul><li><code>768P</code>：标准分辨率。</li><li><code>2K</code>：2K高清分辨率。</li></ul><p><strong>ratio</strong> <code>string</code> （可选）</p><p>生成视频的宽高比例，默认为 <code>adaptive</code>（自动，由输入自适应选择最合适的宽高比）。</p><p>可选值：</p><ul><li><code>adaptive</code>：自适应（默认值）</li><li><code>16:9</code></li><li><code>9:16</code></li><li><code>1:1</code></li><li><code>4:3</code></li><li><code>3:4</code></li><li><code>21:9</code></li></ul><p>各场景填写规则：</p><ul><li><strong>文生视频</strong>：必填，且不能为 <code>adaptive</code>，需指定具体比例。</li><li><strong>图生视频</strong>：宽高比由输入图片决定，恒为 <code>adaptive</code>；传入其他值不会报错，但会被忽略。</li><li><strong>多模态参考生视频</strong>：可选，默认 <code>adaptive</code>，也可指定具体比例。</li></ul><p><strong>duration</strong> <code>integer</code> <strong>（必选）</strong></p><div><div><p><strong>重要</strong>duration直接影响费用，按秒计费，时间越长费用越高，请前往<a href="https://bailian.console.aliyun.com/cn-beijing/model/market">百炼控制台</a>查看价格。</p></div></div><p>生成视频的时长，单位为秒。取值为[4, 15]之间的整数。</p><p>示例值：5。</p><p><strong>watermark</strong> <code>boolean</code> （可选）</p><p>是否在生成视频中添加水印标识。水印位于视频右下角，文案固定为&quot;AI生成&quot;。</p><ul><li><code>false</code>：默认值，不添加水印。</li><li><code>true</code>：添加水印。</li></ul></div></section></td><td><a id="fig-code-group"></a><div><a id="fig-code-group-文生视频-curl-tab"></a>文生视频（curl）<div><a id="code-code-group-文生视频-curl"></a><pre class="language-bash"><code># 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;MiniMax/MiniMax-H3&quot;,
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;史诗级太空歌剧院线预告：女舰长独自站在巨大观景窗前，最后一支舰队正在集结并跃迁离去，强光爆闪、舰桥震动，她被留在原地。&quot;
    },
    &quot;parameters&quot;: {
        &quot;resolution&quot;: &quot;768P&quot;,
        &quot;ratio&quot;: &quot;16:9&quot;,
        &quot;duration&quot;: 5,
        &quot;watermark&quot;: true
    }
}'
</code></pre></div><a id="fig-code-group-文生视频-python-sdk-tab"></a>文生视频（Python SDK）<div><a id="code-code-group-文生视频-python-sdk"></a><pre class="language-python"><code>import dashscope
import os
from dashscope import DashScopeError

# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;
# 获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
client = dashscope.Client(api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;))

def sample_async_call():
    # 异步提交视频生成任务
    try:
        job = client.videos.jobs.create(model='MiniMax/MiniMax-H3',
                                        prompt='史诗级太空歌剧院线预告：女舰长独自站在巨大观景窗前，最后一支舰队正在集结并跃迁离去，强光爆闪、舰桥震动，她被留在原地。',
                                        resolution='768P',
                                        ratio='16:9',
                                        duration=5,
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
</code></pre></div><a id="fig-code-group-图生视频-首帧生视频-tab"></a>图生视频（首帧生视频）<div><a id="code-code-group-图生视频-首帧生视频"></a><pre class="language-bash"><code># 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;MiniMax/MiniMax-H3&quot;,
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;让图片中的人物动起来，头发被微风吹动&quot;,
        &quot;media&quot;: [
            {
                &quot;type&quot;: &quot;first_frame&quot;,
                &quot;url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260121/zlpocv/wan-i2v-haigui.webp&quot;
            }
        ]
    },
    &quot;parameters&quot;: {
        &quot;resolution&quot;: &quot;768P&quot;,
        &quot;duration&quot;: 5,
        &quot;watermark&quot;: true
    }
}'
</code></pre></div><a id="fig-code-group-图生视频-尾帧生视频-tab"></a>图生视频（尾帧生视频）<div><a id="code-code-group-图生视频-尾帧生视频"></a><pre class="language-bash"><code># 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;MiniMax/MiniMax-H3&quot;,
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;镜头缓慢推进，画面逐渐聚焦到图片中的场景&quot;,
        &quot;media&quot;: [
            {
                &quot;type&quot;: &quot;last_frame&quot;,
                &quot;url&quot;: &quot;https://wanx.alicdn.com/material/20250318/last_frame.png&quot;
            }
        ]
    },
    &quot;parameters&quot;: {
        &quot;resolution&quot;: &quot;768P&quot;,
        &quot;duration&quot;: 5,
        &quot;watermark&quot;: true
    }
}'
</code></pre></div><a id="fig-code-group-图生视频-首尾帧生视频-tab"></a>图生视频（首尾帧生视频）<div><a id="code-code-group-图生视频-首尾帧生视频"></a><pre class="language-bash"><code># 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;MiniMax/MiniMax-H3&quot;,
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;写实风格，一只黑色小猫好奇地看向天空，镜头从平视逐渐上升，最后俯拍它的好奇的眼神。&quot;,
        &quot;media&quot;: [
            {
                &quot;type&quot;: &quot;first_frame&quot;,
                &quot;url&quot;: &quot;https://wanx.alicdn.com/material/20250318/first_frame.png&quot;
            },
            {
                &quot;type&quot;: &quot;last_frame&quot;,
                &quot;url&quot;: &quot;https://wanx.alicdn.com/material/20250318/last_frame.png&quot;
            }
        ]
    },
    &quot;parameters&quot;: {
        &quot;resolution&quot;: &quot;768P&quot;,
        &quot;duration&quot;: 5,
        &quot;watermark&quot;: true
    }
}'
</code></pre></div><a id="fig-code-group-多模态参考生视频-tab"></a>多模态参考生视频<div><a id="code-code-group-多模态参考生视频"></a><pre class="language-bash"><code># 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;MiniMax/MiniMax-H3&quot;,
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;参考视频中的角色缓缓转头，微笑着挥手致意，背景光影柔和流转&quot;,
        &quot;media&quot;: [
            {
                &quot;type&quot;: &quot;image_url&quot;,
                &quot;url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260320/knsple/wan-r2v-role-frame.jpg&quot;
            },
            {
                &quot;type&quot;: &quot;feature&quot;,
                &quot;url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qigswt/wan-r2v-role2.mp4&quot;
            }
        ]
    },
    &quot;parameters&quot;: {
        &quot;resolution&quot;: &quot;768P&quot;,
        &quot;ratio&quot;: &quot;16:9&quot;,
        &quot;duration&quot;: 5,
        &quot;watermark&quot;: true
    }
}'
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="mm505h4rsp1"></a><h4>响应参数</h4><p><strong>output</strong> <code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></td><td><a id="sec-tabs"></a><section><a id="成功响应"></a><section><a id="成功响应-h4"></a><h4>成功响应</h4><p>请保存 task_id，用于查询任务状态与结果。</p><a id="code-block"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
        &quot;task_status&quot;: &quot;PENDING&quot;,
        &quot;task_id&quot;: &quot;0385dc79-5ff8-4d82-bcb6-xxxxxx&quot;
    },
    &quot;request_id&quot;: &quot;4909100c-7b5a-9f92-bfe5-xxxxxx&quot;
}
</code></pre></section><a id="异常响应"></a><section><a id="异常响应-h4"></a><h4>异常响应</h4><p>创建任务失败，请参见<a href="../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-2"></a><pre class="language-json"><code>{
    &quot;code&quot;: &quot;InvalidApiKey&quot;,
    &quot;message&quot;: &quot;No API-key provided.&quot;,
    &quot;request_id&quot;: &quot;7438d53d-6eb8-4596-8835-xxxxxx&quot;
}
</code></pre></section></section></td></tr></tbody></table>

<a id="步骤2-根据任务id查询结果"></a>

<a id="mm601h3step2"></a>

### 步骤2：根据任务ID查询结果

**北京地域**：`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`

> **说明**
>
> -   **轮询建议**：视频生成过程约需数分钟，建议采用**轮询**机制，并设置合理的查询间隔（如 15 秒）来获取结果。
> -   **任务状态流转**：PENDING（排队中）→ RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。
> -   **task\_id 有效期**：**24小时**，超时后将无法查询结果，接口将返回任务状态为`UNKNOWN`。
> -   **RPS 限制**：查询接口默认RPS为20。如需更高频查询或事件通知，建议[配置异步任务回调](../../more-about-models/async-task-api.md)。
> -   **更多操作**：如需批量查询、取消任务等操作，请参见[管理异步任务](../../more-about-models/manage-asynchronous-tasks.md)。

<table><tbody><tr><td><a id="mm624h4qr01"></a><h4>请求参数</h4><a id="mm634h5qr01"></a><h5>请求头（Headers）</h5><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><a id="mm640h5qr02"></a><h5>URL路径参数（Path parameters）</h5><p><strong>task_id</strong> <code>string</code><strong>（必选）</strong></p><p>任务ID。</p></td><td><a id="sec-tabs-2"></a><section><a id="查询任务结果"></a><section><a id="查询任务结果-h4"></a><h4>查询任务结果</h4><p>将<code>{task_id}</code>完整替换为上一步接口返回的<code>task_id</code>的值。<code>task_id</code>查询有效期为24小时，并请将<code>{WorkspaceId}</code>替换为真实的<a href="../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain">业务空间ID</a>。</p><a id="code-block-3"></a><pre class="language-bash"><code>curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id} \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="mm654h4qrs1"></a><h4>响应参数</h4><p><strong>output</strong><code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值-2"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section><strong>轮询过程中的状态流转：</strong><ul><li>PENDING（排队中） → RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。</li><li>初次查询状态通常为 PENDING（排队中）或 RUNNING（处理中）。</li><li>当状态变为 SUCCEEDED 时，响应中将包含生成的视频URL。</li><li>若状态为 FAILED，请检查错误信息并重试。</li><li>若状态为 CANCELED，表示任务已取消，如需继续请重新提交任务。</li><li>若状态为 UNKNOWN，表示任务不存在或状态未知，可能在 task_id 不存在或超过 24 小时有效期后出现。</li></ul><p><strong>submit_time</strong> <code>string</code></p><p>任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>scheduled_time</strong> <code>string</code></p><p>任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>end_time</strong> <code>string</code></p><p>任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>video_url</strong><code>string</code></p><p>视频URL。仅在 task_status 为 SUCCEEDED 时返回。</p><p>视频格式为MP4（H.264 编码）。视频链接有效期30天，但不建议将其作为长期存储依赖，请及时下载。</p><p><strong>orig_prompt</strong> <code>string</code></p><p>原始输入的prompt，对应请求参数<code>prompt</code>。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></div></section><p><strong>usage</strong> <code>object</code></p><p>输出信息统计。只对成功的结果计数。</p><a id="accordion-属性-6"></a><section><p>属性</p><div><p><strong>duration</strong> <code>integer</code></p><p>计费总秒数，等于 input_seconds + output_seconds。</p><p><strong>size</strong> <code>string</code></p><p>生成视频的分辨率。示例值：1344*768。</p><p><strong>SR</strong> <code>string</code></p><p>生成视频的分辨率档位。示例值：768。</p><p><strong>video_count</strong> <code>integer</code></p><p>生成视频的数量。固定为1。</p><p><strong>image_count</strong> <code>integer</code></p><p>计费图片数量。输入图片5张以内免费，返回0；超过5张时返回超出部分的数量（例如输入7张图片，返回2，即7-5=2）。</p><p><strong>input_seconds</strong> <code>integer</code></p><p>输入参考视频的总秒数。所有输入视频的毫秒级时长求和后四舍五入取整。无参考视频时为0。</p><p><strong>output_seconds</strong> <code>integer</code></p><p>输出视频的总秒数。</p><p><strong>total_seconds</strong> <code>integer</code></p><p>总秒数，等于 input_seconds + output_seconds。</p></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p></td><td><a id="sec-tabs-3"></a><section><a id="任务执行成功"></a><section><a id="任务执行成功-h4"></a><h4>任务执行成功</h4><a id="code-block-4"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;bde5ed1a-86de-9fac-xxxx-xxxxxxxxxxxx&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;ca7eaceb-2b00-4f29-xxxx-xxxxxxxxxxxx&quot;,
        &quot;task_status&quot;: &quot;SUCCEEDED&quot;,
        &quot;submit_time&quot;: &quot;2026-08-20 13:54:07.204&quot;,
        &quot;scheduled_time&quot;: &quot;2026-08-20 13:54:07.249&quot;,
        &quot;end_time&quot;: &quot;2026-08-20 13:55:58.633&quot;,
        &quot;video_url&quot;: &quot;https://xxx.oss-cn-shanghai.aliyuncs.com/xxx/output.mp4?Expires=xxx&amp;Signature=YOUR_SIGNATURE&quot;
    },
    &quot;usage&quot;: {
        &quot;SR&quot;: &quot;768&quot;,
        &quot;duration&quot;: 5,
        &quot;image_count&quot;: 0,
        &quot;input_seconds&quot;: 0,
        &quot;output_seconds&quot;: 5,
        &quot;size&quot;: &quot;1344*768&quot;,
        &quot;total_seconds&quot;: 5,
        &quot;video_count&quot;: 1
    }
}
</code></pre></section><a id="任务执行失败"></a><section><a id="任务执行失败-h4"></a><h4>任务执行失败</h4><p>若任务执行失败，task_status将置为 FAILED，并提供错误码和信息。请参见<a href="../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-5"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;e5d70b02-ebd3-98ce-9fe8-759d7d7b107d&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;86ecf553-d340-4e21-af6e-a0c6a421c010&quot;,
        &quot;task_status&quot;: &quot;FAILED&quot;,
        &quot;code&quot;: &quot;InvalidParameter&quot;,
        &quot;message&quot;: &quot;The parameter is invalid xxxxxx&quot;
    }
}
</code></pre></section><a id="任务查询过期"></a><section><a id="任务查询过期-h4"></a><h4>任务查询过期</h4><p>task_id查询有效期为 24 小时，超时后将无法查询，返回以下报错信息。</p><a id="code-block-6"></a><pre class="language-json"><code>{
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
