init -950 python in rich_presence:

    # Alpha and Omega of Rich Presence.
    import pypresence

    # Try to set up the Discord Presence object.
    try:
        presence_object = pypresence.Presence(application_id)

    # Discord Desktop App was not found installed:
    except pypresence.DiscordNotFound:
        presence_object = None

    # Used to display time in the presence.
    import time

    # For copying dictionaries with properties.
    from copy import deepcopy

    # Class of object for interacting with the Rich Presence.
    class RenPyDiscord():

        # Called when defined.
        def __init__(self):

            # Ignore this entire class 
            if presence_object is None:

                print("Discord Desktop App not found. Rich Presence will be disabled.")
                return None

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
            presence_object.connect()

            print("Successfully connected.")

            # Store properties used for the first setup.
            self.original_properties = initial_state

            # Sets the presence state to the original properties, those just gotten.
            self.reset()

            # Appends the close method to exit callbacks, to run it once the game is exited.
            # Done here to not overwrite user's define of config.quit_callbacks, if present somewhere.
            renpy.config.quit_callbacks.append(self.close)

            # Appends the close method to after load callbacks, to run it once a game save is loaded.
            # Done here to not overwrite user's define of config.after_load_callbacks, if present somewhere.
            renpy.config.after_load_callbacks.append(self.update_on_load)

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
            presence_object.update(start = start_time, **properties)

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
            presence_object.update(start = start_time, **p)

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
            presence_object.update(start = self.time, **p)

        # Resets the presence to the original properties, gotten from rich_presence.initial_state.
        def reset(self):

            # Sets the initial state.
            self.set(keep_time = False, **self.original_properties)

        # Clears all the info in the presence.
        def clear(self):

            presence_object.clear()

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

        # Restores the presence to a state stored in the save file.
        def update_on_load(self):

            # Right now, Time Elapsed is set to 0:0 upon loading a save file. 
            #
            # A workaround here could be nice to solve this, probably by recording the start property
            # somewhere before the load, and restoring it here afterwards,
            # but I think it's too little of an issue to be worth solving.

            self.set(keep_time = False, **self.properties)

        # Properly closes the connection with the Rich Presence.
        # Internally clears the info, no need to call the clear method.
        def close(self):

            print("Closing DRP connection.")

            presence_object.close()

            print("Successfully closed.")

# The object for interacting with Rich Presence defined.
default discord = rich_presence.RenPyDiscord()