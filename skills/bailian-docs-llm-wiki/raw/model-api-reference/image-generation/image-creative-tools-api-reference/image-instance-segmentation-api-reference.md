# 人物实例分割API参考

本文介绍人物实例分割模型的输入输出参数。人物实例分割运用了检测和分割技术，不仅能够在图像中识别出不同的对象，而且还能准确地画出每一个对象边界的像素级掩码（mask）。

**相关指南**：[人物实例分割](../../../model-user-guide/use-cases/legacy-resources/legacy-image-generation/image-instance-segmentation.md)

> **重要**
>
> -   本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。
> -   image-instance-segmentation 模型当前仅提供**免费体验**，免费额度用完后不可调用且不支持付费。

<a id="模型概览"></a>

<a id="a0c22dbf96vss"></a>

## 模型概览

<table><tbody><tr><td rowspan="2"><strong>模型名</strong></td><td rowspan="2"><p><strong>免费额度</strong><a href="../../../model-user-guide/test-1/new-free-quota.md">（查看）</a></p></td><td rowspan="2"><strong>计费单价</strong></td><td colspan="2"><strong>限流（含主账号与RAM子账号）</strong></td></tr><tr><td><strong>任务下发接口QPS限制</strong></td><td><strong>同时处理中任务数量</strong></td></tr><tr><td><p>image-instance-segmentation</p></td><td><p>500张</p></td><td><p>目前仅供免费体验。</p><blockquote><p>免费额度用完后不可调用，敬请关注后续动态。</p></blockquote></td><td><p>2</p></td><td><p>1</p></td></tr></tbody></table>

<a id="前提条件"></a>

<a id="5167b4367apns"></a>

## 前提条件

您需要已[获取与配置 API Key](../../preparations/get-api-key.md)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

<a id="http调用"></a>

<a id="42703589880ts"></a>

## HTTP调用

为了减少等待时间并且避免请求超时，服务采用异步方式提供。您需要发起两个请求：

-   **创建任务**：首先发送一个请求创建人物实例分割任务，该请求会返回任务ID。
-   **根据任务ID查询结果**：使用上一步获得的任务ID，查询模型生成的结果。

<a id="步骤1-创建任务获取任务id"></a>

<a id="bde0fc73feflg"></a>

### 步骤1：创建任务获取任务ID

`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<table><tbody><tr><td><a id="afcd41d2b57zf"></a><h4>请求头（Headers）</h4><p><strong>Content-Type</strong><em>string</em><strong>必选</strong></p><p>请求内容类型。固定为<code>application/json</code>。</p><p><strong>Authorization</strong><em>string</em><strong>必选</strong></p><p>推荐您使用阿里云百炼API-Key，也可填DashScope API-Key。例如：Bearer d1xxx2a。</p><p><strong>X-DashScope-Async</strong><em>string</em><strong>必选</strong></p><p>是否开启异步处理。必须开启异步处理，设置为<code>enable</code>。</p><a id="66a778d4fbfub"></a><h4>请求体（Request Body）</h4><p><strong>model</strong><em>string</em><strong>必选</strong></p><p>调用模型。</p><p><strong>input</strong><em>object</em><strong>必选</strong></p><p>输入图像的基本信息，比如图像URL。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>image_url</strong><em>string</em><strong>必选</strong></p><p>输入图像URL地址。</p><p>URL 需为公网可访问的地址，并支持 HTTP 或 HTTPS 协议。您也可在此<a href="../../more-about-models/get-temporary-file-url.md">获取临时公网URL</a>。</p><p>图像限制：</p><ul><li>图片格式：JPEG，PNG，JPG，BMP，WEBP。</li><li>图像分辨率：不低于512×512像素且不超过4096×4096像素。</li><li>图像单边长度范围：[512, 4096]，单位像素。</li><li>图片大小：不超过10M。</li><li>URL地址中不能包含中文字符。</li></ul></div></section></td><td><a id="sec-tabs"></a><section><a id="人物实例分割"></a><section><a id="人物实例分割-h4"></a><h4>人物实例分割</h4><a id="code-block"></a><pre class="language-bash"><code># 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location --request POST 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
--header 'X-DashScope-Async: enable' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data-raw '{
    &quot;model&quot;: &quot;image-instance-segmentation&quot;,
    &quot;input&quot;: {
            &quot;image_url&quot;: &quot;http://xxx/image.png&quot;
        },
    &quot;parameters&quot;:{
    }
}'
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="9ea3a66e2a0uv"></a><h4>响应</h4><p><strong>output</strong><em>object</em></p><p>任务输出信息。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>task_id</strong><em>string</em></p><p>任务id，任务唯一标识。</p><p><strong>task_status</strong><em>string</em></p><p>任务状态。</p><ul><li>PENDING：排队中</li><li>RUNNING：处理中</li><li>SUSPENDED：挂起</li><li>SUCCEEDED：执行成功</li><li>FAILED：执行失败</li></ul></div></section><p><strong>code</strong><em>string</em></p><p>接口错误码。接口成功请求不会返回该参数。</p><p><strong>message</strong><em>string</em></p><p>接口错误信息。接口成功请求不会返回该参数。</p><p><strong>request_id（可选）</strong><em>string</em></p><p>本次请求的系统唯一码。</p></td><td><a id="fig-code-group"></a><div><a id="fig-code-group-成功响应-tab"></a>成功响应<div><a id="code-code-group-成功响应"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
        &quot;task_status&quot;: &quot;PENDING&quot;,
        &quot;task_id&quot;: &quot;53950fb7-281a-4e60-xxxxxxxxxxxx&quot;
    },
    &quot;request_id&quot;: &quot;1027557e-8c3f-9db5-8cd2-xxxxxxxxxxxx&quot;
}
</code></pre></div><a id="fig-code-group-异常响应-tab"></a>异常响应<div><a id="code-code-group-异常响应"></a><pre class="language-json"><code>{
    &quot;code&quot;:&quot;InvalidApiKey&quot;,
    &quot;message&quot;:&quot;Invalid API-key provided.&quot;,
    &quot;request_id&quot;:&quot;fb53c4ec-1c12-4fc4-a580-xxxxxxxxxxxx&quot;
}
</code></pre></div></div></td></tr></tbody></table>

<a id="步骤2-根据任务id查询结果"></a>

<a id="481754a27e8sb"></a>

### 步骤2：根据任务ID查询结果

`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<table><tbody><tr><td><a id="5043fa882c26r"></a><h4>请求头（Headers）</h4><p><strong>Authorization</strong><em>string</em><strong>必选</strong></p><p>API-Key，例如：Bearer d1**2a。</p><a id="aa6a7e4730pr2"></a><h4>URL路径参数（Path parameters）</h4><p><strong>task_id</strong><em>string</em><strong>必选</strong></p><p>任务id。</p></td><td><a id="sec-tabs-2"></a><section><a id="获取任务结果"></a><section><a id="获取任务结果-h4"></a><h4>获取任务结果</h4><a id="code-block-2"></a><pre class="language-bash"><code># 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl -X GET \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/53950fb7-281a-4e60-xxxxxxxxxxxx
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="b14ec019d4k6f"></a><h4>响应</h4><p><strong>request_id</strong><em>string</em></p><p>本次请求的系统唯一码。</p><p><strong>status_code</strong><em>int</em></p><p>200（HTTPStatus.OK）表示请求成功，否则表示请求失败，可以通过code获取错误码，通过message字段获取错误详细信息。</p><p><strong>code</strong><em>string</em></p><p>如果失败表示错误码，参考错误码表。</p><p><strong>message</strong><em>string</em></p><p>如果失败，内容为失败详细信息。</p><p><strong>output</strong><em>object</em></p><p>任务输出信息。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>task_id</strong><em>string</em></p><p>任务id。</p><p><strong>task_status</strong><em>string</em></p><p>任务状态。</p><ul><li>PENDING：排队中。</li><li>RUNNING：处理中。</li><li>SUCCEEDED：成功。</li><li>FAILED：失败。</li><li>UNKNOWN：任务不存在或状态未知。</li></ul><p><strong>output_image_url</strong><em>string</em></p><p>分割后图像URL地址。限制输出图像长宽比范围为1:10-10:1。</p><p><strong>output_vis_image_url</strong><em>string</em></p><p>分割后可视化图像的URL地址，限制输出图像长宽比范围为1:10-10:1。</p></div></section><p><strong>usage</strong><em>object</em></p><p>输出信息统计。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>image_count</strong><em>integer</em></p><p>本次请求生成图像数量。</p></div></section></td><td><a id="sec-tabs-3"></a><section><a id="任务执行成功"></a><section><a id="任务执行成功-h4"></a><h4>任务执行成功</h4><p>对于本模型，任务在结束之后的状态会持续保留24小时以备客户随时查询，24小时之后，任务将从系统中清除，相关的结果也将一并清除；对应的，任务生成的结果为图像的URL地址，出于安全考虑，该URL的下载有效期也是24小时，需要用户在获取任务结果后根据需要及时使用或者转存。</p><a id="code-block-3"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;b67df059-ca6a-9d51-afcd-9b3c4456b1e2&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;53950fb7-281a-4e60-xxxxxxxxxxxx&quot;,
        &quot;task_status&quot;: &quot;SUCCEEDED&quot;,
        &quot;submit_time&quot;: &quot;2024-05-16 13:50:01.247&quot;,
        &quot;scheduled_time&quot;: &quot;2024-05-16 13:50:01.354&quot;,
        &quot;end_time&quot;: &quot;2024-05-16 13:50:27.795&quot;,
        &quot;output_image_url&quot;: &quot;http://xxx/result1.png&quot;,
        &quot;output_vis_image_url&quot;:&quot;http://xxx/result2.png&quot;
    },
    &quot;usage&quot;: {
        &quot;image_count&quot;: 1
    }
}
</code></pre></section><a id="任务执行中"></a><section><a id="任务执行中-h4"></a><h4>任务执行中</h4><a id="code-block-4"></a><pre class="language-json"><code>{
    &quot;request_id&quot;:&quot;7574ee8f-38a3-4b1e-xxxxxxxxxxxx&quot;,
    &quot;output&quot;:{
        &quot;task_id&quot;:&quot;53950fb7-281a-4e60-xxxxxxxxxxxx&quot;,
        &quot;task_status&quot;:&quot;RUNNING&quot;,
        &quot;task_metrics&quot;:{
            &quot;TOTAL&quot;:1,
            &quot;SUCCEEDED&quot;:1,
            &quot;FAILED&quot;:0
        }
    }
}
</code></pre></section><a id="任务执行失败"></a><section><a id="任务执行失败-h4"></a><h4>任务执行失败</h4><a id="code-block-5"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;dccfdf23-b38e-97a6-a07b-f35118c1ada6&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;53950fb7-281a-4e60-xxxxxxxxxxxx&quot;,
        &quot;task_status&quot;: &quot;FAILED&quot;,
        &quot;submit_time&quot;: &quot;2024-05-16 14:15:14.103&quot;,
        &quot;scheduled_time&quot;: &quot;2024-05-16 14:15:14.154&quot;,
        &quot;end_time&quot;: &quot;2024-05-16 14:15:14.694&quot;,
        &quot;code&quot;: &quot;InvalidParameter.FileDownload&quot;,
        &quot;message&quot;: &quot;download for input_image error&quot;
    }
}
</code></pre></section></section></td></tr></tbody></table>

<a id="补充-如何从人物实例分割掩码图中获取保留人物和待擦除人物掩码图"></a>

<a id="RWDRR"></a>

## 补充：如何从人物实例分割掩码图中获取保留人物和待擦除人物掩码图？

以下代码示例将得到的人物实例分割结果图拆分成擦除区域图以及保留区域图，后续调用图像擦除模型擦除不需要的人像。

| 原图 | 人物实例分割结果 | 保留区域 | 擦除区域 |
| --- | --- | --- | --- |
| ![图片擦除2-原图.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0184161571/p840837.png) | ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6043984271/p841094.png)<br><br>mask.png | ![图片擦除2-保留.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0184161571/p840841.png)<br><br>reserve.png | ![图片擦除2-擦除.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0184161571/p840839.png)<br><br>remove.png |

<a id="code-block-6"></a>

```python
import cv2
import numpy as np

def get_remove_mask(mask_path, remove_mask_path, reserve_ids=[]):
    mask = cv2.imread(mask_path)
    instance_num = int(mask.max())
    new_mask = np.zeros((mask.shape[0], mask.shape[1], 3))
    for i in range(1, instance_num+1):
        if i in reserve_ids:
            continue
        new_mask[mask[:, :, 0] == i] = (255, 255, 255)
    cv2.imwrite(remove_mask_path, new_mask.astype(np.uint8))

def get_reserve_mask(mask_path, reserve_mask_path, reserve_ids=[]):
    mask = cv2.imread(mask_path)
    instance_num = int(mask.max())
    new_mask = np.zeros((mask.shape[0], mask.shape[1], 3))
    for i in range(1, instance_num + 1):
        if i in reserve_ids:
            new_mask[mask[:,:,0] == i]  = (255, 255, 255)
    cv2.imwrite(reserve_mask_path, new_mask.astype(np.uint8))

if __name__ == '__main__':
    mask_path = 'mask.png'
    remove_mask_path = 'remove.png'
    reserve_mask_path = 'reserve.png'
    get_remove_mask(mask_path, remove_mask_path, reserve_ids=[1])
    get_reserve_mask(mask_path, reserve_mask_path, reserve_ids=[1])
```

<a id="错误码"></a>

<a id="OajFO"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](../../preparations/error-code.md)进行解决。

此API还有特定状态码，具体如下所示。

| HTTP状态码 | 接口错误码（code） | 接口错误信息（message） | 含义说明 |
| --- | --- | --- | --- |
| 400 | InvalidParameter.JsonPhrase | input json error | 输入JSON错误 |
| 400 | InvalidParameter.FileDownload | oss download error | 输入图像下载失败 |
| 400 | InvalidParameter.ImageFormat | read image error | 读取图像失败 |
| 400 | InvalidParameter.ImageContent | The image content does not comply with green network verification. | 图像内容不合规 |
| 400 | InvalidParameter | the parameters must conform to the specification: xxx | 输入参数超出范围 |
| 500 | InternalError.Algo | algorithm process error | 算法错误 |
| 500 | InternalError.FileUpload | oss upload error | 文件上传失败 |
