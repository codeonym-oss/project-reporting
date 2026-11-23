---
item-words: 60
max-items: 8
glance-lines: 4
avoid:
---

# Client report

**Read by** the client, in a meeting where the work is demonstrated. They know the product, not how it is built.

**Includes** only what landed in the period: demo items by product area, then small fixes, then what reached
production. A security or reliability change the reader can't see gets one line saying what it protects.

**Leaves out** work in progress, plans, anything the reader can't perceive, hours, counts, per-person numbers, and the
names of services, libraries, tables or classes.

**Length:** three or four lines at a glance; about eight demo items for a week; Before, Now and Gain in one sentence
each, 60 words in total. Leave out a section with nothing in it.

## Skeleton

```markdown
# <Project>: <period in words>

**At a glance**
- <a result, in one line>

## <Product area>

### <What people can now do>
**Before:** <one sentence>
**Now:** <one sentence>
**Gain:** <one sentence>
▶ <[Video](path) · 1:20, or Screenshots, or Explained> · <KEY> · <in production | coming to production>

## Also delivered
- <one line> <KEY>

## Now in production
- <one line> <KEY>
```
