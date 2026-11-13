# application component api reference

本参考文档汇总了百炼平台 Application Component（应用组件）层的核心 OpenAPI，涵盖数据连接（原应用数据）、知识库两大核心能力。所有接口均基于 `bailian/2023-12-29` 版本，采用 ROA 签名风格，支持通过阿里云百炼 SDK 或 OpenAPI Explorer 快速调用。开发者需先完成 RAM 授权与业务空间绑定，方可安全、合规地集成。

## 支持的模型/功能

Application Component API 不直接提供大模型推理能力，而是支撑**结构化/非结构化数据管理**与**知识库全生命周期管理**两大基础能力：

- **数据连接（原应用数据）**：提供类目（Category）、文件（File）、连接器（Connector）、表格（Table）的增删查改能力，是知识库和智能体应用的数据底座。支持本地上传、OSS 授权导入、解析器配置等。详细功能见 [数据连接（原应用数据）](../../raw/_short/api-bailian-2023-12-29-dir-data-connection-origi-a1f7f2601bd6f7cf.md)。
- **知识库（Knowledge Base）**：覆盖从创建（`CreateIndex`）、提交构建（`SubmitIndexJob`）、追加文档（`SubmitIndexAddDocumentsJob`）、检索（`Retrieve`）到监控（`GetIndexMonitor`）的完整链路，并支持对底层文本切片（Chunk）进行细粒度增删改查（`AddChunk`/`DeleteChunk`/`UpdateChunk`）。其功能概览可参考 [知识库](../../raw/_short/api-bailian-2023-12-29-dir-knowledge-base-f6f202ad9694348f.md) 目录。

> **注意**：文档 39 (`AddChunk`) 中声明支持“图片问答类（image）知识库”，但文档 38 (`UpdateChunk`) 明确指出“仅支持文档搜索类知识库，不支持数据查询和图片问答类知识库”。二者存在功能范围矛盾。实际开发中，请以 `UpdateChunk` 的限制为准，即 Chunk 级别操作目前仅适用于 `unstructured` 类型知识库。

## 关键参数

所有接口均需在请求路径中指定 `WorkspaceId`（业务空间 ID），该 ID 是资源隔离与权限控制的关键维度。其他高频关键参数如下：

- **`CategoryId`**：类目 ID，用于文件归属管理。由 `AddCategory` 接口返回，或在控制台获取。在 `AddFile`、`ListFile` 等接口中为必填项。
- **`FileId`**：文件 ID，标识一个已成功导入的文件。由 `AddFile` 接口返回，是 `DescribeFile`、`DeleteFile`、`UpdateFileTag` 等操作的目标标识。
- **`IndexId`**：知识库 ID，由 `CreateIndex` 接口返回，是知识库所有后续操作（如 `Retrieve`、`DeleteIndexDocument`、`GetIndexMonitor`）的必需参数。
- **`ChunkId`**：文本切片 ID，由 `ListChunks` 接口返回，用于 `UpdateChunk` 和 `DeleteChunk` 等精确操作。
- **分页参数**：`ListCategory`、`ListFile`、`ListIndices` 等列表接口普遍使用 `NextToken`（游标式）或 `PageNumber`/`PageSize`（页码式）进行分页。例如，`ListCategory` 使用 `NextToken`，而 `ListIndices` 使用 `PageNumber` 和 `PageSize`。

## 使用方式

1. **环境准备**：使用 RAM 用户（子账号）调用前，必须为其授予 `AliyunBailianDataFullAccess`（读写）或 `AliyunBailianDataReadOnlyAccess`（只读）策略，并确保该用户已加入目标业务空间。主账号可直接调用。详情请参阅 [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)。
2. **接入点选择**：根据部署地域选择对应的服务接入点。例如，华北2（北京）地域的公网地址为 `bailian.cn-beijing.aliyuncs.com`，VPC 地址为 `bailian-vpc.cn-beijing.aliyuncs.com`。完整列表见 [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)。
3. **典型工作流**：
   - **数据准备**：调用 `AddCategory` 创建类目 → `ApplyFileUploadLease` 获取上传租约 → `AddFile` 导入文件。
   - **知识库构建**：调用 `CreateIndex` 初始化知识库 → `SubmitIndexJob` 启动构建任务 → 轮询 `GetIndexJobStatus` 查询状态。
   - **知识库增强**：调用 `SubmitIndexAddDocumentsJob` 追加新文件 → `Retrieve` 进行语义检索。

## 限制和注意事项

- **限流策略**：各接口有独立的 QPS 限制，例如 `AddCategory`、`ListCategory`、`DeleteCategory` 为 5 次/秒；`ApplyFileUploadLease`、`AddFile` 为 10 次/秒；`ListIndexDocuments` 为 15 次/秒。超出后将返回限流错误，需实现退避重试逻辑。
- **幂等性**：多数查询类（`List*`, `Describe*`, `Get*`）和部分更新类（`UpdateIndex`, `DeleteIndexDocument`）接口具有幂等性，可安全重试；而创建类（`AddCategory`, `AddFile`, `CreateIndex`）通常不具备幂等性，重复调用可能导致资源冗余。
- **功能边界**：
  - API **不支持**通过接口新增或删除数据表（Table），此操作必须通过控制台完成（见 `AddCategory` 和 `DeleteFile` 文档说明）。
  - `DeleteIndexDocument` 仅删除知识库索引中的文件，**不会**影响 `应用数据` 中的原始文件；反之亦然。
- **版本兼容性**：API 行为可能随版本迭代变化。例如，`Retrieve` 接口在 2024-07-23 发生了请求参数变更，`CreateIndex` 在 2025-12-03 也发生了变更。开发者应关注 [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md) 并及时适配。

## 来源文档

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
- [DescribeFile](../../raw/_short/api-bailian-2023-12-29-describefile-020886c28a208bf2.md)
- [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)
- [BatchUpdateFileTag](../../raw/_short/api-bailian-2023-12-29-batchupdatefiletag-34a8f009de66cb8b.md)
- [DeleteFile](../../raw/_short/api-bailian-2023-12-29-deletefile-7e0409a458195fe2.md)
- [DeleteFiles](../../raw/_short/api-bailian-2023-12-29-deletefiles-96ef0815114e4e37.md)
- [GetParseSettings - 获取类目解析设置](../../raw/_short/api-bailian-2023-12-29-getparsesettings-522514560c54f49f.md)
- [GetAvailableParserTypes - 获取文件支持的解析器类型](../../raw/_short/api-bailian-2023-12-29-getavailableparsertypes-09561c4e0fb505d5.md)
- [ListFile](../../raw/_short/api-bailian-2023-12-29-listfile-360209e3a2479f14.md)
- [ChangeParseSetting](../../raw/_short/api-bailian-2023-12-29-changeparsesetting-59a7c69675f499ad.md)
- [AddTable](../../raw/_short/api-bailian-2023-12-29-addtable-6726351659db288d.md)
- [UpdateTableFromAuthorizedOss](../../raw/_short/api-bailian-2023-12-29-updatetablefromauthorized-d7436828bcf51602.md)
- [AddConnector](../../raw/_short/api-bailian-2023-12-29-addconnector-7a3c9650409710fe.md)
- [GetConnector](../../raw/_short/api-bailian-2023-12-29-getconnector-cb2e485a0efd52f7.md)
- [UpdateConnector](../../raw/_short/api-bailian-2023-12-29-updateconnector-6a24905a7d201597.md)
- [知识库](../../raw/_short/api-bailian-2023-12-29-dir-knowledge-base-f6f202ad9694348f.md)
- [GetIndexJobStatus - 查询知识库创建或追加任务状态](../../raw/_short/api-bailian-2023-12-29-getindexjobstatus-1e88b6ccfffe0fe4.md)
- [SubmitIndexJob - 提交知识库创建任务](../../raw/_short/api-bailian-2023-12-29-submitindexjob-63b38294171880d4.md)
- [SubmitIndexAddDocumentsJob - 提交知识库文件追加任务](../../raw/_short/api-bailian-2023-12-29-submitindexadddocumentsjo-ec4f5cf285e2c447.md)
- [Retrieve - 检索知识库](../../raw/_short/api-bailian-2023-12-29-retrieve-c8e6b8d718a30a84.md)
- [UpdateFileTag](../../raw/_short/api-bailian-2023-12-29-updatefiletag-f84d2af6a45d6553.md)
- [ListIndexFileDetails - 查询知识库文件详情](../../raw/_short/api-bailian-2023-12-29-listindexfiledetails-0e2036d0ef0d8fe8.md)
- [UpdateIndex - 更新知识库](../../raw/_short/api-bailian-2023-12-29-updateindex-551997e1d335e340.md)
- [DeleteIndexDocument - 删除知识库下的文件](../../raw/_short/api-bailian-2023-12-29-deleteindexdocument-0792a83f5a741348.md)
- [ListIndices - 查询知识库列表](../../raw/_short/api-bailian-2023-12-29-listindices-c555173be752eaaf.md)
- [DeleteIndex - 删除知识库](../../raw/_short/api-bailian-2023-12-29-deleteindex-500502bd6df1c49c.md)
- [CreateIndex - 创建知识库](../../raw/_short/api-bailian-2023-12-29-createindex-8bc613c75f8af371.md)
- [ListChunks - 查询索引下的分片列表](../../raw/_short/api-bailian-2023-12-29-listchunks-30a6c87b93a583c6.md)
- [UpdateChunk - 修改切片](../../raw/_short/api-bailian-2023-12-29-updatechunk-589b46fcc24261f8.md)
- [AddChunk - 新增切片](../../raw/_short/api-bailian-2023-12-29-addchunk-1607bcddf6713fd9.md)
- [DeleteChunk - 删除切片](../../raw/_short/api-bailian-2023-12-29-deletechunk-d249422088735d90.md)
- [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md)
- [GetIndexMonitor - 获取知识库监控数据](../../raw/_short/api-bailian-2023-12-29-getindexmonitor-3a609181d5c9c034.md)
- [ListIndexDocuments - 查询知识库文件列表](../../raw/_short/api-bailian-2023-12-29-listindexdocuments-9f0db0388c421903.md)


