# 实时转写能力集成

本文介绍如何快速集成听悟智能纪要的实时转写能力。

## **前提条件**

1.  已开通通义听悟-智能纪要后付费服务。
    
2.  已发布一个智能纪要应用，您可以访问[通义听悟-智能纪要控制台](https://bailian.console.aliyun.com/?tab=app#/app/app-market/tingwu/tingwu-meeting-summary)查看您的应用。
    

## **接入流程**

### **1\. 配置Agent**

1.  在 应用配置 - Agent - 百炼应用 - 添加 - 推荐应用 中找到智能纪要并勾选，并确保本应用已开启意图识别功能。
    
2.  点击智能纪要右侧的设置按钮，进入配置应用。
    
3.  在“选择通义听悟应用”处选择一个您已发布的智能纪要应用。
    
4.  您可以对实时录音总结设置进行修改，各配置项的含义如下：
    
    1.  启动指令：启动实时转写的个性化指令，如开启会议实时录制等。若不设置，也可以通过“启动实时转写”等默认指令启动实时转写。
        
    2.  恢复指令：恢复实时转写的个性化指令，如恢复会议实时录制等。若不设置，也可以通过“恢复实时转写”等默认指令恢复实时转写。
        
    3.  退出/暂停唤醒词：当进入实时转写后，为避免误退出，您需要同时说出唤醒词及退出/暂停命令才能退出/暂停实时语音转写，如“小云，退出实时转写”。若不设置，默认唤醒词为“小云”。为了保证识别效果稳定，建议您同步将唤醒词加入听悟智能纪要Agent的热词中，以提升识别准确性。
        
5.  点击确定，保存并发布应用。您也可以在控制台页面通过语音指令测试实时转写能力。
    

### **2\. 交互流程**

整体交互流程如图所示：

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4637314671/p1027755.png)

下面详细介绍各个步骤：

1.  您可以通过多模态交互的WebSocket或RTC链路正常与多模态服务端建立连接，然后发出语音指令：“开启实时转写”，即可调用智能纪要Agent的实时转写能力。开启参数格式请参考[开启转写参数](#7ce322bc94dll)。
    
    1.  您配置的自定义启动指令在此生效。
        
    2.  您可以在语音指令中指定是否开启翻译、翻译语种、会议发言人数等参数覆盖您在听悟应用中的配置，如：“开启实时转写，并帮我翻译成英语，有多个发言人”。若指令中未提取到翻译、发言人选项则会按照听悟应用中的配置进行纪要生成。
        
    3.  注意您只能在全双工duplex模式下使用实时转写能力。
        
2.  当指令意图被正确路由到听悟Agent后，多模态应用服务端会返回一个名为meeting\_state\_change的端指令，其中包含转写已启动状态及转写的dataId，您需要妥善保存此dataId，后续需要通过该dataId恢复转写。端指令参数及含义见[端指令列表](#b7f2ece95e3kv)。
    
3.  您可以正常通过多模态交互的WebSocket或RTC链路发送语音流。
    
4.  在开启实时转写后， 多模态服务将不会回复语音指令，而是会实时返回转写结果或翻译结果。结果参数格式请参考[转写结果参数](#a8462a5144hpd)**。**
    
5.  您可以通过“唤醒词+暂停实时转写”的语音指令暂停当前实时转写，听悟会暂时保存当前实时转写的结果，保存期限为开启转写后的24小时内。
    
6.  多模态应用服务端会返回一个名为meeting\_state\_change的端指令，其中包含转写已暂停状态及转写的dataId。端指令参数及含义见[端指令列表](#b7f2ece95e3kv)。收到该端指令后，会自动退出到多轮对话模式，您可以继续与语音助手进行交互。
    
7.  您可以通过语音指令“恢复实时转写”恢复指定dataId的实时转写，dataId的有效期为24小时，超过后结果将丢失。恢复转写时，dataId需要在Start指令中携带，具体参数格式请参考[恢复转写参数](#f3dc3244bbc0y)。
    
    1.  您配置的自定义恢复指令在此生效。
        
    2.  若您尝试恢复错误的或已过期的dataId，多模态服务端会回复您固定提示语：“重启失败，录音已过期”；若您未传入dataId，调用会失败。
        
8.  当指令意图被正确路由到听悟Agent后，多模态应用服务端会返回一个名为meeting\_state\_change的端指令，其中包含转写已恢复状态及转写的dataId。端指令参数及含义见[端指令列表](#b7f2ece95e3kv)。
    
9.  您可以通过“唤醒词+退出/结束实时转写”的语音指令结束当前实时转写，听悟会自动创建纪要生成任务，并根据您在听悟应用中的配置生成对应的摘要、待办等智能能力结果。
    
10.  多模态应用服务端会返回一个名为meeting\_state\_change的端指令，其中包含转写已停止状态及转写的dataId。端指令参数及含义见[端指令列表](#b7f2ece95e3kv)。收到该端指令后，会自动退出到多轮对话模式，您可以继续与语音助手进行交互。
     

### **3\. 获取生成的智能纪要**

成功结束实时转写后，您可以通过异步方式等待纪要生成结束并推送到您的事件总线服务中，具体步骤请参考[异步获取智能纪要结果](https://help.aliyun.com/zh/model-studio/fast-integrate-offline-tingwu-meeting-agent#b1bfad5d5bbza)。

## **开启转写参数**

您需要在Start指令中设置如下参数：

参数名称

类型

说明

payload.parameters.upstream.mode

string

交互模式设置，实时转写只能设置为duplex，其他模式无效。

## **恢复转写参数**

您需要在Start指令中设置如下参数：

参数名称

类型

说明

payload.parameters.upstream.mode

string

交互模式设置，实时转写只能设置为duplex，其他模式无效。

payload.parameters.biz\_params.user\_defined\_params.tingwu\_meeting.dataId

string

需要恢复的转写dataId

## **转写结果参数**

Agent转写结果会在RespondingContent事件返回：

参数名称

类型

说明

payload.output.extra\_info.agent\_result

object

Agent执行结果

payload.output.extra\_info.agent\_result.agentId

string

固定为tingwu-meeting-realtime

payload.output.extra\_info.agent\_result.agentData

json

转写结果

agentData中可能会存在三种事件，分别是speech-listen、recognize-result及speech-end，其含义和参数列表请参考[接收服务端返回的事件](https://help.aliyun.com/zh/model-studio/tingwu-meeting-api-websocket#cb15739e9d5f4)。

## **端指令列表**

端指令参数

类型

说明

payload.output.extra\_info.commands

string

端指令列表，您可以反序列化为一个JsonArray

payload.output.extra\_info.commands\[i\].name

string

端指令的名称，智能纪要实时转写名称为：meeting\_state\_change

payload.output.extra\_info.commands\[i\].params

JsonArray

执行端指令所需的参数列表，固定包含两个参数。

payload.output.extra\_info.commands\[i\].params\[0\].name

string

端指令的第一个参数名称，标识当前转写状态，固定为state

payload.output.extra\_info.commands\[i\].params\[0\].normValue

string

端指令的第一个参数值，标识当前转写状态。

转写已开启：state\_started

转写已暂停：state\_paused

转写已恢复：state\_resumed

转写已结束：state\_stopped

转写已过期：state\_expired

payload.output.extra\_info.commands\[i\].params\[0\].name

string

端指令的第二个参数名称，标识当前转写的dataId，固定为dataId

payload.output.extra\_info.commands\[i\].params\[0\].normValue

string

端指令的第二个参数值，当前dataId的值，形如：Rq\*\*\*\*\*\*4nro。
