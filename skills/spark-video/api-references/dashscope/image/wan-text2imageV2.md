万相-文生图模型基于文本生成图像，支持多种艺术风格与写实摄影效果，满足多样化创意需求。

**快速入口：**在线体验（[北京](https://bailian.console.aliyun.com/?tab=model#/efm/model_experience_center/vision?currentTab=imageGenerate&modelId=qwen-image) | [新加坡](https://modelstudio.console.aliyun.com/?tab=dashboard#/efm/model_experience_center/vision?currentTab=imageGenerate)| [弗吉尼亚](https://modelstudio.console.aliyun.com/us-east-1?tab=dashboard#/efm/model_experience_center/vision?currentTab=imageGenerate&modelId=wan2.6-t2i)） | [万相官网](https://tongyi.aliyun.com/wan/generate/image/text-to-image) | [文生图使用指南](https://help.aliyun.com/zh/model-studio/text-to-image)

**说明**

万相官网的功能与API支持的能力可能存在差异。本文档以API的实际能力为准，并会随功能更新及时同步。

## 模型概览

| **模型名称** | **模型简介** | **输出图像格式** |
| --- | --- | --- |
| wan2.6-t2i `**推荐**` | 万相2.6 支持在总像素面积与宽高比约束内，自由选尺寸（同wan2.5） | 图像分辨率：总像素在\\[1280\\*1280, 1440\\*1440\\]之间 图像宽高比：\\[1:4, 4:1\\] 图像格式：png |
| wan2.5-t2i-preview `**推荐**` | 万相2.5 preview 支持在总像素面积与宽高比约束内，自由选尺寸 > 例如，支持768\\*2700，而2.2及以下版本单边上限 1400 |
| wan2.2-t2i-flash | 万相2.2极速版 较2.1模型速度提升50% | 图像分辨率：宽高均在\\[512, 1440\\]像素之间 图像格式：png |
| wan2.2-t2i-plus | 万相2.2专业版 较2.1模型稳定性与成功率全面提升 |
| wanx2.1-t2i-turbo | 万相2.1极速版 |
| wanx2.1-t2i-plus | 万相2.1专业版 |
| wanx2.0-t2i-turbo | 万相2.0极速版 |

**说明**

-   调用前，请查阅各地域支持的[模型列表](https://help.aliyun.com/zh/model-studio/models#b77c038c56b7y)。
    
-   **wan2.6模型**：支持[HTTP同步调用](#39337f0fd0wzt)、[HTTP异步调用](#9c68ccc525nta)、[Dashscope Python SDK调用](#b3d1dbc5dbtgx)和[Dashscope Java SDK调用](#e8a7f6d4c9xyz)。
    
-   **wan2.5及以下版本模型**：支持[HTTP异步调用](#0d8029dcc8pxl)、[Dashscope Python SDK调用](#7afdfdd68emtf)和[Dashscope Java SDK调用](#589b80853e6rn)，不支持HTTP同步调用。
    

## 前提条件

在调用前，先[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。如需通过SDK进行调用，请[安装DashScope SDK](https://help.aliyun.com/zh/model-studio/install-sdk)。

**重要**

北京、新加坡和弗吉尼亚地域拥有独立的 **API Key** 与**请求地址**，不可混用，跨地域调用将导致鉴权失败或服务报错，详情请参见[选择地域和服务部署范围](https://help.aliyun.com/zh/model-studio/regions/)。

## **HTTP同步调用（wan2.6）**

**重要**

本章节接口为**新版协议**，仅支持 **wan2.6**模型。

一次请求即可获得结果，流程简单，推荐大多数场景使用。

### 北京

`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

### 新加坡

`POST https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

### 弗吉尼亚

`POST https://dashscope-us.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

| #### 请求参数 | ## **文生图** ``` curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \\ --header 'Content-Type: application/json' \\ --header "Authorization: Bearer $DASHSCOPE_API_KEY" \\ --data '{ "model": "wan2.6-t2i", "input": { "messages": [ { "role": "user", "content": [ { "text": "一间有着精致窗户的花店，漂亮的木质门，摆放着花朵" } ] } ] }, "parameters": { "prompt_extend": true, "watermark": false, "n": 1, "negative_prompt": "", "size": "1280*1280" } }' ``` |
| --- | --- |
| ##### 请求头（Headers） |
| **Content-Type** `*string*` **（必选）** 请求内容类型。此参数必须设置为`application/json`。 |
| **Authorization** `*string*`**（必选）** 请求身份认证。接口使用阿里云百炼API-Key进行身份认证。示例值：Bearer sk-xxxx。 |
| ##### 请求体（Request Body） |
| **model** `*string*` **（必选）** 模型名称。示例值：wan2.6-t2i。 **说明** wan2.5及以下版本模型，HTTP调用请参见[HTTP异步调用](#0d8029dcc8pxl)。 |
| **input** `*object*` **（必选）** 输入的基本信息。 **属性** **messages** `*array*` **（必选）** 请求内容数组。当前**仅支持单轮对话**，即传入一组role、content参数，不支持多轮对话。 **属性** **role** `*string*` **（必选）** 消息的角色。此参数必须设置为`user`。 **content** `*array*` **（必选）** 消息内容数组。 **属性** **text** `*string*` **（必选）** 正向提示词，用于描述期望生成的图像内容、风格和构图。 支持中英文，长度不超过2100个字符，每个汉字、字母、数字或符号计为一个字符，超过部分会自动截断。 示例值：一只坐着的橘黄色的猫，表情愉悦，活泼可爱，逼真准确。 **注意**：仅支持传入一个text，不传或传入多个将报错。 |
| **parameters** `*object*` （可选） 图像处理参数。 **属性** **negative\\_prompt** `*string*` （可选） 反向提示词，用于描述不希望在图像中出现的内容，对画面进行限制。 支持中英文，长度不超过500个字符，超出部分将自动截断。 示例值：低分辨率，低画质，肢体畸形，手指畸形，画面过饱和，蜡像感，人脸无细节，过度光滑，画面具有AI感。构图混乱。文字模糊，扭曲。 **size** `*string*` （可选） 输出图像的分辨率，格式为`**宽*高**`。 - 默认值为 `1280*1280`。 - 总像素在 \\[1280\\*1280, 1440\\*1440\\] 之间且宽高比范围为 \\[1:4, 4:1\\]。例如，768\\*2700符合要求。 示例值：1280\\*1280。 **常见比例推荐的分辨率** - 1:1：1280\\*1280 - 3:4：1104\\*1472 - 4:3：1472\\*1104 - 9:16：960\\*1696 - 16:9：1696\\*960 **n** `*integer*` （可选） **重要** n直接影响费用。费用 = 单价 × 图片张数，请在调用前确认[模型价格](https://help.aliyun.com/zh/model-studio/model-pricing#0006b52b83ua9)。 生成图片的数量。取值范围为1~4张，默认为`4`。 注意：按张计费，测试建议设为 1。 **prompt\\_extend** `*bool*` （可选） 是否开启提示词智能改写。开启后，将使用大模型优化正向提示词，对较短的提示词有明显提升效果，但增加3-4秒耗时。 - true：默认值，开启智能改写。 - false：关闭智能改写。 **watermark** `*bool*` （可选） 是否添加水印标识，水印位于图片右下角，文案固定为“AI生成”。 - false：默认值，不添加水印。 - true：添加水印。 **seed** `*integer*` （可选） 随机数种子，取值范围`[0,2147483647]`。 使用相同的`seed`参数值可使生成内容保持相对稳定。若不提供，算法将自动使用随机数种子。 **注意**：模型生成过程具有概率性，即使使用相同的`seed`，也不能保证每次生成结果完全一致。 |

| #### 响应参数 | ## 任务执行成功 任务数据（如任务状态、图像URL等）仅保留24小时，超时后会被自动清除。请您务必及时保存生成的图像。 ``` { "output": { "choices": [ { "finish_reason": "stop", "message": { "content": [ { "image": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxxx.png?Expires=xxx", "type": "image" } ], "role": "assistant" } } ], "finished": true }, "usage": { "image_count": 1, "input_tokens": 0, "output_tokens": 0, "size": "1280*1280", "total_tokens": 0 }, "request_id": "815505c6-7c3d-49d7-b197-xxxxx" } ``` ## 任务执行异常 如果因为某种原因导致任务执行失败，将返回相关信息，可以通过code和message字段明确指示错误原因。请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。 ``` { "request_id": "a4d78a5f-655f-9639-8437-xxxxxx", "code": "InvalidParameter", "message": "num_images_per_prompt must be 1" } ``` |
| --- | --- |
| **output** `*object*` 任务输出信息。 **属性** **choices** `*array*` 模型生成的输出内容。 **属性** **finish\\_reason** `*string*` 任务停止原因，自然停止时为`stop`。 **message** `*object*` 模型返回的消息。 **属性** **role** `*string*` 消息的角色，固定为`assistant`。 **content** `*array*` **属性** **image** `*string*` 生成图像的 URL，图像格式为PNG。**链接有效期为24小时**，请及时下载并保存图像。 **type** `*string*` 输出的类型，固定为image。 **finished** `*boolean*` 任务是否结束。 - true：已结束。 - false：未结束。 |
| **usage** `*object*` 输出信息统计。只对成功的结果计数。 **属性** **image\\_count** `*integer*` 生成图像的张数。 **size** `*string*` 生成的图像分辨率。示例值：1280\\*1280。 **input\\_tokens** `*integer*` 输入token。文生图按图片张数计费，当前固定为0。 **output\\_tokens** `*integer*` 输出token。文生图按图片张数计费，当前固定为0。 **total\\_tokens** `*integer*` 总token。文生图按图片张数计费，当前固定为0。 |
| **request\\_id** `*string*` 请求唯一标识。可用于请求明细溯源和问题排查。 |
| **code** `*string*` 请求失败的错误码。请求成功时不会返回此参数，详情请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。 |
| **message** `*string*` 请求失败的详细信息。请求成功时不会返回此参数，详情请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。 |

## **HTTP异步调用（wan2.6）**

**重要**

本章节接口为**新版协议**，仅支持 **wan2.6**模型。

任务流程包含 **“创建任务 -> 轮询获取”** 两个核心步骤，具体如下：

### 步骤1：创建任务获取任务ID

#### 北京

`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/image-generation/generation`

#### 新加坡

`POST https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/image-generation/generation`

#### 弗吉尼亚

`POST https://dashscope-us.aliyuncs.com/api/v1/services/aigc/image-generation/generation`

**说明**

-   创建成功后，使用接口返回的 `task_id` 查询结果，task\_id 有效期为 24 小时。**请勿重复创建任务**，轮询获取即可。
    
-   新手指引请参见[Postman](https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api)。
    

| #### 请求参数 | ## **文生图** ``` curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image-generation/generation' \\ --header 'Content-Type: application/json' \\ --header "Authorization: Bearer $DASHSCOPE_API_KEY" \\ --header 'X-DashScope-Async: enable' \\ --data '{ "model": "wan2.6-t2i", "input": { "messages": [ { "role": "user", "content": [ { "text": "一间有着精致窗户的花店，漂亮的木质门，摆放着花朵" } ] } ] }, "parameters": { "prompt_extend": true, "watermark": false, "n": 1, "negative_prompt": "", "size": "1280*1280" } }' ``` |
| --- | --- |
| ##### 请求头（Headers） |
| **Content-Type** `*string*` **（必选）** 请求内容类型。此参数必须设置为`application/json`。 |
| **Authorization** `*string*`**（必选）** 请求身份认证。接口使用阿里云百炼API-Key进行身份认证。示例值：Bearer sk-xxxx。 |
| **X-DashScope-Async** `*string*` **（必选）** 异步处理配置参数。HTTP请求只支持异步，**必须设置为**`**enable**`。 **重要** 缺少此请求头将报错：“current user api does not support synchronous calls”。 |
| ##### 请求体（Request Body） |
| **model** `*string*` **（必选）** 模型名称。示例值：wan2.6-t2i。 **说明** wan2.5及以下版本模型，HTTP调用请参见[HTTP异步调用。](#0d8029dcc8pxl) |
| **input** `*object*` **（必选）** 输入的基本信息。 **属性** **messages** `*array*` **（必选）** 请求内容数组。当前**仅支持单轮对话**，即传入一组role、content参数，不支持多轮对话。 **属性** **role** `*string*` **（必选）** 消息的角色。此参数必须设置为`user`。 **content** `*array*` **（必选）** 消息内容数组。 **属性** **text** `*string*` **（必选）** 正向提示词，用于描述期望生成的图像内容、风格和构图。 支持中英文，长度不超过2100个字符，每个汉字、字母、数字或符号计为一个字符，超过部分会自动截断。 示例值：一间有着精致窗户的花店，漂亮的木质门，摆放着花朵。 **注意**：仅支持传入一个text，不传或传入多个将报错。 |
| **parameters** `*object*` （可选） 图像处理参数。 **属性** **negative\\_prompt** `*string*` （可选） 反向提示词，用于描述不希望在图像中出现的内容，对画面进行限制。 支持中英文，长度不超过500个字符，超出部分将自动截断。 示例值：低分辨率，低画质，肢体畸形，手指畸形，画面过饱和，蜡像感，人脸无细节，过度光滑，画面具有AI感。构图混乱。文字模糊，扭曲。 **size** `*string*` （可选） 输出图像的分辨率，格式为`**宽*高**`。 - 默认值为 `1280*1280`。 - 总像素在 \\[1280\\*1280, 1440\\*1440\\] 之间且宽高比范围为 \\[1:4, 4:1\\]。例如，768\\*2700符合要求。 示例值：1280\\*1280。 **常见比例推荐的分辨率** - 1:1：1280\\*1280 - 3:4：1104\\*1472 - 4:3：1472\\*1104 - 9:16：960\\*1696 - 16:9：1696\\*960 **n** `*integer*` （可选） **重要** n直接影响费用。费用 = 单价 × 图片张数，请在调用前确认[模型价格](https://help.aliyun.com/zh/model-studio/model-pricing#0006b52b83ua9)。 生成图片的数量。取值范围为1~4张，默认为`4`。 注意：按张计费，测试建议设为 1。 **prompt\\_extend** `*bool*` （可选） 是否开启prompt智能改写。开启后，将使用大模型优化正向提示词，对较短的提示词有明显提升效果，但增加3-4秒耗时。 - true：默认值，开启智能改写。 - false：不开启智能改写。 **watermark** `*bool*` （可选） 是否添加水印标识，水印位于图片右下角，文案固定为“AI生成”。 - false：默认值，不添加水印。 - true：添加水印。 **seed** `*integer*` （可选） 随机数种子，取值范围`[0,2147483647]`。 使用相同的`seed`参数值可使生成内容保持相对稳定。若不提供，算法将自动使用随机数种子。 **注意**：模型生成过程具有概率性，即使使用相同的`seed`，也不能保证每次生成结果完全一致。 |

| #### 响应参数 | ### 成功响应 请保存 task\\_id，用于查询任务状态与结果。 ``` { "output": { "task_status": "PENDING", "task_id": "0385dc79-5ff8-4d82-bcb6-xxxxxx" }, "request_id": "4909100c-7b5a-9f92-bfe5-xxxxxx" } ``` ### 异常响应 创建任务失败，请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。 ``` { "code": "InvalidApiKey", "message": "No API-key provided.", "request_id": "7438d53d-6eb8-4596-8835-xxxxxx" } ``` |
| --- | --- |
| **output** `*object*` 任务输出信息。 **属性** **task\\_id** `*string*` 任务ID。查询有效期24小时。 **task\\_status** `*string*` 任务状态。 **枚举值** - PENDING：任务排队中 - RUNNING：任务处理中 - SUCCEEDED：任务执行成功 - FAILED：任务执行失败 - CANCELED：任务已取消 - UNKNOWN：任务不存在或状态未知 |
| **request\\_id** `*string*` 请求唯一标识。可用于请求明细溯源和问题排查。 |
| **code** `*string*` 请求失败的错误码。请求成功时不会返回此参数，详情请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。 |     |
| **message** `*string*` 请求失败的详细信息。请求成功时不会返回此参数，详情请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。 |     |

### 步骤2：根据任务ID查询结果

#### 北京

`GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`

#### 新加坡

`GET https://dashscope-intl.aliyuncs.com/api/v1/tasks/{task_id}`

#### **弗吉尼亚**

`GET https://dashscope-us.aliyuncs.com/api/v1/tasks/{task_id}`

**说明**

-   **轮询建议**：图像生成过程耗时较长，建议采用**轮询**机制，并设置合理的查询间隔（如 10 秒）来获取结果。
    
-   **任务状态流转**：PENDING（排队中）→ RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。
    
-   **结果链接**：任务成功后返回图像链接，有效期为 **24 小时**。建议在获取链接后立即下载并转存至永久存储（如[阿里云 OSS](https://help.aliyun.com/zh/oss/user-guide/what-is-oss)）。
    
-   **RPS 限制**：查询接口默认RPS为20。如需更高频查询或事件通知，建议[配置异步任务回调](https://help.aliyun.com/zh/model-studio/async-task-api)。
    
-   **更多操作**：如需批量查询、取消任务等操作，请参见[管理异步任务](https://help.aliyun.com/zh/model-studio/manage-asynchronous-tasks#f26499d72adsl)。
    

| #### 请求参数 | ## 查询任务结果 将`{task_id}`完整替换为上一步接口返回的`task_id`的值。`task_id`查询有效期为24小时。 ``` curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id} \\ --header "Authorization: Bearer $DASHSCOPE_API_KEY" ``` |
| --- | --- |
| ##### **请求头（Headers）** |
| **Authorization** `*string*`**（必选）** 请求身份认证。接口使用阿里云百炼API-Key进行身份认证。示例值：Bearer sk-xxxx。 |
| ##### **URL路径参数（Path parameters）** |
| **task\\_id** `*string*`**（必选）** 任务ID。 |

| #### 响应参数 | ## 任务执行成功 任务数据（如任务状态、图像URL等）仅保留24小时，超时后会被自动清除。请您务必及时保存生成的图像。 ``` { "request_id": "2ddf53fa-699a-4267-9446-xxxxxx", "output": { "task_id": "3cd3fa4e-53ee-4136-9cab-xxxxxx", "task_status": "SUCCEEDED", "submit_time": "2025-12-18 20:03:01.802", "scheduled_time": "2025-12-18 20:03:01.834", "end_time": "2025-12-18 20:03:29.260", "finished": true, "choices": [ { "finish_reason": "stop", "message": { "role": "assistant", "content": [ { "image": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx.png?Expires=xxx", "type": "image" } ] } } ] }, "usage": { "size": "1280*1280", "total_tokens": 0, "image_count": 1, "output_tokens": 0, "input_tokens": 0 } } ``` ## 任务执行异常 如果因为某种原因导致任务执行失败，将返回相关信息，可以通过code和message字段明确指示错误原因。请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。 ``` { "code": "InvalidApiKey", "message": "No API-key provided.", "request_id": "7438d53d-6eb8-4596-8835-xxxxxx" } ``` |
| --- | --- |
| **output** `*object*` 任务输出信息。 **属性** **task\\_id** `*string*` 任务ID。查询有效期24小时。 **task\\_status** `*string*` 任务状态。 **枚举值** - PENDING：任务排队中 - RUNNING：任务处理中 - SUCCEEDED：任务执行成功 - FAILED：任务执行失败 - CANCELED：任务已取消 - UNKNOWN：任务不存在或状态未知 **轮询过程中的状态流转：** - PENDING（排队中） → RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。 - 初次查询状态通常为 PENDING（排队中）或 RUNNING（处理中）。 - 当状态变为 SUCCEEDED 时，响应中将包含生成的图像url。 - 若状态为 FAILED，请检查错误信息并重试。 **submit\\_time** `*string*` 任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。 **scheduled\\_time** `*string*` 任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。 **end\\_time** `*string*` 任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。 **finished** `*boolean*` 任务是否结束。 - true：已结束。 - false：未结束。 **choices** `*array*` 模型生成的输出内容。 **属性** **finish\\_reason** `*string*` 任务停止原因，正常完成时为 `stop`。 **message** `*object*` 模型返回的消息。 **属性** **role** `*string*` 消息的角色，固定为`assistant`。 **content** `*array*` **属性** **image** `*string*` 生成图像的 URL，图像格式为PNG。 **链接有效期为24小时**，请及时下载并保存图像。 **type** `*string*` 输出的类型，固定为image。 |
| **usage** `*object*` 输出信息统计。**只对成功的结果计数。** **属性** **image\\_count** `*integer*` 生成图像的张数。 **size** `*string*` 生成的图像分辨率。示例值：1280\\*1280。 **input\\_tokens** `*integer*` 输入token数量。当前固定为0。 **output\\_tokens** `*integer*` 输出token数量。当前固定为0。 **total\\_tokens** `*integer*` 总token数量。当前固定为0。 |
| **request\\_id** `*string*` 请求唯一标识。可用于请求明细溯源和问题排查。 |
| **code** `*string*` 请求失败的错误码。请求成功时不会返回此参数，详情请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。 |
| **message** `*string*` 请求失败的详细信息。请求成功时不会返回此参数，详情请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。 |

## **HTTP异步调用（wan2.5及以下版本模型）**

**重要**

此接口为**旧版协议**，仅支持**wan2.5及以下版本模型**。

由于文生图任务耗时较长（通常为1-2分钟），API采用异步调用。整个流程包含 **“创建任务 -> 轮询获取”** 两个核心步骤，具体如下：

> 具体耗时受限于排队任务数和服务执行情况，请在获取结果时耐心等待。

### 步骤1：创建任务获取任务ID

## 北京

`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis`

## 新加坡

`POST https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis`

**说明**

-   创建成功后，使用接口返回的 `task_id` 查询结果，task\_id 有效期为 24 小时。**请勿重复创建任务**，轮询获取即可。
    
-   新手指引请参见[Postman](https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api)。
    

| #### 请求参数 | ## 文生图 ``` curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis \\ -H 'X-DashScope-Async: enable' \\ -H "Authorization: Bearer $DASHSCOPE_API_KEY" \\ -H 'Content-Type: application/json' \\ -d '{ "model": "wan2.5-t2i-preview", "input": { "prompt": "一间有着精致窗户的花店，漂亮的木质门，摆放着花朵" }, "parameters": { "size": "1280*1280", "n": 1 } }' ``` ## 文生图（使用反向提示词） 通过 negative\\_prompt 指定生成的图片避免出现“人物”元素。 ``` curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis \\ -H 'X-DashScope-Async: enable' \\ -H "Authorization: Bearer $DASHSCOPE_API_KEY" \\ -H 'Content-Type: application/json' \\ -d '{ "model": "wan2.2-t2i-flash", "input": { "prompt": "雪地，白色小教堂，极光，冬日场景，柔和的光线。", "negative_prompt": "人物" }, "parameters": { "size": "1024*1024", "n": 1 } }' ``` |
| --- | --- |
| ##### 请求头（Headers） |
| **Content-Type** `*string*` **（必选）** 请求内容类型。此参数必须设置为`application/json`。 |
| **Authorization** `*string*`**（必选）** 请求身份认证。接口使用阿里云百炼API-Key进行身份认证。示例值：Bearer sk-xxxx。 |
| **X-DashScope-Async** `*string*` **（必选）** 异步处理配置参数。HTTP请求只支持异步，**必须设置为**`**enable**`。 **重要** 缺少此请求头将报错：“current user api does not support synchronous calls”。 |
| ##### 请求体（Request Body） |
| **model** `*string*` （必选） 模型名称。文生图模型请参见[模型列表](https://help.aliyun.com/zh/model-studio/wanx-image-edit-api-reference)。 示例值：wan2.5-t2i-preview。 **说明** wan2.6模型的HTTP调用请参见[HTTP同步调用](#39337f0fd0wzt)、[HTTP异步调用](#9c68ccc525nta)。 |
| **input** `*object*` （必选） 输入的基本信息，如提示词等。 **属性** **prompt** `*string*` **（必选）** 正向提示词，用来描述生成图像中期望包含的元素和视觉特点。 支持中英文，每个汉字/字母/标点符号占一个字符，超过部分会自动截断。长度限制因模型版本而异： - wan2.5-t2i-preview：长度不超过2000个字符。 - wan2.2、wan2.1系列模型：长度不超过500个字符。 - wanx2.0-t2i-turbo：长度不超过800个字符。 示例值：一只坐着的橘黄色的猫，表情愉悦，活泼可爱，逼真准确。 提示词的使用技巧请参见[文生图Prompt指南](https://help.aliyun.com/zh/model-studio/text-to-image-prompt)。 **negative\\_prompt** `*string*` （可选） 反向提示词，用来描述不希望在画面中看到的内容，可以对画面进行限制。 支持中英文，长度不超过500个字符，超过部分会自动截断。 示例值：低分辨率、错误、最差质量、低质量、残缺、多余的手指、比例不良等。 |
| **parameters** `*object*` （可选） 图像处理参数。如设置图像分辨率、开启prompt智能改写、添加水印等。 **属性** **size** `*string*` （可选） 输出图像的分辨率，格式为`**宽*高**`。默认值和约束因模型版本而异： - wan2.5-t2i-preview：默认值为 `1280*1280`。总像素在 \\[1280\\*1280, 1440\\*1440\\] 之间且宽高比范围为 \\[1:4, 4:1\\]。例如，768\\*2700符合要求。 - wan2.2及以下版本模型：默认值为`1024*1024`。图像宽高在\\[512, 1440\\]之间，最大分辨率为1440\\*1440。例如， 768\\*2700超单边限制，不支持。 示例值：1280\\*1280。 **常见比例推荐的分辨率** 以下分辨率适用于wan2.5-t2i-preview - 1:1：1280\\*1280 - 3:4：1104\\*1472 - 4:3：1472\\*1104 - 9:16：960\\*1696 - 16:9：1696\\*960 **n** `*integer*` （可选） **重要** n直接影响费用。费用 = 单价 × 图片张数，请在调用前确认[模型价格](https://help.aliyun.com/zh/model-studio/model-pricing#0006b52b83ua9)。 生成图片的数量。取值范围为1~4张，默认为`4`。测试阶段建议设置为1，便于低成本验证。 **prompt\\_extend** `*boolean*` （可选） 是否开启prompt智能改写。开启后使用大模型对输入prompt进行智能改写。对于较短的prompt生成效果提升明显，但会增加耗时。 - true：默认值，开启智能改写。 - false：关闭智能改写。 示例值：true。 **watermark** `*boolean*` （可选） 是否添加水印标识，水印位于图片右下角，文案固定为“AI生成”。 - false：默认值，不添加水印。 - true：添加水印。 **seed** `*integer*` （可选） 随机数种子，取值范围`[0,2147483647]`。 使用相同的`seed`参数值可使生成内容保持相对稳定。若不提供，算法将自动使用随机数种子。 **注意**：模型生成过程具有概率性，即使使用相同的`seed`，也不能保证每次生成结果完全一致。 |

| #### 响应参数 | ## 成功响应 请保存 task\\_id，用于查询任务状态与结果。 ``` { "output": { "task_status": "PENDING", "task_id": "0385dc79-5ff8-4d82-bcb6-xxxxxx" }, "request_id": "4909100c-7b5a-9f92-bfe5-xxxxxx" } ``` ## 异常响应 创建任务失败，请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。 ``` { "code": "InvalidApiKey", "message": "No API-key provided.", "request_id": "7438d53d-6eb8-4596-8835-xxxxxx" } ``` |
| --- | --- |
| **output** `*object*` 任务输出信息。 **属性** **task\\_id** `*string*` 任务ID。查询有效期24小时。 **task\\_status** `*string*` 任务状态。 **枚举值** - PENDING：任务排队中 - RUNNING：任务处理中 - SUCCEEDED：任务执行成功 - FAILED：任务执行失败 - CANCELED：任务已取消 - UNKNOWN：任务不存在或状态未知 |
| **request\\_id** `*string*` 请求唯一标识。可用于请求明细溯源和问题排查。 |
| **code** `*string*` 请求失败的错误码。请求成功时不会返回此参数，详情请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。 |
| **message** `*string*` 请求失败的详细信息。请求成功时不会返回此参数，详情请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。 |

### 步骤2：根据任务ID查询结果

#### **北京**

`GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`

#### 新加坡

`GET https://dashscope-intl.aliyuncs.com/api/v1/tasks/{task_id}`

**说明**

-   **轮询建议**：图像生成过程耗时较长，建议采用**轮询**机制，并设置合理的查询间隔（如 10 秒）来获取结果。
    
-   **任务状态流转**：PENDING（排队中）→ RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。
    
-   **结果链接**：任务成功后返回图像链接，有效期为 **24 小时**。建议在获取链接后立即下载并转存至永久存储（如[阿里云 OSS](https://help.aliyun.com/zh/oss/user-guide/what-is-oss)）。
    
-   **RPS 限制**：查询接口默认RPS为20。如需更高频查询或事件通知，建议[配置异步任务回调](https://help.aliyun.com/zh/model-studio/async-task-api)。
    
-   **更多操作**：如需批量查询、取消任务等操作，请参见[管理异步任务](https://help.aliyun.com/zh/model-studio/manage-asynchronous-tasks#f26499d72adsl)。
    

| #### 请求参数 | ## 查询任务结果 请将`86ecf553-d340-4e21-xxxxxxxxx`替换为真实的task\\_id。 > 若使用新加坡地域的模型，需将base\\_url替换为https://dashscope-intl.aliyuncs.com/api/v1/tasks/86ecf553-d340-4e21-xxxxxxxxx ``` curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/86ecf553-d340-4e21-xxxxxxxxx \\ --header "Authorization: Bearer $DASHSCOPE_API_KEY" ``` |
| --- | --- |
| ##### **请求头（Headers）** |
| **Authorization** `*string*`**（必选）** 请求身份认证。接口使用阿里云百炼API-Key进行身份认证。示例值：Bearer sk-xxxx。 |
| ##### **URL路径参数（Path parameters）** |
| **task\\_id** `*string*`**（必选）** 任务ID。 |

| #### **响应参数** | ## 任务执行成功 图像URL仅保留24小时，超时后会被自动清除，请及时保存生成的图像。 ``` { "request_id": "f767d108-7d50-908b-a6d9-xxxxxx", "output": { "task_id": "d492bffd-10b5-4169-b639-xxxxxx", "task_status": "SUCCEEDED", "submit_time": "2025-01-08 16:03:59.840", "scheduled_time": "2025-01-08 16:03:59.863", "end_time": "2025-01-08 16:04:10.660", "results": [ { "orig_prompt": "一间有着精致窗户的花店，漂亮的木质门，摆放着花朵", "actual_prompt": "一间有着精致雕花窗户的花店，漂亮的深色木质门上挂着铜制把手。店内摆放着各式各样的鲜花，包括玫瑰、百合和向日葵，色彩鲜艳，生机勃勃。背景是温馨的室内场景，透过窗户可以看到街道。高清写实摄影，中景构图。", "url": "https://dashscope-result-wlcb.oss-cn-wulanchabu.aliyuncs.com/1.png" } ], "task_metrics": { "TOTAL": 1, "SUCCEEDED": 1, "FAILED": 0 } }, "usage": { "image_count": 1 } } ``` ## 任务执行失败 若任务执行失败，task\\_status将置为 FAILED，并提供错误码和信息。请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。 ``` { "request_id": "e5d70b02-ebd3-98ce-9fe8-759d7d7b107d", "output": { "task_id": "86ecf553-d340-4e21-af6e-xxxxxx", "task_status": "FAILED", "code": "InvalidParameter", "message": "xxxxxx", "task_metrics": { "TOTAL": 4, "SUCCEEDED": 0, "FAILED": 4 } } } ``` ## 任务部分失败 模型可以在一次任务中生成多张图片。只要有一张图片生成成功，任务状态将标记为`SUCCEEDED`，并且返回相应的图像URL。对于生成失败的图片，结果中会返回相应的失败原因。同时在usage统计中，只会对成功的结果计数。请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。 ``` { "request_id": "85eaba38-0185-99d7-8d16-xxxxxx", "output": { "task_id": "86ecf553-d340-4e21-af6e-xxxxxx", "task_status": "SUCCEEDED", "results": [ { "url": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/123/a1.png" }, { "code": "InternalError.Timeout", "message": "An internal timeout error has occurred during execution, please try again later or contact service support." } ], "task_metrics": { "TOTAL": 2, "SUCCEEDED": 1, "FAILED": 1 } }, "usage": { "image_count": 1 } } ``` ## 任务查询过期 task\\_id查询有效期为 24 小时，超时后将无法查询，返回以下报错信息。 ``` { "request_id": "a4de7c32-7057-9f82-8581-xxxxxx", "output": { "task_id": "502a00b1-19d9-4839-a82f-xxxxxx", "task_status": "UNKNOWN" } } ``` |
| --- | --- |
| **output** `*object*` 任务输出信息。 **属性** **task\\_id** `*string*` 任务ID。查询有效期24小时。 **task\\_status** `*string*` 任务状态。 **枚举值** - PENDING：任务排队中 - RUNNING：任务处理中 - SUCCEEDED：任务执行成功 - FAILED：任务执行失败 - CANCELED：任务已取消 - UNKNOWN：任务不存在或状态未知 **轮询过程中的状态流转：** - PENDING（排队中） → RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。 - 初次查询状态通常为 PENDING（排队中）或 RUNNING（处理中）。 - 当状态变为 SUCCEEDED 时，响应中将包含生成的图像url。 - 若状态为 FAILED，请检查错误信息并重试。 **submit\\_time** `*string*` 任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。 **scheduled\\_time** `*string*` 任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。 **end\\_time** `*string*` 任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。 **results** `*array of object*` 任务结果列表，包括图像URL、prompt、部分任务执行失败报错信息等。 **数据结构** ``` { "results": [ { "orig_prompt": "", "actual_prompt": "", "url": "" }, { "code": "", "message": "" } ] } ``` **属性** **orig\\_prompt** `*string*` 原始输入的prompt，对应请求参数`prompt`。 **actual\\_prompt** `*string*` 开启 prompt 智能改写后，返回实际使用的优化后 prompt。若未开启该功能，则不返回此字段。 **url** `*string*` 图像URL地址。仅在 task\\_status 为 SUCCEEDED 时返回。链接有效期24小时，可通过此URL下载图像。 **code** `*string*` 请求失败的错误码。请求成功时不会返回此参数，详情请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。 **message** `*string*` 请求失败的详细信息。请求成功时不会返回此参数，详情请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。 **task\\_metrics** `*object*` 任务结果统计。 **属性** **TOTAL** `*integer*` 总的任务数。 **SUCCEEDED** `*integer*` 任务状态为成功的任务数。 **FAILED** `*integer*` 任务状态为失败的任务数。 **code** `*string*` 请求失败的错误码。请求成功时不会返回此参数，详情请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。 **message** `*string*` 请求失败的详细信息。请求成功时不会返回此参数，详情请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。 |
| **usage** `*object*` 输出信息统计。只对成功的结果计数。 **属性** **image\\_count** `*integer*` 模型成功生成图片的数量。计费公式：费用 = 图片数量 × 单价。 |
| **request\\_id** `*string*` 请求唯一标识。可用于请求明细溯源和问题排查。 |

## **DashScope Python SDK调用**

SDK 的参数命名与HTTP接口基本一致，参数结构根据语言特性进行封装。

由于文生图任务耗时较长，SDK 在底层封装了 HTTP 异步调用流程，支持同步、异步两种调用方式。

> 具体耗时受限于排队任务数和服务执行情况，请在获取结果时耐心等待。

### **wan2.6**

**重要**

-   以下代码仅适合 **wan2.6** 模型。
    
-   请确保 DashScope Python SDK 版本**不低于** `**1.25.7**`，再运行以下代码。更新请参考[安装SDK](https://help.aliyun.com/zh/model-studio/install-sdk)。
    

各地域的`base_url`和 API Key 不通用，以下示例以北京地域为例进行调用：

#### **北京**

`https://dashscope.aliyuncs.com/api/v1`

#### 新加坡

`https://dashscope-intl.aliyuncs.com/api/v1`

#### 弗吉尼亚

`https://dashscope-us.aliyuncs.com/api/v1`

## 同步调用

##### **请求示例**

```
import os
import dashscope
from dashscope.aigc.image_generation import ImageGeneration
from dashscope.api_entities.dashscope_response import Message

# 以下为北京地域url，各地域的base_url不同
dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
api_key = os.getenv("DASHSCOPE_API_KEY")

message = Message(
    role="user",
    content=[
        {
            'text': '一间有着精致窗户的花店，漂亮的木质门，摆放着花朵'
        }
    ]
)
print("----sync call, please wait a moment----")
rsp = ImageGeneration.call(
    model="wan2.6-t2i",
    api_key=api_key,
    messages=[message],
    negative_prompt="",
    prompt_extend=True,
    watermark=False,
    n=1,
    size="1280*1280"
)
print(rsp)
```

##### 响应示例

> url 有效期24小时，请及时下载图像。

```
{
    "status_code": 200,
    "request_id": "820dd0db-eb42-4e05-8d6a-1ddb4axxxxxx",
    "code": "",
    "message": "",
    "output": {
        "text": null,
        "finish_reason": null,
        "choices": [
            {
                "finish_reason": "stop",
                "message": {
                    "role": "assistant",
                    "content": [
                        {
                            "image": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxxxxx.png?Expires=xxxxxx",
                            "type": "image"
                        }
                    ]
                }
            }
        ],
        "audio": null,
        "finished": true
    },
    "usage": {
        "input_tokens": 0,
        "output_tokens": 0,
        "characters": 0,
        "image_count": 1,
        "size": "1280*1280",
        "total_tokens": 0
    }
}
```

## 异步调用

##### **请求示例**

```
import os
import dashscope
from dashscope.aigc.image_generation import ImageGeneration
from dashscope.api_entities.dashscope_response import Role, Message
from http import HTTPStatus

# 以下为北京地域url，各地域的base_url不同
dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
api_key = os.getenv("DASHSCOPE_API_KEY")

# 创建异步任务
def create_async_task():
    print("Creating async task...")
    message = Message(
        role="user",
        content=[{'text': '一间有着精致窗户的花店，漂亮的木质门，摆放着花朵'}]
    )
    response = ImageGeneration.async_call(
        model="wan2.6-t2i",
        api_key=api_key,
        messages=[message],
        negative_prompt="",
        prompt_extend=True,
        watermark=False,
        n=1,
        size="1280*1280"
    )
    
    if response.status_code == 200:
        print("Task created successfully:", response)
        return response
    else:
        raise Exception(f"Failed to create task: {response.code} - {response.message}")

# 等待任务完成
def wait_for_completion(task_response):
    print("Waiting for task completion...")
    status = ImageGeneration.wait(task=task_response, api_key=api_key)
    
    if status.output.task_status == "SUCCEEDED":
        print("Task succeeded!")
        print("Response:", status)
    else:
        raise Exception(f"Task failed with status: {status.output.task_status}")

# 获取异步任务信息
def fetch_task_status(task):
    print("Fetching task status...")
    status = ImageGeneration.fetch(task=task, api_key=api_key)
    
    if status.status_code == HTTPStatus.OK:
        print("Task status:", status.output.task_status)
        print("Response details:", status)
    else:
        print(f"Failed to fetch status: {status.code} - {status.message}")

# 取消异步任务
def cancel_task(task):
    print("Canceling task...")
    response = ImageGeneration.cancel(task=task, api_key=api_key)
    
    if response.status_code == HTTPStatus.OK:
        print("Task canceled successfully:", response.output.task_status)
    else:
        print(f"Failed to cancel task: {response.code} - {response.message}")

# 主执行流程
if __name__ == "__main__":
    task = create_async_task()
    wait_for_completion(task)
```

##### 响应示例

1、创建任务的响应示例

```
{
    "status_code": 200,
    "request_id": "c4f11410-ea42-4996-957d-9c82f9xxxxxx",
    "code": "",
    "message": "",
    "output": {
        "text": null,
        "finish_reason": null,
        "choices": null,
        "audio": null,
        "task_id": "f470bbfd-d955-4165-935b-d35b8eexxxxxx",
        "task_status": "PENDING"
    },
    "usage": {
        "input_tokens": 0,
        "output_tokens": 0,
        "characters": 0
    }
}
```

2、查询任务结果的响应示例

> url 有效期24小时，请及时下载图像。

```
{
    "status_code": 200,
    "request_id": "7e57e7e8-00b0-4534-9aff-fe31e0xxxxxx",
    "code": null,
    "message": "",
    "output": {
        "text": null,
        "finish_reason": null,
        "choices": [
            {
                "finish_reason": "stop",
                "message": {
                    "role": "assistant",
                    "content": [
                        {
                            "image": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxxxxx.png?Expires=xxxxxx",
                            "type": "image"
                        }
                    ]
                }
            }
        ],
        "audio": null,
        "task_id": "f470bbfd-d955-4165-935b-d35b8exxxxxx",
        "task_status": "SUCCEEDED",
        "submit_time": "2026-01-09 17:18:17.901",
        "scheduled_time": "2026-01-09 17:18:17.941",
        "end_time": "2026-01-09 17:18:45.544",
        "finished": true
    },
    "usage": {
        "input_tokens": 0,
        "output_tokens": 0,
        "characters": 0,
        "size": "1280*1280",
        "total_tokens": 0,
        "image_count": 1
    }
}
```

### **wan2.5及以下版本模型**

**重要**

-   以下代码仅适合wan2.5及以下版本模型。
    
-   请确保 DashScope Python SDK 版本**不低于** `**1.25.2**`，再运行以下代码。
    
    若版本过低，可能会触发 “url error, please check url!” 等错误。请参考[安装SDK](https://help.aliyun.com/zh/model-studio/install-sdk)进行更新。
    

各地域的`base_url`和 API Key 不通用，以下示例以北京地域为例进行调用：

#### 北京

`https://dashscope.aliyuncs.com/api/v1`

#### 新加坡

`https://dashscope-intl.aliyuncs.com/api/v1`

## 同步调用

##### **请求示例**

```
from http import HTTPStatus
from urllib.parse import urlparse, unquote
from pathlib import PurePosixPath
import requests
from dashscope import ImageSynthesis
import os
import dashscope

# 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1
dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
api_key = os.getenv("DASHSCOPE_API_KEY")

print('----sync call, please wait a moment----')
rsp = ImageSynthesis.call(api_key=api_key,
                          model="wan2.5-t2i-preview",
                          prompt="一间有着精致窗户的花店，漂亮的木质门，摆放着花朵",
                          negative_prompt="",
                          n=1,
                          size='1280*1280',
                          prompt_extend=True,
                          watermark=False,
                          seed=12345)
print('response: %s' % rsp)
if rsp.status_code == HTTPStatus.OK:
    # 在当前目录下保存图片
    for result in rsp.output.results:
        file_name = PurePosixPath(unquote(urlparse(result.url).path)).parts[-1]
        with open('./%s' % file_name, 'wb+') as f:
            f.write(requests.get(result.url).content)
else:
    print('sync_call Failed, status_code: %s, code: %s, message: %s' %
          (rsp.status_code, rsp.code, rsp.message))
```

##### 响应示例

> url 有效期24小时，请及时下载图像。

```
{
    "status_code": 200,
    "request_id": "9d634fda-5fe9-9968-a908-xxxxxx",
    "code": null,
    "message": "",
    "output": {
        "task_id": "d35658e4-483f-453b-b8dc-xxxxxx",
        "task_status": "SUCCEEDED",
        "results": [{
            "url": "https://dashscope-result-wlcb.oss-cn-wulanchabu.aliyuncs.com/1.png",
            "orig_prompt": "一间有着精致窗户的花店，漂亮的木质门，摆放着花朵",
            "actual_prompt": "一间精致的花店，窗户上装饰着优雅的雕花，漂亮的木质门上挂着铜制把手。店内摆放着各种色彩鲜艳的花朵，如玫瑰、郁金香和百合等。背景是温馨的室内场景，光线柔和，营造出宁静舒适的氛围。高清写实摄影，近景中心构图。"
        }],
        "submit_time": "2025-01-08 19:36:01.521",
        "scheduled_time": "2025-01-08 19:36:01.542",
        "end_time": "2025-01-08 19:36:13.270",
        "task_metrics": {
            "TOTAL": 1,
            "SUCCEEDED": 1,
            "FAILED": 0
        }
    },
    "usage": {
        "image_count": 1
    }
}
```

## 异步调用

##### 请求示例

```
from http import HTTPStatus
from urllib.parse import urlparse, unquote
from pathlib import PurePosixPath
import requests
from dashscope import ImageSynthesis
import os
import dashscope

# 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1
dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
api_key = os.getenv("DASHSCOPE_API_KEY")


def async_call():
    print('----create task----')
    task_info = create_async_task()
    print('----wait task done then save image----')
    wait_async_task(task_info)


# 创建异步任务
def create_async_task():
    rsp = ImageSynthesis.async_call(api_key=api_key,
                                    model="wan2.5-t2i-preview",
                                    prompt="一间有着精致窗户的花店，漂亮的木质门，摆放着花朵",
                                    negative_prompt="",
                                    n=1,
                                    size='1280*1280',
                                    prompt_extend=True,
                                    watermark=False,
                                    seed=12345)
    print(rsp)
    if rsp.status_code == HTTPStatus.OK:
        print(rsp.output)
    else:
        print('Failed, status_code: %s, code: %s, message: %s' %
              (rsp.status_code, rsp.code, rsp.message))
    return rsp


# 等待异步任务结束
def wait_async_task(task):
    rsp = ImageSynthesis.wait(task=task, api_key=api_key)
    print(rsp)
    if rsp.status_code == HTTPStatus.OK:
        print(rsp.output)
        # save file to current directory
        for result in rsp.output.results:
            file_name = PurePosixPath(unquote(urlparse(result.url).path)).parts[-1]
            with open('./%s' % file_name, 'wb+') as f:
                f.write(requests.get(result.url).content)
    else:
        print('Failed, status_code: %s, code: %s, message: %s' %
              (rsp.status_code, rsp.code, rsp.message))


# 获取异步任务信息
def fetch_task_status(task):
    status = ImageSynthesis.fetch(task=task, api_key=api_key)
    print(status)
    if status.status_code == HTTPStatus.OK:
        print(status.output.task_status)
    else:
        print('Failed, status_code: %s, code: %s, message: %s' %
              (status.status_code, status.code, status.message))


# 取消异步任务，只有处于PENDING状态的任务才可以取消
def cancel_task(task):
    rsp = ImageSynthesis.cancel(task=task, api_key=api_key)
    print(rsp)
    if rsp.status_code == HTTPStatus.OK:
        print(rsp.output.task_status)
    else:
        print('Failed, status_code: %s, code: %s, message: %s' %
              (rsp.status_code, rsp.code, rsp.message))


if __name__ == '__main__':
    async_call()
```

##### 响应示例

1、创建任务的响应示例

```
{
	"status_code": 200,
	"request_id": "31b04171-011c-96bd-ac00-f0383b669cc7",
	"code": "",
	"message": "",
	"output": {
		"task_id": "4f90cf14-a34e-4eae-xxxxxxxx",
		"task_status": "PENDING",
		"results": []
	},
	"usage": null
}
```

2、查询任务结果的响应示例

> url 有效期24小时，请及时下载图像。

```
{
    "status_code": 200,
    "request_id": "9d634fda-5fe9-9968-a908-xxxxxx",
    "code": null,
    "message": "",
    "output": {
        "task_id": "d35658e4-483f-453b-b8dc-xxxxxx",
        "task_status": "SUCCEEDED",
        "results": [{
            "url": "https://dashscope-result-wlcb.oss-cn-wulanchabu.aliyuncs.com/xxx.png",
            "orig_prompt": "一间有着精致窗户的花店，漂亮的木质门，摆放着花朵",
            "actual_prompt": "一间精致的花店，窗户上装饰着优雅的雕花，漂亮的木质门上挂着铜制把手。店内摆放着各种色彩鲜艳的花朵，如玫瑰、郁金香和百合等。背景是温馨的室内场景，光线柔和，营造出宁静舒适的氛围。高清写实摄影，近景中心构图。"
        }],
        "submit_time": "2025-01-08 19:36:01.521",
        "scheduled_time": "2025-01-08 19:36:01.542",
        "end_time": "2025-01-08 19:36:13.270",
        "task_metrics": {
            "TOTAL": 1,
            "SUCCEEDED": 1,
            "FAILED": 0
        }
    },
    "usage": {
        "image_count": 1
    }
}
```

## DashScope Java SDK调用

SDK 的参数命名与HTTP接口基本一致，参数结构根据语言特性进行封装。

由于文生图任务耗时较长，SDK 在底层封装了 HTTP 异步调用流程，支持同步、异步两种调用方式。

> 具体耗时受限于排队任务数和服务执行情况，请在获取结果时耐心等待。

### **wan2.6**

**重要**

-   以下代码仅适合 **wan2.6-t2i** 模型。
    
-   请确保 DashScope Java SDK 版本**不低于** `**2.22.6**`，再运行以下代码。
    

各地域的`base_url`和 API Key 不通用，以下示例以北京地域为例进行调用：

#### **北京**

`https://dashscope.aliyuncs.com/api/v1`

#### 新加坡

`https://dashscope-intl.aliyuncs.com/api/v1`

#### 弗吉尼亚

`https://dashscope-us.aliyuncs.com/api/v1`

## 同步调用

##### **请求示例**

```
import com.alibaba.dashscope.aigc.imagegeneration.*;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;
import com.alibaba.dashscope.utils.JsonUtils;
import java.util.Collections;

public class Main {

    static {
        // 以下为北京地域url，各地域的base_url不同
        Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
    }

    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey="sk-xxx"
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    public static void basicCall() throws ApiException, NoApiKeyException, UploadFileException {
        ImageGenerationMessage message = ImageGenerationMessage.builder()
                .role("user")
                .content(Collections.singletonList(
                        Collections.singletonMap("text", "一间有着精致窗户的花店，漂亮的木质门，摆放着花朵")
                )).build();

        ImageGenerationParam param = ImageGenerationParam.builder()
                .apiKey(apiKey)
                .model("wan2.6-t2i")
                .n(1)
                .size("1280*1280")
                .negativePrompt("")
                .promptExtend(true)
                .watermark(false)
                .messages(Collections.singletonList(message))
                .build();

        ImageGeneration imageGeneration = new ImageGeneration();
        ImageGenerationResult result = null;
        try {
            System.out.println("---sync call, please wait a moment----");
            result = imageGeneration.call(param);
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            throw new RuntimeException(e.getMessage());
        }
        System.out.println(JsonUtils.toJson(result));
    }

    public static void main(String[] args) {
        try {
            basicCall();
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
    }
}
```

##### 响应示例

> url 有效期24小时，请及时下载图像。

```
{
    "status_code": 200,
    "request_id": "50b57166-eaaa-4f17-b1e0-35a5ca88672c",
    "code": "",
    "message": "",
    "output": {
        "choices": [
            {
                "finish_reason": "stop",
                "message": {
                    "role": "assistant",
                    "content": [
                        {
                            "image": "https://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/xxx.png?Expires=xxx",
                            "type": "image"
                        }
                    ]
                }
            }
        ],
        "finished": true
    },
    "usage": {
        "input_tokens": 0,
        "output_tokens": 0,
        "image_count": 1,
        "size": "1280*1280",
        "total_tokens": 0
    }
}
```

## 异步调用

##### **请求示例**

```
import com.alibaba.dashscope.aigc.imagegeneration.*;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;
import com.alibaba.dashscope.utils.JsonUtils;
import java.util.Collections;

public class Main {

    static {
        // 以下为北京地域url，各地域的base_url不同
        Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
    }

    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey="sk-xxx"
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    public static void asyncCall() throws ApiException, NoApiKeyException, UploadFileException {
        ImageGenerationMessage message = ImageGenerationMessage.builder()
                .role("user")
                .content(Collections.singletonList(
                        Collections.singletonMap("text", "一间有着精致窗户的花店，漂亮的木质门，摆放着花朵")
                )).build();

        ImageGenerationParam param = ImageGenerationParam.builder()
                .apiKey(apiKey)
                .model("wan2.6-t2i")
                .n(1)
                .size("1280*1280")
                .negativePrompt("")
                .promptExtend(true)
                .watermark(false)
                .messages(Collections.singletonList(message))
                .build();

        ImageGeneration imageGeneration = new ImageGeneration();
        ImageGenerationResult result = null;
        try {
            System.out.println("---async call, creating task----");
            result = imageGeneration.asyncCall(param);
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            throw new RuntimeException(e.getMessage());
        }
        System.out.println(JsonUtils.toJson(result));

        String taskId = result.getOutput().getTaskId();
        // 等待任务完成
        waitTask(taskId);
    }

    public static void waitTask(String taskId) throws ApiException, NoApiKeyException {
        ImageGeneration imageGeneration = new ImageGeneration();
        ImageGenerationResult result = imageGeneration.wait(taskId, apiKey);
        System.out.println(JsonUtils.toJson(result));
    }

    public static void main(String[] args) {
        try {
            asyncCall();
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
    }
}
```

##### 响应示例

1、创建任务的响应示例

```
{
    "status_code": 200,
    "request_id": "9cd85950-2e26-4b2c-b562-1694cf9288e5",
    "code": "",
    "message": "",
    "output": {
        "task_id": "4c861fbe-af89-4a2f-8fc5-4bb15c3139ba",
        "task_status": "PENDING"
    },
    "usage": null
}
```

2、查询任务结果的响应示例

> url 有效期24小时，请及时下载图像。

```
{
    "status_code": 200,
    "request_id": "cbdf1424-306e-4a52-82f3-8bf5d8a99103",
    "code": "",
    "message": "",
    "output": {
        "choices": [
            {
                "finish_reason": "stop",
                "message": {
                    "role": "assistant",
                    "content": [
                        {
                            "image": "https://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/xxx.png?Expires=xxx",
                            "type": "image"
                        }
                    ]
                }
            }
        ],
        "task_id": "4c861fbe-af89-4a2f-8fc5-4bb15c3139ba",
        "task_status": "SUCCEEDED",
        "submit_time": "2026-01-16 16:36:06.556",
        "scheduled_time": "2026-01-16 16:36:06.591",
        "end_time": "2026-01-16 16:36:25.190",
        "finished": true
    },
    "usage": {
        "input_tokens": 0,
        "output_tokens": 0,
        "size": "1280*1280",
        "total_tokens": 0,
        "image_count": 1
    }
}
```

### wan2.5及以下版本模型

**重要**

-   以下代码仅适合wan2.5及以下版本模型。
    
-   请确保 DashScope Java SDK 版本**不低于** `**2.22.2**`，再运行以下代码。
    
    若版本过低，可能会触发 “url error, please check url!” 等错误。请参考[安装SDK](https://help.aliyun.com/zh/model-studio/install-sdk)进行更新。
    

各地域的`base_url`和 API Key 不通用，以下示例以北京地域为例进行调用：

#### 北京

`https://dashscope.aliyuncs.com/api/v1`

#### 新加坡

`https://dashscope-intl.aliyuncs.com/api/v1`

## 同步调用

##### 请求示例

```
// Copyright (c) Alibaba, Inc. and its affiliates.

import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesis;
import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisListResult;
import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisParam;
import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisResult;
import com.alibaba.dashscope.task.AsyncTaskListParam;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.Constants;
import com.alibaba.dashscope.utils.JsonUtils;

import java.util.HashMap;
import java.util.Map;

public class Main {

    static {
        // 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1
        Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
    }

    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey="sk-xxx"
    // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    static String apiKey = System.getenv("DASHSCOPE_API_KEY");


    public static void basicCall() throws ApiException, NoApiKeyException {
        // 设置parameters参数
        Map<String, Object> parameters = new HashMap<>();
        parameters.put("prompt_extend", true);
        parameters.put("watermark", false);
        parameters.put("seed", 12345);

        ImageSynthesisParam param =
                ImageSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("wan2.5-t2i-preview")
                        .prompt("一间有着精致窗户的花店，漂亮的木质门，摆放着花朵")
                        .n(1)
                        .size("1280*1280")
                        .negativePrompt("")
                        .parameters(parameters)
                        .build();

        ImageSynthesis imageSynthesis = new ImageSynthesis();
        ImageSynthesisResult result = null;
        try {
            System.out.println("---sync call, please wait a moment----");
            result = imageSynthesis.call(param);
        } catch (ApiException | NoApiKeyException e){
            throw new RuntimeException(e.getMessage());
        }
        System.out.println(JsonUtils.toJson(result));
    }

    public static void listTask() throws ApiException, NoApiKeyException {
        ImageSynthesis is = new ImageSynthesis();
        AsyncTaskListParam param = AsyncTaskListParam.builder().build();
        param.setApiKey(apiKey);
        ImageSynthesisListResult result = is.list(param);
        System.out.println(result);
    }

    public static void fetchTask(String taskId) throws ApiException, NoApiKeyException {
        ImageSynthesis is = new ImageSynthesis();
        // If set DASHSCOPE_API_KEY environment variable, apiKey can null.
        ImageSynthesisResult result = is.fetch(taskId, apiKey);
        System.out.println(result.getOutput());
        System.out.println(result.getUsage());
    }

    public static void main(String[] args){
        try{
            basicCall();
            //listTask();
        }catch(ApiException|NoApiKeyException e){
            System.out.println(e.getMessage());
        }
    }
}
```

##### 响应示例

> url 有效期24小时，请及时下载图像。

```
{
    "request_id": "22f9c744-206c-9a78-899a-xxxxxx",
    "output": {
        "task_id": "4a0f8fc6-03fb-4c44-a13a-xxxxxx",
        "task_status": "SUCCEEDED",
        "results": [{
           "orig_prompt": "一间有着精致窗户的花店，漂亮的木质门，摆放着花朵",
            "actual_prompt": "一间有着精致雕花窗户的花店，漂亮的深色木质门微微敞开。店内摆放着各式各样的鲜花，包括玫瑰、百合和向日葵，色彩鲜艳，香气扑鼻。背景是温馨的室内场景，光线柔和，透过窗户洒在花朵上。高清写实摄影，中景构图。",
            "url": "https://dashscope-result-wlcb.oss-cn-wulanchabu.aliyuncs.com/1.png"
        }],
        "task_metrics": {
            "TOTAL": 1,
            "SUCCEEDED": 1,
            "FAILED": 0
        }
    },
    "usage": {
        "image_count": 1
    }
}
```

## 异步调用

##### 请求示例

```
// Copyright (c) Alibaba, Inc. and its affiliates.

import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesis;
import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisParam;
import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.Constants;
import com.alibaba.dashscope.utils.JsonUtils;

import java.util.HashMap;
import java.util.Map;

public class Main {

    static {
        // 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1
        Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
    }

    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey="sk-xxx"
    // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    String apiKey = System.getenv("DASHSCOPE_API_KEY");

    public void asyncCall() {
        System.out.println("---create task----");
        String taskId = this.createAsyncTask();
        System.out.println("---wait task done then return image url----");
        this.waitAsyncTask(taskId);
    }


    /**
     * 创建异步任务
     * @return taskId
     */
    public String createAsyncTask() {
        // 设置parameters参数
        Map<String, Object> parameters = new HashMap<>();
        parameters.put("prompt_extend", true);
        parameters.put("watermark", false);
        parameters.put("seed", 12345);

        ImageSynthesisParam param =
                ImageSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("wan2.5-t2i-preview")
                        .prompt("一间有着精致窗户的花店，漂亮的木质门，摆放着花朵")
                        .n(1)
                        .size("1280*1280")
                        .negativePrompt("")
                        .parameters(parameters)
                        .build();

        ImageSynthesis imageSynthesis = new ImageSynthesis();
        ImageSynthesisResult result = null;
        try {
            result = imageSynthesis.asyncCall(param);
        } catch (Exception e){
            throw new RuntimeException(e.getMessage());
        }
        System.out.println(JsonUtils.toJson(result));
        String taskId = result.getOutput().getTaskId();
        System.out.println("taskId=" + taskId);
        return taskId;
    }


    /**
     * 等待异步任务结束
     * @param taskId 任务id
     * */
    public void waitAsyncTask(String taskId) {
        ImageSynthesis imageSynthesis = new ImageSynthesis();
        ImageSynthesisResult result = null;
        try {
            //环境变量配置后，可在这里将apiKey设置为null
            result = imageSynthesis.wait(taskId, apiKey);
        } catch (ApiException | NoApiKeyException e){
            throw new RuntimeException(e.getMessage());
        }
        System.out.println(JsonUtils.toJson(result));
        System.out.println(JsonUtils.toJson(result.getOutput()));
    }


    public static void main(String[] args){
        Main main = new Main();
        main.asyncCall();
    }

}
```

##### 响应示例

1、创建任务的响应示例

```
{
	"request_id": "5dbf9dc5-4f4c-9605-85ea-542f97709ba8",
	"output": {
		"task_id": "7277e20e-aa01-4709-xxxxxxxx",
		"task_status": "PENDING"
	}
}
```

2、查询任务结果的响应示例

```
{
    "request_id": "22f9c744-206c-9a78-899a-xxxxxx",
    "output": {
        "task_id": "4a0f8fc6-03fb-4c44-a13a-xxxxxx",
        "task_status": "SUCCEEDED",
        "results": [{
           "orig_prompt": "一间有着精致窗户的花店，漂亮的木质门，摆放着花朵",
            "actual_prompt": "一间有着精致雕花窗户的花店，漂亮的深色木质门微微敞开。店内摆放着各式各样的鲜花，包括玫瑰、百合和向日葵，色彩鲜艳，香气扑鼻。背景是温馨的室内场景，光线柔和，透过窗户洒在花朵上。高清写实摄影，中景构图。",
            "url": "https://dashscope-result-wlcb.oss-cn-wulanchabu.aliyuncs.com/1.png"
        }],
        "task_metrics": {
            "TOTAL": 1,
            "SUCCEEDED": 1,
            "FAILED": 0
        }
    },
    "usage": {
        "image_count": 1
    }
}
```

## **使用限制**

-   **数据时效**：任务`task_id`和 图像`url`均只保留 24 小时，过期后将无法查询或下载。
    
-   **内容审核**：输入的 `prompt` 和输出的图像均会经过内容安全审核，包含违规内容的请求将报错“IPInfringementSuspect”或“DataInspectionFailed”，具体参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。
    

## **计费与限流**

-   模型免费额度和计费单价请参见[模型列表](https://help.aliyun.com/zh/model-studio/models)。
    
-   模型限流请参见[万相](https://help.aliyun.com/zh/model-studio/rate-limit#513e0a3df24v7)。
    
-   计费说明：按成功生成的 **图像张数** 计费。模型调用失败或处理错误不产生任何费用，也不消耗[新人免费额度](https://help.aliyun.com/zh/model-studio/new-free-quota)。
    

## **错误码**

如果模型调用失败并返回报错信息，请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。

## **常见问题**

**Q: 如何查看模型的推理费用和调用量？**

A: 详情请参见[账单查询与成本管理](https://help.aliyun.com/zh/model-studio/bill-query-and-cost-management)。

/\* 调整 table 宽度 \*/ .aliyun-docs-content table.medium-width { max-width: 1018px; width: 100%; } .aliyun-docs-content table.table-no-border tr td:first-child { padding-left: 0; } .aliyun-docs-content table.table-no-border tr td:last-child { padding-right: 0; } /\* 支持吸顶 \*/ div:has(.aliyun-docs-content), .aliyun-docs-content .markdown-body { overflow: visible; } .stick-top { position: sticky; top: 46px; } /\*\*代码块字体\*\*/ /\* 减少表格中的代码块 margin，让表格信息显示更紧凑 \*/ .unionContainer .markdown-body table .help-code-block { margin: 0 !important; } /\* 减少表格中的代码块字号，让表格信息显示更紧凑 \*/ .unionContainer .markdown-body .help-code-block pre { font-size: 12px !important; } /\* 减少表格中的代码块字号，让表格信息显示更紧凑 \*/ .unionContainer .markdown-body .help-code-block pre code { font-size: 12px !important; } /\*\* API Reference 表格 \*\*/ .aliyun-docs-content table.api-reference tr td:first-child { margin: 0px; border-bottom: 1px solid #d8d8d8; } .aliyun-docs-content table.api-reference tr:last-child td:first-child { border-bottom: none; } .aliyun-docs-content table.api-reference p { color: #6e6e80; } .aliyun-docs-content table.api-reference b, i { color: #181818; } .aliyun-docs-content table.api-reference .collapse { border: none; margin-top: 4px; margin-bottom: 4px; } .aliyun-docs-content table.api-reference .collapse .expandable-title-bold { padding: 0; } .aliyun-docs-content table.api-reference .collapse .expandable-title { padding: 0; } .aliyun-docs-content table.api-reference .collapse .expandable-title-bold .title { margin-left: 16px; } .aliyun-docs-content table.api-reference .collapse .expandable-title .title { margin-left: 16px; } .aliyun-docs-content table.api-reference .collapse .expandable-title-bold i.icon { position: absolute; color: #777; font-weight: 100; } .aliyun-docs-content table.api-reference .collapse .expandable-title i.icon { position: absolute; color: #777; font-weight: 100; } .aliyun-docs-content table.api-reference .collapse.expanded .expandable-content { padding: 10px 14px 10px 14px !important; margin: 0; border: 1px solid #e9e9e9; } .aliyun-docs-content table.api-reference .collapse .expandable-title-bold b { font-size: 13px; font-weight: normal; color: #6e6e80; } .aliyun-docs-content table.api-reference .collapse .expandable-title b { font-size: 13px; font-weight: normal; color: #6e6e80; } .aliyun-docs-content table.api-reference .tabbed-content-box { border: none; } .aliyun-docs-content table.api-reference .tabbed-content-box section { padding: 8px 0 !important; } .aliyun-docs-content table.api-reference .tabbed-content-box.mini .tab-box { /\* position: absolute; left: 40px; right: 0; \*/ } .aliyun-docs-content .margin-top-33 { margin-top: 33px !important; } .aliyun-docs-content .two-codeblocks pre { max-height: calc(50vh - 136px) !important; height: auto; } .expandable-content section { border-bottom: 1px solid #e9e9e9; padding-top: 6px; padding-bottom: 4px; } .expandable-content section:last-child { border-bottom: none; } .expandable-content section:first-child { padding-top: 0; }

/\* 让表格显示成类似钉钉文档的分栏卡片 \*/ table.help-table-card td { border: 10px solid #FFF !important; background: #F4F6F9; padding: 16px !important; vertical-align: top; } /\* 减少表格中的代码块 margin，让表格信息显示更紧凑 \*/ .unionContainer .markdown-body table .help-code-block { margin: 0 !important; } /\* 减少表格中的代码块字号，让表格信息显示更紧凑 \*/ .unionContainer .markdown-body .help-code-block pre { font-size: 12px !important; } /\* 减少表格中的代码块字号，让表格信息显示更紧凑 \*/ .unionContainer .markdown-body .help-code-block pre code { font-size: 12px !important; } /\* 表格中的引用上下间距调小，避免内容显示过于稀疏 \*/ .unionContainer .markdown-body table blockquote { margin: 4px 0 0 0; }