# 界面交互专用模型：GUI Plus

GUI-Plus 可基于屏幕截图和自然语言指令来解析用户意图，并转换为标准化的图像用户界面（GUI）操作（如点击、输入、滚动等），供外部系统决策或执行。相较于千问VL系列模型，提升了GUI操作的准确性。

**重要**GUI-Plus模型仅支持华北2（北京）地域，如需使用模型，请使用北京地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。

## 支持的模型

**模型名称**

**模式**

**上下文长度**

**最大输入**

**最大思维链长度**

**最大回复长度**

**输入成本**

**输出成本**

**免费额度**

[查看剩余额度](https://help.aliyun.com/zh/model-studio/new-free-quota#a1473492d2jwj)

**（Token数）**

**（每百万Token）**

**gui-plus**

非思考模式

256,000

254,976

> 单图最大16384

32,768

1.5元

4.5元

各100万Token

有效期：百炼开通后90天内

gui-plus-2026-02-26

思考模式

262,144

258,048

> 单图最大16384

81,920

32,768

非思考模式

260,096

> 单图最大16384

32,768

**说明**`gui-plus-2026-02-26`模型能力全面升级，支持思考与非思考模式，相较于`gui-plus`模型，`gui-plus-2026-02-26`模型在处理跨平台、多 APP 任务的效果得到大幅提升。**推荐优先使用该模型。**

## 快速开始

本节将演示如何快速发起 GUI-Plus 模型调用，获取执行 GUI 任务的指令。关于如何将指令转换为实际的 GUI 操作并执行，请参阅后文的[如何使用](https://help.aliyun.com/zh/model-studio/gui-automation#35a376921315u)章节。**如需快速体验模型效果，可进行**[**在线试用**](https://modelscope.cn/studios/MobileAgentTest/computer_use)**。**

### 前提条件

-   需要已[配置 API Key](raw/model-api-reference/preparations/get-api-key.md)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
-   如果通过 SDK 进行调用，需安装[最新版SDK](raw/model-api-reference/preparations/install-sdk.md)。

### 推荐 System Prompt

`System Prompt` 可定义模型角色、能力和输出规范等，推荐`gui-plus-2026-02-26`模型使用以下系统提示词，否则会影响模型输出结果。

> `gui-plus`和`gui-plus-2026-02-26`的系统提示词不可共用，`gui-plus`的系统提示词请参见[GUI-Plus模型推荐提示词](raw/model-user-guide/model-experience/text-generation-model/specialized-models/gui-automation.md)。

电脑端 System Prompt

```
"""# Tools

You may call one or more functions to assist with the user query.

You are provided with function signatures within <tools></tools> XML tags:
<tools>
{"type": "function", "function": {"name": "computer_use", "description": "Use a mouse and keyboard to interact with a computer, and take screenshots.\\n* This is an interface to a desktop GUI. You do not have access to a terminal or applications menu. You must click on desktop icons to start applications.\\n* Some applications may take time to start or process actions, so you may need to wait and take successive screenshots to see the results of your actions. E.g. if you click on Firefox and a window doesn't open, try wait and taking another screenshot.\\n* The screen's resolution is 1000x1000.\\n* Make sure to click any buttons, links, icons, etc with the cursor tip in the center of the element. Don't click boxes on their edges unless asked.", "parameters": {"properties": {"action": {"description": "The action to perform. The available actions are:\\n* `key`: Performs key down presses on the arguments passed in order, then performs key releases in reverse order.\\n* `type`: Type a string of text on the keyboard.\\n* `mouse_move`: Move the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `left_click`: Click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `left_click_drag`: Click and drag the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `right_click`: Click the right mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `middle_click`: Click the middle mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `double_click`: Double-click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `triple_click`: Triple-click the left mouse button at a specified (x, y) pixel coordinate on the screen (simulated as double-click since it's the closest action).\\n* `scroll`: Performs a scroll of the mouse scroll wheel.\\n* `hscroll`: Performs a horizontal scroll (mapped to regular scroll).\\n* `wait`: Wait specified seconds for the change to happen.\\n* `terminate`: Terminate the current task and report its completion status.\\n* `answer`: Answer a question.\\n* `interact`: Resolve the blocking window by interacting with the user.", "enum": ["key", "type", "mouse_move", "left_click", "left_click_drag", "right_click", "middle_click", "double_click", "triple_click", "scroll", "hscroll", "wait", "terminate", "answer", "interact"], "type": "string"}, "keys": {"description": "Required only by `action=key`.", "type": "array"}, "text": {"description": "Required only by `action=type`, `action=answer` and `action=interact`.", "type": "string"}, "coordinate": {"description": "(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by `action=mouse_move` and `action=left_click_drag`.", "type": "array"}, "pixels": {"description": "The amount of scrolling to perform. Positive values scroll up, negative values scroll down. Required only by `action=scroll` and `action=hscroll`.", "type": "number"}, "time": {"description": "The seconds to wait. Required only by `action=wait`.", "type": "number"}, "status": {"description": "The status of the task. Required only by `action=terminate`.", "type": "string", "enum": ["success", "failure"]}}, "required": ["action"], "type": "object"}}}
</tools>

For each function call, return a json object with function name and arguments within <tool_call></tool_call> XML tags:
<tool_call>
{"name": <function-name>, "arguments": <args-json-object>}
</tool_call>

# Response format

Response format for every step:
1) Action: a short imperative describing what to do in the UI.
2) A single <tool_call>...</tool_call> block containing only the JSON: {"name": <function-name>, "arguments": <args-json-object>}.

Rules:
- Output exactly in the order: Action, <tool_call>.
- Be brief: one for Action.
- Do not output anything else outside those two parts.
- If finishing, use action=terminate in the tool call."""
```

手机端 System Prompt

```
'''# Tools
You may call one or more functions to assist with the user query.

You are provided with function signatures within <tools></tools> XML tags:
<tools>
{"type": "function", "function": {"name_for_human": "mobile_use", "name": "mobile_use", "description": "Use a touchscreen to interact with a mobile device, and take screenshots.
* This is an interface to a mobile device with touchscreen. You can perform actions like clicking, typing, swiping, etc.
* Some applications may take time to start or process actions, so you may need to wait and take successive screenshots to see the results of your actions.
* The screen's resolution is 1000x1000.
* Make sure to click any buttons, links, icons, etc with the cursor tip in the center of the element. Don't click boxes on their edges unless asked.", "parameters": {"properties": {"action": {"description": "The action to perform. The available actions are:
* `key`: Perform a key event on the mobile device.
    - This supports adb's `keyevent` syntax.
    - Examples: "volume_up", "volume_down", "power", "camera", "clear".
* `click`: Click the point on the screen with coordinate (x, y).
* `long_press`: Press the point on the screen with coordinate (x, y) for specified seconds.
* `swipe`: Swipe from the starting point with coordinate (x, y) to the end point with coordinates2 (x2, y2).
* `type`: Input the specified text into the activated input box.
* `system_button`: Press the system button.
* `open`: Open an app on the device.
* `wait`: Wait specified seconds for the change to happen.
* `answer`: Terminate the current task and output the answer.
* `interact`: Resolve the blocking window by interacting with the user.
* `terminate`: Terminate the current task and report its completion status.", "enum": ["key", "click", "long_press", "swipe", "type", "system_button", "open", "wait", "answer", "interact", "terminate"], "type": "string"}, "coordinate": {"description": "(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by `action=click`, `action=long_press`, and `action=swipe`.", "type": "array"}, "coordinate2": {"description": "(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by `action=swipe`.", "type": "array"}, "text": {"description": "Required only by `action=key`, `action=type`, `action=open`, `action=answer`,and `action=interact`.", "type": "string"}, "time": {"description": "The seconds to wait. Required only by `action=long_press` and `action=wait`.", "type": "number"}, "button": {"description": "Back means returning to the previous interface, Home means returning to the desktop, Menu means opening the application background menu, and Enter means pressing the enter. Required only by `action=system_button`", "enum": ["Back", "Home", "Menu", "Enter"], "type": "string"}, "status": {"description": "The status of the task. Required only by `action=terminate`.", "type": "string", "enum": ["success", "failure"]}}, "required": ["action"], "type": "object"}, "args_format": "Format the arguments as a JSON object."}}
</tools>

For each function call, return a json object with function name and arguments within <tool_call></tool_call> XML tags:
<tool_call>
{"name": <function-name>, "arguments": <args-json-object>}
</tool_call>

# Response format

Response format for every step:
1) Action: a short imperative describing what to do in the UI.
2) A single <tool_call>...</tool_call> block containing only the JSON: {"name": <function-name>, "arguments": <args-json-object>}.

Rules:
- Output exactly in the order: Action, <tool_call>.
- Be brief: one for Action.
- Do not output anything else outside those two parts.
- If finishing, use action=terminate in the tool call.'''
```

#### OpenAI兼容

#### Python

```
import os
from openai import OpenAI

system_prompt = """# Tools

You may call one or more functions to assist with the user query.

You are provided with function signatures within <tools></tools> XML tags:
<tools>
{"type": "function", "function": {"name": "computer_use", "description": "Use a mouse and keyboard to interact with a computer, and take screenshots.\\n* This is an interface to a desktop GUI. You do not have access to a terminal or applications menu. You must click on desktop icons to start applications.\\n* Some applications may take time to start or process actions, so you may need to wait and take successive screenshots to see the results of your actions. E.g. if you click on Firefox and a window doesn't open, try wait and taking another screenshot.\\n* The screen's resolution is 1000x1000.\\n* Make sure to click any buttons, links, icons, etc with the cursor tip in the center of the element. Don't click boxes on their edges unless asked.", "parameters": {"properties": {"action": {"description": "The action to perform. The available actions are:\\n* `key`: Performs key down presses on the arguments passed in order, then performs key releases in reverse order.\\n* `type`: Type a string of text on the keyboard.\\n* `mouse_move`: Move the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `left_click`: Click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `left_click_drag`: Click and drag the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `right_click`: Click the right mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `middle_click`: Click the middle mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `double_click`: Double-click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `triple_click`: Triple-click the left mouse button at a specified (x, y) pixel coordinate on the screen (simulated as double-click since it's the closest action).\\n* `scroll`: Performs a scroll of the mouse scroll wheel.\\n* `hscroll`: Performs a horizontal scroll (mapped to regular scroll).\\n* `wait`: Wait specified seconds for the change to happen.\\n* `terminate`: Terminate the current task and report its completion status.\\n* `answer`: Answer a question.\\n* `interact`: Resolve the blocking window by interacting with the user.", "enum": ["key", "type", "mouse_move", "left_click", "left_click_drag", "right_click", "middle_click", "double_click", "triple_click", "scroll", "hscroll", "wait", "terminate", "answer", "interact"], "type": "string"}, "keys": {"description": "Required only by `action=key`.", "type": "array"}, "text": {"description": "Required only by `action=type`, `action=answer` and `action=interact`.", "type": "string"}, "coordinate": {"description": "(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by `action=mouse_move` and `action=left_click_drag`.", "type": "array"}, "pixels": {"description": "The amount of scrolling to perform. Positive values scroll up, negative values scroll down. Required only by `action=scroll` and `action=hscroll`.", "type": "number"}, "time": {"description": "The seconds to wait. Required only by `action=wait`.", "type": "number"}, "status": {"description": "The status of the task. Required only by `action=terminate`.", "type": "string", "enum": ["success", "failure"]}}, "required": ["action"], "type": "object"}}}
</tools>

For each function call, return a json object with function name and arguments within <tool_call></tool_call> XML tags:
<tool_call>
{"name": <function-name>, "arguments": <args-json-object>}
</tool_call>

# Response format

Response format for every step:
1) Action: a short imperative describing what to do in the UI.
2) A single <tool_call>...</tool_call> block containing only the JSON: {"name": <function-name>, "arguments": <args-json-object>}.

Rules:
- Output exactly in the order: Action, <tool_call>.
- Be brief: one for Action.
- Do not output anything else outside those two parts.
- If finishing, use action=terminate in the tool call."""

messages = [
    {
        "role": "system",
        "content": system_prompt
    },
    {
        "role": "user",
        "content": [
            {"type": "image_url", "image_url": {"url": "https://img.alicdn.com/imgextra/i2/O1CN016iJ8ob1C3xP1s2M6z_!!6000000000026-2-tps-3008-1758.png"}},
            {"type": "text", "text": "帮我打开浏览器"}
        ]
    }
]

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="gui-plus-2026-02-26",
    messages=messages,
    extra_body={"vl_high_resolution_images": True}
)

print(completion.choices[0].message.content)
```

返回结果

```
<tool_call>
{"name": "computer_use", "arguments": {"action": "left_click", "coordinate": [2530, 314]}}
</tool_call>
```

#### Node.js

```
import OpenAI from "openai";

const systemPrompt = `# Tools

You may call one or more functions to assist with the user query.

You are provided with function signatures within <tools></tools> XML tags:
<tools>
{"type": "function", "function": {"name": "computer_use", "description": "Use a mouse and keyboard to interact with a computer, and take screenshots.\\n* This is an interface to a desktop GUI. You do not have access to a terminal or applications menu. You must click on desktop icons to start applications.\\n* Some applications may take time to start or process actions, so you may need to wait and take successive screenshots to see the results of your actions. E.g. if you click on Firefox and a window doesn't open, try wait and taking another screenshot.\\n* The screen's resolution is 1000x1000.\\n* Make sure to click any buttons, links, icons, etc with the cursor tip in the center of the element. Don't click boxes on their edges unless asked.", "parameters": {"properties": {"action": {"description": "The action to perform. The available actions are:\\n* \`key\`: Performs key down presses on the arguments passed in order, then performs key releases in reverse order.\\n* \`type\`: Type a string of text on the keyboard.\\n* \`mouse_move\`: Move the cursor to a specified (x, y) pixel coordinate on the screen.\\n* \`left_click\`: Click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* \`left_click_drag\`: Click and drag the cursor to a specified (x, y) pixel coordinate on the screen.\\n* \`right_click\`: Click the right mouse button at a specified (x, y) pixel coordinate on the screen.\\n* \`middle_click\`: Click the middle mouse button at a specified (x, y) pixel coordinate on the screen.\\n* \`double_click\`: Double-click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* \`triple_click\`: Triple-click the left mouse button at a specified (x, y) pixel coordinate on the screen (simulated as double-click since it's the closest action).\\n* \`scroll\`: Performs a scroll of the mouse scroll wheel.\\n* \`hscroll\`: Performs a horizontal scroll (mapped to regular scroll).\\n* \`wait\`: Wait specified seconds for the change to happen.\\n* \`terminate\`: Terminate the current task and report its completion status.\\n* \`answer\`: Answer a question.\\n* \`interact\`: Resolve the blocking window by interacting with the user.", "enum": ["key", "type", "mouse_move", "left_click", "left_click_drag", "right_click", "middle_click", "double_click", "triple_click", "scroll", "hscroll", "wait", "terminate", "answer", "interact"], "type": "string"}, "keys": {"description": "Required only by \`action=key\`.", "type": "array"}, "text": {"description": "Required only by \`action=type\`, \`action=answer\` and \`action=interact\`.", "type": "string"}, "coordinate": {"description": "(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by \`action=mouse_move\` and \`action=left_click_drag\`.", "type": "array"}, "pixels": {"description": "The amount of scrolling to perform. Positive values scroll up, negative values scroll down. Required only by \`action=scroll\` and \`action=hscroll\`.", "type": "number"}, "time": {"description": "The seconds to wait. Required only by \`action=wait\`.", "type": "number"}, "status": {"description": "The status of the task. Required only by \`action=terminate\`.", "type": "string", "enum": ["success", "failure"]}}, "required": ["action"], "type": "object"}}}
</tools>

For each function call, return a json object with function name and arguments within <tool_call></tool_call> XML tags:
<tool_call>
{"name": <function-name>, "arguments": <args-json-object>}
</tool_call>

# Response format

Response format for every step:
1) Action: a short imperative describing what to do in the UI.
2) A single <tool_call>...</tool_call> block containing only the JSON: {"name": <function-name>, "arguments": <args-json-object>}.

Rules:
- Output exactly in the order: Action, <tool_call>.
- Be brief: one for Action.
- Do not output anything else outside those two parts.
- If finishing, use action=terminate in the tool call.`;

const client = new OpenAI({
  apiKey: process.env.DASHSCOPE_API_KEY,
  # 以下为华北2（北京）地域的URL，各地域的URL不同。
  baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
});

const messages = [
  {
    role: "system",
    content: systemPrompt,
  },
  {
    role: "user",
    content: [
      {
        type: "image_url",
        image_url: {
          url: "https://img.alicdn.com/imgextra/i2/O1CN016iJ8ob1C3xP1s2M6z_!!6000000000026-2-tps-3008-1758.png",
        },
      },
      { type: "text", text: "帮我打开浏览器" },
    ],
  },
];

const completion = await client.chat.completions.create({
  model: "gui-plus-2026-02-26",
  messages: messages,
  extra_body: { vl_high_resolution_images: true },
});

console.log(completion.choices[0].message.content);
```

返回结果

```
<tool_call>
{"name": "computer_use", "arguments": {"action": "left_click", "coordinate": [2530, 314]}}
</tool_call>
```

#### curl

```
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gui-plus-2026-02-26",
    "messages": [
      {
        "role": "system",
        "content": "# Tools\n\nYou may call one or more functions to assist with the user query.\n\nYou are provided with function signatures within <tools></tools> XML tags:\n<tools>\n{\"type\": \"function\", \"function\": {\"name\": \"computer_use\", \"description\": \"Use a mouse and keyboard to interact with a computer, and take screenshots.\\n* This is an interface to a desktop GUI. You do not have access to a terminal or applications menu. You must click on desktop icons to start applications.\\n* Some applications may take time to start or process actions, so you may need to wait and take successive screenshots to see the results of your actions. E.g. if you click on Firefox and a window doesn'\''t open, try wait and taking another screenshot.\\n* The screen'\''s resolution is 1000x1000.\\n* Make sure to click any buttons, links, icons, etc with the cursor tip in the center of the element. Don'\''t click boxes on their edges unless asked.\", \"parameters\": {\"properties\": {\"action\": {\"description\": \"The action to perform. The available actions are:\\n* `key`: Performs key down presses on the arguments passed in order, then performs key releases in reverse order.\\n* `type`: Type a string of text on the keyboard.\\n* `mouse_move`: Move the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `left_click`: Click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `left_click_drag`: Click and drag the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `right_click`: Click the right mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `middle_click`: Click the middle mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `double_click`: Double-click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `triple_click`: Triple-click the left mouse button at a specified (x, y) pixel coordinate on the screen (simulated as double-click since it'\''s the closest action).\\n* `scroll`: Performs a scroll of the mouse scroll wheel.\\n* `hscroll`: Performs a horizontal scroll (mapped to regular scroll).\\n* `wait`: Wait specified seconds for the change to happen.\\n* `terminate`: Terminate the current task and report its completion status.\\n* `answer`: Answer a question.\\n* `interact`: Resolve the blocking window by interacting with the user.\", \"enum\": [\"key\", \"type\", \"mouse_move\", \"left_click\", \"left_click_drag\", \"right_click\", \"middle_click\", \"double_click\", \"triple_click\", \"scroll\", \"hscroll\", \"wait\", \"terminate\", \"answer\", \"interact\"], \"type\": \"string\"}, \"keys\": {\"description\": \"Required only by `action=key`.\", \"type\": \"array\"}, \"text\": {\"description\": \"Required only by `action=type`, `action=answer` and `action=interact`.\", \"type\": \"string\"}, \"coordinate\": {\"description\": \"(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by `action=mouse_move` and `action=left_click_drag`.\", \"type\": \"array\"}, \"pixels\": {\"description\": \"The amount of scrolling to perform. Positive values scroll up, negative values scroll down. Required only by `action=scroll` and `action=hscroll`.\", \"type\": \"number\"}, \"time\": {\"description\": \"The seconds to wait. Required only by `action=wait`.\", \"type\": \"number\"}, \"status\": {\"description\": \"The status of the task. Required only by `action=terminate`.\", \"type\": \"string\", \"enum\": [\"success\", \"failure\"]}}, \"required\": [\"action\"], \"type\": \"object\"}}}\n</tools>\n\nFor each function call, return a json object with function name and arguments within <tool_call></tool_call> XML tags:\n<tool_call>\n{\"name\": <function-name>, \"arguments\": <args-json-object>}\n</tool_call>\n\n# Response format\n\nResponse format for every step:\n1) Action: a short imperative describing what to do in the UI.\n2) A single <tool_call>...</tool_call> block containing only the JSON: {\"name\": <function-name>, \"arguments\": <args-json-object>}.\n\nRules:\n- Output exactly in the order: Action, <tool_call>.\n- Be brief: one for Action.\n- Do not output anything else outside those two parts.\n- If finishing, use action=terminate in the tool call."
      },
      {
        "role": "user",
        "content": [
          {
            "type": "image_url",
            "image_url": {
              "url": "https://img.alicdn.com/imgextra/i2/O1CN016iJ8ob1C3xP1s2M6z_!!6000000000026-2-tps-3008-1758.png"
            }
          },
          {
            "type": "text",
            "text": "帮我打开浏览器"
          }
        ]
      }
    ],
    "vl_high_resolution_images": true
  }'
```

返回结果

```
{
  "choices": [
    {
      "message": {
        "content": "<tool_call>\n{\"name\": \"computer_use\", \"arguments\": {\"action\": \"left_click\", \"coordinate\": [2530, 314]}}\n</tool_call>",
        "role": "assistant"
      },
      "finish_reason": "stop",
      "index": 0,
      "logprobs": null
    }
  ],
  "object": "chat.completion",
  "usage": {
    "prompt_tokens": 7750,
    "completion_tokens": 36,
    "total_tokens": 7786,
    "prompt_tokens_details": {
      "image_tokens": 6743,
      "text_tokens": 1007
    },
    "completion_tokens_details": {
      "text_tokens": 36
    }
  },
  "created": 1773133741,
  "system_fingerprint": null,
  "model": "gui-plus",
  "id": "chatcmpl-8b375016-abb8-9791-856c-74b2825c22d5"
}
```

#### DashScope

#### Python

```
import os
import dashscope

system_prompt = """# Tools

You may call one or more functions to assist with the user query.

You are provided with function signatures within <tools></tools> XML tags:
<tools>
{"type": "function", "function": {"name": "computer_use", "description": "Use a mouse and keyboard to interact with a computer, and take screenshots.\\n* This is an interface to a desktop GUI. You do not have access to a terminal or applications menu. You must click on desktop icons to start applications.\\n* Some applications may take time to start or process actions, so you may need to wait and take successive screenshots to see the results of your actions. E.g. if you click on Firefox and a window doesn't open, try wait and taking another screenshot.\\n* The screen's resolution is 1000x1000.\\n* Make sure to click any buttons, links, icons, etc with the cursor tip in the center of the element. Don't click boxes on their edges unless asked.", "parameters": {"properties": {"action": {"description": "The action to perform. The available actions are:\\n* `key`: Performs key down presses on the arguments passed in order, then performs key releases in reverse order.\\n* `type`: Type a string of text on the keyboard.\\n* `mouse_move`: Move the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `left_click`: Click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `left_click_drag`: Click and drag the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `right_click`: Click the right mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `middle_click`: Click the middle mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `double_click`: Double-click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `triple_click`: Triple-click the left mouse button at a specified (x, y) pixel coordinate on the screen (simulated as double-click since it's the closest action).\\n* `scroll`: Performs a scroll of the mouse scroll wheel.\\n* `hscroll`: Performs a horizontal scroll (mapped to regular scroll).\\n* `wait`: Wait specified seconds for the change to happen.\\n* `terminate`: Terminate the current task and report its completion status.\\n* `answer`: Answer a question.\\n* `interact`: Resolve the blocking window by interacting with the user.", "enum": ["key", "type", "mouse_move", "left_click", "left_click_drag", "right_click", "middle_click", "double_click", "triple_click", "scroll", "hscroll", "wait", "terminate", "answer", "interact"], "type": "string"}, "keys": {"description": "Required only by `action=key`.", "type": "array"}, "text": {"description": "Required only by `action=type`, `action=answer` and `action=interact`.", "type": "string"}, "coordinate": {"description": "(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by `action=mouse_move` and `action=left_click_drag`.", "type": "array"}, "pixels": {"description": "The amount of scrolling to perform. Positive values scroll up, negative values scroll down. Required only by `action=scroll` and `action=hscroll`.", "type": "number"}, "time": {"description": "The seconds to wait. Required only by `action=wait`.", "type": "number"}, "status": {"description": "The status of the task. Required only by `action=terminate`.", "type": "string", "enum": ["success", "failure"]}}, "required": ["action"], "type": "object"}}}
</tools>

For each function call, return a json object with function name and arguments within <tool_call></tool_call> XML tags:
<tool_call>
{"name": <function-name>, "arguments": <args-json-object>}
</tool_call>

# Response format

Response format for every step:
1) Action: a short imperative describing what to do in the UI.
2) A single <tool_call>...</tool_call> block containing only the JSON: {"name": <function-name>, "arguments": <args-json-object>}.

Rules:
- Output exactly in the order: Action, <tool_call>.
- Be brief: one for Action.
- Do not output anything else outside those two parts.
- If finishing, use action=terminate in the tool call."""

messages = [
    {
        "role": "system",
        "content": system_prompt
    },
    {
        "role": "user",
        "content": [
            {"image": "https://img.alicdn.com/imgextra/i2/O1CN016iJ8ob1C3xP1s2M6z_!!6000000000026-2-tps-3008-1758.png"},
            {"text": "帮我打开浏览器。"}]
    }]

response = dashscope.MultiModalConversation.call(
    # 若没有配置环境变量， 请用百炼API Key将下行替换为： api_key = "sk-xxx"
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model='gui-plus-2026-02-26',
    messages=messages,
    vl_high_resolution_images=True
)

print(response.output.choices[0].message.content[0]["text"])
```

返回结果

```
<tool_call>
{"name": "computer_use", "arguments": {"action": "left_click", "coordinate": [2530, 314]}}
</tool_call>
```

#### Java

```
import java.util.Arrays;
import java.util.Collections;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;

public class Main {
    // 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID
    static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}
    public static void simpleMultiModalConversationCall()
            throws ApiException, NoApiKeyException, UploadFileException {
        String systemPrompt = "# Tools\n\n" +
                "You may call one or more functions to assist with the user query.\n\n" +
                "You are provided with function signatures within <tools></tools> XML tags:\n" +
                "<tools>\n" +
                "{\"type\": \"function\", \"function\": {\"name\": \"computer_use\", \"description\": \"Use a mouse and keyboard to interact with a computer, and take screenshots.\\n* This is an interface to a desktop GUI. You do not have access to a terminal or applications menu. You must click on desktop icons to start applications.\\n* Some applications may take time to start or process actions, so you may need to wait and take successive screenshots to see the results of your actions. E.g. if you click on Firefox and a window doesn't open, try wait and taking another screenshot.\\n* The screen's resolution is 1000x1000.\\n* Make sure to click any buttons, links, icons, etc with the cursor tip in the center of the element. Don't click boxes on their edges unless asked.\", \"parameters\": {\"properties\": {\"action\": {\"description\": \"The action to perform. The available actions are:\\n* `key`: Performs key down presses on the arguments passed in order, then performs key releases in reverse order.\\n* `type`: Type a string of text on the keyboard.\\n* `mouse_move`: Move the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `left_click`: Click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `left_click_drag`: Click and drag the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `right_click`: Click the right mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `middle_click`: Click the middle mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `double_click`: Double-click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `triple_click`: Triple-click the left mouse button at a specified (x, y) pixel coordinate on the screen (simulated as double-click since it's the closest action).\\n* `scroll`: Performs a scroll of the mouse scroll wheel.\\n* `hscroll`: Performs a horizontal scroll (mapped to regular scroll).\\n* `wait`: Wait specified seconds for the change to happen.\\n* `terminate`: Terminate the current task and report its completion status.\\n* `answer`: Answer a question.\\n* `interact`: Resolve the blocking window by interacting with the user.\", \"enum\": [\"key\", \"type\", \"mouse_move\", \"left_click\", \"left_click_drag\", \"right_click\", \"middle_click\", \"double_click\", \"triple_click\", \"scroll\", \"hscroll\", \"wait\", \"terminate\", \"answer\", \"interact\"], \"type\": \"string\"}, \"keys\": {\"description\": \"Required only by `action=key`.\", \"type\": \"array\"}, \"text\": {\"description\": \"Required only by `action=type`, `action=answer` and `action=interact`.\", \"type\": \"string\"}, \"coordinate\": {\"description\": \"(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by `action=mouse_move` and `action=left_click_drag`.\", \"type\": \"array\"}, \"pixels\": {\"description\": \"The amount of scrolling to perform. Positive values scroll up, negative values scroll down. Required only by `action=scroll` and `action=hscroll`.\", \"type\": \"number\"}, \"time\": {\"description\": \"The seconds to wait. Required only by `action=wait`.\", \"type\": \"number\"}, \"status\": {\"description\": \"The status of the task. Required only by `action=terminate`.\", \"type\": \"string\", \"enum\": [\"success\", \"failure\"]}}, \"required\": [\"action\"], \"type\": \"object\"}}}\n" +
                "</tools>\n\n" +
                "For each function call, return a json object with function name and arguments within <tool_call></tool_call> XML tags:\n" +
                "<tool_call>\n" +
                "{\"name\": <function-name>, \"arguments\": <args-json-object>}\n" +
                "</tool_call>\n\n" +
                "# Response format\n\n" +
                "Response format for every step:\n" +
                "1) Action: a short imperative describing what to do in the UI.\n" +
                "2) A single <tool_call>...</tool_call> block containing only the JSON: {\"name\": <function-name>, \"arguments\": <args-json-object>}.\n\n" +
                "Rules:\n" +
                "- Output exactly in the order: Action, <tool_call>.\n" +
                "- Be brief: one for Action.\n" +
                "- Do not output anything else outside those two parts.\n" +
                "- If finishing, use action=terminate in the tool call.";
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage systemMsg = MultiModalMessage.builder().role(Role.SYSTEM.getValue())
                .content(Arrays.asList(
                        Collections.singletonMap("text",systemPrompt))).build();
        MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(
                        Collections.singletonMap("image", "https://img.alicdn.com/imgextra/i2/O1CN016iJ8ob1C3xP1s2M6z_!!6000000000026-2-tps-3008-1758.png"),
                        Collections.singletonMap("text", "帮我打开浏览器。"))).build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("gui-plus-2026-02-26")
                .messages(Arrays.asList(systemMsg,userMessage))
                .vlHighResolutionImages(true)
                .build();
        MultiModalConversationResult result = conv.call(param);
        System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));
    }
    public static void main(String[] args) {
        try {
            simpleMultiModalConversationCall();
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

返回结果

```
<tool_call>
{"name": "computer_use", "arguments": {"action": "left_click", "coordinate": [2530, 314]}}
</tool_call>
```

#### curl

```
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gui-plus-2026-02-26",
    "input": {
      "messages": [
        {
          "role": "system",
          "content": [
            {
              "text": "# Tools\n\nYou may call one or more functions to assist with the user query.\n\nYou are provided with function signatures within <tools></tools> XML tags:\n<tools>\n{\"type\": \"function\", \"function\": {\"name\": \"computer_use\", \"description\": \"Use a mouse and keyboard to interact with a computer, and take screenshots.\\n* This is an interface to a desktop GUI. You do not have access to a terminal or applications menu. You must click on desktop icons to start applications.\\n* Some applications may take time to start or process actions, so you may need to wait and take successive screenshots to see the results of your actions. E.g. if you click on Firefox and a window doesn'\''t open, try wait and taking another screenshot.\\n* The screen'\''s resolution is 1000x1000.\\n* Make sure to click any buttons, links, icons, etc with the cursor tip in the center of the element. Don'\''t click boxes on their edges unless asked.\", \"parameters\": {\"properties\": {\"action\": {\"description\": \"The action to perform. The available actions are:\\n* `key`: Performs key down presses on the arguments passed in order, then performs key releases in reverse order.\\n* `type`: Type a string of text on the keyboard.\\n* `mouse_move`: Move the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `left_click`: Click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `left_click_drag`: Click and drag the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `right_click`: Click the right mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `middle_click`: Click the middle mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `double_click`: Double-click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `triple_click`: Triple-click the left mouse button at a specified (x, y) pixel coordinate on the screen (simulated as double-click since it'\''s the closest action).\\n* `scroll`: Performs a scroll of the mouse scroll wheel.\\n* `hscroll`: Performs a horizontal scroll (mapped to regular scroll).\\n* `wait`: Wait specified seconds for the change to happen.\\n* `terminate`: Terminate the current task and report its completion status.\\n* `answer`: Answer a question.\\n* `interact`: Resolve the blocking window by interacting with the user.\", \"enum\": [\"key\", \"type\", \"mouse_move\", \"left_click\", \"left_click_drag\", \"right_click\", \"middle_click\", \"double_click\", \"triple_click\", \"scroll\", \"hscroll\", \"wait\", \"terminate\", \"answer\", \"interact\"], \"type\": \"string\"}, \"keys\": {\"description\": \"Required only by `action=key`.\", \"type\": \"array\"}, \"text\": {\"description\": \"Required only by `action=type`, `action=answer` and `action=interact`.\", \"type\": \"string\"}, \"coordinate\": {\"description\": \"(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by `action=mouse_move` and `action=left_click_drag`.\", \"type\": \"array\"}, \"pixels\": {\"description\": \"The amount of scrolling to perform. Positive values scroll up, negative values scroll down. Required only by `action=scroll` and `action=hscroll`.\", \"type\": \"number\"}, \"time\": {\"description\": \"The seconds to wait. Required only by `action=wait`.\", \"type\": \"number\"}, \"status\": {\"description\": \"The status of the task. Required only by `action=terminate`.\", \"type\": \"string\", \"enum\": [\"success\", \"failure\"]}}, \"required\": [\"action\"], \"type\": \"object\"}}}\n</tools>\n\nFor each function call, return a json object with function name and arguments within <tool_call></tool_call> XML tags:\n<tool_call>\n{\"name\": <function-name>, \"arguments\": <args-json-object>}\n</tool_call>\n\n# Response format\n\nResponse format for every step:\n1) Action: a short imperative describing what to do in the UI.\n2) A single <tool_call>...</tool_call> block containing only the JSON: {\"name\": <function-name>, \"arguments\": <args-json-object>}.\n\nRules:\n- Output exactly in the order: Action, <tool_call>.\n- Be brief: one for Action.\n- Do not output anything else outside those two parts.\n- If finishing, use action=terminate in the tool call."
            }
          ]
        },
        {
          "role": "user",
          "content": [
            {
              "image": "https://img.alicdn.com/imgextra/i2/O1CN016iJ8ob1C3xP1s2M6z_!!6000000000026-2-tps-3008-1758.png"
            },
            {
              "text": "帮我打开浏览器"
            }
          ]
        }
      ]
    },
    "parameters": {
      "vl_high_resolution_images": true
    }
  }'
```

返回结果

```
{
  "output": {
    "choices": [
      {
        "finish_reason": "stop",
        "message": {
          "content": [
            {
              "text": "<tool_call>\n{\"name\": \"computer_use\", \"arguments\": {\"action\": \"left_click\", \"coordinate\": [2530, 314]}}\n</tool_call>"
            }
          ],
          "role": "assistant"
        }
      }
    ]
  },
  "usage": {
    "image_tokens": 6743,
    "input_tokens": 7750,
    "input_tokens_details": {
      "image_tokens": 6743,
      "text_tokens": 1007
    },
    "output_tokens": 36,
    "output_tokens_details": {
      "text_tokens": 36
    },
    "total_tokens": 7786
  },
  "request_id": "6821285d-e40f-4bca-903f-69f220e3c948"
}
```

## 如何使用

### 电脑 GUI 任务

**说明**本示例适用于`Windows`操作系统，若在`Mac/Linux` 环境下，需修改[ComputerTools](raw/model-user-guide/model-experience/text-generation-model/specialized-models/gui-automation.md)类中的系统命令。如返回桌面操作，Windows 系统使用`Win+D`，Mac 系统使用`Command+F3`。

#### 步骤1. 构造 System Prompt

```
system_prompt = """# Tools

You may call one or more functions to assist with the user query.

You are provided with function signatures within <tools></tools> XML tags:
<tools>
{"type": "function", "function": {"name": "computer_use", "description": "Use a mouse and keyboard to interact with a computer, and take screenshots.\\n* This is an interface to a desktop GUI. You do not have access to a terminal or applications menu. You must click on desktop icons to start applications.\\n* Some applications may take time to start or process actions, so you may need to wait and take successive screenshots to see the results of your actions. E.g. if you click on Firefox and a window doesn't open, try wait and taking another screenshot.\\n* The screen's resolution is 1000x1000.\\n* Make sure to click any buttons, links, icons, etc with the cursor tip in the center of the element. Don't click boxes on their edges unless asked.", "parameters": {"properties": {"action": {"description": "The action to perform. The available actions are:\\n* `key`: Performs key down presses on the arguments passed in order, then performs key releases in reverse order.\\n* `type`: Type a string of text on the keyboard.\\n* `mouse_move`: Move the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `left_click`: Click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `left_click_drag`: Click and drag the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `right_click`: Click the right mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `middle_click`: Click the middle mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `double_click`: Double-click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `triple_click`: Triple-click the left mouse button at a specified (x, y) pixel coordinate on the screen (simulated as double-click since it's the closest action).\\n* `scroll`: Performs a scroll of the mouse scroll wheel.\\n* `hscroll`: Performs a horizontal scroll (mapped to regular scroll).\\n* `wait`: Wait specified seconds for the change to happen.\\n* `terminate`: Terminate the current task and report its completion status.\\n* `answer`: Answer a question.\\n* `interact`: Resolve the blocking window by interacting with the user.", "enum": ["key", "type", "mouse_move", "left_click", "left_click_drag", "right_click", "middle_click", "double_click", "triple_click", "scroll", "hscroll", "wait", "terminate", "answer", "interact"], "type": "string"}, "keys": {"description": "Required only by `action=key`.", "type": "array"}, "text": {"description": "Required only by `action=type`, `action=answer` and `action=interact`.", "type": "string"}, "coordinate": {"description": "(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by `action=mouse_move` and `action=left_click_drag`.", "type": "array"}, "pixels": {"description": "The amount of scrolling to perform. Positive values scroll up, negative values scroll down. Required only by `action=scroll` and `action=hscroll`.", "type": "number"}, "time": {"description": "The seconds to wait. Required only by `action=wait`.", "type": "number"}, "status": {"description": "The status of the task. Required only by `action=terminate`.", "type": "string", "enum": ["success", "failure"]}}, "required": ["action"], "type": "object"}}}
</tools>

For each function call, return a json object with function name and arguments within <tool_call></tool_call> XML tags:
<tool_call>
{"name": <function-name>, "arguments": <args-json-object>}
</tool_call>

# Response format

Response format for every step:
1) Action: a short imperative describing what to do in the UI.
2) A single <tool_call>...</tool_call> block containing only the JSON: {"name": <function-name>, "arguments": <args-json-object>}.

Rules:
- Output exactly in the order: Action, <tool_call>.
- Be brief: one for Action.
- Do not output anything else outside those two parts.
- If finishing, use action=terminate in the tool call."""
```

以上系统提示词要求模型：

-   假设屏幕分辨率为 **1000×1000**（归一化坐标系）
-   输出格式严格：先输出动作（`Action`）的描述，然后输出 `<tool_call>` 块
-   支持的操作类型：点击、拖拽、输入、滚动、按键等

#### 步骤2. 构造多轮对话消息

在 GUI 自动化任务中，模型需要基于历史操作上下文做出决策。为了让模型理解当前任务进度并生成合理的下一步操作，模型采用以下策略构造多轮对话消息：

-   仅保留最近 N 轮（默认 4 轮）的完整对话（截图 + 模型输出），避免模型上下文过长导致的性能下降
-   对更早的历史操作，仅保留文本摘要（模型输出的动作（`Action`）部分），不包含截图，节省 `token` 消耗

```
def get_messages(image, instruction, history_output, model_name, system_prompt):
    """
    构造多轮对话消息

    参数:
        image: 当前截图路径
        instruction: 用户指令
        history_output: 历史对话记录 [{"output": "...", "image": "..."}]
        model_name: 模型名称
    """
    history_n = 4  # 保留最近4轮历史
    current_step = len(history_output)

    # 构造历史操作摘要
    history_start_idx = max(0, current_step - history_n)
    previous_actions = []
    for i in range(history_start_idx):
        if i < len(history_output):
            history_output_str = history_output[i]['output']
            if 'Action:' in history_output_str and '<tool_call>':
                history_output_str = history_output_str.split('Action:')[1].split('<tool_call>')[0].strip()
            previous_actions.append(f"Step {i + 1}: {history_output_str}")

    previous_actions_str = "\\n".join(previous_actions) if previous_actions else "None"

    instruction_prompt = f"""
      Please generate the next move according to the UI screenshot, instruction and previous actions.

      Instruction: {instruction}

      Previous actions:
      {previous_actions_str}"""

    # 构造 messages 数组
    messages = [
        {
            "role": "system",
            "content": [{"text": system_prompt}],
        }
    ]

    history_len = min(history_n, len(history_output))
    if history_len > 0:
        # 添加历史对话
        for history_id, history_item in enumerate(history_output[-history_n:], 0):
            if history_id == 0:
                messages.append({
                    "role": "user",
                    "content": [
                        {"text": instruction_prompt},
                        {"image": "file://" + history_item['image']}
                    ]
                })
            else:
                messages.append({
                    "role": "user",
                    "content": [{"image": "file://" + history_item['image']}]
                })

            messages.append({
                "role": "assistant",
                "content": [{"text": history_item['output']}],
            })

        # 添加当前截图
        messages.append({
            "role": "user",
            "content": [{"image": "file://" + image}]
        })
    else:
        # 首轮对话
        messages.append({
            "role": "user",
            "content": [
                {"text": instruction_prompt},
                {"image": "file://" + image}
            ]
        })

    return messages
```

GUI模型的多轮对话的`message`数组示例如下（以7轮对话为例）

```
model_input
  [{
    "role": "system",
    "content": [{
      "text": "# Tools\n\nYou may call one or more functions to assist with the user query.\n\nYou are provided with function signatures within <tools></tools> XML tags:\n<tools>\n{\"type\": \"function\", \"function\": {\"name_for_human\": \"mobile_use\", \"name\": \"mobile_use\", \"description\": \"Use a touchscreen to interact with a mobile device, and take screenshots.\n* This is an interface to a mobile device with touchscreen. You can perform actions like clicking, typing, swiping, etc.\n* Some applications may take time to start or process actions, so you may need to wait and take successive screenshots to see the results of your actions.\n* The screen's resolution is 1000x1000.\n* Make sure to click any buttons, links, icons, etc with the cursor tip in the center of the element. Don't click boxes on their edges unless asked.\", \"parameters\": {\"properties\": {\"action\": {\"description\": \"The action to perform. The available actions are:\n* `key`: Perform a key event on the mobile device.\n    - This supports adb's `keyevent` syntax.\n    - Examples: \"volume_up\", \"volume_down\", \"power\", \"camera\", \"clear\".\n* `click`: Click the point on the screen with coordinate (x, y).\n* `long_press`: Press the point on the screen with coordinate (x, y) for specified seconds.\n* `swipe`: Swipe from the starting point with coordinate (x, y) to the end point with coordinates2 (x2, y2).\n* `type`: Input the specified text into the activated input box.\n* `system_button`: Press the system button.\n* `open`: Open an app on the device.\n* `wait`: Wait specified seconds for the change to happen.\n* `answer`: Terminate the current task and output the answer.\n* `interact`: Resolve the blocking window by interacting with the user.\n* `terminate`: Terminate the current task and report its completion status.\", \"enum\": [\"key\", \"click\", \"long_press\", \"swipe\", \"type\", \"system_button\", \"open\", \"wait\", \"answer\", \"interact\", \"terminate\"], \"type\": \"string\"}, \"coordinate\": {\"description\": \"(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by `action=click`, `action=long_press`, and `action=swipe`.\", \"type\": \"array\"}, \"coordinate2\": {\"description\": \"(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by `action=swipe`.\", \"type\": \"array\"}, \"text\": {\"description\": \"Required only by `action=key`, `action=type`, `action=open`, `action=answer`,and `action=interact`.\", \"type\": \"string\"}, \"time\": {\"description\": \"The seconds to wait. Required only by `action=long_press` and `action=wait`.\", \"type\": \"number\"}, \"button\": {\"description\": \"Back means returning to the previous interface, Home means returning to the desktop, Menu means opening the application background menu, and Enter means pressing the enter. Required only by `action=system_button`\", \"enum\": [\"Back\", \"Home\", \"Menu\", \"Enter\"], \"type\": \"string\"}, \"status\": {\"description\": \"The status of the task. Required only by `action=terminate`.\", \"type\": \"string\", \"enum\": [\"success\", \"failure\"]}}, \"required\": [\"action\"], \"type\": \"object\"}, \"args_format\": \"Format the arguments as a JSON object.\"}}\n</tools>\n\nFor each function call, return a json object with function name and arguments within <tool_call></tool_call> XML tags:\n<tool_call>\n{\"name\": <function-name>, \"arguments\": <args-json-object>}\n</tool_call>\n\n# Response format\n\nResponse format for every step:\n1) Action: a short imperative describing what to do in the UI.\n2) A single <tool_call>...</tool_call> block containing only the JSON: {\"name\": <function-name>, \"arguments\": <args-json-object>}.\n\nRules:\n- Output exactly in the order: Action, <tool_call>.\n- Be brief: one for Action.\n- Do not output anything else outside those two parts.\n- If finishing, use action=terminate in the tool call."
    }]
  }, {
    "role": "user",
    "content": [{
      "text": "\nPlease generate the next move according to the UI screenshot, instruction and previous actions.\n\nInstruction: 帮我在携程搜一下今天济南喜来登酒店的价格\n\nPrevious actions:\nStep 1: 点击携程旅行应用图标以启动携程旅行预订应用程序。\nStep 2: 等待促销启动画面自动过渡到携程主应用界面。"
    }, {
      "image": "http://nlp-mobile-agent.oss-cn-zhangjiakou.aliyuncs.com/computer-use%2Fscreenshot%2Fscreenshot_a84122ac_853a630315784b64988492c9c07b5534.png"
    }]
  }, {
    "role": "assistant",
    "content": [{
      "text": "Action: 点击应用更新通知弹窗右上角的关闭按钮（X图标）以将其关闭。\n<tool_call>\n{\"name\": \"mobile_use\", \"arguments\": {\"action\": \"click\", \"coordinate\": [789, 280]}}\n</tool_call>"
    }]
  }, {
    "role": "user",
    "content": [{
      "image": "http://nlp-mobile-agent.oss-cn-zhangjiakou.aliyuncs.com/computer-use%2Fscreenshot%2Fscreenshot_6010a769_089b9b35b1904913bd5df492563b02b9.png"
    }]
  }, {
    "role": "assistant",
    "content": [{
      "text": "Action: 点击搜索栏中的"济南的酒店"文本区域，以激活搜索输入框并准备修改搜索词。\n<tool_call>\n{\"name\": \"mobile_use\", \"arguments\": {\"action\": \"click\", \"coordinate\": [112, 134]}}\n</tool_call>"
    }]
  }, {
    "role": "user",
    "content": [{
      "image": "http://nlp-mobile-agent.oss-cn-zhangjiakou.aliyuncs.com/computer-use%2Fscreenshot%2Fscreenshot_47446db4_fd4a5022002c4db99f110d5c7261fea2.png"
    }]
  }, {
    "role": "assistant",
    "content": [{
      "text": "Action: 点击显示"厦门"的位置字段，将搜索位置从厦门更改为济南。\n<tool_call>\n{\"name\": \"mobile_use\", \"arguments\": {\"action\": \"click\", \"coordinate\": [156, 347]}}\n</tool_call>"
    }]
  }, {
    "role": "user",
    "content": [{
      "image": "http://nlp-mobile-agent.oss-cn-zhangjiakou.aliyuncs.com/computer-use%2Fscreenshot%2Fscreenshot_3832132c_8c55861c1716467e802a3554402f3580.png"
    }]
  }, {
    "role": "assistant",
    "content": [{
      "text": "Action: 在搜索输入框中键入"济南"，以指定酒店搜索的城市位置。\n<tool_call>\n{\"name\": \"mobile_use\", \"arguments\": {\"action\": \"type\", \"text\": \"济南\"}}\n</tool_call>"
    }]
  }, {
    "role": "user",
    "content": [{
      "image": "http://nlp-mobile-agent.oss-cn-zhangjiakou.aliyuncs.com/computer-use%2Fscreenshot%2Fscreenshot_ff247bac_39c3e20be32c4baf8677a2b6b61bc021.png"
    }]
  }]
```

#### 步骤3. 解析模型输出

由于模型在处理图像时会进行内部缩放，其返回的坐标是基于缩放后图像的归一化坐标。为在原图上准确执行`GUI`操作，需要进行坐标映射。

1.  **提取 Tool Call 字段**
    
    首先从模型返回的字符串中提取Tool Call：
    

```
import re
import json

def extract_tool_calls(text):
    """
    从模型输出中提取所有 <tool_call> 块

    参数:
        text: 模型返回的文本

    返回:
        actions: 解析后的操作列表
    """
    pattern = re.compile(r'<tool_call>(.*?)</tool_call>', re.DOTALL | re.IGNORECASE)
    blocks = pattern.findall(text)

    actions = []
    for blk in blocks:
        blk = blk.strip()
        try:
            actions.append(json.loads(blk))
        except json.JSONDecodeError as e:
            print(f'解析失败: {e} | 片段: {blk[:80]}...')

    return actions
```

2.  **坐标映射函数**
    
    模型处理图像时会进行内部缩放，以下函数用于计算缩放后的尺寸：
    

```
import math
from PIL import Image

def smart_resize(height, width, factor=32, min_pixels=32*32*4, max_pixels=32*32*1280, max_long_side=8192):
    """
    计算模型内部缩放后的图像尺寸

    参数:
        height: 原始图像高度
        width: 原始图像宽度
        factor: 分辨率因子（默认为 32）
        min_pixels: 最小像素值
        max_pixels: 最大像素值
        max_long_side: 最长边限制

    返回:
        (h_bar, w_bar): 缩放后的高度和宽度
    """
    def round_by_factor(number, factor):
        return round(number / factor) * factor

    def ceil_by_factor(number, factor):
        return math.ceil(number / factor) * factor

    def floor_by_factor(number, factor):
        return math.floor(number / factor) * factor

    if height < 2 or width < 2:
        raise ValueError(f"height:{height} or width:{width} must be larger than factor:{factor}")
    elif max(height, width) / min(height, width) > 200:
        raise ValueError(f"absolute aspect ratio must be smaller than 200, got {height} / {width}")

    # 限制最长边
    if max(height, width) > max_long_side:
        beta = max(height, width) / max_long_side
        height, width = int(height / beta), int(width / beta)

    # 计算缩放后的尺寸
    h_bar = round_by_factor(height, factor)
    w_bar = round_by_factor(width, factor)

    if h_bar * w_bar > max_pixels:
        beta = math.sqrt((height * width) / max_pixels)
        h_bar = floor_by_factor(height / beta, factor)
        w_bar = floor_by_factor(width / beta, factor)
    elif h_bar * w_bar < min_pixels:
        beta = math.sqrt(min_pixels / (height * width))
        h_bar = ceil_by_factor(height * beta, factor)
        w_bar = ceil_by_factor(width * beta, factor)

    return h_bar, w_bar
```

#### 步骤4. 执行GUI操作

解析动作指令后，接下来演示如何使用`pyautogui`库模拟用户的鼠标点击、键盘输入、滚动等物理 GUI 操作。

```
import pyautogui
import pyperclip
import time
from PIL import Image
import os

class ComputerTools:
    """电脑端 GUI 操作工具类"""

    def __init__(self):
        self.image_info = None

    def load_image_info(self, path):
        """加载图像尺寸信息"""
        width, height = Image.open(path).size
        self.image_info = (width, height)

    def get_screenshot(self, image_path, retry_times=3):
        """获取桌面截图"""
        if os.path.exists(image_path):
            os.remove(image_path)

        for i in range(retry_times):
            screenshot = pyautogui.screenshot()
            screenshot.save(image_path)
            if os.path.exists(image_path):
                self.load_image_info(image_path)
                return True
            else:
                time.sleep(0.1)
        return False

    def reset(self):
        """显示桌面"""
        pyautogui.hotkey('win', 'd')

    def press_key(self, keys):
        """按键操作"""
        if isinstance(keys, list):
            cleaned_keys = []
            for key in keys:
                if isinstance(key, str):
                    # 处理键名格式
                    if key.startswith("keys=["):
                        key = key[6:]
                    if key.endswith("]"):
                        key = key[:-1]
                    if key.startswith("['") or key.startswith('["'):
                        key = key[2:] if len(key) > 2 else key
                    if key.endswith("']") or key.endswith('"]'):
                        key = key[:-2] if len(key) > 2 else key
                    key = key.strip()

                    # 转换键名
                    key_map = {
                        "arrowleft": "left",
                        "arrowright": "right",
                        "arrowup": "up",
                        "arrowdown": "down"
                    }
                    key = key_map.get(key, key)
                    cleaned_keys.append(key)
                else:
                    cleaned_keys.append(key)
            keys = cleaned_keys
        else:
            keys = [keys]

        if len(keys) > 1:
            pyautogui.hotkey(*keys)
        else:
            pyautogui.press(keys[0])

    def type(self, text):
        """输入文本（使用剪贴板方式支持中文）"""
        pyperclip.copy(text)
        pyautogui.keyDown('ctrl')
        pyautogui.keyDown('v')
        pyautogui.keyUp('v')
        pyautogui.keyUp('ctrl')

    def mouse_move(self, x, y):
        """移动鼠标到指定坐标"""
        pyautogui.moveTo(x, y)
        time.sleep(0.1)
        pyautogui.moveTo(x, y)

    def left_click(self, x, y):
        """左键点击"""
        pyautogui.moveTo(x, y)
        time.sleep(0.1)
        pyautogui.click()

    def left_click_drag(self, x, y):
        """从当前位置拖拽到指定坐标"""
        pyautogui.dragTo(x, y, duration=0.5)
        pyautogui.moveTo(x, y)

    def right_click(self, x, y):
        """右键点击"""
        pyautogui.moveTo(x, y)
        time.sleep(0.1)
        pyautogui.rightClick()

    def middle_click(self, x, y):
        """中键点击"""
        pyautogui.moveTo(x, y)
        time.sleep(0.1)
        pyautogui.middleClick()

    def double_click(self, x, y):
        """双击"""
        pyautogui.moveTo(x, y)
        time.sleep(0.1)
        pyautogui.doubleClick()

    def triple_click(self, x, y):
        """三击"""
        pyautogui.moveTo(x, y)
        time.sleep(0.1)
        pyautogui.tripleClick()

    def scroll(self, pixels):
        """滚轮滚动"""
        pyautogui.scroll(pixels)
```

#### 步骤5. 完整自动化流程

将以上所有步骤整合到一个完整的自动化流程中，循环执行截图 → 模型推理 → 执行GUI操作，直到任务完成。

```
import os
import uuid
import dashscope
import time

def run_gui_automation(instruction, max_step=30):
    """
    运行完整的 GUI 自动化流程

    参数:
        instruction: 用户指令
        max_step: 最大执行步骤数
    """
    # 配置 API
    dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")
    # 以下为华北2（北京）地域的URL，，调用时请将WorkspaceId替换为真实的业务空间ID
    dashscope.base_http_api_url = 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1'
    model_name = 'gui-plus-2026-02-26'

    # 初始化工具
    computer_tools = ComputerTools()
    computer_tools.reset()  # 显示桌面

    # 创建输出目录
    output_dir = os.path.join(os.path.expanduser("~"), "Desktop", "gui_automation")
    os.makedirs(output_dir, exist_ok=True)

    # 对话历史
    history = []
    stop_flag = False
    session_id = str(uuid.uuid4())
    print('session_id ', session_id)

    print(f"[任务] {instruction}")
    print("=" * 60)

    for step_id in range(max_step):
        if stop_flag:
            break

        print(f"\n[步骤 {step_id + 1}]")

        # 1. 截图
        screen_shot = os.path.join(output_dir, f'screenshot_{step_id}.png')
        computer_tools.get_screenshot(screen_shot)

        # 2. 构造消息
        messages = get_messages(screen_shot, instruction, history, model_name)

        # 3. 调用模型
        retry_time = 3
        for _ in range(retry_time):
            response = dashscope.MultiModalConversation.call(
                model=model_name,
                messages=messages,
                vl_high_resolution_images=True,
                headers={"x-dashscope-gui-session-id": session_id},
                stream=False
            )
            print(response['request_id'])
            try:
                output_text = response.output.choices[0].message.content[0]['text']
                break
            except Exception as e:
                print(response)
                print(e)
        else:
            raise Exception('retry_time out')
        print(f"[模型输出]\n{output_text}\n")

        # 4. 解析操作
        action_list = extract_tool_calls(output_text)
        if not action_list:
            print("未提取到有效操作")
            break

        # 5. 执行操作
        for action_id, action in enumerate(action_list):
            action_parameter = action['arguments']
            action_type = action_parameter['action']

            # 获取图像尺寸用于坐标映射
            dummy_image = Image.open(screen_shot)
            resized_height, resized_width = smart_resize(
                dummy_image.height,
                dummy_image.width,
                factor=16,
                min_pixels=3136,
                max_pixels=1003520 * 200
            )

            # 映射坐标（从归一化坐标 1000x1000 映射到实际尺寸）
            for key in ['coordinate', 'coordinate1', 'coordinate2']:
                if key in action_parameter:
                    action_parameter[key][0] = int(action_parameter[key][0] / 1000 * resized_width)
                    action_parameter[key][1] = int(action_parameter[key][1] / 1000 * resized_height)

            # 执行对应操作
            if action_type in ['click', 'left_click']:
                computer_tools.left_click(
                    action_parameter['coordinate'][0],
                    action_parameter['coordinate'][1]
                )
                print(f"✓ 左键点击 ({action_parameter['coordinate'][0]}, {action_parameter['coordinate'][1]})")

            elif action_type == 'mouse_move':
                computer_tools.mouse_move(
                    action_parameter['coordinate'][0],
                    action_parameter['coordinate'][1]
                )
                print(f"✓ 移动鼠标到 ({action_parameter['coordinate'][0]}, {action_parameter['coordinate'][1]})")

            elif action_type == 'middle_click':
                computer_tools.middle_click(
                    action_parameter['coordinate'][0],
                    action_parameter['coordinate'][1]
                )
                print(f"✓ 中键点击")

            elif action_type in ['right click', 'right_click']:
                computer_tools.right_click(
                    action_parameter['coordinate'][0],
                    action_parameter['coordinate'][1]
                )
                print(f"✓ 右键点击")

            elif action_type in ['key', 'hotkey']:
                computer_tools.press_key(action_parameter['keys'])
                print(f"✓ 按键 {action_parameter['keys']}")

            elif action_type == 'type':
                text = action_parameter['text']
                computer_tools.type(text)
                print(f"✓ 输入文本: {text}")

            elif action_type == 'drag':
                computer_tools.left_click_drag(
                    action_parameter['coordinate'][0],
                    action_parameter['coordinate'][1]
                )
                print(f"✓ 拖拽到 ({action_parameter['coordinate'][0]}, {action_parameter['coordinate'][1]})")

            elif action_type == 'scroll':
                if 'coordinate' in action_parameter:
                    computer_tools.mouse_move(
                        action_parameter['coordinate'][0],
                        action_parameter['coordinate'][1]
                    )
                computer_tools.scroll(action_parameter.get("pixels", 1))
                print(f"✓ 滚动 {action_parameter.get('pixels', 1)} 像素")

            elif action_type in ['computer_double_click', 'double_click']:
                computer_tools.double_click(
                    action_parameter['coordinate'][0],
                    action_parameter['coordinate'][1]
                )
                print(f"✓ 双击")

            elif action_type == 'wait':
                time.sleep(action_parameter.get('time', 2))
                print(f"✓ 等待 {action_parameter.get('time', 2)} 秒")

            elif action_type == 'answer':
                print(f"✓ 任务完成: {action_parameter.get('text', '')}")
                stop_flag = True
                break

            elif action_type in ['stop', 'terminate', 'done']:
                print(f"✓ 任务终止: {action_parameter.get('status', 'success')}")
                stop_flag = True
                break

            else:
                print(f"未知操作类型: {action_type}")

        # 6. 保存历史
        history.append({
            'output': output_text,
            'image': screen_shot
        })

        time.sleep(2)  # 操作间隔

    print("\n" + "=" * 60)
    print(f"[完成] 共执行 {len(history)} 步")

# 使用示例
if __name__ == '__main__':
    run_gui_automation(
        instruction='帮我打开chrome,在百度中搜索阿里巴巴',
        max_step=30
    )
```

电脑端完整示例代码

```
import os
import re
import json
import math
import time
import uuid
import pyautogui
import pyperclip
import dashscope
from PIL import Image

# ===================== 步骤1：System Prompt =====================

system_prompt = """# Tools

You may call one or more functions to assist with the user query.

You are provided with function signatures within <tools></tools> XML tags:
<tools>
{"type": "function", "function": {"name": "computer_use", "description": "Use a mouse and keyboard to interact with a computer, and take screenshots.\\n* This is an interface to a desktop GUI. You do not have access to a terminal or applications menu. You must click on desktop icons to start applications.\\n* Some applications may take time to start or process actions, so you may need to wait and take successive screenshots to see the results of your actions. E.g. if you click on Firefox and a window doesn't open, try wait and taking another screenshot.\\n* The screen's resolution is 1000x1000.\\n* Make sure to click any buttons, links, icons, etc with the cursor tip in the center of the element. Don't click boxes on their edges unless asked.", "parameters": {"properties": {"action": {"description": "The action to perform. The available actions are:\\n* `key`: Performs key down presses on the arguments passed in order, then performs key releases in reverse order.\\n* `type`: Type a string of text on the keyboard.\\n* `mouse_move`: Move the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `left_click`: Click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `left_click_drag`: Click and drag the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `right_click`: Click the right mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `middle_click`: Click the middle mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `double_click`: Double-click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `triple_click`: Triple-click the left mouse button at a specified (x, y) pixel coordinate on the screen (simulated as double-click since it's the closest action).\\n* `scroll`: Performs a scroll of the mouse scroll wheel.\\n* `hscroll`: Performs a horizontal scroll (mapped to regular scroll).\\n* `wait`: Wait specified seconds for the change to happen.\\n* `terminate`: Terminate the current task and report its completion status.\\n* `answer`: Answer a question.\\n* `interact`: Resolve the blocking window by interacting with the user.", "enum": ["key", "type", "mouse_move", "left_click", "left_click_drag", "right_click", "middle_click", "double_click", "triple_click", "scroll", "hscroll", "wait", "terminate", "answer", "interact"], "type": "string"}, "keys": {"description": "Required only by `action=key`.", "type": "array"}, "text": {"description": "Required only by `action=type`, `action=answer` and `action=interact`.", "type": "string"}, "coordinate": {"description": "(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by `action=mouse_move` and `action=left_click_drag`.", "type": "array"}, "pixels": {"description": "The amount of scrolling to perform. Positive values scroll up, negative values scroll down. Required only by `action=scroll` and `action=hscroll`.", "type": "number"}, "time": {"description": "The seconds to wait. Required only by `action=wait`.", "type": "number"}, "status": {"description": "The status of the task. Required only by `action=terminate`.", "type": "string", "enum": ["success", "failure"]}}, "required": ["action"], "type": "object"}}}
</tools>

For each function call, return a json object with function name and arguments within <tool_call></tool_call> XML tags:
<tool_call>
{"name": <function-name>, "arguments": <args-json-object>}
</tool_call>

# Response format

Response format for every step:
1) Action: a short imperative describing what to do in the UI.
2) A single <tool_call>...</tool_call> block containing only the JSON: {"name": <function-name>, "arguments": <args-json-object>}.

Rules:
- Output exactly in the order: Action, <tool_call>.
- Be brief: one for Action.
- Do not output anything else outside those two parts.
- If finishing, use action=terminate in the tool call."""

# ===================== 步骤2：构造多轮对话消息 =====================

def get_messages(image, instruction, history_output, system_prompt):
    history_n = 4
    current_step = len(history_output)

    history_start_idx = max(0, current_step - history_n)
    previous_actions = []
    for i in range(history_start_idx):
        if i < len(history_output):
            history_output_str = history_output[i]['output']
            if 'Action:' in history_output_str and '<tool_call>':
                history_output_str = history_output_str.split('Action:')[1].split('<tool_call>')[0].strip()
            previous_actions.append(f"Step {i + 1}: {history_output_str}")

    previous_actions_str = "\\n".join(previous_actions) if previous_actions else "None"

    instruction_prompt = f"""
      Please generate the next move according to the UI screenshot, instruction and previous actions.

      Instruction: {instruction}

      Previous actions:
      {previous_actions_str}"""

    messages = [{"role": "system", "content": [{"text": system_prompt}]}]

    history_len = min(history_n, len(history_output))
    if history_len > 0:
        for history_id, history_item in enumerate(history_output[-history_n:], 0):
            if history_id == 0:
                messages.append({
                    "role": "user",
                    "content": [
                        {"text": instruction_prompt},
                        {"image": "file://" + history_item['image']}
                    ]
                })
            else:
                messages.append({
                    "role": "user",
                    "content": [{"image": "file://" + history_item['image']}]
                })
            messages.append({
                "role": "assistant",
                "content": [{"text": history_item['output']}],
            })
        messages.append({
            "role": "user",
            "content": [{"image": "file://" + image}]
        })
    else:
        messages.append({
            "role": "user",
            "content": [
                {"text": instruction_prompt},
                {"image": "file://" + image}
            ]
        })
    return messages

# ===================== 步骤3：解析模型输出与坐标映射 =====================

def extract_tool_calls(text):
    pattern = re.compile(r'<tool_call>(.*?)</tool_call>', re.DOTALL | re.IGNORECASE)
    blocks = pattern.findall(text)
    actions = []
    for blk in blocks:
        blk = blk.strip()
        try:
            actions.append(json.loads(blk))
        except json.JSONDecodeError as e:
            print(f'解析失败: {e} | 片段: {blk[:80]}...')
    return actions

def smart_resize(height, width, factor=32, min_pixels=32*32*4, max_pixels=32*32*1280, max_long_side=8192):
    def round_by_factor(number, factor):
        return round(number / factor) * factor
    def ceil_by_factor(number, factor):
        return math.ceil(number / factor) * factor
    def floor_by_factor(number, factor):
        return math.floor(number / factor) * factor

    if height < 2 or width < 2:
        raise ValueError(f"height:{height} or width:{width} must be larger than factor:{factor}")
    elif max(height, width) / min(height, width) > 200:
        raise ValueError(f"absolute aspect ratio must be smaller than 200, got {height} / {width}")

    if max(height, width) > max_long_side:
        beta = max(height, width) / max_long_side
        height, width = int(height / beta), int(width / beta)

    h_bar = round_by_factor(height, factor)
    w_bar = round_by_factor(width, factor)

    if h_bar * w_bar > max_pixels:
        beta = math.sqrt((height * width) / max_pixels)
        h_bar = floor_by_factor(height / beta, factor)
        w_bar = floor_by_factor(width / beta, factor)
    elif h_bar * w_bar < min_pixels:
        beta = math.sqrt(min_pixels / (height * width))
        h_bar = ceil_by_factor(height * beta, factor)
        w_bar = ceil_by_factor(width * beta, factor)
    return h_bar, w_bar

# ===================== 步骤4：GUI 操作工具类 =====================

class ComputerTools:
    def __init__(self):
        self.image_info = None

    def load_image_info(self, path):
        width, height = Image.open(path).size
        self.image_info = (width, height)

    def get_screenshot(self, image_path, retry_times=3):
        if os.path.exists(image_path):
            os.remove(image_path)
        for i in range(retry_times):
            screenshot = pyautogui.screenshot()
            screenshot.save(image_path)
            if os.path.exists(image_path):
                self.load_image_info(image_path)
                return True
            else:
                time.sleep(0.1)
        return False

    def reset(self):
        pyautogui.hotkey('win', 'd')

    def press_key(self, keys):
        if isinstance(keys, list):
            cleaned_keys = []
            for key in keys:
                if isinstance(key, str):
                    if key.startswith("keys=["): key = key[6:]
                    if key.endswith("]"): key = key[:-1]
                    if key.startswith("['") or key.startswith('["'): key = key[2:] if len(key) > 2 else key
                    if key.endswith("']") or key.endswith('"]'): key = key[:-2] if len(key) > 2 else key
                    key = key.strip()
                    key_map = {"arrowleft": "left", "arrowright": "right", "arrowup": "up", "arrowdown": "down"}
                    key = key_map.get(key, key)
                    cleaned_keys.append(key)
                else:
                    cleaned_keys.append(key)
            keys = cleaned_keys
        else:
            keys = [keys]
        if len(keys) > 1:
            pyautogui.hotkey(*keys)
        else:
            pyautogui.press(keys[0])

    def type(self, text):
        pyperclip.copy(text)
        pyautogui.keyDown('ctrl')
        pyautogui.keyDown('v')
        pyautogui.keyUp('v')
        pyautogui.keyUp('ctrl')

    def mouse_move(self, x, y):
        pyautogui.moveTo(x, y)
        time.sleep(0.1)
        pyautogui.moveTo(x, y)

    def left_click(self, x, y):
        pyautogui.moveTo(x, y)
        time.sleep(0.1)
        pyautogui.click()

    def left_click_drag(self, x, y):
        pyautogui.dragTo(x, y, duration=0.5)
        pyautogui.moveTo(x, y)

    def right_click(self, x, y):
        pyautogui.moveTo(x, y)
        time.sleep(0.1)
        pyautogui.rightClick()

    def middle_click(self, x, y):
        pyautogui.moveTo(x, y)
        time.sleep(0.1)
        pyautogui.middleClick()

    def double_click(self, x, y):
        pyautogui.moveTo(x, y)
        time.sleep(0.1)
        pyautogui.doubleClick()

    def triple_click(self, x, y):
        pyautogui.moveTo(x, y)
        time.sleep(0.1)
        pyautogui.tripleClick()

    def scroll(self, pixels):
        pyautogui.scroll(pixels)

# ===================== 步骤5：完整自动化流程 =====================

def run_gui_automation(instruction, max_step=30):
    dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")
    # 以下为华北2（北京）地域的URL，，调用时请将WorkspaceId替换为真实的业务空间ID
    dashscope.base_http_api_url = 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1'
    model_name = 'gui-plus-2026-02-26'

    computer_tools = ComputerTools()
    computer_tools.reset()

    output_dir = os.path.join(os.path.expanduser("~"), "Desktop", "gui_automation")
    os.makedirs(output_dir, exist_ok=True)

    history = []
    stop_flag = False
    session_id = str(uuid.uuid4())
    print('session_id ', session_id)

    print(f"[任务] {instruction}")
    print("=" * 60)

    for step_id in range(max_step):
        if stop_flag:
            break

        print(f"\n[步骤 {step_id + 1}]")

        screen_shot = os.path.join(output_dir, f'screenshot_{step_id}.png')
        computer_tools.get_screenshot(screen_shot)

        messages = get_messages(screen_shot, instruction, history, system_prompt)

        retry_time = 3
        for _ in range(retry_time):
            response = dashscope.MultiModalConversation.call(
                model=model_name,
                messages=messages,
                vl_high_resolution_images=True,
                headers={"x-dashscope-gui-session-id": session_id},
                stream=False
            )
            print(response['request_id'])
            try:
                output_text = response.output.choices[0].message.content[0]['text']
                break
            except Exception as e:
                print(response)
                print(e)
        else:
            raise Exception('retry_time out')
        print(f"[模型输出]\n{output_text}\n")

        action_list = extract_tool_calls(output_text)
        if not action_list:
            print("未提取到有效操作")
            break

        for action_id, action in enumerate(action_list):
            action_parameter = action['arguments']
            action_type = action_parameter['action']

            dummy_image = Image.open(screen_shot)
            resized_height, resized_width = smart_resize(
                dummy_image.height, dummy_image.width,
                factor=16, min_pixels=3136, max_pixels=1003520 * 200
            )

            for key in ['coordinate', 'coordinate1', 'coordinate2']:
                if key in action_parameter:
                    action_parameter[key][0] = int(action_parameter[key][0] / 1000 * resized_width)
                    action_parameter[key][1] = int(action_parameter[key][1] / 1000 * resized_height)

            if action_type in ['click', 'left_click']:
                computer_tools.left_click(action_parameter['coordinate'][0], action_parameter['coordinate'][1])
                print(f"✓ 左键点击 ({action_parameter['coordinate'][0]}, {action_parameter['coordinate'][1]})")
            elif action_type == 'mouse_move':
                computer_tools.mouse_move(action_parameter['coordinate'][0], action_parameter['coordinate'][1])
                print(f"✓ 移动鼠标")
            elif action_type == 'middle_click':
                computer_tools.middle_click(action_parameter['coordinate'][0], action_parameter['coordinate'][1])
                print(f"✓ 中键点击")
            elif action_type in ['right click', 'right_click']:
                computer_tools.right_click(action_parameter['coordinate'][0], action_parameter['coordinate'][1])
                print(f"✓ 右键点击")
            elif action_type in ['key', 'hotkey']:
                computer_tools.press_key(action_parameter['keys'])
                print(f"✓ 按键 {action_parameter['keys']}")
            elif action_type == 'type':
                computer_tools.type(action_parameter['text'])
                print(f"✓ 输入文本: {action_parameter['text']}")
            elif action_type == 'drag':
                computer_tools.left_click_drag(action_parameter['coordinate'][0], action_parameter['coordinate'][1])
                print(f"✓ 拖拽")
            elif action_type == 'scroll':
                if 'coordinate' in action_parameter:
                    computer_tools.mouse_move(action_parameter['coordinate'][0], action_parameter['coordinate'][1])
                computer_tools.scroll(action_parameter.get("pixels", 1))
                print(f"✓ 滚动 {action_parameter.get('pixels', 1)} 像素")
            elif action_type in ['computer_double_click', 'double_click']:
                computer_tools.double_click(action_parameter['coordinate'][0], action_parameter['coordinate'][1])
                print(f"✓ 双击")
            elif action_type == 'wait':
                time.sleep(action_parameter.get('time', 2))
                print(f"✓ 等待 {action_parameter.get('time', 2)} 秒")
            elif action_type == 'answer':
                print(f"✓ 任务完成: {action_parameter.get('text', '')}")
                stop_flag = True
                break
            elif action_type in ['stop', 'terminate', 'done']:
                print(f"✓ 任务终止: {action_parameter.get('status', 'success')}")
                stop_flag = True
                break
            else:
                print(f"未知操作类型: {action_type}")

        history.append({'output': output_text, 'image': screen_shot})
        time.sleep(2)

    print("\n" + "=" * 60)
    print(f"[完成] 共执行 {len(history)} 步")

if __name__ == '__main__':
    run_gui_automation(
        instruction='帮我打开chrome,在百度中搜索阿里巴巴',
        max_step=30
    )
```

### 手机端 GUI 任务

手机端通过 ADB（Android Debug Bridge）工具实现自动化操作。

**环境准备：**

1.  下载适合系统的 [Android Debug Bridge](https://developer.android.com/tools/releases/platform-tools?hl=en)，保存到指定路径
2.  在手机上开启“USB调试”或“ADB调试”（通常需要先开启开发者选项）
3.  通过数据线连接手机和电脑，选择“传输文件”模式
4.  下载[ADB键盘](https://github.com/senzhk/ADBKeyBoard/blob/master/ADBKeyboard.apk)的安装包，并将安装包传输到手机上打开，选择无视风险安装
5.  在系统设置中将默认输入法切换为`ADB Keyboard`
6.  在电脑终端上测试连接：`/path/to/adb devices`（设备列表不为空说明连接成功）
7.  电脑系统为`macOS/Linux`时， 需要开启权限：`sudo chmod +x /path/to/adb`
8.  进入手机的某个App，然后执行命令：`/path/to/adb shell am start -a android.intent.action.MAIN -c android.intent.category.HOME`，如果手机设备退回到桌面，则说明一切就绪

手机端GUI示例与电脑端大致相同，完整示例代码如下：

手机端完整示例代码

1.  **构造手机端**`System Prompt`

```
import json, os, subprocess
import dashscope, time, math
from PIL import Image, ImageDraw
import shutil, requests
from datetime import datetime

mobile_system_prompt = '''# Tools
        You may call one or more functions to assist with the user query.

        You are provided with function signatures within <tools></tools> XML tags:
        <tools>
        {"type": "function", "function": {"name_for_human": "mobile_use", "name": "mobile_use", "description": "Use a touchscreen to interact with a mobile device, and take screenshots.
        * This is an interface to a mobile device with touchscreen. You can perform actions like clicking, typing, swiping, etc.
        * Some applications may take time to start or process actions, so you may need to wait and take successive screenshots to see the results of your actions.
        * The screen's resolution is 1000x1000.
        * Make sure to click any buttons, links, icons, etc with the cursor tip in the center of the element. Don't click boxes on their edges unless asked.", "parameters": {"properties": {"action": {"description": "The action to perform. The available actions are:
        * `key`: Perform a key event on the mobile device.
            - This supports adb's `keyevent` syntax.
            - Examples: "volume_up", "volume_down", "power", "camera", "clear".
        * `click`: Click the point on the screen with coordinate (x, y).
        * `long_press`: Press the point on the screen with coordinate (x, y) for specified seconds.
        * `swipe`: Swipe from the starting point with coordinate (x, y) to the end point with coordinates2 (x2, y2).
        * `type`: Input the specified text into the activated input box.
        * `system_button`: Press the system button.
        * `open`: Open an app on the device.
        * `wait`: Wait specified seconds for the change to happen.
        * `answer`: Terminate the current task and output the answer.
        * `interact`: Resolve the blocking window by interacting with the user.
        * `terminate`: Terminate the current task and report its completion status.", "enum": ["key", "click", "long_press", "swipe", "type", "system_button", "open", "wait", "answer", "interact", "terminate"], "type": "string"}, "coordinate": {"description": "(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by `action=click`, `action=long_press`, and `action=swipe`.", "type": "array"}, "coordinate2": {"description": "(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by `action=swipe`.", "type": "array"}, "text": {"description": "Required only by `action=key`, `action=type`, `action=open`, `action=answer`,and `action=interact`.", "type": "string"}, "time": {"description": "The seconds to wait. Required only by `action=long_press` and `action=wait`.", "type": "number"}, "button": {"description": "Back means returning to the previous interface, Home means returning to the desktop, Menu means opening the application background menu, and Enter means pressing the enter. Required only by `action=system_button`", "enum": ["Back", "Home", "Menu", "Enter"], "type": "string"}, "status": {"description": "The status of the task. Required only by `action=terminate`.", "type": "string", "enum": ["success", "failure"]}}, "required": ["action"], "type": "object"}, "args_format": "Format the arguments as a JSON object."}}
        </tools>

        For each function call, return a json object with function name and arguments within <tool_call></tool_call> XML tags:
        <tool_call>
        {"name": <function-name>, "arguments": <args-json-object>}
        </tool_call>

        # Response format

        Response format for every step:
        1) Action: a short imperative describing what to do in the UI.
        2) A single <tool_call>...</tool_call> block containing only the JSON: {"name": <function-name>, "arguments": <args-json-object>}.

        Rules:
        - Output exactly in the order: Action, <tool_call>.
        - Be brief: one for Action.
        - Do not output anything else outside those two parts.
        - If finishing, use action=terminate in the tool call.'''
```

2.  **构造多轮对话消息**

```
from datetime import datetime

def get_messages(image, instruction, history_output, system_prompt):
    history_n = 4
    current_step = len(history_output)

    history_start_idx = max(0, current_step - history_n)

    previous_actions = []
    for i in range(history_start_idx):
        if i < len(history_output):
            history_output_str = history_output[i]['output']
            if 'Action:' in history_output_str and '<tool_call>':
                history_output_str = history_output_str.split('Action:')[1].split('<tool_call>')[0].strip()
            previous_actions.append(f"Step {i + 1}: {history_output_str}")

    previous_actions_str = (
        "\n".join(previous_actions) if previous_actions else "None"
    )
    # 添加背景信息
    today = datetime.today()
    weekday_names = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    weekday = weekday_names[today.weekday()]
    formatted_date = today.strftime("%Y年%m月%d日") + " " + weekday
    ground_info = f'''今天的日期是:{formatted_date}。'''

    instruction_prompt = f"""
        Please generate the next move according to the UI screenshot, instruction and previous actions.

        Instruction: {ground_info}{instruction}

        Previous actions:
        {previous_actions_str}"""

    ## 模型调用
    messages = [
        {
            "role": "system",
            "content": [
                {"text": system_prompt}
            ],
        }
    ]
    history_len = min(history_n, len(history_output))
    if history_len > 0:
        for history_id, history_item in enumerate(history_output[-history_n:], 0):
            if history_id == 0:
                messages.append({
                    "role": "user",
                    "content": [
                        {"text": instruction_prompt},
                        {"image": "file://" +history_item['image']}
                    ]
                })
            else:
                messages.append({
                    "role": "user",
                    "content": [
                        {"image": "file://" +history_item['image']}
                    ]
                })
            messages.append({
                "role": "assistant",
                "content": [
                    {"text": history_item['output']},
                ]
            })
        messages.append({
            "role": "user",
            "content": [
                {"image": "file://" +image},
            ]
        })
    else:
        messages.append(
            {
                "role": "user",
                "content": [
                    {
                        "text": instruction_prompt
                    },
                    {
                        "image": "file://" +image,
                    },
                ],
            }
        )

    return messages
```

3.  **计算缩放后的图像大小**
    
    手机端与电脑端共用一套 `smart_resize` 函数。详情请参见[坐标映射函数](raw/model-user-guide/model-experience/text-generation-model/specialized-models/gui-automation.md)。
    
4.  **执行GUI操作**
    
    使用 ADB 命令执行实际的手机操作。
    

```
import subprocess
import os
import time
from PIL import Image

class AdbTools:
    def __init__(self, adb_path, device=None):
        self.adb_path = adb_path
        self.device = device
        self.__device_str__ = f" -s {device} " if device is not None else ' '
        self.image_info = None

    def adb_shell(self, command):
        command = self.adb_path + self.__device_str__ + command
        subprocess.run(command, capture_output=True, text=True, shell=True)

    ## 载入手机size
    def load_image_info(self, path):
        width, height = Image.open(path).size
        self.image_info = (width, height)

    ## 获取截图
    def get_screenshot(self, image_path, retry_times=3):
        command = self.adb_path + (f" -s {self.device}" if self.device is not None else '') + f" exec-out screencap -p > {image_path}"

        for i in range(retry_times):
            subprocess.run(command, capture_output=True, text=True, shell=True)
            if os.path.exists(image_path):
                self.load_image_info(image_path)
                return True
            else:
                time.sleep(0.1)
        else:
            return False

    ## 点击(x,y)
    ## coordinate_size: 输入图片的尺寸，默认为None，则使用当前手机的尺寸, 传入为{'x': int, 'y': int}
    def click(self, x, y, coordinate_size=None):
        command = self.adb_path + self.__device_str__ + f" shell input tap {x} {y}"
        subprocess.run(command, capture_output=True, text=True, shell=True)

    def long_press(self, x, y, time=800):
        command = self.adb_path + self.__device_str__ + f" shell input swipe {x} {y} {x} {y} {time}"
        subprocess.run(command, capture_output=True, text=True, shell=True)

    ## 滑动从(x1,y1)->(x2,y2)
    ## coordinate_size: 输入图片的尺寸，默认为None，则使用当前手机的尺寸, 传入为{'x': int, 'y': int}
    def slide(self, x1, y1, x2, y2, coordinate_size=None, slide_time=800):
        command = self.adb_path + self.__device_str__ + f" shell input swipe {x1} {y1} {x2} {y2} {slide_time}"
        subprocess.run(command, capture_output=True, text=True, shell=True)

    ## 返回
    def back(self):
        command = self.adb_path + self.__device_str__ + f"  shell input keyevent 4"
        subprocess.run(command, capture_output=True, text=True, shell=True)

    # 点击Home键
    def home(self):
        command = self.adb_path + self.__device_str__ + f" shell am start -a android.intent.action.MAIN -c android.intent.category.HOME"
        subprocess.run(command, capture_output=True, text=True, shell=True)

    ## 打字(中英均可，不确定其他语言是否可以)，注意需要先在手机安装 adb 键盘
    def type(self, text):
        escaped_text = text.replace('"', '\\"').replace("'", "\\'")
        command_list = [
            f"shell ime enable com.android.adbkeyboard/.AdbIME ",
            f"shell ime set com.android.adbkeyboard/.AdbIME ",
            0.1,
            f'shell am broadcast -a ADB_INPUT_TEXT --es msg "{escaped_text}" ',
            0.1,
            f"shell ime disable com.android.adbkeyboard/.AdbIME"
        ]

        for command in command_list:
            if isinstance(command, float):
                time.sleep(command)
            elif isinstance(command, str):
                subprocess.run(self.adb_path + self.__device_str__ + command.strip(), capture_output=True, text=True, shell=True)

    def get_package_name(self, all_packages=False):
        try:
            if all_packages:
                command = self.adb_path + self.__device_str__ + " shell pm list packages"
            else:
                command = self.adb_path + self.__device_str__ + " shell pm list packages -3"
            res = subprocess.run(command, capture_output=True, text=True, shell=True)
            pkgs = []
            for line in res.stdout.splitlines():
                s = line.strip()
                if not s:
                    continue
                # 去掉前缀 "package:"
                if s.startswith("package:"):
                    s = s[len("package:"):]
                # 如果包含 "="，右侧才是包名
                if "=" in s:
                    _, s = s.split("=", 1)
                if s:
                    pkgs.append(s)
            return sorted(set(pkgs))
        except Exception as e:
            print(e)
            return []

    def open_app(self, package_name):
        command = self.adb_path + self.__device_str__ + f" shell monkey -p {package_name} -c android.intent.category.LAUNCHER 1"
        subprocess.run(command, capture_output=True, text=True, shell=True)
```

5.  **应用包名映射**
    
    包名是 Android 应用的唯一标识符（格式如：`com.公司名.产品名`，示例：`com.tencent.mm`（腾讯的微信，`mm = Mobile Messenger`）
    
    为了支持通过应用名称打开应用（`action=open`），需要维护应用名称到包名的映射。
    

```
# 常见应用包名映射（示例，可根据需要扩展）
package_str_list = '''com.tencent.mm	微信	wechat
com.tencent.mobileqq	qq	腾讯qq
com.sina.weibo	微博
com.taobao.taobao	淘宝
com.jingdong.app.mall	京东	京东秒送
com.xunmeng.pinduoduo	拼多多
com.xingin.xhs	小红书
com.douban.frodo	豆瓣
com.zhihu.android	知乎
com.autonavi.minimap	高德地图	高德
com.baidu.BaiduMap	百度地图
com.sankuai.meituan.takeoutnew	美团外卖
com.sankuai.meituan	美团	美团外卖
com.dianping.v1	大众点评	点评
me.ele	饿了么	淘宝闪购
com.yek.android.kfc.activitys	肯德基
ctrip.android.view	携程	携程旅行
com.MobileTicket	铁路12306	12306
com.Qunar	去哪儿旅行	去哪儿网	去哪儿
com.sdu.didi.psnger	滴滴出行	滴滴
tv.danmaku.bili	bilibili	b站	哔哩哔哩	哔站	bili
com.ss.android.ugc.aweme	抖音
com.smile.gifmaker	快手
com.tencent.qqlive	腾讯视频
com.qiyi.video	爱奇艺
com.youku.phone	优酷	优酷视频
com.hunantv.imgo.activity	芒果tv	芒果
com.phoenix.read	红果短剧	红果
com.netease.cloudmusic	网易云音乐	网易云
com.tencent.qqmusic	qq音乐
com.luna.music	汽水音乐
com.ximalaya.ting.android	喜马拉雅
com.dragon.read	番茄免费小说	番茄小说
com.kmxs.reader	七猫免费小说
com.ss.android.lark	飞书
com.tencent.androidqqmail	qq邮箱
com.larus.nova	豆包	豆包
com.gotokeep.keep	keep
com.lingan.seeyou	美柚
com.tencent.news	腾讯新闻
com.ss.android.article.news	今日头条
com.lianjia.beike	贝壳找房
com.anjuke.android.app	安居客
com.hexin.plat.android	同花顺
com.miHoYo.hkrpg	星穹铁道	崩坏
com.papegames.lysk.cn	恋与深空
com.android.settings	settings	androidsystemsettings
com.android.soundrecorder	audiorecorder
com.rammigsoftware.bluecoins	bluecoins
com.flauschcode.broccoli	broccoli
com.booking	booking
com.android.chrome	谷歌浏览器	googlechrome	chrome
com.android.deskclock	时钟	闹钟	clock
com.android.contacts	contacts
com.duolingo	duolingo	多邻国
com.expedia.bookings	expedia
com.android.fileexplorer	files	filemanager
com.google.android.gm	gmail	googlemail
com.google.android.apps.nbu.files	googlefiles	filesbygoogle
com.google.android.calendar	googlecalendar
com.google.android.apps.dynamite	googlechat
com.google.android.deskclock	googleclock
com.google.android.contacts	googlecontacts
com.google.android.apps.docs.editors.docs	googledocs
com.google.android.apps.docs	googledrive
com.google.android.apps.fitness	googlefit
com.google.android.keep	googlekeep
com.google.android.apps.maps	googlemaps
com.google.android.apps.books	googleplaybooks
com.android.vending	googleplaystore
com.google.android.apps.docs.editors.slides	googleslides
com.google.android.apps.tasks	googletasks
net.cozic.joplin	joplin
com.mcdonalds.app	麦当劳	mcdonald
net.osmand	osmand
com.Project100Pi.themusicplayer	pimusicplayer
com.quora.android	quora
com.reddit.frontpage	reddit
code.name.monkey.retromusic	retromusic
com.scientificcalculatorplus.simplecalculator.basiccalculator.mathcalc	simplecalendarpro
com.simplemobiletools.smsmessenger	simplesmsmessenger
org.telegram.messenger	telegram
com.einnovation.temu	temu
com.zhiliaoapp.musically	tiktok
com.twitter.android	twitter	x
org.videolan.vlc	vlc
com.whatsapp	whatsapp
com.taobao.movie.android	淘票票
com.tongcheng.android	同程旅行	同程
com.sankuai.movie	猫眼
com.wuba.zhuanzhuan	转转
com.tencent.weread	微信读书
com.taobao.idlefish	闲鱼
com.wudaokou.hippo	盒马
com.eg.android.AlipayGphone	支付宝
com.jd.jrapp	京东金融
com.achievo.vipshop	唯品会
com.smzdm.client.android	什么值得买
cn.kuwo.player	酷我音乐
com.taobao.trip	飞猪	飞猪旅行
com.jingdong.pdj	京东到家
com.tencent.map	腾讯地图
com.shizhuang.duapp	得物
cn.damai	大麦	大麦网
com.ss.android.auto	懂车帝
com.cubic.autohome	汽车之家
com.wuba	58同城	五八同城
com.android.calendar	日历
com.alibaba.android.rimet	钉钉
com.meituan.retail.v.android	小象超市
com.aliyun.tongyi	通义	千问	通义千问
com.hupu.games	虎扑	虎扑体育
com.quark.browser	夸克	夸克浏览器
com.yuantiku.tutor	猿辅导
com.tencent.mtt	qq浏览器
com.umetrip.android.msky.app	航旅纵横
com.UCMobile	UC浏览器
com.ss.android.ugc.aweme.lite	抖音极速版	抖音
air.tv.douyu.android	斗鱼
com.tencent.hunyuan.app.chat	元宝
com.baidu.searchbox	百度
com.lemon.lv	剪映
cn.soulapp.android	soul
com.baidu.netdisk	百度网盘
com.tmri.app.main	交管12123	12123
com.kugou.android	酷狗	酷狗音乐
com.ss.android.lark	飞书
com.tencent.android.qqdownloader	应用宝
com.mt.mtxx.mtxx	美图	美图秀秀
com.tencent.karaoke	全民k歌
com.intsig.camscanner	扫描全能王
com.android.bankabc	农业银行	农行
cmb.pb	招商银行	招行
com.ganji.android.haoche_c	瓜子二手车	瓜子
com.sf.activity	顺丰	顺丰快递	顺丰速运
com.ziroom.ziroomcustomer	自如
com.yumc.phsuperapp	必胜客
cn.dominos.pizza	达美乐披萨	达美乐
cn.wps.moffice_eng	WPS Office	WPS
com.mfw.roadbook	马蜂窝
com.moonshot.kimichat	kimi
com.tencent.wemeet.app	腾讯会议
com.deepseek.chat	deepseek
com.spdbccc.app	浦发银行
cn.samsclub.app	山姆超市	山姆	山姆会员商店	山姆会员店
com.tencent.qqsports	腾讯体育
com.hanweb.android.zhejiang.activity	浙里办
com.ss.android.article.video	西瓜视频
com.taou.maimai	脉脉	'''

PACKAGES_NAME_DICT = {}
NAME_PACKAGE_DICT = {}

def normalize_package_name(name):
    name = name.lower().strip().replace(" ", "").replace("-", "")
    return name

for package_str in package_str_list.split("\n"):
    package_name = package_str.strip().split("\t")
    PACKAGES_NAME_DICT[package_name[0]] = [normalize_package_name(i) for i in package_name[1:]]
    for name in package_name[1:]:
        name = normalize_package_name(name)
        if name not in NAME_PACKAGE_DICT:
            NAME_PACKAGE_DICT[name] = [package_name[0]]
        else:
            NAME_PACKAGE_DICT[name].append(package_name[0])
```

6.  **完整自动化流程**

```
import os
import uuid
import dashscope
import time
import shutil
import json
from PIL import Image

if __name__ == '__main__':

    add_info = ''
    ## 指定app，存在applist内，但本地有
    # instruction = '在携程订一张大后天上海到北京的高铁票'
    # instruction = '在虎扑里评论今天NBA比赛'
    # instruction = '航旅纵横帮我查一下明天的机票'
    # instruction = '猿辅导里看一下往年真题'

    ## 指定app，存在applist内，但本地没有
    # instruction = '在猫眼订一张周杰伦的演唱会门票'
    # instruction = '在小象超市里买一个柚子'
    # instruction = '在虎牙直播里看直播'
    # instruction = 'qq音乐播放许嵩的歌'

    ## 不指定app，但本地有
    # instruction = '导航到村里去'
    # instruction = '点一杯奶茶外卖'
    # instruction = '放一首许嵩的歌'
    instruction = '帮我订一张火车票'

    ## 不指定app，但本地没有
    # instruction = '在炒股软件里看看今天上证指数'
    # instruction = '帮我给老婆发一条消息，明天晚上不会去吃饭了'

    history = []
    session_id = str(uuid.uuid4())
    print('session_id ', session_id)
    max_step = 50

    model_name = 'gui-plus-2026-02-26'
    dashscope.api_key = os.getenv("DASHSCOPE_API_KEY", None)
    print("DashScope API Key: ", dashscope.api_key)
    # 以下为华北2（北京）地域的URL，，调用时请将WorkspaceId替换为真实的业务空间ID
    dashscope.base_http_api_url = 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1'

    ## 注意：需要用户填入自己的adb路径
    adb_tools = AdbTools(adb_path="xxx/adb")
    # package_name_list = adb_tools.get_package_name()
    # adb_tools.home()
    # time.sleep(1)
    task_dir = instruction
    anno_dir = f"{instruction}_anno"

    if os.path.exists(task_dir):
        shutil.rmtree(task_dir)
    os.mkdir(task_dir)

    if os.path.exists(anno_dir):
        shutil.rmtree(anno_dir)
    os.mkdir(anno_dir)

    ## {"image": 图片， "output": 模型输出}
    history = []
    open_app_retry = False
    # max_step = 1
    for step_id in range(max_step):
        print(f'\nSTEP {step_id}:\n------------------------------------')
        screen_shot = os.path.join(task_dir, f'screen_shot_{step_id}.png')
        adb_tools.get_screenshot(screen_shot)

        width, height = Image.open(screen_shot).size
        messages = get_messages(screen_shot, instruction, history, model_name)

        retry_time = 3
        for _ in range(retry_time):
            response = dashscope.MultiModalConversation.call(
                                                model=model_name,
                                                messages=messages,
                                                vl_high_resolution_images=True,
                                                headers={"x-dashscope-gui-session-id": session_id},
                                                enable_thinking=False,
                                                stream=False)
            print(response['request_id'])
            try:
                output_text = response.output.choices[0].message.content[0]['text']
                break
            except Exception as e:
                print(response)
                print(e)
        else:
            raise Exception('retry_time out')

        thought = response.output.choices[0].message.reasoning_content
        if thought != '':
            output_text = f"<think>\n{thought}\n</think>{output_text}"
        action = json.loads(output_text.split('<tool_call>\n')[1].split('}}\n')[0] + '}}\n')
        conclusion = output_text.split('<tool_call>')[0].strip()

        action_parameter = action['arguments']
        dummy_image = Image.open(screen_shot)
        resized_height, resized_width = smart_resize(dummy_image.height,
                                                     dummy_image.width,
                                                     factor=16,
                                                     min_pixels=3136,
                                                     max_pixels=1003520*200,
                                                     )
        for key in ['coordinate', 'coordinate1', 'coordinate2']:
            if key in action_parameter:
                action_parameter[key][0] = int(action_parameter[key][0]/1000 * resized_width)
                action_parameter[key][1] = int(action_parameter[key][1]/1000 * resized_height)

        print(output_text)
        action_type = action_parameter['action']
        if action_type == 'click':
            adb_tools.click(action_parameter['coordinate'][0],
                            action_parameter['coordinate'][1])
        elif action_type == 'long_press':
            adb_tools.long_press(action_parameter['coordinate'][0],
                                 action_parameter['coordinate'][1])
        elif action_type == 'type':
            adb_tools.type(action_parameter['text'])
        elif action_type in ['scroll', 'swipe']:
            adb_tools.slide(action_parameter['coordinate'][0],
                            action_parameter['coordinate'][1],
                            action_parameter['coordinate2'][0],
                            action_parameter['coordinate2'][1])
        elif action_type == 'system_button':
            system = action_parameter['button']
            if system == 'Back':
                adb_tools.back()
            elif system == 'Home':
                adb_tools.home()
        elif action_type == 'wait':
            time.sleep(2)
        elif action_type == 'terminate':
            print(f'动作已完成')
            break
        elif action_type == 'open':
            app_name = action_parameter['text']
            package_name = NAME_PACKAGE_DICT.get(app_name, [])
            package_name_list = adb_tools.get_package_name()
            output_app_name = ''
            if app_name != '':
                output_app_name = app_name
            for sub_package_name in package_name:
                if sub_package_name in package_name_list:
                    adb_tools.open_app(sub_package_name)
                    break
            else:
                input(f"请安装相关APP {output_app_name}")
                continue

        elif action_type == 'answer':
            print(f'Answer: {conclusion}\n动作已完成')
            break
        elif action_type in ['call_user', 'calluser', 'interact']:
            text = action_parameter['text']
            input(f"请完成{text}相关动作")
            print("动作已完成，继续运行")
            pass
        else:
            raise Exception(f"mobile-e2e action_type not supported {action}")

        history.append({'output': output_text,
                        'image': screen_shot})
        show_screenshot(screen_shot, action_parameter, f"{anno_dir}/screenshot_anno_{step_id}.png")
        time.sleep(2)
```

手机端完整示例代码

```
import os
import re
import json
import math
import time
import uuid
import shutil
import subprocess
import dashscope
from PIL import Image
from datetime import datetime

# ===================== 步骤1：System Prompt =====================

mobile_system_prompt = '''# Tools

You may call one or more functions to assist with the user query.

You are provided with function signatures within <tools></tools> XML tags:
<tools>
{"type": "function", "function": {"name_for_human": "mobile_use", "name": "mobile_use", "description": "Use a touchscreen to interact with a mobile device, and take screenshots.\\n* This is an interface to a mobile device with touchscreen. You can perform actions like clicking, typing, swiping, etc.\\n* Some applications may take time to start or process actions, so you may need to wait and take successive screenshots to see the results of your actions.\\n* The screen's resolution is 1000x1000.\\n* Make sure to click any buttons, links, icons, etc with the cursor tip in the center of the element. Don't click boxes on their edges unless asked.", "parameters": {"properties": {"action": {"description": "The action to perform. The available actions are:\\n* `key`: Perform a key event on the mobile device.\\n    - This supports adb's `keyevent` syntax.\\n    - Examples: \\"volume_up\\", \\"volume_down\\", \\"power\\", \\"camera\\", \\"clear\\".\\n* `click`: Click the point on the screen with coordinate (x, y).\\n* `long_press`: Press the point on the screen with coordinate (x, y) for specified seconds.\\n* `swipe`: Swipe from the starting point with coordinate (x, y) to the end point with coordinates2 (x2, y2).\\n* `type`: Input the specified text into the activated input box.\\n* `system_button`: Press the system button.\\n* `open`: Open an app on the device.\\n* `wait`: Wait specified seconds for the change to happen.\\n* `answer`: Terminate the current task and output the answer.\\n* `interact`: Resolve the blocking window by interacting with the user.\\n* `terminate`: Terminate the current task and report its completion status.", "enum": ["key", "click", "long_press", "swipe", "type", "system_button", "open", "wait", "answer", "interact", "terminate"], "type": "string"}, "coordinate": {"description": "(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by `action=click`, `action=long_press`, and `action=swipe`.", "type": "array"}, "coordinate2": {"description": "(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by `action=swipe`.", "type": "array"}, "text": {"description": "Required only by `action=key`, `action=type`, `action=open`, `action=answer`,and `action=interact`.", "type": "string"}, "time": {"description": "The seconds to wait. Required only by `action=long_press` and `action=wait`.", "type": "number"}, "button": {"description": "Back means returning to the previous interface, Home means returning to the desktop, Menu means opening the application background menu, and Enter means pressing the enter. Required only by `action=system_button`", "enum": ["Back", "Home", "Menu", "Enter"], "type": "string"}, "status": {"description": "The status of the task. Required only by `action=terminate`.", "type": "string", "enum": ["success", "failure"]}}, "required": ["action"], "type": "object"}, "args_format": "Format the arguments as a JSON object."}}
</tools>

For each function call, return a json object with function name and arguments within <tool_call></tool_call> XML tags:
<tool_call>
{"name": <function-name>, "arguments": <args-json-object>}
</tool_call>

# Response format

Response format for every step:
1) Action: a short imperative describing what to do in the UI.
2) A single <tool_call>...</tool_call> block containing only the JSON: {"name": <function-name>, "arguments": <args-json-object>}.

Rules:
- Output exactly in the order: Action, <tool_call>.
- Be brief: one for Action.
- Do not output anything else outside those two parts.
- If finishing, use action=terminate in the tool call.'''

# ===================== 步骤2：构造多轮对话消息 =====================

def get_messages(image, instruction, history_output, system_prompt):
    history_n = 4
    current_step = len(history_output)
    history_start_idx = max(0, current_step - history_n)

    previous_actions = []
    for i in range(history_start_idx):
        if i < len(history_output):
            history_output_str = history_output[i]['output']
            if 'Action:' in history_output_str and '<tool_call>':
                history_output_str = history_output_str.split('Action:')[1].split('<tool_call>')[0].strip()
            previous_actions.append(f"Step {i + 1}: {history_output_str}")

    previous_actions_str = "\\n".join(previous_actions) if previous_actions else "None"

    # 添加背景信息
    today = datetime.today()
    weekday_names = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    weekday = weekday_names[today.weekday()]
    formatted_date = today.strftime("%Y年%m月%d日") + " " + weekday
    ground_info = f'''今天的日期是:{formatted_date}。'''

    instruction_prompt = f"""
Please generate the next move according to the UI screenshot, instruction and previous actions.

Instruction: {ground_info}{instruction}

Previous actions:
{previous_actions_str}"""

    messages = [{"role": "system", "content": [{"text": system_prompt}]}]

    history_len = min(history_n, len(history_output))
    if history_len > 0:
        for history_id, history_item in enumerate(history_output[-history_n:], 0):
            if history_id == 0:
                messages.append({
                    "role": "user",
                    "content": [
                        {"text": instruction_prompt},
                        {"image": "file://" + history_item['image']}
                    ]
                })
            else:
                messages.append({
                    "role": "user",
                    "content": [{"image": "file://" + history_item['image']}]
                })
            messages.append({
                "role": "assistant",
                "content": [{"text": history_item['output']}],
            })
        messages.append({
            "role": "user",
            "content": [{"image": "file://" + image}]
        })
    else:
        messages.append({
            "role": "user",
            "content": [
                {"text": instruction_prompt},
                {"image": "file://" + image}
            ]
        })
    return messages

# ===================== 步骤3：解析模型输出与坐标映射 =====================

def extract_tool_calls(text):
    pattern = re.compile(r'<tool_call>(.*?)</tool_call>', re.DOTALL | re.IGNORECASE)
    blocks = pattern.findall(text)
    actions = []
    for blk in blocks:
        blk = blk.strip()
        try:
            actions.append(json.loads(blk))
        except json.JSONDecodeError as e:
            print(f'解析失败: {e} | 片段: {blk[:80]}...')
    return actions

def smart_resize(height, width, factor=32, min_pixels=32*32*4, max_pixels=32*32*1280, max_long_side=8192):
    def round_by_factor(number, factor):
        return round(number / factor) * factor
    def ceil_by_factor(number, factor):
        return math.ceil(number / factor) * factor
    def floor_by_factor(number, factor):
        return math.floor(number / factor) * factor

    if height < 2 or width < 2:
        raise ValueError(f"height:{height} or width:{width} must be larger than factor:{factor}")
    if max(height, width) > max_long_side:
        beta = max(height, width) / max_long_side
        height, width = int(height / beta), int(width / beta)

    h_bar = round_by_factor(height, factor)
    w_bar = round_by_factor(width, factor)

    if h_bar * w_bar > max_pixels:
        beta = math.sqrt((height * width) / max_pixels)
        h_bar = floor_by_factor(height / beta, factor)
        w_bar = floor_by_factor(width / beta, factor)
    elif h_bar * w_bar < min_pixels:
        beta = math.sqrt(min_pixels / (height * width))
        h_bar = ceil_by_factor(height * beta, factor)
        w_bar = ceil_by_factor(width * beta, factor)
    return h_bar, w_bar

# ===================== 步骤4：ADB 操作工具类 =====================

class AdbTools:
    def __init__(self, adb_path, device=None):
        self.adb_path = adb_path
        self.device = device
        self.__device_str__ = f" -s {device} " if device is not None else ' '
        self.image_info = None

    def adb_shell(self, command):
        command = self.adb_path + self.__device_str__ + command
        subprocess.run(command, capture_output=True, text=True, shell=True)

    def load_image_info(self, path):
        width, height = Image.open(path).size
        self.image_info = (width, height)

    def get_screenshot(self, image_path, retry_times=3):
        command = self.adb_path + (f" -s {self.device}" if self.device is not None else '') + f" exec-out screencap -p > {image_path}"
        for i in range(retry_times):
            subprocess.run(command, capture_output=True, text=True, shell=True)
            if os.path.exists(image_path):
                self.load_image_info(image_path)
                return True
            else:
                time.sleep(0.1)
        return False

    def click(self, x, y, coordinate_size=None):
        command = self.adb_path + self.__device_str__ + f" shell input tap {x} {y}"
        subprocess.run(command, capture_output=True, text=True, shell=True)

    def long_press(self, x, y, time=800):
        command = self.adb_path + self.__device_str__ + f" shell input swipe {x} {y} {x} {y} {time}"
        subprocess.run(command, capture_output=True, text=True, shell=True)

    def slide(self, x1, y1, x2, y2, coordinate_size=None, slide_time=800):
        command = self.adb_path + self.__device_str__ + f" shell input swipe {x1} {y1} {x2} {y2} {slide_time}"
        subprocess.run(command, capture_output=True, text=True, shell=True)

    def back(self):
        command = self.adb_path + self.__device_str__ + f"  shell input keyevent 4"
        subprocess.run(command, capture_output=True, text=True, shell=True)

    def home(self):
        command = self.adb_path + self.__device_str__ + f" shell am start -a android.intent.action.MAIN -c android.intent.category.HOME"
        subprocess.run(command, capture_output=True, text=True, shell=True)

    def type(self, text):
        escaped_text = text.replace('"', '\\"').replace("'", "\\'")
        command_list = [
            f"shell ime enable com.android.adbkeyboard/.AdbIME ",
            f"shell ime set com.android.adbkeyboard/.AdbIME ",
            0.1,
            f'shell am broadcast -a ADB_INPUT_TEXT --es msg "{escaped_text}" ',
            0.1,
            f"shell ime disable com.android.adbkeyboard/.AdbIME"
        ]
        for command in command_list:
            if isinstance(command, float):
                time.sleep(command)
            elif isinstance(command, str):
                subprocess.run(self.adb_path + self.__device_str__ + command.strip(), capture_output=True, text=True, shell=True)

    def get_package_name(self, all_packages=False):
        try:
            if all_packages:
                command = self.adb_path + self.__device_str__ + " shell pm list packages"
            else:
                command = self.adb_path + self.__device_str__ + " shell pm list packages -3"
            res = subprocess.run(command, capture_output=True, text=True, shell=True)
            pkgs = []
            for line in res.stdout.splitlines():
                s = line.strip()
                if not s:
                    continue
                if s.startswith("package:"):
                    s = s[len("package:"):]
                if "=" in s:
                    _, s = s.split("=", 1)
                if s:
                    pkgs.append(s)
            return sorted(set(pkgs))
        except Exception as e:
            print(e)
            return []

    def open_app(self, package_name):
        command = self.adb_path + self.__device_str__ + f" shell monkey -p {package_name} -c android.intent.category.LAUNCHER 1"
        subprocess.run(command, capture_output=True, text=True, shell=True)

# ===================== 步骤5：应用包名映射 =====================

package_str_list = '''com.tencent.mm\t微信\twechat\t\t\t
com.tencent.mobileqq\tqq\t腾讯qq\t\t\t
com.sina.weibo\t微博\t\t\t\t
com.taobao.taobao\t淘宝\t\t\t\t
com.jingdong.app.mall\t京东\t京东秒送\t\t\t
com.xunmeng.pinduoduo\t拼多多\t\t\t\t
com.xingin.xhs\t小红书\t\t\t\t
com.douban.frodo\t豆瓣\t\t\t\t
com.zhihu.android\t知乎\t\t\t\t
com.autonavi.minimap\t高德地图\t高德\t\t\t
com.baidu.BaiduMap\t百度地图\t\t\t\t
com.sankuai.meituan.takeoutnew\t美团外卖\t\t\t\t
com.sankuai.meituan\t美团\t美团外卖\t\t\t
com.dianping.v1\t大众点评\t点评\t\t\t
me.ele\t饿了么\t淘宝闪购\t\t\t
com.yek.android.kfc.activitys\t肯德基\t\t\t\t
ctrip.android.view\t携程\t携程旅行\t\t\t
com.MobileTicket\t铁路12306\t12306\t\t\t
com.Qunar\t去哪儿旅行\t去哪儿网\t去哪儿\t\t
com.sdu.didi.psnger\t滴滴出行\t滴滴\t\t\t
tv.danmaku.bili\tbilibili\tb站\t哔哩哔哩\t哔站\tbili
com.ss.android.ugc.aweme\t抖音\t\t\t\t
com.smile.gifmaker\t快手\t\t\t\t
com.tencent.qqlive\t腾讯视频\t\t\t\t
com.qiyi.video\t爱奇艺\t\t\t\t
com.youku.phone\t优酷\t优酷视频\t\t\t
com.hunantv.imgo.activity\t芒果tv\t芒果\t\t\t
com.phoenix.read\t红果短剧\t红果\t\t\t
com.netease.cloudmusic\t网易云音乐\t网易云\t\t\t
com.tencent.qqmusic\tqq音乐\t\t\t\t
com.luna.music\t汽水音乐\t\t\t\t
com.ximalaya.ting.android\t喜马拉雅\t\t\t\t
com.dragon.read\t番茄免费小说\t番茄小说\t\t\t
com.kmxs.reader\t七猫免费小说\t\t\t\t
com.ss.android.lark\t飞书\t\t\t\t
com.tencent.androidqqmail\tqq邮箱\t\t\t\t
com.larus.nova\t豆包\t豆包\t\t\t
com.gotokeep.keep\tkeep\t\t\t\t
com.lingan.seeyou\t美柚\t\t\t\t
com.tencent.news\t腾讯新闻\t\t\t\t
com.ss.android.article.news\t今日头条\t\t\t\t
com.lianjia.beike\t贝壳找房\t\t\t\t
com.anjuke.android.app\t安居客\t\t\t\t
com.hexin.plat.android\t同花顺\t\t\t\t
com.miHoYo.hkrpg\t星穹铁道\t崩坏\t\t\t
com.papegames.lysk.cn\t恋与深空\t\t\t\t'''

PACKAGES_NAME_DICT = {}
NAME_PACKAGE_DICT = {}

def normalize_package_name(name):
    name = name.lower().strip().replace(" ", "").replace("-", "")
    return name

for package_str in package_str_list.split("\\n"):
    package_name = package_str.strip().split("\\t")
    if len(package_name) < 2:
        continue
    package, *app_names = package_name
    PACKAGES_NAME_DICT[package] = [normalize_package_name(n) for n in app_names if n.strip()]
    for app_name in app_names:
        if not app_name.strip():
            continue
        normalized_name = normalize_package_name(app_name)
        if normalized_name not in NAME_PACKAGE_DICT:
            NAME_PACKAGE_DICT[normalized_name] = []
        NAME_PACKAGE_DICT[normalized_name].append(package)

# ===================== 步骤6：完整自动化流程 =====================

if __name__ == '__main__':
    instruction = '帮我订一张火车票'  # 可修改为其他任务
    history = []
    session_id = str(uuid.uuid4())
    print('session_id ', session_id)
    max_step = 50

    model_name = 'gui-plus-2026-02-26'
    dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")
    # 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID
    dashscope.base_http_api_url = 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1'

    # 注意：需要填入自己的adb路径
    adb_tools = AdbTools(adb_path="/path/to/adb")  # 修改为实际路径
    # adb_tools.home()
    # time.sleep(1)

    task_dir = instruction
    if os.path.exists(task_dir):
        shutil.rmtree(task_dir)
    os.mkdir(task_dir)

    print(f"[任务] {instruction}")
    print("=" * 60)

    for step_id in range(max_step):
        print(f'\\n[步骤 {step_id + 1}]')

        screen_shot = os.path.join(task_dir, f'screen_shot_{step_id}.png')
        adb_tools.get_screenshot(screen_shot)

        messages = get_messages(screen_shot, instruction, history, mobile_system_prompt)

        retry_time = 3
        for _ in range(retry_time):
            response = dashscope.MultiModalConversation.call(
                model=model_name,
                messages=messages,
                vl_high_resolution_images=True,
                headers={"x-dashscope-gui-session-id": session_id},
                stream=False
            )
            print(response['request_id'])
            try:
                output_text = response.output.choices[0].message.content[0]['text']
                break
            except Exception as e:
                print(response)
                print(e)
        else:
            raise Exception('retry_time out')
        print(f"[模型输出]\\n{output_text}\\n")

        actions = extract_tool_calls(output_text)
        if not actions:
            print("未提取到有效操作")
            break

        action = actions[0]
        action_parameter = action['arguments']

        dummy_image = Image.open(screen_shot)
        resized_height, resized_width = smart_resize(
            dummy_image.height, dummy_image.width,
            factor=16, min_pixels=3136, max_pixels=1003520*200
        )

        for key in ['coordinate', 'coordinate1', 'coordinate2']:
            if key in action_parameter:
                action_parameter[key][0] = int(action_parameter[key][0] / 1000 * resized_width)
                action_parameter[key][1] = int(action_parameter[key][1] / 1000 * resized_height)

        action_type = action_parameter['action']
        if action_type == 'click':
            adb_tools.click(action_parameter['coordinate'][0], action_parameter['coordinate'][1])
            print(f"✓ 点击 ({action_parameter['coordinate'][0]}, {action_parameter['coordinate'][1]})")
        elif action_type == 'long_press':
            adb_tools.long_press(action_parameter['coordinate'][0], action_parameter['coordinate'][1])
            print(f"✓ 长按")
        elif action_type == 'type':
            adb_tools.type(action_parameter['text'])
            print(f"✓ 输入文本: {action_parameter['text']}")
        elif action_type in ['scroll', 'swipe']:
            adb_tools.slide(action_parameter['coordinate'][0], action_parameter['coordinate'][1],
                           action_parameter['coordinate2'][0], action_parameter['coordinate2'][1])
            print(f"✓ 滑动")
        elif action_type == 'system_button':
            system = action_parameter['button']
            if system == 'Back':
                adb_tools.back()
                print(f"✓ 返回")
            elif system == 'Home':
                adb_tools.home()
                print(f"✓ 主页")
        elif action_type == 'wait':
            time.sleep(2)
            print(f"✓ 等待")
        elif action_type == 'terminate':
            print(f'✓ 任务完成')
            break
        elif action_type == 'open':
            app_name = action_parameter['text']
            normalized_name = normalize_package_name(app_name)
            package_name = NAME_PACKAGE_DICT.get(normalized_name, [])
            package_name_list = adb_tools.get_package_name()
            for sub_package_name in package_name:
                if sub_package_name in package_name_list:
                    adb_tools.open_app(sub_package_name)
                    print(f"✓ 打开应用: {app_name}")
                    break
            else:
                print(f"⚠ 未找到应用: {app_name}，请手动安装")
                continue
        elif action_type == 'answer':
            print(f'✓ 任务完成: {action_parameter.get("text", "")}')
            break
        elif action_type in ['call_user', 'calluser', 'interact']:
            print(f"⚠ 需要用户交互: {action_parameter.get('text', '')}")
            input("请完成相关操作后按Enter继续...")
        else:
            print(f"✗ 未知操作类型: {action_type}")

        history.append({'output': output_text, 'image': screen_shot})
        time.sleep(2)

    print("\\n" + "=" * 60)
    print(f"[完成] 共执行 {len(history)} 步")
```

### 浏览器 GUI 任务

浏览器端通过 Playwright 控制浏览器实现自动化操作，并结合 SoM（Set-of-Mark）技术为页面元素自动添加数字标签，模型通过标签编号来精确操作网页元素。

**环境准备：**

1.  安装依赖：`pip install playwright pillow dashscope playwright-stealth termcolor`
2.  安装 Playwright 浏览器：`playwright install chromium`

完整示例代码包含以下核心流程：构造多轮对话消息、解析模型输出的工具调用、执行浏览器 GUI 操作。完整示例代码如下：

浏览器端完整示例代码

1.  **构造 System Prompt**

```
import json, os, base64
import dashscope, time, math
import uuid
from PIL import Image, ImageDraw, ImageTk
import asyncio
from playwright.async_api import async_playwright, Page, Browser, BrowserContext
from datetime import datetime

# 定义动作显示函数
def show_screenshot(image_path, action_parameter, save_path="screenshot_anno.png"):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    if 'coordinate' in action_parameter:
        radius = 15
        center_x, center_y = action_parameter['coordinate'][0], action_parameter['coordinate'][1]
        draw.ellipse((center_x - radius, center_y - radius, center_x + radius, center_y + radius),
                     fill="red", outline="red")
    elif 'coordinate1' in action_parameter and 'coordinate2' in action_parameter:
        x1, y1 = action_parameter['coordinate1'][0], action_parameter['coordinate1'][1]
        x2, y2 = action_parameter['coordinate2'][0], action_parameter['coordinate2'][1]
        arrow_size = 10
        color = 'red'
        draw.line((x1, y1, x2, y2), fill=color, width=2)
        angle = math.atan2(y2 - y1, x2 - x1)
        arrow_x1 = x2 - arrow_size * math.cos(angle - math.pi / 6)
        arrow_y1 = y2 - arrow_size * math.sin(angle - math.pi / 6)
        arrow_x2 = x2 - arrow_size * math.cos(angle + math.pi / 6)
        arrow_y2 = y2 - arrow_size * math.sin(angle + math.pi / 6)
        draw.polygon([(x2, y2), (arrow_x1, arrow_y1), (arrow_x2, arrow_y2)], fill=color)
    else:
        return None
    image.save(save_path)
    return save_path

# Prompt拼装函数
def get_messages(image, env_state, instruction, history_output):
    history_n = 1
    current_step = len(history_output)
    history_start_idx = max(0, current_step - history_n)
    SoM_format_ele_text = env_state["SoM"]["format_ele_text"]

    system_prompt = '''# Tools

You may call one or more functions to assist with the user query.

You are provided with function signatures within <tools></tools> XML tags:
<tools>
{"type": "function", "function": {"name_for_human": "browser_use", "name": "browser_use", "description": "Use a browser to interact with web pages and take labeled screenshots.\\n* This is an interface to a web browser. You can click elements, type into inputs, scroll, wait for loading, go back, etc.\\n* Each Observation screenshot contains Numerical Labels placed at the TOP LEFT of each Web Element. Use these labels to target elements.\\n* Some pages may take time to load; you may need to wait and take successive screenshots.\\n* Avoid clicking near element edges; target the center of the element.\\n* Execute exactly ONE interaction action per step; do not chain multiple interactions in one call.", "parameters": {"properties": {"action": {"description": "The action to perform. The available actions are:\\n* `click`: Click a web element by numerical label.\\n* `type`: Clear existing content in a textbox/input and type content. The system will automatically press ENTER after typing.\\n* `scroll`: Scroll within WINDOW or within a specific scrollable element/area (by label).\\n* `select`: Selects a specific option from a menu or dropdown. Use the option text provided in the textual information.\\n* `wait`: Wait for page processes to finish (default 5 seconds unless specified).\\n* `go_back`: Go back to the previous page.\\n* `wikipedia`: Directly jump to the Wikipedia homepage to search for information.\\n* `answer`: Terminate the current task and output the final answer.", "enum": ["click", "type", "scroll", "select", "wait", "go_back", "wikipedia", "answer"], "type": "string"}, "label": {"description": "Numerical label of the target web element. Required only by `action=click`, `action=type`, `action=scroll`, and `action=select` when scrolling within a specific area. Use string value `WINDOW` to scroll the whole page.", "type": ["integer", "string"]}, "direction": {"description": "Scroll direction. Required only by `action=scroll`.", "enum": ["up", "down"], "type": "string"}, "text": {"description": "Required only by `action=type` and `action=answer`.", "type": "string"}, "option": {"description": "The option to select. Required only by `action=select`", "type": "string"}, "time": {"description": "The seconds to wait. Required only by `action=wait` when overriding the default.", "type": "integer"}}, "required": ["action"], "type": "object"}, "args_format": "Format the arguments as a JSON object."}}
</tools>

For each function call, return a json object with function name and arguments within <tool_call></tool_call> XML tags:
<tool_call>
{"name": <function-name>, "arguments": <args-json-object>}
</tool_call>

# Response format

Response format for every step:
1) Action: a short imperative describing what to do in the UI.
2) A single <tool_call>...</tool_call> block containing only the JSON: {"name": <function-name>, "arguments": <args-json-object>}.

Rules:
- Output exactly in the order: Action, <tool_call>.
- Be brief: one line for Action.
- Do not output anything else outside those two parts.
- Execute ONLY ONE interaction per iteration (one tool call).
- If finishing, use action=answer in the tool call.'''

    today = datetime.today()
    weekday_names = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    weekday = weekday_names[today.weekday()]
    formatted_date = today.strftime("%Y年%m月%d日") + " " + weekday
    day_info = f'''今天的日期是:{formatted_date}。'''

    previous_actions = []
    for i in range(history_start_idx):
        if i < len(history_output):
            history_output_str = history_output[i]['output']
            if 'Action:' in history_output_str and '<tool_call>':
                history_output_str = history_output_str.split('Action:')[1].split('<tool_call>')[0].strip()
            previous_actions.append(f"Step {i + 1}: {history_output_str}")

    previous_actions_str = (
        "\\n".join(previous_actions) if previous_actions else "None"
    )

    instruction_prompt = f'''\nPlease generate the next move according to the UI screenshot, instruction and previous actions.

Instruction: {day_info}{instruction}

Previous actions:
{previous_actions_str}'''

    messages = [
        {
            "role": "system",
            "content": [
                {"text": system_prompt}
            ],
        }
    ]
    history_len = min(history_n, len(history_output))
    if history_len > 0:
        for history_id, history_item in enumerate(history_output[-history_n:], 0):
            if history_id == 0:
                messages.append({
                    "role": "user",
                    "content": [
                        {"text": instruction_prompt},
                        {"text": "Current screenshot:"},
                        {"image": "file://" + history_item['image']},
                    ]
                })
            else:
                messages.append({
                    "role": "user",
                    "content": [
                        {"text": "Current screenshot:"},
                        {"image": "file://" + history_item['image']}
                    ]
                })
            messages.append({
                "role": "assistant",
                "content": [
                    {"text": history_item['output']},
                ]
            })
        messages.append({
            "role": "user",
            "content": [
                {"image": "file://" +image},
                {"text": SoM_format_ele_text}
            ]
        })
    else:
        messages.append(
            {
                "role": "user",
                "content": [
                    {
                        "text": instruction_prompt
                    },
                    {
                        "image": "file://" +image,
                    },
                    {"text": SoM_format_ele_text}
                ],
            }
        )

    return messages

def extract_tool_calls(text: str):
    import re, ast
    """从文本中提取所有 <tool_call> ... </tool_call> 之间的 JSON 字符串"""
    pattern = re.compile(r'<tool_call>(.*?)</tool_call>', re.DOTALL | re.IGNORECASE)
    blocks = pattern.findall(text)

    actions = []
    for blk in blocks:
        blk = blk.strip()
        try:
            actions.append(ast.literal_eval(blk))
        except json.JSONDecodeError as e:
            print(f'⚠️ 解析失败: {e} | 片段: {blk[:80]}...')
    return actions
```

2.  **浏览器控制**

```
PLAYWRIGHT_KEY_MAP = {
    "backspace": "Backspace", "tab": "Tab", "return": "Enter", "enter": "Enter",
    "shift": "Shift", "control": "ControlOrMeta", "alt": "Alt", "escape": "Escape",
    "space": "Space", "pageup": "PageUp", "pagedown": "PageDown", "end": "End",
    "home": "Home", "left": "ArrowLeft", "up": "ArrowUp", "right": "ArrowRight",
    "down": "ArrowDown", "insert": "Insert", "delete": "Delete", "semicolon": ";",
    "equals": "=", "multiply": "Multiply", "add": "Add", "separator": "Separator",
    "subtract": "Subtract", "decimal": "Decimal", "divide": "Divide",
    "f1": "F1", "f2": "F2", "f3": "F3", "f4": "F4", "f5": "F5", "f6": "F6",
    "f7": "F7", "f8": "F8", "f9": "F9", "f10": "F10", "f11": "F11", "f12": "F12",
    "command": "Meta",
}

class PlaywrightComputer:
    """Async Playwright wrapper for web agent"""

    def __init__(self, initial_url="https://baidu.com/", task_dir='data', highlight_mouse=False):
        self._initial_url = initial_url
        self._search_engine_url = "https://baike.baidu.com/"
        self.task_dir = task_dir
        self._highlight_mouse = highlight_mouse

        self._playwright = None
        self._browser: Browser | None = None
        self._context: BrowserContext | None = None
        self._page: Page | None = None
        self._storage_state_path = "storage_state.json"

    async def _handle_new_page(self, new_page: Page):
        """Only keep one tab: redirect new tab url into current page"""
        new_url = new_page.url
        await new_page.close()
        try:
            await self._page.goto(new_url)
        except Exception as e:
            if "interrupted by another navigation" in str(e):
                pass
            else:
                raise

    async def reset(self):
        print("Creating session...")
        self._playwright = await async_playwright().start()
        self._browser = await self._playwright.chromium.launch(
            args=["--start-maximized", "--disable-blink-features=AutomationControlled"],
            headless=False,
        )

        storage_state = None
        if os.path.exists(self._storage_state_path):
            print("Loadding storage state")
            storage_state = self._storage_state_path

        if sys.platform == "darwin":
            user_agent = (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 "
                "Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0 "
            )
            import tkinter as tk
            root = tk.Tk()
            root.withdraw()
            width = root.winfo_screenwidth()
            height = root.winfo_screenheight()
            print(f"Screen size: {width}x{height}", flush=True)
            root.destroy()
            self._context = await self._browser.new_context(
                no_viewport=True,
                user_agent=user_agent,
                locale="en-US",
                timezone_id="America/New_York",
                storage_state=storage_state,
            )
        else:
            user_agent = (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            )
            self._context = await self._browser.new_context(
                no_viewport=True,
                user_agent=user_agent,
                locale="en-US",
                timezone_id="America/New_York",
                storage_state=storage_state,
            )

        self._page = await self._context.new_page()
        await self._page.goto(self._initial_url, timeout=60000, wait_until="domcontentloaded")
        self._context.on("page", lambda p: asyncio.create_task(self._handle_new_page(p)))
        print("Started local playwright (async).")
        return self

    async def close(self):
        if self._context:
            try:
                await self._context.storage_state(path=self._storage_state_path)
            except Exception as e:
                print(f"Failed to save storage state: {e}")

        if self._context:
            await self._context.close()
        try:
            if self._browser:
                await self._browser.close()
        except Exception as e:
            if "Browser.close: Connection closed while reading from the driver" in str(e):
                pass
            else:
                raise
        if self._playwright:
            await self._playwright.stop()

    async def click_at(self, x: int, y: int):
        await self._page.mouse.click(x, y)
        await self._page.mouse.move(x, y)
        await self._page.mouse.down()
        await self._page.wait_for_timeout(100)
        await self._page.mouse.up()
        await self._page.wait_for_load_state()

    async def type_text_at(self, x: int, y: int, text: str, press_enter=True, clear_before_typing=True):
        await self.click_at(x, y)
        await asyncio.sleep(0.1)
        await self._page.wait_for_load_state()

        if clear_before_typing:
            if sys.platform == "darwin":
                await self.key_combination(["Command", "A"])
            else:
                await self.key_combination(["Control", "A"])
            await asyncio.sleep(0.1)
            await self.key_combination(["Delete"])
            await self._page.wait_for_load_state()

        await self.click_at(x, y)
        await asyncio.sleep(0.1)
        await self._page.keyboard.type(text)
        await self._page.wait_for_load_state()

        if press_enter:
            await self.key_combination(["Enter"])
        await self._page.wait_for_load_state()

    async def scroll_at(self, x: int, y: int, direction: str, magnitude: int = 400):
        await self._page.mouse.move(x, y)
        await asyncio.sleep(0.1)

        dx = dy = 0
        if direction == "up":
            dy = -magnitude
        elif direction == "down":
            dy = magnitude
        elif direction == "left":
            dx = -magnitude
        elif direction == "right":
            dx = magnitude
        else:
            raise ValueError("Unsupported direction: ", direction)

        await self._page.mouse.wheel(dx, dy)
        await self._page.wait_for_load_state()

    async def go_back(self):
        await self._page.go_back()
        await self._page.wait_for_load_state()

    async def navigate(self, url: str, normalize=True):
        normalized_url = url
        if normalize and not normalized_url.startswith(("http://", "https://")):
            normalized_url = "https://" + normalized_url
        await self._page.goto(normalized_url)
        await self._page.wait_for_load_state()

    async def key_combination(self, keys: list[str]):
        keys = [PLAYWRIGHT_KEY_MAP.get(k.lower(), k) for k in keys]
        for key in keys[:-1]:
            await self._page.keyboard.down(key)
        await self._page.keyboard.press(keys[-1])
        for key in reversed(keys[:-1]):
            await self._page.keyboard.up(key)

    async def current_state(self, it):
        try:
            await self._page.wait_for_load_state("networkidle", timeout=10000)
        except Exception:
            try:
                await self._page.wait_for_load_state("load", timeout=5000)
            except:
                pass

        await asyncio.sleep(1)

        os.makedirs(os.path.join(self.task_dir, "trajectory_som"), exist_ok=True)
        os.makedirs(os.path.join(self.task_dir, "trajectory"), exist_ok=True)
        img_path = os.path.join(self.task_dir, f"trajectory_som/screenshot{it}.png")
        img_path_no_box = os.path.join(self.task_dir, f"trajectory/{it}_full_screenshot.png")

        SoM_list, format_ele_text = await get_som(self._page, img_path, img_path_no_box)
        width, height = Image.open(img_path).size
        return {
            "img_path": img_path,
            "img_path_no_box": img_path_no_box,
            "SoM": {
                "SoM_list": SoM_list,
                "format_ele_text": format_ele_text
            },
            "current_url": self._page.url,
            "width": width,
            "height": height
        }

    async def _select(self, x, y, text):
        await self._page.mouse.click(x, y)
        target_text = text
        handle = await self._page.evaluate_handle("""
        ([x,y]) => document.elementFromPoint(x,y)
        """, [x, y])

        tag = await handle.evaluate("el => el && el.tagName")
        if tag == "SELECT":
            await handle.evaluate("""(sel, label) => {
                const opt = [...sel.options].find(o => o.label.trim() === label.trim());
                if (!opt) throw new Error("找不到选项: " + label);
                sel.value = opt.value;
                sel.dispatchEvent(new Event('input', {bubbles:true}));
                sel.dispatchEvent(new Event('change', {bubbles:true}));
            }""", target_text)
        else:
            raise RuntimeError(f"坐标处元素不是 SELECT，而是 {tag}")
```

3.  **SoM 标注模块**

```
import asyncio
import base64
import io
import json
from typing import Any, Dict, List
from PIL import Image, ImageDraw, ImageFont
import random

# 一些结构性/装饰性标签，通常没有直接交互
STRUCTURAL_TAGS = {
    "html", "head", "meta", "link", "style", "script", "base",
    "title", "body",
    "header", "footer", "main", "nav", "section", "article",
    "aside", "summary", "details",
}

# 明显非交互的 ARIA role
NON_INTERACTIVE_ROLES = {
    "presentation", "none",
    "img", "banner", "main", "contentinfo",
    "navigation", "region",
}

def looks_interactive(el: Dict[str, Any]) -> bool:
    tag = (el.get("tag") or "").lower()
    role = (el.get("role") or "").lower()
    typ = (el.get("type") or "").lower()
    text = (el.get("text") or "").strip()
    cls = (el.get("cls") or "").lower()
    id_ = (el.get("id") or "").lower()
    aria_label = (el.get("ariaLabel") or "").strip()

    # 原生可交互控件
    if tag in {"a", "button", "select", "textarea"}:
        return True
    if tag == "input" and typ not in {"hidden"}:
        return True

    # 有典型交互 role
    if role in {"button", "link", "tab", "menuitem", "option", "switch", "checkbox", "radio", "textbox"}:
        return True

    # 有常见事件或可获得焦点
    if any(x in el for x in ("onclick", "onmousedown", "onmouseup")):
        return True

    # class / id 里有明显交互关键词
    if any(k in cls or k in id_ for k in ("btn", "button", "link", "click", "nav", "tab", "menu")):
        return True

    # 有文本/aria-label 且是小块区域
    if (text or aria_label) and tag in {"div", "span", "li"}:
        return True

    return False

def is_obviously_non_interactive(el: Dict[str, Any]) -> bool:
    tag = (el.get("tag") or "").lower()
    role = (el.get("role") or "").lower()
    typ = (el.get("type") or "").lower()
    bbox = el.get("bbox") or {}
    w = bbox.get("width") or 0
    h = bbox.get("height") or 0

    if tag in STRUCTURAL_TAGS:
        if not (tag == "body" and (el.get("isContentEditable") or "ke-content" in (el.get("cls") or ""))):
            return True

    if w * h < 9:
        return True
    if tag in STRUCTURAL_TAGS or tag in {"video", "audio", "source"}:
        return True
    if tag == "input" and typ == "hidden":
        return True
    if role in NON_INTERACTIVE_ROLES:
        return True
    if not looks_interactive(el):
        return True

    return False

JS_COLLECT_ALL_RECURSIVE = r"""(args) => {
  const selector = args[0];
  const maxDepth = args[1];
  const maxPerDoc = args[2];
  const minArea = args[3];
  const includeIframes = args[4];

  function oneLine(s){ return String(s||"").replace(/\\s+/g," ").trim(); }

  function describe(el){
    const tagName = (el.tagName || "").toLowerCase();
    const hrefAttr = el.getAttribute("href") || "";
    const typeAttr = (el.getAttribute("type") || "").toLowerCase();
    const roleAttr = (el.getAttribute("role") || "").toLowerCase();
    const ariaAttr = el.getAttribute("aria-label") || "";

    let clickable = true;
    if (tagName == "div") clickable = false;

    if (tagName === "a" && hrefAttr) clickable = true;
    if (tagName === "button") clickable = true;
    if (tagName === "input" && typeAttr !== "hidden") clickable = true;

    if (["button","link","tab","menuitem","option","switch","checkbox","radio"].includes(roleAttr)) {
        clickable = true;
    }

    const isContentEditable = el.isContentEditable || el.getAttribute('contenteditable') === 'true';
    if (isContentEditable) clickable = true;

    if (el.onclick === "function") clickable = true;
    try {
        if (!clickable && typeof el.onclick === "function") {
            clickable = true;
        }
    } catch(e) {}

    const cls = (el.getAttribute("class") || "").toLowerCase();
    if (cls.includes("ke-content") || cls.includes("ke-edit-textarea")) {
        clickable = true;
    }

    return {
        tag: tagName,
        id: oneLine(el.getAttribute("id")),
        cls: oneLine(el.getAttribute("class")),
        role: roleAttr,
        name: oneLine(el.getAttribute("name")),
        type: typeAttr,
        href: oneLine(hrefAttr),
        src: oneLine(el.getAttribute("src")),
        ariaLabel: oneLine(ariaAttr),
        text: oneLine(el.textContent).slice(0, 40),
        clickable: clickable,
        isContentEditable: el.isContentEditable || el.getAttribute('contenteditable') === 'true',
    };
  }

  const out = [];
  let counter = 0;

  function walk(doc, depth, ox, oy, path){
    if (!doc || depth > maxDepth) return;
    const win = doc.defaultView;
    if (!win) return;

    const sx = 0;
    const sy = 0;
    const dpr = win.devicePixelRatio || 1;

    const nodes = Array.from(doc.querySelectorAll(selector)).slice(0, maxPerDoc);
    for (const el of nodes){
      try {
        const r = el.getBoundingClientRect();
        if (!r) continue;
        const area = r.width * r.height;
        if (area < minArea) continue;

        const vw = win.innerWidth || doc.documentElement.clientWidth || 0;
        const vh = win.innerHeight || doc.documentElement.clientHeight || 0;
        if (r.right <= 0 || r.bottom <= 0 || r.left >= vw || r.top >= vh) {
          continue;
        }

        const desc = describe(el);
        if (!desc.clickable) continue;

        if (!el.checkVisibility({ checkOpacity: true, checkVisibilityCSS: true })) continue;

        out.push({
          id: `e_${counter++}`,
          path,
          depth,
          dpr,
          ...describe(el),
          bbox: {
            x: (ox + r.x - sx) * dpr,
            y: (oy + r.y - sy) * dpr,
            width: r.width * dpr,
            height: r.height * dpr
          }
        });
      } catch(e) {}
    }

    if (!includeIframes) return;

    const iframes = Array.from(doc.querySelectorAll("iframe")).slice(0, maxPerDoc);
    for (let i = 0; i < iframes.length; i++){
      const fr = iframes[i];
      try {
        const rr = fr.getBoundingClientRect();
        const iframeOx = ox + rr.x - sx;
        const iframeOy = oy + rr.y - sy;
        const nextPath = path + `/iframe[${i}]`;

        try {
          const childDoc = fr.contentDocument;
          if (!childDoc) {
            out.push({
              id: `iframe_${counter++}`,
              path: nextPath,
              depth,
              dpr,
              tag: "iframe",
              src: oneLine(fr.getAttribute("src")),
              error: "iframe not ready (contentDocument is null)",
              bbox: {x: iframeOx * dpr, y: iframeOy * dpr, width: rr.width * dpr, height: rr.height * dpr},
            });
            continue;
          }
          walk(childDoc, depth + 1, iframeOx, iframeOy, nextPath);
        } catch(e) {
          out.push({
            id: `iframe_${counter++}`,
            path: nextPath,
            depth,
            dpr,
            tag: "iframe",
            src: oneLine(fr.getAttribute("src")),
            error: String(e),
            bbox: {x: iframeOx * dpr, y: iframeOy * dpr, width: rr.width * dpr, height: rr.height * dpr},
          });
        }
      } catch(e) {}
    }
  }

  walk(document, 0, 0, 0, "root");
  return JSON.stringify(out);
}"""

def mark_containing_items_for_removal(items):
    """标记需要移除的包含项"""
    def bbox_contains(a, b):
        ax1, ay1 = a["x"], a["y"]
        ax2, ay2 = ax1 + a["width"], ay1 + a["height"]
        bx1, by1 = b["x"], b["y"]
        bx2, by2 = bx1 + b["width"], by1 + b["height"]
        return (bx1 >= ax1 and by1 >= ay1 and bx2 <= ax2 and by2 <= ay2)

    for item in items:
        item["to_remove"] = False

    n = len(items)
    for i in range(n):
        a = items[i]
        for j in range(n):
            if i == j:
                continue
            b = items[j]
            if (a.get("text") or "").strip() == (b.get("text") or "").strip():
                if bbox_contains(a["bbox"], b["bbox"]):
                    a["to_remove"] = True
                    break

    return [item for item in items if not item["to_remove"]]

def draw_dashed_line(draw, xy, dash_len=6, gap_len=4, fill=(255, 0, 0, 200), width=2):
    """画虚线"""
    x1, y1, x2, y2 = xy
    if y1 == y2:  # 水平线
        total_len = abs(x2 - x1)
        step = dash_len + gap_len
        n = max(1, int(total_len // step) + 1)
        direction = 1 if x2 >= x1 else -1
        for i in range(n):
            start = x1 + direction * i * step
            end = start + direction * dash_len
            if direction == 1:
                if start > x2: break
                end = min(end, x2)
            else:
                if start < x2: break
                end = max(end, x2)
            draw.line((start, y1, end, y2), fill=fill, width=width)
    elif x1 == x2:  # 垂直线
        total_len = abs(y2 - y1)
        step = dash_len + gap_len
        n = max(1, int(total_len // step) + 1)
        direction = 1 if y2 >= y1 else -1
        for i in range(n):
            start = y1 + direction * i * step
            end = start + direction * dash_len
            if direction == 1:
                if start > y2: break
                end = min(end, y2)
            else:
                if start < y2: break
                end = max(end, y2)
            draw.line((x1, start, x2, end), fill=fill, width=width)
    else:
        draw.line((x1, y1, x2, y2), fill=fill, width=width)

def draw_dashed_rect(draw, x1, y1, x2, y2, dash_len=6, gap_len=4, fill=(255, 0, 0, 200), width=2):
    """画虚线矩形"""
    draw_dashed_line(draw, (x1, y1, x2, y1), dash_len, gap_len, fill, width)
    draw_dashed_line(draw, (x1, y2, x2, y2), dash_len, gap_len, fill, width)
    draw_dashed_line(draw, (x1, y1, x1, y2), dash_len, gap_len, fill, width)
    draw_dashed_line(draw, (x2, y1, x2, y2), dash_len, gap_len, fill, width)

def screenshot_to_png_bytes(s: Any) -> bytes:
    if isinstance(s, (bytes, bytearray)):
        return bytes(s)
    if isinstance(s, str):
        ss = s.strip()
        if ss.startswith("data:image"):
            ss = ss.split(",", 1)[-1].strip()
        try:
            return base64.b64decode(ss, validate=True)
        except Exception:
            with open(s, "rb") as f:
                return f.read()
    raise TypeError(f"Unsupported screenshot type: {type(s)}")

def items_to_text(items_raw):
    format_ele_text = []
    for web_ele_id in range(len(items_raw)):
        item = items_raw[web_ele_id]
        is_menu = item.get('isMenu', False)
        menu_options = item.get('menuOptions', [])
        label_text = item.get('text', "")
        ele_tag_name = item.get("tag", "button")
        ele_type = item.get("type", "")
        ele_aria_label = item.get("ariaLabel", "")
        input_attr_types = ['text', 'search', 'password', 'email', 'tel']

        if is_menu and menu_options:
            trigger_text = label_text.split('\\n')[0].strip()
            options_str = ', '.join([f'"{opt}"' for opt in menu_options])
            base_text = f"[{web_ele_id}]: <{ele_tag_name}>"
            if trigger_text:
                base_text += f' "{trigger_text}"'
            elif ele_aria_label:
                base_text += f' "{ele_aria_label}"'
            format_ele_text.append(f"{base_text} is a menu with options: [{options_str}];")
            continue

        if not label_text:
            if (ele_tag_name.lower() == 'input' and ele_type in input_attr_types) or \\
               ele_tag_name.lower() == 'textarea' or \\
               (ele_tag_name.lower() == 'button' and ele_type in ['submit', 'button']):
                if ele_aria_label:
                    format_ele_text.append(f'[{web_ele_id}]: <{ele_tag_name}> "{ele_aria_label}";')
                else:
                    format_ele_text.append(f'[{web_ele_id}]: <{ele_tag_name}> "{label_text}";')
        elif label_text and len(label_text) < 200:
            if not ("<img" in label_text and "src=" in label_text):
                if ele_tag_name in ["button", "input", "textarea"]:
                    if ele_aria_label and (ele_aria_label != label_text):
                        format_ele_text.append(f'[{web_ele_id}]: <{ele_tag_name}> "{label_text}", "{ele_aria_label}";')
                    else:
                        format_ele_text.append(f'[{web_ele_id}]: <{ele_tag_name}> "{label_text}";')
                else:
                    if ele_aria_label and (ele_aria_label != label_text):
                        format_ele_text.append(f'[{web_ele_id}]: "{label_text}", "{ele_aria_label}";')
                    else:
                        format_ele_text.append(f'[{web_ele_id}]: "{label_text}";')

    return '\\t'.join(format_ele_text)

def draw_som(items, overlay, max_draw):
    try:
        font = ImageFont.truetype(ImageFont.load_default().path, size=20)
    except Exception:
        font = ImageFont.load_default()

    placed_label_boxes = []
    draw = ImageDraw.Draw(overlay)
    for idx, it in enumerate(items[:max_draw]):
        b = it.get("bbox") or {}
        x, y, w, h = b.get("x"), b.get("y"), b.get("width"), b.get("height")
        if None in (x, y, w, h) or w <= 0 or h <= 0:
            continue

        r, g, b_color = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        color = (r, g, b_color, 255)

        x1, y1, x2, y2 = x, y, x + w, y + h
        draw_dashed_rect(draw, x1, y1, x2, y2, dash_len=6, gap_len=4, fill=color, width=2)

        if idx < max_draw:
            label = f'{idx}'
            try:
                tb = draw.textbbox((0, 0), label, font=font)
                tw, th = tb[2] - tb[0], tb[3] - tb[1]
            except Exception:
                tw, th = len(label) * 6, 12

            padding_x, padding_y = 6, 4
            label_w, label_h = tw + padding_x * 2, th + padding_y * 2

            candidates = [
                ("top_left", x1, y1 - label_h - 2),
                ("top_right", x2 - label_w, y1 - label_h - 2),
                ("bottom_left", x1, y2 + 2),
                ("bottom_right", x2 - label_w, y2 + 2),
            ]

            img_w, img_h = overlay.size
            normalized_candidates = [
                (name, max(0, min(lx, img_w - label_w)), max(0, min(ly, img_h - label_h)))
                for name, lx, ly in candidates
            ]

            best_pos = None
            best_overlap = None
            for name, lx_c, ly_c in normalized_candidates:
                candidate_rect = (lx_c, ly_c, lx_c + label_w, ly_c + label_h)
                total_overlap = sum(
                    rect_intersection_area(candidate_rect, placed)
                    for placed in placed_label_boxes
                )
                if total_overlap == 0:
                    best_pos = (lx_c, ly_c)
                    best_overlap = 0
                    break
                if best_overlap is None or total_overlap < best_overlap:
                    best_overlap = total_overlap
                    best_pos = (lx_c, ly_c)

            lx, ly = best_pos
            label_box = (lx, ly, lx + label_w, ly + label_h)
            placed_label_boxes.append(label_box)

            color = list(color)
            color[-1] = 150
            draw.rectangle([lx, ly, lx + label_w, ly + label_h], fill=tuple(color))
            draw.text((lx + padding_x, ly + padding_y), label, fill=(255, 255, 255, 255), font=font)

def rect_intersection_area(a, b):
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    ix1, iy1 = max(ax1, bx1), max(ay1, by1)
    ix2, iy2 = min(ax2, bx2), min(ay2, by2)
    if ix2 <= ix1 or iy2 <= iy1:
        return 0
    return (ix2 - ix1) * (iy2 - iy1)

def is_inside_strict(box_inner: dict, box_outer: dict) -> bool:
    x1, y1, w1, h1 = box_inner.get("x"), box_inner.get("y"), box_inner.get("width"), box_inner.get("height")
    x2, y2, w2, h2 = box_outer.get("x"), box_outer.get("y"), box_outer.get("width"), box_outer.get("height")
    i_left, i_top = x1, y1
    i_right, i_bottom = x1 + w1, y1 + h1
    o_left, o_top = x2, y2
    o_right, o_bottom = x2 + w2, y2 + h2
    return (i_left > o_left and i_top > o_top and i_right < o_right and i_bottom < o_bottom)

def remove_outer_boxes(A: list) -> list:
    n = len(A)
    remove_flags = [False] * n
    for i in range(n):
        if remove_flags[i]:
            continue
        box_i = A[i]["bbox"]
        for j in range(n):
            if i == j:
                continue
            box_j = A[j]["bbox"]
            if is_inside_strict(box_j, box_i):
                remove_flags[i] = True
                break
    return [box for k, box in enumerate(A) if not remove_flags[k]]

async def get_css_som(page, selector="*", max_depth=16, max_per_doc=3000, min_area=-1.0, max_retry=3):
    items = []
    for _ in range(max_retry):
        try:
            items_json = await page.evaluate(
                JS_COLLECT_ALL_RECURSIVE,
                [selector, max_depth, max_per_doc, float(min_area), True],
            )
            items = json.loads(items_json)
            break
        except Exception:
            try:
                await page.wait_for_load_state()
            except Exception:
                pass
            await asyncio.sleep(1)
            continue

    if items:
        items = mark_containing_items_for_removal(items)
    return items

def remove_neg_boxes(A: list) -> list:
    n = len(A)
    remove_flags = [False] * n
    for i in range(n):
        box_i = A[i]["bbox"]
        x, y, w, h = box_i.get("x"), box_i.get("y"), box_i.get("width"), box_i.get("height")
        if None in (x, y, w, h) or w <= 0 or h <= 0:
            remove_flags[i] = True
        if box_i.get("x", 0) < 0 or box_i.get("y", 0) < 0:
            remove_flags[i] = True
    return [box for k, box in enumerate(A) if not remove_flags[k]]

async def get_som(page, img_path, img_path_no_box, selector="*", max_depth=16,
                  max_per_doc=3000, min_area=-1.0, max_draw=2000, max_retry=3):
    """获取页面 SoM 标注"""
    items = await get_css_som(page, selector=selector, max_depth=max_depth,
                               max_per_doc=max_per_doc, min_area=min_area, max_retry=max_retry)

    shot = await page.screenshot()
    with open(img_path_no_box, "wb") as f:
        f.write(shot)

    items = remove_neg_boxes(items)

    png_bytes = screenshot_to_png_bytes(shot)
    img = Image.open(io.BytesIO(png_bytes)).convert("RGBA")
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw_som(items, overlay, max_draw)
    img = Image.alpha_composite(img, overlay)
    img.save(img_path)

    return items, items_to_text(items)
```

4.  **主链路运行**

```
async def main():
    instruction = '搜一下今天NBA火箭队比赛结果'
    history = []
    max_step = 30
    model_name = 'gui-plus-2026-02-26'
    task_dir = f'data_{time.strftime("%Y%m%d_%H%M%S")}'
    web_tools = PlaywrightComputer(initial_url='https://www.baidu.com/', task_dir=task_dir)

    await web_tools.reset()
    stop_flag = False
    dashscope.api_key = os.getenv("DASHSCOPE_API_KEY", None)
    # 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID
    dashscope.base_http_api_url = 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1'
    session_id = str(uuid.uuid4())
    print('session_id ', session_id)

    for step_id in range(max_step):
        if stop_flag:
            break
        safe_instruction = "".join(c if c.isalnum() or c in (" ", "_", "-") else "_" for c in instruction).strip()
        env_state = await web_tools.current_state(it=step_id)
        screen_shot = env_state['img_path']
        messages = get_messages(screen_shot, env_state, instruction, history)

        retry_time = 3
        for _ in range(retry_time):
            response = dashscope.MultiModalConversation.call(
                model=model_name,
                messages=messages,
                vl_high_resolution_images=True,
                headers={"x-dashscope-gui-session-id": session_id},
                stream=False
            )
            print(response['request_id'])
            try:
                output_text = response.output.choices[0].message.content[0]['text']
                break
            except Exception as e:
                print(response)
                print(e)
        else:
            raise Exception('retry_time out')
        print(output_text)

        thought = response.output.choices[0].message.reasoning_content
        if thought != '':
            output_text = f"<think>\\n{thought}\\n</think>{output_text}"

        action_list = extract_tool_calls(output_text)
        conclusion = output_text.split('<tool_call>')[0].strip()

        for action_id, action in enumerate(action_list):
            action_parameter = action['arguments']
            action_type = action_parameter['action']
            label = action_parameter.get('label', None)
            weki_url = "https://baike.baidu.com/"
            coordicate = []

            if label is not None:
                if label == "WINDOW":
                    coordicate = [500, 500]
                else:
                    ele = env_state["SoM"]["SoM_list"][label]
                    box = ele["bbox"]
                    x, y, w, h = box.get("x"), box.get("y"), box.get("width"), box.get("height")
                    nx = x + w / 2
                    ny = y + h / 2
                    coordicate = [nx, ny]
                    action_parameter['coordinate'] = coordicate

            if action_type == 'wait':
                await asyncio.sleep(action_parameter.get('time', 2))
            elif action_type == 'scroll':
                direction = action_parameter['direction']
                await web_tools.scroll_at(coordicate[0], coordicate[1], direction=direction, magnitude=300)
            elif action_type == 'select':
                text = action_parameter['option']
                await web_tools._select(coordicate[0], coordicate[1], text=text)
            elif action_type == 'goback':
                await web_tools.go_back()
            elif action_type == 'goto':
                url = action_parameter.get('url', '')
                await web_tools.navigate(url, normalize=True)
            elif action_type == 'click':
                await web_tools.click_at(coordicate[0], coordicate[1])
            elif action_type == 'type':
                text = action_parameter['text']
                await web_tools.type_text_at(coordicate[0], coordicate[1], text)
            elif action_type == 'wikipedia':
                await web_tools.navigate(weki_url, normalize=True)
            elif action_type == 'answer':
                text = action_parameter['text']
                print(f'Answer: {text}\\n动作已完成')
                stop_flag = True
                break

            anno_dir = os.path.join(task_dir, 'anno')
            if not os.path.exists(anno_dir):
                os.makedirs(anno_dir)
            anno_path = show_screenshot(
                env_state['img_path_no_box'],
                action_parameter,
                f'{anno_dir}/anno_{step_id}_{action_id}.png'
            )

        history.append({'output': output_text, 'image': screen_shot})
        await asyncio.sleep(2)

if __name__ == '__main__':
    asyncio.run(main())
```

浏览器完整示例代码

```
"""
浏览器 GUI 自动化完整示例代码
将 browser_local.py 和 som.py 合并为单文件，可直接运行

依赖安装：
pip install playwright dashscope pillow termcolor playwright-stealth
playwright install chromium

运行前设置环境变量：
export DASHSCOPE_API_KEY=your_api_key
"""

import json, os, sys, base64
import dashscope, time, math
import uuid
from PIL import Image, ImageDraw
import asyncio
from playwright.async_api import async_playwright, Page, Browser, BrowserContext
from typing import Literal, Any, List, Dict
import random
from datetime import datetime
import io
import re

# ===================== SoM 标注模块 =====================

# 结构性/装饰性标签，通常没有直接交互
STRUCTURAL_TAGS = {
    "html", "head", "meta", "link", "style", "script", "base",
    "title", "body", "header", "footer", "main", "nav", "section", "article",
    "aside", "summary", "details",
}

# 明显非交互的 ARIA role
NON_INTERACTIVE_ROLES = {
    "presentation", "none", "img", "banner", "main", "contentinfo", "navigation", "region",
}

def looks_interactive(el: Dict[str, Any]) -> bool:
    """判断元素是否看起来可交互"""
    tag = (el.get("tag") or "").lower()
    role = (el.get("role") or "").lower()
    typ = (el.get("type") or "").lower()
    text = (el.get("text") or "").strip()
    cls = (el.get("cls") or "").lower()
    id_ = (el.get("id") or "").lower()
    aria_label = (el.get("ariaLabel") or "").strip()

    if tag in {"a", "button", "select", "textarea"}:
        return True
    if tag == "input" and typ not in {"hidden"}:
        return True
    if role in {"button", "link", "tab", "menuitem", "option", "switch", "checkbox", "radio", "textbox"}:
        return True
    if any(x in el for x in ("onclick", "onmousedown", "onmouseup")):
        return True
    if any(k in cls or k in id_ for k in ("btn", "button", "link", "click", "nav", "tab", "menu")):
        return True
    if (text or aria_label) and tag in {"div", "span", "li"}:
        return True
    return False

def is_obviously_non_interactive(el: Dict[str, Any]) -> bool:
    """判断元素是否明显非交互"""
    tag = (el.get("tag") or "").lower()
    role = (el.get("role") or "").lower()
    typ = (el.get("type") or "").lower()
    bbox = el.get("bbox") or {}
    w = bbox.get("width") or 0
    h = bbox.get("height") or 0

    if tag in STRUCTURAL_TAGS:
        if not (tag == "body" and (el.get("isContentEditable") or "ke-content" in (el.get("cls") or ""))):
            return True
    if w * h < 9:
        return True
    if tag in STRUCTURAL_TAGS or tag in {"video", "audio", "source"}:
        return True
    if tag == "input" and typ == "hidden":
        return True
    if role in NON_INTERACTIVE_ROLES:
        return True
    if not looks_interactive(el):
        return True
    return False

JS_COLLECT_ALL_RECURSIVE = r"""(args) => {
  const selector = args[0];
  const maxDepth = args[1];
  const maxPerDoc = args[2];
  const minArea = args[3];
  const includeIframes = args[4];

  function oneLine(s){ return String(s||"").replace(/\s+/g," ").trim(); }

  function describe(el){
    const tagName = (el.tagName || "").toLowerCase();
    const hrefAttr = el.getAttribute("href") || "";
    const typeAttr = (el.getAttribute("type") || "").toLowerCase();
    const roleAttr = (el.getAttribute("role") || "").toLowerCase();
    const ariaAttr = el.getAttribute("aria-label") || "";

    let clickable = true;
    if (tagName == "div") clickable = false;
    if (tagName === "a" && hrefAttr) clickable = true;
    if (tagName === "button") clickable = true;
    if (tagName === "input" && typeAttr !== "hidden") clickable = true;
    if (["button","link","tab","menuitem","option","switch","checkbox","radio"].includes(roleAttr)) {
        clickable = true;
    }
    const isContentEditable = el.isContentEditable || el.getAttribute('contenteditable') === 'true';
    if (isContentEditable) clickable = true;
    if (el.onclick === "function") clickable = true;
    try {
        if (!clickable && typeof el.onclick === "function") clickable = true;
    } catch(e) {}
    const cls = (el.getAttribute("class") || "").toLowerCase();
    if (cls.includes("ke-content") || cls.includes("ke-edit-textarea")) clickable = true;

    return {
        tag: tagName, id: oneLine(el.getAttribute("id")), cls: oneLine(el.getAttribute("class")),
        role: roleAttr, name: oneLine(el.getAttribute("name")), type: typeAttr,
        href: oneLine(hrefAttr), src: oneLine(el.getAttribute("src")), ariaLabel: oneLine(ariaAttr),
        text: oneLine(el.textContent).slice(0, 40), clickable: clickable,
        isContentEditable: el.isContentEditable || el.getAttribute('contenteditable') === 'true',
    };
  }

  const out = [];
  let counter = 0;

  function walk(doc, depth, ox, oy, path){
    if (!doc || depth > maxDepth) return;
    const win = doc.defaultView;
    if (!win) return;
    const sx = 0, sy = 0;
    const dpr = win.devicePixelRatio || 1;

    const nodes = Array.from(doc.querySelectorAll(selector)).slice(0, maxPerDoc);
    for (const el of nodes){
      try {
        const r = el.getBoundingClientRect();
        if (!r) continue;
        const area = r.width * r.height;
        if (area < minArea) continue;
        const vw = win.innerWidth || doc.documentElement.clientWidth || 0;
        const vh = win.innerHeight || doc.documentElement.clientHeight || 0;
        if (r.right <= 0 || r.bottom <= 0 || r.left >= vw || r.top >= vh) continue;
        const desc = describe(el);
        if (!desc.clickable) continue;
        if (!el.checkVisibility({ checkOpacity: true, checkVisibilityCSS: true })) continue;

        out.push({
          id: `e_${counter++}`, path, depth, dpr, ...describe(el),
          bbox: { x: (ox + r.x - sx) * dpr, y: (oy + r.y - sy) * dpr, width: r.width * dpr, height: r.height * dpr }
        });
      } catch(e) {}
    }
    if (!includeIframes) return;
    const iframes = Array.from(doc.querySelectorAll("iframe")).slice(0, maxPerDoc);
    for (let i = 0; i < iframes.length; i++){
      const fr = iframes[i];
      try {
        const rr = fr.getBoundingClientRect();
        const iframeOx = ox + rr.x - sx;
        const iframeOy = oy + rr.y - sy;
        const nextPath = path + `/iframe[${i}]`;
        try {
          const childDoc = fr.contentDocument;
          if (!childDoc) {
            out.push({ id: `iframe_${counter++}`, path: nextPath, depth, dpr, tag: "iframe",
              src: oneLine(fr.getAttribute("src")), error: "iframe not ready",
              bbox: {x: iframeOx * dpr, y: iframeOy * dpr, width: rr.width * dpr, height: rr.height * dpr} });
            continue;
          }
          walk(childDoc, depth + 1, iframeOx, iframeOy, nextPath);
        } catch(e) {
          out.push({ id: `iframe_${counter++}`, path: nextPath, depth, dpr, tag: "iframe",
            src: oneLine(fr.getAttribute("src")), error: String(e),
            bbox: {x: iframeOx * dpr, y: iframeOy * dpr, width: rr.width * dpr, height: rr.height * dpr} });
        }
      } catch(e) {}
    }
  }
  walk(document, 0, 0, 0, "root");
  return JSON.stringify(out);
}"""

def mark_containing_items_for_removal(items):
    """移除被包含的重复元素"""
    def bbox_contains(a, b):
        ax1, ay1, ax2, ay2 = a["x"], a["y"], a["x"] + a["width"], a["y"] + a["height"]
        bx1, by1, bx2, by2 = b["x"], b["y"], b["x"] + b["width"], b["y"] + b["height"]
        return (bx1 >= ax1 and by1 >= ay1 and bx2 <= ax2 and by2 <= ay2)

    for item in items:
        item["to_remove"] = False
    n = len(items)
    for i in range(n):
        a = items[i]
        for j in range(n):
            if i == j: continue
            b = items[j]
            if (a.get("text") or "").strip() == (b.get("text") or "").strip():
                if bbox_contains(a["bbox"], b["bbox"]):
                    a["to_remove"] = True
                    break
    return [item for item in items if not item["to_remove"]]

def screenshot_to_png_bytes(s: Any) -> bytes:
    if isinstance(s, (bytes, bytearray)):
        return bytes(s)
    if isinstance(s, str):
        ss = s.strip()
        if ss.startswith("data:image"):
            ss = ss.split(",", 1)[-1].strip()
        try:
            return base64.b64decode(ss, validate=True)
        except Exception:
            with open(s, "rb") as f:
                return f.read()
    raise TypeError(f"Unsupported screenshot type: {type(s)}")

def items_to_text(items_raw):
    """将元素列表转换为文本描述"""
    format_ele_text = []
    for web_ele_id in range(len(items_raw)):
        item = items_raw[web_ele_id]
        label_text = item.get('text', "")
        ele_tag_name = item.get("tag", "button")
        ele_type = item.get("type", "")
        ele_aria_label = item.get("ariaLabel", "")
        input_attr_types = ['text', 'search', 'password', 'email', 'tel']

        if not label_text:
            if (ele_tag_name.lower() == 'input' and ele_type in input_attr_types) or \
               ele_tag_name.lower() == 'textarea' or \
               (ele_tag_name.lower() == 'button' and ele_type in ['submit', 'button']):
                format_ele_text.append(f"[{web_ele_id}]: <{ele_tag_name}> \"{ele_aria_label or label_text}\";")
        elif label_text and len(label_text) < 200:
            if not ("<img" in label_text and "src=" in label_text):
                if ele_tag_name in ["button", "input", "textarea"]:
                    format_ele_text.append(f"[{web_ele_id}]: <{ele_tag_name}> \"{label_text}\";")
                else:
                    format_ele_text.append(f"[{web_ele_id}]: \"{label_text}\";")
    return '\t'.join(format_ele_text)

def draw_dashed_rect(draw, x1, y1, x2, y2, dash_len=6, gap_len=4, fill=(255, 0, 0, 200), width=2):
    """画虚线矩形"""
    def draw_dashed_line(xy):
        px1, py1, px2, py2 = xy
        if py1 == py2:  # 水平线
            total_len = abs(px2 - px1)
            step = dash_len + gap_len
            direction = 1 if px2 >= px1 else -1
            for i in range(max(1, int(total_len // step) + 1)):
                start = px1 + direction * i * step
                end = start + direction * dash_len
                if direction == 1:
                    if start > px2: break
                    end = min(end, px2)
                else:
                    if start < px2: break
                    end = max(end, px2)
                draw.line((start, py1, end, py2), fill=fill, width=width)
        elif px1 == px2:  # 垂直线
            total_len = abs(py2 - py1)
            step = dash_len + gap_len
            direction = 1 if py2 >= py1 else -1
            for i in range(max(1, int(total_len // step) + 1)):
                start = py1 + direction * i * step
                end = start + direction * dash_len
                if direction == 1:
                    if start > py2: break
                    end = min(end, py2)
                else:
                    if start < py2: break
                    end = max(end, py2)
                draw.line((px1, start, px2, end), fill=fill, width=width)
    draw_dashed_line((x1, y1, x2, y1))
    draw_dashed_line((x1, y2, x2, y2))
    draw_dashed_line((x1, y1, x1, y2))
    draw_dashed_line((x2, y1, x2, y2))

def draw_som(items, overlay, max_draw):
    """在截图上绘制 SoM 标注"""
    try:
        font = Image.ImageFont.load_default()
    except Exception:
        font = None
    draw = ImageDraw.Draw(overlay)
    placed_label_boxes = []

    for idx, it in enumerate(items[:max_draw]):
        b = it.get("bbox") or {}
        x, y, w, h = b.get("x"), b.get("y"), b.get("width"), b.get("height")
        if None in (x, y, w, h) or w <= 0 or h <= 0:
            continue

        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 255)
        x1, y1, x2, y2 = x, y, x + w, y + h
        draw_dashed_rect(draw, x1, y1, x2, y2, fill=color, width=2)

        if idx < max_draw:
            label = f'{idx}'
            try:
                tb = draw.textbbox((0, 0), label, font=font) if font else (0, 0, len(label) * 6, 12)
                tw, th = tb[2] - tb[0], tb[3] - tb[1]
            except Exception:
                tw, th = len(label) * 6, 12

            padding_x, padding_y = 6, 4
            label_w, label_h = tw + padding_x * 2, th + padding_y * 2

            # 优先左上角
            lx = max(0, min(x1, overlay.size[0] - label_w))
            ly = max(0, y1 - label_h - 2)

            color_list = list(color)
            color_list[-1] = 150
            draw.rectangle([lx, ly, lx + label_w, ly + label_h], fill=tuple(color_list))
            draw.text((lx + padding_x, ly + padding_y), label, fill=(255, 255, 255, 255), font=font)

def remove_neg_boxes(A: list) -> list:
    """移除负坐标的框"""
    return [box for box in A if not (box["bbox"].get("x", 0) < 0 or box["bbox"].get("y", 0) < 0)]

async def get_css_som(page, selector="*", max_depth=16, max_per_doc=3000, min_area=-1.0, max_retry=3):
    """获取页面 CSS 元素"""
    items = []
    for _ in range(max_retry):
        try:
            items_json = await page.evaluate(JS_COLLECT_ALL_RECURSIVE, [selector, max_depth, max_per_doc, float(min_area), True])
            items = json.loads(items_json)
            break
        except Exception:
            try:
                await page.wait_for_load_state()
            except Exception:
                pass
            await asyncio.sleep(1)
    if items:
        items = mark_containing_items_for_removal(items)
    return items

async def get_som(page, img_path, img_path_no_box, selector="*", max_depth=16, max_per_doc=3000, min_area=-1.0, max_draw=2000, max_retry=3):
    """获取页面 SoM 标注"""
    items = await get_css_som(page, selector=selector, max_depth=max_depth, max_per_doc=max_per_doc, min_area=min_area, max_retry=max_retry)
    shot = await page.screenshot()
    with open(img_path_no_box, "wb") as f:
        f.write(shot)
    items = remove_neg_boxes(items)
    png_bytes = screenshot_to_png_bytes(shot)
    img = Image.open(io.BytesIO(png_bytes)).convert("RGBA")
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw_som(items, overlay, max_draw)
    img = Image.alpha_composite(img, overlay)
    img.save(img_path)
    return items, items_to_text(items)

# ===================== PlaywrightComputer 类 =====================

PLAYWRIGHT_KEY_MAP = {
    "backspace": "Backspace", "tab": "Tab", "return": "Enter", "enter": "Enter",
    "shift": "Shift", "control": "ControlOrMeta", "alt": "Alt", "escape": "Escape",
    "space": "Space", "pageup": "PageUp", "pagedown": "PageDown", "end": "End", "home": "Home",
    "left": "ArrowLeft", "up": "ArrowUp", "right": "ArrowRight", "down": "ArrowDown",
    "insert": "Insert", "delete": "Delete", "f1": "F1", "f2": "F2", "f3": "F3", "f4": "F4",
    "f5": "F5", "f6": "F6", "f7": "F7", "f8": "F8", "f9": "F9", "f10": "F10", "f11": "F11", "f12": "F12",
    "command": "Meta",
}

class PlaywrightComputer:
    """Playwright 浏览器自动化封装"""

    def __init__(self, initial_url="https://www.baidu.com/", task_dir='data', highlight_mouse: bool = False):
        self._initial_url = initial_url
        self.task_dir = task_dir
        self._highlight_mouse = highlight_mouse
        self._playwright = None
        self._browser: Browser | None = None
        self._context: BrowserContext | None = None
        self._page: Page | None = None

    async def reset(self):
        """初始化浏览器"""
        self._playwright = await async_playwright().start()
        self._browser = await self._playwright.chromium.launch(
            args=["--start-maximized", "--disable-blink-features=AutomationControlled"],
            headless=False,
        )
        user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
        self._context = await self._browser.new_context(no_viewport=True, user_agent=user_agent, locale="en-US")
        self._page = await self._context.new_page()
        await self._page.goto(self._initial_url, timeout=60000, wait_until="domcontentloaded")
        print("浏览器启动成功")

    async def close(self):
        """关闭浏览器"""
        if self._context:
            await self._context.close()
        if self._browser:
            await self._browser.close()
        if self._playwright:
            await self._playwright.stop()

    async def click_at(self, x: int, y: int):
        await self._page.mouse.click(x, y)
        await self._page.wait_for_load_state()

    async def type_text_at(self, x: int, y: int, text: str, press_enter: bool = True, clear_before_typing: bool = True):
        await self._page.mouse.click(x, y)
        await asyncio.sleep(0.1)
        if clear_before_typing:
            await self.key_combination(["Control", "A"])
            await asyncio.sleep(0.1)
            await self.key_combination(["Delete"])
        await self._page.keyboard.type(text)
        if press_enter:
            await self.key_combination(["Enter"])
        await self._page.wait_for_load_state()

    async def scroll_at(self, x: int, y: int, direction: Literal["up", "down"], magnitude: int = 400):
        await self._page.mouse.move(x, y)
        await asyncio.sleep(0.1)
        dy = -magnitude if direction == "up" else magnitude
        await self._page.mouse.wheel(0, dy)
        await self._page.wait_for_load_state()

    async def go_back(self):
        await self._page.go_back()
        await self._page.wait_for_load_state()

    async def navigate(self, url: str, normalize=True):
        if normalize and not url.startswith(("http://", "https://")):
            url = "https://" + url
        await self._page.goto(url)
        await self._page.wait_for_load_state()

    async def key_combination(self, keys: list[str]):
        keys = [PLAYWRIGHT_KEY_MAP.get(k.lower(), k) for k in keys]
        for key in keys[:-1]:
            await self._page.keyboard.down(key)
        await self._page.keyboard.press(keys[-1])
        for key in reversed(keys[:-1]):
            await self._page.keyboard.up(key)

    async def current_state(self, it):
        """获取当前页面状态和 SoM 标注"""
        try:
            await self._page.wait_for_load_state("networkidle", timeout=10000)
        except Exception:
            pass
        await asyncio.sleep(1)

        os.makedirs(os.path.join(self.task_dir, "trajectory_som"), exist_ok=True)
        os.makedirs(os.path.join(self.task_dir, "trajectory"), exist_ok=True)
        img_path = os.path.join(self.task_dir, f"trajectory_som/screenshot{it}.png")
        img_path_no_box = os.path.join(self.task_dir, f"trajectory/{it}_full_screenshot.png")

        SoM_list, format_ele_text = await get_som(self._page, img_path, img_path_no_box)
        width, height = Image.open(img_path).size
        return {
            "img_path": img_path, "img_path_no_box": img_path_no_box,
            "SoM": {"SoM_list": SoM_list, "format_ele_text": format_ele_text},
            "current_url": self._page.url, "width": width, "height": height
        }

    async def _select(self, x, y, text):
        await self._page.mouse.click(x, y)
        handle = await self._page.evaluate_handle("([x,y]) => document.elementFromPoint(x,y)", [x, y])
        tag = await handle.evaluate("el => el && el.tagName")
        if tag == "SELECT":
            await handle.evaluate("""(sel, label) => {
                const opt = [...sel.options].find(o => o.label.trim() === label.trim());
                if (!opt) throw new Error("找不到选项: " + label);
                sel.value = opt.value;
                sel.dispatchEvent(new Event('input', {bubbles:true}));
                sel.dispatchEvent(new Event('change', {bubbles:true}));
            }""", text)
        else:
            raise RuntimeError(f"坐标处元素不是 SELECT，而是 {tag}")

# ===================== Prompt 构造 =====================

def get_messages(image, env_state, instruction, history_output):
    """构造多轮对话消息"""
    history_n = 1
    current_step = len(history_output)
    history_start_idx = max(0, current_step - history_n)
    SoM_format_ele_text = env_state["SoM"]["format_ele_text"]

    system_prompt = '''# Tools

You may call one or more functions to assist with the user query.

You are provided with function signatures within <tools></tools> XML tags:
<tools>
{"type": "function", "function": {"name_for_human": "browser_use", "name": "browser_use", "description": "Use a browser to interact with web pages and take labeled screenshots.\\n* This is an interface to a web browser. You can click elements, type into inputs, scroll, wait for loading, go back, etc.\\n* Each Observation screenshot contains Numerical Labels placed at the TOP LEFT of each Web Element. Use these labels to target elements.\\n* Some pages may take time to load; you may need to wait and take successive screenshots.\\n* Avoid clicking near element edges; target the center of the element.\\n* Execute exactly ONE interaction action per step; do not chain multiple interactions in one call.", "parameters": {"properties": {"action": {"description": "The action to perform. The available actions are:\\n* `click`: Click a web element by numerical label.\\n* `type`: Clear existing content in a textbox/input and type content. The system will automatically press ENTER after typing.\\n* `scroll`: Scroll within WINDOW or within a specific scrollable element/area (by label).\\n* `select`: Selects a specific option from a menu or dropdown. Use the option text provided in the textual information.\\n* `wait`: Wait for page processes to finish (default 5 seconds unless specified).\\n* `go_back`: Go back to the previous page.\\n* `wikipedia`: Directly jump to the Wikipedia homepage to search for information.\\n* `answer`: Terminate the current task and output the final answer.", "enum": ["click", "type", "scroll", "select", "wait", "go_back", "wikipedia", "answer"], "type": "string"}, "label": {"description": "Numerical label of the target web element. Required only by `action=click`, `action=type`, `action=scroll`, and `action=select` when scrolling within a specific area. Use string value `WINDOW` to scroll the whole page.", "type": ["integer", "string"]}, "direction": {"description": "Scroll direction. Required only by `action=scroll`.", "enum": ["up", "down"], "type": "string"}, "text": {"description": "Required only by `action=type` and `action=answer`.", "type": "string"}, "option": {"description": "The option to select. Required only by `action=select`", "type": "string"}, "time": {"description": "The seconds to wait. Required only by `action=wait` when overriding the default.", "type": "integer"}}, "required": ["action"], "type": "object"}, "args_format": "Format the arguments as a JSON object."}}
</tools>

For each function call, return a json object with function name and arguments within <tool_call></tool_call> XML tags:
<tool_call>
{"name": <function-name>, "arguments": <args-json-object>}
</tool_call>

# Response format

Response format for every step:
1) Action: a short imperative describing what to do in the UI.
2) A single <tool_call>...</tool_call> block containing only the JSON: {"name": <function-name>, "arguments": <args-json-object>}.

Rules:
- Output exactly in the order: Action, <tool_call>.
- Be brief: one line for Action.
- Do not output anything else outside those two parts.
- Execute ONLY ONE interaction per iteration (one tool call).
- If finishing, use action=answer in the tool call.'''

    today = datetime.today()
    weekday_names = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    weekday = weekday_names[today.weekday()]
    formatted_date = today.strftime("%Y年%m月%d日") + " " + weekday
    day_info = f'''今天的日期是:{formatted_date}。'''

    previous_actions = []
    for i in range(history_start_idx):
        if i < len(history_output):
            history_output_str = history_output[i]['output']
            if 'Action:' in history_output_str and '<tool_call>':
                history_output_str = history_output_str.split('Action:')[1].split('<tool_call>')[0].strip()
            previous_actions.append(f"Step {i + 1}: {history_output_str}")
    previous_actions_str = "\n".join(previous_actions) if previous_actions else "None"

    instruction_prompt = f'''\nPlease generate the next move according to the UI screenshot, instruction and previous actions.

Instruction: {day_info}{instruction}

Previous actions:
{previous_actions_str}'''

    messages = [{"role": "system", "content": [{"text": system_prompt}]}]
    history_len = min(history_n, len(history_output))

    if history_len > 0:
        for history_id, history_item in enumerate(history_output[-history_n:], 0):
            if history_id == 0:
                messages.append({"role": "user", "content": [
                    {"text": instruction_prompt}, {"text": "Current screenshot:"},
                    {"image": "file://" + history_item['image']}
                ]})
            else:
                messages.append({"role": "user", "content": [
                    {"text": "Current screenshot:"}, {"image": "file://" + history_item['image']}
                ]})
            messages.append({"role": "assistant", "content": [{"text": history_item['output']}]})
        messages.append({"role": "user", "content": [
            {"image": "file://" + image}, {"text": SoM_format_ele_text}
        ]})
    else:
        messages.append({"role": "user", "content": [
            {"text": instruction_prompt}, {"image": "file://" + image}, {"text": SoM_format_ele_text}
        ]})
    return messages

def extract_tool_calls(text: str):
    """从文本中提取 tool_call"""
    pattern = re.compile(r'<tool_call>(.*?)</tool_call>', re.DOTALL | re.IGNORECASE)
    blocks = pattern.findall(text)
    actions = []
    for blk in blocks:
        blk = blk.strip()
        try:
            actions.append(json.loads(blk))
        except json.JSONDecodeError as e:
            print(f'解析失败: {e}')
    return actions

# ===================== 主程序 =====================

def show_screenshot(image_path, action_parameter, save_path="screenshot_anno.png"):
    """在截图上标注操作点"""
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    if 'coordinate' in action_parameter:
        radius = 15
        center_x, center_y = action_parameter['coordinate'][0], action_parameter['coordinate'][1]
        draw.ellipse((center_x - radius, center_y - radius, center_x + radius, center_y + radius), fill="red", outline="red")
    else:
        return None
    image.save(save_path)
    return save_path

async def main():
    instruction = '搜一下今天NBA火箭队比赛结果'
    history = []
    max_step = 30
    model_name = 'gui-plus-2026-02-26'
    task_dir = f'data_{time.strftime("%Y%m%d_%H%M%S")}'
    web_tools = PlaywrightComputer(initial_url='https://www.baidu.com/', task_dir=task_dir)

    await web_tools.reset()
    stop_flag = False
    dashscope.api_key = os.getenv("DASHSCOPE_API_KEY", None)
    # 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID
    dashscope.base_http_api_url = 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1'
    session_id = str(uuid.uuid4())
    print('session_id ', session_id)

    for step_id in range(max_step):
        if stop_flag:
            break
        env_state = await web_tools.current_state(it=step_id)
        screen_shot = env_state['img_path']
        messages = get_messages(screen_shot, env_state, instruction, history)

        retry_time = 3
        for _ in range(retry_time):
            response = dashscope.MultiModalConversation.call(
                model=model_name, messages=messages, vl_high_resolution_images=True,
                headers={"x-dashscope-gui-session-id": session_id},
                stream=False
            )
            print(response['request_id'])
            try:
                output_text = response.output.choices[0].message.content[0]['text']
                break
            except Exception as e:
                print(response)
                print(e)
        else:
            raise Exception('retry_time out')
        print(output_text)

        thought = response.output.choices[0].message.reasoning_content
        if thought != '':
            output_text = f"<think>\n{thought}\n</think>{output_text}"

        action_list = extract_tool_calls(output_text)

        for action_id, action in enumerate(action_list):
            action_parameter = action['arguments']
            action_type = action_parameter['action']
            label = action_parameter.get('label', None)
            weki_url = "https://baike.baidu.com/"
            coordicate = []

            if label is not None:
                if label == "WINDOW":
                    coordicate = [500, 500]
                else:
                    ele = env_state["SoM"]["SoM_list"][label]
                    box = ele["bbox"]
                    x, y, w, h = box.get("x"), box.get("y"), box.get("width"), box.get("height")
                    nx = x + w / 2
                    ny = y + h / 2
                    coordicate = [nx, ny]
                    action_parameter['coordinate'] = coordicate

            if action_type == 'wait':
                await asyncio.sleep(action_parameter.get('time', 2))
            elif action_type == 'scroll':
                direction = action_parameter['direction']
                await web_tools.scroll_at(coordicate[0], coordicate[1], direction=direction, magnitude=300)
            elif action_type == 'select':
                text = action_parameter['option']
                await web_tools._select(coordicate[0], coordicate[1], text=text)
            elif action_type == 'goback':
                await web_tools.go_back()
            elif action_type == 'goto':
                url = action_parameter.get('url', '')
                await web_tools.navigate(url, normalize=True)
            elif action_type == 'click':
                await web_tools.click_at(coordicate[0], coordicate[1])
            elif action_type == 'type':
                text = action_parameter['text']
                await web_tools.type_text_at(coordicate[0], coordicate[1], text)
            elif action_type == 'wikipedia':
                await web_tools.navigate(weki_url, normalize=True)
            elif action_type == 'answer':
                text = action_parameter['text']
                print(f'Answer: {text}\n任务完成')
                stop_flag = True
                break

            anno_dir = os.path.join(task_dir, 'anno')
            if not os.path.exists(anno_dir):
                os.makedirs(anno_dir)
            show_screenshot(env_state['img_path_no_box'], action_parameter, f'{anno_dir}/anno_{step_id}_{action_id}.png')

        history.append({'output': output_text, 'image': screen_shot})
        await asyncio.sleep(2)

if __name__ == '__main__':
    asyncio.run(main())
```

### 工具调用

#### 步骤1. 构造 System Prompt

电脑 GUI 任务

```
# 定义自定义工具列表（根据需求传入，可选）
tool_list = [
    {
        "name": "save_to_file",
        "description": "Save text content to a file on the local filesystem.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The file path to save to"
                },
                "content": {
                    "type": "string",
                    "description": "The text content to save"
                }
            },
            "required": ["file_path", "content"]
        }
    }
]

# 使用标准结构包装自定义工具
tools_def = {"type": "function", "function": tool_list}

# 定义 GUI 工具
gui_tool = {
    "type": "function",
    "function": {
        "name": "computer_use",
        "description": "Use a mouse and keyboard to interact with a computer, and take screenshots.\n* This is an interface to a desktop GUI. You do not have access to a terminal or applications menu. You must click on desktop icons to start applications.\n* Some applications may take time to start or process actions, so you may need to wait and take successive screenshots to see the results of your actions. E.g. if you click on Firefox and a window doesn't open, try wait and taking another screenshot.\n* The screen's resolution is 1000x1000.\n* Whenever you intend to move the cursor to click on an element like an icon, you should consult a screenshot to determine the coordinates of the element before moving the cursor.\n* If you tried clicking on a program or link but it failed to load, even after waiting, try adjusting your cursor position so that the tip of the cursor visually falls on the element that you want to click.\n* Make sure to click any buttons, links, icons, etc with the cursor tip in the center of the element. Don't click boxes on their edges unless asked.",
        "parameters": {
            "properties": {
                "action": {
                    "description": "The action to perform. The available actions are:\n* `key`: Performs key down presses on the arguments passed in order, then performs key releases in reverse order.\n* `type`: Type a string of text on the keyboard.\n* `mouse_move`: Move the cursor to a specified (x, y) pixel coordinate on the screen.\n* `left_click`: Click the left mouse button at a specified (x, y) pixel coordinate on the screen.\n* `left_click_drag`: Click and drag the cursor to a specified (x, y) pixel coordinate on the screen.\n* `right_click`: Click the right mouse button at a specified (x, y) pixel coordinate on the screen.\n* `middle_click`: Click the middle mouse button at a specified (x, y) pixel coordinate on the screen.\n* `double_click`: Double-click the left mouse button at a specified (x, y) pixel coordinate on the screen.\n* `triple_click`: Triple-click the left mouse button at a specified (x, y) pixel coordinate on the screen (simulated as double-click since it's the closest action).\n* `scroll`: Performs a scroll of the mouse scroll wheel.\n* `hscroll`: Performs a horizontal scroll (mapped to regular scroll).\n* `wait`: Wait specified seconds for the change to happen.\n* `terminate`: Terminate the current task and report its completion status.\n* `answer`: Answer a question.",
                    "enum": ["key", "type", "mouse_move", "left_click", "left_click_drag", "right_click", "middle_click", "double_click", "triple_click", "scroll", "hscroll", "wait", "terminate", "answer"],
                    "type": "string"
                },
                "keys": {"description": "Required only by `action=key`.", "type": "array"},
                "text": {"description": "Required only by `action=type` and `action=answer`.", "type": "string"},
                "coordinate": {"description": "(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by `action=mouse_move` and `action=left_click_drag`.", "type": "array"},
                "pixels": {"description": "The amount of scrolling to perform. Positive values scroll up, negative values scroll down. Required only by `action=scroll` and `action=hscroll`.", "type": "number"},
                "time": {"description": "The seconds to wait. Required only by `action=wait`.", "type": "number"},
                "status": {"description": "The status of the task. Required only by `action=terminate`.", "type": "string", "enum": ["success", "failure"]}
            },
            "required": ["action"],
            "type": "object"
        }
    }
}

# 组合 GUI 工具和自定义工具，构建 System Prompt
system_prompt = """# Tools

You may call one or more functions to assist with the user query.

You are provided with function signatures within <tools></tools> XML tags:
<tools>
""" + json.dumps(gui_tool) + json.dumps(tools_def) + """
</tools>

For each function call, return a json object with function name and arguments within <tool_call></tool_call> XML tags:
<tool_call>
{"name": <function-name>, "arguments": <args-json-object>}
</tool_call>

# Response format

Response format for every step:
1) Action: a short imperative describing what to do in the UI.
2) A single <tool_call>...</tool_call> block containing only the JSON: {"name": <function-name>, "arguments": <args-json-object>}.

Rules:
- Output exactly in the order: Action, <tool_call>.
- Be brief: one sentence for Action.
- Do not output anything else outside those parts.
- If finishing, use 'terminate' function in the tool call."""
```

手机 GUI 任务

```
# 定义自定义工具列表（根据需求传入，可选）
tool_list = [
    {
        "name": "save_to_file",
        "description": "Save text content to a file on the local filesystem.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The file path to save to"
                },
                "content": {
                    "type": "string",
                    "description": "The text content to save"
                }
            },
            "required": ["file_path", "content"]
        }
    }
]

# 使用标准结构包装自定义工具
tools_def = {"type": "function", "function": tool_list}

# 定义 GUI 工具
gui_tool = {
    "type": "function",
    "function": {
        "name_for_human": "mobile_use",
        "name": "mobile_use",
        "description": "Use a touchscreen to interact with a mobile device, and take screenshots.\n* This is an interface to a mobile device with touchscreen. You can perform actions like clicking, typing, swiping, etc.\n* Some applications may take time to start or process actions, so you may need to wait and take successive screenshots to see the results of your actions.\n* The screen's resolution is 1000x1000.\n* Make sure to click any buttons, links, icons, etc with the cursor tip in the center of the element. Don't click boxes on their edges unless asked.",
        "parameters": {
            "properties": {
                "action": {
                    "description": 'The action to perform. The available actions are:\n* `key`: Perform a key event on the mobile device.\n    - This supports adb\'s `keyevent` syntax.\n    - Examples: "volume_up", "volume_down", "power", "camera", "clear".\n* `click`: Click the point on the screen with coordinate (x, y).\n* `long_press`: Press the point on the screen with coordinate (x, y) for specified seconds.\n* `swipe`: Swipe from the starting point with coordinate (x, y) to the end point with coordinates2 (x2, y2).\n* `type`: Input the specified text into the activated input box.\n* `system_button`: Press the system button.\n* `open`: Open an app on the device.\n* `wait`: Wait specified seconds for the change to happen.\n* `terminate`: Terminate the current task and report its completion status.',
                    "enum": [
                        "key",
                        "click",
                        "long_press",
                        "swipe",
                        "type",
                        "system_button",
                        "open",
                        "wait",
                        "terminate",
                    ],
                    "type": "string",
                },
                "coordinate": {
                    "description": "(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by `action=click`, `action=long_press`, and `action=swipe`.",
                    "type": "array",
                },
                "coordinate2": {
                    "description": "(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by `action=swipe`.",
                    "type": "array",
                },
                "text": {
                    "description": "Required only by `action=key`, `action=type`, and `action=open`.",
                    "type": "string",
                },
                "time": {
                    "description": "The seconds to wait. Required only by `action=long_press` and `action=wait`.",
                    "type": "number",
                },
                "button": {
                    "description": "Back means returning to the previous interface, Home means returning to the desktop, Menu means opening the application background menu, and Enter means pressing the enter. Required only by `action=system_button`",
                    "enum": ["Back", "Home", "Menu", "Enter"],
                    "type": "string",
                },
                "status": {
                    "description": "The status of the task. Required only by `action=terminate`.",
                    "type": "string",
                    "enum": ["success", "failure"],
                },
            },
            "required": ["action"],
            "type": "object",
        },
        "args_format": "Format the arguments as a JSON object.",
    },
}

# 组合 GUI 工具和自定义工具，构建 System Prompt
system_prompt = """# Tools

You may call one or more functions to assist with the user query.

You are provided with function signatures within <tools></tools> XML tags:
<tools>
""" + json.dumps(gui_tool) + json.dumps(tools_def) + """
</tools>

For each function call, return a json object with function name and arguments within <tool_call></tool_call> XML tags:
<tool_call>
{"name": <function-name>, "arguments": <args-json-object>}
</tool_call>

# Response format

Response format for every step:
1) Action: a short imperative describing what to do in the UI.
2) A single <tool_call>...</tool_call> block containing only the JSON: {"name": <function-name>, "arguments": <args-json-object>}.

Rules:
- Output exactly in the order: Action, <tool_call>.
- Be brief: one sentence for Action.
- Do not output anything else outside those parts.
- If finishing, use 'terminate' function in the tool call."""
```

#### 步骤2. 构造多轮对话消息

在工具调用场景下，需要正确构造多轮对话消息，包括历史消息管理和工具调用结果的传递。关键点是：**最后一个user消息需要使用<tool\_response>标记包裹工具执行结果**。

电脑 GUI 任务

```
def get_messages(image, instruction, history_output, system_prompt):
    """
    构造多轮对话消息

    参数:
        image: 当前截图路径
        instruction: 用户指令
        history_output: 历史对话记录 [{"output": "...", "tool_response": "...", "image": "..."}]
        system_prompt: 系统提示词
    """
    history_n = 4  # 保留最近4轮历史
    current_step = len(history_output)
    history_start_idx = max(0, current_step - history_n)

    # 构造历史操作摘要
    previous_actions = []
    for i in range(history_start_idx):
        if i < len(history_output):
            history_output_str = history_output[i]['output']
            if 'Action:' in history_output_str and '<tool_call>':
                history_output_str = history_output_str.split('Action:')[1].split('<tool_call>')[0].strip()
            previous_actions.append(f"Step {i + 1}: {history_output_str}")

    previous_actions_str = "\\n".join(previous_actions) if previous_actions else "None"

    instruction_prompt = f"""Please generate the next move according to the UI screenshot, instruction and previous actions.

Instruction: {instruction}

Previous actions:
{previous_actions_str}"""

    # 构造 messages 数组
    messages = [{"role": "system", "content": [{"text": system_prompt}]}]

    history_len = min(history_n, len(history_output))
    if history_len > 0:
        # 添加历史对话
        for history_id, history_item in enumerate(history_output[-history_n:], 0):
            if history_id == 0:
                messages.append({
                    "role": "user",
                    "content": [
                        {"text": instruction_prompt},
                        {"image": "file://" + history_item['image']}
                    ]
                })
            else:
                messages.append({
                    "role": "user",
                    "content": [{"image": "file://" + history_item['image']}]
                })
            messages.append({
                "role": "assistant",
                "content": [{"text": history_item['output']}]
            })
        # 添加当前截图，包含上一轮工具执行结果
        messages.append({
            "role": "user",
            "content": [
                {"text": "<tool_response>\n"},
                {"text": history_output[-1]['tool_response']},
                {"image": "file://" + image},
                {"text": "\n</tool_response>"}
            ]
        })
    else:
        # 首轮对话
        messages.append({
            "role": "user",
            "content": [
                {"text": instruction_prompt},
                {"image": "file://" + image}
            ]
        })

    return messages
```

手机 GUI 任务

```
def get_messages(image, instruction, history_output, system_prompt):
    """
    构造多轮对话消息（手机端）

    参数:
        image: 当前截图路径
        instruction: 用户指令
        history_output: 历史对话记录 [{"output": "...", "tool_response": "...", "image": "..."}]
        system_prompt: 系统提示词
    """
    from datetime import datetime

    history_n = 4  # 保留最近4轮历史
    current_step = len(history_output)
    history_start_idx = max(0, current_step - history_n)

    # 构造历史操作摘要
    previous_actions = []
    for i in range(history_start_idx):
        if i < len(history_output):
            history_output_str = history_output[i]['output']
            if 'Action:' in history_output_str and '<tool_call>':
                history_output_str = history_output_str.split('Action:')[1].split('<tool_call>')[0].strip()
            previous_actions.append(f"Step {i + 1}: {history_output_str}")

    previous_actions_str = "\\n".join(previous_actions) if previous_actions else "None"

    # 添加背景信息（日期）
    today = datetime.today()
    weekday_names = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    weekday = weekday_names[today.weekday()]
    formatted_date = today.strftime("%Y年%m月%d日") + " " + weekday
    ground_info = f'''今天的日期是:{formatted_date}。'''

    instruction_prompt = f"""Please generate the next move according to the UI screenshot, instruction and previous actions.

Instruction: {ground_info}{instruction}

Previous actions:
{previous_actions_str}"""

    # 构造 messages 数组
    messages = [{"role": "system", "content": [{"text": system_prompt}]}]

    history_len = min(history_n, len(history_output))
    if history_len > 0:
        for history_id, history_item in enumerate(history_output[-history_n:], 0):
            if history_id == 0:
                messages.append({
                    "role": "user",
                    "content": [
                        {"text": instruction_prompt},
                        {"image": "file://" + history_item['image']}
                    ]
                })
            else:
                messages.append({
                    "role": "user",
                    "content": [{"image": "file://" + history_item['image']}]
                })
            messages.append({
                "role": "assistant",
                "content": [{"text": history_item['output']}]
            })
        messages.append({
            "role": "user",
            "content": [
                {"text": "<tool_response>\n"},
                {"text": history_output[-1]['tool_response']},
                {"image": "file://" + image},
                {"text": "\n</tool_response>"}
            ]
        })
    else:
        messages.append({
            "role": "user",
            "content": [
                {"text": instruction_prompt},
                {"image": "file://" + image}
            ]
        })

    return messages
```

#### 步骤3. 解析模型输出

从模型输出中提取 `<tool_call>` 块并解析为 JSON，然后根据图像缩放比例进行坐标映射。详情请参见[解析模型输出与坐标映射](raw/model-user-guide/model-experience/text-generation-model/specialized-models/gui-automation.md)。

#### 步骤4. 执行GUI操作

实现 GUI 操作工具类，用于执行实际的界面操作（点击、输入、滚动等）。详情请参见[电脑端 GUI 操作工具类](https://help.aliyun.com/zh/model-studio/gui-automation#08495e2b6d7ki)和[手机端 GUI 操作工具类](raw/model-user-guide/model-experience/text-generation-model/specialized-models/gui-automation.md)。

#### 步骤5. 完整自动化流程

将以上步骤整合到完整的自动化流程中，循环执行截图 → 模型推理 → 执行GUI操作，直到任务完成。详情请参见下方完整示例代码。

电脑端工具调用完整代码

```
import os
import re
import json
import math
import time
import uuid
import pyautogui
import pyperclip
import dashscope
from PIL import Image

# ===================== 步骤1：System Prompt =====================

# 用户自定义工具列表（可根据实际需求传入）
tool_list = [{
    "name": "osworld_mcp_libreoffice_calc.adjust_column_width",
    "description": "Adjust the width of specified columns.",
    "parameters": {
        "type": "object",
        "properties": {
            "columns": {
                "type": "string",
                "description": "Column range to adjust (e.g., 'A:C')"
            },
            "width": {
                "type": "number",
                "description": "Width to set (in characters)"
            },
            "autofit": {
                "type": "boolean",
                "description": "Whether to autofit columns to content"
            }
        },
        "required": ["columns"]
    }
}]

tools_def = {
    "type": "function",
    "function": tool_list
}

# 电脑端基础动作空间
gui_tool = {"type": "function", "function": {"name": "computer_use", "description": "Use a mouse and keyboard to interact with a computer, and take screenshots.\\n* This is an interface to a desktop GUI. You do not have access to a terminal or applications menu. You must click on desktop icons to start applications.\\n* Some applications may take time to start or process actions, so you may need to wait and take successive screenshots to see the results of your actions. E.g. if you click on Firefox and a window doesn't open, try wait and taking another screenshot.\\n* The screen's resolution is 1000x1000.\\n* Make sure to click any buttons, links, icons, etc with the cursor tip in the center of the element. Don't click boxes on their edges unless asked.", "parameters": {"properties": {"action": {"description": "The action to perform. The available actions are:\\n* `key`: Performs key down presses on the arguments passed in order, then performs key releases in reverse order.\\n* `type`: Type a string of text on the keyboard.\\n* `mouse_move`: Move the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `left_click`: Click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `left_click_drag`: Click and drag the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `right_click`: Click the right mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `middle_click`: Click the middle mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `double_click`: Double-click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `triple_click`: Triple-click the left mouse button at a specified (x, y) pixel coordinate on the screen (simulated as double-click since it's the closest action).\\n* `scroll`: Performs a scroll of the mouse scroll wheel.\\n* `hscroll`: Performs a horizontal scroll (mapped to regular scroll).\\n* `wait`: Wait specified seconds for the change to happen.\\n* `terminate`: Terminate the current task and report its completion status.\\n* `answer`: Answer a question.\\n* `interact`: Resolve the blocking window by interacting with the user.", "enum": ["key", "type", "mouse_move", "left_click", "left_click_drag", "right_click", "middle_click", "double_click", "triple_click", "scroll", "hscroll", "wait", "terminate", "answer", "interact"], "type": "string"}, "keys": {"description": "Required only by `action=key`.", "type": "array"}, "text": {"description": "Required only by `action=type`, `action=answer` and `action=interact`.", "type": "string"}, "coordinate": {"description": "(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by `action=mouse_move` and `action=left_click_drag`.", "type": "array"}, "pixels": {"description": "The amount of scrolling to perform. Positive values scroll up, negative values scroll down. Required only by `action=scroll` and `action=hscroll`.", "type": "number"}, "time": {"description": "The seconds to wait. Required only by `action=wait`.", "type": "number"}, "status": {"description": "The status of the task. Required only by `action=terminate`.", "type": "string", "enum": ["success", "failure"]}}, "required": ["action"], "type": "object"}}}

# 拼接系统提示词
system_prompt = """# Tools

You may call one or more functions to assist with the user query.

You are provided with function signatures within <tools></tools> XML tags:
<tools>
""" + json.dumps(gui_tool) + json.dumps(tools_def) + """
</tools>

For each function call, return a json object with function name and arguments within <tool_call></tool_call> XML tags:
<tool_call>
{"name": <function-name>, "arguments": <args-json-object>}
</tool_call>

# Response format

Response format for every step:
1) Action: a short imperative describing what to do in the UI.
2) A single <tool_call>...</tool_call> block containing only the JSON: {"name": <function-name>, "arguments": <args-json-object>}.

Rules:
- Output exactly in the order: Action, <tool_call>.
- Be brief: one for Action.
- Do not output anything else outside those two parts.
- If finishing, use action=terminate in the tool call."""

# ===================== 步骤2：构造多轮对话消息 =====================

def get_messages(image, instruction, history_output, system_prompt):
    history_n = 4
    current_step = len(history_output)

    history_start_idx = max(0, current_step - history_n)
    previous_actions = []
    for i in range(history_start_idx):
        if i < len(history_output):
            history_output_str = history_output[i]['output']
            if 'Action:' in history_output_str and '<tool_call>':
                history_output_str = history_output_str.split('Action:')[1].split('<tool_call>')[0].strip()
            previous_actions.append(f"Step {i + 1}: {history_output_str}")

    previous_actions_str = "\\n".join(previous_actions) if previous_actions else "None"

    instruction_prompt = f"""
      Please generate the next move according to the UI screenshot, instruction and previous actions.

      Instruction: {instruction}

      Previous actions:
      {previous_actions_str}"""

    messages = [{"role": "system", "content": [{"text": system_prompt}]}]

    history_len = min(history_n, len(history_output))
    if history_len > 0:
        for history_id, history_item in enumerate(history_output[-history_n:], 0):
            if history_id == 0:
                messages.append({
                    "role": "user",
                    "content": [
                        {"text": instruction_prompt},
                        {"image": "file://" + history_item['image']}
                    ]
                })
            else:
                messages.append({
                    "role": "user",
                    "content": [{"image": "file://" + history_item['image']}]
                })
            messages.append({
                "role": "assistant",
                "content": [{"text": history_item['output']}],
            })
        messages.append({
            "role": "user",
            "content": [
                {"text": "<tool_response>\n"},
                {"text": history_output[-1]['tool_response']},
                {"image": "file://" + image},
                {"text": "\n</tool_response>"}
            ]
        })
    else:
        messages.append({
            "role": "user",
            "content": [
                {"text": instruction_prompt},
                {"image": "file://" + image}
            ]
        })
    return messages

# ===================== 步骤3：解析模型输出与坐标映射 =====================

def extract_tool_calls(text):
    pattern = re.compile(r'<tool_call>(.*?)</tool_call>', re.DOTALL | re.IGNORECASE)
    blocks = pattern.findall(text)
    actions = []
    for blk in blocks:
        blk = blk.strip()
        try:
            actions.append(json.loads(blk))
        except json.JSONDecodeError as e:
            print(f'解析失败: {e} | 片段: {blk[:80]}...')
    return actions

def smart_resize(height, width, factor=32, min_pixels=32*32*4, max_pixels=32*32*1280, max_long_side=8192):
    def round_by_factor(number, factor):
        return round(number / factor) * factor
    def ceil_by_factor(number, factor):
        return math.ceil(number / factor) * factor
    def floor_by_factor(number, factor):
        return math.floor(number / factor) * factor

    if height < 2 or width < 2:
        raise ValueError(f"height:{height} or width:{width} must be larger than factor:{factor}")
    elif max(height, width) / min(height, width) > 200:
        raise ValueError(f"absolute aspect ratio must be smaller than 200, got {height} / {width}")

    if max(height, width) > max_long_side:
        beta = max(height, width) / max_long_side
        height, width = int(height / beta), int(width / beta)

    h_bar = round_by_factor(height, factor)
    w_bar = round_by_factor(width, factor)

    if h_bar * w_bar > max_pixels:
        beta = math.sqrt((height * width) / max_pixels)
        h_bar = floor_by_factor(height / beta, factor)
        w_bar = floor_by_factor(width / beta, factor)
    elif h_bar * w_bar < min_pixels:
        beta = math.sqrt(min_pixels / (height * width))
        h_bar = ceil_by_factor(height * beta, factor)
        w_bar = ceil_by_factor(width * beta, factor)
    return h_bar, w_bar

# ===================== 步骤4：GUI 操作工具类 =====================

class ComputerTools:
    def __init__(self):
        self.image_info = None

    def load_image_info(self, path):
        width, height = Image.open(path).size
        self.image_info = (width, height)

    def get_screenshot(self, image_path, retry_times=3):
        if os.path.exists(image_path):
            os.remove(image_path)
        for i in range(retry_times):
            screenshot = pyautogui.screenshot()
            screenshot.save(image_path)
            if os.path.exists(image_path):
                self.load_image_info(image_path)
                return True
            else:
                time.sleep(0.1)
        return False

    def reset(self):
        pyautogui.hotkey('win', 'd')

    def press_key(self, keys):
        if isinstance(keys, list):
            cleaned_keys = []
            for key in keys:
                if isinstance(key, str):
                    if key.startswith("keys=["): key = key[6:]
                    if key.endswith("]"): key = key[:-1]
                    if key.startswith("['") or key.startswith('["'): key = key[2:] if len(key) > 2 else key
                    if key.endswith("']") or key.endswith('"]'): key = key[:-2] if len(key) > 2 else key
                    key = key.strip()
                    key_map = {"arrowleft": "left", "arrowright": "right", "arrowup": "up", "arrowdown": "down"}
                    key = key_map.get(key, key)
                    cleaned_keys.append(key)
                else:
                    cleaned_keys.append(key)
            keys = cleaned_keys
        else:
            keys = [keys]
        if len(keys) > 1:
            pyautogui.hotkey(*keys)
        else:
            pyautogui.press(keys[0])

    def type(self, text):
        pyperclip.copy(text)
        pyautogui.keyDown('ctrl')
        pyautogui.keyDown('v')
        pyautogui.keyUp('v')
        pyautogui.keyUp('ctrl')

    def mouse_move(self, x, y):
        pyautogui.moveTo(x, y)
        time.sleep(0.1)
        pyautogui.moveTo(x, y)

    def left_click(self, x, y):
        pyautogui.moveTo(x, y)
        time.sleep(0.1)
        pyautogui.click()

    def left_click_drag(self, x, y):
        pyautogui.dragTo(x, y, duration=0.5)
        pyautogui.moveTo(x, y)

    def right_click(self, x, y):
        pyautogui.moveTo(x, y)
        time.sleep(0.1)
        pyautogui.rightClick()

    def middle_click(self, x, y):
        pyautogui.moveTo(x, y)
        time.sleep(0.1)
        pyautogui.middleClick()

    def double_click(self, x, y):
        pyautogui.moveTo(x, y)
        time.sleep(0.1)
        pyautogui.doubleClick()

    def triple_click(self, x, y):
        pyautogui.moveTo(x, y)
        time.sleep(0.1)
        pyautogui.tripleClick()

    def scroll(self, pixels):
        pyautogui.scroll(pixels)

# ===================== 步骤5：完整自动化流程 =====================

def run_gui_automation(instruction, max_step=30):
    dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")
    # 以下为华北2（北京）地域的URL，，调用时请将WorkspaceId替换为真实的业务空间ID
    dashscope.base_http_api_url = 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1'
    model_name = 'gui-plus-2026-02-26'

    computer_tools = ComputerTools()
    computer_tools.reset()

    output_dir = os.path.join(os.path.expanduser("~"), "Desktop", "gui_automation")
    os.makedirs(output_dir, exist_ok=True)

    history = []
    stop_flag = False
    session_id = str(uuid.uuid4())
    print('session_id ', session_id)

    print(f"[任务] {instruction}")
    print("=" * 60)

    for step_id in range(max_step):
        if stop_flag:
            break

        print(f"\n[步骤 {step_id + 1}]")

        screen_shot = os.path.join(output_dir, f'screenshot_{step_id}.png')
        computer_tools.get_screenshot(screen_shot)

        messages = get_messages(screen_shot, instruction, history, system_prompt)

        retry_time = 3
        for _ in range(retry_time):
            response = dashscope.MultiModalConversation.call(
                model=model_name,
                messages=messages,
                vl_high_resolution_images=True,
                headers={"x-dashscope-gui-session-id": session_id},
                stream=False
            )
            print(response['request_id'])
            try:
                output_text = response.output.choices[0].message.content[0]['text']
                break
            except Exception as e:
                print(response)
                print(e)
        else:
            raise Exception('retry_time out')
        print(f"[模型输出]\n{output_text}\n")

        action_list = extract_tool_calls(output_text)
        if not action_list:
            print("未提取到有效操作")
            break

        tool_response = ""
        for action_id, action in enumerate(action_list):
            action_parameter = action['arguments']
            action_type = action_parameter['action']

            dummy_image = Image.open(screen_shot)
            resized_height, resized_width = smart_resize(
                dummy_image.height, dummy_image.width,
                factor=16, min_pixels=3136, max_pixels=1003520 * 200
            )

            for key in ['coordinate', 'coordinate1', 'coordinate2']:
                if key in action_parameter:
                    action_parameter[key][0] = int(action_parameter[key][0] / 1000 * resized_width)
                    action_parameter[key][1] = int(action_parameter[key][1] / 1000 * resized_height)

            if action_type in ['click', 'left_click']:
                computer_tools.left_click(action_parameter['coordinate'][0], action_parameter['coordinate'][1])
                print(f"✓ 左键点击 ({action_parameter['coordinate'][0]}, {action_parameter['coordinate'][1]})")
            elif action_type == 'mouse_move':
                computer_tools.mouse_move(action_parameter['coordinate'][0], action_parameter['coordinate'][1])
                print(f"✓ 移动鼠标")
            elif action_type == 'middle_click':
                computer_tools.middle_click(action_parameter['coordinate'][0], action_parameter['coordinate'][1])
                print(f"✓ 中键点击")
            elif action_type in ['right click', 'right_click']:
                computer_tools.right_click(action_parameter['coordinate'][0], action_parameter['coordinate'][1])
                print(f"✓ 右键点击")
            elif action_type in ['key', 'hotkey']:
                computer_tools.press_key(action_parameter['keys'])
                print(f"✓ 按键 {action_parameter['keys']}")
            elif action_type == 'type':
                computer_tools.type(action_parameter['text'])
                print(f"✓ 输入文本: {action_parameter['text']}")
            elif action_type == 'drag':
                computer_tools.left_click_drag(action_parameter['coordinate'][0], action_parameter['coordinate'][1])
                print(f"✓ 拖拽")
            elif action_type == 'scroll':
                if 'coordinate' in action_parameter:
                    computer_tools.mouse_move(action_parameter['coordinate'][0], action_parameter['coordinate'][1])
                computer_tools.scroll(action_parameter.get("pixels", 1))
                print(f"✓ 滚动 {action_parameter.get('pixels', 1)} 像素")
            elif action_type in ['computer_double_click', 'double_click']:
                computer_tools.double_click(action_parameter['coordinate'][0], action_parameter['coordinate'][1])
                print(f"✓ 双击")
            elif action_type == 'wait':
                time.sleep(action_parameter.get('time', 2))
                print(f"✓ 等待 {action_parameter.get('time', 2)} 秒")
            elif action_type == 'answer':
                print(f"✓ 任务完成: {action_parameter.get('text', '')}")
                tool_response = action_parameter.get('text', '')
                stop_flag = True
                break
            elif action_type in ['stop', 'terminate', 'done']:
                print(f"✓ 任务终止: {action_parameter.get('status', 'success')}")
                tool_response = f"Task terminated with status: {action_parameter.get('status', 'success')}"
                stop_flag = True
                break
            else:
                print(f"未知操作类型: {action_type}")
                tool_response = f"Unknown action type: {action_type}"

        history.append({'output': output_text, 'tool_response': tool_response, 'image': screen_shot})
        time.sleep(2)

    print("\n" + "=" * 60)
    print(f"[完成] 共执行 {len(history)} 步")

if __name__ == '__main__':
    run_gui_automation(
        instruction='帮我打开chrome,在百度中搜索阿里巴巴',
        max_step=30
    )
```

手机端工具调用完整代码

```
import json, os, subprocess
import dashscope, time, math, re
import uuid
from PIL import Image
from datetime import datetime

# ===================== 步骤1：System Prompt =====================

# 用户自定义工具列表（可根据实际需求传入）
tool_list = [{
    "name": "osworld_mcp_libreoffice_calc.adjust_column_width",
    "description": "Adjust the width of specified columns.",
    "parameters": {
        "type": "object",
        "properties": {
            "columns": {
                "type": "string",
                "description": "Column range to adjust (e.g., 'A:C')"
            },
            "width": {
                "type": "number",
                "description": "Width to set (in characters)"
            },
            "autofit": {
                "type": "boolean",
                "description": "Whether to autofit columns to content"
            }
        },
        "required": ["columns"]
    }
}]

tools_def = {
    "type": "function",
    "function": tool_list
}

# 手机端基础动作空间
gui_tool = {"type": "function", "function": {"name_for_human": "mobile_use", "name": "mobile_use", "description": "Use a touchscreen to interact with a mobile device, and take screenshots.\\n* This is an interface to a mobile device with touchscreen. You can perform actions like clicking, typing, swiping, etc.\\n* Some applications may take time to start or process actions, so you may need to wait and take successive screenshots to see the results of your actions.\\n* The screen's resolution is 1000x1000.\\n* Make sure to click any buttons, links, icons, etc with the cursor tip in the center of the element. Don't click boxes on their edges unless asked.", "parameters": {"properties": {"action": {"description": "The action to perform. The available actions are:\\n* `key`: Perform a key event on the mobile device.\\n    - This supports adb's `keyevent` syntax.\\n    - Examples: \\"volume_up\\", \\"volume_down\\", \\"power\\", \\"camera\\", \\"clear\\".\\n* `click`: Click the point on the screen with coordinate (x, y).\\n* `long_press`: Press the point on the screen with coordinate (x, y) for specified seconds.\\n* `swipe`: Swipe from the starting point with coordinate (x, y) to the end point with coordinates2 (x2, y2).\\n* `type`: Input the specified text into the activated input box.\\n* `system_button`: Press the system button.\\n* `open`: Open an app on the device.\\n* `wait`: Wait specified seconds for the change to happen.\\n* `answer`: Terminate the current task and output the answer.\\n* `interact`: Resolve the blocking window by interacting with the user.\\n* `terminate`: Terminate the current task and report its completion status.", "enum": ["key", "click", "long_press", "swipe", "type", "system_button", "open", "wait", "answer", "interact", "terminate"], "type": "string"}, "coordinate": {"description": "(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by `action=click`, `action=long_press`, and `action=swipe`.", "type": "array"}, "coordinate2": {"description": "(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by `action=swipe`.", "type": "array"}, "text": {"description": "Required only by `action=key`, `action=type`, `action=open`, `action=answer`,and `action=interact`.", "type": "string"}, "time": {"description": "The seconds to wait. Required only by `action=long_press` and `action=wait`.", "type": "number"}, "button": {"description": "Back means returning to the previous interface, Home means returning to the desktop, Menu means opening the application background menu, and Enter means pressing the enter. Required only by `action=system_button`", "enum": ["Back", "Home", "Menu", "Enter"], "type": "string"}, "status": {"description": "The status of the task. Required only by `action=terminate`.", "type": "string", "enum": ["success", "failure"]}}, "required": ["action"], "type": "object"}, "args_format": "Format the arguments as a JSON object."}}

# 拼接系统提示词
mobile_system_prompt = """# Tools

You may call one or more functions to assist with the user query.

You are provided with function signatures within <tools></tools> XML tags:
<tools>
""" + json.dumps(gui_tool) + json.dumps(tools_def) + """
</tools>

For each function call, return a json object with function name and arguments within <tool_call></tool_call> XML tags:
<tool_call>
{"name": <function-name>, "arguments": <args-json-object>}
</tool_call>

# Response format

Response format for every step:
1) Action: a short imperative describing what to do in the UI.
2) A single <tool_call>...</tool_call> block containing only the JSON: {"name": <function-name>, "arguments": <args-json-object>}.

Rules:
- Output exactly in the order: Action, <tool_call>.
- Be brief: one for Action.
- Do not output anything else outside those two parts.
- If finishing, use action=terminate in the tool call."""

# ===================== 步骤2：构造多轮对话消息 =====================

def get_messages(image, instruction, history_output, system_prompt):
    history_n = 4
    current_step = len(history_output)
    history_start_idx = max(0, current_step - history_n)

    previous_actions = []
    for i in range(history_start_idx):
        if i < len(history_output):
            history_output_str = history_output[i]['output']
            if 'Action:' in history_output_str and '<tool_call>':
                history_output_str = history_output_str.split('Action:')[1].split('<tool_call>')[0].strip()
            previous_actions.append(f"Step {i + 1}: {history_output_str}")

    previous_actions_str = "\\n".join(previous_actions) if previous_actions else "None"

    # 添加背景信息
    today = datetime.today()
    weekday_names = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    weekday = weekday_names[today.weekday()]
    formatted_date = today.strftime("%Y年%m月%d日") + " " + weekday
    ground_info = f'''今天的日期是:{formatted_date}。'''

    instruction_prompt = f"""
Please generate the next move according to the UI screenshot, instruction and previous actions.

Instruction: {ground_info}{instruction}

Previous actions:
{previous_actions_str}"""

    messages = [{"role": "system", "content": [{"text": system_prompt}]}]

    history_len = min(history_n, len(history_output))
    if history_len > 0:
        for history_id, history_item in enumerate(history_output[-history_n:], 0):
            if history_id == 0:
                messages.append({
                    "role": "user",
                    "content": [
                        {"text": instruction_prompt},
                        {"image": "file://" + history_item['image']}
                    ]
                })
            else:
                messages.append({
                    "role": "user",
                    "content": [{"image": "file://" + history_item['image']}]
                })
            messages.append({
                "role": "assistant",
                "content": [{"text": history_item['output']}],
            })
        messages.append({
            "role": "user",
            "content": [
                {"text": "<tool_response>\n"},
                {"text": history_output[-1]['tool_response']},
                {"image": "file://" + image},
                {"text": "\n</tool_response>"}
            ]
        })
    else:
        messages.append({
            "role": "user",
            "content": [
                {"text": instruction_prompt},
                {"image": "file://" + image}
            ]
        })
    return messages

# ===================== 步骤3：解析模型输出与坐标映射 =====================

def extract_tool_calls(text):
    pattern = re.compile(r'<tool_call>(.*?)</tool_call>', re.DOTALL | re.IGNORECASE)
    blocks = pattern.findall(text)
    actions = []
    for blk in blocks:
        blk = blk.strip()
        try:
            actions.append(json.loads(blk))
        except json.JSONDecodeError as e:
            print(f'解析失败: {e} | 片段: {blk[:80]}...')
    return actions

def smart_resize(height, width, factor=32, min_pixels=32*32*4, max_pixels=32*32*1280, max_long_side=8192):
    def round_by_factor(number, factor):
        return round(number / factor) * factor
    def ceil_by_factor(number, factor):
        return math.ceil(number / factor) * factor
    def floor_by_factor(number, factor):
        return math.floor(number / factor) * factor

    if height < 2 or width < 2:
        raise ValueError(f"height:{height} or width:{width} must be larger than factor:{factor}")
    elif max(height, width) / min(height, width) > 200:
        raise ValueError(f"absolute aspect ratio must be smaller than 200, got {height} / {width}")

    if max(height, width) > max_long_side:
        beta = max(height, width) / max_long_side
        height, width = int(height / beta), int(width / beta)

    h_bar = round_by_factor(height, factor)
    w_bar = round_by_factor(width, factor)

    if h_bar * w_bar > max_pixels:
        beta = math.sqrt((height * width) / max_pixels)
        h_bar = floor_by_factor(height / beta, factor)
        w_bar = floor_by_factor(width / beta, factor)
    elif h_bar * w_bar < min_pixels:
        beta = math.sqrt(min_pixels / (height * width))
        h_bar = ceil_by_factor(height * beta, factor)
        w_bar = ceil_by_factor(width * beta, factor)
    return h_bar, w_bar

# ===================== 步骤4：GUI 操作工具类 =====================

class AdbTools:
    def __init__(self, adb_path, device=None):
        self.adb_path = adb_path
        self.device = device
        self.__device_str__ = f" -s {device} " if device is not None else ' '
        self.image_info = None

    def adb_shell(self, command):
        command = self.adb_path + self.__device_str__ + command
        subprocess.run(command, capture_output=True, text=True, shell=True)

    def load_image_info(self, path):
        width, height = Image.open(path).size
        self.image_info = (width, height)

    def get_screenshot(self, image_path, retry_times=3):
        command = self.adb_path + (f" -s {self.device}" if self.device is not None else '') + f" exec-out screencap -p > {image_path}"

        for i in range(retry_times):
            subprocess.run(command, capture_output=True, text=True, shell=True)
            if os.path.exists(image_path):
                self.load_image_info(image_path)
                return True
            else:
                time.sleep(0.1)
        else:
            return False

    def click(self, x, y, coordinate_size=None):
        command = self.adb_path + self.__device_str__ + f" shell input tap {x} {y}"
        subprocess.run(command, capture_output=True, text=True, shell=True)

    def long_press(self, x, y, time=800):
        command = self.adb_path + self.__device_str__ + f" shell input swipe {x} {y} {x} {y} {time}"
        subprocess.run(command, capture_output=True, text=True, shell=True)

    def slide(self, x1, y1, x2, y2, coordinate_size=None, slide_time=800):
        command = self.adb_path + self.__device_str__ + f" shell input swipe {x1} {y1} {x2} {y2} {slide_time}"
        subprocess.run(command, capture_output=True, text=True, shell=True)

    def back(self):
        command = self.adb_path + self.__device_str__ + f"  shell input keyevent 4"
        subprocess.run(command, capture_output=True, text=True, shell=True)

    def home(self):
        command = self.adb_path + self.__device_str__ + f" shell am start -a android.intent.action.MAIN -c android.intent.category.HOME"
        subprocess.run(command, capture_output=True, text=True, shell=True)

    def type(self, text):
        escaped_text = text.replace('"', '\\"').replace("'", "\\'")
        command_list = [
            f"shell ime enable com.android.adbkeyboard/.AdbIME ",
            f"shell ime set com.android.adbkeyboard/.AdbIME ",
            0.1,
            f'shell am broadcast -a ADB_INPUT_TEXT --es msg "{escaped_text}" ',
            0.1,
            f"shell ime disable com.android.adbkeyboard/.AdbIME"
        ]

        for command in command_list:
            if isinstance(command, float):
                time.sleep(command)
            elif isinstance(command, str):
                subprocess.run(self.adb_path + self.__device_str__ + command.strip(), capture_output=True, text=True, shell=True)

# ===================== 步骤5：完整自动化流程 =====================

def run_mobile_automation(instruction, adb_path, max_step=50):
    dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")
    # 以下为华北2（北京）地域的URL，，调用时请将WorkspaceId替换为真实的业务空间ID
    dashscope.base_http_api_url = 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1'
    model_name = 'gui-plus-2026-02-26'

    adb_tools = AdbTools(adb_path=adb_path)
    adb_tools.home()
    time.sleep(1)

    task_dir = "mobile_automation"
    if os.path.exists(task_dir):
        import shutil
        shutil.rmtree(task_dir)
    os.mkdir(task_dir)

    history = []
    session_id = str(uuid.uuid4())
    print('session_id ', session_id)

    print(f"[任务] {instruction}")
    print("=" * 60)

    for step_id in range(max_step):
        print(f'\n[步骤 {step_id + 1}]')
        screen_shot = os.path.join(task_dir, f'screen_shot_{step_id}.png')
        adb_tools.get_screenshot(screen_shot)

        messages = get_messages(screen_shot, instruction, history, mobile_system_prompt)

        retry_time = 3
        for _ in range(retry_time):
            response = dashscope.MultiModalConversation.call(
                model=model_name,
                messages=messages,
                vl_high_resolution_images=True,
                headers={"x-dashscope-gui-session-id": session_id},
                stream=False
            )
            print(response['request_id'])
            try:
                output_text = response.output.choices[0].message.content[0]['text']
                break
            except Exception as e:
                print(response)
                print(e)
        else:
            raise Exception('retry_time out')
        print(f"[模型输出]\n{output_text}\n")

        action = json.loads(output_text.split('<tool_call>\n')[1].split('}}\n')[0] + '}}\n')
        action_parameter = action['arguments']

        dummy_image = Image.open(screen_shot)
        resized_height, resized_width = smart_resize(
            dummy_image.height, dummy_image.width,
            factor=16, min_pixels=3136, max_pixels=1003520*200
        )

        for key in ['coordinate', 'coordinate1', 'coordinate2']:
            if key in action_parameter:
                action_parameter[key][0] = int(action_parameter[key][0]/1000 * resized_width)
                action_parameter[key][1] = int(action_parameter[key][1]/1000 * resized_height)

        action_type = action_parameter['action']
        tool_response = ''

        if action_type == 'click':
            adb_tools.click(action_parameter['coordinate'][0], action_parameter['coordinate'][1])
            print(f"✓ 点击 ({action_parameter['coordinate'][0]}, {action_parameter['coordinate'][1]})")
        elif action_type == 'long_press':
            adb_tools.long_press(action_parameter['coordinate'][0], action_parameter['coordinate'][1])
            print(f"✓ 长按")
        elif action_type == 'type':
            adb_tools.type(action_parameter['text'])
            print(f"✓ 输入文本: {action_parameter['text']}")
        elif action_type in ['scroll', 'swipe']:
            adb_tools.slide(action_parameter['coordinate'][0], action_parameter['coordinate'][1],
                           action_parameter['coordinate2'][0], action_parameter['coordinate2'][1])
            print(f"✓ 滑动")
        elif action_type == 'system_button':
            system = action_parameter['button']
            if system == 'Back':
                adb_tools.back()
            elif system == 'Home':
                adb_tools.home()
            print(f"✓ 系统按钮: {system}")
        elif action_type == 'wait':
            time.sleep(action_parameter.get('time', 2))
            print(f"✓ 等待 {action_parameter.get('time', 2)} 秒")
        elif action_type == 'terminate':
            print(f"✓ 任务完成")
            tool_response = f"Task terminated with status: {action_parameter.get('status', 'success')}"
            break
        else:
            print(f"未知操作类型: {action_type}")
            tool_response = f"Unknown action type: {action_type}"

        history.append({'output': output_text, 'tool_response': tool_response, 'image': screen_shot})
        time.sleep(2)

    print("\n" + "=" * 60)
    print(f"[完成] 共执行 {len(history)} 步")

if __name__ == '__main__':
    # 注意：需要填入自己的 ADB 路径
    run_mobile_automation(
        instruction='帮我在携程搜一下今天济南喜来登酒店的价格',
        adb_path="/path/to/adb",
        max_step=50
    )
```

## 更多用法

-   [开启/关闭思考模式](raw/model-user-guide/model-experience/vision-model/vision.md)
-   [流式输出](https://help.aliyun.com/zh/model-studio/stream#e98db795e87q9)
-   [多轮对话](https://help.aliyun.com/zh/model-studio/multi-round-conversation#36eaa79f55dz7)
-   [传入本地文件](raw/model-user-guide/model-experience/vision-model/vision.md)

## 使用说明

### 图像限制

`gui-plus`模型对输入图像有以下具体要求：

-   **支持的图像格式：**
    
    **图像格式**
    
    **常见扩展名**
    
    **MIME Type**
    
    BMP
    
    .bmp
    
    image/bmp
    
    JPEG
    
    .jpe, .jpeg, .jpg
    
    image/jpeg
    
    PNG
    
    .png
    
    image/png
    
    TIFF
    
    .tif, .tiff
    
    image/tiff
    
    WEBP
    
    .webp
    
    image/webp
    
    HEIC
    
    .heic
    
    image/heic
    
-   **图像大小：**单个图像的大小不超过10 MB。如果传入 Base64编码的图像，需保证编码后的字符串小于10MB，详情请参见[传入本地文件](https://help.aliyun.com/zh/model-studio/vision#d987f8de5395x)。如需压缩文件体积请参见[图像或视频压缩方法](raw/model-user-guide/model-experience/vision-model/vision.md)。
    
-   **尺寸与比例：**图像的宽度和高度均需大于 10 像素，图像的宽高比（长边与短边的比值）不得超过 200。
    
-   **像素总量：**模型接受任意像素总量的图像输入，但会在内部将其缩放至特定处理上限，超过此上限的图像会损失细节。
    

### 图像输入方式

-   **公网URL：**提供一个公网可访问的图像地址，支持 HTTP 或 HTTPS 协议。可将本地图像[上传至OSS](https://help.aliyun.com/zh/oss/user-guide/console-quick-start)或[上传文件获取临时URL](raw/model-api-reference/more-about-models/get-temporary-file-url.md)，获取公网 URL。
-   **Base64编码传入：**将图像转换为 Base64 编码字符串。
-   **本地文件路径传入：**直接传入本地图像的路径。

## 计费与限流

-   **限流：**千问GUI-Plus模型的限流条件参见[限流](raw/model-user-guide/get-started-with-models/rate-limit.md)。
    
-   **免费额度**：从开通百炼或模型申请通过之日起计算有效期，有效期90天内，模型提供100万Token的免费额度。
    
-   **计费：**总费用 = 输入 Token 数 × 模型输入单价 + 模型输出 Token 数 × 模型输出单价；输入/输出价格可参见[选择模型](raw/model-user-guide/get-started-with-models/models.md)。
    
    图像转换为Token的规则
    
    图像 Token 数 = `(h_bar * w_bar) / token_pixels + 2`。
    
    -   `h_bar、w_bar`：缩放后的图像长宽，模型在处理图像前会进行预处理，会将图像缩小至特定像素上限内，像素上限与`max_pixels`和`vl_high_resolution_images`参数的取值有关。详情请参见[GUI-Plus API参考](raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)。
    -   `token_pixels`表示每视觉`Token`对应的像素值，目前固定为`28 * 28`（即`784`）。
    
    以下代码演示了模型内部对图像的大致缩放逻辑，可用于估算一张图像的Token，实际计费请以 API 响应为准。
    
    ```
    # 使用以下命令安装Pillow库：pip install Pillow
    import math
    from PIL import Image
    
    factor = 28
    def token_calculate(image_path, max_pixels, vl_high_resolution_images):
        # 打开指定的PNG图片文件
        image = Image.open(image_path)
    
        # 获取图片的原始尺寸
        height = image.height
        width = image.width
    
        # 根据不同模型，将宽高调整为factor的整数倍
        h_bar = round(height / factor) * factor
        w_bar = round(width / factor) * factor
    
        # 图像的Token下限：4 个 Token
        min_pixels = 4 * factor * factor
        # 若 vl_high_resolution_images 设置为True，则输入图像Token上限为16386，对应的最大的像素值为16384 * 28 * 28，否则为max_pixels设置的值
        if vl_high_resolution_images:
            max_pixels = 16384 * factor * factor
        else:
            max_pixels = max_pixels
    
        # 对图像进行缩放处理，调整像素的总数在范围[min_pixels,max_pixels]内
        if h_bar * w_bar > max_pixels:
            # 计算缩放因子beta，使得缩放后的图像总像素数不超过max_pixels
            beta = math.sqrt((height * width) / max_pixels)
            # 重新计算调整后的宽高
            h_bar = math.floor(height / beta / factor) * factor
            w_bar = math.floor(width / beta / factor) * factor
        elif h_bar * w_bar < min_pixels:
            # 计算缩放因子beta，使得缩放后的图像总像素数不低于min_pixels
            beta = math.sqrt(min_pixels / (height * width))
            # 重新计算调整后的高度
            h_bar = math.ceil(height * beta / factor) * factor
            w_bar = math.ceil(width * beta / factor) * factor
        return h_bar, w_bar
    
    if __name__ == "__main__":
        # 将test.png替换为本地的图像路径
        h_bar, w_bar = token_calculate("xxx/test.jpg", vl_high_resolution_images=False, max_pixels=16384*28*28, )
        print(f"缩放后的图像尺寸为：高度为{h_bar}，宽度为{w_bar}")
        # 系统会自动添加<vision_bos>和<vision_eos>视觉标记（各计1个Token）
        token = int((h_bar * w_bar) / (28 * 28))+2
        print(f"图像的Token数为{token}")
    ```
    
-   **查看账单：**您可以在阿里云控制台的[费用与成本](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)页面查看账单或进行充值。
    

## API参考

关于千问GUI-Plus模型的输入输出参数，请参见[GUI-Plus API参考](raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)。

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](raw/model-api-reference/preparations/error-code.md)进行解决。

GUI-Plus模型推荐提示词

电脑端 System Prompt

```
# Tools

You may call one or more functions to assist with the user query.

You are provided with function signatures within <tools></tools> XML tags:

<tools>
{
  "type": "function",
  "function": {
    "name": "computer_use",
    "description": "Use a mouse and keyboard to interact with a computer, and take screenshots.
* This is an interface to a desktop GUI. You do not have access to a terminal or applications menu. You must click on desktop icons to start applications.
* Some applications may take time to start or process actions, so you may need to wait and take successive screenshots to see the results of your actions. E.g. if you click on Firefox and a window doesn't open, try wait and taking another screenshot.
* The screen's resolution is {resized_width}x{resized_height}.
* Whenever you intend to move the cursor to click on an element like an icon, you should consult a screenshot to determine the coordinates of the element before moving the cursor.
* If you tried clicking on a program or link but it failed to load, even after waiting, try adjusting your cursor position so that the tip of the cursor visually falls on the element that you want to click.
* Make sure to click any buttons, links, icons, etc with the cursor tip in the center of the element. Don't click boxes on their edges unless asked.",
    "parameters": {
      "properties": {
        "action": {
          "description": "The action to perform. The available actions are:
* `key`: Performs key down presses on the arguments passed in order, then performs key releases in reverse order.
* `type`: Input a string of text. Use the `clear` parameter to decide whether to overwrite the existing text, and use the `enter` parameter to decide whether the enter key should be pressed after typing the text.
* `mouse_move`: Move the cursor to a specified (x, y) pixel coordinate on the screen.
* `click`: Click the left mouse button at a specified (x, y) pixel coordinate on the screen.
* `drag`: Click at a specified (x, y) pixel coordinate on the screen, and drag the cursor to another specified (x2, y2) pixel coordinate on the screen.
* `right_click`: Click the right mouse button at a specified (x, y) pixel coordinate on the screen.
* `middle_click`: Click the middle mouse button at a specified (x, y) pixel coordinate on the screen.
* `double_click`: Double-click the left mouse button at a specified (x, y) pixel coordinate on the screen.
* `scroll`: Performs a scroll of the mouse scroll wheel.
* `wait`: Wait specified seconds for the change to happen.
* `call_user`: Call the user when the task is unsolvable, or when you need the user's help, such as log in or close the pop up.
* `terminate`: Terminate the current task and report its completion status.",
          "enum": ["key", "type", "mouse_move", "click", "drag", "right_click", "middle_click", "double_click", "scroll", "wait", "call_user", "terminate"],
          "type": "string"
        },
        "keys": {
          "description": "Required only by `action=key`.",
          "type": "array"
        },
        "text": {
          "description": "Required only by `action=type`.",
          "type": "string"
        },
        "clear": {
          "description": "Assign it to 1 if the text should overwrite the existing text, otherwise assign it to 0. Using this argument clears all text in an element. Required only by `action=type`.",
          "type": "number"
        },
        "enter": {
          "description": "Assign it to 1 if the enter key should be pressed after typing the text, otherwise assign it to 0. Required only by `action=type`.",
          "type": "number"
        },
        "coordinate": {
          "description": "(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to.",
          "type": "array"
        },
        "coordinate2": {
          "description": "(x2, y2): The x2 (pixels from the left edge) and y2 (pixels from the top edge) coordinates to drag the cursor to. Required only by `action=drag`.",
          "type": "array"
        },
        "pixels": {
          "description": "The amount of scrolling to perform. Positive values scroll up, negative values scroll down. This value should be between -5 and 5. Required only by `action=scroll`.",
          "type": "number"
        },
        "time": {
          "description": "The seconds to wait. Required only by `action=wait`.",
          "type": "number"
        },
        "status": {
          "description": "The status of the task. Required only by `action=terminate`.",
          "type": "string",
          "enum": ["success", "failure"]
        }
      },
      "required": ["action"],
      "type": "object"
    }
  }
}
</tools>

For each function call, return a json object with function name and arguments within <tool_call></tool_call> XML tags:

<tool_call>
{"name": <function-name>, "arguments": <args-json-object>}
</tool_call>
```

手机端 System Prompt

```
# Tools

You may call one or more functions to assist with the user query.

You are provided with function signatures within <tools></tools> XML tags:

<tools>
{
  "type": "function",
  "function": {
    "name": "mobile_use",
    "description": "Use a touchscreen to interact with a mobile device, and take screenshots.
* This is an interface to a mobile device with touchscreen. You can perform actions like clicking, typing, swiping, etc.
* Some applications may take time to start or process actions, so you may need to wait and take successive screenshots to see the results of your actions.
* The screen's resolution is {resized_width}x{resized_height}.
* Make sure to click any buttons, links, icons, etc with the cursor tip in the center of the element. Don't click boxes on their edges unless asked.",
    "parameters": {
      "properties": {
        "action": {
          "description": "The action to perform. The available actions are:
* `key`: Perform a key event on the mobile device.
    - This supports adb's `keyevent` syntax.
    - Examples: \"volume_up\", \"volume_down\", \"power\", \"camera\", \"clear\".
* `click`: Click the point on the screen with coordinate (x, y).
* `long_press`: Press the point on the screen with coordinate (x, y) for specified seconds.
* `swipe`: Swipe from the starting point with coordinate (x, y) to the end point with coordinates2 (x2, y2).
* `type`: Input the specified text into the activated input box.
* `system_button`: Press the system button.
* `open`: Open an app on the device.
* `wait`: Wait specified seconds for the change to happen.
* `terminate`: Terminate the current task and report its completion status.",
          "enum": ["key", "click", "long_press", "swipe", "type", "system_button", "open", "wait", "terminate"],
          "type": "string"
        },
        "coordinate": {
          "description": "(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by `action=click`, `action=long_press`, and `action=swipe`.",
          "type": "array"
        },
        "coordinate2": {
          "description": "(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by `action=swipe`.",
          "type": "array"
        },
        "text": {
          "description": "Required only by `action=key`, `action=type`, and `action=open`.",
          "type": "string"
        },
        "time": {
          "description": "The seconds to wait. Required only by `action=long_press` and `action=wait`.",
          "type": "number"
        },
        "button": {
          "description": "Back means returning to the previous interface, Home means returning to the desktop, Menu means opening the application background menu, and Enter means pressing the enter. Required only by `action=system_button`",
          "enum": ["Back", "Home", "Menu", "Enter"],
          "type": "string"
        },
        "status": {
          "description": "The status of the task. Required only by `action=terminate`.",
          "type": "string",
          "enum": ["success", "failure"]
        }
      },
      "required": ["action"],
      "type": "object"
    }
  }
}
</tools>

For each function call, return a json object with function name and arguments within <tool_call></tool_call> XML tags:

<tool_call>
{"name": <function-name>, "arguments": <args-json-object>}
</tool_call>
```
