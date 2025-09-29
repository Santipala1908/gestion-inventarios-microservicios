<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Dashboard</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #00b09b, #96c93d);
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .dashboard {
            background: #fff;
            padding: 2rem 3rem;
            border-radius: 15px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.2);
            text-align: center;
            width: 400px;
        }
        h1 { color: #333; }
        .rol {
            background: #f4f4f4;
            padding: 8px 12px;
            border-radius: 8px;
            display: inline-block;
            margin-top: 10px;
            font-weight: bold;
            color: #444;
        }
        .btn {
            margin-top: 2rem;
            padding: 10px 20px;
            background: #ff512f;
            border: none;
            border-radius: 8px;
            color: #fff;
            font-size: 1rem;
            cursor: pointer;
            transition: 0.3s;
        }
        .btn:hover {
            background: #d63c1d;
        }
    </style>
</head>
<body>
    <div class="dashboard">
        <h1>Bienvenido, {{ auth()->user()->name }}</h1>
        <p>Tu rol:</p>

        @if(auth()->user()->roles->isNotEmpty())
            <div class="rol">{{ auth()->user()->roles->first()->name }}</div>
        @else
            <div class="rol">Sin rol asignado</div>
        @endif

        <form method="POST" action="{{ url('/logout') }}">
            @csrf
            <button type="submit" class="btn">Cerrar sesión</button>
        </form>
    </div>
</body>
</html>
