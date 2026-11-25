# 万相-图生动作API参考

基于人物图片和参考视频，生成人物动作视频。

-   **功能简述：**将参考视频中的动作和表情迁移到人物图片，生成动态视频。
-   **适用场景：**舞蹈复刻、高难度肢体动作复刻、影视表演复刻，可作为动作捕捉的低成本替代方案。

<a id="模型效果"></a>

<a id="55a79354d2s4j"></a>

## 模型效果

wan2.2-animate-move 提供两种服务模式：标准模式`wan-std`和专业模式`wan-pro`，两种模式在画质效果和计费上有所不同，详见[万相-图生动作](../../../model-user-guide/test-1/model-pricing.md#1f708fcd62rdc)。

| 人物图片 | 参考视频 | 输出视频（标准模式**`wan-std`**） | 输出视频（专业模式**`wan-pro`**） |
| --- | --- | --- | --- |
| ![move\_input\_image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9815528571/p1008736.jpeg) |  |  |  |

<a id="前提条件"></a>

<a id="9525c5218erzx"></a>

## 前提条件

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

<a id="http调用"></a>

<a id="42703589880ts"></a>

## HTTP调用

视频生成任务耗时较长，API 采用异步调用，分为两个步骤：创建任务，然后轮询获取结果。

<a id="步骤1-创建任务获取任务id"></a>

<a id="db8cf70432oe3"></a>

### 步骤1：创建任务获取任务ID

**北京地域**：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis`

**新加坡地域**：`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis`

> **说明**
>
> -   创建成功后，使用接口返回的 `task_id` 查询结果，task\_id 有效期为 24 小时。**请勿重复创建任务**，轮询获取即可。
> -   新手指引请参见[Postman](https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api)。

<table><tbody><tr><td><a id="afcd41d2b57zf"></a><h4>请求参数</h4><a id="79473e45c592d"></a><h5>请求头（Headers）</h5><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><p><strong>X-DashScope-Async</strong><code>string</code><strong>（必选）</strong></p><p>异步处理配置参数。HTTP请求只支持异步，<strong>必须设置为</strong><code>enable</code>。</p><div><div><p><strong>重要</strong>缺少此请求头将报错：“current user api does not support synchronous calls”。</p></div></div><a id="66a778d4fbfub"></a><h5>请求体（Request Body）</h5><p><strong>model</strong> <code>string</code> <strong>（必选）</strong></p><p>模型名称，固定填写<code>wan2.2-animate-move</code>。</p><p><strong>input</strong> <code>object</code> <strong>（必选）</strong></p><p>输入参数对象，包含以下字段：</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>image_url</strong> <code>string</code> <strong>（必选）</strong></p><p>人物图片的公网可访问 HTTP/HTTPS 链接。URL 中若含中文等非 ASCII 字符，需先进行URL编码。</p><p>本地文件可通过<a href="../../more-about-models/get-temporary-file-url.md">上传文件获取临时URL</a>。</p><ul><li><strong>格式</strong>：JPG、JPEG、PNG、BMP、WEBP。</li><li><strong>尺寸</strong>：宽高均在<code>[200, 4096]</code>像素范围内，宽高比在 1:3 至 3:1 之间。</li><li><strong>文件大小</strong>：不超过 5 MB。</li><li><strong>示例值</strong>：<code>https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250919/adsyrp/move_input_image.jpeg</code></li></ul><p><strong>video_url</strong> <code>string</code> <strong>（必选）</strong></p><p>参考视频的公网可访问 HTTP/HTTPS 链接。URL 中若含中文等非 ASCII 字符，需先进行URL编码。</p><p>本地文件可通过<a href="../../more-about-models/get-temporary-file-url.md">上传文件获取临时URL</a>。</p><p><strong>建议：</strong>使用高分辨率、高帧率的参考视频，可有效提升生成视频的画质效果。</p><ul><li><strong>格式</strong>：MP4、AVI、MOV。</li><li><strong>时长</strong>：2～30 秒。</li><li><strong>尺寸</strong>：宽高均在<code>[200, 2048]</code>像素范围内，宽高比在 1:3 至 3:1 之间。</li><li><strong>文件大小</strong>：不超过 200 MB。</li><li><strong>示例值</strong>：<code>https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250919/kaakcn/move_input_video.mp4</code></li></ul><p><strong>watermark</strong> <code>bool</code>（可选）</p><p>是否在视频右下角添加&quot;千问AI生成&quot;水印。</p><ul><li><code>false</code>（默认值）：不添加水印。</li><li><code>true</code>：添加水印。</li></ul></div></section><p><strong>parameters</strong> <code>object</code> <strong>（必选）</strong></p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>check_image</strong> <code>bool</code> （可选）</p><p>是否对输入图片进行检测。</p><ul><li><code>true</code>：<strong>默认值</strong>，检测传入的图片。</li><li><code>false</code>：跳过图片检测，直接处理。</li></ul><p><strong>mode</strong> <code>string</code> <strong>（必选）</strong></p><p>服务模式，支持以下两种：</p><ul><li><code>wan-std</code>：标准模式，生成速度快、性价比高，适合快速预览和基础动画场景。</li><li><code>wan-pro</code>：专业模式，动画流畅度更高、效果更佳，处理时间和费用相应增加。</li></ul><p>详情请参见<a href="wan-animate-move-api.md#55a79354d2s4j">模型效果</a>和<a href="wan-animate-move-api.md#ce68f54f7bbqe">计费与限流</a>。</p></div></section></td><td><a id="sec-tabs"></a><section><a id="图生动作"></a><section><a id="图生动作-h4"></a><h4>图生动作</h4><p>以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。</p><a id="code-block"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis' \
    --header 'X-DashScope-Async: enable' \
    --header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    --header 'Content-Type: application/json' \
    --data '{
        &quot;model&quot;: &quot;wan2.2-animate-move&quot;,
        &quot;input&quot;: {
            &quot;image_url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250919/adsyrp/move_input_image.jpeg&quot;,
            &quot;video_url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250919/kaakcn/move_input_video.mp4&quot;,
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

<table><tbody><tr><td><a id="eb9c8d77b6xg8"></a><h4>请求参数</h4><a id="36a28b657f196"></a><h5>请求头（Headers）</h5><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><a id="0e29e015d8opn"></a><h5>URL路径参数（Path parameters）</h5><p><strong>task_id</strong> <code>string</code><strong>（必选）</strong></p><p>任务ID。</p></td><td><a id="sec-tabs-4"></a><section><a id="查询任务结果"></a><section><a id="查询任务结果-h4"></a><h4>查询任务结果</h4><p>将<code>0385dc79-5ff8-4d82-bcb6-xxxxxx</code>替换为实际的 task_id。</p><blockquote><p>以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。</p></blockquote><a id="code-block-4"></a><pre class="language-bash"><code>curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/0385dc79-5ff8-4d82-bcb6-xxxxxx \
    --header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="f277d7425foyq"></a><h4>响应参数</h4><p><strong>output</strong><code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值-2"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section><p><strong>submit_time</strong> <code>string</code></p><p>任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>scheduled_time</strong> <code>string</code></p><p>任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>end_time</strong> <code>string</code></p><p>任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>results</strong> <code>object</code></p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>video_url</strong><code>string</code></p><p>视频URL。仅在 task_status 为 SUCCEEDED 时返回。</p><p>链接有效期24小时，可通过此URL下载视频。视频格式为MP4（H.264 编码）。</p></div></section><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></div></section><p><strong>usage</strong> <code>object</code></p><p>用量统计信息，仅统计成功的请求。</p><a id="accordion-属性-6"></a><section><p>属性</p><div><p><strong>video_duration</strong> <code>float</code></p><p>本次请求生成视频的时长，单位：秒。</p><p><strong>video_ratio</strong> <code>string</code></p><p>本次请求所用的服务模式标识，枚举值：<code>standard</code>、<code>pro</code>。</p><p>标准模式<code>wan-std</code>对应<code>standard</code>，专业模式<code>wan-pro</code>对应<code>pro</code>。</p></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p></td><td><a id="sec-tabs-5"></a><section><a id="任务执行成功"></a><section><a id="任务执行成功-h4"></a><h4>任务执行成功</h4><p>视频URL仅保留24小时，超时后会被自动清除，请及时保存生成的视频。</p><a id="code-block-5"></a><pre class="language-json"><code>{
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

**数据时效**：task\_id 和视频URL均只保留 24 小时，请及时[下载视频到本地](wan-animate-move-api.md)，过期后将无法查询或访问。

**内容审核**：输入和输出内容均会经过内容安全审核，包含违规内容的请求将返回 `IPInfringementSuspect` 或 `DataInspectionFailed` 错误，详见[错误码](../../preparations/error-code.md)。

<a id="计费与限流"></a>

<a id="ce68f54f7bbqe"></a>

## 计费与限流

-   免费额度和计费单价，请参见[万相-图生动作](../../../model-user-guide/test-1/model-pricing.md#1f708fcd62rdc)。
    
-   模型限流，请参见[万相系列](../../../model-user-guide/get-started-with-models/rate-limit.md)。
    
-   计费说明：
    
    -   输入不计费，输出按成功生成的视频秒数计费。
    -   调用失败不产生任何费用，也不消耗[新人免费额度](../../../model-user-guide/test-1/new-free-quota.md)。

<a id="错误码"></a>

<a id="3d39f89cb0n1a"></a>

## 错误码

调用失败时，请参见[错误码](../../preparations/error-code.md)排查解决。

<a id="常见问题"></a>

<a id="c928ee689aw6l"></a>

## 常见问题

<a id="q-如何优化生成视频的效果"></a>

<a id="1da0131fc6sha"></a>

#### Q: 如何优化生成视频的效果?

可参考以下建议：

1.  确保输入图片与参考视频中的人物画幅占比相近。
2.  保持图片和视频中人物的身材比例一致。
3.  使用高清素材，避免模糊图片和低帧率视频，以确保细节识别准确。

<a id="q-如何将临时的视频链接转为永久链接"></a>

<a id="c257155348vl4"></a>

#### Q: 如何将临时的视频链接转为永久链接？

无法直接转换该链接。正确做法是：后端获取到视频URL后，通过代码下载视频文件，再上传至永久对象存储（如阿里云 OSS），生成新的永久访问链接。

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

不建议。视频链接 24 小时后失效，最佳实践是后端下载转存后，通过永久链接提供视频播放。

<a id="q-如何获取视频存储的访问域名白名单"></a>

<a id="c7421e6e32dj8"></a>

#### Q：如何获取视频存储的访问域名白名单？

A： 模型生成的视频存储于阿里云OSS，API将返回一个临时的公网URL。**若需要对该下载地址进行防火墙白名单配置**，请注意：由于底层存储会根据业务情况进行动态变更，为避免过期信息影响访问，文档不提供固定的OSS域名白名单。如有安全管控需求，请联系客户经理获取最新OSS域名列表。
