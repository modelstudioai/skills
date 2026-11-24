# application component api reference

本 API 参考文档面向开发者，提供百炼平台应用组件（Application Component）的核心 OpenAPI 接口规范，涵盖数据连接（原应用数据）、知识库两大核心能力模块。所有接口均基于 `bailian/2023-12-29` 版本，采用标准 ROA 签名机制，支持多语言 SDK 封装调用。开发者需通过 RAM 用户最小权限授权，并在指定业务空间内操作资源。

## 支持的模型/功能

应用组件 API 主要支撑两类核心能力：

- **数据连接（原应用数据）**：提供对非结构化文件和结构化表格的全生命周期管理，包括类目（Category）组织、文件（File）上传/查询/标签管理、OSS 批量导入、连接器（Connector）配置及解析策略控制。例如，`AddCategory` 用于创建分类目录，`AddFilesFromAuthorizedOss` 支持从已授权 OSS Bucket 批量导入文件，`ChangeParseSetting` 允许为特定文件类型（如 `.pdf`）指定解析器（如 `DOCMIND_DIGITAL`）。该能力不支持通过 API 新增或删除数据表，相关操作需通过控制台完成 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)。

- **知识库（Knowledge Base）**：提供完整的 RAG 知识库管理链路，覆盖创建（`CreateIndex`）、构建（`SubmitIndexJob`）、追加（`SubmitIndexAddDocumentsJob`）、检索（`Retrieve`）、监控（`GetIndexMonitor`）及细粒度操作（切片 `Chunk` 的增删改查）。支持文档搜索、数据查询、图片问答、音视频搜索四类知识库结构。注意，`SubmitIndexAddDocumentsJob` 明确不支持数据查询/图片问答类知识库的追加更新，其更新方式需参考 [知识库](../../raw/application-user-guide/agent-context/knowledge-base/data-connection-overview/rag-knowledge-base.md) 文档说明。

## 关键参数

- **通用路径参数**：几乎所有接口均要求 `WorkspaceId`（业务空间 ID），需通过控制台获取，是资源隔离与权限控制的基础维度。
- **身份与权限标识**：`CategoryId`、`FileId`、`IndexId`、`ConnectorId` 等均为关键资源 ID，通常由上游接口（如 `AddCategory`、`AddFile`、`CreateIndex`）返回，不可自行构造。
- **文件处理参数**：
  - `LeaseId`：由 `ApplyFileUploadLease` 返回，是文件上传的必要凭证。
  - `Parser`：指定文件解析方式，取值如 `AUTO_SELECT`、`DOCMIND_DIGITAL` 等，需与类目解析设置兼容。
- **知识库操作参数**：
  - `JobId`：用于轮询任务状态（`GetIndexJobStatus`）。
  - `DenseSimilarityTopK` / `SparseSimilarityTopK`：`Retrieve` 和 `UpdateIndex` 中控制向量与关键词检索的召回数量，二者之和 ≤ 200。
- **分页与过滤**：`List*` 类接口普遍支持 `MaxResults`/`PageSize`、`NextToken`/`PageNumber` 分页，以及 `DocumentName`、`DocumentStatus` 等字段过滤。

## 使用方式

1. **环境准备**：首先在阿里云 RAM 控制台创建子用户，授予 `AliyunBailianDataFullAccess`（读写）或 `AliyunBailianDataReadOnlyAccess`（只读）策略，并将其加入目标业务空间。**强烈建议避免使用主账号 AccessKey**，以遵循最小权限原则 [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)。
2. **接入点选择**：根据部署地域选择对应服务地址，例如华北2（北京）使用 `bailian.cn-beijing.aliyuncs.com` [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)。
3. **SDK 调用（推荐）**：直接集成官方 SDK（如 Python、Java 版本），自动处理签名、重试与错误解析。所有接口均提供 OpenAPI Explorer 在线调试入口。
4. **典型工作流示例（知识库）**：
   - 调用 `CreateIndex` 初始化知识库。
   - 调用 `SubmitIndexJob` 启动构建任务。
   - 轮询 `GetIndexJobStatus` 直至任务完成。
   - 后续可调用 `Retrieve` 进行检索，或 `UpdateIndex` 调整配置。

## 限制和注意事项

- **幂等性差异**：`List*`、`Describe*`、`Get*`、`DeleteIndexDocument`、`UpdateChunk`、`DeleteChunk` 等接口具有幂等性；而 `Add*`、`ApplyFileUploadLease`、`CreateIndex`、`SubmitIndexJob` 等创建类接口不具备幂等性，重复调用可能产生冗余资源。`CreateIndex` 接口明确提示“重复调用可能会创建多个同名知识库”，需自行实现“先查后创”逻辑 [CreateIndex - 创建知识库](../../raw/_short/api-bailian-2023-12-29-createindex-8bc613c75f8af371.md)。
- **限流策略**：绝大多数接口限流为 5~15 次/秒，`DescribeFile` 和 `ApplyFileUploadLease` 为 10 次/秒，`ListIndexDocuments` 为 15 次/秒。超出将返回 `429 Too Many Requests`，需实现退避重试。
- > **注意**：文档间存在关键矛盾。`DeleteIndexDocument` 接口说明中明确指出“仅能删除知识库中状态为导入失败（INSERT_ERROR）或导入成功（FINISH）的文件”，但 `ListIndexDocuments` 的 `DocumentStatus` 参数枚举值中却包含 `INSERT_ERROR` 和 `FINISH`，而 `DeleteIndexDocument` 的请求参数描述未列出此状态过滤项，实际调用时需以 `ListIndexDocuments` 返回的状态为准进行预筛选。
- **功能边界**：`AddTable` 用于创建表格，但 `DeleteFiles` 和 `DeleteFile` 均声明“不支持通过 API 删除数据表”，且 `DeleteIndexDocument` 也明确不支持数据查询类知识库的文件删除。所有数据表的删除操作必须通过控制台完成。
- **安全与合规**：OSS 导入接口（如 `AddFilesFromAuthorizedOss`）要求 Bucket 与百炼同属一个主账号，并需将 `*.console.aliyun.com` 加入 Referer 白名单；RAM 用户必须被显式加入业务空间才具备调用权限。

## 来源文档

- [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)
- [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)
- [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)
- [API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md)
- [数据连接（原应用数据）](../../raw/_short/api-bailian-2023-12-29-dir-data-connection-origi-a1f7f2601bd6f7cf.md)
- [AddCategory](../../raw/_short/api-bailian-2023-12-29-addcategory-e2fe0e0435ed504e.md)
- [ListCategory](../../raw/_short/api-bailian-2023-12-29-listcategory-2521532ef3e828b3.md)
- [DeleteCategory - 删除类目](../../raw/_short/api-bailian-2023-12-29-deletecategory-9838436bd2db3113.md)
- [AddFilesFromAuthorizedOss](../../raw/_short/api-bailian-2023-12-29-addfilesfromauthorizedoss-879556d685a301b3.md)
- [ListFile](../../raw/_short/api-bailian-2023-12-29-listfile-360209e3a2479f14.md)
- [DescribeFile](../../raw/_short/api-bailian-2023-12-29-describefile-020886c28a208bf2.md)
- [UpdateFileTag](../../raw/_short/api-bailian-2023-12-29-updatefiletag-f84d2af6a45d6553.md)
- [ApplyFileUploadLease](../../raw/_short/api-bailian-2023-12-29-applyfileuploadlease-39e8ca15e0e9561a.md)
- [BatchUpdateFileTag](../../raw/_short/api-bailian-2023-12-29-batchupdatefiletag-34a8f009de66cb8b.md)
- [DeleteFiles](../../raw/_short/api-bailian-2023-12-29-deletefiles-96ef0815114e4e37.md)
- [DeleteFile](../../raw/_short/api-bailian-2023-12-29-deletefile-7e0409a458195fe2.md)
- [GetParseSettings - 获取类目解析设置](../../raw/_short/api-bailian-2023-12-29-getparsesettings-522514560c54f49f.md)
- [ChangeParseSetting](../../raw/_short/api-bailian-2023-12-29-changeparsesetting-59a7c69675f499ad.md)
- [GetAvailableParserTypes - 获取文件支持的解析器类型](../../raw/_short/api-bailian-2023-12-29-getavailableparsertypes-09561c4e0fb505d5.md)
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
- [UpdateIndex - 更新知识库](../../raw/_short/api-bailian-2023-12-29-updateindex-551997e1d335e340.md)
- [ListIndexFileDetails - 查询知识库文件详情](../../raw/_short/api-bailian-2023-12-29-listindexfiledetails-0e2036d0ef0d8fe8.md)
- [DeleteIndexDocument - 删除知识库下的文件](../../raw/_short/api-bailian-2023-12-29-deleteindexdocument-0792a83f5a741348.md)
- [ListIndices - 查询知识库列表](../../raw/_short/api-bailian-2023-12-29-listindices-c555173be752eaaf.md)
- [DeleteIndex - 删除知识库](../../raw/_short/api-bailian-2023-12-29-deleteindex-500502bd6df1c49c.md)
- [ListChunks - 查询索引下的分片列表](../../raw/_short/api-bailian-2023-12-29-listchunks-30a6c87b93a583c6.md)
- [AddChunk - 新增切片](../../raw/_short/api-bailian-2023-12-29-addchunk-1607bcddf6713fd9.md)
- [UpdateChunk - 修改切片](../../raw/_short/api-bailian-2023-12-29-updatechunk-589b46fcc24261f8.md)
- [DeleteChunk - 删除切片](../../raw/_short/api-bailian-2023-12-29-deletechunk-d249422088735d90.md)
- [GetIndexMonitor - 获取知识库监控数据](../../raw/_short/api-bailian-2023-12-29-getindexmonitor-3a609181d5c9c034.md)
- [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md)
- [AddFile](../../raw/_short/api-bailian-2023-12-29-addfile-8c254b3500bc50bc.md)


