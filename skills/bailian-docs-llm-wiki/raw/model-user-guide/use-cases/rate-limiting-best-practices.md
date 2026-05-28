# 限流应对最佳实践 

百炼 API 按请求数和 Token 用量限流。本文提供从平台配置到客户端流控再到架构兜底的应对方案。

百炼 API 对请求数、Token 用量和增长速率设有限制，即**限流**。大模型请求延迟高，且同时受请求数和 Token 量两个维度约束，单纯"遇错重试"效果有限，需要针对性的流控措施。

本文按改动成本从低到高，介绍三类方案：

-   [平台配置方案](#sec-platform-solutions)（低改动成本）：[服务端排队等待](#sec-wait-timeout)、[提升限流额度](#sec-quota)、[PTU](#sec-ptu)、[Batch API](#sec-batch-api)。
    
-   [客户端流控策略](#sec-strategies)（改客户端代码）：从[基础重试](#h3-l1)到[自适应拥塞控制](#h3-l4)，按工程复杂度递进的四种策略。
    
-   [架构兜底方案](#sec-arch-fallback)（改系统架构）：[模型降级（Fallback）](#sec-fallback)、[基于消息队列（MQ）的削峰填谷](#sec-mq-arch)。
    

如果当前正在解决 `429` 报错，可查看[错误诊断与策略推荐](#sec-diag-table)定位原因。若为突发流量（Traffic Burst）触发，推荐先试[服务端排队等待](#sec-wait-timeout)——只需加一个请求头。

## 平台限流机制

限流按**主账号**维度、**模型**独立计算，触发后通常 1 分钟内恢复。各模型的限流条件和当前用量参见[模型限流条件](https://help.aliyun.com/zh/model-studio/rate-limit)和[模型用量监控](https://help.aliyun.com/zh/model-studio/model-telemetry/)。百炼 API 有以下三种限流规则：

-   **分钟级配额限制（RPM / TPM）**：每分钟允许的最大请求数（Requests Per Minute，RPM）和最大 Token 用量（Tokens Per Minute，TPM）。
    
-   **瞬时频率限制（RPS / TPS）**：每秒允许的最大请求数（RPS）和最大 Token 用量（TPS）。单秒内请求或 Token 消耗过于密集时触发。
    
-   **增速限制（Traffic Burst）**：短时间内请求量或 Token 用量激增时触发。阈值随服务状态动态调整，逐步提升请求量可避免触发。
    

以下从平台配置、客户端流控、架构兜底三个层面介绍应对方案。

## 错误诊断与策略推荐

同一错误码可能由不同限流维度触发。高并发下服务端饱和也可能导致响应变慢或超时，可通过[自适应拥塞控制策略](#h3-l4)缓解。

**错误码 (DashScope / OpenAI)**

**触发维度**

**特征诊断**

**推荐策略**

Throttling.RateQuota / limit\_requests

**请求频率超限**  
（RPM 超限）  

间歇性报错，成功率随时间下降

[令牌桶](#sec-l2)：控制单位时间内的请求配额

**请求频率超限**  
（RPS 超限）  

启动瞬间或并发激增时集中报错

[并发信号量](#sec-l2)或[平滑限速器](#sec-l3)：拉开请求间距

Throttling.AllocationQuota / insufficient\_quota

**Token 用量超限**  
（TPM 超限）  

长文本处理时间歇性报错

[双重令牌桶](#sec-l3)：同时限制 RPM 和 TPM 配额

**Token 用量超限**  
（TPS 超限）  

长文本并发时瞬间 Token 消耗过大

[并发信号量](#sec-l2)或[平滑限速器](#sec-l3)

Throttling.BurstRate / limit\_burst\_rate

**流量增速超限**  
（Traffic Burst）  

启动或空闲恢复后突然发起大量请求

推荐首选[服务端排队等待](#sec-wait-timeout)；或令牌桶设置低初始值（如 `initial_tokens=0`）实现冷启动缓起；或使用[平滑限速器](#sec-l3)削峰

## 平台配置方案

以下方案依赖平台能力，客户端改动极少或无需改动。

### 服务端排队等待（推荐首选）

针对增速/突发限流（Traffic Burst），百炼支持在请求头中声明最大等待时间。服务端收到后，在指定时间内排队重试，直到请求开始处理或超时。相比直接返回 429，该机制可显著提升突发流量下的成功率。

**说明**

该功能仅适用于增速/突发限流（Throttling.BurstRate），不适用于 RPM/TPM 绝对值限流。

**配置方式**

在请求头中添加 `X-DashScope-Wait-Timeout` 字段：

**Header 字段**

**示例**

**说明**

X-DashScope-Wait-Timeout

30

突发请求的最大排队等待时间，单位为秒。

-   值为 `0`：不排队，直接返回 429。
    
-   值大于等于模型最大响应时间：不生效。
    
-   建议值：3~120 秒。
    

**超时时间配置**

配置排队等待后，需相应调整客户端超时时间，避免因叠加排队时间导致连接提前关闭：

-   **非流式请求**（stream: false）：超时时间 = 原基础超时时间 + Wait-Timeout 值。
    
-   **流式请求**（stream: true）：超时时间 > Wait-Timeout 值。流式请求在收到首个 chunk 后开始计时，只需确保首次响应超时大于排队时间。
    

例如：原基础超时时间为 120 秒，Wait-Timeout 设为 30 秒，则非流式请求的超时时间应设为 150 秒。

**代码示例**

## OpenAI Python SDK

```
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    timeout=150.0,  # 原超时 120s + 排队等待 30s
)

response = client.chat.completions.create(
    model="qwen-plus",
    messages=[{"role": "user", "content": "Hello"}],
    extra_headers={
        "X-DashScope-Wait-Timeout": "30"  # 最大排队等待 30 秒
    }
)
print(response.choices[0].message.content)
```

## curl

```
curl -X POST "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -H "X-DashScope-Wait-Timeout: 30" \
  -d '{
    "model": "qwen-plus",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

### 提升限流额度

默认额度不足时，可在百炼控制台直接提升临时限流额度，提交后立即生效。目前支持华北2（北京）和新加坡地域。

适用场景：业务增长导致 RPM/TPM 配额不足，或短期活动需临时提升吞吐量。操作详情参见[限流](https://help.aliyun.com/zh/model-studio/rate-limit#h2-temp-limit-raise)。

操作简单，建议在尝试客户端流控前优先评估。

### 预置吞吐单元（PTU）

[PTU 服务](https://help.aliyun.com/zh/model-studio/model-deployment-introduction)提供独立预留的专享算力，可避免公共资源池的竞争，是保障实时高吞吐的首选。

适用场景：业务对吞吐量有确定性要求（如 SLA 承诺），或希望免去客户端流控开发，直接获得稳定高吞吐。

PTU 为预留资源，未满负荷使用也持续计费。建议根据实际峰值评估规格，避免闲置浪费。

### 异步批处理（Batch API）

数据清洗、离线分析等无实时性要求的任务，可使用 [Batch API](https://help.aliyun.com/zh/model-studio/batch-inference) 批量提交。任务在低峰期异步执行，不受在线限流约束。

适用场景：数据标注、日志分析、批量摘要等允许数小时至数天返回结果的任务。费用通常低于实时 API。

结果返回时间不确定，不适用于需即时响应的在线业务。提交后需通过轮询或回调获取结果。

## 客户端流控策略

当平台方案（如[服务端排队等待](#sec-wait-timeout)、提升额度等）无法满足需求时，需在客户端引入流控。核心原则：**将请求均匀分布在时间窗口内**，避免突发触发限流。系统启动或长时间空闲后，应逐步提升并发而非瞬间拉满。

以下四种策略按工程复杂度递增，每种包含上一级能力并增强：

-   基础重试仅做被动防御；
    
-   请求速率限制加入主动排队；
    
-   流量整形进一步引入 Token 维度管控和平滑发送；
    
-   自适应拥塞控制则基于实时反馈动态调整发送速率。
    

在满足业务需求的前提下，优先选择实现成本更低的策略。

### **各策略的吞吐量表现对比**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0844336771/p1067109.png)

四种策略在不同负载下的吞吐量表现：

-   **基础重试策略**：低负载下有效，高并发下易触发拥塞崩溃，吞吐量断崖式下降。
    
-   **请求速率限制策略**：防崩溃能力强，但长文本混合负载下因缺乏 Token 管控，吞吐量呈锯齿状波动。
    
-   **流量整形策略**：稳定性高，以牺牲部分峰值吞吐换取平稳输出。
    
-   **自适应拥塞控制策略**：高负载下可动态收敛至稳定高吞吐点，但存在冷启动探测开销。
    

### 基础重试策略

适用于个人测试、本地脚本等低并发场景。不限制发送速率，仅在收到 `429` 或 `5xx` 时触发带随机抖动的指数退避重试。

没有前置流量控制，多线程并发下易触发限流并导致请求积压。

**代码示例**

## 使用 tenacity 库

```
import openai
from openai import OpenAI
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
    retry_if_exception_type
)

RETRYABLE_ERRORS = (
    openai.RateLimitError,
    openai.InternalServerError,
    openai.APIConnectionError,
)

@retry(
    wait=wait_random_exponential(min=1, max=60),
    stop=stop_after_attempt(6),
    retry=retry_if_exception_type(RETRYABLE_ERRORS)
)
def chat_with_retry(client, model, messages, max_tokens):
    return client.chat.completions.create(
        model=model,
        max_tokens=max_tokens,
        messages=messages
    )

client = OpenAI(
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key="YOUR_DASHSCOPE_API_KEY"
)

try:
    response = chat_with_retry(
        client=client,
        model="qwen-plus",
        messages=[{"role": "user", "content": "什么是指数退避重试？"}],
        max_tokens=1024
    )
    print(response.choices[0].message.content)
except Exception as e:
    print(f"请求失败: {e}")
```

## 原生实现（无依赖）

```
import time
import random
import openai
from openai import OpenAI

RETRYABLE_ERRORS = (
    openai.RateLimitError,
    openai.InternalServerError,
    openai.APIConnectionError,
)

def chat_with_retry(client, model, messages, max_tokens):
    attempt = 0
    max_retries = 5
    base_delay = 1
    max_delay = 60

    while attempt <= max_retries:
        try:
            return client.chat.completions.create(
                model=model,
                max_tokens=max_tokens,
                messages=messages
            )
        except RETRYABLE_ERRORS as e:
            attempt += 1
            if attempt > max_retries:
                raise e
            backoff = min(max_delay, base_delay * (2 ** (attempt - 1)))
            sleep_time = backoff + random.uniform(0, 1)
            print(f"触发 {type(e).__name__}，等待 {sleep_time:.2f}s 后重试...")
            time.sleep(sleep_time)

client = OpenAI(
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key="YOUR_DASHSCOPE_API_KEY"
)

try:
    response = chat_with_retry(
        client=client,
        model="qwen-plus",
        messages=[{"role": "user", "content": "什么是指数退避重试？"}],
        max_tokens=1024
    )
    print(response.choices[0].message.content)
except Exception as e:
    print(f"请求失败: {e}")
```

上述代码使用指数退避而非固定间隔重试。**固定间隔重试**会让所有失败请求同时重发，再次触发限流。**指数退避 + 随机抖动**将重试打散：

-   **等待时间逐步翻倍**：如 `1s：2s：4s...`，避免短时间内反复请求。
    
-   **加入随机抖动**：引入随机值（如 `2s +/- 0.5s`）打散重试流量，防止"扎堆"重试形成二次洪峰（惊群效应）。
    

系统以分散方式恢复，避免"失败—集体重试—再次失败"的恶性循环。

### 请求速率限制策略

被动重试难以应对真实业务流量，频繁重试增加延迟。该策略引入**主动流控**：请求发出前先自检，将无序涌入的请求梳理成符合 RPM 限额的队列。主动平滑带来少量可控的排队延迟，但远低于”报错—等待—重试”循环的代价——**用确定的小代价，避免不确定的大延迟**。

适用于 Chatbot 等轻量交互、对首字延迟敏感的在线服务。

客户端主动排队分两级控制：

-   **RPM 令牌桶**：限制每分钟请求总数。桶容量即 RPM 配额，令牌恒定速率填充。支持预支：令牌不足时可透支未来额度，严格 FIFO。
    
-   **并发信号量**：限制并发请求数，防止瞬时高并发触发 RPS 限制。
    

两级控制必须**先获取 RPM 令牌，再获取并发信号量**。并发槽位是稀缺资源，只应分配给已满足执行条件的请求。若顺序颠倒，高负载下会引发**队头阻塞**——请求占住槽位却无令牌可用，所有槽位被占满但无请求发出。原则：持有稀缺资源时，不做长耗时等待。

下方代码将令牌桶初始化为满桶（`initial_tokens=rpm_limit`），适合在线服务启动时立即处理请求。若满桶启动触发限流，可降低初始值（如 `initial_tokens=0`，空桶启动），使系统以更平缓的速率进入工作状态。

该策略不追踪 Token 用量，长文本任务中仍可能耗尽 TPM 配额。

**代码示例**

## 核心组件：令牌桶

```
import time

class TokenBucket:
    """
    令牌桶实现，用于控制每分钟请求数 (RPM)。
    支持预支 (Debt) 机制，以保证高并发下的先进先出 (FIFO) 顺序。
    """
    def __init__(self, quota_per_minute: float, initial_tokens: float = 0.0):
        self.capacity = quota_per_minute
        self.tokens = initial_tokens
        self.refill_rate = quota_per_minute / 60.0
        self.last_refill = time.monotonic()

    def reserve(self, cost: float = 1.0) -> float:
        """
        申请令牌。
        如果令牌不足，返回需要等待的秒数（支持预支）。
        """
        self._refill()

        # 1. 令牌充足：直接扣除
        if self.tokens >= cost:
            self.tokens -= cost
            return 0.0

        # 2. 令牌不足：计算等待时间并预支
        # 为当前请求"预定"了未来的令牌，确保 FIFO 顺序
        deficit = cost - self.tokens
        wait_seconds = deficit / self.refill_rate
        self.tokens -= cost
        return wait_seconds

    def _refill(self):
        """根据流逝时间补充令牌"""
        now = time.monotonic()
        elapsed = now - self.last_refill
        if elapsed > 0:
            self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
            self.last_refill = now
```

## 客户端逻辑

```
import asyncio
import openai
from openai import AsyncOpenAI
from tenacity import retry, wait_random_exponential, stop_after_attempt, retry_if_exception_type

class RateLimitedClient:
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1",
        rpm_limit: float = 600.0,
        max_concurrency: int = 20
    ):
        self.client = AsyncOpenAI(api_key=api_key, base_url=base_url)
        # 组件 1: RPM 令牌桶 (控制总量)
        self.rpm_bucket = TokenBucket(
            quota_per_minute=rpm_limit,
            initial_tokens=rpm_limit  # 满桶启动，适合轻量在线服务
        )
        # 组件 2: 并发信号量 (控制瞬间并发)
        self.semaphore = asyncio.Semaphore(max_concurrency)

    async def _execute_request(self, model, messages, max_tokens):
        """执行单个请求：依次通过 RPM 检查和并发限制。"""
        # 1. RPM 检查 (先拿令牌)
        wait_seconds = self.rpm_bucket.reserve(1.0)
        if wait_seconds > 0:
            await asyncio.sleep(wait_seconds)
        # 2. 并发检查 (再拿信号量)
        async with self.semaphore:
            # 3. 发起 API 调用
            return await self.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens
            )

    @retry(
        wait=wait_random_exponential(min=1, max=60),
        stop=stop_after_attempt(5),
        retry=retry_if_exception_type((
            openai.RateLimitError,
            openai.InternalServerError,
            openai.APIConnectionError
        ))
    )
    async def chat_with_limit(self, model, messages, max_tokens=1024):
        # 设计考量：为什么重试也要重新拿 Token？
        # 答：为了安全。如果不重新拿，重试带来的流量脉冲
        # 可能会瞬间突破 RPM 限制
        return await self._execute_request(model, messages, max_tokens)
```

### 流量整形策略

RAG 实时入库、长文档批量分析等高稳吞吐场景中，请求速率限制存在 **TPM 盲区**。流量整形策略升级为**双重资源感知（RPM & TPM）**，并在发送端引入整形机制，将突发脉冲削峰填谷为平滑流速。

在请求速率限制基础上，增强了以下能力：

-   **双重资源管控（RPM & TPM）**：同时维护 RPM 和 TPM 令牌桶，所有请求在发出前必须通过两个维度的配额检查。
    
-   **输入事前预扣，输出事后结算**：模型输出长度请求前未知。TPM 令牌桶发送时仅预扣输入 Token，完成后结算实际输出。即使结算后令牌为负，后续请求也会等待回正，自然平滑流速。
    
-   **匀速预热**：冷启动期间，令牌发放速率随时间线性增长，消除初始突发风险。
    
-   **平滑限速**：通过强制请求间保持最小间隔（Pacing），平滑发送速率，降低触发速率限制的风险。
    

**备选方案**：若业务对启动时的微小排队延迟不敏感，可复用标准令牌桶（设 `initial_tokens=0`）实现安全启动，降低客户端复杂度。Python 令牌桶仅用于演示思路，生产环境建议使用成熟限流组件（如 Java Guava 的 `SmoothRateLimiter`）。

代码示例中平滑等待置于并发锁**内部**。多个请求可能在等待结束后同时竞争信号量，导致流量在出口再次拥堵。锁内平滑虽轻微降低并发效率，但能确保发送间隔可控。

完整的流量整形链路为：`预估输入 Token → 双重准入（RPM & TPM）→ 并发锁 → 平滑整形 → 发送 → 输出 Token 结算`。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0844336771/p1067110.png)

该策略采用保守平滑机制，会牺牲部分峰值并发，不适用于极致低延迟的在线服务。

**代码示例**

## 进阶令牌桶

```
import time

class TokenBucket:
    """进阶令牌桶，支持匀速预热 (Continuous Warm-up) 机制。"""
    def __init__(self, quota_per_minute: float, warmup_seconds: float = 0.0):
        self.capacity = quota_per_minute
        self.tokens = 0.0
        self.target_refill_rate = quota_per_minute / 60.0
        self.warmup_seconds = warmup_seconds
        self.start_time = time.monotonic()
        self.last_update_time = self.start_time
        self.cumulative_generated = 0.0

    def _get_cumulative_tokens(self, t: float) -> float:
        if t <= 0:
            return 0.0
        R = self.target_refill_rate
        T = self.warmup_seconds
        if T <= 0:
            return R * t
        if t <= T:
            return (R / (2 * T)) * (t ** 2)
        else:
            warmup_total = (R * T) / 2.0
            return warmup_total + R * (t - T)

    def _get_time_for_cumulative_tokens(self, target_cumulative: float) -> float:
        if target_cumulative <= 0:
            return 0.0
        R = self.target_refill_rate
        T = self.warmup_seconds
        if T <= 0:
            return target_cumulative / R
        warmup_total = (R * T) / 2.0
        if target_cumulative <= warmup_total:
            return ((2 * T * target_cumulative) / R) ** 0.5
        else:
            return (target_cumulative - warmup_total) / R + T

    def reserve(self, cost: float = 1.0) -> float:
        now = time.monotonic()
        relative_now = now - self.start_time
        current_cumulative = self._get_cumulative_tokens(relative_now)
        new_tokens = current_cumulative - self.cumulative_generated
        self.tokens = min(self.capacity, self.tokens + new_tokens)
        self.cumulative_generated = current_cumulative
        self.last_update_time = now
        if self.tokens >= cost:
            self.tokens -= cost
            return 0.0
        deficit = cost - self.tokens
        self.tokens -= cost
        target_cumulative = self.cumulative_generated + deficit
        target_time = self._get_time_for_cumulative_tokens(target_cumulative)
        wait_seconds = target_time - relative_now
        return max(0.0, wait_seconds)

    def adjust(self, amount: float):
        self.tokens = min(self.capacity, self.tokens + amount)
```

## 平滑限流器

```
import time

class SmoothRateLimiter:
    def __init__(self, rate_per_minute: float):
        self._min_interval = 60.0 / rate_per_minute
        self._last_operation = time.monotonic()

    def reserve(self) -> float:
        now = time.monotonic()
        elapsed = now - self._last_operation
        wait_time = max(0.0, self._min_interval - elapsed)
        self._last_operation = now + wait_time
        return wait_time
```

## 客户端逻辑

```
import asyncio

class TrafficShapingClient:
    def __init__(self):
        self._rpm_bucket = TokenBucket(quota_per_minute=600)
        self._tpm_bucket = TokenBucket(quota_per_minute=1_000_000)
        self._smooth_limiter = SmoothRateLimiter(rate_per_minute=600)
        self._concurrency_semaphore = asyncio.Semaphore(20)

    async def _execute_throttled_request(self, model, prompt, max_tokens, input_tokens):
        # [步骤 1] 双重准入控制 (Parallel Admission)
        # 同时检查 RPM 和 TPM，取两者中较长的等待时间
        wait_rpm = self._rpm_bucket.reserve(1.0)
        # TPM 检查仅针对输入 Token 申请额度
        wait_tpm = self._tpm_bucket.reserve(input_tokens)
        admission_wait = max(wait_rpm, wait_tpm)
        if admission_wait > 0:
            await asyncio.sleep(admission_wait)

        # [步骤 2] 获取并发锁 (Concurrency Lock)
        async with self._concurrency_semaphore:
            # [步骤 3] 流量整形 (Traffic Shaping)
            # 关键：在锁内进行平滑等待
            # 牺牲部分并发效率，换取发送间隔的精准可控
            smooth_wait = self._smooth_limiter.reserve()
            if smooth_wait > 0:
                await asyncio.sleep(smooth_wait)

            # [步骤 4] 发送请求
            content, actual_usage = await self._send_chat_request(model, prompt, max_tokens)

            # [步骤 5] 输出 Token 结算
            output_tokens = actual_usage.completion_tokens
            if output_tokens > 0:
                self._tpm_bucket.adjust(-output_tokens)
            return content
```

### 自适应拥塞控制策略

适用于 API 网关、复杂代理、多租户等大规模动态负载场景。

**说明**

**选型提示：该策略并非通用方案**

该策略的价值在于应对**高度不确定**与**剧烈波动**的环境，并非普适选择：

-   **性能悖论**：若负载可预测（如定量批处理），直接设定最优静态参数通常优于需要"试探与收敛"的动态探测。
    
-   **探测损耗**：动态算法必然伴随冷启动爬坡与试探波动，在可知场景下是不必要的性能损耗。
    
-   **维护成本**：闭环反馈机制增加系统复杂度与排查难度。
    

除非业务**规模极大、负载复杂且波动显著**，否则优先选择更简单的前三种策略。

请求速率限制和流量整形基于**静态配额**，负载稳定时完全适用。但在网关级场景下，下游负载复杂多变（短请求与深度推理交织），平台阈值也动态波动，静态策略难以兼顾效率与稳定。

该策略借鉴 [BBR](https://cacm.acm.org/practice/bbr-congestion-based-congestion-control)，建立基于 **EBP（Elastic Bandwidth Probing）** 的闭环控制系统。以 RPM/TPM 配额为指导上限，根据实时反馈（延迟、限流信号）动态计算最佳发送速率。

-   **弹性探测（EBP）**：记忆历史最高成功水位，根据当前并发与最高水位的距离模拟弹簧张力计算探测增益（距离远加速，近减速）。叠加微小线性推力确保高饱和区仍能探索边界。
    
-   **TPT 拥塞感知**：大模型生成耗时与长度成正比，长文本延迟高不代表拥塞。使用 TPT（Time Per Token）作为指标，滤除内容长度噪声，仅在 TPT 显著恶化时判定为计算饱和。
    
-   **防突发调速器**：无论 EBP 算出的目标多高，调速器强制限制并发增长加速度，确保流量平滑上升，避免阶梯跳变触发增速限制。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0844336771/p1067112.png)

相较于原生 BBR，针对大模型特性做了以下改造：

-   **指导性探测**：引入已知的 RPM/TPM 配额作为"指导上限"，避免盲目试探导致的频繁撞墙。
    
-   **信号源改造（RTT → TPT）**：原生 BBR 依赖 RTT，但大模型中内容长度带来的延迟差异远大于网络抖动，改用 TPT 剔除干扰。
    
-   **响应机制强化（ProbeRTT → Hold）**：面对延迟波动，选择保持当前并发水平，而非主动退避降低吞吐。
    
-   **硬限流响应（Packet Loss → 429 Drain）**：一旦触发 `429` 错误，进入激进的 Drain 状态，冷却期结束后执行快速恢复。
    

局限：

-   **TPT 噪点**：当前 TPT 按"总延迟 / 总 Token 数"粗估，混入了网络往返、排队与首字生成耗时，易受抖动或长输入干扰而虚高，可能误触发 Hold 状态。
    
-   **大请求饥饿**：为追求调度性能采用了非严格 FIFO 唤醒机制，配额紧缺时短 Token 请求可能抢占资源，导致长 Token 请求等待过长。
    
-   **冷启动**：需要预热时间建立统计模型，低负载或短时任务中吞吐量可能低于前三种策略。
    

**代码示例**

## 控制入口

```
class ElasticCongestionController:
    async def acquire(self):
        """[准入阶段] 请求发起前的检查"""
        # 1. SSR 慢启动重启：若空闲太久，主动衰减上限
        #    防止过时水位导致的突发流量
        if self.is_idle_too_long():
            self.perform_slow_start_restart()

        # 2. 熔断检查：若处于 DRAIN (冷却) 状态，强制等待
        if self.state == CongestionState.DRAIN:
            await self.wait_for_cooldown()

        # 3. 双重预算检查：同时检查并发槽位和 Token 预算
        await self.wait_for_budget(request_tokens)

    async def release(self, latency, actual_tokens, error):
        """[反馈阶段] 请求结束后的决策"""
        if error:
            # [故障响应] 遇限流错误 (429/503)：立即排水 + 乘性回退
            self.state = CongestionState.DRAIN
            self.concurrency_limit *= self.backoff_factor  # e.g. 0.7
            return

        # [正常响应] 计算 TPT (Time-Per-Token)
        current_tpt = latency / actual_tokens

        # [拥塞感知] TPT 突增 (生成变慢)：进入 HOLD 观察
        # 维持并发水平，不退避也不增长
        if current_tpt > self.metrics.ema_tpt * 2.0:
            self.state = CongestionState.HOLD
        else:
            # [稳态探测] 网络健康：执行 EBP 弹性探测
            self.state = CongestionState.PROBING
            self.update_limit_via_ebp()
```

## EBP 探测

```
def probe_next_limit(self, current_limit, max_known_capacity):
    """
    计算下一个并发上限
    核心公式：Next = Max(弹簧张力, 线性推力) + 调速器平滑
    """
    # 1. 计算物理上限 (Little's Law)
    # 理论上限 = 吞吐量 * 延迟 * 缓冲因子
    dynamic_ceiling = self.metrics.tps * self.metrics.avg_latency * 1.2

    # 2. 弹簧逻辑 (Spring Tension)
    # 距离历史最高水位越远，张力越大（加速）；越近则越小（减速）
    tension = 1.0 - (current_limit / max_known_capacity)
    spring_target = current_limit * (1.0 + tension * gain)

    # 3. 线性推力 (Additive Thrust)
    # 解决"芝诺悖论"：张力趋近于 0 时，强制叠加微小线性增量
    # 确保系统能突破局部极值，持续探索边界
    linear_target = current_limit + self.min_additive_step

    raw_target = max(spring_target, linear_target)

    # 4. 防突发调速器 (Rate Governor)
    # 限制并发增长的加速度，防止阶梯跳变
    final_limit = self.governor.smooth(raw_target)

    return min(final_limit, dynamic_ceiling)
```

## 统计追踪

```
class CongestionMetrics:
    def update_stats(self, latency, token_count):
        """
        [传感器] 实时更新统计指标
        使用 EMA (指数移动平均) 滤除长尾请求的噪声
        """
        alpha = 0.2  # 平滑因子

        # 1. 估算单请求大小 (Token Size)
        self.ema_tokens = (1 - alpha) * self.ema_tokens + alpha * token_count

        # 2. 估算 TPT (Time Per Token)
        # 用 TPT 代替 Latency，消除 LLM 生成长度不同带来的误差
        instant_tpt = latency / token_count
        self.ema_tpt = (1 - alpha) * self.ema_tpt + alpha * instant_tpt

    def track_inflight(self, estimated_tokens):
        """
        [盲区填充] 修正"响应后才计数"的滞后性
        请求发起瞬间，立即预扣额度
        """
        self.inflight_tokens += estimated_tokens
```

## 架构兜底方案

当平台配置和客户端流控仍无法满足可用性或峰值吞吐要求时，可在架构层面引入兜底。

### 模型降级（Fallback）

主模型因限流或异常无法响应时，自动回退至配额宽裕的备选模型，保障主流程持续可用。

**降级链路设计原则**

-   **选择不同系列的模型**：百炼限流按模型独立计算，可选不同模型作为备选，例如 `qwen3.6-plus` 降级至 `qwen3.6-flash`。
    
-   **仅限流错误时降级**：降级针对 `429` 限流错误，网络超时或参数错误切换模型无法解决。
    
-   **备选模型需提前验证**：确保备选模型支持业务所需功能（如 Function Calling、结构化输出），避免降级后功能异常。
    

**代码示例**

以下示例演示了基于 429 错误码的模型降级逻辑：主模型请求触发限流时，自动切换至备选模型重试。

```
import os
import asyncio
from openai import AsyncOpenAI, APIStatusError

# 主模型与备选模型（不同系列，独立配额）
PRIMARY_MODEL = "qwen3.6-plus"
FALLBACK_MODEL = "qwen3.6-flash"

client = AsyncOpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

async def chat_with_fallback(messages: list) -> str:
    """带降级的请求：主模型限流时自动切换备选模型。"""
    for model in [PRIMARY_MODEL, FALLBACK_MODEL]:
        try:
            response = await client.chat.completions.create(
                model=model,
                messages=messages
            )
            return response.choices[0].message.content
        except APIStatusError as e:
            if e.status_code == 429 and model == PRIMARY_MODEL:
                print(f"[限流触发] {model}，降级至 {FALLBACK_MODEL}")
                continue
            raise
    raise RuntimeError("所有模型均不可用")

async def main():
    result = await chat_with_fallback(
        messages=[{"role": "user", "content": "你好"}]
    )
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

模型降级可与客户端流控策略组合使用。例如，在[请求速率限制策略](#sec-l2)的重试逻辑中集成降级判断：当重试次数耗尽仍触发限流时，切换至备选模型。

### 基于消息队列（MQ）的削峰填谷

不要求即时响应的后端业务，可引入消息中间件（如 RabbitMQ、Kafka）削峰。突发流量先写入 MQ，消费端按限流配额匀速拉取处理，从根本上解耦前端峰值与后端调用。

适用场景：用户提交任务后可异步通知结果的业务，如工单处理、内容审核、批量标注等。

设计要点：

-   **消费速率控制**：消费端应配合[请求速率限制](#sec-l2)或[流量整形](#sec-l3)策略，按 RPM/TPM 配额匀速消费，而非无限制地拉取消息。
    
-   **死信处理**：多次重试仍失败的消息转入死信队列并告警，避免无限重试阻塞消费。
    
-   **背压传递**：MQ 积压超阈值时向上游反馈压力（如返回排队状态），避免队列无限增长。
    

## 生产环境注意事项

上述示例基于 Python asyncio 单线程循环，用于演示核心算法。大规模生产前需关注以下问题。

-   **非文本模型的适配**
    
    上述策略以文本模型为例，核心思想同样适用于多模态模型（图像生成、语音合成等）。计量单位不同，但本质均为限制提交速率和处理容量：
    
    -   语音识别等模型：通常受单位时间内请求数（如 RPM）和用量（如音频时长）双重约束，策略与文本模型基本一致。
        
    -   图片/视频等模型：通常受任务提交速率和并发任务数约束。可沿用请求速率限制策略的思路，限制任务提交速率并配合信号量控制并发数。
        
    
    无论限流指标如何变化，客户端主动流控的原则不变。只需将计数器或探测指标替换为对应模态的指标。具体规则参见[模型限流条件](https://help.aliyun.com/zh/model-studio/rate-limit)。
    
-   **并发模型的原子性**
    
    示例：`asyncio` 单线程协作式调度，状态修改天然原子，单进程内无需额外并发保护。
    
    生产建议：多线程或多进程环境需确保令牌桶及统计窗口的并发安全，否则竞态条件会导致流控失效。
    
-   **分布式限流**
    
    示例：流控组件均为本地内存实现。
    
    生产建议：多实例部署中各实例独立流控，实际总用量可能超标。建议使用中心化计数器（如 Redis）统一管控。
    
-   **优先级队列与饥饿预防**
    
    示例：均未实现优先级区分。自适应拥塞控制策略为追求调度性能采用了非严格 FIFO 唤醒。
    
    生产建议：业务存在高低优先级请求时，建议实现加权优先级队列保障高优带宽，同时为低优队列保留最小配额防止饥饿。
