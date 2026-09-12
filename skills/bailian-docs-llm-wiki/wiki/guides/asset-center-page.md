# asset center page

资产中心是百炼平台中统一管理模型、数据集、Prompt 模板等 AI 资产的核心界面，支持开发者快速发现、复用和共享已注册的资产。它为模型调用、微调任务配置及 RAG 应用构建提供标准化入口。所有资产均需通过平台审核并发布后方可被项目引用。

## 支持的模型/功能

- 支持托管以下类型资产：大语言模型（LLM）、嵌入模型（Embedding）、重排序模型（Rerank）、语音识别（ASR）与合成（TTS）模型、自定义训练完成的微调模型（Fine-tuned Model），以及结构化数据集与 [Prompt 工程](../concepts/prompt-engineering.md)模板  
- 提供资产版本管理、权限控制（组织级/项目级可见性）、标签分类与全文检索能力  
- 可直接从资产中心发起模型在线调试（Inference Playground）、批量测试（Batch Test）及 RAG 知识库绑定操作  
- 详细能力说明见 [资产中心](../../raw/model-user-guide/asset-center-page.md)

## 关键参数

- `asset_id`：全局唯一标识符（UUID 格式），用于 API 调用与 SDK 引用，不可修改  
- `version`：语义化版本号（如 `v1.2.0`），默认为 `latest`；历史版本仅可查看与部署，不可编辑  
- `visibility`：取值为 `public`（全组织可见）、`project`（仅限指定项目）、`private`（仅创建者）  
- `metadata`：JSON 结构，支持自定义字段如 `task_type: "text-generation"`、`input_schema`、`output_schema`，用于自动化工具链解析  
- 参数规范详见 [资产中心](../../raw/model-user-guide/asset-center-page.md) 中的“资产元数据定义”章节

## 使用方式

1. **Web 界面**：登录百炼控制台 → 进入「资产中心」→ 使用顶部搜索栏或左侧筛选器定位资产 → 点击资产卡片进入详情页 → 执行「部署」、「调试」或「复制 ID」等操作  
2. **API 调用**：通过 `GET /api/v1/assets/{asset_id}/versions/{version}` 获取资产描述与 endpoint；使用 `POST /api/v1/invoke` 并在 `body.asset_ref` 中传入 `{"asset_id": "...", "version": "v1.0.0"}`  
3. **SDK 集成（Python）**：  
   ```python
   from alibabacloud_bailian20231219 import models as bailian_models
   client = BailianClient(...)
   invoke_req = bailian_models.InvokeRequest(
       asset_id="as-abc123",
       version="latest",
       input={"prompt": "你好"}
   )
   response = client.invoke(invoke_req)
   ```  
   完整示例参见 [资产中心](../../raw/model-user-guide/asset-center-page.md) 的“SDK 快速开始”部分

## 限制和注意事项

- 单个资产最多保留 10 个历史版本；超过后需手动归档旧版本以释放配额  
- `private` 资产无法被跨项目 API 调用，即使调用方拥有项目管理员权限（此行为与文档 [资产中心](../../raw/model-user-guide/asset-center-page.md) 描述一致）  
- > **注意**：原始文档中提及“支持上传本地 CSV 文件作为数据集资产”，但当前平台仅接受 OSS URI 导入（`oss://bucket-name/path/to/file.csv`），该功能尚未开放本地直传，实际行为以控制台 UI 和 OpenAPI 文档为准  
- 资产删除为软删除（保留 30 天可恢复），但已部署至生产环境的服务实例不受影响；建议先下线服务再执行删除操作

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page.md)



