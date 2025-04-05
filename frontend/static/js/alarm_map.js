const openModalButtons = document.querySelectorAll(".openModal");
const closeModal = document.getElementById("closeModal");
const modal = document.getElementById("modal");
const regionName = document.getElementById("regionName");
const newsContainer = document.getElementById("newsContainer");
const n1 = document.getElementById("n1");
const n2 = document.getElementById("n2");
const n3 = document.getElementById("n3");

openModalButtons.forEach(button => {
    button.addEventListener("click", (event) => {
        const name = event.target.getAttribute('name');
        regionName.textContent = name + " oblast";
        const news = event.target.dataset.content.split('///');
        for (let n of [n1, n2, n3]) {
            n.textContent = news[[n1, n2, n3].indexOf(n)];
        }

        modal.classList.add("active");
        document.body.classList.add("modal-open");
    });
});

closeModal.addEventListener("click", () => {
    modal.classList.remove("active");
    document.body.classList.remove("modal-open");
});