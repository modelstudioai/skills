# 官方 MCP 服务

阿里云百炼的官方 MCP 服务开通后即可使用。百炼官方 MCP 服务既支持在平台内部（如智能体、工作流）直接集成，也支持通过外部调用集成至第三方应用或项目中。

## **开通**云部署 **MCP 服务**

**说明**

阿里云百炼采取了安全策略来保障云部署 MCP Server 的数据安全。对于敏感数据，云部署 MCP Server 会在创建时使用 KMS 进行加密管理。

**说明**

目前 Amap Maps MCP 服务限时免费使用。

开通后，即可使用云部署 MCP 服务。以“开通 **Amap Maps** MCP 服务”为例：

1.  前往[阿里云百炼 MCP 页面](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)，点击 **Amap Maps** 卡片。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1522646571/p1001809.png)
    
2.  点击**立即开通**，点击**确认开通**，即可开通 Amap Maps MCP 服务。
    
    > 阿里云百炼已部署云端的 Amap Maps MCP 服务，开通试用服务无需填写**AMAP\_MAPS\_API\_KEY**。如需商业化服务定制，也支持使用个人**AMAP\_MAPS\_API\_KEY**。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1522646571/p1001810.png)
    
    对于涉及敏感信息的 MCP 服务，需通过创建 KMS 凭据加密这些信息。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9796380571/p966038.png)
    

## **在智能体或工作流中配置 MCP 服务**

### **智能体应用**

在智能体应用中，大模型会根据输入对话来判断是否调用 MCP 服务。

1.  #### **创建智能体**
    
    前往阿里云百炼[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，点击**创建应用**，选择**智能体应用** > **立即创建**。
    
2.  #### **添加 MCP 服务**
    
    智能体在回答时可以调用多个 MCP 服务，可同时添加最多 5 个 **MCP 服务**。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5124314471/p939247.png)
    
3.  #### **测试 MCP 服务**
    
    智能体可以自动调用合适的 MCP 服务来解决问题。以下是几个参考使用场景：
    
    ## 路程规划（单 MCP 服务）
    
    请确认已添加 Amap Maps MCP 服务，帮助智能体获取地理信息。
    
    在右侧对话窗格中发送一条测试消息：“`现在出发，从杭州萧山国际机场到杭州西湖景区。请你提供三种公共交通出行方案`”。智能体将多次调用 MCP 服务，完成路径规划和时间估算。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4527964471/p942298.png)
    
    ## 逐步思考（单 MCP 服务）
    
    请确认已添加 Sequential Thinking MCP 服务，帮助智能体逐步思考逻辑推理问题。
    
    在右侧对话窗格中发送一条测试消息：“`请你解答这道“鸡兔同笼”问题：假设共有头12个，脚32只，请问鸡兔各有几何？`”。智能体将多次调用 MCP 服务，完成逻辑推理任务。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4527964471/p942281.png)
    
    ## 气温趋势（多 MCP 服务）
    
    请确认已添加 Amap Maps 和 QuickChart MCP 服务，帮助智能体获取实时天气预报，并用折线图展示气温变化趋势。
    
    在右侧对话窗格中发送一条测试消息：“`请使用折线图绘制杭州未来几天的气温走势`”。智能体将多次调用 MCP 服务，完成天气查询和图表绘制任务。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4527964471/p942303.png)
    

### **工作流应用**

MCP 服务可能有多个工具，但在工作流应用中，每个 MCP 节点只能使用一个工具，因此需要手动指定 MCP 节点的输入参数，再传递输出参数到下一个节点。

使用Amap Maps MCP 服务的 maps\_weather 工具，快速构建一个城市天气查询工作流。

> 在只使用 maps\_weather 工具时，工作流无法回答与天气查询无关的问题。

1.  #### **创建工作流**
    
    前往阿里云百炼[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，点击**创建应用**，选择**工作流应用** > **立即创建**。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1614144471/p941093.png)
    
2.  #### **设置开始节点**
    
    删除开始节点的两个默认参数。
    
    > 在这个案例中，只需使用默认的系统变量 query，故删去这两个参数。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7991344471/p941616.png)
    
3.  #### **提取城市名称**
    
    为了将输入对话的自然语言解析为 MCP 节点需要的城市名称，从左侧工具栏中拖入一个大模型节点，命名为“信息提取”。请将此节点连接到开始节点，并按照指引填写参数。
    
    > 其他参数保持默认即可。
    
    **参数名**
    
    **参数值**
    
    **模型配置**
    
    通义千问-Max
    
    **System Prompt**
    
    你是一个信息提取专家，你的任务是帮助“查询天气工具”解析正确的输入参数。
    
    \---
    
    “查询天气工具”的描述如下：
    
    名称：maps\_weather
    
    描述：根据城市名称或者标准adcode查询指定城市的天气
    
    输入参数：city \[string\] 城市名称或者adcode
    
    输出参数：result \[string\] 城市的天气预报
    
    \---
    
    你的输出是“查询天气工具”的输入，你只需要输出城市的名称即可。
    
    注意：你一次只能输出一个城市。
    
    **User Prompt**
    
    通过键入"`/`"来呼出变量菜单，选中“**系统变量** > **query**。
    
    **说明**
    
    使用 MCP 节点前，通常需要将输入对话的自然语言转换为 MCP 节点的输入参数。因此，需要在 System Prompt 中描述 MCP 服务的功能和输入输出信息，以限定大模型的输出格式。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4527964471/p942187.png)
    
4.  #### **查询天气信息**
    
    > 使用高德 MCP 服务提供的天气查询工具，接收一个城市名，返回该城市的天气信息。
    
    从左侧工具栏中拖入一个 MCP 节点，按照图示选择 maps\_weather 工具，确认节点配置。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5124314471/p939250.png)
    
    将 MCP 节点命名为“天气查询工具”，然后将此节点连接到“信息提取”节点。
    
    **说明**
    
    点击节点左上角的箭头按钮，即可展开或收起节点配置。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4527964471/p942188.png)
    
    点击 MCP 节点内 maps\_weather 工具的配置按钮，修改输入为“引用：信息提取/result”。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4527964471/p942143.png)
    
5.  #### **总结天气信息**
    
    为了将 MCP 服务返回的结果整理成便于阅读的自然语言，从左侧工具栏中拖入一个大模型节点，命名为“信息总结”。请将此节点连接到“天气查询工具”节点，并按照指引填写参数。
    
    > 其他参数保持默认即可：
    
    **参数名**
    
    **参数值**
    
    **模型配置**
    
    通义千问-Max
    
    **System Prompt**
    
    你是一个信息处理助手，你的任务是将用户输入的信息整合为自然语言。
    
    **User Prompt**
    
    通过键入"`/`"来呼出变量菜单，选中“**天气查询工具** > **result**”
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4527964471/p942186.png)
    
6.  #### **输出查询结果**
    
    将此节点连接到“信息总结”节点，并按照指引填写参数，以获取最终的输出结果。
    
    **参数名**
    
    **参数值**
    
    **输入框**
    
    键入"`/`"来呼出变量菜单，选中“**信息总结** > **result**
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4527964471/p942204.png)
    
7.  #### **测试查询效果**
    
    点击右上角“测试”按钮，输入“`查询杭州天气`”，查看工作流的输出结果。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7991344471/p941629.png)
    

## 外部调用 MCP 服务

阿里云百炼支持通过外部调用将 MCP 服务集成至第三方应用或项目中，详情参考[外部调用](https://help.aliyun.com/zh/model-studio/mcp-external-calls)。
