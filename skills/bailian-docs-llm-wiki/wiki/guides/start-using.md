# start using

`start using` 是百炼平台的入门引导模块，帮助开发者快速初始化应用、接入模型服务并构建基础 AI 功能。它不依赖预编译环境，支持通过控制台或 API 两种路径启动，适用于知识库问答、对话代理等典型场景。所有操作均需先完成[项目创建与密钥配置](../../raw/application-user-guide/project-setup.md)。

## 支持的模型/功能

当前 `start using` 模块默认集成以下模型能力：  
- 通义千问系列（qwen-max、qwen-plus、qwen-turbo）用于通用对话与推理；  
- 通义听悟（tingwu）用于音频转写（需显式启用 `enable_audio_input: true`）；  
- 知识库检索增强（RAG）功能，支持对接向量库与结构化数据源。  
完整模型列表及能力矩阵详见 [开始使用](../../raw/application-user-guide/start-using.md) 的“可用服务”章节。注意：部分新模型（如 qwen2.5-72b）虽已在 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md) 中宣布上线，但尚未在 `start using` 初始化流程中默认启用，需通过 `/v1/models` 接口手动指定。

## 关键参数

初始化请求必须包含以下参数：  
- `model`: 字符串，必填，值须为平台当前支持的模型 ID（见上节）；  
- `input`: 对象，必填，至少含 `text` 字段（纯文本输入）或 `audio_url`（启用听悟时）；  
- `parameters.temperature`: 浮点数，可选，默认 `0.8`，范围 `[0.0, 2.0]`；  
- `parameters.top_p`: 浮点数，可选，默认 `0.95`；  
- `enable_rag`: 布尔值，可选，默认 `false`；启用后自动触发知识库匹配（需提前配置知识库 ID）。  
详细参数说明请参考 [开始使用](../../raw/application-user-guide/start-using.md) 的“API 参数规范”小节。

## 使用方式

1. **控制台快速启动**：登录百炼控制台 → 进入「应用开发」→ 点击「新建应用」→ 选择「问答助手」模板 → 按向导完成知识库绑定与模型选择；  
2. **API 直连调用**：  
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "qwen-turbo",
           "input": {"text": "你好"},
           "parameters": {"temperature": 0.5}
         }'
   ```  
   更多示例见 [0代码构建问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。

## 限制和注意事项

- 单次请求 `input.text` 长度上限为 32768 字符，超长将被截断且**不返回警告**；  
- 启用 RAG 时，若未配置有效知识库 ID，请求将静默降级为纯模型生成（无报错），该行为与 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md) 中“RAG 失败必报错”的承诺存在矛盾；  
> **注意**：文档 [开始使用](../../raw/application-user-guide/start-using.md) 中声明“所有错误均返回 HTTP 4xx/5xx 及明确 code”，但实测 RAG 配置缺失时返回 200 + `{"output":{"text":"..."}}`，建议以实际接口响应为准；  
- 免费试用额度仅覆盖 `qwen-turbo` 和 `qwen-plus`，调用 `qwen-max` 需已开通付费账户，否则返回 `403 Forbidden`；  
- 音频输入（`audio_url`）仅支持 HTTPS 协议且文件大小 ≤ 100MB，格式限 MP3/WAV，该限制在 [0代码构建问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md) 中有明确说明。

## 来源文档

- [开始使用](../../raw/application-user-guide/start-using.md)


