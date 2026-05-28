# 图片生成与编辑

选择适合文生图、图片编辑等场景的模型。

## 文生图

推荐使用`wan2.7-image-pro`，它在一个模型中集成了文字渲染、品牌色控制、角色一致性多图生成以及图片编辑功能。文生图最高支持4096x4096分辨率，图片编辑最高支持2048x2048分辨率。详细使用方法请参见[文本生成图像](https://help.aliyun.com/zh/model-studio/text-to-image)。

### 何时使用z-image-turbo

-   只需要生成图片（不需要编辑功能）
    
-   速度或成本是优先考虑 -- 生成速度快10倍，价格约为1/5
    
-   写实人像和产品照片
    

### 何时使用qwen-image-2.0-pro

-   需要使用负向提示词排除输出中的特定元素
    
-   需要每次调用生成最多6张图片变体（Wan标准模式最多支持4张）
    

## 图片编辑

推荐使用`wan2.7-image-pro`，它支持多图参考（最多9张输入图片）、边界框交互式编辑以及角色一致性多图生成。详细使用方法请参见[图像编辑-千问](https://help.aliyun.com/zh/model-studio/qwen-image-edit-guide)和[图像编辑-万相2.7/2.6/2.5](https://help.aliyun.com/zh/model-studio/wan-image-edit)。

### 何时使用qwen-image-2.0-pro

如果编辑时需要使用负向提示词，请使用`qwen-image-2.0-pro`（生成和编辑使用同一个模型ID）。

## 推荐模型

**模型**

**适用场景**

**文生图**

**编辑**

**最大输出数**

**最大分辨率**

`wan2.7-image-pro`

文字渲染、品牌色、角色一致性多图生成、多图编辑

支持

支持

4（连续12）

4096x4096（文生图）/ 2048x2048（编辑）

`wan2.7-image`

同上，生成速度更快，最高2K

支持

支持

4（连续12）

2048x2048

`z-image-turbo`

快速生成、低成本、写实人像

支持

不支持

1

2048x2048

`qwen-image-2.0-pro`

负向提示词、最多6张图片变体

支持

支持

6

2048x2048

`qwen-image-2.0`

qwen-image-2.0-pro的快速版本

支持

支持

6

2048x2048

## 所有模型

### Wan

**模型ID**

**文生图**

**编辑**

**最大输出数**

**最大分辨率**

`wan2.7-image-pro`

支持

支持

4（连续12）

4096x4096（文生图）/ 2048x2048（编辑）

`wan2.7-image`

支持

支持

4（连续12）

2048x2048

`wan2.6-t2i`

支持

支持

4

1440x1440

`wan2.6-image`

支持

支持

4

1440x1440

`wan2.5-t2i-preview`

支持

不支持

4

1440x1440

`wan2.5-i2i-preview`

不支持

支持

4

1280x1280

`wan2.2-t2i-plus`

支持

不支持

4

1440x1440

`wan2.2-t2i-flash`

支持

不支持

4

1440x1440

`wan2.1-t2i-plus`

支持

不支持

4

1440x1440

`wan2.1-t2i-turbo`

支持

不支持

4

1440x1440

**Legacy**

`wanx2.1-imageedit`

> 仅支持北京地域

不支持

支持

1

1024x1024

### Qwen Image

**模型ID**

**文生图**

**编辑**

**最大输出数**

**最大分辨率**

`qwen-image-2.0-pro`

支持

支持

6

2048x2048

`qwen-image-2.0-pro-2026-03-03`

支持

支持

6

2048x2048

`qwen-image-2.0`

支持

支持

6

2048x2048

`qwen-image-2.0-2026-03-03`

支持

支持

6

2048x2048

`qwen-image-max`

支持

不支持

1

1664x928

`qwen-image-max-2025-12-30`

支持

不支持

1

1664x928

`qwen-image-plus`

支持

不支持

1

1664x928

`qwen-image-plus-2026-01-09`

支持

不支持

1

1664x928

`qwen-image`

支持

不支持

1

1664x928

`qwen-image-edit-max`

不支持

支持

6

2048x2048

`qwen-image-edit-max-2026-01-16`

不支持

支持

6

2048x2048

`qwen-image-edit-plus`

不支持

支持

6

2048x2048

`qwen-image-edit-plus-2025-12-15`

不支持

支持

6

2048x2048

`qwen-image-edit-plus-2025-10-30`

不支持

支持

6

2048x2048

`qwen-image-edit`

不支持

支持

1

1024x1024

### Z-Image

**模型ID**

**文生图**

**编辑**

**最大输出数**

**最大分辨率**

`z-image-turbo`

支持

不支持

1

2048x2048
