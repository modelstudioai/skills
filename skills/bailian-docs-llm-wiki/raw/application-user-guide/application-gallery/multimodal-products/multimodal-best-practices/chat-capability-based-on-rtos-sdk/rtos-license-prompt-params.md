# RTOS SDK (License模式) 提示词变量设置

本文介绍如何基于RTOS SDK (License模式) 实现自定义提示词变量设置。

## 1\. 开发准备

### 1.1. 前置说明

-   本文依赖前置文档 “[基于RTOS SDK (License模式) 实现聊天能力](raw/application-user-guide/application-gallery/multimodal-products/multimodal-best-practices/chat-capability-based-on-rtos-sdk.md)” ，请在阅读本文前先完成相关内容的学习与环境准备。
-   默认开发者已完成SDK接入，并可正常运行语音交互流程。

### 1.2. 配置提示词

-   在**百炼控制台**创建应用
    
-   修改`提示词`新增`自定义变量`
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4791619671/p1044760.png)
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4791619671/p1044761.png)
    

## 2\. 端侧功能开发

### 2.1. 示例代码

```
int main(void)
{
    c_mmi_prompt_pram_t prompt[] = {
        {"name", "阿云"},
        {"skill", "唱歌"},
    };

    // 初始化SDK
    c_mmi_sdk_init();

    // 配置提示词变量
    c_mmi_data_set_prompt_param(prompt, ARRAY_SIZE(prompt));

    return 0;
}
```

### 2.2. 关键日志

```
[UT][I][_gen_cmd_start]out [870][{"header":{"action":"run-task","streaming":"duplex","task_id":"Task Id"},"payload":{"task_group":"aigc","task":"multimodal-generation","function":"generation","model":"multimodal-dialog","input":{"workspace_id":"Workspace Id","app_id":"App Id","directive":"Start"},"parameters":{"upstream":{"sample_rate":16000,"type":"AudioAndVideo","mode":"tap2talk","audio_format":"pcm","enable_server_vad_start":false},"downstream":{"voice":"longanhuan","sample_rate":16000,"audio_format":"mp3","volume":50,"speech_rate":100,"pitch_rate":100,"intermediate_text":"transcript,dialog","transmit_rate_limit":16000},"client_info":{"user_id":"test_1","device":{"uuid":"test_1"}},"biz_params":{"user_prompt_params":{"name":"阿云","skill":"唱歌"},"user_defined_params":{"children_story":{"speaker_1_voice":"longxiaochun_v2"}}}}}}]
```

如上述日志，可以看到在建立连接时的cmd\_start中包含我们自定义的提示词变量。

## 3\. 典型应用场景介绍

-   通过自定义提示词变量，可以实现在不切换App Id的情况下，进行角色的切换，比如可以定义角色姓名、年龄、性别、爱好等属性。
-   也可以将整个提示词作为一个变量，通过设备端传递参数，重写整个提示词。
