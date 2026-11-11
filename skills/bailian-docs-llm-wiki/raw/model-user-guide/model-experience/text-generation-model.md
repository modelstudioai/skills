# 文本生成与视觉理解

千问 Plus、Max、Flash 支持文本、图像和视频输入，并以文本回答。你可以用同一个模型生成内容、理解图片或分析视频，无需仅因输入包含图片或视频就改选 VL 模型。

## 选择模型

Plus、Max、Flash 均可接收文本、图像和视频，并以文本回答。文本生成用于根据输入生成或处理文字；图像与视频理解用于理解画面内容并回答问题，也可以结合文字指令完成任务。

-   **效果优先**：`qwen4-max-preview`（[仅 Token Plan](https://help.aliyun.com/zh/model-studio/token-plan-personal-overview)），适合对推理和理解能力要求更高的任务。
-   **均衡之选**：`qwen3.7-plus`，兼顾能力与成本。
-   **成本优先**：`qwen3.8-flash`，使用前确认效果满足需求。

如偏好第三方模型，长程编程可选 [kimi-k3](raw/model-user-guide/get-started-with-models/model-studio-model-list/model-list-text-generation/kimi-k3.md)，编程与智能体任务可选 [glm-5.3](raw/model-user-guide/get-started-with-models/model-studio-model-list/model-list-text-generation/glm-5-3.md)。具体输入模态、功能和地域可用性，请查看对应模型文档。

调用方式参见[文本生成](raw/model-user-guide/model-experience/text-generation-model/text-generation.md)和[图像与视频理解](raw/model-user-guide/model-experience/text-generation-model/vision.md)。

**深度思考**：通过逐步推理处理需要多步分析的问题，让模型在给出答案前进行更充分的思考。可根据任务需要调整思考模式，参见[深度思考](raw/model-user-guide/model-experience/text-generation-model/deep-thinking.md)。

**工具调用**：模型可以结合输入内容调用工具：Function Calling 用于对接你定义的函数或业务接口；内置工具提供联网搜索、代码解释器、网页抓取等能力，帮助获取外部信息或处理数据。参见[工具调用](raw/model-user-guide/model-experience/text-generation-model/tool-calls.md)。

**结构化输出**：将文本、图像或视频中的信息整理为有效的 JSON，便于程序读取、校验和后续处理。参见[结构化输出](raw/model-user-guide/model-experience/text-generation-model/qwen-structured-output.md)。

**批量推理**：如果需要处理大量请求，且不要求即时返回结果，可以使用批量推理降低请求成本。参见[批量推理](raw/model-user-guide/model-high-speed-inference/batch-inference.md)。

## 领域模型

针对特定任务，也可以选择专门优化的模型。

-   [翻译](raw/model-user-guide/model-experience/text-generation-model/specialized-models/machine-translation.md)：Qwen-MT 面向多语言文本翻译。
-   [长文档](raw/model-user-guide/model-experience/text-generation-model/specialized-models/long-context-qwen-long.md)：Qwen-Long 通过文件上传和引用处理超长文档。
-   [角色扮演](raw/model-user-guide/model-experience/text-generation-model/specialized-models/role-play.md)：Qwen-Character 面向需要保持人设的拟人化对话。
-   [数据挖掘](raw/model-user-guide/model-experience/text-generation-model/specialized-models/data-mining-qwen-doc.md)：Qwen-Doc 面向文档信息抽取、分类打标和摘要生成。
-   [深入研究](raw/model-user-guide/model-experience/text-generation-model/specialized-models/qwen-deep-research.md)：Qwen-Deep-Research 规划研究步骤，结合多轮联网搜索生成研究报告。
-   [对话分析](raw/model-user-guide/model-experience/text-generation-model/specialized-models/dialogue-analysis.md)：通义晓蜜面向对话信息抽取、分类和满意度分析。
-   [界面交互](raw/model-user-guide/model-experience/text-generation-model/specialized-models/gui-automation.md)：根据界面截图和指令完成交互操作。
-   [文字提取](raw/model-user-guide/model-experience/text-generation-model/specialized-models/qwen-vl-ocr.md)：Qwen-OCR 从文档、表格或手写内容的图片中提取文字。

各领域模型的地域和调用方式可能不同，请以对应文档为准。

## 推荐模型

### 功能支持

**模型ID**

**上下文**

**思考模式**

**Function Calling**

**内置工具**

**结构化输出**

`qwen4-max-preview`

1M

支持

支持

支持

支持

`qwen3.8-max`

1M

支持

支持

支持

支持

`qwen3.8-flash`

1M

支持

支持

支持

支持

`qwen3.7-plus`

1M

支持

支持

支持

支持

`deepseek-v4.1-flash-1017`

1M

支持

支持

支持

支持

`glm-5.3`

1M

支持

支持

不支持

支持

`kimi-k3.1-pro`

1M

支持

支持

支持（Responses）

支持（JSON Mode）

`kimi-k3`

1M

支持

支持

不支持

支持

`MiniMax-M3.1-Flash`

1M

支持

支持

不支持

不支持

`mimo-v2.6-pro-ultraspeed`

1M

支持

支持

不支持

支持

`step-5-preview`

1M

支持

支持

不支持

支持

### 图像与视频参数

**模型 ID（Model ID）**

**上下文**

最大输出

**最大像素/图**

**最大视频时长**

**最大视频大小**

**最大图片数**

**最大视频数**

**Function Calling**

**内置工具**

**结构化输出**

`qwen4-max-preview`

1M

393,216（思考+输出）

16M

2小时

2GB

2048

64

支持

支持

支持

`qwen3.8-max`

1M

128k

16M

2小时

2GB

2048

64

支持

支持

支持

`qwen3.8-flash`

1M

128k

16M

2小时

2GB

2048

64

支持

支持

支持

`qwen3.7-plus`

1M

128k

16M

2小时

2GB

2048

64

支持

支持

支持

## 旧版模型

以下模型不再作为首选推荐。同一型号仅列正式版本，不重复列出预览名称和快照。

查看旧版模型

### Qwen3.7

#### 功能支持

**模型ID**

**上下文**

**思考模式**

**Function Calling**

**内置工具**

**结构化输出**

`qwen3.7-max`

1M

支持

支持

支持

支持

`qwen3.7-flash`

1M

支持

支持

支持

支持

#### 图像与视频参数

**模型 ID（Model ID）**

**上下文**

**最大像素/图**

**最大视频时长**

**最大视频大小**

**最大图片数**

**最大视频数**

**Function Calling**

**内置工具**

**结构化输出**

`qwen3.7-flash`

1M

16M

2小时

2GB

256

64

支持

支持

支持

#### 图像与视频参数

**模型 ID（Model ID）**

**输入**

**输出**

**上下文**

**最大输出**

**最大图片数**

**最大视频数**

**Function Calling**

**内置工具**

**结构化输出**

`qwen3.7-flash`

文本、图像、视频

文本

1M

64k

256

64

支持

支持

支持

### Qwen3.6

#### 图像与视频参数

**模型 ID（Model ID）**

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

#### 功能支持

**模型ID**

**上下文**

**思考模式**

**Function Calling**

**内置工具**

**结构化输出**

`qwen3.6-plus`

1M

支持

支持

支持

支持

`qwen3.6-flash`

1M

支持

支持

支持

支持

### Qwen3.5

#### 图像与视频参数

#### 功能支持

**模型ID**

**上下文**

**思考模式**

**Function Calling**

**内置工具**

**结构化输出**

`qwen3.5-plus`

1M

支持

支持

支持

支持

`qwen3.5-flash`

1M

支持

支持

支持

支持

`qwen3.5-397b-a17b`

256k

支持

支持

支持

支持

`qwen3.5-122b-a10b`

256k

支持

支持

支持

支持

`qwen3.5-27b`

256k

支持

支持

支持

支持

`qwen3.5-35b-a3b`

256k

支持

支持

支持

支持

#### 图像与视频参数

**模型 ID（Model ID）**

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

### Qwen3-Coder

#### 功能支持

**模型ID**

**上下文**

**思考模式**

**Function Calling**

**内置工具**

**结构化输出**

`qwen3-coder-flash`

1M

支持

支持

不支持

支持

### Qwen-MT

#### 功能支持

**模型ID**

**上下文**

**思考模式**

**Function Calling**

**内置工具**

**结构化输出**

`qwen-mt-plus`

16k

不支持

不支持

不支持

不支持

`qwen-mt-flash`

16k

不支持

不支持

不支持

不支持

`qwen-mt-lite`

16k

不支持

不支持

不支持

不支持

### Qwen-Long

#### 功能支持

**模型ID**

**上下文**

**思考模式**

**Function Calling**

**内置工具**

**结构化输出**

`qwen-long`

10M

不支持

不支持

不支持

不支持

### Qwen-Character

#### 功能支持

**模型ID**

**上下文**

**思考模式**

**Function Calling**

**内置工具**

**结构化输出**

`qwen-plus-character`

32k

不支持

不支持

不支持

不支持

`qwen-plus-character-ja`

32k

不支持

不支持

不支持

不支持

`qwen-flash-character`

8k

不支持

不支持

不支持

不支持

### Qwen

#### 功能支持

**模型ID**

**上下文**

**思考模式**

**Function Calling**

**内置工具**

**结构化输出**

`qwen-plus`及其快照版本

1M

支持

支持

支持

支持

`qwen-max`

32k

不支持

支持

支持

支持

`qwen-flash`及其快照版本

1M

支持

支持

支持

支持

### DeepSeek

#### 功能支持

**模型ID**

**上下文**

**思考模式**

**Function Calling**

**内置工具**

**结构化输出**

`deepseek-r1-distill-llama-70b`

128k

支持

不支持

不支持

不支持

`deepseek-r1-distill-qwen-1.5b`

128k

支持

不支持

不支持

不支持

### Qwen3-VL

-   `qwen3-vl-plus`
