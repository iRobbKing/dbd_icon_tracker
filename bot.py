import config
import tracker


def prepair_templates():
    return (
        tracker.get_status_templates(config.STATUSES['folders']['states'], config.STATUSES['states']), 
        tracker.get_status_templates(config.STATUSES['folders']['actions'], config.STATUSES['actions'])  
    )


def read_survivor_states(states):
    conf = dict(config.COORDINATES)
    del conf['action_offset']
    del conf['action_size']

    for i in range(4):
        yield tracker.read_survivor_state(conf, states, i) 


def read_survivor_actions(actions):
    for i in range(4):
        yield tracker.read_survivor_action(config.COORDINATES, actions, i) 


def read_survivor_statuses(states, actions):
    return zip(read_survivor_states(states), read_survivor_actions(actions))
