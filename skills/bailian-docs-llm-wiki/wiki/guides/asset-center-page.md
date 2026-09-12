# asset center page

资产中心是百炼平台中统一管理模型、数据集、Prompt 模板等 AI 资产的核心界面，支持开发者快速发现、复用和共享已验证的资产。它为模型调用、微调准备、评估实验提供标准化入口，所有资产均按权限隔离并支持版本化管理。该页面不直接执行推理，而是作为资产生命周期的管控枢纽。

## 支持的模型/功能

- 支持托管模型（如 Qwen 系列、Qwen-VL、Qwen2-Audio）、自定义微调模型（Fine-tuned Model）及第三方模型接入（需通过 Model Gateway 注册）  
- 提供资产类型过滤：模型（Model）、数据集（Dataset）、Prompt 模板（Prompt Template）、评估任务（Evaluation Task）  
- 支持一键部署至 API 服务、导入 Notebook 环境、下载配置文件（如 `model_config.json`）  
- 可查看资产元信息：创建者、更新时间、引用次数、兼容 SDK 版本（见 [资产中心](../../raw/model-user-guide/asset-center-page.md)）

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `asset_id` | string | 是 | 资产唯一标识，格式为 `m-xxx`（模型）、`d-xxx`（数据集）等，可在 URL 或详情页获取 |
| `version` | string | 否 | 指定资产版本号（如 `v1.2.0`），默认使用 `latest`；历史版本仅对拥有 `read:version` 权限的用户可见 |
| `visibility` | enum | 否 | 取值 `public` / `org` / `private`，控制资产可见范围；`public` 仅限平台官方认证资产（参见 [资产中心](../../raw/model-user-guide/asset-center-page.md)） |

> **注意**：文档中提及的 `visibility=shared` 已废弃，当前仅支持 `public`/`org`/`private` 三档；旧版 SDK（< v3.8.0）可能仍解析 `shared`，建议升级至最新版（见 [资产中心](../../raw/model-user-guide/asset-center-page.md)）

## 使用方式

1. **访问路径**：登录百炼控制台 → 左侧导航栏点击「资产中心」→ 选择资产类型标签页  
2. **搜索与筛选**：支持按名称、ID、标签（tag）、创建者、SDK 兼容性（如 `sdk>=3.7.0`）组合过滤  
3. **API 集成**：通过 `GET /v1/assets` 接口拉取列表，传入 `type=model&version=latest` 等 query 参数（详见 OpenAPI 文档）  
4. **代码引用示例（Python SDK）**：
   ```python
   from alibabacloud_bailian20231219 import models
   client.get_asset(asset_id="m-qwen2-7b", version="v1.0.0")
   ```

## 限制和注意事项

- 单个组织下最多创建 500 个私有资产（含模型、数据集等），超出后需删除或归档旧资产  
- 数据集资产不支持跨地域复制；模型资产跨地域部署需重新注册（因底层镜像存储隔离）  
- `asset_id` 在组织内全局唯一，但不同组织可重名；调用时务必确认 `organization_id` 上下文  
- 所有资产操作受 RAM 权限策略约束，例如 `bailian:ListAssets`、`bailian:GetAsset`（权限配置参考 [资产中心](../../raw/model-user-guide/asset-center-page.md)）

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page.md)


