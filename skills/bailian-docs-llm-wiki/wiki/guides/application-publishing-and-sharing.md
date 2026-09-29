# application publishing and sharing

百炼平台提供多种应用发布与共享能力，支持将智能体（Agent 1.0）、工作流及 UI 应用以网页、钉钉、微信、音视频互动、可复用组件等形式对外交付。所有发布行为均需在统一业务空间内完成，且依赖有效的 API Key 和已发布的上游应用。核心路径包括：通过 UI 设计器构建可视化界面、通过分享渠道集成至第三方平台、或发布为可被其他智能体/工作流复用的模块化组件。

## 支持的模型/功能

- **UI 应用**：基于魔笔低代码平台，支持拖放式页面搭建，预置 4 类模板（如企业AI知识库Lite、AI基础对话等），兼容 PC/H5 终端；支持数据库表自动映射、文件上传、权限组管理及 OIDC/OAuth 2.0 登录集成 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。  
- **第三方平台集成**：仅限 **Agent 1.0** 智能体应用（Agent 2.0 不支持），支持钉钉机器人、微信公众号、音视频实时互动（H5/APP/SDK）三种发布渠道 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。  
- **组件化复用**：智能体或工作流可发布为组件，供其他智能体（作为工具调用）或工作流（作为节点接入）使用；预设 `query` 和 `imageList` 系统参数，支持 `业务透传` 与 `模型识别` 两种传参方式 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。

> **注意**：文档 2 明确指出“分享渠道（魔笔分享渠道、钉钉、微信、组件、音视频实时互动）均为 **Agent 1.0** 智能体应用的功能。**Agent 2.0** 智能体应用仅支持通过 API 调用，不支持上述分享渠道”，而文档 3 在“步骤二：发布应用为组件”中未限定 Agent 版本，存在潜在矛盾。实际开发中请严格遵循文档 2 的版本约束，即仅 Agent 1.0 可发布为组件并用于分享渠道。

## 关键参数

| 参数名 | 说明 | 约束 |
|--------|------|------|
| `API Key` | 调用百炼服务的认证凭证，必须与目标应用、UI 设计器位于同一业务空间 | 必填；不支持跨空间引用 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md) |
| `百炼智能体` | 已发布的 Agent 1.0 或工作流应用 ID | 必填；UI 设计器中若无法选择，需检查业务空间一致性 |
| `query` / `imageList` | 组件预设系统参数，分别用于传递文本输入和图像 URL 列表 | `query` 类型为 `String`，建议设为必填；`imageList` 类型为 `Array<String>`，仅当组件使用视觉模型时有效 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md) |
| `传参方式` | 分 `业务透传`（由调用方显式传入）和 `模型识别`（仅智能体中由大模型自动填充） | 工作流中无论配置为何种方式，均需上游节点明确提供输入值 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md) |

## 使用方式

1. **UI 应用发布流程**：  
   - 进入 [UI设计器](https://bailian.console.aliyun.com/?tab=app#/app-ui)，选择模板或空白画布 → 填写应用名称、API Key、绑定智能体 → 配置数据库映射（可选）→ 拖放组件编辑界面 → 点击右上角 **发布** → 选择**开发环境**（24 小时有效期，免费）或**生产环境**（需订阅团队版套餐）[UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。  

2. **第三方平台发布流程**：  
   - 在智能体应用的 **发布渠道** 页签，依次选择钉钉/微信/音视频等卡片 → 完成授权（SLR + API Key 加密传输）→ 配置平台凭证（如钉钉 Client ID/Secret、微信 AppID）→ 获取回调地址或二维码 → 分享给终端用户 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。  

3. **组件发布与接入流程**：  
   - 在智能体/工作流编辑页点击 **发布应用** → 勾选 **发布应用组件** → 设置组件名称、描述、参数别名及传参方式 → 发布后，在其他智能体的 **技能** 中选择该组件，或在工作流画布中拖入 **组件节点** 并绑定 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。

## 限制和注意事项

- **环境时效性**：UI 应用在**开发环境**发布的链接有效期为 **24 小时**，到期后需重新发布；生产环境发布长期有效，但需付费订阅 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。  
- **版本兼容性**：仅 **Agent 1.0** 支持所有分享渠道（含 UI、钉钉、微信、音视频、组件），Agent 2.0 仅支持 API 调用，此限制为硬性要求 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。  
- **调用安全边界**：  
  - 避免组件嵌套调用（A→B→A）或深度多级调用（A→B→C），否则易触发超时或循环调用错误 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)；  
  - 工作流中引用组件时，即使参数配置为 `模型识别`，也**必须**由上游节点显式传入值，不可依赖模型自动推断 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。  
- **权限与计费**：默认分享链接仅对持有链接的阿里云用户开放；匿名访问需手动开启并配置权限组；生产环境发布、自定义域名、超出免费额度的文件/数据库存储均需付费 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。

## 来源文档

- [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)
- [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)
- [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)


