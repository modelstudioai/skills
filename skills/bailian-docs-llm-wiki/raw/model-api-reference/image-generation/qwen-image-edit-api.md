# 千问-图像编辑API参考

千问-图像编辑模型支持多图输入和多图输出，可精确修改图内文字、增删或移动物体、改变主体动作、迁移图片风格及增强画面细节。

**快速入口：**[使用指南](https://help.aliyun.com/zh/model-studio/qwen-image-edit-guide) **|** [技术博客](https://qwen.ai/blog?id=1675c295dc29dd31073e5b3f72876e9d684e41c6&from=research.research-list) | [在线体验](https://bailian.console.aliyun.com/?tab=model#/efm/model_experience_center/vision?currentTab=imageGenerate&modelId=qwen-image-edit)

## **模型概览**

**提示词**

**输入图**

**输出图像**

在画面右下角石板路旁、靠近树干根部的位置，以浅灰墨色手写体题写一首七言绝句，字体为行楷风格，笔触自然流畅、略带飞白，大小适中（约占画面高度1/10），与整体水墨淡雅氛围协调。诗文内容为：“青石桥畔柳风轻， 素手拈花闭目听。 一水碧痕浮旧梦， 半篙烟雨入空舲。”诗句横向排列，四句分两行书写（前两句一行，后两句一行），末句“舲”字右下角钤一枚朱红小印，印文为“江南”二字篆书，尺寸约等于单字高度的1/3。

![image (18)-2026-03-10-16-39-59](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3279833771/p1058430.webp)

![image (19)](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3279833771/p1058432.png)

使用图一的城市照片作为底图。请勿更改照片中的真实建筑、街道、车辆或人物。保持照片的真实性。三个图二中的卡通形象在建筑物周围，一个趴在建筑物上方，一个从建筑物的右边探出头来，一个坐在建筑物前的空地上。该形象应采用扁平化的图形风格绘制，轮廓清晰，类似于壁画或海报插图。

![image (15)-combine](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3279833771/p1058424.webp)

![image (17)](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3279833771/p1058425.png)

**模型名称**

**模型简介**

**输出图像规格**

qwen-image-2.0-pro `**推荐**`

> 当前与qwen-image-2.0-pro-2026-04-22能力相同

千问图像生成与编辑模型Pro系列。文字渲染、真实质感、语义遵循能力更强。

> 图像生成请参考[千问-文生图](https://help.aliyun.com/zh/model-studio/qwen-image-api)。

图像分辨率：

-   **可指定**：图像总像素需在512\*512至2048\*2048之间。
    
-   **默认**：总像素数接近 1024\*1024，宽高比与输入图（多图输入时为最后一张）相近。
    

图像格式：png

图像张数：1-6张

qwen-image-2.0-pro-2026-04-22 `**推荐**`

qwen-image-2.0-pro-2026-03-03

qwen-image-2.0 `**推荐**`

> 当前与qwen-image-2.0-2026-03-03能力相同

千问图像生成与编辑模型加速版，兼顾效果与响应速度。

> 图像生成请参考[千问-文生图](https://help.aliyun.com/zh/model-studio/qwen-image-api)。

qwen-image-2.0-2026-03-03 `**推荐**`

qwen-image-edit-max

> 当前与qwen-image-edit-max-2026-01-16能力相同

千问图像编辑Max系列。工业设计、几何推理、角色一致性更强。

图像分辨率：

-   **可指定**：宽和高的取值范围均为`[512, 2048]`像素。
    
-   **默认**：总像素数接近 1024\*1024，宽高比与输入图（多图输入时为最后一张）相近。
    

图像格式：png

图像张数：1-6张

qwen-image-edit-max-2026-01-16

qwen-image-edit-plus

> 当前与qwen-image-edit-plus-2025-10-30能力相同

千问图像编辑Plus系列，支持多图输出与自定义分辨率。

qwen-image-edit-plus-2025-12-15

qwen-image-edit-plus-2025-10-30

qwen-image-edit

支持单图编辑和多图融合。

图像分辨率：**不可指定**。生成规则同上方的**默认**规则。

图像格式：png

图像张数：固定1张

各地域支持的模型请参见[百炼控制台](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market/all)。

## **前提条件**

在调用前，您需要[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

如需通过SDK进行调用，请[安装DashScope SDK](https://help.aliyun.com/zh/model-studio/install-sdk)。目前，该SDK已支持Python和Java。

**重要**

北京和新加坡地域拥有独立的 **API Key** 与**请求地址**，不可混用，跨地域调用将导致鉴权失败或服务报错。

## HTTP调用

**北京地域**：`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

**新加坡地域**：`POST https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

#### 请求参数

## 单图编辑

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--data '{
    "model": "qwen-image-2.0-pro",
    "input": {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260310/jiydyi/image+%2818%29-2026-03-10-16-39-59.webp"
                    },
                    {
                        "text": "在画面右下角石板路旁、靠近树干根部的位置，以浅灰墨色手写体题写一首七言绝句，字体为行楷风格，笔触自然流畅、略带飞白，大小适中（约占画面高度1/10），与整体水墨淡雅氛围协调。诗文内容为：“青石桥畔柳风轻， 素手拈花闭目听。 一水碧痕浮旧梦， 半篙烟雨入空舲。”诗句横向排列，四句分两行书写（前两句一行，后两句一行），末句“舲”字右下角钤一枚朱红小印，印文为“江南”二字篆书，尺寸约等于单字高度的1/3。"
                    }
                ]
            }
        ]
    },
    "parameters": {
        "n": 1,
        "negative_prompt": " ",
        "prompt_extend": true,
        "watermark": false,
        "size": "2048*2048"
    }
}'
```

## 多图融合

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--data '{
    "model": "qwen-image-2.0-pro",
    "input": {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260310/rdsgaa/image+%2815%29.png"
                    },
                    {
                        "image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260310/qokhtl/image+%2816%29.png"
                    },
                    {
                        "text": "使用图一的城市照片作为底图。请勿更改照片中的真实建筑、街道、车辆或人物。保持照片的真实性。三个图二中的卡通形象在建筑物周围，一个趴在建筑物上方，一个从建筑物的右边探出头来，一个坐在建筑物前的空地上。该形象应采用扁平化的图形风格绘制，轮廓清晰，类似于壁画或海报插图。"
                    }
                ]
            }
        ]
    },
    "parameters": {
        "n": 1,
        "negative_prompt": " ",
        "prompt_extend": true,
        "watermark": false,
        "size": "2048*2048"
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

模型名称，示例值qwen-image-2.0-pro。

**input** `_object_` **（必选）**

输入参数对象，包含以下字段：

**属性**

**messages** `_array_` **（必选）**

请求内容数组。**当前仅支持单轮对话**，因此数组内**有且只有一个对象**，该对象包含`role`和`content`两个属性。

**属性**

**role** `_string_` **（必选）**

消息发送者角色，必须设置为`user`。

**content** `_array_` **（必选）**

消息内容，包含1-3张图像，格式为 `{"image": "..."}`；以及单个编辑指令，格式为 `{"text": "..."}`。

**属性**

**image** `_string_` **（必选）**

输入图像的 URL 或 Base64 编码数据。支持传入1-3张图像。

多图输入时，按照数组顺序定义图像顺序，输出图像的比例以最后一张为准。

**图像要求：**

-   图像格式：JPG、JPEG、PNG、BMP、TIFF、WEBP和GIF。
    
    > 输出图像为PNG格式，对于GIF动图，仅处理其第一帧。
    
-   图像分辨率：为获得最佳效果，建议图像的宽和高均在384像素至3072像素之间。分辨率过低可能导致生成效果模糊，过高则会增加处理时长。
    
-   图像大小：不超过10MB。
    

**支持的输入格式**

1.  公网URL：
    
    -   支持 HTTP 和 HTTPS 协议。
        
    -   示例值：`https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/fpakfo/image36.webp`。
        
2.  临时URL：
    
    -   支持OSS协议，必须通过[上传文件获取临时 URL](https://help.aliyun.com/zh/model-studio/get-temporary-file-url)。
        
    -   示例值：`oss://dashscope-instant/xxx/2024-07-18/xxx/cat.png`。
        
3.  传入 Base64 编码图像后的字符串
    
    -   示例值：`data:image/jpeg;base64,GDU7MtCZz...`（示例已截断，仅做演示）
        
    -   Base64 编码规范请参见[通过Base64编码传入图片](#907c84c1a6wrm)。
        

**text** `_string_` **（必选）**

正向提示词用于描述您期望生成的图像内容、风格和构图。

支持中英文，qwen-image-2.0系列模型长度上限为 1300 Token，其他模型为 800 Token，超出部分将自动截断。

**注意**：仅支持传入一个text，不传或传入多个将报错。

**parameters** `_object_` （可选）

控制图像生成的附加参数。

**属性**

**n** `_integer_` （可选）

输出图像的数量，默认值为1。

对于qwen-image-2.0系列、qwen-image-edit-max、qwen-image-edit-plus系列模型，可选择输出1-6张图片。

对于`qwen-image-edit`，仅支持输出1张图片。

**negative\_prompt** `_string_` （可选）

反向提示词，用来描述不希望在画面中看到的内容，可以对画面进行限制。

支持中英文，长度上限500个字符，每个汉字、字母、数字或符号计为一个字符，超过部分会自动截断。

示例值：低分辨率、错误、最差质量、低质量、残缺、多余的手指、比例不良等。

**size** `_string_` （可选）

设置输出图像的分辨率，格式为`宽*高`，例如`"1024*1536"`。

**qwen-image-2.0系列模型**：

-   图像总像素需在512\*512至2048\*2048之间。
    
-   默认总像素数接近 `1024*1024`，宽高比与输入图（多图输入时为最后一张）相近。
    

**qwen-image-edit-max、qwen-image-edit-plus系列模型**：

-   宽和高的取值范围均为\[512, 2048\]像素。
    
-   默认总像素数接近 `1024*1024`，宽高比与输入图（多图输入时为最后一张）相近。
    

> 指定 `size` 参数，系统会以 `size`指定的宽高为目标，将实际输出图像的宽高调整为最接近的16的倍数。例如，设置`1033*1032`，输出图像尺寸为`1040*1024`。

常见比例推荐分辨率

-   1:1: 1024\*1024、1536\*1536
    
-   2:3: 768\*1152、1024\*1536
    
-   3:2: 1152\*768、1536\*1024
    
-   3:4: 960\*1280、1080\*1440
    
-   4:3: 1280\*960、1440\*1080
    
-   9:16: 720\*1280、1080\*1920
    
-   16:9: 1280\*720、1920\*1080
    
-   21:9: 1344\*576、2048\*872
    

**支持模型**：除`qwen-image-edit`以外的模型。

**prompt\_extend** `_boolean_` （可选）

是否开启提示词智能改写，默认值为 `true`。开启后，模型会优化正向提示词（`text`），对描述较简单的提示词效果提升明显。

**支持模型**：除`qwen-image-edit`以外的模型。

**watermark** `_boolean_` （可选）

是否在图像右下角添加 "Qwen-Image" 水印。默认值为 `false`。

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
                            "image": "https://dashscope-result-sz.oss-cn-shenzhen.aliyuncs.com/xxx.png?Expires=xxx"
                        }
                    ],
                    "role": "assistant"
                }
            }
        ]
    },
    "usage": {
        "height": 2048,
        "image_count": 1,
        "width": 2048
    },
    "request_id": "571ae02f-5c9d-436c-83c2-f221e6df0xxx"
}
```

## 任务执行异常

如果因为某种原因导致任务执行失败，将返回相关信息，可以通过code和message字段明确指示错误原因。请参见[错误码](https://help.aliyun.com/zh/model-studio/error-code)进行解决。

```
{
    "request_id": "31f808fd-8eef-9004-xxxxx",
    "code": "InvalidApiKey",
    "message": "Invalid API-key provided."
}
```

**output** `_object_`

包含模型生成结果。

**属性**

**choices** `_array_`

结果选项列表。

**属性**

**finish\_reason** `_string_`

任务停止原因，自然停止时为`stop`。

**message** `_object_`

模型返回的消息。

**属性**

**role** `_string_`

消息的角色，固定为`assistant`。

**content** `_array_`

消息内容，包含生成的图像信息。

**属性**

**image** `_string_`

生成图像的 URL，格式为PNG。**链接有效期为24小时**，请及时下载并保存图像。

**usage** `_object_`

本次调用的资源使用情况，仅调用成功时返回。

**属性**

**image\_count** `_integer_`

生成图像的张数。

**width** `_integer_`

生成图像的宽度（像素）。

**height** `_integer_`

生成图像的高度（像素）。

**request\_id** `_string_`

请求唯一标识。可用于请求明细溯源和问题排查。

**code** `_string_`

请求失败的错误码。请求成功时不会返回此参数，详情请参见[错误码](https://help.aliyun.com/zh/model-studio/error-code)。

**message** `_string_`

请求失败的详细信息。请求成功时不会返回此参数，详情请参见[错误码](https://help.aliyun.com/zh/model-studio/error-code)。

## DashScope SDK调用

SDK 的参数命名与[HTTP接口](#42703589880ts)基本一致，参数结构根据语言特性进行封装，完整参数列表请参见[千问 API 参考](https://help.aliyun.com/zh/model-studio/qwen-api-reference/)。

### Python SDK调用

**说明**

-   推荐安装最新版DashScope Python SDK，否则可能运行报错：[安装或升级SDK](https://help.aliyun.com/zh/model-studio/install-sdk)。
    
-   不支持异步接口。
    

#### **请求示例**

## 通过公网URL传入图片

```
import json
import os
from dashscope import MultiModalConversation
import dashscope

# 以下为中国（北京）地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1
dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

# 模型支持输入1-3张图片
messages = [
    {
        "role": "user",
        "content": [
            {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260310/rdsgaa/image+%2815%29.png"},
            {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260310/qokhtl/image+%2816%29.png"},
            {"text": "使用图一的城市照片作为底图。请勿更改照片中的真实建筑、街道、车辆或人物。保持照片的真实性。三个图二中的卡通形象在建筑物周围，一个趴在建筑物上方，一个从建筑物的右边探出头来，一个坐在建筑物前的空地上。该形象应采用扁平化的图形风格绘制，轮廓清晰，类似于壁画或海报插图。"}
        ]
    }
]

# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 若没有配置环境变量，请用百炼 API Key 将下行替换为：api_key="sk-xxx"
api_key = os.getenv("DASHSCOPE_API_KEY")

# qwen-image-2.0系列、qwen-image-edit-max、qwen-image-edit-plus系列支持输出1-6张图片
response = MultiModalConversation.call(
    api_key=api_key,
    model="qwen-image-2.0-pro",
    messages=messages,
    stream=False,
    n=1,
    watermark=False,
    negative_prompt=" ",
    prompt_extend=True,
    size="2048*2048",
)

if response.status_code == 200:
    # 如需查看完整响应，请取消下行注释
    # print(json.dumps(response, ensure_ascii=False))
    for i, content in enumerate(response.output.choices[0].message.content):
        print(f"输出图像{i+1}的URL:{content['image']}")
else:
    print(f"HTTP返回码：{response.status_code}")
    print(f"错误码：{response.code}")
    print(f"错误信息：{response.message}")
    print("请参考文档：https://help.aliyun.com/zh/model-studio/error-code")
```

## 通过Base64编码传入图片

```
import json
import os
from dashscope import MultiModalConversation
import base64
import mimetypes
import dashscope

# 以下为中国（北京）地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1
dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

# ---用于 Base64 编码 ---
# 格式为 data:{mime_type};base64,{base64_data}
def encode_file(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type or not mime_type.startswith("image/"):
        raise ValueError("不支持或无法识别的图像格式")

    try:
        with open(file_path, "rb") as image_file:
            encoded_string = base64.b64encode(
                image_file.read()).decode('utf-8')
        return f"data:{mime_type};base64,{encoded_string}"
    except IOError as e:
        raise IOError(f"读取文件时出错: {file_path}, 错误: {str(e)}")

# 获取图像的 Base64 编码
# 调用编码函数，请将 "/path/to/your/image.png" 替换为您的本地图片文件路径，否则无法运行
image = encode_file("/path/to/your/image.png")

messages = [
    {
        "role": "user",
        "content": [
            {"image": image},
            {"text": "在画面右下角石板路旁、靠近树干根部的位置，以浅灰墨色手写体题写一首七言绝句，字体为行楷风格，笔触自然流畅、略带飞白，大小适中（约占画面高度1/10），与整体水墨淡雅氛围协调。诗文内容为：“青石桥畔柳风轻， 素手拈花闭目听。 一水碧痕浮旧梦， 半篙烟雨入空舲。”诗句横向排列，四句分两行书写（前两句一行，后两句一行），末句“舲”字右下角钤一枚朱红小印，印文为“江南”二字篆书，尺寸约等于单字高度的1/3。"}
        ]
    }
]

# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 若没有配置环境变量，请用百炼 API Key 将下行替换为：api_key="sk-xxx"
api_key = os.getenv("DASHSCOPE_API_KEY")

# qwen-image-2.0系列、qwen-image-edit-max、qwen-image-edit-plus系列支持输出1-6张图片
response = MultiModalConversation.call(
    api_key=api_key,
    model="qwen-image-2.0-pro",
    messages=messages,
    stream=False,
    n=1,
    watermark=False,
    negative_prompt=" ",
    prompt_extend=True,
    size="2048*2048",
)

if response.status_code == 200:
    # 如需查看完整响应，请取消下行注释
    # print(json.dumps(response, ensure_ascii=False))
    for i, content in enumerate(response.output.choices[0].message.content):
        print(f"输出图像{i+1}的URL:{content['image']}")
else:
    print(f"HTTP返回码：{response.status_code}")
    print(f"错误码：{response.code}")
    print(f"错误信息：{response.message}")
    print("请参考文档：https://help.aliyun.com/zh/model-studio/error-code")
```

## 通过URL下载图像

```
# 需要安装requests以下载图像: pip install requests
import requests

def download_image(image_url, save_path='output.png'):
    try:
        response = requests.get(image_url, stream=True, timeout=300)  # 设置超时
        response.raise_for_status()  # 如果HTTP状态码不是200，则引发异常
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"图像已成功下载到: {save_path}")

    except requests.exceptions.RequestException as e:
        print(f"图像下载失败: {e}")

image_url = "https://dashscope-result-sz.oss-cn-shenzhen.aliyuncs.com/xxx.png?Expires=xxx"
download_image(image_url, save_path='output.png')
```

#### **响应示例**

图像链接的有效期为24小时，请及时下载图像。

> `input_tokens`、`output_tokens`和`characters`为兼容字段，当前固定为0。

```
{
    "status_code": 200,
    "request_id": "959afba6-544e-487e-b58a-6bd9fea97xxx",
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
                            "image": "https://dashscope-result-hz.oss-cn-hangzhou.aliyuncs.com/xxx.png?Expires=xxx"
                        }
                    ]
                }
            }
        ],
        "audio": null
    },
    "usage": {
        "input_tokens": 0,
        "output_tokens": 0,
        "characters": 0,
        "height": 2048,
        "image_count": 1,
        "width": 2048
    }
}
```

### Java SDK调用

**说明**

推荐安装最新版DashScope Java SDK，否则可能运行报错：[安装或升级SDK](https://help.aliyun.com/zh/model-studio/install-sdk)。

#### **请求示例**

## 通过公网URL传入图片

```
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;
import com.alibaba.dashscope.utils.JsonUtils;

import java.io.IOException;
import java.util.*;

public class QwenImageEdit {

    static {
        // 以下为中国（北京）地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1
        Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
    }

    // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    // 若没有配置环境变量，请用百炼 API Key 将下行替换为：apiKey="sk-xxx"
    static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    public static void call() throws ApiException, NoApiKeyException, UploadFileException, IOException {

        MultiModalConversation conv = new MultiModalConversation();

        // 模型支持输入1-3张图片
        MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(
                        Collections.singletonMap("image", "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260310/rdsgaa/image+%2815%29.png"),
                        Collections.singletonMap("image", "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260310/qokhtl/image+%2816%29.png"),
                        Collections.singletonMap("text", "使用图一的城市照片作为底图。请勿更改照片中的真实建筑、街道、车辆或人物。保持照片的真实性。三个图二中的卡通形象在建筑物周围，一个趴在建筑物上方，一个从建筑物的右边探出头来，一个坐在建筑物前的空地上。该形象应采用扁平化的图形风格绘制，轮廓清晰，类似于壁画或海报插图。")
                )).build();
        // qwen-image-2.0系列、qwen-image-edit-max、qwen-image-edit-plus系列支持输出1-6张图片
        Map<String, Object> parameters = new HashMap<>();
        parameters.put("watermark", false);
        parameters.put("negative_prompt", " ");
        parameters.put("n", 1);
        parameters.put("prompt_extend", true);
        parameters.put("size", "2048*2048");

        MultiModalConversationParam param = MultiModalConversationParam.builder()
                .apiKey(apiKey)
                .model("qwen-image-2.0-pro")
                .messages(Collections.singletonList(userMessage))
                .parameters(parameters)
                .build();

        MultiModalConversationResult result = conv.call(param);
        // 如需查看完整响应，请取消下行注释
        // System.out.println(JsonUtils.toJson(result));
        List<Map<String, Object>> contentList = result.getOutput().getChoices().get(0).getMessage().getContent();
        int imageIndex = 1;
        for (Map<String, Object> content : contentList) {
            if (content.containsKey("image")) {
                System.out.println("输出图像" + imageIndex + "的URL：" + content.get("image"));
                imageIndex++;
            }
        }
    }

    public static void main(String[] args) {
        try {
            call();
        } catch (ApiException | NoApiKeyException | UploadFileException | IOException e) {
            System.out.println(e.getMessage());
        }
    }
}
```

## 通过Base64编码传入图片

```
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;
import com.alibaba.dashscope.utils.JsonUtils;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.*;

public class QwenImageEdit {
     
    static {
        // 以下为中国（北京）地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1
        Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
    }
    
    // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    // 若没有配置环境变量，请用百炼 API Key 将下行替换为：apiKey="sk-xxx"
    static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    public static void call() throws ApiException, NoApiKeyException, UploadFileException, IOException {

        // 请将 "/path/to/your/image.png" 替换为您的本地图片文件路径，否则无法运行
        String image = encodeFile("/path/to/your/image.png");

        MultiModalConversation conv = new MultiModalConversation();

        MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(
                        Collections.singletonMap("image", image),
                        Collections.singletonMap("text", "在画面右下角石板路旁、靠近树干根部的位置，以浅灰墨色手写体题写一首七言绝句，字体为行楷风格，笔触自然流畅、略带飞白，大小适中（约占画面高度1/10），与整体水墨淡雅氛围协调。诗文内容为：“青石桥畔柳风轻， 素手拈花闭目听。 一水碧痕浮旧梦， 半篙烟雨入空舲。”诗句横向排列，四句分两行书写（前两句一行，后两句一行），末句“舲”字右下角钤一枚朱红小印，印文为“江南”二字篆书，尺寸约等于单字高度的1/3。")
                )).build();
        // qwen-image-2.0系列、qwen-image-edit-max、qwen-image-edit-plus系列支持输出1-6张图片
        Map<String, Object> parameters = new HashMap<>();
        parameters.put("watermark", false);
        parameters.put("negative_prompt", " ");
        parameters.put("n", 1);
        parameters.put("prompt_extend", true);
        parameters.put("size", "2048*2048");

        MultiModalConversationParam param = MultiModalConversationParam.builder()
                .apiKey(apiKey)
                .model("qwen-image-2.0-pro")
                .messages(Collections.singletonList(userMessage))
                .parameters(parameters)
                .build();

        MultiModalConversationResult result = conv.call(param);
        // 如需查看完整响应，请取消下行注释
        // System.out.println(JsonUtils.toJson(result));
        List<Map<String, Object>> contentList = result.getOutput().getChoices().get(0).getMessage().getContent();
        int imageIndex = 1;
        for (Map<String, Object> content : contentList) {
            if (content.containsKey("image")) {
                System.out.println("输出图像" + imageIndex + "的URL：" + content.get("image"));
                imageIndex++;
            }
        }
    }

    /**
     * 将文件编码为Base64字符串
     * @param filePath 文件路径
     * @return Base64字符串，格式为 data:{mime_type};base64,{base64_data}
     */
    public static String encodeFile(String filePath) {
        Path path = Paths.get(filePath);
        if (!Files.exists(path)) {
            throw new IllegalArgumentException("文件不存在: " + filePath);
        }
        // 检测MIME类型
        String mimeType = null;
        try {
            mimeType = Files.probeContentType(path);
        } catch (IOException e) {
            throw new IllegalArgumentException("无法检测文件类型: " + filePath);
        }
        if (mimeType == null || !mimeType.startsWith("image/")) {
            throw new IllegalArgumentException("不支持或无法识别的图像格式");
        }
        // 读取文件内容并编码
        byte[] fileBytes = null;
        try{
            fileBytes = Files.readAllBytes(path);
        } catch (IOException e) {
            throw new IllegalArgumentException("无法读取文件内容: " + filePath);
        }

        String encodedString = Base64.getEncoder().encodeToString(fileBytes);
        return "data:" + mimeType + ";base64," + encodedString;
    }

    public static void main(String[] args) {
        try {
            call();
        } catch (ApiException | NoApiKeyException | UploadFileException | IOException e) {
            System.out.println(e.getMessage());
        }
    }
}
```

## 通过URL下载图像

```
import java.io.FileOutputStream;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;
 
public class ImageDownloader {
    public static void downloadImage(String imageUrl, String savePath) {
        try {
            URL url = new URL(imageUrl);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setConnectTimeout(5000);
            connection.setReadTimeout(300000);
            connection.setRequestMethod("GET");
            InputStream inputStream = connection.getInputStream();
            FileOutputStream outputStream = new FileOutputStream(savePath);
            byte[] buffer = new byte[8192];
            int bytesRead;
            while ((bytesRead = inputStream.read(buffer)) != -1) {
                outputStream.write(buffer, 0, bytesRead);
            }
            inputStream.close();
            outputStream.close();
 
            System.out.println("图像已成功下载到: " + savePath);
        } catch (Exception e) {
            System.err.println("图像下载失败: " + e.getMessage());
        }
    }
 
    public static void main(String[] args) {
        String imageUrl = "http://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx?Expires=xxx";
        String savePath = "output.png";
        downloadImage(imageUrl, savePath);
    }
}
```

#### **响应示例**

图像链接的有效期为24小时，请及时下载图像。

```
{
    "requestId": "5d5c3260-fc6c-4b4f-8b35-c06366effxxx",
    "usage": {
        "image_count": 1,
        "width": 2048,
        "height": 2048
    },
    "output": {
        "choices": [
            {
                "finish_reason": "stop",
                "message": {
                    "role": "assistant",
                    "content": [
                        {
                            "image": "https://dashscope-result-sz.oss-cn-shenzhen.aliyuncs.com/xxx.png?Expires=xxx"
                        }
                    ]
                }
            }
        ]
    },
    "status_code": 200,
    "code": "",
    "message": ""
}
```

## **错误码**

如果模型调用失败并返回报错信息，请参见[错误码](https://help.aliyun.com/zh/model-studio/error-code)进行解决。

## **计费与限流**

-   模型免费额度和计费单价请参见[选择模型](https://help.aliyun.com/zh/model-studio/models#bfe15d8aa2lxh)。
    
-   模型限流请参见[千问（Qwen-Image）](https://help.aliyun.com/zh/model-studio/rate-limit#f812e7c63axvx)。
    
-   计费说明：按成功生成的 **图像张数** 计费。模型调用失败或处理错误不产生任何费用，也不消耗[新人免费额度](https://help.aliyun.com/zh/model-studio/new-free-quota)。
    

## **常见问题**

#### **Q：千问图像编辑模型支持哪些语言？**

A：目前正式支持**简体中文和英文**；其他语言可自行尝试，但效果存在不确定性。

##### **Q: 如何查看模型调用量？**

A: 模型调用完一小时后，请在[**模型监控**（北京）](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/model-telemetry)或[**模型监控**（新加坡）](https://modelstudio.console.aliyun.com/ap-southeast-1?tab=dashboard#/model-telemetry) 页面，查看模型的调用次数、成功率等指标。详情请参见[账单查询与成本管理](https://help.aliyun.com/zh/model-studio/bill-query-and-cost-management)。

##### **Q：如何获取图像存储的访问域名白名单？**

A： 模型生成的图像存储于阿里云OSS，API将返回一个临时的公网URL。**若需要对该下载地址进行防火墙白名单配置**，请注意：由于底层存储会根据业务情况进行动态变更，为避免过期信息影响访问，文档不提供固定的OSS域名白名单。如有安全管控需求，请联系客户经理获取最新OSS域名列表。
