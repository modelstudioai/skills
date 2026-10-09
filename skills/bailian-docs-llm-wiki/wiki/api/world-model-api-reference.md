# world model api reference

世界模型 API 提供对多模态世界建模能力的程序化访问，支持场景理解、动态推演与行为生成等核心功能。当前以 HappyOyster 系列为主要实现，涵盖 Adventure（探索推演）、Directing（策略调度）和 Acting（具身动作生成）三类子模型。该接口面向需要构建智能体环境交互逻辑的开发者，需通过百炼平台统一鉴权调用。

## 支持的模型/功能

- **Adventure 模型**：用于开放世界状态推演与因果链预测，适用于游戏、仿真等长程决策场景。  
- **Directing 模型**：专注多智能体协作调度与任务分解，输出结构化指令序列。  
- **Acting 模型**：处于邀测阶段，提供细粒度动作生成能力（如“抓取左前方红色方块并旋转90°”），详见 [Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md)。  

> **注意**：原始文档中将 Acting 标注为“邀测中”，但 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) 的最新修订版（2024-05-12）已列出 `/v1/acting/generate` 路径，实际可用性请以控制台开通状态为准。

## 关键参数

所有请求需包含以下通用参数：
- `model`: 必填，值为 `happyoyster-adventure`、`happyoyster-directing` 或 `happyoyster-acting`  
- `input`: 必填，JSON 对象，结构依模型类型而异（详见 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md)）  
- `max_tokens`: 可选，最大输出 token 数，默认 1024，上限 4096  
- `temperature`: 可选，采样随机性控制，范围 [0.0, 2.0]，默认 0.7  

## 使用方式

1. 通过百炼平台获取 `API Key` 和 `Endpoint URL`（如 `https://dashscope.aliyuncs.com/api/v1/services/aigc/world-model/invoke`）  
2. 构造 POST 请求，`Content-Type: application/json`，Body 包含上述关键参数  
3. 解析响应中的 `output.text` 字段（文本生成类）或 `output.actions`（结构化动作类）  

示例调用可参考 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) 中的 cURL 片段。

## 限制和注意事项

- 单次请求 `input` 总长度（含上下文）不得超过 8192 tokens；超长输入将被截断且不报错。  
- Acting 模型仅对白名单用户开放，未获邀测权限时调用返回 `403 Forbidden`。  
- 所有模型均不支持流式响应（`stream: true` 无效），必须等待完整响应。  
- 输入中若含非 UTF-8 编码字符，可能导致解析失败，建议预处理为标准 Unicode。

## 来源文档

- [世界模型](../../raw/model-api-reference/world-model-api-reference.md)


