PostgreSQL: Documentation: 18: Chapter 14. Performance Tips

























November 13, 2025: [PostgreSQL 18.1, 17.7, 16.11, 15.15, 14.20, and 13.23 Released!](/about/news/postgresql-181-177-1611-1515-1420-and-1323-released-3171/)











[Documentation](/docs/ "Documentation") → [PostgreSQL 18](/docs/18/index.html)





 Supported Versions:
 
 
 
 [Current](/docs/current/performance-tips.html "PostgreSQL 18 - Chapter 14. Performance Tips")
 ([18](/docs/18/performance-tips.html "PostgreSQL 18 - Chapter 14. Performance Tips"))
 
 
 / 
 
 [17](/docs/17/performance-tips.html "PostgreSQL 17 - Chapter 14. Performance Tips")
 
 
 / 
 
 [16](/docs/16/performance-tips.html "PostgreSQL 16 - Chapter 14. Performance Tips")
 
 
 / 
 
 [15](/docs/15/performance-tips.html "PostgreSQL 15 - Chapter 14. Performance Tips")
 
 
 / 
 
 [14](/docs/14/performance-tips.html "PostgreSQL 14 - Chapter 14. Performance Tips")




 Development Versions:
 
 
 [devel](/docs/devel/performance-tips.html "PostgreSQL devel - Chapter 14. Performance Tips")




 Unsupported versions:
 
 
 [13](/docs/13/performance-tips.html "PostgreSQL 13 - Chapter 14. Performance Tips")
 
 / 
 [12](/docs/12/performance-tips.html "PostgreSQL 12 - Chapter 14. Performance Tips")
 
 / 
 [11](/docs/11/performance-tips.html "PostgreSQL 11 - Chapter 14. Performance Tips")
 
 / 
 [10](/docs/10/performance-tips.html "PostgreSQL 10 - Chapter 14. Performance Tips")
 
 / 
 [9.6](/docs/9.6/performance-tips.html "PostgreSQL 9.6 - Chapter 14. Performance Tips")
 
 / 
 [9.5](/docs/9.5/performance-tips.html "PostgreSQL 9.5 - Chapter 14. Performance Tips")
 
 / 
 [9.4](/docs/9.4/performance-tips.html "PostgreSQL 9.4 - Chapter 14. Performance Tips")
 
 / 
 [9.3](/docs/9.3/performance-tips.html "PostgreSQL 9.3 - Chapter 14. Performance Tips")
 
 / 
 [9.2](/docs/9.2/performance-tips.html "PostgreSQL 9.2 - Chapter 14. Performance Tips")
 
 / 
 [9.1](/docs/9.1/performance-tips.html "PostgreSQL 9.1 - Chapter 14. Performance Tips")
 
 / 
 [9.0](/docs/9.0/performance-tips.html "PostgreSQL 9.0 - Chapter 14. Performance Tips")
 
 / 
 [8.4](/docs/8.4/performance-tips.html "PostgreSQL 8.4 - Chapter 14. Performance Tips")
 
 / 
 [8.3](/docs/8.3/performance-tips.html "PostgreSQL 8.3 - Chapter 14. Performance Tips")
 
 / 
 [8.2](/docs/8.2/performance-tips.html "PostgreSQL 8.2 - Chapter 14. Performance Tips")
 
 / 
 [8.1](/docs/8.1/performance-tips.html "PostgreSQL 8.1 - Chapter 14. Performance Tips")
 
 / 
 [8.0](/docs/8.0/performance-tips.html "PostgreSQL 8.0 - Chapter 14. Performance Tips")
 
 / 
 [7.4](/docs/7.4/performance-tips.html "PostgreSQL 7.4 - Chapter 14. Performance Tips")
 
 / 
 [7.3](/docs/7.3/performance-tips.html "PostgreSQL 7.3 - Chapter 14. Performance Tips")
 
 / 
 [7.2](/docs/7.2/performance-tips.html "PostgreSQL 7.2 - Chapter 14. Performance Tips")
 
 / 
 [7.1](/docs/7.1/performance-tips.html "PostgreSQL 7.1 - Chapter 14. Performance Tips")



















| Chapter 14. Performance Tips |
| --- |
| [Prev](locking-indexes.html "13.7. Locking and Indexes") | [Up](sql.html "Part II. The SQL Language") | Part II. The SQL Language | [Home](index.html "PostgreSQL 18.1 Documentation") | [Next](using-explain.html "14.1. Using EXPLAIN") |




---







## Chapter 14. Performance Tips






**Table of Contents**



[14.1. Using `EXPLAIN`](using-explain.html)


[14.1.1. `EXPLAIN` Basics](using-explain.html#USING-EXPLAIN-BASICS)
[14.1.2. `EXPLAIN ANALYZE`](using-explain.html#USING-EXPLAIN-ANALYZE)
[14.1.3. Caveats](using-explain.html#USING-EXPLAIN-CAVEATS)


[14.2. Statistics Used by the Planner](planner-stats.html)


[14.2.1. Single-Column Statistics](planner-stats.html#PLANNER-STATS-SINGLE-COLUMN)
[14.2.2. Extended Statistics](planner-stats.html#PLANNER-STATS-EXTENDED)


[14.3. Controlling the Planner with Explicit `JOIN` Clauses](explicit-joins.html)
[14.4. Populating a Database](populate.html)


[14.4.1. Disable Autocommit](populate.html#DISABLE-AUTOCOMMIT)
[14.4.2. Use `COPY`](populate.html#POPULATE-COPY-FROM)
[14.4.3. Remove Indexes](populate.html#POPULATE-RM-INDEXES)
[14.4.4. Remove Foreign Key Constraints](populate.html#POPULATE-RM-FKEYS)
[14.4.5. Increase `maintenance_work_mem`](populate.html#POPULATE-WORK-MEM)
[14.4.6. Increase `max_wal_size`](populate.html#POPULATE-MAX-WAL-SIZE)
[14.4.7. Disable WAL Archival and Streaming Replication](populate.html#POPULATE-PITR)
[14.4.8. Run `ANALYZE` Afterwards](populate.html#POPULATE-ANALYZE)
[14.4.9. Some Notes about pg\_dump](populate.html#POPULATE-PG-DUMP)


[14.5. Non-Durable Settings](non-durability.html)


Query performance can be affected by many things. Some of these can be controlled by the user, while others are fundamental to the underlying design of the system. This chapter provides some hints about understanding and tuning PostgreSQL performance.






---




|  |  |  |
| --- | --- | --- |
| [Prev](locking-indexes.html "13.7. Locking and Indexes") | [Up](sql.html "Part II. The SQL Language") | [Next](using-explain.html "14.1. Using EXPLAIN") |
| 13.7. Locking and Indexes  | [Home](index.html "PostgreSQL 18.1 Documentation") |  14.1. Using `EXPLAIN` |





## Submit correction



 If you see anything in the documentation that is not correct, does not match
 your experience with the particular feature or requires further clarification,
 please use
 [this form](/account/comments/new/18/performance-tips.html/)
 to report a documentation issue.