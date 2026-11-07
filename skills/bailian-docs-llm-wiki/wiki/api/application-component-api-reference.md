# application component api reference

本参考文档汇总了百炼平台 Application Component（应用组件）相关的 OpenAPI 接口规范，涵盖数据连接（原应用数据）、知识库两大核心能力模块。所有接口均基于 `bailian/2023-12-29` 版本，采用 ROA 签名风格，支持通过阿里云百炼 SDK 或自签名方式调用。开发者需结合业务空间（Workspace）模型进行资源隔离与权限管控。

## 支持的模型/功能

Application Component API 主要支撑两类核心场景：

- **数据连接（原应用数据）**：提供非结构化文件与结构化表格的全生命周期管理能力，包括类目（Category）组织、文件（File）上传/查询/标签管理、OSS 批量导入、连接器（Connector）配置及解析策略控制。该模块是知识库的数据源基础，[数据连接（原应用数据）](../../raw/_short/api-bailian-2023-12-29-dir-data-connection-origi-a1f7f2601bd6f7cf.md) 文档详细列出了全部相关接口。
- **知识库（Knowledge Base）**：提供面向 RAG 场景的向量索引构建、检索、监控与精细化管理能力，支持文档搜索、音视频、数据查询、图片问答四类知识库结构。关键流程为：创建知识库 → 提交构建任务 → 追加/更新文档 → 检索 → 监控。完整目录见 [知识库](../../raw/_short/api-bailian-2023-12-29-dir-knowledge-base-f6f202ad9694348f.md)。

> **注意**：文档 25（CreateIndex）明确指出“本接口仅初始化知识库创建作业。完成调用后，必须调用 **SubmitIndexJob** 接口以完成创建”，而文档 29（SubmitIndexJob）的接口说明中未强调此强依赖关系，易导致开发者遗漏关键步骤。请务必遵循“先 CreateIndex，再 SubmitIndexJob”的两步流程。

## 关键参数

所有接口均要求在路径中传入 `WorkspaceId`（业务空间 ID），其获取方式统一参见 [如何使用业务空间](https://help.aliyun.com/zh/model-studio/use-workspace)。其他高频关键参数如下：

- **类目与文件标识**：`CategoryId`（来自 [AddCategory](../../raw/_short/api-bailian-2023-12-29-addcategory-e2fe0e0435ed504e.md) 返回）、`FileId`（来自 [AddFile](../../raw/_short/api-bailian-2023-12-29-addfile-8c254b3500bc50bc.md) 返回）、`IndexId`（来自 [CreateIndex](../../raw/_short/api-bailian-2023-12-29-createindex-8bc613c75f8af371.md) 返回）是绝大多数操作的必填资源定位参数。
- **分页控制**：`MaxResults`（数据连接类接口）与 `PageSize`/`PageNumber`（知识库类接口）用于分页，最大值均为 200 或 10（依接口而定），默认值多为 20 或 10。
- **状态过滤**：`DocumentStatus`（如 `FINISH`, `PARSE_FAILED`）和 `EnableNameLike`（布尔值）常用于 `ListIndexDocuments`、`ListIndexFileDetails` 等接口，实现精准或模糊查询。
- **解析与切片控制**：`Parser`（如 `AUTO_SELECT`, `DOCMIND`）、`DenseSimilarityTopK`（向量检索 Top K，默认 100）、`SparseSimilarityTopK`（关键词检索 Top K，默认 100）等参数直接影响数据处理与检索效果。

## 使用方式

1. **环境准备**：使用 RAM 用户（子账号）时，必须授予 `AliyunBailianDataFullAccess`（读写）或 `AliyunBailianDataReadOnlyAccess`（只读）策略，并确保该用户已加入目标业务空间；主账号可直接调用。访问密钥（AccessKey）需通过 [RAM 用户指南](https://help.aliyun.com/zh/ram/user-guide/create-a-ram-user) 创建。
2. **接入点选择**：根据部署地域选择对应公网或 VPC 接入地址，例如华北2（北京）地域的公网地址为 `bailian.cn-beijing.aliyuncs.com`，详情见 [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)。
3. **调用流程**：
   - **文件上传**：`ApplyFileUploadLease` → `AddFile`（或 `AddFilesFromAuthorizedOss`）。
   - **知识库构建**：`CreateIndex` → `SubmitIndexJob`（或 `SubmitIndexAddDocumentsJob`）。
   - **知识库检索**：`Retrieve`（支持向量+关键词混合检索）。
4. **调试工具**：所有接口均支持在 [OpenAPI Explorer](https://api.aliyun.com/) 中直接调试，可自动生成各语言 SDK 示例代码。

## 限制和注意事项

- **限流策略**：各接口有独立的 QPS 限制，常见值为 5 次/秒（如 `AddCategory`, `ListCategory`）或 10 次/秒（如 `AddFile`, `DescribeFile`）。超出将返回 `429 Too Many Requests`，需实现指数退避重试逻辑。
- **幂等性**：多数查询类（`List*`, `Describe*`, `Get*`）和部分管理类（`Delete*`, `Update*`）接口声明为幂等，但 `CreateIndex`、`AddCategory`、`ApplyFileUploadLease` 等创建类接口明确不具备幂等性，重复调用将产生新资源。
- **数据一致性**：`DeleteFile` 仅删除应用数据中的文件，不影响已构建的知识库；反之，`DeleteIndexDocument` 仅删除知识库索引中的文件，不删除原始应用数据。二者不可互换。
- **功能边界**：API 不支持直接新增/删除数据表（表格），此类操作必须通过控制台完成；`AddTable` 接口虽存在，但其文档（文档 19）未在 API 目录（文档 3）中被引用，且无后续配套的 `ListTable` 或 `DeleteTable` 接口，实际可用性存疑，建议优先使用控制台管理表格。

## 来源文档

- [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)
- [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)
- [API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md)
- [数据连接（原应用数据）](../../raw/_short/api-bailian-2023-12-29-dir-data-connection-origi-a1f7f2601bd6f7cf.md)
- [AddCategory](../../raw/_short/api-bailian-2023-12-29-addcategory-e2fe0e0435ed504e.md)
- [ListCategory](../../raw/_short/api-bailian-2023-12-29-listcategory-2521532ef3e828b3.md)
- [ApplyFileUploadLease](../../raw/_short/api-bailian-2023-12-29-applyfileuploadlease-39e8ca15e0e9561a.md)
- [AddFile](../../raw/_short/api-bailian-2023-12-29-addfile-8c254b3500bc50bc.md)
- [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)
- [ListFile](../../raw/_short/api-bailian-2023-12-29-listfile-360209e3a2479f14.md)
- [DescribeFile](../../raw/_short/api-bailian-2023-12-29-describefile-020886c28a208bf2.md)
- [UpdateFileTag](../../raw/_short/api-bailian-2023-12-29-updatefiletag-f84d2af6a45d6553.md)
- [BatchUpdateFileTag](../../raw/_short/api-bailian-2023-12-29-batchupdatefiletag-34a8f009de66cb8b.md)
- [DeleteFile](../../raw/_short/api-bailian-2023-12-29-deletefile-7e0409a458195fe2.md)
- [DeleteCategory - 删除类目](../../raw/_short/api-bailian-2023-12-29-deletecategory-9838436bd2db3113.md)
- [AddFilesFromAuthorizedOss](../../raw/_short/api-bailian-2023-12-29-addfilesfromauthorizedoss-879556d685a301b3.md)
- [GetAvailableParserTypes - 获取文件支持的解析器类型](../../raw/_short/api-bailian-2023-12-29-getavailableparsertypes-09561c4e0fb505d5.md)
- [ChangeParseSetting](../../raw/_short/api-bailian-2023-12-29-changeparsesetting-59a7c69675f499ad.md)
- [AddTable](../../raw/_short/api-bailian-2023-12-29-addtable-6726351659db288d.md)
- [UpdateTableFromAuthorizedOss](../../raw/_short/api-bailian-2023-12-29-updatetablefromauthorized-d7436828bcf51602.md)
- [AddConnector](../../raw/_short/api-bailian-2023-12-29-addconnector-7a3c9650409710fe.md)
- [GetConnector](../../raw/_short/api-bailian-2023-12-29-getconnector-cb2e485a0efd52f7.md)
- [UpdateConnector](../../raw/_short/api-bailian-2023-12-29-updateconnector-6a24905a7d201597.md)
- [知识库](../../raw/_short/api-bailian-2023-12-29-dir-knowledge-base-f6f202ad9694348f.md)
- [CreateIndex - 创建知识库](../../raw/_short/api-bailian-2023-12-29-createindex-8bc613c75f8af371.md)
- [GetIndexJobStatus - 查询知识库创建或追加任务状态](../../raw/_short/api-bailian-2023-12-29-getindexjobstatus-1e88b6ccfffe0fe4.md)
- [DeleteFiles](../../raw/_short/api-bailian-2023-12-29-deletefiles-96ef0815114e4e37.md)
- [SubmitIndexAddDocumentsJob - 提交知识库文件追加任务](../../raw/_short/api-bailian-2023-12-29-submitindexadddocumentsjo-ec4f5cf285e2c447.md)
- [SubmitIndexJob - 提交知识库创建任务](../../raw/_short/api-bailian-2023-12-29-submitindexjob-63b38294171880d4.md)
- [GetParseSettings - 获取类目解析设置](../../raw/_short/api-bailian-2023-12-29-getparsesettings-522514560c54f49f.md)
- [ListIndexDocuments - 查询知识库文件列表](../../raw/_short/api-bailian-2023-12-29-listindexdocuments-9f0db0388c421903.md)
- [Retrieve - 检索知识库](../../raw/_short/api-bailian-2023-12-29-retrieve-c8e6b8d718a30a84.md)
- [ListIndexFileDetails - 查询知识库文件详情](../../raw/_short/api-bailian-2023-12-29-listindexfiledetails-0e2036d0ef0d8fe8.md)
- [DeleteIndexDocument - 删除知识库下的文件](../../raw/_short/api-bailian-2023-12-29-deleteindexdocument-0792a83f5a741348.md)
- [UpdateIndex - 更新知识库](../../raw/_short/api-bailian-2023-12-29-updateindex-551997e1d335e340.md)
- [DeleteIndex - 删除知识库](../../raw/_short/api-bailian-2023-12-29-deleteindex-500502bd6df1c49c.md)
- [ListIndices - 查询知识库列表](../../raw/_short/api-bailian-2023-12-29-listindices-c555173be752eaaf.md)
- [ListChunks - 查询索引下的分片列表](../../raw/_short/api-bailian-2023-12-29-listchunks-30a6c87b93a583c6.md)
- [UpdateChunk - 修改切片](../../raw/_short/api-bailian-2023-12-29-updatechunk-589b46fcc24261f8.md)
- [AddChunk - 新增切片](../../raw/_short/api-bailian-2023-12-29-addchunk-1607bcddf6713fd9.md)
- [DeleteChunk - 删除切片](../../raw/_short/api-bailian-2023-12-29-deletechunk-d249422088735d90.md)
- [GetIndexMonitor - 获取知识库监控数据](../../raw/_short/api-bailian-2023-12-29-getindexmonitor-3a609181d5c9c034.md)
- [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md)


