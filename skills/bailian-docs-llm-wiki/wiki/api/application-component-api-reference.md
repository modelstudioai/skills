# application component api reference

本 API 参考文档面向开发者，提供百炼平台 Application Component（应用组件）层的核心 OpenAPI 接口规范，涵盖数据连接（原应用数据）与知识库两大核心能力模块。所有接口均基于 `bailian/2023-12-29` 版本，采用标准 ROA 签名机制，支持通过官方 SDK 或自签名方式调用。使用前需完成 RAM 权限配置与业务空间绑定。

## 支持的模型/功能

Application Component API 主要支撑两类关键能力：

- **数据连接（原应用数据）**：提供对原始文件和表格数据的全生命周期管理，包括类目（Category）组织、文件（File）上传/查询/标签更新/删除、OSS 授权导入、解析器配置等。该模块是知识库的数据源基础，但不直接参与检索逻辑。例如，`AddCategory` 用于构建分类体系，`AddFilesFromAuthorizedOss` 支持从已授权 OSS Bucket 批量导入文件 [AddFilesFromAuthorizedOss](../../raw/_short/api-bailian-2023-12-29-addfilesfromauthorizedoss-879556d685a301b3.md)。
- **知识库（Knowledge Base）**：提供结构化与非结构化知识的索引构建、内容检索与细粒度管理。支持创建（`CreateIndex`）、提交构建任务（`SubmitIndexJob`）、追加文档（`SubmitIndexAddDocumentsJob`）、检索（`Retrieve`）、查询文件列表（`ListIndexDocuments`）及切片（Chunk）级操作（`AddChunk`, `UpdateChunk`, `DeleteChunk`）。其中，`Retrieve` 是核心推理入口，用于在应用中注入私有知识 [Retrieve](../../raw/_short/api-bailian-2023-12-29-retrieve-c8e6b8d718a30a84.md)。

> **注意**：文档 37（`AddChunk`）与文档 38（`UpdateChunk`）在适用知识库类型上存在矛盾。`AddChunk` 文档明确说明支持 document/table/image 三类知识库，而 `UpdateChunk` 文档则强调“仅支持文档搜索类知识库，不支持数据查询和图片问答类知识库”。实际开发中，请以 `UpdateChunk` 的限制为准，其功能范围窄于 `AddChunk`。

## 关键参数

所有 API 均依赖以下通用参数，并遵循统一的权限与资源模型：

- **`WorkspaceId`（业务空间 ID）**：必填路径参数，标识操作所属的业务空间。获取方式请参见[如何使用业务空间](https://help.aliyun.com/zh/model-studio/use-workspace)。此 ID 是资源隔离与权限控制的核心维度。
- **身份凭证**：必须使用有效的阿里云 AccessKey（推荐为 RAM 子用户配置最小权限策略 `AliyunBailianDataFullAccess`），严禁使用主账号 AK。安全最佳实践详见 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md) 中的“账号与安全准备”章节。
- **幂等性控制**：多数查询类接口（如 `ListCategory`, `ListFile`, `GetIndexJobStatus`）具备幂等性；而创建、更新、删除类接口（如 `AddCategory`, `ChangeParseSetting`, `DeleteIndex`）多数不具备幂等性，需由客户端自行实现“先查后建”等幂等逻辑。
- **分页与限流**：`List*` 类接口普遍支持 `MaxResults`/`NextToken` 分页；所有接口均有明确的 QPS 限流阈值（常见为 5~15 次/秒），超限将返回错误，需实现退避重试。

## 使用方式

1. **环境准备**：访问 [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md) 获取对应地域的公网或 VPC Endpoint（如 `bailian.cn-beijing.aliyuncs.com`）。
2. **认证授权**：为调用者 RAM 用户授予 `AliyunBailianDataFullAccess`（读写）或 `AliyunBailianDataReadOnlyAccess`（只读）策略，并确保其已加入目标 `WorkspaceId` 对应的业务空间。
3. **调用流程（以知识库为例）**：
   - 调用 `CreateIndex` 初始化知识库；
   - 调用 `SubmitIndexJob` 提交构建任务；
   - （可选）调用 `SubmitIndexAddDocumentsJob` 追加新文件；
   - 调用 `Retrieve` 进行在线检索。
4. **调试与开发**：强烈推荐使用 [OpenAPI Explorer](https://api.aliyun.com/) 直接调试，或集成最新版 [阿里云百炼 SDK](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29)，避免手动处理复杂签名。

## 限制和注意事项

- **数据与知识库分离**：`DeleteFile` 仅删除应用数据中的原始文件，不影响已构建的知识库；反之，`DeleteIndexDocument` 仅删除知识库中的索引文档，不删除原始数据集中的文件。二者不可混淆。
- **文件状态约束**：`DeleteFile` 和 `DeleteFiles` 接口仅允许删除状态为 `PARSE_FAILED` 或 `PARSE_SUCCESS` 的文件；`DeleteIndexDocument` 仅允许删除状态为 `INSERT_ERROR` 或 `FINISH` 的文件。调用前务必通过 `DescribeFile` 或 `ListIndexDocuments` 查询状态。
- **OSS 授权要求**：使用 `AddFilesFromAuthorizedOss` 或 `UpdateTableFromAuthorizedOss` 时，OSS Bucket 必须与百炼同属一个阿里云主账号，且存储类型不能为归档/冷归档/深度冷归档。若开启 Referer 防盗链，需将 `*.console.aliyun.com` 加入白名单。
- **切片（Chunk）操作限制**：`UpdateChunk` 和 `DeleteChunk` 仅适用于文档搜索类（document）知识库，对 table/image 类型无效，此限制在 `AddChunk` 文档中未被明确排除，构成潜在风险点。
- **版本兼容性**：API 行为以 `2023-12-29` 版本为准。后续变更（如 `CreateIndex` 和 `Retrieve` 参数调整）记录在 [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md) 中，升级前需仔细比对。

## 来源文档

- [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)
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
- [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)
- [DeleteFiles](../../raw/_short/api-bailian-2023-12-29-deletefiles-96ef0815114e4e37.md)
- [GetParseSettings - 获取类目解析设置](../../raw/_short/api-bailian-2023-12-29-getparsesettings-522514560c54f49f.md)
- [GetAvailableParserTypes - 获取文件支持的解析器类型](../../raw/_short/api-bailian-2023-12-29-getavailableparsertypes-09561c4e0fb505d5.md)
- [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)
- [ChangeParseSetting](../../raw/_short/api-bailian-2023-12-29-changeparsesetting-59a7c69675f499ad.md)
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
- [AddTable](../../raw/_short/api-bailian-2023-12-29-addtable-6726351659db288d.md)
- [UpdateIndex - 更新知识库](../../raw/_short/api-bailian-2023-12-29-updateindex-551997e1d335e340.md)
- [DeleteIndexDocument - 删除知识库下的文件](../../raw/_short/api-bailian-2023-12-29-deleteindexdocument-0792a83f5a741348.md)
- [ListIndices - 查询知识库列表](../../raw/_short/api-bailian-2023-12-29-listindices-c555173be752eaaf.md)
- [DeleteIndex - 删除知识库](../../raw/_short/api-bailian-2023-12-29-deleteindex-500502bd6df1c49c.md)
- [DeleteFile](../../raw/_short/api-bailian-2023-12-29-deletefile-7e0409a458195fe2.md)
- [AddChunk - 新增切片](../../raw/_short/api-bailian-2023-12-29-addchunk-1607bcddf6713fd9.md)
- [UpdateChunk - 修改切片](../../raw/_short/api-bailian-2023-12-29-updatechunk-589b46fcc24261f8.md)
- [DeleteChunk - 删除切片](../../raw/_short/api-bailian-2023-12-29-deletechunk-d249422088735d90.md)
- [GetIndexMonitor - 获取知识库监控数据](../../raw/_short/api-bailian-2023-12-29-getindexmonitor-3a609181d5c9c034.md)
- [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md)
- [ListIndexFileDetails - 查询知识库文件详情](../../raw/_short/api-bailian-2023-12-29-listindexfiledetails-0e2036d0ef0d8fe8.md)
- [ListChunks - 查询索引下的分片列表](../../raw/_short/api-bailian-2023-12-29-listchunks-30a6c87b93a583c6.md)


