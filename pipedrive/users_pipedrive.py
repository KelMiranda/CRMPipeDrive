def get_id_pipedrive():
    user_ids = {
        # User for IGO
        'IGO': {
            'SANDRA DOÑAN': 13581921,
            'ALVARO AVILES': 13581921,
            'CARLOS AVILES': 13581921,
            'WILLIAM RAMIREZ': 13581932,
            'ALEX ORELLANA': 13581932,
            'JOSE ESTRADA': 13581943,
            'JOSE MENA.': 13581943,
            'JOSE PEREZ': 13581943,
            'PABLO FLORES': 13045165,
            'GERENCIA AV': 13045165,
            'WILFREDO DIAZ': 13045165
        },

        # User for Contra
        'CONTRA': {
            'VICTOR ESCOBAR': 13582075,
            'MARLON VIDES': 13582075,
            'MARY LANDAVERDE': 13582086,
            'GERMAN CATIVO': 13582086,
            'MERCEDES CRUZ': 13582097,
            'EDUARDO MARTINEZ': 13582097,
            'ESTHER GUERRERO': 13582097,
            'GERENCIA FB': 13042899
        },

        # User for Retail-FB
        'RETAIL - FB': {
            'ERIKA ESTHEFANY JOVEL ARCE (FLOR BLANCA)': 13738649,
            'ROBERTO GONZALES CARTERA': 13738649,
            'ROBERTO GONZALEZ': 13738649,
            'CESAR NAVIDAD': 13738660,
            'CESAR NAVIDAD CARTERA': 13738660,
            'EDUARDO ACEVEDO': 13738660,
            'EDWIN BARAHONA': 13738660
        },

        # User for Retail - AV
        'RETAIL - AV': {
            'EMILY ORELLANA': 13738638,
            'JOSSELYNE HERNANDEZ': 13738638,
            'MARIA LUISA': 13091607,
            'MARTIN OSEGUEDA': 13738638,
            'MARTIN OSEGUEDA CARTERA': 13738638,
            'SAUL RIVAS': 13091607,
        },

        # User for Retail - SM
        'RETAIL- SM': {
            'MISAEL CHAVEZ': 13738671,
            'NELSON GUEVARA': 13091607,
            'RENE LOPEZ': 13738671,
            'WILMAN ORELLANA': 13091607,
        },

        # User for ING
        'ING':{
            'CARLOS HERNANDEZ': 13545610,
            'HUGO CERRITOS': 13545610,
            'WILLIAM MOLINA': 13814725,
            'GONZALO CHAVARRI': 13814725,
            'WILLAN MEJIA': 13814736,
            'FATIMA FLORES': 13814747,
            'JOSE PREZA': 13814747,
            'JAMIL PALMA': 13814747,
            'ALEX  CAMPOS': 14592007,
        },

        # User for Mayo
        'MAYO': {
            'ASTRID MORAN': 14592007,
            'LUIS PACHECO GUARDADO': 14592007,
            'ALEX  CAMPOS': 14592007,
            'MARVIN RAMIREZ': 14592018,
            'DAVID ISAAC ORELLANA VASQUEZ': 14592018,
            'NICOLAS QUINTANILLA': 14592018,
            'ERNESTO CAMPOS': 13060961,
            'GERENTE MAYOREO': 13060961,
        },

        # User for Utili
        'UTIL': {
            'JOSE ORTEGA': 14065624
        }

    }
    return user_ids


class GetIdUser:
    def __init__(self, name):
        self.name = name

    def get_user_id_and_sector(self):
        result = {}
        sector = {
            'CONTRA',
            'IGO',
            'ING',
            'MAYO',
            'RETAIL - AV',
            'RETAIL - FB',
            'RETAIL- SM',
            'UTIL'
        }
        for row in sector:
            all_sales_person = get_id_pipedrive().get(f'{row}')
            if self.name in all_sales_person:
                result = {
                    'sector': row,
                    'id_user_pipedrive': all_sales_person.get(f'{self.name}'),
                    'name': self.name
                }
            else:
                result = {
                    'sector': row,
                    'id_user_pipedrive': 12806795,
                    'name': self.name,
                    'Cuenta': 'Principal'
                }
        return result
