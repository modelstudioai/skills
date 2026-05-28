# 通义 UI Agent

UI Agent 是基于终端屏幕理解操作手机/车机/电视/PC等终端的多模态智能体方案。支持跨应用操作且无需训练，即插即用。

## **基础信息**

版本号：V0.0.1

API Endpoint： [https://dashscope.aliyuncs.com/](https://dashscope.aliyuncs.com/)

## 接口信息

本接口协议适配 Agent API，涉及全链路调用的实例参考最后的例子，本节仅介绍服务接口信息。

**使用准备**

-   需要[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)
    

**请求地址**

https://dashscope.aliyuncs.com/api/v2/apps/gui-owl/gui\_agent\_server

**请求头**

**字段**

**类型**

**必选**

**描述**

**示例值**

Authorization

String

是

填写通过阿里云控制台获取的API Key

`Bearer sk-xxxxxxxxxxxxxxxxxxxx`

Content-Type

String

是

格式

application/json

### **移动端（Mobile） 链路**

**入参描述**

**字段**

**类型**

**必选**

**描述**

**示例值**

app\_id

String

是

固定值为：gui-owl

gui-owl

input

Array

是

传入信息结构列表，目前固定为单条

input\[0\].role

String

是

角色，默认传user

user

input\[0\].content

Array

是

当前版本只处理第一个元素，并忽略其余

{

"type": "data",

"data":

}

input\[0\].content\[0\].type

String

是

类型

input\[0\].content\[0\].data

Dict

是

数据体

input\[0\].content\[0\].data.messages

Array

是

单键值对对象数组

messages单键值对对象数组

单键值对象数组

```
[
              {
                "image": "http://" # 请替换为有效的url
              },
              {
                "instruction": "打开微博"
              },
              {
                "session_id": ""
              },
              {
                "device_type": "mobile"
              },
              {
                "pipeline_type": "agent"
              },
              {
                "model_name": "pre-gui_owl_7b"
              },
              {
                "thought_language": "chinese"
              },
              {
                "param_list": [
                  {
                    "add_info": ""
                  }
                ]
              }
            ]
```

image

String

是

图片路径

http(s)://

instruction

String

是

任务指令，即Mobile-Agent需要完成的任务

在去哪儿旅行中查询10月19日从北京到杭州的火车票

session\_id

String

是

用于关联历史操作的查询ID，第一次调用空置，后续调用填入第一次返回的 session\_id 字段即可将所有操作关联起来

session id : bee1915d-6f4d-4bfc-b657-ecb9d0ed8dad

device\_type

String

是

链路类型

mobile

pipeline\_type

String

是

框架类型

agent

model\_name

String

是

模型名称

pre-gui\_owl\_7b

thought\_language

String

否

返回语言

chinese

param\_list

Array

是

额外参数

param\_list数组内键值对

add\_info

String

是

操作说明，可以添加操作知识来帮助Agent更准确地进行操作

1\. 点击火车·高铁模块.\\n2. 点击日期修改时间.\\n3. 点击对应的出发时间.\\n4. 点击左侧的城市名来修改出发地.\\n5. 点击起点的对应城市.\\n6. 点击右侧的城市名来修改目的地.\\n7. 点击终点对应的城市.\\n8. 上述操作完成后，点击“搜索”.

请求示例

```
curl --location --request POST 'https://dashscope.aliyuncs.com/api/v2/apps/gui-owl/gui_agent_server' \
--header 'Authorization: Bearer sk-' \
--header 'Content-Type: application/json' \
--data-raw '{
  "app_id": "gui-owl",
  "input": [
    {
      "role": "user",
      "content": [
        {
          "type": "data",
          "data": {
            "messages": [
              {
                "image": "http://" # 请替换为有效的url
              },
              {
                "instruction": "打开微博"
              },
              {
                "session_id": ""
              },
              {
                "device_type": "mobile"
              },
              {
                "pipeline_type": "agent"
              },
              {
                "model_name": "pre-gui_owl_7b"
              },
              {
                "thought_language": "chinese"
              },
              {
                "param_list": [
                  {
                    "add_info": ""
                  }
                ]
              }
            ]
          }
        }
      ]
    }
  ]
}'
```

响应示例

```
import time
import uuid
import requests
import json
import os

session_id = ""

# 定义请求URL
url = "https://dashscope.aliyuncs.com/api/v2/apps/gui-owl/gui_agent_server"
# 准备请求头
headers = {
    "Authorization": f"Bearer {os.getenv('DASHSCOPE_API_KEY')}",  # 请替换为有效的API-KEY
    "Content-Type": "application/json"
}

content = [
    {
        "type": "data",
        "data": {
            "messages": [
                {
                    "image": "http://" # 请替换为有效的url
                },
                {
                    "instruction": "打开浏览器"
                },
                {
                    "session_id": session_id
                },
                {
                    "device_type": "mobile"
                },
                {
                    "pipeline_type": "agent"
                },
                {
                    "model_name": "pre-gui_owl_7b"
                },
                {
                    "thought_language": "chinese"
                },
                {
                    "param_list": [
                        {
                            "add_info": ""
                        }
                    ]
                }
            ]
        }
    }
]

try:
    payload = {
        "app_id": "gui-owl",
        "input": [
            {
                "role": "user",
                "content": content
            }
        ]
    }

    start_time = time.time()
    # 发送POST请求
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print(f"Response Body: {response.text}")
    # 检查响应状态
    response.raise_for_status()
    response_data = response.json()
    session_id = response_data['session_id']

    print(f"耗时：\n", time.time() - start_time)

except requests.exceptions.RequestException as e:
    print(f"请求发生错误: {e}")
```

##### **出参描述**

**字段**

**类型**

**描述**

**示例值**

id

String

请求id

output

Array

返回数据，固定一条

output\[0\].code

String

业务状态码，200表示成功

output\[0\].id

String

请求id

86693b43-2c99-9f51-9df0-2c32f15e7a3a

output\[0\].content

Array

output\[0\].content.data

Dict

推理数据

data内的数据

Explanation

String

动作信息

Tap on the Weibo app icon located in the first row of the home screen.

Operation

String

操作动作

Click (144, 248, 144, 248)

Thought

String

思考内容

The user wants to open the Weibo app. The Weibo app icon is visible in the first row of the home screen, so I need to tap on it to proceed with opening the application.

usage

dict

该次请求的token消耗

{  
"input\_tokens": 1537,  
"output\_tokens": 39  
}

完整返回实例

```
{
    "created_at": 1758548962,
    "id": "401a9031-3fa5-4655-a34d-090523a6dd1d",
    "object": "response",
    "output": [
        {
            "code": "200",
            "content": [
                {
                    "data": {
                        "Explanation": "Swipe up from the bottom of the screen to open the app drawer.",
                        "Operation": "Swipe (512, 708, 512, 353)",
                        "Thought": "To achieve the user's request of opening the Google app, I need to first access the app drawer. Since the Google app is not visible on the home screen, swiping up or accessing the app drawer is necessary. This will allow me to locate and tap on the Google app icon."
                    },
                    "delta": false,
                    "object": "content",
                    "type": "data"
                }
            ],
            "id": "401a9031-3fa5-4655-a34d-090523a6dd1d",
            "message": "Success",
            "object": "message",
            "role": "assistant",
            "status": "Success",
            "type": "message"
        }
    ],
    "session_id": "7c86289e-127a-4edf-8055-5727489aef49",
    "status": "created",
    "usage": {
        "input_tokens": 0,
        "output_tokens": 0
    }
}
```

### **PC 端链路**

##### **入参描述**

**字段**

**类型**

**必选**

**描述**

**示例值**

app\_id

String

是

固定值为：gui-owl

gui-owl

input

Array

是

传入信息结构列表，目前固定为单条

input\[0\].role

String

是

角色，默认传user

user

input\[0\].content

Array

输入内容

目前固定为单条content

{

"type": "data",

"data":

}

input\[0\].content\[0\].type

String

是

类型

input\[0\].content\[0\].data

Dict

是

数据体

input\[0\].content\[0\].data.messages

Array

是

每条messages必须包含： image, instruction,add\_info,session\_id 四个值

messages数组内键值对

image

String

是

当前的设备屏幕截屏的本地路径

oss地址

instruction

String

是

任务指令，即Mobile-Agent需要完成的任务

在去哪儿旅行中查询10月19日从北京到杭州的火车票

session\_id

String

是

用于关联历史操作的查询ID，第一次调用空置，后续调用填入第一次返回的 session\_id 字段即可将所有操作关联起来

session id : bee1915d-6f4d-4bfc-b657-ecb9d0ed8dad

device\_type

String

是

链路类型

pc

pipeline\_type

String

是

框架类型

agent

model\_name

String

是

模型名称

pre-gui\_owl\_7b

param\_list

Array

是

额外参数

param\_list数组内键值对

add\_info

String

是

操作说明，可以添加操作知识来帮助Agent更准确地进行操作，书写格式请参考add\_info文档

enable\_reflector

Boolean

否

是否添加反思agent

enable\_notetaker

Boolean

否

是否添加memory agent

worker\_model

String

是

决策agent使用的模型

manager\_model

String

是

规划agent使用的模型

reflector\_model

String

是

反思agent使用的模型

notetaker\_model

String

是

Memory agent使用的模型

请求示例

```
curl --location --request POST 'https://dashscope.aliyuncs.com/api/v2/apps/gui-owl/gui_agent_server' \
--header 'Authorization: Bearer sk-' \
--header 'Content-Type: application/json' \
--data-raw '{
  "app_id": "gui-owl",
  "input": [
    {
      "role": "user",
      "content": [
        {
          "type": "data",
          "data": {
            "messages": [
              {
                "image": "http://" # 请替换为有效的url
              },
              {
                "instruction": "打开计算器"
              },
              {
                "session_id": ""
              },
              {
                "device_type": "pc"
              },
              {
                "pipeline_type": "agent"
              },
              {
                "model_name": "pre-gui_owl_7b"
              },
              {
                "thought_language": "chinese"
              },
              {
                "param_list": [
                  {
                    "add_info": ""
                  },
                  {
                    "enable_reflector": true
                  },
                  {
                    "enable_notetaker": true
                  },
                  {
                    "worker_model": "pre-gui_owl_7b"
                  },
                  {
                    "manager_model": "pre-gui_owl_7b"
                  },
                  {
                    "reflector_model": "pre-gui_owl_7b"
                  },
                  {
                    "notetaker_model": "pre-gui_owl_7b"
                  }
                ]
              }
            ]
          }
        }
      ]
    }
  ]
}'
```

响应示例

```
import time
import uuid
import requests
import json
import os

session_id = ""

# 定义请求URL
url = "https://dashscope.aliyuncs.com/api/v2/apps/gui-owl/gui_agent_server"
# 准备请求头
headers = {
    "Authorization": f"Bearer {os.getenv('DASHSCOPE_API_KEY')}",  # 请替换为有效的API-KEY
    "Content-Type": "application/json"
}

content = [
    {
        "type": "data",
        "data": {
            "messages": [
                {
                    "image": "http://" # 请替换为有效的url
                },
                {
                    "instruction": "打开浏览器"
                },
                {
                    "session_id": session_id
                },
                {
                    "device_type": "pc"
                },
                {
                    "pipeline_type": "agent"
                },
                {
                    "model_name": "pre-gui_owl_7b"
                },
                {
                    "thought_language": "chinese"
                },
                {
                    "param_list": [
                        {
                            "add_info": ""
                        },
                        {
                            "enable_reflector": True
                        },
                        {
                            "enable_notetaker": True
                        },
                        {
                            "worker_model": "pre-gui_owl_7b"
                        },
                        {
                            "manager_model": "pre-gui_owl_7b"
                        },
                        {
                            "reflector_model": "pre-gui_owl_7b"
                        },
                        {
                            "notetaker_model": "pre-gui_owl_7b"
                        }
                    ]
                }
            ]
        }
    }
]

try:
      # 随机生成request_id
      payload = {
          "app_id": "gui-owl",
          "input": [
              {
                  "role": "user",
                  "content": content
              }
          ]
      }

      start_time = time.time()
      # 发送POST请求
      response = requests.post(url, headers=headers, data=json.dumps(payload))
      print(f"Response Body: {response.text}")
      # 检查响应状态
      response.raise_for_status()
      response_data = response.json()
      session_id = response_data['session_id']

      print(f"耗时：\n", time.time() - start_time)

except requests.exceptions.RequestException as e:
    print(f"请求发生错误: {e}")
```

##### **出参描述**

**字段**

**类型**

**描述**

**示例值**

output

Array

返回数据，固定一条

output\[0\].code

String

200

output\[0\].id

String

请求id

86693b43-2c99-9f51-9df0-2c32f15e7a3a

output\[0\].content

Array

output\[0\].content.data

Dict

推理数据

data内的数据

action\_parameter

Dict

动作的参数

{

"count": 1,

"position": \[

69,

2124

\]

}

action\_type

String

动作类型

click

explanation

String

动作的总结

global\_state

Dict

整体规划、当前子任务等信息

meta\_data

Dict

此字段仅供调试使用，生产环境请勿依赖，其结构和内容未来可能变更或移除

thought

String

思考内容

完整返回实例

```
{
    "created_at": 1758182731,
    "object": "response",
    "output": [
        {
            "code": "200",
            "content": [
                {
                    "data": {
                        "action_parameter": {
                            "count": 1,
                            "position": [
                                69,
                                2124
                            ]
                        },
                        "action_type": "click",
                        "explanation": "点击屏幕底部左侧的“开始按钮”，这将打开Windows的开始菜单，从而允许我们接下来搜索并打开计算器应用。",
                        "global_state": {
                            "manager": "### Thought ###\nThe user wants to open the calculator application. The screenshot shows the Windows desktop with various icons, but the calculator icon is not immediately visible. To achieve this, I need to locate and open the calculator. Since it's not on the desktop, I'll assume it might be in the Start menu or another location like the All Apps menu. Therefore, the plan involves accessing the Start menu and finding the calculator there.\n\n### Plan ###\n1. {'name': 'Open the Start Menu', 'info': 'Click on the Start button located at the bottom left corner of the screen to open the Start menu.'}\n2. {'name': 'Locate Calculator', 'info': 'In the Start menu, scroll through the list of applications or use the search bar at the top to find \"Calculator\".'}\n\n### Current Subgoal ###\nOpen the Start Menu",
                            "worker": "### Thought ###\n为了打开计算器，我需要首先打开开始菜单。根据Windows操作系统的标准，点击左下角的“开始按钮”可以打开开始菜单。这个按钮通常位于屏幕底部左侧，并且是一个带有Windows标志的圆形图标。\n\n### Action ###\n{\"action\": \"click\", \"coordinate\": [35, 1074]}\n\n### Description ###\n点击屏幕底部左侧的“开始按钮”，这将打开Windows的开始菜单，从而允许我们接下来搜索并打开计算器应用。"
                        },
                        "meta_data": {
                            "executor": {
                                "messages": [
                                    {
                                        "content": [
                                            {
                                                "text": "You are a helpful assistant.",
                                                "type": "text"
                                            }
                                        ],
                                        "role": "system"
                                    },
                                    {
                                        "content": [
                                            {
                                                "text": "You are an agent who can operate a computer on behalf of a user. Your goal is to decide the next action to perform based on the current state of the phone and the user's request.\n\n### User Request ###\n打开计算器\nYou can follow these tips:\n\nOn Windows, you absolutely have to double-click to open any desktop icon or folder in File Explorer—one single click will NOT open them. Always double-click.\n\n### Overall Plan ###\n1. {'name': 'Open the Start Menu', 'info': 'Click on the Start button located at the bottom left corner of the screen to open the Start menu.'} 2. {'name': 'Locate Calculator', 'info': 'In the Start menu, scroll through the list of applications or use the search bar at the top to find \"Calculator\".'}\n\n### Progress Status ###\nNo progress yet.\n\n### Current Subgoal ###\nOpen the Start Menu\n\n### Collected Task-Related Notes ###\nNo important notes recorded.\n\n---\nCarefully examine all the information provided above and decide on the next action to perform. If you notice an unsolved error in the previous action, think as a human user and attempt to rectify them. You must choose your action from one of the atomic actions.\n\n#### Atomic Actions ####\nThe atomic action functions are listed in the format of `action(arguments): description` as follows:\n- open_app(app_name): Open the App with app_name such as Chrome and Wechat. Usage Example: {\"action\": \"open_app\", \"app_name\": \"chrome\"}\n- click(coordinate): Click the point on the screen with specified (x, y) coordinates. Usage Example: {\"action\": \"click\", \"coordinate\": [x, y]}\n- double_click(coordinate): Double click on the position (x, y) on the screen. Usage Example: {\"action\": \"double_click\", \"coordinate\": [x, y]}\n- right_click(coordinate): Right-click using the mouse on the position (x, y) on the screen. Usage Example: {\"action\": \"double_click\", \"coordinate\": [x, y]}\n- type(coordinate, text, clear, enter): Type text into the position (x, y) on the screen. Use escape characters \\', \\\", and \\n in the `text` part to ensure we can parse the content in normal python string format. If you want to clear the existing content, set the `clear` parameter to 1; otherwise, set it to 0. If you want to press `enter` after input, set the `enter` parameter to 1; otherwise, set it to 0. Usage Example: {\"action\": \"type\", \"coordinate\": [x, y], \"text\": \"the text you want to type\", \"clear\": 1, \"enter\": 1}\n- hotkey(keys): Press a hotkey combination. The `keys` parameter is a list of keys represented as a string, such as \"['ctrl', 'c']\". Usage Example: {\"action\": \"hotkey\", \"keys\": \"['ctrl', 'c']\"}\n- scroll(coordinate, value): Scroll at the position (x, y) on the screen. The `value` parameter can be positive (scroll up) or negative (scroll down), which is usually set to 5 or -5. Usage Example: {\"action\": \"scroll\", \"coordinate\": [x, y], \"value\": 5}\n- wait(time): Wait for a specified amount of time, such as 3s. Usage Example: {\"action\": \"wait\", \"time\": 3}\n- call_user(): Call the user when the task is unsolvable, or when you need the user's help, such as log in or close the pop up. Usage Example: {\"action\": \"call_user\"}\n- drag(coordinate, coordinate2): drag from the position with coordinate to the position with coordinate2. Usage Example: {\"action\": \"drag\", \"coordinate\": [x1, y1], \"coordinate2\": [x2, y2]}\n- set_cell_values(cell_values, file_name, sheet_name): set individual cell values (a Dict) in the sheet with sheet_name and in the spreadsheet with file_name. Usage Example: {\"action\": \"set_cell_value\", \"cell_values\": {\"A2\": \"hello\"}, \"file_name\": 'Untitled 1', \"sheet_name\": 'Sheet1'}\n- done(): Output this action when you think this instruction is done. Usage Example: {\"action\": \"done\"}\n\n### Latest Action History ###\nNo actions have been taken yet.\n\n### Tips\n\n* On Windows, you absolutely have to double-click to open any desktop icon or folder in File Explorer—one single click will NOT open them. Always double-click.\n* 如果需要登录或者遇到弹窗，请使用call_user工具来呼唤用户进行接管，不要输入账号密码或者擅自操作\n* Use app-specific tools first, rather than generic cv tools such as cv_click or cv_key.\n\n\n---\nProvide your output in the following format, which contains three parts:\n### Thought ###\nProvide a detailed explanation of your rationale for the chosen action.  Please output in Chinese.\n\n### Action ###\nChoose only one action or shortcut from the options provided. IMPORTANT: Do NOT return invalid actions like null or stop. Do NOT repeat previously failed actions multiple times.\nYou must provide your decision using a valid JSON format specifying the `action` and the arguments of the action.\n\n### Description ###\nA brief description of the chosen action and the expected outcome.  Please output in Chinese."
                                            },
                                            {
                                                "image": "C:\\0421d463-47ac-4307-8bed-a22df6568cad.png"
                                            }
                                        ],
                                        "role": "user"
                                    },
                                    {
                                        "content": [
                                            {
                                                "text": "### Thought ###\n为了打开计算器，我需要首先打开开始菜单。根据Windows操作系统的标准，点击左下角的“开始按钮”可以打开开始菜单。这个按钮通常位于屏幕底部左侧，并且是一个带有Windows标志的圆形图标。\n\n### Action ###\n{\"action\": \"click\", \"coordinate\": [35, 1074]}\n\n### Description ###\n点击屏幕底部左侧的“开始按钮”，这将打开Windows的开始菜单，从而允许我们接下来搜索并打开计算器应用。"
                                            }
                                        ],
                                        "role": "assistant"
                                    }
                                ],
                                "name": "operator",
                                "response": "### Thought ###\n为了打开计算器，我需要首先打开开始菜单。根据Windows操作系统的标准，点击左下角的“开始按钮”可以打开开始菜单。这个按钮通常位于屏幕底部左侧，并且是一个带有Windows标志的圆形图标。\n\n### Action ###\n{\"action\": \"click\", \"coordinate\": [35, 1074]}\n\n### Description ###\n点击屏幕底部左侧的“开始按钮”，这将打开Windows的开始菜单，从而允许我们接下来搜索并打开计算器应用。"
                            },
                            "manager": {
                                "messages": [
                                    {
                                        "content": [
                                            {
                                                "text": "You are a helpful assistant.",
                                                "type": "text"
                                            }
                                        ],
                                        "role": "system"
                                    },
                                    {
                                        "content": [
                                            {
                                                "text": "You are an agent who can operate a windows computer on behalf of a user. Your goal is to track progress and devise high-level plans to achieve the user's requests.\n\n### User Request ###\n打开计算器\nYou can follow these tips:\n\nOn Windows, you absolutely have to double-click to open any desktop icon or folder in File Explorer—one single click will NOT open them. Always double-click.\n\n---\nMake a high-level plan to achieve the user's request. If the request is complex, break it down into subgoals. The screenshot displays the starting state of the computer.\n请返回中文。\n\n##### Important Notes #####\n1. Before generating your plan, carefully observe and understand the current state of the computer.\n2. Your plan should contain only necessary steps; however, please include information useful for executing the subgoal in the 'info' field.\n3. Do not include verification steps in your plan. Steps that confirm or validate other subtasks should not be included.\n4. Do not include optional steps in your plan.\n\nProvide your output in the following format which contains three parts:\n\n### Thought ###\nA detailed explanation of your rationale for the plan and subgoals.\n\n### Plan ###\n1. {'name': 'brief description of the first subgoal.', 'info': 'detailed information about executing the first subgoal.'}\n2. {'name': 'brief description of the second subgoal.', 'info': 'detailed information about executing the second subgoal.'}\n...\n\n### Current Subgoal ###\nThe first subgoal's name you should work on.\n\n"
                                            },
                                            {
                                                "image": "C:\\Usersimages\\b5bf3eff-ae32-4dd0-85ee-7ee31c359142.png"
                                            }
                                        ],
                                        "role": "user"
                                    },
                                    {
                                        "content": [
                                            {
                                                "text": "### Thought ###\nThe user wants to open the calculator application. The screenshot shows the Windows desktop with various icons, but the calculator icon is not immediately visible. To achieve this, I need to locate and open the calculator. Since it's not on the desktop, I'll assume it might be in the Start menu or another location like the All Apps menu. Therefore, the plan involves accessing the Start menu and finding the calculator there.\n\n### Plan ###\n1. {'name': 'Open the Start Menu', 'info': 'Click on the Start button located at the bottom left corner of the screen to open the Start menu.'}\n2. {'name': 'Locate Calculator', 'info': 'In the Start menu, scroll through the list of applications or use the search bar at the top to find \"Calculator\".'}\n\n### Current Subgoal ###\nOpen the Start Menu"
                                            }
                                        ],
                                        "role": "assistant"
                                    }
                                ],
                                "name": "manager",
                                "response": "### Thought ###\nThe user wants to open the calculator application. The screenshot shows the Windows desktop with various icons, but the calculator icon is not immediately visible. To achieve this, I need to locate and open the calculator. Since it's not on the desktop, I'll assume it might be in the Start menu or another location like the All Apps menu. Therefore, the plan involves accessing the Start menu and finding the calculator there.\n\n### Plan ###\n1. {'name': 'Open the Start Menu', 'info': 'Click on the Start button located at the bottom left corner of the screen to open the Start menu.'}\n2. {'name': 'Locate Calculator', 'info': 'In the Start menu, scroll through the list of applications or use the search bar at the top to find \"Calculator\".'}\n\n### Current Subgoal ###\nOpen the Start Menu"
                            }
                        },
                        "thought": "为了打开计算器，我需要首先打开开始菜单。根据Windows操作系统的标准，点击左下角的“开始按钮”可以打开开始菜单。这个按钮通常位于屏幕底部左侧，并且是一个带有Windows标志的圆形图标。\n\n"
                    },
                    "delta": false,
                    "object": "content",
                    "type": "data"
                }
            ],
            "id": "msg_e9dd72ea-19fc-4a22-93ee-d97588645f88",
            "message": "Success",
            "object": "message",
            "role": "assistant",
            "status": "Success",
            "type": "message"
        }
    ],
    "session_id": "bee1915d-6f4d-4bfc-b657-ecb9d0ed8dad",
    "status": "created"
}{
    "created_at": 1758182731,
    "object": "response",
    "output": [
        {
            "code": "200",
            "content": [
                {
                    "data": {
                        "action_parameter": {
                            "count": 1,
                            "position": [
                                69,
                                2124
                            ]
                        },
                        "action_type": "click",
                        "explanation": "点击屏幕底部左侧的“开始按钮”，这将打开Windows的开始菜单，从而允许我们接下来搜索并打开计算器应用。",
                        "global_state": {
                            "manager": "### Thought ###\nThe user wants to open the calculator application. The screenshot shows the Windows desktop with various icons, but the calculator icon is not immediately visible. To achieve this, I need to locate and open the calculator. Since it's not on the desktop, I'll assume it might be in the Start menu or another location like the All Apps menu. Therefore, the plan involves accessing the Start menu and finding the calculator there.\n\n### Plan ###\n1. {'name': 'Open the Start Menu', 'info': 'Click on the Start button located at the bottom left corner of the screen to open the Start menu.'}\n2. {'name': 'Locate Calculator', 'info': 'In the Start menu, scroll through the list of applications or use the search bar at the top to find \"Calculator\".'}\n\n### Current Subgoal ###\nOpen the Start Menu",
                            "worker": "### Thought ###\n为了打开计算器，我需要首先打开开始菜单。根据Windows操作系统的标准，点击左下角的“开始按钮”可以打开开始菜单。这个按钮通常位于屏幕底部左侧，并且是一个带有Windows标志的圆形图标。\n\n### Action ###\n{\"action\": \"click\", \"coordinate\": [35, 1074]}\n\n### Description ###\n点击屏幕底部左侧的“开始按钮”，这将打开Windows的开始菜单，从而允许我们接下来搜索并打开计算器应用。"
                        },
                        "meta_data": {
                            "executor": {
                                "messages": [
                                    {
                                        "content": [
                                            {
                                                "text": "You are a helpful assistant.",
                                                "type": "text"
                                            }
                                        ],
                                        "role": "system"
                                    },
                                    {
                                        "content": [
                                            {
                                                "text": "You are an agent who can operate a computer on behalf of a user. Your goal is to decide the next action to perform based on the current state of the phone and the user's request.\n\n### User Request ###\n打开计算器\nYou can follow these tips:\n\nOn Windows, you absolutely have to double-click to open any desktop icon or folder in File Explorer—one single click will NOT open them. Always double-click.\n\n### Overall Plan ###\n1. {'name': 'Open the Start Menu', 'info': 'Click on the Start button located at the bottom left corner of the screen to open the Start menu.'} 2. {'name': 'Locate Calculator', 'info': 'In the Start menu, scroll through the list of applications or use the search bar at the top to find \"Calculator\".'}\n\n### Progress Status ###\nNo progress yet.\n\n### Current Subgoal ###\nOpen the Start Menu\n\n### Collected Task-Related Notes ###\nNo important notes recorded.\n\n---\nCarefully examine all the information provided above and decide on the next action to perform. If you notice an unsolved error in the previous action, think as a human user and attempt to rectify them. You must choose your action from one of the atomic actions.\n\n#### Atomic Actions ####\nThe atomic action functions are listed in the format of `action(arguments): description` as follows:\n- open_app(app_name): Open the App with app_name such as Chrome and Wechat. Usage Example: {\"action\": \"open_app\", \"app_name\": \"chrome\"}\n- click(coordinate): Click the point on the screen with specified (x, y) coordinates. Usage Example: {\"action\": \"click\", \"coordinate\": [x, y]}\n- double_click(coordinate): Double click on the position (x, y) on the screen. Usage Example: {\"action\": \"double_click\", \"coordinate\": [x, y]}\n- right_click(coordinate): Right-click using the mouse on the position (x, y) on the screen. Usage Example: {\"action\": \"double_click\", \"coordinate\": [x, y]}\n- type(coordinate, text, clear, enter): Type text into the position (x, y) on the screen. Use escape characters \\', \\\", and \\n in the `text` part to ensure we can parse the content in normal python string format. If you want to clear the existing content, set the `clear` parameter to 1; otherwise, set it to 0. If you want to press `enter` after input, set the `enter` parameter to 1; otherwise, set it to 0. Usage Example: {\"action\": \"type\", \"coordinate\": [x, y], \"text\": \"the text you want to type\", \"clear\": 1, \"enter\": 1}\n- hotkey(keys): Press a hotkey combination. The `keys` parameter is a list of keys represented as a string, such as \"['ctrl', 'c']\". Usage Example: {\"action\": \"hotkey\", \"keys\": \"['ctrl', 'c']\"}\n- scroll(coordinate, value): Scroll at the position (x, y) on the screen. The `value` parameter can be positive (scroll up) or negative (scroll down), which is usually set to 5 or -5. Usage Example: {\"action\": \"scroll\", \"coordinate\": [x, y], \"value\": 5}\n- wait(time): Wait for a specified amount of time, such as 3s. Usage Example: {\"action\": \"wait\", \"time\": 3}\n- call_user(): Call the user when the task is unsolvable, or when you need the user's help, such as log in or close the pop up. Usage Example: {\"action\": \"call_user\"}\n- drag(coordinate, coordinate2): drag from the position with coordinate to the position with coordinate2. Usage Example: {\"action\": \"drag\", \"coordinate\": [x1, y1], \"coordinate2\": [x2, y2]}\n- set_cell_values(cell_values, file_name, sheet_name): set individual cell values (a Dict) in the sheet with sheet_name and in the spreadsheet with file_name. Usage Example: {\"action\": \"set_cell_value\", \"cell_values\": {\"A2\": \"hello\"}, \"file_name\": 'Untitled 1', \"sheet_name\": 'Sheet1'}\n- done(): Output this action when you think this instruction is done. Usage Example: {\"action\": \"done\"}\n\n### Latest Action History ###\nNo actions have been taken yet.\n\n### Tips\n\n* On Windows, you absolutely have to double-click to open any desktop icon or folder in File Explorer—one single click will NOT open them. Always double-click.\n* 如果需要登录或者遇到弹窗，请使用call_user工具来呼唤用户进行接管，不要输入账号密码或者擅自操作\n* Use app-specific tools first, rather than generic cv tools such as cv_click or cv_key.\n\n\n---\nProvide your output in the following format, which contains three parts:\n### Thought ###\nProvide a detailed explanation of your rationale for the chosen action.  Please output in Chinese.\n\n### Action ###\nChoose only one action or shortcut from the options provided. IMPORTANT: Do NOT return invalid actions like null or stop. Do NOT repeat previously failed actions multiple times.\nYou must provide your decision using a valid JSON format specifying the `action` and the arguments of the action.\n\n### Description ###\nA brief description of the chosen action and the expected outcome.  Please output in Chinese."
                                            },
                                            {
                                                "image": "C:\\0421d463-47ac-4307-8bed-a22df6568cad.png"
                                            }
                                        ],
                                        "role": "user"
                                    },
                                    {
                                        "content": [
                                            {
                                                "text": "### Thought ###\n为了打开计算器，我需要首先打开开始菜单。根据Windows操作系统的标准，点击左下角的“开始按钮”可以打开开始菜单。这个按钮通常位于屏幕底部左侧，并且是一个带有Windows标志的圆形图标。\n\n### Action ###\n{\"action\": \"click\", \"coordinate\": [35, 1074]}\n\n### Description ###\n点击屏幕底部左侧的“开始按钮”，这将打开Windows的开始菜单，从而允许我们接下来搜索并打开计算器应用。"
                                            }
                                        ],
                                        "role": "assistant"
                                    }
                                ],
                                "name": "operator",
                                "response": "### Thought ###\n为了打开计算器，我需要首先打开开始菜单。根据Windows操作系统的标准，点击左下角的“开始按钮”可以打开开始菜单。这个按钮通常位于屏幕底部左侧，并且是一个带有Windows标志的圆形图标。\n\n### Action ###\n{\"action\": \"click\", \"coordinate\": [35, 1074]}\n\n### Description ###\n点击屏幕底部左侧的“开始按钮”，这将打开Windows的开始菜单，从而允许我们接下来搜索并打开计算器应用。"
                            },
                            "manager": {
                                "messages": [
                                    {
                                        "content": [
                                            {
                                                "text": "You are a helpful assistant.",
                                                "type": "text"
                                            }
                                        ],
                                        "role": "system"
                                    },
                                    {
                                        "content": [
                                            {
                                                "text": "You are an agent who can operate a windows computer on behalf of a user. Your goal is to track progress and devise high-level plans to achieve the user's requests.\n\n### User Request ###\n打开计算器\nYou can follow these tips:\n\nOn Windows, you absolutely have to double-click to open any desktop icon or folder in File Explorer—one single click will NOT open them. Always double-click.\n\n---\nMake a high-level plan to achieve the user's request. If the request is complex, break it down into subgoals. The screenshot displays the starting state of the computer.\n请返回中文。\n\n##### Important Notes #####\n1. Before generating your plan, carefully observe and understand the current state of the computer.\n2. Your plan should contain only necessary steps; however, please include information useful for executing the subgoal in the 'info' field.\n3. Do not include verification steps in your plan. Steps that confirm or validate other subtasks should not be included.\n4. Do not include optional steps in your plan.\n\nProvide your output in the following format which contains three parts:\n\n### Thought ###\nA detailed explanation of your rationale for the plan and subgoals.\n\n### Plan ###\n1. {'name': 'brief description of the first subgoal.', 'info': 'detailed information about executing the first subgoal.'}\n2. {'name': 'brief description of the second subgoal.', 'info': 'detailed information about executing the second subgoal.'}\n...\n\n### Current Subgoal ###\nThe first subgoal's name you should work on.\n\n"
                                            },
                                            {
                                                "image": "C:\\Usersimages\\b5bf3eff-ae32-4dd0-85ee-7ee31c359142.png"
                                            }
                                        ],
                                        "role": "user"
                                    },
                                    {
                                        "content": [
                                            {
                                                "text": "### Thought ###\nThe user wants to open the calculator application. The screenshot shows the Windows desktop with various icons, but the calculator icon is not immediately visible. To achieve this, I need to locate and open the calculator. Since it's not on the desktop, I'll assume it might be in the Start menu or another location like the All Apps menu. Therefore, the plan involves accessing the Start menu and finding the calculator there.\n\n### Plan ###\n1. {'name': 'Open the Start Menu', 'info': 'Click on the Start button located at the bottom left corner of the screen to open the Start menu.'}\n2. {'name': 'Locate Calculator', 'info': 'In the Start menu, scroll through the list of applications or use the search bar at the top to find \"Calculator\".'}\n\n### Current Subgoal ###\nOpen the Start Menu"
                                            }
                                        ],
                                        "role": "assistant"
                                    }
                                ],
                                "name": "manager",
                                "response": "### Thought ###\nThe user wants to open the calculator application. The screenshot shows the Windows desktop with various icons, but the calculator icon is not immediately visible. To achieve this, I need to locate and open the calculator. Since it's not on the desktop, I'll assume it might be in the Start menu or another location like the All Apps menu. Therefore, the plan involves accessing the Start menu and finding the calculator there.\n\n### Plan ###\n1. {'name': 'Open the Start Menu', 'info': 'Click on the Start button located at the bottom left corner of the screen to open the Start menu.'}\n2. {'name': 'Locate Calculator', 'info': 'In the Start menu, scroll through the list of applications or use the search bar at the top to find \"Calculator\".'}\n\n### Current Subgoal ###\nOpen the Start Menu"
                            }
                        },
                        "thought": "为了打开计算器，我需要首先打开开始菜单。根据Windows操作系统的标准，点击左下角的“开始按钮”可以打开开始菜单。这个按钮通常位于屏幕底部左侧，并且是一个带有Windows标志的圆形图标。\n\n"
                    },
                    "delta": false,
                    "object": "content",
                    "type": "data"
                }
            ],
            "id": "msg_e9dd72ea-19fc-4a22-93ee-d97588645f88",
            "message": "Success",
            "object": "message",
            "role": "assistant",
            "status": "Success",
            "type": "message"
        }
    ],
    "session_id": "bee1915d-6f4d-4bfc-b657-ecb9d0ed8dad",
    "status": "created"
}
```

## **使用限制与计费说明**

限时免费

## 状态码说明

大模型服务平台通用状态码详情，请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。
