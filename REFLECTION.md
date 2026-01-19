\# Reflection



\## Approach

I approached this task by building a static code analysis tool for ERPNext.

Instead of running the Frappe framework, I focused on reading Python source code

directly and extracting structural information using the Python AST module.



I started with entity extraction (classes and functions), then incrementally

added relationship detection, business rule signals, and data access detection.



\## New Concepts Learned

\- Static analysis using Python AST

\- Understanding large legacy codebases without running them

\- Identifying business rules through validation and conditional patterns

\- Generating call graphs and dependency diagrams using Mermaid



\## Challenges Faced

\- The ERPNext codebase is very large and tightly coupled to the framework

\- Understanding analyzer output required mapping raw JSON data to real concepts

\- Large diagrams became unreadable, so I learned to limit scope intentionally



\## What I Would Do With More Time

\- Improve filtering to reduce noise in relationship graphs

\- Add human-readable summaries for detected business rules

\- Group related functions by domain responsibility



\## Open Questions

\- How to best combine static analysis with runtime tracing

\- How to map extracted rules to domain documentation



