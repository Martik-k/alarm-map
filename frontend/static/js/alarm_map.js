const openModalButtons = document.querySelectorAll(".openModal");
const closeModalButton = document.getElementById("closeModal");
const modal = document.getElementById("modal");
const regionNameH3 = document.getElementById("regionName");
const newsItemDivs = [
    document.getElementById("n1"),
    document.getElementById("n2"),
    document.getElementById("n3")
];

openModalButtons.forEach(button => {
    button.addEventListener("click", (event) => {
        const targetElement = event.target;
        const name = targetElement.getAttribute('name');
        const contentString = targetElement.dataset.content || '';
        const formattedRegionName = name.replace(/_/g, ' ') + " область";
        regionNameH3.textContent = formattedRegionName;
        const newsEntries = contentString.split('///');
        newsItemDivs.forEach((newsDiv, index) => {
            const headlineSpan = newsDiv.querySelector('.news-headline');
            const linkAnchor = newsDiv.querySelector('.news-link');

            if (headlineSpan && linkAnchor) {
                if (newsEntries[index]) {
                    const parts = newsEntries[index].split('::');
                    const headline = parts[0] ? parts[0].trim() : 'Немає заголовку';
                    const url = parts[1] ? parts[1].trim() : '#';

                    headlineSpan.textContent = headline;
                    linkAnchor.href = url;
                    newsDiv.style.display = 'flex';
                } else {
                    newsDiv.style.display = 'none';
                    headlineSpan.textContent = '';
                    linkAnchor.href = '#';
                }
            }
        });

        modal.classList.add("active");
        document.body.classList.add("modal-open");
    });
});

closeModalButton.addEventListener("click", () => {
    modal.classList.remove("active");
    document.body.classList.remove("modal-open");
});

modal.addEventListener('click', (event) => {
   if (event.target === modal) {
       modal.classList.remove("active");
       document.body.classList.remove("modal-open");
   }
});
