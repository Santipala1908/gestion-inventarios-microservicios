<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\User;
use App\Models\Role;
use Illuminate\Support\Facades\Hash;

class AuthController extends Controller
{
    public function register(Request $request)
    {
        $validated = $request->validate([
            'name' => 'required|string',
            'email' => 'required|email|unique:users',
            'password' => 'required|min:6',
            'role' => 'required|in:admin,empleado,auditor'
        ]);

        $user = User::create([
            'name' => $validated['name'],
            'email' => $validated['email'],
            'password' => Hash::make($validated['password']),
        ]);

        $role = Role::where('name', $validated['role'])->first();
        $user->roles()->attach($role->id);

        $token = $user->createToken('auth_token')->plainTextToken;

        return response()->json(['user' => $user->load('roles'), 'token' => $token]);
    }

    public function login(Request $request)
    {
        $user = User::where('email', $request->email)->first();

        if (!$user || !Hash::check($request->password, $user->password)) {
            return response()->json(['message' => 'Credenciales incorrectas'], 401);
        }

        $token = $user->createToken('auth_token')->plainTextToken;

        return response()->json(['user' => $user->load('roles'), 'token' => $token]);
    }


     public function logout(Request $request)
    {
        $request->user()->tokens()->delete();
        return response()->json(['message' => 'Sesión cerrada']);
    }

    public function me(Request $request)
    {
        return response()->json($request->user()->load('roles'));
    }
    public function registerWeb(Request $request)
{
    $validated = $request->validate([
        'name' => 'required|string',
        'email' => 'required|email|unique:users',
        'password' => 'required|min:6',
        'role' => 'required|in:admin,empleado,auditor'
    ]);

    $user = User::create([
        'name' => $validated['name'],
        'email' => $validated['email'],
        'password' => Hash::make($validated['password']),
    ]);

    $role = Role::where('name', $validated['role'])->first();
    $user->roles()->attach($role->id);

    // iniciar sesión al registrar
    auth()->login($user);

    return redirect('/dashboard')->with('success', 'Usuario registrado con éxito');
}

public function loginWeb(Request $request)
{
    $user = User::where('email', $request->email)->first();

    if (!$user || !Hash::check($request->password, $user->password)) {
        return back()->with('error', 'Credenciales incorrectas');
    }

    // iniciar sesión
    auth()->login($user);

    return redirect('/dashboard')->with('success', 'Bienvenido '.$user->name);
}

public function logoutWeb(Request $request)
{
    auth()->logout();
    return redirect('/login')->with('success', 'Sesión cerrada correctamente');
}

}
