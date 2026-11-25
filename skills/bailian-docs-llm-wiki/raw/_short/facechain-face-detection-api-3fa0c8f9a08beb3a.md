# 人物图像检测API详情

> **重要**
>
> 本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。

<a id="人物图像检测"></a>

<a id="40e48c80477de"></a>

## 人物图像检测

> **说明**
>
> 支持的领域 / 任务：aigc /facechain人物写真生成

对用户上传的人物图像进行检测，判断其中所包含的人脸是否符合facechain微调所需的标准，检测维度包括人脸数量、大小、角度、光照、清晰度等多维度，支持图像组输入，并返回每张图像对应的检测结果。

该模型非任务流程强制环节，可以根据业务需要自行选择是否接入。

<a id="选择图像建议"></a>

<a id="9bf8700077wmy"></a>

#### 选择图像建议

1.  人脸数量：1个人脸，不支持多人脸、不支持无人脸图像；
2.  人脸质量：建议为正面人脸，面部大于128\*128像素，无墨镜、手部等遮挡，不要有浓妆和过度美颜；
3.  图像质量：图像分辨率大于256_256，小于4096_4096，文件大小不超过5MB，图像清晰，没有复杂的光线和阴影关系；

![20231030192317.jpg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2490768961/p733107.jpg)

<a id="模型概览"></a>

<a id="ad4a5f601bhtp"></a>

## 模型概览

|  |  |
| --- | --- |
| 模型名 | 模型简介 |
| facechain-facedetect | 对用户上传的人物图像进行检测，判断其中所包含的人脸是否符合facechain微调所需的标准，检测维度包括人脸数量、大小、角度、光照、清晰度等多维度，支持图像组输入，并返回每张图像对应的检测结果。 |

<a id="http调用接口"></a>

<a id="08675ef11bhvi"></a>

## HTTP调用接口

<a id="功能描述"></a>

<a id="8f79b5d0f8ker"></a>

### 功能描述

本模型为同步接口，在提交任务后会返回对应的作业结果。

<a id="前提条件"></a>

<a id="48063821f9diz"></a>

### 前提条件

-   已开通服务并获得API-KEY：[获取与配置 API Key](../model-api-reference/preparations/get-api-key.md)。

> **说明**
>
> 接口限制：对单账户（含主账号与RAM子账号）任务下发接口限制QPS为5。

<a id="作业提交接口调用"></a>

<a id="cd5c7c20fb74b"></a>

### 作业提交接口调用

POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/vision/facedetection/detect

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="入参描述"></a>

<a id="25745d61fbx49"></a>

### 入参描述

<table><thead><tr><th><strong>传参方式</strong></th><th><strong>字段</strong></th><th><strong>类型</strong></th><th><strong>必选</strong></th><th><strong>描述</strong></th><th><strong>示例值</strong></th></tr></thead><tbody><tr><td rowspan="2"><p>Header</p></td><td><p>Content-Type</p></td><td><p><em>String</em></p></td><td><p>是</p></td><td><p>请求类型：application/json</p></td><td><p>application/json</p></td></tr><tr><td><p>Authorization</p></td><td><p><em>String</em></p></td><td><p>是</p></td><td><p>API-Key，例如：Bearer d1**2a</p></td><td><p>Bearer d1**2a</p></td></tr><tr><td rowspan="2"><p>Body</p></td><td><p>model</p></td><td><p><em>String</em></p></td><td><p>是</p></td><td><p>指明需要调用的模型，固定值</p></td><td><p>facechain-facedetect</p></td></tr><tr><td><p>input.images</p></td><td><p><em>Array</em></p></td><td><p>是</p></td><td><p>输入的图像 URL，分辨率不小于256<em>256，不超过4096</em>4096，文件大小不超过5MB, 支持格式包括JPEG, PNG, JPG, WEBP。</p><p>URL 需为公网可访问的地址，并支持 HTTP 或 HTTPS 协议。您也可在此<a href="../model-api-reference/more-about-models/get-temporary-file-url.md">获取临时公网URL</a>。</p><div><div><p><strong>重要</strong>图片URL中如果包含非ASCII字符（如中文文件名），需要先进行URL编码（percent-encoding），否则可能导致</p><a id="code-block"></a><pre class="language-text"><code>InternalError.Algo
</code></pre><p>错误。例如，在Python中使用</p><a id="code-block-2"></a><pre class="language-text"><code>urllib.parse.quote()
</code></pre><p>，在JavaScript中使用</p><a id="code-block-3"></a><pre class="language-text"><code>encodeURI()
</code></pre><p>对URL进行编码。</p></div></div></td><td><p>&quot;images&quot;: [ &quot;<a href="http://a/a.jpg">http://a/a.jpg</a>&quot;,</p><p>&quot;<a href="http://b/b.jpg"></a><a href="http://b/b.jpg">http://b/b.jpg</a>&quot;,</p><p>&quot;<a href="http://c/c.jpg"></a><a href="http://c/c.jpg">http://c/c.jpg</a>&quot;,</p><p>]</p></td></tr></tbody></table>

<a id="出参描述"></a>

<a id="58595f510c3zl"></a>

### 出参描述

<table><thead><tr><th><p><strong>字段</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td><p>output.is_face</p></td><td><p><em>Array</em></p></td><td><p>客户提交的图像列表对应的检测结果，与输入图像顺序一一对应。</p><ul><li><p>true：检测通过。</p></li><li><p>false：检测不通过。</p></li></ul></td><td><p>&quot;is_face&quot;:[</p><p>true,</p><p>true,</p><p>false,</p><p>false</p><p>]</p></td></tr><tr><td><p>output.failed_reason</p></td><td><p><em>Array</em></p></td><td><p>图像检测不通过的原因。</p></td><td><p>no face detected</p></td></tr><tr><td><p>usage</p></td><td><p><em>Object</em></p></td><td><p>本次请求的计费用量统计信息。由于目前facechain-facedetect模型处于限时免费阶段，因此用量信息显示为空。</p></td><td><p>-</p></td></tr><tr><td><p>request_id</p></td><td><p><em>String</em></p></td><td><p>本次请求的系统唯一码。</p></td><td><p>7574ee8f-38a3-4b1e-9280-11c33ab46e51</p></td></tr></tbody></table>

<a id="请求示例"></a>

<a id="43f1fc511b2wv"></a>

### 请求示例

以下示例展示通过CURL命令来调用本模型的脚本

> **说明**
>
> 需要使用您的API-KEY替换示例中的_your-dashscope-api-key_，代码才能正常运行。

<a id="code-block-4"></a>

```bash
curl --location --request POST 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/vision/facedetection/detect' \
--header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
--header 'Content-Type: application/json' \
--data '{
  "model": "facechain-facedetect",
  "input": {
    "images": [
      "http://finetune-swap-wulanchabu.oss-cn-wulanchabu.aliyuncs.com/zhicheng/tmp/1E1D5AFA-3C3A-4B6F-ABD6-8742CA983C42.png",
      "http://finetune-swap-wulanchabu.oss-cn-wulanchabu.aliyuncs.com/zhicheng/tmp/3.JPG",
      "http://finetune-swap-wulanchabu.oss-cn-wulanchabu.aliyuncs.com/zhicheng/tmp/F2EA3984-6EE2-44CD-928F-109B7276BCB6.png"
    ]
  },
  "parameters": {
  }
}'
```

<a id="响应示例"></a>

<a id="d647dd20fb5t4"></a>

### 响应示例

<a id="code-block-5"></a>

```json
{
  "output": {
    "is_face": [true, false, true],
    "failed_reason": ["", "no face detected", ""]
  },
  "usage": {},
  "request_id": "549e0573-f630-9c17-8df2-08f605b4a646"
}
```

<a id="异常响应示例"></a>

<a id="70d006711btg7"></a>

### 异常响应示例

在提交作业请求出错的情况下，输出的结果中会通过 code 和 message 指明出错原因。

<a id="code-block-6"></a>

```json
{
    "code":"InvalidApiKey",
    "message":"Invalid API-key provided.",
    "request_id":"fb53c4ec-1c12-4fc4-a580-cdb7c3261fc1"
}
```

<a id="状态码说明"></a>

<a id="9c31ff011bxae"></a>

## 状态码说明

大模型服务平台通用状态码请查阅：[错误码](../model-api-reference/preparations/error-code.md)

|  |  |  |  |
| --- | --- | --- | --- |
| http 返回码\* | 错误码（code） | 错误信息（message） | 含义说明 |
| **400** | **InvalidParameter** | Required parameter(s) missing or invalid, please check the request parameters. | 接口调用参数不合法 |
| **500** | **InternalError.Algo** | InternalError.Algo | 服务内部算法执行异常。常见原因为输入的图片URL包含非ASCII字符（如中文），请对URL进行编码处理后重试。 |
