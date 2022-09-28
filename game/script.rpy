## Main Menu screen ############################################################
##
## Used to display the main menu when Ren'Py starts.
##
## https://www.renpy.org/doc/html/screen_special.html#main-menu

init -900:

    # First example featured in Readme.
    define rich_presence.first_example = { "details" : "Testing Discord Rich Presence.",
                                           "state" : "It's super easy in Ren'Py 8!",
                                           "large_image" : "lezalith", 
                                           "small_image" : "lezalith",
                                           "time" : True} # small_image is not visible without large_image also set.

    # time gets the timestamp for end property.
    python:
        import time

    # Second example featured in Readme.
    define rich_presence.second_example = { "state" : "Reading a Chapter",
                                           "end" : time.time() + 3000,
                                           "party_size" : [1, 5],
                                           "buttons" : [ dict(label = "Discord Presence Example Button", url = "https://github.com/Lezalith/RenPy_Discord_Presence"),
                                                         dict(label = "Lezalith's Promotion Button!", url = "https://www.lezcave.com") ],
                                            "time" : False} # Included even with `end` overwriting it because the `selected` property of textbutton wouldn't work - `time` is *always* present in discord.properties.

    # Originally defined in discord_rich_presence_settings.rpy, it is overwritten for this project
    # here and controlled from main_menu to display one of the two examples defined above.
    define rich_presence.initial_state = rich_presence.first_example

define g = Solid("808080")
define f = Frame("gui/frame.png")

screen main_menu():

    add g

    frame:
        align (0.5, 0.5)
        padding (80, 100)
        background f

        vbox:
            align (0.5, 0.5)
            spacing 8

            text "Discord Rich Presence in Ren'Py!" xalign 0.5 underline True

            null height 30

            text "{b}Ren'Py Discord Presence{/b} script gives Ren'Py full support for interacting with {b}D{/b}iscord {b}R{/b}ich {b}P{/b}resence."
            text "{b}DRP{/b} is the status shown in one's Discord profile - Game being played, elapsed time played etc."

            null height 30

            text "To see the script in action just click one of the buttons below and watch your Discord activity info change."
            text "First Example is set as the default state."

            null height 30

            vbox:
                xalign 0.5

                hbox:
                    xalign 0.5
                    spacing 100

                    textbutton "Set to First Example":
                        action Function(discord.set, **rich_presence.first_example) 
                        selected discord.properties == rich_presence.first_example
                    textbutton "Set to Second Example":
                        action Function(discord.set, **rich_presence.second_example) 
                        selected discord.properties == rich_presence.second_example

                textbutton "See a dialogue showcasing the script!":
                    xalign 0.5
                    action Start(label = "label_example")

            null height 30

            text "Do not forget that this is just a preview!"
            text "For full instructions on how to use this script, check out its Readme, ideally on {a=https://github.com/Lezalith/RenPy_Discord_Presence}the GitHub page{/a}."

label label_example():

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

    "After this line, {b}discord.change_time{/b} is called to change the Time Elapsed shown. The time is reset and 3000 seconds are added to it."

    $ discord.change_time(timestamp = time.time() - 3000)

    "3000 seconds is 50 minutes, so that's what Time Elapsed got set to."

    "By default, the Time Elapsed is shown. It can be hidden by setting the {b}time{/b} property to False."

    "It is done with {b}discord.update{/b} after this line."

    $ discord.update(time = False)

    "As you can see, Time Elapsed is no longer visible."

    "Finally, after this line, {b}discord.clear{/b} is called to clear the presence."

    $ discord.clear()

    "Presence all cleared and hidden!"

    "After this line, you will return to the main menu, and {b}initial_state{/b} will be restored."

    return