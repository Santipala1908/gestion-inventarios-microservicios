# Etapa base: PHP + Apache
FROM php:8.2-apache

# Instalar dependencias necesarias para Laravel
RUN apt-get update && apt-get install -y \
    libpng-dev libonig-dev libxml2-dev zip unzip git curl \
    && docker-php-ext-install pdo_mysql mbstring exif pcntl bcmath gd

# Habilitar mod_rewrite para Laravel (rutas limpias)
RUN a2enmod rewrite

# Instalar Composer
COPY --from=composer:2.7 /usr/bin/composer /usr/bin/composer

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /var/www/html

# Copiar el código del proyecto al contenedor
COPY . .

# Asignar permisos correctos a las carpetas necesarias de Laravel
RUN chown -R www-data:www-data /var/www/html/storage /var/www/html/bootstrap/cache \
    && chmod -R 775 /var/www/html/storage /var/www/html/bootstrap/cache

# Instalar dependencias de Laravel (solo si no existen vendor/)
RUN if [ ! -d "vendor" ]; then composer install --no-dev --optimize-autoloader; fi

# Configurar Apache para servir Laravel
COPY ./docker/000-default.conf /etc/apache2/sites-available/000-default.conf

# Exponer el puerto del servidor Apache
EXPOSE 80

# Comando que ejecutará el contenedor
CMD ["apache2-foreground"]