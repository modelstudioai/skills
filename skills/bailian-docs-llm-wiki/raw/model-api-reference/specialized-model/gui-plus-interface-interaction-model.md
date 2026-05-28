# GUI-Plus API参考

本文介绍通过 OpenAI 兼容接口 或 DashScope API 调用GUI-Plus模型的输入与输出参数。

> 相关文档：[界面交互专用模型（GUI-Plus）](https://help.aliyun.com/zh/model-studio/gui-automation)

## OpenAI 兼容

SDK 调用配置的`base_url`为：`https://dashscope.aliyuncs.com/compatible-mode/v1`

HTTP 调用配置的`endpoint`：`POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions`

> 您需要已[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。若通过OpenAI SDK进行调用，需要[安装SDK](https://help.aliyun.com/zh/model-studio/install-sdk)。

### 请求体

## 非流式输出

## Python

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
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="gui-plus-2026-02-26",
    messages=messages,
    extra_body={"vl_high_resolution_images": True}
)

print(completion.choices[0].message.content)
```

## Node.js

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
  baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1",
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

## curl

```
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
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

**返回结果**

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

## 流式输出

## Python

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
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="gui-plus-2026-02-26",
    messages=messages,
    stream=True,
    stream_options={"include_usage":True}
)
for chunk in completion:
    print(chunk.model_dump_json())
```

## Node.js

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
  baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1",
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

const openai = new OpenAI({
  // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx"
  apiKey: process.env.DASHSCOPE_API_KEY,
  baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
});

async function main() {
  const response = await openai.chat.completions.create({
    model: "gui-plus",
    messages: messages,
    stream:true,
    stream_options:{"include_usage":true}
  });

    console.log("流式输出内容为：")
    for await (const chunk of response) {
        // 如果stream_options.include_usage为true，则最后一个chunk的choices字段为空数组，需要跳过（可以通过chunk.usage获取 Token 使用量）
        if (chunk.choices[0] && chunk.choices[0].delta.content != null) {
          console.log(chunk.choices[0].delta.content);
        }
    }
}
main()
```

## curl

```
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
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
    "vl_high_resolution_images": true,
    "stream":true,
    "stream_options":{"include_usage":true}
  }'
```

**model** `_string_` **（必选）**

模型名称。支持的模型：gui-plus。

**messages** `_array_` **（必选）**传递给大模型的上下文，按对话顺序排列。

**消息类型**

System Message `_object_` （可选）

系统消息，用于设定大模型的角色、语气、任务目标或约束条件等。一般放在`messages`数组的第一位。

**属性**

**content** `_string_` **（必选）**

系统指令，用于明确模型的角色、行为规范、回答风格和任务约束等。

**role** `_string_` **（必选）**

系统消息的角色，固定为`system`。

User Message `_object_` **（必选）**

用户消息。

**属性**

**content** `_array_`**（必选）**

消息内容。

**属性**

**type** `_string_` **（必选）**

可选值：

-   `text`
    
    输入文本时需设为`text`。
    
-   `image_url`
    
    输入图片时需设为`image_url`。
    

**text** `_string_` **（可选）**

输入的文本。当`type`为`text`时，是必选参数。

**image\_url** `_object_`

输入的图片信息。当`type`为`image_url`时是必选参数。

**属性**

**url** `_string_`**（必选）**

图片的 URL或 Base64 Data URL。传入本地文件请参考[传入本地文件](https://help.aliyun.com/zh/model-studio/vision#a63fbac15a8s8)。

**min\_pixels** `_integer_` （可选）

用于设定输入图像的最小像素阈值，单位为像素。

当输入图像像素小于`min_pixels`时，会将图像进行放大，直到总像素高于`min_pixels`。

默认值和最小值均为 3136 。

**max\_pixels** `_integer_` （可选）

用于设定输入图像的最大像素阈值，单位为像素。

当输入图像像素在`[min_pixels, max_pixels]`区间内时，模型会按原图进行识别。当输入图像像素大于`max_pixels`时，会将图像进行缩小，直到总像素低于`max_pixels`。

默认值和最大值和[vl\_high\_resolution\_images](#3b5c2d499e544)的取值有关：

-   当 [vl\_high\_resolution\_images](#3b5c2d499e544) 为False时：默认值为1003520 ，最大值为12845056
    
-   当 [vl\_high\_resolution\_images](#3b5c2d499e544) 为True时：max\_pixels无效，输入图像的最大像素固定为12845056
    

**role** `_string_` **（必选）**

用户消息的角色，固定为`user`。

Assistant Message `_object_` （可选）

模型的回复。通常用于在多轮对话中作为上下文回传给模型。

**属性**

**content** `_string_` （必选）

模型回复的文本内容。

**role** `_string_` **（必选）**

助手消息的角色，固定为`assistant`。

**stream** `_boolean_` （可选） 默认值为 `false`

是否以流式方式输出回复。

可选值：

-   `false`：等待模型生成完整回复后一次性返回。
    
-   `true`：模型边生成边返回数据块。客户端需逐块读取，以还原完整回复。
    

**stream\_options** `_object_` （可选）

流式输出的配置项，仅在 `stream` 为 `true` 时生效。

**属性**

**include\_usage** `_boolean_` （可选）默认值为 `false`

是否在**最后一个数据块**包含Token消耗信息。

可选值：

-   `true`：包含；
    
-   `false`：不包含。
    

**max\_tokens** `_integer_` （可选）

用于限制模型输出的最大 Token 数。若生成内容超过此值，响应将被截断。

默认值与最大值均为模型的最大输出长度，请参见[适用范围](https://help.aliyun.com/zh/model-studio/qwen-vl-ocr#f4299b0a1ace4)。

**vl\_high\_resolution\_images** `_boolean_` （可选）默认值为`false`

是否将输入图像的像素上限提升至 16384 Token 对应的像素值。

-   `vl_high_resolution_images为true`，使用固定分辨率策略，像素上限固定为`12845056`，忽略 `max_pixels` 设置，超过此分辨率时会将图像总像素缩小至此上限内。
    
-   `vl_high_resolution_images`为`false`，像素上限由`max_pixels`决定，输入图像的像素超过`max_pixels`会将图像缩小至`max_pixels`内。模型的默认像素上限即`max_pixels`的默认值。
    

**enable\_thinking** `_boolean_` （可选）

使用混合思考（回复前既可思考也可不思考）模型时，是否开启思考模式。在界面交互系列模型中，仅`gui-plus-2026-02-26`为混合思考模型。相关文档：[视觉推理](https://help.aliyun.com/zh/model-studio/visual-reasoning#02ccad9e41nsv)

可选值：

-   `true`：开启
    
    > 开启后，思考内容将通过`reasoning_content`字段返回。
    
-   `false`：不开启
    

> 该参数非OpenAI标准参数。通过 Python SDK调用时，请放入 **extra\_body** 对象中。配置方式为：`extra_body={"enable_thinking": xxx}`。

**seed** `_integer_` （可选）

随机数种子。用于确保在相同输入和参数下生成结果可复现。若调用时传入相同的 `seed` 且其他参数不变，模型将尽可能返回相同结果。

取值范围：`[0,231−1]`。

**temperature** `_float_` （可选） 默认值为0.01

采样温度，控制模型生成文本的多样性。

temperature越高，生成的文本更多样，反之，生成的文本更确定。

取值范围： \[0, 2)

temperature与top\_p均可以控制生成文本的多样性，建议只设置其中一个值。

**top\_p** `_float_` （可选）默认值为0.01

核采样的概率阈值，控制模型生成文本的多样性。

top\_p越高，生成的文本更多样。反之，生成的文本更确定。

取值范围：（0,1.0\]

temperature与top\_p均可以控制生成文本的多样性，建议只设置其中一个值。

**top\_k** `_integer_` （可选）默认值为1

生成过程中采样候选集的大小。例如，取值为50时，仅将单次生成中得分最高的50个Token组成随机采样的候选集。取值越大，生成的随机性越高；取值越小，生成的确定性越高。取值为None或当top\_k大于100时，表示不启用top\_k策略，此时仅有top\_p策略生效。

取值需要大于或等于0。

该参数非OpenAI标准参数。通过 Python SDK调用时，请放入 **extra\_body** 对象中，配置方式为：`extra_body={"top_k": xxx}`；通过 Node.js SDK 或 HTTP 方式调用时，请作为顶层参数传递。

**repetition\_penalty** `_float_` （可选）默认值为1.0

模型生成时连续序列中的重复度。提高repetition\_penalty时可以降低模型生成的重复度，1.0表示不做惩罚。该参数对模型效果影响较大，建议保持默认值。

**presence\_penalty** `_float_` （可选）

控制模型生成文本时的内容重复度。默认值为1.5

取值范围：\[-2.0, 2.0\]。正值降低重复度，负值增加重复度。

在创意写作或头脑风暴等需要多样性、趣味性或创造力的场景中，建议调高该值；在技术文档或正式文本等强调一致性与术语准确性的场景中，建议调低该值。

**原理介绍**

如果参数值是正数，模型将对目前文本中已存在的Token施加一个惩罚值（惩罚值与文本出现的次数无关），减少这些Token重复出现的几率，从而减少内容重复度，增加用词多样性。

**示例**

提示词：把这句话翻译成中文“This movie is good. The plot is good, the acting is good, the music is good, and overall, the whole movie is just good. It is really good, in fact. The plot is so good, and the acting is so good, and the music is so good.”

参数值为2.0：这部电影很好。剧情很棒，演技棒，音乐也非常好听，总的来说，整部电影都好得不得了。实际上它真的很优秀。剧情非常精彩，演技出色，音乐也是那么的动听。

参数值为0.0：这部电影很好。剧情好，演技好，音乐也好，总的来说，整部电影都很好。事实上，它真的很棒。剧情非常好，演技也非常出色，音乐也同样优秀。

参数值为-2.0：这部电影很好。情节很好，演技很好，音乐也很好，总的来说，整部电影都很好。实际上，它真的很棒。情节非常好，演技也非常好，音乐也非常好。

**stop** `_string 或 array_` （可选）

用于指定停止词。当模型生成的文本中出现`stop` 指定的字符串或`token_id`时，生成将立即终止。

可传入敏感词以控制模型的输出。

> stop为数组时，不可将`token_id`和字符串同时作为元素输入，比如不可以指定为`["你好",104307]`。

### chat响应对象（非流式输出）

```
{
  "id": "chatcmpl-ef17511a-aceb-4c47-8757-13a87af2152d",
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "logprobs": null,
      "message": {
        "content": "```json\n{\"thought\": \"用户想要打开浏览器，我观察到屏幕截图中有一个Google Chrome的图标，其位置在右上角一排的最后一个。因此，下一步操作应该是点击这个Chrome浏览器图标来启动它。\", \"action\": \"click\", \"parameters\": {\"x\": 1086, \"y\": 129}}\n```",
        "refusal": null,
        "role": "assistant",
        "annotations": null,
        "audio": null,
        "function_call": null,
        "tool_calls": null
      }
    }
  ],
  "created": 1763451557,
  "model": "gui-plus",
  "object": "chat.completion",
  "service_tier": null,
  "system_fingerprint": null,
  "usage": {
    "completion_tokens": 78,
    "prompt_tokens": 2020,
    "total_tokens": 2098,
    "completion_tokens_details": {
      "accepted_prediction_tokens": null,
      "audio_tokens": null,
      "reasoning_tokens": null,
      "rejected_prediction_tokens": null,
      "text_tokens": 78
    },
    "prompt_tokens_details": {
      "audio_tokens": null,
      "cached_tokens": null,
      "image_tokens": 1244,
      "text_tokens": 776
    }
  }
}
```

**id** `_string_`

本次请求的唯一标识符。

**choices** `_array_`

模型生成内容的数组。

**属性**

**finish\_reason** `_string_`

模型停止生成的原因。

有两种情况：

-   自然停止输出时为`stop`；
    
-   生成长度过长而结束为`length`。
    

**index** `_integer_`

当前对象在`choices`数组中的索引。

**message** `_object_`

模型输出的消息。

**属性**

**content** `_string_`

GUI任务的结果。

**refusal** `_string_`

该参数当前固定为`null`。

**role** `_string_`

消息的角色，固定为`assistant`。

**audio** `_object_`

该参数当前固定为`null`。

**function\_call** `_object_`

该参数当前固定为`null`。

**tool\_calls** `_array_`

该参数当前固定为`null`。

**created** `_integer_`

本次请求被创建时的时间戳。

**model** `_string_`

本次请求使用的模型。

**object** `_string_`

始终为`chat.completion`。

**service\_tier** `_string_`

该参数当前固定为`null`。

**system\_fingerprint** `_string_`

该参数当前固定为`null`。

**usage** `_object_`

本次请求的 Token 消耗信息。

**属性**

**completion\_tokens** `_integer_`

模型输出的 Token 数。

**prompt\_tokens** `_integer_`

输入的 Token 数。

**total\_tokens** `_integer_`

消耗的总 Token 数，为`prompt_tokens`与`completion_tokens`的总和。

**completion\_tokens\_details** `_object_`

模型输出Token的细粒度分类。

**属性**

**accepted\_prediction\_tokens**`_integer_`

该参数当前固定为`null`。

**audio\_tokens** `_integer_`

该参数当前固定为`null`。

**reasoning\_tokens** `_integer_`

该参数当前固定为`null`。

**text\_tokens** `_integer_`

模型输出文本对应的 Token 数。

**rejected\_prediction\_tokens** `_integer_`

该参数当前固定为`null`。

**prompt\_tokens\_details** `_object_`

输入 Token 的细粒度分类。

**属性**

**audio\_tokens** `_integer_`

该参数当前固定为`null`。

**cached\_tokens** `_integer_`

该参数当前固定为`null`。

**text\_tokens** `_integer_`

模型输入的文本对应的Token 数。

**image\_tokens** `_integer_`

模型输入的图像对应的 Token数。

### chat响应chunk对象（流式输出）

```
ChatCompletionChunk(id='chatcmpl-9f3c627a-b0fc-4160-a558-3cc2cc7aa988', choices=[Choice(delta=ChoiceDelta(content='', function_call=None, refusal=None, role='assistant', tool_calls=None), finish_reason=None, index=0, logprobs=None)], created=1763452343, model='gui-plus', object='chat.completion.chunk', service_tier=None, system_fingerprint=None, usage=None)
ChatCompletionChunk(id='chatcmpl-9f3c627a-b0fc-4160-a558-3cc2cc7aa988', choices=[Choice(delta=ChoiceDelta(content='```', function_call=None, refusal=None, role=None, tool_calls=None), finish_reason=None, index=0, logprobs=None)], created=1763452343, model='gui-plus', object='chat.completion.chunk', service_tier=None, system_fingerprint=None, usage=None)
ChatCompletionChunk(id='chatcmpl-9f3c627a-b0fc-4160-a558-3cc2cc7aa988', choices=[Choice(delta=ChoiceDelta(content='json', function_call=None, refusal=None, role=None, tool_calls=None), finish_reason=None, index=0, logprobs=None)], created=1763452343, model='gui-plus', object='chat.completion.chunk', service_tier=None, system_fingerprint=None, usage=None)
ChatCompletionChunk(id='chatcmpl-9f3c627a-b0fc-4160-a558-3cc2cc7aa988', choices=[Choice(delta=ChoiceDelta(content=None, function_call=None, refusal=None, role=None, tool_calls=None), finish_reason=None, index=0, logprobs=None)], created=1763452343, model='gui-plus', object='chat.completion.chunk', service_tier=None, system_fingerprint=None, usage=None)
ChatCompletionChunk(id='chatcmpl-9f3c627a-b0fc-4160-a558-3cc2cc7aa988', choices=[Choice(delta=ChoiceDelta(content='\n{"thought": "', function_call=None, refusal=None, role=None, tool_calls=None), finish_reason=None, index=0, logprobs=None)], created=1763452343, model='gui-plus', object='chat.completion.chunk', service_tier=None, system_fingerprint=None, usage=None)
...
ChatCompletionChunk(id='chatcmpl-9f3c627a-b0fc-4160-a558-3cc2cc7aa988', choices=[Choice(delta=ChoiceDelta(content=' 1086', function_call=None, refusal=None, role=None, tool_calls=None), finish_reason=None, index=0, logprobs=None)], created=1763452343, model='gui-plus', object='chat.completion.chunk', service_tier=None, system_fingerprint=None, usage=None)
ChatCompletionChunk(id='chatcmpl-9f3c627a-b0fc-4160-a558-3cc2cc7aa988', choices=[Choice(delta=ChoiceDelta(content=', "y":', function_call=None, refusal=None, role=None, tool_calls=None), finish_reason=None, index=0, logprobs=None)], created=1763452343, model='gui-plus', object='chat.completion.chunk', service_tier=None, system_fingerprint=None, usage=None)
ChatCompletionChunk(id='chatcmpl-9f3c627a-b0fc-4160-a558-3cc2cc7aa988', choices=[Choice(delta=ChoiceDelta(content=' 127', function_call=None, refusal=None, role=None, tool_calls=None), finish_reason=None, index=0, logprobs=None)], created=1763452343, model='gui-plus', object='chat.completion.chunk', service_tier=None, system_fingerprint=None, usage=None)
ChatCompletionChunk(id='chatcmpl-9f3c627a-b0fc-4160-a558-3cc2cc7aa988', choices=[Choice(delta=ChoiceDelta(content='}}\n```', function_call=None, refusal=None, role=None, tool_calls=None), finish_reason='stop', index=0, logprobs=None)], created=1763452343, model='gui-plus', object='chat.completion.chunk', service_tier=None, system_fingerprint=None, usage=None)
ChatCompletionChunk(id='chatcmpl-bdb03054-42a2-459b-8a7e-5b94b39626f2', choices=[], created=1763452463, model='gui-plus', object='chat.completion.chunk', service_tier=None, system_fingerprint=None, usage=CompletionUsage(completion_tokens=78, prompt_tokens=2020, total_tokens=2098, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=None, audio_tokens=None, reasoning_tokens=None, rejected_prediction_tokens=None, text_tokens=78), prompt_tokens_details=PromptTokensDetails(audio_tokens=None, cached_tokens=None, image_tokens=1244, text_tokens=776)))
```

**id** `_string_`

本次调用的唯一标识符。每个chunk对象有相同的 id。

**choices** `_array_`

模型生成内容的数组。若设置`include_usage`参数为`true`，则在最后一个chunk中为空。

**属性**

**delta** `_object_`

流式返回的输出内容。

**属性**

**content** `_string_`

翻译结果，qwen-mt-flash为增量式更新，qwen-mt-plus和qwen-mt-turbo为非增量式更新。

**function\_call** `_object_`

该参数当前固定为`null`。

**refusal** `_object_`

该参数当前固定为`null`。

**role** `_string_`

消息对象的角色，只在第一个chunk中有值。

**finish\_reason** `_string_`

模型停止生成的原因。有三种情况：

-   自然停止输出时为`stop`；
    
-   生成未结束时为`null`；
    
-   生成长度过长而结束为`length`。
    

**index** `_integer_`

当前响应在`choices`数组中的索引。

**created** `_integer_`

本次请求被创建时的时间戳。每个chunk有相同的时间戳。

**model** `_string_`

本次请求使用的模型。

**object** `_string_`

始终为`chat.completion.chunk`。

**service\_tier** `_string_`

该参数当前固定为`null`。

**system\_fingerprint**`_string_`

该参数当前固定为`null`。

**usage** `_object_`

本次请求消耗的Token。只在`include_usage`为`true`时，在最后一个chunk返回。

**属性**

**completion\_tokens** `_integer_`

模型输出的 Token 数。

**prompt\_tokens** `_integer_`

输入的 Token 数。

**total\_tokens** `_integer_`

消耗的总 Token 数，为`prompt_tokens`与`completion_tokens`的总和。

**completion\_tokens\_details** `_object_`

模型输出Token的细粒度分类。

**属性**

**accepted\_prediction\_tokens**`_integer_`

该参数当前固定为`null`。

**audio\_tokens** `_integer_`

该参数当前固定为`null`。

**reasoning\_tokens** `_integer_`

该参数当前固定为`null`。

**text\_tokens** `_integer_`

模型输出文本对应的 Token 数。

**rejected\_prediction\_tokens** `_integer_`

该参数当前固定为`null`。

**prompt\_tokens\_details** `_object_`

输入 Token 的细粒度分类。

**属性**

**audio\_tokens** `_integer_`

该参数当前固定为`null`。

**cached\_tokens** `_integer_`

该参数当前固定为`null`。

**text\_tokens** `_integer_`

模型输入的文本对应的Token 数。

**image\_tokens** `_integer_`

模型输入的图像对应的 Token数。

## DashScope

-   HTTP 请求地址：`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`
    
-   SDK 调用：无需配置 `base_url`
    

> 您需要已[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。若通过DashScope SDK进行调用，需要[安装DashScope SDK](https://help.aliyun.com/zh/model-studio/install-sdk#f3e80b21069aa)。

### 请求体

## 非流式输出

## Python

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

## Java

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

public class Main {
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

## curl

```
curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
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

## 流式输出

## Python

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
    api_key = os.getenv('DASHSCOPE_API_KEY'),
    model = 'gui-plus',
    messages = messages,
    stream=True
)
for chunk in response:
    print(chunk)
```

## Java

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
import io.reactivex.Flowable;

public class Main {

    public static void streamCall()
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
                .model("gui-plus")
                .messages(Arrays.asList(userMessage,systemMsg))
                .incrementalOutput(true)
                .build();
        Flowable<MultiModalConversationResult> result = conv.streamCall(param);
        result.blockingForEach(item -> {
            try {
                var content = item.getOutput().getChoices().get(0).getMessage().getContent();
                // 判断content是否存在且不为空
                if (content != null &&  !content.isEmpty()) {
                    System.out.println(content.get(0).get("text"));
                }
            } catch (Exception e) {
                System.out.println(e.getMessage());
            }
        });
    }

    public static void main(String[] args) {
        try {
            streamCall();
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

## curl

```
curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-H "X-DashScope-SSE: enable" \
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

**model** `_string_` **（必选）**

模型名称。支持的模型：gui-plus。

**messages** `_array_` **（必选）**

传递给大模型的上下文，按对话顺序排列。

> 通过HTTP调用时，请将**messages** 放入 **input** 对象中。

**消息类型**

System Message `_object_` （可选）

系统消息，用于设定大模型的角色、语气、任务目标或约束条件等。一般放在`messages`数组的第一位。

**属性**

**content** `_string_` **（必选）**

系统指令，用于明确模型的角色、行为规范、回答风格和任务约束等。

**role** `_string_` **（必选）**

系统消息的角色，固定为`system`。

User Message `_object_`**（必选）**

用户消息，用于向模型传递问题、指令或上下文等。

**属性**

**content** `_string 或 array_`**（必选）**

消息内容。若输入只有文本，则为 string 类型；若输入包含图像数据，则为 array 类型。

**属性**

**text** `_string_`**（必选）**

输入的文本。

**image** `_string_`（可选）

传入的图片文件。可以为图片的URL或本地路径。传入本地文件请参见[传入本地文件](https://help.aliyun.com/zh/model-studio/vision#f18fc2bb52wxo)。

示例值：{"image":"https://xxxx.jpeg","max-pixels":1280\*28\*28}

**min\_pixels** `_integer_` （可选）

用于设定输入图像的最小像素阈值，单位为像素。

当输入图像像素小于`min_pixels`时，会将图像进行放大，直到总像素高于`min_pixels`。

默认值和最小值均为 3136 。

与 image 参数一起使用，示例：{"image":"https://xxxx.jpeg","min\_pixels":3136}

**max\_pixels** `_integer_` （可选）

用于设定输入图像的最大像素阈值，单位为像素。

当输入图像像素在`[min_pixels, max_pixels]`区间内时，模型会按原图进行识别。当输入图像像素大于`max_pixels`时，会将图像进行缩小，直到总像素低于`max_pixels`。

默认值和最大值和[vl\_high\_resolution\_images](#3b5c2d499e544)的取值有关：

-   当 [vl\_high\_resolution\_images](#3b5c2d499e544) 为False时：默认值为1003520 ，最大值为12845056
    
-   当 [vl\_high\_resolution\_images](#3b5c2d499e544) 为True时：max\_pixels无效，输入图像的最大像素固定为12845056
    

与 image 参数一起使用，示例：{"image":"https://xxxx.jpeg","max\_pixels":1003520 }

Assistant Message `_object_` （可选）

模型的回复。通常用于在多轮对话中作为上下文回传给模型。

**属性**

**content** `_string_` （必选）

模型回复的文本内容。

**role** `_string_` **（必选）**

助手消息的角色，固定为`assistant`。

**vl\_high\_resolution\_images** `_boolean_` （可选）默认值为`false`

是否将输入图像的像素上限提升至 16384 Token 对应的像素值。

-   `vl_high_resolution_images为true`，使用固定分辨率策略，像素上限固定为`12845056`，忽略 `max_pixels` 设置，超过此分辨率时会将图像总像素缩小至此上限内。
    
-   `vl_high_resolution_images`为`false`，像素上限由`max_pixels`决定，输入图像的像素超过`max_pixels`会将图像缩小至`max_pixels`内。模型的默认像素上限即`max_pixels`的默认值。
    

**enable\_thinking** `_boolean_` （可选）

使用混合思考模型时，是否开启思考模式。在界面交互系列模型中，仅`gui-plus-2026-02-26`为混合思考模型。相关文档：[视觉推理](https://help.aliyun.com/zh/model-studio/visual-reasoning#02ccad9e41nsv)

可选值：

-   `true`：开启
    
    > 开启后，思考内容将通过`reasoning_content`字段返回。
    
-   `false`：不开启
    

不同模型的默认值：[支持的模型](https://help.aliyun.com/zh/model-studio/deep-thinking#78286fdc35hlw)

> Java SDK 为enableThinking；通过HTTP调用时，请将 **enable\_thinking** 放入 **parameters** 对象中。

**max\_tokens** `_integer_` （可选）

用于限制模型输出的最大 Token 数。若生成内容超过此值，响应将被截断。

默认值与最大值均为模型的最大输出长度，请参见[模型选型](https://help.aliyun.com/zh/model-studio/machine-translation#efd59c2b9eosx)。

> Java SDK中为**maxTokens**_。_通过HTTP调用时，请将 **max\_tokens** 放入 **parameters** 对象中。

**seed** `_integer_` （可选）

随机数种子。用于确保在相同输入和参数下生成结果可复现。若调用时传入相同的 `seed` 且其他参数不变，模型将尽可能返回相同结果。

取值范围：`[0,231−1]`。

> 通过HTTP调用时，请将 **seed** 放入 **parameters** 对象中。

**temperature** `_float_` （可选） 默认值为0.01

采样温度，控制模型生成文本的多样性。

temperature越高，生成的文本更多样，反之，生成的文本更确定。

取值范围： \[0, 2)

temperature与top\_p均可以控制生成文本的多样性，建议只设置其中一个值。

> 通过HTTP调用时，请将 **temperature** 放入 **parameters** 对象中。

**top\_p** `_float_` （可选）默认值为0.01

核采样的概率阈值，控制模型生成文本的多样性。

top\_p越高，生成的文本更多样。反之，生成的文本更确定。

取值范围：（0,1.0\]

temperature与top\_p均可以控制生成文本的多样性，建议只设置其中一个值。

> Java SDK中为**topP**_。_通过HTTP调用时，请将 **top\_p** 放入 **parameters** 对象中。

**repetition\_penalty** `_float_` （可选）默认值为1.0

模型生成时连续序列中的重复度。提高repetition\_penalty时可以降低模型生成的重复度，1.0表示不做惩罚。该参数对模型效果影响较大，建议保持默认值。

> Java SDK中为**repetitionPenalty**_。_通过HTTP调用时，请将 **repetition\_penalty** 放入 **parameters** 对象中。

**presence\_penalty** `_float_` （可选）

控制模型生成文本时的内容重复度。默认值为1.5

取值范围：\[-2.0, 2.0\]。正值降低重复度，负值增加重复度。

在创意写作或头脑风暴等需要多样性、趣味性或创造力的场景中，建议调高该值；在技术文档或正式文本等强调一致性与术语准确性的场景中，建议调低该值。

**原理介绍**

如果参数值是正数，模型将对目前文本中已存在的Token施加一个惩罚值（惩罚值与文本出现的次数无关），减少这些Token重复出现的几率，从而减少内容重复度，增加用词多样性。

**示例**

提示词：把这句话翻译成中文“This movie is good. The plot is good, the acting is good, the music is good, and overall, the whole movie is just good. It is really good, in fact. The plot is so good, and the acting is so good, and the music is so good.”

参数值为2.0：这部电影很好。剧情很棒，演技棒，音乐也非常好听，总的来说，整部电影都好得不得了。实际上它真的很优秀。剧情非常精彩，演技出色，音乐也是那么的动听。

参数值为0.0：这部电影很好。剧情好，演技好，音乐也好，总的来说，整部电影都很好。事实上，它真的很棒。剧情非常好，演技也非常出色，音乐也同样优秀。

参数值为-2.0：这部电影很好。情节很好，演技很好，音乐也很好，总的来说，整部电影都很好。实际上，它真的很棒。情节非常好，演技也非常好，音乐也非常好。

**top\_k** `_integer_` （可选）默认值为1

生成过程中采样候选集的大小。例如，取值为50时，仅将单次生成中得分最高的50个Token组成随机采样的候选集。取值越大，生成的随机性越高；取值越小，生成的确定性越高。取值为None或当top\_k大于100时，表示不启用top\_k策略，此时仅有top\_p策略生效。

取值需要大于或等于0。

该参数非OpenAI标准参数。通过 Python SDK调用时，请放入 **extra\_body** 对象中，配置方式为：`extra_body={"top_k": xxx}`；通过 Node.js SDK 或 HTTP 方式调用时，请作为顶层参数传递。

> Java SDK中为**topK**_。_通过HTTP调用时，请将 **top\_k** 放入 **parameters** 对象中。

**repetition\_penalty** `_float_` （可选）默认值为1.0

模型生成时连续序列中的重复度。提高repetition\_penalty时可以降低模型生成的重复度，1.0表示不做惩罚。该参数对模型效果影响较大，建议保持默认值。

**stream** `_boolean_` （可选）

是否以流式方式输出回复。

可选值：

-   `false`：等待模型生成完整回复后一次性返回。
    
-   `true`：模型边生成边返回数据块。客户端需逐块读取，以还原完整回复。
    

> 该参数仅支持Python SDK。通过Java SDK实现流式输出请通过`streamCall`接口调用；通过HTTP实现流式输出请在Header中指定`X-DashScope-SSE`为`enable`。

**incremental\_output** `_boolean_` （可选）默认为`false`

在流式输出模式下是否开启增量输出。推荐您优先设置为`true`。

参数值：

-   false：每次输出为当前已经生成的整个序列，最后一次输出为生成的完整结果。
    
    ```
    I
    I like
    I like apple
    I like apple.
    ```
    
-   true（推荐）：增量输出，即后续输出内容不包含已输出的内容。您需要实时地逐个读取这些片段以获得完整的结果。
    
    ```
    I
    like
    apple
    .
    ```
    

> Java SDK中为**incrementalOutput**_。_通过HTTP调用时，请将 **incremental\_output** 放入 **parameters** 对象中。

**stop** `_string 或 array_` （可选）

用于指定停止词。当模型生成的文本中出现`stop` 指定的字符串或`token_id`时，生成将立即终止。

可传入敏感词以控制模型的输出。

> stop为数组时，不可将`token_id`和字符串同时作为元素输入，比如不可以指定为`["你好",104307]`。

### chat响应对象（流式与非流式输出格式一致）

```
{
  "status_code": 200,
  "request_id": "b74b3a25-3968-4059-8c44-63d793c07f02",
  "code": "",
  "message": "",
  "output": {
    "text": null,
    "finish_reason": null,
    "choices": [
      {
        "finish_reason": "stop",
        "message": {
          "role": "assistant",
          "content": [
            {
              "text": "```json\n{\"thought\": \"用户想要打开浏览器，我观察到屏幕截图中有一个Google Chrome的图标，其位置在右上角一排的最后一个。因此，下一步操作应该是点击这个Chrome浏览器图标来启动它。\", \"action\": \"CLICK\", \"parameters\": {\"x\": 1086, \"y\": 127}}\n```"
            }
          ]
        }
      }
    ],
    "audio": null
  },
  "usage": {
    "input_tokens": 2021,
    "output_tokens": 78,
    "characters": 0,
    "image_tokens": 1244,
    "input_tokens_details": {
      "image_tokens": 1244,
      "text_tokens": 777
    },
    "output_tokens_details": {
      "text_tokens": 78
    },
    "total_tokens": 2099
  }
}
```

**status\_code** `_string_`

本次请求的状态码。200 表示请求成功，否则表示请求失败。

> Java SDK不会返回该参数。调用失败会抛出异常，异常信息为**status\_code**和**message**的内容。

**request\_id** `_string_`

本次调用的唯一标识符。

> Java SDK返回参数为**requestId。**

**code** `_string_`

错误码，调用成功时为空值。

> 只有Python SDK返回该参数。

**output** `_object_`

调用结果信息。

**属性**

**text** `_string_`

该参数当前固定为`null`。

**finish\_reason** `_string_`

模型结束生成的原因。有以下情况：

-   正在生成时为`null`；
    
-   模型输出自然结束为`stop`；
    
-   因生成长度过长而结束为`length`；
    

**choices** `_array_`

模型的输出信息。

**属性**

**finish\_reason** `_string_`

有以下情况：

-   正在生成时为`null`；
    
-   因模型输出自然结束为`stop`；
    
-   因生成长度过长而结束为`length`；
    

**message** `_object_`

模型输出的消息对象。

**属性**

**role** `_string_`

输出消息的角色，固定为`assistant`。

**content** `_string_`

模型输出结果

**audio** `_string_`

该参数当前固定为`null`。

**usage** `_object_`

本次请求使用的Token信息。

**属性**

**input\_tokens** `_integer_`

输入 Token 数。

**output\_tokens** `_integer_`

输出 Token 数。

**image\_tokens** `_integer_`

输入内容包含`image`时返回该字段。为用户输入图片内容转换成Token后的长度。

**characters** `_integer_`

该参数当前固定为`null`。

**input\_tokens\_details** `_object_`

输入 Token 的细粒度分类。

**属性**

**image\_tokens** `_integer_`

模型输入的图像对应的 Token数。

**text\_tokens** `_integer_`

模型输入的文本对应的Token 数。

**output\_tokens\_details** `_object_`

输出 Token 的细粒度分类。

**属性**

**text\_tokens** `_integer_`

模型输入的文本对应的Token 数。

**total\_tokens** `_integer_`

消耗的总 Token 数，为`input_tokens`与`output_tokens`的总和。

## **错误码**

如果模型调用失败并返回报错信息，请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。
