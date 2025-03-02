let conversationId = Date.now(); // Unique ID for each session

document.getElementById('submit-btn').addEventListener('click', async () => {
  const codeInput = document.getElementById('code');
  const resultsDiv = document.getElementById('results');
  const errorDiv = document.getElementById('error');
  const responseDiv = document.getElementById('response');
  const loadingDiv = document.getElementById('loading');
  const followUpSection = document.getElementById('follow-up-section');

  // Clear previous results and errors
  resultsDiv.classList.add('hidden');
  errorDiv.classList.add('hidden');
  responseDiv.textContent = '';

  const codeSnippet = codeInput.value.trim();
  if (!codeSnippet) {
    errorDiv.textContent = 'Please enter a code snippet.';
    errorDiv.classList.remove('hidden');
    return;
  }

  try {
    // Show loading state
    loadingDiv.classList.remove('hidden');
    document.getElementById('submit-btn').disabled = true;

    // Fetch initial explanation
    const response = await fetch('http://127.0.0.1:5000/explain-code', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ conversation_id: conversationId, code: codeSnippet }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json();
    if (data.explanation) {
      // Display explanation
      resultsDiv.classList.remove('hidden');
      loadingDiv.classList.add('hidden');
      responseDiv.textContent = data.explanation;
      followUpSection.classList.remove('hidden'); // Enable follow-up section
    } else {
      throw new Error(data.error || 'An error occurred while generating the explanation.');
    }
  } catch (err) {
    loadingDiv.classList.add('hidden');
    errorDiv.textContent = err.message || 'Failed to connect to the server. Please try again later.';
    errorDiv.classList.remove('hidden');
  } finally {
    // Reset button state
    document.getElementById('submit-btn').disabled = false;
  }
});

document.getElementById('follow-up-btn').addEventListener('click', async () => {
  const followUpQuestion = document.getElementById('follow-up-question');
  const resultsDiv = document.getElementById('results');
  const errorDiv = document.getElementById('error');
  const responseDiv = document.getElementById('response');
  const loadingDiv = document.getElementById('loading');

  // Clear previous errors
  errorDiv.classList.add('hidden');

  const question = followUpQuestion.value.trim();
  if (!question) {
    errorDiv.textContent = 'Please enter a follow-up question.';
    errorDiv.classList.remove('hidden');
    return;
  }

  try {
    // Show loading state
    loadingDiv.classList.remove('hidden');
    document.getElementById('follow-up-btn').disabled = true;

    // Fetch follow-up response
    const response = await fetch('http://127.0.0.1:5000/follow-up', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ conversation_id: conversationId, question }),
    });

    const data = await response.json();
    if (response.ok) {
      // Display response
      resultsDiv.classList.remove('hidden');
      loadingDiv.classList.add('hidden');
      responseDiv.textContent += `\n\nQ: ${question}\nA: ${data.response}`;
      followUpQuestion.value = ''; // Clear input
    } else {
      // Display error
      loadingDiv.classList.add('hidden');
      errorDiv.textContent = data.error || 'An error occurred while generating the response.';
      errorDiv.classList.remove('hidden');
    }
  } catch (err) {
    loadingDiv.classList.add('hidden');
    errorDiv.textContent = 'Failed to connect to the server. Please try again later.';
    errorDiv.classList.remove('hidden');
  } finally {
    // Reset button state
    document.getElementById('follow-up-btn').disabled = false;
  }
});