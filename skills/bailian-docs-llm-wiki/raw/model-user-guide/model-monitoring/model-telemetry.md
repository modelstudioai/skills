# 模型监控

模型监控功能可用于：

-   查看调用记录
    
-   指标监控与告警，如Token延时、调用时长、RPM（每分钟调用次数）、TPM（每分钟消耗Token数）和失败率
    
-   统计Token消耗
    

## 支持的模型

-   **监控：普通监控**支持[模型列表](https://help.aliyun.com/zh/model-studio/models)中的所有模型，，包括基于它们调优后的[自定义模型](https://help.aliyun.com/zh/model-studio/model-deployment-introduction#f17bf700c06k5)；**高级监控**支持北京、新加坡、弗吉尼亚地域下的所有模型**。**
    
-   **告警功能：**支持北京、新加坡地域下的所有模型。
    
-   **日志功能：**目前支持的部分模型列表如下：
    
    ## 北京
    
    -   qwen3-max、qwen3-max-2025-09-23、qwen3-max-2026-01-23、qwen3-max-preview
        
    -   qwen-max、qwen-max-0919、qwen-max-2025-01-25、qwen-max-latest
        
    -   qwen-plus、qwen-plus-2025-04-28、qwen-plus-2025-07-14、qwen-plus-2025-07-28、qwen-plus-2025-09-11、qwen-plus-2025-12-01、qwen-plus-latest
        
    -   qwen-flash、qwen-flash-2025-07-28
        
    -   qwen-turbo、qwen-turbo-2025-07-15、qwen-turbo-2025-04-28、qwen-turbo-latest
        
    -   deepseek-v3.1、deepseek-v3.2、deepseek-v3.2-exp
        
    -   qwen3-235b-a22b、qwen3-235b-a22b-instruct-2507、qwen3-235b-a22b-thinking-2507、qwen3-30b-a3b、qwen3-30b-a3b-instruct-2507、qwen3-30b-a3b-thinking-2507、qwen3-next-80b-a3b-instruct、qwen3-next-80b-a3b-thinking
        
    -   qwen3-coder-480b-a35b-instruct、qwen3-coder-flash、qwen3-coder-flash-2025-07-28、qwen3-coder-plus、qwen3-coder-plus-2025-07-22、qwen3-coder-plus-2025-09-23
        
    
    ## 新加坡
    
    -   qwen3-max、qwen3-max-2025-09-23、qwen3-max-2026-01-23、qwen3-max-preview
        
    -   qwen-max、qwen-max-2025-01-25、qwen-max-latest
        
    -   qwen-plus、qwen-plus-2025-04-28、qwen-plus-2025-07-14、qwen-plus-2025-07-28、qwen-plus-2025-09-11、qwen-plus-2025-12-01、qwen-plus-latest
        
    -   qwen-flash、qwen-flash-2025-07-28
        
    -   qwen-turbo、qwen-turbo-2025-04-28、qwen-turbo-latest
        
    -   qwen3-235b-a22b、qwen3-235b-a22b-instruct-2507、qwen3-235b-a22b-thinking-2507、qwen3-30b-a3b、qwen3-30b-a3b-instruct-2507、qwen3-30b-a3b-thinking-2507、qwen3-next-80b-a3b-instruct、qwen3-next-80b-a3b-thinking
        
    -   qwen3-coder-480b-a35b-instruct、qwen3-coder-flash、qwen3-coder-flash-2025-07-28、qwen3-coder-plus、qwen3-coder-plus-2025-07-22、qwen3-coder-plus-2025-09-23
        
    

## **监控模型运行**

系统会自动采集主账号下所有业务空间内的模型调用数据。当有[直接或间接](#0806932be6woi)模型调用发生时，系统会自动收集并同步相关数据至目标业务空间的[模型监控](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)列表中。

> 列表记录按“模型 + 业务空间”维度生成。新模型在首次数据同步完成后自动加入列表（普通监控的延迟通常为小时级，请耐心等待；如需分钟级的数据洞察，请使用[高级监控](#2e5f2f0dffijg)）。

> 默认业务空间成员可查看所有业务空间的模型调用情况；子业务空间成员仅能查看当前空间的数据，无法切换查看其他业务空间数据。

在列表中找到目标模型后，点击其右侧**操作**列的**监控**，可查询以下**4**类监控指标：

-   **安全：**识别对话中的违规内容，例如`内容安全错误次数`。
    
-   **成本：**评估模型的成本效益，例如`平均单次请求调用量`。
    
-   **性能：**观察模型的性能变化，例如`调用时长`、`首Token延时`。
    
-   **错误：**判断模型的稳定性，例如`失败次数`、`失败率`。
    

您可基于上述指标创建[告警](#b8fcd646d5avf)，以便及时发现和处理异常。

**调用统计**

此页签可查看**安全、成本、错误**相关指标（如调用次数、失败次数等）。支持按[API-KEY](https://help.aliyun.com/zh/model-studio/apikey)、[推理类型](#f131611173sdx)，以及时间范围进行筛选。

-   **限流错误次数：**指因[429状态码](https://help.aliyun.com/zh/model-studio/error-code#5ed5532c85ckv)导致的调用失败。
    
-   **内容安全错误次数：**指输入或输出包含疑似敏感或高风险内容（例如涉黄、涉政和广告等）被[内容安全服务](https://www.aliyun.com/product/content-moderation/guardrail)拦截。
    

**性能指标**

此页签可查看RPM、TPM、调用时长以及首Token延时等**性能**相关指标。

## **查看 Token 消耗**

在实际使用中，调整模型的参数、系统提示词等操作均会改变模型的Token消耗。为统计和精细化管理成本，模型监控提供成本监控相关功能：

-   **汇总：**按业务空间维度汇总模型的历史Token消耗，并可按时间范围和API Key进一步筛选。
    
-   **追踪：**记录每一次模型调用的Token消耗。
    
-   **告警：**设置Token消耗阈值，当指定模型出现异常消耗时，系统立即告警。
    

#### **查看模型历史 Token 消耗**

-   查看最近**30**天的Token消耗：
    
    1.  当模型出现在目标业务空间的[模型监控](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)列表中后，点击其右侧**操作**列的**监控**。
        
    2.  在调用统计页签的**调用量**区域，可以查看Token消耗数据。
        
-   查看更早的用量：在[费用与成本](https://billing-cost.console.aliyun.com/finance/expense-report/expense-detail-by-instance?month=2025-02&statisticItem=DEFAULT_CHARGE_ITEM&commodityCode%5BfilterMode%5D=IN&commodityCode%5Bvalues%5D=sfm_deployment_public_cn%26sfm_inference_public_cn%26sfm_training_public_cn&statisticCycle=MONTHLY_SUMMARY)页面查询。
    

#### **查看某次调用的 Token 消耗**

> 该功能目前仅适用于**华北2（北京）**地域的[部分模型](#7f2491defbdpt)。

1.  使用主账号（[或拥有足够权限的子账号](#f9d06146c0xe0)）登录，在目标业务空间的[模型监控（北京）](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)页面，点击右上角的**模型监控配置**，按照指引依次开通审计日志和推理日志。
    
    > 开通后，系统即开始记录该业务空间内每一次模型调用的输入与输出。从调用发生到日志被记录存在分钟级延迟，请耐心等待。
    
2.  在模型监控列表中找到目标模型，点击其右侧**操作**列的**日志**。
    
3.  **日志**页签展示该模型的[实时推理](#f131611173sdx)调用记录，**用量**字段即为本次调用的Token消耗。
    

#### **创建异常消耗告警**

-   请参见[建立主动告警](#b8fcd646d5avf)。
    

## **查看历史对话（模型日志）**

**重要**

该功能目前仅适用于**华北2（北京）**地域的[部分模型](#7f2491defbdpt)。

模型监控支持查看模型的每一次对话，包括输入、输出及耗时，是故障排查和内容审计的关键工具。

#### **步骤一：开通日志**

使用主账号（[或拥有足够权限的子账号](#f9d06146c0xe0)）登录，在目标业务空间的[模型监控（北京）](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)页面，点击右上角的**模型监控配置**，按照指引依次开通审计日志和推理日志。

> 开通后，系统即开始记录该业务空间内每一次模型调用的输入与输出。从调用发生到日志被记录存在分钟级延迟，请耐心等待。

> 如需停止记录，只需在模型监控配置中关闭推理日志即可。

#### **步骤二：查看历史对话**

1.  在模型监控列表中找到目标模型，点击其右侧**操作**列的**日志**。
    
2.  **日志**页签展示该模型的[实时推理](#f131611173sdx)调用记录，**请求和响应**字段分别对应本次调用的输入与输出。
    

## **建立主动告警**

**重要**

该功能目前仅适用于新加坡和华北2（北京）地域。

模型的静默失败（如超时、Token消耗突增），传统应用日志难以发现。模型监控支持对监控指标（如成本、失败率、响应延迟）设置告警。一旦指标出现异常，系统立即告警。

#### **步骤一：开启高级监控**

1.  使用主账号（[或拥有足够权限的子账号](#54ea9ba526ovz)）登录，在目标业务空间的模型监控（[北京](https://bailian.console.aliyun.com/?tab=model#/model-telemetry) 或 [新加坡](https://modelstudio.console.aliyun.com/?tab=dashboard#/model-telemetry)）页面，点击右上角的**模型监控配置**。
    
2.  在高级监控区域，手动开启**性能和用量指标监控**。
    

#### **步骤二：创建告警规则**

1.  在模型告警（[北京](https://bailian.console.aliyun.com/?tab=model#/model-alert) 或[新加坡](https://modelstudio.console.aliyun.com/?tab=dashboard#/model-alert)）页面，点击右上角的**创建告警规则**。
    
2.  在对话框中，选择要监控的模型和监控模板，确认无误后点击**创建**。当指定的监控指标（如调用统计或性能指标）出现异常时，系统将通知您的团队。
    
    -   **通知方式：**支持短信、电子邮件、电话、钉钉群机器人、企业微信机器人及Webhook。
        
    -   **告警等级：**分为**普通**、**警告**、**错误**和**紧急**，不支持自定义新增或修改。各等级与通知渠道的对应关系如下：
        
        -   紧急（CRITICAL）: 电话、短信、邮件
            
        -   错误（ERROR）: 短信、邮件
            
        -   警告（WARNING）: 短信、邮件
            
        -   普通（INFO）: 邮件
            

## **接入 Grafana 与自建应用**

模型监控的监控指标数据存储在您的私有Prometheus实例中，并支持标准的Prometheus HTTP API，可用于接入 Grafana 或您的自建应用进行可视化分析。

#### **步骤一：获取数据源HTTP API地址**

1.  确保已[开启高级监控](#c6d515ccdeunl)。
    
2.  在[模型监控（北京）](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)、[模型监控（弗吉尼亚）](https://modelstudio.console.aliyun.com/us-east-1?tab=dashboard#/model-telemetry)或[模型监控（新加坡）](https://modelstudio.console.aliyun.com/?tab=dashboard#/model-telemetry)页面，点击右上角的**模型监控配置**。点击云监控Prometheus实例右侧的**查看详情**。
    
3.  在**设置**页面，根据您的客户端网络环境（公网或VPC访问），复制对应的 HTTP API 地址。
    
    ![1](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4023704671/p1028669.jpg)
    

#### **步骤二：接入 Grafana 或自建应用**

## 接入自建应用

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
        
        **展开查看监控指标**
        
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
        
        **用量**
        
        model\_usage
        
        模型用量总和
        
    -   **HTTP API：**`{HTTP API}`需替换为前面[步骤一](#title-tkb-ds1-4p5)获取的HTTP API地址。
        
    -   **Authorization：**需将阿里云账号的 `AccessKey:AccessKeySecret` 拼接后进行Base64编码，并以 `Basic 编码后字符串` 的形式提供。
        
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
    
    -   **query：**通过`{}` 包裹多个过滤条件，条件之间以英文逗号分隔，例如：`{workspace_id="值1",model="值2"}` 。**支持的过滤条件（LabelKey）**清单如下。
        
        **展开查看支持的过滤条件**
        
        **LabelKey**
        
        **描述**
        
        **user\_id**
        
        阿里云账号ID。
        
        > RAM用户为UID。[如何获取](https://help.aliyun.com/zh/ram/user-guide/view-the-basic-information-about-a-ram-user)
        
        **apikey\_id**
        
        API Key ID（非API Key），可在**密钥管理**（[北京](https://bailian.console.aliyun.com/?tab=model#/api-key) |[美国](https://modelstudio.console.aliyun.com/us-east-1?tab=dashboard#/api-key)| [新加坡](https://modelstudio.console.aliyun.com/?tab=playground#/api-key)）页面获取。
        
        ![56](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4023704671/p1028878.jpg)
        
        **说明**
        
        apikey\_id 值为 -1 表示调用源自阿里云百炼控制台，而非通过API。
        
        **workspace\_id**
        
        业务空间ID。[如何获取](https://help.aliyun.com/zh/model-studio/use-workspace#c5222ec081sbo)
        
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
            
            > 常见于图像生成模型。[文本生成图像](https://help.aliyun.com/zh/model-studio/text-to-image)
            
        
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
            
        
    

## 接入 Grafana

在 Grafana（自建或阿里云 Grafana 服务）中添加模型监控数据源。此处以Grafana 10.x（英文版）为例。其他版本的操作类似，详情请参考[Grafana官方文档](https://grafana.com/docs/grafana/latest/datasources/prometheus/configure/)。

1.  **添加数据源：**
    
    1.  使用管理员账号登录Grafana。点击页面左上角的![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5066520371/p864738.png)图标，选择**Administration** > **Data sources**。点击**\+ Add new data source**，数据源类型选择**Prometheus**。
        
    2.  在**Settings**页签配置数据源信息：
        
        -   **Name：**输入自定义的名称。
            
        -   **Prometheus server URL：**输入前面[步骤一](#title-tkb-ds1-4p5)获取的HTTP API地址。
            
        -   **Auth：**开启**Basic auth**，并设置**User**（阿里云账号的[AccessKey](https://help.aliyun.com/zh/sdk/developer-reference/configure-the-alibaba-cloud-accesskey-environment-variable-on-linux-macos-and-windows-systems)）及**Password**（阿里云账号的[AccessKey Secret](https://help.aliyun.com/zh/sdk/developer-reference/configure-the-alibaba-cloud-accesskey-environment-variable-on-linux-macos-and-windows-systems)）。
            
            > AccessKey及AccessKeySecret与前面步骤一的Prometheus实例必须归属同一阿里云账号。
            
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4023704671/p1028673.png)
        
    3.  点击页签底部的**Save & Test**。
        
2.  **指标查询：**
    
    1.  点击Grafana页面左上角的![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5461402171/p785190.png)图标，在左侧导航栏中点击**Dashboards**。
        
    2.  点击**Dashboards**页面右侧的**New** > **New dashboard**创建一个新的仪表盘。
        
    3.  点击**\+ Add visualization**，并选择您刚创建的数据源。
        
    4.  在**Edit Panel**页面点击**Query**页签，在**A**区域的**Label filters**字段中选择**\_name\_**及指标名称。以查询模型Token消耗`model_usage`为例：
        
        **示例**
        
        **说明**
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4023704671/p1028714.png)
        
        图中`_name_`对应的值（`model_usage`）可替换为下方**监控指标**列表中的任意指标名称。
        
        **展开查看监控指标**
        
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
        
        **用量**
        
        model\_usage
        
        模型用量总和
        
        增加以下Label filters进一步筛选：
        
        **展开查看支持的过滤条件**
        
        **LabelKey**
        
        **描述**
        
        **user\_id**
        
        阿里云账号ID。
        
        > RAM用户为UID。[如何获取](https://help.aliyun.com/zh/ram/user-guide/view-the-basic-information-about-a-ram-user)
        
        **apikey\_id**
        
        API Key ID（非API Key），可在**密钥管理**（[北京](https://bailian.console.aliyun.com/?tab=model#/api-key) |[美国](https://modelstudio.console.aliyun.com/us-east-1?tab=dashboard#/api-key)| [新加坡](https://modelstudio.console.aliyun.com/?tab=playground#/api-key)）页面获取。
        
        ![56](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4023704671/p1028878.jpg)
        
        **说明**
        
        apikey\_id 值为 -1 表示调用源自阿里云百炼控制台，而非通过API。
        
        **workspace\_id**
        
        业务空间ID。[如何获取](https://help.aliyun.com/zh/model-studio/use-workspace#c5222ec081sbo)
        
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
            
            > 常见于图像生成模型。[文本生成图像](https://help.aliyun.com/zh/model-studio/text-to-image)
            
        
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
        
        > 如果图表中成功渲染出数据，则说明配置成功。否则请检查：1）填写的HTTP API地址或AccessKey及AccessKeySecret是否正确；2）前面[步骤一](#title-tkb-ds1-4p5)的Prometheus实例中是否有监控数据。
        

## **监控模式对比**

模型监控提供两种监控模式：**普通监控**和**高级监控**。

> **普通监控****：**作为基础服务提供，随阿里云百炼的开通自动开启，不支持关闭。

> **高级监控****：**需主账号（[或拥有足够权限的子账号](#54ea9ba526ovz)）在目标业务空间的[模型监控（北京）](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)、[模型监控（弗吉尼亚）](https://modelstudio.console.aliyun.com/us-east-1?tab=dashboard#/model-telemetry)或[模型监控（新加坡）](https://modelstudio.console.aliyun.com/?tab=dashboard#/model-telemetry)界面手动开启，支持关闭。仅记录开启高级监控后的调用数据。

**对比项**

**普通监控****（默认）**

**高级监控****（需手动开启）**

**数据延时**

小时级

分钟级

**查看调用统计**

支持

支持

**查看失败调用（详情）**

不支持

支持

**查看性能指标**

支持

支持

**作用范围**

主账号下所有业务空间

仅在开启的业务空间内生效

**计费**

免费

收费

## **配额与限制**

-   **数据保留周期：**普通和高级监控的数据默认均保留**30天**。如需查询更早的用量信息，请通过[费用与成本](https://billing-cost.console.aliyun.com/finance/expense-report/expense-detail-by-instance?month=2025-02&statisticItem=DEFAULT_CHARGE_ITEM&commodityCode%5BfilterMode%5D=IN&commodityCode%5Bvalues%5D=sfm_deployment_public_cn%26sfm_inference_public_cn%26sfm_training_public_cn&statisticCycle=MONTHLY_SUMMARY)页面查询。
    
-   **告警模板限制：**每个业务空间最多可创建**100**个告警模板。
    
-   **API限制：**模型监控的监控指标数据请通过[Prometheus HTTP API](#1f0d765b83nwb)查询。
    
    -   **替代方案：**如需通过API获取单次调用Token消耗，可在每次调用模型时从响应中的`usage`字段提取当前调用数据。该字段结构示例如下（更多说明请参见[千问API参考](https://help.aliyun.com/zh/model-studio/qwen-api-reference/)）：
        
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
        

## **计费说明**

-   **普通监控：**免费。
    
-   **高级监控：**开启后，分钟级的监控数据将写入[云监控CMS](https://cloudmonitornext.console.aliyun.com/newOverview)服务并产生费用。具体计费方式参见[云监控CMS计费概述](https://help.aliyun.com/zh/cms/cloudmonitor-1-0/product-overview/billing-overview-1)。
    
-   **推理日志：**开启后，分钟级的日志数据将写入[日志服务SLS](https://sls.console.aliyun.com/)服务并产生费用。具体计费方式参见[日志服务SLS计费概述](https://help.aliyun.com/zh/sls/billing-overview)。
    

## **常见问题**

**为什么调用了模型，但在模型监控中查不到调用次数和消耗Token数？**

按以下步骤排查：

1.  **数据延迟：**确认是否已等待足够的数据同步时间。普通监控延迟为小时级，高级监控为分钟级。
    
2.  **业务空间：**如果当前处于某个子业务空间，则只能看到该空间内的数据。切换到**默认业务空间**可查看所有数据。
    

**调用大模型时出现超时，可能是什么原因？**

常见原因：

-   **输出内容过长：**模型生成内容过多导致整体耗时超过客户端等待上限。建议改用[流式输出](https://help.aliyun.com/zh/model-studio/stream)方式，以更快获得首个Token。
    
-   **网络问题：**检查客户端与阿里云服务之间的网络连接是否稳定。
    

**使用子账号开通高级监控，应如何配置权限？**

操作步骤：

1.  为子账号配置`AliyunBailianFullAccess`[全局管理（阿里云百炼）权限](https://help.aliyun.com/zh/model-studio/member-management#cd0f1152d50hj)。
    
2.  为子账号配置`模型监控-操作`（或`管理员`）[页面权限](https://help.aliyun.com/zh/model-studio/member-management#febd776ce5lbx)，使其能在模型监控页面执行写入类操作。
    
3.  为子账号[配置AliyunCloudMonitorFullAccess系统策略](https://help.aliyun.com/zh/cms/cloudmonitor-1-0/user-guide/grant-permissions-to-a-ram-user)。
    
4.  创建并授予子账号**创建服务关联角色**系统策略。
    
    1.  登录[RAM控制台](https://ram.console.aliyun.com/)，在左侧导航栏，选择**权限管理** > **权限策略**，然后点击页面上的**创建权限策略**。
        
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
        
    4.  在左侧导航栏，选择**身份管理** > **用户**。从页面列表中找到待授权的子账号，然后点击子账号**操作**列的**添加权限**。
        
    5.  从**权限策略**列表中，选择刚创建的权限策略（CreateServiceLinkedRole），然后点击**确认新增授权**。至此，子账号拥有了创建服务关联角色的权限。
        
5.  完成以上所有权限配置后，返回[模型监控（北京）](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)、[模型监控（弗吉尼亚）](https://modelstudio.console.aliyun.com/us-east-1?tab=dashboard#/model-telemetry)或[模型监控（新加坡）](https://modelstudio.console.aliyun.com/?tab=dashboard#/model-telemetry)页面，使用子账号重试开启**高级监控**。
    

**使用子账号开通推理日志，应如何配置权限？**

操作步骤：

1.  为子账号配置`AliyunBailianFullAccess`[全局管理（阿里云百炼）权限](https://help.aliyun.com/zh/model-studio/member-management#cd0f1152d50hj)。
    
2.  为子账号配置`模型监控-操作`（或`管理员`）[页面权限](https://help.aliyun.com/zh/model-studio/member-management#febd776ce5lbx)，使其能在模型监控页面执行写入类操作。
    
3.  为子账号[配置AliyunLogFullAccess系统策略](https://help.aliyun.com/zh/cms/cloudmonitor-1-0/user-guide/grant-permissions-to-a-ram-user)。
    
4.  创建并授予子账号**创建服务关联角色**系统策略。
    
    1.  登录[RAM控制台](https://ram.console.aliyun.com/)，在左侧导航栏，选择**权限管理** > **权限策略**，然后点击页面上的**创建权限策略**。
        
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
        
    4.  在左侧导航栏，选择**身份管理** > **用户**。从页面列表中找到待授权的子账号，然后点击子账号**操作**列的**添加权限**。
        
    5.  从**权限策略**列表中，选择刚创建的权限策略（CreateServiceLinkedRole），然后点击**确认新增授权**。至此，子账号拥有了创建服务关联角色的权限。
        
5.  完成以上所有权限配置后，返回[模型监控（北京）](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)页面，使用子账号重试开启**推理日志**。
    

## **附录**

#### **名词解释**

**名词**

**解释**

**实时推理**

指对模型的所有直接和间接调用，主要涵盖以下场景：

-   通过DashScope SDK或OpenAI兼容接口的API调用
    
-   模型体验
    
-   [阿里云百炼应用](https://help.aliyun.com/zh/model-studio/application-introduction)（智能体/工作流/智能体编排应用，以及涉及到模型调用的节点，如大模型节点、意图分类节点以及智能体群组节点等）的测试态和发布态
    
-   [Assistant API](https://help.aliyun.com/zh/model-studio/assistant-api/)调用
    
-   [应用调用](https://help.aliyun.com/zh/model-studio/application-calling-guide)
    
-   [Prompt反馈优化](https://help.aliyun.com/zh/model-studio/prompt-feedback-optimization)
    

**批量推理**

对于无需实时响应的场景，通过[OpenAI兼容-Batch（文件输入）](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)接口以离线方式进行的大规模数据处理。
