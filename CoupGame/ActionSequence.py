from Enums import Actions
class ActionSequence:
    def  __init__(self, action, agent, target, block_action = None):
        self.action = action
        self.agent = agent
        self.target = target
        self.block_action = block_action

    def action_string(self, counter):
        possible_actions_active = []
        possible_actions_active.append(Actions.Income)
        possible_actions_active.append(Actions.Foreign_Aid)
        possible_actions_active.append(Actions.Coup)
        for card in self.agent.cards:
            action_active = card.get_action_active()
            action_reactive = card.get_action_reactive()
            # only allow assasinate if agent has >= 3 coin
            if action_active == Actions.Assasinate and self.agent.coins <= 3:
                continue
            # Keep list unique and without None values
            if action_active is not None and action_active not in possible_actions_active:
                possible_actions_active.append(action_active)
        if self.action not in possible_actions_active:
            bluff = True
        else:
            bluff = False

        if bluff:
            if self.target is not None:
                if self.action is Actions.Foreign_Aid:
                    return "{}. (Bluff) Chosen action: {}\n".format(counter, self.actionToString())
                else:
                    return  "{}. (Bluff) Chosen action: {} \nTargetted Player {}\n".format(counter, self.actionToString(), self.target.identifier+1)
            return "{}. (Bluff) Chosen action: {}\n".format(counter, self.actionToString())
        else:
            if self.target is not None:
                if self.action is Actions.Foreign_Aid:
                    return "{}. Chosen action: {}\n".format(counter, self.actionToString())
                else:
                    return  "{}. Chosen action: {} \nTargetted Player {}\n".format(counter, self.actionToString(), self.target.identifier+1)
            return "{}. Chosen action: {}\n".format(counter, self.actionToString())
    

    def target_string(self, counter):
        if self.action is Actions.Foreign_Aid:
            return ""
        elif self.action is Actions.Coup:
            return "{}. Was coupped by Player {} and lost a card\n".format(counter, self.agent.identifier+1)
        elif self.action is Actions.Assasinate:
            return "{}. Was targetted for assasination by Player {}\n".format(counter, self.agent.identifier+1)
        elif self.action is Actions.Steal:
            return "{}. Was targetted for steal by Player {}\n".format(counter, self.agent.identifier+1)

    def block_string(self, counter):
        if self.block_action is Actions.Block_Assasinate:
            return "{}. Blocks assasination of Player {}\n".format(counter, self.agent.identifier+1)
        elif self.block_action is Actions.Block_Foreign_Aid:
            return "{}. Blocks foreign aid of Player {}\n".format(counter, self.agent.identifier+1)
        elif self.block_action is Actions.Block_Steal:
            return "{}. Blocks steal of Player {}\n".format(counter, self.agent.identifier+1)

    def actionToString(self):
        return str(self.action).replace("Actions.", "")

