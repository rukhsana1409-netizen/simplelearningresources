document.addEventListener("DOMContentLoaded", () => {
    const navigation = document.querySelector(".main-nav");
    const toggle = navigation?.querySelector(".mobile-menu-toggle");
    const mobileQuery = window.matchMedia("(max-width: 768px)");
    if (!navigation || !toggle) return;

    const closeNavigation = () => {
        navigation.classList.remove("mobile-menu-open");
        navigation.querySelectorAll(".dropdown.mobile-dropdown-open").forEach((dropdown) => {
            dropdown.classList.remove("mobile-dropdown-open");
        });
        toggle.setAttribute("aria-expanded", "false");
        toggle.setAttribute("aria-label", "Open navigation menu");
    };

    toggle.addEventListener("click", () => {
        const isOpen = navigation.classList.toggle("mobile-menu-open");
        toggle.setAttribute("aria-expanded", String(isOpen));
        toggle.setAttribute("aria-label", isOpen ? "Close navigation menu" : "Open navigation menu");
    });

    navigation.querySelectorAll(".dropdown > a").forEach((trigger) => {
        trigger.addEventListener("click", (event) => {
            if (!mobileQuery.matches) return;
            event.preventDefault();
            trigger.parentElement.classList.toggle("mobile-dropdown-open");
        });
    });

    mobileQuery.addEventListener("change", (event) => {
        if (!event.matches) closeNavigation();
    });
});
