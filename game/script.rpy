label start:

    "So far, the state is still the same from the project launch."

    $ discord.update(state = "First update, with the time kept.")

    "State was now updated, time kept."

    $ discord.update(state = "Second update, with the time reset.", keep_time = False)

    "State updated again, time reset."

    "I'll now try to change the time!"

    $ discord.change_time()

    "Did it work?"

    return
