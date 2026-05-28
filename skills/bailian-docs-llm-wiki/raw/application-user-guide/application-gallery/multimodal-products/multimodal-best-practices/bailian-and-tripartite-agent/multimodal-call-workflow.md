# 接入百炼工作流应用

本文主要介绍如何在多模态交互应用中接入百炼工作流和调用方式。

## **创建百炼工作流**

1.创建百炼工作流，详细介绍可参考[工作流应用](https://help.aliyun.com/zh/model-studio/workflow-application/)。

2.创建一个名为【自助食堂】的工作流。

3.测试后发布应用。

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0826629771/p1074630.png)

* * *

## **接入百炼工作流**

1.在您的多模态应用中导入【自助食堂】工作流。

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0826629771/p1074628.png)

2.编辑工作流应用，添加对应的描述；

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0826629771/p1074629.png)

* * *

## **参数配置**

### **直连工作流**

可以在与服务建立连接时，通过参数配置创建和工作流的连接通道，进而实现将请求直接透传给百炼工作流。

详细配置可参考文档：[百炼及三方Agent直连调用](https://help.aliyun.com/zh/model-studio/agent-direct-call)

* * *

### **透传参数**

如果需要给工作流的自定义变量传参，可以通过Start或者UpdateInfo指令来透传更新工作流参数。

parameters.bizParams

参数

类型

说明

user\_defined\_params

Object

配置给 Agent 的参数

agentId

Object

以 agentId为 key的对象，对象中的参数会传递给 Agent

**parameters.bizParams.user\_defined\_params**

```
"user_defined_params":{
    "xxxxx":{
        "name": "小熊食堂"
    }
}
```

**以Android SDK为例**

```
private void updateParams(){
    try {
        JSONObject agentIdParams = new JSONObject();
        agentIdParams.put("name","小熊食堂");

        JSONObject userDefinedParams = new JSONObject();
        userDefinedParams.put("2009506107285893120", agentIdParams); //key为app_id

        MultiModalRequestParam updateParams = MultiModalRequestParam
                .builder()
                .bizParams(MultiModalRequestParam.BizParams.builder()
                        .userDefinedParams(userDefinedParams)
                        .build())
                .build();

        Log.i(TAG, "bizParams: " + updateParams.getParametersAsJson());
        multiModalDialog.updateInfo(updateParams.getParametersAsJson());
    } catch (JSONException e) {
        throw new RuntimeException(e);
    }
}
```

* * *

### **设置增量输出**

如果您想要增量返回工作流结果，需要进行如下配置。

**打开工作流的流式输出开关**

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0826629771/p1074624.png)

**设置多模态增量输出**

在Start消息中设置返回系统回答中间结果，并打开增量下发开关。

parameters.downstream

类型

说明

intermediate\_text

string

控制返回给用户哪些中间文本：

-   transcript：返回用户语音识别结果
    
-   dialog：返回对话系统回答中间结果
    

可以设置多种，以逗号分隔，默认为transcript

incremental\_response

boolean

是否增量返回大模型结果，true为增量，false为全量。默认为false，全量下发

**parameters.downstream**

```
"parameters":{
  "downstream":{
    "intermediate_text": "transcript,dialog",
    "incremental_response": true
  }
}
```

**以Android SDK为例**

```
private MultiModalRequestParam buildRequestParams() {
    Map<String,Object> map = new HashMap<>();
    map.put("incremental_response", true);

    return MultiModalRequestParam.builder()
            .clientInfo(MultiModalRequestParam.ClientInfo.builder()
                    .device(MultiModalRequestParam.ClientInfo.Device.builder()
                            .uuid("uuid_12345").build()) // 请配置为您的设备UUID
                    .userId("your_user_id")  //userid 需要每个用户唯一，建议使用设备UUID。 对话历史会使用 userId关联
                    .build())
            .upStream(MultiModalRequestParam.UpStream.builder()
                    .type("AudioAndVideo")
                    .build())
            .downStream(MultiModalRequestParam.DownStream.builder()
                    .voice("longanhuan") //tts 音色对应的模型需要和管控台配置的模型一致。longxiaochun_v2对应了cosyvoice_v2
                    .sampleRate(48000)
                    .intermediateText("transcript,dialog")
                    .passThroughParams(map)
                    .build())
            .build();
}
```

* * *

## **常见问题排查**

### **返回结果超时**

报错："SOCKET\_TIMEOUT\_EXCEPTION: Read timed out"

需要留意工作流处理的时长，如果超过多模态应用的规定时间后，仍没有返回结果，则会报错。目前时间阈值为10s，建议控制好工作流的处理链路，若有超时的现象，可联系技术人员分析；

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0826629771/p1074626.png)

* * *

### **避免输出JSON格式**

目前多模态应用不会对工作流输出的结果做额外的处理， 因此建议工作流选择文本输出。若输出JSON格式的内容，则JSON格式中的符号也会合成语音进行播报。

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0826629771/p1074627.png)

* * *

### **避免MarkDown格式输出**

输出markdown格式的内容会影响音频的合成，所以要尽量避免输出该格式的内容。通常会在多模态应用的提示词中加入相关限制类的提示词，但容易忽略在工作流中加入限制，进而导致输出了错误输出了markdown格式内容；

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0826629771/p1074625.png)
