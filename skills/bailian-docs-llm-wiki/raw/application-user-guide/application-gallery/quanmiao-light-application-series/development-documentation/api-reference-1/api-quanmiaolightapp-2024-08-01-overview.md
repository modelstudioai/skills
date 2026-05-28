# API概览

## **API标准及多语言预置SDK**

本产品（`QuanMiaoLightApp/2024-08-01`）的OpenAPI采用[ROA](https://help.aliyun.com/zh/sdk/product-overview/roa-mechanism)签名风格。我们已经为开发者封装了常见编程语言的SDK，开发者可通过[下载SDK](https://api.aliyun.com/api-tools/sdk/QuanMiaoLightApp?version=2024-08-01)直接调用本产品OpenAPI而无需关心技术细节。如果现有SDK不能满足使用需求，可通过签名机制进行自签名对接。由于自签名细节非常复杂，需花费 5个工作日左右。因此建议加入我们的服务钉钉群（147535001692），在专家指导下进行签名对接。

在使用API前，您需要准备好身份账号及访问密钥（AccessKey），才能有效通过客户端工具（SDK、CLI等）访问API。细节请参见[获取AccessKey](https://help.aliyun.com/zh/ram/user-guide/create-an-accesskey-pair)。

## **自定义签名场景**

若您的业务场景有特殊需求，需通过自签名方式对接 API，建议优先咨询我们的技术支持团队（服务钉钉群：147535001692），获取专业指导以确保高效接入。

## **账号与安全准备**

阿里云账号具备对所有资源的完全管理权限。一旦 AccessKey 泄露，所有相关资源都将面临未经授权访问的风险。为确保安全，建议创建一个仅具备 API 访问权限的[RAM用户](https://help.aliyun.com/zh/ram/user-guide/create-a-ram-user)并配置其 AccessKey，同时基于最小权限原则 (PoLP) 配置 RAM 策略。仅在明确需要阿里云账号权限的特定场景下，才使用阿里云账号。

## 电商零售推广文案写作

API

标题

API概述

[RunMarketingInformationWriting](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-runmarketinginformationwriting)

电商零售推广文案写作

电商零售推广文案写作。

[RunMarketingInformationExtract](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-runmarketinginformationextract)

电商零售内容实体抽取

电商零售内容实体抽取。

## 传媒/零售文章风格与格式学习

API

标题

API概述

[RunStyleWriting](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-runstylewriting)

传媒/零售文章风格与格式学习

传媒/零售文章风格与格式学习。

## 影视互娱剧本创作

API

标题

API概述

[RunScriptRefine](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-runscriptrefine)

影视互娱剧本创作-剧本整理

剧本对话内容的整理。

[RunScriptChat](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-runscriptchat)

影视互娱剧本创作-交互式创作

长剧本创作。

[RunScriptPlanning](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-runscriptplanning)

影视互娱剧本创作-剧本策划

影视互娱乐剧本创作-剧本策划。

[RunScriptContinue](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-runscriptcontinue)

影视互娱剧本创作-剧本续写

影视互娱乐剧本创作-剧本续写。

## 影视传媒视频理解

API

标题

API概述

[SubmitVideoAnalysisTask](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-submitvideoanalysistask)

视频理解-提交异步任务

阿里云百炼轻应用-提交视频理解离线异步任务。

[GetVideoAnalysisTask](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-getvideoanalysistask)

视频理解-获取异步任务状态和结果

轻应用-获取视频理解异步任务结果。

[UpdateVideoAnalysisConfig](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-updatevideoanalysisconfig)

视频理解-更新配置

视频理解-更新配置。

[GetVideoAnalysisConfig](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-getvideoanalysisconfig)

视频理解-获取配置

视频理解：获取基础配置。

[RunVideoAnalysis](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-runvideoanalysis)

视频理解-在线任务

阿里云百炼轻应用-影视传媒视频理解。

[UpdateVideoAnalysisTask](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-updatevideoanalysistask)

视频理解-修改异步任务状态

视频理解-修改任务状态：目前仅支持取消任务。

[UpdateVideoAnalysisTasks](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-updatevideoanalysistasks)

视频理解-批量取消任务

视频理解-批量取消任务

## 影视传媒智能拆条

API

标题

API概述

[SubmitVideoDetectShotTask](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-submitvideodetectshottask)

智能拆条-提交异步任务

轻应用-视频拆条异步任务 使用视频拆条需先开通影视传媒视频理解（免费开通）https://bailian.console.aliyun.com/?tab=app#/app/app-market/quanmiao/video-comprehend 目前拆条提供三种场景视频的处理： 1、节目场景 2、新闻场景 3、其他场景 详细使用建议及参考prompt请查看下方补充说明。

[GetVideoDetectShotTask](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-getvideodetectshottask)

智能拆条-获取异步任务状态和结果

轻应用-获取视频拆条异步任务结果

[UpdateVideoDetectShotTask](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-updatevideodetectshottask)

智能拆条-修改异步任务状态

智能拆条-修改异步任务状态：目前仅支持取消任务。

[UpdateVideoDetectShotConfig](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-updatevideodetectshotconfig)

智能拆条-更新配置

智能拆条-更新配置

[GetVideoDetectShotConfig](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-getvideodetectshotconfig)

智能拆条-获取配置

智能拆条-获取配置

[RunVideoDetectShot](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-runvideodetectshot)

智能拆条-在线任务

轻应用-视频拆条 使用视频拆条需先开通影视传媒视频理解（免费开通）https://bailian.console.aliyun.com/?tab=app#/app/app-market/quanmiao/video-comprehend 目前拆条提供三种场景视频的处理： 1、节目场景 2、新闻场景 3、其他场景 详细使用建议及参考prompt请查看下方补充说明。

## 车机网络热点信息互动问答

API

标题

API概述

[RunHotTopicChat](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-runhottopicchat)

播报单（热榜）问答

阿里云百炼轻应用-车机/内容平台新闻热榜互动-播报单（热榜）问答：可以对播报单、新闻、开放域内容问答。

[RunHotTopicSummary](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-runhottopicsummary)

播报单热点自定义摘要生成

阿里云百炼轻应用-车机/内容平台新闻热榜互动-播报单热点自定义摘要生成：流式生成自定义风格的热点摘要。

## 泛企业VOC挖掘

API

标题

API概述

[RunEnterpriseVocAnalysis](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-runenterprisevocanalysis)

在线企业VOC分析

企业VOC分析。

## 泛企业线索挖掘

API

标题

API概述

[GenerateOutputFormat](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-generateoutputformat)

获取输出格式示例

轻应用-标签挖掘-获取示例输出格式。

[RunTagMiningAnalysis](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-runtagmininganalysis)

标签挖掘分析

轻应用-标签挖掘。

## 网络内容安全审核

API

标题

API概述

[RunNetworkContentAudit](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-runnetworkcontentaudit)

网络内容安全审核

轻应用-网络内容审核。

## 作文批改

API

标题

API概述

[RunEssayCorrection](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-runessaycorrection)

作文批改

作业批改

[RunOcrParse](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-runocrparse)

图片OCR解析

作文图片OCR解析

[SubmitEssayCorrectionTask](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-submitessaycorrectiontask)

提交作文批改任务

提交作文批改任务。

[GetEssayCorrectionTask](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-getessaycorrectiontask)

获取作文批改任务结果

获取作文批改结果

## 其他

API

标题

API概述

[GenerateBroadcastNews](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-generatebroadcastnews)

播报单（热榜）热点推荐

阿里云百炼轻应用-车机/内容平台新闻热榜互动-播报单热点推荐：理解用户意图，获取对应频道下热点列表。

[SubmitTagMiningAnalysisTask](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-submittagmininganalysistask)

提交标签挖掘分析任务

轻应用-标签挖掘。

[ListHotTopicSummaries](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-listhottopicsummaries)

查询完整播报单（热榜）

阿里云百炼-轻应用-车机/内容平台新闻热榜互动-查询完整播报单（热榜）：通过这个接口可以获取播报单所有内容。

[GetTagMiningAnalysisTask](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-gettagmininganalysistask)

获取标签挖掘分析任务结果

获取挖掘分析任务结果。

[HotNewsRecommend](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-hotnewsrecommend)

新闻热点推荐

热点新闻推荐

[GetFileContent](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-getfilecontent)

获取文件内容

获取文件内容

[CancelAsyncTask](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-cancelasynctask)

根据任务ID取消异步任务的执行

取消异步任务

[ExportAnalysisTagDetailByTaskId](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-exportanalysistagdetailbytaskid)

根据任务ID导出分析明细

导出挖掘任务明细

[GetEnterpriseVocAnalysisTask](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-getenterprisevocanalysistask)

获取企业VOC分析任务结果

获取企业VOC分析任务结果

[ListAnalysisTagDetailByTaskId](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-listanalysistagdetailbytaskid)

获取挖掘结果明细列表

获取挖掘分析结果明细列表

[SubmitEnterpriseVocAnalysisTask](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-submitenterprisevocanalysistask)

提交企业VOC挖掘异步任务

提交企业VOC异步任务
