// Read-only freshness labels. Publication/source times stay unchanged.
(() => {
  const formatter = new Intl.DateTimeFormat('en-CA', {
    timeZone: 'Europe/Istanbul', year: 'numeric', month: '2-digit', day: '2-digit'
  });
  function update() {
    const now = new Date();
    const parts = Object.fromEntries(formatter.formatToParts(now).map(p => [p.type, p.value]));
    document.querySelectorAll('.freshness li[data-hour]').forEach(row => {
      let expected = new Date(`${parts.year}-${parts.month}-${parts.day}T${row.dataset.hour.padStart(2, '0')}:00:00+03:00`);
      if (expected > now) expected = new Date(expected.getTime() - 86400000);
      const slot = new Date(row.dataset.slot);
      const ready = !Number.isNaN(slot.getTime()) && slot >= expected;
      row.querySelector('.status').textContent = ready ? 'Son bülten hazır' : 'Yeni bülten bekleniyor';
    });
  }
  update();
  setInterval(update, 60000);
})();
