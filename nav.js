document.addEventListener("DOMContentLoaded", () => {
    const mobileQuery = window.matchMedia("(max-width: 768px)");

    document.querySelectorAll(".main-nav").forEach((nav) => {
        const links = nav.querySelector(".nav-links");
        const logo = nav.querySelector(".logo");
        if (!links || !logo) return;

        const button = document.createElement("button");
        button.className = "mobile-menu-toggle";
        button.type = "button";
        button.setAttribute("aria-label", "Open navigation menu");
        button.setAttribute("aria-expanded", "false");
        button.innerHTML = "<span></span><span></span><span></span>";
        logo.insertAdjacentElement("afterend", button);

        const closeMenu = () => {
            nav.classList.remove("mobile-menu-open");
            nav.querySelectorAll(".dropdown.mobile-dropdown-open").forEach((dropdown) => dropdown.classList.remove("mobile-dropdown-open"));
            button.setAttribute("aria-expanded", "false");
            button.setAttribute("aria-label", "Open navigation menu");
        };

        const syncDropdownLabels = () => {
            nav.querySelectorAll(".dropdown > a").forEach((trigger) => {
                if (!trigger.dataset.desktopLabel) trigger.dataset.desktopLabel = trigger.textContent;
                trigger.textContent = mobileQuery.matches
                    ? trigger.dataset.desktopLabel.replace(/\s*(?:▾|â–¾)\s*$/, "")
                    : trigger.dataset.desktopLabel;
            });
        };

        button.addEventListener("click", () => {
            const isOpen = nav.classList.toggle("mobile-menu-open");
            if (!isOpen) nav.querySelectorAll(".dropdown.mobile-dropdown-open").forEach((dropdown) => dropdown.classList.remove("mobile-dropdown-open"));
            button.setAttribute("aria-expanded", String(isOpen));
            button.setAttribute("aria-label", isOpen ? "Close navigation menu" : "Open navigation menu");
        });

        nav.querySelectorAll(".dropdown > a").forEach((trigger) => {
            trigger.addEventListener("click", (event) => {
                if (!mobileQuery.matches) return;
                event.preventDefault();
                trigger.parentElement.classList.toggle("mobile-dropdown-open");
            });
        });

        links.querySelectorAll("a").forEach((link) => {
            if (link.parentElement.classList.contains("dropdown")) return;
            link.addEventListener("click", () => {
                if (mobileQuery.matches && !link.getAttribute("href").startsWith("#")) closeMenu();
            });
        });

        mobileQuery.addEventListener("change", (event) => {
            if (!event.matches) closeMenu();
            syncDropdownLabels();
        });

        syncDropdownLabels();
    });
});
