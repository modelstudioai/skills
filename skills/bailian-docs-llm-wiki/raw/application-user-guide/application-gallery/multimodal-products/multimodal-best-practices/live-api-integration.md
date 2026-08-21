# 接入视频通话Agent

视频通话能力可以赋予AI感知周围环境、用户行为和状态的视觉理解能力，打造更丰富生动的实时多模态互动体验，例如：文物讲解、景点导览、烹饪指导、模拟面试等。本文介绍如何通过多模交互套件接入视频通话能力。

## **开通视频通话Agent**

在[多模态开发套件](https://bailian.console.aliyun.com/?tab=app#/app/app-market/multi-modal-app)中创建**多模态应用**（语音应用不支持视频通话）。

在应用配置-Agent - 添加 - 推荐应用中添加【视频通话】，并保存应用。

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9367243571/p987567.png)

## **使用官方Android/iOS SDK 进行视频通话**

百炼多模交互 Android 和iOS SDK 内置了 RTC 协议，原生支持音视频录制和传输，通过简单的配置即可方便的实现视频通话功能。

#### **SDK 调用流程**

1.  设置交互链路（`ChainMode`）为`RTC` ，并设置 `upstream.type`为`AudioAndVideo`。
    
2.  进入视频通话 Agent。支持语音或者发送指令方式切换到视频通话。
    
    -   启动对话后直接进入视频通话：启动对话之后，等待对话状态切换到 Listening状态后，发送切换视频对话指令。
        
    -   通过语音命令进入视频通话：在对话建立连接中，语音说“进入视频通话”。
        
3.  服务端返回视频通话 Agent 欢迎语，即成功进入视频通话。
    
4.  退出视频通话 Agent：发送退出指令或者语音说“退出视频通话”。
    

##### **请求参数说明**

通过 requestToRespond 方法请求提交参数如下。

一级参数

二级参数

三级参数

是否必选

说明

parameters

biz\_params

videos

是

类型为 List。list 中的元素为视频请求相关的 object。

```
{
    "header": {
        "action":"continue-task",
        "task_id": "9B32878******************3D053",
        "streaming":"duplex"
    },
    "payload": {
        "input":{
          "directive": "RequestToRespond",
          "dialog_id": "b39398c9dd8147********35cdea81f7",
          "type": "prompt"
        },
        "parameters":{
          "biz_params":{
            "videos": [
                  {
                    "action": "connect", //进入视频模式
                    "type": "voicechat_video_channel"
                  },
                  {
                    "action": "exit",  //退出视频模式
                    "type": "voicechat_video_channel"
                  }
                ]
          }
        }
    }
}
```

##### **调用时序图**

![截屏2025-06-20 11](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9367243571/p987566.png)

##### **关键代码示例**

```
//1. 设置交互类型为AudioAndVideo
MultiModalRequestParam.UpStream.builder().mode("duplex").type("AudioAndVideo").build();

//2. 在建联后发送voicechat_video_channel 请求
private void startVideoMode() {
    if (isVideoMode) return;

    try {
        MultiModalRequestParam updateParams = MultiModalRequestParam.builder().build();
        JSONObject videoObj = new JSONObject();
        videoObj.put("action", "connect");
        videoObj.put("type", "voicechat_video_channel");

        List<JSONObject> videos = new ArrayList<>();
        videos.add(videoObj);

        updateParams.setBizParams(MultiModalRequestParam.BizParams.builder()
                .videos(videos).build());

        multiModalDialog.requestToRespond("prompt", "", updateParams.getParametersAsJson());
        multiModalDialog.setVideoContainer(videoContainer, uiHandler);

        isVideoMode = true;
        runOnUiThread(() -> videoContainer.setVisibility(View.VISIBLE));

    } catch (JSONException e) {
        Log.e(TAG, "启动视频模式失败", e);
    }
}

//3. 开始音视频交互。处理交互流程。注意 demo 中Constant.ChainMode.RTC 类型的处理。
private void handleOutputStarted() {
    if (!isRtcUseInternalAudio()) {
        audioPlayer.pause(true);
        audioPlayer.play();
    }
    if (authParams.getChainMode() == Constant.ChainMode.RTC) {
        //RTC 模式下，tts 合成数据速度为正常比例
        multiModalDialog.sendResponseStarted();
    }
}

private void handleOutputCompleted() {
    Log.d(TAG, "输出完成");
    if (authParams.getChainMode() != Constant.ChainMode.RTC) {
        multiModalDialog.sendResponseEnded();
        audioPlayer.isFinishSend(true);
    }
}
```
```
//1. 设置交互类型为AudioAndVideo
multiBuilder.upStream = MultiModalRequestParam.UpStream(builder: { upstreamBuilder in
                upstreamBuilder.mode = mode.rawValue
                upstreamBuilder.type = "AudioAndVideo"
            })
//2. 初始化 MultiModalDialog 实例，选择 RTC 链路 chainMode: ChainMode.RTC
self.conversation = MultiModalDialog(url: self.HOST, chainMode: self.chain,  workSpaceId:self.WORKSPACE_ID ,
                                             appId: self.APP_ID, mode: mode)

//3. 在建联后发送voicechat_video_channel 请求
private func createVideoChatParams() -> [String: Any]{
        var video:[String: Any] = [
            "action":"connect",
            "type" : "voicechat_video_channel"
        ]
        var videos = [video]
        
        var updateParam = MultiModalRequestParam{ multiBuilder in
            multiBuilder.bizParams = MultiModalRequestParam.BizParams(builder: {
                bizBuilder in
                bizBuilder.videos = videos
            })
        }
        return updateParam.parameters
}

//4. 开始音视频交互。处理交互流程。注意 demo 中有关ChainMode.RTC 类型的特殊处理。
//完整代码请参考示例代码。
```

## **使用图片序列实现视频通话**

接入方法参见[三方RTC接入视频通话](https://help.aliyun.com/zh/model-studio/third-party-rtc-invoke-liveai)。
