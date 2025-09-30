<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Recuperar Contraseña</title>
</head>
<body>
    <h1>Recuperar Contraseña</h1>

    @if(session('success'))
        <p style="color:green">{{ session('success') }}</p>
    @endif

    @if($errors->any())
        <p style="color:red">{{ $errors->first() }}</p>
    @endif

    <form method="POST" action="{{ url('/forgot-password') }}">
        @csrf
        <label>Email:</label>
        <input type="email" name="email" required>
        <button type="submit">Enviar enlace</button>
    </form>
</body>
</html>
