# Discord Rich Presence Support for Ren'Py Projects
This script creates a **RenPyDiscord** object stored in the **discord** variable, which can be used to interact with Discord Rich Presence. To use it in your project, copy the **discord_rich_presence.rpy** file from one of the releases into your **game** folder, and set up the necessary variables listed below in **Related Variables** .

An Application set up on the [Discord Developer Portal](https://discord.com/developers) and it's **Application ID** is also required. How to set it up is described below, in **Setting Up Application on Discord Developer Portal**.

# This Project
Downloading a release of this project and launching it will reveal a simple preview. It shows how to update the presence status from both screens and labels, utilizing the **set** and **update** methods.

The **examples.rpy** file contains a custom **main_menu** screen, which shows how the presence can be updated, as well as a button to enter a label, where updating presence from inside labels is shown. However! You're still better off checking the examples below rather than studying the file.

# Setting Up Application on Discord Developer Portal
Every project that uses the rich presence has to have an application created on the [Discord Developer Portal](https://discord.com/developers).

[TODO]

# Related Variables
There are couple of variables defined in the **discord_rich_presence.rpy** file that you need to visit before using the code.
All are defined within the **rich_presence** namespace, on top of the file. Here is what all of them do and what their default value is.

**application_id** takes a **string** with an Application ID of the Application set up on Discord Developer Portal. This process is described above. 
```py
define rich_presence.application_id = "1020817<six letters left out>262795"
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
All of them are listed below.

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

The difference between the two methods is that while **set** sets the properties only to those given, **update** updates the given properties and leaves others already set alone. 
The overview below also features examples of both **discord.set** and **discord.update**.

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

**large_image** takes a **string** that needs to correspond with an image uploaded onto the Discord Application.
It is the large image shown on the left side.
```py
discord.update(large_image = "lezalith")
```

**small_image** takes a **string** that needs to correspond with an image uploaded onto the Discord Application.
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

Overall, state shown on the screenshot can be accomplished with the following:
```py
discord.set(details = "Testing Discord Rich Presence.",
            state = "It's super easy in Ren'Py 8!",
            large_image = "lezalith",
            large_text = "Large Image Tooltip!",
            small_image = "lezalith",
            small_text = "Small Image Tooltip!",
            time = True)
```

As you can see, there are two more variables there that I haven't mentioned - **large_text** and **small_text**. This is a text tooltip that appears when the respective images are hovered by a cursor.

# Advanced Rich Presence Elements
We have one more screenshot, after which all the features of Rich Presence will be covered. **state** was covered above, however it is required for **party_size** to work.

Dictionary with all the properties for this example is stored in the **rich_presence.second_example** variable.

![rich_presence_example](https://user-images.githubusercontent.com/56970124/190882416-25642658-8823-4d05-8dd9-ee9f9e6d62bf.png)

**end** takes a **string** with an epoch timestamp and calculates time remaining until that timestamp. It pushes aside **start** completely, and the Time Elapsed with it.
It is the smaller image, shown at the bottom right of the **large_image**.
```py
discord.update(end = time.time() + 3000)
```

**party_size** takes a **list** of two **ints**. This is used for multiplayer games, where the two numbers would represent the current party size and max party size respectively. We can still use it with visual novels if we're clever enough.

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
            buttons = [ {"label" : "Discord Presence Example Button", "url" : "https://github.com/Lezalith/RenPy_Discord_Presence"},
                        {"label" : "Lezalith's Promotion Button!", "url" : "https://www.lezcave.com"}])
```