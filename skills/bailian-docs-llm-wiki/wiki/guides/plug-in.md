# plug in

插件是百炼平台用于扩展大模型能力的核心机制，通过将外部工具（如 API）封装为可被大模型识别和调用的标准化单元，解决模型在实时信息获取、精确计算、代码执行、图像生成等场景下的固有局限。插件支持官方预置、三方市场及自定义开发三种来源，可集成至智能体应用、工作流应用或通过 Assistant API 直接调用。其设计目标是让开发者以最小认知成本实现能力增强，而非替代模型本身。

## 支持的模型/功能

当前插件能力仅在以下模型上可用：`qwen-turbo`、`qwen-plus`、`qwen-max`、`qwen-vl-max`、`qwen-vl-plus`。各模型对插件的兼容性存在差异，实际调用效果应以控制台运行结果为准，[选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 文档提供了各模型的详细规格说明。

插件按来源分为三类：
- **官方插件**：组件广场预置，开箱即用，无需配置参数。包括 `code_interpreter`（Python 代码执行）、`calculator`（复杂数学计算）、`text_to_image`（文生图）、`quark_search`（实时网络搜索）、`generate_qrcode`（URL 转二维码）、`github_search`（GitHub 项目检索）等。具体能力与计费状态详见 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)。
- **三方插件**：来自阿里云云市场，覆盖商业服务、图像视频、教育等领域，需开通后使用。开通流程与权限要求见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **自定义插件**：支持开发者基于自有 API 创建，支持鉴权（Header/Query）、多工具路径、JSON/Object 参数定义，并可通过 MCP 服务方式接入智能体。完整创建与调试流程请参考 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

> **注意**：文档 1 和文档 2 均列出 `quark_search` 插件，但文档 2 明确指出“夸克搜索和联网搜索（`enable_search`）有什么区别？”，并强调二者并非同一机制；而文档 1 未提及 `enable_search`。因此，`enable_search` 是独立于插件系统的模型级开关，不可与 `quark_search` 插件混用或等同理解。

## 关键参数

插件调用依赖以下关键参数，尤其在自定义插件和 API 集成中必须准确配置：

- **工具 ID（tool_id）**：唯一标识一个工具，如 `calculator`、`text_to_image`。调用时必须显式传入，获取方式见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md) 和 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。
- **输入参数（input parameters）**：
  - `传参方式`：分为 `大模型识别`（从用户 query 中抽取）和 `业务透传`（由外部系统传入，需通过 `biz_params` 或 `user_defined_params` 指定）；
  - `类型`：支持 `String`、`Number`、`Boolean`、`Object`（子属性不能为空）；
  - `参数描述`：必须填写，直接影响大模型参数提取准确性。
- **输出参数（output parameters）**：所有字段必填，用于指导大模型解析 API 响应并构造最终回复。嵌套层级应尽量扁平。
- **高级配置（可选）**：提供 `Value` 字段填写调用示例（如 `{"city": "杭州", "date": "2025-04-25"}`），显著提升复杂参数场景下的召回率与准确率。

## 使用方式

插件可通过三种方式接入应用：

1. **控制台集成（推荐用于快速验证）**：
   - 在 [插件市场](https://bailian.console.aliyun.com/#/plugin-market) 页面，为插件授权（主账号或 RAM 用户需提前配置 `AliyunServiceRoleForSFMAccessCloudAPI` 角色，详见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)）；
   - 官方/三方插件：单击“添加至智能体”，选择目标智能体应用即可；
   - 自定义插件：需先发布为 MCP 服务，再在智能体编排页的 **MCP 区块** 中添加。

2. **工作流应用节点**：
   - 将插件作为独立节点拖入工作流画布，按需配置输入/输出映射，不依赖大模型自主决策，适用于确定性任务编排。

3. **API 调用**：
   - **Assistant API**：在请求体 `tools` 字段中声明工具列表，模型自动规划调用逻辑；
   - **DashScope SDK / HTTP 接口**：需在 `tools` 中传入 `tool_id` 及必要参数；若含 `业务透传` 或 `用户级鉴权`，须通过 `biz_params` 传递对应值（详见 [工作流与旧版智能体应用 API 应用 DashScope API 参考](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)）。

## 限制和注意事项

- **权限限制**：RAM 用户首次访问插件市场前，必须由主账号授予 `ram:CreateServiceLinkedRole` 权限（策略条件中 `ram:ServiceName` 必须为 `cloundapi-access.sfm.aliyuncs.com`），否则无法完成 SLR 授权，该要求在 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md) 和 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md) 中均被强调。
- **功能限制**：
  - `code_interpreter` 不支持网络访问与本地文件上传，依赖库版本固定（如 `requests~=2.31.0`、`pandas` 等），详见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)；
  - `quark_search` 和 `github_search` 仅返回网页/项目标题、摘要、链接，**不支持访问原始网页内容或 GitHub 仓库详情页**；
  - 自定义插件中，GET 请求**不支持 Object 类型输入参数**（错误码 `130022`），需改用 POST。
- **发布与调试**：所有自定义工具必须经“测试工具”成功运行后，再执行“发布”操作；草稿状态工具不可被调用。删除插件或工具将导致已关联的应用失效，且操作不可逆。
- **计费提示**：`text_to_image` 与 `quark_search` 为“限时免费，需申请开通”，其余官方插件当前免费；三方插件按所选套餐计费。

## 来源文档

- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)


