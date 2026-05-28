# 调用三方语音模型

本文主要介绍如何调用三方语音模型实现语音识别和语音合成，并通过文本调用多模态交互开发套件的交互能力实现完整交互链路。

百炼多模态交互开发套件集成了大模型语音识别和语音合成，并提供 VAD、AEC 等音频算法提升交互效果。

如果我们提供的服务不能满足您的特定需求，如语种、音色等，您也可以使用三方语音服务替换千问多模态交互开发套件中提供的语音识别、语音合成能力。我们支持通过文本调用后续对话链路，以及仅以文本模式输出对话结果。

基于三方语音模型自身的能力特性，可能增加语音对话的延迟，以实际测试效果为准。

## **调用流程**

### **调用三方语音流程图**

您可以使用三方语音识别结果调用多模交互服务；并使用服务返回的文本响应通过三方语音合成服务合成音频回复。

![截屏2025-07-09 20](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5856452571/p983815.png)

### **使用三方语音识别（ASR）结果请求对话**

您可以调用三方的语音识别服务进行语音识别。并使用其识别结果调用百炼多模交互服务。

获取完整语音识别结果后，您可以使用文本直接调用的方式请求多模态交互服务。

您需要在客户端处于Listening状态下发送`requestToRespond`请求。 参数说明：

-   请求中 type 字段使用"prompt"。
    
-   请求参数中 text 字段为您要输入的第三方识别文本。
    

若当前状态非Listening，需要先调用`Interrupt` 接口打断当前播报。

Java

```
// 创建UpdateParams对象（第三个参数不能为null）
UpdateParams params = new UpdateParams();
dialog.requestToRespond("prompt", "今天天气怎么样？", params);
```

Python

```
dialog.request_to_respond("prompt", "今天天气怎么样？", parameters=None)
```

C++

```
Json::Value root;
root["text"] = "今天天气怎么样？";
root["type"] = "prompt";

Json::StreamWriterBuilder writer;
writer["indentation"] = "";

ConvRetCode ret = conversation->SendResponseData(Json::writeString(writer, root).c_str());
```

### **使用文本请求三方语音合成（TTS）**

使用百炼多模交互服务，您可以设置输出对话结果的格式为仅输出【文本】。使用输出文本您可以调用三方的语音合成服务进行语音合成。

**说明**

百炼多模交互输出的对话结果文本支持「流式输出」，推荐您调用的三方 TTS服务也支持「流式合成」。即将多模态对话输出的多个文本片段流式发送给语音合成服务，语音合成服务流式返回合成音频。这种调用方式可以显著的提升系统的交互速度。

参考接口：百炼CosyVoice 语音合成 [Java SDK](https://help.aliyun.com/zh/model-studio/cosyvoice-java-sdk)。
