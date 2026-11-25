# 图片生成与编辑

选择适合文生图、图片编辑等场景的模型。

<a id="从闭源模型迁移到百炼"></a>

<a id="mg1a2b3c4d5e02"></a>

<a id="mg1a2b3c4d5e01"></a>

## 从闭源模型迁移到百炼?

如果你正在使用 Nano Banana、GPT Image、Midjourney 或 Seedream，可参考下表选择对应的百炼模型。

| 能力档位 | 闭源模型代表 | 百炼推荐 |
| --- | --- | --- |
| 高质量 | Nano Banana Pro、GPT Image、Seedream 4.0 | `qwen-image-3.0-pro`、`wan2.7-image-pro` |
| 平衡 | Imagen 4 Ultra、Midjourney v7 | `qwen-image-3.0`、`wan2.7-image` |
| 快速低成本 | FLUX.2 | `z-image-turbo` |

<a id="文生图"></a>

<a id="e1a2c3d4e5f02"></a>

<a id="e1a2c3d4e5f01"></a>

## 文生图

推荐使用`qwen-image-3.0-pro`，千问图像3.0旗舰版，支持agent prompt智能改写，擅长文本渲染，能精准生成贴合物理材质的中英文详细使用方法请参见[文本生成图像](image-model/text-to-image.md)。

<a id="何时使用wan2-7-image-pro"></a>

<a id="e1a2c3d4e5f0e"></a>

<a id="e1a2c3d4e5f0d"></a>

### 何时使用wan2.7-image-pro

-   需要品牌色控制，调色盘功能
-   需要更高分辨率，`wan2.7-image-pro`文生图最高支持4096x4096分辨率

<a id="何时使用z-image-turbo"></a>

<a id="e1a2c3d4e5f05"></a>

<a id="e1a2c3d4e5f04"></a>

### 何时使用z-image-turbo

-   只需要生成图片（不需要编辑功能）
-   速度或成本是优先考虑 -- 生成速度快10倍，价格约为1/5
-   写实人像和产品照片

<a id="图片编辑"></a>

<a id="e1a2c3d4e5f15"></a>

<a id="e1a2c3d4e5f14"></a>

## 图片编辑

推荐使用`qwen-image-3.0-pro`，具备强大的复杂内容生成与高保真渲染能力，支持最大 4.5k token 输入，可生成复杂版面，并兼容图中图与密集信息排版，接近真实摄影质感。详细使用方法请参见[图像编辑](image-model/image-edit-guide.md)。

<a id="何时使用wan2-7-image-pro-2"></a>

<a id="e1a2c3d4e5f18"></a>

<a id="e1a2c3d4e5f17"></a>

### 何时使用wan2.7-image-pro

支持多图参考（最多9张输入图片）、边界框交互式编辑以及角色一致性多图生成。

<a id="推荐模型"></a>

<a id="e1a2c3d4e5f1b"></a>

<a id="e1a2c3d4e5f1a"></a>

## 推荐模型

| 模型 ID（Model ID） | 适用场景 | 文生图 | 编辑 | 最大输出数 | 最大分辨率 |
| --- | --- | --- | --- | --- | --- |
| `qwen-image-3.0-pro` | 复杂版面生成、小字渲染、多语言字体 | 支持 | 支持 | 6 | 2048x2048 |
| `qwen-image-3.0` | 同上，生成速度更快 | 支持 | 支持 | 6 | 2048x2048 |
| `wan2.7-image-pro` | 文字渲染、品牌色、角色一致性多图生成、多图编辑 | 支持 | 支持 | 4（连续12） | 4096x4096（文生图）/ 2048x2048（编辑） |
| `wan2.7-image` | 同上，生成速度更快，最高2K | 支持 | 支持 | 4（连续12） | 2048x2048 |
| `z-image-turbo` | 快速生成、低成本、写实人像 | 支持 | 不支持 | 1 | 2048x2048 |

<a id="所有模型"></a>

<a id="e1a2c3d4e5f6e"></a>

<a id="e1a2c3d4e5f6d"></a>

## 所有模型

<a id="wan"></a>

<a id="e1a2c3d4e5f70"></a>

<a id="e1a2c3d4e5f6f"></a>

### Wan

<table><thead><tr><th><strong>模型 ID（Model ID）</strong></th><th><strong>文生图</strong></th><th><strong>编辑</strong></th><th><strong>最大输出数</strong></th><th><strong>最大分辨率</strong></th></tr></thead><tbody><tr><td><p><code>wan2.7-image-pro</code></p></td><td><p>支持</p></td><td><p>支持</p></td><td><p>4（连续12）</p></td><td><p>4096x4096（文生图）/ 2048x2048（编辑）</p></td></tr><tr><td><p><code>wan2.7-image</code></p></td><td><p>支持</p></td><td><p>支持</p></td><td><p>4（连续12）</p></td><td><p>2048x2048</p></td></tr><tr><td><p><code>wan2.6-t2i</code></p></td><td><p>支持</p></td><td><p>支持</p></td><td><p>4</p></td><td><p>1440x1440</p></td></tr><tr><td><p><code>wan2.6-image</code></p></td><td><p>支持</p></td><td><p>支持</p></td><td><p>4</p></td><td><p>1440x1440</p></td></tr><tr><td><p><code>wan2.5-t2i-preview</code></p></td><td><p>支持</p></td><td><p>不支持</p></td><td><p>4</p></td><td><p>1440x1440</p></td></tr><tr><td><p><code>wan2.5-i2i-preview</code></p></td><td><p>不支持</p></td><td><p>支持</p></td><td><p>4</p></td><td><p>1280x1280</p></td></tr><tr><td><p><code>wan2.2-t2i-plus</code></p></td><td><p>支持</p></td><td><p>不支持</p></td><td><p>4</p></td><td><p>1440x1440</p></td></tr><tr><td><p><code>wan2.2-t2i-flash</code></p></td><td><p>支持</p></td><td><p>不支持</p></td><td><p>4</p></td><td><p>1440x1440</p></td></tr><tr><td><p><code>wan2.1-t2i-plus</code></p></td><td><p>支持</p></td><td><p>不支持</p></td><td><p>4</p></td><td><p>1440x1440</p></td></tr><tr><td><p><code>wan2.1-t2i-turbo</code></p></td><td><p>支持</p></td><td><p>不支持</p></td><td><p>4</p></td><td><p>1440x1440</p></td></tr><tr><td colspan="5"><strong>Legacy</strong></td></tr><tr><td><p><code>wanx2.1-imageedit</code></p><blockquote><p>仅支持北京地域</p></blockquote></td><td><p>不支持</p></td><td><p>支持</p></td><td><p>1</p></td><td><p>1024x1024</p></td></tr></tbody></table>

<a id="qwen-image"></a>

<a id="e1a2c3d4e5fee"></a>

<a id="e1a2c3d4e5fed"></a>

### Qwen Image

| 模型 ID（Model ID） | 文生图 | 编辑 | 最大输出数 | 最大分辨率 |
| --- | --- | --- | --- | --- |
| `qwen-image-3.0-pro` | 支持 | 支持 | 6 | 2048x2048 |
| `qwen-image-3.0` | 支持 | 支持 | 6 | 2048x2048 |
| `qwen-image-2.0-pro` | 支持 | 支持 | 6 | 2048x2048 |
| `qwen-image-2.0-pro-2026-06-22` | 支持 | 支持 | 6 | 2048x2048 |
| `qwen-image-2.0-pro-2026-04-22` | 支持 | 支持 | 6 | 2048x2048 |
| `qwen-image-2.0-pro-2026-03-03` | 支持 | 支持 | 6 | 2048x2048 |
| `qwen-image-2.0` | 支持 | 支持 | 6 | 2048x2048 |
| `qwen-image-2.0-2026-03-03` | 支持 | 支持 | 6 | 2048x2048 |

<a id="z-image"></a>

<a id="e1a2c3d4e60a3"></a>

<a id="e1a2c3d4e60a2"></a>

### Z-Image

| 模型 ID（Model ID） | 文生图 | 编辑 | 最大输出数 | 最大分辨率 |
| --- | --- | --- | --- | --- |
| `z-image-turbo` | 支持 | 不支持 | 1 | 2048x2048 |
