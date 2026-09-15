# Emoji 视频生成API参考

表情包emoji-v1模型可基于 人物肖像图片和预设模板ID ，生成人脸表情包视频。

**重要**本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。

## 模型概览

**模型名称**

**模型简介**

emoji-v1

输入通过检测的人物肖像图片、对应的人脸区域、动态表情区域坐标以及表情包模板ID，生成人脸表情包视频。

## 前提条件

1.  您需要已[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。请将示例代码中的 `DASHSCOPE_API_HOST` 替换为获取的 API Host。
2.  输入图像已通过[Emoji 图像检测](raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start/emoji-detect-api.md)，并获得对应人脸区域和动态表情区域的坐标作为入参。

## HTTP调用

由于视频生成任务耗时较长（通常为1-5分钟），API采用异步调用。整个流程包含 **“创建任务 -> 轮询获取”** 两个核心步骤，具体如下：

> 模型耗时受限于排队任务数和服务执行情况，请在获取结果时耐心等待。

### 步骤1：创建任务获取任务ID

`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis`

#### 请求参数

##### 请求头（Headers）

**Content-Type**`string`**（必选）**

请求内容类型。此参数必须设置为`application/json`。

**Authorization**`string`**（必选）**

请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。

**X-DashScope-Async**`string`**（必选）**

异步处理配置参数。HTTP请求只支持异步，**必须设置为**`enable`。

**重要**缺少此请求头将报错：“current user api does not support synchronous calls”。

##### 请求体（Request Body）

**model** `string` **（必选）**

模型名称。固定为`emoji-v1`。

**input** `object` **（必选）**

输入的基本信息，如人脸图像、人脸区域、表情包区域等。

属性

**image\_url** `string` **（必选）**

人脸正面肖像图像的公网 URL。支持 HTTP 或 HTTPS 协议。本地文件可通过[上传文件获取临时URL](raw/model-api-reference/more-about-models/get-temporary-file-url.md)。

图像限制：

-   图像格式：JPEG、JPG、PNG、BMP、WEBP。
-   图像分辨率：图像的宽度和高度均在\[400, 7000\]像素之间。
-   文件大小：不超过10MB。
-   此图像必须通过[Emoji 图像检测](raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start/emoji-detect-api.md)。

示例值：[](https://help-static-aliyun-doc.aliyuncs.com/xxx.png)[https://help-static-aliyun-doc.aliyuncs.com/xxx.png](https://help-static-aliyun-doc.aliyuncs.com/xxx.png)。

**face\_bbox** `array of integer` **（必选）**

图片中人脸区域坐标，格式为 \[x1, y1, x2, y2\]，单位为像素，对应左上和右下两个点的坐标。

此参数需填入[Emoji 图像检测](raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start/emoji-detect-api.md)接口响应中的`output.bbox_face` 字段的值。

示例值：\[212,194,460,441\]。

**ext\_bbox** `array of integer` **（必选）**

动态表情区域坐标，该区域的宽高比约为1:1，格式为 \[x1, y1, x2, y2\]，单位为像素，对应左上和右下两个点的坐标。

此参数需填入[Emoji 图像检测](raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start/emoji-detect-api.md)接口响应中的`output.ext_bbox_face`字段的值。

示例值：\[63,30,609,575\]。

> 说明：动态表情区域指的是模型进行视频生成时实际关注的正方形图像区域，它通常比人脸区域稍大，以包含部分背景和肩膀，确保动画效果自然。

**driven\_id** `string` **（必选）**

预设模板ID，可选值参见[表情包模板ID列表](https://help.aliyun.com/zh/model-studio/emoji-api#552aacbdadtaq)。

示例值：mengwa\_kaixin。

#### 表情包视频生成

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'X-DashScope-Async: enable' \
--header 'Content-Type: application/json' \
--data '{
    "model": "emoji-v1",
    "input": {
        "image_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250912/uopnly/emoji-%E5%9B%BE%E5%83%8F%E6%A3%80%E6%B5%8B.png",
        "driven_id": "mengwa_kaixin",
        "face_bbox": [212,194,460,441],
        "ext_bbox": [63,30,609,575]
    }
}'
```

#### 响应参数

**output** `object`

任务输出信息。

属性

**task\_id** `string`

任务ID。查询有效期24小时。

**task\_status** `string`

任务状态。

枚举值

-   PENDING：任务排队中
-   RUNNING：任务处理中
-   SUCCEEDED：任务执行成功
-   FAILED：任务执行失败
-   CANCELED：任务已取消
-   UNKNOWN：任务不存在或状态未知

**request\_id**`string`

请求唯一标识。可用于请求明细溯源和问题排查。

**code**`string`

请求失败的错误码。请求成功时不会返回此参数，详情请参见[错误码](raw/model-api-reference/preparations/error-code.md)。

**message**`string`

请求失败的详细信息。请求成功时不会返回此参数，详情请参见[错误码](raw/model-api-reference/preparations/error-code.md)。

#### 成功响应

请保存 task\_id，用于查询任务状态与结果。

```
{
    "output": {
        "task_status": "PENDING",
        "task_id": "0385dc79-5ff8-4d82-bcb6-xxxxxx"
    },
    "request_id": "4909100c-7b5a-9f92-bfe5-xxxxxx"
}
```

#### 异常响应

创建任务失败，请参见[错误码](raw/model-api-reference/preparations/error-code.md)进行解决。

```
{
    "code": "InvalidApiKey",
    "message": "No API-key provided.",
    "request_id": "7438d53d-6eb8-4596-8835-xxxxxx"
}
```

### 步骤2：根据任务ID查询结果

`GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`

**说明**

-   **轮询建议**：视频生成过程约需数分钟，建议采用**轮询**机制，并设置合理的查询间隔（如 15 秒）来获取结果。
-   **任务状态流转**：PENDING（排队中）→ RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。
-   **结果链接**：任务成功后返回视频链接，有效期为 **24 小时**。建议在获取链接后立即下载并转存至永久存储（如[阿里云 OSS](https://help.aliyun.com/zh/oss/user-guide/what-is-oss)）。
-   **task\_id 有效期**：**24小时**，超时后将无法查询结果，接口将返回任务状态为`UNKNOWN`。
-   **RPS 限制**：查询接口默认RPS为20。如需更高频查询或事件通知，建议[配置异步任务回调](raw/model-api-reference/more-about-models/async-task-api.md)。
-   **更多操作**：如需批量查询、取消任务等操作，请参见[管理异步任务](raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。

#### 请求参数

##### 请求头（Headers）

**Authorization**`string`**（必选）**

请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。

##### URL路径参数（Path parameters）

**task\_id** `string`**（必选）**

任务ID。

#### 查询任务结果

请将`86ecf553-d340-4e21-xxxxxxxxx`替换为真实的task\_id。

> 若使用新加坡地域的模型，需将base\_url替换为https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/tasks/86ecf553-d340-4e21-xxxxxxxxx，其中{WorkspaceId}需替换为真实的业务空间ID。

```
curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/86ecf553-d340-4e21-xxxxxxxxx \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

#### 响应参数

**output**`object`

任务输出信息。

属性

**task\_id** `string`

任务ID。查询有效期24小时。

**task\_status** `string`

任务状态。

枚举值

-   PENDING：任务排队中
-   RUNNING：任务处理中
-   SUCCEEDED：任务执行成功
-   FAILED：任务执行失败
-   CANCELED：任务已取消
-   UNKNOWN：任务不存在或状态未知

**轮询过程中的状态流转：**

-   PENDING（排队中） → RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。
-   初次查询状态通常为 PENDING（排队中）或 RUNNING（处理中）。
-   当状态变为 SUCCEEDED 时，响应中将包含生成的视频URL。
-   若状态为 FAILED，请检查错误信息并重试。
-   若状态为 CANCELED，表示任务已取消，如需继续请重新提交任务。
-   若状态为 UNKNOWN，表示任务不存在或状态未知，可能在 task\_id 不存在或超过 24 小时有效期后出现。

**submit\_time** `string`

任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。

**scheduled\_time** `string`

任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。

**end\_time** `string`

任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。

**video\_url**`string`

视频URL。仅在 task\_status 为 SUCCEEDED 时返回。

链接有效期24小时，可通过此URL下载视频。视频格式为MP4（H.264 编码）。

**code**`string`

请求失败的错误码。请求成功时不会返回此参数，详情请参见[错误码](raw/model-api-reference/preparations/error-code.md)。

**message**`string`

请求失败的详细信息。请求成功时不会返回此参数，详情请参见[错误码](raw/model-api-reference/preparations/error-code.md)。

**usage** `object`

输出信息统计，只对成功的结果计数。

属性

**video\_duration** `integer`

生成视频的时长，单位为秒。

> 计费公式：费用 = 视频秒数 × 单价。

**video\_ratio** `string`

生成视频的画幅，固定为standard，表示生成1:1画幅的视频。

**request\_id**`string`

请求唯一标识。可用于请求明细溯源和问题排查。

#### 任务执行成功

视频URL仅保留24小时，超时后会被自动清除，请及时保存生成的视频。

```
{
    "request_id": "ad225054-6c94-47e5-9356-xxxxxxx",
    "output": {
        "task_id": "b56f509a-3ea9-4cfe-848d-xxxxxxx",
        "task_status": "SUCCEEDED",
        "submit_time": "2025-10-14 11:28:04.372",
        "scheduled_time": "2025-10-14 11:28:04.400",
        "end_time": "2025-10-14 11:29:03.924",
        "video_url": "http://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/xx.mp4?Expires=xxx"
    },
    "usage": {
        "video_duration": 2,
        "video_ratio": "standard"
    }
}
```

#### 任务执行失败

若任务执行失败，task\_status将置为 FAILED，并提供错误码和信息。请参见[错误码](raw/model-api-reference/preparations/error-code.md)进行解决。

```
{
    "request_id": "e5d70b02-ebd3-98ce-9fe8-759d7d7b107d",
    "output": {
        "task_id": "86ecf553-d340-4e21-af6e-a0c6a421c010",
        "task_status": "FAILED",
        "code": "InvalidParameter",
        "message": "The size is not match xxxxxx"
    }
}
```

#### 任务查询过期

task\_id查询有效期为 24 小时，超时后将无法查询，返回以下报错信息。

```
{
    "request_id": "a4de7c32-7057-9f82-8581-xxxxxx",
    "output": {
        "task_id": "502a00b1-19d9-4839-a82f-xxxxxx",
        "task_status": "UNKNOWN"
    }
}
```

## 计费与限流

-   模型免费额度和计费单价请参见[模型价格](raw/model-user-guide/get-started-with-models/models.md)。
-   模型限流请参见[限流](raw/model-user-guide/get-started-with-models/rate-limit.md)。

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](raw/model-api-reference/preparations/error-code.md)进行解决。

## 附录：表情包模板ID列表

参数设置示例：{ "input": { "driven\_id": "mengwa\_kaixin" } }。

**说明**

-   以下生成效果，由集成了“表情包Emoji”的通义APP生成。
-   表情包Emoji模型生成的内容为人物视频，不包含贴纸和文字。

**模板 ID (driven\_id)**

**效果示意**

**模板 ID (driven\_id)**

**效果示意**

mengwa\_kaixin

![1\_mengwa\_kaixin](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3667357371/p906418.gif)

dagong\_zhuakuang

![10\_dagong\_zhuakuang](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4667357371/p906428.gif)

mengwa\_dengyan

![7\_mengwa\_dengyan](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3667357371/p906425.gif)

dagong\_wunai

![15\_dagong\_wunai](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4667357371/p906434.gif)

mengwa\_gandong

![16\_mengwan\_gandong](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3667357371/p906435.gif)

dagong\_weixiao

![17\_dagong\_weixiao](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3667357371/p906438.gif)

mengwa\_renzhen\_1

![18\_mengwa\_renzhen\_1](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4667357371/p906439.gif)

dagong\_ganji

![20\_dagong\_ganji](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4667357371/p906441.gif)

mengwa\_jidong

![8\_mengwa\_jidong](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4667357371/p906426.gif)

jingdian\_tiaopi

![4\_jingdian\_tiaopi](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3667357371/p906422.gif)

mengwa\_kun\_1

![11\_mengwa\_kun\_1](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3667357371/p906429.gif)

jingdian\_deyi\_1

![5\_jingdian\_deyi\_1](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4667357371/p906423.gif)

mengwa\_jiaoxie

![19\_mengwa\_renzhen\_1](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3667357371/p906440.gif)

jingdian\_qidai

![6\_jingdian\_qidai](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4667357371/p906424.gif)

dagong\_kaixin

![2\_dagong\_kaixin](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4667357371/p906419.gif)

jingdian\_landuo\_1

![12\_jingdian\_landuo\_1](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3667357371/p906431.gif)

dagong\_yangwang

![3\_dagong\_yangwang](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4667357371/p906421.gif)

jingdian\_xianqi

![13\_jingdian\_xianqi](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4667357371/p906432.gif)

dagong\_kunhuo

![9\_dagong\_kunhuo](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3667357371/p906427.gif)

jingdian\_lei

![14\_jingdian\_lei](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3667357371/p906433.gif)
