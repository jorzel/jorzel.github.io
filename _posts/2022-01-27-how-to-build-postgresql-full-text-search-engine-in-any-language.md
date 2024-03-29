---
title: How to build PostgreSQL full text search engine in any language
description: In this short post I will show step by step how to establish full text search engine in PostgreSQL. Several options like `ilike`, trigrams search and tsearch will be presented.
tags: postgresql full-text-search database
---

PostgreSQL is a widely-used, open source object-relational database system. However, it is not limited only to relational applications. Thanks to [JSONB](https://www.postgresql.org/docs/13/datatype-json.html) feature it can be a document store, [hstore](https://www.postgresql.org/docs/current/hstore.html) extension allows to use PostgreSQL as a key-value store. So this database system is extremely versatile. It could be used also as a search engine. In this short post I will show step by step how to establish full text search in PostgreSQL. Several options like: `ilike`, trigrams search and `tsearch` will be presented.

## Setup
The first step is the creation of a database instance. All database commands will be executed inside `psql` terminal.
```sql
>> CREATE DATABASE ftdb;
```
To create a table and feed it with an example dataset (100k rows, 15 English words each) I have written a python script (link to Github repo, which you find at the end of this story). However, you can do it with native SQL as well.

## Full-text search using simple `ilike`
At the very beginning, I start with `ilike` operator. This option is easy and straightforward.  However, you may not be satisfied with query performance when your database is getting large.
```sql
>> EXPLAIN ANALYZE
   SELECT text, language
   FROM public.document
   WHERE
      text ilike '%field%'
      AND text ilike '%window%'
      AND text ilike '%lamp%'
      AND text ilike '%research%'
      AND language = 'en'
    LIMIT 1;
                                                                  QUERY PLAN
----------------------------------------------------------------------------------------------------------------------------------------------
 Limit  (cost=0.00..3734.02 rows=1 width=105) (actual time=87.473..87.474 rows=0 loops=1)
   ->  Seq Scan on document  (cost=0.00..3734.02 rows=1 width=105) (actual time=87.466..87.466 rows=0 loops=1)
         Filter: ((text ~~* '%field%'::text) AND (text ~~* '%window%'::text) AND (text ~~* '%lamp%'::text) AND (text ~~* '%research%'::text))
         Rows Removed by Filter: 100001
 Planning Time: 2.193 ms
 Execution Time: 87.500 ms
 ```

## Full-text search using `ilike` supported by trigram index
However, we can improve `ilike` performance using trigram search. What is a trigram search? Citing [wikipedia](https://en.wikipedia.org/wiki/Trigram_search): *It finds objects which match the maximum number of three-character strings in the entered search terms*. See the trigram example:
```sql
>> CREATE EXTENSION pg_trgm;
CREATE EXTENSION
>> select show_trgm('fielded');
                show_trgm
-----------------------------------------
 {"  f"," fi",ded,"ed ",eld,fie,iel,lde}
```
Creating a trigram index can speed up `ilike` query.
```sql
>> CREATE INDEX  ix_document_text_trigram ON document USING gin (text gin_trgm_ops) where language = 'en';
CREATE INDEX

>> EXPLAIN ANALYZE
   SELECT text, language
   FROM public.document
   WHERE
      text ilike '%field%'
      AND text ilike '%window%'
      AND text ilike '%lamp%'
      AND text ilike '%research%'
      AND language = 'en'
    LIMIT 1;
                                                                                       QUERY PLAN
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 Limit  (cost=176.00..180.02 rows=1 width=105) (actual time=1.473..1.474 rows=0 loops=1)
   ->  Bitmap Heap Scan on document  (cost=176.00..180.02 rows=1 width=105) (actual time=1.470..1.471 rows=0 loops=1)
         Recheck Cond: ((text ~~* '%field%'::text) AND (text ~~* '%window%'::text) AND (text ~~* '%lamp%'::text) AND (text ~~* '%research%'::text) AND ((language)::text = 'en'::text))
         ->  Bitmap Index Scan on ix_document_text_trigram  (cost=0.00..176.00 rows=1 width=0) (actual time=1.466..1.466 rows=0 loops=1)
               Index Cond: ((text ~~* '%field%'::text) AND (text ~~* '%window%'::text) AND (text ~~* '%lamp%'::text) AND (text ~~* '%research%'::text))
 Planning Time: 2.389 ms
 Execution Time: 1.524 ms
```
`ilike` with trigrams can be enough solution for many projects. However, this approach is generic and does not exploit the morphological distinction of a language. So, when you would like to perform a search based on canonical forms of words, you should choose tsearch engine.


## Create non-default language configuration for tsearch full-text search
Postgres tsearch does not provide support for many languages by default. However, you can set up the configuration quite easily. You just need additional dictionary files. Here is an example for the polish language. Polish dictionary files can be downloaded from: https://github.com/judehunter/polish-tsearch.
polish.affix, polish.stop and polish.dict files should be copied to PostgreSQL sharedir `tsearch_data` location,
e.g. `/usr/share/postgresql/13/tsearch_data`. To determine your sharedir location you can use `pg_config --sharedir`.

There also must be created a configuration (see [docs](https://www.postgresql.org/docs/current/textsearch-dictionaries.html)) inside database:
```sql
>> DROP TEXT SEARCH DICTIONARY IF EXISTS polish_hunspell CASCADE;
   CREATE TEXT SEARCH DICTIONARY polish_hunspell (
    TEMPLATE  = ispell,
    DictFile  = polish,
    AffFile   = polish,
    StopWords = polish
  );
  CREATE TEXT SEARCH CONFIGURATION public.polish (
    COPY = pg_catalog.english
  );
  ALTER TEXT SEARCH CONFIGURATION polish
    ALTER MAPPING
    FOR
        asciiword, asciihword, hword_asciipart,  word, hword, hword_part
    WITH
        polish_hunspell, simple;

```
You need these files and configuration because full-text search engine uses lexeme comparing to find the best matches (both query pattern and stored text are lexemized):
```sql
>> SELECT to_tsquery('english', 'fielded'), to_tsvector('english', text)
   FROM document
   LIMIT 1;
 to_tsquery |                                                                    to_tsvector
------------+----------------------------------------------------------------------------------------------------------------------------------------------------
 'field'    | '19':16 'bat':12 'dead':8 'degre':1 'depth':5 'field':15 'lamp':13 'men':6 'put':14 'ranch':2 'tall':4 'time':3 'underlin':11 'wast':10 'window':9
```
If you cannot provide dictionary files you can still use full-text search in "simple" form (without transformation to lexeme):

```sql
>> SELECT to_tsquery('simple', 'fielded'), to_tsvector('simple', text)
   FROM document
   LIMIT 1;
 to_tsquery |                                                                             to_tsvector
------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------
 'fielded'  | '19':16 'bat':12 'below':7 'dead':8 'degree':1 'depth':5 'field':15 'lamp':13 'men':6 'putting':14 'ranch':2 'tall':4 'time':3 'underline':11 'waste':10 'window':9
```

## Tsearch full-text search without the stored index
At first glance, the performance of tsearch query is really poor... 
```sql
>> EXPLAIN ANALYZE
   SELECT text, language
   FROM public.document
   WHERE to_tsvector('english', text) @@ to_tsquery('english', 'fielded & window & lamp & depth & test ')
   LIMIT 1;
                                                                                  QUERY PLAN
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 Limit  (cost=1000.00..18298.49 rows=1 width=103) (actual time=489.802..491.352 rows=0 loops=1)
   ->  Gather  (cost=1000.00..18298.49 rows=1 width=103) (actual time=489.800..491.349 rows=0 loops=1)
         Workers Planned: 1
         Workers Launched: 1
         ->  Parallel Seq Scan on document  (cost=0.00..17298.39 rows=1 width=103) (actual time=486.644..486.644 rows=0 loops=2)
               Filter: (((language)::text = 'en'::text) AND (to_tsvector('english'::regconfig, text) @@ '''field'' & ''window'' & ''lamp'' & ''depth'' & ''test'''::tsquery))
               Rows Removed by Filter: 50000
 Planning Time: 0.272 ms
 Execution Time: 491.376 ms
```
However, our data have not been indexed yet...

## Tsearch full-text search with stored partial index
A partial index gives a possibility to store records in different languages using the same database table and query them effectively.
```sql
>> CREATE INDEX ix_en_document_tsvector_text ON public.document USING gin (to_tsvector('english'::regconfig, text)) WHERE language = 'en';
CREATED INDEX
>> EXPLAIN ANALYZE
   SELECT text, language
   FROM public.document
   WHERE to_tsvector('english', text) @@ to_tsquery('english', 'fielded & window & lamp & depth & test ')
   LIMIT 1;
                                                               QUERY PLAN
----------------------------------------------------------------------------------------------------------------------------------------
 Limit  (cost=1000.00..18151.43 rows=1 width=103) (actual time=487.120..488.569 rows=0 loops=1)
   ->  Gather  (cost=1000.00..18151.43 rows=1 width=103) (actual time=487.117..488.567 rows=0 loops=1)
         Workers Planned: 1
         Workers Launched: 1
         ->  Parallel Seq Scan on document  (cost=0.00..17151.33 rows=1 width=103) (actual time=484.418..484.419 rows=0 loops=2)
               Filter: (to_tsvector('english'::regconfig, text) @@ '''field'' & ''window'' & ''lamp'' & ''depth'' & ''test'''::tsquery)
               Rows Removed by Filter: 50000
 Planning Time: 0.193 ms
 Execution Time: 488.596 ms
```

No difference? The index has not been used... Why is it not working?
Ohh, look to the partial index [docs](https://www.postgresql.org/docs/current/indexes-partial.html):
> However, keep in mind that the predicate must match the conditions used in the queries that are supposed to benefit from the index.
> To be precise, a partial index can be used in a query only if the system can recognize that the WHERE condition of the query mathematically implies the predicate of the index.
> PostgreSQL does not have a sophisticated theorem prover that can recognize mathematically equivalent expressions that are written in different forms.
> (Not only is such a general theorem prover extremely difficult to create, but it would also probably be too slow to be of any real use.)
> The system can recognize simple inequality implications, for example "x < 1" implies "x < 2";
> otherwise the predicate condition must exactly match part of the query's WHERE condition or the index will not be recognized as usable.
> Matching takes place at query planning time, not at run time. As a result, parameterized query clauses do not work with a partial index.

We have to add to our query a condition that was used to create a partial index: `document.language = 'en'`:
```sql
>> EXPłLAIN ANALYZE
   SELECT text, language
   FROM public.document
   WHERE
      to_tsvector('english', text) @@ to_tsquery('english', 'fielded & window & lamp & depth & test ')
      AND language = 'en'
   LIMIT 1;                                                                           QUERY PLAN
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 Limit  (cost=64.00..68.27 rows=1 width=103) (actual time=0.546..0.548 rows=0 loops=1)
   ->  Bitmap Heap Scan on document  (cost=64.00..68.27 rows=1 width=103) (actual time=0.544..0.545 rows=0 loops=1)
         Recheck Cond: ((to_tsvector('english'::regconfig, text) @@ '''field'' & ''window'' & ''lamp'' & ''depth'' & ''test'''::tsquery) AND ((language)::text = 'en'::text))
         ->  Bitmap Index Scan on ix_en_document_tsvector_text  (cost=0.00..64.00 rows=1 width=0) (actual time=0.540..0.540 rows=0 loops=1)
               Index Cond: (to_tsvector('english'::regconfig, text) @@ '''field'' & ''window'' & ''lamp'' & ''depth'' & ''test'''::tsquery)
 Planning Time: 0.244 ms
 Execution Time: 0.590 ms
```

## Tsearch full-text search for partial words
`:*` operator enables prefix search. It can be useful to execute full-text search during typing a word.
```sql
>> EXPLAIN ANALYZE
   SELECT text, language
   FROM public.document
   WHERE
      to_tsvector('english', text) @@ to_tsquery('english', 'fielded & window & l:*')
      AND language = 'en'
   LIMIT 1;
                                                                   QUERY PLAN
------------------------------------------------------------------------------------------------------------------------------------------------
 Bitmap Heap Scan on document  (cost=168.00..172.27 rows=1 width=102) (actual time=5.207..5.210 rows=4 loops=1)
   Recheck Cond: ((to_tsvector('english'::regconfig, text) @@ '''field'' & ''window'' & ''l'':*'::tsquery) AND ((language)::text = 'en'::text))
   Heap Blocks: exact=4
   ->  Bitmap Index Scan on ix_en_document_tsvector_text  (cost=0.00..168.00 rows=1 width=0) (actual time=5.202..5.202 rows=4 loops=1)
         Index Cond: (to_tsvector('english'::regconfig, text) @@ '''field'' & ''window'' & ''l'':*'::tsquery)
 Planning Time: 0.240 ms
 Execution Time: 5.240 ms

>> SELECT id,  text
   FROM public.document
   WHERE
      to_tsvector('english', text) @@ to_tsquery('english', 'fielded & window & l:*')
      AND language = 'en'
   LIMIT 20;
  id   |                                                   text
-------+-----------------------------------------------------------------------------------------------------------
     1 | ﻿degree ranch time tall depth men below dead window waste underline bat lamp putting field               +
 20152 | Law pony follow memory star whatever window sets oxygen longer word whom glass field actual              +
 21478 | Dried symbol willing design managed shade window pick share faster education drive field land everybody  +
 30293 | Pencil seen engineer labor image entire smallest serve field should riding smaller window imagine traffic+

```

## Tsearch full-text search results ranking
There are two quite similar functions to rank tsearch results:
- `ts_rank`, that ranks vectors based on the frequency of their matching lexemes
- `ts_rank_cd`, that computes the "cover density" ranking

For more info, see the [docs](https://www.postgresql.org/docs/13/textsearch-controls.html)
```sql
>> SELECT
     id,
     ts_rank_cd(to_tsvector('english', text), to_tsquery('english', 'fielded & wind:*')) rank,
     text
    FROM public.document
    WHERE to_tsvector('english', text) @@ to_tsquery('english', 'fielded & wind:*')
    ORDER BY rank DESC
    LIMIT 20;
   id   |    rank     |                                                   text
--------+-------------+-----------------------------------------------------------------------------------------------------------
 100002 |         0.1 | fielded window
   9376 |        0.05 | Own mouse girl effect surprise physical newspaper forgot eat upper field element window simply unhappy   +
  96597 |        0.05 | Opinion fastened pencil rear more theory size window heading field understanding farm up position attack +
  44626 | 0.033333335 | Symbol each halfway window swam spider field page shinning donkey chose until cow cabin congress         +
  80922 | 0.033333335 | Victory famous field shelter girl wind adventure he divide rear tip few studied ruler judge              +
  30293 |       0.025 | Pencil seen engineer labor image entire smallest serve field should riding smaller window imagine traffic+
      1 | 0.016666668 | ﻿degree ranch time tall depth men below dead window waste underline bat lamp putting field               +
  21478 | 0.016666668 | Dried symbol willing design managed shade window pick share faster education drive field land everybody  +
  60059 | 0.016666668 | However hungry make proud kids come willing field officer row above highest round wind mile              +
  26001 | 0.014285714 | Earth earlier pocket might sense window way frog fire court family mouth field somebody recognize        +
  20152 | 0.014285714 | Law pony follow memory star whatever window sets oxygen longer word whom glass field actual              +
  37470 |      0.0125 | Farm weight balloon buried wind water donkey grain pig week should damage field was he                   +
  49433 |        0.01 | Wind scientist leaving atom year bad child drink shore spirit field facing indicate wagon here           +
  37851 | 0.007142857 | Field cloud you wife rhythm upward applied weigh continued property replace ahead forgotten trip window  +

```
`text='fielded window'` record was added manually to show the best match result.

## GIST vs GIN
We have created a GIN index. But there is also a GIST index option. Which one is better?
It depends...

```sql
>> EXPLAIN ANALYZE
   SELECT text, language
   FROM public.document
   WHERE
      to_tsvector('english', text) @@ to_tsquery('english', 'fielded & window & lamp & depth & test ')
      AND language = 'en'
   LIMIT 1;
                                                                  QUERY PLAN
-----------------------------------------------------------------------------------------------------------------------------------------------
 Limit  (cost=0.28..8.30 rows=1 width=103) (actual time=2.699..2.700 rows=0 loops=1)
   ->  Index Scan using ix_en_document_tsvector_text on document  (cost=0.28..8.30 rows=1 width=103) (actual time=2.697..2.697 rows=0 loops=1)
         Index Cond: (to_tsvector('english'::regconfig, text) @@ '''field'' & ''window'' & ''lamp'' & ''depth'' & ''test'''::tsquery)
 Planning Time: 0.274 ms
 Execution Time: 2.730 ms
 ```

 GIN seems to be a little bit faster. I don't think I could explain it better than the [docs](https://www.postgresql.org/docs/13/textsearch-indexes.html) already does:
> In choosing which index type to use, GiST or GIN, consider these performance differences:
> - GIN index lookups are about three times faster than GiST
> - GIN indexes take about three times longer to build than GiST
> - GIN indexes are moderately slower to update than GiST indexes, but about 10 times slower if fast-update support was disabled (see Section 58.4.1 for details)
> - GIN indexes are two-to-three times larger than GiST indexes

## Conclusion
I hope this will be helpful for you. Python code to create the database, insert records, and provide integration with SQLAlchemy can be found [here](https://github.com/jorzel/postgres-full-text-search). Thanks!

## Inspiration and help
- [https://about.gitlab.com/blog/2016/03/18/fast-search-using-postgresql-trigram-indexes/](https://about.gitlab.com/blog/2016/03/18/fast-search-using-postgresql-trigram-indexes/)
- [http://rachbelaid.com/postgres-full-text-search-is-good-enough/](http://rachbelaid.com/postgres-full-text-search-is-good-enough/)
- [https://scoutapm.com/blog/how-to-make-text-searches-in-postgresql-faster-with-trigram-similarity](https://scoutapm.com/blog/how-to-make-text-searches-in-postgresql-faster-with-trigram-similarity)
- [https://stackoverflow.com/questions/27443950/make-postgres-full-text-search-tsvector-act-like-ilike-to-search-inside-words](https://stackoverflow.com/questions/27443950/make-postgres-full-text-search-tsvector-act-like-ilike-to-search-inside-words)
- [https://stackoverflow.com/questions/46122175/fulltext-search-combined-with-fuzzysearch-in-postgresql](https://stackoverflow.com/questions/46122175/fulltext-search-combined-with-fuzzysearch-in-postgresql)
- [https://stackoverflow.com/questions/58651852/use-postgresql-full-text-search-to-fuzzy-match-all-search-terms](https://stackoverflow.com/questions/58651852/use-postgresql-full-text-search-to-fuzzy-match-all-search-terms)
- [https://stackoverflow.com/questions/52140727/fuzzy-search-in-full-text-search](https://stackoverflow.com/questions/52140727/fuzzy-search-in-full-text-search)
- [https://stackoverflow.com/questions/2513501/postgresql-full-text-search-how-to-search-partial-words](https://stackoverflow.com/questions/2513501/postgresql-full-text-search-how-to-search-partial-words)
- [https://stackoverflow.com/questions/28975517/difference-between-gist-and-gin-index](https://stackoverflow.com/questions/28975517/difference-between-gist-and-gin-index)
- [https://dba.stackexchange.com/questions/149765/postgresql-gin-index-not-used-when-ts-query-language-is-fetched-from-a-column](https://dba.stackexchange.com/questions/149765/postgresql-gin-index-not-used-when-ts-query-language-is-fetched-from-a-column)
- [https://dba.stackexchange.com/questions/251177/postgres-full-text-search-on-words-not-lexemes](https://dba.stackexchange.com/questions/251177/postgres-full-text-search-on-words-not-lexemes)