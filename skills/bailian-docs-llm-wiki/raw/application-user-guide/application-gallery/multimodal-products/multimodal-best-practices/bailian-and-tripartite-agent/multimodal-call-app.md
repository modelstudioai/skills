# 接入百炼智能体应用

本文介绍如何在多模态交互应用中接入百炼智能体应用，以及在客户端调用。

在多模态交互开发套件中，我们预置了多种官方插件和 Agent。当官方能力不能满足您的特定需求时，您也可以将自己开发的百炼平台应用（如智能体应用、工作流应用等）接入到多模态平台，实现能力更丰富的多模态交互。关于推荐应用模板请参考[百炼应用推荐模板](https://help.aliyun.com/zh/model-studio/agent-template)。

本文档以创建和接入一个【西游记大全】应用为例，介绍如何在多模态应用中接入百炼平台应用。

## **创建和配置百炼应用**

1.  创建百炼平台应用，参考[应用类型介绍](https://help.aliyun.com/zh/model-studio/application-introduction)。
    
2.  配置应用，调整模型、提示词和其他需要的能力。应用名修改为【西游记大全】。
    
3.  测试并发布应用。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9888172571/p986224.png)

## **在多模交互应用中接入**

在您的多模交互应用中导入上个步骤配置好的【西游记大全】。

1.  在菜单Agent - 添加 - 我的应用 中选中【西游记大全】，点击确定导入。
    
2.  发布应用。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9888172571/p986235.png)

## **应用测试和参数配置**

### **应用测试**

在多模应用中导入【西游记大全】后，我们可以在网页进行测试。

进入【西游记大全】应用的方式为语音说： **打开西游记大全,帮我查一下三清是谁**。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9888172571/p986238.png)

### **参数配置**

在【西游记大全】应用中，我们配置了一个名为${user\_name}的参数。代表用户昵称，默认值为“小宝”。

通过 SDK 调用多模应用，我们可以在代码中配置`${user_name}`。

一级参数

二级参数

三级参数

四级参数

参数说明

biz\_params

多模请求参数中的biz\_params

user\_defined\_params

透传用户自定义参数

user\_defined\_app\_id

导入的百炼**应用 id**

user\_prompt\_params

类型为 Object

对应百炼应用prompt 的自定义变量名和值。

-   格式化示例
    

```
{
    "biz_params": {
        "user_defined_params": {
            "84***********************acc": {
                "user_prompt_params": {
                    "user_name": "大米"
                }
            }
        }
    }
}
```

#### **通过UpdateInfo更新参数**

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

#### **通过UpdateInfo透传图片**

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

### **客户端验证**

以 Android SDK 为例。

-   在建联参数中设置变量值。
    

```
HashMap<String, Object> appParams = new HashMap<>();
appParams.put("user_name","大米");
HashMap<String, Object> userPromptParams = new HashMap<>();
userPromptParams.put("user_prompt_params",appParams);
HashMap<String, Object> userDefinedParams = new HashMap<>();
userDefinedParams.put("67f3ad7d6496475483db4a184c926e77",userPromptParams); //西游记大全的 appid

MultiModalRequestParam.BizParams bizParams = MultiModalRequestParam.BizParams
   .builder()
   .userDefinedParams(userDefinedParams)
   .build();
```

-   运行 Demo 通过语音请求【西游记大全】 Agent。由于端侧设置了用户名为“大米”，可以看到 APP 回复的昵称为“大米”，验证链路测试通过。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9888172571/p986380.png)

## **由百炼平台应用主动退出接管模式**

在多模态交互应用中，您可以为接入的百炼平台应用开启“对话接管”模式。开启后，当用户通过“触发指令”唤起该应用，后续的多轮对话将持续由其处理，直到用户说出“退出指令”，或由应用本身主动结束对话。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9332574671/p1031331.png)

除了让用户说出“退出指令”外，百炼应用内部也可以根据自身的业务逻辑，主动判断并决定何时退出接管模式。这种方式更为灵活，能实现更智能的对话流程控制。

应用通过在返回内容的开头添加特定的“指令标记”来实现主动退出。目前支持以下两种退出场景：

-   场景1：应用完成任务并回复后退出
    
    指应用判断当前对话可以结束，并已生成了本轮的最终回复。退出后，多模态平台将仅播报该应用返回的回复内容。
    
    -   **指令标记：**`[#blmm-quit#]`
        
        **使用示例：**应用返回`[#blmm-quit#]再见啦`。用户将只会听到`再见啦`。随后对话将退出当前应用。
        
-   场景2：应用无法处理当前问题，交还控制权后退出
    
    指应用判断自己无法处理用户的当前请求，需要退出并将问题交还给多模态交互主流程来处理。
    
    -   **指令标记：**`[#blmm-rejected#]`
        
        **使用示例：**应用仅返回 `[#blmm-rejected#]`。多模态平台会接管并根据用户的原始问题寻找其他方式来回复，而不会播报任何来自当前应用的内容。
        

## **自定义播报音色**

您还可以为接入的百炼平台应用单独指定音色，以便与主链路的音色进行区分。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9865798671/p1047510.png)

-   除了在管控台为每个接入的百炼平台应用指定音色，您还可以通过API参数进行更精细的音色控制。设置方式
    

入参

配置方式

是否必传

说明

speaker\_1\_voice

SDK

否

指定播报的声音，音色取值范围取决于应用中配置的tts模型支持的声音列表

-   客户端调用示例，在Start消息的payload.biz\_params节点下，通过如下格式设置要使用的播报音色
    

```
{
  "user_defined_params": {
    "请替换为百炼应用ID": {
      "speaker_1_voice": "请替换为百炼应用配置的tts模型对应的音色"
    }
  }
}
```

-   百炼应用ID查看方式
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9865798671/p1047514.png)
