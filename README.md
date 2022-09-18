# Discord Rich Presence Support for Ren'Py Projects
This script creates a **RenPyDiscord** object stored in the **discord** variable, which can be used to interact with Discord Rich Presence. To use it in your project, copy the **discord_rich_presence.rpy** file and the **python-packages** folder - that one contains **pypresence**, the module that handles everything here - from one of the releases into your **game** folder, and set up the necessary variables listed below in **Related Variables** .

An Application set up on the [Discord Developer Portal](https://discord.com/developers) and it's **Application ID** is also required. How to set it up is described below, in **Setting Up Application on Discord Developer Portal**.

# This Project
Downloading a release of this project and launching it will reveal a simple preview. It shows how to update the presence status from both screens and labels, utilizing the **set** and **update** methods.

The **examples.rpy** file contains a custom **main_menu** screen, which shows how the presence can be updated from both a screen and a label. Examples there are the same examples at the bottom of this Readme in **Examples**.

# Setting Up Application on Discord Developer Portal
Every project that uses the rich presence has to have an Application created on the [Discord Developer Portal](https://discord.com/developers).

[TODO]

# Preparing Images on the Discord Developer Portal
Every image that you plan to show in the presence has to be uploaded into the Application's Art Assets, under the **Rich Presence** tab.

[TODO]

# Related Variables
There are couple of variables defined in the **discord_rich_presence.rpy** file that you need to visit before using the code.
All are defined within the **rich_presence** namespace, on top of the file. Here is what all of them do and what their default value is.

**application_id** takes a **string** with an Application ID of the Application set up on Discord Developer Portal. This process is described above. 
```py
define rich_presence.application_id = "1020817abcdef262795"
```

**initial_state** takes a dictionary. Keys are **strings** of properties corresponding to presence elements (listed below), and values are **strings** of their values.
In the example project, two examples are defined separately and **initial_state** refers to one of them.
```py
define rich_presence.initial_state = { "details" : "Testing Discord Rich Presence.",
                                       "state" : "It's super easy in Ren'Py 8!",
                                       "large_image" : "lezalith", 
                                       "small_image" : "lezalith"}
```

**main_menu_initial** can be **True** or **False**, determining whether state given in **initial_state** is restored when the game finishes and returns to the main menu. It is **True** by default.
```py
define rich_presence.main_menu_initial = True
```

# List of Methods
Methods used to interact with the presence are bound to the defined **RenPyDiscord** instance stored in the **discord** variable.
Two core methods are described below.

**discord.set** takes the **keep_time** argument to determine whether the Elapsed Time shown should be reset to 0:0 with this change.
As for the arguments that follow, they should correspond to presence elements - all are listed below. 
If some properties are already set in the presence, they are discarded, and only the passed properties are kept.
```py
discord.set(keep_time = False, details = "Testing Discord Rich Presence.")
```

**discord.update** takes **keep_time** and properties corresponding to presence elements just like **discord.set** does.
Difference between the two is that **discord.update** keeps the current properties and only sets the ones provided.
```py
discord.set(details = "Testing Discord Rich Presence.")
discord.update(state = "State got changed while details stayed the same!")
```

# Basic Rich Presence Elements
There are many things that can be shown in Rich Presence. In this screenshot, individual elements of the Presence are highlighted and their **argument** equivalent for **discord.update** method listed at the bottom.

Dictionary with all the properties for this example is stored in the **rich_presence.first_example** variable.

![rich_presence_example](https://user-images.githubusercontent.com/56970124/190881237-3f1e0b72-d954-4af2-8a93-a35e59bdf51e.png)

**details** takes a **string**, and is the upper line of text shown in the Presence.
```py
discord.update(details = "Testing Discord Rich Presence.")
```

**state** takes a **string**, and is the lower line of text shown in the Presence.
```py
discord.update(state = "It's super easy in Ren'Py 8!")
```

**start** takes a **string** with an epoch timestamp, from which it counts the Time Elapsed. However, Elapsed Time should only be changed with the specialized method **change_time**.

**change_time** takes the optional **timestamp** argument, which is the epoch timestamp from which the Time Elapsed is calculated. If it's **None**, as it is by default, the time gets reset to 0:0.
```py
discord.change_time(timestamp = time.time() + 600)
```

**large_image** takes a **string** that needs to correspond with an image uploaded onto the Discord Application - this process is described above.
It is the large image shown on the left side.
```py
discord.update(large_image = "lezalith")
```

**small_image** takes a **string** that needs to correspond with an image uploaded onto the Discord Application - this process is described above.
It is the smaller image, shown at the bottom right of the **large_image**.

If no **large_image** is set, **small_image** is used in it's place and no smaller image at the bottom right is shown.
```py
discord.update(large_image = "lezalith", small_image = "lezalith")
```

**time** is a special non-presence property that can be **True** or **False**.
If **True** (the default), Elapsed Time is shown in the presence. If **False**, it is hidden.
```py
discord.update(time = False)
```

Overall, state shown on the screenshot can be accomplished with the following properties passed:
```py
discord.set(details = "Testing Discord Rich Presence.",
            state = "It's super easy in Ren'Py 8!",
            large_image = "lezalith",
            large_text = "Large Image Tooltip!",
            small_image = "lezalith",
            small_text = "Small Image Tooltip!",
            time = True)
```

As you can see, there are two more variables included there that I haven't mentioned - **large_text** and **small_text**. These are text tooltips that appears when the respective images are hovered by a cursor.

# Advanced Rich Presence Elements
We have one more screenshot, which covers all the remaining rich presence properties. **state** was covered above, however it is required for the **party_size** property to work.

Dictionary with all the properties for this example is stored in the **rich_presence.second_example** variable.

![rich_presence_example](https://user-images.githubusercontent.com/56970124/190882416-25642658-8823-4d05-8dd9-ee9f9e6d62bf.png)

**end** takes a **string** with an epoch timestamp and calculates time remaining until that timestamp. 

Setting this pushed**start** completely aside and the Time Elapsed with it, displaying Time Left instead.
```py
discord.update(end = time.time() + 3000)
```

**party_size** takes a **list** of two **ints**. This is used for multiplayer games, where the two numbers represent the current party size and max party size respectively. We can still use it with visual novels if we're creative enough.

For the **party_size** to be visible, **state** has to be also provided.
```py
discord.update(state = "Reading a Chapter", party_size = [1, 5])
```

**buttons** takes a **list** of **up to two dicts**, and allows for buttons to be added into the Presence. The dict consists of two keys, **label** being the text written on the button, and **url** being the url opened upon clicking it. 

Note: Clicking buttons in your own Presence does nothing.

```py
discord.update(buttons = [ dict(label = "Discord Presence Example Button", url = "https://github.com/Lezalith/RenPy_Discord_Presence"),
                           dict(label = "Lezalith's Promotion Button!", url = "https://www.lezcave.com") ]
```

Putting all of that together, state shown on the screenshot was created with these properties:
```py
discord.set(state = "Reading a Chapter",
            end = time.time() + 3000,
            party_size = [1, 5],
            buttons = [ dict(label = "Discord Presence Example Button", url = "https://github.com/Lezalith/RenPy_Discord_Presence"),
                        dict(label = "Lezalith's Promotion Button!", url = "https://www.lezcave.com") ])
```

# Important Note
Connecting to the Discord Rich Presence multiple times in quick succession will result in the connection not being established.
This makes the program unresponsive and unable to being launched again for about the next 30s. I'd imagine it's a precation against malicious exploits on Discord's side, and cannot be affected by code here.

In practice, this can be achieved by quickly launching and quitting the game, or quickly reloading it multiple times.

# Examples
Here is an example of two **textbutton**s in a screen, one with **discord.set** and other with **discord.update**.
```py
screen screen_example():

    vbox:
        align (0.5, 0.5)

        textbutton "This one sets the state only.":
            action Function(discord.set, state = "Example State.")

        textbutton "This sets details and leaves the state alone.":
            action Function(discord.update, details = "Example Details.")
```

And here is an example of a **label** with most of the functions showcased. Everything is explained by the dialogue lines.
```py
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

    "Finally, after this line, {b}discord.clear{/b} is called to clear the presence.\nIf {b}rich_presence.main_menu_initial{/b} is set to True, it will get reset again when entering the main menu!"

    $ discord.clear()

    "Cleared and hidden!"

    "After this line, you will return to the main menu."

    return
```
