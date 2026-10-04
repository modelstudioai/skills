# application publishing and sharing

百炼平台支持将智能体（Agent 1.0）和工作流应用以多种方式发布与共享，包括作为可复用组件接入其他AI应用、封装为网页UI应用、集成至钉钉/微信等第三方平台，以及启用音视频实时互动能力。所有发布行为均需基于已创建并发布的应用，且不同渠道对应用版本（如 Agent 1.0 vs Agent 2.0）有明确兼容性要求。

## 支持的模型/功能

- **组件化能力**：智能体或工作流应用可发布为模块化组件，供其他智能体或工作流调用，实现功能复用。组件支持预设系统参数（如 `query`、`imageList`），并可通过 `模型识别` 或 `业务透传` 方式传参 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。
- **UI应用**：通过可视化UI设计器，可将智能体或工作流快速封装为网页应用，支持PC/H5多端访问，并集成数据库、文件存储、权限管理等功能 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
- **第三方平台集成**：支持发布至钉钉机器人、微信公众号、魔笔分享渠道；其中钉钉/微信需配置API Key、Client ID/Secret及消息模板ID等凭证 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **音视频实时互动**：仅支持图文类智能体或工作流应用，提供H5扫码体验、APP集成及SDK开发集成路径，适用于语音/视频交互场景 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。

> **注意**：文档 3 明确指出“分享渠道（魔笔分享渠道、钉钉、微信、组件、音视频实时互动）均为 **Agent 1.0** 智能体应用的功能。**Agent 2.0** 智能体应用仅支持通过 API 调用，不支持上述分享渠道”。而文档 1 和文档 2 均未提及 Agent 版本限制，存在隐含矛盾。开发者在使用钉钉、微信、UI应用或组件发布时，**必须确保目标应用为 Agent 1.0 版本**，否则相关发布操作将不可用。

## 关键参数

| 参数名 | 类型 | 是否必填 | 说明 | 来源 |
|--------|------|----------|------|------|
| `query` | String | 是 | 用户输入的自然语言指令，如“查询杭州天气” | [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md) |
| `imageList` | Array<String> | 否 | 图像公网地址列表，仅在启用视觉模型时生效 | [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md) |
| `biz_param` | Object | 否（按需） | API调用时传递业务参数，用于填充组件中设为“业务透传”的入参 | [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md) |
| `API Key` | String | 是（UI/钉钉/微信必需） | 用于身份认证和计费归属，**必须与应用同属一个业务空间** | [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md) |

## 使用方式

1. **发布为组件**：在应用编辑页点击「发布应用」→ 勾选「发布应用组件」，或进入[组件管理](https://bailian.console.aliyun.com/?tab=app#/component-manage)页面创建；配置组件名称、描述及参数（别名、是否可见、传参方式等）后发布。
2. **发布为UI应用**：在应用发布渠道选择「UI应用」→ 自动填充基础信息（API Key、智能体等）→ 进入UI设计器拖放组件搭建界面 → 发布至开发环境（24小时有效）或生产环境（需订阅套餐）。
3. **发布至第三方平台**：
   - **钉钉/微信**：在「发布平台」页签完成授权 → 配置凭证（Client ID/Secret、模板ID、AppID）→ 获取回调地址或二维码 → 在对应平台完成机器人配置。
   - **音视频互动**：在「AI实时互动」页签配置API Key → 生成临时体验二维码 → 发布后开通智能媒体服务并完成SLR授权。
4. **接入组件**：
   - 智能体中：在「技能」区域添加已发布组件，大模型根据组件描述和上下文自动决策调用；
   - 工作流中：拖入「组件节点」并选择目标组件，手动连接上游节点输出至组件输入参数。

## 限制和注意事项

- **版本限制**：钉钉、微信、UI应用、组件、音视频互动等所有分享渠道**仅支持 Agent 1.0 应用**，Agent 2.0 应用不兼容 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **嵌套与多级调用**：禁止 A 调用 B、B 再调用 A 的循环嵌套；避免 A→B→C 等三级及以上调用链，否则易因超时导致失败 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。
- **参数传参差异**：组件参数设为“模型识别”时，在智能体中由大模型自动填充；但在工作流中**该模式无效**，必须通过上游节点显式传入值 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。
- **环境有效期**：UI应用开发环境链接有效期为24小时，需重新发布才能继续访问；生产环境需订阅付费套餐并绑定自定义域名 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
- **业务空间一致性**：UI设计器、API Key、智能体应用三者**必须归属于同一业务空间**，否则无法关联配置 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。

## 来源文档

- [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)
- [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)
- [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)


