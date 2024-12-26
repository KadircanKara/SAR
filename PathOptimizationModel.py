# T MODELS
T_SOO_GA = {
    'Type': 'SOO',
    'Exp': 'T',
    'Alg': "GA",
    'F': ['Mission Time'],
    'G': ['Max Mission Time'],
    'H': ['Path Speed Violations as Constraint']
}


# C MODELS
C_SOO_GA = {
    'Type': 'SOO',
    'Exp': 'C',
    'Alg': "GA",
    'F': ['Percentage Connectivity'],
    'G': ['Min Percentage Connectivity'],
    'H': ['Path Speed Violations as Constraint']
}


# TC MODELS
TC_SOO_GA_MODEL = {
    'Type': 'SOO',
    'Exp':'TC',
    'Alg': "GA",
    'F': ["Mission Time and Percentage Connectivity Weighted Sum"],
    'G': ['Max Mission Time', 'Min Percentage Connectivity'],
    'H': ['Path Speed Violations as Constraint']
}
TC_MOO_NSGA2 = {
    'Type': 'MOO',
    'Exp':'TC',
    'Alg': "NSGA2",
    'F': ['Mission Time', 'Percentage Connectivity'],
    'G': ['Min Percentage Connectivity', 'Max Mission Time'],
    'H': ['Path Speed Violations as Constraint']
}
TC_MOO_NSGA3 = {
    'Type': 'MOO',
    'Exp':'TC',
    'Alg': "NSGA3",
    'F': ['Mission Time', 'Percentage Connectivity'],
    'G': ['Min Percentage Connectivity', 'Max Mission Time'],
    'H': ['Path Speed Violations as Constraint']
}
TC_MOO_MOEAD = {
    'Type': 'MOO',
    'Exp':'TC',
    'Alg': "MOEAD",
    'F': ['Mission Time', 'Percentage Connectivity'],
    'G': ['Min Percentage Connectivity', 'Max Mission Time'],
    'H': ['Path Speed Violations as Constraint']
}


# TCT MODELS
TCT_SOO_GA_MODEL = {
    'Type': 'SOO',
    'Exp':'TCT',
    'Alg': "GA",
    'F': ["Mission Time and Percentage Connectivity and Max Mean TBV Weighted Sum"],
    'G': ['Max Mission Time', 'Min Percentage Connectivity'],
    'H': ['Path Speed Violations as Constraint']
}
TCT_MOO_NSGA2 = {
    'Type': 'MOO',
    'Exp':'TCT',
    'Alg': "NSGA2",
    'F': ['Mission Time', 'Percentage Connectivity', 'Max Mean TBV'],
    'G': ['Max Mission Time', 'Min Percentage Connectivity'],
    'H': ['Path Speed Violations as Constraint']
}
TCT_MOO_NSGA3 = {
    'Type': 'MOO',
    'Exp':'TCT',
    'Alg': "NSGA3",
    'F': ['Mission Time', 'Percentage Connectivity', 'Max Mean TBV'],
    'G': ['Max Mission Time', 'Min Percentage Connectivity'],
    'H': ['Path Speed Violations as Constraint']
}
TCT_MOO_MOEAD = {
    'Type': 'MOO',
    'Exp':'TCT',
    'Alg': "MOEAD",
    'F': ['Mission Time', 'Percentage Connectivity', 'Max Mean TBV'],
    'H': []
}


# TCDT MODELS
TCDT_SOO_GA = {
    'Type': 'SOO',
    'Exp':'TCDT',
    'Alg': "GA",
    'F': ["Mission Time & Percentage Connectivity & Max Mean TBV & Max Disconnected Time & Mean Disconnected & Time Between Visits Weighted Sum"],
    'G': ['Max Mission Time', 'Min Percentage Connectivity'],
    'H': ['Path Speed Violations as Constraint']
}
TCDT_MOO_NSGA2 = {
    'Type': 'MOO',
    'Exp':'TCDT',
    'Alg': "NSGA2",
    'F': ['Mission Time', 'Percentage Connectivity', 'Mean Disconnected Time','Max Disconnected Time', 'Max Mean TBV'],
    'G': ['Max Mission Time', 'Min Percentage Connectivity'],
    'H': ['Path Speed Violations as Constraint']
}
TCDT_MOO_NSGA3 = {
    'Type': 'MOO',
    'Exp':'TCDT',
    'Alg': "NSGA3",
    'F': ['Mission Time', 'Percentage Connectivity', 'Mean Disconnected Time','Max Disconnected Time','Max Mean TBV'],
    'G': ['Max Mission Time', 'Min Percentage Connectivity'],
    'H': ['Path Speed Violations as Constraint']
}
TCDT_MOO_MOEAD = {
    'Type': 'MOO',
    'Exp':'TCDT',
    'Alg': "MOEAD",
    'F': ['Mission Time', 'Percentage Connectivity', 'Mean Disconnected Time','Max Disconnected Time', 'Path Speed Violations as Objective', 'Max Mean TBV'],
    'G': [],
    'H': []
}


# TCD MODELS
TCD_SOO_GA = {
    'Type': 'SOO',
    'Exp':'TCD',
    'Alg': "GA",
    'F': ["Mission Time & Percentage Connectivity & Max Disconnected Time & Mean Disconnected Weighted Sum"],
    'G': ['Path Speed Violations as Constraint', 'Max Mission Time', 'Min Percentage Connectivity'],
    'H': []
}
TCD_MOO_NSGA2 = {
    'Type': 'MOO',
    'Exp':'TCD',
    'Alg': "NSGA2",
    'F': ['Mission Time', 'Percentage Connectivity', 'Mean Disconnected Time','Max Disconnected Time'],
    'G': ['Path Speed Violations as Constraint', 'Max Mission Time', 'Min Percentage Connectivity'],
    'H': []
}
TCD_MOO_NSGA3 = {
    'Type': 'MOO',
    'Exp':'TCD',
    'Alg': "NSGA3",
    'F': ['Mission Time', 'Percentage Connectivity', 'Mean Disconnected Time','Max Disconnected Time'],
    'G': ['Min Percentage Connectivity','Max Mission Time'],
    'H': ['Path Speed Violations as Constraint']
}
TCD_MOO_MOEAD = {
    'Type': 'MOO',
    'Exp':'TCD',
    'Alg': "MOEAD",
    'F': ['Mission Time', 'Percentage Connectivity', 'Mean Disconnected Time','Max Disconnected Time', 'Path Speed Violations as Objective'],
    'G': [],
    'H': []
}


# CD MODELS
CD_SOO_GA = {
    'Type': 'SOO',
    'Exp': 'CD',
    'Alg': "GA",
    'F': ["Percentage Connectivity & Mean Disconnected Time & Max Disconnected Time Weighted Sum"],
    'G': [],
    'H': ['Path Speed Violations as Constraint']
}
CD_MOO_NSGA2 = {
    'Type': 'MOO',
    'Exp': 'CD',
    'Alg': "NSGA2",
    'F': ['Percentage Connectivity', 'Mean Disconnected Time','Max Disconnected Time'],
    'G': [],
    'H': ['Path Speed Violations as Constraint']
}
CD_MOO_NSGA3 = {
    'Type': 'MOO',
    'Exp': 'CD',
    'Alg': "NSGA3",
    'F': ['Percentage Connectivity', 'Mean Disconnected Time','Max Disconnected Time'],
    'G': [],
    'H': ['Path Speed Violations as Constraint']
}
CD_MOO_MOEAD = {
    'Type': 'MOO',
    'Exp': 'CD',
    'Alg': "MOEAD",
    'F': ['Percentage Connectivity', 'Mean Disconnected Time','Max Disconnected Time'],
    'G': [],
    'H': ['Path Speed Violations as Constraint']
}

















"""Mission Time, Percentage Connectivity, TBV MOO Models"""




"""Mission Time, Percentage Connectivity, Max and Mean Disconnected Time, TBV MOO Models"""



"""Mission Time, Percentage Connectivity, Max and Mean Disconnected Time MOO Models"""



"""Mission Time, Percentage Connectivity MOO Models"""






"""Percentage Connectivity, Max and Mean Disconnected Time MOO Models"""



"""GA Models"""

