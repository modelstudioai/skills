# application publishing and sharing

应用发布与分享是百炼平台中将已构建的 Agent 或 Workflow 对外提供服务的关键能力，支持以链接形式共享、嵌入到第三方系统，或作为可复用组件被其他应用调用。该能力覆盖公开/私密分享、跨空间调用、UI 定制化等场景，适用于协作开发与生产集成。所有操作均通过控制台或 OpenAPI 完成，无需代码部署。

## 支持的模型/功能

- **应用分享**：生成带权限控制的访问链接，支持“仅限成员可见”“指定用户可见”“公开链接（需空间管理员授权）”三种模式  
- **发布为组件**：将 Workflow 或 Agent 发布为标准组件（Component），供同一工作空间内其他应用在编排画布中直接拖拽调用  
- **UI 自定义**：通过 [UI设计](https://help.aliyun.com/zh/model-studio/ui-designer) 功能配置前端交互界面，包括输入表单、响应模板、主题色等，发布后生效  
- **API 调用入口**：每个已发布应用自动获得唯一 `/v1/applications/{app_id}/invoke` OpenAPI 端点，支持 `POST` 请求调用（参见 [原文标题](../../raw/application-user-guide/application-publishing-and-sharing.md)）

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `visibility` | string | 是 | 取值：`private`（仅创建者）、`workspace`（同空间成员）、`public`（需空间开启公开发布白名单） |
| `component_enabled` | boolean | 否 | 设为 `true` 时启用组件模式，发布后生成 `component_id` 用于跨应用引用 |
| `ui_config` | object | 否 | JSON 结构，字段详见 [原文标题](../../raw/application-user-guide/application-publishing-and-sharing.md) 中 UI 设计文档链接说明 |
| `callback_url` | string | 否 | 异步调用时接收结果回调的 HTTPS 地址（仅 `visibility=private` 或 `workspace` 时可用） |

## 使用方式

1. 在应用详情页点击「发布」按钮，进入发布向导  
2. 选择可见性策略并配置组件开关（如需）  
3. （可选）进入 [UI设计](https://help.aliyun.com/zh/model-studio/ui-designer) 页面完成界面定制，保存后发布生效  
4. 发布成功后，获取分享链接、`component_id` 或 API 调用凭证  
> **注意**：使用 OpenAPI 发布时，`visibility=public` 参数需提前由空间管理员在「空间设置 → 应用管理」中开启白名单；控制台界面未显式提示该依赖，易导致发布失败 —— 详见 [原文标题](../../raw/application-user-guide/application-publishing-and-sharing.md) 中的权限说明章节。  

## 限制和注意事项

- 单个工作空间内最多发布 100 个公开链接应用（`visibility=public`），超出需联系管理员扩容  
- 已发布的组件不可直接修改 schema；如需变更输入/输出结构，须新建版本并重新发布  
- UI 设计配置仅影响 Web 端分享链接的渲染效果，对 API 调用无影响  
- `callback_url` 必须为有效 HTTPS 地址且响应超时 ≤ 10 秒，否则回调失败不重试  
- 所有分享链接默认有效期为永久，但空间管理员可在后台统一禁用某应用的分享状态

## 来源文档

- [应用发布与分享](../../raw/application-user-guide/application-publishing-and-sharing.md)


