# 妙搜

AI妙搜是一款基于multi-agent架构的多模态搜索产品，能够提供多元、高效、丰富且可干预的搜索体验。

## **产品优势**

-   多模态搜索产品，具有灵活、开放和可插拔的特点，能够对接客户的多源异构数据库（包括文档、富文本、图片、视频、URL等），通过对query理解与转化、多路召回、VL caption索引阶段的优化等链路上的细节雕琢，以及适配场景的后处理功能，为不同行业的客户提供信息获取和加工的提效工具。
    
-   该产品支持基于多数据源的向量化检索，多类型搜回逻辑，能够对接本地知识库、本地搜索引擎、本地文件库和外部搜索引擎，最大化丰富搜索来源，确保数据不出本地，即可实现搜索增强。
    

**重要**

-   妙搜的收费方式是基于实际调用模型所消耗的输入和输出总Token数，以后付费的方式进行计费。具体请参见[妙搜-计费文档](https://help.aliyun.com/zh/model-studio/miaosou-miaodu-api-billing#fa58dc56e6rc6)。
    
-   您可点击[链接](https://common-buy.aliyun.com/?commodityCode=sfm_quanmiaoAPI_public_cn)开通全妙智能检索生成应用后付费API。
    
-   您可通过直接调用妙搜API（[妙搜-数据源](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-dir-wonderful-search-data-source/)、[妙搜-智能搜索](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-dir-wonderful-search-smart-search/)）或者通过[妙搜产品控制台](https://aimiaobi.console.aliyun.com/?product_code=g_broadscope_search#/home)来使用妙搜的功能。
    

## **产品入口**

1.  前往阿里云百炼[应用广场](https://bailian.console.aliyun.com/#/app-market/solution)页面，在**全部应用**页签下找到全妙应用，点击其卡片区域进入全妙产详页。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6038620771/p1052587.png)
    
2.  点击妙搜即可进入[妙搜](https://aimiaobi.console.aliyun.com/?product_code=g_broadscope_search&from=bailian#/home)产品页面。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6038620771/p1052588.png)
    

## **搜索类型**

### **问答式搜索**

-   让大模型基于相应query，自主决策并筛选出高度相关的资料，对其进行总结，从而提供准确、直接的答案及参考来源。
    
-   支持基于当前query再进行深度搜索。
    

![1](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7389678571/p1011450.webp)

#### **配置项说明**

支持上传图片，根据搜索类型、搜索范围、模型选择、回答模态进行配置。

-   **搜索类型：**
    
    -   **通用（默认）：**直接搜索并总结，适合简单明确的问题。
        
    -   **深度：**改写和拓展问题，搜索较多资料，适合复杂问题。
        
    -   **研究：**像人类专家一样拆解步骤，更多资料、全面总结。适合深入研究。
        
    -   **自动：**根据上下文和问题的特点自由切换。
        
-   **搜索范围：**
    
    -   **搜索源设置：**支持互联网搜索和方寸搜索，可配置自定义数据源（可多选）。
        
    -   **回答的形式：**包括总结生成答案、用原文语句回答和按时间线总结。
        
    -   **设置资料的时间范围：**支持搜索最近7天、最近1个月、最近2个月、最近6个月、最近1年和自定义。
        
-   **模型选择：**支持全妙-max（默认）和全妙-plus以及对应的思考模型。
    
-   **回答模态**：支持文档、图片、视频、音频（可多选）。
    

### **纯搜索**

为庞大媒资库提供全面搜索功能。检索完成后，可对指定的资料进行聚类、生成原文回答、总结时间线、抽取新闻要素等多种方式的整理与加工。

![9](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7389678571/p1011596.webp)

#### **配置项说明**

支持上传图片和文档，根据搜索范围、模型选择、回答模态进行配置。

-   **搜索范围：**
    
    -   **搜索源设置：**默认支持互联网搜索和方寸搜索，可配置自定义数据源（可多选）。
        
    -   **设置资料的时间范围：**支持搜索最近7天、最近1个月、最近2个月、最近6个月、最近1年和自定义。
        
-   **模型选择：**支持全妙-max（默认）和全妙-plus。
    
-   **回答模态**：支持文档、图片、视频、音频（可多选）。
    

## **搜索数据源**

### **新建数据源**

妙搜支持**手动创建数据源**、**授权OSS对接数据源**、**视频理解Agent引入数据源**、**通过API引入数据源**四种方式添加数据源。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8256823771/p1057660.png)

#### **类型一：手动创建数据源**

分组上传文件，体验基于数据源的搜索效果。支持文本、图片、视频三种数据源的上传。

1.  点击**手动创建数据源**，设置数据源的名称。
    
2.  在已创建的数据源下，点击对应数据源进入文件上传页面。
    

**说明**

每个UID可上传文档总数不得超过100万条，且每个文档根据格式不同，也有大小的限制。如因业务情况，需要上传更多或更大的文档，可联系产研同学协助调整限制。

#### **类型二：授权OSS对接数据源**

妙搜支持对接云存储（OSS）作为存储数据源，实现对其中数据的搜索与问答。具体的对接授权步骤参考《[云存储（OSS）设置指南](https://help.aliyun.com/zh/model-studio/oss-setup-guide)》。

#### **类型三：**视频理解Agent引入数据源

对于视频素材，若需更精细的内容解析，可通过“影视传媒视频理解 Agent”对视频进行深度理解与分析，并将分析结果作为一路元数据（meta data）源导入妙搜。该元数据将与妙搜自有存储中的数据融合，共同参与后续的搜索与问答流程。

**说明**

影视传媒视频理解的操作文档参考《[影视传媒视频理解](https://help.aliyun.com/zh/model-studio/media-video-understanding)》。

#### **类型四：通过API引入数据源**

通过对接API的方式接入数据源。

1.  点击**配置API**，设置数据源的名称。
    
2.  修改配置信息接入外部API数据源，详情请参见[妙搜-通过API引入数据源](https://help.aliyun.com/zh/model-studio/miaosou-introduce-data-source-through-api)。
    

### **数据源支持多路元数据与标签管理**

对各类数据源支持查看和维护meta及标签信息，都可参与检索及知识问答；数据源下的数据支持搜索

-   针对不同模态的数据，支持对每条数据维护其标签和meta信息，meta信息目前只支持通过接口「CreateDataset」进行上传；且标签和meta信息均参与到搜索链路
    
    -   文本、图片：支持添加标签信息、meta信息（key value）
        
    -   音频：支持添加标签、meta信息（key value和ASR）
        
    -   视频：支持添加标签、meta信息（key value、ASR、视频理解Agent解析结果）
        

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6038620771/p1052519.png)

## **应用搜索数据源**

平台默认接入互联网搜索数据源。可以在**配置**页面下选择**启用的数据源**，从而将其纳入问答式搜索或纯搜索信源。

![8](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7389678571/p1011585.webp)

## 搜索问答

用户可输入搜索问题，并灵活配置搜索模式、目标数据源、回答形式、大模型及期望返回的模态类型等参数，确认后即可开始搜索。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6038620771/p1052521.png)

搜索结果：

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6038620771/p1052522.png)

### **元数据与标签可视化**

在完成“问答式搜索”或“纯搜索”后，可点击对应的音视频内容，查看视频理解分析结果及ASR生成的两路meta信息。且会针对query及答案中对应到meta信息最相关的部分，做片段及关键词的高亮。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6038620771/p1052520.png)

## **常见问题**

### **1\. 妙搜支持上传哪些类型的文件，**各类文件的上传大小限制是多少？

-   支持文件类型：妙搜数据源支持上传以下常见格式的文件：HTML、PDF、Word、Excel、CSV、图片、音频和视频。
    
-   各类文件的上传限制：
    
    -   HTML ：不超过 20 MB；
        
    -   PDF ：不超过 50 MB；
        
    -   Word ：不超过 20 MB；
        
    -   Excel ：不超过 20 MB；
        
    -   CSV ：不超过 15 MB；
        
    -   图片：不超过 40 MB；
        
    -   音频：不超过 100 MB；
        
    -   视频：不超过 2 GB。
        

**说明**

当前线上环境采用上述文件大小限制。如果您的业务需求超过上述限制，可以联系我们，研发可以针对您的需求进行调整。

### **2\. 妙搜是否支持**直接配置oss数据源？

支持，具体的配置方法可以参考《[云存储（OSS）设置指南](https://help.aliyun.com/zh/model-studio/oss-setup-guide)》。
