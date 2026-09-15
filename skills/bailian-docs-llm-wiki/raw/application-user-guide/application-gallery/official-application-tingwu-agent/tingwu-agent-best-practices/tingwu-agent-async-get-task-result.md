# 通过回调获取异步任务结果

本文介绍如何以异步回调获取听悟Agent任务结果。

听悟Agent任务创建接口为异步接口。您可通过两种方式获取结果：

1.  主动轮询查询接口（参见[汽车销售服务洞察API参考](raw/application-user-guide/application-gallery/official-application-tingwu-agent/tingwu-automotive-service-insights/tingwu-automotive-service-insights-api.md)或[购车客户画像API参考](raw/application-user-guide/application-gallery/official-application-tingwu-agent/tingwu-automotive-customer-profile/tingwu-automotive-customer-profile-api.md)）
2.  配置回调通知（本文档核心内容）

## 前提条件

-   [开通](https://common-buy.aliyun.com/?commodityCode=sfm_TingWuAgent_public_cn)通义听悟 Agent 服务。
-   若使用阿里云事件总线，需[开通事件总线EventBridge并授权](https://help.aliyun.com/zh/eventbridge/getting-started/activate-eventbridge-and-grant-permissions-to-a-ram-user)。

## 注意事项

1.  仅SDK/API调用触发回调，阿里云百炼提交的任务不触发
2.  HTTP回调与EventBridge回调的`data`字段一致
3.  两种回调方式的通知节奏相同

## 基于HTTP进行回调

### 步骤1：构建回调接收服务

构建HTTP服务接收回调消息：

```
package com.alibaba.langpower;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.ResponseBody;
@Controller
@SpringBootApplication
public class TingwuAgentCallbackDemoApplication {
    public static void main(String[] args) {
        SpringApplication.run(TingwuAgentCallbackDemoApplication.class, args);
    }
    @PostMapping("/tingwu-agent/callback")
    @ResponseBody
    public String receiveTingwuAgentCallbackEvent(@RequestBody String data) {
        System.out.println("Received callback data: \n" + data);
        return "Callback received!";
    }
}
```

### 步骤2：测试回调服务

使用curl验证服务可用性：

```
# 将 {your-external-service-url} 替换为实际的URL
curl --request POST 'http://{your-external-service-url}/tingwu-agent/callback' \
--header 'Content-Type: application/json' \
--data '{
    "output": {
        "test": "checkSyncConf1753325301***"
    },
    "requestId": "61b093d1200e4286ae5d5b15448698f2"
}'
```

### 步骤3：配置回调参数

进入[阿里云百炼控制台](https://bailian.console.aliyun.com/?tab=app#/app/app-market/tingwu/tingwu-automotive-service-insights)，创建或选择已创建的应用，单击调试配置，进入配置界面。回调方式选择**HTTP post协议**，填写真实回调地址并发布应用。

配置回调地址后，服务端需返回 200 状态码，项目才能创建成功。回调消息的 JSON 格式示例包含 `output` 对象（含 `test` 字段）和 `requestId` 字段。

### 步骤4：验证回调结果

使用SDK创建任务后（参见SDK文档），回调服务将分阶段接收：

1.  阶段1：接收转写任务信息

```
{
    "output": {
        "transcriptionPath": "https://***.oss-cn-hangzhou.aliyuncs.com/agentic/prepub/CommonDataField/transcription/1627865****/llm-3cx2a3o4n8y****/2025/07/24/5c6117f77a274cf8b795c8749c28b****?Expires=175341****&OSSAccessKeyId=YOUR_ACCESS_KEY_ID&Signature=YOUR_SIGNATURE",
        "status": 1,
        "taskInfo": {
            "appId": "tw_gDEAnYwAIs****",
            "dataId": "fgVnGZkX5x****",
            "model": "tingwu-automotive-service-insights",
            "userId": "1627865****",
            "userSpaceId": "llm-3cx2a3o4n8y****"
        }
    },
    "requestId": "5038efee3f3a448bb600fc5617fc****"
}
```

2.  阶段2：接收任务结果

```
{
    "output": {
        "transcriptionPath": "https://***.oss-cn-hangzhou.aliyuncs.com/agentic/prepub/CommonDataField/transcription/1627865****/llm-3cx2a3o4n8y****/2025/07/24/5c6117f77a274cf8b795c8749c28b****?Expires=175341****&OSSAccessKeyId=YOUR_ACCESS_KEY_ID&Signature=YOUR_SIGNATURE",
        "status": 0,
        "saleInsightsPath": "https://***.oss-cn-hangzhou.aliyuncs.com/agentic/prepub/CommonDataField/saleInspec/1627865****/llm-3cx2a3o4n8y****/2025/07/24/7b6271d72bc4408b8e2801ebfcf2****?Expires=175341****&OSSAccessKeyId=YOUR_ACCESS_KEY_ID&Signature=YOUR_SIGNATURE",
        "serviceInsightsPath": "https://***.oss-cn-hangzhou.aliyuncs.com/agentic/prepub/CommonDataField/servInspec/1627865****/llm-3cx2a3o4n8y****/2025/07/24/b8574b1b92184d4caae003408896****?Expires=175341****&OSSAccessKeyId=YOUR_ACCESS_KEY_ID&Signature=YOUR_SIGNATURE",
        "taskInfo": {
            "appId": "tw_gDEAnYwAIs****",
            "dataId": "fgVnGZkX5x****",
            "model": "tingwu-automotive-service-insights",
            "userId": "1627865****",
            "userSpaceId": "llm-3cx2a3o4n8y****"
        }
    },
    "requestId": "6005f5c621794168a508cb2dff3a****"
}
```

其中HTTP通知协议和事件总线发送的事件中的一级字段data对应的value是相同的，可以参考事件总线里的协议。

同时为HTTP设计了指数退避的重试策略，在失败后会进行6次重试，重试间隔为：1秒，2秒，5秒，10秒，30秒，60秒。

### 任务失败后通过回调状态重新发起任务

当回调返回的 `status` 字段值不为 `0`（成功）时，表示任务执行失败。您可以在回调接收服务中根据任务状态实现自动重试逻辑。

实现步骤：

1.  在回调接收服务中解析回调消息的 `status` 字段。`status` 为 `0` 表示成功，非 `0` 表示失败。
2.  任务失败时，从回调消息的 `taskInfo` 中提取 `appId` 和原始请求参数，调用任务创建接口重新提交任务。
3.  重试时采用指数退避策略（如间隔 5 秒、10 秒、30 秒），避免短时间内大量重试导致请求被限流。

如使用 EventBridge 回调方式，对应的失败事件类型为 `tingwuagent:TaskStateUpdated:AgentTaskFailed`，处理逻辑相同。

## 基于阿里云[事件总线](https://help.aliyun.com/zh/eventbridge/product-overview/what-is-eventbridge)进行回调

### 步骤1：创建事件规则

1.  [开通](https://help.aliyun.com/zh/eventbridge/getting-started/activate-eventbridge-and-grant-permissions-to-a-ram-user)EventBridge并进入EventBridge[控制台](https://eventbridge.console.aliyun.com/cn-beijing/event-buses)
    
2.  地域选择**华北2（北京）**
    
3.  单击**创建规则**，配置基本信息
    
    在顶部区域选择器中选择**华北2（北京）**，在左侧导航栏进入**default**事件总线的**事件规则**页面。
    
    **事件总线**默认为`default`（只读），**名称**填写`tingwuEBNotificationDemo`，**描述**填写`tingwuEBNotificationDemo`。
    
4.  配置事件模式
    
    -   事件源：`acs.tingwuagent`
    -   事件类型：按需选择
    
    本示例中选择以下三种事件类型：`tingwuagent:TaskStateUpdated:AgentSubTaskCompleted`、`tingwuagent:TaskStateUpdated:AgentTaskFailed`、`tingwuagent:TaskStateUpdated:AgentWholeTaskCompleted`。
    
5.  配置事件目标（以RocketMQ为例，EventBridge会将tingwuAgent的回调消息投递到相应的EventBridge实例中）
    
    **版本**选择**RocketMQ 5.x**，**实例 ID**选择目标实例，**Topic**选择**tingwuEBNotificationDemo**，配置**VPC**和**交换机**，**消息体**选择**完整事件**，然后单击**创建**。
    
6.  单击**创建**按钮
    

### 步骤2：配置回调方式

进入阿里云百炼控制台，创建或选择已创建的应用，单击调试配置，进入配置界面。回调方式选择**事件总线**并发布应用。

处理结果将按事件总线北京Region的default配置发送到您的服务，需提前开通阿里云事件总线。

### 步骤3：验证回调结果

1.  使用SDK创建一个客户画像分析任务，然后在EventBridge中的default总线中，看到两条有tingwuAgent发送的回调消息。
    
    在**事件追踪**页面，将事件源设置为 `acs.tingwuagent` 进行查询，可看到两条事件，事件类型分别为 `tingwuagent:TaskStateUpdated:AgentWholeTaskCompleted`（整体任务完成）和 `tingwuagent:TaskStateUpdated:AgentSubTaskCompleted`（子任务完成）。
    
2.  在配置好的rocketMq实例中查看EventBridge路由到其中的消息。
    
    在**消息队列 RocketMQ 版**控制台，依次进入**实例列表** > **Topic 管理** > **Topic 详情**页面，选择**消息查询** Tab。将查询方式设置为**按 Topic 查询**，时间范围设置为**最近1小时**，单击**查询**。若结果表格中出现消息记录，则表示 EventBridge 回调成功。
    

### 事件类型以及回调事件协议

#### 汽车销售服务洞察、购车客户画像、通用服务洞察Agent的回调协议

**事件类型**

**事件描述**

**事件协议参考**

tingwuagent:TaskStateUpdated:AgentSubTaskCompleted

子任务完成后的回调消息。

[汽车销售服务质检、购车客户画像、通用服务洞察Agent](https://eventbridge.console.aliyun.com/cn-beijing/event-bus/default/event-source/acs.tingwuagent/detail)

tingwuagent:TaskStateUpdated:AgentTaskFailed

任务失败的回调消息。

tingwuagent:TaskStateUpdated:AgentWholeTaskCompleted

整个任务完成后的回调消息。

#### 会议纪要Agent的回调协议

**事件类型**

**事件描述**

**事件协议参考**

tingwuagent:TaskStateUpdated:MeetingAgentSubTaskCompleted

子任务完成后的回调消息。

[会议纪要Agent](https://eventbridge.console.aliyun.com/cn-beijing/event-bus/default/event-source/acs.tingwuagent/detail)

tingwuagent:TaskStateUpdated:MeetingAgentTaskFailed

任务失败的回调消息。

tingwuagent:TaskStateUpdated:MeetingAgentWholeTaskCompleted

整个任务完成后的回调消息。

### 事件总线通知节奏

#### 汽车销售服务洞察、购车客户画像、通用服务洞察Agent

Agent的结果会分为几个阶段进行返回，下面是各Agent的通知节奏。

-   任务成功：
    
    -   tingwuagent:TaskStateUpdated:AgentSubTaskCompleted：转写任务完成
    -   tingwuagent:TaskStateUpdated:AgentWholeTaskCompleted：所有任务完成
-   任务失败：收到tingwuagent:TaskStateUpdated:AgentTaskFailed回调通知
    

#### 会议纪要Agent

-   任务成功：
    
    -   tingwuagent:TaskStateUpdated:AgentSubTaskCompleted：会议纪要的每个子任务完成。
    -   tingwuagent:TaskStateUpdated:AgentWholeTaskCompleted：会议纪要任务完成
-   任务失败：收到tingwuagent:TaskStateUpdated:AgentTaskFailed回调通知
