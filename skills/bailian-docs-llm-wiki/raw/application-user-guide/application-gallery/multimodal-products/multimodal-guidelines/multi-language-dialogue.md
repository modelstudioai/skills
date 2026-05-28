# 多语言对话

提供欧美、亚洲热门国家的单一语言对话能力，语种、功能持续扩展中。

## **语言列表**

**语种**

**应用类型**

**语音识别**

**语音合成**

**大模型对话 - 细节功能**

**中文（普通话）**

多模态应用

语音应用

支持

支持

-   全部功能可用
    

**英语**

支持

支持

-   闲聊和知识问答
    
-   联网搜索
    
-   语义拒识和判停能力
    
-   对话承接语
    
-   知识库
    
-   指令：系统指令、自定义指令
    
-   插件：自定义插件
    
-   MCP服务：自定义mcp
    
-   Agent：百炼“我的应用”、三方应用、视频通话&拍照问答&拍照翻译
    

**法语、德语、西班牙、意大利、俄语、葡萄牙、韩语、日语、泰语、印尼语、马来语**

多模态应用

支持

（但不支持热词）

支持

-   闲聊和知识问答（暂不支持联网搜索）
    
-   指令：系统指令、自定义指令
    
-   插件：自定义插件
    
-   MCP服务：自定义mcp
    
-   Agent：百炼“我的应用”、三方应用、视频通话&拍照问答&拍照翻译
    

**粤语**

支持

（但不支持热词）

支持

**越南语、菲律宾语**

支持

（但不支持热词）

当前需接入三方模型能力

**阿拉伯语、印地语、土耳其语、乌克兰语、捷克语、丹麦语、芬兰语、冰岛语、挪威语、波兰语、荷兰语、瑞典语**

支持

（但不支持热词）

当前需接入三方模型能力

## **功能说明**

-   **仅支持单一语种对话，不支持多语种混合对话（中英混说除外）。**
    
-   如需在同一台硬件设备中提供多种语言，需要每个语言单独创建一个应用，通过系统设置的方式切换应用ID，为终端用户提供对应语言的对话能力。
    
-   上述语言的计费逻辑与中文保持一致。
    

## **ASR和TTS模型挑选建议**

-   不同语言可使用、推荐使用的语音模型如下表：
    
    -   表格为空，代表当前语种无语音模型可支持，需[接入三方模型能力](https://help.aliyun.com/zh/model-studio/third-party-voice-integration)。
        

**语种**

**推荐ASR模型**

**（效果优先）**

**可用ASR模型**

**推荐TTS模型 & 音色**

**（效果优先）**

**可用TTS模型**

**中文**

-   Fun-ASR实时语音识别
    
-   千问3-ASR-Flash-Realtime
    

-   Fun-ASR实时语音识别
    
-   千问3-ASR-Flash-Realtime
    
-   Paraformer语音识别
    
-   多模态交互轻量版语音识别
    

-   CosyVoice-v3-Flash大模型 龙安欢
    

-   CosyVoice-v3-Flash大模型
    
-   千问3-TTS-Flash-Realtime
    
-   CosyVoice-v3-Plus大模型
    
-   CosyVoice-v2大模型
    
-   Sambert语音合成模型
    
-   多模态交互轻量版语音合成
    

**英语**

-   Fun-ASR实时语音识别
    
-   千问3-ASR-Flash-Realtime
    

-   Fun-ASR实时语音识别
    
-   千问3-ASR-Flash-Realtime
    
-   Paraformer语音识别（含轻量版）
    

-   CosyVoice-v3-Flash大模型 龙安欢
    

-   CosyVoice-v3-Flash大模型
    
-   千问3-TTS-Flash-Realtime
    
-   CosyVoice-v3-Plus大模型
    
-   CosyVoice-v2大模型
    
-   Sambert语音合成模型
    
-   多模态交互轻量版语音合成
    

**日语**

-   Fun-ASR实时语音识别
    
-   千问3-ASR-Flash-Realtime
    

-   Fun-ASR实时语音识别
    
-   千问3-ASR-Flash-Realtime
    
-   Paraformer语音识别
    
-   多模态交互轻量版语音识别
    

-   千问3-TTS-Flash-Realtime 芊悦
    

-   千问3-TTS-Flash-Realtime
    
-   多模态交互轻量版语音合成
    

**韩语**

-   千问3-ASR-Flash-Realtime
    

-   千问3-ASR-Flash-Realtime
    
-   Paraformer语音识别
    
-   多模态交互轻量版语音识别
    

-   千问3-TTS-Flash-Realtime 芊悦
    

-   千问3-TTS-Flash-Realtime
    
-   多模态交互轻量版语音合成
    

**法语**

-   千问3-ASR-Flash-Realtime
    

-   千问3-ASR-Flash-Realtime
    
-   Paraformer语音识别
    
-   多模态交互轻量版语音识别
    

-   千问3-TTS-Flash-Realtime 芊悦
    

-   千问3-TTS-Flash-Realtime
    
-   Sambert语音合成模型
    

**德语**

-   千问3-ASR-Flash-Realtime
    

-   千问3-ASR-Flash-Realtime
    
-   Paraformer语音识别
    
-   多模态交互轻量版语音识别
    

-   千问3-TTS-Flash-Realtime 芊悦
    

-   千问3-TTS-Flash-Realtime
    
-   Sambert语音合成模型
    

**意大利**

-   千问3-ASR-Flash-Realtime
    

-   千问3-ASR-Flash-Realtime
    

-   千问3-TTS-Flash-Realtime 芊悦
    

-   千问3-TTS-Flash-Realtime
    
-   Sambert语音合成模型
    

**西班牙**

-   千问3-ASR-Flash-Realtime
    

-   千问3-ASR-Flash-Realtime
    

-   千问3-TTS-Flash-Realtime 芊悦
    

-   千问3-TTS-Flash-Realtime
    
-   Sambert语音合成模型
    

**葡萄牙**

-   千问3-ASR-Flash-Realtime
    

-   千问3-ASR-Flash-Realtime
    

-   千问3-TTS-Flash-Realtime 芊悦
    

-   千问3-TTS-Flash-Realtime
    

**俄语**

-   千问3-ASR-Flash-Realtime
    

-   千问3-ASR-Flash-Realtime
    
-   Paraformer语音识别
    
-   多模态交互轻量版语音识别
    

-   千问3-TTS-Flash-Realtime 芊悦
    

-   千问3-TTS-Flash-Realtime
    

**泰语**

-   千问3-ASR-Flash-Realtime
    

-   千问3-ASR-Flash-Realtime
    

-   Sambert语音合成模型 Waan
    

-   Sambert语音合成模型
    

**印尼语**

-   千问3-ASR-Flash-Realtime
    

-   千问3-ASR-Flash-Realtime
    

-   Sambert语音合成模型 Indah
    

-   Sambert语音合成模型
    

**菲律宾语**

-   千问3-ASR-Flash-Realtime
    

-   千问3-ASR-Flash-Realtime
    

**粤语**

-   Fun-ASR实时语音识别
    
-   千问3-ASR-Flash-Realtime
    

-   Fun-ASR实时语音识别
    
-   千问3-ASR-Flash-Realtime
    

-   千问3-TTS-Flash-Realtime 芊悦
    

-   千问3-TTS-Flash-Realtime
    
-   CosyVoice-v3-Flash大模型
    
-   多模态交互轻量版语音合成
    

**阿拉伯语**

-   千问3-ASR-Flash-Realtime
    

-   千问3-ASR-Flash-Realtime
    

-   千问3-TTS-Flash-Realtime
    

**印地语**

-   千问3-ASR-Flash-Realtime
    

-   千问3-ASR-Flash-Realtime
    

**土耳其语**

-   千问3-ASR-Flash-Realtime
    

-   千问3-ASR-Flash-Realtime
    

-   千问3-TTS-Flash-Realtime
    

**乌克兰语**

-   千问3-ASR-Flash-Realtime
    

-   千问3-ASR-Flash-Realtime
    

**捷克语**

-   千问3-ASR-Flash-Realtime
    

-   千问3-ASR-Flash-Realtime
    

**丹麦语**

-   千问3-ASR-Flash-Realtime
    

-   千问3-ASR-Flash-Realtime
    

**芬兰语**

-   千问3-ASR-Flash-Realtime
    

-   千问3-ASR-Flash-Realtime
    

**冰岛语**

-   千问3-ASR-Flash-Realtime
    

-   千问3-ASR-Flash-Realtime
    

**挪威语**

-   千问3-ASR-Flash-Realtime
    

-   千问3-ASR-Flash-Realtime
    

**波兰语**

-   千问3-ASR-Flash-Realtime
    

-   千问3-ASR-Flash-Realtime
    

**荷兰语**

当前需接入三方模型能力

当前需接入三方模型能力

**瑞典语**

-   千问3-ASR-Flash-Realtime
    

-   千问3-ASR-Flash-Realtime
    

## **配置方式**

1.  在控制台点击创建「多模态应用」。
    

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1476777671/p1041959.png)

2.  选择所需语种和品类，创建应用。系统会提供最合适的模型、提示词和功能组合。
    

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1476777671/p1041957.png)

3.  根据业务场景调整提示词等内容，当前语种不可用的功能会被隐藏。
    

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1476777671/p1041956.png)

4.  点击「立即运行」，在右侧选择合适的音色。
    

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1476777671/p1041958.png)

5.  在右侧进行对话体验，以及后续的发布、开发接入和购买等流程。
