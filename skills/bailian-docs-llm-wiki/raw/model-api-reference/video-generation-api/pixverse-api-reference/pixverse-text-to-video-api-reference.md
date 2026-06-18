# 爱诗-文生视频API参考

爱诗-文生视频模型基于**文本提示词**，生成一段流畅的视频。

**重要**

本文档仅适用于“中国内地（北京）”地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)。

## **服务开通**

1.  前往[阿里云百炼控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/model-market/all)，搜索 **PixVerse**，找到 PixVerse 模型卡片，单击**立即开通**；
    
2.  在弹窗内确认开通及授权。
    

## 适用范围

为确保调用成功，请务必保证**模型、Endpoint URL 和 API Key 均属于同一地域**。跨地域调用将会失败。

-   [**选择模型**](https://help.aliyun.com/zh/model-studio/use-video-generation#3ad2d09509ldb)：确认模型所属的地域。
    
-   **选择 URL**：选择对应的地域 Endpoint URL，支持HTTP URL或 DashScope SDK URL。
    
-   **配置 API Key**：选择地域并[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
    
-   **安装 SDK**：如需通过SDK进行调用，请[安装DashScope SDK](https://help.aliyun.com/zh/model-studio/install-sdk)。
    

## HTTP调用

由于文生视频任务耗时较长（通常为1-5分钟），API采用异步调用。整个流程包含 **"创建任务 -> 轮询获取"** 两个核心步骤，具体如下：

### **步骤1：创建任务获取任务ID**

**北京地域**：`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`

**说明**

-   创建成功后，使用接口返回的 `task_id` 查询结果，task\_id 有效期为 24 小时。**请勿重复创建任务**，轮询获取即可。
    
-   新手指引请参见[Postman](https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api)。
    

#### 请求参数

## 文生视频

支持模型：pixverse/pixverse-c1-t2v、pixverse/pixverse-v6-t2v、pixverse/pixverse-v5.6-t2v。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "pixverse/pixverse-c1-t2v",
    "input": {
        "prompt": "下着雨，赛博城市里，一只浣熊在栏杆上行走。突然他眼睛发出蓝光，变身成一架高科技无人机，快速飞离画面。"
    },
    "parameters": {
        "size": "1280*720",
        "duration": 5,
        "watermark": true
    }
}'
```

## 文生视频（多镜头）

## pixverse-c1

支持模型：pixverse/pixverse-c1-t2v。

在`prompt`中描述多镜头场景即可，不支持设置 `shot_type`参数。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "pixverse/pixverse-c1-t2v",
    "input": {
        "prompt": "镜头1：模特面向镜头平稳向前漫步；镜头2： 快速切换至中景，展示腰线裁剪与蓝白格纹棉质面料的清爽质感；镜头3： 远景捕捉微风吹拂裙摆的自然动态，画面干净明亮。"
    },
    "parameters": {
        "size": "1280*720",
        "duration": 5,
        "audio": true,
        "watermark": true
    }
}'
```

## pixverse-v6

支持模型：pixverse/pixverse-v6-t2v。

在`prompt`中描述多镜头场景，并设置 `shot_type` 为`multi`， 即可生成有声多镜头视频。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "pixverse/pixverse-v6-t2v",
    "input": {
        "prompt": "镜头1：模特面向镜头平稳向前漫步；镜头2： 快速切换至中景，展示腰线裁剪与蓝白格纹棉质面料的清爽质感；镜头3： 远景捕捉微风吹拂裙摆的自然动态，画面干净明亮。"
    },
    "parameters": {
        "size": "1280*720",
        "duration": 5,
        "audio": true,
        "shot_type": "multi",
        "watermark": true
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

模型名称。模型输出规格请参见[模型列表](https://help.aliyun.com/zh/model-studio/use-video-generation#3ad2d09509ldb)。

可选值：

-   pixverse/pixverse-c1-t2v
    
-   pixverse/pixverse-v6-t2v
    
-   pixverse/pixverse-v5.6-t2v
    

**模型选型**

-   针对打斗、法术特效及高速运动等动态场景，推荐选用 **c1**。
    
-   通用场景推荐使用**v6**，**v5.6**建议直接升级至**v6**。
    

**input** `_object_` **（必选）**

输入的基本信息，如提示词等。

**属性**

**prompt** `_string_` **（必选）**

文本提示词。用来描述生成视频中期望包含的元素和视觉特点。

支持中英文，每个汉字/字母占一个字符，字符编码为UTF-8，超过部分会自动截断。

-   pixverse/pixverse-c1-t2v：不超过5000个字符。
    
-   pixverse/pixverse-v6-t2v：不超过5000个字符。
    
-   pixverse/pixverse-v5.6-t2v：不超过2048个字符。
    

**parameters** `_object_` **（必选）**

视频生成参数。如设置视频分辨率、时长、是否生成音频等。

**属性**

**size** `_string_` **（必选）**

生成视频的分辨率，格式为`**宽*高**`的像素值。

**重要**

-   size直接影响费用，请在调用前确认[模型价格](https://help.aliyun.com/zh/model-studio/model-pricing#pxt001a0sec01)。
    
-   使用pixverse/pixverse-v5.6-t2v模型，若设置size为1808\*1808，且duration为8时，实际输出的视频分辨率为1440\*1440。
    

不同分辨率档位和宽高比对应的可选值见下方表格。

pixverse/pixverse-c1-t2v、pixverse/pixverse-v6-t2v模型

分辨率档位

宽高比

size取值（宽\*高）

360P

16:9

640\*360

4:3

640\*480

1:1

640\*640

3:4

480\*640

9:16

360\*640

3:2

640\*432

2:3

432\*640

21:9

640\*288

540P

16:9

1024\*576

4:3

1024\*768

1:1

1024\*1024

3:4

768\*1024

9:16

576\*1024

3:2

1024\*688

2:3

688\*1024

21:9

1024\*448

720P

16:9

1280\*720

4:3

1108\*832

1:1

960\*960

3:4

832\*1108

9:16

720\*1280

3:2

1200\*800

2:3

800\*1200

21:9

1280\*560

1080P

16:9

1920\*1080

4:3

1664\*1248

1:1

1440\*1440

3:4

1248\*1664

9:16

1080\*1920

3:2

1776\*1184

2:3

1184\*1776

21:9

1920\*832

pixverse/pixverse-v5.6-t2v模型

分辨率档位

宽高比

size取值（宽\*高）

360P

16:9

640\*360

4:3

640\*480

1:1

640\*640

3:4

480\*640

9:16

360\*640

540P

16:9

1024\*576

4:3

1024\*768

1:1

1024\*1024

3:4

768\*1024

9:16

576\*1024

720P

16:9

1280\*720

4:3

1280\*960

1:1

1280\*1280

3:4

960\*1280

9:16

720\*1280

1080P

16:9

1920\*1080

4:3

1920\*1440

1:1

1808\*1808

3:4

1440\*1920

9:16

1080\*1920

**duration** `_integer_` **（必选）**

**重要**

duration直接影响费用，按秒计费，请在调用前确认[模型价格](https://help.aliyun.com/zh/model-studio/model-pricing#pxt001a0sec01)。

生成视频的时长，单位为秒。

-   pixverse/pixverse-c1-t2v：取值范围为\[1, 15\]之间的整数。
    
-   pixverse/pixverse-v6-t2v：取值范围为\[1, 15\]之间的整数。
    
-   pixverse/pixverse-v5.6-t2v：
    
    -   当 size 为 360P / 540P / 720P 对应的所有分辨率时：取值为5、8、10。
        
    -   当size为1080P对应的所有分辨率时：取值为5、8。
        

**audio** `_boolean_` （可选）

**重要**

audio直接影响费用，请在调用前确认[模型价格](https://help.aliyun.com/zh/model-studio/model-pricing#pxt001a0sec01)。

是否生成有声视频。开启后模型将根据视频内容自动生成匹配的背景音乐或音效。

-   `false`：默认值，输出无声视频。
    
-   `true`：输出有声视频。
    

**watermark** `_boolean_` （可选）

是否添加水印标识，水印位于视频右下角，文案固定为“AI生成”。

-   `false`：默认值，不添加水印。
    
-   `true`：添加水印。
    

**shot\_type** `_string_` （可选）

**支持模型**：pixverse/pixverse-v6-t2v。

指定生成视频的镜头类型，控制视频是由一个连续镜头还是多镜头组成。

-   `single`：默认值，生成单镜头视频。
    
-   `multi`：多镜头，系统会进行智能分镜。
    

使用建议：prompt 参数优先级高于 shot\_type 。为获得最佳效果，建议此参数设置与 prompt 描述保持一致。

-   若想稳定输出单镜头：设置 `shot_type="single"` 并在 prompt 中描述单镜头场景。
    
-   若想稳定输出多镜头：设置 `shot_type="multi"` 并在 prompt 中描述多镜头场景。
    

**seed** `_integer_` （可选）

随机数种子，取值范围为`[0, 2147483647]`。

未指定时，系统自动生成随机种子。若需提升生成结果的可复现性，建议固定seed值。

请注意，由于模型生成具有概率性，即使使用相同 seed，也不能保证每次生成结果完全一致。

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

**code** `_string_`

请求失败的错误码。请求成功时不会返回此参数，详情请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。

**message** `_string_`

请求失败的详细信息。请求成功时不会返回此参数，详情请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。

### **步骤2：根据任务ID查询结果**

**北京地域**：`GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`

**说明**

-   **轮询建议**：视频生成过程约需数分钟，建议采用**轮询**机制，并设置合理的查询间隔（如 15 秒）来获取结果。
    
-   **任务状态流转**：PENDING（排队中）→ RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。
    
-   **task\_id 有效期**：**24小时**，超时后将无法查询结果，接口将返回任务状态为`UNKNOWN`。
    
-   **RPS 限制**：查询接口默认RPS为20。如需更高频查询或事件通知，建议[配置异步任务回调](https://help.aliyun.com/zh/model-studio/async-task-api)。
    
-   **更多操作**：如需批量查询、取消任务等操作，请参见[管理异步任务](https://help.aliyun.com/zh/model-studio/manage-asynchronous-tasks#f26499d72adsl)。
    

#### 请求参数

## 查询任务结果

将`{task_id}`完整替换为上一步接口返回的`task_id`的值。`task_id`查询有效期为24小时。

```
curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id} \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

##### **请求头（Headers）**

**Authorization** `_string_`**（必选）**

请求身份认证。接口使用阿里云百炼API-Key进行身份认证。示例值：Bearer sk-xxxx。

##### **URL路径参数（Path parameters）**

**task\_id** `_string_`**（必选）**

任务ID。

#### **响应参数**

#### **任务执行成功**

```
{
    "request_id": "19171ea5-9efb-4d35-93a1-xxxxxx",
    "output": {
        "task_id": "7ed706b7-a9a9-4319-820c-xxxxxx",
        "task_status": "SUCCEEDED",
        "submit_time": "2026-03-20 10:34:41.630",
        "scheduled_time": "2026-03-20 10:34:41.655",
        "end_time": "2026-03-20 10:35:12.725",
        "orig_prompt": "下着雨，赛博城市里，一只浣熊在栏杆上行走。突然他眼睛发出蓝光，变身成一架高科技无人机，快速飞离画面。",
        "video_url": "https://media.pixverseai.cn/xxxx.mp4"
    },
    "usage": {
        "duration": 5,
        "shot_type": "single",
        "size": "1280*720",
        "fps": 24,
        "video_count": 1,
        "audio": false,
        "SR": "720"
    }
}
```

## 任务执行失败

若任务执行失败，task\_status将置为 FAILED，并提供错误码和信息。请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。

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

## 任务查询过期

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
    

**轮询过程中的状态流转：**

-   PENDING（排队中） → RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。
    
-   初次查询状态通常为 PENDING（排队中）或 RUNNING（处理中）。
    
-   当状态变为 SUCCEEDED 时，响应中将包含生成的视频url。
    
-   若状态为 FAILED，请检查错误信息并重试。
    

**submit\_time** `_string_`

任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。

**scheduled\_time** `_string_`

任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。

**end\_time** `_string_`

任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。

**video\_url** `_string_`

视频URL。仅在 task\_status 为 SUCCEEDED 时返回。

视频格式为MP4（H.264 编码）。视频链接暂无过期时间，但不建议将其作为长期存储，请及时下载。

**orig\_prompt** `_string_`

原始输入的prompt，对应请求参数`prompt`。

**code** `_string_`

请求失败的错误码。请求成功时不会返回此参数，详情请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。

**message** `_string_`

请求失败的详细信息。请求成功时不会返回此参数，详情请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。

**usage** `_object_`

输出信息统计。只对成功的结果计数。

**属性**

**duration** `_integer_`

生成视频的总视频时长（秒），用于计费。

**size** `_string_`

生成视频的分辨率。

**fps** `_integer_`

生成视频的帧率。

**SR** `_string_`

生成视频的分辨率档位。

**audio** `_boolean_`

生成视频是否为有声视频。

**video\_count** `_integer_`

生成视频的数量。固定为1。

**shot\_type** `_string_`

生成视频的镜头类型。

**request\_id** `_string_`

请求唯一标识。可用于请求明细溯源和问题排查。

## DashScope SDK调用

SDK 的参数命名与[HTTP接口](#pv101a0h2http)基本一致，参数结构根据语言特性进行封装。

由于文生视频任务耗时较长（通常为1-5分钟），SDK 在底层封装了 HTTP 异步调用流程，支持同步、异步两种调用方式。

> 具体耗时受限于排队任务数和服务执行情况，请在获取结果时耐心等待。

### Python SDK调用

**重要**

请确保 DashScope Python SDK 版本**不低于** `**1.25.8**`，再运行以下代码。

若版本过低，可能会触发 "url error, please check url!" 等错误。请参考[安装SDK](https://help.aliyun.com/zh/model-studio/install-sdk)进行更新。

**北京地域**：`dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'`

## 同步调用

##### 请求示例

```
from http import HTTPStatus
from dashscope import VideoSynthesis
import dashscope
import os

# 以下为北京地域URL
dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
# 获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
api_key = os.getenv("DASHSCOPE_API_KEY")

def sample_sync_call_t2v():
    # call sync api, will return the result
    print('please wait...')
    rsp = VideoSynthesis.call(api_key=api_key,
                              model='pixverse/pixverse-c1-t2v',
                              prompt='下着雨，赛博城市里，一只浣熊在栏杆上行走。突然他眼睛发出蓝光，变身成一架高科技无人机，快速飞离画面。',
                              size='1280*720',
                              duration=5,
                              audio=False,
                              watermark=False)
    print(rsp)
    if rsp.status_code == HTTPStatus.OK:
        print(rsp.output.video_url)
    else:
        print('Failed, status_code: %s, code: %s, message: %s' %
              (rsp.status_code, rsp.code, rsp.message))

if __name__ == '__main__':
    sample_sync_call_t2v()
```

##### 响应示例

> `video_url`暂无过期时间，但不建议将其作为长期存储，请及时下载。

```
{
    "status_code": 200,
    "request_id": "2b68d32e-86c8-4383-8a18-xxxxxx",
    "code": null,
    "message": "",
    "output": {
        "task_id": "ec40bb42-02d4-44d8-bf35-xxxxxx",
        "task_status": "SUCCEEDED",
        "video_url": "https://media.pixverseai.cn/xxx.mp4",
        "submit_time": "2026-03-20 10:59:01.993",
        "scheduled_time": "2026-03-20 10:59:02.028",
        "end_time": "2026-03-20 11:00:06.322",
        "orig_prompt": "下着雨，赛博城市里，一只浣熊在栏杆上行走。突然他眼睛发出蓝光，变身成一架高科技无人机，快速飞离画面。"
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

## 异步调用

##### 请求示例

```
from http import HTTPStatus
from dashscope import VideoSynthesis
import dashscope
import os

# 以下为北京地域URL
dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
# 获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
api_key = os.getenv("DASHSCOPE_API_KEY")

def sample_async_call_t2v():
    # call async api, will return the task information
    # you can get task status with the returned task id.
    rsp = VideoSynthesis.async_call(api_key=api_key,
                                    model='pixverse/pixverse-c1-t2v',
                                    prompt='下着雨，赛博城市里，一只浣熊在栏杆上行走。突然他眼睛发出蓝光，变身成一架高科技无人机，快速飞离画面。',
                                    size='1280*720',
                                    duration=5,
                                    audio=False,
                                    watermark=True)
    print(rsp)
    if rsp.status_code == HTTPStatus.OK:
        print("task_id: %s" % rsp.output.task_id)
    else:
        print('Failed, status_code: %s, code: %s, message: %s' %
              (rsp.status_code, rsp.code, rsp.message))

    # get the task information include the task status.
    status = VideoSynthesis.fetch(task=rsp, api_key=api_key)
    if status.status_code == HTTPStatus.OK:
        print(status.output.task_status)  # check the task status
    else:
        print('Failed, status_code: %s, code: %s, message: %s' %
              (status.status_code, status.code, status.message))

    # wait the task complete, will call fetch interval, and check it's in finished status.
    rsp = VideoSynthesis.wait(task=rsp, api_key=api_key)
    print(rsp)
    if rsp.status_code == HTTPStatus.OK:
        print(rsp.output.video_url)
    else:
        print('Failed, status_code: %s, code: %s, message: %s' %
              (rsp.status_code, rsp.code, rsp.message))

if __name__ == '__main__':
    sample_async_call_t2v()
```

##### 响应示例

1、创建任务的响应示例

```
{
	"status_code": 200,
	"request_id": "c86ff7ba-8377-917a-90ed-xxxxxx",
	"code": "",
	"message": "",
	"output": {
		"task_id": "721164c6-8619-4a35-a6d9-xxxxxx",
		"task_status": "PENDING",
		"video_url": ""
	},
	"usage": null
}
```

2、查询任务结果的响应示例

> `video_url` 暂无过期时间，但不建议将其作为长期存储，请及时下载。

```
{
    "status_code": 200,
    "request_id": "2b68d32e-86c8-4383-8a18-xxxxxx",
    "code": null,
    "message": "",
    "output": {
        "task_id": "ec40bb42-02d4-44d8-bf35-xxxxxx",
        "task_status": "SUCCEEDED",
        "video_url": "https://media.pixverseai.cn/xxx.mp4",
        "submit_time": "2026-03-20 10:59:01.993",
        "scheduled_time": "2026-03-20 10:59:02.028",
        "end_time": "2026-03-20 11:00:06.322",
        "orig_prompt": "下着雨，赛博城市里，一只浣熊在栏杆上行走。突然他眼睛发出蓝光，变身成一架高科技无人机，快速飞离画面。"
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

### Java SDK调用

**重要**

请确保 DashScope Java SDK 版本**不低于** `**2.22.6**`，再运行以下代码。

若版本过低，可能会触发 “url error, please check url!” 等错误。请参考[安装SDK](https://help.aliyun.com/zh/model-studio/install-sdk)进行更新。

**北京地域**：`Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";`

## 同步调用

##### 请求示例

```
// Copyright (c) Alibaba, Inc. and its affiliates.

import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesis;
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisParam;
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.JsonUtils;
import com.alibaba.dashscope.utils.Constants;

public class Text2Video {

    static {
        // 以下为北京地域url
        Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
    }

    // 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    // 获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    public static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    /**
     * Create a video compositing task and wait for the task to complete.
     */
    public static void text2Video() throws ApiException, NoApiKeyException, InputRequiredException {
        VideoSynthesis vs = new VideoSynthesis();
        VideoSynthesisParam param =
                VideoSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("pixverse/pixverse-c1-t2v")
                        .prompt("下着雨，赛博城市里，一只浣熊在栏杆上行走。突然他眼睛发出蓝光，变身成一架高科技无人机，快速飞离画面。")
                        .size("1280*720")
                        .duration(5)
                        .audio(true)
                        .watermark(true)
                        .seed(12345)
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

##### 响应示例

> `video_url` 暂无过期时间，但不建议将其作为长期存储，请及时下载。

```
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

## 异步调用

##### 请求示例

```
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

public class Text2Video {

    static {
        // 以下为北京地域url
        Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
    }

    // 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    // 获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    public static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    /**
     * Create a video compositing task and wait for the task to complete.
     */
    public static void text2Video() throws ApiException, NoApiKeyException, InputRequiredException {
        VideoSynthesis vs = new VideoSynthesis();

        VideoSynthesisParam param =
                VideoSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("pixverse/pixverse-c1-t2v")
                        .prompt("下着雨，赛博城市里，一只浣熊在栏杆上行走。突然他眼睛发出蓝光，变身成一架高科技无人机，快速飞离画面。")
                        .size("1280*720")
                        .duration(5)
                        .audio(true)
                        .watermark(true)
                        .seed(12345)
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

##### 响应示例

1、创建任务的响应示例。

```
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

```
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

## **错误码**

如果模型调用失败并返回报错信息，请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。

## **常见问题**

#### **Q：为什么1080P分辨率下不能使用10秒时长？**

A： `pixverse-v5.6-t2v` 在 1080P 下不支持 10 秒。建议降低分辨率至 720P/540P/360P，或切换至 `pixverse-c1-t2v`或`pixverse-v6-t2v` 模型。
