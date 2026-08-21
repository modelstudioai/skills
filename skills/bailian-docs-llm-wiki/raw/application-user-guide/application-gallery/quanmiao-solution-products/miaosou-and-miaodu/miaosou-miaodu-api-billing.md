# 计费说明（妙搜和妙读）

本文档介绍全妙-妙搜和妙读的计费说明。

## **计费概述**

1.  妙搜计费分为在线和离线两部分：
    

-   在线：通过问答式搜索和纯搜索进行问答所消耗的大模型Token量；
    
-   离线：包含各种模态的文件存储及索引存储，各种模态文件的预处理，各种模态文件的向量索引。
    

2.  妙读则统一按接口调用消耗的 Token 计费。
    

## **开通&产品地址**

-   开通产品：点击[全妙智能检索生成应用后付费API](https://common-buy.aliyun.com/?commodityCode=sfm_quanmiaoAPI_public_cn)打开页面，选择需要开通的产品（妙搜/妙读）；
    
-   妙搜SaaS产品地址：[妙搜控制台](https://aimiaobi.console.aliyun.com/?product_code=g_broadscope_search&from=bailian#/search_copilot_reference)，接口地址：[妙搜-智能搜索](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runsearchgeneration)；
    
-   妙读线上仅提供PaaS接口调用，接口地址：[获取文档信息](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getdocinfo)。
    

## **妙搜计费说明**

### **在线计费项**

用户在 SaaS 页面可选择问答式搜索或纯搜索，系统将根据所选模型按以下规则计费：

**计费项**

**子计费项**

**计费**

全妙-max（思考/非思考）

quanmiao-max

0.06元/千Token

全妙-Plus（思考/非思考）

quanmiao-Plus

0.002元/千Token

### **离线计费项**

**计费项**

**子计费项**

**计费**

**选择说明**

索引存储（**必选**，子计费项二选一）

索引存储-性能优先

0.0118元/小时\*GB

**检索速度快**，适用于知识库体量**≥1TB**、同时在线用户数量多的情况。

索引存储-成本优先

0.0066元/小时\*GB

**检索速度慢**，适用于知识库体量**＜1TB**、同时在线用户数量少的情况。

多模态文件存储（**可选项**，**请根据说明要求进行选择**）

多模态文件存储

0.0003元/小时\*GB

如果您**仅有文本知识库**，**且其被存放在**[**阿里云OSS**](https://www.aliyun.com/product/oss?spm=5176.21213303.J_ZGek9Blx07Hclc3Ddt9dg.2.77d12f3dsETRba&scm=20140722.S_card@@%E4%BA%A7%E5%93%81@@218843.S_new~UND~card.ID_card@@%E4%BA%A7%E5%93%81@@218843-RL_%E9%98%BF%E9%87%8C%E4%BA%91oss%E5%AD%98%E5%82%A8-LOC_2024SPSearchCard-OR_ser-PAR1_2150423017666263353741744efe07-V_4-RE_new5-P0_0-P1_0)**或其他支持读取的云上**，**此项可不选**；

如果您的**知识库里涉及视频**，**此项必选**，因为在构建索引时会将抽帧自动存于此处并计费。

文件格式转换与处理（**可选项**，**请根据说明要求进行选择**）

文件格式转换与处理

1.20元/小时

您需要对知识库中的音视频做ASR转写，并参与检索与召回。

文本及多模态文件的向量构建（**必选**）

quanmiao-clip

0.0004元/千Token

您需要对知识库中的文本及多模态文件进行向量化（Embedding）处理。

## **妙读计费说明**

调用妙读接口（包括生成类、抽取类、问答类）时，可通过 `ModelName` 字段指定模型（ `quanmiao-max` 或 `quanmiao-plus`），系统将根据所选模型的实际 Token 消耗进行计费。

**计费项**

**计费**

quanmiao-max

0.06元/千Token

quanmiao-Plus

0.002元/千Token

## **接口调用最佳实践**

-   妙搜：[妙搜API最佳实践](https://help.aliyun.com/zh/model-studio/best-practices-for-miaosou-api/#2c08b4f8e2wz3)；
    
-   妙读：[妙读最佳实践](https://help.aliyun.com/zh/model-studio/miaodu-best-practices)。
    

## **账单查询**

请点击[账单详情](https://usercenter2.aliyun.com/finance/expense-report/expense-detail?spm=a2c4g.11186623.0.0.619355efACwmfT)查看账单。
