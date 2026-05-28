# 人物实例分割API参考

本文介绍人物实例分割模型的输入输出参数。人物实例分割运用了检测和分割技术，不仅能够在图像中识别出不同的对象，而且还能准确地画出每一个对象边界的像素级掩码（mask）。

**相关指南**：[人物实例分割](https://help.aliyun.com/zh/model-studio/image-instance-segmentation)

**重要**

-   本文档仅适用于“中国内地（北京）”地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)。
    
-   image-instance-segmentation 模型当前仅提供**免费体验**，免费额度用完后不可调用且不支持付费。
    

## **模型概览**

**模型名**

**免费额度**[（查看）](https://help.aliyun.com/zh/model-studio/new-free-quota)

**计费单价**

**限流（含主账号与RAM子账号）**

**任务下发接口QPS限制**

**同时处理中任务数量**

image-instance-segmentation

500张

目前仅供免费体验。

> 免费额度用完后不可调用，敬请关注后续动态。

2

1

## **前提条件**

您需要已[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

## HTTP调用

为了减少等待时间并且避免请求超时，服务采用异步方式提供。您需要发起两个请求：

-   **创建任务**：首先发送一个请求创建人物实例分割任务，该请求会返回任务ID。
    
-   **根据任务ID查询结果**：使用上一步获得的任务ID，查询模型生成的结果。
    

### **步骤1：创建任务获取任务ID**

`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis`

#### **请求头（Headers）**

## 人物实例分割

```
curl --location --request POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
--header 'X-DashScope-Async: enable' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data-raw '{
    "model": "image-instance-segmentation",
    "input": {
            "image_url": "http://xxx/image.png"
        },
    "parameters":{
    }
}'
```

**Content-Type** _string_ **必选**

请求内容类型。固定为`application/json`。

**Authorization** _string_ **必选**

推荐您使用阿里云百炼API-Key，也可填DashScope API-Key。例如：Bearer d1xxx2a。

**X-DashScope-Async** _string_ **必选**

是否开启异步处理。必须开启异步处理，设置为`enable`。

#### **请求体（Request Body）**

**model** _string_ **必选**

调用模型。

**input** _object_ **必选**

输入图像的基本信息，比如图像URL。

**属性**

**image\_url** _string_ **必选**

输入图像URL地址。

URL 需为公网可访问的地址，并支持 HTTP 或 HTTPS 协议。您也可在此[获取临时公网URL](https://help.aliyun.com/zh/model-studio/get-temporary-file-url)。

图像限制：

-   图片格式：JPEG，PNG，JPG，BMP，WEBP。
    
-   图像分辨率：不低于512×512像素且不超过4096×4096像素。
    
-   图像单边长度范围：\[512, 4096\]，单位像素。
    
-   图片大小：不超过10M。
    
-   URL地址中不能包含中文字符。
    

#### **响应**

## 成功响应

```
{
    "output": {
        "task_status": "PENDING",
        "task_id": "53950fb7-281a-4e60-xxxxxxxxxxxx"
    },
    "request_id": "1027557e-8c3f-9db5-8cd2-xxxxxxxxxxxx"
}
```

## 异常响应

```
{
    "code":"InvalidApiKey",
    "message":"Invalid API-key provided.",
    "request_id":"fb53c4ec-1c12-4fc4-a580-xxxxxxxxxxxx"
}
```

**output** _object_

任务输出信息。

**属性**

**task\_id** _string_

任务id，任务唯一标识。

**task\_status** _string_

任务状态。

-   PENDING：排队中
    
-   RUNNING：处理中
    
-   SUSPENDED：挂起
    
-   SUCCEEDED：执行成功
    
-   FAILED：执行失败
    

**code** _string_

接口错误码。接口成功请求不会返回该参数。

**message** _string_

接口错误信息。接口成功请求不会返回该参数。

**request\_id（可选）**_string_

本次请求的系统唯一码。

### **步骤2：根据任务ID查询结果**

`GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`

#### **请求头（Headers）**

## 获取任务结果

```
curl -X GET \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
https://dashscope.aliyuncs.com/api/v1/tasks/53950fb7-281a-4e60-xxxxxxxxxxxx
```

**Authorization** _string_ **必选**

API-Key，例如：Bearer d1\*\*2a。

#### **URL路径参数（Path parameters）**

**task\_id** _string_ **必选**

任务id。

#### **响应**

## 任务执行成功

对于本模型，任务在结束之后的状态会持续保留24小时以备客户随时查询，24小时之后，任务将从系统中清除，相关的结果也将一并清除；对应的，任务生成的结果为图像的URL地址，出于安全考虑，该URL的下载有效期也是24小时，需要用户在获取任务结果后根据需要及时使用或者转存。

```
{
    "request_id": "b67df059-ca6a-9d51-afcd-9b3c4456b1e2",
    "output": {
        "task_id": "53950fb7-281a-4e60-xxxxxxxxxxxx",
        "task_status": "SUCCEEDED",
        "submit_time": "2024-05-16 13:50:01.247",
        "scheduled_time": "2024-05-16 13:50:01.354",
        "end_time": "2024-05-16 13:50:27.795",
        "output_image_url": "http://xxx/result1.png",
        "output_vis_image_url":"http://xxx/result2.png"
    },
    "usage": {
        "image_count": 1
    }
}
```

## 任务执行中

```
{
    "request_id":"7574ee8f-38a3-4b1e-xxxxxxxxxxxx",
    "output":{
        "task_id":"53950fb7-281a-4e60-xxxxxxxxxxxx",
        "task_status":"RUNNING",
        "task_metrics":{
            "TOTAL":1,
            "SUCCEEDED":1,
            "FAILED":0
        }
    }
}
```

## 任务执行失败

```
{
    "request_id": "dccfdf23-b38e-97a6-a07b-f35118c1ada6",
    "output": {
        "task_id": "53950fb7-281a-4e60-xxxxxxxxxxxx",
        "task_status": "FAILED",
        "submit_time": "2024-05-16 14:15:14.103",
        "scheduled_time": "2024-05-16 14:15:14.154",
        "end_time": "2024-05-16 14:15:14.694",
        "code": "InvalidParameter.FileDownload",
        "message": "download for input_image error"
    }
}
```

**request\_id** _string_

本次请求的系统唯一码。

**status\_code** _int_

200（HTTPStatus.OK）表示请求成功，否则表示请求失败，可以通过code获取错误码，通过message字段获取错误详细信息。

**code** _string_

如果失败表示错误码，参考错误码表。

**message** _string_

如果失败，内容为失败详细信息。

**output** _object_

任务输出信息。

**属性**

**task\_id** _string_

任务id。

**task\_status** _string_

任务状态。

-   PENDING：排队中。
    
-   RUNNING：处理中。
    
-   SUCCEEDED：成功。
    
-   FAILED：失败。
    
-   UNKNOWN：任务不存在或状态未知。
    

**output\_image\_url** _string_

分割后图像URL地址。限制输出图像长宽比范围为1:10-10:1。

**output\_vis\_image\_url** _string_

分割后可视化图像的URL地址，限制输出图像长宽比范围为1:10-10:1。

**usage** _object_

输出信息统计。

**属性**

**image\_count** _integer_

本次请求生成图像数量。

## 补充：如何从人物实例分割掩码图中获取保留人物和待擦除人物掩码图？

以下代码示例将得到的人物实例分割结果图拆分成擦除区域图以及保留区域图，后续调用图像擦除模型擦除不需要的人像。

**原图**

**人物实例分割结果**

**保留区域**

**擦除区域**

![图片擦除2-原图.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0184161571/p840837.png)

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6043984271/p841094.png)

mask.png

![图片擦除2-保留.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0184161571/p840841.png)

reserve.png

![图片擦除2-擦除.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0184161571/p840839.png)

remove.png

```
import cv2
import numpy as np

def get_remove_mask(mask_path, remove_mask_path, reserve_ids=[]):
    mask = cv2.imread(mask_path)
    instance_num = int(mask.max())
    new_mask = np.zeros((mask.shape[0], mask.shape[1], 3))
    for i in range(1, instance_num+1):
        if i in reserve_ids:
            continue
        new_mask[mask[:, :, 0] == i] = (255, 255, 255)
    cv2.imwrite(remove_mask_path, new_mask.astype(np.uint8))

def get_reserve_mask(mask_path, reserve_mask_path, reserve_ids=[]):
    mask = cv2.imread(mask_path)
    instance_num = int(mask.max())
    new_mask = np.zeros((mask.shape[0], mask.shape[1], 3))
    for i in range(1, instance_num + 1):
        if i in reserve_ids:
            new_mask[mask[:,:,0] == i]  = (255, 255, 255)
    cv2.imwrite(reserve_mask_path, new_mask.astype(np.uint8))

if __name__ == '__main__':
    mask_path = 'mask.png'
    remove_mask_path = 'remove.png'
    reserve_mask_path = 'reserve.png'
    get_remove_mask(mask_path, remove_mask_path, reserve_ids=[1])
    get_reserve_mask(mask_path, reserve_mask_path, reserve_ids=[1])
```

## **错误码**

如果模型调用失败并返回报错信息，请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。

此API还有特定状态码，具体如下所示。

**HTTP状态码**

**接口错误码（code）**

**接口错误信息（message）**

**含义说明**

400

InvalidParameter.JsonPhrase

input json error

输入JSON错误

400

InvalidParameter.FileDownload

oss download error

输入图像下载失败

400

InvalidParameter.ImageFormat

read image error

读取图像失败

400

InvalidParameter.ImageContent

The image content does not comply with green network verification.

图像内容不合规

400

InvalidParameter

the parameters must conform to the specification: xxx

输入参数超出范围

500

InternalError.Algo

algorithm process error

算法错误

500

InternalError.FileUpload

oss upload error

文件上传失败
