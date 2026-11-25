# decision-model-preview

面向高频业务判断的结构化决策模型，可根据文本或业务状态并行完成分类、是非判断与评分，并返回概率分布和置信度，适用于工单分流、内容审核、智能体路由与结果校验等场景。

<a id="推理服务供应商"></a>

<a id="h-dm-provider"></a>

## 推理服务供应商

`decision-model-preview` 模型的推理服务供应商为阿里云百炼。

<a id="模型能力"></a>

<a id="h-dm-cap"></a>

## 模型能力

| 能力项 | 支持情况 | 能力项 | 支持情况 |
| --- | --- | --- | --- |
| 输入模态 | **Text** | 输出模态 | **Text（结构化决策结果）** |
| 模型体验 | 不支持 | Function Calling | 不支持 |
| 结构化输出 | 不支持 | 联网搜索 | 不支持 |
| 前缀续写 | 不支持 | 上下文缓存 | 不支持 |
| 批量推理 | 不支持 | 模型调优 | **支持** |

<a id="上下文限制"></a>

<a id="h-dm-ctx"></a>

## 上下文限制

| 参数 | 值 | 参数 | 值 |
| --- | --- | --- | --- |
| 最大输入长度 | 65,536 | 最大输出长度 | 0 |
| 上下文长度 | 65,536 |  |  |

<a id="模型价格"></a>

<a id="h-dm-price"></a>

## 模型价格

本文仅展示模型调用原价，不包含限时优惠等活动信息，请前往[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)查看活动优惠。

<a id="sec-tabs"></a>

<a id="华北2-北京"></a>

<a id="华北2-北京-h4"></a>

#### 华北2（北京）

<table><thead><tr><th>计费项</th><th>价格（元）</th><th>单位</th></tr></thead><tbody><tr><td colspan="3"><p>限时免费</p></td></tr></tbody></table>

<a id="新加坡"></a>

<a id="新加坡-h4"></a>

#### 新加坡

<table><thead><tr><th>计费项</th><th>价格（元）</th><th>单位</th></tr></thead><tbody><tr><td colspan="3"><p>限时免费</p></td></tr></tbody></table>

<a id="限流"></a>

<a id="h-dm-rl"></a>

## 限流

<a id="sec-tabs-2"></a>

<a id="华北2-北京-2"></a>

<a id="华北2-北京-2-h4"></a>

#### 华北2（北京）

| 参数 | 值 |
| --- | --- |
| RPM（每分钟请求数） | 1,200 |
| TPM（每分钟tokens） | 2,000,000 |

<a id="新加坡-2"></a>

<a id="新加坡-2-h4"></a>

#### 新加坡

| 参数 | 值 |
| --- | --- |
| RPM（每分钟请求数） | 1,200 |
| TPM（每分钟tokens） | 2,000,000 |

<a id="调用方式"></a>

<a id="h-dm-call"></a>

## 调用方式

模型的调用协议、请求/响应参数与代码示例请参见[决策模型 API](../../../../model-api-reference/decision-model/decision-model-api.md)。
