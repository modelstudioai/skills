# 万相3.0-视频生成API参考

万相3.0是全能参考视频生成模型（All-in-One），统一支持 文生视频 、 图生视频 （首帧/首尾帧）和 参考生视频 等多种用法。最长可生成30秒视频，输出帧率为30fps。

## 适用范围

为确保调用成功，请务必保证**模型、Endpoint URL 和 API Key 均属于同一地域**。跨地域调用将会失败。

-   [**选择模型**](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market)：前往模型广场选择模型，并确认其所属地域。
-   **选择 URL**：选择对应的地域 Endpoint URL。
-   **配置 API Key**：选择地域并[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

**说明**本文的示例代码适用于**北京地域**。

## HTTP调用

由于视频生成任务耗时较长（通常为1-5分钟），API采用异步调用。整个流程包含 **"创建任务 -> 轮询获取"** 两个核心步骤，具体如下：

### 步骤1：创建任务获取任务ID

#### 北京

`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`

#### 新加坡

`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`

#### 日本（东京）

`POST https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`

#### 德国（法兰克福）

`POST https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`

#### 美国（弗吉尼亚）

`POST https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)。

**说明**

-   创建成功后，使用接口返回的 `task_id` 查询结果，task\_id 有效期为 24 小时。**请勿重复创建任务**，轮询获取即可。
-   新手指引请参见[Postman](raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)。

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

模型名称。可选值：

-   `wan3.0-video-prime`：高速版，能力对齐标准版，端到端速度显著提升。
-   `wan3.0-video`：标准版。

**input** `object` **（必选）**

输入的基本信息。`prompt` 和 `media` 必填其一。

属性

**prompt** `string` （条件必选）

文本提示词，用来描述期望生成的视频内容。和 `media` 必填其一。

支持中英文，每个汉字/字母占一个字符，不超过20000个字符，超过部分会自动截断。

在全能参考模式下，prompt中可以用"图1""视频1""音频1"等指代 media 数组中对应顺序的媒体素材。

**media** `array` （条件必选）

媒体素材数组，支持图像、视频、音频、文件和网页作为输入。和 `prompt` 必填其一。

-   数组中每个元素为一个媒体对象，包含 `type` 与 `url` 字段。
    
-   在参考生视频模式下，按照数组顺序定义 `prompt` 中素材引用的顺序。图和视频分别计数，即可同时存在图1、视频1。
    
    -   数组中的第 1 个 `reference_video` 对应 **视频1**，第 2 个对应 **视频2**，以此类推。
    -   数组中的第 1 个 `reference_image` 对应 **图1**，第 2 个对应 **图2**，以此类推。
    -   数组中的第 1 个 `reference_audio` 对应 **音频1**，第 2 个对应 **音频2**，以此类推。

属性

**type** `string` **（必选）**

媒体素材类型。可选值为：

-   `first_frame`：首帧图像。最多1张，严格作为视频第一帧。
-   `last_frame`：尾帧图像。最多1张，严格作为视频最后一帧。
-   `reference_image`：参考图像。最多10张。
-   `reference_video`：参考视频。最多5段，总时长不大于15秒。
-   `reference_audio`：参考音频。最多5段，总时长不大于15秒。
-   `file`：文件。最多1个，不可与 link 同时输入。
-   `link`：网页链接。最多1个，不可与 file 同时输入。

**重要**`reference_xx`/`file`/`link` 类型和 `first_frame`/`last_frame` 类型互斥，不能在同一请求中混用。

**url** `string` **（必选）**

媒体素材URL或Base64 编码数据。

传入图像（type=first\_frame / last\_frame / reference\_image）

图像URL或Base64 编码数据。

图像限制：

-   格式：JPEG、JPG、PNG（不支持透明通道）、BMP、WEBP。
-   分辨率：单边\[240, 8000\]像素。
-   长宽比：不超过8:1。
-   文件大小：不超过20MB。

支持输入的格式：

1.  公网URL：
    
    -   支持HTTP或HTTPS协议。
    -   示例值：[](https://xxx/xxx.png)[https://xxx/xxx.png](https://xxx/xxx.png)。
2.  临时URL：
    
    -   支持OSS协议，必须通过[上传文件获取临时 URL](raw/model-api-reference/more-about-models/get-temporary-file-url.md)。
    -   示例值：oss://dashscope-instant/xxx/xxx.png。
3.  Base64 编码图像后的字符串：
    
    -   数据格式：`data:{MIME_type};base64,{base64_data}`。
    -   示例值：data:image/png;base64,GDU7MtCZzEbTbmRZ......。（编码字符串过长，仅展示片段）
    -   详情请参见[传入图像](https://help.aliyun.com/zh/model-studio/image-to-video-guide#32d9db99f1fk0)。

传入视频（type=reference\_video）

参考视频URL。

视频限制：

-   格式：mp4、mov。
-   时长：单个\[1, 15\]秒，总时长不大于15秒。
-   分辨率：单边\[240, 4096\]像素。
-   长宽比：不超过8:1。
-   单文件大小：不超过100MB。

支持输入的格式：

1.  公网URL：
    
    -   支持HTTP或HTTPS协议。
    -   示例值：[](https://xxx/xxx.mp4)[https://xxx/xxx.mp4](https://xxx/xxx.mp4)。
2.  临时URL：
    
    -   支持OSS协议，必须通过[上传文件获取临时 URL](raw/model-api-reference/more-about-models/get-temporary-file-url.md)。
    -   示例值：oss://dashscope-instant/xxx/xxx.mp4。

传入音频（type=reference\_audio）

参考音频URL。

音频限制：

-   格式：wav、mp3。
-   时长：单个\[1, 15\]秒，总时长不大于15秒。
-   文件大小：不超过15MB。

支持输入的格式：

1.  公网URL：
    
    -   支持HTTP或HTTPS协议。
    -   示例值：[](https://xxx/xxx.mp3)[https://xxx/xxx.mp3](https://xxx/xxx.mp3)。
2.  临时URL：
    
    -   支持OSS协议，必须通过[上传文件获取临时 URL](raw/model-api-reference/more-about-models/get-temporary-file-url.md)。
    -   示例值：oss://dashscope-instant/xxx/xxx.mp3。

传入文件（type=file）

文件URL。

文件限制：

-   格式：docx、doc、xlsx、xls、pptx、ppt、pdf、txt、key、pages、numbers、md。
-   文件大小：不超过100MB。
-   页数限制：不超过50页（对pdf、docx、doc、pptx、ppt、key、pages格式校验）。

支持输入的格式：

1.  公网URL：
    
    -   支持HTTP或HTTPS协议。
    -   示例值：[](https://xxx/xxx.pdf)[https://xxx/xxx.pdf](https://xxx/xxx.pdf)。
2.  临时URL：
    
    -   支持OSS协议，必须通过[上传文件获取临时 URL](raw/model-api-reference/more-about-models/get-temporary-file-url.md)。
    -   示例值：oss://dashscope-instant/xxx/xxx.pdf。

传入网页链接（type=link）

公开网页的URL地址。仅支持解析无需登录的公开网页（如新闻、博客、公众号等）。

支持输入的格式：

1.  公网URL：
    
    -   支持HTTP或HTTPS协议。
    -   示例值：[](https://xxx/article/xxx)[https://xxx/article/xxx](https://xxx/article/xxx)。

**parameters** `object` （可选）

视频处理参数。

属性

**resolution** `string` （可选）

生成视频的分辨率档位。默认值为 `1080P`。可选值：

-   `1080P`
-   `720P`
-   `480P`

**ratio** `string` （可选）

生成视频的宽高比。可选值：

-   `adaptive`（默认值）：自适应长宽比，根据输入媒体比例和意图自动推荐合适的长宽比。
-   `16:9`
-   `4:3`
-   `1:1`
-   `3:4`
-   `9:16`

**duration** `integer` （可选）

生成视频的时长，单位为秒。默认值为5。

-   无视频输入时：取值范围为\[2, 30\]的整数。
-   有视频输入时：输入视频总时长 + 输出视频时长不超过30秒。
-   传 `-1` 时：智能时长模式，模型根据输入的 prompt、内容和富媒体自动推荐合适时长生成。

**audio** `boolean` （可选）

输出视频是否包含音频。

-   `true`：默认值，输出视频包含声音。
-   `false`：输出视频不包含音轨。

开关声音价格相同。

**seed** `integer` （可选）

随机种子，用于复现生成结果。取值范围：\[0, 2147483647\]。

**prompt\_extend** `boolean` （可选）

是否开启prompt智能改写。开启后使用大模型对输入prompt进行智能改写。对于较短的prompt生成效果提升明显，但会增加耗时。

-   `true`：默认值，开启智能改写。
-   `false`：不开启智能改写。

**watermark** `boolean` （可选）

是否添加水印标识。

-   `false`：默认值，不添加水印。
-   `true`：添加水印。

#### 参考文件生视频

通过 `file` 类型传入文件，模型自动理解文件内容生成视频。

```
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "wan3.0-video",
    "input": {
        "prompt": "一支高端智能眼镜产品广告，整体风格极简、未来感、时尚高级，光影克制，画面以黑色、银灰色、冰蓝色为主色调，局部点缀柔和白光与参数UI图形。开场在纯黑背景中，一副智能眼镜从黑暗中缓缓浮现，镜腿边缘掠过精致高光，镜框轮廓在冷冽边缘光下被勾勒出来，镜头超近距离掠过镜片、鼻托、转轴、镜腿与材质细节，展现金属与高性能复合材料的细腻质感，表面处理高级克制，线条轻薄流畅。随后产品在空中缓慢旋转，画面以极简动态图形同步展示核心参数信息。随后镜头快速收拢，所有零件精准回归组装成完整产品，切换到年轻模特佩戴展示，模特五官立体、气质自信，穿着简洁高级的都市时尚服装，在极简空间和城市光影环境中自然转头、抬手、行走、微笑，镜头从正面、侧面、斜后方展示眼镜佩戴状态，突出轻薄贴合、时尚轮廓与日常百搭属性。结尾在纯色背景中，产品悬浮定格，镜头缓慢推进到品牌logo和核心slogan，整体音乐极简电子氛围配合精准鼓点，节奏干净有力，画面质感高级、克制、纯粹，具有强烈品牌记忆点和国际化科技审美。",
        "media": [
            {
                "type": "file",
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260806/ebapmr/glass.pptx"
            }
        ]
    },
    "parameters": {
        "resolution": "480P",
        "ratio": "adaptive",
        "duration": 10,
        "prompt_extend": true
    }
}'
```

#### 参考生视频

通过 `input.media` 传入参考图片、视频、音频、文件或网页链接，模型自动理解意图生成视频。

```
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "wan3.0-video",
    "input": {
        "prompt": "视频1抱着图3，在图4的椅子上弹奏一支舒缓的乡村民谣，并说道："今天的阳光真好。"图1手中拿着图2，路过视频1，把手中的图2放到视频1旁边的桌子上，并说道："真好听，能不能再唱一遍"。",
        "media": [
            {
                "type": "reference_image",
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260408/sjuytr/wan-r2v-object-girl.jpg"
            },
            {
                "type": "reference_video",
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qigswt/wan-r2v-role2.mp4"
            },
            {
                "type": "reference_image",
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/rtjeqf/wan-r2v-object3.png"
            },
            {
                "type": "reference_image",
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qpzxps/wan-r2v-object4.png"
            },
            {
                "type": "reference_image",
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/wfjikw/wan-r2v-backgroud5.png"
            }
        ]
    },
    "parameters": {
        "resolution": "480P",
        "ratio": "adaptive",
        "duration": 5,
        "prompt_extend": true
    }
}'
```

#### 文生视频

仅通过 `prompt` 生成视频，不传入任何媒体文件。

```
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "wan3.0-video",
    "input": {
        "prompt": "一只小猫在月光下的屋顶上奔跑，城市的霓虹灯在远处闪烁，电影级画质，流畅运镜。"
    },
    "parameters": {
        "resolution": "480P",
        "ratio": "adaptive",
        "duration": 5,
        "prompt_extend": true
    }
}'
```

#### 首帧生视频

通过 `first_frame` 严格指定视频首帧图像。

```
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "wan3.0-video",
    "input": {
        "prompt": "一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色。一个由喷漆所画成的少年，正从一面混凝土墙上活过来。他一边用极快的语速演唱一首英文rap，一边摆着一个经典的、充满活力的说唱歌手姿势。场景设定在夜晚一个充满都市感的铁路桥下。灯光来自一盏孤零零的街灯，营造出电影般的氛围，充满高能量和惊人的细节。视频的音频部分完全由rap构成，没有其他对话或杂音。",
        "media": [
            {
                "type": "first_frame",
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/wpimhv/rap.png"
            }
        ]
    },
    "parameters": {
        "resolution": "480P",
        "ratio": "adaptive",
        "duration": 5,
        "prompt_extend": true
    }
}'
```

#### 首尾帧生视频

同时传入 `first_frame` 和 `last_frame`，严格指定视频的首帧和尾帧图像。

```
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "wan3.0-video",
    "input": {
        "prompt": "一个年轻女孩从微笑逐渐变为大笑，镜头缓缓推进，背景光线从冷色调渐变为暖色调。",
        "media": [
            {
                "type": "first_frame",
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/wpimhv/rap.png"
            },
            {
                "type": "last_frame",
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260408/sjuytr/wan-r2v-object-girl.jpg"
            }
        ]
    },
    "parameters": {
        "resolution": "480P",
        "ratio": "adaptive",
        "duration": 5,
        "prompt_extend": true
    }
}'
```

#### 视频编辑

通过 `reference_video` 类型传入待编辑视频，结合 `prompt` 指令编辑视频内容。

```
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "wan3.0-video",
    "input": {
        "prompt": "将整个画面转换为黏土风格",
        "media": [
            {
                "type": "reference_video",
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260402/ldnfdf/wan2.7-videoedit-style-change.mp4"
            }
        ]
    },
    "parameters": {
        "resolution": "720P",
        "prompt_extend": true
    }
}'
```

#### 视频延长

通过 `reference_video` 类型传入原始视频，结合含延长意图关键词的 `prompt` 延长视频内容。需将 `ratio` 设为 `adaptive`。

```
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "wan3.0-video",
    "input": {
        "prompt": "将视频1向后延长，面包师端上刷好的面包，将刷子放到一旁，镜头跟随面包师，去斜后方的烤炉进行烤制",
        "media": [
            {
                "type": "reference_video",
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260402/ldnfdf/wan2.7-videoedit-style-change.mp4"
            }
        ]
    },
    "parameters": {
        "resolution": "720P",
        "ratio": "adaptive",
        "prompt_extend": true
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

#### 北京

`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`

#### 新加坡

`GET https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/tasks/{task_id}`

#### 日本（东京）

`GET https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/api/v1/tasks/{task_id}`

#### 德国（法兰克福）

`GET https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/api/v1/tasks/{task_id}`

#### 美国（弗吉尼亚）

`GET https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v1/tasks/{task_id}`

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

将`{task_id}`完整替换为上一步接口返回的`task_id`的值。`task_id`查询有效期为24小时，并请将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)。

```
curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id} \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

#### 响应参数

**output** `object`

任务输出信息。

属性

**task\_id** `string`**（必选）**

任务ID。

**task\_status** `string`

任务状态。

枚举值

-   PENDING：任务排队中
-   RUNNING：任务处理中
-   SUCCEEDED：任务执行成功
-   FAILED：任务执行失败
-   CANCELED：任务已取消
-   UNKNOWN：任务不存在或状态未知

**submit\_time** `string`

任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。

**scheduled\_time** `string`

任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。

**end\_time** `string`

任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。

**orig\_prompt** `string`

原始输入的提示词。

**video\_url** `string`

生成视频的URL地址。任务成功时返回。

**code**`string`

请求失败的错误码。请求成功时不会返回此参数，详情请参见[错误码](raw/model-api-reference/preparations/error-code.md)。

**message**`string`

请求失败的详细信息。请求成功时不会返回此参数，详情请参见[错误码](raw/model-api-reference/preparations/error-code.md)。

**usage** `object`

输出信息统计。只对成功的结果计数。

属性

**video\_count** `integer`

生成视频的数量。固定为1。

**duration** `float`

生成视频的时长，单位为秒。

**input\_video\_duration** `float`

输入视频的时长，单位为秒。无视频输入时为0.0。

**output\_video\_duration** `float`

输出视频的时长，单位为秒。

**fps** `integer`

生成视频的帧率。默认值为30。

**SR** `integer`

生成视频的分辨率。示例值：720。

**ratio** `string`

生成视频的宽高比。示例值：16:9。

**request\_id**`string`

请求唯一标识。可用于请求明细溯源和问题排查。

#### 任务执行成功

视频URL仅保留24小时，超时后会被自动清除，请及时保存生成的视频。

```
{
    "request_id": "78c9b768-0285-996c-b682-xxxxxx",
    "output": {
        "task_id": "17ed7e50-00cf-4509-aea1-xxxxxx",
        "task_status": "SUCCEEDED",
        "submit_time": "2026-08-06 10:01:35.452",
        "scheduled_time": "2026-08-06 10:01:35.507",
        "end_time": "2026-08-06 10:13:33.838",
        "orig_prompt": "A golden retriever running on a sunny beach, waves crashing in the background, cinematic lighting",
        "video_url": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx/video.mp4"
    },
    "usage": {
        "video_count": 1,
        "duration": 5.0,
        "input_video_duration": 0.0,
        "output_video_duration": 5.0,
        "fps": 30,
        "SR": 720,
        "ratio": "16:9"
    }
}
```

#### 任务执行失败

若任务执行失败，task\_status将置为 FAILED，并提供错误码和信息。请参见[错误码](raw/model-api-reference/preparations/error-code.md)进行解决。

```
{
    "request_id": "e5e57877-c0fc-47ed-8fad-xxxxxx",
    "output": {
        "task_id": "eff1443c-ccab-4676-aad3-xxxxxx",
        "task_status": "FAILED",
        "code": "InvalidParameter",
        "message": "The two modes are mutually exclusive. Do not pass reference_xx and first_frame/last_frame at the same time."
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
