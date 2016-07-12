

in_memory_dict = {}
numequalto_dict = {}
transactions_list = []


def add_numequalsto_value(value):
    """
    Add one to the number of occurrences of the value in the database
    :param value: value of the variable
    :return:
    """

    if value in numequalto_dict:
        numequalto_dict[value] += 1
    else:
        numequalto_dict[value] = 1


def substract_numequalsto_value(value):
    """
    Substract one to the number of occurrences of the value in the database
    :param value: value of the variable
    :return:
    """

    if value in numequalto_dict:
        numequalto_dict[value] -= 1
        if numequalto_dict[value] == 0:
            numequalto_dict.pop(value)


def store_current_variable_and_value_state(name, value=None):
    """
    Stores the value of a variable and the number of occurrences of
    the values that are involved in the command
    This is only performed the first time they are modified in a transaction block
    :param name: name of the variable
    :param value: value of the variable
    :return:
    """

    if is_an_active_transaction():
        last_transaction_block = transactions_list[-1]
        transaction_in_memory_dict = last_transaction_block.get("in_memory_dict")
        if name not in transaction_in_memory_dict:
            transaction_in_memory_dict[name] = in_memory_dict.get(name)
        transaction_numequalto_dict = last_transaction_block.get("numequalto_dict")
        # Current value of the variable
        if name in in_memory_dict:
            before_command_value = in_memory_dict.get(name)
            if before_command_value not in transaction_numequalto_dict:
                transaction_numequalto_dict[before_command_value] = numequalto_dict.get(before_command_value)
        # Value that the command is going to assign the variable
        if value not in transaction_numequalto_dict:
            transaction_numequalto_dict[value] = numequalto_dict.get(value)


def set_command(name, value):
    """
    Store the variable name with the value,
    increase the number of occurrences of the value in the database
    and decrease the occurrence of the previous value, if exists
    :param name: name of the variable
    :param value: value of the variable to be stored
    :return:
    """
    store_current_variable_and_value_state(name, value)

    if name in in_memory_dict:
        substract_numequalsto_value(in_memory_dict.get(name))
    in_memory_dict[name] = value
    add_numequalsto_value(value)


def unset_command(name):
    """
    Remove the variable from the database and reduce
    the number of occurrences of the previous value in the database
    :param name: name of the variable
    :return:
    """
    store_current_variable_and_value_state(name)

    if name in in_memory_dict:
        substract_numequalsto_value(in_memory_dict.get(name))
        in_memory_dict.pop(name)


def begin_command():
    """
    Add a new entry to the transactions_array for a new transaction block
    Initialize the in_memory_dict and numequatoto_dict dictionaries
    :return:
    """
    new_transaction_block = {"in_memory_dict": {}, "numequalto_dict": {}}
    transactions_list.append(new_transaction_block)


def rollback_command():
    """
    Undo all the commands of the last transaction block
    Reading the transaction array in reverse order until it finds the first BEGIN
    :return:
    """

    if is_an_active_transaction():
        last_transaction_block = transactions_list.pop()
        # Set the variables values to those before the transaction started
        for key, value in last_transaction_block.get("in_memory_dict").items():
            if value is None:
                # Remove variable from the database
                if key in in_memory_dict:
                    in_memory_dict.pop(key)
            else:
                # Update variable's value
                in_memory_dict[key] = value
        # Set the values occurrences to those before the transaction started
        for key, value in last_transaction_block.get("numequalto_dict").items():
            if value is None:
                # Remove value from the database
                if key in numequalto_dict:
                    numequalto_dict.pop(key)
            else:
                # Update value occurrences
                numequalto_dict[key] = value


def is_an_active_transaction():
    """
    Return if there is at least on active transaction block
    :return: boolean
    """
    return len(transactions_list) > 0


def run_command(command_line):

    """
    Parse and run the database command
    :param command_line:
    :return:
    """

    command_array = command_line.split()

    if len(command_array) == 1:
        # 0 arguments commands
        ################################
        command = command_array[0]
        if command == 'BEGIN':
            begin_command()
        elif command == 'ROLLBACK':
            if not is_an_active_transaction():
                print 'NO TRANSACTION'
            else:
                rollback_command()
        elif command == 'COMMIT':
            if is_an_active_transaction():
                del transactions_list[:]
            else:
                print 'NO TRANSACTION'
        elif command == 'END':
            return True
        else:
            print 'COMMAND NOT RECOGNIZED'
    elif len(command_array) == 2:
        # 1 arguments commands
        ################################
        command = command_array[0]
        arg1 = command_array[1]
        if command == 'GET':
            print in_memory_dict.get(arg1, 'NULL')
        elif command == 'UNSET':
            if arg1 in in_memory_dict:
                unset_command(arg1)
        elif command == 'NUMEQUALTO':
            print numequalto_dict.get(arg1, '0')
        else:
            print 'COMMAND NOT RECOGNIZED'
    elif len(command_array) == 3:
        # 3 arguments commands
        ################################
        command = command_array[0]
        arg1 = command_array[1]
        arg2 = command_array[2]
        if command == 'SET':
            set_command(arg1, arg2)
        else:
            print 'COMMAND NOT RECOGNIZED'
    else:
        print 'COMMAND NOT RECOGNIZED'

    # No END command
    return False


if __name__ == "__main__":
    end_command = False
    try:
        while not end_command:
            command_line = raw_input()
            end_command = run_command(command_line.strip())
    except EOFError:
        pass
