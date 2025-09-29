<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Registro de Usuario</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #6a11cb, #2575fc);
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
        input, select {
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
            background: #2575fc;
            border: none;
            border-radius: 8px;
            color: #fff;
            font-size: 1rem;
            cursor: pointer;
            transition: 0.3s;
        }
        button:hover { background: #1a5ed9; }
        p { margin-top: 1rem; }
        a { color: #2575fc; text-decoration: none; }
        a:hover { text-decoration: underline; }
        .error { color: red; font-size: 0.9rem; margin-bottom: 1rem; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Crear Usuario</h1>

        @if ($errors->any())
            <div class="error">
                <ul>
                    @foreach ($errors->all() as $error)
                        <li>{{ $error }}</li>
                    @endforeach
                </ul>
            </div>
        @endif

        <form method="POST" action="{{ url('/registro') }}">
            @csrf
            <label>Nombre:</label>
            <input type="text" name="name" required>

            <label>Email:</label>
            <input type="email" name="email" required>

            <label>Contraseña:</label>
            <input type="password" name="password" required>

            <label>Rol:</label>
            <select name="role" required>
                <option value="admin">Admin</option>
                <option value="empleado">Empleado</option>
                <option value="auditor">Auditor</option>
            </select>

            <button type="submit">Registrar</button>
        </form>

        <p>¿Ya tienes cuenta? <a href="{{ url('/login') }}">Inicia sesión</a></p>
    </div>
</body>
</html>
