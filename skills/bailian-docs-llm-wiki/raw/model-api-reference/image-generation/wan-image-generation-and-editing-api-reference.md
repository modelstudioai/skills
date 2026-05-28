# 万相-图像生成与编辑2.7 API参考

万相2.7图像生成与编辑模型支持文生图、文生组图、图生组图、图像编辑和多图参考生成。

## 模型概览

**模型名称**

**模型简介**

**输出图像规格**

wan2.7-image-pro

万相2.7 image专业版，文生图（非组图生成）支持4K高清输出

图片格式：PNG。

图像分辨率和尺寸请参见[size参数](https://help.aliyun.com/zh/model-studio/wan-image-generation-api-reference#wan27-param-size-section)。

wan2.7-image

万相2.7 image，生成速度更快

**说明**

调用前，请查阅各地域支持的[模型列表与价格](https://help.aliyun.com/zh/model-studio/model-pricing#e2540d71a2utl)。

## 前提条件

您需要已[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

**重要**

北京和新加坡地域拥有独立的 **API Key** 与**请求地址**，不可混用，跨地域调用将导致鉴权失败或服务报错。

## **HTTP同步调用**

一次请求即可获得结果，流程简单，推荐大多数场景使用。

## **北京**

`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

## **新加坡**

`POST https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

#### 请求参数

## 文生图

> wan2.7-image-pro仅文生图场景支持4K分辨率，图像编辑和组图生成支持最高2K分辨率

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--data '{
    "model": "wan2.7-image-pro",
    "input": {
        "messages": [
            {
                "role": "user",
                "content": [
                    {"text": "一间有着精致窗户的花店，漂亮的木质门，摆放着花朵"}
                ]
            }
        ]
    },
    "parameters": {
        "size": "2K",
        "n": 1,
        "watermark": false,
        "thinking_mode": true
    }
}'
```

## **图像编辑**

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--data '{
    "model": "wan2.7-image-pro",
    "input": {
        "messages": [
            {
                "role": "user",
                "content": [
                    {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/pjeqdf/car.webp"},
                    {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/xsunlm/paint.webp"},
                    {"text": "把图2的涂鸦喷绘在图1的汽车上"}
                ]
            }
        ]
    },
    "parameters": {
        "size": "2K",
        "n": 1,
        "watermark": false
    }
}'
```

## **交互式编辑**

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--data '{
    "model": "wan2.7-image-pro",
    "input": {
        "messages": [
            {
                "role": "user",
                "content": [
                    {"image": "https://img.alicdn.com/imgextra/i3/O1CN0157XGE51l6iL9441yX_!!6000000004770-49-tps-1104-1472.webp"},
                    {"image": "https://img.alicdn.com/imgextra/i3/O1CN01SfG4J41UYn9WNt4X1_!!6000000002530-49-tps-1696-960.webp"},
                    {"text": "把图1的闹钟放在图2的框选的位置，保持场景和光线融合自然"}
                ]
            }
        ]
    },
    "parameters": {
        "bbox_list": [[],[[989, 515, 1138, 681]]],
        "size": "2K",
        "n": 1,
        "watermark": false
    }
}'
```

## **组图生成**

> wan2.7-image-pro组图生成仅支持最高2K分辨率。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--data '{
    "model": "wan2.7-image-pro",
    "input": {
        "messages": [
            {
                "role": "user",
                "content": [
                    {"text": "电影感组图，记录同一只流浪橘猫，特征必须前后一致。第一张：春天，橘猫穿梭在盛开的樱花树下；第二张：夏天，橘猫在老街的树荫下乘凉避暑；第三张：秋天，橘猫踩在满地的金色落叶上；第四张：冬天，橘猫在雪地上走留下足迹。"}
                ]
            }
        ]
    },
    "parameters": {
        "enable_sequential": true,
        "n": 4,
        "size": "2K"
    }
}'
```

##### 请求头（Headers）

**Content-Type** `_string_` **（必选）**

请求内容类型。此参数必须设置为`application/json`。

**Authorization** `_string_`**（必选）**

请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。

##### 请求体（Request Body）

**model** `_string_` **（必选）**

模型名称。可选值：`wan2.7-image-pro`、`wan2.7-image`。

**input** `_object_` **（必选）**

输入的基本信息。

**属性**

**messages** `_array_` **（必选）**

请求内容数组。当前**仅支持单轮对话**，即传入一组role、content参数，不支持多轮对话。

**属性**

**role** `_string_` **（必选）**

消息的角色。此参数固定设置为`user`。

**content** `_array_` **（必选）**

消息内容数组。

**属性**

**text** `_string_`

用户输入提示词。支持中英文，长度不超过5000个字符，每个汉字、字母、数字或符号计为一个字符，超过部分会自动截断。

**image** `_string_`

输入图像的URL或Base64编码字符串。

图像限制：

-   图像格式：JPEG、JPG、PNG（不支持透明通道）、BMP、WEBP。
    
-   图像分辨率：图像的宽高范围均为\[240, 8000\]像素，宽高比范围\[1:8, 8:1\]。
    
-   文件大小：不超过20MB。
    

图像数量限制：

-   可传入0-9张图片。
    
-   当输入多张图像时，需在`content`数组中传入多个`image`对象，并按照数组顺序定义图像顺序。
    

支持的输入格式：

1.  使用公网可访问URL
    
    -   支持HTTP或HTTPS协议。
        
    -   示例值：`http://wanx.alicdn.com/material/xxx.jpeg`。
        
2.  传入 Base64 编码图像后的字符串
    
    -   格式：data:{MIME\_type};base64,{base64\_data}
        
    -   示例：data:image/jpeg;base64,GDU7MtCZzEbTbmRZ...（仅示意，实际需传入完整字符串）
        
    -   Base64 编码规范请参见[图像传入方式](https://help.aliyun.com/zh/model-studio/wan-image-edit#8db0e2215frua)。
        

**parameters** `_object_` （可选）

模型参数配置。

**属性**

**bbox\_list** `_array[array[array[integer]]]_` （可选）

交互式编辑框选区域。

-   对应关系：列表长度必须与输入图片数量一致。若某张图片无需编辑，请在对应位置传入空列表 `[]`。
    
-   坐标格式：`[x1, y1, x2, y2]`（左上角 x, 左上角 y, 右下角 x, 右下角 y），使用原图绝对像素坐标，左上角坐标为（0，0）。
    
-   限制条件：单张图片最多支持 2 个边界框。
    

示例：输入 3 张图片，其中第 2 张无框选，第 1 张有两个框选：

```
[
  [[0, 0, 12, 12], [25, 25, 100, 100]],  # 图 1 (2个框)
  [],                                    # 图 2 (无框)
  [[10, 10, 50, 50]]                    # 图 3 (1个框)
]
```

**enable\_sequential** `_boolean_` （可选）

控制生图模式：

-   false：默认值。
    
-   true ：启用组图输出模式。
    

**size** `_string_` （可选）

关于输出图片分辨率参数，支持以下两种方式，不可混用：

**模型：wan2.7-image-pro**

-   **方式一：指定输出图片的分辨率（推荐）**
    
    -   支持 1K、2K（默认）、4K 三种规格
        
    -   **适用范围**：
        
        -   文生图（无图片输入，非组图生成）：支持1K、2K、4K。
            
        -   其他场景：支持1K、2K。
            
    -   **各规格总像素**：1K：1024_1024、2K：2048_2048、4K：4096\*4096
        
    -   **图像比例**：
        
        -   当有图片输入时：输出宽高比与输入图像（多图输入时为最后一张）一致，并缩放到选定分辨率。
            
        -   当没有图片输入时：输出为正方形。
            
-   **方式二：指定生成图像的宽高像素值**
    
    -   文生图：总像素在 \[768_768, 4096_4096\] 之间，宽高比范围为 \[1:8, 8:1\]。
        
    -   其他场景：总像素在 \[768_768, 2048_2048\] 之间，宽高比范围为 \[1:8, 8:1\]。
        

**模型：wan2.7-image**

-   **方式一：指定输出图片的分辨率（推荐）**
    
    -   支持1K、2K（默认）两种规格，不支持4K。
        
-   **方式二：指定生成图像的宽高像素值**
    
    -   所有场景下，总像素在 \[768_768, 2048_2048\] 之间，宽高比范围为 \[1:8, 8:1\]。
        

> 输出图片的像素值可能和指定像素值存在微小差异。

**n** `_integer_` （可选）

**重要**

n直接影响费用。费用 = 单价 × 成功生成的图片张数，请在调用前确认[模型价格](https://help.aliyun.com/zh/model-studio/model-pricing#e2540d71a2utl)。

-   关闭组图模式时，该数值代表生成图像数量，取值范围 1-4，**默认为 1**；
    
-   开启组图模式时，该数值代表最大生成图像数量，取值范围 1-12，**默认为 12**。实际数量由模型决定且不超过 n。
    

**thinking\_mode** `_boolean_` （可选）

是否开启思考模式，默认为`true`（开启）。仅在关闭组图模式且无图片输入时生效。开启时，模型将增强推理能力以提升出图质量，但会增加生成耗时。

**color\_palette** `_array_` （可选）

自定义颜色主题，一个包含颜色（hex）和占比（ratio）的对象数组，需要包含 3 至 10 种颜色，推荐设置为 8 种。

仅当关闭组图模式（`enable_sequential=false`）时可用。

**属性**

**hex** `_string_` **（必选）**

十六进制（HEX）格式的色值。

**ratio** `_string_` **（必选）**

颜色所占的百分比，需精确到小数点后两位（如`"25.00%"`）。所有 ratio 值相加**总和必须为 100.00%**。

**点击查看输入示例**

```
"color_palette": [
    {
        "hex": "#C2D1E6",
        "ratio": "23.51%"
    },
    {
        "hex": "#CDD8E9",
        "ratio": "20.13%"
    },
    {
        "hex": "#B5C8DB",
        "ratio": "15.88%"
    },
    {
        "hex": "#C0B5B4",
        "ratio": "13.27%"
    },
    {
        "hex": "#DAE0EC",
        "ratio": "10.11%"
    },
    {
        "hex": "#636574",
        "ratio": "8.93%"
    },
    {
        "hex": "#CACAD2",
        "ratio": "5.55%"
    },
    {
        "hex": "#CBD4E4",
        "ratio": "2.62%"
    }
]
```

**watermark** `_bool_` （可选）

是否添加水印标识，水印位于图片右下角，文案固定为“AI生成”。

-   false：默认值，不添加水印。
    
-   true：添加水印。
    

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
                            "image": "https://dashscope-xxx.oss-xxx.aliyuncs.com/xxx.png?Expires=xxx",
                            "type": "image"
                        }
                    ],
                    "role": "assistant"
                }
            }
        ],
        "finished": true
    },
    "usage": {
        "image_count": 1,
        "input_tokens": 10867,
        "output_tokens": 2,
        "size": "1488*704",
        "total_tokens": 10869
    },
    "request_id": "71dfc3c6-f796-9972-97e4-bc4efc4faxxx"
}
```

## 任务执行异常

如果因为某种原因导致任务执行失败，将返回相关信息，可以通过code和message字段明确指示错误原因。请参见[错误码](https://help.aliyun.com/zh/model-studio/error-code)进行解决。

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

模型生成的输出内容。

**属性**

**finish\_reason** `_string_`

任务停止原因。自然停止时为`stop`。

**message** `_object_`

模型返回的消息。

**属性**

**role** `_string_`

消息的角色，固定为`assistant`。

**content** `_array_`

**属性**

**type** `_string_`

输出的类型，固定为image。

**image** `_string_`

生成图像的 URL，图像格式为PNG。

**链接有效期为24小时**，请及时下载并保存图像。

**finished** `_boolean_`

任务是否结束。

-   true：已结束。
    
-   false：未结束。
    

**usage** `_object_`

输出信息统计。只对成功的结果计数。

**属性**

**image\_count** `_integer_`

生成图像的张数。

**size** `_string_`

生成的图像分辨率。示例值：1376\*768。

**input\_tokens** `_integer_`

输入token数量（不计费）。按图片张数计费。

**output\_tokens** `_integer_`

输出token数量（不计费）。按图片张数计费。

**total\_tokens** `_integer_`

总token数量（不计费）。按图片张数计费。

**request\_id** `_string_`

请求唯一标识。可用于请求明细溯源和问题排查。

**code** `_string_`

请求失败的错误码。请求成功时不会返回此参数，详情请参见[错误码](https://help.aliyun.com/zh/model-studio/error-code)。

**message** `_string_`

请求失败的详细信息。请求成功时不会返回此参数，详情请参见[错误码](https://help.aliyun.com/zh/model-studio/error-code)。

## **HTTP异步调用**

适用于耗时较长的任务，支持查询任务状态和结果。

### 步骤1：创建任务获取任务ID

## **北京**

`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/image-generation/generation`

## **新加坡**

`POST https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/image-generation/generation`

#### 请求参数

## **文生图**

> wan2.7-image-pro仅文生图场景支持4K分辨率，图像编辑和组图生成支持最高2K分辨率

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image-generation/generation' \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header "X-DashScope-Async: enable" \
--data '{
    "model": "wan2.7-image-pro",
    "input": {
        "messages": [
            {
                "role": "user",
                "content": [
                    {"text": "一间有着精致窗户的花店，漂亮的木质门，摆放着花朵"}
                ]
            }
        ]
    },
    "parameters": {
        "size": "2K",
        "n": 1,
        "watermark": false,
        "thinking_mode": true
    }
}'
```

## **图像编辑**

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image-generation/generation' \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header "X-DashScope-Async: enable" \
--data '{
    "model": "wan2.7-image-pro",
    "input": {
        "messages": [
            {
                "role": "user",
                "content": [
                    {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/pjeqdf/car.webp"},
                    {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/xsunlm/paint.webp"},
                    {"text": "把图2的涂鸦喷绘在图1的汽车上"}
                ]
            }
        ]
    },
    "parameters": {
        "size": "2K",
        "n": 1,
        "watermark": false
    }
}'
```

## **交互式编辑**

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image-generation/generation' \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header "X-DashScope-Async: enable" \
--data '{
    "model": "wan2.7-image-pro",
    "input": {
        "messages": [
            {
                "role": "user",
                "content": [
                    {"image": "https://img.alicdn.com/imgextra/i3/O1CN0157XGE51l6iL9441yX_!!6000000004770-49-tps-1104-1472.webp"},
                    {"image": "https://img.alicdn.com/imgextra/i3/O1CN01SfG4J41UYn9WNt4X1_!!6000000002530-49-tps-1696-960.webp"},
                    {"text": "把图1的闹钟放在图2的框选的位置，保持场景和光线融合自然"}
                ]
            }
        ]
    },
    "parameters": {
        "bbox_list": [[],[[989, 515, 1138, 681]]],
        "size": "2K",
        "n": 1,
        "watermark": false
    }
}'
```

## **组图生成**

> wan2.7-image-pro组图生成仅支持最高2K分辨率。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image-generation/generation' \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header "X-DashScope-Async: enable" \
--data '{
    "model": "wan2.7-image-pro",
    "input": {
        "messages": [
            {
                "role": "user",
                "content": [
                    {"text": "电影感组图，记录同一只流浪橘猫，特征必须前后一致。第一张：春天，橘猫穿梭在盛开的樱花树下；第二张：夏天，橘猫在老街的树荫下乘凉避暑；第三张：秋天，橘猫踩在满地的金色落叶上；第四张：冬天，橘猫在雪地上走留下足迹。"}
                ]
            }
        ]
    },
    "parameters": {
        "enable_sequential": true,
        "n": 4,
        "size": "2K"
    }
}'
```

##### 请求头（Headers）

**Content-Type** `_string_` **（必选）**

请求内容类型。此参数必须设置为`application/json`。

**Authorization** `_string_`**（必选）**

请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。

**X-DashScope-Async** `_string_` **（必选）**

异步处理配置参数。HTTP请求只支持异步，**必须设置为**`**enable**`。

**重要**

缺少此请求头将报错：“current user api does not support synchronous calls”。

##### 请求体（Request Body）

**model** `_string_` **（必选）**

模型名称。可选值：`wan2.7-image-pro`、`wan2.7-image`。

**input** `_object_` **（必选）**

输入的基本信息。

**属性**

**messages** `_array_` **（必选）**

请求内容数组。当前**仅支持单轮对话**，即传入一组role、content参数，不支持多轮对话。

**属性**

**role** `_string_` **（必选）**

消息的角色。此参数固定设置为`user`。

**content** `_array_` **（必选）**

消息内容数组。

**属性**

**text** `_string_`

用户输入提示词。支持中英文，长度不超过5000个字符，每个汉字、字母、数字或符号计为一个字符，超过部分会自动截断。

**image** `_string_`

输入图像的URL或Base64编码字符串。

图像限制：

-   图像格式：JPEG、JPG、PNG（不支持透明通道）、BMP、WEBP。
    
-   图像分辨率：图像的宽高范围均为\[240, 8000\]像素，宽高比范围\[1:8, 8:1\]。
    
-   文件大小：不超过20MB。
    

图像数量限制：

-   可传入0-9张图片。
    
-   当输入多张图像时，需在`content`数组中传入多个`image`对象，并按照数组顺序定义图像顺序。
    

支持的输入格式：

1.  使用公网可访问URL
    
    -   支持HTTP或HTTPS协议。
        
    -   示例值：`http://wanx.alicdn.com/material/xxx.jpeg`。
        
2.  传入 Base64 编码图像后的字符串
    
    -   格式：data:{MIME\_type};base64,{base64\_data}
        
    -   示例：data:image/jpeg;base64,GDU7MtCZzEbTbmRZ...（仅示意，实际需传入完整字符串）
        
    -   Base64 编码规范请参见[图像传入方式](https://help.aliyun.com/zh/model-studio/wan-image-edit#8db0e2215frua)。
        

**parameters** `_object_` （可选）

模型参数配置。

**属性**

**bbox\_list** `_array[array[array[integer]]]_` （可选）

交互式编辑框选区域。

-   对应关系：列表长度必须与输入图片数量一致。若某张图片无需编辑，请在对应位置传入空列表 `[]`。
    
-   坐标格式：`[x1, y1, x2, y2]`（左上角 x, 左上角 y, 右下角 x, 右下角 y），使用原图绝对像素坐标，左上角坐标为（0，0）。
    
-   限制条件：单张图片最多支持 2 个边界框。
    

示例：输入 3 张图片，其中第 2 张无框选，第 1 张有两个框选：

```
[
  [[0, 0, 12, 12], [25, 25, 100, 100]],  # 图 1 (2个框)
  [],                                    # 图 2 (无框)
  [[10, 10, 50, 50]]                    # 图 3 (1个框)
]
```

**enable\_sequential** `_boolean_` （可选）

控制生图模式：

-   false：默认值。
    
-   true ：启用组图输出模式。
    

**size** `_string_` （可选）

关于输出图片分辨率参数，支持以下两种方式，不可混用：

**模型：wan2.7-image-pro**

-   **方式一：指定输出图片的分辨率（推荐）**
    
    -   支持 1K、2K（默认）、4K 三种规格
        
    -   **适用范围**：
        
        -   文生图（无图片输入，非组图生成）：支持1K、2K、4K。
            
        -   其他场景：支持1K、2K。
            
    -   **各规格总像素**：1K：1024_1024、2K：2048_2048、4K：4096\*4096
        
    -   **图像比例**：
        
        -   当有图片输入时：输出宽高比与输入图像（多图输入时为最后一张）一致，并缩放到选定分辨率。
            
        -   当没有图片输入时：输出为正方形。
            
-   **方式二：指定生成图像的宽高像素值**
    
    -   文生图：总像素在 \[768_768, 4096_4096\] 之间，宽高比范围为 \[1:8, 8:1\]。
        
    -   其他场景：总像素在 \[768_768, 2048_2048\] 之间，宽高比范围为 \[1:8, 8:1\]。
        

**模型：wan2.7-image**

-   **方式一：指定输出图片的分辨率（推荐）**
    
    -   支持1K、2K（默认）两种规格，不支持4K。
        
-   **方式二：指定生成图像的宽高像素值**
    
    -   所有场景下，总像素在 \[768_768, 2048_2048\] 之间，宽高比范围为 \[1:8, 8:1\]。
        

> 输出图片的像素值可能和指定像素值存在微小差异。

**n** `_integer_` （可选）

**重要**

n直接影响费用。费用 = 单价 × 成功生成的图片张数，请在调用前确认[模型价格](https://help.aliyun.com/zh/model-studio/model-pricing#e2540d71a2utl)。

-   关闭组图模式时，该数值代表生成图像数量，取值范围 1-4，**默认为 1**；
    
-   开启组图模式时，该数值代表最大生成图像数量，取值范围 1-12，**默认为 12**。实际数量由模型决定且不超过 n。
    

**thinking\_mode** `_boolean_` （可选）

是否开启思考模式，默认为`true`（开启）。仅在关闭组图模式且无图片输入时生效。开启时，模型将增强推理能力以提升出图质量，但会增加生成耗时。

**color\_palette** `_array_` （可选）

自定义颜色主题，一个包含颜色（hex）和占比（ratio）的对象数组，需要包含 3 至 10 种颜色，推荐设置为 8 种。

仅当关闭组图模式（`enable_sequential=false`）时可用。

**属性**

**hex** `_string_` **（必选）**

十六进制（HEX）格式的色值。

**ratio** `_string_` **（必选）**

颜色所占的百分比，需精确到小数点后两位（如`"25.00%"`）。所有 ratio 值相加**总和必须为 100.00%**。

**点击查看输入示例**

```
"color_palette": [
    {
        "hex": "#C2D1E6",
        "ratio": "23.51%"
    },
    {
        "hex": "#CDD8E9",
        "ratio": "20.13%"
    },
    {
        "hex": "#B5C8DB",
        "ratio": "15.88%"
    },
    {
        "hex": "#C0B5B4",
        "ratio": "13.27%"
    },
    {
        "hex": "#DAE0EC",
        "ratio": "10.11%"
    },
    {
        "hex": "#636574",
        "ratio": "8.93%"
    },
    {
        "hex": "#CACAD2",
        "ratio": "5.55%"
    },
    {
        "hex": "#CBD4E4",
        "ratio": "2.62%"
    }
]
```

**watermark** `_bool_` （可选）

是否添加水印标识，水印位于图片右下角，文案固定为“AI生成”。

-   false：默认值，不添加水印。
    
-   true：添加水印。
    

**seed** `_integer_` （可选）

随机数种子，取值范围`[0,2147483647]`。

使用相同的`seed`参数值可使生成内容保持相对稳定。若不提供，算法将自动使用随机数种子。

**注意**：模型生成过程具有概率性，即使使用相同的`seed`，也不能保证每次生成结果完全一致。

#### 响应参数

#### 成功响应

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

#### 异常响应

创建任务失败，请参见[错误码](https://help.aliyun.com/zh/model-studio/error-code)进行解决。

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

**code** `_string_`

请求失败的错误码。请求成功时不会返回此参数，详情请参见[错误码](https://help.aliyun.com/zh/model-studio/error-code)。

**message** `_string_`

请求失败的详细信息。请求成功时不会返回此参数，详情请参见[错误码](https://help.aliyun.com/zh/model-studio/error-code)。

### 步骤2：根据任务ID查询结果

## **北京**

`GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`

## **新加坡**

`GET https://dashscope-intl.aliyuncs.com/api/v1/tasks/{task_id}`

#### 请求参数

## 查询任务结果

将`{task_id}`完整替换为上一步接口返回的`task_id`的值。`task_id`查询有效期为24小时。

```
curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id} \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

##### **请求头（Headers）**

**Authorization** `_string_`**（必选）**

请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。

##### **URL路径参数（Path parameters）**

**task\_id** `_string_`**（必选）**

任务ID。

#### 响应参数

## 任务执行成功

任务数据（如任务状态、图像URL等）仅保留24小时，超时后会被自动清除。请您务必及时保存生成的图像。

```
{
    "request_id": "810fa5f5-334c-91f3-aaa4-ed89cf0caxxx",
    "output": {
        "task_id": "a81ee7cb-014c-473d-b842-76e98311cxxx",
        "task_status": "SUCCEEDED",
        "submit_time": "2026-03-26 17:16:01.663",
        "scheduled_time": "2026-03-26 17:16:01.716",
        "end_time": "2026-03-26 17:16:22.961",
        "finished": true,
        "choices": [
            {
                "finish_reason": "stop",
                "message": {
                    "role": "assistant",
                    "content": [
                        {
                            "image": "https://dashscope-xxx.oss-xxx.aliyuncs.com/xxx.png?Expires=xxx",
                            "type": "image"
                        }
                    ]
                }
            }
        ]
    },
    "usage": {
        "size": "2976*1408",
        "total_tokens": 11017,
        "image_count": 1,
        "output_tokens": 2,
        "input_tokens": 11015
    }
}
```

## 任务执行异常

如果因为某种原因导致任务执行失败，将返回相关信息，可以通过code和message字段明确指示错误原因。请参见[错误码](https://help.aliyun.com/zh/model-studio/error-code)进行解决。

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
    

**轮询过程中的状态流转：**

-   PENDING（排队中） → RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。
    
-   初次查询状态通常为 PENDING（排队中）或 RUNNING（处理中）。
    
-   当状态变为 SUCCEEDED 时，响应中将包含生成的图像URL。
    
-   若状态为 FAILED，请检查错误信息并重试。
    

**submit\_time** `_string_`

任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。

**scheduled\_time** `_string_`

任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。

**end\_time** `_string_`

任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。

**finished** `_boolean_`

任务是否结束。

-   true：已结束。
    
-   false：未结束。
    

**choices** `_array_`

模型生成的输出内容。

**属性**

**finish\_reason** `_string_`

任务停止原因，自然停止时为`stop`。

**message** `_object_`

模型返回的消息。

**属性**

**role** `_string_`

消息的角色，固定为`assistant`。

**content** `_array_`

**属性**

**type** `_string_`

输出的类型，枚举值为text、image。

**text** `_string_`

生成的文字。

**image** `_string_`

生成图像的 URL，图像格式为PNG。

**链接有效期为24小时**，请及时下载并保存图像。

**usage** `_object_`

输出信息统计。只对成功的结果计数。

**属性**

**image\_count** `_integer_`

生成图像的张数。

**size** `_string_`

生成的图像分辨率。示例值：1376\*768。

**input\_tokens** `_integer_`

输入token数量（不计费）。按图片张数计费。

**output\_tokens** `_integer_`

输出token数量（不计费）。按图片张数计费。

**total\_tokens** `_integer_`

总token数量（不计费）。按图片张数计费。

**request\_id** `_string_`

请求唯一标识。可用于请求明细溯源和问题排查。

**code** `_string_`

请求失败的错误码。请求成功时不会返回此参数，详情请参见[错误码](https://help.aliyun.com/zh/model-studio/error-code)。

**message** `_string_`

请求失败的详细信息。请求成功时不会返回此参数，详情请参见[错误码](https://help.aliyun.com/zh/model-studio/error-code)。

## **Python SDK调用**

SDK 参数命名与HTTP接口基本一致。

任务可能耗时较长，SDK 已封装HTTP异步调用流程，同时支持同步和异步调用。

> 具体耗时受限于排队任务数和服务执行情况，请在获取结果时耐心等待。

**重要**

请确保 DashScope Python SDK版本**不低于 1.25.15**，再运行以下代码。更新请参考[安装SDK](https://help.aliyun.com/zh/model-studio/install-sdk)。

各地域的`base_url`和API Key 不通用，以下示例以北京地域为例进行调用：

### 北京

`https://dashscope.aliyuncs.com/api/v1`

### 新加坡

`https://dashscope-intl.aliyuncs.com/api/v1`

### **图像编辑**

## **同步调用**

##### **请求示例**

```
import os
import base64
import mimetypes
import urllib.request
import dashscope
from dashscope.aigc.image_generation import ImageGeneration
from dashscope.api_entities.dashscope_response import Message

# 以下为北京地域base_url，各地域的base_url不同
dashscope.base_http_api_url = "https://dashscope.aliyuncs.com/api/v1"

# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
api_key = os.getenv("DASHSCOPE_API_KEY")

# --- Base64编码函数 ---
# base64编码格式为 data:{MIME_type};base64,{base64_data}
def encode_file(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type or not mime_type.startswith("image/"):
        raise ValueError("不支持或无法识别的图像格式")
    with open(file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return f"data:{mime_type};base64,{encoded_string}"

"""
图像输入方式说明：
以下提供了三种图片输入方式，三选一即可
1. 使用公网URL - 适合已有公开可访问的图片
2. 使用本地文件 - 适合本地开发测试
3. 使用Base64编码 - 适合私有图片或需要加密传输的场景
"""
# 【方式一】使用公网图片 URL
image_1 = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/pjeqdf/car.webp"
image_2 = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/xsunlm/paint.webp"

# 【方式二】使用本地文件（支持绝对路径和相对路径）
# image_1 = "file:///path/to/your/car.png"
# image_2 = "file:///path/to/your/paint.png"

# 【方式三】使用Base64编码的图片
# image_1 = encode_file("/path/to/your/car.png")
# image_2 = encode_file("/path/to/your/paint.png")

message = Message(
    role="user",
    content=[
        {"text": "把图2的涂鸦喷绘在图1的汽车上"},
        {"image": image_1},
        {"image": image_2},
    ],
)
print("----sync call, please wait a moment----")
rsp = ImageGeneration.call(
    model="wan2.7-image-pro",
    api_key=api_key,
    messages=[message],
    watermark=False,
    n=1,
    size="2K",  # wan2.7-image-pro仅文生图场景支持4K分辨率，图像编辑和组图生成支持最高2K分辨率
)

# 提取结果图片URL并保存到本地
if rsp.status_code == 200:
    for i, choice in enumerate(rsp.output.choices):
        for j, content in enumerate(choice["message"]["content"]):
            if content.get("type") == "image":
                image_url = content["image"]
                file_name = f"output_{i}_{j}.png"
                # 结果URL有效期为24小时，请及时下载
                urllib.request.urlretrieve(image_url, file_name)
                print(f"Image saved to {file_name}")
else:
    print(f"Failed: status_code={rsp.status_code}, message={rsp.message}")
```

##### 响应示例

> URL 有效期24小时，请及时下载图像。

```
{
    "status_code": 200,
    "request_id": "81d868c6-6ce1-92d8-a90d-d2ee71xxxxxx",
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
        "input_tokens": 18790,
        "output_tokens": 2,
        "characters": 0,
        "image_count": 1,
        "size": "2985*1405",
        "total_tokens": 18792
    }
}
```

## **异步调用**

##### **请求示例**

```
import os
import base64
import mimetypes
import urllib.request
import dashscope
from dashscope.aigc.image_generation import ImageGeneration
from dashscope.api_entities.dashscope_response import Message
from http import HTTPStatus

# 以下为北京地域base_url，各地域的base_url不同
dashscope.base_http_api_url = "https://dashscope.aliyuncs.com/api/v1"

# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
api_key = os.getenv("DASHSCOPE_API_KEY")

# --- Base64编码函数 ---
# base64编码格式为 data:{MIME_type};base64,{base64_data}
def encode_file(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type or not mime_type.startswith("image/"):
        raise ValueError("不支持或无法识别的图像格式")
    with open(file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return f"data:{mime_type};base64,{encoded_string}"

"""
图像输入方式说明：
以下提供了三种图片输入方式，三选一即可
1. 使用公网URL - 适合已有公开可访问的图片
2. 使用本地文件 - 适合本地开发测试
3. 使用Base64编码 - 适合私有图片或需要加密传输的场景
"""
# 【方式一】使用公网图片 URL
image_1 = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/pjeqdf/car.webp"
image_2 = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/xsunlm/paint.webp"

# 【方式二】使用本地文件（支持绝对路径和相对路径）
# image_1 = "file:///path/to/your/car.png"
# image_2 = "file:///path/to/your/paint.png"

# 【方式三】使用Base64编码的图片
# image_1 = encode_file("/path/to/your/car.png")
# image_2 = encode_file("/path/to/your/paint.png")

# 创建异步任务
def create_async_task():
    print("Creating async task...")
    message = Message(
        role="user",
        content=[
            {"text": "把图2的涂鸦喷绘在图1的汽车上"},
            {"image": image_1},
            {"image": image_2},
        ],
    )
    response = ImageGeneration.async_call(
        model="wan2.7-image-pro",
        api_key=api_key,
        messages=[message],
        watermark=False,
        n=1,
        size="2K",  # wan2.7-image-pro仅文生图场景支持4K分辨率，图像编辑和组图生成支持最高2K分辨率
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
        # 提取结果图片URL并保存到本地
        for i, choice in enumerate(status.output.choices):
            for j, content in enumerate(choice["message"]["content"]):
                if content.get("type") == "image":
                    image_url = content["image"]
                    file_name = f"output_{i}_{j}.png"
                    # 结果URL有效期为24小时，请及时下载
                    urllib.request.urlretrieve(image_url, file_name)
                    print(f"Image saved to {file_name}")
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
    "request_id": "4fb3050f-de57-4a24-84ff-e37ee5xxxxxx",
    "code": "",
    "message": "",
    "output": {
        "text": null,
        "finish_reason": null,
        "choices": null,
        "audio": null,
        "task_id": "127ec645-118f-4884-955d-0eba8dxxxxxx",
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

> URL 有效期24小时，请及时下载图像。

```
{
    "status_code": 200,
    "request_id": "3b99aae5-d26f-9059-8dd0-ee9ca4804xxx",
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
        "task_id": "127ec645-118f-4884-955d-0eba8dxxxxxx",
        "task_status": "SUCCEEDED",
        "submit_time": "2026-03-31 22:58:47.646",
        "scheduled_time": "2026-03-31 22:58:47.683",
        "end_time": "2026-03-31 22:58:59.642",
        "finished": true
    },
    "usage": {
        "input_tokens": 18711,
        "output_tokens": 2,
        "characters": 0,
        "size": "2985*1405",
        "total_tokens": 18713,
        "image_count": 1
    }
}
```

### **组图生成**

## **同步调用**

##### **请求示例**

```
import os
import base64
import mimetypes
import urllib.request
import dashscope
from dashscope.aigc.image_generation import ImageGeneration
from dashscope.api_entities.dashscope_response import Message

# 以下为北京地域base_url，各地域的base_url不同
dashscope.base_http_api_url = "https://dashscope.aliyuncs.com/api/v1"

# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
api_key = os.getenv("DASHSCOPE_API_KEY")

# --- Base64编码函数 ---
# base64编码格式为 data:{MIME_type};base64,{base64_data}
def encode_file(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type or not mime_type.startswith("image/"):
        raise ValueError("不支持或无法识别的图像格式")
    with open(file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return f"data:{mime_type};base64,{encoded_string}"

"""
图像输入方式说明（图生组图场景）：
以下提供了三种图片输入方式，三选一即可
1. 使用公网URL - 适合已有公开可访问的图片
2. 使用本地文件 - 适合本地开发测试
3. 使用Base64编码 - 适合私有图片或需要加密传输的场景
"""
# 【方式一】使用公网图片 URL
# image_1 = "https://img.alicdn.com/imgextra/i4/O1CN01IM44WN23dq5uY1yla_!!6000000007279-49-tps-1024-1024.webp"

# 【方式二】使用本地文件（支持绝对路径和相对路径）
# image_1 = "file:///path/to/your/image.png"

# 【方式三】使用Base64编码的图片
# image_1 = encode_file("/path/to/your/image.png")

message = Message(
    role="user",
    content=[
        {
            "text": "电影感组图，记录同一只流浪橘猫，特征必须前后一致。第一张：春天，橘猫穿梭在盛开的樱花树下；第二张：夏天，橘猫在老街的树荫下乘凉避暑；第三张：秋天，橘猫踩在满地的金色落叶上；第四张：冬天，橘猫在雪地上走留下足迹。"
        }
        # 图生组图场景：取消以下注释并注释掉上方纯文本
        # {"text": "参考图片风格生成四季组图"},
        # {"image": image_1}
    ],
)

print("----sync call, please wait a moment----")
rsp = ImageGeneration.call(
    model="wan2.7-image-pro",
    api_key=api_key,
    messages=[message],
    enable_sequential=True,
    n=4,
    size="2K",  # wan2.7-image-pro仅文生图场景支持4K分辨率，图像编辑和组图生成支持最高2K分辨率
)

# 提取结果图片URL并保存到本地
if rsp.status_code == 200:
    for i, choice in enumerate(rsp.output.choices):
        for j, content in enumerate(choice["message"]["content"]):
            if content.get("type") == "image":
                image_url = content["image"]
                file_name = f"output_{i}_{j}.png"
                # 结果URL有效期为24小时，请及时下载
                urllib.request.urlretrieve(image_url, file_name)
                print(f"Image saved to {file_name}")
else:
    print(f"Failed: status_code={rsp.status_code}, message={rsp.message}")
```

##### 响应示例

> URL 有效期24小时，请及时下载图像。

```
{
    "status_code": 200,
    "request_id": "56e318fd-ed60-99e8-8ca1-cdef25ca4xxx",
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
                        },
                        {
                            "image": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxxxxx.png?Expires=xxxxxx",
                            "type": "image"
                        },
                        {
                            "image": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxxxxx.png?Expires=xxxxxx",
                            "type": "image"
                        },
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
        "input_tokens": 720,
        "output_tokens": 11,
        "characters": 0,
        "image_count": 4,
        "size": "2048*2048",
        "total_tokens": 731
    }
}
```

## **异步调用**

##### **请求示例**

```
import os
import base64
import mimetypes
import urllib.request
import dashscope
from dashscope.aigc.image_generation import ImageGeneration
from dashscope.api_entities.dashscope_response import Message

# 以下为北京地域base_url，各地域的base_url不同
dashscope.base_http_api_url = "https://dashscope.aliyuncs.com/api/v1"

# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
api_key = os.getenv("DASHSCOPE_API_KEY")

# --- Base64编码函数 ---
# base64编码格式为 data:{MIME_type};base64,{base64_data}
def encode_file(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type or not mime_type.startswith("image/"):
        raise ValueError("不支持或无法识别的图像格式")
    with open(file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return f"data:{mime_type};base64,{encoded_string}"

"""
图像输入方式说明（图生组图场景）：
以下提供了三种图片输入方式，三选一即可
1. 使用公网URL - 适合已有公开可访问的图片
2. 使用本地文件 - 适合本地开发测试
3. 使用Base64编码 - 适合私有图片或需要加密传输的场景
"""
# 【方式一】使用公网图片 URL
# image_1 = "https://img.alicdn.com/imgextra/i4/O1CN01IM44WN23dq5uY1yla_!!6000000007279-49-tps-1024-1024.webp"

# 【方式二】使用本地文件（支持绝对路径和相对路径）
# image_1 = "file:///path/to/your/image.png"

# 【方式三】使用Base64编码的图片
# image_1 = encode_file("/path/to/your/image.png")

def main():
    message = Message(
        role="user",
        content=[
            {
                "text": "电影感组图，记录同一只流浪橘猫，特征必须前后一致。第一张：春天，橘猫穿梭在盛开的樱花树下；第二张：夏天，橘猫在老街的树荫下乘凉避暑；第三张：秋天，橘猫踩在满地的金色落叶上；第四张：冬天，橘猫在雪地上走留下足迹。"
            }
            # 图生组图场景：取消以下注释并注释掉上方纯文本
            # {"text": "参考图片风格生成四季组图"},
            # {"image": image_1}
        ],
    )

    # 提交异步任务
    print("提交异步任务...")
    response = ImageGeneration.async_call(
        model="wan2.7-image-pro",
        api_key=api_key,
        messages=[message],
        enable_sequential=True,
        n=4,
        size="2K",  # wan2.7-image-pro仅文生图场景支持4K分辨率，图像编辑和组图生成支持最高2K分辨率
    )

    if response.status_code == 200:
        print(f"任务提交成功，任务ID: {response.output.task_id}")

        # 等待任务完成
        status = ImageGeneration.wait(task=response, api_key=api_key)

        if status.output.task_status == "SUCCEEDED":
            print("任务完成!")
            # 提取结果图片URL并保存到本地
            for i, choice in enumerate(status.output.choices):
                for j, content in enumerate(choice["message"]["content"]):
                    if content.get("type") == "image":
                        image_url = content["image"]
                        file_name = f"output_{i}_{j}.png"
                        # 结果URL有效期为24小时，请及时下载
                        urllib.request.urlretrieve(image_url, file_name)
                        print(f"Image saved to {file_name}")
        else:
            print(f"任务失败，状态: {status.output.task_status}")
    else:
        print(f"任务创建失败: {response.code} - {response.message}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"错误: {e}")
```

##### 响应示例

1、创建任务的响应示例

```
{
    "status_code": 200,
    "request_id": "4fb3050f-de57-4a24-84ff-e37ee5xxxxxx",
    "code": "",
    "message": "",
    "output": {
        "text": null,
        "finish_reason": null,
        "choices": null,
        "audio": null,
        "task_id": "77093787-a217-4c29-9cd4-ca7b5ac86xxx",
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

> URL 有效期24小时，请及时下载图像。

```
{
    "status_code": 200,
    "request_id": "56e318fd-ed60-99e8-8ca1-cdef25ca4xxx",
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
                        },
                        {
                            "image": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxxxxx.png?Expires=xxxxxx",
                            "type": "image"
                        },
                        {
                            "image": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxxxxx.png?Expires=xxxxxx",
                            "type": "image"
                        },
                        {
                            "image": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxxxxx.png?Expires=xxxxxx",
                            "type": "image"
                        }
                    ]
                }
            }
        ],
        "audio": null,
        "task_id": "77093787-a217-4c29-9cd4-ca7b5ac86xxx",
        "task_status": "SUCCEEDED",
        "submit_time": "2026-03-31 23:04:46.166",
        "scheduled_time": "2026-03-31 23:04:46.208",
        "end_time": "2026-03-31 23:05:11.664",
        "finished": true
    },
    "usage": {
        "input_tokens": 720,
        "output_tokens": 11,
        "characters": 0,
        "size": "2048*2048",
        "total_tokens": 731,
        "image_count": 4
    }
}
```

## **Java SDK调用**

SDK 参数命名与HTTP接口基本一致。

任务可能耗时较长，SDK 已封装HTTP异步调用流程，同时支持同步和异步调用。

**重要**

请确保 DashScope Java SDK版本不低于 `2.22.13`，否则可能不支持本文所用的部分参数。

### 北京

`https://dashscope.aliyuncs.com/api/v1`

### 新加坡

`https://dashscope-intl.aliyuncs.com/api/v1`

### **图像编辑**

## **同步调用**

##### 请求示例

```
import com.alibaba.dashscope.aigc.imagegeneration.*;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;
import com.alibaba.dashscope.utils.JsonUtils;

import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.Arrays;
import java.util.Base64;
import java.util.Collections;
import java.util.List;
import java.util.Map;

/**
 * wan2.7-image-pro 图像编辑 - 同步调用示例
 */
public class Main {

    static {
        // 以下为北京地域url，各地域的base_url不同
        Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
    }

    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey="sk-xxx"
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    // --- Base64编码函数 ---
    // base64编码格式为 data:{MIME_type};base64,{base64_data}
    public static String encodeFile(String filePath) throws IOException {
        byte[] fileContent = Files.readAllBytes(Paths.get(filePath));
        String base64String = Base64.getEncoder().encodeToString(fileContent);
        String mimeType = Files.probeContentType(Paths.get(filePath));
        return "data:" + mimeType + ";base64," + base64String;
    }

    public static void basicCall() throws ApiException, NoApiKeyException, UploadFileException, IOException {
        /*
         * 图像输入方式说明：
         * 以下提供了三种图片输入方式，三选一即可
         * 1. 使用公网URL - 适合已有公开可访问的图片
         * 2. 使用本地文件 - 适合本地开发测试
         * 3. 使用Base64编码 - 适合私有图片或需要加密传输的场景
         */
        // 【方式一】使用公网图片 URL
        String image1 = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/pjeqdf/car.webp";
        String image2 = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/xsunlm/paint.webp";

        // 【方式二】使用本地文件（支持绝对路径和相对路径）
        // 格式要求：file:// + 文件路径
        // String image1 = "file:///path/to/your/car.png";
        // String image2 = "file:///path/to/your/paint.png";

        // 【方式三】使用Base64编码的图片
        // String image1 = encodeFile("/path/to/your/car.png");
        // String image2 = encodeFile("/path/to/your/paint.png");

        // 构建多图输入消息
        ImageGenerationMessage message = ImageGenerationMessage.builder()
                .role("user")
                .content(Arrays.asList(
                        // 支持多图输入，可以提供多张参考图片
                        Collections.singletonMap("text", "把图2的涂鸦喷绘在图1的汽车上"),
                        Collections.singletonMap("image", image1),
                        Collections.singletonMap("image", image2)
                )).build();

        ImageGenerationParam param = ImageGenerationParam.builder()
                .apiKey(apiKey)
                .model("wan2.7-image-pro")
                .messages(Collections.singletonList(message))
                .n(1)
                .size("2K") // wan2.7-image-pro仅文生图场景支持4K分辨率，图像编辑和组图生成支持最高2K分辨率
                .build();

        ImageGeneration imageGeneration = new ImageGeneration();
        ImageGenerationResult result = null;
        try {
            System.out.println("---sync call for image editing, please wait a moment----");
            result = imageGeneration.call(param);
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            throw new RuntimeException(e.getMessage());
        }
        // 提取结果图片URL并保存到本地
        for (int i = 0; i < result.getOutput().getChoices().size(); i++) {
            List<Map<String, Object>> contents = result.getOutput().getChoices().get(i)
                    .getMessage().getContent();
            for (int j = 0; j < contents.size(); j++) {
                if ("image".equals(contents.get(j).get("type"))) {
                    String imageUrl = (String) contents.get(j).get("image");
                    String fileName = "output_" + i + "_" + j + ".png";
                    // 结果URL有效期为24小时，请及时下载
                    try (InputStream in = new URL(imageUrl).openStream()) {
                        Files.copy(in, Paths.get(fileName), StandardCopyOption.REPLACE_EXISTING);
                    }
                    System.out.println("Image saved to " + fileName);
                }
            }
        }
    }

    public static void main(String[] args) throws ApiException, NoApiKeyException, UploadFileException, IOException {
        basicCall();
    }
}
```

##### 响应示例

> URL 有效期24小时，请及时下载并保存图像。

```
{
    "requestId": "1bf6173a-e8de-9f75-94d3-5e618f875xxx",
    "usage": {
        "input_tokens": 18790,
        "output_tokens": 2,
        "total_tokens": 18792,
        "image_count": 1,
        "size": "2985*1405"
    },
    "output": {
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
        "finished": true
    },
    "status_code": 200,
    "code": "",
    "message": ""
}
```

## **异步调用**

##### 请求示例

```
import com.alibaba.dashscope.aigc.imagegeneration.*;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;
import com.alibaba.dashscope.utils.JsonUtils;

import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.Arrays;
import java.util.Base64;
import java.util.Collections;
import java.util.List;
import java.util.Map;

/**
 * wan2.7-image-pro 图像编辑 - 异步调用示例
 */
public class Main {

    static {
        // 以下为北京地域url，各地域的base_url不同
        Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
    }

    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey="sk-xxx"
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    // --- Base64编码函数 ---
    // base64编码格式为 data:{MIME_type};base64,{base64_data}
    public static String encodeFile(String filePath) throws IOException {
        byte[] fileContent = Files.readAllBytes(Paths.get(filePath));
        String base64String = Base64.getEncoder().encodeToString(fileContent);
        String mimeType = Files.probeContentType(Paths.get(filePath));
        return "data:" + mimeType + ";base64," + base64String;
    }

    public static void asyncCall() throws ApiException, NoApiKeyException, UploadFileException, IOException {
        /*
         * 图像输入方式说明：
         * 以下提供了三种图片输入方式，三选一即可
         * 1. 使用公网URL - 适合已有公开可访问的图片
         * 2. 使用本地文件 - 适合本地开发测试
         * 3. 使用Base64编码 - 适合私有图片或需要加密传输的场景
         */
        // 【方式一】使用公网图片 URL
        String image1 = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/pjeqdf/car.webp";
        String image2 = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/xsunlm/paint.webp";

        // 【方式二】使用本地文件（支持绝对路径和相对路径）
        // 格式要求：file:// + 文件路径
        // String image1 = "file:///path/to/your/car.png";
        // String image2 = "file:///path/to/your/paint.png";

        // 【方式三】使用Base64编码的图片
        // String image1 = encodeFile("/path/to/your/car.png");
        // String image2 = encodeFile("/path/to/your/paint.png");

        // 构建多图输入消息
        ImageGenerationMessage message = ImageGenerationMessage.builder()
                .role("user")
                .content(Arrays.asList(
                        // 支持多图输入，可以提供多张参考图片
                        Collections.singletonMap("text", "把图2的涂鸦喷绘在图1的汽车上"),
                        Collections.singletonMap("image", image1),
                        Collections.singletonMap("image", image2)
                )).build();

        ImageGenerationParam param = ImageGenerationParam.builder()
                .apiKey(apiKey)
                .model("wan2.7-image-pro")
                .n(1)
                .size("2K") // wan2.7-image-pro仅文生图场景支持4K分辨率，图像编辑和组图生成支持最高2K分辨率
                .messages(Arrays.asList(message))
                .build();

        ImageGeneration imageGeneration = new ImageGeneration();
        ImageGenerationResult result = null;
        try {
            System.out.println("---async call for image editing, creating task----");
            result = imageGeneration.asyncCall(param);
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            throw new RuntimeException(e.getMessage());
        }
        System.out.println("任务创建结果:");
        System.out.println(JsonUtils.toJson(result));

        String taskId = result.getOutput().getTaskId();
        // 等待任务完成
        waitTask(taskId);
    }

    public static void waitTask(String taskId) throws ApiException, NoApiKeyException, IOException {
        ImageGeneration imageGeneration = new ImageGeneration();
        System.out.println("\n---waiting for task completion----");
        ImageGenerationResult result = imageGeneration.wait(taskId, apiKey);
        // 提取结果图片URL并保存到本地
        for (int i = 0; i < result.getOutput().getChoices().size(); i++) {
            List<Map<String, Object>> contents = result.getOutput().getChoices().get(i)
                    .getMessage().getContent();
            for (int j = 0; j < contents.size(); j++) {
                if ("image".equals(contents.get(j).get("type"))) {
                    String imageUrl = (String) contents.get(j).get("image");
                    String fileName = "output_" + i + "_" + j + ".png";
                    // 结果URL有效期为24小时，请及时下载
                    try (InputStream in = new URL(imageUrl).openStream()) {
                        Files.copy(in, Paths.get(fileName), StandardCopyOption.REPLACE_EXISTING);
                    }
                    System.out.println("Image saved to " + fileName);
                }
            }
        }
    }

    public static void main(String[] args) throws ApiException, NoApiKeyException, UploadFileException, IOException {
        asyncCall();
    }
}
```

##### 响应示例

1、创建任务的响应示例

```
{
    "requestId": "ccf4b2f4-bf30-9e13-9461-3a28c6a7bxxx",
    "output": {
        "task_id": "8811b4a4-00ac-4aa2-a2fd-017d3b90cxxx",
        "task_status": "PENDING"
    },
    "status_code": 200,
    "code": "",
    "message": ""
}
```

2、查询任务结果的响应示例

> URL 有效期24小时，请及时下载并保存图像。

```
{
    "requestId": "60a08540-f1c1-9e76-8cd3-d5949db8cxxx",
    "usage": {
        "input_tokens": 18711,
        "output_tokens": 2,
        "total_tokens": 18713,
        "image_count": 1,
        "size": "2985*1405"
    },
    "output": {
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
        "task_id": "8811b4a4-00ac-4aa2-a2fd-017d3b90cxxx",
        "task_status": "SUCCEEDED",
        "finished": true,
        "submit_time": "2026-03-31 19:57:58.840",
        "scheduled_time": "2026-03-31 19:57:58.877",
        "end_time": "2026-03-31 19:58:11.563"
    },
    "status_code": 200,
    "code": "",
    "message": ""
}
```

### **组图生成**

## **同步调用**

##### 请求示例

```
import com.alibaba.dashscope.aigc.imagegeneration.*;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;
import com.alibaba.dashscope.utils.JsonUtils;

import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.Arrays;
import java.util.Base64;
import java.util.Collections;
import java.util.List;
import java.util.Map;

/**
 * wan2.7-image-pro 组图生成 - 同步调用示例（北京地域）
 */
public class Main {

    static {
        // 以下为北京地域url，各地域的base_url不同
        Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
    }

    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey="sk-xxx"
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    // --- Base64编码函数 ---
    // base64编码格式为 data:{MIME_type};base64,{base64_data}
    public static String encodeFile(String filePath) throws IOException {
        byte[] fileContent = Files.readAllBytes(Paths.get(filePath));
        String base64String = Base64.getEncoder().encodeToString(fileContent);
        String mimeType = Files.probeContentType(Paths.get(filePath));
        return "data:" + mimeType + ";base64," + base64String;
    }

    public static void basicCall() throws ApiException, NoApiKeyException, UploadFileException, IOException {
        /*
         * 图像输入方式说明（图生组图场景）：
         * 以下提供了三种图片输入方式，三选一即可
         * 1. 使用公网URL - 适合已有公开可访问的图片
         * 2. 使用本地文件 - 适合本地开发测试
         * 3. 使用Base64编码 - 适合私有图片或需要加密传输的场景
         */
        // 【方式一】使用公网图片 URL
        // String image1 = "https://img.alicdn.com/imgextra/i4/O1CN01IM44WN23dq5uY1yla_!!6000000007279-49-tps-1024-1024.webp";

        // 【方式二】使用本地文件（支持绝对路径和相对路径）
        // 格式要求：file:// + 文件路径
        // String image1 = "file:///path/to/your/image.png";

        // 【方式三】使用Base64编码的图片
        // String image1 = encodeFile("/path/to/your/image.png");

        // 构建文本输入消息（支持文生组图以及图生组图，此处以文生组图为例）
        ImageGenerationMessage message = ImageGenerationMessage.builder()
                .role("user")
                .content(Collections.singletonList(
                        Collections.singletonMap("text", "电影感组图，记录同一只流浪橘猫，特征必须前后一致。第一张：春天，橘猫穿梭在盛开的樱花树下；第二张：夏天，橘猫在老街的树荫下乘凉避暑；第三张：秋天，橘猫踩在满地的金色落叶上；第四张：冬天，橘猫在雪地上走留下足迹。")
                )).build();
        // 图生组图场景：取消以下注释并注释掉上方纯文本构建
        // ImageGenerationMessage message = ImageGenerationMessage.builder()
        //         .role("user")
        //         .content(Arrays.asList(
        //                 Collections.singletonMap("text", "参考图片风格生成四季组图"),
        //                 Collections.singletonMap("image", image1)
        //         )).build();

        ImageGenerationParam param = ImageGenerationParam.builder()
                .apiKey(apiKey)
                .model("wan2.7-image-pro")
                .messages(Collections.singletonList(message))
                .enableSequential(true)
                .n(4)
                .size("2K") // wan2.7-image-pro仅文生图场景支持4K分辨率，图像编辑和组图生成支持最高2K分辨率
                .build();

        ImageGeneration imageGeneration = new ImageGeneration();
        ImageGenerationResult result = null;
        try {
            System.out.println("----sync call, please wait a moment----");
            result = imageGeneration.call(param);
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            throw new RuntimeException(e.getMessage());
        }
        // 提取结果图片URL并保存到本地
        for (int i = 0; i < result.getOutput().getChoices().size(); i++) {
            List<Map<String, Object>> contents = result.getOutput().getChoices().get(i)
                    .getMessage().getContent();
            for (int j = 0; j < contents.size(); j++) {
                if ("image".equals(contents.get(j).get("type"))) {
                    String imageUrl = (String) contents.get(j).get("image");
                    String fileName = "output_" + i + "_" + j + ".png";
                    // 结果URL有效期为24小时，请及时下载
                    try (InputStream in = new URL(imageUrl).openStream()) {
                        Files.copy(in, Paths.get(fileName), StandardCopyOption.REPLACE_EXISTING);
                    }
                    System.out.println("Image saved to " + fileName);
                }
            }
        }
    }

    public static void main(String[] args) throws ApiException, NoApiKeyException, UploadFileException, IOException {
        basicCall();
    }
}
```

##### 响应示例

> URL 有效期24小时，请及时下载并保存图像。

```
{
    "requestId": "4678c314-b37a-91c9-a2ae-2d3cd54bbxxx",
    "usage": {
        "input_tokens": 720,
        "output_tokens": 11,
        "total_tokens": 731,
        "image_count": 4,
        "size": "2048*2048"
    },
    "output": {
        "choices": [
            {
                "finish_reason": "stop",
                "message": {
                    "role": "assistant",
                    "content": [
                        {
                            "image": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxxxxx.png?Expires=xxxxxx",
                            "type": "image"
                        },
                        {
                            "image": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxxxxx.png?Expires=xxxxxx",
                            "type": "image"
                        },
                        {
                            "image": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxxxxx.png?Expires=xxxxxx",
                            "type": "image"
                        },
                        {
                            "image": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxxxxx.png?Expires=xxxxxx",
                            "type": "image"
                        }
                    ]
                }
            }
        ],
        "finished": true
    },
    "status_code": 200,
    "code": "",
    "message": ""
}
```

## **异步调用**

##### 请求示例

```
import com.alibaba.dashscope.aigc.imagegeneration.*;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;
import com.alibaba.dashscope.utils.JsonUtils;

import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.Arrays;
import java.util.Base64;
import java.util.Collections;
import java.util.List;
import java.util.Map;

/**
 * wan2.7-image-pro 组图生成 - 异步调用示例（北京地域）
 */
public class Main {

    static {
        // 以下为北京地域url，各地域的base_url不同
        Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
    }

    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey="sk-xxx"
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    // --- Base64编码函数 ---
    // base64编码格式为 data:{MIME_type};base64,{base64_data}
    public static String encodeFile(String filePath) throws IOException {
        byte[] fileContent = Files.readAllBytes(Paths.get(filePath));
        String base64String = Base64.getEncoder().encodeToString(fileContent);
        String mimeType = Files.probeContentType(Paths.get(filePath));
        return "data:" + mimeType + ";base64," + base64String;
    }

    public static ImageGenerationResult waitTask(String taskId)
            throws ApiException, NoApiKeyException {
        ImageGeneration imageGeneration = new ImageGeneration();
        return imageGeneration.wait(taskId, apiKey);
    }

    public static void asyncCall() throws ApiException, NoApiKeyException, UploadFileException, IOException {
        /*
         * 图像输入方式说明（图生组图场景）：
         * 以下提供了三种图片输入方式，三选一即可
         * 1. 使用公网URL - 适合已有公开可访问的图片
         * 2. 使用本地文件 - 适合本地开发测试
         * 3. 使用Base64编码 - 适合私有图片或需要加密传输的场景
         */
        // 【方式一】使用公网图片 URL
        // String image1 = "https://img.alicdn.com/imgextra/i4/O1CN01IM44WN23dq5uY1yla_!!6000000007279-49-tps-1024-1024.webp";

        // 【方式二】使用本地文件（支持绝对路径和相对路径）
        // 格式要求：file:// + 文件路径
        // String image1 = "file:///path/to/your/image.png";

        // 【方式三】使用Base64编码的图片
        // String image1 = encodeFile("/path/to/your/image.png");

        // 构建文本输入消息（支持文生组图以及图生组图，此处以文生组图为例）
        ImageGenerationMessage message = ImageGenerationMessage.builder()
                .role("user")
                .content(Collections.singletonList(
                        Collections.singletonMap("text", "电影感组图，记录同一只流浪橘猫，特征必须前后一致。第一张：春天，橘猫穿梭在盛开的樱花树下；第二张：夏天，橘猫在老街的树荫下乘凉避暑；第三张：秋天，橘猫踩在满地的金色落叶上；第四张：冬天，橘猫在雪地上走留下足迹。")
                )).build();
        // 图生组图场景：取消以下注释并注释掉上方纯文本构建
        // ImageGenerationMessage message = ImageGenerationMessage.builder()
        //         .role("user")
        //         .content(Arrays.asList(
        //                 Collections.singletonMap("text", "参考图片风格生成四季组图"),
        //                 Collections.singletonMap("image", image1)
        //         )).build();

        ImageGenerationParam param = ImageGenerationParam.builder()
                .apiKey(apiKey)
                .model("wan2.7-image-pro")
                .messages(Collections.singletonList(message))
                .enableSequential(true)
                .n(4)
                .size("2K") // wan2.7-image-pro仅文生图场景支持4K分辨率，图像编辑和组图生成支持最高2K分辨率
                .build();

        ImageGeneration imageGeneration = new ImageGeneration();
        ImageGenerationResult taskResult = null;
        try {
            System.out.println("----async call, creating task----");
            taskResult = imageGeneration.asyncCall(param);
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            throw new RuntimeException(e.getMessage());
        }
        System.out.println("Task created: " + JsonUtils.toJson(taskResult));

        // 等待任务完成
        String taskId = taskResult.getOutput().getTaskId();
        ImageGenerationResult result = waitTask(taskId);
        // 提取结果图片URL并保存到本地
        for (int i = 0; i < result.getOutput().getChoices().size(); i++) {
            List<Map<String, Object>> contents = result.getOutput().getChoices().get(i)
                    .getMessage().getContent();
            for (int j = 0; j < contents.size(); j++) {
                if ("image".equals(contents.get(j).get("type"))) {
                    String imageUrl = (String) contents.get(j).get("image");
                    String fileName = "output_" + i + "_" + j + ".png";
                    // 结果URL有效期为24小时，请及时下载
                    try (InputStream in = new URL(imageUrl).openStream()) {
                        Files.copy(in, Paths.get(fileName), StandardCopyOption.REPLACE_EXISTING);
                    }
                    System.out.println("Image saved to " + fileName);
                }
            }
        }
    }

    public static void main(String[] args) throws ApiException, NoApiKeyException, UploadFileException, IOException {
        asyncCall();
    }
}
```

##### 响应示例

1、创建任务的响应示例

```
{
    "requestId": "7d026dc1-e8c9-9caa-84ac-e82e2da97xxx",
    "output": {
        "task_id": "2de18c56-c151-4b80-8105-1d164733exxx",
        "task_status": "PENDING"
    },
    "status_code": 200,
    "code": "",
    "message": ""
}
```

2、查询任务结果的响应示例

> URL 有效期24小时，请及时下载并保存图像。

```
{
    "requestId": "daea7295-4ce0-928a-9a11-4d2bea058xxx",
    "usage": {
        "input_tokens": 720,
        "output_tokens": 11,
        "total_tokens": 731,
        "image_count": 4,
        "size": "2048*2048"
    },
    "output": {
        "choices": [
            {
                "finish_reason": "stop",
                "message": {
                    "role": "assistant",
                    "content": [
                        {
                            "image": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxxxxx.png?Expires=xxxxxx",
                            "type": "image"
                        },
                        {
                            "image": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxxxxx.png?Expires=xxxxxx",
                            "type": "image"
                        },
                        {
                            "image": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxxxxx.png?Expires=xxxxxx",
                            "type": "image"
                        },
                        {
                            "image": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxxxxx.png?Expires=xxxxxx",
                            "type": "image"
                        }
                    ]
                }
            }
        ],
        "task_id": "2de18c56-c151-4b80-8105-1d164733exxx",
        "task_status": "SUCCEEDED",
        "finished": true,
        "submit_time": "2026-03-31 19:49:53.124",
        "scheduled_time": "2026-03-31 19:49:53.175",
        "end_time": "2026-03-31 19:50:53.160"
    },
    "status_code": 200,
    "code": "",
    "message": ""
}
```

## **计费与限流**

-   模型免费额度和计费单价请参见[模型价格](https://help.aliyun.com/zh/model-studio/model-pricing#e2540d71a2utl)。
    
-   模型限流请参见[万相](https://help.aliyun.com/zh/model-studio/rate-limit#513e0a3df24v7)。
    
-   计费说明：按成功生成的 **图像张数** 计费。模型调用失败或处理错误不产生任何费用，也不消耗[新人免费额度](https://help.aliyun.com/zh/model-studio/new-free-quota)。
    

## **错误码**

如果模型调用失败并返回报错信息，请参见[错误码](https://help.aliyun.com/zh/model-studio/error-code)进行解决。
