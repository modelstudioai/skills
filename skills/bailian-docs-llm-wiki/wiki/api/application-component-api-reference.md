# application component api reference

本 API 参考文档面向开发者，系统性地描述了百炼平台中应用组件（Application Component）的核心 OpenAPI 接口能力，覆盖数据连接（原应用数据）、知识库、Prompt 模板等关键模块。所有接口均基于 `bailian/2023-12-29` 版本，采用标准 ROA 签名机制，支持通过官方 SDK 快速集成。开发者需预先配置 RAM 权限与业务空间访问权限方可调用。

## 支持的模型/功能

本组件提供三大类核心能力：

- **数据连接（原应用数据）**：管理非结构化文件与结构化表格的生命周期，包括类目（Category）管理（`AddCategory`、`ListCategory`、`DeleteCategory`）、[文件上传](../concepts/file-upload.md)与元数据操作（`ApplyFileUploadLease`、`AddFile`、`ListFile`、`DescribeFile`、`UpdateFileTag`、`BatchUpdateFileTag`、`DeleteFile`、`DeleteFiles`），以及连接器（Connector）管理（`AddConnector`、`GetConnector`、`UpdateConnector`）。此外支持从已授权 OSS 批量导入文件或更新表格（`AddFilesFromAuthorizedOss`、`UpdateTableFromAuthorizedOss`）。[API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md) 中明确指出，该层不支持通过 API 新增或删除数据表，相关操作需通过控制台完成。

- **知识库（Knowledge Base）**：支持创建、查询、更新和删除两类知识库（非结构化 `unstructured` 与结构化 `structured`），并提供完整的索引构建、检索与细粒度管理能力。关键流程为：先调用 `CreateIndex` 初始化，再通过 `SubmitIndexJob` 提交创建任务；追加文档使用 `SubmitIndexAddDocumentsJob`；检索使用 `Retrieve`；查询状态使用 `GetIndexJobStatus`；管理文件列表使用 `ListIndexDocuments` 和 `ListIndexFileDetails`；管理底层文本切片（Chunk）使用 `ListChunks`、`AddChunk`、`UpdateChunk` 和 `DeleteChunk`。[知识库](../../raw/_short/api-bailian-2023-12-29-dir-knowledge-base-f6f202ad9694348f.md) 文档汇总了全部相关接口。

- **[Prompt 工程](../concepts/prompt-engineering.md)**：提供 Prompt 模板的全生命周期管理，包括创建、获取、更新、删除及列表查询（`CreatePromptTemplate`、`GetPromptTemplate`、`UpdatePromptTemplate`、`DeletePromptTemplate`、`ListPromptTemplates`），用于标准化提示词复用与版本控制。

> **注意**：`AddChunk` 和 `UpdateChunk` 接口的文档存在矛盾。文档 38 明确说明 `AddChunk` 支持文档搜索、数据查询、图片问答三类知识库；而文档 39 的 `UpdateChunk` 则明确限定“仅支持文档搜索类知识库，不支持数据查询和图片问答类知识库”。此为设计上的功能不对称，开发者在更新结构化知识库内容时，应优先使用 `SubmitIndexAddDocumentsJob` 或 `UpdateTableFromAuthorizedOss` 等替代方案。

## 关键参数

- **通用路径参数**：几乎所有接口均要求 `WorkspaceId`（业务空间 ID），需通过控制台获取，是资源隔离与权限控制的基础。
- **类目与文件标识**：`CategoryId`（来自 `AddCategory` 返回）、`FileId`（来自 `AddFile` 返回）、`ConnectorId`（来自 `AddConnector` 返回）是操作关联资源的必需字段。
- **知识库标识**：`IndexId`（来自 `CreateIndex` 返回）是所有知识库操作的核心标识符；`JobId`（来自 `SubmitIndexJob` 返回）用于轮询任务状态。
- **分页与过滤**：`List*` 类接口普遍支持 `MaxResults`/`PageSize`、`NextToken`/`PageNumber` 进行分页；支持按名称（`FileName`、`DocumentName`）、状态（`DocumentStatus`）、标签等进行过滤。
- **解析器控制**：`AddFile` 和 `ChangeParseSetting` 接口中的 `Parser` 参数（如 `DOCMIND`、`AUTO_SELECT`）决定了文件内容的解析策略，其可选值需结合 `GetAvailableParserTypes` 接口动态查询。

## 使用方式

1. **环境准备**：
   - 获取阿里云账号或 RAM 子账号的 AccessKey（建议遵循最小权限原则，使用 RAM 用户并授予 `AliyunBailianDataFullAccess` 策略）。
   - 确认服务接入点：根据地域选择公网或 VPC 地址，例如北京地域为 `bailian.cn-beijing.aliyuncs.com` [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)。
   - 将业务空间 ID (`WorkspaceId`) 加入 RAM 用户的授权范围。

2. **典型工作流（以构建知识库为例）**：
   - 调用 `AddCategory` 创建文件分类目录。
   - 调用 `ApplyFileUploadLease` 获取上传租约。
   - 将[文件上传](../concepts/file-upload.md)至租约指定地址。
   - 调用 `AddFile` 将文件正式导入应用数据。
   - 调用 `CreateIndex` 初始化知识库。
   - 调用 `SubmitIndexJob` 提交创建任务。
   - 调用 `GetIndexJobStatus` 轮询任务状态直至完成。

3. **SDK 集成**：强烈推荐使用官方 SDK（[下载链接](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29)），它自动处理签名、重试、错误解析等细节，大幅降低接入成本。

## 限制和注意事项

- **限流策略**：各接口有独立的 QPS 限制（如 `ListCategory` 为 5 次/秒，`Retrieve` 为 15 次/秒），超出将返回限流错误。请在客户端实现指数退避重试逻辑。
- **幂等性**：多数查询类（`List*`, `Describe*`, `Get*`）和部分操作类（`Delete*`, `Update*`）接口具有幂等性，但 `Add*`、`Apply*`、`Submit*` 等初始化类接口不具备，重复调用可能导致资源冗余。
- **数据一致性**：`DeleteFile` 仅删除应用数据中的文件，不影响已构建的知识库；反之，`DeleteIndexDocument` 仅删除知识库索引，不影响应用数据中的源文件。二者需按需组合使用。
- **安全与权限**：所有 API 调用必须携带有效 AccessKey，并确保 RAM 策略中已精确授予对应 `Action`（如 `sfm:ListCategory`），否则将返回权限拒绝错误。
- **国际站支持**：`UpdateIndex` 和 `GetIndexMonitor` 接口明确声明不支持国际站，中国站用户需确认地域配置。

## 来源文档

- [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)
- [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)
- [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)
- [ListCategory](../../raw/_short/api-bailian-2023-12-29-listcategory-2521532ef3e828b3.md)
- [DeleteCategory - 删除类目](../../raw/_short/api-bailian-2023-12-29-deletecategory-9838436bd2db3113.md)
- [数据连接（原应用数据）](../../raw/_short/api-bailian-2023-12-29-dir-data-connection-origi-a1f7f2601bd6f7cf.md)
- [AddFile](../../raw/_short/api-bailian-2023-12-29-addfile-8c254b3500bc50bc.md)
- [AddCategory](../../raw/_short/api-bailian-2023-12-29-addcategory-e2fe0e0435ed504e.md)
- [ListFile](../../raw/_short/api-bailian-2023-12-29-listfile-360209e3a2479f14.md)
- [DescribeFile](../../raw/_short/api-bailian-2023-12-29-describefile-020886c28a208bf2.md)
- [UpdateFileTag](../../raw/_short/api-bailian-2023-12-29-updatefiletag-f84d2af6a45d6553.md)
- [BatchUpdateFileTag](../../raw/_short/api-bailian-2023-12-29-batchupdatefiletag-34a8f009de66cb8b.md)
- [DeleteFile](../../raw/_short/api-bailian-2023-12-29-deletefile-7e0409a458195fe2.md)
- [DeleteFiles](../../raw/_short/api-bailian-2023-12-29-deletefiles-96ef0815114e4e37.md)
- [GetParseSettings - 获取类目解析设置](../../raw/_short/api-bailian-2023-12-29-getparsesettings-522514560c54f49f.md)
- [GetAvailableParserTypes - 获取文件支持的解析器类型](../../raw/_short/api-bailian-2023-12-29-getavailableparsertypes-09561c4e0fb505d5.md)
- [ChangeParseSetting](../../raw/_short/api-bailian-2023-12-29-changeparsesetting-59a7c69675f499ad.md)
- [AddTable](../../raw/_short/api-bailian-2023-12-29-addtable-6726351659db288d.md)
- [ApplyFileUploadLease](../../raw/_short/api-bailian-2023-12-29-applyfileuploadlease-39e8ca15e0e9561a.md)
- [UpdateTableFromAuthorizedOss](../../raw/_short/api-bailian-2023-12-29-updatetablefromauthorized-d7436828bcf51602.md)
- [AddConnector](../../raw/_short/api-bailian-2023-12-29-addconnector-7a3c9650409710fe.md)
- [AddFilesFromAuthorizedOss](../../raw/_short/api-bailian-2023-12-29-addfilesfromauthorizedoss-879556d685a301b3.md)
- [GetConnector](../../raw/_short/api-bailian-2023-12-29-getconnector-cb2e485a0efd52f7.md)
- [UpdateConnector](../../raw/_short/api-bailian-2023-12-29-updateconnector-6a24905a7d201597.md)
- [CreateIndex](../../raw/_short/api-bailian-2023-12-29-createindex-8bc613c75f8af371.md)
- [GetIndexJobStatus](../../raw/_short/api-bailian-2023-12-29-getindexjobstatus-1e88b6ccfffe0fe4.md)
- [知识库](../../raw/_short/api-bailian-2023-12-29-dir-knowledge-base-f6f202ad9694348f.md)
- [SubmitIndexAddDocumentsJob](../../raw/_short/api-bailian-2023-12-29-submitindexadddocumentsjo-ec4f5cf285e2c447.md)
- [SubmitIndexJob - 提交知识库创建任务](../../raw/_short/api-bailian-2023-12-29-submitindexjob-63b38294171880d4.md)
- [Retrieve](../../raw/_short/api-bailian-2023-12-29-retrieve-c8e6b8d718a30a84.md)
- [ListIndexDocuments](../../raw/_short/api-bailian-2023-12-29-listindexdocuments-9f0db0388c421903.md)
- [ListIndexFileDetails](../../raw/_short/api-bailian-2023-12-29-listindexfiledetails-0e2036d0ef0d8fe8.md)
- [DeleteIndexDocument - 删除知识库下的文件](../../raw/_short/api-bailian-2023-12-29-deleteindexdocument-0792a83f5a741348.md)
- [UpdateIndex - 更新知识库](../../raw/_short/api-bailian-2023-12-29-updateindex-551997e1d335e340.md)
- [ListIndices](../../raw/_short/api-bailian-2023-12-29-listindices-c555173be752eaaf.md)
- [DeleteIndex - 删除知识库](../../raw/_short/api-bailian-2023-12-29-deleteindex-500502bd6df1c49c.md)
- [ListChunks - 查询索引下的分片列表](../../raw/_short/api-bailian-2023-12-29-listchunks-30a6c87b93a583c6.md)
- [AddChunk](../../raw/_short/api-bailian-2023-12-29-addchunk-1607bcddf6713fd9.md)
- [UpdateChunk - 修改切片](../../raw/_short/api-bailian-2023-12-29-updatechunk-589b46fcc24261f8.md)
- [DeleteChunk - 删除切片](../../raw/_short/api-bailian-2023-12-29-deletechunk-d249422088735d90.md)
- [Prompt 模板](../../raw/_short/api-bailian-2023-12-29-dir-prompt-engineering-11ee962a5f5d5d1e.md)
- [GetIndexMonitor - 获取知识库监控数据](../../raw/_short/api-bailian-2023-12-29-getindexmonitor-3a609181d5c9c034.md)
- [CreatePromptTemplate - 创建Prompt模板](../../raw/_short/api-bailian-2023-12-29-createprompttemplate-1194e536beb0529a.md)
- [UpdatePromptTemplate - 更新Prompt模板](../../raw/_short/api-bailian-2023-12-29-updateprompttemplate-519fb4af5ea50522.md)
- [DeletePromptTemplate - 删除Prompt模板](../../raw/_short/api-bailian-2023-12-29-deleteprompttemplate-b441fa1b9c777b81.md)
- [GetPromptTemplate - 获取Prompt模板](../../raw/_short/api-bailian-2023-12-29-getprompttemplate-584c357dd7cb48d6.md)
- [其他](../../raw/_short/api-bailian-2023-12-29-dir-others-b9c3a16db11771f5.md)
- [ListPromptTemplates - 获取Prompt模板列表](../../raw/_short/api-bailian-2023-12-29-listprompttemplates-ab5ba5362e93cfcd.md)
- [GetAlipayUrl - 获取支付宝打赏URL](../../raw/_short/api-bailian-2023-12-29-getalipayurl-e6e9715d5164f74a.md)
- [GetAlipayTransferStatus - 查询支付宝打赏状态](../../raw/_short/api-bailian-2023-12-29-getalipaytransferstatus-04aa88852762fd85.md)
- [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md)
- [ApplyTempStorageLease - 申请临时文件上传许可](../../raw/_short/api-bailian-2023-12-29-applytempstoragelease-5a38ce0eefc66408.md)
- [API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md)


