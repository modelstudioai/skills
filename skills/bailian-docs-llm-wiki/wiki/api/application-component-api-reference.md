# application component api reference

本 API 参考文档面向开发者，系统性地描述了百炼平台 Application Component（应用组件）提供的核心 OpenAPI 接口能力，涵盖数据连接（原应用数据）、知识库、Prompt 模板三大功能模块。所有接口均基于 `bailian/2023-12-29` 版本，采用标准 ROA 签名机制，支持多语言 SDK 快速集成。开发者需通过 RAM 权限策略进行精细化访问控制，并严格遵循各接口的限流与幂等性要求。

## 支持的模型/功能

Application Component API 提供三大类核心能力：

- **数据连接（原应用数据）**：管理非结构化文件与结构化表格的生命周期，包括类目（Category）管理（`AddCategory`, `ListCategory`, `DeleteCategory`）、文件上传与元数据操作（`ApplyFileUploadLease`, `AddFile`, `DescribeFile`, `UpdateFileTag`, `ListFile`, `DeleteFile`, `DeleteFiles`）、OSS 批量导入（`AddFilesFromAuthorizedOss`, `UpdateTableFromAuthorizedOss`）、连接器管理（`AddConnector`, `GetConnector`, `UpdateConnector`）以及解析配置（`GetParseSettings`, `GetAvailableParserTypes`, `ChangeParseSetting`）。该模块不支持通过 API 新增或删除数据表，相关操作需通过控制台完成 [数据连接（原应用数据）](../../raw/_short/api-bailian-2023-12-29-dir-data-connection-origi-a1f7f2601bd6f7cf.md)。
- **知识库（Knowledge Base）**：提供完整的 RAG 知识库管理能力，覆盖创建（`CreateIndex`）、提交构建任务（`SubmitIndexJob`）、查询状态（`GetIndexJobStatus`）、检索（`Retrieve`）、文件与切片管理（`ListIndexDocuments`, `ListIndexFileDetails`, `ListChunks`, `AddChunk`, `UpdateChunk`, `DeleteChunk`）、更新配置（`UpdateIndex`）及监控（`GetIndexMonitor`）等全链路操作。知识库类型分为 `unstructured`（文档/音视频）和 `structured`（数据查询/图片问答），其中部分接口（如 `AddChunk`）对不同类型有明确限制 [知识库](../../raw/_short/api-bailian-2023-12-29-dir-knowledge-base-f6f202ad9694348f.md)。
- **Prompt 模板（Prompt Engineering）**：支持 Prompt 模板的增删改查（`CreatePromptTemplate`, `GetPromptTemplate`, `UpdatePromptTemplate`, `DeletePromptTemplate`, `ListPromptTemplates`），用于标准化提示词工程。当前版本暂不支持文生图类 Prompt 模板的创建 [CreatePromptTemplate - 创建Prompt模板](../../raw/_short/api-bailian-2023-12-29-createprompttemplate-1194e536beb0529a.md)。

> **注意**：文档 25 (`CreateIndex`) 明确指出“本接口仅初始化知识库创建作业。完成调用后，必须调用 `SubmitIndexJob` 接口以完成创建”，而文档 29 (`SubmitIndexJob`) 的说明中却遗漏了此关键依赖关系，仅提及“调用本接口前，您必须预先调用 `CreateIndex` 接口”。为确保流程正确，开发者必须严格遵循“先 `CreateIndex`，再 `SubmitIndexJob`”的两步调用顺序。

## 关键参数

- **`WorkspaceId`（业务空间 ID）**：几乎所有接口的必需路径参数，标识操作所属的业务空间。获取方式请参见[如何使用业务空间](https://help.aliyun.com/zh/model-studio/use-workspace)。
- **`CategoryId` / `FileId` / `IndexId` / `ConnectorId`**：各类资源的唯一标识符，通常由上游接口（如 `AddCategory`, `AddFile`, `CreateIndex`, `AddConnector`）返回，后续操作需复用。
- **`Parser`（解析器类型）**：在 `AddFile` 和 `ChangeParseSetting` 等接口中指定，决定文件内容的解析逻辑。有效值包括 `DOCMIND`, `DOCMIND_DIGITAL`, `DOCMIND_LLM_VERSION`, `DASH_QWEN_VL_PARSER`, `AUTO_SELECT` 等，具体支持列表可通过 `GetAvailableParserTypes` 查询。
- **分页与过滤参数**：`List*` 类接口普遍支持 `MaxResults`/`PageSize`（每页数量）、`NextToken`/`PageNumber`（分页凭证）以及 `DocumentName`, `DocumentStatus`, `CategoryType` 等过滤参数，用于高效检索海量资源。
- **权限点（Action）**：每个 API 对应一个 RAM 权限点，如 `sfm:AddCategory`, `sfm:Retrieve`, `sfm:CreatePromptTemplate`，用于在 RAM 策略中精确授权。

## 使用方式

1. **环境准备**：
   - 获取阿里云账号或 RAM 用户的 AccessKey（建议遵循最小权限原则，创建专用 RAM 用户并授予 `AliyunBailianDataFullAccess` 或更细粒度策略）。
   - 配置网络访问：根据部署地域选择公网或 VPC 接入点，例如华北2（北京）的公网地址为 `bailian.cn-beijing.aliyuncs.com` [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)。
2. **SDK 集成（推荐）**：
   - 下载并安装最新版 [阿里云百炼 SDK](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29)，可自动处理签名、重试、限流等复杂逻辑。
   - 初始化客户端时传入 `accessKeyId`, `accessKeySecret`, `regionId`（如 `cn-beijing`）及 `endpoint`。
3. **API 调用**：
   - 构造请求对象，填入必需的路径参数（如 `WorkspaceId`）和请求参数（如 `FileName`, `Query`, `Name`）。
   - 发起同步或异步调用，处理返回结果（`Success`, `Code`, `Data`）及错误（`Message`, `ErrorCode`）。
4. **调试与验证**：
   - 使用 [OpenAPI Explorer](https://api.aliyun.com/api/bailian/2023-12-29) 在线调试，实时查看请求/响应，并一键生成各语言 SDK 示例代码。

## 限制和注意事项

- **限流策略**：各接口均有严格的 QPS 限制，例如 `AddCategory`/`ListCategory`/`DeleteCategory` 为 5 次/秒，`ApplyFileUploadLease`/`AddFile`/`DeleteFiles` 为 10 次/秒，`ListIndices` 为 10 次/秒。超出限制将返回 `429 Too Many Requests`，需实现指数退避重试。
- **幂等性**：多数查询类（`List*`, `Describe*`, `Get*`）和部分操作类（`DeleteCategory`, `DeleteFile`, `UpdateChunk`, `DeleteChunk`）接口具有幂等性；而 `AddCategory`, `CreateIndex`, `AddFile` 等创建类接口不具备幂等性，重复调用可能产生重复资源，建议通过“先查后创”逻辑规避。
- **资源关联性**：知识库操作强依赖前置步骤。例如，`SubmitIndexJob` 必须在 `CreateIndex` 之后调用；`Retrieve` 前知识库必须已成功构建（`Status` 为 `FINISH`）；`DeleteIndexDocument` 仅能删除状态为 `FINISH` 或 `INSERT_ERROR` 的文件。
- **功能边界**：
  - 数据表（Table）的创建（`AddTable`）和更新（`UpdateTableFromAuthorizedOss`）仅支持表格连接器，且不支持通过 API 删除数据表。
  - `ApplyFileUploadLease` 接口在用于智能体应用会话交互时，`CategoryId` 参数必须传入 `default`。
  - `DeleteIndex` 接口要求知识库必须先从应用中解除关联，此操作当前仅支持控制台完成。
- **安全与合规**：所有敏感操作（如删除、更新）均需显式授权，且建议在生产环境禁用主账号 AccessKey，全程使用具备最小权限的 RAM 用户。

## 来源文档

- [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)
- [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)
- [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)
- [数据连接（原应用数据）](../../raw/_short/api-bailian-2023-12-29-dir-data-connection-origi-a1f7f2601bd6f7cf.md)
- [API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md)
- [AddCategory](../../raw/_short/api-bailian-2023-12-29-addcategory-e2fe0e0435ed504e.md)
- [ListCategory](../../raw/_short/api-bailian-2023-12-29-listcategory-2521532ef3e828b3.md)
- [ApplyFileUploadLease](../../raw/_short/api-bailian-2023-12-29-applyfileuploadlease-39e8ca15e0e9561a.md)
- [AddFile](../../raw/_short/api-bailian-2023-12-29-addfile-8c254b3500bc50bc.md)
- [DeleteCategory - 删除类目](../../raw/_short/api-bailian-2023-12-29-deletecategory-9838436bd2db3113.md)
- [AddFilesFromAuthorizedOss](../../raw/_short/api-bailian-2023-12-29-addfilesfromauthorizedoss-879556d685a301b3.md)
- [DescribeFile](../../raw/_short/api-bailian-2023-12-29-describefile-020886c28a208bf2.md)
- [UpdateFileTag](../../raw/_short/api-bailian-2023-12-29-updatefiletag-f84d2af6a45d6553.md)
- [ListFile](../../raw/_short/api-bailian-2023-12-29-listfile-360209e3a2479f14.md)
- [DeleteFiles](../../raw/_short/api-bailian-2023-12-29-deletefiles-96ef0815114e4e37.md)
- [GetParseSettings - 获取类目解析设置](../../raw/_short/api-bailian-2023-12-29-getparsesettings-522514560c54f49f.md)
- [GetAvailableParserTypes - 获取文件支持的解析器类型](../../raw/_short/api-bailian-2023-12-29-getavailableparsertypes-09561c4e0fb505d5.md)
- [ChangeParseSetting](../../raw/_short/api-bailian-2023-12-29-changeparsesetting-59a7c69675f499ad.md)
- [AddTable](../../raw/_short/api-bailian-2023-12-29-addtable-6726351659db288d.md)
- [UpdateTableFromAuthorizedOss](../../raw/_short/api-bailian-2023-12-29-updatetablefromauthorized-d7436828bcf51602.md)
- [AddConnector](../../raw/_short/api-bailian-2023-12-29-addconnector-7a3c9650409710fe.md)
- [GetConnector](../../raw/_short/api-bailian-2023-12-29-getconnector-cb2e485a0efd52f7.md)
- [UpdateConnector](../../raw/_short/api-bailian-2023-12-29-updateconnector-6a24905a7d201597.md)
- [知识库](../../raw/_short/api-bailian-2023-12-29-dir-knowledge-base-f6f202ad9694348f.md)
- [CreateIndex - 创建知识库](../../raw/_short/api-bailian-2023-12-29-createindex-8bc613c75f8af371.md)
- [BatchUpdateFileTag](../../raw/_short/api-bailian-2023-12-29-batchupdatefiletag-34a8f009de66cb8b.md)
- [DeleteFile](../../raw/_short/api-bailian-2023-12-29-deletefile-7e0409a458195fe2.md)
- [GetIndexJobStatus - 查询知识库创建或追加任务状态](../../raw/_short/api-bailian-2023-12-29-getindexjobstatus-1e88b6ccfffe0fe4.md)
- [SubmitIndexJob - 提交知识库创建任务](../../raw/_short/api-bailian-2023-12-29-submitindexjob-63b38294171880d4.md)
- [Retrieve - 检索知识库](../../raw/_short/api-bailian-2023-12-29-retrieve-c8e6b8d718a30a84.md)
- [ListIndexDocuments - 查询知识库文件列表](../../raw/_short/api-bailian-2023-12-29-listindexdocuments-9f0db0388c421903.md)
- [UpdateIndex - 更新知识库](../../raw/_short/api-bailian-2023-12-29-updateindex-551997e1d335e340.md)
- [DeleteIndexDocument - 删除知识库下的文件](../../raw/_short/api-bailian-2023-12-29-deleteindexdocument-0792a83f5a741348.md)
- [ListIndices - 查询知识库列表](../../raw/_short/api-bailian-2023-12-29-listindices-c555173be752eaaf.md)
- [DeleteIndex - 删除知识库](../../raw/_short/api-bailian-2023-12-29-deleteindex-500502bd6df1c49c.md)
- [ListChunks - 查询索引下的分片列表](../../raw/_short/api-bailian-2023-12-29-listchunks-30a6c87b93a583c6.md)
- [AddChunk - 新增切片](../../raw/_short/api-bailian-2023-12-29-addchunk-1607bcddf6713fd9.md)
- [UpdateChunk - 修改切片](../../raw/_short/api-bailian-2023-12-29-updatechunk-589b46fcc24261f8.md)
- [DeleteChunk - 删除切片](../../raw/_short/api-bailian-2023-12-29-deletechunk-d249422088735d90.md)
- [GetIndexMonitor - 获取知识库监控数据](../../raw/_short/api-bailian-2023-12-29-getindexmonitor-3a609181d5c9c034.md)
- [Prompt 模板](../../raw/_short/api-bailian-2023-12-29-dir-prompt-engineering-11ee962a5f5d5d1e.md)
- [CreatePromptTemplate - 创建Prompt模板](../../raw/_short/api-bailian-2023-12-29-createprompttemplate-1194e536beb0529a.md)
- [ListIndexFileDetails - 查询知识库文件详情](../../raw/_short/api-bailian-2023-12-29-listindexfiledetails-0e2036d0ef0d8fe8.md)
- [GetPromptTemplate - 获取Prompt模板](../../raw/_short/api-bailian-2023-12-29-getprompttemplate-584c357dd7cb48d6.md)
- [UpdatePromptTemplate - 更新Prompt模板](../../raw/_short/api-bailian-2023-12-29-updateprompttemplate-519fb4af5ea50522.md)
- [DeletePromptTemplate - 删除Prompt模板](../../raw/_short/api-bailian-2023-12-29-deleteprompttemplate-b441fa1b9c777b81.md)
- [ListPromptTemplates - 获取Prompt模板列表](../../raw/_short/api-bailian-2023-12-29-listprompttemplates-ab5ba5362e93cfcd.md)
- [GetAlipayUrl - 获取支付宝打赏URL](../../raw/_short/api-bailian-2023-12-29-getalipayurl-e6e9715d5164f74a.md)
- [其他](../../raw/_short/api-bailian-2023-12-29-dir-others-b9c3a16db11771f5.md)
- [GetAlipayTransferStatus - 查询支付宝打赏状态](../../raw/_short/api-bailian-2023-12-29-getalipaytransferstatus-04aa88852762fd85.md)
- [ApplyTempStorageLease - 申请临时文件上传许可](../../raw/_short/api-bailian-2023-12-29-applytempstoragelease-5a38ce0eefc66408.md)
- [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md)
- [SubmitIndexAddDocumentsJob - 提交知识库文件追加任务](../../raw/_short/api-bailian-2023-12-29-submitindexadddocumentsjo-ec4f5cf285e2c447.md)


