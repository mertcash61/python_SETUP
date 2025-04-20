<?php

use Illuminate\Support\Facades\Route;

// Dil değişikliği için route
Route::get('/lang/{lang}', function ($lang) {
    // Desteklenen diller
    $supportedLanguages = ['en', 'de', 'es', 'fr'];

    // Geçerli dil kontrolü
    if (in_array($lang, $supportedLanguages)) {
        session(['applocale' => $lang]); // Seçilen dili oturumda sakla
        return redirect()->back()->with('success', 'Dil başarıyla değiştirildi.'); // Başarı mesajı ile yönlendir
    } else {
        return redirect()->back()->with('error', 'Geçersiz dil seçimi.'); // Hata mesajı ile yönlendir
    }
});

// Diğer route'larınızı buraya ekleyebilirsiniz
