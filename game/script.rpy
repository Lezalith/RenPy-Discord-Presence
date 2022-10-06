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
            text "{b}DRP{/b} is the status shown in one's Discord profile - Game being played, Elapsed Time played etc."
            text "Your Discord profile should already display this preview being played!"

            null height 30

            text "These buttons change your Presence to the two examples from Readme."

            null height 15

            hbox:
                xalign 0.5
                spacing 100

                textbutton "Set to First Example":
                    action Function(discord.set, **rich_presence.first_example) 
                    selected discord.properties == rich_presence.first_example
                textbutton "Set to Second Example":
                    action Function(discord.set, **rich_presence.second_example) 
                    selected discord.properties == rich_presence.second_example

            null height 30

            text "You can also check out one of the labels."

            null height 15

            hbox:
                xalign 0.5
                spacing 100

                vbox:
                    spacing 8
                    textbutton "Long Simple Label" xalign 0.5 action Start(label = "long_example")
                    text "Great for trying saving/loading\nand rollback compatibility."

                vbox:
                    spacing 8
                    textbutton "Functionality Label" xalign 0.5 action Start(label = "functionality_example")
                    text "Shows everythings this script\ncan do in action."

            null height 30

            text "Do not forget that this is just a preview!"
            text "For full instructions on how to use this script, check out its Readme, ideally on {a=https://github.com/Lezalith/RenPy_Discord_Presence}the GitHub page{/a}."

label functionality_example():

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

    "Last method is {b}discord.clear{/b}, which can be called to clear the presence of all properties."

    "This hides the game completely, as if nothing was being played."

    $ print("\n\n")
    $ discord.clear()

    "Presence all cleared and hidden!"

    "You will now return to the main menu. {b}main_menu_state{/b} will be restored and Time Elapsed will go back to the time of first launch."

    return

label long_example():

    $ discord.set(details = "Inside a Preview", state = "Save & Load")

    "Welcome to the Save/Load preview label."

    "Feel free to save in any of the following places - just right-click and select a save slot."

    scene scarian_island

    $ discord.set(details = "Hanging out on Scarian Island", state = "Swimming")

    "An island in the middle of the ocean."

    "Swim around as much as you want, you won't find any sharks here!"

    "Moving on..."

    scene cerise_chantry

    $ discord.set(details = "Walking around Cerise", state = "Visiting the Garden")

    "A peaceful chantry with a rose garden."

    "Can you hear the sound of silence?"

    "Of course you can, this project has no audio."

    "Moving on..."

    scene gamboge_peninsula

    $ discord.set(details = "On Gamboge Peninsula", state = "Sunbathing")

    "A desert oasis with a strange name."

    "Be careful not to get a heatstroke."

    "Moving on..."

    scene minty_meadows

    $ discord.set(details = "Traversing Minty Meadows", state = "Chasing Cats")

    "A beautiful land filled with flowers and bushes."

    "For some reason, there are cats running everywhere around you."

    "Okay, that's it. Ready to head back?"

    scene 

    $ discord.set(details = "Inside a Preview", state = "Save & Load")

    "You can now right-click again and {b}load{/b} the previous saved game."

    "Presence properties will be reverted, too!"

    "Moving past this line returns you to the main screen."

    return