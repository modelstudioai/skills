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

[CreateToken](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-universal-interface/api-aimiaobi-2023-08-01-createtoken.md)

获取授权token

创建在线推理API的临时Token。

[ListDialogues](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-universal-interface/api-aimiaobi-2023-08-01-listdialogues.md)

生成历史列表

在线推理场景的历史记录。

[ListVersions](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-universal-interface/api-aimiaobi-2023-08-01-listversions.md)

获取版本信息

获取用户购买的版本信息。

[GetProperties](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-universal-interface/api-aimiaobi-2023-08-01-getproperties.md)

获取配置信息

获取配置信息。包括不限于智能配置的风格，推理相关元数据配置等。

## 通用接口-文件上传下载

API

标题

API概述

[GenerateFileUrlByKey](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-common-interface-file-upload-and-download/api-aimiaobi-2023-08-01-generatefileurlbykey.md)

生成文件URL

生成临时可访问的公开url。

[GenerateUploadConfig](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-common-interface-file-upload-and-download/api-aimiaobi-2023-08-01-generateuploadconfig.md)

生成上传配置

生成文件上传配置。 1. 使用本接口 获取上传的配置 返回 PostUrl （妙笔内部OSS地址）、以及OSS临时鉴权信息：key、OSSAccessKeyId、Signature、policy，还有文件唯一标识：fileKey 2. 客户端 使用 PostUrl、以及临时鉴权信息：key、OSSAccessKeyId、Signature、policy 进行文件的上传 3. 使用 fileKey 调用 后续带有fileKey的接口 （例如：GenerateFileUrlByKey）

## 通用接口-异步任务管理

API

标题

API概述

[SubmitAsyncTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-common-interface-asynchronous-task-management/api-aimiaobi-2023-08-01-submitasynctask.md)

提交异步任务

执行系统预定义的异步任务。

[CancelAsyncTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-common-interface-asynchronous-task-management/api-aimiaobi-2023-08-01-cancelasynctask.md)

取消异步任务

取消已提交，尚未执行完成的异步任务。

[QueryAsyncTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-common-interface-asynchronous-task-management/api-aimiaobi-2023-08-01-queryasynctask.md)

查询异步任务明细

查询已提交异步任务执行明细。

[ListAsyncTasks](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-common-interface-asynchronous-task-management/api-aimiaobi-2023-08-01-listasynctasks.md)

获取异步任务列表

获取异步任务列表。

## 通用接口-通用配置

API

标题

API概述

[CreateGeneralConfig](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-common-interface-common-configuration/api-aimiaobi-2023-08-01-creategeneralconfig.md)

通用配置-创建

通用配置-创建

[ListGeneralConfigs](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-common-interface-common-configuration/api-aimiaobi-2023-08-01-listgeneralconfigs.md)

通用配置-列表

通用配置-列表

[GetGeneralConfig](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-common-interface-common-configuration/api-aimiaobi-2023-08-01-getgeneralconfig.md)

通用配置-详情

通用配置-查询。

[UpdateGeneralConfig](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-common-interface-common-configuration/api-aimiaobi-2023-08-01-updategeneralconfig.md)

通用配置-修改

通用配置-修改。

[DeleteGeneralConfig](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-common-interface-common-configuration/api-aimiaobi-2023-08-01-deletegeneralconfig.md)

通用配置-删除

通用配置-删除

## 妙笔-创作文章

API

标题

API概述

[RunAiHelperWriting](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-creative-articles/api-aimiaobi-2023-08-01-runaihelperwriting.md)

AI帮写

妙笔：AI助手写作

[RunWritingV2](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-creative-articles/api-aimiaobi-2023-08-01-runwritingv2.md)

智能写作

智能写作。

[RunWriting](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-creative-articles/api-aimiaobi-2023-08-01-runwriting.md)

直接写作

直接写作

[RunStepByStepWriting](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-creative-articles/api-aimiaobi-2023-08-01-runstepbystepwriting.md)

分步骤写作

使用大纲+摘编的分步骤的模式进行写作。

[RunTranslateGeneration](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-creative-articles/api-aimiaobi-2023-08-01-runtranslategeneration.md)

中英翻译

AI妙笔-创作-中英文翻译。

[RunTextPolishing](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-creative-articles/api-aimiaobi-2023-08-01-runtextpolishing.md)

润色

创作-文本润色。

[RunKeywordsExtractionGeneration](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-creative-articles/api-aimiaobi-2023-08-01-runkeywordsextractiongeneration.md)

关键词抽取

AI妙笔-创作-抽取关键词。

[RunContinueContent](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-creative-articles/api-aimiaobi-2023-08-01-runcontinuecontent.md)

内容续写

内容续写。

[RunWriteToneGeneration](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-creative-articles/api-aimiaobi-2023-08-01-runwritetonegeneration.md)

文风改写

AI妙笔-创作-文风改写。

[RunTitleGeneration](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-creative-articles/api-aimiaobi-2023-08-01-runtitlegeneration.md)

标题生成

妙笔：标题生成。

[RunSummaryGenerate](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-creative-articles/api-aimiaobi-2023-08-01-runsummarygenerate.md)

摘要生成

内容摘要生成。

[RunExpandContent](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-creative-articles/api-aimiaobi-2023-08-01-runexpandcontent.md)

内容扩写

内容扩写。

[RunAbbreviationContent](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-creative-articles/api-aimiaobi-2023-08-01-runabbreviationcontent.md)

内容缩写

内容缩写。

[SearchNews](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-creative-articles/api-aimiaobi-2023-08-01-searchnews.md)

信息检索

根据输入检索新闻，目前仅支持互联网搜索。

[RunQuickWriting](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-creative-articles/api-aimiaobi-2023-08-01-runquickwriting.md)

快速写作

可直接输入写作指令，进行快速写作。

[ListBuildConfigs](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-creative-articles/api-aimiaobi-2023-08-01-listbuildconfigs.md)

获取系统自定义预设

获取系统自定义预设，用于创作文章 -> 直接生成中的内置选项。例如：写作文体、文章篇幅、输出语言、生成文章篇数等选项。

[GenerateImageTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-creative-articles/api-aimiaobi-2023-08-01-generateimagetask.md)

生成智能配图任务

根据文字异步生成图片。

[FetchImageTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-creative-articles/api-aimiaobi-2023-08-01-fetchimagetask.md)

获取图片任务执行结果

获取图片任务执行结果。

[FeedbackDialogue](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-creative-articles/api-aimiaobi-2023-08-01-feedbackdialogue.md)

反馈对话

反馈模型生成的内容质量。

## 妙笔-文体仿写

API

标题

API概述

[ListStyleLearningResult](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-style-imitation-writing/api-aimiaobi-2023-08-01-liststylelearningresult.md)

获取文体学习分析结果列表

获取文体学习分析结果列表。

[RunStyleFeatureAnalysis](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-style-imitation-writing/api-aimiaobi-2023-08-01-runstylefeatureanalysis.md)

内容特点分析

内容特点分析。

[SaveStyleLearningResult](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-style-imitation-writing/api-aimiaobi-2023-08-01-savestylelearningresult.md)

保存文体学习分析结果

保存自定义文体。

[DeleteStyleLearningResult](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-style-imitation-writing/api-aimiaobi-2023-08-01-deletestylelearningresult.md)

删除自定义文体

删除指定自定义文体。

[GetStyleLearningResult](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-style-imitation-writing/api-aimiaobi-2023-08-01-getstylelearningresult.md)

获取文体学习分析结果

获取文体学习分析结果。

[ListWritingStyles](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-style-imitation-writing/api-aimiaobi-2023-08-01-listwritingstyles.md)

获取写作文体列表

获取文体列表。

## 妙笔-视频审校

API

标题

API概述

[SubmitVideoAudit](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-video-review/api-aimiaobi-2023-08-01-submitvideoaudit.md)

提交视频审校任务

提交视频审校

[QueryVideoAuditResult](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-video-review/api-aimiaobi-2023-08-01-queryvideoauditresult.md)

查询视频审校结果

查询视频审校结果

## 妙笔-文章审校-规则库管理

API

标题

API概述

[SubmitAuditNote](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaobi-article-proofreading-rule-library-management/api-aimiaobi-2023-08-01-submitauditnote.md)

提交自定义规则库

妙笔为您提供了与公有云“智能审校”模块中相同的上传自定义规则库的功能。由于鉴权限制，用户需要使用自定义规则库文件的 fileKey 作为入参才能顺利调用本接口。该接口在被调用后，会对用户的自定义规则库进行结构化处理，并生成一个 xlsx 格式的结构化解析结果。您可以调用 GetAuditNoteProcessingStatus 接口查询结构化处理状态，也可以调用 DownloadAuditNote 接口获取结构化之后的规则库。接口功能正在迭代中，预计会在未来使用可访问的文件 URL 作为入参。

[ConfirmAndPostProcessAuditNote](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaobi-article-proofreading-rule-library-management/api-aimiaobi-2023-08-01-confirmandpostprocessauditnote.md)

确认提交规则库用于审核

是否将本次提交自定义规则库得到的解析结果用于审核任务。由于解析结果可能不满足用户需求，因此我们为您提供了该接口用于二次确认。如果对提交的规则库解析满意，则可以直接将本次提交任务的 TaskId 作为入参，系统会对您上传的规则库做后处理，使它可以被用于审核。反之，您可以重新调用 SubmitAuditNote 接口上传修改之后的规则库。

[DownloadAuditNote](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaobi-article-proofreading-rule-library-management/api-aimiaobi-2023-08-01-downloadauditnote.md)

下载规则库

您可以通过调用该接口下载结构化后的规则库，供您进行进一步处理。该接口同时拥有两个功能：下载未后处理的结构化规则库，或下载当前可用于审核的结构化规则库。具体使用方法，请参考入参说明。

[DeleteAuditNote](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaobi-article-proofreading-rule-library-management/api-aimiaobi-2023-08-01-deleteauditnote.md)

删除规则库

删除用户账户下所有可供审核使用的自定义规则库。删除后无法找回，如果您有对规则库存档的需求，请预先使用 DownloadAuditNote 接口保存需要的规则库。

[GetAuditNotePostProcessingStatus](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaobi-article-proofreading-rule-library-management/api-aimiaobi-2023-08-01-getauditnotepostprocessingstatus.md)

获取规则库后处理进度

查询规则库后处理的进度。与 ConfirmAndPostProcessAuditNote 接口配合使用，供您查询当前后处理任务的状态。

[GetAuditNoteProcessingStatus](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaobi-article-proofreading-rule-library-management/api-aimiaobi-2023-08-01-getauditnoteprocessingstatus.md)

查询规则库上传状态

查询用户上传规则库的处理状态。通过该接口，用户可以查询到当前规则库上传任务的状态，并获取到解析后的规则库文件大小、存储路径等信息。

[GetAvailableAuditNotes](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaobi-article-proofreading-rule-library-management/api-aimiaobi-2023-08-01-getavailableauditnotes.md)

查询可用规则库

查询用户当前可供审核的规则库信息，只能查询到当前可用于审核的规则库。如果您想看到自定义规则库的具体内容，请使用 DownloadAuditNote 接口。

## 妙笔-文章审校-词库管理

API

标题

API概述

[ListAuditTerms](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaobi-article-review-thesaurus-management/api-aimiaobi-2023-08-01-listauditterms.md)

获取自定义词库记录

获取词库列表。

[AddAuditTerms](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaobi-article-review-thesaurus-management/api-aimiaobi-2023-08-01-addauditterms.md)

添加自定义词库记录

添加审核自定义词库记录。

[EditAuditTerms](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaobi-article-review-thesaurus-management/api-aimiaobi-2023-08-01-editauditterms.md)

编辑自定义词库记录

编辑审核自定义词库记录

[DeleteAuditTerms](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaobi-article-review-thesaurus-management/api-aimiaobi-2023-08-01-deleteauditterms.md)

删除指定词库记录

删除指定的词库记录。

[SubmitImportTermsTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaobi-article-review-thesaurus-management/api-aimiaobi-2023-08-01-submitimporttermstask.md)

提交导入词库任务

提交导入自定义词库任务

[FetchImportTermsTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaobi-article-review-thesaurus-management/api-aimiaobi-2023-08-01-fetchimporttermstask.md)

获取导入词库任务结果

获取导入词库任务结果

[SubmitExportTermsTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaobi-article-review-thesaurus-management/api-aimiaobi-2023-08-01-submitexporttermstask.md)

提交导出词库任务

导出词库任务

[FetchExportTermsTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaobi-article-review-thesaurus-management/api-aimiaobi-2023-08-01-fetchexporttermstask.md)

获取导出词库任务结果

获取词库导出任务结果

## 妙笔-文章审校-事实性审核

API

标题

API概述

[SubmitFactAuditUrl](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaobi-article-review-factual-review/api-aimiaobi-2023-08-01-submitfactauditurl.md)

提交事实性审核 URL

妙笔为您提供了新的事实性审核能力，在联网搜索并判断正误的前提下，还支持用户自定义配置搜索来源 URL。

[GetFactAuditUrl](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaobi-article-review-factual-review/api-aimiaobi-2023-08-01-getfactauditurl.md)

获取事实性审核 URL

获取当前正用于事实性审核的信源 URL。

[DeleteFactAuditUrl](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaobi-article-review-factual-review/api-aimiaobi-2023-08-01-deletefactauditurl.md)

删除事实性审核 URL

删除指定的用于事实性审核的 URL。

## 妙笔-文章审校

API

标题

API概述

[SubmitSmartAudit](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-article-reviser/api-aimiaobi-2023-08-01-submitsmartaudit.md)

提交智能审校任务

提交智能审核

[GetSmartAuditResult](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-article-reviser/api-aimiaobi-2023-08-01-getsmartauditresult.md)

查询智能审校结果

查询智能审核结果

[ListAuditContentErrorTypes](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-article-reviser/api-aimiaobi-2023-08-01-listauditcontenterrortypes.md)

获取审校维度列表

获取审核维度列表

[ExportAuditContentResult](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-article-reviser/api-aimiaobi-2023-08-01-exportauditcontentresult.md)

导出智能审校报告

导出智能审核报告

## 妙笔-文档管理

API

标题

API概述

[GenerateExportWordTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-document-management/api-aimiaobi-2023-08-01-generateexportwordtask.md)

生成导出文档任务

生成内容导出文档任务

[FetchExportWordTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-document-management/api-aimiaobi-2023-08-01-fetchexportwordtask.md)

获取导出文档任务结果

获取异步导出文档任务结果

[CreateGeneratedContent](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-document-management/api-aimiaobi-2023-08-01-creategeneratedcontent.md)

保存文档

保存文档：用来保存妙笔中创作的文章，支持富文本。

[DeleteGeneratedContent](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-document-management/api-aimiaobi-2023-08-01-deletegeneratedcontent.md)

删除文档

删除文档：用来删除妙笔中创作的文章。

[UpdateGeneratedContent](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-document-management/api-aimiaobi-2023-08-01-updategeneratedcontent.md)

更新文档

更新文档：用来更新妙笔中创作的文章历史。

[GetGeneratedContent](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-document-management/api-aimiaobi-2023-08-01-getgeneratedcontent.md)

获取文档

获取文档：用来查询妙笔中创作的文章历史。

[ListGeneratedContents](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-document-management/api-aimiaobi-2023-08-01-listgeneratedcontents.md)

获取文档列表

获取文档列表：用来查询妙笔中创作的文章历史列表。

[ExportGeneratedContent](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-document-management/api-aimiaobi-2023-08-01-exportgeneratedcontent.md)

导出文档

导出文档：用来导出妙笔中创作的文章历史。

## 妙笔-素材库

API

标题

API概述

[SaveMaterialDocument](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-material-library/api-aimiaobi-2023-08-01-savematerialdocument.md)

保存素材

保存素材：保存素材库中素材。

[DeleteMaterialById](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-material-library/api-aimiaobi-2023-08-01-deletematerialbyid.md)

删除素材

删除素材：删除素材库中素材。

[UpdateMaterialDocument](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-material-library/api-aimiaobi-2023-08-01-updatematerialdocument.md)

更新素材

更新素材：更新素材库中素材。

[GetMaterialById](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-material-library/api-aimiaobi-2023-08-01-getmaterialbyid.md)

获取素材

获取素材：获取素材库中素材详细信息。

[ListMaterialDocuments](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-material-library/api-aimiaobi-2023-08-01-listmaterialdocuments.md)

获取素材列表

获取素材列表：获取素材库中素材列表。

## 妙笔-素材库-自定义文本

API

标题

API概述

[GetCustomText](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-material-library-custom-text/api-aimiaobi-2023-08-01-getcustomtext.md)

获取自定义文本

获取自定义文本。

[UpdateCustomText](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-material-library-custom-text/api-aimiaobi-2023-08-01-updatecustomtext.md)

更新自定义文本

更新自定义文本。

[ListCustomText](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-material-library-custom-text/api-aimiaobi-2023-08-01-listcustomtext.md)

获取自定义文本列表

获取自定义文本列表。

[SaveCustomText](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-material-library-custom-text/api-aimiaobi-2023-08-01-savecustomtext.md)

保存自定义文本

保存自定义文本。

[DeleteCustomText](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-material-library-custom-text/api-aimiaobi-2023-08-01-deletecustomtext.md)

删除自定义文本

删除自定义文本。

[DocumentExtraction](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-material-library-custom-text/api-aimiaobi-2023-08-01-documentextraction.md)

文档提取

从链接中提取文档内容。

## 妙笔-视频混剪

API

标题

API概述

[GetClipsBuildInResource](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-video-mixed-cut/api-aimiaobi-2023-08-01-getclipsbuildinresource.md)

获取智能混剪内置资源

获得智能混剪内置资源

[AsyncCreateClipsTimeLine](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-video-mixed-cut/api-aimiaobi-2023-08-01-asynccreateclipstimeline.md)

创建剪辑口播时间线

智能剪辑timeline

[AsyncEditTimeline](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-video-mixed-cut/api-aimiaobi-2023-08-01-asyncedittimeline.md)

编辑剪辑口播时间线

编辑剪辑任务的timeline

[AsyncUploadVideo](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-video-mixed-cut/api-aimiaobi-2023-08-01-asyncuploadvideo.md)

异步上传视频剪辑素材

上传剪辑素材

[GetAutoClipsTaskInfo](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-video-mixed-cut/api-aimiaobi-2023-08-01-getautoclipstaskinfo.md)

获得剪辑任务信息

获得剪辑任务状态

[AsyncCreateClipsTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-video-mixed-cut/api-aimiaobi-2023-08-01-asynccreateclipstask.md)

创建剪辑任务

生成剪辑视频

[ListAutoClipsTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-video-mixed-cut/api-aimiaobi-2023-08-01-listautoclipstask.md)

智能混剪任务列表

列出智能混剪任务列表

## 妙策-自定义数据源

API

标题

API概述

[SubmitCustomSourceTopicAnalysis](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-tips-custom-data-source/api-aimiaobi-2023-08-01-submitcustomsourcetopicanalysis.md)

提交自定义源话题选题分析任务

从自定义数据源提交选题热点分析

[GetCustomSourceTopicAnalysisTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-tips-custom-data-source/api-aimiaobi-2023-08-01-getcustomsourcetopicanalysistask.md)

获取自定义源话题分析任务结果

获取自定义数据源-选题视角分析任务结果

[ExportCustomSourceAnalysisTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-tips-custom-data-source/api-aimiaobi-2023-08-01-exportcustomsourceanalysistask.md)

导出自定义源-话题分析任务结果

导出-自定义数据源-选题视角分析任务结果

## 公文库检索

API

标题

API概述

[ListDocumentRetrieve](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-public-library-retrieval/api-aimiaobi-2023-08-01-listdocumentretrieve.md)

公文库检索

根据复杂条件进行政务公文库的检索。

## 妙策-选题热点

API

标题

API概述

[RunTopicSelectionMerge](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaozi-hot-topics/api-aimiaobi-2023-08-01-runtopicselectionmerge.md)

选题热点融合

妙策选题策划聚合

[ListHotNewsWithType](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaozi-hot-topics/api-aimiaobi-2023-08-01-listhotnewswithtype.md)

获取选题热点列表

获取选题热点列表。

[ListHotSources](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaozi-hot-topics/api-aimiaobi-2023-08-01-listhotsources.md)

获取三方热榜源列表

获取所有平台热榜源列表。

[ListHotTopics](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaozi-hot-topics/api-aimiaobi-2023-08-01-listhottopics.md)

获取热点话题列表

获取热点话题列表。

[GetTopicById](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaozi-hot-topics/api-aimiaobi-2023-08-01-gettopicbyid.md)

获取热点对象

根据ID获取热点事件信息。

[ListHotViewPoints](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaozi-hot-topics/api-aimiaobi-2023-08-01-listhotviewpoints.md)

获取热门视角列表

热门视角列表。

[ListTimedViewAttitude](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaozi-hot-topics/api-aimiaobi-2023-08-01-listtimedviewattitude.md)

获取时效性视角列表

时效性视角列表。

[ListFreshViewPoints](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaozi-hot-topics/api-aimiaobi-2023-08-01-listfreshviewpoints.md)

获取新颖视角列表

新颖视角列表。

[ListWebReviewPoints](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaozi-hot-topics/api-aimiaobi-2023-08-01-listwebreviewpoints.md)

获取网友视角列表

网友视角列表。

[ListPlanningProposal](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaozi-hot-topics/api-aimiaobi-2023-08-01-listplanningproposal.md)

获取选题策划列表

获取选题策划列表。

[ExportHotTopicPlanningProposals](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaozi-hot-topics/api-aimiaobi-2023-08-01-exporthottopicplanningproposals.md)

导出选题策划文档

导出选题策划文档，响应为一个可公开访问的URL。一小时后失效。

## 妙策-自定义话题

API

标题

API概述

[DeleteCustomTopicByTopic](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-policy-custom-topic/api-aimiaobi-2023-08-01-deletecustomtopicbytopic.md)

删除自定义热点事件

根据热点名称删除自定义热点事件。

[ListTopicViewPointRecommendEventList](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-policy-custom-topic/api-aimiaobi-2023-08-01-listtopicviewpointrecommendeventlist.md)

获取热点事件推荐观点列表

获取热点事件推荐观点列表。

[ListTopicRecommendEventList](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-policy-custom-topic/api-aimiaobi-2023-08-01-listtopicrecommendeventlist.md)

获取热点推荐事件列表

获取热点推荐事件。

[RunCustomHotTopicAnalysis](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-policy-custom-topic/api-aimiaobi-2023-08-01-runcustomhottopicanalysis.md)

自定义热点话题分析

自定义热点话题分析。

[RunCustomHotTopicViewPointAnalysis](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-policy-custom-topic/api-aimiaobi-2023-08-01-runcustomhottopicviewpointanalysis.md)

自定义选题视角分析

自定义选题视角分析。

[ListCustomViewPoints](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-policy-custom-topic/api-aimiaobi-2023-08-01-listcustomviewpoints.md)

获取自定义视角列表

自定义视角列表。

[DeleteCustomTopicViewPointById](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-policy-custom-topic/api-aimiaobi-2023-08-01-deletecustomtopicviewpointbyid.md)

删除自定义选题视角

根据自定义选题视角ID删除自定义选题视角。

## 妙策-openapi

API

标题

API概述

[SubmitDocClusterTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-tips-openapi/api-aimiaobi-2023-08-01-submitdocclustertask.md)

提交内容聚合任务

提交内容聚合任务。

[GetDocClusterTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-tips-openapi/api-aimiaobi-2023-08-01-getdocclustertask.md)

获取内容聚合任务结果

获取内容聚合任务结果。

[SubmitTopicSelectionPerspectiveAnalysisTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-tips-openapi/api-aimiaobi-2023-08-01-submittopicselectionperspectiveanalysistask.md)

提交选题热点分析任务

提交选题热点分析任务。

[GetTopicSelectionPerspectiveAnalysisTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-tips-openapi/api-aimiaobi-2023-08-01-gettopicselectionperspectiveanalysistask.md)

获取选题视角分析任务结果

获取选题视角分析任务结果。

[SubmitCustomTopicSelectionPerspectiveAnalysisTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-tips-openapi/api-aimiaobi-2023-08-01-submitcustomtopicselectionperspectiveanalysistask.md)

提交自定义热点选题视角分析任务

提交自定义热点选题视角分析任务。

[GetCustomTopicSelectionPerspectiveAnalysisTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-tips-openapi/api-aimiaobi-2023-08-01-getcustomtopicselectionperspectiveanalysistask.md)

获取自定义选题视角分析任务结果

获取自定义选题视角分析任务结果。

## 妙策-新闻播报

API

标题

API概述

[GetHotTopicBroadcast](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-policy-news-broadcast/api-aimiaobi-2023-08-01-gethottopicbroadcast.md)

查询完整播报单（热榜）

查询新闻播报单。

[SubmitCustomHotTopicBroadcastJob](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-policy-news-broadcast/api-aimiaobi-2023-08-01-submitcustomhottopicbroadcastjob.md)

提交自定义播报单任务

提交自定义播报单任务。

[GetCustomHotTopicBroadcastJob](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-policy-news-broadcast/api-aimiaobi-2023-08-01-getcustomhottopicbroadcastjob.md)

获取自定义播报单任务结果

获取自定义播报单任务结果。

## 妙策-企业VOC挖掘

API

标题

API概述

[ExportAnalysisTagDetailByTaskId](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaoce-enterprise-voc-mining/api-aimiaobi-2023-08-01-exportanalysistagdetailbytaskid.md)

导出标签挖掘结果

导出企业VOC分析任务明细列表。

[ValidateUploadTemplate](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaoce-enterprise-voc-mining/api-aimiaobi-2023-08-01-validateuploadtemplate.md)

校验VOC上传模板

校验企业VOC上传模板。

[SubmitEnterpriseVocAnalysisTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaoce-enterprise-voc-mining/api-aimiaobi-2023-08-01-submitenterprisevocanalysistask.md)

提交企业VOC分析任务

提交VOC异步任务。

[ListAnalysisTagDetailByTaskId](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaoce-enterprise-voc-mining/api-aimiaobi-2023-08-01-listanalysistagdetailbytaskid.md)

根据任务ID获取标签分析明细列表

分页获取企业VOC分析任务明细列表。

[GetEnterpriseVocAnalysisTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaoce-enterprise-voc-mining/api-aimiaobi-2023-08-01-getenterprisevocanalysistask.md)

获取企业VOC挖掘任务结果

获取企业VOC分析任务结果。

[GetCategoriesByTaskId](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaoce-enterprise-voc-mining/api-aimiaobi-2023-08-01-getcategoriesbytaskid.md)

根据任务ID获取分类列表

获取某次标签挖掘结果分类。

## 妙搜-数据源

API

标题

API概述

[CreateDataset](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-search-data-source/api-aimiaobi-2023-08-01-createdataset.md)

数据源-创建

数据源管理-创建。

[GetDataset](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-search-data-source/api-aimiaobi-2023-08-01-getdataset.md)

数据源-详情

数据源管理-详情。

[UpdateDataset](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-search-data-source/api-aimiaobi-2023-08-01-updatedataset.md)

数据源-修改

数据源管理-更新。

[ListDatasets](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-search-data-source/api-aimiaobi-2023-08-01-listdatasets.md)

数据源-列表

数据源管理-查询。

[DeleteDataset](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-search-data-source/api-aimiaobi-2023-08-01-deletedataset.md)

数据源-删除

数据源管理-删除。

[AddDatasetDocument](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-search-data-source/api-aimiaobi-2023-08-01-adddatasetdocument.md)

数据源-添加文档到数据集

添加文档到数据源。

[GetDatasetDocument](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-search-data-source/api-aimiaobi-2023-08-01-getdatasetdocument.md)

数据源-获取文档详情

获取数据源文档。

[UpdateDatasetDocument](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-search-data-source/api-aimiaobi-2023-08-01-updatedatasetdocument.md)

数据源-修改文档

修改数据源文档。

[ListDatasetDocuments](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-search-data-source/api-aimiaobi-2023-08-01-listdatasetdocuments.md)

数据源-文档列表

查询数据源文档列表。

[SearchDatasetDocuments](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-search-data-source/api-aimiaobi-2023-08-01-searchdatasetdocuments.md)

数据源-搜索文档

搜索数据源文档。

[DeleteDatasetDocument](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-search-data-source/api-aimiaobi-2023-08-01-deletedatasetdocument.md)

数据源-删除数据集文档

删除数据源文档。

## 妙搜-智能搜索

API

标题

API概述

[RunSearchGeneration](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-search-smart-search/api-aimiaobi-2023-08-01-runsearchgeneration.md)

妙搜-智能搜索

AI妙搜-智能搜索生成：对应妙搜首页的搜索生成能力。此接口支持通用搜索和媒资搜索。支持用户问题澄清、多模态知识搜索、多agent生成等能力。 - 通用搜索：可以对数据集中知识进行语义检索，并对搜索结果进行多agent后处理，包括总结生成、摘编、时间线总结等。 - 媒资搜索：应搜尽搜，全文检索，召回更多相关知识，并可进行多agent后处理，包括聚类、新闻抽取等。

[ListSearchTasks](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-search-smart-search/api-aimiaobi-2023-08-01-listsearchtasks.md)

查询妙搜搜索生成历史任务列表

查询妙搜搜索生成历史任务列表。

[ListSearchTaskDialogues](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-search-smart-search/api-aimiaobi-2023-08-01-listsearchtaskdialogues.md)

查询妙搜搜索生成任务详情列表

查询妙搜搜索生成任务详情列表。

[ListSearchTaskDialogueDatas](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-search-smart-search/api-aimiaobi-2023-08-01-listsearchtaskdialoguedatas.md)

查询搜索生成任务对话详情中数据列表

查询搜索生成任务对话详情中数据列表。

[RunSearchSimilarArticles](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-search-smart-search/api-aimiaobi-2023-08-01-runsearchsimilararticles.md)

妙搜-文搜文

妙搜-文搜文。

## 系统配置-干预配置

API

标题

API概述

[ListInterveneCnt](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-system-configuration-intervention-configuration/api-aimiaobi-2023-08-01-listintervenecnt.md)

获得所有干预项的数量

获得干预项目数量列表。

[ListIntervenes](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-system-configuration-intervention-configuration/api-aimiaobi-2023-08-01-listintervenes.md)

列出干预项

获得干预项列表。

[ImportInterveneFile](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-system-configuration-intervention-configuration/api-aimiaobi-2023-08-01-importintervenefile.md)

同步导入干预项文件

导入干预文件。

[InsertInterveneGlobalReply](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-system-configuration-intervention-configuration/api-aimiaobi-2023-08-01-insertinterveneglobalreply.md)

插入干预全局回复项

设置干预全局回复。

[ImportInterveneFileAsync](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-system-configuration-intervention-configuration/api-aimiaobi-2023-08-01-importintervenefileasync.md)

异步导入干预项文件

异步导入干预文件。

[GetInterveneTemplateFileUrl](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-system-configuration-intervention-configuration/api-aimiaobi-2023-08-01-getintervenetemplatefileurl.md)

获得干预导入模版文件地址

获得干预导入模版文件下载地址。

[ClearIntervenes](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-system-configuration-intervention-configuration/api-aimiaobi-2023-08-01-clearintervenes.md)

清除所有干预项

清除所有干预内容。

[GetInterveneGlobalReply](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-system-configuration-intervention-configuration/api-aimiaobi-2023-08-01-getinterveneglobalreply.md)

获得干预全局回复内容

获得干预全局回复。

[ListInterveneRules](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-system-configuration-intervention-configuration/api-aimiaobi-2023-08-01-listintervenerules.md)

列出干预规则

获得干预规则列表。

[ListInterveneImportTasks](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-system-configuration-intervention-configuration/api-aimiaobi-2023-08-01-listinterveneimporttasks.md)

列出干预项导入任务

获得导入任务列表。

[InsertInterveneRule](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-system-configuration-intervention-configuration/api-aimiaobi-2023-08-01-insertintervenerule.md)

插入干预规则

插入干预规则。

[GetInterveneRuleDetail](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-system-configuration-intervention-configuration/api-aimiaobi-2023-08-01-getinterveneruledetail.md)

获得干预规则的详情

获得干预项规则详情。

[DeleteInterveneRule](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-system-configuration-intervention-configuration/api-aimiaobi-2023-08-01-deleteintervenerule.md)

删除干预规则

删除干预规则。

[ExportIntervenes](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-system-configuration-intervention-configuration/api-aimiaobi-2023-08-01-exportintervenes.md)

导出干预项内容

导出所有干预内容。

[GetInterveneImportTaskInfo](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-system-configuration-intervention-configuration/api-aimiaobi-2023-08-01-getinterveneimporttaskinfo.md)

获得干预项目导入任务信息

获得导入任务信息。

## 系统配置-信源管理

API

标题

API概述

[SaveDataSourceOrderConfig](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-system-configuration-source-management/api-aimiaobi-2023-08-01-savedatasourceorderconfig.md)

保存信源权重配置

保存用户写作信源配置，通用搜索信源配置的配置信息。

[GetDataSourceOrderConfig](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-system-configuration-source-management/api-aimiaobi-2023-08-01-getdatasourceorderconfig.md)

获取信源配置权重数据

获取写作信源，通用搜索信源的配置信息。

## 妙读-基础操作类

API

标题

API概述

[GetDocInfo](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-reading-basic-operation-class/api-aimiaobi-2023-08-01-getdocinfo.md)

获取文档信息

妙读获取文档信息。

[GetFileContentLength](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-reading-basic-operation-class/api-aimiaobi-2023-08-01-getfilecontentlength.md)

获取文件长度

妙读获得文档字数。

[UploadBook](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-reading-basic-operation-class/api-aimiaobi-2023-08-01-uploadbook.md)

书籍上传

妙读上传书籍。

[UploadDoc](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-reading-basic-operation-class/api-aimiaobi-2023-08-01-uploaddoc.md)

文档上传

妙读上传文档接口。

[ListDocs](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-reading-basic-operation-class/api-aimiaobi-2023-08-01-listdocs.md)

获取文档列表

妙读获取文档列表。

[DeleteDocs](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-reading-basic-operation-class/api-aimiaobi-2023-08-01-deletedocs.md)

批量删除文档

妙读删除多个文档。

## 妙读-生成类

API

标题

API概述

[RunMultiDocIntroduction](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-reading-generate-class/api-aimiaobi-2023-08-01-runmultidocintroduction.md)

多文档聚合摘要

针对多篇文章、视频或者URL，生成总分结构的摘要（几篇文章的综合概述、关键要点）。此外支持多种多语言的输入和输出。

[RunDocBrainmap](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-reading-generate-class/api-aimiaobi-2023-08-01-rundocbrainmap.md)

全文脑图

针对文章或者书，生成三级脑图，且支持生成多语种，支持控制脑图第二级数量，支持控制叶子节点的字数。

[RunDocIntroduction](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-reading-generate-class/api-aimiaobi-2023-08-01-rundocintroduction.md)

文档导读

针对一篇文章、视频或者URL，生成文章的导读内容，包含全文总结、关键要点、章节速览（即分段、每段的总结、段落摘要）。此外支持多种多语言的输入和输出。如果用户仅需要对文章进行全文总结，可使用RunDocSummary接口实现，具体请参见[](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-rundocsummary)[https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-rundocsummary](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-rundocsummary)。

[RunDocSummary](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-reading-generate-class/api-aimiaobi-2023-08-01-rundocsummary.md)

文档摘要

针对一篇文章、视频或者URL，生成文章的摘要内容，即全文总结。此外支持多种多语言的输入和输出。

[RunDocWashing](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-reading-generate-class/api-aimiaobi-2023-08-01-rundocwashing.md)

改写

把一篇文章改换成指定风格。

[RunBookIntroduction](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-reading-generate-class/api-aimiaobi-2023-08-01-runbookintroduction.md)

书籍导读（抽取书籍卖点/书籍摘要）

基于一本书，抽取书籍的内容概要，以及结构化的卖点、热词信息。

[RunBookBrainmap](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-reading-generate-class/api-aimiaobi-2023-08-01-runbookbrainmap.md)

书籍脑图

妙读生成书籍脑图。

[RunCommentGeneration](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-reading-generate-class/api-aimiaobi-2023-08-01-runcommentgeneration.md)

客户之声预测

针对指定文章，预测用户之声。

## 妙读-抽取类

API

标题

API概述

[RunHotword](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-reading-extraction-class/api-aimiaobi-2023-08-01-runhotword.md)

抽取关键词

基于指定文章抽取关键词。关键词主要是指在特定领域或行业中具有代表性和识别度的专业术语或概念，它们能够精准地描述和概括某一行业内的核心内容、重要人物、关键事件或技术名词。

## 妙读-问答类

API

标题

API概述

[RunGenerateQuestions](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-reading-question-and-answer-class/api-aimiaobi-2023-08-01-rungeneratequestions.md)

猜你想问

输入一个query，返回几个相关query。

[RunDocQa](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-reading-question-and-answer-class/api-aimiaobi-2023-08-01-rundocqa.md)

文档问答（文章问答/多模态文件问答）

文章问答：针对一个自然语言类的query，在指定的文章范围内给出文字答案（有图则会配图），并显示溯源信息。 多模态文件问答：针对一个自然语言类的query，在指定的多模态文件范围内给出文字答案，并带上相关的图片、视频片段或者文字，并显示溯源信息。

## 妙读-其他

API

标题

API概述

[RunDocTranslation](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-reading-other/api-aimiaobi-2023-08-01-rundoctranslation.md)

文档翻译

中英文互译接口。

[RunDocSmartCard](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-reading-other/api-aimiaobi-2023-08-01-rundocsmartcard.md)

文档智能卡片

针对划选的文字或指定chat，自动打标并生成一个卡片笔记。

[RunBookSmartCard](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-reading-other/api-aimiaobi-2023-08-01-runbooksmartcard.md)

书籍智能卡片

书籍智能卡片接口。

## 深度写作

API

标题

API概述

[SubmitDeepWriteTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-deep-writing/api-aimiaobi-2023-08-01-submitdeepwritetask.md)

提交深度写作任务

提交深度写作任务。 用户可以根据要研究或分析的主题，填入问题、指令、附件等信息，来提交深度写作任务。该任务会在系统后台调度和执行。

[GetDeepWriteTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-deep-writing/api-aimiaobi-2023-08-01-getdeepwritetask.md)

查询深度写作任务

查询深度写作任务。 主要用来查询指定任务的运行状态。

[GetDeepWriteTaskResult](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-deep-writing/api-aimiaobi-2023-08-01-getdeepwritetaskresult.md)

查询深度写作任务的结果

查询深度写作任务的结果。 如果指定任务没有执行完成（排队、执行中、失败、取消等），会返回当前执行状态。如果指定任务已完成，会以URL的形式返回该任务的产出物的压缩包，供用户下载查看。

[CancelDeepWriteTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-deep-writing/api-aimiaobi-2023-08-01-canceldeepwritetask.md)

取消深度写作任务

取消深度写作任务。

[RunDeepWriting](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-deep-writing/api-aimiaobi-2023-08-01-rundeepwriting.md)

查询深度写作事件

查询深度写作事件。 系统以SSE事件的形式下发任务执行过程中的详细信息。

## PPT生成

API

标题

API概述

[ListEnterprisePptTemplates](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-ppt-generation/api-aimiaobi-2023-08-01-listenterpriseppttemplates.md)

查询企业专属PPT模板列表

查询企业专属PPT模板列表

[InitiatePptCreationV2](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-ppt-generation/api-aimiaobi-2023-08-01-initiatepptcreationv2.md)

初始化PPT创建操作

初始化PPT创建操作V2

[ListPptTemplates](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-ppt-generation/api-aimiaobi-2023-08-01-listppttemplates.md)

查询PPT模板列表

查询PPT模板列表

[GetPptTemplateSelector](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-ppt-generation/api-aimiaobi-2023-08-01-getppttemplateselector.md)

查询PPT模板筛选器

查询PPT模板筛选器

[GetPptArtifactExportResult](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-ppt-generation/api-aimiaobi-2023-08-01-getpptartifactexportresult.md)

查询PPT导出任务的结果

查询PPT导出任务的结果

[ExportPptArtifact](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-ppt-generation/api-aimiaobi-2023-08-01-exportpptartifact.md)

导出PPT作品

导出PPT作品

[GetPptArtifact](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-ppt-generation/api-aimiaobi-2023-08-01-getpptartifact.md)

查询PPT作品信息

查询PPT作品信息。

[ListPptArtifacts](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-ppt-generation/api-aimiaobi-2023-08-01-listpptartifacts.md)

查询PPT作品列表

查询PPT作品列表

[RunPptOutlineGeneration](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-ppt-generation/api-aimiaobi-2023-08-01-runpptoutlinegeneration.md)

生成PPT大纲内容

生成PPT大纲内容

[InitiatePptCreation](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-ppt-generation/api-aimiaobi-2023-08-01-initiatepptcreation.md)

初始化用来创建PPT的会话

重要说明：这个接口涉及到扣费，请注意费用 这个接口包含两个操作： 1. 下发用于初始化“PPT生成”的前端组件的code 2. 进行计费

[GetPptConfig](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-ppt-generation/api-aimiaobi-2023-08-01-getpptconfig.md)

获取PPT组件配置

获取PPT组件配置

[BindPptArtifact](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-ppt-generation/api-aimiaobi-2023-08-01-bindpptartifact.md)

绑定PPT作品信息

绑定PPT作品信息

[DeletePptArtifact](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-ppt-generation/api-aimiaobi-2023-08-01-deletepptartifact.md)

删除PPT作品

删除PPT作品

## 标书生成

API

标题

API概述

[AsyncUploadTenderDoc](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-tender-generation/api-aimiaobi-2023-08-01-asyncuploadtenderdoc.md)

招标文档解析

上传招标书文件

[GetBiddingRemainLimitNum](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-tender-generation/api-aimiaobi-2023-08-01-getbiddingremainlimitnum.md)

获得标书写作剩余额度

获得标书功能剩余额度

[GetBiddingDocInfo](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-tender-generation/api-aimiaobi-2023-08-01-getbiddingdocinfo.md)

获得标书写作结果

获得标书写作结果接口

[EditBiddingDoc](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-tender-generation/api-aimiaobi-2023-08-01-editbiddingdoc.md)

编辑标书内容

编辑标书内容接口

[DownloadBiddingDoc](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-tender-generation/api-aimiaobi-2023-08-01-downloadbiddingdoc.md)

下载标书文件

标书下载接口

[AsyncWritingBiddingDoc](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-tender-generation/api-aimiaobi-2023-08-01-asyncwritingbiddingdoc.md)

标书写作

标书写作接口

[ListBiddingDoc](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-tender-generation/api-aimiaobi-2023-08-01-listbiddingdoc.md)

列出标书写作任务

获得标书写作任务列表

## 其他

API

标题

API概述

[RunVideoScriptGenerate](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-other/api-aimiaobi-2023-08-01-runvideoscriptgenerate.md)

AI生成视频剪辑脚本

AI生成视频剪辑脚本

[GetSmartClipTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-other/api-aimiaobi-2023-08-01-getsmartcliptask.md)

获取智能剪辑任务结果

查询一键成片剪辑任务。

[SubmitSmartClipTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-other/api-aimiaobi-2023-08-01-submitsmartcliptask.md)

提交智能一键成片任务

提交一键成片剪辑任务。

[SaveOrUpdateOssConfig](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-other/api-aimiaobi-2023-08-01-saveorupdateossconfig.md)

配置-云存储-参数配置

配置-云存储-参数配置

[CreateDataPermissions](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-other/api-aimiaobi-2023-08-01-createdatapermissions.md)

权限-批量添加

权限-批量添加： - 数据集权限：

[DeleteDataPermissions](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-other/api-aimiaobi-2023-08-01-deletedatapermissions.md)

权限-删除

权限-批量删除： - 数据集权限

[ListDataPermissions](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-other/api-aimiaobi-2023-08-01-listdatapermissions.md)

权限-列表

权限-列表 - 数据集

[GenerateViewPoint](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-other/api-aimiaobi-2023-08-01-generateviewpoint.md)

生成选题视角（已过时，不推荐使用）

生成选题视角。

[GetPptInfo](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-other/api-aimiaobi-2023-08-01-getpptinfo.md)

查询PPT任务信息

查询PPT任务信息

SubmitParseDocumentLayoutTask

提交排版任务

提交版本任务

[FetchParseDocumentLayoutTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-other/api-aimiaobi-2023-08-01-fetchparsedocumentlayouttask.md)

获取排版任务结果

获取排版任务结果

[CancelAuditTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-other/api-aimiaobi-2023-08-01-cancelaudittask.md)

取消审核任务

取消审核任务

[QueryAuditTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-other/api-aimiaobi-2023-08-01-queryaudittask.md)

查询审核结果

查询审核结果。

[SubmitAuditTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-other/api-aimiaobi-2023-08-01-submitaudittask.md)

提交审核任务

提交审核任务
