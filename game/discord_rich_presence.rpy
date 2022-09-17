
init -10 python:
    import time


define rich_presence.application_id = "1020817080838262795"
define GAME_START_TIME = time.time()

define rich_presence.initial_state = { "state" : "Testing Discord Rich Presence 2."}

init -5 python:

    from pypresence import Presence

    class RenPyDiscord():

        def __init__(self, app_id):

            self.presence = Presence(rich_presence.application_id)

            self.time = GAME_START_TIME

            self.first_setup()

        def first_setup(self):

            self.presence.connect()

            self.update(keep_time = False, **rich_presence.initial_state)

        # if keep_time is True, current timestamp is kept.
        # if False, time is reset to 0.0
        def update(self, state, keep_time = True, **fields):

            if not keep_time:
                self.time = time.time()

            self.presence.update(state = state, start = self.time, **fields)


default discord = RenPyDiscord(app_id = rich_presence.application_id)