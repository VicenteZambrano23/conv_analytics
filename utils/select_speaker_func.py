def state_transition(last_speaker ,agents):

        if last_speaker is agents[2]:
            # init -> retrieve
            return agents[0]
        elif last_speaker is agents[0]:
            # retrieve: action 1 -> action 2
            return agents[1]
        elif last_speaker is agents[1]:
         
            return agents[3]
        elif last_speaker is agents[3]:
            return agents[2]