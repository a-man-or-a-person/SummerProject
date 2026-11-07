document.addEventListener('DOMContentLoaded', () => {
    // Получаем элементы
    const longUrlInput = document.getElementById('longUrl');
    const shortenBtn = document.getElementById('shortenBtn');
    const resultDiv = document.getElementById('result');
    const shortUrlLink = document.getElementById('shortUrl');
    const copyBtn = document.getElementById('copyBtn');
    const errorDiv = document.getElementById('error');
    const loader = document.getElementById('loader');

    // Проверка элементов
    if (!longUrlInput || !shortenBtn || !resultDiv || !shortUrlLink || !copyBtn || !errorDiv || !loader) {
        console.error('Error: Some elements are missing');
        errorDiv.textContent = 'Configuration error. Please reload the page.';
        errorDiv.classList.remove('hidden');
        return;
    }

    // Обработчики событий
    shortenBtn.addEventListener('click', shortenUrl);
    copyBtn.addEventListener('click', copyToClipboard);

    // Функция сокращения URL
    async function shortenUrl() {
        // Сброс состояния
        resultDiv.classList.add('hidden');
        errorDiv.classList.add('hidden');
        errorDiv.textContent = '';

        const longUrl = longUrlInput.value.trim();

        // Валидация URL
        if (!longUrl) {
            showError('Please enter a URL');
            return;
        }

        if (!isValidUrl(longUrl)) {
            showError('Please enter a valid URL (e.g., https://example.com)');
            return;
        }

        try {
            // Показать лоадер
            loader.style.display = 'block';
            shortenBtn.disabled = true;
            shortenBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';

            // Отправка запроса
            const response = await fetch('http://localhost:8003/get_short', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ url: longUrl })
            });

            // Обработка ответа
            const contentType = response.headers.get('content-type');
            let responseData;

            if (contentType && contentType.includes('application/json')) {
                responseData = await response.json();
            } else {
                const text = await response.text();
                throw new Error(`Unexpected response: ${text}`);
            }

            if (response.ok) {
                // Успешный ответ
                shortUrlLink.textContent = responseData.short_url;
                shortUrlLink.href = responseData.short_url;
                resultDiv.classList.remove('hidden');
            } else {
                // Обработка ошибки
                throw new Error(responseData.detail || responseData.error || `Server error: ${response.status}`);
            }

        } catch (error) {
            console.error('Error:', error);
            showError(error.message || 'An error occurred. Please try again.');
        } finally {
            // Скрыть лоадер
            loader.style.display = 'none';
            shortenBtn.disabled = false;
            shortenBtn.innerHTML = '<i class="fas fa-scissors"></i> Shorten URL';
        }
    }

    // Функция копирования
    function copyToClipboard() {
        navigator.clipboard.writeText(shortUrlLink.href)
            .then(() => {
                const originalIcon = copyBtn.innerHTML;
                copyBtn.innerHTML = '<i class="fas fa-check"></i> Copied!';
                setTimeout(() => {
                    copyBtn.innerHTML = originalIcon;
                }, 2000);
            })
            .catch(err => {
                showError('Failed to copy: ' + err.message);
            });
    }

    // Показать ошибку
    function showError(message) {
        errorDiv.textContent = message;
        errorDiv.classList.remove('hidden');

        // Автоскрытие через 5 секунд
        setTimeout(() => {
            errorDiv.classList.add('hidden');
        }, 5000);
    }

    // Проверка валидности URL
    function isValidUrl(url) {
        try {
            new URL(url);
            return true;
        } catch {
            return false;
        }
    }

    // Фокус на поле ввода при загрузке
    longUrlInput.focus();

    // Обработка нажатия Enter
    longUrlInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            shortenBtn.click();
        }
    });
});