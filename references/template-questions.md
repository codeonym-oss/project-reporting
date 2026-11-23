# Making a template

Used by `init` for the default format, and by `report` when a format doesn't exist yet. Start from
`<plugin>/templates/client.md`. Ask one question at a time, each with your recommendation, and skip what the person
already said:

1. **Who reads it,** and what do they do with it (a demo meeting, a decision, a record)?
2. **What does it include,** and what must never be in it? By default, only work that landed, with no hours, counts
   or per-person numbers.
3. **How is it grouped:** by product area, by person, by epic?
4. **What does an entry look like?** By default, Before / Now / Gain and a demo.
5. **How long may it be:** the number of demo items, words per item, lines at a glance?
6. **Words to avoid:** names only the team knows.

Write the answers into the template in plain words, with its skeleton, and show it. Its header is what `check`
enforces; leave a limit out to have none:

```markdown
---
item-words: 60
max-items: 8
glance-lines: 4
avoid: broker, replica
---
```
