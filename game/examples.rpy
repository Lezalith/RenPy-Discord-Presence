label start:

    "This label shows how discord presence can be changed inside labels!"

    "After this line, {b}discord.set{/b} will be called to set presence to only contain a {b}state{/b} text line."

    $ discord.set(state = "Update after the first line.")

    "And it is so. Elapsed Time stayed the same."

    "After this line, {b}discord.set{/b} is called again, with {b}keep_time = False{/b} argument passed, so that the time gets set to 0:0."

    $ discord.set(state = "Second update, with the time reset.", keep_time = False)

    "State updated and Elapsed Time reset."

    "After this line, {b}discord.update{/b} is called to change the {b}details{/b} property, while keeping others ({b}state{/b} and {b}time{/b}) as they are."

    $ discord.update(details = "This wasn't here before!")

    "Presence now contains one more piece of info."

    "After this line, {b}discord.change_time{/b} is called to change the Time Elapsed shown. The time is reset and 50 mins are added to it."

    $ discord.change_time(timestamp = time.time() - 3000)

    "By default, the Time Elapsed is shown. It can be hidden by setting the {b}time{/b} property to False."

    "It is done with {b}discord.update{/b} after this line."

    $ discord.update(time = False)

    "Finally, after this line, {b}discord.clear{/b} is called to clear the presence.\nIf {b}rich_presence.main_menu_initial{/b} is set to True, it will get reset again when entering the main menu!"

    $ discord.clear()

    "Cleared and hidden!"

    "After this line, you will return to the main menu."

    return
