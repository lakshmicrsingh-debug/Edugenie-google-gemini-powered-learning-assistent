const task = document.getElementById('task');
const input = document.getElementById('input-text');
const dynamic = document.getElementById('dynamic-fields');
const submit = document.getElementById('submit-btn');
const statusEl = document.getElementById('status');
const result = document.getElementById('result');
const copyBtn = document.getElementById('copy-btn');

const placeholders = {
  qa: 'Example: Which is the largest ocean?',
  explain: 'Example: Explain photosynthesis for a beginner.',
  quiz: 'Paste a passage or topic here to create multiple-choice questions.',
  summarize: 'Paste a long educational passage here.',
  learn: 'Example: SQL'
};

function renderFields() {
  input.placeholder = placeholders[task.value];
  if (task.value === 'quiz') {
    dynamic.innerHTML = `
      <div class="dynamic">
        <div><label for="count">Number of questions</label><input id="count" type="number" min="1" max="10" value="3"></div>
      </div>`;
  } else if (task.value === 'learn') {
    dynamic.innerHTML = `
      <div class="dynamic">
        <div><label for="level">Learner level</label><select id="level"><option>beginner</option><option>intermediate</option><option>advanced</option></select></div>
        <div><label for="hours">Hours per week</label><input id="hours" type="number" min="1" max="40" value="5"></div>
      </div>`;
  } else {
    dynamic.innerHTML = '';
  }
}

task.addEventListener('change', renderFields);
renderFields();

function showQuiz(data) {
  result.classList.remove('empty');
  result.innerHTML = data.questions.map((q, i) => `
    <article class="quiz-question">
      <h3>${i + 1}. ${escapeHtml(q.question)}</h3>
      ${q.options.map((option, n) => `<div class="quiz-option"><strong>${String.fromCharCode(65+n)}.</strong> ${escapeHtml(option)}</div>`).join('')}
      <div class="quiz-answer"><strong>Correct answer:</strong> ${escapeHtml(q.correct_answer)}<br><strong>Why:</strong> ${escapeHtml(q.explanation)}</div>
    </article>`).join('');
}

function escapeHtml(value) {
  return String(value).replace(/[&<>'"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));
}

function showText(text) {
  result.classList.remove('empty');
  result.textContent = text;
}

submit.addEventListener('click', async () => {
  const text = input.value.trim();
  if (!text) {
    statusEl.textContent = 'Please enter something first.';
    statusEl.className = 'status error';
    return;
  }

  let endpoint;
  let body;
  if (task.value === 'qa') {
    endpoint = '/qa'; body = { text };
  } else if (task.value === 'explain') {
    endpoint = '/explain'; body = { text };
  } else if (task.value === 'summarize') {
    endpoint = '/summarize'; body = { text };
  } else if (task.value === 'quiz') {
    endpoint = '/quiz'; body = { text, count: Number(document.getElementById('count').value) };
  } else {
    endpoint = '/learn/recommendations'; body = {
      topic: text,
      level: document.getElementById('level').value,
      hours_per_week: Number(document.getElementById('hours').value)
    };
  }

  submit.disabled = true;
  statusEl.className = 'status';
  statusEl.textContent = 'Thinking…';
  copyBtn.hidden = true;

  try {
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || 'Request failed.');
    if (task.value === 'quiz') showQuiz(data);
    else showText(data.result);
    copyBtn.hidden = false;
    statusEl.textContent = 'Completed.';
  } catch (error) {
    result.classList.add('empty');
    result.textContent = error.message;
    statusEl.className = 'status error';
    statusEl.textContent = 'Could not complete the request.';
  } finally {
    submit.disabled = false;
  }
});

copyBtn.addEventListener('click', async () => {
  await navigator.clipboard.writeText(result.innerText);
  statusEl.textContent = 'Copied to clipboard.';
});
