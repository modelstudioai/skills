# application publishing and sharing

百炼平台支持将已构建的智能体应用（Agent 1.0）、工作流应用及 UI 应用以多种方式发布与共享，覆盖终端用户触达（如微信、钉钉、H5）、能力复用（组件化）、实时音视频交互等场景。所有发布行为均需基于已发布的应用，并受 Agent 版本、业务空间隔离、权限与计费策略约束。开发者应根据目标集成方式选择对应路径，并严格遵循参数配置与调用限制。

## 支持的模型/功能

- **适用应用类型**：  
  - `Agent 1.0` 智能体应用：完整支持魔笔 UI、钉钉、微信、组件、音视频实时互动五类发布渠道；  
  - `Agent 2.0` 智能体应用：**仅支持 API 调用**，不支持任何 UI 或渠道类分享方式（见[分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)）；  
  - 工作流应用：支持发布为组件、接入 UI 设计器、音视频实时互动（图文类），但**不支持钉钉/微信机器人渠道**（文档未明确支持，且钉钉/微信配置流程仅指向智能体应用）；  
  - UI 应用：基于魔笔低代码平台构建，可集成智能体或工作流作为后端能力，支持开发/生产环境部署。

- **核心能力矩阵**：
  | 发布方式             | 支持应用类型                     | 关键能力说明                                                                 |
  |----------------------|----------------------------------|----------------------------------------------------------------------------|
  | 魔笔 UI 应用         | Agent 1.0、工作流                | 可视化拖拽搭建 H5/PC 界面，绑定 API Key 与应用，支持匿名访问与权限组控制（见[UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)） |
  | 钉钉/微信机器人      | Agent 1.0 专属                   | 需授权 AppFlow SLR、配置钉钉 Client ID/Secret/模板 ID 或微信 AppID，回调地址由百炼生成 |
  | 组件（Reusable Component） | Agent 1.0、工作流（二者均可发布） | 作为模块化能力被其他智能体或工作流引用；预设 `query` 和 `imageList` 系统参数（见[使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)） |
  | 音视频实时互动       | Agent 1.0、工作流（图文类）       | 生成临时体验二维码（24h 有效）或长期 H5/APP 分享链接；支持 SDK 集成（WEB/IOS/Android） |

> **注意**：文档 1 明确限定钉钉/微信发布仅适用于 Agent 1.0；而文档 3 中 UI 设计器明确支持工作流应用接入。但文档 1 的“通过钉钉发布应用”章节全程以智能体应用为操作对象，未提及工作流适配——若需在工作流中复用钉钉能力，必须通过组件封装后间接集成，而非直接发布。

## 关键参数

所有发布方式均依赖以下基础参数，且需确保**同一业务空间内一致**：

- `API Key`：用于身份认证与计费归属，必须与目标应用同属一个业务空间（见[UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)）；
- `应用标识`：Agent 1.0 或工作流应用须已**发布成功**，方可被 UI、组件、音视频等渠道引用；
- `系统参数（组件专用）`：
  - `query`（String，必填）：承载用户自然语言输入，如 `"查询杭州天气"`；
  - `imageList`（Array<String>，非必填）：图像公网 URL 列表，仅当组件内部使用多模态模型时生效；
- `渠道特有参数`：
  - 钉钉：`Client ID`、`Client Secret`、`卡片模板 ID`（需在钉钉开放平台申请并授予权限 `Card.Streaming.Write`/`Card.Instance.Write`）；
  - 微信：`AppID`（开发者 ID），需在微信公众号后台获取；
  - UI 应用：`数据库表映射名`（如 `kb_chat_list`），结构必须与模板严格一致，否则运行时报错。

## 使用方式

1. **统一入口**：进入百炼控制台 → [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) → 打开目标应用 → 切换至对应页签（`发布渠道` / `AI实时互动` / `UI应用`）。

2. **分场景操作**：
   - **UI 应用**：在 `UI应用` 页签点击 `创建` → 自动填充或手动配置 API Key、智能体/工作流、图标等 → `立即创建` → 进入 UI 设计器编辑 → 右上角 `发布` 至开发/生产环境（见[UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)）；
   - **组件**：在 `发布渠道` 页签 → `组件` 区域点击 `+ 创建` → 填写组件名称、描述、配置 `query`/`imageList` 等参数的别名、可见性、传参方式（`业务透传` 或 `模型识别`）→ `确定发布`；
   - **钉钉/微信**：在 `发布平台` 页签 → 对应卡片点击 `创建` → 授权 AppFlow → 选择 API Key → 输入渠道凭证 → 完成后复制回调地址（钉钉）或扫码二维码（微信）；
   - **音视频实时互动**：在 `AI实时互动` 页签 → 点击 `语音互动/视频互动` → `去配置` → 选择 API Key → `发布` → 开通智能媒体服务并完成 SLR 授权 → 生成分享链接或集成 SDK。

3. **组件接入**：
   - 智能体中：在技能配置中选择已发布组件，大模型根据组件描述与上下文自动触发调用；
   - 工作流中：拖入 `组件节点` → 选择组件 → 手动连接上游节点输出至 `query` 等参数（即使设为 `模型识别`，工作流也**不自动推断**，必须显式传参）。

## 限制和注意事项

- **Agent 版本硬限制**：Agent 2.0 应用完全不可用于魔笔 UI、钉钉、微信、组件、音视频等发布渠道，仅开放 API 接口（见[分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)）；
- **嵌套与多级调用禁止**：组件 A 调用 B、B 再调用 A 将导致死循环；A→B→C 多级链路易超时，应尽量扁平化设计（见[使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)）；
- **环境时效性**：
  - UI 开发环境链接有效期为 **24 小时**，需重新发布才能续期；
  - 音视频临时体验二维码有效期也为 **24 小时**；
  - 生产环境 UI 需订阅付费套餐并绑定自定义域名；
- **权限与计费**：
  - 所有分享链接访问者产生的模型调用费用，均由应用创建者 UID 账号承担；
  - UI 应用生产环境发布、文件存储（>1GB）、数据库（>0.3GB）需按量计费；
  - 钉钉/微信渠道需额外授权 AppFlow SLR 及 API-KEY 加密传输（见[分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)）；
- **参数兼容性**：工作流应用若含文件类自定义参数（如 `files`），在 UI 设计器中必须显式配置 `{{{file_name:files[0]}}}` 格式变量，否则无法读取上传文件（见[UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)）。

## 来源文档

- [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)
- [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)
- [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)


