# Etapa base: PHP + Apache
FROM php:8.2-apache

# Instalar dependencias necesarias para Laravel
RUN apt-get update && apt-get install -y \
    libpng-dev libonig-dev libxml2-dev zip unzip git curl \
    && docker-php-ext-install pdo_mysql mbstring exif pcntl bcmath gd

# Habilitar mod_rewrite para Laravel (rutas limpias)
RUN a2enmod rewrite

# Instalar Composer desde la imagen oficial
COPY --from=composer:2.7 /usr/bin/composer /usr/bin/composer

# Directorio de trabajo dentro del contenedor
WORKDIR /var/www/html

# Copiar el código del proyecto
COPY . .

# Dar permisos a storage y cache
RUN chown -R www-data:www-data /var/www/html/storage /var/www/html/bootstrap/cache \
    && chmod -R 775 /var/www/html/storage /var/www/html/bootstrap/cache

# Instalar dependencias de Laravel (si no existe vendor/)
RUN if [ ! -d "vendor" ]; then composer install --no-dev --optimize-autoloader; fi

# Configurar Apache para servir Laravel (public/)
COPY ./docker/000-default.conf /etc/apache2/sites-available/000-default.conf

# Exponer puerto HTTP del contenedor
EXPOSE 80

# Comando de arranque
CMD ["apache2-foreground"]
