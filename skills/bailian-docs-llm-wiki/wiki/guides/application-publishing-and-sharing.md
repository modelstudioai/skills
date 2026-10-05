# application publishing and sharing

百炼平台支持将已构建的智能体应用（Agent 1.0）、工作流应用及 UI 应用以多种方式发布与共享，覆盖嵌入式集成（组件）、多端触达（钉钉/微信/H5/APP）、实时音视频交互等场景。所有发布行为均需基于已发布的应用，并受 Agent 版本、业务空间隔离、权限与计费策略约束。开发者应根据目标使用方和集成深度选择合适方式。

## 支持的模型/功能

- **Agent 版本限制**：仅 **Agent 1.0** 智能体应用支持魔笔分享渠道、钉钉、微信、UI 应用、音视频实时互动及组件发布；**Agent 2.0 应用仅支持 API 调用**，不支持上述任何分享渠道 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **支持的应用类型**：
  - 智能体应用（Agent 1.0）
  - 工作流应用（任务型/对话型）
  - UI 应用（基于魔笔低代码平台构建）
- **核心共享能力**：
  - **UI 应用**：通过可视化设计器构建网页界面，一键发布至开发/生产环境，支持匿名访问与权限组配置 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
  - **第三方平台集成**：钉钉机器人（需配置 Client ID/Secret、卡片模板 ID 及 `Card.Streaming.Write` 权限）、微信公众号（需 AppID 授权）。
  - **音视频实时互动**：仅支持图文类应用（智能体/工作流），提供 H5/APP 扫码体验与 SDK 集成两种模式。
  - **组件化复用**：智能体或工作流可发布为可被其他智能体/工作流引用的模块化组件，支持 `query` 和 `imageList` 等预设系统参数。

> **注意**：文档 1 中称“通过音视频实时互动发布应用”仅支持“图文对话类应用（含智能体应用和工作流应用）”，而文档 3 的 UI 设计器说明中明确指出其可集成“百炼智能体、大模型、数据库和 HTTP 服务等多种资源”。二者无直接冲突，但需注意：音视频互动能力本身**不作用于 UI 应用**，而是独立通道；UI 应用若需音视频能力，须通过 SDK 集成 AICallKit 实现，而非通过 UI 设计器原生支持。

## 关键参数

| 参数 | 说明 | 使用场景 | 约束 |
|------|------|----------|------|
| `API Key` | 百炼平台调用凭证，用于身份认证与计费归属 | 所有对外发布渠道（钉钉、微信、UI、音视频、组件调用）必需 | 必须与目标应用、UI 设计器处于**同一业务空间** [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md) |
| `query` / `imageList` | 组件预设系统参数，不可删除；`query` 类型为 `String`（必填），`imageList` 类型为 `Array<String>`（非必填） | 组件接入智能体/工作流时传递用户输入 | 若组件不处理图像，应将 `imageList` 的 **是否可见** 设为 `否` |
| `biz_param` | API 调用时传入业务透传参数的字段名 | 当组件含 `业务透传` 参数且需在 API 调用中显式传参时使用 | 仅对智能体应用有效；工作流中必须通过上游节点显式连接 |
| 回调地址 / Token / 分享链接 | 各渠道唯一访问入口 | 钉钉（回调地址）、微信（二维码）、UI（应用地址）、音视频（临时二维码/分享链接） | UI 开发环境链接**24 小时失效**；生产环境需订阅付费套餐 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md) |

## 使用方式

1. **前置条件**  
   - 应用已完成构建并**已发布**（未发布应用无法进入发布渠道页签）；
   - 确认当前操作账号具备对应资源（API Key、智能体、UI）的读写权限；
   - 所有资源（应用、API Key、UI）必须位于**同一业务空间**。

2. **通用操作路径**  
   进入百炼控制台 → **[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)** → 选择目标应用 → 切换至 **发布渠道**（或 **AI实时互动** / **UI应用**）页签 → 根据渠道点击对应卡片的 **创建** 或 **请先授权** → 按向导完成配置。

3. **典型流程示例**  
   - **发布为组件**：在发布渠道页签 → 悬停 **组件** → 点击 **+ 创建** → 填写组件名称、描述、参数别名/描述/传参方式 → 单击 **确定发布** → 在其他智能体/工作流中通过技能面板或组件节点引用 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。  
   - **发布为 UI 应用**：在发布渠道页签 → 点击 **UI应用** → **创建** → 自动填充基础信息（可编辑）→ **立即创建** → 进入 UI 设计器编辑 → 右上角 **发布** 至开发/生产环境 → 获取 **应用地址** 分享 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。  
   - **接入钉钉**：完成计算巢 AppFlow 授权 → 配置钉钉 Client ID/Secret、卡片模板 ID → 获取百炼侧 **回调地址** → 在钉钉开放平台配置机器人（HTTP 模式）并绑定该地址 → 发布钉钉应用版本 → 在群聊中添加并 @ 机器人测试。

## 限制和注意事项

- **Agent 版本硬性限制**：Agent 2.0 应用完全不支持除 API 外的任何发布渠道，此限制在所有文档中一致，无矛盾。
- **组件调用风险**：
  - **禁止嵌套调用**（A→B→A）：导致无限循环，功能不可用；
  - **慎用多级调用**（A→B→C）：受最长运行时间限制，易超时失败 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **权限与计费归属**：
  - 所有通过分享链接产生的模型调用费用，均由**应用创建者 UID 账号承担**；
  - UI 应用开发环境免费但链接 24 小时失效；生产环境需订阅团队版及以上套餐并配置自定义域名 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
- **参数传参差异**：
  > **注意**：文档 1 与文档 2 对“模型识别”传参方式在工作流中的行为描述存在**关键差异**。文档 1 仅说明“在工作流中引用该组件时，即使参数的传参方式设置为模型识别，应用也不会自动推断参数值……必须从上游节点明确地为该参数提供输入值”；文档 2 完全复述了该规则。二者一致，**无矛盾**，但需强调：**工作流中“模型识别”形同虚设，必须显式传参**。
- **环境一致性要求**：UI 设计器中无法选择 API Key 或智能体，大概率因业务空间不匹配 —— 此问题在文档 3 的“准备工作”和“创建UI”章节中被反复强调，属关键检查点。

## 来源文档

- [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)
- [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)
- [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)


