# application component api reference

本 API 参考文档面向开发者，提供百炼平台应用组件（Application Component）的核心 OpenAPI 接口规范，涵盖数据连接（原应用数据）、知识库两大核心能力模块。所有接口均基于 `bailian/2023-12-29` 版本，采用 ROA 签名机制，支持多语言 SDK 封装调用。开发者需通过 RAM 用户最小权限原则进行授权，并在指定业务空间（Workspace）内操作资源。

## 支持的模型/功能

API 当前聚焦于两类核心能力：

- **数据连接（原应用数据）**：提供类目管理（`AddCategory`/`ListCategory`/`DeleteCategory`）、文件全生命周期管理（`ApplyFileUploadLease` → `AddFile` → `ListFile`/`DescribeFile` → `DeleteFile`）、OSS 批量导入（`AddFilesFromAuthorizedOss`）、解析器配置（`GetAvailableParserTypes`/`ChangeParseSetting`）及连接器管理（`AddConnector`/`GetConnector`）等功能。该模块不支持通过 API 新增或删除数据表，相关操作需通过控制台完成 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)。
- **知识库（Knowledge Base）**：覆盖知识库全生命周期管理，包括创建（`CreateIndex`）、提交构建任务（`SubmitIndexJob`）、追加文件（`SubmitIndexAddDocumentsJob`）、检索（`Retrieve`）、查询列表与详情（`ListIndices`/`ListIndexDocuments`/`ListIndexFileDetails`）、更新配置（`UpdateIndex`）、删除（`DeleteIndex`），以及细粒度的切片（Chunk）操作（`AddChunk`/`UpdateChunk`/`DeleteChunk`/`ListChunks`）和监控（`GetIndexMonitor`）。注意：`SubmitIndexAddDocumentsJob` 明确不支持数据查询/图片问答类知识库，相关更新请参见 [知识库](../../raw/application-user-guide/agent-context/knowledge-base/data-connection-overview/rag-knowledge-base.md) 文档。

> **注意**：文档 42 (`AddChunk`) 声明支持 `document`/`table`/`image` 三类知识库，但文档 36 (`ListChunks`) 和文档 38 (`UpdateChunk`) 均明确指出其仅支持文档搜索类知识库；文档 39 (`DeleteChunk`) 同样限定为文档搜索类。此为功能范围描述不一致，以 `ListChunks`、`UpdateChunk`、`DeleteChunk` 的权威说明为准，即切片级 CRUD 操作当前仅适用于 `unstructured` 类型的知识库。

## 关键参数

- **通用路径参数**：几乎所有接口均需 `WorkspaceId`（业务空间 ID），用于隔离资源作用域，获取方式详见 [如何使用业务空间](https://help.aliyun.com/zh/model-studio/use-workspace)。
- **类目与文件标识**：`CategoryId`（来自 `AddCategory` 返回值）、`FileId`（来自 `AddFile` 返回值）、`DocumentId`（同 `FileId`，用于知识库操作）是关键关联字段。
- **知识库标识**：`IndexId`（来自 `CreateIndex` 返回值）是知识库操作的核心 ID。
- **分页与过滤**：`List*` 类接口普遍支持 `NextToken`（游标分页）、`MaxResults`/`PageSize`（每页数量）、`PageNumber`（页码）及 `DocumentName`/`IndexName` 等过滤参数。
- **解析器选择**：`AddFile` 接口的 `Parser` 参数支持 `AUTO_SELECT`, `DOCMIND`, `DOCMIND_DIGITAL`, `DOCMIND_LLM_VERSION`, `DASH_QWEN_VL_PARSER`, `DOCMIND_LLM_VERSION_MEDIA` 等值，具体兼容性需结合 `GetAvailableParserTypes` 查询结果确定。

## 使用方式

1. **环境准备**：使用 RAM 子账号并授予 `AliyunBailianDataFullAccess`（读写）或 `AliyunBailianDataReadOnlyAccess`（只读）策略，确保其已加入目标业务空间。主账号可直接调用 [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)。
2. **接入点**：根据地域选择公网或 VPC 接入地址，例如北京地域为 `bailian.cn-beijing.aliyuncs.com` 或 `bailian-vpc.cn-beijing.aliyuncs.com` [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)。
3. **调用流程（典型文件入库）**：
   - 调用 `ApplyFileUploadLease` 获取上传租约 `LeaseId`；
   - 使用租约将文件上传至百炼临时存储；
   - 调用 `AddFile` 并传入 `LeaseId`、`CategoryId`、`Parser` 完成文件导入；
   - （可选）调用 `UpdateFileTag` 为文件打标签。
4. **调用流程（典型知识库构建）**：
   - 调用 `CreateIndex` 初始化知识库，获取 `IndexId`；
   - 调用 `SubmitIndexJob` 提交构建任务；
   - 调用 `GetIndexJobStatus` 轮询任务状态直至完成；
   - （可选）调用 `SubmitIndexAddDocumentsJob` 追加新文件。
5. **调试工具**：推荐使用 [OpenAPI Explorer](https://api.aliyun.com/api/bailian/2023-12-29) 直接运行接口并生成 SDK 代码示例。

## 限制和注意事项

- **限流策略**：各接口有独立 QPS 限制，常见为 `5` 次/秒（如 `AddCategory`, `DeleteCategory`）或 `10` 次/秒（如 `ApplyFileUploadLease`, `AddFile`, `Retrieve`），超限将返回 `429` 错误，需实现退避重试逻辑。
- **幂等性**：`List*`, `Describe*`, `Get*`, `Delete*`（除 `DeleteIndex` 外）等查询与删除类接口通常具有幂等性；`Add*`, `Submit*`, `Update*` 等创建与更新类接口多数不具备幂等性，重复调用可能导致资源冗余或状态异常，建议通过“先查后建”逻辑保障。
- **安全要求**：严禁使用主账号 AccessKey；必须遵循最小权限原则，为 RAM 用户分配精确的 `Action`（如 `sfm:AddCategory`）而非宽泛策略。
- **功能边界**：API 不支持数据表的创建、删除、修改及行级操作；`DeleteIndexDocument` 删除的是知识库索引中的文件引用，不影响 `application data` 中的原始文件；`DeleteIndex` 删除知识库前需在控制台解除其与智能体应用的关联。
- **版本兼容性**：API 行为以 `2023-12-29` 版本为准，历史变更记录见 [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md)。

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
- [DeleteFile](../../raw/_short/api-bailian-2023-12-29-deletefile-7e0409a458195fe2.md)
- [DeleteFiles](../../raw/_short/api-bailian-2023-12-29-deletefiles-96ef0815114e4e37.md)
- [GetAvailableParserTypes - 获取文件支持的解析器类型](../../raw/_short/api-bailian-2023-12-29-getavailableparsertypes-09561c4e0fb505d5.md)
- [GetParseSettings - 获取类目解析设置](../../raw/_short/api-bailian-2023-12-29-getparsesettings-522514560c54f49f.md)
- [ChangeParseSetting](../../raw/_short/api-bailian-2023-12-29-changeparsesetting-59a7c69675f499ad.md)
- [UpdateTableFromAuthorizedOss](../../raw/_short/api-bailian-2023-12-29-updatetablefromauthorized-d7436828bcf51602.md)
- [AddTable](../../raw/_short/api-bailian-2023-12-29-addtable-6726351659db288d.md)
- [AddConnector](../../raw/_short/api-bailian-2023-12-29-addconnector-7a3c9650409710fe.md)
- [GetConnector](../../raw/_short/api-bailian-2023-12-29-getconnector-cb2e485a0efd52f7.md)
- [UpdateConnector](../../raw/_short/api-bailian-2023-12-29-updateconnector-6a24905a7d201597.md)
- [知识库](../../raw/_short/api-bailian-2023-12-29-dir-knowledge-base-f6f202ad9694348f.md)
- [CreateIndex - 创建知识库](../../raw/_short/api-bailian-2023-12-29-createindex-8bc613c75f8af371.md)
- [GetIndexJobStatus - 查询知识库创建或追加任务状态](../../raw/_short/api-bailian-2023-12-29-getindexjobstatus-1e88b6ccfffe0fe4.md)
- [SubmitIndexJob - 提交知识库创建任务](../../raw/_short/api-bailian-2023-12-29-submitindexjob-63b38294171880d4.md)
- [Retrieve - 检索知识库](../../raw/_short/api-bailian-2023-12-29-retrieve-c8e6b8d718a30a84.md)
- [SubmitIndexAddDocumentsJob - 提交知识库文件追加任务](../../raw/_short/api-bailian-2023-12-29-submitindexadddocumentsjo-ec4f5cf285e2c447.md)
- [ListIndexDocuments - 查询知识库文件列表](../../raw/_short/api-bailian-2023-12-29-listindexdocuments-9f0db0388c421903.md)
- [DeleteIndexDocument - 删除知识库下的文件](../../raw/_short/api-bailian-2023-12-29-deleteindexdocument-0792a83f5a741348.md)
- [ListIndices - 查询知识库列表](../../raw/_short/api-bailian-2023-12-29-listindices-c555173be752eaaf.md)
- [DeleteIndex - 删除知识库](../../raw/_short/api-bailian-2023-12-29-deleteindex-500502bd6df1c49c.md)
- [ListChunks - 查询索引下的分片列表](../../raw/_short/api-bailian-2023-12-29-listchunks-30a6c87b93a583c6.md)
- [UpdateIndex - 更新知识库](../../raw/_short/api-bailian-2023-12-29-updateindex-551997e1d335e340.md)
- [UpdateChunk - 修改切片](../../raw/_short/api-bailian-2023-12-29-updatechunk-589b46fcc24261f8.md)
- [DeleteChunk - 删除切片](../../raw/_short/api-bailian-2023-12-29-deletechunk-d249422088735d90.md)
- [GetIndexMonitor - 获取知识库监控数据](../../raw/_short/api-bailian-2023-12-29-getindexmonitor-3a609181d5c9c034.md)
- [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md)
- [AddChunk - 新增切片](../../raw/_short/api-bailian-2023-12-29-addchunk-1607bcddf6713fd9.md)
- [ListIndexFileDetails - 查询知识库文件详情](../../raw/_short/api-bailian-2023-12-29-listindexfiledetails-0e2036d0ef0d8fe8.md)


