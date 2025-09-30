<?php

use Illuminate\Support\Facades\Route;
use Illuminate\Support\Facades\Auth;
use App\Http\Controllers\AuthController;

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider and all of them will
| be assigned to the "web" middleware group. Make something great!
|
*/

Route::get('/', function () {
    return view('welcome');
});
Route::view('/registro', 'auth.register');
Route::view('/login', 'auth.login');

Route::post('/registro', [AuthController::class, 'registerWeb']);
Route::post('/login', [AuthController::class, 'loginWeb']);
Route::post('/logout', [AuthController::class, 'logoutWeb']);

Route::get('/dashboard', function () {
    return view('dashboard');
})->middleware('auth'); 

Route::view('/forgot-password', 'auth.forgot');
Route::post('/forgot-password', [AuthController::class, 'sendResetLink']);

Route::view('/reset-password/{token}', 'auth.reset')->name('password.reset');
Route::post('/reset-password', [AuthController::class, 'resetPassword']);