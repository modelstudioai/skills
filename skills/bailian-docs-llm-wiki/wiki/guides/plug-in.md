# plug in

插件是百炼平台用于扩展大模型能力的核心机制，通过将外部工具（API）集成到推理流程中，弥补大模型在实时信息获取、精确计算、代码执行、图像生成等任务上的固有局限。插件以“工具集合”形式组织，支持官方预置、三方市场及完全自定义三种类型，可被智能体应用、工作流应用或 Assistant API 调用。其核心价值在于将确定性操作交由专业服务执行，再由大模型整合结果生成自然语言响应。

## 支持的模型/功能

百炼当前支持在以下模型上启用插件能力：`qwen-turbo`、`qwen-plus`、`qwen-max`、`qwen-vl-max` 和 `qwen-vl-plus`。各模型对插件调用的规划能力与上下文处理深度存在差异，实际兼容性请以控制台运行结果为准。详细模型能力对比见 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。

插件按来源分为三类：
- **官方插件**：组件广场预置，开箱即用，无需配置参数。包括 `code_interpreter`（Python 代码执行）、`calculator`（复杂数学计算）、`text_to_image`（文生图）、`quark_search`（实时网络搜索）、`generate_qrcode`（URL 生成二维码）、`github_search`（GitHub 项目检索）等。具体说明详见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **三方插件**：来自阿里云市场，覆盖商业服务、图像视频、教育等领域，需开通后使用。
- **自定义插件**：用户自主创建或从云市场导入的 API 封装，支持完整鉴权、参数映射与调试。完整流程见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

> **注意**：文档 1 中称“夸克搜索插件目前支持检索网页标题、关键词和摘要，但不支持直接访问网页详情”，而文档 2 在“常见问题”部分明确指出“夸克搜索和联网搜索（enable_search）有什么区别？——开启夸克搜索插件时，模型将直接调用插件执行搜索，并将搜索结果以文本形式返回”，二者描述角度一致（均强调返回摘要而非全文），无实质矛盾；但文档 2 补充了关键对比项，更具实操参考价值。

## 关键参数

插件调用依赖两类关键参数：
- **工具 ID**：唯一标识一个工具，如 `calculator`、`text_to_image`。必须在 API 请求或应用配置中准确传递。获取方式见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md) 的“获取工具ID”章节。
- **输入/输出参数**（仅自定义插件需显式配置）：
  - 输入参数需指定名称、类型（String/Number/Object 等）、传参方式（`大模型识别` 或 `业务透传`）、是否必填；
  - 输出参数需明确定义字段名与类型，大模型据此解析 API 响应并构造最终回答；
  - Object 类型参数的子属性**不能为空**，否则发布失败（错误码 130022）；
  - GET 请求下**不支持 Object 类型输入参数**（错误码 130022）。

## 使用方式

插件可通过三种方式接入：
1. **控制台集成**：
   - 官方/三方插件：在 [插件市场](https://bailian.console.aliyun.com/#/plugin-market) 页面单击“添加至智能体”，选择目标智能体应用即可关联（最多支持 10 个工具）；
   - 自定义插件：需先发布为 MCP 服务，再在智能体编排页面的 **MCP 区块** 中添加；
2. **工作流应用**：将插件作为独立节点拖入画布，按需编排执行顺序，不依赖大模型自动规划；
3. **API 调用**：
   - Assistant API：在 `tools` 字段中声明工具列表，请求时由模型自主决策调用；
   - DashScope SDK / HTTP 接口：通过 `biz_params` 传递业务透传参数或用户级鉴权 [Token](../concepts/token.md)（见 [应用的参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)）。

## 限制和注意事项

- **权限要求**：首次使用插件需授权服务关联角色 `AliyunServiceRoleForSFMAccessCloudAPI`。主账号可直接授权；RAM 子账号需主账号预先授予 `ram:CreateServiceLinkedRole` 权限（策略脚本见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)）。
- **功能限制**：
  - `code_interpreter` 插件**不支持网络访问**及**本地文件上传**，可用依赖版本已固化（见文档 2）；
  - `quark_search` 和 `github_search` 均仅返回摘要信息，**不支持访问原始网页或仓库详情页**；
  - 自定义插件中，GET 请求方法下输入参数**禁止使用 Object 类型**；
- **发布约束**：
  - 工具名称长度上限为 20 字符（超长将导致发布失败）；
  - 删除插件或工具将导致所有关联应用失效，且**不可撤回**；
- **计费提示**：`text_to_image` 与 `quark_search` 为“限时免费，需申请开通”，其余官方插件默认免费；三方插件按所选套餐计费。

## 来源文档

- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)


