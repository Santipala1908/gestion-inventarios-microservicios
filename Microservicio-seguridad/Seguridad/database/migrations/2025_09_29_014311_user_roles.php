<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('user_roles', function (Blueprint $table) {
        $table->id();
        
        // Relación con usuarios
        $table->foreignId('user_id')
              ->constrained()
              ->onDelete('cascade');
        
        // Relación con roles
        $table->foreignId('role_id')
              ->constrained()
              ->onDelete('cascade');
        
        $table->timestamps();
    });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        //
    }
};
