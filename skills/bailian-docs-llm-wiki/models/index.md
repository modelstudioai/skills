# 百炼模型市场索引

> 自动生成 · 共 160 个模型家族 · 355 个主干模型 · 更新于 2026-05-27

**机器查询走结构化文件**：

- `index.json` — 全局摘要（统计 + 能力/厂商分布 + 轻量家族列表），适合 dashboard 或 LLM 快速定位
- `families.jsonl` — 每行一个家族（含轻量 `items[]` 摘要），适合按家族筛选
- `models.jsonl` — 每行一个主干模型（含价格/QPM/features），适合跨家族批量查询
- `groups/<slug>.json` — 单家族完整明细（含调用代码、入参 schema）

join：`models.jsonl[].family == families.jsonl[].slug == index.json.families[].slug`。

## 文本生成 `TG` — 30 个家族

- [通义法睿-Plus-32K](groups/farui-plus.json) — 通义法睿是以通义千问为基座经法律行业数据和知识专门训练的法律行业大模型产品，综合运用了模型精调、强化学习、 RAG检索增强、法律Agent技术，具有回答法律问题、推理法律适用、推荐裁判类案、辅助案情分…
  - 模型：`farui-plus`
- [通义晓蜜-对话分析-flash](groups/tongyi-xiaomi-analysis-flash.json) — 通义晓蜜-对话分析-flash是专注于日常任务，如对话信息抽取、场景分类等分析类需求的模型，自定义分析标准遵循与对话语义理解能力显著提升，适用于低时延的离线在线分析任务。
  - 模型：`tongyi-xiaomi-analysis-flash`
- [通义晓蜜-对话分析-pro](groups/tongyi-xiaomi-analysis-pro.json) — 通义晓蜜-对话分析-pro是专注于高阶复杂分析，如针对具备复杂业务逻辑的复杂质检规则等分析需求的模型，支持自定义更细粒度的分析标准，具备更强的多轮上下文建模、深层语义理解与推理能力。
  - 模型：`tongyi-xiaomi-analysis-pro`
- [意图分类模型](groups/tongyi-intent-detect-v3.json) — 意图识别和槽位填充是对话系统中的基础任务。本模型实现了一个基于 API的意图（intent）和槽位参数（slots）联合预测。在一次模型输出中，同时完成多个指令API的返回和槽位参数的填充。返回的结果…
  - 模型：`tongyi-intent-detect-v3`
- [智谱GLM系列文本模型](groups/zhipu-models-market-place.json) — 由智谱提供的GLM系列文本模型API服务
  - 模型：`ZHIPU/GLM-5`, `ZHIPU/GLM-5.1`
- [GLM](groups/glm-4.5.json) — GLM是由智谱提供的开源模型。
  - 模型：`glm-4.5`, `glm-4.5-air`, `glm-4.6`, `glm-4.7`, `glm-5`, `glm-5.1`
- [Kimi](groups/kimi-models-market-place.json) — 由月之暗面提供的Kimi系列模型的API服务。
  - 模型：`kimi/kimi-k2.5`, `kimi/kimi-k2.6`
- [MiMo文本模型](groups/xiaomi-models-market-place.json) — 由小米MiMo提供的MiMo文本模型API服务
  - 模型：`xiaomi/mimo-v2.5-pro`
- [MiniMax文本模型](groups/minimax-models-market-place.json) — 由MiniMax提供的MiniMax-M系列文本模型API服务。
  - 模型：`MiniMax/MiniMax-M2.1`, `MiniMax/MiniMax-M2.5`, `MiniMax/MiniMax-M2.7`
- [Qwen-Coder-Plus](groups/qwen-coder-plus.json) — 千问系列代码及编程模型是专门用于编程和代码生成的语言模型，性能出色，效果突出。
  - 模型：`qwen-coder-plus`
- [Qwen-Coder-Turbo](groups/qwen-coder-turbo.json) — Qwen-Coder-Turbo模型是专门用于编程和代码生成的语言模型，推理速度快，成本低。
  - 模型：`qwen-coder-turbo`
- [qwen-deep-research](groups/qwen-deep-research.json) — 千问深入研究是一款面向复杂研究任务的高级智能体系统，具备多轮推理与全局规划能力，能够运用互联网搜索等多种工具，对任务进行精细化拆解，开展推理与分析，最终为用户生成可溯源、逻辑严谨的研究型报告。
  - 模型：`qwen-deep-research`
- [Qwen-Doc-Turbo](groups/qwen-doc-turbo.json) — 快速对文档进行精准信息抽取，打标分类，内容审核及摘要总结。
  - 模型：`qwen-doc-turbo`
- [Qwen-Flash-Character](groups/qwen-flash-character.json) — 千问系列多语言角色扮演模型，本模型是动态更新版本，模型更新会提前通知，适合拟人化的角色扮演，同时优化了限定人设指令遵循、话题推进、倾听共情等能力，支持个性化角色的深度还原。
  - 模型：`qwen-flash-character`
- [Qwen-Long](groups/qwen-long.json) — Qwen-Long是在通义实验室针对超长上下文处理场景的大语言模型，支持中文、英文等不同语言输入，支持最长1000万tokens(约1500万字或1.5万页文档)的超长上下文对话。配合同步上线的文档服…
  - 模型：`qwen-long`, `qwen-long-latest`
- [Qwen-Math-Plus](groups/qwen-math-plus.json) — Qwen-Math-Plus模型具有强大的数学解题能力,擅长处理中英文数学题，包括方程、计算、证明等方向。
  - 模型：`qwen-math-plus`, `qwen-math-plus-0816`, `qwen-math-plus-0919`, `qwen-math-plus-latest`
- [Qwen-Math-Turbo](groups/qwen-math-turbo.json) — Qwen-Math-Turbo模型是专门用于数学解题的语言模型，推理速度快，成本低。
  - 模型：`qwen-math-turbo`
- [Qwen-Max](groups/qwen-max.json) — 千问2.5系列千亿级别超大规模语言模型，支持中文、英文等不同语言输入。随着模型的升级，qwen-max将滚动更新升级。如果希望使用固定版本，请使用历史快照版本。
  - 模型：`qwen-max`
- [Qwen-MT-Flash](groups/qwen-mt-flash.json) — 基于Qwen3全面升级的轻量级文本翻译大模型，支持92个语种互译，模型性能和翻译效果全面升级，并提供更稳定的术语定制、格式还原度、领域提示能力，让译文更精准、自然。
  - 模型：`qwen-mt-flash`
- [Qwen-MT-Lite](groups/qwen-mt-lite.json) — 基于Qwen3全面升级的基础级文本翻译大模型，支持32个语种互译，模型性能和翻译效果全面升级，并提供更稳定的术语定制、格式还原度、领域提示能力，让译文更精准、自然。
  - 模型：`qwen-mt-lite`
- [Qwen-MT-Plus](groups/qwen-mt-plus.json) — 基于Qwen3全面升级的旗舰级翻译大模型，支持92个语种互译，模型性能和翻译效果全面升级，并提供更稳定的术语定制、格式还原度、领域提示能力，让译文更精准、自然。
  - 模型：`qwen-mt-plus`
- [Qwen-MT-Turbo](groups/qwen-mt-turbo.json) — 基于Qwen3全面升级的轻量级文本翻译大模型，支持92个语种互译，模型性能和翻译效果全面升级，提供更稳定的术语定制、格式还原度、领域提示能力，让译文更精准、自然。
  - 模型：`qwen-mt-turbo`
- [Qwen-Plus-Character](groups/qwen-plus-character.json) — 千问系列角色扮演模型，本模型是动态更新版本，模型更新会提前通知，适合拟人化的角色扮演，同时优化了限定人设指令遵循、话题推进、倾听共情等能力，支持个性化角色的深度还原。
  - 模型：`qwen-plus-character`
- [Qwen3-Coder-30B-A3B-Instruct](groups/qwen3-coder-30b-a3b-instruct.json) — 基于Qwen3的代码生成模型，继承Qwen3-Coder-480B-A35B-Instruct的coding agent能力，代码能力达到同尺寸规模模型SOTA。
  - 模型：`qwen3-coder-30b-a3b-instruct`
- [Qwen3-Coder-480B-A35B-Instruct](groups/qwen3-coder-480b-a35b-instruct.json) — 基于Qwen3的代码生成模型，具有强大的Coding Agent能力，代码能力达到开源模型 SOTA。
  - 模型：`qwen3-coder-480b-a35b-instruct`
- [Qwen3-Coder-Flash](groups/qwen3-coder-flash.json) — 基于Qwen3的代码生成模型，继承Qwen3-Coder-Plus的coding agent能力，支持多轮工具交互，重点优化仓库级别理解能力并增加工具调用稳定性。
  - 模型：`qwen3-coder-flash`
- [Qwen3-Coder-Plus](groups/qwen3-coder-plus.json) — 基于Qwen3的代码生成模型，具有强大的Coding Agent能力，擅长工具调用和环境交互，能够实现自主编程、代码能力卓越的同时兼具通用能力。
  - 模型：`qwen3-coder-plus`
- [Qwen3-Max](groups/qwen3-max.json) — 千问3系列Max模型，相较preview版本在智能体编程与工具调用方向进行了专项升级。本次发布的正式版模型达到领域SOTA水平，适配场景更加复杂的智能体需求。
  - 模型：`qwen3-max`, `qwen3-max-preview`
- [Qwen3.5-Plus](groups/qwen3.5-plus.json) — Qwen3.5原生视觉语言系列Plus模型，展现出与当前顶尖前沿模型相媲美的卓越性能，模型效果在纯文本与多模态方面相较3系列均实现飞跃式进步。
  - 模型：`qwen3.5-plus`
- [SiliconFlow DeepSeek](groups/siliconflow-models.json) — 由硅基流动提供的DeepSeek系列模型API服务。
  - 模型：`siliconflow/deepseek-r1-0528`, `siliconflow/deepseek-v3-0324`, `siliconflow/deepseek-v3.1-terminus`, `siliconflow/deepseek-v3.2`

## 图像生成 `IG` — 29 个家族

- [创意海报生成](groups/wanx-poster-generation-v1.json) — 创意海报生成，您的创意海报魔法工厂！它能够根据你的要求自动生成海报的背景和文字排版，支持多种海报风格，从宣传到祝福，让每一张海报都成为你的个性宣言。无需设计基础，轻松制作出彩作品，让创意触手可及。
  - 模型：`wanx-poster-generation-v1`
- [人物实例分割](groups/image-instance-segmentation.json) — 人物实例分割运用了检测和分割技术，不仅能够在图像中识别出不同的对象，而且还能准确地画出每一个对象边界的像素级掩码（mask）。
  - 模型：`image-instance-segmentation`
- [人像风格重绘](groups/wanx-style-repaint-v1.json) — 人像风格重绘可以将输入的人物图像进行多种风格化的重绘生成，使新生成的图像在兼顾原始人物相貌的同时，带来不同风格的绘画效果。
  - 模型：`wanx-style-repaint-v1`
- [图像背景生成](groups/wanx-background-generation-v2.json) — 图像背景生成可以基于输入的前景图像素材拓展生成背景信息，实现自然的光影融合效果，与细腻的写实画面生成。支持文本描述、图像引导等多种方式，同时支持对生成的图像智能添加文字内容。
  - 模型：`wanx-background-generation-v2`
- [图像擦除补全](groups/image-erase-completion.json) — 图像擦除补全通过指定图像mask中要删除的人体、宠物、物品、文字、水印等图像区域，在保留背景的同时移除图像中的一个或多个人物、物体、文字等元素，此功能不支持输入prompt的消除。擦除补全技术结合了计…
  - 模型：`image-erase-completion`
- [图像画面扩展](groups/image-out-painting.json) — 图像画面大模型，对输入图像进行画面自由扩展，支持旋转画面，支持按照扩展系数和扩展像素数两种方式进行扩图。用户可以通过指定宽度、高度画面扩展比例或者左、右、上、下的扩展的像素值来控制画面扩展，可用于创意…
  - 模型：`image-out-painting`
- [万相-图像局部重绘](groups/wanx-x-painting.json) — 万相-图像局部重绘是基于自研的Composer组合生成框架的AI绘画创作大模型后置处理链路，能够根据用户输入的原始图片和意涂抹图中局部区域和prompt提示词文字内容，生成符合语义描述的多样化风格的局…
  - 模型：`wanx-x-painting`
- [万相-涂鸦作画](groups/wanx-sketch-to-image-lite.json) — 万相-涂鸦作画通过手绘任意内容加文字描述，即可生成精美的涂鸦绘画作品，作品中的内容在参考手绘线条的同时，兼顾创意性和趣味性。涂鸦作画支持扁平插画、油画、二次元、3D卡通和水彩5种风格，可用于创意娱乐、…
  - 模型：`wanx-sketch-to-image-lite`
- [鞋靴模特](groups/shoemodel-v1.json) — 鞋靴模特支持输入多视角鞋靴系列图片，同时对输入模特模板图的鞋子区域进行鞋靴AI试穿，实现模特鞋靴布局重绘生成，最终生成图片的效果, 布局自然、细节丰富、画面细腻、试穿结果逼真。可用于模特商品图设计、新…
  - 模型：`shoemodel-v1`
- [虚拟模特](groups/wanx-virtualmodel.json) — 虚拟模特可以对上传的真人或者人台实拍商品展示图进行智能生成，将其中的模特和背景替换为心仪的内容，在保持人物姿态不变的情况下，使用虚拟模特对商品进行更加精美、多样的展示。支持各种与模特产生互动的商品，如…
  - 模型：`wanx-virtualmodel`
- [虚拟模特V2](groups/virtualmodel-v2.json) — 虚拟模特可以对上传的真人或者人台实拍商品展示图进行智能生成，将其中的模特和背景替换为心仪的内容，在保持人物姿态不变的情况下，使用虚拟模特对商品进行更加精美、多样的展示。支持各种与模特产生互动的商品，如…
  - 模型：`virtualmodel-v2`
- [AI试衣-基础版](groups/aitryon.json) — aitryon是一款性能出众的虚拟试衣图片生成模型，可基于服饰平拍图片以及人物正面全身照，输出服饰的人物试衣效果图片。aitryon模型可在较短时间内生成试衣图片，适用于对时效性要求较高的场景。
  - 模型：`aitryon`
- [AI试衣-Plus版](groups/aitryon-plus.json) — aitryon-plus是一款效果出众的虚拟试衣图片生成模型，可基于服饰平拍图片以及人物正面全身照，输出服饰的人物试衣效果图片。 相较于aitryon模型，aitryon-plus模型在图片清晰度、服…
  - 模型：`aitryon-plus`
- [AI试衣OutfitAnyone-图片分割](groups/aitryon-parsing-v1.json) — 图片分割模型是AI试衣OutfitAnyone的辅助模型，可对模特图、服饰图进行分割，用于试衣图片的前后处理。
  - 模型：`aitryon-parsing-v1`
- [AI试衣OutfitAnyone-图片精修](groups/aitryon-refiner.json) — 图片精修是对AI试衣生成的效果图进行二次生成，输出还原度更高的精修试衣效果图。
  - 模型：`aitryon-refiner`
- [FaceChain人物图像检测](groups/facechain-facedetect.json) — 对用户上传的人物图像进行检测，判断其中所包含的人脸是否符合facechain微调所需的标准，检测维度包括人脸数量、大小、角度、光照、清晰度等多维度，支持图像组输入，并返回每张图像对应的检测结果。
  - 模型：`facechain-facedetect`
- [FaceChain人物写真生成](groups/facechain-generation.json) — 基于人物形象训练已经得到的形象，可以继续通过人物生成写真模型完成该形象的写真生成，支持多种预设风格，包括证件照、商务写真等。
  - 模型：`facechain-generation`
- [Qwen-Image-2.0](groups/qwen-image-2.0.json) — Qwen-Image-2.0系列加速版模型，实现了图片生成和图片编辑的融合；具备更专业的文字渲染1k token指令支持能力、更细腻的真实质感，细腻刻画写实场景、更强的语义遵循能力。加速版有效实现了模…
  - 模型：`qwen-image-2.0`
- [Qwen-Image-2.0-Pro](groups/qwen-image-2.0-pro.json) — Qwen-Image-2.0系列满血版模型，实现了图片生成和图片编辑的融合；具备更专业的文字渲染1k token指令支持能力、更细腻的真实质感，细腻刻画写实场景、更强的语义遵循能力。满血版具备2.0系…
  - 模型：`qwen-image-2.0-pro`
- [Qwen-Image-Edit-Max](groups/qwen-image-edit-max.json) — 千问图像编辑模型Max系列，提供更稳定、更丰富的编辑能力：提升工业设计与几何推理能力；提升角色一致性；减轻偏移问题；集成Lora能力，可以进行更多功能的图像编辑。此版本为2026年1月16日快照。
  - 模型：`qwen-image-edit-max`
- [Qwen-Image-Edit-Plus](groups/qwen-image-edit.json) — 千问系列图像编辑Plus模型，在首版Edit模型基础上进一步优化了推理性能与系统稳定性，大幅缩短图像生成与编辑的响应时间；支持单次请求返回多张图片，显著提升用户体验。
  - 模型：`qwen-image-edit`, `qwen-image-edit-plus`
- [Qwen-Image-Max](groups/qwen-image-max.json) — 千问图像生成模型Max系列，在各类生成任务中表现出色，相较Plus系列大幅度降低生成图片的AI感，提升图像真实性；具备更真实的人物质感、更细腻的自然纹理、更美观的文字渲染。
  - 模型：`qwen-image-max`
- [Qwen-Image-Plus](groups/qwen-image-plus.json) — 千问系列图像生成模型，参数规模200亿。具备卓越的文本渲染能力，在复杂文本渲染、各类生成与编辑任务重表现出色，在多个公开基准测试中获得SOTA，模型性能大幅提升。
  - 模型：`qwen-image`, `qwen-image-plus`
- [Qwen-MT-Image](groups/qwen-mt-image.json) — 专注做图片翻译的模型服务，能将中、英、日等11个语言的图片翻译到指定的语言，精准还原图片排版和内容信息，支持术语定义、敏感词过滤、商品主体检测等自定义功能，提供灵活、准确、高效的图像本地化服务。
  - 模型：`qwen-mt-image`
- [Wan-Image](groups/wan-image-edit.json) — 指令编辑图片内容，轻松实现局部修改、风格变化、一致性保持等
  - 模型：`wan2.5-i2i-preview`, `wan2.6-image`, `wan2.7-image`, `wan2.7-image-pro`, `wanx2.1-imageedit`
- [Wan-T2I](groups/wan-text-to-image.json) — 文字生成图片，写实质感细腻画面，文字内容生成，艺术风格表现
  - 模型：`wan2.2-t2i-flash`, `wan2.2-t2i-plus`, `wan2.5-t2i-preview`, `wan2.6-t2i`, `wanx-v1`, `wanx-v1-0521`, `wanx2.0-t2i-turbo`, `wanx2.1-t2i-plus`, `wanx2.1-t2i-turbo`
- [WordArt锦书-文字变形](groups/wordart-semantic.json) — WordArt锦书-文字变形可以对输入的文字边缘轮廓进行创意变形，根据提示词内容进行边缘变化，实现一种字体的更多种创意用法，返回带有文字内容的黑底白色mask图。
  - 模型：`wordart-semantic`
- [WordArt锦书-文字纹理生成](groups/wordart-texture.json) — WordArt锦书-文字纹理生成可以对输入的文字内容或文字图片进行创意设计，根据提示词内容对文字添加材质和纹理，实现立体凸显或场景融合的效果，生成效果精美、风格多样的艺术字，结合背景可以直接作为文字海…
  - 模型：`wordart-texture`
- [Z-Image-Turbo](groups/z-image-turbo.json) — Z-Image-Turbo是在Artificial Analysis评测中荣登文生图开源模型世界第一的高效图像生成模型,仅用60亿参数和8步推理就能生成媲美大规模商业模型的照片级真实感图像,并在中英双…
  - 模型：`z-image-turbo`

## 视频生成 `VG` — 25 个家族

- [表情包Emoji](groups/emoji-v1.json) — 表情包emoji是一款人脸动效视频生成模型，可基于人脸图片和预设的人脸动态模板，生成人脸动效视频。
  - 模型：`emoji-v1`
- [表情包Emoji-detect](groups/emoji-detect-v1.json) — 表情包Emoji-Detect是辅助表情包Emoji生成的图像检测模型，用于检测图片中的人物形象是否符合视频生成要求。
  - 模型：`emoji-detect-v1`
- [可灵AI](groups/kling-models-market-place.json) — 由可灵AI提供的高质量视频与图像生成及编辑模型。
  - 模型：`kling/kling-v3-image-generation`, `kling/kling-v3-omni-image-generation`, `kling/kling-v3-omni-video-generation`, `kling/kling-v3-video-generation`
- [灵动人像LivePortrait](groups/liveportrait.json) — LivePortrait是一款视频生成模型，可基于人物图片生成轻量化的人物肖像动态视频。
  - 模型：`liveportrait`
- [灵动人像LivePortrait-detect](groups/liveportrait-detect.json) — LivePortrait-detect是辅助LivePortrait的图像检测模型，用于检测图片中的人物形象是否符合视频生成要求。
  - 模型：`liveportrait-detect`
- [声动人像VideoRetalk](groups/videoretalk.json) — VideoRetalk是一个人物视频生成模型，可基于人物视频和人声音频，生成人物讲话口型与输入音频相匹配的新视频。
  - 模型：`videoretalk`
- [视频风格重绘](groups/video-style-transform.json) — 视频风格重绘可以将输入的视频帧序列进行多种风格化的重绘/生成，使新视频画面在兼顾原始人物和物体相貌的同时，带来不同风格的绘画效果。当前支持预置重绘风格包括日式漫画、美式漫画、清新漫画、3D卡通、国风卡…
  - 模型：`video-style-transform`
- [舞动人像AnimateAnyone](groups/animate-anyone-gen2.json) — AnimateAnyone是一款视频生成模型，可基于人物图片和动作模板生成人物全身动作视频。
  - 模型：`animate-anyone-gen2`
- [舞动人像AnimateAnyone-detect](groups/animate-anyone-detect-gen2.json) — AnimateAnyone-detect是辅助AnimateAnyone的图像检测模型，用于检测图片中的人物形象是否符合视频生成要求。
  - 模型：`animate-anyone-detect-gen2`
- [舞动人像AnimateAnyone-template](groups/animate-anyone-template-gen2.json) — AnimateAnyone-Template是辅助AnimateAnyone的动作模板生成模型，可基于视频提取人物动作并制作模板。
  - 模型：`animate-anyone-template-gen2`
- [悦动人像EMO](groups/emo-v1.json) — EMO是一款视频生成模型，可基于人物图片生成高质量的人物肖像动态视频。
  - 模型：`emo-v1`
- [悦动人像EMO-detect](groups/emo-detect-v1.json) — EMO-Detect是辅助EMO的图像检测模型，用于检测图片中的人物形象是否符合视频生成要求。
  - 模型：`emo-detect-v1`
- [HappyHorse-I2V](groups/happyhorse-i2v.json) — HappyHorse系列最新图生视频模型，具备高度还原的动态画面生成能力，能够稳定保持与图像一致性，输出流畅自然、细节丰富的高质量视频。
  - 模型：`happyhorse-1.0-i2v`
- [HappyHorse-R2V](groups/happyhorse-r2v.json) — HappyHorse-R2V支持参考生视频，更加稳定的主体与场景参考，支持最多9张图片参考，能够精准保持创作意图，实现更强表现能力。
  - 模型：`happyhorse-1.0-r2v`
- [HappyHorse-T2V](groups/happyhorse-t2v.json) — HappyHorse系列最新文生视频模型，具备高度还原的动态画面生成能力，能够精准理解文本语义，输出流畅自然、细节丰富的高质量视频。
  - 模型：`happyhorse-1.0-t2v`
- [HappyHorse-Video-Edit](groups/happyhorse-video-edit.json) — HappyHorse-Video-Edit支持视频编辑，自然语言指令编辑视频，可参考最多5张图片局部或全局编辑视频元素，能够精准复刻视频动态过程，实现更强表现能力。
  - 模型：`happyhorse-1.0-video-edit`
- [PixVerse C1](groups/pixverse-c1-market-place.json) — 由爱诗科技提供的PixVerse C系列视频大模型API服务。
  - 模型：`pixverse/pixverse-c1-it2v`, `pixverse/pixverse-c1-kf2v`, `pixverse/pixverse-c1-r2v`, `pixverse/pixverse-c1-t2v`
- [PixVerse V5.6](groups/pixverse-market-place.json) — 由爱诗科技提供的PixVerse V系列视频大模型API服务。
  - 模型：`pixverse/pixverse-v5.6-it2v`, `pixverse/pixverse-v5.6-kf2v`, `pixverse/pixverse-v5.6-r2v`, `pixverse/pixverse-v5.6-t2v`
- [PixVerse V6](groups/pixverse-v6-market-place.json) — 由爱诗科技提供的PixVerse V系列视频大模型API服务。
  - 模型：`pixverse/pixverse-v6-it2v`, `pixverse/pixverse-v6-kf2v`, `pixverse/pixverse-v6-t2v`
- [Vidu](groups/vidu-models-market-place.json) — 由生数科技提供Vidu系列视频生成API服务，电影级画质、一致性保持、精准可控。
  - 模型：`vidu/viduq2_reference2video`, `vidu/viduq2_text2video`, `vidu/viduq2-pro_img2video`, `vidu/viduq2-pro_reference2video`, `vidu/viduq2-pro_start-end2video`, `vidu/viduq2-pro-fast_img2video`, `vidu/viduq2-turbo_img2video`, `vidu/viduq2-turbo_start-end2video`, `vidu/viduq3_reference2video`, `vidu/viduq3-mix_reference2video`, `vidu/viduq3-pro_img2video`, `vidu/viduq3-pro_start-end2video`, `vidu/viduq3-pro_text2video`, `vidu/viduq3-turbo_img2video`, `vidu/viduq3-turbo_reference2video`, `vidu/viduq3-turbo_start-end2video`, `vidu/viduq3-turbo_text2video`
- [Wan-I2V](groups/wan-image-to-video.json) — 图片生成视频内容，稳定保持图像主体、风格和文字等细节信息
  - 模型：`wan2.2-animate-mix`, `wan2.2-animate-move`, `wan2.2-i2v-flash`, `wan2.2-i2v-plus`, `wan2.2-kf2v-flash`, `wan2.2-s2v`, `wan2.2-s2v-detect`, `wan2.5-i2v-preview`, `wan2.6-i2v`, `wan2.6-i2v-flash`, `wan2.7-i2v`, `wanx2.1-i2v-plus`, `wanx2.1-i2v-turbo`, `wanx2.1-kf2v-plus`
- [Wan-R2V](groups/wan-reference-to-video.json) — 参考视频中的人或物，精准保持形象和声音，支持多参考合拍
  - 模型：`wan2.6-r2v`, `wan2.6-r2v-flash`, `wan2.7-r2v`
- [Wan-T2V](groups/wan-text-to-video.json) — 文字生成视频内容，丝滑动态能力，电影美学控制，精准指令遵循
  - 模型：`wan2.2-t2v-plus`, `wan2.5-t2v-preview`, `wan2.6-t2v`, `wan2.7-t2v`, `wanx2.1-t2v-plus`, `wanx2.1-t2v-turbo`
- [Wan-VideoEdit](groups/wan-video-edit.json) — 通过指令对视频进行编辑，支持局部/整体编辑、视频重塑、视频复刻等
  - 模型：`wan2.7-videoedit`
- [Wan2.1-VACE-Plus](groups/wanx2.1-vace-plus.json) — 万相2.1-VACE-Plus，视频编辑统一模型。支持局部编辑、视频重绘、背景扩展、时长延展、图片参考等多种视频编辑与生成任务，支持文本、图像、视频等多模态条件控制。
  - 模型：`wanx2.1-vace-plus`

## 推理 `Reasoning` — 16 个家族

- [DeepSeek](groups/deepseek.json) — DeepSeek是由深度求索提供的开源模型，包含 V3.1、V3、R1以及基于Qwen2.5系列蒸馏的大语言模型。
  - 模型：`deepseek-r1`, `deepseek-r1-0528`, `deepseek-r1-distill-qwen-1.5b`, `deepseek-r1-distill-qwen-14b`, `deepseek-r1-distill-qwen-32b`, `deepseek-r1-distill-qwen-7b`, `deepseek-v3`, `deepseek-v3.1`, `deepseek-v3.2`, `deepseek-v3.2-exp`, `deepseek-v4-flash`, `deepseek-v4-pro`
- [Kimi](groups/Kimi-K2.json) — Kimi是由月之暗面提供的开源模型，包含k2.5、k2-thinking、k2-instruct等多模态和大语言模型。
  - 模型：`kimi-k2-thinking`, `kimi-k2.5`, `kimi-k2.6`, `Moonshot-Kimi-K2-Instruct`
- [MiniMax](groups/MiniMax-M2.1.json) — MiniMax推出的旗舰级开源大模型，聚焦真实世界复杂任务，包含MiniMax-M2.1、MiniMax-M2.5等开源模型。
  - 模型：`MiniMax-M2.1`, `MiniMax-M2.5`
- [QVQ-Max](groups/qvq-max.json) — 千问QVQ视觉推理模型，支持视觉输入及思维链输出，在数学、编程、视觉分析、创作以及通用任务上都表现了更强的能力。
  - 模型：`qvq-max`
- [Qwen-Flash](groups/qwen-flash.json) — Qwen3系列Flash模型，实现思考模式和非思考模式的有效融合，可在对话中切换模式。复杂推理类任务性能优秀，指令遵循、文本理解等能力显著提高。支持1M上下文长度，按照上下文长度进行阶梯计费。
  - 模型：`qwen-flash`
- [Qwen-Plus](groups/qwen-plus.json) — 千问超大规模语言模型的增强版，支持中文英文等不同语言输入。主干模型、latest和快照04-28已升级Qwen3系列，实现思考模式和非思考模式的有效融合，可在对话中切换模式。
  - 模型：`qwen-plus`, `qwen-plus-0112`, `qwen-plus-1220`, `qwen-plus-latest`
- [Qwen-QVQ-Plus](groups/qvq-plus.json) — 千问QVQ视觉推理模型增强版，支持视觉输入及思维链输出，在数学、编程、视觉分析、创作以及通用任务上都表现了更强的能力。
  - 模型：`qvq-plus`
- [Qwen-QwQ-Plus](groups/qwq-plus.json) — 千问QwQ推理模型增强版，基于Qwen2.5模型训练的QwQ推理模型，通过强化学习大幅度提升了模型推理能力。模型数学代码等核心指标（AIME 24/25、livecodebench）以及部分通用指标（…
  - 模型：`qwq-plus`
- [Qwen-Turbo](groups/qwen-turbo.json) — 千问超大规模语言模型，支持中文英文等不同语言输入。主干模型、latest和快照04-28已升级Qwen3系列，实现思考模式和非思考模式的有效融合，可在对话中切换模式。
  - 模型：`qwen-turbo`
- [Qwen3.5-Flash](groups/qwen3.5-flash.json) — Qwen3.5原生视觉语言系列Flash模型，展现出与当前顶尖前沿模型相媲美的卓越性能，模型效果在纯文本与多模态方面相较3系列均实现飞跃式进步。
  - 模型：`qwen3.5-flash`
- [Qwen3.5开源模型](groups/qwen3.5.json) — Qwen3.5系列开源模型，基于混合架构设计的原生视觉语言模型，融合了线性注意力机制与稀疏混合专家模型，实现了更高的推理效率。
  - 模型：`qwen3.5-122b-a10b`, `qwen3.5-27b`, `qwen3.5-35b-a3b`, `qwen3.5-397b-a17b`
- [Qwen3.6-Flash](groups/qwen3.6-flash.json) — Qwen3.6原生视觉语言系列Flash模型，模型效果相较3.5-Flash显著提升。本模型重点提升agentic coding能力（在多项代码智能体基准上大幅超越前代）、数学推理和代码推理能力；视觉…
  - 模型：`qwen3.6-flash`
- [Qwen3.6-Max](groups/qwen3.6-max.json) — Qwen3.6原生Max模型，相较于此前发布的Qwen3-Max和Qwen3.6-Plus，本模型在vibe coding能力上进一步提升、coding agent执行更加高效、前端编程开发能力显著提…
  - 模型：`qwen3.6-max-preview`
- [Qwen3.6-Plus](groups/qwen3.6-plus.json) — Qwen3.6原生视觉语言系列Plus模型，展现出与当前顶尖前沿模型相媲美的卓越性能，模型效果相较3.5系列显著提升。模型在Agentic coding、前端编程、Vibe coding等代码能力、多…
  - 模型：`qwen3.6-plus`
- [Qwen3.7-Max](groups/qwen3.7-max.json) — Qwen3.7系列中规模最大、综合能力最强的Max模型，当前开放纯文本模型能力供体验。Qwen3.7是面向智能体时代的新一代旗舰模型，核心优势在于智能体能力的广度与深度：在编程、办公与生产力、长周期自…
  - 模型：`qwen3.7-max`, `qwen3.7-max-preview`
- [Vanchin DeepSeek](groups/vanchin-models-market-place.json) — 由快手万擎提供的DeepSeek系列模型API服务。
  - 模型：`vanchin/deepseek-ocr`, `vanchin/deepseek-r1`, `vanchin/deepseek-v3`, `vanchin/deepseek-v3.1-terminus`, `vanchin/deepseek-v3.2-think`

## 语音合成 `TTS` — 16 个家族

- [大模型声音复刻及声音设计](groups/voice-enrollment.json) — 大模型声音复刻服务依托先进的大模型技术进行特征提取，无需训练过程就可以完成声音的复刻。仅需提供极短的音频，即可迅速生成高度相似且听感自然的定制声音。 大模型声音设计使用FunAudioGen-VD模型…
  - 模型：`voice-enrollment`
- [音乐生成](groups/fun-music.json) — 百聆音乐生成大模型（Fun音乐大模型）支持输入开放性歌曲的创作要求或歌词，生成整首男/女声演唱的中文或英文歌曲。歌曲通俗易懂，情绪由浅入深，是人类灵感与大模型能力的完美结合。
  - 模型：`fun-music-v1`
- [CosyVoice大模型](groups/cosyvoice.json) — 基于新一代生成式语音大模型，CosyVoice将文本理解和语音生成技术深度融合，能够精准解析并诠释各种文本内容，将其转化为如同真人发声般的自然语音，带来高度拟人化的自然语音合成体验。
  - 模型：`cosyvoice-clone-v1`, `cosyvoice-v1`, `cosyvoice-v2`, `cosyvoice-v3-flash`, `cosyvoice-v3-plus`, `cosyvoice-v3.5-flash`, `cosyvoice-v3.5-plus`
- [MiniMax-Speech系列语音模型](groups/MiniMax-speech-market-place.json) — 由MiniMax提供的MiniMax-Speech系列语音模型API服务。
  - 模型：`MiniMax/speech-02-hd`, `MiniMax/speech-02-turbo`, `MiniMax/speech-2.8-hd`, `MiniMax/speech-2.8-turbo`
- [Qwen-声音复刻](groups/qwen-voice-enrollment.json) — 千问voice-enrollment模型是千问语音模型的声音复刻系列模型，仅需5s以上的音频，即可迅速复刻高相似度声音。结合qwen3-tts-vc-realtime模型使用，可将一个人的声音高保真复…
  - 模型：`qwen-voice-enrollment`
- [Qwen-声音设计](groups/qwen-voice-design.json) — Qwen-Voice-Design模型是千问语音模型的声音设计系列模型，仅需输入简单的文字描述，即可迅速设计出符合要求的相关声音。结合qwen3-tts-vd-realtime模型使用，可设计输出11…
  - 模型：`qwen-voice-design`
- [Qwen-TTS](groups/qwen-tts.json) — 千问系列首个语音合成模型，支持中文、英文、中英混合输入。自适应根据输入文本调整输出语气，音色真实自然，支持输入输出全流式。
  - 模型：`qwen-tts`, `qwen-tts-latest`
- [Qwen3-TTS-Flash](groups/qwen3-tts-flash.json) — Qwen3-TTS-Flash模型是通义实验室最新推出的离线语音合成大模型，不仅拥有17种高表现力的拟人音色，且能低延迟高稳定地合成音频；同时支持多种语言，方言，支持同一音色多语言输出。该模型经过海量…
  - 模型：`qwen3-tts-flash`
- [Qwen3-TTS-Flash-Realtime](groups/qwen3-tts-flash-realtime.json) — Qwen3-TTS-Flash-Realtime模型是通义实验室最新的实时语音合成大模型，不仅拥有17种高表现力的拟人音色，且能低延迟高稳定地实时合成音频；同时支持多种语言，方言，支持同一音色多语言输…
  - 模型：`qwen3-tts-flash-realtime`
- [Qwen3-TTS-Instruct-Flash](groups/qwen3-tts-instruct-flash.json) — Qwen3-TTS-Flash模型是通义实验室最新推出的实时语音合成大模型，Instruct模型可通过自然语言进行合成效果的处理，确保在不同语境下，合成情感、表达高度贴合的语音。目前支持25个音色的中…
  - 模型：`qwen3-tts-instruct-flash`
- [qwen3-tts-instruct-flash-realtime](groups/qwen3-tts-instruct-flash-realtime.json) — 通义千问3-TTS-Flash模型是通义最新推出的实时语音合成大模型，Instruct模型可通过自然语言进行合成效果的处理，确保在不同语境下，合成情感、表达高度贴合的语音。目前支持25个音色的中英文I…
  - 模型：`qwen3-tts-instruct-flash-realtime`
- [Qwen3-TTS-VC](groups/qwen3-tts-vc.json) — Qwen3-TTS-Flash模型是通义实验室最新推出的实时语音合成大模型，可对qwen-voice-enrollment服务复刻的声音进行高保真实时语音合成，且同一音色支持11个语种的语音输出。该模…
  - 模型：`qwen3-tts-vc-2026-01-22`
- [Qwen3-TTS-VC-Realtime](groups/qwen3-tts-vc-realtime.json) — Qwen3-TTS-VC-Realtime模型是通义实验室最新推出的实时语音合成大模型，可对qwen3-voice-enrollment服务复刻的声音进行高保真实时语音合成，且同一音色支持11个语种的…
  - 模型：`qwen3-tts-vc-realtime-2026-01-15`
- [Qwen3-TTS-VD](groups/qwen3-tts-vd.json) — Qwen3-TTS-VD模型是通义实验室最新推出的实时语音合成大模型，可对qwen3-voice-design服务设计的声音进行高保真实时语音合成，且同一音色支持11个语种的语音输出。该模型经过海量数…
  - 模型：`qwen3-tts-vd-2026-01-26`
- [Qwen3-TTS-VD-Realtime](groups/qwen3-tts-vd-realtime.json) — Qwen3-TTS-VD模型是通义实验室最新推出的实时语音合成大模型，可对qwen3-voice-design服务设计的声音进行高保真实时语音合成，且同一音色支持11个语种的语音输出。该模型经过海量数…
  - 模型：`qwen3-tts-vd-realtime-2026-01-15`
- [Sambert语音合成](groups/sambert.json) — 提供高效的文字转语音服务。该技术具备推理速度快、合成效果卓越、读音精准、韵律自然、声音还原度高以及表现力强等优点。此外，用户可以选择开启字级别和音素级别的时间戳，用于生成字幕或驱动数字人的嘴型。
  - 模型：`sambert-beth-v1`, `sambert-betty-v1`, `sambert-brian-v1`, `sambert-cally-v1`, `sambert-camila-v1`, `sambert-cindy-v1`, `sambert-clara-v1`, `sambert-donna-v1`, `sambert-eva-v1`, `sambert-hanna-v1`, `sambert-indah-v1`, `sambert-perla-v1`, `sambert-waan-v1`, `sambert-zhichu-v1`, `sambert-zhida-v1`, `sambert-zhide-v1`, `sambert-zhifei-v1`, `sambert-zhigui-v1`, `sambert-zhihao-v1`, `sambert-zhijia-v1`, `sambert-zhijing-v1`, `sambert-zhilun-v1`, `sambert-zhimao-v1`, `sambert-zhimiao-emo-v1`, `sambert-zhiming-v1`, `sambert-zhimo-v1`, `sambert-zhina-v1`, `sambert-zhinan-v1`, `sambert-zhiqi-v1`, `sambert-zhiqian-v1`, `sambert-zhiru-v1`, `sambert-zhishu-v1`, `sambert-zhishuo-v1`, `sambert-zhistella-v1`, `sambert-zhiting-v1`, `sambert-zhiwei-v1`, `sambert-zhixiang-v1`, `sambert-zhixiao-v1`, `sambert-zhiya-v1`, `sambert-zhiye-v1`, `sambert-zhiying-v1`, `sambert-zhiyuan-v1`, `sambert-zhiyue-v1`

## 语音识别 `ASR` — 11 个家族

- [一句话识别及翻译V1.0](groups/gummy-chat-v1.json) — 多语言语音转写及翻译的多模态大模型。本模型支持60秒以内的实时语音识别，适用于语音搜索、设备指令等场景。提供10个混合语种的高准确率识别服务，同时支持中英日韩互译，以其他6个语种翻译成中文或英文。
  - 模型：`gummy-chat-v1`
- [语音识别热词](groups/speech-biasing.json) — 热词是指用户可以预先定义的一组特定词汇或短语，这些词汇或短语在识别、翻译过程中会被赋予更高的优先级。针对您的特定业务领域，如果有部分词汇的语音识别、翻译效果不够好，可以将这些关键词或短语添加为热词进行…
  - 模型：`speech-biasing`
- [Fun-ASR语音识别](groups/fun-asr.json) — 通义百聆新一代语音识别大模型，主打中文、英文、日文语音识别，多地区方言覆盖，具备更强的噪声鲁棒性，适应多样复杂环境，国内用户首推。
  - 模型：`fun-asr`, `fun-asr-mtl`
- [Paraformer语音识别-8k-v1](groups/paraformer-8k-v1.json) — Paraformer语音识别提供的文件转写API，能够对常见的音频或音视频文件进行语音识别，并将结果返回给调用者。Paraformer中文语音识别模型，支持8kHz电话语音识别。
  - 模型：`paraformer-8k-v1`
- [Paraformer语音识别-8k-v2](groups/paraformer-8k-v2.json) — Paraformer最新中文语音识别模型，模型结构升级，具有更好的识别效果,支持8kHz电话语音识别，仅支持中文热词。
  - 模型：`paraformer-8k-v2`
- [Paraformer语音识别-mtl-v1](groups/paraformer-mtl-v1.json) — Paraformer多语言语音识别模型，支持16kHz及以上采样率的音频或视频语音识别。 支持的语种/方言包括：中文普通话、中文方言（粤语、吴语、闽南语、东北话、甘肃话、贵州话、河南话、湖北话、湖南话…
  - 模型：`paraformer-mtl-v1`
- [Paraformer语音识别-v1](groups/paraformer-v1.json) — Paraformer中英文语音识别模型，支持16kHz及以上采样率的音频或视频语音识别。
  - 模型：`paraformer-v1`
- [Paraformer语音识别-v2](groups/paraformer-v2.json) — 推荐使用 Paraformer最新语音识别模型，支持多个语种的语音识别。可以通过language_hints参数选择语种获得更准确的识别效果，支持任意采样率。 支持的语言包括：中文（含粤语等各种方言）…
  - 模型：`paraformer-v2`
- [Qwen3-ASR-Flash](groups/qwen3-asr-flash.json) — Qwen3-ASR-Flash是一款基于大语言模型的高精度、高智能、高鲁棒性的多语种语音识别模型。依托强大的基座模型、海量的文本与多模态数据、千万小时音频数据，Qwen3-ASR-Flash实现了高精…
  - 模型：`qwen3-asr-flash`
- [Qwen3-ASR-Flash-Filetrans](groups/qwen3-asr-flash-filetrans.json) — Qwen3-ASR-Flash的大文件转录版本，Qwen3-ASR-Flash是一款基于大语言模型的高精度、高智能、高鲁棒性的多语种语音识别模型。依托强大的基座模型、海量的文本与多模态数据、千万小时音…
  - 模型：`qwen3-asr-flash-filetrans`
- [Qwen3-Omni-30b-a3b-Captioner](groups/qwen3-omni-30b-a3b-captioner.json) — 千问3-Omni-30b-a3b-Captioner是一款强大的音频细粒度分析模型，专为在复杂多变的音频场景中生成精准、全面的内容描述而设计，可自动解析并描述从复杂语音、环境声到音乐、影视声效等各类音…
  - 模型：`qwen3-omni-30b-a3b-captioner`

## 视觉理解 `VU` — 8 个家族

- [GUI-Plus](groups/gui-plus.json) — GUI系列图形界面交互基础模型，针对手机端与电脑端图形界面理解与交互任务，性能优于开源版同类GUI模型。全面升级跨平台界面理解与多步任务规划，支持跨应用复杂任务；具备精细化动作执行与多角色多智能体协作…
  - 模型：`gui-plus`
- [Qwen-VL-Max](groups/qwen-vl-max.json) — Qwen-VL-Max，即千问超大规模视觉语言模型。相比增强版，再次提升视觉推理能力和指令遵循能力，提供更高的视觉感知和认知水平。在更多复杂任务上提供最佳的性能。
  - 模型：`qwen-vl-max`
- [Qwen-VL-OCR](groups/qwen-vl-ocr.json) — Qwen-VL-OCR，即基于Qwen-VL训练的OCR识别大模型。通过统一模型的方式聚合多种图文识别、解析、处理类任务，提供强大的图文识别能力。
  - 模型：`qwen-vl-ocr`, `qwen-vl-ocr-1028`, `qwen-vl-ocr-latest`
- [Qwen-VL-Plus](groups/qwen-vl-plus.json) — Qwen-VL-Plus，即千问大规模视觉语言模型增强版。大幅提升细节识别能力和文字识别能力，支持超百万像素分辨率和任意长宽比规格的图像。在广泛的视觉任务上提供卓越的性能。
  - 模型：`qwen-vl-plus`, `qwen-vl-plus-latest`
- [Qwen3-VL-Flash](groups/qwen3-vl-flash.json) — Qwen3系列小尺寸视觉理解模型，实现思考模式和非思考模式的有效融合，效果优于开源版Qwen3-VL-30B-A3B，响应速度快。全面升级图像/视频理解，支持长视频长文档等超长上下文、空间感知与万物识…
  - 模型：`qwen3-vl-flash`
- [Qwen3-VL-Plus](groups/qwen3-vl-plus.json) — Qwen3系列视觉理解模型，实现思考模式和非思考模式的有效融合，视觉智能体能力在OS World等公开测试集上达到世界顶尖水平。此版本在视觉coding、空间感知、多模态思考等方向全面升级；视觉感知与…
  - 模型：`qwen3-vl-plus`
- [Qwen3.6开源模型](groups/qwen3.6.json) — Qwen3.6系列开源模型，基于混合架构设计的原生视觉语言模型，模型效果相较于3.5系列同尺寸有大幅提升。
  - 模型：`qwen3.6-27b`, `qwen3.6-35b-a3b`
- [Qwen3开源模型](groups/qwen3.json) — Qwen3系列开源模型，包含混合模型、思考模型与非思考模型，思考能力与通用能力均达到同规模业界SOTA水平。
  - 模型：`qwen3-14b`, `qwen3-235b-a22b`, `qwen3-235b-a22b-instruct-2507`, `qwen3-235b-a22b-thinking-2507`, `qwen3-30b-a3b`, `qwen3-30b-a3b-instruct-2507`, `qwen3-30b-a3b-thinking-2507`, `qwen3-32b`, `qwen3-8b`, `qwen3-coder-next`, `qwen3-next-80b-a3b-instruct`, `qwen3-next-80b-a3b-thinking`, `qwen3-vl-235b-a22b-instruct`, `qwen3-vl-235b-a22b-thinking`, `qwen3-vl-30b-a3b-instruct`, `qwen3-vl-30b-a3b-thinking`, `qwen3-vl-32b-instruct`, `qwen3-vl-32b-thinking`, `qwen3-vl-8b-instruct`, `qwen3-vl-8b-thinking`

## 实时语音识别 `Realtime-ASR` — 7 个家族

- [Fun-ASR实时语音识别](groups/fun-asr-realtime.json) — 通义实验室新一代端到端语音识别大模型的实时版，基于领先的自研语音技术，具备卓越的上下文感知和高精度语音转写能力。基于端到端架构，Fun-ASR 集成了创新的 RAG 技术，支持大规模热词自定义、敏感/…
  - 模型：`fun-asr-flash-8k-realtime`, `fun-asr-realtime`
- [Paraformer实时语音识别-8k-v1](groups/paraformer-realtime-8k-v1.json) — Paraformer中文实时语音识别模型，支持8kHz电话客服等场景下的实时语音识别。
  - 模型：`paraformer-realtime-8k-v1`
- [Paraformer实时语音识别-8k-v2](groups/paraformer-realtime-8k-v2.json) — 推荐使用 Paraformer最新实时语音识别模型，支持多个语种自由切换的视频直播、会议等实时场景的语音识别。可以通过language_hints参数选择语种获得更准确的识别效果。支持8kHz电话客服…
  - 模型：`paraformer-realtime-8k-v2`
- [Paraformer实时语音识别-v1](groups/paraformer-realtime-v1.json) — Paraformer中文实时语音识别模型，支持16kHz及以上采样率的视频直播、会议等实时场景下的语音识别。
  - 模型：`paraformer-realtime-v1`
- [Paraformer实时语音识别-v2](groups/paraformer-realtime-v2.json) — 推荐使用 Paraformer最新实时语音识别模型，支持多个语种自由切换的视频直播、会议等实时场景的语音识别。可以通过language_hints参数选择语种获得更准确的识别效果。支持任意采样率。 支…
  - 模型：`paraformer-realtime-v2`
- [Qwen3-ASR-Flash-Realtime](groups/qwen3-asr-flash-realtime.json) — Qwen3-ASR-Flash的实时版，一款基于大语言模型的高精度、高智能、高鲁棒性的多语种语音识别模型。依托强大的基座模型、海量的文本与多模态数据、千万小时音频数据，Qwen3-ASR-Flash实…
  - 模型：`qwen3-asr-flash-realtime`
- [Qwen3-LiveTranslate-Flash](groups/qwen3-livetranslate-flash.json) — Qwen3-LiveTranslate-Flash，一款高精度、高响应、高鲁棒性的多语言实时音视频同传大模型。依托Qwen3-Omni强大的基座能力、海量多模态数据、跨语言跨模态对齐和视觉增强等技术，…
  - 模型：`qwen3-livetranslate-flash`

## 全模态 `Multimodal-Omni` — 5 个家族

- [Qwen-Omni-Turbo](groups/qwen-omni-turbo.json) — 千问全新多模态理解生成大模型，支持文本, 图像，语音，视频输入理解和混合输入理解，具备文本和语音同时流式生成能力，多模态内容理解速度显著提升，提供了4种自然对话音色。
  - 模型：`qwen-omni-turbo`, `qwen-omni-turbo-latest`
- [Qwen2.5-开源模型](groups/qwen2.5.json) — Qwen2.5系列开源模型，包含文本生成模型、视觉理解模型、多模态模型等多个领域领先模型。
  - 模型：`qwen2.5-omni-7b`
- [Qwen3-Omni-Flash](groups/qwen3-omni-flash.json) — Qwen3-Omni-Flash多模态大模型，基于Thinker–Talker混合专家（MoE）架构，支持文本、图像、音频、视频的高效理解与语音生成能力，可进行119种语言文本交互和20种语言语音交互…
  - 模型：`qwen3-omni-flash`
- [Qwen3.5-Omni-Flash](groups/qwen3.5-omni-flash.json) — Qwen3.5-Omni是Qwen最新一代全模态大模型，支持文本，图片，音频，音视频理解与交互。作为 Qwen3-Omni 的全面进化版本， 支持超过 10 小时的音频理解及超过 400 秒的 720…
  - 模型：`qwen3.5-omni-flash`
- [Qwen3.5-Omni-Plus](groups/qwen3.5-omni-plus.json) — Qwen3.5-Omni是Qwen最新一代全模态大模型，支持文本，图片，音频，音视频理解与交互。作为 Qwen3-Omni 的全面进化版本， 支持超过 10 小时的音频理解及超过 400 秒的 720…
  - 模型：`qwen3.5-omni-plus`

## 实时全模态 `Realtime-Omni` — 4 个家族

- [Qwen-Omni-Turbo-Realtime](groups/qwen-omni-turbo-realtime.json) — 千问全新多模态理解生成大模型实时版，适合实时音频交互场景。支持音频伴随文本、图像、视频混合输入理解，具备语音和文本同时流式生成能力，提供了4种自然对话音色。
  - 模型：`qwen-omni-turbo-realtime`, `qwen-omni-turbo-realtime-latest`
- [Qwen3-Omni-Flash-Realtime](groups/qwen3-omni-flash-realtime.json) — Qwen3-Omni-Flash-Realtime多模态大模型的实时版，基于Thinker–Talker混合专家（MoE）架构，支持文本、图像、音频、视频的高效理解与语音生成能力，可进行119种语言文…
  - 模型：`qwen3-omni-flash-realtime`
- [Qwen3.5-Omni-Flash-Realtime](groups/qwen3.5-omni-flash-realtime.json) — Qwen3.5-Omni是Qwen最新一代全模态大模型，支持文本，图片，音频，音视频理解与交互。作为 Qwen3-Omni 的全面进化版本，支持60+种语言音频输入，30+语言语音输出以及可控语音对话…
  - 模型：`qwen3.5-omni-flash-realtime`
- [Qwen3.5-Omni-Plus-Realtime](groups/qwen3.5-omni-plus-realtime.json) — Qwen3.5-Omni是Qwen最新一代全模态大模型，支持文本，图片，音频，音视频理解与交互。作为 Qwen3-Omni 的全面进化版本，支持60+种语言音频输入，30+语言语音输出以及可控语音对话…
  - 模型：`qwen3.5-omni-plus-realtime`

## 实时音频翻译 `Realtime-Audio-Translate` — 3 个家族

- [实时语音识别及翻译V1.0](groups/gummy-realtime-v1.json) — 多语言语音转写及翻译的多模态大模型。本模型提供长时间、高准确率、实时转写中/英/日/韩等10个混合语种的服务。同时支持中英日韩互译，以其他6个语种翻译成中文或英文。
  - 模型：`gummy-realtime-v1`
- [Qwen3-LiveTranslate-Flash-Realtime](groups/qwen3-livetranslate-flash-realtime.json) — Qwen3-LiveTranslate-Flash-Realtime的实时版本，一款高精度、高响应、高鲁棒性的多语言实时音视频同传大模型。依托Qwen3-Omni强大的基座能力、海量多模态数据、跨语言…
  - 模型：`qwen3-livetranslate-flash-realtime`
- [Qwen3.5-LiveTranslate-Flash-Realtime](groups/qwen3.5-livetranslate-flash-realtime.json) — Qwen3.5-LiveTranslate-Flash的实时版本，一款高精度、高响应、高鲁棒性的多语言实时音视频同传大模型。依托Qwen3.5-Omni强大的基座能力、海量多模态数据、跨语言跨模态对齐…
  - 模型：`qwen3.5-livetranslate-flash-realtime`

## 多模态嵌入 `ME` — 2 个家族

- [通义多模态向量](groups/embedding.json) — 基于LLM底座的通用多模态表征模型，支持文本、图像、视频3种模态，具有以视觉为中心、全场景性能优异、高性价比的特点，适用于以图搜图、以文搜图、以文搜视频、以视频搜视频、以文搜文等下游多样化任务场景。
  - 模型：`multimodal-embedding-v1`, `tongyi-embedding-vision-flash`, `tongyi-embedding-vision-plus`
- [Qwen-VL-Embedding](groups/qwen-vl-embedding.json) — 基于Qwen-VL底座训练的统一多模态向量模型，支持文本、图片、视频单模态/混合模态输入，输出统一表征向量，适用于跨模态检索、图搜、视频检索、图像聚类、复杂多模态信息检索、打标等场景。
  - 模型：`qwen2.5-vl-embedding`, `qwen3-vl-embedding`

## 翻译 `TR` — 2 个家族

- [Qwen-Embedding](groups/qwen-embedding.json) — 基于Qwen模型基座训练的多语言文本统一向量模型，文本检索、聚类、分类性能大幅提升，多语言支持，适用于向量检索、向量化等等场景，可搭配检索增强、文档处理场景使用，支持64~2048维用户自定义向量维度…
  - 模型：`text-embedding-async-v1`, `text-embedding-async-v2`, `text-embedding-v1`, `text-embedding-v2`, `text-embedding-v3`, `text-embedding-v4`
- [Qwen-Rerank](groups/qwen-rerank.json) — 基于Qwen LLM底座训练的文本排序模型，对输入的Query和候选Docs进行相关性排序，支持100+语种和长文本输入，适用于文本检索、RAG等场景，效果对齐Qwen家族开源Rerank系列模型。
  - 模型：`gte-rerank-v2`, `qwen3-rerank`, `qwen3-vl-rerank`

## 实时语音合成 `Realtime-Text-to-Speech` — 1 个家族

- [Qwen-TTS-Realtime](groups/qwen-tts-realtime.json) — Qwen-TTS实时模型是通义实验室“qwen系列”模型中的语音合成利器。具备双向上下文感知能力，可以低延迟高保真完成多音色、方言及长文本的双向流式生成。
  - 模型：`qwen-tts-realtime`, `qwen-tts-realtime-latest`

## 3D 生成 `3D-generation` — 1 个家族

- [Tripo](groups/tripo-models-market-place.json) — AI驱动的3D通用大模型Tripo，支持文本或图片输入，数秒内一键生成高质量3D模型。
  - 模型：`Tripo/Tripo-H3.1`, `Tripo/Tripo-P1.0`
