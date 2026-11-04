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

[CreateToken](raw/_short/api-aimiaobi-2023-08-01-createtoken-981cf209302c80d5.md)

获取授权token

创建在线推理API的临时Token。

[ListDialogues](raw/_short/api-aimiaobi-2023-08-01-listdialogues-61cfb60e703e2024.md)

生成历史列表

在线推理场景的历史记录。

[ListVersions](raw/_short/api-aimiaobi-2023-08-01-listversions-e13aeb5fb9759776.md)

获取版本信息

获取用户购买的版本信息。

[GetProperties](raw/_short/api-aimiaobi-2023-08-01-getproperties-227db200efb65951.md)

获取配置信息

获取配置信息。包括不限于智能配置的风格，推理相关元数据配置等。

## 通用接口-文件上传下载

API

标题

API概述

[GenerateFileUrlByKey](raw/_short/api-aimiaobi-2023-08-01-generatefileurlbykey-9259e036b36e906e.md)

生成文件URL

生成临时可访问的公开url。

[GenerateUploadConfig](raw/_short/api-aimiaobi-2023-08-01-generateuploadconfig-b7fff5389b2cbb66.md)

生成上传配置

生成文件上传配置。 1. 使用本接口 获取上传的配置 返回 PostUrl （妙笔内部OSS地址）、以及OSS临时鉴权信息：key、OSSAccessKeyId、Signature、policy，还有文件唯一标识：fileKey 2. 客户端 使用 PostUrl、以及临时鉴权信息：key、OSSAccessKeyId、Signature、policy 进行文件的上传 3. 使用 fileKey 调用 后续带有fileKey的接口 （例如：GenerateFileUrlByKey）

## 通用接口-异步任务管理

API

标题

API概述

[SubmitAsyncTask](raw/_short/api-aimiaobi-2023-08-01-submitasynctask-07564d84da416279.md)

提交异步任务

执行系统预定义的异步任务。

[CancelAsyncTask](raw/_short/api-aimiaobi-2023-08-01-cancelasynctask-cff6e72978ed6068.md)

取消异步任务

取消已提交，尚未执行完成的异步任务。

[QueryAsyncTask](raw/_short/api-aimiaobi-2023-08-01-queryasynctask-882ed78b81e346f5.md)

查询异步任务明细

查询已提交异步任务执行明细。

[ListAsyncTasks](raw/_short/api-aimiaobi-2023-08-01-listasynctasks-76b88ff5435ad197.md)

获取异步任务列表

获取异步任务列表。

## 通用接口-通用配置

API

标题

API概述

[CreateGeneralConfig](raw/_short/api-aimiaobi-2023-08-01-creategeneralconfig-86f4dc453b9743a3.md)

通用配置-创建

通用配置-创建

[ListGeneralConfigs](raw/_short/api-aimiaobi-2023-08-01-listgeneralconfigs-630d0961286433c3.md)

通用配置-列表

通用配置-列表

[GetGeneralConfig](raw/_short/api-aimiaobi-2023-08-01-getgeneralconfig-f2ee935b25738158.md)

通用配置-详情

通用配置-查询。

[UpdateGeneralConfig](raw/_short/api-aimiaobi-2023-08-01-updategeneralconfig-045ba8737985ed17.md)

通用配置-修改

通用配置-修改。

[DeleteGeneralConfig](raw/_short/api-aimiaobi-2023-08-01-deletegeneralconfig-fd8c5615923b9ff2.md)

通用配置-删除

通用配置-删除

## 妙笔-创作文章

API

标题

API概述

[RunAiHelperWriting](raw/_short/api-aimiaobi-2023-08-01-runaihelperwriting-9e965c7e9fdbd13a.md)

AI帮写

妙笔：AI助手写作

[RunWritingV2](raw/_short/api-aimiaobi-2023-08-01-runwritingv2-c908f14d478d0459.md)

智能写作

智能写作。

[RunWriting](raw/_short/api-aimiaobi-2023-08-01-runwriting-5e97e8ba3ea2e785.md)

直接写作

直接写作

[RunStepByStepWriting](raw/_short/api-aimiaobi-2023-08-01-runstepbystepwriting-4ff99b2db5069654.md)

分步骤写作

使用大纲+摘编的分步骤的模式进行写作。

[RunTranslateGeneration](raw/_short/api-aimiaobi-2023-08-01-runtranslategeneration-2f8d19c9f2356b75.md)

中英翻译

AI妙笔-创作-中英文翻译。

[RunTextPolishing](raw/_short/api-aimiaobi-2023-08-01-runtextpolishing-d2237dfca46f820a.md)

润色

创作-文本润色。

[RunKeywordsExtractionGeneration](raw/_short/api-aimiaobi-2023-08-01-runkeywordsextractiongen-5ec2ef5a48d0ee19.md)

关键词抽取

AI妙笔-创作-抽取关键词。

[RunContinueContent](raw/_short/api-aimiaobi-2023-08-01-runcontinuecontent-ab23bb7881b05f49.md)

内容续写

内容续写。

[RunWriteToneGeneration](raw/_short/api-aimiaobi-2023-08-01-runwritetonegeneration-4e42ab315d97d32e.md)

文风改写

AI妙笔-创作-文风改写。

[RunTitleGeneration](raw/_short/api-aimiaobi-2023-08-01-runtitlegeneration-a6c45cae66bbca21.md)

标题生成

妙笔：标题生成。

[RunSummaryGenerate](raw/_short/api-aimiaobi-2023-08-01-runsummarygenerate-4842711c2c69d073.md)

摘要生成

内容摘要生成。

[RunExpandContent](raw/_short/api-aimiaobi-2023-08-01-runexpandcontent-9ef545004396e6b9.md)

内容扩写

内容扩写。

[RunAbbreviationContent](raw/_short/api-aimiaobi-2023-08-01-runabbreviationcontent-16382e8e5c8d6a6a.md)

内容缩写

内容缩写。

[SearchNews](raw/_short/api-aimiaobi-2023-08-01-searchnews-2c347c0bb8002e65.md)

信息检索

根据输入检索新闻，目前仅支持互联网搜索。

[RunQuickWriting](raw/_short/api-aimiaobi-2023-08-01-runquickwriting-0e3b4ffec0852cef.md)

快速写作

可直接输入写作指令，进行快速写作。

[ListBuildConfigs](raw/_short/api-aimiaobi-2023-08-01-listbuildconfigs-a6bef156747baddc.md)

获取系统自定义预设

获取系统自定义预设，用于创作文章 -> 直接生成中的内置选项。例如：写作文体、文章篇幅、输出语言、生成文章篇数等选项。

[GenerateImageTask](raw/_short/api-aimiaobi-2023-08-01-generateimagetask-081ae48bd13db383.md)

生成智能配图任务

根据文字异步生成图片。

[FetchImageTask](raw/_short/api-aimiaobi-2023-08-01-fetchimagetask-31305890a48151ef.md)

获取图片任务执行结果

获取图片任务执行结果。

[FeedbackDialogue](raw/_short/api-aimiaobi-2023-08-01-feedbackdialogue-924bdb6696987000.md)

反馈对话

反馈模型生成的内容质量。

## 妙笔-文体仿写

API

标题

API概述

[ListStyleLearningResult](raw/_short/api-aimiaobi-2023-08-01-liststylelearningresult-6c5e1f83a5872222.md)

获取文体学习分析结果列表

获取文体学习分析结果列表。

[RunStyleFeatureAnalysis](raw/_short/api-aimiaobi-2023-08-01-runstylefeatureanalysis-9944b2eede7623b9.md)

内容特点分析

内容特点分析。

[SaveStyleLearningResult](raw/_short/api-aimiaobi-2023-08-01-savestylelearningresult-da5242a6d765f766.md)

保存文体学习分析结果

保存自定义文体。

[DeleteStyleLearningResult](raw/_short/api-aimiaobi-2023-08-01-deletestylelearningresul-6b84f0160aafcb9d.md)

删除自定义文体

删除指定自定义文体。

[GetStyleLearningResult](raw/_short/api-aimiaobi-2023-08-01-getstylelearningresult-5360d3dde2c4474f.md)

获取文体学习分析结果

获取文体学习分析结果。

[ListWritingStyles](raw/_short/api-aimiaobi-2023-08-01-listwritingstyles-00ef4732c20d15a3.md)

获取写作文体列表

获取文体列表。

## 妙笔-视频审校

API

标题

API概述

[SubmitVideoAudit](raw/_short/api-aimiaobi-2023-08-01-submitvideoaudit-b7445c8adb8a8d2a.md)

提交视频审校任务

提交视频审校

[QueryVideoAuditResult](raw/_short/api-aimiaobi-2023-08-01-queryvideoauditresult-3b8b4811530192fa.md)

查询视频审校结果

查询视频审校结果

## 妙笔-文章审校-规则库管理

API

标题

API概述

[SubmitAuditNote](raw/_short/api-aimiaobi-2023-08-01-submitauditnote-4dd821cdf8013394.md)

提交自定义规则库

妙笔为您提供了与公有云“智能审校”模块中相同的上传自定义规则库的功能。由于鉴权限制，用户需要使用自定义规则库文件的 fileKey 作为入参才能顺利调用本接口。该接口在被调用后，会对用户的自定义规则库进行结构化处理，并生成一个 xlsx 格式的结构化解析结果。您可以调用 GetAuditNoteProcessingStatus 接口查询结构化处理状态，也可以调用 DownloadAuditNote 接口获取结构化之后的规则库。接口功能正在迭代中，预计会在未来使用可访问的文件 URL 作为入参。

[ConfirmAndPostProcessAuditNote](raw/_short/api-aimiaobi-2023-08-01-confirmandpostprocessaud-84319a0fa03a0d5f.md)

确认提交规则库用于审核

是否将本次提交自定义规则库得到的解析结果用于审核任务。由于解析结果可能不满足用户需求，因此我们为您提供了该接口用于二次确认。如果对提交的规则库解析满意，则可以直接将本次提交任务的 TaskId 作为入参，系统会对您上传的规则库做后处理，使它可以被用于审核。反之，您可以重新调用 SubmitAuditNote 接口上传修改之后的规则库。

[DownloadAuditNote](raw/_short/api-aimiaobi-2023-08-01-downloadauditnote-02e275cb53c50d03.md)

下载规则库

您可以通过调用该接口下载结构化后的规则库，供您进行进一步处理。该接口同时拥有两个功能：下载未后处理的结构化规则库，或下载当前可用于审核的结构化规则库。具体使用方法，请参考入参说明。

[DeleteAuditNote](raw/_short/api-aimiaobi-2023-08-01-deleteauditnote-7c2265362fc1e2b7.md)

删除规则库

删除用户账户下所有可供审核使用的自定义规则库。删除后无法找回，如果您有对规则库存档的需求，请预先使用 DownloadAuditNote 接口保存需要的规则库。

[GetAuditNotePostProcessingStatus](raw/_short/api-aimiaobi-2023-08-01-getauditnotepostprocessi-0aa9857194b67f71.md)

获取规则库后处理进度

查询规则库后处理的进度。与 ConfirmAndPostProcessAuditNote 接口配合使用，供您查询当前后处理任务的状态。

[GetAuditNoteProcessingStatus](raw/_short/api-aimiaobi-2023-08-01-getauditnoteprocessingst-d90bc8538711a38c.md)

查询规则库上传状态

查询用户上传规则库的处理状态。通过该接口，用户可以查询到当前规则库上传任务的状态，并获取到解析后的规则库文件大小、存储路径等信息。

[GetAvailableAuditNotes](raw/_short/api-aimiaobi-2023-08-01-getavailableauditnotes-ed16fde575f68a31.md)

查询可用规则库

查询用户当前可供审核的规则库信息，只能查询到当前可用于审核的规则库。如果您想看到自定义规则库的具体内容，请使用 DownloadAuditNote 接口。

## 妙笔-文章审校-词库管理

API

标题

API概述

[ListAuditTerms](raw/_short/api-aimiaobi-2023-08-01-listauditterms-1cf5da35bc82f01e.md)

获取自定义词库记录

获取词库列表。

[AddAuditTerms](raw/_short/api-aimiaobi-2023-08-01-addauditterms-c2e7e65e3718af44.md)

添加自定义词库记录

添加审核自定义词库记录。

[EditAuditTerms](raw/_short/api-aimiaobi-2023-08-01-editauditterms-ce093d7e95e2db64.md)

编辑自定义词库记录

编辑审核自定义词库记录

[DeleteAuditTerms](raw/_short/api-aimiaobi-2023-08-01-deleteauditterms-dcec0441ef3384b0.md)

删除指定词库记录

删除指定的词库记录。

[SubmitImportTermsTask](raw/_short/api-aimiaobi-2023-08-01-submitimporttermstask-a5e8e8627cfa2b43.md)

提交导入词库任务

提交导入自定义词库任务

[FetchImportTermsTask](raw/_short/api-aimiaobi-2023-08-01-fetchimporttermstask-12ad325ce266ad04.md)

获取导入词库任务结果

获取导入词库任务结果

[SubmitExportTermsTask](raw/_short/api-aimiaobi-2023-08-01-submitexporttermstask-ded711ad9a7779f9.md)

提交导出词库任务

导出词库任务

[FetchExportTermsTask](raw/_short/api-aimiaobi-2023-08-01-fetchexporttermstask-029fa7b5f8e826dd.md)

获取导出词库任务结果

获取词库导出任务结果

## 妙笔-文章审校-事实性审核

API

标题

API概述

[SubmitFactAuditUrl](raw/_short/api-aimiaobi-2023-08-01-submitfactauditurl-7ea215332c708901.md)

提交事实性审核 URL

妙笔为您提供了新的事实性审核能力，在联网搜索并判断正误的前提下，还支持用户自定义配置搜索来源 URL。

[GetFactAuditUrl](raw/_short/api-aimiaobi-2023-08-01-getfactauditurl-99a00a3a6ceaa9b7.md)

获取事实性审核 URL

获取当前正用于事实性审核的信源 URL。

[DeleteFactAuditUrl](raw/_short/api-aimiaobi-2023-08-01-deletefactauditurl-b6796061bd36bd1d.md)

删除事实性审核 URL

删除指定的用于事实性审核的 URL。

## 妙笔-文章审校

API

标题

API概述

[SubmitSmartAudit](raw/_short/api-aimiaobi-2023-08-01-submitsmartaudit-1b12b5a3618bb1cf.md)

提交智能审校任务

提交智能审核

[GetSmartAuditResult](raw/_short/api-aimiaobi-2023-08-01-getsmartauditresult-d5d51df64c9a539b.md)

查询智能审校结果

查询智能审核结果

[ListAuditContentErrorTypes](raw/_short/api-aimiaobi-2023-08-01-listauditcontenterrortyp-dc8a1e855346739b.md)

获取审校维度列表

获取审核维度列表

[ExportAuditContentResult](raw/_short/api-aimiaobi-2023-08-01-exportauditcontentresult-12ec62cdb9103ee9.md)

导出智能审校报告

导出智能审核报告

## 妙笔-文档管理

API

标题

API概述

[GenerateExportWordTask](raw/_short/api-aimiaobi-2023-08-01-generateexportwordtask-4ded5df79af1a93e.md)

生成导出文档任务

生成内容导出文档任务

[FetchExportWordTask](raw/_short/api-aimiaobi-2023-08-01-fetchexportwordtask-07e6992c68761aec.md)

获取导出文档任务结果

获取异步导出文档任务结果

[CreateGeneratedContent](raw/_short/api-aimiaobi-2023-08-01-creategeneratedcontent-7d826fa65c957a57.md)

保存文档

保存文档：用来保存妙笔中创作的文章，支持富文本。

[DeleteGeneratedContent](raw/_short/api-aimiaobi-2023-08-01-deletegeneratedcontent-34f0916fae2b2468.md)

删除文档

删除文档：用来删除妙笔中创作的文章。

[UpdateGeneratedContent](raw/_short/api-aimiaobi-2023-08-01-updategeneratedcontent-408a790e4f35aba5.md)

更新文档

更新文档：用来更新妙笔中创作的文章历史。

[GetGeneratedContent](raw/_short/api-aimiaobi-2023-08-01-getgeneratedcontent-2b1bcf044ca9bcc2.md)

获取文档

获取文档：用来查询妙笔中创作的文章历史。

[ListGeneratedContents](raw/_short/api-aimiaobi-2023-08-01-listgeneratedcontents-88d7de02c6ba070f.md)

获取文档列表

获取文档列表：用来查询妙笔中创作的文章历史列表。

[ExportGeneratedContent](raw/_short/api-aimiaobi-2023-08-01-exportgeneratedcontent-4f19c9aa87904422.md)

导出文档

导出文档：用来导出妙笔中创作的文章历史。

## 妙笔-素材库

API

标题

API概述

[SaveMaterialDocument](raw/_short/api-aimiaobi-2023-08-01-savematerialdocument-c9fe1c0e21a3e01f.md)

保存素材

保存素材：保存素材库中素材。

[DeleteMaterialById](raw/_short/api-aimiaobi-2023-08-01-deletematerialbyid-ce963e1d0cf3a2f3.md)

删除素材

删除素材：删除素材库中素材。

[UpdateMaterialDocument](raw/_short/api-aimiaobi-2023-08-01-updatematerialdocument-a325206d60bcfb13.md)

更新素材

更新素材：更新素材库中素材。

[GetMaterialById](raw/_short/api-aimiaobi-2023-08-01-getmaterialbyid-22e7878700a6f08e.md)

获取素材

获取素材：获取素材库中素材详细信息。

[ListMaterialDocuments](raw/_short/api-aimiaobi-2023-08-01-listmaterialdocuments-d2cab230af7fc017.md)

获取素材列表

获取素材列表：获取素材库中素材列表。

## 妙笔-素材库-自定义文本

API

标题

API概述

[GetCustomText](raw/_short/api-aimiaobi-2023-08-01-getcustomtext-8157bfb9335a59f8.md)

获取自定义文本

获取自定义文本。

[UpdateCustomText](raw/_short/api-aimiaobi-2023-08-01-updatecustomtext-8c266521c9515813.md)

更新自定义文本

更新自定义文本。

[ListCustomText](raw/_short/api-aimiaobi-2023-08-01-listcustomtext-b5954f5a136d9fb9.md)

获取自定义文本列表

获取自定义文本列表。

[SaveCustomText](raw/_short/api-aimiaobi-2023-08-01-savecustomtext-3e5e75cf554b196d.md)

保存自定义文本

保存自定义文本。

[DeleteCustomText](raw/_short/api-aimiaobi-2023-08-01-deletecustomtext-49ecdbe276c7d043.md)

删除自定义文本

删除自定义文本。

[DocumentExtraction](raw/_short/api-aimiaobi-2023-08-01-documentextraction-aa864d298372391a.md)

文档提取

从链接中提取文档内容。

## 妙笔-视频混剪

API

标题

API概述

[GetClipsBuildInResource](raw/_short/api-aimiaobi-2023-08-01-getclipsbuildinresource-d1ab0d82b9ba11de.md)

获取智能混剪内置资源

获得智能混剪内置资源

[AsyncCreateClipsTimeLine](raw/_short/api-aimiaobi-2023-08-01-asynccreateclipstimeline-2a7e2aa5dfe9623f.md)

创建剪辑口播时间线

智能剪辑timeline

[AsyncEditTimeline](raw/_short/api-aimiaobi-2023-08-01-asyncedittimeline-420f22884628bd96.md)

编辑剪辑口播时间线

编辑剪辑任务的timeline

[AsyncUploadVideo](raw/_short/api-aimiaobi-2023-08-01-asyncuploadvideo-9f3f37ee9ab819ca.md)

异步上传视频剪辑素材

上传剪辑素材

[GetAutoClipsTaskInfo](raw/_short/api-aimiaobi-2023-08-01-getautoclipstaskinfo-a6fc5ba7dfd32888.md)

获得剪辑任务信息

获得剪辑任务状态

[AsyncCreateClipsTask](raw/_short/api-aimiaobi-2023-08-01-asynccreateclipstask-f0727c5910f93f6f.md)

创建剪辑任务

生成剪辑视频

[ListAutoClipsTask](raw/_short/api-aimiaobi-2023-08-01-listautoclipstask-3fc611032bbe6624.md)

智能混剪任务列表

列出智能混剪任务列表

## 妙策-自定义数据源

API

标题

API概述

[SubmitCustomSourceTopicAnalysis](raw/_short/api-aimiaobi-2023-08-01-submitcustomsourcetopica-205245308ab89fe9.md)

提交自定义源话题选题分析任务

从自定义数据源提交选题热点分析

[GetCustomSourceTopicAnalysisTask](raw/_short/api-aimiaobi-2023-08-01-getcustomsourcetopicanal-eb47231ec72f7dad.md)

获取自定义源话题分析任务结果

获取自定义数据源-选题视角分析任务结果

[ExportCustomSourceAnalysisTask](raw/_short/api-aimiaobi-2023-08-01-exportcustomsourceanalys-dde5bfb67e895c5b.md)

导出自定义源-话题分析任务结果

导出-自定义数据源-选题视角分析任务结果

## 公文库检索

API

标题

API概述

[ListDocumentRetrieve](raw/_short/api-aimiaobi-2023-08-01-listdocumentretrieve-4c7d5716896386e5.md)

公文库检索

根据复杂条件进行政务公文库的检索。

## 妙策-选题热点

API

标题

API概述

[RunTopicSelectionMerge](raw/_short/api-aimiaobi-2023-08-01-runtopicselectionmerge-3593266936554a26.md)

选题热点融合

妙策选题策划聚合

[ListHotNewsWithType](raw/_short/api-aimiaobi-2023-08-01-listhotnewswithtype-65411800b9013884.md)

获取选题热点列表

获取选题热点列表。

[ListHotSources](raw/_short/api-aimiaobi-2023-08-01-listhotsources-0d21da74b7aa0b35.md)

获取三方热榜源列表

获取所有平台热榜源列表。

[ListHotTopics](raw/_short/api-aimiaobi-2023-08-01-listhottopics-c4f5349d89ca55f4.md)

获取热点话题列表

获取热点话题列表。

[GetTopicById](raw/_short/api-aimiaobi-2023-08-01-gettopicbyid-cec5b365c1dfb4bf.md)

获取热点对象

根据ID获取热点事件信息。

[ListHotViewPoints](raw/_short/api-aimiaobi-2023-08-01-listhotviewpoints-f5b56834fe3de5e8.md)

获取热门视角列表

热门视角列表。

[ListTimedViewAttitude](raw/_short/api-aimiaobi-2023-08-01-listtimedviewattitude-87c50823d6877c36.md)

获取时效性视角列表

时效性视角列表。

[ListFreshViewPoints](raw/_short/api-aimiaobi-2023-08-01-listfreshviewpoints-5ac76a5b6c3f4436.md)

获取新颖视角列表

新颖视角列表。

[ListWebReviewPoints](raw/_short/api-aimiaobi-2023-08-01-listwebreviewpoints-3943abfd6701e5cd.md)

获取网友视角列表

网友视角列表。

[ListPlanningProposal](raw/_short/api-aimiaobi-2023-08-01-listplanningproposal-7fadcb3c2ad047a5.md)

获取选题策划列表

获取选题策划列表。

[ExportHotTopicPlanningProposals](raw/_short/api-aimiaobi-2023-08-01-exporthottopicplanningpr-87a00d2165ad9bf3.md)

导出选题策划文档

导出选题策划文档，响应为一个可公开访问的URL。一小时后失效。

## 妙策-自定义话题

API

标题

API概述

[DeleteCustomTopicByTopic](raw/_short/api-aimiaobi-2023-08-01-deletecustomtopicbytopic-0b9cd39aeb957af4.md)

删除自定义热点事件

根据热点名称删除自定义热点事件。

[ListTopicViewPointRecommendEventList](raw/_short/api-aimiaobi-2023-08-01-listtopicviewpointrecomm-71836941fef7f644.md)

获取热点事件推荐观点列表

获取热点事件推荐观点列表。

[ListTopicRecommendEventList](raw/_short/api-aimiaobi-2023-08-01-listtopicrecommendeventl-6b169c8697e358f3.md)

获取热点推荐事件列表

获取热点推荐事件。

[RunCustomHotTopicAnalysis](raw/_short/api-aimiaobi-2023-08-01-runcustomhottopicanalysi-8bd7a8fe36026851.md)

自定义热点话题分析

自定义热点话题分析。

[RunCustomHotTopicViewPointAnalysis](raw/_short/api-aimiaobi-2023-08-01-runcustomhottopicviewpoi-ed90e405982fea66.md)

自定义选题视角分析

自定义选题视角分析。

[ListCustomViewPoints](raw/_short/api-aimiaobi-2023-08-01-listcustomviewpoints-2498b20aeb2e3417.md)

获取自定义视角列表

自定义视角列表。

[DeleteCustomTopicViewPointById](raw/_short/api-aimiaobi-2023-08-01-deletecustomtopicviewpoi-1b44cc137249a490.md)

删除自定义选题视角

根据自定义选题视角ID删除自定义选题视角。

## 妙策-openapi

API

标题

API概述

[SubmitDocClusterTask](raw/_short/api-aimiaobi-2023-08-01-submitdocclustertask-54ca4a8668e488bc.md)

提交内容聚合任务

提交内容聚合任务。

[GetDocClusterTask](raw/_short/api-aimiaobi-2023-08-01-getdocclustertask-8b6e25a105e3999f.md)

获取内容聚合任务结果

获取内容聚合任务结果。

[SubmitTopicSelectionPerspectiveAnalysisTask](raw/_short/api-aimiaobi-2023-08-01-submittopicselectionpers-122ab8b66568eb05.md)

提交选题热点分析任务

提交选题热点分析任务。

[GetTopicSelectionPerspectiveAnalysisTask](raw/_short/api-aimiaobi-2023-08-01-gettopicselectionperspec-ef7ec32a61ba11fd.md)

获取选题视角分析任务结果

获取选题视角分析任务结果。

[SubmitCustomTopicSelectionPerspectiveAnalysisTask](raw/_short/api-aimiaobi-2023-08-01-submitcustomtopicselecti-e062bab5658516ce.md)

提交自定义热点选题视角分析任务

提交自定义热点选题视角分析任务。

[GetCustomTopicSelectionPerspectiveAnalysisTask](raw/_short/api-aimiaobi-2023-08-01-getcustomtopicselectionp-9fc38ab6a2f293a9.md)

获取自定义选题视角分析任务结果

获取自定义选题视角分析任务结果。

## 妙策-新闻播报

API

标题

API概述

[GetHotTopicBroadcast](raw/_short/api-aimiaobi-2023-08-01-gethottopicbroadcast-8bd753b9c4dd8b39.md)

查询完整播报单（热榜）

查询新闻播报单。

[SubmitCustomHotTopicBroadcastJob](raw/_short/api-aimiaobi-2023-08-01-submitcustomhottopicbroa-ef63e50230f3647a.md)

提交自定义播报单任务

提交自定义播报单任务。

[GetCustomHotTopicBroadcastJob](raw/_short/api-aimiaobi-2023-08-01-getcustomhottopicbroadca-d81006ae3cdf61d0.md)

获取自定义播报单任务结果

获取自定义播报单任务结果。

## 妙策-企业VOC挖掘

API

标题

API概述

[ExportAnalysisTagDetailByTaskId](raw/_short/api-aimiaobi-2023-08-01-exportanalysistagdetailb-b8456d8de7d22dff.md)

导出标签挖掘结果

导出企业VOC分析任务明细列表。

[ValidateUploadTemplate](raw/_short/api-aimiaobi-2023-08-01-validateuploadtemplate-66737360c2dfa698.md)

校验VOC上传模板

校验企业VOC上传模板。

[SubmitEnterpriseVocAnalysisTask](raw/_short/api-aimiaobi-2023-08-01-submitenterprisevocanaly-3dc1a2175631556e.md)

提交企业VOC分析任务

提交VOC异步任务。

[ListAnalysisTagDetailByTaskId](raw/_short/api-aimiaobi-2023-08-01-listanalysistagdetailbyt-e0dcf88e65760df1.md)

根据任务ID获取标签分析明细列表

分页获取企业VOC分析任务明细列表。

[GetEnterpriseVocAnalysisTask](raw/_short/api-aimiaobi-2023-08-01-getenterprisevocanalysis-007980209765d6cc.md)

获取企业VOC挖掘任务结果

获取企业VOC分析任务结果。

[GetCategoriesByTaskId](raw/_short/api-aimiaobi-2023-08-01-getcategoriesbytaskid-29e8a5a3ec522b51.md)

根据任务ID获取分类列表

获取某次标签挖掘结果分类。

## 妙搜-数据源

API

标题

API概述

[CreateDataset](raw/_short/api-aimiaobi-2023-08-01-createdataset-1f6c6af171e2174b.md)

数据源-创建

数据源管理-创建。

[GetDataset](raw/_short/api-aimiaobi-2023-08-01-getdataset-22149b3781cffd5d.md)

数据源-详情

数据源管理-详情。

[UpdateDataset](raw/_short/api-aimiaobi-2023-08-01-updatedataset-84bb97dbcac8c8eb.md)

数据源-修改

数据源管理-更新。

[ListDatasets](raw/_short/api-aimiaobi-2023-08-01-listdatasets-0f50aee17fb84ace.md)

数据源-列表

数据源管理-查询。

[DeleteDataset](raw/_short/api-aimiaobi-2023-08-01-deletedataset-0ec7388963806422.md)

数据源-删除

数据源管理-删除。

[AddDatasetDocument](raw/_short/api-aimiaobi-2023-08-01-adddatasetdocument-9b751b0f9ec6b91e.md)

数据源-添加文档到数据集

添加文档到数据源。

[GetDatasetDocument](raw/_short/api-aimiaobi-2023-08-01-getdatasetdocument-53e494d1732896c8.md)

数据源-获取文档详情

获取数据源文档。

[UpdateDatasetDocument](raw/_short/api-aimiaobi-2023-08-01-updatedatasetdocument-20a215b97bba17aa.md)

数据源-修改文档

修改数据源文档。

[ListDatasetDocuments](raw/_short/api-aimiaobi-2023-08-01-listdatasetdocuments-ceeb17246b42816b.md)

数据源-文档列表

查询数据源文档列表。

[SearchDatasetDocuments](raw/_short/api-aimiaobi-2023-08-01-searchdatasetdocuments-a4c30deb56fbfd19.md)

数据源-搜索文档

搜索数据源文档。

[DeleteDatasetDocument](raw/_short/api-aimiaobi-2023-08-01-deletedatasetdocument-c2d21ec292e79729.md)

数据源-删除数据集文档

删除数据源文档。

## 妙搜-智能搜索

API

标题

API概述

[RunSearchGeneration](raw/_short/api-aimiaobi-2023-08-01-runsearchgeneration-9f952fe3b300d756.md)

妙搜-智能搜索

AI妙搜-智能搜索生成：对应妙搜首页的搜索生成能力。此接口支持通用搜索和媒资搜索。支持用户问题澄清、多模态知识搜索、多agent生成等能力。 - 通用搜索：可以对数据集中知识进行语义检索，并对搜索结果进行多agent后处理，包括总结生成、摘编、时间线总结等。 - 媒资搜索：应搜尽搜，全文检索，召回更多相关知识，并可进行多agent后处理，包括聚类、新闻抽取等。

[ListSearchTasks](raw/_short/api-aimiaobi-2023-08-01-listsearchtasks-3ff96b450681db57.md)

查询妙搜搜索生成历史任务列表

查询妙搜搜索生成历史任务列表。

[ListSearchTaskDialogues](raw/_short/api-aimiaobi-2023-08-01-listsearchtaskdialogues-f99b815c8643ed2b.md)

查询妙搜搜索生成任务详情列表

查询妙搜搜索生成任务详情列表。

[ListSearchTaskDialogueDatas](raw/_short/api-aimiaobi-2023-08-01-listsearchtaskdialogueda-b9ade5026d8c596c.md)

查询搜索生成任务对话详情中数据列表

查询搜索生成任务对话详情中数据列表。

[RunSearchSimilarArticles](raw/_short/api-aimiaobi-2023-08-01-runsearchsimilararticles-0ba6542b93a5e56d.md)

妙搜-文搜文

妙搜-文搜文。

## 系统配置-干预配置

API

标题

API概述

[ListInterveneCnt](raw/_short/api-aimiaobi-2023-08-01-listintervenecnt-2d93b76026d1ed5f.md)

获得所有干预项的数量

获得干预项目数量列表。

[ListIntervenes](raw/_short/api-aimiaobi-2023-08-01-listintervenes-aeda2abf29c49a64.md)

列出干预项

获得干预项列表。

[ImportInterveneFile](raw/_short/api-aimiaobi-2023-08-01-importintervenefile-a4d65125f35c2f6b.md)

同步导入干预项文件

导入干预文件。

[InsertInterveneGlobalReply](raw/_short/api-aimiaobi-2023-08-01-insertinterveneglobalrep-298cfcee20646204.md)

插入干预全局回复项

设置干预全局回复。

[ImportInterveneFileAsync](raw/_short/api-aimiaobi-2023-08-01-importintervenefileasync-34c43150e55a6512.md)

异步导入干预项文件

异步导入干预文件。

[GetInterveneTemplateFileUrl](raw/_short/api-aimiaobi-2023-08-01-getintervenetemplatefile-fe147f4cb14c0790.md)

获得干预导入模版文件地址

获得干预导入模版文件下载地址。

[ClearIntervenes](raw/_short/api-aimiaobi-2023-08-01-clearintervenes-aa9df2177225ab48.md)

清除所有干预项

清除所有干预内容。

[GetInterveneGlobalReply](raw/_short/api-aimiaobi-2023-08-01-getinterveneglobalreply-cea7cb5dcdfaf5ab.md)

获得干预全局回复内容

获得干预全局回复。

[ListInterveneRules](raw/_short/api-aimiaobi-2023-08-01-listintervenerules-b783831749be3506.md)

列出干预规则

获得干预规则列表。

[ListInterveneImportTasks](raw/_short/api-aimiaobi-2023-08-01-listinterveneimporttasks-e3b269367d9de10e.md)

列出干预项导入任务

获得导入任务列表。

[InsertInterveneRule](raw/_short/api-aimiaobi-2023-08-01-insertintervenerule-5f3a709565c0df27.md)

插入干预规则

插入干预规则。

[GetInterveneRuleDetail](raw/_short/api-aimiaobi-2023-08-01-getinterveneruledetail-2a38c8e60d5f6b9b.md)

获得干预规则的详情

获得干预项规则详情。

[DeleteInterveneRule](raw/_short/api-aimiaobi-2023-08-01-deleteintervenerule-85d7c16bea7a6615.md)

删除干预规则

删除干预规则。

[ExportIntervenes](raw/_short/api-aimiaobi-2023-08-01-exportintervenes-665adb0369561931.md)

导出干预项内容

导出所有干预内容。

[GetInterveneImportTaskInfo](raw/_short/api-aimiaobi-2023-08-01-getinterveneimporttaskin-3a75bb78582f514b.md)

获得干预项目导入任务信息

获得导入任务信息。

## 系统配置-信源管理

API

标题

API概述

[SaveDataSourceOrderConfig](raw/_short/api-aimiaobi-2023-08-01-savedatasourceorderconfi-da7481b7bb79267c.md)

保存信源权重配置

保存用户写作信源配置，通用搜索信源配置的配置信息。

[GetDataSourceOrderConfig](raw/_short/api-aimiaobi-2023-08-01-getdatasourceorderconfig-02dd0b2876015623.md)

获取信源配置权重数据

获取写作信源，通用搜索信源的配置信息。

## 妙读-基础操作类

API

标题

API概述

[GetDocInfo](raw/_short/api-aimiaobi-2023-08-01-getdocinfo-e63b147cceaff4cb.md)

获取文档信息

妙读获取文档信息。

[GetFileContentLength](raw/_short/api-aimiaobi-2023-08-01-getfilecontentlength-7895970d20b8a70d.md)

获取文件长度

妙读获得文档字数。

[UploadBook](raw/_short/api-aimiaobi-2023-08-01-uploadbook-70a69960e8a10bde.md)

书籍上传

妙读上传书籍。

[UploadDoc](raw/_short/api-aimiaobi-2023-08-01-uploaddoc-65330797e2012078.md)

文档上传

妙读上传文档接口。

[ListDocs](raw/_short/api-aimiaobi-2023-08-01-listdocs-726e0c28b9af37d5.md)

获取文档列表

妙读获取文档列表。

[DeleteDocs](raw/_short/api-aimiaobi-2023-08-01-deletedocs-cde7906f2c831321.md)

批量删除文档

妙读删除多个文档。

## 妙读-生成类

API

标题

API概述

[RunMultiDocIntroduction](raw/_short/api-aimiaobi-2023-08-01-runmultidocintroduction-1aa5a5e92698ff45.md)

多文档聚合摘要

针对多篇文章、视频或者URL，生成总分结构的摘要（几篇文章的综合概述、关键要点）。此外支持多种多语言的输入和输出。

[RunDocBrainmap](raw/_short/api-aimiaobi-2023-08-01-rundocbrainmap-dc8e5bb64d710c98.md)

全文脑图

针对文章或者书，生成三级脑图，且支持生成多语种，支持控制脑图第二级数量，支持控制叶子节点的字数。

[RunDocIntroduction](raw/_short/api-aimiaobi-2023-08-01-rundocintroduction-10faef44b834783f.md)

文档导读

针对一篇文章、视频或者URL，生成文章的导读内容，包含全文总结、关键要点、章节速览（即分段、每段的总结、段落摘要）。此外支持多种多语言的输入和输出。如果用户仅需要对文章进行全文总结，可使用RunDocSummary接口实现，具体请参见[](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-rundocsummary)[https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-rundocsummary](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-rundocsummary)。

[RunDocSummary](raw/_short/api-aimiaobi-2023-08-01-rundocsummary-747d3826b5a072aa.md)

文档摘要

针对一篇文章、视频或者URL，生成文章的摘要内容，即全文总结。此外支持多种多语言的输入和输出。

[RunDocWashing](raw/_short/api-aimiaobi-2023-08-01-rundocwashing-c04c4d4024297e9e.md)

改写

把一篇文章改换成指定风格。

[RunBookIntroduction](raw/_short/api-aimiaobi-2023-08-01-runbookintroduction-187585ee56810a9d.md)

书籍导读（抽取书籍卖点/书籍摘要）

基于一本书，抽取书籍的内容概要，以及结构化的卖点、热词信息。

[RunBookBrainmap](raw/_short/api-aimiaobi-2023-08-01-runbookbrainmap-6df4d57ebb0aa70e.md)

书籍脑图

妙读生成书籍脑图。

[RunCommentGeneration](raw/_short/api-aimiaobi-2023-08-01-runcommentgeneration-14291096fd211b29.md)

客户之声预测

针对指定文章，预测用户之声。

## 妙读-抽取类

API

标题

API概述

[RunHotword](raw/_short/api-aimiaobi-2023-08-01-runhotword-027ef76322241544.md)

抽取关键词

基于指定文章抽取关键词。关键词主要是指在特定领域或行业中具有代表性和识别度的专业术语或概念，它们能够精准地描述和概括某一行业内的核心内容、重要人物、关键事件或技术名词。

## 妙读-问答类

API

标题

API概述

[RunGenerateQuestions](raw/_short/api-aimiaobi-2023-08-01-rungeneratequestions-7cf400348adb2544.md)

猜你想问

输入一个query，返回几个相关query。

[RunDocQa](raw/_short/api-aimiaobi-2023-08-01-rundocqa-45115fa76b5c8329.md)

文档问答（文章问答/多模态文件问答）

文章问答：针对一个自然语言类的query，在指定的文章范围内给出文字答案（有图则会配图），并显示溯源信息。 多模态文件问答：针对一个自然语言类的query，在指定的多模态文件范围内给出文字答案，并带上相关的图片、视频片段或者文字，并显示溯源信息。

## 妙读-其他

API

标题

API概述

[RunDocTranslation](raw/_short/api-aimiaobi-2023-08-01-rundoctranslation-31e4461fd87a5ffb.md)

文档翻译

中英文互译接口。

[RunDocSmartCard](raw/_short/api-aimiaobi-2023-08-01-rundocsmartcard-0237f0e317daae40.md)

文档智能卡片

针对划选的文字或指定chat，自动打标并生成一个卡片笔记。

[RunBookSmartCard](raw/_short/api-aimiaobi-2023-08-01-runbooksmartcard-35cbe00c12792058.md)

书籍智能卡片

书籍智能卡片接口。

## 深度写作

API

标题

API概述

[SubmitDeepWriteTask](raw/_short/api-aimiaobi-2023-08-01-submitdeepwritetask-eef9df189279c77b.md)

提交深度写作任务

提交深度写作任务。 用户可以根据要研究或分析的主题，填入问题、指令、附件等信息，来提交深度写作任务。该任务会在系统后台调度和执行。

[GetDeepWriteTask](raw/_short/api-aimiaobi-2023-08-01-getdeepwritetask-2445f319d2d961c8.md)

查询深度写作任务

查询深度写作任务。 主要用来查询指定任务的运行状态。

[GetDeepWriteTaskResult](raw/_short/api-aimiaobi-2023-08-01-getdeepwritetaskresult-a48c5d1c3eb0da71.md)

查询深度写作任务的结果

查询深度写作任务的结果。 如果指定任务没有执行完成（排队、执行中、失败、取消等），会返回当前执行状态。如果指定任务已完成，会以URL的形式返回该任务的产出物的压缩包，供用户下载查看。

[CancelDeepWriteTask](raw/_short/api-aimiaobi-2023-08-01-canceldeepwritetask-6fbb6df1c9f568b7.md)

取消深度写作任务

取消深度写作任务。

[RunDeepWriting](raw/_short/api-aimiaobi-2023-08-01-rundeepwriting-5745e4d86a24743c.md)

查询深度写作事件

查询深度写作事件。 系统以SSE事件的形式下发任务执行过程中的详细信息。

## PPT生成

API

标题

API概述

[ListEnterprisePptTemplates](raw/_short/api-aimiaobi-2023-08-01-listenterpriseppttemplat-0f6af38d590d2725.md)

查询企业专属PPT模板列表

查询企业专属PPT模板列表

[InitiatePptCreationV2](raw/_short/api-aimiaobi-2023-08-01-initiatepptcreationv2-89f1190e9dc82ba3.md)

初始化PPT创建操作

初始化PPT创建操作V2

[ListPptTemplates](raw/_short/api-aimiaobi-2023-08-01-listppttemplates-88c8fe161f29a68f.md)

查询PPT模板列表

查询PPT模板列表

[GetPptTemplateSelector](raw/_short/api-aimiaobi-2023-08-01-getppttemplateselector-5b8157ba87d36c80.md)

查询PPT模板筛选器

查询PPT模板筛选器

[GetPptArtifactExportResult](raw/_short/api-aimiaobi-2023-08-01-getpptartifactexportresu-16475c338abc9043.md)

查询PPT导出任务的结果

查询PPT导出任务的结果

[ExportPptArtifact](raw/_short/api-aimiaobi-2023-08-01-exportpptartifact-fdb00f37b4c36d44.md)

导出PPT作品

导出PPT作品

[GetPptArtifact](raw/_short/api-aimiaobi-2023-08-01-getpptartifact-0f24541bb6f0fb00.md)

查询PPT作品信息

查询PPT作品信息。

[ListPptArtifacts](raw/_short/api-aimiaobi-2023-08-01-listpptartifacts-f05d5c55d265b07f.md)

查询PPT作品列表

查询PPT作品列表

[RunPptOutlineGeneration](raw/_short/api-aimiaobi-2023-08-01-runpptoutlinegeneration-7bb578387e9124a4.md)

生成PPT大纲内容

生成PPT大纲内容

[InitiatePptCreation](raw/_short/api-aimiaobi-2023-08-01-initiatepptcreation-5737c5ef27fa268d.md)

初始化用来创建PPT的会话

重要说明：这个接口涉及到扣费，请注意费用 这个接口包含两个操作： 1. 下发用于初始化“PPT生成”的前端组件的code 2. 进行计费

[GetPptConfig](raw/_short/api-aimiaobi-2023-08-01-getpptconfig-f664f98d565e54f9.md)

获取PPT组件配置

获取PPT组件配置

[BindPptArtifact](raw/_short/api-aimiaobi-2023-08-01-bindpptartifact-9ab377fb301d3f3f.md)

绑定PPT作品信息

绑定PPT作品信息

[DeletePptArtifact](raw/_short/api-aimiaobi-2023-08-01-deletepptartifact-2c9c2c6cefcc45cd.md)

删除PPT作品

删除PPT作品

## 标书生成

API

标题

API概述

[AsyncUploadTenderDoc](raw/_short/api-aimiaobi-2023-08-01-asyncuploadtenderdoc-c44972bda9d77b18.md)

招标文档解析

上传招标书文件

[GetBiddingRemainLimitNum](raw/_short/api-aimiaobi-2023-08-01-getbiddingremainlimitnum-3d1bd6af4806959d.md)

获得标书写作剩余额度

获得标书功能剩余额度

[GetBiddingDocInfo](raw/_short/api-aimiaobi-2023-08-01-getbiddingdocinfo-2fba9aa02ef96557.md)

获得标书写作结果

获得标书写作结果接口

[EditBiddingDoc](raw/_short/api-aimiaobi-2023-08-01-editbiddingdoc-8f9a8217921fd807.md)

编辑标书内容

编辑标书内容接口

[DownloadBiddingDoc](raw/_short/api-aimiaobi-2023-08-01-downloadbiddingdoc-635cd728381c2cbb.md)

下载标书文件

标书下载接口

[AsyncWritingBiddingDoc](raw/_short/api-aimiaobi-2023-08-01-asyncwritingbiddingdoc-2448bdba888d3b83.md)

标书写作

标书写作接口

[ListBiddingDoc](raw/_short/api-aimiaobi-2023-08-01-listbiddingdoc-ca714519e77804be.md)

列出标书写作任务

获得标书写作任务列表

## 其他

API

标题

API概述

[RunVideoScriptGenerate](raw/_short/api-aimiaobi-2023-08-01-runvideoscriptgenerate-3bc899c41f140c1f.md)

AI生成视频剪辑脚本

AI生成视频剪辑脚本

[GetSmartClipTask](raw/_short/api-aimiaobi-2023-08-01-getsmartcliptask-c9166cfc941760b9.md)

获取智能剪辑任务结果

查询一键成片剪辑任务。

[SubmitSmartClipTask](raw/_short/api-aimiaobi-2023-08-01-submitsmartcliptask-f428eaea1e0c51a0.md)

提交智能一键成片任务

提交一键成片剪辑任务。

[SaveOrUpdateOssConfig](raw/_short/api-aimiaobi-2023-08-01-saveorupdateossconfig-90d3b00a842fbe4f.md)

配置-云存储-参数配置

配置-云存储-参数配置

[CreateDataPermissions](raw/_short/api-aimiaobi-2023-08-01-createdatapermissions-92bb8122d208ea90.md)

权限-批量添加

权限-批量添加： - 数据集权限：

[DeleteDataPermissions](raw/_short/api-aimiaobi-2023-08-01-deletedatapermissions-ea275f3378d861c1.md)

权限-删除

权限-批量删除： - 数据集权限

[ListDataPermissions](raw/_short/api-aimiaobi-2023-08-01-listdatapermissions-221440708fc649f4.md)

权限-列表

权限-列表 - 数据集

[GenerateViewPoint](raw/_short/api-aimiaobi-2023-08-01-generateviewpoint-2bad7e470e8c9975.md)

生成选题视角（已过时，不推荐使用）

生成选题视角。

[GetPptInfo](raw/_short/api-aimiaobi-2023-08-01-getpptinfo-204afb4585337757.md)

查询PPT任务信息

查询PPT任务信息

SubmitParseDocumentLayoutTask

提交排版任务

提交版本任务

[FetchParseDocumentLayoutTask](raw/_short/api-aimiaobi-2023-08-01-fetchparsedocumentlayout-4560135ea6cda4ce.md)

获取排版任务结果

获取排版任务结果

[CancelAuditTask](raw/_short/api-aimiaobi-2023-08-01-cancelaudittask-2c8ab9606eeda99c.md)

取消审核任务

取消审核任务

[QueryAuditTask](raw/_short/api-aimiaobi-2023-08-01-queryaudittask-4649ac6969ac59fc.md)

查询审核结果

查询审核结果。

[SubmitAuditTask](raw/_short/api-aimiaobi-2023-08-01-submitaudittask-c89e9e79c8c2943f.md)

提交审核任务

提交审核任务
