(() => {
    document.querySelectorAll('[data-gallery]').forEach((gallery) => {
        const links = Array.from(gallery.querySelectorAll('[data-gallery-image]'));
        const dialog = gallery.querySelector('dialog');
        if (!links.length || typeof dialog.showModal !== 'function') return;

        const preview = dialog.querySelector('[data-gallery-preview]');
        const counter = dialog.querySelector('[data-gallery-counter]');
        const previous = dialog.querySelector('[data-gallery-prev]');
        const next = dialog.querySelector('[data-gallery-next]');
        let current = 0;
        let opener;

        const show = (index) => {
            current = (index + links.length) % links.length;
            preview.src = links[current].href;
            preview.alt = links[current].querySelector('img').alt;
            counter.textContent = `${current + 1} / ${links.length}`;
        };

        previous.hidden = next.hidden = links.length < 2;
        links.forEach((link, index) => {
            link.addEventListener('click', (event) => {
                if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
                event.preventDefault();
                opener = link;
                show(index);
                dialog.showModal();
                document.body.classList.add('gallery-open');
            });
        });
        previous.addEventListener('click', () => show(current - 1));
        next.addEventListener('click', () => show(current + 1));
        dialog.querySelector('[data-gallery-close]').addEventListener('click', () => dialog.close());
        dialog.addEventListener('click', (event) => {
            if (event.target === dialog) dialog.close();
        });
        dialog.addEventListener('keydown', (event) => {
            if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
                event.preventDefault();
                show(current + (event.key === 'ArrowLeft' ? -1 : 1));
            }
        });
        dialog.addEventListener('close', () => {
            document.body.classList.remove('gallery-open');
            opener?.focus();
        });
    });
})();
