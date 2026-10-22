# application component api reference

本 API 参考文档面向开发者，提供百炼平台应用组件（Application Component）的核心能力接口规范，涵盖数据连接（原应用数据）、知识库两大核心功能模块。所有接口均基于 ROA 风格设计，支持通过阿里云百炼 SDK 或自签名方式调用，并严格遵循 RAM 权限模型进行访问控制。开发者需先完成业务空间绑定与最小权限策略配置，方可安全、合规地集成相关能力。

## 支持的模型/功能

API 覆盖两类核心应用场景：

- **数据连接（原应用数据）**：提供结构化与非结构化数据的全生命周期管理能力，包括类目（Category）组织、文件（File）上传/查询/标签管理、OSS 批量导入、连接器（Connector）配置及解析器（Parser）策略控制。支持 `UNSTRUCTURED`（文档类）和 `SESSION_FILE`（会话文件）两类类目类型，但明确不支持通过 API 新增或删除数据表（表格），该操作需在控制台完成 [AddCategory](../../raw/_short/api-bailian-2023-12-29-addcategory-e2fe0e0435ed504e.md)。
- **知识库（Knowledge Base）**：支持创建、更新、查询、监控及细粒度内容管理。可构建 `unstructured`（文档/音视频搜索）、`structured`（数据查询/图片问答）两类知识库。除基础 CRUD 外，还提供分片（Chunk）级操作（添加、修改、删除、查询），并支持通过 `Retrieve` 接口进行向量+关键词混合检索。注意 `SubmitIndexAddDocumentsJob` 明确不支持 `structured` 类型知识库的更新 [SubmitIndexAddDocumentsJob](../../raw/_short/api-bailian-2023-12-29-submitindexadddocumentsjo-ec4f5cf285e2c447.md)。

> **注意**：文档 24（知识库目录）中列出的 `ListIndexFileDetails` 接口在文档 32 中其授权信息字段为 `sfm:ListIndexFileDetails`，但文档 31（`ListIndexDocuments`）的授权信息却错误地指向了 `sfm:ListIndexFiles`。经交叉核对，`ListIndexDocuments` 的正确权限点应为 `sfm:ListIndexDocuments`，而 `sfm:ListIndexFiles` 是一个过时或错误的引用，实际未在任何权威权限策略定义中出现。请以各接口自身文档中明确声明的 `Action` 字段为准。

## 关键参数

- **`WorkspaceId`**：所有接口的必需路径参数，标识业务空间。必须通过控制台或 API 获取有效 ID，不可猜测或复用其他环境 ID。
- **`CategoryId` / `FileId` / `IndexId` / `ConnectorId`**：资源标识符，均为字符串类型，由上游接口（如 `AddCategory`, `AddFile`, `CreateIndex`, `AddConnector`）返回，不可自行构造。
- **`Parser`**：文件解析器类型，关键于 `AddFile` 和 `ChangeParseSetting` 接口。取值包括 `DOCMIND`, `DOCMIND_DIGITAL`, `DOCMIND_LLM_VERSION`, `DASH_QWEN_VL_PARSER`, `AUTO_SELECT` 等。可通过 `GetAvailableParserTypes` 接口动态查询特定文件扩展名（如 `pdf`）所支持的解析器列表 [GetAvailableParserTypes](../../raw/_short/api-bailian-2023-12-29-getavailableparsertypes-09561c4e0fb505d5.md)。
- **`StructureType`**：知识库创建时的关键参数，决定知识库形态。`unstructured` 支持文档/音视频问答；`structured` 支持数据查询/图片问答，二者能力边界严格分离。
- **分页与过滤**：`List*` 类接口普遍支持 `MaxResults`/`PageSize`、`NextToken`/`PageNumber` 及 `DocumentName`/`IndexName` 等过滤参数，用于高效遍历海量资源。

## 使用方式

1. **环境准备**：
   - 获取阿里云 AccessKey（推荐使用 RAM 子账号，遵循最小权限原则）。
   - 在 RAM 控制台为子账号附加 `AliyunBailianDataFullAccess`（读写）或 `AliyunBailianDataReadOnlyAccess`（只读）策略。
   - 确保子账号已加入目标业务空间。
2. **接入点选择**：根据部署地域选择对应公网或 VPC 接入地址，例如华北2（北京）地域的公网地址为 `bailian.cn-beijing.aliyuncs.com` [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)。
3. **SDK 调用（推荐）**：直接使用官方维护的 [阿里云百炼 SDK](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29)，自动处理签名、重试、限流等细节。
4. **自签名对接（谨慎）**：若必须自实现，需严格遵循 ROA 签名机制，复杂度高且易出错，强烈建议加入钉钉群（147535001692）获取技术支持。
5. **典型流程示例（知识库）**：
   - `CreateIndex` → `SubmitIndexJob`（创建空知识库）
   - `ApplyFileUploadLease` → `AddFile`（上传并解析文件到应用数据）
   - `SubmitIndexAddDocumentsJob`（将已解析文件导入知识库索引）
   - `Retrieve`（执行检索）

## 限制和注意事项

- **限流策略**：各接口有独立 QPS 限制，常见值为 5 次/秒（如 `AddCategory`, `DeleteCategory`）或 10 次/秒（如 `AddFile`, `Retrieve`）。超出后将返回 `429` 错误，需实现指数退避重试。
- **幂等性**：`List*`, `Describe*`, `Get*`, `Delete*`（部分）等查询与删除类接口通常具备幂等性；`Add*`, `Create*`, `Submit*` 等创建类接口大多不具备幂等性，重复调用可能导致资源冗余，需自行实现“先查后建”逻辑。
- **数据一致性**：`DeleteFile` 仅删除应用数据中的文件，不影响已构建的知识库索引；反之，`DeleteIndexDocument` 仅删除知识库索引中的文件，不影响应用数据源。两者需按需组合使用。
- **文件状态约束**：`DeleteFile` 仅允许删除 `PARSE_FAILED` 或 `PARSE_SUCCESS` 状态的文件；`DeleteIndexDocument` 仅允许删除 `INSERT_ERROR` 或 `FINISH` 状态的文件。调用前务必通过 `DescribeFile` 或 `ListIndexDocuments` 查询状态。
- **国际站限制**：`UpdateIndex` 和 `GetIndexMonitor` 接口明确不支持国际站，国内站用户需确保地域配置正确。

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
- [AddFilesFromAuthorizedOss](../../raw/_short/api-bailian-2023-12-29-addfilesfromauthorizedoss-879556d685a301b3.md)
- [ListFile](../../raw/_short/api-bailian-2023-12-29-listfile-360209e3a2479f14.md)
- [DescribeFile](../../raw/_short/api-bailian-2023-12-29-describefile-020886c28a208bf2.md)
- [UpdateFileTag](../../raw/_short/api-bailian-2023-12-29-updatefiletag-f84d2af6a45d6553.md)
- [BatchUpdateFileTag](../../raw/_short/api-bailian-2023-12-29-batchupdatefiletag-34a8f009de66cb8b.md)
- [DeleteFile](../../raw/_short/api-bailian-2023-12-29-deletefile-7e0409a458195fe2.md)
- [DeleteFiles](../../raw/_short/api-bailian-2023-12-29-deletefiles-96ef0815114e4e37.md)
- [GetParseSettings - 获取类目解析设置](../../raw/_short/api-bailian-2023-12-29-getparsesettings-522514560c54f49f.md)
- [GetAvailableParserTypes - 获取文件支持的解析器类型](../../raw/_short/api-bailian-2023-12-29-getavailableparsertypes-09561c4e0fb505d5.md)
- [AddTable](../../raw/_short/api-bailian-2023-12-29-addtable-6726351659db288d.md)
- [UpdateTableFromAuthorizedOss](../../raw/_short/api-bailian-2023-12-29-updatetablefromauthorized-d7436828bcf51602.md)
- [AddConnector](../../raw/_short/api-bailian-2023-12-29-addconnector-7a3c9650409710fe.md)
- [GetConnector](../../raw/_short/api-bailian-2023-12-29-getconnector-cb2e485a0efd52f7.md)
- [UpdateConnector](../../raw/_short/api-bailian-2023-12-29-updateconnector-6a24905a7d201597.md)
- [知识库](../../raw/_short/api-bailian-2023-12-29-dir-knowledge-base-f6f202ad9694348f.md)
- [CreateIndex](../../raw/_short/api-bailian-2023-12-29-createindex-8bc613c75f8af371.md)
- [GetIndexJobStatus](../../raw/_short/api-bailian-2023-12-29-getindexjobstatus-1e88b6ccfffe0fe4.md)
- [DeleteCategory - 删除类目](../../raw/_short/api-bailian-2023-12-29-deletecategory-9838436bd2db3113.md)
- [SubmitIndexJob - 提交知识库创建任务](../../raw/_short/api-bailian-2023-12-29-submitindexjob-63b38294171880d4.md)
- [SubmitIndexAddDocumentsJob](../../raw/_short/api-bailian-2023-12-29-submitindexadddocumentsjo-ec4f5cf285e2c447.md)
- [Retrieve](../../raw/_short/api-bailian-2023-12-29-retrieve-c8e6b8d718a30a84.md)
- [ListIndexDocuments](../../raw/_short/api-bailian-2023-12-29-listindexdocuments-9f0db0388c421903.md)
- [ListIndexFileDetails](../../raw/_short/api-bailian-2023-12-29-listindexfiledetails-0e2036d0ef0d8fe8.md)
- [UpdateIndex - 更新知识库](../../raw/_short/api-bailian-2023-12-29-updateindex-551997e1d335e340.md)
- [DeleteIndexDocument - 删除知识库下的文件](../../raw/_short/api-bailian-2023-12-29-deleteindexdocument-0792a83f5a741348.md)
- [ListIndices](../../raw/_short/api-bailian-2023-12-29-listindices-c555173be752eaaf.md)
- [DeleteIndex - 删除知识库](../../raw/_short/api-bailian-2023-12-29-deleteindex-500502bd6df1c49c.md)
- [ChangeParseSetting](../../raw/_short/api-bailian-2023-12-29-changeparsesetting-59a7c69675f499ad.md)
- [ListChunks - 查询索引下的分片列表](../../raw/_short/api-bailian-2023-12-29-listchunks-30a6c87b93a583c6.md)
- [AddChunk](../../raw/_short/api-bailian-2023-12-29-addchunk-1607bcddf6713fd9.md)
- [DeleteChunk - 删除切片](../../raw/_short/api-bailian-2023-12-29-deletechunk-d249422088735d90.md)
- [UpdateChunk - 修改切片](../../raw/_short/api-bailian-2023-12-29-updatechunk-589b46fcc24261f8.md)
- [GetIndexMonitor - 获取知识库监控数据](../../raw/_short/api-bailian-2023-12-29-getindexmonitor-3a609181d5c9c034.md)
- [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md)


