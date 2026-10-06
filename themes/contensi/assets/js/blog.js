function navToggle() {
  const button = document.getElementById('navToggle');
  const header = document.getElementById('kopf');
  if (!button || !header) return;
  button.addEventListener('click', () => {
    const open = header.classList.toggle('offen');
    button.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
}

function navGroups() {
  const groups = document.querySelectorAll('.nav-gruppe');
  if (!groups.length) return;
  const closeAll = () => groups.forEach((g) => {
    g.classList.remove('offen');
    g.querySelector('.nav-gruppen-knopf').setAttribute('aria-expanded', 'false');
  });
  const openOnly = (group) => {
    closeAll();
    group.classList.add('offen');
    group.querySelector('.nav-gruppen-knopf').setAttribute('aria-expanded', 'true');
  };
  groups.forEach((group) => {
    const button = group.querySelector('.nav-gruppen-knopf');
    button.addEventListener('click', () => {
      if (group.classList.contains('offen')) closeAll(); else openOnly(group);
    });
    group.addEventListener('mouseenter', () => openOnly(group));
    group.addEventListener('mouseleave', () => {
      group.classList.remove('offen');
      button.setAttribute('aria-expanded', 'false');
    });
  });
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.nav-gruppe')) closeAll();
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeAll();
  });
}

function slackDialog() {
  const opener = document.querySelector('[data-open="slackDialog"]');
  const dialog = document.getElementById('slackDialog');
  if (!opener || !dialog) return;
  opener.addEventListener('click', () => dialog.showModal());
  document.getElementById('slackSchliessen').addEventListener('click', () => dialog.close());
  document.getElementById('slackSenden').addEventListener('click', () => {
    const form = document.getElementById('slackForm');
    if (!form.reportValidity()) return;
    const value = (id) => document.getElementById(id).value.trim();
    const phone = value('slackTelefon');
    const body = `Name: ${value('slackName')}\n` +
      `Unternehmen: ${value('slackFirma')}\n` +
      `E-Mail: ${value('slackEmail')}\n` +
      (phone ? `Telefon: ${phone}\n` : '') +
      `Anliegen:\n${value('slackAnliegen')}`;
    const subject = `Slack - Empfang - ${value('slackFirma')}`;
    window.location.href = `mailto:jreincke@contensi.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
  });
}

function escapeHtml(s) {
  return s.replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
}

function highlight(text, term) {
  const i = text.toLowerCase().indexOf(term.toLowerCase());
  if (i === -1) return escapeHtml(text);
  return escapeHtml(text.slice(0, i)) + '<mark>' + escapeHtml(text.slice(i, i + term.length)) +
    '</mark>' + escapeHtml(text.slice(i + term.length));
}

function excerpt(text, term, length) {
  const i = text.toLowerCase().indexOf(term.toLowerCase());
  if (i === -1) return text.slice(0, length);
  const start = Math.max(0, i - 40);
  return (start > 0 ? '… ' : '') + text.slice(start, start + length);
}

function search() {
  const opener = document.getElementById('sucheOeffnen');
  const dialog = document.getElementById('sucheDialog');
  if (!opener || !dialog) return;
  const input = document.getElementById('sucheEingabe');
  const list = document.getElementById('sucheErgebnisse');
  const empty = document.getElementById('sucheLeer');
  let index = null;

  const load = () => {
    index ??= fetch(dialog.dataset.index).then((r) => r.json());
    return index;
  };

  const run = async (term) => {
    list.innerHTML = '';
    if (!term) { empty.hidden = true; return; }
    const t = term.toLowerCase();
    const hits = (await load())
      .filter((p) => p.titel.toLowerCase().includes(t) || p.text.toLowerCase().includes(t))
      .sort((a, b) => Number(!a.titel.toLowerCase().includes(t)) - Number(!b.titel.toLowerCase().includes(t)))
      .slice(0, 12);
    empty.hidden = hits.length !== 0;
    hits.forEach((p, i) => {
      const li = document.createElement('li');
      const snippet = p.text.toLowerCase().includes(t) ? excerpt(p.text, term, 110) : p.text.slice(0, 110);
      li.innerHTML = `<a href="${escapeHtml(p.url)}"${i === 0 ? ' class="aktiv"' : ''}>` +
        `<span class="such-treffer-titel">${highlight(p.titel, term)}</span>` +
        `<span class="such-treffer-text">${highlight(snippet, term)}</span></a>`;
      list.appendChild(li);
    });
  };

  opener.addEventListener('click', () => {
    dialog.showModal();
    input.value = '';
    list.innerHTML = '';
    empty.hidden = true;
    input.focus();
    load();
  });
  document.getElementById('sucheSchliessen').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', (e) => { if (e.target === dialog) dialog.close(); });

  let timer;
  input.addEventListener('input', () => {
    clearTimeout(timer);
    timer = setTimeout(() => run(input.value.trim()), 80);
  });
  input.addEventListener('keydown', (e) => {
    if (e.key !== 'Enter') return;
    const first = list.querySelector('a');
    if (first) window.location.href = first.getAttribute('href');
  });
}

function activeHeading() {
  const links = [...document.querySelectorAll('.inhalt a')];
  const headings = links.map((a) => document.getElementById(decodeURIComponent(a.hash.slice(1))));
  if (!links.length || headings.includes(null)) return;
  let frame = 0;
  const update = () => {
    frame = 0;
    const line = window.innerHeight * 0.3;
    const atEnd = window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 4;
    let current = -1;
    headings.forEach((h, i) => { if (h.getBoundingClientRect().top <= line) current = i; });
    if (atEnd && headings[headings.length - 1].getBoundingClientRect().top < window.innerHeight) current = headings.length - 1;
    links.forEach((a, i) => {
      if (i === current) a.setAttribute('aria-current', 'location'); else a.removeAttribute('aria-current');
    });
  };
  window.addEventListener('scroll', () => { frame ||= requestAnimationFrame(update); }, { passive: true });
  update();
}

navToggle();
navGroups();
slackDialog();
search();
activeHeading();
