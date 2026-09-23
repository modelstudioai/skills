# AI试衣-Plus版API参考

相较于AI试衣-基础版 （ aitryon ） ，aitryon-plus 在 图像清晰度、布料纹理和Logo还原 方面表现更为出色，但生成耗时也相应更长，更适用于对生成结果质量有高要求、对实时性要求不高的场景。

**重要**本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。

**快速入口：** [在线体验](https://bailian.console.aliyun.com/model/experience/vision/imageGenerate?modelId=aitryon-plus) ｜ [AI试衣模型总览](raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md) ｜ [计费与限流](raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/billing-for-outfitanyone.md) ｜ [免费额度](raw/model-user-guide/test-1/new-free-quota.md) ｜ [新手API调用入门指南](raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)

**相关API：**![api](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6710872271/p824099.png) [AI试衣-基础版](raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/outfitanyone-api.md)｜![api](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6710872271/p824099.png)[](https://www.google.com/url?sa=E&q=t2725305.md)[https://www.google.com/url?sa=E&q=t2725305.md](https://www.google.com/url?sa=E&q=t2725305.md)[AI试衣-图片精修](raw/_short/ai-fitting-picture-finishing-api-details-8c8f980f48b3085f.md)｜![api](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6710872271/p824099.png) [AI试衣-图片分割](raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/aitryon-parsing-api.md)

## 模型能力

**多种服饰试穿**

-   **单件上装试穿**：模型随机生成下装，或保留模特原有下装。
    
-   **单件下装试穿**：模型随机生成上装，或保留模特原有上装。
    
-   **上下装组合试穿**：完整替换全身套装。
    
-   **连衣裙/连体衣试穿**
    

**精细化控制**

-   **人脸策略**：可选择保留模特原有人脸，或生成一张全新的随机人脸。
    
-   **指定分辨率**：可指定输出图片的尺寸，或保持与原图一致。
    

## 模型概览

#### 模型简介

**模型名称**

**计费单价**

**限流（主账号与RAM子账号共用）**

**免费额度**[（查看）](raw/model-user-guide/test-1/new-free-quota.md)

**任务下发接口RPS限制**

**同时处理中任务数量**

aitryon-plus

0.50元/张

10

5

400张

**说明**

-   **API兼容性**：aitryon-plus 模型完全兼容 [aitryon](raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/outfitanyone-api.md) 模型的调用方式。如果您已集成 aitryon，只需将请求参数中的 model 字段值修改为 aitryon-plus 即可升级。
-   **计费与限流**：aitryon-plus 与 aitryon 模型的计费标准和调用频率限制不同，详情请参见[AI试衣模型计量计费](raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/billing-for-outfitanyone.md)。

#### 模型效果示意

**输入模特的全身正面照**

**输入服装平铺图**

**生成的试衣效果图**

![test\_client\_tryon](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1760598171/p812706.png)

**上装平铺图**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5286834571/p992716.png)

![test\_client\_tryon](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1760598171/p812707.png)

**下装平铺图**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5286834571/p992717.png)

## 输入图片要求

高质量的输入是高质量输出的保障。在调用API前，请务必确保您的图片符合以下规范。

### 模特图要求

**要求类别**

**详细说明**

图片要求

-   文件大小：5KB ～ 5MB之间
    
-   分辨率：图片宽度和高度均需在 150px ～ 4096px 范围内
    
-   图片格式：支持JPG、JPEG、PNG、BMP、HEIC
    
-   链接要求：上传图片必须为公网可访问的HTTP/HTTPS地址，不支持本地路径
    

模特人物要求

-   人群要求：支持不同性别、肤色、年龄（6岁以上）的人物图
    
-   姿势要求：**人物全身正面照**，光照良好。人物手部展示完整，避免手臂交叉遮挡等情况
    
-   人物要求：保持图片中**有且仅有一个完整的人**
    

#### 正确的人物图示例

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5286834571/p992718.png)

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5286834571/p992719.png)

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1389646171/p801328.png)

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2389646171/p801337.png)

#### 错误的人物图示例

**❌多人照片**

**❌非正面全身照**

**（避免上传侧身、坐姿、躺姿、半身照片）**

**❌人物服装遮挡**

**（避免手持物、包等）**

**❌光线过暗/模糊不清**

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1389646171/p801334.png)

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1389646171/p801546.png)

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2389646171/p801331.png)

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1389646171/p801322.png)

### 服饰图要求

**要求类别**

**详细说明**

图片要求

-   文件大小：5KB ～ 5MB之间
    
-   分辨率：图片宽度和高度均需在 150px ～ 4096px 范围内
    
-   图片格式：支持JPG、JPEG、PNG、BMP、HEIC
    
-   链接要求：上传图片必须为公网可访问的HTTP/HTTPS地址，不支持本地路径
    

服饰要求

-   服饰类型：支持单件上装、下装、连衣裙；支持套装、上下装组合
    
-   服装类目：支持常见服饰品类。不支持内衣、婚纱礼服、特色民族服饰等
    
-   服饰要求：
    
    -   **单件服饰**：服饰平铺拍摄，仅含单件服装
        
    -   **服饰无折叠/遮挡**：衣服应舒展、平整，无褶皱或折叠遮挡
        
    -   **背景简约干净**：图片背景简洁干净、色彩统一，保持服饰主体清晰，无复杂的光照阴影
        
    -   **服饰占比大：**服饰的画面占比尽可能大，四周不宜留白过多，过多的背景留白会降低试衣效果
        

#### 正确的服饰图示例

**上装**

![image.jpeg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1389646171/p801339.jpeg)

![image.jpeg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1389646171/p801341.jpeg)

![image.jpeg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1389646171/p801327.jpeg)

**下装**

![image.jpeg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1389646171/p801340.jpeg)

![image.jpeg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1389646171/p801333.jpeg)

![image.webp](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1389646171/p801330.webp)

**连衣裙/连体服**

![image.webp](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1389646171/p801338.webp)

![image.webp](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1389646171/p801335.webp)

![连衣裙\_2](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6945562571/p978579.jpg)

#### 错误的服饰图示例

❌**多件服装**

❌**非正面照**

❌**折叠遮挡**

❌**服装褶皱**

![image.jpeg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1389646171/p801342.jpeg)

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2389646171/p801323.png)

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1389646171/p801325.png)

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1389646171/p801336.png)

## 前提条件

AI试衣Plus API仅支持通过HTTP进行调用。

在调用前，您需要[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

## HTTP调用

API提供一个异步接口，调用分为两步：

1.  **创建任务**：创建图片生成任务，获取一个唯一的 task\_id。
2.  **查询结果**：使用 task\_id 轮询任务状态，直到任务完成并获取结果。

### 步骤1：创建任务

发送 POST 请求创建试衣任务。

```
POST https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis
```

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

**说明**

-   因该模型调用耗时较长，故采用异步调用的方式创建任务。
-   任务创建后，系统会立即返回一个 `task_id`。在下一步中，需要使用此 task\_id 在**24小时内**查询任务结果。

#### 入参描述

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

API-Key，例如：Bearer sk-xxxx。

Bearer sk-xxxx

X-DashScope-Async

String

Header

是

固定值为 enable，表示使用异步调用方式。

enable

model

String

Body

是

指明需要调用的模型。

aitryon-plus

input.person\_image\_url

String

Body

是

模特人物图片的公网URL。您也可在此[获取临时公网URL](raw/model-api-reference/more-about-models/get-temporary-file-url.md)。

-   5KB≤图像文件≤5M
    
-   150≤图像边长≤4096
    
-   格式支持：jpg、png、jpeg、bmp、heic
    
-   需保持图片中有且仅有一个完整的人
    
-   仅支持HTTP/HTTPS链接，不支持本地路径
    

模特图示例请参见[模特图要求](https://help.aliyun.com/zh/model-studio/aitryon-plus-api#0e7241d97f71g)。

请[点击此处](https://dashscope-swap.oss-cn-beijing.aliyuncs.com/aa-test/aitryon-model-pic/%E6%A8%A1%E7%89%B9%E5%8F%82%E8%80%83%E5%9B%BE.zip)下载我们提供的模特图。

http://aaa/1.jpg

input.top\_garment\_url

String

Body

否

上装/连衣裙服饰图的公网URL。您也可在此[获取临时公网URL](raw/model-api-reference/more-about-models/get-temporary-file-url.md)。

-   5KB≤图像文件≤5M
    
-   150≤图像边长≤4096
    
-   格式支持：jpg、png、jpeg、bmp、heic
    
-   需上传服饰平拍图，保持服饰是单一主体且完整，背景干净，四周不宜留白过多
    
-   仅支持HTTP/HTTPS链接，不支持本地路径
    

服饰图示例请参见[服饰图要求](https://help.aliyun.com/zh/model-studio/aitryon-plus-api#30963a7918m7s)。

-   top\_garment\_url 和 bottom\_garment\_url 至少提供一个。
    
-   如果不传此字段，模型将随机生成上装。
    
-   对于连衣裙/连体衣，请将图片URL填入此字段，并将 bottom\_garment\_url 留空。
    

http://aaa/2.jpg

input.bottom\_garment\_url

String

Body

否

下装服饰图的公网URL。您也可在此[获取临时公网URL](raw/model-api-reference/more-about-models/get-temporary-file-url.md)。

-   5KB≤图像文件≤5M
    
-   150≤图像边长≤4096
    
-   格式支持：jpg、png、jpeg、bmp、heic
    
-   需上传服饰平拍图，保持服饰是单一主体且完整，背景干净，四周不宜留白过多
    
-   仅支持HTTP/HTTPS链接，不支持本地路径
    

服饰图示例请参见[服饰图要求](https://help.aliyun.com/zh/model-studio/aitryon-plus-api#30963a7918m7s)。

-   top\_garment\_url 和 bottom\_garment\_url 至少提供一个。
    
-   如果不传此字段，模型将随机生成下装。
    

http://aaa/3.jpg

parameters.resolution

Int

Body

否

输出图片的分辨率。推荐使用以下值：

-   \-1：默认值，与原图尺寸保持一致。
    
-   1024：表示 576x1024 分辨率。
    
-   1280：表示 720x1280 分辨率。
    

API可能接受其他数值，但使用推荐值可获得最佳效果。

若后续还需调用[AI试衣-图片精修API](raw/_short/ai-fitting-picture-finishing-api-details-8c8f980f48b3085f.md)，此值必须设为 -1。

\-1

parameters.restore\_face

Bool

Body

否

是否还原模特图中的人脸。

-   true：默认值，保留原图人脸。
    
-   false：随机生成一张新的人脸。
    

若后续还需调用[AI试衣-图片精修API](raw/_short/ai-fitting-picture-finishing-api-details-8c8f980f48b3085f.md)，此值必须设为true。

true

#### 出参描述

**字段**

**类型**

**描述**

**示例值**

output.task\_id

String

异步任务的唯一ID。

a8532587-fa8c-4ef8-82be-0c46b17950d1

output.task\_status

String

任务提交后的状态。

PENDING

request\_id

String

本次请求的唯一ID。

7574ee8f-38a3-4b1e-9280-11c33ab46e51

#### 请求示例

#### 试穿 上装

-   **试穿上装**：传入top\_garment\_url（待试穿的上装），模型将**随机**生成下装。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
--header 'X-DashScope-Async: enable' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "aitryon-plus",
    "input": {
        "person_image_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250626/ubznva/model_person.png",
        "top_garment_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250626/epousa/short_sleeve.jpeg"
    },
    "parameters": {
        "resolution": -1,
        "restore_face": true
    }
 }'
```

-   **保留模特原下装**：包含两个步骤，如下：
    
    1.  调用[AI试衣-图片分割API](raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/aitryon-parsing-api.md)，获取模特下装图像URL。
    2.  调用本文的试衣 API，传入 top\_garment\_url（待试穿的上装）和 bottom\_garment\_url（分割获取的下装URL）。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
--header 'X-DashScope-Async: enable' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "aitryon-plus",
    "input": {
        "person_image_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250626/ubznva/model_person.png",
        "top_garment_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250626/epousa/short_sleeve.jpeg",
        "bottom_garment_url": "图片分割API输出的图像URL"
    },
    "parameters": {
        "resolution": -1,
        "restore_face": true
    }
 }'
```

#### 试穿 下装

-   **试穿下装**：传入 bottom\_garment\_url（待试穿的下装），模型将**随机**生成上装。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
--header 'X-DashScope-Async: enable' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "aitryon-plus",
    "input": {
        "person_image_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250626/ubznva/model_person.png",
        "bottom_garment_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250626/rchumi/pants.jpeg"
    },
    "parameters": {
        "resolution": -1,
        "restore_face": true
    }
}'
```

-   **保留模特原上装**：包含两个步骤，如下：
    
    1.  调用[AI试衣-图片分割API](raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/aitryon-parsing-api.md)，获取模特上装图像URL。
    2.  调用本文的试衣 API，传入 top\_garment\_url（分割获取的上装URL） 和 bottom\_garment\_url（待试穿的下装）。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
--header 'X-DashScope-Async: enable' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "aitryon-plus",
    "input": {
        "person_image_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250626/ubznva/model_person.png",
        "top_garment_url": "图片分割API输出的图像URL",
        "bottom_garment_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250626/rchumi/pants.jpeg"
    },
    "parameters": {
        "resolution": -1,
        "restore_face": true
    }
 }'
```

#### 试穿 上下装

-   传入top\_garment\_url（待试穿的上装）和 bottom\_garment\_url（待试穿的下装）。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
--header 'X-DashScope-Async: enable' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "aitryon-plus",
    "input": {
        "person_image_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250626/ubznva/model_person.png",
        "top_garment_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250626/epousa/short_sleeve.jpeg",
        "bottom_garment_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250626/rchumi/pants.jpeg"
    },
    "parameters": {
        "resolution": -1,
        "restore_face": true
    }
}'
```

#### 试穿 连衣裙/连体服

-   对于连衣裙或连体服，仅传入 top\_garment\_url 即可。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
--header 'X-DashScope-Async: enable' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "aitryon-plus",
    "input": {
        "person_image_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250626/ubznva/model_person.png",
        "top_garment_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250626/odngby/dress.jpg"
    },
    "parameters": {
        "resolution": -1,
        "restore_face": true
    }
}'
```

#### 响应示例

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

创建任务失败，请参见[错误码](raw/model-api-reference/preparations/error-code.md)进行解决。

```
{
    "code": "InvalidApiKey",
    "message": "No API-key provided.",
    "request_id": "7438d53d-6eb8-4596-8835-xxxxxx"
}
```

### 步骤2：根据任务ID查询结果

使用上一步获取的 `task_id`，发送 GET 请求查询任务状态和结果。请将 URL 中的`{task_id}` 替换为您的实际任务ID，将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

```
GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}
```

**说明**

-   AI 试衣任务耗时较长（约90秒），建议采用轮询机制，并设置合理的查询间隔（如 3-5 秒）来获取结果。
-   任务成功后返回的 `image_url`有效期为**24小时**，请及时下载并保存图片。
-   此查询接口的默认QPS为20。如需更高频次的查询或事件通知，请[配置异步任务回调](raw/model-api-reference/more-about-models/async-task-api.md)。
-   如需批量查询或取消任务，请参见[管理异步任务](raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。

#### 入参描述

**字段**

**类型**

**传参方式**

**必选**

**描述**

**示例值**

Authorization

String

Header

是

API-Key，例如：Bearer sk-xxx。

Bearer sk-xxx

task\_id

String

Url Path

是

需要查询任务的ID。

a8532587-fa8c-4ef8-82be-0c46b17950d1

#### 出参描述

**字段**

**类型**

**描述**

**示例值**

output.task\_id

String

查询的任务ID。

a8532587-fa8c-4ef8-82be-0c46b17950d1

output.task\_status

String

任务状态。可能的值包括：

-   PENDING 排队中
    
-   PRE-PROCESSING 前置处理中
    
-   RUNNING 处理中
    
-   POST-PROCESSING 后置处理中
    
-   SUCCEEDED 成功
    
-   FAILED 失败
    
-   UNKNOWN 作业不存在或状态未知
    
-   CANCELED：任务取消成功
    

SUCCEEDED

output.image\_url

String

生成的试衣效果图地址。

**image\_url有效期为24小时**，请及时下载。

[https://.../result.jpg?Expires=xxx](https://.../result.jpg?Expires=xxx)

output.submit\_time

String

任务提交时间。

2024-07-30 15:39:39.918

output.scheduled\_time

String

任务执行时间。

2024-07-30 15:39:39.941

output.end\_time

String

任务完成时间。

2024-07-30 15:39:55.080

output.code

String

错误码。任务失败时返回此参数。

InvalidParameter

output.message

String

错误详情。任务失败时返回此参数。

The request is missing required parameters or in a wrong format

usage.image\_count

Int

本次请求生成的图片张数。

1

request\_id

String

本次请求的唯一ID。

7574ee8f-38a3-4b1e-9280-11c33ab46e51

#### 请求示例

将`86ecf553-d340-4e21-xxxxxxxxx`替换为真实的task\_id。

```
curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/86ecf553-d340-4e21-xxxxxxxxx \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

**说明**task\_id 仅支持在**24小时内**查询任务结果，超时会被系统自动清除。

#### 响应示例

#### 成功响应

任务数据（如任务状态、图像URL等）仅保留24小时，超时后会被自动清除。请及时保存生成的图片。

```
{
    "request_id": "98d46cd0-1f90-9231-9a6c-xxxxxx",
    "output": {
        "task_id": "15991992-1487-40d4-ae66-xxxxxx",
        "task_status": "SUCCEEDED",
        "submit_time": "2025-06-30 14:37:53.838",
        "scheduled_time": "2025-06-30 14:37:53.858",
        "end_time": "2025-06-30 14:38:11.472",
        "image_url": "http://dashscope-result-hz.oss-cn-hangzhou.aliyuncs.com/tryon.jpg?Expires=xxx"
    },
    "usage": {
        "image_count": 1
    }
}
```

#### 失败响应

```
{
    "request_id": "6bf4693b-c6d0-933a-b7b7-xxxxxx",
    "output": {
        "task_id": "e32bd911-5a3d-4687-bf53-xxxxxx",
        "task_status": "FAILED",
        "code": "InvalidParameter",
        "message": "The request is missing required parameters xxxxx"
  }
}
```

## 错误码

大模型服务通用状态码请查阅：[错误码](raw/model-api-reference/preparations/error-code.md)。

AI试衣模型特定错误码如下：

**HTTP返回码**

**错误码（code）**

**错误信息（message）**

**含义说明**

400

InvalidParameter

The request is missing required parameters or in a wrong format, please check the parameters that you send.

请求参数缺失或格式错误。请检查您的请求体是否符合API规范。

400

InvalidParameter

Download the media resource timed out during the data inspection process.

图片下载超时。 可能的原因及解决方法如下：

-   网络问题：您的服务器可能与阿里云百炼服务之间的网络不通。请检查网络链接。
    
-   OSS内网URL：阿里云百炼服务无法访问内网地址。请改用OSS公网 URL。
    
-   非中国内地资源：跨境网络访问不稳定。请使用中国内地的存储服务。
    

400

InvalidURL

The request URL is invalid, please check the request URL is available and the request image format is one of the following types: JPEG, JPG, PNG, BMP, and WEBP.

图片URL无效。请检查URL是否为公网地址或者图片格式是否符合要求。

400

InvalidPerson

The input image has no human body or multi human bodies. Please upload other image with single person.

模特图不合规。请确保输入图片中有且仅有一个完整的人。

400

InvalidGarment

Missing clothing image.Please input at least one top garment or bottom garment image.

缺少服饰图片。请至少提供一张上装 (top\_garment\_url) 或下装 (bottom\_garment\_url) 的图片。

400

InvalidInputLength

The image resolution is invalid, please make sure that the largest length of image is smaller than 4096, and the smallest length of image is larger than 150. and the size of image ranges from 5KB to 5MB.

图片尺寸或文件大小不符合要求。请参见[输入图片要求](https://help.aliyun.com/zh/model-studio/aitryon-plus-api#7239603c85fye)。

## 常见问题

### 如何准备模特图和服饰图

1.  **为什么必须使用服装平铺图？**
    
    平铺图能最清晰地展示服装的版型、图案和轮廓，帮助AI准确理解服装结构，从而生成更贴合、更真实的试穿效果。
    
2.  **如果没有服装平铺图怎么办？**
    
    您可以尝试将服装平整地放置在干净的背景上（如地面或墙面）进行俯拍，或者让真人模特/人台穿着后拍摄正面照。关键是确保服装完整、平整、无遮挡。
    
3.  **如何选择合适的模特图？**
    
    选择正面、清晰、完整的全身照。模特穿着的衣物应尽量简洁修身（如T恤+短裤），避免穿着长裙、宽袍大袖或有多层叠穿。同时，确保模特的双手双脚清晰可见，无配饰（如包、伞）遮挡。
    
4.  **如果没有合适的模特图怎么办？**
    
    我们提供了一批符合规范的模特参考图，您可以[点击此处](https://dashscope-swap.oss-cn-beijing.aliyuncs.com/aa-test/aitryon-model-pic/%E6%A8%A1%E7%89%B9%E5%8F%82%E8%80%83%E5%9B%BE.zip)下载使用。
    

### 模型效果不符合预期

1.  **为什么生成的图片效果不佳，缺少细节？**
    
    主要原因可能是输入的服装图质量不高。请确保服装图高清、完整，没有因折叠或拍摄角度问题导致细节丢失。高质量的输入是高质量输出的保障。
    

### 功能使用咨询

1.  **如何为连衣裙或连体衣生成试衣图？**
    
    将连衣裙/连体衣的图片URL填入`input.top_garment_url`字段，并将`input.bottom_garment_url`字段留空或不传。
    

### 计费与限流

AI试衣的计费与限流问题请参见[常见问题](https://help.aliyun.com/zh/model-studio/billing-for-outfitanyone#ab05817cca0ws)。
