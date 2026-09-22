# application publishing and sharing

百炼平台支持将智能体（Agent 1.0）和工作流应用以多种形态发布与共享，包括作为可复用组件接入其他AI应用、生成网页UI界面、集成至钉钉/微信等企业通讯平台，以及通过音视频实时互动渠道部署。所有发布行为均基于已创建并发布的应用，且需注意版本兼容性与运行时约束。

## 支持的模型/功能

- **支持的应用类型**：仅 [智能体应用（Agent 1.0）](raw/application-user-guide/application-publishing-and-sharing/share-an-application.md) 支持全部发布渠道（魔笔UI、钉钉、微信、组件、音视频互动）；Agent 2.0 仅支持 API 调用，不支持 UI 或第三方平台分享。
- **组件能力**：智能体或工作流应用均可发布为组件，供其他智能体（作为工具调用）或工作流（作为节点接入）复用。组件支持预设系统参数 `query`（String，必填）和 `imageList`（Array<String>，非必填），详见 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。
- **UI 应用**：通过 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md) 可将智能体或工作流应用封装为网页应用，支持拖放式低代码搭建、数据库集成、权限配置及一键发布至开发/生产环境。
- **实时互动**：图文类智能体或工作流应用可发布为音视频实时互动应用，支持 H5/APP 扫码体验及 SDK 集成。

## 关键参数

| 参数名 | 类型 | 是否必填 | 说明 | 来源 |
|--------|------|----------|------|------|
| `query` | String | 是 | 用户输入的自然语言指令，如“查询杭州天气” | [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md) |
| `imageList` | Array<String> | 否 | 图像公网地址列表，仅在启用视觉模型时生效 | [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md) |
| `biz_param` | Object | 否（按需） | API 调用时传入业务透传参数，用于覆盖组件配置中“业务透传”类参数 | [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md) |
| `API Key` | String | 是（UI/第三方平台必需） | 用于身份认证与计费归属，必须与应用、UI设计器处于同一业务空间 | [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md) |

> **注意**：文档2明确指出“Agent 2.0 不支持魔笔、钉钉、微信、组件、音视频等分享渠道”，而文档1未提及版本限制，易造成混淆。实际开发中应以文档2为准——组件发布功能仅对 Agent 1.0 和工作流应用有效，Agent 2.0 应用不可发布为组件。

## 使用方式

1. **发布为组件**  
   - 在应用编辑页点击「发布应用」→ 勾选「发布应用组件」→ 进入组件配置页设置名称、描述、参数别名、传参方式（`业务透传` 或 `模型识别`）及可见性。  
   - 已发布应用可在 [组件管理](https://bailian.console.aliyun.com/?tab=app#/component-manage) 中补发。  
   - 接入时：智能体在「技能」中选择组件；工作流拖入「组件节点」并绑定输入（如 `系统变量/query`）与输出（如 `组件1/result`）。

2. **发布为 UI 应用**  
   - 从应用发布渠道页点击「UI应用」→「创建」，自动填充基础信息；或直接进入 [UI设计器](https://bailian.console.aliyun.com/?tab=app#/app-ui) 选择模板新建。  
   - 编辑完成后发布至「开发环境」（24小时有效期，免费）或「生产环境」（需订阅套餐，支持自定义域名）。

3. **集成至第三方平台**  
   - **钉钉/微信**：在应用「发布平台」页签完成授权（需 SLR 与 API Key）、配置凭据（Client ID/Secret、模板 ID、AppID）及回调地址/二维码。  
   - **音视频互动**：在「AI实时互动」页签配置 API Key，生成临时体验链接或发布至 H5/APP/SDK 环境。

## 限制和注意事项

- **版本限制**：Agent 2.0 应用不支持任何 UI 或第三方平台分享渠道，仅可通过 API 调用，详见 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **嵌套与多级调用**：组件间禁止 A↔B 循环调用（导致死循环），也应避免 A→B→C 多级链式调用（易超时），该约束在 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md) 和 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md) 中均被强调。
- **参数识别差异**：`模型识别` 传参方式在智能体中由大模型自动填充，在工作流中**完全无效**——必须显式通过上游节点传入值，此关键差异在两篇文档中一致说明，但易被忽略。
- **环境与权限**：UI设计器、API Key、应用必须归属同一业务空间；UI 开发环境链接 24 小时失效；生产环境发布需订阅付费套餐。
- **计费归属**：所有通过分享链接、二维码、回调地址触发的调用，费用均由应用创建者 UID 账号承担。

## 来源文档

- [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)
- [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)
- [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)


