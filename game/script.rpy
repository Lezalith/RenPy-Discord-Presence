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
                                           "small_image" : "lezalith"} # small_image is not visible without large_image also set.

    # time gets the timestamp for end property.
    python:
        import time

    # Second example featured in Readme.
    define rich_presence.second_example = { "state" : "Reading a Chapter",
                                           "end" : time.time() + 3000,
                                           "party_size" : [1, 5],
                                           "buttons" : [ dict(label = "Discord Presence Example Button", url = "https://github.com/Lezalith/RenPy_Discord_Presence"),
                                                         dict(label = "Lezalith's Promotion Button!", url = "https://www.lezcave.com") ]}

    # Originally defined in discord_rich_presence_settings.rpy, it is overwritten for this project
    # here and controlled from main_menu to display one of the two examples defined above.
    define rich_presence.initial_state = rich_presence.first_example

# TODO: Mention saving/loading in the preview, maybe make a separate label for people to try it out?

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

    "Since it is set as the {b}start_label{/b} in {b}settings.rpy{/b}, entering it sets the presence to {b}start_state{/b}."

    "After this line, {b}discord.set{/b} will be called to set presence to only contain a {b}state{/b} text line."

    $ discord.set(state = "Update after the first line.")

    "And it is so."

    "After this line, {b}discord.update{/b} is called to change the {b}details{/b} property, while keeping others as they are."

    $ discord.update(details = "This wasn't here before!")

    "Presence now contains one more piece of info."

    "After this line, {b}start{/b} property is changed to {b}\"new_time\"{/b}, which will reset Time Elapsed to 0:0."

    $ discord.update(start = "new_time")

    "The time since the first launch can always be restored by changing {b}start{/b} property to {b}\"start_time\"{/b}"

    "Done after this line."

    $ discord.update(start = "start_time")

    "Finally, changing the {b}start{/b} property to {b}None{/b} hides Time Elapsed altogether."

    "Again, done after this line."

    $ discord.update(start = None)

    "As you can see, Time Elapsed is no longer visible."

    "Last method is {b}discord.clear{/b}, which can be called to clear the presence."

    $ discord.clear()

    "Presence all cleared and hidden!"

    "You will now return to the main menu. {b}main_menu_state{/b} will be restored and Time Elapsed will go back to the time of first launch."

    return