# Oneshot: Vibe Code Your Own AI Agent System

Oneshot was built to give friends and people in the Peregian Digital Hub network a powerful but approachable way to "vibe code" their own AI agent systems. There's something magical about creating your own specialised AI assistants, and we wanted to make that accessible to everyone—not just experienced developers.

This framework lets you create and orchestrate specialist AI agents without needing to understand complex infrastructure. You write a simple markdown file, and you have a working agent. You issue instructions to Cursor or Claude Code, and they orchestrate those specialised agents to perform useful knowledge work for you.

<div>
    <a href="https://www.loom.com/share/b434737c295c4b2483b375217d051339">
      <p>Creating a News Agent from Scratch - Watch Video</p>
    </a>
    <a href="https://www.loom.com/share/b434737c295c4b2483b375217d051339">
      <img style="max-width:300px;" src="https://cdn.loom.com/sessions/thumbnails/b434737c295c4b2483b375217d051339-12a0ff783b72514f-full-play.gif">
    </a>
</div>

## Quick Start

### Setup (2 minutes)
1. Clone this repo in Cursor: `https://github.com/chrisboden/oneshot`
2. Ask Cursor or Claude Code to set it up for you. You'll need your Openrouter key handy. It should be able to do the rest with a little bit of input from you.

Manual steps are:

1. Rename `.env_example` to `.env`
2. Add your [OpenRouter API key](https://openrouter.ai/keys) to `.env`
3. Run `pip install -r requirements.txt`
4. Open .cursor directory and rename mcp_example.json to mcp.json
5. In the mcp config json simply update the path you see there, ie `/Users/PATH/TO/oneshot/app/oneshot_mcp.py` to the where you actually have the oneshot repo on your computer.
6. Enable the oneshot mcp server in Cursor>Settings>Cursor Settings>Tools & Integrations

Optional but recommended:

1. Add your Logfire token to .env so that Cursor/Claude Code can inspect logs and help you debug when things go wrong. Cursor can guide you through how to do this.
2. Get a Brave search api key and add it to your .env file as you'll need it for some of the provided tools. Do that [here](https://brave.com/search/api/)

### Your First Agent

Simply ask your AI assistant (Cursor/Claude) to delegate tasks to one of the example agents provided:

**"Research the latest developments in vertical farming"** → Your assistant will use the research_agent

**"Describe this screenshot in detail (provide filepath)"** → Your assistant will use the vision_agent  

**"Create a match report for the latest Broncos game"** → Your assistant will use the nrl_agent

**"Create a news agent that produces pdf reports for any topic"** → Your assistant will build a custom news agent for you


## Create your own agents

Write a markdown file, get a working agent:

```markdown
# eg agents/content_agent.md
---
name: content_agent
model: openai/gpt-4.1-mini
tools: 
  - web_search
  - save_to_file
  - etc
---

You create engaging blog posts about tech trends.
Research the topic thoroughly, then write in a conversational tone.
```

That's it. Your agent is ready.

Want to create your own? Just ask Cursor: *"Create an agent that summarises YouTube videos"*


## Why Oneshot?

### Managing Token Costs Intelligently
Tools like Cursor and Claude Code that use the Claude models are getting expensive—$200 is the new $20. What if we could use cheaper models to do useful work for us and save those expensive tokens for high-value software development tasks?

Oneshot gives you access to pretty much all the models available via the OpenRouter gateway. You can use workhorses like GPT-4.1-mini to do the grunt work and powerful models like Gemini-2.5-flash or reasoning models from OpenAI and DeepSeek for more complex tasks. Importantly, you can use Cursor on Auto mode for free to do your agent orchestration work, keeping your expensive credits for actual coding.

<div>
    <a href="https://www.loom.com/share/4ed6992dd037446998f4182996524d46">
      <p>Demonstrating a OneShot Research agent - Watch Video</p>
    </a>
    <a href="https://www.loom.com/share/4ed6992dd037446998f4182996524d46">
      <img style="max-width:300px;" src="https://cdn.loom.com/sessions/thumbnails/4ed6992dd037446998f4182996524d46-78ab8d11ccb4c98f-full-play.gif">
    </a>
  </div>

### Learn by Building, Not Just Using
The Oneshot system is designed to make building agents a breeze. Create a markdown file in `/agents` with some frontmatter to specify the model, allocate a few tools, give it a system instruction, and you're off to the races. Better still, you can ask Cursor or Claude Code to create a new agent for you, and they'll read the instructions and do that in one shot without you having to lift a finger.

Most AI systems are black boxes—you see the magic but not how it works. Oneshot is transparent. You can watch agents make decisions in real-time, see exactly which tools they use and why, understand the conversation flow, and debug when things go sideways. Through the Logfire integration, you get a window into the agent's "thought process"—it's both educational and fascinating.

### Novel Context Engineering
Oneshot uses a novel context management approach where agents produce artifacts (files) and pass these files to each other to perform work. This allows for more accurate agent orchestration because the context window doesn't get crowded with voluminous tool output responses.

This lends itself to the orchestrator → sub-agent pattern, where an orchestrator agent (like Cursor or Claude Code) delegates tasks to specialist agents. The specialist agents perform the detailed work, which may involve many tool calls and lots of context processing, but they respond back with only the artifact they produced from that process. They agents can, in turn call other agents or sub agents to complete tasks. See the research agent for an example of how it uses a search analyst to perform discrete web search tasks. This keeps the main thread—the orchestrator's context window—clean and focused.

## Key Features

### Self-Aware and Vibecoding-Friendly
One of the goals of Oneshot is to make it vibecoding-friendly. Inspired by projects like Manus, Cursor itself, v0, and Lovable, the Oneshot system has built-in instructions and guides that help it help you. The system is self-describing to coding agents like Cursor and Claude Code, which means they know immediately how it works and can create agents and tools, or troubleshoot when things go wrong.

If you're curious, you can inspect these instructions in the `.cursor/rules` directory and the `app/guides` directory. The system has access to the Logfire MCP server for inspecting its own logs and the context7 MCP server for troubleshooting core technologies like PydanticAI and OpenRouter.

### All About Artifacts
Another design goal for this system is artifact creation. Whereas Claude Code, Cursor, Lovable, and v0 are all primarily designed to produce code as the primary artifact, there isn't really a "Cursor for knowledge work." The Oneshot system aims to let you develop agents and tools that can do knowledge work for you and create artifacts like emails written in your voice, reports in your company letterhead, blog posts that are on brand, slides with your company template.

The tool system is set up for creating these kinds of artifacts, and you can easily create agents that have multi-step workflows with tools that generate useful outputs for real work.

### Model Flexibility
Access hundreds of models through OpenRouter:
- openai/gpt-4.1-mini: Reliable workhorse for most tasks
- google/gemini-2.5-flash: Fast and capable for general work
- deepseek/deepseek-r1-0528: Advanced reasoning for complex problems
- anthropic/claude-sonnet-4: Nuanced writing and coding
- Plus many other specialised models

Visit the [Openrouter models page](https://openrouter.ai/models) to browse available models

### Learning About MCP Servers
The Oneshot system also provides a useful playground for learning about MCP servers, which is increasingly important as the ecosystem develops.

First, the system itself can be used as an MCP server. When Cursor or Claude Code call a specialist agent to do a task, they do that by calling the Oneshot MCP server. You can add the Oneshot MCP server to your global Cursor/Claude Code settings so you can use it in any repo or project.

Second, Oneshot agents act as MCP clients. This means they can call native tools and MCP servers—both local and remote. If you have an MCP server listed in your mcp.json file, you can allocate it to an agent. The system doesn't yet support MCP servers that use OAuth, but it's very handy for giving your agents access to things like your email, Notion, HubSpot, and more.

Finally, the Oneshot system knows how to build MCP servers for you. If you want it to build an MCP server that integrates with an external API, give it the link to the API docs, add the auth token to your .env file, and it should do the rest for you. Local MCP servers are saved in `/tools/local_mcp_servers`.

### Complete Visibility
With Logfire integration:
- Real-time agent decision tracking
- Token usage monitoring
- Performance optimisation insights
- Educational debugging experience

### Smart Usage Tracking
Built-in resource management prevents infinite loops and provides agents with self-awareness:
- **Real-time usage footers**: Every tool response shows progress like `🟢 *Tool usage: 15/30 calls (50%) - 15 remaining*`
- **Visual indicators**: Color-coded warnings (🟢🟡🟠🔴) help agents plan their resource usage
- **Intelligent error recovery**: When agents hit usage limits, delegation tools provide clear feedback to continue with partial results
- **Agent self-awareness**: The `usage_status` tool lets agents monitor and adapt their behavior based on remaining capacity

### Flexible use

You can use the oneshot system in a few different modes depending on your preference.

#### MCP Server Mode

Open the repo in Cursor or other AI-enabled IDE and the oneshot system becomes available as an MCP server to the coding agent (Cursor Agent, Cline, Roo, etc). In this mode, the coding agent does the orchestrating by using the oneshot mcp server to call your agents.

#### Terminal

Run oneshot in the terminal 

```bash
   cd app
   ./oneshot "please generate a report for the latest nrl game involving the Broncos"
```

#### Claude Code and other CLI's

Add oneshot as an mcp server either at project or global level. See included `CLAUDE.md` file which tells Claude how to use the oneshot system. Rename to `AGENTS.md` if you use Gemini or other coding CLI.


## Project Structure

```
oneshot/
├── agents/          # AI agents (markdown files)
├── tools/           # Python tools agents can use
├── artifacts/       # Agent-generated files
├── runs/            # Conversation histories
├── templates/       # Templates for creating formatted artifacts
└── snippets/        # Reusable text blocks for use in agent prompts
```

## Advanced Patterns

### Multi-Agent Workflows
Chain specialists for complex tasks:
```
Research Agent → Data Analyst → Report Writer → Editor
```

Each agent focuses on what it does best, passing clean artifacts forward.

### Artifact-First Design
Unlike code-focused tools, Oneshot creates knowledge work artifacts:
- Reports in your company template
- Emails in your voice
- Presentations with your branding
- Analysis with your methodology

### Lightweight Collaboration Philosophy
One of the principles for the Oneshot system is to enable very lightweight collaboration. If you create a useful agent or tool, you can share it via gist, and someone else using Oneshot can copy and paste it into a new markdown file in the `/agents` directory or a new python file in the `/tools` directory. No complex deployment, no package management—just sharing and experimenting.

## Built on Proven Stack

- **PydanticAI**: LLM integration and context management
- **OpenRouter**: Access to 200+ models through unified API
- **Logfire**: Real-time observability and debugging
- **MCP Protocol**: Interoperability with other AI tools

## Philosophy and Vision

The term "one shot" refers to an AI getting the right outcome the first time—from a single prompt, a coding agent creates perfect working software in one shot, without the need for correction and further "shots" to get it working. If you're working in AI, you're constantly in pursuit of a oneshot machine—a system that produces valuable outputs reliably, every time.

This project won't get it right in one shot every time, but that's the inspiration for it. There are a lot of behind-the-scenes prompts and instructions intended to have coding agents like Cursor and Claude Code be able to use this system and build things with it for you in one shot, without mistakes.

Oneshot was built for the Peregian Digital Hub community—a place where people experiment with emerging technologies. The core principles are accessibility (you shouldn't need a CS degree to build useful AI), transparency (see how agents actually work, don't just use them), experimentation (fast iteration cycles, low barrier to trying new ideas), collaboration (easy sharing of agents and tools), and practical value (build things that solve real problems).

Within a couple of hours, you'll have built out multiple agents with a growing portfolio of tools at their disposal. The goal is to demystify agentic systems and expose what goes into building them, while making the process genuinely enjoyable.

### Starter Tools for Immediate Productivity
The oneshot repo comes with a collection of starter tools that can be used in common knowledge work tasks. These include a todo system which allows agents to make plans and track progress (`todo_read`/`todo_write` tools); document management systemfor iterative document creation (`wip_doc_create`, `wip_doc_read`, `wip_doc_edit`); web search capabilities (`web_search`, `web_news_search`,`structured_search`, `web_image_search`- you'll need a free Brave Search API key); file operations (`file_creator`, `read_file_contents`, `export_as_pdf`, `export_as_screenshot`), and some research-specific tools like `research_planner`, `search_analyst`. 

We provide these starter tools because they represent the foundational building blocks that most knowledge work agents need—whether you're researching topics, managing documents, or creating reports. Having these tools ready-to-use means you can start building productive agents immediately without having to create basic infrastructure first.

The starter tools also serve as practical examples of how to build effective tools for the oneshot system. Each tool demonstrates proper error handling, clear parameter definitions, and useful output formatting. By studying these examples, you can quickly understand the patterns for creating your own tools. The tools are designed to be composable—you can chain them together in agents to create sophisticated workflows. For instance, the `research_agent` uses `web_search` to gather information, `search_analyst` to process the results, and `file_creator` to save the findings. This modular approach means you can focus on building specialized agents rather than reinventing common functionality.

Note: You do not have to use these - adapt or delete as you please.

### Starter Agents for Common Use Cases
The oneshot repo includes several pre-built agents that demonstrate different patterns and capabilities. The `research_agent` shows how to create agents that can perform comprehensive research tasks using multiple tools and sub-agents. The `vision_agent` demonstrates image and PDF analysis workflows, while the `nrl_agent` showcases structured report generation with specific formatting requirements. The `web_agent` shows how to build agents that can browse the web and extract information from web pages. These starter agents cover the most common knowledge work scenarios you're likely to encounter.

We provide these starter agents because they serve as both working examples and starting points for your own agent development. Each agent demonstrates different patterns for tool selection, prompt engineering, and workflow design. By studying these agents, you can quickly understand how to structure effective prompts, allocate appropriate tools, and design agents that produce useful outputs. The agents are designed to be easily customizable—you can modify their prompts, change their tool allocations, or use them as templates for creating new agents. For instance, you might use the `research_agent` as a base to create a specialized market research agent, or adapt the `nrl_agent` to create an agent that generates consistent structured reports in your company's templates.

Note: You do not have to use these - adapt or delete as you please.

## Getting Deeper

### Creating Custom Tools
Need something specific? Describe it to Cursor:
> "Create a tool that extracts data from PDFs and formats it as structured JSON"

The system will build it, often in one shot.

### Advanced Agent Design
Study the included examples to learn patterns:
- **Vision Agent**: Image analysis workflows
- **Research Agent**: Multi-source fact-checking
- **NRL Agent**: Structured report generation

### Context Engineering
Learn how different prompt patterns affect agent behavior. The system exposes everything, making it an excellent learning environment.

### MCP Server Development
Build integrations with your existing tools and services. The system can generate MCP servers from API documentation.

## Community

This isn't just an open source project—it's a learning environment. Built for people who want to understand AI agents by building them, not just using them.

Share your agents, tools, and discoveries. Every experiment teaches us something new about what's possible when AI becomes truly accessible.

---

Ready to build your first agent? Start with the examples, then let your imagination run wild.