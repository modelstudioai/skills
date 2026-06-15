# Token 与计量

Token 是大语言模型处理文本的基本单位，也是百炼平台衡量模型用量和计算费用的核心度量。在百炼平台中，Token 贯穿模型推理、训练、部署、监控和成本管理的全流程。

## Token 的含义

Token 并非直接等同于字符或单词，而是模型分词器（Tokenizer）对文本切分后的最小片段。在百炼平台中，经验换算关系为：

- 1 个汉字约对应 1.5–2 个 Token
- 1 个英文单词约对应 1.3 个 Token

不同模态的用量统计单位有所不同：

| 模型类型 | 统计单位 |
|---------|---------|
| 大语言模型（文本生成、深度思考、视觉理解） | Token |
| 图像生成 | 张 |
| 视频生成 | 秒 |
| 语音模型 | 秒/字符/Token |
| 向量模型 | Token |

对于视觉理解场景，图片的 Token 数按分辨率计算：`Token 数 = h × w / (32 × 32) + 2`。

## 推理计费中的 Token

百炼模型推理按输入/输出 Token 数量分别计费，部分模型实行阶梯计费——单价取决于单次请求的输入 Token 总量，该请求所有 Token 均按对应阶梯单价结算。

关键定价参考（每百万 Token，华北2北京/中国内地）：

| 模型 | 输入单价 | 输出单价 |
|------|---------|---------|
| qwen3.7-max | 12 元 | 36 元 |
| qwen3-max（0~32K） | 2.5 元 | 10 元 |
| qwen-plus（0~128K） | 0.8 元 | 2–8 元 |

Batch 调用可享半价，上下文缓存支持折扣。不同地域定价存在差异。

## 训练与部署中的 Token

模型训练同样按 Token 计费，公式为：

```
费用 = (训练数据 Token 总数 + 混合训练数据 Token 总数) × 循环次数 × 训练单价
```

[模型部署](model-deployment.md)场景中，预置吞吐按 TPM（每分钟 Token 数）和使用时长计费。当输入超过最长输入 Token 或超出购买的 TPM 量时，调用自动切换为按量付费模式。

## Token 监控与管理

百炼平台提供三个层次的 Token 消耗管理：

- **汇总**：按[业务空间](workspace.md)维度汇总各模型的历史 Token 消耗，支持按时间范围和 API Key 筛选
- **追踪**：开通推理日志后，可记录每一次调用的 Token 消耗明细
- **告警**：支持设置 Token 消耗阈值，异常时立即通知

核心监控指标包括 `model_usage`（模型用量总和）、RPM（每分钟请求数）、TPM（每分钟 Token 数）等，支持接入 Prometheus/Grafana 进行可视化分析。

## 成本优化

费用抵扣顺序为：**免费额度 > 资源包 > 其他模型节省计划 > AI 通用型节省计划 > 按量付费**。

- **免费额度**：首次开通时自动发放，仅抵扣实时推理，不支持 Batch 调用和训练
- **资源包**：预购固定 Token 数量，仅抵扣特定模型的实时推理用量
- **节省计划**：通过承诺月消费金额换取折扣，AI 通用型最高 5.3 折

## Token Plan 订阅模式

除按量付费外，百炼还提供 Token Plan 团队版和 Coding Plan 两种包月订阅：

- **Token Plan 团队版**：按 Token 消耗抵扣 Credits，无频次限额，适合团队/企业场景
- **Coding Plan**：按模型调用次数计费，适合个人开发者

两种订阅的 API Key 和 Base URL 与按量付费体系互不相通，不可混用。

## 关联主题页

- [test 1](../guides/test-1.md)
- [token plan guide](../guides/token-plan-guide.md)
- [model monitoring](../guides/model-monitoring.md)
- [model inference](../guides/model-inference.md)
- [support](../guides/support.md)


