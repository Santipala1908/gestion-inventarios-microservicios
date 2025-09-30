<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Gestión de Productos</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #43cea2, #185a9d);
            color: #333;
            margin: 0;
            padding: 20px;
        }
        .container {
            background: #fff;
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.2);
        }
        h1 { text-align: center; margin-bottom: 20px; }
        a.button {
            background: #185a9d;
            color: #fff;
            padding: 10px 15px;
            border-radius: 8px;
            text-decoration: none;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 10px;
            text-align: center;
        }
        th {
            background: #185a9d;
            color: #fff;
        }
        .actions a, .actions form button {
            margin: 0 5px;
            padding: 5px 10px;
            border-radius: 5px;
            border: none;
            cursor: pointer;
            text-decoration: none;
        }
        .actions a.edit { background: #f39c12; color: white; }
        .actions a.show { background: #3498db; color: white; }
        .actions form button { background: #e74c3c; color: white; }
    </style>
</head>
<body>
<div class="container">
    <h1>Gestión de Productos</h1>

    <a href="{{ route('products.create') }}" class="button">+ Nuevo Producto</a>

    @if(session('success'))
        <p style="color:green; margin-top:15px;">{{ session('success') }}</p>
    @endif

    <table>
        <tr>
            <th>ID</th>
            <th>Nombre</th>
            <th>SKU</th>
            <th>Categoría</th>
            <th>Cantidad</th>
            <th>Precio</th>
            <th>Acciones</th>
        </tr>
        @foreach($products as $p)
        <tr>
            <td>{{ $p->id }}</td>
            <td>{{ $p->name }}</td>
            <td>{{ $p->sku }}</td>
            <td>{{ $p->category }}</td>
            <td>{{ $p->quantity }}</td>
            <td>${{ $p->price }}</td>
            <td class="actions">
                <a href="{{ route('products.show', $p->id) }}" class="show">Ver</a>
                <a href="{{ route('products.edit', $p->id) }}" class="edit">Editar</a>
                <form action="{{ route('products.destroy', $p->id) }}" method="POST" style="display:inline;">
                    @csrf @method('DELETE')
                    <button type="submit" onclick="return confirm('¿Seguro que deseas eliminar este producto?')">Eliminar</button>
                </form>
            </td>
        </tr>
        @endforeach
    </table>
</div>
</body>
</html>
