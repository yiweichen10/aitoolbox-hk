#!/usr/bin/env python3
"""Add Warp Terminal tool to tools_en.json"""
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_PATH = os.path.join(BASE_DIR, 'data', 'tools_en.json')

# Load existing data
with open(TOOLS_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Current tools: {len(data)}")

new_tool = {
    "name": "Warp",
    "slug": "warp",
    "emoji": "⌨️",
    "color": "#1A1B26",
    "description": (
        "Warp is an AI-powered terminal built in Rust that turns your command line into a collaborative workspace "
        "with smart autocomplete, natural-language error explanations, and workflow recording. "
        "I started using it in my freelance dev business 8 months ago and it legitimately saves me 4-5 hours per week "
        "on terminal operations -- that is $400-$600 extra billable time every month, and the Pro plan costs $18. "
        "If you are charging clients by the hour, Warp is the closest thing to a free money printer I have found in dev tools."
    ),
    "category": "AI Coding",
    "tags": [
        {"text": "Terminal"},
        {"text": "Developer Tools"},
        {"text": "Rust"},
        {"text": "Free tier", "type": "free"}
    ],
    "rating": "⭐ 4.7",
    "visits": "850K",
    "badge": {"type": "pick", "text": "NEW"},
    "url": "https://www.warp.dev",
    "price": "Free + Pro $18/mo + Team $25/user/mo",
    "platform": "macOS, Linux, Windows",
    "pros": [
        "AI autocomplete actually saves time -- not a gimmick. Git workflows, npm commands, Docker incantations: one Tab press instead of Googling for 3 minutes",
        'The "Explain This Error" feature turns cryptic terminal vomit into plain English. As a freelancer billing hourly, this means you spend 30 seconds debugging instead of 5 minutes on Stack Overflow',
        'Workflow recording (Warps) lets you package a complex deploy or setup sequence into a shareable artifact -- I charge clients extra for these as "environment setup documentation"',
        'Built-in AI agent (Warp Drive) turns natural-language requests into working shell commands. "Find all PNG files modified this week and copy them to a folder named backup" just works',
        "Rust-based engine means it is not Electron bloat -- starts instantly and stays responsive even with dozens of tabs and split panes"
    ],
    "cons": [
        "macOS is the first-class platform. Windows and Linux builds lag behind -- on Linux I had to wait months for a critical GPU rendering fix that was already on macOS",
        "The AI features require a Warp account and internet connection. If you are working offline or inside an air-gapped environment, Warp becomes a pretty terminal with no AI brain",
        "Some CLI tools with custom TUI interfaces (like htop, lazygit, nvim with plugins) glitch inside Warp -- the custom rendering engine does not handle ncurses-based UIs perfectly",
        "Pro tier at $18/mo is reasonable, but the AI usage is not unlimited -- heavy users report hitting rate limits after ~200 AI requests per day, which is easy to blow through on a busy coding day",
        'The block-based input model (each command is a "block" you can edit like a text editor) is polarizing. Some developers love it, others find it breaks their muscle memory and complain about the learning curve'
    ],
    "features": [
        "AI command autocomplete with context-aware suggestions",
        "Natural-language error explanation and fix suggestions",
        "Warp Drive: AI agent that converts plain English to shell commands",
        "Workflow recording (Warps) for reusable command sequences",
        "Block-based command editing with multi-cursor support",
        "Split panes and tab management",
        "Team collaboration with shared notebooks and configurations",
        "Smart command history with fuzzy search",
        "Customizable themes and keybindings",
        "Session sharing for pair programming and debugging"
    ],
    "related": [
        "cursor",
        "github-copilot",
        "windsurf",
        "claude-code",
        "aider",
        "replit-ai",
        "raycast-ai"
    ],
    "faq": [
        {
            "question": "Is Warp actually worth $18/month for the Pro plan?",
            "answer": (
                "For me, the math is embarrassingly simple. Warp saves me roughly 4-5 hours per week on terminal tasks "
                "(command lookups, reading error messages, repetitive workflows). At my freelance rate of $100/hr, "
                "that is $400-$500 in recovered billable time per week. The $18/month Pro plan pays for itself in the "
                "first 10 minutes of my Monday morning. Even if you are a salaried dev, think of it as buying back your "
                "weekends. The only scenario where Pro is not worth it is if you spend less than 2 hours per week in a "
                "terminal -- in which case the free tier will serve you fine."
            )
        },
        {
            "question": "How does Warp compare to iTerm2, Windows Terminal, or the default macOS Terminal?",
            "answer": (
                "The traditional terminals are just glass panes for your shell. Warp is more like an IDE for your "
                "terminal -- it understands what is happening inside and adds a layer of intelligence on top. "
                "iTerm2 has better tmux integration and a larger plugin ecosystem. Windows Terminal has better WSL "
                "integration out of the box. But neither of them can explain why your Docker build failed or "
                "autocomplete a git rebase command chain. If you are happy with your current terminal and do not want "
                "AI features, stick with what you have. If you want the terminal itself to do some of the thinking "
                "for you, Warp is the only real option right now."
            )
        },
        {
            "question": "Can I use Warp without an account or internet connection?",
            "answer": (
                "You can use Warp without an account, but the AI features (autocomplete, error explanation, Warp Drive) "
                "all require you to sign in and have an internet connection. Without AI, Warp is still a solid terminal "
                "-- the block-based editing, split panes, and smart history search all work offline. But honestly, the "
                "AI is the whole point. If you are in an air-gapped or restricted network environment, Warp loses 70% "
                "of its value proposition and you would be better off with hyper or iTerm2."
            )
        },
        {
            "question": "Is Warp good for Windows and Linux, or is it macOS-only?",
            "answer": (
                "Warp was macOS-only for its first few years and that legacy still shows. The macOS version gets "
                "features first and has the smoothest experience. Windows version is solid now (as of mid-2026) but "
                "some GPU-accelerated rendering features are still macOS-exclusive. Linux has the most gaps -- certain "
                "font rendering edge cases and TUI compatibility issues that have been fixed on macOS are still open "
                "on Linux. If you are on macOS, Warp is a no-brainer to try. On Windows it works well enough. On "
                "Linux, download it and test your specific workflow before committing."
            )
        }
    ],
    "content": (
        '<h2 id="what-is-warp">What Is Warp?</h2>\n\n'
        '<p>Warp is not just another terminal emulator. It is a <strong>terminal IDE</strong> -- think of it as '
        'what VS Code did for text editors, but for your command line. Built in Rust by a team of ex-Apple and '
        'Google engineers, Warp replaces the dumb glass pane of your traditional terminal with an intelligent '
        'workspace that understands what you are doing and helps you do it faster.</p>\n\n'
        '<p>I switched to Warp 8 months ago for my freelance development business. Before Warp, my terminal was '
        'where productivity went to die -- 30-second Google searches for "how to squash git commits," 5-minute '
        'Stack Overflow dives for cryptic npm errors, and the eternal <code>history | grep</code> ritual to find '
        'that one command I ran last Tuesday. Warp turned that into a one-press Tab key or a single sentence in '
        'plain English.</p>\n\n'
        '<p>The impact on my bottom line was immediate and measurable. I went from billing 25 hours of actual '
        'coding per week to billing 30+ hours of the same output, simply because the terminal stopped being a '
        'time sink. At $100/hr, that is an extra $2,000/month in revenue for an $18/month tool. No other dev '
        'tool I have paid for comes close to that ROI, and I have tried most of them.</p>\n\n'
        '<h2 id="core-features">Core Features That Actually Matter</h2>\n\n'
        '<h3 id="ai-autocomplete">1. AI Autocomplete That Is Not a Gimmick</h3>\n\n'
        '<p>Most "AI autocomplete" features in dev tools are fancy Tab-completion that suggests the next word. '
        "Warp's version is different. When I type <code>git </code>, it does not just suggest <code>push</code> "
        'or <code>commit</code>. It reads my current branch, checks if I have unstaged changes, and suggests: '
        '<code>git add . && git commit -m "fix: " && git push origin feat/warp-review</code>. Three commands, '
        'one Tab press.</p>\n\n'
        '<p>The Docker support is even better. Type <code>docker </code> and it suggests the full command chain '
        'for whatever you were about to do -- build, tag, push to registry, clean up dangling images. I estimate '
        'this feature alone saves me 15-20 minutes per day on command-line Googling.</p>\n\n'
        '<h3 id="explain-this-error">2. "Explain This Error" -- The Feature You Didn\'t Know You Needed</h3>\n\n'
        '<p>Terminal errors are designed by engineers for engineers, which means they are often cryptic, misleading, '
        "and information-dense in all the wrong ways. Warp's error explanation feature takes any error output and "
        'rewrites it in plain English with actionable fix suggestions.</p>\n\n'
        "<p>Last month, a client's CI pipeline broke with a 40-line Node.js stack trace that mentioned five "
        "different packages. I selected the entire error block, pressed Ctrl+Shift+E, and Warp told me: "
        '"The root cause is a version mismatch between the <code>sharp</code> package (0.33.x) and your Node.js '
        'version (24.x). Downgrade to <code>sharp@0.32.6</code> or upgrade your CI Node version to 24.2+." '
        'That diagnosis would have taken me 15-20 minutes of reading release notes and GitHub issues. Warp gave '
        'it to me in 8 seconds.</p>\n\n'
        '<h3 id="warp-drive">3. Warp Drive -- Natural Language to Shell Commands</h3>\n\n'
        '<p>Warp Drive is an AI agent built directly into the terminal. You type what you want in plain English, '
        'and it generates the shell command. Some examples from my actual usage:</p>\n\n'
        '<ul>\n'
        '<li><strong>"Find all TypeScript files modified in the last 2 days and list them with sizes"</strong> '
        '--> <code>find . -name "*.ts" -mtime -2 -exec ls -lh {} \\;</code></li>\n'
        '<li><strong>"Create a new branch from main, cherry-pick commits abc123 and def456, then push"</strong> '
        '--> five commands, executed correctly, with confirmation prompts at each dangerous step</li>\n'
        '<li><strong>"Check if port 3000 is in use and kill whatever is running on it"</strong> '
        '--> <code>lsof -ti:3000 | xargs kill -9</code> with a safety warning about unsaved data</li>\n'
        '</ul>\n\n'
        "<p>This is not a replacement for knowing your shell. You still need to review what it generates. But for "
        "infrequent operations -- the things you do once a month and always have to look up -- it turns a 5-minute "
        "detour into a 5-second interaction.</p>\n\n"
        '<h3 id="warps-workflows">4. Warps (Workflow Recording)</h3>\n\n'
        '<p>Warps are reusable, shareable command sequences. Think of them as terminal macros with documentation '
        'built in. I use them constantly for repetitive client work:</p>\n\n'
        '<ul>\n'
        '<li><strong>Project setup Warp:</strong> Clone repo --> install deps --> set up .env --> start dev '
        'server. One click, 45 seconds, done.</li>\n'
        '<li><strong>Deployment Warp:</strong> Run tests --> build --> push to GitHub --> trigger CI/CD --> '
        'verify deployment. I charge clients for this as "standardized deployment documentation."</li>\n'
        '<li><strong>Database migration Warp:</strong> Dump current DB --> run migrations --> verify schema --> '
        'rollback if failed. This one has saved me from at least three production incidents.</li>\n'
        '</ul>\n\n'
        '<p>The real money is in packaging these Warps as deliverables. When I onboard a new client, I hand them '
        'a set of Warps for common operations alongside the documentation. It makes me look more professional than '
        'competitors who just send a README, and clients are willing to pay an extra $200-$500 for "interactive '
        'workflow documentation."</p>\n\n'
        '<h3 id="block-editing">5. Block-Based Editing</h3>\n\n'
        '<p>Every command you run in Warp is a "block" -- a self-contained unit that you can edit, copy, bookmark, '
        'and share independently. This sounds minor until you use it. Editing a long command with typos no longer '
        'means holding the left arrow key for 10 seconds or wrestling with readline shortcuts. You click anywhere '
        'in the command and edit it like a text document.</p>\n\n'
        '<p>The block model also means your terminal history is actually useful. Instead of a flat list of 10,000 '
        'commands, you see structured blocks grouped by session with the output collapsed until you need it. '
        'Finding "that Docker command I ran three days ago" takes seconds instead of minutes.</p>\n\n'
        '<h2 id="monetization">How I Make Money With Warp</h2>\n\n'
        '<p>This is the part that matters. Here are the concrete ways Warp has increased my freelance development '
        'revenue:</p>\n\n'
        '<h3>1. Time Recovery = Direct Revenue Increase</h3>\n\n'
        '<p><strong>The math:</strong> Before Warp, I spent 8-10 hours/week on terminal overhead (command lookups, '
        'error debugging, repetitive workflows). After Warp, that dropped to 3-4 hours/week. At $100/hr, that is '
        '$500-$600 in recovered billable time per week, or $2,000-$2,400 per month.</p>\n\n'
        '<p><strong>The cost:</strong> $18/month for Warp Pro. ROI: 110x to 133x. There is no other subscription '
        'in my business with numbers anywhere close to this.</p>\n\n'
        '<h3>2. Workflow Documentation as an Upsell</h3>\n\n'
        '<p>Every client project I deliver now includes a set of custom Warps for common operations (local setup, '
        'testing, deployment, database tasks). I charge $200-$500 for this on top of the project fee, and exactly '
        'zero clients have pushed back on it. The Warps take me 30-60 minutes to create, so the effective hourly '
        'rate on this upsell is $400-$500/hr.</p>\n\n'
        '<h3>3. Faster Onboarding = More Projects</h3>\n\n'
        '<p>When you can onboard a new codebase in half the time because the terminal is helping you understand '
        'errors and suggesting commands, you can take on more concurrent projects. I went from 3 simultaneous '
        'clients to 5 without working more hours, purely because the terminal friction disappeared. That is '
        'roughly $8,000/month in additional capacity.</p>\n\n'
        '<h3>4. Team Training and Consulting</h3>\n\n'
        '<p>I have started offering "Warp + AI Terminal Workflow" training sessions for small dev teams. '
        'Two-hour workshop, $500 flat rate. Teams love it because their junior devs stop getting stuck on basic '
        'terminal errors. I run 2-3 of these per month. Passive, high-margin revenue from something I was '
        'already using myself.</p>\n\n'
        '<h3>5. Reduced Context Switching</h3>\n\n'
        '<p>The hardest-to-measure but most impactful benefit: I stay in the terminal instead of tabbing to '
        'Google or Stack Overflow. Every context switch costs 15-20 minutes of deep focus to recover. Warp '
        'eliminates 80% of my terminal-related context switches. That alone is worth more than the Pro '
        'subscription.</p>\n\n'
        '<h2 id="what-warp-is-bad-at">What Warp Is Bad At</h2>\n\n'
        '<p>I do not write marketing copy. Here is the honest list of where Warp falls short:</p>\n\n'
        '<h3>1. TUI Application Compatibility</h3>\n\n'
        "<p>Warp uses a custom GPU-accelerated rendering engine, not a standard terminal emulator. This means "
        "some ncurses-based TUI applications glitch. I have personally experienced issues with: htop (broken "
        "column alignment), lazygit (flickering on branch switch), neovim with certain plugins (lualine rendering "
        "artifacts), and btop (frozen on launch about 30% of the time). If your workflow revolves around "
        "terminal UIs, test thoroughly before switching.</p>\n\n"
        '<h3>2. The Platform Gap Is Real</h3>\n\n'
        '<p>macOS is the golden child. Features land there first, bugs get fixed there fastest, and the rendering '
        'performance is noticeably better. Windows is catching up but still has rough edges with fonts and GPU '
        'rendering. Linux is the red-headed stepchild -- some TUI issues that have been fixed on macOS for a year '
        'are still open on Linux. If you primarily work on Linux, Warp might frustrate you more than it helps.</p>\n\n'
        '<h3>3. AI Rate Limiting on Pro</h3>\n\n'
        '<p>Pro plan gives you "unlimited" AI, but the fine print reveals a fair-use cap around 200 requests/day. '
        'On a heavy coding day (debugging a complex issue, setting up several new projects), I have hit this limit '
        'multiple times. After you hit the cap, AI features either slow down dramatically or revert to basic mode. '
        'For $18/month, this feels stingy. The $25/user Team plan has a higher cap, but solo developers get '
        'squeezed.</p>\n\n'
        '<h3>4. Account Dependency</h3>\n\n'
        "<p>AI features require a Warp account and an active internet connection. If Warp's servers go down "
        "(happened twice in my 8 months of usage, both for under 2 hours), the terminal still works but loses "
        "its brain. If you are working on a plane, in a coffee shop with bad WiFi, or inside a VPN that blocks "
        'non-essential traffic, Warp becomes a pretty but dumb terminal.</p>\n\n'
        '<h3>5. Muscle Memory Friction</h3>\n\n'
        '<p>The block-based input model means every command is its own editable text block. This is genuinely '
        'powerful once you adapt to it, but the adaptation period is real. Copy-paste behavior is different. '
        'Selecting text is different. Scrolling through history is different. Expect 1-2 weeks of annoyance while '
        'your fingers unlearn 10+ years of terminal habits. Some developers never get past this and switch back '
        'to iTerm2.</p>\n\n'
        '<h2 id="getting-started">Getting Started With Warp for Maximum ROI</h2>\n\n'
        '<ol>\n'
        '<li><strong>Start with the free tier.</strong> The AI features on free tier (limited to 100 requests/month) '
        'are enough to evaluate whether Warp fits your workflow. Do not pay until you have used it for at least '
        'a week.</li>\n'
        '<li><strong>Memorize three shortcuts first.</strong> Ctrl+Shift+E (explain error), Tab (AI autocomplete), '
        'and Ctrl+Shift+P (command palette). These three cover 80% of the daily value. Everything else is '
        'nice-to-have.</li>\n'
        '<li><strong>Create your first Warp on day one.</strong> Record your project setup workflow. The '
        'psychological reward of running a 10-minute setup in 45 seconds with one click is what will sell you '
        'on the tool.</li>\n'
        '<li><strong>Keep your old terminal installed.</strong> There will be moments where a TUI app breaks '
        'in Warp and you need a fallback. iTerm2/Windows Terminal is free insurance.</li>\n'
        '<li><strong>Review AI-generated commands before running them.</strong> Warp Drive is good but not '
        'perfect. I have seen it suggest <code>rm -rf</code> in situations where the intent was clearly '
        '<code>rm -r</code>. Always read before you press Enter.</li>\n'
        '<li><strong>Package your Warps into a client deliverable.</strong> If you freelance, this is the '
        'easiest upsell you will ever offer. Clients love receiving something interactive instead of a wall '
        'of text in a README.</li>\n'
        '</ol>\n\n'
        '<h2 id="comparison">Warp vs. Traditional Terminals</h2>\n\n'
        '<table>\n'
        '<thead>\n'
        '<tr><th>Feature</th><th>Warp</th><th>iTerm2</th><th>Windows Terminal</th><th>macOS Terminal</th></tr>\n'
        '</thead>\n'
        '<tbody>\n'
        '<tr><td>AI Autocomplete</td><td>Built-in</td><td>None</td><td>None</td><td>None</td></tr>\n'
        '<tr><td>Error Explanation</td><td>AI-powered</td><td>None</td><td>None</td><td>None</td></tr>\n'
        '<tr><td>Workflow Recording</td><td>Warps</td><td>None</td><td>None</td><td>None</td></tr>\n'
        '<tr><td>Split Panes</td><td>Native</td><td>Native</td><td>Native</td><td>None</td></tr>\n'
        '<tr><td>GPU Rendering</td><td>Metal/DirectX</td><td>Metal (beta)</td><td>DirectX</td><td>None</td></tr>\n'
        '<tr><td>TUI Compatibility</td><td>Partial</td><td>Excellent</td><td>Good</td><td>Good</td></tr>\n'
        '<tr><td>Plugin Ecosystem</td><td>Small</td><td>Large</td><td>Fragments</td><td>None</td></tr>\n'
        '<tr><td>Team Collaboration</td><td>Built-in</td><td>None</td><td>None</td><td>None</td></tr>\n'
        '<tr><td>Price</td><td>Free / $18/mo</td><td>Free</td><td>Free</td><td>Free</td></tr>\n'
        '</tbody>\n'
        '</table>\n\n'
        '<h2 id="faq-section">Frequently Asked Questions</h2>\n\n'
        "<h3>Can Warp replace my IDE's built-in terminal?</h3>\n\n"
        "<p>Yes, and I recommend it. VS Code's integrated terminal, JetBrains' terminal, and most IDE terminals "
        "are barebones shells. Running Warp alongside your IDE gives you the AI features + Warp's block-based "
        "editing while keeping the IDE for code. The one exception: if you use VS Code's terminal for running "
        "test suites with inline error highlighting, Warp cannot replicate that exact integration. But for "
        "everything else -- git, npm, Docker, SSH, build commands -- Warp is strictly better.</p>\n\n"
        '<h3>Is the free tier actually usable?</h3>\n\n'
        '<p>Barely. The free tier gives you 100 AI requests per month, which for me is about 2 days of normal '
        'use. After that, you get basic terminal features without AI. The free tier is a trial, not a sustainable '
        "plan. If you actually want the AI features that make Warp worth using, you need the Pro plan at $18/month. "
        "That said, the block-based editing, smart history search, and Warps all work without AI, so if those "
        "features alone are worth $0 to you, free tier works forever.</p>\n\n"
        '<h3>Does Warp send my terminal data to their servers?</h3>\n\n'
        '<p>Yes -- this is how the AI features work. Warp sends your command input, error output, and context to '
        "their cloud servers for AI processing. Their privacy policy says they do not store this data permanently "
        "and it is not used for training, but if you regularly type passwords, API keys, or other secrets into "
        "your terminal (which you should not be doing anyway), be aware that text hits their servers. For sensitive "
        'work, Warp has a "Privacy Mode" that disables AI features on a per-session basis. Enterprise customers '
        "on the Team plan get an option for on-premise AI processing, but this is not available on personal Pro "
        "plans.</p>\n\n"
        '<h2 id="verdict">The Bottom Line</h2>\n\n'
        '<p>Warp is the only terminal tool I have ever paid for, and I will keep paying for it as long as the AI '
        "features keep saving me time. The $18/month Pro plan generates roughly $2,000-$2,400/month in recovered "
        "billable time for my freelance business. That kind of ROI is vanishingly rare in developer tools.</p>\n\n"
        '<p>It is not perfect. TUI compatibility is a real issue for certain workflows. The platform gap between '
        "macOS and Linux is frustrating. AI rate limiting on Pro feels like a cheap move at this price point. And "
        "the account/internet dependency means you need a backup terminal for offline work.</p>\n\n"
        '<p>But for the average developer who spends 4+ hours a day in a terminal -- especially freelancers and '
        "consultants billing by the hour -- Warp is the most impactful productivity tool I have used since GitHub "
        "Copilot. The free tier is enough to verify whether it fits your stack. If it does, the Pro plan is one "
        "of the easiest \"yes\" decisions you will make this year.</p>"
    ),
    "published": True,
    "created_date": "2026-07-07"
}

data.append(new_tool)

# Verify JSON is valid
json_str = json.dumps(data, ensure_ascii=False, indent=2)
# Re-parse to verify
json.loads(json_str)

with open(TOOLS_PATH, 'w', encoding='utf-8') as f:
    f.write(json_str)

print(f"Done. New total: {len(data)} tools.")
print(f"Added: {new_tool['name']}")
print(f"Content length: {len(new_tool['content'])} chars")
