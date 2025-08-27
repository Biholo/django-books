# Test de l'API avec curl

Token d'authentification : `220eeab6d742f8713aa88d76eee55295453de1f7`

## 1. Test sans authentification (devrait échouer)
```bash
curl -X GET http://localhost:8000/api/livres/
```

## 2. Liste des livres avec authentification
```bash
curl -X GET http://localhost:8000/api/livres/ -H "Authorization: Token 220eeab6d742f8713aa88d76eee55295453de1f7"
```

## 3. Recherche de livre par titre
```bash
curl -X GET "http://localhost:8000/api/livres/?search=misérables" -H "Authorization: Token 220eeab6d742f8713aa88d76eee55295453de1f7"
```

## 4. Liste des auteurs
```bash
curl -X GET http://localhost:8000/api/auteurs/ -H "Authorization: Token 220eeab6d742f8713aa88d76eee55295453de1f7"
```

## 5. Filtrage des auteurs par année de naissance
```bash
curl -X GET "http://localhost:8000/api/auteurs/?year=1830" -H "Authorization: Token 220eeab6d742f8713aa88d76eee55295453de1f7"
```

## 6. Création d'un nouvel auteur
```bash
curl -X POST http://localhost:8000/api/auteurs/ -H "Authorization: Token 220eeab6d742f8713aa88d76eee55295453de1f7" -H "Content-Type: application/json" -d "{\"nom\": \"Marcel Proust\", \"date_naissance\": \"1871-07-10\"}"
```

## 7. Consultation des titres d'un auteur (action personnalisée)
```bash
curl -X GET http://localhost:8000/api/auteurs/1/titres/ -H "Authorization: Token 220eeab6d742f8713aa88d76eee55295453de1f7"
```

## Note
Le serveur Django doit être démarré avec : `python manage.py runserver`
