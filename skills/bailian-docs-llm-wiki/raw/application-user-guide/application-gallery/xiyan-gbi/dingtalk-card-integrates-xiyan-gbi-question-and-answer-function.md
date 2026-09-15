# 钉钉客户端（卡片）中集成析言GBI问答功能

本文基于析言GBI的API实现了在钉钉客户端的智能数据问答功能。旨在帮助您熟悉析言GBI的API的使用，以便在实际项目中将析言GBI的API灵活运用到一些常见的终端上。

## 前提条件

-   已开通阿里云百炼服务。
-   已[获取Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)。
-   已[获取AccessKey ID和AccessKey Secret](https://help.aliyun.com/zh/model-studio/get-accesskey-appid-and-agentkey)。
-   已在析言GBI的**[数据表管理](https://bailian.console.aliyun.com/xiyan#/dataManagement/dataSourceM)**中授权连接了数据库。具体操作，请参见[数据库连接](https://help.aliyun.com/zh/model-studio/xiyan-gbi-user-guide#8e5d17697392b)。
-   已注册钉钉企业。
-   已注册钉钉开发者。

## 步骤1：创建钉钉应用

1.  登录[钉钉开放平台后台](https://open-dev.dingtalk.com)。
    
2.  创建企业内部应用。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8662085371/p894932.png)
3.  添加**应用能力机器人**。
    
4.  设置机器人的**消息接收模式**为**Stream模式**。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8662085371/p894933.png)
5.  开通权限、**调用企业API基础权限**、**企业内机器人发送消息权限**、**互动卡片实例写权限**、**AI卡片流式更新权限**。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8662085371/p894937.png)
6.  将**事件订阅推送方式**设置为**Stream模式推送**，保存后完成接入验证。
    
    ![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8662085371/p894941.png)
7.  将**版本管理与发布发布应用**，创建新版本并发布。
    
    ![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8662085371/p894942.png)

## 步骤2：创建卡片模板

1.  登录[钉钉卡片平台](https://open-dev.dingtalk.com/fe/card)。
    
2.  单击**模板管理新建模板**。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8662085371/p894945.png)
3.  单击**导入模板**，导入[模板文件](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241226/mkighb/card_template.json)并保存。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8662085371/p894948.png) ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8662085371/p894949.png)

## 步骤3：开发钉钉机器人后端应用

此步骤基于Java语言，实现钉钉后端机器人、析言问答服务SDK、钉钉卡片的集成。

1.  提供两种获取项目代码方式。
    
    1.  参考[钉钉官方文件](https://github.com/open-dingtalk/dingtalk-card-examples/tree/main/examples/AI%20%E5%8D%A1%E7%89%87%E5%90%8C%E6%97%B6%E6%9B%B4%E6%96%B0%E6%99%AE%E9%80%9A%E5%8F%98%E9%87%8F%E5%92%8C%E6%B5%81%E5%BC%8F%E5%8F%98%E9%87%8F/java)，自行修改代码。
    2.  直接使用析言提供的[测试文件](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250414/ncszrh/xiyan-dingding-demo.zip)。
2.  如果您使用析言提供的测试文件，您需要替换`Properties`中的关键参数，`client-id`和`client-secret`，以及代码中的`templateId`。
    

```
xiyan.access-key-id=xx
xiyan.access-key-secret=xx
xiyan.workspace-id=xxx
dingtalk.app.client-id=xx
dingtalk.app.client-secret=xx
openApiHost=https://api.dingtalk.com
```

-   `client-id`和`client-secret`：您可以在**步骤1：创建钉钉应用**的**凭证与基础信息**页面获取。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9636758471/p962484.png)
-   `templateId`：您可在**步骤2：创建卡片模板**的**模板列表**页面获取。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9636758471/p962515.png)

3.  运行Java项目，检查应用初始化和网络连接是否正常。

```
2024-12-26 15:30:04.004  INFO 48685 --- [ection-pool-2-1] .d.o.a.s.n.w.WebsocketTransportConnector : [DingTalk] start websocket connection, uri=wss://wss-open-connection.dingtalk.com:443/connect
2024-12-26 15:30:04.472  INFO 48685 --- [           main] o.s.b.a.e.web.EndpointLinksResolver      : Exposing 2 endpoint(s) beneath base path '/actuator'
2024-12-26 15:30:04.556  INFO 48685 --- [           main] o.s.b.w.embedded.tomcat.TomcatWebServer  : Tomcat started on port(s): 8080 (http) with context path ''
2024-12-26 15:30:04.589  INFO 48685 --- [           main] com.aliyun.xiyan.demo.Application        : Started Application in 5.972 seconds (JVM running for 6.717)
2024-12-26 15:30:04.984  INFO 48685 --- [ection-pool-2-1] c.d.o.a.s.n.core.DefaultSessionPool      : [DingTalk] connection is established, connectionId=xxxx-xxx-xxx-xxx-xxx
```

## 步骤4：效果验证

1.  登录钉钉App，在消息框中`@机器人`进行问答。在Java应用日志中确认，是否有收到事件通知。

```
2024-12-26 15:31:32.758  INFO 48685 --- [lk-Consumer-1-1] com.aliyun.xiyan.demo.ChatBotHandler     : received message: 每月访客人数趋势
```

2.  您可以在钉钉App聊天窗，查看卡片渲染情况。
    

## 相关文档

如果您想参考析言GBI使用，请参见[使用指南](raw/application-user-guide/application-gallery/xiyan-gbi/xiyan-gbi-user-guide.md)。

如果您想应用析言GBI，请参见[析言GBI关于云服务访问数据库最佳实践](raw/application-user-guide/application-gallery/xiyan-gbi/gbi-best-practices.md)。
