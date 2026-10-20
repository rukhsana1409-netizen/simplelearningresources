document.addEventListener("DOMContentLoaded", () => {
    const navigation = document.querySelector(".main-nav");
    const toggle = navigation?.querySelector(".mobile-menu-toggle");
    const mobileQuery = window.matchMedia("(max-width: 768px)");
    if (!navigation || !toggle) return;

    const closeNavigation = () => {
        navigation.classList.remove("mobile-menu-open");
        navigation.querySelectorAll(".dropdown").forEach((dropdown) => {
            dropdown.classList.remove("mobile-dropdown-open");
            dropdown.querySelector(":scope > a").setAttribute("aria-expanded", "false");
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
        const dropdown = trigger.parentElement;
        trigger.setAttribute("aria-haspopup", "true");
        trigger.setAttribute("aria-expanded", "false");
        dropdown.addEventListener("focusin", () => {
            if (!mobileQuery.matches) trigger.setAttribute("aria-expanded", "true");
        });
        dropdown.addEventListener("focusout", (event) => {
            if (!mobileQuery.matches && !dropdown.contains(event.relatedTarget)) {
                trigger.setAttribute("aria-expanded", "false");
            }
        });
        trigger.addEventListener("click", (event) => {
            if (!mobileQuery.matches) return;
            event.preventDefault();
            const isOpen = dropdown.classList.toggle("mobile-dropdown-open");
            trigger.setAttribute("aria-expanded", String(isOpen));
        });
    });

    mobileQuery.addEventListener("change", (event) => {
        if (!event.matches) closeNavigation();
    });
});
