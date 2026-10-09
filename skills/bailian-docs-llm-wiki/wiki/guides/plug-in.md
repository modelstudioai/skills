# plug in

插件是百炼平台用于扩展大模型能力的核心机制，通过将外部工具（如 API）封装为可调用的标准化组件，弥补大模型在实时信息获取、精确计算、代码执行、图像生成等方面的固有局限。插件支持由大模型自主规划调用（Agent 模式），也可作为工作流节点显式编排，适用于智能体应用、工作流应用及 Assistant API 等多种调用路径。其设计兼顾开箱即用性与深度定制能力。

## 支持的模型/功能

百炼插件当前支持以下模型：`qwen-turbo`、`qwen-plus`、`qwen-max`、`qwen-vl-max`、`qwen-vl-plus`。各模型对插件的兼容性存在差异，**实际可用性以控制台运行结果为准**，不建议依赖文档中静态列表做兼容性断言 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)。

插件按来源分为三类：
- **官方插件**：预置于组件广场，免配置即用，包括 `code_interpreter`（Python 代码执行）、`calculator`（复杂数学计算）、`text_to_image`（文生图）、`quark_search`（实时网络搜索）、`generate_qrcode`（URL 转二维码）、`github_search`（GitHub 项目检索）等 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **三方插件**：来自云市场，覆盖商业服务、图像视频、教育等领域，需开通后使用，无需额外参数配置。
- **自定义插件**：用户自主创建并托管的 API 封装，支持完全自定义 URL、鉴权方式、输入/输出参数结构及调用逻辑 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

> **注意**：文档 1 中称“夸克搜索插件目前支持检索网页标题、关键词和摘要，但不支持直接访问网页详情”，而文档 3 的“常见问题”明确指出“夸克搜索和联网搜索（enable_search）有什么区别？——开启夸克搜索插件时，模型将直接调用插件执行搜索，并将搜索结果以文本形式返回……”，二者描述存在潜在矛盾：前者强调“不支持访问详情”，后者隐含“结果已包含足够上下文供模型生成”。实践中应以插件实际返回的 `results` 字段内容为准，而非预设限制。

## 关键参数

插件调用的核心参数由两层定义构成：

- **插件级参数**（仅自定义插件）：
  - `plugin_url`：插件根域名，如 `https://example.com`；
  - 鉴权配置：支持 `Header` 或 `Query` 位置，`Type` 可选 `basic`/`bearer`/`appcode`，`Token` 为服务级凭据；
  - 是否启用鉴权：影响请求头或 URL 构造。

- **工具级参数**（所有插件）：
  - `tool_name`：语义化名称，影响模型调用决策；
  - `tool_description`：自然语言描述，**必须包含使用示例**，直接影响模型是否准确识别调用意图；
  - `tool_path`：相对路径，拼接至 `plugin_url` 构成完整 endpoint；
  - 输入参数（`in_params`）：
    - `parameter_name`：如 `city`、`article_index`；
    - `parameter_description`：需精确说明格式（如 `yyyy-MM-dd`）；
    - `type`：支持 `String`/`Number`/`Object`（Object 子属性**不可为空**）；
    - `passing_method`：`大模型识别`（从用户 query 提取）或 `业务透传`（由外部传入 `biz_params`）；
  - 输出参数（`out_params`）：定义模型如何解析 API 响应，**所有字段必填且层级宜扁平**。

## 使用方式

插件可通过三种方式集成：

1. **控制台可视化集成**：
   - 官方/三方插件：在[插件](https://bailian.console.aliyun.com/#/plugin-market)页面，单击目标插件的**添加至智能体**，选择工具与目标智能体应用即可；
   - 自定义插件：需先发布为 MCP 服务（插件卡片 → **发布为MCP服务**），再在智能体编排页的 **MCP 区块**中添加 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)；
   - 注意：官方插件仅支持与**同业务空间**的智能体关联；子业务空间首次使用需单独授权。

2. **工作流应用**：
   - 将插件作为独立节点拖入画布，显式配置输入/输出映射，不依赖模型自主决策 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)。

3. **API 调用**：
   - Assistant API：在 `tools` 数组中声明工具 ID（如 `"id": "calculator"`），模型自动规划调用；
   - DashScope SDK / HTTP 接口：需在请求体中传入 `tools` 列表及 `tool_choice` 策略，并通过 `biz_params` 传递 `业务透传` 参数或用户级鉴权 [Token](../concepts/token.md) [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

## 限制和注意事项

- **调用上限**：单次对话中最多调用 10 个工具（含同一插件下的多个工具）；
- **Object 类型限制**：GET 请求**不支持 Object 类型输入参数**；POST 请求中 Object 的子属性**必须非空**，否则发布失败（错误码 130022）；
- **鉴权与透传**：`业务透传` 参数和用户级鉴权 [Token](../concepts/token.md) **必须通过 `biz_params` 传入**，不可写入用户 query；
- **调试要求**：所有自定义工具必须经**在线测试成功**并**发布**后才可在应用中调用；草稿状态工具不可用；
- **删除风险**：删除插件将**级联删除其下所有工具**，且已关联该插件的应用将立即失效，操作不可逆；
- **计费提示**：`text_to_image` 和 `quark_search` 为限时免费，需主动申请开通；其余官方插件当前免费，但策略可能调整；
- **安全边界**：`code_interpreter` 插件**禁止网络访问与本地文件上传**，依赖库版本固定，不可扩展 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。

## 来源文档

- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)
- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)


