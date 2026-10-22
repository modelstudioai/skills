# application component api reference

本 API 参考文档面向开发者，提供百炼平台应用组件（Application Component）的核心 OpenAPI 接口规范，涵盖数据连接（原应用数据）、知识库两大核心能力模块。所有接口均基于 `bailian/2023-12-29` 版本，采用标准 ROA 签名机制，支持通过官方 SDK 或自签名方式调用。开发者需预先配置 RAM 权限及业务空间成员身份方可使用。

## 支持的模型/功能

API 当前聚焦于**结构化与非结构化数据管理**和**知识库全生命周期操作**两大能力域，不直接暴露大语言模型推理接口（该能力归属 Model API 分类）。具体包括：

- **数据连接（原应用数据）**：提供类目（Category）管理、文件（File）上传/查询/标签更新/删除、表格（Table）增删改查、OSS 批量导入、解析器配置等能力，支撑知识库的数据源准备。详细功能见 [数据连接（原应用数据）](../../raw/_short/api-bailian-2023-12-29-dir-data-connection-origi-a1f7f2601bd6f7cf.md)。
- **知识库（Knowledge Base）**：提供知识库（Index）创建、更新、删除、监控，以及文件索引、切片（Chunk）增删改查、检索（Retrieve）等完整 RAG 能力链路。详细功能见 [知识库](../../raw/_short/api-bailian-2023-12-29-dir-knowledge-base-f6f202ad9694348f.md)。
- **通用能力**：所有接口均支持分页（`NextToken`/`PageNumber`/`PageSize`）、幂等性控制（部分接口明确声明）及统一的限流策略。

> **注意**：文档 41 中提及 `CreateIndex` 和 `Retrieve` 接口在 2025-12-03 和 2024-07-23 发生参数变更，但原始文档中未提供具体变更内容。开发者应以最新版 OpenAPI Explorer 或 SDK 文档为准，避免依赖过时字段。

## 关键参数

所有接口均需在请求路径中指定 `WorkspaceId`（业务空间 ID），其获取方式请参见[如何使用业务空间](https://help.aliyun.com/zh/model-studio/use-workspace)。核心资源标识参数如下：

- **类目操作**：`CategoryId`（由 `AddCategory` 返回），用于 `ListCategory`、`DeleteCategory`、`ApplyFileUploadLease` 等。
- **文件操作**：`FileId`（由 `AddFile` 返回），用于 `DescribeFile`、`DeleteFile`、`UpdateFileTag`、`DeleteIndexDocument` 等。
- **知识库操作**：`IndexId`（由 `CreateIndex` 返回），用于 `SubmitIndexJob`、`Retrieve`、`ListIndexDocuments`、`DeleteIndex` 等。
- **切片操作**：`ChunkId`（由 `ListChunks` 返回的 `Node.Metadata._id` 字段），用于 `UpdateChunk`、`DeleteChunk`。
- **连接器操作**：`ConnectorId`（由 `AddConnector` 返回），用于 `GetConnector`、`UpdateConnector`。

权限相关参数统一为 RAM Action，如 `sfm:AddCategory`、`sfm:Retrieve`，需在 RAM 策略中显式授予。详情请参考 [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)。

## 使用方式

1. **环境准备**：
   - 获取阿里云 AccessKey（推荐使用最小权限的 RAM 用户，而非主账号）。
   - 为目标 RAM 用户附加 `AliyunBailianDataFullAccess`（读写）或 `AliyunBailianDataReadOnlyAccess`（只读）策略。
   - 将 RAM 用户加入目标业务空间。

2. **调用流程（以构建知识库为例）**：
   - 调用 `AddCategory` 创建类目 → `ApplyFileUploadLease` 申请租约 → `AddFile` 上传文件。
   - 调用 `CreateIndex` 初始化知识库 → `SubmitIndexJob` 提交创建任务 → 轮询 `GetIndexJobStatus` 直至完成。
   - 调用 `Retrieve` 进行检索。

3. **SDK 优先**：强烈推荐使用官方 SDK（[下载地址](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29)），可自动处理签名、重试、限流等细节。自签名对接复杂度高，建议仅在特殊场景下使用，并优先咨询钉钉群（147535001692）。

4. **调试工具**：所有接口均支持在 [OpenAPI Explorer](https://api.aliyun.com/) 中直接调试，可生成多语言 SDK 示例代码。

## 限制和注意事项

- **限流策略**：各接口有独立的 QPS 限制（常见为 5~15 次/秒），超限将返回 `429 Too Many Requests`。请务必实现客户端重试逻辑（带指数退避），并避免高频轮询（如 `GetIndexJobStatus` 建议间隔 ≥5 秒）。
- **幂等性**：`List*`、`Describe*`、`Get*` 类查询接口及 `Delete*`、`Update*` 类部分接口（如 `DeleteCategory`、`DeleteIndex`）声明为幂等；`Add*`、`Create*`、`Submit*` 类接口通常不具备幂等性，重复调用可能产生冗余资源。
- **数据一致性**：`DeleteFile` 仅删除应用数据中的文件，不影响已构建的知识库；反之，`DeleteIndexDocument` 仅删除知识库索引中的文件，不影响应用数据源。二者需按需组合使用。
- **地域与接入点**：服务支持华北2（北京）和新加坡地域，对应公网及 VPC 接入地址详见 [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)。请确保客户端请求地址与资源所在地域一致。
- **安全要求**：所有请求必须通过 HTTPS 发起，且 AccessKey 必须通过签名认证。严禁在客户端代码或日志中硬编码或泄露 AccessKey。

## 来源文档

- [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)
- [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)
- [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)
- [API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md)
- [AddCategory](../../raw/_short/api-bailian-2023-12-29-addcategory-e2fe0e0435ed504e.md)
- [数据连接（原应用数据）](../../raw/_short/api-bailian-2023-12-29-dir-data-connection-origi-a1f7f2601bd6f7cf.md)
- [ListCategory](../../raw/_short/api-bailian-2023-12-29-listcategory-2521532ef3e828b3.md)
- [DeleteCategory - 删除类目](../../raw/_short/api-bailian-2023-12-29-deletecategory-9838436bd2db3113.md)
- [AddFile](../../raw/_short/api-bailian-2023-12-29-addfile-8c254b3500bc50bc.md)
- [ApplyFileUploadLease](../../raw/_short/api-bailian-2023-12-29-applyfileuploadlease-39e8ca15e0e9561a.md)
- [AddFilesFromAuthorizedOss](../../raw/_short/api-bailian-2023-12-29-addfilesfromauthorizedoss-879556d685a301b3.md)
- [ListFile](../../raw/_short/api-bailian-2023-12-29-listfile-360209e3a2479f14.md)
- [DescribeFile](../../raw/_short/api-bailian-2023-12-29-describefile-020886c28a208bf2.md)
- [UpdateFileTag](../../raw/_short/api-bailian-2023-12-29-updatefiletag-f84d2af6a45d6553.md)
- [BatchUpdateFileTag](../../raw/_short/api-bailian-2023-12-29-batchupdatefiletag-34a8f009de66cb8b.md)
- [DeleteFile](../../raw/_short/api-bailian-2023-12-29-deletefile-7e0409a458195fe2.md)
- [GetParseSettings - 获取类目解析设置](../../raw/_short/api-bailian-2023-12-29-getparsesettings-522514560c54f49f.md)
- [DeleteFiles](../../raw/_short/api-bailian-2023-12-29-deletefiles-96ef0815114e4e37.md)
- [AddTable](../../raw/_short/api-bailian-2023-12-29-addtable-6726351659db288d.md)
- [ChangeParseSetting](../../raw/_short/api-bailian-2023-12-29-changeparsesetting-59a7c69675f499ad.md)
- [GetAvailableParserTypes - 获取文件支持的解析器类型](../../raw/_short/api-bailian-2023-12-29-getavailableparsertypes-09561c4e0fb505d5.md)
- [UpdateTableFromAuthorizedOss](../../raw/_short/api-bailian-2023-12-29-updatetablefromauthorized-d7436828bcf51602.md)
- [GetConnector](../../raw/_short/api-bailian-2023-12-29-getconnector-cb2e485a0efd52f7.md)
- [AddConnector](../../raw/_short/api-bailian-2023-12-29-addconnector-7a3c9650409710fe.md)
- [CreateIndex](../../raw/_short/api-bailian-2023-12-29-createindex-8bc613c75f8af371.md)
- [知识库](../../raw/_short/api-bailian-2023-12-29-dir-knowledge-base-f6f202ad9694348f.md)
- [UpdateConnector](../../raw/_short/api-bailian-2023-12-29-updateconnector-6a24905a7d201597.md)
- [GetIndexJobStatus](../../raw/_short/api-bailian-2023-12-29-getindexjobstatus-1e88b6ccfffe0fe4.md)
- [SubmitIndexAddDocumentsJob](../../raw/_short/api-bailian-2023-12-29-submitindexadddocumentsjo-ec4f5cf285e2c447.md)
- [SubmitIndexJob - 提交知识库创建任务](../../raw/_short/api-bailian-2023-12-29-submitindexjob-63b38294171880d4.md)
- [Retrieve](../../raw/_short/api-bailian-2023-12-29-retrieve-c8e6b8d718a30a84.md)
- [ListIndexDocuments](../../raw/_short/api-bailian-2023-12-29-listindexdocuments-9f0db0388c421903.md)
- [ListIndexFileDetails](../../raw/_short/api-bailian-2023-12-29-listindexfiledetails-0e2036d0ef0d8fe8.md)
- [UpdateIndex - 更新知识库](../../raw/_short/api-bailian-2023-12-29-updateindex-551997e1d335e340.md)
- [ListIndices](../../raw/_short/api-bailian-2023-12-29-listindices-c555173be752eaaf.md)
- [ListChunks - 查询索引下的分片列表](../../raw/_short/api-bailian-2023-12-29-listchunks-30a6c87b93a583c6.md)
- [AddChunk](../../raw/_short/api-bailian-2023-12-29-addchunk-1607bcddf6713fd9.md)
- [DeleteIndex - 删除知识库](../../raw/_short/api-bailian-2023-12-29-deleteindex-500502bd6df1c49c.md)
- [DeleteIndexDocument - 删除知识库下的文件](../../raw/_short/api-bailian-2023-12-29-deleteindexdocument-0792a83f5a741348.md)
- [GetIndexMonitor - 获取知识库监控数据](../../raw/_short/api-bailian-2023-12-29-getindexmonitor-3a609181d5c9c034.md)
- [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md)
- [UpdateChunk - 修改切片](../../raw/_short/api-bailian-2023-12-29-updatechunk-589b46fcc24261f8.md)
- [DeleteChunk - 删除切片](../../raw/_short/api-bailian-2023-12-29-deletechunk-d249422088735d90.md)


