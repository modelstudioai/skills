# application component api reference

本 API 参考文档面向开发者，提供百炼平台应用组件（Application Component）的核心 OpenAPI 接口规范，涵盖数据连接（原应用数据）、知识库两大核心能力模块。所有接口均基于 `bailian/2023-12-29` 版本，采用标准 ROA 签名机制，支持通过官方 SDK 或自签名方式调用。开发者需预先配置 RAM 权限与业务空间成员身份方可使用。

## 支持的模型/功能

API 当前支持两类核心应用组件能力：

- **数据连接（原应用数据）**：提供非结构化文件与结构化表格的全生命周期管理，包括类目（Category）组织、文件（File）上传/查询/标签管理、OSS 批量导入、解析器配置等。该模块不支持通过 API 新增或删除数据表（即结构化数据表），相关操作必须通过控制台完成 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)。
- **知识库（Knowledge Base）**：支持创建、更新、检索、监控及维护两类知识库：
  - *非结构化知识库*（`unstructured`）：适用于文档搜索、音视频问答场景；
  - *结构化知识库*（`structured`）：适用于数据查询、图片问答场景。
  > **注意**：`ListIndexDocuments` 接口在文档 32 中声明其权限点为 `sfm:ListIndexFiles`，而文档 33 的 `ListIndexFileDetails` 同样声明为 `sfm:ListIndexFiles`，但文档 36 的 `ListIndices` 明确使用 `sfm:ListIndex`。这表明 `sfm:ListIndexFiles` 是文件级列表操作的通用权限点，而非知识库列表权限，实际使用时应严格按接口文档匹配权限点，避免混淆。

## 关键参数

所有接口均以 `WorkspaceId`（业务空间 ID）为必需路径参数，用于隔离资源作用域。关键请求参数按功能模块归纳如下：

- **数据连接通用参数**：
  - `CategoryId`：类目 ID，由 `AddCategory` 返回，用于文件归属、解析设置等上下文。
  - `FileId`：文件 ID，由 `AddFile` 返回，用于文件详情、标签更新、删除等操作。
  - `ConnectorId`：连接器 ID，用于关联 OSS 存储或自定义数据源。
- **知识库通用参数**：
  - `IndexId`：知识库 ID，由 `CreateIndex` 返回，是绝大多数知识库操作（如 `Retrieve`, `UpdateIndex`, `DeleteIndexDocument`）的必需标识。
  - `JobId`：任务 ID，由 `SubmitIndexJob` 或 `SubmitIndexAddDocumentsJob` 返回，用于异步任务状态轮询（`GetIndexJobStatus`）。
- **分页与过滤**：
  - `MaxResults` / `PageSize`：控制单页返回条目数，最大值通常为 200（文件列表）或无硬限制（知识库列表）。
  - `NextToken`：用于分页游标，首次调用不传，后续调用需填入上一次响应中的 `NextToken` 值。
  - `DocumentStatus`：用于过滤知识库文件状态（如 `FINISH`, `PARSE_FAILED`）。

## 使用方式

1. **环境准备**：
   - 获取访问凭证：使用 RAM 用户 AccessKey（推荐最小权限原则），而非主账号密钥 [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)。
   - 配置网络接入点：根据地域选择公网或 VPC 地址，例如北京地域为 `bailian.cn-beijing.aliyuncs.com` [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)。
2. **典型工作流（以知识库为例）**：
   - 创建知识库：调用 `CreateIndex` 初始化，再立即调用 `SubmitIndexJob` 提交构建任务。
   - 追加文件：先通过 `ApplyFileUploadLease` 和 `AddFile` 将文件导入应用数据，再调用 `SubmitIndexAddDocumentsJob` 将其加入知识库索引。
   - 检索内容：调用 `Retrieve` 接口，指定 `IndexId` 和 `Query` 即可获取召回结果。
3. **调试与开发**：
   - 推荐使用 [OpenAPI Explorer](https://api.aliyun.com/api-tools/explorer/bailian?version=2023-12-29) 直接调试，无需手动签名。
   - 生产环境强烈建议使用官方 SDK（如 Python、Java 等），其已封装签名、重试、限流处理逻辑。

## 限制和注意事项

- **限流策略**：各接口有独立 QPS 限制，常见阈值为 `5 次/秒`（如 `AddCategory`, `ListCategory`）或 `10 次/秒`（如 `AddFile`, `Retrieve`）。超出将返回 `429 Too Many Requests`，需实现指数退避重试。
- **幂等性**：多数查询类接口（`List*`, `Describe*`, `Get*`）具备幂等性；写入类接口（`Add*`, `Submit*`）多数不具备，需自行实现“先查后建”逻辑确保幂等。
- **数据一致性**：
  - 应用数据（`datacenter`）与知识库（`index`）是分离的存储层。删除 `datacenter` 中的文件（`DeleteFile`）不影响已构建的知识库索引；反之，删除知识库中的文件（`DeleteIndexDocument`）也不影响原始应用数据。
  - `DeleteIndex` 删除知识库后，其关联的 `datacenter` 文件仍保留。
- **功能边界**：
  - 不支持通过 API 管理数据表（`AddTable`, `UpdateTableFromAuthorizedOss` 仅用于已有连接器的表格更新，且 `AddTable` 文档未说明其是否支持新建表，存在歧义）。
  - `ApplyFileUploadLease` 接口路径中 `/{CategoryId}` 参数允许传入 `default`，但文档 10 明确指出“用于智能体应用会话交互的文件时，此处传入 `default` 即可”，而文档 6 的 `AddCategory` 示例中 `CategoryType` 仅列出 `UNSTRUCTURED`，未提及 `SESSION_FILE` 类型，表明 `SESSION_FILE` 是内部专用类型，开发者不应在 `AddCategory` 中显式指定。

## 来源文档

- [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)
- [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)
- [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)
- [API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md)
- [数据连接（原应用数据）](../../raw/_short/api-bailian-2023-12-29-dir-data-connection-origi-a1f7f2601bd6f7cf.md)
- [AddCategory](../../raw/_short/api-bailian-2023-12-29-addcategory-e2fe0e0435ed504e.md)
- [ListCategory](../../raw/_short/api-bailian-2023-12-29-listcategory-2521532ef3e828b3.md)
- [DeleteCategory - 删除类目](../../raw/_short/api-bailian-2023-12-29-deletecategory-9838436bd2db3113.md)
- [AddFile](../../raw/_short/api-bailian-2023-12-29-addfile-8c254b3500bc50bc.md)
- [ApplyFileUploadLease](../../raw/_short/api-bailian-2023-12-29-applyfileuploadlease-39e8ca15e0e9561a.md)
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
- [AddConnector](../../raw/_short/api-bailian-2023-12-29-addconnector-7a3c9650409710fe.md)
- [UpdateTableFromAuthorizedOss](../../raw/_short/api-bailian-2023-12-29-updatetablefromauthorized-d7436828bcf51602.md)
- [GetConnector](../../raw/_short/api-bailian-2023-12-29-getconnector-cb2e485a0efd52f7.md)
- [知识库](../../raw/_short/api-bailian-2023-12-29-dir-knowledge-base-f6f202ad9694348f.md)
- [UpdateConnector](../../raw/_short/api-bailian-2023-12-29-updateconnector-6a24905a7d201597.md)
- [CreateIndex - 创建知识库](../../raw/_short/api-bailian-2023-12-29-createindex-8bc613c75f8af371.md)
- [GetIndexJobStatus - 查询知识库创建或追加任务状态](../../raw/_short/api-bailian-2023-12-29-getindexjobstatus-1e88b6ccfffe0fe4.md)
- [SubmitIndexAddDocumentsJob - 提交知识库文件追加任务](../../raw/_short/api-bailian-2023-12-29-submitindexadddocumentsjo-ec4f5cf285e2c447.md)
- [SubmitIndexJob - 提交知识库创建任务](../../raw/_short/api-bailian-2023-12-29-submitindexjob-63b38294171880d4.md)
- [Retrieve - 检索知识库](../../raw/_short/api-bailian-2023-12-29-retrieve-c8e6b8d718a30a84.md)
- [ListIndexDocuments - 查询知识库文件列表](../../raw/_short/api-bailian-2023-12-29-listindexdocuments-9f0db0388c421903.md)
- [ListIndexFileDetails - 查询知识库文件详情](../../raw/_short/api-bailian-2023-12-29-listindexfiledetails-0e2036d0ef0d8fe8.md)
- [UpdateIndex - 更新知识库](../../raw/_short/api-bailian-2023-12-29-updateindex-551997e1d335e340.md)
- [DeleteIndexDocument - 删除知识库下的文件](../../raw/_short/api-bailian-2023-12-29-deleteindexdocument-0792a83f5a741348.md)
- [ListIndices - 查询知识库列表](../../raw/_short/api-bailian-2023-12-29-listindices-c555173be752eaaf.md)
- [ListChunks - 查询索引下的分片列表](../../raw/_short/api-bailian-2023-12-29-listchunks-30a6c87b93a583c6.md)
- [DeleteIndex - 删除知识库](../../raw/_short/api-bailian-2023-12-29-deleteindex-500502bd6df1c49c.md)
- [AddChunk - 新增切片](../../raw/_short/api-bailian-2023-12-29-addchunk-1607bcddf6713fd9.md)
- [UpdateChunk - 修改切片](../../raw/_short/api-bailian-2023-12-29-updatechunk-589b46fcc24261f8.md)
- [GetIndexMonitor - 获取知识库监控数据](../../raw/_short/api-bailian-2023-12-29-getindexmonitor-3a609181d5c9c034.md)
- [DeleteChunk - 删除切片](../../raw/_short/api-bailian-2023-12-29-deletechunk-d249422088735d90.md)
- [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md)


