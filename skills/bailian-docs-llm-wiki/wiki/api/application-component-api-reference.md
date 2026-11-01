# application component api reference

本 API 参考文档面向开发者，提供百炼平台应用组件（Application Component）的核心 OpenAPI 接口规范，涵盖数据连接（原应用数据）、知识库两大核心能力模块。所有接口均基于 ROA 签名风格，支持通过官方 SDK 或自签名方式调用，并严格遵循 RAM 权限模型进行访问控制。[服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)定义了各地域的公网与 VPC 接入地址，是调用前必须确认的基础配置。

## 支持的模型/功能

应用组件 API 主要支撑两类核心业务场景：

- **数据连接（原应用数据）**：提供对非结构化文件（PDF、Word、PPT、图片等）及结构化表格（Excel）的全生命周期管理，包括类目（Category）组织、文件（File）上传/查询/标签管理、连接器（Connector）配置、解析设置（Parser Setting）定制等。支持从本地、OSS 批量导入，并可对接知识库构建流程。
- **知识库（Knowledge Base）**：支持创建、更新、删除文档搜索类（`unstructured`）、数据查询类（`structured`）及图片问答类知识库；提供文件追加、切片（Chunk）级增删改查、检索（`Retrieve`）、监控（`GetIndexMonitor`）等精细化操作。知识库与应用数据解耦，删除知识库不影响原始文件。

> **注意**：文档 26（`SubmitIndexAddDocumentsJob`）明确说明“本接口不支持数据查询/图片问答类知识库”，但文档 35（`AddChunk`）指出其支持 `table` 和 `image` 类型知识库。二者存在功能覆盖矛盾，实际使用时请以最新版 SDK 文档或控制台行为为准，建议优先通过 `AddChunk` 管理结构化知识库的切片。

## 关键参数

- **`WorkspaceId`**：所有接口的必需路径参数，标识业务空间。获取方式见[如何使用业务空间](https://help.aliyun.com/zh/model-studio/use-workspace)。
- **`CategoryId` / `FileId` / `IndexId` / `ChunkId`**：资源标识符，均为对应操作（如 `AddCategory`, `AddFile`, `CreateIndex`, `ListChunks`）返回的 `Data.Id` 字段值，需在后续关联操作中复用。
- **`Parser`**：文件解析器类型，关键于数据质量。支持 `DOCMIND`, `DOCMIND_DIGITAL`, `DOCMIND_LLM_VERSION`, `DASH_QWEN_VL_PARSER` 等，可通过 [GetAvailableParserTypes](../../raw/_short/api-bailian-2023-12-29-getavailableparsertypes-09561c4e0fb505d5.md) 查询特定文件类型（如 `pdf`）支持的解析器列表。
- **分页参数**：`MaxResults`/`PageSize`（最大 200）、`NextToken`/`PageNumber`，广泛用于 `ListCategory`, `ListFile`, `ListIndices`, `ListIndexFileDetails` 等列表接口。
- **权限参数**：所有操作均需 RAM 用户具备对应 `sfm:*` 权限点（如 `sfm:AddFile`, `sfm:Retrieve`），且策略中 `Resource` 字段通常为 `*`（全部资源），详见 [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)。

## 使用方式

1. **环境准备**：确保已开通百炼服务，创建具备最小权限的 RAM 用户并授予 `AliyunBailianDataFullAccess`（读写）或 `AliyunBailianDataReadOnlyAccess`（只读）策略；获取 AccessKey。
2. **接入点选择**：根据部署地域，选用对应的 [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)，例如华北2（北京）为 `bailian.cn-beijing.aliyuncs.com`。
3. **SDK 调用（推荐）**：下载并初始化最新版 [阿里云百炼 SDK](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29)，传入 AccessKey 和 Region ID，直接调用封装好的方法（如 `client.addCategory(...)`）。
4. **自签名调用（谨慎）**：若必须自签名，请严格遵循 [ROA 签名机制](https://help.aliyun.com/zh/sdk/product-overview/roa-mechanism)，并加入钉钉群（147535001692）获取专家支持，避免因签名错误导致 5 个工作日以上的调试延迟。
5. **典型工作流示例（构建知识库）**：
   - 调用 `AddCategory` 创建类目 → `ApplyFileUploadLease` 获取租约 → `AddFile` 上传文件；
   - 调用 `CreateIndex` 初始化知识库 → `SubmitIndexJob` 提交创建任务 → `GetIndexJobStatus` 轮询状态直至 `FINISH`；
   - 后续追加文件：`AddFile` → `SubmitIndexAddDocumentsJob`；检索：`Retrieve`。

## 限制和注意事项

- **限流策略**：各接口有独立 QPS 限制（如 `AddCategory`/`ListCategory` 为 5 次/秒，`ApplyFileUploadLease`/`DescribeFile` 为 10 次/秒），超限将返回 `429` 错误，需实现退避重试逻辑。
- **幂等性**：`List*`, `Describe*`, `Get*`, `Delete*`（除 `DeleteCategory` 外）等查询与删除类接口多为幂等；`Add*`, `Create*`, `Submit*` 等创建类接口通常**不幂等**，重复调用可能产生冗余资源，应自行实现幂等逻辑（如先 `List` 后 `Create`）。
- **数据一致性**：`DeleteFile` 仅删除应用数据中的文件，不影响已构建的知识库；反之，`DeleteIndexDocument` 仅删除知识库索引，不影响原始文件。二者不可互替。
- **功能边界**：API **不支持**通过接口新增/删除/查询数据表（Table），该操作必须通过控制台完成；`DeleteCategory` 接口虽存在，但文档 6 明确提示“不支持通过 API 新增数据表”，暗示其对表格类目的管理能力受限。
- **版本兼容性**：API 版本固定为 `2023-12-29`，但部分接口参数随时间演进（如 `CreateIndex` 在 2025-12-03 变更），请关注 [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md) 中的变更记录。

## 来源文档

- [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)
- [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)
- [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)
- [API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md)
- [数据连接（原应用数据）](../../raw/_short/api-bailian-2023-12-29-dir-data-connection-origi-a1f7f2601bd6f7cf.md)
- [AddCategory](../../raw/_short/api-bailian-2023-12-29-addcategory-e2fe0e0435ed504e.md)
- [ListCategory](../../raw/_short/api-bailian-2023-12-29-listcategory-2521532ef3e828b3.md)
- [ApplyFileUploadLease](../../raw/_short/api-bailian-2023-12-29-applyfileuploadlease-39e8ca15e0e9561a.md)
- [DeleteCategory - 删除类目](../../raw/_short/api-bailian-2023-12-29-deletecategory-9838436bd2db3113.md)
- [ListFile](../../raw/_short/api-bailian-2023-12-29-listfile-360209e3a2479f14.md)
- [DescribeFile](../../raw/_short/api-bailian-2023-12-29-describefile-020886c28a208bf2.md)
- [UpdateFileTag](../../raw/_short/api-bailian-2023-12-29-updatefiletag-f84d2af6a45d6553.md)
- [BatchUpdateFileTag](../../raw/_short/api-bailian-2023-12-29-batchupdatefiletag-34a8f009de66cb8b.md)
- [AddFile](../../raw/_short/api-bailian-2023-12-29-addfile-8c254b3500bc50bc.md)
- [AddFilesFromAuthorizedOss](../../raw/_short/api-bailian-2023-12-29-addfilesfromauthorizedoss-879556d685a301b3.md)
- [GetParseSettings - 获取类目解析设置](../../raw/_short/api-bailian-2023-12-29-getparsesettings-522514560c54f49f.md)
- [GetAvailableParserTypes - 获取文件支持的解析器类型](../../raw/_short/api-bailian-2023-12-29-getavailableparsertypes-09561c4e0fb505d5.md)
- [AddTable](../../raw/_short/api-bailian-2023-12-29-addtable-6726351659db288d.md)
- [GetConnector](../../raw/_short/api-bailian-2023-12-29-getconnector-cb2e485a0efd52f7.md)
- [UpdateConnector](../../raw/_short/api-bailian-2023-12-29-updateconnector-6a24905a7d201597.md)
- [UpdateTableFromAuthorizedOss](../../raw/_short/api-bailian-2023-12-29-updatetablefromauthorized-d7436828bcf51602.md)
- [知识库](../../raw/_short/api-bailian-2023-12-29-dir-knowledge-base-f6f202ad9694348f.md)
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
- [UpdateChunk - 修改切片](../../raw/_short/api-bailian-2023-12-29-updatechunk-589b46fcc24261f8.md)
- [DeleteChunk - 删除切片](../../raw/_short/api-bailian-2023-12-29-deletechunk-d249422088735d90.md)
- [GetIndexMonitor - 获取知识库监控数据](../../raw/_short/api-bailian-2023-12-29-getindexmonitor-3a609181d5c9c034.md)
- [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md)
- [DeleteFile](../../raw/_short/api-bailian-2023-12-29-deletefile-7e0409a458195fe2.md)
- [DeleteFiles](../../raw/_short/api-bailian-2023-12-29-deletefiles-96ef0815114e4e37.md)
- [ChangeParseSetting](../../raw/_short/api-bailian-2023-12-29-changeparsesetting-59a7c69675f499ad.md)
- [AddConnector](../../raw/_short/api-bailian-2023-12-29-addconnector-7a3c9650409710fe.md)


