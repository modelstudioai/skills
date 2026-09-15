# 表情包Emoji 图像检测API参考

表情包emoji-detect-v1是一个图像合规性检测模型，用于判断输入图像中的人物形象是否满足“表情包Emoji模型”的要求。检测通过后，该模型输出人脸区域及扩展后的动态表情区域坐标，供后续视频生成使用。

**重要**本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。

## 模型概览

**模型名称**

**模型简介**

emoji-detect-v1

检测输入的图像是否符合[Emoji 视频生成](raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start/emoji-api.md)所需要的图像规范。  
检测通过后，输出人脸区域（face\_bbox）和扩展后的动态表情区域（ext\_bbox\_face）坐标，供视频生成使用。

## 输入图像要求

**合规图像示例（检测通过）**

**图像要求**

**合规图像示例**

-   **单人正面肖像**
    
-   **面部无遮挡**（如手、头发、饰品等）
    
-   **表情自然**，无夸张表情
    
-   **头部姿态端正**，无大幅度倾斜
    

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1667357371/p906311.png)

**不合规图像示例（检测失败）**

**脸部区域附近露出手部**

**存在面部遮挡**

**存在夸张表情**

**头部倾斜角度过大**

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1667357371/p906315.png)

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1667357371/p906313.png)

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1667357371/p906314.png)

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1667357371/p906312.png)

## 前提条件

您需要已[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。请将示例代码中的 `DASHSCOPE_API_HOST` 替换为获取的 API Host。

## HTTP调用

`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/image2video/face-detect`

#### 请求参数

##### 请求头（Headers）

**Content-Type**`string`**（必选）**

请求内容类型。此参数必须设置为`application/json`。

**Authorization**`string`**（必选）**

请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。

##### 请求体（Request Body）

**model** `string` **（必选）**

模型名称。固定为`emoji-detect-v1`。

**input** `object` **（必选）**

输入的基本信息，如待检测图像。

属性

**image\_url** `string` **（必选）**

待检测图像的公网 URL。支持 HTTP 或 HTTPS 协议。本地文件可通过[上传文件获取临时URL](raw/model-api-reference/more-about-models/get-temporary-file-url.md)。

图像限制：

-   图像格式：JPEG、JPG、PNG、BMP、WEBP。
-   图像分辨率：图像的宽度和高度范围均在\[400, 7000\]像素之间。
-   文件大小：不超过10MB。

示例值：[](https://help-static-aliyun-doc.aliyuncs.com/xxx.png)[https://help-static-aliyun-doc.aliyuncs.com/xxx.png](https://help-static-aliyun-doc.aliyuncs.com/xxx.png)。

**parameters** `object` **（必选）**

图像处理参数。

属性

**ratio** `string` **（必选）**

待检测区域的长宽比。对于 Emoji 视频生成，此值固定为 `1:1`。

示例值：1:1。

#### 人像合规检测

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2video/face-detect' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "emoji-detect-v1",
    "input": {
        "image_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250912/uopnly/emoji-%E5%9B%BE%E5%83%8F%E6%A3%80%E6%B5%8B.png"
    },
    "parameters": {
        "ratio":"1:1"
    }
  }'
```

#### 响应参数

**output** `object`

任务输出信息。

属性

**bbox\_face** `array of integer`

检测到的人脸区域坐标，格式为 \[x1, y1, x2, y2\]，单位为像素，对应左上和右下两个点的坐标。仅在检测通过时返回。

此值应作为[Emoji 视频生成](raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start/emoji-api.md)接口 input.face\_bbox 参数的值。

示例值：\[212,194,460,441\]。

**ext\_bbox\_face** `array of integer`

扩展后的动态表情区域坐标，格式为 \[x1, y1, x2, y2\]，单位为像素，对应左上和右下两个点的坐标。仅在检测通过时返回。

此值应作为[Emoji 视频生成](raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start/emoji-api.md)接口 input.ext\_bbox 参数的值。

示例值：\[63,30,609,575\]。

**code**`string`

错误码。仅在检测不通过时返回，详情请参见[错误码](raw/model-api-reference/preparations/error-code.md)。

**message**`string`

错误信息。仅在检测不通过时返回，详情请参见[错误码](raw/model-api-reference/preparations/error-code.md)。

**request\_id**`string`

请求唯一标识。可用于请求明细溯源和问题排查。

**usage** `object`

输出信息统计。

属性

**image\_count** `integer`

本次请求检测图像数量，固定为 1 张，用于计费。  
无论检测是否通过，只要请求成功就计费；请求失败不计费。计费信息详见[模型价格](raw/model-user-guide/get-started-with-models/models.md)。

**说明**当图像因不合规而导致检测不通过时，本次API调用仍会正常计费，因为模型已经执行了完整的检测流程。

**message**`string`

请求失败的详细信息。请求成功时不会返回此参数，详情请参见[错误码](raw/model-api-reference/preparations/error-code.md)。

**request\_id**`string`

请求唯一标识。可用于请求明细溯源和问题排查。

#### 检测通过

请求成功且检测通过，将产生计费，接口会在响应中返回usage.image\_count。

请保存返回的 `bbox_face` 和 `ext_bbox_face`。这是下一步[Emoji 视频生成](raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start/emoji-api.md)接口中`input.face_bbox`和`input.ext_bbox`参数的值。

```
{
    "output": {
        "bbox_face": [212,194,460,441],
        "ext_bbox_face": [63,30,609,575]
    },
    "usage": {
        "image_count": 1
    },
    "request_id": "78becbc4-f7f7-41ea-9e38-xxxxxx"
}
```

#### 检测不通过

请求成功但人像检测未通过，将产生计费，接口会在响应中返回usage.image\_count。请参见[错误码](raw/model-api-reference/preparations/error-code.md)排查问题。

```
{
    "output": {
        "code": "InvalidFile.FacePose",
        "message": "The pose of the detected face is invalid, please upload other image with the expected oriention."
    },
    "usage": {
        "image_count": 1
    },
    "request_id": "ed0d0d8f-e55a-4144-b855-xxxxxx"
}
```

#### 请求失败

接口请求失败，不计费。此时接口不返回usage.image\_count。请参见[错误码](raw/model-api-reference/preparations/error-code.md)进行解决。

```
{
    "request_id": "5e1fefbd-fa7a-4e59-82a0-xxxxxx",
    "code": "InvalidParameter",
    "message": "Required body invalid, please check the request body format."
}
```

## 计费与限流

-   模型免费额度和计费单价请参见[模型价格](raw/model-user-guide/get-started-with-models/models.md)。
-   模型限流请参见[限流](raw/model-user-guide/get-started-with-models/rate-limit.md)。

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](raw/model-api-reference/preparations/error-code.md)进行解决。
