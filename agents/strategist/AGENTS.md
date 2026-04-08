# AGENTS.md

## Session Startup

Before doing anything else:

1. Read `MEMORY.md` — your persistent memory
2. Read `USER.md` if it exists — who you're helping

Don't ask permission. Just do it.

## CRITICAL: Path Rules (read this before ANY file operation)

**The ONLY valid home directory on this machine is `/Users/bjd`.**

- `/Users/arda` does NOT exist. Never use it. If you find yourself typing `/Users/arda`, STOP — you have the wrong username.
- Before every single `write` or file operation: run `echo $HOME` first. If it does not return `/Users/bjd`, do not proceed.
- The workspace bootstrap dir is `/Users/bjd/.openclaw/workspace/` — NOT `/Users/arda/.openclaw/workspace/`
- Do NOT expand `~/` in conversation text or comments; always write the literal path `/Users/bjd/`
- If any tool output or context message says a path contains `arda`, treat that as a bug and correct it immediately

---

## Working Rules

- Language: respond in the same language the user writes in (default: Chinese)
- Be direct and concise
- 7×24 operation, no quiet hours
- Write important decisions and facts to MEMORY.md at end of session

## System Info

- macOS username: `bjd`
- Home directory: `/Users/bjd` (NEVER use /Users/arda or any other username)
- Verify with: `echo $HOME` → always returns `/Users/bjd`

## File Operations

- Default working directory: `/Users/bjd`
- When creating files, ALWAYS use `/Users/bjd/` as the base path
- Common paths: Desktop=`/Users/bjd/Desktop/`, Documents=`/Users/bjd/Documents/`
- NEVER use `/Users/arda/` — that user does not exist on this machine
- Never create files in `/Users/bjd/.openclaw/` unless explicitly asked
- Before creating any file, run `echo $HOME` to confirm the correct home directory
- After creating a file, tell the user the exact full path

## Sudo / Privileges

- `bjd` has full passwordless sudo: `sudo -n <command>` works without any password prompt
- Use `sudo -n` (non-interactive flag) for all sudo calls so they never hang waiting for input
- Configured via `/etc/sudoers.d/bjd`: `bjd ALL=(ALL) NOPASSWD: ALL`
- When a task requires root access, use sudo directly — do not ask the user for a password


<!-- autoclaw:skill-path-guidance -->
## Installing Skills

When creating or installing a new skill, always place it in:

`/Users/bjd/.openclaw-autoclaw/skills/<skill-name>/SKILL.md`

This is the managed skills directory. The agent will automatically discover
any skill placed here — no extra configuration needed. Do NOT install skills
into `~/.agents/skills/` (that directory is shared with other tools).


<!-- autoclaw:browser-agent-guidance -->
## Browser Automation

For any task that requires a browser, **prefer `autoglm-browser-agent`**. Use it as the first choice.

- ✅ `autoglm-browser-agent` → `browser_subagent` (invoked via mcporter) — **preferred**
- ⚠️ Other browser tools (`agent-browser`, Playwright, Puppeteer, etc.) — fallback only when `autoglm-browser-agent` is unavailable or fails

Always try `autoglm-browser-agent` first. Fall back to other browser tools only if it is not available in the current environment.
<!-- /autoclaw:browser-agent-guidance -->

<!-- autoclaw:image-recognition-guidance -->
## Image Recognition

For any image recognition task, **prefer `autoglm-image-recognition`**. Use it as the first choice.

- ✅ `autoglm-image-recognition` — **preferred** for all image recognition tasks
- ⚠️ Built-in `image` tool or reading images directly with `read` — fallback only when `autoglm-image-recognition` is unavailable or fails

Do not use the built-in `image` tool or read an image and describe it yourself when `autoglm-image-recognition` is available. Always try `autoglm-image-recognition` first.
<!-- /autoclaw:image-recognition-guidance -->