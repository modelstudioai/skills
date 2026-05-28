# 模型上下架与更新

**模型上架**详见下表，**模型下线**规则及清单请参考[模型下线机制说明](https://help.aliyun.com/zh/model-studio/model-depreciation)。

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型类型**

**时间**

**模型规格**

**功能说明**

推理模型

2026-05-25

qwen3.7-max-preview、qwen3.7-max-2026-05-17

Qwen Max 系列模型。仅支持纯文本输入，仅支持思考模式。

推理模型

2026-05-21

qwen3.7-max、qwen3.7-max-2026-05-20

Qwen Max 系列新一代旗舰模型。仅支持纯文本输入，默认开启思考模式，支持显式缓存，在编程、办公与生产力、长周期自主执行方面均能出色胜任各项任务。

音视频翻译

2026-05-19

qwen3.5-livetranslate-flash-realtime、qwen3.5-livetranslate-flash-realtime-2026-05-19

一款多语言音视频实时翻译模型，可识别 60 种语言，并实时翻译为 29 种语言的音频。[实时语音/音视频翻译-千问](https://help.aliyun.com/zh/model-studio/qwen3-5-livetranslate-flash-realtime)

推理模型

2026-05-19

xiaomi/mimo-v2.5-pro

小米直供的 MiMo-V2.5-Pro 模型，在通用智能体能力、复杂软件工程以及长程任务等方面提升显著。[MiMo-小米](https://help.aliyun.com/zh/model-studio/mimo)

推理模型

2026-05-19

ZHIPU/GLM-5.1、ZHIPU/GLM-5

智谱直供的 glm-5、glm-5.1模型，适用于智能交互、企业应用及开发辅助等场景。[GLM-智谱](https://help.aliyun.com/zh/model-studio/glm-zhipu)

音乐生成

2026-05-06

fun-music-v1

百聆音乐生成大模型（Fun音乐大模型）支持输入开放性歌曲的创作要求或歌词，生成整首男/女声演唱的中文或英文歌曲。歌曲通俗易懂，情绪由浅入深，是人类灵感与大模型能力的完美结合。[音乐生成](https://help.aliyun.com/zh/model-studio/fun-music)

推理模型

2026-04-29

deepseek-v4-pro

deepseek-v4-pro `cached_token` 单价调整为 **1 元/百万 token**，标准 `input_token` 单价不变。详见[上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)。

参考生视频

2026-04-29

vidu/viduq3-mix\_reference2video、vidu/viduq3\_reference2video、vidu/viduq3-turbo\_reference2video

Vidu-参考生视频系列模型，支持传入参考图片和文本提示词，将图片中的主体角色融合到提示词描述的场景中，生成流畅的视频内容。[Vidu-参考生视频](https://help.aliyun.com/zh/model-studio/vidu-reference-to-video-api-reference)

图生视频

2026-04-29

vidu/viduq2-pro-fast\_img2video

Vidu-首帧生视频系列模型，根据输入图像和文本提示词，生成一段流畅的视频。[Vidu-图生视频-基于首帧](https://help.aliyun.com/zh/model-studio/vidu-image-to-video-api-reference)

3D生成

2026-04-29

Tripo/Tripo-H3.1

Tripo 高精度3D生成模型，支持最高200万面，可实现文生3D、单图生3D和多图生3D任务。[Tripo-3D模型生成](https://help.aliyun.com/zh/model-studio/tripo-3d-generation-api-reference)

3D生成

2026-04-29

Tripo/Tripo-P1.0

Tripo 专业3D生成模型，最高2万面，生成速度较快，可实现文生3D、单图生3D和多图生3D任务。[Tripo-3D模型生成](https://help.aliyun.com/zh/model-studio/tripo-3d-generation-api-reference)

文生视频

2026-04-27

happyhorse-1.0-t2v

HappyHorse系列文生视频模型，支持有声视频生成，可生成3~15秒、720P/1080P视频。[HappyHorse-文生视频](https://help.aliyun.com/zh/model-studio/happyhorse-text-to-video-api-reference)

图生视频

2026-04-27

happyhorse-1.0-i2v

HappyHorse系列图生视频模型，支持有声视频生成，可生成3~15秒、720P/1080P视频。[HappyHorse-图生视频-基于首帧](https://help.aliyun.com/zh/model-studio/happyhorse-image-to-video-api-reference)

参考生视频

2026-04-27

happyhorse-1.0-r2v

HappyHorse系列参考生视频模型，支持多参考图输入生成有声视频，可生成3~15秒、720P/1080P视频。[HappyHorse-参考生视频](https://help.aliyun.com/zh/model-studio/happyhorse-reference-to-video-api-reference)

视频编辑

2026-04-27

happyhorse-1.0-video-edit

HappyHorse系列视频编辑模型，支持对视频进行编辑处理。[HappyHorse-视频编辑](https://help.aliyun.com/zh/model-studio/happyhorse-video-edit-api-reference)

文生视频

2026-04-26

wan2.7-t2v-2026-04-25

万相2.7-文生视频模型快照版本，模型能力与wan2.7-t2v一致。[万相2.7-文生视频](https://help.aliyun.com/zh/model-studio/text-to-video-api-reference)

图生视频

2026-04-26

wan2.7-i2v-2026-04-25

万相2.7-图生视频模型快照版本，模型能力与wan2.7-i2v一致。[万相2.7-图生视频](https://help.aliyun.com/zh/model-studio/image-to-video-general-api-reference)

文生文与视觉理解

2026-04-26

kimi/kimi-k2.6

kimi/kimi-k2.6 是 Kimi 最新最智能的模型，月之暗面直供，在通用 Agent、代码、视觉理解等综合能力得到全面提升，同时支持文本、图片与视频输入、思考与非思考模式、对话与 Agent 任务。[Kimi-月之暗面](https://help.aliyun.com/zh/model-studio/kimi-api-by-moonshot-ai)

推理模型

2026-04-24

deepseek-v4-pro、deepseek-v4-flash

DeepSeek-V4系列模型，阿里直供。deepseek-v4-pro为旗舰模型，deepseek-v4-flash为轻量级高速模型。[DeepSeek -阿里云](https://help.aliyun.com/zh/model-studio/deepseek-api)

图像生成

2026-04-23

qwen-image-2.0-pro-2026-04-22

Qwen-Image-2.0系列模型，实现了图片生成和图片编辑的融合。相较于3月3日快照，本模型在画面质感，尤其是纹理细节、光影、材质上有明显跃升；支持多语言的图内文字生成；艺术风格表现更加均衡。[千问-文生图](https://help.aliyun.com/zh/model-studio/qwen-image-api)、[千问-图像编辑](https://help.aliyun.com/zh/model-studio/qwen-image-edit-api)

推理模型

2026-04-23

qwen3.5-plus-2026-04-20

Qwen3.5原生视觉语言系列Plus模型新快照，相较2月15日快照Agentic coding能力大幅提升，推理速度显著提升；知识、推理与长上下文能力保持较高水准，适合编码智能体、生产工作流和高吞吐场景。

推理模型

2026-04-23

qwen3.6-27b

Qwen3.6系列27B原生视觉语言Dense模型，相较3.5-27B重点提升Agentic coding能力，STEM与推理能力进一步增强；视觉模态方面空间智能、物体定位与检测能力显著增强，视频理解、文档OCR及视觉Agent能力稳步提升。

文生文与视觉理解

2026-04-21

kimi-k2.6

Kimi最新最智能的模型，具备更强更稳的长程代码编写能力，指令遵循和自我纠错能力显著提升。同时支持文本、图片与视频输入、思考与非思考模式、对话与 Agent 任务。[Kimi-阿里云](https://help.aliyun.com/zh/model-studio/kimi-api)

推理模型

2026-04-20

qwen3.6-max-preview

Qwen3.6系列规模最大的闭源模型，Coding能力进一步提升、Agent执行更加高效。仅支持纯文本输入，支持思考模式（默认开启），支持显式缓存和Function Calling。[概述](https://help.aliyun.com/zh/model-studio/text-generation)

> 不支持图像与视频输入。

推理模型

2026-04-16

qwen3.6-flash、qwen3.6-flash-2026-04-16、qwen3.6-35b-a3b

Qwen3.6 原生视觉语言 Flash 系列模型，在整体性能上较 Qwen3.5-Flash 显著提升。重点增强了智能体编程能力（在多项代码智能体基准上大幅超越前代）、数学推理和代码推理能力；在视觉能力方面，空间智能显著增强，其中物体定位和目标检测表现尤为突出。[概述](https://help.aliyun.com/zh/model-studio/text-generation)

语音识别

2026-04-16

fun-asr、fun-asr-2025-11-07

Fun-ASR 实时语音识别能力升级：

-   方言支持：覆盖汉语七大方言（官话/吴/湘/赣/客/闽/粤）及 20+ 地区口音
    
-   古诗词优化：提升古诗词识别准确率，适用于文化教育、有声读物等场景
    
-   文本优化：标点预测与文本归一化增强，数字/日期/金额自动转标准格式
    
-   多语种扩展：支持中、英、日、韩、法、德、西班牙等共 30 个语种
    

详情请参见[录音文件识别-Fun-ASR/Paraformer](https://help.aliyun.com/zh/model-studio/recording-file-recognition)

推理模型

2026-04-14

glm-5.1

智谱GLM-5.1模型，专为长程任务设计，支持 200K 上下文，最大输出可达 128K Token。通过强大的逻辑推理、长文本理解及代码生成能力，在多项基准测试中表现优异，适用于智能交互、企业应用及开发辅助等场景。[GLM-阿里云](https://help.aliyun.com/zh/model-studio/glm)

文生文

2026-04-14

vanchin/deepseek-v3.2-think、vanchin/deepseek-v3.1-terminus、vanchin/deepseek-r1、vanchin/deepseek-v3

由快手万擎直供的 DeepSeek 模型推理服务。[DeepSeek-快手万擎](https://help.aliyun.com/zh/model-studio/deepseek-api-by-vanchin)

文字识别

2026-04-14

vanchin/deepseek-ocr

由快手万擎直供的 DeepSeek OCR 模型推理服务。[DeepSeek-快手万擎](https://help.aliyun.com/zh/model-studio/deepseek-api-by-vanchin)

文生视频

2026-04-13

pixverse/pixverse-c1-t2v

爱诗C1-文生视频模型，基于文本提示词生成视频。支持提示词智能分镜，打斗与特效强化升级，支持真人或动漫风格。[爱诗-文生视频](https://help.aliyun.com/zh/model-studio/pixverse-text-to-video-api-reference)

图生视频

2026-04-13

pixverse/pixverse-c1-it2v

爱诗C1-首帧生视频模型，根据输入图像和文本提示词生成视频。支持提示词智能分镜，打斗与特效强化升级，支持真人或动漫风格。[爱诗-图生视频-基于首帧](https://help.aliyun.com/zh/model-studio/pixverse-image-to-video-api-reference)

图生视频

2026-04-13

pixverse/pixverse-c1-kf2v

爱诗C1-首尾帧生视频模型，基于首帧图像、尾帧图像和文本提示词生成平滑过渡的视频。支持提示词智能分镜，打斗与特效强化升级，支持真人或动漫风格。[爱诗-图生视频-基于首尾帧](https://help.aliyun.com/zh/model-studio/pixverse-keyframe-to-video-api-reference)

参考生视频

2026-04-13

pixverse/pixverse-c1-r2v

爱诗C1-参考生视频模型，参考多张图像生成视频。支持将一张多宫格分镜拼接图一键转化为视频。[爱诗-参考生视频](https://help.aliyun.com/zh/model-studio/pixverse-reference-to-video-api-reference)

视频编辑

2026-04-03

wan2.7-videoedit

万相2.7-视频编辑模型，支持指令编辑与视频迁移任务，可修改视频局部或整体画面，同时支持多图参考替换及动作、特效、运镜的复刻。[万相2.7-视频编辑](https://help.aliyun.com/zh/model-studio/wan-video-editing-api-reference)

图生视频

2026-04-03

wan2.7-i2v

万相2.7-图生视频模型，支持多模态输入（文本/图像/音频/视频），可完成首帧生视频、首尾帧生视频、视频续写三大任务。[万相2.7-图生视频](https://help.aliyun.com/zh/model-studio/image-to-video-general-api-reference)

文生视频

2026-04-03

wan2.7-t2v

万相2.7-文生视频模型，新增分辨率档位与宽高比自定义设置，支持灵活适配不同创作场景与平台发布需求。[万相2.7-文生视频](https://help.aliyun.com/zh/model-studio/text-to-video-api-reference)

参考生视频

2026-04-03

wan2.7-r2v

万相2.7参考生视频模型，支持主体参考和音色定制，并可输入单张多宫格故事板直接生成剧本化视频。[万相2.7-参考生视频](https://help.aliyun.com/zh/model-studio/wan-video-to-video-api-reference)

推理模型

2026-04-02

qwen3.6-plus、qwen3.6-plus-2026-04-02

千问3.6-Plus，代码开发能力重点升级（Agentic Coding、前端编程等），Vibe Coding体验显著提升；泛化场景推理能力进一步增强；多模态方面，万物识别、OCR、物体定位等能力显著提升；同时修复了Qwen3.5-Plus上线后的已知问题。使用方法与qwen3.5-plus一致。[概述](https://help.aliyun.com/zh/model-studio/text-generation)

图像生成与编辑

2026-04-01

wan2.7-image-pro、wan2.7-image

万相2.7-图像生成与编辑模型，支持文生图、文生组图、图生组图、图像编辑、多图参考生成、交互式编辑，在文字渲染、主体一致性、复杂指令遵循表现更优。Pro系列支持4K输出；加速版兼顾效果与响应速度。[万相-图像生成与编辑2.7](https://help.aliyun.com/zh/model-studio/wan-image-generation-and-editing-api-reference)

全模态

2026-03-30

qwen3.5-omni-plus、qwen3.5-omni-plus-2026-03-15、qwen3.5-omni-flash、qwen3.5-omni-flash-2026-03-15

最新一代全模态大模型，支持长视频分析、会议纪要、字幕输出、安全审核、音视频交互；支持音视频内容的深度理解与生成描述，支持 113 种语言识别和 36 种语言的音频生成，可处理 3 小时音频及1 小时视频输入，支持联网搜索及指令来控制输出音频的音量、语速、情绪。[非实时（Qwen-Omni）](https://help.aliyun.com/zh/model-studio/qwen-omni)

全模态

2026-03-30

qwen3.5-omni-plus-realtime、qwen3.5-omni-plus-realtime-2026-03-15、qwen3.5-omni-flash-realtime、qwen3.5-omni-flash-realtime-2026-03-15

千问最新推出的实时多模态模型，相比于上一代的 Qwen3-Omni-Flash-Realtime：模型智力大幅提升，与 Qwen3.5-Plus 智能水平相当。原生支持联网搜索（WebSearch），支持语音打断和控制；支持 113 种语种和方言的语音识别，以及 36 种语种和方言的语音生成。[实时（Qwen-Omni-Realtime）](https://help.aliyun.com/zh/model-studio/realtime)

文生视频

2026-03-29

pixverse/pixverse-v6-t2v

爱诗v6-文生视频模型，基于文本提示词，生成一段流畅的视频。[爱诗-文生视频](https://help.aliyun.com/zh/model-studio/pixverse-text-to-video-api-reference)

图生视频

2026-03-29

pixverse/pixverse-v6-it2v

爱诗v6-首帧生视频模型，根据输入图像和文本提示词，生成一段流畅的视频。[爱诗-图生视频-基于首帧](https://help.aliyun.com/zh/model-studio/pixverse-image-to-video-api-reference)

图生视频

2026-03-29

pixverse/pixverse-v6-kf2v

爱诗v6-首尾帧生视频模型，基于首帧图像、尾帧图像和文本提示词，生成一段平滑过渡的视频。[爱诗-图生视频-基于首尾帧](https://help.aliyun.com/zh/model-studio/pixverse-keyframe-to-video-api-reference)

文生视频

2026-03-27

vidu/viduq3-pro\_text2video、vidu/viduq3-turbo\_text2video、vidu/viduq2\_text2video

Vidu-文生视频系列模型。基于文本提示词，生成一段流畅的视频。[Vidu-文生视频](https://help.aliyun.com/zh/model-studio/vidu-text-to-video-api-reference)

图生视频

2026-03-27

vidu/viduq3-pro\_img2video、vidu/viduq3-turbo\_img2video、vidu/viduq2-pro\_img2video、vidu/viduq2-turbo\_img2video

Vidu-首帧生视频系列模型，根据输入图像和文本提示词，生成一段流畅的视频。[Vidu-图生视频-基于首帧](https://help.aliyun.com/zh/model-studio/vidu-image-to-video-api-reference)

首尾帧生视频

2026-03-27

vidu/viduq3-pro\_start-end2video、vidu/viduq3-turbo\_start-end2video、vidu/viduq2-pro\_start-end2video、vidu/viduq2-turbo\_start-end2video

Vidu-首尾帧生视频系列模型，基于首帧图像、尾帧图像和文本提示词，生成一段平滑过渡的视频。[Vidu-图生视频-基于首尾帧](https://help.aliyun.com/zh/model-studio/vidu-keyframe-to-video-api-reference)

参考生视频

2026-03-27

vidu/viduq2-pro\_reference2video、vidu/viduq2\_reference2video

Vidu-参考生视频系列模型，支持传入参考图片和文本提示词，将图片中的主体角色融合到提示词描述的场景中，生成流畅的视频内容。[Vidu-参考生视频](https://help.aliyun.com/zh/model-studio/vidu-reference-to-video-api-reference)

图像生成

2026-03-24

kling/kling-v3-image-generation、kling/kling-v3-omni-image-generation

可灵V3图像生成系列模型，支持文生图、参考图生图两种任务。[可灵-图像生成](https://help.aliyun.com/zh/model-studio/kling-image-generation-api-reference)

视频生成

2026-03-24

kling/kling-v3-video-generation、kling/kling-v3-omni-video-generation

可灵V3视频生成系列模型，支持文生视频、图生视频-基于首帧、图生视频-基于首尾帧、参考生视频以及视频编辑。[可灵-视频生成](https://help.aliyun.com/zh/model-studio/kling-video-generation-api-reference/)

参考生视频

2026-03-20

pixverse/pixverse-v5.6-r2v

参考多张图像生视频。[爱诗-参考生视频](https://help.aliyun.com/zh/model-studio/pixverse-reference-to-video-api-reference)

图生视频

2026-03-20

pixverse/pixverse-v5.6-kf2v

基于首帧和尾帧生视频。[爱诗-图生视频-基于首尾帧](https://help.aliyun.com/zh/model-studio/pixverse-keyframe-to-video-api-reference)

图生视频

2026-03-20

pixverse/pixverse-v5.6-it2v

基于首帧生视频。[爱诗-图生视频-基于首帧](https://help.aliyun.com/zh/model-studio/pixverse-image-to-video-api-reference)

文生视频

2026-03-20

pixverse/pixverse-v5.6-t2v

文生视频系列模型。[爱诗-文生视频](https://help.aliyun.com/zh/model-studio/pixverse-text-to-video-api-reference)

多模态向量

2026-03-19

tongyi-embedding-vision-plus-2026-03-06、tongyi-embedding-vision-flash-2026-03-06

相较于 tongyi-embedding-vision 主线模型，tongyi-embedding-vision-plus-2026-03-06 / flash-2026-03-06 视觉向量化能力全面升级，基于 Qwen3 底座，支持多分辨率（0-3 档可调）、多维度（Plus 64-1152 维 / Flash 64-768 维）、30+ 语言，以及文本/图片/视频融合向量化，IPC/自驾/电商/视频营销等场景图像搜索效果大幅提升。

界面交互

2026-03-18

gui-plus-2026-02-26

相较于`gui-plus`，`gui-plus-2026-02-26`模型能力全面升级，支持思考与非思考模式，模型在处理跨平台、多 APP 任务的效果上得到大幅提升。[界面交互](https://help.aliyun.com/zh/model-studio/gui-automation)

语音识别

2026-03-05

fun-asr-realtime-2026-02-28

Fun-ASR实时语音识别新增快照模型，较 fun-asr-realtime-2025-11-07 效果更优。[实时语音识别-Fun-ASR/Paraformer](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition)

图像生成与编辑

2026-03-03

qwen-image-2.0、qwen-image-2.0-2026-03-03、qwen-image-2.0-pro、qwen-image-2.0-pro-2026-03-03

千问-Image2.0系列，同时支持图像生成和编辑。Pro系列文字渲染、真实质感、语义遵循能力更强；加速版兼顾效果与响应速度。[千问-文生图](https://help.aliyun.com/zh/model-studio/qwen-image-api)、[千问-图像编辑](https://help.aliyun.com/zh/model-studio/qwen-image-edit-api)

语音识别

2026-03-03

qwen3-asr-flash-2026-02-10

千问录音文件识别新增快照模型，较 qwen3-asr-flash-2025-09-08 效果更优。[非实时语音识别](https://help.aliyun.com/zh/model-studio/non-realtime-speech-recognition-user-guide)

语音合成

2026-03-02

cosyvoice-v3.5-plus、cosyvoice-v3.5-flash

CosyVoice3.5 模型上线，专注声音复刻与设计，支持指令控制语音合成效果。[实时语音合成-CosyVoice /Sambert](https://help.aliyun.com/zh/model-studio/text-to-speech)

推理模型

2026-02-24

MiniMax-M2.5

稀宇科技（MiniMax）推出的新模型，响应速度快，擅长编程、办公等任务。[使用方法](https://help.aliyun.com/zh/model-studio/minimax-api)

推理模型

2026-02-24

qwen3.5-flash、qwen3.5-flash-2026-02-23、qwen3.5-122b-a10b、qwen3.5-27b、qwen3.5-35b-a3b

阿里巴巴推出的最新模型千问3.5-Flash和开源模型，支持文本、图像和视频输入，响应速度快，综合表现接近qwen3.5-plus，支持内置[工具调用](https://help.aliyun.com/zh/model-studio/tool-calls/)。[概述](https://help.aliyun.com/zh/model-studio/text-generation)

代码模型

2026-02-20

qwen3-coder-next

Qwen3系列新一代开源代码生成模型，支持多轮工具交互，提升了对仓库级别代码的理解能力和对AI编程工具的适配性。[代码能力（Qwen-Coder）](https://help.aliyun.com/zh/model-studio/qwen-coder)

推理模型

2026-02-18

glm-5

智谱推出的最新模型，专为编程与智能体场景打造，擅长复杂的系统工程与长程Agent任务。[GLM-阿里云](https://help.aliyun.com/zh/model-studio/glm)

推理模型

2026-02-16

qwen3.5-plus、qwen3.5-plus-2026-02-15、qwen3.5-397b-a17b

阿里巴巴推出的最新模型千问3.5-Plus和开源模型，支持文本、图像和视频输入，在语言理解、逻辑推理、代码生成、智能体任务、图像理解、视频理解、图形用户界面（GUI）等多种任务中表现卓越，支持内置[工具调用](https://help.aliyun.com/zh/model-studio/tool-calls/)。[概述](https://help.aliyun.com/zh/model-studio/text-generation)

语音识别

2026-02-13

qwen3-asr-flash-realtime-2026-02-10

千问实时语音识别新增最新快照模型，较 qwen3-asr-flash-realtime-2025-10-27 效果更优。[实时语音识别](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition-user-guide)

语音识别

2026-02-12

fun-asr-flash-8k-realtime、fun-asr-flash-8k-realtime-2026-01-28

新增基于Fun-ASR大模型架构的小尺寸ASR模型，专为8kHz场景优化，适合对成本敏感的客户。[实时语音识别-Fun-ASR/Paraformer](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition)

语音合成

2026-02-10

qwen3-tts-instruct-flash、qwen3-tts-instruct-flash-2026-01-26

千问语音合成上线Instruct（指令控制）模型，支持通过自然语言指令精准控制合成效果。[非实时语音合成](https://help.aliyun.com/zh/model-studio/non-realtime-tts-user-guide)

语音合成

2026-02-10

qwen3-tts-vd-2026-01-26

千问语音合成上线声音设计模型，可通过文本描述创建定制化音色。[非实时语音合成](https://help.aliyun.com/zh/model-studio/non-realtime-tts-user-guide)

语音合成

2026-02-10

qwen3-tts-vc-2026-01-22

千问语音合成上线声音复刻模型，可基于真实音频样本快速复刻音色。[非实时语音合成](https://help.aliyun.com/zh/model-studio/non-realtime-tts-user-guide)

语音合成

2026-02-04

qwen3-tts-instruct-flash-realtime、qwen3-tts-instruct-flash-realtime-2026-01-22

千问实时语音合成新增Instruct（指令控制）模型，支持通过自然语言指令精准控制合成效果。[实时语音合成](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide)

参考生视频

2026-02-02

wan2.6-r2v-flash

基于参考视频和图像的角色形象，生成多镜头视频，支持自动配音。[万相2.7-参考生视频](https://help.aliyun.com/zh/model-studio/wan-video-to-video-api-reference)

文生文与视觉理解

2026-01-30

kimi-k2.5

由月之暗面（Moonshot AI）公司推出的视觉理解模型，在代码生成、视觉理解等通用智能任务中表现突出。同时支持图像、视频与文本输入、对话与 Agent 任务。[Kimi-阿里云](https://help.aliyun.com/zh/model-studio/kimi-api)

文生文

2026-01-29

tongyi-xiaomi-analysis-flash、tongyi-xiaomi-analysis-pro

通义晓蜜对话分析专注于对话信息抽取、场景分类、满意度判定等分析需求，擅长处理复杂业务逻辑的质检规则，支持自定义分析标准，具备强大的多轮对话理解和语义推理能力。[对话分析（Tongyi-Xiaomi-Analysis）](https://help.aliyun.com/zh/model-studio/dialogue-analysis)

语音识别

2026-01-28

qwen3-asr-flash-filetrans、qwen3-asr-flash-filetrans-2025-11-17

千问3-ASR-Flash-Filetrans系列模型现已支持词级别时间戳，通过设置新参数 `enable_words`，获取毫秒级的词/字对齐信息，并体验更符合语义的精细化断句。[非实时语音识别](https://help.aliyun.com/zh/model-studio/non-realtime-speech-recognition-user-guide)

推理模型

2026-01-27

qwen3-max-2026-01-23

相较于 2025 年 9 月 23 日的快照版本，有效融合了思考模式与非思考模式，显著提升了模型的整体性能。在思考模式下，模型集成了 Web 搜索、网页信息提取和代码解释器三项工具，通过在思考过程中引入外部工具，在复杂问题上实现更高的准确率。[OpenAI兼容-Responses](https://help.aliyun.com/zh/model-studio/compatibility-with-openai-responses-api)

推理模型

2026-01-27

MiniMax-M2.1

MiniMax-M2.1是MiniMax推出的旗舰级开源大模型，聚焦真实世界复杂任务，其核心优势在于多语言编程能力以及作为Agent解决复杂任务的能力。[使用方法](https://help.aliyun.com/zh/model-studio/minimax-api)

视觉理解

2026-01-23

qwen3-vl-flash-2026-01-22

千问VL的全新快照版模型，有效融合了思考模式与非思考模式，相较于 2025 年 10 月 15 日的快照版本，显著提升了模型的整体性能，在通用视觉识别、安防、巡店、巡检、拍照解题等业务场景中实现了更高准确率的推理。[图像与视频理解](https://help.aliyun.com/zh/model-studio/vision)

图生视频

2026-01-17

wan2.6-i2v-flash

支持生成有声与无声视频，两类视频按各自计费规则独立计费；同时具备多镜头叙事能力与音频处理能力。[万相-图生视频-基于首帧（2.1-2.6）](https://help.aliyun.com/zh/model-studio/legacy-image-to-video-api-reference/)

图像编辑

2026-01-17

qwen-image-edit-max、qwen-image-edit-max-2026-01-16

千问图像编辑模型Max系列，具备更稳定、丰富的编辑能力，增强了工业设计与几何推理能力，并提升了角色一致性与编辑的精准度。[图像编辑-千问](https://help.aliyun.com/zh/model-studio/qwen-image-edit-guide)

语音合成

2026-01-16

qwen3-tts-vc-realtime-2026-01-15

千问实时语音合成新增最新快照模型，[声音复刻（Qwen）](https://help.aliyun.com/zh/model-studio/qwen-tts-voice-cloning)效果进一步优化，较 qwen3-tts-vc-realtime-2025-11-27 更自然、更贴近原声。[实时语音合成](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide)

文生图

2026-01-12

qwen-image-plus-2026-01-09

千问图像生成的全新快照版模型，为qwen-image-max的蒸馏加速版，支持快速生成高质量图像。[千问-文生图](https://help.aliyun.com/zh/model-studio/qwen-image-api)

推理模型

2026-01-12

deepseek-v3.2

deepseek-v3.2 模型支持隐式缓存与显式缓存，可提升响应速度，并在不影响回复效果的前提下降低使用成本。[上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)

语音识别

2026-01-06

qwen3-asr-flash、qwen3-asr-flash-2025-09-08

千问3-ASR-Flash支持OpenAI兼容模式。[非实时语音识别](https://help.aliyun.com/zh/model-studio/non-realtime-speech-recognition-user-guide)

语音合成

2026-01-05

cosyvoice-v3-flash

语音合成CosyVoice新增24个音色（详情请参见[音色列表](https://help.aliyun.com/zh/model-studio/cosyvoice-voice-list)）：

-   方言：龙嘉怡、龙老铁
    
-   出海营销：loongkyong、loongtomoka
    
-   诗词朗诵：龙飞
    
-   语音助手：龙小淳、龙小夏、YUMI
    
-   社交陪伴：龙橙、龙泽、龙哲、龙颜、龙星、龙天、龙婉、龙嫱、龙菲菲、龙浩
    
-   有声书：龙三叔、龙媛、龙悦、龙修、龙楠
    
-   新闻播报：龙书
    

文生图

2025-12-31

qwen-image-max、qwen-image-max-2025-12-30

千问图像生成模型Max系列，相较于Plus系列提升了图像的真实感与自然度，有效降低了AI合成痕迹，在人物质感、纹理细节和文字渲染等方面表现突出。[千问-文生图](https://help.aliyun.com/zh/model-studio/qwen-image-api)

推理模型

2025-12-29

glm-4.7

智谱最新旗舰模型，编程能力更强，多步骤推理与执行更稳定。模型总参数达355B，支持复杂任务的分步规划、代码生成与工具协同；问答流畅，写作沉浸感强，创意角色扮演表现突出。[GLM-阿里云](https://help.aliyun.com/zh/model-studio/glm)

图像编辑

2025-12-23

qwen-image-edit-plus-2025-12-15

千问图像编辑发布的最新快照模型，相较于上一版本提升了角色一致性、工业设计能力和几何推理能力，并优化了编辑后的图片与原图在空间布局、纹理和风格上的匹配度，编辑效果更精准。[图像编辑-千问](https://help.aliyun.com/zh/model-studio/qwen-image-edit-guide)

文生图

2025-12-19

z-image-turbo

轻量级文生图模型，可快速生成高质量图像，支持中英双语渲染、复杂语义理解和多风格题材，并可灵活适配多种分辨率与宽高比。[文生图Z-Image](https://help.aliyun.com/zh/model-studio/z-image-api-reference)

视觉理解

2025-12-19

qwen3-vl-plus-2025-12-19

千问VL的全新快照版模型，指令遵循能力更强，具有更低的延迟。[图像与视频理解](https://help.aliyun.com/zh/model-studio/vision)

语音识别

2025-12-19

qwen3-asr-flash-filetrans、qwen3-asr-flash-filetrans-2025-11-17、qwen3-asr-flash、qwen3-asr-flash-2025-09-08

新增捷克语、丹麦语等共 9 种语言的语音识别支持。[非实时语音识别](https://help.aliyun.com/zh/model-studio/non-realtime-speech-recognition-user-guide)

语音识别

2025-12-17

qwen3-asr-flash-realtime、qwen3-asr-flash-realtime-2025-10-27

新增捷克语、丹麦语等共 9 种语言的语音识别支持。[实时语音识别](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition-user-guide)

语音识别

2025-12-17

qwen3-asr-flash、qwen3-asr-flash-2025-09-08

支持任意采样率和声道的音频。[非实时语音识别](https://help.aliyun.com/zh/model-studio/non-realtime-speech-recognition-user-guide)

语音识别

2025-12-17

fun-asr-mtl、fun-asr-mtl-2025-08-25

支持对中、英、日、韩等共 31 种语言的语音识别，尤其适合东南亚出海场景。[录音文件识别-Fun-ASR/Paraformer](https://help.aliyun.com/zh/model-studio/recording-file-recognition)

文生图

2025-12-16

wan2.6-t2i

新增同步接口。支持在总像素面积与宽高比约束内，自由选尺寸。[万相-文生图V2](https://help.aliyun.com/zh/model-studio/text-to-image-v2-api-reference)

图像生成与编辑

2025-12-16

wan2.6-image

支持图像编辑和图文混合输出。[万相-图像生成与编辑2.6](https://help.aliyun.com/zh/model-studio/wan-image-generation-api-reference)

图生视频-基于首帧

2025-12-16

wan2.6-i2v

新增多镜头叙事能力，支持音频能力，支持自动配音，或传入自定义音频文件。[万相-图生视频-基于首帧（2.1-2.6）](https://help.aliyun.com/zh/model-studio/legacy-image-to-video-api-reference/)

参考生视频

2025-12-16

wan2.6-r2v

基于参考视频的角色形象和音色，生成多镜头视频，支持自动配音。[万相2.7-参考生视频](https://help.aliyun.com/zh/model-studio/wan-video-to-video-api-reference)

文生视频

2025-12-16

wan2.6-t2v

新增多镜头叙事能力，支持音频能力，支持自动配音，或传入自定义音频文件。[文生视频](https://help.aliyun.com/zh/model-studio/text-to-video-api-reference)

声音设计

2025-12-16

qwen-voice-design

千问发布声音设计模型，通过文本描述生成定制化音色。结合qwen3-tts-vd-realtime-2025-12-16模型使用生成语音，覆盖 10 种语言。[声音设计（Qwen）](https://help.aliyun.com/zh/model-studio/qwen-tts-voice-design)

语音合成

2025-12-16

qwen3-tts-vd-realtime-2025-12-16（快照版）

千问实时语音合成发布全新快照版模型，可使用[声音设计（Qwen）](https://help.aliyun.com/zh/model-studio/qwen-tts-voice-design)生成的音色进行低延迟、高稳定性的实时合成；支持多语言输出；能根据文本自动调节语气，并优化复杂文本的合成表现。[实时语音合成](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide)

语音识别

2025-12-12

fun-asr、fun-asr-2025-11-07

录音文件识别-Fun-ASR功能更新：

-   支持歌唱识别，能实现整首歌曲的转写，详情请参见[录音文件识别-Fun-ASR/Paraformer](https://help.aliyun.com/zh/model-studio/recording-file-recognition)。
    

语音合成

2025-12-11

cosyvoice-v3-flash、cosyvoice-v3-plus

CosyVoice模型音色更新：

-   cosyvoice-v3-flash模型新增5个系统音色：longanrou\_v3、longyingjing\_v3、longyingling\_v3、longanling\_v3和longhan\_v3，均支持时间戳与SSML功能，详情请参见[音色列表](https://help.aliyun.com/zh/model-studio/cosyvoice-voice-list)。
    
-   cosyvoice-v3-flash和cosyvoice-v3-plus模型的复刻音色功能增强：支持时间戳与SSML功能，韵律效果提升。请参见[CosyVoice声音复刻/设计API](https://help.aliyun.com/zh/model-studio/cosyvoice-clone-design-api)创建新音色体验。
    

全模态

2025-12-04

qwen3-omni-flash-2025-12-01

千问Omni发布的最新快照模型，支持的音色增加至49种，模型的指令跟随能力大幅升级，能高效理解文本、图像、音频、视频。[非实时（Qwen-Omni）](https://help.aliyun.com/zh/model-studio/qwen-omni)

实时多模态

2025-12-04

qwen3-omni-flash-realtime**\-**2025-12-01

千问Omni 实时版发布的最新快照模型，提供了低延迟的多模态交互能力，支持的音色增加至49种，模型的指令跟随能力和交互体验大幅升级。[实时（Qwen-Omni-Realtime）](https://help.aliyun.com/zh/model-studio/realtime)

语音翻译

2025-12-04

qwen3-livetranslate-flash、qwen3-livetranslate-flash-2025-12-01

千问3-LiveTranslate-Flash 是音视频翻译模型，支持 18 种语言（包括中文、英文、俄文、法文等）互译，可结合视觉上下文提升翻译准确性，并输出文本与语音。[音视频文件翻译-千问](https://help.aliyun.com/zh/model-studio/qwen3-livetranslate-flash)

推理模型

2025-12-04

deepseek-v3.2

DeepSeek-V3.2是引入DeepSeek Sparse Attention（一种稀疏注意力机制）的正式版模型，也是DeepSeek推出的首个将思考融入工具使用的模型，同时支持思考模式与非思考模式的工具调用。

[DeepSeek -阿里云](https://help.aliyun.com/zh/model-studio/deepseek-api)

多语言翻译

2025-11-28

qwen-mt-lite

千问基础级文本翻译大模型，支持31个语种互译，相较于qwen-mt-flash响应更快，成本更低，适用于等对延迟敏感的场景。[翻译能力（Qwen-MT）](https://help.aliyun.com/zh/model-studio/machine-translation)

声音复刻

2025-11-27

qwen-voice-enrollment

千问发布声音复刻模型，仅需 5 秒以上音频即可快速生成高相似度声音。结合qwen3-tts-vc-realtime-2025-11-27模型使用，可高保真复刻并实时输出某人的声音，覆盖 11 种语言。[声音复刻（Qwen）](https://help.aliyun.com/zh/model-studio/qwen-tts-voice-cloning)

语音合成

2025-11-27

qwen3-tts-vc-realtime-2025-11-27（快照版）

千问实时语音合成发布全新快照版模型，可使用[声音复刻（Qwen）](https://help.aliyun.com/zh/model-studio/qwen-tts-voice-cloning)生成的音色进行低延迟、高稳定性的实时合成；支持多语言输出；能根据文本自动调节语气，并优化复杂文本的合成表现。[实时语音合成](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide)

语音合成

2025-11-27

qwen3-tts-flash-realtime-2025-11-27（快照版）

千问实时语音合成发布全新快照版模型，低延迟且稳定性高；音色更丰富，同一音色支持多语言输出；能根据文本自动调节语气，并提升复杂文本的合成表现。[实时语音合成](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide)

语音合成

2025-11-27

qwen3-tts-flash-2025-11-27（快照版）

千问语音合成发布全新快照版模型，音色更丰富；同一音色支持多语言输出；可自适应文本调节语气，并优化复杂文本的合成能力。[非实时语音合成](https://help.aliyun.com/zh/model-studio/non-realtime-tts-user-guide)

文字提取

2025-11-21

qwen-vl-ocr-2025-11-20（快照版）

千问文字提取模型，该快照版基于Qwen3-VL架构，大幅提升文档解析、文字定位能力。[文字提取](https://help.aliyun.com/zh/model-studio/qwen-vl-ocr)

语音识别

2025-11-20

qwen3-asr-flash-filetrans、qwen3-asr-flash-filetrans-2025-11-17（快照版）

千问录音文件识别发布了新模型，专为音频文件的异步转写设计，支持最长12小时录音。[非实时语音识别](https://help.aliyun.com/zh/model-studio/non-realtime-speech-recognition-user-guide)

界面交互

2025-11-20

gui-plus

GUI-Plus 可基于屏幕截图和自然语言指令来解析用户意图，并转换为标准化的图像用户界面（GUI）操作（如点击、输入、滚动等），供外部系统决策或执行。相较于千问VL系列模型，提升了GUI操作的准确性。[界面交互](https://help.aliyun.com/zh/model-studio/gui-automation)

语音识别

2025-11-19

fun-asr-realtime-2025-11-07（快照版）

Fun-ASR实时语音识别发布了全新快照版模型，优化远场语音活动检测（VAD）以提升识别准确率与稳定性，并在原有中英文识别基础上新增支持中文多地方言及日语。[实时语音识别-Fun-ASR/Paraformer](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition)

语音识别

2025-11-19

fun-asr-2025-11-07（快照版）

Fun-ASR录音文件识别发布了全新快照版模型，优化远场语音活动检测（VAD）以提升识别准确率与稳定性，并在原有中英文识别基础上新增支持中文多地方言及日语。[录音文件识别-Fun-ASR/Paraformer](https://help.aliyun.com/zh/model-studio/recording-file-recognition)

语音合成

2025-11-19

cosyvoice-v3-flash

较之前版本提升了发音准确性、音色相似度，并且增加了更多小语种支持（德、西、法、意、俄）。[实时语音合成-CosyVoice /Sambert](https://help.aliyun.com/zh/model-studio/text-to-speech)

推理模型

2025-11-11

kimi-k2-thinking

由月之暗面（Moonshot AI）公司推出的思考模型，具有通用智能体能力和推理能力，擅长深度推理，并能通过多步工具调用解决各类难题。[Kimi-阿里云](https://help.aliyun.com/zh/model-studio/kimi-api)

多语言翻译

2025-11-10

qwen-mt-flash

相较于qwen-mt-turbo支持流式增量输出，整体性能表现有所提升。[翻译能力（Qwen-MT）](https://help.aliyun.com/zh/model-studio/machine-translation)

推理模型

2025-11-03

qwen3-max-preview

qwen3-max-preview 模型的思考模式：在整体推理能力上显著提升，尤其在智能体编程、常识推理，以及数学、科学和通用任务方面表现更优。[深度思考](https://help.aliyun.com/zh/model-studio/deep-thinking)

图像编辑

2025-10-31

qwen-image-edit-plus、qwen-image-edit-plus-2025-10-30

在qwen-image-edit的基础上优化了推理性能与系统稳定性，大幅缩短图像生成与编辑的响应时间，且支持单次请求返回多张图片。[图像编辑-千问](https://help.aliyun.com/zh/model-studio/qwen-image-edit-guide)

实时语音识别

2025-10-27

qwen3-asr-flash-realtime、qwen3-asr-flash-realtime-2025-10-27

千问实时语音识别大模型具备自动语种识别功能，可识别 11 种语音类型，并能在复杂音频环境下较为准确地转录。[实时语音识别](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition-user-guide)

视觉理解

2025-10-21

qwen3-vl-32b-thinking、qwen3-vl-32b-instruct

Qwen3-VL系列 32B 的Dense模型，文档识别与理解、空间感知与万物识别能力、视觉2D检测与空间推理能力均表现出色，适合通用场景下的复杂感知任务。[图像与视频理解](https://help.aliyun.com/zh/model-studio/vision)

推理模型

2025-10-21

glm-4.6

GLM新一代旗舰模型，核心能力较glm-4.5全面提升。总参数量为3550 亿，激活参数320亿，上下文窗口扩展至200K。[GLM-阿里云](https://help.aliyun.com/zh/model-studio/glm)

视觉理解

2025-10-16

qwen3-vl-flash、qwen3-vl-flash-2025-10-15

Qwen3系列小尺寸视觉理解模型，实现思考模式和非思考模式的有效融合，相较于开源版Qwen3-VL-30B-A3B，效果更优，响应速度更快。[图像与视频理解](https://help.aliyun.com/zh/model-studio/vision)

视觉理解

2025-10-14

qwen3-vl-8b-thinking、qwen3-vl-8b-instruct

Qwen3-VL系列 8B 的Dense模型，占用显存更低，能够完成多模态理解与推理；支持长视频长文档等超长上下文、视觉2D/3D定位；全面空间感知与万物识别能力。[图像与视频理解](https://help.aliyun.com/zh/model-studio/vision)

视觉理解

2025-10-03

qwen3-vl-30b-a3b-thinking、qwen3-vl-30b-a3b-instruct

基于Qwen3-VL新一代开源模型，响应速度快，具备更强多模态理解与推理、视觉智能体、长视频长文档等超长上下文支持能力；全面升级空间感知与万物识别能力，胜任复杂现实任务。[图像与视频理解](https://help.aliyun.com/zh/model-studio/vision)

推理模型

2025-09-30

deepseek-v3.2-exp

混合推理架构模型，同时支持思考模式与非思考模式，引入稀疏注意力机制，旨在提升处理长文本时的训练与推理效率，价格低于 deepseek-v3.1。详情参见[DeepSeek -阿里云](https://help.aliyun.com/zh/model-studio/deepseek-api)。

图生视频

2025-09-23

wan2.5-i2v-preview

新增音频能力，支持自动配音，或传入自定义音频文件，实现音画同步。[图生视频-基于首帧](https://help.aliyun.com/zh/model-studio/legacy-image-to-video-api-reference/)

文生视频

2025-09-23

wan2.5-t2v-preview

新增音频能力，支持自动配音，或传入自定义音频文件，实现音画同步。[文生视频](https://help.aliyun.com/zh/model-studio/text-to-video-api-reference)

图像编辑

2025-09-23

wan2.5-i2i-preview

支持输入文本、单图或多图实现基于主体一致性的图像编辑、多图融合和组图生成。[通用图像编辑2.5](https://help.aliyun.com/zh/model-studio/wan2-5-image-edit-api-reference)

文生图

2025-09-23

wan2.5-t2i-preview

取消单边限制，在总像素面积与宽高比约束内，自由选尺寸。[文生图V2](https://help.aliyun.com/zh/model-studio/text-to-image-v2-api-reference)

视觉理解

2025-09-23

qwen3-vl-plus、qwen3-vl-plus-2025-09-23、qwen3-vl-235b-a22b-thinking、qwen3-vl-235b-a22b-instruct

Qwen3系列视觉理解模型，实现思考模式和非思考模式的有效融合，视觉智能体能力达到世界顶尖水平。此版本在视觉编码、空间感知、多模态思考等方向全面升级；视觉感知与识别能力大幅提升。[图像与视频理解](https://help.aliyun.com/zh/model-studio/vision)

文生文

2025-09-23

qwen3-max、qwen3-max-2025-09-23

相较qwen3-max-preview版本，在智能体编程与工具调用方向进行了专项升级。本次发布的正式版模型达到领域SOTA水平，适配场景更加复杂的智能体需求。模型列表

音视频翻译

2025-09-23

qwen3-livetranslate-flash-realtime-2025-09-22

qwen3-livetranslate-flash-realtime 是一款多语言音视频实时翻译模型，可识别 18 种语言，并实时翻译为 10 种语言的音频。[实时语音/音视频翻译-千问](https://help.aliyun.com/zh/model-studio/qwen3-5-livetranslate-flash-realtime)

文生图

2025-09-23

qwen-image-plus

在复杂文本渲染方面表现突出，特别是中英文文本渲染，可实现复杂的图文混合布局，相较于qwen-image更具价格优势。[文生图（Qwen-Image)](https://help.aliyun.com/zh/model-studio/qwen-image-api)

代码模型

2025-09-23

qwen3-coder-plus-2025-09-23

基于 Qwen3 的代码生成模型，相较上一版本（7月22日快照）在下游任务效果和工具调用方面鲁棒性有所提升，代码安全性增强。[代码能力（Qwen-Coder）](https://help.aliyun.com/zh/model-studio/qwen-coder)

多模态向量

2025-09-23

tongyi-embedding-vision-plus、tongyi-embedding-vision-flash

以Qwen系列大语言模型为基座构建，围绕视觉向量化能力进行增强训练，支持文字、图像、视频三种模态。[文本与多模态向量化](https://help.aliyun.com/zh/model-studio/embedding)

语音识别

2025-09-23

fun-asr-realtime、fun-asr-realtime-2025-09-15

集成了创新的 RAG 技术，支持大规模热词自定义、ITN 规范化、标点预测等多维功能，显著提升了整体识别准确率和语境贴合度，同时支持中英文自由切换，具备更强的噪声鲁棒性，适应多样复杂环境。[实时语音识别-Fun-ASR/Paraformer](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition)

实时语音合成

2025-09-22

qwen3-tts-flash-realtime、qwen3-tts-flash-realtime-2025-09-18

千问最新的实时语音合成大模型，不仅拥有17种高表现力的拟人音色，且能低延迟高稳定地合成音频；同时支持多种语言、方言。[实时语音合成](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide)

语音合成

2025-09-22

qwen3-tts-flash、qwen3-tts-flash-2025-09-18

千问最新的离线语音合成大模型，不仅拥有17种高表现力的拟人音色，且能低延迟高稳定地合成音频；同时支持多种语言、方言。[非实时语音合成](https://help.aliyun.com/zh/model-studio/non-realtime-tts-user-guide)

实时全模态

2025-09-22

qwen3-omni-flash-realtime、qwen3-omni-flash-realtime-2025-09-15

Qwen3系列多模态大模型的实时版，提供了低延迟的多模态交互能力，支持音频的流式输入，支持输出文本和音频，同时支持多种音色和语言。[实时（Qwen-Omni-Realtime）](https://help.aliyun.com/zh/model-studio/realtime)

全模态

2025-09-22

qwen3-omni-flash、qwen3-omni-flash-2025-09-15

Qwen3系列多模态模型，能高效理解文本、图像、音频和视频，支持119种语言的文本交互，具备卓越的指令跟随与系统提示定制能力，可轻松设定角色和对话风格，可用于构建语音助手、多媒体分析和内容创作应用。[非实时（Qwen-Omni）](https://help.aliyun.com/zh/model-studio/qwen-omni)

音频理解

2025-09-22

qwen3-omni-30b-a3b-captioner

以千问3-Omni为基座的开源模型，无需任何提示，自动为复杂语音、环境声、音乐、影视声效等生成精准、全面的描述，能识别说话人情绪、音乐元素（如风格、乐器）、敏感信息等，适用于音频内容分析、安全审核、意图识别、音频剪辑等多个领域。[音频理解-Qwen3-Omni-Captioner](https://help.aliyun.com/zh/model-studio/qwen3-omni-captioner)

图生视频

2025-09-19

wan2.2-animate-move

支持将模板视频中角色的动作和表情，迁移至单张静态人物图片上，生成人物动作视频。[万相-图生动作](https://help.aliyun.com/zh/model-studio/wan-animate-move-api)

图生视频

2025-09-19

wan2.2-animate-mix

能够依据人物图片和参考视频，将视频中的主角替换为图片中的角色，同时保留原视频的场景、光照和色调，实现无缝人物替换。[万相-视频换人](https://help.aliyun.com/zh/model-studio/wan-animate-mix-api)

视觉理解

2025-09-12

qwen-vl-ocr-2025-08-18

文字定位能力全面升级，通用文字识别、信息抽取能力均有提升。[文字提取](https://help.aliyun.com/zh/model-studio/qwen-vl-ocr#e91318ce09pxi)。

首尾帧生视频

2025-09-12

wan2.2-kf2v-flash

指令理解与运镜控制更准，稳定性全面提升。[图生视频-基于首尾帧](https://help.aliyun.com/zh/model-studio/legacy-image-to-video-by-first-and-last-frame-api-reference)

推理模型

2025-09-11

qwen-plus-2025-09-11

属于 Qwen3 系列模型，相较于qwen-plus-2025-07-28，在思考模式下提升了指令遵循能力、总结回复更加精简，详见[深度思考](https://help.aliyun.com/zh/model-studio/deep-thinking)。在非思考模式下中文理解与逻辑推理能力得到增强，详见[概述](https://help.aliyun.com/zh/model-studio/text-generation)。

推理模型

2025-09-11

qwen3-next-80b-a3b-thinking、qwen3-next-80b-a3b-instruct

基于Qwen3的新一代开源模型，thinking模型相较于qwen3-235b-a22b-thinking-2507提升了指令遵循能力，总结回复更加精简，详见[深度思考](https://help.aliyun.com/zh/model-studio/deep-thinking)。instruct模型相较于qwen3-235b-a22b-instruct-2507增强了中文理解、逻辑推理及文本生成能力，详见[概述](https://help.aliyun.com/zh/model-studio/text-generation)。

语音合成

2025-09-08

cosyvoice-v3-plus、cosyvoice-v3

语音合成CosyVoice新增cosyvoice-v3-plus和cosyvoice-v3模型，较之前版本在自然度、音质、韵律、情感表现力上有更好的表现。使用方法请参见[实时语音合成-CosyVoice /Sambert](https://help.aliyun.com/zh/model-studio/text-to-speech)。

语音识别

2025-09-08

qwen3-asr-flash（稳定版，等同qwen3-asr-flash-2025-09-08）

qwen3-asr-flash-2025-09-08（快照版）

Qwen3-ASR模型基于Qwen3-Omni模型基座训练而成，支持多语言识别、歌唱识别、噪声拒识等功能。[非实时语音识别](https://help.aliyun.com/zh/model-studio/non-realtime-speech-recognition-user-guide)

文生文

2025-09-05

qwen3-max-preview

基于Qwen3的Qwen-Max模型（预览版），相较Qwen 2.5系列整体通用能力有大幅度提升，中英文通用文本理解能力、复杂指令遵循能力、主观开放任务能力、多语言能力、工具调用能力均显著增强；模型知识幻觉更少。千问 Max

视频生成

2025-08-26

wan2.2-s2v-detect、wan2.2-s2v

万相数字人模型支持基于单张图片和音频，生成动作自然的说话、唱歌或表演视频，不限制形象画幅，支持肖像、全身或半身的人物图像。[万相-数字人](https://help.aliyun.com/zh/model-studio/wan-s2v-overview/)

图像翻译

2025-08-22

qwen-mt-image

千问图像翻译模型支持将11种语言图片的文字翻译成中文或英文，能精准保留原始排版与内容信息，并提供术语定义、敏感词过滤、图像主体检测等功能。[千问-图像翻译](https://help.aliyun.com/zh/model-studio/qwen-mt-image-api)

推理模型

2025-08-22

deepseek-v3.1

混合推理架构模型，同时支持思考模式与非思考模式。详情参见[DeepSeek -阿里云](https://help.aliyun.com/zh/model-studio/deepseek-api)。

深入研究

2025-08-22

qwen-deep-research

千问深入研究模型，它可以拆解复杂问题，结合互联网搜索进行推理分析并生成研究报告。详情请参见[深入研究（Qwen-Deep-Research）](https://help.aliyun.com/zh/model-studio/qwen-deep-research)

语音识别

2025-08-22

fun-asr（稳定版，等同fun-asr-2025-08-25）

fun-asr-2025-08-25（快照版）

Fun-ASR 是通义实验室推出的端到端语音识别大模型。它基于先进的自研语音技术，具备卓越的上下文感知和高精度转写能力，支持中英文录音文件识别。[录音文件识别-Fun-ASR/Paraformer](https://help.aliyun.com/zh/model-studio/recording-file-recognition)

图像编辑

2025-08-19

qwen-image-edit

千问图像编辑模型支持精准的中英双语文字编辑、调色、细节增强、风格迁移、增删物体、改变位置和动作等操作，可实现复杂的图文编辑。[图像编辑-千问](https://help.aliyun.com/zh/model-studio/qwen-image-edit-guide)

视觉理解

2025-08-15

qwen-vl-plus-2025-08-15

视觉理解模型。在物体识别与定位、多语言处理的能力上有显著提升。[图像与视频理解](https://help.aliyun.com/zh/model-studio/vision)

视觉理解

2025-08-13

qwen-vl-max-2025-08-13

视觉理解模型。视觉理解指标全面提升，数学、推理、物体识别、多语言处理能力显著增强。[图像与视频理解](https://help.aliyun.com/zh/model-studio/vision)

文生图

2025-08-13

qwen-image

千问文生图模型在复杂文本渲染方面表现突出，特别是中英文文本渲染，可实现复杂的图文混合布局**。**[文生图（Qwen-Image)](https://help.aliyun.com/zh/model-studio/qwen-image-api)

图生视频

2025-08-11

wan2.2-i2v-flash

万相2.2极速版模型。相较 2.1 模型，新版本在画面细节表现和运动稳定性方面均有显著提升，生成速度提升达 50%。[首帧生视频](https://help.aliyun.com/zh/model-studio/legacy-image-to-video-api-reference/)

视觉理解

2025-08-06

qwen-vl-plus-2025-07-10

视觉理解模型。相较于上一版模型，进一步提升监控视频内容的理解能力。[图像与视频理解](https://help.aliyun.com/zh/model-studio/vision)

代码模型

2025-08-05

qwen3-coder-flash、qwen3-coder-flash-2025-07-28

千问Coder系列速度最快、成本最低的模型。[代码能力（Qwen-Coder）](https://help.aliyun.com/zh/model-studio/qwen-coder)

推理模型

2025-08-05

qwen-flash、qwen-flash-2025-07-28

千问系列速度最快、成本极低的模型，适合简单任务。模型列表

推理模型

2025-07-30

qwen-plus-2025-07-28

属于 Qwen3 系列模型，相较于上一版模型，将上下文长度提高到了1,000,000。思考模式请参见[深度思考](https://help.aliyun.com/zh/model-studio/deep-thinking)，非思考模式请参见[概述](https://help.aliyun.com/zh/model-studio/text-generation)。

推理模型

2025-07-30

qwen3-30b-a3b-thinking-2507

qwen3-30b-a3b-instruct-2507

是qwen3-30b-a3b的升级版。thinking模型逻辑能力、通用能力、知识增强及创作能力提升，参见[深度思考](https://help.aliyun.com/zh/model-studio/deep-thinking)。instruct模型创作能力与模型安全性提升，参见[概述](https://help.aliyun.com/zh/model-studio/text-generation)。

图生视频

2025-07-28

wan2.2-i2v-plus

相较 2.1 模型，新版本在画面细节表现和运动稳定性方面均有显著提升，生成速度提升达 50%。[首帧生视频](https://help.aliyun.com/zh/model-studio/legacy-image-to-video-api-reference/)

文生视频

2025-07-28

wan2.2-t2v-plus

相较 2.1 模型，新版本在画面细节表现和运动稳定性方面均有显著提升，生成速度提升达 50%。[文生视频](https://help.aliyun.com/zh/model-studio/text-to-video-api-reference)

文生图

2025-07-28

wan2.2-t2i-flash、wan2.2-t2i-plus

相较 2.1 模型，新版本在创意性、稳定性、写实质感上全面升级，生成速度提升达 50%。[文生图V2版](https://help.aliyun.com/zh/model-studio/text-to-image-v2-api-reference)

数据挖掘

2025-07-26

qwen-doc-turbo

千问数据挖掘模型，可以提取文档中的结构化信息并用于数据标注和内容审核等领域。详情请参见[数据挖掘（Qwen-Doc）](https://help.aliyun.com/zh/model-studio/data-mining-qwen-doc)。

推理模型

2025-07-24

qwen3-235b-a22b-thinking-2507、qwen3-235b-a22b-instruct-2507

是qwen3-235b-a22b的升级版。thinking模型逻辑能力、通用能力、知识增强及创作能力均有大幅提升，适用于高难度强推理场景，参见[深度思考](https://help.aliyun.com/zh/model-studio/deep-thinking)。instruct模型创作能力与模型安全性均有提升，参见[概述](https://help.aliyun.com/zh/model-studio/text-generation)。

代码模型

2025-07-23

qwen3-coder、qwen3-coder-plus-2025-07-22

基于 Qwen3 的代码生成模型，具有强大的Coding Agent能力，擅长工具调用和环境交互，代码能力卓越的同时兼具通用能力。[代码能力（Qwen-Coder）](https://help.aliyun.com/zh/model-studio/qwen-coder)

语音合成

2025-06-26

qwen-tts-2025-05-22

qwen-tts 模型的2025年5月22日快照版本。新增北京话、吴语和四川话三种音色。[非实时语音合成](https://help.aliyun.com/zh/model-studio/non-realtime-tts-user-guide)

推理模型

2025-06-24

qwen-plus、qwen-turbo

qwen-plus 已更新，支持[思考模式](https://help.aliyun.com/zh/model-studio/deep-thinking)，与 qwen-plus-2025-04-28 能力相同；qwen-turbo 已更新，支持[思考模式](https://help.aliyun.com/zh/model-studio/deep-thinking)，与 qwen-turbo-2025-04-28 能力相同。

语音合成

2025-06-23

cosyvoice-v2

cosyvoice-v2 全新升级，新增多种音色，不仅丰富了语言支持范围（如粤语、韩语、日语），还引入了更多风格化音色（如英式英语、美式英语）。详情请参见[音色列表](https://help.aliyun.com/zh/model-studio/cosyvoice-voice-list)。

文本向量

2025-06-04

text-embedding-v4

text-embedding-v4为text-embedding-v3的升级版模型，属于[Qwen3-Embedding](https://qwenlm.github.io/zh/blog/qwen3-embedding/)系列。相较于上一版模型，新版模型涵盖了更多自然语言以及多种编程语言，并新增2048及1536向量维度的选择。[文本与多模态向量化](https://help.aliyun.com/zh/model-studio/embedding)

推理模型

2025-06-04

deepseek-r1-0528

deepseek-r1-0528为deepseek-r1的升级版模型，相较于上一版模型，新版模型在复杂推理任务中的表现有了显著提升。在数学、编程与通用逻辑等多个基准测评中取得了优异成绩。[DeepSeek -阿里云](https://help.aliyun.com/zh/model-studio/deepseek-api)

视觉推理

2025-06-03

qvq-max-2025-05-15

视觉推理模型。较上一个版本，增强了在数学、编程、视觉分析、创作以及通用任务方面的能力。[视觉推理](https://help.aliyun.com/zh/model-studio/visual-reasoning)

视觉推理

2025-06-03

qvq-plus、qvq-plus-latest、qvq-plus-2025-05-15

视觉推理模型。支持视觉输入及思维链输出，继qvq-max模型后推出的plus版本，相较于qvq-max模型，qvq-plus系列模型推理速度更快，效果和成本更均衡。[视觉推理](https://help.aliyun.com/zh/model-studio/visual-reasoning)

语音合成

2025-06-03

cosyvoice-v2

SSML（Speech Synthesis Markup Language，语音合成标记语言）不仅能指定语音合成读什么内容，还能精细控制其朗读方式，包括断句分词、发音、语速、停顿、语调、音量等语音特征，甚至支持添加背景音乐，从而实现更加自然、富有表现力的语音输出。详细使用方法请参见[SSML标记语言介绍](https://help.aliyun.com/zh/model-studio/introduction-to-cosyvoice-ssml-markup-language)。

视频编辑

2025-05-19

wanx2.1-vace-plus

通用视频编辑模型。模型具备多模态输入能力，融合图片、视频与文本提示词，可执行图生视频（参考图像主体或背景生成视频）、视频重绘（从输入视频中提取运动特征生成视频）等多种任务。[通用视频编辑](https://help.aliyun.com/zh/model-studio/legacy-wanx-vace-api-reference)

图像生成

2025-05-15

aitryon-plus

AI试衣模型。相较于基础版aitryon模型，aitryon-plus模型在图片清晰度、服饰纹理细节和logo还原效果等方面均有提升，但生成耗时较长，适用于对时效性要求不高的场景。[AI试衣-Plus版](https://help.aliyun.com/zh/model-studio/aitryon-plus-api)

视觉理解

2025-05-15

qwen-vl-plus-2025-05-07

视觉理解模型。模型在数学、推理、监控视频内容的理解方面的能力有显著提升。[图像与视频理解](https://help.aliyun.com/zh/model-studio/vision)

文字提取

2025-04-30

qwen-vl-ocr-2025-04-13

基于Qwen-VL训练的OCR专有大模型，提供强大的图文识别能力；该模型新增六种内置的OCR任务，分别是：通用识别、文档解析、表格解析、信息抽取、多语言识别、公式识别。[文字提取](https://help.aliyun.com/zh/model-studio/qwen-vl-ocr)

推理模型

2025-04-28

**Qwen3商业版模型**

qwen-plus-2025-04-28、qwen-turbo-2025-04-28

**Qwen3开源版模型**

qwen3-235b-a22b、qwen3-30b-a3b、qwen3-32b、qwen3-14b、qwen3-8b、qwen3-4b、qwen3-1.7b、qwen3-0.6b

Qwen3 模型支持思考模式和非思考模式，您可以通过 `enable_thinking` 参数实现两种模式的切换。除此之外，Qwen3 模型的能力得到了大幅提升：

1.  **推理能力**：在数学、代码和逻辑推理等评测中，显著超过 QwQ 和同尺寸的非推理模型，达到同规模业界顶尖水平。
    
2.  **人类偏好能力**：创意写作、角色扮演、多轮对话、指令遵循能力均大幅提升，通用能力显著超过同尺寸模型。
    
3.  **Agent 能力**：在推理、非推理两种模式下都达到业界领先水平，能够精准地调用外部工具。
    
4.  **多语言能力**：支持100多种语言和方言，多语言翻译、指令理解、常识推理能力都明显提升。
    
5.  **回复格式问题修复**：修复了之前版本存在的回复格式的问题，如异常 Markdown、中间截断、错误输出 boxed 等问题。
    

思考模式请参见[深度思考](https://help.aliyun.com/zh/model-studio/deep-thinking)，非思考模式请参见[概述](https://help.aliyun.com/zh/model-studio/text-generation)。

声音复刻

2025-04-24

cosyvoice-v2

用户仅需提供10~20秒的音频，即可迅速生成高度相似且听感自然的定制声音。[声音复刻/设计](https://help.aliyun.com/zh/model-studio/voice-replica-1/)

视觉理解

2025-04-18

qwen-vl-max-2025-04-08

视觉理解模型。数学和推理能力有所提升，回复风格面向人类偏好进行调整，模型回复详实程度和格式清晰度明显改善。[图像与视频理解](https://help.aliyun.com/zh/model-studio/vision)

图生视频

2025-04-18

wanx2.1-kf2v-plus

基于输入的首帧和尾帧图片，模型能够根据提示词生成一段丝滑流畅的动态视频。[首尾帧生视频](https://help.aliyun.com/zh/model-studio/legacy-image-to-video-by-first-and-last-frame-api-reference)

视觉理解

2025-04-04

qwen-vl-max-2025-04-02

视觉理解模型。在解决复杂数学问题方面，准确性显著提高，回复风格面向人类偏好进行大幅调整，尤其是数学、逻辑推理、知识问答等客观类问题，模型回复详实程度和格式清晰度明显改善。[图像与视频理解](https://help.aliyun.com/zh/model-studio/vision)

视觉推理

2025-03-28

qvq-max、qvq-max-latest、qvq-max-2025-03-25

视觉推理模型。支持视觉输入及思维链输出，在数学、编程、视觉分析、创作以及通用任务上都表现出更强的能力。[视觉推理](https://help.aliyun.com/zh/model-studio/visual-reasoning)

全模态

2025-03-26

qwen-omni-turbo-2025-03-26

千问全新多模态理解生成大模型，支持文本、图像、语音与视频输入，并输出文本与音频，提供了4种自然对话音色。使用方法请参见[非实时（Qwen-Omni）](https://help.aliyun.com/zh/model-studio/qwen-omni)。

全模态

2025-03-26

qwen2.5-omni-7b

千问全新多模态理解生成大模型，支持文本、图像、语音与视频输入，并输出文本与音频，提供了2种自然对话音色。使用方法请参见[非实时（Qwen-Omni）](https://help.aliyun.com/zh/model-studio/qwen-omni)。

图像编辑

2025-03-25

wanx2.1-imageedit

通用图像编辑模型。通过一句话指令实现多样化的图像编辑功能，如扩图、去文字水印、图像修复、图像风格迁移等。[万相-通用图像编辑2.1](https://help.aliyun.com/zh/model-studio/wanx-image-edit-api-reference)

视觉理解

2025-03-24

qwen2.5-vl-32b-instruct 

视觉理解模型。在数学问题的解答方面达到了接近Qwen2.5VL-72B的水平，回复风格面向人类偏好进行大幅调整，尤其是数学、逻辑推理、知识问答等客观类问题，模型回复详实程度和格式清晰度明显改善。[图像与视频理解](https://help.aliyun.com/zh/model-studio/vision)

推理模型

2025-03-06

qwq-plus、qwq-plus-latest、qwq-plus-2025-03-05

基于 Qwen2.5 模型训练的 QwQ 推理模型，通过强化学习大幅度提升了模型推理能力。模型数学代码等核心指标（AIME 24/25、LiveCodeBench）以及部分通用指标（IFEval、LiveBench等）达到DeepSeek-R1 满血版水平。[深度思考](https://help.aliyun.com/zh/model-studio/deep-thinking)

开源推理模型

2025-03-06

qwq-32b

基于 Qwen2.5-32B 模型训练的 QwQ 推理模型，通过强化学习大幅度提升了模型推理能力。模型数学代码等核心指标（AIME 24/25、LiveCodeBench）以及部分通用指标（IFEval、LiveBench等）达到DeepSeek-R1 满血版水平，各指标均显著超过同样基于 Qwen2.5-32B 的 DeepSeek-R1-Distill-Qwen-32B。[深度思考](https://help.aliyun.com/zh/model-studio/deep-thinking)

语音识别/翻译

2025-03-03

gummy-realtime-v1

gummy-chat-v1

Gummy大模型支持实时语音识别与翻译，能够精准识别中、英、日、韩等10种语言。此外，它还支持中、英、日、韩之间的互译，以及其他6种语言单向翻译成中文或英文。使用方法请参见[实时语音识别-Fun-ASR/Paraformer](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition)。

图生视频

2025-02-25

wanx2.1-i2v-turbo

相较于wanx2.1-i2v-plus模型，turbo模型生成速度更快，耗时仅为plus模型的三分之一，性价比更高。使用方法请参见[首帧生视频](https://help.aliyun.com/zh/model-studio/legacy-image-to-video-api-reference/)。

全模态

2025-02-14

qwen-omni-turbo

qwen-omni-turbo-latest

qwen-omni-turbo-2025-01-19

Qwen-Omni 系列模型支持输入多种模态的数据，包括视频、音频、图片、文本，并输出文本。使用方法请参见[非实时（Qwen-Omni）](https://help.aliyun.com/zh/model-studio/qwen-omni)。

视觉理解

2025-02-07

qwen-vl-max-2025-01-25

视觉理解模型。属于[Qwen2.5-VL](https://qwenlm.github.io/blog/qwen2.5-vl/)系列模型，相较于上一版模型，扩展上下文至128k，显著增强图像和视频的理解能力。

视觉理解

2025-02-07

qwen-vl-plus-2025-01-25

视觉理解模型。属于[Qwen2.5-VL](https://qwenlm.github.io/blog/qwen2.5-vl/)系列模型，相较于上一版模型，扩展上下文至128k，显著增强图像和视频的理解能力。

文生文

2025-01-27

deepseek-v3

deepseek-r1

DeepSeek系列模型是由深度求索（DeepSeek）公司推出的大语言模型。

-   DeepSeek-V3 为 MoE 模型，671B 参数，激活 37B，在 14.8T Token 上进行了预训练，在长文本、代码、数学、百科、中文能力上表现优秀。
    
-   DeepSeek-R1 在后训练阶段大规模使用了强化学习技术，在仅有极少标注数据的情况下，极大提升了模型推理能力，尤其在数学、代码、自然语言推理等任务上。
    
-   具体请参见[DeepSeek -阿里云](https://help.aliyun.com/zh/model-studio/deepseek-api)。
    

视觉理解

2025-01-27

qwen2.5-vl-3b-instruct

qwen2.5-vl-7b-instruct

qwen2.5-vl-72b-instruct

-   相对于Qwen2-VL大模型有如下改进：
    
    -   在指令跟随、数学计算、代码生成、结构化输出（JSON输出）等方面的能力有显著提升。
        
    -   支持对图像中的文字、图表、布局等视觉内容进行统一解析，并增加了精准定位视觉元素的能力，支持检测框和坐标点的表示方式。
        
    -   支持对长视频文件（最长10分钟）进行理解，具备秒级别的事件时刻定位能力，能理解时间先后和快慢。
        
-   使用方法请参见[图像与视频理解](https://help.aliyun.com/zh/model-studio/vision)。
    

文生文

2025-01-27

qwen-max-2025-01-25

qwen2.5-14b-instruct-1m

qwen2.5-7b-instruct-1m

-   qwen-max-2025-01-25模型（又称为[Qwen2.5-Max](https://qwenlm.github.io/zh/blog/qwen2.5-max/)）：千问系列效果最好的模型，代码编写与理解能力、逻辑能力、多语言能力显著提升，回复风格面向人类偏好进行大幅调整，模型回复详实程度和格式清晰度明显改善，内容创作、JSON格式遵循、角色扮演能力定向提升。使用方法请参见：[概述](https://help.aliyun.com/zh/model-studio/text-generation)。
    
-   qwen2.5-14b-instruct-1m、qwen2.5-7b-instruct-1m模型：相比于qwen2.5-14b-instruct与qwen2.5-7b-instruct模型，将上下文长度提高到了1,000,000。使用方法请参见：[概述](https://help.aliyun.com/zh/model-studio/text-generation)。
    

图生视频

2025-01-22

emoji-detect-v1

emoji-v1

-   基于人脸图片和预设的人脸动态模板，生成人脸动态视频。该模型可用于表情包制作、视频素材生成等场景。使用方法请参见[表情包Emoji快速开始](https://help.aliyun.com/zh/model-studio/emoji-quick-start/)。
    

文生文

2025-01-17

qwen-plus-2025-01-12

-   相对于qwen-plus-2024-12-20模型，中英文整体能力有提升，中英常识、阅读理解能力提升较为显著，在不同语言、方言、风格之间自然切换的能力有显著改善，中文指令遵循能力显著提升。使用方法请参见[qwen-plus-2025-01-12](https://bailian.console.aliyun.com/#/model-market/detail/qwen-plus-0112)。
    

图生视频

2025-01-17

wanx2.1-i2v-plus

-   输入图片作为视频首帧，再根据提示词生成视频。使用方法请参见[首帧生视频](https://help.aliyun.com/zh/model-studio/legacy-image-to-video-api-reference/)。
    

文生图

2025-01-17

wanx2.0-t2i-turbo

-   擅长质感人像与创意设计，速度中等，性价比高。使用方法请参见[文生图V2系列模型](https://help.aliyun.com/zh/model-studio/text-to-image-v2-api-reference)。
    

视觉理解

2025-01-13

qwen-vl-plus-2025-01-02

-   相较于qwen-vl-plus-0809模型，大幅提升指令跟随、图像理解和数学能力。使用方法请参见[图像与视频理解](https://help.aliyun.com/zh/model-studio/vision)。
    

文生视频

2025-01-08

wanx2.1-t2v-turbo

wanx2.1-t2v-plus

-   一句话生成视频。
    
-   具备强大的指令遵循能力，支持大幅度复杂运动、现实物理规律还原，生成的视频呈现丰富的艺术风格及影视级画面质感。使用方法请参见[万相2.7-文生视频](https://help.aliyun.com/zh/model-studio/text-to-video-api-reference)。
    

文生图

2025-01-08

wanx2.1-t2i-turbo

wanx2.1-t2i-plus

-   [文生图V2系列模型](https://help.aliyun.com/zh/model-studio/text-to-image-v2-api-reference)为全面升级的万相文生图模型，推荐体验。
    

视觉理解

2025-01-07

qwen-vl-max-2024-12-30

-   该模型丰富了知识库，图像识别和理解能力进一步提升，能够解析复杂的视觉内容。使用方法请参见[图像与视频理解](https://help.aliyun.com/zh/model-studio/vision)。
    

语音识别

2025-01-02

qwen-audio-asr

qwen-audio-asr-latest

qwen-audio-asr-2024-12-04

-   千问ASR是基于Qwen-Audio训练，专用于语音识别的模型，目前支持的语言有：中文、英文。使用方法请参见[实时语音识别-Fun-ASR/Paraformer](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition)。
    

视觉推理

2024-12-25

qvq-72b-preview

-   专注于提升视觉推理能力，尤其在数学推理领域。使用方法请参见[图像与视频理解](https://help.aliyun.com/zh/model-studio/vision)。
    

多语言翻译

2024-12-25

qwen-mt-plus

qwen-mt-turbo

-   Qwen-MT模型是基于千问模型优化的机器翻译大语言模型，擅长中英互译、中文与小语种互译、英文与小语种互译，小语种包括日、韩、法、西、德、葡（巴西）、泰、印尼、越、阿等26种。在多语言互译的基础上，提供术语干预、领域提示、记忆库等能力，提升模型在复杂应用场景下的翻译效果。详情请参见[翻译能力（Qwen-MT）](https://help.aliyun.com/zh/model-studio/machine-translation)。
    

视觉理解

2024-12-18

qwen2-vl-72b-instruct

-   在多个视觉理解基准测试中取得了最先进的成绩，显著增强多模态任务的处理能力。使用方法请参见[图像与视频理解](https://help.aliyun.com/zh/model-studio/vision)。
    

意图理解

2024-12-12

tongyi-intent-detect-v3

-   千问意图理解模型，能够在百毫秒级时间内快速、准确地解析用户意图，并选择合适工具来解决用户问题。详情请参见[意图理解](https://help.aliyun.com/zh/model-studio/intent-detect-capability)。
    

声动人像

2024-12-10

videoretalk

-   支持根据人物视频和音频生成对口型视频，详情请参见[快速开始](https://help.aliyun.com/zh/model-studio/videos/videoretalk-quick-start)。
    

舞动人像

2024-12-10

animate-anyone-gen2

animate-anyone-detect-gen2

animate-anyone-template-gen2

-   分别提供人物图片合规检测、人物动作模板生成与人物视频生成能力，依次调用这三个模型可生成人物舞蹈视频。详情请参见[快速开始](https://help.aliyun.com/zh/model-studio/videos/animateanyone-quick-start)。
    

语音合成

2024-12-10

cosyvoice-v1

-   用户仅需提供10~20秒的音频，即可迅速生成高度相似且听感自然的定制声音。详情请参见[声音复刻/设计](https://help.aliyun.com/zh/model-studio/voice-replica-1/)。
    

llama系列

2024-12-09

llama3.3-70b-instruct

-   新增第三方大模型llama3.3系列中70B参数的模型。详情请参见[Llama（输入文本和图像）](https://help.aliyun.com/zh/model-studio/api-details-of-llama3-2-text-image)。
    

音频理解

2024-12-09

qwen-audio-turbo-latest

qwen-audio-turbo-2024-12-04

-   新增的模型，相较于qwen-audio-turbo-2024-08-07版本，大幅提升语音识别准确率，并新增了语音聊天能力。详情请参见[音频理解-Qwen-Audio](https://help.aliyun.com/zh/model-studio/audio-language-model)。
    

文生文

2024-11-28

qwq-32b-preview

-   本模型专注于增强 AI 推理能力。详情请参见QWQ。
    

2024-11-28

qwen-plus-2024-11-25

qwen-plus-2024-11-27

-   相较于qwen-plus-0919模型中英文回复详实程度显著提升，更加符合用户偏好；模型角色扮演能力显著增强；模型中文的文本创作能力显著提升；中英文指令遵循能力提升；修复了RAG场景下引用角标的生成问题。详情请参见[百炼控制台](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market/all)。
    

2024-11-15

qwen-turbo-2024-11-01

-   上下文长度扩展至一百万Token。详情请参见[百炼控制台](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market/all)。
    

视觉理解

2024-11-15

qwen-vl-max-2024-11-19

-   增强了图像理解效果，改善生成重复文本的情况。详情请参见[图像与视频理解](https://help.aliyun.com/zh/model-studio/vision)。
    

qwen-vl-max-2024-10-30

-   加强了多语言理解能力。详情请参见[图像与视频理解](https://help.aliyun.com/zh/model-studio/vision)。
    

-   qwen-vl-ocr
    
-   qwen-vl-ocr-2024-10-28
    
-   qwen-vl-ocr-latest
    

-   qwen-vl-ocr是专用于OCR的模型；在表格、试题等类型图像的文字提取能力大幅提升。详情请参见[文字提取](https://help.aliyun.com/zh/model-studio/qwen-vl-ocr)。
    

文生文

2024-11-12

-   闭源版本qwen-coder-plus等模型
    
-   开源版本qwen2.5-coder-32b-instruct等模型
    

-   这些模型在代码生成、代码修复及代码推理能力上具备业界领先水平。详情请参见[代码能力（Qwen-Coder）](https://help.aliyun.com/zh/model-studio/qwen-coder)。
    

灵动人像

2024-11-7

-   liveportrait-detect
    
-   liveportrait
    

-   基于人物肖像图片和人声音频文件，**快速、轻量**地生成人物肖像动态视频。详情请参见[灵动人像LivePortrait 快速开始](https://help.aliyun.com/zh/model-studio/liveportrait-quick-start/)。
    

悦动人像

2024-11-7

-   emo-detect-v1
    
-   emo-v1
    

-   基于人物肖像图片和人声音频文件，生成人物肖像动态视频，不需要部署，可直接调用。与旧版的EMO模型（emo-detect、emo）相比，在调用方式及计费方式上有区别。详情请参见[悦动人像EMO 快速开始](https://help.aliyun.com/zh/model-studio/emo-quick-start/)。
    

llama系列

2024-11-5

-   llama3.2-90b-vision-instruct
    
-   llama3.2-11b-vision
    

-   新增第三方大模型llama3.2系列中11B和90B参数的模型，这两个模型加入了视觉理解的功能。详情请参见[Llama模型API参考](https://help.aliyun.com/zh/model-studio/api-details-of-llama3-2-text-image)。
    

视觉理解

2024-10-29

qwen2-vl-2b-instruct

-   扩展上下文至32k，大幅提升图像理解能力。详情请参见[图像与视频理解](https://help.aliyun.com/zh/model-studio/vision)。
    

视觉理解

2024-10-23

qwen2-vl-7b-instruct

-   新增qwen2-vl-7b-instruct模型，详情请参见[图像与视频理解](https://help.aliyun.com/zh/model-studio/vision)。
    

文生文

2024-09-18

qwen-long

-   新增qwen-long模型，详情请参见[长上下文（Qwen-Long）](https://help.aliyun.com/zh/model-studio/long-context-qwen-long)
    

视觉理解

2024-08-27

qwen-vl-max-0809

-   本模型为qwen-vl-max的2024年8月9日快照版本，将在9月9日更新至qwen-vl-max主版本，快照版本维护到下个快照版本发布时间（待定）后一个月。点击[千问VL API详情](https://help.aliyun.com/zh/document_detail/2712587.html)查看完整信息。
    

文生文

2024-08-16

Qwen2-Math系列模型

-   具有强大的数学解题能力，点击[通过API调用Qwen2-Math模型](https://help.aliyun.com/zh/document_detail/2844170.html)进行体验。
    

文生图

2024-08-07

FLUX文生图模型

-   FLUX文生图模型是由 Black Forest Labs 开源的高质量文本到图像生成模型，它在多个维度上展现了卓越性能，尤其在文本引导的图像生成、多主体场景构建、以及精细的手部细节生成等方面，实现了显著的提升，为文生图领域设定了新的技术标杆。点击[文生图FLUX](https://help.aliyun.com/zh/model-studio/videos/flux/)进行了解。
    

llama系列

2024-07-23

-   Llama3.1-8b-instruct
    
-   Llama3.1-70b-instruct
    
-   Llama3.1-405b-instruct
    

-   新增Llama-3.1系列模型版本，点击[Llama （仅文本输入）](https://help.aliyun.com/zh/model-studio/api-details-of-llama-llm)查看。
    

文本向量

2024-07-10

text-embedding-v3

-   **text-embedding-v3**模型是**text-embedding-v2**模型的升级版本，主打**高性能、低成本、支持50+多语言、超长文本**。
    

> 更新内容主要包括：

-   > **语种扩充**：**text-embedding-v3**模型对比**text-embedding-v2**模型扩展了意大利语、波兰语、越南语、泰语等语种，支持语种数量增加到50+。
    
-   > **输入长度扩展**：支持编码的输入长度从2048扩展至8192, 对text-embedding-v3, 8192指文本输入的最大token长度
    
-   > **可变输出连续向量维度**: 相比text-embedding-v2模型的固定1536向量维度, text-embedding-v3支持用户自定义连续向量的维度, 目前可以选择512,768和1024维度；同时为了进一步节省下游任务的使用成本，text-embedding-v3模型在不衰减效果的前提下将最大的向量维度降低至1024维。
    
-   > **不再区分Query/Document类型：**text-embedding-v3模型在不降低模型效果的前提下不再区分输入文本的类型，text\_type参数无需指定输入的文本是Query还是Document类型。
    
-   > **Sparse向量支持**: text-embedding-v3模型同时支持连续向量表示（dense vector）和离散向量表示模型（sparse vector）, 用户可以在接口参数中指定输出连续向量、离散向量或者同时输出。
    
-   > **效果提升**：预训练模型底座和SFT策略优化提升embedding模型整体效果，公开数据评测结果。
    

文生文

2024-07-05

-   qwen-turbo-0206
    
-   qwen-turbo-0624
    

-   新增qwen-turbo模型的快照版本，点击[文本生成](https://help.aliyun.com/zh/model-studio/qwen-api-reference/)查看详情。
    

文生文

2024-07-05

-   qwen-plus-0206
    
-   qwen-plus-0624
    

-   新增qwen-plus模型的快照版本，点击[文本生成](https://help.aliyun.com/zh/model-studio/qwen-api-reference/)查看详情。
    

文生文

2024-07-02

Minimax大语言模型

-   新增Minimax大语言模型，点击[MiniMax大语言模型](https://help.aliyun.com/zh/model-studio/videos/minimax-llm/)查看详情。
    

文生文

2024-06-07

qwen2系列开源大语言模型

-   与qwen1.5相比，qwen2在语言理解、语言生成、多语言能力、编码、推理等基准测试中超越了大多数开源模型。点击[模型介绍](https://help.aliyun.com/zh/document_detail/2804542.html)查看详情。
    

文生文

2024-06-03

零一万物大语言模型

零一万物大语言模型是千亿参数大语言模型，是LM SYS榜单TOP10上唯一国产大模型。具备超强的问答、推理及文本生能力，完整内容请点击[零一万物大语言模型](https://help.aliyun.com/zh/model-studio/videos/yi-large-llm/)查看。

文生文

2024-04-28

qwen1.5-110b-chat

-   qwen1.5-110b-chat模型时千问1.5对外开源的110B规模参数量的经过人类指令对齐的chat模型。点击[通义千问开源模型](https://help.aliyun.com/zh/document_detail/2713159.html)查看详情。
    

## 全球

服务部署范围为[全球](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度；静态数据存储于您所选的地域。该部署范围支持的地域：美国（弗吉尼亚）、德国（法兰克福）。

**模型类型**

**时间**

**模型规格**

**功能说明**

推理模型

2026-05-21

qwen3.7-max、qwen3.7-max-2026-05-20

Qwen Max 系列新一代旗舰模型。仅支持纯文本输入，默认开启思考模式，支持显式缓存，在编程、办公与生产力、长周期自主执行方面均能出色胜任各项任务。

推理模型

2026-05-20

glm-5.1

智谱GLM-5.1模型，专为长程任务设计，支持 200K 上下文，最大输出可达 128K Token。通过强大的逻辑推理、长文本理解及代码生成能力，在多项基准测试中表现优异，适用于智能交互、企业应用及开发辅助等场景。[GLM-阿里云](https://help.aliyun.com/zh/model-studio/glm)

文生视频

2026-05-06

happyhorse-1.0-t2v

HappyHorse系列文生视频模型，支持有声视频生成，可生成3~15秒、720P/1080P视频。[HappyHorse-文生视频](https://help.aliyun.com/zh/model-studio/happyhorse-text-to-video-api-reference)

图生视频

2026-05-06

happyhorse-1.0-i2v

HappyHorse系列图生视频模型，支持有声视频生成，可生成3~15秒、720P/1080P视频。[HappyHorse-图生视频-基于首帧](https://help.aliyun.com/zh/model-studio/happyhorse-image-to-video-api-reference)

视频编辑

2026-05-06

happyhorse-1.0-video-edit

HappyHorse系列视频编辑模型，支持对视频进行编辑处理。[HappyHorse-视频编辑](https://help.aliyun.com/zh/model-studio/happyhorse-video-edit-api-reference)

参考生视频

2026-05-06

happyhorse-1.0-r2v

HappyHorse系列参考生视频模型，支持多参考图输入生成有声视频，可生成3~15秒、720P/1080P视频。[HappyHorse-参考生视频](https://help.aliyun.com/zh/model-studio/happyhorse-reference-to-video-api-reference)

文生文与视觉理解

2026-04-29

kimi-k2.5

由月之暗面（Moonshot AI）公司推出的视觉理解模型，在代码生成、视觉理解等通用智能任务中表现突出。同时支持图像、视频与文本输入、对话与 Agent 任务。[Kimi-阿里云](https://help.aliyun.com/zh/model-studio/kimi-api)

推理模型

2026-04-29

deepseek-v4-pro

deepseek-v4-pro `cached_token` 单价调整为 **1 元/百万 token**，标准 `input_token` 单价不变。详见[上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)。

推理模型

2026-04-02

qwen3.6-plus、qwen3.6-plus-2026-04-02

千问3.6-Plus，代码开发能力重点升级（Agentic Coding、前端编程等），Vibe Coding体验显著提升；泛化场景推理能力进一步增强；多模态方面，万物识别、OCR、物体定位等能力显著提升；同时修复了Qwen3.5-Plus上线后的已知问题。使用方法与qwen3.5-plus一致。[概述](https://help.aliyun.com/zh/model-studio/text-generation)

推理模型

2026-03-04

qwen3.5-flash、qwen3.5-flash-2026-02-23、qwen3.5-122b-a10b、qwen3.5-27b、qwen3.5-35b-a3b

阿里巴巴推出的最新模型千问3.5-Flash和开源模型，支持文本、图像和视频输入，响应速度快，综合表现接近qwen3.5-plus，支持内置[工具调用](https://help.aliyun.com/zh/model-studio/tool-calls/)。[概述](https://help.aliyun.com/zh/model-studio/text-generation)

推理模型

2026-03-04

qwen3.5-plus、qwen3.5-plus-2026-02-15、qwen3.5-397b-a17b

阿里巴巴推出的最新模型千问3.5-Plus和开源模型，支持文本、图像和视频输入，在语言理解、逻辑推理、代码生成、智能体任务、图像理解、视频理解、图形用户界面（GUI）等多种任务中表现卓越，支持内置[工具调用](https://help.aliyun.com/zh/model-studio/tool-calls/)。[概述](https://help.aliyun.com/zh/model-studio/text-generation)

文生图

2026-01-12

wan2.6-t2i

新增同步接口。支持在总像素面积与宽高比约束内，自由选尺寸。[万相-文生图V2](https://help.aliyun.com/zh/model-studio/text-to-image-v2-api-reference)

图像生成与编辑

2026-01-12

wan2.6-image

支持图像编辑和图文混合输出。[万相-图像生成与编辑2.6](https://help.aliyun.com/zh/model-studio/wan-image-generation-api-reference)

图生视频-基于首帧

2026-01-12

wan2.6-i2v

新增多镜头叙事能力，支持音频能力，支持自动配音，或传入自定义音频文件。[万相-图生视频-基于首帧（2.1-2.6）](https://help.aliyun.com/zh/model-studio/legacy-image-to-video-api-reference/)

参考生视频

2026-01-12

wan2.6-r2v

基于参考视频的角色形象和音色，生成多镜头视频，支持自动配音。[万相2.7-参考生视频](https://help.aliyun.com/zh/model-studio/wan-video-to-video-api-reference)

文生视频

2026-01-12

wan2.6-t2v

新增多镜头叙事能力，支持音频能力，支持自动配音，或传入自定义音频文件。[万相2.7-文生视频](https://help.aliyun.com/zh/model-studio/text-to-video-api-reference)

视觉理解

2026-01-12

qwen3-vl-flash、qwen3-vl-flash-2025-10-15

Qwen3系列小尺寸视觉理解模型，实现思考模式和非思考模式的有效融合，相较于开源版Qwen3-VL-30B-A3B，效果更优，响应速度更快。[图像与视频理解](https://help.aliyun.com/zh/model-studio/vision)

视觉理解

2026-01-12

qwen3-vl-30b-a3b-thinking、qwen3-vl-30b-a3b-instruct

基于Qwen3-VL新一代开源模型，提供思考和非思考两个版本。响应速度快，具备更强多模态理解与推理、视觉智能体、长视频长文档等超长上下文支持能力；全面升级空间感知与万物识别能力，胜任复杂现实任务。[图像与视频理解](https://help.aliyun.com/zh/model-studio/vision)

视觉理解

2026-01-12

qwen3-vl-8b-thinking、qwen3-vl-8b-instruct

Qwen3-VL系列 8B 的Dense开源模型，提供思考和非思考两个版本。占用显存更低，能够完成多模态理解与推理；支持长视频长文档等超长上下文、视觉2D/3D定位；全面空间感知与万物识别能力。[图像与视频理解](https://help.aliyun.com/zh/model-studio/vision)

视觉理解

2026-01-12

qwen3-vl-32b-thinking、qwen3-vl-32b-instruct

Qwen3-VL系列 32B 的Dense模型，综合表现仅次于Qwen3-VL-235B模型，文档识别和理解、空间感知与万物识别、视觉2D检测/空间推理能力均表现出色，适合通用场景下的复杂感知任务。[图像与视频理解](https://help.aliyun.com/zh/model-studio/vision)

视觉理解

2026-01-12

qwen3-vl-plus、qwen3-vl-plus-2025-09-23、qwen3-vl-235b-a22b-thinking、qwen3-vl-235b-a22b-instruct

Qwen3系列视觉理解模型，实现思考模式和非思考模式的有效融合，视觉智能体能力达到世界顶尖水平。此版本在视觉编码、空间感知、多模态思考等方向全面升级；视觉感知与识别能力大幅提升。[图像与视频理解](https://help.aliyun.com/zh/model-studio/vision)

推理模型

2026-01-12

qwen3-next-80b-a3b-thinking、qwen3-next-80b-a3b-instruct

基于Qwen3的新一代开源模型，thinking模型相较于qwen3-235b-a22b-thinking-2507提升了指令遵循能力，总结回复更加精简，详见[深度思考](https://help.aliyun.com/zh/model-studio/deep-thinking)。instruct模型相较于qwen3-235b-a22b-instruct-2507增强了中文理解、逻辑推理及文本生成能力，详见[概述](https://help.aliyun.com/zh/model-studio/text-generation)。

推理模型

2026-01-12

qwen3-max、qwen3-max-2025-09-23

相较qwen3-max-preview版本，在智能体编程与工具调用方向进行了专项升级。本次发布的正式版模型达到领域SOTA水平，适配场景更加复杂的智能体需求。模型列表

推理模型

2026-01-12

qwen3-max-preview

基于Qwen3的Qwen-Max模型（预览版），相较Qwen 2.5系列整体通用能力有大幅度提升，中英文通用文本理解能力、复杂指令遵循能力、主观开放任务能力、多语言能力、工具调用能力均显著增强；模型知识幻觉更少。千问 Max

代码模型

2026-01-12

qwen3-coder-flash、qwen3-coder-flash-2025-07-28

千问Coder系列速度最快、成本最低的模型。[代码能力（Qwen-Coder）](https://help.aliyun.com/zh/model-studio/qwen-coder)。

代码模型

2026-01-12

qwen3-coder-plus-2025-09-23

相较上一版本（7月22日快照）在下游任务效果和工具调用方面鲁棒性有所提升，代码安全性增强。[代码能力（Qwen-Coder）](https://help.aliyun.com/zh/model-studio/qwen-coder)

代码模型

2026-01-12

qwen3-coder-plus、qwen3-coder-plus-2025-07-22、qwen3-coder-30b-a3b-instruct、qwen3-coder-480b-a35b-instruct

基于 Qwen3 的代码生成模型，具有强大的Coding Agent能力，擅长工具调用和环境交互，代码能力卓越的同时兼具通用能力。[代码能力（Qwen-Coder）](https://help.aliyun.com/zh/model-studio/qwen-coder)

推理模型

2026-01-12

qwen3-30b-a3b-thinking-2507、qwen3-30b-a3b-instruct-2507

是qwen3-30b-a3b的升级版。thinking模型逻辑能力、通用能力、知识增强及创作能力提升，参见[深度思考](https://help.aliyun.com/zh/model-studio/deep-thinking)。instruct模型创作能力与模型安全性提升，参见[概述](https://help.aliyun.com/zh/model-studio/text-generation)。

推理模型

2026-01-12

qwen3-235b-a22b-thinking-2507、qwen3-235b-a22b-instruct-2507

是qwen3-235b-a22b的升级版。thinking模型逻辑能力、通用能力、知识增强及创作能力均有大幅提升，适用于高难度强推理场景，参见[深度思考](https://help.aliyun.com/zh/model-studio/deep-thinking)。instruct模型创作能力与模型安全性均有提升，参见[概述](https://help.aliyun.com/zh/model-studio/text-generation)。

推理模型

2026-01-12

qwen3-235b-a22b、qwen3-30b-a3b、qwen3-32b、qwen3-14b、qwen3-8b

Qwen3 模型支持思考模式和非思考模式，您可以通过 `enable_thinking` 参数实现两种模式的切换。除此之外，Qwen3 模型的能力得到了大幅提升：

1.  推理能力：在数学、代码和逻辑推理等评测中，显著超过 QwQ 和同尺寸的非推理模型，达到同规模业界顶尖水平。
    
2.  人类偏好能力：创意写作、角色扮演、多轮对话、指令遵循能力均大幅提升，通用能力显著超过同尺寸模型。
    
3.  Agent 能力：在推理、非推理两种模式下都达到业界领先水平，能够精准地调用外部工具。
    
4.  多语言能力：支持100多种语言和方言，多语言翻译、指令理解、常识推理能力都明显提升。
    
5.  回复格式问题修复：修复了之前版本存在的回复格式的问题，如异常 Markdown、中间截断、错误输出 boxed 等问题。
    

思考模式请参见[深度思考](https://help.aliyun.com/zh/model-studio/deep-thinking)，非思考模式请参见[概述](https://help.aliyun.com/zh/model-studio/text-generation)。

文字提取

2026-01-12

qwen-vl-ocr-2025-11-20

千问文字提取模型，该快照版基于Qwen3-VL架构，大幅提升文档解析、文字定位能力。[文字提取](https://help.aliyun.com/zh/model-studio/qwen-vl-ocr)

文字提取

2026-01-12

qwen-vl-ocr

qwen-vl-ocr是专用于OCR的模型；在表格、试题等类型图像的文字提取能力大幅提升。详情请参见[文字提取](https://help.aliyun.com/zh/model-studio/qwen-vl-ocr)。

推理模型

2026-01-12

qwen-plus-2025-12-01、qwen-plus-2025-09-11

属于 Qwen3 系列模型，相较于qwen-plus-2025-07-28，在思考模式下提升了指令遵循能力、总结回复更加精简，详见[深度思考](https://help.aliyun.com/zh/model-studio/deep-thinking)。在非思考模式下中文理解与逻辑推理能力得到增强，详见[概述](https://help.aliyun.com/zh/model-studio/text-generation)。

推理模型

2026-01-12

qwen-plus-2025-07-28

属于 Qwen3 系列模型，相较于上一版模型，将上下文长度提高到了1,000,000。思考模式请参见[深度思考](https://help.aliyun.com/zh/model-studio/deep-thinking)，非思考模式请参见[概述](https://help.aliyun.com/zh/model-studio/text-generation)。

推理模型

2026-01-12

qwen-plus

能力均衡，推理效果、成本和速度介于千问Max和千问Flash之间，适合中等复杂任务。模型列表

多语言翻译

2026-01-12

qwen-mt-lite

千问基础级文本翻译大模型，支持31个语种互译，相较于qwen-mt-flash响应更快，成本更低，适用于对延迟敏感的场景。[翻译能力（Qwen-MT）](https://help.aliyun.com/zh/model-studio/machine-translation)

多语言翻译

2026-01-12

qwen-mt-plus、qwen-mt-flash

Qwen-MT模型是基于千问模型优化的机器翻译大语言模型，擅长中英互译、中文与小语种互译、英文与小语种互译，小语种包括日、韩、法、西、德、葡（巴西）、泰、印尼、越、阿等26种。在多语言互译的基础上，提供术语干预、领域提示、记忆库等能力，提升模型在复杂应用场景下的翻译效果。详情请参见[翻译能力（Qwen-MT）](https://help.aliyun.com/zh/model-studio/machine-translation)。

文生文

2026-01-12

qwen-flash、qwen-flash-2025-07-28

千问系列速度最快、成本极低的模型，适合简单任务。模型列表

## 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**模型类型**

**时间**

**模型规格**

**功能说明**

推理模型

2026-05-21

qwen3.7-max、qwen3.7-max-2026-05-20

Qwen Max 系列新一代旗舰模型。仅支持纯文本输入，默认开启思考模式，支持显式缓存，在编程、办公与生产力、长周期自主执行方面均能出色胜任各项任务。

音视频翻译

2026-05-19

qwen3.5-livetranslate-flash-realtime、qwen3.5-livetranslate-flash-realtime-2026-05-19

一款多语言音视频实时翻译模型，可识别 60 种语言，并实时翻译为 29 种语言的音频。[实时语音/音视频翻译-千问](https://help.aliyun.com/zh/model-studio/qwen3-5-livetranslate-flash-realtime)

文生视频

2026-04-27

happyhorse-1.0-t2v

HappyHorse系列文生视频模型，支持有声视频生成，可生成3~15秒、720P/1080P视频。[HappyHorse-文生视频](https://help.aliyun.com/zh/model-studio/happyhorse-text-to-video-api-reference)

图生视频

2026-04-27

happyhorse-1.0-i2v

HappyHorse系列图生视频模型，支持有声视频生成，可生成3~15秒、720P/1080P视频。[HappyHorse-图生视频-基于首帧](https://help.aliyun.com/zh/model-studio/happyhorse-image-to-video-api-reference)

参考生视频

2026-04-27

happyhorse-1.0-r2v

HappyHorse系列参考生视频模型，支持多参考图输入生成有声视频，可生成3~15秒、720P/1080P视频。[HappyHorse-参考生视频](https://help.aliyun.com/zh/model-studio/happyhorse-reference-to-video-api-reference)

视频编辑

2026-04-27

happyhorse-1.0-video-edit

HappyHorse系列视频编辑模型，支持对视频进行编辑处理。[HappyHorse-视频编辑](https://help.aliyun.com/zh/model-studio/happyhorse-video-edit-api-reference)

文生视频

2026-04-26

wan2.7-t2v-2026-04-25

万相2.7-文生视频模型快照版本，模型能力与wan2.7-t2v一致。[万相2.7-文生视频](https://help.aliyun.com/zh/model-studio/text-to-video-api-reference)

图生视频

2026-04-26

wan2.7-i2v-2026-04-25

万相2.7-图生视频模型快照版本，模型能力与wan2.7-i2v一致。[万相2.7-图生视频](https://help.aliyun.com/zh/model-studio/image-to-video-general-api-reference)

图像生成

2026-04-23

qwen-image-2.0-pro-2026-04-22

Qwen-Image-2.0系列模型，实现了图片生成和图片编辑的融合。相较于3月3日快照，本模型在画面质感，尤其是纹理细节、光影、材质上有明显跃升；支持多语言的图内文字生成；艺术风格表现更加均衡。

[千问-文生图](https://help.aliyun.com/zh/model-studio/qwen-image-api)、[千问-图像编辑](https://help.aliyun.com/zh/model-studio/qwen-image-edit-api)

推理模型

2026-04-23

qwen3.5-plus-2026-04-20

Qwen3.5原生视觉语言系列Plus模型新快照，相较2月15日快照Agentic coding能力大幅提升，推理速度显著提升；知识、推理与长上下文能力保持较高水准，适合编码智能体、生产工作流和高吞吐场景。

推理模型

2026-04-23

qwen3.6-27b

Qwen3.6系列27B原生视觉语言Dense模型，相较3.5-27B重点提升Agentic coding能力，STEM与推理能力进一步增强；视觉模态方面空间智能、物体定位与检测能力显著增强，视频理解、文档OCR及视觉Agent能力稳步提升。

推理模型

2026-04-20

qwen3.6-max-preview

Qwen3.6系列规模最大的闭源模型，Coding能力进一步提升、Agent执行更加高效。仅支持纯文本输入，支持思考模式（默认开启），支持显式缓存和Function Calling。[概述](https://help.aliyun.com/zh/model-studio/text-generation)

> 不支持图像与视频输入。

推理模型

2026-04-16

qwen3.6-flash、qwen3.6-flash-2026-04-16、qwen3.6-35b-a3b

Qwen3.6 原生视觉语言 Flash 系列模型，在整体性能上较 Qwen3.5-Flash 显著提升。重点增强了智能体编程能力（在多项代码智能体基准上大幅超越前代）、数学推理和代码推理能力；在视觉能力方面，空间智能显著增强，其中物体定位和目标检测表现尤为突出。[概述](https://help.aliyun.com/zh/model-studio/text-generation)

语音识别

2026-04-16

fun-asr、fun-asr-2025-11-07

Fun-ASR 实时语音识别能力升级：

-   方言支持：覆盖汉语七大方言（官话/吴/湘/赣/客/闽/粤）及 20+ 地区口音
    
-   古诗词优化：提升古诗词识别准确率，适用于文化教育、有声读物等场景
    
-   文本优化：标点预测与文本归一化增强，数字/日期/金额自动转标准格式
    
-   多语种扩展：支持中、英、日、韩、法、德、西班牙等共 30 个语种
    

详情请参见[录音文件识别-Fun-ASR/Paraformer](https://help.aliyun.com/zh/model-studio/recording-file-recognition)

视频编辑

2026-04-03

wan2.7-videoedit

万相2.7-视频编辑模型，支持指令编辑与视频迁移任务，可修改视频局部或整体画面，同时支持多图参考替换及动作、特效、运镜的复刻。[万相2.7-视频编辑](https://help.aliyun.com/zh/model-studio/wan-video-editing-api-reference)

图生视频

2026-04-03

wan2.7-i2v

万相2.7-图生视频模型，支持多模态输入（文本/图像/音频/视频），可完成首帧生视频、首尾帧生视频、视频续写三大任务。[万相2.7-图生视频](https://help.aliyun.com/zh/model-studio/image-to-video-general-api-reference)

文生视频

2026-04-03

wan2.7-t2v

万相2.7-文生视频模型，新增分辨率档位与宽高比自定义设置，支持灵活适配不同创作场景与平台发布需求。[万相2.7-文生视频](https://help.aliyun.com/zh/model-studio/text-to-video-api-reference)

参考生视频

2026-04-03

wan2.7-r2v

万相2.7参考生视频模型，支持主体参考和音色定制，并可输入单张多宫格故事板直接生成剧本化视频。[万相2.7-参考生视频](https://help.aliyun.com/zh/model-studio/wan-video-to-video-api-reference)

推理模型

2026-04-02

qwen3.6-plus、qwen3.6-plus-2026-04-02

千问3.6-Plus，代码开发能力重点升级（Agentic Coding、前端编程等），Vibe Coding体验显著提升；泛化场景推理能力进一步增强；多模态方面，万物识别、OCR、物体定位等能力显著提升；同时修复了Qwen3.5-Plus上线后的已知问题。使用方法与qwen3.5-plus一致。[概述](https://help.aliyun.com/zh/model-studio/text-generation)

图像生成与编辑

2026-04-01

wan2.7-image-pro、wan2.7-image

万相2.7-图像生成与编辑模型，支持文生图、文生组图、图生组图、图像编辑、多图参考生成、交互式编辑，在文字渲染、主体一致性、复杂指令遵循表现更优。Pro系列支持4K输出；加速版兼顾效果与响应速度。[万相-图像生成与编辑2.7](https://help.aliyun.com/zh/model-studio/wan-image-generation-and-editing-api-reference)

全模态

2026-03-30

qwen3.5-omni-plus、qwen3.5-omni-plus-2026-03-15、qwen3.5-omni-flash、qwen3.5-omni-flash-2026-03-15

最新一代全模态大模型，支持长视频分析、会议纪要、字幕输出、安全审核、音视频交互；支持音视频内容的深度理解与生成描述，支持 113 种语言识别和 36 种语言的音频生成，可处理 3 小时音频及1 小时视频输入，支持联网搜索及指令来控制输出音频的音量、语速、情绪。[非实时（Qwen-Omni）](https://help.aliyun.com/zh/model-studio/qwen-omni)

全模态

2026-03-30

qwen3.5-omni-plus-realtime、qwen3.5-omni-plus-realtime-2026-03-15、qwen3.5-omni-flash-realtime、qwen3.5-omni-flash-realtime-2026-03-15

千问最新推出的实时多模态模型，相比于上一代的 Qwen3-Omni-Flash-Realtime：模型智力大幅提升，与 Qwen3.5-Plus 智能水平相当。原生支持联网搜索（WebSearch），支持语音打断和控制；支持 113 种语种和方言的语音识别，以及 36 种语种和方言的语音生成。[实时（Qwen-Omni-Realtime）](https://help.aliyun.com/zh/model-studio/realtime)

推理模型

2026-03-20

deepseek-v3.2

DeepSeek-V3.2是引入DeepSeek Sparse Attention（一种稀疏注意力机制）的正式版模型，也是DeepSeek推出的首个将思考融入工具使用的模型，同时支持思考模式与非思考模式的工具调用。

[DeepSeek -阿里云](https://help.aliyun.com/zh/model-studio/deepseek-api)

图像生成与编辑

2026-03-03

qwen-image-2.0、qwen-image-2.0-2026-03-03、qwen-image-2.0-pro、qwen-image-2.0-pro-2026-03-03

千问-Image2.0系列，同时支持图像生成和编辑。Pro系列文字渲染、真实质感、语义遵循能力更强。；加速版兼顾效果与响应速度。[千问-文生图](https://help.aliyun.com/zh/model-studio/qwen-image-api)、[千问-图像编辑](https://help.aliyun.com/zh/model-studio/qwen-image-edit-api)

语音识别

2026-03-03

qwen3-asr-flash-2026-02-10

千问录音文件识别新增快照模型，较 qwen3-asr-flash-2025-09-08 效果更优。[非实时语音识别](https://help.aliyun.com/zh/model-studio/non-realtime-speech-recognition-user-guide)

推理模型

2026-02-24

qwen3.5-flash、qwen3.5-flash-2026-02-23、qwen3.5-122b-a10b、qwen3.5-27b、qwen3.5-35b-a3b

阿里巴巴推出的最新模型千问3.5-Flash和开源模型，支持文本、图像和视频输入，响应速度快，综合表现接近qwen3.5-plus，支持内置[工具调用](https://help.aliyun.com/zh/model-studio/tool-calls/)。[概述](https://help.aliyun.com/zh/model-studio/text-generation)

代码模型

2026-02-20

qwen3-coder-next

Qwen3系列新一代开源代码生成模型，支持多轮工具交互，提升了对仓库级别代码的理解能力和对AI编程工具的适配性。[代码能力（Qwen-Coder）](https://help.aliyun.com/zh/model-studio/qwen-coder)

推理模型

2026-02-16

qwen3.5-plus、qwen3.5-plus-2026-02-15、qwen3.5-397b-a17b

阿里巴巴推出的最新模型千问3.5-Plus和开源模型，支持文本、图像和视频输入，在语言理解、逻辑推理、代码生成、智能体任务、图像理解、视频理解、图形用户界面（GUI）等多种任务中表现卓越，支持内置工具调用。[概述](https://help.aliyun.com/zh/model-studio/text-generation)

语音识别

2026-02-13

qwen3-asr-flash-realtime-2026-02-10

千问实时语音识别新增最新快照模型，较 qwen3-asr-flash-realtime-2025-10-27 效果更优。[实时语音识别](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition-user-guide)

语音合成

2026-02-10

cosyvoice-v3-plus、cosyvoice-v3-flash

语音合成 CosyVoice 新增 v3 模型，支持使用系统音色和复刻音色进行语音合成。[实时语音合成-CosyVoice /Sambert](https://help.aliyun.com/zh/model-studio/text-to-speech)

语音合成

2026-02-10

qwen3-tts-instruct-flash、qwen3-tts-instruct-flash-2026-01-26

千问语音合成上线Instruct（指令控制）模型，支持通过自然语言指令精准控制合成效果。[非实时语音合成](https://help.aliyun.com/zh/model-studio/non-realtime-tts-user-guide)

语音合成

2026-02-10

qwen3-tts-vd-2026-01-26

千问语音合成上线声音设计模型，可通过文本描述创建定制化音色。[非实时语音合成](https://help.aliyun.com/zh/model-studio/non-realtime-tts-user-guide)

语音合成

2026-02-10

qwen3-tts-vc-2026-01-22

千问语音合成上线声音复刻模型，可基于真实音频样本快速复刻音色。[非实时语音合成](https://help.aliyun.com/zh/model-studio/non-realtime-tts-user-guide)

语音合成

2026-02-04

qwen3-tts-instruct-flash-realtime、qwen3-tts-instruct-flash-realtime-2026-01-22

千问实时语音合成新增Instruct（指令控制）模型，支持通过自然语言指令精准控制合成效果。[实时语音合成](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide)

参考生视频

2026-02-02

wan2.6-r2v-flash

基于参考视频和图像的角色形象，生成多镜头视频，支持自动配音。[万相2.7-参考生视频](https://help.aliyun.com/zh/model-studio/wan-video-to-video-api-reference)

视觉理解

2026-01-28

qwen3-vl-flash-2026-01-22

千问VL的全新快照版模型，有效融合了思考模式与非思考模式，相较于 2025 年 10 月 15 日的快照版本，显著提升了模型的整体性能，在通用视觉识别、安防、巡店、巡检、拍照解题等业务场景中实现了更高准确率的推理。[图像与视频理解](https://help.aliyun.com/zh/model-studio/vision)

语音识别

2026-01-28

qwen3-asr-flash-filetrans、qwen3-asr-flash-filetrans-2025-11-17

千问3-ASR-Flash-Filetrans系列模型现已支持词级别时间戳，通过设置新参数 `enable_words`，获取毫秒级的词/字对齐信息，并体验更符合语义的精细化断句。[非实时语音识别](https://help.aliyun.com/zh/model-studio/non-realtime-speech-recognition-user-guide)

推理模型

2026-01-27

qwen3-max-2026-01-23

相较于 2025 年 9 月 23 日的快照版本，有效融合了思考模式与非思考模式，显著提升了模型的整体性能。在思考模式下，模型集成了 Web 搜索、网页信息提取和代码解释器三项工具，通过在思考过程中引入外部工具，在复杂问题上实现更高的准确率。[OpenAI兼容-Responses](https://help.aliyun.com/zh/model-studio/compatibility-with-openai-responses-api)

图生视频

2026-01-18

wan2.6-i2v-flash

支持生成有声与无声视频，两类视频按各自计费规则独立计费；同时具备多镜头叙事能力与音频处理能力。[万相-图生视频-基于首帧（2.1-2.6）](https://help.aliyun.com/zh/model-studio/legacy-image-to-video-api-reference/)

图像编辑

2026-01-18

qwen-image-edit-max、qwen-image-edit-max-2026-01-16

千问图像编辑模型Max系列，具备更稳定、丰富的编辑能力，增强了工业设计与几何推理能力，并提升了角色一致性与编辑的精准度。[图像编辑-千问](https://help.aliyun.com/zh/model-studio/qwen-image-edit-guide)

语音合成

2026-01-16

qwen3-tts-vc-realtime-2026-01-15

千问实时语音合成新增最新快照模型，[声音复刻（Qwen）](https://help.aliyun.com/zh/model-studio/qwen-tts-voice-cloning)效果进一步优化，较 qwen3-tts-vc-realtime-2025-11-27 更自然、更贴近原声。[实时语音合成](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide)

文生图

2026-01-12

qwen-image-plus-2026-01-09

千问图像生成的全新快照版模型，为qwen-image-max的蒸馏加速版，支持快速生成高质量图像。[千问-文生图](https://help.aliyun.com/zh/model-studio/qwen-image-api)

语音识别

2026-01-06

qwen3-asr-flash、qwen3-asr-flash-2025-09-08

千问3-ASR-Flash支持OpenAI兼容模式。[非实时语音识别](https://help.aliyun.com/zh/model-studio/non-realtime-speech-recognition-user-guide)

文生图

2025-12-31

qwen-image-max、qwen-image-max-2025-12-30

千问图像生成模型Max系列，相较于Plus系列提升了图像的真实感与自然度，有效降低了AI合成痕迹，在人物质感、纹理细节和文字渲染等方面表现突出。[千问-文生图](https://help.aliyun.com/zh/model-studio/qwen-image-api)

图像编辑

2025-12-23

qwen-image-edit-plus-2025-12-15

千问图像编辑发布的最新快照模型，相较于上一版本提升了角色一致性、工业设计能力和几何推理能力，并优化了编辑后的图片与原图在空间布局、纹理和风格上的匹配度，编辑效果更精准。[图像编辑-千问](https://help.aliyun.com/zh/model-studio/qwen-image-edit-guide)

文生图

2025-12-22

z-image-turbo

轻量级文生图模型，可快速生成高质量图像，支持中英双语渲染、复杂语义理解和多风格题材，并可灵活适配多种分辨率与宽高比。[文生图Z-Image](https://help.aliyun.com/zh/model-studio/z-image-api-reference)

视觉理解

2025-12-19

qwen3-vl-plus-2025-12-19

千问VL的全新快照版模型，指令遵循能力更强，具有更低的延迟。[图像与视频理解](https://help.aliyun.com/zh/model-studio/vision)

语音识别

2025-12-19

qwen3-asr-flash-filetrans、qwen3-asr-flash-filetrans-2025-11-17、qwen3-asr-flash、qwen3-asr-flash-2025-09-08

新增捷克语、丹麦语等共 9 种语言的语音识别支持。[非实时语音识别](https://help.aliyun.com/zh/model-studio/non-realtime-speech-recognition-user-guide)

语音识别

2025-12-17

qwen3-asr-flash-realtime、qwen3-asr-flash-realtime-2025-10-27

新增捷克语、丹麦语等共 9 种语言的语音识别支持。[实时语音识别](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition-user-guide)

语音识别

2025-12-17

qwen3-asr-flash、qwen3-asr-flash-2025-09-08

支持任意采样率和声道的音频。[非实时语音识别](https://help.aliyun.com/zh/model-studio/non-realtime-speech-recognition-user-guide)

语音识别

2025-12-17

fun-asr-mtl、fun-asr-mtl-2025-08-25

支持对中、英、日、韩等共 31 种语言的语音识别，尤其适合东南亚出海场景。[录音文件识别-Fun-ASR/Paraformer](https://help.aliyun.com/zh/model-studio/recording-file-recognition)

声音设计

2025-12-16

qwen-voice-design

千问发布声音设计模型，通过文本描述生成定制化音色。结合qwen3-tts-vd-realtime-2025-12-16模型使用生成语音，覆盖 10 种语言。[声音设计（Qwen）](https://help.aliyun.com/zh/model-studio/qwen-tts-voice-design)

语音合成

2025-12-16

qwen3-tts-vd-realtime-2025-12-16（快照版）

千问实时语音合成发布全新快照版模型，可使用[声音设计（Qwen）](https://help.aliyun.com/zh/model-studio/qwen-tts-voice-design)生成的音色进行低延迟、高稳定性的实时合成；支持多语言输出；能根据文本自动调节语气，并优化复杂文本的合成表现。[实时语音合成](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide)

文生图

2025-12-16

wan2.6-t2i

新增同步接口。支持在总像素面积与宽高比约束内，自由选尺寸。[万相-文生图V2](https://help.aliyun.com/zh/model-studio/text-to-image-v2-api-reference)

图像生成与编辑

2025-12-16

wan2.6-image

支持图像编辑和图文混合输出。[万相-图像生成与编辑2.6](https://help.aliyun.com/zh/model-studio/wan-image-generation-api-reference)

图生视频-基于首帧

2025-12-16

wan2.6-i2v

新增多镜头叙事能力，支持音频能力，支持自动配音，或传入自定义音频文件。[万相-图生视频-基于首帧（2.1-2.6）](https://help.aliyun.com/zh/model-studio/legacy-image-to-video-api-reference/)

参考生视频

2025-12-16

wan2.6-r2v

基于参考视频的角色形象和音色，生成多镜头视频，支持自动配音。[万相2.7-参考生视频](https://help.aliyun.com/zh/model-studio/wan-video-to-video-api-reference)

文生视频

2025-12-16

wan2.6-t2v

新增多镜头叙事能力，支持音频能力，支持自动配音，或传入自定义音频文件。[文生视频](https://help.aliyun.com/zh/model-studio/text-to-video-api-reference)

语音识别

2025-12-12

fun-asr、fun-asr-2025-11-07

录音文件识别-Fun-ASR功能更新：

-   支持歌唱识别，能实现整首歌曲的转写，详情请参见[录音文件识别-Fun-ASR/Paraformer](https://help.aliyun.com/zh/model-studio/recording-file-recognition)。
    

全模态

2025-12-04

qwen3-omni-flash-2025-12-01

千问Omni发布的最新快照模型，支持的音色增加至49种，模型的指令跟随能力大幅升级，能高效理解文本、图像、音频、视频。[非实时（Qwen-Omni）](https://help.aliyun.com/zh/model-studio/qwen-omni)

实时多模态

2025-12-04

qwen3-omni-flash-realtime**\-**2025-12-01

千问Omni 实时版发布的最新快照模型，提供了低延迟的多模态交互能力，支持的音色增加至49种，模型的指令跟随能力和交互体验大幅升级。[实时（Qwen-Omni-Realtime）](https://help.aliyun.com/zh/model-studio/realtime)

语音翻译

2025-12-04

qwen3-livetranslate-flash、qwen3-livetranslate-flash-2025-12-01

千问3-LiveTranslate-Flash 是音视频翻译模型，支持 18 种语言（包括中文、英文、俄文、法文等）互译，可结合视觉上下文提升翻译准确性，并输出文本与语音。[音视频文件翻译-千问](https://help.aliyun.com/zh/model-studio/qwen3-livetranslate-flash)

多语言翻译

2025-12-02

qwen-mt-lite

千问基础级文本翻译大模型，支持31个语种互译，相较于qwen-mt-flash响应更快，成本更低，适用于等对延迟敏感的场景。[翻译能力（Qwen-MT）](https://help.aliyun.com/zh/model-studio/machine-translation)

声音复刻

2025-11-27

qwen-voice-enrollment

千问发布声音复刻模型，仅需 5 秒以上音频即可快速生成高相似度声音。结合qwen3-tts-vc-realtime-2025-11-27模型使用，可高保真复刻并实时输出某人的声音，覆盖 11 种语言。[声音复刻（Qwen）](https://help.aliyun.com/zh/model-studio/qwen-tts-voice-cloning)

语音合成

2025-11-27

qwen3-tts-vc-realtime-2025-11-27（快照版）

千问实时语音合成发布全新快照版模型，可使用[声音复刻（Qwen）](https://help.aliyun.com/zh/model-studio/qwen-tts-voice-cloning)生成的音色进行低延迟、高稳定性的实时合成；支持多语言输出；能根据文本自动调节语气，并优化复杂文本的合成表现。[实时语音合成](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide)

语音合成

2025-11-27

qwen3-tts-flash-realtime-2025-11-27（快照版）

千问实时语音合成发布全新快照版模型，低延迟且稳定性高；音色更丰富，同一音色支持多语言输出；能根据文本自动调节语气，并提升复杂文本的合成表现。[实时语音合成](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide)

语音合成

2025-11-27

qwen3-tts-flash-2025-11-27（快照版）

千问语音合成发布全新快照版模型，音色更丰富；同一音色支持多语言输出；可自适应文本调节语气，并优化复杂文本的合成能力。[非实时语音合成](https://help.aliyun.com/zh/model-studio/non-realtime-tts-user-guide)

文字提取

2025-11-21

qwen-vl-ocr-2025-11-20（快照版）

千问文字提取模型，该快照版基于Qwen3-VL架构，大幅提升文档解析、文字定位能力。[文字提取](https://help.aliyun.com/zh/model-studio/qwen-vl-ocr)

语音识别

2025-11-20

qwen3-asr-flash-filetrans、qwen3-asr-flash-filetrans-2025-11-17（快照版）

千问录音文件识别发布了新模型，专为音频文件的异步转写设计，支持最长12小时录音。[非实时语音识别](https://help.aliyun.com/zh/model-studio/non-realtime-speech-recognition-user-guide)

语音识别

2025-11-19

fun-asr-2025-11-07（快照版）

Fun-ASR录音文件识别发布了全新快照版模型，优化远场语音活动检测（VAD）以提升识别准确率与稳定性，并在原有中英文识别基础上新增支持中文多地方言及日语。[录音文件识别-Fun-ASR/Paraformer](https://help.aliyun.com/zh/model-studio/recording-file-recognition)

多语言翻译

2025-11-11

qwen-mt-flash

相较于qwen-mt-turbo支持流式增量输出，整体性能表现有所提升。[翻译能力（Qwen-MT）](https://help.aliyun.com/zh/model-studio/machine-translation)

图生视频

2025-11-10

wan2.2-animate-move

支持将模板视频中角色的动作和表情，迁移至单张静态人物图片上，生成人物动作视频。[万相-图生动作](https://help.aliyun.com/zh/model-studio/wan-animate-move-api)

图生视频

2025-11-10

wan2.2-animate-mix

能够依据人物图片和参考视频，将视频中的主角替换为图片中的角色，同时保留原视频的场景、光照和色调，实现无缝人物替换。[万相-视频换人](https://help.aliyun.com/zh/model-studio/wan-animate-mix-api)

推理模型

2025-11-03

qwen3-max-preview

qwen3-max-preview 模型的思考模式：在整体推理能力上显著提升，尤其在智能体编程、常识推理，以及数学、科学和通用任务方面表现更优。[深度思考](https://help.aliyun.com/zh/model-studio/deep-thinking)

图像编辑

2025-10-31

qwen-image-edit-plus、qwen-image-edit-plus-2025-10-30

在qwen-image-edit的基础上优化了推理性能与系统稳定性，大幅缩短图像生成与编辑的响应时间，且支持单次请求返回多张图片。[图像编辑-千问](https://help.aliyun.com/zh/model-studio/qwen-image-edit-guide)

推理模型

2025-10-31

qwen3-next-80b-a3b-thinking、qwen3-next-80b-a3b-instruct

基于Qwen3的新一代开源模型，thinking模型相较于qwen3-235b-a22b-thinking-2507提升了指令遵循能力，总结回复更加精简，详见[深度思考](https://help.aliyun.com/zh/model-studio/deep-thinking)。instruct模型相较于qwen3-235b-a22b-instruct-2507增强了中文理解、逻辑推理及文本生成能力，详见[概述](https://help.aliyun.com/zh/model-studio/text-generation)。

实时语音识别

2025-10-27

qwen3-asr-flash-realtime、qwen3-asr-flash-realtime-2025-10-27

千问实时语音识别大模型具备自动语种识别功能，可识别 11 种语音类型，并能在复杂音频环境下较为准确地转录。[实时语音识别](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition-user-guide)

文本、图像、视频、语音等

2025-09-23

模型列表

新加坡地域首次上线。

## 美国

服务部署范围为[美国](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于美国境内；静态数据存储于您所选的地域。该部署范围支持的地域：美国（弗吉尼亚）。

**模型类型**

**时间**

**模型规格**

**功能说明**

多语言翻译

2026-04-10

qwen-mt-lite-us

千问基础级文本翻译大模型，支持31个语种互译，相较于qwen-mt-flash响应更快，成本更低，适用于对延迟敏感的场景。[翻译能力（Qwen-MT）](https://help.aliyun.com/zh/model-studio/machine-translation)

图生视频-基于首帧

2026-01-12

wan2.6-i2v-us

新增多镜头叙事能力，支持音频能力，支持自动配音，或传入自定义音频文件。[万相-图生视频-基于首帧（2.1-2.6）](https://help.aliyun.com/zh/model-studio/legacy-image-to-video-api-reference/)

文生视频

2026-01-12

wan2.6-t2v-us

新增多镜头叙事能力，支持音频能力，支持自动配音，或传入自定义音频文件。[万相2.7-文生视频](https://help.aliyun.com/zh/model-studio/text-to-video-api-reference)

语音识别

2026-01-12

qwen3-asr-flash-us、qwen3-asr-flash-2025-09-08-us

支持任意采样率和声道的音频。[非实时语音识别](https://help.aliyun.com/zh/model-studio/non-realtime-speech-recognition-user-guide)

视觉理解

2026-01-12

qwen3-vl-flash-us、qwen3-vl-flash-2025-10-15-us

Qwen3系列小尺寸视觉理解模型，实现思考模式和非思考模式的有效融合，相较于开源版Qwen3-VL-30B-A3B，效果更优，响应速度更快。[图像与视频理解](https://help.aliyun.com/zh/model-studio/vision)

推理模型

2026-01-12

qwen-plus-2025-12-01-us

属于 Qwen3 系列模型，相较于qwen-plus-2025-07-28，在思考模式下提升了指令遵循能力、总结回复更加精简，详见[深度思考](https://help.aliyun.com/zh/model-studio/deep-thinking)。在非思考模式下中文理解与逻辑推理能力得到增强，详见[概述](https://help.aliyun.com/zh/model-studio/text-generation)。

推理模型

2026-01-12

qwen-plus-us

能力均衡，推理效果、成本和速度介于千问Max和千问Flash之间，适合中等复杂任务。模型列表

文生文

2026-01-12

qwen-flash-us、qwen-flash-2025-07-28-us

千问系列速度最快、成本极低的模型，适合简单任务。模型列表

## 欧盟

服务部署范围为[欧盟](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于欧盟境内；静态数据存储于您所选的地域。该部署范围支持的地域：德国（法兰克福）。

**模型类型**

**时间**

**模型规格**

**功能说明**

推理模型

2026-05-07

qwen3-max、qwen3-max-2026-01-23

相较于 2025 年 9 月 23 日的快照版本，有效融合了思考模式与非思考模式，显著提升了模型的整体性能。

推理模型

2026-05-07

qwen-plus、qwen-plus-2025-12-01

属于 Qwen3 系列模型，相较于qwen-plus-2025-07-28，在思考模式下提升了指令遵循能力、总结回复更加精简，详见[深度思考](https://help.aliyun.com/zh/model-studio/deep-thinking)。在非思考模式下中文理解与逻辑推理能力得到增强，详见[概述](https://help.aliyun.com/zh/model-studio/text-generation)。

推理模型

2026-05-07

qwen3.5-flash、qwen3.5-flash-2026-02-23

阿里巴巴推出的最新模型千问3.5-Flash和开源模型，支持文本、图像和视频输入，响应速度快。[概述](https://help.aliyun.com/zh/model-studio/text-generation)

视觉理解

2026-05-07

qwen3-vl-plus、qwen3-vl-flash、qwen3-vl-flash-2025-10-15

Qwen3系列视觉理解模型，实现思考模式和非思考模式的有效融合，视觉智能体能力达到世界顶尖水平。此版本在视觉编码、空间感知、多模态思考等方向全面升级；视觉感知与识别能力大幅提升，指令遵循能力更强，具有更低的延迟。[图像与视频理解](https://help.aliyun.com/zh/model-studio/vision)

代码能力

2026-05-07

qwen3-coder-next

Qwen3系列新一代开源代码生成模型，支持多轮工具交互，提升了对仓库级别代码的理解能力和对AI编程工具的适配性。[代码能力（Qwen-Coder）](https://help.aliyun.com/zh/model-studio/qwen-coder)
