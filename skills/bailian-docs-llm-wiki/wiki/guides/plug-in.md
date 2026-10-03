# plug in

插件是百炼平台用于扩展大模型能力的核心机制，通过将外部工具（如 API）封装为可被大模型识别和调用的标准化单元，弥补其在实时信息获取、精确计算、代码执行、图像生成等场景下的固有局限。插件支持官方预置、三方市场及自定义开发三类来源，可集成至智能体应用、工作流应用或通过 Assistant API 直接调用。所有插件均需经服务关联角色（`AliyunServiceRoleForSFMAccessCloudAPI`）授权后方可使用，详见 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)。

## 支持的模型/功能

当前插件能力仅在以下模型上可用：
- `qwen-turbo`、`qwen-plus`、`qwen-max`（文本模型）
- `qwen-vl-plus`、`qwen-vl-max`（多模态模型）

> **注意**：文档 1 中列出的模型兼容性表格未包含 `qwen-vl-plus`，但文档 2 和控制台实际行为已确认其支持插件调用；请以控制台最新运行结果为准，该差异已在 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md) 中隐含体现。

插件按来源分为三类：
- **官方插件**：开箱即用，无需配置参数，包括 `code_interpreter`（Python 执行）、`calculator`（数学计算）、`text_to_image`（文生图）、`quark_search`（实时搜索）、`generate_qrcode`（二维码生成）、`github_search`（GitHub 搜索）等。
- **三方插件**：来自阿里云云市场，覆盖商业服务、教育、音视频等领域，需开通后使用。
- **自定义插件**：用户自主创建或从云市场导入的 API 封装，支持完整参数映射、鉴权（Header/Query）、输入输出 Schema 定义与在线调试，详见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

## 关键参数

插件调用依赖以下核心参数，尤其在自定义插件中必须显式配置：

- **工具 ID（tool_id）**：全局唯一标识符，用于 API 调用时指定目标工具（如 `calculator`）。可通过插件详情页悬浮图标复制，见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **工具路径（path）**：相对路径，拼接至插件 URL 构成完整请求地址（如 `/query`）。
- **输入参数（in-params）**：
  - `传参方式`：`大模型识别`（从用户 query 中抽取）或 `业务透传`（由外部通过 `biz_params` 或 `user_defined_params` 注入）；
  - `类型`：支持 `String`、`Number`、`Boolean`、`Object`（子属性不可为空）；
  - `参数描述`：必须填写，直接影响大模型参数提取准确率。
- **输出参数（out-params）**：定义 API 响应中需提取并传递给大模型的字段，结构应扁平化，避免深层嵌套。
- **鉴权配置**：可选 Header（如 `Authorization: Bearer <token>`）或 Query（如 `?api_key=xxx`），支持 `basic`/`bearer`/`appcode` 类型。

## 使用方式

插件可通过三种方式接入：

1. **控制台集成（推荐用于快速验证）**：
   - 在 [插件市场](https://bailian.console.aliyun.com/#/plugin-market) 授权 `AliyunServiceRoleForSFMAccessCloudAPI` 角色（主账号直接授权；RAM 子账号需主账号预先授予 `ram:CreateServiceLinkedRole` 权限，详见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)）；
   - 官方/三方插件：单击“添加至智能体”，选择目标智能体应用（注意：官方插件仅支持同业务空间内关联）；
   - 自定义插件：需先发布为 MCP 服务，再在智能体编排页的 **MCP 区块** 中添加。

2. **工作流应用节点**：
   - 将插件作为独立节点拖入画布，手动编排执行顺序，不依赖大模型自动规划（区别于智能体模式）。

3. **API 调用**：
   - **Assistant API**：在 `tools` 字段中声明工具列表，模型自动决策是否调用（参考 [Assistant API 文档](https://help.aliyun.com/zh/model-studio/quick-start-of-assistant-api)）；
   - **DashScope SDK / HTTP 接口**：对含 `业务透传` 参数或启用用户级鉴权的插件，需通过 `biz_params` 传入对应值（详见 [应用的参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)）。

## 限制和注意事项

- **权限限制**：RAM 用户首次访问插件市场前，必须由主账号授予 `ram:CreateServiceLinkedRole` 权限，否则授权失败（错误码 140052），该要求在 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md) 和 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md) 中均明确说明。
- **功能限制**：
  - `code_interpreter` 不支持网络访问、本地文件上传，依赖库版本固定（如 `requests~=2.31.0`, `pandas`, `matplotlib` 等）；
  - `quark_search` 和 `github_search` 仅返回网页/项目标题、摘要、链接，**不支持访问原始网页内容或 GitHub 仓库详情页**；
  - 单个智能体应用最多关联 **10 个工具**。
- **配置强制项**：自定义插件发布前，所有输入/输出参数的 `参数描述` 必须非空（错误码 `130040`），且 `Object` 类型参数的子属性不可为空（错误码 `130022`）；
- **计费说明**：官方插件中 `text_to_image` 和 `quark_search` 为“限时免费，需申请开通”；其余官方及三方插件按实际开通套餐计费；自定义插件调用产生的云资源费用由用户自行承担。

## 来源文档

- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)


