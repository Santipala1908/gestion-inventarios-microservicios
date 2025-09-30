<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Restablecer Contraseña</title>
</head>
<body>
    <h1>Restablecer Contraseña</h1>

    @if($errors->any())
        <p style="color:red">{{ $errors->first() }}</p>
    @endif

    <form method="POST" action="{{ url('/reset-password') }}">
        @csrf
        <input type="hidden" name="token" value="{{ request()->route('token') }}">

        <label>Email:</label>
        <input type="email" name="email" required>

        <label>Nueva Contraseña:</label>
        <input type="password" name="password" required>

        <label>Confirmar Contraseña:</label>
        <input type="password" name="password_confirmation" required>

        <button type="submit">Restablecer</button>
    </form>
</body>
</html>
