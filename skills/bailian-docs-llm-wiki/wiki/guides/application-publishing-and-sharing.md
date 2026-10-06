# application publishing and sharing

百炼平台支持将已构建的智能体应用（Agent 1.0）、工作流应用及 UI 应用以多种方式发布与共享，覆盖终端用户触达（如钉钉、微信、H5）、能力复用（组件化）和实时交互（音视频）三大场景。所有发布行为均需基于已发布的应用，并受 Agent 版本、业务空间隔离、权限与计费策略约束。开发者应优先确认目标应用类型与版本兼容性，再选择适配的发布路径。

## 支持的模型/功能

- **Agent 1.0 智能体应用**：完整支持全部发布渠道，包括魔笔分享渠道、钉钉机器人、微信公众号、组件化、音视频实时互动及 UI 应用集成。  
- **Agent 2.0 智能体应用**：**仅支持 API 调用**，不支持任何 UI 或第三方平台分享渠道（如钉钉、微信、UI 应用等）[分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。  
- **工作流应用**：支持发布为组件、接入 UI 应用、音视频实时互动（图文类），但**不支持直接发布为钉钉/微信机器人**；其作为组件被引用时，参数必须显式传入（即使配置为“模型识别”）[使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。  
- **UI 应用**：基于魔笔低代码平台构建，可集成 Agent 1.0 或工作流应用，支持开发/生产双环境部署，但**生产环境需订阅付费套餐** [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。

> **注意**：文档 1 中称“音视频实时互动仅支持图文对话类应用（含智能体应用和工作流应用）”，而文档 3 明确 UI 应用亦可接入音视频能力（通过 SDK 或 H5 扫码）。二者无矛盾，因 UI 应用本身是容器，其内嵌的智能体/工作流才是实际处理逻辑——故音视频能力最终仍作用于底层 Agent 1.0 或工作流。

## 关键参数

| 参数 | 说明 | 约束与注意事项 |
|------|------|----------------|
| `API Key` | 用于调用百炼服务的身份凭证，所有发布渠道（钉钉、微信、UI、音视频）均需绑定 | 必须与目标应用、UI 设计器处于**同一业务空间**；未授权时需完成 SLR 关联与密钥加密传输授权 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md) |
| `query` / `imageList` | 组件预设系统参数，分别用于传递文本输入与图像 URL 列表 | `query` 类型为 `String`，默认必填；`imageList` 类型为 `Array<String>`，仅在启用多模态模型时生效；二者不可删除，但可通过“是否可见”隐藏 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md) |
| `biz_param` | API 调用时传入业务透传参数的字段名 | 仅对智能体应用有效；当组件配置“业务透传”且测试时未手动填入入参变量，需通过此字段显式传参 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md) |
| [Token](../concepts/token.md) 有效期 | UI 应用开发环境链接、音视频临时体验二维码均具时效性 | 开发环境 UI 链接**24 小时后失效**；音视频临时二维码同样为 24 小时 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md) |

## 使用方式

1. **UI 应用发布**：进入应用「发布渠道」页签 → 选择「UI 应用」→「创建」→ 自动填充基础信息（API Key、智能体、图标等）→ 编辑 UI 后发布至开发/生产环境 → 获取应用地址分享 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。  
2. **第三方平台发布（钉钉/微信）**：在「发布平台」页签 → 授权计算巢 AppFlow（首次需 SLR + API Key 加密授权）→ 配置平台凭证（钉钉：Client ID/Secret + 卡片模板 ID；微信：AppID）→ 获取回调地址或二维码 → 在对应平台完成机器人/公众号配置 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。  
3. **组件化发布**：在应用编辑页点击「发布应用」→ 勾选「发布应用组件」→ 或进入「组件管理」面板 → 「+ 创建」→ 设置组件名称、描述、参数别名/是否可见/传参方式/默认值 → 发布后，在其他智能体（作为技能）或工作流（作为节点）中引用 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。  
4. **音视频实时互动**：在「AI 实时互动」页签 → 选择语音/视频 → 配置 API Key → 生成临时二维码或链接测试 → 发布后开通智能媒体服务并授权 SLR → 选择 H5/APP 扫码或 SDK 集成 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。

## 限制和注意事项

- **Agent 版本限制**：Agent 2.0 应用**完全不支持**除 API 外的任何发布渠道，该限制为硬性约束，无法绕过 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。  
- **组件调用风险**：禁止 A 调用 B 同时 B 调用 A（嵌套调用），会导致无限循环；A→B→C（多级调用）易触发运行超时，建议控制在两级以内 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。  
- **业务空间强隔离**：API Key、智能体应用、UI 设计器三者必须归属同一业务空间，否则在 UI 创建或组件配置中无法下拉选择对应资源 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。  
- **计费主体明确**：所有通过分享链接产生的模型调用费用，均由应用创建者 UID 账号承担；生产环境 UI 发布需额外订阅套餐 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。  
- **工作流组件传参强制性**：即使组件参数配置为“模型识别”，在工作流中引用时**仍需上游节点显式提供输入值**，大模型不会自动推断——此行为与智能体场景不同，属关键差异点 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。

## 来源文档

- [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)
- [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)
- [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)


