# 语音识别概述

百炼语音识别支持实时音频和录音文件转写，提供多语言与方言、热词与上下文、文本润色、说话人分离等能力。

## 功能介绍

语音识别将音视频中的语音转换为文本，可用于语音输入、实时字幕、会议记录和通话分析等场景。百炼支持持续输入音频的实时识别，以及提交完整音频文件的非实时识别；不同模型支持的语言、方言和增强能力有所不同。

## 模型选型

按音频输入方式、业务场景和结果返回需求选择模型。以下推荐使用 Qwen-Audio 3.1 系列。

**类型**

**使用场景**

**推荐模型**

**主要区别**

实时

实时字幕、会议记录等持续转写

[qwen-audio-3.1-asr-flash-streaming](https://bailian.console.aliyun.com/cn-beijing/model/market/detail/qwen-audio-3.1-asr-flash-streaming)

持续发送音频，同时接收中间结果和最终结果。

输入法、语音消息等短段语音输入

[qwen-audio-3.1-asr-flash-message](https://bailian.console.aliyun.com/cn-beijing/model/market/detail/qwen-audio-3.1-asr-flash-message)

默认返回句子最终结果，可分别开启中间结果和文本润色。

非实时

5 分钟以内的短音频文件

[qwen-audio-3.1-asr-flash](https://bailian.console.aliyun.com/cn-beijing/model/market/detail/qwen-audio-3.1-asr-flash)

在当前请求中获取识别结果，可选择 SSE 流式输出。

长录音、后台音视频转写

[qwen-audio-3.1-asr-flash-filetrans](https://bailian.console.aliyun.com/cn-beijing/model/market/detail/qwen-audio-3.1-asr-flash-filetrans)

提交异步任务，完成后下载转写结果文件。

## 识别方式

**识别方式**

**音频输入**

**结果返回**

[实时语音识别](raw/model-user-guide/model-experience/speech-and-audio/speech-recognition/real-time-speech-recognition-user-guide.md)

分块持续发送音频，适合在说话过程中展示转写。

发送音频的同时接收识别结果；中间结果、最终结果的返回方式随模型而异。

[非实时语音识别](raw/model-user-guide/model-experience/speech-and-audio/speech-recognition/non-realtime-speech-recognition-user-guide.md)

一次提交完整音频或音视频文件，适合处理已有录音。

同步调用在当前请求中返回结果，支持 SSE 的模型可分次输出；异步调用先返回任务 ID，完成后获取结果文件。

## 识别效果与结果

选定模型后，可根据业务需要改善特定词汇的识别、文本可读性及结构化结果。具体配置方法参见[实时语音识别](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition-user-guide#rt03_advanced_h2)或[非实时语音识别](https://help.aliyun.com/zh/model-studio/non-realtime-speech-recognition-user-guide#nrt03_advanced_h2)。

-   **热词与上下文**： 热词提供人名、品牌名等词汇的目标写法；上下文补充前几轮对话及业务背景。使用方法、支持范围和调优参见[提升识别准确率](raw/model-user-guide/model-experience/speech-and-audio/speech-recognition/improve-asr-accuracy.md)。
    
-   **文本润色**： 整理口语中的语气词、重复和自我纠正。qwen-audio-3.1-asr-flash-message 和 qwen-audio-3.1-asr-flash 支持原生文本润色。
    
-   **保留方言表达**： qwen-audio-3.1-asr-flash-streaming、qwen-audio-3.1-asr-flash-message、qwen-audio-3.1-asr-flash、qwen-audio-3.1-asr-flash-filetrans 支持保留方言特有表达。识别某种方言与保留其文本表达是不同的能力。
    
-   **说话人分离**： 为转写结果标注说话人编号，用于区分会议、访谈中的发言人。qwen-audio-3.1-asr-flash 和 qwen-audio-3.1-asr-flash-filetrans 支持该能力。
    
-   **时间戳**： 将句子或字词与音频位置对应，用于字幕对齐、关键词高亮和音频跳转。
    
-   **敏感词过滤**： 将指定词汇替换为星号或从转写文本中移除。
    

音频准备、连接与并发管理、异步作业及异常处理，参见[语音识别最佳实践](raw/model-user-guide/model-experience/speech-and-audio/speech-recognition/speech-recognition-best-practices.md)。

## 模型与语言

以下按模型系列和版本列出支持的语言与方言。

Qwen-Audio-ASR-Streaming

-   qwen-audio-3.1-asr-flash-streaming、qwen-audio-3.0-asr-flash-streaming：中文（普通话、粤语、吴语、闽南语、客家话、赣语、湘语、晋语；并支持中原、西南、冀鲁、江淮、兰银、胶辽、东北、北京、港台等，包括河南、陕西、湖北、四川、重庆、云南、贵州、广东、广西、河北、天津、山东、安徽、南京、江苏、杭州、甘肃、宁夏等地区官话口音）、英语、日语、韩语、越南语、泰语、印尼语、马来语、菲律宾语、印地语、阿拉伯语、法语、德语、西班牙语、葡萄牙语、俄语、意大利语、荷兰语、瑞典语、丹麦语、芬兰语、挪威语、希腊语、波兰语、捷克语、匈牙利语、罗马尼亚语、保加利亚语、克罗地亚语、斯洛伐克语

Qwen-Audio-ASR-Message

-   qwen-audio-3.1-asr-flash-message：中文（普通话、粤语、吴语、闽南语、客家话、赣语、湘语、晋语；并支持中原、西南、冀鲁、江淮、兰银、胶辽、东北、北京、港台等，包括河南、陕西、湖北、四川、重庆、云南、贵州、广东、广西、河北、天津、山东、安徽、南京、江苏、杭州、甘肃、宁夏等地区官话口音）、英语、日语、韩语、越南语、泰语、印尼语、马来语、菲律宾语、印地语、阿拉伯语、法语、德语、西班牙语、葡萄牙语、俄语、意大利语、荷兰语、瑞典语、丹麦语、芬兰语、挪威语、希腊语、波兰语、捷克语、匈牙利语、罗马尼亚语、保加利亚语、克罗地亚语、斯洛伐克语

Qwen-Audio-ASR

-   qwen-audio-3.1-asr-flash：中文（普通话、粤语、吴语、闽南语、客家话、赣语、湘语、晋语；并支持中原、西南、冀鲁、江淮、兰银、胶辽、东北、北京、港台等，包括河南、陕西、湖北、四川、重庆、云南、贵州、广东、广西、河北、天津、山东、安徽、南京、江苏、杭州、甘肃、宁夏等地区官话口音）、英语、日语、韩语、越南语、泰语、印尼语、马来语、菲律宾语、印地语、阿拉伯语、法语、德语、西班牙语、葡萄牙语、俄语、意大利语、荷兰语、瑞典语、丹麦语、芬兰语、挪威语、希腊语、波兰语、捷克语、匈牙利语、罗马尼亚语、保加利亚语、克罗地亚语、斯洛伐克语、土耳其语、波斯语、马拉地语、马拉雅拉姆语、尼泊尔语、吉尔吉斯语、阿塞拜疆语、格鲁吉亚语、亚美尼亚语、斯洛文尼亚语、阿尔巴尼亚语、爱沙尼亚语、拉脱维亚语、立陶宛语、加泰罗尼亚语、巴斯克语、加利西亚语、奥里亚语、迪维希语、阿萨姆语、库尔德语、提格雷语、西弗里西亚语、巴什基尔语、白俄罗斯语、鞑靼语、国际语、东马里语、道本语
-   qwen-audio-3.0-asr-flash：中文（普通话、粤语、吴语、闽南语、客家话、赣语、湘语、晋语；并支持中原、西南、冀鲁、江淮、兰银、胶辽、东北、北京、港台等，包括河南、陕西、湖北、四川、重庆、云南、贵州、广东、广西、河北、天津、山东、安徽、南京、江苏、杭州、甘肃、宁夏等地区官话口音）、英语、日语、韩语、越南语、泰语、印尼语、马来语、菲律宾语、印地语、阿拉伯语、法语、德语、西班牙语、葡萄牙语、俄语、意大利语、荷兰语、瑞典语、丹麦语、芬兰语、挪威语、希腊语、波兰语、捷克语、匈牙利语、罗马尼亚语、保加利亚语、克罗地亚语、斯洛伐克语

Qwen-Audio-ASR-Filetrans

-   qwen-audio-3.1-asr-flash-filetrans、qwen-audio-3.0-asr-flash-filetrans：中文（普通话、粤语、吴语、闽南语、客家话、赣语、湘语、晋语；并支持中原、西南、冀鲁、江淮、兰银、胶辽、东北、北京、港台等，包括河南、陕西、湖北、四川、重庆、云南、贵州、广东、广西、河北、天津、山东、安徽、南京、江苏、杭州、甘肃、宁夏等地区官话口音）、英语、日语、韩语、越南语、泰语、印尼语、马来语、菲律宾语、印地语、阿拉伯语、法语、德语、西班牙语、葡萄牙语、俄语、意大利语、荷兰语、瑞典语、丹麦语、芬兰语、挪威语、希腊语、波兰语、捷克语、匈牙利语、罗马尼亚语、保加利亚语、克罗地亚语、斯洛伐克语

Fun-ASR

-   fun-asr-realtime：中文（普通话、粤语、吴语、闽南语、客家话、赣语、湘语、晋语；并支持中原、西南、冀鲁、江淮、兰银、胶辽、东北、北京、港台等，包括河南、陕西、湖北、四川、重庆、云南、贵州、广东、广西、河北、天津、山东、安徽、南京、江苏、杭州、甘肃、宁夏等地区官话口音）、英语、日语、韩语、越南语、泰语、印尼语、马来语、菲律宾语、印地语、阿拉伯语、法语、德语、西班牙语、葡萄牙语、俄语、意大利语、荷兰语、瑞典语、丹麦语、芬兰语、挪威语、希腊语、波兰语、捷克语、匈牙利语、罗马尼亚语、保加利亚语、克罗地亚语、斯洛伐克语
-   fun-asr-realtime-2026-02-28：中文（普通话、粤语、吴语、闽南语、客家话、赣语、湘语、晋语；并支持中原、西南、冀鲁、江淮、兰银、胶辽、东北、北京、港台等，包括河南、陕西、湖北、四川、重庆、云南、贵州、广东、广西、河北、天津、山东、安徽、南京、江苏、杭州、甘肃、宁夏等地区官话口音）、英语、日语
-   fun-asr-flash-8k-realtime、fun-asr-flash-8k-realtime-2026-01-28：中文
-   fun-asr：中文（普通话、粤语、吴语、闽南语、客家话、赣语、湘语、晋语；并支持中原、西南、冀鲁、江淮、兰银、胶辽、东北、北京、港台等，包括河南、陕西、湖北、四川、重庆、云南、贵州、广东、广西、河北、天津、山东、安徽、南京、江苏、杭州、甘肃、宁夏等地区官话口音）、英语、日语、韩语、越南语、泰语、印尼语、马来语、菲律宾语、印地语、阿拉伯语、法语、德语、西班牙语、葡萄牙语、俄语、意大利语、荷兰语、瑞典语、丹麦语、芬兰语、挪威语、希腊语、波兰语、捷克语、匈牙利语、罗马尼亚语、保加利亚语、克罗地亚语、斯洛伐克语
-   fun-asr-flash-2026-06-15：中文（普通话、粤语、吴语、闽南语、客家话、赣语、湘语、晋语；并支持中原、西南、冀鲁、江淮、兰银、胶辽、东北、北京、港台等，包括河南、陕西、湖北、四川、重庆、云南、贵州、广东、广西、河北、天津、山东、安徽、南京、江苏、杭州、甘肃、宁夏等地区官话口音）、英语、日语、韩语、越南语、泰语、印尼语、马来语、菲律宾语、印地语、阿拉伯语、法语、德语、西班牙语、葡萄牙语、俄语、意大利语、荷兰语、瑞典语、丹麦语、芬兰语、挪威语、希腊语、波兰语、捷克语、匈牙利语、罗马尼亚语、保加利亚语、克罗地亚语、斯洛伐克语

Qwen3-ASR

-   qwen3-asr-flash-realtime、qwen3-asr-flash-filetrans、qwen3-asr-flash：中文（普通话、四川话、闽南语、吴语、粤语）、英语、日语、德语、韩语、俄语、法语、葡萄牙语、阿拉伯语、意大利语、西班牙语、印地语、印尼语、泰语、土耳其语、乌克兰语、越南语、捷克语、丹麦语、菲律宾语、芬兰语、冰岛语、马来语、挪威语、波兰语、瑞典语。

Paraformer

-   paraformer-realtime-v2、paraformer-v2：中文（普通话、粤语、吴语、闽南语、东北话、甘肃话、贵州话、河南话、湖北话、湖南话、宁夏话、山西话、陕西话、山东话、四川话、天津话、江西话、云南话、上海话）、英文、日语、韩语、德语、法语、俄语
-   paraformer-realtime-8k-v2、paraformer-8k-v2：中文普通话

## 音频输入要求

音频格式、采样率、声道、文件大小和时长等要求，参见 [实时语音识别](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition-user-guide#usage-limits)或 [非实时语音识别](https://help.aliyun.com/zh/model-studio/non-realtime-speech-recognition-user-guide#usage-limits)的使用限制。
