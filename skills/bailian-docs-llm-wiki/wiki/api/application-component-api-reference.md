# application component api reference

本 API 参考文档面向开发者，提供百炼平台应用组件（Application Component）的核心 OpenAPI 接口规范，涵盖数据连接（原应用数据）、知识库两大核心能力模块。所有接口均基于 `bailian/2023-12-29` 版本，采用标准 ROA 签名机制，支持多语言 SDK 封装调用。开发者需通过 RAM 子账号最小权限原则进行授权，并在指定业务空间上下文中操作资源。

## 支持的模型/功能

应用组件 API 主要支撑两类核心场景：

- **数据连接（原应用数据）**：提供非结构化文件与结构化表格的全生命周期管理能力，包括类目（Category）组织、文件（File）上传/查询/标签管理、连接器（Connector）配置、解析器（Parser）策略控制等。该模块是知识库的数据源基础，[数据连接（原应用数据）](../../raw/_short/api-bailian-2023-12-29-dir-data-connection-origi-a1f7f2601bd6f7cf.md) 文档详细列出了全部 12 个相关接口。
- **知识库（Knowledge Base）**：提供基于 RAG 的私有知识检索服务，支持文档搜索、数据查询、图片问答、音视频搜索四类知识库类型。功能覆盖知识库创建/更新/删除、文件追加/删除、切片（Chunk）增删改查、实时检索（Retrieve）及监控数据获取。其完整能力集见 [知识库](../../raw/_short/api-bailian-2023-12-29-dir-knowledge-base-f6f202ad9694348f.md) 目录。

> **注意**：文档 37（AddChunk）和文档 38（UpdateChunk）均声明仅支持“文档搜索类”知识库，但文档 37 的说明中又明确指出该接口“可为文档搜索类（document）、数据查询类（table）、图片问答类（image）知识库添加切片”，且强调“仅当数据源为表格连接器(excel)时，对数据查询与图片问答类型知识库的操作方可生效”。此描述存在逻辑矛盾——若接口本身不支持 table/image 类型，则“仅当...方可生效”的前提不成立。实际开发中，请以接口调试结果和最新 SDK 文档为准，优先验证目标知识库类型与接口兼容性。

## 关键参数

所有接口均需在请求路径中传入 `WorkspaceId`（业务空间 ID），这是资源隔离与权限控制的核心维度。其他关键参数按功能域划分如下：

- **数据连接域**：
  - `CategoryId`：类目唯一标识，由 `AddCategory` 返回，用于 `ListCategory`、`DeleteCategory`、`ApplyFileUploadLease` 等接口。
  - `FileId`：文件唯一标识，由 `AddFile` 返回，用于 `DescribeFile`、`DeleteFile`、`UpdateFileTag` 等接口。
  - `ConnectorId`：连接器唯一标识，用于 `AddConnector`、`GetConnector`、`UpdateConnector`。
  - `Parser`：解析器类型，如 `DOCMIND`、`AUTO_SELECT`，用于 `AddFile` 和 `ChangeParseSetting`，其有效值列表可通过 [GetAvailableParserTypes](../../raw/_short/api-bailian-2023-12-29-getavailableparsertypes-09561c4e0fb505d5.md) 接口动态查询。

- **知识库域**：
  - `IndexId`：知识库唯一标识，由 `CreateIndex` 返回，是 `SubmitIndexJob`、`Retrieve`、`ListIndexDocuments` 等绝大多数知识库接口的必填参数。
  - `JobId`：异步任务 ID，由 `SubmitIndexJob` 或 `SubmitIndexAddDocumentsJob` 返回，用于 `GetIndexJobStatus` 查询状态。
  - `ChunkId`：文本切片唯一标识，由 `ListChunks` 返回，用于 `UpdateChunk` 和 `DeleteChunk`。

## 使用方式

1. **环境准备**：访问 [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md) 获取对应地域（如 `cn-beijing`）的公网或 VPC 接入地址；使用阿里云账号创建具备最小权限的 RAM 子账号，并为其授予 `AliyunBailianDataFullAccess`（读写）或 `AliyunBailianDataReadOnlyAccess`（只读）策略。
2. **SDK 调用（推荐）**：直接集成官方 SDK（如 Python、Java），传入 AccessKey ID/Secret 和 `WorkspaceId` 即可发起调用，无需手动签名。例如，调用 `AddCategory` 前需确保子账号已加入目标业务空间。
3. **自签名调用（不推荐）**：若必须自实现，需严格遵循 [ROA 签名机制](https://help.aliyun.com/zh/sdk/product-overview/roa-mechanism)，过程复杂且易出错，建议加入钉钉群（147535001692）寻求技术支持。
4. **调试验证**：所有接口均支持在 [OpenAPI Explorer](https://api.aliyun.com/api/bailian/2023-12-29) 中在线调试，可即时查看请求/响应并生成各语言 SDK 示例代码。

## 限制和注意事项

- **限流策略**：各接口均有独立 QPS 限制，例如 `AddCategory`、`ListCategory`、`DeleteCategory` 为 5 次/秒；`ApplyFileUploadLease`、`AddFile`、`DeleteFile` 为 10 次/秒；`ListIndices` 为 10 次/秒。超出限制将返回 `429 Too Many Requests`，需实现指数退避重试。
- **幂等性**：`ListCategory`、`ListFile`、`DescribeFile`、`GetIndexJobStatus`、`Retrieve`、`ListIndexDocuments`、`ListIndexFileDetails`、`DeleteIndexDocument`、`DeleteIndex`、`UpdateIndex`、`GetIndexMonitor`、`ListChunks`、`UpdateChunk`、`DeleteChunk` 等接口具有幂等性；而 `AddCategory`、`ApplyFileUploadLease`、`AddFile`、`SubmitIndexJob`、`SubmitIndexAddDocumentsJob` 等则不具备，重复调用可能导致资源冗余或任务重复提交。
- **数据一致性**：`DeleteFile` 仅删除应用数据中的文件，**不会**影响已构建的知识库索引；反之，`DeleteIndexDocument` 仅删除知识库中的文件索引，**不会**删除应用数据中的原始文件。二者操作完全独立，需根据业务需求谨慎选择。
- **功能边界**：API 不支持直接新增或删除数据表（Table），此类操作必须通过控制台完成；`AddTable` 接口仅用于为已有表格连接器添加新表，而非创建连接器本身。

## 来源文档

- [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)
- [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)
- [API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md)
- [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)
- [AddCategory](../../raw/_short/api-bailian-2023-12-29-addcategory-e2fe0e0435ed504e.md)
- [ListCategory](../../raw/_short/api-bailian-2023-12-29-listcategory-2521532ef3e828b3.md)
- [DeleteCategory - 删除类目](../../raw/_short/api-bailian-2023-12-29-deletecategory-9838436bd2db3113.md)
- [ApplyFileUploadLease](../../raw/_short/api-bailian-2023-12-29-applyfileuploadlease-39e8ca15e0e9561a.md)
- [AddFile](../../raw/_short/api-bailian-2023-12-29-addfile-8c254b3500bc50bc.md)
- [ListFile](../../raw/_short/api-bailian-2023-12-29-listfile-360209e3a2479f14.md)
- [DescribeFile](../../raw/_short/api-bailian-2023-12-29-describefile-020886c28a208bf2.md)
- [数据连接（原应用数据）](../../raw/_short/api-bailian-2023-12-29-dir-data-connection-origi-a1f7f2601bd6f7cf.md)
- [UpdateFileTag](../../raw/_short/api-bailian-2023-12-29-updatefiletag-f84d2af6a45d6553.md)
- [BatchUpdateFileTag](../../raw/_short/api-bailian-2023-12-29-batchupdatefiletag-34a8f009de66cb8b.md)
- [DeleteFile](../../raw/_short/api-bailian-2023-12-29-deletefile-7e0409a458195fe2.md)
- [DeleteFiles](../../raw/_short/api-bailian-2023-12-29-deletefiles-96ef0815114e4e37.md)
- [GetParseSettings - 获取类目解析设置](../../raw/_short/api-bailian-2023-12-29-getparsesettings-522514560c54f49f.md)
- [ChangeParseSetting](../../raw/_short/api-bailian-2023-12-29-changeparsesetting-59a7c69675f499ad.md)
- [AddTable](../../raw/_short/api-bailian-2023-12-29-addtable-6726351659db288d.md)
- [UpdateTableFromAuthorizedOss](../../raw/_short/api-bailian-2023-12-29-updatetablefromauthorized-d7436828bcf51602.md)
- [AddConnector](../../raw/_short/api-bailian-2023-12-29-addconnector-7a3c9650409710fe.md)
- [GetConnector](../../raw/_short/api-bailian-2023-12-29-getconnector-cb2e485a0efd52f7.md)
- [UpdateConnector](../../raw/_short/api-bailian-2023-12-29-updateconnector-6a24905a7d201597.md)
- [知识库](../../raw/_short/api-bailian-2023-12-29-dir-knowledge-base-f6f202ad9694348f.md)
- [CreateIndex - 创建知识库](../../raw/_short/api-bailian-2023-12-29-createindex-8bc613c75f8af371.md)
- [GetIndexJobStatus - 查询知识库创建或追加任务状态](../../raw/_short/api-bailian-2023-12-29-getindexjobstatus-1e88b6ccfffe0fe4.md)
- [SubmitIndexJob - 提交知识库创建任务](../../raw/_short/api-bailian-2023-12-29-submitindexjob-63b38294171880d4.md)
- [SubmitIndexAddDocumentsJob - 提交知识库文件追加任务](../../raw/_short/api-bailian-2023-12-29-submitindexadddocumentsjo-ec4f5cf285e2c447.md)
- [Retrieve - 检索知识库](../../raw/_short/api-bailian-2023-12-29-retrieve-c8e6b8d718a30a84.md)
- [ListIndexDocuments - 查询知识库文件列表](../../raw/_short/api-bailian-2023-12-29-listindexdocuments-9f0db0388c421903.md)
- [ListIndexFileDetails - 查询知识库文件详情](../../raw/_short/api-bailian-2023-12-29-listindexfiledetails-0e2036d0ef0d8fe8.md)
- [AddFilesFromAuthorizedOss](../../raw/_short/api-bailian-2023-12-29-addfilesfromauthorizedoss-879556d685a301b3.md)
- [DeleteIndexDocument - 删除知识库下的文件](../../raw/_short/api-bailian-2023-12-29-deleteindexdocument-0792a83f5a741348.md)
- [ListIndices - 查询知识库列表](../../raw/_short/api-bailian-2023-12-29-listindices-c555173be752eaaf.md)
- [DeleteIndex - 删除知识库](../../raw/_short/api-bailian-2023-12-29-deleteindex-500502bd6df1c49c.md)
- [UpdateIndex - 更新知识库](../../raw/_short/api-bailian-2023-12-29-updateindex-551997e1d335e340.md)
- [AddChunk - 新增切片](../../raw/_short/api-bailian-2023-12-29-addchunk-1607bcddf6713fd9.md)
- [UpdateChunk - 修改切片](../../raw/_short/api-bailian-2023-12-29-updatechunk-589b46fcc24261f8.md)
- [DeleteChunk - 删除切片](../../raw/_short/api-bailian-2023-12-29-deletechunk-d249422088735d90.md)
- [GetIndexMonitor - 获取知识库监控数据](../../raw/_short/api-bailian-2023-12-29-getindexmonitor-3a609181d5c9c034.md)
- [ListChunks - 查询索引下的分片列表](../../raw/_short/api-bailian-2023-12-29-listchunks-30a6c87b93a583c6.md)
- [GetAvailableParserTypes - 获取文件支持的解析器类型](../../raw/_short/api-bailian-2023-12-29-getavailableparsertypes-09561c4e0fb505d5.md)
- [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md)


