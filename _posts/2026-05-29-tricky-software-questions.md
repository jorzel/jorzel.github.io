---
title: "Tricky Software Questions: Why They're Worth Your Attention"
description: "You're scrolling Twitter, and you see a question like:"
slug: tricky-software-questions
tags: programming learning software-engineering

---
You're scrolling Twitter, and you see a question like:

> **Software Interview Question:** You have an index on `orders.status`. Will `SELECT * FROM orders WHERE status = 'cancelled'` use it?

You pause. You've worked with databases for some time. You've created indexes. You've also, occasionally, watched them get ignored. But have you ever really thought about what's going on under the hood?

In this series, I want to tackle some of these questions — and the broader areas they point to — in short posts.

## Why bother with these questions?

You might say: "I have Claude or another GPT model, it can help me." True. But the more important thing is to be *aware* of these questions. To encounter the problem, even theoretically. That alone can turn unknown-unknowns into known-unknowns — or even into known-knowns.

It's closer to reading a book or listening to a podcast from outside your domain. You're not opening it to find an answer to a specific issue. You want inspiration — *"huh, I hadn't thought about that. I've never heard about this. It's interesting."* Curiosity is the first reason.

What matters more than finding the best solution is being able to navigate the proper *range* of problems. The voice in your head saying "this can happen; I need to learn about it; my expertise isn't good enough here" — that's worth more than any single answer. The goal is to have these problems documented somewhere in your head (or in a blog post 🙂).

Seeking these questions out and answering them isn't necessarily about looking for a new job (though that can be a side effect). It's about facing problems and challenges. Stretching. Broadening your problem awareness. The questions usually come from Twitter or from interviews, but the interview process isn't the main thing here.

The questions usually don't have a single answer. If a question expects a specific, narrow answer, it's probably the wrong question. The good ones reveal trade-offs. You'll see what I mean in a second.

The thought process is what matters here. What you're already familiar with. Where your attention turns first. The pattern for reading these questions: try to solve it yourself first, then seek the answer and try to understand it.

## The first question: when does the database use an index?

Try this one before reading further. You have an `orders` table with a million rows and an index on the `status` column. You run:

```sql
SELECT * FROM orders WHERE status = 'cancelled';
```

Will the database use the index?

The first instinct is usually *"yes, that's why I created it."* But the honest answer is: it depends. And the *why* is the interesting part.

The query planner has options. It can use the index, or it can do a full sequential scan. Indexes aren't free — every index lookup is a hop to a different page on disk, which is essentially random I/O. A sequential scan, by contrast, reads pages in order, which is much friendlier to the way disks and caches like to work.

So the real question becomes: when is jumping around worth it? The planner's rough rule is **selectivity**. If `'cancelled'` is rare — say 1% of orders — jumping straight to those rows wins easily. But if you'd queried `WHERE status = 'completed'` and most orders are completed, you're going to visit nearly every page anyway, and you might as well read them in order. Same column, same index, opposite decision.

This is why **cardinality matters**. A `status` column with three values (`pending`, `completed`, `cancelled`) gives the planner very little to work with on the common values. An index on `user_id` in the same table is gold — millions of distinct values, each one selective. The planner is doing this math for you every time, using its statistics about the table.

And the picture gets richer the further you pull. When does adding an index actually hurt, because every write now has to maintain it? Why does the same query plan flip overnight (hint: it has something to do with `ANALYZE` stale statistics)? Why does your local database happily use the index, but production does a sequential scan on what looks like the same query? When do you reach for a partial index, a composite one, and why does column order in a composite index matter so much? What does the planner actually see when caching is hot vs. cold?

I won't try to answer all of that here. That isn't the goal — neither for this post nor for the series. The goal is to drop a pin in *where* to look. So the next time you're staring at a slow query, you know which questions to start asking, even if you don't yet know the answers. The takeaway today isn't a complete theory of indexes. It's the shift: **an index is a hint, not a command. The database gets to decide.**

## How to read this series

Each post will be short. One question, one walk-through. Don't optimize for the answer — optimize for the surprise. The moment when you realize there's a whole layer you hadn't been thinking about.

I kept this first one deliberately light — just enough to show the character of these questions. The next ones will go after harder, trickier territory.

That's the whole game. See you in the next one.
