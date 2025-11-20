document.addEventListener('DOMContentLoaded', function() {
    const chatBox = document.getElementById('chat-box');
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user_input');
    const nextButton = document.getElementById('next')
    const chatUrl = chatForm.dataset.url;
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    let latesNextQuestion = null;

    function appendMessage(sender, text='', isLoading=false) {
        const wrapper = document.createElement('div');
        wrapper.classList.add('mb-3', 'd-flex');

        let content = text;
        if (isLoading) content ='...';

        if (sender === 'AI') {
            wrapper.classList.add('justify-content-start');
            wrapper.innerHTML = `
                <div class='text-start d-flex flex-column'>
                    <span class='badge bg-success mb-1'>AI</span>
                    <div class='message bg-white border p-2 rounded'>${content}</div>
                </div>`;
        } else {
            wrapper.classList.add('justify-content-end');
            wrapper.innerHTML =`
                <div class='text-end d-flex flex-column'>
                    <span class='badge bg-primary mb-1'>You</span>
                    <div class='message bg-light border p-2 rounded'>${content}</div>
                </div>`;
        }

        chatBox.appendChild(wrapper);
        chatBox.scrollTop = chatBox.scrollHeight;
        return wrapper.querySelector('.message')
    }

    chatForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const userMessage = userInput.value.trim();
        if (!userMessage) return;

        appendMessage('You', userMessage);
        userInput.value = ''

        const aiContainer = appendMessage('AI', '', true);

        fetch(chatUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({ user_input: userMessage })
        })
        .then(response => response.json())
        .then(data => {
            aiContainer.innerHTML = `
                <strong>Score:</strong> ${data.score}<br>
                <strong>Explanation:</strong> ${data.explanation}
            `;

            latesNextQuestion = data.next_question;

            chatBox.scrollTop = chatBox.scrollHeight;
        })
        .catch(err => {
            aiContainer.innerHTML = 'An error has occurred.';
            console.error('Error: ', err);
        });
    });
    nextButton.addEventListener('click', () => {
        if (latesNextQuestion) {
            appendMessage('AI', latesNextQuestion);
            latesNextQuestion = null;
        }
    });
});
