# application publishing and sharing

百炼平台支持将智能体（Agent 1.0）和工作流应用以多种形态发布与共享，包括作为可复用组件接入其他AI应用、生成网页UI界面、集成至钉钉/微信等企业通讯平台，以及通过音视频实时互动渠道部署。所有发布行为均基于已创建并发布的应用，且需注意版本兼容性与运行时约束。

## 支持的模型/功能

- **支持的应用类型**：仅 [智能体应用（Agent 1.0）](raw/application-user-guide/llm-application/single-agent-application.md) 支持全部发布渠道（魔笔UI、钉钉、微信、组件、音视频互动）；[Agent 2.0](raw/application-user-guide/llm-application/agent2-introduction.md) 仅支持 API 调用，**不支持**任何 UI 或第三方平台分享渠道（见 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)）。
- **组件能力**：智能体或工作流应用均可发布为组件，供其他智能体（作为工具）或工作流（作为节点）调用。组件支持预设系统参数 `query`（String，必填）和 `imageList`（Array<String>，非必填），并可通过别名、描述、传参方式（业务透传 / 模型识别）进行标准化配置。
- **UI 集成能力**：通过 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)，可将智能体或工作流应用封装为低代码网页应用，支持拖放式界面搭建、数据库映射、权限控制及一键发布至开发/生产环境。

## 关键参数

| 参数名 | 类型 | 是否必填 | 说明 | 传参方式约束 |
|--------|------|----------|------|--------------|
| `query` | String | 是 | 用户输入的自然语言指令，如“查询杭州天气” | 支持“业务透传”（由调用方显式传入）和“模型识别”（仅在智能体中由大模型自动填充） |
| `imageList` | Array<String> | 否 | 图像公网 URL 列表，仅当组件使用视觉模型时生效 | 必须设为“不可见”或隐藏，若组件未启用图像理解能力（见 [图像与视频理解](../../raw/model-user-guide/model-experience/vision-model/vision.md)） |
| `biz_param` | Object | 否（API 场景） | API 调用时传递业务参数的顶层字段，用于承载 `query` 等入参 | 仅适用于 API 调用场景，UI/组件节点内无需此结构 |

> **注意**：工作流中引用组件时，即使参数配置为“模型识别”，系统**不会自动推断值**，必须通过上游节点显式传入（如 `系统变量/query`），该限制在 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md) 和 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md) 中均明确强调，无矛盾。

## 使用方式

1. **发布为组件**  
   - 在应用编辑页点击「发布应用」→ 勾选「发布应用组件」→ 进入组件配置页设置名称、描述、参数别名与传参方式；  
   - 或通过 [组件管理](https://bailian.console.aliyun.com/?tab=app#/component-manage) 页面，对已发布应用单独创建组件。

2. **接入组件**  
   - **智能体中**：在「技能」列表选择组件，大模型根据组件描述与上下文自动触发调用；含 `biz_param` 的参数需在 API 请求中传入。  
   - **工作流中**：拖入「组件节点」→ 选择目标组件 → 在「输入」配置中绑定上游变量（如 `系统变量/query`）→ 将 `组件1/result` 传递至下游节点。

3. **发布为 UI 应用**  
   - 从应用发布页选择「UI应用」→ 自动填充基础信息（API Key、智能体、图标等）→ 编辑界面后发布至开发环境（24小时有效）或生产环境（需订阅套餐）；  
   - 或直接进入 [UI设计器](https://bailian.console.aliyun.com/?tab=app#/app-ui) 创建新 UI，选择模板（如企业AI知识库Lite）、绑定百炼应用与 API Key 后发布。

4. **第三方平台集成**  
   - **钉钉/微信**：需先授权计算巢 AppFlow，配置 API Key、Client ID/Secret 及消息模板 ID（钉钉）或 AppID（微信），获取回调地址或二维码后分发；  
   - **音视频互动**：在「AI实时互动」页签配置 API Key，生成临时体验二维码或发布为 H5/APP/SDK 集成方案。

## 限制和注意事项

- **版本限制**：Agent 2.0 应用不支持除 API 外的任何发布渠道，该信息在 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md) 中明确声明，开发者须确认所用应用版本。
- **调用深度限制**：避免嵌套调用（A→B→A）或多级调用（A→B→C），否则易触发超时或循环调用错误（见 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md) 和 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)）。
- **环境隔离**：UI 设计器、API Key、智能体/工作流应用必须归属同一[业务空间](https://help.aliyun.com/zh/model-studio/use-workspace)，否则无法关联（见 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)）。
- **开发环境时效性**：UI 应用发布至开发环境后**24 小时失效**，需重新发布才能继续访问；生产环境需订阅付费套餐并配置自定义域名（见 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)）。
- **文件参数处理**：工作流应用若含文件类自定义参数，在 UI 设计器中需手动配置变量映射（如 `{{{file_name:files[0]}}}`），否则无法正确读取用户上传文件（见 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)）。

## 来源文档

- [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)
- [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)
- [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)


