# application component api reference

本 API 参考文档面向开发者，系统性地描述了百炼平台 Application Component（应用组件）层提供的核心 OpenAPI 能力，覆盖数据连接（原应用数据）与知识库两大功能域。所有接口均基于 `bailian/2023-12-29` 版本，采用标准 ROA 签名机制，支持通过官方 SDK 快速集成。开发者需预先配置 RAM 权限与业务空间成员身份方可调用。

## 支持的模型/功能

Application Component API 主要提供两类能力：

- **数据连接（原应用数据）**：用于管理非结构化文件与结构化表格数据的生命周期。包括类目（Category）的增删查、文件（File）的上传（通过租约）、导入、查询、标签更新及解析设置管理。支持从本地或授权 OSS 批量导入文件与表格，并可为不同文件类型（如 `.pdf`, `.xlsx`）配置专用解析器（如 `DOCMIND_LLM_VERSION`, `Qwen VL`）。详细功能见 [数据连接（原应用数据）](../../raw/_short/api-bailian-2023-12-29-dir-data-connection-origi-a1f7f2601bd6f7cf.md)。

- **知识库（Knowledge Base）**：用于构建、维护和检索私有知识索引。支持创建（`CreateIndex`）、提交构建任务（`SubmitIndexJob`）、追加文档（`SubmitIndexAddDocumentsJob`）、全文/向量混合检索（`Retrieve`）、以及对知识库元数据、文件、文本切片（Chunk）的精细化管理（如 `ListIndexDocuments`, `ListChunks`, `UpdateChunk`）。该模块明确区分 `unstructured`（文档/音视频）与 `structured`（数据查询/图片问答）两类知识库，其操作约束与适用场景各不相同，详见 [知识库](../../raw/_short/api-bailian-2023-12-29-dir-knowledge-base-f6f202ad9694348f.md) 目录。

> **注意**：`ListIndexDocuments` 接口的权限点在文档 32 中被标记为 `sfm:ListIndexFiles`，而 `ListIndexFileDetails` 在文档 33 中同样使用 `sfm:ListIndexFiles`；但 `ListIndexFiles` 并未在权威的 [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md) 文档中定义。实际应以 `sfm:ListIndexDocuments` 和 `sfm:ListIndexFileDetails` 为准，此为文档表述不一致导致的混淆。

## 关键参数

所有 API 均要求在路径中传入 `WorkspaceId`（业务空间 ID），这是资源隔离与权限控制的核心维度。其他关键参数按功能域划分：

- **数据连接域**：
  - `CategoryId`：类目唯一标识，由 `AddCategory` 返回，是文件归属与解析策略的绑定依据。
  - `FileId`：文件唯一标识，由 `AddFile` 返回，用于后续 `DescribeFile`, `UpdateFileTag`, `DeleteFile` 等操作。
  - `LeaseId`：上传租约 ID，由 `ApplyFileUploadLease` 返回，是执行 `AddFile` 的前置凭证。
  - `Parser`：解析器类型（如 `AUTO_SELECT`, `DOCMIND_LLM_VERSION`），决定文件内容如何被切分与向量化，必须与文件类型兼容。

- **知识库域**：
  - `IndexId`：知识库唯一标识，由 `CreateIndex` 返回，是几乎所有知识库操作（`Retrieve`, `ListIndexDocuments`, `DeleteIndexDocument`）的必需参数。
  - `JobId`：[异步任务](../concepts/asynchronous-task.md) ID，由 `SubmitIndexJob` 或 `SubmitIndexAddDocumentsJob` 返回，用于轮询 `GetIndexJobStatus`。
  - `ChunkId`：文本切片唯一标识，由 `ListChunks` 返回，是 `UpdateChunk` 和 `DeleteChunk` 的操作对象。

## 使用方式

1. **环境准备**：获取阿里云 AccessKey（推荐使用最小权限的 RAM 用户），并确保该用户已加入目标业务空间且被授予 `AliyunBailianDataFullAccess`（读写）或 `AliyunBailianDataReadOnlyAccess`（只读）策略。详情请参阅 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md) 中的账号与安全准备章节。
2. **接入点选择**：根据部署地域选择对应的服务接入地址，例如华北2（北京）为 `bailian.cn-beijing.aliyuncs.com`。完整列表见 [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)。
3. **调用流程**（以构建知识库为例）：
   - 调用 `AddCategory` 创建类目。
   - 调用 `ApplyFileUploadLease` 获取租约。
   - 调用 `AddFile` 上传并解析文件。
   - 调用 `CreateIndex` 初始化知识库。
   - 调用 `SubmitIndexJob` 提交构建任务。
   - 轮询 `GetIndexJobStatus` 直至任务完成。
4. **调试工具**：所有接口均支持在 OpenAPI Explorer 中直接调试，无需手动签名。

## 限制和注意事项

- **限流策略**：各接口有独立的 QPS 限制，常见值为 5 次/秒（如 `AddCategory`, `ListCategory`）或 10 次/秒（如 `ApplyFileUploadLease`, `AddFile`, `Retrieve`）。超出后将返回 `429` 错误，需实现指数退避重试。
- **幂等性**：`List*`, `Describe*`, `Get*` 类查询接口普遍具备幂等性；而 `Add*`, `Submit*`, `Delete*` 类操作接口多数不具备幂等性（如 `CreateIndex`, `AddFile`），重复调用可能导致资源冗余或状态异常，建议在客户端实现“先查后创”逻辑。
- **功能边界**：
  - API **不支持**通过接口新增或删除数据表（Table），此类操作必须通过控制台完成。
  - `DeleteIndexDocument` 仅删除知识库索引中的文件，**不会**删除应用数据中对应的原始文件；反之亦然。
  - `UpdateChunk` 仅适用于 `unstructured` 类型知识库，对 `structured` 类型无效。
- **安全与合规**：所有敏感操作（如 `Delete*`）均为不可逆的硬删除，调用前务必进行二次确认。

## 来源文档

- [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)
- [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)
- [API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md)
- [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)
- [数据连接（原应用数据）](../../raw/_short/api-bailian-2023-12-29-dir-data-connection-origi-a1f7f2601bd6f7cf.md)
- [AddCategory](../../raw/_short/api-bailian-2023-12-29-addcategory-e2fe0e0435ed504e.md)
- [ListCategory](../../raw/_short/api-bailian-2023-12-29-listcategory-2521532ef3e828b3.md)
- [DeleteCategory - 删除类目](../../raw/_short/api-bailian-2023-12-29-deletecategory-9838436bd2db3113.md)
- [ApplyFileUploadLease](../../raw/_short/api-bailian-2023-12-29-applyfileuploadlease-39e8ca15e0e9561a.md)
- [AddFile](../../raw/_short/api-bailian-2023-12-29-addfile-8c254b3500bc50bc.md)
- [ListFile](../../raw/_short/api-bailian-2023-12-29-listfile-360209e3a2479f14.md)
- [AddFilesFromAuthorizedOss](../../raw/_short/api-bailian-2023-12-29-addfilesfromauthorizedoss-879556d685a301b3.md)
- [DescribeFile](../../raw/_short/api-bailian-2023-12-29-describefile-020886c28a208bf2.md)
- [UpdateFileTag](../../raw/_short/api-bailian-2023-12-29-updatefiletag-f84d2af6a45d6553.md)
- [BatchUpdateFileTag](../../raw/_short/api-bailian-2023-12-29-batchupdatefiletag-34a8f009de66cb8b.md)
- [DeleteFiles](../../raw/_short/api-bailian-2023-12-29-deletefiles-96ef0815114e4e37.md)
- [DeleteFile](../../raw/_short/api-bailian-2023-12-29-deletefile-7e0409a458195fe2.md)
- [ChangeParseSetting](../../raw/_short/api-bailian-2023-12-29-changeparsesetting-59a7c69675f499ad.md)
- [GetAvailableParserTypes - 获取文件支持的解析器类型](../../raw/_short/api-bailian-2023-12-29-getavailableparsertypes-09561c4e0fb505d5.md)
- [UpdateTableFromAuthorizedOss](../../raw/_short/api-bailian-2023-12-29-updatetablefromauthorized-d7436828bcf51602.md)
- [AddConnector](../../raw/_short/api-bailian-2023-12-29-addconnector-7a3c9650409710fe.md)
- [GetParseSettings - 获取类目解析设置](../../raw/_short/api-bailian-2023-12-29-getparsesettings-522514560c54f49f.md)
- [UpdateConnector](../../raw/_short/api-bailian-2023-12-29-updateconnector-6a24905a7d201597.md)
- [知识库](../../raw/_short/api-bailian-2023-12-29-dir-knowledge-base-f6f202ad9694348f.md)
- [AddTable](../../raw/_short/api-bailian-2023-12-29-addtable-6726351659db288d.md)
- [GetConnector](../../raw/_short/api-bailian-2023-12-29-getconnector-cb2e485a0efd52f7.md)
- [CreateIndex](../../raw/_short/api-bailian-2023-12-29-createindex-8bc613c75f8af371.md)
- [GetIndexJobStatus](../../raw/_short/api-bailian-2023-12-29-getindexjobstatus-1e88b6ccfffe0fe4.md)
- [SubmitIndexJob - 提交知识库创建任务](../../raw/_short/api-bailian-2023-12-29-submitindexjob-63b38294171880d4.md)
- [SubmitIndexAddDocumentsJob](../../raw/_short/api-bailian-2023-12-29-submitindexadddocumentsjo-ec4f5cf285e2c447.md)
- [Retrieve](../../raw/_short/api-bailian-2023-12-29-retrieve-c8e6b8d718a30a84.md)
- [ListIndexDocuments](../../raw/_short/api-bailian-2023-12-29-listindexdocuments-9f0db0388c421903.md)
- [ListIndexFileDetails](../../raw/_short/api-bailian-2023-12-29-listindexfiledetails-0e2036d0ef0d8fe8.md)
- [UpdateIndex - 更新知识库](../../raw/_short/api-bailian-2023-12-29-updateindex-551997e1d335e340.md)
- [DeleteIndexDocument - 删除知识库下的文件](../../raw/_short/api-bailian-2023-12-29-deleteindexdocument-0792a83f5a741348.md)
- [ListIndices](../../raw/_short/api-bailian-2023-12-29-listindices-c555173be752eaaf.md)
- [DeleteIndex - 删除知识库](../../raw/_short/api-bailian-2023-12-29-deleteindex-500502bd6df1c49c.md)
- [ListChunks - 查询索引下的分片列表](../../raw/_short/api-bailian-2023-12-29-listchunks-30a6c87b93a583c6.md)
- [AddChunk](../../raw/_short/api-bailian-2023-12-29-addchunk-1607bcddf6713fd9.md)
- [DeleteChunk - 删除切片](../../raw/_short/api-bailian-2023-12-29-deletechunk-d249422088735d90.md)
- [UpdateChunk - 修改切片](../../raw/_short/api-bailian-2023-12-29-updatechunk-589b46fcc24261f8.md)
- [GetIndexMonitor - 获取知识库监控数据](../../raw/_short/api-bailian-2023-12-29-getindexmonitor-3a609181d5c9c034.md)
- [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md)


