# application component api reference

本 API 参考文档面向开发者，提供百炼平台应用组件（Application Component）的核心能力接口规范，涵盖数据连接（原应用数据）、知识库两大核心模块。所有接口均基于 `bailian/2023-12-29` 版本，采用 ROA 风格，支持标准阿里云 OpenAPI 签名机制。建议优先使用官方 SDK 调用，避免手动签名复杂性 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)。

## 支持的模型/功能

当前 Application Component API 主要支撑两类核心能力：

- **数据连接（原应用数据）**：提供结构化与非结构化数据的统一接入、分类管理与元数据操作。支持类目（Category）生命周期管理（`AddCategory`/`ListCategory`/`DeleteCategory`）、文件上传与元数据维护（`ApplyFileUploadLease`/`AddFile`/`ListFile`/`DescribeFile`）、标签管理（`UpdateFileTag`/`BatchUpdateFileTag`）、解析配置（`GetParseSettings`/`ChangeParseSetting`）及 OSS 批量导入（`AddFilesFromAuthorizedOss`）。注意：**不支持通过 API 新增或删除数据表**，该操作仅限控制台完成 [AddCategory](../../raw/_short/api-bailian-2023-12-29-addcategory-e2fe0e0435ed504e.md)。
- **知识库（Knowledge Base）**：提供文档搜索、音视频、数据查询、图片问答四类知识库的全生命周期管理。覆盖创建（`CreateIndex`）、提交构建（`SubmitIndexJob`）、追加文件（`SubmitIndexAddDocumentsJob`）、检索（`Retrieve`）、监控（`GetIndexMonitor`）及细粒度操作（切片增删改查 `AddChunk`/`UpdateChunk`/`DeleteChunk`/`ListChunks`）。其中，`Retrieve` 接口具有幂等性，且支持向量与关键词混合检索 [Retrieve](../../raw/_short/api-bailian-2023-12-29-retrieve-c8e6b8d718a30a84.md)。

> **注意**：`ListIndexDocuments` 和 `ListIndexFileDetails` 两个接口在授权信息中均引用了 `sfm:ListIndexFiles` 权限点，但其权限策略名称在文档 42 和 43 中存在不一致（前者为 `sfm:ListIndexFiles`，后者为 `sfm:ListIndexFileDetails`）。实际调用时请以 `sfm:ListIndexFiles` 为准，该权限已覆盖两者所需能力。

## 关键参数

- **通用路径参数**：几乎所有接口均需 `WorkspaceId`（业务空间 ID），用于标识资源归属，必须从控制台获取。
- **类目与文件标识**：`CategoryId`（来自 `AddCategory` 返回）和 `FileId`（来自 `AddFile` 返回）是绝大多数数据连接操作的必填路径或请求参数。
- **知识库标识**：`IndexId`（来自 `CreateIndex` 返回）是所有知识库操作的核心标识。
- **分页与过滤**：`List*` 类接口普遍支持 `MaxResults`/`PageSize`（默认 20/10）、`NextToken`/`PageNumber` 及 `DocumentName`/`FileName` 等过滤参数。
- **解析器选择**：`AddFile` 的 `Parser` 参数支持 `AUTO_SELECT`、`DOCMIND`、`DOCMIND_DIGITAL`、`DOCMIND_LLM_VERSION`、`DASH_QWEN_VL_PARSER` 等值；`GetAvailableParserTypes` 可动态查询指定 `FileType`（如 `pdf`）所支持的解析器列表 [GetAvailableParserTypes](../../raw/_short/api-bailian-2023-12-29-getavailableparsertypes-09561c4e0fb505d5.md)。
- **限流控制**：各接口有明确的 QPS 限制（如 `AddCategory` 为 5 次/秒，`ApplyFileUploadLease` 为 10 次/秒），超限将返回 `429` 错误，需实现退避重试逻辑。

## 使用方式

1. **环境准备**：使用 RAM 子账号并授予最小权限策略（如 `AliyunBailianDataFullAccess`），避免使用主账号 AccessKey。确保子账号已加入目标业务空间。
2. **接入点配置**：根据部署地域选择对应服务地址，例如华北2（北京）公网地址为 `bailian.cn-beijing.aliyuncs.com` [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)。
3. **调用流程**（以知识库为例）：
   - 调用 `CreateIndex` 初始化知识库；
   - 调用 `SubmitIndexJob` 提交构建任务；
   - 调用 `GetIndexJobStatus` 轮询任务状态直至完成；
   - 调用 `Retrieve` 进行检索。
4. **文件上传流程**（以非结构化数据为例）：
   - 调用 `ApplyFileUploadLease` 获取临时上传凭证；
   - 使用该凭证将文件上传至百炼临时存储；
   - 调用 `AddFile` 将临时文件导入至指定 `CategoryId` 下的数据连接。
5. **调试工具**：所有接口均支持在 OpenAPI Explorer 中直接调试，可自动生成各语言 SDK 示例代码。

## 限制和注意事项

- **幂等性**：`List*`、`Describe*`、`Get*`、`DeleteIndexDocument`、`DeleteChunk` 等读取与删除类接口大多具备幂等性；而 `Add*`、`Create*`、`Submit*` 等创建类接口不具备幂等性，重复调用可能产生冗余资源，需自行实现“先查后建”逻辑。
- **数据一致性**：`DeleteFile` 仅删除应用数据中的文件，**不会**影响已构建的知识库内容；反之，`DeleteIndexDocument` 仅删除知识库索引中的文件，**不会**删除应用数据中的原始文件。二者需按需独立调用。
- **功能边界**：知识库的 `structured`（数据查询/图片问答）类型不支持 `SubmitIndexAddDocumentsJob`，其数据更新需通过 `UpdateTableFromAuthorizedOss` 或控制台完成；`AddChunk`/`UpdateChunk` 仅支持 `document` 类型知识库，不支持 `table` 或 `image` 类型。
- **安全要求**：所有 API 调用必须通过 HTTPS，并使用阿里云标准签名机制。RAM 用户必须严格遵循最小权限原则配置策略，禁止授予 `*` 全资源权限。
- **版本兼容性**：API 行为以 `2023-12-29` 版本为准，历史变更记录见 [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md)，重大变更（如 `Retrieve` 参数调整）已明确标注。

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
- [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)
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
- [AddFilesFromAuthorizedOss](../../raw/_short/api-bailian-2023-12-29-addfilesfromauthorizedoss-879556d685a301b3.md)
- [UpdateTableFromAuthorizedOss](../../raw/_short/api-bailian-2023-12-29-updatetablefromauthorized-d7436828bcf51602.md)
- [AddConnector](../../raw/_short/api-bailian-2023-12-29-addconnector-7a3c9650409710fe.md)
- [GetConnector](../../raw/_short/api-bailian-2023-12-29-getconnector-cb2e485a0efd52f7.md)
- [知识库](../../raw/_short/api-bailian-2023-12-29-dir-knowledge-base-f6f202ad9694348f.md)
- [CreateIndex - 创建知识库](../../raw/_short/api-bailian-2023-12-29-createindex-8bc613c75f8af371.md)
- [GetIndexJobStatus - 查询知识库创建或追加任务状态](../../raw/_short/api-bailian-2023-12-29-getindexjobstatus-1e88b6ccfffe0fe4.md)
- [UpdateConnector](../../raw/_short/api-bailian-2023-12-29-updateconnector-6a24905a7d201597.md)
- [SubmitIndexAddDocumentsJob - 提交知识库文件追加任务](../../raw/_short/api-bailian-2023-12-29-submitindexadddocumentsjo-ec4f5cf285e2c447.md)
- [Retrieve - 检索知识库](../../raw/_short/api-bailian-2023-12-29-retrieve-c8e6b8d718a30a84.md)
- [SubmitIndexJob - 提交知识库创建任务](../../raw/_short/api-bailian-2023-12-29-submitindexjob-63b38294171880d4.md)
- [UpdateIndex - 更新知识库](../../raw/_short/api-bailian-2023-12-29-updateindex-551997e1d335e340.md)
- [DeleteIndexDocument - 删除知识库下的文件](../../raw/_short/api-bailian-2023-12-29-deleteindexdocument-0792a83f5a741348.md)
- [ListIndices - 查询知识库列表](../../raw/_short/api-bailian-2023-12-29-listindices-c555173be752eaaf.md)
- [DeleteIndex - 删除知识库](../../raw/_short/api-bailian-2023-12-29-deleteindex-500502bd6df1c49c.md)
- [ListChunks - 查询索引下的分片列表](../../raw/_short/api-bailian-2023-12-29-listchunks-30a6c87b93a583c6.md)
- [AddChunk - 新增切片](../../raw/_short/api-bailian-2023-12-29-addchunk-1607bcddf6713fd9.md)
- [UpdateChunk - 修改切片](../../raw/_short/api-bailian-2023-12-29-updatechunk-589b46fcc24261f8.md)
- [DeleteChunk - 删除切片](../../raw/_short/api-bailian-2023-12-29-deletechunk-d249422088735d90.md)
- [GetIndexMonitor - 获取知识库监控数据](../../raw/_short/api-bailian-2023-12-29-getindexmonitor-3a609181d5c9c034.md)
- [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md)
- [ListIndexDocuments - 查询知识库文件列表](../../raw/_short/api-bailian-2023-12-29-listindexdocuments-9f0db0388c421903.md)
- [ListIndexFileDetails - 查询知识库文件详情](../../raw/_short/api-bailian-2023-12-29-listindexfiledetails-0e2036d0ef0d8fe8.md)


