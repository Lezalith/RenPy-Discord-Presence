# TODO: time in second_example stays the same.
# TODO: label_callback is NOT a list!

init -950 python in rich_presence:

    # Used instead of regular print across this code.
    # Difference is that it only prints out text if `log` is set to True in settings.rpy
    def rich_print(s):
        global log
        if log is True:
            print(s)

    # Alpha and Omega of Rich Presence.
    import pypresence

    # Try to set up the Presence object and connect through it to the Discord Presence App.
    try:
        rich_print("Attempting to connect to Discord Rich Presence...")
        presence_object = pypresence.Presence(application_id)
        presence_object.connect()
        rich_print("Successfully connected.")

    # Discord Desktop App was not found installed.
    except pypresence.DiscordNotFound:
        rich_print("Discord Desktop App not found. Rich Presence will be disabled.")
        presence_object = None

    # Error occured while connecting to the Presence App.
    # Note: This is also raised when the Desktop App is installed but no account is logged in.
    except pypresence.DiscordError:
        rich_print("Error occured during connection. Rich Presence will be disabled.")
        presence_object = None

    # For interacting with Rollback.
    from store import NoRollback

    # Used to display time in the presence.
    import time

    # Timestamp of when the game started. Time Elapsed is calculated from it.
    # Presence can always restore it by changing the start property to "start_time"
    start_time = time.time()

    # For copying dictionaries with properties.
    from copy import deepcopy

    # Returns None, no matter the arguments.
    def return_none(*_args, **_kwargs): pass

    # Decorator that is called before every RenPyDiscord method.
    # If DiscordNotFound or DiscordError were encountered during init, return_none follows rather than the method called originally.
    def presence_disabled(func):
        global presence_object
        if presence_object is None:
            return return_none
        else:
            return func

    # Class of object used for interacting with the Rich Presence.
    class RenPyDiscord(NoRollback):

        # Called when defined.
        def __init__(self):

            # Dict of properties used in the first_setup.
            self.original_properties = {}

            # Dict of currently used Presence properties.
            self.properties = {}

            # Runs the first setup.
            self.first_setup()

        # Sets the initial state and callbacks.
        @presence_disabled
        def first_setup(self):

            # Store properties used for the first setup.
            global main_menu_state
            self.original_properties = main_menu_state

            # If "start" for calculating elapsed time is not provided in the state,
            # set it here to the recorded start_time.
            global start_time
            if not "start" in self.original_properties:
                self.original_properties["start"] = start_time

            # Sets the presence state to the original properties, those just gotten.
            self.reset()

            # Following are all methods being appended to different callbacks.
            # Callbacks are lists of methods that are ran when something happens.
            # As creators can define them themselves, they're accessed here and changed rather than overwritten.

            # quit_callbacks trigger when quitting the game. Serves to properly close the connection to the Presence.
            renpy.config.quit_callbacks.append(self.close)

            # after_load_callbacks trigger when a game is loaded. Updates properties to the ones in a save file.
            renpy.config.after_load_callbacks.append(self.update_on_load)

            # interact_callbacks trigger on every interaction. This keeps a track of rollback.
            renpy.config.interact_callbacks.append(self.rollback_check)

            # start_callbacks trigger when the game is done launching. Records the presence's initial properties into a global var.
            # Even though backup_properties is triggered during init, the global var is overwritten afterwards by a default statement.
            renpy.config.start_callbacks.append(self.backup_properties)

            # start_callbacks trigger when the game is done launching. Records the presence's initial properties into a global var.
            renpy.config.label_callback = self.set_start

        # Sets the state to provided properties.
        @presence_disabled
        def set(self, **properties):

            # Records all the properties passed to the Presence.
            self.properties = deepcopy(properties)

            global start_time

            # If start is specified in the passed properties:
            if "start" in self.properties:

                # First special argument, restores start_time
                if self.properties["start"] == "start_time":
                    self.properties["start"] = start_time

                # Second special argument, resets time to 0:0.
                elif properties["start"] == "new_time":
                    self.properties["start"] = time.time()

            # If "start" for calculating elapsed time is not provided in the state,
            # set it here to the recorded start_time.
            else:
                self.properties["start"] = start_time

            # Record the updated properties into a global var.
            self.backup_properties()

            # Update the presence.
            global presence_object
            presence_object.update(**self.properties)

        # Updates the provided properties, while leaving others as they are.
        @presence_disabled
        def update(self, **properties):

            global start_time

            # If start is specified in the passed properties:
            if "start" in properties:

                # First special argument, restores start_time
                if properties["start"] == "start_time":
                    self.properties["start"] = start_time
                    del properties["start"]    

                # Second special argument, resets time to 0:0.
                elif properties["start"] == "new_time":
                    self.properties["start"] = time.time()
                    del properties["start"]          
 
            # Update properties passed.
            for p in properties:
                self.properties[p] = properties[p]

            # Record the updated properties into a global var.
            self.backup_properties()

            # Update the presence.
            global presence_object
            presence_object.update(**self.properties)

        # Resets the presence to the original properties, gotten from rich_presence.main_menu_state.
        @presence_disabled
        def reset(self):

            # Sets the initial state.
            self.set(**self.original_properties)

        # Clears all the info in the presence.
        @presence_disabled
        def clear(self):

            global presence_object
            presence_object.clear()

            # Clear currently recorded properties.
            self.properties = {}

        ## NOTE: clear seems to have its effect delayed if called too soon
        ##       after establishing the connection (first_setup) or another clear call.
        ## 
        ##       The delay seems to be about 10s on average.
        ##       The minimum wait time to avoid this seems to be about 15s.
        ##
        ##       Same happens with the close method defined below.

        # Restores the presence to a state stored in the save file.
        @presence_disabled
        def update_on_load(self):

            self.set(**self.properties)

        # Sets the Presence to start_state properties.
        @presence_disabled
        def set_start(self, label_name, interaction):

            global start_state, start_label

            if label_name == start_label:
                self.set(**start_state)

        # Sets the properties to those from start_state and records properties into a global var.
        # This var is rollback compatible, unlike this object, and is what makes rollback_check below work.
        # Decorator excluded, it's only used in methods that have the decorator already.
        def backup_properties(self):

            global properties_copy
            properties_copy = deepcopy(self.properties)
            print("Properties recorded: {}".format(properties_copy))

        # Compares the properties to their rollback-able version and updates the presence accordingly if they do not match.
        # This is what makes the script rollback/rollforward compatible.
        @presence_disabled
        def rollback_check(self):

            global properties_copy

            if self.properties != properties_copy:

                print("Properties do not match during this interaction. They will be set to Copy.")
                print("Copy: {}".format(properties_copy))
                print("This: {}\n".format(self.properties))

                self.set(**properties_copy)

        # Properly closes the connection with the Rich Presence.
        # Internally clears the info, no need to call the clear method prior.
        @presence_disabled
        def close(self):

            rich_print("Closing DRP connection.")

            global presence_object
            presence_object.close()

            rich_print("Successfully closed.")

# The object for interacting with Rich Presence defined.
default discord = rich_presence.RenPyDiscord()

default rich_presence.properties_copy = {}