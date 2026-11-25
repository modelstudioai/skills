# API 兼容性升级

阿里云百炼 API 兼容性升级记录，持续更新请求参数、响应结构及接口行为调整。

为提升协议兼容性，阿里云百炼将持续升级 API 的请求参数、响应结构和接口行为。以下按公告更新日期记录升级内容。

<a id="2026-年-11-月-2-日"></a>

## 2026 年 11 月 2 日

<table><thead><tr><th>升级点</th><th>涉及 API</th><th>说明</th></tr></thead><tbody><tr><td><p><code>max_tokens</code> 行为调整，对齐 OpenAI 最新协议</p></td><td><p><a href="../../model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md">OpenAI Chat Completions API</a>、<a href="../../model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md">DashScope API</a></p></td><td><ul><li><strong>升级前</strong>：限制范围随模型及 <code>thinking_budget</code> 设置而异，可能仅包含最终回答，也可能包含思考与回答。</li><li><strong>升级后</strong>：自 <code>qwen4-max-preview</code> / <code>qwen4-max</code> 起，Qwen 系列新模型的 <code>max_tokens</code> 等效于 <code>max_completion_tokens</code>，限制思考内容与最终回答的 Token 总量；<code>max_completion_tokens</code> 含义不变。开启思考时，思考内容占用同一输出预算。<code>qwen4-max-preview</code> 之前的存量模型行为不变。</li></ul></td></tr></tbody></table>
