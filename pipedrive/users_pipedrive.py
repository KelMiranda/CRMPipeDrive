def get_id_pipedrive():
    user_ids = {
        # User for IGO
        'IGO': {
            'SANDRA DOÑAN': [13581921, 'sandra.donan@grupopelsa.com'],
            'ALVARO AVILES': [13581921, 'alvaro.aviles@grupopelsa.com'],
            'CARLOS AVILES': [13581921, 'carlos.aviles@grupopelsa.com'],
            'WILLIAM RAMIREZ': [13581932, 'william.ramirez@grupopelsa.com'],
            'ALEX ORELLANA': [13581932, 'alex.orellana@grupopelsa.com'],
            'JOSE ESTRADA': [13581943, 'vendedor.industria2@grupopelsa.com'], 
            'JOSE MENA.': [13581943, 'vendedor.industria1@grupopelsa.com'],
            'JOSE PEREZ': [13581943, 'grandesclientes.pelsa@grupopelsa.com'],
            'PABLO FLORES': [13045165, 'nilson.doradea@grupopelsa.com'],
            'GERENCIA AV': [13045165, 'nilson.doradea@grupopelsa.com'],
            'WILFREDO DIAZ': [13045165, 'nilson.doradea@grupopelsa.com']
        },

        # User for Contra
        'CONTRA': {
            'VICTOR ESCOBAR': [13582075, 'victor.escobar@grupopelsa.com'],
            'MARLON VIDES': [13582075, 'marlon.vides@grupopelsa.com'],
            'MARY LANDAVERDE': [13582086, 'maria.landaverde@grupopelsa.com'],
            'GERMAN CATIVO': [13582086, 'german.cativo@grupopelsa.com'],
            'MERCEDES CRUZ': [13582097, 'mercedes.cruz@grupopelsa.com'],
            'EDUARDO MARTINEZ': [13582097, 'eduardo.martinez@grupopelsa.com'],
            'ESTHER GUERRERO': [13582097, 'esther.guerrero@grupopelsa.com'],
            'GERENCIA FB': [13042899, 'esau.osegueda@grupopelsa.com']
        },

        # User for Retail-FB
        'RETAIL - FB': {
            'ERIKA ESTHEFANY JOVEL ARCE (FLOR BLANCA)': [13738649, 'erika.jovel@grupopelsa.com'],
            'ROBERTO GONZALES CARTERA': [13738649, 'roberto.gonzalez@grupopelsa.com'],
            'ROBERTO GONZALEZ': [13738649, 'roberto.gonzalez@grupopelsa.com'],
            'CESAR NAVIDAD': [13738660, 'cesar.navidad@grupopelsa.com'],
            'CESAR NAVIDAD CARTERA': [13738660, 'cesar.navidad@grupopelsa.com'],
            'EDUARDO ACEVEDO': [13738660, 'eduardo.acevedo@grupopelsa.com'],
            'EDWIN BARAHONA': [13738660, 'edwin.barahona@grupopelsa.com']
        },

        # User for Retail - AV
        'RETAIL - AV': {
            'EMILY ORELLANA': [13738638, ''],
            'JOSSELYNE HERNANDEZ': [13738638, ''],
            'MARIA LUISA': [13091607, ''],
            'MARTIN OSEGUEDA': [13738638, ''],
            'MARTIN OSEGUEDA CARTERA': [13738638, ''],
            'SAUL RIVAS': [13091607, ],
        },

        # User for Retail - SM
        'RETAIL- SM': {
            'MISAEL CHAVEZ': [13738671, ''],
            'NELSON GUEVARA': [13091607, ''],
            'RENE LOPEZ': [13738671, ''],
            'WILMAN ORELLANA': [13091607, ''],
        },

        # User for ING
        'ING': {
            'CARLOS HERNANDEZ': [13545610, ''],
            'HUGO CERRITOS': [13545610, ''],
            'WILLIAM MOLINA': [13814725, ''],
            'GONZALO CHAVARRI': [13814725, ''],
            'WILLAN MEJIA': [13814736, ''],
            'FATIMA FLORES': [13814747, ''],
            'JOSE PREZA': [13814747, ''],
            'JAMIL PALMA': [13814747, ''],
            'ALEX  CAMPOS': [14592007, ''],
        },

        # User for Mayo
        'MAYO': {
            'ASTRID MORAN': [14592007, ''],
            'LUIS PACHECO GUARDADO': [14592007, ''],
            'ALEX  CAMPOS': [14592007, ''],
            'MARVIN RAMIREZ': [14592018, ''],
            'DAVID ISAAC ORELLANA VASQUEZ': [14592018, ''],
            'NICOLAS QUINTANILLA': [14592018, ''],
            'ERNESTO CAMPOS': [13060961, ''],
            'GERENTE MAYOREO': [13060961, ''],
        },

        # User for Utili
        'UTIL': {
            'JOSE ORTEGA': [14065624, '']
        },

        # User for Admin
        'ADMIN': {
            'GRUPO PELSA': [12806795, '']
        },

        #User for Guatemala
        'GUATEMALA': {
            '4 - ROBERTO ROMERO': [13013045, ''],
            '33 - MYNOR GARCIA': [13004509, ''],
            'JULIO JOSUE CANO LOPEZ': [13013045, ''],
            'WALTER ENRIQUEZ': [13013045, ''],
            'AMANDA BOCHE':[13004509, ''],
            'GERENCIA': [12992629, ''],
            'RUBEN ESCOBAR': [12992629, '']
        }
    }
    return user_ids


class GetIdUser:
    def __init__(self, name=None, mail=None):
        self.name = name
        self.mail = mail

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
            'UTIL',
            'ADMIN',
            'GUATEMALA'
        }
        for row in sector:
            all_sales_person = get_id_pipedrive().get(f'{row}')
            if self.name in all_sales_person:
                result = {
                    'sector': row,
                    'id_user_pipedrive': all_sales_person.get(f'{self.name}')[0],
                    'name': self.name,
                    'mail_pelsa': all_sales_person.get(f'{self.name}')[1],
                }
        return result