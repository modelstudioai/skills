# LivePortrait图像检测API参考

LivePortrait-detect模型，用于确认输入的人物肖像图片是否符合LivePortrait模型的输入规范。本文档介绍了该模型提供的图像检测能力的API调用方法。

**重要**本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。

## 模型概览

**模型名**

**模型简介**

liveportrait-detect

liveportrait-detect是一个特定的图像检测模型，用于检测输入的图片是否满足liveportrait模型所需的人物肖像图片规范。

## HTTP调用接口

### 功能描述

该模型用于检测输入的图片是否满足“[LivePortrait 视频生成](raw/_short/liveportrait-api-aed61e9b5a74b8a5.md)”所需的人物肖像图片规范。

### 前提条件

-   已开通阿里云百炼服务并获得API-KEY：[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)。

### 输入限制

-   图像格式为jpeg、jpg、png、bmp、webp。
-   图像文件<10M，宽高比≤2，最大边长≤4096像素。
-   上传图片仅支持HTTP链接方式，不支持本地链接方式。

### 作业提交接口调用

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

指明需要调用的模型，此处用liveportrait-detect。

liveportrait-detect

input.image\_url

String

Body

是

需要检查的图像 URL。

-   图像文件<10M，宽高比≤2，最大边长≤4096。
    
-   格式支持：jpeg、jpg、png、bmp、webp。
    

上传文件支持HTTP或HTTPS链接方式，不支持本地链接方式。您也可在此[获取临时公网URL](raw/model-api-reference/more-about-models/get-temporary-file-url.md)。

"image\_url": "[http://a/a.jpg](http://a/a.jpg)"

#### 出参描述

**字段**

**类型**

**描述**

**示例值**

output.pass

Bool

所提交图像对应的检查结果

"pass":true/false

output.message

String

所提交图像对应的检查结果信息

"message":No human face detected.

request\_id

String

本次请求的系统唯一码

7574ee8f-38a3-4b1e-9280-11c33ab46e51

#### 检查不通过原因

**output.message**

**原因说明**

No human face detected

未检测到人脸（包含人脸过小、侧脸、遮挡等情况）

##### 请求示例

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2video/face-detect' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data-raw '{
  "model": "liveportrait-detect",
  "input": {
      "image_url":"https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250911/ynhjrg/p874909.png"
  }
}'
```

##### 响应示例（通过）

```
{
    "output": {
        "pass": true,
        "message": ""
    },
    "usage": {
        "image_count": 1
    },
    "request_id": "a92e2ffd-9263-44ba-92c5-xxxxxx"
}
```

##### 响应示例（不通过）

```
{
    "output": {
        "pass": false,
        "message": "No human face detected."
    },
    "usage": {
        "image_count": 1
    },
    "request_id": "c56f62df-724e-9c19-96bd-xxxxxx"
}
```

##### 响应示例（错误）

```
{
    "code": "InvalidParameter.UnsupportedFileFormat",
    "message": "Input files format not supported.",
    "request_id": "788b30fe-05f6-999f-a0b1-xxxxxx"
}
```

## 状态码说明

大模型服务平台通用状态码请查阅：[错误码](raw/model-api-reference/preparations/error-code.md)。
