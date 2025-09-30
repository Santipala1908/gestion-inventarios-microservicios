<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Detalle Producto</title>
    <style>
        body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #00b09b, #96c93d); display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .container { background: #fff; padding: 2rem; border-radius: 15px; box-shadow: 0 8px 20px rgba(0,0,0,0.2); width: 400px; }
        h1 { text-align: center; }
        p { margin: 10px 0; }
        a { display: block; text-align: center; margin-top: 1rem; color: #00b09b; text-decoration: none; }
    </style>
</head>
<body>
<div class="container">
    <h1>{{ $product->name }}</h1>
    <p><strong>SKU:</strong> {{ $product->sku }}</p>
    <p><strong>Descripción:</strong> {{ $product->description }}</p>
    <p><strong>Categoría:</strong> {{ $product->category }}</p>
    <p><strong>Cantidad:</strong> {{ $product->quantity }}</p>
    <p><strong>Precio:</strong> ${{ $product->price }}</p>

    <a href="{{ route('products.index') }}">Volver</a>
</div>
</body>
</html>
