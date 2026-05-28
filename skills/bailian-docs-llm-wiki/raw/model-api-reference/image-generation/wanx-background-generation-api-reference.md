# 图像背景生成API参考

本文介绍万相-背景生成模型的输入输出参数。

**相关指南**：[图像背景生成](https://help.aliyun.com/zh/model-studio/image-background-generation)

**重要**

本文档仅适用于“中国内地（北京）”地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)。

## **模型概览**

**模型效果示意**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5996781571/p904710.png)

**模型简介**

**模型名**

**模型简介**

wanx-background-generation-v2

万相-图像背景生成模型为主体商品生成背景图，适用于电商和海报场景。

支持多种背景生成方法：文本引导、图像引导、文本与图像结合引导，以及文本、图像与边缘引导元素的综合应用。

**模型名**

**计费单价**

**限流（含主账号与RAM子账号）**

**免费额度**[（查看）](https://help.aliyun.com/zh/model-studio/new-free-quota)

**任务下发接口QPS限制**

**同时处理中任务数量**

wanx-background-generation-v2

0.08元/张

2

1

500张

更多说明请参见[模型计费与限流](https://help.aliyun.com/zh/model-studio/image-faq#3436cf2280fnh)。

## **前提条件**

图像背景生成API目前仅支持HTTP调用。

您需要已[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

## HTTP调用

图像模型处理时间较长，为了避免请求超时，HTTP调用仅支持异步获取模型结果。您需要发起两个请求：

1.  **创建任务获取任务ID**：首先发起创建任务请求，该请求会返回任务ID（task\_id）。
    
2.  **根据任务ID查询结果**：使用上一步获得的任务ID，查询任务状态及结果。任务成功执行时将返回图像URL，有效期24小时。
    

**说明**

创建任务后，该任务将被加入到排队队列，等待调度执行。后续需要调用“根据任务ID查询结果接口”获取任务状态及结果。

### **步骤1：创建任务获取任务ID**

`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/background-generation/generation/`

#### **请求头（Headers）**

## 图像背景生成

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/background-generation/generation/' \
--header 'X-DashScope-Async: enable' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "wanx-background-generation-v2",
    "input": {
        "base_image_url": "https://vision-poster.oss-cn-shanghai.aliyuncs.com/lllcho.lc/data/test_data/images/main_images/new_main_img/a.png",
        "ref_image_url": "http://vision-poster.oss-cn-shanghai.aliyuncs.com/lllcho.lc/data/test_data/images/ref_images/c5e50d27be534709817b2ab080b0162f_0.jpg",
        "ref_prompt": "山脉和晚霞",
        "reference_edge": {
            "foreground_edge": [
                "https://vision-poster.oss-cn-shanghai.aliyuncs.com/lllcho.lc/data/test_data/images/huaban_soft_edge/6cdd13941cef1b11d885aea1717b983ae566b8efc9094-vcsvxa_fw658webp.png",
                "http://vision-poster.oss-cn-shanghai.aliyuncs.com/lllcho.lc/data/test_data/images/ref_edge/2c36cc4b7da027279e87311dac48fc2d5d784b1e72c0e-x4f1wC_fw658webp.png"
            ],
            "background_edge": [
                "http://vision-poster.oss-cn-shanghai.aliyuncs.com/lllcho.lc/data/test_data/images/ref_edge/0718a9741e07c52ca5506e75c4f2b99e22fff68a4c7d3-P9WGLr_fw658webp.png"
            ],
            "foreground_edge_prompt": [
                "粉色桃花",
                "可爱小狗"
            ],
            "background_edge_prompt": [
                "树叶"
            ]
        }
    },
    "parameters": {
        "n": 4,
        "ref_prompt_weight": 0.5,
        "model_version": "v3"
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

**X-DashScope-WorkSpace** `_string_` （可选）

阿里云百炼业务空间ID。示例值：llm-xxxx。

您可以在此[获取Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#d3eb3cd37b7fu)。

**详细说明**

此参数根据阿里云百炼API-Key进行填写。

-   若为主账号API-Key，可不填。不填则使用主账号权限，填写则使用对应的业务空间权限。
    
-   若为RAM子账号API-Key，则必填。RAM子账号一定归属于某个业务空间。
    

业务空间必须具备访问模型的权限，才能调用API。若无权限，请参考[授权子业务空间模型调用、训练和部署](https://help.aliyun.com/zh/model-studio/use-workspace#f2e68d7ba7ubk)。

> 关于如何区分阿里云百炼主账号和RAM子账号，请参考[主账号管理](https://help.aliyun.com/zh/model-studio/business-space-management)。

#### **请求体（Request Body）**

**model** `_string_` **（必选）**

模型名称。**当前仅支持填写** `**wanx-background-generation-v2**`。

wanx-background-generation-v2模型有两个版本：v2和v3，默认版本为v2。如需切换版本，请设置parameters.model\_version参数。

> **注意：**切换模型版本时，请不要将model设置为wanx-background-generation-v3。

> **正确的做法是**：model设置为wanx-background-generation-v2，parameters.model\_version设置为v3。

**如何切换模型版本？**

```
//注意：model必须设置为 wanx-background-generation-v2，model_version参数只支持设置为 v2 或 v3
//默认版本v2：旧版模型，速度快。
{
    "model": "wanx-background-generation-v2",
    "parameters": {
        "model_version": "v2"
    }
}

//切换为新版本v3：新版模型，速度稍慢，但效果更好，推荐切换到v3。
{
    "model": "wanx-background-generation-v2",
    "parameters": {
        "model_version": "v3"
    }
}
```

**input** `_object_`**（必选）**

输入图像的基本信息，比如图像URL。

**属性**

**base\_image\_url** `_string_`**（****_必选_****）**

主体图像URL。主体图像必须为带透明背景的RGBA四通道图像。输出图像的分辨率与该图像保持一致。

URL 需为公网可访问的地址，并支持 HTTP 或 HTTPS 协议。您也可在此[获取临时公网URL](https://help.aliyun.com/zh/model-studio/get-temporary-file-url)。

图像格式为png，图像长边不超过2048像素。

更多说明请参见[主体图像限制](https://help.aliyun.com/zh/model-studio/image-background-generation#a65d17585c3iz)、[如何查看并获取RGBA图像](https://help.aliyun.com/zh/model-studio/image-background-generation#c456bddd3e6vy)。

**ref\_image\_url** `_string_`（可选）

引导图像URL。它与`ref_prompt`参数至少填写一个。

URL 需为公网可访问的地址，并支持 HTTP 或 HTTPS 协议。您也可在此[获取临时公网URL](https://help.aliyun.com/zh/model-studio/get-temporary-file-url)。

图像要求：jpg、png、webp等常见格式。

引导图像可以是 RGB 图像或带透明背景的 RGBA 图像。对于RGBA图像，Alpha通道值为0的区域将不参与引导过程的生成，适用于带有主体的引导图。

**ref\_prompt** `_string_` （可选）

引导文本提示词，支持中英双语。它与`ref_image_url`参数至少填写一个。

英文最多支持150个单词，中文大概是100-120个中文字符，超过部分会被自动忽略。

示例：山脉和晚霞。

**neg\_ref\_prompt** `_string_` （可选）

负向提示词，描述画面不希望出现的内容。一般不填，使用模型内置的默认值。

英文最多支持150个单词，中文大概是100-120个中文字符，超过部分会被自动忽略。

示例：低质量的，模糊的，错误的。

**reference\_edge** `_object_` （可选）

边缘引导元素图像，包括前景元素图像列表和背景元素图像列表。

**属性**

**foreground\_edge** `**s**_tring list_` （可选）

前景元素图像URL列表。

每个图像必须为带透明背景的RGBA四通道图像，分辨率和主体图像相同，如果不同则会自动缩放到和主体图像相同的分辨率。

所有前景元素生成的图层在主体前面，可以对主体形成遮挡。每个元素的图层顺序为从底到上。

foreground\_edge图像列表和background\_edge图像列表之和不得超过10。

前景元素图像的生成方式参考[边缘引导元素生成方法](#ce3012665044e)。

**foreground\_edge\_prompt** `**s**_tring list_` （可选）

前景元素列表对应的prompt列表。

如果输入该参数，长度必须和foreground\_edge列表相等，且顺序一一对应。如果无需填写某个元素的prompt，可用空字符串占位。

对于每个列表元素，若为英文，则最多支持150个单词；若为中文，则大约支持100至120个中文字符。超过该范围的部分将被自动忽略。

**background\_edge** `**s**_tring list_` （可选）

背景元素图像URL列表。

每个图像必须为带透明背景的RGBA四通道图像，分辨率和主体图像相同，如果不同则会自动缩放到和主体图像相同的分辨率。

生成图层在主体的后面，如果重叠会被主体遮挡，每个元素的图层顺序为从底到上。

foreground\_edge图像列表和background\_edge图像列表之和不得超过10。

背景图像的生成方式参考[边缘引导元素生成方法](#ce3012665044e)。

**background\_edge\_prompt** `s_tring list_` （可选）

背景元素列表对应的prompt列表。

如果输入该参数，长度必须和background\_edge列表相等，且顺序一一对应，如果无需填写某个元素的prompt，可用空字符串占位。

对于每个列表元素，若为英文，则最多支持150个单词；若为中文，则大约支持100至120个中文字符。超过该范围的部分将被自动忽略。

**已废弃字段**

**title** `_string_` （可选）

**已废弃**，建议使用[图配文](https://help.aliyun.com/zh/model-studio/image-text-composition-api-reference)。

图像上添加文字主标题。算法自动确定文字的大小和位置，限制1~8个字符。

**sub\_title** `_string_` （可选）

**已废弃**，建议使用[图配文](https://help.aliyun.com/zh/model-studio/image-text-composition-api-reference)。

图像上添加文字副标题。算法自动确定文字的大小和位置，限制1~10个字符。

仅当title不为空时生效**。**

**parameters** `_object_` （可选）

图像处理参数。

属性

**n** `_integer_` （可选）

图片生成的数量，支持1~4 张，默认值1。

**model\_version** `_string_` （可选）

模型版本。可选值有：

-   v2：旧版模型，速度快，默认值。
    
-   v3：新版模型，速度慢，但效果更好，推荐切换到最新版本v3。
    

**noise\_level** `_integer_` （可选）

当ref\_image\_url不为空时生效。该参数在图像引导的过程中添加随机变化，数值越大生成背景与引导图像的相关性越低，默认值300，取值范围\[0,999\]。

**ref\_prompt\_weight** `_float_` （可选）

仅当ref\_image\_url和ref\_prompt同时输入时生效，表示引导文本prompt的权重。取值范围 \[0,1\]，默认值为0.5。

默认值表示引导文本和引导图像的权重都是0.5，对生成背景的影响程度相当。数值越大（大于0.5）表示引导文本对生成背景的影响程度越大。

**已废弃字段**

**scene\_type** `_string_` （可选）

**已废弃**，不建议使用该参数。

使用场景，当前包含3种场景：

-   GENERAL: 通用场景，默认值。
    
-   ROOM: 室内家居场景。
    
-   COSMETIC：美妆场景，也适用于大部分小商品摆放场景。
    

#### **响应**

## 成功响应

```
{
    "output": {
        "task_status": "PENDING",
        "task_id": "0385dc79-5ff8-4d82-bcb6-xxxxxx"
    },
    "request_id": "4909100c-7b5a-9f92-bfe5-xxxxxx"
}
```

## 异常响应

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

> 若使用新加坡地域的模型，需将base\_url替换为https://dashscope-intl.aliyuncs.com/api/v1/tasks/86ecf553-d340-4e21-xxxxxxxxx

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

任务数据（如任务状态、图像URL等）仅保留24小时，超时后会被自动清除。请您务必及时保存生成的图像。

```
{
    "request_id": "ded2407a-ec61-4a7d-adc0-xxxxxxxxxxxx",
    "output": {
        "task_id": "86ecf553-d340-4e21-xxxxxxxxx",
        "task_status": "SUCCEEDED",
        "submit_time": "2025-12-23 10:25:26.436",
        "scheduled_time": "2025-12-23 10:25:26.471",
        "end_time": "2025-12-23 10:26:06.390",
        "results": [
            {
                "url": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx.png?Expires=xxx"
            },
            {
                "url": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx.png?Expires=xxx"
            },
            {
                "url": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx.png?Expires=xxx"
            },
            {
                "url": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx.png?Expires=xxx"
            }
        ],
        "task_metrics": {
            "TOTAL": 4,
            "SUCCEEDED": 4,
            "FAILED": 0
        }
    },
    "usage": {
        "image_count": 4
    }
}
```

## 任务执行中

```
{
    "request_id":"e5d70b02-ebd3-98ce-9fe8-xxxxxxxxxxxx",
    "output":{
        "task_id":"13b1848b-5493-4c0e-xxxxxxxxxxxx",
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
    

**submit\_time** `_string_`

任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。

**scheduled\_time** `_string_`

任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。

**end\_time** `_string_`

任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。

**results** `_list_`

返回结果图像，图像分辨率大小与输入图像（base\_image\_url）保持一致。

示例值： \[{"url":"http://oss.aliyuncs.com/xxx/a.jpg"},{"url":"http://oss.aliyuncs.com/xxx/b.jpg"}\]。

**task\_metrics** `_object_`

任务结果统计。

**属性**

**TOTAL** `_integer_`

总的任务数。

**SUCCEEDED** `_integer_`

任务状态为成功的任务数。

**FAILED** `_integer_`

任务状态为失败的任务数。

**usage** `_object_`

输出信息统计。

**属性**

**image\_count** `_integer_`

模型成功生成图片的数量。计费公式：费用 = 图片数量 × 单价。

**request\_id** `_string_`

请求唯一标识。可用于请求明细溯源和问题排查。

## **边缘引导元素生成方法**

边缘引导元素生成方法因其能够有效保留图像中的边缘和结构信息，在图像背景生成任务中常用于生成前景或背景元素图像。

**步骤1**：PS抠图，导出带透明背景的4通道格式图像。

**步骤2**：生成边缘引导元素图像。

针对步骤2，我们提供两种方案，任选一种即可。

方案一：ModelScope在线生成。

访问ModelScope[背景图edge元素生成](https://modelscope.cn/studios/lllcho/bg_edge_elements)，直接上传第一步抠图后的图像点击运行即可获得符合要求的元素图像。

方案二：使用代码本地生成。

-   环境准备，Python环境中安装需要用到的依赖包。
    

```
pip install controlnet-aux==0.0.7
```

-   运行代码，使用如下Python脚本生成边缘引导元素。
    

```
import numpy as np
from PIL import Image
from controlnet_aux.processor import Processor

hed_processor = Processor('softedge_hed')

def make_elements(name):
    img=Image.open(name)
    img=np.array(img)
    img[:,:,:-1]=img[:,:,:-1]*(img[:,:,-1:]>127)
    img=Image.fromarray(img,mode='RGBA')
    r,g,b,a=img.split()
    img=Image.merge(mode='RGB',bands=[r,g,b])
    edge = hed_processor(img, to_pil=True).resize(img.size).convert('RGB')
    edge.putalpha(a)
    edge=np.array(edge)
    edge[:,:,:-1]=edge[:,:,:-1]*(edge[:,:,-1:]>50)
    edge=Image.fromarray(edge,mode='RGBA')
    edge.save('result.png')
```

## 错误码

大模型服务通用状态码请查阅：[错误信息](https://help.aliyun.com/zh/model-studio/error-code)

同时本模型还有如下特定错误码：

**HTTP 返回码**

**错误码（code）**

**错误信息（message）**

**含义说明**

400

InvalidParameter.DataInspection

Download the media resource timed out during the data inspection process.

可能原因：图片所属服务器不稳定，导致下载超时

## 常见问题

图像模型的通用问题请参见[常见问题](https://help.aliyun.com/zh/model-studio/image-faq)文档，包含模型计费与限流、接口高频报错等。

本模型还存在一些特有问题。

### **接口报错**

#### **wanx-background-generation-v3模型不存在**

**报错场景**：如果您想切换V3模型，并将model参数设置为wanx-background-generation-v3，发送请求后发现报错，报错信息显示模型不存在。

```
{
    "code": "InvalidParameter",
    "message": "Model not exist.",
    "request_id": "539f3cf9-9b9c-9a0f-988f-1829c7eb502f"
}
```

**原因及解决方案**：目前图像背景生成只有`wanx-background-generation-v2`这一个模型。如果需要切换V3模型，请设置`parameters.model_version`为v3，才能成功调用v3模型。

#### **使用文档中的示例图片报错提示需要提供RGBA模式的图片**

**报错场景**：如果您将文档的示例图片下载到本地，重新上传到自己的存储服务器，并使用新的图片链接发起请求。请求后报错提示图像格式是RGB格式，而不是RGBA格式。

```
{
    "request_id": "8f7d6829-281a-9270-944b-xxxxxx",
    "output": {
        "task_id": "72a2d266-6822-4165-a6e4-xxxxxx",
        "task_status": "FAILED",
        "submit_time": "2024-11-07 09:51:19.xxx",
        "scheduled_time": "2024-11-07 09:51:19.xxx",
        "end_time": "2024-11-07 09:51:20.xxx",
        "code": "BadRequest.UnsupportedFileFormat",
        "message": "Base image require RGBA format, but is RGB, modes concept see https://pillow.readthedocs.io/en/stable/handbook/concepts.html#concept-modes"
    },
    "usage": {
        "image_count": 0
    }
}
```

**主要原因**：存在主体图像、前景元素图像或背景元素图像不是RGBA图像的情况。在从文档示例链接下载图片至本地并再上传至存储服务的过程中，这些环节可能会改变原始的RGBA图像。可能出现的情况包括：图片下载至本地时保存的格式不支持透明度，例如.jpg、.jpeg等；上传至存储服务器时不支持RGBA格式；在使用工具进行图像编辑或转换时，未能保留图像透明度等。

**解决方案**：请参见[如何查看并获取RGBA图像](https://help.aliyun.com/zh/model-studio/image-background-generation#c456bddd3e6vy)。
