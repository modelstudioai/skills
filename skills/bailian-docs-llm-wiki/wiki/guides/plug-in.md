# plug in

[插件](../concepts/plugin.md)是百炼平台用于扩展大模型能力的核心机制，通过将外部工具（如 API）封装为可被大模型识别和调用的标准化单元，弥补其在实时信息获取、精确计算、代码执行、图像生成等场景下的固有局限。[插件](../concepts/plugin.md)支持官方预置、三方市场及自定义开发三类来源，可集成至智能体应用、工作流应用或通过 Assistant API 直接调用。所有[插件](../concepts/plugin.md)均需经服务关联角色（`AliyunServiceRoleForSFMAccessCloudAPI`）授权后方可使用，详见 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)。

## 支持的模型/功能

当前插件能力仅在以下模型上可用：
- `qwen-turbo`、`qwen-plus`、`qwen-max`（文本模型）
- `qwen-vl-max`、`qwen-vl-plus`（多模态模型）

> **注意**：文档 1 中列出的模型兼容性表格未包含 `qwen-vl-turbo` 和 `qwen2` 系列，而控制台实际已支持部分 `qwen2` 模型调用插件。最新兼容状态请以控制台执行结果为准，避免依赖过时列表。

插件按来源分为三类，功能边界明确：
- **官方插件**：开箱即用，无需配置参数，涵盖 `code_interpreter`（Python 执行）、`calculator`（数学计算）、`text_to_image`（文生图）、`quark_search`（实时搜索）、`generate_qrcode`（二维码生成）、`github_search`（GitHub 项目检索）等。详细说明见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **三方插件**：来自阿里云云市场，覆盖商业服务、教育、音视频等领域，需开通后使用，不需额外配置。
- **自定义插件**：支持用户通过定义插件 URL、工具路径、输入/输出参数及鉴权方式，将自有 API 封装为插件。完整流程参见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

## 关键参数

插件调用依赖以下核心参数，尤其在自定义插件和 API 集成中必须准确配置：

- **工具 ID（tool_id）**：全局唯一标识符，用于在请求中指定目标工具（如 `calculator`）。可通过插件详情页悬浮图标复制，见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **输入参数（input parameters）**：
  - `传参方式`：必须明确设为 `大模型识别`（由 LLM 从用户输入中抽取）或 `业务透传`（由外部系统注入，需通过 `biz_params` 或 `user_defined_params` 传递）。
  - `参数名称` 与 `参数描述`：需语义清晰，直接影响 LLM 参数提取准确率；Object 类型子属性不可为空。
- **输出参数（output parameters）**：定义 API 响应中哪些字段将被 LLM 提取并用于生成最终回答，所有字段均为必填。
- **鉴权配置**（自定义插件）：
  - 支持 `Header` 或 `Query` 位置；
  - `Type` 可选 `basic`/`bearer`/`appcode`，决定 [Token](../concepts/token.md) 前缀；
  - `Token` 为服务级鉴权凭据，用户级鉴权需在对话前通过控制台 UI 或 `biz_params` 注入。

## 使用方式

插件可通过三种方式接入：

1. **控制台集成（推荐用于快速验证）**：
   - 在 [插件市场](https://bailian.console.aliyun.com/#/plugin-market) 授权 `AliyunServiceRoleForSFMAccessCloudAPI` 角色（主账号直接授权；RAM 子账号需主账号预先授予 `ram:CreateServiceLinkedRole` 权限），见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
   - 官方/三方插件：在插件详情页单击 **添加至智能体**，选择目标智能体应用（注意：官方插件仅支持同业务空间内关联）。
   - 自定义插件：需先发布为 MCP 服务，再在智能体编排页的 **MCP 区块** 中添加。

2. **工作流应用**：
   - 将插件作为独立节点拖入画布，显式编排执行顺序，不依赖 LLM 自主决策。具体操作见 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)。

3. **API 调用**：
   - **Assistant API**：在请求 `tools` 字段中声明工具列表，模型自动规划调用；参考 [Assistant API 文档](https://help.aliyun.com/zh/model-studio/quick-start-of-assistant-api)。
   - **DashScope SDK / HTTP 接口**：对含 `业务透传` 或 `用户级鉴权` 的插件，必须通过 `biz_params` 传入对应参数，详见 [应用的参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)。

## 限制和注意事项

- **权限限制**：RAM 用户首次访问插件市场或导入云市场插件时，必须由主账号授予 `ram:CreateServiceLinkedRole` 权限，否则触发错误码 `140052`；该要求在 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md) 和 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md) 中均被强调。
- **功能限制**：
  - `code_interpreter` 插件禁止网络访问与本地文件上传，仅支持预装依赖（如 `pandas`, `matplotlib`, `requests` 等）；
  - `quark_search` 和 `github_search` 仅返回网页/项目标题、摘要、链接，**不支持访问原始网页内容或 GitHub 仓库详情页**；
  - 单个智能体应用最多绑定 10 个工具。
- **调试与发布**：自定义插件的工具必须完成 **在线测试成功 → 保存草稿 → 发布** 全流程，未发布的工具无法被调用；发布失败常见原因为参数描述缺失（错误码 `130040`）或 GET 请求误配 Object 类型入参（错误码 `130022`），详见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。
- **计费说明**：官方插件中 `text_to_image` 和 `quark_search` 为限时免费且需单独申请开通；其余官方及三方插件按实际调用量计费，详情以控制台报价为准。

## 来源文档

- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)


