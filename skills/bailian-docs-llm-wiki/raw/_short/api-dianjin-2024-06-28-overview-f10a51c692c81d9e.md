# API概览

## API标准及多语言预置SDK

本产品（`DianJin/2024-06-28`）的OpenAPI采用[ROA](https://help.aliyun.com/zh/sdk/product-overview/roa-mechanism)签名风格。我们已经为开发者封装了常见编程语言的SDK，开发者可通过[下载SDK](https://api.aliyun.com/api-tools/sdk/DianJin?version=2024-06-28)直接调用本产品OpenAPI而无需关心技术细节。如果现有SDK不能满足使用需求，可通过签名机制进行自签名对接。由于自签名细节非常复杂，需花费 5个工作日左右。因此建议加入我们的服务钉钉群（147535001692），在专家指导下进行签名对接。

在使用API前，您需要准备好身份账号及访问密钥（AccessKey），才能有效通过客户端工具（SDK、CLI等）访问API。细节请参见[获取AccessKey](https://help.aliyun.com/zh/ram/user-guide/create-an-accesskey-pair)。

## 自定义签名场景

若您的业务场景有特殊需求，需通过自签名方式对接 API，建议优先咨询我们的技术支持团队（服务钉钉群：147535001692），获取专业指导以确保高效接入。

## 账号与安全准备

阿里云账号具备对所有资源的完全管理权限。一旦 AccessKey 泄露，所有相关资源都将面临未经授权访问的风险。为确保安全，建议创建一个仅具备 API 访问权限的[RAM用户](https://help.aliyun.com/zh/ram/user-guide/create-a-ram-user)并配置其 AccessKey，同时基于最小权限原则 (PoLP) 配置 RAM 策略。仅在明确需要阿里云账号权限的特定场景下，才使用阿里云账号。

## 平台能力-文档库

API

标题

API概述

[UpdateDocumentChunk](raw/_short/api-dianjin-2024-06-28-updatedocumentchunk-95f1a29a25b7c6b4.md)

更新文档块内容

更新文档中的文档块文本内容。

[GetAppConfig](raw/_short/api-dianjin-2024-06-28-getappconfig-f485996c5592f58d.md)

获取配置信息

获取app配置。

[CreateLibrary](raw/_short/api-dianjin-2024-06-28-createlibrary-fe96c03f278c21a9.md)

创建文档库

创建文档库。创建一个新的文档库，文档库用作隔离文档信息、索引信息，如果使用场景中需要经常按类别去做自然语言检索，建议创建多个文档库，来隔离不同类型的数据。支持按照格式自定义向量索引和文本索引。

[GetLibraryList](raw/_short/api-dianjin-2024-06-28-getlibrarylist-d4c0f01c6da10135.md)

获取文档库列表

获取文档库列表，包含文档名称、描述、唯一标识等信息。

[GetLibrary](raw/_short/api-dianjin-2024-06-28-getlibrary-4e60718f81cf43ec.md)

获取文档库详情

查看文档库的详细配置，包括文档库名称、描述以及索引等详细配置信息。

[UploadDocument](raw/_short/api-dianjin-2024-06-28-uploaddocument-748599774e1f9b34.md)

上传文档

上传文档至文档库，会对文档进行解析、分块、构建索引等一系列操作。

[GetDocumentUrl](raw/_short/api-dianjin-2024-06-28-getdocumenturl-177de44f49163647.md)

获取文档的下载链接

获取文档的下载链接，链接过期时间为1小时。

[PreviewDocument](raw/_short/api-dianjin-2024-06-28-previewdocument-7cc9b2e89958a89a.md)

预览文档

预览文档，可获取文档的下载链接，文档类型、标题等信息，可用于文档预览。

[GetFilterDocumentList](raw/_short/api-dianjin-2024-06-28-getfilterdocumentlist-10c5255d093607e7.md)

按元信息过滤查询文档列表

获取文档列表（可按元信息过滤查询，也支持分页查询）。

[GetDocumentList](raw/_short/api-dianjin-2024-06-28-getdocumentlist-97cc9f04612aafd3.md)

获取文档列表

获取文档库内文档列表，可分页查询，也根据文档状态进行过滤查询。

[DeleteDocument](raw/_short/api-dianjin-2024-06-28-deletedocument-1cac7eaaa8be4c82.md)

删除文档

删除文档，删除后将无法查看原始文档，无法召回该文档。

[UpdateDocument](raw/_short/api-dianjin-2024-06-28-updatedocument-9b247eb074c12c6d.md)

更新文档

更新文档，用于更新文档的标题、元数据等信息。

[CreatePredefinedDocument](raw/_short/api-dianjin-2024-06-28-createpredefineddocument-87ec6835919ceb8a.md)

创建预定义文档

根据业务场景灵活构建文档块。

[GetDocumentChunkList](raw/_short/api-dianjin-2024-06-28-getdocumentchunklist-fcc333a65326dc4b.md)

获取文档块列表

获取文档块列表，可根据查询条件过滤。

[RecallDocument](raw/_short/api-dianjin-2024-06-28-recalldocument-fad6fb7e42441a58.md)

文档召回

文档召回，可根据文本从文档库中召回文档块。并可设置召回文档块数量、也可根据元信息条件进行过滤，同时可选择是否进行文档块的补全。

[GetParseResult](raw/_short/api-dianjin-2024-06-28-getparseresult-bdc9de7bd8602bf1.md)

获取文档解析结果

获取文档解析结果。可查询文档的解析状态以及获取文档的解析结果。

[ReIndex](raw/_short/api-dianjin-2024-06-28-reindex-15ae475eaeb9f921.md)

重建索引

重建索引，会对指定文档重新进行文档解析、分块、构建索引等流程。

[UpdateLibrary](raw/_short/api-dianjin-2024-06-28-updatelibrary-ca4fa6020b3343e7.md)

更新文档库

更新文档库，可用于更新文档库的名称、描述、索引配置等信息。

[DeleteLibrary](raw/_short/api-dianjin-2024-06-28-deletelibrary-5b704daaf5dc6eab.md)

删除文档库

删除文档库，注意⚠️，此接口将会删除文档库及其关联的所有文档。

[RunLibraryChatGeneration](raw/_short/api-dianjin-2024-06-28-runlibrarychatgeneration-aa6a43f9039346d0.md)

文档库会话生成

文档库会话生成，用自然语言提问，检索文档库相关信息，总结回答。

[GetHistoryListByBizType](raw/_short/api-dianjin-2024-06-28-gethistorylistbybiztype-37e128c2a4d84a3d.md)

根据业务类型获取对话历史记录

根据业务类型获取对话历史记录。

[InvokePlugin](raw/_short/api-dianjin-2024-06-28-invokeplugin-0b57a6f398ea03af.md)

调用插件

调用插件，获取插件返回结果。

## 平台能力-应用

API

标题

API概述

[EndToEndRealTimeDialog](raw/_short/api-dianjin-2024-06-28-endtoendrealtimedialog-789616a9d974ef61.md)

语音实时对话

本接口通过 WebSocket 协议实现实时语音对话转写、意图识别、话术语音合成返回等功能，支持多种音频格式的输入输出，满足实时性与高兼容性需求。

[RunDialogAnalysis](raw/_short/api-dianjin-2024-06-28-rundialoganalysis-9d097046c0901d7d.md)

会话分析结果生成

流式接口，获取会话分析结果。

[RunAgent](raw/_short/api-dianjin-2024-06-28-runagent-291ba01f8150decb.md)

运行智能体

运行智能体，支持流式和非流式。

[CreateDialog](raw/_short/api-dianjin-2024-06-28-createdialog-4f1b6f52d296cff3.md)

创建外呼会话

创建外呼会话。

[RealTimeDialog](raw/_short/api-dianjin-2024-06-28-realtimedialog-6e1584e95bab923f.md)

实时会话

实时会话，通过API CreateDialog创建会话后，可使用该API进行实时会话。

[RealtimeDialogAssist](raw/_short/api-dianjin-2024-06-28-realtimedialogassist-b7d92807b0722c04.md)

实时会话辅助

实时会话辅助，使用CreateDialog创建会话后，可进行实时的会话辅助。注意：与实时会话不同，会话辅助可返回多个意图、标签和SOP流程等，但不支持流式返回。

[GetDialogDetail](raw/_short/api-dianjin-2024-06-28-getdialogdetail-afae609741520f70.md)

获取会话详情

获取会话详情信息。

[GetDialogLog](raw/_short/api-dianjin-2024-06-28-getdialoglog-4c2258166af0cd02.md)

获取对话日志

用于获取实时对话的记录及意图分析结果。

[GetDialogAnalysisResult](raw/_short/api-dianjin-2024-06-28-getdialoganalysisresult-707cee4927aefc3f.md)

获取会话分析结果

获取会话分析结果。可批量获取，根据会话ID列表或时间范围。

[CreateDialogAnalysisTask](raw/_short/api-dianjin-2024-06-28-createdialoganalysistask-ef74d145582f87ee.md)

创建会话分析任务

创建会话分析任务，创建成功后可根据会话ID使用GetDialogAnalysisResult查询结果

[RebuildTask](raw/_short/api-dianjin-2024-06-28-rebuildtask-261efcb12afc4125.md)

重建任务

对已有任务进行重建，但在队列中或执行中的任务不可重建。

[EvictTask](raw/_short/api-dianjin-2024-06-28-evicttask-9c7fbb21a4f0a49d.md)

取消任务

中断任务。

[GetTaskStatus](raw/_short/api-dianjin-2024-06-28-gettaskstatus-8e77d88df65964dc.md)

获取任务状态

获取任务状态。

[CreateDocsSummaryTask](raw/_short/api-dianjin-2024-06-28-createdocssummarytask-4ee1b4b147537c6e.md)

创建多文档总结任务

创建多文档总结任务。

[CreateAnnualDocSummaryTask](raw/_short/api-dianjin-2024-06-28-createannualdocsummarytas-d0858b7a68f1501d.md)

创建按年份总结文档任务

创建按年份总结文档任务。

[CreatePdfTranslateTask](raw/_short/api-dianjin-2024-06-28-createpdftranslatetask-f9276660d23e2fd5.md)

创建pdf文档翻译任务

创建pdf文档翻译任务。提交翻译任务，异步执行翻译过程。

[CreateFinReportSummaryTask](raw/_short/api-dianjin-2024-06-28-createfinreportsummarytas-5a84417ddeb394e2.md)

创建财报总结任务

创建财报总结接口。

[GetSummaryTaskResult](raw/_short/api-dianjin-2024-06-28-getsummarytaskresult-0ce802b1fbb0f4a2.md)

获取财报总结任务结果

获取财报总结任务结果。

[GetTaskResult](raw/_short/api-dianjin-2024-06-28-gettaskresult-6d86ccbb347639e9.md)

获取结果

获取异步任务结果。

[CreateQualityCheckTask](raw/_short/api-dianjin-2024-06-28-createqualitychecktask-7e856435445fc73e.md)

创建质检任务

创建质检任务。

[GetQualityCheckTaskResult](raw/_short/api-dianjin-2024-06-28-getqualitychecktaskresult-fbfd65435be19a3a.md)

获取质检结果

获取质检结果。

[RecognizeIntention](raw/_short/api-dianjin-2024-06-28-recognizeintention-b7ec3836a14da8fd.md)

意图识别

意图识别，支持意图识别（全局+分层）、态度识别、企业识别。

[GenDocQaResult](raw/_short/api-dianjin-2024-06-28-gendocqaresult-861ddce81b5e38cd.md)

根据文档解析问答QA

根据文档解析问答QA，可在API UpdateQaLibrary进行QA对的更新。

[UpdateQaLibrary](raw/_short/api-dianjin-2024-06-28-updateqalibrary-1113de843f1bd0b6.md)

更新QA问答库

更新QA问答库。更新后，可通过API GenDocQaResult来解析QA。

[SubmitChatQuestion](raw/_short/api-dianjin-2024-06-28-submitchatquestion-015f8f190d5889df.md)

提交问题列表

提交问题列表，通过API GetChatQuestionResp获取结果。

[GetChatQuestionResp](raw/_short/api-dianjin-2024-06-28-getchatquestionresp-af6e2e087efc2119.md)

获取问答结果

获取问答结果，即API SubmitChatQuestion的结果。

[RunChatResultGeneration](raw/_short/api-dianjin-2024-06-28-runchatresultgeneration-f618282b43943c42.md)

对话结果生成

对话结果生成，可选择模型进行对话，支持流式和非流式。

## 其他

API

标题

API概述

[DashscopeAsyncTaskFinishEvent](raw/_short/api-dianjin-2024-06-28-dashscopeasynctaskfinishe-177ccb24aa56105f.md)

Dashscope异步任务完成回调事件

Dashscope异步任务完成回调事件
