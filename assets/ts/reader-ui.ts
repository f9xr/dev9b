/* ------------------------------------------------------------------ */
/* Reading progress bar + back-to-top button (article pages)           */
/* ------------------------------------------------------------------ */

function initProgress(): void {
    const bar = document.querySelector<HTMLElement>('.read-progress-bar');
    if (!bar) return;

    let ticking = false;
    const update = (): void => {
        const doc = document.documentElement;
        const max = doc.scrollHeight - doc.clientHeight;
        const progress = max > 0 ? Math.min(1, doc.scrollTop / max) : 0;
        bar.style.transform = `scaleX(${progress.toFixed(4)})`;
        ticking = false;
    };

    const requestUpdate = (): void => {
        if (!ticking) {
            ticking = true;
            requestAnimationFrame(update);
        }
    };

    window.addEventListener('scroll', requestUpdate, { passive: true });
    window.addEventListener('resize', requestUpdate, { passive: true });
    update();
}

function initBackToTop(): void {
    const btn = document.querySelector<HTMLElement>('[data-back-to-top]');
    if (!btn) return;

    const SHOW_AFTER = 400;
    const toggle = (): void => {
        btn.hidden = document.documentElement.scrollTop < SHOW_AFTER;
    };

    window.addEventListener('scroll', toggle, { passive: true });
    btn.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
    toggle();
}

export function initReaderUi(): void {
    initProgress();
    initBackToTop();
}
