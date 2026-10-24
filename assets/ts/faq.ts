/* ------------------------------------------------------------------ */
/* Collapsible FAQ sections (article pages)                            */
/* ------------------------------------------------------------------ */

type FaqGroup = {
    heading: HTMLHeadingElement;
    nodes: HTMLElement[];
};

function getArticleContent(): HTMLElement | null {
    const content = document.querySelector<HTMLElement>('.article-content');
    return content;
}

function isFaqHeading(heading: HTMLElement): boolean {
    const text = (heading.textContent ?? '').replace(/\s+/g, ' ').trim();
    return heading.id === 'faq'
        || /^faq$/i.test(text)
        || /frequently asked questions/i.test(text);
}

function collectGroups(faqHeading: HTMLElement): FaqGroup[] {
    const groups: FaqGroup[] = [];
    let current: FaqGroup | null = null;
    let sibling = faqHeading.nextElementSibling;

    while (sibling) {
        if (sibling instanceof HTMLHeadingElement && sibling.tagName === 'H2') break;

        if (sibling instanceof HTMLHeadingElement && sibling.tagName === 'H3') {
            current = { heading: sibling, nodes: [] };
            groups.push(current);
        } else if (current && sibling instanceof HTMLElement) {
            current.nodes.push(sibling);
        }

        sibling = sibling.nextElementSibling;
    }

    return groups;
}

function buildDetails(group: FaqGroup): HTMLDetailsElement {
    const details = document.createElement('details');
    details.className = 'faq-item';
    details.dataset.faqEnhanced = 'true';
    if (group.heading.id) details.id = group.heading.id;

    const summary = document.createElement('summary');
    summary.className = 'faq-question';
    while (group.heading.firstChild) {
        summary.appendChild(group.heading.firstChild);
    }

    const answer = document.createElement('div');
    answer.className = 'faq-answer';
    for (const node of group.nodes) {
        answer.appendChild(node);
    }

    details.append(summary, answer);
    return details;
}

function openLinkedQuestion(): void {
    if (!window.location.hash) return;

    let id = window.location.hash.slice(1);
    try {
        id = decodeURIComponent(id);
    } catch {
        /* keep the raw fragment */
    }

    const target = document.getElementById(id);
    if (target instanceof HTMLDetailsElement && target.classList.contains('faq-item')) {
        target.open = true;
    }
}

function enhanceFaq(): void {
    const content = getArticleContent();
    if (!content) return;

    const headings = Array.from(content.querySelectorAll<HTMLElement>('h2'));
    const faqHeading = headings.find(isFaqHeading);
    if (!faqHeading) return;

    const groups = collectGroups(faqHeading);
    if (groups.length === 0) return;

    faqHeading.classList.add('faq-heading');

    for (const group of groups) {
        group.heading.replaceWith(buildDetails(group));
    }

    openLinkedQuestion();
    window.addEventListener('hashchange', openLinkedQuestion);
}

export function initFaqAccordion(): void {
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', enhanceFaq, { once: true });
    } else {
        enhanceFaq();
    }
}
