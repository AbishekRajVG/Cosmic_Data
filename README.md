# COSMIC Data | Round 2: Technical Assessment

This repository tracks my submission towards the Technical Assessment for the Data Engineer Opportunity with Cosmic team at Wellcome Sanger

Please check the notion page for official submission:
[https://abishekrajvg.notion.site/COSMIC-Data-Round-2-Technical-Assessment](https://www.notion.so/COSMIC-Data-Round-2-Technical-Assessment-474c0fa9c7c943c0a62323032a127b74?pvs=21)

# Question 1: Bash

## 1.1) Error Handling in a Bash Script

### 1.1.A) To handle errors in Bashmain when we call other Unix commands - We can use one of these two methods:

1. **Exit Code:** Verify if the exit code `$?` of the previous command is zero.
    
    ```bash
    #!/bin/bash
    
    echo "Abishek executes a bash script till a bad unix command"
    
    badcommand
    exit_code=$?
    if [ $exit_code -ne 0 ]; then
    	# Error Handling logic goes here
        echo "ERROR: An error occurred. Exit code: $exit_code"
        exit 1
    fi
    
    echo "No exit? test script scope after the bad unix command"
    ```
    
    ```bash
    (cosmic_data) abishek@Abishekrajs-MacBook-Air 1_Bash % ./main.sh
    Abishek executes a bash script till a bad unix command
    ./main.sh: line 4: badcommand: command not found
    ERROR: An error occurred. Exit code: 127
    ```
    
    Problem: A small problem with this method, or Bash in general is that here the exception/error handling does not happen like in Python or Java. We’ve to manually `exit 1` out of the shell script. However, this behaviour can also be used to our advantage based on our script logic. 
    
2. **Trap: Bash `trap` function to implement error handling when we encounter `ERR` signal**
    
    ```bash
    #!/bin/bash
    
    trap 'catch $? $LINENO' ERR
    
    catch() {
      echo "ERROR: Error code: $1 occurred on line $2"
      exit 1
    }
    
    echo "Abishek executes a bash script till a bad unix command"
    badcommand
    echo "No exit?, test script scope after the bad unix command"
    ```
    
    ```bash
    (cosmic_data) abishek@Abishekrajs-MacBook-Air 1_Bash % ./main.sh
    Abishek executes a bash script till a bad unix command
    ./main.sh: line 11: badcommand: command not found
    ERROR: Error code: 127 occurred on line 11
    ```
    
    Problem: We have the same problem of having to explicitly `exit 1` out of the script. A peculiar issue that could raise is when we have functions that cause errors but bash is unable to catch them through `trap`. Here is an examlpe:
    
    ```bash
    #!/bin/bash
    
    trap 'catch $? $LINENO' ERR
    
    catch() {
      echo "ERROR: Error code: $1 occurred on line $2"
      exit 1
    }
    
    func_with_badcommand() {
      badcommand
      echo "After badcommand: Function executes with no problem"
    }
    
    func_with_badcommand
    echo "After func: The script continues to execute and ERR is never caught"
    ```
    
    ```bash
    (cosmic_data) abishek@Abishekrajs-MacBook-Air 1_Bash % ./main.sh
    ./main.sh: line 11: badcommand: command not found
    After badcommand: Function executes with no problem
    After func: The script continues to execute and ERR is never caught
    ```
    
    Please note that we are not seeing our customer error message, and script seems to execute unfazed even though we have a erroneous command. So bash views functions as separate sub-shells, which means it expects independent sub-shells to take care of their own error handling. In the scope of the [`main.sh`](http://main.sh) script, the sub-shell  `func_with_badcommand` ’s error `badcommand` does not trigger the `ERR` signal unless it is at the end of the function. 
    
    **Fix**: Firstly, we’ll enable `set -e` option to enable exit on error. We’re going to mix both methods: Method 2’s `trap` function now waits for `EXIT`  signal from any sub-shell (or in our case function `func_with_badcommand()` ) and executes `catch()` error handling logic, which will now check exit code `?$` and verify if there is an error on exit or no. 
    
    ```bash
    #!/bin/bash
    
    set -e
    
    trap 'catch $? $LINENO' EXIT
    
    catch() {
        exit_code=$?
        if [ $exit_code -ne 0 ]; then
            # Error Handling logic goes here
            echo "ERROR: An error occurred. Exit code: $exit_code"
            exit 1
        fi
    }
    
    func_with_badcommand() {
      badcommand
      echo "After badcommand: Function executes with no problem"
    }
    
    func_with_badcommand
    echo "After func: The script continues to execute and ERR is never caught"
    ```
    
    ```
    (cosmic_data) abishek@Abishekrajs-MacBook-Air 1_Bash % ./main.sh
    ./main.sh: line 17: badcommand: command not found
    ERROR: An error occurred. Exit code: 127
    ```
    
    The error handling functions as expected. Steps to recreate the output (assuming you have a local clone of the git repository). 
    
    ```
    ./1_Bash/main.sh
    ```
    

### 1.1.B) Error Handling in Python Scripts:

Python has inbuilt exception handling functionality using the `try` `except` `raise` and `finally` statements along with some in-built Exception classes. Here are some examples:

1. A very simple `try-except` statement to catch errors:
    
    ```python
    try:
        print(1/0)
    except ZeroDivisionError as ie:
        print("Error: An "+ str(ie) + " exception has occurred")
    ```
    
    ```python
    (cosmic_data) abishek@Abishekrajs-MacBook-Air Cosmic_Data % python3 1_Bash/myapp.py
    Error: An division by zero exception has occoured
    ```
    
2. Improving, we can have `try-except-else` block statements to handle exception scenarios where we want to execute a set of commands only if there is no exception:
    
    ```python
    try:
        n=1/10
    except ZeroDivisionError as ie:
        print("Error: An "+ str(ie) + " exception has occurred")
    else:
        print("No exceptions, here is your result: " + str(n))
    ```
    
    ```bash
    (cosmic_data) abishek@Abishekrajs-MacBook-Air Cosmic_Data % python3 1_Bash/myapp.py
    No exceptions, here is your result: 0.1
    ```
    
3. Improving, we can have `try-except-else-finally` block statements to handle exception scenarios where no matter what the exception status is, we need a piece of code to execute unfazed:
    
    ```python
    try:
        n=1/10
    except ZeroDivisionError as ie:
        print("Error: An "+ str(ie) + " exception has occurred")
    else:
        print("No exceptions, here is your result: " + str(n))
    finally:
        print("Exception or not, this code was written by Abishek")
    ```
    
    ```bash
    (cosmic_data) abishek@Abishekrajs-MacBook-Air Cosmic_Data % python3 1_Bash/myapp.py
    No exceptions, here is your result: 0.1
    Exception or not, this code was written by Abishek
    ```
    
4. We can also use the `raise` keyword to raise an exception (in-built or user-defined exceptions):
    
    ```bash
    try:
        n=1/10
        if n < 1:
            raise ValueError("Error: value is too small")
    except ZeroDivisionError as ie:
        print("Error: An "+ str(ie) + " exception has occurred")
    except ValueError as ve:
        print('Caught Exception: ' + str(ve))
    else:
        print("No exceptions, here is your result: " + str(n))
    finally:
        print("Exception or not, this code was written by Abishek")
    ```
    
    ```bash
    (cosmic_data) abishek@Abishekrajs-MacBook-Air Cosmic_Data % python3 1_Bash/myapp.py
    Caught Exception: Error: value is too small
    Exception or not, this code was written by Abishek
    (cosmic_data) abishek@Abishekrajs-MacBook-Air Cosmic_Data % 
    ```
    

### 1.1.C) Error Handling in PERL scripts

In Perl scripts, we can use built in components such as `eval` `die` `warn` or popular external cpan modules such as `Try:Tiny` `autodie` `Carp`

1. using `eval` block to catch runtime errors by checking the exit code of eval function `$@` just like bash scripts:
    
    ```perl
    
    eval {
        my $result = 1 / 0; 
        print "Result: $result\n";
    };
    if ($@) {
        print "Error Caught: $@\n";
    }
    ```
    
    ```perl
    (cosmic_data) abishek@Abishekrajs-MacBook-Air 1_Bash % perl myapp.pl 
    Error Caught: Illegal division by zero at myapp.pl line 3.
    ```
    
2. Improving, we can use `die` to explicitly throw exception to be caught from `eval` block’s exit code `$@`
    
    ```perl
    eval {
        open my $fh, '<', 'badfile.txt' or die "Can't open file: $!";
    };
    if ($@) {
        print "Error Caught: $@\n";
    }
    ```
    
    ```bash
    (cosmic_data) abishek@Abishekrajs-MacBook-Air 1_Bash % perl myapp.pl
    Error Caught: Can't open file: No such file or directory at myapp.pl line 11.
    ```
    
3. Improving, we could use CPAN module`autodie` to automatically throw exceptions without explicitly throwing using `die`
    
    ```perl
    use autodie;
    
    eval {
        open my $fh, '<', 'badfile.txt';
        close $fh
    };
    if ($@) {
        print "Error Caught: $@\n";
    }
    ```
    
    ```bash
    (cosmic_data) abishek@Abishekrajs-MacBook-Air 1_Bash % perl myapp.pl
    Error Caught: Can't open 'badfile.txt' for reading: 'No such file or directory' at myapp.pl line 13
    ```
    
4. We could use the CPAN module `Try:Tiny` through which we can implement the classic `try-catch-finally` block statements.
    
    ```perl
    use Try::Tiny;
    
    try {
        my $n=1/0;
    }
    catch {
        print "Exception Caught: $_";
    }
    finally {
        print "Exception or not, this code was written by Abishek";
    };
    
    ```
    
    ```bash
    (cosmic_data) abishek@Abishekrajs-MacBook-Air 1_Bash % perl myapp.pl
    Exception Caught: Illegal division by zero at myapp.pl line 24.
    Exception or not, this code was written by Abishek%                                
    (cosmic_data) abishek@Abishekrajs-MacBook-Air 1_Bash % 
    ```
    
5. Alternatively, we could use CPAN module `carp` which provides detailed functions like `croak` and `confess` that gives a even more detailed error-handling. Carp is mainly only useful when we have complex perl scripts with multiple modules and we need good stack trace of where what went wrong. Here is a very simple example:
    
    ```perl
    use strict;
    use warnings;
    use Carp;
    
    sub bad_function {
        my ($value) = @_;
        if (!$value) {
            carp "Error Caught: value is undefined";
        }
    }
    
    bad_function();
    ```
    
    ```bash
    (cosmic_data) abishek@Abishekrajs-MacBook-Air 1_Bash % perl myapp.pl
    Error Caught: value is undefined at myapp.pl line 39.
            main::bad_function() called at myapp.pl line 44
    ```
    

### 1.1.D) Error handling in DB command line tool: `psql interactive terminal` for Postgres:

The psql command line tool provides a very nifty command line option to enable exception handling. Using the verbose option with `-v ON_ERROR_STOP=1` enables psql to exit with an error code if any command should fail. 

Combining this with Bash’s regular method of checking the exit status method using `$?` helps us catch said error and neatly handle it or persist in a log file depending on our logic. Here is an example:

```bash
#!/bin/bash

# Database connection parameters
DB_HOST="localhost"
DB_PORT="5432"
DB_NAME="mydb"
DB_USER="vgsabishekraj"

# Let there be some SQL querries to execute saved here
SQL_FILE="queries.sql"

# Log file to persist errors
ERROR_LOG="error.log"

# psql command with ON_ERROR_STOP option
psql -v ON_ERROR_STOP=1 \
	-h "$DB_HOST" \
	-p "$DB_PORT" \
	-d "$DB_NAME" \
	-U "$DB_USER" \
	-f "$SQL_FILE" \
	-q -X 2> "$ERROR_LOG"
EXIT_STATUS=$?

if [ $EXIT_STATUS -ne 0 ]; then
  echo "Error: psql command failed. Please see $ERROR_LOG for details."
  exit $EXIT_STATUS
else
  echo "Success: psql command executed successfully."
fi
```

```bash
#!/bin/bash

psql -U postgres -f sample.sql -v ON_ERROR_STOP=1 -q -X >> errors.log
EXIT_STATUS=$?

if [ $EXIT_STATUS -ne 0 ]; then
  echo "Error: psql command failed. See log file for details."
  exit $EXIT_STATUS
else
  echo "Success: psql command executed successfully."
fi
```

```bash
root@23c61d425572:/# ./mypsqlscript.sh 
psql:sample.sql:7: ERROR:  relation "users" already exists
Error: psql command failed. See log file for details.
```

```bash
root@23c61d425572:/# psql -U postgres
psql (16.3 (Debian 16.3-1.pgdg120+1))
Type "help" for help.

postgres=# 
postgres=# 
postgres=# \dt
         List of relations
 Schema | Name  | Type  |  Owner   
--------+-------+-------+----------
 public | users | table | postgres
(1 row)

postgres=# 
```

## 1.2) Asynchronous commands - Best practices

If I were to write a bash script with asynchronous jobs such as nohup or SLURM job, I’d follow the following techniques for best results:

1. Primary thing to implement is a stdout or stderr logfile to all these background processes. This way we can check the progress of the background process at any given time. Here is how:
    
    ```bash
    command > logfile 2>&1 &
    ```
    
    And then to check progress, we can `ps -a` to check the running asynchronous processes and perform a `watch` on the `logfile` we created to see live logs from the background process
    
2. We can also `wait` to keep track of checkpoints and force all asynchronous process to synchronise before exit. This way my script logic would wait for all background process to complete at a checkpoint before proceeding. 
    
    ```bash
    abishek@Abishekrajs-MacBook-Air ~ % cat parallel_proc.sh 
    #!/bin/bash
    
    { sleep 5; echo "Raj called after 5 secs"; } &
    { sleep 1; echo "Abishek called after 1 sec."; } &
    wait
    echo all jobs are done!
    
    abishek@Abishekrajs-MacBook-Air ~ % 
    abishek@Abishekrajs-MacBook-Air ~ % chmod +x parallel_proc.sh 
    abishek@Abishekrajs-MacBook-Air ~ % 
    abishek@Abishekrajs-MacBook-Air ~ % ./parallel_proc.sh 
    Abishek called after 1 sec.
    Raj called after 5 secs
    all jobs are done!
    abishek@Abishekrajs-MacBook-Air ~ % 
    
    ```
    
3. In addition to this, we can use `?!` which is the Process ID and the `?$` which is the exit code of the previous command in our bash logic
    
    ```bash
    abishek@Abishekrajs-MacBook-Air ~ % cat ./parallel_proc.sh 
    #!/bin/bash
    
    wait_and_echo() {
        PID=$1
        echo Waiting for PID $PID to terminate
        wait $PID
        CODE=$?
        echo PID $PID terminated with exit code $CODE
        return $CODE
    }
    
    { sleep 5; echo "Raj called after 5 secs"; } &
    wait_and_echo $!
    
    { sleep 1; echo "Abishek called after 1 sec."; } &
    wait_and_echo $!
    
    echo all jobs are done!
    
    ```
    
    ```bash
    abishek@Abishekrajs-MacBook-Air ~ % ./parallel_proc.sh    
    Waiting for PID 58049 to terminate
    Raj called after 5 secs
    PID 58049 terminated with exit code 0
    Waiting for PID 58052 to terminate
    Abishek called after 1 sec.
    PID 58052 terminated with exit code 0
    all jobs are done!
    ```
    

## 1.3) Code comments in Bash

- Code comments are very important in any language be it OOPs or scripts.
    1. Comments give a better documentation and readability of code. enables clarity of what the original author intended the piece of code to accomplish. 
    2. Comments also embrace maintainability, team collaboration and future-proofing. It allows other people to build and improve upon any piece of code
- Comments are especially important in Bash script due to these following reasons:
    1. Since bash scripts don’t have explicit type or structured syntax like Python or Java, comments are very important to define script flow and logic. Bash scripts can become quite complex, especially when handling conditional logic, loops, or functions. Comments help outline the flow of the script, explaining why certain commands are used in a specific order or how different sections interact.
    2. Bash scripts often work with infrastructure, os or system level and could be very environment specific. Comments can document assumptions about the environment (e.g., required system utilities, expected directory structures) and provide context about why certain commands or settings are necessary.
    3. Error handling in bash is also not very defined like we have pre-defined exception classes and libraries in other programming languages. Thus comments become vital to explaining what possible error is handled and how it is being handled
- To comment in any bash script, we use `#` token followed by our comment string. Two popular methods are
    1. Single line comments  `echo 'hi this is abishek' # This is an example single line comment` 
    2. An multiline comments, usually just a combination of single line comments. 
        
        ```bash
        ############################################################
        # config-driven shell script with cmd line options         #
        ############################################################
        ```
        

---

# Question 2: Data Processing

The relevant Python code for all questions pertaining to this section is uploaded to Github and can be found here: [https://github.com/AbishekRajVG/Cosmic_Data/tree/main/2_Data_Processing](https://github.com/AbishekRajVG/Cosmic_Data/tree/main/2_Data_Processing)

Please find the output below:

```bash
(cosmic_data) abishek@Abishekrajs-MacBook-Air 2_Data_Processing % pip freeze
iniconfig==2.0.0
numpy==2.0.0
packaging==24.1
pandas==2.2.2
pluggy==1.5.0
pytest==8.2.2
python-dateutil==2.9.0.post0
pytz==2024.1
six==1.16.0
tzdata==2024.1
(cosmic_data) abishek@Abishekrajs-MacBook-Air 2_Data_Processing % 
(cosmic_data) abishek@Abishekrajs-MacBook-Air 2_Data_Processing % 
(cosmic_data) abishek@Abishekrajs-MacBook-Air 2_Data_Processing % python3 describe_somatic_mutation.py
mutated_from_allele mutated_to_allele  unique_icgc_mutation_id
                  A                 C                     3613
                  A                 G                     6687
                  A                 T                     3108
                  C                 A                     6195
                  C                 G                    11000
                  C                 T                    30121
                  G                 A                    27458
                  G                 C                    10409
                  G                 T                     4837
                  T                 A                     3004
                  T                 C                     6720
                  T                 G                     4914

        icgc_sample_id  unique_icgc_mutation_id
Highest       SA514800                     4536
Lowest        SA514876                      117
(cosmic_data) abishek@Abishekrajs-MacBook-Air 2_Data_Processing % 
(cosmic_data) abishek@Abishekrajs-MacBook-Air 2_Data_Processing % python3 -m pytest -v                
============================================================= test session starts =============================================================
platform darwin -- Python 3.11.4, pytest-8.2.2, pluggy-1.5.0 -- /Users/abishek/Documents/Job Hunt/cosmic_data/Cosmic_Data/cosmic_data/bin/python3
cachedir: .pytest_cache
rootdir: /Users/abishek/Documents/Job Hunt/cosmic_data/Cosmic_Data/2_Data_Processing
collected 5 items                                                                                                                             

test_describe_somatic_mutation.py::test_get_df_from_tsv_file_not_found PASSED                                                           [ 20%]
test_describe_somatic_mutation.py::test_get_df_from_tsv_valid_case PASSED                                                               [ 40%]
test_describe_somatic_mutation.py::test_get_unique_icgc_mutations PASSED                                                                [ 60%]
test_describe_somatic_mutation.py::test_get_unique_icgc_mutations_count_from_mutated_allele_patterns PASSED                             [ 80%]
test_describe_somatic_mutation.py::test_get_unique_icgc_mutations_count_from_icgc_sample_id PASSED                                      [100%]

============================================================== 5 passed in 0.33s ==============================================================
(cosmic_data) abishek@Abishekrajs-MacBook-Air 2_Data_Processing % 
```

---

# Question 3: Database

### 3.1) How many genes in the gene table have an id_biotype of 23?

```sql
mysql> SELECT COUNT(ID_GENE) AS "# of Genes having id_biotype of 23"
    -> FROM cosmic.gene
    -> WHERE ID_BIOTYPE=23;
+------------------------------------+
| # of Genes having id_biotype of 23 |
+------------------------------------+
|                                174 |
+------------------------------------+
1 row in set (0.00 sec)
```

### 3.2) What is the Ensembl Gene ID for the Gene_symbol TTTY2?

```sql
mysql> SELECT ENSEMBL_GENE_ID
    -> FROM cosmic.gene
    -> WHERE GENE_SYMBOL='TTTY2';
+-----------------+
| ENSEMBL_GENE_ID |
+-----------------+
| ENSG00000212855 |
+-----------------+
1 row in set (0.03 sec)
```

### 3.3) Give a breakdown of the number of genes for each chromosome.

```sql
mysql> SELECT CHROMOSOME, COUNT(ID_GENE) AS "# of Genes per Chromosome"
    -> FROM cosmic.gene
    -> GROUP BY CHROMOSOME;
+------------+---------------------------+
| CHROMOSOME | # of Genes per Chromosome |
+------------+---------------------------+
|         11 |                        25 |
|          6 |                        16 |
|         24 |                         4 |
|         16 |                        28 |
|         15 |                        17 |
|          2 |                        25 |
|          1 |                        51 |
|          5 |                        25 |
|          7 |                        19 |
|          4 |                        20 |
|         17 |                        27 |
|         10 |                        21 |
|         19 |                        27 |
|         22 |                        16 |
|         20 |                        16 |
|         14 |                        18 |
|          8 |                        25 |
|          9 |                        18 |
|         21 |                         9 |
|         18 |                         9 |
|         13 |                        16 |
|          3 |                        31 |
|         23 |                        16 |
|         12 |                        21 |
+------------+---------------------------+
24 rows in set (0.00 sec)
```

### 3.4) How many Transcripts does the Gene Symbol RAI14 has?

```sql
mysql> SELECT g.ID_GENE, g.GENE_SYMBOL, COUNT(t.ID_TRANSCRIPT) AS "# of Transcripts of GENE_SYMBOL RAI14"
    -> FROM cosmic.gene g JOIN cosmic.transcript t
    -> ON g.ID_GENE = t.ID_GENE 
    -> WHERE g.GENE_SYMBOL = 'RAI14'
    -> GROUP BY g.ID_GENE, g.GENE_SYMBOL;
+---------+-------------+---------------------------------------+
| ID_GENE | GENE_SYMBOL | # of Transcripts of GENE_SYMBOL RAI14 |
+---------+-------------+---------------------------------------+
|      61 | RAI14       |                                    29 |
+---------+-------------+---------------------------------------+
1 row in set (0.00 sec)

```

### 3.5) What is the canonical transcript accession for Ensembl Gene id `ENSG00000266960`?

```sql
mysql> SELECT g.ID_GENE, g.ENSEMBL_GENE_ID, t.IS_CANONICAL, t.ACCESSION as "Canonical Transcript Accession for ENSEMBL_GENE_ID"
    -> FROM cosmic.gene g JOIN cosmic.transcript t
    -> ON g.ID_GENE = t.ID_GENE 
    -> AND g.ENSEMBL_GENE_ID = 'ENSG00000266960'
    -> AND t.IS_CANONICAL = 'y';
+---------+-----------------+--------------+----------------------------------------------------+
| ID_GENE | ENSEMBL_GENE_ID | IS_CANONICAL | Canonical Transcript Accession for ENSEMBL_GENE_ID |
+---------+-----------------+--------------+----------------------------------------------------+
|      65 | ENSG00000266960 | y            | ENST00000586416                                    |
+---------+-----------------+--------------+----------------------------------------------------+
1 row in set (0.01 sec)
```

### 3.6) List the Transcript accessions for the Gene Symbol AK1 with id_biotype 23 and flags gencode_basic

```sql
mysql> SELECT -- g.ID_GENE, g.GENE_SYMBOL, g.ID_BIOTYPE, 
    -> t.ACCESSION AS "List of Transcript Accession"
    -> FROM cosmic.gene g JOIN cosmic.transcript t
    -> ON g.ID_GENE = t.ID_GENE 
    -> AND g.GENE_SYMBOL = 'AK1'
    -> AND g.ID_BIOTYPE = '23'
    -> AND t.FLAGS = 'gencode_basic';
+------------------------------+
| List of Transcript Accession |
+------------------------------+
| ENST00000223836              |
| ENST00000373156              |
| ENST00000373176              |
+------------------------------+
3 rows in set (0.00 sec)

```

### 3.7) Imagine that we have a table called “some_gene” with only a subset of the gene data. If I want to join the gene table with this table but display all the genes in the result, what kind of join would you do?

In this scenario, we would want to use an `OUTER JOIN` to ensure all records are returned even if there is a match in the `cosmic.gene` table. Here is an example scenario where I’ve used `RIGHT OUTER JOIN` to focus on the `g.CHROMOSOMES` column from `gene` table. We can see the output containing all CHROMOSOMES even though the `same_gene` has only `s.CHROMOSOME = '10'` 

```sql
mysql> WITH some_gene as (Select * from cosmic.gene WHERE CHROMOSOME='10')
    -> SELECT g.CHROMOSOME, COUNT(g.ID_GENE)
    -> FROM some_gene s RIGHT OUTER JOIN cosmic.gene g
    -> ON s.ID_GENE = g.ID_GENE
    -> WHERE g.ID_BIOTYPE > 45
    -> GROUP BY g.CHROMOSOME
    -> ORDER BY g.CHROMOSOME ;
+------------+------------------+
| CHROMOSOME | COUNT(g.ID_GENE) |
+------------+------------------+
|          1 |               18 |
|          2 |                6 |
|          3 |                4 |
|          4 |                7 |
|          5 |                6 |
|          6 |                2 |
|          7 |                9 |
|          8 |                4 |
|          9 |                6 |
|         10 |                7 |
|         11 |                6 |
|         12 |                7 |
|         13 |                5 |
|         14 |                6 |
|         15 |                8 |
|         16 |                4 |
|         17 |                6 |
|         19 |                6 |
|         20 |                6 |
|         21 |                2 |
|         22 |                2 |
|         23 |                3 |
|         24 |                2 |
+------------+------------------+
23 rows in set (0.01 sec)
```

### 3.8) Imagine that the gene and transcript tables are getting very big and that joining the two tables get slower and slower. What would you do to improve performances?

We can improve performance, expecially when dealing with JOINS between two very large tables using the following methods:

1. **Indexing**: We’ve to primarily ensure that all the columns involved in the JOIN and filtering (such as columns involved in WHERE, GROUP BY and ORDER BY clauses ) as per our logic must be indexed. 
2. **Better SQL Queries:** We have to select required columns instead of maybe `select *` and include aliases (using the `WITH` clause) to sub-queries for better efficiency. 
3. **Right type of JOIN**: The next performance impacting choice is the type of join we use. Unless the business logic requires to use outer joins, inner joins are always more efficient.
4. **Query Caching**: We can smartly save outputs of sub-queries that are getting repeatedly executed (to maybe views or like `PREPARE` clause in Postgres ) to save unnecessary round trips to the DB.
5. **Data Types**: Proper typing can save the DBMS the need to perform type conversions etc.
6. **Partitioning**: Another way to manage very large tables are by partitioning based on some business logic, or just partitioning tables across a swarm of nodes (for example creating parallel interconnected VMs on a Cloud infrastructure) and write SQL quarries to smartly access each partition and aggregate results
7. **Hardware Scaling:** In continuation to this previous idea, we can just physically scale the hardware hosting the DB to improve performance. We could do this by Vertical scaling (improving the CPU Memory resources of a single host) or Horizontal scaling (paritioning the DB into parallel nodes and just adding new nodes to scale up the DB) 

I tried experimenting with indexed but unfortuntely I am not able to create indexes in the provided cosmic VM:

```sql
mysql> CREATE INDEX idx_id_biotype
    -> ON cosmic.gene (ID_BIOTYPE);
ERROR 1142 (42000): INDEX command denied to user 'cosmic'@'localhost' for table 'gene'

mysql> CREATE INDEX idx_gene_symbol
    -> ON cosmic.gene (GENE_SYMBOL);
ERROR 1142 (42000): INDEX command denied to user 'cosmic'@'localhost' for table 'gene'

mysql> CREATE INDEX idx_FLAGS
    -> ON transcript (FLAGS);
ERROR 1142 (42000): INDEX command denied to user 'cosmic'@'localhost' for table 'transcript'
```

### 3.9) If you want to avoid duplicates in a table, what kind of index would you create?

Preventing duplicates from a table is very straight forward, we just have to create a `UNIQUE INDEX` on our desired column. Here is a simple example in Postgres:

```sql
abishek@Abishekrajs-MacBook-Air ~ % docker exec -it postgresql-server-1 psql -U postgres
psql (16.3 (Debian 16.3-1.pgdg120+1))
Type "help" for help.

postgres=# 
postgres=# 
postgres=# CREATE TABLE movies (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    release_year INT,
    genre VARCHAR(100)
);
CREATE TABLE
postgres=# 
postgres=# CREATE UNIQUE INDEX unique_title_idx ON movies (title);
CREATE INDEX
postgres=# 
postgres=# -- Insert a movie into the table
INSERT INTO movies (title, release_year, genre) VALUES ('Inception', 2010, 'Sci-Fi');

-- Insert another movie with a different title
INSERT INTO movies (title, release_year, genre) VALUES ('The Matrix', 1999, 'Sci-Fi');

-- Attempt to insert a movie with a duplicate title, which should fail
INSERT INTO movies (title, release_year, genre) VALUES ('Inception', 2020, 'Sci-Fi');
INSERT 0 1
INSERT 0 1
ERROR:  duplicate key value violates unique constraint "unique_title_idx"
DETAIL:  Key (title)=(Inception) already exists.
postgres=# 
postgres=# 
```

### 3.10) If you want to make sure that all the `id_gene ids` in the transcript table exists in the gene table, what kind of index would you create?

In this scenario, we are going to make sure that the `cosmic.transcript` table does not contain any new `id_gene` which is unfamiliar or not present already in `cosmic.gene` table. We can achieve this in two steps:

1. Create a Foreign key constraint on the `cosmic.transcript` table (example sql, unable to verify in the provided cosmic vm):
    
    ```sql
    ALTER TABLE cosmic.transcript
    ADD CONSTRAINT fk_transcript_gene FOREIGN KEY (ID_GENE)
    REFERENCES cosmic.gene (ID_GENE);
    ```
    
2. Create an Index on the Foreign Key column on the `cosmic.gene` table (example sql, unable to verify in the provided cosmic vm)
    
    ```sql
    CREATE INDEX idx_id_gene ON cosmic.gene (ID_GENE) ;
    ```