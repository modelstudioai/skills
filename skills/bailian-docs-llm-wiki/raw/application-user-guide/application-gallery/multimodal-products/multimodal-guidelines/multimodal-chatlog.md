# 对话日志接入

如果您需要保存全量对话日志，需要使用阿里云事件总线能力，操作步骤请查看本文档。

## **操作步骤**

1.  开通事件总线：
    
    在多模态交互应用或语音交互应用的**配置应用**页面，点击**存储地址**配置处的**事件总线** 。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9345897471/p959429.png)页面会自动跳转到事件总线官方地址。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9345897471/p959466.png)
    
    > 如果您是首次进入，需点击**授权并开通事件总线**（事件总线目前是免费的）。
    
    > 地域：北京，聊天日志默认发送到default事件总线中。
    
2.  配置事件规则：
    
    1.  点击 **default** 事件总线右侧**操作**列下的**事件规则**。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9345897471/p959470.png)
        
    2.  在**事件规则**页面，您可以参考以下步骤配置事件规则。
        
        1.  点击**创建规则**，在创建规则面板填写**名称**（名称示例： `multi-modal-chat-log` ）， 输入规则**描述**，完成后点击**下一步**。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9345897471/p959475.png)
            
        2.  配置事件模式，完成后点击下一步。
            
            1.  选择事件源：`acs.multimodal`。
                
            2.  选择事件类型：`multimodal:Dialogue:ChatLogPush`。
                
            
            ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9345897471/p959479.png)
            
        3.  配置事件目标（聊天日志消费方式）：
            
            > 同一个事件支持配置多个事件目标。
            
            1.  选择**服务类型**（有些服务类型可能需要先完成授权），支持的类型有：RocketMQ、飞书、企业微信、日志服务、数据库、短信、SLS等。
                
            2.  按照服务类型的配置要求，完成事件目标配置。
                
            
            如果选择**云消息队列 RocketMQ 版**，您需按照页面上的要求填写配置（实例 ID、Topic、Vpc、交换机等），后续聊天日志就会发送到RocketMQ的对应配置中，用户只需要消费MQ中的消息即可。 其余服务类型配置步骤类似。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9345897471/p959483.png)
            
        

### **事件总线文档**

-   事件总线官方文档：[什么是事件总线EventBridge](https://help.aliyun.com/zh/eventbridge/product-overview/what-is-eventbridge)
    
-   事件总线API文档： [API概览](https://help.aliyun.com/zh/eventbridge/developer-reference/api-eventbridge-2020-04-01-overview)
    

## **聊天日志追踪**

1.  在**事件总线**页面，点击 **default** 事件总线右侧**操作**列下的**事件追踪**。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9345897471/p959488.png)
    
2.  在**事件追踪**页面，支持按时间范围查询和按事件ID查询。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9345897471/p959492.png)
    
    **说明**
    
    事件ID和聊天日志的`requestId`是同一个。
    
    在下图示例中，事件ID即为聊天日志中的`requestId`。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9345897471/p959493.png)
    

## **聊天日志格式说明**

-   事件总线关键字段说明
    
    -   aliyunaccountid ： 登录账号的阿里云UID
        
    -   data ： 聊天日志
        
    -   id: 事件ID （和聊天日志的requestId一致）
        
    -   aliyuneventbusname ： 事件总线名称
        
    -   source 事件源
        
    -   type : 事件类型
        
-   聊天日志字段说明（data）：
    
    -   code ： 失败的错误码，成功时为空
        
    -   message: 失败的错误信息，成功时为空
        
    -   requestId ： 聊天日志唯一的ID
        
    -   sessionId ： 聊天日志会话ID
        
    -   input ： 会话请求数据，JSON字符串
        
    -   output: 会话响应数据，JSON字符串
        
-   日志示例代码如下：
    
    ```
    {
        "datacontenttype": "application/json;charset=utf-8",
        "aliyunaccountid": "1406635223510007",
        "data": {
            "output": "{\"biz_info\":{\"agent_infos\":[{\"code\":\"telephone\",\"name\":\"telephone\"}],\"intent_infos\":[{\"domain\":\"telephone\",\"intent\":\"confirm\",\"slots\":[]}]},\"output\":{\"commands\":[{\"name\":\"call\",\"params\":[{\"name\":\"phone_number\",\"norm_value\":\"10086\",\"value\":\"10086\"},{\"name\":\"record\",\"norm_value\":\"False\",\"value\":\"False\"}]}],\"text\":\"好的，开始拨打\"}}",
            "input": "{\"biz_params\":{\"chat_history\":[],\"device\":{\"device_id\":\"{\\\"uuid\\\":\\\"0b0d8eaf-c429-46a9-a1fa-6def543887f7\\\"}\"},\"resources\":[],\"user\":{\"user_id\":\"API_TEST\"},\"user_defined_tokens\":{}},\"prompt\":\"确定\"}",
            "code": "",
            "requestId": "a09a51c9233743beae2a2e4ef8cacc3c",
            "sessionId": "0b0d8eaf-c429-46a9-a1fa-6def543887f7",
            "message": ""
        },
        "subject": "acs.multimodal:cn-hangzhou:123456789098****:215672",
        "aliyunoriginalaccountid": "1406635223510007",
        "source": "acs.multimodal",
        "type": "multimodal:Dialogue:ChatLogPush",
        "aliyunpublishtime": "2025-05-13T03:40:11.265Z",
        "specversion": "1.0",
        "aliyuneventbusname": "default",
        "id": "a09a51c9233743beae2a2e4ef8cacc3c",
        "time": "2025-05-13T03:40:11.244Z",
        "aliyunregionid": "cn-hangzhou"
    }
    ```
