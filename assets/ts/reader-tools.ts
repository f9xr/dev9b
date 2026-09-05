const STORAGE_KEY = 'dev9b:reader:font-scale';
const FONT_MIN = 0.8;
const FONT_MAX = 1.5;
const FONT_STEP = 0.05;

const clamp = (value: number): number =>
    Math.min(FONT_MAX, Math.max(FONT_MIN, Math.round(value * 100) / 100));

function readStoredScale(): number {
    try {
        const raw = localStorage.getItem(STORAGE_KEY);
        if (raw !== null) {
            const parsed = parseFloat(raw);
            if (!Number.isNaN(parsed)) return clamp(parsed);
        }
    } catch {
        /* private mode / storage disabled — keep default */
    }
    return 1;
}

function storeScale(scale: number): void {
    try {
        localStorage.setItem(STORAGE_KEY, scale.toString());
    } catch {
        /* ignore write failures */
    }
}

function getArticleContent(): HTMLElement | null {
    const content = document.querySelector('.article-content');
    return content instanceof HTMLElement ? content : null;
}

/* ------------------------------------------------------------------ */
/* Font size controls (persisted per reader)                           */
/* ------------------------------------------------------------------ */
function initFontSize(): void {
    const content = getArticleContent();
    if (!content) return;

    const applyScale = (scale: number): void => {
        content.style.setProperty('--reader-font-scale', scale.toFixed(2));
        storeScale(scale);
    };

    applyScale(readStoredScale());

    document.querySelectorAll<HTMLElement>('[data-font-scale]').forEach((button) => {
        button.addEventListener('click', () => {
            const delta = parseInt(button.dataset.fontScale || '0', 10);
            if (Number.isNaN(delta) || delta === 0) return;
            const current = readStoredScale();
            applyScale(clamp(current + delta * FONT_STEP));
        });
    });

    document.querySelectorAll<HTMLElement>('[data-font-reset]').forEach((button) => {
        button.addEventListener('click', () => applyScale(1));
    });
}

/* ------------------------------------------------------------------ */
/* Text-to-speech "Listen" (browser Web Speech API, no server)         */
/* ------------------------------------------------------------------ */
type TtsState = 'idle' | 'playing' | 'paused';

let ttsSentences: string[] = [];
let ttsIndex = 0;
let ttsState: TtsState = 'idle';
let ttsPlayBtn: HTMLElement | null = null;
let ttsLabel: HTMLElement | null = null;
let ttsStopBtn: HTMLElement | null = null;
let ttsVoiceLang = '';

function splitSentences(text: string): string[] {
    return text
        .replace(/\s+/g, ' ')
        .split(/[.!?…]+(?=\s|$)/)
        .map((part) => part.trim())
        .filter((part) => part.length > 0);
}

function ttsSpeakNext(): void {
    if (ttsIndex >= ttsSentences.length) {
        ttsReset();
        return;
    }

    const utterance = new SpeechSynthesisUtterance(ttsSentences[ttsIndex]);
    if (ttsVoiceLang) utterance.lang = ttsVoiceLang;

    utterance.onend = () => {
        if (ttsState === 'playing') {
            ttsIndex += 1;
            ttsSpeakNext();
        }
    };
    utterance.onerror = () => ttsReset();

    speechSynthesis.speak(utterance);
    ttsState = 'playing';
    updateTtsUi();
}

function ttsReset(): void {
    speechSynthesis.cancel();
    ttsIndex = 0;
    ttsState = 'idle';
    updateTtsUi();
}

function ttsToggle(): void {
    if (ttsState === 'idle') {
        const content = getArticleContent();
        if (!content) return;
        ttsSentences = splitSentences(content.innerText);
        if (ttsSentences.length === 0) return;
        ttsSpeakNext();
    } else if (ttsState === 'paused') {
        speechSynthesis.resume();
        ttsState = 'playing';
        updateTtsUi();
    } else {
        speechSynthesis.pause();
        ttsState = 'paused';
        updateTtsUi();
    }
}

function updateTtsUi(): void {
    if (!ttsPlayBtn || !ttsLabel) return;
    ttsPlayBtn.setAttribute('aria-pressed', ttsState !== 'idle' ? 'true' : 'false');
    ttsPlayBtn.classList.toggle('is-active', ttsState !== 'idle');
    if (ttsState === 'playing') ttsLabel.textContent = 'Pause';
    else if (ttsState === 'paused') ttsLabel.textContent = 'Resume';
    else ttsLabel.textContent = 'Listen';
}

function initTts(): void {
    ttsPlayBtn = document.querySelector('[data-tts-play]');
    ttsLabel = document.querySelector('[data-tts-label]');
    ttsStopBtn = document.querySelector('[data-tts-stop]');

    const unsupported = typeof speechSynthesis === 'undefined';
    if (!ttsPlayBtn || unsupported) {
        document.querySelectorAll('[data-tts]').forEach((el) => el.classList.add('reading-hidden'));
        return;
    }

    ttsVoiceLang = document.documentElement.lang || 'en-US';

    ttsPlayBtn.addEventListener('click', ttsToggle);
    if (ttsStopBtn) {
        ttsStopBtn.addEventListener('click', ttsReset);
    }

    window.addEventListener('beforeunload', () => speechSynthesis.cancel());
    document.addEventListener('visibilitychange', () => {
        if (document.hidden && ttsState !== 'idle') {
            speechSynthesis.pause();
            ttsState = 'paused';
            updateTtsUi();
        }
    });
}

/* ------------------------------------------------------------------ */
/* Sharing: native share, copy link                                    */
/* ------------------------------------------------------------------ */
function initShare(): void {
    const toolbar = document.querySelector<HTMLElement>('[data-share-url]');
    if (!toolbar) return;

    const url = toolbar.dataset.shareUrl || window.location.href;
    const title = toolbar.dataset.shareText || document.title;

    const nativeShare = document.querySelector<HTMLElement>('[data-share-native]');
    if (nativeShare) {
        if (typeof navigator.share === 'function') {
            nativeShare.addEventListener('click', () => {
                navigator.share({ title, url }).catch(() => { /* user cancelled */ });
            });
        } else {
            nativeShare.classList.add('reading-hidden');
        }
    }

    document.querySelectorAll<HTMLElement>('[data-share-copy]').forEach((button) => {
        button.addEventListener('click', async () => {
            const label = button.querySelector('[data-copy-label]');
            try {
                await navigator.clipboard.writeText(url);
                if (label) {
                    const original = label.textContent;
                    label.textContent = button.dataset.copiedText || 'Copied';
                    window.setTimeout(() => {
                        if (label) label.textContent = original;
                    }, 1600);
                }
            } catch {
                /* clipboard unavailable — fall back to prompt */
                try {
                    window.prompt('Copy this link:', url);
                } catch {
                    /* ignore */
                }
            }
        });
    });
}

export function initReaderTools(): void {
    initFontSize();
    initTts();
    initShare();
}