<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Iniciar Sesión</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #ff512f, #dd2476);
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            background: #fff;
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.2);
            width: 350px;
            text-align: center;
        }
        h1 { margin-bottom: 1rem; color: #333; }
        label { font-weight: bold; display: block; margin-top: 1rem; text-align: left; }
        input {
            width: 100%;
            padding: 10px;
            margin-top: 0.5rem;
            border: 1px solid #ccc;
            border-radius: 8px;
        }
        button {
            margin-top: 1.5rem;
            padding: 10px;
            width: 100%;
            background: #dd2476;
            border: none;
            border-radius: 8px;
            color: #fff;
            font-size: 1rem;
            cursor: pointer;
            transition: 0.3s;
        }
        button:hover { background: #b81d5f; }
        p { margin-top: 1rem; }
        a { color: #dd2476; text-decoration: none; }
        a:hover { text-decoration: underline; }
        .error { color: red; font-size: 0.9rem; margin-bottom: 1rem; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Login</h1>

        @if(session('error'))
            <div class="error">{{ session('error') }}</div>
        @endif

        <form method="POST" action="{{ url('/login') }}">
            @csrf
            <label>Email:</label>
            <input type="email" name="email" required>

            <label>Contraseña:</label>
            <input type="password" name="password" required>

            <button type="submit">Iniciar Sesión</button>
        </form>

        <p>¿No tienes cuenta? <a href="{{ url('/registro') }}">Regístrate</a></p>
    </div>
</body>
</html>
