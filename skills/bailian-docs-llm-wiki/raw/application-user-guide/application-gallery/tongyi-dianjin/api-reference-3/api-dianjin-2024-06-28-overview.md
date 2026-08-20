# API概览

## API标准及多语言预置SDK

本产品（`DianJin/2024-06-28`）的OpenAPI采用ROA签名风格。我们已经为开发者封装了常见编程语言的SDK，开发者可通过[下载SDK](https://api.aliyun.com/api-tools/sdk/DianJin?version=2024-06-28)直接调用本产品OpenAPI而无需关心技术细节。如果现有SDK不能满足使用需求，可通过签名机制进行自签名对接。由于自签名细节非常复杂，需花费 5个工作日左右。因此建议加入我们的服务钉钉群（147535001692），在专家指导下进行签名对接。

在使用API前，您需要准备好身份账号及访问密钥（AccessKey），才能有效通过客户端工具（SDK、CLI等）访问API。细节请参见获取AccessKey。

## 自定义签名场景

若您的业务场景有特殊需求，需通过自签名方式对接 API，建议优先咨询我们的技术支持团队（服务钉钉群：147535001692），获取专业指导以确保高效接入。

## 账号与安全准备

阿里云账号具备对所有资源的完全管理权限。一旦 AccessKey 泄露，所有相关资源都将面临未经授权访问的风险。为确保安全，建议创建一个仅具备 API 访问权限的RAM用户并配置其 AccessKey，同时基于最小权限原则 (PoLP) 配置 RAM 策略。仅在明确需要阿里云账号权限的特定场景下，才使用阿里云账号。

## 平台能力-文档库

API

标题

API概述

[UpdateDocumentChunk](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-document-library/api-dianjin-2024-06-28-updatedocumentchunk.md)

更新文档块内容

更新文档中的文档块文本内容。

[GetAppConfig](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-document-library/api-dianjin-2024-06-28-getappconfig.md)

获取配置信息

获取app配置。

[CreateLibrary](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-document-library/api-dianjin-2024-06-28-createlibrary.md)

创建文档库

创建文档库。创建一个新的文档库，文档库用作隔离文档信息、索引信息，如果使用场景中需要经常按类别去做自然语言检索，建议创建多个文档库，来隔离不同类型的数据。支持按照格式自定义向量索引和文本索引。

[GetLibraryList](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-document-library/api-dianjin-2024-06-28-getlibrarylist.md)

获取文档库列表

获取文档库列表，包含文档名称、描述、唯一标识等信息。

[GetLibrary](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-document-library/api-dianjin-2024-06-28-getlibrary.md)

获取文档库详情

查看文档库的详细配置，包括文档库名称、描述以及索引等详细配置信息。

[UploadDocument](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-document-library/api-dianjin-2024-06-28-uploaddocument.md)

上传文档

上传文档至文档库，会对文档进行解析、分块、构建索引等一系列操作。

[GetDocumentUrl](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-document-library/api-dianjin-2024-06-28-getdocumenturl.md)

获取文档的下载链接

获取文档的下载链接，链接过期时间为1小时。

[PreviewDocument](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-document-library/api-dianjin-2024-06-28-previewdocument.md)

预览文档

预览文档，可获取文档的下载链接，文档类型、标题等信息，可用于文档预览。

[GetFilterDocumentList](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-document-library/api-dianjin-2024-06-28-getfilterdocumentlist.md)

按元信息过滤查询文档列表

获取文档列表（可按元信息过滤查询，也支持分页查询）。

[GetDocumentList](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-document-library/api-dianjin-2024-06-28-getdocumentlist.md)

获取文档列表

获取文档库内文档列表，可分页查询，也根据文档状态进行过滤查询。

[DeleteDocument](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-document-library/api-dianjin-2024-06-28-deletedocument.md)

删除文档

删除文档，删除后将无法查看原始文档，无法召回该文档。

[UpdateDocument](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-document-library/api-dianjin-2024-06-28-updatedocument.md)

更新文档

更新文档，用于更新文档的标题、元数据等信息。

[CreatePredefinedDocument](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-document-library/api-dianjin-2024-06-28-createpredefineddocument.md)

创建预定义文档

根据业务场景灵活构建文档块。

[GetDocumentChunkList](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-document-library/api-dianjin-2024-06-28-getdocumentchunklist.md)

获取文档块列表

获取文档块列表，可根据查询条件过滤。

[RecallDocument](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-document-library/api-dianjin-2024-06-28-recalldocument.md)

文档召回

文档召回，可根据文本从文档库中召回文档块。并可设置召回文档块数量、也可根据元信息条件进行过滤，同时可选择是否进行文档块的补全。

[GetParseResult](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-document-library/api-dianjin-2024-06-28-getparseresult.md)

获取文档解析结果

获取文档解析结果。可查询文档的解析状态以及获取文档的解析结果。

[ReIndex](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-document-library/api-dianjin-2024-06-28-reindex.md)

重建索引

重建索引，会对指定文档重新进行文档解析、分块、构建索引等流程。

[UpdateLibrary](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-document-library/api-dianjin-2024-06-28-updatelibrary.md)

更新文档库

更新文档库，可用于更新文档库的名称、描述、索引配置等信息。

[DeleteLibrary](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-document-library/api-dianjin-2024-06-28-deletelibrary.md)

删除文档库

删除文档库，注意⚠️，此接口将会删除文档库及其关联的所有文档。

[RunLibraryChatGeneration](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-document-library/api-dianjin-2024-06-28-runlibrarychatgeneration.md)

文档库会话生成

文档库会话生成，用自然语言提问，检索文档库相关信息，总结回答。

[GetHistoryListByBizType](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-document-library/api-dianjin-2024-06-28-gethistorylistbybiztype.md)

根据业务类型获取对话历史记录

根据业务类型获取对话历史记录。

[InvokePlugin](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-document-library/api-dianjin-2024-06-28-invokeplugin.md)

调用插件

调用插件，获取插件返回结果。

## 平台能力-应用

API

标题

API概述

[EndToEndRealTimeDialog](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-application/api-dianjin-2024-06-28-endtoendrealtimedialog.md)

语音实时对话

本接口通过 WebSocket 协议实现实时语音对话转写、意图识别、话术语音合成返回等功能，支持多种音频格式的输入输出，满足实时性与高兼容性需求。

[RunDialogAnalysis](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-application/api-dianjin-2024-06-28-rundialoganalysis.md)

会话分析结果生成

流式接口，获取会话分析结果。

[RunAgent](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-application/api-dianjin-2024-06-28-runagent.md)

运行智能体

运行智能体，支持流式和非流式。

[CreateDialog](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-application/api-dianjin-2024-06-28-createdialog.md)

创建外呼会话

创建外呼会话。

[RealTimeDialog](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-application/api-dianjin-2024-06-28-realtimedialog.md)

实时会话

实时会话，通过API CreateDialog创建会话后，可使用该API进行实时会话。

[RealtimeDialogAssist](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-application/api-dianjin-2024-06-28-realtimedialogassist.md)

实时会话辅助

实时会话辅助，使用CreateDialog创建会话后，可进行实时的会话辅助。注意：与实时会话不同，会话辅助可返回多个意图、标签和SOP流程等，但不支持流式返回。

[GetDialogDetail](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-application/api-dianjin-2024-06-28-getdialogdetail.md)

获取会话详情

获取会话详情信息。

[GetDialogLog](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-application/api-dianjin-2024-06-28-getdialoglog.md)

获取对话日志

用于获取实时对话的记录及意图分析结果。

[GetDialogAnalysisResult](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-application/api-dianjin-2024-06-28-getdialoganalysisresult.md)

获取会话分析结果

获取会话分析结果。可批量获取，根据会话ID列表或时间范围。

[CreateDialogAnalysisTask](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-application/api-dianjin-2024-06-28-createdialoganalysistask.md)

创建会话分析任务

创建会话分析任务，创建成功后可根据会话ID使用GetDialogAnalysisResult查询结果

[RebuildTask](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-application/api-dianjin-2024-06-28-rebuildtask.md)

重建任务

对已有任务进行重建，但在队列中或执行中的任务不可重建。

[EvictTask](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-application/api-dianjin-2024-06-28-evicttask.md)

取消任务

中断任务。

[GetTaskStatus](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-application/api-dianjin-2024-06-28-gettaskstatus.md)

获取任务状态

获取任务状态。

[CreateDocsSummaryTask](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-application/api-dianjin-2024-06-28-createdocssummarytask.md)

创建多文档总结任务

创建多文档总结任务。

[CreateAnnualDocSummaryTask](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-application/api-dianjin-2024-06-28-createannualdocsummarytask.md)

创建按年份总结文档任务

创建按年份总结文档任务。

[CreatePdfTranslateTask](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-application/api-dianjin-2024-06-28-createpdftranslatetask.md)

创建pdf文档翻译任务

创建pdf文档翻译任务。提交翻译任务，异步执行翻译过程。

[CreateFinReportSummaryTask](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-application/api-dianjin-2024-06-28-createfinreportsummarytask.md)

创建财报总结任务

创建财报总结接口。

[GetSummaryTaskResult](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-application/api-dianjin-2024-06-28-getsummarytaskresult.md)

获取财报总结任务结果

获取财报总结任务结果。

[GetTaskResult](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-application/api-dianjin-2024-06-28-gettaskresult.md)

获取结果

获取异步任务结果。

[CreateQualityCheckTask](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-application/api-dianjin-2024-06-28-createqualitychecktask.md)

创建质检任务

创建质检任务。

[GetQualityCheckTaskResult](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-application/api-dianjin-2024-06-28-getqualitychecktaskresult.md)

获取质检结果

获取质检结果。

[RecognizeIntention](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-application/api-dianjin-2024-06-28-recognizeintention.md)

意图识别

意图识别，支持意图识别（全局+分层）、态度识别、企业识别。

[GenDocQaResult](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-application/api-dianjin-2024-06-28-gendocqaresult.md)

根据文档解析问答QA

根据文档解析问答QA，可在API UpdateQaLibrary进行QA对的更新。

[UpdateQaLibrary](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-application/api-dianjin-2024-06-28-updateqalibrary.md)

更新QA问答库

更新QA问答库。更新后，可通过API GenDocQaResult来解析QA。

[SubmitChatQuestion](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-application/api-dianjin-2024-06-28-submitchatquestion.md)

提交问题列表

提交问题列表，通过API GetChatQuestionResp获取结果。

[GetChatQuestionResp](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-application/api-dianjin-2024-06-28-getchatquestionresp.md)

获取问答结果

获取问答结果，即API SubmitChatQuestion的结果。

[RunChatResultGeneration](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-application/api-dianjin-2024-06-28-runchatresultgeneration.md)

对话结果生成

对话结果生成，可选择模型进行对话，支持流式和非流式。

## 其他

API

标题

API概述

[DashscopeAsyncTaskFinishEvent](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-other/api-dianjin-2024-06-28-dashscopeasynctaskfinishevent.md)

Dashscope异步任务完成回调事件

Dashscope异步任务完成回调事件
