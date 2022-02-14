# Advertisment

Aby uruchomić aplikację należy:

- wygenerować klucze ssh to autentykacji. Przykładowo:
``` 
openssl genrsa -des3 -out private.pem 2048
openssl rsa -in private.pem -outform PEM -pubout -out RS512.key.pub
openssl rsa -in private.pem -out RS512.key -outform PEM
```
- skopiować klucze do mikroserwisów relations, users, advertisements
- docker-compose uruchomi wszystkie serwisy backendowe + varnish + bazy danych
- trzeba uruchomić frontend (zobacz README frontendowe)
