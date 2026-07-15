# model high speed inference

百炼平台针对推理性能与容量保障提供了两类高速推理能力：一是通过 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 为指定模型锁定专属吞吐容量，规避公共资源限流；二是通过[快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)（Fast mode）提升单请求的 TPS（Tokens Per Second），面向对输出速度敏感的场景。两者关注点不同——预留解决"容量刚性兑付"，快速模式解决"输出更快"，可按需选型或组合使用。

## 能力对比与选型

| 能力 | 解决的问题 | 计费方式 | 超额处理 | 代码改动 |
| --- | --- | --- | --- | --- |
| TPM 预留 | 高峰期专属容量、不被公共限流 | 按 kTPM 预付费 | 自动降级公共池按量，不中断 | 替换 `model` 为专属 code |
| 快速模式 | 更高 TPS（80~100 TPS） | 按 token（同标准 API） | 超额进入排队，不立即限流 | 指定 fast 模型 ID + 专属域名 |

> **注意**：[TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 文档中的方案对比还列出了按量付费、资源包/节省计划、PTU 专属部署等其他容量方案；如需专属部署实例或极致高吞吐，可评估 PTU（模型部署）。

## TPM 预留

### 功能与特性

TPM（Tokens Per Minute）预留为指定模型锁定专属推理吞吐量，预留容量内的调用不与其他用户共享、不受公共限流影响。核心特性见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)：

- **容量保障**：预留 TPM 为业务专属，刚性兑付。
- **专属模型 code**：创建后系统自动生成专属 `model` code，必须在 API 请求中把 `model` 参数替换为该 code 才生效。
- **超额不中断**：超出预留容量的请求自动降级为按量计费，无需改代码，可在详情页"超额降级统计"查看降级次数。

### 关键参数（创建时）

| 参数 | 说明 | 取值 |
| --- | --- | --- |
| 预留名称 | 自定义标识 | ≤ 50 字符 |
| 选择模型 | 仅支持已开放 TPM 预留的模型 | 以控制台为准 |
| 付费周期 | 计费周期 | 按天 |
| 输入 TPM / 输出 TPM | 预留吞吐量，1 kTPM = 1,000 Tokens/分钟 | 起步与步长因模型而异 |
| 购买时长 | 有效时长 | 1~30、60、90、120、365 天 |
| 到期自动续费 | 到期前一天 08:00 自动扣款 | 默认开启 |

创建页右侧提供 **TPM 容量计算器**，可根据 RPM、平均输入/输出长度、缓存命中率估算推荐的输入/输出 TPM，其中缓存命中率仅影响输入 TPM。

### 使用方式

创建预留后进入详情页"概览"Tab 复制专属模型 code，将请求中的 `model` 参数替换即可：

```python
import dashscope

response = dashscope.Generation.call(
    api_key="your-api-key",
    model="your-dedicated-model-code",   # 替换为专属模型 code
    messages=[{"role": "user", "content": "你好"}],
)
print(response.output.text)
```

> **注意**：请求量短时间快速拉升时系统需短暂预热，预热期间部分请求可能出现延迟波动，请做好排队或重试机制。

### 计费、生命周期与管理

- 部署成功即开始计费，预留容量内的调用不额外收费；预付费一次性支付，费用以控制台为准。
- 缩容/退订退费按已用部分 1.5 倍系数结算：`退款 = 降量部分预付费 - (降量部分预付费 × 已用时长/购买时长 × 1.5)`。
- 到期后生命周期：0~2 小时仍运行中可调用/续费；2~14 小时已停止不可调用但可续费；14 小时后实例删除不可恢复。
- 详情页含"概览""监控""API 接入"三个 Tab，支持扩缩容（变配期间不中断）、续订、退订。退订不可恢复，专属 code 失效后请求回退公共资源。

## 快速模式（Fast mode）

### 功能与特性

快速模式面向 AI 编程助手、Agent 多步推理、实时对话等对输出速度敏感的场景。据[快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)文档：

- **高速输出**：TPS 提升至标准 API 的 1.5~2 倍，达 80~100 TPS。
- **按 token 计费**：计费逻辑与标准 API 一致，按输入/输出 token 计费。
- **特殊限流**：超出 TPM 额度不立即限流，请求进入排队队列。
- **preview 阶段**：能力与规格可能随版本调整。

当前支持模型为 `glm-5.2-fast-preview`（华北2（北京）、新加坡地域）。

### 使用方式

无需额外参数，调用时把 `model` 指定为支持的 fast 模型 ID 即可开启，但需使用专属接入域名：

```
https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1
```

其中 `{workspace_id}` 可在业务空间管理页切换到对应地域后查看。基础调用示例：

```bash
curl -X POST https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "glm-5.2-fast-preview",
    "messages": [{"role": "user", "content": "你是谁"}],
    "stream": false
}'
```

`glm-5.2` 默认返回 `reasoning_content` 思考字段；[流式输出](../concepts/streaming.md)时思考内容与回答内容分别通过 `delta.reasoning_content` 与 `delta.content` 推送，`usage.completion_tokens_details.reasoning_tokens` 记录思考 token 数。

## 限制与注意事项

- **接入域名不同**：TPM 预留使用标准 `dashscope.aliyuncs.com` 域名 + 专属 code；快速模式使用 `{workspace_id}.cn-beijing.maas.aliyuncs.com` 专属域名 + fast 模型 ID，两者接入方式不可混用。
- **超额行为不同**：TPM 预留超额自动降级按量计费（不中断）；快速模式超额进入排队（不立即限流）。
- **preview 风险**：快速模式仍处 preview，能力与规格可能变动，生产接入前请评估稳定性。
- **计价与错误码**：快速模式的详细价格与错误码分别参见[快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)引用的"模型调用计费""错误码"文档；TPM 预留的实际费用以百炼控制台为准。

## 来源文档

- [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)
- [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)


