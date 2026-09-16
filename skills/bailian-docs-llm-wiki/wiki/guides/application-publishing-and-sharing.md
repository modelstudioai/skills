# application publishing and sharing

百炼平台支持将智能体（Agent 1.0）和工作流应用以多种方式发布与共享，包括作为可复用组件接入其他AI应用、封装为网页UI应用、集成至钉钉/微信等第三方平台，以及通过音视频实时互动渠道部署。所有发布行为均需在统一业务空间内完成，且依赖已发布的应用及有效的API Key。核心能力围绕模块化复用、低代码界面交付和跨平台分发展开。

## 支持的模型/功能

- **组件化能力**：智能体或工作流应用可发布为标准化组件，供其他智能体（作为工具）或工作流（作为节点）调用，实现功能复用。组件预设系统参数 `query`（String，必填）和 `imageList`（Array<String>，非必填），支持传参方式为“业务透传”或“模型识别”[使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。
- **UI应用发布**：通过可视化UI设计器，可将已发布的智能体或工作流快速封装为网页应用，支持PC/H5多端访问，并集成数据库、文件存储、权限管理（如匿名访问、钉钉/企微登录）等功能[UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
- **第三方平台分发**：支持发布至钉钉机器人、微信公众号、音视频实时互动（H5/APP扫码或SDK集成）等渠道，但**仅限 Agent 1.0 应用**；Agent 2.0 仅支持 API 调用，不支持上述分享渠道[分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。

> **注意**：文档3明确指出“分享渠道（魔笔分享渠道、钉钉、微信、组件、音视频实时互动）均为 **Agent 1.0** 智能体应用的功能”，而文档1中示例未限定Agent版本，易引发混淆。实际开发中，若使用Agent 2.0，仅能通过API集成，不可用于组件发布或UI/钉钉等渠道分发。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 传参方式约束 |
|--------|------|------|------|--------------|
| `query` | String | 是 | 用户输入的自然语言指令（如“查询杭州天气”） | 智能体中支持“模型识别”或“业务透传”；工作流中**必须**用“业务透传”显式传入 |
| `imageList` | Array<String> | 否 | 图像公网URL列表，仅当组件使用视觉模型时有效 | 同上，且需在配置中设为“是否可见=否”以隐藏于文本模型场景 |
| `biz_param` | Object | 否（按需） | API调用时传递业务参数的顶层字段，用于透传`query`等值 | 仅适用于API调用场景，不适用于UI/钉钉等托管渠道 |

- 所有预设系统参数不可删除，仅可通过“是否可见”控制暴露状态。
- 组件别名（Alias）用于避免参数名冲突，调用方仅感知别名，不影响内部逻辑。

## 使用方式

1. **发布为组件**  
   - 在应用编辑页点击**发布应用** → 勾选**发布应用组件** → 配置组件名称、描述、参数（含别名、是否可见、传参方式）→ 确定发布。  
   - 或通过**[组件管理](https://bailian.console.aliyun.com/?tab=app#/component-manage)**面板，对已发布应用创建组件。  
   - 接入时：智能体在“技能”中选择组件；工作流拖入“组件节点”并绑定。

2. **发布为UI应用**  
   - 进入应用发布渠道 → 选择**UI应用** → 创建（自动填充基础信息）→ 进入UI设计器编辑界面 → 拖放组件搭建页面 → 右上角**发布**至开发环境（24小时有效期）或生产环境（需订阅套餐）[UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。

3. **发布至第三方平台**  
   - **钉钉/微信**：在应用**发布平台**页签，完成API Key授权、配置凭证（Client ID/Secret、模板ID、AppID等）→ 获取回调地址或二维码 → 分享给目标用户。  
   - **音视频互动**：在**AI实时互动**页签配置API Key → 生成临时体验二维码（24小时）→ 发布后支持H5扫码或SDK集成。

## 限制和注意事项

- **Agent版本限制**：钉钉、微信、UI应用、音视频互动及组件发布功能**仅支持 Agent 1.0**；Agent 2.0 应用无法使用这些发布渠道，仅支持API调用[分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **嵌套与多级调用风险**：组件间禁止A调B、B再调A（嵌套调用），否则导致死循环；A→B→C等多级调用易触发超时（因总运行时间受限）[使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。
- **业务空间一致性**：UI设计器、API Key、智能体/工作流应用**必须归属同一业务空间**，否则无法关联或发布[UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
- **开发环境时效性**：UI应用发布至开发环境后链接**24小时失效**，需重新发布；生产环境需订阅付费套餐并配置自定义域名。
- **参数识别差异**：工作流中即使将参数设为“模型识别”，也不会自动推断值，**必须手动从上游节点传入**；该行为与智能体不同，需特别注意配置一致性[使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。

## 来源文档

- [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)
- [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)
- [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)


