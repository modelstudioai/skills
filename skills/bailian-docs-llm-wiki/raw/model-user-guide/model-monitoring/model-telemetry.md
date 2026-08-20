# 模型监控

在阿里云百炼控制台，模型可观测能力由以下入口提供：**模型监控&告警**（含**监控**与**告警**两个页签，左侧导航为「监控告警」）用于实时查看指标并配置告警；**模型日志**（含**审计日志**与**推理日志**两个页签）用于查看调用记录与历史对话；**数据投递**用于将监控数据投递到云监控 Prometheus、将日志投递到日志服务 SLS。

## 支持的模型

-   **监控：**实时监控开箱即用、无需开通，支持[选择模型](raw/model-user-guide/get-started-with-models/models.md)中的所有模型，包括基于它们调优后的自定义模型。如需将监控数据投递到云监控 Prometheus（用于 Grafana 或自建应用接入），可在北京、上海、新加坡、弗吉尼亚地域开启**监控数据投递**。
-   **告警功能：**支持北京、新加坡、弗吉尼亚地域下的所有模型。

## 监控模型运行

系统会自动采集主账号下所有业务空间内的模型调用数据。当有[直接或间接](https://help.aliyun.com/zh/model-studio/model-telemetry#0806932be6woi)模型调用发生时，系统会自动收集并同步相关数据至目标业务空间的[模型监控](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)列表中。

> 列表记录按“模型 + 业务空间”维度生成。新模型在首次数据同步完成后自动加入列表（实时监控开箱即用，数据从调用发生到可查询通常有 1-2 分钟延迟，请耐心等待）。

列表顶部「**监控数据**」以卡片形式汇总**模型总量**、**总调用次数**、**总失败次数**、**平均调用时长**、**平均首包时长**。

「模型监控」表格列出各模型的**模型Code**、**业务空间**、**调用总量**、**调用失败量**、**失败率**、**平均调用时长**、**平均首Token延时**（除模型Code、业务空间外均可排序），操作列提供**监控**、**日志**入口。列表工具栏还提供**日志回流**入口，可将推理日志回流为训练数据集。

> 默认业务空间成员可查看所有业务空间的模型调用情况；子业务空间成员仅能查看当前空间的数据，无法切换查看其他业务空间数据。

在列表中找到目标模型后，点击其右侧**操作**列的**监控**，可查询以下**4**类监控指标：

-   **安全：**识别对话中的违规内容，例如`内容安全错误次数`。
-   **成本：**评估模型的成本效益，例如`平均单次请求调用量`。
-   **性能：**观察模型的性能变化，例如`调用时长`、`首Token延时`。
-   **错误：**判断模型的稳定性，例如`失败次数`、`失败率`。

您可基于上述指标创建[告警](https://help.aliyun.com/zh/model-studio/model-telemetry#b8fcd646d5avf)，以便及时发现和处理异常。

点击操作列「监控」进入模型详情页，详情页含**监控**、**日志**两个页签。监控页签下分为**调用统计**与**性能指标**两类。

此页签可查看**安全、成本、错误**相关指标（如调用次数、失败次数等）。支持按API-KEY、[推理类型](raw/model-user-guide/model-monitoring/model-telemetry.md)、时间范围以及时间精度（按分钟/按小时）进行筛选。

-   **限流错误次数：**指因429状态码导致的调用失败。
-   **内容安全错误次数：**指输入或输出包含疑似敏感或高风险内容（例如涉黄、涉政和广告等）被[内容安全服务](https://www.aliyun.com/product/content-moderation/guardrail)拦截。

调用统计页签的失败次数图表支持点击**失败详情**查看失败明细，便于定位调用失败原因。

**性能指标**

此页签可查看RPM、TPM、调用时长、首Token延时以及非首Token延时等**性能**相关指标。

## 查看 Token 消耗

在实际使用中，调整模型的参数、系统提示词等操作均会改变模型的Token消耗。为统计和精细化管理成本，模型监控提供成本监控相关功能：

-   **汇总：**按业务空间维度汇总模型的历史Token消耗，并可按时间范围和API Key进一步筛选。
-   **追踪：**记录每一次模型调用的Token消耗。
-   **告警：**设置Token消耗阈值，当指定模型出现异常消耗时，系统立即告警。

### 查看模型历史 Token 消耗

-   查看最近**30**天的Token消耗：
    
    1.  当模型出现在目标业务空间的[模型监控](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)列表中后，点击其右侧**操作**列的**监控**。
    2.  在调用统计页签的**调用量**区域，可以查看Token消耗数据。
-   查看更早的用量：在[费用与成本](https://billing-cost.console.aliyun.com/finance/expense-report/expense-detail-by-instance?month=2025-02&statisticItem=DEFAULT_CHARGE_ITEM&commodityCode%5BfilterMode%5D=IN&commodityCode%5Bvalues%5D=sfm_deployment_public_cn%26sfm_inference_public_cn%26sfm_training_public_cn&statisticCycle=MONTHLY_SUMMARY)页面查询。
    

### 查看某次调用的 Token 消耗

> 该功能目前适用于**华北2（北京）**、新加坡地域的部分模型，弗吉尼亚地域同样支持。

**说明****数据说明：**推理日志从调用发生到可查询存在分钟级延迟，请耐心等待；调用次数、Token 总量等用量汇总通常有 1-2 分钟延迟。如遇无数据或查不到记录的情况，请先确认已等待足够的数据同步时间。仅记录**开启推理日志后**的调用数据，开通前的历史调用无法追溯。

1.  使用主账号（[或拥有足够权限的子账号](raw/model-user-guide/model-monitoring/model-telemetry.md)）登录，在目标业务空间的[模型监控（北京）](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)页面，点击右上角的**模型监控配置**，开启推理日志（审计日志默认开启、无需配置）。
    
    > 开启推理日志后，系统即开始记录该业务空间内每一次模型调用的输入与输出。从调用发生到日志被记录存在分钟级延迟，请耐心等待。
    
2.  在模型监控列表中找到目标模型，点击其右侧**操作**列的**日志**。
    
3.  **日志**页签以表格形式展示该模型的[实时推理](raw/model-user-guide/model-monitoring/model-telemetry.md)调用记录，表格包含**Request ID/调用时间**、**调用时长**、**状态码**（支持筛选）、**错误码**、**用量**、**请求和响应**、**操作**等列。其中**用量**字段即为本次调用的Token消耗。
    

### 创建异常消耗告警

-   请参见[建立主动告警](https://help.aliyun.com/zh/model-studio/model-telemetry#b8fcd646d5avf)。

## 模型日志

**重要**该功能目前适用于**华北2（北京）**、新加坡地域的部分模型，弗吉尼亚地域同样支持。

模型日志分为**审计日志**和**推理日志**两个页签。**审计日志**默认开启、无需配置，记录每一次调用的 Request ID、处理时间、模型名、API Key、用量、延迟、状态码等元数据，存储在百炼平台侧；**推理日志**需手动开启（前提是开启日志投递到 SLS，会产生费用），在审计日志基础上额外记录每一次对话的输入（Prompt）与输出（Response），是故障排查和内容审计的关键工具。

**说明****数据说明：**日志从调用发生到可查询存在分钟级延迟，请耐心等待。审计日志默认记录，无需开通；推理日志仅记录**开启推理日志后**的调用数据（Prompt/Response），开通前的历史调用无法追溯。

### 步骤一：开启日志记录

**审计日志**默认开启、无需配置，系统自动记录每一次模型调用的 Request ID、处理时间、模型名、API Key、用量、延迟、状态码等元数据，存储在百炼平台侧。如需记录完整的对话输入与输出，请开启**推理日志**：使用主账号（[或拥有足够权限的子账号](raw/model-user-guide/model-monitoring/model-telemetry.md)）登录，在目标业务空间的[模型监控（北京）](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)页面，点击右上角的**模型监控配置**，开启推理日志并将日志投递到 SLS（会产生日志服务费用）。

> 开启推理日志后，系统即开始记录该业务空间内每一次模型调用的输入与输出。从调用发生到日志被记录存在分钟级延迟，请耐心等待。

> 如需停止记录，只需在模型监控配置中关闭推理日志即可。

**说明**推理日志仅记录 HTTP API 调用的输入与输出。WebSocket 实时调用（如 qwen-audio 实时语音模型）产生的转写文本（partial/final）和语音回复音频仅在会话中传输给客户端，不写入推理日志。审计日志会记录此类调用的模型名、状态码、时长和 Token 用量，但不包含转写文本和音频内容。

### 步骤二：查看历史对话

1.  在模型监控列表中找到目标模型，点击其右侧**操作**列的**日志**。
2.  **日志**页签以表格形式展示该模型的[实时推理](raw/model-user-guide/model-monitoring/model-telemetry.md)调用记录，表格包含**Request ID/调用时间**、**调用时长**、**状态码**（支持筛选）、**错误码**、**用量**、**请求和响应**、**操作**等列。其中**请求和响应**字段分别对应本次调用的输入与输出。

支持请求和响应的模型

-   千问Max
    
    -   qwen3-max、qwen3-max-preview、qwen3-max-2025-09-23及之后的快照版本
    -   qwen-max
-   千问Plus
    
    -   qwen3.7-plus、qwen3.7-plus-2026-05-26及之后的快照版本
    -   qwen3.6-plus、qwen3.6-plus-2026-04-02及之后的快照版本
    -   qwen3.5-plus、qwen3.5-plus-2026-02-15及之后的快照版本
    -   qwen-plus、qwen-plus-latest、qwen-plus-2025-12-01及之后的快照版本
-   千问Flash
    
    -   qwen3.5-flash、qwen3.5-flash-2026-02-23
    -   qwen-flash、qwen-flash-2025-07-28
-   千问Turbo：qwen-turbo
    
-   千问Coder：qwen3-coder-flash、qwen3-coder-flash-2025-07-28、qwen3-coder-plus、qwen3-coder-plus-2025-07-22、qwen3-coder-plus-2025-09-23
    
-   开源模型：qwen3-235b-a22b、qwen3-235b-a22b-instruct-2507、qwen3-235b-a22b-thinking-2507、qwen3-30b-a3b、qwen3-30b-a3b-instruct-2507、qwen3-30b-a3b-thinking-2507、qwen3-next-80b-a3b-instruct、qwen3-next-80b-a3b-thinking、qwen3-coder-480b-a35b-instruct
    
-   三方模型：deepseek-v3.1、deepseek-v3.2、deepseek-v3.2-exp
    

并非所有模型都支持推理日志（请求/响应内容记录）。是否支持由模型本身决定，与模型是否为多模态无关。当所选模型不支持时，界面会显示**当前模型暂不支持日志**。

请注意：请求和响应内容**仅在开启推理日志后**才会被采集，开通前的历史调用不会补录。若某次调用的输出内容缺失或存在日志缺失，请先确认该模型是否支持推理日志，以及推理日志是否已在调用发生前完成开通。

## 建立主动告警

**重要**该功能目前适用于新加坡、北京和弗吉尼亚地域。

模型的静默失败（如超时、Token消耗突增），传统应用日志难以发现。模型监控支持对监控指标（如成本、失败率、响应延迟）设置告警。一旦指标出现异常，系统立即告警。

模型告警页面包含**告警规则**和**告警历史**两个页签。**告警历史**页签可按告警时间、告警规则、告警等级、状态筛选查看历史告警记录，点击详情可查看告警详情。

### 步骤一：授权云监控服务角色

1.  首次创建告警规则时，系统会引导您授权云监控（CloudMonitor）服务关联角色，用于下发和管理告警通知。使用主账号（[或拥有足够权限的子账号](raw/model-user-guide/model-monitoring/model-telemetry.md)）按界面提示完成一次性授权即可，无需开启监控数据投递。

### 步骤二：创建告警规则

1.  在模型告警（[北京](https://bailian.console.aliyun.com/?tab=model#/model-alert) 或[新加坡](https://modelstudio.console.aliyun.com/?tab=dashboard#/model-alert)）页面，点击右上角的**创建告警规则**。
    
2.  在对话框中，选择要监控的模型和监控模板，确认无误后点击**确定**。当指定的监控指标（如调用统计或性能指标）出现异常时，系统将通知您的团队。
    
    -   **通知方式：**支持短信、电子邮件、电话、钉钉群机器人、企业微信机器人及Webhook。
        
    -   **告警等级：**分为**普通**、**警告**、**错误**和**紧急**，不支持自定义新增或修改。各等级与通知渠道的对应关系如下：
        
        -   紧急（CRITICAL）: 电话、短信、邮件
        -   错误（ERROR）: 短信、邮件
        -   警告（WARNING）: 短信、邮件
        -   普通（INFO）: 邮件

## 监控数据投递：接入 Grafana 与自建应用

模型监控的监控指标数据存储在您的私有Prometheus实例中，并支持标准的Prometheus HTTP API，可用于接入 Grafana 或您的自建应用进行可视化分析。

## 步骤一：获取数据源HTTP API地址

1.  确保已在目标业务空间开启**监控数据投递**（在模型监控页面右上角的模型监控配置中开启，将监控数据投递到云监控 Prometheus）。
    
2.  在[模型监控（北京）](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)、[模型监控（弗吉尼亚）](https://modelstudio.console.aliyun.com/us-east-1?tab=dashboard#/model-telemetry)或[模型监控（新加坡）](https://modelstudio.console.aliyun.com/?tab=dashboard#/model-telemetry)页面，点击右上角的**模型监控配置**。点击云监控Prometheus实例右侧的**查看详情**。
    
3.  在**设置**页面，根据您的客户端网络环境（公网或VPC访问），复制对应的 HTTP API 地址。
    

## 步骤二：接入 Grafana 或自建应用

#### 接入自建应用

通过Prometheus HTTP API获取监控数据的示例如下。完整 API 用法，请参考[Prometheus HTTP API文档](https://prometheus.io/docs/prometheus/latest/querying/api/)。

-   **示例1：**查询阿里云账号下全部业务空间在指定时间范围内（2025年11月20日全天，UTC时间）所有模型的Token消耗（query=`model_usage`），步长`step=60s`。
    
    **示例**
    
    **参数说明**
    
    ```
    GET {HTTP API}/api/v1/query_range?query=model_usage&start=2025-11-20T00:00:00Z&end=2025-11-20T23:59:59Z&step=60s
    
    Accept: application/json
    Content-Type: application/json
    Authorization: Basic base64Encode(AccessKey:AccessKeySecret)
    ```
    
    -   **query：**`query`对应的值可替换为下方**监控指标**列表中的任意指标名称。
        
        展开查看监控指标
        
        **类型**
        
        **指标名称**
        
        **描述**
        
        **调用次数**
        
        model\_call\_count
        
        模型调用次数总和
        
        **调用时长**
        
        model\_call\_duration\_total
        
        模型调用时长总和
        
        model\_call\_duration
        
        模型调用时长均值
        
        model\_call\_duration\_p50
        
        模型调用时长p50
        
        model\_call\_duration\_p99
        
        模型调用时长p99
        
        model\_first\_token\_duration\_total
        
        模型首包时长总和
        
        model\_first\_token\_duration
        
        模型首包时长均值
        
        model\_first\_token\_duration\_p50
        
        模型首包时长p50
        
        model\_first\_token\_duration\_p99
        
        模型首包时长p99
        
        **非首包时长**
        
        model\_generation\_duration\_per\_token\_total
        
        模型非首包时长总和
        
        model\_generation\_duration\_per\_token
        
        模型非首包时长均值
        
        model\_generation\_duration\_per\_token\_p50
        
        模型非首包时长p50
        
        model\_generation\_duration\_per\_token\_p99
        
        模型非首包时长p99
        
        **TPS**
        
        model\_tps\_per\_request
        
        单次请求输出 Token 速度（TPS），每秒生成 Token 数，衡量模型生成速度（需开启监控数据投递后支持）
        
        **用量**
        
        model\_usage
        
        模型用量总和
        
        **关于 TPS 指标：**`model_tps_per_request` 仅在开启**监控数据投递**后展示，监控数据投递为收费功能。TPS（每秒生成 Token 数）与非首包时长（每 Token 的平均生成耗时）呈倒数关系（TPS ≈ 1 ÷ 非首包时长均值）。排查响应慢的问题时，建议结合首 Token 延时（TTFT）、非首 Token 延时及输入 Token 量综合分析，单次调用总耗时还受输入长度、网络等因素影响，不能仅凭 TPS 判断。TPS 触发的是按请求维度的限流，区别于 TPM（每分钟 Token 数）的按账号维度限流。
        
    -   **HTTP API：**`{HTTP API}`需替换为前面[步骤一](https://help.aliyun.com/zh/model-studio/model-telemetry#title_tkb_ds1_4p5)获取的HTTP API地址。
        
    -   **Authorization：**需将阿里云账号的 `AccessKey:AccessKeySecret` 拼接后进行Base64编码，并以 `Basic 编码后字符串` 的形式提供。
        
        > **示例值：**Basic TFRBSTV3OWlid0U4XXXXU0xb1dZMFVodmRsNw==
        
        > **请注意：**[AccessKey](https://help.aliyun.com/zh/sdk/developer-reference/configure-the-alibaba-cloud-accesskey-environment-variable-on-linux-macos-and-windows-systems)及[AccessKey Secret](https://help.aliyun.com/zh/sdk/developer-reference/configure-the-alibaba-cloud-accesskey-environment-variable-on-linux-macos-and-windows-systems)与前面步骤一的Prometheus实例必须归属同一阿里云账号。
        
    
-   **示例2：**在**示例1**基础上增加筛选，仅获取指定模型（model=`qwen-plus`）在指定业务空间（workspace\_id=`llm-nymssti2mzww****`）内的Token消耗。
    
    **示例**
    
    **说明**
    
    ```
    GET {HTTP API}/api/v1/query_range?query=model_usage{workspace_id="llm-nymssti2mzww****",model="qwen-plus"}&start=2025-11-20T00:00:00Z&end=2025-11-20T23:59:59Z&step=60s
    
    Accept: application/json
    Content-Type: application/json
    Authorization: Basic base64Encode(AccessKey:AccessKeySecret)
    ```
    
    -   **query：**通过`{}` 包裹多个过滤条件，条件之间以英文逗号分隔，例如：`{workspace_id="值1",model="值2"}` 。**支持的过滤条件（LabelKey）**清单如下。
        
        展开查看支持的过滤条件
        
        **LabelKey**
        
        **描述**
        
        **user\_id**
        
        阿里云账号ID。
        
        > RAM用户为UID。[如何获取](https://help.aliyun.com/zh/ram/user-guide/view-the-basic-information-about-a-ram-user)
        
        **apikey\_id**
        
        API Key ID（非API Key），可在**密钥管理**（[北京](https://bailian.console.aliyun.com/?tab=model#/api-key) |[美国](https://modelstudio.console.aliyun.com/us-east-1?tab=dashboard#/api-key)| [新加坡](https://modelstudio.console.aliyun.com/?tab=playground#/api-key)）页面获取。
        
        **说明**apikey\_id 值为 -1 表示调用源自阿里云百炼控制台，而非通过API。
        
        **workspace\_id**
        
        业务空间ID。如何获取
        
        **model**
        
        模型。
        
        **protocol**
        
        协议类型。可能取值：
        
        -   **HTTP：**HTTP非流式
        -   **SSE：**HTTP流式
        -   **WS：**Websocket协议
        
        **sub\_protocol**
        
        子协议。可能取值：
        
        -   **DEFAULT：**同步调用
            
        -   **ASYNC：**异步调用
            
            > 常见于图像生成模型。文本生成图像
            
        
        **status\_code**
        
        HTTP状态码。
        
        > 仅`model_call_count`监控指标支持该LabelKey。
        
        **error\_code**
        
        错误码。
        
        > 仅`model_call_count`监控指标支持该LabelKey。
        
        **usage\_type**
        
        用量类型。
        
        > 仅`model_usage`监控指标支持该LabelKey。
        
        可能取值：
        
        -   total\_tokens
        -   input\_tokens
        -   output\_tokens
        -   cache\_tokens
        -   image\_tokens
        -   audio\_tokens
        -   video\_tokens
        -   image\_count
        -   audio\_count
        -   video\_count
        -   duration
        -   characters
        -   audio\_tts
        -   times
        
    

#### 接入 Grafana

在 Grafana（自建或阿里云 Grafana 服务）中添加模型监控数据源。此处以Grafana 10.x（英文版）为例。其他版本的操作类似，详情请参考[Grafana官方文档](https://grafana.com/docs/grafana/latest/datasources/prometheus/configure/)。

1.  **添加数据源：**
    1.  使用管理员账号登录Grafana。点击页面左上角的图标，选择**AdministrationData sources**。点击**\+ Add new data source**，数据源类型选择**Prometheus**。
        
    2.  在**Settings**页签配置数据源信息：
        
        -   **Name：**输入自定义的名称。
            
        -   **Prometheus server URL：**输入前面[步骤一](https://help.aliyun.com/zh/model-studio/model-telemetry#title_tkb_ds1_4p5)获取的HTTP API地址。
            
        -   **Auth：**开启**Basic auth**，并设置**User**（阿里云账号的[AccessKey](https://help.aliyun.com/zh/sdk/developer-reference/configure-the-alibaba-cloud-accesskey-environment-variable-on-linux-macos-and-windows-systems)）及**Password**（阿里云账号的[AccessKey Secret](https://help.aliyun.com/zh/sdk/developer-reference/configure-the-alibaba-cloud-accesskey-environment-variable-on-linux-macos-and-windows-systems)）。
            
            > AccessKey及AccessKeySecret与前面步骤一的Prometheus实例必须归属同一阿里云账号。
            
        
    3.  点击页签底部的**Save & Test**。
        
2.  **指标查询：**
    1.  点击Grafana页面左上角的图标，在左侧导航栏中点击**Dashboards**。
        
    2.  点击**Dashboards**页面右侧的**NewNew dashboard**创建一个新的仪表盘。
        
    3.  点击**\+ Add visualization**，并选择您刚创建的数据源。
        
    4.  在**Edit Panel**页面点击**Query**页签，在**A**区域的**Label filters**字段中选择**_name_**及指标名称。以查询模型Token消耗`model_usage`为例：
        
        **示例**
        
        **说明**
        
        图中`_name_`对应的值（`model_usage`）可替换为下方**监控指标**列表中的任意指标名称。
        
        展开查看监控指标
        
        **类型**
        
        **指标名称**
        
        **描述**
        
        **调用次数**
        
        model\_call\_count
        
        模型调用次数总和
        
        **调用时长**
        
        model\_call\_duration\_total
        
        模型调用时长总和
        
        model\_call\_duration
        
        模型调用时长均值
        
        model\_call\_duration\_p50
        
        模型调用时长p50
        
        model\_call\_duration\_p99
        
        模型调用时长p99
        
        model\_first\_token\_duration\_total
        
        模型首包时长总和
        
        model\_first\_token\_duration
        
        模型首包时长均值
        
        model\_first\_token\_duration\_p50
        
        模型首包时长p50
        
        model\_first\_token\_duration\_p99
        
        模型首包时长p99
        
        **非首包时长**
        
        model\_generation\_duration\_per\_token\_total
        
        模型非首包时长总和
        
        model\_generation\_duration\_per\_token
        
        模型非首包时长均值
        
        model\_generation\_duration\_per\_token\_p50
        
        模型非首包时长p50
        
        model\_generation\_duration\_per\_token\_p99
        
        模型非首包时长p99
        
        **TPS**
        
        model\_tps\_per\_request
        
        单次请求输出 Token 速度（TPS），每秒生成 Token 数，衡量模型生成速度（需开启监控数据投递后支持）
        
        **用量**
        
        model\_usage
        
        模型用量总和
        
        增加以下Label filters进一步筛选：
        
        展开查看支持的过滤条件
        
        **LabelKey**
        
        **描述**
        
        **user\_id**
        
        阿里云账号ID。
        
        > RAM用户为UID。[如何获取](https://help.aliyun.com/zh/ram/user-guide/view-the-basic-information-about-a-ram-user)
        
        **apikey\_id**
        
        API Key ID（非API Key），可在**密钥管理**（[北京](https://bailian.console.aliyun.com/?tab=model#/api-key) |[美国](https://modelstudio.console.aliyun.com/us-east-1?tab=dashboard#/api-key)| [新加坡](https://modelstudio.console.aliyun.com/?tab=playground#/api-key)）页面获取。
        
        **说明**apikey\_id 值为 -1 表示调用源自阿里云百炼控制台，而非通过API。
        
        **workspace\_id**
        
        业务空间ID。如何获取
        
        **model**
        
        模型。
        
        **protocol**
        
        协议类型。可能取值：
        
        -   **HTTP：**HTTP非流式
        -   **SSE：**HTTP流式
        -   **WS：**Websocket协议
        
        **sub\_protocol**
        
        子协议。可能取值：
        
        -   **DEFAULT：**同步调用
            
        -   **ASYNC：**异步调用
            
            > 常见于图像生成模型。文本生成图像
            
        
        **status\_code**
        
        HTTP状态码。
        
        > 仅`model_call_count`监控指标支持该LabelKey。
        
        **error\_code**
        
        错误码。
        
        > 仅`model_call_count`监控指标支持该LabelKey。
        
        **usage\_type**
        
        用量类型。
        
        > 仅`model_usage`监控指标支持该LabelKey。
        
        可能取值：
        
        -   total\_tokens
        -   input\_tokens
        -   output\_tokens
        -   cache\_tokens
        -   image\_tokens
        -   audio\_tokens
        -   video\_tokens
        -   image\_count
        -   audio\_count
        -   video\_count
        -   duration
        -   characters
        -   audio\_tts
        -   times
        
    5.  点击**Run queries**进行查询。
        
        > 如果图表中成功渲染出数据，则说明配置成功。否则请检查：1）填写的HTTP API地址或AccessKey及AccessKeySecret是否正确；2）前面[步骤一](https://help.aliyun.com/zh/model-studio/model-telemetry#title_tkb_ds1_4p5)的Prometheus实例中是否有监控数据。
        

## 内置监控与监控数据投递

模型监控的实时监控作为基础能力**开箱即用、无需开通、免费**，随阿里云百炼的开通自动生效，覆盖主账号下所有业务空间。如需将监控数据投递到云监控 Prometheus，以便通过 Grafana 或自建应用查看，可按需开启**监控数据投递**。

> **内置监控：**作为基础服务提供，随阿里云百炼的开通自动开启，不支持关闭，数据分钟级更新，免费。

> **监控数据投递：**需主账号（[或拥有足够权限的子账号](raw/model-user-guide/model-monitoring/model-telemetry.md)）在目标业务空间的模型监控页面右上角的模型监控配置中手动开启，支持关闭。开启后，监控数据额外写入云监控 Prometheus，可对接 Grafana 或自建应用。仅记录开启监控数据投递后的调用数据。

**对比项**

**内置监控（默认开启）**

**监控数据投递（需手动开启）**

**是否需开通**

无需开通，开箱即用

需手动开启

**数据延时**

分钟级（1-2 分钟）

分钟级

**在控制台查看调用统计与性能指标**

支持

支持

**对接 Grafana / 自建应用（Prometheus）**

不支持

支持

**作用范围**

主账号下所有业务空间

仅在开启的业务空间内生效

**计费**

免费

监控数据写入云监控 CMS，收费

## 配额与限制

-   **数据保留周期：**监控数据默认保留**30天**。开启推理日志后，调用数据写入日志服务SLS并保留**30天**，可在SLS控制台调整保留时间。关闭推理日志后，日志不再同步到SLS。如需查询更早的用量信息，请通过[费用与成本](https://billing-cost.console.aliyun.com/finance/expense-report/expense-detail-by-instance?month=2025-02&statisticItem=DEFAULT_CHARGE_ITEM&commodityCode%5BfilterMode%5D=IN&commodityCode%5Bvalues%5D=sfm_deployment_public_cn%26sfm_inference_public_cn%26sfm_training_public_cn&statisticCycle=MONTHLY_SUMMARY)页面查询。
    
-   **告警模板限制：**每个业务空间最多可创建**100**个告警模板。
    
-   **API限制：**模型监控的监控指标数据请通过[Prometheus HTTP API](https://help.aliyun.com/zh/model-studio/model-telemetry#1f0d765b83nwb)查询。
    
    -   **替代方案：**如需通过API获取单次调用Token消耗，可在每次调用模型时从响应中的`usage`字段提取当前调用数据。该字段结构示例如下（更多说明请参见[千问API参考](raw/model-api-reference/qwen-api-reference.md)）：

```
{
  "prompt_tokens": 3019,
  "completion_tokens": 104,
  "total_tokens": 3123,
  "prompt_tokens_details": {
    "cached_tokens": 2048
  }
}
```

-   **API Key 用量限额：**当前不支持为单个 API Key 设置月度或每日 Token 消耗上限并自动停服（即不支持硬性阻断，无法实现额度用尽后自动禁用 API 调用）。如需防止意外欠费，可采用以下替代方案：
    
    -   **告警通知 + 手动禁用 Key：**配置**模型告警**后，可对 Token 消耗设置告警阈值，当消耗超出阈值时接收消费预警通知，再人工介入处理（如手动禁用对应 API Key）。
    -   **免费额度用完即停：**适用于仅使用免费配额的场景，开启后免费额度耗尽时自动停止调用。

## 计费说明

-   **内置监控：**免费。
-   **监控数据投递：**开启后，监控数据将写入[云监控CMS](https://cloudmonitornext.console.aliyun.com/newOverview)服务并产生费用。具体计费方式参见[云监控CMS计费概述](https://help.aliyun.com/zh/cms/cloudmonitor-1-0/product-overview/billing-overview-1)。
-   **推理日志：**开启后，分钟级的日志数据将写入[日志服务SLS](https://sls.console.aliyun.com/)服务并产生费用。具体计费方式参见[日志服务SLS计费概述](https://help.aliyun.com/zh/sls/billing-overview)。

## 常见问题

**为什么调用了模型，但在模型监控中查不到调用次数和消耗Token数？**

按以下步骤排查：

1.  **数据延迟：**确认是否已等待足够的数据同步时间，数据同步通常有 1-2 分钟延迟。
2.  **业务空间：**如果当前处于某个子业务空间，则只能看到该空间内的数据。切换到**默认业务空间**可查看所有数据。

**调用大模型时出现超时，可能是什么原因？**

常见原因：

-   **输出内容过长：**模型生成内容过多导致整体耗时超过客户端等待上限。建议改用流式输出方式，以更快获得首个Token。
-   **网络问题：**检查客户端与阿里云服务之间的网络连接是否稳定。

**调用模型时Token消耗异常高，如何排查？**

当发现某模型（如 qwen3.6-plus）Token 消耗高于预期时，可通过以下 4 步进行排查：

1.  在百炼控制台左侧导航栏选择**用量&费用** > **模型用量**，进入用量统计页面查看各模型的 Token 消耗。该页面汇总展示**调用模型数**、**调用成功总次数**、**Token总量**。
2.  点击**大语言模型**页签，关注**输入Token总数(不包含缓存)**与**输出Tokens总量**两列。若某模型的输入 Token 总数远大于输出 Tokens 总量，说明 input 内容过长是消耗偏高的主因。
3.  查看缓存指标三列——**隐式缓存命中Token总量**、**显式缓存创建Token总数**、**显式缓存命中Token总数**。取值为“-”表示该模型未启用上下文缓存；有数值表示缓存已生效，可降低 input Token 消耗。
4.  点击目标模型行的**查看详情**，进入单模型详情页查看调用量趋势与平均单次请求 Token 量等细粒度数据。

Token 消耗异常的两类常见原因：input 内容过长、上下文缓存未启用。

**使用子账号开启监控数据投递，应如何配置权限？**

操作步骤：

1.  为子账号配置`AliyunBailianFullAccess`全局管理（阿里云百炼）权限。
    
2.  为子账号配置`模型监控-操作`（或`管理员`）页面权限，使其能在模型监控页面执行写入类操作。
    
3.  为子账号[配置AliyunCloudMonitorFullAccess系统策略](https://help.aliyun.com/zh/cms/cloudmonitor-1-0/user-guide/grant-permissions-to-a-ram-user)。
    
4.  创建并授予子账号**创建服务关联角色**系统策略。
    
    1.  登录[RAM控制台](https://ram.console.aliyun.com/)，在左侧导航栏，选择**权限管理权限策略**，然后点击页面上的**创建权限策略**。
    2.  点击**脚本编辑**，将以下内容粘贴至策略输入框后，点击**确定**。

```
{
    "Version": "1",
    "Statement": [
        {
            "Action": "ram:CreateServiceLinkedRole",
            "Resource": "*",
            "Effect": "Allow"
        }
    ]
}
```

3.  输入权限策略名称`CreateServiceLinkedRole`后，点击**确定**。
4.  在左侧导航栏，选择**身份管理用户**。从页面列表中找到待授权的子账号，然后点击子账号**操作**列的**添加权限**。
5.  从**权限策略**列表中，选择刚创建的权限策略（CreateServiceLinkedRole），然后点击**确认新增授权**。至此，子账号拥有了创建服务关联角色的权限。
6.  完成以上所有权限配置后，返回[模型监控（北京）](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)、[模型监控（弗吉尼亚）](https://modelstudio.console.aliyun.com/us-east-1?tab=dashboard#/model-telemetry)或[模型监控（新加坡）](https://modelstudio.console.aliyun.com/?tab=dashboard#/model-telemetry)页面，使用子账号重试开启**监控数据投递**。

**使用子账号开通推理日志，应如何配置权限？**

操作步骤：

1.  为子账号配置`AliyunBailianFullAccess`全局管理（阿里云百炼）权限。
    
2.  为子账号配置`模型监控-操作`（或`管理员`）页面权限，使其能在模型监控页面执行写入类操作。
    
3.  为子账号[配置AliyunLogFullAccess系统策略](https://help.aliyun.com/zh/cms/cloudmonitor-1-0/user-guide/grant-permissions-to-a-ram-user)。
    
4.  创建并授予子账号**创建服务关联角色**系统策略。
    
    1.  登录[RAM控制台](https://ram.console.aliyun.com/)，在左侧导航栏，选择**权限管理权限策略**，然后点击页面上的**创建权限策略**。
    2.  点击**脚本编辑**，将以下内容粘贴至策略输入框后，点击**确定**。

```
{
    "Version": "1",
    "Statement": [
        {
            "Action": "ram:CreateServiceLinkedRole",
            "Resource": "*",
            "Effect": "Allow"
        }
    ]
}
```

3.  输入权限策略名称`CreateServiceLinkedRole`后，点击**确定**。
4.  在左侧导航栏，选择**身份管理用户**。从页面列表中找到待授权的子账号，然后点击子账号**操作**列的**添加权限**。
5.  从**权限策略**列表中，选择刚创建的权限策略（CreateServiceLinkedRole），然后点击**确认新增授权**。至此，子账号拥有了创建服务关联角色的权限。
6.  完成以上所有权限配置后，返回[模型监控（北京）](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)页面，使用子账号重试开启**推理日志**。

**如何确保调用后的数据被删除？**

百炼平台在调用完成后不会即时物理删除数据，数据保留遵循服务协议的最短必要时间原则。推理日志默认关闭；开启后，调用数据写入日志服务SLS并保留**30天**，关闭后不再写入新数据。如需缩短保留时间，可在SLS控制台修改对应日志库的TTL。

## 附录

### 名词解释

**名词**

**解释**

**实时推理**

指对模型的所有直接和间接调用，主要涵盖以下场景：

-   通过DashScope SDK或OpenAI兼容接口的API调用
    
-   模型体验
    
-   阿里云百炼应用（智能体/工作流/智能体编排应用，以及涉及到模型调用的节点，如大模型节点、意图分类节点以及智能体群组节点等）的测试态和发布态
    
-   [Assistant API（下线中）](https://help.aliyun.com/zh/model-studio/assistant-api)调用
    
-   应用调用
    
-   Prompt反馈优化
    

**批量推理**

对于无需实时响应的场景，通过[OpenAI兼容-Batch（文件输入）](raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)接口以离线方式进行的大规模数据处理。
