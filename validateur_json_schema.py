nouvelle_plainte_etablissement = {
    'title': 'Nouvelle plainte',
    "description": "Un client veut déposer une plainte sur un établissement",
    'type': 'object',
    'properties': {
        'etablissement': {
            'type': 'string'
        },
        'no_civique': {
            'type': 'string'
        },
        'nom_rue': {
            'type': 'string'
        },
        'ville': {
            'type': 'string'
        },
        'date_visite': {
            'type': 'string'
        },
        'prenom_plaignant': {
            'type': 'string'
        },
        'nom_plaignant': {
            'type': 'string'
        },
        'description': {
            'type': 'string'
        }
    },
    'required': ['etablissement', 'no_civique', 'nom_rue', 'ville',
                 'date_visite', 'prenom_plaignant', 'nom_plaignant',
                 'description'],
    'additionalProperties': False
}
