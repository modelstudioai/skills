# model high speed inference

百炼平台针对高吞吐、高速率的推理场景提供两类能力：**TPM 预留**用于为指定模型锁定专属推理容量，避免业务高峰期受公共限流影响；**快速模式（Fast mode）**则针对输出速度敏感的场景提升 TPS。两者都通过替换或指定 `model` 参数接入，无需大改代码。

## TPM 预留：锁定专属容量

TPM（Tokens Per Minute）预留为指定模型锁定专属的推理吞吐量，预留容量内的调用不受公共资源限流影响，容量为业务专属、不与其他用户共享。详见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。

核心特性：

- **专属模型 code**：创建预留后系统自动生成专属模型 code，需将 API 请求中的 `model` 参数替换为该 code 才能使用预留容量。
- **超额不中断**：超出预留容量的请求自动降级为按量计费处理，服务不中断，无需修改代码。可在详情页的**超额降级统计**查看降级次数。
- **计费单位**：按 kTPM 预付费（1 kTPM = 1,000 Tokens/分钟），一次性支付，从购买成功起连续生效。

### 方案选型

[TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 文档给出了多种容量方案的对比，便于按业务诉求选型：

| 方案 | 计费单位 | 容量保障 | 适用场景 | 超额处理 | 代码改动 |
| --- | --- | --- | --- | --- | --- |
| 按量付费 | 按 token | 无（共享公共池） | 流量波动大/短期 | 自动服务，受公共限流 | 无需改动 |
| 资源包/节省计划 | 预付费额度 | 承诺用量折扣（非专属） | 费用优化 | 超出转按量 | 无需改动 |
| TPM 预留 | 按 kTPM 预付费 | 专属容量刚性兑付 | 流量可预估、不能接受限流 | 超出自动降级公共池按量，不中断 | 替换 model 参数 |
| PTU 专属部署 | 按 kTPM 预付费 | 专属部署实例 | 高吞吐高性能 | 超出转按量 | 替换 model 参数 |

### 创建与接入

1. 登录百炼控制台创建 TPM 预留，填写预留名称、选择模型、付费周期（按天）、输入/输出 TPM（单位 kTPM）、购买时长（支持 1~30、60、90、120、365 天）等参数。建议先用 **TPM 容量计算器**（根据 RPM、平均输入/输出长度、缓存命中率估算）确认所需额度。
2. 确认费用后完成支付。
3. 在详情页**概览** Tab 复制**专属模型 code**。
4. 将 API 请求的 `model` 参数替换为该 code 即可：

```python
import dashscope

response = dashscope.Generation.call(
    api_key="your-api-key",
    model="your-dedicated-model-code",   # 替换为专属模型 code
    messages=[{"role": "user", "content": "你好"}],
)
print(response.output.text)
```

> **注意**：短时间内请求量快速拉升时，系统需短暂预热以匹配算力，预热期间部分请求可能出现延迟波动，请做好请求排队或重试机制。

### 容量换算参数

部分模型支持长输入阶梯系数和缓存折扣，容量计算器会自动应用。例如 glm-5.2 输入长度上限 1M、缓存折扣 0.25、无阶梯；glm-5.1 缓存折扣 0.2，且在 [32K, 200K] 区间输入系数 1.33 / 输出 1.17；deepseek-v4-pro 缓存折扣低至 0.08。Qwen3.6-flash-2026-04-16 不支持缓存。

### 管理与生命周期

- **扩缩容**：在详情页调整输入/输出 TPM，变配期间服务不中断。利用率持续接近 100% 或频繁降级时建议扩容。
- **续费**：可手动续订，或开启**到期自动续费**（到期前一天 08:00 自动扣款）。
- **退订**：跳转费用中心完成，退订后专属模型 code 失效、请求回退公共资源，不可恢复。缩容/退订退费按已使用部分 1.5 倍系数结算：`退款 = 降量部分预付费 - (降量部分预付费 × 已用时长/购买时长 × 1.5)`。

预留实例状态：服务到期后 2 小时内仍为**运行中**（可调用、可续费）；2~14 小时转为**已停止**（不可调用、仍可续费）；到期 14 小时后**已过期/删除**，不可恢复。其余状态包括待生效、变配中、已取消。

## 快速模式（Fast mode）：提升输出速度

[快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md) 面向对输出速度敏感的场景（AI 编程助手、Agent 多步推理、实时对话等），当前处于 **preview 阶段**，能力与规格可能随版本调整。

关键特性：

- **高速输出**：TPS 提升至标准 API 的 1.5~2 倍，达 80~100 TPS。
- **按 token 计费**：计费逻辑与标准 API 一致，按输入/输出 token 计费。
- **特殊限流**：超出 TPM 额度不会立即限流，请求进入排队队列。

### 接入方式

将 `model` 参数指定为支持的模型 ID（如 `glm-5.2-fast-preview`）即可开启，无需额外参数。接入域名格式为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`，其中 `{workspace_id}` 可在业务空间管理页面切换到对应地域后查看。

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

glm-5.2 默认返回 `reasoning_content` 思考字段；[流式输出](../concepts/streaming-output.md)时思考内容与回答内容分别通过 `delta.reasoning_content` 与 `delta.content` 推送。

## 限制与注意事项

- **两者定位不同**：TPM 预留解决"容量保障/不受限流"，快速模式解决"输出速率提升"。快速模式仍为 preview，生产环境需评估稳定性。
- **接入差异**：TPM 预留通过替换为专属模型 code 接入标准 dashscope 域名；快速模式使用带 `{workspace_id}` 的 maas 域名并指定 fast-preview 模型 ID。
- **限流行为差异**：TPM 预留超额自动降级按量、不中断；快速模式超额不立即限流而是排队。
- **计费口径**：具体价格、容量换算与费用以百炼控制台为准，[TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 与快速模式的价格表可能随时间调整，请以控制台实时展示为准。

## 来源文档

- [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)
- [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)


