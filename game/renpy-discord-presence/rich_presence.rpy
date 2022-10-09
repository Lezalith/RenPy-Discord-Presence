# Following are all functions being appended to different callbacks. Callbacks are lists of methods that are ran when something happens.

# Triggers upon quitting the game, properly closes connection to the Presence.
define config.quit_callbacks += [discord.close] 

# Triggers upon loading a saved game, updates properties to those in the save file.
define config.after_load_callbacks += [discord.on_load] 

# Triggers upon every interaction, check whether rollbackable and non-rollbackable properties match.
# This is what makes Presence rollback compatible. 
define config.interact_callbacks += [discord.rollback_check] 

# Triggers when the game is done launching. Resets the properties to the default ones.
define config.start_callbacks += [discord.reset]

# Triggers when entering a new label. This is responsible for setting start_state.
define config.label_callback = discord.set_start  # Delete this line in Ren'Py 8.1 or newer.
# define config.label_callbacks += [discord.set_start] # Uncomment this line in Ren'Py 8.1 or newer.

init -950 python in discord:

    # Functions used instead of `print` across this code.
    # Difference is that these only prints out text if the correlating `log` variable is set to True in settings.rpy.
    def print_important(s):
        global log_important
        if log_important is True:
            print("\n" + s)
    def print_properties(s):
        global log_properties
        if log_properties is True:
            print("\n" + s)
    def print_rollback(s):
        global log_restore
        if log_restore is True:
            print("\n" + s)

    # Takes dict of properties, returns string with the dict better represented for printing by print_properties and print_rollback.
    def format_properties(d):
        s = ""
        for key in d:
            s += "\n{}: ".format(key).ljust(14) + " {}".format(d[key])
        return s

    # Alpha and Omega of Rich Presence.
    import pypresence

    # Try to set up the Presence object and connect through it to the Discord Presence App.
    try:
        print_important("Attempting to connect to Discord Rich Presence...")
        presence_object = pypresence.Presence(application_id)
        presence_object.connect()
        print_important("Successfully connected.")

    # Discord Desktop App was not found installed.
    except pypresence.DiscordNotFound:
        print_important("Discord Desktop App not found. Rich Presence will be disabled.")
        presence_object = None

    # Error occured while connecting to the Presence App.
    # Note: This is also raised when the Desktop App is installed but no account is logged in.
    except pypresence.DiscordError:
        print_important("Error occured during connection. Rich Presence will be disabled.")
        presence_object = None

    # For compatibility with Rollback.
    from store import NoRollback

    # Used to display time in the presence.
    import time

    # Timestamp of when the game started. Time Elapsed is calculated from it.
    # Presence can always restore it by changing the start property to "start_time"
    start_time = time.time()

    # For copying dictionaries with properties.
    from copy import deepcopy

    # Decorator that is called before every functions, except those only called from functions that already have it.
    # If DiscordNotFound or DiscordError were encountered during init, return_none follows rather than the method called originally.
    def presence_disabled(func):
        global presence_object
        if presence_object is None:
            return return_none
        else:
            return func

    # Returns None, no matter the arguments.
    def return_none(*_args, **_kwargs): pass

    # Copies properties from non-rollback var to rollback var.
    def record_into_rollback():
        global no_rollback, rollback_properties
        rollback_properties = deepcopy(no_rollback.properties)

    # Inserts a timestamp for the `start` in case it has the value of "start_time".
    # Used by set and update.
    def clean_properties(d):
        d = deepcopy(d)
        global start_time
        if "start" in d:
            if d["start"] == "start_time":
                d["start"] = start_time
        return d

    # Sets the presence to provided properties.
    # Prints out new properties if log is True, used by on_load and rollback_check functions.
    @presence_disabled
    def set(log = True, **props):

        if "start" in props: # If start is specified in the passed properties:
            if props["start"] == "new_time": # Special argument, resets time to 0:0.
                props["start"] = time.time()

        # If "start" for calculating elapsed time is not provided in the state, set it here to "start_time".
        else:
            props["start"] = "start_time"

        # Records all the properties passed to the Presence.
        global no_rollback
        no_rollback.properties = deepcopy(props)

        # Update the presence.
        global presence_object
        presence_object.update(**clean_properties(no_rollback.properties))

        # Record the updated properties into a rollbackable var.
        record_into_rollback()

        if log:
            print_properties("Discord Presence Set:{}".format(format_properties(rollback_properties)))

    # Updates the provided properties, while leaving others as they are.
    # Prints out new properties if log is True.
    @presence_disabled
    def update(log = True, **props):
        if "start" in props: # If start is specified in the passed properties:
            if props["start"] == "new_time": # Special argument, resets time to 0:0.
                props["start"] = time.time()

        # Update properties passed.
        global no_rollback
        for p in props:
            no_rollback.properties[p] = props[p]

        # Update the presence.
        global presence_object
        presence_object.update(**clean_properties(no_rollback.properties))

        # Record the updated properties into a rollbackable var.
        record_into_rollback()

        if log:
            print_properties("Discord Presence Updated:{}".format(format_properties(rollback_properties)))

    # Resets the presence to the properties first shown, gotten from discord.main_menu_state.
    @presence_disabled
    def reset():
        global original_properties
        set(**original_properties)

    # Sets Presence to properties found in the rollbackable var - that one is saved in save files.
    @presence_disabled
    def on_load():
        print_rollback("Discord Presence has been loaded from a save file:{}".format(format_properties(rollback_properties)))

        global rollback_properties
        set(log = False, **rollback_properties)

    # Compares the properties in rollbackable and non-rollbackable variables and restores the presence accordingly if they do not match.
    # This is what makes the script rollback/rollforward compatible.
    @presence_disabled
    def rollback_check():
        global no_rollback, rollback_properties

        if no_rollback.properties != rollback_properties:
            print_rollback("Discord Presence does not match during this interaction. It is restored from the rollbackable variable:{}".format(format_properties(rollback_properties)))

            set(log = False, **rollback_properties)

    # Sets the Presence to start_state properties when entering label(s) given in discord.start_label.
    @presence_disabled
    def set_start(label_name, interaction):
        global start_state, start_label

        # If there are multiple start labels:
        if isinstance(start_label, list):
            if label_name in start_label:
                set(**start_state)

        # If there is only one start label:
        elif label_name == start_label:
            set(**start_state)

    # Clears all the info in the presence, hiding the game being played.
    @presence_disabled
    def clear():
        global no_rollback
        no_rollback.properties = {} # Clear the non-rollbackable var.
        
        record_into_rollback() # Clear the rollbackable var.

        global presence_object
        presence_object.clear()

    # Properly closes the connection with the Rich Presence.
    # Internally clears the info, no need to call the clear method prior.
    @presence_disabled
    def close():
        print_important("Closing DRP connection.")

        global presence_object
        presence_object.close()

        print_important("Successfully closed.")

    # Subclass of NoRollback, this holds the non-rollbackable variable of properties.
    class RenPyDiscord(NoRollback):
        def __init__(self):
            self.properties = {} 

    # First properties to be displayed.
    global original_properties, main_menu_state    
    original_properties = deepcopy(main_menu_state)

    # Insert Time Elapsed into original properties if not provided.
    if not "start" in original_properties:
        original_properties["start"] = "start_time"

    # For creating custom Screen Actions.
    from store import Action

    # Custom Screen Action, equivalent of Function(discord.set). 
    @presence_disabled
    @renpy.pure
    class Set(Action):

        # Remembers the properties given.
        def __init__(self, **properties):
            self.properties = properties

        # What happens when the Action is executed.
        def __call__(self):
            set(**self. properties)

            # Refresh the screen.
            renpy.restart_interaction()

        # Determines whether button is sensitive. True if Presence was successfully initialized.
        def get_sensitive(self):
            global presence_object
            return presence_object is not None

        # Determines whether button is selected. True is current properties match those given to the Action.
        # Exception to this is `start`. If it's not provided in the Action and but it's present in rollback_properties,
        # it is inserted as "start_time" for the comparison.
        def get_selected(self):
            global rollback_properties

            # Determines whether "start_time" should be included in the comparison.
            if "start" in rollback_properties:

                if not "start" in self.properties:

                    a = deepcopy(self.properties)
                    a["start"] = "start_time"

                # Returns the comparison.
                return a == rollback_properties

            # Same here.
            return self.properties == rollback_properties

    # Custom Screen Action, equivalent of Function(discord.update). 
    @presence_disabled
    @renpy.pure
    class Update(Action):

        # Remembers the properties given.
        def __init__(self, **properties):
            self.properties = properties

        # What happens when the Action is executed.
        def __call__(self):
            update(**self. properties)

            # Refresh the screen.
            renpy.restart_interaction()

        # Determines whether button is sensitive. True if Presence was successfully initialized.
        def get_sensitive(self):
            global presence_object
            return presence_object is not None

        # Determines whether button is selected. True is current properties match those given to the Action.
        # Exception to this is `start`. If it's not provided in the Action and but it's present in rollback_properties,
        # it is inserted as "start_time" for the comparison.
        def get_selected(self):
            global rollback_properties

            # Determines whether "start_time" should be included in the comparison.
            if "start" in rollback_properties:

                if not "start" in self.properties:

                    a = deepcopy(self.properties)
                    a["start"] = "start_time"

                # Returns the comparison.
                return a == rollback_properties

            # Same here.
            return self.properties == rollback_properties

# Non-rollbackable variable holding a dict of current Presence properties.
define discord.no_rollback = discord.RenPyDiscord()

# Rollbackable and Saveable variable holding a dict of current Presence properties.
default discord.rollback_properties = {}