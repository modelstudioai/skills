# asset center page

资产中心是百炼平台中统一管理模型、提示词、知识库等 AI 资源的核心界面，支持开发者快速查看、筛选、复用和调试已注册的资产。所有资产均按类型隔离展示，并提供版本控制、权限配置与调用统计能力。该页面为模型集成与工作流编排提供基础资源支撑。

## 支持的模型/功能

资产中心当前支持以下四类资产：
- **大模型（LLM）**：包括通义千问系列（qwen-max、qwen-plus、qwen-turbo）、第三方模型（如 claude-3-haiku）及自定义部署模型；
- **[提示词工程](../concepts/prompt-engineering.md)资产（Prompt Template）**：支持结构化 Prompt 编辑、变量注入与多环境测试；
- **知识库（Knowledge Base）**：对接向量库与文档解析服务，支持增量更新与 chunk 策略配置；
- **工具函数（Tool Function）**：以 OpenAPI Schema 描述的可调用函数，用于 Agent 工作流编排。

> **注意**：部分旧版文档仍将“插件（Plugin）”列为独立资产类型，但根据 [资产中心](../../raw/model-user-guide/asset-center-page.md) 的最新定义，插件能力已整合进 Tool Function 类型，不再单独展示。

## 关键参数

在资产详情页或 API 调用中，以下参数具有全局意义：
- `asset_id`：平台内唯一标识符，格式为 `ac-<8位小写十六进制>`；
- `version`：语义化版本号（如 `v1.2.0`），默认为 `latest`，历史版本可通过下拉菜单切换；
- `visibility`：取值为 `private`（仅创建者可见）、`workspace`（同工作空间成员可见）或 `public`（需管理员审批）；
- `invoke_count_7d`：近 7 天调用次数，仅对已启用监控的资产实时更新。

上述字段定义与行为逻辑详见 [资产中心](../../raw/model-user-guide/asset-center-page.md) 中的“资产元数据规范”章节。

## 使用方式

1. **Web 界面操作**：登录后进入「资产中心」→ 选择左侧资产类型标签 → 点击「+ 新建」或已有资产卡片进入编辑页；
2. **API 集成**：通过 `POST /v1/assets/{type}/create` 创建，使用 `GET /v1/assets/{asset_id}/invoke` 直接调用（需携带 `Authorization: Bearer <token>`）；
3. **SDK 调用（Python）**：
   ```python
   from alibabacloud_bailian20231219 import models as bailian_models
   client = bailian_models.Client(...)
   resp = client.invoke_asset(asset_id="ac-1a2b3c4d", input={"query": "你好"})
   ```

完整请求体结构与错误码说明请参考 [资产中心](../../raw/model-user-guide/asset-center-page.md) 的“API 接口参考”小节。

## 限制和注意事项

- 单个工作空间最多创建 500 个资产（含所有类型），超出后需归档或删除旧资产；
- 知识库类资产单次上传文档总大小上限为 200 MB，且不支持 `.exe`、`.bin` 等可执行文件；
- 所有资产的 `version` 字段一旦发布即不可修改；若需变更逻辑，请新建版本并更新引用；
- 自定义模型资产必须通过 `model_endpoint` 参数显式指定服务地址，且该地址须通过平台白名单校验（参见 [资产中心](../../raw/model-user-guide/asset-center-page.md) “安全策略”章节）。

> **注意**：文档中提及的“资产自动同步至 Flow 编排画布”功能，在 v2.4.0 后已改为按需手动拖入，此变更未在部分旧版示意图中体现，请以实际 UI 为准。

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page.md)


