# Application Id - This is gotten from Discord's Developer Portal. 
# Process of setting it up is described on GitHub under the Wiki tab, or locally in [TO-BE-WRITTEN].md
define rich_presence.application_id = "YOUR_APP_ID_HERE"


# Dict with all the properties of the presence state displayed when the game is launched.
# keys correspond not to Presence Fields, but to pypresence arguments! Here is the list of them, from pypresence documentation:
#
# state (str) – the user’s current status
# details (str) – what the player is currently doing
# start (int) – epoch time for game start
# end (int) – epoch time for game end
# large_image (str) – name of the uploaded image for the large profile artwork
# large_text (str) – tooltip for the large image
# small_image (str) – name of the uploaded image for the small profile artwork
# small_text (str) – tootltip for the small image
# party_size (list) – current size of the player’s party, lobby, or group, and the max in this format: [1,4]
# buttons (list) – list of dicts for buttons on your profile in the format [{"label": "My Website", "url": "https://qtqt.cf"}, ...], can list up to two buttons
# time (bool) is a special non-presence property. Giving it the True value displays the Elapsed Time in the presence (default), False hides it.

# First example featured in Readme.
define rich_presence.first_example = { "details" : "Testing Discord Rich Presence.",
                                       "state" : "It's super easy in Ren'Py 8!",
                                       "large_image" : "lezalith", 
                                       "small_image" : "lezalith",
                                       "time" : True} # small_image is not visible without large_image also set.

# Second example featured in Readme.
define rich_presence.second_example = { "state" : "Reading a Chapter",
                                       "end" : time.time() + 3000,
                                       "party_size" : [1, 5],
                                       "buttons" : [ dict(label = "Discord Presence Example Button", url = "https://github.com/Lezalith/RenPy_Discord_Presence"),
                                                     dict(label = "Lezalith's Promotion Button!", url = "https://www.lezcave.com") ]}

# State of the Presence upon the game's launch.
# Here it refers to one of the examples defined above.
define rich_presence.initial_state = rich_presence.first_example

define rich_presence.presence_object = Presence(rich_presence.application_id)

init -10 python:

    # Used to display time in the presence.
    import time

    # For copying dictionaries with properties.
    from copy import deepcopy

    # Alpha and Omega of Rich Presence.
    from pypresence import Presence

    # Class of object for interacting with the Rich Presence.
    class RenPyDiscord():

        # Called when defined.
        def __init__(self):

            # Records the timestamp currently used in the presence.
            # This is so that the same time can be kept upon updating the presence.
            self.time = time.time()

            # Dict of properties used in the first_setup.
            self.original_properties = {}

            # Dict of current Presence properties.
            self.properties = {}

            # Runs the first setup.
            self.first_setup()

        # Connects to the Presence App and sets the initial state.
        def first_setup(self):

            print("Attempting to connect to Discord Rich Presence...")

            # Connects to the Presence App.
            rich_presence.presence_object.connect()

            print("Successfully connected.")

            # Store properties used for the first setup.
            self.original_properties = rich_presence.initial_state

            # Sets the presence state to the original properties, those just gotten.
            self.reset()

            # Appends the close method to exit callbacks,
            # to run it once the game is exited.
            # Done here to not overwrite user's define of config.quit_callbacks, if present somewhere.
            config.quit_callbacks.append(self.close)

        # Sets the state to provided properties.
        # Current timestamp is kept if keep_time is True, and is reset to 0:0 if keep_time is False.
        def set(self, keep_time = True, **properties):

            # Records all the properties passed to the Presence.
            self.properties = deepcopy(properties)

            # We need to care of the default of the time property, if it's not given.
            if not "time" in self.properties:
                self.properties["time"] = True

            # Resets the time if it's not to be kept.
            if not keep_time:
                self.time = time.time()


            # Time prepared to be shown...
            start_time = self.time

            # ...overwritten to None if time property is given...
            if "time" in properties:

                # ...so that time is not displayed if it's False.
                if not properties["time"]:
                    start_time = None

                # time is not a valid property to be passed to presence.update, so we need to remove it.
                del properties["time"]

            # Update the presence.
            # self.properties not used because it includes the time property.
            rich_presence.presence_object.update(start = start_time, **properties)

        # Updates the provided properties, while leaving others as they are.
        # Current timestamp is kept if keep_time is True, and is reset to 0:0 if keep_time is False.
        def update(self, keep_time = True, **properties):

            for p in properties:
                self.properties[p] = properties[p]

            # Resets the time if it's not to be kept.
            if not keep_time:
                self.time = time.time()


            # Time prepared to be shown,...
            start_time = self.time

            # ...as well as the ALL properties to be shown...
            p = self.properties

            # ...with time overwritten to None if time property is given or already set...
            if "time" in p:

                # ...so that time is not displayed if it's False.
                if not p["time"]:
                    start_time = None

                # time is not a valid property to be passed to presence.update, so we need to remove it.
                del p["time"]

            # Update the presence.
            rich_presence.presence_object.update(start = start_time, **p)

        # Changes the Time Elapsed, while keeping everything else untouched.
        # timestamp is None by default, which resets the time to 0:0.
        def change_time(self, timestamp = None):

            if timestamp is None:
                self.time = time.time()

            else:
                self.time = timestamp

            # Prepare the ALL properties to be shown.
            p = self.properties

            # if time is present, remove it, as it's not a valid property for presence.update.
            if "time" in p:
                del p["time"]

            # Update the Presence with new time and current properties.
            rich_presence.presence_object.update(start = self.time, **p)

        # Resets the presence to the original properties, gotten from rich_presence.initial_state.
        def reset(self):

            # Sets the initial state.
            self.set(keep_time = False, **self.original_properties)

        # Clears all the info in the presence.
        def clear(self):

            rich_presence.presence_object.clear()

            # Clear currently recorded properties and time, too.
            self.properties = {}
            self.time = None

        ## NOTE: clear seems to have its effect delayed if called too soon
        ##       after establishing the connection (first_setup) or another clear call.
        ## 
        ##       The delay seems to be about 10s on average.
        ##       The minimum wait time to avoid this seems to be about 15s.
        ##
        ##       Same happens with the close method defined below.

        # Properly closes the connection with the Rich Presence.
        # Internally clears the info, no need to call the clear method.
        def close(self):

            print("Closing DRP connection.")

            rich_presence.presence_object.close()

            print("Successfully closed.")

# The object for interacting with Rich Presence defined.
default discord = RenPyDiscord()