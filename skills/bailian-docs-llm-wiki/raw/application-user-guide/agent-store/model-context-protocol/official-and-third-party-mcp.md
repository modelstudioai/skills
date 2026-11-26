# 官方 MCP 服务

阿里云百炼的官方 MCP 服务开通后即可使用。阿里云百炼官方 MCP 服务既支持在平台内部（如智能体、工作流）直接集成，也支持通过外部调用集成至第三方应用或项目中。

阿里云百炼 MCP 广场的 MCP 服务分为两类：

-   **One Key MCP**：无需手动开通，使用阿里云百炼 API Key 直接鉴权，按量后付费。MCP 广场中标识为 One Key 的服务均属于此类。
-   **需开通的广场 MCP**：需在 MCP 广场手动开通后使用，部分服务可能需要填写第三方服务商的 API Key。

> **说明**
>
> 阿里云百炼采取了安全策略来保障云部署 MCP Server 的数据安全。对于敏感数据，云部署 MCP Server 会在创建时使用 KMS 进行加密管理。

<a id="one-key-mcp"></a>

<a id="h-onekey-mcp"></a>

## One Key MCP

One Key MCP 服务无需手动开通，首次调用自动生效。以使用 **联网搜索** MCP 服务为例：

1.  **进入 MCP 广场**：前往[阿里云百炼 MCP 页面](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)，浏览并选择带有 One Key 标识的 MCP 服务。
2.  **获取安装配置**：在服务详情页的**安装**区域，复制安装命令或 MCP 服务地址。使用阿里云百炼 API Key（DASHSCOPE\_API\_KEY）即可完成鉴权，无需为该服务单独申请密钥。
3.  **开始调用**：配置完成后即可调用。首次调用自动生效，无需手动开通。如服务提供免费额度，将自动激活。

<a id="需开通的广场-mcp"></a>

<a id="47ed5b5cff6hs"></a>

## 需开通的广场 MCP

对于未标识为 One Key 的广场 MCP 服务，需手动开通后使用。以开通 Amap Maps 高德地图 MCP 服务为例：

> **说明**
>
> 目前 Amap Maps MCP 服务限时免费使用。

1.  前往[阿里云百炼 MCP 页面](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)，点击 **Amap Maps** 卡片。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1522646571/p1001809.png)
2.  点击**立即开通**，点击**确认开通**，即可开通 Amap Maps MCP 服务。
    
    > 阿里云百炼已部署云端的 Amap Maps MCP 服务，开通试用服务无需填写**AMAP\_MAPS\_API\_KEY**。如需商业化服务定制，也支持使用个人**AMAP\_MAPS\_API\_KEY**。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1522646571/p1001810.png)

<a id="在智能体或工作流中配置-mcp-服务"></a>

<a id="8319d03864jym"></a>

## 在智能体或工作流中配置 MCP 服务

<a id="智能体应用"></a>

<a id="532b3d2bca34n"></a>

### 智能体应用

在智能体应用中，大模型会根据输入对话来判断是否调用 MCP 服务。

1.  **创建智能体**
    
    在[**创建智能体**](https://bailian.console.aliyun.com/cn-beijing/flow-agent/app-center/assistant?immediatelyCreate=true)表单中输入**应用名称**，然后单击**立即创建**。
    
2.  **添加 MCP 服务**
    
    智能体在回答时可以调用多个 MCP 服务，可同时添加最多 5 个 **MCP 服务**。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5124314471/p939247.png)
3.  **测试 MCP 服务**
    
    智能体可以自动调用合适的 MCP 服务来解决问题。以下是几个参考使用场景：
    
    <a id="sec-tabs"></a>
    
    <a id="路程规划-单-mcp-服务"></a>
    
    <a id="路程规划-单-mcp-服务-h4"></a>
    
    #### 路程规划（单 MCP 服务）
    
    请确认已添加 Amap Maps MCP 服务，帮助智能体获取地理信息。
    
    在右侧对话窗格中发送一条测试消息：“`现在出发，从杭州萧山国际机场到杭州西湖景区。请你提供三种公共交通出行方案`”。智能体将多次调用 MCP 服务，完成路径规划和时间估算。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4527964471/p942298.png)
    
    <a id="逐步思考-单-mcp-服务"></a>
    
    <a id="逐步思考-单-mcp-服务-h4"></a>
    
    #### 逐步思考（单 MCP 服务）
    
    请确认已添加 Sequential Thinking MCP 服务，帮助智能体逐步思考逻辑推理问题。
    
    在右侧对话窗格中发送一条测试消息：“`请你解答这道“鸡兔同笼”问题：假设共有头12个，脚32只，请问鸡兔各有几何？`”。智能体将多次调用 MCP 服务，完成逻辑推理任务。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4527964471/p942281.png)
    
    <a id="气温趋势-多-mcp-服务"></a>
    
    <a id="气温趋势-多-mcp-服务-h4"></a>
    
    #### 气温趋势（多 MCP 服务）
    
    请确认已添加 Amap Maps 和 QuickChart MCP 服务，帮助智能体获取实时天气预报，并用折线图展示气温变化趋势。
    
    在右侧对话窗格中发送一条测试消息：“`请使用折线图绘制杭州未来几天的气温走势`”。智能体将多次调用 MCP 服务，完成天气查询和图表绘制任务。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4527964471/p942303.png)
    

<a id="工作流应用"></a>

<a id="1349b5c4886jm"></a>

### 工作流应用

MCP 服务可能有多个工具，但在工作流应用中，每个 MCP 节点只能使用一个工具，因此需要手动指定 MCP 节点的输入参数，再传递输出参数到下一个节点。

使用Amap Maps MCP 服务的 maps\_weather工具，快速构建一个城市天气查询工作流。

> 在只使用 maps\_weather工具时，工作流无法回答与天气查询无关的问题。

1.  **创建工作流**
    
    在[**创建工作流**](https://bailian.console.aliyun.com/cn-beijing/flow-agent/app-center/workflow?immediatelyCreate=true)表单中输入**应用名称**，然后单击**立即创建**。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1614144471/p941093.png)
2.  **设置开始节点**
    
    删除开始节点的两个默认参数。
    
    > 在这个案例中，只需使用默认的系统变量 query，故删去这两个参数。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7991344471/p941616.png)
3.  **提取城市名称**
    
    为了将输入对话的自然语言解析为 MCP 节点需要的城市名称，从左侧工具栏中拖入一个大模型节点，命名为“信息提取”。请将此节点连接到开始节点，并按照指引填写参数。
    
    > 其他参数保持默认即可。
    
    | 参数名 | 参数值 |
    | --- | --- |
    | **模型配置** | 通义千问-Max |
    | **System Prompt** | 你是一个信息提取专家，你的任务是帮助“查询天气工具”解析正确的输入参数。<br><br>\---<br><br>“查询天气工具”的描述如下：<br><br>名称：maps\_weather<br><br>描述：根据城市名称或者标准adcode查询指定城市的天气<br><br>输入参数：city \[string\] 城市名称或者adcode<br><br>输出参数：result \[string\] 城市的天气预报<br><br>\---<br><br>你的输出是“查询天气工具”的输入，你只需要输出城市的名称即可。<br><br>注意：你一次只能输出一个城市。 |
    | **User Prompt** | 通过键入"`/`"来呼出变量菜单，选中“**系统变量****query**。 |
    
    > **说明**
    >
    > 使用 MCP 节点前，通常需要将输入对话的自然语言转换为 MCP 节点的输入参数。因此，需要在 System Prompt 中描述 MCP 服务的功能和输入输出信息，以限定大模型的输出格式。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4527964471/p942187.png)
4.  **查询天气信息**
    
    > 使用高德 MCP 服务提供的天气查询工具，接收一个城市名，返回该城市的天气信息。
    
    从左侧工具栏中拖入一个 MCP 节点，按照图示选择 maps\_weather 工具，确认节点配置。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5124314471/p939250.png)
    
    将 MCP 节点命名为“天气查询工具”，然后将此节点连接到“信息提取”节点。
    
    > **说明**
    >
    > 点击节点左上角的箭头按钮，即可展开或收起节点配置。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4527964471/p942188.png)
    
    点击 MCP 节点内 maps\_weather 工具的配置按钮，修改输入为“引用：信息提取/result”。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4527964471/p942143.png)
5.  **总结天气信息**
    
    为了将 MCP 服务返回的结果整理成便于阅读的自然语言，从左侧工具栏中拖入一个大模型节点，命名为“信息总结”。请将此节点连接到“天气查询工具”节点，并按照指引填写参数。
    
    > 其他参数保持默认即可：
    
    | 参数名 | 参数值 |
    | --- | --- |
    | **模型配置** | 通义千问-Max |
    | **System Prompt** | 你是一个信息处理助手，你的任务是将用户输入的信息整合为自然语言。 |
    | **User Prompt** | 通过键入"`/`"来呼出变量菜单，选中“**天气查询工具****result**” |
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4527964471/p942186.png)
6.  **输出查询结果**
    
    将此节点连接到“信息总结”节点，并按照指引填写参数，以获取最终的输出结果。
    
    | 参数名 | 参数值 |
    | --- | --- |
    | **输入框** | 键入"`/`"来呼出变量菜单，选中“**信息总结****result** |
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4527964471/p942204.png)
7.  **测试查询效果**
    
    点击右上角“测试”按钮，输入“`查询杭州天气`”，查看工作流的输出结果。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7991344471/p941629.png)

> **重要**
>
> 也可通过阿里云百炼 CLI 管理和调用 MCP 服务：`bl mcp list` 查看已激活的服务，`bl mcp tools --server <Server Code>` 列出可用工具，`bl mcp call --target <Server Code>.<工具>` 直接调用。详见[使用 CLI](../../../cli/capabilities/agent-infrastructure/mcp-skill.md)。

<a id="外部调用-mcp-服务"></a>

<a id="51a14d6948thz"></a>

## 外部调用 MCP 服务

阿里云百炼支持通过外部调用将 MCP 服务集成至第三方应用或项目中，详情参考[外部调用](mcp-external-calls.md)。
