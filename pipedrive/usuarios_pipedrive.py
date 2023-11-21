
'''
    En este archivo se guardaran todas aquellas consultas de los usuarios de los vendedores,
    es importante se guardaran por sector, para mejorar el Json y que sea algo modular.
'''


def actualizandoUsuario_IGO(SlpName):
    data = {}
    user_ids = {
        'SANDRA DOÑAN': 13581921,
        'ALVARO AVILES': 13581921,
        'CARLOS AVILES': 13581921,
        'WILLIAM RAMIREZ': 13581932,
        'ALEX ORELLANA': 13581932,
        'JOSE ESTRADA': 13581943,
        'JOSE MENA.': 13581943
    }
    data['user_id'] = user_ids.get(SlpName, 13045165)
    return data

def actualizandoUsuario_CONTRA(SlpName):
    data = {}
    user_ids = {
        'VICTOR ESCOBAR': 13582075,
        'MARLON VIDES': 13582075,
        'MARY LANDAVERDE': 13582086,
        'GERMAN CATIVO': 13582086,
        'MERCEDES CRUZ': 13582097,
        'EDUARDO MARTINEZ': 13582097,
        'ESTHER GUERRERO': 13582097
    }
    data['user_id'] = user_ids.get(SlpName, 13042899)
    return data


def actualizandoUsuario_RETAILAV():
    data = {'user_id': 13738638}
    return data


def actualizandoUsuario_RETAILFB(SlpName):
    data = {}
    user_ids = {
        'ERIKA ESTHEFANY JOVEL ARCE (FLOR BLANCA)': 13738649,
        'ROBERTO GONZALES CARTERA': 13738649,
        'ROBERTO GONZALEZ': 13738649,
        'CESAR NAVIDAD': 13738660,
        'CESAR NAVIDAD CARTERA': 13738660,
        'EDUARDO ACEVEDO': 13738660,
        'EDWIN BARAHONA': 13738660
    }
    data['user_id'] = user_ids.get(SlpName, 13091607)
    return data


def actualizandoUsuario_RETAILSM():
    data = {'user_id': 13738671}
    return data


def actualizandoUsuario_UTIL():
    data = {'user_id': 14065624}
    return data


def actualizandoUsuario_ING(SlpName):
    data = {}
    user_ids = {
        'CARLOS HERNANDEZ': 13545610,
        'HUGO CERRITOS': 13545610,
        'WILLIAM MOLINA': 13814725,
        'GONZALO CHAVARRI': 13814725,
        'WILLAN MEJIA': 13814736,
        'FATIMA FLORES': 13814747,
        'JOSE PREZA': 13814747,
        'JAMIL PALMA': 13814747
    }
    data['user_id'] = user_ids.get(SlpName, 13046551)
    return data


def actualizandoUsuario_MAYO(SlpName):
    data = {}
    user_ids = {
        'ALEX  CAMPOS': 14592007,
        'ASTRID MORAN': 14592007,
        'LUIS PACHECO GUARDADO': 14592007,
        'MARVIN RAMIREZ': 14592018,
        'DAVID ISAAC ORELLANA VASQUEZ': 14592018,
        'NICOLAS QUINTANILLA': 14592018
    }
    data['user_id'] = user_ids.get(SlpName, 13060961)
    return data


