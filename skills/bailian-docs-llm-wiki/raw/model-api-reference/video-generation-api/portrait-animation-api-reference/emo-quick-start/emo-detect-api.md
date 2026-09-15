# EMO图像检测API参考

EMO-detect模型，用于确认输入的人物肖像图片是否符合EMO视频生成模型的输入规范。本文档介绍了该模型提供的图像检测能力的API调用方法。

**重要**本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。

## 模型概览

**模型名**

**模型简介**

emo-detect-v1

emo-detect-v1是一个特定的图像检测模型，用于检测输入的图片是否满足emo模型所需的人物肖像图片规范。

## HTTP调用接口

### 功能描述

该模型用于检测输入的图片是否满足“[EMO 视频生成](raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start/emo-api.md)”所需的人物肖像图片规范。

### 前提条件

-   已开通服务并获得API-KEY：[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)。

### 输入限制

-   图像格式：格式为jpg，jpeg，png，bmp，webp。
-   图像分辨率：图像最小边长≥400像素，最大边长≤7000像素。
-   上传图片仅支持HTTP链接方式，不支持本地链接方式。

### 请求接口

```
POST https://dashscope.aliyuncs.com/api/v1/services/aigc/image2video/face-detect
```

#### 入参描述

**字段**

**类型**

**传参方式**

**必选**

**描述**

**示例值**

Content-Type

String

Header

是

请求类型：application/json。

application/json

Authorization

String

Header

是

API-Key，例如：Bearer d1\*\*2a。

Bearer d1\*\*2a

model

String

Body

是

指明需要调用的模型，此处用emo-detect-v1。

若调用独立部署模型，则改为填入**部署成功的模型名称**

emo-detect-v1

input.image\_url

String

Body

是

-   需要检测的图像URL。
    
-   图像最小边长≥400像素，最大边长≤7000像素。
    
-   格式支持：jpg、jpeg、png、bmp、webp。
    

上传文件支持HTTP或HTTPS链接方式，不支持本地链接方式。您也可在此[获取临时公网URL](raw/model-api-reference/more-about-models/get-temporary-file-url.md)。

http://a/a.jpg

parameters.ratio

String

Body

是

希望检测确认的画幅，可选 "1:1"或"3:4"。默认值为"1:1"。

-   1:1适用于头像图片。
    
-   3:4适用于半身像图片。
    

"ratio": "1:1"

#### 出参描述

**字段**

**类型**

**描述**

**示例值**

output.check\_pass

Bool

客户提交的图像列表对应的检查结果。true表示检测通过，false表示检测不通过。

true

output.face\_bbox

Array

-   算法检测到的人脸区域bbox，可将该值作为EMO视频生成API的入参。
    
-   人脸区域坐标（x1，y1，x2，y2），对应左上和右下两个点的坐标。
    

\[10,20,30,40\]

output.ext\_bbox

Array

-   算法预测的动态区域bbox，可将该值作为EMO视频生成API的入参。该区域的宽高比与入参画幅一致。
    
-   动态区域坐标（x1，y1，x2，y2），对应左上和右下两个点的坐标。
    

\[10,20,30,40\]

usage.image\_count

Integer

检测的图像张数。用于计费。

1

code

String

请求失败时返回的错误码，详情请参见[状态码说明](https://help.aliyun.com/zh/model-studio/emo-api#933856b630hez)。

InvalidApiKey

message

String

请求失败时返回的详细错误信息，详情请参见[状态码说明](https://help.aliyun.com/zh/model-studio/emo-api#933856b630hez)。

No API-key provided.

request\_id

String

本次请求的系统唯一码。

7574ee8f-38a3-4b1e-9280-xxxxx

#### 请求示例

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2video/face-detect' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data-raw '{
  "model": "emo-detect-v1",
  "input": {
      "image_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251225/onmomb/emo.png"
  },
  "parameters": {
      "ratio": "1:1"
  }
}'
```

#### 响应示例（请求成功）

图像检测通过

```
{
    "output":{
        "check_pass": true,
        "face_bbox":[302,286,610,593], #人脸bbox
        "ext_bbox":[71,9,840,778] #动态区域bbox
    },
    "usage":{
        "image_count":1
    },
    "request_id":"c56f62df-724e-9c19-96bd-xxxxxx"
}
```

图像检测不通过

```
{
    "output":{
      "check_pass": false,
      "code": "",
      "message": ""
    },
    "usage":{
        "image_count":1
    },
    "request_id":"c56f62df-724e-9c19-96bd-xxxxxx"
}
```

#### 响应示例（请求失败）

```
{
    "code": "InvalidApiKey",
    "message": "No API-key provided.",
    "request_id": "7438d53d-6eb8-4596-8835-xxxxxx"
}
```

## 状态码说明

大模型服务平台通用状态码请查阅：[错误码](raw/model-api-reference/preparations/error-code.md)。
