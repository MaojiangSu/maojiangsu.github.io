(() => {
  const button = document.querySelector('[data-project-copy]');
  const code = document.getElementById('project-bibtex');
  const status = document.querySelector('.project-copy-status');
  if (!button || !code || !status) return;
  button.hidden = false;
  button.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(code.textContent);
      status.textContent = 'BibTeX copied to clipboard.';
    } catch {
      const selection = window.getSelection();
      const range = document.createRange();
      range.selectNodeContents(code);
      selection.removeAllRanges();
      selection.addRange(range);
      status.textContent = 'Select and copy the highlighted BibTeX with Ctrl+C or Command+C.';
    }
  });
})();
