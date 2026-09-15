# plug in

插件是百炼平台用于扩展大模型能力的核心机制，通过将外部工具（如 API）封装为可被大模型识别和调用的标准化单元，解决模型在实时信息获取、精确计算、代码执行、图像生成等场景下的固有局限。插件支持官方预置、三方市场及用户自定义三种来源，可在智能体应用、工作流应用及 Assistant API 中统一接入与调度。其本质是将任务规划权部分交由大模型，由其根据输入内容、工具描述和参数定义自主决策是否调用及如何构造请求。

## 支持的模型/功能

百炼当前支持在以下模型上启用插件能力：`qwen-turbo`、`qwen-plus`、`qwen-max`、`qwen-vl-max` 和 `qwen-vl-plus`。各模型对插件的兼容性可能存在差异，**实际可用性请以控制台运行结果为准**，不建议依赖文档静态列表做兼容性断言 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)。

插件按来源分为三类：
- **官方插件**：开箱即用，无需配置参数，包括 `code_interpreter`（Python 代码执行）、`calculator`（复杂数学计算）、`text_to_image`（文生图）、`quark_search`（实时网络搜索）、`generate_qrcode`（URL 转二维码）、`github_search`（GitHub 项目检索）等 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **三方插件**：来自云市场，覆盖商业服务、图像视频、教育等领域，开通后即可调用，无需额外配置。
- **自定义插件**：用户通过定义插件 URL、添加工具路径（如 `/query`）、配置输入/输出参数（支持 `application/json` 或 `application/x-www-form-urlencoded`）实现私有 API 集成 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

> **注意**：文档 1 与文档 3 均列出 `quark_search` 插件说明，但文档 1 称其“不支持直接访问网页详情”，文档 3 补充说明“支持检索出网页标题、关键词和摘要”——二者一致，无矛盾；但文档 3 新增了 `github_search` 的同类限制说明（“不支持访问项目详情”），该细节在文档 1 中缺失，应以文档 3 为准。

## 关键参数

插件调用依赖两类关键参数：

- **工具 ID**：全局唯一标识符（如 `calculator`），用于在 API 请求或工作流节点中指定目标工具。可通过插件详情页悬浮工具名称图标复制 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **输入参数**：
  - `传参方式` 决定参数值来源：`大模型识别`（从用户 Query 中抽取）、`业务透传`（由外部通过 `biz_params` 或 `user_defined_params` 显式传入）；
  - `类型` 支持 `String`、`Number`、`Object` 等，其中 `Object` 类型子属性**不能为空**，需手动展开配置；
  - `传入方法` 指定位置：`Body`（JSON 主体）、`Query`（URL 参数）或 `Header`（请求头）。
- **输出参数**：必须明确定义返回字段名、类型及描述，大模型据此从 API 响应中提取并结构化输出。嵌套层级应尽量扁平。

鉴权参数仅在自定义插件中配置：
- 支持 `Header` 或 `Query` 位置；
- `Type` 可选 `basic`、`bearer`、`appcode`，决定 Token 前缀（如 `Bearer <TOKEN>`）；
- `Token` 为服务级鉴权凭据，`用户级鉴权` 需在对话前通过控制台配置界面动态传入。

## 使用方式

插件可通过三种方式集成：

1. **控制台智能体应用**：
   - 官方/三方插件：在[插件市场](https://bailian.console.aliyun.com/#/plugin-market)页面单击“添加至智能体”，选择工具与目标应用；
   - 自定义插件：需先发布为 MCP 服务，再在智能体编排页的 **MCP 区块** 中添加 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)；
   - **注意**：官方插件仅支持与**同业务空间**内的智能体关联；子业务空间首次使用需单独授权 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。

2. **工作流应用**：将插件作为独立节点拖入画布，手动编排执行顺序，不依赖大模型自动规划 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)。

3. **API 调用**：
   - Assistant API：在 `tools` 字段中声明工具 ID 及描述，由 SDK 自动处理调用循环；
   - DashScope SDK / HTTP 接口：需在请求中显式传递 `tool_choice` 和 `tools`，业务透传参数通过 `biz_params` 传入 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

## 限制和注意事项

- **数量限制**：单个智能体应用最多关联 10 个工具 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **参数约束**：
  - GET 请求**不支持 Object 类型输入参数**，否则发布失败（错误码 `130022`）；
  - 所有输入/输出参数**必须填写参数描述**，缺失将导致发布失败（错误码 `130040`）；
  - 工具名称长度上限为 20 字符，超限需截断。
- **安全与权限**：
  - RAM 子账号使用插件（含云市场导入）前，主账号须授予 `ram:CreateServiceLinkedRole` 权限，策略条件需匹配 `cloundapi-access.sfm.aliyuncs.com` [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)；
  - 删除插件或工具为**不可逆操作**，将导致已关联应用失效。
- **功能边界**：
  - `code_interpreter` 插件**禁止网络访问与本地文件上传**，仅限沙箱内执行，依赖库版本固定（如 `requests~=2.31.0`, `pandas` 等）；
  - `quark_search` 与 `github_search` 均仅返回摘要信息，**无法获取原始网页或仓库完整内容**；
  - 多插件组合调用（如搜索+绘图+生成二维码）需确保各工具输出格式能被下游正确解析，无隐式数据格式转换保障。

## 来源文档

- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)
- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)


