# Security By Design - Laboratoria 3

## Zadanie 1: Implementacja rozszerzonego zestawu testów jednostkowych

Dla modelu `customers` przygotowano kompleksowy zestaw testów, obejmujący:
* Weryfikację poprawnych danych (happy path).
* Obsługę danych nieprawidłowych (walidacja).
* Testy bezpieczeństwa (podatność na SQL Injection oraz XSS/JavaScript injection).
* Przypadki skrajne (testy ekstremalne).

![z1.png](.github/TBO/z1.png)

**Status:** Zgodnie z założeniami, przy obecnym stanie implementacji, testy kończą się wynikiem negatywnym.

## Zadanie 2: JWT — wykorzystanie podatności oraz realizacja poprawki

W pierwszej kolejności pozyskałem JWT dla użytkownika Bob:
![z2-1.png](.github/TBO/z2-1.png)
![z2-2.png](.github/TBO/z2-2.png)

Następnie przy pomocy narzędzia [token.dev](https://token.dev) zmodyfikowałem token, zmieniając nazwę użytkownika z `Bob` na `Administrator`:
![z2-3.png](.github/TBO/z2-3.png)

Token został przyjęty bez problemu przez serwer, umożliwiając dostęp do zasobów z uprawnieniami administratora:
![z2-4.png](.github/TBO/z2-4.png)

Zgodnie z wymaganiami, wprowadziłem poprawkę do mechanizmu weryfikacji tokenów JWT.
Po jej wdrożeniu, próba użycia zmodyfikowanego tokena kończy się odrzuceniem go przez serwer:
![z2-5.png](.github/TBO/z2-5.png)
