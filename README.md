# Simple Database Challenge

By Carlos Maycas Nadal

In this document I explain the thought process I followed to developed this test challenge and quick examples about how to run the code.

### Thought process

I decided to use Python because is, with Java, one of the programming languages that I feel most comfortable with and in my opinion it is faster to write the code on it.

I chose the data structure of dictionary (dict object *in_memory_dict* in the code) to hold the database because it already offers the functionality, managing stored data, that the challenge requires keeping the time constraints ([Python Time Complexity](https://wiki.python.org/moin/TimeComplexity)).

I have also used a dictionary to develop the logic of the command NUMEQUALTO. In order to fulfill the time complexity requirements of the command I decided to store the number of times a value appears in the database in a dictionary (*numequalto_dict*), using the values as keys and the occurrences as values. Based on this design, the code updates the values of the dictionary each time a SET or UNSET command is performed.

* **SET:** It adds one to the number of occurrences of the value that is set to the variable and it subtracts one to the previous value of the variable, in case it was alredy set.
* **UNSET:** It subtracts an occurrence to the value that the variable, which is going to be unset, has in that moment.

About the transactions, I decided it to manage them as a list (*transactions_list*). Each cell of the list represents a transition block, being the last transition block the one in the last position of the list. Each cell is a dictionary with two keys:

* **in_memory_dict**: contains the value of a variable before it was modified, set or unset, for first time inside the transition block. A value of None represents that the variable did not exists in the database before that transition block.
* **numequalsto_dict**: contains the number of ocurrences of a value before it was modified, due to a set or unset command, for first time in the transition block. A value of None represents that the value did not exists in the database before that transition block.

Each command performed inside a transaction block is inmediately applied in the database, changing the state of the dictionaries *in_memory_dict* and *numequalto_dict* (not the ones of each transaction block cell of the list). This design allows to keep the time complexity of the database commands, no matter the size of the transaction block, while it consumes the maxium allowed additional memory per transaction.

In case a ROLLBACK is typed, the last transaction blocked is read from the *transactions_list* and the variables values and number of occurrences of the values are restored to the original values that they had before the transaction block began.

On the other hand, due to the logic implemented, the COMMIT command just clean the transaction array because the commands performed inside the possible active transactions blocks are already commited in the database.

### Setup

This in-memory database require the installation of Python 2.7. 

##### Pass a file of commands to standard input

Just type:
```sh
$ python simpledatabase.py < {commands_file_path}
```
Example:
```sh
$ python simpledatabase.py < example1.txt
```

##### Run the program interactively

Just type:
```sh
$ python simpledatabase.py
```

**Thanks for your attention!**
