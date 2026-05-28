# API概览

## **API标准及多语言预置SDK**

本产品（`AiMiaoBi/2023-08-01`）的OpenAPI采用[RPC](https://help.aliyun.com/zh/sdk/product-overview/v3-request-structure-and-signature)签名风格。我们已经为开发者封装了常见编程语言的SDK，开发者可通过[下载SDK](https://api.aliyun.com/api-tools/sdk/AiMiaoBi?version=2023-08-01)直接调用本产品OpenAPI而无需关心技术细节。如果现有SDK不能满足使用需求，可通过签名机制进行自签名对接。由于自签名细节非常复杂，需花费 5个工作日左右。因此建议加入我们的服务钉钉群（147535001692），在专家指导下进行签名对接。

在使用API前，您需要准备好身份账号及访问密钥（AccessKey），才能有效通过客户端工具（SDK、CLI等）访问API。细节请参见[获取AccessKey](https://help.aliyun.com/zh/ram/user-guide/create-an-accesskey-pair)。

## **自定义签名场景**

若您的业务场景有特殊需求，需通过自签名方式对接 API，建议优先咨询我们的技术支持团队（服务钉钉群：147535001692），获取专业指导以确保高效接入。

## **账号与安全准备**

阿里云账号具备对所有资源的完全管理权限。一旦 AccessKey 泄露，所有相关资源都将面临未经授权访问的风险。为确保安全，建议创建一个仅具备 API 访问权限的[RAM用户](https://help.aliyun.com/zh/ram/user-guide/create-a-ram-user)并配置其 AccessKey，同时基于最小权限原则 (PoLP) 配置 RAM 策略。仅在明确需要阿里云账号权限的特定场景下，才使用阿里云账号。

## 通用接口

API

标题

API概述

[CreateToken](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-createtoken)

获取授权token

创建在线推理API的临时Token。

[ListDialogues](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listdialogues)

生成历史列表

在线推理场景的历史记录。

[ListVersions](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listversions)

获取版本信息

获取用户购买的版本信息。

[GetProperties](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getproperties)

获取配置信息

获取配置信息。包括不限于智能配置的风格，推理相关元数据配置等。

## 通用接口-文件上传下载

API

标题

API概述

[GenerateFileUrlByKey](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-generatefileurlbykey)

生成文件URL

生成临时可访问的公开url。

[GenerateUploadConfig](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-generateuploadconfig)

生成上传配置

生成文件上传配置。 1. 使用本接口 获取上传的配置 返回 PostUrl （妙笔内部OSS地址）、以及OSS临时鉴权信息：key、OSSAccessKeyId、Signature、policy，还有文件唯一标识：fileKey 2. 客户端 使用 PostUrl、以及临时鉴权信息：key、OSSAccessKeyId、Signature、policy 进行文件的上传 3. 使用 fileKey 调用 后续带有fileKey的接口 （例如：GenerateFileUrlByKey）

## 通用接口-异步任务管理

API

标题

API概述

[SubmitAsyncTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-submitasynctask)

提交异步任务

执行系统预定义的异步任务。

[CancelAsyncTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-cancelasynctask)

取消异步任务

取消已提交，尚未执行完成的异步任务。

[QueryAsyncTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-queryasynctask)

查询异步任务明细

查询已提交异步任务执行明细。

[ListAsyncTasks](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listasynctasks)

获取异步任务列表

获取异步任务列表。

## 通用接口-通用配置

API

标题

API概述

[CreateGeneralConfig](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-creategeneralconfig)

通用配置-创建

通用配置-创建

[ListGeneralConfigs](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listgeneralconfigs)

通用配置-列表

通用配置-列表

[GetGeneralConfig](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getgeneralconfig)

通用配置-详情

通用配置-查询。

[UpdateGeneralConfig](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-updategeneralconfig)

通用配置-修改

通用配置-修改。

[DeleteGeneralConfig](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-deletegeneralconfig)

通用配置-删除

通用配置-删除

## 妙笔-创作文章

API

标题

API概述

[RunAiHelperWriting](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runaihelperwriting)

AI帮写

妙笔：AI助手写作

[RunWritingV2](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runwritingv2)

智能写作

智能写作。

[RunWriting](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runwriting)

直接写作

直接写作

[RunStepByStepWriting](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runstepbystepwriting)

分步骤写作

使用大纲+摘编的分步骤的模式进行写作。

[RunTranslateGeneration](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runtranslategeneration)

中英翻译

AI妙笔-创作-中英文翻译。

[RunTextPolishing](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runtextpolishing)

润色

创作-文本润色。

[RunKeywordsExtractionGeneration](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runkeywordsextractiongeneration)

关键词抽取

AI妙笔-创作-抽取关键词。

[RunContinueContent](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runcontinuecontent)

内容续写

内容续写。

[RunWriteToneGeneration](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runwritetonegeneration)

文风改写

AI妙笔-创作-文风改写。

[RunTitleGeneration](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runtitlegeneration)

标题生成

妙笔：标题生成。

[RunSummaryGenerate](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runsummarygenerate)

摘要生成

内容摘要生成。

[RunExpandContent](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runexpandcontent)

内容扩写

内容扩写。

[RunAbbreviationContent](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runabbreviationcontent)

内容缩写

内容缩写。

[SearchNews](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-searchnews)

信息检索

根据输入检索新闻，目前仅支持互联网搜索。

[RunQuickWriting](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runquickwriting)

快速写作

可直接输入写作指令，进行快速写作。

[ListBuildConfigs](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listbuildconfigs)

获取系统自定义预设

获取系统自定义预设，用于创作文章 -> 直接生成中的内置选项。例如：写作文体、文章篇幅、输出语言、生成文章篇数等选项。

[GenerateImageTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-generateimagetask)

生成智能配图任务

根据文字异步生成图片。

[FetchImageTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-fetchimagetask)

获取图片任务执行结果

获取图片任务执行结果。

[FeedbackDialogue](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-feedbackdialogue)

反馈对话

反馈模型生成的内容质量。

## 妙笔-文体仿写

API

标题

API概述

[ListStyleLearningResult](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-liststylelearningresult)

获取文体学习分析结果列表

获取文体学习分析结果列表。

[RunStyleFeatureAnalysis](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runstylefeatureanalysis)

内容特点分析

内容特点分析。

[SaveStyleLearningResult](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-savestylelearningresult)

保存文体学习分析结果

保存自定义文体。

[DeleteStyleLearningResult](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-deletestylelearningresult)

删除自定义文体

删除指定自定义文体。

[GetStyleLearningResult](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getstylelearningresult)

获取文体学习分析结果

获取文体学习分析结果。

[ListWritingStyles](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listwritingstyles)

获取写作文体列表

获取文体列表。

## 妙笔-视频审校

API

标题

API概述

[SubmitVideoAudit](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-submitvideoaudit)

提交视频审校任务

提交视频审校

[QueryVideoAuditResult](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-queryvideoauditresult)

查询视频审校结果

查询视频审校结果

## 妙笔-文章审校-规则库管理

API

标题

API概述

[SubmitAuditNote](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-submitauditnote)

提交自定义规则库

妙笔为您提供了与公有云“智能审校”模块中相同的上传自定义规则库的功能。由于鉴权限制，用户需要使用自定义规则库文件的 fileKey 作为入参才能顺利调用本接口。该接口在被调用后，会对用户的自定义规则库进行结构化处理，并生成一个 xlsx 格式的结构化解析结果。您可以调用 GetAuditNoteProcessingStatus 接口查询结构化处理状态，也可以调用 DownloadAuditNote 接口获取结构化之后的规则库。接口功能正在迭代中，预计会在未来使用可访问的文件 URL 作为入参。

[ConfirmAndPostProcessAuditNote](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-confirmandpostprocessauditnote)

确认提交规则库用于审核

是否将本次提交自定义规则库得到的解析结果用于审核任务。由于解析结果可能不满足用户需求，因此我们为您提供了该接口用于二次确认。如果对提交的规则库解析满意，则可以直接将本次提交任务的 TaskId 作为入参，系统会对您上传的规则库做后处理，使它可以被用于审核。反之，您可以重新调用 SubmitAuditNote 接口上传修改之后的规则库。

[DownloadAuditNote](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-downloadauditnote)

下载规则库

您可以通过调用该接口下载结构化后的规则库，供您进行进一步处理。该接口同时拥有两个功能：下载未后处理的结构化规则库，或下载当前可用于审核的结构化规则库。具体使用方法，请参考入参说明。

[DeleteAuditNote](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-deleteauditnote)

删除规则库

删除用户账户下所有可供审核使用的自定义规则库。删除后无法找回，如果您有对规则库存档的需求，请预先使用 DownloadAuditNote 接口保存需要的规则库。

[GetAuditNotePostProcessingStatus](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getauditnotepostprocessingstatus)

获取规则库后处理进度

查询规则库后处理的进度。与 ConfirmAndPostProcessAuditNote 接口配合使用，供您查询当前后处理任务的状态。

[GetAuditNoteProcessingStatus](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getauditnoteprocessingstatus)

查询规则库上传状态

查询用户上传规则库的处理状态。通过该接口，用户可以查询到当前规则库上传任务的状态，并获取到解析后的规则库文件大小、存储路径等信息。

[GetAvailableAuditNotes](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getavailableauditnotes)

查询可用规则库

查询用户当前可供审核的规则库信息，只能查询到当前可用于审核的规则库。如果您想看到自定义规则库的具体内容，请使用 DownloadAuditNote 接口。

## 妙笔-文章审校-词库管理

API

标题

API概述

[ListAuditTerms](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listauditterms)

获取自定义词库记录

获取词库列表。

[AddAuditTerms](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-addauditterms)

添加自定义词库记录

添加审核自定义词库记录。

[EditAuditTerms](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-editauditterms)

编辑自定义词库记录

编辑审核自定义词库记录

[DeleteAuditTerms](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-deleteauditterms)

删除指定词库记录

删除指定的词库记录。

[SubmitImportTermsTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-submitimporttermstask)

提交导入词库任务

提交导入自定义词库任务

[FetchImportTermsTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-fetchimporttermstask)

获取导入词库任务结果

获取导入词库任务结果

[SubmitExportTermsTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-submitexporttermstask)

提交导出词库任务

导出词库任务

[FetchExportTermsTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-fetchexporttermstask)

获取导出词库任务结果

获取词库导出任务结果

## 妙笔-文章审校-事实性审核

API

标题

API概述

[SubmitFactAuditUrl](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-submitfactauditurl)

提交事实性审核 URL

妙笔为您提供了新的事实性审核能力，在联网搜索并判断正误的前提下，还支持用户自定义配置搜索来源 URL。

[GetFactAuditUrl](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getfactauditurl)

获取事实性审核 URL

获取当前正用于事实性审核的信源 URL。

[DeleteFactAuditUrl](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-deletefactauditurl)

删除事实性审核 URL

删除指定的用于事实性审核的 URL。

## 妙笔-文章审校

API

标题

API概述

[QueryAuditTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-queryaudittask)

查询审核结果

查询审核结果。

[SubmitAuditTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-submitaudittask)

提交审核任务

提交审核任务

[CancelAuditTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-cancelaudittask)

取消审核任务

取消审核任务

[SubmitSmartAudit](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-submitsmartaudit)

提交智能审校任务

提交智能审核

[GetSmartAuditResult](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getsmartauditresult)

查询智能审校结果

查询智能审核结果

[ListAuditContentErrorTypes](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listauditcontenterrortypes)

获取审校维度列表

获取审核维度列表

[ExportAuditContentResult](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-exportauditcontentresult)

导出智能审校报告

导出智能审核报告

## 妙笔-文档管理

API

标题

API概述

[GenerateExportWordTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-generateexportwordtask)

生成导出文档任务

生成内容导出文档任务

[FetchExportWordTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-fetchexportwordtask)

获取导出文档任务结果

获取异步导出文档任务结果

[CreateGeneratedContent](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-creategeneratedcontent)

保存文档

保存文档：用来保存妙笔中创作的文章，支持富文本。

[DeleteGeneratedContent](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-deletegeneratedcontent)

删除文档

删除文档：用来删除妙笔中创作的文章。

[UpdateGeneratedContent](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-updategeneratedcontent)

更新文档

更新文档：用来更新妙笔中创作的文章历史。

[GetGeneratedContent](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getgeneratedcontent)

获取文档

获取文档：用来查询妙笔中创作的文章历史。

[ListGeneratedContents](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listgeneratedcontents)

获取文档列表

获取文档列表：用来查询妙笔中创作的文章历史列表。

[ExportGeneratedContent](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-exportgeneratedcontent)

导出文档

导出文档：用来导出妙笔中创作的文章历史。

## 妙笔-素材库

API

标题

API概述

[SaveMaterialDocument](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-savematerialdocument)

保存素材

保存素材：保存素材库中素材。

[DeleteMaterialById](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-deletematerialbyid)

删除素材

删除素材：删除素材库中素材。

[UpdateMaterialDocument](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-updatematerialdocument)

更新素材

更新素材：更新素材库中素材。

[GetMaterialById](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getmaterialbyid)

获取素材

获取素材：获取素材库中素材详细信息。

[ListMaterialDocuments](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listmaterialdocuments)

获取素材列表

获取素材列表：获取素材库中素材列表。

## 妙笔-素材库-自定义文本

API

标题

API概述

[GetCustomText](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getcustomtext)

获取自定义文本

获取自定义文本。

[UpdateCustomText](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-updatecustomtext)

更新自定义文本

更新自定义文本。

[ListCustomText](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listcustomtext)

获取自定义文本列表

获取自定义文本列表。

[SaveCustomText](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-savecustomtext)

保存自定义文本

保存自定义文本。

[DeleteCustomText](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-deletecustomtext)

删除自定义文本

删除自定义文本。

[DocumentExtraction](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-documentextraction)

文档提取

从链接中提取文档内容。

## 妙笔-视频混剪

API

标题

API概述

[GetClipsBuildInResource](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getclipsbuildinresource)

获取智能混剪内置资源

获得智能混剪内置资源

[AsyncCreateClipsTimeLine](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-asynccreateclipstimeline)

创建剪辑口播时间线

智能剪辑timeline

[AsyncEditTimeline](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-asyncedittimeline)

编辑剪辑口播时间线

编辑剪辑任务的timeline

[AsyncUploadVideo](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-asyncuploadvideo)

异步上传视频剪辑素材

上传剪辑素材

[GetAutoClipsTaskInfo](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getautoclipstaskinfo)

获得剪辑任务信息

获得剪辑任务状态

[AsyncCreateClipsTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-asynccreateclipstask)

创建剪辑任务

生成剪辑视频

[ListAutoClipsTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listautoclipstask)

智能混剪任务列表

列出智能混剪任务列表

## 妙策-自定义数据源

API

标题

API概述

[SubmitCustomSourceTopicAnalysis](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-submitcustomsourcetopicanalysis)

提交自定义源话题选题分析任务

从自定义数据源提交选题热点分析

[GetCustomSourceTopicAnalysisTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getcustomsourcetopicanalysistask)

获取自定义源话题分析任务结果

获取自定义数据源-选题视角分析任务结果

[ExportCustomSourceAnalysisTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-exportcustomsourceanalysistask)

导出自定义源-话题分析任务结果

导出-自定义数据源-选题视角分析任务结果

## 公文库检索

API

标题

API概述

[ListDocumentRetrieve](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listdocumentretrieve)

公文库检索

根据复杂条件进行政务公文库的检索。

## 妙策-选题热点

API

标题

API概述

[RunTopicSelectionMerge](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runtopicselectionmerge)

选题热点融合

妙策选题策划聚合

[ListHotNewsWithType](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listhotnewswithtype)

获取选题热点列表

获取选题热点列表。

[ListHotSources](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listhotsources)

获取三方热榜源列表

获取所有平台热榜源列表。

[ListHotTopics](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listhottopics)

获取热点话题列表

获取热点话题列表。

[GetTopicById](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-gettopicbyid)

获取热点对象

根据ID获取热点事件信息。

[ListHotViewPoints](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listhotviewpoints)

获取热门视角列表

热门视角列表。

[ListTimedViewAttitude](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listtimedviewattitude)

获取时效性视角列表

时效性视角列表。

[ListFreshViewPoints](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listfreshviewpoints)

获取新颖视角列表

新颖视角列表。

[ListWebReviewPoints](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listwebreviewpoints)

获取网友视角列表

网友视角列表。

[ListPlanningProposal](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listplanningproposal)

获取选题策划列表

获取选题策划列表。

[ExportHotTopicPlanningProposals](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-exporthottopicplanningproposals)

导出选题策划文档

导出选题策划文档，响应为一个可公开访问的URL。一小时后失效。

## 妙策-自定义话题

API

标题

API概述

[DeleteCustomTopicByTopic](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-deletecustomtopicbytopic)

删除自定义热点事件

根据热点名称删除自定义热点事件。

[ListTopicViewPointRecommendEventList](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listtopicviewpointrecommendeventlist)

获取热点事件推荐观点列表

获取热点事件推荐观点列表。

[ListTopicRecommendEventList](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listtopicrecommendeventlist)

获取热点推荐事件列表

获取热点推荐事件。

[RunCustomHotTopicAnalysis](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runcustomhottopicanalysis)

自定义热点话题分析

自定义热点话题分析。

[RunCustomHotTopicViewPointAnalysis](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runcustomhottopicviewpointanalysis)

自定义选题视角分析

自定义选题视角分析。

[ListCustomViewPoints](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listcustomviewpoints)

获取自定义视角列表

自定义视角列表。

[DeleteCustomTopicViewPointById](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-deletecustomtopicviewpointbyid)

删除自定义选题视角

根据自定义选题视角ID删除自定义选题视角。

## 妙策-openapi

API

标题

API概述

[SubmitDocClusterTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-submitdocclustertask)

提交内容聚合任务

提交内容聚合任务。

[GetDocClusterTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getdocclustertask)

获取内容聚合任务结果

获取内容聚合任务结果。

[SubmitTopicSelectionPerspectiveAnalysisTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-submittopicselectionperspectiveanalysistask)

提交选题热点分析任务

提交选题热点分析任务。

[GetTopicSelectionPerspectiveAnalysisTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-gettopicselectionperspectiveanalysistask)

获取选题视角分析任务结果

获取选题视角分析任务结果。

[SubmitCustomTopicSelectionPerspectiveAnalysisTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-submitcustomtopicselectionperspectiveanalysistask)

提交自定义热点选题视角分析任务

提交自定义热点选题视角分析任务。

[GetCustomTopicSelectionPerspectiveAnalysisTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getcustomtopicselectionperspectiveanalysistask)

获取自定义选题视角分析任务结果

获取自定义选题视角分析任务结果。

## 妙策-新闻播报

API

标题

API概述

[GetHotTopicBroadcast](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-gethottopicbroadcast)

查询完整播报单（热榜）

查询新闻播报单。

[SubmitCustomHotTopicBroadcastJob](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-submitcustomhottopicbroadcastjob)

提交自定义播报单任务

提交自定义播报单任务。

[GetCustomHotTopicBroadcastJob](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getcustomhottopicbroadcastjob)

获取自定义播报单任务结果

获取自定义播报单任务结果。

## 妙策-企业VOC挖掘

API

标题

API概述

[ExportAnalysisTagDetailByTaskId](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-exportanalysistagdetailbytaskid)

导出标签挖掘结果

导出企业VOC分析任务明细列表。

[ValidateUploadTemplate](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-validateuploadtemplate)

校验VOC上传模板

校验企业VOC上传模板。

[SubmitEnterpriseVocAnalysisTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-submitenterprisevocanalysistask)

提交企业VOC分析任务

提交VOC异步任务。

[ListAnalysisTagDetailByTaskId](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listanalysistagdetailbytaskid)

根据任务ID获取标签分析明细列表

分页获取企业VOC分析任务明细列表。

[GetEnterpriseVocAnalysisTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getenterprisevocanalysistask)

获取企业VOC挖掘任务结果

获取企业VOC分析任务结果。

[GetCategoriesByTaskId](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getcategoriesbytaskid)

根据任务ID获取分类列表

获取某次标签挖掘结果分类。

## 妙搜-数据源

API

标题

API概述

[CreateDataset](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-createdataset)

数据源-创建

数据源管理-创建。

[GetDataset](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getdataset)

数据源-详情

数据源管理-详情。

[UpdateDataset](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-updatedataset)

数据源-修改

数据源管理-更新。

[ListDatasets](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listdatasets)

数据源-列表

数据源管理-查询。

[DeleteDataset](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-deletedataset)

数据源-删除

数据源管理-删除。

[AddDatasetDocument](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-adddatasetdocument)

数据源-添加文档到数据集

添加文档到数据源。

[GetDatasetDocument](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getdatasetdocument)

数据源-获取文档详情

获取数据源文档。

[UpdateDatasetDocument](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-updatedatasetdocument)

数据源-修改文档

修改数据源文档。

[ListDatasetDocuments](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listdatasetdocuments)

数据源-文档列表

查询数据源文档列表。

[SearchDatasetDocuments](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-searchdatasetdocuments)

数据源-搜索文档

搜索数据源文档。

[DeleteDatasetDocument](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-deletedatasetdocument)

数据源-删除数据集文档

删除数据源文档。

## 妙搜-智能搜索

API

标题

API概述

[RunSearchGeneration](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runsearchgeneration)

妙搜-智能搜索

AI妙搜-智能搜索生成：对应妙搜首页的搜索生成能力。此接口支持通用搜索和媒资搜索。支持用户问题澄清、多模态知识搜索、多agent生成等能力。 - 通用搜索：可以对数据集中知识进行语义检索，并对搜索结果进行多agent后处理，包括总结生成、摘编、时间线总结等。 - 媒资搜索：应搜尽搜，全文检索，召回更多相关知识，并可进行多agent后处理，包括聚类、新闻抽取等。

[ListSearchTasks](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listsearchtasks)

查询妙搜搜索生成历史任务列表

查询妙搜搜索生成历史任务列表。

[ListSearchTaskDialogues](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listsearchtaskdialogues)

查询妙搜搜索生成任务详情列表

查询妙搜搜索生成任务详情列表。

[ListSearchTaskDialogueDatas](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listsearchtaskdialoguedatas)

查询搜索生成任务对话详情中数据列表

查询搜索生成任务对话详情中数据列表。

[RunSearchSimilarArticles](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runsearchsimilararticles)

妙搜-文搜文

妙搜-文搜文。

## 系统配置-干预配置

API

标题

API概述

[ListInterveneCnt](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listintervenecnt)

获得所有干预项的数量

获得干预项目数量列表。

[ListIntervenes](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listintervenes)

列出干预项

获得干预项列表。

[ImportInterveneFile](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-importintervenefile)

同步导入干预项文件

导入干预文件。

[InsertInterveneGlobalReply](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-insertinterveneglobalreply)

插入干预全局回复项

设置干预全局回复。

[ImportInterveneFileAsync](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-importintervenefileasync)

异步导入干预项文件

异步导入干预文件。

[GetInterveneTemplateFileUrl](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getintervenetemplatefileurl)

获得干预导入模版文件地址

获得干预导入模版文件下载地址。

[ClearIntervenes](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-clearintervenes)

清除所有干预项

清除所有干预内容。

[GetInterveneGlobalReply](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getinterveneglobalreply)

获得干预全局回复内容

获得干预全局回复。

[ListInterveneRules](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listintervenerules)

列出干预规则

获得干预规则列表。

[ListInterveneImportTasks](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listinterveneimporttasks)

列出干预项导入任务

获得导入任务列表。

[InsertInterveneRule](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-insertintervenerule)

插入干预规则

插入干预规则。

[GetInterveneRuleDetail](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getinterveneruledetail)

获得干预规则的详情

获得干预项规则详情。

[DeleteInterveneRule](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-deleteintervenerule)

删除干预规则

删除干预规则。

[ExportIntervenes](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-exportintervenes)

导出干预项内容

导出所有干预内容。

[GetInterveneImportTaskInfo](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getinterveneimporttaskinfo)

获得干预项目导入任务信息

获得导入任务信息。

## 系统配置-信源管理

API

标题

API概述

[SaveDataSourceOrderConfig](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-savedatasourceorderconfig)

保存信源权重配置

保存用户写作信源配置，通用搜索信源配置的配置信息。

[GetDataSourceOrderConfig](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getdatasourceorderconfig)

获取信源配置权重数据

获取写作信源，通用搜索信源的配置信息。

## 妙读-基础操作类

API

标题

API概述

[GetDocInfo](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getdocinfo)

获取文档信息

妙读获取文档信息。

[GetFileContentLength](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getfilecontentlength)

获取文件长度

妙读获得文档字数。

[UploadBook](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-uploadbook)

书籍上传

妙读上传书籍。

[UploadDoc](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-uploaddoc)

文档上传

妙读上传文档接口。

[ListDocs](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listdocs)

获取文档列表

妙读获取文档列表。

[DeleteDocs](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-deletedocs)

批量删除文档

妙读删除多个文档。

## 妙读-生成类

API

标题

API概述

[RunMultiDocIntroduction](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runmultidocintroduction)

多文档聚合摘要

针对多篇文章、视频或者URL，生成总分结构的摘要（几篇文章的综合概述、关键要点）。此外支持多种多语言的输入和输出。

[RunDocBrainmap](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-rundocbrainmap)

全文脑图

针对文章或者书，生成三级脑图，且支持生成多语种，支持控制脑图第二级数量，支持控制叶子节点的字数。

[RunDocIntroduction](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-rundocintroduction)

文档导读

针对一篇文章、视频或者URL，生成文章的导读内容，包含全文总结、关键要点、章节速览（即分段、每段的总结、段落摘要）。此外支持多种多语言的输入和输出。如果用户仅需要对文章进行全文总结，可使用RunDocSummary接口实现，具体请参见https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-rundocsummary。

[RunDocSummary](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-rundocsummary)

文档摘要

针对一篇文章、视频或者URL，生成文章的摘要内容，即全文总结。此外支持多种多语言的输入和输出。

[RunDocWashing](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-rundocwashing)

改写

把一篇文章改换成指定风格。

[RunBookIntroduction](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runbookintroduction)

书籍导读（抽取书籍卖点/书籍摘要）

基于一本书，抽取书籍的内容概要，以及结构化的卖点、热词信息。

[RunBookBrainmap](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runbookbrainmap)

书籍脑图

妙读生成书籍脑图。

[RunCommentGeneration](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runcommentgeneration)

客户之声预测

针对指定文章，预测用户之声。

## 妙读-抽取类

API

标题

API概述

[RunHotword](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runhotword)

抽取关键词

基于指定文章抽取关键词。关键词主要是指在特定领域或行业中具有代表性和识别度的专业术语或概念，它们能够精准地描述和概括某一行业内的核心内容、重要人物、关键事件或技术名词。

## 妙读-问答类

API

标题

API概述

[RunGenerateQuestions](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-rungeneratequestions)

猜你想问

输入一个query，返回几个相关query。

[RunDocQa](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-rundocqa)

文档问答（文章问答/多模态文件问答）

文章问答：针对一个自然语言类的query，在指定的文章范围内给出文字答案（有图则会配图），并显示溯源信息。 多模态文件问答：针对一个自然语言类的query，在指定的多模态文件范围内给出文字答案，并带上相关的图片、视频片段或者文字，并显示溯源信息。

## 妙读-其他

API

标题

API概述

[RunDocTranslation](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-rundoctranslation)

文档翻译

中英文互译接口。

[RunDocSmartCard](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-rundocsmartcard)

文档智能卡片

针对划选的文字或指定chat，自动打标并生成一个卡片笔记。

[RunBookSmartCard](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runbooksmartcard)

书籍智能卡片

书籍智能卡片接口。

## 深度写作

API

标题

API概述

[SubmitDeepWriteTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-submitdeepwritetask)

提交深度写作任务

提交深度写作任务。 用户可以根据要研究或分析的主题，填入问题、指令、附件等信息，来提交深度写作任务。该任务会在系统后台调度和执行。

[GetDeepWriteTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getdeepwritetask)

查询深度写作任务

查询深度写作任务。 主要用来查询指定任务的运行状态。

[GetDeepWriteTaskResult](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getdeepwritetaskresult)

查询深度写作任务的结果

查询深度写作任务的结果。 如果指定任务没有执行完成（排队、执行中、失败、取消等），会返回当前执行状态。如果指定任务已完成，会以URL的形式返回该任务的产出物的压缩包，供用户下载查看。

[CancelDeepWriteTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-canceldeepwritetask)

取消深度写作任务

取消深度写作任务。

[RunDeepWriting](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-rundeepwriting)

查询深度写作事件

查询深度写作事件。 系统以SSE事件的形式下发任务执行过程中的详细信息。

## PPT生成

API

标题

API概述

[ListEnterprisePptTemplates](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listenterpriseppttemplates)

查询企业专属PPT模板列表

查询企业专属PPT模板列表

[InitiatePptCreationV2](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-initiatepptcreationv2)

初始化PPT创建操作

初始化PPT创建操作V2

[ListPptTemplates](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listppttemplates)

查询PPT模板列表

查询PPT模板列表

[GetPptTemplateSelector](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getppttemplateselector)

查询PPT模板筛选器

查询PPT模板筛选器

[GetPptArtifactExportResult](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getpptartifactexportresult)

查询PPT导出任务的结果

查询PPT导出任务的结果

[ExportPptArtifact](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-exportpptartifact)

导出PPT作品

导出PPT作品

[GetPptArtifact](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getpptartifact)

查询PPT作品信息

查询PPT作品信息。

[ListPptArtifacts](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listpptartifacts)

查询PPT作品列表

查询PPT作品列表

[RunPptOutlineGeneration](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runpptoutlinegeneration)

生成PPT大纲内容

生成PPT大纲内容

[InitiatePptCreation](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-initiatepptcreation)

初始化用来创建PPT的会话

重要说明：这个接口涉及到扣费，请注意费用 这个接口包含两个操作： 1. 下发用于初始化“PPT生成”的前端组件的code 2. 进行计费

[GetPptConfig](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getpptconfig)

获取PPT组件配置

获取PPT组件配置

[BindPptArtifact](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-bindpptartifact)

绑定PPT作品信息

绑定PPT作品信息

[DeletePptArtifact](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-deletepptartifact)

删除PPT作品

删除PPT作品

## 标书生成

API

标题

API概述

[AsyncUploadTenderDoc](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-asyncuploadtenderdoc)

招标文档解析

上传招标书文件

[GetBiddingRemainLimitNum](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getbiddingremainlimitnum)

获得标书写作剩余额度

获得标书功能剩余额度

[GetBiddingDocInfo](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getbiddingdocinfo)

获得标书写作结果

获得标书写作结果接口

[EditBiddingDoc](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-editbiddingdoc)

编辑标书内容

编辑标书内容接口

[DownloadBiddingDoc](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-downloadbiddingdoc)

下载标书文件

标书下载接口

[AsyncWritingBiddingDoc](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-asyncwritingbiddingdoc)

标书写作

标书写作接口

[ListBiddingDoc](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listbiddingdoc)

列出标书写作任务

获得标书写作任务列表

## 其他

API

标题

API概述

[RunVideoScriptGenerate](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runvideoscriptgenerate)

AI生成视频剪辑脚本

AI生成视频剪辑脚本

[GetSmartClipTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getsmartcliptask)

获取智能剪辑任务结果

查询一键成片剪辑任务。

[SubmitSmartClipTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-submitsmartcliptask)

提交智能一键成片任务

提交一键成片剪辑任务。

[SaveOrUpdateOssConfig](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-saveorupdateossconfig)

配置-云存储-参数配置

配置-云存储-参数配置

[CreateDataPermissions](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-createdatapermissions)

权限-批量添加

权限-批量添加： - 数据集权限：

[DeleteDataPermissions](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-deletedatapermissions)

权限-删除

权限-批量删除： - 数据集权限

[ListDataPermissions](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listdatapermissions)

权限-列表

权限-列表 - 数据集

[GenerateViewPoint](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-generateviewpoint)

生成选题视角（已过时，不推荐使用）

生成选题视角。

GetPptInfo

查询PPT任务信息

查询PPT任务信息
