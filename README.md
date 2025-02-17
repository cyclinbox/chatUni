# chatUni: A command line tool for AI chatting

## introduction

This is a small AI python tool. It utilizes APIs from [Baidu Qianfan platfrom](qianfan.baidubce.com/) and [Alibaba Bailian platform](https://bailian.console.aliyun.com/), and provide more than 10 models for using.

> See more: 
> + https://help.aliyun.com/zh/dashscope/developer-reference/api-details
> + https://help.aliyun.com/zh/dashscope/developer-reference/quick-start
> + https://help.aliyun.com/zh/dashscope/developer-reference/tongyi-thousand-questions-metering-and-billing
> + https://cloud.baidu.com/doc/WENXINWORKSHOP/s/flfmc9do2
> + https://cloud.baidu.com/doc/WENXINWORKSHOP/s/Nlks5zkzu
> + https://cloud.baidu.com/doc/WENXINWORKSHOP/s/clntwmv7t

## Requirements

It use Python3 and following python libraries:

```
requests
json
datetime
os
sys
platform
```

All libraries are python standard library except `requests`. Users can install `requests` by the following commands:

```cmd
python -m pip install requests
```

## Available models:

All available models:

```
[0]:    deepseek-r1(ernie)
[1]:    deepseek-r1(qwen)
[2]:    deepseek-v3(ernie)
[3]:    deepseek-v3(qwen)
[4]:    ernie-4.0-8k
[5]:    ernie-4.0-turbo-8k
[6]:    ernie-3.5-128k
[7]:    ernie-3.5-8K
[8]:    ernie-speed-128k
[9]:    ernie-speed-8K
[10]:   ernie-char-8k
[11]:   ernie-lite-8k
[12]:   ernie-tiny-8k
[13]:   qwen-max
[14]:   qwen-plus
[15]:   qwen-turbo
[16]:   qwen-long
[17]:   qwen-max-longcontext
[18]:   qwen1.5-72b-chat
[19]:   qwen1.5-72b-chat
[20]:   qwen1.5-14b-chat
[21]:   qwen1.5-7b-chat
[22]:   qwen-1.8b-chat
```

Both `deepseek-r1(ernie)` and `deepseek-r1(qwen)` are full-scale DeepSeek-R1 model, the only difference is the former one provided by [Baidu Qianfan platfrom](qianfan.baidubce.com/) while the later one provided by [Alibaba Bailian platform](https://bailian.console.aliyun.com/).

Default model is `deepseek-r1(ernie)` , users can switch model through `/chmod` command in the program.

## Usage

First, you should run

```
python chatUni-debug.py
```

in the terminal(or windows prompt, or any shell app). You will come into a interactive user interface like this:

```text
+-----------------------+
|  chatUni-CLI version  |
+-----------------------+
2025.02.12 modified.
Type `/exit` to exit program.                                                                                                                                                          
[User]:
```

You can type any question after `[User]:` prompt. 

### In-program command system

Any input start with `/` will be interpreted as a command. 

To show all available commands, you can input `/help`, and you will get some output like this:

```text
[User]: /help

[deepseek-r1(ernie)]:   Help:
    Basic commands:
        /help   Print this help message.
        /exit   Exit program.
        /chmod  Change model API.
        /replay Replay history messages.

    New chat commands:
        /clear  Clean both screen and history message.
        /hide   Only Clean screen, don't clean history.
        /reset  Clean history message.

    Export and import commands:
        /export [file name]
                Export all history message as an json file.
                `file name` parameter is optional.
                If user don't specify a file name, the program
                will use 'chatUni-history-YY-mm-dd_HHMMSS.json'
                as file name, while 'YY-mm-dd_HHMMSS' represent
                current date and time.
                Please do not include any space characters in
                the file name.
        /import <file name>
                Import history message from a json file.
                `file name` parameter is necessary.
                If user don't specify a file name, the program
                won't do anything.
                Please do not include any space characters in
                the file name.
    Use """ to begin a multi-line message.
```

To start a new chat session, you can input "/reset" or "/clear" command, and you will get a message "All reset! Start new topic now~"

```
[User]: /reset

[deepseek-r1(ernie)]:   All reset! Start new topic now~
```

Once you exit program (by `/exit` command), all chat history in this session will be lost. 

To save your chat history, you can use `/export` command, it will export your chat history into an json file. 

To re-use your chat history, you can use `/import` command to load chat history from a json file. You also can use `/replay` command to see them:

```
[User]: /reset

[qwen-turbo]:   All reset! Start new topic now~


[User]: /replay
------ replay start ------
------- replay end -------

[qwen-turbo]:   All history message replayed.


[User]: /import chatUni-history-25-02-17_170422.json

[qwen-turbo]:   Imported chat history from 'chatUni-history-25-02-17_170422.json'.


[User]: /replay
------ replay start ------

[user]: How to distinguish apple and pineapple?


[assistant]:    <reasoning></reasoning>Apples and pineapples are two very different fruits that can be distinguished by several characteristics:

1. Appearance:
- Apple: Round or oval shape, typically 3-4 inches in diameter. Smooth skin that comes in various colors like red, green, or yellow.
- Pineapple: A large, elongated tropical fruit with a tough, spiky outer shell. The edible part consists of many fused berries.

2. Skin texture:
- Apple: Thin, smooth, and edible.
- Pineapple: Thick, rough, and spiky exterior, with a waxy feel.

3. Stem:
- Apple: Has a small, stem-like structure at the top.
- Pineapple: Has a leafy tuft at the top rather than a stem.

4. Taste:
- Apple: Crisp, juicy, and sweet to tart flavor depending on variety.
- Pineapple: Sweet and tangy taste with high acidity.

5. Smell:
- Apple: Mild aroma, often described as slightly floral or fruity.
- Pineapple: Strong, sweet, and tropical scent.

6. Inside flesh:
- Apple: Creamy white to pale yellow flesh.
- Pineapple: Yellow flesh with fibrous strands.

7. Growth:
- Apple: Grows on trees.
- Pineapple: Grows as a Bromeliad plant low to the ground.

By examining these characteristics, you can easily tell an apple from a pineapple.<reasoning>

------- replay end -------

[qwen-turbo]:   All history message replayed.
```

### Multiple-line mode

Sometimes we need to input more than one line. However, in general, this program considers a line break as the end of a user input.

To begin a multi-line message, you can start the sentence with three English double quotes before entering it, and use three English quotes and the last line to end this multi-line message.

```
[User]: """
> Heilium walks into a bar
> The bar tender says"we don't serve noble gases in here."
> helium doesn't react.
> This joke is funny because what?
> """

[qwen-turbo]:  This joke is funny because it plays on the chemical property of helium, which is a noble gas. Noble gases are known for their tendency not to react chemically with other elements, hence the pun on "doesn't react" which works both as the bartender's observation about Helium's behavior and as a reference to helium's chemical inertness. The humor arises from the clever wordplay and the personification of a chemical element.
```

### Chain-of-Thought(CoT)

Currently, only DeepSeek-R1 ( `deepseek-r1(ernie)` and `deepseek-r1(qwen)` ) support CoT. The thinking steps will be provided in the `<think></think>` block.

```
[User]: """
> Heilium walks into a bar
> The bar tender says"we don't serve noble gases in here."
> helium doesn't react.
> This joke is funny because what? please answer me in English."""

[deepseek-r1(qwen)]:    <think>
Okay, so I need to figure out why this joke is funny. Let's break it down step by step. The joke goes like this: Heilium walks into a bar. The bartender says, "We don't serve noble gases in here." Helium doesn't react.

First, let's parse the elements. Helium is a noble gas, which is a group in the periodic table. Noble gases are known for being chemically inert, meaning they don't react easily with other elements. The bartender's statement is a play on words because "noble gases" are the actual elements, but the phrase "we don't serve noble gases here" sounds like a typical thing a bartender might say to refuse service, maybe similar to "we don't serve your type here" or something like that.

Then the punchline is "Helium doesn't react." Here, "react" has a double meaning. In chemistry, noble gases like helium don't undergo chemical reactions. But in everyday language, if someone is told they're not being served, they might react emotionally—get angry, protest, etc. So the humor comes from the double entendre: Helium, being a noble gas, doesn't react chemically, and in the joke's context, it also doesn't react emotionally to being refused service.

Wait, but the setup is "Heilium walks into a bar"—maybe there's a typo here? The element is Helium, not Heilium. But maybe that's intentional, like a play on the word "Heil" which is a German word associated with certain greetings, but that seems unrelated. More likely, it's just a typo and should be Helium. The bartender's refusal is based on the type of customer (noble gases), and Helium's non-reaction is both a chemical property and a play on not responding to the insult or rejection.

So the joke combines a pun on "react"—both the chemical and the emotional response—and the stereotype that noble gases are inert. The humor is in the wordplay and the unexpected twist using scientific facts to create a pun.
</think>

This joke is funny because it relies on a **pun** related to chemistry and wordplay:
1. **Noble gases** (like helium) are chemically inert, meaning they don’t easily react with other elements.
2. When the bartender says, “We don’t serve noble gases here,” it’s a playful refusal akin to a bar not serving certain “types” of people.
3. The punchline—“Helium doesn’t react”—has a **double meaning**:
   - Chemically: Helium, being a noble gas, doesn’t undergo chemical reactions.
   - Socially: Helium “doesn’t react” emotionally to the rejection (no anger, protest, etc.).

The humor comes from blending a scientific fact with human-like behavior, creating a clever, unexpected twist. 😄
```


