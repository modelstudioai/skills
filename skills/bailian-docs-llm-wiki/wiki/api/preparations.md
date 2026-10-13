# preparations

在调用百炼平台模型服务前，开发者需完成 API Key 获取与配置、SDK 安装、环境准备及参数校验等基础工作。这些步骤直接影响调用的可用性、安全性与稳定性。本文汇总关键准备事项，覆盖模型接入全链路起点，适用于所有通过 HTTP、DashScope SDK 或 [OpenAI 兼容接口](../concepts/openai-compatibility.md)调用百炼模型的场景。

## 支持的模型/功能

百炼支持两类主流调用路径：  
- **DashScope 原生协议**：适用于全部标准模型（如 `qwen-plus`、`qwen-max`、`deepseek-v4-pro`）、多模态模型（`qwen-vl`、`qwen3-vl`）、语音（ASR/TTS）、向量（Embedding）、排序（Rerank）等，详见 [文本生成](raw/model-api-reference/qwen-api-reference.md) 等单模型参考文档；  
- **[OpenAI 兼容接口](../concepts/openai-compatibility.md)**：支持 Python/Node.js/Java/Go 等语言的 OpenAI SDK，但仅限已开通的模型（如 `qwen3.7-plus`、`kimi-k3`），未在[模型市场](https://bailian.console.aliyun.com/cn-beijing/model/market)开通的模型将返回 `The product is not activated` 错误 [错误码](../../raw/model-api-reference/preparations/error-code.md)；  
- **实时语音与多模态模型**（如 Realtime API）需使用专用 [AOQ SDK](raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)，不兼容通用 DashScope 或 OpenAI SDK。

> **注意**：文档 2 中称“OpenAI Java SDK 推荐设置为 `3.5.0`”，但文档 3 明确要求 DashScope Python SDK Expert 需 ≥ `1.27.3`，且文档 4 的错误码示例中多次出现 `qwen3.7-plus` 等新模型名——表明模型命名体系已更新，旧文档中如 `Qwen/Qwen3.7-Plus`（文档 4 错误码节）等开源格式模型名**不可用**，必须使用百炼控制台模型列表中的标准 ID（如 `qwen3.7-plus`）[错误码](../../raw/model-api-reference/preparations/error-code.md)。

## 关键参数

调用必需的核心参数包括：

- `model`：严格匹配百炼模型市场中的 ID（如 `qwen-plus`），大小写敏感、不可含空格或社区别名；  
- `DASHSCOPE_API_KEY`：环境变量名，值为控制台生成的 `sk-` 开头密钥；  
- `base_url`：按地域区分，华北2（北京）为 `https://dashscope.aliyuncs.com/compatible-mode/v1`，其他地域需查 [Base URL 总览](raw/model-user-guide/get-started-with-models/base-url.md)；  
- `stream` / `incremental_output` / `enable_thinking`：强约束组合参数。例如：  
  - 启用 `enable_thinking` 时，`stream` 必须为 `true`，`result_format` 必须为 `"message"`，`incremental_output` 必须为 `"true"`；  
  - 某些模型（如 `qwen3.7-plus`）强制要求 `enable_thinking=true`，不可设为 `false` [错误码](../../raw/model-api-reference/preparations/error-code.md)；  
- `messages`：结构必须合法。纯文本模型禁止 `content` 为数组（如 `[{ "type": "text", ... }]`），必须为字符串；多模态模型则要求 `content` 数组内元素 `type` 仅限 `text`/`image_url`/`video_url` 等白名单类型 [错误码](../../raw/model-api-reference/preparations/error-code.md)。

## 使用方式

### 1. 获取与配置 API Key  
前往百炼控制台 [API Key](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key) 页面创建或复制密钥。**务必注意地域隔离**：各地域 API Key、接入域名、模型列表完全独立，不可混用 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)。配置方式推荐：  
- **环境变量**（最常用）：`export DASHSCOPE_API_KEY='sk-xxx'`（Linux/macOS）或系统属性（Windows）；  
- **代码内显式赋值**（仅限调试）：`dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")`；  
- **严禁**在客户端（浏览器/移动端）硬编码长期密钥，生产环境应使用 [临时 API Key](raw/model-api-reference/more-about-models/generate-temporary-api-key.md)（最长 1800 秒）。

### 2. 安装 SDK  
- **Python**：`pip install -U dashscope`（原生）或 `pip install -U openai`（OpenAI 兼容）；  
- **Java/Node.js/Go**：按 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md) 文档添加对应依赖；  
- **高级工具**：DashScope Python SDK ≥1.27.3 内置 [SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md)，支持自然语言生成可运行代码、自动诊断报错（如 `/skill diagnose gen.py`）、解释代码逻辑等，大幅提升开发效率。

## 限制和注意事项

- **地域与权限隔离**：API Key 绑定地域与业务空间，跨地域调用必失败；权限由归属业务空间决定，同一空间内所有 API Key 权限一致 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)；  
- **配额与数量**：单账号+单地域最多 50 个 API Key；自定义权限下最多勾选 30 个模型；IP 白名单最多 20 个地址 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)；  
- **安全红线**：  
  - 不得在客户端暴露长期 API Key；  
  - `sudo` 执行脚本时需加 `-E` 参数继承环境变量（`sudo -E python xx.py`），否则密钥不可见；  
  - systemd 等服务管理器需显式加载环境文件（`EnvironmentFile=`）；  
- **常见陷阱**：  
  - 环境变量配置后未重启 IDE/终端/服务，导致密钥未生效；  
  - 混用 DashScope 协议与 OpenAI 协议的 `messages` 结构（前者需嵌套于 `input` 对象内）；  
  - 纯文本模型传入图片 URL 导致 `Unexpected item type in content` 错误 [错误码](../../raw/model-api-reference/preparations/error-code.md)；  
- **排障必备**：所有错误响应均含 `request_id`（UUID 格式），调用失败时务必记录，用于日志查询或提工单 [错误码](../../raw/model-api-reference/preparations/error-code.md)。

## 来源文档

- [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [DashScope SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)


