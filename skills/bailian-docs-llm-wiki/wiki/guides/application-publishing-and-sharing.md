# application publishing and sharing

百炼平台支持将已发布的智能体应用（Agent 1.0）和工作流应用以多种方式对外发布与共享，包括 UI 网页应用、钉钉/微信机器人、可复用组件、音视频实时互动等形态，便于集成至业务系统或直接面向终端用户交付。所有发布行为均需基于已成功发布的应用，并严格遵循版本兼容性与权限隔离要求。注意：Agent 2.0 应用仅支持 API 调用，不支持本节所述任何 UI 或渠道类发布能力。

## 支持的模型/功能

- **适用应用类型**：仅限 **Agent 1.0 智能体应用** 和 **工作流应用**；Agent 2.0 应用不支持魔笔分享、钉钉/微信发布、UI 设计器集成及音视频互动等渠道发布能力 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **核心发布形态**：
  - **UI 应用**：通过魔笔低代码平台生成网页界面，支持拖放式编辑、数据库/文件集成及 OIDC/OAuth 2.0 登录 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
  - **IM 渠道机器人**：支持钉钉、微信公众号两种机器人形态，需配置 API Key、Client ID/Secret 及消息模板 ID。
  - **模块化组件**：将智能体或工作流发布为可被其他智能体/工作流引用的组件，支持 `query` 和 `imageList` 系统参数及自定义输入 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。
  - **音视频实时互动**：仅支持图文类应用（智能体/工作流），提供 H5/APP 扫码体验与 SDK 集成两种接入方式。

> **注意**：文档 1 中称“音视频实时互动仅支持百炼的图文对话类应用（含智能体应用和工作流应用）”，而文档 3 的实践示例中明确包含图像理解模型（如 Amap Maps + QuickChart）的调用，且文档 3 提到 `imageList` 参数在图像与视频理解模型下有效。这表明音视频互动通道实际支持多模态输入，但文档 1 表述存在局限，应以文档 3 的组件能力说明为准。

## 关键参数

| 参数 | 说明 | 使用场景 | 来源约束 |
|------|------|----------|----------|
| `API Key` | 用于身份认证与计费归属，必须与目标应用、UI 设计器处于同一业务空间 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md) | 所有发布渠道（UI、钉钉、微信、音视频）均需显式选择 | 必须提前创建并授权；未选时需跳转至“管理 API Key”页面创建 |
| `query`（系统参数） | 字符串类型，必填，承载用户原始文本输入 | 组件接入智能体（模型识别/业务透传）或工作流（仅业务透传） | 预设不可删除；别名可自定义（如 `userQuery`） |
| `imageList`（系统参数） | `Array<String>` 类型，非必填，承载图像公网 URL 列表 | 仅当组件底层使用视觉模型时生效 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md) | 需显式设置“是否可见”为 `否` 以隐藏文本模型场景下的冗余参数 |
| `biz_param` | API 调用时传入的业务参数对象，用于覆盖组件中“业务透传”类参数 | 智能体测试或生产 API 调用时手动注入入参 | 仅对“业务透传”参数生效，不作用于“模型识别”参数 |

## 使用方式

1. **前置条件**：确保目标应用已完成发布（非仅保存），且所属业务空间与所用 API Key 一致。
2. **入口统一**：全部操作均从应用详情页的 **发布渠道** 页签进入（UI 应用、钉钉、微信、组件）或 **AI 实时互动** 页签（音视频）。
3. **典型流程**：
   - **UI 应用**：选择“UI 应用” → 创建 → 编辑（拖放组件/配置路由）→ 发布至开发环境（24 小时有效期）或生产环境（需订阅套餐）[UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
   - **钉钉/微信**：授权计算巢 AppFlow（SLR + API Key 加密传输）→ 配置平台凭证（Client ID/Secret、模板 ID、AppID）→ 获取回调地址/二维码 → 在对应平台完成机器人配置与发布。
   - **组件**：在“组件”卡片点击“创建” → 填写名称/描述 → 配置参数（别名、是否必填、是否可见、传参方式）→ 发布 → 在其他智能体（技能区）或工作流（组件节点）中引用。
   - **音视频互动**：选择“语音/视频互动” → 配置 API Key → 生成临时体验二维码（24 小时）→ 正式发布后开通智能媒体服务并完成 SLR 授权 → 选择 H5/APP 分享或 SDK 集成。

## 限制和注意事项

- **版本限制**：Agent 2.0 应用完全不支持除 API 调用外的任何发布渠道，该限制为硬性约束 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **嵌套与调用深度**：禁止组件 A 调用 B、B 再调用 A 的循环依赖；多级调用（A→B→C）易触发超时，建议控制在两级以内 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。
- **环境与计费**：
  - UI 开发环境链接 24 小时失效，生产环境需订阅付费套餐并绑定域名；
  - 所有通过分享链接产生的模型调用费用，均由应用创建者 UID 账号承担；
  - 文件存储（1GB 免费）与数据库（0.3GB 免费）超出配额后按量计费。
- **权限范围**：默认分享链接仅限阿里云用户访问；如需匿名访问，须在 UI 设计器中显式开启“允许匿名访问”并配置权限组 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
- **参数传参差异**：“模型识别”传参方式在智能体中由大模型自动填充，在工作流中**无效**——必须通过上游节点显式传入值，此为关键行为差异，不可忽略。

## 来源文档

- [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)
- [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)
- [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)


