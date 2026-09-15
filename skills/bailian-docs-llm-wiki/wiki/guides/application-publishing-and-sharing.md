# application publishing and sharing

百炼平台支持将智能体（Agent 1.0）和工作流应用以多种方式发布与共享，包括作为可复用组件接入其他AI应用、封装为网页UI应用、集成至钉钉/微信等第三方平台，以及通过音视频实时互动渠道部署。所有发布行为均需在统一业务空间内完成，且依赖已发布的应用及有效的API Key。核心能力围绕模块化复用、低代码界面交付和跨平台分发展开。

## 支持的模型/功能

- **组件化能力**：智能体或工作流应用可发布为标准化组件，供其他智能体（作为工具）或工作流（作为节点）调用，实现功能复用。组件支持预设系统参数 `query`（String，必填）和 `imageList`（Array<String>，非必填），并可通过别名、可见性、传参方式（业务透传 / 模型识别）精细控制接入逻辑 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。
- **UI应用**：通过可视化UI设计器，可将智能体或工作流快速封装为网页应用，支持PC/H5多端访问，内置权限管理、数据库映射和文件存储能力 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
- **第三方平台集成**：支持发布至钉钉机器人、微信公众号、魔笔分享渠道及音视频实时互动（H5/APP/SDK），其中钉钉与微信需配置Client ID/Secret、模板ID等凭证，并完成SLR授权 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **版本限制**：仅 **Agent 1.0** 智能体支持全部分享渠道；**Agent 2.0** 仅支持API调用，不支持UI、钉钉、微信、组件等发布方式 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。

## 关键参数

| 参数 | 类型 | 必填 | 说明 | 适用场景 |
|------|------|------|------|----------|
| `query` | String | 是 | 用户输入的自然语言指令，如“查询杭州天气” | 所有文本类组件默认入参 |
| `imageList` | Array<String> | 否 | 图像公网URL列表，仅当组件使用视觉模型时生效 | 视觉理解类组件 |
| `biz_param` | Object | 否（按需） | API调用时传递业务透传参数的字段，用于填充组件中设为“业务透传”的参数 | 服务端集成场景 |
| API Key | String | 是 | 调用百炼服务的身份凭证，必须与应用、UI设计器同属一个业务空间 | UI应用、钉钉、微信、音视频等所有外部集成 |

> **注意**：文档1中描述“组件自动更新”（应用重新发布即触发组件更新），但文档3未提及该机制，且文档3的组件发布流程未说明更新策略。实际行为以控制台最新逻辑为准，建议发布后手动验证组件版本一致性。

## 使用方式

1. **发布为组件**  
   - 在应用编辑页点击**发布应用** → 勾选**发布应用组件** → 配置组件名称、描述、参数（别名、是否可见、传参方式）→ 确定发布。  
   - 已发布应用也可在[组件管理](https://bailian.console.aliyun.com/?tab=app#/component-manage)中补发。  
   - 接入时：智能体在“技能”中选择组件；工作流拖入“组件节点”并绑定。

2. **发布为UI应用**  
   - 进入应用发布渠道 → 选择**UI应用** → 创建或编辑UI（可选模板）→ 配置API Key、智能体、数据库映射 → 发布至开发环境（24小时有效）或生产环境（需订阅套餐） [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。

3. **发布至第三方平台**  
   - **钉钉/微信**：在应用**发布平台**页签授权计算巢AppFlow → 配置凭证（Client ID/Secret、模板ID、AppID）→ 获取回调地址或二维码 → 在对应平台完成机器人/公众号配置。  
   - **音视频互动**：在**AI实时互动**页签配置API Key → 生成临时体验二维码（24小时）→ 发布后开通智能媒体服务并创建互动智能体。

## 限制和注意事项

- **业务空间隔离**：应用、API Key、UI设计器、数据库等资源必须归属同一业务空间，否则无法关联或发布 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
- **嵌套与多级调用风险**：组件间禁止A→B→A循环调用；A→B→C三级调用易因超时失败，建议控制在两层以内 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。
- **开发环境时效性**：UI应用和音视频临时体验链接均**24小时后失效**，生产环境需订阅付费套餐并绑定自定义域名 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
- **Agent版本兼容性**：钉钉、微信、UI、组件等所有分享渠道**仅支持Agent 1.0**；Agent 2.0应用无法使用这些功能，仅开放API接口 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **视觉参数约束**：`imageList`参数仅在组件明确使用[图像与视频理解模型](raw/model-user-guide/model-experience/vision-model/vision.md)时生效，文本模型组件中应隐藏该参数。

## 来源文档

- [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)
- [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)
- [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)


