# plug in

插件是百炼平台用于扩展大模型能力的核心机制，通过将外部工具（如计算器、搜索、代码执行等）以标准化方式接入，弥补大模型在实时信息获取、精确计算、多模态生成等方面的固有局限。插件可直接集成至智能体应用、工作流或通过 Assistant API 调用，无需修改模型本身。所有插件均以“工具”为最小可调用单元，由大模型根据用户输入自主规划调用逻辑（智能体模式）或按编排顺序执行（工作流模式）。

## 支持的模型/功能

当前明确支持插件调用的模型为：  
- `qwen-plus`（通义千问-Plus）  
- `qwen-max`（通义千问-Max）  

> **注意**：文档 1 中称“各模型对插件的兼容性可能有差异，最新的兼容性状态，请以控制台实际执行结果为准”，而文档 3 未提及其他模型支持情况；目前无证据表明 `qwen-turbo` 或 `qwen2-*` 系列已正式支持插件，开发者应以控制台运行验证为准。  
官方插件开箱即用，覆盖 Python 代码解释、复杂数学计算、文本生成图像、实时网络搜索（夸克）、二维码生成、GitHub 项目检索等场景；三方插件需开通后使用，领域涵盖商业服务、教育、音视频等；自定义插件支持完全自主开发与云市场 API 导入。详情请参见 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)。

## 关键参数

插件调用依赖两类关键参数配置：

- **插件级参数**：  
  - `plugin_url`（必需）：插件根域名，如 `https://myapi.example.com`；所有工具路径将拼接于此。  
  - 鉴权配置（可选）：支持 `Header`（如 `Authorization: Bearer <token>`）或 `Query`（如 `?api_key=xxx`）方式，鉴权类型包括 `basic`/`bearer`/`appcode`；服务级鉴权使用 `Token` 字段，用户级鉴权需在对话前动态传入。  

- **工具级参数**（每个工具独立配置）：  
  - `tool_path`：以 `/` 开头的相对路径（如 `/search`），与 `plugin_url` 拼接成完整请求地址。  
  - 输入参数（`in_params`）：需明确定义 `name`、`description`、`type`（String/Number/Object 等）、`required`、`passing_method`（`大模型识别` 或 `业务透传`）。Object 类型子属性**不能为空**，否则发布失败（见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md) 错误码 130022）。  
  - 输出参数（`out_params`）：定义 API 返回数据中哪些字段将被大模型提取并用于最终回复，描述须简洁准确，层级宜扁平。  
  - 高级配置（可选）：提供 `user_input → expected_payload` 示例对，提升大模型参数构造准确率。

## 使用方式

插件可通过三种方式集成：

1. **控制台智能体应用**：  
   - 官方/三方插件：在 [插件市场](https://bailian.console.aliyun.com/#/plugin-market) 页面点击 **添加至智能体** → 选择工具 → 关联目标智能体（注意：官方插件仅支持同业务空间内关联）。  
   - 自定义插件：需先发布为 MCP 服务（插件卡片 → **发布为MCP服务**），再在智能体编排页的 **MCP 区块** 中添加。  
   - 鉴权或业务透传参数需在开启对话前通过图标配置（[自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md) 中详述）。

2. **工作流应用**：  
   将插件作为独立节点拖入画布，手动编排执行顺序，不依赖大模型自主决策。适用于确定性任务链路。

3. **API 调用**：  
   - Assistant API：在 `tools` 数组中传入工具 ID（如 `"calculator"`），系统自动处理调用与结果注入。  
   - DashScope SDK / HTTP 接口：通过 `biz_params` 传递业务透传参数或用户级鉴权 [Token](../concepts/token.md)（详见 [应用的参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)）。

工具 ID 获取路径：插件详情页 → 工具行悬浮 → 点击复制图标（见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)）。

## 限制和注意事项

- **数量限制**：单个智能体应用最多关联 **10 个工具**（含不同插件下的工具）。  
- **Object 参数约束**：GET 请求**不支持 Object 类型输入参数**；POST 请求中 Object 的子属性必须显式定义，不可为空（否则发布报错 130022）。  
- **鉴权与权限**：RAM 子账号首次使用插件（含云市场导入）需主账号授予 `ram:CreateServiceLinkedRole` 权限（策略脚本见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md) 和 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)），否则授权失败。  
- **功能边界**：  
  - Python 代码解释器**禁止网络访问与本地文件上传**，仅支持预装依赖（如 pandas、matplotlib、sympy 等）；  
  - 夸克搜索与 GitHub 搜索**仅返回标题、摘要、链接，不支持抓取网页正文或仓库代码**；  
  - 图片生成与二维码生成均为限时免费，需单独申请开通。  
- **变更风险**：删除插件将**级联删除其下所有工具**，且已关联该插件的应用将立即失效（[自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md) 明确警示）。

## 来源文档

- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)
- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)


