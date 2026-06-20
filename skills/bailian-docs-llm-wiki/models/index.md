# 百炼模型市场索引

> 自动生成 · 共 78 个模型家族 · 90 个主干模型 · 更新于 2026-06-20

**机器查询走结构化文件**：

- `index.json` — 全局摘要（统计 + 能力/厂商分布 + 轻量家族列表）
- `families.jsonl` — 每行一个家族（含轻量 `items[]` 摘要），适合按家族筛选
- `models.jsonl` — 每行一个主干模型（含价格/QPM/features），适合跨家族批量查询
- `groups/<slug>.json` — 单家族完整明细（含调用代码、入参 schema）

join：`models.jsonl[].family == families.jsonl[].slug == index.json.families[].slug`。

## 图像生成 `IG` — 21 个家族

- [AI试衣-Plus版](groups/aitryon-plus.json) — aitryon-plus是一款效果出众的虚拟试衣图片生成模型，可基于服饰平拍图片以及人物正面全身照，输出服饰的人物试衣效果图片。 相较于aitryon模型，aitryon-plus模型在图片清晰度、服…
  - 模型：`aitryon-plus`
- [AI试衣-基础版](groups/aitryon.json) — aitryon是一款性能出众的虚拟试衣图片生成模型，可基于服饰平拍图片以及人物正面全身照，输出服饰的人物试衣效果图片。aitryon模型可在较短时间内生成试衣图片，适用于对时效性要求较高的场景。
  - 模型：`aitryon`
- [AI试衣OutfitAnyone-图片分割](groups/aitryon-parsing-v1.json) — 图片分割模型是AI试衣OutfitAnyone的辅助模型，可对模特图、服饰图进行分割，用于试衣图片的前后处理。
  - 模型：`aitryon-parsing-v1`
- [AI试衣OutfitAnyone-图片精修](groups/aitryon-refiner.json) — 图片精修是对AI试衣生成的效果图进行二次生成，输出还原度更高的精修试衣效果图。
  - 模型：`aitryon-refiner`
- [FaceChain人物写真生成](groups/facechain-generation.json) — 基于人物形象训练已经得到的形象，可以继续通过人物生成写真模型完成该形象的写真生成，支持多种预设风格，包括证件照、商务写真等。
  - 模型：`facechain-generation`
- [FaceChain人物图像检测](groups/facechain-facedetect.json) — 对用户上传的人物图像进行检测，判断其中所包含的人脸是否符合facechain微调所需的标准，检测维度包括人脸数量、大小、角度、光照、清晰度等多维度，支持图像组输入，并返回每张图像对应的检测结果。
  - 模型：`facechain-facedetect`
- [Qwen-MT-Image](groups/qwen-mt-image.json) — 专注做图片翻译的模型服务，能将中、英、日等11个语言的图片翻译到指定的语言，精准还原图片排版和内容信息，支持术语定义、敏感词过滤、商品主体检测等自定义功能，提供灵活、准确、高效的图像本地化服务。
  - 模型：`qwen-mt-image`
- [WordArt锦书-文字变形](groups/wordart-semantic.json) — WordArt锦书-文字变形可以对输入的文字边缘轮廓进行创意变形，根据提示词内容进行边缘变化，实现一种字体的更多种创意用法，返回带有文字内容的黑底白色mask图。
  - 模型：`wordart-semantic`
- [WordArt锦书-文字纹理生成](groups/wordart-texture.json) — WordArt锦书-文字纹理生成可以对输入的文字内容或文字图片进行创意设计，根据提示词内容对文字添加材质和纹理，实现立体凸显或场景融合的效果，生成效果精美、风格多样的艺术字，结合背景可以直接作为文字海…
  - 模型：`wordart-texture`
- [Z-Image-Turbo](groups/z-image-turbo.json) — Z-Image-Turbo是在Artificial Analysis评测中荣登文生图开源模型世界第一的高效图像生成模型,仅用60亿参数和8步推理就能生成媲美大规模商业模型的照片级真实感图像,并在中英双…
  - 模型：`z-image-turbo`
- [万相-图像局部重绘](groups/wanx-x-painting.json) — 万相-图像局部重绘是基于自研的Composer组合生成框架的AI绘画创作大模型后置处理链路，能够根据用户输入的原始图片和意涂抹图中局部区域和prompt提示词文字内容，生成符合语义描述的多样化风格的局…
  - 模型：`wanx-x-painting`
- [万相-涂鸦作画](groups/wanx-sketch-to-image-lite.json) — 万相-涂鸦作画通过手绘任意内容加文字描述，即可生成精美的涂鸦绘画作品，作品中的内容在参考手绘线条的同时，兼顾创意性和趣味性。涂鸦作画支持扁平插画、油画、二次元、3D卡通和水彩5种风格，可用于创意娱乐、…
  - 模型：`wanx-sketch-to-image-lite`
- [人像风格重绘](groups/wanx-style-repaint-v1.json) — 人像风格重绘可以将输入的人物图像进行多种风格化的重绘生成，使新生成的图像在兼顾原始人物相貌的同时，带来不同风格的绘画效果。
  - 模型：`wanx-style-repaint-v1`
- [人物实例分割](groups/image-instance-segmentation.json) — 人物实例分割运用了检测和分割技术，不仅能够在图像中识别出不同的对象，而且还能准确地画出每一个对象边界的像素级掩码（mask）。
  - 模型：`image-instance-segmentation`
- [创意海报生成](groups/wanx-poster-generation-v1.json) — 创意海报生成，您的创意海报魔法工厂！它能够根据你的要求自动生成海报的背景和文字排版，支持多种海报风格，从宣传到祝福，让每一张海报都成为你的个性宣言。无需设计基础，轻松制作出彩作品，让创意触手可及。
  - 模型：`wanx-poster-generation-v1`
- [图像擦除补全](groups/image-erase-completion.json) — 图像擦除补全通过指定图像mask中要删除的人体、宠物、物品、文字、水印等图像区域，在保留背景的同时移除图像中的一个或多个人物、物体、文字等元素，此功能不支持输入prompt的消除。擦除补全技术结合了计…
  - 模型：`image-erase-completion`
- [图像画面扩展](groups/image-out-painting.json) — 图像画面大模型，对输入图像进行画面自由扩展，支持旋转画面，支持按照扩展系数和扩展像素数两种方式进行扩图。用户可以通过指定宽度、高度画面扩展比例或者左、右、上、下的扩展的像素值来控制画面扩展，可用于创意…
  - 模型：`image-out-painting`
- [图像背景生成](groups/wanx-background-generation-v2.json) — 图像背景生成可以基于输入的前景图像素材拓展生成背景信息，实现自然的光影融合效果，与细腻的写实画面生成。支持文本描述、图像引导等多种方式，同时支持对生成的图像智能添加文字内容。
  - 模型：`wanx-background-generation-v2`
- [虚拟模特](groups/wanx-virtualmodel.json) — 虚拟模特可以对上传的真人或者人台实拍商品展示图进行智能生成，将其中的模特和背景替换为心仪的内容，在保持人物姿态不变的情况下，使用虚拟模特对商品进行更加精美、多样的展示。支持各种与模特产生互动的商品，如…
  - 模型：`wanx-virtualmodel`
- [虚拟模特V2](groups/virtualmodel-v2.json) — 虚拟模特可以对上传的真人或者人台实拍商品展示图进行智能生成，将其中的模特和背景替换为心仪的内容，在保持人物姿态不变的情况下，使用虚拟模特对商品进行更加精美、多样的展示。支持各种与模特产生互动的商品，如…
  - 模型：`virtualmodel-v2`
- [鞋靴模特](groups/shoemodel-v1.json) — 鞋靴模特支持输入多视角鞋靴系列图片，同时对输入模特模板图的鞋子区域进行鞋靴AI试穿，实现模特鞋靴布局重绘生成，最终生成图片的效果, 布局自然、细节丰富、画面细腻、试穿结果逼真。可用于模特商品图设计、新…
  - 模型：`shoemodel-v1`

## 文本生成 `TG` — 19 个家族

- [Qwen-Coder-Plus](groups/qwen-coder-plus.json) — 千问系列代码及编程模型是专门用于编程和代码生成的语言模型，性能出色，效果突出。
  - 模型：`qwen-coder-plus`
- [Qwen-Coder-Turbo](groups/qwen-coder-turbo.json) — Qwen-Coder-Turbo模型是专门用于编程和代码生成的语言模型，推理速度快，成本低。
  - 模型：`qwen-coder-turbo`
- [qwen-deep-research](groups/qwen-deep-research.json) — 千问深入研究是一款面向复杂研究任务的高级智能体系统，具备多轮推理与全局规划能力，能够运用互联网搜索等多种工具，对任务进行精细化拆解，开展推理与分析，最终为用户生成可溯源、逻辑严谨的研究型报告。
  - 模型：`qwen-deep-research`
- [Qwen-Doc-Turbo](groups/qwen-doc-turbo.json) — 快速对文档进行精准信息抽取，打标分类，内容审核及摘要总结。
  - 模型：`qwen-doc-turbo`
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
- [意图分类模型](groups/tongyi-intent-detect-v3.json) — 意图识别和槽位填充是对话系统中的基础任务。本模型实现了一个基于 API的意图（intent）和槽位参数（slots）联合预测。在一次模型输出中，同时完成多个指令API的返回和槽位参数的填充。返回的结果…
  - 模型：`tongyi-intent-detect-v3`
- [通义晓蜜-对话分析-flash](groups/tongyi-xiaomi-analysis-flash.json) — 通义晓蜜-对话分析-flash是专注于日常任务，如对话信息抽取、场景分类等分析类需求的模型，自定义分析标准遵循与对话语义理解能力显著提升，适用于低时延的离线在线分析任务。
  - 模型：`tongyi-xiaomi-analysis-flash`
- [通义晓蜜-对话分析-pro](groups/tongyi-xiaomi-analysis-pro.json) — 通义晓蜜-对话分析-pro是专注于高阶复杂分析，如针对具备复杂业务逻辑的复杂质检规则等分析需求的模型，支持自定义更细粒度的分析标准，具备更强的多轮上下文建模、深层语义理解与推理能力。
  - 模型：`tongyi-xiaomi-analysis-pro`
- [通义法睿-Plus-32K](groups/farui-plus.json) — 通义法睿是以通义千问为基座经法律行业数据和知识专门训练的法律行业大模型产品，综合运用了模型精调、强化学习、 RAG检索增强、法律Agent技术，具有回答法律问题、推理法律适用、推荐裁判类案、辅助案情分…
  - 模型：`farui-plus`

## 视频生成 `VG` — 12 个家族

- [Wan2.1-VACE-Plus](groups/wanx2.1-vace-plus.json) — 万相2.1-VACE-Plus，视频编辑统一模型。支持局部编辑、视频重绘、背景扩展、时长延展、图片参考等多种视频编辑与生成任务，支持文本、图像、视频等多模态条件控制。
  - 模型：`wanx2.1-vace-plus`
- [声动人像VideoRetalk](groups/videoretalk.json) — VideoRetalk是一个人物视频生成模型，可基于人物视频和人声音频，生成人物讲话口型与输入音频相匹配的新视频。
  - 模型：`videoretalk`
- [悦动人像EMO](groups/emo-v1.json) — EMO是一款视频生成模型，可基于人物图片生成高质量的人物肖像动态视频。
  - 模型：`emo-v1`
- [悦动人像EMO-detect](groups/emo-detect-v1.json) — EMO-Detect是辅助EMO的图像检测模型，用于检测图片中的人物形象是否符合视频生成要求。
  - 模型：`emo-detect-v1`
- [灵动人像LivePortrait](groups/liveportrait.json) — LivePortrait是一款视频生成模型，可基于人物图片生成轻量化的人物肖像动态视频。
  - 模型：`liveportrait`
- [灵动人像LivePortrait-detect](groups/liveportrait-detect.json) — LivePortrait-detect是辅助LivePortrait的图像检测模型，用于检测图片中的人物形象是否符合视频生成要求。
  - 模型：`liveportrait-detect`
- [视频风格重绘](groups/video-style-transform.json) — 视频风格重绘可以将输入的视频帧序列进行多种风格化的重绘/生成，使新视频画面在兼顾原始人物和物体相貌的同时，带来不同风格的绘画效果。当前支持预置重绘风格包括日式漫画、美式漫画、清新漫画、3D卡通、国风卡…
  - 模型：`video-style-transform`
- [舞动人像AnimateAnyone](groups/animate-anyone-gen2.json) — AnimateAnyone是一款视频生成模型，可基于人物图片和动作模板生成人物全身动作视频。
  - 模型：`animate-anyone-gen2`
- [舞动人像AnimateAnyone-detect](groups/animate-anyone-detect-gen2.json) — AnimateAnyone-detect是辅助AnimateAnyone的图像检测模型，用于检测图片中的人物形象是否符合视频生成要求。
  - 模型：`animate-anyone-detect-gen2`
- [舞动人像AnimateAnyone-template](groups/animate-anyone-template-gen2.json) — AnimateAnyone-Template是辅助AnimateAnyone的动作模板生成模型，可基于视频提取人物动作并制作模板。
  - 模型：`animate-anyone-template-gen2`
- [表情包Emoji](groups/emoji-v1.json) — 表情包emoji是一款人脸动效视频生成模型，可基于人脸图片和预设的人脸动态模板，生成人脸动效视频。
  - 模型：`emoji-v1`
- [表情包Emoji-detect](groups/emoji-detect-v1.json) — 表情包Emoji-Detect是辅助表情包Emoji生成的图像检测模型，用于检测图片中的人物形象是否符合视频生成要求。
  - 模型：`emoji-detect-v1`

## 语音识别 `ASR` — 8 个家族

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
- [Qwen3-Omni-30b-a3b-Captioner](groups/qwen3-omni-30b-a3b-captioner.json) — 千问3-Omni-30b-a3b-Captioner是一款强大的音频细粒度分析模型，专为在复杂多变的音频场景中生成精准、全面的内容描述而设计，可自动解析并描述从复杂语音、环境声到音乐、影视声效等各类音…
  - 模型：`qwen3-omni-30b-a3b-captioner`
- [一句话识别及翻译V1.0](groups/gummy-chat-v1.json) — 多语言语音转写及翻译的多模态大模型。本模型支持60秒以内的实时语音识别，适用于语音搜索、设备指令等场景。提供10个混合语种的高准确率识别服务，同时支持中英日韩互译，以其他6个语种翻译成中文或英文。
  - 模型：`gummy-chat-v1`
- [语音识别热词](groups/speech-biasing.json) — 热词是指用户可以预先定义的一组特定词汇或短语，这些词汇或短语在识别、翻译过程中会被赋予更高的优先级。针对您的特定业务领域，如果有部分词汇的语音识别、翻译效果不够好，可以将这些关键词或短语添加为热词进行…
  - 模型：`speech-biasing`

## 推理 `Reasoning` — 5 个家族

- [QVQ-Max](groups/qvq-max.json) — 千问QVQ视觉推理模型，支持视觉输入及思维链输出，在数学、编程、视觉分析、创作以及通用任务上都表现了更强的能力。
  - 模型：`qvq-max`
- [Qwen-Plus](groups/qwen-plus.json) — 千问超大规模语言模型的增强版，支持中文英文等不同语言输入。主干模型、latest和快照04-28已升级Qwen3系列，实现思考模式和非思考模式的有效融合，可在对话中切换模式。
  - 模型：`qwen-plus`, `qwen-plus-0112`, `qwen-plus-1220`, `qwen-plus-latest`
- [Qwen-QVQ-Plus](groups/qvq-plus.json) — 千问QVQ视觉推理模型增强版，支持视觉输入及思维链输出，在数学、编程、视觉分析、创作以及通用任务上都表现了更强的能力。
  - 模型：`qvq-plus`
- [Qwen-QwQ-Plus](groups/qwq-plus.json) — 千问QwQ推理模型增强版，基于Qwen2.5模型训练的QwQ推理模型，通过强化学习大幅度提升了模型推理能力。模型数学代码等核心指标（AIME 24/25、livecodebench）以及部分通用指标（…
  - 模型：`qwq-plus`
- [Qwen-Turbo](groups/qwen-turbo.json) — 千问超大规模语言模型，支持中文英文等不同语言输入。主干模型、latest和快照04-28已升级Qwen3系列，实现思考模式和非思考模式的有效融合，可在对话中切换模式。
  - 模型：`qwen-turbo`

## 视觉理解 `VU` — 4 个家族

- [GUI-Plus](groups/gui-plus.json) — GUI系列图形界面交互基础模型，针对手机端与电脑端图形界面理解与交互任务，性能优于开源版同类GUI模型。全面升级跨平台界面理解与多步任务规划，支持跨应用复杂任务；具备精细化动作执行与多角色多智能体协作…
  - 模型：`gui-plus`
- [Qwen-VL-Max](groups/qwen-vl-max.json) — Qwen-VL-Max，即千问超大规模视觉语言模型。相比增强版，再次提升视觉推理能力和指令遵循能力，提供更高的视觉感知和认知水平。在更多复杂任务上提供最佳的性能。
  - 模型：`qwen-vl-max`
- [Qwen-VL-OCR](groups/qwen-vl-ocr.json) — Qwen-VL-OCR，即基于Qwen-VL训练的OCR识别大模型。通过统一模型的方式聚合多种图文识别、解析、处理类任务，提供强大的图文识别能力。
  - 模型：`qwen-vl-ocr`, `qwen-vl-ocr-1028`, `qwen-vl-ocr-latest`
- [Qwen-VL-Plus](groups/qwen-vl-plus.json) — Qwen-VL-Plus，即千问大规模视觉语言模型增强版。大幅提升细节识别能力和文字识别能力，支持超百万像素分辨率和任意长宽比规格的图像。在广泛的视觉任务上提供卓越的性能。
  - 模型：`qwen-vl-plus`

## 实时语音识别 `Realtime-ASR` — 4 个家族

- [Paraformer实时语音识别-8k-v1](groups/paraformer-realtime-8k-v1.json) — Paraformer中文实时语音识别模型，支持8kHz电话客服等场景下的实时语音识别。
  - 模型：`paraformer-realtime-8k-v1`
- [Paraformer实时语音识别-8k-v2](groups/paraformer-realtime-8k-v2.json) — 推荐使用 Paraformer最新实时语音识别模型，支持多个语种自由切换的视频直播、会议等实时场景的语音识别。可以通过language_hints参数选择语种获得更准确的识别效果。支持8kHz电话客服…
  - 模型：`paraformer-realtime-8k-v2`
- [Paraformer实时语音识别-v1](groups/paraformer-realtime-v1.json) — Paraformer中文实时语音识别模型，支持16kHz及以上采样率的视频直播、会议等实时场景下的语音识别。
  - 模型：`paraformer-realtime-v1`
- [Paraformer实时语音识别-v2](groups/paraformer-realtime-v2.json) — 推荐使用 Paraformer最新实时语音识别模型，支持多个语种自由切换的视频直播、会议等实时场景的语音识别。可以通过language_hints参数选择语种获得更准确的识别效果。支持任意采样率。 支…
  - 模型：`paraformer-realtime-v2`

## 语音合成 `TTS` — 2 个家族

- [Qwen-TTS](groups/qwen-tts.json) — 千问系列首个语音合成模型，支持中文、英文、中英混合输入。自适应根据输入文本调整输出语气，音色真实自然，支持输入输出全流式。
  - 模型：`qwen-tts`, `qwen-tts-latest`
- [大模型声音复刻及声音设计](groups/voice-enrollment.json) — 大模型声音复刻服务依托先进的大模型技术进行特征提取，无需训练过程就可以完成声音的复刻。仅需提供极短的音频，即可迅速生成高度相似且听感自然的定制声音。 大模型声音设计使用FunAudioGen-VD模型…
  - 模型：`voice-enrollment`

## 实时音频翻译 `Realtime-Audio-Translate` — 1 个家族

- [实时语音识别及翻译V1.0](groups/gummy-realtime-v1.json) — 多语言语音转写及翻译的多模态大模型。本模型提供长时间、高准确率、实时转写中/英/日/韩等10个混合语种的服务。同时支持中英日韩互译，以其他6个语种翻译成中文或英文。
  - 模型：`gummy-realtime-v1`

## 实时全模态 `Realtime-Omni` — 1 个家族

- [Qwen-Omni-Turbo-Realtime](groups/qwen-omni-turbo-realtime.json) — 千问全新多模态理解生成大模型实时版，适合实时音频交互场景。支持音频伴随文本、图像、视频混合输入理解，具备语音和文本同时流式生成能力，提供了4种自然对话音色。
  - 模型：`qwen-omni-turbo-realtime`, `qwen-omni-turbo-realtime-latest`

## 全模态 `Multimodal-Omni` — 1 个家族

- [Qwen-Omni-Turbo](groups/qwen-omni-turbo.json) — 千问全新多模态理解生成大模型，支持文本, 图像，语音，视频输入理解和混合输入理解，具备文本和语音同时流式生成能力，多模态内容理解速度显著提升，提供了4种自然对话音色。
  - 模型：`qwen-omni-turbo`, `qwen-omni-turbo-latest`
