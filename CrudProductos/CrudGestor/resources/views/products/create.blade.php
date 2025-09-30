<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Crear Producto</title>
    <style>
        body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #00c6ff, #0072ff); display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .container { background: #fff; padding: 2rem; border-radius: 15px; box-shadow: 0 8px 20px rgba(0,0,0,0.2); width: 400px; }
        h1 { text-align: center; }
        label { font-weight: bold; display: block; margin-top: 1rem; }
        input, textarea { width: 100%; padding: 10px; margin-top: 0.5rem; border: 1px solid #ccc; border-radius: 8px; }
        button { margin-top: 1.5rem; padding: 10px; width: 100%; background: #0072ff; border: none; border-radius: 8px; color: #fff; cursor: pointer; font-size: 1rem; }
        button:hover { background: #0056cc; }
        a { display: block; text-align: center; margin-top: 1rem; color: #0072ff; text-decoration: none; }
    </style>
</head>
<body>
<div class="container">
    <h1>Crear Producto</h1>
    <form method="POST" action="{{ route('products.store') }}">
        @csrf
        <label>Nombre:</label>
        <input type="text" name="name" required>

        <label>SKU:</label>
        <input type="text" name="sku" required>

        <label>Descripción:</label>
        <textarea name="description"></textarea>

        <label>Cantidad:</label>
        <input type="number" name="quantity" required>

        <label>Precio:</label>
        <input type="number" step="0.01" name="price" required>

        <label>Categoría:</label>
        <input type="text" name="category">

        <button type="submit">Guardar</button>
    </form>
    <a href="{{ route('products.index') }}">Volver</a>
</div>
</body>
</html>
