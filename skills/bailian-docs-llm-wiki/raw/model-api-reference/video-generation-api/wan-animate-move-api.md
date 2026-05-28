# 万相-图生动作API参考

基于人物图片和参考视频，生成人物动作视频。

-   **功能简述：**将参考视频中的动作和表情迁移到人物图片，生成动态视频。
    
-   **适用场景：**舞蹈复刻、高难度肢体动作复刻、影视表演复刻，可作为动作捕捉的低成本替代方案。
    

## **模型效果**

wan2.2-animate-move 提供两种服务模式：标准模式`wan-std`和专业模式`wan-pro`，两种模式在画质效果和计费上有所不同，详见[万相-图生动作](https://help.aliyun.com/zh/model-studio/model-pricing#1f708fcd62rdc)。

**人物图片**

**参考视频**

**输出视频（标准模式**`**wan-std**`**）**

**输出视频（专业模式**`**wan-pro**`**）**

![move\_input\_image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9815528571/p1008736.jpeg)

## **前提条件**

您需要已[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

**重要**

北京和新加坡地域拥有独立的 **API Key** 与**请求地址**，不可混用，跨地域调用将导致鉴权失败或服务报错。

## HTTP调用

视频生成任务耗时较长，API 采用异步调用，分为两个步骤：创建任务，然后轮询获取结果。

### 步骤1：创建任务获取任务ID

**北京地域**：`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis`

**新加坡地域**：`POST https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis`

**说明**

-   创建成功后，使用接口返回的 `task_id` 查询结果，task\_id 有效期为 24 小时。**请勿重复创建任务**，轮询获取即可。
    
-   新手指引请参见[Postman](https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api)。
    

#### 请求参数

## 图生动作

以下为北京地域 base\_url，若使用新加坡地域的模型，需将 base\_url 替换为：`https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis`

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis' \
    --header 'X-DashScope-Async: enable' \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
    --header 'Content-Type: application/json' \
    --data '{
        "model": "wan2.2-animate-move",
        "input": {
            "image_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250919/adsyrp/move_input_image.jpeg",
            "video_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250919/kaakcn/move_input_video.mp4",
            "watermark": true
        },
        "parameters": {
            "mode": "wan-std"
        }
      }'
```

##### 请求头（Headers）

**Content-Type** `_string_` **（必选）**

请求内容类型。此参数必须设置为`application/json`。

**Authorization** `_string_`**（必选）**

请求身份认证。接口使用阿里云百炼API-Key进行身份认证。示例值：Bearer sk-xxxx。

**X-DashScope-Async** `_string_` **（必选）**

异步处理配置参数。HTTP请求只支持异步，**必须设置为**`**enable**`。

**重要**

缺少此请求头将报错：“current user api does not support synchronous calls”。

##### 请求体（Request Body）

**model** `_string_` **（必选）**

模型名称，固定填写`wan2.2-animate-move`。

**input** `_object_` **（必选）**

输入参数对象，包含以下字段：

**属性**

**image\_url** `_string_` **（必选）**

人物图片的公网可访问 HTTP/HTTPS 链接。URL 中若含中文等非 ASCII 字符，需先进行URL编码。

本地文件可通过[上传文件获取临时URL](https://help.aliyun.com/zh/model-studio/get-temporary-file-url)。

-   **格式**：JPG、JPEG、PNG、BMP、WEBP。
    
-   **尺寸**：宽高均在`[200, 4096]`像素范围内，宽高比在 1:3 至 3:1 之间。
    
-   **文件大小**：不超过 5 MB。
    
-   **内容**：画面中仅有一人，正对镜头，人脸完整无遮挡，人物在画面中占比适中。
    
-   **示例值**：`https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250919/adsyrp/move_input_image.jpeg`
    

**video\_url** `_string_` **（必选）**

参考视频的公网可访问 HTTP/HTTPS 链接。URL 中若含中文等非 ASCII 字符，需先进行URL编码。

本地文件可通过[上传文件获取临时URL](https://help.aliyun.com/zh/model-studio/get-temporary-file-url)。

**建议：**使用高分辨率、高帧率的参考视频，可有效提升生成视频的画质效果。

-   **格式**：MP4、AVI、MOV。
    
-   **时长**：2～30 秒。
    
-   **尺寸**：宽高均在`[200, 2048]`像素范围内，宽高比在 1:3 至 3:1 之间。
    
-   **文件大小**：不超过 200 MB。
    
-   **内容**：画面中仅有一人，正对镜头，人脸完整无遮挡，人物在画面中占比适中。
    
-   **示例值**：`https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250919/kaakcn/move_input_video.mp4`
    

**watermark** `_bool_` （可选）

是否在视频右下角添加"千问AI生成"水印。

-   `false`（默认值）：不添加水印。
    
-   `true`：添加水印。
    

**parameters** `_object_` **（必选）**

**属性**

**check\_image** `_bool_` （可选）

是否对输入图片进行检测。

-   `true`：**默认值**，检测传入的图片。
    
-   `false`：跳过图片检测，直接处理。
    

**mode** `_string_` **（必选）**

服务模式，支持以下两种：

-   `wan-std`：标准模式，生成速度快、性价比高，适合快速预览和基础动画场景。
    
-   `wan-pro`：专业模式，动画流畅度更高、效果更佳，处理时间和费用相应增加。
    

详情请参见[模型效果](#55a79354d2s4j)和[计费与限流](#ce68f54f7bbqe)。

#### 响应参数

### 成功响应

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

### 异常响应

创建任务失败，请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。

```
{
    "code": "InvalidApiKey",
    "message": "No API-key provided.",
    "request_id": "7438d53d-6eb8-4596-8835-xxxxxx"
}
```

**output** `_object_`

任务输出信息。

**属性**

**task\_id** `_string_`

任务ID。查询有效期24小时。

**task\_status** `_string_`

任务状态。

**枚举值**

-   PENDING：任务排队中
    
-   RUNNING：任务处理中
    
-   SUCCEEDED：任务执行成功
    
-   FAILED：任务执行失败
    
-   CANCELED：任务已取消
    
-   UNKNOWN：任务不存在或状态未知
    

**request\_id** `_string_`

请求唯一标识。可用于请求明细溯源和问题排查。

**message** `_string_`

请求失败的详细信息。请求成功时不会返回此参数，详情请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。

**code** `_string_`

请求失败的错误码。请求成功时不会返回此参数，详情请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。

### 步骤2：根据任务ID查询结果

#### **北京**

`GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`

#### 新加坡

`GET https://dashscope-intl.aliyuncs.com/api/v1/tasks/{task_id}`

**说明**

-   **轮询建议**：视频生成过程约需数分钟，建议采用**轮询**机制，并设置合理的查询间隔（如 15 秒）来获取结果。
    
-   **任务状态流转**：PENDING（排队中）→ RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。
    
-   **结果链接**：任务成功后返回视频链接，有效期为 **24 小时**。建议在获取链接后立即下载并转存至永久存储（如[阿里云 OSS](https://help.aliyun.com/zh/oss/user-guide/what-is-oss)）。
    
-   **task\_id 有效期**：**24小时**，超时后将无法查询结果，接口将返回任务状态为`UNKNOWN`。
    
-   **RPS 限制**：查询接口默认RPS为20。如需更高频查询或事件通知，建议[配置异步任务回调](https://help.aliyun.com/zh/model-studio/async-task-api)。
    
-   **更多操作**：如需批量查询、取消任务等操作，请参见[管理异步任务](https://help.aliyun.com/zh/model-studio/manage-asynchronous-tasks#f26499d72adsl)。
    

#### 请求参数

## 查询任务结果

将`0385dc79-5ff8-4d82-bcb6-xxxxxx`替换为实际的 task\_id。

> 以下为北京地域 base\_url，若使用新加坡地域的模型，需将 base\_url 替换为：`https://dashscope-intl.aliyuncs.com/api/v1/tasks/0385dc79-5ff8-4d82-bcb6-xxxxxx`

```
curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/0385dc79-5ff8-4d82-bcb6-xxxxxx \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

##### **请求头（Headers）**

**Authorization** `_string_`**（必选）**

请求身份认证。接口使用阿里云百炼API-Key进行身份认证。示例值：Bearer sk-xxxx。

##### **URL路径参数（Path parameters）**

**task\_id** `_string_`**（必选）**

任务ID。

#### **响应参数**

## 任务执行成功

视频URL仅保留24小时，超时后会被自动清除，请及时保存生成的视频。

```
{
    "request_id": "a67f8716-18ef-447c-a286-xxxxxx",
    "output": {
        "task_id": "0385dc79-5ff8-4d82-bcb6-xxxxxx",
        "task_status": "SUCCEEDED",
        "submit_time": "2025-09-18 15:32:00.105",
        "scheduled_time": "2025-09-18 15:32:15.066",
        "end_time": "2025-09-18 15:34:41.898",
        "results": {
            "video_url": "http://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxxxx.mp4?Expires=xxxxxx"
        }
    },
    "usage": {
        "video_duration": 5.2,
        "video_ratio": "standard"
    }
}
```

## 任务执行失败

若任务执行失败，task\_status将置为 FAILED，并提供错误码和信息。请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。

```
{
    "request_id": "daad9007-6acd-9fb3-a6bc-xxxxxx",
    "output": {
        "task_id": "fe8aa114-d9f1-4f76-b598-xxxxxx",
        "task_status": "FAILED",
        "code": "InternalError",
        "message": "xxxxxx"
    }
}
```

**output** `_object_`

任务输出信息。

**属性**

**task\_id** `_string_`

任务ID。查询有效期24小时。

**task\_status** `_string_`

任务状态。

**枚举值**

-   PENDING：任务排队中
    
-   RUNNING：任务处理中
    
-   SUCCEEDED：任务执行成功
    
-   FAILED：任务执行失败
    
-   CANCELED：任务已取消
    
-   UNKNOWN：任务不存在或状态未知
    

**submit\_time** `_string_`

任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。

**scheduled\_time** `_string_`

任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。

**end\_time** `_string_`

任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。

**results** `_object_`

**属性**

**video\_url** `_string_`

视频URL。仅在 task\_status 为 SUCCEEDED 时返回。

链接有效期24小时，可通过此URL下载视频。视频格式为MP4（H.264 编码）。

**code** `_string_`

请求失败的错误码。请求成功时不会返回此参数，详情请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。

**message** `_string_`

请求失败的详细信息。请求成功时不会返回此参数，详情请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。

**usage** `_object_`

用量统计信息，仅统计成功的请求。

**属性**

**video\_duration** `_float_`

本次请求生成视频的时长，单位：秒。

**video\_ratio** `_string_`

本次请求所用的服务模式标识，枚举值：`standard`、`pro`。

标准模式`wan-std`对应`standard`，专业模式`wan-pro`对应`pro`。

**request\_id** `_string_`

请求唯一标识。可用于请求明细溯源和问题排查。

## **使用限制**

**数据时效**：task\_id 和视频URL均只保留 24 小时，请及时[下载视频到本地](#866ccf3fa3y1p)，过期后将无法查询或访问。

**内容审核**：输入和输出内容均会经过内容安全审核，包含违规内容的请求将返回 `IPInfringementSuspect` 或 `DataInspectionFailed` 错误，详见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。

## **计费与限流**

-   免费额度和计费单价，请参见[万相-图生动作](https://help.aliyun.com/zh/model-studio/model-pricing#1f708fcd62rdc)。
    
-   模型限流，请参见[万相系列](https://help.aliyun.com/zh/model-studio/rate-limit#a729d7b6bar7y)。
    
-   计费说明：
    
    -   输入不计费，输出按成功生成的视频秒数计费。
        
    -   调用失败不产生任何费用，也不消耗[新人免费额度](https://help.aliyun.com/zh/model-studio/new-free-quota)。
        

## **错误码**

调用失败时，请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)排查解决。

## **常见问题**

#### **Q: 如何优化生成视频的效果?**

可参考以下建议：

1.  确保输入图片与参考视频中的人物画幅占比相近。
    
2.  保持图片和视频中人物的身材比例一致。
    
3.  使用高清素材，避免模糊图片和低帧率视频，以确保细节识别准确。
    

#### **Q: 如何将临时的视频链接转为永久链接？**

无法直接转换该链接。正确做法是：后端获取到视频URL后，通过代码下载视频文件，再上传至永久对象存储（如阿里云 OSS），生成新的永久访问链接。

**示例代码：下载视频到本地**

```
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

#### **Q: 返回的视频链接可以在浏览器中直接播放吗？**

不建议。视频链接 24 小时后失效，最佳实践是后端下载转存后，通过永久链接提供视频播放。

#### **Q：如何获取视频存储的访问域名白名单？**

A： 模型生成的视频存储于阿里云OSS，API将返回一个临时的公网URL。**若需要对该下载地址进行防火墙白名单配置**，请注意：由于底层存储会根据业务情况进行动态变更，为避免过期信息影响访问，文档不提供固定的OSS域名白名单。如有安全管控需求，请联系客户经理获取最新OSS域名列表。
