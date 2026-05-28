# 应用配置

完成应用创建后，您可以在应用配置页面，自由组合需要的对话能力。应用配置分为语音交互、理解与生成、技能、Agent四个主要部分。

## **语言选择**

支持欧美、亚洲热门国家的单一语言对话能力，语种、功能持续扩展中。详情请参考[多语言对话](https://help.aliyun.com/zh/model-studio/multi-language-dialogue)。

## **语音交互**

配置语音交互相关的功能，例如语音模型、打断方式等。

### **语音AI**

可选择是否调用语音识别、语音合成能力，以及调用的具体模型。

#### **语音识别**

支持使用阿里云百炼的语音识别模型，包括Fun-ASR实时语音识别、千问3-ASR-Flash-Realtime、Paraformer实时语音识别以及多模态交互轻量版语音识别。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1813879771/p1075139.png)

除千问3-ASR-Flash-Realtime外，以上语音识别模型均支持定制热词功能。

-   热词数量：最多支持创建10个热词库，每个热词库最多500个词。
    
-   配置方式：您可以手动添加词汇，也可以上传文件进行批量添加，文件示例详见页面说明。
    

![DBBAEF53-B83E-4505-9BA8-A0674EF3A283](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7463950671/p1003638.png)

配置应用时，可以在界面中下拉选择一个热词组并添加，发布后相应热词即可生效。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1813879771/p1075138.png)

如需针对不同用户设置不同ASR热词，可通过API接口传入。通过接口传入热词后，控制台热词不再生效。接口文档：[管理热词](https://help.aliyun.com/zh/model-studio/management-hot-words)

您还可以使用即时纠错功能，通过接口上传词表，对语音识别结果进行实时干预。接口文档：[ASR结果即时纠错](https://help.aliyun.com/zh/model-studio/multimodal-sdk-java/#020a84a017w5l)

#### **语音合成**

支持使用阿里云百炼的语音合成模型，包括CosyVoice-实时语音合成、千问3-实时语音合成以及其他语音合成。除系统音色外，还支持声音复刻能力[CosyVoice声音复刻/设计API](https://help.aliyun.com/zh/model-studio/cosyvoice-clone-design-api)（CosyVoice-v2大模型、CosyVoice-v3-Flash大模型、CosyVoice-v3.5-Plus大模型、CosyVoice-v3.5-Flash大模型）、[Qwen-TTS声音复刻API参考](https://help.aliyun.com/zh/model-studio/qwen-tts-voice-cloning)（千问3-TTS-声音复刻）以及[声音设计（Qwen）](https://help.aliyun.com/zh/model-studio/qwen-tts-voice-design)能力（通义千问3-TTS-声音设计）。

-   CosyVoice-实时语音合成：CosyVoice-v3-Flash大模型、CosyVoice-v3-Plus大模型、CosyVoice-v3.5-Plus大模型、CosyVoice-v3.5-Flash大模型、CosyVoice-v2大模型。
    
-   通义千问3-实时语音合成：通义千问3-TTS-Flash-Realtime、通义千问3-TTS-instruct-Flash-Realtime、通义千问3-TTS-声音设计、通义千问3-TTS-声音复刻。
    
-   其他语音合成模型：Sambert语音合成模型、多模态交互轻量版语音合成。
    

三方语音模型：支持接入三方语音模型，具体方法参见[调用三方语音模型](https://help.aliyun.com/zh/model-studio/third-party-voice-integration)。

![截屏2026-03-23 15](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4557144771/p1061707.png)

语音应用支持开启「语音合成播报过滤」，通过配置符号对的形式，在TTS播报中过滤，避免系统读出参数。

-   例如，模型输出的文本为：“早上好呀！\[smile\]今天天气不错，你想去哪玩？\[wink\]”
    
    配置过滤符号对\[\]后，TTS播报文本为：“早上好呀！今天天气不错，你想去哪玩？”
    

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1885880771/p1054342.png)

### **对话打断**

支持三种打断方式：任意语音打断（全双工）、点击打断（半双工）、长按对话（半双工，仅移动端支持）。

您可以在控制台选择并体验对话效果。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2655897471/p958288.png)

### **语义判停与拒识**

支持开启语义判停与拒识能力，避免误打断、误唤醒，语音交互体验更佳。

全双工场景下功能效果更显著，开启后可能导致对话延迟增加。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7463950671/p1001891.png)

### **端侧算法**

提供以下端侧算法能力：

-   **语音唤醒**：支持默认唤醒词“小云”，移动端 Android 和 iOS 可直接使用。如需其它芯片平台请联系商务。
    
-   **端侧VAD**：语音活性检测，用于检测是否存在语音信号。移动端可直接使用，其他芯片平台可使用云端 VAD 方案，或联系商务进行定制。
    
-   **AEC**：回声消除，减少自身播报对语音交互的干扰。移动端 Android 和 iOS 可直接使用已集成的语音打断，其它芯片平台如需定制请联系商务。
    
-   **定向拾音**：增强特定方向拾音，抑制甚至屏蔽其他方向声音。依赖麦克风阵列硬件布局，如需定制请联系商务。
    

## **理解与生成**

配置对话理解与生成相关功能，例如文本生成模型、Prompt、知识库等。

### **意图识别**

关闭将不再触发调用工具、Agent、联网搜索、对话承接语等基于语义理解的交互功能，适用于低成本、轻量级语音交互场景。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7463950671/p1001915.png)

### **文本模型**

可选择对话中的文本生成大模型。

-   推荐模型：支持选择多模态交互专有模型-高速版、多模态交互专有模型以及多模态交互专有模型-风格化版。
    
    -   多模态交互专有模型-高速版：对话速度更快，适合通用场景、闲聊陪伴场景，如儿童玩具、陪伴机器人等。
        
    -   多模态交互专有模型：指令遵循能力更强，适合工作学习场景，如穿戴设备、学习机等。
        
    -   多模态专有模型-风格化版：风格化能力更强，适合角色扮演等场景，如儿童玩具。
        
-   百炼模型：您也可选择阿里云百炼提供的文本生成模型，例如Qwen3.6系列、 Qwen3.5 系列，可在更多模型中自由切换。在多模态交互应用中，您还可以选择“我的模型”。
    

可以在右侧体验区测试对话效果，选择最合适产品应用场景的模型。

![截屏2025-10-29 10](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9682332671/p1020489.png)

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0615827771/p1071076.png)

若关闭文本模型开关，仅输出意图识别结果，不会调用大模型和各类技能/agent生成回复。

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9780406671/p1035502.png)

### **欢迎语**

支持设置对话交互的欢迎语，进入对话后模型主动发起话题。如未设置，则需要用户主动提问，模型不会主动发起话题。

您可以配置一句欢迎语用于效果测试。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2655897471/p958290.png)

语音交互应用尚不支持通过控制台设置欢迎语。

### **提示词**

支持自定义Prompt，用于设定对话风格和人设。

如未填写，则使用通用Prompt，适用于常见的口语对话场景。

您可以在右侧体验区测试提示词效果。

支持使用阿里云百炼的Prompt[模板概述](https://help.aliyun.com/zh/model-studio/prompt-template)和Prompt[自动优化](https://help.aliyun.com/zh/model-studio/optimize-prompt)功能。

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9207470571/p975737.png)

支持插入自定义变量，可以设置变量并传参。传入变量值将替换提示词中对应的变量位置。

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2204344771/p975740.png)

### 对话变量

支持在对话输入中添加变量，为模型提供用户语音之外的更多信息，如动作行为、人脸识别结果、时间、地点、天气、周围环境等。

每轮对话中，没有传入参数的变量，将不会输入给模型进行处理。

例如，设置变量名currentWeather（当前天气）、 currentPerson（当前与AI对话的人物的名字），并传入currentWeather=36、 currentPerson=Lily，则本轮对话除传入用户问题，还会传入对应参数。

![image (5)](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8207470571/p977037.png)

### 携带上下文轮数

该参数用于控制模型参考历史对话的轮数，设为1时表示模型在回复时不会参考历史对话信息。

可设置范围为：1~30。

![截屏2025-10-17 13](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0815860671/p1016808.png)

### **对话承接语**

在联网搜索、拍照问答等对话延迟可能较长的场景，大模型结合场景自动生成承接语，减少等待时间，对话体感更流畅。例如：“马上帮你查最新的热点新闻！”，“好的，马上帮你拍照分析！”。

![截屏2025-09-22 13](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7463950671/p1009427.png)

### **知识库**

支持配置阿里云百炼创建的知识库，并进行检索设置。

开启知识库后，通过在提示词中手动输入「/」来添加变量。

具体操作可查看[创建和使用知识库](https://help.aliyun.com/zh/model-studio/rag-knowledge-base)说明文档。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2655897471/p958293.png)

![截屏2026-03-24 11](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4557144771/p1061888.png)![截屏2026-03-24 11](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4557144771/p1061890.png)

### **长期记忆**

开启长期记忆开关，大模型可以基于对话历史，分析挖掘个人信息和偏好、近期生活状况和行为计划，形成长期记忆库，并在后续对话中主动召回，为用户提供更个性化的智能服务。

如需根据业务场景自定义记忆策略、管理记忆结果，请查看接口文档：[长期记忆开放接口](https://help.aliyun.com/zh/model-studio/long-term-memory-api)。

**说明**

不同应用之间记忆内容隔离；同一个应用中，按照userid维度生成记忆库，不同userid之间记忆隔离。

![image (31)](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9780406671/p1035508.png)

### **联网搜索**

由于训练数据的时效性，大模型无法准确回答如股票价格、今日资讯等时效性问题。

您可以通过开启联网搜索开关，启用联网检索功能，使大模型可以基于实时检索数据进行回复。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2655897471/p958294.png)

在语音交互应用中，您还可以选择开启效率模式或效果模式。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2655897471/p959527.png)

效率模式返回结果的速度更快，效果模式返回结果的精度更高。

### **对话日志储存**

如果您需要保存全量对话数据，可使用阿里云事件总线 Event Bridge 服务。

详细使用方法可查看：[对话日志接入](https://help.aliyun.com/zh/model-studio/multimodal-chatlog)。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7463950671/p1003681.png)

## **技能**

### **指令**

指令是指由多模态交互下发，设备终端执行的任务，如打开台灯、调高音量等。具体指令可查看：[指令列表](https://help.aliyun.com/zh/model-studio/instruction-list)。

### **插件**

支持接入您在阿里云百炼创建的插件，以增强对话能力。

-   点击添加按钮，选择您需要的插件即可。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2655897471/p958295.png)
    
-   支持按需勾选多模态交互套件预置插件，您也可以在插件广场中选择，或接入自定义插件。
    
    -   天气查询：实时和历史天气信息查询。
        
    -   万年历：日期、节气、节假日查询。
        
    -   股价查询：获取股票市场实时行情。
        
    -   油价查询：了解燃油最新价格信息。
        
    -   金价查询：掌握黄金市场价格变动。
        
    -   银价查询：掌握白银实时价格变动。
        
    -   汇率查询：提供货币兑换比率参考。
        
    -   新闻资讯：热点新闻一网打尽，新鲜事儿有问必答。
        
    -   路线规划：支持获取当前定位、查询地点信息、进行出行路线规划。例如：“从这里去故宫怎么走？”“从西溪湿地开车去阿里总部大概需要多久？”
        
    -   本地生活：支持查询并推荐POI（兴趣点），推荐基于定位的周边吃喝玩乐。例如：“湖滨银泰有什么好吃的韩餐推荐？”“最近的海底捞在哪里？”“我这里到奥克斯广场走路要多久”![截屏2025-11-11 16](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1300582671/p1025749.png)
        

### **MCP服务**

#### **MCP广场**

-   支持接入百炼官方MCP服务。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1300582671/p1025696.png)
    
-   当前仅支持接入部分百炼官方MCP服务，列表如下：
    
    **MCP服务**
    
    **功能介绍**
    
    **详情**
    
    全国快递物流查询
    
    为实现电子商务平台的溯源与记录，全国快递查询服务可以一站式接入，提供了即时查询、路由跟踪、平台监控管理。增强了电子商务行业与各行业的物流数据赋能。
    
    [https://bailian.console.aliyun.com/?tab=mcp#/mcp-market/detail/market-cmapi021863](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market/detail/market-cmapi021863)
    
    图书信息查询
    
    通过10位或者13位ISBN查询图书信息，包含书名、作者、出版社、价格、出版日期、印次、装帧方式、语种、摘要等几十项图书相关信息。
    
    [https://bailian.console.aliyun.com/?tab=mcp#/mcp-market/detail/market-cmapi00053669](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market/detail/market-cmapi00053669)
    
    黄历运势查询
    
    可查询传统日历、节假日、运势、宜忌等信息，广泛用于日程安排，出行指南，风水评估等。
    
    [https://bailian.console.aliyun.com/?tab=mcp#/mcp-market/detail/market-cmapi00066017](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market/detail/market-cmapi00066017)
    
    新电途-ChargeStation
    
    朗新集团新电途官方提供的充电站查询服务，用户可通过此服务按页查询指定文本地址或经纬度坐标周边范围内的充电站详细信息。服务支持灵活的距离范围设置，让用户能够精确获取所需区域内的充电设施数据。
    
    [https://bailian.console.aliyun.com/?tab=mcp#/mcp-market/detail/ChargeStation](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market/detail/ChargeStation)
    
    火车票查询
    
    提供国内火车的车次查询，余票查询和站站查询三个子服务。
    
    [https://bailian.console.aliyun.com/?tab=mcp#/mcp-market/detail/market-cmapi011240](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market/detail/market-cmapi011240)
    
    星座运势查询
    
    本数据包含十二星座的每日运势，明日运势，每周运势，当年运势以及星座配对。具体包括缘份星座、吉利颜色、幸运数字、爱情提醒、运势简评、爱情运势、工作运势、财富运势、健康运势等。可用于微信公众号、小程序、网站等引流及增加与用户的联系等场景。
    
    [https://bailian.console.aliyun.com/?tab=mcp#/mcp-market/detail/market-cmapi011529](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market/detail/market-cmapi011529)
    
    八字排盘
    
    八字排盘是中国传统命理学工具，根据出生年、月、日、时干支共八字，分析五行生克关系，推算命运、性格与运势，用于趋吉避凶，解读人生轨迹。切勿迷信，仅供参考。
    
    [https://bailian.console.aliyun.com/?tab=mcp#/mcp-market/detail/market-cmapi011212](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market/detail/market-cmapi011212)
    
    12306车票查询
    
    开源社区开发者封装,提供 12306购票信息查询等服务
    
    [https://bailian.console.aliyun.com/?tab=mcp#/mcp-market/detail/china-railway](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market/detail/china-railway)
    
    今天吃什么
    
    开源社区开发者封装，让 AI 助手变身私人大厨，为你的一日三餐出谋划策！
    
    [https://bailian.console.aliyun.com/?tab=mcp#/mcp-market/detail/how-to-cook](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market/detail/how-to-cook)
    
    谣言鉴别
    
    快速鉴别新闻事件信息真伪
    
    [https://bailian.console.aliyun.com/?tab=mcp#/mcp-market/detail/rumor-identify](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market/detail/rumor-identify)
    

#### **自定义MCP**

支持接入基于百炼平台的自定义MCP。

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4557144771/p1061727.png)

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4557144771/p1061726.png)

### **Agent**

#### **接入预置Agent**

多模态交互应用提供一系列适用于不同场景的Agent，API参考[调用官方Agent](https://help.aliyun.com/zh/model-studio/official-agent)。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7463950671/p1003700.png)

语音交互应用目前支持语音翻译Agent、极速语音通话Agent、地图出行Agent、新闻电台Agent、儿童故事Agent以及录音纪要Agent，敬请期待。

-   实时视频通话：实时视觉理解，适用于带有摄像头的设备。点开右侧设置，可配置功能名称、视觉理解模型、欢迎语、退出语、启动指令、退出指令以及提示词。
    
    -   视觉理解模型：包含「推荐模型」及「更多模型」，其中「推荐模型」支持视觉理解高级版以及均衡版，「更多模型」支持Qwen3.6系列、Qwen3.5系列等多模态模型。
        
    -   ![截屏2026-04-27 14](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0615827771/p1071073.png)
        
-   拍照问答：当识别到用户有画面理解的需求时，自动调用摄像头拍照并回复。适用于带有摄像头的设备。点开右侧设置，可配置启动指令、提示词，还能选择视觉理解模型。
    
    -   视觉理解模型：包含「推荐模型」及「更多模型」，其中「推荐模型」支持视觉理解高级版以及均衡版，「更多模型」支持Qwen3.6系列、Qwen3.5系列等多模态模型。
        
        -   ![截屏2026-04-27 15](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0615827771/p1071120.png)
            
    -   支持IPC模式：将图片直接送入Agent进行识别，适用于带摄像头产品的图片理解、拍学机或学习机内的拍照识图等功能。详情可查看：[通过HTTP协议接入拍照问答Agent](https://help.aliyun.com/zh/model-studio/vqa-agent-through-the-http-protocol)。
        
        -   **说明**
            
            直通链路：是指不通过语音识别（ASR）、意图识别、语音合成（TTS）等节点，直接将请求送入Agent，并将Agent的回答直接返回的链路。
            
-   新闻电台：每日更新热门新闻资讯，两位AI主播互动解说，用户可以随时打断并加入对话。点开右侧设置，可配置功能名称、启动指令、退出指令、续播指令以及角色音色。
    
    -   ![截屏2025-06-03 18](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8207470571/p963587.png)
        
-   语音翻译：多语种实时语音识别，并输出语音翻译、文本翻译结果。点开右侧设置，可配置功能名称、启动指令、退出指令，选择输出结果。
    
    -   ![截屏2025-06-20 15](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9207470571/p975960.png)
        
-   极速视频通话：基于Qwen-Omni模型的视频对话，支持响应速度更快的闲聊。点开右侧设置，可配置功能名称、启动指令以及退出指令。
    
    -   ![4ED65AB6-0EC1-48c7-B18A-66AAD087C09B](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5359526571/p997666.png)
        
-   拍照翻译：多模态应用专属，支持多语言、自动拍照的翻译能力，能够精准翻译眼前的文字。点开右侧设置，可配置触发指令、提示词以及对话变量，支持一键导入主对话链路中的提示词和变量配置。
    
    -   ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5359526571/p997695.png)
        
-   儿童故事：陪伴式讲故事功能，拥有自有故事库，支持讲故事过程中的对话交互、故事创作和续写改写。点开右侧设置，可配置功能名称、启动指令、退出指令、语音合成模型以及对应音色。
    
    -   ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5359526571/p997699.png)
        
-   多模态备忘录：用户可以通过语音输入的方式，让模型创建备忘、记录关键信息，支持自动拍照并结合视觉信息提取备忘。备忘信息支持通过语音指令查询、修改、删除。
    
    -   典型场景：设定日程提醒如“明天下午两点提醒我开会”，设定闹钟如“五分钟后提醒我”，记忆视觉信息如“记一下我的停车位号码”、“记一下这本书的名字”。
        
    -   ![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9715860671/p1016801.png)
        
-   地图出行：提供复杂路线规划、周边地点查询和推荐能力。例如，“怎么去首都机场最快？”、“推荐附近评分最高的咖啡厅”。（本Agent仅支持上述场景的多轮对话，不支持实时语音导航。）
    
    -   ![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9715860671/p1016802.png)
        
-   录音纪要：提供实时录音字幕和总结，提炼核心信息、生成会议纪要。例如，“开始实时转写”、“开始录制并总结”。支持对录音总结的内容进行多轮对话问答，例如询问上次会议的讨论内容、昨天课程的课程要点等。还支持对历史内容进行问答，可提问的内容范围包括录音原文，以及大模型总结的纪要文本。
    
    **说明**
    
    对历史内容进行问答的功能对上线后创建的录音任务可用，对之前的历史任务不支持问答。
    
    -   ![截屏2025-11-26 16](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3052464671/p1029738.png)
        
    -   接入方式：
        
        -   在[听悟-智能纪要Agent](https://bailian.console.aliyun.com/?spm=a2ty02.31808181.d_app-market.1.27b274a1lPyXvF&tab=app#/app/app-market/tingwu/tingwu-meeting-summary)中创建应用并发布，按需配置总结能力
            
        -   在多模态应用中勾选录音纪要Agent，并选择配置好的通义听悟应用
            
        -   支持设置语音指令，退出、暂停需要配置唤醒词，避免在会议中误打断录音
            
        -   开发接入，请查看文档：[接入听悟智能纪要Agent](https://help.aliyun.com/zh/model-studio/fast-integrate-tingwu-meeting-agent/)
            
    -   ![image (32)](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9780406671/p1035517.png)
        
-   音乐电台：推荐和随机播放舒缓的轻音乐（无人声）。
    
    -   ![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3150877671/p1041259.png)
        
-   图像生成：适用于壁纸生成、涂鸦作画、照片美化、图像风格化等各类图像生成场景。目前仅支持直通链路。接入方式请参考：[通过HTTP协议接入图像生成Agent](https://help.aliyun.com/zh/model-studio/image-agent)。
    
    -   ![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4557144771/p1061710.png)
        
    -   ![截屏2026-03-23 15](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4557144771/p1061712.png)
        
-   主动导览：摄像头常开，会持续分析眼前景象，遇到需要讲解的展品，会主动进行介绍。也可以主动要求AI对眼前的展品做介绍或进行问答。
    
    -   ![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6104800771/p1051074.png)
        
-   主动陪伴：摄像头常开，会持续分析眼前景象（也会产生费用），支持功能如下：
    
    -   手势互动：对着摄像头比动作，AI可快速进行动作、表情、语音回复的反馈。如果同时比动作和说话，优先响应说话内容。
        
    -   打招呼：结合视觉信息，与用户互动（类似进入语），如对用户的着装进行点评、针对表情回复相应的夸赞或安抚、对用户手持物品表达兴趣、随机唠嗑等。
        
    -   主动发起话题：结合用户情境（比如绘画/玩魔方、家中打扫卫生等）主动参与活动，发起话题。
        
    -   ![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1885880771/p1054350.png)
        

#### 接入**百炼平台Agent**

-   可以接入您在阿里云百炼平台创建的Agent，以增强对话能力。
    
    -   ![E68FD306-503A-4fb4-A19C-6BCBD4D89E59](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7463950671/p1003707.png)
        
-   也可以前往百炼应用广场的[AI硬件方案专区](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/app-market/app-template-recommendation/share/AIHardwareSolutions)快速复制与您业务场景需求相似的模板，如穿戴设备的身体指标分析、教育场景的口语陪练等。详情请参考：[百炼应用推荐模板](https://help.aliyun.com/zh/model-studio/agent-template)。
    
    -   ![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1885880771/p1054351.png)
        

#### 接入**三方Agent**

-   支持客户开发的三方Agent接入，需基于Google A2A协议进行集成，详情请参考[三方Agent接入](https://help.aliyun.com/zh/model-studio/multimodal-integration-a2a/)。
    
    -   ![image (1)](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9872243571/p986227.png)
        
    -   ![image (2)](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9872243571/p986229.png)
        
-   Agent内部可以配置和语音助手不同的音色，但需要保持使用同一个模型。例如，语音助手选择通用的温柔女声，接入的童话故事Agent选择一个童声。当启动童话故事Agent时，系统自动切换为童声。
    
    -   ![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3150877671/p1041270.png)
