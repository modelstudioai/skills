# application publishing and sharing

百炼平台支持将智能体（Agent 1.0）和工作流应用以多种方式发布与共享，包括对外提供 Web UI、集成至钉钉/微信等第三方平台、作为可复用组件被其他智能体或工作流调用，以及通过音视频实时互动渠道部署。所有发布行为均基于已创建并发布的应用，且需注意 Agent 版本兼容性与运行时约束。

## 支持的模型/功能

- **支持的应用类型**：仅 [Agent 1.0](raw/application-user-guide/llm-application/single-agent-application.md) 智能体和工作流应用支持全部发布渠道（UI 应用、钉钉、微信、组件、音视频实时互动）；[Agent 2.0](raw/application-user-guide/llm-application/agent2-introduction.md) 仅支持 API 调用，**不支持**任何 UI 或渠道类分享功能。
- **核心发布形态**：
  - **UI 应用**：通过 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md) 构建可视化界面，支持拖放式低代码开发、多端适配（PC/H5）、权限管理及一键发布至开发/生产环境。
  - **第三方渠道**：支持发布至钉钉机器人、微信公众号，需配置 API Key、平台凭证（Client ID/Secret）及消息模板（如钉钉卡片 ID）。
  - **组件化复用**：智能体或工作流可发布为标准化组件，供其他智能体（作为工具）或工作流（作为节点）接入，实现跨应用能力复用。
  - **音视频实时互动**：支持图文类智能体/工作流发布为语音或视频交互应用，提供扫码体验、H5/APP 分享及 SDK 集成路径。

> **注意**：文档 2 明确指出“分享渠道（魔笔分享渠道、钉钉、微信、组件、音视频实时互动）均为 **Agent 1.0** 智能体应用的功能”，而文档 1 未限定 Agent 版本即描述组件发布流程，存在隐含矛盾。实际使用中，**组件发布仅对 Agent 1.0 和工作流应用有效**，Agent 2.0 不支持该能力 —— 此处以文档 2 的明确版本约束为准。

## 关键参数

- **组件参数（发布为组件时必配）**：
  - `query`（String，必填）：默认系统参数，用于传递用户文本输入，别名建议设为 `userQuery`，传参方式可选 `业务透传` 或 `模型识别`。
  - `imageList`（Array<String>，非必填）：默认系统参数，用于传递图像公网地址列表，仅在组件启用视觉模型时有效；若无需图像输入，须将“是否可见”设为否。
  - 所有预设系统参数不可删除，仅可通过“是否可见”控制暴露状态。
- **UI 应用参数**：
  - `百炼API-KEY` 和 `百炼智能体`：必须与 UI 所属**同一业务空间**，否则无法选择（见 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md) 文档）。
  - 文件类自定义参数（如工作流中 `files[0]`）：需在 UI 设计器中显式映射为 `{{{file_name:files[0]}}}` 格式，否则上传文件无法透传。
- **渠道类参数（钉钉/微信）**：
  - 钉钉：需 `钉钉模版ID`、`钉钉Client ID`、`钉钉Client Secret` 及回调地址；其中模版 ID 必须关联已申请 `Card.Streaming.Write` 权限的应用。
  - 微信：需 `开发者ID（AppID）`，从微信公众号后台获取。

## 使用方式

- **发布为组件**：
  1. 在应用编辑页点击 **发布 → 发布渠道 → 组件 → 创建**；
  2. 填写组件名称、描述，配置 `query`/`imageList` 等参数的别名、是否必填、是否可见、传参方式；
  3. 发布后，可在其他智能体的“技能”中添加，或在工作流画布中拖入“组件节点”并选择该组件。
- **发布为 UI 应用**：
  1. 进入应用发布页，选择 **UI应用 → 创建**（自动填充基础信息），或直接访问 [UI设计器](https://bailian.console.aliyun.com/?tab=app#/app-ui) 新建；
  2. 使用预置模板（如“企业AI知识库Lite”）或空白模板搭建页面，集成智能体、数据库等资源；
  3. 点击 **发布 → 开发环境**（免费，24小时有效期）或 **生产环境**（需订阅套餐）。
- **发布至钉钉/微信**：
  1. 在应用发布页选择对应渠道卡片，完成授权（首次需授权计算巢 AppFlow SLR 及 API-Key 加密传输）；
  2. 配置平台凭证（钉钉 Client ID/Secret、微信 AppID）及模板 ID；
  3. 获取回调地址（钉钉）或二维码（微信），分发给目标用户或群组。
- **音视频实时互动**：
  1. 在应用 **AI实时互动** 页签点击 **去配置**，绑定 API Key；
  2. 生成临时二维码或分享链接体验；
  3. 正式发布需开通智能媒体服务并完成 SLR 授权。

## 限制和注意事项

- **Agent 版本限制**：所有非 API 类发布方式（UI、钉钉、微信、组件、音视频）**仅支持 Agent 1.0**，Agent 2.0 无对应入口 —— 此限制在 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md) 中明确说明。
- **组件调用约束**：
  - **禁止嵌套调用**：A 调用 B 且 B 又调用 A 将导致无限循环，功能不可用。
  - **慎用多级调用**：A→B→C 等链式调用易触发最长运行时间超时，应尽量扁平化设计。
  - **工作流中“模型识别”无效**：即使组件参数设为“模型识别”，工作流仍需上游节点**显式传入值**，不能依赖大模型自动推断（见 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)）。
- **环境与权限**：
  - UI 应用开发环境链接**24 小时失效**，生产环境需订阅付费套餐并配置自定义域名。
  - 所有分享链接默认仅限**阿里云用户访问**，费用由应用创建者 UID 承担；如需匿名访问，须在 UI 设计器中开启“允许匿名访问”并配置权限组。
- **计费关联**：
  - UI 设计器本身免费，但模型调用、文件存储（1GB 免费）、数据库（0.3GB 免费）及生产环境发布均按量计费（详见 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md) 计费说明）。

> **注意**：文档 1 与文档 2 对“组件发布”的入口描述存在细微差异（文档 1 提到“组件管理面板”，文档 2 仅提“发布渠道页签”），但二者最终指向同一控制台路径（`#/component-manage` 或 `#/app-center` 内的发布操作），属 UI 导航路径差异，无实质矛盾。

## 来源文档

- [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)
- [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)
- [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)


