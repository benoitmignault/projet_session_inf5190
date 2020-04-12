nouveau_profil = {
    'title': 'Nouveau profil',
    "description": "Les informations nécessaires pour créer un profil "
                   "utilisateur",
    'type': 'object',
    'properties': {
        'nom': {
            'type': 'string',
            "minLength": 3,
            "maxLength": 50
        },
        'prenom': {
            'type': 'string',
            "minLength": 3,
            "maxLength": 50
        },
        'password': {
            'type': 'string',
            "minLength": 8,
            "maxLength": 100
        },
        'courriel': {
            'type': 'string',
            "minLength": 10,
            "maxLength": 50,
            "pattern": "^([a-zA-Z0-9_\.\-\+])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$"
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
    'required': ['nom', 'prenom', 'password', 'courriel',
                 'liste_etablissement'],
    'additionalProperties': False
}
