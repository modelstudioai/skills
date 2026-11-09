# application component api reference

本 API 参考文档面向开发者，提供百炼平台应用组件（Application Component）的核心 OpenAPI 接口规范，涵盖数据连接（原应用数据）与知识库两大核心能力模块。所有接口均基于 `bailian/2023-12-29` 版本，采用标准 ROA 签名机制，支持通过官方 SDK 或自签名方式调用。开发者需预先配置 RAM 用户权限及业务空间访问授权，方可安全、合规地集成。

## 支持的模型/功能

本组件不直接提供大模型推理能力，而是聚焦于**结构化与非结构化数据的接入、管理与检索增强**，主要功能包括：

- **数据连接（原应用数据）**：支持类目（Category）管理（增删查）、文件（File）全生命周期操作（上传租约申请、导入、列表、详情、标签更新、批量删除）、OSS 授权导入、解析器配置（按文件类型指定 DOCMIND / Qwen VL 等解析器）及连接器（Connector）管理。
- **知识库（Knowledge Base）**：支持两类知识库——`unstructured`（文档/音视频搜索）与 `structured`（数据查询/图片问答）。覆盖完整生命周期：创建（`CreateIndex`）、提交构建任务（`SubmitIndexJob`）、追加文件（`SubmitIndexAddDocumentsJob`）、检索（`Retrieve`）、文件与切片（Chunk）的增删改查（`ListIndexDocuments`, `AddChunk`, `UpdateChunk`, `DeleteChunk`）、监控（`GetIndexMonitor`）及删除（`DeleteIndex`）。

> **注意**：文档 39（`AddChunk`）与文档 40（`UpdateChunk`）在适用范围上存在矛盾。文档 39 明确说明 `AddChunk` 支持 `document`/`table`/`image` 三类知识库，而文档 40 则强调 `UpdateChunk` “仅支持文档搜索类知识库，不支持数据查询和图片问答类知识库”。该差异表明切片级写入能力在不同知识库类型间尚未完全对齐，实际开发中请以 [AddChunk](../../raw/_short/api-bailian-2023-12-29-addchunk-1607bcddf6713fd9.md) 的描述为准，并在更新前确认知识库类型。

## 关键参数

- **`WorkspaceId`**：所有接口的必需路径参数，标识业务空间。必须通过控制台获取，当前无 API 枚举能力。示例值：`llm-3z7uw7fwz0vexxxx`。
- **`CategoryId` / `FileId` / `IndexId` / `ChunkId`**：资源标识符，均由上游接口（如 `AddCategory`, `AddFile`, `CreateIndex`, `ListChunks`）返回，不可自行构造。
- **`Parser`**：文件解析器类型，关键于 `AddFile` 和 `ChangeParseSetting` 接口。有效值包括 `AUTO_SELECT`, `DOCMIND`, `DOCMIND_DIGITAL`, `DOCMIND_LLM_VERSION`, `DASH_QWEN_VL_PARSER`, `DOCMIND_LLM_VERSION_MEDIA`。具体支持关系需结合 [GetAvailableParserTypes](../../raw/_short/api-bailian-2023-12-29-getavailableparsertypes-09561c4e0fb505d5.md) 接口动态查询。
- **分页参数**：`List*` 类接口普遍支持 `NextToken`（游标式）或 `PageNumber`/`PageSize`（页码式）分页。`MaxResults`（最大返回数）默认为 20，上限 200；`PageSize` 默认为 10，无硬性上限。

## 使用方式

1. **环境准备**：
   - 获取 AccessKey（推荐使用最小权限 RAM 子账号，而非主账号），参考 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md) 中的安全最佳实践。
   - 根据地域选择服务接入点，例如北京地域公网地址为 `bailian.cn-beijing.aliyuncs.com`（见 [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)）。
2. **权限配置**：
   - 为 RAM 用户附加 `AliyunBailianDataFullAccess`（读写）或 `AliyunBailianDataReadOnlyAccess`（只读）策略。
   - 确保该用户已加入目标 `WorkspaceId` 对应的业务空间。
3. **典型流程（知识库构建）**：
   - 创建类目 → `AddCategory`
   - 申请上传租约 → `ApplyFileUploadLease`
   - 上传并解析文件 → `AddFile`
   - 创建知识库 → `CreateIndex`
   - 提交构建任务 → `SubmitIndexJob`
   - （可选）追加文件 → `SubmitIndexAddDocumentsJob`
   - 检索知识 → `Retrieve`

## 限制和注意事项

- **限流策略**：各接口有独立限流阈值，常见为 `5` 或 `10` 次/秒。`ListIndexDocuments` 较宽松（`15` 次/秒）。超限将返回 `429` 错误，需实现指数退避重试。
- **幂等性**：`List*`, `Describe*`, `Get*`, `Delete*`（除 `DeleteFiles` 外）及 `Update*` 类接口多为幂等；`Add*`, `Submit*`, `Apply*` 类接口通常不幂等，重复调用可能产生冗余资源。
- **数据一致性**：
  - `DeleteFiles` 删除的是“应用数据”中的源文件，不影响已构建的知识库索引；反之，`DeleteIndexDocument` 删除的是知识库索引中的文件，源文件仍保留在应用数据中。
  - `DeleteIndex` 不会级联删除其关联的 `AddFile` 文件，二者生命周期独立。
- **功能边界**：
  - 所有 `AddTable`/`UpdateTableFromAuthorizedOss` 等表格操作仅适用于 `structured` 知识库，且不支持通过 API 新增或删除数据表（见 [AddCategory](../../raw/_short/api-bailian-2023-12-29-addcategory-e2fe0e0435ed504e.md) 和 [DeleteFiles](../../raw/_short/api-bailian-2023-12-29-deletefiles-96ef0815114e4e37.md) 的明确说明）。
  - `Retrieve` 接口响应延迟较高，务必设置合理的客户端超时（建议 ≥ 30s）与重试策略。

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
- [UpdateFileTag](../../raw/_short/api-bailian-2023-12-29-updatefiletag-f84d2af6a45d6553.md)
- [BatchUpdateFileTag](../../raw/_short/api-bailian-2023-12-29-batchupdatefiletag-34a8f009de66cb8b.md)
- [DeleteFiles](../../raw/_short/api-bailian-2023-12-29-deletefiles-96ef0815114e4e37.md)
- [GetParseSettings - 获取类目解析设置](../../raw/_short/api-bailian-2023-12-29-getparsesettings-522514560c54f49f.md)
- [DeleteFile](../../raw/_short/api-bailian-2023-12-29-deletefile-7e0409a458195fe2.md)
- [ChangeParseSetting](../../raw/_short/api-bailian-2023-12-29-changeparsesetting-59a7c69675f499ad.md)
- [AddTable](../../raw/_short/api-bailian-2023-12-29-addtable-6726351659db288d.md)
- [GetAvailableParserTypes - 获取文件支持的解析器类型](../../raw/_short/api-bailian-2023-12-29-getavailableparsertypes-09561c4e0fb505d5.md)
- [UpdateTableFromAuthorizedOss](../../raw/_short/api-bailian-2023-12-29-updatetablefromauthorized-d7436828bcf51602.md)
- [GetConnector](../../raw/_short/api-bailian-2023-12-29-getconnector-cb2e485a0efd52f7.md)
- [AddConnector](../../raw/_short/api-bailian-2023-12-29-addconnector-7a3c9650409710fe.md)
- [UpdateConnector](../../raw/_short/api-bailian-2023-12-29-updateconnector-6a24905a7d201597.md)
- [知识库](../../raw/_short/api-bailian-2023-12-29-dir-knowledge-base-f6f202ad9694348f.md)
- [CreateIndex - 创建知识库](../../raw/_short/api-bailian-2023-12-29-createindex-8bc613c75f8af371.md)
- [GetIndexJobStatus - 查询知识库创建或追加任务状态](../../raw/_short/api-bailian-2023-12-29-getindexjobstatus-1e88b6ccfffe0fe4.md)
- [SubmitIndexJob - 提交知识库创建任务](../../raw/_short/api-bailian-2023-12-29-submitindexjob-63b38294171880d4.md)
- [SubmitIndexAddDocumentsJob - 提交知识库文件追加任务](../../raw/_short/api-bailian-2023-12-29-submitindexadddocumentsjo-ec4f5cf285e2c447.md)
- [Retrieve - 检索知识库](../../raw/_short/api-bailian-2023-12-29-retrieve-c8e6b8d718a30a84.md)
- [ListIndexDocuments - 查询知识库文件列表](../../raw/_short/api-bailian-2023-12-29-listindexdocuments-9f0db0388c421903.md)
- [ListIndexFileDetails - 查询知识库文件详情](../../raw/_short/api-bailian-2023-12-29-listindexfiledetails-0e2036d0ef0d8fe8.md)
- [UpdateIndex - 更新知识库](../../raw/_short/api-bailian-2023-12-29-updateindex-551997e1d335e340.md)
- [DeleteIndexDocument - 删除知识库下的文件](../../raw/_short/api-bailian-2023-12-29-deleteindexdocument-0792a83f5a741348.md)
- [ListIndices - 查询知识库列表](../../raw/_short/api-bailian-2023-12-29-listindices-c555173be752eaaf.md)
- [DeleteIndex - 删除知识库](../../raw/_short/api-bailian-2023-12-29-deleteindex-500502bd6df1c49c.md)
- [ListChunks - 查询索引下的分片列表](../../raw/_short/api-bailian-2023-12-29-listchunks-30a6c87b93a583c6.md)
- [AddChunk - 新增切片](../../raw/_short/api-bailian-2023-12-29-addchunk-1607bcddf6713fd9.md)
- [UpdateChunk - 修改切片](../../raw/_short/api-bailian-2023-12-29-updatechunk-589b46fcc24261f8.md)
- [DeleteChunk - 删除切片](../../raw/_short/api-bailian-2023-12-29-deletechunk-d249422088735d90.md)
- [GetIndexMonitor - 获取知识库监控数据](../../raw/_short/api-bailian-2023-12-29-getindexmonitor-3a609181d5c9c034.md)
- [Prompt 模板](../../raw/_short/api-bailian-2023-12-29-dir-prompt-engineering-11ee962a5f5d5d1e.md)
- [CreatePromptTemplate - 创建Prompt模板](../../raw/_short/api-bailian-2023-12-29-createprompttemplate-1194e536beb0529a.md)
- [UpdatePromptTemplate - 更新Prompt模板](../../raw/_short/api-bailian-2023-12-29-updateprompttemplate-519fb4af5ea50522.md)
- [GetPromptTemplate - 获取Prompt模板](../../raw/_short/api-bailian-2023-12-29-getprompttemplate-584c357dd7cb48d6.md)
- [DeletePromptTemplate - 删除Prompt模板](../../raw/_short/api-bailian-2023-12-29-deleteprompttemplate-b441fa1b9c777b81.md)
- [ListPromptTemplates - 获取Prompt模板列表](../../raw/_short/api-bailian-2023-12-29-listprompttemplates-ab5ba5362e93cfcd.md)
- [GetAlipayTransferStatus - 查询支付宝打赏状态](../../raw/_short/api-bailian-2023-12-29-getalipaytransferstatus-04aa88852762fd85.md)
- [GetAlipayUrl - 获取支付宝打赏URL](../../raw/_short/api-bailian-2023-12-29-getalipayurl-e6e9715d5164f74a.md)
- [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md)
- [ApplyTempStorageLease - 申请临时文件上传许可](../../raw/_short/api-bailian-2023-12-29-applytempstoragelease-5a38ce0eefc66408.md)
- [其他](../../raw/_short/api-bailian-2023-12-29-dir-others-b9c3a16db11771f5.md)


