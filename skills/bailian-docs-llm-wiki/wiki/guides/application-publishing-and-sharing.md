# application publishing and sharing

百炼平台支持将已构建的智能体应用（Agent 1.0）、工作流应用及 UI 应用以多种方式发布与共享，包括对外提供 Web 访问、集成至钉钉/微信等第三方平台、封装为可复用组件、或接入音视频实时互动场景。所有发布行为均需基于已发布的应用实例，并受制于 Agent 版本、业务空间隔离及权限模型约束。开发者应根据目标使用场景选择适配的发布路径。

## 支持的模型/功能

- **仅限 Agent 1.0**：魔笔分享渠道、钉钉机器人、微信公众号、组件发布、音视频实时互动等功能**全部仅支持 Agent 1.0 智能体应用**；Agent 2.0 应用不支持上述任何分享渠道，仅可通过 API 调用 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **UI 设计器能力**：支持将 Agent 1.0 或工作流应用一键发布为网页 UI 应用，集成魔笔低代码能力，提供拖放式界面搭建、数据库映射、多端适配（PC/H5）及权限配置 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
- **组件化复用**：智能体或工作流应用可发布为组件，供其他智能体（作为工具调用）或工作流（作为节点接入）引用，支持 `query` 和 `imageList` 等预设系统参数及自定义传参逻辑 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。

> **注意**：文档 1 明确指出“Agent 2.0 仅支持通过 API 调用，不支持上述分享渠道”，而文档 3 未提及 Agent 2.0 兼容性，但其全部操作示例均基于 Agent 1.0 工作流/智能体。因此，**组件发布与接入功能亦仅适用于 Agent 1.0**，该限制在文档 3 中未显式声明，属隐含前提。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| `API Key` | 所有发布渠道（钉钉、微信、音视频、UI）均需绑定有效的百炼 API Key | 必须与目标应用、UI 设计器处于**同一业务空间**；否则在 UI 设计器中无法选择 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md) |
| `回调地址`（钉钉） | 百炼生成的 HTTP 地址，需填入钉钉机器人配置的“消息接收地址” | 仅支持 HTTP 模式；Stream 模式会导致消息无法返回 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md) |
| `模板 ID` / `Client ID` / `Client Secret`（钉钉） | 钉钉开放平台创建应用后获取的凭证 | 需额外申请 `Card.Streaming.Write` 和 `Card.Instance.Write` 权限，否则卡片消息无法发送 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md) |
| `传参方式`（组件） | 分为 `业务透传` 与 `模型识别`：<br>- 工作流中**无论设置为何种方式，均需上游节点显式传参**；<br>- 智能体中 `模型识别` 由大模型自动填充，`业务透传` 需手动配置 `biz_param` | 文档 1 与文档 3 对工作流中 `模型识别` 的行为描述一致，确认该模式在工作流中**无效**，必须显式传参 |

## 使用方式

1. **UI 应用发布**  
   - 进入应用「发布渠道」页签 → 选择「UI 应用」→ 「创建」→ 自动填充基础信息（API Key、智能体、图标等）→ 编辑 UI（可选）→ 发布至「开发环境」（24 小时有效）或「生产环境」（需订阅套餐）→ 获取「应用地址」分享 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。

2. **第三方平台集成**  
   - **钉钉/微信**：在「发布平台」页签授权计算巢 AppFlow → 创建对应平台应用并获取凭证 → 填入百炼配置面板 → 获取回调地址（钉钉）或二维码（微信）→ 在目标平台完成机器人/公众号配置 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。  
   - **音视频实时互动**：在「AI 实时互动」页签 → 选择语音/视频 → 配置 API Key → 生成临时体验二维码（24 小时）→ 发布后开通智能媒体服务并完成 SLR 授权 → 选择 H5/APP 扫码或 SDK 集成 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。

3. **组件发布与引用**  
   - 发布：在应用「发布渠道」→ 「组件」→ 「创建」→ 填写名称、描述、参数（别名、是否可见、传参方式、默认值）→ 「确定发布」。  
   - 引用：  
     - *智能体*：创建新智能体 → 在「技能」中选择已发布组件 → 测试时若含 `业务透传` 参数，需在「入参变量配置」中手动填入或 API 调用时传 `biz_param`；  
     - *工作流*：拖入「组件」节点 → 选择组件 → 在「输入」中绑定上游变量（如 `系统变量/query`）→ 连接至下游节点 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。

## 限制和注意事项

- **Agent 版本硬限制**：所有非 API 形式的发布（UI、钉钉、微信、组件、音视频）**仅支持 Agent 1.0**，Agent 2.0 应用不可见、不可选、不可配置 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **业务空间强绑定**：API Key、目标应用、UI 设计器三者必须归属同一业务空间，否则 UI 创建时无法下拉选择资源，且发布失败 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
- **组件调用风险**：  
  - 禁止嵌套调用（A→B→A），将导致无限循环；  
  - 多级调用（A→B→C）易触发超时（因总运行时间受限），建议控制在两级以内 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md) 和 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。
- **开发环境时效性**：UI 应用发布至开发环境后链接**24 小时失效**，需重新发布；生产环境需订阅付费套餐并绑定自定义域名 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
- **权限与计费**：  
  - UI 应用默认仅阿里云用户可访问；如需匿名访问，须在 UI 设计器中开启「允许匿名访问」并配置权限组；  
  - 所有发布行为本身不额外收费，但模型调用、文件存储（1GB 免费）、数据库（0.3GB 免费）、生产环境部署均按量计费 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。

## 来源文档

- [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)
- [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)
- [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)


