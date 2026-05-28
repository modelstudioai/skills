# 千问-图像翻译API参考

Qwen-MT-Image 可精准识别并翻译图像中的文字，同时保留原始排版。支持领域提示、敏感词过滤、术语干预等自定义功能。

**重要**

本文档仅适用于[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)，必须使用对应的[API Key](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/api-key)。

## 模型概览

![1](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6962921671/p1007156.webp)

源语种：中文

![2](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6962921671/p1006389.webp)

英文

![3](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6962921671/p1006396.webp)

日文

![4](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6962921671/p1006438.webp)

韩语

![es](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6962921671/p1006451.webp)

西班牙语

![fr](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6962921671/p1006452.webp)

法语

**模型名称**

**模型简介**

**输出图像规格**

qwen-mt-image

千问图像翻译模型，支持中文或英文与其他语种之间的互译，不支持两个非中、英语种之间的直接翻译（例如，从日语翻译为韩语）。详见[支持的语种](#d2aa4b03d2kco)。

图片格式：JPG

## 前提条件

您需要已[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

## HTTP调用

`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis`

HTTP API 采用异步模式，调用流程分两步：

1.  **创建任务获取任务ID**：发送一个请求创建任务，该请求会返回**任务ID（task\_id）**。
    
2.  **根据任务ID查询结果**：使用task\_id轮询任务状态，直到任务完成并获得图像URL。
    

### 步骤1：创建任务获取任务ID

**说明**

-   创建成功后，使用接口返回的 `task_id` 查询结果，task\_id 有效期为 24 小时。**请勿重复创建任务**，轮询获取即可。
    
-   新手指引请参见[Postman](https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api)。
    

#### 请求参数

## 图像翻译

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
--header 'X-DashScope-Async: enable' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "qwen-mt-image",
    "input": {
        "image_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250916/ordhsk/1.webp",
        "source_lang": "zh",
        "target_lang": "en",
        "ext": {
            "config": {
                "imageSegment": false
            }
        }
    }
}'
```

##### 请求头（Headers）

**Content-Type** `_string_` **（必选）**

请求内容类型。此参数必须设置为`application/json`。

**Authorization** `_string_`**（必选）**

请求身份认证。接口使用阿里云百炼API-Key进行身份认证。示例值：Bearer sk-xxxx。

**X-DashScope-Async** `_string_` **（必选）**

异步处理配置参数。HTTP请求只支持异步，**必须设置为**`**enable**`。

**重要**

缺少此请求头将报错：“current user api does not support synchronous calls”。

##### 请求体（Request Body）

**model** `_string_` **（必选）**

模型名称，必须设置为`qwen-mt-image`。

**input** `_object_` **（必选）**

输入参数对象，包含以下字段：

**属性**

**image\_url** `_string_` **（必选）**

图像的公网可访问的URL，支持 HTTP 和 HTTPS 协议。如需获取本地文件的公网URL，请参见[上传文件获取临时URL](https://help.aliyun.com/zh/model-studio/get-temporary-file-url) 。

-   **格式限制**：JPG、JPEG、PNG、BMP、PNM、PPM、TIFF、WEBP
    
-   **尺寸限制**：图像的宽度和高度均需在15-8192像素范围内，宽高比在1:10至10:1范围内。
    
-   **大小限制**：不超过100MB
    
-   URL地址中不能包含中文字符。
    
-   **示例**：`https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250916/ordhsk/1.webp`
    

**source\_lang** `_string_` **（必选）**

[源语种](#d2aa4b03d2kco)。

-   **支持值**：语种全称、语种编码或`auto`（自动检测），对大小写不敏感
    
-   **限制**：与`target_lang`不同，且至少有一项为中文或英文
    
-   **示例**：`Chinese`、`en`、`auto`
    

**target\_lang** `_string_` **（必选）**

[目标语种](#d2aa4b03d2kco)。

-   **支持值**：语种全称或语种编码，对大小写不敏感
    
-   **限制**：与`source_lang`不同，且至少有一项为中文或英文
    
-   **示例**：`Chinese`、`en`
    

**ext** `_object_` （可选）

可选拓展字段。

**属性**

**domainHint** `_string_` （可选）

领域提示，为使译文风格更贴合特定领域，可以使用英文描述使用场景、译文风格等需求。

为确保翻译效果，建议不超过200个英文单词。

**重要**

领域提示语句当前**只支持英文**。

**示例：**These sentences are from seller-buyer conversations on a B2C ecommerce platform. Translate them into clear, engaging customer service language, ensuring the translation is appropriate for handling potential issues or disputes.

**sensitives** `_array_` （可选）

配置敏感词，以在翻译前过滤图片中**完全匹配**的文本，**对大小写敏感**。

敏感词的语种可与源语种不一致，支持全部的[源语种](#ffcebd6c57dfn)和[目标语种](#d2aa4b03d2kco)。为确保翻译效果，建议单次请求添加的敏感词不超过50个。

**示例：**\["全场9折", "七天无理由退换"\]

**terminologies** `_array_` （可选）

术语干预，为特定术语设定译文，以满足特定领域的翻译需求，术语对的语种需要与`source_lang`和`target_lang`对应。

**属性**

**src** `_string_` **（必选）**

术语的源文本，语种需要与源语种`source_lang`一致。

**tgt** `_string_` **（必选）**

术语的目标文本，语种需要与目标语种`target_lang`一致。

**示例**：\[{"src": "应用程序接口", "tgt": "API"}, {"src": "机器学习", "tgt": "ML"}\]

**config** `_object_` （可选）

**属性**

**imageSegment** `_bool_` （可选）

是否开启图像主体分割。开启后，将跳过对图像中主体（如人物、商品、Logo）上文字的翻译。

-   `false`：（默认值）翻译图像中的所有文字。
    
-   `true`：不翻译图像主体的文字。
    

> **注意**：旧版本参数名为`skipImgSegment`（是否跳过图像主体分割）。为保持兼容，该参数仍受支持，但建议使用新的 `imageSegment`参数。

#### 响应参数

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
    "code": "InvalidApiKey",
    "message": "No API-key provided.",
    "request_id": "7438d53d-6eb8-4596-8835-xxxxxx"
}
```

**output** `_object_`

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

**message** `_string_`

请求失败的详细信息。请求成功时不会返回此参数，详情请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。

**code** `_string_`

请求失败的错误码。请求成功时不会返回此参数，详情请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。

### 步骤2：根据任务ID查询结果

`GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`

**说明**

-   `task_id` 有效期为**24小时**，若ID不存在或已过期，任务状态将返回 `UNKNOWN`。
    
-   任务成功后返回的 `url`有效期为**24小时**，请及时下载并保存图像。
    
-   此查询接口的默认RPS为1。如需更高频次的查询或事件通知，请[配置异步任务回调](https://help.aliyun.com/zh/model-studio/async-task-api)。
    
-   如需批量查询或取消任务，请参见[管理异步任务](https://help.aliyun.com/zh/model-studio/manage-asynchronous-tasks#f26499d72adsl)。
    

#### 请求参数

## 查询任务结果

您需要将`86ecf553-d340-4e21-xxxxxxxxx`替换为真实的task\_id。

```
curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/86ecf553-d340-4e21-xxxxxxxxx \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

##### **请求头（Headers）**

**Authorization** `_string_`**（必选）**

请求身份认证。接口使用阿里云百炼API-Key进行身份认证。示例值：Bearer sk-xxxx。

##### **URL路径参数（Path parameters）**

**task\_id** `_string_`**（必选）**

任务ID。

#### **响应参数**

## 任务执行成功-存在可翻译内容

任务数据（如任务状态、图像URL等）仅保留24小时，超时后会被自动清除。请您务必及时保存生成的图像。

```
{
    "request_id": "5fec62eb-bf94-91f8-b9f4-f7f758e4e27e",
    "output": {
        "task_id": "72c52225-8444-4cab-ad0c-xxxxxx",
        "task_status": "SUCCEEDED",
        "submit_time": "2025-08-13 18:11:16.954",
        "scheduled_time": "2025-08-13 18:11:17.003",
        "end_time": "2025-08-13 18:11:23.860",
        "image_url": "http://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx?Expires=xxx"
    },
    "usage": {
        "image_count":1
    }
}
```

## 任务执行成功-无可翻译内容

在图像中无可翻译文本（例如，在识别出图像主体后，其余部分无文字）时，**任务仍会成功并正常计费**，但会返回`No text detected for translation`的提示。

```
{
    "request_id": "0ccb84aa-e034-431d-9d54-08e14fxxxxxx",
    "output": {
        "task_id": "34ec4208-97d6-498b-a390-9173f7xxxxxx",
        "task_status": "SUCCEEDED",
        "submit_time": "2026-01-12 17:56:23.625",
        "scheduled_time": "2026-01-12 17:56:23.656",
        "end_time": "2026-01-12 17:56:25.324",
        "image_url": "http://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx.jpg?Expires=xxx",
        "message": "No text detected for translation"
    },
    "usage": {
        "image_count": 1
    }
}
```

## 任务执行失败

若任务执行失败，task\_status将置为 FAILED，并提供错误码和信息。请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。

```
{
    "request_id": "daad9007-6acd-9fb3-a6bc-d55902b9c9ff",
    "output": {
        "task_id": "fe8aa114-d9f1-4f76-b598-xxxxxx",
        "task_status": "FAILED",
        "submit_time": "2025-08-20 09:54:21.911",
        "scheduled_time": "2025-08-20 09:54:21.984",
        "end_time": "2025-08-20 12:55:00.818",
        "code": "InternalError",
        "message": "xxxxxx"
    }
}
```

**output** `_object_`

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

**image\_url** `_string_`

模型生成图像的URL地址，与原图长宽相同，JPG格式。有效期为24小时，请及时下载并保存图像。

**code** `_string_`

请求失败的错误码。请求成功时不会返回此参数，详情请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。

**message** `_string_`

请求失败的详细信息，详情请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。

通常请求成功时不会返回此参数，仅在图像中无可翻译文本（例如，在分割图像主体后，其余部分无文字）时，**任务仍会成功并正常计费**，但会返回`No text detected for translation`的提示。

**usage** `_object_`

输出信息统计。只对成功的结果计数。

**属性**

**image\_count** `_integer_`

模型生成图像的数量，固定为1。

**request\_id** `_string_`

请求唯一标识。可用于请求明细溯源和问题排查。

## 支持的语种

源语种或目标语种**至少有一种必须是中文或英文**，不支持两个非中、英语种之间的直接翻译（例如，从日语翻译为韩语）。若不确定源语种，可将 `source_lang` 设置为 `auto` 进行自动检测。

**语种（中文名）**

**英文全称**

**编码**

**支持作为源语种**

**支持作为目标语种**

简体中文

Chinese

zh

支持

支持

英文

English

en

支持

支持

韩语

Korean

ko

支持

支持

日语

Japanese

ja

支持

支持

俄语

Russian

ru

支持

支持

西班牙语

Spanish

es

支持

支持

法语

French

fr

支持

支持

葡萄牙语

Portuguese

pt

支持

支持

意大利语

Italian

it

支持

支持

德语

German

de

支持

不支持

越南语

Vietnamese

vi

支持

支持

马来语

Malay

ms

不支持

支持

泰语

Thai

th

不支持

支持

印尼语

Indonesian

id

不支持

支持

阿拉伯语

Arabian

ar

不支持

支持

## 计费与限流

-   免费额度和计费单价请参见[模型价格](https://help.aliyun.com/zh/model-studio/model-pricing#a3250eda6bgjx)。
    
-   限流规则请参见[限流](https://help.aliyun.com/zh/model-studio/rate-limit#f812e7c63axvx)。
    
-   按成功生成的**图像张数**计费。调用失败或处理出错不产生费用，也不消耗[新人免费额度](https://help.aliyun.com/zh/model-studio/new-free-quota)。
    
-   若图像中无可翻译文本，或启用主体分割后非主体部分无文字，**任务仍记为成功并正常计费**，接口会返回 `No text detected for translation`。
    

## **错误码**

如果模型调用失败并返回报错信息，请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。

## 常见问题

#### Q：为什么图中的内容没有被翻译？

启用了[主体分割](#245ec24fe92ls)功能后，模型不翻译图像中人物、商品、Logo 等主体上的文字。如需翻译所有文字，将 `ext.config.imageSegment` 设置为 `false` 即可。

#### Q：如何将临时图像链接转为永久链接？

临时链接无法直接转为永久链接。通过后端服务下载图像，再上传至对象存储（如阿里云 OSS），即可获取永久链接。

**示例代码：下载图像到本地**

```
import requests

def download_and_save_image(image_url, save_path):
    try:
        response = requests.get(image_url, stream=True, timeout=300) # 设置超时
        response.raise_for_status() # 如果 HTTP 状态码不是 200，则抛出异常
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"图像已成功下载到: {save_path}")
        # 此处可接上传至永久存储的逻辑
    except requests.exceptions.RequestException as e:
        print(f"图像下载失败: {e}")

if __name__ == '__main__':
    image_url = "http://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx?Expires=xxx"
    save_path = "image-translation.jpg"
    download_and_save_image(image_url, save_path)
```

### **Q: 如何查看模型调用量？**

A: 模型调用完一小时后，请在[**模型监控**（北京）](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/model-telemetry)或[**模型监控**（新加坡）](https://modelstudio.console.aliyun.com/ap-southeast-1?tab=dashboard#/model-telemetry) 页面，查看模型的调用次数、成功率等指标。详情请参见[账单查询与成本管理](https://help.aliyun.com/zh/model-studio/bill-query-and-cost-management)。

### **Q：如何获取图像存储的访问域名白名单？**

A： 模型生成的图像存储于阿里云OSS，API将返回一个临时的公网URL。**若需要对该下载地址进行防火墙白名单配置**，请注意：由于底层存储会根据业务情况进行动态变更，为避免过期信息影响访问，文档不提供固定的OSS域名白名单。如有安全管控需求，请联系客户经理获取最新OSS域名列表。
