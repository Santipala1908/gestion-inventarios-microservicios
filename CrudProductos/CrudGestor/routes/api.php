<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\ProductController;
use App\Models\Product;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application. These
| routes are loaded by the RouteServiceProvider and all of them will
| be assigned to the "api" middleware group. Make something great!
|
*/

Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
    return $request->user();
});
Route::get('/products/exists', function () {
    $sku = request('sku');
    if (!$sku) {
        return response()->json(['error' => 'sku_required'], 422);
    }
    $p = Product::where('sku', $sku)->select('id','sku')->first();
    return response()->json([
        'exists' => (bool)$p,
        'id'     => $p->id  ?? null,
        'sku'    => $p->sku ?? null,
    ]);
});

// Validación por ID
Route::get('/products/{id}/exists', function ($id) {
    $p = Product::select('id','sku')->find($id);
    return response()->json([
        'exists' => (bool)$p,
        'id'     => $p->id  ?? null,
        'sku'    => $p->sku ?? null,
    ]);
});

Route::get('/products', [ProductController::class, 'apiIndex']);
Route::get('/products/{id}', [ProductController::class, 'apiShow']);
Route::post('/products', [ProductController::class, 'apiStore']);
Route::put('/products/{id}', [ProductController::class, 'apiUpdate']);
Route::delete('/products/{id}', [ProductController::class, 'apiDestroy']);

