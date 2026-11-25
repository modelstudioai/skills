# VideoRetalk 视频生成 API参考

声动人像VideoRetalk是一个人物视频生成模型，可基于人物视频和人声音频，生成人物讲话口型与输入音频相匹配的新视频。本文档介绍了该模型提供的视频生成能力的API调用方法。

> **重要**
>
> 本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。

<a id="http调用接口"></a>

<a id="a36070fcff2bv"></a>

## HTTP调用接口

<a id="videoretalk视频生成api仅支持通过http进行调用-为了减少等待时间并且避免请求超时-采用了异步处理方法-因此-您需要发起两个请求来生成视频"></a>

<a id="b188c19ebb602"></a>

## VideoRetalk视频生成API仅支持通过HTTP进行调用。为了减少等待时间并且避免请求超时，采用了异步处理方法。因此，您需要发起两个请求来生成视频。

-   [作业提交接口](videoretalk-api.md#99d4e18b3e9hc)：您需要先发送一个请求来创建视频生成任务。任务提交后，将返回该任务ID。
-   [作业任务状态查询和结果获取接口](videoretalk-api.md#c89331030e0y3)：使用上一步获得的任务ID，再发送一个请求，获取任务状态及生成的视频。

<a id="前提条件"></a>

<a id="31548f9be6np9"></a>

### 前提条件

您需要已[获取与配置 API Key](../../../preparations/get-api-key.md)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

<a id="输入限制"></a>

<a id="453159b867r4g"></a>

### 输入限制

-   视频要求：
    
    -   文件限制：支持mp4、avi、mov，文件≤300MB，2秒＜时长＜120秒。
    -   视频限制：15fps≤帧率≤60fps；编码采用H.264或H.265；边长不低于640，不大于2048。
    -   视频内容：视频应为人物正面出镜的近景画面。避免大角度侧脸或人脸过小。
-   音频要求：
    
    -   文件限制：支持wav、mp3、aac，文件≤30MB，2秒＜时长＜120秒。
    -   音频内容：音频中需包含清晰、响亮的人声语音，并去除了环境噪音、背景音乐等声音干扰信息。
-   人物参考图要求：
    
    -   文件限制：支持jpeg、jpg、png、bmp、webp，文件≤10MB。
    -   图片内容：需包含一张清晰的人物正脸，且该人物出现在视频画面中。也可从视频画面中截图用作人物参考图。
-   上传文件链接要求：
    
    -   上传的视频、音频、图像文件支持HTTP链接，不支持本地路径。也可使用平台提供的[临时存储空间](../../../more-about-models/get-temporary-file-url.md)，上传本地文件并创建链接。
    -   如果使用临时存储空间上传文件后获取到的`oss://`前缀URL，在HTTP请求头中必须添加`X-DashScope-OssResourceResolve: enable`参数。未添加该参数会导致报错`No connection adapters were found for 'oss://...'`。详细说明请参见[上传文件获取临时URL](../../../more-about-models/get-temporary-file-url.md)。

<a id="作业提交接口"></a>

<a id="99d4e18b3e9hc"></a>

### 作业提交接口

<a id="code-block"></a>

```http
POST https://dashscope.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis
```

<a id="入参描述"></a>

<a id="45e3c74b3byfh"></a>

#### 入参描述

<table><thead><tr><th><p><strong>字段</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>传参方式</strong></p></th><th><p><strong>必选</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td><p>Content-Type</p></td><td><p>String</p></td><td><p>Header</p></td><td><p>是</p></td><td><p>请求类型：application/json</p></td><td><p>application/json</p></td></tr><tr><td><p>Authorization</p></td><td><p>String</p></td><td><p>Header</p></td><td><p>是</p></td><td><p>API-Key，例如：Bearer d1**2a</p></td><td><p>Bearer d1**2a</p></td></tr><tr><td><p>X-DashScope-Async</p></td><td><p>String</p></td><td><p>Header</p></td><td><p>是</p></td><td><p>设置为<code>enable</code>，表明使用异步方式创建任务</p></td><td><p>enable</p></td></tr><tr><td><p>model</p></td><td><p>String</p></td><td><p>Body</p></td><td><p>是</p></td><td><p>指明需要调用的模型</p></td><td><p>videoretalk</p></td></tr><tr><td><p>input.video_url</p></td><td><p>String</p></td><td><p>Body</p></td><td><p>是</p></td><td><p>用户上传的视频文件 URL。</p><p>URL 需为公网可访问的地址，并支持 HTTP 或 HTTPS 协议。您也可在此<a href="../../../more-about-models/get-temporary-file-url.md">获取临时公网URL</a>。</p><p>视频文件要求：</p><ul><li><p>大小：文件≤300MB</p></li><li><p>格式：mp4、avi、mov</p></li><li><p>时长：2秒＜时长＜120秒</p></li><li><p>帧率：15fps≤帧率≤60fps</p></li><li><p>编码：推荐采用H.264或H.265编码</p></li><li><p>边长：640≤边长≤2048</p></li><li><p>内容：人物正面出镜的近景画面，避免大角度侧脸或人脸过小。如果视频的画面中人脸拍不全、没有人，请参考<a href="videoretalk-api.md#a6986dc8b724w">常见问题</a>进行处理。</p></li></ul></td><td><p>http://aaa/bbb.mp4</p></td></tr><tr><td><p>input.audio_url</p></td><td><p>String</p></td><td><p>Body</p></td><td><p>是</p></td><td><p>用户上传的音频文件 URL。</p><p>URL 需为公网可访问的地址，并支持 HTTP 或 HTTPS 协议。您也可在此<a href="../../../more-about-models/get-temporary-file-url.md">获取临时公网URL</a>。</p><p>音频文件要求：</p><ul><li><p>大小：文件≤30MB</p></li><li><p>格式：wav、mp3、aac</p></li><li><p>时长：2秒＜时长＜120秒，如果视频和音频的时长不一致，请参考<a href="videoretalk-api.md#a6986dc8b724w">常见问题</a>进行处理</p></li><li><p>内容：音频中需包含清晰、响亮的人声语音，并去除了环境噪音、背景音乐等声音干扰信息。</p></li></ul></td><td><p>http://aaa/bbb.wav</p></td></tr><tr><td><p>input.ref_image_url</p></td><td><p>String</p></td><td><p>Body</p></td><td><p>否</p></td><td><p>用户上传的人脸参考图 URL。</p><p>URL 需为公网可访问的地址，并支持 HTTP 或 HTTPS 协议。您也可在此<a href="../../../more-about-models/get-temporary-file-url.md">获取临时公网URL</a>。</p><p>当输入视频中存在多张人脸时，您可以通过该参数指定用于口型匹配的人脸。如果视频中仅有一张人脸，则无需进行指定。</p><p>若不输入人脸参考图，默认将选择视频中第一个有人脸的画面中，人脸占比最大的人物为目标。</p><p>图像文件要求：</p><ul><li><p>内容：需包含一张清晰的人物正脸，且为视频中出现的人物</p></li><li><p>文件大小：文件≤10MB</p></li><li><p>图像大小：长宽比小于等于2，最大边长小于等4096</p></li><li><p>格式：jpeg、jpg、png、bmp、webp</p></li></ul></td><td><p>http://aaa/bbb.jpg</p></td></tr><tr><td><p>parameters.video_extension</p></td><td><p>Boolean</p></td><td><p>Body</p></td><td><p>否</p></td><td><p>当输入的音频时长大于视频时长时，是否扩展视频长度。默认值为<code>false</code>，可设置为<code>true</code>或<code>false</code>。</p><ul><li><p>值为<code>true</code>时，使用原视频画面“倒放-正放”交替模式扩展视频时长，直至与音频相同。</p></li><li><p>值为<code>false</code>时，不扩展画面长度，生成视频时长将与原视频相同，音频将被截断。</p></li></ul></td><td><p>false</p></td></tr><tr><td><p>parameters.query_face_threshold</p></td><td><p>Integer</p></td><td><p>Body</p></td><td><p>否</p></td><td><p>当输入人脸参考图时，可通过该值调整人脸匹配的置信度。</p><p>取值范围为120-200。值越小，人脸参考图的匹配越宽松；值越大，人脸参考图的匹配越严格。默认值为170。</p><p>备注：input.ref_image_url 为空时该参数不生效。</p></td><td><p>170</p></td></tr></tbody></table>

<a id="出参描述"></a>

<a id="1553c7f6daoc3"></a>

#### 出参描述

| 字段 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
| output.task\_id | String | 提交异步任务的作业 ID，实际作业结果需要通过异步任务查询接口获取。 | a8532587-fa8c-4ef8-82be-0c46b17950d1 |
| output.task\_status | String | 提交异步任务后的作业状态。 | “PENDING” |
| request\_id | String | 本次请求的系统唯一码。 | 7574ee8f-38a3-4b1e-9280-11c33ab46e51 |

<a id="请求示例"></a>

<a id="469d8d64cc95l"></a>

#### 请求示例

<a id="code-block-2"></a>

```bash
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis' \
--header 'X-DashScope-Async: enable' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "videoretalk",
    "input": {
        "video_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250717/pvegot/input_video_01.mp4",
        "audio_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250717/aumwir/stella2-%E6%9C%89%E5%A3%B0%E4%B9%A67.wav",
        "ref_image_url": ""
     },
    "parameters": {
        "video_extension": false
    }
  }'
```

<a id="响应示例"></a>

<a id="0d7715817cl3c"></a>

#### 响应示例

<a id="code-block-3"></a>

```json
{
    "output": {
	"task_id": "a8532587-fa8c-4ef8-82be-0c46b17950d1",
        "task_status": "PENDING"
    },
    "request_id": "7574ee8f-38a3-4b1e-9280-11c33ab46e51"
}
```

<a id="作业任务状态查询和结果获取接口"></a>

<a id="c89331030e0y3"></a>

### 作业任务状态查询和结果获取接口

<a id="code-block-4"></a>

```http
GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}
```

<a id="入参描述-2"></a>

<a id="3fe6afeb79bju"></a>

#### 入参描述

| 字段 | 类型 | 传参方式 | 必选 | 描述 | 示例值 |
| --- | --- | --- | --- | --- | --- |
| Authorization | String | Header | 是 | API-Key，例如：Bearer d1\*\*2a。 | Bearer d1\*\*2a |
| task\_id | String | Url Path | 是 | 需要查询作业的task\_id，为作业提交接口返回的值。 | a8532587-fa8c-4ef8-82be-0c46b17950d1 |

<a id="出参描述-2"></a>

<a id="1fe854c50ckzz"></a>

#### 出参描述

<table><thead><tr><th><p><strong>字段</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td><p>output.task_id</p></td><td><p>String</p></td><td><p>查询作业的 task_id。</p></td><td><p>a8532587-fa8c-4ef8-82be-0c46b17950d1</p></td></tr><tr><td><p>output.task_status</p></td><td><p>String</p></td><td><p>被查询作业的作业状态。</p></td><td><p>任务状态：</p><ul><li><p>PENDING：排队中</p></li><li><p>PRE-PROCESSING：前置处理中</p></li><li><p>RUNNING：处理中</p></li><li><p>POST-PROCESSING：后置处理中</p></li><li><p>SUCCEEDED：成功</p></li><li><p>FAILED：失败</p></li><li><p>UNKNOWN：作业不存在或状态未知</p></li></ul></td></tr><tr><td><p>output.video_url</p></td><td><p>String</p></td><td><p>生成的视频，<strong>video_url有效期为作业完成后24小时。</strong></p></td><td><p><a href="https://xxx/1.mp4">https://xxx/1.mp4</a>&quot;</p></td></tr><tr><td><p>usage.video_duration</p></td><td><p>Float</p></td><td><p>本次请求生成视频时长计量，单位：秒。</p></td><td><p>&quot;video_duration&quot;: 10.23</p></td></tr><tr><td><p>usage.video_ratio</p></td><td><p>String</p></td><td><p>本次请求生成视频的画幅类型，该值为standard，默认按原视频比例输出。</p></td><td><p>&quot;video_ratio&quot;: &quot;standard&quot;</p></td></tr><tr><td><p>usage.size</p></td><td><p>String</p></td><td><p>本次请求生成视频的分辨率，和输入视频分辨率一致</p></td><td><p>&quot;size&quot;: &quot;1080*1920&quot;</p></td></tr><tr><td><p>usage.fps</p></td><td><p>Integer</p></td><td><p>本次请求生成视频的帧率，和输入视频帧率一致</p></td><td><p>&quot;fps&quot;: 25</p></td></tr><tr><td><p>request_id</p></td><td><p>String</p></td><td><p>本次请求的系统唯一码。</p></td><td><p>7574ee8f-38a3-4b1e-9280-11c33ab46e51</p></td></tr></tbody></table>

<a id="请求示例-2"></a>

<a id="e0200c87dblj3"></a>

#### 请求示例

<a id="code-block-5"></a>

```bash
curl -X GET 'https://dashscope.aliyuncs.com/api/v1/tasks/<YOUR_TASK_ID>' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

<a id="响应示例-2"></a>

<a id="7bfc2ff742jqm"></a>

#### 响应示例

<a id="code-block-6"></a>

```json
{
    "request_id": "87b9dce5-7f36-4305-a347-xxxxxx",
    "output": {
        "task_id": "3afd65eb-9604-48ea-8a91-xxxxxx",
        "task_status": "SUCCEEDED",
        "submit_time": "2025-09-11 20:15:29.887",
        "scheduled_time": "2025-09-11 20:15:36.741",
        "end_time": "2025-09-11 20:16:40.577",
        "video_url": "http://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/xxx.mp4?Expires=xxx"
    },
    "usage": {
        "video_duration": 7.2,
        "size": "1080*1920",
        "video_ratio": "standard",
        "fps": 25
    }
}
```

<a id="异常响应示例"></a>

<a id="4d01f109585oo"></a>

#### 异常响应示例

<a id="code-block-7"></a>

```json
{
    "request_id": "7574ee8f-38a3-4b1e-9280-11c33ab46e51",
    "output": {
        "task_id": "a8532587-fa8c-4ef8-82be-0c46b17950d1",
        "task_status": "FAILED",
        "code": "xxx",
        "message": "xxxxxx"
    }
}
```

<a id="状态码说明"></a>

<a id="0a1ca76200o0m"></a>

## 状态码说明

大模型服务通用状态码请查阅：[错误码](../../../preparations/error-code.md)

同时本模型还有如下特定错误码：

| HTTP 返回码 | 错误码（code） | 错误信息（message） | 含义说明 |
| --- | --- | --- | --- |
| 400 | InvalidParameter | Field required: xxx | 缺少入参，或格式错误 |
| 400 | InvalidURL.ConnectionRefused | Connection to ${url} refused, please provide avaiable URL | 下载被拒绝，请提供可用的url |
| 400 | InvalidURL.Timeout | Download ${url} timeout, please check network connection. | 下载超时，60s超时 |
| 400 | InvalidFile.Size | Invalid file size. The video/audio/image file size must be less than \*\*MB. | 视频/音频/图像文件必须小于\*\*MB |
| 400 | InvalidFile.Format | Invalid file format，the request file format is one of the following types: MP4, AVI, MOV, MP3, WAV, AAC, JPEG, JPG, PNG, BMP, and WEBP. | 文件格式不符合要求，视频支持mp4、avi、mov；音频支持mp3, wav, aac；图片支持jpg, jpeg, png, bmp, webp |
| 400 | InvalidFile.Resolution | Invalid video resolution. The height or width of video must be 640 ~ 2048. | 视频边长需介于640-2048之间 |
| 400 | InvalidFile.FPS | Invalid video FPS. The video FPS must be 15 ~ 60. | 视频帧率需介于15-60fps之间。 |
| 400 | InvalidFile.Duration | Invalid file duration. The video/audio file duration must be 2s ~ 120s. | 视频/音频时长需介于2-120s之间 |
| 400 | InvalidFile.ImageSize | The size of image is beyond limit. | 图片大小超出限制。<br><br>要求图片长宽比例不大于2，且最长边不大于4096 |
| 400 | InvalidFile.Openerror | Invalid file, cannot open file as video/audio/image. | 视频/音频/图像文件无法打开 |
| 400 | InvalidFile.Content | The input image has no human body or multi human bodies. Please upload other image with single person. | 输入图片中没有人或有多人 |
| 400 | InvalidFile.FaceNotMatch | There are no matched face in the video with the provided reference image. | 参考图与视频人脸匹配失败 |

<a id="常见问题"></a>

<a id="a6986dc8b724w"></a>

## 常见问题

1.  输入语音和视频长度不一致，会如何处理？
    
    默认将按音频、视频两者中时长较短的来截断。
    
    当输入的音频时长大于视频时长时，并希望按音频长度来生成时，可将入参的视频扩展（parameters.video\_extension）值设为true，算法将使用原视频画面“倒放-正放”交替模式扩展视频时长，直至与音频相同。
    
2.  输入音频中有静音的情况，会如何处理？
    
    音频静音的时段，预期视频中人物也会闭嘴。
    
3.  输入视频的画面中有无人/脸拍不全的情况，会如何处理？
    
    若音频中有人声，但画面无人或未出现人物嘴型，则保留原视频画面，音频正常播放。
    
4.  输入视频的画面中有多人的情况，会如何处理？
    
    仅支持替换一个人物。算法会按照输入人脸参考图（input.ref\_image\_url），识别指定人脸。若未输入人脸参考图，则默认选择第一个有人脸画面中，占比最大的人脸。
