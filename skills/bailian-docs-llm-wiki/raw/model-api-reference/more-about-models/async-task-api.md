# 通过HTTP回调URL或MQ接收异步任务完成通知

在异步任务处理中，频繁轮询任务结果接口不仅会造成资源浪费，还可能因请求频率过高触发接口限流。阿里云百炼支持通过事件总线在任务完成处理后主动推送任务完成通知。您可以通过配置 HTTP 回调 URL 或 RocketMQ 消息队列来接收通知，在收到通知后，只需一次查询即可获取任务结果，从而避免频繁轮询。

<a id="背景介绍"></a>

<a id="f9e4c6c88c6ho"></a>

## 背景介绍

阿里云百炼的异步任务已接入[事件总线EventBridge](https://help.aliyun.com/zh/eventbridge/product-overview/what-is-eventbridge)。事件总线作为事件中转服务，负责将事件路由至配置的事件目标（即事件接收端）。本文中提到的“通知”，在事件总线体系中即为一个具体的“事件”。

当阿里云百炼完成异步任务处理后，无论任务成功还是失败，都会生成一个**“任务完成事件”**（包含任务状态、任务ID等信息），并将其上报到事件总线。事件总线会将该事件推送到您配置的事件目标。更多的事件目标及配置方式请参见[事件目标](https://help.aliyun.com/zh/eventbridge/user-guide/event-target-overview)、[目标服务类型](https://help.aliyun.com/zh/eventbridge/user-guide/target-service-types/)。

**主动轮询 VS 接收异步任务完成通知**

<table><thead><tr><th><strong>对比维度</strong></th><th><strong>主动轮询</strong></th><th><strong>接收异步任务完成通知</strong></th></tr></thead><tbody><tr><td><p>是否限流</p></td><td><p>查询结果接口限流（20QPS）</p></td><td><p>不限流</p></td></tr><tr><td><p>接入难度</p></td><td><p>简单，轮询查询结果接口即可</p><blockquote><p>部分任务（如<a href="../image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md#db17b3098c2iv">文生图</a>、<a href="../video-generation-api/wan-api-reference/text-to-video-api-reference.md#db17b3098c2iv">文生视频</a>）提供了SDK，SDK已实现轮询，可直接使用；若未提供SDK，需自行实现</p></blockquote></td><td><p>稍复杂</p><p>需要在事件总线中配置HTTP回调URL或RocketMQ，还需解析事件总线推送的通知</p></td></tr><tr><td><p>服务器资源消耗</p></td><td><p>轮询会占用您的业务系统资源，尤其是高频查询</p></td><td><p>不占用您的业务系统资源，由事件总线主动推送</p></td></tr><tr><td><p>实时性</p></td><td><p>实时性较低，依赖轮询频率</p></td><td><p>实时性高，任务完成后立即推送</p></td></tr><tr><td><p>选型建议</p></td><td><p>适合低并发、小规模任务，或对实时性要求不高的场景</p></td><td><p>适合高并发、大规模任务，或对实时性要求较高的场景</p></td></tr></tbody></table>

为接收异步任务完成通知，您可以通过事件总线配置事件目标，常见的配置方案包括：

-   [配置HTTP回调URL](async-task-api.md#d3591b073966f)：需要一个支持公网或[阿里云专有网络VPC](https://help.aliyun.com/zh/vpc/what-is-vpc)访问的 HTTP URL，且支持 POST 请求，适合大多数通用场景。
-   [配置RocketMQ](async-task-api.md#e2f044afc2c0w)：通过[云消息队列 RocketMQ](https://help.aliyun.com/zh/apsaramq-for-rocketmq/product-overview/what-is-apsaramq-for-rocketmq) 接收事件并进行消费，适用于对消息可靠性要求较高的场景。

<a id="方案一-配置http回调url"></a>

<a id="d3591b073966f"></a>

## 方案一：配置HTTP回调URL

<a id="方案介绍"></a>

<a id="596c553a1e9dk"></a>

### 方案介绍

阿里云百炼在任务完成后上报至事件总线，事件总线将任务完成事件推送到回调接口。回调接口接收到事件并进行解析，解析出已成功处理的任务 ID，随后只需调用一次查询结果接口即可获取任务结果。

**方案特点**：与直接轮询相比，该方案有效避免了无效轮询请求，减少资源消耗并降低查询结果接口的限流压力。

**计费说明**：[事件总线计费](https://help.aliyun.com/zh/eventbridge/product-overview/billing-overview)。

<table><tbody><tr><td><p>以<a href="../image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md">文生图</a>为例，基于HTTP回调URL的异步调用流程为：</p><ul><li><p>创建文生图任务，返回task_id，此时任务未完成。</p></li><li><p>阿里云百炼完成任务处理后，将任务完成事件上报至事件总线。</p></li><li><p>事件总线将该事件主动推送给HTTP回调接口。</p></li><li><p>回调接口解析该事件，获取已成功处理的<code>task_id</code>。</p></li><li><p>最后调用查询结果接口获取生成的图像URL。</p></li></ul></td><td><p><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9610776471/p950666.png" alt="image"></p></td></tr></tbody></table>

<a id="操作步骤"></a>

<a id="198cd2e3f8fzg"></a>

### 操作步骤

<a id="accordion-步骤1-准备http回调接口"></a>

步骤1：准备HTTP回调接口

通常情况下，HTTP 回调接口部署在您的业务系统中，用于接收异步事件通知。其配置需满足以下要求：

-   请求URL：支持公网或[阿里云专有网络VPC](https://help.aliyun.com/zh/vpc/what-is-vpc) 访问的 HTTP URL。
-   请求方式：`POST`。
-   请求Body：`JSON` 格式，内容为异步任务完成事件数据。具体事件结构可在事件总线控制台查询，示例如下：

<a id="accordion-点击查看异步任务完成事件的数据结构"></a>

点击查看异步任务完成事件的数据结构

<a id="code-block"></a>

```json
{
    "datacontenttype": "application/json;charset=utf-8",
    "aliyunaccountid": "xxxxx",
    "aliyunpublishtime": "2023-10-25T01:45:16.993Z",
    "data": {
        "start_time": "2023-10-25 09:45:09",
        "user_api_unique_key": "apikey:v1:audio:asr:transcription:paraformer-8k-v2",
        "task_status": "SUCCEEDED",
        "contain_result": false,
        "end_time": "2023-10-25 09:45:16",
        "task_id": "a154c328-xxxx-xxxx-xxxx-e52a9a7e9a35",
        "region": "cn-beijing",
        "request_id": "108f38f5-xxxx-xxxx-xxxx-6504db9080b3",
        "api_key_id": "1250"
    },
    "aliyunoriginalaccountid": "xxxxxxxx",
    "specversion": "1.0",
    "aliyuneventbusname": "default",
    "id": "81765e5b-xxxx-xxxx-xxxx-bbad8dde2bd9",
    "source": "acs.dashscope",
    "time": "2023-1-25T01:45:16.969Z",
    "aliyunregionid": "cn-beijing",
    "type": "dashscope:System:AsyncTaskFinish"
}
```

<a id="accordion-步骤2-在事件总线控制台查询事件"></a>

步骤2：在事件总线控制台查询事件

事件总线控制台支持查询阿里云百炼投递的事件。

1.  登录阿里云主账号，进入[事件总线控制台](https://eventbridge.console.aliyun.com/cn-beijing/event-buses)，切换到****华北2（北京）地域****，在左侧导航栏选择**事件总线**，点击**default**进入云服务专用总线。
    
    > 阿里云百炼所属的事件总线默认为default。
    
2.  点击**事件追踪**，输入查询条件，查询阿里云百炼的异步任务完成事件。
    
    -   事件源：搜索选择`acs.dashscope`，表示事件来源于 DashScope（即灵积模型服务，属于阿里云百炼的底层服务）。
    -   事件类型：搜索选择`dashscope:System:AsyncTaskFinish`，表示异步任务完成事件。
3.  点击**详情**，查看阿里云百炼上报的异步任务完成事件的详细信息。
    

<a id="code-block-2"></a>

```json
{
    "datacontenttype": "application/json;charset=utf-8",
    "aliyunaccountid": "xxxxx",
    "aliyunpublishtime": "2023-10-25T01:45:16.993Z",
    "data": {
        "start_time": "2023-10-25 09:45:09",
        "user_api_unique_key": "apikey:v1:audio:asr:transcription:paraformer-8k-v2",
        "task_status": "SUCCEEDED",
        "contain_result": false,
        "end_time": "2023-10-25 09:45:16",
        "task_id": "a154c328-xxxx-xxxx-xxxx-e52a9a7e9a35",
        "region": "cn-beijing",
        "request_id": "108f38f5-xxxx-xxxx-xxxx-6504db9080b3",
        "api_key_id": "1250"
    },
    "aliyunoriginalaccountid": "xxxxxxxx",
    "specversion": "1.0",
    "aliyuneventbusname": "default",
    "id": "81765e5b-xxxx-xxxx-xxxx-bbad8dde2bd9",
    "source": "acs.dashscope",
    "time": "2023-1-25T01:45:16.969Z",
    "aliyunregionid": "cn-beijing",
    "type": "dashscope:System:AsyncTaskFinish"
}
```

<a id="accordion-点击查看事件的参数描述"></a>

点击查看事件的参数描述

<table><thead><tr><th><p><strong>参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td><p>datacontenttype</p></td><td><p>String</p></td><td><p>参数data的内容形式。datacontenttype只支持<code>application/json</code>格式。</p></td><td><p><code>application/json;charset=utf-8</code></p></td></tr><tr><td><p>aliyunaccountid</p></td><td><p>String</p></td><td><p>阿里云账号ID。</p></td><td><p>123456789098****</p></td></tr><tr><td><p>aliyunpublishtime</p></td><td><p>String</p></td><td><p>接收事件的时间。</p></td><td><p>2020-11-19T21:04:42.179PRC</p></td></tr><tr><td><p>data</p></td><td><p>Object</p></td><td><p>事件内容。JSON对象，内容由发起事件的服务决定。CloudEvents可能包含事件发生时由事件生产者给定的上下文，data中封装了这些信息。</p></td><td></td></tr><tr><td><p>data[].start_time</p></td><td><p>String</p></td><td><p>异步任务开始时间，</p><p>格式：yyyy-MM-dd HH:mm:ss</p></td><td><p>2023-10-25 09:45:09</p></td></tr><tr><td><p>data[].end_time</p></td><td><p>String</p></td><td><p>异步任务完成时间</p><p>格式：yyyy-MM-dd HH:mm:ss</p></td><td><p>2023-10-25 09:45:16</p></td></tr><tr><td><p>data[].user_api_unique_key</p></td><td><p>String</p></td><td><p>API 的唯一key（提交任务时，模型API的五要素），组成格式为：</p><p><code>apikey:version:group:task:function-call:model</code></p><ul><li><p>version：版本</p></li><li><p>group：分组</p></li><li><p>task：任务名称</p></li><li><p>function-call：方法名称</p></li><li><p>model：模型名称</p></li></ul></td><td><p><code>apikey:v1:audio:asr:transcription:paraformer-8k-v2</code></p></td></tr><tr><td><p>data[].task_status</p></td><td><p>String</p></td><td><p>任务状态</p><ul><li><p>PENDING：任务排队中</p></li><li><p>RUNNING：任务处理中</p></li><li><p>SUCCEEDED：处理成功</p></li><li><p>FAILED：处理失败</p></li><li><p>CANCELED：任务取消</p></li><li><p>UNKNOWN：任务不存在或状态未知</p></li></ul></td><td><p>SUCCEEDED</p></td></tr><tr><td><p>data[].task_id</p></td><td><p>String</p></td><td><p>任务ID</p></td><td><p>a154c328-xxxx-xxxx-xxxx-e52a9a7e9a35</p></td></tr><tr><td><p>data[].region</p></td><td><p>String</p></td><td><p>任务所在地域</p></td><td><p>cn-beijing</p></td></tr><tr><td><p>data[].request_id</p></td><td><p>String</p></td><td><p>请求ID</p></td><td><p>108f38f5-xxxx-xxxx-xxxx-6504db9080b3</p></td></tr><tr><td><p>data[].api_key_id</p></td><td><p>String</p></td><td><p>API Key ID</p></td><td><p>1234</p></td></tr><tr><td><p>data[].contain_result</p></td><td><p>Boolean</p></td><td><p>是否包含结果详情。</p><ul><li><p>true：包含</p></li><li><p>false：不包含</p></li></ul></td><td><p>true</p></td></tr><tr><td><p>data[].output_result</p></td><td><p>JSON</p></td><td><p>结果详情。当<code>contain_result</code>为<code>true</code>时返回。</p></td><td><p><code>{&quot;request_id&quot;: &quot;6abe5b9b-f95c-9a23-8bed-0a04c2158b5c&quot;, &quot;output&quot;: {&quot;task_id&quot;: &quot;84d0e919-5eda-40a1-a6e9-a94033840693&quot;, &quot;task_status&quot;: &quot;SUCCEEDED&quot;, &quot;submit_time&quot;: &quot;2026-05-20 15:38:19.940&quot;, &quot;scheduled_time&quot;: &quot;2026-05-20 15:38:19.995&quot;, &quot;end_time&quot;: &quot;2026-05-20 15:38:25.186&quot;, &quot;text&quot;: &quot;这是一个模拟的文本生成结果。&quot;}, &quot;usage&quot;: {&quot;output_tokens&quot;: 100, &quot;input_tokens&quot;: 21}}</code></p></td></tr><tr><td><p>aliyunoriginalaccountid</p></td><td><p>String</p></td><td><p>阿里云原始账号ID</p></td><td><p>123456789098****</p></td></tr><tr><td><p>specversion</p></td><td><p>String</p></td><td><p>CloudEvents协议版本</p></td><td><p>1.0</p></td></tr><tr><td><p>aliyuneventbusname</p></td><td><p>String</p></td><td><p>接收事件的事件总线名称</p></td><td><p>default</p></td></tr><tr><td><p>id</p></td><td><p>String</p></td><td><p>事件ID，标识事件的唯一值。</p></td><td><p>45ef4dewdwe1-7c35-447a-bd93-fab****</p></td></tr><tr><td><p>source</p></td><td><p>String</p></td><td><p>事件源。</p><p>提供事件的服务，标识事件发生的内容。通常包含事件源的类型，发布事件的机制或生产事件的过程。发送端必须确保每个事件的<code>source+id</code>是唯一的。</p></td><td><p>acs.dashscope</p></td></tr><tr><td><p>time</p></td><td><p>String</p></td><td><p>事件产生的时间。</p><p>如果无法确定事件发生的时间，CloudEvents生产者可以把time设置为其他时间（例如当前时间），但是同一个source的所有生产者设置的值必须是一致的。</p></td><td><p>2020-11-19T21:04:41+08:00</p></td></tr><tr><td><p>aliyunregionid</p></td><td><p>String</p></td><td><p>接收事件的地域。</p></td><td><p>cn-beijing</p></td></tr><tr><td><p>type</p></td><td><p>String</p></td><td><p>事件类型。</p><p>描述事件源相关的事件类型。该参数用于路由、事件查询和策略执行等。格式由生产者定义且包含版本等信息。</p></td><td><p>dashscope:System:AsyncTaskFinish</p></td></tr></tbody></table>

<a id="accordion-步骤3-配置事件转发规则"></a>

步骤3：配置事件转发规则

1.  在左侧导航栏选择**事件规则**，单击**创建规则**。
    
2.  **配置基本信息**，自定义规则名称和描述。
    
3.  **配置事件模式**：指定需要转发的事件。
    
    -   **事件源**：搜索选择`acs.dashscope`，表示事件来源于阿里云百炼。
        
    -   **事件类型**：搜索选择`dashscope:System:AsyncTaskFinish`，表示异步任务完成事件。
        
    -   **模式内容**：用来配置过滤条件，可通过指定字段过滤事件。指定字段来源于步骤2中查询到的事件详情字段。模式编写规则请参见[事件模式](https://help.aliyun.com/zh/eventbridge/user-guide/event-patterns)，示例如下：
        
        -   默认情况：在选择事件源和事件类型后，模式内容默认展示如下内容，表示转发所有的`dashscope:System:AsyncTaskFinish`事件。

<a id="code-block-3"></a>

```json
{
  "source": ["acs.dashscope"],
  "type": ["dashscope:System:AsyncTaskFinish"]
}
```

-   通过指定字段过滤事件：筛选出 `user_api_unique_key`字段后缀为`:paraformer-8k-v2`的事件，即仅转发模型名称为`paraformer-8k-v2`的事件。事件类型为`dashscope:System:AsyncTaskFinish`。

<a id="code-block-4"></a>

```json
{
  "source": ["acs.dashscope"],
  "type": ["dashscope:System:AsyncTaskFinish"],
  "data": {
    "user_api_unique_key": [
      {"suffix": ":paraformer-8k-v2"}
    ]
  }
}
```

4.  **配置事件目标**：支持配置多种类型的[事件目标](https://help.aliyun.com/zh/eventbridge/user-guide/event-target-overview)，包括HTTP回调URL、RocketMQ消息队列等。具体操作见步骤4。

<a id="accordion-步骤4-配置事件目标为http回调接口"></a>

步骤4：配置事件目标为HTTP回调接口

1.  **配置事件目标**：将事件转发到HTTP回调URL。
    
    -   服务类型：选择“HTTP”。
        
    -   URL：填写HTTP服务地址。
        
    -   Body：选择“完整事件”。
        
    -   网络类型：根据服务地址选择。
        
        -   HTTP支持公网和专用网络两种类型，当选择专用网络时，需要配置VPC、vSwitch和SecurityGroup。
2.  点击**确认**即可完成规则的修改。查看事件目标，如果有HTTP样式，则代表配置成功。
    
    此时规则的**事件目标**列将显示**HTTP (1)**。
    

<a id="方案二-配置rocketmq"></a>

<a id="e2f044afc2c0w"></a>

## 方案二：配置RocketMQ

<a id="方案介绍-2"></a>

<a id="2e55ac6eabnac"></a>

### 方案介绍

阿里云百炼在任务完成后上报至事件总线，事件总线将任务完成事件推送到云消息队列RocketMQ。业务方监听消息队列并消费消息，解析出已成功处理的任务 ID，随后只需调用一次查询结果接口即可获取任务结果。

**方案特点**：与HTTP回调接口方案不同的是，RocketMQ 能够保证消息无丢失并支持失败重试，适合对消息可靠性要求较高的场景。

**计费说明**：[事件总线计费](https://help.aliyun.com/zh/eventbridge/product-overview/billing-overview)、[RocketMQ计费](https://help.aliyun.com/zh/apsaramq-for-rocketmq/cloud-message-queue-rocketmq-5-x-series/product-overview/overview-2)。

<table><tbody><tr><td><p>以<a href="../image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md">文生图</a>为例，基于RocketMQ的异步调用流程为：</p><ul><li><p>创建文生图任务，返回task_id，此时任务未完成。</p></li><li><p>阿里云百炼完成任务处理后，将任务完成事件上报至事件总线。</p></li><li><p>事件总线将该事件主动转发到指定的RocketMQ队列。</p></li><li><p>业务方监听RocketMQ队列，并消费消息，从中获取已成功处理<code>task_id</code>。</p></li><li><p>最后调用查询结果接口获取生成的图像URL。</p></li></ul></td><td><p><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9610776471/p950716.png" alt="image"></p></td></tr></tbody></table>

<a id="操作步骤-2"></a>

<a id="c16486a497b3q"></a>

### 操作步骤

<a id="accordion-步骤1-准备rocketmq实例-若已有-rocketmq队列-可跳过此步"></a>

步骤1：准备RocketMQ实例（若已有 RocketMQ队列，可跳过此步 ）

通过RocketMQ消息队列接收事件，需要先准备好RocketMQ队列，再接收消息。

1.  进入[RocketMQ控制台](https://ons.console.aliyun.com/overview)，在左侧导航栏选择**实例列表**，单击**创建实例**。
    
    实例ID：示例为`rmq-cn-nwy*******`。
    
2.  创建对应实例的`Topic`，设置自定义的Topic名称。
    
3.  创建对应实例的`Group`，设置自定义的Group名称。
    

<a id="accordion-步骤2-在事件总线控制台查询事件-2"></a>

步骤2：在事件总线控制台查询事件

事件总线控制台支持查询阿里云百炼投递的事件。

1.  登录阿里云主账号，进入[事件总线控制台](https://eventbridge.console.aliyun.com/cn-beijing/event-buses)，切换到****华北2（北京）地域****，在左侧导航栏选择**事件总线**，点击**default**进入云服务专用总线。
    
    > 阿里云百炼所属的事件总线默认为default。
    
2.  点击**事件追踪**，输入查询条件，查询阿里云百炼的异步任务完成事件。
    
    -   事件源：搜索选择`acs.dashscope`，表示事件来源于 DashScope（即灵积模型服务，属于阿里云百炼的底层服务）。
    -   事件类型：搜索选择`dashscope:System:AsyncTaskFinish`，表示异步任务完成事件。
3.  点击**详情**，查看阿里云百炼上报的异步任务完成事件的详细信息。
    

<a id="code-block-5"></a>

```json
{
    "datacontenttype": "application/json;charset=utf-8",
    "aliyunaccountid": "xxxxx",
    "aliyunpublishtime": "2023-10-25T01:45:16.993Z",
    "data": {
        "start_time": "2023-10-25 09:45:09",
        "user_api_unique_key": "apikey:v1:audio:asr:transcription:paraformer-8k-v2",
        "task_status": "SUCCEEDED",
        "contain_result": false,
        "end_time": "2023-10-25 09:45:16",
        "task_id": "a154c328-xxxx-xxxx-xxxx-e52a9a7e9a35",
        "region": "cn-beijing",
        "request_id": "108f38f5-xxxx-xxxx-xxxx-6504db9080b3",
        "api_key_id": "1250"
    },
    "aliyunoriginalaccountid": "xxxxxxxx",
    "specversion": "1.0",
    "aliyuneventbusname": "default",
    "id": "81765e5b-xxxx-xxxx-xxxx-bbad8dde2bd9",
    "source": "acs.dashscope",
    "time": "2023-1-25T01:45:16.969Z",
    "aliyunregionid": "cn-beijing",
    "type": "dashscope:System:AsyncTaskFinish"
}
```

<a id="accordion-点击查看事件的参数描述-2"></a>

点击查看事件的参数描述

<table><thead><tr><th><p><strong>参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td><p>datacontenttype</p></td><td><p>String</p></td><td><p>参数data的内容形式。datacontenttype只支持<code>application/json</code>格式。</p></td><td><p><code>application/json;charset=utf-8</code></p></td></tr><tr><td><p>aliyunaccountid</p></td><td><p>String</p></td><td><p>阿里云账号ID。</p></td><td><p>123456789098****</p></td></tr><tr><td><p>aliyunpublishtime</p></td><td><p>String</p></td><td><p>接收事件的时间。</p></td><td><p>2020-11-19T21:04:42.179PRC</p></td></tr><tr><td><p>data</p></td><td><p>Object</p></td><td><p>事件内容。JSON对象，内容由发起事件的服务决定。CloudEvents可能包含事件发生时由事件生产者给定的上下文，data中封装了这些信息。</p></td><td></td></tr><tr><td><p>data[].start_time</p></td><td><p>String</p></td><td><p>异步任务开始时间，</p><p>格式：yyyy-MM-dd HH:mm:ss</p></td><td><p>2023-10-25 09:45:09</p></td></tr><tr><td><p>data[].end_time</p></td><td><p>String</p></td><td><p>异步任务完成时间</p><p>格式：yyyy-MM-dd HH:mm:ss</p></td><td><p>2023-10-25 09:45:16</p></td></tr><tr><td><p>data[].user_api_unique_key</p></td><td><p>String</p></td><td><p>API 的唯一key（提交任务时，模型API的五要素），组成格式为：</p><p><code>apikey:version:group:task:function-call:model</code></p><ul><li><p>version：版本</p></li><li><p>group：分组</p></li><li><p>task：任务名称</p></li><li><p>function-call：方法名称</p></li><li><p>model：模型名称</p></li></ul></td><td><p><code>apikey:v1:audio:asr:transcription:paraformer-8k-v2</code></p></td></tr><tr><td><p>data[].task_status</p></td><td><p>String</p></td><td><p>任务状态</p><ul><li><p>PENDING：任务排队中</p></li><li><p>RUNNING：任务处理中</p></li><li><p>SUCCEEDED：处理成功</p></li><li><p>FAILED：处理失败</p></li><li><p>CANCELED：任务取消</p></li><li><p>UNKNOWN：任务不存在或状态未知</p></li></ul></td><td><p>SUCCEEDED</p></td></tr><tr><td><p>data[].task_id</p></td><td><p>String</p></td><td><p>任务ID</p></td><td><p>a154c328-xxxx-xxxx-xxxx-e52a9a7e9a35</p></td></tr><tr><td><p>data[].region</p></td><td><p>String</p></td><td><p>任务所在地域</p></td><td><p>cn-beijing</p></td></tr><tr><td><p>data[].request_id</p></td><td><p>String</p></td><td><p>请求ID</p></td><td><p>108f38f5-xxxx-xxxx-xxxx-6504db9080b3</p></td></tr><tr><td><p>data[].api_key_id</p></td><td><p>String</p></td><td><p>API Key ID</p></td><td><p>1234</p></td></tr><tr><td><p>data[].contain_result</p></td><td><p>Boolean</p></td><td><p>是否包含结果详情。</p><ul><li><p>true：包含</p></li><li><p>false：不包含</p></li></ul></td><td><p>true</p></td></tr><tr><td><p>data[].output_result</p></td><td><p>JSON</p></td><td><p>结果详情。当<code>contain_result</code>为<code>true</code>时返回。</p></td><td><p><code>{&quot;request_id&quot;: &quot;6abe5b9b-f95c-9a23-8bed-0a04c2158b5c&quot;, &quot;output&quot;: {&quot;task_id&quot;: &quot;84d0e919-5eda-40a1-a6e9-a94033840693&quot;, &quot;task_status&quot;: &quot;SUCCEEDED&quot;, &quot;submit_time&quot;: &quot;2026-05-20 15:38:19.940&quot;, &quot;scheduled_time&quot;: &quot;2026-05-20 15:38:19.995&quot;, &quot;end_time&quot;: &quot;2026-05-20 15:38:25.186&quot;, &quot;text&quot;: &quot;这是一个模拟的文本生成结果。&quot;}, &quot;usage&quot;: {&quot;output_tokens&quot;: 100, &quot;input_tokens&quot;: 21}}</code></p></td></tr><tr><td><p>aliyunoriginalaccountid</p></td><td><p>String</p></td><td><p>阿里云原始账号ID</p></td><td><p>123456789098****</p></td></tr><tr><td><p>specversion</p></td><td><p>String</p></td><td><p>CloudEvents协议版本</p></td><td><p>1.0</p></td></tr><tr><td><p>aliyuneventbusname</p></td><td><p>String</p></td><td><p>接收事件的事件总线名称</p></td><td><p>default</p></td></tr><tr><td><p>id</p></td><td><p>String</p></td><td><p>事件ID，标识事件的唯一值。</p></td><td><p>45ef4dewdwe1-7c35-447a-bd93-fab****</p></td></tr><tr><td><p>source</p></td><td><p>String</p></td><td><p>事件源。</p><p>提供事件的服务，标识事件发生的内容。通常包含事件源的类型，发布事件的机制或生产事件的过程。发送端必须确保每个事件的<code>source+id</code>是唯一的。</p></td><td><p>acs.dashscope</p></td></tr><tr><td><p>time</p></td><td><p>String</p></td><td><p>事件产生的时间。</p><p>如果无法确定事件发生的时间，CloudEvents生产者可以把time设置为其他时间（例如当前时间），但是同一个source的所有生产者设置的值必须是一致的。</p></td><td><p>2020-11-19T21:04:41+08:00</p></td></tr><tr><td><p>aliyunregionid</p></td><td><p>String</p></td><td><p>接收事件的地域。</p></td><td><p>cn-beijing</p></td></tr><tr><td><p>type</p></td><td><p>String</p></td><td><p>事件类型。</p><p>描述事件源相关的事件类型。该参数用于路由、事件查询和策略执行等。格式由生产者定义且包含版本等信息。</p></td><td><p>dashscope:System:AsyncTaskFinish</p></td></tr></tbody></table>

<a id="accordion-步骤3-配置事件转发规则-2"></a>

步骤3：配置事件转发规则

1.  在左侧导航栏选择**事件规则**，单击**创建规则**。
    
2.  **配置基本信息**，自定义规则名称和描述。
    
3.  **配置事件模式**：指定需要转发的事件。
    
    -   **事件源**：搜索选择`acs.dashscope`，表示事件来源于阿里云百炼。
        
    -   **事件类型**：搜索选择`dashscope:System:AsyncTaskFinish`，表示异步任务完成事件。
        
    -   **模式内容**：用来配置过滤条件，可通过指定字段过滤事件。指定字段来源于步骤2中查询到的事件详情字段。模式编写规则请参见[事件模式](https://help.aliyun.com/zh/eventbridge/user-guide/event-patterns)，示例如下：
        
        -   默认情况：在选择事件源和事件类型后，模式内容默认展示如下内容，表示转发所有的`dashscope:System:AsyncTaskFinish`事件。

<a id="code-block-6"></a>

```json
{
  "source": ["acs.dashscope"],
  "type": ["dashscope:System:AsyncTaskFinish"]
}
```

-   通过指定字段过滤事件：筛选出 `user_api_unique_key`字段后缀为`:paraformer-8k-v2`的事件，即仅转发模型名称为`paraformer-8k-v2`的事件。事件类型为`dashscope:System:AsyncTaskFinish`。

<a id="code-block-7"></a>

```json
{
  "source": ["acs.dashscope"],
  "type": ["dashscope:System:AsyncTaskFinish"],
  "data": {
    "user_api_unique_key": [
      {"suffix": ":paraformer-8k-v2"}
    ]
  }
}
```

4.  **配置事件目标**：支持配置多种类型的[事件目标](https://help.aliyun.com/zh/eventbridge/user-guide/event-target-overview)，包括HTTP回调URL、RocketMQ消息队列等。具体操作见步骤4。

<a id="accordion-步骤4-配置事件目标为rocketmq"></a>

步骤4：配置事件目标为RocketMQ

RocketMQ创建完成后，打开配置的事件目标界面，选择已配置的RocketMQ实例。

-   服务类型：选择“消息队列RocketMQ版”。
-   版本：已创建的RocketMQ版本，如RocketMQ 5.x
-   实例ID：已创建的RocketMQ的实例ID。请参见[步骤1](async-task-api.md)的配置。
-   Topic：已创建的Topic名称。请参见[步骤1](async-task-api.md)的配置。

<a id="accordion-步骤5-在rocketmq控制台查看消息"></a>

步骤5：在RocketMQ控制台查看消息

配置完成后，提交异步任务，待任务完成后，在配置的RocketMQ的Topic中查看消息。

-   RocketMQ在线查看消息需要开通消息一键收发体验功能。
-   消息一键收发体验功能是基于[函数计算](https://help.aliyun.com/zh/functioncompute/what-is-function-compute)实现的，如果超过了免费试用额度后将会产生少量费用，请查看[函数计算计费规则](https://help.aliyun.com/zh/functioncompute/what-is-function-compute)。

在**Topic 管理**页面找到已创建的Topic，单击其右侧**操作**列中的**详情**。

进入Topic详情后，切换到**消息一键收发体验**页签，在**基础功能**区域选择消费方式，如**PushConsumer 方式消费**。

配置好**Topic 名称**和**Group ID**等参数后，单击**运行**开始接收消息。**运行结果**页签将显示收到的消息列表，包括消息ID和接收时间等信息。

<a id="accordion-步骤6-使用sdk接收并消费消息"></a>

步骤6：使用SDK接收并消费消息

使用RocketMQ的[Java SDK](https://help.aliyun.com/zh/apsaramq-for-rocketmq/cloud-message-queue-rocketmq-5-x-series/developer-reference/overview-8)实现以下逻辑：先订阅相关Topic，实现消息监听逻辑。在接收到消息后，再进行消费处理。

下面展示RocketMQ 5.0版本的Java客户端示例代码。

-   在Maven项目中，引入以下依赖

<a id="code-block-8"></a>

```xml
<dependency>
  <groupId>org.apache.rocketmq</groupId>
  <artifactId>rocketmq-client-java</artifactId>
  <version>5.0.4</version>
</dependency>
```

-   消费MQ消息的示例代码

<a id="code-block-9"></a>

```java
import com.alibaba.fastjson2.JSON;
import org.apache.rocketmq.client.apis.*;
import org.apache.rocketmq.client.apis.consumer.ConsumeResult;
import org.apache.rocketmq.client.apis.consumer.FilterExpression;
import org.apache.rocketmq.client.apis.consumer.FilterExpressionType;
import org.apache.rocketmq.client.apis.consumer.PushConsumer;
import org.apache.rocketmq.shaded.org.slf4j.Logger;
import org.apache.rocketmq.shaded.org.slf4j.LoggerFactory;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.util.Collections;

public class ConsumerExample {
    private static final Logger LOGGER = LoggerFactory.getLogger(ConsumerExample.class);

    private ConsumerExample() {
    }

    public static void main(String[] args) throws ClientException, IOException, InterruptedException {
        /*
          实例接入点，从控制台实例详情页的接入点页签中获取。
          如果是在阿里云ECS内网访问，建议填写VPC接入点。
          如果是在本地公网访问，或者是线下IDC环境访问，可以使用公网接入点。使用公网接入点访问，必须开启实例的公网访问功能。
         */
        String endpoints = "xxxx";
        //指定需要订阅哪个目标Topic，Topic需要提前在控制台创建，如果不创建直接使用会返回报错。
        String topic = "xxxx";
        //为消费者指定所属的消费者分组，Group需要提前在控制台创建，如果不创建直接使用会返回报错。
        String consumerGroup = "xxxx";
        final ClientServiceProvider provider = ClientServiceProvider.loadService();
        ClientConfigurationBuilder builder = ClientConfiguration.newBuilder().setEndpoints(endpoints);
        /*
          如果是使用公网接入点访问，configuration还需要设置实例的用户名和密码。用户名和密码在控制台实例详情页获取。
          如果是在阿里云ECS内网访问，无需填写该配置，服务端会根据内网VPC信息智能获取。
         */
        builder.setCredentialProvider(new StaticSessionCredentialsProvider("xxxx", "xxxx"));
        ClientConfiguration clientConfiguration = builder.build();
        //订阅消息的过滤规则，表示订阅所有Tag的消息。
        String tag = "*";
        FilterExpression filterExpression = new FilterExpression(tag, FilterExpressionType.TAG);
        //初始化SimpleConsumer，需要绑定消费者分组ConsumerGroup、通信参数以及订阅关系。
        PushConsumer pushConsumer = provider.newPushConsumerBuilder()
        .setClientConfiguration(clientConfiguration)
        //设置消费者分组。
        .setConsumerGroup(consumerGroup)
        //设置预绑定的订阅关系。
        .setSubscriptionExpressions(Collections.singletonMap(topic, filterExpression))
        //设置消费监听器。
        .setMessageListener(messageView -> {
            try {
                //处理消息并返回消费结果。
                ByteBuffer buffer = messageView.getBody();
                ByteBuffer newBuffer = ByteBuffer.allocate(buffer.capacity());
                for (int i = 0; i < buffer.capacity(); i++) {
                    newBuffer.put(buffer.get(i));
                }
                String result = new String(newBuffer.array());
                LOGGER.info("Consume message={}", JSON.toJSONString(result));
                System.out.println(result);
                return ConsumeResult.SUCCESS;
            } catch (Exception e) {
                LOGGER.error("deal message has error", e);
                return ConsumeResult.FAILURE;
            }
        })
        .build();
        Thread.sleep(Long.MAX_VALUE);

        //如果不需要再使用PushConsumer，可关闭该进程。
        pushConsumer.close();
    }
}
```

<a id="常见问题"></a>

<a id="8847c3ad61g9o"></a>

## 常见问题

<a id="一个事件规则可以配置多个事件目标吗"></a>

<a id="47e055bd6199b"></a>

### 一个事件规则可以配置多个事件目标吗？

可以，同一个事件规则可以配置多个事件目标。如果配置多个事件目标，则同一个事件会投递到配置的每个事件目标中。

<a id="配置完事件规则-但是接收不到事件"></a>

<a id="cc6909ea7f28u"></a>

### 配置完事件规则，但是接收不到事件？

请确认事件转发规则的地域与事件所属地域一致。例如，北京地域配置的规则仅能转发北京地域的事件，无法转发上海等地域的事件。事件总线所在地域可在控制台页面顶部导航栏的地域选择器中查看。

<a id="http-https服务请求超时或者请求错误"></a>

<a id="bf527806a13b5"></a>

### HTTP/HTTPS服务请求超时或者请求错误？

请按以下步骤排查：

1.  检查HTTP/HTTPS服务状态。
    
2.  检查事件目标中配置的 URL 是否正确。
    
3.  检查事件目标配置的Network类型：
    
    -   PublicNetwork：公网，需确保 URL 可被公网访问。
        
    -   PrivateNetwork：VPC网络，若选择此项，需正确配置VPC、vSwitch和SecurityGroup信息。
        
        -   检查VPC网络和交换机配置是否正确。
        -   检查网络安全组配置是否正确。
4.  其他参数配置：请参见[事件目标参数](https://help.aliyun.com/zh/eventbridge/user-guide/event-target-parameters#section-tpm-hnw-bdr)。
