# application publishing and sharing

百炼平台支持将已构建的智能体应用（Agent 1.0）、工作流应用及 UI 应用以多种方式发布与共享，覆盖终端用户触达（如钉钉、微信、H5）、能力复用（组件化）和实时交互（音视频）三大场景。所有发布行为均需基于已发布的应用实例，并受 Agent 版本、业务空间隔离及权限模型约束。开发者应根据目标集成方式选择对应发布路径，并注意各渠道对模型类型、参数传递机制和运行环境的差异化要求。

## 支持的模型/功能

- **Agent 版本限制**：仅 **Agent 1.0** 智能体应用支持魔笔分享渠道、钉钉、微信、UI 应用、组件发布及音视频实时互动；**Agent 2.0 应用不支持任何 UI 或渠道类发布方式，仅可通过 API 调用** [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **应用类型支持**：
  - **智能体应用（Agent 1.0）**：支持全部发布方式（UI、钉钉、微信、组件、音视频）。
  - **工作流应用**：支持 UI 应用发布、组件发布、音视频实时互动（图文类），但**不支持钉钉/微信机器人发布**（该能力仅限 Agent 1.0）[UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
  - **UI 应用**：本身是发布产物，不可再作为源应用发布为其他渠道；但可集成智能体或工作流作为后端能力。
- **组件能力**：智能体或工作流均可发布为组件，供其他智能体（作为工具）或工作流（作为节点）引用。组件自动继承源应用的模型、MCP 服务及逻辑 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。

> **注意**：文档 1 中称“音视频实时互动仅支持图文对话类应用（含智能体应用和工作流应用）”，而文档 3 的 UI 设计器章节未明确排除工作流，但文档 1 的钉钉/微信发布说明中明确限定为 Agent 1.0。三者一致确认工作流**不支持钉钉/微信渠道**，此为版本能力边界，非矛盾。

## 关键参数

| 参数 | 适用场景 | 说明 |
|--------|----------|------|
| `API Key` | 所有需调用百炼服务的发布方式（UI、钉钉、微信、音视频） | 必须与目标应用、UI 设计器位于**同一业务空间**；未配置时 UI/钉钉/微信流程会失败 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。 |
| `query` / `imageList` | 组件发布与引用 | 系统预设参数，不可删除；`query` 为必填 String 类型，用于传递用户文本输入；`imageList` 为非必填 Array<String>，仅在启用[多模态](../concepts/multi-modal.md)模型时生效 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。 |
| `传参方式`（业务透传 / 模型识别） | 组件参数配置 | 在智能体中引用时，“模型识别”允许大模型自动填充参数；在工作流中引用时，**无论设置为何种方式，均需上游节点显式传入值**，模型识别逻辑不生效 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。 |
| `回调地址`（钉钉）、`二维码`（微信）、`分享链接`（UI/音视频） | 渠道分发 | 均为一次性或短期有效凭证（如 UI 开发环境链接有效期 24 小时），生产环境需绑定自定义域名或完成 SLR 授权 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。 |

## 使用方式

1. **前置条件**：确保目标应用（智能体或工作流）已完成构建并**已发布**；确认 API Key 与应用同属一个业务空间。
2. **入口统一**：进入百炼控制台 → [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) → 选择目标应用 → 点击**发布**按钮 → 切换至对应页签（如“发布平台”、“AI实时互动”、“UI应用”或“组件”）。
3. **分渠道操作**：
   - **UI 应用**：在“UI应用”页签创建，系统自动填充基础信息；编辑后发布至开发环境（免费，24 小时失效）或生产环境（需订阅套餐）[UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
   - **钉钉/微信**：在“发布平台”页签授权计算巢 AppFlow（SLR + API Key 加密传输），配置平台凭证（Client ID/Secret、模板 ID、AppID），获取回调地址或二维码分发 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
   - **组件**：在“组件”页签或 [组件管理](https://bailian.console.aliyun.com/?tab=app#/component-manage) 页面创建；需明确定义名称、描述、参数别名、可见性及传参方式 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。
   - **音视频实时互动**：在“AI实时互动”页签配置，生成临时体验二维码（24 小时）或发布至 H5/APP/SDK 渠道；需开通智能媒体服务并完成 SLR 授权 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。

## 限制和注意事项

- **Agent 版本硬限制**：Agent 2.0 应用完全不支持 UI、钉钉、微信、组件、音视频等发布能力，仅开放 API 接口。迁移前务必确认版本兼容性。
- **嵌套与多级调用禁止**：组件间禁止 A→B→A 循环调用（导致死循环），也应避免 A→B→C 多级链式调用（易超时）[分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **工作流组件传参强制性**：即使参数设为“模型识别”，工作流中仍需上游节点显式提供输入值；该模式仅在智能体中生效 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。
- **环境与计费隔离**：UI 开发环境链接 24 小时失效且不可续期；生产环境需订阅付费套餐并配置自定义域名；所有模型调用费用由应用创建者 UID 账号承担，与访问者身份无关 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
- **权限与访问控制**：默认分享链接仅限阿里云用户访问；如需匿名访问，须在 UI 设计器中显式开启“允许匿名访问”并配置权限组 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。

## 来源文档

- [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)
- [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)
- [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)


