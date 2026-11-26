---
title: "Intelligence is Cheap. What's Expensive?"
description: "The growing tempo of AI and agentic coding is changing the software industry. Not threatening to change it, not promising to—actually changing it, right now."
slug: intelligence-is-cheap-whats-expensive
tags: programming ai agentic-coding software-engineering career

---
## The Drudgery is Gone

The growing tempo of AI and agentic coding is changing the software industry. Not threatening to change it, not promising to—actually changing it, right now.

Software engineers spend less time on manual coding activity, delegating more and more to AI agents. Something that used to need several people and weeks of experimenting can now be done within hours by a single person delivering a proof of concept. The entry level to test ideas is much lower. You can sketch an architecture, point an agent at it, and have a working prototype before lunch.

Some people claim that [software engineering is back](https://medium.com/@tobrien/stop-calling-it-vibe-coding-91b0daa726fb). We no longer need to care about syntax, frameworks, formatting. The drudgery that consumed most of our days—dependency hell, boilerplate, configuration—is handled. What's left, they argue, is the real engineering: thinking about architecture, trade-offs, design decisions.

It's an optimistic framing. But it raises a question that the optimists tend to skip over. If we keep getting rid of more and more aspects of software and delegate them to AI—what will remain of it?

## What Can Be Automated, Will Be Automated

We can already see the pattern: what can be automated eventually will be. The tempo of improvement leaves little doubt. The question worth asking is different: what can be automated, and what resists it?

Anything measurable. Anything with clear rules and fast feedback. If the input-output relationship is stable and the success criteria are unambiguous, a computer will eventually do it better than a human. This isn't speculation—it's the history of every industry that computers have touched.

This reminds me of the distinction between kind and wicked domains. Kind domains have stable patterns, clear rules, and tight feedback loops. Chess is kind. Assembly lines are kind. Wicked domains are the opposite—the rules shift, the feedback is delayed or ambiguous, and the same action can produce different outcomes depending on context.

AI thrives in kind domains. Automation there is almost inevitable, because computers are built for stable patterns. Code generation—translating a clear spec into syntax—is a kind problem. So is formatting, linting, boilerplate, dependency resolution. These are the parts of software engineering that are disappearing fastest, and they should.

Some people draw the line at creativity. Maybe. But creativity is usually great craft with a lot of trial and error—and trial and error is exactly what machines are good at.

The harder line is elsewhere—judgment and decisions. Not because they're mystical, but because they require valuing trade-offs where the values themselves are unclear. Assessing long-term effects that won't be visible for months or years. Weighing competing priorities that can't be reduced to a metric. These are wicked problems—the feedback loop is broken or deferred, and there's no objective function to optimize against.

Catalini, Hui, and Wu frame this precisely in [Some Simple Economics of AGI](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6298838): the cost to automate drops exponentially, but the cost to verify is biologically bottlenecked by human time and experience. The gap between what AI can execute and what humans can afford to verify keeps widening. Scale without verification is debt.

The more we automate everything else, the harder the remaining part—judgment—becomes.

## The Fragile Foundation of Judgment

Judgment relies on understanding. Understanding what we have, what is working and how, and why. Without that foundation, judgment is guesswork dressed up as decision-making.

And understanding is more fragile than we think. I see two forces that erode it—two kinds of cognitive debt that accumulate silently, especially now that we're moving faster than ever.

### Phantom Understanding

Even in human-to-human cooperation, misalignment is the default. You sit in a meeting, discuss a feature, nod along. Everyone seems to agree. Then implementation starts, and it turns out you were picturing different things. Your mental models of the problem were never the same—you just never collided them hard enough to notice.

This is the hardest thing to tackle, because it feels like alignment. When you have phantom understanding, your requirements become phantom too. The decisions you make aren't wrong in some obvious way—they're wrong in a way that only reveals itself later, when the cost of correction is high. Cognitive debt accumulates. It feels like progress, but it isn't. You're moving faster, but in the wrong direction.

Does the human-AI relationship change anything here? I think it makes it worse. An AI agent gives confident answers. You nod along—just like in that meeting. But how can you be sure its model of the problem matches yours, when you're not even sure what you want? The same phantom understanding, now with a collaborator that never pushes back, never says "I think we're picturing different things."

### Shallow Awareness

There's a second kind of debt, and it comes not from misalignment but from speed itself.

You delegate more. You ship faster. You cover more ground in a week than you used to in a month. But your capacity to be aware of what you've built doesn't scale with your output. You build more, understand less of what you built. Breadth increases, depth erodes.

You ask an agent to design a service. It delivers clean code, good tests, reasonable structure. You approve it and move on. Months later, the system struggles under growing traffic. You're asked why the architecture doesn't scale—and you don't have an answer. Not because the design was bad, but because you never understood the trade-offs behind it. The agent made choices. You accepted them. Now you own a system whose rationale lives nowhere except in a conversation you've long forgotten.

Simon Willison calls this [cognitive debt](https://simonwillison.net/2026/Feb/15/cognitive-debt/)—the gap between what your system does and what you understand about it. This is subtle because it doesn't feel like a problem at first. Everything works. The tests pass. The features ship. But your system thinking becomes shallow—you lose track of what is working, what was done, and what should be done next. In the long run, this backfires. You lose control over the thing you're supposedly driving.

### The Driver's Seat—For Now

Both of these debts operate under one assumption: that you are still the driver of change. That judgment, navigation, and verification are your job.

Right now, that assumption holds. The emerging role in software—call it a software orchestrator—is about exactly this: directing, supervising, setting quality criteria rather than typing code. You define what "done" looks like, break the problem into subtasks, review what the agent produces, and redirect when it drifts. Less typing, more steering. The central skill is easing misalignment. Between humans. Between humans and AI. Between intent and implementation.

What helps, practically? Make your mental models visible. Draw before you discuss. Write specs before you delegate. Review not just whether the code works, but whether you understand why it was built that way. And even when you delegate, remain the intentional source of changes—not just an accepter of working things. The goal isn't to slow down. It's to keep your understanding close to your output. The moment those two diverge, you're accumulating debt you can't see.

## Where Could This Go

The tempo of improvement doesn't let you rest on the assumption that humans stay in the driver's seat. AGI, superintelligence—these aren't science fiction anymore, they're research agendas with funding and timelines. What happens when AI gets consistently better than most humans at most decisions?

Catalini, Hui, and Wu describe two possible endpoints. In the "Hollow Economy," nominal output explodes but human agency decays—we produce more and understand less, drifting into a world where unverified systems accumulate hidden debt. In the "Augmented Economy," verification scales alongside agentic power, and the same forces that threaten collapse become the engine of discovery. The difference between the two isn't the technology. It's whether we scale our capacity for oversight as fast as we scale our capacity for execution.

If we drift toward the hollow end, the question stops being about software engineering. Why do you need human engineers if AI makes better architectural decisions? But then—why do you need human managers if AI allocates resources better? Why do you need human strategists if AI forecasts outcomes more accurately?

This isn't a software question anymore. It's a civilization question. What is the role of humans in a world where intelligence—including judgment—is no longer scarce?

I don't have a prediction. Just honesty: we don't know. And anyone who claims to know which way this goes hasn't sat long enough with the question.

What I do know is what's true today. Clear thinking is the bottleneck, not intelligence. AI didn't change what's hard about software. It revealed it.
