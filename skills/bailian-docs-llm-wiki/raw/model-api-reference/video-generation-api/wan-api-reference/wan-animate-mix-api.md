# 万相-视频换人API参考

万相-视频换人模型能够依据人物图片和参考视频，将视频中的主角替换为图片中的角色，同时保留原视频的场景、光照和色调，实现无缝换人。

-   **核心功能：** 在不改变原始视频的动作、表情及环境的条件下，将视频中的角色替换为指定图片中的人物。
-   **适用场景：**适用于二次创作、影视后期制作等需要进行角色替换的场景。

<a id="效果示例"></a>

<a id="55a79354d2s4j"></a>

## 效果示例

万相-视频换人模型wan2.2-animate-mix提供标准模式`wan-std`和专业模式`wan-pro`两种服务模式，不同模式在效果和计费上存在差异，详情参见[计费与限流](wan-animate-mix-api.md#ce68f54f7bbqe)。

| 人物图片 | 参考视频 | 输出视频（标准模式**`wan-std`**） | 输出视频（专业模式**`wan-pro`**） |
| --- | --- | --- | --- |
| ![mix\_input\_image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3025528571/p1008733.jpeg) |  |  |  |

<a id="http调用"></a>

<a id="42703589880ts"></a>

## HTTP调用

您需要已[获取与配置 API Key](../../preparations/get-api-key.md)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

> **重要**
>
> 华北2（北京）和新加坡地域拥有独立的 **API Key**与**请求地址**，不可混用，跨地域调用将导致鉴权失败或服务报错。

> **重要**
>
> 阿里云百炼为华北2（北京）、新加坡地域推出了业务空间专属域名，**能够为推理请求提供卓越的性能和更高的稳定性**，建议迁移至新域名：
>
> -   华北2（北京）地域：从 `https://dashscope.aliyuncs.com` 迁移至 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
> -   新加坡地域：从 `https://dashscope-intl.aliyuncs.com` 迁移至 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`
>
> 其中 `{WorkspaceId}` 为您的业务空间 ID，可在阿里云百炼控制台的**业务空间详情**页面查看。现有域名仍可正常使用。

由于视频生成耗时较长，HTTP API采用异步模式，调用流程分两步：

1.  **创建任务获取任务ID**：发送一个请求创建任务，该请求会返回**任务ID（task\_id）**。
2.  **根据任务ID查询结果**：使用task\_id轮询任务状态，直到任务完成并获得视频URL。

<a id="步骤1-创建任务获取任务id"></a>

<a id="db8cf70432oe3"></a>

### 步骤1：创建任务获取任务ID

**北京地域**：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis`

**新加坡地域**：`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

> **说明**
>
> -   创建成功后，使用接口返回的 `task_id` 查询结果，task\_id 有效期为 24 小时。**请勿重复创建任务**，轮询获取即可。
> -   新手指引请参见[Postman](https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api)。

<table><tbody><tr><td><a id="afcd41d2b57zf"></a><h4>请求参数</h4><a id="79473e45c592d"></a><h5>请求头（Headers）</h5><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><p><strong>X-DashScope-Async</strong><code>string</code><strong>（必选）</strong></p><p>异步处理配置参数。HTTP请求只支持异步，<strong>必须设置为</strong><code>enable</code>。</p><div><div><p><strong>重要</strong>缺少此请求头将报错：“current user api does not support synchronous calls”。</p></div></div><a id="66a778d4fbfub"></a><h5>请求体（Request Body）</h5><p><strong>model</strong> <code>string</code> <strong>（必选）</strong></p><p>模型名称，必须设置为<code>wan2.2-animate-mix</code>。</p><p><strong>input</strong> <code>object</code> <strong>（必选）</strong></p><p>视频换人的输入图片和视频。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>image_url</strong> <code>string</code> <strong>（必选）</strong></p><p>人物图片的公网可访问HTTP/HTTPS URL，不能包含中文等非ASCII字符，否则需编码后传入。</p><p>本地文件可通过<a href="../../more-about-models/get-temporary-file-url.md">上传文件获取临时URL</a>。</p><ul><li><strong>格式限制</strong>：JPG、JPEG、PNG、BMP、WEBP</li><li><strong>尺寸限制</strong>：图像的宽度和高度都在<code>[200,4096]</code>像素范围内，宽高比在1:3至3:1范围内。</li><li><strong>大小限制</strong>：不超过5MB</li><li><strong>示例</strong>：<code>https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250919/bhkfor/mix_input_image.jpeg</code></li></ul><p><strong>video_url</strong> <code>string</code> <strong>（必选）</strong></p><p>参考视频的公网可访问HTTP/HTTPS URL，不能包含中文等非ASCII字符，否则需编码后传入。</p><p>本地文件可通过<a href="../../more-about-models/get-temporary-file-url.md">上传文件获取临时URL</a>。</p><p><strong>建议：</strong>更高的分辨率和帧率可有效提升输出视频画质。</p><ul><li><strong>格式限制</strong>：MP4、AVI、MOV</li><li><strong>尺寸限制</strong>：视频的宽度和高度<strong>都</strong>在<code>[200, 2048]</code>像素范围内，宽高比在1:3至3:1范围内。</li><li><strong>大小限制</strong>：不超过200MB</li><li><strong>时长限制</strong>：不小于2s且不大于30s</li><li><strong>示例</strong>：<code>https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250919/wqefue/mix_input_video.mp4</code></li></ul><p><strong>watermark</strong> <code>bool</code>（可选）</p><p>是否添加水印标识，水印位于图片右下角，文案为“通义AI生成”。</p><ul><li><code>false</code>（默认值）：不添加水印。</li><li><code>true</code>：添加水印。</li></ul></div></section><p><strong>parameters</strong> <code>object</code> <strong>（必选）</strong></p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>check_image</strong> <code>bool</code> （可选）</p><p>控制是否在处理前对输入图片进行检查。</p><ul><li><code>true</code>（默认值）：在处理前检查输入图片。</li><li><code>false</code>：跳过检查，直接处理。</li></ul><p><strong>mode</strong> <code>string</code> <strong>（必选）</strong></p><p>服务模式，提供两种选择：</p><ul><li><code>wan-std</code>：标准模式。生成速度快、性价比高，适用于快速预览和基础动画。</li><li><code>wan-pro</code>：专业模式。动画更流畅、画质更优，但处理时间和费用相应增加。</li></ul><p>详情请参见<a href="wan-animate-mix-api.md#55a79354d2s4j">效果示例</a>和<a href="wan-animate-mix-api.md#ce68f54f7bbqe">计费与限流</a>。</p></div></section></td><td><a id="sec-tabs"></a><section><a id="视频换人"></a><section><a id="视频换人-h4"></a><h4>视频换人</h4><p>以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。</p><a id="code-block"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis' \
    --header 'X-DashScope-Async: enable' \
    --header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    --header 'Content-Type: application/json' \
    --data '{
        &quot;model&quot;: &quot;wan2.2-animate-mix&quot;,
        &quot;input&quot;: {
            &quot;image_url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250919/bhkfor/mix_input_image.jpeg&quot;,
            &quot;video_url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250919/wqefue/mix_input_video.mp4&quot;,
            &quot;watermark&quot;: true
        },
        &quot;parameters&quot;: {
            &quot;mode&quot;: &quot;wan-std&quot;
        }
      }'
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="cd3063363egdc"></a><h4>响应参数</h4><p><strong>output</strong> <code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></td><td><a id="sec-tabs-2"></a><section><a id="成功响应"></a><section><a id="成功响应-h4"></a><h4>成功响应</h4><p>请保存 task_id，用于查询任务状态与结果。</p><a id="code-block-2"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
        &quot;task_status&quot;: &quot;PENDING&quot;,
        &quot;task_id&quot;: &quot;0385dc79-5ff8-4d82-bcb6-xxxxxx&quot;
    },
    &quot;request_id&quot;: &quot;4909100c-7b5a-9f92-bfe5-xxxxxx&quot;
}
</code></pre></section><a id="异常响应"></a><section><a id="异常响应-h4"></a><h4>异常响应</h4><p>创建任务失败，请参见<a href="../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-3"></a><pre class="language-json"><code>{
    &quot;code&quot;: &quot;InvalidApiKey&quot;,
    &quot;message&quot;: &quot;No API-key provided.&quot;,
    &quot;request_id&quot;: &quot;7438d53d-6eb8-4596-8835-xxxxxx&quot;
}
</code></pre></section></section></td></tr></tbody></table>

<a id="步骤2-根据任务id查询结果"></a>

<a id="420e6e77a17om"></a>

### 步骤2：根据任务ID查询结果

<a id="sec-tabs-3"></a>

<a id="华北2-北京"></a>

<a id="华北2-北京-h4"></a>

#### 华北2（北京）

`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="新加坡"></a>

<a id="新加坡-h4"></a>

#### 新加坡

`GET https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/tasks/{task_id}`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

> **说明**
>
> -   **轮询建议**：视频生成过程约需数分钟，建议采用**轮询**机制，并设置合理的查询间隔（如 15 秒）来获取结果。
> -   **任务状态流转**：PENDING（排队中）→ RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。
> -   **结果链接**：任务成功后返回视频链接，有效期为 **24 小时**。建议在获取链接后立即下载并转存至永久存储（如[阿里云 OSS](https://help.aliyun.com/zh/oss/user-guide/what-is-oss)）。
> -   **task\_id 有效期**：**24小时**，超时后将无法查询结果，接口将返回任务状态为`UNKNOWN`。
> -   **RPS 限制**：查询接口默认RPS为20。如需更高频查询或事件通知，建议[配置异步任务回调](../../more-about-models/async-task-api.md)。
> -   **更多操作**：如需批量查询、取消任务等操作，请参见[管理异步任务](../../more-about-models/manage-asynchronous-tasks.md)。

<table><tbody><tr><td><a id="eb9c8d77b6xg8"></a><h4>请求参数</h4><a id="36a28b657f196"></a><h5>请求头（Headers）</h5><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><a id="0e29e015d8opn"></a><h5>URL路径参数（Path parameters）</h5><p><strong>task_id</strong> <code>string</code><strong>（必选）</strong></p><p>任务ID。</p></td><td><a id="sec-tabs-4"></a><section><a id="查询任务结果"></a><section><a id="查询任务结果-h4"></a><h4>查询任务结果</h4><p>请将<code>0385dc79-5ff8-4d82-bcb6-xxxxxx</code>替换为真实的task_id。</p><blockquote><p>以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。</p></blockquote><a id="code-block-4"></a><pre class="language-bash"><code>curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/0385dc79-5ff8-4d82-bcb6-xxxxxx \
    --header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="f277d7425foyq"></a><h4>响应参数</h4><p><strong>output</strong><code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值-2"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section><p><strong>submit_time</strong> <code>string</code></p><p>任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>scheduled_time</strong> <code>string</code></p><p>任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>end_time</strong> <code>string</code></p><p>任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>results</strong> <code>object</code></p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>video_url</strong><code>string</code></p><p>视频URL。仅在 task_status 为 SUCCEEDED 时返回。</p><p>链接有效期24小时，可通过此URL下载视频。视频格式为MP4（H.264 编码）。</p></div></section><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></div></section><p><strong>usage</strong> <code>object</code></p><p>仅在任务成功时返回。</p><a id="accordion-属性-6"></a><section><p>属性</p><div><p><strong>video_duration</strong> <code>float</code></p><p>生成视频的时长，单位：秒。</p><p><strong>video_ratio</strong> <code>string</code></p><p>本次请求使用的服务模式。选择标准模式<code>wan-std</code>时返回<code>standard</code>，选择专业模式<code>wan-pro</code>时返回<code>pro</code>。</p></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p></td><td><a id="sec-tabs-5"></a><section><a id="任务执行成功"></a><section><a id="任务执行成功-h4"></a><h4>任务执行成功</h4><p>视频URL仅保留24小时，超时后会被自动清除，请及时保存生成的视频。</p><a id="code-block-5"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;a67f8716-18ef-447c-a286-xxxxxx&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;0385dc79-5ff8-4d82-bcb6-xxxxxx&quot;,
        &quot;task_status&quot;: &quot;SUCCEEDED&quot;,
        &quot;submit_time&quot;: &quot;2025-09-18 15:32:00.105&quot;,
        &quot;scheduled_time&quot;: &quot;2025-09-18 15:32:15.066&quot;,
        &quot;end_time&quot;: &quot;2025-09-18 15:34:41.898&quot;,
        &quot;results&quot;: {
            &quot;video_url&quot;: &quot;http://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxxxx.mp4?Expires=xxxxxx&quot;
        }
    },
    &quot;usage&quot;: {
        &quot;video_duration&quot;: 5.2,
        &quot;video_ratio&quot;: &quot;standard&quot;
    }
}
</code></pre></section><a id="任务执行失败"></a><section><a id="任务执行失败-h4"></a><h4>任务执行失败</h4><p>若任务执行失败，task_status将置为 FAILED，并提供错误码和信息。请参见<a href="../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-6"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;daad9007-6acd-9fb3-a6bc-xxxxxx&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;fe8aa114-d9f1-4f76-b598-xxxxxx&quot;,
        &quot;task_status&quot;: &quot;FAILED&quot;,
        &quot;code&quot;: &quot;InternalError&quot;,
        &quot;message&quot;: &quot;xxxxxx&quot;
    }
}
</code></pre></section></section></td></tr></tbody></table>

<a id="使用限制"></a>

<a id="534013237a77q"></a>

## 使用限制

**数据时效**：任务task\_id和视频URL均只保留 24 小时，过期后将无法查询或下载，请及时[下载视频到本地](wan-animate-mix-api.md)。

**内容审核**：输入与输出内容均会经过内容安全审核，包含违规内容的请求将报错“IPInfringementSuspect”或“DataInspectionFailed”，具体参见[错误码](../../preparations/error-code.md)。

<a id="计费与限流"></a>

<a id="ce68f54f7bbqe"></a>

## 计费与限流

-   模型免费额度和计费单价请参见[模型价格](../../../model-user-guide/test-1/model-pricing.md#86bd5c57adaos)。
    
-   模型限流请参见[万相系列](../../../model-user-guide/get-started-with-models/rate-limit.md)。
    
-   计费说明：
    
    -   输入不计费，输出计费。按成功生成的 **视频秒数** 计费。
    -   模型调用失败或处理错误不产生任何费用，也不消耗[免费额度](../../../model-user-guide/test-1/new-free-quota.md)。

<a id="错误码"></a>

<a id="3d39f89cb0n1a"></a>

## 错误码

如果调用失败，请参见[错误码](../../preparations/error-code.md)。

<a id="常见问题"></a>

<a id="c928ee689aw6l"></a>

## 常见问题

<a id="q-如何查看模型调用量"></a>

<a id="7daf9e8eden75"></a>

#### Q: 如何查看模型调用量？

A: 调用数据存在分钟级延迟。请在模型监控（[北京](https://bailian.console.aliyun.com/cn-beijing/model/telemetry)或[新加坡](https://bailian.console.aliyun.com/ap-southeast-1/model/telemetry)）页面查看调用量、调用次数和成功率等指标。[如何查看模型调用记录？](../../../model-user-guide/test-1/new-free-quota.md#ab6ba5c538rn3)

<a id="q-如何提升生成视频的质量"></a>

<a id="1da0131fc6sha"></a>

#### Q: 如何提升生成视频的质量?

A: 建议：

1.  确保输入图片与参考视频中的人物画幅占比相似。
2.  尽量保持图片和视频中人物的身材比例一致。
3.  使用高清素材，避免使用模糊图片和低帧率视频，确保细节识别准确。

<a id="q-如何将临时的视频链接转为永久链接"></a>

<a id="c257155348vl4"></a>

#### Q: 如何将临时的视频链接转为永久链接？

A: 不支持直接转换。请在后端下载视频文件后上传至对象存储服务（如阿里云 OSS），生成永久访问链接。

<a id="accordion-示例代码-下载视频到本地"></a>

示例代码：下载视频到本地

<a id="code-block-7"></a>

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

<a id="2c24257030bb4"></a>

#### Q: 返回的视频链接可以在浏览器中直接播放吗？

A: 不建议直接播放，链接会在 24 小时后失效。请在后端下载转存后，使用永久链接播放。

<a id="q-如何获取视频存储的访问域名白名单"></a>

<a id="c7421e6e32dj8"></a>

#### Q：如何获取视频存储的访问域名白名单？

A： 模型生成的视频存储于阿里云OSS，API将返回一个临时的公网URL。**若需要对该下载地址进行防火墙白名单配置**，请注意：由于底层存储会根据业务情况进行动态变更，为避免过期信息影响访问，文档不提供固定的OSS域名白名单。如有安全管控需求，请联系客户经理获取最新OSS域名列表。
