# application component api reference

阿里云百炼（Model Studio）应用组件 OpenAPI（产品代码 `bailian/2023-12-29`）面向开发者提供数据连接、Prompt 工程与知识库（RAG）三大类能力的编程接口。本文汇总该版本下主要 API 的功能、调用方式、权限模型与关键限制，便于在服务端或自动化流程中快速集成。

## API 基础

### 签名风格与 SDK

- 采用 [ROA 签名风格](https://help.aliyun.com/zh/sdk/product-overview/roa-mechanism)，请求通过 HTTP 方法 + 资源路径表达语义。
- 官方已封装 Java、Python、Go、Node.js、PHP、C# 等多语言 SDK，建议优先通过 [SDK 下载页](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29) 获取最新版本，避免自行实现签名。
- 自签名对接复杂度高（预估约 5 个工作日），如确有需要请联系钉钉服务群（147535001692）获取指导。
- 可在 [OpenAPI Explorer](https://api.aliyun.com/api/bailian/2023-12-29) 在线调试并自动生成 SDK 代码示例。

详细背景见 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)。

### 接入点（Endpoint）

当前提供两个地域的接入点，所有 API 调用均需路由至对应[业务空间](../concepts/workspace.md)的 Endpoint：

| 地域 | 地域 ID | 公网接入点 | VPC 接入点 |
| --- | --- | --- | --- |
| 华北2（北京） | cn-beijing | `bailian.cn-beijing.aliyuncs.com` | `bailian-vpc.cn-beijing.aliyuncs.com` |
| 新加坡 | ap-southeast-1 | `bailian.ap-southeast-1.aliyuncs.com` | `bailian-vpc.ap-southeast-1.aliyuncs.com` |

完整接入点信息见 [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)。

### 身份与认证

- 调用前必须准备阿里云账号或 RAM 用户的 **AccessKey**（[获取方式](https://help.aliyun.com/zh/ram/user-guide/create-an-accesskey-pair)）。
- 阿里云账号拥有全部资源管理权限；生产环境建议创建独立 RAM 用户，并按最小权限原则配置策略。
- 所有 API 请求都携带 `WorkspaceId`（[业务空间](../concepts/workspace.md) ID）作为路径参数，资源隔离以[业务空间](../concepts/workspace.md)为粒度。

## 权限模型（RAM）

百炼 OpenAPI 在 RAM 中的 RamCode 为 `sfm`，授权粒度为**操作级**。权限策略结构遵循标准 RAM JSON 格式：

```json
{
  "Version": "1",
  "Statement": [{
    "Effect": "Allow",
    "Action": "sfm:<ActionName>",
    "Resource": "*"
  }]
}
```

每个 API 对应一个 `sfm:<ActionName>` 权限点，访问级别分为 `create / get / list / update / delete / none`。常用系统策略：

- `AliyunBailianDataFullAccess`：数据类 API 的完整读写权限。
- `AliyunBailianDataReadOnlyAccess`：仅读权限，可用于监控与状态查询场景。

授权矩阵与条件关键字详见 [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)。

> **注意**：RAM 用户调用任何 API 前，除了配置对应 Action 的权限策略外，还必须**先加入目标业务空间**，否则会返回鉴权失败。

## 数据连接（原应用数据）

数据连接负责管理百炼中的非结构化文件、表格与外部连接器，是知识库与智能体应用的"数据底座"。所有接口路径以 `/{WorkspaceId}/datacenter/...` 为前缀。

### 类目管理（Category）

每个业务空间最多创建 **500 个类目**，支持最多一级的层级结构（通过 `ParentCategoryId` 指定父类目）。

| API | 用途 | 备注 |
| --- | --- | --- |
| [AddCategory](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-addcategory.md) | 创建类目 | `CategoryType` 目前仅支持 `UNSTRUCTURED`；非幂等 |
| ListCategory | 分页查询类目 | 通过 `NextToken` 翻页 |
| DeleteCategory | 删除类目 | 不可恢复 |

> **注意**：当前**不支持**通过 API 新增或查询"数据表"（结构化表格容器），数据表只能通过控制台操作。

### 文件管理（File）

文件必须先通过上传租约或 OSS 授权进入百炼临时存储，再通过 AddFile 类接口导入到数据连接。

| API | 用途 |
| --- | --- |
| ApplyFileUploadLease | 申请上传租约（用于知识库文件 / 会话文件） |
| [AddFile](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-addfile.md) | 从临时存储导入文件 |
| AddFilesFromAuthorizedOss | 从已授权 OSS Bucket 批量导入 |
| ListFile | 分页查询类目下的文件 |
| DescribeFile | 查询单个文件的状态（解析中等） |
| UpdateFileTag / BatchUpdateFileTag | 单文件 / 批量更新文件标签 |
| DeleteFile / DeleteFiles | 删除单个 / 批量删除文件 |

文件导入是异步过程，需轮询 `DescribeFile` 确认状态变为成功再用于知识库构建。

### 解析设置（Parse Settings）

控制类目下文档的默认解析行为（chunk 策略、解析器等）：

- `GetAvailableParserTypes`：查询某文件类型支持的解析器。
- `GetParseSettings`：获取类目当前的解析配置。
- `ChangeParseSetting`：修改类目解析设置，仅对**新导入**的文件生效。

### 表格（Table）与连接器（Connector）

- **AddTable / UpdateTableFromAuthorizedOss**：管理结构化表格数据（仅控制台入口可创建表格容器，API 仅支持内容更新）。
- **AddConnector**：创建文件类型的连接器，将自有 OSS 或平台 OSS 作为外部数据源接入。`StorageType` 支持 `OSS_CUSTOM`（自有 OSS）和 `OSS_PLATFORM`（平台 OSS）。
- **GetConnector / UpdateConnector**：查询与更新连接器配置。

## Prompt 工程

Prompt 模板用于在业务空间内统一管理可复用的 Prompt 片段，支持变量占位（例如 `${theme}`）。

| API | 用途 |
| --- | --- |
| [CreatePromptTemplate](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-prompt-engineering/api-bailian-2023-12-29-createprompttemplate.md) | 创建模板（**暂不支持**文生图 Prompt 模板） |
| GetPromptTemplate | 按 ID 查询模板 |
| UpdatePromptTemplate | 更新模板名称或内容 |
| DeletePromptTemplate | 删除模板 |
| ListPromptTemplates | 分页查询模板列表 |

返回字段主要包括 `promptTemplateId` 与 `requestId`。模板 `content` 中可使用 `${var}` 形式声明变量，在调用时动态替换。

## 知识库（RAG Index）

知识库 API 覆盖创建、填充、检索、监控的全生命周期，路径前缀为 `/{WorkspaceId}/index/...`。

### 构建流程

创建知识库是**两步式异步**过程，必须先 `CreateIndex` 再 `SubmitIndexJob`，否则会得到一个空知识库：

1. **CreateIndex**：初始化知识库元数据（名称、类型、Embedding 模型、分片策略等）。支持两类知识库：
   - **非结构化**：基于文档 / 音视频。
   - **结构化**：用于数据查询或图片问答。
2. **SubmitIndexJob**：提交创建任务，触发实际构建（高峰期可能耗时数小时）。
3. **GetIndexJobStatus**：轮询任务状态，建议调用间隔 ≥ 5 秒。
4. **SubmitIndexAddDocumentsJob**：对已存在的知识库追加文档。

任务完成后，可在智能体应用中关联知识库，或在应用调用 API 中通过 `rag_options.IndexId` 指定。

### 文档管理

| API | 用途 |
| --- | --- |
| ListIndexDocuments | 查询知识库下的文件列表及概要 |
| ListIndexFileDetails | 查询文件级详细状态 |
| DeleteIndexDocument | 删除知识库中的指定文件 |
| UpdateIndex | 更新知识库配置（2026-01 新增） |
| ListIndices | 分页查询业务空间下的知识库列表 |
| DeleteIndex | 删除整个知识库 |

### 分片（Chunk）与检索

- **ListChunks**：查询知识库某索引下的分片列表。
- **UpdateChunk / DeleteChunk**：对切片进行微调或清理。
- **[Retrieve](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-retrieve.md)**：在指定知识库中检索信息，`Query` 为原始 [prompt](../guides/prompt.md)，长度无限制；由于包含复杂检索与匹配逻辑，响应时间可能较长，应合理设置超时与重试。

### 监控

- **GetIndexMonitor**：获取知识库在指定时间窗口内的存储与检索 QPS 监控数据（存储限额 / 使用量、QPS 峰值、成功 / 失败 / 限流请求细分）。查询时间范围最大 **30 天**，时间窗粒度会随查询范围动态调整。返回中 `pipelineCommercialType` 字段区分 standard / enterprise 规格。

## 通用限制与注意事项

- **限流**：
  - 数据连接类接口（Category / File / Connector 等）：≤ **5 次/秒**。
  - 知识库创建类接口（CreateIndex / SubmitIndexJob 等）：≤ **10 次/秒**。
  - 触发限流时请退避重试，避免雪崩。
- **幂等性**：
  - 读接口（List / Get / Describe）普遍具有幂等性。
  - 写接口大多**不具备幂等性**（AddCategory、AddFile、CreateIndex、SubmitIndexJob 等），重复调用会产生重复资源；建议在业务层实现"先查询后操作"。
- **WorkspaceId 必带**：所有 API 都将 `WorkspaceId` 作为路径参数，资源隔离完全依赖业务空间。
- **API-Key vs AccessKey**：知识库检索等部分接口同时支持 SDK + AccessKey 与 Spring AI Alibaba + API-Key 两种调用方式，请根据技术栈选择。
- **[异步任务](../concepts/async-task.md)**：知识库构建、文件解析均为异步，需要配合状态查询接口做进度跟踪，不要在任务未完成时重复发起。

## 版本与变更

API 在 2026 年近期有以下关键变更（详见 [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md)）：

| 时间 | 变更 |
| --- | --- |
| 2026-03-30 | `CreateIndex` 入参变更；`Retrieve` 内部配置调整（不影响调用） |
| 2026-03-27 | `CreateIndex` 入参再次调整 |
| 2026-01-19 | 新增 `UpdateIndex` |
| 2026-01-15 | `DescribeFile` 返回结构调整 |
| 2026-01-14 | 新增 `GetIndexMonitor` |

集成时建议锁定 SDK 版本并在发版前核对 changeset，避免因入参/返回结构变化导致线上失败。

## 来源文档

- [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)
- [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)
- [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md)
- [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)
- [AddCategory - 新增类目](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-addcategory.md)
- [ListCategory - 类目列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-listcategory.md)
- [DeleteCategory - 删除类目](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-deletecategory.md)
- [ApplyFileUploadLease - 申请文件上传租约](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-applyfileuploadlease.md)
- [ListFile - 文件列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-listfile.md)
- [AddFilesFromAuthorizedOss - 从已授权OSS Bucket中导入文件](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-addfilesfromauthorizedoss.md)
- [AddFile - 添加文件](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-addfile.md)
- [DescribeFile - 查询文件状态](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-describefile.md)
- [UpdateFileTag - 更新文件标签](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-updatefiletag.md)
- [DeleteFile - 删除文件](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-deletefile.md)
- [BatchUpdateFileTag - 批量更新文档标签](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-batchupdatefiletag.md)
- [GetParseSettings - 获取类目解析设置](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-getparsesettings.md)
- [GetAvailableParserTypes - 获取文件支持的解析器类型](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-getavailableparsertypes.md)
- [ChangeParseSetting - 修改类目解析设置](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-changeparsesetting.md)
- [AddTable - 添加表格](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-addtable.md)
- [UpdateTableFromAuthorizedOss - 从已授权OSS Bucket中选择文件更新表格](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-updatetablefromauthorizedoss.md)
- [AddConnector - 新增连接器](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-addconnector.md)
- [CreatePromptTemplate - 创建Prompt模板](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-prompt-engineering/api-bailian-2023-12-29-createprompttemplate.md)
- [GetConnector - 获取连接器信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-getconnector.md)
- [GetPromptTemplate - 获取Prompt模板](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-prompt-engineering/api-bailian-2023-12-29-getprompttemplate.md)
- [UpdatePromptTemplate - 更新Prompt模板](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-prompt-engineering/api-bailian-2023-12-29-updateprompttemplate.md)
- [DeletePromptTemplate - 删除Prompt模板](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-prompt-engineering/api-bailian-2023-12-29-deleteprompttemplate.md)
- [ListPromptTemplates - 获取Prompt模板列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-prompt-engineering/api-bailian-2023-12-29-listprompttemplates.md)
- [CreateIndex - 创建知识库](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-createindex.md)
- [GetIndexJobStatus - 查询知识库创建任务状态](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-getindexjobstatus.md)
- [SubmitIndexJob - 提交知识库创建任务](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-submitindexjob.md)
- [SubmitIndexAddDocumentsJob - 提交知识库追加任务](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-submitindexadddocumentsjob.md)
- [Retrieve - 检索知识库](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-retrieve.md)
- [ListIndexDocuments - 查询知识库下的文件列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-listindexdocuments.md)
- [ListIndexFileDetails - 查询知识库下的文件详情](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-listindexfiledetails.md)
- [DeleteIndexDocument - 删除知识库下的文件](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-deleteindexdocument.md)
- [UpdateIndex - 更新知识库](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-updateindex.md)
- [ListIndices - 查询知识库列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-listindices.md)
- [DeleteIndex - 删除知识库](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-deleteindex.md)
- [ListChunks - 查询索引下的分片列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-listchunks.md)
- [DeleteChunk - 删除切片](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-deletechunk.md)
- [UpdateChunk - 修改切片](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-updatechunk.md)
- [GetIndexMonitor - 获取知识库监控数据](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-getindexmonitor.md)
- [GetAlipayUrl - 获取支付宝打赏URL](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-getalipayurl.md)
- [GetAlipayTransferStatus - 查询支付宝打赏状态](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-getalipaytransferstatus.md)
- [ApplyTempStorageLease - 申请临时文件上传许可](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-applytempstoragelease.md)
- [GetMemory - 获取长期记忆体](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-getmemory.md)
- [CreateMemory - 创建长期记忆体](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-creatememory.md)
- [UpdateMemory - 更新长期记忆体](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-updatememory.md)
- [DeleteMemory - 删除长期记忆体](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-deletememory.md)
- [ListMemories - 获取长期记忆体列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-listmemories.md)
- [CreateMemoryNode - 创建记忆片段](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-creatememorynode.md)
- [GetMemoryNode - 获取记忆片段](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-getmemorynode.md)
- [UpdateMemoryNode - 更新记忆片段](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-updatememorynode.md)
- [DeleteMemoryNode - 删除记忆片段](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-deletememorynode.md)
- [ListMemoryNodes - 获取记忆片段列表](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-listmemorynodes.md)
- [UpdateConnector - 编辑连接器](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-data-connection-original-application-data/api-bailian-2023-12-29-updateconnector.md)
- [DeleteFiles - 批量删除文件](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-deletefiles.md)


