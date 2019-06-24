class ActionSequence:
    def  __init__(self, action, agent, target):
        self.action = str(action).replace("Actions.", "")
        self.agent = agent
        self.target = target

    def action_string(self):
        if self.target is not None:
            return  "Chosen action: {} with target Player {}".format(self.action, self.target.identifier+1)
        return "Chosen action: {}\n".format(self.action)
    

    def target_string(self):
        return "Was the target of Player {}'s action {}\n".format(str(self.agent.identifier+1), str(self.action))