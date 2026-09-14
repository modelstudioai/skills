# asset center page

资产中心是百炼平台中统一管理模型、数据集、提示词、工作流等 AI 资产的核心界面，支持开发者快速发现、复用和协作共享已注册资产。所有资产均按类型分类展示，并提供元信息查看、权限配置与版本管理能力。该页面为模型调用、RAG 构建及低代码编排提供基础资产支撑。

## 支持的模型/功能

- 支持托管和引用以下资产类型：大语言模型（LLM）、嵌入模型（Embedding）、重排序模型（Reranker）、向量数据库索引、结构化数据集、Prompt 模板、Workflow 实例  
- 提供资产搜索（按名称、标签、创建者、更新时间）、批量导入导出（JSON/YAML 格式）、跨项目共享（基于 RAM 角色策略）  
- 支持模型资产的在线调试（`Try it` 功能），可直接输入文本并查看响应与 token 统计  
- 详细能力说明见 [资产中心](../../raw/model-user-guide/asset-center-page.md)

## 关键参数

- `asset_type`: 必填，取值为 `model` / `dataset` / `prompt` / `workflow` / `index`  
- `visibility`: 可选，`private`（仅本人）、`project`（本项目成员）、`public`（组织内可见）  
- `tags`: 字符串数组，用于多维检索，单个 tag 长度 ≤ 32 字符，总数 ≤ 10  
- `version`: 创建时自动生成语义版本（如 `v1.2.0`），历史版本保留且不可删除；回滚需显式调用 `/versions/{id}/rollback` 接口  
- 参数约束详见 [资产中心](../../raw/model-user-guide/asset-center-page.md)

## 使用方式

1. **Web 界面操作**：进入控制台 → 左侧导航栏点击「资产中心」→ 选择资产类型标签页 → 点击「新建」或上传文件  
2. **API 集成**：调用 `POST /api/v1/assets` 创建资产，请求体需包含 `asset_type`、`name`、`content`（Base64 或 URL 引用）及 `metadata` 字段  
3. **SDK 调用（Python）**：
   ```python
   from alibabacloud_bailian20231219 import models as bailian_models
   client = BailianClient(...)
   req = bailian_models.CreateAssetRequest(
       asset_type="model",
       name="qwen2-7b-chat",
       visibility="project",
       tags=["chat", "cn"]
   )
   resp = client.create_asset(req)
   ```
   完整 SDK 示例参见 [资产中心](../../raw/model-user-guide/asset-center-page.md)

## 限制和注意事项

- 单个资产文件大小上限为 512 MB（数据集类资产）或 10 MB（模型配置类）；超限需使用 OSS 外链方式上传  
- `prompt` 类型资产不支持嵌套引用其他 [prompt](prompt.md)；若需组合逻辑，应使用 `workflow` 类型封装  
- > **注意**：文档中提及“支持实时预览 PDF 数据集内容”，但当前 v2.4.1 版本尚未实现该功能，实际仅支持 CSV/JSONL/TSV 的表格化预览 —— 此处与 [资产中心](../../raw/model-user-guide/asset-center-page.md) 中描述存在不一致，请以控制台实际行为为准  
- 所有资产在删除后进入 7 天软删除期，期间可通过回收站恢复；硬删除后不可逆  
- 公共资产（`visibility=public`）默认禁止修改，如需编辑，须先切换为 `project` 或 `private`

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page.md)


