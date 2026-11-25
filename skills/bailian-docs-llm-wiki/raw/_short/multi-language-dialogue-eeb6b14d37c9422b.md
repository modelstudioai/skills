# 多语言对话

提供欧美、亚洲热门国家的单一语言对话能力，语种、功能持续扩展中。

<a id="语言列表"></a>

<a id="5085c494472it"></a>

## 语言列表

<table><tbody><tr><td><p><strong>语种</strong></p></td><td><p><strong>应用类型</strong></p></td><td><p><strong>语音识别</strong></p></td><td><p><strong>语音合成</strong></p></td><td><p><strong>大模型对话 - 细节功能</strong></p></td></tr><tr><td><p><strong>中文（普通话）</strong></p></td><td rowspan="2"><p>多模态应用</p><p>语音应用</p></td><td><p>支持</p></td><td><p>支持</p></td><td><ul><li><p>全部功能可用</p></li></ul></td></tr><tr><td><p><strong>英语</strong></p></td><td><p>支持</p></td><td><p>支持</p></td><td><ul><li><p>闲聊和知识问答</p></li><li><p>联网搜索</p></li><li><p>语义拒识和判停能力</p></li><li><p>对话承接语</p></li><li><p>知识库</p></li><li><p>指令：系统指令、自定义指令</p></li><li><p>插件：自定义插件</p></li><li><p>MCP服务：自定义mcp</p></li><li><p>Agent：百炼“我的应用”、三方应用、视频通话&amp;拍照问答&amp;拍照翻译</p></li></ul></td></tr><tr><td><p><strong>法语、德语、西班牙、意大利、俄语、葡萄牙、韩语、日语、泰语、印尼语、马来语</strong></p></td><td rowspan="4"><p>多模态应用</p></td><td><p>支持</p><p>（但不支持热词）</p></td><td><p>支持</p></td><td rowspan="4"><ul><li><p>闲聊和知识问答（暂不支持联网搜索）</p></li><li><p>指令：系统指令、自定义指令</p></li><li><p>插件：自定义插件</p></li><li><p>MCP服务：自定义mcp</p></li><li><p>Agent：百炼“我的应用”、三方应用、视频通话&amp;拍照问答&amp;拍照翻译</p></li></ul></td></tr><tr><td><p><strong>粤语</strong></p></td><td><p>支持</p><p>（但不支持热词）</p></td><td><p>支持</p></td></tr><tr><td><p><strong>越南语、菲律宾语</strong></p></td><td><p>支持</p><p>（但不支持热词）</p></td><td><p>当前需接入三方模型能力</p></td></tr><tr><td><p><strong>阿拉伯语、印地语、土耳其语、乌克兰语、捷克语、丹麦语、芬兰语、冰岛语、挪威语、波兰语、荷兰语、瑞典语</strong></p></td><td><p>支持</p><p>（但不支持热词）</p></td><td><p>当前需接入三方模型能力</p></td></tr></tbody></table>

<a id="功能说明"></a>

<a id="bf113cbd4djdr"></a>

## 功能说明

-   **仅支持单一语种对话，不支持多语种混合对话（中英混说除外）。**
-   如需在同一台硬件设备中提供多种语言，需要每个语言单独创建一个应用，通过系统设置的方式切换应用ID，为终端用户提供对应语言的对话能力。
-   上述语言的计费逻辑与中文保持一致。

<a id="asr和tts模型挑选建议"></a>

<a id="8791b53260jeq"></a>

## ASR和TTS模型挑选建议

-   不同语言可使用、推荐使用的语音模型如下表：
    
    -   表格为空，代表当前语种无语音模型可支持，需[接入三方模型能力](third-party-voice-integration-8ea83955d322380a.md)。

<table><tbody><tr><td><p><strong>语种</strong></p></td><td><p><strong>推荐ASR模型</strong></p><p><strong>（效果优先）</strong></p></td><td><p><strong>可用ASR模型</strong></p></td><td><p><strong>推荐TTS模型 &amp; 音色</strong></p><p><strong>（效果优先）</strong></p></td><td><p><strong>可用TTS模型</strong></p></td></tr><tr><td><p><strong>中文</strong></p></td><td><ul><li><p>Fun-ASR实时语音识别</p></li><li><p>千问3-ASR-Flash-Realtime</p></li></ul></td><td><ul><li><p>Fun-ASR实时语音识别</p></li><li><p>千问3-ASR-Flash-Realtime</p></li><li><p>Paraformer语音识别</p></li><li><p>多模态交互轻量版语音识别</p></li></ul></td><td><ul><li><p>CosyVoice-v3-Flash大模型 龙安欢</p></li></ul></td><td><ul><li><p>CosyVoice-v3-Flash大模型</p></li><li><p>千问3-TTS-Flash-Realtime</p></li><li><p>CosyVoice-v3-Plus大模型</p></li><li><p>CosyVoice-v2大模型</p></li><li><p>Sambert语音合成模型</p></li><li><p>多模态交互轻量版语音合成</p></li></ul></td></tr><tr><td><p><strong>英语</strong></p></td><td><ul><li><p>Fun-ASR实时语音识别</p></li><li><p>千问3-ASR-Flash-Realtime</p></li></ul></td><td><ul><li><p>Fun-ASR实时语音识别</p></li><li><p>千问3-ASR-Flash-Realtime</p></li><li><p>Paraformer语音识别（含轻量版）</p></li></ul></td><td><ul><li><p>CosyVoice-v3-Flash大模型 龙安欢</p></li></ul></td><td><ul><li><p>CosyVoice-v3-Flash大模型</p></li><li><p>千问3-TTS-Flash-Realtime</p></li><li><p>CosyVoice-v3-Plus大模型</p></li><li><p>CosyVoice-v2大模型</p></li><li><p>Sambert语音合成模型</p></li><li><p>多模态交互轻量版语音合成</p></li></ul></td></tr><tr><td><p><strong>日语</strong></p></td><td><ul><li><p>Fun-ASR实时语音识别</p></li><li><p>千问3-ASR-Flash-Realtime</p></li></ul></td><td><ul><li><p>Fun-ASR实时语音识别</p></li><li><p>千问3-ASR-Flash-Realtime</p></li><li><p>Paraformer语音识别</p></li><li><p>多模态交互轻量版语音识别</p></li></ul></td><td><ul><li><p>千问3-TTS-Flash-Realtime 芊悦</p></li></ul></td><td><ul><li><p>千问3-TTS-Flash-Realtime</p></li><li><p>多模态交互轻量版语音合成</p></li></ul></td></tr><tr><td><p><strong>韩语</strong></p></td><td><ul><li><p>千问3-ASR-Flash-Realtime</p></li></ul></td><td><ul><li><p>千问3-ASR-Flash-Realtime</p></li><li><p>Paraformer语音识别</p></li><li><p>多模态交互轻量版语音识别</p></li></ul></td><td><ul><li><p>千问3-TTS-Flash-Realtime 芊悦</p></li></ul></td><td><ul><li><p>千问3-TTS-Flash-Realtime</p></li><li><p>多模态交互轻量版语音合成</p></li></ul></td></tr><tr><td><p><strong>法语</strong></p></td><td><ul><li><p>千问3-ASR-Flash-Realtime</p></li></ul></td><td><ul><li><p>千问3-ASR-Flash-Realtime</p></li><li><p>Paraformer语音识别</p></li><li><p>多模态交互轻量版语音识别</p></li></ul></td><td><ul><li><p>千问3-TTS-Flash-Realtime 芊悦</p></li></ul></td><td><ul><li><p>千问3-TTS-Flash-Realtime</p></li><li><p>Sambert语音合成模型</p></li></ul></td></tr><tr><td><p><strong>德语</strong></p></td><td><ul><li><p>千问3-ASR-Flash-Realtime</p></li></ul></td><td><ul><li><p>千问3-ASR-Flash-Realtime</p></li><li><p>Paraformer语音识别</p></li><li><p>多模态交互轻量版语音识别</p></li></ul></td><td><ul><li><p>千问3-TTS-Flash-Realtime 芊悦</p></li></ul></td><td><ul><li><p>千问3-TTS-Flash-Realtime</p></li><li><p>Sambert语音合成模型</p></li></ul></td></tr><tr><td><p><strong>意大利</strong></p></td><td><ul><li><p>千问3-ASR-Flash-Realtime</p></li></ul></td><td><ul><li><p>千问3-ASR-Flash-Realtime</p></li></ul></td><td><ul><li><p>千问3-TTS-Flash-Realtime 芊悦</p></li></ul></td><td><ul><li><p>千问3-TTS-Flash-Realtime</p></li><li><p>Sambert语音合成模型</p></li></ul></td></tr><tr><td><p><strong>西班牙</strong></p></td><td><ul><li><p>千问3-ASR-Flash-Realtime</p></li></ul></td><td><ul><li><p>千问3-ASR-Flash-Realtime</p></li></ul></td><td><ul><li><p>千问3-TTS-Flash-Realtime 芊悦</p></li></ul></td><td><ul><li><p>千问3-TTS-Flash-Realtime</p></li><li><p>Sambert语音合成模型</p></li></ul></td></tr><tr><td><p><strong>葡萄牙</strong></p></td><td><ul><li><p>千问3-ASR-Flash-Realtime</p></li></ul></td><td><ul><li><p>千问3-ASR-Flash-Realtime</p></li></ul></td><td><ul><li><p>千问3-TTS-Flash-Realtime 芊悦</p></li></ul></td><td><ul><li><p>千问3-TTS-Flash-Realtime</p></li></ul></td></tr><tr><td><p><strong>俄语</strong></p></td><td><ul><li><p>千问3-ASR-Flash-Realtime</p></li></ul></td><td><ul><li><p>千问3-ASR-Flash-Realtime</p></li><li><p>Paraformer语音识别</p></li><li><p>多模态交互轻量版语音识别</p></li></ul></td><td><ul><li><p>千问3-TTS-Flash-Realtime 芊悦</p></li></ul></td><td><ul><li><p>千问3-TTS-Flash-Realtime</p></li></ul></td></tr><tr><td><p><strong>泰语</strong></p></td><td><ul><li><p>千问3-ASR-Flash-Realtime</p></li></ul></td><td><ul><li><p>千问3-ASR-Flash-Realtime</p></li></ul></td><td><ul><li><p>Sambert语音合成模型 Waan</p></li></ul></td><td><ul><li><p>Sambert语音合成模型</p></li></ul></td></tr><tr><td><p><strong>印尼语</strong></p></td><td><ul><li><p>千问3-ASR-Flash-Realtime</p></li></ul></td><td><ul><li><p>千问3-ASR-Flash-Realtime</p></li></ul></td><td><ul><li><p>Sambert语音合成模型 Indah</p></li></ul></td><td><ul><li><p>Sambert语音合成模型</p></li></ul></td></tr><tr><td><p><strong>菲律宾语</strong></p></td><td><ul><li><p>千问3-ASR-Flash-Realtime</p></li></ul></td><td><ul><li><p>千问3-ASR-Flash-Realtime</p></li></ul></td><td></td><td></td></tr><tr><td><p><strong>粤语</strong></p></td><td><ul><li><p>Fun-ASR实时语音识别</p></li><li><p>千问3-ASR-Flash-Realtime</p></li></ul></td><td><ul><li><p>Fun-ASR实时语音识别</p></li><li><p>千问3-ASR-Flash-Realtime</p></li></ul></td><td><ul><li><p>千问3-TTS-Flash-Realtime 芊悦</p></li></ul></td><td><ul><li><p>千问3-TTS-Flash-Realtime</p></li><li><p>CosyVoice-v3-Flash大模型</p></li><li><p>多模态交互轻量版语音合成</p></li></ul></td></tr><tr><td><p><strong>阿拉伯语</strong></p></td><td><ul><li><p>千问3-ASR-Flash-Realtime</p></li></ul></td><td><ul><li><p>千问3-ASR-Flash-Realtime</p></li></ul></td><td></td><td></td></tr><tr><td><p><strong>印地语</strong></p></td><td><ul><li><p>千问3-ASR-Flash-Realtime</p></li></ul></td><td><ul><li><p>千问3-ASR-Flash-Realtime</p></li></ul></td><td></td><td></td></tr><tr><td><p><strong>土耳其语</strong></p></td><td><ul><li><p>千问3-ASR-Flash-Realtime</p></li></ul></td><td><ul><li><p>千问3-ASR-Flash-Realtime</p></li></ul></td><td></td><td></td></tr><tr><td><p><strong>乌克兰语</strong></p></td><td><ul><li><p>千问3-ASR-Flash-Realtime</p></li></ul></td><td><ul><li><p>千问3-ASR-Flash-Realtime</p></li></ul></td><td></td><td></td></tr><tr><td><p><strong>捷克语</strong></p></td><td><ul><li><p>千问3-ASR-Flash-Realtime</p></li></ul></td><td><ul><li><p>千问3-ASR-Flash-Realtime</p></li></ul></td><td></td><td></td></tr><tr><td><p><strong>丹麦语</strong></p></td><td><ul><li><p>千问3-ASR-Flash-Realtime</p></li></ul></td><td><ul><li><p>千问3-ASR-Flash-Realtime</p></li></ul></td><td></td><td></td></tr><tr><td><p><strong>芬兰语</strong></p></td><td><ul><li><p>千问3-ASR-Flash-Realtime</p></li></ul></td><td><ul><li><p>千问3-ASR-Flash-Realtime</p></li></ul></td><td></td><td></td></tr><tr><td><p><strong>冰岛语</strong></p></td><td><ul><li><p>千问3-ASR-Flash-Realtime</p></li></ul></td><td><ul><li><p>千问3-ASR-Flash-Realtime</p></li></ul></td><td></td><td></td></tr><tr><td><p><strong>挪威语</strong></p></td><td><ul><li><p>千问3-ASR-Flash-Realtime</p></li></ul></td><td><ul><li><p>千问3-ASR-Flash-Realtime</p></li></ul></td><td></td><td></td></tr><tr><td><p><strong>波兰语</strong></p></td><td><ul><li><p>千问3-ASR-Flash-Realtime</p></li></ul></td><td><ul><li><p>千问3-ASR-Flash-Realtime</p></li></ul></td><td></td><td></td></tr><tr><td><p><strong>荷兰语</strong></p></td><td><p>当前需接入三方模型能力</p></td><td><p>当前需接入三方模型能力</p></td><td></td><td></td></tr><tr><td><p><strong>瑞典语</strong></p></td><td><ul><li><p>千问3-ASR-Flash-Realtime</p></li></ul></td><td><ul><li><p>千问3-ASR-Flash-Realtime</p></li></ul></td><td></td><td></td></tr></tbody></table>

<a id="配置方式"></a>

<a id="7dcf4e66a1yie"></a>

## 配置方式

1.  在控制台点击创建“多模态应用”。
    
2.  选择所需语种和品类，创建应用。系统会提供最合适的模型、提示词和功能组合。
    
    本示例中，**对话语言**选择**英语**，场景模板选择**AI眼镜**。
    
3.  根据业务场景调整提示词等内容，当前语种不可用的功能会被隐藏。
    
    在**语音交互**页签中，可配置**语音识别**（如 Fun-ASR 实时语音识别）和**语音合成**（如 CosyVoice-v3-Flash 大模型），以及**热词**、**即时纠错**和**对话打断**（任意语音打断/全双工 或 点击打断/半双工）等选项。在**理解和生成页签中，**可配置**意图识别**、**文本模型**（如Qwen3.6-Plus）、**承接语**、**知识库**、**联网搜索**、**长期记忆**等选项。页面还包含**技能**、**Agent**页签供后续配置。
    
4.  点击“立即运行”，在右侧运行面板的音色选择区域中，浏览可用音色列表并选择合适的音色。
    
5.  在右侧进行对话体验，以及后续的发布、开发接入和购买等流程。
