# Discord eCommerce Infrastructure
Kullanıcıların Discord uygulaması içerisinden alışveriş yapmalarını sağlayan e-ticaret altyapısı.


## Docker Compose:
```bash
    docker exec -it <web_container_id> bash
    cd ..
    ./setup.sh
```

## Sistemde Kullanılan Discord Botları
- Kullanıcı Discord hesap doğrulaması için [AuthenticateBot](https://github.com/mehmeter3n/Discord-Bots-for-DiscordeCi/tree/main/AuthenticateBot)
- Discord sunucusu üzerinden ürün önermek için [NotificationBot](https://github.com/mehmeter3n/Discord-Bots-for-DiscordeCi/tree/main/NotificationBot)
- Kullanıcıları Discord sunucusu içinde yetkilendiren (Role veren) [RoleBot](https://github.com/mehmeter3n/Discord-Bots-for-DiscordeCi/tree/main/RoleBot)
- Alışveriş sunucusunun gerekli tüm kanal ve yetki (Role) kurulumlarını yapan [SetupBot](https://github.com/mehmeter3n/Discord-Bots-for-DiscordeCi/tree/main/SetupBot)
- Tüm alışveriş işlmelerini (Ürün listeleme, alışveriş onaylama vb.) gerçekleştiren [ShoppingBot](https://github.com/mehmeter3n/Discord-Bots-for-DiscordeCi/tree/main/ShoppingBot)
