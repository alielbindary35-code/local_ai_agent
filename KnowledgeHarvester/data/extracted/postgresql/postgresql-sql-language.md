PostgreSQL: Documentation: 18: Part II. The SQL Language

























November 13, 2025: [PostgreSQL 18.1, 17.7, 16.11, 15.15, 14.20, and 13.23 Released!](/about/news/postgresql-181-177-1611-1515-1420-and-1323-released-3171/)











[Documentation](/docs/ "Documentation") → [PostgreSQL 18](/docs/18/index.html)





 Supported Versions:
 
 
 
 [Current](/docs/current/sql.html "PostgreSQL 18 - Part II. The SQL Language")
 ([18](/docs/18/sql.html "PostgreSQL 18 - Part II. The SQL Language"))
 
 
 / 
 
 [17](/docs/17/sql.html "PostgreSQL 17 - Part II. The SQL Language")
 
 
 / 
 
 [16](/docs/16/sql.html "PostgreSQL 16 - Part II. The SQL Language")
 
 
 / 
 
 [15](/docs/15/sql.html "PostgreSQL 15 - Part II. The SQL Language")
 
 
 / 
 
 [14](/docs/14/sql.html "PostgreSQL 14 - Part II. The SQL Language")




 Development Versions:
 
 
 [devel](/docs/devel/sql.html "PostgreSQL devel - Part II. The SQL Language")




 Unsupported versions:
 
 
 [13](/docs/13/sql.html "PostgreSQL 13 - Part II. The SQL Language")
 
 / 
 [12](/docs/12/sql.html "PostgreSQL 12 - Part II. The SQL Language")
 
 / 
 [11](/docs/11/sql.html "PostgreSQL 11 - Part II. The SQL Language")
 
 / 
 [10](/docs/10/sql.html "PostgreSQL 10 - Part II. The SQL Language")
 
 / 
 [9.6](/docs/9.6/sql.html "PostgreSQL 9.6 - Part II. The SQL Language")
 
 / 
 [9.5](/docs/9.5/sql.html "PostgreSQL 9.5 - Part II. The SQL Language")
 
 / 
 [9.4](/docs/9.4/sql.html "PostgreSQL 9.4 - Part II. The SQL Language")
 
 / 
 [9.3](/docs/9.3/sql.html "PostgreSQL 9.3 - Part II. The SQL Language")
 
 / 
 [9.2](/docs/9.2/sql.html "PostgreSQL 9.2 - Part II. The SQL Language")
 
 / 
 [9.1](/docs/9.1/sql.html "PostgreSQL 9.1 - Part II. The SQL Language")
 
 / 
 [9.0](/docs/9.0/sql.html "PostgreSQL 9.0 - Part II. The SQL Language")
 
 / 
 [8.4](/docs/8.4/sql.html "PostgreSQL 8.4 - Part II. The SQL Language")
 
 / 
 [8.3](/docs/8.3/sql.html "PostgreSQL 8.3 - Part II. The SQL Language")
 
 / 
 [8.2](/docs/8.2/sql.html "PostgreSQL 8.2 - Part II. The SQL Language")
 
 / 
 [8.1](/docs/8.1/sql.html "PostgreSQL 8.1 - Part II. The SQL Language")
 
 / 
 [8.0](/docs/8.0/sql.html "PostgreSQL 8.0 - Part II. The SQL Language")
 
 / 
 [7.4](/docs/7.4/sql.html "PostgreSQL 7.4 - Part II. The SQL Language")
 
 / 
 [7.1](/docs/7.1/sql.html "PostgreSQL 7.1 - Part II. The SQL Language")



















| Part II. The SQL Language |
| --- |
| [Prev](tutorial-conclusion.html "3.7. Conclusion") | [Up](index.html "PostgreSQL 18.1 Documentation") | PostgreSQL 18.1 Documentation | [Home](index.html "PostgreSQL 18.1 Documentation") | [Next](sql-syntax.html "Chapter 4. SQL Syntax") |




---







# Part II. The SQL Language






This part describes the use of the SQL language in PostgreSQL. We start with describing the general syntax of SQL, then how to create tables, how to populate the database, and how to query it. The middle part lists the available data types and functions for use in SQL commands. Lastly, we address several aspects of importance for tuning a database.


The information is arranged so that a novice user can follow it from start to end and gain a full understanding of the topics without having to refer forward too many times. The chapters are intended to be self-contained, so that advanced users can read the chapters individually as they choose. The information is presented in narrative form with topical units. Readers looking for a complete description of a particular command are encouraged to review the [Part VI](reference.html "Part VI. Reference").


Readers should know how to connect to a PostgreSQL database and issue SQL commands. Readers that are unfamiliar with these issues are encouraged to read [Part I](tutorial.html "Part I. Tutorial") first. SQL commands are typically entered using the PostgreSQL interactive terminal psql, but other programs that have similar functionality can be used as well.



**Table of Contents**



[4. SQL Syntax](sql-syntax.html)


[4.1. Lexical Structure](sql-syntax-lexical.html)
[4.2. Value Expressions](sql-expressions.html)
[4.3. Calling Functions](sql-syntax-calling-funcs.html)


[5. Data Definition](ddl.html)


[5.1. Table Basics](ddl-basics.html)
[5.2. Default Values](ddl-default.html)
[5.3. Identity Columns](ddl-identity-columns.html)
[5.4. Generated Columns](ddl-generated-columns.html)
[5.5. Constraints](ddl-constraints.html)
[5.6. System Columns](ddl-system-columns.html)
[5.7. Modifying Tables](ddl-alter.html)
[5.8. Privileges](ddl-priv.html)
[5.9. Row Security Policies](ddl-rowsecurity.html)
[5.10. Schemas](ddl-schemas.html)
[5.11. Inheritance](ddl-inherit.html)
[5.12. Table Partitioning](ddl-partitioning.html)
[5.13. Foreign Data](ddl-foreign-data.html)
[5.14. Other Database Objects](ddl-others.html)
[5.15. Dependency Tracking](ddl-depend.html)


[6. Data Manipulation](dml.html)


[6.1. Inserting Data](dml-insert.html)
[6.2. Updating Data](dml-update.html)
[6.3. Deleting Data](dml-delete.html)
[6.4. Returning Data from Modified Rows](dml-returning.html)


[7. Queries](queries.html)


[7.1. Overview](queries-overview.html)
[7.2. Table Expressions](queries-table-expressions.html)
[7.3. Select Lists](queries-select-lists.html)
[7.4. Combining Queries (`UNION`, `INTERSECT`, `EXCEPT`)](queries-union.html)
[7.5. Sorting Rows (`ORDER BY`)](queries-order.html)
[7.6. `LIMIT` and `OFFSET`](queries-limit.html)
[7.7. `VALUES` Lists](queries-values.html)
[7.8. `WITH` Queries (Common Table Expressions)](queries-with.html)


[8. Data Types](datatype.html)


[8.1. Numeric Types](datatype-numeric.html)
[8.2. Monetary Types](datatype-money.html)
[8.3. Character Types](datatype-character.html)
[8.4. Binary Data Types](datatype-binary.html)
[8.5. Date/Time Types](datatype-datetime.html)
[8.6. Boolean Type](datatype-boolean.html)
[8.7. Enumerated Types](datatype-enum.html)
[8.8. Geometric Types](datatype-geometric.html)
[8.9. Network Address Types](datatype-net-types.html)
[8.10. Bit String Types](datatype-bit.html)
[8.11. Text Search Types](datatype-textsearch.html)
[8.12. UUID Type](datatype-uuid.html)
[8.13. XML Type](datatype-xml.html)
[8.14. JSON Types](datatype-json.html)
[8.15. Arrays](arrays.html)
[8.16. Composite Types](rowtypes.html)
[8.17. Range Types](rangetypes.html)
[8.18. Domain Types](domains.html)
[8.19. Object Identifier Types](datatype-oid.html)
[8.20. `pg_lsn` Type](datatype-pg-lsn.html)
[8.21. Pseudo-Types](datatype-pseudo.html)


[9. Functions and Operators](functions.html)


[9.1. Logical Operators](functions-logical.html)
[9.2. Comparison Functions and Operators](functions-comparison.html)
[9.3. Mathematical Functions and Operators](functions-math.html)
[9.4. String Functions and Operators](functions-string.html)
[9.5. Binary String Functions and Operators](functions-binarystring.html)
[9.6. Bit String Functions and Operators](functions-bitstring.html)
[9.7. Pattern Matching](functions-matching.html)
[9.8. Data Type Formatting Functions](functions-formatting.html)
[9.9. Date/Time Functions and Operators](functions-datetime.html)
[9.10. Enum Support Functions](functions-enum.html)
[9.11. Geometric Functions and Operators](functions-geometry.html)
[9.12. Network Address Functions and Operators](functions-net.html)
[9.13. Text Search Functions and Operators](functions-textsearch.html)
[9.14. UUID Functions](functions-uuid.html)
[9.15. XML Functions](functions-xml.html)
[9.16. JSON Functions and Operators](functions-json.html)
[9.17. Sequence Manipulation Functions](functions-sequence.html)
[9.18. Conditional Expressions](functions-conditional.html)
[9.19. Array Functions and Operators](functions-array.html)
[9.20. Range/Multirange Functions and Operators](functions-range.html)
[9.21. Aggregate Functions](functions-aggregate.html)
[9.22. Window Functions](functions-window.html)
[9.23. Merge Support Functions](functions-merge-support.html)
[9.24. Subquery Expressions](functions-subquery.html)
[9.25. Row and Array Comparisons](functions-comparisons.html)
[9.26. Set Returning Functions](functions-srf.html)
[9.27. System Information Functions and Operators](functions-info.html)
[9.28. System Administration Functions](functions-admin.html)
[9.29. Trigger Functions](functions-trigger.html)
[9.30. Event Trigger Functions](functions-event-triggers.html)
[9.31. Statistics Information Functions](functions-statistics.html)


[10. Type Conversion](typeconv.html)


[10.1. Overview](typeconv-overview.html)
[10.2. Operators](typeconv-oper.html)
[10.3. Functions](typeconv-func.html)
[10.4. Value Storage](typeconv-query.html)
[10.5. `UNION`, `CASE`, and Related Constructs](typeconv-union-case.html)
[10.6. `SELECT` Output Columns](typeconv-select.html)


[11. Indexes](indexes.html)


[11.1. Introduction](indexes-intro.html)
[11.2. Index Types](indexes-types.html)
[11.3. Multicolumn Indexes](indexes-multicolumn.html)
[11.4. Indexes and `ORDER BY`](indexes-ordering.html)
[11.5. Combining Multiple Indexes](indexes-bitmap-scans.html)
[11.6. Unique Indexes](indexes-unique.html)
[11.7. Indexes on Expressions](indexes-expressional.html)
[11.8. Partial Indexes](indexes-partial.html)
[11.9. Index-Only Scans and Covering Indexes](indexes-index-only-scans.html)
[11.10. Operator Classes and Operator Families](indexes-opclass.html)
[11.11. Indexes and Collations](indexes-collations.html)
[11.12. Examining Index Usage](indexes-examine.html)


[12. Full Text Search](textsearch.html)


[12.1. Introduction](textsearch-intro.html)
[12.2. Tables and Indexes](textsearch-tables.html)
[12.3. Controlling Text Search](textsearch-controls.html)
[12.4. Additional Features](textsearch-features.html)
[12.5. Parsers](textsearch-parsers.html)
[12.6. Dictionaries](textsearch-dictionaries.html)
[12.7. Configuration Example](textsearch-configuration.html)
[12.8. Testing and Debugging Text Search](textsearch-debugging.html)
[12.9. Preferred Index Types for Text Search](textsearch-indexes.html)
[12.10. psql Support](textsearch-psql.html)
[12.11. Limitations](textsearch-limitations.html)


[13. Concurrency Control](mvcc.html)


[13.1. Introduction](mvcc-intro.html)
[13.2. Transaction Isolation](transaction-iso.html)
[13.3. Explicit Locking](explicit-locking.html)
[13.4. Data Consistency Checks at the Application Level](applevel-consistency.html)
[13.5. Serialization Failure Handling](mvcc-serialization-failure-handling.html)
[13.6. Caveats](mvcc-caveats.html)
[13.7. Locking and Indexes](locking-indexes.html)


[14. Performance Tips](performance-tips.html)


[14.1. Using `EXPLAIN`](using-explain.html)
[14.2. Statistics Used by the Planner](planner-stats.html)
[14.3. Controlling the Planner with Explicit `JOIN` Clauses](explicit-joins.html)
[14.4. Populating a Database](populate.html)
[14.5. Non-Durable Settings](non-durability.html)


[15. Parallel Query](parallel-query.html)


[15.1. How Parallel Query Works](how-parallel-query-works.html)
[15.2. When Can Parallel Query Be Used?](when-can-parallel-query-be-used.html)
[15.3. Parallel Plans](parallel-plans.html)
[15.4. Parallel Safety](parallel-safety.html)









---




|  |  |  |
| --- | --- | --- |
| [Prev](tutorial-conclusion.html "3.7. Conclusion") | [Up](index.html "PostgreSQL 18.1 Documentation") | [Next](sql-syntax.html "Chapter 4. SQL Syntax") |
| 3.7. Conclusion  | [Home](index.html "PostgreSQL 18.1 Documentation") |  Chapter 4. SQL Syntax |





## Submit correction



 If you see anything in the documentation that is not correct, does not match
 your experience with the particular feature or requires further clarification,
 please use
 [this form](/account/comments/new/18/sql.html/)
 to report a documentation issue.