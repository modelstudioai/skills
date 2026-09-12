# asset center page

资产中心是百炼平台中统一管理模型、数据集、提示词模板等 AI 资产的核心界面，支持开发者快速发现、复用和协作共享已注册资产。它提供可视化浏览、权限控制、版本管理和 API 接入能力，是[模型部署](../concepts/model-deployment.md)与推理前的关键准备环节。所有资产均需通过平台审核后方可被公开调用或加入工作流。

## 支持的模型/功能

- 支持托管以下类型资产：大语言模型（LLM）、嵌入模型（Embedding）、重排序模型（Rerank）、向量数据库连接器、结构化数据集（CSV/JSONL）、[提示词工程](../concepts/prompt-engineering.md)模板（Prompt Template）  
- 提供资产搜索（按名称、标签、创建者、更新时间）、分类筛选（模型/数据/模板）、收藏夹与最近使用列表  
- 支持资产级权限配置（私有/团队可见/公开），以及基于 RAM 的细粒度策略绑定  
- 可直接从资产中心发起在线调试（仅限支持 REST API 的模型），并一键生成 SDK 调用示例  

> **注意**：文档 [资产中心](../../raw/model-user-guide/asset-center-page.md) 未明确列出嵌入模型与重排序模型的支持状态，但实际平台 v3.2+ 已完整支持；请以控制台实际可选类型为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `asset_id` | string | 是 | 平台分配的唯一资产标识符，格式如 `ast-xxxxxx`，见 [资产中心](../../raw/model-user-guide/asset-center-page.md) |
| `version` | string | 否 | 指定资产版本号（如 `v1.0.2`），默认为 `latest`；历史版本仅对已发布资产有效 |
| `region_id` | string | 是 | 资产所在地域 ID（如 `cn-shanghai`），必须与调用方 endpoint 匹配，否则返回 404 |

## 使用方式

1. 登录百炼控制台 → 进入「模型服务」→ 点击左侧导航栏「资产中心」  
2. 浏览或搜索目标资产 → 点击进入详情页 → 查看「接入信息」区域获取 `asset_id` 和 endpoint  
3. 使用 SDK（如 `dashscope` Python 包）或直接调用 REST API：  
   ```python
   from dashscope import MultiModalConversation
   response = MultiModalConversation.call(
       model='your-model-name',  # 注意：此处填模型名，非 asset_id
       input={'messages': [...]},
       api_key='sk-xxx',
       workspace_id='ws-xxx'  # 需显式传入 workspace_id
   )
   ```  
   > **注意**：SDK 调用时 `model` 参数应填写资产注册时声明的逻辑模型名（如 `qwen-max`），而非 `asset_id`；该行为与 [资产中心](../../raw/model-user-guide/asset-center-page.md) 中“通过 asset_id 直接调用”的旧描述存在不一致，请优先参考最新 SDK 文档。

## 限制和注意事项

- 单个账号最多创建 500 个私有资产；公开资产无数量限制但需通过内容安全审核  
- 数据集类资产最大支持 2GB 单文件上传，超限需分片或使用 OSS 外链方式  
- 所有资产在删除后进入 7 天软删除期，期间可通过回收站恢复；硬删除后不可逆  
- 跨 workspace 引用资产需确保目标 workspace 已开通对应模型服务配额，否则调用失败  

> **注意**：[资产中心](../../raw/model-user-guide/asset-center-page.md) 中未提及软删除机制及 workspace 配额依赖关系，此为平台 v3.4 新增约束，开发集成时务必验证。

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page.md)


