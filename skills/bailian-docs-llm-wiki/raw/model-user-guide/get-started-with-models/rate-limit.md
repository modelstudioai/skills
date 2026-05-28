# 限流

百炼按主账号维度对模型调用设置限流，账号下所有RAM子账号、业务空间和API Key 的调用量合并计算。超出限制时请求会被拒绝，通常在一分钟内自动恢复。

## 限流规则

-   **账号级别限流**：限流按主账号维度计算，账号下所有RAM子账号、业务空间和API Key 的调用量合并计算。
    
-   **模型独立限流**：不同模型限流额度相互独立，具体参见下方表格。
    

## FAQ

### 为什么触发限流？

根据错误信息判断触发了哪类限流：

-   `Requests rate limit exceeded` 或 `You exceeded your current requests list`：触发了每分钟请求数（RPM）限流。
    
-   `Allocated quota exceeded` 或 `You exceeded your current quota`：触发了每分钟 Token 消耗（TPM）限流。
    
-   `Request rate increased too quickly`：请求频率在短时间内激增，触发了系统稳定性保护——即使总调用量未达到 RPM 或 TPM 上限也会触发。
    
-   其他报错，参见[错误码](https://help.aliyun.com/zh/model-studio/error-code)确认原因。
    

除 RPM 和 TPM 外，限流策略可能按秒级 RPS（RPM/60）与 TPS（TPM/60）执行。即使每分钟总调用量未超限，短时间内的请求爆发也可能触发限流。

### 如何查看模型调用量？

模型调用完**一小时后**，在模型监控（[北京](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)或[新加坡](https://modelstudio.console.aliyun.com/?tab=model#/model-telemetry)）页面设置查询条件（例如，选择时间范围、业务空间等），再在**模型列表**区域找到目标模型并单击**操作**列的**监控**，即可查看该模型的调用统计结果。具体请参见[模型监控](https://help.aliyun.com/zh/model-studio/model-telemetry/)文档。

> 数据按小时更新，高峰期可能有小时级延迟，请您耐心等待。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6923304571/p992753.png)

### 遇到限流后多久恢复？

通常在一分钟内恢复。如出现其他报错，参见[错误码](https://help.aliyun.com/zh/model-studio/error-code)进行处理。

### 如何避免限流？

1.  **选用高限流模型**
    
    -   优先使用 [qwen-plus](https://help.aliyun.com/zh/model-studio/models#6c45e49509gtr) 等限流额度更高的模型。
        
    -   稳定版或最新版比带日期的快照版本限流更宽松。
        
2.  **优化调用策略**
    
    -   **降低调用频率**：收到 `Requests rate limit exceeded` 或 `You exceeded your current requests list` 时，降低API调用频率。
        
    -   **减少 Token 消耗**：收到 `Allocated quota exceeded` 或 `You exceeded your current quota` 时，缩短输入或限制输出长度。
        
    -   **平滑请求速率**：收到 `Request rate increased too quickly` 时，采用匀速调度、指数退避或请求队列将请求均匀分散，避免瞬时高峰。
        
3.  **添加备选模型**
    
    触发限流后切换到备用模型继续生成，可降低失败概率、提升吞吐量。以下代码在调用 `qwen-plus-2025-07-28` 触发限流后，自动改用 `qwen-plus-2025-07-14` 重试。
    
    **示例代码**
    
    ```
    import os
    import asyncio
    from openai import AsyncOpenAI, APIStatusError
    
    # 配置
    API_KEY = os.getenv("DASHSCOPE_API_KEY")
    # 主用模型
    MODEL = "qwen-plus-2025-07-28"
    # 备选模型
    BACKUP_MODEL = "qwen-plus-2025-07-14"
    # 测试问题
    QUESTION = "你是谁？"
    # 并发设置
    NUM_REQUESTS = 10
    
    client = AsyncOpenAI(
        api_key=API_KEY,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    )
    
    async def send_request(model):
        """发送单个请求"""
        try:
            await client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": QUESTION}]
            )
            return True
        except APIStatusError as e:
            if e.status_code == 429:
                print(f"[限流触发] 模型 {model}")
                return False
            raise
        except Exception as e:
            print(f"[请求失败] 模型 {model}，错误：{e}")
            return False
    
    async def task(i):
        # 尝试主模型
        if await send_request(MODEL):
            return True
        # 限流时尝试备用模型
        return await send_request(BACKUP_MODEL)
    
    async def main():
        results = await asyncio.gather(*(task(i) for i in range(NUM_REQUESTS)))
        print(f"成功请求: {sum(results)}, 失败请求: {len(results) - sum(results)}")
    
    if __name__ == "__main__":
        asyncio.run(main())
    ```
    
4.  **拆分任务**：长对话或大型文档会快速消耗大量 Token。将大批量任务拆分为小批次，分时段提交。
    
5.  **批量推理**：无需实时响应时，使用[批量推理](https://help.aliyun.com/zh/model-studio/batch-inference)（Batch API）。批量请求不受实时限流约束，但需考虑排队和处理时间。
    
6.  **提升限流额度**：默认限流额度不足时，在百炼控制台的**限流提额**页面提升模型的临时 TPM 额度，提交后立即生效。详见[提升临时限流额度](#h2-temp-limit-raise)。
    

## 提升临时限流额度

默认限流额度不足时，可在百炼控制台提升模型的临时 TPM 额度。提交后立即生效，有效期 30 天，到期后自动恢复为系统默认值。

目前支持华北2（北京）和新加坡地域。

1.  登录百炼控制台，进入[限流提额](https://bailian.console.aliyun.com/?tab=model#/efm/temp_limit_raise)页面。
    
2.  单击页面右上角的**提升模型临时限流额度**。
    
3.  在弹窗中选择**模型**，填写期望的 **Token 账号限流（Token/60 秒）**值。弹窗中会显示当前额度和可设置上限。
    
4.  单击**确定**，提额立即生效。
    

提额生效后，可通过以下方式确认：

-   在[限流提额](https://bailian.console.aliyun.com/?tab=model#/efm/temp_limit_raise)页面的列表中，查看已提额的模型及对应限流数据。
    
-   在[模型广场](https://bailian.console.aliyun.com/?tab=model#/model-market/all)中进入对应模型的详情页，查看更新后的限流数据。
    

**说明**

-   支持临时提额的模型以[限流提额](https://bailian.console.aliyun.com/?tab=model#/efm/temp_limit_raise)页面弹窗的可选列表为准。
    
-   对已提额的模型再次提交视为重新申请，有效期随之重置为 30 天。
    
-   按实际需求申请额度。若配置容量长期显著超过实际使用量，系统可能在提前通知后将其恢复为默认值。
    

## **文本生成-千问**

### **千问语言模型**

## **中国内地**

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

qwen3.7-max

30,000

5,000,000

qwen3.7-max-2026-05-20

600

1,000,000

qwen3.7-max-preview

60

500,000

qwen3.7-max-2026-05-17

60

500,000

qwen3.6-max-preview

600

1,000,000

qwen3-max

30,000

5,000,000

qwen3-max-2026-01-23

600

1,000,000

qwen3-max-2025-09-23

60

100,000

qwen3-max-preview

600

1,000,000

qwen-max

> 用[Batch API](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)调用服务时，不受限流限制。

1,200

qwen-max-latest

qwen-max-2025-01-25

（qwen-max-0125）

60

100,000

qwen-max-2024-09-19

（qwen-max-0919）

qwen-max-2024-04-28

（qwen-max-0428）

qwen3.6-plus

30,000

5,000,000

qwen3.6-plus-2026-04-02

600

1,000,000

qwen3.6-flash

30,000

10,000,000

qwen3.6-flash-2026-04-16

600

1,000,000

qwen3.5-plus

30,000

5,000,000

qwen3.5-plus-2026-04-20

600

1,000,000

qwen3.5-plus-2026-02-15

600

1,000,000

qwen-plus

> 用[Batch API](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)调用服务时，不受限流限制。

30,000

5,000,000

qwen-plus-latest

15,000

1,200,000

qwen-plus-2025-12-01

120

1,000,000

qwen-plus-2025-09-11

60

qwen-plus-2025-07-28

（qwen-plus-0728）

qwen-plus-2025-07-14

（qwen-plus-0714）

100,000

qwen-plus-2025-04-28

（qwen-plus-0428）

1,000,000

qwen-plus-2025-01-25

（qwen-plus-0125）

150,000

qwen-plus-2025-01-12

（qwen-plus-0112）

qwen-plus-2024-12-20

（qwen-plus-1220）

qwen3.5-flash

30,000

10,000,000

qwen3.5-flash-2026-02-23

600

1,000,000

qwen-flash

30,000

10,000,000

qwen-flash-2025-07-28

60

1,000,000

qwen-turbo

> 用[Batch API](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)调用服务时，不受限流限制。

1,200

5,000,000

qwen-turbo-latest

qwen-turbo-2025-07-15

(qwen-turbo-0715)

60

100,000

qwen-turbo-2025-04-28

(qwen-turbo-0428)

1,000,000

qwen-turbo-2025-02-11

(qwen-turbo-0211)

5,000,000

qwen-turbo-2024-11-01

(qwen-turbo-1101)

qwq-plus

600

1,000,000

qwq-plus-latest

qwq-plus-2025-03-05

60

100,000

qwen-long

1,200

3,000,000

qwen-long-latest

60,000

qwen-long-2025-01-25

(qwen-long-0125)

3

7,500

## **全球**

服务部署范围为[全球](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度；静态数据存储于您所选的地域。该部署范围支持的地域：美国（弗吉尼亚）、德国（法兰克福）。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

qwen3.7-max

30,000

5,000,000

qwen3.7-max-2026-05-20

600

1,000,000

qwen3-max

600

1,000,000

qwen3-max-2025-09-23

60

100,000

qwen3-max-preview

600

1,000,000

qwen3.6-plus

30,000

5,000,000

qwen3.6-plus-2026-04-02

600

1,000,000

qwen3.6-flash

15,000

5,000,000

qwen3.6-flash-2026-04-16

60

1,000,000

qwen3.5-plus

30,000

5,000,000

qwen3.5-plus-2026-02-15

600

1,000,000

qwen-plus

15,000

5,000,000

qwen-plus-2025-12-01

60

1,000,000

qwen-plus-2025-09-11

qwen-plus-2025-07-28

qwen3.5-flash

30,000

10,000,000

qwen3.5-flash-2026-02-23

600

1,000,000

qwen-flash

15,000

10,000,000

qwen-flash-2025-07-28

60

1,000,000

## **国际**

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

qwen3.7-max

600

1,000,000

qwen3.7-max-2026-05-20

60

1,000,000

qwen3.6-max-preview

600

1,000,000

qwen3-max

600

1,000,000

qwen3-max-2026-01-23

qwen3-max-2025-09-23

60

100,000

qwen3-max-preview

600

1,000,000

qwen-max

600

1,000,000

qwen-max-latest

600

1,000,000

qwen-max-2025-01-25

(qwen-max-0125)

60

100,000

qwen3.6-plus

15,000

5,000,000

qwen3.6-plus-2026-04-02

60

1,000,000

qwen3.6-flash

15,000

5,000,000

qwen3.6-flash-2026-04-16

60

1,000,000

qwen3.5-plus

15,000

5,000,000

qwen3.5-plus-2026-04-20

600

1,000,000

qwen3.5-plus-2026-02-15

60

1,000,000

qwen-plus-latest

600

1,000,000

qwen-plus-2025-12-01

120

qwen-plus-2025-09-11

120

qwen-plus-2025-07-28

60

100,000

qwen-plus-2025-07-14

(qwen-plus-0714)

qwen-plus-2025-04-28

(qwen-plus-0428)

1,000,000

qwen-plus-2025-01-25

(qwen-plus-0125)

100,000

qwen3.5-flash

15,000

5,000,000

qwen3.5-flash-2026-02-23

60

1,000,000

qwen-flash

600

5,000,000

qwen-flash-2025-07-28

600

5,000,000

qwq-plus

60

100,000

qwen-turbo

600

5,000,000

qwen-turbo-latest

600

5,000,000

qwen-turbo-2025-04-28

(qwen-turbo-0428)

60

1,000,000

qwen-turbo-2024-11-01

(qwen-turbo-1101)

5,000,000

## **美国**

服务部署范围为[美国](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于美国境内；静态数据存储于您所选的地域。该部署范围支持的地域：美国（弗吉尼亚）。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

qwen-plus-us

600

1,000,000

qwen-plus-2025-12-01-us

60

qwen-flash-us

600

5,000,000

qwen-flash-2025-07-28-us

## **欧盟**

服务部署范围为[欧盟](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于欧盟境内；静态数据存储于您所选的地域。该部署范围支持的地域：德国（法兰克福）。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

qwen3-max

600

1,000,000

qwen3-max-2026-01-23

qwen-plus

600

1,000,000

qwen-plus-2025-12-01

120

1,000,000

qwen3.5-flash

30,000

10,000,000

qwen3.5-flash-2026-02-23

600

1,000,000

### **千问VL（视觉理解/图生文）**

## **中国内地**

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

qwen3-vl-plus

3,000

5,000,000

qwen3-vl-plus-2025-12-19

60

100,000

qwen3-vl-plus-2025-09-23

qwen3-vl-flash

3,000

5,000,000

qwen3-vl-flash-2026-01-22

60

100,000

qwen3-vl-flash-2025-10-15

qwen-vl-max

1,200

1,000,000

qwen-vl-max-latest

qwen-vl-max-2025-08-13

（qwen-vl-max-0813）

60

100,000

qwen-vl-max-2025-04-08

（qwen-vl-max-0408）

qwen-vl-max-2025-04-02

（qwen-vl-max-0402）

qwen-vl-max-2025-01-25

（qwen-vl-max-0125）

qwen-vl-max-2024-12-30

（qwen-vl-max-1230）

qwen-vl-max-2024-11-19

（qwen-vl-max-1119）

qwen-vl-plus

1,200

1,000,000

qwen-vl-plus-latest

qwen-vl-plus-2025-08-15

（qwen-vl-plus-0815）

60

100,000

qwen-vl-plus-2025-07-10

（qwen-vl-plus-0710）

qwen-vl-plus-2025-05-07

（qwen-vl-plus-0507）

qwen-vl-plus-2025-01-25

（qwen-vl-plus-0125）

qwen-vl-plus-2025-01-02

（qwen-vl-plus-0102）

qvq-max

qvq-max-latest

qvq-max-2025-05-15

（qvq-max-0515）

qvq-max-2025-03-25

（qvq-max-0325）

qvq-plus

qvq-plus-latest

qvq-plus-2025-05-15

（qvq-plus-0515）

## **全球**

服务部署范围为[全球](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度；静态数据存储于您所选的地域。该部署范围支持的地域：美国（弗吉尼亚）、德国（法兰克福）。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

qwen3-vl-plus

1,200

1,000,000

qwen3-vl-plus-2025-09-23

60

100,000

qwen3-vl-flash

1,200

1,000,000

qwen3-vl-flash-2025-10-15

60

100,000

## **国际**

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

qwen3-vl-plus

1,200

1,000,000

qwen3-vl-plus-2025-12-19

60

100,000

qwen3-vl-plus-2025-09-23

120

1,000,000

qwen3-vl-flash

1,200

1,000,000

qwen3-vl-flash-2026-01-22

60

100,000

qwen3-vl-flash-2025-10-15

120

1,000,000

qwen-vl-max

1,200

1,000,000

qwen-vl-max-latest

qwen-vl-max-2025-08-13

(qwen-vl-max-0813)

60

100,000

qwen-vl-max-2025-04-08

(qwen-vl-max-0408)

1,200

1,000,000

qwen-vl-plus

qwen-vl-plus-latest

qwen-vl-plus-2025-08-15

(qwen-vl-plus-0815)

120

1,000,000

qwen-vl-plus-2025-05-07

(qwen-vl-plus-0507)

qwen-vl-plus-2025-01-25

(qwen-vl-plus-0125)

1,200

qvq-max

60

100,000

qvq-max-latest

qvq-max-2025-03-25

(qvq-max-0325)

## **美国**

服务部署范围为[美国](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于美国境内；静态数据存储于您所选的地域。该部署范围支持的地域：美国（弗吉尼亚）。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

qwen3-vl-flash-us

1,200

1,000,000

qwen3-vl-flash-2025-10-15-us

120

1,000,000

## **欧盟**

服务部署范围为[欧盟](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于欧盟境内；静态数据存储于您所选的地域。该部署范围支持的地域：德国（法兰克福）。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

qwen3-vl-plus

1,200

1,000,000

qwen3-vl-flash

1,200

1,000,000

qwen3-vl-flash-2026-01-22

60

100,000

qwen3-vl-flash-2025-10-15

60

100,000

### **千问Omni**

## **中国内地**

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

qwen3.5-omni-plus

60

100,000

qwen3.5-omni-plus-2026-03-15

qwen3.5-omni-flash

qwen3.5-omni-flash-2026-03-15

qwen3-omni-flash

qwen3-omni-flash-2025-12-01

qwen3-omni-flash-2025-09-15

qwen-omni-turbo

qwen-omni-turbo-latest

qwen-omni-turbo-2025-03-26

（qwen-omni-turbo-0326）

qwen-omni-turbo-2025-01-19

（qwen-omni-turbo-0119）

## **国际**

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

qwen3.5-omni-plus

60

100,000

qwen3.5-omni-plus-2026-03-15

qwen3.5-omni-flash

qwen3.5-omni-flash-2026-03-15

qwen3-omni-flash

qwen3-omni-flash-2025-12-01

qwen3-omni-flash-2025-09-15

qwen-omni-turbo

qwen-omni-turbo-latest

qwen-omni-turbo-2025-03-26

### **千问Omni-Realtime**

## **中国内地**

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

qwen3.5-omni-plus-realtime

60

100,000

qwen3.5-omni-plus-realtime-2026-03-15

qwen3.5-omni-flash-realtime

qwen3.5-omni-flash-realtime-2026-03-15

qwen3-omni-flash-realtime

qwen3-omni-flash-realtime-2025-12-01

qwen3-omni-flash-realtime-2025-09-15

qwen-omni-turbo-realtime-latest

qwen-omni-turbo-realtime-2025-05-08

## **国际**

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

qwen3.5-omni-plus-realtime

60

100,000

qwen3.5-omni-plus-realtime-2026-03-15

qwen3.5-omni-flash-realtime

qwen3.5-omni-flash-realtime-2026-03-15

qwen3-omni-flash-realtime

qwen3-omni-flash-realtime-2025-12-01

qwen3-omni-flash-realtime-2025-09-15

qwen-omni-turbo-realtime

10,000

qwen-omni-turbo-realtime-latest

qwen-omni-turbo-realtime**\-**2025-05-08

### **千问OCR（文字提取）**

## **中国内地**

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

qwen-vl-ocr

600

6,000,000

qwen-vl-ocr-latest

1,200

qwen-vl-ocr-2025-11-20

qwen-vl-ocr-2025-08-28

600

qwen-vl-ocr-2025-04-13

qwen-vl-ocr-2024-10-28

## **全球**

服务部署范围为[全球](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度；静态数据存储于您所选的地域。该部署范围支持的地域：美国（弗吉尼亚）、德国（法兰克福）。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

qwen-vl-ocr

600

6,000,000

qwen-vl-ocr-2025-11-20

1,200

## **国际**

服务部署范围为[美国](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于美国境内；静态数据存储于您所选的地域。该部署范围支持的地域：美国（弗吉尼亚）。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

qwen-vl-ocr

600

6,000,000

qwen-vl-ocr-2025-11-20

1,200

### **千问Audio（音频理解）**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

qwen-audio-turbo

120

100,000

qwen-audio-turbo-latest

60

### **千问数学模型**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

qwen-math-plus

1,200

1,000,000

qwen-math-plus-latest

qwen-math-plus-2024-09-19

（qwen-math-plus-0919）

60

100,000

qwen-math-plus-2024-08-16

（qwen-math-plus-0816）

10

20,000

qwen-math-turbo

1200

1,000,000

qwen-math-turbo-latest

qwen-math-turbo-2024-09-19

（qwen-math-turbo-0919）

60

100,000

### **千问Coder**

## **中国内地**

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

qwen3-coder-plus

5,000

5,000,000

qwen3-coder-plus-2025-09-23

60

1,000,000

qwen3-coder-plus-2025-07-22

qwen3-coder-flash

5,000

5,000,000

qwen3-coder-flash-2025-07-28

60

1,000,000

qwen-coder-plus

1,200

qwen-coder-plus-latest

qwen-coder-plus-2024-11-06

（qwen-coder-plus-1106）

120

200,000

qwen-coder-turbo

1,200

1,000,000

qwen-coder-turbo-latest

qwen-coder-turbo-2024-09-19

（qwen-coder-turbo-0919）

60

100,000

## **全球**

服务部署范围为[全球](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度；静态数据存储于您所选的地域。该部署范围支持的地域：美国（弗吉尼亚）、德国（法兰克福）。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

qwen3-coder-plus

2,400

2,000,000

qwen3-coder-plus-2025-09-23

60

1,000,000

qwen3-coder-plus-2025-07-22

qwen3-coder-flash

1,200

qwen3-coder-flash-2025-07-28

60

## **国际**

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

qwen3-coder-plus

2,400

2,000,000

qwen3-coder-plus-2025-09-23

600

1,000,000

qwen3-coder-plus-2025-07-22

60

1,000,000

qwen3-coder-flash

600

5,000,000

qwen3-coder-flash-2025-07-28

600

5,000,000

### **千问翻译模型**

## **中国内地**

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

qwen-mt-plus

60

25,000

qwen-mt-flash

35,000

qwen-mt-lite

100,000

qwen-mt-turbo

35,000

## **全球**

服务部署范围为[全球](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度；静态数据存储于您所选的地域。该部署范围支持的地域：美国（弗吉尼亚）、德国（法兰克福）。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

qwen-mt-plus

60

25,000

qwen-mt-flash

35,000

qwen-mt-lite

100,000

## **国际**

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

qwen-mt-plus

60

100,000

qwen-mt-flash

qwen-mt-lite

qwen-mt-turbo

## **美国**

服务部署范围为[美国](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于美国境内；静态数据存储于您所选的地域。该部署范围支持的地域：美国（弗吉尼亚）。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

qwen-mt-lite-us

60

100,000

### **千问数据挖掘模型**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

qwen-doc-turbo

600

3,000,000

### **千问深入研究模型**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

qwen-deep-research

120

1,200,000

### **通义晓蜜对话分析模型**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

tongyi-xiaomi-analysis-flash

600

1,000,000

tongyi-xiaomi-analysis-pro

## **文本生成-千问-开源版**

### **千问语言模型开源版**

## **中国内地**

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

qwen3.6-35b-a3b

600

1,000,000

qwen3.6-27b

qwen3.5-397b-a17b

qwen3.5-122b-a10b

qwen3.5-27b

qwen3.5-35b-a3b

qwen3-next-80b-a3b-thinking

qwen3-next-80b-a3b-instruct

qwen3-235b-a22b-thinking-2507

qwen3-235b-a22b-instruct-2507

qwen3-30b-a3b-thinking-2507

qwen3-30b-a3b-instruct-2507

qwen3-235b-a22b

qwen3-30b-a3b

qwen3-32b

2400

qwen3-14b

600

qwen3-8b

qwen3-4b

qwen3-1.7b

qwen3-0.6b

qwq-32b

qwq-32b-preview

1,200

qwen2.5-72b-instruct

qwen2.5-32b-instruct

qwen2.5-14b-instruct

qwen2.5-14b-instruct-1m

5,000,000

qwen2.5-7b-instruct

1,000,000

qwen2.5-7b-instruct-1m

5,000,000

qwen2.5-3b-instruct

2,000,000

qwen2.5-1.5b-instruct

qwen2.5-0.5b-instruct

## **全球**

服务部署范围为[全球](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度；静态数据存储于您所选的地域。该部署范围支持的地域：美国（弗吉尼亚）、德国（法兰克福）。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

qwen3.6-35b-a3b

600

1,000,000

qwen3.5-397b-a17b

qwen3.5-122b-a10b

qwen3.5-27b

qwen3.5-35b-a3b

qwen3-next-80b-a3b-thinking

qwen3-next-80b-a3b-instruct

qwen3-235b-a22b-thinking-2507

qwen3-235b-a22b-instruct-2507

qwen3-30b-a3b-thinking-2507

qwen3-30b-a3b-instruct-2507

qwen3-235b-a22b

qwen3-32b

qwen3-30b-a3b

qwen3-14b

qwen3-8b

## **国际**

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

qwen3.6-35b-a3b

600

1,000,000

qwen3.6-27b

1,000,000

qwen3.5-397b-a17b

1,000,000

qwen3.5-122b-a10b

1,000,000

qwen3.5-27b

1,000,000

qwen3.5-35b-a3b

5,000,000

qwen3-next-80b-a3b-thinking

1,000,000

qwen3-next-80b-a3b-instruct

qwen3-235b-a22b-thinking-2507

qwen3-235b-a22b-instruct-2507

qwen3-30b-a3b-thinking-2507

5,000,000

qwen3-30b-a3b-instruct-2507

qwen3-235b-a22b

1,000,000

qwen3-32b

qwen3-30b-a3b

qwen3-14b

qwen3-8b

qwen3-4b

qwen3-1.7b

qwen3-0.6b

qwen2.5-14b-instruct-1m

1,200

5,000,000

qwen2.5-7b-instruct-1m

qwen2.5-72b-instruct

60

150,000

qwen2.5-32b-instruct

qwen2.5-14b-instruct

qwen2.5-7b-instruct

### **Qwen-VL**

## **中国内地**

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

qwen3-vl-32b-thinking

600

1,000,000

qwen3-vl-32b-instruct

qwen3-vl-30b-a3b-thinking

qwen3-vl-30b-a3b-instruct

qwen3-vl-8b-thinking

qwen3-vl-8b-instruct

qwen3-vl-235b-a22b-thinking

60

100,000

qwen3-vl-235b-a22b-instruct

qwen2.5-vl-72b-instruct

qwen2.5-vl-32b-instruct

qwen2.5-vl-7b-instruct

1,200

1,000,000

qwen2.5-vl-3b-instruct

qvq-72b-preview

60

100,000

## **全球**

服务部署范围为[全球](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度；静态数据存储于您所选的地域。该部署范围支持的地域：美国（弗吉尼亚）、德国（法兰克福）。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

qwen3-vl-235b-a22b-thinking

60

100,000

qwen3-vl-235b-a22b-instruct

qwen3-vl-32b-thinking

600

1,000,000

qwen3-vl-32b-instruct

qwen3-vl-30b-a3b-thinking

qwen3-vl-30b-a3b-instruct

qwen3-vl-8b-thinking

qwen3-vl-8b-instruct

## **国际**

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

qwen3-vl-32b-thinking

60

100,000

qwen3-vl-32b-instruct

qwen3-vl-30b-a3b-thinking

qwen3-vl-30b-a3b-instruct

qwen3-vl-8b-thinking

qwen3-vl-8b-instruct

qwen3-vl-235b-a22b-thinking

qwen3-vl-235b-a22b-instruct

qwen2.5-vl-72b-instruct

qwen2.5-vl-32b-instruct

qwen2.5-vl-7b-instruct

1,200

1,000,000

qwen2.5-vl-3b-instruct

### **Qwen-Omni**

## **中国内地**

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

qwen2.5-omni-7b

60

100,000

## **国际**

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

qwen2.5-omni-7b

60

100,000

### **Qwen3-Omni-Captioner**

## **中国内地**

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

qwen3-omni-30b-a3b-captioner

60

100,000

## **国际**

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

qwen3-omni-30b-a3b-captioner

60

100,000

### **Qwen-Math**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

qwen2.5-math-72b-instruct

1,200

1,000,000

qwen2.5-math-7b-instruct

### **Qwen-Coder**

## **中国内地**

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

qwen3-coder-next

600

1,000,000

qwen3-coder-480b-a35b-instruct

qwen3-coder-30b-a3b-instruct

qwen2.5-coder-32b-instruct

1,200

qwen2.5-coder-14b-instruct

qwen2.5-coder-7b-instruct

## **全球**

服务部署范围为[全球](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度；静态数据存储于您所选的地域。该部署范围支持的地域：美国（弗吉尼亚）、德国（法兰克福）。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

qwen3-coder-480b-a35b-instruct

600

1,000,000

qwen3-coder-30b-a3b-instruct

600

1,000,000

## **国际**

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

qwen3-coder-next

600

1,000,000

qwen3-coder-480b-a35b-instruct

qwen3-coder-30b-a3b-instruct

## **欧盟**

服务部署范围为[欧盟](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于欧盟境内；静态数据存储于您所选的地域。该部署范围支持的地域：德国（法兰克福）。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

qwen3-coder-next

600

1,000,000

## **文本生成-第三方模型**

### **DeepSeek**

## **中国内地**

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

deepseek-v4-pro

15,000

1,200,000

deepseek-v4-flash

deepseek-v3.2

15,000

1,200,000

deepseek-v3.2-exp

15,000

1,200,000

deepseek-v3.1

deepseek-r1-0528

60

100,000

deepseek-r1

15,000

1,200,000

deepseek-v3

deepseek-r1-distill-qwen-7b

deepseek-r1-distill-qwen-14b

deepseek-r1-distill-qwen-32b

deepseek-r1-distill-qwen-1.5b

60

100,000

deepseek-r1-distill-llama-8b

deepseek-r1-distill-llama-70b

## **全球**

服务部署范围为[全球](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度；静态数据存储于您所选的地域。该部署范围支持的地域：美国（弗吉尼亚）、德国（法兰克福）。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

deepseek-v4-pro

15,000

1,200,000

deepseek-v4-flash

## **国际**

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

deepseek-v4-pro

10,000

1,200,000

deepseek-v4-flash

deepseek-v3.2

10,000

1,200,000

### **DeepSeek-硅基流动直供**

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

siliconflow/deepseek-v3.2

500

500,000

siliconflow/deepseek-v3.1-terminus

siliconflow/deepseek-r1-0528

siliconflow/deepseek-v3-0324

### **DeepSeek-快手万擎直供**

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

vanchin/deepseek-v3.2-think

30

600,000

vanchin/deepseek-v3.1-terminus

500

1,000,000

vanchin/deepseek-r1

vanchin/deepseek-v3

vanchin/deepseek-ocr

### **Kimi**

## **中国内地**

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

kimi-k2.6

500

1,000,000

kimi-k2.5

500

1,000,000

kimi-k2-thinking

500

1,000,000

Moonshot-Kimi-K2-Instruct

500

1,000,000

## **全球**

服务部署范围为[全球](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度；静态数据存储于您所选的地域。该部署范围支持的地域：美国（弗吉尼亚）、德国（法兰克福）。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

kimi-k2.5

500

1,000,000

### **Kimi-月之暗面直供**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

kimi/kimi-k2.6

500

> 同一个阿里云百炼API Key 下，kimi/kimi-k2.6与 kimi/kimi-k2.5 共享 500 RPM 限流配额。即这 2 个模型的每分钟请求总数加起来不能超过 500。

3,000,000

> 同一个阿里云百炼API Key 下，kimi/kimi-k2.6 与 kimi/kimi-k2.5 共享 3000000 TPM 限流配额。即这 2 个模型的每分钟 Token 消耗总数加起来不能超过 3000000。

kimi/kimi-k2.5

### **GLM**

## **中国内地**

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

glm-5.1

500

1,000,000

glm-5

500

1,000,000

glm-4.7

glm-4.6

60

glm-4.5

glm-4.5-air

## **全球**

服务部署范围为[全球](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度；静态数据存储于您所选的地域。该部署范围支持的地域：美国（弗吉尼亚）、德国（法兰克福）。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

glm-5.1

500

1,000,000

### **GLM-智谱直供**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

ZHIPU/GLM-5.1

200

30,000,000

ZHIPU/GLM-5

200

30,000,000

### **MiniMax**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

MiniMax-M2.5

500

1,000,000

MiniMax-M2.1

500

1,000,000

### **MiniMax-稀宇科技直供**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

MiniMax/MiniMax-M2.7

500

20,000,000

MiniMax/MiniMax-M2.5

MiniMax/MiniMax-M2.1

### **MiMo-小米直供**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

xiaomi/mimo-v2.5-pro

100

10,000,000

## **图像生成**

### **千问（Qwen-Image）**

## **中国内地**

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型名称**

**模型名称**

**限流条件（超出任一数值时触发限流）**

**任务下发接口调用限制**

**同时处理中任务数量（并发数）**

文生图与图像编辑

qwen-image-2.0-pro

2 次/分钟

同步接口无限制

qwen-image-2.0-pro-2026-04-22

2 次/分钟

同步接口无限制

qwen-image-2.0-pro-2026-03-03

2 次/分钟

同步接口无限制

qwen-image-2.0

2 次/秒

同步接口无限制

qwen-image-2.0-2026-03-03

2 次/秒

同步接口无限制

文生图

qwen-image-max

2 次/分钟

同步接口无限制

qwen-image-max-2025-12-30

2 次/分钟

同步接口无限制

qwen-image-plus

2 次/秒

同步接口无限制 / 异步接口 2

qwen-image-plus-2026-01-09

2 次/秒

同步接口无限制

qwen-image

2 次/秒

同步接口无限制 / 异步接口 2

图像编辑

qwen-image-edit-max

2 次/分钟

同步接口无限制

qwen-image-edit-max-2026-01-16

2 次/分钟

同步接口无限制

qwen-image-edit-plus

2 次/秒

同步接口无限制

qwen-image-edit-plus-2025-12-15

2 次/秒

同步接口无限制

qwen-image-edit-plus-2025-10-30

2 次/秒

同步接口无限制

qwen-image-edit

2 次/秒

同步接口无限制

图像翻译

qwen-mt-image

1 次/秒

2

## **国际**

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**模型服务**

**模型名称**

**限流条件（超出任一数值时触发限流）**

**任务下发接口调用限制**

**同时处理中任务数量（并发数）**

文生图与图像编辑

qwen-image-2.0-pro

2 次/分钟

同步接口无限制

qwen-image-2.0-pro-2026-04-22

2 次/分钟

同步接口无限制

qwen-image-2.0-pro-2026-03-03

2 次/分钟

同步接口无限制

qwen-image-2.0

2 次/秒

同步接口无限制

qwen-image-2.0-2026-03-03

2 次/秒

同步接口无限制

文生图

qwen-image-max

2 次/分钟

同步接口无限制

qwen-image-max-2025-12-30

2 次/分钟

同步接口无限制

qwen-image-plus

2 次/秒

同步接口无限制 / 异步接口 2

qwen-image-plus-2026-01-09

2 次/秒

同步接口无限制

qwen-image

2 次/秒

同步接口无限制 / 异步接口 2

图像编辑

qwen-image-edit-max

2 次/分钟

同步接口无限制

qwen-image-edit-max-2026-01-16

2 次/分钟

同步接口无限制

qwen-image-edit-plus

2 次/秒

同步接口无限制

qwen-image-edit-plus-2025-12-15

2 次/秒

同步接口无限制

qwen-image-edit-plus-2025-10-30

2 次/秒

同步接口无限制

qwen-image-edit

2 次/秒

同步接口无限制

### **文生图-Z-Image**

## **中国内地**

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型名称**

**限流条件（超出任一数值时触发限流）**

**每秒钟任务下发接口RPS限制**

**同时处理中任务数量（并发数）**

z-image-turbo

2

同步接口无限制

## **国际**

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**模型名称**

**限流条件（超出任一数值时触发限流）**

**每秒钟任务下发接口RPS限制**

**同时处理中任务数量（并发数）**

z-image-turbo

2

同步接口无限制

### **万相**

## **中国内地**

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型服务**

**模型名称**

**限流条件（超出任一数值时触发限流）**

**每秒钟任务下发接口RPS限制**

**同时处理中任务数量（并发数）**

图像生成与编辑

wan2.7-image-pro

5

5

wan2.7-image

wan2.6-image

文生图

wan2.6-t2i

1

5

wan2.5-t2i-preview

5

wan2.2-t2i-plus

2

2

wan2.2-t2i-flash

wanx2.1-t2i-plus

wanx2.1-t2i-turbo

wanx2.0-t2i-turbo

通用图像编辑

wan2.5-i2i-preview

5

5

wanx2.1-imageedit

2

2

文生图

wanx-v1

2

1

图像局部重绘

wanx-x-painting

涂鸦作画

wanx-sketch-to-image-lite

## **全球**

服务部署范围为[全球](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度；静态数据存储于您所选的地域。该部署范围支持的地域：美国（弗吉尼亚）、德国（法兰克福）。

**模型服务**

**模型名称**

**限流条件（超出任一数值时触发限流）**

**每秒钟任务下发接口RPS限制**

**同时处理中任务数量（并发数）**

文生图

wan2.6-t2i

5

5

图像生成

wan2.6-image

5

5

## **国际**

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**模型服务**

**模型名称**

**限流条件（超出任一数值时触发限流）**

**每秒钟任务下发接口RPS限制**

**同时处理中任务数量（并发数）**

图像生成与编辑

wan2.7-image-pro

5

5

wan2.7-image

wan2.6-image

文生图

wan2.6-t2i

5

5

wan2.5-t2i-preview

wan2.2-t2i-flash

2

2

wan2.2-t2i-plus

wan2.1-t2i-turbo

wan2.1-t2i-plus

通用图像编辑

wan2.5-i2i-preview

5

5

### **图像编辑与生成**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

**模型名称**

**限流条件（超出任一数值时触发限流）**

**每秒钟任务下发接口RPS限制**

**同时处理中任务数量（并发数）**

shoemodel-v1

2

1

wanx-virtualmodel

wanx-style-repaint-v1

2

wanx-poster-generation-v1

1

virtualmodel-v2

wanx-background-generation-v2

image-instance-segmentation

image-erase-completion

image-out-painting

2

10

### **人物写真生成-FaceChain**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

**模型名称**

**限流条件（超出任一数值时触发限流）**

**作业提交接口RPS限制**

**同时处理中任务数量**

facechain-facedetect

5

同步接口无限制

facechain-finetune

1

1

facechain-generation

2

### **创意文字生成-WordArt锦书**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

**模型名称**

**限流条件（超出任一数值时触发限流）**

**作业提交接口RPS限制**

**同时处理中任务数量**

wordart-texture

2

1

wordart-semantic

### **AI试衣-OutfitAnyone**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

**模型名称**

**限流条件（超出任一数值时触发限流）**

**作业提交接口RPS限制**

**同时处理中任务数量**

aitryon

10

5

aitryon-plus

10

5

aitryon-parsing-v1

10

同步接口无限制

aitryon-refiner

10

5

## **图像生成-第三方模型**

### **可灵系列**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

**模型名称**

**限流条件（超出任一数值时触发限流）**

**每秒钟任务下发接口RPS限制**

**同时处理中任务数量（并发数）**

kling/kling-v3-omni-image-generation

5

10

> 同一阿里云百炼API Key 下，可灵系列的 4 个模型（[图像](#fdd6e348d2md4)及[视频](#kling-third-party-limit)）共享 10 个并发数。即这 4 个模型处于运行状态的任务总数加起来不能超过 10 个。

kling/kling-v3-image-generation

5

## **音乐生成**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

**模型名称**

**每分钟调用次数（RPM）**

fun-music-v1

180

## **语音合成（文本转语音）**

### **千问语音合成**

#### 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

##### **千问3-TTS-Instruct-Flash**

**模型名称**

**每分钟调用次数（RPM）**

qwen3-tts-instruct-flash

180

qwen3-tts-instruct-flash-2026-01-26

180

##### **千问3-TTS-VD**

**模型名称**

**每分钟调用次数（RPM）**

qwen3-tts-vd-2026-01-26

180

##### **千问3-TTS-VC**

**模型名称**

**每分钟调用次数（RPM）**

qwen3-tts-vc-2026-01-22

180

##### 千问3-TTS-Flash

**模型名称**

**每分钟调用次数（RPM）**

qwen3-tts-flash

180

qwen3-tts-flash-2025-11-27

180

qwen3-tts-flash-2025-09-18

10

##### 千问-TTS

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

qwen-tts

10

100,000

qwen-tts-latest

qwen-tts-2025-05-22

qwen-tts-2025-04-10

#### 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

##### **千问3-TTS-Instruct-Flash**

**模型名称**

**每分钟调用次数（RPM）**

qwen3-tts-instruct-flash

180

qwen3-tts-instruct-flash-2026-01-26

180

##### **千问3-TTS-VD**

**模型名称**

**每分钟调用次数（RPM）**

qwen3-tts-vd-2026-01-26

180

##### **千问3-TTS-VC**

**模型名称**

**每分钟调用次数（RPM）**

qwen3-tts-vc-2026-01-22

180

##### 千问3-TTS-Flash

**模型名称**

**每分钟调用次数（RPM）**

qwen3-tts-flash

180

qwen3-tts-flash-2025-11-27

180

qwen3-tts-flash-2025-09-18

10

### **千问实时语音合成**

#### 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

##### **千问3-TTS-Instruct-Flash-Realtime**

**模型名称**

**每分钟调用次数（RPM）**

qwen3-tts-instruct-flash-realtime

180

qwen3-tts-instruct-flash-realtime-2026-01-22

180

##### 千问3-TTS-VD-Realtime

**模型名称**

**每分钟调用次数（RPM）**

qwen3-tts-vd-realtime-2026-01-15

180

qwen3-tts-vd-realtime-2025-12-16

##### 千问3-TTS-VC-Realtime

**模型名称**

**每分钟调用次数（RPM）**

qwen3-tts-vc-realtime-2026-01-15

180

qwen3-tts-vc-realtime-2025-11-27

##### 千问3-TTS-Flash-Realtime

**模型名称**

**每分钟调用次数（RPM）**

qwen3-tts-flash-realtime

180

qwen3-tts-flash-realtime-2025-11-27

180

qwen3-tts-flash-realtime-2025-09-18

10

##### 千问-TTS-Realtime

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

qwen-tts-realtime

10

100,000

qwen-tts-realtime-latest

qwen-tts-realtime-2025-07-15

#### 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

##### **千问3-TTS-Instruct-Flash-Realtime**

**模型名称**

**每分钟调用次数（RPM）**

qwen3-tts-instruct-flash-realtime

180

qwen3-tts-instruct-flash-realtime-2026-01-22

180

##### 千问3-TTS-VD-Realtime

**模型名称**

**每分钟调用次数（RPM）**

qwen3-tts-vd-realtime-2026-01-15

180

qwen3-tts-vd-realtime-2025-12-16

##### 千问3-TTS-VC-Realtime

**模型名称**

**每分钟调用次数（RPM）**

qwen3-tts-vc-realtime-2026-01-15

180

qwen3-tts-vc-realtime-2025-11-27

##### 千问3-TTS-Flash-Realtime

**模型名称**

**每分钟调用次数（RPM）**

qwen3-tts-flash-realtime

180

qwen3-tts-flash-realtime-2025-11-27

180

qwen3-tts-flash-realtime-2025-09-18

10

### **千问声音复刻**

#### 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型名称**

**每分钟调用次数（RPM）**

qwen-voice-enrollment

180

#### 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**模型名称**

**每分钟调用次数（RPM）**

qwen-voice-enrollment

180

### **千问声音设计**

#### 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型名称**

**每分钟调用次数（RPM）**

qwen-voice-design

180

#### 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**模型名称**

**每分钟调用次数（RPM）**

qwen-voice-design

180

### **CosyVoice语音合成**

#### 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型名称**

**提交作业接口RPS限制**

cosyvoice-v3.5-plus

3

cosyvoice-v3.5-flash

cosyvoice-v3-plus

cosyvoice-v3-flash

cosyvoice-v2

cosyvoice-v1

#### 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**模型名称**

**提交作业接口RPS限制**

cosyvoice-v3-plus

3

cosyvoice-v3-flash

### **CosyVoice声音复刻/设计**

CosyVoice声音复刻共用一个模型，共用限流额度。

#### 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型名称**

**提交作业接口RPS限制**

voice-enrollment

10

#### 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**模型名称**

**提交作业接口RPS限制**

voice-enrollment

10

### **Sambert语音合成**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

**模型服务**

**提交作业接口RPS限制**

Sambert系列模型

20

## **语音合成（文本转语音）-第三方模型**

### **MiniMax-稀宇科技直供**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

**模型名称**

**限流条件（超出任一数值时触发限流）**

**每分钟调用次数（RPM）**

**每分钟消耗字符数**

> **仅含输入字符数**

MiniMax/speech-2.8-hd

20

20,000

MiniMax/speech-02-hd

MiniMax/speech-2.8-turbo

MiniMax/speech-02-turbo

## **语音识别（语音转文本）与翻译（语音转成指定语种的文本）**

### **千问3-LiveTranslate-Flash**

#### 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

qwen3-livetranslate-flash

100

100,000

qwen3-livetranslate-flash-2025-12-01

#### 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

qwen3-livetranslate-flash

100

100,000

qwen3-livetranslate-flash-2025-12-01

### **千问-LiveTranslate-Flash-Realtime**

#### 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

qwen3.5-livetranslate-flash-realtime

10

100,000

qwen3.5-livetranslate-flash-realtime-2026-05-19

qwen3-livetranslate-flash-realtime

qwen3-livetranslate-flash-realtime-2025-09-22

#### 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

qwen3.5-livetranslate-flash-realtime

10

100,000

qwen3.5-livetranslate-flash-realtime-2026-05-19

qwen3-livetranslate-flash-realtime

qwen3-livetranslate-flash-realtime-2025-09-22

### **千问录音文件识别**

#### 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

##### 千问3-ASR-Flash-Filetrans

**模型名称**

**每分钟调用次数（RPM）**

qwen3-asr-flash-filetrans

100

qwen3-asr-flash-filetrans-2025-11-17

##### **千问3-ASR-Flash**

**模型名称**

**每分钟调用次数（RPM）**

qwen3-asr-flash

100

qwen3-asr-flash-2026-02-10

qwen3-asr-flash-2025-09-08

#### 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

##### 千问3-ASR-Flash-Filetrans

**模型名称**

**每分钟调用次数（RPM）**

qwen3-asr-flash-filetrans

100

qwen3-asr-flash-filetrans-2025-11-17

##### **千问3-ASR-Flash**

**模型名称**

**每分钟调用次数（RPM）**

qwen3-asr-flash

100

qwen3-asr-flash-2026-02-10

qwen3-asr-flash-2025-09-08

#### 美国

服务部署范围为[美国](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于美国境内；静态数据存储于您所选的地域。该部署范围支持的地域：美国（弗吉尼亚）。

**模型名称**

**每分钟调用次数（RPM）**

qwen3-asr-flash-us

100

qwen3-asr-flash-2025-09-08-us

### **千问实时语音识别**

#### 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型名称**

**每秒钟调用次数（RPS）**

qwen3-asr-flash-realtime

20

qwen3-asr-flash-realtime-2026-02-10

qwen3-asr-flash-realtime-2025-10-27

#### 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**模型名称**

**每秒钟调用次数（RPS）**

qwen3-asr-flash-realtime

20

qwen3-asr-flash-realtime-2026-02-10

qwen3-asr-flash-realtime-2025-10-27

### **Fun-ASR录音文件识别**

#### 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型名称**

**每分钟调用次数（RPM）**

fun-asr

600

fun-asr-2025-11-07

fun-asr-2025-08-25

fun-asr-mtl

fun-asr-mtl-2025-08-25

#### 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**模型名称**

**每分钟调用次数（RPM）**

fun-asr

600

fun-asr-2025-11-07

600

fun-asr-2025-08-25

600

fun-asr-mtl

100

fun-asr-mtl-2025-08-25

100

### **Fun-ASR实时语音识别**

#### 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型名称**

**提交作业接口RPS限制**

fun-asr-realtime

20

fun-asr-realtime-2026-02-28

fun-asr-realtime-2025-11-07

fun-asr-realtime-2025-09-15

fun-asr-flash-8k-realtime

fun-asr-flash-8k-realtime-2026-01-28

#### 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**模型名称**

**提交作业接口RPS限制**

fun-asr-realtime

20

fun-asr-realtime-2025-11-07

### **Paraformer语音识别**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

**模型名称**

**提交作业接口RPS限制**

paraformer-realtime-v2

20

paraformer-realtime-v1

paraformer-realtime-8k-v2

paraformer-realtime-8k-v1

**模型名称**

**每分钟调用次数（RPM）**

paraformer-v2

1,200

**模型名称**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

paraformer-v1

600

6,000,000

paraformer-mtl-v1

600

6,000,000

**模型名称**

**提交作业接口RPS限制**

**同时处理中任务数量（并发数）**

paraformer-8k-v2

20

100

paraformer-8k-v1

10

500

## **视频生成**

### **HappyHorse系列**

## **中国内地**

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型名称**

**限流条件（超出任一数值时触发限流）**

**每秒钟任务下发接口RPS限制**

**同时处理中任务数量（并发数）**

happyhorse-1.0-t2v

5

5

happyhorse-1.0-i2v

5

5

happyhorse-1.0-r2v

5

5

happyhorse-1.0-video-edit

5

5

## **全球**

服务部署范围为[全球](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度；静态数据存储于您所选的地域。该部署范围支持的地域：美国（弗吉尼亚）、德国（法兰克福）。

**模型名称**

**限流条件（超出任一数值时触发限流）**

**每秒钟任务下发接口RPS限制**

**同时处理中任务数量（并发数）**

happyhorse-1.0-t2v

5

5

happyhorse-1.0-i2v

5

5

happyhorse-1.0-r2v

5

5

happyhorse-1.0-video-edit

5

5

## **国际**

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**模型名称**

**限流条件（超出任一数值时触发限流）**

**每秒钟任务下发接口RPS限制**

**同时处理中任务数量（并发数）**

happyhorse-1.0-t2v

5

5

happyhorse-1.0-i2v

5

5

happyhorse-1.0-r2v

5

5

happyhorse-1.0-video-edit

5

5

### **万相系列**

## **中国内地**

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型服务**

**模型名称**

**限流条件（超出任一数值时触发限流）**

**每秒钟任务下发接口RPS限制**

**同时处理中任务数量（并发数）**

文生视频

wan2.7-t2v-2026-04-25

5

5

wan2.7-t2v

5

5

wan2.6-t2v

5

5

wan2.5-t2v-preview

5

5

wan2.2-t2v-plus

2

2

wanx2.1-t2v-turbo

wanx2.1-t2v-plus

图生视频

wan2.7-i2v-2026-04-25

5

5

wan2.7-i2v

5

5

图生视频-基于首帧

wan2.6-i2v-flash

5

5

wan2.6-i2v

5

5

wan2.5-i2v-preview

5

5

wan2.2-i2v-flash

2

2

wan2.2-i2v-plus

wanx2.1-i2v-turbo

wanx2.1-i2v-plus

图生视频-基于首尾帧

wan2.2-kf2v-flash

wanx2.1-kf2v-plus

通用视频编辑

wanx2.1-vace-plus

wan2.7-videoedit

5

5

参考生视频

wan2.7-r2v

5

5

wan2.6-r2v-flash

5

5

wan2.6-r2v

5

5

数字人s2v

wan2.2-s2v-detect

5

同步接口无限制

wan2.2-s2v

1

图生动作

wan2.2-animate-move

5

1

视频换人

wan2.2-animate-mix

5

1

## **全球**

服务部署范围为[全球](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度；静态数据存储于您所选的地域。该部署范围支持的地域：美国（弗吉尼亚）、德国（法兰克福）。

**模型服务**

**模型名称**

**限流条件（超出任一数值时触发限流）**

**每秒钟任务下发接口RPS限制**

**同时处理中任务数量（并发数）**

文生视频

wan2.6-t2v

5

5

图生视频-基于首帧

wan2.6-i2v

参考生视频

wan2.6-r2v

## **国际**

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**模型服务**

**模型名称**

**限流条件（超出任一数值时触发限流）**

**每秒钟任务下发接口RPS限制**

**同时处理中任务数量（并发数）**

文生视频

wan2.7-t2v-2026-04-25

5

5

wan2.7-t2v

5

5

wan2.6-t2v

5

5

wan2.5-t2v-preview

5

5

wan2.2-t2v-plus

2

2

wan2.1-t2v-turbo

wan2.1-t2v-plus

图生视频

wan2.7-i2v-2026-04-25

5

5

wan2.7-i2v

5

5

图生视频-基于首帧

wan2.6-i2v-flash

5

5

wan2.6-i2v

wan2.5-i2v-preview

wan2.2-i2v-plus

2

2

wan2.1-i2v-turbo

wan2.1-i2v-plus

图生视频-基于首尾帧

wan2.1-kf2v-plus

1

通用视频编辑

wan2.1-vace-plus

2

wan2.7-videoedit

5

5

参考生视频

wan2.7-r2v

5

5

wan2.6-r2v-flash

5

5

wan2.6-r2v

5

5

图生动作

wan2.2-animate-move

5

1

视频换人

wan2.2-animate-mix

5

1

## **美国**

服务部署范围为[美国](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于美国境内；静态数据存储于您所选的地域。该部署范围支持的地域：美国（弗吉尼亚）。

**模型服务**

**模型名称**

**限流条件（超出任一数值时触发限流）**

**每秒钟任务下发接口RPS限制**

**同时处理中任务数量（并发数）**

文生视频

wan2.6-t2v-us

5

5

图生视频-基于首帧

wan2.6-i2v-us

### **舞动人像AnimateAnyone**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

**模型名称**

**任务下发接口RPS限制**

**同时处理中任务数量**

animate-anyone-detect-gen2

5

同步接口无限制

animate-anyone-template-gen2

1

在同一时刻，只有1个作业实际处于运行状态，其他队列中的作业处于排队状态。

animate-anyone-gen2

animate-anyone-detect

1算力单元支持2并发

animate-anyone

1算力单元支持1并发

### **悦动人像EMO**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

**模型名称**

**任务下发接口RPS限制**

**同时处理中任务数量**

emo-detect-v1

5

同步接口无限制

emo-v1

1

在同一时刻，只有1个作业实际处于运行状态，其他队列中的作业处于排队状态。

### **灵动人像LivePortrait**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

**模型名称**

**任务下发接口RPS限制**

**同时处理中任务数量**

liveportrait-detect

5

同步接口无限制

liveportrait

1

在同一时刻，只有1个作业实际处于运行状态，其他队列中的作业处于排队状态。

### **声动人像VideoRetalk**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

**模型名称**

**任务下发接口RPS限制**

**同时处理中任务数量**

videoretalk

1

1

在同一时刻，只有1个作业实际处于运行状态，其他队列中的作业处于排队状态。

### **表情包Emoji**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

**模型名称**

**任务下发接口RPS限制**

**同时处理中任务数量**

emoji-detect-v1

1

同步接口无限制

emoji-v1

1

在同一时刻，只有1个作业实际处于运行状态，其他队列中的作业处于排队状态。

### **视频风格重绘**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

**模型名称**

**任务下发接口RPS限制**

**同时处理中任务数量**

video-style-transform

20

2

在同一时刻，只有1个作业实际处于运行状态，其他队列中的作业处于排队状态。

## **视频生成-第三方模型**

### **爱诗系列**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

**模型名称**

**限流条件（超出任一数值时触发限流）**

**每秒钟任务下发接口RPS限制**

**同时处理中任务数量（并发数）**

pixverse/pixverse-c1-t2v

5

5

> 同一个阿里云百炼API Key 在 4个模型间共享额度。即这 4个模型处于运行状态的任务总数加起来不能超过 5 个。

pixverse/pixverse-c1-it2v

5

pixverse/pixverse-c1-kf2v

5

pixverse/pixverse-c1-r2v

5

pixverse/pixverse-v6-t2v

5

5

> 同一个阿里云百炼API Key 在 3 个模型间共享额度。即这 3个模型处于运行状态的任务总数加起来不能超过 5 个。

pixverse/pixverse-v6-it2v

5

pixverse/pixverse-v6-kf2v

5

pixverse/pixverse-v5.6-t2v

5

5

> 同一个阿里云百炼API Key 在 4 个模型间共享额度。即这 4 个模型处于运行状态的任务总数加起来不能超过 5 个。

pixverse/pixverse-v5.6-it2v

5

pixverse/pixverse-v5.6-kf2v

5

pixverse/pixverse-v5.6-r2v

5

### **可灵系列**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

**模型名称**

**限流条件（超出任一数值时触发限流）**

**每秒钟任务下发接口RPS限制**

**同时处理中任务数量（并发数）**

kling/kling-v3-omni-video-generation

5

10

> 同一阿里云百炼API Key 下，可灵系列的 4 个模型（[图像](#fdd6e348d2md4)及[视频](#kling-third-party-limit)）共享 10 个并发数。即这 4 个模型处于运行状态的任务总数加起来不能超过 10 个。

kling/kling-v3-video-generation

5

### **Vidu系列**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

**模型服务**

**模型名称**

**限流条件（超出任一数值时触发限流）**

**每秒钟任务下发接口RPS限制**

**同时处理中任务数量（并发数）**

文生视频

vidu/viduq3-turbo\_text2video

5

5

> 同一个阿里云百炼API Key 在 17 个模型间共享并发额度。即这 17 个模型处于运行状态的任务总数加起来不能超过 5 个。

vidu/viduq3-pro\_text2video

5

vidu/viduq2\_text2video

5

图生视频-基于首帧

vidu/viduq3-turbo\_img2video

5

vidu/viduq3-pro\_img2video

5

vidu/viduq2-turbo\_img2video

5

vidu/viduq2-pro\_img2video

5

vidu/viduq2-pro-fast\_img2video

5

图生视频-基于首尾帧

vidu/viduq3-turbo\_start-end2video

5

vidu/viduq3-pro\_start-end2video

5

vidu/viduq2-turbo\_start-end2video

5

vidu/viduq2-pro\_start-end2video

5

参考生视频

vidu/viduq3-mix\_reference2video

5

vidu/viduq3\_reference2video

5

vidu/viduq3-turbo\_reference2video

5

vidu/viduq2-pro\_reference2video

5

vidu/viduq2\_reference2video

5

## **3D模型生成-第三方模型**

### **Tripo系列**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

**模型名称**

**限流条件（超出任一数值时触发限流）**

**每秒钟任务下发接口RPS限制**

**同时处理中任务数量（并发数）**

Tripo/Tripo-H3.1

5

10

> 同一个阿里云百炼API Key 在 2 个模型间共享额度。即这 2 个模型处于运行状态的任务总数加起来不能超过 10 个。

Tripo/Tripo-P1.0

5

## **向量模型**

### **文本向量**

## **中国内地**

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型名称**

**限流条件（超出任一数值时触发限流）**

**每秒钟调用次数（RPS）**

**每分钟消耗Token数（TPM）/作业数**

> **仅输入Token**

text-embedding-v1

30

1,200,000

text-embedding-v2

text-embedding-v3

text-embedding-v4

text-embedding-async-v1

1

当前用户在系统通用文本向量异步作业排队中和运行中的作业数量不超过50个。

另外，为了避免大量突发的作业占据太多资源，限制并发的作业数为3个，即任意时间，单个用户最多只有3个通用文本向量的异步作业在并发运行，其他的作业只能在队列中等待。

text-embedding-async-v2

## **国际**

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）/作业数**

> **含输入与输出Token**

text-embedding-v3

6,000

24,000,000

### **多模态向量**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

**模型名称**

**限流条件**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **仅输入Token**

qwen3-vl-embedding

2,400

1,200,000

qwen2.5-vl-embedding

1,200

600,000

tongyi-embedding-vision-plus

600

200,000

tongyi-embedding-vision-flash

tongyi-embedding-vision-flash-2026-03-06

1,200

9,600,000

tongyi-embedding-vision-plus-2026-03-06

multimodal-embedding-v1

120

1,000,000

## **排序模型**

### **排序模型**

## **中国内地**

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

qwen3-rerank

5,400

5,000,000,000

qwen3-vl-rerank

600

9,000,000

gte-rerank-v2

5,040

4,980,000,000

## **国际**

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

qwen3-rerank

5,400

5,000,000,000

gte-rerank-v2

5,040

4,980,000,000

## **行业**

### **通义法睿（法律模型）**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

farui-plus

240

1,000,000

### **意图理解**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

tongyi-intent-detect-v3

1,200

1,000,000

### **角色扮演**

## **中国内地**

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

qwen-plus-character

120

500,000

qwen-flash-character

qwen-flash-character-2026-02-26

## **国际**

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

qwen-plus-character

120

500,000

qwen-flash-character

120

500,000

qwen-plus-character-ja

120

500,000

### 界面交互

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

**模型名称**

**限流条件（超出任一数值时触发限流）**

> **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

gui-plus

80

540,000

gui-plus-2026-02-26

100

540,000

## **已下线模型**

> 详细信息，请参见 [模型下线机制说明](https://help.aliyun.com/zh/model-studio/model-depreciation) 。

## **2026年3月30日下线**

**类别**

**模型名称**

**限流条件（超出任一数值时触发限流）**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

千问语言模型

qwen2-72b-instruct

0

0

qwen2-57b-a14b-instruct

qwen2-7b-instruct

qwen2-1.5b-instruct

qwen2-0.5b-instruct

qwen1.5-110b-chat

qwen1.5-72b-chat

qwen1.5-32b-chat

qwen1.5-14b-chat

qwen1.5-7b-chat

qwen1.5-1.8b-chat

qwen1.5-0.5b-chat

qwen2.5-coder-3b-instruct

qwen2.5-coder-1.5b-instruct

qwen2.5-coder-0.5b-instruct

qwen2.5-math-1.5b-instruct

千问VL

qwen2-vl-72b-instruct

qwen2-vl-7b-instruct

qwen2-vl-2b-instruct

qwen-vl-v1

qwen-vl-chat-v1

MiniMax-abab

abab6.5g-chat

abab6.5t-chat

abab6.5s-chat

StableDiffusion文生图

stable-diffusion-xl

stable-diffusion-v1.5

stable-diffusion-3.5-large

stable-diffusion-3.5-large-turbo

FLUX文生图

flux-schnell

flux-dev

flux-merged

千问Audio

qwen2-audio-instruct

qwen-audio-chat

OpenNLU

opennlu-v1

## **2026年1月30日下线**

**类别**

**模型名称**

**限流条件（超出任一数值时触发限流）**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

千问Max

qwen-max-2024-04-03

0

0

千问Plus

qwen-plus-2024-11-27

qwen-plus-2024-11-25

qwen-plus-2024-09-19

qwen-plus-2024-08-06

qwen-plus-2024-07-23

千问Turbo

qwen-turbo-2024-09-19

qwen-turbo-2024-06-24

千问VL

qwen-vl-max-2024-10-30

qwen-vl-max-2024-08-09

qwen-vl-plus-2024-08-09

千问Audio

qwen-audio-turbo-2024-12-04

qwen-audio-turbo-2024-08-07

qwen-audio-asr-2024-12-04

## **2025年7月30日下线**

**类别**

**模型名称**

**限流条件（超出任一数值时触发限流）**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

千问VL

qwen-vl-plus-2023-12-01

0

0

零一万物

yi-large

yi-medium

yi-large-rag

yi-large-turbo

Dolly

dolly-12b-v2

## **2025年7月2日下线**

**类别**

**模型名称**

**限流条件（超出任一数值时触发限流）**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

Llama-仅文本输入

llama3.3-70b-instruct

0

0

llama3.2-3b-instruct

llama3.2-1b-instruct

llama3.1-405b-instruct

llama3.1-70b-instruct

llama3.1-8b-instruct

llama3-70b-instruct

llama3-8b-instruct

llama2-13b-chat-v2

llama2-7b-chat-v2

Llama-文本和图像输入

llama3.2-90b-vision-instruct

llama3.2-11b-vision

百川-开源版

baichuan2-13b-chat-v1

baichuan2-7b-chat-v1

baichuan-7b-v1

ChatGLM

chatglm3-6b

chatglm-6b-v2

姜子牙

ziya-llama-13b-v1

BELLE

belle-llama-13b-2m-v1

元语

chatyuan-large-v2

BiLLa

billa-7b-sft-v1

**类别**

**模型名称**

**限流条件（超出任一数值时触发限流）**

**每秒钟任务下发接口RPS限制**

**同时处理中任务数量**

动漫人物生成

wanx-style-cosplay-v1

0

0

图配文

wanx-ast

创意文字生成-WordArt锦书

wordart-surnames

AnyText图文融合

wanx-anytext-v1

## **2025年5月8日下线**

**类别**

**模型名称**

**限流条件（超出任一数值时触发限流）**

**替代模型**

**每分钟调用次数（RPM）**

**每分钟消耗Token数（TPM）**

> **含输入与输出Token**

文本生成-千问

qwen-max-2024-01-07

（qwen-max-0107）

0

0

qwen-max

qwen-plus-2024-06-24

（qwen-plus-0624）

qwen-plus

qwen-plus-2024-02-06

（qwen-plus-0206）

qwen-turbo-2024-02-06

（qwen-turbo-0206）

qwen-turbo

qwen-vl-max-2024-02-01

（qwen-vl-max-0201）

qwen-vl-max

文本生成-千问-开源版

qwen-72b-chat

qwen2.5-72b-instruct

qwen-14b-chat

qwen2.5-14b-instruct

qwen-7b-chat

qwen2.5-7b-instruct

qwen-1.8b-chat

qwen2.5-1.5b-instruct

qwen-1.8b-longcontext-chat

qwen2.5-1.5b-instruct

qwen2-math-72b-instruct

qwen2.5-math-72b-instruct

qwen2-math-7b-instruct

qwen2.5-math-7b-instruct

qwen2-math-1.5b-instruct

qwen2.5-math-7b-instruct

**类别**

**模型名称**

**限流条件（超出任一数值时触发限流）**

**替代模型**

**任务下发接口RPS限制**

**同时处理中任务数量**

幻影人像Motionshop视频生成模型

motionshop-video-detect

0

0

使用animate-anyone-gen2的“按视频背景生成”功能，可达到近似效果

motionshop-gen3d

motionshop-synthesis
