function windowSmoothScrollTo(element, duration) {
    console.log('into function');
    const startingY = window.scrollY;
    const elementRect = element.getBoundingClientRect();

    // Calculate the element's top position relative to the window
    const elementTop = elementRect.top + startingY;

    // Set the target to the element's top position
    const targetY = elementTop;
    const diff = targetY - startingY;
    let start;

    // Easing function: easeInOutCubic
    //https://gist.github.com/gre/1650294
    function easeInOutCubic(t) {
        return t < 0.5 ? 4 * t * t * t : (t - 1) * (2 * t - 2) * (2 * t - 2) + 1;
    }

    function step(timestamp) {
        if (!start) start = timestamp;
        const time = timestamp - start;
        let percent = Math.min(time / duration, 1);
        percent = easeInOutCubic(percent);
        window.scrollTo(0, startingY + diff * percent);
        if (time < duration) {
            window.requestAnimationFrame(step);
        }
    }

    window.requestAnimationFrame(step);
}



aboutButton = document.getElementById('about-button');
//if clicked, scroll to about section
aboutButton.addEventListener('click', function () {
    console.log('clicked');
    let aboutSection = document.getElementById('about-section');
    windowSmoothScrollTo(aboutSection, 1000);

});

FAQButton = document.getElementById('FAQ-button');
//if clicked, scroll to FAQ section
FAQButton.addEventListener('click', function () {
    console.log('clicked');
    let FAQSection = document.getElementById('FAQ-section');
    windowSmoothScrollTo(FAQSection, 1000);

});

function reveal() {
    let reveals = document.querySelectorAll(".reveal");

    reveals.forEach(reveal => {
        let windowHeight = window.innerHeight;
        let elementTop = reveal.getBoundingClientRect().top;
        let elementVisible = 50;

        if (elementTop < windowHeight - elementVisible) {
            reveal.classList.add("active");
        } /*else {
            reveal.classList.remove("active");
        }*/
    });
}

window.addEventListener("scroll", reveal);