# application component api reference

本参考文档面向开发者，系统性地描述百炼平台 Application Component（应用组件）提供的核心 API 能力，覆盖数据连接（原应用数据）、知识库两大核心模块。所有接口均基于 `bailian/2023-12-29` 版本，采用 ROA 签名风格，并支持多语言 SDK 封装调用。开发者需通过 RAM 进行最小权限授权，并在指定业务空间（Workspace）上下文中调用。

## 支持的模型/功能

Application Component API 主要提供两类能力：**数据连接管理**与**知识库全生命周期管理**。

- **数据连接（原应用数据）**：提供对非结构化文件和结构化表格的统一管理能力。支持类目（Category）的增删查、文件（File）的上传（含 OSS 授权导入）、解析设置配置、标签管理及元数据查询。例如，`AddCategory` 用于创建分类目录，`AddFilesFromAuthorizedOss` 支持从已授权的 OSS Bucket 批量导入文件 [数据连接（原应用数据）](../../raw/_short/api-bailian-2023-12-29-dir-data-connection-origi-a1f7f2601bd6f7cf.md)。
- **知识库（Knowledge Base）**：提供完整的 RAG 知识库构建与运维能力。涵盖知识库创建（`CreateIndex`）、[异步任务](../concepts/asynchronous-task.md)提交（`SubmitIndexJob`）、文档追加（`SubmitIndexAddDocumentsJob`）、检索（`Retrieve`）、文件与切片（Chunk）的增删改查（`ListIndexDocuments`, `AddChunk`, `DeleteChunk`），以及监控（`GetIndexMonitor`）。其中，`Retrieve` 是核心推理入口，支持稠密向量与关键词混合检索 [Retrieve](../../raw/_short/api-bailian-2023-12-29-retrieve-c8e6b8d718a30a84.md)。

> **注意**：文档 38 (`AddChunk`) 和文档 39 (`DeleteChunk`) 的授权信息存在矛盾。前者声明“当前API暂无授权信息透出”，而后者明确列出了 `sfm:DeleteChunk` 权限点。应以后者为准，即 `AddChunk` 同样需要 `sfm:AddChunk` 权限（尽管未在表中显式列出），该权限点属于 `AliyunBailianDataFullAccess` 策略范畴。

## 关键参数

所有 API 均以 `WorkspaceId`（业务空间 ID）为路径参数，是资源隔离与权限控制的基础。关键请求参数按功能域划分如下：

- **数据连接通用参数**：
  - `CategoryId`: 类目 ID，由 `AddCategory` 返回，用于文件归属和解析设置。
  - `FileId`: 文件 ID，由 `AddFile` 返回，是文件操作（如 `DescribeFile`, `DeleteFile`）的核心标识。
  - `ConnectorId`: 连接器 ID，用于关联自定义存储（如 OSS）。
- **知识库通用参数**：
  - `IndexId`: 知识库 ID，由 `CreateIndex` 返回，是所有知识库操作（如 `Retrieve`, `DeleteIndex`）的必需参数。
  - `PipelineId`: 在切片（Chunk）相关 API（如 `AddChunk`, `UpdateChunk`）中，此参数等同于 `IndexId`。
- **分页与过滤参数**：
  - `NextToken` / `PageNumber` & `PageSize`: 分页查询标准参数，见 `ListCategory` 和 `ListIndexDocuments`。
  - `DocumentStatus`: 用于 `ListIndexDocuments` 等接口，按文件状态（如 `FINISH`, `INSERT_ERROR`）过滤结果。
- **解析与检索参数**：
  - `Parser`: 指定文件解析器类型（如 `DOCMIND_DIGITAL`, `AUTO_SELECT`），见 `AddFile` 和 `ChangeParseSetting`。
  - `DenseSimilarityTopK` / `SparseSimilarityTopK`: 控制 `Retrieve` 和 `UpdateIndex` 的检索召回数量，二者之和 ≤ 200。

## 使用方式

1. **环境准备**：获取 AccessKey（推荐使用 RAM 子账号并授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略），确认业务空间 ID。
2. **接入点选择**：根据部署地域选择公网或 VPC 接入地址，例如华北2（北京）的公网地址为 `bailian.cn-beijing.aliyuncs.com` [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)。
3. **调用流程**：
   - **数据连接**：典型流程为 `AddCategory` → `ApplyFileUploadLease` → `AddFile` → `ListFile`。
   - **知识库**：典型流程为 `CreateIndex` → `SubmitIndexJob`（等待完成）→ `Retrieve`；追加文档则为 `AddFile` → `SubmitIndexAddDocumentsJob`。
4. **调试与开发**：强烈推荐使用 OpenAPI Explorer 进行在线调试，或直接集成官方 SDK（Java/Python/Go 等），避免手动签名。

## 限制和注意事项

- **限流策略**：各接口有独立的 QPS 限制，常见值为 5~15 次/秒。例如 `AddCategory`、`ListCategory` 为 5 次/秒，`Retrieve` 为 15 次/秒。超限将返回 `429 Too Many Requests`，需实现指数退避重试。
- **幂等性**：多数查询类接口（如 `ListCategory`, `ListIndexDocuments`）和部分删除/更新类接口（如 `DeleteCategory`, `DeleteIndexDocument`）具有幂等性；但创建类接口（如 `AddCategory`, `CreateIndex`）不具备，重复调用会创建新资源。
- **数据一致性**：`DeleteFile` 仅删除应用数据中的文件，不影响已构建的知识库；反之，`DeleteIndexDocument` 仅删除知识库索引，不删除源文件。二者需按需配合使用。
- **功能边界**：API 不支持直接创建/删除数据表（需通过控制台），也不支持对音视频搜索类（`multimedia`）知识库进行切片操作（见 `AddChunk` 文档说明）。

## 来源文档

- [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)
- [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)
- [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)
- [AddCategory](../../raw/_short/api-bailian-2023-12-29-addcategory-e2fe0e0435ed504e.md)
- [数据连接（原应用数据）](../../raw/_short/api-bailian-2023-12-29-dir-data-connection-origi-a1f7f2601bd6f7cf.md)
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
- [GetParseSettings - 获取类目解析设置](../../raw/_short/api-bailian-2023-12-29-getparsesettings-522514560c54f49f.md)
- [ChangeParseSetting](../../raw/_short/api-bailian-2023-12-29-changeparsesetting-59a7c69675f499ad.md)
- [GetAvailableParserTypes - 获取文件支持的解析器类型](../../raw/_short/api-bailian-2023-12-29-getavailableparsertypes-09561c4e0fb505d5.md)
- [AddTable](../../raw/_short/api-bailian-2023-12-29-addtable-6726351659db288d.md)
- [UpdateTableFromAuthorizedOss](../../raw/_short/api-bailian-2023-12-29-updatetablefromauthorized-d7436828bcf51602.md)
- [AddConnector](../../raw/_short/api-bailian-2023-12-29-addconnector-7a3c9650409710fe.md)
- [UpdateConnector](../../raw/_short/api-bailian-2023-12-29-updateconnector-6a24905a7d201597.md)
- [知识库](../../raw/_short/api-bailian-2023-12-29-dir-knowledge-base-f6f202ad9694348f.md)
- [CreateIndex](../../raw/_short/api-bailian-2023-12-29-createindex-8bc613c75f8af371.md)
- [GetIndexJobStatus](../../raw/_short/api-bailian-2023-12-29-getindexjobstatus-1e88b6ccfffe0fe4.md)
- [SubmitIndexJob - 提交知识库创建任务](../../raw/_short/api-bailian-2023-12-29-submitindexjob-63b38294171880d4.md)
- [SubmitIndexAddDocumentsJob](../../raw/_short/api-bailian-2023-12-29-submitindexadddocumentsjo-ec4f5cf285e2c447.md)
- [Retrieve](../../raw/_short/api-bailian-2023-12-29-retrieve-c8e6b8d718a30a84.md)
- [ListIndexDocuments](../../raw/_short/api-bailian-2023-12-29-listindexdocuments-9f0db0388c421903.md)
- [GetConnector](../../raw/_short/api-bailian-2023-12-29-getconnector-cb2e485a0efd52f7.md)
- [UpdateIndex - 更新知识库](../../raw/_short/api-bailian-2023-12-29-updateindex-551997e1d335e340.md)
- [DeleteIndexDocument - 删除知识库下的文件](../../raw/_short/api-bailian-2023-12-29-deleteindexdocument-0792a83f5a741348.md)
- [API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md)
- [ListIndices](../../raw/_short/api-bailian-2023-12-29-listindices-c555173be752eaaf.md)
- [ListChunks - 查询索引下的分片列表](../../raw/_short/api-bailian-2023-12-29-listchunks-30a6c87b93a583c6.md)
- [DeleteIndex - 删除知识库](../../raw/_short/api-bailian-2023-12-29-deleteindex-500502bd6df1c49c.md)
- [AddChunk](../../raw/_short/api-bailian-2023-12-29-addchunk-1607bcddf6713fd9.md)
- [DeleteChunk - 删除切片](../../raw/_short/api-bailian-2023-12-29-deletechunk-d249422088735d90.md)
- [GetIndexMonitor - 获取知识库监控数据](../../raw/_short/api-bailian-2023-12-29-getindexmonitor-3a609181d5c9c034.md)
- [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md)
- [ListIndexFileDetails](../../raw/_short/api-bailian-2023-12-29-listindexfiledetails-0e2036d0ef0d8fe8.md)
- [UpdateChunk - 修改切片](../../raw/_short/api-bailian-2023-12-29-updatechunk-589b46fcc24261f8.md)


