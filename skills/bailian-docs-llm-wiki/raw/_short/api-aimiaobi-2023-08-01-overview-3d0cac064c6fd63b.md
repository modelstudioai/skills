# API概览

## API标准及多语言预置SDK

本产品（`AiMiaoBi/2023-08-01`）的OpenAPI采用[RPC](https://help.aliyun.com/zh/sdk/product-overview/v3-request-structure-and-signature)签名风格。我们已经为开发者封装了常见编程语言的SDK，开发者可通过[下载SDK](https://api.aliyun.com/api-tools/sdk/AiMiaoBi?version=2023-08-01)直接调用本产品OpenAPI而无需关心技术细节。如果现有SDK不能满足使用需求，可通过签名机制进行自签名对接。由于自签名细节非常复杂，需花费 5个工作日左右。因此建议加入我们的服务钉钉群（147535001692），在专家指导下进行签名对接。

在使用API前，您需要准备好身份账号及访问密钥（AccessKey），才能有效通过客户端工具（SDK、CLI等）访问API。细节请参见[获取AccessKey](https://help.aliyun.com/zh/ram/user-guide/create-an-accesskey-pair)。

## 自定义签名场景

若您的业务场景有特殊需求，需通过自签名方式对接 API，建议优先咨询我们的技术支持团队（服务钉钉群：147535001692），获取专业指导以确保高效接入。

## 账号与安全准备

阿里云账号具备对所有资源的完全管理权限。一旦 AccessKey 泄露，所有相关资源都将面临未经授权访问的风险。为确保安全，建议创建一个仅具备 API 访问权限的[RAM用户](https://help.aliyun.com/zh/ram/user-guide/create-a-ram-user)并配置其 AccessKey，同时基于最小权限原则 (PoLP) 配置 RAM 策略。仅在明确需要阿里云账号权限的特定场景下，才使用阿里云账号。

## 通用接口

API

标题

API概述

[CreateToken](raw/_short/api-aimiaobi-2023-08-01-createtoken-31d0f72627ed1e95.md)

获取授权token

创建在线推理API的临时Token。

[ListDialogues](raw/_short/api-aimiaobi-2023-08-01-listdialogues-633f18a2791021db.md)

生成历史列表

在线推理场景的历史记录。

[ListVersions](raw/_short/api-aimiaobi-2023-08-01-listversions-7e06722f5d06863e.md)

获取版本信息

获取用户购买的版本信息。

[GetProperties](raw/_short/api-aimiaobi-2023-08-01-getproperties-b79eceec87432e84.md)

获取配置信息

获取配置信息。包括不限于智能配置的风格，推理相关元数据配置等。

## 通用接口-文件上传下载

API

标题

API概述

[GenerateFileUrlByKey](raw/_short/api-aimiaobi-2023-08-01-generatefileurlbykey-43a4fbecc2395492.md)

生成文件URL

生成临时可访问的公开url。

[GenerateUploadConfig](raw/_short/api-aimiaobi-2023-08-01-generateuploadconfig-6bb22e9b8a3c683c.md)

生成上传配置

生成文件上传配置。 1. 使用本接口 获取上传的配置 返回 PostUrl （妙笔内部OSS地址）、以及OSS临时鉴权信息：key、OSSAccessKeyId、Signature、policy，还有文件唯一标识：fileKey 2. 客户端 使用 PostUrl、以及临时鉴权信息：key、OSSAccessKeyId、Signature、policy 进行文件的上传 3. 使用 fileKey 调用 后续带有fileKey的接口 （例如：GenerateFileUrlByKey）

## 通用接口-异步任务管理

API

标题

API概述

[SubmitAsyncTask](raw/_short/api-aimiaobi-2023-08-01-submitasynctask-b8e07c70487ee1e2.md)

提交异步任务

执行系统预定义的异步任务。

[CancelAsyncTask](raw/_short/api-aimiaobi-2023-08-01-cancelasynctask-58375d56808add96.md)

取消异步任务

取消已提交，尚未执行完成的异步任务。

[QueryAsyncTask](raw/_short/api-aimiaobi-2023-08-01-queryasynctask-8aa4356039580ce4.md)

查询异步任务明细

查询已提交异步任务执行明细。

[ListAsyncTasks](raw/_short/api-aimiaobi-2023-08-01-listasynctasks-b4270d078065c3ba.md)

获取异步任务列表

获取异步任务列表。

## 通用接口-通用配置

API

标题

API概述

[CreateGeneralConfig](raw/_short/api-aimiaobi-2023-08-01-creategeneralconfig-5fd6ad7a5aceecc5.md)

通用配置-创建

通用配置-创建

[ListGeneralConfigs](raw/_short/api-aimiaobi-2023-08-01-listgeneralconfigs-a889bc46882e86e6.md)

通用配置-列表

通用配置-列表

[GetGeneralConfig](raw/_short/api-aimiaobi-2023-08-01-getgeneralconfig-122f3097253cebd4.md)

通用配置-详情

通用配置-查询。

[UpdateGeneralConfig](raw/_short/api-aimiaobi-2023-08-01-updategeneralconfig-a6333a8d0884350c.md)

通用配置-修改

通用配置-修改。

[DeleteGeneralConfig](raw/_short/api-aimiaobi-2023-08-01-deletegeneralconfig-e2d486a6149dc804.md)

通用配置-删除

通用配置-删除

## 妙笔-创作文章

API

标题

API概述

[RunAiHelperWriting](raw/_short/api-aimiaobi-2023-08-01-runaihelperwriting-1492711ad2fd2716.md)

AI帮写

妙笔：AI助手写作

[RunWritingV2](raw/_short/api-aimiaobi-2023-08-01-runwritingv2-29d0abaf2738f46a.md)

智能写作

智能写作。

[RunWriting](raw/_short/api-aimiaobi-2023-08-01-runwriting-9d6e099473aae89e.md)

直接写作

直接写作

[RunStepByStepWriting](raw/_short/api-aimiaobi-2023-08-01-runstepbystepwriting-334d441c5a2388c5.md)

分步骤写作

使用大纲+摘编的分步骤的模式进行写作。

[RunTranslateGeneration](raw/_short/api-aimiaobi-2023-08-01-runtranslategeneration-b780b5a3f4af697b.md)

中英翻译

AI妙笔-创作-中英文翻译。

[RunTextPolishing](raw/_short/api-aimiaobi-2023-08-01-runtextpolishing-9673d4832b2a38ee.md)

润色

创作-文本润色。

[RunKeywordsExtractionGeneration](raw/_short/api-aimiaobi-2023-08-01-runkeywordsextractiongen-a558548b4828a2a6.md)

关键词抽取

AI妙笔-创作-抽取关键词。

[RunContinueContent](raw/_short/api-aimiaobi-2023-08-01-runcontinuecontent-2253fd16575800be.md)

内容续写

内容续写。

[RunWriteToneGeneration](raw/_short/api-aimiaobi-2023-08-01-runwritetonegeneration-52d5e2eb7aceaffc.md)

文风改写

AI妙笔-创作-文风改写。

[RunTitleGeneration](raw/_short/api-aimiaobi-2023-08-01-runtitlegeneration-dce82a814e9d2d49.md)

标题生成

妙笔：标题生成。

[RunSummaryGenerate](raw/_short/api-aimiaobi-2023-08-01-runsummarygenerate-6d8d20235b9716a2.md)

摘要生成

内容摘要生成。

[RunExpandContent](raw/_short/api-aimiaobi-2023-08-01-runexpandcontent-a2bbe2a2a1bf2f84.md)

内容扩写

内容扩写。

[RunAbbreviationContent](raw/_short/api-aimiaobi-2023-08-01-runabbreviationcontent-9d4883501cf8bfb9.md)

内容缩写

内容缩写。

[SearchNews](raw/_short/api-aimiaobi-2023-08-01-searchnews-a4ff1a25537b0ca8.md)

信息检索

根据输入检索新闻，目前仅支持互联网搜索。

[RunQuickWriting](raw/_short/api-aimiaobi-2023-08-01-runquickwriting-0913fdae211015fe.md)

快速写作

可直接输入写作指令，进行快速写作。

[ListBuildConfigs](raw/_short/api-aimiaobi-2023-08-01-listbuildconfigs-3cc338f62bb472ca.md)

获取系统自定义预设

获取系统自定义预设，用于创作文章 -> 直接生成中的内置选项。例如：写作文体、文章篇幅、输出语言、生成文章篇数等选项。

[GenerateImageTask](raw/_short/api-aimiaobi-2023-08-01-generateimagetask-96a6665068d7d7a4.md)

生成智能配图任务

根据文字异步生成图片。

[FetchImageTask](raw/_short/api-aimiaobi-2023-08-01-fetchimagetask-955891bc23019c34.md)

获取图片任务执行结果

获取图片任务执行结果。

[FeedbackDialogue](raw/_short/api-aimiaobi-2023-08-01-feedbackdialogue-7e2be294b274b693.md)

反馈对话

反馈模型生成的内容质量。

## 妙笔-文体仿写

API

标题

API概述

[ListStyleLearningResult](raw/_short/api-aimiaobi-2023-08-01-liststylelearningresult-39f16039f72598b1.md)

获取文体学习分析结果列表

获取文体学习分析结果列表。

[RunStyleFeatureAnalysis](raw/_short/api-aimiaobi-2023-08-01-runstylefeatureanalysis-160e341164f4c588.md)

内容特点分析

内容特点分析。

[SaveStyleLearningResult](raw/_short/api-aimiaobi-2023-08-01-savestylelearningresult-56dac23f73924d93.md)

保存文体学习分析结果

保存自定义文体。

[DeleteStyleLearningResult](raw/_short/api-aimiaobi-2023-08-01-deletestylelearningresul-c94fd4b7dfe5101b.md)

删除自定义文体

删除指定自定义文体。

[GetStyleLearningResult](raw/_short/api-aimiaobi-2023-08-01-getstylelearningresult-456707d84adbf341.md)

获取文体学习分析结果

获取文体学习分析结果。

[ListWritingStyles](raw/_short/api-aimiaobi-2023-08-01-listwritingstyles-52bccb929c9fee6e.md)

获取写作文体列表

获取文体列表。

## 妙笔-视频审校

API

标题

API概述

[SubmitVideoAudit](raw/_short/api-aimiaobi-2023-08-01-submitvideoaudit-f1daecd67484be9a.md)

提交视频审校任务

提交视频审校

[QueryVideoAuditResult](raw/_short/api-aimiaobi-2023-08-01-queryvideoauditresult-d063c7e865ff6788.md)

查询视频审校结果

查询视频审校结果

## 妙笔-文章审校-规则库管理

API

标题

API概述

[SubmitAuditNote](raw/_short/api-aimiaobi-2023-08-01-submitauditnote-d429bd0fa8ba411a.md)

提交自定义规则库

妙笔为您提供了与公有云“智能审校”模块中相同的上传自定义规则库的功能。由于鉴权限制，用户需要使用自定义规则库文件的 fileKey 作为入参才能顺利调用本接口。该接口在被调用后，会对用户的自定义规则库进行结构化处理，并生成一个 xlsx 格式的结构化解析结果。您可以调用 GetAuditNoteProcessingStatus 接口查询结构化处理状态，也可以调用 DownloadAuditNote 接口获取结构化之后的规则库。接口功能正在迭代中，预计会在未来使用可访问的文件 URL 作为入参。

[ConfirmAndPostProcessAuditNote](raw/_short/api-aimiaobi-2023-08-01-confirmandpostprocessaud-02f771c9a5326671.md)

确认提交规则库用于审核

是否将本次提交自定义规则库得到的解析结果用于审核任务。由于解析结果可能不满足用户需求，因此我们为您提供了该接口用于二次确认。如果对提交的规则库解析满意，则可以直接将本次提交任务的 TaskId 作为入参，系统会对您上传的规则库做后处理，使它可以被用于审核。反之，您可以重新调用 SubmitAuditNote 接口上传修改之后的规则库。

[DownloadAuditNote](raw/_short/api-aimiaobi-2023-08-01-downloadauditnote-b2b15d4831e61bf7.md)

下载规则库

您可以通过调用该接口下载结构化后的规则库，供您进行进一步处理。该接口同时拥有两个功能：下载未后处理的结构化规则库，或下载当前可用于审核的结构化规则库。具体使用方法，请参考入参说明。

[DeleteAuditNote](raw/_short/api-aimiaobi-2023-08-01-deleteauditnote-295374bda0cc78a8.md)

删除规则库

删除用户账户下所有可供审核使用的自定义规则库。删除后无法找回，如果您有对规则库存档的需求，请预先使用 DownloadAuditNote 接口保存需要的规则库。

[GetAuditNotePostProcessingStatus](raw/_short/api-aimiaobi-2023-08-01-getauditnotepostprocessi-10b0d630c7d4777f.md)

获取规则库后处理进度

查询规则库后处理的进度。与 ConfirmAndPostProcessAuditNote 接口配合使用，供您查询当前后处理任务的状态。

[GetAuditNoteProcessingStatus](raw/_short/api-aimiaobi-2023-08-01-getauditnoteprocessingst-42f3952de60d4eaf.md)

查询规则库上传状态

查询用户上传规则库的处理状态。通过该接口，用户可以查询到当前规则库上传任务的状态，并获取到解析后的规则库文件大小、存储路径等信息。

[GetAvailableAuditNotes](raw/_short/api-aimiaobi-2023-08-01-getavailableauditnotes-17f54efd8b06c91c.md)

查询可用规则库

查询用户当前可供审核的规则库信息，只能查询到当前可用于审核的规则库。如果您想看到自定义规则库的具体内容，请使用 DownloadAuditNote 接口。

## 妙笔-文章审校-词库管理

API

标题

API概述

[ListAuditTerms](raw/_short/api-aimiaobi-2023-08-01-listauditterms-0cdf6342a3c1ba2c.md)

获取自定义词库记录

获取词库列表。

[AddAuditTerms](raw/_short/api-aimiaobi-2023-08-01-addauditterms-2421387c4f814ba2.md)

添加自定义词库记录

添加审核自定义词库记录。

[EditAuditTerms](raw/_short/api-aimiaobi-2023-08-01-editauditterms-19833e85ab21ee1f.md)

编辑自定义词库记录

编辑审核自定义词库记录

[DeleteAuditTerms](raw/_short/api-aimiaobi-2023-08-01-deleteauditterms-5bec31d0945e0f6e.md)

删除指定词库记录

删除指定的词库记录。

[SubmitImportTermsTask](raw/_short/api-aimiaobi-2023-08-01-submitimporttermstask-9a94f483ca7bc550.md)

提交导入词库任务

提交导入自定义词库任务

[FetchImportTermsTask](raw/_short/api-aimiaobi-2023-08-01-fetchimporttermstask-3e325a59df01c370.md)

获取导入词库任务结果

获取导入词库任务结果

[SubmitExportTermsTask](raw/_short/api-aimiaobi-2023-08-01-submitexporttermstask-4713f23ec141d82e.md)

提交导出词库任务

导出词库任务

[FetchExportTermsTask](raw/_short/api-aimiaobi-2023-08-01-fetchexporttermstask-a316ab339965da1d.md)

获取导出词库任务结果

获取词库导出任务结果

## 妙笔-文章审校-事实性审核

API

标题

API概述

[SubmitFactAuditUrl](raw/_short/api-aimiaobi-2023-08-01-submitfactauditurl-50ef7c2f7fbcdd5a.md)

提交事实性审核 URL

妙笔为您提供了新的事实性审核能力，在联网搜索并判断正误的前提下，还支持用户自定义配置搜索来源 URL。

[GetFactAuditUrl](raw/_short/api-aimiaobi-2023-08-01-getfactauditurl-b88dfd44ccf55f6b.md)

获取事实性审核 URL

获取当前正用于事实性审核的信源 URL。

[DeleteFactAuditUrl](raw/_short/api-aimiaobi-2023-08-01-deletefactauditurl-7c2603d348156de8.md)

删除事实性审核 URL

删除指定的用于事实性审核的 URL。

## 妙笔-文章审校

API

标题

API概述

[SubmitSmartAudit](raw/_short/api-aimiaobi-2023-08-01-submitsmartaudit-c9bb41d30ae288c1.md)

提交智能审校任务

提交智能审核

[GetSmartAuditResult](raw/_short/api-aimiaobi-2023-08-01-getsmartauditresult-7103e3facc2406a5.md)

查询智能审校结果

查询智能审核结果

[ListAuditContentErrorTypes](raw/_short/api-aimiaobi-2023-08-01-listauditcontenterrortyp-ae99f744060b0271.md)

获取审校维度列表

获取审核维度列表

[ExportAuditContentResult](raw/_short/api-aimiaobi-2023-08-01-exportauditcontentresult-5d43ee5b856f6e26.md)

导出智能审校报告

导出智能审核报告

## 妙笔-文档管理

API

标题

API概述

[GenerateExportWordTask](raw/_short/api-aimiaobi-2023-08-01-generateexportwordtask-95985f758c2f1e70.md)

生成导出文档任务

生成内容导出文档任务

[FetchExportWordTask](raw/_short/api-aimiaobi-2023-08-01-fetchexportwordtask-bb378dad8224a696.md)

获取导出文档任务结果

获取异步导出文档任务结果

[CreateGeneratedContent](raw/_short/api-aimiaobi-2023-08-01-creategeneratedcontent-ab73761b0df9b458.md)

保存文档

保存文档：用来保存妙笔中创作的文章，支持富文本。

[DeleteGeneratedContent](raw/_short/api-aimiaobi-2023-08-01-deletegeneratedcontent-1df6fa814ba5cf1f.md)

删除文档

删除文档：用来删除妙笔中创作的文章。

[UpdateGeneratedContent](raw/_short/api-aimiaobi-2023-08-01-updategeneratedcontent-2e8dd063dcd14c64.md)

更新文档

更新文档：用来更新妙笔中创作的文章历史。

[GetGeneratedContent](raw/_short/api-aimiaobi-2023-08-01-getgeneratedcontent-1909d9ce44a08b0b.md)

获取文档

获取文档：用来查询妙笔中创作的文章历史。

[ListGeneratedContents](raw/_short/api-aimiaobi-2023-08-01-listgeneratedcontents-80a3d80c1c5380c1.md)

获取文档列表

获取文档列表：用来查询妙笔中创作的文章历史列表。

[ExportGeneratedContent](raw/_short/api-aimiaobi-2023-08-01-exportgeneratedcontent-16c0c93e55633e9f.md)

导出文档

导出文档：用来导出妙笔中创作的文章历史。

## 妙笔-素材库

API

标题

API概述

[SaveMaterialDocument](raw/_short/api-aimiaobi-2023-08-01-savematerialdocument-2ed89ecadfabe906.md)

保存素材

保存素材：保存素材库中素材。

[DeleteMaterialById](raw/_short/api-aimiaobi-2023-08-01-deletematerialbyid-e1160cc591477f8c.md)

删除素材

删除素材：删除素材库中素材。

[UpdateMaterialDocument](raw/_short/api-aimiaobi-2023-08-01-updatematerialdocument-21039974b5d50370.md)

更新素材

更新素材：更新素材库中素材。

[GetMaterialById](raw/_short/api-aimiaobi-2023-08-01-getmaterialbyid-a41e3f081d3b690f.md)

获取素材

获取素材：获取素材库中素材详细信息。

[ListMaterialDocuments](raw/_short/api-aimiaobi-2023-08-01-listmaterialdocuments-a02fb69f2708de2b.md)

获取素材列表

获取素材列表：获取素材库中素材列表。

## 妙笔-素材库-自定义文本

API

标题

API概述

[GetCustomText](raw/_short/api-aimiaobi-2023-08-01-getcustomtext-f0aa71879c4ce9d6.md)

获取自定义文本

获取自定义文本。

[UpdateCustomText](raw/_short/api-aimiaobi-2023-08-01-updatecustomtext-1b28fa3c526a111e.md)

更新自定义文本

更新自定义文本。

[ListCustomText](raw/_short/api-aimiaobi-2023-08-01-listcustomtext-5c8b74495701eb8c.md)

获取自定义文本列表

获取自定义文本列表。

[SaveCustomText](raw/_short/api-aimiaobi-2023-08-01-savecustomtext-45514e1e2c987f11.md)

保存自定义文本

保存自定义文本。

[DeleteCustomText](raw/_short/api-aimiaobi-2023-08-01-deletecustomtext-df47fb16e3e3db78.md)

删除自定义文本

删除自定义文本。

[DocumentExtraction](raw/_short/api-aimiaobi-2023-08-01-documentextraction-879dcd16a978286b.md)

文档提取

从链接中提取文档内容。

## 妙笔-视频混剪

API

标题

API概述

[GetClipsBuildInResource](raw/_short/api-aimiaobi-2023-08-01-getclipsbuildinresource-14ccf9f66f82db80.md)

获取智能混剪内置资源

获得智能混剪内置资源

[AsyncCreateClipsTimeLine](raw/_short/api-aimiaobi-2023-08-01-asynccreateclipstimeline-14877300ad7c1050.md)

创建剪辑口播时间线

智能剪辑timeline

[AsyncEditTimeline](raw/_short/api-aimiaobi-2023-08-01-asyncedittimeline-d0c7f457f2d113b3.md)

编辑剪辑口播时间线

编辑剪辑任务的timeline

[AsyncUploadVideo](raw/_short/api-aimiaobi-2023-08-01-asyncuploadvideo-d0e99ebcb110c597.md)

异步上传视频剪辑素材

上传剪辑素材

[GetAutoClipsTaskInfo](raw/_short/api-aimiaobi-2023-08-01-getautoclipstaskinfo-50f6650b8f3c65c5.md)

获得剪辑任务信息

获得剪辑任务状态

[AsyncCreateClipsTask](raw/_short/api-aimiaobi-2023-08-01-asynccreateclipstask-12435f3b2efae2e3.md)

创建剪辑任务

生成剪辑视频

[ListAutoClipsTask](raw/_short/api-aimiaobi-2023-08-01-listautoclipstask-91cab23de98380bf.md)

智能混剪任务列表

列出智能混剪任务列表

## 妙策-自定义数据源

API

标题

API概述

[SubmitCustomSourceTopicAnalysis](raw/_short/api-aimiaobi-2023-08-01-submitcustomsourcetopica-1588b67464848f92.md)

提交自定义源话题选题分析任务

从自定义数据源提交选题热点分析

[GetCustomSourceTopicAnalysisTask](raw/_short/api-aimiaobi-2023-08-01-getcustomsourcetopicanal-3f63cd5d0eb9099a.md)

获取自定义源话题分析任务结果

获取自定义数据源-选题视角分析任务结果

[ExportCustomSourceAnalysisTask](raw/_short/api-aimiaobi-2023-08-01-exportcustomsourceanalys-67d4a70d158d53c4.md)

导出自定义源-话题分析任务结果

导出-自定义数据源-选题视角分析任务结果

## 公文库检索

API

标题

API概述

[ListDocumentRetrieve](raw/_short/api-aimiaobi-2023-08-01-listdocumentretrieve-36263f723f8bc86b.md)

公文库检索

根据复杂条件进行政务公文库的检索。

## 妙策-选题热点

API

标题

API概述

[RunTopicSelectionMerge](raw/_short/api-aimiaobi-2023-08-01-runtopicselectionmerge-958f3d415ff349d3.md)

选题热点融合

妙策选题策划聚合

[ListHotNewsWithType](raw/_short/api-aimiaobi-2023-08-01-listhotnewswithtype-5ee22bfbb19de172.md)

获取选题热点列表

获取选题热点列表。

[ListHotSources](raw/_short/api-aimiaobi-2023-08-01-listhotsources-2977aa404a278eec.md)

获取三方热榜源列表

获取所有平台热榜源列表。

[ListHotTopics](raw/_short/api-aimiaobi-2023-08-01-listhottopics-be1206a872d0fc62.md)

获取热点话题列表

获取热点话题列表。

[GetTopicById](raw/_short/api-aimiaobi-2023-08-01-gettopicbyid-e2940091d7b12bdf.md)

获取热点对象

根据ID获取热点事件信息。

[ListHotViewPoints](raw/_short/api-aimiaobi-2023-08-01-listhotviewpoints-4e7aa5f65b1c8418.md)

获取热门视角列表

热门视角列表。

[ListTimedViewAttitude](raw/_short/api-aimiaobi-2023-08-01-listtimedviewattitude-a66456e6ac87d8c2.md)

获取时效性视角列表

时效性视角列表。

[ListFreshViewPoints](raw/_short/api-aimiaobi-2023-08-01-listfreshviewpoints-bb696a988a17c02b.md)

获取新颖视角列表

新颖视角列表。

[ListWebReviewPoints](raw/_short/api-aimiaobi-2023-08-01-listwebreviewpoints-ed2b4a25f4ee1fcd.md)

获取网友视角列表

网友视角列表。

[ListPlanningProposal](raw/_short/api-aimiaobi-2023-08-01-listplanningproposal-1a619658c92c5fbf.md)

获取选题策划列表

获取选题策划列表。

[ExportHotTopicPlanningProposals](raw/_short/api-aimiaobi-2023-08-01-exporthottopicplanningpr-4c72d53eedb8d622.md)

导出选题策划文档

导出选题策划文档，响应为一个可公开访问的URL。一小时后失效。

## 妙策-自定义话题

API

标题

API概述

[DeleteCustomTopicByTopic](raw/_short/api-aimiaobi-2023-08-01-deletecustomtopicbytopic-66df35e4f3a7ae25.md)

删除自定义热点事件

根据热点名称删除自定义热点事件。

[ListTopicViewPointRecommendEventList](raw/_short/api-aimiaobi-2023-08-01-listtopicviewpointrecomm-ebe93014b2db3119.md)

获取热点事件推荐观点列表

获取热点事件推荐观点列表。

[ListTopicRecommendEventList](raw/_short/api-aimiaobi-2023-08-01-listtopicrecommendeventl-571464d0d7dbac01.md)

获取热点推荐事件列表

获取热点推荐事件。

[RunCustomHotTopicAnalysis](raw/_short/api-aimiaobi-2023-08-01-runcustomhottopicanalysi-eee1c995bd24b8a9.md)

自定义热点话题分析

自定义热点话题分析。

[RunCustomHotTopicViewPointAnalysis](raw/_short/api-aimiaobi-2023-08-01-runcustomhottopicviewpoi-b4cbf10013f689d2.md)

自定义选题视角分析

自定义选题视角分析。

[ListCustomViewPoints](raw/_short/api-aimiaobi-2023-08-01-listcustomviewpoints-3e0955032d94655e.md)

获取自定义视角列表

自定义视角列表。

[DeleteCustomTopicViewPointById](raw/_short/api-aimiaobi-2023-08-01-deletecustomtopicviewpoi-8d7a39d5cb24a64f.md)

删除自定义选题视角

根据自定义选题视角ID删除自定义选题视角。

## 妙策-openapi

API

标题

API概述

[SubmitDocClusterTask](raw/_short/api-aimiaobi-2023-08-01-submitdocclustertask-997ad9822426e716.md)

提交内容聚合任务

提交内容聚合任务。

[GetDocClusterTask](raw/_short/api-aimiaobi-2023-08-01-getdocclustertask-4888868ba4ccadaa.md)

获取内容聚合任务结果

获取内容聚合任务结果。

[SubmitTopicSelectionPerspectiveAnalysisTask](raw/_short/api-aimiaobi-2023-08-01-submittopicselectionpers-b46d6db50c29c545.md)

提交选题热点分析任务

提交选题热点分析任务。

[GetTopicSelectionPerspectiveAnalysisTask](raw/_short/api-aimiaobi-2023-08-01-gettopicselectionperspec-b259efa3e95830ee.md)

获取选题视角分析任务结果

获取选题视角分析任务结果。

[SubmitCustomTopicSelectionPerspectiveAnalysisTask](raw/_short/api-aimiaobi-2023-08-01-submitcustomtopicselecti-f43c96bd9199b0b0.md)

提交自定义热点选题视角分析任务

提交自定义热点选题视角分析任务。

[GetCustomTopicSelectionPerspectiveAnalysisTask](raw/_short/api-aimiaobi-2023-08-01-getcustomtopicselectionp-9d02679b5ad8c643.md)

获取自定义选题视角分析任务结果

获取自定义选题视角分析任务结果。

## 妙策-新闻播报

API

标题

API概述

[GetHotTopicBroadcast](raw/_short/api-aimiaobi-2023-08-01-gethottopicbroadcast-d602ac9dc08f3c2e.md)

查询完整播报单（热榜）

查询新闻播报单。

[SubmitCustomHotTopicBroadcastJob](raw/_short/api-aimiaobi-2023-08-01-submitcustomhottopicbroa-696f6e7806399ac7.md)

提交自定义播报单任务

提交自定义播报单任务。

[GetCustomHotTopicBroadcastJob](raw/_short/api-aimiaobi-2023-08-01-getcustomhottopicbroadca-7518d2dff5cab560.md)

获取自定义播报单任务结果

获取自定义播报单任务结果。

## 妙策-企业VOC挖掘

API

标题

API概述

[ExportAnalysisTagDetailByTaskId](raw/_short/api-aimiaobi-2023-08-01-exportanalysistagdetailb-3fd7221595c0d2b0.md)

导出标签挖掘结果

导出企业VOC分析任务明细列表。

[ValidateUploadTemplate](raw/_short/api-aimiaobi-2023-08-01-validateuploadtemplate-e42a1128a9b137bd.md)

校验VOC上传模板

校验企业VOC上传模板。

[SubmitEnterpriseVocAnalysisTask](raw/_short/api-aimiaobi-2023-08-01-submitenterprisevocanaly-d287f2bd7de3d396.md)

提交企业VOC分析任务

提交VOC异步任务。

[ListAnalysisTagDetailByTaskId](raw/_short/api-aimiaobi-2023-08-01-listanalysistagdetailbyt-6d37c9bfa9675c69.md)

根据任务ID获取标签分析明细列表

分页获取企业VOC分析任务明细列表。

[GetEnterpriseVocAnalysisTask](raw/_short/api-aimiaobi-2023-08-01-getenterprisevocanalysis-210c72887adca821.md)

获取企业VOC挖掘任务结果

获取企业VOC分析任务结果。

[GetCategoriesByTaskId](raw/_short/api-aimiaobi-2023-08-01-getcategoriesbytaskid-694c03be06cc2d35.md)

根据任务ID获取分类列表

获取某次标签挖掘结果分类。

## 妙搜-数据源

API

标题

API概述

[CreateDataset](raw/_short/api-aimiaobi-2023-08-01-createdataset-9cf2fa0cba66e0a0.md)

数据源-创建

数据源管理-创建。

[GetDataset](raw/_short/api-aimiaobi-2023-08-01-getdataset-afa789c817f35796.md)

数据源-详情

数据源管理-详情。

[UpdateDataset](raw/_short/api-aimiaobi-2023-08-01-updatedataset-4e703cba19f41d7d.md)

数据源-修改

数据源管理-更新。

[ListDatasets](raw/_short/api-aimiaobi-2023-08-01-listdatasets-2313cd6272804496.md)

数据源-列表

数据源管理-查询。

[DeleteDataset](raw/_short/api-aimiaobi-2023-08-01-deletedataset-1ea96ab7e4a8eed5.md)

数据源-删除

数据源管理-删除。

[AddDatasetDocument](raw/_short/api-aimiaobi-2023-08-01-adddatasetdocument-d634038ff7246468.md)

数据源-添加文档到数据集

添加文档到数据源。

[GetDatasetDocument](raw/_short/api-aimiaobi-2023-08-01-getdatasetdocument-288cb4bd87c944f5.md)

数据源-获取文档详情

获取数据源文档。

[UpdateDatasetDocument](raw/_short/api-aimiaobi-2023-08-01-updatedatasetdocument-18ab686c5f35fc8b.md)

数据源-修改文档

修改数据源文档。

[ListDatasetDocuments](raw/_short/api-aimiaobi-2023-08-01-listdatasetdocuments-e5d9a8f76f09beb3.md)

数据源-文档列表

查询数据源文档列表。

[SearchDatasetDocuments](raw/_short/api-aimiaobi-2023-08-01-searchdatasetdocuments-dc8b0ab1d58aa26c.md)

数据源-搜索文档

搜索数据源文档。

[DeleteDatasetDocument](raw/_short/api-aimiaobi-2023-08-01-deletedatasetdocument-9e9a8e3a4e6a76c3.md)

数据源-删除数据集文档

删除数据源文档。

## 妙搜-智能搜索

API

标题

API概述

[RunSearchGeneration](raw/_short/api-aimiaobi-2023-08-01-runsearchgeneration-008d7da322c502e5.md)

妙搜-智能搜索

AI妙搜-智能搜索生成：对应妙搜首页的搜索生成能力。此接口支持通用搜索和媒资搜索。支持用户问题澄清、多模态知识搜索、多agent生成等能力。 - 通用搜索：可以对数据集中知识进行语义检索，并对搜索结果进行多agent后处理，包括总结生成、摘编、时间线总结等。 - 媒资搜索：应搜尽搜，全文检索，召回更多相关知识，并可进行多agent后处理，包括聚类、新闻抽取等。

[ListSearchTasks](raw/_short/api-aimiaobi-2023-08-01-listsearchtasks-16cba5cd29273c99.md)

查询妙搜搜索生成历史任务列表

查询妙搜搜索生成历史任务列表。

[ListSearchTaskDialogues](raw/_short/api-aimiaobi-2023-08-01-listsearchtaskdialogues-3d8d4525ce15ac3c.md)

查询妙搜搜索生成任务详情列表

查询妙搜搜索生成任务详情列表。

[ListSearchTaskDialogueDatas](raw/_short/api-aimiaobi-2023-08-01-listsearchtaskdialogueda-40b8e7ed38a3461c.md)

查询搜索生成任务对话详情中数据列表

查询搜索生成任务对话详情中数据列表。

[RunSearchSimilarArticles](raw/_short/api-aimiaobi-2023-08-01-runsearchsimilararticles-bcda6f0ee4f20779.md)

妙搜-文搜文

妙搜-文搜文。

## 系统配置-干预配置

API

标题

API概述

[ListInterveneCnt](raw/_short/api-aimiaobi-2023-08-01-listintervenecnt-ddf7e96fccd1cbaf.md)

获得所有干预项的数量

获得干预项目数量列表。

[ListIntervenes](raw/_short/api-aimiaobi-2023-08-01-listintervenes-872b29b2fdaa31b7.md)

列出干预项

获得干预项列表。

[ImportInterveneFile](raw/_short/api-aimiaobi-2023-08-01-importintervenefile-793880acb61b1871.md)

同步导入干预项文件

导入干预文件。

[InsertInterveneGlobalReply](raw/_short/api-aimiaobi-2023-08-01-insertinterveneglobalrep-f0e6cc945d8afcb7.md)

插入干预全局回复项

设置干预全局回复。

[ImportInterveneFileAsync](raw/_short/api-aimiaobi-2023-08-01-importintervenefileasync-e2549c89026ee3b1.md)

异步导入干预项文件

异步导入干预文件。

[GetInterveneTemplateFileUrl](raw/_short/api-aimiaobi-2023-08-01-getintervenetemplatefile-f8fabdf8a7a17100.md)

获得干预导入模版文件地址

获得干预导入模版文件下载地址。

[ClearIntervenes](raw/_short/api-aimiaobi-2023-08-01-clearintervenes-6f2779628a8415e0.md)

清除所有干预项

清除所有干预内容。

[GetInterveneGlobalReply](raw/_short/api-aimiaobi-2023-08-01-getinterveneglobalreply-cb707e0863d06e20.md)

获得干预全局回复内容

获得干预全局回复。

[ListInterveneRules](raw/_short/api-aimiaobi-2023-08-01-listintervenerules-be029c7a7c1dd9a1.md)

列出干预规则

获得干预规则列表。

[ListInterveneImportTasks](raw/_short/api-aimiaobi-2023-08-01-listinterveneimporttasks-6e722c478738a886.md)

列出干预项导入任务

获得导入任务列表。

[InsertInterveneRule](raw/_short/api-aimiaobi-2023-08-01-insertintervenerule-839c4bd6eb0087cb.md)

插入干预规则

插入干预规则。

[GetInterveneRuleDetail](raw/_short/api-aimiaobi-2023-08-01-getinterveneruledetail-852eecc9a22c6a88.md)

获得干预规则的详情

获得干预项规则详情。

[DeleteInterveneRule](raw/_short/api-aimiaobi-2023-08-01-deleteintervenerule-cd1c8557749e6f23.md)

删除干预规则

删除干预规则。

[ExportIntervenes](raw/_short/api-aimiaobi-2023-08-01-exportintervenes-3684439a1506d245.md)

导出干预项内容

导出所有干预内容。

[GetInterveneImportTaskInfo](raw/_short/api-aimiaobi-2023-08-01-getinterveneimporttaskin-7f7c6f974abcd47b.md)

获得干预项目导入任务信息

获得导入任务信息。

## 系统配置-信源管理

API

标题

API概述

[SaveDataSourceOrderConfig](raw/_short/api-aimiaobi-2023-08-01-savedatasourceorderconfi-11a35e9d66ef9dfb.md)

保存信源权重配置

保存用户写作信源配置，通用搜索信源配置的配置信息。

[GetDataSourceOrderConfig](raw/_short/api-aimiaobi-2023-08-01-getdatasourceorderconfig-e2d6ff83ddbb8c7a.md)

获取信源配置权重数据

获取写作信源，通用搜索信源的配置信息。

## 妙读-基础操作类

API

标题

API概述

[GetDocInfo](raw/_short/api-aimiaobi-2023-08-01-getdocinfo-1792f23538478a5f.md)

获取文档信息

妙读获取文档信息。

[GetFileContentLength](raw/_short/api-aimiaobi-2023-08-01-getfilecontentlength-1f70516ba56bd5fd.md)

获取文件长度

妙读获得文档字数。

[UploadBook](raw/_short/api-aimiaobi-2023-08-01-uploadbook-50ae98ab14ff4412.md)

书籍上传

妙读上传书籍。

[UploadDoc](raw/_short/api-aimiaobi-2023-08-01-uploaddoc-fc9dfbba774d5eb3.md)

文档上传

妙读上传文档接口。

[ListDocs](raw/_short/api-aimiaobi-2023-08-01-listdocs-ad0fdf3af98a7522.md)

获取文档列表

妙读获取文档列表。

[DeleteDocs](raw/_short/api-aimiaobi-2023-08-01-deletedocs-cb552930413a9a4f.md)

批量删除文档

妙读删除多个文档。

## 妙读-生成类

API

标题

API概述

[RunMultiDocIntroduction](raw/_short/api-aimiaobi-2023-08-01-runmultidocintroduction-bc4c44fecdb736c9.md)

多文档聚合摘要

针对多篇文章、视频或者URL，生成总分结构的摘要（几篇文章的综合概述、关键要点）。此外支持多种多语言的输入和输出。

[RunDocBrainmap](raw/_short/api-aimiaobi-2023-08-01-rundocbrainmap-c4b3bc56029576ba.md)

全文脑图

针对文章或者书，生成三级脑图，且支持生成多语种，支持控制脑图第二级数量，支持控制叶子节点的字数。

[RunDocIntroduction](raw/_short/api-aimiaobi-2023-08-01-rundocintroduction-b3dff35f3fe6ef41.md)

文档导读

针对一篇文章、视频或者URL，生成文章的导读内容，包含全文总结、关键要点、章节速览（即分段、每段的总结、段落摘要）。此外支持多种多语言的输入和输出。如果用户仅需要对文章进行全文总结，可使用RunDocSummary接口实现，具体请参见[](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-rundocsummary)[https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-rundocsummary](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-rundocsummary)。

[RunDocSummary](raw/_short/api-aimiaobi-2023-08-01-rundocsummary-93fed1072d326095.md)

文档摘要

针对一篇文章、视频或者URL，生成文章的摘要内容，即全文总结。此外支持多种多语言的输入和输出。

[RunDocWashing](raw/_short/api-aimiaobi-2023-08-01-rundocwashing-3dfdb3e3dbc3bf19.md)

改写

把一篇文章改换成指定风格。

[RunBookIntroduction](raw/_short/api-aimiaobi-2023-08-01-runbookintroduction-932b09ce0ede16e1.md)

书籍导读（抽取书籍卖点/书籍摘要）

基于一本书，抽取书籍的内容概要，以及结构化的卖点、热词信息。

[RunBookBrainmap](raw/_short/api-aimiaobi-2023-08-01-runbookbrainmap-495cdb43a5e90c9a.md)

书籍脑图

妙读生成书籍脑图。

[RunCommentGeneration](raw/_short/api-aimiaobi-2023-08-01-runcommentgeneration-aaa80fae0d17b5d7.md)

客户之声预测

针对指定文章，预测用户之声。

## 妙读-抽取类

API

标题

API概述

[RunHotword](raw/_short/api-aimiaobi-2023-08-01-runhotword-750e7a4a7db2266b.md)

抽取关键词

基于指定文章抽取关键词。关键词主要是指在特定领域或行业中具有代表性和识别度的专业术语或概念，它们能够精准地描述和概括某一行业内的核心内容、重要人物、关键事件或技术名词。

## 妙读-问答类

API

标题

API概述

[RunGenerateQuestions](raw/_short/api-aimiaobi-2023-08-01-rungeneratequestions-f55f369366c49818.md)

猜你想问

输入一个query，返回几个相关query。

[RunDocQa](raw/_short/api-aimiaobi-2023-08-01-rundocqa-dd1ebcfbe739f1b9.md)

文档问答（文章问答/多模态文件问答）

文章问答：针对一个自然语言类的query，在指定的文章范围内给出文字答案（有图则会配图），并显示溯源信息。 多模态文件问答：针对一个自然语言类的query，在指定的多模态文件范围内给出文字答案，并带上相关的图片、视频片段或者文字，并显示溯源信息。

## 妙读-其他

API

标题

API概述

[RunDocTranslation](raw/_short/api-aimiaobi-2023-08-01-rundoctranslation-0f3a1feddae9d305.md)

文档翻译

中英文互译接口。

[RunDocSmartCard](raw/_short/api-aimiaobi-2023-08-01-rundocsmartcard-af6c27edb34673b0.md)

文档智能卡片

针对划选的文字或指定chat，自动打标并生成一个卡片笔记。

[RunBookSmartCard](raw/_short/api-aimiaobi-2023-08-01-runbooksmartcard-fffc7fbdcf026ae2.md)

书籍智能卡片

书籍智能卡片接口。

## 深度写作

API

标题

API概述

[SubmitDeepWriteTask](raw/_short/api-aimiaobi-2023-08-01-submitdeepwritetask-d0829118e2b72254.md)

提交深度写作任务

提交深度写作任务。 用户可以根据要研究或分析的主题，填入问题、指令、附件等信息，来提交深度写作任务。该任务会在系统后台调度和执行。

[GetDeepWriteTask](raw/_short/api-aimiaobi-2023-08-01-getdeepwritetask-c6c54c4400f43c73.md)

查询深度写作任务

查询深度写作任务。 主要用来查询指定任务的运行状态。

[GetDeepWriteTaskResult](raw/_short/api-aimiaobi-2023-08-01-getdeepwritetaskresult-c4aa5ce1a27de345.md)

查询深度写作任务的结果

查询深度写作任务的结果。 如果指定任务没有执行完成（排队、执行中、失败、取消等），会返回当前执行状态。如果指定任务已完成，会以URL的形式返回该任务的产出物的压缩包，供用户下载查看。

[CancelDeepWriteTask](raw/_short/api-aimiaobi-2023-08-01-canceldeepwritetask-f1d2e18084b53a79.md)

取消深度写作任务

取消深度写作任务。

[RunDeepWriting](raw/_short/api-aimiaobi-2023-08-01-rundeepwriting-ff148f017931e795.md)

查询深度写作事件

查询深度写作事件。 系统以SSE事件的形式下发任务执行过程中的详细信息。

## PPT生成

API

标题

API概述

[ListEnterprisePptTemplates](raw/_short/api-aimiaobi-2023-08-01-listenterpriseppttemplat-11fb38dc423d3cdc.md)

查询企业专属PPT模板列表

查询企业专属PPT模板列表

[InitiatePptCreationV2](raw/_short/api-aimiaobi-2023-08-01-initiatepptcreationv2-4062493b702b42ec.md)

初始化PPT创建操作

初始化PPT创建操作V2

[ListPptTemplates](raw/_short/api-aimiaobi-2023-08-01-listppttemplates-49fdbe4a26736e15.md)

查询PPT模板列表

查询PPT模板列表

[GetPptTemplateSelector](raw/_short/api-aimiaobi-2023-08-01-getppttemplateselector-1a17a431df471928.md)

查询PPT模板筛选器

查询PPT模板筛选器

[GetPptArtifactExportResult](raw/_short/api-aimiaobi-2023-08-01-getpptartifactexportresu-37a0f7509007c9b8.md)

查询PPT导出任务的结果

查询PPT导出任务的结果

[ExportPptArtifact](raw/_short/api-aimiaobi-2023-08-01-exportpptartifact-3ab2c360f21119c8.md)

导出PPT作品

导出PPT作品

[GetPptArtifact](raw/_short/api-aimiaobi-2023-08-01-getpptartifact-05d70ce3defd7029.md)

查询PPT作品信息

查询PPT作品信息。

[ListPptArtifacts](raw/_short/api-aimiaobi-2023-08-01-listpptartifacts-86ceeb78e8675d61.md)

查询PPT作品列表

查询PPT作品列表

[RunPptOutlineGeneration](raw/_short/api-aimiaobi-2023-08-01-runpptoutlinegeneration-9b5a71de31898ea6.md)

生成PPT大纲内容

生成PPT大纲内容

[InitiatePptCreation](raw/_short/api-aimiaobi-2023-08-01-initiatepptcreation-fb43bbeadaa03b4e.md)

初始化用来创建PPT的会话

重要说明：这个接口涉及到扣费，请注意费用 这个接口包含两个操作： 1. 下发用于初始化“PPT生成”的前端组件的code 2. 进行计费

[GetPptConfig](raw/_short/api-aimiaobi-2023-08-01-getpptconfig-52f53c774cb5add0.md)

获取PPT组件配置

获取PPT组件配置

[BindPptArtifact](raw/_short/api-aimiaobi-2023-08-01-bindpptartifact-4a67476f37b3d367.md)

绑定PPT作品信息

绑定PPT作品信息

[DeletePptArtifact](raw/_short/api-aimiaobi-2023-08-01-deletepptartifact-9553eeced05220b3.md)

删除PPT作品

删除PPT作品

## 标书生成

API

标题

API概述

[AsyncUploadTenderDoc](raw/_short/api-aimiaobi-2023-08-01-asyncuploadtenderdoc-7785704010a85310.md)

招标文档解析

上传招标书文件

[GetBiddingRemainLimitNum](raw/_short/api-aimiaobi-2023-08-01-getbiddingremainlimitnum-e93ae2f1850d3bb1.md)

获得标书写作剩余额度

获得标书功能剩余额度

[GetBiddingDocInfo](raw/_short/api-aimiaobi-2023-08-01-getbiddingdocinfo-25fab3d029976395.md)

获得标书写作结果

获得标书写作结果接口

[EditBiddingDoc](raw/_short/api-aimiaobi-2023-08-01-editbiddingdoc-f0c191cc201bd6cf.md)

编辑标书内容

编辑标书内容接口

[DownloadBiddingDoc](raw/_short/api-aimiaobi-2023-08-01-downloadbiddingdoc-96709e9db4f8d2de.md)

下载标书文件

标书下载接口

[AsyncWritingBiddingDoc](raw/_short/api-aimiaobi-2023-08-01-asyncwritingbiddingdoc-82200a3e98741182.md)

标书写作

标书写作接口

[ListBiddingDoc](raw/_short/api-aimiaobi-2023-08-01-listbiddingdoc-d296bfd7208fb3a9.md)

列出标书写作任务

获得标书写作任务列表

## 其他

API

标题

API概述

[RunVideoScriptGenerate](raw/_short/api-aimiaobi-2023-08-01-runvideoscriptgenerate-184c90127ca3e802.md)

AI生成视频剪辑脚本

AI生成视频剪辑脚本

[GetSmartClipTask](raw/_short/api-aimiaobi-2023-08-01-getsmartcliptask-37342952edacb40e.md)

获取智能剪辑任务结果

查询一键成片剪辑任务。

[SubmitSmartClipTask](raw/_short/api-aimiaobi-2023-08-01-submitsmartcliptask-692691c843acd7e6.md)

提交智能一键成片任务

提交一键成片剪辑任务。

[SaveOrUpdateOssConfig](raw/_short/api-aimiaobi-2023-08-01-saveorupdateossconfig-1e5b39d94b913c47.md)

配置-云存储-参数配置

配置-云存储-参数配置

[CreateDataPermissions](raw/_short/api-aimiaobi-2023-08-01-createdatapermissions-f2c3b1411dc813f2.md)

权限-批量添加

权限-批量添加： - 数据集权限：

[DeleteDataPermissions](raw/_short/api-aimiaobi-2023-08-01-deletedatapermissions-f908866cf49c5d10.md)

权限-删除

权限-批量删除： - 数据集权限

[ListDataPermissions](raw/_short/api-aimiaobi-2023-08-01-listdatapermissions-6a463276f7a9b04b.md)

权限-列表

权限-列表 - 数据集

[GenerateViewPoint](raw/_short/api-aimiaobi-2023-08-01-generateviewpoint-e5f80eb517621506.md)

生成选题视角（已过时，不推荐使用）

生成选题视角。

[GetPptInfo](raw/_short/api-aimiaobi-2023-08-01-getpptinfo-7884360e080c1512.md)

查询PPT任务信息

查询PPT任务信息

SubmitParseDocumentLayoutTask

提交排版任务

提交版本任务

[FetchParseDocumentLayoutTask](raw/_short/api-aimiaobi-2023-08-01-fetchparsedocumentlayout-7a49aed824b7425d.md)

获取排版任务结果

获取排版任务结果

[CancelAuditTask](raw/_short/api-aimiaobi-2023-08-01-cancelaudittask-954a245fd407b59f.md)

取消审核任务

取消审核任务

[QueryAuditTask](raw/_short/api-aimiaobi-2023-08-01-queryaudittask-e02e1f1166a11563.md)

查询审核结果

查询审核结果。

[SubmitAuditTask](raw/_short/api-aimiaobi-2023-08-01-submitaudittask-aa18a0881f0d21ab.md)

提交审核任务

提交审核任务
