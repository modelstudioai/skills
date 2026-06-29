# 模型训练与部署计费

本文介绍阿里云百炼平台的模型训练、模型部署的计费规则及价格。

## **模型训练计费**

### **文本生成模型-千问**

**说明**

模型训练流程请参见[模型调优](https://help.aliyun.com/zh/model-studio/model-training-overview)。训练完成后的新模型需先完成**模型部署**，才能评测和调用。

**计费方式**

按训练Token计费

**计费公式**

模型训练费用 = （训练数据 Token 总数 + 混合训练数据 Token 总数）× 循环次数 × 训练单价（最小计费单位：1 token）

> 您可以查看[模型训练控制台](https://bailian.console.aliyun.com/#/efm/model_manager/create)底部的预估训练费用，并单击**计算详情**，查看训练 Token 总数、循环次数和训练单价。

#### 千问

**模型服务**

**模型代码**

**价格**

Qwen3.6-Flash-2026-04-16

qwen3.6-flash-2026-04-16

¥0.05/千Token

Qwen3.5-27B

qwen3.5-27b

¥0.05/千Token

Qwen3.5-9B

qwen3.5-9b

¥0.02/千Token

Qwen3.5-Flash-2026-02-23

qwen3.5-flash-2026-02-23

¥0.05/千Token

Qwen3-32B

qwen3-32b

¥0.04/千Token

Qwen3-30B-A3B-Instruct-2507

qwen3-30b-a3b-instruct-2507

¥0.03/千Token

Qwen3-14B

qwen3-14b

¥0.03/千Token

Qwen3-8B

qwen3-8b

¥0.006/千Token

Qwen3-4B-Instruct-2507

qwen3-4b-instruct-2507

¥0.006/千Token

Qwen3-1.7B

qwen3-1.7b

¥0.0045/千Token

Qwen3-0.6B

qwen3-0.6b

¥0.003/千Token

Qwen2.5-72B-Instruct

qwen2.5-72b-instruct

¥0.15/千Token

Qwen2.5-32B-Instruct

qwen2.5-32b-instruct

¥0.03/千Token

Qwen2.5-14B-Instruct

qwen2.5-14b-instruct

¥0.03/千Token

Qwen2.5-7B-Instruct

qwen2.5-7b-instruct

¥0.006/千Token

千问-Plus-Character-2025-11-06

qwen-plus-character-2025-11-06

¥0.15/千Token

#### 千问VL

**模型服务**

**模型代码**

**价格**

Qwen3-VL-8B-Instruct

qwen3-vl-8b-instruct

¥0.012/千Token

Qwen3-VL-8B-Thinking

qwen3-vl-8b-thinking

¥0.012/千Token

Qwen3-VL-4B-Instruct

qwen3-vl-4b-instruct

¥0.006/千Token

Qwen2.5-VL-72B-Instruct

qwen2.5-vl-72b-instruct

¥0.05/千Token

Qwen2.5-VL-32B-Instruct

qwen2.5-vl-32b-instruct

¥0.02/千Token

Qwen2.5-VL-7B-Instruct

qwen2.5-vl-7b-instruct

¥0.01/千Token

**计算图像与视频的Token**

##### **图像**

计算公式：`图像 Token = h_bar * w_bar / token_pixels + 2`

-   `h_bar、w_bar`：缩放后的图像长宽，模型在处理图像前会进行预处理，会将图像缩小至特定像素上限内，像素上限与`max_pixels`和`vl_high_resolution_images`参数的取值有关，相关章节：[处理高分辨率图像](https://help.aliyun.com/zh/model-studio/vision#e7e2db755f9h7)。
    
-   `token_pixels`：每视觉`Token`对应的像素值，不同模型情况不同：
    
    -   `qwen3.7系列`、`qwen3.6系列`、`qwen3.5系列`、`Qwen3-VL`、`qwen-vl-max`、`qwen-vl-plus`**：**每个`Token`对应 `32x32`像素
        
    -   `QVQ`及其他`Qwen2.5-VL`模型**：**每个Token对应`28x28`像素
        

以下代码演示了模型内部对图像的大致缩放逻辑，可用于估算一张图像的Token，实际计费请以API响应为准。

```
import math
from PIL import Image  # pip install Pillow

def smart_size(image_path, max_pixels, vl_high_resolution_images):
    """根据模型参数，计算图像缩放后的尺寸，用于估算图像 Token。"""
    image = Image.open(image_path)
    height, width = image.height, image.width

    # Qwen3.6、Qwen3.5、Qwen3-VL 等模型的缩放因子为 32；其他模型为 28
    factor = 32
    h_bar = round(height / factor) * factor
    w_bar = round(width / factor) * factor

    # Token 下限：4 个 Token
    min_pixels = 4 * factor * factor

    # vl_high_resolution_images=True 时，Token 上限固定为 16384，忽略 max_pixels
    if vl_high_resolution_images:
        max_pixels = 16384 * factor * factor

    # 将总像素数约束在 [min_pixels, max_pixels] 范围内
    if h_bar * w_bar > max_pixels:
        beta = math.sqrt((height * width) / max_pixels)
        h_bar = math.floor(height / beta / factor) * factor
        w_bar = math.floor(width / beta / factor) * factor
    elif h_bar * w_bar < min_pixels:
        beta = math.sqrt(min_pixels / (height * width))
        h_bar = math.ceil(height * beta / factor) * factor
        w_bar = math.ceil(width * beta / factor) * factor

    return h_bar, w_bar

if __name__ == "__main__":
    # 注意：max_pixels 和 vl_high_resolution_images 的值需要与调用模型时传入的参数保持一致
    h_bar, w_bar = smart_size("xxx/test.jpg", max_pixels=2560 * 32 * 32, vl_high_resolution_images=False)
    print(f"缩放后的图像尺寸：高度 {h_bar}，宽度 {w_bar}")

    # 每张图像额外包含 <vision_bos> 和 <vision_eos> 各 1 个 Token
    token = int(h_bar * w_bar / (32 * 32)) + 2
    print(f"图像的 Token 数：{token}")
```

##### **视频**

-   **视频文件：**
    
    模型处理视频文件时，会先进行抽帧，然后计算所有视频帧的总 Token 数。由于该计算过程较为复杂，可使用以下代码，通过传入视频路径来估算视频消耗的总 Token 数：
    
    ```
    # 使用前安装：pip install opencv-python
    import math
    import os
    import logging
    import cv2
    
    logger = logging.getLogger(__name__)
    
    FRAME_FACTOR = 2
    
    # Qwen3.6、Qwen3.5、Qwen3-VL、qwen-vl-max-0813、qwen-vl-plus-0815、qwen-vl-plus-0710等模型，图像缩放因子为32
    IMAGE_FACTOR = 32
    
    #  其他模型，图像缩放因子为28
    # IMAGE_FACTOR = 28
    
    # 视频帧的最大长宽比
    MAX_RATIO = 200
    # 视频帧的像素下限
    VIDEO_MIN_PIXELS = 4 * 32 * 32
    # 视频帧的像素上限，使用Qwen3-VL-Plus模型，VIDEO_MAX_PIXELS为640 * 32 * 32，其他模型为768 * 32 * 32
    VIDEO_MAX_PIXELS = 640 * 32 * 32
    
    # 用户未传入FPS参数，则fps使用默认值
    FPS = 2.0
    # 最少抽取帧数
    FPS_MIN_FRAMES = 4
    # 最大抽取帧数（根据模型选择设置值）
    FPS_MAX_FRAMES = 2000
    
    # 视频输入的最大像素值，使用Qwen3-VL-Plus模型，请将VIDEO_TOTAL_PIXELS设置为131072 * 32 * 32，其他模型设置为65536 * 32 * 32
    VIDEO_TOTAL_PIXELS = int(float(os.environ.get('VIDEO_MAX_PIXELS', 131072 * 32 * 32)))
    
    def round_by_factor(number: int, factor: int) -> int:
        """返回与”number“最接近的整数，该整数可被”factor“整除。"""
        return round(number / factor) * factor
    
    def ceil_by_factor(number: int, factor: int) -> int:
        """返回大于或等于“number”且可被“factor”整除的最小整数。"""
        return math.ceil(number / factor) * factor
    
    def floor_by_factor(number: int, factor: int) -> int:
        """返回小于或等于“number”且可被“factor”整除的最大整数。"""
        return math.floor(number / factor) * factor
    
    def extract_vision_info(conversations):
        vision_infos = []
        if isinstance(conversations[0], dict):
            conversations = [conversations]
        for conversation in conversations:
            for message in conversation:
                if isinstance(message["content"], list):
                    for ele in message["content"]:
                        if (
                            "image" in ele
                            or "image_url" in ele
                            or "video" in ele
                            or ele.get("type","") in ("image", "image_url", "video")
                        ):
                            vision_infos.append(ele)
        return vision_infos
    
    def smart_nframes(ele,total_frames,video_fps):
        """用于计算抽取的视频帧数。
    
        Args:
            ele (dict): 包含视频配置的字典格式
                - fps: fps用于控制提取模型输入帧的数量。
            total_frames (int): 视频的原始总帧数。
            video_fps (int | float): 视频的原始帧率
    
        Raises:
            nframes应该在[FRAME_FACTOR，total_frames]间隔内，否则会报错
    
        Returns:
            用于模型输入的视频帧数。
        """
        assert not ("fps" in ele and "nframes" in ele), "Only accept either `fps` or `nframes`"
        fps = ele.get("fps", FPS)
        min_frames = ceil_by_factor(ele.get("min_frames", FPS_MIN_FRAMES), FRAME_FACTOR)
        max_frames = floor_by_factor(ele.get("max_frames", min(FPS_MAX_FRAMES, total_frames)), FRAME_FACTOR)
        duration = total_frames / video_fps if video_fps != 0 else 0
        if duration-int(duration)>(1/fps):
            total_frames = math.ceil(duration * video_fps)
        else:
            total_frames = math.ceil(int(duration)*video_fps)
        nframes = total_frames / video_fps * fps
        if nframes > total_frames:
            logger.warning(f"smart_nframes: nframes[{nframes}] > total_frames[{total_frames}]")
        nframes = int(min(min(max(nframes, min_frames), max_frames), total_frames))
        if not (FRAME_FACTOR <= nframes and nframes <= total_frames):
            raise ValueError(f"nframes should in interval [{FRAME_FACTOR}, {total_frames}], but got {nframes}.")
    
        return nframes
    
    def get_video(video_path):
        # 获取视频信息
        cap = cv2.VideoCapture(video_path)
    
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        # 获取视频高度
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
        video_fps = cap.get(cv2.CAP_PROP_FPS)
        return frame_height, frame_width, total_frames, video_fps
    
    def smart_resize(ele, path, factor=IMAGE_FACTOR):
        # 获取原视频的宽和高
        height, width, total_frames, video_fps = get_video(path)
        # 视频帧的Token下限
        min_pixels = VIDEO_MIN_PIXELS
        total_pixels = VIDEO_TOTAL_PIXELS
        # 抽取的视频帧数
        nframes = smart_nframes(ele, total_frames, video_fps)
        max_pixels = max(min(VIDEO_MAX_PIXELS, total_pixels / nframes * FRAME_FACTOR),int(min_pixels * 1.05))
    
        # 视频的长宽比不应超过200:1或1:200
        if max(height, width) / min(height, width) > MAX_RATIO:
            raise ValueError(
                f"absolute aspect ratio must be smaller than {MAX_RATIO}, got {max(height, width) / min(height, width)}"
            )
    
        h_bar = max(factor, round_by_factor(height, factor))
        w_bar = max(factor, round_by_factor(width, factor))
        if h_bar * w_bar > max_pixels:
            beta = math.sqrt((height * width) / max_pixels)
            h_bar = floor_by_factor(height / beta, factor)
            w_bar = floor_by_factor(width / beta, factor)
        elif h_bar * w_bar < min_pixels:
            beta = math.sqrt(min_pixels / (height * width))
            h_bar = ceil_by_factor(height * beta, factor)
            w_bar = ceil_by_factor(width * beta, factor)
        return h_bar, w_bar
    
    def token_calculate(video_path, fps):
        # 传入视频路径和fps抽帧参数
        messages = [{"content": [{"video": video_path, "fps": fps}]}]
        vision_infos = extract_vision_info(messages)[0]
    
        resized_height, resized_width = smart_resize(vision_infos, video_path)
    
        height, width, total_frames, video_fps = get_video(video_path)
        num_frames = smart_nframes(vision_infos, total_frames, video_fps)
        print(f"原视频尺寸：{height}*{width}， 输入模型的尺寸：{resized_height}*{resized_width}，视频总帧数:{total_frames}，fps等于{fps}时，抽取的总帧数：{num_frames}", end="，")
        video_token = int(math.ceil(num_frames / 2) * resized_height / 32 * resized_width / 32)
        video_token += 2   # 系统会自动添加<|vision_bos|>和<|vision_eos|>视觉标记（各计1个Token）
        return video_token
    
    video_token = token_calculate("xxx/test.mp4", 1)
    print("视频tokens:", video_token)
    ```
    
-   **图像列表：**
    
    当以图像列表形式传入视频时，表示已预先完成视频抽帧，可使用以下代码，通过传入图像的路径和数量来计算传入图像列表时消耗的Token数：
    
    ```
    # 使用前安装：pip install Pillow
    import math
    import os
    import logging
    from typing import Tuple
    from PIL import Image
    
    logger = logging.getLogger(__name__)
    
    # ==================== 常量定义 ====================
    FRAME_FACTOR = 2
    # Qwen3-VL、qwen-vl-max-0813、qwen-vl-plus-0815、qwen-vl-plus-0710模型，缩放因子为32
    IMAGE_FACTOR = 32
    
    #  其他模型，缩放因子为28
    # IMAGE_FACTOR = 28
    
    # Token计算相关常量
    TOKEN_DIVISOR = 32  # token计算时的除数
    VISION_SPECIAL_TOKENS = 2  # <|vision_bos|>和<|vision_eos|>标记
    
    # 视频帧的最大长宽比
    MAX_RATIO = 200
    # 视频帧的像素下限
    VIDEO_MIN_PIXELS = 4 * 32 * 32
    # 视频帧的像素上限，使用Qwen3-VL-Plus模型，VIDEO_MAX_PIXELS为640 * 32 * 32，其他模型为768 * 32 * 32
    VIDEO_MAX_PIXELS = 640 * 32 * 32
    
    # 视频输入的最大像素值，使用Qwen3-VL-Plus模型，请将VIDEO_TOTAL_PIXELS设置为131072 * 32 * 32，其他模型设置为65536 * 32 * 32
    VIDEO_TOTAL_PIXELS = int(float(os.environ.get('VIDEO_MAX_PIXELS', 131072 * 32 * 32)))
    
    def round_by_factor(number: int, factor: int) -> int:
        """返回与”number“最接近的整数，该整数可被”factor“整除。"""
        return round(number / factor) * factor
    
    def ceil_by_factor(number: int, factor: int) -> int:
        """返回大于或等于“number”且可被“factor”整除的最小整数。"""
        return math.ceil(number / factor) * factor
    
    def floor_by_factor(number: int, factor: int) -> int:
        """返回小于或等于“number”且可被“factor”整除的最大整数。"""
        return math.floor(number / factor) * factor
    
    def get_image_size(image_path: str) -> Tuple[int, int]:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"图像文件不存在: {image_path}")
    
        try:
            image = Image.open(image_path)
            height = image.height
            width = image.width
            image.close()  # 及时关闭文件
            return height, width
        except Exception as e:
            raise ValueError(f"无法读取图像文件 {image_path}: {str(e)}")
    
    def smart_resize(height: int, width: int, nframes: int, factor: int = IMAGE_FACTOR) -> Tuple[int, int]:
        """
        计算图像缩放后的尺寸
    
        Args:
            height: 原始图像高度
            width: 原始图像宽度
            nframes: 视频帧数
            factor: 缩放因子，默认为IMAGE_FACTOR
    
        Returns:
            (resized_height, resized_width) 缩放后的高度和宽度
    
        Raises:
            ValueError: 长宽比超过限制
        """
        # 视频帧的Token下限
        min_pixels = VIDEO_MIN_PIXELS
        total_pixels = VIDEO_TOTAL_PIXELS
        # 抽取的视频帧数
        max_pixels = max(min(VIDEO_MAX_PIXELS, total_pixels / nframes * FRAME_FACTOR), int(min_pixels * 1.05))
    
        # 视频的长宽比不应超过200:1或1:200
        aspect_ratio = max(height, width) / min(height, width)
        if aspect_ratio > MAX_RATIO:
            raise ValueError(
                f"图像长宽比必须小于 {MAX_RATIO}:1，当前为 {aspect_ratio:.2f}:1"
            )
    
        h_bar = max(factor, round_by_factor(height, factor))
        w_bar = max(factor, round_by_factor(width, factor))
        if h_bar * w_bar > max_pixels:
            beta = math.sqrt((height * width) / max_pixels)
            h_bar = floor_by_factor(height / beta, factor)
            w_bar = floor_by_factor(width / beta, factor)
        elif h_bar * w_bar < min_pixels:
            beta = math.sqrt(min_pixels / (height * width))
            h_bar = ceil_by_factor(height * beta, factor)
            w_bar = ceil_by_factor(width * beta, factor)
        return h_bar, w_bar
    
    def calculate_video_tokens(image_path: str, nframes: int = 1, factor: int = IMAGE_FACTOR, verbose: bool = True) -> int:
        """
    
        Args:
            image_path: 视频帧文件路径
            nframes: 视频帧数，
            factor: 缩放因子，默认为IMAGE_FACTOR
            verbose: 是否打印详细信息
    
        Returns:
            所消耗的token数量
    
        Raises:
            FileNotFoundError: 文件不存在
            ValueError: 文件格式无效或长宽比超限
        """
        # 获取原始图像尺寸（只读取一次）
        height, width = get_image_size(image_path)
    
        # 计算缩放后的尺寸
        resized_height, resized_width = smart_resize(height, width, nframes, factor)
    
        # 计算token数量
        # 公式：⌈帧数/2⌉ × (高度/TOKEN_DIVISOR) × (宽度/TOKEN_DIVISOR) + VISION_SPECIAL_TOKENS
        video_token = int(
            math.ceil(nframes / 2) *
            (resized_height / TOKEN_DIVISOR) *
            (resized_width / TOKEN_DIVISOR)
        )
        # 添加视觉标记token（<|vision_bos|>和<|vision_eos|>）
        video_token += VISION_SPECIAL_TOKENS
    
        if verbose:
            print(f"原视频帧尺寸：{height}×{width}，输入模型的尺寸：{resized_height}×{resized_width}，", end="")
    
        return video_token
    
    if __name__ == "__main__":
        try:
            video_token = calculate_video_tokens("xxx/test.jpg", nframes=30)
            print(f"视频tokens: {video_token}\n")
        except Exception as e:
            print(f"错误: {str(e)}\n")
    ```
    

### **图像生成模型-万相**

**说明**

模型训练流程请参见[图像生成模型调优](https://help.aliyun.com/zh/model-studio/wan-image-generation-finetune-guide)。训练完成后的新模型需先完成**模型部署**，才能调用。

**计费方式**

按训练Token计费

**计费公式**

模型训练费用 = 训练Token总量 × 训练单价（计费单位：每千Token）

**训练Token总量的计算公式**

训练Token总量≈max\_steps×Lstep​

其中：

-   max\_steps：训练时指定的超参数，表示最大训练步数（创建微调任务时配置）。
    
-   Lstep：每步的Token消耗量，计算公式为：
    
    Lstep​\=i∈batch∑​Litem(i)​≤Lmax​
    
    Lstep 近似等于 Lmax。Lmax 由 max\_token\_length 和 generation\_type 共同决定，具体取值如下表：
    

**generation\_type**

**max\_token\_length**

**L****max**

t2i（文生图）

1k

128,000

2k

232,200

i2i（图生图）

1k

232,200

2k

320,000

**模型服务**

**模型名称**

**训练价格（每千Token）**

万相-图像生成

wan2.7-image-pro

0.08元

万相-图像生成

wan2.7-image

0.08元

**计费示例**

假设使用 wan2.7-image-pro 模型进行 t2i 微调，max\_steps = 200，max\_token\_length = "1k"，训练单价 = 0.08元/千Token：

-   查表得 Lmax = 128,000（generation\_type=t2i，max\_token\_length=1k），Lstep ≈ Lmax = 128,000
    
-   训练Token总量 ≈ 200 × 128,000 = 25,600,000 = 25,600千Token
    
-   模型训练费用 ≈ 25,600 × 0.08 = 2,048元
    

### **视频生成模型-万相**

**说明**

模型训练流程请参见[模型调优](https://help.aliyun.com/zh/model-studio/wan-video-generation-finetune-guide)。训练完成后的新模型需先完成**模型部署**，才能调用。

**计费方式**

按训练Token计费

**计费公式**

模型训练费用 = 训练Token总量 × 训练单价（计费单位：每千Token）

**训练Token总量的计算公式**

训练Token总量\=(i\=1∑N​视频i​的计费时长)×1024max\_pixels​×n\_epochs

其中：

-   N：训练集中的视频总数。
    
-   max\_pixels：训练时指定的超参数，表示视频的最大像素数（创建微调任务时配置）。
    
-   n\_epochs：训练时指定的超参数，表示循环次数（创建微调任务时配置）。
    
-   单个视频计费时长计算规则：先将原始视频时长（秒）四舍五入取整，再根据模型限制取最终值。
    
    -   wan2.5模型：`计费时长=min(10, 四舍五入后的时长)`，即单条视频最多按 10 秒计算。
        
    -   wan2.2模型：`计费时长=min(5, 四舍五入后的时长)`，即单条视频最多按 5 秒计算。
        

**模型服务**

**模型名称**

**训练价格（每千Token）**

万相-图生视频-基于首帧

wan2.2-i2v-flash

0.06元

wan2.5-i2v-preview

0.32元

图生视频-基于首尾帧

wan2.2-kf2v-flash

0.06元

**计费示例**

假设训练集包含 2 条视频，时长分别为 3.4 秒 和 6.5 秒，max\_pixels = 262144，n\_epochs = 400，训练单价 = 0.06元/千Token：

-   时长计算：
    
    -   视频 1：3.4 → 四舍五入 → 3 秒 → 计费时长 = min(5, 3) = 3
        
    -   视频 2：6.5 → 四舍五入 → 7 秒 → 计费时长 = min(5, 7) = 5
        
    -   总计费时长 = 3 + 5 = 8 秒
        
-   训练Token总量 = 8 ×（262144/1024）× 400 = 819200 = 819.2千Token
    
-   模型训练费用 = 819.2 × 0.06 = 49.152元
    

## **模型部署计费**

### **文本生成模型-千问**

#### 按使用时长计费（预置吞吐）

`**费用 = 使用时长 × (输入 TPM 单价 × 输入 TPM + 输出 TPM 单价 × 输出 TPM)**`

后付费按小时计算：使用时长单位为小时，单价取下表"持续 1 小时"列；预付费按天计算：使用时长单位为天，单价取下表"持续 1 天"列。

-   预付费订单支付后实时生效，有效期 N 天至第 N 天 23:59 结束。若在 22:00 后下单，到期日将自动顺延1天。
    
-   预付费订单到期后，将延后2小时停止服务，停止后资源保留14小时后释放。
    
-   预付费订单无法提前终止服务。
    
-   后付费时，如果账户欠费，部署的资源将继续保留并计费 24 小时，在这 24 小时内服务仍可正常使用。超过 24 小时后系统停止计费，模型部署进入欠费状态，底层资源将被删除，但模型部署任务仍会保留。补足欠费后，系统将重新分配资源并恢复使用（恢复后继续产生费用）。如果您不希望继续产生费用，可删除模型部署任务，删除成功后将不再计费。
    

当模型输入超过最长输入 Token 或 超出购买的 TPM 量时，相关调用将自动切换为当前模型的按量付费模式。此时，推理性能可能下降，将受业务空间中当前快照模型的公共流量的管控，[费用](https://help.aliyun.com/zh/model-studio/model-pricing)按模型调用（按量付费）标准计收。

-   此时，调用 API 返回 Header 将包含：`x-dashscope-ptu-overflow:true`。
    
-   TPM 统计请前往：[模型监控（北京）](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)。
    

缩容场景（降配）的具体降费退费规则请参考：[降配退款规则说明](https://help.aliyun.com/zh/user-center/description-of-downgrade-refund-rules)。

##### 千问

**模型名称**

**模型代码**

**最长输入Token**

**后付费输入**

**Per 10K TPM/小时**

**后付费输出**

**Per 1K TPM/小时**

**预付费输入**

**Per 10K TPM/天**

**预付费输出**

**Per 1K TPM/天**

千问3.7-Max-2026-05-20

qwen3.7-max-2026-05-20

256K

¥28.8

¥8.64

¥345.6

¥103.68

千问3.7-Plus-2026-05-26

qwen3.7-plus-2026-05-26

256K

¥4.8

¥1.92

¥57.6

¥23.04

千问3.6-Flash-2026-04-16

qwen3.6-flash-2026-04-16

128K

¥2.88

¥1.73

¥34.56

¥20.74

千问3.6-Plus-2026-04-02

qwen3.6-plus-2026-04-02

128K

¥4.8

¥2.88

¥57.6

¥34.56

千问3.5-Plus-2026-04-20

qwen3.5-plus-2026-04-20

128K

¥1.92

¥1.15

¥23.04

¥13.82

千问3-Max-2025-09-23

qwen3-max-2025-09-23

128K

¥7.68

¥3.08

¥92.16

¥36.96

千问-Flash-2025-07-28

qwen-flash-2025-07-28

128K

¥0.36

¥0.36

¥4.32

¥4.32

千问-Plus-2025-12-01

qwen-plus-2025-12-01

128K

¥1.92

非思考：¥0.48

思考：¥1.92

¥23.04

非思考：¥5.76

思考：¥23.04

##### DeepSeek

**模型名称**

**模型代码**

**最长输入Token**

**后付费输入**

**Per 10K TPM/小时**

**后付费输出**

**Per 1K TPM/小时**

**预付费输入**

**Per 10K TPM/天**

**预付费输出**

**Per 1K TPM/天**

DeepSeek-v4-Flash

deepseek-v4-flash

256K

¥3.6

¥0.72

¥43.2

¥8.64

DeepSeek-v4-Pro

deepseek-v4-pro

256K

¥43.2

¥8.64

¥518.4

¥103.68

DeepSeek-v3.2

deepseek-v3.2

64K

¥7.2

¥1.08

¥86.4

¥12.96

DeepSeek-v3

deepseek-v3

64K

¥7.2

¥2.88

¥86.4

¥34.56

##### 千问VL

**模型名称**

**模型代码**

**最长输入Token**

**后付费输入**

**Per 10K TPM/小时**

**后付费输出**

**Per 1K TPM/小时**

**预付费输入**

**Per 10K TPM/天**

**预付费输出**

**Per 1K TPM/天**

千问3-VL-Plus-2025-09-23

qwen3-vl-plus-2025-09-23

128K

¥2.4

¥2.4

¥28.8

¥28.8

##### 更多模型

**模型名称**

**模型代码**

**最长输入Token**

**后付费输入**

**Per 10K TPM/小时**

**后付费输出**

**Per 1K TPM/小时**

**预付费输入**

**Per 10K TPM/天**

**预付费输出**

**Per 1K TPM/天**

GLM-5.1

glm-5.1

64K

¥21.6

¥8.64

¥259.2

¥103.68

#### 按使用时长计费（模型单元）

`**费用 = 使用时长（小时）× 模型单元数量 × 模型单元单价**`

"模型单元单价"在后付费场景下取下表"小时单价"列；预付费按月计费时，公式改为 **包月数 × 模型单元数量 × 月单价**。

-   预付费购买的首月，如在首月内提前退订，日单价（≈ 月单价 / 30）将按 **1.2** 倍计费（不满一天按一天计费）
    

**说明**

模型单元-后付费方式的算力资源先买到先得。如购买不成功会全额退款。

##### 文本生成

###### 千问

**模型名称**

**模型代码**

**模型单元规格**

**小时单价（元）**

**最小计费：分钟**

**包月单价（元）**

**最小计费：天**

千问3.7-Plus-2026-05-26

qwen3.7-plus-2026-05-26

MU3 x 8

¥1,096

¥527,752

千问3.6-35B-A3B

qwen3.6-35b-a3b

MU8 x 1

¥47

¥22,400

MU9 x 1

¥51

¥24,600

千问3.6-27B

qwen3.6-27b

MU9 x 1

¥51

¥24,600

千问3.6-Flash-2026-04-16

qwen3.6-flash-2026-04-16

MU1 x 2

¥108

¥52,236

千问3.6-Plus-2026-04-02

qwen3.6-plus-2026-04-02

MU1 x 8

MU1 x 16（PD分离模式）

¥432

PD分离模式：¥864

¥208,944

PD分离模式：¥417,888

千问3.5-397B-A17B

qwen3.5-397b-a17b

MU2 x 8

¥504

¥240,288

MU3 x 8

MU3 x 16（PD分离模式）

¥1,096

PD分离模式：¥2,192

¥527,752

PD分离模式：¥1,055,504

MU6 x 16

¥400

¥193,424

千问3.5-122B-A10B

qwen3.5-122b-a10b

MU1 x 4

¥216

¥104,472

MU2 x 8

¥504

¥240,288

MU6 x 16

¥400

¥193,424

MU9 x 2

¥102

¥49,200

千问3.5-35B-A3B

qwen3.5-35b-a3b

MU1 x 2

¥108

¥52,236

MU2 x 8

¥504

¥240,288

MU8 x 1

¥47

¥22,400

MU9 x 1

¥51

¥24,600

千问3.5-27B

qwen3.5-27b

MU9 x 1

¥51

¥24,600

千问3.5-9B

qwen3.5-9b

MU8 x 1

¥47

¥22,400

MU9 x 1

¥51

¥24,600

千问3.5-Flash-2026-02-23

qwen3.5-flash-2026-02-23

MU1 x 2

¥108

¥52,236

千问3.5-Plus-2026-02-15

qwen3.5-plus-2026-02-15

MU1 x 16（PD分离模式）

PD分离模式：¥864

PD分离模式：¥417,888

MU3 x 8

MU3 x 16（PD分离模式）

¥1,096

PD分离模式：¥2,192

¥527,752

PD分离模式：¥1,055,504

千问3-235B-A22B-Instruct-2507

qwen3-235b-a22b-instruct-2507

MU1 x 4

¥216

¥104,472

MU2 x 8

¥504

¥240,288

千问3-Next-80B-A3B-Instruct

qwen3-next-80b-a3b-instruct

MU1 x 2

¥108

¥52,236

千问3-32B

qwen3-32b

MU1 x 4

¥216

¥104,472

MU6 x 4

¥100

¥48,356

千问3-30B-A3B

qwen3-30b-a3b

MU9 x 2

¥102

¥49,200

千问3-30B-A3B-Instruct-2507

qwen3-30b-a3b-instruct-2507

MU1 x 4

¥216

¥104,472

MU2 x 8

¥504

¥240,288

千问3-8B

qwen3-8b

MU1 x 2

¥108

¥52,236

MU2 x 2

¥126

¥60,072

MU5 x 1

¥21

¥10,139

千问3-4B

qwen3-4b

MU1 x 2

¥108

¥52,236

MU5 x 1

¥21

¥10,139

千问3-1.7B

qwen3-1.7b

MU1 x 2

¥108

¥52,236

MU5 x 1

¥21

¥10,139

千问3-Embedding-0.6B

qwen3-embedding-0.6b

MU5 x 1

¥21

¥10,139

MU6 x 1

¥25

¥12,089

千问3-MoE-Rerank-0.6B

qwen3-moe-rerank-0.6b

MU5 x 1

¥21

¥10,139

千问3-Rerank-0.6B

qwen3-rerank-0.6b

MU5 x 1

¥21

¥10,139

MU6 x 1

¥25

¥12,089

千问3-Max-2025-09-23

qwen3-max-2025-09-23

MU2 x 8

¥504

¥240,288

MU3 x 8

¥1,096

¥527,752

千问3-Rerank

qwen3-rerank

MU5 x 1

¥21

¥10,139

千问2.5-开源版-72B

qwen2.5-72b-instruct

MU1 x 4

¥216

¥104,472

千问2.5-开源版-32B

qwen2.5-32b-instruct

MU1 x 4

¥216

¥104,472

千问2.5-开源版-14B

qwen2.5-14b-instruct

MU1 x 2

¥108

¥52,236

千问2.5-开源版-7B

qwen2.5-7b-instruct

MU1 x 2

¥108

¥52,236

MU5 x 1

¥21

¥10,139

千问2.5-开源版-3B

qwen2.5-3b-instruct

MU5 x 1

¥21

¥10,139

千问-Flash-2025-07-28

qwen-flash-2025-07-28

MU1 x 4

¥216

¥104,472

千问-Plus-2025-07-28

qwen-plus-2025-07-28

MU1 x 4

MU1 x 16（PD分离模式）

¥216

PD分离模式：¥864

¥104,472

PD分离模式：¥417,888

千问-Plus-2025-12-01

qwen-plus-2025-12-01

MU1 x 4

¥216

¥104,472

###### GLM

**模型名称**

**模型代码**

**模型单元规格**

**小时单价（元）**

**最小计费：分钟**

**包月单价（元）**

**最小计费：天**

GLM-5.1

glm-5.1

MU2 x 8

MU2 x 16（PD分离模式）

¥504

PD分离模式：¥1,008

¥240,288

PD分离模式：¥480,576

MU3 x 16（PD分离模式）

PD分离模式：¥2,192

PD分离模式：¥1,055,504

MU6 x 16

¥400

¥193,424

GLM-5

glm-5

MU3 x 16（PD分离模式）

PD分离模式：¥2,192

PD分离模式：¥1,055,504

GLM-4.7

glm-4.7

MU6 x 32（PD分离模式）

PD分离模式：¥800

PD分离模式：¥386,848

###### DeepSeek

**模型名称**

**模型代码**

**模型单元规格**

**小时单价（元）**

**最小计费：分钟**

**包月单价（元）**

**最小计费：天**

DeepSeek-v4-Flash

deepseek-v4-flash

MU1 x 8

¥432

¥208,944

DeepSeek-v3.2

deepseek-v3.2

MU2 x 16（PD分离模式）

PD分离模式：¥1,008

PD分离模式：¥480,576

###### 更多模型

**模型名称**

**模型代码**

**模型单元规格**

**小时单价（元）**

**最小计费：分钟**

**包月单价（元）**

**最小计费：天**

MiniMax-M2.5

MiniMax-M2.5

MU1 x 16（PD分离模式）

PD分离模式：¥864

PD分离模式：¥417,888

Kimi-K2.5

kimi-k2.5

MU2 x 8

¥504

¥240,288

模型类型：

-   Instruct - 模型部署后以**非思考模式**进行推理。
    
-   Thinking - 模型部署后以思考模式进行推理。
    

模型部署类型：

-   PD 分离模式 - **降低首 Token 延迟、提高吞吐。**
    
    该部署模式部署的模型在进行模型推理时，将首 Token 计算（Prefill）和后续 Token 计算（Decode）两个计算阶段，拆到不同的计算节点执行。
    

##### 多模态

###### 千问VL

**模型名称**

**模型代码**

**模型单元规格**

**小时单价（元）**

**最小计费：分钟**

**包月单价（元）**

**最小计费：天**

千问3-VL-235B-A22B-Instruct

qwen3-vl-235b-a22b-instruct

MU1 x 4

¥216

¥104,472

千问3-VL-235B-A22B-Thinking

qwen3-vl-235b-a22b-thinking

MU1 x 4

¥216

¥104,472

千问3-VL-32B-Instruct

qwen3-vl-32b-instruct

MU2 x 8

¥504

¥240,288

千问3-VL-8B-Instruct

qwen3-vl-8b-instruct

MU1 x 2

¥108

¥52,236

千问3-VL-4B-Instruct

qwen3-vl-4b-instruct

MU1 x 2

¥108

¥52,236

千问3-VL-2B-Instruct

qwen3-vl-2b-instruct

MU5 x 1

¥21

¥10,139

千问3-VL-Embedding-2B

qwen3-vl-embedding-2b

MU5 x 1

¥21

¥10,139

千问3-VL-Flash-2025-10-15

qwen3-vl-flash-2025-10-15

MU1 x 4

¥216

¥104,472

千问3-VL-Plus-2025-09-23

qwen3-vl-plus-2025-09-23

MU1 x 4

¥216

¥104,472

千问VL-Max-2025-08-13

qwen-vl-max-2025-08-13

MU6 x 4

¥100

¥48,356

千问VL-OCR-2025-11-20

qwen-vl-ocr-2025-11-20

MU6 x 4

¥100

¥48,356

###### 千问 Omni

**模型名称**

**模型代码**

**模型单元规格**

**小时单价（元）**

**最小计费：分钟**

**包月单价（元）**

**最小计费：天**

千问3.5-Omni-Flash

qwen3.5-omni-flash

MU8 x 1

¥47

¥22,400

MU9 x 1

¥51

¥24,600

千问3.5-Omni-Plus

qwen3.5-omni-plus

MU9 x 8

¥408

¥196,800

模型类型：

-   Instruct - 模型部署后以**非思考模式**进行推理。
    
-   Thinking - 模型部署后以思考模式进行推理。
    
-   Instruct/Thinking - 可在模型部署时**选择是否开启思考模式**。
    

##### 语音合成

**CosyVoice**

**模型名称**

**模型代码**

**模型单元规格**

**小时单价（元）**

**包月单价（元）**

cosyvoice-v3-flash

cosyvoice-v3-flash

MU5

¥21

¥10,139

#### 按模型 Token 使用量

`**费用 = 模型输入 Token 数 × 模型输入单价 + 模型输出 Token 数 × 模型输出单价（最小计费单位：1 token）**`

-   仅当对下列基础模型完成 SFT 高效训练并得到自定义模型后，才支持按模型 Token 使用量计费。
    

##### 千问

**基础模型**

**模型代码**

**输入**

**元/千Token**

**输出**

**元/千Token**

千问3-32B

qwen3-32b

¥0.002

非思考模式：¥0.008

思考模式：¥0.02

千问3-14B

qwen3-14b

¥0.001

非思考模式：¥0.004

思考模式：¥0.01

千问3-8B

qwen3-8b

¥0.0005

非思考模式：¥0.002

思考模式：¥0.005

千问2.5-开源版-72B

qwen2.5-72b-instruct

¥0.004

¥0.012

千问2.5-开源版-32B

qwen2.5-32b-instruct

¥0.002

¥0.006

千问2.5-开源版-14B

qwen2.5-14b-instruct

¥0.001

¥0.003

千问2.5-开源版-7B

qwen2.5-7b-instruct

¥0.0005

¥0.001

##### 千问VL

**基础模型**

**模型代码**

**输入**

**元/千Token**

**输出**

**元/千Token**

千问3-VL-8B-Instruct

qwen3-vl-8b-instruct

¥0.0005

¥0.002

千问2.5-VL-72B

qwen2.5-vl-72b-instruct

¥0.016

¥0.048

千问2.5-VL-32B

qwen2.5-vl-32b-instruct

¥0.008

¥0.024

千问2.5-VL-7B

qwen2.5-vl-7b-instruct

¥0.002

¥0.005

### **图像生成模型-万相**

经过SFT-LoRA高效微调的万相图像生成模型，部署免费，调用按微调的基础模型的标准调用价格计费。模型训练和部署流程请参见[图像生成模型调优](https://help.aliyun.com/zh/model-studio/wan-image-generation-finetune-guide)。

**模型名称**

**Lora部署调用价格**

wan2.7-image-pro

0.50元/张

wan2.7-image

0.20元/张

## **常见问题**

#### **Q：**模型部署什么时候开始计费？

A：当模型完成部署，即状态为**运行中**时，开始收取模型部署的费用。模型状态为**部署中**、**欠费**、**部署失败**时，均不会计费。

如果是包月预付费，模型状态为**运行中**后，开始消耗包月时间。

#### **Q：**取消模型训练会收费么？

A：**会收费**。如果您主动取消训练，之前已产生的费用仍会被计算。其他原因导致的训练中断，阿里云百炼不会向您收取训练费用。

#### **Q：怎么查看已部署模型的调用统计？**

A：请访问[模型监控（北京）](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)、[模型监控（弗吉尼亚）](https://modelstudio.console.aliyun.com/us-east-1?tab=dashboard#/model-telemetry)、[模型监控（新加坡）](https://modelstudio.console.aliyun.com/?spm=a2c4g.11186623.0.0.39086143l397a1&tab=model#/model-telemetry)页面。

模型监控页面支持按时间范围（今天、昨天、近3天、近七天、近15天）和推理类型筛选，上方汇总区展示模型总量、总调用次数、总失败次数、平均调用时长、平均首包时长，下方模型列表展示各模型的调用总量、调用失败量、失败率、平均调用时长、平均首Token延时等指标，可单击**监控**查看单模型详细数据。
