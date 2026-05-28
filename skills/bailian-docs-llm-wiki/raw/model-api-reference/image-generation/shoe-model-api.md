# 鞋靴模特API参考

本文介绍鞋靴模特模型的输入输出参数。鞋靴模特模型支持输入多视角鞋靴系列图片，同时对输入模特模板图的鞋子区域进行鞋靴AI试穿，实现模特鞋靴布局重绘生成，最终生成图片的效果布局自然、细节丰富、画面细腻、试穿结果逼真。可用于模特商品图设计、新鞋AI试穿、模特穿戴布局重绘等场景。

**相关指南**：[鞋靴模特](https://help.aliyun.com/zh/model-studio/shoes-and-boots-model)

**重要**

-   本文档仅适用于“中国内地（北京）”地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)。
    
-   shoemodel-v1 模型当前仅提供**免费体验**，免费额度用完后不可调用且不支持付费。
    

## **模型概览**

**模型名**

**免费额度**[（查看）](https://help.aliyun.com/zh/model-studio/new-free-quota)

**计费单价**

**限流（含主账号与RAM子账号）**

**任务下发接口QPS限制**

**同时处理中任务数量**

shoemodel-v1

500张

目前仅供免费体验。

> 免费额度用完后不可调用，敬请关注后续动态。

2

1

## **前提条件**

您需要已[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

## HTTP调用

为了减少等待时间并且避免请求超时，服务采用异步方式提供。您需要发起两个请求：

-   **创建任务**：首先发送一个请求创建鞋靴模特任务，该请求会返回任务ID。
    
-   **根据任务ID查询结果**：使用上一步获得的任务ID，查询模型生成的结果。
    

### **步骤1：创建任务获取任务ID**

`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/virtualmodel/generation/`

#### **请求头（Headers）**

## 鞋靴模特试穿

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/virtualmodel/generation/' \
--header 'X-DashScope-Async: enable' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "shoemodel-v1",
    "input": {
        "template_image_url": "https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8268778171/p809310.webp",
        "shoe_image_url": ["https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8268778171/p809301.webp"]
    },
    "parameters": 
    {
        "n": 1
    }
}'
```

**Authorization** _string_ **必选**

推荐您使用阿里云百炼API-Key，也可填DashScope API-Key。例如：Bearer d1xxx2a。

**X-DashScope-Async** _string_ **必选**

是否使用DashScope异步调用。HTTP只支持异步调用，设置为`enable`。

**Content-Type** _string_ **必选**

请求内容类型。固定为`application/json`。

#### **请求体（Request Body）**

**model** _string_ **必选**

调用模型。鞋靴模特生成模型为`shoemodel-v1`。

**parameters** Integer **必选**

图片生成的数量，目前支持 1~4 张，默认值 1。

**input** _object_ **必选**

输入图像的基本信息，比如图像URL地址。

**属性**

**template\_image\_url** _string_ **必选**

模板模特图片的URL地址。

URL 需为公网可访问的地址，并支持 HTTP 或 HTTPS 协议。您也可在此[获取临时公网URL](https://help.aliyun.com/zh/model-studio/get-temporary-file-url)。

图像限制：

-   图片大小建议小于5M。
    
-   图像格式：jpg、png、jpeg、bmp、webp、avif。
    
-   图像比例：图长边与短边的比例需在`[2:3, 3:2]` 范围内，推荐比例为`4:3`。
    

**shoe\_image\_url** _list_ **必选**

鞋靴多视角图片URL地址。

URL 需为公网可访问的地址，并支持 HTTP 或 HTTPS 协议。您也可在此[获取临时公网URL](https://help.aliyun.com/zh/model-studio/get-temporary-file-url)。

-   图片大小建议小于5M。
    
-   图像格式：jpg、png、jpeg、bmp、webp、avif。
    
-   图像比例：图长边与短边的比例需在`[2:3, 3:2]` 范围内，推荐与模特模板一样，比例为`4:3`。
    
-   多视角图片张数小于3。
    

**scale** _float_ 可选

控制生成强度。

范围在\[2.0,8.0\]，默认为5.0，数值越大，颜色越鲜亮。

#### **响应**

## 正常响应

```
{
    "output": {
	"task_id": "d76ec1e8-ea27-4038-8913-xxxxxxxxxxxx", 
        "task_status": "PENDING"
    }
    "request_id": "7574ee8f-38a3-4b1e-9280-11c33ab46e51"
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
    

**code** _string_

任务执行失败的错误码。

**message** _string_

任务执行失败的详细信息。

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

```
{
    "request_id":"<your request id>",
    "output":{
        "task_id":"<your task id>",
        "task_status":"SUCCEEDED",
        "submit_time":"2024-05-16 13:50:xx.xxx",
        "scheduled_time":"2024-05-16 13:50:xx.xxx",
        "end_time":"2024-05-16 13:50:xx.xxx",
        "results":[
            {
                "url":"https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx/res_img.png?Expires=xxx&OSSAccessKeyId=xxx&Signature=xxx"
            }
        ],
        "task_metrics":{
            "TOTAL":1,
            "SUCCEEDED":1,
            "FAILED":0
        }
    },
    "usage":{
        "image_count":1
    }
}
```

## 任务执行中

```
{
    "request_id":"e5d70b02-ebd3-98ce-9fe8-759d7d7b107d",
    "output":{
        "task_id":"86ecf553-d340-4e21-af6e-a0c6a421c010",
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
  "request_id": "<your request id>",
  "output": {
    "task_id": "<your task id>",
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

**results** _array_

输出图片列表。每个元素包含一个`url`字段，表示生成图片的URL。

**code** _string_

任务执行失败的错误码。

**message** _string_

任务执行失败的详细信息。

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

InvalidParameter

Required parameter(s) missing or invalid, please check the request parameters.（可根据实际情况修改）

接口调用参数不合法

400

InvalidFile.Content

The input image has no human body or has unclear human body. Please upload other image.

输入图片中人体不完整或者没有人体

400

InvalidParameter

The request is missing required parameters or in a wrong format, please check the parameters that you send.

入参格式不对

400

InvalidParameter.DataInspection

Unable to download the media resource during the data inspection process.

数据检查过程中无法下载媒体资源，请检查输入URL是否可访问以及图片格式是否正确

400

InvalidFile.Resolution

The image resolution is invalid, please make sure that the aspect ratio is smaller than 3:2, and largest length of image is smaller than 4096.

上传图片大小不符合要求

500

InternalError.Algo

An internal error occurs during computation, please try this model later.

算法运行错误
