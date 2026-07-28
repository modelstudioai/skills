# model high speed inference

百炼平台为高吞吐、低[限流](../concepts/rate-limit.md)影响的推理场景提供两类高速推理能力：**TPM 预留**通过预付费锁定专属推理容量，保障业务高峰期不受公共[限流](../concepts/rate-limit.md)影响；**快速模式（Fast mode）**则以更高的输出 TPS（80~100 TPS，约为标准 API 的 1.5~2 倍）服务对输出速度敏感的场景。两者定位不同：前者解决"容量确定性"，后者解决"输出速度"。

## 能力概览与选型

| 能力 | 解决的问题 | 计费方式 | 接入改动 | 状态 |
| --- | --- | --- | --- | --- |
| TPM 预留 | 锁定专属吞吐容量，不受公共[限流](../concepts/rate-limit.md)影响 | 按 kTPM 预付费（按天） | 将 `model` 参数替换为专属模型 code | 正式 |
| 快速模式 | 提升输出速度（TPS 1.5~2 倍） | 按 token 计费，与标准 API 一致 | 使用专属域名 + fast 模型 ID | preview |

结合 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 中的方案对比：流量可预估、不能接受限流选 TPM 预留；追求更高吞吐/性能可考虑 PTU 专属部署；流量波动大或短期使用则维持按量付费（可叠加资源包/节省计划做费用优化）。

## TPM 预留

### 核心机制

- **专属容量**：预留的 TPM（Tokens Per Minute）容量业务专属，不与其他用户共享，刚性兑付。
- **专属模型 code**：创建后系统自动生成专属模型 code，API 请求中把 `model` 参数替换为该 code 即可使用预留容量，无需其他代码改动。
- **溢出策略**（创建时选择）：
  - 自动溢出至按量计费（默认）：超出部分降级为标准按量计费，业务不中断，可在详情页"超额降级统计"查看降级次数；
  - 仅使用预留容量：超出请求返回 429，不产生额外费用。

### 关键参数（创建时）

| 参数 | 说明 |
| --- | --- |
| 选择模型 | 仅支持已开放 TPM 预留的模型（如千问3.7-Max/Plus、千问3.6-Flash、GLM-5.2/5.1、DeepSeek-v4-Flash/Pro、Kimi-K2.6，以控制台为准） |
| 输入/输出 TPM | 单位 kTPM（1 kTPM = 1,000 Tokens/分钟），起步和步长因模型而异 |
| 付费周期 | 按天 |
| 购买时长 | 1~30、60、90、120、365 天 |
| 到期自动续费 | 默认开启，到期前一天 08:00 自动扣款 |
| 溢出策略 | 自动溢出（默认）/ 仅使用预留容量 |

创建页右侧提供 **TPM 容量计算器**，按 RPM、平均输入/输出长度、缓存命中率估算所需容量；部分模型有长输入阶梯系数（如 glm-5.1 在 [32K, 200K] 区间输入按 1.33 折算）和缓存折扣（如 deepseek-v4-pro 缓存命中按 8% 折算容量），计算器会自动应用，详见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。

### 接入方式

```python
import dashscope

response = dashscope.Generation.call(
    api_key="your-api-key",
    model="your-dedicated-model-code",   # 替换为专属模型 code
    messages=[{"role": "user", "content": "你好"}],
)
print(response.output.text)
```

> **注意**：短时间内请求量快速拉升时系统需要短暂预热，预热期间部分请求可能出现延迟波动，请做好请求排队或重试机制。

### 计费与生命周期要点

- 部署成功即开始计费，预留容量内调用不额外收费；价格按地域和模型不同（如北京地域千问3.7-Max 输入 ¥121.00 / Per 10,000 TPM / 天），**以控制台为准**。
- 缩容/退订退费公式：`退款 = 降量部分预付费 - (降量部分预付费 × 已用时长/购买时长 × 1.5)`，即已使用部分按 1.5 倍系数结算。
- 支持扩缩容（不中断服务）；TPM 可归 0 以保留专属模型 code 且不产生容量费用，但归 0 属减配、按上述违约金结算。
- 到期后 2 小时内仍可调用、可续费；2~14 小时实例停止、可续费恢复；14 小时后删除、不可恢复。退订后专属 code 失效，请求回退公共资源按量计费。

## 快速模式（Fast mode）

### 核心特性

- **高速输出**：TPS 达 80~100，为标准 API 的 1.5~2 倍，适用于 AI 编程助手、Agent 多步推理、实时对话等场景。
- **按 token 计费**：与标准 API 一致，按输入/输出 token 计费。
- **特殊限流**：超出 TPM 额度不立即限流，请求进入排队队列。

> **注意**：快速模式当前为 preview 阶段，能力与规格可能随版本调整，详见 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)。

### 使用方式

将 `model` 指定为 fast 模型 ID（当前支持 `glm-5.2-fast-preview`，北京与新加坡地域）即可开启，无需额外参数。接入域名为专属格式：

```
https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1
```

`{workspace_id}` 在控制台[业务空间](../concepts/workspace.md)管理页面切换到对应地域后查看。

```bash
curl -X POST https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "glm-5.2-fast-preview", "messages": [{"role": "user", "content": "你是谁"}], "stream": false}'
```

glm-5.2 默认返回 `reasoning_content` 思考字段；[流式输出](../concepts/streaming.md)时思考内容与回答内容分别通过 `delta.reasoning_content` 与 `delta.content` 推送，客户端需分别处理。

## 限制与注意事项

- **TPM 预留**：仅支持控制台展示的已开放模型；创建需一次性预付费，建议先用容量计算器估算；退订不可恢复且专属 code 立即失效；频繁降级或 429 时应扩容。
- **快速模式**：preview 阶段规格可能变化；当前支持模型有限（glm-5.2-fast-preview）；使用专属 workspace 域名而非标准 dashscope 域名。
- **两者接入方式不同**：TPM 预留走标准域名 + 专属模型 code；快速模式走专属 workspace 域名 + fast 模型 ID，切勿混用，具体分别参见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 与 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)。

## 来源文档

- [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)
- [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)


