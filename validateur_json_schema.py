nouvelle_plainte_etablissement = {
    'title': 'Nouvelle plainte',
    "description": "Un client veut déposer une plainte sur un établissement",
    'type': 'object',
    'properties': {
        'etablissement': {
            'type': 'string',
            "minLength": 3,
            "maxLength": 65
        },
        'no_civique': {
            'type': 'string',
            "minLength": 1,
            "maxLength": 5
        },
        'nom_rue': {
            'type': 'string',
            "minLength": 3,
            "maxLength": 35
        },
        'ville': {
            'type': 'string',
            "minLength": 3,
            "maxLength": 40
        },
        'date_visite': {
            'type': 'string',
            "minLength": 10,
            "maxLength": 10,
            "pattern": '^([0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])$'
        },
        'prenom_plaignant': {
            'type': 'string',
            "minLength": 3,
            "maxLength": 35
        },
        'nom_plaignant': {
            'type': 'string',
            "minLength": 3,
            "maxLength": 35
        },
        'description': {
            'type': 'string',
            "minLength": 5,
            "maxLength": 800
        }
    },
    'required': ['etablissement', 'no_civique', 'nom_rue', 'ville',
                 'date_visite', 'prenom_plaignant', 'nom_plaignant',
                 'description'],
    'additionalProperties': False
}
