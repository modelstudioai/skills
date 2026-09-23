# AnimateAnyone 图像检测API参考

AnimateAnyone图像检测模型，用于确认输入的人物图像是否符合AnimateAnyone视频生成模型的要求。本文档介绍了该模型提供的图像检测能力的API调用方法。

**重要**本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。

## 模型概览

**模型名**

**模型简介**

animate-anyone-detect-gen2

animate-anyone-detect-gen2是一个图像检测模型，专门用于检测输入的图片是否满足animate-anyone-gen2模型所需的人物图像规范。

## 效果示例

#### 人物图像检测通过示例

**人物全身照**

**人物半身照**

-   单人从头到脚完整露出、身体无遮挡
    
-   面朝镜头，无大角度侧身或镜头俯仰
    

![AA\_正面建议\_全身@4x](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0680383371/p883941.png)

-   单人腰部以上完整露出、身体无遮挡
    
-   面朝镜头，无大角度侧身或镜头俯仰
    

![AA\_正面建议\_半身@4x](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0680383371/p883942.png)

#### 人物图像检测不通过示例

**非正面照**

**（侧身侧脸）**

**光线暗淡**

**（人物不清晰）**

**人物遮挡**

**（服饰遮手、手持物品等）**

**复杂背景**

**多人照片**

![AA\_错误\_侧身侧脸@4x](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0680383371/p883947.png)

![AA\_错误\_光线暗淡@4x](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0680383371/p883948.png)

![AA\_错误\_手拿物品@4x](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0680383371/p883949.png)

![AA\_错误\_复杂背景@4x](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0680383371/p883950.png)

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4017834571/p992598.png)

## HTTP调用接口

### 功能描述

该模型用于检测输入的图片是否满足“[AnimateAnyone 视频生成API](raw/_short/animateanyone-video-generation-api-5a2827f4de69f8c0.md)”所需的人物图片规范。

### 前提条件

-   已开通服务并获得API-KEY：[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)。

### 请求接口

```
POST https://dashscope.aliyuncs.com/api/v1/services/aigc/image2video/aa-detect
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

请求类型：application/json

application/json

Authorization

String

Header

是

API-Key，例如：Bearer d1\*\*2a

Bearer d1\*\*2a

model

String

Body

是

指明需要调用的模型

animate-anyone-detect-gen2

input.image\_url

String

Body

是

需要检查的图像 URL

URL 需为公网可访问的地址，并支持 HTTP 或 HTTPS 协议。您也可在此[获取临时公网URL](raw/model-api-reference/more-about-models/get-temporary-file-url.md)。

"image\_url": "[http://a/a.jpg](http://a/a.jpg)"

#### 出参描述

**字段**

**类型**

**描述**

**示例值**

output.check\_pass

Bool

提交的图像列表对应的检查结果

true

output.bodystyle

String

半身或全身：half 表示半身图，full 代表全身图

half

output.reason

String

提交的图像列表对应的检查结果原因，仅当"check\_pass": false返回此参数

The input image has no human body...

usage.image\_count

Integer

检测的图片数量

1

request\_id

String

本次请求的系统唯一码

7574ee8f-38a3-4b1e-9280-11c33ab46e51

#### 请求示例

```
curl --location --request POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2video/aa-detect' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data-raw '{
  "model": "animate-anyone-detect-gen2",
  "input": {
      "image_url":"https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251224/pkswoc/p883941.png"
  }
}'
```

#### 响应示例（请求成功）

图像检测通过

```
{
    "output": {
        "bodystyle": "full",
        "check_pass": true
    },
    "usage": {
        "image_count": 1
    },
    "request_id": "76df937d-6eb6-40aa-9ccf-xxxxxx"
}
```

图像检测不通过

```
{
    "output":{
        "check_pass": false,
        "reason": "The input image has no human body. Please upload other image with single person.",
        "bodystyle": ""
    },
    "usage":{
        "image_count": 1
    },
    "request_id": "c56f62df-724e-9c19-96bd-xxxxxx"
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
