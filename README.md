# Merged question bank

This folder combines the four supplied archives using the requested topic assignments.
The existing JSON schema, topic folders, relative image paths, and all tests are preserved.
Question and asset files are exact copies from the assigned archive.

- Akshat: graphs.
- Sanchit: greedy.
- Vaishnav: advanced-data-structures, arrays, binary-search, bit-manipulation, design,
  divide-and-conquer, dynamic-programming, hashing, heaps.
- Rishi: two-pointers, tries, trees, strings, stacks-queues, sorting, sliding-window,
  simulation, recursion-backtracking, prefix-sum, miscellaneous, mathematics, linked-lists.
- Database: retained from Rishi; these questions are identical across all four sources.

Browse `questions/dsa/<topic>/` and `questions/database/<topic>/`.
Each topic's `assets/` folder contains its original diagrams and images.

See `reports/merge-report.md` for topic totals and verification results,
`reports/topic-summary.csv` for a spreadsheet-friendly summary, and
`manifests/merge-provenance.json` for the source and SHA-256 of every copied question/asset.
`manifests/questions-index.json` indexes the merged question bank.

The original tooling and schema are retained. See `README.source.md` for the original
repository documentation. Historical collection timestamps remain source timestamps.

Run `python scripts/verify_merge.py` to recheck file integrity without extra dependencies.
If Node dependencies are installed, the original `npm run validate` and `npm test`
commands are also available. No dependencies or Git history are bundled here.

Validation checks preservation and data structure; it does not independently execute
every supplied test or prove every expected answer correct.
