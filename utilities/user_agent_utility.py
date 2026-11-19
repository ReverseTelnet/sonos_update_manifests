# ╭────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
# │                                                                                                                                    │
# │     User Agent Utility                                                                                                             │
# │                                                                                                                                    │
# │         This Utility is used to generate a pseudo-random Web Browser User Agent String.                                            │
# │                                                                                                                                    │
# ╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯



# ╭──────────────────────────────────────────────────────────────────────────╮
# │                                                                          │
# │                Absolute Path Imports - Enablement Function               │
# │                                                                          │
# ╰──────────────────────────────────────────────────────────────────────────╯



#  ─────────────────────  Enables Absolute Path Imports  ─────────────────────



def enable_absolute_imports():
    import sys
    from os import getcwd
    PWD = getcwd()
    if PWD in sys.path:
        pass
    else:
        sys.path.append(PWD)



enable_absolute_imports()



# ╭──────────────────────────────────────────────────────────────────────────╮
# │                                                                          │
# │                    Generate Random User Agent Function                   │
# │                                                                          │
# ╰──────────────────────────────────────────────────────────────────────────╯



from secrets import SystemRandom
from utilities.user_agent_list_utility import user_agents_list



#  ───────────────────────  ⚀ ⚁ ⚂ ⚃ ⚄ ⚅ | User Agent  ───────────────────────



def roll_the_user_agent_dice():
    random = SystemRandom()
    first_multiple = random.randint(0, 100)
    second_multiple = random.randint(0, 100)
    first_list = user_agents_list * first_multiple
    second_list = user_agents_list * second_multiple
    complete_list = first_list + second_list
    user_agent = random.choice(complete_list)
    return user_agent


