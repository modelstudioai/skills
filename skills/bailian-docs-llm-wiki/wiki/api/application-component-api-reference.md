# application component api reference

本 API 参考文档面向开发者，提供百炼平台应用组件（Application Component）的核心 OpenAPI 接口规范，覆盖数据连接（原应用数据）、知识库两大核心能力模块。所有接口均基于 `bailian/2023-12-29` 版本，采用 ROA 签名机制，支持多语言 SDK 快速集成。开发者需通过 RAM 用户最小权限原则进行授权，并在指定业务空间（Workspace）上下文中调用。

## 支持的模型/功能

当前 API 主要支撑两类核心应用能力：

- **数据连接（原应用数据）**：提供类目管理（`AddCategory`、`ListCategory`、`DeleteCategory`）、文件全生命周期操作（`ApplyFileUploadLease`、`AddFile`、`ListFile`、`DescribeFile`、`DeleteFile`、`DeleteFiles`）、OSS 批量导入（`AddFilesFromAuthorizedOss`）、解析配置（`GetParseSettings`、`ChangeParseSetting`、`GetAvailableParserTypes`）及连接器管理（`AddConnector`、`GetConnector`、`UpdateConnector`）等功能。该模块不支持通过 API 新增或删除数据表，相关操作需通过控制台完成 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)。
- **知识库（Knowledge Base）**：覆盖知识库全生命周期管理，包括创建（`CreateIndex`）、提交构建任务（`SubmitIndexJob`）、追加文件（`SubmitIndexAddDocumentsJob`）、查询列表（`ListIndices`）、检索（`Retrieve`）、文件与切片管理（`ListIndexDocuments`、`ListIndexFileDetails`、`ListChunks`、`AddChunk`、`DeleteChunk`、`UpdateChunk`）、监控（`GetIndexMonitor`）及删除（`DeleteIndex`、`DeleteIndexDocument`）。注意，`DeleteIndexDocument` 仅适用于文档搜索类知识库，对数据查询/图片问答类知识库的操作需通过控制台完成 [DeleteIndexDocument](../../raw/_short/api-bailian-2023-12-29-deleteindexdocument-0792a83f5a741348.md)。

> **注意**：文档 38 (`AddChunk`) 和文档 40 (`UpdateChunk`) 均明确声明“仅支持文档搜索类知识库”，但文档 38 的接口说明中又提到“可为文档搜索类（document）、数据查询类（table）、图片问答类（image）知识库添加切片”，二者存在矛盾。根据文档 40 的权威限制及实际权限点 `sfm:UpdateChunk` 的设计意图，应以“仅支持文档搜索类”为准，数据查询与图片问答类知识库的切片管理应通过表格连接器更新或控制台操作实现。

## 关键参数

- **通用路径参数**：所有接口均需在请求路径中指定 `WorkspaceId`（业务空间 ID），其获取方式请参见[如何使用业务空间](https://help.aliyun.com/zh/model-studio/use-workspace)。
- **类目与文件标识**：`CategoryId`（来自 `AddCategory` 返回值）、`FileId`（来自 `AddFile` 返回值）、`IndexId`（来自 `CreateIndex` 返回值）是绝大多数操作的必需参数，用于精确指向资源。
- **分页与过滤**：`ListCategory`、`ListFile`、`ListIndices` 等列表接口统一支持 `NextToken`/`MaxResults`（或 `PageNumber`/`PageSize`）分页机制；`ListIndexDocuments`、`ListIndexFileDetails` 支持 `DocumentStatus`、`DocumentName`、`EnableNameLike` 等字段进行状态与名称过滤。
- **解析器配置**：`AddFile` 接口的 `Parser` 参数支持 `AUTO_SELECT`、`DOCMIND`、`DOCMIND_DIGITAL` 等多种解析器 code；`ChangeParseSetting` 则允许为特定 `FileType`（如 `pdf`）绑定解析器，其可用值可通过 `GetAvailableParserTypes` 查询 [GetAvailableParserTypes](../../raw/_short/api-bailian-2023-12-29-getavailableparsertypes-09561c4e0fb505d5.md)。

## 使用方式

1. **环境准备**：确保已开通百炼服务，并在阿里云控制台创建 RAM 用户，授予 `AliyunBailianDataFullAccess`（读写）或 `AliyunBailianDataReadOnlyAccess`（只读）策略，且该用户已加入目标业务空间。
2. **接入点选择**：根据部署地域选择对应服务地址，例如华北2（北京）公网地址为 `bailian.cn-beijing.aliyuncs.com` [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)。
3. **SDK 集成（推荐）**：优先使用官方 SDK（如 Python、Java、TypeScript 等），它自动处理签名、重试和限流。SDK 下载地址：[阿里云百炼 SDK 中心](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29)。
4. **自签名对接（备选）**：若必须自签名，请严格遵循 ROA 规范，并务必加入钉钉群（147535001692）获取技术支持，避免因签名错误导致长时间调试 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)。
5. **典型流程示例（知识库）**：
   - 调用 `AddCategory` 创建类目 → `ApplyFileUploadLease` 申请租约 → `AddFile` 上传文件；
   - 调用 `CreateIndex` 初始化知识库 → `SubmitIndexJob` 提交构建任务 → 轮询 `GetIndexJobStatus` 直至完成；
   - 调用 `Retrieve` 进行检索，或 `ListChunks` 查看切片详情。

## 限制和注意事项

- **限流策略**：各接口有独立 QPS 限制，例如 `ListCategory`、`AddCategory` 为 5 次/秒，`ApplyFileUploadLease`、`AddFile` 为 10 次/秒，`Retrieve` 为 15 次/秒。超出将返回限流错误，需实现退避重试逻辑。
- **幂等性**：多数查询类（`List*`, `Describe*`, `Get*`）和删除类（`Delete*`）接口具备幂等性，但创建类（`Add*`, `Create*`, `Submit*`）接口通常不具备，重复调用可能产生冗余资源。
- **安全要求**：严禁使用主账号 AccessKey；必须遵循最小权限原则，为 RAM 用户分配精确到 `Action` 级别的权限（如 `sfm:ListCategory`），而非宽泛的 `*` 权限。
- **数据一致性**：`DeleteFile` 仅删除应用数据中的文件，不影响已构建的知识库；反之，`DeleteIndexDocument` 仅删除知识库索引中的文件，不影响原始应用数据。二者不可互替。
- **版本兼容性**：API 版本 `2023-12-29` 是当前稳定版，后续变更（如 `Retrieve` 在 2024-07-23 的参数调整）均在 [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md) 中明确记录，升级前务必查阅。

## 来源文档

- [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)
- [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)
- [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)
- [API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md)
- [数据连接（原应用数据）](../../raw/_short/api-bailian-2023-12-29-dir-data-connection-origi-a1f7f2601bd6f7cf.md)
- [ListCategory](../../raw/_short/api-bailian-2023-12-29-listcategory-2521532ef3e828b3.md)
- [AddCategory](../../raw/_short/api-bailian-2023-12-29-addcategory-e2fe0e0435ed504e.md)
- [DeleteCategory - 删除类目](../../raw/_short/api-bailian-2023-12-29-deletecategory-9838436bd2db3113.md)
- [ApplyFileUploadLease](../../raw/_short/api-bailian-2023-12-29-applyfileuploadlease-39e8ca15e0e9561a.md)
- [AddFile](../../raw/_short/api-bailian-2023-12-29-addfile-8c254b3500bc50bc.md)
- [AddFilesFromAuthorizedOss](../../raw/_short/api-bailian-2023-12-29-addfilesfromauthorizedoss-879556d685a301b3.md)
- [ListFile](../../raw/_short/api-bailian-2023-12-29-listfile-360209e3a2479f14.md)
- [DescribeFile](../../raw/_short/api-bailian-2023-12-29-describefile-020886c28a208bf2.md)
- [UpdateFileTag](../../raw/_short/api-bailian-2023-12-29-updatefiletag-f84d2af6a45d6553.md)
- [BatchUpdateFileTag](../../raw/_short/api-bailian-2023-12-29-batchupdatefiletag-34a8f009de66cb8b.md)
- [DeleteFile](../../raw/_short/api-bailian-2023-12-29-deletefile-7e0409a458195fe2.md)
- [GetParseSettings - 获取类目解析设置](../../raw/_short/api-bailian-2023-12-29-getparsesettings-522514560c54f49f.md)
- [ChangeParseSetting](../../raw/_short/api-bailian-2023-12-29-changeparsesetting-59a7c69675f499ad.md)
- [AddTable](../../raw/_short/api-bailian-2023-12-29-addtable-6726351659db288d.md)
- [GetAvailableParserTypes - 获取文件支持的解析器类型](../../raw/_short/api-bailian-2023-12-29-getavailableparsertypes-09561c4e0fb505d5.md)
- [UpdateTableFromAuthorizedOss](../../raw/_short/api-bailian-2023-12-29-updatetablefromauthorized-d7436828bcf51602.md)
- [AddConnector](../../raw/_short/api-bailian-2023-12-29-addconnector-7a3c9650409710fe.md)
- [GetConnector](../../raw/_short/api-bailian-2023-12-29-getconnector-cb2e485a0efd52f7.md)
- [UpdateConnector](../../raw/_short/api-bailian-2023-12-29-updateconnector-6a24905a7d201597.md)
- [知识库](../../raw/_short/api-bailian-2023-12-29-dir-knowledge-base-f6f202ad9694348f.md)
- [GetIndexJobStatus - 查询知识库创建或追加任务状态](../../raw/_short/api-bailian-2023-12-29-getindexjobstatus-1e88b6ccfffe0fe4.md)
- [CreateIndex - 创建知识库](../../raw/_short/api-bailian-2023-12-29-createindex-8bc613c75f8af371.md)
- [SubmitIndexAddDocumentsJob - 提交知识库文件追加任务](../../raw/_short/api-bailian-2023-12-29-submitindexadddocumentsjo-ec4f5cf285e2c447.md)
- [SubmitIndexJob - 提交知识库创建任务](../../raw/_short/api-bailian-2023-12-29-submitindexjob-63b38294171880d4.md)
- [ListIndexDocuments - 查询知识库文件列表](../../raw/_short/api-bailian-2023-12-29-listindexdocuments-9f0db0388c421903.md)
- [Retrieve - 检索知识库](../../raw/_short/api-bailian-2023-12-29-retrieve-c8e6b8d718a30a84.md)
- [ListIndexFileDetails - 查询知识库文件详情](../../raw/_short/api-bailian-2023-12-29-listindexfiledetails-0e2036d0ef0d8fe8.md)
- [UpdateIndex - 更新知识库](../../raw/_short/api-bailian-2023-12-29-updateindex-551997e1d335e340.md)
- [ListIndices - 查询知识库列表](../../raw/_short/api-bailian-2023-12-29-listindices-c555173be752eaaf.md)
- [DeleteIndexDocument - 删除知识库下的文件](../../raw/_short/api-bailian-2023-12-29-deleteindexdocument-0792a83f5a741348.md)
- [DeleteIndex - 删除知识库](../../raw/_short/api-bailian-2023-12-29-deleteindex-500502bd6df1c49c.md)
- [ListChunks - 查询索引下的分片列表](../../raw/_short/api-bailian-2023-12-29-listchunks-30a6c87b93a583c6.md)
- [AddChunk - 新增切片](../../raw/_short/api-bailian-2023-12-29-addchunk-1607bcddf6713fd9.md)
- [DeleteChunk - 删除切片](../../raw/_short/api-bailian-2023-12-29-deletechunk-d249422088735d90.md)
- [UpdateChunk - 修改切片](../../raw/_short/api-bailian-2023-12-29-updatechunk-589b46fcc24261f8.md)
- [GetIndexMonitor - 获取知识库监控数据](../../raw/_short/api-bailian-2023-12-29-getindexmonitor-3a609181d5c9c034.md)
- [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md)
- [DeleteFiles](../../raw/_short/api-bailian-2023-12-29-deletefiles-96ef0815114e4e37.md)


