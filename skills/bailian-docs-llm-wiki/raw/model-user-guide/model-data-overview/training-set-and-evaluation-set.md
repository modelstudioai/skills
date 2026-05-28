# 训练集与评测集

数据集是模型训练与评测的基础，阿里云百炼模型数据功能可以帮助您高效地创建和管理数据集。

**重要**

本文档仅适用于中国大陆版（北京地域）。

## **支持的数据集**

**[模型数据](https://bailian.console.aliyun.com/#/efm/model_data)**实现了对您业务空间下所有大模型相关数据集的统一管理。这些数据集可分为**训练集**（用于[模型调优](https://help.aliyun.com/zh/model-studio/model-training-overview)）和**评测集**（用于[模型评测](https://help.aliyun.com/zh/model-studio/model-evaluation-overview)）两类。

**类型**

**说明**

**训练集**

用于对大模型进行调优，通过在特定任务的数据集上进行有监督训练，使大模型学会解决特定问题和区分相关特征之间的细微差异，从而显著提升其在特定任务上的准确性和效率。

目前支持**文本生成**、**多模态理解**、**图生视频（首帧）** 、**图生视频（收尾帧）**训练集，详见[下方说明](#cc3d858463790)。

**评测集**

用于评测大模型的泛化能力，即评估经过调优后的大模型在未见过的数据集上的表现如何。

目前支持**文本生成**评测集，详见[下方说明](#9105fad5173kz)。

## 文本生成与多模态理解训练集

### **SFT 训练集**

SFT ChatML（Chat Markup Language）格式训练数据，支持多轮对话和多种角色设置。

> 不支持OpenAI 的`name`、`weight`参数，所有的 assistant 输出都会被训练。

```
# 一行训练数据（json 格式），展开后典型结构如下:
{"messages": [
  {"role": "system", "content": "系统输入1"}, 
  {"role": "user", "content": "用户输入1"}, 
  {"role": "assistant", "content": "期望的模型输出1"}, 
  {"role": "user", "content": "用户输入2"}, 
  {"role": "assistant", "content": "期望的模型输出2"}
  ...
]}
```

system/user/assistant 区别请参见[概述](https://help.aliyun.com/zh/model-studio/text-generation#51574d7e93su4)，训练数据集样例：[SFT-ChatML格式示例.jsonl](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241014/utjdbx/SFT-ChatML%E6%A0%BC%E5%BC%8F%E7%A4%BA%E4%BE%8B.jsonl)、[SFT-ChatML格式示例.xlsx](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251111/jrxbpn/SFT-ChatML%E6%A0%BC%E5%BC%8F%E7%A4%BA%E4%BE%8B.xlsx)（xls、xlsx 格式只支持单轮对话）。

单条训练数据的**所有** assistant 行都支持`"loss_weight"`参数，用于设置该行在训练时的相对重要性。（设置范围`0.0 ~ 1.0`，数值越大，重要性越高）

> 该参数属于邀测参数，如需使用，请联系您的商务经理。

```
{"role": "assistant", "content": "期望的模型输出1", "loss_weight": 1.0}, 
 {"role": "assistant", "content": "期望的模型输出2", "loss_weight": 0.5}
```

### SFT 思考模型（thinking）

训练数据支持多轮对话和多种角色设置，但只能针对**最后**的 assistant 输出进行训练，**一行训练数据展开后结构如下**：

> 思考标签前后的若干个`\n`必须要保留。

```
# 一行训练数据（json 格式），展开后典型结构如下:
{"messages": [
  {"role": "system", "content": "系统输入1"}, 
  {"role": "user", "content": "用户输入1"}, 
  {"role": "assistant", "content": "模型输出1"}, --中间的 assistant 输出不应添加 <think> 标签
   ...
  {"role": "user", "content": "用户输入2"}, 
  {"role": "assistant", "content": "<think>\n期望的思考内容2\n</think>\n\n期望的输出2"} --思考内容只能包含在最后一个 assistant 输出中。 
]}
```

system/user/assistant 区别请参见[概述](https://help.aliyun.com/zh/model-studio/text-generation#51574d7e93su4)，训练数据集样例：[SFT- 深度思考内容示例.jsonl](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251224/txsbci/SFT-+%E6%B7%B1%E5%BA%A6%E6%80%9D%E8%80%83%E5%86%85%E5%AE%B9%E7%A4%BA%E4%BE%8B.jsonl)。

也可以在训练样本中设置模型不输出`<think>`标签， 如果使用这种输出方式，模型训练完成后**不建议再开启思考模式进行调用**。

```
{"role": "assistant", "content": "期望的模型输出2"}  --告诉模型不开启思考
```

单条训练数据**最后**的 assistant 行支持`"loss_weight"`参数，用于设置该条数据在训练时的相对重要性。（设置范围`0.0 ~ 1.0`，数值越大，重要性越高）

> 该参数属于邀测参数，如需使用，请联系您的商务经理。

```
{"role": "assistant", "content": "<think>\n期望的思考内容2\n</think>\n\n期望的输出2", "loss_weight": 1.0}
```

### SFT 视觉理解（千问VL）

> 不支持OpenAI 的`name`、`weight`参数，所有的 assistant 输出都会被训练。

system/user/assistant 区别请参见[概述](https://help.aliyun.com/zh/model-studio/text-generation#51574d7e93su4)。ChatML 格式训练数据样例：

> 如需传入 `system` 消息，对应的 `content` 必须使用数组格式 `[{"text":"..."}]`，不能使用字符串格式 `"content":"字符串"`。

```
# 一行训练数据（json 格式），展开后典型结构如下：
{"messages": [
  {"role": "system", "content": [{"text": "系统输入"}]},
  {"role": "user", "content": [{"text": "用户输入1"}, {"image": "图像文件名1.jpg", "resized_width": 200, "resized_height": 200}]},
  {"role": "assistant", "content": [{"text": "期望的模型输出1"}]},
  {"role": "user", "content": [{"text": "用户输入2"}, {"video": "视频文件名1.mp4", "fps": 3.0, "resized_width": 200, "resized_height": 200, "video_start": 0.0, "video_end": 3.0}]},
  {"role": "assistant", "content": [{"text": "期望的模型输出2"}]},
  {"role": "user", "content": [{"text": "用户输入2"}, {"video": ["0.jpg", "1.jpg", "2.jpg", "3.jpg"], "sample_fps": 5.0, "resized_width": 200, "resized_height": 200}]},
  {"role": "assistant", "content": [{"text": "期望的模型输出2"}]},
  ...
]}
```

点击此处查看更多支持的参数

**字段**

**类型**

**必填**

**说明**

**图片文件**

`image`

`str`

是

图片文件路径

`resized_width`

`int`

否

图片目标缩放宽度（像素）

`resized_height`

`int`

否

图片目标缩放高度（像素）

**视频文件-视频文件路径模式（仅 qwen3.5 及以后的 VL 模型支持）**

**样例：**[阿里云VL\_Video.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260514/xllbzy/%E9%98%BF%E9%87%8C%E4%BA%91VL_Video.zip)

`video`

`str` 

是

视频文件路径模式：`{"video": "视频文件名1.mp4"}`

`resized_width`

`int`

否

视频目标缩放宽度（像素）

`resized_height`

`int`

否

视频目标缩放高度（像素）

`fps`

`float`

否

训练时的输入频率。如果设置`fps=30`，实际训练用的视频帧率为 30 帧。

`video_start`

`float`

否

视频截取起始时间（秒）

`video_end`

`float`

否

视频截取结束时间（秒）

**视频文件-图片帧列表模式（仅 qwen3.5 及以后的 VL 模型支持）**

`video`

`List[str]`

是

图片帧列表模式：`{"video": ["0.jpg", "1.jpg", "2.jpg", ...], "sample_fps": 2.0}`

`sample_fps`

`float`

否

用于告知图片帧的帧率。

`resized_width`

`int`

否

图片帧缩放宽度（像素）

`resized_height`

`int`

否

图片帧缩放高度（像素）

**说明**

如果训练思考模型（Thinking），也需要遵循[SFT 思考模型（thinking）](#f5454632ef4yo)的数据格式要求。

#### **压缩包要求：**

1.  压缩包格式：ZIP。最大支持 2 GB， ZIP 包内文件夹、文件名仅支持 ASCII 字符集中的字母 (a-z, A-Z)、数字 (0-9)、下划线 (\_)、连字符 (-)。
    
2.  训练文本数据固定为 data.jsonl，并且位于压缩包的**根目录**下，应**确保压缩后打开 zip 文件，直接就能看到** `**data.jsonl**` **文件。**
    
3.  图片单张尺寸的宽度和高度均不得超过 1024px，最大不超过10MB，支持 `.bmp`, `.jpeg /.jpg`, `.png`, `.tif /.tiff`, `.webp` 格式。
    
4.  图片文件的名称不能重复，即使分布在不同的文件夹中。
    
5.  压缩包目录结构：
    
    ##### **单层目录（推荐）**
    
    图片文件与 `data.jsonl` 文件均位于压缩包根目录下。
    
    ```
    Trainingdata_vl.zip
       |--- data.jsonl #注意：外层不能再包裹文件夹
       |--- image1.png
       |--- video1.mp4
    ```
    
    ##### 多层目录
    
    1.  data.jsonl 必须在压缩包根目录下。
        
    2.  data.jsonl 内只需要声明图像/视频文件名，**不需要声明文件路径**。例如：
        
        **正确示例**：`image1.jpg`；**错误示例**：`jpg_folder/image1.jpg`。
        
    3.  图像/视频文件名应在压缩包内全局唯一。
        
    
    ```
    Trainingdata_vl.zip
        |--- data.jsonl #注意：外层不能再包裹文件夹
        |--- jpg_folder
        |   └── image1.jpg
        |--- mp4_folder
            └── video.mp4
    ```
    

### DPO 数据集

DPO ChatML 格式训练数据，**一行训练数据展开后结构如下**：

system/user/assistant 区别请参见[概述](https://help.aliyun.com/zh/model-studio/text-generation#51574d7e93su4)，训练数据集样例：[DPO ChatML格式样例.jsonl](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241014/ihjgry/DPO+ChatML%E6%A0%BC%E5%BC%8F%E6%A0%B7%E4%BE%8B.jsonl)。

```
# 一行训练数据（json 格式），展开后典型结构如下:
{"messages": [
  {"role": "system", "content": "系统输入"},
  {"role": "user", "content": "用户输入1"},
  {"role": "assistant", "content": "模型输出1"},
  {"role": "user", "content": "用户输入2"},
  {"role": "assistant", "content": "模型输出2"},
  {"role": "user", "content": "用户输入3"}
 ],
 "chosen":
   {"role": "assistant", "content": "赞同的模型期望输出3"},
 "rejected":
   {"role": "assistant", "content": "反对的模型期望输出3"}}
```

模型将 `messages` 内的所有内容均作为输入，DPO 用于训练模型对`用户输入3`的正负反馈。

针对深度思考的内容，需要使用`<think>`标签包裹：

```
{"role": "assistant", "content": "<think>期望的模型思考内容</think>期望的模型输出"}
```

单条训练数据的`"chosen"`模块支持`"loss_weight"`参数，用于设置该条训练数据在训练中的相对重要性。（设置范围`0.0 ~ 1.0`，数值越大，重要性越高）

> 该参数属于邀测参数，如需使用，请联系您的商务经理。

```
"chosen":
   {"role": "assistant", "content": "赞同的模型期望输出3", "loss_weight": 1.0},
```

### CPT 训练集

CPT 纯文本格式训练数据，**一行训练数据展开后结构如下**：

```
{"text":"文本内容"}
```

训练数据集样例：[CPT-文本生成训练集示例.jsonl](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241127/qrtlrz/CPT-%E6%96%87%E6%9C%AC%E7%94%9F%E6%88%90%E8%AE%AD%E7%BB%83%E9%9B%86%E6%A0%BC%E5%BC%8F%E7%A4%BA%E4%BE%8B.jsonl)

## 图生视频训练集

### **数据集格式**

#### **训练集：必须提供**

##### 图生视频-基于首帧

训练集包括**首帧图像、训练视频和标注文件（data.jsonl）**。

-   训练集样例：[wan-i2v-training-dataset.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251107/ujfrui/wan-i2v-training-dataset.zip)。
    
-   zip包目录结构：
    
    ```
    wan-i2v-training-dataset.zip
    ├── data.jsonl        # 必须固定命名为data.jsonl，最大支持 20MB
    ├── image_1.jpeg      # 图像最大分辨率为4096*4096，支持BMP、JPEG、PNG、WEBP格式
    ├── video_1.mp4       # 视频最大分辨率为4096*4096，支持MP4、MOV格式
    ├── image_2.jpeg
    └── video_2.mp4
    ```
    
-   标注文件（data.jsonl）：每一行代表一条训练数据，必须为JSON 对象。一行训练数据的结构如下：
    
    ```
    {
        "prompt": "视频开头展示了一位年轻女性站在一堵爬满常春藤的砖墙前。她有着一头柔顺的红棕色长发，穿着一件白色的无袖连衣裙，佩戴着一条闪亮的银色项链，面带微笑。背景中的砖墙被绿色的藤蔓覆盖，显得古朴而自然。然后开始展示s86b5p金钱雨特效，无数巨大尺寸的美元钞票（米黄底/深绿图案）如暴雨般倾泻而下，密集地砸向并环绕她。钞票持续落下，她双臂舒展上扬，脖颈微仰，表情惊喜，完全沉浸在这场狂野的金钱雨中。",
        "first_frame_path": "image_1.jpg",
        "video_path": "video_1.mp4"        
    }
    ```
    

##### 图生视频-基于首尾帧

训练集包括**首帧图像、尾帧图像、训练视频和标注文件（data.jsonl）**。

-   训练集样例：[wan-kf2v-training-dataset.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260119/wapfil/wan-kf2v-training-dataset.zip)。
    
-   zip包目录结构：
    
    ```
    wan-kf2v-training-dataset.zip
    ├── data.jsonl                # 必须固定命名为data.jsonl，最大支持 20MB
    ├── image/                    # 存放首帧和尾帧图像
    │   ├── image_1_first.jpg     # 图像最大分辨率为4096*4096，支持BMP、JPEG、PNG、WEBP格式
    │   └── image_1_last.png
    └── video/                    # 存放作为“训练目标”的视频文件
        ├── video_1.mp4           # 视频最大分辨率为4096*4096，支持MP4、MOV格式
        └── video_2.mov
    ```
    
-   标注文件（data.jsonl）：每一行代表一条训练数据，必须为JSON 对象。一行训练数据的结构如下：
    
    ```
    {
        "prompt": "视频开头展示了一位年轻女性在户外的场景。她有着短而卷曲的深棕色头发，面带微笑，显得非常亲切。她穿着一件黑色的Polo衫，上面有彩色的花卉刺绣图案，背景是绿色的植被和远处的山脉。然后她开始了s86b5p变身。",
        "first_frame_path": "image/image_1_first.jpg",
        "last_frame_path": "image/image_1_last.jpg", 
        "video_path": "video/video_1.mp4"  
    }
    ```
    

#### **验证集：可选**

##### 图生视频-基于首帧

验证集包括**首帧图像和标注文件（data.jsonl）**，无需提供视频。训练任务会在每个评估节点，自动调用模型服务，使用验证集的图像和 Prompt 生成预览视频。

-   验证集样例**：**[wan-i2v-valid-dataset.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251113/iumzue/wan-i2v-valid-dataset.zip)。
    
-   zip包目录结构：
    
    ```
    wan-i2v-valid-dataset.zip
    ├── data.jsonl       # 必须固定命名为data.jsonl，最大支持 20MB
    ├── image_1.jpeg     # 图像最大分辨率为4096*4096，支持BMP、JPEG、PNG、WEBP格式
    └── image_2.jpeg
    ```
    
-   标注文件（data.jsonl）：每一行代表一条验证数据，必须为JSON 对象。一行验证数据的结构如下：
    
    ```
    {
        "prompt": "视频开头展示了一位年轻男性站在城市景观前的场景。他穿着黑白格子外套，内搭黑色连帽衫，面带微笑，神情自信。背景是夕阳下的城市天际线，远处可以看到著名的圆顶建筑和错落有致的屋顶，天空中云层密布，呈现出温暖的橙黄色调。然后开始展示s86b5p金钱雨特效，无数巨大尺寸的美元钞票（米黄底/深绿图案）如暴雨般倾泻而下，密集地砸向并环绕他。钞票持续落下，同时镜头缓缓拉进，他双臂舒展上扬，脖颈微仰，表情惊喜，完全沉浸在这场狂野的金钱雨中。",
        "first_frame_path": "image_1.jpg"
    }
    ```
    

##### 图生视频-基于首尾帧

验证集包括**首帧图像、尾帧图像和标注文件（data.jsonl）**，无需提供视频。训练任务会在每个评估节点，自动调用模型服务，使用验证集的图像和 Prompt 生成预览视频。

-   验证集样例：[wan-kf2v-valid-dataset.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260119/gjlxnm/wan-kf2v-valid-dataset.zip)。
    
-   zip包目录结构：
    
    ```
    wan-kf2v-valid-dataset.zip
    ├── data.jsonl                 # 必须固定命名为data.jsonl，最大支持 20MB
    └── image/                     # 存放首帧和尾帧图像
        ├── image_1_first.jpg      # 图像最大分辨率为4096*4096，支持BMP、JPEG、PNG、WEBP格式
        └── image_1_last.jpg
    ```
    
-   标注文件（data.jsonl）：每一行代表一条验证数据，必须为JSON 对象。一行验证数据的结构如下：
    
    ```
    {
        "prompt": "视频开头展示了一位年轻男性站在城市景观前的场景。他穿着黑白格子外套，内搭黑色连帽衫，面带微笑，神情自信。背景是夕阳下的城市天际线，远处可以看到著名的圆顶建筑和错落有致的屋顶，天空中云层密布，呈现出温暖的橙黄色调。然后开始展示s86b5p金钱雨特效，无数巨大尺寸的美元钞票（米黄底/深绿图案）如暴雨般倾泻而下，密集地砸向并环绕他。钞票持续落下，同时镜头缓缓拉进，他双臂舒展上扬，脖颈微仰，表情惊喜，完全沉浸在这场狂野的金钱雨中。",
        "first_frame_path": "image/image_1_first.jpg",
        "last_frame_path": "image/image_1_last.jpg",
    }
    ```
    

## 文本生成评测集

是一种单轮对话的评测数据，用于文本生成类模型的评测。

文本生成 Excel 格式评测数据，**一行评测数据展开后结构如下**：

**Prompt**

**Completion**

<用户输入1>

<模型期望输出1>

在[模型评测](https://help.aliyun.com/zh/model-studio/model-evaluation-overview)中，参评的大模型将基于您的评测集中每一条Prompt进行推理。随后您的评分员或自动化评分系统将参考评测集中的Completion数据来对大模型的推理结果进行评分。

[文本生成评测集格式示例.xlsx](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241113/wvniky/%E6%96%87%E6%9C%AC%E7%94%9F%E6%88%90%E8%AF%84%E6%B5%8B%E9%9B%86%E7%A4%BA%E4%BE%8B.xlsx)

## 数据集构建技巧

## 文本生成与多模态理解

### 训练集的规模要求

对于CPT来说，数据集最少需要**一千万Token优质预训练数据**；对于 SFT 来说，训练集最少需要**上千条优质微调数据**；对于 DPO 来说，训练集一般需要**上百条人类偏好数据**。如果模型调优后的模型评测结果不佳，最简单的改进方法是收集更多数据进行训练。

如果您缺乏数据，建议构建[智能体应用](https://help.aliyun.com/zh/model-studio/single-agent-application)，使用知识库索引来增强模型能力。当然在很多复杂的业务场景，可以综合采用模型调优和知识库检索结合的技术方案。

以客服场景为例，可以借助模型调优解决客服回答的语气、表达习惯、自我认知等问题，场景涉及的专业知识可以结合知识库，动态引入到模型上下文中。

阿里云百炼推荐您可以先构建 RAG 应用试运行，在收集到足够的应用数据后再通过模型调优继续提升模型表现。

您可以采用以下策略扩充训练集：

> 您可以在准备训练集的同时，准备一份与训练集数据不重叠的评测集，用来评测调优后模型的效果。

1.  让大模型模拟生成特定业务/场景的相关内容，辅助您生成更多用于调优数据。（生成模型建议选取表现优异、规模更大的模型）
    
2.  使用阿里云百炼的[数据处理](https://bailian.console.aliyun.com/?tab=model#/efm/model_data)功能，对您的数据集进行数据清洗、数据增强。
    
3.  通过应用场景收集、网络爬虫、社交媒体和在线论坛、公开数据集、合作伙伴与行业资源、用户贡献等各种方式，人工获取更多数据。
    

### 训练数据的多样性与均衡性

模型调优有不同场景，针对具体业务场景时，专业性更重要；而针对问答场景时通用性更重要。您需要根据模型负责的业务模块或使用场景进行数据用例设计。因此训练效果好坏并不是仅取决于数据量，更需要考虑针对场景的专业性和多样性。

这里以智能 AI 对话场景为例，介绍一个专业、多样的训练集应该包含的各种业务场景：

**具体业务**

**多样化场景/业务**

电商客服

活动推送、售前咨询、售中引导、售后服务、售后回访、投诉处理等。

金融服务

贷款咨询、投资理财顾问、信用卡服务、银行账户管理等。

在线医疗

病症咨询、挂号预约、就诊须知、药品信息查询、健康小建议等。

AI 秘书

IT 信息、行政信息、HR 信息、员工福利解答、公司日历查询等。

旅游出行助手

旅行规划、出入境指南、旅行保险咨询、目的地风土人情介绍等。

企业法律顾问

合同审核、知识产权保护、合规性检查、劳动法律答疑、跨境交易咨询、个案法律分析等。

还请特别注意的是各个场景/业务的数据数量应**相对均衡，数据比例符合实际场景比例**，避免某一类数据过多导致模型偏向于学习该类特征，影响模型的泛化能力。

## 图生视频

### **1\. 确定微调场景**

万相支持**图生视频**的微调场景包括：

-   **固定视频特效**：让模型学会某种特定的视觉变化，如旋转木马、魔法换装等。
    
-   **固定人物动作**：提升模型对特定肢体动作的复现度，如特定的舞蹈动作、武术招式。
    
-   **固定视频运镜**：复刻复杂的镜头语言，如推拉摇移、环绕拍摄等固定模板。
    

### **2\. 获取原始素材**

-   AI 生成筛选：利用“万相”基础模型批量生成视频，再人工挑选出最符合目标效果的优质样本。这是最常用的方法。
    
-   真实拍摄：如果您的目标是追求高真实感的互动场景（如拥抱、握手等），使用实拍素材是最佳选择。
    
-   三维软件渲染：对于需要控制细节的特效或抽象动画，建议使用 3D 软件（如 Blender、C4D）制作素材。
    

### **3\. 清洗数据**

**维度**

**正面要求**

**负面案例**

**一致性**

**核心特征必须高度统一**。

例如：训练“360度旋转”，所有视频必须都是顺时针旋转，且旋转速度基本一致。

**方向混杂**。

数据集中既有顺时针，又有逆时针。模型不知道该学哪个方向。

**多样性**

**主体与场景越丰富越好**。

覆盖不同主体（男女老少、猫狗建筑）和不同构图（远近景、俯仰拍）。同时，分辨率和长宽比应尽可能多样化。

**单一场景或主体**。

所有视频都是“穿红衣的人在白墙前旋转”。模型会误以为“红衣”和“白墙”是特效的一部分，换了衣服就不会转了。

**均衡性**

**各类型数据比例均衡**。

如果包含多种风格，数量应大致相等。

**比例严重失调**。

90%是人像视频，10%是风景视频。模型可能在生成风景视频时效果不佳。

**纯净度**

**画面干净清晰**。

使用无干扰的原始素材。

**有干扰元素**。

视频中带有字幕、台标、水印、明显的黑边或噪点。模型可能会把水印当成特效学进去_。_

**时长**

**素材时长 ≤ 目标时长**。

若期望生成5秒视频，素材最好裁剪为4-5秒。

**素材过长**。

期望生成5秒，却喂给模型8秒的素材，会导致动作学习不完整，产生截断感。

## 创建数据集

本段落指导您如何在阿里云百炼控制台上创建一个数据集。

> 阿里云百炼目前对数据集的创建数量没有限制，导入的数据量也没有上限。

1.  访问**[数据集](https://bailian.console.aliyun.com/#/efm/model_data)**列表，单击**新增数据集**。
    
2.  输入**数据集名称**，并选择需要创建的**数据集类型**。
    
    ## 训练集
    
    1.  **数据格式**，根据您的训练需求，选择**训练场景**和**训练方式**。可选的训练方式取决于训练场景，请以控制台实际显示为准。
        
    2.  **存储位置**，选择**平台OSS存储**。
        
        > 使用阿里云百炼提供的免费存储空间。目前阿里云百炼对导入的数据量没有设置上限。
        
    3.  **导入方式**，选择**本地上传**或**从OSS导入**。
        
        > 为保障数据安全，平台会为您导入的数据集开启OSS服务端加密，使用OSS完全托管密钥进行加解密（SSE-OSS），加密算法为AES256。
        
        > 选择**从OSS导入**时，需要先为目标Bucket添加标签`bailian-datahub-access`\=`read`，然后在控制台选择对应的Bucket和文件。仅支持选择符合当前数据格式要求的文件类型。
        
    4.  **上传文件**，单击![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2312799171/p816622.png)图标选择并上传文件。您上传的训练数据必须与给出的数据示例结构一致，否则会导致导入失败。
        
        > 您可以参考阿里云百炼提供的数据模板，将示例数据替换为您的训练数据，然后直接上传。
        
        > 阿里云百炼不支持创建空训练集。
        
        > system/user/assistant 区别请参见[概述](https://help.aliyun.com/zh/model-studio/text-generation#51574d7e93su4)。
        
        > **SFT-文本生成**和**DPO-文本生成**训练集支持同时上传多个文件。阿里云百炼会整合并统一导入训练集。
        
    5.  **发布配置**，选择**立即发布**或**保存为草稿**。选择**保存为草稿**仅创建数据集，状态为**草稿**；选择**立即发布**则会创建并发布数据集。
        
        > **CPT-文本生成**和**图生视频**类型的训练集不支持**草稿**状态，只能立即发布。
        
        **发布状态**
        
        **说明**
        
        **草稿**
        
        数据集**支持在线编辑**，可用于[数据清洗或增强](https://help.aliyun.com/zh/model-studio/data-processing)（例如进行数据清洗和数据增强），但无法用于模型调优和模型评测（模型调优或评测前需[发布数据集](#7f73aeb29dt97)）。
        
        **发布**
        
        数据集**不支持在线编辑**，可用于[数据清洗或增强](https://help.aliyun.com/zh/model-studio/data-processing)、[模型调优](https://help.aliyun.com/zh/model-studio/model-training-overview)（训练集）和[模型评测](https://help.aliyun.com/zh/model-studio/model-evaluation-overview)（评测集）。
        
    
    ## 评测集
    
    1.  **数据集类型**选择**文本生成**（暂不支持其它）。
        
    2.  **存储位置**，选择**平台存储**（暂不支持其它）。
        
        > 使用百炼提供的免费存储空间。目前百炼对导入的数据量没有设置上限。
        
    3.  **导入方式**，选择**本地上传**（评测集暂不支持从OSS导入）。
        
    4.  **上传文件**，单击![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2312799171/p816622.png)图标选择并上传文件。您上传的评测数据必须与给出的数据示例结构一致，否则会导致导入失败。
        
        > 您可以参考阿里云百炼提供的数据模板，将示例数据替换为您的评测数据，然后直接上传。
        
        > 百炼不支持创建空评测集。
        
        > 您可以同时上传多个文件。百炼会先整合这些文件中的数据，然后统一导入评测集。
        
    
3.  单击**确认**，新创建的数据集（版本V1）将出现在**[数据集](https://bailian.console.aliyun.com/#/efm/model_data)**[列表](https://bailian.console.aliyun.com/#/efm/model_data)中，并开始导入数据。单击![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0659913271/p833282.png)图标，查看最新**导入状态**。
    
    **导入状态**
    
    **说明**
    
    **导入中**
    
    在请求高峰时段，该过程可能需要较长时间，请耐心等待，期间无需您介入操作。
    
    **导入成功**
    
    表示数据集已成功创建。
    
    **导入失败**
    
    表示数据集创建失败。
    

## 管理数据集

**操作**

**说明**

**管理数据集版本**

您可以为数据集创建多个独立编辑的版本。在**[数据集列表](https://bailian.console.aliyun.com/#/efm/model_data)**页面，单击数据集的名称，左侧**数据版本**导航树会显示当前数据集的所有版本。

-   **新增版本**：单击**新增版本**，数据集**版本号**自动递增。
    
    1.  **数据继承**，选择**继承数据**或**新建数据**。
        
        > **继承数据**：新版本将保留继承版本的所有数据，**数据集类型**保持不变，方便您在继承版本的基础上进行修改。请注意，**CPT-文本生成**训练集不支持该模式。
        
        > **新建数据**：新版本内容为空，**数据集类型**保持不变，方便您重新导入数据。
        
    2.  单击**确定**，左侧**数据版本**导航树中出现新版本。
        

-   **删除版本**：在左侧**数据版本**导航树中选择相应版本，然后单击页面右上角的**删除**。
    
    > 版本删除后将不再可用且不可恢复，请谨慎操作。
    

**查看数据集**

在**[数据集列表](https://bailian.console.aliyun.com/#/efm/model_data)**页面，单击数据集的名称，可查看该数据集的基本信息（例如数据集类型、数据集创建时间等）、所有版本和数据。

**查找数据集**

在**[数据集列表](https://bailian.console.aliyun.com/#/efm/model_data)**页面的搜索框中输入数据集名称后，单击![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7506671371/p870527.png)图标在业务空间下查找数据集，支持模糊搜索，支持按**数据集类型**筛选结果。

**编辑数据集**

数据集不支持编辑，如需调整，请新增**数据版本**。

**导出数据集**

在**[数据集列表](https://bailian.console.aliyun.com/#/efm/model_data)**页面，单击数据集名称右侧的**导出**，可下载该数据集的最新版本到本地。暂不支持设置导出文件格式。

> 如需导出数据集的指定版本，请先**查看**该数据集，然后在左侧**数据版本**导航树中选择相应版本，再单击页面右上角的**导出**。

> 阿里云百炼不支持导出空数据集。

-   **训练集**：**SFT-文本生成**（导出为jsonl格式）、**SFT-图片理解**（导出为zip格式）、**DPO-文本生成**（导出为jsonl格式）以及**CPT-文本生成**（导出为jsonl格式）。
    
-   **评测集**：**文本生成**（导出为xlsx格式）。
    

**发布数据集**

在**[数据集列表](https://bailian.console.aliyun.com/#/efm/model_data)**页面，单击数据集名称右侧的**发布**（当数据集最新版本的**发布状态**为**草稿**可用），可发布该数据集的最新版本。发布后，该版本可用于模型调优或模型评测。

> 如需发布数据集的指定版本，请先**查看**该数据集，然后在左侧**数据版本**导航树中选择相应版本，再单击页面右上角的**发布**。

> 数据集发布后将无法再转为**草稿**状态进行编辑。如需编辑，请为该数据集新增一个版本。

> 阿里云百炼不支持发布空数据集。

**删除数据集**

如果您不再需要某个数据集，请在**[数据集列表](https://bailian.console.aliyun.com/#/efm/model_data)**页面单击该数据集右侧的**删除**，以彻底删除此数据集。删除数据集后，该数据集将不再可用且不可恢复，请谨慎操作。

> 如需删除数据集的指定版本，请先**查看**该数据集，然后在左侧**数据版本**导航树中选择相应版本，再单击页面右上角的**删除**。

## **计费说明**

模型数据功能和数据集存储均免费。

## **API参考**

阿里云百炼模型数据目前尚未提供可用的API。

## **下一步**

-   **训练集**发布后，可用于[模型调优](https://help.aliyun.com/zh/model-studio/model-training-overview)。
    
-   **评测集**发布后，可用于[模型评测](https://help.aliyun.com/zh/model-studio/model-evaluation-overview)。
