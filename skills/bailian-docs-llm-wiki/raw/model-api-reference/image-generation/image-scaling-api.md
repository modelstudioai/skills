# 图像画面扩展API参考

本文介绍图像画面扩展模型的输入输出参数。图像画面扩展（也称“扩图”）支持多种扩展方式，包括按宽高比扩图、按比例扩图、在上下左右四个方向添加像素扩图。这三种方式还可以结合旋转角度进行扩图。

**相关指南**：[图像画面扩展](https://help.aliyun.com/zh/model-studio/image-expansion)

**重要**

本文档仅适用于“中国大陆（北京）”地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)。

## **模型概览**

**模型名称**

**计费单价**

**限流（主账号与RAM子账号共享）**

**免费额度**[（查看）](https://help.aliyun.com/zh/model-studio/new-free-quota)

**任务下发接口QPS限制**

**同时处理中任务数量**

image-out-painting

0.18元/张

2

5

500张

## **前提条件**

您需要已[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。如果通过SDK调用，还需要[安装DashScope SDK](https://help.aliyun.com/zh/model-studio/install-sdk)。

## **HTTP调用**

为了减少等待时间并且避免请求超时，服务采用异步方式提供。您需要发起两个请求：

-   **步骤1：创建任务获取任务ID**：首先发送一个请求创建扩图任务，该请求会返回任务ID。
    
-   **步骤2：根据任务ID查询结果**：使用上一步获得的任务ID，查询模型生成的结果。
    

### **步骤1：创建任务获取任务ID**

`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/out-painting`

#### **请求头（Headers）**

## 旋转图像

```
curl --location --request POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/out-painting' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'X-DashScope-Async: enable' \
--header 'Content-Type: application/json' \
--data '{
    "model": "image-out-painting",
    "input": {
        "image_url": "http://xxx/image.jpg"
    },
    "parameters":{
        "angle": 45,
        "x_scale":1.5,
        "y_scale":1.5
    }
}'
```

## 等比例扩图

```
curl --location --request POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/out-painting' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'X-DashScope-Async: enable' \
--header 'Content-Type: application/json' \
--data '{
    "model": "image-out-painting",
    "input": {
        "image_url": "http://xxx/image.jpg"
    },
    "parameters":{
        "x_scale":2,
        "y_scale":2,
        "best_quality":false,
        "limit_image_size":true
    }
}'
```

## 指定方向扩图

```
curl --location --request POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/out-painting' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'X-DashScope-Async: enable' \
--header 'Content-Type: application/json' \
--data '{
    "model": "image-out-painting",
    "input": {
        "image_url": "http://xxx/image.jpg"
    },
    "parameters": {
        "left_offset": 200,
        "right_offset": 100,
        "best_quality": false,
        "limit_image_size": true
    }
}'
```

## 指定宽高比扩图

```
curl --location --request POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/out-painting' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'X-DashScope-Async: enable' \
--header 'Content-Type: application/json' \
--data-raw '{
    "model": "image-out-painting",
    "input": {
        "image_url": "https://huarong123.oss-cn-hangzhou.aliyuncs.com/image/%E5%9B%BE%E5%83%8F%E7%94%BB%E9%9D%A2%E6%89%A9%E5%B1%95.png"
    },
    "parameters":{
        "angle":0,
        "output_ratio":"4:3",
        "best_quality":false,
        "limit_image_size":true
    }
}'
```

**Content-Type** `_string_` **（必选）**

请求内容类型。此参数必须设置为`application/json`。

**Authorization** `_string_`**（必选）**

请求身份认证。接口使用阿里云百炼API-Key进行身份认证。示例值：Bearer sk-xxxx。

**X-DashScope-Async** `_string_` **（必选）**

异步处理配置参数。HTTP请求只支持异步，**必须设置为**`**enable**`。

**重要**

缺少此请求头将报错：“current user api does not support synchronous calls”。

#### **请求体（Request Body）**

**model** `_string_` **（必选）**

模型名称。示例值：`image-out-painting`。

**input** `_object_` **（必选）**

输入图像的基本信息，比如图像URL地址。

**属性**

**image\_url** `_string_` **（必选）**

图像URL地址或者图像base64数据。

URL 需为公网可访问的地址，并支持 HTTP 或 HTTPS 协议。您也可在此[获取临时公网URL](https://help.aliyun.com/zh/model-studio/get-temporary-file-url)。

图像限制：

-   图像格式：JPG、JPEG、PNG、HEIF、WEBP。
    
-   图像大小：不超过10MB。
    
-   图像分辨率：不低于512×512像素且不超过4096×4096像素。
    
-   图像单边长度范围：\[512, 4096\]，单位像素。
    

**parameters** `_object_` **（必选）**

设置输出图像的处理参数，如逆时针旋转角度、宽高比、扩展比例、四个方向像素填充等。

**属性**

**angle** `_integer_` （可选）

逆时针旋转角度。默认值为0，取值范围\[0, 359\]，单位为度。

更多内容请参见[参数使用说明](#014530f228d94)。

**output\_ratio** `_string_` （可选）

图像宽高比。可选值有\["","1:1", "3:4", "4:3", "9:16", "16:9"\]。默认值为""，表示不设置输出图像的宽高比。

更多内容请参见[参数使用说明](#014530f228d94)。

**x\_scale** `_float_` （可选）

图像居中，在水平方向上按比例扩展图像。

默认值为1.0，取值范围\[1.0, 3.0\]。

您可以选择与y\_scale参数搭配使用，更多内容请参见[参数使用说明](#014530f228d94)。

**示例**

例如：输入图像分辨率为1000×1000（宽×高），x\_scale=2.0，扩展后的图像分辨率为2000×1000（宽×高）。保持高度不变，左右各添加500个像素。

**y\_scale** `_float_` （可选）

图像居中，在垂直方向上按比例扩展图像。

默认值为1.0，取值范围\[1.0, 3.0\]。

您可以选择与x\_scale参数搭配使用，更多内容请参见[参数使用说明](#014530f228d94)。

**示例**

例如：输入图像分辨率为1000×1000（宽×高），y\_scale=2.0，扩展后的图像分辨率为1000×2000（宽×高）。保持宽度不变，上下各添加500个像素。

**top\_offset** `_integer_` （可选）

在图像上方添加像素。

默认值为0，取值限制`top_offset+bottom_offset < 3×输入图像高度`。

您可以选择与bottom\_offset、left\_offset 、right\_offset参数搭配使用，更多内容请参见[参数使用说明](#014530f228d94)。

**示例**

例如：输入图像分辨率为1000×1000（宽×高），top\_offset=500，扩展后的图像分辨率为1000×1500（宽×高）。保持宽度不变，只在图像上方添加500个像素。

**bottom\_offset** `_integer_` （可选）

在图像下方添加像素。

默认值为0，取值限制`top_offset+bottom_offset < 3×输入图像高度`。

您可以选择与top\_offset、left\_offset 、right\_offset参数搭配使用，更多内容请参见[参数使用说明](#014530f228d94)。

**示例**

例如：输入图像分辨率为1000×1000（宽×高），bottom\_offset=500，扩展后的图像分辨率为1000×1500（宽×高）。保持宽度不变，只在图像下方添加500个像素。

**left\_offset** `_integer_` （可选）

在图像左侧添加像素。

默认值为0，扩展限制`left_offset+right_offset < 3×输入图像宽度`。

您可以选择与top\_offset、bottom\_offset、right\_offset参数搭配使用，更多内容请参见[参数使用说明](#014530f228d94)。

**示例**

例如：输入图像分辨率为1000×1000（宽×高），left\_offset=500，扩展后的图像分辨率为1500×1000（宽×高）。保持高度不变，只在图像左侧添加500个像素。

**right\_offset** `_integer_` （可选）

在图像右侧添加像素。

默认值为0，扩展限制`left_offset+right_offset < 3×输入图像宽度`。

您可以选择与top\_offset、bottom\_offset、left\_offset参数搭配使用，更多内容请参见[参数使用说明](#014530f228d94)。

**示例**

例如：输入图像分辨率为1000×1000（宽×高），right\_offset=500，扩展后的图像分辨率为1500×1000（宽×高）。保持高度不变，只在图像右侧添加500个像素。

**best\_quality** `_boolean_` （可选）

开启图像最佳质量模式。默认值为false，减少图像生成的等待时间。

如果您需要更多图像细节，可以设置为true，但耗时会成倍增加。

**limit\_image\_size** `_boolean_` （可选）

限制模型生成的图像文件大小。默认值为true，当输入图像单边长度<=10000时，输出图像文件大小在5MB以下。

输出图像的长宽比范围为`1:4至4:1`。

**建议设置为true**。模型生成的图像需要经过一层安全过滤后才能输出，当前不支持大于10M的图像处理。

**add\_watermark** `_boolean_` （可选）

添加`Generated by AI`水印。默认值为True，在输出图像左下角处添加水印。

#### **响应**

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
    "code":"InvalidApiKey",
    "message":"Invalid API-key provided.",
    "request_id":"fb53c4ec-1c12-4fc4-a580-xxxxxx"
}
```

**output** _object_

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

`GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`

#### **请求头（Headers）**

## 查询任务结果

请将`86ecf553-d340-4e21-xxxxxxxxx`替换为真实的task\_id。

```
curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/86ecf553-d340-4e21-xxxxxxxxx \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

**Authorization** `_string_`**（必选）**

请求身份认证。接口使用阿里云百炼API-Key进行身份认证。示例值：Bearer sk-xxxx。

#### **URL路径参数（Path parameters）**

**task\_id** `_string_`**（必选）**

任务ID。

#### **响应**

## 任务执行成功

```
{
    "request_id": "b67df059-ca6a-9d51-afcd-9b3c4456b1e2",
    "output": {
        "task_id": "d76ec1e8-ea27-4038-8913-235c88ef0f70",
        "task_status": "SUCCEEDED",
        "submit_time": "2024-05-16 13:50:01.247",
        "scheduled_time": "2024-05-16 13:50:01.354",
        "end_time": "2024-05-16 13:50:27.795",
        "output_image_url": "https://xxxx/xxxx"
    },
    "usage": {
        "image_count": 1
    }
}
```

## 任务执行中

```
{
    "request_id":"e5d70b02-ebd3-98ce-9fe8-759d7d7b107d",
    "output":{
        "task_id":"d76ec1e8-ea27-4038-8913-235c88ef0f70",
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
        "task_id": "4cbabbdf-2c1f-43f4-b983-c2cc47f4c115",
        "task_status": "FAILED",
        "submit_time": "2024-05-16 14:15:14.103",
        "scheduled_time": "2024-05-16 14:15:14.154",
        "end_time": "2024-05-16 14:15:14.694",
        "code": "InvalidParameter.FileDownload",
        "message": "download for input_image error"
    }
}
```

**output** _object_

输出的任务信息。

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
    

**task\_metrics** `_object_`

任务结果统计。

**属性**

**TOTAL** `_integer_`

总的任务数。

**SUCCEEDED** `_integer_`

任务状态为成功的任务数。

**FAILED** `_integer_`

任务状态为失败的任务数。

**submit\_time** `_string_`

任务提交时间。

**end\_time** `_string_`

任务完成时间。

**output\_image\_url** `_string_`

输出图像URL地址。

**code** `_string_`

请求失败的错误码。请求成功时不会返回此参数，详情请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。

**message** `_string_`

请求失败的详细信息。请求成功时不会返回此参数，详情请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。

**usage** _object_

图像统计信息。

**属性**

**image\_count** `_integer_`

模型成功生成图片的数量。计费公式：费用 = 图片数量 × 单价。

**request\_id** `_string_`

请求唯一标识。可用于请求明细溯源和问题排查。

## **图像处理参数使用说明**

在图像处理参数 `parameters`中，主要包含两类参数：旋转参数、扩展参数。扩展参数按功能分为三类，它们之间相互独立、互不影响。

**参数类型**

**优先级**

**参数**

旋转参数

先旋转，后扩展

`angle`

扩展参数

扩展优先级1：按宽高比扩展

`output_ratio`

扩展优先级2：按比例扩展

`x_scale`、`y_scale`

扩展优先级3：在指定方向添加像素扩展

`left_offset`、`right_offset`、`top_offset`、`bottom_offset`

**参数设置建议**

1.  **仅按宽高比扩图** ：只需设置 `output_ratio`，并将其设置为非空的宽高比值（如 "4:3"、"16:9" 等）。
    
2.  **仅按比例扩图** ：只需设置`x_scale`、`y_scale`，且至少一个参数值大于 1.0，两者既可单独使用也可搭配使用。
    
3.  **仅在指定方向添加像素扩图** ：只需设置 `left_offset`、`right_offset`、`top_offset`、`bottom_offset`，且至少有一个参数值大于 0。这四个参数既可单独使用也可搭配使用。
    
4.  **仅旋转图像** ：只需设置 `angle` ，并将其设置为 \[1, 359\] 范围内的值，但不能设置为 90、180、270。
    
5.  **先旋转再扩图**：需要设置`angle` ，并将其设置为 \[1, 359\] 范围内的任意值。同时必须与以下三组扩展参数中的一组搭配使用。若同时设置多组扩展参数，按[参数优先级](#3404cbdb44tku)生效。
    
    1.  `output_ratio`：不为空。
        
    2.  `x_scale、y_scale`：至少有一个大于 1.0。
        
    3.  `top_offset、bottom_offset、left_offset、right_offset`：至少有一个参数值大于 0。
        
    
    > **注意** ：先旋转后扩图时，模型会先根据指定角度旋转图像，再在旋转后的图像上进行扩图操作。实际扩图效果请以模型输出为准。
    

**参数优先级**

-   当`angle > 0`且同时设置扩展参数时，处理顺序为：**先旋转 → 后扩展**。
    
-   当 `angle = 0`或图像完成旋转后，扩展参数按以下优先级生效：
    
    -   **优先级1：按宽高比扩展（output\_ratio）**
        
        若 output\_ratio 不为空，则按此宽高比生成图像，其他扩展参数均被忽略。
        
    -   **优先级2：按比例扩展（x\_scale、y\_scale）**
        
        若未设置 output\_ratio，且 x\_scale 和 y\_scale 至少有一个参数值大于 1，则按此比例对图像进行扩展。此时，忽略添加像素扩展的相关参数。
        
    -   **优先级3：在指定方向添加像素扩展（left\_offset、right\_offset、top\_offset、bottom\_offset）**
        
        若未设置 output\_ratio、x\_scale、y\_scale，且left\_offset、right\_offset、top\_offset、bottom\_offset至少有一个参数值大于0，则按此方式在指定方向添加像素扩图。
        

**参数组合示例**

**配置组合**

**实际生效模式**

`output_ratio="4:3", x_scale=2.0`

按宽高比4:3扩图（仅`output_ratio`生效）

`x_scale=2.0, left_offset=100`

按比例扩图（仅`x_scale`生效）

`angle=90, x_scale=2.0`

先逆时针旋转 90°，再将旋转后的图像的宽边扩展到2.0倍（`angle`、`x_scale`均生效）

`angle=90, output_ratio="4:3", x_scale=2.0, left_offset=100`

先逆时针旋转90°，再对旋转后的图像按宽高比4:3扩图（仅`angle`、`output_ratio`生效）

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

输入json错误

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

The image content does not comply with green network verification

图像内容不合规

400

InvalidParameter

the parameters must conform to the specification: xxx

输入参数值超出范围

400

InvalidParameter.DataInspection

The image size is not supported for the data inspection.

输出图像尺寸超限（大于10M）

500

InternalError.Algo

algorithm process error

算法错误

500

InternalError.FileUpload

oss upload error

文件上传失败

## **常见问题**

**Q：创建任务接口响应成功，但没有返回图像URL？**

**A：**在图像模型处理中，HTTP请求需要经过两步才能获取结果：创建任务、根据任务ID查询结果。创建任务接口仅提交任务，不返回图像结果。您需要查询 `GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}` 接口获得模型生成的图像URL。

**Q：设置输出比例** `**output_ratio**` **后，为什么模型没有根据** `**x_scale**` **或** `**y_scale**` **自动计算另一个方向的比例？**

**A：**图像画面扩展API目前支持三种扩展方式：按宽高比扩展、按比例扩展、在指定方向添加像素扩展。三者参数相互独立，互不影响。为避免参数冲突，系统设定了明确的优先级：`output_ratio > x_scale / y_scale > *offset`。

一旦设置了 output\_ratio（非空），系统将仅按该宽高比进行扩展，忽略所有其他扩展参数。因此，若同时设置了 output\_ratio 和 x\_scale ，只有 output\_ratio 生效，x\_scale 被自动忽略，也不会基于 x\_scale 自动推导或计算 y\_scale。
