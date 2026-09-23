# API概览

## API标准及多语言预置SDK

本产品（`bailian/2023-12-29`）的OpenAPI采用[ROA](https://help.aliyun.com/zh/sdk/product-overview/roa-mechanism)签名风格。我们已经为开发者封装了常见编程语言的SDK，开发者可通过[下载SDK](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29)直接调用本产品OpenAPI而无需关心技术细节。如果现有SDK不能满足使用需求，可通过签名机制进行自签名对接。由于自签名细节非常复杂，需花费 5个工作日左右。因此建议加入我们的服务钉钉群（147535001692），在专家指导下进行签名对接。

在使用API前，您需要准备好身份账号及访问密钥（AccessKey），才能有效通过客户端工具（SDK、CLI等）访问API。细节请参见[获取AccessKey](https://help.aliyun.com/zh/ram/user-guide/create-an-accesskey-pair)。

## 自定义签名场景

若您的业务场景有特殊需求，需通过自签名方式对接 API，建议优先咨询我们的技术支持团队（服务钉钉群：147535001692），获取专业指导以确保高效接入。

## 账号与安全准备

阿里云账号具备对所有资源的完全管理权限。一旦 AccessKey 泄露，所有相关资源都将面临未经授权访问的风险。为确保安全，建议创建一个仅具备 API 访问权限的[RAM用户](https://help.aliyun.com/zh/ram/user-guide/create-a-ram-user)并配置其 AccessKey，同时基于最小权限原则 (PoLP) 配置 RAM 策略。仅在明确需要阿里云账号权限的特定场景下，才使用阿里云账号。

## 数据连接（原应用数据）

API

标题

API概述

[AddCategory](raw/_short/api-bailian-2023-12-29-addcategory-e2fe0e0435ed504e.md)

新增类目

在指定的业务空间中创建一个类目，用于分类和管理文件。每个业务空间最多创建500个类目。

[ListCategory](raw/_short/api-bailian-2023-12-29-listcategory-2521532ef3e828b3.md)

类目列表

获取指定业务空间下一个或多个类目的详细信息。

[DeleteCategory](raw/_short/api-bailian-2023-12-29-deletecategory-9838436bd2db3113.md)

删除类目

永久性删除指定的类目。

[ApplyFileUploadLease](raw/_short/api-bailian-2023-12-29-applyfileuploadlease-39e8ca15e0e9561a.md)

申请文件上传租约

请求一个上传租约用于上传知识库文件，或智能体应用会话交互的文件。

[AddFile](raw/_short/api-bailian-2023-12-29-addfile-8c254b3500bc50bc.md)

添加文件

将存储于阿里云百炼临时存储空间内的文件导入至阿里云百炼数据连接（原应用数据）。

[AddFilesFromAuthorizedOss](raw/_short/api-bailian-2023-12-29-addfilesfromauthorizedoss-879556d685a301b3.md)

从已授权OSS Bucket中导入文件

将已授权OSS Bucket中的文件导入阿里云百炼应用数据中。

[ListFile](raw/_short/api-bailian-2023-12-29-listfile-360209e3a2479f14.md)

文件列表

获取指定类目下一个或多个文档的详细信息。

[DescribeFile](raw/_short/api-bailian-2023-12-29-describefile-020886c28a208bf2.md)

查询文件状态

查询应用数据中文件的基本信息，包括文件名称、类型、状态等。

[UpdateFileTag](raw/_short/api-bailian-2023-12-29-updatefiletag-f84d2af6a45d6553.md)

更新文件标签

更新指定文件标签。

[BatchUpdateFileTag](raw/_short/api-bailian-2023-12-29-batchupdatefiletag-34a8f009de66cb8b.md)

批量更新文档标签

该接口用于批量更新数据连接中的文档标签。

[DeleteFile](raw/_short/api-bailian-2023-12-29-deletefile-7e0409a458195fe2.md)

删除文件

永久删除应用数据中的指定文件。不支持通过API删除数据表，详见下方接口说明。

[DeleteFiles](raw/_short/api-bailian-2023-12-29-deletefiles-96ef0815114e4e37.md)

批量删除文件

批量删除文件

[GetParseSettings](raw/_short/api-bailian-2023-12-29-getparsesettings-522514560c54f49f.md)

获取类目解析设置

查询指定类目的数据解析设置。

[GetAvailableParserTypes](raw/_short/api-bailian-2023-12-29-getavailableparsertypes-09561c4e0fb505d5.md)

获取文件支持的解析器类型

根据输入的文件类型（文件扩展名），获取所有支持的解析器类型列表。

[ChangeParseSetting](raw/_short/api-bailian-2023-12-29-changeparsesetting-59a7c69675f499ad.md)

修改类目解析设置

配置特定文件类型的解析方式。例如，为 .pdf 文件指定使用大模型文档解析，为 .jpg 文件指定使用Qwen VL解析。

[AddTable](raw/_short/api-bailian-2023-12-29-addtable-6726351659db288d.md)

添加表格

为表格数据连接器添加表格。

[UpdateTableFromAuthorizedOss](raw/_short/api-bailian-2023-12-29-updatetablefromauthorized-d7436828bcf51602.md)

从已授权OSS Bucket中选择文件更新表格

使用已授权OSS Bucket中的文件更新阿里云百炼数据连接中表格连接器中的表格。

[AddConnector](raw/_short/api-bailian-2023-12-29-addconnector-7a3c9650409710fe.md)

新增连接器

创建连接器，当前接口仅支持创建文件类型连接器。

[GetConnector](raw/_short/api-bailian-2023-12-29-getconnector-cb2e485a0efd52f7.md)

获取连接器信息

获取连接器信息。当前接口仅支持获取文件连接器信息。

DeleteConnector

删除连接器

删除连接器

[UpdateConnector](raw/_short/api-bailian-2023-12-29-updateconnector-6a24905a7d201597.md)

编辑连接器

编辑连接器

## 知识库

API

标题

API概述

[CreateIndex](raw/_short/api-bailian-2023-12-29-createindex-8bc613c75f8af371.md)

创建知识库

使用此API可创建两类知识库：基于文档或音视频的非结构化知识库，以及用于数据查询或图片问答的结构化知识库。

[GetIndexJobStatus](raw/_short/api-bailian-2023-12-29-getindexjobstatus-1e88b6ccfffe0fe4.md)

查询知识库创建任务状态

查询指定的知识库创建任务或知识库追加任务的当前状态。

[SubmitIndexJob](raw/_short/api-bailian-2023-12-29-submitindexjob-63b38294171880d4.md)

提交知识库创建任务

提交指定的 CreateIndex 任务以完成知识库创建。

[SubmitIndexAddDocumentsJob](raw/_short/api-bailian-2023-12-29-submitindexadddocumentsjo-ec4f5cf285e2c447.md)

提交知识库追加任务

向指定知识库中追加导入已解析的文件。

[Retrieve](raw/_short/api-bailian-2023-12-29-retrieve-c8e6b8d718a30a84.md)

检索知识库

在指定的知识库中检索信息。

[ListIndexDocuments](raw/_short/api-bailian-2023-12-29-listindexdocuments-9f0db0388c421903.md)

查询知识库下的文件列表

获取指定知识库中的文件，以及它们的概要信息。

[ListIndexFileDetails](raw/_short/api-bailian-2023-12-29-listindexfiledetails-0e2036d0ef0d8fe8.md)

查询知识库下的文件详情

获取指定知识库中的文件，以及它们的详细信息。

[UpdateIndex](raw/_short/api-bailian-2023-12-29-updateindex-551997e1d335e340.md)

更新知识库

更新指定知识库的部分配置。

[DeleteIndexDocument](raw/_short/api-bailian-2023-12-29-deleteindexdocument-0792a83f5a741348.md)

删除知识库下的文件

永久删除指定知识库中的文件。

[ListIndices](raw/_short/api-bailian-2023-12-29-listindices-c555173be752eaaf.md)

查询知识库列表

获取指定业务空间下知识库列表。

[DeleteIndex](raw/_short/api-bailian-2023-12-29-deleteindex-500502bd6df1c49c.md)

删除知识库

永久性删除指定的知识库。

[ListChunks](raw/_short/api-bailian-2023-12-29-listchunks-30a6c87b93a583c6.md)

查询索引下的分片列表

查看文本切片列表及信息。

[AddChunk](raw/_short/api-bailian-2023-12-29-addchunk-1607bcddf6713fd9.md)

新增切片

使用此API可为文档搜索类（document）、数据查询类（table）、图片问答类（image）知识库添加切片。

[UpdateChunk](raw/_short/api-bailian-2023-12-29-updatechunk-589b46fcc24261f8.md)

修改切片

修改知识库中指定文本切片的内容（content）和标题（title），并设置是否参与知识库检索。

[DeleteChunk](raw/_short/api-bailian-2023-12-29-deletechunk-d249422088735d90.md)

删除切片

删除知识库中的指定文本切片，被删的文本切片将无法被检索和召回。

[GetIndexMonitor](raw/_short/api-bailian-2023-12-29-getindexmonitor-3a609181d5c9c034.md)

获取知识库监控数据

调用GetIndexMonitor接口，查询指定知识库在特定时间范围内的监控数据。这些数据对于性能分析、容量规划和成本管理至关重要。 监控数据主要包含两大维度： 存储监控：获取知识库的索引存储限额和当前使用量。 检索（QPS）监控：获取查询时间段内总的及按时间窗口细分的检索性能指标，包括QPS峰值、总请求数、平均QPS，并细分为成功、失败和被限流的请求。

## Prompt工程

API

标题

API概述

[CreatePromptTemplate](raw/_short/api-bailian-2023-12-29-createprompttemplate-1194e536beb0529a.md)

创建Prompt模板

创建Prompt模板。

[GetPromptTemplate](raw/_short/api-bailian-2023-12-29-getprompttemplate-584c357dd7cb48d6.md)

获取Prompt模板

基于模板Id获取Prompt模板。

[UpdatePromptTemplate](raw/_short/api-bailian-2023-12-29-updateprompttemplate-519fb4af5ea50522.md)

更新Prompt模板

基于模板Id增量更新Prompt模板。

[DeletePromptTemplate](raw/_short/api-bailian-2023-12-29-deleteprompttemplate-b441fa1b9c777b81.md)

删除Prompt模板

基于模板Id删除Prompt模板。

[ListPromptTemplates](raw/_short/api-bailian-2023-12-29-listprompttemplates-ab5ba5362e93cfcd.md)

获取Prompt模板列表

获取Prompt模板列表。

## 其他

API

标题

API概述

长期记忆（旧）

长期记忆（旧）

[CreateMemory](raw/_short/api-bailian-2023-12-29-creatememory-b8e710cdd3512a87.md)

创建长期记忆体

创建一个长期记忆体。

[GetMemory](raw/_short/api-bailian-2023-12-29-getmemory-c25d3815c2b70f40.md)

获取长期记忆体

获取指定长期记忆体的描述信息。

[UpdateMemory](raw/_short/api-bailian-2023-12-29-updatememory-b5fdfa9f480e94bb.md)

更新长期记忆体

更新指定长期记忆体的描述信息。

[DeleteMemory](raw/_short/api-bailian-2023-12-29-deletememory-ffa5f461924db8f6.md)

删除长期记忆体

永久性删除指定的长期记忆体。

[ListMemories](raw/_short/api-bailian-2023-12-29-listmemories-3411c870627f174b.md)

获取长期记忆体列表

获取指定业务空间下一个或多个长期记忆体的详细信息。

[CreateMemoryNode](raw/_short/api-bailian-2023-12-29-creatememorynode-c6cd91f25e1f7997.md)

创建记忆片段

创建记忆片段。

[GetMemoryNode](raw/_short/api-bailian-2023-12-29-getmemorynode-59d0d4efa0e86d78.md)

获取记忆片段

获取记忆片段。

[UpdateMemoryNode](raw/_short/api-bailian-2023-12-29-updatememorynode-f2d05378b761b201.md)

更新记忆片段

更新记忆片段。

[DeleteMemoryNode](raw/_short/api-bailian-2023-12-29-deletememorynode-d7919fd53d316466.md)

删除记忆片段

删除记忆片段。

[ListMemoryNodes](raw/_short/api-bailian-2023-12-29-listmemorynodes-4f1cc5232bdc67a5.md)

获取记忆片段列表

获取记忆片段列表。

[GetAlipayTransferStatus](raw/_short/api-bailian-2023-12-29-getalipaytransferstatus-04aa88852762fd85.md)

查询支付宝打赏状态

查询应用中绑定的支付宝钱包的打赏状态。

[GetAlipayUrl](raw/_short/api-bailian-2023-12-29-getalipayurl-e6e9715d5164f74a.md)

获取支付宝打赏URL

获取应用上支付宝的打赏链接。

[ApplyTempStorageLease](raw/_short/api-bailian-2023-12-29-applytempstoragelease-5a38ce0eefc66408.md)

申请临时文件上传许可

该接口用于高代码部署，其他场景暂不支持。用于申请临时文件上传许可，之后需要自己完成文件上传动作。
