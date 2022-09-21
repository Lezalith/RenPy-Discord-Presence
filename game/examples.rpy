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
                                                         dict(label = "Lezalith's Promotion Button!", url = "https://www.lezcave.com") ]}

    # Originally defined in discord_rich_presence_settings.rpy, it is overwritten in this project
    # to display one of the two examples defined above.
    define rich_presence.initial_state = rich_presence.first_example

define g = Solid("808080")
define f = Frame("gui/frame.png")

# label before_main_menu():

#     if rich_presence.presence_object is None:

#         call screen error_screen

#     return

screen error_screen():

    add g

    frame:
        align (0.5, 0.5)
        xysize (1380, 720)
        padding (20, 20)
        background f

        vbox:
            align (0.5, 0.5)

            text "Welcome to a preview of Discord Rich Presence in Ren'Py!" xalign 0.5

            null height 30

            text "It would appear you do not have the Discord Desktop App installed."
            text "It is required to launch this project."

            null height 30

            text "As for players in your own projects that do not have the App installed, don't worry!"
            text "The feature simply gets disabled for them and will not bring up any errors."

screen main_menu():

    add g

    frame:
        align (0.5, 0.5)
        xysize (1280, 720)
        padding (20, 20)
        background f

        vbox:
            align (0.5, 0.5)

            text "Welcome to a preview of Discord Rich Presence in Ren'Py!" xalign 0.5

            null height 30

            text "Below you can see how easy it is to change the presence through screen buttons."
            text "The first_example should already be set, as it's the default when the game is launched!"

            textbutton "Set to First Example":
                action Function(discord.set, **rich_presence.first_example) 
                selected discord.properties == rich_presence.first_example
            textbutton "Set to Second Example":
                action Function(discord.set, **rich_presence.second_example) 
                selected discord.properties == rich_presence.second_example

            textbutton "See examples inside a label.":
                action Start(label = "label_example")

screen screen_example():

    vbox:
        align (0.5, 0.5)

        textbutton "This one sets the state only.":
            action Function(discord.set, state = "Example State.")

        textbutton "This sets details and leaves the state alone.":
            action Function(discord.update, details = "Example Details.")

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

    "After this line, {b}discord.change_time{/b} is called to change the Time Elapsed shown. The time is reset and 50 mins are added to it."

    $ discord.change_time(timestamp = time.time() - 3000)

    "By default, the Time Elapsed is shown. It can be hidden by setting the {b}time{/b} property to False."

    "It is done with {b}discord.update{/b} after this line."

    $ discord.update(time = False)

    "Finally, after this line, {b}discord.clear{/b} is called to clear the presence."

    $ discord.clear()

    "Cleared and hidden!"

    "After this line, you will return to the main menu, and {b}initial_state{/b} will be restored."

    return