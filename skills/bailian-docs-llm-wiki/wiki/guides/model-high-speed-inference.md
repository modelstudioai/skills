# model high speed inference

百炼平台针对推理调用的容量保障与输出速度提供了两类高速推理能力：**TPM 预留**为指定模型锁定专属吞吐量、抵御公共限流；**快速模式（Fast mode）**则在按 token 计费不变的前提下把输出速度（TPS）提升至标准 API 的 1.5~2 倍。两者定位不同，可根据业务是"要容量刚性兑付"还是"要更快出字"分别选用。

## TPM 预留：锁定专属推理容量

通过 TPM（Tokens Per Minute）预留，可为指定模型锁定专属推理吞吐量，预留容量内的调用不受公共资源限流影响，容量为业务专属、不与其他用户共享。详见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。

核心机制：

- **专属模型 code**：创建预留后系统自动生成专属 `model` code，需将 API 请求中的 `model` 参数替换为该 code 才能命中预留容量。
- **超额不中断**：超出预留容量的请求自动降级为按量计费处理，无需修改代码，可在详情页**超额降级统计**中查看降级次数。
- **计费**：按 kTPM（1 kTPM = 1,000 Tokens/分钟）预付费，部署成功即开始计费，预留容量内调用不额外收费。

### 方案选型

[TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 文档给出了四种容量方案对比，便于选型：

| 方案 | 计费单位 | 容量保障 | 适用场景 | 超额处理 | 代码改动 |
| --- | --- | --- | --- | --- | --- |
| 按量付费 | 按 token | 无（共享公共池） | 流量波动大/短期 | 受公共限流 | 无需改动 |
| 资源包/节省计划 | 预付费额度 | 承诺用量折扣（非专属） | 费用优化 | 超出转按量 | 无需改动 |
| TPM 预留 | 按 kTPM 预付费 | 专属容量刚性兑付 | 流量可预估、不能接受限流 | 自动降级公共池按量，不中断 | 替换 model 参数 |
| PTU 专属部署 | 按 kTPM 预付费 | 专属部署实例 | 高吞吐高性能 | 超出转按量 | 替换 model 参数 |

### 创建与接入

在[百炼控制台](https://bailian.console.aliyun.com/#/efm/tpm_reservation)单击**创建 TPM 预留**，填写预留名称、模型、付费周期（按天）、输入/输出 TPM（起步与步长因模型而异）、购买时长等参数并支付。创建页右侧的 **TPM 容量计算器**可根据 RPM、平均输入/输出长度、预估缓存命中率估算所需额度。

接入时将 `model` 替换为专属模型 code 即可（其余请求结构不变）：

```python
import dashscope

response = dashscope.Generation.call(
    api_key="your-api-key",
    model="your-dedicated-model-code",   # 替换为专属模型 code
    messages=[{"role": "user", "content": "你好"}],
)
print(response.output.text)
```

> **注意**：短时间内请求量快速拉升时，系统需要短暂预热以匹配算力，预热期间部分请求可能出现延迟波动，请做好请求排队或重试机制。

### 生命周期与管理

- **扩缩容**：详情页可随时调整输入/输出 TPM，变配期间服务不中断。
- **续费/退订**：支持到期自动续费（到期前一天 08:00 扣款）；退订不可恢复，退订后专属 code 失效、请求回退公共资源。缩容/退订退费按已用部分 1.5 倍系数结算：`退款 = 降量部分预付费 - (降量部分预付费 × 已用时长/购买时长 × 1.5)`。
- **到期状态**：到期后 2 小时内仍运行中可调用；2~14 小时转为已停止（不可调用、可续费）；14 小时后实例删除，不可恢复。
- **监控**：详情页提供利用率、配额内/外调用次数、缓存命中量等；利用率持续接近 100% 或频繁降级时应扩容。

## 快速模式（Fast mode）：更高的输出速度

[快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md) 面向对输出速度敏感的场景（AI 编程助手、Agent 多步推理、实时对话等），当前处于 **preview 阶段**，能力与规格可能随版本调整。

关键特性：

- **高速输出**：TPS 提升至标准 API 的 1.5~2 倍，达 80~100 TPS。
- **按 token 计费**：计费逻辑与标准 API 一致，按输入/输出 token 计费。
- **特殊限流**：超出 TPM 额度不会立即限流，请求进入排队队列（与 TPM 预留"超额降级按量"的处理方式不同）。

### 使用方式

将 `model` 指定为支持快速模式的 model ID（如 `glm-5.2-fast-preview`）即可开启，无需额外参数。接入域名格式为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`，其中 `workspace_id` 可在[业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management)页面切换到对应地域后查看。

`glm-5.2` 默认返回 `reasoning_content` 思考字段；[流式输出](../concepts/streaming.md)时思考内容与回答内容分别通过 `delta.reasoning_content` 与 `delta.content` 推送：

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ.get("API_KEY"),
    base_url=os.environ.get("BASE_URL"),
)

completion = client.chat.completions.create(
    model="glm-5.2-fast-preview",
    messages=[{"role": "user", "content": "你是谁"}],
    stream=True,
)

for chunk in completion:
    if not chunk.choices:
        continue
    delta = chunk.choices[0].delta
    if hasattr(delta, "reasoning_content") and delta.reasoning_content:
        print(delta.reasoning_content, end="", flush=True)
    if hasattr(delta, "content") and delta.content:
        print(delta.content, end="", flush=True)
```

## 限制与注意事项

- **TPM 预留支持的模型**以控制台展示为准（当前覆盖千问 3.x、GLM-5.x、DeepSeek-v4、Kimi-K2.6 等），部分模型支持长输入阶梯系数与缓存折扣，容量计算器会自动应用；详见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。
- **快速模式当前仅 preview**，支持的模型有限（如 `glm-5.2-fast-preview`），且接入域名与标准 dashscope 域名不同，迁移时需注意 base_url。
- **超额行为差异**：TPM 预留超额自动降级为按量计费、服务不中断；快速模式超额则进入排队队列。二者机制不同，选型时需区分。
- 具体价格、容量起步值、支持模型均**以百炼控制台为准**，文档中的价格表可能随版本变动。

## 来源文档

- [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)
- [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)


