# 万相-通用图像编辑API参考

本文介绍万相-通用图像编辑模型的输入输出参数。

**重要**

本文档仅适用于“中国内地（北京）”地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)。

该模型通过简单的指令即可实现多样化的图像编辑，适用于扩图、去水印、风格迁移、图像修复、图像美化等场景。 当前支持以下功能：

-   **图像风格化**：全局风格化、局部风格化。
    
-   **图像内容编辑**：指令编辑（无需指定区域，仅通过指令增加/修改图片内容）、局部重绘（针对指定区域增加/删除/修改图片内容）、去文字水印（中英文）。
    
-   **图像尺寸与分辨率优化**：扩图（按比例扩图）、图像超分（高清放大）。
    
-   **图像色彩处理**：图像上色（黑白或灰度图像转为彩色图像）。
    
-   **基于参考图像生成**：线稿生图（先提取输入图像的线稿，再参考线稿生成图像）、参考卡通形象生图。
    

**相关指南**：[图像编辑-万相2.1](https://help.aliyun.com/zh/model-studio/wanx-image-edit)

## 模型概览

**模型名称**

**计费单价**

**限流（主账号与RAM子账号共用）**

**免费额度**[（查看）](https://help.aliyun.com/zh/model-studio/new-free-quota)

**任务下发接口RPS限制**

**同时处理中任务数量**

wanx2.1-imageedit

0.14元/张

2

2

500张

更多说明请参见[模型计费与限流](https://help.aliyun.com/zh/model-studio/image-faq#3436cf2280fnh)。

## **模型效果**

**模型功能**

**输入图像**

**输入提示词**

**输出图像**

**全局风格化**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9206061571/p930138.png)

转换成法国绘本风格

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9206061571/p930139.png)

**局部风格化**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9206061571/p930188.png)

把房子变成木板风格。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9206061571/p930413.png)

**指令编辑**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9206061571/p942602.png)

把她的头发修改为红色。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9206061571/p942603.png)

**局部重绘**

输入图像

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9206061571/p930416.png)

输入涂抹区域图像（白色为涂抹区域）

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9206061571/p930417.png)

一只陶瓷兔子抱着一朵陶瓷花。

输出图像

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9206061571/p930415.png)

**去文字水印**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9206061571/p930146.png)

去除图像中的文字。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9206061571/p930418.png)

**扩图**

![20250319105917](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9206061571/p930580.jpg)

一位绿色仙子。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9206061571/p930750.png)

**图像超分**

模糊图像

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9206061571/p930151.png)

图像超分。

清晰图像

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9206061571/p930152.png)

**图像上色**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9206061571/p930149.png)

蓝色背景，黄色的叶子。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9206061571/p930150.png)

**线稿生图**

输入图像

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9206061571/p930155.png)

北欧极简风格的客厅。

提取原图的线稿并生成图像

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9206061571/p930156.png)

**参考卡通形象生图**

输入参考图（卡通形象）

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9206061571/p930153.png)

卡通形象小心翼翼地探出头，窥视着房间内一颗璀璨的蓝色宝石。

输出图像

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9206061571/p930154.png)

## 前提条件

万相-通用图像编辑API支持通过HTTP和DashScope SDK进行调用。

在调用前，您需要[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

如需通过SDK进行调用，请[安装DashScope SDK](https://help.aliyun.com/zh/model-studio/install-sdk)。目前，该SDK已支持Python和Java。

## HTTP调用

图像模型处理时间较长，为了避免请求超时，HTTP调用仅支持异步获取模型结果。您需要发起两个请求：

1.  **创建任务获取任务ID**：首先发起创建任务请求，该请求会返回任务ID（task\_id）。
    
2.  **根据任务ID查询结果**：使用上一步获得的任务ID，查询任务状态及结果。任务成功执行时将返回图像URL，有效期24小时。
    

**说明**

创建任务后，该任务将被加入到排队队列，等待调度执行。后续需要调用“根据任务ID查询结果接口”获取任务状态及结果。

> 通用图像编辑模型大约需要5-15秒。实际耗时取决于排队任务数量和网络状况，请您在获取结果时耐心等待。

### 步骤1：创建任务获取任务ID

`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis`

#### 请求参数

## **全局风格化**

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
--header 'X-DashScope-Async: enable' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
  "model": "wanx2.1-imageedit",
  "input": {
    "function": "stylization_all",
    "prompt": "转换成法国绘本风格",
    "base_image_url": "http://wanx.alicdn.com/material/20250318/stylization_all_1.jpeg"
  },
  "parameters": {
    "n": 1
  }
}'
```

## 传入本地文件（base64）

下面以全局风格化为例，展示Base64传参示例。

由于 Base64 编码后的字符串较长，请下载[image\_base64](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250722/lzyoev/stylization_image_base64.txt)，并将文本内容全部复制到`base_image_url`参数中。

数据格式详见[传值方式](#c92c9077cbebb)。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
--header 'X-DashScope-Async: enable' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
  "model": "wanx2.1-imageedit",
  "input": {
    "function": "stylization_all",
    "prompt": "转换成法国绘本风格",
    "base_image_url": "data:image/jpeg;base64,/9j/4AAQSkZJR......"
  },
  "parameters": {
    "n": 1
  }
}'
```

## 局部风格化

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
--header 'X-DashScope-Async: enable' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
  "model": "wanx2.1-imageedit",
  "input": {
    "function": "stylization_local",
    "prompt": "把房子变成木板风格。",
    "base_image_url": "http://wanx.alicdn.com/material/20250318/stylization_local_1.png"
  },
  "parameters": {
    "n": 1
  }
}'
```

## 指令编辑

功能描述：无需指定区域，仅通过指令进行增加/修改图片内容的操作。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
--header 'X-DashScope-Async: enable' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
  "model": "wanx2.1-imageedit",
  "input": {
    "function": "description_edit",
    "prompt": "把她的头发修改为红色。",
    "base_image_url": "http://wanx.alicdn.com/material/20250318/description_edit_2.png"
  },
  "parameters": {
    "n": 1
  }
}'
```

## 局部重绘

功能描述：针对指定区域增加/删除/修改图片内容。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
--header 'X-DashScope-Async: enable' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
  "model": "wanx2.1-imageedit",
  "input": {
    "function": "description_edit_with_mask",
    "prompt": "陶瓷兔子拿着陶瓷小花。",
    "base_image_url": "http://wanx.alicdn.com/material/20250318/description_edit_with_mask_3.jpeg",
    "mask_image_url": "http://wanx.alicdn.com/material/20250318/description_edit_with_mask_3_mask.png"
  },
  "parameters": {
    "n": 1
  }
}'
```

## 去文字水印

功能描述：支持去除中英文的文字水印。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
--header 'X-DashScope-Async: enable' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
  "model": "wanx2.1-imageedit",
  "input": {
    "function": "remove_watermark",
    "prompt": "去除图像中的文字",
    "base_image_url": "http://wanx.alicdn.com/material/20250318/remove_watermark_1.png"
  },
  "parameters": {
    "n": 1
  }
}'
```

## 扩图

功能描述：支持在上、下、左、右四个方向按比例扩图。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
--header 'X-DashScope-Async: enable' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
  "model": "wanx2.1-imageedit",
  "input": {
    "function": "expand",
    "prompt": "一位绿色仙子",
    "base_image_url": "http://wanx.alicdn.com/material/20250318/expand_2.jpg"
  },
  "parameters": {
    "top_scale": 1.5,
    "bottom_scale": 1.5,
    "left_scale": 1.5,
    "right_scale": 1.5,
    "n": 1
  }
}'
```

## 图像超分

功能描述：支持将模糊图像进行高清放大。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
--header 'X-DashScope-Async: enable' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
  "model": "wanx2.1-imageedit",
  "input": {
    "function": "super_resolution",
    "prompt": "图像超分。",
    "base_image_url": "http://wanx.alicdn.com/material/20250318/super_resolution_1.jpeg"  
  },
  "parameters": {
    "upscale_factor": 2,
    "n": 1
  }
}'
```

## 图像上色

功能描述：黑白或灰度图像转为彩色图像。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
--header 'X-DashScope-Async: enable' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
  "model": "wanx2.1-imageedit",
  "input": {
    "function": "colorization",
    "prompt": "蓝色背景，黄色的叶子。",
    "base_image_url": "http://wanx.alicdn.com/material/20250318/colorization_1.jpeg"  
  },
  "parameters": {
    "n": 1
  }
}'
```

## 线稿生图

功能描述：先提取输入图像的线稿，再参考线稿生成图像。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
--header 'X-DashScope-Async: enable' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
  "model": "wanx2.1-imageedit",
  "input": {
    "function": "doodle",
    "prompt": "北欧极简风格的客厅。",
    "base_image_url": "http://wanx.alicdn.com/material/20250318/doodle_1.png"
  },
  "parameters": {
    "n": 1
  }
}'
```

## 参考卡通形象生图

功能描述：支持参考卡通形象生成图像。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
--header 'X-DashScope-Async: enable' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
  "model": "wanx2.1-imageedit",
  "input": {
    "function": "control_cartoon_feature",
    "prompt": "卡通形象小心翼翼地探出头，窥视着房间内一颗璀璨的蓝色宝石。",
    "base_image_url": "http://wanx.alicdn.com/material/20250318/control_cartoon_feature_1.png"
  },
  "parameters": {
    "n": 1
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

模型名称。示例值：wanx2.1-imageedit。

**input** `_object_` **（必选）**

输入的基本信息，如提示词等。

**属性**

**prompt** `_string_` **（必选）**

提示词，用来描述生成图像中期望包含的元素和视觉特点。

支持中英文，长度不超过800个字符，每个汉字/字母占一个字符，超过部分会自动截断。

> 不同功能的提示词存在差异，建议根据具体功能参考相应的技巧说明。

**function** `_string_` **（必选）**

图像编辑功能。目前支持的功能有：

-   stylization\_all：全局风格化，当前支持2种风格。[风格和提示词技巧](https://help.aliyun.com/zh/model-studio/wanx-image-edit#3be4a1e9569kk)
    
-   stylization\_local：局部风格化，当前支持8种风格。[风格和提示词技巧](https://help.aliyun.com/zh/model-studio/wanx-image-edit#9b8864717b5al)
    
-   description\_edit：指令编辑。通过指令即可编辑图像，简单编辑任务优先推荐这种方式。[提示词技巧](https://help.aliyun.com/zh/model-studio/wanx-image-edit#0c932e6efebf7)
    
-   description\_edit\_with\_mask：局部重绘。需要指定编辑区域，适合对编辑范围有精确控制的场景。[提示词技巧](https://help.aliyun.com/zh/model-studio/wanx-image-edit#346e4ebb1ctjj)
    
-   remove\_watermark：去文字水印。[提示词技巧](https://help.aliyun.com/zh/model-studio/wanx-image-edit#c82e609a4f0bq)
    
-   expand：扩图。[提示词技巧](https://help.aliyun.com/zh/model-studio/wanx-image-edit#4bd67e438bnuv)
    
-   super\_resolution：图像超分。[提示词技巧](https://help.aliyun.com/zh/model-studio/wanx-image-edit#b438794ec2agn)
    
-   colorization：图像上色。[提示词技巧](https://help.aliyun.com/zh/model-studio/wanx-image-edit#ade6bb5d8d28j)
    
-   doodle：线稿生图。[提示词技巧](https://help.aliyun.com/zh/model-studio/wanx-image-edit#b78933f9e819x)
    
-   control\_cartoon\_feature：参考卡通形象生图。[提示词技巧](https://help.aliyun.com/zh/model-studio/wanx-image-edit#ee9063aeaeagf)
    

**base\_image\_url** `_string_` **（必选）**

输入图像的URL或 Base64 编码数据。

图像限制：

-   图像格式：JPG、JPEG、PNG、BMP、TIFF、WEBP。
    
-   图像分辨率：图像的宽度和高度范围为\[512, 4096\]像素。
    
-   图像大小：不超过10MB。
    
-   URL地址中不能包含中文字符。
    

输入图像说明：

1.  使用公网可访问URL
    
    -   支持 HTTP 或 HTTPS 协议。您也可在此[获取临时公网URL](https://help.aliyun.com/zh/model-studio/get-temporary-file-url)。
        
    -   示例值：`http://wanx.alicdn.com/material/20250318/stylization_all_1.jpeg`。
        
2.  传入 Base64 编码图像后的字符串
    
    -   数据格式：`data:{MIME_type};base64,{base64_data}`。
        
    -   示例值：`data:image/jpeg;base64,GDU7MtCZzEbTbmRZ......`。
        
    -   示例中的编码字符串不完整，仅做演示，更多内容请参见[传值方式](#c92c9077cbebb)。
        

**mask\_image\_url** `_string_` （可选）

仅当`**function**`设置为`**description_edit_with_mask**`（局部重绘）时必填，其余情况无需填写。

涂抹区域图像的URL或 Base64 编码数据。

支持传入公网可访问的 URL（HTTP/HTTPS）或 Base64 编码字符串，更多内容请参见[传值方式](#c92c9077cbebb)。

涂抹区域图像要求：

-   图像分辨率 ：必须与`base_image_url`的图像分辨率保持一致。图像宽度和高度需在\[512, 4096\]像素之间。
    
-   图像格式 ：支持JPG、JPEG、PNG、BMP、TIFF、WEBP。
    
-   图像大小 ：不超过10MB。
    
-   URL地址中不能包含中文字符。
    

涂抹区域颜色要求：

-   白色区域 ：表示需要编辑的部分，必须使用纯白色（RGB值为\[255,255,255\]），否则可能无法正确识别。
    
-   黑色区域：表示无需改变的部分，必须使用纯黑色（RGB值为\[0,0,0\]），否则可能无法正确识别。
    

关于如何获取涂抹区域图像：使用PS抠图或其他工具生成黑白涂抹图像。

**parameters** `_object_` （可选）

图像处理参数。

**属性**

## 通用

**n** `_integer_` （可选）

生成图片的数量。取值范围为1~4张，默认为1。

**seed** `_integer_` （可选）

随机数种子，用于控制模型生成内容的随机性。seed参数取值范围是`[0, 2147483647]`。

如果不提供，则算法自动生成一个随机数作为种子。如果您希望生成内容保持相对稳定，请使用相同的seed参数值。

**watermark** `_bool_` （可选）

是否添加水印标识，水印位于图片右下角，文案为“AI生成”。

-   false：默认值，不添加水印。
    
-   true：添加水印。
    

## 全局风格化

**n** `_integer_` （可选）

生成图片的数量。取值范围为1~4张，默认为1。

**seed** `_integer_` （可选）

随机数种子，用于控制模型生成内容的随机性。seed参数取值范围是`[0, 2147483647]`。

如果不提供，则算法自动生成一个随机数作为种子。如果您希望生成内容保持相对稳定，请使用相同的seed参数值。

**watermark** `_bool_` （可选）

是否添加水印标识，水印位于图片右下角，文案为“AI生成”。

-   false：默认值，不添加水印。
    
-   true：添加水印。
    

**strength** `_float_` （可选）

当`**function**`设置为 `**stylization_all**`（全局风格化）时填写。

图像修改幅度。取值范围\[0.0 1.0\]，默认值为0.5。

值越接近0，则越接近原图效果；值越接近1，对原图的修改幅度越大。

## 指令编辑

**n** `_integer_` （可选）

生成图片的数量。取值范围为1~4张，默认为1。

**seed** `_integer_` （可选）

随机数种子，用于控制模型生成内容的随机性。seed参数取值范围是`[0, 2147483647]`。

如果不提供，则算法自动生成一个随机数作为种子。如果您希望生成内容保持相对稳定，请使用相同的seed参数值。

**watermark** `_bool_` （可选）

是否添加水印标识，水印位于图片右下角，文案为“AI生成”。

-   false：默认值，不添加水印。
    
-   true：添加水印。
    

**strength** `_float_` （可选）

当`**function**`设置为`**description_edit**`（指令编辑）时填写。

图像修改幅度。取值范围\[0.0, 1.0\]，默认值为0.5。

值越接近0，则越接近原图效果；值越接近1，对原图的修改幅度越大。

## 扩图

**n** `_integer_` （可选）

生成图片的数量。取值范围为1~4张，默认为1。

**seed** `_integer_` （可选）

随机数种子，用于控制模型生成内容的随机性。seed参数取值范围是`[0, 2147483647]`。

如果不提供，则算法自动生成一个随机数作为种子。如果您希望生成内容保持相对稳定，请使用相同的seed参数值。

**watermark** `_bool_` （可选）

是否添加水印标识，水印位于图片右下角，文案为“AI生成”。

-   false：默认值，不添加水印。
    
-   true：添加水印。
    

**top\_scale** `_float_` （可选）

当`**function**`设置为`**expand**`（扩图）时才需填写。

图像居中，向上按比例扩展图像。默认值为1.0，取值范围\[1.0, 2.0\]。

**bottom\_scale** `_float_` （可选）

当`**function**`设置为`**expand**`（扩图）时才需填写。

图像居中，向下按比例扩展图像。默认值为1.0，取值范围\[1.0, 2.0\]。

**left\_scale** `_float_` （可选）

当`**function**`设置为`**expand**`（扩图）时才需填写。

图像居中，向左按比例扩展图像。默认值为1.0，取值范围\[1.0, 2.0\]。

**right\_scale** `_float_` （可选）

当`**function**`设置为`**expand**`（扩图）时才需填写。

图像居中，向右按比例扩展图像。默认值为1.0，取值范围\[1.0, 2.0\]。

## 图像超分

**n** `_integer_` （可选）

生成图片的数量。取值范围为1~4张，默认为1。

**seed** `_integer_` （可选）

随机数种子，用于控制模型生成内容的随机性。seed参数取值范围是`[0, 2147483647]`。

如果不提供，则算法自动生成一个随机数作为种子。如果您希望生成内容保持相对稳定，请使用相同的seed参数值。

**watermark** `_bool_` （可选）

是否添加水印标识，水印位于图片右下角，文案为“AI生成”。

-   false：默认值，不添加水印。
    
-   true：添加水印。
    

**upscale\_factor** `_integer_` （可选）

当`**function**`设置为`**super_resolution**`（图像超分）时才需填写。

图像超分的放大倍数。在放大图像的同时增强细节，提升图像分辨率，实现高清处理。

取值范围为1~4，默认值为1。当upscale\_factor设置为1时，仅对图像进行高清处理，不进行放大。

## 线稿生图

**n** `_integer_` （可选）

生成图片的数量。取值范围为1~4张，默认为1。

**seed** `_integer_` （可选）

随机数种子，用于控制模型生成内容的随机性。seed参数取值范围是`[0, 2147483647]`。

如果不提供，则算法自动生成一个随机数作为种子。如果您希望生成内容保持相对稳定，请使用相同的seed参数值。

**watermark** `_bool_` （可选）

是否添加水印标识，水印位于图片右下角，文案为“AI生成”。

-   false：默认值，不添加水印。
    
-   true：添加水印。
    

**is\_sketch** `_bool_` （可选）

当`**function**`设置为`**doodle**`（线稿生图）时才需填写。

输入图像是否为线稿图像。

-   false：默认值，输入图像不为线稿图像。模型会先从输入图像中提取线稿，再参考提取的线稿生成新的图像。
    
-   true：输入图像为线稿图像。模型将直接基于输入图像生成图像，适用于涂鸦作画场景。
    

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

**code** `_string_`

请求失败的错误码。请求成功时不会返回此参数，详情请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。

**message** `_string_`

请求失败的详细信息。请求成功时不会返回此参数，详情请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。

### 步骤2：根据任务ID查询结果

`GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`

#### 请求参数

## 查询任务结果

请将`86ecf553-d340-4e21-xxxxxxxxx`替换为真实的task\_id。

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

## 任务执行成功

任务数据（如任务状态、图像URL等）仅保留24小时，超时后会被自动清除。请您务必及时保存生成的图像。

```
{
    "request_id": "eeef0935-02e9-9742-bb55-xxxxxx",
    "output": {
        "task_id": "a425c46f-dc0a-400f-879e-xxxxxx",
        "task_status": "SUCCEEDED",
        "submit_time": "2025-02-21 17:56:31.786",
        "scheduled_time": "2025-02-21 17:56:31.821",
        "end_time": "2025-02-21 17:56:42.530",
        "results": [
            {
                "url": "https://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/aaa.png"
            }
        ],
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

## 任务执行失败

若任务执行失败，task\_status将置为 FAILED，并提供错误码和信息。请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。

```
{
    "request_id": "e5d70b02-ebd3-98ce-9fe8-759d7d7b107d",
    "output": {
        "task_id": "86ecf553-d340-4e21-af6e-xxxxxx",
        "task_status": "FAILED",
        "code": "InvalidParameter",
        "message": "xxxxxx",
        "task_metrics": {
            "TOTAL": 4,
            "SUCCEEDED": 0,
            "FAILED": 4
        }
    }
}
```

## 任务部分失败

模型可以在一次任务中生成多张图片。只要有一张图片生成成功，任务状态将标记为`SUCCEEDED`，并且返回相应的图像URL。对于生成失败的图片，结果中会返回相应的失败原因。同时在usage统计中，只会对成功的结果计数。请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。

```
{
    "request_id": "85eaba38-0185-99d7-8d16-xxxxxx",
    "output": {
        "task_id": "86ecf553-d340-4e21-af6e-xxxxxx",
        "task_status": "SUCCEEDED",
        "results": [
            {
                "url": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/123/a1.png"
            },
            {
                "code": "InternalError.Timeout",
                "message": "An internal timeout error has occured during execution, please try again later or contact service support."
            }
        ],
        "task_metrics": {
            "TOTAL": 2,
            "SUCCEEDED": 1,
            "FAILED": 1
        }
    },
    "usage": {
        "image_count": 1
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

**results** `_array object_`

任务结果列表，包括图像URL、部分任务执行失败报错信息等。

**数据结构**

```
{
    "results": [
        {
            "url": ""
        },
        {
            "code": "",
            "message": ""
        }
    ]
}
```

**task\_metrics** `_object_`

任务结果统计。

**属性**

**TOTAL** `_integer_`

总的任务数。

**SUCCEEDED** `_integer_`

任务状态为成功的任务数。

**FAILED** `_integer_`

任务状态为失败的任务数。

**code** `_string_`

请求失败的错误码。请求成功时不会返回此参数，详情请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。

**message** `_string_`

请求失败的详细信息。请求成功时不会返回此参数，详情请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。

**usage** `_object_`

输出信息统计。只对成功的结果计数。

**属性**

**image\_count** `_integer_`

模型成功生成图片的数量。计费公式：费用 = 图片数量 × 单价。

**request\_id** `_string_`

请求唯一标识。可用于请求明细溯源和问题排查。

## DashScope SDK调用

请先确认已[安装最新版DashScope SDK](https://help.aliyun.com/zh/model-studio/install-sdk)，否则可能导致运行报错。

DashScope SDK目前已支持Python和Java。

SDK与HTTP接口的参数名基本一致，参数结构根据不同语言的SDK封装而定。参数说明可参考[HTTP调用](https://help.aliyun.com/zh/model-studio/legacy-image-to-video-api-reference/#42703589880ts)。

由于视频模型处理时间较长，底层服务采用异步方式提供。SDK在上层进行了封装，支持同步、异步两种调用方式。

> 通用图像编辑模型大约需要5-15秒。实际耗时取决于排队任务数量和网络状况，请您在获取结果时耐心等待。

### Python SDK调用

使用Python SDK处理图像文件时，支持以下三种方式输入图像。请根据您的场景选择其中一种即可。

1.  公网 URL：公网可访问的图像 URL（HTTP/HTTPS）。您可在此[获取临时公网URL](https://help.aliyun.com/zh/model-studio/get-temporary-file-url)。
    
2.  Base64编码：传入Base64编码文件后的字符串，格式为`data:{MIME_type};base64,{base64_data}`。
    
3.  本地文件路径：支持传入文件的**绝对路径和相对路径**。请参考下表，传入正确的文件路径。
    

**系统**

**传入的文件路径**

**示例（绝对路径）**

**示例（相对路径）**

Linux或macOS系统

file://{文件的绝对路径或相对路径}

file:///home/images/test.png

file://./images/test.png

Windows系统

file://D:/images/test.png

file://./images/test.png

#### **示例代码**

**说明**

在调用代码前，请确保已安装 DashScope Python SDK，推荐升级至最新版本：`pip install -U dashscope`，详见[安装SDK](https://help.aliyun.com/zh/model-studio/install-sdk)。

## 同步调用

本示例展示同步调用方式，并支持三种图像输入方式：公网URL、Base64编码、本地文件路径。

##### 请求示例

```
import base64
import os
from http import HTTPStatus
from dashscope import ImageSynthesis
import mimetypes

"""
环境要求：
    dashscope python SDK >= 1.23.8
安装/升级SDK:
    pip install -U dashscope
"""

# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
api_key = os.getenv("DASHSCOPE_API_KEY")

# --- 辅助函数：用于 Base64 编码 ---
# 格式为 data:{MIME_type};base64,{base64_data}
def encode_file(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type or not mime_type.startswith("image/"):
        raise ValueError("不支持或无法识别的图像格式")
    with open(file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return f"data:{mime_type};base64,{encoded_string}"

"""
图像输入方式说明：
以下提供了三种图片输入方式，三选一即可

1. 使用公网URL - 适合已有公开可访问的图片
2. 使用本地文件 - 适合本地开发测试
3. 使用Base64编码 - 适合私有图片或需要加密传输的场景
"""

# 【方式一】使用公网图片 URL
mask_image_url = "http://wanx.alicdn.com/material/20250318/description_edit_with_mask_3_mask.png"
base_image_url = "http://wanx.alicdn.com/material/20250318/description_edit_with_mask_3.jpeg"

# 【方式二】使用本地文件（支持绝对路径和相对路径）
# 格式要求：file:// + 文件路径
# 示例（绝对路径）：
# mask_image_url = "file://" + "/path/to/your/mask_image.png"     # Linux/macOS
# base_image_url = "file://" + "C:/path/to/your/base_image.jpeg"  # Windows
# 示例（相对路径）：
# mask_image_url = "file://" + "./mask_image.png"                 # 以实际路径为准
# base_image_url = "file://" + "./base_image.jpeg"                # 以实际路径为准

# 【方式三】使用Base64编码的图片
# mask_image_url = encode_file("./mask_image.png")               # 以实际路径为准
# base_image_url = encode_file("./base_image.jpeg")              # 以实际路径为准

def sample_sync_call_imageedit():
    print('please wait...')
    rsp = ImageSynthesis.call(api_key=api_key,
                              model="wanx2.1-imageedit",
                              function="description_edit_with_mask",
                              prompt="陶瓷兔子拿着陶瓷小花",
                              mask_image_url=mask_image_url,
                              base_image_url=base_image_url,
                              n=1)
    assert rsp.status_code == HTTPStatus.OK

    print('response: %s' % rsp)
    if rsp.status_code == HTTPStatus.OK:
        for result in rsp.output.results:
            print("---------------------------")
            print(result.url)
    else:
        print('sync_call Failed, status_code: %s, code: %s, message: %s' %
              (rsp.status_code, rsp.code, rsp.message))

if __name__ == '__main__':
    sample_sync_call_imageedit()
```

##### 响应示例

> url 有效期24小时，请及时下载图像。

```
{
    "status_code": 200,
    "request_id": "dc41682c-4e4a-9010-bc6f-xxxxxx",
    "code": null,
    "message": "",
    "output": {
        "task_id": "6e319d88-a07a-420c-9493-xxxxxx",
        "task_status": "SUCCEEDED",
        "results": [
            {
                "url": "https://dashscope-result-wlcb-acdr-1.oss-cn-wulanchabu-acdr-1.aliyuncs.com/xxx.png?xxxxxx"
            }
        ],
        "submit_time": "2025-05-26 14:58:27.320",
        "scheduled_time": "2025-05-26 14:58:27.339",
        "end_time": "2025-05-26 14:58:39.170",
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

本示例仅展示异步调用方式。

##### 请求示例

```
import os
from http import HTTPStatus
from dashscope import ImageSynthesis

"""
环境要求：
    dashscope python SDK >= 1.23.4
安装/升级SDK:
    pip install -U dashscope
"""

# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
api_key = os.getenv("DASHSCOPE_API_KEY")

# 使用公网图片 URL
mask_image_url = "http://wanx.alicdn.com/material/20250318/description_edit_with_mask_3_mask.png"
base_image_url = "http://wanx.alicdn.com/material/20250318/description_edit_with_mask_3.jpeg"

def sample_async_call_imageedit():
    # 异步调用，返回一个task_id
    rsp = ImageSynthesis.async_call(api_key=api_key,
                                    model="wanx2.1-imageedit",
                                    function="description_edit_with_mask",
                                    prompt="陶瓷兔子拿着陶瓷小花",
                                    mask_image_url=mask_image_url,
                                    base_image_url=base_image_url,
                                    n=1)
    print(rsp)
    if rsp.status_code == HTTPStatus.OK:
        print("task_id: %s" % rsp.output.task_id)
    else:
        print('Failed, status_code: %s, code: %s, message: %s' %
              (rsp.status_code, rsp.code, rsp.message))

    # 获取异步任务信息
    status = ImageSynthesis.fetch(task=rsp, api_key=api_key)
    if status.status_code == HTTPStatus.OK:
        print(status.output.task_status)  # check the task status
    else:
        print('Failed, status_code: %s, code: %s, message: %s' %
              (status.status_code, status.code, status.message))

    # 等待异步任务结束
    rsp = ImageSynthesis.wait(rsp)
    print(rsp)
    if rsp.status_code == HTTPStatus.OK:
        print(rsp.output)
        for result in rsp.output.results:
            print("---------------------------")
            print(result.url)
    else:
        print('Failed, status_code: %s, code: %s, message: %s' %
              (rsp.status_code, rsp.code, rsp.message))

if __name__ == '__main__':
    sample_async_call_imageedit()
```

##### 响应示例

1、创建任务的响应示例

```
{
	"status_code": 200,
	"request_id": "6dc3bf6c-be18-9268-9c27-xxxxxx",
	"code": "",
	"message": "",
	"output": {
		"task_id": "686391d9-7ecf-4290-a8e9-xxxxxx",
		"task_status": "PENDING",
		"video_url": ""
	},
	"usage": null
}
```

2、查询任务结果的响应示例

> url 有效期24小时，请及时下载图像。

```
{
    "status_code": 200,
    "request_id": "dc41682c-4e4a-9010-bc6f-xxxxxx",
    "code": null,
    "message": "",
    "output": {
        "task_id": "6e319d88-a07a-420c-9493-xxxxxx",
        "task_status": "SUCCEEDED",
        "results": [
            {
                "url": "https://dashscope-result-wlcb-acdr-1.oss-cn-wulanchabu-acdr-1.aliyuncs.com/xxx.png?Expires=17xxxxxx"
            }
        ],
        "submit_time": "2025-05-26 14:58:27.320",
        "scheduled_time": "2025-05-26 14:58:27.339",
        "end_time": "2025-05-26 14:58:39.170",
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

### Java SDK调用

使用Java SDK处理图像文件时，支持以下三种方式输入图像。请根据您的场景选择其中一种即可。

1.  公网 URL：公网可访问的图像 URL（HTTP/HTTPS）。您可在此[获取临时公网URL](https://help.aliyun.com/zh/model-studio/get-temporary-file-url)。
    
2.  Base 64编码：传入Base64编码文件后的字符串，格式为`data:{MIME_type};base64,{base64_data}`。
    
3.  本地文件路径：仅支持传入文件的**绝对路径**。请参考下表，传入正确的文件路径。
    

**系统**

**传入的文件路径**

**示例**

Linux或macOS系统

file://{文件的绝对路径}

file:///home/images/test.png

Windows系统

file:///{文件的绝对路径}

file:///D:/images/test.png

#### **示例代码**

**说明**

在调用代码前，请确保已安装 DashScope Java SDK。推荐您升级至最新版本，详见[安装SDK](https://help.aliyun.com/zh/model-studio/install-sdk)。

## 同步调用

本示例展示同步调用方式，并支持三种图像输入方式：公网URL、Base64编码、本地文件路径。

##### 请求示例

```
// Copyright (c) Alibaba, Inc. and its affiliates.

import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesis;
import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisParam;
import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.JsonUtils;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Base64;
import java.util.HashMap;
import java.util.Map;

/**
 * 环境要求
 *      dashscope java SDK >=2.20.9
 * 更新maven依赖:
 *      https://mvnrepository.com/artifact/com.alibaba/dashscope-sdk-java
 */
 
public class ImageEditSync {

    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey="sk-xxx"
    static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    /**
     * 图像输入方式说明：三选一即可
     *
     * 1. 使用公网URL - 适合已有公开可访问的图片
     * 2. 使用本地文件 - 适合本地开发测试
     * 3. 使用Base64编码 - 适合私有图片或需要加密传输的场景
     */

    //【方式一】公网URL
    static String maskImageUrl = "http://wanx.alicdn.com/material/20250318/description_edit_with_mask_3_mask.png";
    static String baseImageUrl = "http://wanx.alicdn.com/material/20250318/description_edit_with_mask_3.jpeg";

    //【方式二】本地文件路径（file://+绝对路径 or file:///+绝对路径）
    // static String maskImageUrl = "file://" + "/your/path/to/mask_image.png";    // Linux/macOS
    // static String baseImageUrl = "file:///" + "C:/your/path/to/base_image.png";  // Windows

    //【方式三】Base64编码
    // static String maskImageUrl = encodeFile("/your/path/to/mask_image.png");
    // static String baseImageUrl = encodeFile("/your/path/to/base_image.png");

    public static void syncCall() {
        // 设置parameters参数
        Map<String, Object> parameters = new HashMap<>();
        parameters.put("prompt_extend", true);

        ImageSynthesisParam param =
                ImageSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("wanx2.1-imageedit")
                        .function(ImageSynthesis.ImageEditFunction.DESCRIPTION_EDIT_WITH_MASK)
                        .prompt("陶瓷兔子拿着陶瓷小花")
                        .maskImageUrl(maskImageUrl)
                        .baseImageUrl(baseImageUrl)
                        .n(1)
                        .size("1024*1024")
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

    /**
     * 将文件编码为Base64字符串
     * @param filePath 文件路径
     * @return Base64字符串，格式为 data:{MIME_type};base64,{base64_data}
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
        syncCall();
    }
}
```

##### 响应示例

> url 有效期24小时，请及时下载图像。

```
{
    "request_id": "bf6c6361-f0fc-949c-9d60-xxxxxx",
    "output": {
        "task_id": "958db858-153b-4c81-b243-xxxxxx",
        "task_status": "SUCCEEDED",
        "results": [
            {
                "url": "https://dashscope-result-wlcb-acdr-1.oss-cn-wulanchabu-acdr-1.aliyuncs.com/xxx.png?xxxxxx"
            }
        ],
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

本示例仅展示异步调用方式。

##### 请求示例

```
// Copyright (c) Alibaba, Inc. and its affiliates.

import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesis;
import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisListResult;
import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisParam;
import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.task.AsyncTaskListParam;
import com.alibaba.dashscope.utils.JsonUtils;

import java.util.HashMap;
import java.util.Map;

/**
 * 环境要求
 *      dashscope java SDK >= 2.20.1
 * 更新maven依赖:
 *      https://mvnrepository.com/artifact/com.alibaba/dashscope-sdk-java
 */
 
public class ImageEditAsync {

    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey="sk-xxx"
    static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    //【方式一】公网URL
    static String maskImageUrl = "http://wanx.alicdn.com/material/20250318/description_edit_with_mask_3_mask.png";
    static String baseImageUrl = "http://wanx.alicdn.com/material/20250318/description_edit_with_mask_3.jpeg";

    public static void asyncCall() {
        // 设置parameters参数
        Map<String, Object> parameters = new HashMap<>();
        parameters.put("prompt_extend", true);

        ImageSynthesisParam param =
                ImageSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("wanx2.1-imageedit")
                        .function(ImageSynthesis.ImageEditFunction.DESCRIPTION_EDIT_WITH_MASK)
                        .prompt("陶瓷兔子拿着陶瓷小花")
                        .maskImageUrl(maskImageUrl)
                        .baseImageUrl(baseImageUrl)
                        .n(1)
                        .size("1024*1024")
                        .parameters(parameters)
                        .build();
        ImageSynthesis imageSynthesis = new ImageSynthesis();
        ImageSynthesisResult result = null;
        try {
            System.out.println("---async call, please wait a moment----");
            result = imageSynthesis.asyncCall(param);
        } catch (ApiException | NoApiKeyException e){
            throw new RuntimeException(e.getMessage());
        }

        System.out.println(JsonUtils.toJson(result));

        String taskId = result.getOutput().getTaskId();

        System.out.println("taskId=" + taskId);

        try {
            result = imageSynthesis.wait(taskId, apiKey);
        } catch (ApiException | NoApiKeyException e){
            throw new RuntimeException(e.getMessage());
        }
        System.out.println(JsonUtils.toJson(result));
        System.out.println(JsonUtils.toJson(result.getOutput()));
    }

    public static void listTask() throws ApiException, NoApiKeyException {
        ImageSynthesis is = new ImageSynthesis();
        AsyncTaskListParam param = AsyncTaskListParam.builder().build();
        param.setApiKey(apiKey);
        ImageSynthesisListResult result = is.list(param);
        System.out.println(result);
    }

    public void fetchTask(String taskId) throws ApiException, NoApiKeyException {
        ImageSynthesis is = new ImageSynthesis();
        // 如果已设置 DASHSCOPE_API_KEY 为环境变量，apiKey 可为空。
        ImageSynthesisResult result = is.fetch(taskId, apiKey);
        System.out.println(result.getOutput());
        System.out.println(result.getUsage());
    }

    public static void main(String[] args) {
        asyncCall();
    }
}
```

##### 响应示例

1、创建任务的响应示例

```
{
	"request_id": "5dbf9dc5-4f4c-9605-85ea-xxxxxxxx",
	"output": {
		"task_id": "7277e20e-aa01-4709-xxxxxxxx",
		"task_status": "PENDING"
	}
}
```

2、查询任务结果的响应示例

> url 有效期24小时，请及时下载图像。

```
{
	"request_id": "3d740fc4-a968-9c36-b0e7-xxxxxxxx",
	"output": {
		"task_id": "34dcf4b0-ed84-441e-91cb-xxxxxxxx",
		"task_status": "SUCCEEDED",
		"results": [
			{
				"url": "https://dashscope-result-hz.oss-cn-hangzhou.aliyuncs.com/xxx.png"
			}
		],
		"submit_time": "2025-02-21 17:56:31.786",
		"scheduled_time": "2025-02-21 17:56:31.821",
		"end_time": "2025-02-21 17:56:42.530",
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

## **错误码**

如果模型调用失败并返回报错信息，请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。

此API还有特定状态码，具体如下所示。

**HTTP状态码**

**接口错误码（code）**

**接口错误信息（message）**

**含义说明**

400

InvalidParameter

InvalidParameter

请求参数不合法。

400

IPInfringementSuspect

Input data is suspected of being involved in IP infringement.

输入数据（如提示词或图像）涉嫌知识产权侵权。请检查输入，确保不包含引发侵权风险的内容。

400

DataInspectionFailed

Input data may contain inappropriate content.

输入数据（如提示词或图像）可能包含敏感内容。请修改输入后重试。

500

InternalError

InternalError

服务异常。请先尝试重试，排除偶发情况。

## **输入图像说明**

### **传值方式**

输入图像支持多种字符串格式，不同调用方式的支持情况如下表所示。

**调用方式**

**HTTP**

**Python SDK**

**Java SDK**

支持的输入图像方式

-   公网URL
    
-   Base64编码
    

-   公网URL
    
-   Base64编码
    
-   本地文件路径
    

-   公网URL
    
-   Base64编码
    
-   本地文件路径
    

**方式一：使用公网URL**

-   提供一个公网可访问的图像地址，支持 HTTP 或 HTTPS 协议。请在此[获取临时公网URL](https://help.aliyun.com/zh/model-studio/get-temporary-file-url)。
    
-   示例值：`https://xxxx/img.png`。
    

**方式二：使用Base64编码**

将本地图片文件转换为 Base64 格式的字符串，并根据`data:{MIME_type};base64,{base64_data}`格式拼接成完整的字符串。

-   转换代码请参见[示例代码](#f2b1639e488og)。
    
-   {MIME\_type}：图像的媒体类型，需与文件格式对应。
    
-   {base64\_data}：图像文件经过 Base64 编码后的字符串。
    
-   MIME 类型对应关系：
    
    **图像格式**
    
    **MIME Type**
    
    JPEG
    
    image/jpeg
    
    JPG
    
    image/jpeg
    
    PNG
    
    image/png
    
    BMP
    
    image/bmp
    
    TIFF
    
    image/tiff
    
    WEBP
    
    image/webp
    
-   示例值**：**`"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABDg......"`**。**
    
    注意：为便于展示，上述 Base64 字符串是截断的。在实际使用中，请务必传入完整的编码字符串。
    

**方式三：本地文件路径**

-   HTTP调用不支持本地文件路径，仅Python SDK和Java SDK支持。
    
-   关于本地文件路径的传入规则，请参见[Python SDK调用](#a3ad9a3b6d9if)和[Java SDK调用](#589b80853e6rn)。
    

## 常见问题

图像模型的通用问题请参见[常见问题](https://help.aliyun.com/zh/model-studio/image-faq)文档，包括以下内容：模型计费与限流规则、接口高频报错解决方法等。
