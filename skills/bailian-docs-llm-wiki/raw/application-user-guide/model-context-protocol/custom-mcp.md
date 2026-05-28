# 自定义 MCP 服务

除官方 MCP 服务外，阿里云百炼还支持以下三种自定义 MCP 服务部署方式：

1.  **使用脚本部署**：面向**代码**。适用于您拥有或找到了一个遵循 MCP 协议的**代码包**，例如您自行开发或开源社区的 MCP 服务代码。
    
2.  **从 AI 网关导入**：面向**已有的 API**。适用于您想将一个**现成的、非 MCP 规范的 RESTful API**（例如公司内部的业务接口、第三方服务接口）封装成可供大模型调用的工具。
    
3.  **从阿里云 OpenAPI 导入**：面向**阿里云生态**。适用于您想让大模型能够操作**其他的阿里云产品**（如 OSS, ECS 等）。
    

## **使用脚本部署**

对于自行开发或开源社区的 MCP 服务代码，阿里云百炼支持使用[函数计算 FC](https://www.aliyun.com/product/fc)进行托管。

以部署开源社区的 Knowledge Graph Memory MCP 服务为例：

> Knowledge Graph Memory MCP 服务：该服务使大模型能够记录个性化信息，并在后续交互中调用这些信息进行回复。

1.  **创建 MCP 服务**
    
    前往[MCP 管理](https://bailian.console.aliyun.com/?tab=app#/mcp-manage)，点击**创建MCP服务**。选择**使用脚本部署**，点击**部署服务**。
    
2.  **配置 MCP 服务**
    
    按照以下指引填写配置，确认无误后提交部署。
    
    **配置项**
    
    **用途**
    
    **本案例的配置**
    
    **服务名称**
    
    **描述**
    
    用于区分不同的 MCP 服务，不影响大模型的判断和调用。
    
    **服务名称**：长期记忆
    
    **描述**：该服务使大模型能够记录个性化信息，并在后续交互中调用这些信息进行回复。
    
    **安装方式**
    
    如果需要托管本地 MCP 服务（stdio），支持以下方式：
    
    -   **npx**：启动使用 Node.js 开发的 MCP 服务
        
    -   **uvx**：启动使用 Python 开发的 MCP 服务。
        
    
    如果需要连接远程 MCP 服务，支持以下方式：
    
    -   **http**：连接到一个已有的、运行在别处的远程 MCP 服务器。
        
    
    选择：**npx**
    
    **部署方式**
    
    （仅限 npx/uvx）
    
    **基础模式：按次计费**：适用于按需启动、节省成本、可以承受较慢响应的场景。
    
    **极速模式**：适用于持续运行、快速响应、可以承受较高成本的场景。
    
    > 详细计费规则请参考[计费说明](https://help.aliyun.com/zh/model-studio/mcp-introduction#fb482455a3u8c)。
    
    保持**基础模式：按次计费**，关闭**极速模式**
    
    **部署地域**
    
    （仅限 npx/uvx）
    
    为获得最佳响应速度，建议选择靠近其他已有云服务的地域。若不确定如何选择，推荐使用“**北京**”地域。
    
    选择：**北京**
    
    **MCP 服务配置**
    
    **重要**
    
    请务必核实 MCP 服务的来源和源代码，以免遭受钓鱼攻击。
    
    **重要**
    
    并非所有 MCP 服务都支持 npx/uvx/http 方式部署。若缺少相应配置代码，则无法直接部署到阿里云百炼。建议参考 [MCP 官方文档](https://modelcontextprotocol.io/quickstart/server)进行本地部署。
    
    **说明**
    
    使用 Java 开发的 MCP 服务，可以[自行部署到阿里云函数计算](https://help.aliyun.com/zh/functioncompute/mcp-server)，再通过 http 托管到百炼。
    
    -   如需部署开源社区 MCP 服务，请直接粘贴从 MCP 服务详情页获取的配置代码。
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5067198471/p963082.png)
        
    -   如需部署自行开发的 MCP 服务，请参考以下模板编写配置代码。
        
        **说明**
        
        此配置模板适用于[基于 npx/uvx/http 最佳实践开发的 MCP 服务](https://modelcontextprotocol.io/examples)。若采用其他开发方式，请对模板进行相应修改。
        
        ```
        {
          "mcpServers": {
            "本地 MCP 服务": {
              "type": "stdio",
              "command": "npx",
              "args": [
                "-y",
                "@your_acc_name/your_pkg_name"
              ],
              "env": {
                "YOUR_ENV_KEY": "YOUR_ENV_VALUE"
              }
            },
            "远程 MCP 服务": {
              "type": "sse/streamableHttp",
              "url": "https://your-mcp-server/sse"
            }
          }
        }
        ```
        
    
    直接使用以下配置代码:
    
    ```
    {
      "mcpServers": {
        "memory": {
          "command": "npx",
          "args": [
            "-y",
            "@modelcontextprotocol/server-memory"
          ]
        }
      }
    }
    ```
    
    或在[MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)找到这个 MCP 服务，单击进入详情页，找到标题为 `NPX` 的配置代码。
    
3.  **管理 MCP 服务**
    
    提交部署后，可查看部署状态、测试工具效果以及修改服务配置。
    
    1.  **查看部署状态**
        
        可前往函数计算 FC 控制台查看 MCP 服务的详细部署状态。
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9001984471/p944519.png)
        
        （可选）建议启用日志服务，方便实时查看服务运行状态，排查可能出现的错误。
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9001984471/p944533.png)
        
        **说明**
        
        函数计算 FC 的日志服务会产生一定费用，详情请参考控制台的日志服务计费说明。
        
    2.  **测试工具效果：**
        
        在**工具**页可测试 MCP 服务的运行效果
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9001984471/p944542.png)
        
    3.  **修改服务配置：**
        
        部署后，仅支持编辑**服务名称**和**描述**。如需修改**部署方式**、**部署地域**、**安装方式**和 **MCP 服务配置**，必须先停止当前部署，在修改配置后重新部署。
        
4.  **使用 MCP 服务**
    
    部署完成后，即可将自定义 MCP 服务[在智能体或工作流中配置 MCP 服务](https://help.aliyun.com/zh/model-studio/official-and-third-party-mcp#8319d03864jym)。
    

## **从 AI 网关导入**

对于已有的自建或第三方业务接口，可使用AI 网关将 RESTful API 升级为 MCP 服务，详情请参考[网关托管MCP服务](https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/gateway-managed-mcp-services)。通过阿里云百炼，可以快速导入在 AI 网关托管的 MCP 服务。

1.  **导入准备**
    
    请确保已在 [AI 网关](https://apig.console.aliyun.com/#/cn-hangzhou/ai-gateway)托管了 MCP 服务。
    
2.  **导入 MCP 服务**
    
    前往 [MCP 管理](https://bailian.console.aliyun.com/?tab=app#/mcp-manage)，单击**创建MCP服务**。选择**AI网关**，单击**导入服务**。
    
3.  **配置 MCP 服务**
    
    按照下表指引填写配置信息，确认无误后单击**确认导入**。
    
    **配置项**
    
    **配置说明**
    
    **示例**
    
    **网关所在区域**
    
    AI 网关所在地域
    
    华东 1（杭州）
    
    **网关实例**
    
    AI 网关实例
    
    test
    
    **选择MCP服务**
    
    AI 网关托管的 MCP 服务
    
    test
    
    **选择接入点**
    
    AI 网关托管的 MCP 服务的接入点。系统会自动生成一个可供测试的接入点。
    
    \[自动生成\]
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7729282571/p987431.png)
    
4.  **完成导入**
    
    导入完成后，可在**MCP 管理** > **自定义服务**查看从 AI 网关导入的 MCP 服务。
    

## **从阿里云 OpenAPI 导入**

如需通过操作阿里云云资源创建服务，可使用 OpenAPI 开发者门户将官方 OpenAPI 快速发布为 MCP 服务，详情请参考[OpenAPI MCP Server使用指南](https://help.aliyun.com/zh/openapi/user-guide/openapi-mcp-server-guide)。通过阿里云百炼，可以快速导入 OpenAPI 开发者门户 MCP 服务。

1.  **导入准备**
    
    请确保在 [OpenAPI 开发者门户](https://api.aliyun.com/mcp)创建过 MCP 服务。
    
2.  **导入 MCP 服务**
    
    前往[MCP 管理](https://bailian.console.aliyun.com/?tab=app#/mcp-manage)，点击**创建MCP服务**。选择**阿里云OpenAPI**，点击**导入服务**。
    
3.  **配置 MCP 服务**
    
    按照以下指引填写配置，检查无误后点击**确认导入**。
    
    **配置项**
    
    **配置说明**
    
    **示例**
    
    **服务名称**
    
    需要导入的 OpenAPI MCP 服务。
    
    oss
    
    **访问阿里云 OpenAPI 角色**
    
    阿里云百炼访问 OpenAPI 时的角色。可使用已有角色，或在此处**创建角色**。
    
    BailianMcpRoleFoross
    
    **权限策略**
    
    前往[RAM 权限策略](https://ram.console.aliyun.com/policies)，使用此处的 JSON 脚本创建权限策略，并为**访问阿里云 OpenAPI 角色**授予该权限策略。
    
    \[自动生成\]
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7729282571/p987389.png)
    
4.  **完成导入**
    
    导入完成后，可在**MCP 管理** > **自定义服务**查看从 OpenAPI 导入的 MCP 服务。
