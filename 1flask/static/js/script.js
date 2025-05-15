document.addEventListener('DOMContentLoaded', function() {
    console.log("Page Loaded: Adding greeting message.");
    addGreeting();
    attachButtonListeners();  // 페이지 로드 시 처음에 버튼에 리스너를 추가
    setupInfoToggleButton(); // 인포추가
});

// 사용자 입력을 표준화하는 함수
function standardizeInput(input) {
    input = input.toLowerCase();  // 소문자로 변환
    if (input.includes('코드')) {
        return '질병 코드 안내';
    } else if (input.includes('절차')) {
        return '산재 신청 절차';
    } else if (input.includes('등급')) {
        return '장해 등급기준';
    }
    
    return input;  // 변경하지 않고 반환
}

document.getElementById('chatForm').addEventListener('submit', function(event) {
    event.preventDefault();  // 폼의 기본 동작(새로고침)을 방지
    console.log("Form submitted.");

    const messageInput = document.getElementById('messageInput');
    const message = messageInput.value.trim();

    if (message === '') {
        console.log("Empty message. Aborting submission.");
        return;  // 빈 메시지 전송 방지
    }

    addMessageToChat('sent', message);
    messageInput.value = '';  // 입력 필드 초기화
    console.log("User message added to chat.");

    messageInput.blur();  // 입력 필드에서 포커스를 제거하여 키보드를 숨김

    const loadingMessageId = addLoadingDots();
    console.log("Loading dots added to chat with ID:", loadingMessageId);

    const matchedButton = findMatchingButton(message);
    if (matchedButton) {
        processButtonClick(matchedButton, loadingMessageId);
    } else {
        // 사용자 입력을 표준화
        const standardizedMessage = standardizeInput(message);

        fetch('/query/NORMAL', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query: standardizedMessage })  // 'Query' 키로 메시지를 서버에 전송
        })
        .then(response => {
            console.log("Received response from server.");
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();  // JSON 형식으로 응답 받기
        })
        .then(data => {
            // console.log('Received data:', data);  // 응답 데이터 콘솔에 출력

            const updatedMessageType = 'received';  // 메시지 타입을 "received"로 설정

            const intentToButtonMap = {
                '질병코드안내': '질병코드안내',
                '산재신청절차': '산재신청절차',
                '보상금종류안내': '보상금종류안내',
                '장해등급기준': '장해등급기준',
                '자주묻는질문': '자주묻는질문'
            };

            const matchedIntnet = intentToButtonMap[data.Intent];

            if (matchedIntnet) {
                updateMessageContent(loadingMessageId, data.Answer, updatedMessageType);
                processButtonClick(matchedIntnet, loadingMessageId);

            } else {
                updateMessageContent(loadingMessageId, data['Answer'] || 'No response from bot', updatedMessageType);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            updateMessageContent(loadingMessageId, 'Error: Unable to get response from server.', 'received');
        });
    }
});


function addGreeting() {
    const chatBody = document.getElementById('chatBody');
    const greetingElement = document.createElement('div');
    greetingElement.className = 'chat-message received greeting fade-in';  // 애니메이션 클래스 추가
    greetingElement.innerHTML = `
    <img src="/static/images/bear_icon.png" alt="워크내비 챗봇" class="chatbot-avatar">
    <p>
        안녕하세요! 👷‍♂️ <strong>산재 보상 챗봇 워크내비</strong>입니다.<br><br>
        근로자의 산재 관련 궁금증을 빠르게 해결해드립니다.<br><br>
        아래 항목 중 원하시는 주제를 선택해주세요!<br><br>
        <a href="#" class="startfunction-button">🩺 <span>질병 코드 안내</span></a>
        <a href="#" class="startfunction-button">🧾 <span>산재 신청 절차</span></a>
        <a href="#" class="startfunction-button">💰 <span>보상금 종류 안내</span></a>
        <a href="#" class="startfunction-button">📋 <span>장해등급 기준</span></a>
        <a href="#" class="startfunction-button">❓ <span>자주 묻는 질문</span></a>
    </p>
`;

    chatBody.appendChild(greetingElement);
    scrollToBottom();  // 최신 메시지로 스크롤 이동

    attachButtonListeners();
    console.log("Greeting message added and button listeners attached.");
}

function attachButtonListeners() {
    document.querySelectorAll('.startfunction-button').forEach(button => {
        button.removeEventListener('click', handleButtonClick);  // 기존 이벤트 리스너 제거 (중복 방지)
        button.addEventListener('click', handleButtonClick);  // 새로운 이벤트 리스너 추가
    });

    document.querySelectorAll('.response-button').forEach(button => {
        button.removeEventListener('click', handleButtonClick);  // 기존 이벤트 리스너 제거 (중복 방지)
        button.addEventListener('click', handleButtonClick);  // 새로운 이벤트 리스너 추가
    });
}

function handleButtonClick(event) {
    event.preventDefault();  // 기본 동작 방지

    const buttonText = this.querySelector('span').innerText.trim();
    console.log('Button clicked:', buttonText);

    // 링크 연결 처리
    const url = this.getAttribute('href');
    if (url !== '#' && url !== null) {
        window.location.href = url;  // URL이 있는 경우 링크로 이동
        return;
    }

    addMessageToChat('sent', buttonText);
    const loadingMessageId = addLoadingDots();  // 로딩 도트 추가

    processButtonClick(buttonText, loadingMessageId);
}

function sendMessageToServer(message, loadingMessageId) {
    fetch('/query/NORMAL', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ query: message })
    })
    .then(response => response.json())
    .then(data => {
        updateMessageContent(loadingMessageId, data.Answer || 'No response from server', 'received');
        console.log('Message sent to server:', message);
    })
    .catch(error => {
        console.error('Error sending message to server:', error);
        updateMessageContent(loadingMessageId, 'Error: Unable to get response from server.', 'received');
    });
}

function processButtonClick(buttonText, loadingMessageId) {
    fetch('/buttons/handle-button-click', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ buttonTitle: buttonText })
    })
    .then(response => response.json())
    .then(data => {
        updateMessageContent(loadingMessageId, data.message, 'received');
        updateChatWithResponse(data.message, data.buttons);
    })
    .catch(error => {
        console.error('Error:', error);
        updateMessageContent(loadingMessageId, 'Error: Unable to get response from server.', 'received');
    });
}

function updateMessageContent(messageId, newContent, type = 'received') {
    console.log(`Attempting to update message with ID: ${messageId}`);

    const messageElement = document.getElementById(messageId);
    if (messageElement) {
        const pElement = messageElement.querySelector('p');
        if (pElement) {
            const formattedContent = newContent.replace(/\n/g, '<br>');
            pElement.innerHTML = formattedContent;
            messageElement.className = `chat-message ${type} fade-in`; // 애니메이션 클래스 추가
            scrollToBottom();  // 최신 메시지로 스크롤 이동
            console.log(`Successfully updated message content for ID: ${messageId}`);
        } else {
            console.error(`pElement not found in message element with ID: ${messageId}`);
        }
    } else {
        console.error(`Message element not found with ID: ${messageId}`);
    }
}

function updateChatWithResponse(message, buttons) {
    const chatBody = document.getElementById('chatBody');

    if (buttons.length > 0) {
        const lastMessageElement = chatBody.lastElementChild; // 가장 최근 메시지 요소 가져오기
        const pElement = lastMessageElement.querySelector('p'); // 기존의 <p> 요소 찾기

        if (pElement) {
            buttons.forEach(button => {
                // 버튼에 링크를 포함하여 response-button으로 생성
                pElement.innerHTML += `<br><a href="${button.url}" target="_blank" class="response-button"><span>${button.text}</span></a>`;
            });

            console.log('Buttons added to last message:', lastMessageElement.innerHTML);
        } else {
            console.error('No <p> element found in the last message element.');
        }

        scrollToBottom();  // 최신 메시지로 스크롤 이동
        attachButtonListeners(); // 새로 생성된 버튼들에 대한 이벤트 리스너 추가
    }
}

function addMessageToChat(type, message) {
    const chatBody = document.getElementById('chatBody');
    const messageElement = document.createElement('div');
    const messageId = `msg-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    messageElement.className = `chat-message ${type} fade-in`; // 애니메이션 클래스 추가
    messageElement.id = messageId;

    if (type === 'received') {
        messageElement.innerHTML = `
            <img src="static/images/bear_icon.png" alt="Chatbot" class="chatbot-avatar">
            <p>${message}</p>
        `;
    } else {
        messageElement.innerHTML = `<p>${message}</p>`;
    }

    chatBody.appendChild(messageElement);
    scrollToBottom();  // 최신 메시지로 스크롤 이동
    console.log("Message added to chat with ID:", messageId);
    return messageId;  // 메시지 ID 반환
}

function addLoadingDots() {
    const chatBody = document.getElementById('chatBody');
    const loadingElement = document.createElement('div');
    const messageId = `msg-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    loadingElement.className = 'chat-message received fade-in'; // 애니메이션 클래스 추가
    loadingElement.id = messageId;

    loadingElement.innerHTML = `
        <img src="static/images/bear_icon.png" alt="Chatbot" class="chatbot-avatar">
        <p>
            <span class="loading-dots">
                <span></span><span></span><span></span>
            </span>
        </p>
    `;

    chatBody.appendChild(loadingElement);
    scrollToBottom();  // 최신 메시지로 스크롤 이동
    console.log("Loading dots added with ID:", messageId);
    return messageId;  // 메시지 ID 반환
}

function findMatchingButton(message) {
    const buttons = document.querySelectorAll('.startfunction-button span');
    for (let button of buttons) {
        if (button.innerText.trim() === message) {
            return button.parentElement.querySelector('span').innerText.trim();
        }
    }
    return null;
}

// 스크롤을 최신 메시지로 이동시키는 함수
function scrollToBottom() {
    const chatBody = document.getElementById('chatBody');
    chatBody.scrollTop = chatBody.scrollHeight;
}

function setupInfoToggleButton() {
    const infoToggleButton = document.getElementById('infoToggleButton');
    const chatBody = document.getElementById('chatBody');
    const messageInput = document.getElementById('messageInput'); // 사용자 입력 필드
    const sendButton = document.querySelector('.button-container button'); // 전송 버튼
    let infoVisible = false;

    infoToggleButton.addEventListener('click', () => {
        if (!infoVisible) {
            // chatBody를 먼저 부드럽게 숨기기
            chatBody.style.opacity = '0';
            setTimeout(() => {
                chatBody.style.display = 'none'; // 완전히 숨김

                // 안내 사항 요소 생성
                const infoMessage = document.createElement('div');
                infoMessage.id = 'infoMessage';
                infoMessage.className = 'chat-info';
                infoMessage.style.opacity = '0'; // 초기 투명도 설정
                infoMessage.style.transition = 'opacity 0.3s ease'; // 부드러운 전환 효과 추가
                infoMessage.innerHTML = `
                    <h1>안녕하세요!</h1>
                    <h2>산재 보상 챗봇 <strong>‘워크내비’</strong>입니다 👷‍♂️</h2><br>

                    <p>근로자 여러분이 <strong>산재 보상 절차</strong>를 빠르고 쉽게 이해할 수 있도록 돕는 챗봇입니다.</p><br>

                    <h3>🛠️ 주요 기능</h3>
                    <ul>
                        <li>🩺 <strong>질병 코드 안내</strong><br>→ 질병명 또는 증상으로 KCD 코드와 보상 승인 여부 확인</li><br>
                        <li>🧾 <strong>산재 신청 절차</strong><br>→ 재해 발생부터 서류 제출까지 단계별 안내 및 서류 다운로드</li><br>
                        <li>💰 <strong>보상금 종류 안내</strong><br>→ 요양급여, 휴업급여, 장해급여, 간병급여 등의 지급 조건 및 신청 링크 제공</li><br>
                        <li>📋 <strong>장해등급 기준</strong><br>→ 등급 기준표, 판정기준, 장해급여 금액표 안내</li><br>
                        <li>❓ <strong>자주 묻는 질문</strong><br>→ 대표적인 문의사항에 대한 답변 제공</li><br>
                    </ul>

                    <h3>💬 사용 예시</h3>
                    <ul>
                        <li>"허리디스크 산재 되나요?"</li>
                        <li>"산재 신청에 필요한 서류 알려줘"</li>
                        <li>"장해 7급이면 얼마 받아요?"</li>
                        <li>"간병급여 신청 조건이 뭐야?"</li>
                    </ul><br>

                    <p></p>
                `;
                chatBody.parentNode.insertBefore(infoMessage, chatBody.nextSibling);

                // 입력 필드와 전송 버튼 비활성화
                messageInput.disabled = true;
                sendButton.disabled = true;

                // 안내 사항을 부드럽게 표시
                requestAnimationFrame(() => {
                    infoMessage.style.opacity = '1';
                });
            }, 300); // chatBody가 부드럽게 사라질 시간을 줌

            infoVisible = true;
        } else {
            // 안내 사항이 사라지도록 설정
            const infoMessage = document.getElementById('infoMessage');
            if (infoMessage) {
                infoMessage.style.opacity = '0';
                setTimeout(() => {
                    infoMessage.remove(); // 안내 사항이 사라진 후 제거
                    chatBody.style.display = 'block'; // chat-body 다시 표시
                    chatBody.style.opacity = '1'; // 완전히 나타남
                }, 300); // 애니메이션 시간 후 chatBody 표시
            }

            // 입력 필드와 전송 버튼 다시 활성화
            messageInput.disabled = false;
            sendButton.disabled = false;

            infoVisible = false;
        }
    });
};