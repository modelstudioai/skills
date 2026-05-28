# 视觉理解

选择适合图像分析、视频理解、OCR等场景的模型。

## 图像与视频理解

推荐从`qwen3.6-plus`开始，它是千问旗舰模型，支持1M上下文、最长2小时视频、Function Calling和内置工具等完整功能。当您的场景稳定后，可以尝试`qwen3.6-flash`来降低成本，它提供接近旗舰的效果，并支持相同的上下文长度和功能集。

### 图像分辨率

大多数模型支持每张图片最高1600万像素。更高的分辨率会消耗更多Token：每张图片的Token数计算公式为 `h x w / (32 x 32) + 2`。

### 视频支持

-   最长2小时 / 2GB：`qwen3.6-plus`、`qwen3.6-flash`、`qwen3.5-plus`、`qwen3.5-flash`
    
-   最长1小时 / 2GB：`qwen3-vl-plus`、`qwen3-vl-flash`
    
-   最长1小时 / 2GB：`qwen3.5-omni-plus`、`qwen3.5-omni-flash`（同时支持音频输入）
    

### Function Calling与内置工具

让模型根据图像或视频中的内容执行操作。

-   Function Calling：Qwen3.6、Qwen3.5和Qwen3-VL系列模型均支持
    
-   内置工具（联网搜索、代码执行，无需额外配置）：仅`qwen3.6-plus`、`qwen3.6-flash`、`qwen3.5-plus`、`qwen3.5-flash`
    

### 结构化输出

从视觉输入中获取有效的JSON输出，例如从照片中提取商品信息。

Qwen3.6、Qwen3.5和Qwen3-VL系列在非思考模式下支持此功能。

## OCR与文档提取

`qwen-vl-ocr`专为文档、表格、试卷和手写内容的文字提取而优化。您也可以使用`qwen3.6-plus`或`qwen3.6-flash`进行通用图片文字提取。

## 推荐模型

**模型**

**上下文**

**最大像素/图**

**最大视频时长**

**最大视频大小**

**最大图片数**

**最大视频数**

**Function Calling**

**内置工具**

**结构化输出**

`qwen3.6-plus`

1M

16M

2小时

2GB

256

64

支持

支持

支持

`qwen3.6-flash`

1M

16M

2小时

2GB

256

64

支持

支持

支持

`qwen3.5-omni-plus`

64k

\--

1小时

2GB

2,048

512

支持

\--

支持

## 所有模型

### Qwen3.6

**模型ID**

**输入**

**输出**

**上下文**

**最大输出**

**最大图片数**

**最大视频数**

**Function Calling**

**内置工具**

**结构化输出**

`qwen3.6-plus`

文本、图像、视频

文本

1M

64k

256

64

支持

支持

支持

`qwen3.6-plus-2026-04-02`

文本、图像、视频

文本

1M

64k

256

64

支持

支持

支持

`qwen3.6-flash`

文本、图像、视频

文本

1M

64k

256

64

支持

支持

支持

`qwen3.6-flash-2026-04-16`

文本、图像、视频

文本

1M

64k

256

64

支持

支持

支持

`qwen3.6-35b-a3b`

文本、图像、视频

文本

256k

64k

256

64

支持

支持

支持

### Qwen3.5

**模型ID**

**输入**

**输出**

**上下文**

**最大输出**

**最大图片数**

**最大视频数**

**Function Calling**

**内置工具**

**结构化输出**

`qwen3.5-plus`

文本、图像、视频

文本

1M

64k

256

64

支持

支持

支持

`qwen3.5-plus-2026-02-15`

文本、图像、视频

文本

1M

64k

256

64

支持

支持

支持

`qwen3.5-flash`

文本、图像、视频

文本

1M

64k

256

64

支持

支持

支持

`qwen3.5-flash-2026-02-23`

文本、图像、视频

文本

1M

64k

256

64

支持

支持

支持

`qwen3.5-397b-a17b`

文本、图像、视频

文本

32k

8k

256

64

支持

支持

支持

`qwen3.5-122b-a10b`

文本、图像、视频

文本

32k

8k

256

64

支持

支持

支持

`qwen3.5-27b`

文本、图像、视频

文本

32k

8k

256

64

支持

支持

支持

`qwen3.5-35b-a3b`

文本、图像、视频

文本

32k

8k

256

64

支持

支持

支持

### 旧版及其他模型

以下模型不再作为首选推荐。新项目建议使用Qwen3.6或Qwen3.5系列。如需查看模型详细参数，请前往模型广场。

[华北2（北京）](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market/all) | [新加坡](https://modelstudio.console.aliyun.com/ap-southeast-1?tab=doc#/doc/?type=model&url=2840914) | [美国](https://modelstudio.console.aliyun.com/us-east-1?tab=doc#/doc/?type=model&url=2840914) | [法兰克福](https://modelstudio.console.aliyun.com/eu-central-1?tab=doc#/doc/?type=model&url=2840914)

**查看旧版及其他模型列表**

#### Qwen3-VL

-   `qwen3-vl-plus`
    
-   `qwen3-vl-plus-2026-01-25`
    
-   `qwen3-vl-flash`
    
-   `qwen3-vl-flash-2026-01-25`
    

#### Qwen2.5-VL

-   `qwen2.5-vl-72b-instruct`
    
-   `qwen2.5-vl-32b-instruct`
    
-   `qwen2.5-vl-7b-instruct`
    
-   `qwen2.5-vl-3b-instruct`
    

#### Qwen-Omni

-   `qwen3-omni-flash`
    
-   `qwen3-omni-flash-2025-10-22`
    
-   `qwen-omni-turbo`及其快照版本
    

#### Qwen-OCR

-   `qwen-vl-ocr`
    
-   `qwen-vl-ocr-latest`
    
-   `qwen-vl-ocr-2025-07-14`
    

#### QVQ

-   `qvq-max`
    
-   `qvq-max-2025-08-28`
    
-   `qvq-plus`
    
-   `qvq-plus-2025-08-27`
    

#### 旧版Qwen-VL

-   `qwen-vl-max`及其快照版本
    
-   `qwen-vl-plus`及其快照版本
