supprimer_etablissement = {
    'title': 'Supprimer un établissement non nécessaire',
    "description": "Les informations nécessaires",
    'type': 'object',
    'properties': {
        'id_personne': {
            'type': 'integer'
        },
        'id_surveillance': {
            'type': 'integer'
        }
    },
    'required': ['id_personne', 'id_surveillance'],
    'additionalProperties': False
}

ajouter_plusieurs_etablissement = {
    'title': 'Ajout un ou plusieurs établissements à un profil',
    "description": "Les informations nécessaires",
    'type': 'object',
    'properties': {
        'id_personne': {
            'type': 'integer'
        },
        'liste_etablissement': {
            'type': 'array',
            "items": {
                "type": "string"
            },
            "minItems": 1,
            "uniqueItems": True
        }
    },
    'required': ['id_personne', 'liste_etablissement'],
    'additionalProperties': False
}
