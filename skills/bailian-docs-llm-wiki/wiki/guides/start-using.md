# start using

本节介绍如何快速接入百炼平台并启动首个应用，涵盖模型调用、应用构建与基础配置。适用于希望以最小学习成本完成原型验证或生产部署的开发者。所有操作均基于统一 API 接口与控制台交互，无需修改底层基础设施。

## 支持的模型/功能

百炼当前支持通义千问系列（Qwen1.5、Qwen2、Qwen2.5）、Qwen-VL 多模态模型，以及面向企业场景优化的 Qwen-Audio 和 Qwen-Embedding。应用层功能包括知识库问答、工作流编排、RAG 增强、[函数调用](../concepts/function-calling.md)（Function Calling）和多轮对话状态管理。详细能力矩阵请参见 [开始使用](../../raw/application-user-guide/start-using.md)。

## 关键参数

调用 `/v1/chat/completions` 时必填参数为 `model`（如 `qwen-max`、`qwen-plus`）与 `messages`；推荐显式设置 `temperature=0.7` 和 `top_p=0.9` 以平衡确定性与多样性。若启用流式响应，需传入 `stream=true` 并按 SSE 协议解析。参数说明详见 [开始使用](../../raw/application-user-guide/start-using.md) 中的“API 参数速查”小节。

## 使用方式

1. **控制台快速启动**：登录后进入「应用」→「新建应用」，选择「知识库问答」模板，上传文档后点击「发布」即可获得可调用 endpoint；  
2. **API 直接调用**：使用 `Authorization: Bearer <api_key>` 请求 `https://dashscope.aliyuncs.com/api/v1/chat/completions`，示例见 [开始使用](../../raw/application-user-guide/start-using.md)；  
3. **SDK 集成**：推荐使用 `dashscope==1.20.0+` 版本（旧版 `dashscope<1.18.0` 不兼容 Qwen2.5 模型），初始化时需指定 `api_key` 与 `base_url`（国内用户建议设为 `https://dashscope.aliyuncs.com/api/v1`）。

> **注意**：原始文档中提及的 `build-knowledge-base-qa-assistant-without-coding.md` 所述“零代码拖拽节点”功能，已于 v2.3.0 版本起移至「工作流」模块，原路径下内容已过时，请以控制台最新 UI 为准。

## 限制和注意事项

- 免费额度仅限新注册账号首 30 天内使用，超出后需绑定支付方式；  
- 单次请求 `messages` 总长度上限为 32768 token（含 system + user + assistant），超长文本需预切分；  
- 知识库上传文件单个不超过 100 MB，且不支持 `.exe`、`.bin` 等可执行格式；  
- 流式响应中 `delta.content` 可能为空字符串（尤其在 function call 场景），需容错处理——该行为与 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md) 中 v2.4.1 的变更说明一致。

## 来源文档

- [开始使用](../../raw/application-user-guide/start-using.md)


