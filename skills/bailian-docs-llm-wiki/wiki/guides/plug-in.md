# plug in

插件是百炼平台用于扩展大模型能力的核心机制，通过将外部工具（如 API）封装为可调用的标准化组件，弥补大模型在实时信息获取、精确计算、代码执行、图像生成等方面的固有局限。插件支持官方预置、三方市场及自定义开发三种来源，可在智能体应用、工作流应用及 Assistant API 中统一调用。其核心设计目标是让大模型“按需调用工具”，而非替代工具本身。

## 支持的模型与功能

当前插件能力仅在以下模型上完整支持：  
- `qwen-plus`（通义千问-Plus）  
- `qwen-max`（通义千问-Max）  

> **注意**：文档 1 中声明“各模型对插件的兼容性可能有差异”，但未明确说明不兼容场景；而文档 3 未提及其他模型支持状态。实际使用请以控制台运行结果为准，建议优先选用 `qwen-max` 进行插件集成验证。该兼容性说明详见 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)。

插件按来源分为三类，功能边界清晰：  
- **官方插件**：开箱即用，无需配置参数，包括 `code_interpreter`（Python 执行）、`calculator`（数学计算）、`text_to_image`（文生图）、`quark_search`（实时搜索）、`generate_qrcode`（二维码生成）、`github_search`（GitHub 搜索）等。详细能力与限制见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。  
- **三方插件**：来自云市场，覆盖商业服务、教育、音视频等领域，开通后即可调用，无需额外配置。  
- **自定义插件**：用户自主开发或导入的 API 封装，支持完全可控的鉴权（Header/Query）、参数映射与错误处理，适用于私有业务系统集成。创建与调试流程详见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

## 关键参数

插件调用依赖两类关键参数：**插件级配置**与**工具级参数**。

- **插件级参数**（作用于整个插件）：
  - `plugin_url`：插件根域名（如 `https://xxx.com`），所有工具路径均以此为基础拼接。
  - 鉴权配置（可选）：支持 `Header` 或 `Query` 方式，`Type` 可选 `basic`/`bearer`/`appcode`，`Token` 为服务级凭据；用户级鉴权需在对话前通过控制台或 `biz_params` 透传。

- **工具级参数**（作用于单个 API）：
  - `tool_path`：必须以 `/` 开头的相对路径（如 `/query`），与 `plugin_url` 拼接为完整请求地址。
  - 输入参数（`in-params`）：需明确定义 `参数名称`、`参数描述`、`类型`（String/Number/Object 等）、`传参方式`（`大模型识别` 或 `业务透传`）。Object 类型子属性**不可为空**，否则发布失败（错误码 `130022`）。
  - 输出参数（`out-params`）：定义 API 返回数据中哪些字段将被大模型提取并用于最终回复，描述须精简准确，层级宜扁平。

> **注意**：文档 2 明确要求 GET 请求下输入参数**不支持 Object 类型**，而文档 3 未提及此限制。若使用 GET 方法，请严格遵循 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md) 的约束，避免因类型不匹配导致发布失败。

## 使用方式

插件可通过以下三种方式集成：

1. **控制台集成（推荐快速验证）**：
   - 官方/三方插件：在 [插件市场](https://bailian.console.aliyun.com/#/plugin-market) 页面点击 **添加至智能体** → 选择工具 → 绑定目标智能体应用。
   - 自定义插件：先发布为 MCP 服务（插件卡片 → **发布为MCP服务**），再在智能体编排页的 **MCP 区块** → **+** → **自定义MCP** 中添加。
   - 所有插件均支持在对话测试页配置鉴权 Token 或业务透传参数（点击 ![icon] 按钮）。

2. **工作流应用**：
   - 将插件作为独立节点拖入画布，手动编排执行顺序，不依赖大模型自动规划。详情见 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)。

3. **API 调用**：
   - 通过 DashScope SDK 或 HTTP 接口，在 `tools` 字段中传入工具 ID（如 `"calculator"`）及必要参数。
   - 若含 `业务透传` 参数或用户级鉴权，需通过 `biz_params` 传递（参考 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md) 中的 API 调用说明）。
   - Assistant API 用户请查阅其文档中 `tools` 相关章节。

## 限制和注意事项

- **权限限制**：首次访问插件市场需主账号或已授权 RAM 子账号完成 `AliyunServiceRoleForSFMAccessCloudAPI` 服务关联角色授权。RAM 用户需主账号预先授予 `ram:CreateServiceLinkedRole` 权限（脚本见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)），否则无法进入插件页面。
- **调用限制**：
  - 单个智能体应用最多绑定 **10 个工具**（含不同插件下的工具）。
  - Python 代码解释器插件**禁止网络访问与本地文件上传**，可用依赖库已固化（见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)）。
  - 夸克搜索与 GitHub 搜索插件**仅返回摘要/标题/链接，不支持抓取网页或仓库详情页内容**。
- **生命周期管理**：
  - 插件/工具删除为**不可逆操作**，将导致所有关联应用失效。
  - 修改插件 URL 或鉴权配置后，必须重新测试并发布所有下属工具。
- **调试要点**：
  - 工具发布前必须通过 **在线调试**（`测试工具` 按钮），确保返回状态码为 `200` 且响应结构符合出参定义。
  - 常见发布失败原因：参数描述缺失（错误码 `130040`）、Object 子属性为空（`130022`）、工具名称超长（>20 字符）。

## 来源文档

- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)
- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)


