# AI试衣-图片分割API参考

AI 试衣-图片分割是一个辅助模型，支持从模特图或 AI 试衣图中分割出服装区域，如上装、下装、连衣裙或连体衣。此模型为可选模型，与 AI 试衣模型配合使用，可实现 局部试衣 、 获取指定服饰坐标 等特定效果。

**重要**本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。

**快速入口：** [在线体验](https://bailian.console.aliyun.com/model/experience/vision/imageGenerate) ｜ [AI试衣模型总览](raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md) ｜ [计费与限流](raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/billing-for-outfitanyone.md) ｜ [免费额度](raw/model-user-guide/test-1/new-free-quota.md)

**相关API：**![api](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6710872271/p824099.png) [AI试衣-基础版](raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/outfitanyone-api.md)｜![api](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6710872271/p824099.png) [AI试衣-Plus版](raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/aitryon-plus-api.md)｜![api](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6710872271/p824099.png)[](https://www.google.com/url?sa=E&q=t2725305.md)[https://www.google.com/url?sa=E&q=t2725305.md](https://www.google.com/url?sa=E&q=t2725305.md)[AI试衣-图片精修](raw/_short/ai-fitting-picture-finishing-api-details-8c8f980f48b3085f.md)

## 模型概览

**模型名称**

**计费单价**

**限流（主账号与RAM子账号共用）**

**免费额度**[（查看）](raw/model-user-guide/test-1/new-free-quota.md)

**任务下发接口RPS限制**

**同时处理中任务数量**

aitryon-parsing-v1

0.004元/张

10

无限制 (同步接口)

400张

更多详情请参见[计量计费](raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/billing-for-outfitanyone.md)。

## 核心输出图解

调用本 API 后，您将获得三个核心参数输出。下面以“**分割一件上衣**”为例，展示了每个参数的含义和用途。

**输入**

**输出**

**输出参数**

**可视化示例**

**含义及用途**

![1](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2670447371/p906743.png)

-   输入模特图
-   选择服饰类型为上衣

> "clothes\_type": \["upper"\]

**crop\_img\_url**

![3](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2670447371/p906744.png)

-   **分割后的服饰图（RGB）**：本示例为穿着上衣的模特服饰图。
-   作为 AI 试衣模型的输入参数，用于局部试衣场景。
-   URL有效期为24小时，请及时下载并保存。

**parsing\_img\_url**

![4](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2670447371/p906843.png)

-   **分割后的服饰图（RGBA）**：本示例为分割出来的上衣图。
-   用于效果预览，直观验证分割结果是否准确。
-   URL有效期为24小时，请及时下载并保存。

**bbox**

bbox值：\[\[331, 239,641,637\]\]

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0495562571/p983797.png)

> 此图展示 bbox 值与原图坐标的对应关系，并非模型输出。

-   **边界框（bounding box）**：分割后的服饰图（parsing\_img\_url）在输入模特图中的矩形区域坐标。
    
    -   **bbox数组的**元素格式为 \[x1, y1, x2, y2\]，代表边界框的左上角和右下角坐标。
    -   坐标原点 (0,0) 为输入模特图的左上角。
-   用于实现前端交互功能（如商品热区）。
    

## 使用场景

### 场景一：局部试衣

**目标**：替换模特的部分服饰（上装或下装），保留另一部分衣物不变。此场景需要先分割模特图。

##### 示例：保留模特上装，替换下装

1.  **分割模特图，提取上衣**
    
    -   调用本文的图片分割 API，输入原始模特图，设置参数 clothes\_type 为 \["upper"\]，提取模特上衣。
    -   API 返回包含上衣的服饰图（ crop\_img\_url）。
    
    **输入：模特图**
    
    **输出：分割后的服饰图（crop\_img\_url）**
    
    ![1](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2670447371/p906743.png)
    
    ![3](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2670447371/p906744.png)
    
2.  **试衣图片生成**
    
    -   调用 [AI试衣-Plus版](raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/aitryon-plus-api.md)或[AI试衣-基础版](raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/outfitanyone-api.md);
    -   输入模特图、服饰上装图（由分割获得）、服饰下装图，获得最终的试衣效果图。
    
    **输入**
    
    **输出：试衣效果图**
    
    **模特图**
    
    **服饰上装图**
    
    **服饰下装图**
    
    ![1](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2670447371/p906754.png)
    
    与图片分割API输入保持一致模特图
    
    ![3](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2670447371/p906755.png)
    
    图片分割API的出参crop\_img\_url
    
    ![2](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2670447371/p906756.png)
    
    需替换的服饰图
    
    ![5](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2670447371/p906766.png)
    

### 场景二：获取指定服饰的坐标

**目标**：在模特图或AI试衣效果图上，获取指定服饰的边界框（bbox）坐标。这些坐标可用于添加商品标签或创建交互热区。

##### 示例：获取上衣的坐标

1.  **准备输入图片**：输入图片可为 模特图 或 AI试衣生成的效果图。输入图像要求请参见[模特图要求](https://help.aliyun.com/zh/model-studio/aitryon-plus-api#0e7241d97f71g)。
    
2.  **分割图片，获取坐标**：设置输入图片的分割类型，例如，设为 \["upper"\] 分割并定位上衣，获得所需区域的bbox。
    
    **输入：模特图或试衣效果图**
    
    **输出：分割后的服饰图和坐标范围**
    
    ![1](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2670447371/p906743.png)
    
    入参"clothes\_type": \["upper"\]
    
    ![4](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2670447371/p906843.png)
    
    -   parsing\_img\_url：可视化分割结果的 URL。
        
    -   bbox：该分割区域的边界框坐标，例如，\[\[331, 239,641,637\]\]。
        
    

## 前提条件

AI试衣-图片分割API仅支持通过HTTP进行调用。

在调用前，您需要[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

## HTTP调用

### 请求接口

```
POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/vision/image-process/process
```

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

### 入参描述

**字段**

**类型**

**传参方式**

**必选**

**描述**

**示例值**

Content-Type

String

Header

是

请求类型：application/json。

application/json

Authorization

String

Header

是

API-Key，格式为 Bearer sk-xxxx。

Bearer sk-xxxx

model

String

Body

是

指定调用的模型，固定为aitryon-parsing-v1。

aitryon-parsing-v1

input.image\_url

String

Body

是

待分割的模特图公网 URL。 您也可在此[获取临时公网URL](raw/model-api-reference/more-about-models/get-temporary-file-url.md)。

-   5KB≤图像文件≤5M
    
-   150≤图像边长≤4096
    
-   格式支持：jpg、png、jpeg、bmp、heic
    
-   需保持图片中有且仅有一个完整的人
    
-   仅支持HTTP/HTTPS链接，不支持本地路径
    

模特图示例请详见[模特图要求](https://help.aliyun.com/zh/model-studio/aitryon-plus-api#0e7241d97f71g)。

http://a/a.jpg

parameters.clothes\_type

List\[String\]

Body

否

指定需要分割类型。默认为 \["upper"\]（上装）。

列表的长度和顺序决定了输出结果中 URL 列表的长度和顺序。

可选值为：

-   \["upper"\]：表示分割上装。
    
-   \["lower"\]：表示分割下装。
    
-   \["dress"\]：表示连衣裙或连体衣或全身穿搭。
    
-   \["upper", "lower"\]：表示分割上装和下装。
    

\["upper"\]

### 出参描述

**字段**

**类型**

**描述**

**示例值**

output.parsing\_img\_url

List\[String\]

分割区域的可视化图片 URL 列表。

长度和顺序与入参 clothes\_type 保持一致。如果未检测到对应服饰，则该位置为 None/null。

图片通道数为RGBA，保存为PNG格式，

\["[http://a/a.png](http://a/a.png)"\]

\[null\] 或者 \[None\]

output.crop\_img\_url

List\[String\]

分割出的服饰图片 URL 列表。

长度和顺序与入参 clothes\_type 保持一致。如果未找到对应服饰，则该位置为 None/null。

图片为RGB格式。

\["[http://a/a.png](http://a/a.png)"\]

\[null\] 或者 \[None\]

output.bbox

List\[Integer\]

分割区域在原图中位置的坐标列表。

按照入参 clothes\_type 中指定分割的区域顺序排序。

每个bbox定义为 \[x1, y1, x2, y2\]，以输入原图的左上角为坐标原点，分别代表左上角和右下角的坐标。

\[\[10,20,30,40\], \[50,60,70,80\]\]

usage.image\_count

Integer

本次请求检测的图片张数。

1

request\_id

String

本次请求的唯一 ID。

7574ee8f-38a3-4b1e-9280-11c33ab46e51

### 请求示例

#### 分割模特图的上装

```
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/vision/image-process/process' \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--data '{
  "model": "aitryon-parsing-v1",
  "input": {
      "image_url":"https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250630/bakbqz/aitryon_parse_model.png"
  },
  "parameters": {
      "clothes_type": ["upper"]
  }
}'
```

### 响应示例

#### 成功响应（ 存在对应类型服饰 ）

`parsing_img_url`和`crop_img_url`有效期为24小时，请及时下载。

```
{
    "output": {
        "bbox": [[331, 239,641,637]],
        "parsing_img_url": ["http://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/example_parsing_img.png?Expires=xxxx"],
        "crop_img_url": ["http://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/example_crop_img.jpg?Expires=xxxx"]
    },
    "usage": {
        "image_count": 1
    },
    "request_id": "b68147d6-e7d0-920f-b889-xxxxxx"
}
```

#### 成功响应（不 存在对应类型服饰 ）

```
{
    "output":{
        "bbox":[null],
        "parsing_img_url":[null],
        "crop_img_url":[null]
    },
    "usage":{
        "image_count":1
    },
    "request_id":"c56f62df-724e-9c19-96bd-308627cf5262"
}
```

#### 失败响应

```
{
    "request_id": "1d075a37-3768-9bc9-b781-xxxx",
    "code": "InvalidParameter.ClothesType",
    "message": "The request parameter is invalid, please check the request parameter."
}
```

## 错误码

大模型服务平台通用状态码请查阅：[错误码](raw/model-api-reference/preparations/error-code.md)。

## 常见问题

### 计费与限流

AI试衣的计费与限流问题请参见[常见问题](https://help.aliyun.com/zh/model-studio/billing-for-outfitanyone#ab05817cca0ws)。
