# 百炼及三方Agent直连调用

本文档介绍将用户的请求直接透传给您在百炼平台自己创建的应用（包括Agent、工作流、智能体编排）以及三方Agent（通过A2A协议对接）的方法。

## 直连Agent配置方法

您可以关闭「文本模型」，开启「直连Agent」开关，通过直连Agent方式调用其它百炼应用或第三方Agent。![截屏2026-03-30 17](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8925294771/p1063619.png)

**说明**

1.  目前该功能仅多模态应用支持，语音应用暂不支持。
    
2.  关闭文本模型后，只下发意图识别结果，欢迎语、提示词、对话承接语、知识库、长期记忆暂不可用，开启后即可恢复。
    

## 通过管控台集成百炼Agent和三方Agent

当前您可以在多模态应用中使用该方式。套件提供两种方式接入您的业务Agent。

1.  百炼Agent：参见[接入百炼平台应用](https://help.aliyun.com/zh/model-studio/multimodal-call-app)创建和配置说明。
    
2.  三方Agent：您完成 A2A 服务部署后在管控台集成，参见 [AgentCard](https://help.aliyun.com/zh/model-studio/multimodal-integration-a2a/#854b8c0b10ozm)。
    

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1007419671/p1048468.png)

## 建联传参

在与服务的建立连接时，通过配置agent\_command创建与 A2A/百炼 Agent 服务连接管道，本次请求所有文本和识别请求直接透传Agent处理。

关键参数，parameters.bizParams.commands\[\]

bizParams

参数

一级参数

类型

说明

commands\[\]

name

String

固定为“agent\_command”

exec\_params

Object

app\_id

String

管控台应用列表中的 agentId

intent

String

固定为"open\_"+ agentId

user\_defined\_params

Object

配置给 Agent 的参数

agentId

Object

以 agentId为 key的对象，对象中的参数会传递给 Agent

**parameters.bizParams.commands\[\]**

```
[{
  "name":"agent_command",
  "exec_params":{
    "app_id": "xxxxx",
    "intent": "open_xxxxx"
  }
}]
```

**以 Android SDK 设置参数为例**

```
private MultiModalRequestParam buildRequestParams() {

    JSONArray commands = new JSONArray();
    try {
        JSONObject command = new JSONObject();
        command.put("name", "agent_command");

        JSONObject execParams = new JSONObject();
        execParams.put("app_id", "tpa_2009506107285893120");
        execParams.put("intent", "open_tpa_2009506107285893120");
        command.put("exec_params", execParams);
        commands.put(command);

    } catch (JSONException e) {
        throw new RuntimeException(e);
    }

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
                .intermediateText("transcript")
                .build())
    .bizParams(MultiModalRequestParam.BizParams.builder()
               .userCustomParams(Collections.singletonMap("commands", commands))
               .build())
    .build();
}
```

## 通过UpdateInfo更新参数

在对话过程中如需携带参数给您的Agent。可通过此方式将参数透传，透传参数会在下一次请求Agent服务时带入。

通过该方式设置的参数每次请求Agent都会携带。您可以通过UpdateInfo更新同名参数。

parameters.bizParams

参数

一级参数

类型

说明

user\_defined\_params

Object

配置给 Agent 的参数

agentId

Object

以 agentId为 key的对象，对象中的参数会传递给 Agent

user\_prompt\_params

Object

当您使用百炼**智能体应用**时，通过此结构传递智能体提示词中定义的参数。

**parameters.bizParams.user\_defined\_params**

```
"user_defined_params":{
    "xxxxx":{
        "user_prompt_params":{
            "age": 8,
            "text": "今天是 2025年 1 月 9 日"
        }
    }
}
```

**以 Android SDK 设置参数为例**

```
private void updateParams(){
        try {
            JSONObject userAgentPromptParams = new JSONObject();
            userAgentPromptParams.put("age", 8);
            userAgentPromptParams.put("text","今天是 2025年 1 月 9 日");
            JSONObject agentIdParams = new JSONObject();
            agentIdParams.put("user_prompt_params", userAgentPromptParams);

            JSONObject userDefinedParams = new JSONObject();
            userDefinedParams.put("tpa_2009506107285893120", agentIdParams); //key为app_id

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

## 通过UpdateInfo透传图片

如果您的 Agent 支持图像模态的交互，您也可以将图片以链接或者 base64 数据的方式透传给 Agent。

关键参数：parameters.images\[\]

images\[\]

参数

类型

说明

type

String

图片类型，支持"url"/"base64"

value

String

图片连接或者 base64 编码数据。注意以 base64 提交数据原始图片大小不应超过 180KB。

```
{
  "images": [{
    "type": "base64",
    "value": "\/9j\/4QDKRXhpZgAATU0AKgAAAAgABgESAAMAAAABAAEAAAEaAAUAAAABAAAAVgEbAAUAAAABAAAAXgEoAAMAAAABAAIAAAITAAMAAAABAAEAAIdpAAQAAAABAAAAZgAAAAAAAABIAAAAAQAAAEgBbEWenR5HJ\/lXXa62IW244FaR0RhN3ZwVp4fkljIRuleZeOtFu4oWAPavdtElAgbPYV5V46uh09KiT90qC1R80y2d---"
  }]
}
```

**以 Android SDK 设置参数为例**

```
MultiModalRequestParam updateParams = null;
try {
    updateParams = MultiModalRequestParam
    .builder()
    .images(MultimodalDialogActivity.this.getImageList())
    .build();
} catch (JSONException e) {
    e.printStackTrace();
}

multimodalDialog.updateInfo(updateParams);
```
