# 虚拟模特API参考

本文介绍万相-虚拟模特模型的输入输出参数。该模型可以对上传的真人或者人台实拍商品展示图进行智能生成，将其中的模特和背景替换为心仪的内容。在保持人物姿态不变的情况下，使用虚拟模特对商品进行更加精美、多样的展示。同时支持各种与模特产生互动的商品，如手持小商品、服装、鞋靴、配饰等。

**相关指南**：[虚拟模特生成](https://help.aliyun.com/zh/model-studio/virtual-model-generation)

**重要**

-   本文档仅适用于“中国内地（北京）”地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)。
    
-   wanx-virtualmodel、virtualmodel-v2 模型当前仅提供**免费体验**，免费额度用完后不可调用且不支持付费，推荐参考[图像编辑-千问](https://help.aliyun.com/zh/model-studio/qwen-image-edit-guide)或[图像编辑-万相2.1](https://help.aliyun.com/zh/model-studio/wanx-image-edit)获取替代方案。
    

## 模型概览

万相-虚拟模特可以对上传的真人实拍商品展示图进行智能生成，将其中的模特和背景替换为心仪的内容，在保持人物姿态不变的情况下，使用虚拟模特对商品进行更加精美、多样的展示。支持各种与模特产生互动的商品，如手持小商品、服装、鞋靴、配饰等。

**模型版本**

**模型名称**

**模型简介**

虚拟模特

（V1版本）

wanx-virtualmodel

-   支持真人实拍图上传
    

-   生成的图片短边：512像素或1024像素
    

虚拟模特V2

（V2版本）

virtualmodel-v2

-   支持真人、人台实拍图上传
    
-   生成的图片短边为：1024像素或2048像素
    
-   支持改变分辨率，生成图片长宽比可选择：比例不变、2:1、16:9、4:3、1:1、3:4、 9:16、1:2。
    
-   支持背景参考图权重自由控制
    
-   文本引导效果更准确
    

**模型名称**

**计费单价**

**限流（主账号与RAM子账号共用）**

**免费额度**[（查看）](https://help.aliyun.com/zh/model-studio/new-free-quota)

**任务下发接口RPS限制**

**同时处理中任务数量**

wanx-virtualmodel

目前仅供免费体验。

> 免费额度用完后不可调用，推荐参考[图像编辑-千问](https://help.aliyun.com/zh/model-studio/qwen-image-edit-guide)或[图像编辑-万相2.1](https://help.aliyun.com/zh/model-studio/wanx-image-edit)获取替代方案。

2

1

500张

virtualmodel-v2

## 前提条件

您需要已[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

## HTTP调用

为了减少等待时间并且避免请求超时，服务采用异步方式提供。您需要发起两个请求：

-   **创建任务**：首先发送一个请求创建文生图任务，该请求会返回任务ID。
    
-   **根据任务ID查询结果**：使用上一步获得的任务ID，查询模型生成的结果。
    

### **步骤1：创建任务获取任务ID**

`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/virtualmodel/generation/`

> 注意：若无特殊说明，下面的参数支持在虚拟模特模型V1版本和V2版本中使用。

#### **请求头（Headers）**

## 虚拟模特V1

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/virtualmodel/generation' \
--header 'X-DashScope-Async: enable' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
  "model": "wanx-virtualmodel",
  "input": {
    "base_image_url": "https://huarong123.oss-cn-hangzhou.aliyuncs.com/image/%E7%9C%9F%E4%BA%BA%E6%A8%A1%E7%89%B9%E5%AE%9E%E6%8B%8D-%E5%A5%B3%20%281%29.jpeg",
    "mask_image_url": "https://huarong123.oss-cn-hangzhou.aliyuncs.com/image/image.jpg",
    "prompt": "一名年轻女子，身穿白色短裤，极简风格调色板，长镜头，双色效果（暗银色和浅粉色）",
    "face_prompt": "年轻女子，面容姣好，最高品质"
  },
  "parameters": {
    "short_side_size": "512",
    "n": 1
  }
}'
```

## 虚拟模特V2

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/virtualmodel/generation' \
--header 'X-DashScope-Async: enable' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
  "model": "virtualmodel-v2",
  "input": {
    "base_image_url": "https://huarong123.oss-cn-hangzhou.aliyuncs.com/image/%E7%9C%9F%E4%BA%BA%E6%A8%A1%E7%89%B9%E5%AE%9E%E6%8B%8D-%E5%A5%B3%20%281%29.jpeg",
    "mask_image_url": "https://huarong123.oss-cn-hangzhou.aliyuncs.com/image/image.jpg",
    "background_image_url": "https://huarong123.oss-cn-hangzhou.aliyuncs.com/image/%E8%99%9A%E6%8B%9F%E6%A8%A1%E7%89%B9%E7%94%9F%E6%88%90%E8%83%8C%E6%99%AF%E5%9B%BE.png",
    "prompt": "a beautiful chinese woman stands in front of a plain white background",
    "face_prompt": "a beautiful chinese woman, good face, best face, best quality"
  },
  "parameters": {
      "short_side_size": "1024",
      "n": 1
  }
}'
```

**Authorization** _string_ **必选**

推荐您使用阿里云百炼API-Key，也可填DashScope API-Key。例如：Bearer d1xxx2a。

**X-DashScope-Async** _string_ **必选**

是否使用异步调用。HTTP只支持异步调用，设置为`enable`。

**Content-Type** _string_ **必选**

请求内容类型。固定为`application/json`。

#### **请求体（Request Body）**

**model** _string_ **必选**

调用模型。

**input** _object_ **必选**

输入图像的基本信息，比如图像URL地址。

**属性**

**base\_image\_url** _string_ **必选**

原始真人展示图像URL地址。

URL 需为公网可访问的地址，并支持 HTTP 或 HTTPS 协议。您也可在此[获取临时公网URL](https://help.aliyun.com/zh/model-studio/get-temporary-file-url)。

图像限制：

-   图像格式：JPEG、JPG、PNG、WEBP。
    
-   图像分辨率：不低于256×256像素且不超过4096×4096像素，人脸占比不低于128×128像素。
    
-   图修比例：长宽比大于1:2且小于2:1。
    
-   图像大小：不超过5MB。
    
-   URL地址中不能包含中文字符。
    

**真人图像示例**

**mask\_image\_url** _string_ **必选**

对应原图的期望保留区域mask图URL，图片为（0,255）的黑白图，其中白色表示商品主体区域。

URL 需为公网可访问的地址，并支持 HTTP 或 HTTPS 协议。您也可在此[获取临时公网URL](https://help.aliyun.com/zh/model-studio/get-temporary-file-url)。

图片限制：

-   图像格式：JPEG、JPG、PNG、WEBP。
    
-   图像分辨率：与base\_image\_url参数对应的图像保持一致。
    
-   图修比例：长宽比大于1:2且小于2:1。
    
-   图像大小：不超过5MB。
    
-   URL地址中不能包含中文字符。
    

**mask图像示例**

**predefined\_face\_id** _string 可选_

预设人物ID。**仅在V1版本使用。**

**枚举示例**

-   girl1
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0489386271/p850530.png)

-   girl2
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0489386271/p850531.png)

-   girl3
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0489386271/p850532.png)

-   boy1
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0489386271/p850533.png)

-   boy2
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0489386271/p850534.png)

-   boy3
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0489386271/p850535.png)

**face\_image\_url** _string 可选_

期望替换的人物图像URL地址。

URL 需为公网可访问的地址，并支持 HTTP 或 HTTPS 协议。您也可在此[获取临时公网URL](https://help.aliyun.com/zh/model-studio/get-temporary-file-url)。

图片限制：

-   图像格式：JPEG、JPG、PNG、WEBP。
    
-   图像分辨率：长边像素不大于2048，人脸区域大于128×128像素。
    
-   图像大小：建议不超过5MB。
    

优先级低于predefined\_face\_id参数。

**prompt** _string_ **必选**

针对生成图像背景环境、模特的全身形象描述。

支持中英文，小于100字符。

示例：一名年轻女子，身穿白色短裤，极简风格调色板，长镜头，双色效果，暗银色和浅粉色。

**face\_prompt** _string_ **必选**

生成人像面部描述，支持中英文，小于100字符。

示例：一名年轻女子，面容娇好，最好的品质。

**background\_image\_url** _string 可选_

背景环境参考图像URL地址。

URL 需为公网可访问的地址，并支持 HTTP 或 HTTPS 协议。您也可在此[获取临时公网URL](https://help.aliyun.com/zh/model-studio/get-temporary-file-url)。

图片限制：

-   图像格式：JPEG、JPG、PNG、WEBP。
    
-   图像分辨率：图像长边像素不大于4096。
    
-   图像比例：长宽比小于等于2。
    
-   图像大小：不超过5MB。
    

**bgstyle\_scale** _float 可选_

背景参考图像权重控制。**仅在V2版本使用。**

取值范围：\[0.0, 1.0\]，默认0.7。

数值越大表示参考程度越大。

**realPerson** _bool 可选_

输入图片是否是真人。**仅在V2版本使用。**

-   true：默认值，表示输入图像是真人。
    
-   false：表示输入图像是人台或者非真人。
    

**style** _string 可选_

生成图片风格。**仅在V2版本使用。**

可选参数\["","portrait"\]，默认是portrait，

说明：portrait模式会增加一些景深，突出人像的效果_。_

**seed** _integer 可选_

控制生成seed。**仅在V2版本使用。**

取值范围：\[-1,10000000\]。默认值为-1, 表示系统随机内置seed.

> seed表示随机种子值，-1表示系统内部随机一个值；0至10000000则是由用户自行决定所用的随机种子值，同样的seed值会生成相同的结果。

**aspect\_ratio** _String 可选_

生成图片长宽比例。**仅在V2版本使用。**

**枚举值**

可选的比例有：

-   比例不变，默认值
    
-   2:1
    
-   16:9
    
-   4:3
    
-   1:1
    
-   3:4
    
-   9:16
    
-   1:2
    

**parameters** _object_ 可选

**属性**

**n** _Integer 可选_

生成图像的数量，支持 1~4 张，默认值 1。

**short\_side\_size** _string_ **必选**

指定生成的图像短边大小，单位：像素。生成图片和输入原图会保持相同的长宽比。

V1版本可选值：512和1024。

V2版本可选值：1024和2048

#### **响应**

## 成功响应

```
{
    "output": {
        "task_status": "PENDING",
        "task_id": "0385dc79-5ff8-4d82-bcb6-xxxxxx"
    },
    "request_id": "4909100c-7b5a-9f92-bfe5-28c7cece6b47"
}
```

## 异常响应

```
{
    "code":"InvalidApiKey",
    "message":"Invalid API-key provided.",
    "request_id":"fb53c4ec-1c12-4fc4-a580-cdb7c3261fc1"
}
```

**output** _object_

任务输出信息。

**属性**

**task\_id** _string_

任务id。

**task\_status** _string_

任务状态。

-   PENDING：排队中
    
-   RUNNING：处理中
    
-   SUSPENDED：挂起
    
-   SUCCEEDED：执行成功
    
-   FAILED：执行失败
    
-   UNKNOWN：任务不存在或状态未知
    

**code** _string_

接口错误码。接口成功请求不会返回该参数。

**message** _string_

接口错误信息。接口成功请求不会返回该参数。

**request\_id** _string_

请求唯一标识。可用于请求明细溯源和问题排查。

### **步骤2：根据任务ID查询结果**

`GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`

#### **请求头（Headers）**

## 获取任务结果

```
curl --location --request GET 'https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

**Authorization** _string_ **必选**

推荐使用阿里云百炼API-Key，也可填DashScope API-Key。例如：Bearer d1xxx2a。

#### **URL路径参数（Path parameters）**

**task\_id** _string_ **必选**

任务id。

#### **响应**

## 任务执行成功

任务数据（如任务状态、图像URL等）仅保留24小时，超时后会被自动清除。请您务必及时保存生成的图像。

```
{
    "request_id": "f24149fe-4722-9763-xxxxxx",
    "output": {
        "task_id": "9d62befa-0139-4e4d-xxxxxx",
        "task_status": "SUCCEEDED",
        "submit_time": "2025-04-24 10:51:35.004",
        "scheduled_time": "2025-04-24 10:51:35.033",
        "end_time": "2025-04-24 10:51:59.424",
        "results": [
            {
                "url": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/test_1.png"
            },
            {
                "url": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/test_2.png"
            }
        ],
        "task_metrics": {
            "TOTAL": 2,
            "SUCCEEDED": 2,
            "FAILED": 0
        }
    },
    "usage": {
        "image_count": 2
    }
}
```

## 任务执行失败

```
{
  "request_id": "f24149fe-4722-9763-xxxxxx",
  "output": {
    "task_id": "9d62befa-0139-4e4d-xxxxxx",
    "task_status": "FAILED",
    "submit_time": "2024-05-16 13:50:xx.xxx",
    "scheduled_time": "2024-05-16 13:50:xx.xxx",
    "end_time": "2024-05-16 13:50:xx.xxx",
    "code": "InvalidImageResolution",
    "message": "The input image resolution is too large or small"
  },
  "usage": {
    "image_num": 0
  }
}
```

**output** _object_

任务输出信息。

**属性**

**task\_id** _string_

任务id。

**task\_status** _string_

任务状态。

-   PENDING：排队中
    
-   RUNNING：处理中
    
-   SUSPENDED：挂起
    
-   SUCCEEDED：执行成功
    
-   FAILED：执行失败
    
-   UNKNOWN：任务不存在或状态未知
    

**results** _array object_

任务结果列表，包括图像URL。

**属性**

**url** _string_

模型生成图片的URL地址。

**task\_metrics** _object_

任务信息统计指标。

**属性**

**TOTAL** _integer_

总的任务数。

**SUCCEEDED** _integer_

任务状态为成功的任务数。

**FAILED** _integer_

任务状态为失败的任务数。

**submit\_time** _string_

任务提交时间。

**scheduled\_time** _string_

任务排期执行时间。

**end\_time** _string_

任务完成时间。

**result\_url** _string_

输出图片url。

**code** _string_

任务执行失败的错误码。

**message** _string_

任务执行失败的详细信息。

**usage** _object_

输出信息统计。

**属性**

**image\_count** _integer_

模型生成图像的数量。

**request\_id** _string_

请求唯一标识。可用于请求明细溯源和问题排查。

## **错误码**

如果模型调用失败并返回报错信息，请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。

此API还有特定状态码，具体如下所示。

**HTTP状态码**

**接口错误码（code）**

**接口错误信息（message）**

**含义说明**

400

InvalidFile.Content

The input image has no human body or has unclear human body. Please upload other image

输入图片中没有人

400

InvalidParameter

The request is missing required parameters or in a wrong format, please check the parameters that you send.

入参格式不对

400

InvalidURL

The request URL is invalid, please check the request URL is available and the request image format is one of the following types: JPEG, JPG, PNG, BMP, and WEBP.

输入图片下载失败，请检查网络或者输入格式

400

InvalidFile.Resolution

The image resolution is invalid, please make sure that the aspect ratio is smaller than 2.0, and largest length of image is smaller than 4096

上传图片大小不符合要求

500

InternalError.Algo

An internal error occurs during computation, please try this model later.

算法运行错误
