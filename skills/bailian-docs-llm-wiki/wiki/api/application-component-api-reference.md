# application component api reference

本 API 参考文档面向开发者，系统性地描述了百炼平台 Application Component（应用组件）层提供的核心 OpenAPI 能力，覆盖数据连接（原应用数据）、知识库、Prompt 模板三大功能域。所有接口均基于 `bailian/2023-12-29` 版本，采用标准 ROA 签名机制，支持通过官方 SDK 快速集成。开发者需预先配置 RAM 权限与业务空间成员身份方可调用。

## 支持的模型/功能

Application Component API 主要提供三类能力：

- **数据连接（原应用数据）**：管理非结构化文件与结构化表格的生命周期，包括类目（Category）管理（`AddCategory`、`ListCategory`、`DeleteCategory`）、文件上传与元数据操作（`ApplyFileUploadLease`、`AddFile`、`ListFile`、`DescribeFile`）、OSS 批量导入（`AddFilesFromAuthorizedOss`）、解析器配置（`GetParseSettings`、`ChangeParseSetting`）以及连接器管理（`AddConnector`、`GetConnector`）。注意：[API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md) 明确指出“不支持通过 API 新增数据表”，但后续文档 [AddTable](../../raw/_short/api-bailian-2023-12-29-addtable-6726351659db288d.md) 提供了该能力，此为矛盾点。
- **知识库（Knowledge Base）**：支持从零构建、追加更新、检索与运维全链路。涵盖知识库创建与提交（`CreateIndex`、`SubmitIndexJob`）、文件追加（`SubmitIndexAddDocumentsJob`）、检索（`Retrieve`）、列表与详情查询（`ListIndices`、`ListIndexFileDetails`）、文件级操作（`DeleteIndexDocument`）、分片（Chunk）管理（`ListChunks`、`AddChunk`、`UpdateChunk`、`DeleteChunk`）及监控（`GetIndexMonitor`）。其中，`Retrieve` 接口明确区分了 OpenAPI 与 Spring AI Alibaba 的调用路径，后者使用独立的 DashScope Pipeline 路径 [Retrieve - 检索知识库](../../raw/_short/api-bailian-2023-12-29-retrieve-c8e6b8d718a30a84.md)。
- **Prompt 模板（Prompt Engineering）**：提供 Prompt 模板的 CRUD 操作，包括创建（`CreatePromptTemplate`）、获取（`GetPromptTemplate`）、更新（`UpdatePromptTemplate`）、删除（`DeletePromptTemplate`）和列表（`ListPromptTemplates`）。需注意，[CreatePromptTemplate - 创建Prompt模板](../../raw/_short/api-bailian-2023-12-29-createprompttemplate-1194e536beb0529a.md) 明确声明“本接口暂不支持文生图 Prompt 模板的创建”。

> **注意**：文档中关于“是否支持 API 新增数据表”存在矛盾。[API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md) 在 `AddCategory` 接口说明中强调“不支持通过 API 新增数据表”，而单独的 [AddTable](../../raw/_short/api-bailian-2023-12-29-addtable-6726351659db288d.md) 文档则完整描述了该功能。请以 `AddTable` 接口的实际可用性为准，并确认其在最新 SDK 中的支持状态。

## 关键参数

- **通用路径参数**：几乎所有接口均要求 `WorkspaceId`（业务空间 ID），用于标识资源归属，必须通过控制台或 API 获取。
- **鉴权参数**：所有请求需携带有效的 AccessKey（推荐使用最小权限的 RAM 用户凭证），并遵循 ROA 签名规范。RAM 权限策略需包含对应 Action（如 `sfm:AddCategory`, `sfm:Retrieve`），详见 [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)。
- **核心业务参数**：
  - **数据连接**：`CategoryId`（类目 ID）、`FileId`（文件 ID）、`ConnectorId`（连接器 ID）、`Parser`（解析器类型，如 `AUTO_SELECT`, `DOCMIND`）。
  - **知识库**：`IndexId`（知识库 ID）、`JobId`（任务 ID）、`DocumentIds`（文件 ID 列表）、`Query`（检索文本）、`DenseSimilarityTopK`（向量检索 Top K）。
  - **Prompt 模板**：`promptTemplateId`（模板 ID）、`workspaceId`（业务空间 ID）、`content`（模板内容，支持 `${variable}` 占位符）。
- **分页与过滤**：`List*` 类接口普遍支持 `MaxResults`/`PageSize`、`NextToken`/`PageNumber` 进行分页；部分接口（如 `ListIndexFileDetails`）支持 `DocumentStatus`、`DocumentName`、`EnableNameLike` 进行结果过滤。

## 使用方式

1. **环境准备**：在阿里云控制台创建 RAM 用户，授予 `AliyunBailianDataFullAccess` 或更细粒度的策略（如仅 `sfm:ListCategory`），并将该用户加入目标业务空间。
2. **接入点选择**：根据部署地域选择公网或 VPC 接入地址，例如华北2（北京）为 `bailian.cn-beijing.aliyuncs.com`，详情见 [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)。
3. **SDK 集成（推荐）**：下载并初始化对应语言的 [阿里云百炼 SDK](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29)，传入 `AccessKeyId`、`AccessKeySecret` 和 `RegionId`（如 `cn-beijing`），SDK 将自动处理签名与请求。
4. **自签名对接（备选）**：若需自定义签名，务必参考 ROA 机制文档，并强烈建议先加入钉钉群（147535001692）获取专家指导，因自签名细节复杂且易出错。
5. **典型流程示例（知识库）**：
   - 调用 `CreateIndex` 初始化知识库。
   - 调用 `ApplyFileUploadLease` 获取上传租约。
   - 调用 `AddFile` 上传文件至应用数据。
   - 调用 `SubmitIndexJob` 启动知识库构建任务。
   - 调用 `GetIndexJobStatus` 轮询任务状态直至完成。
   - 调用 `Retrieve` 进行语义检索。

## 限制和注意事项

- **限流策略**：各接口有严格 QPS 限制，常见值为 5 次/秒（如 `AddCategory`, `ListCategory`）或 10 次/秒（如 `ApplyFileUploadLease`, `Retrieve`）。超出将返回限流错误，需实现退避重试逻辑。
- **幂等性**：多数 `List*`、`Get*`、`Describe*` 接口具有幂等性；而 `Add*`、`Create*`、`Submit*` 等写操作通常不具备幂等性（如重复 `CreateIndex` 会创建多个同名知识库），需自行实现“先查后建”逻辑。
- **文件与知识库分离**：`DeleteFile` 仅删除应用数据中的文件，不影响已构建的知识库；反之，`DeleteIndexDocument` 仅删除知识库中的索引，不影响源文件。二者需按需分别调用。
- **安全最佳实践**：严禁使用主账号 AccessKey；务必遵循最小权限原则（PoLP）配置 RAM 策略；敏感操作（如 `DeleteIndex`, `DeleteChunk`）均为硬删除且不可逆，调用前须二次确认。
- **地域与版本一致性**：确保 SDK 的 `RegionId` 与所选 [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md) 地域一致，且 SDK 版本与 API 版本（`2023-12-29`）匹配。

## 来源文档

- [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)
- [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)
- [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)
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
- [BatchUpdateFileTag](../../raw/_short/api-bailian-2023-12-29-batchupdatefiletag-34a8f009de66cb8b.md)
- [UpdateFileTag](../../raw/_short/api-bailian-2023-12-29-updatefiletag-f84d2af6a45d6553.md)
- [DeleteFile](../../raw/_short/api-bailian-2023-12-29-deletefile-7e0409a458195fe2.md)
- [DeleteFiles](../../raw/_short/api-bailian-2023-12-29-deletefiles-96ef0815114e4e37.md)
- [GetParseSettings - 获取类目解析设置](../../raw/_short/api-bailian-2023-12-29-getparsesettings-522514560c54f49f.md)
- [GetAvailableParserTypes - 获取文件支持的解析器类型](../../raw/_short/api-bailian-2023-12-29-getavailableparsertypes-09561c4e0fb505d5.md)
- [ChangeParseSetting](../../raw/_short/api-bailian-2023-12-29-changeparsesetting-59a7c69675f499ad.md)
- [AddTable](../../raw/_short/api-bailian-2023-12-29-addtable-6726351659db288d.md)
- [UpdateTableFromAuthorizedOss](../../raw/_short/api-bailian-2023-12-29-updatetablefromauthorized-d7436828bcf51602.md)
- [AddConnector](../../raw/_short/api-bailian-2023-12-29-addconnector-7a3c9650409710fe.md)
- [GetConnector](../../raw/_short/api-bailian-2023-12-29-getconnector-cb2e485a0efd52f7.md)
- [知识库](../../raw/_short/api-bailian-2023-12-29-dir-knowledge-base-f6f202ad9694348f.md)
- [UpdateConnector](../../raw/_short/api-bailian-2023-12-29-updateconnector-6a24905a7d201597.md)
- [CreateIndex - 创建知识库](../../raw/_short/api-bailian-2023-12-29-createindex-8bc613c75f8af371.md)
- [GetIndexJobStatus - 查询知识库创建或追加任务状态](../../raw/_short/api-bailian-2023-12-29-getindexjobstatus-1e88b6ccfffe0fe4.md)
- [SubmitIndexJob - 提交知识库创建任务](../../raw/_short/api-bailian-2023-12-29-submitindexjob-63b38294171880d4.md)
- [SubmitIndexAddDocumentsJob - 提交知识库文件追加任务](../../raw/_short/api-bailian-2023-12-29-submitindexadddocumentsjo-ec4f5cf285e2c447.md)
- [ListIndexFileDetails - 查询知识库文件详情](../../raw/_short/api-bailian-2023-12-29-listindexfiledetails-0e2036d0ef0d8fe8.md)
- [Retrieve - 检索知识库](../../raw/_short/api-bailian-2023-12-29-retrieve-c8e6b8d718a30a84.md)
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
- [GetPromptTemplate - 获取Prompt模板](../../raw/_short/api-bailian-2023-12-29-getprompttemplate-584c357dd7cb48d6.md)
- [ListIndexDocuments - 查询知识库文件列表](../../raw/_short/api-bailian-2023-12-29-listindexdocuments-9f0db0388c421903.md)
- [UpdatePromptTemplate - 更新Prompt模板](../../raw/_short/api-bailian-2023-12-29-updateprompttemplate-519fb4af5ea50522.md)
- [DeletePromptTemplate - 删除Prompt模板](../../raw/_short/api-bailian-2023-12-29-deleteprompttemplate-b441fa1b9c777b81.md)
- [ListPromptTemplates - 获取Prompt模板列表](../../raw/_short/api-bailian-2023-12-29-listprompttemplates-ab5ba5362e93cfcd.md)
- [其他](../../raw/_short/api-bailian-2023-12-29-dir-others-b9c3a16db11771f5.md)
- [UpdateIndex - 更新知识库](../../raw/_short/api-bailian-2023-12-29-updateindex-551997e1d335e340.md)
- [GetAlipayUrl - 获取支付宝打赏URL](../../raw/_short/api-bailian-2023-12-29-getalipayurl-e6e9715d5164f74a.md)
- [ApplyTempStorageLease - 申请临时文件上传许可](../../raw/_short/api-bailian-2023-12-29-applytempstoragelease-5a38ce0eefc66408.md)
- [GetAlipayTransferStatus - 查询支付宝打赏状态](../../raw/_short/api-bailian-2023-12-29-getalipaytransferstatus-04aa88852762fd85.md)
- [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md)


