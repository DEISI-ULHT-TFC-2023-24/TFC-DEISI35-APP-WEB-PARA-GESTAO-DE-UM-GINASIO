document.addEventListener('DOMContentLoaded', function() {
    const servicesSection = document.getElementById('services');
    const servicesContent = servicesSection.querySelector('.services-content');

    window.addEventListener('scroll', function() {
        const sectionTop = servicesSection.getBoundingClientRect().top;
        const triggerPoint = window.innerHeight - 100;

        if (sectionTop < triggerPoint) {
            servicesContent.classList.add('scroll-active');
        } else {
            servicesContent.classList.remove('scroll-active');
        }
    });
});
