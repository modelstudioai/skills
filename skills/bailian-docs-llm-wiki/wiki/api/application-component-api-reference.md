# application component api reference

本 API 参考文档面向开发者，提供百炼平台应用组件（Application Component）的核心 OpenAPI 接口规范，涵盖数据连接（原应用数据）、知识库、Prompt 模板三大功能模块。所有接口均基于 `bailian/2023-12-29` 版本，采用标准 ROA 签名机制，支持通过官方 SDK 快速集成。开发者需预先配置 RAM 用户权限及业务空间访问授权。

## 支持的模型/功能

当前 API 覆盖以下核心能力模块：

- **数据连接（原应用数据）**：提供类目管理（`AddCategory`、`ListCategory`、`DeleteCategory`）、文件全生命周期操作（`ApplyFileUploadLease`、`AddFile`、`ListFile`、`DescribeFile`、`DeleteFile`）、批量标签管理（`UpdateFileTag`、`BatchUpdateFileTag`）、解析器配置（`GetParseSettings`、`ChangeParseSetting`、`GetAvailableParserTypes`）及 OSS 数据导入（`AddFilesFromAuthorizedOss`、`UpdateTableFromAuthorizedOss`）。注意：**不支持通过 API 新增或删除数据表**，该操作仅限控制台完成 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)。
- **知识库**：支持知识库创建与管理（`CreateIndex`、`SubmitIndexJob`、`UpdateIndex`、`DeleteIndex`）、文档导入与状态查询（`SubmitIndexAddDocumentsJob`、`ListIndexDocuments`、`ListIndexFileDetails`）、检索（`Retrieve`）、分片管理（`ListChunks`、`DeleteChunk`）及监控（`GetIndexMonitor`）。其中，`DeleteIndexDocument` 用于删除知识库内文件，但**不会影响应用数据中已存在的原始文件** [DeleteIndexDocument - 删除知识库下的文件](../../raw/_short/api-bailian-2023-12-29-deleteindexdocument-0792a83f5a741348.md)。
- **Prompt 模板**：提供完整的 Prompt 模板 CRUD 能力（`CreatePromptTemplate`、`GetPromptTemplate`、`UpdatePromptTemplate`、`DeletePromptTemplate`、`ListPromptTemplates`），支持变量注入与模板复用。**暂不支持文生图类 Prompt 模板的创建** [CreatePromptTemplate - 创建Prompt模板](../../raw/_short/api-bailian-2023-12-29-createprompttemplate-1194e536beb0529a.md)。

> **注意**：文档 31 (`ListIndexDocuments`) 和文档 32 (`ListIndexFileDetails`) 在授权信息中均引用了 `sfm:ListIndexFiles` 权限点，但文档 32 的请求语法为 `POST /{WorkspaceId}/index/list_index_file_detail HTTP/1.1`，而文档 31 为 `GET /{WorkspaceId}/index/list_index_documents HTTP/1.1`，二者路径、方法及返回结构均不同，属两个独立接口，非矛盾信息。

## 关键参数

- **通用路径参数**：几乎所有接口均需 `WorkspaceId`（业务空间 ID），获取方式请参见[如何使用业务空间](https://help.aliyun.com/zh/model-studio/use-workspace)。
- **类目与文件标识**：
  - `CategoryId`：由 `AddCategory` 返回，用于类目及所属文件操作。
  - `FileId`：由 `AddFile` 返回，用于文件详情、更新、删除等操作。
  - `IndexId`：由 `CreateIndex` 返回，用于知识库所有相关操作。
- **分页与过滤**：
  - `MaxResults` / `PageSize`：控制每页返回条目数，最大值通常为 200（如 `ListCategory`）或 10（如 `ListIndexFileDetails`）。
  - `NextToken`：用于分页查询后续页，首次调用无需提供。
  - `DocumentName` / `IndexName`：支持精确匹配，部分接口（如 `ListIndexFileDetails`）支持 `EnableNameLike=true` 开启模糊匹配。
- **解析与检索配置**：
  - `Parser`：在 `AddFile` 中指定，取值如 `AUTO_SELECT`、`DOCMIND` 等；其有效值可通过 `GetAvailableParserTypes` 查询。
  - `DenseSimilarityTopK` / `SparseSimilarityTopK`：在 `Retrieve` 和 `UpdateIndex` 中控制向量与关键词检索的 Top K 数量，二者之和 ≤ 200。

## 使用方式

1. **环境准备**：
   - 获取阿里云 AccessKey（推荐使用最小权限的 RAM 用户，而非主账号）[API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)。
   - 为 RAM 用户授予 `AliyunBailianDataFullAccess`（读写）或 `AliyunBailianDataReadOnlyAccess`（只读）策略，并确保其已加入目标业务空间。
   - 根据地域选择服务接入点，例如北京地域公网地址为 `bailian.cn-beijing.aliyuncs.com` [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)。

2. **典型文件上传流程**：
   - 调用 `ApplyFileUploadLease` 获取临时上传凭证（`LeaseId`）。
   - 使用凭证将文件上传至百炼临时存储。
   - 调用 `AddFile`，传入 `LeaseId`、`CategoryId` 和 `Parser`，完成文件导入与解析。

3. **典型知识库构建流程**：
   - 调用 `CreateIndex` 初始化知识库（返回 `IndexId`）。
   - 调用 `SubmitIndexJob` 提交创建任务（返回 `JobId`）。
   - 调用 `GetIndexJobStatus` 轮询任务状态直至完成。
   - 后续追加文件时，先 `AddFile`，再 `SubmitIndexAddDocumentsJob`。

4. **调试与开发**：
   - 强烈推荐使用 [OpenAPI Explorer](https://api.aliyun.com/api-tools/explorer) 直接调试，免去签名计算。
   - 生产环境务必使用最新版 [阿里云百炼 SDK](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29)，避免手动签名。

## 限制和注意事项

- **限流策略**：各接口有独立 QPS 限制，常见值为 5 次/秒（如 `AddCategory`、`ListCategory`）或 10 次/秒（如 `AddFile`、`Retrieve`）。超出后将返回限流错误，需实现退避重试逻辑。
- **幂等性**：多数查询类接口（如 `ListCategory`、`ListFile`、`GetIndexJobStatus`）具有幂等性；创建类（`AddCategory`、`CreateIndex`）和删除类（`DeleteCategory`、`DeleteIndex`）接口也多为幂等，但 `AddFile`、`ApplyFileUploadLease` 等明确标注“不具备幂等性”，重复调用可能产生冗余资源。
- **安全与权限**：
  - 避免使用阿里云主账号 AccessKey，严格遵循最小权限原则配置 RAM 策略 [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)。
  - `DeleteCategory`、`DeleteFile`、`DeleteIndex`、`DeleteIndexDocument`、`DeleteChunk` 均为**永久性删除且不可恢复**，调用前必须进行业务确认。
- **功能边界**：
  - 所有数据表（结构化数据）的增删改查操作均**不支持 API**，必须通过控制台完成。
  - `DeleteIndexDocument` 仅删除知识库索引中的文件，不影响 `application data` 中的原始文件；反之，`DeleteFile` 仅删除 `application data` 中的文件，不影响已构建的知识库索引。
  - `UpdateConnector` 等接口当前未透出完整授权信息，实际调用仍需 `AliyunBailianDataFullAccess` 策略。

## 来源文档

- [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)
- [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)
- [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)
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
- [DeleteFile](../../raw/_short/api-bailian-2023-12-29-deletefile-7e0409a458195fe2.md)
- [API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md)
- [DeleteFiles](../../raw/_short/api-bailian-2023-12-29-deletefiles-96ef0815114e4e37.md)
- [GetParseSettings - 获取类目解析设置](../../raw/_short/api-bailian-2023-12-29-getparsesettings-522514560c54f49f.md)
- [ChangeParseSetting](../../raw/_short/api-bailian-2023-12-29-changeparsesetting-59a7c69675f499ad.md)
- [AddTable](../../raw/_short/api-bailian-2023-12-29-addtable-6726351659db288d.md)
- [UpdateTableFromAuthorizedOss](../../raw/_short/api-bailian-2023-12-29-updatetablefromauthorized-d7436828bcf51602.md)
- [AddConnector](../../raw/_short/api-bailian-2023-12-29-addconnector-7a3c9650409710fe.md)
- [GetConnector](../../raw/_short/api-bailian-2023-12-29-getconnector-cb2e485a0efd52f7.md)
- [UpdateConnector](../../raw/_short/api-bailian-2023-12-29-updateconnector-6a24905a7d201597.md)
- [知识库](../../raw/_short/api-bailian-2023-12-29-dir-knowledge-base-f6f202ad9694348f.md)
- [CreateIndex](../../raw/_short/api-bailian-2023-12-29-createindex-8bc613c75f8af371.md)
- [GetIndexJobStatus](../../raw/_short/api-bailian-2023-12-29-getindexjobstatus-1e88b6ccfffe0fe4.md)
- [SubmitIndexJob - 提交知识库创建任务](../../raw/_short/api-bailian-2023-12-29-submitindexjob-63b38294171880d4.md)
- [SubmitIndexAddDocumentsJob](../../raw/_short/api-bailian-2023-12-29-submitindexadddocumentsjo-ec4f5cf285e2c447.md)
- [Retrieve](../../raw/_short/api-bailian-2023-12-29-retrieve-c8e6b8d718a30a84.md)
- [GetAvailableParserTypes - 获取文件支持的解析器类型](../../raw/_short/api-bailian-2023-12-29-getavailableparsertypes-09561c4e0fb505d5.md)
- [ListIndexDocuments](../../raw/_short/api-bailian-2023-12-29-listindexdocuments-9f0db0388c421903.md)
- [ListIndexFileDetails](../../raw/_short/api-bailian-2023-12-29-listindexfiledetails-0e2036d0ef0d8fe8.md)
- [DeleteIndexDocument - 删除知识库下的文件](../../raw/_short/api-bailian-2023-12-29-deleteindexdocument-0792a83f5a741348.md)
- [UpdateIndex - 更新知识库](../../raw/_short/api-bailian-2023-12-29-updateindex-551997e1d335e340.md)
- [ListIndices](../../raw/_short/api-bailian-2023-12-29-listindices-c555173be752eaaf.md)
- [DeleteIndex - 删除知识库](../../raw/_short/api-bailian-2023-12-29-deleteindex-500502bd6df1c49c.md)
- [ListChunks - 查询索引下的分片列表](../../raw/_short/api-bailian-2023-12-29-listchunks-30a6c87b93a583c6.md)
- [DeleteChunk - 删除切片](../../raw/_short/api-bailian-2023-12-29-deletechunk-d249422088735d90.md)
- [GetIndexMonitor - 获取知识库监控数据](../../raw/_short/api-bailian-2023-12-29-getindexmonitor-3a609181d5c9c034.md)
- [Prompt 模板](../../raw/_short/api-bailian-2023-12-29-dir-prompt-engineering-11ee962a5f5d5d1e.md)
- [CreatePromptTemplate - 创建Prompt模板](../../raw/_short/api-bailian-2023-12-29-createprompttemplate-1194e536beb0529a.md)
- [GetPromptTemplate - 获取Prompt模板](../../raw/_short/api-bailian-2023-12-29-getprompttemplate-584c357dd7cb48d6.md)
- [UpdatePromptTemplate - 更新Prompt模板](../../raw/_short/api-bailian-2023-12-29-updateprompttemplate-519fb4af5ea50522.md)
- [DeletePromptTemplate - 删除Prompt模板](../../raw/_short/api-bailian-2023-12-29-deleteprompttemplate-b441fa1b9c777b81.md)
- [ListPromptTemplates - 获取Prompt模板列表](../../raw/_short/api-bailian-2023-12-29-listprompttemplates-ab5ba5362e93cfcd.md)
- [其他](../../raw/_short/api-bailian-2023-12-29-dir-others-b9c3a16db11771f5.md)
- [GetAlipayTransferStatus - 查询支付宝打赏状态](../../raw/_short/api-bailian-2023-12-29-getalipaytransferstatus-04aa88852762fd85.md)
- [GetAlipayUrl - 获取支付宝打赏URL](../../raw/_short/api-bailian-2023-12-29-getalipayurl-e6e9715d5164f74a.md)
- [ApplyTempStorageLease - 申请临时文件上传许可](../../raw/_short/api-bailian-2023-12-29-applytempstoragelease-5a38ce0eefc66408.md)
- [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md)
- [AddChunk](../../raw/_short/api-bailian-2023-12-29-addchunk-1607bcddf6713fd9.md)
- [UpdateChunk - 修改切片](../../raw/_short/api-bailian-2023-12-29-updatechunk-589b46fcc24261f8.md)
- [数据连接（原应用数据）](../../raw/_short/api-bailian-2023-12-29-dir-data-connection-origi-a1f7f2601bd6f7cf.md)


