async function fetchTasks(){
  const res = await fetch('/api/tasks');
  const tasks = await res.json();
  const container = document.getElementById('tasks');
  if (!Array.isArray(tasks)) { container.textContent = 'Failed to load tasks'; return }
  if (tasks.length === 0) { container.innerHTML = '<p>No tasks yet.</p>'; return }
  const ul = document.createElement('ul');
  tasks.forEach(t => {
    const li = document.createElement('li');
    li.innerHTML = `<strong>${escapeHtml(t.title)}</strong> - ${escapeHtml(t.description || '')} (due: ${escapeHtml(t.due_date || '')}) [${escapeHtml(t.status)}] `;
    const del = document.createElement('button'); del.textContent = 'Delete';
    del.addEventListener('click', async ()=>{
      if (!confirm('Delete this task?')) return;
      const r = await fetch('/api/tasks/' + t.id, {method: 'DELETE'});
      if (r.ok) fetchTasks(); else alert('Delete failed');
    })
    li.appendChild(del);
    ul.appendChild(li);
  })
  container.innerHTML = '';
  container.appendChild(ul);
}

function escapeHtml(s){
  return String(s || '').replace(/[&<>"']/g, function(c){
    const map = {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'};
    return map[c] || c;
  });
}

window.addEventListener('load', ()=>{
  fetchTasks();
});
