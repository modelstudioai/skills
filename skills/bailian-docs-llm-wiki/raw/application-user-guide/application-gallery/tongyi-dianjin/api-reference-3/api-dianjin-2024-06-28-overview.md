# API概览

## API标准及多语言预置SDK

本产品（`通义点金/2024-06-28`）的 OpenAPI 采用 ROA 签名机制，具体签名方式请参见[签名机制说明](https://help.aliyun.com/zh/sdk/product-overview/v3-request-structure-and-signature)。我们已为开发者封装了主流编程语言的 SDK，您可通过 [下载 SDK](https://api.aliyun.com/api-tools/sdk/DianJin?version=2024-06-28) 快速调用 API，无需关注签名等底层实现细节，显著降低开发门槛与集成复杂度。

## 自定义签名场景

若您的业务场景有特殊需求，需通过自签名方式对接 API，建议优先咨询我们的技术支持团队（服务钉钉群：147535001692），获取专业指导以确保高效接入。

## 账号与安全准备

阿里云账号具备对所有资源的完全管理权限。一旦 AccessKey 泄露，所有相关资源都将面临未经授权访问的风险。为确保安全，建议创建一个仅具备 API 访问权限的 [RAM 用户](https://help.aliyun.com/zh/ram/user-guide/create-a-ram-user)并配置其 AccessKey，同时基于最小权限原则 (PoLP) 配置 RAM 策略。仅在明确需要阿里云账号权限的特定场景下，才使用阿里云账号。

## 平台能力-文档库

API

标题

API概述

[UpdateDocumentChunk](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-updatedocumentchunk)

更新文档块内容

更新文档中的文档块文本内容。

[GetAppConfig](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-getappconfig)

获取配置信息

获取app配置。

[CreateLibrary](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-createlibrary)

创建文档库

创建文档库。创建一个新的文档库，文档库用作隔离文档信息、索引信息，如果使用场景中需要经常按类别去做自然语言检索，建议创建多个文档库，来隔离不同类型的数据。支持按照格式自定义向量索引和文本索引。

[GetLibraryList](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-getlibrarylist)

获取文档库列表

获取文档库列表，包含文档名称、描述、唯一标识等信息。

[GetLibrary](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-getlibrary)

获取文档库详情

查看文档库的详细配置，包括文档库名称、描述以及索引等详细配置信息。

[UploadDocument](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-uploaddocument)

上传文档

上传文档至文档库，会对文档进行解析、分块、构建索引等一系列操作。

[GetDocumentUrl](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-getdocumenturl)

获取文档的下载链接

获取文档的下载链接，链接过期时间为1小时。

[PreviewDocument](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-previewdocument)

预览文档

预览文档，可获取文档的下载链接，文档类型、标题等信息，可用于文档预览。

[GetFilterDocumentList](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-getfilterdocumentlist)

按元信息过滤查询文档列表

获取文档列表（可按元信息过滤查询，也支持分页查询）。

[GetDocumentList](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-getdocumentlist)

获取文档列表

获取文档库内文档列表，可分页查询，也根据文档状态进行过滤查询。

[DeleteDocument](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-deletedocument)

删除文档

删除文档，删除后将无法查看原始文档，无法召回该文档。

[UpdateDocument](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-updatedocument)

更新文档

更新文档，用于更新文档的标题、元数据等信息。

[CreatePredefinedDocument](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-createpredefineddocument)

创建预定义文档

根据业务场景灵活构建文档块。

[GetDocumentChunkList](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-getdocumentchunklist)

获取文档块列表

获取文档块列表，可根据查询条件过滤。

[RecallDocument](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-recalldocument)

文档召回

文档召回，可根据文本从文档库中召回文档块。并可设置召回文档块数量、也可根据元信息条件进行过滤，同时可选择是否进行文档块的补全。

[GetParseResult](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-getparseresult)

获取文档解析结果

获取文档解析结果。可查询文档的解析状态以及获取文档的解析结果。

[ReIndex](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-reindex)

重建索引

重建索引，会对指定文档重新进行文档解析、分块、构建索引等流程。

[UpdateLibrary](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-updatelibrary)

更新文档库

更新文档库，可用于更新文档库的名称、描述、索引配置等信息。

[DeleteLibrary](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-deletelibrary)

删除文档库

删除文档库，注意⚠️，此接口将会删除文档库及其关联的所有文档。

[RunLibraryChatGeneration](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-runlibrarychatgeneration)

文档库会话生成

文档库会话生成，用自然语言提问，检索文档库相关信息，总结回答。

[GetHistoryListByBizType](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-gethistorylistbybiztype)

根据业务类型获取对话历史记录

根据业务类型获取对话历史记录。

[InvokePlugin](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-invokeplugin)

调用插件

调用插件，获取插件返回结果。

## 平台能力-应用

API

标题

API概述

[EndToEndRealTimeDialog](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-endtoendrealtimedialog)

语音实时对话

本接口通过 WebSocket 协议实现实时语音对话转写、意图识别、话术语音合成返回等功能，支持多种音频格式的输入输出，满足实时性与高兼容性需求。

[RunDialogAnalysis](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-rundialoganalysis)

会话分析结果生成

流式接口，获取会话分析结果。

[RunAgent](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-runagent)

运行智能体

运行智能体，支持流式和非流式。

[CreateDialog](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-createdialog)

创建外呼会话

创建外呼会话。

[RealTimeDialog](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-realtimedialog)

实时会话

实时会话，通过API CreateDialog创建会话后，可使用该API进行实时会话。

[RealtimeDialogAssist](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-realtimedialogassist)

实时会话辅助

实时会话辅助，使用CreateDialog创建会话后，可进行实时的会话辅助。注意：与实时会话不同，会话辅助可返回多个意图、标签和SOP流程等，但不支持流式返回。

[GetDialogDetail](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-getdialogdetail)

获取会话详情

获取会话详情信息。

[GetDialogLog](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-getdialoglog)

获取对话日志

用于获取实时对话的记录及意图分析结果。

[GetDialogAnalysisResult](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-getdialoganalysisresult)

获取会话分析结果

获取会话分析结果。可批量获取，根据会话ID列表或时间范围。

[CreateDialogAnalysisTask](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-createdialoganalysistask)

创建会话分析任务

创建会话分析任务，创建成功后可根据会话ID使用GetDialogAnalysisResult查询结果

[RebuildTask](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-rebuildtask)

重建任务

对已有任务进行重建，但在队列中或执行中的任务不可重建。

[EvictTask](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-evicttask)

取消任务

中断任务。

[GetTaskStatus](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-gettaskstatus)

获取任务状态

获取任务状态。

[CreateDocsSummaryTask](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-createdocssummarytask)

创建多文档总结任务

创建多文档总结任务。

[CreateAnnualDocSummaryTask](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-createannualdocsummarytask)

创建按年份总结文档任务

创建按年份总结文档任务。

[CreatePdfTranslateTask](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-createpdftranslatetask)

创建pdf文档翻译任务

创建pdf文档翻译任务。提交翻译任务，异步执行翻译过程。

[CreateFinReportSummaryTask](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-createfinreportsummarytask)

创建财报总结任务

创建财报总结接口。

[GetSummaryTaskResult](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-getsummarytaskresult)

获取财报总结任务结果

获取财报总结任务结果。

[GetTaskResult](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-gettaskresult)

获取结果

获取异步任务结果。

[CreateQualityCheckTask](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-createqualitychecktask)

创建质检任务

创建质检任务。

[GetQualityCheckTaskResult](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-getqualitychecktaskresult)

获取质检结果

获取质检结果。

[RecognizeIntention](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-recognizeintention)

意图识别

意图识别，支持意图识别（全局+分层）、态度识别、企业识别。

[GenDocQaResult](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-gendocqaresult)

根据文档解析问答QA

根据文档解析问答QA，可在API UpdateQaLibrary进行QA对的更新。

[UpdateQaLibrary](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-updateqalibrary)

更新QA问答库

更新QA问答库。更新后，可通过API GenDocQaResult来解析QA。

[SubmitChatQuestion](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-submitchatquestion)

提交问题列表

提交问题列表，通过API GetChatQuestionResp获取结果。

[GetChatQuestionResp](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-getchatquestionresp)

获取问答结果

获取问答结果，即API SubmitChatQuestion的结果。

[RunChatResultGeneration](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-runchatresultgeneration)

对话结果生成

对话结果生成，可选择模型进行对话，支持流式和非流式。

## 其他

API

标题

API概述

[DashscopeAsyncTaskFinishEvent](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-dashscopeasynctaskfinishevent)

Dashscope异步任务完成回调事件

Dashscope异步任务完成回调事件
