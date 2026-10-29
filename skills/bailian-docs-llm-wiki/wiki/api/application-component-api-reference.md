# application component api reference

本 API 参考文档面向开发者，完整描述百炼平台 `application component`（应用组件）层提供的核心 OpenAPI 接口能力，覆盖数据连接（原应用数据）、知识库、[Prompt 工程](../concepts/prompt-engineering.md)三大功能域。所有接口均基于 ROA 签名机制，推荐使用官方 SDK 调用以规避签名复杂性。接口权限通过 RAM 策略精细控制，需为子账号授予对应 `sfm:*` 操作权限。

## 支持的模型/功能

API 当前不直接暴露大语言模型调用能力（该能力归属 `model-api-reference` 分类），而是聚焦于**应用构建基础设施**，提供以下三类核心功能：

- **数据连接（原应用数据）**：管理非结构化文件与结构化表格的生命周期，包括类目（Category）管理（[AddCategory](../../raw/_short/api-bailian-2023-12-29-addcategory-e2fe0e0435ed504e.md)、[ListCategory](../../raw/_short/api-bailian-2023-12-29-listcategory-2521532ef3e828b3.md)、[DeleteCategory](../../raw/_short/api-bailian-2023-12-29-deletecategory-9838436bd2db3113.md)）、文件上传与元数据操作（[ApplyFileUploadLease](../../raw/_short/api-bailian-2023-12-29-applyfileuploadlease-39e8ca15e0e9561a.md)、[AddFile](../../raw/_short/api-bailian-2023-12-29-addfile-8c254b3500bc50bc.md)、[ListFile](../../raw/_short/api-bailian-2023-12-29-listfile-360209e3a2479f14.md)）、以及连接器（Connector）管理（[AddConnector](../../raw/_short/api-bailian-2023-12-29-addconnector-7a3c9650409710fe.md)、[GetConnector](../../raw/_short/api-bailian-2023-12-29-getconnector-cb2e485a0efd52f7.md)）。
- **知识库（Knowledge Base）**：支持创建（[CreateIndex](../../raw/_short/api-bailian-2023-12-29-createindex-8bc613c75f8af371.md)）、查询（[ListIndices](../../raw/_short/api-bailian-2023-12-29-listindices-c555173be752eaaf.md)）、更新（[UpdateIndex](../../raw/_short/api-bailian-2023-12-29-updateindex-551997e1d335e340.md)）、删除（[DeleteIndex](../../raw/_short/api-bailian-2023-12-29-deleteindex-500502bd6df1c49c.md)）全生命周期管理；支持向知识库中添加、检索、删除文档切片（Chunk）（[AddChunk](../../raw/_short/api-bailian-2023-12-29-addchunk-1607bcddf6713fd9.md)、[ListChunks](../../raw/_short/api-bailian-2023-12-29-listchunks-30a6c87b93a583c6.md)、[UpdateChunk](../../raw/_short/api-bailian-2023-12-29-updatechunk-589b46fcc24261f8.md)、[DeleteChunk](../../raw/_short/api-bailian-2023-12-29-deletechunk-d249422088735d90.md)）；并提供监控（[GetIndexMonitor](../../raw/_short/api-bailian-2023-12-29-getindexmonitor-3a609181d5c9c034.md)）与诊断能力。
- **[Prompt 工程](../concepts/prompt-engineering.md)**：支持 Prompt 模板的创建、管理与复用（[CreatePromptTemplate](../../raw/_short/api-bailian-2023-12-29-createprompttemplate-1194e536beb0529a.md)）。

> **注意**：文档 1 中提及“不支持通过 API 新增数据表”，而文档 19 明确提供了 [AddTable](../../raw/_short/api-bailian-2023-12-29-addtable-6726351659db288d.md) 接口。经交叉验证，`AddTable` 是真实可用的结构化数据接入能力，文档 1 的说明已过时，应以文档 19 为准。

## 关键参数

- **`WorkspaceId`（业务空间 ID）**：几乎所有接口的必需路径参数，用于标识资源所属的隔离工作空间。获取方式请参见[如何使用业务空间](https://help.aliyun.com/zh/model-studio/use-workspace)。
- **`CategoryId` / `FileId` / `IndexId` / `ConnectorId`**：各类资源的唯一标识符，通常由上游接口（如 `AddCategory`, `AddFile`, `CreateIndex`, `AddConnector`）返回，后续操作必须传入。
- **`Parser`（解析器类型）**：在 `AddFile` 和 `ChangeParseSetting` 等接口中指定，决定文件内容的解析策略。有效值包括 `DOCMIND`, `DOCMIND_DIGITAL`, `DOCMIND_LLM_VERSION`, `DASH_QWEN_VL_PARSER`, `AUTO_SELECT` 等，具体支持列表可通过 [GetAvailableParserTypes](../../raw/_short/api-bailian-2023-12-29-getavailableparsertypes-09561c4e0fb505d5.md) 查询。
- **分页参数**：`List*` 类接口普遍支持 `MaxResults`/`PageSize`（每页条数）和 `NextToken`/`PageNumber`（分页凭证或页码）进行分页查询。
- **限流参数**：所有接口均有明确的 QPS 限制（如 `AddCategory` 为 5 次/秒，`Retrieve` 为 15 次/秒），详见各接口文档的“限流说明”章节。

## 使用方式

1.  **环境准备**：
    - 获取阿里云 AccessKey（推荐使用 RAM 子账号并遵循最小权限原则配置 `AliyunBailianDataFullAccess` 或更细粒度策略）。
    - 根据地域选择服务接入点，例如华北2（北京）的公网地址为 `bailian.cn-beijing.aliyuncs.com`（[服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)）。
2.  **调用流程（以构建知识库为例）**：
    - **准备数据**：调用 `AddCategory` 创建类目 → `ApplyFileUploadLease` 申请租约 → `AddFile` 上传文件。
    - **创建知识库**：调用 `CreateIndex` 初始化知识库 → `SubmitIndexJob` 提交创建任务。
    - **监控状态**：调用 `GetIndexJobStatus` 查询任务进度，直至状态为 `FINISH`。
    - **使用知识库**：调用 `Retrieve` 进行语义检索，或在智能体应用中通过 `rag_options` 配置 `IndexId`。
3.  **开发工具**：
    - **首选 SDK**：强烈推荐使用 [阿里云百炼 SDK](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29)，它已封装签名逻辑并提供各语言示例。
    - **调试工具**：可直接在 [OpenAPI Explorer](https://api.aliyun.com/api/bailian/2023-12-29) 中调试任意接口，无需手动签名。

## 限制和注意事项

- **幂等性**：并非所有接口都具备幂等性。`AddCategory`, `ApplyFileUploadLease`, `AddFile`, `AddTable`, `SubmitIndexJob`, `SubmitIndexAddDocumentsJob` 等接口不具备幂等性，重复调用可能导致重复资源创建；而 `List*`, `Describe*`, `Get*`, `Delete*`, `Update*` 等多数查询与变更操作具备幂等性。务必在代码中根据接口文档明确标注处理。
- **资源依赖与顺序**：知识库相关操作有严格依赖链。例如，`SubmitIndexJob` 必须在 `CreateIndex` 之后调用；`SubmitIndexAddDocumentsJob` 要求文件已通过 `AddFile` 导入且知识库已创建完成；`DeleteIndexDocument` 仅能删除状态为 `FINISH` 或 `INSERT_ERROR` 的文件。
- **安全与权限**：RAM 权限策略是访问控制的核心。所有 `sfm:*` 操作均需显式授权，且部分操作（如 `DeleteIndex`）要求知识库先解除与应用的关联（此操作目前仅支持控制台）。
- **功能边界**：
    - 不支持通过 API 删除数据表（仅支持删除文件）。
    - `Retrieve` 接口的 OpenAPI 形式（`POST /{WorkspaceId}/index/retrieve`）与 Spring AI Alibaba SDK 使用的 DashScope Pipeline 路径不同，二者不可混用。
    - `CreatePromptTemplate` 暂不支持文生图类 Prompt 模板。
- **性能与成本**：`GetIndexMonitor` 接口可用于分析知识库的存储用量与 QPS 峰值，对容量规划至关重要；高频调用 `ListChunks` 或 `Retrieve` 等接口需关注其限流阈值，避免请求被拒绝。

## 来源文档

- [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)
- [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)
- [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)
- [API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md)
- [数据连接（原应用数据）](../../raw/_short/api-bailian-2023-12-29-dir-data-connection-origi-a1f7f2601bd6f7cf.md)
- [AddCategory](../../raw/_short/api-bailian-2023-12-29-addcategory-e2fe0e0435ed504e.md)
- [ListCategory](../../raw/_short/api-bailian-2023-12-29-listcategory-2521532ef3e828b3.md)
- [DeleteCategory - 删除类目](../../raw/_short/api-bailian-2023-12-29-deletecategory-9838436bd2db3113.md)
- [ApplyFileUploadLease](../../raw/_short/api-bailian-2023-12-29-applyfileuploadlease-39e8ca15e0e9561a.md)
- [AddFile](../../raw/_short/api-bailian-2023-12-29-addfile-8c254b3500bc50bc.md)
- [AddFilesFromAuthorizedOss](../../raw/_short/api-bailian-2023-12-29-addfilesfromauthorizedoss-879556d685a301b3.md)
- [ListFile](../../raw/_short/api-bailian-2023-12-29-listfile-360209e3a2479f14.md)
- [DescribeFile](../../raw/_short/api-bailian-2023-12-29-describefile-020886c28a208bf2.md)
- [BatchUpdateFileTag](../../raw/_short/api-bailian-2023-12-29-batchupdatefiletag-34a8f009de66cb8b.md)
- [DeleteFile](../../raw/_short/api-bailian-2023-12-29-deletefile-7e0409a458195fe2.md)
- [DeleteFiles](../../raw/_short/api-bailian-2023-12-29-deletefiles-96ef0815114e4e37.md)
- [GetParseSettings - 获取类目解析设置](../../raw/_short/api-bailian-2023-12-29-getparsesettings-522514560c54f49f.md)
- [GetAvailableParserTypes - 获取文件支持的解析器类型](../../raw/_short/api-bailian-2023-12-29-getavailableparsertypes-09561c4e0fb505d5.md)
- [AddTable](../../raw/_short/api-bailian-2023-12-29-addtable-6726351659db288d.md)
- [UpdateFileTag](../../raw/_short/api-bailian-2023-12-29-updatefiletag-f84d2af6a45d6553.md)
- [AddConnector](../../raw/_short/api-bailian-2023-12-29-addconnector-7a3c9650409710fe.md)
- [GetConnector](../../raw/_short/api-bailian-2023-12-29-getconnector-cb2e485a0efd52f7.md)
- [ChangeParseSetting](../../raw/_short/api-bailian-2023-12-29-changeparsesetting-59a7c69675f499ad.md)
- [UpdateConnector](../../raw/_short/api-bailian-2023-12-29-updateconnector-6a24905a7d201597.md)
- [CreateIndex](../../raw/_short/api-bailian-2023-12-29-createindex-8bc613c75f8af371.md)
- [GetIndexJobStatus](../../raw/_short/api-bailian-2023-12-29-getindexjobstatus-1e88b6ccfffe0fe4.md)
- [SubmitIndexJob - 提交知识库创建任务](../../raw/_short/api-bailian-2023-12-29-submitindexjob-63b38294171880d4.md)
- [SubmitIndexAddDocumentsJob](../../raw/_short/api-bailian-2023-12-29-submitindexadddocumentsjo-ec4f5cf285e2c447.md)
- [Retrieve](../../raw/_short/api-bailian-2023-12-29-retrieve-c8e6b8d718a30a84.md)
- [知识库](../../raw/_short/api-bailian-2023-12-29-dir-knowledge-base-f6f202ad9694348f.md)
- [ListIndexDocuments](../../raw/_short/api-bailian-2023-12-29-listindexdocuments-9f0db0388c421903.md)
- [UpdateIndex - 更新知识库](../../raw/_short/api-bailian-2023-12-29-updateindex-551997e1d335e340.md)
- [DeleteIndexDocument - 删除知识库下的文件](../../raw/_short/api-bailian-2023-12-29-deleteindexdocument-0792a83f5a741348.md)
- [DeleteIndex - 删除知识库](../../raw/_short/api-bailian-2023-12-29-deleteindex-500502bd6df1c49c.md)
- [ListIndices](../../raw/_short/api-bailian-2023-12-29-listindices-c555173be752eaaf.md)
- [ListChunks - 查询索引下的分片列表](../../raw/_short/api-bailian-2023-12-29-listchunks-30a6c87b93a583c6.md)
- [AddChunk](../../raw/_short/api-bailian-2023-12-29-addchunk-1607bcddf6713fd9.md)
- [ListIndexFileDetails](../../raw/_short/api-bailian-2023-12-29-listindexfiledetails-0e2036d0ef0d8fe8.md)
- [UpdateChunk - 修改切片](../../raw/_short/api-bailian-2023-12-29-updatechunk-589b46fcc24261f8.md)
- [DeleteChunk - 删除切片](../../raw/_short/api-bailian-2023-12-29-deletechunk-d249422088735d90.md)
- [GetIndexMonitor - 获取知识库监控数据](../../raw/_short/api-bailian-2023-12-29-getindexmonitor-3a609181d5c9c034.md)
- [CreatePromptTemplate - 创建Prompt模板](../../raw/_short/api-bailian-2023-12-29-createprompttemplate-1194e536beb0529a.md)
- [Prompt 模板](../../raw/_short/api-bailian-2023-12-29-dir-prompt-engineering-11ee962a5f5d5d1e.md)
- [GetPromptTemplate - 获取Prompt模板](../../raw/_short/api-bailian-2023-12-29-getprompttemplate-584c357dd7cb48d6.md)
- [UpdatePromptTemplate - 更新Prompt模板](../../raw/_short/api-bailian-2023-12-29-updateprompttemplate-519fb4af5ea50522.md)
- [DeletePromptTemplate - 删除Prompt模板](../../raw/_short/api-bailian-2023-12-29-deleteprompttemplate-b441fa1b9c777b81.md)
- [ListPromptTemplates - 获取Prompt模板列表](../../raw/_short/api-bailian-2023-12-29-listprompttemplates-ab5ba5362e93cfcd.md)
- [其他](../../raw/_short/api-bailian-2023-12-29-dir-others-b9c3a16db11771f5.md)
- [GetAlipayUrl - 获取支付宝打赏URL](../../raw/_short/api-bailian-2023-12-29-getalipayurl-e6e9715d5164f74a.md)
- [ApplyTempStorageLease - 申请临时文件上传许可](../../raw/_short/api-bailian-2023-12-29-applytempstoragelease-5a38ce0eefc66408.md)
- [GetAlipayTransferStatus - 查询支付宝打赏状态](../../raw/_short/api-bailian-2023-12-29-getalipaytransferstatus-04aa88852762fd85.md)
- [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md)
- [UpdateTableFromAuthorizedOss](../../raw/_short/api-bailian-2023-12-29-updatetablefromauthorized-d7436828bcf51602.md)


