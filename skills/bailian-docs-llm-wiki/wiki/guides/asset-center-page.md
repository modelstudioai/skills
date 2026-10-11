# asset center page

资产中心是百炼平台中统一管理模型资产（如微调模型、推理服务、Prompt 模板等）的核心页面，提供可视化浏览、版本控制、权限配置与快速部署能力。开发者可通过该页面完成模型生命周期的关键操作，包括上传、发布、下线及关联应用。所有资产均按命名空间隔离，支持团队协作与审计追踪。

## 支持的模型/功能

- 支持托管以下类型资产：微调后的 LLM 模型（Qwen 系列、GLM 系列等）、自定义 Prompt 模板、结构化推理服务（含 API 配置）、向量检索索引（需绑定知识库）  
- 提供资产克隆、版本回滚、灰度发布、访问日志查看等运维功能  
- 支持通过 [资产中心](raw/model-user-guide/asset-center-page/asset-center.md) 页面直接触发模型在线调试（需已部署为服务）  

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `asset_id` | string | 是 | 平台生成的全局唯一资产标识，格式为 `ac-xxxxxx` |
| `namespace` | string | 是 | 命名空间，取值为 `user`（个人）或团队 ID（如 `team-abc123`） |
| `version` | string | 否 | 版本号，默认为 `latest`；支持语义化版本（如 `v1.2.0`）或时间戳（如 `202405201430`） |
| `visibility` | enum | 否 | 取值：`private`（默认）、`internal`（同命名空间可见）、`public`（仅限白名单用户） |

> **注意**：`visibility=public` 在 [资产中心](raw/model-user-guide/asset-center-page/asset-center.md) 中已废弃，实际生效策略以 [原文标题](../../raw/model-user-guide/asset-center-page.md) 的最新权限模型为准，当前仅支持 `private` 和 `internal`。

## 使用方式

1. **访问入口**：登录百炼控制台 → 左侧导航栏点击「资产中心」→ 选择目标命名空间  
2. **创建资产**：点击「+ 新建资产」→ 选择类型（如「微调模型」）→ 上传模型文件或填写服务元数据 → 提交审核（企业版需审批流）  
3. **API 调用**：通过 `POST /v1/assets/{namespace}/{asset_id}/deploy` 部署资产，请求体需包含 `runtime_config`（见 [原文标题](../../raw/model-user-guide/asset-center-page.md)）  
4. **集成开发**：在应用配置中引用资产时，使用 `asset://<namespace>/<asset_id>@<version>` URI 格式（示例：`asset://user/ac-7f9a2b@v2.1.0`）

## 限制和注意事项

- 单个资产最大体积为 100 GB（向量索引类资产上限为 50 GB）  
- `asset_id` 创建后不可修改；重命名需新建资产并迁移引用  
- 所有资产默认保留最近 3 个版本，历史版本超过 90 天自动归档（可手动清理）  
- 删除资产前必须确保无活跃服务实例或应用依赖，否则操作失败 —— 具体校验逻辑详见 [原文标题](../../raw/model-user-guide/asset-center-page.md)  
- 企业版用户启用 SSO 后，资产权限继承自 Identity Provider 的组策略，本地角色配置可能被覆盖

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page.md)


