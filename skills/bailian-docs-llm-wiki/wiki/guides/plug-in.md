# plug in

[插件](../concepts/plugin.md)是百炼平台用于扩展大模型能力的核心机制，通过将外部工具（如 API）集成到推理流程中，弥补大模型在实时信息获取、精确计算、代码执行、图像生成等方面的固有局限。[插件](../concepts/plugin.md)以“工具集合”形式组织，支持官方预置、三方市场及完全自定义三类来源，可被智能体应用、工作流应用或 Assistant API 主动调用或编排执行。

## 支持的模型/功能

当前[插件](../concepts/plugin.md)能力仅在以下模型上可用：`qwen-turbo`、`qwen-plus`、`qwen-max`、`qwen-vl-max`、`qwen-vl-plus`。各模型对插件调用的规划能力与响应稳定性存在差异，实际兼容性请以控制台运行结果为准。插件功能覆盖四类典型场景：  
- **计算与数据处理**：如 `calculator`（复杂数学运算）、`code_interpreter`（Python 代码执行，支持 `pandas`、`matplotlib`、`sympy` 等依赖，但[不支持网络访问与本地文件上传](../../raw/application-user-guide/plug-in/plugins.md)）；  
- **实时信息检索**：如 `quark_search`（基于夸克引擎的网页标题/关键词/摘要检索，[不支持直接访问网页详情](../../raw/application-user-guide/plug-in/plugins.md)）；  
- **内容生成**：如 `text_to_image`（文生图）、`generate_qrcode`（URL 转二维码）；  
- **第三方服务集成**：如 `github_search`（GitHub 项目检索，[仅返回标题、链接与摘要，不支持项目详情访问](../../raw/application-user-guide/plug-in/plugins.md)）。

> **注意**：文档 1 中称“夸克搜索插件目前支持检索网页标题、关键词和摘要，但不支持直接访问网页详情”，而文档 2 在相同位置重复该描述，但文档 2 后续“常见问题”节明确指出“联网搜索（`enable_search`）也是基于夸克搜索”，暗示夸克搜索是底层能力而非独立插件形态。此处以插件调用行为为准——即 `quark_search` 工具调用返回的是结构化摘要结果，非原始网页。

## 关键参数

插件调用依赖两类关键参数：  
- **工具 ID**：唯一标识一个工具，例如 `calculator`、`text_to_image`，用于 API 请求中指定目标工具。可通过插件详情页悬浮图标复制（见[自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)）；  
- **输入/输出参数**：  
  - 输入参数需明确定义 `参数名称`、`参数描述`、`类型`（String/Number/Object 等）、`传参方式`（`大模型识别` 或 `业务透传`）；Object 类型子属性**不能为空**，否则发布失败（见[自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)）；  
  - 输出参数用于指导大模型解析 API 响应，所有字段均为必填，且嵌套层级应尽量扁平；  
- **鉴权配置**（自定义插件专属）：支持 `Header` 或 `Query` 方式传递，`Type` 可选 `basic`/`bearer`/`appcode`，[Token](../concepts/token.md) 值由 API 提供方发放。

## 使用方式

插件可通过三种方式接入：  
1. **控制台集成至智能体应用**：在插件市场页面单击“添加至智能体”，选择工具与目标智能体（注意：[官方插件仅支持与同业务空间的智能体关联](../../raw/application-user-guide/plug-in/plugins.md)），最多添加 10 个工具；  
2. **工作流应用节点**：将插件作为独立节点拖入工作流画布，按编排顺序执行，不依赖大模型自主决策；  
3. **API 调用**：  
   - 通过 [Assistant API](https://help.aliyun.com/zh/model-studio/quick-start-of-assistant-api) 的 `tools` 字段声明可用工具；  
   - 通过 DashScope SDK 或 HTTP 接口调用时，若含 `业务透传` 参数或用户级鉴权，需通过 `biz_params` 传递（见[应用的参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)）；  
   - 自定义插件需先发布为 MCP 服务，再在智能体编排页的 **MCP 区块**中添加（见[自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)）。

## 限制和注意事项

- **权限前提**：首次使用插件前，主账号或 RAM 子账号必须授权服务关联角色 `AliyunServiceRoleForSFMAccessCloudAPI`。RAM 用户需主账号预先授予 `ram:CreateServiceLinkedRole` 权限（策略条件中 `ram:ServiceName` 必须为 `cloundapi-access.sfm.aliyuncs.com`），否则无法进入插件市场（见[官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)）；  
- **调用限制**：  
  - Python 代码解释器禁止网络请求与文件上传，依赖库版本固定（如 `requests~=2.31.0`、`pandas` 等）；  
  - 图片生成与夸克搜索为限时免费，需单独申请开通；  
  - 自定义插件发布前必须完成在线调试且状态为“成功”，否则无法启用；  
- **配置风险**：  
  - 删除插件将**不可逆地清除其下所有工具**，并导致已关联的应用失效；  
  - 修改插件 URL 或鉴权配置后，必须重新测试并发布所有工具；  
  - Object 类型输入参数在 GET 请求中不被支持，会导致发布失败（见[自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)）。

## 来源文档

- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)


