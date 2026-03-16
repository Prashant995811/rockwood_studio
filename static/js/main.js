const navToggle = document.getElementById("navToggle");
const mainNav = document.getElementById("mainNav");
const backToTop = document.getElementById("backToTop");
const lightbox = document.getElementById("lightbox");
const lightboxImage = document.getElementById("lightboxImage");
const lightboxTitle = document.getElementById("lightboxTitle");
const lightboxClose = document.getElementById("lightboxClose");

document.body.classList.add("js-ready");

if (navToggle && mainNav) {
    navToggle.addEventListener("click", () => {
        mainNav.classList.toggle("open");
    });
}

if (backToTop) {
    window.addEventListener("scroll", () => {
        backToTop.style.display = window.scrollY > 260 ? "grid" : "none";
    });

    backToTop.addEventListener("click", () => {
        window.scrollTo({ top: 0, behavior: "smooth" });
    });
}

if (lightbox) {
    document.querySelectorAll("[data-lightbox]").forEach((button) => {
        button.addEventListener("click", () => {
            lightboxImage.src = button.dataset.lightbox;
            lightboxImage.alt = button.dataset.title || "Gallery preview";
            lightboxTitle.textContent = button.dataset.title || "";
            lightbox.classList.add("is-open");
        });
    });

    const closeLightbox = () => {
        lightbox.classList.remove("is-open");
        lightboxImage.src = "";
    };

    if (lightboxClose) {
        lightboxClose.addEventListener("click", closeLightbox);
    }

    lightbox.addEventListener("click", (event) => {
        if (event.target === lightbox) {
            closeLightbox();
        }
    });
}

const revealItems = document.querySelectorAll(".hero-section, .page-hero, .section");

if (revealItems.length) {
    const revealObserver = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("is-visible");
                    revealObserver.unobserve(entry.target);
                }
            });
        },
        {
            threshold: 0.12,
        }
    );

    revealItems.forEach((item) => {
        revealObserver.observe(item);
    });
}
