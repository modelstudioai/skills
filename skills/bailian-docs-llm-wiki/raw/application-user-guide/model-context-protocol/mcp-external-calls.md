# 外部调用

阿里云百炼提供了全周期 MCP 服务，既支持在平台内部（如智能体、工作流）进行配置，也支持通过外部调用集成至第三方应用或个人项目。针对外部调用场景，可以选择以下两种方式：

-   集成至第三方应用：支持一键自动配置到第三方应用，快速实现外部调用。
    
-   集成至个人项目：通过 MCP SDK 调用，实现灵活编码和深度定制。
    

## 效果展示

在 Cherry Studio 中调用阿里云百炼提供的 Amap Maps MCP 服务，搭建一个路线规划智能体应用。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9558605571/p996589.png)

## 前提条件

### 1\. 开通阿里云百炼

1.  **注册账号**：若无阿里云账号，需首先[注册](https://account.aliyun.com/register/qr_register.htm)。
    
    > 如遇问题，请参见[注册阿里云账号](https://help.aliyun.com/zh/account/step-1-register-an-alibaba-cloud-account)。
    
2.  **开通阿里云百炼：**使用**阿里云主账号**前往[阿里云百炼大模型服务平台](https://bailian.console.aliyun.com/?tab=model#/model-market)，阅读并同意协议后，将自动开通阿里云百炼，如果未弹出服务协议，则表示您已经开通。
    
    > 如果开通服务时提示"您尚未进行实名认证"，请先进行[实名认证](https://help.aliyun.com/zh/account/verify-your-identity-individual-account)。
    

> 首次开通百炼后，您可领取新人免费额度（有效期：百炼开通后90天内），用于模型推理服务。免费额度领取方法和详情，请查看[新人免费额度](https://help.aliyun.com/zh/model-studio/new-free-quota)页面。

**说明**

超出额度或期限将产生费用，开启[消费限额](https://help.aliyun.com/zh/model-studio/new-free-quota#d1cb80ac11i92)功能将避免此情况下产生费用，具体费用请以控制台的实际报价和最终账单为准。

### **2\. 获取百炼 API Key**

1.  前往[API Key（北京）](https://bailian.console.aliyun.com/?tab=model#/api-key)、[API Key（新加坡）](https://modelstudio.console.aliyun.com/?tab=model#/api-key)或[API Key（弗吉尼亚）](https://modelstudio.console.aliyun.com/us-east-1?tab=model#/api-key)页面，单击**创建API KEY**。
    
2.  在弹窗中配置以下信息，并单击**确定**：
    
    -   **归属账号**：建议选择主账号（**账号**列内容为纯数字账号ID）。
        
    -   **归属业务空间**：建议选择默认业务空间。
        
3.  点击API Key旁的![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8412544571/p994217.png)图标获取该API Key。
    
    > 主账号可以查看全部API Key，子账号仅能查看自己创建的API Key。
    
    ![2026-02-11\_11-56-27](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0009970771/p1054137.jpg)
    

## 开通 MCP 服务

**说明**

百炼 MCP 服务已从旧版 SSE 协议升级为新版 Streamable HTTP 协议。请根据您的情况选择对应的操作步骤：

## **首次开通（新用户）**

1.  前往[阿里云百炼 MCP 广场](https://bailian.console.aliyun.com/cn-beijing/?spm=5176.21213303.aillm.1.1a232f3dAFihmQ&tab=app&scm=20140722.S_%E7%99%BE%E7%82%BCprompt._.RL_%E7%99%BE%E7%82%BCprompt-LOC_aillm-OR_chat-V_3-RC_llm#/mcp-market)选择 MCP 服务。以 Amap Maps 服务为例，点击卡片。
    
    ![截屏2026-03-16 15](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9768463771/p1060094.png)
    
2.  点击**立即开通**，点击**确认开通**后即可开通 Amap Maps MCP 服务。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9558605571/p996657.png)
    
    **说明**
    
    阿里云百炼已部署云端的 Amap Maps MCP 服务，开通试用服务无需填写**AMAP\_MAPS\_API\_KEY**。如需商业化服务定制，也支持使用个人**AMAP\_MAPS\_API\_KEY**。
    
    如果涉及输入敏感信息，需通过创建 KMS 凭据进行加密。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9558605571/p995653.png)
    

## **升级协议（已开通用户）**

1.  前往[阿里云百炼 MCP 广场](https://bailian.console.aliyun.com/cn-beijing/?spm=5176.21213303.aillm.1.1a232f3dAFihmQ&tab=app&scm=20140722.S_%E7%99%BE%E7%82%BCprompt._.RL_%E7%99%BE%E7%82%BCprompt-LOC_aillm-OR_chat-V_3-RC_llm#/mcp-market)选择 MCP 服务。以 Amap Maps 服务为例，点击卡片。
    
    ![截屏2026-03-16 15](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9768463771/p1060094.png)
    
2.  单击右侧**取消开通**，再单击**立即开通**，**确认开通**后即可更新 Amap Maps MCP 服务。
    

## 外部调用 MCP 服务

### **集成至第三方应用**

阿里云百炼支持配置 MCP 服务至 Cherry Studio 和 Cursor，支持自动配置和手动配置。以 Amap Maps 服务为例。

## Cherry Studio

1.  安装 [Cherry Studio](https://www.cherry-ai.com/)。
    
2.  进入 [Amap Maps MCP](https://bailian.console.aliyun.com/?tab=mcp&scm=20140722.S_%E7%99%BE%E7%82%BCprompt._.RL_%E7%99%BE%E7%82%BCprompt-LOC_aillm-OR_chat-V_3-RC_llm#/mcp-market/detail/amap-maps) 服务界面，在**外部调用**界面中选择 **Cherry Studio**。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9768463771/p1060096.png)
    
3.  点击**一键配置至 Cherry Studio**，选择 API Key，点击**确定**。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9558605571/p996572.png)可以在弹出的 Cherry Studio 界面中看到所配置的 MCP 服务的详细信息。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9558605571/p996573.png)
    
4.  也可以手动配置 MCP 服务。点击右上角![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9558605571/p996575.png)，在弹出界面选择 API Key 并复制配置文件。在 Cherry Studio 的 **MCP 设置**页面点击**添加服务器**\>**从JSON导入**，粘贴配置信息，点击**确定**。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9558605571/p996576.png)
    
5.  在 Cherry Studio中使用 MCP 服务。新建话题，在下方点击![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9558605571/p995669.png)，选择**AliyunBailianMCP\_amap-maps** 服务。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9558605571/p996571.png)
    
6.  在对话框中输入`现在出发，从杭州萧山国际机场到杭州西湖景区。请你提供三种公共交通出行方案`，可以看到大模型成功调用了 MCP 工具来规划路线。
    
    > 若模型无法调用 MCP，请参考[常见问题](#a7dddab168yub)。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9558605571/p996570.png)
    

## Cursor

1.  安装 [Cursor](https://cursor.com/)。
    
2.  进入 [Amap Maps MCP](https://bailian.console.aliyun.com/?tab=mcp&scm=20140722.S_%E7%99%BE%E7%82%BCprompt._.RL_%E7%99%BE%E7%82%BCprompt-LOC_aillm-OR_chat-V_3-RC_llm#/mcp-market/detail/amap-maps) 服务界面，在**外部调用**界面中选择 **Cursor**。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9768463771/p1060096.png)
    
3.  点击**一键配置至Cursor**，选择 API Key，点击**确定**。在弹出的 Cursor 界面中点击 **Install**。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9558605571/p996580.png)
    
    头像右下角状态显示为绿色即为安装成功。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9558605571/p996581.png)
    

### 通过 SDK 进行开发集成

通过 MCP SDK 调用阿里云百炼 MCP 服务，编码更加灵活。

以下是一个基于 [Qwen Agent](https://github.com/QwenLM/Qwen-Agent) 框架、调用 Amap Maps MCP 服务的智能体应用实例，支持查询杭州市天气。

1.  安装 Qwen Agent 框架。
    
    ```
    pip install -U "qwen-agent[gui,rag,code_interpreter,mcp]"
    ```
    
2.  [配置百炼 API Key 到环境变量](https://help.aliyun.com/zh/model-studio/first-api-call-to-qwen#688de734136xo) 。
    
3.  新建文件`hangzhou_weather.py`，代码示例如下：
    
    ## Python
    
    ```
    # -*- coding: utf-8 -*-
    # 使用amap-maps工具查询杭州天气
    
    import os
    from qwen_agent.agents import Assistant
    
    
    def query_hangzhou_weather():
        """查询杭州今日天气"""
        # 检查环境变量
        api_key = os.getenv('DASHSCOPE_API_KEY')
        if not api_key:
            print("错误：请设置环境变量 DASHSCOPE_API_KEY")
            print("例如：export DASHSCOPE_API_KEY=your_api_key")
            return
        
        llm_cfg = {'model': 'qwen-max'}
        system = (
            '你是一个天气查询智能体。你将调用名为 amap-maps 的 MCP 服务来查询天气信息。'
            '请优先调用工具获取结构化的天气数据，并对天气情况做简明解释。'
        )
        
        # 配置MCP工具 (Streamable HTTP 协议)
        tools = [{
            "mcpServers": {
                "amap-maps": {
                    "type": "streamable-http",
                    "url": "https://dashscope.aliyuncs.com/api/v1/mcps/amap-maps/mcp",
                    "headers": {
                        "Authorization": f"Bearer {api_key}"
                    }
                }
            }
        }]
        
        # 创建智能体
        bot = Assistant(
            llm=llm_cfg,
            name='天气查询智能体',
            description='天气信息查询',
            system_message=system,
            function_list=tools,
        )
    
        # 查询杭州天气
        messages = []
        query = "今天是几号？查询杭州今日的天气情况"
        messages.append({'role': 'user', 'content': query})
    
        print("正在查询杭州今日天气...")
        print("=" * 50)
        
        # 执行查询并收集所有响应
        all_responses = []
        for response in bot.run(messages):
            all_responses.append(response)
        
        # 提取最终的assistant回复内容
        final_content = ""
        if all_responses:
            last_response = all_responses[-1]
            if isinstance(last_response, list):
                for item in last_response:
                    if isinstance(item, dict) and item.get('role') == 'assistant' and 'content' in item:
                        final_content = item['content']
            elif isinstance(last_response, dict) and 'content' in last_response:
                final_content = last_response['content']
        
        # 输出最终结果
        if final_content:
            print(final_content)
        else:
            print("未能获取到天气信息")
    
    
    if __name__ == '__main__':
        query_hangzhou_weather()
    ```
    
4.  运行代码，结果如下：
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9768463771/p1060102.png)
    
    > 运行代码时，若提示`npx`不是内部或外部命令，请先安装`[Node.js](https://nodejs.org/zh-cn)`。
    

## 常见问题

### 无法连接 MCP 服务怎么办？

1.  **未开通或者未升级 MCP 服务**：请确认已在百炼 MCP 广场开通或升级 MCP 服务，详情参见[开通 MCP 服务](#1387ea635cibi)。
    
2.  **API Key 错误**：请确认使用了有效的百炼通用 API Key。
    
3.  **额度用尽**：部分 MCP （如联网搜索）存在每月额度限制，额度用尽后自动停止。
    

其他报错及常见问题请参考[常见问题](https://help.aliyun.com/zh/model-studio/mcp-faq)。

### **模型正常对话且 MCP 无报错，但无法成功地调用 MCP 怎么办？**

大模型需要明确的指令才能准确地调用 MCP 服务。请在提示词中明确工具名称和工具能力。示例：调用阿里云百炼 Amap Maps MCP 服务，规划从杭州到上海的自驾路线。
