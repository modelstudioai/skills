# application publishing and sharing

百炼平台支持将智能体（Agent 1.0）和工作流应用以多种方式发布与共享，包括作为可复用组件接入其他AI应用、封装为网页UI应用、集成至钉钉/微信等第三方平台，以及通过音视频实时互动渠道部署。所有发布行为均需在统一业务空间内完成，且依赖已发布的应用及有效的API Key。核心能力围绕模块化复用、低代码界面构建和跨平台分发展开。

## 支持的模型/功能

- **组件化能力**：智能体或工作流应用可发布为标准化组件，供其他智能体或工作流调用，实现功能复用。组件支持预设系统参数（如 `query`、`imageList`），并兼容文本与多模态模型（如[图像与视频理解](raw/model-user-guide/model-experience/vision-model/vision.md)）。
- **UI应用构建**：通过[UI设计器](raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)，可拖放式搭建网页界面，并集成百炼智能体、大模型、数据库及HTTP服务；支持PC/H5双端适配及权限管理。
- **第三方平台分发**：支持发布至钉钉机器人、微信公众号、魔笔分享渠道及音视频实时互动（H5/APP/SDK），其中钉钉与微信需配置对应平台凭证（Client ID/Secret、AppID等）。
- **版本限制**：仅 [Agent 1.0 智能体应用](raw/application-user-guide/llm-application/single-agent-application.md) 支持全部分享渠道；Agent 2.0 仅支持 API 调用，不支持 UI、钉钉、微信等前端分发方式（见[分享智能体应用](raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)）。

> **注意**：文档 3 明确指出“分享渠道（魔笔分享渠道、钉钉、微信、组件、音视频实时互动）均为 **Agent 1.0** 智能体应用的功能”，而文档 1 和文档 2 均未提及 Agent 2.0 的兼容性限制。因此，若开发者尝试对 Agent 2.0 应用使用 UI 设计器或钉钉发布，将失败——此为关键约束，非文档疏漏。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 来源上下文 |
|--------|------|------|------|------------|
| `query` | String | 是 | 用户输入的自然语言指令（如“查询杭州天气”），用于驱动组件逻辑 | [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md) 中定义为预设系统参数 |
| `imageList` | Array<String> | 否 | 图像公网地址列表，仅当组件使用视觉模型时生效 | 同上文档中明确说明其条件有效性 |
| `biz_param` | Object | 否（按需） | API 调用时传入业务透传参数的字段名，用于显式传递 `query` 等参数 | [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md) 提及测试/API 场景下需通过该字段传参 |
| API Key | String | 是 | 所有发布渠道（UI、钉钉、微信、音视频）必需的身份凭证，必须与应用同属一个业务空间 | [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md) 和 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md) 均强调此前提 |

## 使用方式

- **发布为组件**：在应用编辑页点击「发布应用」→ 勾选「发布应用组件」，或进入[组件管理](https://bailian.console.aliyun.com/?tab=app#/component-manage)单独创建；配置名称、描述、参数别名与传参方式（业务透传 / 模型识别）后发布。
- **构建UI应用**：通过[UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)选择模板（如企业AI知识库Lite）→ 绑定API Key与已发布智能体 → 拖放组件编辑界面 → 发布至开发环境（24小时有效）或生产环境（需订阅套餐）。
- **集成至钉钉/微信**：在应用「发布渠道」页签选择对应平台 → 完成授权（SLR + API Key加密传输）→ 配置平台凭证（钉钉：Client ID/Secret/卡片模板ID；微信：AppID）→ 获取回调地址或二维码分发。
- **音视频实时互动**：在「AI实时互动」页签配置 → 生成临时体验二维码（24小时）→ 发布后支持H5扫码、APP授权Token或SDK集成（含快速集成与开发集成两种模式）。

## 限制和注意事项

- **业务空间隔离**：UI设计器、API Key、智能体应用三者必须归属同一[业务空间](https://help.aliyun.com/zh/model-studio/use-workspace)，否则无法关联（见[UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)「准备工作」节）。
- **组件调用风险**：
  - 禁止嵌套调用（A→B→A），否则导致无限循环；
  - 多级调用（A→B→C）易触发最长运行时间超时（见[使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)「注意事项」）。
- **参数传参差异**：`模型识别`传参方式在智能体中由大模型自动填充，但在工作流中**完全无效**——必须通过上游节点显式传入（该规则在文档 1 和文档 3 中一致强调，属强制行为）。
- **开发环境时效性**：UI应用在开发环境发布的链接**24小时后失效**，需重新发布；生产环境长期有效但需付费订阅（见[UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)「环境对比」表）。
- **文件参数处理**：工作流应用若含文件类自定义参数，需在UI设计器中手动映射为 `{{{file_name:files[0]}}}` 格式（`file_name` 替换为实际变量名），否则UI无法正确上传（见[UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)「从已有应用发布为 UI」说明）。

## 来源文档

- [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)
- [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)
- [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)


