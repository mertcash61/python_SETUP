<!DOCTYPE html>
<html lang="{{ app()->getLocale() }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ __('messages.welcome') }}</title>
    <link rel="stylesheet" href="{{ asset('css/style.css') }}">
</head>
<body>
    <header>
        <h1>{{ __('messages.welcome') }}</h1>
        <div class="version">Versiyon 1.0.2</div>
        <div class="theme-selector">
            <label for="theme">{{ __('messages.language') }}:</label>
            <select id="theme" onchange="changeLanguage(this.value)">
                <option value="en" {{ app()->getLocale() == 'en' ? 'selected' : '' }}>English</option>
                <option value="de" {{ app()->getLocale() == 'de' ? 'selected' : '' }}>Deutsch</option>
            </select>
        </div>
    </header>
    
    <main>
        <div class="setup-container">
            <h2>{{ __('messages.settings') }}</h2>
            <form id="settingsForm">
                <label for="apiUrl">{{ __('messages.api_url') }}:</label>
                <input type="text" id="apiUrl" name="apiUrl" required placeholder="https://api.example.com">
                <button type="submit">{{ __('messages.save') }}</button>
            </form>
        </div>
    </main>
    
    <footer>
        <p>&copy; 2023 Setup Uygulaması | Tüm Hakları Saklıdır</p>
    </footer>
    
    <script>
        function changeLanguage(lang) {
            window.location.href = '/lang/' + lang; // Dili değiştirmek için yönlendirme
        }
    </script>
</body>
</html>
