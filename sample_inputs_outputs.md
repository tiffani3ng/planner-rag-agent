# Anchor Sample Inputs and Outputs

This file shows representative inputs and outputs for **Anchor**, a grounded planning assistant that turns a user’s real documents into cited, actionable work plans.

The examples below are based on the current CLI MVP. They are intended to demonstrate the core behavior of the system: retrieve relevant deadlines, generate a feasible recommendation, cite source documents, and expose useful failure modes for future improvement.

---

## Example 1: Weekly Planning

### Sample Input

```text
What should I work on this week?
```

### Sample Output

```text
# Your Week at a Glance (Sep 28 – Oct 5)

You have one urgent item today and a Sprint 1 demo wrapping up the week. Here's how to tackle it:

Monday, Sep 28 (TODAY — urgent)
- Finish Lab 2: TDD — submit code + coverage report to GitHub by 11:59 PM tonight. Block off 2–3 hours this evening if not yet done. [software_dev_tasks.md]

Tuesday, Sep 29 – Wednesday, Sep 30
- Read Popper, Ch. 1 ("Science: Conjectures and Refutations") for Reading Response 2. Aim for a 1.5–2 hour focused reading block on Tuesday; due Oct 1. [philosophy_tasks.md]
- Take notes as you read — they'll feed directly into the response paper due Oct 6.

Thursday, Oct 1
- Submit the Popper reading. [philosophy_tasks.md]
- Begin Sprint 1 prep: start setting up the demo deployment through Render or GitHub Pages. [software_dev_tasks.md]

Friday, Oct 2 – Saturday, Oct 3
- Finish demo deployment by Oct 3. Test that the live link works end-to-end. [software_dev_tasks.md]

Sunday, Oct 4
- Demo rehearsal with team. Schedule a 1-hour team call to run through the 10-minute demo twice. [software_dev_tasks.md]

Monday, Oct 5
- Sprint 1 Demo day. Submit the retrospective document after the demo while details are fresh. [software_dev_tasks.md]

Priority Order
1. Lab 2 submission tonight. [software_dev_tasks.md]
2. Popper reading by Oct 1. [philosophy_tasks.md]
3. Demo deployment, rehearsal, and retrospective. [software_dev_tasks.md]

Knock out tonight's lab first — everything else has breathing room.
```

### What This Demonstrates

- Deadline-aware weekly planning
- Source-cited recommendations
- Priority ordering
- Concrete work blocks and next steps

---

## Example 2: Vacation Feasibility Check

### Sample Input

```text
Can I take a weeklong vacation starting today?
```

### Sample Output

```text
Probably not this week.

You have an urgent same-day deadline: Lab 2 is due tonight by 11:59 PM, so leaving today would create an immediate blocker. [software_dev_tasks.md]

You also have upcoming coursework and Sprint 1 preparation during the next several days, including the Popper reading due Oct 1 and demo deployment work due Oct 3. [philosophy_tasks.md] [software_dev_tasks.md]

Recommendation:
- Finish Lab 2 first.
- Complete the Popper reading before Oct 1.
- Finish the Sprint 1 deployment before Oct 3.
- Reassess after the Sprint 1 demo and retrospective are complete.
```

### What This Demonstrates

- Feasibility reasoning
- Blocker identification
- Deadline-based rejection of an unrealistic plan
- Grounded explanation instead of generic advice

---

## Example 3: Short Time-Block Planning

### Sample Input

```text
I have 3 hours free. What should I work on?
```

### Sample Output

```text
Use the 3-hour block for focused coursework and sprint preparation.

Suggested plan:
1. Spend 90 minutes on the highest-priority coding or software development task retrieved from your task list. [software_dev_tasks.md]
2. Spend 45 minutes reviewing upcoming philosophy reading notes or preparing for the response paper. [philosophy_tasks.md]
3. Use the final 30–45 minutes to update your task list, check what is due next, and identify anything blocked before the next work session.
```

### Evaluation Note

This query produced a useful time-block plan, but it also revealed a ranking weakness: the assistant surfaced a later Lab 4 item instead of the more urgent same-day Lab 2 task.

### What This Demonstrates

- Time-block generation
- Actionable planning from retrieved context
- A clear evaluation finding for future improvement
- Need for stronger urgency-aware reranking

---

## Summary of Sample Behaviors

| Input Type | Example Query | Expected Behavior |
|---|---|---|
| Weekly planning | `What should I work on this week?` | Retrieve upcoming deadlines and generate a prioritized weekly plan |
| Feasibility check | `Can I take a weeklong vacation starting today?` | Identify blockers and explain whether the plan is realistic |
| Time-block planning | `I have 3 hours free. What should I work on?` | Recommend a focused work block based on retrieved tasks |

---

## Current Evaluation Takeaways

- Anchor retrieves deadline-specific chunks from task documents.
- Generated answers include source citations.
- Weekly planning and feasibility reasoning are promising.
- Retrieval is fast enough for interactive use.
- Generation latency remains above the intended target.
- Open-ended time-window queries need stronger urgency and deadline weighting.

---

## Future Improvement Targets

The next version should improve:

- urgency-aware reranking,
- task completion state tracking,
- calendar-aware scheduling,
- live document or calendar updates,
- and evaluation against expected retrieved sources.
