# 图片生成与编辑

选择适合文生图、图片编辑等场景的模型。

## 从闭源模型迁移到百炼?

如果你正在使用 Nano Banana、GPT Image、Midjourney 或 Seedream，可参考下表选择对应的百炼模型。

**能力档位**

**闭源模型代表**

**百炼推荐**

高质量

Nano Banana Pro、GPT Image、Seedream 4.0

`qwen-image-3.0-pro`、`wan2.7-image-pro`

平衡

Imagen 4 Ultra、Midjourney v7

`qwen-image-3.0`、`wan2.7-image`

快速低成本

FLUX.2

`z-image-turbo`

## 文生图

推荐使用`qwen-image-3.0-pro`，千问图像3.0旗舰版，支持agent prompt智能改写，擅长文本渲染，能精准生成贴合物理材质的中英文详细使用方法请参见[文本生成图像](https://help.aliyun.com/zh/model-studio/text-to-image)。

### 何时使用wan2.7-image-pro

-   需要品牌色控制，调色盘功能
-   需要更高分辨率，`wan2.7-image-pro`文生图最高支持4096x4096分辨率

### 何时使用z-image-turbo

-   只需要生成图片（不需要编辑功能）
-   速度或成本是优先考虑 -- 生成速度快10倍，价格约为1/5
-   写实人像和产品照片

## 图片编辑

推荐使用`qwen-image-3.0-pro`，具备强大的复杂内容生成与高保真渲染能力，支持最大 4.5k token 输入，可生成复杂版面，并兼容图中图与密集信息排版，接近真实摄影质感。详细使用方法请参见[图像编辑](https://help.aliyun.com/zh/model-studio/image-edit-guide)。

### 何时使用wan2.7-image-pro

支持多图参考（最多9张输入图片）、边界框交互式编辑以及角色一致性多图生成。

## 推荐模型

**模型 ID（Model ID）**

**适用场景**

**文生图**

**编辑**

**最大输出数**

**最大分辨率**

`qwen-image-3.0-pro`

复杂版面生成、小字渲染、多语言字体

支持

支持

6

2048x2048

`qwen-image-3.0`

同上，生成速度更快

支持

支持

6

2048x2048

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

## 所有模型

### Wan

**模型 ID（Model ID）**

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

**模型 ID（Model ID）**

**文生图**

**编辑**

**最大输出数**

**最大分辨率**

`qwen-image-3.0-pro`

支持

支持

6

2048x2048

`qwen-image-3.0`

支持

支持

6

2048x2048

`qwen-image-2.0-pro`

支持

支持

6

2048x2048

`qwen-image-2.0-pro-2026-06-22`

支持

支持

6

2048x2048

`qwen-image-2.0-pro-2026-04-22`

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

**模型 ID（Model ID）**

**文生图**

**编辑**

**最大输出数**

**最大分辨率**

`z-image-turbo`

支持

不支持

1

2048x2048
