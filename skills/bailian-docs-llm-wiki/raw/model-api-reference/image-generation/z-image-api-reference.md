# Z-Image API参考

Z-Image 是一款轻量级文生图模型，可快速生成图像，支持中英文字渲染，并灵活适配多种分辨率与宽高比例。

**快速入口**：在线体验（[北京](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/model_experience_center/vision?currentTab=imageGenerate&modelId=z-image-turbo) | [新加坡](https://modelstudio.console.aliyun.com/ap-southeast-1?tab=dashboard#/efm/model_experience_center/vision?currentTab=imageGenerate&modelId=z-image-turbo)） | [技术博客](https://tongyi-mai.github.io/Z-Image-blog/)

## **效果展示**

**输入提示词**

**输出图像**

film grain, analog film texture, soft film lighting, Kodak Portra 400 style, cinematic grainy texture, photorealistic details, subtle noise, (film grain:1.2)。采用近景特写镜头拍摄的东亚年轻女性，呈现户外雪地场景。她体型纤瘦，呈站立姿势，身体微微向右侧倾斜，头部抬起看向画面上方，姿态自然放松。她的面部是典型东亚长相，肤色白皙，脸颊带有自然的红润感，五官清秀：眼睛是深棕色，眼型偏圆，眼神略带惊讶地望向上方，眼白部分可见；眉毛是深黑色，形状自然弯长；鼻子小巧挺直，嘴唇涂有红色口红，唇瓣微张，表情带着轻微的惊讶或好奇。她的头发是深黑色长直发，发丝被风吹得略显凌乱，部分垂在脸颊两侧，头顶佩戴一顶深灰色的头盔，头盔边缘露出少量发丝。服装是蓝白拼接的厚重外套，外套材质看起来是毛绒与布料结合，显得温暖厚实，适合雪地环境。背景是被白雪覆盖的户外场景，远处可见模糊的树木轮廓，天空是明亮的浅蓝色，带有少量白云，光线是强烈的自然日光，照亮人物面部与头发，形成清晰的光影，色调以蓝、白、黑为主，整体风格清新自然。画面顶部有黑色提示框，内有“**Press esc to exit full screen**”的白色文字。镜头的近景视角放大了人物的表情与细节，营造出户外雪地的真实氛围。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6915736671/p1036890.png)

## 模型概览

**模型名称**

**模型简介**

**输出图像规格**

z-image-turbo

轻量模型，快速生图

图像分辨率：总像素在\[512\*512, 2048\*2048\]之间，推荐分辨率请参见[size参数设置](#46b942a420o4e)

图像格式：png

图像张数：固定1张

**说明**

调用前，请查阅各地域支持的[模型列表](https://help.aliyun.com/zh/model-studio/models#b77c038c56b7y)。

## **前提条件**

您需要[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

## **HTTP同步调用**

**北京地域**：`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

**新加坡地域**：`POST https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

#### 请求参数

## **文生图**

以下示例直接返回图片，响应速度较快。

若想开启“智能思考”能力，请设置`prompt_extend=true` 。开启后，系统将在返回图片的同时，返回优化后的提示词及其推理过程，但会增加响应时间。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--data '{
    "model": "z-image-turbo",
    "input": {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "text": "film grain, analog film texture, soft film lighting, Kodak Portra 400 style, cinematic grainy texture, photorealistic details, subtle noise, (film grain:1.2)。采用近景特写镜头拍摄的东亚年轻女性，呈现户外雪地场景。她体型纤瘦，呈站立姿势，身体微微向右侧倾斜，头部抬起看向画面上方，姿态自然放松。她的面部是典型东亚长相，肤色白皙，脸颊带有自然的红润感，五官清秀：眼睛是深棕色，眼型偏圆，眼神略带惊讶地望向上方，眼白部分可见；眉毛是深黑色，形状自然弯长；鼻子小巧挺直，嘴唇涂有红色口红，唇瓣微张，表情带着轻微的惊讶或好奇。她的头发是深黑色长直发，发丝被风吹得略显凌乱，部分垂在脸颊两侧，头顶佩戴一顶深灰色的头盔，头盔边缘露出少量发丝。服装是蓝白拼接的厚重外套，外套材质看起来是毛绒与布料结合，显得温暖厚实，适合雪地环境。背景是被白雪覆盖的户外场景，远处可见模糊的树木轮廓，天空是明亮的浅蓝色，带有少量白云，光线是强烈的自然日光，照亮人物面部与头发，形成清晰的光影，色调以蓝、白、黑为主，整体风格清新自然。画面顶部有黑色提示框，内有“Press esc to exit full screen”的白色文字。镜头的近景视角放大了人物的表情与细节，营造出户外雪地的真实氛围。"
                    }
                ]
            }
        ]
    },
    "parameters": {
        "prompt_extend": false,
        "size": "1120*1440"
    }
}'
```

##### 请求头（Headers）

**Content-Type** `_string_` **（必选）**

请求内容类型。此参数必须设置为`application/json`。

**Authorization** `_string_`**（必选）**

请求身份认证。接口使用阿里云百炼API-Key进行身份认证。示例值：Bearer sk-xxxx。

##### 请求体（Request Body）

**model** `_string_` **（必选）**

模型名称。必须为：z-image-turbo。

**input** `_object_` **（必选）**

输入的基本信息。

**属性**

**messages** `_array_` **（必选）**

请求内容数组。当前**仅支持单轮对话**，即传入一组role、content参数，不支持多轮对话。

**属性**

**role** `_string_` **（必选）**

消息的角色。此参数必须设置为`user`。

**content** `_array_` **（必选）**

消息内容数组。必须包含且仅包含 **1 个 text 对象**。

**属性**

**text** `_string_` **（必选）**

正向提示词用于描述期望生成的图像内容、风格和构图。

支持中英文，长度不超过800个字符，每个汉字、字母、数字或符号计为一个字符，超过部分会自动截断。

示例值：一只坐着的橘黄色的猫，表情愉悦，活泼可爱，逼真准确。

**注意**：仅支持传入一个text，不传或传入多个将报错。

**parameters** `_object_` （可选）

图像处理参数。

**属性**

**size** `_string_` （可选）

输出图像的分辨率，格式为`**宽*高**`。

-   默认值：`1024*1536`。
    
-   总像素范围限制：总像素在 \[512\*512, 2048\*2048\]之间。
    
-   推荐分辨率范围：总像素在 \[1024\*1024, 1536\*1536\]之间，出图效果更佳。
    

示例值：1024\*1536。

**总像素为1024\*1024的推荐分辨率：**

-   1:1: 1024\*1024
    
-   2:3: 832\*1248
    
-   3:2: 1248\*832
    
-   3:4: 864\*1152
    
-   4:3: 1152\*864
    
-   7:9: 896\*1152
    
-   9:7: 1152\*896
    
-   9:16: 720\*1280
    
-   9:21: 576\*1344
    
-   16:9: 1280\*720
    
-   21:9：1344\*576
    

**总像素为1280\*1280的推荐分辨率：**

-   1:1: 1280\*1280
    
-   2:3: 1024\*1536
    
-   3:2: 1536\*1024
    
-   3:4: 1104\*1472
    
-   4:3: 1472\*1104
    
-   7:9: 1120\*1440
    
-   9:7: 1440\*1120
    
-   9:16: 864\*1536
    
-   9:21: 720\*1680
    
-   16:9: 1536\*864
    
-   21:9: 1680\*720
    

**总像素为1536\*1536的推荐分辨率：**

-   1:1：1536\*1536
    
-   2:3: 1248\*1872
    
-   3:2: 1872\*1248
    
-   3:4: 1296\*1728
    
-   4:3: 1728\*1296
    
-   7:9: 1344\*1728
    
-   9:7: 1728\*1344
    
-   9:16: 1152\*2048
    
-   9:21: 864\*2016
    
-   16:9: 2048\*1152
    
-   21:9: 2016\*864
    

**prompt\_extend** `_bool_` （可选）

**重要**

prompt\_extend直接影响费用。设为 `true` 时价格高于 `false`，具体见参见[模型价格](https://help.aliyun.com/zh/model-studio/model-pricing#6713612f55h4l)。

是否启用智能提示词（text）改写。开启后，将使用大模型优化提示词，并输出思考过程。

-   false：默认值，关闭智能改写。输出图像和原始文本提示词。
    
-   true：开启智能改写。输出图像、优化后的文本提示词、思考过程。
    

**seed** `_integer_` （可选）

随机数种子，取值范围`[0,2147483647]`。

使用相同的`seed`参数值可使生成内容保持相对稳定。若不提供，算法将自动使用随机数种子。

**注意**：模型生成过程具有概率性，即使使用相同的`seed`，也不能保证每次生成结果完全一致。

#### 响应参数

## 任务执行成功

任务数据（如任务状态、图像URL等）仅保留24小时，超时后会被自动清除。请您务必及时保存生成的图像。

```
{
    "output": {
        "choices": [
            {
                "finish_reason": "stop",
                "message": {
                    "content": [
                        {
                            "image": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx.png?Expires=xxx"
                        },
                        {
                            "text": "film grain, analog film texture, soft film lighting, Kodak Portra 400 style, cinematic grainy texture, photorealistic details, subtle noise, (film grain:1.2)。采用近景特写镜头拍摄的东亚年轻女性，呈现户外雪地场景。她体型纤瘦，呈站立姿势，身体微微向右侧倾斜，头部抬起看向画面上方，姿态自然放松。她的面部是典型东亚长相，肤色白皙，脸颊带有自然的红润感，五官清秀：眼睛是深棕色，眼型偏圆，眼神略带惊讶地望向上方，眼白部分可见；眉毛是深黑色，形状自然弯长；鼻子小巧挺直，嘴唇涂有红色口红，唇瓣微张，表情带着轻微的惊讶或好奇。她的头发是深黑色长直发，发丝被风吹得略显凌乱，部分垂在脸颊两侧，头顶佩戴一顶深灰色的头盔，头盔边缘露出少量发丝。服装是蓝白拼接的厚重外套，外套材质看起来是毛绒与布料结合，显得温暖厚实，适合雪地环境。背景是被白雪覆盖的户外场景，远处可见模糊的树木轮廓，天空是明亮的浅蓝色，带有少量白云，光线是强烈的自然日光，照亮人物面部与头发，形成清晰的光影，色调以蓝、白、黑为主，整体风格清新自然。画面顶部有黑色提示框，内有“Press esc to exit full screen”的白色文字。镜头的近景视角放大了人物的表情与细节，营造出户外雪地的真实氛围。"
                        }
                    ],
                    "reasoning_content": "",
                    "role": "assistant"
                }
            }
        ]
    },
    "usage": {
        "height": 1440,
        "image_count": 1,
        "input_tokens": 0,
        "output_tokens": 0,
        "total_tokens": 0,
        "width": 1120
    },
    "request_id": "8a0809b4-a796-47f4-a095-394b02b62xxx"
}
```

## 任务执行异常

如果因为某种原因导致任务执行失败，将返回相关信息，可以通过code和message字段明确指示错误原因。请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。

```
{
    "request_id": "a4d78a5f-655f-9639-8437-xxxxxx",
    "code": "InvalidParameter",
    "message": "num_images_per_prompt must be 1"
}
```

**output** `_object_`

任务输出信息。

**属性**

**choices** `_array_`

模型生成的输出内容。此数组仅包含1个元素。

**属性**

**finish\_reason** `_string_`

任务停止原因，正常完成时为 `stop`。

**message** `_object_`

模型返回的消息。

**属性**

**role** `_string_`

消息的角色，固定为`assistant`。

**content** `_array_`

**属性**

**image** `_string_`

生成图像的 URL，图像格式为PNG。**链接有效期为24小时**，请及时下载并保存图像。

**text** `_string_`

-   当prompt\_extend=false时，为输入的提示词。
    
-   当prompt\_extend=true时，为改写后的提示词。
    

**reasoning\_content** `_string_`

模型的思考过程，仅在prompt\_extend=true时返回思考文本。

**usage** `_object_`

输出信息统计。只对成功的结果计数。

**属性**

**width** `_integer_`

生成图像的宽度（像素）。

**height** `_integer_`

生成图像的高度（像素）。

**image\_count** `_integer_`

生成图像的数量，固定为1。

**input\_tokens** `_integer_`

输入token数量，prompt\_extend=false时固定为0。

**output\_tokens** `_integer_`

输出token数量，prompt\_extend=false时固定为0。

**output\_tokens\_details** `_object_`

输出 token 详情，仅当prompt\_extend=true时返回。

**属性**

**reasoning\_tokens** `_integer_`

推理思考使用的 token 数量。

**total\_tokens** `_integer_`

总token数量，prompt\_extend=false时固定为0。

**request\_id** `_string_`

请求唯一标识。可用于请求明细溯源和问题排查。

**code** `_string_`

请求失败的错误码。请求成功时不会返回此参数，详情请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。

**message** `_string_`

请求失败的详细信息。请求成功时不会返回此参数，详情请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。

## **使用限制**

-   图像`url`均只保留 24 小时，请及时下载。
    
-   **内容审核**：输入的 `prompt` 和输出的图像均会经过内容安全审核，包含违规内容的请求将报错“IPInfringementSuspect”或“DataInspectionFailed”，具体参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。
    

## **计费与限流**

-   模型免费额度和计费单价请参见[模型价格](https://help.aliyun.com/zh/model-studio/model-pricing#6713612f55h4l)。
    
-   模型限流请参见[Z-Image](https://help.aliyun.com/zh/model-studio/rate-limit#e17ad85fd8wwl)。
    
-   根据是否开启智能按成功生成的 **图像张数** 计费。模型调用失败或处理错误不产生任何费用，也不消耗[免费额度](https://help.aliyun.com/zh/model-studio/new-free-quota)。
    

## **错误码**

如果模型调用失败并返回报错信息，请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。

## **常见问题**

### **Q: 如何查看模型调用量？**

A: 模型调用完一小时后，请在[**模型监控**（北京）](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/model-telemetry)或[**模型监控**（新加坡）](https://modelstudio.console.aliyun.com/ap-southeast-1?tab=dashboard#/model-telemetry) 页面，查看模型的调用次数、成功率等指标。详情请参见[账单查询与成本管理](https://help.aliyun.com/zh/model-studio/bill-query-and-cost-management)。

### **Q：如何获取图像存储的访问域名白名单？**

A： 模型生成的图像存储于阿里云OSS，API将返回一个临时的公网URL。**若需要对该下载地址进行防火墙白名单配置**，请注意：由于底层存储会根据业务情况进行动态变更，为避免过期信息影响访问，文档不提供固定的OSS域名白名单。如有安全管控需求，请联系客户经理获取最新OSS域名列表。
