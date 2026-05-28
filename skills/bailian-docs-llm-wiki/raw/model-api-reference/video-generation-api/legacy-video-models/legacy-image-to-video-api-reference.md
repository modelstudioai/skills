# 万相-图生视频-基于首帧API参考（2.1-2.6）

万相-图生视频模型根据**首帧图像**和**文本提示词**，生成一段流畅的视频。

**相关文档**：[使用指南](https://help.aliyun.com/zh/model-studio/image-to-video-guide)

**说明**

全新推出的[万相2.7-图生视频](https://help.aliyun.com/zh/model-studio/image-to-video-general-api-reference)支持首帧生视频、首尾帧生视频、视频续写三大任务，**推荐优先选用**。

本文档的[图生视频-基于首帧](#)（wan2.6及早期模型）仅支持首帧生视频。

## 适用范围

为确保调用成功，请务必保证模型、endpoint URL 和 API Key 均属于**同一地域**。跨地域调用将会失败。

-   [**选择模型**](https://help.aliyun.com/zh/model-studio/image-to-video-guide#06f39eafa2dwt)：确认模型所属的地域。
    
-   **选择 URL**：选择对应的地域 Endpoint URL，支持HTTP URL或 DashScope SDK URL。
    
-   **配置 API Key**：获取该地域的[API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
    
-   **安装 SDK**：如需通过SDK进行调用，请[安装DashScope SDK](https://help.aliyun.com/zh/model-studio/install-sdk)。
    

**说明**

本文的示例代码适用于**北京地域**。

## HTTP调用

图生视频任务耗时较长（通常为1-5分钟），API采用异步调用的方式。整个流程包含 **“创建任务 -> 轮询获取”** 两个核心步骤，具体如下：

### 步骤1：创建任务获取任务ID

## **北京**

`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`

## **新加坡**

`POST https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`

## **弗吉尼亚**

`POST https://dashscope-us.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`

## 法兰克福

`POST https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`

调用时请将`WorkspaceId`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#d3eb3cd37b7fu)。

**说明**

-   创建成功后，使用接口返回的 `task_id` 查询结果，task\_id 有效期为 24 小时。**请勿重复创建任务**，轮询获取即可。
    
-   新手指引请参见[Postman](https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api)。
    

#### 请求参数

## 多镜头叙事

仅wan2.6系列模型支持此功能。

可通过设置`"prompt_extend": true`和`"shot_type":"multi"`启用。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "wan2.6-i2v-flash",
    "input": {
        "prompt": "一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色。一个由喷漆所画成的少年，正从一面混凝土墙上活过来。他一边用极快的语速演唱一首英文rap，一边摆着一个经典的、充满活力的说唱歌手姿势。场景设定在夜晚一个充满都市感的铁路桥下。灯光来自一盏孤零零的街灯，营造出电影般的氛围，充满高能量和惊人的细节。视频的音频部分完全由他的rap构成，没有其他对话或杂音。",
        "img_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/wpimhv/rap.png",
        "audio_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/ozwpvi/rap.mp3"
    },
    "parameters": {
        "resolution": "720P",
        "prompt_extend": true,
        "duration": 10,
        "shot_type":"multi"
    }
}'
```

## 自动配音

仅wan2.6和wan2.5系列模型支持此功能。

若不提供 `input.audio_url` ，模型将根据视频内容自动生成匹配的背景音乐或音效。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "wan2.5-i2v-preview",
    "input": {
        "prompt": "一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色。一个由喷漆所画成的少年，正从一面混凝土墙上活过来。他一边用极快的语速演唱一首英文rap，一边摆着一个经典的、充满活力的说唱歌手姿势。场景设定在夜晚一个充满都市感的铁路桥下。灯光来自一盏孤零零的街灯，营造出电影般的氛围，充满高能量和惊人的细节。视频的音频部分完全由他的rap构成，没有其他对话或杂音。",
        "img_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/wpimhv/rap.png"
    },
    "parameters": {
        "resolution": "480P",
        "prompt_extend": true,
        "duration": 10
    }
}'
```

## 传入音频文件

仅wan2.6和wan2.5系列模型支持此功能。

如需为视频指定背景音乐或配音，可通过 `input.audio_url` 参数传入自定义音频的 URL。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "wan2.5-i2v-preview",
    "input": {
        "prompt": "一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色。一个由喷漆所画成的少年，正从一面混凝土墙上活过来。他一边用极快的语速演唱一首英文rap，一边摆着一个经典的、充满活力的说唱歌手姿势。场景设定在夜晚一个充满都市感的铁路桥下。灯光来自一盏孤零零的街灯，营造出电影般的氛围，充满高能量和惊人的细节。视频的音频部分完全由他的rap构成，没有其他对话或杂音。",
        "img_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/wpimhv/rap.png",
        "audio_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/ozwpvi/rap.mp3"
    },
    "parameters": {
        "resolution": "480P",
        "prompt_extend": true,
        "duration": 10
    }
}'
```

## 生成无声视频

仅以下模型支持生成无声视频：

-   wan2.6-i2v-flash：若需生成无声视频，**必须显式设置** `parameters.audio = false`。
    
-   wan2.2 和wanx2.1系列模型：默认生成无声视频，无需额外参数配置。
    

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "wan2.2-i2v-plus",
    "input": {
        "prompt": "一只猫在草地上奔跑",
        "img_url": "https://cdn.translate.alibaba.com/r/wanx-demo-1.png"
    },
    "parameters": {
        "resolution": "480P",
        "prompt_extend": true
    }
}'
```

## 使用Base64

通过 `img_url` 参数传入图像的 Base64 编码字符串。

关于 Base64 字符串的格式要求，请参见[传入图像](https://help.aliyun.com/zh/model-studio/image-to-video-guide#32d9db99f1fk0)。

示例：下载[img\_base64](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250722/pmcjis/img_base64.txt)文件，并将完整内容粘贴至`img_url`参数中。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "wan2.2-i2v-plus",
    "input": {
        "prompt": "一只猫在草地上奔跑",
        "img_url": "data:image/png;base64,GDU7MtCZzEbTbmRZ......"
    },
    "parameters": {
        "resolution": "480P",
        "prompt_extend": true
    }
}'
```

## 使用视频特效

-   prompt 字段将被忽略，建议留空。
    
-   特效的可用性与模型相关。调用前请查阅[万相-图生视频-视频特效](https://help.aliyun.com/zh/model-studio/wanx-video-effects)，以免调用失败。
    

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "wanx2.1-i2v-turbo",
    "input": {
        "img_url": "https://cdn.translate.alibaba.com/r/wanx-demo-1.png",
        "template": "flying"
    },
    "parameters": {
        "resolution": "720P"
    }
}'
```

## 使用反向提示词

通过 negative\_prompt 指定生成的视频避免出现“花朵”元素。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "wan2.2-i2v-plus",
    "input": {
        "prompt": "一只猫在草地上奔跑",
        "negative_prompt": "花朵",
        "img_url": "https://cdn.translate.alibaba.com/r/wanx-demo-1.png"
    },
    "parameters": {
        "resolution": "480P",
        "prompt_extend": true
    }
}'
```

##### 请求头（Headers）

**Content-Type** `_string_` **（必选）**

请求内容类型。此参数必须设置为`application/json`。

**Authorization** `_string_`**（必选）**

请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。

**X-DashScope-Async** `_string_` **（必选）**

异步处理配置参数。HTTP请求只支持异步，**必须设置为**`**enable**`。

**重要**

缺少此请求头将报错：“current user api does not support synchronous calls”。

##### 请求体（Request Body）

**model** `_string_` **（必选）**

模型名称。模型列表与价格详见[模型价格](https://help.aliyun.com/zh/model-studio/model-pricing#517789fb633zr)。

示例值：wan2.6-i2v-flash。

**input** `_object_` **（必选）**

输入的基本信息，如提示词等。

**属性**

**prompt** `_string_` （可选）

文本提示词。用来描述生成图像中期望包含的元素和视觉特点。

支持中英文，每个汉字/字母占一个字符，超过部分会自动截断。长度限制因模型版本而异：

-   wan2.6和wan2.5系列模型：长度不超过1500个字符。
    
-   wan2.2 和wanx2.1系列模型：长度不超过800个字符。
    

当使用视频特效参数（即`template`不为空）时，prompt参数无效，无需填写。

示例值：一只小猫在草地上奔跑。

提示词使用技巧详见[文生视频/图生视频Prompt指南](https://help.aliyun.com/zh/model-studio/text-to-video-prompt)。

**negative\_prompt** `_string_` （可选）

反向提示词，用来描述不希望在视频画面中看到的内容，可以对视频画面进行限制。

支持中英文，长度不超过500个字符，超过部分会自动截断。

示例值：低分辨率、错误、最差质量、低质量、残缺、多余的手指、比例不良等。

**img\_url** `_string_` **（必选）**

首帧图像的URL或 Base64 编码数据。

图像限制：

-   图像格式：JPEG、JPG、PNG（不支持透明通道）、BMP、WEBP。
    
-   图像分辨率：图像的宽度和高度范围为\[240,8000\]，单位为像素。
    
-   文件大小：
    
    -   wan2.6和wan2.5系列模型：不超过20MB。
        
    -   wan2.2 和wanx2.1系列模型：不超过10MB。
        

支持输入的格式：

1.  公网URL:
    
    -   支持 HTTP 或 HTTPS 协议。
        
    -   示例值：https://cdn.translate.alibaba.com/r/wanx-demo-1.png。
        
2.  临时URL：
    
    -   支持OSS协议，必须通过[上传文件获取临时 URL](https://help.aliyun.com/zh/model-studio/get-temporary-file-url)。
        
    -   示例值：oss://dashscope-instant/xxx/xxx.png。
        
3.  Base64 编码图像后的字符串：
    
    -   数据格式：`data:{MIME_type};base64,{base64_data}`。
        
    -   示例值：data:image/png;base64,GDU7MtCZzEbTbmRZ......。（编码字符串过长，仅展示片段）
        
    -   详情请参见[传入图像](https://help.aliyun.com/zh/model-studio/image-to-video-guide#32d9db99f1fk0)。
        

**audio\_url** `_string_` （可选）

**支持模型：wan2.6和wan2.5系列模型。**

音频文件的 URL，模型将使用该音频生成视频。

支持输入的格式：

1.  公网URL：
    
    -   支持 HTTP 和 HTTPS 协议。
        
    -   示例值：https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/xxx.mp3。
        
2.  临时URL：
    
    -   支持OSS协议，必须通过[上传文件获取临时 URL](https://help.aliyun.com/zh/model-studio/get-temporary-file-url)。
        
    -   示例值：oss://dashscope-instant/xxx/2024-07-18/xxx/xxx.mp3。
        

音频限制：

-   格式：wav、mp3。
    
-   时长：3～30s。
    
-   文件大小：不超过15MB。
    
-   超限处理：若音频长度超过 `duration` 值（5秒或10秒），自动截取前5秒或10秒，其余部分丢弃。若音频长度不足视频时长，超出音频长度部分为无声视频。例如，音频为3秒，视频时长为5秒，输出视频前3秒有声，后2秒无声。
    

示例值：https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/ozwpvi/rap.mp3。

**template** `_string_` （可选）

视频特效模板的名称。若未填写，表示不使用任何视频特效。

不同模型支持不同的特效模板。调用前请查阅[万相-图生视频-视频特效](https://help.aliyun.com/zh/model-studio/wanx-video-effects)，以免调用失败。

示例值：flying，表示使用“魔法悬浮”特效。

**parameters** `_object_` （可选）

视频处理参数，如设置视频分辨率、设置视频时长、开启prompt智能改写、添加水印等。

**属性**

**resolution** `_string_` （可选）

**重要**

resolution直接影响费用，请在调用前确认[模型价格](https://help.aliyun.com/zh/model-studio/model-pricing#517789fb633zr)。

指定生成的视频分辨率档位，用于调整视频的清晰度（总像素）。模型根据选择的分辨率档位，自动缩放至相近总像素，**视频宽高比将尽量与输入图像 img\_url 的宽高比保持一致**，详见[常见问题](#2b6ac4aea9h5n)。

此参数的默认值和可用枚举值依赖于 model 参数，规则如下：

-   wan2.6-i2v-flash：可选值：720P、1080P。默认值为`1080P`。
    
-   wan2.6-i2v ：可选值：720P、1080P。默认值为`1080P`。
    
-   wan2.6-i2v-us ：可选值：720P、1080P。默认值为`1080P`。
    
-   wan2.5-i2v-preview ：可选值：480P、720P、1080P。默认值为`1080P`。
    
-   wan2.2-i2v-flash：可选值：480P、720P、1080P。默认值为`720P`。
    
-   wan2.2-i2v-plus：可选值：480P、1080P。默认值为`1080P`。
    
-   wanx2.1-i2v-turbo：可选值：480P、720P。默认值为`720P`。
    
-   wanx2.1-i2v-plus：可选值：720P。默认值为`720P`。
    

示例值：1080P。

**duration** `_integer_` （可选）

**重要**

duration直接影响费用，请在调用前确认[模型价格](https://help.aliyun.com/zh/model-studio/model-pricing#517789fb633zr)。

生成视频的时长，单位为秒。该参数的取值依赖于 model参数：

-   wan2.6-i2v-flash：取值为\[2, 15\]之间的整数。默认值为5。
    
-   wan2.6-i2v：取值为\[2, 15\]之间的整数。默认值为5。
    
-   wan2.6-i2v-us：可选值为5、10、15。默认值为5。
    
-   wan2.5-i2v-preview：可选值为5、10。默认值为5。
    
-   wan2.2-i2v-plus：固定为5秒，且不支持修改。
    
-   wan2.2-i2v-flash：固定为5秒，且不支持修改。
    
-   wanx2.1-i2v-plus：固定为5秒，且不支持修改。
    
-   wanx2.1-i2v-turbo：可选值为3、4或5。默认值为5。
    

示例值：5。

**prompt\_extend** `_boolean_` （可选）

是否开启prompt智能改写。开启后使用大模型对输入prompt进行智能改写。对于较短的prompt生成效果提升明显，但会增加耗时。

-   true：默认值，开启智能改写。
    
-   false：不开启智能改写。
    

示例值：true。

**shot\_type** `_string_` （可选）

**支持模型：wan2.6系列模型。**

指定生成视频的镜头类型，即视频是由一个连续镜头还是多个切换镜头组成。

生效条件：仅当`"prompt_extend": true` 时生效。

参数优先级：`shot_type > prompt`。例如，若 shot\_type设置为"single"，即使 prompt 中包含“生成多镜头视频”，模型仍会输出单镜头视频。

可选值：

-   single：默认值，输出单镜头视频
    
-   multi：输出多镜头视频。
    

示例值：single。

**说明**

当希望严格控制视频的叙事结构（如产品展示用单镜头、故事短片用多镜头），可通过此参数指定。

**audio** `_boolean_` （可选）

**重要**

audio直接影响费用，有声视频与无声视频价格不同，请前往百炼控制台查看价格。

**支持模型：wan2.6-i2v-flash。**

是否生成有声视频。

参数优先级：`audio > audio_url`。当 `audio=false`时，即使传入 `audio_url`，输出仍为无声视频，且计费按无声视频计算。

可选值：

-   true：默认值，输出有声视频。
    
-   false：输出无声视频。
    

示例值：true。

**watermark** `_boolean_` （可选）

是否添加水印标识，水印位于视频右下角，文案固定为“AI生成”。

-   false：默认值，不添加水印。
    
-   true：添加水印。
    

示例值：false。

**seed** `_integer_` （可选）

随机数种子，取值范围为`[0, 2147483647]`。

未指定时，系统自动生成随机种子。若需提升生成结果的可复现性，建议固定seed值。

请注意，由于模型生成具有概率性，即使使用相同 seed，也不能保证每次生成结果完全一致。

示例值：12345。

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

属性

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

### 步骤2：根据任务ID查询结果

## **北京**

`GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`

## **新加坡**

`GET https://dashscope-intl.aliyuncs.com/api/v1/tasks/{task_id}`

## **弗吉尼亚**

`GET https://dashscope-us.aliyuncs.com/api/v1/tasks/{task_id}`

## 法兰克福

`GET https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/api/v1/tasks/{task_id}`

调用时请将`WorkspaceId`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#d3eb3cd37b7fu)。

**说明**

-   **轮询建议**：视频生成过程约需数分钟，建议采用**轮询**机制，并设置合理的查询间隔（如 15 秒）来获取结果。
    
-   **任务状态流转**：PENDING（排队中）→ RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。
    
-   **结果链接**：任务成功后返回视频链接，有效期为 **24 小时**。建议在获取链接后立即下载并转存至永久存储（如[阿里云 OSS](https://help.aliyun.com/zh/oss/user-guide/what-is-oss)）。
    
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

请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。

##### **URL路径参数（Path parameters）**

**task\_id** `_string_`**（必选）**

任务ID。

#### **响应参数**

## 任务执行成功

视频URL仅保留24小时，超时后会被自动清除，请及时保存生成的视频。

```
{
    "request_id": "2ca1c497-f9e0-449d-9a3f-xxxxxx",
    "output": {
        "task_id": "af6efbc0-4bef-4194-8246-xxxxxx",
        "task_status": "SUCCEEDED",
        "submit_time": "2025-09-25 11:07:28.590",
        "scheduled_time": "2025-09-25 11:07:35.349",
        "end_time": "2025-09-25 11:17:11.650",
        "orig_prompt": "一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色。一个由喷漆所画成的少年，正从一面混凝土墙上活过来。他一边用极快的语速演唱一首英文rap，一边摆着一个经典的、充满活力的说唱歌手姿势。场景设定在夜晚一个充满都市感的铁路桥下。灯光来自一盏孤零零的街灯，营造出电影般的氛围，充满高能量和惊人的细节。视频的音频部分完全由他的rap构成，没有其他对话或杂音。",
        "video_url": "https://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/xxx.mp4?Expires=xxx"
    },
    "usage": {
        "duration": 10,
        "input_video_duration": 0,
        "output_video_duration": 10,
        "video_count": 1,
        "SR": 720
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
    
-   当状态变为 SUCCEEDED 时，响应中将包含生成的视频URL。
    
-   若状态为 FAILED，请检查错误信息并重试。
    
-   若状态为 CANCELED，表示任务已取消，如需继续请重新提交任务。
    
-   若状态为 UNKNOWN，表示任务不存在或状态未知，可能在 task\_id 不存在或超过 24 小时有效期后出现。
    

**submit\_time** `_string_`

任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。

**scheduled\_time** `_string_`

任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。

**end\_time** `_string_`

任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。

**video\_url** `_string_`

视频URL。仅在 task\_status 为 SUCCEEDED 时返回。

链接有效期24小时，可通过此URL下载视频。视频格式为MP4（H.264 编码）。

**orig\_prompt** `_string_`

原始输入的prompt，对应请求参数`prompt`。

**actual\_prompt** `_string_`

当 `prompt_extend=true` 时，系统会对输入 prompt 进行智能改写，此字段返回实际用于生成的优化后 prompt。

-   若 `prompt_extend=false`，该字段不会返回。
    
-   注意：wan2.6 模型无论 `prompt_extend` 取值如何，均不返回此字段。
    

**code** `_string_`

请求失败的错误码。请求成功时不会返回此参数，详情请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。

**message** `_string_`

请求失败的详细信息。请求成功时不会返回此参数，详情请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。

**usage** `_object_`

输出信息统计，只对成功的结果计数。

**属性**

**wan2.6系列模型返回参数**

**input\_video\_duration** `_integer_`

输入的视频的时长，单位秒。当前不支持传入视频，因此固定为0。

**output\_video\_duration** `_integer_`

仅在使用 wan2.6 模型时返回。

输出视频的时长，单位秒。其值等同于`input.duration`的值。

**duration** `_integer_`

总的视频时长，用于计费。

计费公式：`duration=input_video_duration+output_video_duration`。

**SR** `_integer_`

仅在使用 wan2.6 模型时返回。生成视频的分辨率档位。示例值：720。

**video\_count** `_integer_`

生成视频的数量。固定为1。

**audio**`_boolean_`

仅在使用wan2.6-i2v-flash模型时返回。表示输出视频是否为有声视频。

**wan2.2和wan2.5系列模型返回参数**

**duration** `_integer_`

生成视频的时长，单位为秒。枚举值为5、10。

计费公式：费用 = 视频秒数 × 单价。

**SR** `_integer_`

生成视频的分辨率。枚举值为480、720、1080。

**video\_count** `_integer_`

生成视频的数量。固定为1。

**wan2.1系列模型返回参数**

**video\_duration** `_integer_`

生成视频的时长，单位为秒。枚举值为3、4、5。

计费公式：费用 = 视频秒数 × 单价。

**video\_ratio** `_string_`

生成视频的比例。固定为standard。

**video\_count** `_integer_`

生成视频的数量。固定为1。

**request\_id** `_string_`

请求唯一标识。可用于请求明细溯源和问题排查。

## DashScope SDK调用

SDK 的参数命名与[HTTP接口](#42703589880ts)基本一致，参数结构根据语言特性进行封装。

由于图生视频任务耗时较长（通常为1-5分钟），SDK 在底层封装了 HTTP 异步调用流程，支持同步、异步两种调用方式。

> 具体耗时受限于排队任务数和服务执行情况，请在获取结果时耐心等待。

### Python SDK调用

**重要**

请确保 DashScope Python SDK 版本**不低于** `**1.25.8**`，再运行以下代码。

若版本过低，可能会触发 “url error, please check url!” 等错误。请参考[安装SDK](https://help.aliyun.com/zh/model-studio/install-sdk)进行更新。

根据模型所在地域设置 `**base_http_api_url**`:

## **北京**

`dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'`

## **新加坡**

`dashscope.base_http_api_url = 'https://dashscope-intl.aliyuncs.com/api/v1'`

## **弗吉尼亚**

`dashscope.base_http_api_url = 'https://dashscope-us.aliyuncs.com/api/v1'`

## 法兰克福

`dashscope.base_http_api_url = 'https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/api/v1'`

调用时请将`WorkspaceId`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#d3eb3cd37b7fu)。

#### **示例代码**

## **同步调用**

同步调用会阻塞等待，直到视频生成完成并返回结果。本示例展示三种图像输入方式：公网URL、Base64编码、本地文件路径。

##### 请求示例

```
import base64
import os
from http import HTTPStatus
from dashscope import VideoSynthesis
import mimetypes
import dashscope

# 以下为北京地域url，获取url：https://help.aliyun.com/zh/model-studio/image-to-video-api-reference
dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
# 获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
api_key = os.getenv("DASHSCOPE_API_KEY")

# --- 辅助函数：用于 Base64 编码 ---
# 格式为 data:{MIME_type};base64,{base64_data}
def encode_file(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type or not mime_type.startswith("image/"):
        raise ValueError("不支持或无法识别的图像格式")
    with open(file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return f"data:{mime_type};base64,{encoded_string}"

"""
图像输入方式说明：
以下提供了三种图片输入方式，三选一即可

1. 使用公网URL - 适合已有公开可访问的图片
2. 使用本地文件 - 适合本地开发测试
3. 使用Base64编码 - 适合私有图片或需要加密传输的场景
"""

# 【方式一】使用公网可访问的图片URL
# 示例：使用一个公开的图片URL
img_url = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/wpimhv/rap.png"

# 【方式二】使用本地文件（支持绝对路径和相对路径）
# 格式要求：file:// + 文件路径
# 示例（绝对路径）：
# img_url = "file://" + "/path/to/your/img.png"    # Linux/macOS
# img_url = "file://" + "/C:/path/to/your/img.png"  # Windows
# 示例（相对路径）：
# img_url = "file://" + "./img.png"                # 相对当前执行文件的路径

# 【方式三】使用Base64编码的图片
# img_url = encode_file("./img.png")

# 设置音频audio url
audio_url = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/ozwpvi/rap.mp3"

def sample_call_i2v():
    # 同步调用，直接返回结果
    print('please wait...')
    rsp = VideoSynthesis.call(api_key=api_key,
                              model='wan2.6-i2v-flash',
                              prompt='一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色。一个由喷漆所画成的少年，正从一面混凝土墙上活过来。他一边用极快的语速演唱一首英文rap，一边摆着一个经典的、充满活力的说唱歌手姿势。场景设定在夜晚一个充满都市感的铁路桥下。灯光来自一盏孤零零的街灯，营造出电影般的氛围，充满高能量和惊人的细节。视频的音频部分完全由他的rap构成，没有其他对话或杂音。',
                              img_url=img_url,
                              audio_url=audio_url,
                              resolution="720P",
                              duration=10,
                              prompt_extend=True,
                              watermark=False,
                              negative_prompt="",
                              seed=12345)
    print(rsp)
    if rsp.status_code == HTTPStatus.OK:
        print("video_url:", rsp.output.video_url)
    else:
        print('Failed, status_code: %s, code: %s, message: %s' %
              (rsp.status_code, rsp.code, rsp.message))

if __name__ == '__main__':
    sample_call_i2v()
```

##### 响应示例

> video\_url 有效期24小时，请及时下载视频。

```
{
    "status_code": 200,
    "request_id": "2794c7a3-fe8c-4dd4-a1b7-xxxxxx",
    "code": null,
    "message": "",
    "output": {
        "task_id": "c15d5b14-07c4-4af5-b862-xxxxxx",
        "task_status": "SUCCEEDED",
        "video_url": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx.mp4?Expires=xxx",
        "submit_time": "2026-01-22 23:24:46.527",
        "scheduled_time": "2026-01-22 23:24:46.565",
        "end_time": "2026-01-22 23:25:59.978",
        "orig_prompt": "一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色。一个由喷漆所画成的少年，正从一面混凝土墙上活过来。他一边用极快的语速演唱一首英文rap，一边摆着一个经典的、充满活力的说唱歌手姿势。场景设定在夜晚一个充满都市感的铁路桥下。灯光来自一盏孤零零的街灯，营造出电影般的氛围，充满高能量和惊人的细节。视频的音频部分完全由他的rap构成，没有其他对话或杂音。"
    },
    "usage": {
        "video_count": 1,
        "video_duration": 0,
        "video_ratio": "",
        "duration": 10,
        "input_video_duration": 0,
        "output_video_duration": 10,
        "audio": true,
        "SR": 720
    }
}
```

## 异步调用

本示例展示异步调用方式。该方式会立即返回任务ID，需要自行轮询或等待任务完成。

##### 请求示例

```
import os
from http import HTTPStatus
from dashscope import VideoSynthesis
import dashscope

# 以下为北京地域url，获取url：https://help.aliyun.com/zh/model-studio/image-to-video-api-reference
dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
# 获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
api_key = os.getenv("DASHSCOPE_API_KEY")

# 使用公网可访问的图片URL
img_url = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/wpimhv/rap.png"

# 设置音频audio url
audio_url = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/ozwpvi/rap.mp3"

def sample_async_call_i2v():
    # 异步调用，返回一个task_id
    rsp = VideoSynthesis.async_call(api_key=api_key,
                                    model='wan2.6-i2v-flash',
                                    prompt='一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色。一个由喷漆所画成的少年，正从一面混凝土墙上活过来。他一边用极快的语速演唱一首英文rap，一边摆着一个经典的、充满活力的说唱歌手姿势。场景设定在夜晚一个充满都市感的铁路桥下。灯光来自一盏孤零零的街灯，营造出电影般的氛围，充满高能量和惊人的细节。视频的音频部分完全由他的rap构成，没有其他对话或杂音。',
                                    img_url=img_url,
                                    audio_url=audio_url,
                                    resolution="720P",
                                    duration=10,
                                    prompt_extend=True,
                                    watermark=False,
                                    negative_prompt="",
                                    seed=12345)
    print(rsp)
    if rsp.status_code == HTTPStatus.OK:
        print("task_id: %s" % rsp.output.task_id)
    else:
        print('Failed, status_code: %s, code: %s, message: %s' %
              (rsp.status_code, rsp.code, rsp.message))

    # 获取异步任务信息
    status = VideoSynthesis.fetch(task=rsp, api_key=api_key)
    if status.status_code == HTTPStatus.OK:
        print(status.output.task_status)
    else:
        print('Failed, status_code: %s, code: %s, message: %s' %
              (status.status_code, status.code, status.message))

    # 等待异步任务结束
    rsp = VideoSynthesis.wait(task=rsp, api_key=api_key)
    print(rsp)
    if rsp.status_code == HTTPStatus.OK:
        print(rsp.output.video_url)
    else:
        print('Failed, status_code: %s, code: %s, message: %s' %
              (rsp.status_code, rsp.code, rsp.message))

if __name__ == '__main__':
    sample_async_call_i2v()
```

##### 响应示例

1、创建任务的响应示例

```
{
    "status_code": 200,
    "request_id": "6dc3bf6c-be18-9268-9c27-xxxxxx",
    "code": "",
    "message": "",
    "output": {
        "task_id": "686391d9-7ecf-4290-a8e9-xxxxxx",
        "task_status": "PENDING",
        "video_url": ""
    },
    "usage": null
}
```

2、查询任务结果的响应示例

> video\_url 有效期24小时，请及时下载视频。

```
{
    "status_code": 200,
    "request_id": "2794c7a3-fe8c-4dd4-a1b7-xxxxxx",
    "code": null,
    "message": "",
    "output": {
        "task_id": "c15d5b14-07c4-4af5-b862-xxxxxx",
        "task_status": "SUCCEEDED",
        "video_url": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx.mp4?Expires=xxx",
        "submit_time": "2026-01-22 23:24:46.527",
        "scheduled_time": "2026-01-22 23:24:46.565",
        "end_time": "2026-01-22 23:25:59.978",
        "orig_prompt": "一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色。一个由喷漆所画成的少年，正从一面混凝土墙上活过来。他一边用极快的语速演唱一首英文rap，一边摆着一个经典的、充满活力的说唱歌手姿势。场景设定在夜晚一个充满都市感的铁路桥下。灯光来自一盏孤零零的街灯，营造出电影般的氛围，充满高能量和惊人的细节。视频的音频部分完全由他的rap构成，没有其他对话或杂音。"
    },
    "usage": {
        "video_count": 1,
        "video_duration": 0,
        "video_ratio": "",
        "duration": 10,
        "input_video_duration": 0,
        "output_video_duration": 10,
        "audio": true,
        "SR": 720
    }
}
```

### Java SDK调用

**重要**

请确保 DashScope Java SDK 版本**不低于** `**2.22.6**`，再运行以下代码。

若版本过低，可能会触发 “url error, please check url!” 等错误。请参考[安装SDK](https://help.aliyun.com/zh/model-studio/install-sdk)进行更新。

根据模型所在地域设置 `**baseHttpApiUrl**`:

## **北京**

`Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";`

## **新加坡**

`Constants.baseHttpApiUrl = "https://dashscope-intl.aliyuncs.com/api/v1";`

## **弗吉尼亚**

`Constants.baseHttpApiUrl = "https://dashscope-us.aliyuncs.com/api/v1";`

## 法兰克福

`Constants.baseHttpApiUrl = "https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/api/v1";`

调用时请将`WorkspaceId`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#d3eb3cd37b7fu)。

#### **示例代码**

## 同步调用

同步调用会阻塞等待，直到视频生成完成并返回结果。本示例展示三种图像输入方式：公网URL、Base64编码、本地文件路径。

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

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Base64;
import java.util.HashMap;
import java.util.Map;
 
public class Image2Video {

    static {
        // 以下为北京地域url，获取url：https://help.aliyun.com/zh/model-studio/image-to-video-api-reference
        Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
    }

    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey="sk-xxx"
    // 获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    static String apiKey = System.getenv("DASHSCOPE_API_KEY");
    
    /**
     * 图像输入方式说明：三选一即可
     *
     * 1. 使用公网URL - 适合已有公开可访问的图片
     * 2. 使用本地文件 - 适合本地开发测试
     * 3. 使用Base64编码 - 适合私有图片或需要加密传输的场景
     */

    //【方式一】公网URL
    static String imgUrl = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/wpimhv/rap.png";

    //【方式二】本地文件路径（file://+绝对路径）
    // static String imgUrl = "file://" + "/your/path/to/img.png";    // Linux/macOS
    // static String imgUrl = "file://" + "/C:/your/path/to/img.png";  // Windows

    //【方式三】Base64编码
    // static String imgUrl = Image2Video.encodeFile("/your/path/to/img.png");
    
    // 设置音频audio url
    static String audioUrl = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/ozwpvi/rap.mp3";

    public static void image2video() throws ApiException, NoApiKeyException, InputRequiredException {
        // 设置parameters参数
        Map<String, Object> parameters = new HashMap<>();
        parameters.put("prompt_extend", true);
        parameters.put("watermark", false);
        parameters.put("seed", 12345);

        VideoSynthesis vs = new VideoSynthesis();
        VideoSynthesisParam param =
                VideoSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("wan2.6-i2v-flash")
                        .prompt("一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色。一个由喷漆所画成的少年，正从一面混凝土墙上活过来。他一边用极快的语速演唱一首英文rap，一边摆着一个经典的、充满活力的说唱歌手姿势。场景设定在夜晚一个充满都市感的铁路桥下。灯光来自一盏孤零零的街灯，营造出电影般的氛围，充满高能量和惊人的细节。视频的音频部分完全由他的rap构成，没有其他对话或杂音。")
                        .imgUrl(imgUrl)
                        .audioUrl(audioUrl)
                        .duration(10)
                        .parameters(parameters)
                        .resolution("720P")
                        .negativePrompt("")
                        .build();
        System.out.println("please wait...");
        VideoSynthesisResult result = vs.call(param);
        System.out.println(JsonUtils.toJson(result));
    }
    
     /**
     * 将文件编码为Base64字符串
     * @param filePath 文件路径
     * @return Base64字符串，格式为 data:{MIME_type};base64,{base64_data}
     */
    public static String encodeFile(String filePath) {
        Path path = Paths.get(filePath);
        if (!Files.exists(path)) {
            throw new IllegalArgumentException("文件不存在: " + filePath);
        }
        // 检测MIME类型
        String mimeType = null;
        try {
            mimeType = Files.probeContentType(path);
        } catch (IOException e) {
            throw new IllegalArgumentException("无法检测文件类型: " + filePath);
        }
        if (mimeType == null || !mimeType.startsWith("image/")) {
            throw new IllegalArgumentException("不支持或无法识别的图像格式");
        }
        // 读取文件内容并编码
        byte[] fileBytes = null;
        try{
            fileBytes = Files.readAllBytes(path);
        } catch (IOException e) {
            throw new IllegalArgumentException("无法读取文件内容: " + filePath);
        }
    
        String encodedString = Base64.getEncoder().encodeToString(fileBytes);
        return "data:" + mimeType + ";base64," + encodedString;
    }
    

    public static void main(String[] args) {
        try {
            image2video();
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

##### 响应示例

> video\_url 有效期24小时，请及时下载视频。

```
{
    "request_id": "87c091bb-7a3c-4904-8501-xxxxxx",
    "output": {
        "task_id": "413ed6e4-5f3a-4f57-8d58-xxxxxx",
        "task_status": "SUCCEEDED",
        "video_url": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx.mp4?Expires=xxx",
        "orig_prompt": "一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色。一个由喷漆所画成的少年，正从一面混凝土墙上活过来。他一边用极快的语速演唱一首英文rap，一边摆着一个经典的、充满活力的说唱歌手姿势。场景设定在夜晚一个充满都市感的铁路桥下。灯光来自一盏孤零零的街灯，营造出电影般的氛围，充满高能量和惊人的细节。视频的音频部分完全由他的rap构成，没有其他对话或杂音。",
        "submit_time": "2026-01-22 23:25:45.729",
        "scheduled_time": "2026-01-22 23:25:45.771",
        "end_time": "2026-01-22 23:26:44.942"
    },
    "usage": {
        "video_count": 1,
        "duration": 10.0,
        "input_video_duration": 0.0,
        "output_video_duration": 10.0,
        "SR": "720"
    },
    "status_code": 200,
    "code": "",
    "message": ""
}
```

## 异步调用

本示例展示异步调用方式。该方式会立即返回任务ID，需要自行轮询或等待任务完成。

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

import java.util.HashMap;
import java.util.Map;

public class Image2Video {

    static {
        // 以下为北京地域url，获取url：https://help.aliyun.com/zh/model-studio/image-to-video-api-reference
        Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
    }

    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey="sk-xxx"
    // 获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    static String apiKey = System.getenv("DASHSCOPE_API_KEY");
    
    //设置输入图像url
    static String imgUrl = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/wpimhv/rap.png";

    // 设置音频audio url
    static String audioUrl = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/ozwpvi/rap.mp3";

    public static void image2video() throws ApiException, NoApiKeyException, InputRequiredException {
        // 设置parameters参数
        Map<String, Object> parameters = new HashMap<>();
        parameters.put("prompt_extend", true);
        parameters.put("watermark", false);
        parameters.put("seed", 12345);

        VideoSynthesis vs = new VideoSynthesis();
        VideoSynthesisParam param =
                VideoSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("wan2.6-i2v-flash")
                        .prompt("一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色。一个由喷漆所画成的少年，正从一面混凝土墙上活过来。他一边用极快的语速演唱一首英文rap，一边摆着一个经典的、充满活力的说唱歌手姿势。场景设定在夜晚一个充满都市感的铁路桥下。灯光来自一盏孤零零的街灯，营造出电影般的氛围，充满高能量和惊人的细节。视频的音频部分完全由他的rap构成，没有其他对话或杂音。")
                        .imgUrl(imgUrl)
                        .audioUrl(audioUrl)
                        .duration(10)
                        .parameters(parameters)
                        .resolution("720P")
                        .negativePrompt("")
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
            image2video();
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

##### 响应示例

1、创建任务的响应示例

```
{
    "request_id": "5dbf9dc5-4f4c-9605-85ea-xxxxxxxx",
    "output": {
        "task_id": "7277e20e-aa01-4709-xxxxxxxx",
        "task_status": "PENDING"
    }
}
```

2、查询任务结果的响应示例

> video\_url 有效期24小时，请及时下载视频。

```
{
    "request_id": "87c091bb-7a3c-4904-8501-xxxxxx",
    "output": {
        "task_id": "413ed6e4-5f3a-4f57-8d58-xxxxxx",
        "task_status": "SUCCEEDED",
        "video_url": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx.mp4?Expires=xxx",
        "orig_prompt": "一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色。一个由喷漆所画成的少年，正从一面混凝土墙上活过来。他一边用极快的语速演唱一首英文rap，一边摆着一个经典的、充满活力的说唱歌手姿势。场景设定在夜晚一个充满都市感的铁路桥下。灯光来自一盏孤零零的街灯，营造出电影般的氛围，充满高能量和惊人的细节。视频的音频部分完全由他的rap构成，没有其他对话或杂音。",
        "submit_time": "2026-01-22 23:25:45.729",
        "scheduled_time": "2026-01-22 23:25:45.771",
        "end_time": "2026-01-22 23:26:44.942"
    },
    "usage": {
        "video_count": 1,
        "duration": 10.0,
        "input_video_duration": 0.0,
        "output_video_duration": 10.0,
        "SR": "720"
    },
    "status_code": 200,
    "code": "",
    "message": ""
}
```

## **使用限制**

-   **数据时效**：任务task\_id和 视频url均只保留 24 小时，过期后将无法查询或下载。
    
-   **内容审核**：输入的内容（如prompt、图像）、输出视频均会经过内容安全审核，含违规内容将返回 “IPInfringementSuspect”或“DataInspectionFailed”错误，详见参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。
    

## **错误码**

如果模型调用失败并返回报错信息，请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。

## **常见问题**

#### **Q：如何生成特定宽高比（如3:4）的视频？**

**A：** 输出视频的宽高比由**输入首帧图像（img\_url）**决定，但**无法保证精确比例**（如严格3:4），会存在一定偏差。

-   **为什么会有偏差？**
    
    模型会以输入图像的比例为基准，结合设置的分辨率档位（resolution）总像素，自动计算出最接近的合法分辨率。由于要求视频的长和宽必须是 16 的倍数，模型会对最终分辨率做微调，因此无法保证输出比例严格等于 3:4，但会非常接近。
    
    -   例如：输入图像750×1000（宽高比 3:4 = 0.75），并设置 resolution = "720P"（目标总像素约 92 万），实际输出816×1104（宽高比 ≈ 0.739，总像素约90万）。
        
-   **实践建议**：
    
    -   **输入控制**：尽量使用与目标比例一致的图片作为首帧输入。
        
    -   **后期处理**：如果您对比例有严格要求，建议在视频生成后，使用编辑工具进行简单的裁剪或黑边填充。
        

#### **Q：如何获取视频存储的访问域名白名单？**

A： 模型生成的视频存储于阿里云OSS，API将返回一个临时的公网URL。**若需要对该下载地址进行防火墙白名单配置**，请注意：由于底层存储会根据业务情况进行动态变更，为避免过期信息影响访问，文档不提供固定的OSS域名白名单。如有安全管控需求，请联系客户经理获取最新OSS域名列表。
