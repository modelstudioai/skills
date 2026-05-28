# 车机网络热点信息互动问答计费文档

本文档主要介绍全妙产品矩阵里的AI Agent -- 车机网络热点互动问答 的计费方案。

## **计费说明**

计费方式：**开通型后付费（按量付费）**。开通服务本身不产生费用，仅在实际调用API时根据用量计费。

-   获取播报单：按调用版本数后付费；
    
-   个性化内容推荐 ：按调用的次数后付费；
    
-   新闻问答互动：按提问的次数后付费。
    

## **计费详情**

**计费项**

**计费**

**功能及计费说明**

**接口地址**

获取播报单及聚合摘要的写作风格化

1元/次

-   功能说明：
    
    -   获取播报单包含官方聚合新闻播报单和自定义播报单，自定义播报单支持用户根据频道、自定义热度、话题数量等生成专属播报单。
        
    -   根据客户诉求，从热榜里抽取符合其诉求的新闻信息并结构化展现。
        
-   计费说明：
    
    -   系统以每天3次的频率，在早上7点、 中午13点和晚上19点根据当下最新的实时新闻聚类，每天产出3版带图的新闻播报单。同个版本调多次，只收费1元。
        
    -   如果改过频道、热点条数或者风格，导致版本会改变，则调取时会重新收取1元。
        

-   [HotNewsRecommend - 新闻热点推荐](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-hotnewsrecommend)
    
-   [GetHotTopicBroadcast - 查询完整播报单（热榜）](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-gethottopicbroadcast)
    

-   功能说明：
    
    -   用户可以根据需求，自定义播报单的输出风格，以满足个性化体验。
        

[RunHotTopicSummary - 播报单热点自定义摘要生成](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-runhottopicsummary)

个性化内容推荐

0.009元/次

-   功能说明：
    
    -   通过主动发问等方式收集用户的偏好并结合当日榜单内容给用户推荐感兴趣的个性化内容。
        
-   计费说明
    
    -   每推荐一次收费0.009元。
        

如需要测试个性化推荐效果，请加 钉钉群（群号：101930016606） ，我们会以离线形式支持您进行测试。

新闻问答互动

0.018元/次

-   功能说明：
    
    -   支持基于生成的播报单内容进行问答；支持联网搜索问答；并支持答案配图等能力。
        
-   计费说明：
    
    -   用户提问收费0.018元/次。
        

-   [RunHotTopicChat - 播报单（热榜）问答](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-runhottopicchat)
    

若只需用【车机网络热点信息互动问答】agent的第一步 -- 获取播报单及聚合摘要的写作风格化，开通【新闻榜单订阅】即可（commonbuy地址：[新闻榜单订阅](https://common-buy.aliyun.com/?commodityCode=sfm_newshotlist_public_cn)）；如也要使用个性化推荐及新闻互动问答能力，需同时开通商品【全妙智能检索生成应用后付费API】（commonbuy地址：[全妙智能检索生成应用后付费API](https://common-buy.aliyun.com/?commodityCode=sfm_quanmiaoAPI_public_cn)）。

此外您还可以通过MCP server的形式使用此agent，对应地址为 [全妙网络热点信息播报MCP Server](https://bailian.console.aliyun.com/?spm=5176.29619931.J__Z58Z6CX7MY__Ll8p1ZOR.1.5f3c521cV95qKK&tab=mcp#/mcp-market/detail/quanmiao-hotnews)

## **账单地址**

账单查询地址：[账单详情](https://usercenter2.aliyun.com/finance/expense-report/expense-detail?spm=a2c4g.11186623.0.0.619355efACwmfT)。

## **产品地址**

可点击[产品地址](https://bailian.console.aliyun.com/?spm=5176.29619931.J__Z58Z6CX7MY__Ll8p1ZOR.1.74cd521c43xzda#/app/app-market/quanmiao/news-broadcast)进行产品体验。

## **相关文档**

[车机网络热点信息互动问答接口文档](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-dir-car-machine-network-hot-information-interactive-question-and-answer/)
