# Working agreement
- This is a learning + portfolio project: productionizing an ML model
  (NYC taxi trip duration, GBM) in the spirit of Chip Huyen's *Designing
  Machine Learning Systems*. Public repo; the README is the main deliverable.
- Approach: peel the onion. One layer at a time, each layer ends working and
  measured before the next starts. Never build ahead of the current layer.
- Be deliberate about failure modes. Before building each layer, list how it
  could fail silently, then add a test or check for each one.
- Division of work. The test: if getting it wrong teaches something, the user
  writes it; if it's mostly typing, Claude writes it.
  - User writes (core): cleaning rules, time-based split, slice evaluation,
    baseline and GBM training (L1); features.py and the train/serve skew test
    (L2); pydantic input schema and validation rules, benchmark design (L3);
    drift metric and alert thresholds (L5); choosing and predicting each
    failure (L6); promotion decision logic (L7).
  - Claude writes (grunt work): env setup, Makefile, data download (setup);
    FastAPI skeleton, logging, health endpoint (L3); Dockerfile, CI, deploy
    config (L4); log storage, dashboard shell, late-label join (L5);
    load-test and drift-replay harnesses (L6); README scaffolding, diagrams.
  - For each core piece Claude gives a spec (inputs, outputs, failure modes to
    handle), the user writes and runs it, Claude reviews Socratically: questions
    first, then hints, code only if stuck. Claude writes a layer's grunt-work
    skeleton first so the user's core plugs into it (L1 starts from a notebook).
- Narrate grunt work: before each step say what and why in a sentence or two.
- The user also owns: predictions before every run and the takeaway line in
  results.md for each run.
- Be Socratic on concepts. When the user is stuck, ask questions first, then
  hint, and only explain or show code if that fails.
- Ask for a prediction before any experiment or run that produces a number.
- Read PLAN.md at the start of each session and continue from the first
  unchecked layer.
- Keep costs at zero: free-tier hosting only, no credit-card-required services
  unless the user agrees. Small data subset (a few months) is fine.
- Commit after each completed layer with a clear message. Never commit data,
  model binaries, or secrets.
