document.addEventListener("DOMContentLoaded", () => {
    const mobileQuery = window.matchMedia("(max-width: 768px)");

    if (!document.querySelector("footer")) {
        document.body.insertAdjacentHTML("beforeend", `<footer><div class="footer-content"><div class="footer-brand"><h3>Learning Made Simple</h3><p>Simple resources. Meaningful learning.</p></div><div class="footer-links"><div><h4>Explore</h4><a href="index.html">Home</a><a href="worksheets.html">All Resources</a><a href="about.html">About</a><a href="contact.html">Contact</a></div><div><h4>Information</h4><a href="privacy.html">Privacy Policy</a><a href="terms.html">Terms of Use</a><a href="disclaimer.html">Disclaimer</a></div></div></div><div class="footer-bottom"><p>&copy; 2026 Learning Made Simple. All rights reserved.</p></div></footer>`);
    }

    document.querySelectorAll(".main-nav").forEach((nav) => {
        const links = nav.querySelector(".nav-links");
        const logo = nav.querySelector(".logo");
        if (!links || !logo) return;
        links.innerHTML = `
            <a href="index.html">Home</a>
            <div class="dropdown"><a href="worksheets.html">Resources</a><div class="dropdown-menu"><a href="worksheets.html">All Resources</a><a href="math.html">Math</a><a href="reading.html">Reading &amp; Language</a><a href="communication.html">Communication &amp; Life Skills</a><a href="science.html">Science &amp; Discovery</a><a href="thinking-world.html">Thinking &amp; Our World</a></div></div>
            <div class="dropdown"><a href="preschool.html">By Grade</a><div class="dropdown-menu"><a href="preschool.html">Preschool</a><a href="kindergarten.html">Kindergarten</a><a href="grade-1.html">Grade 1</a><a href="grade-2.html">Grade 2</a></div></div>
            <a href="about.html">About</a><a href="contact.html">Contact</a>`;

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
const directoryScript=document.createElement("script");
directoryScript.src="directory.js";
directoryScript.defer=true;
document.head.appendChild(directoryScript);
