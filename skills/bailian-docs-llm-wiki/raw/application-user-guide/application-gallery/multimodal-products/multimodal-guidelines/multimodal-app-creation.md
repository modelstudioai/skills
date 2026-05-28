# 应用创建

您可以在控制台创建多个应用，每个应用内自由组合模型和功能，以满足不同场景的开发需求。

## **应用创建**

1.  在[阿里云百炼官网](https://bailian.console.aliyun.com/?spm=a2ty02.31808181.d_app-market.1.38a374a1XgQHkZ&tab=app#/app-market/newTemplate)中，找到「应用开发」-「应用实践」，在应用广场中选择多模态交互开发套件。
    
    ![截屏2026-01-08 15](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9961748671/p1042976.png)
    
    ![截屏2026-01-08 15](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9961748671/p1042972.png)
    
2.  点击右上角「免费开通」，在开通页面中勾选服务协议后点击「立即购买」即可开通成功。
    
    ![截屏2026-01-08 16](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9961748671/p1042996.png)![截屏2026-01-08 16](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9961748671/p1043005.png)
    
3.  开通成功后，点击「管理控制台」回到阿里云百炼官网。![截屏2026-01-08 16](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9961748671/p1043011.png)
    
    **说明**
    
    回到阿里云百炼官网后需要点击「应用开发」才会出现应用列表。
    
4.  点击「应用开发」找到多模态交互开发套件应用，点击前往创建应用。您可以基于业务需求，选择创建不同类型的应用。
    
    ![截屏2026-01-08 16](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9961748671/p1043017.png)
    
    ![截屏2026-01-08 16](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9961748671/p1043018.png)
    

-   多模态交互应用：实时“视频+语音”对话，适用于带摄像头和麦克风、需要实时视频对话能力的软硬件。例如AI眼镜、AI视频对话APP等。
    
    -   全能版：广泛适用于各类智能硬件，提供语音及实时视频对话功能，语音对话和视频对话随时切换，并支持插件、Agent等能力。
        
    -   视觉版：针对摄像头常开的实时视频互动类产品，提供视觉版应用（纯视频通话，不提供语音对话功能），默认进入视频通话模式，并且可以正常使用指令、插件、Agent等对话能力。（目前不支持知识库）。
        
        -   创建应用时，选择「多模态应用-视觉版」即可，在配置页面可以选择视觉理解模型。
            
        -   「推荐模型」支持视觉理解均衡版、高级版；「更多模型」支持Qwen3.6-plus、Qwen3.5-plus、Qwen3.5-flash等多模态模型。
            
        -   ![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9639482671/p1025714.png)![截屏2026-04-27 14](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7115827771/p1071089.png)
            
        -   ![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7115827771/p1071090.png)
            
-   语音交互应用：实时纯语音对话，适用于带麦克风的软硬件。例如AI耳机、儿童玩具等。支持选择全能版或轻量版。（本应用不支持实时视频对话）
    
    -   全能版：支持意图识别、工具调用、联网搜索、多场景Agent，广泛适用于各类交互场景。
        
    -   轻量版：更快速、更低价的语音闲聊，不支持意图识别、工具调用和Agent等能力。
        
    -   ![截屏2025-09-19 15](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0259158571/p1008976.png)
        

## **应用管理**

您可以在[**我的应用**](https://bailian.console.aliyun.com/?tab=app#/app/app-market/multi-modal-app)页面，查看所有已经创建的应用。

![截屏2026-03-09 13](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1468303771/p1057774.png)

点击API接入、下载SDK，可以查看对应的开发文档。

支持对应用进行复制、删除操作，删除后无法恢复。

**重要**

删除应用后，对应的线上服务将无法正常使用，请谨慎操作。

## **数据看板**

您可以通过数据看板查看单个应用的对话次数、平均对话延迟、license激活和消耗情况，支持按照时间范围维度查看。

**说明**

单轮对话的延迟统计口径为：从语音识别结束到语音合成首字输出。未接入语音模型时，统计口径为从文本输入到文本首字输出。

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1468303771/p1057749.png)

您也可以在应用列表中，点击【查看数据】，跳转到数据看板。

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1468303771/p1057750.png)
