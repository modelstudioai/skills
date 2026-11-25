# 语音识别概述

百炼语音识别支持实时音频和录音文件转写，提供多语言与方言、热词与上下文、文本润色、说话人分离等能力。

<a id="功能介绍"></a>

<a id="asr-capabilities"></a>

## 功能介绍

语音识别将音视频中的语音转换为文本，可用于语音输入、实时字幕、会议记录和通话分析等场景。百炼支持持续输入音频的实时识别，以及提交完整音频文件的非实时识别；不同模型支持的语言、方言和增强能力有所不同。

<a id="模型选型"></a>

<a id="mg1a2b3c4d5e02"></a>

<a id="mg1a2b3c4d5e01"></a>

<a id="asr_decide02"></a>

<a id="asr_decide01"></a>

<a id="asr_rec02"></a>

<a id="asr_rec01"></a>

## 模型选型

按音频输入方式、业务场景和结果返回需求选择模型。以下推荐使用 Qwen-Audio 3.1 系列。

<table><thead><tr><th><strong>类型</strong></th><th><strong>使用场景</strong></th><th><strong>推荐模型</strong></th><th><strong>主要区别</strong></th></tr></thead><tbody><tr><td rowspan="2"><p>实时</p></td><td><p>实时字幕、会议记录等持续转写</p></td><td><p><a href="https://bailian.console.aliyun.com/cn-beijing/model/market/detail/qwen-audio-3.1-asr-flash-streaming">qwen-audio-3.1-asr-flash-streaming</a></p></td><td><p>持续发送音频，同时接收中间结果和最终结果。</p></td></tr><tr><td><p>输入法、语音消息等短段语音输入</p></td><td><p><a href="https://bailian.console.aliyun.com/cn-beijing/model/market/detail/qwen-audio-3.1-asr-flash-message">qwen-audio-3.1-asr-flash-message</a></p></td><td><p>默认返回句子最终结果，可分别开启中间结果和文本润色。</p></td></tr><tr><td rowspan="2"><p>非实时</p></td><td><p>5 分钟以内的短音频文件</p></td><td><p><a href="https://bailian.console.aliyun.com/cn-beijing/model/market/detail/qwen-audio-3.1-asr-flash">qwen-audio-3.1-asr-flash</a></p></td><td><p>在当前请求中获取识别结果，可选择 SSE 流式输出。</p></td></tr><tr><td><p>长录音、后台音视频转写</p></td><td><p><a href="https://bailian.console.aliyun.com/cn-beijing/model/market/detail/qwen-audio-3.1-asr-flash-filetrans">qwen-audio-3.1-asr-flash-filetrans</a></p></td><td><p>提交异步任务，完成后下载转写结果文件。</p></td></tr></tbody></table>

<a id="识别方式"></a>

<a id="b1a2c3d4e5f08"></a>

<a id="b1a2c3d4e5f07"></a>

<a id="asr-input-and-output"></a>

## 识别方式

| 识别方式 | 音频输入 | 结果返回 |
| --- | --- | --- |
| [实时语音识别](real-time-speech-recognition-user-guide.md) | 分块持续发送音频，适合在说话过程中展示转写。 | 发送音频的同时接收识别结果；中间结果、最终结果的返回方式随模型而异。 |
| [非实时语音识别](non-realtime-speech-recognition-user-guide.md) | 一次提交完整音频或音视频文件，适合处理已有录音。 | 同步调用在当前请求中返回结果，支持 SSE 的模型可分次输出；异步调用先返回任务 ID，完成后获取结果文件。 |

<a id="识别效果与结果"></a>

<a id="asr-results-and-quality"></a>

## 识别效果与结果

选定模型后，可根据业务需要改善特定词汇的识别、文本可读性及结构化结果。具体配置方法参见[实时语音识别](real-time-speech-recognition-user-guide.md#rt03_advanced_h2)或[非实时语音识别](non-realtime-speech-recognition-user-guide.md#nrt03_advanced_h2)。

-   **热词与上下文**：
    
    <a id="b1a2c3d4e5f51"></a>
    
     
    
    <a id="b1a2c3d4e5f50"></a>
    
    热词提供人名、品牌名等词汇的目标写法；上下文补充前几轮对话及业务背景。使用方法、支持范围和调优参见[提升识别准确率](improve-asr-accuracy.md)。
    
-   **文本润色**：
    
    <a id="asr-text-refinement"></a>
    
     整理口语中的语气词、重复和自我纠正。qwen-audio-3.1-asr-flash-message 和 qwen-audio-3.1-asr-flash 支持原生文本润色。
    
-   **保留方言表达**：
    
    <a id="asr-dialect-expression"></a>
    
     qwen-audio-3.1-asr-flash-streaming、qwen-audio-3.1-asr-flash-message、qwen-audio-3.1-asr-flash、qwen-audio-3.1-asr-flash-filetrans 支持保留方言特有表达。识别某种方言与保留其文本表达是不同的能力。
    
-   **说话人分离**：
    
    <a id="b1a2c3d4e5f5b"></a>
    
     
    
    <a id="b1a2c3d4e5f5a"></a>
    
    为转写结果标注说话人编号，用于区分会议、访谈中的发言人。qwen-audio-3.1-asr-flash 和 qwen-audio-3.1-asr-flash-filetrans 支持该能力。
    
-   **时间戳**：
    
    <a id="asr-timestamps"></a>
    
     将句子或字词与音频位置对应，用于字幕对齐、关键词高亮和音频跳转。
    
-   **敏感词过滤**：
    
    <a id="asr-sensitive-filter"></a>
    
     将指定词汇替换为星号或从转写文本中移除。
    

音频准备、连接与并发管理、异步作业及异常处理，参见[语音识别最佳实践](speech-recognition-best-practices.md)。

<a id="模型与语言"></a>

<a id="asr_all02"></a>

<a id="asr_all01"></a>

## 模型与语言

以下按模型系列和版本列出支持的语言与方言。

<a id="qa30st_sec02"></a>

<a id="qa30st_sec01"></a>

<a id="accordion-qwen-audio-asr-streaming"></a>

Qwen-Audio-ASR-Streaming

-   qwen-audio-3.1-asr-flash-streaming、qwen-audio-3.0-asr-flash-streaming：中文（普通话、粤语、吴语、闽南语、客家话、赣语、湘语、晋语；并支持中原、西南、冀鲁、江淮、兰银、胶辽、东北、北京、港台等，包括河南、陕西、湖北、四川、重庆、云南、贵州、广东、广西、河北、天津、山东、安徽、南京、江苏、杭州、甘肃、宁夏等地区官话口音）、英语、日语、韩语、越南语、泰语、印尼语、马来语、菲律宾语、印地语、阿拉伯语、法语、德语、西班牙语、葡萄牙语、俄语、意大利语、荷兰语、瑞典语、丹麦语、芬兰语、挪威语、希腊语、波兰语、捷克语、匈牙利语、罗马尼亚语、保加利亚语、克罗地亚语、斯洛伐克语

<a id="asr_message_h3"></a>

<a id="accordion-qwen-audio-asr-message"></a>

Qwen-Audio-ASR-Message

-   qwen-audio-3.1-asr-flash-message：中文（普通话、粤语、吴语、闽南语、客家话、赣语、湘语、晋语；并支持中原、西南、冀鲁、江淮、兰银、胶辽、东北、北京、港台等，包括河南、陕西、湖北、四川、重庆、云南、贵州、广东、广西、河北、天津、山东、安徽、南京、江苏、杭州、甘肃、宁夏等地区官话口音）、英语、日语、韩语、越南语、泰语、印尼语、马来语、菲律宾语、印地语、阿拉伯语、法语、德语、西班牙语、葡萄牙语、俄语、意大利语、荷兰语、瑞典语、丹麦语、芬兰语、挪威语、希腊语、波兰语、捷克语、匈牙利语、罗马尼亚语、保加利亚语、克罗地亚语、斯洛伐克语

<a id="qa30fl_sec02"></a>

<a id="qa30fl_sec01"></a>

<a id="accordion-qwen-audio-asr"></a>

Qwen-Audio-ASR

-   qwen-audio-3.1-asr-flash：中文（普通话、粤语、吴语、闽南语、客家话、赣语、湘语、晋语；并支持中原、西南、冀鲁、江淮、兰银、胶辽、东北、北京、港台等，包括河南、陕西、湖北、四川、重庆、云南、贵州、广东、广西、河北、天津、山东、安徽、南京、江苏、杭州、甘肃、宁夏等地区官话口音）、英语、日语、韩语、越南语、泰语、印尼语、马来语、菲律宾语、印地语、阿拉伯语、法语、德语、西班牙语、葡萄牙语、俄语、意大利语、荷兰语、瑞典语、丹麦语、芬兰语、挪威语、希腊语、波兰语、捷克语、匈牙利语、罗马尼亚语、保加利亚语、克罗地亚语、斯洛伐克语、土耳其语、波斯语、马拉地语、马拉雅拉姆语、尼泊尔语、吉尔吉斯语、阿塞拜疆语、格鲁吉亚语、亚美尼亚语、斯洛文尼亚语、阿尔巴尼亚语、爱沙尼亚语、拉脱维亚语、立陶宛语、加泰罗尼亚语、巴斯克语、加利西亚语、奥里亚语、迪维希语、阿萨姆语、北库尔德语、提格雷语、西弗里西亚语、巴什基尔语、白俄罗斯语、鞑靼语、国际语、草原马里语、道本语
-   qwen-audio-3.0-asr-flash：中文（普通话、粤语、吴语、闽南语、客家话、赣语、湘语、晋语；并支持中原、西南、冀鲁、江淮、兰银、胶辽、东北、北京、港台等，包括河南、陕西、湖北、四川、重庆、云南、贵州、广东、广西、河北、天津、山东、安徽、南京、江苏、杭州、甘肃、宁夏等地区官话口音）、英语、日语、韩语、越南语、泰语、印尼语、马来语、菲律宾语、印地语、阿拉伯语、法语、德语、西班牙语、葡萄牙语、俄语、意大利语、荷兰语、瑞典语、丹麦语、芬兰语、挪威语、希腊语、波兰语、捷克语、匈牙利语、罗马尼亚语、保加利亚语、克罗地亚语、斯洛伐克语

<a id="qa30ft_sec02"></a>

<a id="qa30ft_sec01"></a>

<a id="accordion-qwen-audio-asr-filetrans"></a>

Qwen-Audio-ASR-Filetrans

-   qwen-audio-3.1-asr-flash-filetrans、qwen-audio-3.0-asr-flash-filetrans：中文（普通话、粤语、吴语、闽南语、客家话、赣语、湘语、晋语；并支持中原、西南、冀鲁、江淮、兰银、胶辽、东北、北京、港台等，包括河南、陕西、湖北、四川、重庆、云南、贵州、广东、广西、河北、天津、山东、安徽、南京、江苏、杭州、甘肃、宁夏等地区官话口音）、英语、日语、韩语、越南语、泰语、印尼语、马来语、菲律宾语、印地语、阿拉伯语、法语、德语、西班牙语、葡萄牙语、俄语、意大利语、荷兰语、瑞典语、丹麦语、芬兰语、挪威语、希腊语、波兰语、捷克语、匈牙利语、罗马尼亚语、保加利亚语、克罗地亚语、斯洛伐克语

<a id="asr_fa02"></a>

<a id="asr_fa01"></a>

<a id="accordion-fun-asr"></a>

Fun-ASR

-   fun-asr-realtime：中文（普通话、粤语、吴语、闽南语、客家话、赣语、湘语、晋语；并支持中原、西南、冀鲁、江淮、兰银、胶辽、东北、北京、港台等，包括河南、陕西、湖北、四川、重庆、云南、贵州、广东、广西、河北、天津、山东、安徽、南京、江苏、杭州、甘肃、宁夏等地区官话口音）、英语、日语、韩语、越南语、泰语、印尼语、马来语、菲律宾语、印地语、阿拉伯语、法语、德语、西班牙语、葡萄牙语、俄语、意大利语、荷兰语、瑞典语、丹麦语、芬兰语、挪威语、希腊语、波兰语、捷克语、匈牙利语、罗马尼亚语、保加利亚语、克罗地亚语、斯洛伐克语
-   fun-asr-realtime-2026-02-28：中文（普通话、粤语、吴语、闽南语、客家话、赣语、湘语、晋语；并支持中原、西南、冀鲁、江淮、兰银、胶辽、东北、北京、港台等，包括河南、陕西、湖北、四川、重庆、云南、贵州、广东、广西、河北、天津、山东、安徽、南京、江苏、杭州、甘肃、宁夏等地区官话口音）、英语、日语
-   fun-asr-flash-8k-realtime、fun-asr-flash-8k-realtime-2026-01-28：中文
-   fun-asr：中文（普通话、粤语、吴语、闽南语、客家话、赣语、湘语、晋语；并支持中原、西南、冀鲁、江淮、兰银、胶辽、东北、北京、港台等，包括河南、陕西、湖北、四川、重庆、云南、贵州、广东、广西、河北、天津、山东、安徽、南京、江苏、杭州、甘肃、宁夏等地区官话口音）、英语、日语、韩语、越南语、泰语、印尼语、马来语、菲律宾语、印地语、阿拉伯语、法语、德语、西班牙语、葡萄牙语、俄语、意大利语、荷兰语、瑞典语、丹麦语、芬兰语、挪威语、希腊语、波兰语、捷克语、匈牙利语、罗马尼亚语、保加利亚语、克罗地亚语、斯洛伐克语
-   fun-asr-flash-2026-06-15：中文（普通话、粤语、吴语、闽南语、客家话、赣语、湘语、晋语；并支持中原、西南、冀鲁、江淮、兰银、胶辽、东北、北京、港台等，包括河南、陕西、湖北、四川、重庆、云南、贵州、广东、广西、河北、天津、山东、安徽、南京、江苏、杭州、甘肃、宁夏等地区官话口音）、英语、日语、韩语、越南语、泰语、印尼语、马来语、菲律宾语、印地语、阿拉伯语、法语、德语、西班牙语、葡萄牙语、俄语、意大利语、荷兰语、瑞典语、丹麦语、芬兰语、挪威语、希腊语、波兰语、捷克语、匈牙利语、罗马尼亚语、保加利亚语、克罗地亚语、斯洛伐克语

<a id="asr_qa02"></a>

<a id="asr_qa01"></a>

<a id="b1a2c3d4e5f5e"></a>

<a id="b1a2c3d4e5f5d"></a>

<a id="accordion-qwen3-asr"></a>

Qwen3-ASR

-   qwen3-asr-flash-realtime、qwen3-asr-flash-filetrans、qwen3-asr-flash：中文（普通话、四川话、闽南语、吴语、粤语）、英语、日语、德语、韩语、俄语、法语、葡萄牙语、阿拉伯语、意大利语、西班牙语、印地语、印尼语、泰语、土耳其语、乌克兰语、越南语、捷克语、丹麦语、菲律宾语、芬兰语、冰岛语、马来语、挪威语、波兰语、瑞典语。

<a id="asr_pf02"></a>

<a id="asr_pf01"></a>

<a id="accordion-paraformer"></a>

Paraformer

-   paraformer-realtime-v2、paraformer-v2：中文（普通话、粤语、吴语、闽南语、东北话、甘肃话、贵州话、河南话、湖北话、湖南话、宁夏话、山西话、陕西话、山东话、四川话、天津话、江西话、云南话、上海话）、英文、日语、韩语、德语、法语、俄语
-   paraformer-realtime-8k-v2、paraformer-8k-v2：中文普通话

<a id="音频输入要求"></a>

<a id="asr_audio_spec02"></a>

<a id="asr_audio_spec01"></a>

## 音频输入要求

音频格式、采样率、声道、文件大小和时长等要求，参见 

<a id="asr_rt_spec02"></a>

<a id="asr_rt_spec01"></a>

[实时语音识别](real-time-speech-recognition-user-guide.md#usage-limits)或 

<a id="asr_nrt_spec02"></a>

<a id="asr_nrt_spec01"></a>

[非实时语音识别](non-realtime-speech-recognition-user-guide.md#usage-limits)的使用限制。
