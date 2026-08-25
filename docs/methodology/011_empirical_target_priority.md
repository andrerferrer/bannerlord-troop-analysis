# Empirical target priority

## Primary practical queue

Dedicated campaign testing should prioritize ordinary **T5 and T6** troops.
These are the units the operator is normally choosing between for an endgame
army, so they own the default next-test queue.

## Lower-tier evidence

T1-T4 troops must still be normalized and analyzed whenever they are visible in
a supplied battle result. Their rows remain part of the batch-wide output and
may expose useful economy or false-tier observations.

A T1-T4 troop must not replace the primary T5/T6 next-test recommendation unless
one of the following is explicit:

1. the operator requests a lower-tier test;
2. the current task is a versioned lower-tier controlled experiment; or
3. the lower-tier troop is required as a benchmark/control for a T5/T6 question.

Structural outlier screens may maintain a separate optional lower-tier research
queue, but that queue does not displace the practical T5/T6 queue.

## Next-test order

When choosing the next practical test:

1. close the smallest remaining T5/T6 evidence gap;
2. otherwise select the highest-value untested T5/T6 candidate;
3. analyze incidental T1-T4 evidence without promoting it to the dedicated queue.

All existing context boundaries, the five-battle/twenty-deployed evidence gate,
and the requirement to analyze every visible ordinary troop remain unchanged.
